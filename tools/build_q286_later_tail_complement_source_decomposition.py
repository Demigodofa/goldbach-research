"""Decompose later q286 complement rescue into support components.

The later full-block scan found 73 first-three-tail rows and zero full failures.
This receipt asks what supplied the rescue: the principal baseline, lower
CRT-support components, q286 local action, q286 modes 4-6, or the q286 residual
tail.

Finite diagnostic only.  This decomposition does not prove an eventual
threshold theorem, signed correlation theorem, pointwise character-sum theorem,
or Goldbach.
"""

from __future__ import annotations

import itertools
import json
import math
import subprocess
import sys
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-later-tail-complement-source-decomposition.json"

LATER_SCAN = EVIDENCE / "q286-prime-indexed-later-full-block-scan.json"
ROW_VERIFIER = EVIDENCE / "q286-prime-indexed-row-filter-order-audit.json"

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_complement_rescue_margin_schedule import (  # noqa: E402
    finite_summary,
)
from tools.build_q286_prime_indexed_kernel_route_audit import logs  # noqa: E402
from tools.build_q286_prime_indexed_row_filter_order_audit import (  # noqa: E402
    SUPPORT_ORDER,
    TOLERANCE,
    load_json,
    optimized_reduced_row,
    prepare_support_context,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def support_key(support):
    return "support_" + "_".join(str(part) for part in support)


def component_summary(component_rows, total_positive_component_mass):
    rows = []
    for key in sorted(component_rows):
        values = tuple(float(value) for value in component_rows[key])
        positives = tuple(value for value in values if value > TOLERANCE)
        negatives = tuple(value for value in values if value < -TOLERANCE)
        positive_sum = math.fsum(positives)
        rows.append({
            "component": key,
            "positive_count": len(positives),
            "negative_count": len(negatives),
            "zero_count": len(values) - len(positives) - len(negatives),
            "minimum": min(values) if values else None,
            "average": math.fsum(values) / len(values) if values else None,
            "maximum": max(values) if values else None,
            "net_sum": math.fsum(values),
            "positive_sum": positive_sum,
            "positive_component_mass_share": (
                positive_sum / total_positive_component_mass
                if total_positive_component_mass else None),
        })
    return sorted(
        rows,
        key=lambda row: (
            -abs(row["net_sum"]), row["component"]))


def target_components(target, context, primes, prime_values, log_values):
    row = optimized_reduced_row(
        target, context, primes, prime_values, log_values)
    principal = float(row["principal_contribution"].real)
    if abs(principal) <= TOLERANCE:
        raise ValueError(f"near-zero principal contribution for {target}")
    support_rows = row["support_rows"]
    q286_support = support_rows[(11, 13)]
    mode_ratios = {
        f"q286_mode_{mode['mode_index']}": (
            float(mode["contribution"].real) / principal)
        for mode in row["q286_mode_rows"]
    }
    support_ratios = {
        support_key(support): (
            float(support_rows[support]["actual_contribution"].real)
            / principal)
        for support in SUPPORT_ORDER if support != (11, 13)
    }
    rescue_components = {
        "principal_baseline": 1.0,
        "q286_local": (
            float(q286_support["local_prediction"].real) / principal),
        "q286_tail_residual": (
            float(q286_support["tail"].real) / principal),
    }
    rescue_components.update({
        key: mode_ratios[key]
        for key in ("q286_mode_4", "q286_mode_5", "q286_mode_6")
    })
    rescue_components.update(support_ratios)
    first_three = math.fsum(
        mode_ratios[f"q286_mode_{index}"] for index in (1, 2, 3))
    complement = math.fsum(rescue_components.values())
    full = first_three + complement
    return {
        "target": int(target),
        "first_three_modes_to_principal_ratio": first_three,
        "complement_to_principal_ratio": complement,
        "full_action_to_principal_ratio": full,
        "rescue_components": rescue_components,
        "deficit_mode_components": {
            key: mode_ratios[key]
            for key in ("q286_mode_1", "q286_mode_2", "q286_mode_3")
        },
        "identity_error": abs(
            full - float(row["full_action_to_principal_ratio"])),
    }


def removal_results(rows, component_keys):
    result = []
    for key in component_keys:
        failures = [
            row for row in rows
            if (row["full_action_to_principal_ratio"]
                - row["rescue_components"][key]) <= TOLERANCE]
        result.append({
            "removed_component": key,
            "failure_count": len(failures),
            "removing_component_makes_any_tail_fail": bool(failures),
            "minimum_margin_after_removal": min(
                (row["full_action_to_principal_ratio"]
                 - row["rescue_components"][key] for row in rows),
                default=None),
            "first_failure_targets": [
                row["target"] for row in sorted(
                    failures,
                    key=lambda item: (
                        item["full_action_to_principal_ratio"]
                        - item["rescue_components"][key],
                        item["target"]))[:12]],
        })
    return sorted(
        result,
        key=lambda row: (
            -row["failure_count"], row["removed_component"]))


def smallest_subset(rows, component_keys, allow_principal=True):
    keys = tuple(
        key for key in component_keys
        if allow_principal or key != "principal_baseline")
    checked = 0
    for size in range(1, len(keys) + 1):
        passing = []
        for subset in itertools.combinations(keys, size):
            checked += 1
            margins = [
                row["first_three_modes_to_principal_ratio"]
                + math.fsum(row["rescue_components"][key] for key in subset)
                for row in rows
            ]
            if all(margin > TOLERANCE for margin in margins):
                passing.append({
                    "components": list(subset),
                    "minimum_margin": min(margins),
                    "average_margin": math.fsum(margins) / len(margins),
                    "maximum_margin": max(margins),
                })
        if passing:
            return {
                "allow_principal": allow_principal,
                "minimum_size": size,
                "checked_subset_count_until_first_pass": checked,
                "passing_subset_count_at_minimum_size": len(passing),
                "best_subsets_by_minimum_margin": sorted(
                    passing,
                    key=lambda item: (
                        -item["minimum_margin"], item["components"]))[:12],
            }
    return {
        "allow_principal": allow_principal,
        "minimum_size": None,
        "checked_subset_count_until_first_pass": checked,
        "passing_subset_count_at_minimum_size": 0,
        "best_subsets_by_minimum_margin": [],
    }


def main():
    later_scan = load_json(LATER_SCAN)
    row_verifier = load_json(ROW_VERIFIER)
    tail_targets = tuple(
        int(row["target"])
        for block in later_scan["block_summaries"]
        for row in block["tail_rows"])
    if not tail_targets:
        raise ValueError("later scan has no tail rows to decompose")

    maximum_target = max(tail_targets)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    context = prepare_support_context()

    started = time.perf_counter()
    target_rows = [
        target_components(
            target, context, primes, prime_values, log_values)
        for target in tail_targets
    ]
    elapsed = time.perf_counter() - started
    component_keys = tuple(sorted(target_rows[0]["rescue_components"]))
    component_values = {
        key: [row["rescue_components"][key] for row in target_rows]
        for key in component_keys
    }
    deficit_values = {
        key: [row["deficit_mode_components"][key] for row in target_rows]
        for key in ("q286_mode_1", "q286_mode_2", "q286_mode_3")
    }
    total_positive_component_mass = math.fsum(
        max(0.0, value)
        for values in component_values.values()
        for value in values)
    principal_only_margins = [
        row["first_three_modes_to_principal_ratio"] + 1.0
        for row in target_rows]
    nonprincipal_margins = [
        row["first_three_modes_to_principal_ratio"]
        + math.fsum(value for key, value in row["rescue_components"].items()
                    if key != "principal_baseline")
        for row in target_rows]

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "later_full_block_scan": str(LATER_SCAN.relative_to(ROOT)),
            "row_verifier": str(ROW_VERIFIER.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite later-tail complement-source diagnostic only; it proves "
            "no eventual threshold theorem, signed correlation theorem, "
            "pointwise character-sum theorem, or Goldbach."),
        "question": (
            "Which arithmetic support components supply the positive "
            "complement rescue on the 73 later full-block q286 tail rows?"),
        "mechanism": (
            "Re-evaluate the 73 later first-three-tail targets with the "
            "validated optimized row action, then split full/principal into "
            "first-three deficit modes plus principal baseline, lower "
            "CRT-support terms, q286 local action, q286 modes 4-6, and q286 "
            "residual tail."),
        "prediction": (
            "If rescue is narrow, a small component subset keeps all 73 rows "
            "positive. If rescue is genuinely distributed, no tiny fixed "
            "subset should pass after principal is excluded."),
        "falsifier": (
            "A component claimed essential is falsified by removal producing "
            "no failing row. A distributed-cone interpretation is weakened "
            "if a one- or two-component fixed subset keeps all tail rows "
            "positive under this finite decomposition."),
        "upstream_validation": {
            "later_candidate_status": (
                later_scan["decision_metrics"]["candidate_status"]),
            "later_tail_count": (
                later_scan["decision_metrics"]["first_three_tail_count"]),
            "optimized_row_verifier_validated": (
                row_verifier["decision_metrics"][
                    "optimized_row_verifier_validated"]),
        },
        "target_count": len(target_rows),
        "target_rows": target_rows,
        "component_summary_rows": component_summary(
            component_values, total_positive_component_mass),
        "deficit_mode_summary_rows": component_summary(
            deficit_values,
            math.fsum(max(0.0, value)
                      for values in deficit_values.values()
                      for value in values)),
        "component_removal_results": removal_results(
            target_rows, component_keys),
        "smallest_rescue_subset": smallest_subset(
            target_rows, component_keys, allow_principal=True),
        "smallest_rescue_subset_without_principal": smallest_subset(
            target_rows, component_keys, allow_principal=False),
        "principal_only_margin_summary": finite_summary(
            principal_only_margins),
        "nonprincipal_only_margin_summary": finite_summary(
            nonprincipal_margins),
        "identity_error_summary": finite_summary(
            row["identity_error"] for row in target_rows),
        "decision_metrics": {
            "target_count": len(target_rows),
            "maximum_identity_error": max(
                row["identity_error"] for row in target_rows),
            "principal_only_keeps_all_tail_rows_positive": all(
                margin > TOLERANCE for margin in principal_only_margins),
            "principal_only_minimum_margin": min(principal_only_margins),
            "nonprincipal_only_keeps_all_tail_rows_positive": all(
                margin > TOLERANCE for margin in nonprincipal_margins),
            "nonprincipal_only_minimum_margin": min(nonprincipal_margins),
            "smallest_subset_size": (
                smallest_subset(
                    target_rows, component_keys,
                    allow_principal=True)["minimum_size"]),
            "smallest_subset_without_principal_size": (
                smallest_subset(
                    target_rows, component_keys,
                    allow_principal=False)["minimum_size"]),
            "elapsed_seconds": elapsed,
            "goldbach_proved": False,
        },
        "decision": (
            "Read the smallest-subset and principal-only metrics. If the "
            "principal baseline alone keeps all later tail rows positive, "
            "the next theorem target is a first-three lower bound plus a "
            "bound on nonprincipal drag, not merely a positive cone over many "
            "lower support channels. If principal-excluded subsets fail or "
            "need many components, the nonprincipal correction still points "
            "toward a signed correlation/cone estimate."),
        "next_obligation": (
            "Formulate the non-circular inequality as either first_three > "
            "-1 plus bounded nonprincipal drag on the later q286 class, or "
            "as a support-component signed correlation estimate if "
            "principal-only margin does not survive stronger holdouts."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
