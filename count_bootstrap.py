"""Bootstrap finite ordered Goldbach-count prefixes from the canonical G(6)=1.

The algebraic reconstruction identifies prior odd prime flags only when its
input is already a correct Goldbach-count prefix.  Given that inductive input,
an endpoint ``T`` is safe from a prior endpoint ``B`` when
``T <= (B - 1)**2 + 1``: every composite at most ``T-3`` then has a known
least prime divisor.  This module performs that finite composition without a
primality oracle or an ordinary sieve builder.
"""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from math import isqrt

from count_reconstruction import recover_binary_flags
from packed_goldbach import positive_digit_mask


def _sha_values(values: list[int]) -> str:
    return hashlib.sha256(",".join(str(value) for value in values).encode("ascii")).hexdigest()


def _exact_even(value: object, name: str, *, minimum: int = 6) -> int:
    if type(value) is not int or value < minimum or value % 2:
        raise ValueError(f"{name} must be an even exact integer at least {minimum}")
    return value


def _digit_bytes(maximum_coefficient: int) -> int:
    if maximum_coefficient < 1:
        raise RuntimeError("prime polynomial has no odd-prime inputs")
    width = 1
    while (1 << (8 * width - 1)) <= maximum_coefficient:
        width += 1
    return width


def _largest_odd_at_most(value: int) -> int:
    return value if value % 2 else value - 1


def _local_prime_flags(limit: int, recovered_divisors: list[int]) -> bytearray:
    """Sieve through ``limit`` using only the supplied recovered odd primes and 2."""
    flags = bytearray(b"\1") * (limit + 1)
    flags[:2] = b"\0\0"
    if limit >= 2:
        flags[2] = 1
    for even in range(4, limit + 1, 2):
        flags[even] = 0
    for divisor in recovered_divisors:
        if divisor * divisor > limit:
            break
        for composite in range(divisor * divisor, limit + 1, divisor):
            flags[composite] = 0
    return flags


