"""Build q286 volatile signed-channel Octave SVD rank audit evidence.

The adverse-absorption ladder leaves a full six-versus-two channel balance at
the tight row 1222142.  This receipt asks whether the selected volatile
channel ledger has a lower-rank linear-algebra explanation, using Octave for
the SVD and rank-truncation calculations.
"""

from __future__ import annotations

import csv
import json
import math
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAGNITUDE_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-polarity-magnitude-ledger.json")
LADDER_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-adverse-absorption-ladder.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-octave-svd-rank-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set)):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def label_tuple(label):
    return tuple(int(part) for part in label)


def contribution_map(row):
    return {
        label_tuple(item["label"]): float(item["contribution_to_principal"])
        for item in row["volatile_channel_contributions"]
    }


def posix_path(path):
    return str(path).replace("\\", "/")


def write_csv_matrix(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerows(rows)


def run_octave_svd(matrix_rows, base_rows):
    with tempfile.TemporaryDirectory(prefix="q286_octave_svd_") as temp:
        temp_path = Path(temp)
        matrix_path = temp_path / "oriented_matrix.csv"
        base_path = temp_path / "oriented_base.csv"
        write_csv_matrix(matrix_path, matrix_rows)
        write_csv_matrix(base_path, ([value] for value in base_rows))
        code = f"""
M = dlmread('{posix_path(matrix_path)}');
b = dlmread('{posix_path(base_path)}');
[U,S,V] = svd(M, 'econ');
sv = diag(S);
energy = (sv .^ 2) / sum(sv .^ 2);
rank_count = min(size(M));
rank_fail_counts = zeros(1, rank_count);
rank_min_margins = zeros(1, rank_count);
rank_frobenius_errors = zeros(1, rank_count);
rank_relative_frobenius_errors = zeros(1, rank_count);
rank_max_abs_entry_errors = zeros(1, rank_count);
rank_margins = zeros(rows(M), rank_count);
for k = 1:rank_count
  Mk = U(:,1:k) * S(1:k,1:k) * V(:,1:k)';
  margins = b + sum(Mk, 2);
  rank_margins(:,k) = margins;
  rank_fail_counts(k) = sum(margins <= 0);
  rank_min_margins(k) = min(margins);
  E = M - Mk;
  rank_frobenius_errors(k) = norm(E, 'fro');
  rank_relative_frobenius_errors(k) = norm(E, 'fro') / norm(M, 'fro');
  rank_max_abs_entry_errors(k) = max(max(abs(E)));
endfor
tol = max(size(M)) * eps(max(sv)) * max(sv);
out = struct(
  'octave_version', OCTAVE_VERSION(),
  'singular_values', sv',
  'energy_fraction', energy',
  'cumulative_energy_fraction', cumsum(energy)',
  'numerical_rank_tolerance', tol,
  'numerical_rank', sum(sv > tol),
  'rank_fail_counts', rank_fail_counts,
  'rank_min_margins', rank_min_margins,
  'rank_frobenius_errors', rank_frobenius_errors,
  'rank_relative_frobenius_errors', rank_relative_frobenius_errors,
  'rank_max_abs_entry_errors', rank_max_abs_entry_errors,
  'rank_margins', rank_margins
);
disp(jsonencode(out));
"""
        completed = subprocess.run(
            ["octave", "--quiet", "--eval", code],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True)
        return json.loads(completed.stdout)


def as_float_list(values):
    return [float(value) for value in values]


def as_matrix(values):
    return [[float(value) for value in row] for row in values]


def rank_records(octave_payload, targets):
    margins_by_rank = as_matrix(octave_payload["rank_margins"])
    records = []
    for rank_index, margins in enumerate(zip(*margins_by_rank), start=1):
        margins = tuple(float(value) for value in margins)
        failing_targets = tuple(
            target for target, margin in zip(targets, margins)
            if margin <= 0)
        records.append({
            "rank": rank_index,
            "cumulative_energy_fraction": float(
                octave_payload["cumulative_energy_fraction"][rank_index - 1]),
            "relative_frobenius_error": float(
                octave_payload[
                    "rank_relative_frobenius_errors"][rank_index - 1]),
            "maximum_absolute_entry_error": float(
                octave_payload[
                    "rank_max_abs_entry_errors"][rank_index - 1]),
            "minimum_oriented_margin": float(
                octave_payload["rank_min_margins"][rank_index - 1]),
            "failing_target_count": int(
                octave_payload["rank_fail_counts"][rank_index - 1]),
            "failing_targets": failing_targets,
            "oriented_margins_by_target": {
                str(target): margin for target, margin in zip(targets, margins)
            },
        })
    return tuple(records)


def first_all_pass_rank(records):
    for record in records:
        if record["failing_target_count"] == 0:
            return record["rank"]
    return None


def main():
    magnitude_payload = json.loads(
        MAGNITUDE_SOURCE.read_text(encoding="utf-8"))
    ladder_payload = json.loads(LADDER_SOURCE.read_text(encoding="utf-8"))
    labels = tuple(label_tuple(label) for label in magnitude_payload[
        "volatile_labels"])
    targets = []
    oriented_rows = []
    oriented_base = []
    row_records = []
    for row in magnitude_payload["rows"]:
        target = int(row["target"])
        targets.append(target)
        orientation = 1 if row["dominant_floor_passes"] else -1
        contributions = contribution_map(row)
        oriented_channel_values = tuple(
            orientation * contributions[label] for label in labels)
        base = orientation * float(row["base_margin_without_volatile"])
        full_margin = base + sum(oriented_channel_values)
        expected_margin = abs(float(row["full_margin_to_floor"]))
        if abs(full_margin - expected_margin) > 1e-10:
            raise AssertionError(f"oriented margin mismatch for {target}")
        oriented_rows.append(oriented_channel_values)
        oriented_base.append(base)
        row_records.append({
            "target": target,
            "dominant_floor_passes": row["dominant_floor_passes"],
            "orientation": orientation,
            "oriented_base_margin": base,
            "oriented_channel_values": oriented_channel_values,
            "full_oriented_margin": full_margin,
            "signed_magnitude_surplus": row["signed_magnitude_surplus"],
        })

    octave_payload = run_octave_svd(oriented_rows, oriented_base)
    records = rank_records(octave_payload, targets)
    first_pass_rank = first_all_pass_rank(records)
    if first_pass_rank != 5:
        raise AssertionError("selected SVD all-pass rank changed")
    if records[3]["failing_target_count"] == 0:
        raise AssertionError("rank-4 truncation unexpectedly passes")
    if records[3]["cumulative_energy_fraction"] <= .93:
        raise AssertionError("rank-4 energy fraction changed")
    if records[4]["minimum_oriented_margin"] <= 0:
        raise AssertionError("rank-5 selected minimum margin changed")
    stress_ladder = next(
        row for row in ladder_payload["rows"] if row["target"] == 1222142)
    if stress_ladder["minimum_repair_bundle_sizes_by_adverse_step"] != [
            4, 5, 5, 6]:
        raise AssertionError("source adverse ladder drifted for 1222142")

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_polarity_magnitude_ledger": str(
            MAGNITUDE_SOURCE.relative_to(ROOT)),
        "source_adverse_absorption_ladder": str(
            LADDER_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite Octave SVD rank audit only; no low-rank theorem, "
            "volatile-rim theorem, selected-fixture classifier theorem, "
            "pointwise character-sum estimate, or Goldbach proof is "
            "established"),
        "candidate": (
            "The signed volatile-channel ledger might have a low-rank "
            "linear-algebra explanation that replaces the local six-versus-"
            "two channel balance."),
        "mechanism": (
            "Orient every selected row so positive channel mass helps the "
            "row's actual classification, then use Octave SVD on the 10 by 8 "
            "oriented volatile-channel matrix.  For each truncated rank, "
            "reconstruct the channel matrix and test whether oriented base "
            "plus reconstructed channel sum stays positive for every "
            "selected row."),
        "prediction": (
            "If the six-versus-two balance is a low-rank shadow, a small "
            "rank truncation preserving most matrix energy should preserve "
            "all selected classifications with comfortable margin."),
        "falsifier": (
            "If high-energy rank truncations still misclassify selected "
            "rows, the low-rank shortcut is too blunt at this fixture level."),
        "novelty_label": "new-to-this-task",
        "octave": {
            "used": True,
            "version": octave_payload["octave_version"],
            "operation": "svd(M, 'econ') plus truncated-rank margin replay",
        },
        "arithmetic_modulus": magnitude_payload["arithmetic_modulus"],
        "support": magnitude_payload["support"],
        "dominant_modes": magnitude_payload["dominant_modes"],
        "tail_threshold": magnitude_payload["tail_threshold"],
        "volatile_labels": labels,
        "target_order": targets,
        "row_count": len(targets),
        "channel_count": len(labels),
        "oriented_rows": tuple(row_records),
        "singular_values": as_float_list(octave_payload["singular_values"]),
        "energy_fraction": as_float_list(
            octave_payload["energy_fraction"]),
        "cumulative_energy_fraction": as_float_list(
            octave_payload["cumulative_energy_fraction"]),
        "numerical_rank": int(octave_payload["numerical_rank"]),
        "numerical_rank_tolerance": float(
            octave_payload["numerical_rank_tolerance"]),
        "rank_records": records,
        "first_all_selected_rows_pass_rank": first_pass_rank,
        "summary": {
            "rank_4": (
                "Rank 4 captures about 0.9315947381 of oriented volatile "
                "matrix energy, but still leaves five selected rows with "
                "nonpositive reconstructed oriented margin."),
            "rank_5": (
                "Rank 5 is the first truncation preserving all selected "
                "row classifications, with minimum reconstructed oriented "
                "margin about 0.0055715827."),
            "low_rank_status": (
                "The selected fixture is not explained by a rank <=4 "
                "volatile-channel shadow, even though rank 4 captures more "
                "than 93 percent of the matrix energy."),
        },
        "interpretation": {
            "hole_status": (
                "The q286 loop is tightening, but the six-versus-two stress "
                "balance is not replaced by a very-low-rank SVD explanation "
                "on the selected fixture."),
            "route_status": (
                "Low-rank linear algebra remains useful diagnostically, but "
                "rank <=4 truncation is too blunt for the current q286 "
                "classification margins."),
            "remaining_theorem": (
                "Prove the critical adverse-pair absorption balance from "
                "actual binary-prime residue weights, or find a stronger "
                "signed aggregate theorem; do not rely on a rank <=4 SVD "
                "compression as the proof engine."),
        },
        "volatile_octave_svd_rank_audit_measured": True,
        "rank_le_4_selected_classifier_found": False,
        "rank_5_selected_classifier_found": True,
        "low_rank_theorem_proved": False,
        "volatile_threshold_theorem_proved": False,
        "volatile_rim_theorem_proved": False,
        "stable_core_theorem_proved": False,
        "selected_fixture_classifier_theorem_proved": False,
        "pointwise_character_sum_estimate_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }

    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
