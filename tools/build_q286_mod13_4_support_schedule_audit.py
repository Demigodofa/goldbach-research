"""Predeclared support schedule for the q286 mod-13 low-(3,1) pocket.

The immediate prospective block after discovery had no ``full_nonpositive``
support, so it neither confirmed nor falsified the frozen ``target_mod_13==4``
pocket.  This receipt predeclares the next four 8-cycle q286 blocks and tests
whether support appears there before scoring weighted centered (3,1).

Finite evidence only: this is a support/falsifier schedule for a candidate
stress pocket, not a stress theorem, signed correlation theorem, pointwise
character-sum theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-mod13-4-support-schedule-audit.json"
IMMEDIATE_SOURCE = (
    EVIDENCE / "q286-mod13-4-prospective-descriptor-audit.json")
THRESHOLD_SOURCE = (
    EVIDENCE / "q286-centered-3-1-threshold-subclass-audit.json")
DESCRIPTOR_SOURCE = (
    EVIDENCE / "q286-low-3-1-independent-descriptor-audit.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
    q286_first_three_filter_order_audit_receipt,
)
from tools.build_q286_centered_3_1_stress_class_audit import (  # noqa: E402
    predicate_sets,
)
from tools.build_q286_centered_3_1_threshold_subclass_audit import (  # noqa: E402
    centered_row,
    finite_summary,
    rank_rows,
)
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    label_tuple,
)
from tools.build_q286_mod13_4_prospective_descriptor_audit import (  # noqa: E402
    COMPLEMENT_FLOOR,
    DISCOVERY_CYCLES,
    DISCOVERY_START,
    FROZEN_DESCRIPTOR,
    FROZEN_DESCRIPTOR_RESIDUE,
    TAIL_THRESHOLD,
    TARGETS_PER_CYCLE,
    TOLERANCE,
    classify_row,
    get_thresholds,
    selected_descriptor_row,
    summarize_reference_group,
)


FUTURE_BLOCK_INDICES = (2, 3, 4, 5)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def block_start(period, block_index):
    return DISCOVERY_START + int(block_index) * DISCOVERY_CYCLES * int(period)


def cycle_counts(rows):
    counts = {}
    for row in rows:
        cycle = int(row["cycle"])
        counts.setdefault(cycle, {
            "cycle": cycle,
            "reference_count": 0,
            "mod13_4_count": 0,
            "low_selected_max_count": 0,
            "above_selected_max_count": 0,
            "above_or_equal_fresh_min_count": 0,
        })
        counts[cycle]["reference_count"] += 1
        counts[cycle]["mod13_4_count"] += int(
            row["target_mod_13"] == FROZEN_DESCRIPTOR_RESIDUE)
        counts[cycle]["low_selected_max_count"] += int(
            row["low_selected_max_threshold"])
        counts[cycle]["above_selected_max_count"] += int(
            not row["low_selected_max_threshold"])
        counts[cycle]["above_or_equal_fresh_min_count"] += int(
            row["above_or_equal_fresh_min_threshold"])
    return [counts[key] for key in sorted(counts)]


def score_block(receipt, labels, local_rows_by_residue, lp_vector,
                thresholds):
    broad_targets = tuple(sorted(predicate_sets(receipt)[
        "full_nonpositive"]))
    if not broad_targets:
        return [], None
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=broad_targets,
        dominant_modes=(1, 2),
        tail_threshold=TAIL_THRESHOLD,
        top_channel_count=40)
    raw_rows = []
    for target in broad_targets:
        base = centered_row(
            target, profile, labels, local_rows_by_residue, lp_vector)
        raw_rows.append({
            **base,
            **classify_row(base, thresholds),
            "cycle": int(receipt["target_rows"][target]["cycle"]),
            "target_mod_11": target % 11,
            "target_mod_13": target % 13,
            "target_mod_143": target % 143,
            "target_mod_286": target % 286,
            "passed_predicates": receipt["target_rows"][target][
                "passed_predicates"],
            "full_action_to_principal_ratio": receipt[
                "target_rows"][target]["full_action_to_principal_ratio"],
            "first_two_modes_to_principal_ratio": receipt[
                "target_rows"][target][
                    "first_two_modes_to_principal_ratio"],
            "first_three_modes_to_principal_ratio": receipt[
                "target_rows"][target][
                    "first_three_modes_to_principal_ratio"],
            "complement_to_principal_ratio": receipt[
                "target_rows"][target]["complement_to_principal_ratio"],
        })
    return rank_rows(raw_rows), profile


def residue_summaries(rows, total_low, total_strict, total_broad):
    return [
        summarize_reference_group(
            f"target_mod_13=={residue}",
            [row for row in rows if row["target_mod_13"] == residue],
            total_low,
            total_strict,
            total_broad)
        for residue in range(13)
    ]


def block_summary(block_index, start, receipt, rows):
    total_broad = len(rows)
    total_low = sum(1 for row in rows if row["low_selected_max_threshold"])
    total_strict = sum(
        1 for row in rows if row["strict_low_selected_min_threshold"])
    descriptor_rows = [
        row for row in rows if row["target_mod_13"] == FROZEN_DESCRIPTOR_RESIDUE]
    descriptor = summarize_reference_group(
        FROZEN_DESCRIPTOR, descriptor_rows, total_low, total_strict,
        total_broad)
    return {
        "block_index_after_discovery": int(block_index),
        "start": int(start),
        "cycle_count": int(receipt["cycle_count"]),
        "targets_per_cycle": int(receipt["targets_per_cycle"]),
        "tested_target_count": int(receipt["tested_target_count"]),
        "predicate_counts": receipt["predicate_counts"],
        "full_nonpositive_count": int(total_broad),
        "mod13_4_full_nonpositive_count": int(
            descriptor["reference_count"]),
        "cycle_counts": cycle_counts(rows),
        "descriptor_result": descriptor,
        "mod13_residue_results": residue_summaries(
            rows, total_low, total_strict, total_broad),
        "lowest_rows": rows[:12],
        "highest_rows": rows[-12:],
    }


def aggregate_blocks(blocks):
    rows = [
        row
        for block in blocks
        for row in block.get("scored_rows", [])
    ]
    total_broad = len(rows)
    total_low = sum(1 for row in rows if row["low_selected_max_threshold"])
    total_strict = sum(
        1 for row in rows if row["strict_low_selected_min_threshold"])
    descriptor_rows = [
        row for row in rows if row["target_mod_13"] == FROZEN_DESCRIPTOR_RESIDUE]
    descriptor = summarize_reference_group(
        FROZEN_DESCRIPTOR, descriptor_rows, total_low, total_strict,
        total_broad)
    return {
        "scored_full_nonpositive_count": total_broad,
        "scored_low_selected_max_count": total_low,
        "scored_strict_low_selected_min_count": total_strict,
        "descriptor_result": descriptor,
        "weighted_centered_3_1_summary": finite_summary(
            row["weighted_centered_channel_value"] for row in rows),
        "lowest_rows": sorted(
            rows,
            key=lambda row: (
                row["weighted_centered_channel_value"], row["target"]))[:20],
        "highest_rows": sorted(
            rows,
            key=lambda row: (
                row["weighted_centered_channel_value"], row["target"]))[-20:],
    }


def main():
    immediate_payload = load_json(IMMEDIATE_SOURCE)
    threshold_payload = load_json(THRESHOLD_SOURCE)
    descriptor_payload = load_json(DESCRIPTOR_SOURCE)
    local_payload = load_json(LOCAL_SOURCE)
    lp_payload = load_json(LP_SOURCE)
    thresholds = get_thresholds(threshold_payload)
    descriptor_row = selected_descriptor_row(descriptor_payload)
    if descriptor_row["descriptor"] != FROZEN_DESCRIPTOR:
        raise AssertionError("frozen descriptor moved")
    if immediate_payload["decision_metrics"]["descriptor_test_status"] != (
            "untested_no_prospective_full_nonpositive_support"):
        raise AssertionError("immediate source is not the no-support receipt")

    period = int(immediate_payload["discovery_window"]["arithmetic_period"])
    labels = tuple(label_tuple(label) for label in local_payload[
        "outside_labels"])
    lp_vector = np.asarray(
        lp_payload["selected_lp_effective_vector"], dtype=np.float64)
    local_rows_by_residue = {
        int(row["n_mod_143"]): row
        for row in local_payload["local_residue_rows"]
    }

    block_results = []
    scored_blocks = []
    for block_index in FUTURE_BLOCK_INDICES:
        start = block_start(period, block_index)
        receipt = q286_first_three_filter_order_audit_receipt(
            start=start,
            cycle_count=DISCOVERY_CYCLES,
            targets_per_cycle=TARGETS_PER_CYCLE,
            tail_threshold=TAIL_THRESHOLD,
            complement_floor=COMPLEMENT_FLOOR)
        rows, _profile = score_block(
            receipt, labels, local_rows_by_residue, lp_vector, thresholds)
        summary = block_summary(block_index, start, receipt, rows)
        block_results.append(summary)
        scored_blocks.append({**summary, "scored_rows": rows})

    aggregate = aggregate_blocks(scored_blocks)
    descriptor = aggregate["descriptor_result"]
    support_count = descriptor["reference_count"]
    if support_count == 0:
        status = "untested_no_scheduled_mod13_4_full_nonpositive_support"
    elif (descriptor["above_selected_max_count"] == 0
          and descriptor["above_or_equal_fresh_min_count"] == 0):
        status = "passes_scheduled_support_zero_failure_gate"
    else:
        status = "falsified_on_scheduled_support"

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "immediate_prospective_no_support": str(
                IMMEDIATE_SOURCE.relative_to(ROOT)),
            "threshold_subclass": str(THRESHOLD_SOURCE.relative_to(ROOT)),
            "independent_descriptor": str(
                DESCRIPTOR_SOURCE.relative_to(ROOT)),
            "local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
            "low_frequency_lp_cone": str(LP_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite predeclared support-schedule audit only; this tests "
            "whether target_mod_13==4 gets future full_nonpositive support "
            "and, if so, whether that support remains low in weighted "
            "centered (3,1). It proves no stress theorem, signed correlation "
            "theorem, pointwise character-sum theorem, or Goldbach proof."),
        "question": (
            "After the immediate no-support block, does the frozen "
            "target_mod_13==4 pocket encounter and pass a broader "
            "predeclared future support schedule?"),
        "mechanism": (
            "Use the previously frozen independent descriptor and scan four "
            "predeclared future 8-cycle q286 blocks after the immediate "
            "prospective block. Only rows selected by full_nonpositive are "
            "scored by weighted locally centered (3,1)."),
        "prediction": (
            "If target_mod_13==4 is a real stress-classifier pocket, any "
            "scheduled full_nonpositive rows in that residue should stay "
            "below the selected-max and fresh-min centered-(3,1) thresholds."),
        "falsifier": (
            "A scheduled target_mod_13==4 full_nonpositive row above the "
            "selected-max threshold or at/above the fresh-min threshold "
            "falsifies the pocket for this schedule. No support keeps it "
            "untested on this schedule."),
        "frozen_descriptor": {
            "descriptor": FROZEN_DESCRIPTOR,
            "source_reference_count": int(descriptor_row["reference_count"]),
            "source_low_count": int(descriptor_row["low_count"]),
            "source_above_threshold_count": int(
                descriptor_row["above_threshold_count"]),
            "source_precision": float(descriptor_row["precision"]),
            "source_recall": float(descriptor_row["recall"]),
            "source_references": descriptor_row["references"],
        },
        "thresholds": thresholds,
        "schedule": {
            "arithmetic_period": period,
            "discovery_start": DISCOVERY_START,
            "block_cycle_count": DISCOVERY_CYCLES,
            "targets_per_cycle": TARGETS_PER_CYCLE,
            "immediate_no_support_start": immediate_payload[
                "prospective_window"]["start"],
            "future_block_indices": list(FUTURE_BLOCK_INDICES),
            "future_starts": [
                block_start(period, block_index)
                for block_index in FUTURE_BLOCK_INDICES
            ],
        },
        "block_results": block_results,
        "aggregate": aggregate,
        "decision_metrics": {
            "scheduled_test_status": status,
            "scheduled_block_count": len(FUTURE_BLOCK_INDICES),
            "scheduled_target_count": sum(
                block["tested_target_count"] for block in block_results),
            "scheduled_full_nonpositive_count": (
                aggregate["scored_full_nonpositive_count"]),
            "scheduled_mod13_4_support_count": int(support_count),
            "scheduled_mod13_4_above_selected_max_count": int(
                descriptor["above_selected_max_count"]),
            "scheduled_mod13_4_above_or_equal_fresh_min_count": int(
                descriptor["above_or_equal_fresh_min_count"]),
            "scheduled_mod13_4_precision_for_low_selected_max": (
                descriptor["precision_for_low_selected_max"]),
            "scheduled_mod13_4_recall_for_low_selected_max": (
                descriptor["recall_for_low_selected_max"]),
        },
        "decision": (
            "If the scheduled status is passes_scheduled_support_zero_failure_gate, "
            "the mod-13 pocket survives a broader finite prospective support "
            "test but still needs a theorem-level family. If falsified, close "
            "the mod-13 bridge. If untested, move away from this sparse "
            "classifier schedule or predeclare a larger support-search before "
            "reading centered values."),
        "next_obligation": (
            "A surviving pocket should be compared against a signed "
            "correlation/cone formulation. A no-support or failed pocket "
            "pushes the proof route toward distributed cone/correlation "
            "rather than single-residue classifier language."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
