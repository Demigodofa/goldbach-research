"""Autopsy the fifth Octave SVD mode for the q286 volatile ledger.

The previous rank audit found that rank 5 is the first truncation that
classifies every selected row.  This receipt asks what the fifth mode is
actually doing, especially at the stress row 1222142.
"""

from __future__ import annotations

import csv
import json
import math
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RANK_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-octave-svd-rank-audit.json")
MAGNITUDE_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-polarity-magnitude-ledger.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-octave-rank5-autopsy.json")


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


def run_octave_mode_autopsy(matrix_rows, base_rows):
    with tempfile.TemporaryDirectory(prefix="q286_octave_rank5_") as temp:
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
M4 = U(:,1:4) * S(1:4,1:4) * V(:,1:4)';
M5 = U(:,1:5) * S(1:5,1:5) * V(:,1:5)';
C5 = S(5,5) * U(:,5) * V(:,5)';
rank4_margins = b + sum(M4, 2);
rank5_margins = b + sum(M5, 2);
rank5_row_sums = sum(C5, 2);
out = struct(
  'octave_version', OCTAVE_VERSION(),
  'singular_values', sv',
  'rank4_margins', rank4_margins',
  'rank5_margins', rank5_margins',
  'rank5_increment_row_sums', rank5_row_sums',
  'rank5_component', C5,
  'rank5_left_singular_vector', U(:,5)',
  'rank5_right_singular_vector', V(:,5)'
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


def descending_abs(items, value_key):
    return tuple(sorted(
        items, key=lambda item: abs(float(item[value_key])), reverse=True))


def channel_side(row, label):
    label = list(label)
    if label in row["sign_expected_repair_channels"]:
        return "repair"
    if label in row["sign_expected_adverse_channels"]:
        return "adverse"
    return "neutral"


def target_row(rows, target):
    return next(row for row in rows if int(row["target"]) == target)


def main():
    rank_payload = json.loads(RANK_SOURCE.read_text(encoding="utf-8"))
    magnitude_payload = json.loads(
        MAGNITUDE_SOURCE.read_text(encoding="utf-8"))
    labels = tuple(label_tuple(label) for label in rank_payload[
        "volatile_labels"])
    targets = tuple(int(target) for target in rank_payload["target_order"])
    oriented_rows = tuple(
        tuple(float(value) for value in row["oriented_channel_values"])
        for row in rank_payload["oriented_rows"])
    oriented_base = tuple(
        float(row["oriented_base_margin"])
        for row in rank_payload["oriented_rows"])

    octave_payload = run_octave_mode_autopsy(oriented_rows, oriented_base)
    rank4_margins = as_float_list(octave_payload["rank4_margins"])
    rank5_margins = as_float_list(octave_payload["rank5_margins"])
    rank5_increments = as_float_list(
        octave_payload["rank5_increment_row_sums"])
    rank5_component = as_matrix(octave_payload["rank5_component"])
    right5 = as_float_list(octave_payload["rank5_right_singular_vector"])
    left5 = as_float_list(octave_payload["rank5_left_singular_vector"])

    stress_index = targets.index(1222142)
    # SVD vector signs are arbitrary.  Canonicalize only the reported vectors
    # so the stress-row row-sum rescue is positive; the component itself is
    # sign-invariant and is never altered.
    sign = 1.0 if rank5_increments[stress_index] >= 0 else -1.0
    canonical_right5 = tuple(sign * value for value in right5)
    canonical_left5 = tuple(sign * value for value in left5)

    failing_rank4 = tuple(
        target for target, margin in zip(targets, rank4_margins)
        if margin <= 0)
    rescued_by_rank5 = tuple(
        target for target, margin4, margin5 in zip(
            targets, rank4_margins, rank5_margins)
        if margin4 <= 0 and margin5 > 0)
    if failing_rank4 != tuple(
            int(target) for target in rank_payload["rank_records"][3][
                "failing_targets"]):
        raise AssertionError("rank-4 failing target set drifted")
    if set(rescued_by_rank5) != set(failing_rank4):
        raise AssertionError("rank-5 did not rescue all rank-4 failures")

    channel_loadings = tuple({
        "label": label,
        "right_singular_vector_loading": canonical_right5[index],
        "absolute_loading": abs(canonical_right5[index]),
    } for index, label in enumerate(labels))

    row_effects = []
    rows_by_target = {
        int(row["target"]): row for row in magnitude_payload["rows"]
    }
    for row_index, target in enumerate(targets):
        source_row = rows_by_target[target]
        per_channel = []
        for channel_index, label in enumerate(labels):
            component_value = rank5_component[row_index][channel_index]
            per_channel.append({
                "label": label,
                "rank5_component_contribution": component_value,
                "absolute_rank5_component_contribution": abs(
                    component_value),
                "stress_or_row_side": channel_side(source_row, label),
            })
        row_effects.append({
            "target": target,
            "dominant_floor_passes": source_row["dominant_floor_passes"],
            "rank4_oriented_margin": rank4_margins[row_index],
            "rank5_oriented_margin": rank5_margins[row_index],
            "rank5_row_sum_increment": rank5_increments[row_index],
            "rank5_rescues_rank4_failure": (
                rank4_margins[row_index] <= 0 and rank5_margins[row_index] > 0),
            "full_oriented_margin": float(
                rank_payload["rank_records"][7][
                    "oriented_margins_by_target"][str(target)]),
            "rank5_component_by_channel": descending_abs(
                per_channel, "rank5_component_contribution"),
        })

    stress_source_row = target_row(magnitude_payload["rows"], 1222142)
    stress_effect = row_effects[stress_index]
    stress_channels = stress_effect["rank5_component_by_channel"]
    stress_repair_sum = sum(
        item["rank5_component_contribution"] for item in stress_channels
        if item["stress_or_row_side"] == "repair")
    stress_adverse_sum = sum(
        item["rank5_component_contribution"] for item in stress_channels
        if item["stress_or_row_side"] == "adverse")
    stress_abs_repair_sum = sum(
        abs(item["rank5_component_contribution"]) for item in stress_channels
        if item["stress_or_row_side"] == "repair")
    stress_abs_adverse_sum = sum(
        abs(item["rank5_component_contribution"]) for item in stress_channels
        if item["stress_or_row_side"] == "adverse")

    top_abs_loadings = descending_abs(
        channel_loadings, "right_singular_vector_loading")
    top_stress_components = stress_channels[:4]
    adverse_pair = ((1, 7), (4, 4))
    adverse_pair_stress_sum = sum(
        item["rank5_component_contribution"] for item in stress_channels
        if tuple(item["label"]) in adverse_pair)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_octave_svd_rank_audit": str(RANK_SOURCE.relative_to(ROOT)),
        "source_polarity_magnitude_ledger": str(
            MAGNITUDE_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite Octave rank-5 mode autopsy only; no low-rank theorem, "
            "rank-5 theorem, volatile-rim theorem, selected-fixture "
            "classifier theorem, pointwise character-sum estimate, or "
            "Goldbach proof is established"),
        "candidate": (
            "The fifth SVD mode might be the linear shadow of the named "
            "adverse-pair absorption hinge at stress row 1222142."),
        "mechanism": (
            "Use Octave to isolate the rank-5 increment C5 = sigma_5 u_5 "
            "v_5^T.  Compare rank-4 and rank-5 reconstructed oriented "
            "margins, then inspect the fifth right singular vector and the "
            "stress-row channel contributions."),
        "prediction": (
            "If rank 5 is a theorem-shaped correction, its stress-row "
            "increment should rescue the rank-4 failure through a named "
            "channel pattern rather than diffuse numerical cleanup."),
        "falsifier": (
            "If the fifth vector is mixed across several volatile labels and "
            "the stress-row rescue is not concentrated on the adverse pair, "
            "then rank 5 remains diagnostic and not a direct proof route."),
        "novelty_label": "new-to-this-task",
        "octave": {
            "used": True,
            "version": octave_payload["octave_version"],
            "operation": (
                "svd(M, 'econ') plus explicit sigma_5*u_5*v_5' component "
                "audit"),
            "reported_singular_vectors_canonicalized": (
                "u5 and v5 signs are flipped if needed so the stress-row "
                "rank-5 row-sum increment is positive; the rank-5 component "
                "matrix is sign-invariant"),
        },
        "arithmetic_modulus": rank_payload["arithmetic_modulus"],
        "support": rank_payload["support"],
        "dominant_modes": rank_payload["dominant_modes"],
        "tail_threshold": rank_payload["tail_threshold"],
        "target_order": targets,
        "volatile_labels": labels,
        "singular_value_5": float(octave_payload["singular_values"][4]),
        "rank4_energy_fraction": rank_payload[
            "cumulative_energy_fraction"][3],
        "rank5_energy_fraction": rank_payload[
            "cumulative_energy_fraction"][4],
        "rank4_failing_targets": failing_rank4,
        "rank5_rescued_targets": rescued_by_rank5,
        "rank5_right_singular_vector_by_channel": channel_loadings,
        "rank5_right_singular_vector_top_abs_channels": top_abs_loadings,
        "rank5_left_singular_vector_by_target": tuple({
            "target": target,
            "left_singular_vector_loading": canonical_left5[index],
            "absolute_loading": abs(canonical_left5[index]),
        } for index, target in enumerate(targets)),
        "rank5_row_effects": tuple(row_effects),
        "stress_target_1222142": {
            "rank4_oriented_margin": stress_effect["rank4_oriented_margin"],
            "rank5_row_sum_increment": stress_effect[
                "rank5_row_sum_increment"],
            "rank5_oriented_margin": stress_effect["rank5_oriented_margin"],
            "full_oriented_margin": stress_effect["full_oriented_margin"],
            "rank5_increment_to_rank4_deficit_ratio": (
                stress_effect["rank5_row_sum_increment"]
                / abs(stress_effect["rank4_oriented_margin"])),
            "rank5_adverse_pair_component_sum": adverse_pair_stress_sum,
            "rank5_repair_side_component_sum": stress_repair_sum,
            "rank5_adverse_side_component_sum": stress_adverse_sum,
            "rank5_abs_repair_side_component_sum": stress_abs_repair_sum,
            "rank5_abs_adverse_side_component_sum": stress_abs_adverse_sum,
            "rank5_top_abs_component_channels": top_stress_components,
            "stress_row_expected_repair_channels": tuple(
                label_tuple(label)
                for label in stress_source_row[
                    "sign_expected_repair_channels"]),
            "stress_row_expected_adverse_channels": tuple(
                label_tuple(label)
                for label in stress_source_row[
                    "sign_expected_adverse_channels"]),
        },
        "summary": {
            "rank5_rescue": (
                "The fifth Octave SVD mode rescues exactly the five selected "
                "rows that failed at rank 4."),
            "stress_row": (
                "At 1222142, rank 4 has negative oriented margin, while the "
                "rank-5 row-sum increment is larger than that deficit and "
                "moves the rank-5 reconstruction positive."),
            "mode_shape": (
                "The fifth right singular vector is mixed across volatile "
                "labels; the stress-row rank-5 increment is not concentrated "
                "as a clean adverse-pair-only correction."),
        },
        "interpretation": {
            "hole_status": (
                "The finite q286 loop is still tightening: rank 5 names the "
                "first SVD correction that closes the selected fixture, but "
                "the correction is a mixed channel balance rather than an "
                "obvious two-channel theorem."),
            "route_status": (
                "Octave remains useful for exposing the shape of the hole, "
                "but the fifth mode does not replace the explicit "
                "six-versus-two adverse-absorption obligation."),
            "remaining_theorem": (
                "Prove the signed adverse-pair absorption balance from "
                "actual binary-prime residue weights, or find a stronger "
                "signed aggregate arithmetic-placement theorem."),
        },
        "rank5_mode_autopsy_measured": True,
        "rank5_named_adverse_pair_theorem_proved": False,
        "rank5_low_rank_theorem_proved": False,
        "volatile_threshold_theorem_proved": False,
        "volatile_rim_theorem_proved": False,
        "stable_core_theorem_proved": False,
        "selected_fixture_classifier_theorem_proved": False,
        "pointwise_character_sum_estimate_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }

    if payload["stress_target_1222142"][
            "rank5_increment_to_rank4_deficit_ratio"] <= 1:
        raise AssertionError("rank-5 stress increment no longer rescues")
    if tuple(payload["rank5_rescued_targets"]) != tuple(failing_rank4):
        raise AssertionError("rank-5 rescued target list drifted")

    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
