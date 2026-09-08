"""Exact paired-wheel maximum gaps and the intervals they certify.

Owner/purpose: Kevin's calculation-Z research. A finite modular computation
feeds a proved interval rule; this never extrapolates a bound to larger wheels.
Only stdlib is used. `check` compares with independent enumeration.
"""
from __future__ import annotations

import argparse
from math import gcd, prod
import json
from pathlib import Path
import time

from redistribution import sieve, trial_prime


def rotate(bits: int, offset: int, width: int) -> int:
    offset %= width
    mask = (1 << width)-1
    return ((bits << offset) | (bits >> (width-offset))) & mask


def cyclic_gap(bits: int, width: int) -> tuple[int, int]:
    """Return maximum cyclic distance between set bits and a preceding bit.

    Find zero runs in two periods using intersection doubling, then a binary
    extension. No assumptions about primes enter this bit algorithm.
    """
    if type(width) is not int or width < 1:
        raise ValueError("positive integer width required")
    mask = (1 << width)-1
    if type(bits) is not int or bits <= 0 or bits & ~mask:
        raise ValueError("nonempty bit set within width required")
    zeros = mask ^ bits
    if not zeros:
        return 1, 0
    zeros |= zeros << width
    powers = []
    length, starts = 1, zeros
    while starts:
        powers.append((length, starts))
        starts &= starts >> length
        length *= 2
    best, starts = 0, (1 << (2*width))-1
    for length, pattern in reversed(powers):
        extended = starts & (pattern >> best)
        if extended:
            best += length
            starts = extended
    first_zero = (starts & -starts).bit_length()-1
    return best+1, (first_zero-1) % width


def direct_gap(bits: int, width: int) -> tuple[int, int]:
    points = [i for i in range(width) if bits >> i & 1]
    if not points:
        raise ValueError("empty circle")
    pairs = [(points[(i+1) % len(points)]-a, a)
             for i, a in enumerate(points)]
    pairs[-1] = (pairs[-1][0]+width, pairs[-1][1])
    return max(pairs)


def prime_prefix(p: int) -> tuple[list[int], int]:
    if type(p) is not int or not trial_prime(p):
        raise ValueError("wheel endpoint must be prime")
    primes = [q for q in range(2, p+1) if trial_prime(q)]
    following = p+1
    while not trial_prime(following):
        following += 1
    return primes, following


def interval_from_gap(p: int, following: int, gap: int) -> dict:
    """All numbers coprime to the wheel in (p,following**2) are prime.

    The reflected intersection of that integer interval with N minus itself
    contains >=gap consecutive integers for the displayed target interval.
    """
    primes, actual_following = prime_prefix(p)
    if type(following) is not int or following != actual_following:
        raise ValueError("following must be the next prime")
    if type(gap) is not int or gap < 1:
        raise ValueError("positive integer gap bound required")
    lower, upper = p+1, following*following-1
    if gap > upper-lower+1:
        return {"status": "inconclusive", "reason": "gap exceeds prime-safe window"}
    first = 2*lower+gap-1
    last = 2*upper-gap+1
    first += first % 2
    last -= last % 2
    return {"status": "conditional_on_gap_bound", "first_even": first,
            "last_even": last, "count": max(0,(last-first)//2+1),
            "prime_safe_integer_window": [lower,upper]}


def analyze_wheel(p: int) -> dict:
    started = time.monotonic()
    primes, following = prime_prefix(p)
    wheel = prod(primes)
    units = sum(1 << a for a in range(wheel) if gcd(a,wheel)==1)
    largest, witness, distribution = 0, None, {}
    for target in range(0, wheel, 2):
        # Units are invariant under negation; target-A equals target+A.
        candidates = units & rotate(units,target,wheel)
        if not candidates:
            raise ValueError("even-target wheel unexpectedly has no survivor")
        gap, before = cyclic_gap(candidates,wheel)
        distribution[gap] = distribution.get(gap,0)+1
        if gap > largest:
            largest = gap
            witness = {"target_residue": target, "gap_before": before,
                       "gap_after": (before+gap) % wheel}
    # Independent gcd witness for the attained lower bound.
    target, before = witness["target_residue"], witness["gap_before"]
    good = lambda x: gcd(x,wheel)==1 and gcd(target-x,wheel)==1
    if not good(before) or not good(before+largest):
        raise ValueError("invalid gap endpoints")
    if any(good(before+i) for i in range(1,largest)):
        raise ValueError("gap witness contains a survivor")
    interval = interval_from_gap(p,following,largest)
    if interval["status"] == "conditional_on_gap_bound":
        interval["status"] = "certified_by_exhaustive_wheel_gap"
    return {"last_wheel_prime": p, "next_prime": following,
            "wheel": wheel, "unit_count": units.bit_count(),
            "even_target_residues_examined": wheel//2,
            "paired_maximum_gap": largest, "attaining_witness": witness,
            "gap_distribution": dict(sorted(distribution.items())),
            "certified_interval": interval,
            "seconds": round(time.monotonic()-started,4)}


def self_check() -> dict:
    masks = 0
    for width in range(1,13):
        for bits in range(1,1 << width):
            got, before = cyclic_gap(bits,width)
            expected, _ = direct_gap(bits,width)
            if got != expected or not (bits >> before & 1):
                raise ValueError("cyclic gap mismatch")
            if not (bits >> ((before+got) % width) & 1):
                raise ValueError("gap endpoint mismatch")
            if any(bits >> ((before+i) % width) & 1 for i in range(1,got)):
                raise ValueError("gap interior mismatch")
            masks += 1
    patterns = 0
    for wheel in [2,6,30,210]:
        units = sum(1 << a for a in range(wheel) if gcd(a,wheel)==1)
        for target in range(0,wheel,2):
            fast = units & rotate(units,target,wheel)
            exact = sum(1 << a for a in range(wheel)
                        if gcd(a,wheel)==1 and gcd(target-a,wheel)==1)
            if fast != exact:
                raise ValueError("reflected wheel mismatch")
            patterns += 1
    # Independent Goldbach enumeration tests consequences, not the derivation.
    targets = 0
    for p in [2,3,5,7,11,13]:
        row = analyze_wheel(p)
        z = row["certified_interval"]
        flags = sieve(z["last_even"])
        for target in range(z["first_even"],z["last_even"]+1,2):
            if not any(flags[a] and flags[target-a]
                       for a in range(2,target//2+1)):
                raise ValueError("invalid Goldbach interval consequence")
            targets += 1
    return {"arbitrary_nonempty_cyclic_masks": masks,
            "direct_reflected_gcd_patterns": patterns,
            "independent_interval_target_checks": targets, "status": "passed"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=["check","table"])
    parser.add_argument("--last-prime",type=int,default=13)
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    if args.command == "check":
        result = self_check()
    else:
        if args.last_prime > 13:
            parser.error("bounded experiment supports wheel primes through13")
        primes, _ = prime_prefix(args.last_prime)
        result = {"method": "all-phase paired-wheel gap to prime-safe intervals",
                  "scope": "finite computed wheels only; no uncomputed gap bound assumed",
                  "rows": [analyze_wheel(p) for p in primes]}
    rendered = json.dumps(result,indent=2)
    if args.output:
        args.output.write_text(rendered+"\n",encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
