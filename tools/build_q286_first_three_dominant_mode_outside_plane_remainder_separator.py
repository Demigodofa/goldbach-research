"""Audit the outside-pair/complement remainder on the q286 window holdout.

The pair/complement false-positive autopsy showed that clear row 1200302 is
rescued outside the two-coordinate volatile plane.  This receipt recomputes
the predeclared 72-row window-closest denominator and asks whether the same
outside-plane remainder separates the stress deficit from all checked clears.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NEAR_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-near-boundary-selector-audit.json")
PLANE_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pair-complement-plane-audit.json")
OFFSET_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pair-complement-false-positive-offset.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-separator.json")
STRESS_TARGET = 1222142
EPSILONS = (0.01, 0.02, 0.03, 0.05, 0.075, 0.1)
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
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def label_tuple(label):
    return tuple(int(part) for part in label)


def summarize(values):
    values = tuple(float(value) for value in values)
    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None}
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": float(math.fsum(values) / len(values)),
    }


def pearson(left, right):
    left = tuple(float(value) for value in left)
    right = tuple(float(value) for value in right)
    if len(left) != len(right):
        raise ValueError("correlation inputs must have the same length")
    if not left:
        return math.nan
    left_mean = math.fsum(left) / len(left)
    right_mean = math.fsum(right) / len(right)
    left_delta = tuple(value - left_mean for value in left)
    right_delta = tuple(value - right_mean for value in right)
    denominator = math.sqrt(
        math.fsum(value * value for value in left_delta)
        * math.fsum(value * value for value in right_delta))
    if denominator == 0:
        return math.nan
    return math.fsum(
        a * b for a, b in zip(left_delta, right_delta)) / denominator


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


def compact_row(row):
    return {
        "target": int(row["target"]),
        "classification": (
            "clear" if row["dominant_floor_passes"] else "deficit"),
        "window_start": int(row["window_start"]),
        "window_role": row["window_role"],
        "target_mod_286": int(row["target_mod_286"]),
        "target_mod_10010": int(row["target_mod_10010"]),
        "absolute_above_floor_signed_surplus": float(
            row["absolute_above_floor_signed_surplus"]),
        "dominant_sum_to_principal": float(
            row["dominant_sum_to_principal"]),
        "adverse_pair_sum_to_principal": float(
            row["adverse_pair_sum_to_principal"]),
        "repair_complement_sum_to_principal": float(
            row["repair_complement_sum_to_principal"]),
        "volatile_pair_complement_total_to_principal": float(
            row["volatile_pair_complement_total_to_principal"]),
        "outside_pair_complement_plane_sum_to_principal": float(
            row["outside_pair_complement_plane_sum_to_principal"]),
        "outside_delta_to_stress": float(row["outside_delta_to_stress"]),
        "plane_total_delta_to_stress": float(
            row["plane_total_delta_to_stress"]),
        "dominant_sum_delta_to_stress": float(
            row["dominant_sum_delta_to_stress"]),
        "stress_plane_l1_distance": float(row["stress_plane_l1_distance"]),
        "stress_plane_linf_distance": float(row["stress_plane_linf_distance"]),
    }


def square_summary(rows, epsilon):
    selected = tuple(
        row for row in rows
        if row["stress_plane_linf_distance"] <= epsilon)
    clear_rows = tuple(row for row in selected if row["dominant_floor_passes"])
    deficit_rows = tuple(
        row for row in selected if not row["dominant_floor_passes"])
    return {
        "epsilon": float(epsilon),
        "selected_count": len(selected),
        "deficit_targets": tuple(row["target"] for row in deficit_rows),
        "clear_targets": tuple(row["target"] for row in clear_rows),
        "minimum_clear_outside_delta_to_stress": (
            min((row["outside_delta_to_stress"] for row in clear_rows),
                default=None)),
        "minimum_clear_dominant_sum_delta_to_stress": (
            min((row["dominant_sum_delta_to_stress"] for row in clear_rows),
                default=None)),
        "maximum_clear_plane_total_deficit_to_stress": (
            min((row["plane_total_delta_to_stress"] for row in clear_rows),
                default=None)),
        "rows": tuple(compact_row(row) for row in selected),
    }


def main():
    near_payload = json.loads(NEAR_SOURCE.read_text(encoding="utf-8"))
    plane_payload = json.loads(PLANE_SOURCE.read_text(encoding="utf-8"))
    json.loads(OFFSET_SOURCE.read_text(encoding="utf-8"))
    source_rows = collect_window_closest_rows(near_payload)
    targets = tuple(row["target"] for row in source_rows)
    if len(targets) != 72:
        raise AssertionError("window-closest denominator drifted")
    if STRESS_TARGET not in targets:
        raise AssertionError("stress target missing")

    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=targets, dominant_modes=(1, 2), tail_threshold=.3,
        top_channel_count=40)
    volatile_labels = tuple(
        label_tuple(label) for label in plane_payload["volatile_labels"])
    adverse_pair = tuple(
        label_tuple(label) for label in plane_payload["adverse_pair"])

    rows = []
    for source_row in source_rows:
        target = source_row["target"]
        profile_row = profile["target_rows"][target]
        if not profile_row["has_strict_central_prime_pairs"]:
            raise AssertionError(f"target {target} lacks strict pairs")
        channel_map = {
            label_tuple(item["representative_label"]): float(
                item["contribution_to_principal_ratio"])
            for item in profile_row["real_channel_contribution_rows"]
        }
        pair_sum = math.fsum(channel_map[label] for label in adverse_pair)
        complement_sum = math.fsum(
            channel_map[label] for label in volatile_labels
            if label not in adverse_pair)
        plane_total = pair_sum + complement_sum
        outside_sum = (
            float(source_row["dominant_sum_to_principal"]) - plane_total)
        rows.append({
            **source_row,
            "dominant_floor_passes": bool(
                profile_row["dominant_floor_passes"]),
            "adverse_pair_sum_to_principal": pair_sum,
            "repair_complement_sum_to_principal": complement_sum,
            "volatile_pair_complement_total_to_principal": plane_total,
            "outside_pair_complement_plane_sum_to_principal": outside_sum,
        })

    stress = next(row for row in rows if row["target"] == STRESS_TARGET)
    for row in rows:
        row["stress_plane_l1_distance"] = (
            abs(row["adverse_pair_sum_to_principal"]
                - stress["adverse_pair_sum_to_principal"])
            + abs(row["repair_complement_sum_to_principal"]
                  - stress["repair_complement_sum_to_principal"]))
        row["stress_plane_linf_distance"] = max(
            abs(row["adverse_pair_sum_to_principal"]
                - stress["adverse_pair_sum_to_principal"]),
            abs(row["repair_complement_sum_to_principal"]
                - stress["repair_complement_sum_to_principal"]))
        row["outside_delta_to_stress"] = (
            row["outside_pair_complement_plane_sum_to_principal"]
            - stress["outside_pair_complement_plane_sum_to_principal"])
        row["plane_total_delta_to_stress"] = (
            row["volatile_pair_complement_total_to_principal"]
            - stress["volatile_pair_complement_total_to_principal"])
        row["dominant_sum_delta_to_stress"] = (
            row["dominant_sum_to_principal"]
            - stress["dominant_sum_to_principal"])

    deficit_rows = tuple(
        row for row in rows if not row["dominant_floor_passes"])
    clear_rows = tuple(row for row in rows if row["dominant_floor_passes"])
    if tuple(row["target"] for row in deficit_rows) != (STRESS_TARGET,):
        raise AssertionError("deficit set drifted")

    minimum_clear_outside_row = min(
        clear_rows, key=lambda row: row["outside_delta_to_stress"])
    if minimum_clear_outside_row["target"] != 1242118:
        raise AssertionError("minimum clear outside row drifted")
    if minimum_clear_outside_row["outside_delta_to_stress"] <= 0:
        raise AssertionError("outside-plane remainder no longer separates")
    if not all(row["outside_delta_to_stress"] > 0 for row in clear_rows):
        raise AssertionError("a clear row is not above stress outside remainder")

    square_summaries = tuple(square_summary(rows, epsilon)
                             for epsilon in EPSILONS)
    all_window_square = square_summary(rows, math.inf)

    sorted_by_outside = tuple(sorted(
        rows, key=lambda row: (
            row["outside_pair_complement_plane_sum_to_principal"],
            row["target"])))
    sorted_by_plane = tuple(sorted(
        rows, key=lambda row: (
            row["stress_plane_l1_distance"],
            row["target"])))

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_near_boundary_selector_audit": str(
            NEAR_SOURCE.relative_to(ROOT)),
        "source_pair_complement_plane_audit": str(
            PLANE_SOURCE.relative_to(ROOT)),
        "source_false_positive_offset": str(
            OFFSET_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite outside-plane remainder separator audit only; stress "
            "row 1222142 is the unique minimum outside-remainder row on the "
            "predeclared 72-row denominator, but no uniform outside-remainder "
            "theorem, three-part balance theorem, signed projection theorem, "
            "or Goldbach proof is established"),
        "candidate": (
            "The outside-pair/complement dominant remainder may be the "
            "missing separator that explains why rows close to the stress "
            "target in the volatile plane can still clear."),
        "mechanism": (
            "Recompute exact q286 signed channel profiles for the 72 "
            "window-closest rows.  Split the full dominant first-three sum "
            "into named pair, six-channel complement, and the remainder "
            "outside that two-coordinate volatile plane."),
        "prediction": (
            "If the outside-plane remainder is the finite separator, every "
            "checked clear row should have outside remainder above stress "
            "row 1222142, including rows inside the .02 and .03 "
            "pair/complement boxes."),
        "falsifier": (
            "A checked clear with outside remainder at or below the stress "
            "row, or another deficit above the stress outside remainder, "
            "would falsify this finite separator formulation."),
        "novelty_label": "new-to-this-task",
        "arithmetic_modulus": near_payload["arithmetic_modulus"],
        "support": near_payload["support"],
        "window_specs": near_payload["window_specs"],
        "expanded_target_count": len(rows),
        "deficit_targets": tuple(row["target"] for row in deficit_rows),
        "clear_count": len(clear_rows),
        "adverse_pair": tuple(adverse_pair),
        "volatile_labels": tuple(volatile_labels),
        "stress_row": compact_row(stress),
        "minimum_clear_outside_remainder_row": compact_row(
            minimum_clear_outside_row),
        "minimum_clear_outside_delta_to_stress": float(
            minimum_clear_outside_row["outside_delta_to_stress"]),
        "square_summaries": square_summaries,
        "all_window_square_summary": all_window_square,
        "rows_by_outside_remainder": tuple(
            compact_row(row) for row in sorted_by_outside),
        "nearest_plane_rows": tuple(
            compact_row(row) for row in sorted_by_plane[:20]),
        "summaries": {
            "outside_pair_complement_plane_sum_to_principal": summarize(
                row["outside_pair_complement_plane_sum_to_principal"]
                for row in rows),
            "outside_delta_to_stress": summarize(
                row["outside_delta_to_stress"] for row in rows),
            "plane_total_delta_to_stress": summarize(
                row["plane_total_delta_to_stress"] for row in rows),
            "dominant_sum_delta_to_stress": summarize(
                row["dominant_sum_delta_to_stress"] for row in rows),
        },
        "correlations": {
            "pearson_abs_surplus_vs_outside_remainder": pearson(
                (row["absolute_above_floor_signed_surplus"] for row in rows),
                (row["outside_pair_complement_plane_sum_to_principal"]
                 for row in rows)),
            "pearson_abs_surplus_vs_outside_delta_to_stress": pearson(
                (row["absolute_above_floor_signed_surplus"] for row in rows),
                (row["outside_delta_to_stress"] for row in rows)),
            "pearson_abs_surplus_vs_plane_total_delta_to_stress": pearson(
                (row["absolute_above_floor_signed_surplus"] for row in rows),
                (row["plane_total_delta_to_stress"] for row in rows)),
        },
        "summary": {
            "outside_remainder_separator": (
                "On the predeclared 72-row denominator, stress row 1222142 "
                "is the unique minimum outside-pair/complement remainder row; "
                "all 71 clears have positive outside delta to stress."),
            "minimum_clear_gap": (
                "The closest clear by outside remainder is 1242118, with "
                "outside delta to stress about 0.0398241886."),
            "danger_box_behavior": (
                "Inside the .03 pair/complement box, all six clear rows have "
                "positive outside delta to stress; the smallest is again "
                "1242118."),
            "theorem_shape": (
                "The finite signal shifts the target from a pure plane box to "
                "a lower bound on the outside-plane remainder, conditioned by "
                "the volatile pair/complement placement."),
        },
        "interpretation": {
            "hole_status": (
                "The loop is tightening around an outside-remainder floor: "
                "the two-coordinate plane locates the danger zone, while the "
                "omitted dominant remainder separates the checked clears from "
                "the stress deficit."),
            "route_status": (
                "Preserve this as a finite separator and theorem target only; "
                "it is stress-centered and not a uniform arithmetic estimate."),
            "remaining_theorem": (
                "Prove a non-post-hoc lower bound for the outside-plane "
                "dominant remainder under the relevant pair/complement "
                "placement conditions, or replace the decomposition with a "
                "stronger signed aggregate theorem."),
        },
        "outside_plane_remainder_separator_measured": True,
        "stress_unique_minimum_outside_remainder_on_holdout": True,
        "all_checked_clears_above_stress_outside_remainder": True,
        "outside_remainder_theorem_proved": False,
        "three_part_balance_theorem_proved": False,
        "arithmetic_placement_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }

    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