def _pack_odd_prime_polynomial(flags: bytearray, last_odd: int,
                               digit_bytes: int) -> tuple[int, list[int]]:
    slots = (last_odd - 3) // 2 + 1
    encoded = bytearray(slots * digit_bytes)
    primes = []
    for odd in range(3, last_odd + 1, 2):
        if flags[odd]:
            encoded[((odd - 3) // 2) * digit_bytes] = 1
            primes.append(odd)
    return int.from_bytes(encoded, "little"), primes


def _stage(previous_end: int, previous_counts: list[int], target_end: int) -> tuple[list[int], dict]:
    """Compute one safe endpoint and its compact reproducibility receipt."""
    _exact_even(previous_end, "previous endpoint")
    _exact_even(target_end, "target endpoint")
    if target_end <= previous_end:
        raise ValueError("stage endpoints must strictly increase")
    safe_limit = (previous_end - 1) ** 2 + 1
    if target_end > safe_limit:
        raise ValueError(f"target endpoint exceeds safe limit {safe_limit}")
    expected_previous_length = (previous_end - 4) // 2
    if len(previous_counts) != expected_previous_length:
        raise RuntimeError("internal previous count prefix has the wrong length")

    divisor_limit = _largest_odd_at_most(isqrt(target_end - 3))
    needed_count_length = (divisor_limit - 1) // 2
    if needed_count_length > len(previous_counts):
        raise RuntimeError("safe stage did not retain enough recovery input")
    # At the earliest endpoints (8 and 10), no odd divisor can be needed.
    # The reconstruction itself correctly rejects an empty *Goldbach* prefix,
    # so represent this mathematically empty divisor input directly.
    recovered_flags = (recover_binary_flags(previous_counts[:needed_count_length])
                       if needed_count_length else [])
    recovered_divisors = [2 * index + 3 for index, flag in enumerate(recovered_flags)
                          if flag]
    if recovered_divisors != sorted(recovered_divisors) or any(p % 2 == 0 for p in recovered_divisors):
        raise RuntimeError("invalid recovered divisor list")

    last_odd = target_end - 3
    flags = _local_prime_flags(last_odd, recovered_divisors)
    digit_bytes = _digit_bytes(sum(bool(flags[odd]) for odd in range(3, last_odd + 1, 2)))
    polynomial, odd_primes = _pack_odd_prime_polynomial(flags, last_odd, digit_bytes)
    if len(odd_primes) >= (1 << (8 * digit_bytes - 1)):
        raise RuntimeError("prime count violates the borrow-free packed digit bound")
    square = polynomial * polynomial
    target_count = (target_end - 4) // 2
    digit_bits = 8 * digit_bytes
    extracted_byte_length = target_count * digit_bytes
    square_bytes = square.to_bytes((square.bit_length() + 7) // 8, "little")
    extracted_bytes = square_bytes[:extracted_byte_length].ljust(extracted_byte_length, b"\0")
    extracted = int.from_bytes(extracted_bytes, "little")
    positives, all_sentinels = positive_digit_mask(extracted, digit_bits, target_count)
    counts = [int.from_bytes(extracted_bytes[index * digit_bytes:(index + 1) * digit_bytes],
                             "little")
              for index in range(target_count)]
    if any(count >= (1 << (digit_bits - 1)) for count in counts):
        raise RuntimeError("packed count exceeds its borrow-free bound")
    if counts[:expected_previous_length] != previous_counts:
        raise RuntimeError("newly computed count prefix does not preserve prior counts")
    zero_sentinels = all_sentinels ^ positives
    zero_targets = []
    while zero_sentinels:
        lowest = zero_sentinels & -zero_sentinels
        index = (lowest.bit_length() - 1) // digit_bits
        zero_targets.append(6 + 2 * index)
        zero_sentinels ^= lowest

    receipt = {
        "schema": 1,
        "method": "recovered-divisor local sieve then packed odd-prime square",
        "previous_end": previous_end,
        "target_end": target_end,
        "safe_target_limit": safe_limit,
        "previous_counts_sha256": _sha_values(previous_counts),
        "recovered_count_prefix_length": needed_count_length,
        "recovered_largest_odd": divisor_limit,
        "recovered_divisor_prime_count": len(recovered_divisors),
        "recovered_divisor_prime_sha256": _sha_values(recovered_divisors),
        "odd_prime_input_count": len(odd_primes),
        "odd_prime_input_sha256": _sha_values(odd_primes),
        "digit_bytes": digit_bytes,
        "counts_sha256": _sha_values(counts),
        "newly_generated_even_count": target_count - expected_previous_length,
        "positive_target_count": positives.bit_count(),
        "all_targets_positive": positives == all_sentinels,
        "zero_targets": zero_targets,
        "scope": ("exact finite bootstrap computation conditional on every prior count prefix "
                  "having its Goldbach-count meaning; no unbounded positivity or speed claim"),
    }
    return counts, receipt


def _validate_stage_ends(stage_ends: object) -> list[int]:
    if not isinstance(stage_ends, list) or not stage_ends:
        raise ValueError("stage ends must be a nonempty list")
    result = []
    previous = 6
    for index, endpoint in enumerate(stage_ends):
        _exact_even(endpoint, f"stage endpoint {index}")
        if endpoint <= previous:
            raise ValueError("stage endpoints must strictly increase from the canonical base")
        if endpoint > (previous - 1) ** 2 + 1:
            raise ValueError("stage endpoint exceeds its prior safe limit")
        result.append(endpoint)
        previous = endpoint
    return result


def build_chain(stage_ends: list[int]) -> dict:
    """Build a canonical chain beginning only from exact base count G(6)=1."""
    endpoints = _validate_stage_ends(stage_ends)
    current_end = 6
    counts = [1]
    receipts = []
    for endpoint in endpoints:
        counts, receipt = _stage(current_end, counts, endpoint)
        receipts.append(receipt)
        current_end = endpoint
    return {
        "schema": 1,
        "method": "canonical Goldbach-count bootstrap from G(6)=1",
        "canonical_base": {"first_even": 6, "ordered_counts": [1]},
        "stage_ends": endpoints,
        "final_end": current_end,
        "ordered_counts": counts,
        "internal_state": {"count_prefix_first_even": 6,
                           "count_prefix_last_even": current_end,
                           "count_prefix_length": len(counts)},
        "stage_receipts": receipts,
        "scope": ("formal finite composition only; reconstructed flags have prime meaning only "
                  "because each prior exact count prefix is generated by this canonical chain; "
                  "no unbounded positivity or speed claim"),
    }


def replay_chain(record: dict) -> bool:
    """Rebuild only from the canonical base and reject any serialized alteration."""
    if type(record) is not dict or "stage_ends" not in record:
        raise ValueError("canonical chain record required")
    endpoints = _validate_stage_ends(record["stage_ends"])
    expected = build_chain(endpoints)
    if json.dumps(record, sort_keys=True, separators=(",", ":")) != json.dumps(expected, sort_keys=True, separators=(",", ":")):
        raise ValueError("chain record does not match a fresh canonical replay")
    return True


def compact_receipt(chain: dict) -> dict:
    """Return the complete replay data except the bulk ordered-count prefix."""
    if type(chain) is not dict:
        raise ValueError("canonical chain record required")
    keys = (
        "schema", "method", "canonical_base", "stage_ends", "final_end",
        "internal_state", "stage_receipts", "scope",
    )
    if set(chain) != set(keys) | {"ordered_counts"}:
        raise ValueError("chain has an unexpected compact-receipt structure")
    return {key: deepcopy(chain[key]) for key in keys}


def replay_receipt(receipt: dict) -> bool:
    """Replay a compact receipt from the canonical base, excluding only counts."""
    if type(receipt) is not dict or "stage_ends" not in receipt:
        raise ValueError("compact chain receipt required")
    expected = compact_receipt(build_chain(_validate_stage_ends(receipt["stage_ends"])))
    if json.dumps(receipt, sort_keys=True, separators=(",", ":")) != json.dumps(
            expected, sort_keys=True, separators=(",", ":")):
        raise ValueError("compact receipt does not match a fresh canonical replay")
    return True
