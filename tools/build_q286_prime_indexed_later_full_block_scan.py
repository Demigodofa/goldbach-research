"""Scan later q286 full blocks with the validated prime-indexed row verifier.

The sampled suffix holdout froze six later block starts beyond the checked
post-discovery schedule, but its first-101 and replayed-offset samples found no
first-three-tail support.  This receipt scans the full six later blocks with
the row-level verifier validated by
``build_q286_prime_indexed_row_filter_order_audit.py``.

Finite computation only: this classifies a predeclared later window.  It does
not prove a threshold theorem, signed correlation theorem, pointwise
character-sum theorem, or Goldbach.
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
OUT = EVIDENCE / "q286-prime-indexed-later-full-block-scan.json"

ROW_VERIFIER = EVIDENCE / "q286-prime-indexed-row-filter-order-audit.json"
SUFFIX_HOLDOUT = EVIDENCE / "q286-complement-rescue-suffix-holdout.json"
SUPPORT_SOURCE = EVIDENCE / "q286-mod13-4-support-schedule-audit.json"

sys.path.insert(0, str(ROOT))

from tools.build_q286_complement_rescue_margin_schedule import (  # noqa: E402
    block_start,
    finite_summary,
)
from tools.build_q286_mod13_4_prospective_descriptor_audit import (  # noqa: E402
    COMPLEMENT_FLOOR,
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
from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402


BLOCK_INDICES = (6, 7, 8, 9, 10, 11)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def compact_row(target, row, block_index, block_start_value, cycle, period):
    first_two = float(row["first_two_modes_to_principal_ratio"])
    first_three = float(row["first_three_modes_to_principal_ratio"])
    complement = float(row["complement_to_principal_ratio"])
    full = float(row["full_action_to_principal_ratio"])
    required = max(0.0, -first_three)
    complement_to_required = (
        complement / required if required > TOLERANCE else None)
    return {
        "target": int(target),
        "block_index_after_discovery": int(block_index),
        "block_start": int(block_start_value),
        "local_cycle": int(cycle),
        "global_cycle": int((block_start_value - DISCOVERY_START) // period
                            + cycle),
        "target_mod_13": int(target) % 13,
        "target_mod_143": int(target) % 143,
        "target_mod_286": int(target) % 286,
        "first_two_modes_to_principal_ratio": first_two,
        "first_three_modes_to_principal_ratio": first_three,
        "complement_to_principal_ratio": complement,
        "full_action_to_principal_ratio": full,
        "required_complement_to_cancel_first_three": required,
        "complement_surplus_to_cancel_first_three": complement - required,
        "complement_to_required_ratio": complement_to_required,
        "identity_error": abs((first_three + complement) - full),
        "small_support_to_principal_ratio": float(
            row["small_support_to_principal_ratio"]),
        "first_two_active": (
            "first_two_active" in row["passed_predicates"]),
        "first_three_tail": (
            "first_three_tail" in row["passed_predicates"]),
        "complement_positive": (
            "complement_positive" in row["passed_predicates"]),
        "complement_floor": (
            "complement_floor" in row["passed_predicates"]),
        "full_positive": (
            "full_positive" in row["passed_predicates"]),
        "full_nonpositive": (
            "full_nonpositive" in row["passed_predicates"]),
        "passed_predicates": list(row["passed_predicates"]),
    }


def summarize_tail_rows(name, rows):
    failures = [
        row for row in rows
        if row["full_action_to_principal_ratio"] <= TOLERANCE]
    active_rows = [row for row in rows if row["first_two_active"]]
    return {
        "name": name,
        "row_count": len(rows),
        "active_selector_count": len(active_rows),
        "rescued_count": len(rows) - len(failures),
        "failure_count": len(failures),
        "first_three_ratio_summary": finite_summary(
            row["first_three_modes_to_principal_ratio"] for row in rows),
        "complement_ratio_summary": finite_summary(
            row["complement_to_principal_ratio"] for row in rows),
        "full_action_ratio_summary": finite_summary(
            row["full_action_to_principal_ratio"] for row in rows),
        "complement_surplus_summary": finite_summary(
            row["complement_surplus_to_cancel_first_three"] for row in rows),
        "complement_to_required_ratio_summary": finite_summary(
            row["complement_to_required_ratio"] for row in rows
            if row["complement_to_required_ratio"] is not None),
        "maximum_identity_error": max(
            (row["identity_error"] for row in rows), default=0.0),
        "tightest_rescue_rows": sorted(
            rows,
            key=lambda row: (
                row["full_action_to_principal_ratio"], row["target"]))[:12],
        "deepest_tail_rows": sorted(
            rows,
            key=lambda row: (
                row["first_three_modes_to_principal_ratio"],
                row["target"]))[:12],
        "failure_rows": sorted(
            failures,
            key=lambda row: (
                row["full_action_to_principal_ratio"], row["target"]))[:50],
    }


def classify_candidate(tail_summary):
    if tail_summary["row_count"] == 0:
        return "support_starved_no_first_three_tail_rows"
    if tail_summary["failure_count"] == 0:
        return "rescued_with_tail_support"
    return "falsified_by_nonpositive_tail_rows"


def scan_block(
        block_index, start, period, context, primes, prime_values, log_values):
    predicate_counts = {
        "first_two_active": 0,
        "first_three_tail": 0,
        "complement_positive": 0,
        "complement_floor": 0,
        "full_positive": 0,
        "full_nonpositive": 0,
        "active_selector": 0,
        "rescued_first_three_tail": 0,
        "nonrescued_first_three_tail": 0,
        "active_nonrescued": 0,
    }
    cycle_rows = []
    tail_rows = []
    minimum_full_row = None
    minimum_first_three_row = None
    tested = 0
    started = time.perf_counter()
    for cycle in range(DISCOVERY_CYCLES):
        cycle_start = start + cycle * period
        cycle_tail_rows = []
        cycle_full_nonpositive = 0
        cycle_first_two_active = 0
        for offset in range(TARGETS_PER_CYCLE):
            target = cycle_start + 2 * offset
            row = optimized_filter_row(
                target, context, primes, prime_values, log_values)
            compact = compact_row(
                target, row, block_index, start, cycle, period)
            tested += 1
            for predicate in (
                    "first_two_active", "first_three_tail",
                    "complement_positive", "complement_floor",
                    "full_positive", "full_nonpositive"):
                if compact[predicate]:
                    predicate_counts[predicate] += 1
            if compact["first_two_active"]:
                cycle_first_two_active += 1
            if compact["first_three_tail"]:
                cycle_tail_rows.append(compact)
                tail_rows.append(compact)
                if compact["first_two_active"]:
                    predicate_counts["active_selector"] += 1
                if compact["full_positive"]:
                    predicate_counts["rescued_first_three_tail"] += 1
                if compact["full_nonpositive"]:
                    predicate_counts["nonrescued_first_three_tail"] += 1
                    if compact["first_two_active"]:
                        predicate_counts["active_nonrescued"] += 1
            if compact["full_nonpositive"]:
                cycle_full_nonpositive += 1
            if (minimum_full_row is None
                    or compact["full_action_to_principal_ratio"]
                    < minimum_full_row["full_action_to_principal_ratio"]):
                minimum_full_row = compact
            if (minimum_first_three_row is None
                    or compact["first_three_modes_to_principal_ratio"]
                    < minimum_first_three_row[
                        "first_three_modes_to_principal_ratio"]):
                minimum_first_three_row = compact
        cycle_rows.append({
            "local_cycle": cycle,
            "global_cycle": int((start - DISCOVERY_START) // period + cycle),
            "cycle_start": cycle_start,
            "target_count": TARGETS_PER_CYCLE,
            "first_two_active_count": cycle_first_two_active,
            "first_three_tail_count": len(cycle_tail_rows),
            "full_nonpositive_count": cycle_full_nonpositive,
            "nonrescued_tail_count": sum(
                1 for row in cycle_tail_rows if row["full_nonpositive"]),
            "minimum_tail_full_action_ratio": min(
                (row["full_action_to_principal_ratio"]
                 for row in cycle_tail_rows), default=None),
        })
    tail_summary = summarize_tail_rows("first_three_tail", tail_rows)
    return {
        "block_index_after_discovery": int(block_index),
        "start": int(start),
        "end": int(start + (DISCOVERY_CYCLES - 1) * period
                   + 2 * (TARGETS_PER_CYCLE - 1)),
        "tested_target_count": tested,
        "seconds": time.perf_counter() - started,
        "predicate_counts": predicate_counts,
        "cycle_rows": cycle_rows,
        "tail_summary": tail_summary,
        "candidate_status": classify_candidate(tail_summary),
        "minimum_full_row": minimum_full_row,
        "minimum_first_three_row": minimum_first_three_row,
        "tail_rows": tail_rows,
    }


def aggregate_blocks(blocks):
    tail_rows = [
        row for block in blocks for row in block["tail_rows"]]
    tested_target_count = sum(block["tested_target_count"] for block in blocks)
    predicate_counts = {
        key: sum(block["predicate_counts"][key] for block in blocks)
        for key in blocks[0]["predicate_counts"]
    } if blocks else {}
    tail_summary = summarize_tail_rows("first_three_tail", tail_rows)
    return {
        "tested_target_count": tested_target_count,
        "predicate_counts": predicate_counts,
        "tail_summary": tail_summary,
        "candidate_status": classify_candidate(tail_summary),
        "block_status_counts": {
            status: sum(
                1 for block in blocks if block["candidate_status"] == status)
            for status in sorted({
                block["candidate_status"] for block in blocks})
        },
        "minimum_full_row": min(
            (block["minimum_full_row"] for block in blocks),
            key=lambda row: row["full_action_to_principal_ratio"],
            default=None),
        "minimum_first_three_row": min(
            (block["minimum_first_three_row"] for block in blocks),
            key=lambda row: row["first_three_modes_to_principal_ratio"],
            default=None),
        "seconds": math.fsum(block["seconds"] for block in blocks),
    }


def main():
    support_payload = load_json(SUPPORT_SOURCE)
    row_verifier = load_json(ROW_VERIFIER)
    suffix_holdout = load_json(SUFFIX_HOLDOUT)
    period = int(support_payload["schedule"]["arithmetic_period"])
    starts = tuple(block_start(period, index) for index in BLOCK_INDICES)
    maximum_target = (
        starts[-1] + (DISCOVERY_CYCLES - 1) * period
        + 2 * (TARGETS_PER_CYCLE - 1))

    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    context = prepare_support_context()

    blocks = []
    full_start = time.perf_counter()
    for block_index, start in zip(BLOCK_INDICES, starts):
        block = scan_block(
            block_index, start, period, context, primes, prime_values,
            log_values)
        blocks.append(block)
        print(
            f"block {block_index} start {start}: "
            f"{block['candidate_status']}, "
            f"tail={block['tail_summary']['row_count']}, "
            f"fail={block['tail_summary']['failure_count']}, "
            f"seconds={block['seconds']:.3f}",
            flush=True)
    aggregate = aggregate_blocks(blocks)
    elapsed = time.perf_counter() - full_start

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "row_verifier": str(ROW_VERIFIER.relative_to(ROOT)),
            "suffix_sampled_holdout": str(SUFFIX_HOLDOUT.relative_to(ROOT)),
            "mod13_4_support_schedule": str(
                SUPPORT_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite predeclared later full-block scan only; this does not "
            "prove a threshold theorem, signed correlation theorem, "
            "pointwise character-sum theorem, or Goldbach."),
        "question": (
            "Do the six predeclared later q286 full blocks beyond start "
            "410400 remain support-starved like the sampled holdout, or do "
            "they contain first-three-tail rows that are rescued/falsified "
            "by the full recombined action?"),
        "mechanism": (
            "Use the validated prime-indexed row verifier to scan every even "
            "target in blocks 6..11, each with 8 q286 cycles and 5005 "
            "targets per cycle. Classify first-three-tail rows as rescued "
            "when full_action_to_principal_ratio remains positive."),
        "prediction": (
            "If the post-discovery complement-rescue threshold generalizes "
            "to these unseen blocks, every first-three-tail row should have "
            "positive full action. If no first-three-tail rows appear, the "
            "test remains support-starved. If any tail row is nonpositive, "
            "the frozen suffix candidate is finitely falsified."),
        "falsifier": (
            "Any block-index 6..11 first-three-tail row with "
            "full_action_to_principal_ratio <= 0 falsifies the checked "
            "later-block rescue candidate."),
        "predeclared_window": {
            "block_indices_after_discovery": list(BLOCK_INDICES),
            "starts": list(starts),
            "cycle_count_per_block": DISCOVERY_CYCLES,
            "targets_per_cycle": TARGETS_PER_CYCLE,
            "tested_target_count": aggregate["tested_target_count"],
            "prior_sampled_holdout_status": {
                "block_start_window_candidate_status": (
                    suffix_holdout["decision_metrics"][
                        "block_start_window_candidate_status"]),
                "offset_replay_candidate_status": (
                    suffix_holdout["decision_metrics"][
                        "offset_replay_candidate_status"]),
            },
        },
        "upstream_validation": {
            "optimized_row_verifier_validated": (
                row_verifier["decision_metrics"][
                    "optimized_row_verifier_validated"]),
            "row_verifier_validation_target_count": (
                row_verifier["decision_metrics"][
                    "validation_target_count"]),
            "row_verifier_predicate_mismatch_count": (
                row_verifier["decision_metrics"][
                    "predicate_mismatch_count"]),
        },
        "block_summaries": blocks,
        "aggregate": aggregate,
        "decision_metrics": {
            "later_full_block_scan_completed": True,
            "optimized_row_verifier_validated": (
                row_verifier["decision_metrics"][
                    "optimized_row_verifier_validated"]),
            "tested_target_count": aggregate["tested_target_count"],
            "block_count": len(blocks),
            "first_three_tail_count": (
                aggregate["tail_summary"]["row_count"]),
            "active_selector_count": (
                aggregate["tail_summary"]["active_selector_count"]),
            "first_three_tail_full_nonpositive_count": (
                aggregate["tail_summary"]["failure_count"]),
            "predicate_full_nonpositive_count": (
                aggregate["predicate_counts"]["full_nonpositive"]),
            "candidate_status": aggregate["candidate_status"],
            "minimum_rescue_margin": (
                aggregate["tail_summary"]["full_action_ratio_summary"][
                    "minimum"]),
            "minimum_complement_to_required_ratio": (
                aggregate["tail_summary"][
                    "complement_to_required_ratio_summary"]["minimum"]),
            "maximum_identity_error": (
                aggregate["tail_summary"]["maximum_identity_error"]),
            "elapsed_seconds": elapsed,
            "targets_per_second": (
                aggregate["tested_target_count"] / elapsed
                if elapsed else math.inf),
            "goldbach_proved": False,
        },
        "decision": (
            "Read candidate_status. rescued_with_tail_support means the "
            "frozen later-block rescue candidate survived this finite "
            "predeclared scan with actual tail support. "
            "support_starved_no_first_three_tail_rows means the test still "
            "did not encounter the relevant tail class. "
            "falsified_by_nonpositive_tail_rows means the candidate failed "
            "on the recorded rows."),
        "next_obligation": (
            "Convert any surviving finite pattern into a non-circular "
            "complement-rescue or signed prime-pair correlation estimate, "
            "or use recorded failures/support-starvation to choose the next "
            "predeclared arithmetic split."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
