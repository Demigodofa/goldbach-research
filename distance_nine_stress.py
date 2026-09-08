"""Construct exact palette misses with preceding-prime distance fixed at nine.

CRT gives a reduced progression; a separately verified prime in it supplies
a finite witness.  The infinite-existence arguments are in the accompanying
proof note, not inferred from the bounded search here.
"""
from __future__ import annotations

import json
from math import gcd, isqrt

from redistribution import crt_merge, sieve, trial_prime


def _integer(value: int, minimum: int, name: str) -> None:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an exact integer at least {minimum}")


def build_pattern(palette_cap: int) -> dict:
    """Return finite divisibility constraints with coprime CRT residue."""
    _integer(palette_cap, 3, "palette cap")
    flags = sieve(palette_cap)
    palette = [p for p in range(3, palette_cap + 1, 2) if flags[p]]
    offsets = sorted({2, 4, 6, 8} | {9 - p for p in palette})
    residue, modulus, used = 1, 2, set()
    constraints = []
    for offset in offsets:
        divisor = 3
        while divisor in used or not trial_prime(divisor) or offset % divisor == 0:
            divisor += 2
        used.add(divisor)
        residue, modulus = crt_merge(residue, modulus, -offset % divisor, divisor)
        constraints.append({"offset": offset, "prime_divisor": divisor})
    minimum_q = max([palette_cap + 1]
                    + [row["prime_divisor"] - row["offset"] + 1 for row in constraints])
    if gcd(residue, modulus) != 1:
        raise RuntimeError("constructed progression is not reduced")
    return {"palette_cap": palette_cap, "blocked_odd_primes": palette,
            "distance_to_preceding_prime": 9, "constraints": constraints,
            "q_residue": residue, "modulus": modulus, "minimum_q": minimum_q,
            "residue_coprime_to_modulus": True}


def verify_witness(pattern: dict, prime_q: int, pair_left: int | None = None) -> dict:
    """Verify all finite primes/divisors, optionally including a real prime pair."""
    if type(pattern) is not dict or "palette_cap" not in pattern:
        raise ValueError("pattern object required")
    expected = build_pattern(pattern["palette_cap"])
    if json.dumps(pattern, sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("pattern differs from canonical CRT reconstruction")
    _integer(prime_q, 3, "q")
    if (prime_q < pattern["minimum_q"] or
            prime_q % pattern["modulus"] != pattern["q_residue"] or
            not trial_prime(prime_q)):
        raise ValueError("q is not a sufficiently large prime in the progression")
    target = prime_q + 9
    composites = []
    for row in pattern["constraints"]:
        number, divisor = prime_q + row["offset"], row["prime_divisor"]
        if not (1 < divisor < number and number % divisor == 0):
            raise ValueError("proper composite witness failed")
        composites.append({"integer": number, "proper_prime_divisor": divisor,
                           "offset_from_q": row["offset"]})
    pair = None
    if pair_left is not None:
        _integer(pair_left, 2, "pair left")
        if (pair_left > target // 2 or pair_left <= pattern["palette_cap"] or
                not trial_prime(pair_left) or not trial_prime(target - pair_left)):
            raise ValueError("claimed larger-summand prime pair is invalid")
        pair = [pair_left, target - pair_left]
    return {"target_even": target, "preceding_prime": prime_q,
            "distance_to_preceding_prime": 9, "blocked_palette_cap": pattern["palette_cap"],
            "proper_composite_witnesses": composites, "verified_goldbach_pair": pair,
            "scope": "finite palette counterexample; Goldbach represented only if verified pair supplied"}


def find_prime_witness(palette_cap: int, max_candidates: int = 100,
                       maximum_trial_root: int = 5_000_000) -> dict:
    """Bounded search for an exact prime in the already-defined progression."""
    _integer(max_candidates, 1, "max candidates")
    _integer(maximum_trial_root, 1, "maximum trial root")
    pattern = build_pattern(palette_cap)
    residue, modulus, lower = pattern["q_residue"], pattern["modulus"], pattern["minimum_q"]
    first = residue + max(0, (lower - residue + modulus - 1) // modulus) * modulus
    for index in range(max_candidates):
        candidate = first + index * modulus
        if isqrt(candidate) > maximum_trial_root:
            return {"status": "search_limit", "reason": "trial root bound",
                    "pattern": pattern, "tested_candidates": index}
        if trial_prime(candidate):
            return {"status": "found", "pattern": pattern,
                    "tested_candidates": index + 1,
                    "witness": verify_witness(pattern, candidate)}
    return {"status": "search_limit", "reason": "candidate count bound",
            "pattern": pattern, "tested_candidates": max_candidates}
