"""Audit coupled slack on all active source-summary q286 rows.

The post-discovery stress audit kept one worst active row per block.  This
builder widens the finite fixture to every unique active row already present
in the principal-rescue source summaries, while preserving the selected-late
calibration constants.  It asks whether the payment-ratio hinge seen in the
viewer is structure beyond the 11-row projection.

Finite diagnostic only.  It proves no active-lane theorem, pointwise
adverse-drag theorem, q286 threshold theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE = EVIDENCE / "q286-principal-rescue-obstruction-audit.json"
OUT = (
    EVIDENCE
    / "q286-active-lane-source-summary-coupled-slack-audit.json")

FIRST_TWO_THRESHOLD = -0.2
FIRST_THREE_THRESHOLD = -0.3
CALIBRATION_TARGETS = (14138, 1222142, 1323632, 1379072)
COMPONENT_PAIR = ((5, 7), (7, 11))
TOLERANCE = 1e-9

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_lower_support_component_pair_action_identity_receipt,
    q286_lower_support_component_pair_closure_margin_profile_receipt,
)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def finite_summary(values):
    vals = [float(value) for value in values]
    if not vals:
        return {"count": 0, "minimum": None, "mean": None, "maximum": None}
    return {
        "count": len(vals),
        "minimum": min(vals),
        "mean": math.fsum(vals) / len(vals),
        "maximum": max(vals),
    }


def candidate_rows(block):
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


def collect_active_source_summary_rows(source):
    rows = {}
    duplicate_count = 0
    active_candidates_by_block = defaultdict(int)
    unique_active_by_block = defaultdict(int)
    for block in source["block_summaries"]:
        block_index = block["block_index_after_discovery"]
        if block_index <= 0:
            continue
        for row in candidate_rows(block):
            if not active_selector(row):
                continue
            active_candidates_by_block[block_index] += 1
            target = int(row["target"])
            if target in rows:
                duplicate_count += 1
                continue
            rows[target] = dict(row)
            unique_active_by_block[block_index] += 1
    ordered = [rows[target] for target in sorted(rows)]
    return ordered, duplicate_count, active_candidates_by_block, unique_active_by_block


def payment_row(source_row, identity_row, constants):
    driver = identity_row["combined_floor_driver_to_principal_ratio"]
    closure_row = identity_row["source_closure_row"]
    max_channel = closure_row["maximum_normalized_real_channel_sum"]
    driver_margin = driver - constants["driver_floor"]
    channel_margin = constants["channel_bound"] - max_channel
    channel_contribution = (
        constants["channel_l1_to_principal"] * channel_margin)
    strict_margin = driver_margin + channel_contribution
    driver_deficit = max(0.0, -driver_margin)
    payment_ratio = (
        channel_contribution / driver_deficit
        if driver_deficit > 0.0 else None)
    return {
        "target": int(source_row["target"]),
        "block_index_after_discovery": int(
            source_row["block_index_after_discovery"]),
        "target_mod_286": int(source_row["target_mod_286"]),
        "target_mod_143": int(source_row["target_mod_143"]),
        "target_mod_13": int(source_row["target_mod_13"]),
        "source_full_action_to_principal_ratio": float(
            source_row["full_action_to_principal_ratio"]),
        "source_first_two_modes_to_principal_ratio": float(
            source_row["first_two_modes_to_principal_ratio"]),
        "source_first_three_modes_to_principal_ratio": float(
            source_row["first_three_modes_to_principal_ratio"]),
        "source_principal_only_margin": float(
            source_row["principal_only_margin"]),
        "source_complement_to_principal_ratio": float(
            source_row["complement_to_principal_ratio"]),
        "combined_floor_driver_to_principal_ratio": driver,
        "maximum_normalized_real_channel_sum": max_channel,
        "driver_margin_to_calibrated_floor": driver_margin,
        "driver_floor_condition_met": driver_margin >= -TOLERANCE,
        "driver_deficit_to_calibrated_floor": driver_deficit,
        "channel_margin_to_calibrated_linf_bound": channel_margin,
        "channel_linf_condition_met": channel_margin >= -TOLERANCE,
        "channel_margin_contribution_to_strict_closure": (
            channel_contribution),
        "channel_payment_ratio_to_driver_deficit": payment_ratio,
        "strict_closure_margin_to_calibrated_endpoint": strict_margin,
        "strict_closure_margin_positive": strict_margin > TOLERANCE,
        "full_action_to_principal_ratio": float(
            identity_row["full_action_to_principal_ratio"]),
        "positive_by_reconstructed_identity": bool(
            identity_row["positive_by_reconstructed_identity"]),
    }


def build_receipt():
    source = load_json(SOURCE)
    source_rows, duplicate_count, active_by_block, unique_by_block = (
        collect_active_source_summary_rows(source))
    targets = tuple(row["target"] for row in source_rows)
    calibration = q286_lower_support_component_pair_closure_margin_profile_receipt(
        targets=CALIBRATION_TARGETS, component_pair=COMPONENT_PAIR,
        tolerance=TOLERANCE)
    constants = {
        "driver_floor": calibration["combined_floor_driver_floor"],
        "channel_bound": calibration["normalized_real_channel_linf_bound"],
        "channel_l1_to_principal": calibration[
            "real_channel_l1_to_principal_mean"],
    }
    identity = q286_lower_support_component_pair_action_identity_receipt(
        targets=targets, component_pair=COMPONENT_PAIR, tolerance=TOLERANCE)
    rows = [
        payment_row(source_row, identity["rows"][source_row["target"]],
                    constants)
        for source_row in source_rows
    ]
    positive_rows = [
        row for row in rows if row["strict_closure_margin_positive"]]
    nonpositive_rows = [
        row for row in rows if not row["strict_closure_margin_positive"]]
    negative_driver_rows = [
        row for row in rows
        if row["driver_margin_to_calibrated_floor"] < -TOLERANCE]
    ratio_rows = [
        row for row in rows
        if row["channel_payment_ratio_to_driver_deficit"] is not None]
    ratio_pass_rows = [
        row for row in ratio_rows
        if row["channel_payment_ratio_to_driver_deficit"] > 1.0 + TOLERANCE]
    ratio_fail_rows = [
        row for row in ratio_rows
        if row["channel_payment_ratio_to_driver_deficit"] <= 1.0 + TOLERANCE]
    nonnegative_driver_positive_rows = [
        row for row in positive_rows
        if row["driver_margin_to_calibrated_floor"] >= -TOLERANCE]
    payment_ratio_mismatches = [
        row for row in ratio_rows
        if (row["channel_payment_ratio_to_driver_deficit"] > 1.0 + TOLERANCE)
        != row["strict_closure_margin_positive"]]
    by_block = []
    for block in sorted(unique_by_block):
        block_rows = [
            row for row in rows
            if row["block_index_after_discovery"] == block]
        by_block.append({
            "block_index_after_discovery": block,
            "active_candidate_rows_in_source_summaries": (
                active_by_block[block]),
            "unique_active_rows": unique_by_block[block],
            "positive_coupled_slack_rows": sum(
                row["strict_closure_margin_positive"]
                for row in block_rows),
            "nonpositive_coupled_slack_rows": sum(
                not row["strict_closure_margin_positive"]
                for row in block_rows),
        })

    return {
        "schema_version": 1,
        "receipt": "q286-active-lane-source-summary-coupled-slack-audit",
        "generated_from_commit": source_commit(),
        "sources": {
            "source_summary": str(SOURCE.relative_to(ROOT)),
            "calibration_targets": list(CALIBRATION_TARGETS),
            "component_pair": [list(pair) for pair in COMPONENT_PAIR],
        },
        "selector": {
            "first_two_modes_to_principal_ratio": f"< {FIRST_TWO_THRESHOLD}",
            "first_three_modes_to_principal_ratio": (
                f"< {FIRST_THREE_THRESHOLD}"),
            "source_summary_row_families": [
                "worst_full_rows",
                "tightest_principal_only_rows",
                "first_full_failure_rows",
            ],
        },
        "calibrated_constants": constants,
        "unique_active_source_summary_row_count": len(rows),
        "duplicate_active_candidate_count": duplicate_count,
        "positive_coupled_slack_count": len(positive_rows),
        "nonpositive_coupled_slack_count": len(nonpositive_rows),
        "driver_floor_condition_met_count": sum(
            row["driver_floor_condition_met"] for row in rows),
        "driver_floor_condition_failed_count": len(negative_driver_rows),
        "channel_linf_condition_met_count": sum(
            row["channel_linf_condition_met"] for row in rows),
        "channel_linf_condition_failed_count": sum(
            not row["channel_linf_condition_met"] for row in rows),
        "negative_driver_rows_with_payment_ratio_count": len(ratio_rows),
        "payment_ratio_above_one_count": len(ratio_pass_rows),
        "payment_ratio_at_or_below_one_count": len(ratio_fail_rows),
        "nonnegative_driver_positive_count": len(
            nonnegative_driver_positive_rows),
        "payment_ratio_mismatch_count_on_negative_driver_rows": len(
            payment_ratio_mismatches),
        "strict_margin_summary": finite_summary(
            row["strict_closure_margin_to_calibrated_endpoint"]
            for row in rows),
        "driver_margin_summary": finite_summary(
            row["driver_margin_to_calibrated_floor"] for row in rows),
        "channel_contribution_summary": finite_summary(
            row["channel_margin_contribution_to_strict_closure"]
            for row in rows),
        "payment_ratio_summary": finite_summary(
            row["channel_payment_ratio_to_driver_deficit"]
            for row in ratio_rows),
        "worst_strict_margin_row": min(
            rows,
            key=lambda row: row[
                "strict_closure_margin_to_calibrated_endpoint"]),
        "best_strict_margin_row": max(
            rows,
            key=lambda row: row[
                "strict_closure_margin_to_calibrated_endpoint"]),
        "smallest_positive_strict_margin_row": min(
            positive_rows,
            key=lambda row: row[
                "strict_closure_margin_to_calibrated_endpoint"]),
        "largest_nonpositive_strict_margin_row": max(
            nonpositive_rows,
            key=lambda row: row[
                "strict_closure_margin_to_calibrated_endpoint"]),
        "block_summary": by_block,
        "rows": rows,
        "candidate": {
            "name": "source-summary coupled slack transition audit",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Replay the frozen selected-late coupled slack scalar on "
                "every unique active source-summary row, not only one "
                "worst row per block."),
            "prediction": (
                "If the payment-ratio hinge is a broader active-lane "
                "transition coordinate, negative-driver rows should pass "
                "exactly when channel_payment/driver_deficit exceeds 1; "
                "rows with nonnegative driver margin should be separately "
                "classified as driver-carried."),
            "falsifier": (
                "A negative-driver row whose strict margin sign disagrees "
                "with ratio>1 would falsify the payment-ratio diagnosis. "
                "A large population of nonpositive rows falsifies any claim "
                "that the finite source-summary active population already "
                "satisfies the coupled slack endpoint."),
            "smallest_test": (
                "Collect the active source-summary rows from the "
                "principal-rescue audit, compute action identities once, "
                "apply the fixed calibration constants, and compare strict "
                "margin signs to payment-ratio threshold 1."),
        },
        "decision": (
            "The payment-ratio hinge is algebraically exact on the "
            "negative-driver subpopulation, but the widened finite fixture "
            "does not support a finite pass claim: only 83 of 226 unique "
            "active source-summary rows have positive coupled slack, while "
            "143 are nonpositive.  The next theorem target remains a "
            "coupled pointwise tradeoff or direct unnormalized signed "
            "estimate; the finite data now also separates 74 "
            "negative-driver ratio-paid passes from 9 driver-carried "
            "passes."),
        "status_boundary": (
            "Finite source-summary coupled-slack audit only.  Source rows "
            "come from compact summary families in the principal-rescue "
            "receipt, not from all possible active targets.  This proves no "
            "universal active-lane theorem, pointwise adverse-drag theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof."),
        "goldbach_proved": False,
        "active_lane_theorem_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
