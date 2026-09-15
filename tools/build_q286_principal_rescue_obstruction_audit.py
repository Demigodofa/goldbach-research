"""Separate first-three<-1 obstruction from nonprincipal drag on q286 tails.

The later-tail source decomposition showed that the principal baseline alone
keeps the later 73 tail rows positive.  This receipt reruns the validated
prime-indexed q286 row verifier over the checked discovery, post-discovery,
and later blocks, then classifies every first-three-tail row by

    principal_only_margin = 1 + first_three_modes_to_principal_ratio
    nonprincipal_correction = complement_to_principal_ratio - 1
    full = principal_only_margin + nonprincipal_correction.

Finite diagnostic only.  It does not prove a threshold theorem, signed
correlation theorem, pointwise character-sum theorem, or Goldbach.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-principal-rescue-obstruction-audit.json"

MARGIN_SCHEDULE = EVIDENCE / "q286-complement-rescue-margin-schedule.json"
LATER_SCAN = EVIDENCE / "q286-prime-indexed-later-full-block-scan.json"
ROW_VERIFIER = EVIDENCE / "q286-prime-indexed-row-filter-order-audit.json"
SUPPORT_SOURCE = EVIDENCE / "q286-mod13-4-support-schedule-audit.json"

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_mod13_4_prospective_descriptor_audit import (  # noqa: E402
    DISCOVERY_CYCLES,
    DISCOVERY_START,
    TAIL_THRESHOLD,
    TARGETS_PER_CYCLE,
)
from tools.build_q286_prime_indexed_kernel_route_audit import logs  # noqa: E402
from tools.build_q286_prime_indexed_row_filter_order_audit import (  # noqa: E402
    TOLERANCE,
    load_json,
    optimized_filter_row,
    prepare_support_context,
)


BLOCK_INDICES = tuple(range(12))


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


def compact_tail_row(target, row, block_index, start, cycle, period):
    first_three = float(row["first_three_modes_to_principal_ratio"])
    complement = float(row["complement_to_principal_ratio"])
    full = float(row["full_action_to_principal_ratio"])
    principal_only_margin = 1.0 + first_three
    nonprincipal_correction = complement - 1.0
    full_rebuilt = principal_only_margin + nonprincipal_correction
    return {
        "target": int(target),
        "block_index_after_discovery": int(block_index),
        "block_start": int(start),
        "local_cycle": int(cycle),
        "global_cycle": int((start - DISCOVERY_START) // period + cycle),
        "target_mod_13": int(target) % 13,
        "target_mod_143": int(target) % 143,
        "target_mod_286": int(target) % 286,
        "first_two_modes_to_principal_ratio": float(
            row["first_two_modes_to_principal_ratio"]),
        "first_three_modes_to_principal_ratio": first_three,
        "complement_to_principal_ratio": complement,
        "full_action_to_principal_ratio": full,
        "principal_only_margin": principal_only_margin,
        "nonprincipal_correction": nonprincipal_correction,
        "nonprincipal_drag": max(0.0, -nonprincipal_correction),
        "full_rebuild_error": abs(full_rebuilt - full),
        "principal_only_positive": principal_only_margin > TOLERANCE,
        "first_three_below_minus_one": (
            principal_only_margin <= TOLERANCE),
        "nonprincipal_correction_positive": (
            nonprincipal_correction > TOLERANCE),
        "full_positive": full > TOLERANCE,
        "full_nonpositive": full <= TOLERANCE,
        "principal_fails_but_nonprincipal_rescues": (
            principal_only_margin <= TOLERANCE and full > TOLERANCE),
        "principal_passes_but_nonprincipal_drag_breaks": (
            principal_only_margin > TOLERANCE and full <= TOLERANCE),
    }


def summarize_rows(name, rows):
    return {
        "name": name,
        "row_count": len(rows),
        "principal_only_positive_count": sum(
            1 for row in rows if row["principal_only_positive"]),
        "first_three_below_minus_one_count": sum(
            1 for row in rows if row["first_three_below_minus_one"]),
        "full_nonpositive_count": sum(
            1 for row in rows if row["full_nonpositive"]),
        "principal_fails_but_nonprincipal_rescues_count": sum(
            1 for row in rows
            if row["principal_fails_but_nonprincipal_rescues"]),
        "principal_passes_but_nonprincipal_drag_breaks_count": sum(
            1 for row in rows
            if row["principal_passes_but_nonprincipal_drag_breaks"]),
        "first_three_summary": finite_summary(
            row["first_three_modes_to_principal_ratio"] for row in rows),
        "principal_only_margin_summary": finite_summary(
            row["principal_only_margin"] for row in rows),
        "nonprincipal_correction_summary": finite_summary(
            row["nonprincipal_correction"] for row in rows),
        "nonprincipal_drag_summary": finite_summary(
            row["nonprincipal_drag"] for row in rows),
        "full_action_summary": finite_summary(
            row["full_action_to_principal_ratio"] for row in rows),
        "maximum_full_rebuild_error": max(
            (row["full_rebuild_error"] for row in rows), default=0.0),
        "tightest_principal_only_rows": sorted(
            rows, key=lambda row: (
                row["principal_only_margin"], row["target"]))[:20],
        "worst_full_rows": sorted(
            rows, key=lambda row: (
                row["full_action_to_principal_ratio"], row["target"]))[:20],
        "first_full_failure_rows": sorted(
            (row for row in rows if row["full_nonpositive"]),
            key=lambda row: (
                row["full_action_to_principal_ratio"], row["target"]))[:50],
    }


def scan_block(block_index, period, context, primes, prime_values, log_values):
    start = block_start(period, block_index)
    tail_rows = []
    predicate_counts = {
        "first_two_active": 0,
        "first_three_tail": 0,
        "full_nonpositive": 0,
    }
    started = time.perf_counter()
    for cycle in range(DISCOVERY_CYCLES):
        cycle_start = start + cycle * period
        for offset in range(TARGETS_PER_CYCLE):
            target = cycle_start + 2 * offset
            row = optimized_filter_row(
                target, context, primes, prime_values, log_values)
            predicates = set(row["passed_predicates"])
            for predicate in predicate_counts:
                if predicate in predicates:
                    predicate_counts[predicate] += 1
            if "first_three_tail" in predicates:
                tail_rows.append(compact_tail_row(
                    target, row, block_index, start, cycle, period))
    return {
        "block_index_after_discovery": int(block_index),
        "start": int(start),
        "tested_target_count": DISCOVERY_CYCLES * TARGETS_PER_CYCLE,
        "seconds": time.perf_counter() - started,
        "predicate_counts": predicate_counts,
        "tail_summary": summarize_rows("first_three_tail", tail_rows),
        "tail_rows": tail_rows,
    }


def aggregate_named(blocks, name, predicate):
    rows = [
        row for block in blocks if predicate(block)
        for row in block["tail_rows"]]
    return summarize_rows(name, rows)


def validate_against_sources(blocks, margin_schedule, later_scan):
    discovery = aggregate_named(
        blocks, "discovery", lambda block: (
            block["block_index_after_discovery"] == 0))
    post_discovery_1_to_5 = aggregate_named(
        blocks, "post_discovery_blocks_1_to_5", lambda block: (
            1 <= block["block_index_after_discovery"] <= 5))
    later_6_to_11 = aggregate_named(
        blocks, "later_blocks_6_to_11", lambda block: (
            block["block_index_after_discovery"] >= 6))
    observed = {
        "discovery_first_three_tail_count": discovery["row_count"],
        "discovery_first_three_tail_full_nonpositive_count": (
            discovery["full_nonpositive_count"]),
        "post_discovery_first_three_tail_count": (
            post_discovery_1_to_5["row_count"]),
        "post_discovery_first_three_tail_full_nonpositive_count": (
            post_discovery_1_to_5["full_nonpositive_count"]),
        "later_first_three_tail_count": later_6_to_11["row_count"],
        "later_first_three_tail_full_nonpositive_count": (
            later_6_to_11["full_nonpositive_count"]),
    }
    expected = {
        "discovery_first_three_tail_count": (
            margin_schedule["decision_metrics"][
                "discovery_first_three_tail_count"]),
        "discovery_first_three_tail_full_nonpositive_count": (
            margin_schedule["decision_metrics"][
                "discovery_first_three_tail_full_nonpositive_count"]),
        "post_discovery_first_three_tail_count": (
            margin_schedule["decision_metrics"][
                "post_discovery_first_three_tail_count"]),
        "post_discovery_first_three_tail_full_nonpositive_count": (
            margin_schedule["decision_metrics"][
                "post_discovery_first_three_tail_full_nonpositive_count"]),
        "later_first_three_tail_count": (
            later_scan["decision_metrics"]["first_three_tail_count"]),
        "later_first_three_tail_full_nonpositive_count": (
            later_scan["decision_metrics"][
                "first_three_tail_full_nonpositive_count"]),
    }
    matches = {
        key: observed[key] == expected[key] for key in expected}
    return {
        "observed": observed,
        "expected": expected,
        "matches": matches,
        "all_source_counts_match": all(matches.values()),
    }


def main():
    margin_schedule = load_json(MARGIN_SCHEDULE)
    later_scan = load_json(LATER_SCAN)
    row_verifier = load_json(ROW_VERIFIER)
    support = load_json(SUPPORT_SOURCE)
    period = int(support["schedule"]["arithmetic_period"])
    maximum_target = (
        block_start(period, BLOCK_INDICES[-1])
        + (DISCOVERY_CYCLES - 1) * period
        + 2 * (TARGETS_PER_CYCLE - 1))
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    context = prepare_support_context()

    blocks = []
    started = time.perf_counter()
    for block_index in BLOCK_INDICES:
        block = scan_block(
            block_index, period, context, primes, prime_values, log_values)
        blocks.append(block)
        print(
            f"block {block_index}: tail="
            f"{block['tail_summary']['row_count']} full_fail="
            f"{block['tail_summary']['full_nonpositive_count']} "
            f"principal_fail="
            f"{block['tail_summary']['first_three_below_minus_one_count']} "
            f"seconds={block['seconds']:.3f}",
            flush=True)
    elapsed = time.perf_counter() - started
    validation = validate_against_sources(
        blocks, margin_schedule, later_scan)
    all_tail = summarize_rows(
        "all_blocks_0_to_11",
        [row for block in blocks for row in block["tail_rows"]])
    discovery = aggregate_named(
        blocks, "discovery_block_0", lambda block: (
            block["block_index_after_discovery"] == 0))
    post_discovery = aggregate_named(
        blocks, "post_discovery_blocks_1_to_11", lambda block: (
            block["block_index_after_discovery"] >= 1))
    early_checked = aggregate_named(
        blocks, "post_discovery_blocks_1_to_5", lambda block: (
            1 <= block["block_index_after_discovery"] <= 5))
    later_checked = aggregate_named(
        blocks, "later_blocks_6_to_11", lambda block: (
            block["block_index_after_discovery"] >= 6))

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "margin_schedule": str(MARGIN_SCHEDULE.relative_to(ROOT)),
            "later_full_block_scan": str(LATER_SCAN.relative_to(ROOT)),
            "row_verifier": str(ROW_VERIFIER.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite q286 principal-rescue obstruction audit only; reruns "
            "checked blocks with the validated row verifier and proves no "
            "eventual first_three > -1 theorem, nonprincipal drag bound, "
            "signed correlation theorem, pointwise character-sum theorem, or "
            "Goldbach."),
        "question": (
            "Across checked q286 discovery, post-discovery, and later blocks, "
            "are nonrescued tail rows caused by first_three dropping below "
            "-1, by nonprincipal drag overturning principal-only positivity, "
            "or by both?"),
        "mechanism": (
            "For every first-three-tail row in blocks 0..11, compute "
            "principal_only_margin = 1 + first_three and "
            "nonprincipal_correction = complement - 1, then classify whether "
            "the principal baseline alone is positive and whether "
            "nonprincipal correction rescues or breaks the row."),
        "prediction": (
            "If the principal-rescue theorem shape is correct, checked "
            "post-discovery rows should have positive principal-only margins, "
            "and discovery failures should line up with first_three < -1 "
            "rather than principal-positive rows broken by nonprincipal drag."),
        "falsifier": (
            "Any full-nonpositive tail row with principal_only_margin > 0 "
            "is a nonprincipal-drag overturning witness and falsifies the "
            "claim that the checked obstruction is only first_three < -1."),
        "upstream_validation": {
            "optimized_row_verifier_validated": (
                row_verifier["decision_metrics"][
                    "optimized_row_verifier_validated"]),
            "source_count_validation": validation,
        },
        "schedule": {
            "block_indices_after_discovery": list(BLOCK_INDICES),
            "cycle_count_per_block": DISCOVERY_CYCLES,
            "targets_per_cycle": TARGETS_PER_CYCLE,
            "tested_target_count": (
                len(BLOCK_INDICES) * DISCOVERY_CYCLES
                * TARGETS_PER_CYCLE),
        },
        "block_summaries": [
            {
                "block_index_after_discovery": (
                    block["block_index_after_discovery"]),
                "start": block["start"],
                "tested_target_count": block["tested_target_count"],
                "seconds": block["seconds"],
                "predicate_counts": block["predicate_counts"],
                "tail_summary": block["tail_summary"],
            } for block in blocks
        ],
        "aggregate_summaries": {
            "all_blocks_0_to_11": all_tail,
            "discovery_block_0": discovery,
            "post_discovery_blocks_1_to_11": post_discovery,
            "post_discovery_blocks_1_to_5": early_checked,
            "later_blocks_6_to_11": later_checked,
        },
        "decision_metrics": {
            "source_counts_match": validation["all_source_counts_match"],
            "tested_target_count": (
                len(BLOCK_INDICES) * DISCOVERY_CYCLES
                * TARGETS_PER_CYCLE),
            "tail_row_count": all_tail["row_count"],
            "full_nonpositive_tail_count": (
                all_tail["full_nonpositive_count"]),
            "first_three_below_minus_one_tail_count": (
                all_tail["first_three_below_minus_one_count"]),
            "principal_positive_full_nonpositive_tail_count": (
                all_tail[
                    "principal_passes_but_nonprincipal_drag_breaks_count"]),
            "discovery_full_nonpositive_tail_count": (
                discovery["full_nonpositive_count"]),
            "discovery_first_three_below_minus_one_tail_count": (
                discovery["first_three_below_minus_one_count"]),
            "post_discovery_tail_count": post_discovery["row_count"],
            "post_discovery_first_three_below_minus_one_tail_count": (
                post_discovery["first_three_below_minus_one_count"]),
            "post_discovery_full_nonpositive_tail_count": (
                post_discovery["full_nonpositive_count"]),
            "post_discovery_principal_only_minimum_margin": (
                post_discovery["principal_only_margin_summary"]["minimum"]),
            "later_principal_only_minimum_margin": (
                later_checked["principal_only_margin_summary"]["minimum"]),
            "maximum_full_rebuild_error": (
                all_tail["maximum_full_rebuild_error"]),
            "elapsed_seconds": elapsed,
            "goldbach_proved": False,
        },
        "decision": (
            "Read principal_positive_full_nonpositive_tail_count. If it is "
            "zero and all full failures have first_three_below_minus_one, "
            "the checked q286 obstruction is the first-three<-1 event, while "
            "post-discovery rescue reduces to proving first_three>-1 plus a "
            "nonprincipal drag bound that does not overturn the positive "
            "principal-only margin."),
        "next_obligation": (
            "Search for an arithmetic condition or Fourier/operator bound "
            "that prevents first_three_modes_to_principal_ratio from dropping "
            "below -1 after the discovery block, then separately bound "
            "nonprincipal drag against the remaining principal-only surplus."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
