"""Exact finite experiments for Goldbach redistribution; no universal inference.

Standard-library only. Exhaustive sieve results use bounded integers.
Tiny self-checks use independent trial division.
"""
from __future__ import annotations

import argparse
from bisect import bisect_left
from datetime import datetime, timezone
from math import gcd, isqrt
import json
import time


def trial_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def sieve(limit: int) -> bytearray:
    if limit < 0:
        raise ValueError("negative sieve limit")
    flags = bytearray(b"\1") * (limit + 1)
    flags[:min(2, limit + 1)] = b"\0" * min(2, limit + 1)
    for p in range(2, isqrt(limit) + 1):
        if flags[p]:
            flags[p*p:limit+1:p] = b"\0" * ((limit-p*p)//p + 1)
    return flags


def goldbach_left(n: int, primes: list[int], flags: bytearray) -> list[int]:
    """Smaller member of each unordered representation, including equal primes."""
    return [p for p in primes[:bisect_left(primes, n//2 + 1)] if flags[n-p]]


def shift_cost(k: int, metric: str) -> int:
    return abs(k) if metric == "asymmetric" else max(abs(k), abs(1-k))


def min_shift(p: int, target_members: list[int], metric: str = "asymmetric") -> tuple[int, int]:
    """Minimize the selected cost, then k; target first member is p+2k."""
    if not target_members:
        raise ValueError("target even integer has no prime pair in exact sieve")
    pos = bisect_left(target_members, p)
    nearby = target_members[max(0, pos-1):pos+1]
    shifts = [(x-p)//2 for x in nearby]
    return min((shift_cost(k, metric), k) for k in shifts)


def scan(limit: int, metric: str = "asymmetric") -> dict:
    start = time.monotonic()
    flags = sieve(limit + 2)
    primes = [i for i, flag in enumerate(flags) if flag]
    records = []
    global_records = []
    total_pairs = 0
    worst_radius = -1
    worst_global = -1
    direct_failures = []
    for n in range(6, limit + 1, 2):
        left = goldbach_left(n, primes, flags)
        targets = goldbach_left(n+2, primes, flags)
        if not left or not targets:
            raise AssertionError({"n": n, "left": left, "targets": targets})
        ordered_targets = sorted(set(targets + [n+2-r for r in targets]))
        best = None
        direct = False
        for p in left:
            q = n-p
            radius, k = min_shift(p, ordered_targets, metric)
            total_pairs += 1
            if best is None or radius < best[0]:
                best = (radius, p, q, k)
            if flags[p+2] or flags[q+2]:
                direct = True
            if radius > worst_radius:
                worst_radius = radius
                records.append({"n": n, "pair": [p, q], "radius": radius,
                                "k": k, "target": [p+2*k, q+2-2*k]})
        if best[0] > worst_global:
            worst_global = best[0]
            r, p, q, k = best
            global_records.append({"n": n, "radius": r, "pair": [p, q],
                                   "k": k, "target": [p+2*k, q+2-2*k]})
        if not direct and len(direct_failures) < 12:
            direct_failures.append(n)
    return {"experiment": "exact_redistribution_scan", "limit_n": limit,
            "prime_sieve_limit": limit+2, "starting_n": 6,
            "quantifier_local": "each unordered starting pair, oriented p<=q",
            "quantifier_global": "minimum over starting pairs at each n",
            "metric": metric,
            "cost": "abs(k)" if metric == "asymmetric" else "max(abs(k),abs(1-k)); each prime moves at most twice this",
            "checked_starting_pairs": total_pairs,
            "local_radius_records": records,
            "best_pair_radius_records": global_records,
            "first_direct_add_two_failures": direct_failures,
            "elapsed_seconds": round(time.monotonic()-start, 6),
            "completed_utc": datetime.now(timezone.utc).isoformat(),
            "scope": "finite computational evidence only"}


def crt_merge(a: int, m: int, b: int, r: int) -> tuple[int, int]:
    if gcd(m, r) != 1:
        raise ValueError("CRT requires coprime moduli")
    return (a + m * (((b-a)*pow(m, -1, r)) % r)) % (m*r), m*r


def crt_pattern(kmax: int, p: int = 7) -> dict:
    """Design divisibility witnesses; this alone does not prove q is prime."""
    if kmax < 1 or not trial_prime(p) or trial_prime(p+2):
        raise ValueError("need K>=1 and prime p with composite p+2")
    active = [k for k in range(-kmax, kmax+1) if trial_prime(p+2*k)]
    a, modulus, used, constraints = 0, 1, set(), []
    for k in active:
        shift = 2-2*k
        assert shift != 0
        r = 3
        while r in used or not trial_prime(r) or shift % r == 0:
            r += 2
        used.add(r)
        residue = (-shift) % r
        a, modulus = crt_merge(a, modulus, residue, r)
        constraints.append({"k": k, "left": p+2*k, "right_shift": shift,
                            "divisor": r, "q_residue": residue})
    assert gcd(a, modulus) == 1
    return {"p": p, "K": kmax, "q_residue": a, "modulus": modulus,
            "coprime": True, "constraints": constraints,
            "q_strict_lower_bound": max([p] + [c["divisor"]-c["right_shift"]
                                               for c in constraints])}


def global_scan(limit: int, radius: int) -> dict:
    """Find failures of the existence of SOME edge, with symmetric displacement.

    At radius B, allowed k are 1-B,...,B and each prime moves by at most 2B.
    A failure is a failure of this bounded transition, not of Goldbach.
    """
    started = time.monotonic()
    flags = sieve(limit + 2*radius + 2)
    primes = [i for i, f in enumerate(flags) if f and i >= 3]
    allowed = {p: [k for k in range(1-radius, radius+1)
                   if p+2*k >= 2 and p+2*k < len(flags) and flags[p+2*k]]
               for p in primes}
    failures = []
    maximal_witness = {"p": 0}
    for n in range(6, limit+1, 2):
        found = None
        for p in primes:
            if p > n//2:
                break
            q = n-p
            if not flags[q]:
                continue
            for k in allowed[p]:
                other = q+2-2*k
                if other >= 2 and flags[other]:
                    found = (p, q, k)
                    break
            if found:
                break
        if found is None:
            failures.append(n)
        elif found[0] > maximal_witness["p"]:
            p, q, k = found
            maximal_witness = {"n": n, "p": p, "q": q, "k": k,
                               "target": [p+2*k, q+2-2*k]}
    return {"experiment": "some_pair_bounded_transition", "limit_n": limit,
            "symmetric_radius": radius, "maximum_prime_displacement": 2*radius,
            "failure_count": len(failures), "first_failures": failures[:30],
            "last_failure": failures[-1] if failures else None,
            "largest_minimal_starting_p": maximal_witness,
            "elapsed_seconds": round(time.monotonic()-started, 6),
            "scope": "finite evidence, no implication beyond checked range"}


def crt_witness(kmax: int) -> dict:
    pattern = crt_pattern(kmax)
    q = pattern["q_residue"]
    modulus = pattern["modulus"]
    attempts = 0
    while q <= pattern["q_strict_lower_bound"] or not trial_prime(q):
        q += modulus
        attempts += 1
        if attempts > 10000:
            raise RuntimeError("finite search allowance exhausted")
    divisors = {c["k"]: c["divisor"] for c in pattern["constraints"]}
    rows = []
    for k in range(-kmax, kmax+1):
        left, right = 7+2*k, q+2-2*k
        if not trial_prime(left):
            rows.append({"k": k, "left": left, "right": right,
                         "obstruction": "left is not prime"})
        else:
            divisor = divisors[k]
            assert right > divisor and right % divisor == 0
            rows.append({"k": k, "left": left, "right": right,
                         "right_divisor": divisor, "right_cofactor": right//divisor})
    return {"experiment": "CRT_certificate", "K": kmax,
            "starting_pair": [7, q], "n": q+7,
            "q_primality": "exhaustive trial division through integer square root",
            "q_trial_division_bound": isqrt(q), "progression": pattern,
            "steps_to_prime": attempts, "blocked_shifts": rows,
            "scope": "this chosen orientation, every integer k in [-K,K]"}


def self_check() -> dict:
    flags = sieve(10000)
    assert all(bool(flags[n]) == trial_prime(n) for n in range(10001))
    primes = [n for n, f in enumerate(flags) if f]
    assert goldbach_left(38, primes, flags) == [7, 19]
    assert goldbach_left(40, primes, flags) == [3, 11, 17]
    for n in range(6, 502, 2):
        targets = [x for x in range(3, n, 2) if trial_prime(x) and trial_prime(n+2-x)]
        for p in goldbach_left(n, primes, flags):
            for metric in ["asymmetric", "symmetric"]:
                expected = min((shift_cost((x-p)//2, metric), (x-p)//2) for x in targets)
                assert min_shift(p, targets, metric) == expected, (n, p, metric)
    for kmax in [1, 2, 4, 8, 16]:
        pattern = crt_pattern(kmax)
        for c in pattern["constraints"]:
            assert (pattern["q_residue"] + c["right_shift"]) % c["divisor"] == 0
        assert gcd(pattern["q_residue"], pattern["modulus"]) == 1
    return {"sieve_trial_division_inputs": 10001,
            "nearest_shift_checked_through_n": 500,
            "crt_radii_checked": [1, 2, 4, 8, 16], "status": "passed"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["check", "scan", "crt", "global", "witness"])
    parser.add_argument("--limit", type=int, default=20000)
    parser.add_argument("--radius", type=int, default=4)
    parser.add_argument("--metric", choices=["asymmetric", "symmetric"], default="asymmetric")
    args = parser.parse_args()
    result = {"check": lambda: self_check(),
              "scan": lambda: scan(args.limit, args.metric),
              "crt": lambda: crt_pattern(args.radius),
              "witness": lambda: crt_witness(args.radius),
              "global": lambda: global_scan(args.limit, args.radius)}[args.mode]()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
