"""Stress the q286 strict-closure scalar on post-discovery active samples.

The selected-late closure receipt only tested three late active rows.  This
builder takes one unchanged-selector stress row from each post-discovery block
in the principal-rescue audit, freezes the same closure constants, and records
whether the strict closure margin stays positive.

Finite diagnostic only.  A negative strict-closure margin falsifies the current
calibrated closure endpoint on that finite row; it does not falsify Goldbach,
because the actual full action can still be positive by a route not captured by
this scalar endpoint.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-active-lane-strict-closure-post-discovery-stress.json"
SOURCE = EVIDENCE / "q286-principal-rescue-obstruction-audit.json"

FIRST_TWO_THRESHOLD = -0.2
FIRST_THREE_THRESHOLD = -0.3
TARGETS_PER_WINDOW = 1

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_active_lane_strict_closure_margin_census_receipt,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(inner) for key, inner in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(inner) for inner in value]
    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        if math.isinf(value):
            return "Infinity" if value > 0 else "-Infinity"
    return value


def candidate_rows(block):
    """Return the finite row summaries available in the source receipt."""
    rows = {}
    summary = block["tail_summary"]
    for key in (
            "worst_full_rows",
            "tightest_principal_only_rows",
            "first_full_failure_rows"):
        for row in summary.get(key, ()):
            rows[row["target"]] = row
    return rows.values()


def active_selector(row):
    return (
        row["first_two_modes_to_principal_ratio"] < FIRST_TWO_THRESHOLD
        and row["first_three_modes_to_principal_ratio"] < FIRST_THREE_THRESHOLD)


def select_post_discovery_stress_targets(source):
    """Select one worst active sample row from each post-discovery block."""
    selected = []
    for block in source["block_summaries"]:
        block_index = block["block_index_after_discovery"]
        if block_index <= 0:
            continue
        candidates = [
            row for row in candidate_rows(block)
            if active_selector(row)
        ]
        if not candidates:
            continue
        row = min(candidates, key=lambda item: (
            item["full_action_to_principal_ratio"], item["target"]))
        selected.append({
            "block_index_after_discovery": block_index,
            "block_start": block["start"],
            "candidate_count_in_source_summary": len(candidates),
            "selected_target": row["target"],
            "selected_source_row": row,
        })
    return selected


def phase_space_point(source_row, closure_row, max_abs_margin):
    strict_margin = closure_row[
        "strict_closure_margin_to_calibrated_endpoint"]
    distance = abs(strict_margin)
    return {
        "target": source_row["target"],
        "x_log_N": math.log(source_row["target"]),
        "y_driver_margin_to_calibrated_floor": closure_row[
            "driver_margin_to_calibrated_floor"],
        "z_strict_closure_margin": strict_margin,
        "color_target_mod_286": source_row["target_mod_286"],
        "color_target_mod_143": source_row["target_mod_143"],
        "fixed_conductor_pair": [35, 77],
        "brightness_distance_from_failure": distance,
        "brightness_normalized_to_sample": (
            distance / max_abs_margin if max_abs_margin else 0.0),
        "animation_block_index_after_discovery": (
            source_row["block_index_after_discovery"]),
        "animation_global_cycle": source_row["global_cycle"],
        "strict_closure_margin_positive": closure_row[
            "strict_closure_margin_positive"],
        "dominant_strict_margin_source": closure_row[
            "dominant_strict_margin_source"],
    }


def build_receipt():
    source = load_json(SOURCE)
    selected = select_post_discovery_stress_targets(source)
    starts = tuple(row["selected_target"] for row in selected)
    census = q286_active_lane_strict_closure_margin_census_receipt(
        starts=starts, targets_per_window=TARGETS_PER_WINDOW)

    target_rows = {}
    margins = []
    for selected_row in selected:
        target = selected_row["selected_target"]
        closure_row = census["target_rows"][target]
        source_row = selected_row["selected_source_row"]
        margin = closure_row[
            "strict_closure_margin_to_calibrated_endpoint"]
        margins.append(abs(margin))
        target_rows[target] = {
            "target": target,
            "block_index_after_discovery": (
                selected_row["block_index_after_discovery"]),
            "block_start": selected_row["block_start"],
            "candidate_count_in_source_summary": (
                selected_row["candidate_count_in_source_summary"]),
            "source_full_action_to_principal_ratio": source_row[
                "full_action_to_principal_ratio"],
            "source_first_two_modes_to_principal_ratio": source_row[
                "first_two_modes_to_principal_ratio"],
            "source_first_three_modes_to_principal_ratio": source_row[
                "first_three_modes_to_principal_ratio"],
            "source_principal_only_margin": source_row[
                "principal_only_margin"],
            "source_complement_to_principal_ratio": source_row[
                "complement_to_principal_ratio"],
            "source_target_mod_286": source_row["target_mod_286"],
            "source_target_mod_143": source_row["target_mod_143"],
            "source_target_mod_13": source_row["target_mod_13"],
            "driver_margin_to_calibrated_floor": closure_row[
                "driver_margin_to_calibrated_floor"],
            "channel_margin_to_calibrated_linf_bound": closure_row[
                "channel_margin_to_calibrated_linf_bound"],
            "channel_margin_contribution_to_strict_closure": closure_row[
                "channel_margin_contribution_to_strict_closure"],
            "strict_closure_margin_to_calibrated_endpoint": margin,
            "dominant_strict_margin_source": closure_row[
                "dominant_strict_margin_source"],
            "strict_closure_margin_positive": closure_row[
                "strict_closure_margin_positive"],
            "full_action_to_principal_ratio": closure_row[
                "full_action_to_principal_ratio"],
            "positive_by_reconstructed_identity": closure_row[
                "positive_by_reconstructed_identity"],
        }

    max_abs_margin = max(margins, default=0.0)
    phase_points = [
        phase_space_point(
            selected_row["selected_source_row"],
            census["target_rows"][selected_row["selected_target"]],
            max_abs_margin)
        for selected_row in selected
    ]
    positive_targets = list(census["positive_strict_margin_targets"])
    nonpositive_targets = list(census["nonpositive_strict_margin_targets"])
    failed_rows = [
        target_rows[target] for target in nonpositive_targets]
    passed_rows = [
        target_rows[target] for target in positive_targets]

    return {
        "schema_version": 1,
        "receipt": (
            "q286-active-lane-strict-closure-post-discovery-stress"),
        "generated_from_commit": source_commit(),
        "purpose": (
            "Select one worst unchanged active-lane sample row from each "
            "post-discovery block in the principal-rescue audit and stress "
            "the frozen strict-closure scalar on those rows."),
        "source_receipts": {
            "selection_source": str(SOURCE.relative_to(ROOT)),
            "closure_function": (
                "q286_active_lane_strict_closure_margin_census_receipt"),
            "calibration_source": (
                "same frozen calibration targets as selected-late receipt"),
        },
        "selector": {
            "block_indices_after_discovery": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            "per_block_rule": (
                "among source summary rows satisfying first_two<-0.2 and "
                "first_three<-0.3, choose the smallest "
                "full_action_to_principal_ratio, then target"),
            "first_two_modes_to_principal_ratio": f"< {FIRST_TWO_THRESHOLD}",
            "first_three_modes_to_principal_ratio": f"< {FIRST_THREE_THRESHOLD}",
            "targets_per_window": TARGETS_PER_WINDOW,
            "selected_targets": starts,
        },
        "scanned_target_count": census["scanned_target_count"],
        "tail_target_count": census["tail_target_count"],
        "tail_targets": census["tail_targets"],
        "calibration_targets": census["calibration_targets"],
        "calibrated_combined_floor_driver_floor": census[
            "calibrated_combined_floor_driver_floor"],
        "calibrated_normalized_real_channel_linf_bound": census[
            "calibrated_normalized_real_channel_linf_bound"],
        "calibrated_real_channel_l1_to_principal_mean": census[
            "calibrated_real_channel_l1_to_principal_mean"],
        "positive_strict_margin_targets": positive_targets,
        "nonpositive_strict_margin_targets": nonpositive_targets,
        "all_tail_targets_have_positive_strict_margin": census[
            "all_tail_targets_have_positive_strict_margin"],
        "failed_strict_closure_count": len(failed_rows),
        "passed_strict_closure_count": len(passed_rows),
        "minimum_strict_closure_margin": min(
            (row["strict_closure_margin_to_calibrated_endpoint"]
             for row in target_rows.values()),
            default=None),
        "maximum_strict_closure_margin": max(
            (row["strict_closure_margin_to_calibrated_endpoint"]
             for row in target_rows.values()),
            default=None),
        "failed_rows": failed_rows,
        "passed_rows": passed_rows,
        "target_rows": target_rows,
        "phase_space_visual_schema": {
            "x": "log(target)",
            "y": "driver_margin_to_calibrated_floor",
            "z": "strict_closure_margin_to_calibrated_endpoint",
            "color": (
                "target_mod_286 or target_mod_143; conductor pair is fixed "
                "as 35/77 for this component-pair receipt"),
            "brightness": (
                "absolute distance from zero strict-closure failure boundary"),
            "animation": (
                "block_index_after_discovery, with global_cycle as an "
                "in-block secondary time coordinate"),
            "boundary": (
                "Visualization is a hypothesis/falsifier locator only; every "
                "glow must be reduced back to an analytic inequality or an "
                "explicit finite counterexample."),
        },
        "phase_space_points": phase_points,
        "decision": (
            "The frozen selected-late strict-closure endpoint does not survive "
            "this stronger post-discovery stress selection: six early "
            "post-discovery samples have nonpositive strict closure margin, "
            "while five later samples stay positive.  The actual full action "
            "remains positive on these source rows, so the failure is specific "
            "to the calibrated endpoint route, not to Goldbach."),
        "next_obligation": (
            "Replace the selected-late closure scalar with a genuinely "
            "pointwise, unnormalized analytic estimate or prove a phase/scale "
            "condition explaining the transition from failed early stress rows "
            "to positive later stress rows."),
        "falsifier": (
            "Any target listed in nonpositive_strict_margin_targets is a "
            "finite falsifier for the current calibrated strict-closure "
            "endpoint as a universal active-lane certificate."),
        "status_boundary": (
            "Finite post-discovery stress diagnostic only.  It proves no "
            "universal active-lane theorem, no adverse-drag theorem, no "
            "signed prime-correlation theorem, no strict-central Goldbach "
            "theorem, and no Goldbach proof."),
        "goldbach_proved": False,
        "strict_closure_margin_theorem_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(json_ready(build_receipt()), indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
