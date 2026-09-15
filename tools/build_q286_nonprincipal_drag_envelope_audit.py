"""Quantify nonprincipal drag against principal-only surplus on q286 tails.

The principal-rescue obstruction audit showed that checked post-discovery
tail rows are full positive, while many discovery failures are principal-
positive rows overturned by nonprincipal drag.  This receipt reruns the same
validated row verifier and measures the sharper inequality

    nonprincipal_drag < principal_only_margin

on every first-three-tail row.

Finite diagnostic only.  It proves no eventual first_three theorem,
nonprincipal drag theorem, signed correlation theorem, pointwise character-sum
theorem, or Goldbach.
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
OUT = EVIDENCE / "q286-nonprincipal-drag-envelope-audit.json"

PRINCIPAL_SOURCE = (
    EVIDENCE / "q286-principal-rescue-obstruction-audit.json")
SUPPORT_SOURCE = EVIDENCE / "q286-mod13-4-support-schedule-audit.json"

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_mod13_4_prospective_descriptor_audit import (  # noqa: E402
    DISCOVERY_CYCLES,
    TARGETS_PER_CYCLE,
)
from tools.build_q286_prime_indexed_kernel_route_audit import logs  # noqa: E402
from tools.build_q286_prime_indexed_row_filter_order_audit import (  # noqa: E402
    load_json,
    prepare_support_context,
)
from tools.build_q286_principal_rescue_obstruction_audit import (  # noqa: E402
    BLOCK_INDICES,
    block_start,
    finite_summary,
    scan_block,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def quantile(sorted_values, q):
    if not sorted_values:
        return None
    position = (len(sorted_values) - 1) * q
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return float(sorted_values[lower])
    fraction = position - lower
    return float(
        sorted_values[lower] * (1.0 - fraction)
        + sorted_values[upper] * fraction)


def enrich_row(row):
    enriched = dict(row)
    margin = float(row["principal_only_margin"])
    drag = float(row["nonprincipal_drag"])
    correction = float(row["nonprincipal_correction"])
    ratio = None
    if margin > 0.0:
        ratio = drag / margin
    enriched["nonprincipal_drag_to_principal_margin_ratio"] = ratio
    enriched["drag_surplus_margin"] = margin - drag
    enriched["positive_nonprincipal_bonus"] = max(0.0, correction)
    enriched["full_from_drag_envelope"] = (
        margin - drag + max(0.0, correction))
    enriched["full_drag_envelope_error"] = abs(
        enriched["full_from_drag_envelope"]
        - float(row["full_action_to_principal_ratio"]))
    enriched["drag_overturns_principal_margin"] = (
        margin > 0.0 and drag >= margin)
    return enriched


def summarize_scope(name, rows):
    enriched = [enrich_row(row) for row in rows]
    ratios = sorted(
        row["nonprincipal_drag_to_principal_margin_ratio"]
        for row in enriched
        if row["nonprincipal_drag_to_principal_margin_ratio"] is not None)
    drag_rows = [
        row for row in enriched if row["nonprincipal_drag"] > 0.0]
    ratio_rows = [
        row for row in enriched
        if row["nonprincipal_drag_to_principal_margin_ratio"] is not None]
    return {
        "name": name,
        "row_count": len(enriched),
        "principal_only_positive_count": sum(
            1 for row in enriched if row["principal_only_margin"] > 0.0),
        "full_nonpositive_count": sum(
            1 for row in enriched if row["full_nonpositive"]),
        "rows_with_nonprincipal_drag_count": len(drag_rows),
        "drag_overturns_principal_margin_count": sum(
            1 for row in enriched
            if row["drag_overturns_principal_margin"]),
        "first_three_below_minus_one_count": sum(
            1 for row in enriched if row["first_three_below_minus_one"]),
        "nonprincipal_drag_summary": finite_summary(
            row["nonprincipal_drag"] for row in enriched),
        "principal_only_margin_summary": finite_summary(
            row["principal_only_margin"] for row in enriched),
        "drag_surplus_margin_summary": finite_summary(
            row["drag_surplus_margin"] for row in enriched),
        "drag_to_margin_ratio_summary": finite_summary(ratios),
        "drag_to_margin_ratio_quantiles": {
            "q50": quantile(ratios, 0.50),
            "q75": quantile(ratios, 0.75),
            "q90": quantile(ratios, 0.90),
            "q95": quantile(ratios, 0.95),
            "q99": quantile(ratios, 0.99),
        },
        "maximum_full_drag_envelope_error": max(
            (row["full_drag_envelope_error"] for row in enriched),
            default=0.0),
        "largest_drag_to_margin_rows": sorted(
            ratio_rows,
            key=lambda row: (
                -(row["nonprincipal_drag_to_principal_margin_ratio"]
                  or -math.inf),
                row["target"]))[:25],
        "tightest_drag_surplus_rows": sorted(
            enriched,
            key=lambda row: (
                row["drag_surplus_margin"], row["target"]))[:25],
    }


def rows_from_blocks(blocks, predicate):
    return [
        row for block in blocks if predicate(block)
        for row in block["tail_rows"]]


def validate_against_principal_source(blocks, principal_source):
    expected = principal_source["decision_metrics"]
    all_rows = rows_from_blocks(blocks, lambda _block: True)
    post_rows = rows_from_blocks(
        blocks, lambda block: block["block_index_after_discovery"] >= 1)
    later_rows = rows_from_blocks(
        blocks, lambda block: block["block_index_after_discovery"] >= 6)
    observed = {
        "tail_row_count": len(all_rows),
        "full_nonpositive_tail_count": sum(
            1 for row in all_rows if row["full_nonpositive"]),
        "first_three_below_minus_one_tail_count": sum(
            1 for row in all_rows
            if row["first_three_below_minus_one"]),
        "post_discovery_tail_count": len(post_rows),
        "post_discovery_full_nonpositive_tail_count": sum(
            1 for row in post_rows if row["full_nonpositive"]),
        "later_principal_only_minimum_margin": min(
            row["principal_only_margin"] for row in later_rows),
    }
    keys = tuple(observed)
    matches = {
        key: observed[key] == expected[key] for key in keys}
    return {
        "observed": observed,
        "expected": {key: expected[key] for key in keys},
        "matches": matches,
        "all_counts_match": all(matches.values()),
    }


def main():
    principal_source = load_json(PRINCIPAL_SOURCE)
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
            f"seconds={block['seconds']:.3f}",
            flush=True)
    elapsed = time.perf_counter() - started

    all_rows = rows_from_blocks(blocks, lambda _block: True)
    discovery_rows = rows_from_blocks(
        blocks, lambda block: block["block_index_after_discovery"] == 0)
    post_rows = rows_from_blocks(
        blocks, lambda block: block["block_index_after_discovery"] >= 1)
    early_post_rows = rows_from_blocks(
        blocks, lambda block: 1 <= block["block_index_after_discovery"] <= 5)
    later_rows = rows_from_blocks(
        blocks, lambda block: block["block_index_after_discovery"] >= 6)

    scope_summaries = {
        "all_blocks_0_to_11": summarize_scope(
            "all_blocks_0_to_11", all_rows),
        "discovery_block_0": summarize_scope(
            "discovery_block_0", discovery_rows),
        "post_discovery_blocks_1_to_11": summarize_scope(
            "post_discovery_blocks_1_to_11", post_rows),
        "post_discovery_blocks_1_to_5": summarize_scope(
            "post_discovery_blocks_1_to_5", early_post_rows),
        "later_blocks_6_to_11": summarize_scope(
            "later_blocks_6_to_11", later_rows),
    }
    validation = validate_against_principal_source(blocks, principal_source)
    post_summary = scope_summaries["post_discovery_blocks_1_to_11"]
    discovery_summary = scope_summaries["discovery_block_0"]

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "principal_rescue_obstruction": str(
                PRINCIPAL_SOURCE.relative_to(ROOT)),
            "support_schedule": str(SUPPORT_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite q286 nonprincipal-drag envelope audit only; reruns "
            "checked blocks with the validated row verifier and proves no "
            "eventual first_three > -1 theorem, nonprincipal drag theorem, "
            "signed correlation theorem, pointwise character-sum theorem, or "
            "Goldbach."),
        "question": (
            "Can the checked post-discovery q286 rescue be restated as the "
            "strict envelope nonprincipal_drag < principal_only_margin on "
            "every first-three-tail row, and where does that envelope fail?"),
        "mechanism": (
            "For every tail row compute drag_to_margin = "
            "max(0,1-complement_to_principal_ratio) / "
            "(1+first_three_modes_to_principal_ratio).  Rows with ratio >= 1 "
            "are exactly principal-positive rows where nonprincipal drag is "
            "large enough to overturn principal-only positivity."),
        "prediction": (
            "The envelope should hold with room on checked post-discovery "
            "rows, while the discovery block should contain ratio >= 1 "
            "overturning witnesses."),
        "falsifier": (
            "Any post-discovery first-three-tail row with "
            "drag_to_margin >= 1 falsifies the checked suffix envelope."),
        "validation": validation,
        "block_summaries": [
            {
                "block_index_after_discovery": (
                    block["block_index_after_discovery"]),
                "start": block["start"],
                "tested_target_count": block["tested_target_count"],
                "seconds": block["seconds"],
                "predicate_counts": block["predicate_counts"],
                "envelope_summary": summarize_scope(
                    f"block_{block['block_index_after_discovery']}",
                    block["tail_rows"]),
            } for block in blocks
        ],
        "scope_summaries": scope_summaries,
        "decision_metrics": {
            "source_counts_match": validation["all_counts_match"],
            "tested_target_count": (
                len(BLOCK_INDICES) * DISCOVERY_CYCLES
                * TARGETS_PER_CYCLE),
            "tail_row_count": len(all_rows),
            "post_discovery_tail_count": len(post_rows),
            "post_discovery_maximum_drag_to_margin_ratio": (
                post_summary["drag_to_margin_ratio_summary"]["maximum"]),
            "post_discovery_drag_to_margin_gap_below_one": (
                1.0
                - post_summary["drag_to_margin_ratio_summary"]["maximum"]),
            "post_discovery_drag_overturn_count": (
                post_summary["drag_overturns_principal_margin_count"]),
            "post_discovery_tightest_drag_surplus_margin": (
                post_summary["drag_surplus_margin_summary"]["minimum"]),
            "later_maximum_drag_to_margin_ratio": (
                scope_summaries["later_blocks_6_to_11"][
                    "drag_to_margin_ratio_summary"]["maximum"]),
            "discovery_drag_overturn_count": (
                discovery_summary[
                    "drag_overturns_principal_margin_count"]),
            "discovery_full_nonpositive_count": (
                discovery_summary["full_nonpositive_count"]),
            "maximum_full_drag_envelope_error": max(
                summary["maximum_full_drag_envelope_error"]
                for summary in scope_summaries.values()),
            "elapsed_seconds": elapsed,
            "goldbach_proved": False,
        },
        "decision": (
            "If post_discovery_drag_overturn_count is zero and the maximum "
            "post-discovery drag_to_margin ratio is below one, the checked "
            "suffix rescue has a sharper finite theorem target: prove "
            "first_three > -1 and nonprincipal_drag/principal_margin < 1. "
            "Discovery rows with ratio >= 1 remain explicit obstructions."),
        "next_obligation": (
            "Seek an arithmetic or Fourier/operator estimate for the ratio "
            "nonprincipal_drag / principal_only_margin on the post-discovery "
            "tail class, or prove that this ratio bound is still equivalent "
            "to a hard signed prime-correlation estimate."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
