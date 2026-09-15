"""Audit a prime-indexed kernel route for q286 full-block verification.

The current q286 receipts compute strict-central prime-pair weights by scanning
every integer in the central interval for each target.  This route audit tests
the first safe optimization: precompute primes once, iterate only central
primes, and preserve exact residue-weight sums.  Since the q286 action is
linear in those residue weights, matching the direct residue kernel validates
the arithmetic input needed by a later optimized verifier.

This is a finite route audit only.  It does not itself verify later full
blocks, prove a threshold theorem, or prove Goldbach.
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
OUT = EVIDENCE / "q286-prime-indexed-kernel-route-audit.json"
SUFFIX_HOLDOUT = EVIDENCE / "q286-complement-rescue-suffix-holdout.json"
THRESHOLD_CANDIDATE = (
    EVIDENCE / "q286-complement-rescue-threshold-candidate-audit.json")

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402


MODULI = (286, 10010)
DISCOVERY_TARGETS = (10664, 14138, 24148, 94856)
LATER_STARTS = (490480, 570560, 650640, 730720, 810800, 890880)
LATER_FIRST_101_SAMPLE = tuple(
    target for start in LATER_STARTS for target in (start, start + 100,
                                                    start + 200))
BENCHMARK_TARGETS = tuple(490480 + 2 * index for index in range(101))
TOLERANCE = 1e-7


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def logs(maximum):
    values = np.zeros(maximum + 1, dtype=np.float64)
    if maximum >= 2:
        values[2:] = np.log(np.arange(2, maximum + 1, dtype=np.float64))
    return values


def direct_residue_weights(target, primes, log_values, modulus):
    lower = target // 3
    upper = target - lower
    totals = [0.0 for _ in range(modulus)]
    count = 0
    for prime in range(max(2, lower + 1), min(target, upper)):
        partner = target - prime
        if primes[prime] and primes[partner]:
            weight = float(log_values[prime] * log_values[partner])
            totals[prime % modulus] += weight
            count += 1
    return count, math.fsum(totals), totals


def prime_indexed_residue_weights(
        target, primes, prime_values, log_values, modulus):
    lower = target // 3
    upper = target - lower
    left = int(np.searchsorted(prime_values, max(2, lower + 1), side="left"))
    right = int(np.searchsorted(prime_values, min(target, upper), side="left"))
    central = prime_values[left:right]
    partners = target - central
    if len(central):
        mask = primes[partners]
        central = central[mask]
        partners = partners[mask]
    residues = np.remainder(central, modulus)
    weights = log_values[central] * log_values[partners]
    totals = np.bincount(residues, weights=weights, minlength=modulus)
    return int(len(central)), float(math.fsum(totals.tolist())), totals.tolist()


def compare_rows(targets, primes, prime_values, log_values):
    rows = []
    maximum_abs_delta = 0.0
    maximum_total_delta = 0.0
    maximum_count_delta = 0
    for target in targets:
        for modulus in MODULI:
            direct_count, direct_total, direct_weights = (
                direct_residue_weights(target, primes, log_values, modulus))
            indexed_count, indexed_total, indexed_weights = (
                prime_indexed_residue_weights(
                    target, primes, prime_values, log_values, modulus))
            deltas = [
                abs(left - right)
                for left, right in zip(direct_weights, indexed_weights)
            ]
            max_delta = max(deltas, default=0.0)
            total_delta = abs(direct_total - indexed_total)
            count_delta = abs(direct_count - indexed_count)
            maximum_abs_delta = max(maximum_abs_delta, max_delta)
            maximum_total_delta = max(maximum_total_delta, total_delta)
            maximum_count_delta = max(maximum_count_delta, count_delta)
            rows.append({
                "target": int(target),
                "modulus": int(modulus),
                "ordered_central_prime_pair_count": int(indexed_count),
                "direct_total_weight": direct_total,
                "prime_indexed_total_weight": indexed_total,
                "count_delta": count_delta,
                "total_weight_abs_delta": total_delta,
                "maximum_residue_weight_abs_delta": max_delta,
            })
    return {
        "rows": rows,
        "maximum_count_delta": maximum_count_delta,
        "maximum_total_weight_abs_delta": maximum_total_delta,
        "maximum_residue_weight_abs_delta": maximum_abs_delta,
        "matches_within_tolerance": (
            maximum_count_delta == 0
            and maximum_total_delta <= TOLERANCE
            and maximum_abs_delta <= TOLERANCE),
    }


def benchmark(targets, primes, prime_values, log_values, modulus):
    start = time.perf_counter()
    direct = [
        direct_residue_weights(target, primes, log_values, modulus)
        for target in targets
    ]
    direct_seconds = time.perf_counter() - start
    start = time.perf_counter()
    indexed = [
        prime_indexed_residue_weights(
            target, primes, prime_values, log_values, modulus)
        for target in targets
    ]
    indexed_seconds = time.perf_counter() - start
    max_total_delta = max(
        abs(left[1] - right[1]) for left, right in zip(direct, indexed))
    return {
        "target_count": len(targets),
        "modulus": modulus,
        "first_target": targets[0],
        "last_target": targets[-1],
        "direct_seconds": direct_seconds,
        "prime_indexed_seconds": indexed_seconds,
        "speedup": (
            direct_seconds / indexed_seconds if indexed_seconds else math.inf),
        "maximum_total_weight_abs_delta": max_total_delta,
        "mean_prime_pair_count": (
            math.fsum(row[0] for row in indexed) / len(indexed)),
    }


def main():
    suffix = load_json(SUFFIX_HOLDOUT)
    threshold = load_json(THRESHOLD_CANDIDATE)
    replay_targets = tuple(
        int(row["target"])
        for row in suffix["prior_tail_offset_replay_holdout"]["target_rows"])
    representative_replay_targets = replay_targets[:12]
    validation_targets = tuple(dict.fromkeys(
        DISCOVERY_TARGETS
        + LATER_FIRST_101_SAMPLE
        + representative_replay_targets))
    maximum_target = max(validation_targets + BENCHMARK_TARGETS)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)

    validation = compare_rows(
        validation_targets, primes, prime_values, log_values)
    benchmark_result = benchmark(
        BENCHMARK_TARGETS, primes, prime_values, log_values, 10010)
    full_later_target_count = (
        len(LATER_STARTS)
        * int(threshold["frozen_candidate"]["selected_from_blocks"][-1] + 3)
        if False else 6 * 8 * 5005)
    estimated_indexed_seconds = (
        benchmark_result["prime_indexed_seconds"]
        * full_later_target_count / benchmark_result["target_count"])

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "suffix_sampled_holdout": str(SUFFIX_HOLDOUT.relative_to(ROOT)),
            "threshold_candidate": str(
                THRESHOLD_CANDIDATE.relative_to(ROOT)),
            "prime_table": "lcm_sawtooth_goldbach_transfer._prime_table",
        },
        "status_boundary": (
            "finite kernel-route audit only; validates residue-weight input "
            "equivalence for sampled targets and records the remaining "
            "full-block verifier blocker. It proves no full-block threshold "
            "theorem, signed correlation theorem, pointwise character-sum "
            "theorem, or Goldbach proof."),
        "question": (
            "Can the direct integer scan in the q286 verifier be replaced by "
            "a prime-indexed strict-central residue-weight kernel without "
            "changing the arithmetic inputs?"),
        "mechanism": (
            "Both kernels compute the same sums of log(p)log(N-p) by residue "
            "class for strict-central prime pairs. Since the q286 action and "
            "support decomposition are linear in those residue weights, exact "
            "agreement validates this as a safe first optimization layer."),
        "prediction": (
            "Prime-indexed residue weights should match direct integer-loop "
            "residue weights target-by-target and modulus-by-modulus, while "
            "running faster on later q286 windows."),
        "falsifier": (
            "Any nonzero pair-count delta or residue-weight delta above "
            f"{TOLERANCE} on the validation targets falsifies this optimized "
            "kernel route."),
        "validation_targets": list(validation_targets),
        "validation": validation,
        "benchmark": benchmark_result,
        "full_later_block_projection": {
            "target_count": full_later_target_count,
            "projected_prime_indexed_seconds_from_benchmark": (
                estimated_indexed_seconds),
            "projected_prime_indexed_minutes_from_benchmark": (
                estimated_indexed_seconds / 60.0),
            "projection_boundary": (
                "Linear projection from a 101-target microbenchmark; it is a "
                "routing estimate, not a completed full-block verification."),
        },
        "decision_metrics": {
            "prime_indexed_kernel_validated": (
                validation["matches_within_tolerance"]),
            "validation_target_count": len(validation_targets),
            "validated_moduli": list(MODULI),
            "maximum_count_delta": validation["maximum_count_delta"],
            "maximum_total_weight_abs_delta": (
                validation["maximum_total_weight_abs_delta"]),
            "maximum_residue_weight_abs_delta": (
                validation["maximum_residue_weight_abs_delta"]),
            "benchmark_speedup": benchmark_result["speedup"],
            "benchmark_prime_indexed_seconds": (
                benchmark_result["prime_indexed_seconds"]),
            "projected_full_later_block_minutes": (
                estimated_indexed_seconds / 60.0),
            "full_block_verifier_ready": False,
            "goldbach_proved": False,
        },
        "decision": (
            "The prime-indexed residue kernel is validated if "
            "prime_indexed_kernel_validated is true. It is a safe input "
            "optimization, but it is not yet the full optimized verifier: "
            "later full-block verification still needs this kernel integrated "
            "into the q286 support/mode action or replaced by a true "
            "window-convolution implementation."),
        "next_obligation": (
            "Integrate the validated prime-indexed residue weights into a "
            "drop-in q286 filter-order receipt and validate row-level ratios "
            "against the existing direct receipt before running exhaustive "
            "later full blocks."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
