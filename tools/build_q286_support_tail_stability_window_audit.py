"""Scan later windows for q286 support-tail sign stability.

The signed support-tail control definition says the next theorem must control
the tail term R_N in

    A_N/P_N = 1 + d_N + r_N.

This receipt tests the first finite prediction: after the last known raw q286
failure, negative support-tail kills should not recur in the already checked
positive suffix or in the next predeclared fresh arithmetic cycle.

Finite diagnostic only.  It is not a q286 threshold theorem, signed tail-control
theorem, pointwise prime-correlation theorem, or Goldbach proof.
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
OUT = EVIDENCE / "q286-support-tail-stability-window-audit.json"

ACTION_REFERENCE = EVIDENCE / "q286-three-support-action-decomposition.json"
TAIL_DEFINITION = EVIDENCE / "q286-signed-support-tail-control-definition.json"

PERIOD = 10010
TOLERANCE = 1e-7
POSITIVE_SUFFIX_START = 90080
POSITIVE_SUFFIX_END = 250238
FRESH_CYCLE_START = 250240
FRESH_CYCLE_END = FRESH_CYCLE_START + 2 * ((PERIOD // 2) - 1)
DOMINANT_SUPPORTS = ((11, 13), (7, 11), (5, 7))

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_prime_indexed_kernel_route_audit import logs  # noqa: E402
from tools.build_q286_prime_indexed_row_filter_order_audit import (  # noqa: E402
    SUPPORT_ORDER,
    optimized_reduced_row,
    prepare_support_context,
)


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
        return {
            "count": 0,
            "minimum": None,
            "maximum": None,
            "mean": None,
        }
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def target_range(start, end):
    if start % 2 or end % 2 or end < start:
        raise ValueError("window endpoints must be increasing even integers")
    return tuple(range(start, end + 1, 2))


def classify_target(target, context, primes, prime_values, log_values):
    row = optimized_reduced_row(
        target, context, primes, prime_values, log_values)
    principal = row["principal_contribution"].real
    if abs(principal) <= TOLERANCE:
        raise ValueError(f"near-zero principal contribution for {target}")
    support_rows = row["support_rows"]
    dominant = math.fsum(
        support_rows[support]["actual_contribution"].real
        for support in DOMINANT_SUPPORTS)
    tail = math.fsum(
        support_rows[support]["actual_contribution"].real
        for support in SUPPORT_ORDER
        if support not in DOMINANT_SUPPORTS)
    dominant_ratio = dominant / principal
    tail_ratio = tail / principal
    partial_ratio = 1.0 + dominant_ratio
    full_ratio = row["full_action_to_principal_ratio"]
    rebuilt_ratio = partial_ratio + tail_ratio
    return {
        "target": int(target),
        "target_mod_10010": int(target % PERIOD),
        "target_mod_286": int(target % 286),
        "ordered_central_prime_pair_weight": float(
            row["ordered_central_prime_pair_weight"]),
        "principal_plus_dominant_to_principal_ratio": partial_ratio,
        "dominant_support_to_principal_ratio": dominant_ratio,
        "support_tail_to_principal_ratio": tail_ratio,
        "full_action_to_principal_ratio": full_ratio,
        "full_reconstruction_error": abs(rebuilt_ratio - full_ratio),
        "principal_plus_dominant_positive": partial_ratio > TOLERANCE,
        "full_action_positive": full_ratio > TOLERANCE,
        "tail_sign_change": (
            (partial_ratio > TOLERANCE) != (full_ratio > TOLERANCE)),
        "negative_tail_kill": (
            partial_ratio > TOLERANCE and full_ratio <= TOLERANCE),
        "positive_tail_rescue": (
            partial_ratio <= TOLERANCE and full_ratio > TOLERANCE),
        "negative_tail_erodes_positive_partial": (
            partial_ratio > TOLERANCE and tail_ratio < -TOLERANCE),
        "tail_to_partial_margin_ratio": (
            tail_ratio / partial_ratio
            if abs(partial_ratio) > TOLERANCE else None),
    }


def summarize_window(name, targets, context, primes, prime_values, log_values):
    started = time.perf_counter()
    rows = [
        classify_target(target, context, primes, prime_values, log_values)
        for target in targets
    ]
    seconds = time.perf_counter() - started
    sign_change_rows = [row for row in rows if row["tail_sign_change"]]
    negative_kill_rows = [row for row in rows if row["negative_tail_kill"]]
    positive_rescue_rows = [row for row in rows if row["positive_tail_rescue"]]
    eroded_rows = [
        row for row in rows
        if row["negative_tail_erodes_positive_partial"]]
    return {
        "name": name,
        "start": int(targets[0]),
        "end": int(targets[-1]),
        "target_count": len(rows),
        "seconds": seconds,
        "targets_per_second": len(rows) / seconds if seconds else math.inf,
        "full_action_positive_count": sum(
            row["full_action_positive"] for row in rows),
        "full_action_nonpositive_count": sum(
            not row["full_action_positive"] for row in rows),
        "principal_plus_dominant_positive_count": sum(
            row["principal_plus_dominant_positive"] for row in rows),
        "principal_plus_dominant_nonpositive_count": sum(
            not row["principal_plus_dominant_positive"] for row in rows),
        "tail_sign_change_count": len(sign_change_rows),
        "negative_tail_kill_count": len(negative_kill_rows),
        "positive_tail_rescue_count": len(positive_rescue_rows),
        "negative_tail_erodes_positive_partial_count": len(eroded_rows),
        "principal_plus_dominant_ratio_summary": finite_summary(
            row["principal_plus_dominant_to_principal_ratio"]
            for row in rows),
        "support_tail_ratio_summary": finite_summary(
            row["support_tail_to_principal_ratio"] for row in rows),
        "full_action_ratio_summary": finite_summary(
            row["full_action_to_principal_ratio"] for row in rows),
        "tail_to_partial_margin_ratio_summary": finite_summary(
            row["tail_to_partial_margin_ratio"] for row in rows
            if row["tail_to_partial_margin_ratio"] is not None),
        "maximum_full_reconstruction_error": max(
            row["full_reconstruction_error"] for row in rows),
        "sign_change_rows": sorted(
            sign_change_rows,
            key=lambda row: (row["full_action_to_principal_ratio"],
                             row["target"]))[:50],
        "negative_tail_kill_rows": sorted(
            negative_kill_rows,
            key=lambda row: (row["full_action_to_principal_ratio"],
                             row["target"]))[:50],
        "positive_tail_rescue_rows": sorted(
            positive_rescue_rows,
            key=lambda row: (
                row["principal_plus_dominant_to_principal_ratio"],
                row["target"]))[:50],
        "worst_full_rows": sorted(
            rows,
            key=lambda row: (row["full_action_to_principal_ratio"],
                             row["target"]))[:12],
        "worst_principal_plus_dominant_rows": sorted(
            rows,
            key=lambda row: (
                row["principal_plus_dominant_to_principal_ratio"],
                row["target"]))[:12],
        "most_negative_tail_rows": sorted(
            rows,
            key=lambda row: (
                row["support_tail_to_principal_ratio"], row["target"]))[:12],
    }


def validation_against_action_reference(
        context, primes, prime_values, log_values):
    reference = load_json(ACTION_REFERENCE)
    rows_by_target = {row["target"]: row for row in reference["rows"]}
    deltas = []
    for target, ref in rows_by_target.items():
        row = classify_target(
            target, context, primes, prime_values, log_values)
        deltas.append({
            "target": int(target),
            "dominant_delta": abs(
                row["dominant_support_to_principal_ratio"]
                - ref["top_three_centered_to_principal_ratio"]),
            "tail_delta": abs(
                row["support_tail_to_principal_ratio"]
                - ref["tail_centered_to_principal_ratio"]),
            "full_delta": abs(
                row["full_action_to_principal_ratio"]
                - ref["full_action_to_principal_ratio"]),
        })
    return {
        "reference": str(ACTION_REFERENCE.relative_to(ROOT)),
        "target_count": len(deltas),
        "maximum_dominant_delta": max(
            row["dominant_delta"] for row in deltas),
        "maximum_tail_delta": max(row["tail_delta"] for row in deltas),
        "maximum_full_delta": max(row["full_delta"] for row in deltas),
        "matches_reference": max(
            max(row["dominant_delta"], row["tail_delta"], row["full_delta"])
            for row in deltas) <= TOLERANCE,
    }


def build_receipt():
    windows = {
        "checked_positive_suffix": target_range(
            POSITIVE_SUFFIX_START, POSITIVE_SUFFIX_END),
        "fresh_next_arithmetic_cycle": target_range(
            FRESH_CYCLE_START, FRESH_CYCLE_END),
    }
    reference = load_json(ACTION_REFERENCE)
    reference_targets = tuple(int(row["target"]) for row in reference["rows"])
    maximum_target = max(
        max(targets[-1] for targets in windows.values()),
        max(reference_targets),
    )
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    context = prepare_support_context()
    validation = validation_against_action_reference(
        context, primes, prime_values, log_values)
    window_summaries = [
        summarize_window(
            name, targets, context, primes, prime_values, log_values)
        for name, targets in windows.items()
    ]
    aggregate = {
        "target_count": sum(row["target_count"] for row in window_summaries),
        "tail_sign_change_count": sum(
            row["tail_sign_change_count"] for row in window_summaries),
        "negative_tail_kill_count": sum(
            row["negative_tail_kill_count"] for row in window_summaries),
        "positive_tail_rescue_count": sum(
            row["positive_tail_rescue_count"] for row in window_summaries),
        "full_action_nonpositive_count": sum(
            row["full_action_nonpositive_count"] for row in window_summaries),
        "principal_plus_dominant_nonpositive_count": sum(
            row["principal_plus_dominant_nonpositive_count"]
            for row in window_summaries),
        "maximum_reconstruction_error": max(
            row["maximum_full_reconstruction_error"]
            for row in window_summaries),
    }
    no_later_negative_tail_kills = (
        aggregate["negative_tail_kill_count"] == 0)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "action_reference": str(ACTION_REFERENCE.relative_to(ROOT)),
            "tail_control_definition": (
                str(TAIL_DEFINITION.relative_to(ROOT))),
            "optimized_row_verifier":
                "tools/build_q286_prime_indexed_row_filter_order_audit.py",
        },
        "status_boundary": (
            "finite support-tail stability window audit only; no signed "
            "tail-control theorem, no q286 threshold theorem, no "
            "strict-central Goldbach theorem, and no Goldbach proof"),
        "question": (
            "After the last observed raw q286 failure, do support-tail sign "
            "flips recur, and are they negative kills or positive rescues?"),
        "mechanism": (
            "Use the validated prime-indexed row verifier to split each row "
            "as A_N/P_N=1+d_N+r_N where d_N is the dominant support action "
            "from 286,154,70 and r_N is the support tail from 14,26,130,10,22."),
        "prediction": (
            "If a later tail-stable threshold is plausible, predeclared "
            "post-88346 windows should have zero negative-tail kills; any "
            "remaining sign flips should be positive-tail rescues."),
        "falsifier": (
            "A negative-tail kill in either predeclared later window refutes "
            "this finite tail-stability candidate and keeps R_N in the main "
            "analytic correlation theorem."),
        "windows": window_summaries,
        "aggregate": aggregate,
        "validation_against_action_reference": validation,
        "decision": (
            "The finite later tail-stability candidate survives this audit; "
            "the next theorem may split known boundary failures from a later "
            "tail-control threshold."
            if no_later_negative_tail_kills else
            "The finite later tail-stability candidate is falsified by a "
            "negative-tail kill in a predeclared later window."),
        "candidate_status": (
            "supported_finite_tail_stability_candidate"
            if no_later_negative_tail_kills else
            "falsified_by_later_negative_tail_kill"),
        "next_obligation": (
            "Do not claim a threshold theorem.  Either prove a signed tail "
            "lower-control inequality for all sufficiently large targets, or "
            "freeze a larger later holdout before scanning."),
        "support_tail_stability_window_measured": True,
        "tail_stable_threshold_proved": False,
        "signed_tail_control_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    payload = build_receipt()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(json.dumps({
        "wrote": str(OUT.relative_to(ROOT)),
        "target_count": payload["aggregate"]["target_count"],
        "tail_sign_change_count": (
            payload["aggregate"]["tail_sign_change_count"]),
        "negative_tail_kill_count": (
            payload["aggregate"]["negative_tail_kill_count"]),
        "positive_tail_rescue_count": (
            payload["aggregate"]["positive_tail_rescue_count"]),
        "candidate_status": payload["candidate_status"],
        "goldbach_proved": payload["goldbach_proved"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
