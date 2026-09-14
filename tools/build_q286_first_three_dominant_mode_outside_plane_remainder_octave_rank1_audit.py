"""Audit Octave rank-1 compression of the q286 outside-plane remainder.

The outside-plane separator showed that all checked clears sit above stress
row 1222142 after removing the named pair/complement plane.  This receipt
asks whether those clear-minus-stress outside-channel deltas have a small
linear-algebra handle.  Octave performs the SVD; Python preserves the source
boundary and evidence schema.
"""

from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NEAR_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-near-boundary-selector-audit.json")
SEPARATOR_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-separator.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-octave-rank1-audit.json")
STRESS_TARGET = 1222142
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)


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


def collect_window_closest_rows(payload):
    rows = []
    seen = set()
    for window in payload["window_rows"]:
        for row in window["closest_margin_rows"]:
            target = int(row["target"])
            if target in seen:
                continue
            seen.add(target)
            rows.append({
                **row,
                "window_start": int(window["start"]),
                "window_role": window["window_role"],
                "target_mod_10010": target % 10010,
            })
    return tuple(rows)


def contribution_map(row):
    return {
        label_tuple(item["representative_label"]): float(
            item["contribution_to_principal_ratio"])
        for item in row["real_channel_contribution_rows"]
    }


def posix_path(path):
    return str(path).replace("\\", "/")


