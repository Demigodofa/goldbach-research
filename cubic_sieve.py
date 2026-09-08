"""Exact finite Goldbach counts by a cubic-cutoff composite sieve.

For one even target, candidate index ``i`` denotes the ordered odd candidate
``a = 3 + 2*i`` and its reflected argument ``N-a``.  This is a finite count
certificate, not a claim that the resulting lower bounds stay positive for
all future targets.
"""
from __future__ import annotations

import argparse
import json
from math import isqrt
from pathlib import Path
import time

from redistribution import sieve


def exact_floor_cuberoot(value: int) -> int:
    """Return the exact integer z with z**3 <= value < (z+1)**3."""
    if type(value) is not int or value < 0:
        raise ValueError("nonnegative exact integer required")
    low, high = 0, 1
    while high * high * high <= value:
        low, high = high, high * 2
    while low + 1 < high:
        middle = (low + high) // 2
        if middle * middle * middle <= value:
            low = middle
        else:
            high = middle
    return low


def _target_shape(target: int) -> tuple[int, int]:
    if type(target) is not int or target < 4 or target % 2:
        raise ValueError("target must be an even exact integer at least 4")
    if target == 4:
        return 1, 1
    return (target - 4) // 2, target - 3


def _mask_from_indices(indices: list[int], slots: int) -> int:
    """Pack bit indices once, avoiding repeated growing-integer ORs."""
    packed = bytearray((slots + 7) // 8)
    for index in indices:
        packed[index >> 3] |= 1 << (index & 7)
    return int.from_bytes(packed, "little")


def event_masks(target: int) -> dict:
    """Build E_r masks for odd prime factors through floor(sqrt(N-3)).

    E_r contains candidate positions where either ordered argument is a
    multiple r*r, r*r+2*r, ... .  Starting at r*r makes r the least possible
    factor represented by that event after smaller factors are excluded.
    """
    slots, high = _target_shape(target)
    if target == 4:
        return {"target_even": target, "M_slots": 1, "H": 1,
                "sqrt_cutoff": 1, "event_masks": {}}
    root = isqrt(high)
    flags = sieve(root)
    masks = {}
    for factor in range(3, root + 1, 2):
        if not flags[factor]:
            continue
        positions = []
        for candidate in range(factor * factor, high + 1, 2 * factor):
            index = (candidate - 3) // 2
            positions.append(index)
            positions.append(slots - 1 - index)
        masks[factor] = _mask_from_indices(positions, slots)
    return {"target_even": target, "M_slots": slots, "H": high,
            "sqrt_cutoff": root, "event_masks": masks}


def cubic_sieve_count(target: int) -> dict:
    """Return the exact finite ordered odd-prime-pair count for ``target``.

    After removing every E_r with r <= floor(cuberoot(H)), any remaining
    composite argument at most H is semiprime.  Its event is its least factor,
    because E_r begins at r*r.  A candidate then lies in at most two residual
    events, one per argument, so pairwise inclusion-exclusion is exact.
    """
    started = time.monotonic()
    built = event_masks(target)
    slots, high = built["M_slots"], built["H"]
    if target == 4:
        return {"method": "finite cubic-cutoff exact sieve", "target_even": 4,
                "candidate_order": "special 2 + 2 base case", "M_slots": 1, "H": 1,
                "cubic_cutoff": 1, "sqrt_cutoff": 1, "pre_sieve_primes": [],
                "residual_primes": [], "pre_sieve_event_count": 0,
                "residual_event_count": 0, "base_slots": 1, "M_after_pre_sieve": 1,
                "S1": 0, "S2": 0,
                "union_bound_raw": 1, "result": 1,
                "intersecting_residual_event_pairs": 0,
                "seconds": round(time.monotonic() - started, 6),
                "scope": "exact finite count; no universal positivity inference"}

    cutoff = exact_floor_cuberoot(high)
    all_mask = (1 << slots) - 1
    masks = built["event_masks"]
    pre_primes = [factor for factor in masks if factor <= cutoff]
    residual_primes = [factor for factor in masks if factor > cutoff]
    pre_union = 0
    for factor in pre_primes:
        pre_union |= masks[factor]
    base = all_mask & ~pre_union
    base_slots = base.bit_count()
    residual_masks = [(factor, masks[factor] & base) for factor in residual_primes]
    S1 = sum(mask.bit_count() for _, mask in residual_masks)
    S2 = 0
    pair_count = 0
    for left, (_, left_mask) in enumerate(residual_masks):
        for _, right_mask in residual_masks[left + 1:]:
            common = (left_mask & right_mask).bit_count()
            S2 += common
            if common:
                pair_count += 1
    result = base_slots - S1 + S2
    return {"method": "finite cubic-cutoff exact sieve", "target_even": target,
            "candidate_order": "ordered a=3,5,...,N-3; i=(a-3)//2; reflected index=M-1-i",
            "M_slots": slots, "H": high, "cubic_cutoff": cutoff,
            "sqrt_cutoff": built["sqrt_cutoff"], "pre_sieve_primes": pre_primes,
            "residual_primes": residual_primes,
            "pre_sieve_event_count": len(pre_primes),
            "residual_event_count": len(residual_primes), "base_slots": base_slots,
            "M_after_pre_sieve": base_slots,
            "S1": S1, "S2": S2,
            "union_bound_raw": base_slots - S1,
            "result": result, "intersecting_residual_event_pairs": pair_count,
            "seconds": round(time.monotonic() - started, 6),
            "scope": "exact finite count; no universal positivity inference"}


def cubic_sieve_block(first: int, count: int) -> dict:
    """Run one finite block and tally its already-computed raw union bounds."""
    if type(first) is not int or first < 4 or first % 2:
        raise ValueError("first must be an even exact integer at least 4")
    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive exact integer")
    started = time.monotonic()
    rows = [cubic_sieve_count(target) for target in range(first, first + 2 * count, 2)]
    return {"method": "finite cubic-cutoff exact sieve block", "first_even": first,
            "last_even": first + 2 * (count - 1), "count": count,
            "nonpositive_union_bounds": sum(row["union_bound_raw"] <= 0 for row in rows),
            "rows": rows, "seconds": round(time.monotonic() - started, 6),
            "scope": "finite measured block; no universal positivity inference"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["target", "block"])
    parser.add_argument("--target", type=int, default=1000)
    parser.add_argument("--first", type=int, default=4)
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = (cubic_sieve_count(args.target) if args.command == "target"
              else cubic_sieve_block(args.first, args.count))
    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
