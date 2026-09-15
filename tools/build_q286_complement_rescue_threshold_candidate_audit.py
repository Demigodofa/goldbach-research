"""Derive q286 complement-rescue threshold candidates from the margin schedule.

This receipt does not rerun the q286 scan.  It reads the already checked
complement-rescue margin schedule and asks which candidate statements are
actually supported by that finite data, which are tautological, and which are
already falsified.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE = EVIDENCE / "q286-complement-rescue-margin-schedule.json"
OUT = EVIDENCE / "q286-complement-rescue-threshold-candidate-audit.json"
TOLERANCE = 1e-9


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def summary_number(summary, field, metric="minimum"):
    return summary[field][metric]


def summarize_blocks(blocks):
    tail_count = sum(block["first_three_tail"]["row_count"] for block in blocks)
    tail_failures = sum(
        block["first_three_tail"]["failure_count"] for block in blocks)
    active_count = sum(block["active_selector"]["row_count"] for block in blocks)
    active_failures = sum(
        block["active_selector"]["failure_count"] for block in blocks)
    full_nonpositive = sum(
        int(block["predicate_counts"]["full_nonpositive"]) for block in blocks)
    margins = [
        summary_number(
            block["first_three_tail"], "rescue_margin_to_zero_summary")
        for block in blocks
        if block["first_three_tail"]["row_count"]
    ]
    ratios = [
        summary_number(
            block["first_three_tail"],
            "complement_to_required_ratio_summary")
        for block in blocks
        if block["first_three_tail"]["row_count"]
    ]
    first_failures = []
    for block in blocks:
        first_failures.extend(block["first_three_tail"]["first_failure_rows"])
    return {
        "block_indices": [
            block["block_index_after_discovery"] for block in blocks],
        "starts": [block["start"] for block in blocks],
        "first_three_tail_count": tail_count,
        "first_three_tail_failure_count": tail_failures,
        "active_selector_count": active_count,
        "active_selector_failure_count": active_failures,
        "predicate_full_nonpositive_count": full_nonpositive,
        "minimum_rescue_margin": min(margins) if margins else None,
        "minimum_complement_to_required_ratio": (
            min(ratios) if ratios else None),
        "first_failure_rows": sorted(
            first_failures,
            key=lambda row: (
                row["rescue_margin_to_zero"], row["target"]))[:12],
    }


def summarize_cycles(cycles):
    tail_count = sum(row["first_three_tail_count"] for row in cycles)
    active_count = sum(row["active_selector_count"] for row in cycles)
    failures = sum(row["full_nonpositive_count"] for row in cycles)
    rescued = sum(row["rescued_count"] for row in cycles)
    margins = [row["minimum_rescue_margin"] for row in cycles]
    return {
        "cycle_count": len(cycles),
        "first_three_tail_count": tail_count,
        "active_selector_count": active_count,
        "rescued_count": rescued,
        "full_nonpositive_count": failures,
        "minimum_rescue_margin": min(margins) if margins else None,
        "failing_cycles": [
            row for row in cycles if row["full_nonpositive_count"] > 0],
    }


def pass_status(summary):
    return (
        summary["first_three_tail_count"] > 0
        and summary["first_three_tail_failure_count"] == 0
        and summary["active_selector_failure_count"] == 0
        and summary["minimum_rescue_margin"] is not None
        and summary["minimum_rescue_margin"] > TOLERANCE
    )


def main():
    schedule = load_json(SOURCE)
    blocks = schedule["block_summaries"]
    by_index = {block["block_index_after_discovery"]: block for block in blocks}
    cycles = (
        schedule["discovery_block"]["cycle_summary"]
        + schedule["post_discovery_blocks"]["cycle_summary"]
    )

    suffix_candidates = []
    for threshold in sorted(by_index):
        selected = [
            block for block in blocks
            if block["block_index_after_discovery"] >= threshold
        ]
        summary = summarize_blocks(selected)
        suffix_candidates.append({
            "candidate": (
                f"block_index_after_discovery >= {threshold}"),
            "threshold": threshold,
            "summary": summary,
            "passes_current_fixture": pass_status(summary),
            "status": (
                "supported_on_current_fixture"
                if pass_status(summary)
                else "falsified_on_current_fixture"),
        })

    smallest_supported_suffix = next(
        (
            item for item in suffix_candidates
            if item["passes_current_fixture"]
        ),
        None,
    )
    all_blocks = suffix_candidates[0]
    post_discovery = next(
        item for item in suffix_candidates if item["threshold"] == 1)
    scheduled_future = next(
        item for item in suffix_candidates if item["threshold"] == 2)

    cycle_ge_4 = summarize_cycles(
        [row for row in cycles if row["cycle"] >= 4])
    discovery_cycles_4_to_6 = summarize_cycles(
        [
            row for row in cycles
            if row["block_index_after_discovery"] == 0
            and 4 <= row["cycle"] <= 6
        ])
    discovery_cycle_7 = summarize_cycles(
        [
            row for row in cycles
            if row["block_index_after_discovery"] == 0
            and row["cycle"] == 7
        ])

    tight_post_row = schedule["post_discovery_blocks"]["first_three_tail"][
        "tightest_rescue_rows"][0]
    worst_discovery_row = schedule["discovery_block"]["first_three_tail"][
        "tightest_rescue_rows"][0]

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_schedule": str(SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite derived threshold-candidate audit only; no eventual "
            "threshold theorem, signed correlation theorem, pointwise "
            "character-sum theorem, or Goldbach proof."),
        "question": (
            "Which complement-rescue threshold statements survive the checked "
            "q286 margin schedule, and which tempting shortcuts are "
            "tautological or already falsified?"),
        "mechanism": (
            "A row is rescued exactly when "
            "complement_to_principal_ratio exceeds "
            "-first_three_modes_to_principal_ratio.  The audit therefore "
            "separates explanatory candidate thresholds from statements that "
            "merely restate this identity."),
        "suffix_threshold_candidates": suffix_candidates,
        "decision_metrics": {
            "all_blocks_rescue_claim_passes": (
                all_blocks["passes_current_fixture"]),
            "all_blocks_failure_count": (
                all_blocks["summary"]["first_three_tail_failure_count"]),
            "smallest_supported_suffix_threshold": (
                smallest_supported_suffix["threshold"]
                if smallest_supported_suffix else None),
            "post_discovery_threshold_passes": (
                post_discovery["passes_current_fixture"]),
            "post_discovery_tail_count": (
                post_discovery["summary"]["first_three_tail_count"]),
            "post_discovery_failure_count": (
                post_discovery["summary"][
                    "first_three_tail_failure_count"]),
            "post_discovery_minimum_rescue_margin": (
                post_discovery["summary"]["minimum_rescue_margin"]),
            "post_discovery_minimum_complement_to_required_ratio": (
                post_discovery["summary"][
                    "minimum_complement_to_required_ratio"]),
            "scheduled_future_threshold_passes": (
                scheduled_future["passes_current_fixture"]),
            "scheduled_future_tail_count": (
                scheduled_future["summary"]["first_three_tail_count"]),
            "cycle_ge_4_candidate_passes": (
                cycle_ge_4["full_nonpositive_count"] == 0
                and cycle_ge_4["minimum_rescue_margin"] > TOLERANCE),
            "cycle_ge_4_failure_count": (
                cycle_ge_4["full_nonpositive_count"]),
            "discovery_cycles_4_to_6_pass": (
                discovery_cycles_4_to_6["full_nonpositive_count"] == 0
                and discovery_cycles_4_to_6["minimum_rescue_margin"]
                > TOLERANCE),
            "discovery_cycle_7_failure_count": (
                discovery_cycle_7["full_nonpositive_count"]),
            "tail_pressure_disappears_post_discovery": (
                post_discovery["summary"]["first_three_tail_count"] == 0),
            "tautological_rescue_ratio_flagged": True,
            "goldbach_proved": False,
        },
        "candidate_decisions": [
            {
                "name": "unconditional_all_checked_blocks_rescue",
                "status": "falsified_on_current_fixture",
                "reason": (
                    "The discovery block contributes first-three-tail "
                    "full_nonpositive rows, so no all-block rescue statement "
                    "is available without excluding or explaining that early "
                    "stress block."),
                "summary": all_blocks["summary"],
                "representative_failure": worst_discovery_row,
            },
            {
                "name": "post_discovery_suffix_threshold",
                "status": "supported_finite_candidate_not_theorem",
                "condition": "block_index_after_discovery >= 1",
                "reason": (
                    "This is the smallest suffix threshold in the checked "
                    "schedule with tail support, zero failures, and positive "
                    "minimum rescue margin.  It is still derived from the "
                    "same schedule and must be frozen against future unseen "
                    "blocks before promotion."),
                "summary": post_discovery["summary"],
                "tightest_row": tight_post_row,
            },
            {
                "name": "scheduled_future_suffix_threshold",
                "status": "supported_finite_candidate_not_theorem",
                "condition": "block_index_after_discovery >= 2",
                "reason": (
                    "The later scheduled subset has a larger margin, but the "
                    "smaller block>=1 suffix already passes and is the more "
                    "informative current separator."),
                "summary": scheduled_future["summary"],
            },
            {
                "name": "cycle_ge_4_rescue",
                "status": "falsified_on_current_fixture",
                "reason": (
                    "Discovery cycles 4, 5, and 6 pass, but discovery cycle "
                    "7 has full_nonpositive rows.  A within-block late-cycle "
                    "shortcut is therefore not durable."),
                "cycle_ge_4_summary": cycle_ge_4,
                "discovery_cycles_4_to_6_summary": discovery_cycles_4_to_6,
                "discovery_cycle_7_summary": discovery_cycle_7,
            },
            {
                "name": "complement_to_required_ratio_greater_than_one",
                "status": "tautology_not_explanation",
                "reason": (
                    "For first-three-tail rows, complement_to_required_ratio "
                    "> 1 is algebraically equivalent to positive rescue.  It "
                    "is a verification metric, not an independent theorem "
                    "mechanism."),
            },
            {
                "name": "tail_pressure_disappears_after_discovery",
                "status": "falsified_on_current_fixture",
                "reason": (
                    "Post-discovery blocks still contain first-three-tail "
                    "rows; the hole closes by complement surplus, not by the "
                    "absence of tail pressure."),
                "post_discovery_tail_count": (
                    post_discovery["summary"]["first_three_tail_count"]),
            },
        ],
        "prospective_falsifier": (
            "Freeze the block>=1 suffix condition before testing additional "
            "q286 blocks beyond start 410400.  Any first_three_tail or "
            "active-selector row in that predeclared future horizon with "
            "full_action_to_principal_ratio <= 0 falsifies the finite "
            "threshold candidate as a generalizing rule."),
        "next_obligation": (
            "Replace the empirical block suffix with a non-circular arithmetic "
            "or correlation condition that implies "
            "complement_to_principal_ratio > "
            "-first_three_modes_to_principal_ratio on the intended class."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
