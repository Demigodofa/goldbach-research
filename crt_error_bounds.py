"""Rigorous elementary CRT bounds for the cubic sieve's central window.

This module separates a density prediction from its worst-case arithmetic
error.  The optional exact comparison is a finite diagnostic, never an input
to the bound.  It does not assert a uniform Goldbach result.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from math import ceil, floor, isqrt
from pathlib import Path

from cubic_sieve import event_masks, exact_floor_cuberoot
from redistribution import sieve


def odd_multiples(lo: int, hi: int, factor: int) -> int:
    """Count odd multiples of a positive odd factor in an integer interval."""
    if any(type(value) is not int for value in (lo, hi, factor)):
        raise ValueError("exact integers required")
    if lo < 1 or factor < 1 or factor % 2 == 0:
        raise ValueError("positive interval and positive odd factor required")
    if hi < lo:
        return 0
    return (hi // factor + 1) // 2 - ((lo - 1) // factor + 1) // 2


def central_crt_bound(target: int, compare_exact: bool = False) -> dict:
    """Return a proven finite lower bound without per-candidate enumeration.

    There are rho_p forbidden classes modulo a small odd prime p.  Full CRT
    inclusion-exclusion bounds the discrepancy by E=prod(1+rho_p)-1.  The
    same E applies on a progression of odd multiples of any residual prime.
    Reflection doubles a safe bound on each arm; overlap is deliberately
    overcounted.  compare_exact adds independently computed diagnostic masks.
    """
    if type(target) is not int or target < 6 or target % 2:
        raise ValueError("target must be an even exact integer at least 6")
    high = target - 3
    cutoff = exact_floor_cuberoot(high)
    lo = max(3, cutoff * cutoff)
    lo += 1 - lo % 2
    hi = target - lo
    slots = max(0, (hi - lo) // 2 + 1)
    flags = sieve(isqrt(high))
    primes = [p for p in range(3, len(flags), 2) if flags[p]]
    pre_primes = [p for p in primes if p <= cutoff]
    density = Fraction(1)
    error_plus_one = 1
    for prime in pre_primes:
        rho = 1 if target % prime == 0 else 2
        density *= Fraction(prime - rho, prime)
        error_plus_one *= 1 + rho
    error = error_plus_one - 1
    main = slots * density
    M_lower = max(0, ceil(main - error))
    branches = []
    for prime in primes:
        if prime <= cutoff or prime * prime > hi:
            continue
        raw = odd_multiples(max(lo, prime * prime), hi, prime)
        if not raw:
            continue
        arm_upper = min(raw, floor(raw * density + error))
        branches.append({"prime": prime, "raw_arm_count": raw,
                         "presieved_arm_upper": arm_upper,
                         "event_upper": 2 * arm_upper})
    S1_upper = sum(row["event_upper"] for row in branches)
    raw_lower = M_lower - S1_upper
    result = {
        "target_even": target, "cubic_cutoff": cutoff,
        "candidate_interval": [lo, hi], "odd_candidate_slots": slots,
        "pre_sieve_primes": pre_primes,
        "density_exact": str(density), "density_decimal": float(density),
        "M_main_term_exact": str(main), "M_main_term_decimal": float(main),
        "absolute_CRT_error_bound": error, "M_lower": M_lower,
        "residual_branches": branches, "S1_upper": S1_upper,
        "raw_G_lower": raw_lower, "G_lower": max(0, raw_lower),
        "certifies_positive": raw_lower > 0,
        "scope": "finite rigorous bound; failure is inconclusive; no uniform positivity claim",
    }
    if compare_exact:
        built = event_masks(target)
        clip = (((1 << slots) - 1) << ((lo - 3) // 2)) if slots else 0
        base = clip
        for prime, mask in built["event_masks"].items():
            if prime <= cutoff:
                base &= ~mask
        residual = [mask & base for prime, mask in built["event_masks"].items()
                    if prime > cutoff]
        M = base.bit_count()
        S1 = sum(mask.bit_count() for mask in residual)
        S2 = sum((left & right).bit_count()
                 for i, left in enumerate(residual) for right in residual[i + 1:])
        exact_error = Fraction(M) - main
        result["exact_diagnostic"] = {
            "M": M, "S1": S1, "S2": S2, "G_ordered": M - S1 + S2,
            "raw_union_margin": M - S1,
            "M_error_exact": str(exact_error),
            "M_error_decimal": float(exact_error),
            "M_bound_holds": M_lower <= M,
            "S1_bound_holds": S1 <= S1_upper,
            "absolute_error_bound_holds": abs(exact_error) <= error,
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="+", type=int)
    parser.add_argument("--compare-exact", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    results = [central_crt_bound(n, args.compare_exact) for n in args.targets]
    rendered = json.dumps(results, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
