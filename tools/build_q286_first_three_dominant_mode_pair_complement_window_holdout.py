"""Hold out the q286 pair/complement plane on per-window closest rows.

The top-20 pair/complement audit found that small stress-centered boxes could
isolate the stress deficit.  This receipt expands the denominator to the
predeclared closest-margin rows from each near-boundary audit window and asks
whether that local isolation survives exact channel recomputation.
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
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pair-complement-window-holdout.json")
STRESS_TARGET = 1222142
EPSILONS = (0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.1)
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


def compact_near_row(row):
    return {
        "target": int(row["target"]),
        "window_start": int(row["window_start"]),
        "window_role": row["window_role"],
        "target_mod_286": int(row["target_mod_286"]),
        "target_mod_10010": int(row["target_mod_10010"]),
        "absolute_above_floor_signed_surplus": float(
            row["absolute_above_floor_signed_surplus"]),
        "above_floor_signed_surplus_to_threshold": float(
            row["above_floor_signed_surplus_to_threshold"]),
        "dominant_sum_to_principal": float(
            row["dominant_sum_to_principal"]),
        "nonportfolio_residual_sum_to_principal": float(
            row["nonportfolio_residual_sum_to_principal"]),
        "required_portfolio_for_floor": float(
            row["required_portfolio_for_floor"]),
        "above_floor_mass_fraction": float(row["above_floor_mass_fraction"]),
        "above_floor_mass_threshold": float(row["above_floor_mass_threshold"]),
    }


def compact_plane_row(row):
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
        "adverse_pair_sum_to_principal": float(
            row["adverse_pair_sum_to_principal"]),
        "repair_complement_sum_to_principal": float(
            row["repair_complement_sum_to_principal"]),
        "volatile_total_sum_to_principal": float(
            row["volatile_total_sum_to_principal"]),
        "stress_plane_l1_distance": float(row["stress_plane_l1_distance"]),
        "stress_plane_linf_distance": float(row["stress_plane_linf_distance"]),
    }


def collect_window_closest_rows(near_payload):
    rows = []
    seen = set()
    for window in near_payload["window_rows"]:
        for row in window["closest_margin_rows"]:
            target = int(row["target"])
            if target in seen:
                continue
            seen.add(target)
            compact = dict(compact_near_row({
                **row,
                "window_start": window["start"],
                "window_role": window["window_role"],
                "target_mod_10010": target % 10010,
            }))
            rows.append(compact)
    return tuple(rows)


def square_record(rows, stress, epsilon):
    selected = tuple(
        row for row in rows
        if row["stress_plane_linf_distance"] <= epsilon)
    clear_targets = tuple(
        int(row["target"]) for row in selected if row["dominant_floor_passes"])
    deficit_targets = tuple(
        int(row["target"]) for row in selected
        if not row["dominant_floor_passes"])
    return {
        "epsilon": float(epsilon),
        "selected_count": len(selected),
        "deficit_targets": deficit_targets,
        "clear_false_positive_targets": clear_targets,
        "selected_targets": tuple(int(row["target"]) for row in selected),
        "selected_rows": tuple(compact_plane_row(row) for row in selected),
    }


def main():
    near_payload = json.loads(NEAR_SOURCE.read_text(encoding="utf-8"))
    plane_payload = json.loads(PLANE_SOURCE.read_text(encoding="utf-8"))
    source_rows = collect_window_closest_rows(near_payload)
    targets = tuple(row["target"] for row in source_rows)
    if len(targets) != 72:
        raise AssertionError("window-closest denominator drifted")
    if STRESS_TARGET not in targets:
        raise AssertionError("stress target missing from denominator")

    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=targets, dominant_modes=(1, 2), tail_threshold=.3,
        top_channel_count=40)
    volatile_labels = tuple(
        label_tuple(label) for label in plane_payload["volatile_labels"])
    adverse_pair = tuple(
        label_tuple(label) for label in plane_payload["adverse_pair"])
    near_by_target = {row["target"]: row for row in source_rows}
    rows = []
    for target in targets:
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
        near_row = near_by_target[target]
        rows.append({
            **near_row,
            "dominant_floor_passes": bool(
                profile_row["dominant_floor_passes"]),
            "adverse_pair_sum_to_principal": pair_sum,
            "repair_complement_sum_to_principal": complement_sum,
            "volatile_total_sum_to_principal": pair_sum + complement_sum,
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

    deficit_rows = tuple(
        row for row in rows if not row["dominant_floor_passes"])
    clear_rows = tuple(row for row in rows if row["dominant_floor_passes"])
    if tuple(row["target"] for row in deficit_rows) != (STRESS_TARGET,):
        raise AssertionError("deficit set drifted")

    square_records = tuple(
        square_record(rows, stress, epsilon) for epsilon in EPSILONS)
    first_square_false_positive = next(
        (record for record in square_records
         if record["clear_false_positive_targets"]),
        None)
    if first_square_false_positive is None:
        raise AssertionError("expanded holdout did not find a clear")
    if first_square_false_positive["epsilon"] != 0.02:
        raise AssertionError("first expanded false-positive epsilon drifted")
    if first_square_false_positive["clear_false_positive_targets"] != (1200302,):
        raise AssertionError("first expanded false-positive target drifted")

    sorted_by_plane_l1 = tuple(sorted(
        rows, key=lambda row: (
            row["stress_plane_l1_distance"],
            row["absolute_above_floor_signed_surplus"],
            row["target"])))
    sorted_by_margin = tuple(sorted(
        rows, key=lambda row: (
            row["absolute_above_floor_signed_surplus"],
            row["target"])))

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_near_boundary_selector_audit": str(
            NEAR_SOURCE.relative_to(ROOT)),
        "source_pair_complement_plane_audit": str(
            PLANE_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite pair/complement expanded-window holdout only; it "
            "falsifies the top-20 stress-box isolation as a stable checked "
            "selector on the predeclared 72-row window-closest denominator "
            "and proves no arithmetic placement theorem, signed projection "
            "theorem, or Goldbach proof"),
        "candidate": (
            "The pair/complement plane's small stress-centered boxes might "
            "remain isolated when expanded from the top-20 closest rows to "
            "the closest-margin rows from each checked window."),
        "mechanism": (
            "Reuse the six windows from the near-boundary selector audit, "
            "take the twelve closest-margin rows per window, recompute exact "
            "q286 signed channel profiles, and test square neighborhoods "
            "around stress target 1222142 in the pair/complement plane."),
        "prediction": (
            "If the top-20 local locator is stable, the .02 stress-centered "
            "pair/complement square should still select only 1222142 on the "
            "expanded predeclared denominator."),
        "falsifier": (
            "A clear row inside the .02 stress-centered square falsifies the "
            "top-20 isolation as a stable checked selector."),
        "novelty_label": "new-to-this-task",
        "arithmetic_modulus": near_payload["arithmetic_modulus"],
        "support": near_payload["support"],
        "window_specs": near_payload["window_specs"],
        "targets_per_window_from_source": 12,
        "expanded_target_count": len(rows),
        "deficit_targets": tuple(row["target"] for row in deficit_rows),
        "clear_count": len(clear_rows),
        "adverse_pair": tuple(adverse_pair),
        "volatile_labels": tuple(volatile_labels),
        "stress_row": compact_plane_row(stress),
        "square_records": square_records,
        "nearest_plane_rows": tuple(
            compact_plane_row(row) for row in sorted_by_plane_l1[:16]),
        "nearest_margin_rows": tuple(
            compact_plane_row(row) for row in sorted_by_margin[:16]),
        "plane_summaries": {
            "stress_plane_l1_distance": summarize(
                row["stress_plane_l1_distance"] for row in rows),
            "stress_plane_linf_distance": summarize(
                row["stress_plane_linf_distance"] for row in rows),
            "pair_sum": summarize(
                row["adverse_pair_sum_to_principal"] for row in rows),
            "repair_complement_sum": summarize(
                row["repair_complement_sum_to_principal"] for row in rows),
        },
        "correlations": {
            "pearson_abs_surplus_vs_stress_plane_l1_distance": pearson(
                (row["absolute_above_floor_signed_surplus"] for row in rows),
                (row["stress_plane_l1_distance"] for row in rows)),
            "pearson_abs_surplus_vs_stress_plane_linf_distance": pearson(
                (row["absolute_above_floor_signed_surplus"] for row in rows),
                (row["stress_plane_linf_distance"] for row in rows)),
            "pearson_abs_surplus_vs_pair_sum": pearson(
                (row["absolute_above_floor_signed_surplus"] for row in rows),
                (row["adverse_pair_sum_to_principal"] for row in rows)),
            "pearson_abs_surplus_vs_repair_complement_sum": pearson(
                (row["absolute_above_floor_signed_surplus"] for row in rows),
                (row["repair_complement_sum_to_principal"] for row in rows)),
        },
        "summary": {
            "top20_isolation_demoted": (
                "The .02 stress-centered pair/complement square isolated "
                "1222142 on the top-20 receipt but not on the expanded "
                "72-row window-closest holdout."),
            "first_expanded_false_positive": (
                "Clear row 1200302 enters the .02 square, with plane L1 "
                "distance about 0.0195523595 from the stress row."),
            "remaining_local_signal": (
                "The .005 and .01 stress-centered squares still isolate "
                "1222142 on this finite holdout, so the plane remains a "
                "local diagnostic rather than a theorem."),
            "live_target": (
                "Any proof route must explain the pair/complement placement "
                "arithmetically, not just assert a stable fixed-width box."),
        },
        "interpretation": {
            "hole_status": (
                "The loop did not vanish; the expanded denominator punctures "
                "the .02 top-20 box while preserving a smaller .01 local "
                "isolation."),
            "route_status": (
                "Demote fixed-width pair/complement stress boxes as a stable "
                "selector.  Preserve the plane as a microscope for the "
                "arithmetic placement theorem obligation."),
            "remaining_theorem": (
                "Prove coefficient-sensitive placement of actual "
                "binary-prime residue weights, or replace this geometry with "
                "a signed aggregate estimate that survives expanded "
                "denominators."),
        },
        "pair_complement_window_holdout_measured": True,
        "top20_point_zero_two_stress_box_isolation_refuted": True,
        "point_zero_one_stress_box_expanded_holdout_isolated": True,
        "stable_pair_complement_box_selector_theorem_proved": False,
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
