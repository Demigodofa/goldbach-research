"""Scan fresh q286 active-lane cycles after the coupled-slack failure edge.

The source-summary phase audit found a pass-only suffix after target 647392,
but that suffix was too sparse to become a phase theorem.  This builder uses
the validated prime-indexed row verifier to scan two predeclared full q286
cycles:

* the first full even-target cycle after the largest source-summary failure;
* the first full cycle after the largest source-summary row.

Every active-selector hit is then checked with the frozen component-pair
coupled-slack scalar.  Finite diagnostic only: this proves no active-lane
theorem, pointwise adverse-drag theorem, q286 threshold theorem, strict-central
Goldbach theorem, or Goldbach proof.
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
SOURCE = EVIDENCE / "q286-active-lane-source-summary-coupled-slack-audit.json"
OUT = EVIDENCE / "q286-active-lane-post-failure-cycle-holdout.json"

POST_FAILURE_START = 647394
POST_SOURCE_MAX_START = 955834
TARGETS_PER_CYCLE = 5005
FIRST_TWO_THRESHOLD = -0.2
FIRST_THREE_THRESHOLD = -0.3
CALIBRATION_TARGETS = (14138, 1222142, 1323632, 1379072)
COMPONENT_PAIR = ((5, 7), (7, 11))
TOLERANCE = 1e-9

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    _prime_table,
    q286_first_two_mode_lower_tail_receipt,
    q286_lower_support_component_pair_action_identity_receipt,
    q286_lower_support_component_pair_closure_margin_profile_receipt,
)
from tools.build_q286_prime_indexed_kernel_route_audit import logs  # noqa: E402
from tools.build_q286_prime_indexed_row_filter_order_audit import (  # noqa: E402
    optimized_filter_row,
    prepare_support_context,
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


def compact_selector_row(target, row, window_name):
    first_two = float(row["first_two_modes_to_principal_ratio"])
    first_three = float(row["first_three_modes_to_principal_ratio"])
    full = float(row["full_action_to_principal_ratio"])
    predicates = tuple(row["passed_predicates"])
    return {
        "target": int(target),
        "window_name": window_name,
        "target_mod_286": int(target) % 286,
        "target_mod_143": int(target) % 143,
        "target_mod_13": int(target) % 13,
        "first_two_modes_to_principal_ratio": first_two,
        "first_three_modes_to_principal_ratio": first_three,
        "full_action_to_principal_ratio": full,
        "complement_to_principal_ratio": float(
            row["complement_to_principal_ratio"]),
        "small_support_to_principal_ratio": float(
            row["small_support_to_principal_ratio"]),
        "first_two_active": "first_two_active" in predicates,
        "first_three_tail": "first_three_tail" in predicates,
        "active_selector": (
            "first_two_active" in predicates
            and "first_three_tail" in predicates),
        "passed_predicates": list(predicates),
    }


def scan_window(name, start, context, primes, prime_values, log_values):
    rows = []
    active_rows = []
    tail_rows = []
    minimum_first_two_row = None
    minimum_first_three_row = None
    minimum_full_row = None
    started = time.perf_counter()
    for offset in range(TARGETS_PER_CYCLE):
        target = start + 2 * offset
        compact = compact_selector_row(
            target,
            optimized_filter_row(
                target, context, primes, prime_values, log_values),
            name)
        rows.append(compact)
        if compact["first_three_tail"]:
            tail_rows.append(compact)
        if compact["active_selector"]:
            active_rows.append(compact)
        if (minimum_first_two_row is None
                or compact["first_two_modes_to_principal_ratio"]
                < minimum_first_two_row["first_two_modes_to_principal_ratio"]):
            minimum_first_two_row = compact
        if (minimum_first_three_row is None
                or compact["first_three_modes_to_principal_ratio"]
                < minimum_first_three_row[
                    "first_three_modes_to_principal_ratio"]):
            minimum_first_three_row = compact
        if (minimum_full_row is None
                or compact["full_action_to_principal_ratio"]
                < minimum_full_row["full_action_to_principal_ratio"]):
            minimum_full_row = compact

    return {
        "name": name,
        "start": int(start),
        "end": int(start + 2 * (TARGETS_PER_CYCLE - 1)),
        "scanned_target_count": TARGETS_PER_CYCLE,
        "first_three_tail_count": len(tail_rows),
        "active_selector_count": len(active_rows),
        "active_targets": [row["target"] for row in active_rows],
        "minimum_first_two_row": minimum_first_two_row,
        "minimum_first_three_row": minimum_first_three_row,
        "minimum_full_row": minimum_full_row,
        "first_three_tail_rows": tail_rows[:50],
        "active_rows": active_rows,
        "seconds": time.perf_counter() - started,
    }


def validate_active_rows(active_rows):
    if not active_rows:
        return {
            "validated_target_count": 0,
            "maximum_first_two_delta": 0.0,
            "maximum_first_three_delta": 0.0,
            "maximum_full_delta": 0.0,
            "rows": [],
        }
    targets = tuple(row["target"] for row in active_rows)
    direct = q286_first_two_mode_lower_tail_receipt(
        selected_targets=targets, include_residue_weights=False)
    rows = []
    max_first_two = 0.0
    max_first_three = 0.0
    max_full = 0.0
    active_by_target = {row["target"]: row for row in active_rows}
    for target in targets:
        fast = active_by_target[target]
        exact = direct["rows"][target]
        first_two_delta = abs(
            fast["first_two_modes_to_principal_ratio"]
            - exact["first_two_modes_to_principal_ratio"])
        first_three_delta = abs(
            fast["first_three_modes_to_principal_ratio"]
            - exact["first_three_modes_to_principal_ratio"])
        full_delta = abs(
            fast["full_action_to_principal_ratio"]
            - exact["full_action_to_principal_ratio"])
        max_first_two = max(max_first_two, first_two_delta)
        max_first_three = max(max_first_three, first_three_delta)
        max_full = max(max_full, full_delta)
        rows.append({
            "target": int(target),
            "first_two_delta": first_two_delta,
            "first_three_delta": first_three_delta,
            "full_delta": full_delta,
            "direct_first_two_modes_to_principal_ratio": exact[
                "first_two_modes_to_principal_ratio"],
            "direct_first_three_modes_to_principal_ratio": exact[
                "first_three_modes_to_principal_ratio"],
            "direct_full_action_to_principal_ratio": exact[
                "full_action_to_principal_ratio"],
        })
    return {
        "validated_target_count": len(targets),
        "maximum_first_two_delta": max_first_two,
        "maximum_first_three_delta": max_first_three,
        "maximum_full_delta": max_full,
        "rows": rows,
    }


def closure_rows(active_rows):
    if not active_rows:
        return {
            "calibrated_constants": {},
            "positive_strict_margin_targets": [],
            "nonpositive_strict_margin_targets": [],
            "rows": [],
        }
    targets = tuple(row["target"] for row in active_rows)
    calibration = q286_lower_support_component_pair_closure_margin_profile_receipt(
        targets=CALIBRATION_TARGETS, component_pair=COMPONENT_PAIR,
        tolerance=TOLERANCE)
    constants = {
        "driver_floor": calibration["combined_floor_driver_floor"],
        "channel_bound": calibration[
            "normalized_real_channel_linf_bound"],
        "channel_l1_to_principal": calibration[
            "real_channel_l1_to_principal_mean"],
    }
    identity = q286_lower_support_component_pair_action_identity_receipt(
        targets=targets, component_pair=COMPONENT_PAIR, tolerance=TOLERANCE)
    active_by_target = {row["target"]: row for row in active_rows}
    rows = []
    positive = []
    nonpositive = []
    for target in targets:
        selector_row = active_by_target[target]
        identity_row = identity["rows"][target]
        closure_row = identity_row["source_closure_row"]
        driver = identity_row["combined_floor_driver_to_principal_ratio"]
        max_channel = closure_row["maximum_normalized_real_channel_sum"]
        driver_margin = driver - constants["driver_floor"]
        channel_margin = constants["channel_bound"] - max_channel
        channel_contribution = (
            constants["channel_l1_to_principal"] * channel_margin)
        strict_margin = driver_margin + channel_contribution
        passed = strict_margin > TOLERANCE
        if passed:
            positive.append(target)
        else:
            nonpositive.append(target)
        rows.append({
            **selector_row,
            "combined_floor_driver_to_principal_ratio": driver,
            "maximum_normalized_real_channel_sum": max_channel,
            "driver_margin_to_calibrated_floor": driver_margin,
            "channel_margin_to_calibrated_linf_bound": channel_margin,
            "channel_margin_contribution_to_strict_closure": (
                channel_contribution),
            "strict_closure_margin_to_calibrated_endpoint": strict_margin,
            "strict_closure_margin_positive": passed,
            "positive_by_reconstructed_identity": bool(
                identity_row["positive_by_reconstructed_identity"]),
        })
    return {
        "calibrated_constants": constants,
        "positive_strict_margin_targets": positive,
        "nonpositive_strict_margin_targets": nonpositive,
        "rows": rows,
    }


def build_receipt():
    source = load_json(SOURCE)
    source_targets = {int(row["target"]) for row in source["rows"]}
    starts = {
        "first_full_cycle_after_largest_source_failure": POST_FAILURE_START,
        "first_full_cycle_after_source_summary_maximum": POST_SOURCE_MAX_START,
    }
    maximum_target = max(
        start + 2 * (TARGETS_PER_CYCLE - 1)
        for start in starts.values())
    setup_started = time.perf_counter()
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    context = prepare_support_context()
    setup_seconds = time.perf_counter() - setup_started

    windows = [
        scan_window(name, start, context, primes, prime_values, log_values)
        for name, start in starts.items()
    ]
    active_rows = [
        row for window in windows for row in window["active_rows"]]
    validation = validate_active_rows(active_rows)
    closure = closure_rows(active_rows)
    known_active = [
        row["target"] for row in active_rows
        if row["target"] in source_targets]
    later_new_active = [
        row["target"] for row in active_rows
        if row["target"] not in source_targets]

    return {
        "schema_version": 1,
        "receipt": "q286-active-lane-post-failure-cycle-holdout",
        "generated_from_commit": source_commit(),
        "sources": {
            "source_summary_coupled_slack": str(SOURCE.relative_to(ROOT)),
            "source_summary_commit": source["generated_from_commit"],
            "fast_selector": (
                "tools.build_q286_prime_indexed_row_filter_order_audit."
                "optimized_filter_row"),
            "closure_function": (
                "q286_lower_support_component_pair_action_identity_receipt"),
        },
        "predeclared_windows": {
            "largest_source_summary_failure_target": 647392,
            "largest_source_summary_target": 955832,
            "targets_per_full_q286_cycle": TARGETS_PER_CYCLE,
            "windows": starts,
        },
        "selector": {
            "first_two_modes_to_principal_ratio": (
                f"< {FIRST_TWO_THRESHOLD}"),
            "first_three_modes_to_principal_ratio": (
                f"< {FIRST_THREE_THRESHOLD}"),
        },
        "setup_seconds": setup_seconds,
        "maximum_target": maximum_target,
        "window_summaries": windows,
        "scanned_target_count": sum(
            window["scanned_target_count"] for window in windows),
        "first_three_tail_count": sum(
            window["first_three_tail_count"] for window in windows),
        "active_selector_count": len(active_rows),
        "active_targets": [row["target"] for row in active_rows],
        "active_targets_already_in_source_summary": known_active,
        "active_targets_not_in_source_summary": later_new_active,
        "active_selector_validation": validation,
        "calibration_targets": list(CALIBRATION_TARGETS),
        "component_pair": [list(pair) for pair in COMPONENT_PAIR],
        "calibrated_constants": closure["calibrated_constants"],
        "positive_strict_margin_targets": closure[
            "positive_strict_margin_targets"],
        "nonpositive_strict_margin_targets": closure[
            "nonpositive_strict_margin_targets"],
        "all_active_targets_have_positive_strict_margin": (
            bool(active_rows) and not closure[
                "nonpositive_strict_margin_targets"]),
        "strict_margin_summary": finite_summary(
            row["strict_closure_margin_to_calibrated_endpoint"]
            for row in closure["rows"]),
        "closure_rows": closure["rows"],
        "candidate": {
            "name": "post-failure full-cycle active-lane holdout",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use a full q286 denominator cycle immediately after the "
                "largest source-summary failure, plus a full cycle after the "
                "source-summary maximum, to separate phase evidence from "
                "active-selector rarity."),
            "prediction": (
                "If the phase suffix is real, active rows after 647392 should "
                "not reintroduce nonpositive frozen coupled slack.  If the "
                "later cycle is zero-hit, the evidence points more toward "
                "active-selector rarity than to a robust closure-margin "
                "theorem."),
            "falsifier": (
                "Any active-selector row in either predeclared cycle with "
                "nonpositive strict coupled slack falsifies the finite "
                "post-failure pass candidate."),
            "smallest_test": (
                "Fast-scan the two full cycles, direct-validate every active "
                "hit, and run the frozen component-pair identity only on the "
                "active hits."),
        },
        "decision": (
            "The first full cycle after the largest source-summary failure "
            "contains exactly one active-selector row, target 650476, and it "
            "has positive frozen coupled slack.  The first full cycle after "
            "the source-summary maximum contains zero active-selector rows.  "
            "This gives no fresh nonpositive strict-slack falsifier, but the "
            "genuinely later cycle is support-starved, so the result supports "
            "active-selector rarity as the next theorem obligation more than "
            "a phase-transition closure theorem."),
        "status_boundary": (
            "Finite predeclared cycle audit only.  Target 650476 was already "
            "present in the source-summary suffix; the later full cycle adds "
            "zero-hit denominator evidence, not a new strict-slack row.  This "
            "proves no phase transition theorem, active-lane theorem, "
            "pointwise adverse-drag theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof."),
        "goldbach_proved": False,
        "phase_transition_theorem_proved": False,
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
