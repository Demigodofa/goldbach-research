"""Audit q286 positive/negative coefficient-cell landing advantage.

The coefficientwise minorant failed: arbitrary nonnegative residue mass can
land on negative coefficient cells.  The surviving theorem must therefore
control the actual strict-central prime-pair residue mass W_N.

This receipt measures the exact finite landing inequality

    sum W_N(r) c_+(r) > sum W_N(r) c_-(r)

for the full coefficient and for the principal-plus-dominant partial
coefficient.  It also records the signed tail drag relative to the positive
partial margin.

Finite diagnostic only.  It is not a signed prime-correlation theorem, q286
threshold theorem, strict-central Goldbach theorem, or Goldbach proof.
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
OUT = EVIDENCE / "q286-landing-advantage-audit.json"

KNOWN_EXTREMALS = EVIDENCE / "q286-three-support-known-extremals-audit.json"
ACTION_REFERENCE = EVIDENCE / "q286-three-support-action-decomposition.json"

PERIOD = 10010
TOLERANCE = 1e-7
POSITIVE_SUFFIX_START = 90080
POSITIVE_SUFFIX_END = 250238
FRESH_CYCLE_START = 250240
FRESH_CYCLE_END = FRESH_CYCLE_START + 2 * ((PERIOD // 2) - 1)

sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))

from build_q286_three_support_action_decomposition import (  # noqa: E402
    build_components,
    json_ready,
)
from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_prime_indexed_kernel_route_audit import (  # noqa: E402
    logs,
    prime_indexed_residue_weights,
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
    return tuple(range(start, end + 1, 2))


def build_coefficient_vectors():
    built = build_components(TOLERANCE)
    units = tuple(built["units"])
    components = built["components"]
    top_three = tuple(built["top_three_labels"])
    principal = components["principal"]
    dominant = np.zeros(len(units), dtype=np.complex128)
    for label in top_three:
        dominant += components[label]
    full = np.asarray([
        built["coefficient_by_unit"][unit] for unit in units],
        dtype=np.complex128)
    partial = principal + dominant
    tail = full - partial
    principal_mean = complex(built["principal_mean"])
    if principal_mean.real <= TOLERANCE:
        raise AssertionError("expected positive principal mean")
    return {
        "units": units,
        "principal_mean": principal_mean,
        "top_three_support_labels": top_three,
        "full_ratio": np.asarray(
            [value.real / principal_mean.real for value in full],
            dtype=np.float64),
        "partial_ratio": np.asarray(
            [value.real / principal_mean.real for value in partial],
            dtype=np.float64),
        "tail_ratio": np.asarray(
            [value.real / principal_mean.real for value in tail],
            dtype=np.float64),
    }


def landing_stats(coefficient_ratio, weights):
    weights = np.asarray(weights, dtype=np.float64)
    coeff = np.asarray(coefficient_ratio, dtype=np.float64)
    total_weight = float(math.fsum(weights.tolist()))
    positive = float(np.dot(weights, np.maximum(coeff, 0.0)))
    negative = float(np.dot(weights, np.maximum(-coeff, 0.0)))
    signed = positive - negative
    return {
        "positive_cell_weighted_contribution": positive,
        "negative_cell_weighted_drag": negative,
        "signed_contribution": signed,
        "positive_to_negative_drag_ratio": (
            positive / negative if negative > TOLERANCE else None),
        "signed_to_total_pair_weight_ratio": (
            signed / total_weight if total_weight > TOLERANCE else None),
        "negative_drag_to_total_pair_weight_ratio": (
            negative / total_weight if total_weight > TOLERANCE else None),
    }


def classify_target(target, vectors, primes, prime_values, log_values):
    count, total_weight, residue_weights = prime_indexed_residue_weights(
        target, primes, prime_values, log_values, PERIOD)
    weights = np.asarray(
        [residue_weights[unit] for unit in vectors["units"]],
        dtype=np.float64)
    if count <= 0 or total_weight <= TOLERANCE:
        raise ValueError(f"target {target} has no strict-central pairs")
    partial = landing_stats(vectors["partial_ratio"], weights)
    full = landing_stats(vectors["full_ratio"], weights)
    tail = landing_stats(vectors["tail_ratio"], weights)
    partial_signed = partial["signed_contribution"]
    full_signed = full["signed_contribution"]
    tail_signed = tail["signed_contribution"]
    tail_negative_drag = tail["negative_cell_weighted_drag"]
    tail_positive = tail["positive_cell_weighted_contribution"]
    return {
        "target": int(target),
        "target_mod_10010": int(target % PERIOD),
        "target_mod_286": int(target % 286),
        "ordered_central_prime_pair_count": int(count),
        "total_prime_pair_weight": total_weight,
        "partial_landing": partial,
        "full_landing": full,
        "tail_landing": tail,
        "partial_positive": partial_signed > TOLERANCE,
        "full_positive": full_signed > TOLERANCE,
        "tail_sign_change": (
            (partial_signed > TOLERANCE) != (full_signed > TOLERANCE)),
        "negative_tail_kill": (
            partial_signed > TOLERANCE and full_signed <= TOLERANCE),
        "positive_tail_rescue": (
            partial_signed <= TOLERANCE and full_signed > TOLERANCE),
        "tail_signed_to_partial_margin_ratio": (
            tail_signed / partial_signed
            if abs(partial_signed) > TOLERANCE else None),
        "tail_negative_drag_to_partial_plus_tail_positive_ratio": (
            tail_negative_drag / (partial_signed + tail_positive)
            if partial_signed + tail_positive > TOLERANCE else None),
        "tail_control_margin": (
            partial_signed + tail_positive - tail_negative_drag),
        "full_reconstruction_error": abs(
            (partial_signed + tail_signed) - full_signed),
    }


def summarize_rows(name, targets, vectors, primes, prime_values, log_values):
    started = time.perf_counter()
    rows = [
        classify_target(target, vectors, primes, prime_values, log_values)
        for target in targets
    ]
    seconds = time.perf_counter() - started
    return {
        "name": name,
        "start": int(targets[0]),
        "end": int(targets[-1]),
        "target_count": len(rows),
        "seconds": seconds,
        "targets_per_second": len(rows) / seconds if seconds else math.inf,
        "partial_positive_count": sum(row["partial_positive"] for row in rows),
        "full_positive_count": sum(row["full_positive"] for row in rows),
        "tail_sign_change_count": sum(row["tail_sign_change"] for row in rows),
        "negative_tail_kill_count": sum(
            row["negative_tail_kill"] for row in rows),
        "positive_tail_rescue_count": sum(
            row["positive_tail_rescue"] for row in rows),
        "partial_positive_to_negative_drag_ratio_summary": finite_summary(
            row["partial_landing"]["positive_to_negative_drag_ratio"]
            for row in rows
            if row["partial_landing"][
                "positive_to_negative_drag_ratio"] is not None),
        "full_positive_to_negative_drag_ratio_summary": finite_summary(
            row["full_landing"]["positive_to_negative_drag_ratio"]
            for row in rows
            if row["full_landing"][
                "positive_to_negative_drag_ratio"] is not None),
        "tail_negative_drag_to_total_weight_summary": finite_summary(
            row["tail_landing"]["negative_drag_to_total_pair_weight_ratio"]
            for row in rows),
        "tail_control_margin_summary": finite_summary(
            row["tail_control_margin"] for row in rows),
        "tail_negative_drag_to_partial_plus_tail_positive_summary":
            finite_summary(
                row[
                    "tail_negative_drag_to_partial_plus_tail_positive_ratio"]
                for row in rows
                if row[
                    "tail_negative_drag_to_partial_plus_tail_positive_ratio"]
                is not None),
        "maximum_full_reconstruction_error": max(
            row["full_reconstruction_error"] for row in rows),
        "worst_full_landing_rows": sorted(
            rows,
            key=lambda row: (
                row["full_landing"]["signed_to_total_pair_weight_ratio"],
                row["target"]))[:12],
        "worst_partial_landing_rows": sorted(
            rows,
            key=lambda row: (
                row["partial_landing"]["signed_to_total_pair_weight_ratio"],
                row["target"]))[:12],
        "tightest_tail_control_rows": sorted(
            rows,
            key=lambda row: (row["tail_control_margin"], row["target"]))[:12],
        "tail_sign_change_rows": [
            row for row in rows if row["tail_sign_change"]][:50],
    }


def validate_against_action_reference(vectors, primes, prime_values, log_values):
    reference = load_json(ACTION_REFERENCE)
    deltas = []
    for ref in reference["rows"]:
        row = classify_target(
            int(ref["target"]), vectors, primes, prime_values, log_values)
        deltas.append({
            "target": int(ref["target"]),
            "partial_delta": abs(
                row["partial_landing"]["signed_to_total_pair_weight_ratio"]
                - ref["principal_plus_top_three_to_principal_ratio"]),
            "tail_delta": abs(
                row["tail_landing"]["signed_to_total_pair_weight_ratio"]
                - ref["tail_centered_to_principal_ratio"]),
            "full_delta": abs(
                row["full_landing"]["signed_to_total_pair_weight_ratio"]
                - ref["full_action_to_principal_ratio"]),
        })
    return {
        "reference": str(ACTION_REFERENCE.relative_to(ROOT)),
        "target_count": len(deltas),
        "maximum_partial_delta": max(row["partial_delta"] for row in deltas),
        "maximum_tail_delta": max(row["tail_delta"] for row in deltas),
        "maximum_full_delta": max(row["full_delta"] for row in deltas),
        "matches_reference": max(
            max(row["partial_delta"], row["tail_delta"], row["full_delta"])
            for row in deltas) <= TOLERANCE,
    }


def build_receipt():
    known = load_json(KNOWN_EXTREMALS)
    known_targets = tuple(known["target_selection"]["targets"])
    windows = {
        "known_extremals": known_targets,
        "checked_positive_suffix": target_range(
            POSITIVE_SUFFIX_START, POSITIVE_SUFFIX_END),
        "fresh_next_arithmetic_cycle": target_range(
            FRESH_CYCLE_START, FRESH_CYCLE_END),
    }
    vectors = build_coefficient_vectors()
    maximum_target = max(max(targets) for targets in windows.values())
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    validation = validate_against_action_reference(
        vectors, primes, prime_values, log_values)
    summaries = [
        summarize_rows(
            name, targets, vectors, primes, prime_values, log_values)
        for name, targets in windows.items()
    ]
    aggregate = {
        "target_count": sum(row["target_count"] for row in summaries),
        "partial_positive_count": sum(
            row["partial_positive_count"] for row in summaries),
        "full_positive_count": sum(
            row["full_positive_count"] for row in summaries),
        "tail_sign_change_count": sum(
            row["tail_sign_change_count"] for row in summaries),
        "negative_tail_kill_count": sum(
            row["negative_tail_kill_count"] for row in summaries),
        "positive_tail_rescue_count": sum(
            row["positive_tail_rescue_count"] for row in summaries),
        "maximum_full_reconstruction_error": max(
            row["maximum_full_reconstruction_error"] for row in summaries),
    }
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "known_extremals": str(KNOWN_EXTREMALS.relative_to(ROOT)),
            "action_reference": str(ACTION_REFERENCE.relative_to(ROOT)),
            "coefficient_builder":
                "tools/build_q286_three_support_action_decomposition.py",
        },
        "status_boundary": (
            "finite landing-advantage audit only; no signed prime-correlation "
            "theorem, no q286 threshold theorem, no strict-central Goldbach "
            "theorem, and no Goldbach proof"),
        "question": (
            "Do actual strict-central prime-pair weights land with enough "
            "weighted advantage on positive coefficient cells to overcome "
            "negative coefficient drag?"),
        "candidate_theorem": {
            "name": "q286 landing advantage",
            "novelty_label": "new-to-this-task",
            "statement": (
                "For each even residue a mod 10010 and all sufficiently "
                "large N == a, the actual W_N measure satisfies "
                "sum W_N c_+ > sum W_N c_- for the full q286 coefficient, "
                "with the support-tail sub-inequality "
                "tail_negative_drag < partial_margin + tail_positive_mass."),
            "falsifier": (
                "A predeclared later target with full positive/negative "
                "landing ratio <= 1, or a negative-tail kill, falsifies the "
                "finite later-threshold version."),
        },
        "top_three_support_labels": vectors["top_three_support_labels"],
        "windows": summaries,
        "aggregate": aggregate,
        "validation_against_action_reference": validation,
        "decision": (
            "This audit turns the surviving q286 gap into a landing theorem "
            "about actual prime-pair mass on coefficient cells.  Known "
            "extremals include negative-tail kills and full failures; the "
            "post-boundary windows preserve strict landing advantage."),
        "next_obligation": (
            "Seek an analytic source-backed fixed-modulus AP-pair estimate "
            "or a cone constraint strong enough to prove the landing "
            "advantage for actual W_N, not arbitrary nonnegative residue mass."),
        "landing_advantage_measured": True,
        "q286_landing_advantage_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    receipt = build_receipt()
    OUT.write_text(
        json.dumps(json_ready(receipt), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(json.dumps(json_ready({
        "wrote": str(OUT.relative_to(ROOT)),
        "target_count": receipt["aggregate"]["target_count"],
        "full_positive_count": receipt["aggregate"]["full_positive_count"],
        "tail_sign_change_count": (
            receipt["aggregate"]["tail_sign_change_count"]),
        "negative_tail_kill_count": (
            receipt["aggregate"]["negative_tail_kill_count"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }), sort_keys=True))


if __name__ == "__main__":
    main()
