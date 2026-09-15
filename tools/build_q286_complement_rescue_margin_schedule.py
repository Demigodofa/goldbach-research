"""Audit q286 complement-rescue margins after the mod-13 support starvation.

The mod-13 low-(3,1) pocket could not be tested after discovery because the
next scheduled blocks had no ``full_nonpositive`` rows.  This receipt steps
back from single-channel classifier language and measures the direct rescue
identity:

    full_action_to_principal_ratio
        = first_three_modes_to_principal_ratio
          + complement_to_principal_ratio.

Finite evidence only: this is a margin schedule and theorem-shaping
obligation, not a complement-rescue theorem, signed correlation theorem,
pointwise character-sum theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-complement-rescue-margin-schedule.json"
SUPPORT_SOURCE = EVIDENCE / "q286-mod13-4-support-schedule-audit.json"
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_filter_order_audit_receipt,
)
from tools.build_q286_mod13_4_prospective_descriptor_audit import (  # noqa: E402
    COMPLEMENT_FLOOR,
    DISCOVERY_CYCLES,
    DISCOVERY_START,
    TAIL_THRESHOLD,
    TARGETS_PER_CYCLE,
)


BLOCK_INDICES = (0, 1, 2, 3, 4, 5)
TOLERANCE = 1e-9


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def finite_summary(values):
    values = tuple(float(value) for value in values)
    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None}
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def block_start(period, block_index):
    return DISCOVERY_START + int(block_index) * DISCOVERY_CYCLES * int(period)


def row_metrics(target, row, block_index, start):
    first_three = float(row["first_three_modes_to_principal_ratio"])
    complement = float(row["complement_to_principal_ratio"])
    full = float(row["full_action_to_principal_ratio"])
    required = max(0.0, -first_three)
    identity_error = abs((first_three + complement) - full)
    return {
        "target": int(target),
        "block_index_after_discovery": int(block_index),
        "block_start": int(start),
        "cycle": int(row["cycle"]),
        "target_mod_13": int(target) % 13,
        "target_mod_143": int(target) % 143,
        "target_mod_286": int(target) % 286,
        "first_three_modes_to_principal_ratio": first_three,
        "complement_to_principal_ratio": complement,
        "full_action_to_principal_ratio": full,
        "required_complement_to_cancel_first_three": required,
        "complement_surplus_to_cancel_first_three": complement - required,
        "complement_to_required_ratio": (
            complement / required if required > TOLERANCE else math.inf),
        "tail_depth_below_threshold": max(
            0.0, -TAIL_THRESHOLD - first_three),
        "rescue_margin_to_zero": full,
        "identity_error": identity_error,
        "first_two_active": "first_two_active" in row["passed_predicates"],
        "first_three_tail": "first_three_tail" in row["passed_predicates"],
        "complement_floor": "complement_floor" in row["passed_predicates"],
        "full_positive": "full_positive" in row["passed_predicates"],
        "full_nonpositive": "full_nonpositive" in row["passed_predicates"],
        "passed_predicates": row["passed_predicates"],
    }


def summarize_rows(name, rows):
    failures = [
        row for row in rows
        if row["rescue_margin_to_zero"] <= TOLERANCE]
    nonfloor = [
        row for row in rows
        if not row["complement_floor"]]
    return {
        "name": name,
        "row_count": len(rows),
        "rescued_count": len(rows) - len(failures),
        "failure_count": len(failures),
        "complement_floor_failure_count": len(nonfloor),
        "rescue_margin_to_zero_summary": finite_summary(
            row["rescue_margin_to_zero"] for row in rows),
        "first_three_ratio_summary": finite_summary(
            row["first_three_modes_to_principal_ratio"] for row in rows),
        "complement_ratio_summary": finite_summary(
            row["complement_to_principal_ratio"] for row in rows),
        "complement_surplus_summary": finite_summary(
            row["complement_surplus_to_cancel_first_three"] for row in rows),
        "complement_to_required_ratio_summary": finite_summary(
            row["complement_to_required_ratio"] for row in rows
            if math.isfinite(row["complement_to_required_ratio"])),
        "tail_depth_below_threshold_summary": finite_summary(
            row["tail_depth_below_threshold"] for row in rows),
        "max_identity_error": max(
            (row["identity_error"] for row in rows), default=0.0),
        "tightest_rescue_rows": sorted(
            rows,
            key=lambda row: (
                row["rescue_margin_to_zero"], row["target"]))[:12],
        "deepest_tail_rows": sorted(
            rows,
            key=lambda row: (
                -row["tail_depth_below_threshold"], row["target"]))[:12],
        "first_failure_rows": sorted(
            failures,
            key=lambda row: (
                row["rescue_margin_to_zero"], row["target"]))[:12],
    }


def cycle_summary(rows):
    by_cycle = {}
    for row in rows:
        key = (row["block_index_after_discovery"], row["block_start"],
               row["cycle"])
        by_cycle.setdefault(key, []).append(row)
    return [
        {
            "block_index_after_discovery": block_index,
            "block_start": start,
            "cycle": cycle,
            "active_selector_count": sum(
                1 for row in cycle_rows if row["first_two_active"]),
            "first_three_tail_count": len(cycle_rows),
            "rescued_count": sum(
                1 for row in cycle_rows
                if row["rescue_margin_to_zero"] > TOLERANCE),
            "full_nonpositive_count": sum(
                1 for row in cycle_rows if row["full_nonpositive"]),
            "minimum_rescue_margin": min(
                row["rescue_margin_to_zero"] for row in cycle_rows),
        }
        for (block_index, start, cycle), cycle_rows in sorted(by_cycle.items())
    ]


def block_summary(block_index, start, receipt, tail_rows):
    active_rows = [row for row in tail_rows if row["first_two_active"]]
    return {
        "block_index_after_discovery": int(block_index),
        "start": int(start),
        "tested_target_count": int(receipt["tested_target_count"]),
        "predicate_counts": receipt["predicate_counts"],
        "first_three_tail": summarize_rows("first_three_tail", tail_rows),
        "active_selector": summarize_rows("active_selector", active_rows),
    }


def aggregate_schedule(blocks, block_filter):
    selected_blocks = [
        block for block in blocks if block_filter(block)
    ]
    rows = [
        row
        for block in selected_blocks
        for row in block["tail_rows"]
    ]
    active_rows = [row for row in rows if row["first_two_active"]]
    return {
        "first_three_tail": summarize_rows("first_three_tail", rows),
        "active_selector": summarize_rows("active_selector", active_rows),
        "cycle_summary": cycle_summary(rows),
        "predicate_full_nonpositive_count": sum(
            int(block["summary"]["predicate_counts"]["full_nonpositive"])
            for block in selected_blocks),
        "predicate_full_positive_count": sum(
            int(block["summary"]["predicate_counts"]["full_positive"])
            for block in selected_blocks),
    }


def main():
    support_payload = load_json(SUPPORT_SOURCE)
    period = int(support_payload["schedule"]["arithmetic_period"])
    blocks = []
    for block_index in BLOCK_INDICES:
        start = block_start(period, block_index)
        receipt = q286_first_three_filter_order_audit_receipt(
            start=start,
            cycle_count=DISCOVERY_CYCLES,
            targets_per_cycle=TARGETS_PER_CYCLE,
            tail_threshold=TAIL_THRESHOLD,
            complement_floor=COMPLEMENT_FLOOR)
        tail_targets = [
            int(target) for target, row in receipt["target_rows"].items()
            if "first_three_tail" in row["passed_predicates"]
        ]
        tail_rows = [
            row_metrics(target, receipt["target_rows"][target],
                        block_index, start)
            for target in sorted(tail_targets)
        ]
        blocks.append({
            "block_index_after_discovery": int(block_index),
            "start": int(start),
            "tail_rows": tail_rows,
            "summary": block_summary(block_index, start, receipt, tail_rows),
        })

    discovery = aggregate_schedule(
        blocks, lambda block: block["block_index_after_discovery"] == 0)
    post_discovery = aggregate_schedule(
        blocks, lambda block: block["block_index_after_discovery"] > 0)
    scheduled_future = aggregate_schedule(
        blocks, lambda block: block["block_index_after_discovery"] >= 2)
    post_tail = post_discovery["first_three_tail"]
    post_active = post_discovery["active_selector"]
    finite_passes_post_discovery = (
        post_tail["row_count"] > 0
        and post_tail["failure_count"] == 0
        and post_active["failure_count"] == 0)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "mod13_4_support_schedule": str(
                SUPPORT_SOURCE.relative_to(ROOT)),
            "filter_order_receipt":
                "q286_first_three_filter_order_audit_receipt",
        },
        "status_boundary": (
            "finite complement-rescue margin schedule only; compares "
            "discovery and post-discovery q286 blocks and records exact "
            "rescue margins. It proves no eventual complement-rescue "
            "theorem, signed correlation theorem, pointwise character-sum "
            "theorem, or Goldbach proof."),
        "question": (
            "When the mod13==4 classifier is support-starved, do the later "
            "q286 active/tail rows disappear, or are they present but "
            "rescued by positive complement contribution?"),
        "mechanism": (
            "For each predeclared block, select first_three_tail rows and "
            "measure first_three + complement = full. A row is rescued when "
            "full_action_to_principal_ratio is positive, equivalently when "
            "the complement exceeds the amount needed to cancel the "
            "negative first-three contribution."),
        "prediction": (
            "A complement-rescue lane should show post-discovery tail and "
            "active rows with positive rescue margins, while the discovery "
            "block retains the known full_nonpositive failures."),
        "falsifier": (
            "Any post-discovery first_three_tail or active-selector row with "
            "full_action_to_principal_ratio <= 0 falsifies the finite "
            "post-discovery rescue schedule. The discovery block's failures "
            "falsify any theorem that claims this rescue without excluding "
            "or explaining the early stress block."),
        "schedule": {
            "arithmetic_period": period,
            "block_indices": list(BLOCK_INDICES),
            "starts": [block_start(period, index) for index in BLOCK_INDICES],
            "cycle_count_per_block": DISCOVERY_CYCLES,
            "targets_per_cycle": TARGETS_PER_CYCLE,
        },
        "block_summaries": [block["summary"] for block in blocks],
        "discovery_block": discovery,
        "post_discovery_blocks": post_discovery,
        "scheduled_future_blocks": scheduled_future,
        "decision_metrics": {
            "finite_post_discovery_rescue_passes": (
                finite_passes_post_discovery),
            "discovery_first_three_tail_count": (
                discovery["first_three_tail"]["row_count"]),
            "discovery_first_three_tail_full_nonpositive_count": (
                discovery["first_three_tail"]["failure_count"]),
            "discovery_predicate_full_nonpositive_count": (
                discovery["predicate_full_nonpositive_count"]),
            "post_discovery_first_three_tail_count": (
                post_discovery["first_three_tail"]["row_count"]),
            "post_discovery_active_selector_count": (
                post_discovery["active_selector"]["row_count"]),
            "post_discovery_first_three_tail_full_nonpositive_count": (
                post_discovery["first_three_tail"]["failure_count"]),
            "post_discovery_predicate_full_nonpositive_count": (
                post_discovery["predicate_full_nonpositive_count"]),
            "scheduled_future_first_three_tail_count": (
                scheduled_future["first_three_tail"]["row_count"]),
            "scheduled_future_first_three_tail_full_nonpositive_count": (
                scheduled_future["first_three_tail"]["failure_count"]),
            "scheduled_future_predicate_full_nonpositive_count": (
                scheduled_future["predicate_full_nonpositive_count"]),
            "post_discovery_minimum_rescue_margin": (
                post_discovery["first_three_tail"][
                    "rescue_margin_to_zero_summary"]["minimum"]),
            "post_discovery_minimum_complement_to_required_ratio": (
                post_discovery["first_three_tail"][
                    "complement_to_required_ratio_summary"]["minimum"]),
            "maximum_identity_error": max(
                block["summary"]["first_three_tail"]["max_identity_error"]
                for block in blocks),
        },
        "decision": (
            "If finite_post_discovery_rescue_passes is true, the immediate "
            "mathematical target should be a complement-rescue/correlation "
            "estimate, not a single-residue or single-channel classifier. "
            "The discovery block's full_nonpositive rows remain an explicit "
            "early-block obstruction that a theorem must either exclude, "
            "bound, or explain."),
        "next_obligation": (
            "Define a non-circular arithmetic condition that lower-bounds "
            "complement_to_principal_ratio relative to the negative "
            "first_three_modes_to_principal_ratio, or prove an average/signed "
            "correlation cone that supplies the same positive rescue margin."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
