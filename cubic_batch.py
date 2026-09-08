"""Finite cubic raw lower bounds from a smaller, correct Goldbach-count prefix.

Owner: Kevin's research; purpose: test block certificates using earlier counts. For one
cube-root band, square-start survivors A are primes plus semiprimes C=qr with
z<q<=r. The earlier counts recover every required small prime. Coefficientwise,
R=A*A-2*A*C+sum_q C_q*C_q is exactly the first-order bound M-S1. The same-q
correction uses earlier G(N/q). No high-target prime square is computed here.

The low-level function is CONDITIONAL on its input being actual ordered odd
Goldbach counts G(6)..G(B). Binary square-root consistency alone does not prove
that meaning. The canonical wrapper establishes it by replaying build_chain.
The returned raw bounds are not exact G counts: they cannot be passed to
recover_binary_flags or used as the next bootstrap count prefix.
This is finite composition, not an unbounded positivity or speed theorem.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
import hashlib
import json
from math import isqrt
from pathlib import Path
from time import perf_counter

from count_bootstrap import build_chain
from count_reconstruction import recover_binary_flags
from cubic_sieve import exact_floor_cuberoot


def _block_shape(first: int, count: int) -> tuple[int, int, int]:
    if type(first) is not int or first < 6 or first % 2:
        raise ValueError("first must be an even exact integer at least 6")
    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive exact integer")
    last = first + 2 * (count - 1)
    z = exact_floor_cuberoot(first - 3)
    if exact_floor_cuberoot(last - 3) != z:
        raise ValueError("block must stay in one cube-root band for H=N-3")
    return last, last - 3, z


def _pack_binary(flags: bytearray, digit_bytes: int) -> int:
    encoded = bytearray(len(flags) * digit_bytes)
    encoded[::digit_bytes] = flags
    return int.from_bytes(encoded, "little")


def _extract(packed: int, first: int, count: int, digit_bytes: int) -> list[int]:
    """Decode nonnegative coefficients before any signed arithmetic."""
    width = 8 * digit_bytes
    start = (first - 6) // 2
    block = (packed >> (width * start)) & ((1 << (width * count)) - 1)
    raw = block.to_bytes(count * digit_bytes, "little")
    return [int.from_bytes(raw[i:i + digit_bytes], "little")
            for i in range(0, len(raw), digit_bytes)]


def batch_from_counts(ordered_counts: list[int], first: int, count: int) -> dict:
    """Conditional finite bound; input must already have its Goldbach meaning.

    Requires enough recovered odd flags for max(z,floor(H_max/(z+1))),
    and enough earlier counts through floor(last/(z+1)) (even targets only).
    These are conservative sufficient range checks, not minimal requirements.
    """
    started = perf_counter()
    last, high, z = _block_shape(first, count)
    if not isinstance(ordered_counts, list) or not ordered_counts:
        raise ValueError("nonempty ordered count prefix required")
    prefix_end = 2 * len(ordered_counts) + 4
    recovered_last = prefix_end - 3
    factor_limit = max(z, high // (z + 1))
    factor_limit -= 1 - factor_limit % 2  # largest odd at most this limit
    correction_limit = 2 * ((last // (z + 1)) // 2)
    if recovered_last < factor_limit or prefix_end < correction_limit:
        raise ValueError("count prefix is too short for semiprimes or corrections")
    recovered = recover_binary_flags(ordered_counts)
    small_primes = [2 * i + 3 for i, flag in enumerate(recovered) if flag]
    prime_flags = bytearray(recovered_last + 1)
    for p in small_primes:
        prime_flags[p] = 1
    recovery_seconds = perf_counter() - started

    built_at = perf_counter()
    slots = (high - 1) // 2  # odds 3..high, local index (a-3)//2
    survivors = bytearray(b"\1") * slots
    for p in small_primes:
        if p > z:
            break
        offset = (p * p - 3) // 2
        length = len(range(offset, slots, p))
        survivors[offset::p] = b"\0" * length
    composites = bytearray(slots)
    residual_primes = []
    for index, q in enumerate(small_primes):
        if q * q > high:
            break
        if q <= z:
            continue
        residual_primes.append(q)
        stop = bisect_right(small_primes, high // q)
        for r in small_primes[index:stop]:
            composites[(q * r - 3) // 2] = 1
    if any(c and not a for a, c in zip(survivors, composites)):
        raise RuntimeError("recovered semiprimes contradict first-stage survivors")
    construction_seconds = perf_counter() - built_at

    multiplied_at = perf_counter()
    # Every coefficient of these binary products is <=slots; base>slots.
    digit_bytes = max(1, (slots.bit_length() + 7) // 8)
    packed_a = _pack_binary(survivors, digit_bytes)
    packed_c = _pack_binary(composites, digit_bytes)
    m_values = _extract(packed_a * packed_a, first, count, digit_bytes)
    ac_values = _extract(packed_a * packed_c, first, count, digit_bytes)
    convolution_seconds = perf_counter() - multiplied_at

    corrected_at = perf_counter()
    corrections = [0] * count
    correction_terms = 0
    largest_correction_input = 0
    for q in residual_primes:
        # All targets are even, so q|N is equivalent to 2q|N here.
        start = max(2 * q * q, ((first + 2 * q - 1) // (2 * q)) * (2 * q))
        small = small_primes[:bisect_right(small_primes, q - 1)]
        for target in range(start, last + 1, 2 * q):
            t = target // q
            excluded = sum(prime_flags[t - p] for p in small)
            same_q = ordered_counts[(t - 6) // 2] - 2 * excluded
            if same_q < 0:
                raise RuntimeError("negative same-factor correction contradicts the input meaning")
            corrections[(target - first) // 2] += same_q
            correction_terms += 1
            largest_correction_input = max(largest_correction_input, t)
    correction_seconds = perf_counter() - corrected_at
    rows = []
    for i, (m, ac, same) in enumerate(zip(m_values, ac_values, corrections)):
        s1 = 2 * ac - same
        rows.append({"target_even": first + 2 * i, "M": m, "AC": ac,
                     "same_factor": same, "S1": s1, "raw": m - s1})
    minimum = min(rows, key=lambda row: row["raw"])
    return {
        "method": "cubic raw block bound from an earlier ordered count prefix",
        "first_even": first, "last_even": last, "target_count": count,
        "cubic_cutoff": z, "input_prefix_end": prefix_end,
        "input_counts_sha256": hashlib.sha256(
            ",".join(map(str, ordered_counts)).encode("ascii")).hexdigest(),
        "recovered_last_odd": recovered_last, "required_factor_limit": factor_limit,
        "required_correction_limit": correction_limit,
        "largest_correction_input": largest_correction_input,
        "same_factor_terms": correction_terms, "digit_bytes": digit_bytes,
        "survivor_arguments": sum(survivors), "composite_arguments": sum(composites),
        "minimum_row": minimum,
        "nonpositive_targets": [row["target_even"] for row in rows if row["raw"] <= 0],
        "rows": rows,
        "seconds": {"recovery": recovery_seconds, "construction": construction_seconds,
                    "convolution": convolution_seconds, "corrections": correction_seconds,
                    "pipeline_total": perf_counter() - started},
        "input_meaning": "conditional on actual ordered odd Goldbach counts G(6)..G(B)",
        "scope": ("finite raw lower bounds, not exact counts usable as the next bootstrap "
                  "prefix; no unbounded positivity or speed claim"),
    }


def canonical_batch(stage_ends: list[int], first: int, count: int) -> dict:
    """Establish the input meaning from canonical G(6)=1, charging its cost."""
    started = perf_counter()
    chain = build_chain(stage_ends)
    generated = perf_counter() - started
    result = batch_from_counts(chain["ordered_counts"], first, count)
    result["stage_ends"] = stage_ends.copy()
    result["input_meaning"] = "canonical count_bootstrap chain from G(6)=1"
    result["seconds"]["input_generation"] = generated
    result["seconds"]["complete_total"] = perf_counter() - started
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-controls", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = canonical_batch([26, 626, 10000], 1002000, 1000)
    rows = {row["target_even"]: row for row in result.pop("rows")}
    if args.check_controls:
        from cubic_sieve import cubic_sieve_count
        validation_started = perf_counter()
        result["independent_controls"] = []
        for target in sorted({result["first_even"], result["minimum_row"]["target_even"],
                              result["last_even"]}):
            reference = cubic_sieve_count(target)
            row = rows[target]
            if (row["M"], row["S1"], row["raw"]) != (
                    reference["M_after_pre_sieve"], reference["S1"], reference["union_bound_raw"]):
                raise RuntimeError(f"independent event-mask disagreement at {target}")
            result["independent_controls"].append({
                **row, "reference_G": reference["result"],
                "reference_S2": reference["S2"], "reference_seconds": reference["seconds"]})
        result["seconds"]["independent_validation"] = perf_counter() - validation_started
    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