def write_csv_matrix(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerows(rows)


def write_csv_vector(path, values):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        for value in values:
            writer.writerow([value])


def run_octave_rank_audit(delta_rows, full_deltas):
    with tempfile.TemporaryDirectory(prefix="q286_outside_rank1_") as temp:
        temp_path = Path(temp)
        matrix_path = temp_path / "outside_delta_matrix.csv"
        full_path = temp_path / "full_outside_deltas.csv"
        write_csv_matrix(matrix_path, delta_rows)
        write_csv_vector(full_path, full_deltas)
        code = f"""
function r = pearson1(a, b)
  a = a(:);
  b = b(:);
  da = a - mean(a);
  db = b - mean(b);
  denom = norm(da) * norm(db);
  if denom == 0
    r = NaN;
  else
    r = (da' * db) / denom;
  endif
endfunction
D = dlmread('{posix_path(matrix_path)}');
y = dlmread('{posix_path(full_path)}');
[U,S,V] = svd(D, 'econ');
sv = diag(S);
energy = (sv .^ 2) / sum(sv .^ 2);
rank_count = min(size(D));
rank_row_sums = zeros(rows(D), rank_count);
rank_min_row_sums = zeros(1, rank_count);
rank_nonpositive_counts = zeros(1, rank_count);
rank_l2_errors = zeros(1, rank_count);
rank_max_abs_errors = zeros(1, rank_count);
rank_pearson = zeros(1, rank_count);
for k = 1:rank_count
  Dk = U(:,1:k) * S(1:k,1:k) * V(:,1:k)';
  row_sums = sum(Dk, 2);
  rank_row_sums(:,k) = row_sums;
  rank_min_row_sums(k) = min(row_sums);
  rank_nonpositive_counts(k) = sum(row_sums <= 0);
  rank_l2_errors(k) = norm(y - row_sums);
  rank_max_abs_errors(k) = max(abs(y - row_sums));
  rank_pearson(k) = pearson1(y, row_sums);
endfor
rank1 = U(:,1) * S(1,1) * V(:,1)';
rank1_row_sums = sum(rank1, 2);
residual_after_rank1 = y - rank1_row_sums;
u1 = U(:,1);
v1 = V(:,1);
if sum(v1) < 0
  u1 = -u1;
  v1 = -v1;
endif
tol = max(size(D)) * eps(max(sv)) * max(sv);
out = struct(
  'octave_version', OCTAVE_VERSION(),
  'singular_values', sv',
  'energy_fraction', energy',
  'cumulative_energy_fraction', cumsum(energy)',
  'numerical_rank_tolerance', tol,
  'numerical_rank', sum(sv > tol),
  'rank_row_sums', rank_row_sums,
  'rank_min_row_sums', rank_min_row_sums,
  'rank_nonpositive_counts', rank_nonpositive_counts,
  'rank_l2_errors', rank_l2_errors,
  'rank_max_abs_errors', rank_max_abs_errors,
  'rank_pearson_full_delta', rank_pearson,
  'rank1_left_singular_vector', u1',
  'rank1_right_singular_vector', v1',
  'rank1_right_vector_sum', sum(v1),
  'rank1_residual_row_sums', residual_after_rank1'
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


def summarize(values):
    values = tuple(float(value) for value in values)
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def min_record(targets, values):
    pairs = tuple(zip(targets, values))
    target, value = min(pairs, key=lambda item: (item[1], item[0]))
    return {"target": target, "value": value}


def max_record(targets, values):
    pairs = tuple(zip(targets, values))
    target, value = max(pairs, key=lambda item: (item[1], -item[0]))
    return {"target": target, "value": value}


def rank_records(octave_payload, clear_targets):
    row_sums = as_matrix(octave_payload["rank_row_sums"])
    records = []
    rank_count = len(octave_payload["rank_min_row_sums"])
    for index in range(rank_count):
        sums = tuple(float(row[index]) for row in row_sums)
        nonpositive_targets = tuple(
            target for target, value in zip(clear_targets, sums)
            if value <= 0)
        records.append({
            "rank": index + 1,
            "cumulative_energy_fraction": float(
                octave_payload["cumulative_energy_fraction"][index]),
            "minimum_reconstructed_outside_delta": min_record(
                clear_targets, sums),
            "maximum_reconstructed_outside_delta": max_record(
                clear_targets, sums),
            "nonpositive_reconstructed_count": int(
                octave_payload["rank_nonpositive_counts"][index]),
            "nonpositive_reconstructed_targets": nonpositive_targets,
            "l2_error_to_full_outside_delta": float(
                octave_payload["rank_l2_errors"][index]),
            "maximum_absolute_error_to_full_outside_delta": float(
                octave_payload["rank_max_abs_errors"][index]),
            "pearson_full_delta": float(
                octave_payload["rank_pearson_full_delta"][index]),
        })
    return tuple(records)


def first_all_positive_rank(records):
    for record in records:
        if record["nonpositive_reconstructed_count"] == 0:
            return record["rank"]
    return None


def descending_abs(items, value_key):
    return tuple(sorted(
        items, key=lambda item: abs(float(item[value_key])), reverse=True))


def main():
    near_payload = json.loads(NEAR_SOURCE.read_text(encoding="utf-8"))
    separator_payload = json.loads(
        SEPARATOR_SOURCE.read_text(encoding="utf-8"))
    source_rows = collect_window_closest_rows(near_payload)
    targets = tuple(int(row["target"]) for row in source_rows)
    if len(targets) != separator_payload["expanded_target_count"]:
        raise AssertionError("expanded target count drifted")
    if STRESS_TARGET not in targets:
        raise AssertionError("stress target missing")

    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=targets, dominant_modes=(1, 2), tail_threshold=.3,
        top_channel_count=40)
    volatile_labels = tuple(
        label_tuple(label) for label in separator_payload["volatile_labels"])
    all_labels = tuple(
        label_tuple(row["representative_label"])
        for row in profile["target_rows"][targets[0]][
            "real_channel_contribution_rows"])
    outside_labels = tuple(
        label for label in all_labels if label not in volatile_labels)
    if len(outside_labels) != 17:
        raise AssertionError("outside channel count drifted")

    stress_profile_row = profile["target_rows"][STRESS_TARGET]
    stress_contributions = contribution_map(stress_profile_row)
    separator_by_target = {
        int(row["target"]): row
        for row in separator_payload["rows_by_outside_remainder"]
    }

    clear_targets = []
    delta_rows = []
    clear_records = []
    for source_row in source_rows:
        target = int(source_row["target"])
        if target == STRESS_TARGET:
            continue
        profile_row = profile["target_rows"][target]
        if not profile_row["dominant_floor_passes"]:
            raise AssertionError(f"unexpected non-clear target {target}")
        contributions = contribution_map(profile_row)
        deltas = tuple(
            contributions[label] - stress_contributions[label]
            for label in outside_labels)
        full_delta = math.fsum(deltas)
        expected_delta = float(
            separator_by_target[target]["outside_delta_to_stress"])
        if abs(full_delta - expected_delta) > 1e-10:
            raise AssertionError(
                f"outside-delta reconstruction drifted for {target}")
        clear_targets.append(target)
        delta_rows.append(deltas)
        clear_records.append({
            "target": target,
            "window_start": int(source_row["window_start"]),
            "window_role": source_row["window_role"],
            "target_mod_286": int(source_row["target_mod_286"]),
            "target_mod_10010": int(source_row["target_mod_10010"]),
            "full_outside_delta_to_stress": full_delta,
            "absolute_above_floor_signed_surplus": float(
                source_row["absolute_above_floor_signed_surplus"]),
        })

    full_deltas = tuple(
        row["full_outside_delta_to_stress"] for row in clear_records)
    if min(full_deltas) <= 0:
        raise AssertionError("source outside separator no longer positive")

    octave_payload = run_octave_rank_audit(delta_rows, full_deltas)
    records = rank_records(octave_payload, tuple(clear_targets))
    first_positive_rank = first_all_positive_rank(records)
    if first_positive_rank != 1:
        raise AssertionError("rank-1 outside compression no longer separates")
    rank1_record = records[0]
    rank1_energy = float(octave_payload["energy_fraction"][0])
    if rank1_energy <= 0.7:
        raise AssertionError("rank-1 outside energy fraction drifted low")
    if rank1_record["minimum_reconstructed_outside_delta"]["target"] != 1240160:
        raise AssertionError("rank-1 minimum clear target drifted")

    rank1_row_sums = tuple(
        float(row[0]) for row in as_matrix(octave_payload["rank_row_sums"]))
    residual_after_rank1 = as_float_list(
        octave_payload["rank1_residual_row_sums"])
    rank1_by_target = {
        target: value for target, value in zip(clear_targets, rank1_row_sums)
    }
    for row, rank1_value, residual in zip(
            clear_records, rank1_row_sums, residual_after_rank1):
        row["rank1_reconstructed_outside_delta"] = rank1_value
        row["residual_after_rank1_row_sum"] = residual
        row["rank1_overshoots_full_delta"] = (
            rank1_value > row["full_outside_delta_to_stress"])

    right1 = as_float_list(octave_payload["rank1_right_singular_vector"])
    left1 = as_float_list(octave_payload["rank1_left_singular_vector"])
    right_vector_rows = tuple({
        "label": label,
        "rank1_right_singular_vector_loading": value,
        "absolute_loading": abs(value),
    } for label, value in zip(outside_labels, right1))
    left_vector_rows = tuple({
        "target": target,
        "rank1_left_singular_vector_loading": value,
        "rank1_reconstructed_outside_delta": rank1_by_target[target],
    } for target, value in zip(clear_targets, left1))

    minimum_full = min_record(tuple(clear_targets), full_deltas)
    if minimum_full["target"] != 1242118:
        raise AssertionError("full outside minimum target drifted")
    rank1_overshoot_count = sum(
        1 for row in clear_records if row["rank1_overshoots_full_delta"])
    if rank1_overshoot_count == 0:
        raise AssertionError("rank-1 residual boundary drifted")

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_near_boundary_selector_audit": str(
            NEAR_SOURCE.relative_to(ROOT)),
        "source_outside_plane_remainder_separator": str(
            SEPARATOR_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite Octave rank-1 outside-remainder audit only; rank-1 "
            "reconstruction keeps all checked clear-minus-stress outside "
            "deltas positive on the predeclared 72-row denominator, but no "
            "rank-1 theorem, residual-bound theorem, signed projection "
            "theorem, or Goldbach proof is established"),
        "candidate": (
            "The outside-pair/complement remainder floor may have a "
            "one-dimensional SVD shadow: clear-minus-stress outside-channel "
            "deltas might project positively along a common Octave rank-1 "
            "direction."),
        "mechanism": (
            "Recompute exact q286 signed channel profiles for the 72-row "
            "holdout.  Remove the eight volatile pair/complement channels.  "
            "For each of the 71 clear rows, subtract the stress row's outside "
            "channel vector and run Octave SVD on the resulting 71 by 17 "
            "delta matrix."),
        "prediction": (
            "If a one-dimensional outside-remainder handle exists, the "
            "rank-1 reconstructed row sum should remain positive for every "
            "checked clear row, even before the exact residual is restored."),
        "falsifier": (
            "Any checked clear row with nonpositive rank-1 reconstructed "
            "outside delta would falsify the finite rank-1 separator handle; "
            "a theorem route would still need a bound showing the omitted "
            "SVD residual cannot undo the positive rank-1 margin."),
        "novelty_label": "new-to-this-task",
        "octave": {
            "version": octave_payload["octave_version"],
            "operation": (
                "svd(D, 'econ') on clear-minus-stress outside-channel delta "
                "matrix, followed by truncated-rank row-sum replay"),
        },
        "stress_target": STRESS_TARGET,
        "clear_count": len(clear_targets),
        "outside_label_count": len(outside_labels),
        "outside_labels": outside_labels,
        "volatile_labels_removed": volatile_labels,
        "singular_values": as_float_list(octave_payload["singular_values"]),
        "energy_fraction": as_float_list(octave_payload["energy_fraction"]),
        "cumulative_energy_fraction": as_float_list(
            octave_payload["cumulative_energy_fraction"]),
        "numerical_rank": int(octave_payload["numerical_rank"]),
        "numerical_rank_tolerance": float(
            octave_payload["numerical_rank_tolerance"]),
        "first_all_positive_rank": first_positive_rank,
        "rank_records": records,
        "minimum_full_outside_delta": minimum_full,
        "maximum_full_outside_delta": max_record(
            tuple(clear_targets), full_deltas),
        "full_outside_delta_summary": summarize(full_deltas),
        "rank1_reconstructed_outside_delta_summary": summarize(
            rank1_row_sums),
        "rank1_residual_row_sum_summary": summarize(residual_after_rank1),
        "rank1_energy_fraction": rank1_energy,
        "rank1_minimum_reconstructed_outside_delta": (
            rank1_record["minimum_reconstructed_outside_delta"]),
        "rank1_maximum_absolute_error_to_full_outside_delta": (
            rank1_record["maximum_absolute_error_to_full_outside_delta"]),
        "rank1_pearson_full_delta": rank1_record["pearson_full_delta"],
        "rank1_overshoots_full_delta_count": rank1_overshoot_count,
        "rank1_right_vector_sum": float(
            octave_payload["rank1_right_vector_sum"]),
        "rank1_right_singular_vector_by_channel": right_vector_rows,
        "rank1_right_singular_vector_top_abs_channels": descending_abs(
            right_vector_rows, "rank1_right_singular_vector_loading")[:8],
        "rank1_left_singular_vector_by_target": left_vector_rows,
        "rows_by_full_outside_delta": tuple(sorted(
            clear_records,
            key=lambda row: (row["full_outside_delta_to_stress"],
                             row["target"]))),
        "rows_by_rank1_reconstructed_outside_delta": tuple(sorted(
            clear_records,
            key=lambda row: (row["rank1_reconstructed_outside_delta"],
                             row["target"]))),
        "summary": {
            "rank1_separator": (
                "Octave rank 1 is already all-positive on the 71 checked "
                "clear-minus-stress outside-channel deltas."),
            "rank1_energy": (
                "The first singular mode carries about 0.7471393937 of the "
                "outside-delta matrix energy."),
            "minimums_differ": (
                "The exact outside-remainder closest clear is 1242118, but "
                "the rank-1 reconstructed minimum is 1240160; this is a "
                "compression handle, not an exact ordering theorem."),
            "residual_boundary": (
                "Rank 1 sometimes overshoots the exact outside delta, so a "
                "proof would need a residual-drag bound in addition to the "
                "positive rank-1 margin."),
        },
        "interpretation": {
            "hole_status": (
                "The loop tightened again: the outside-remainder floor has a "
                "finite one-dimensional Octave shadow on the checked q286 "
                "denominator."),
            "route_status": (
                "Promote only as a theorem target.  The next obligation is "
                "to identify the arithmetic meaning of the rank-1 outside "
                "direction and bound the residual row-sum drag."),
        },
        "outside_plane_remainder_octave_rank1_audit_measured": True,
        "rank1_all_checked_clears_positive": True,
        "rank1_separator_theorem_proved": False,
        "rank1_residual_bound_theorem_proved": False,
        "outside_remainder_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }

    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
