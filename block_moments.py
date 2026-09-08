"""Finite block positivity certificates from two exact aggregate moments.

Positive weights depend only on the target's factorization. Their use does
not assume the Hardy-Littlewood conjecture. A serialized certificate must
be replayed from fresh prime inputs before it is accepted as evidence.
"""
from __future__ import annotations

import hashlib
import json

from packed_goldbach import build_prime_square


def _positive_int(value: object, name: str) -> None:
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive exact integer")


def positive_count_bound(count: int, total: int, square_total: int) -> int:
    """Cauchy lower bound given actual moments of nonnegative quantities."""
    _positive_int(count, "count")
    if any(type(x) is not int or x < 0 for x in [total, square_total]):
        raise ValueError("moments must be nonnegative exact integers")
    if total == 0 or square_total == 0:
        if total != 0 or square_total != 0:
            raise ValueError("inconsistent zero moments")
        return 0
    if total*total > count*square_total or square_total > total*total:
        raise ValueError("inconsistent nonnegative moments")
    return (total*total + square_total - 1) // square_total


def sufficient_bounded_moments(count: int, total_lower: int, square_upper: int) -> bool:
    """Use separately proved S>=L>=0 and T<=U; this does not prove the premises."""
    _positive_int(count, "count")
    if any(type(x) is not int or x < 0 for x in [total_lower, square_upper]):
        raise ValueError("moment bounds must be nonnegative exact integers")
    if total_lower*total_lower > count*square_upper:
        raise ValueError("moment bounds cannot enclose any nonnegative input")
    return total_lower*total_lower > (count-1)*square_upper


def target_weight(target: int, mode: str = "singular", bits: int = 32) -> int:
    """Positive integer approximation to the inverse odd singular factor."""
    if type(target) is not int or target < 6 or target % 2:
        raise ValueError("an even exact target >=6 is required")
    if mode not in ("singular", "unit"):
        raise ValueError("unknown weight mode")
    _positive_int(bits, "weight bits")
    if mode == "unit":
        return 1
    remainder = target
    while remainder % 2 == 0:
        remainder //= 2
    numerator = denominator = 1
    divisor = 3
    while divisor*divisor <= remainder:
        if remainder % divisor == 0:
            numerator *= divisor-2
            denominator *= divisor-1
            while remainder % divisor == 0:
                remainder //= divisor
        divisor += 2
    if remainder > 1:
        numerator *= remainder-2
        denominator *= remainder-1
    # Ceiling remains positive even for a singular factor larger than 2**bits.
    return ((1 << bits)*numerator + denominator - 1) // denominator


def _hash_ints(values: list[int]) -> str:
    return hashlib.sha256(",".join(map(str, values)).encode("ascii")).hexdigest()


def make_certificate(first_even: int, count: int = 1000,
                     mode: str = "singular", bits: int = 32) -> dict:
    """Recompute finite prime-pair counts, then certify only through S and T."""
    _positive_int(count, "count")
    target_weight(first_even, mode, bits)  # Validate before allocating.
    last = first_even + 2*(count-1)
    computed = build_prime_square(last)
    digit_bytes = computed.digit_bits // 8
    shift = (first_even//2-1)*computed.digit_bits
    mask = (1 << (count*computed.digit_bits))-1
    packed_counts = (computed.packed_square >> shift) & mask
    encoded = packed_counts.to_bytes(count*digit_bytes, "little")
    counts = [int.from_bytes(encoded[i*digit_bytes:(i+1)*digit_bytes], "little")
              for i in range(count)]
    weights = [target_weight(n, mode, bits) for n in range(first_even, last+1, 2)]
    values = [w*g for w, g in zip(weights, counts)]
    S = sum(values)
    T = sum(x*x for x in values)
    lower = positive_count_bound(count, S, T)
    return {
        "schema": 1,
        "method": "two-moment Cauchy block certificate",
        "first_even": first_even,
        "last_even": last,
        "target_count": count,
        "weight_mode": mode,
        "weight_bits": bits,
        "weight_rule": ("ceil(2^bits*product_{odd prime p|N}(p-2)/(p-1))"
                        if mode == "singular" else "one"),
        "counts_sha256": _hash_ints(counts),
        "weights_sha256": _hash_ints(weights),
        "sum_weighted_counts": S,
        "sum_squared_weighted_counts": T,
        "strict_all_positive_margin": S*S-(count-1)*T,
        "positive_count_lower_bound": lower,
        "all_certified": lower == count,
        "scope": ("exact finite aggregate certificate; a partial count bound does not identify "
                  "which targets are positive; no unbounded positivity or speed claim"),
    }


def replay_certificate(receipt: dict) -> bool:
    """Validate all receipt fields against a fresh canonical computation."""
    if type(receipt) is not dict:
        raise ValueError("certificate object required")
    try:
        expected = make_certificate(receipt["first_even"], receipt["target_count"],
                                    receipt["weight_mode"], receipt["weight_bits"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("invalid certificate parameters") from error
    if json.dumps(receipt, sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("certificate does not match fresh replay")
    return True
