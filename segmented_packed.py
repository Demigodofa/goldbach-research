"""Finite asymmetric packed Goldbach certificates.

For a fixed even block, use a small odd-prime palette ``A`` and a nearby
segmented-prime interval ``B``.  Their local base-``2**(8*w)`` polynomials
convolve to restricted ordered counts for ``a + b``.  A positive restricted
count is a Goldbach witness; a zero says only that this palette did not find
one.  This is an exact finite computation, never an assertion beyond its
explicit target block.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from math import isqrt
from pathlib import Path

from packed_goldbach import positive_digit_mask
from redistribution import sieve
from stacked_cover import segmented_flags


def _integer(value: object, name: str, *, minimum: int | None = None) -> int:
    if type(value) is not int or (minimum is not None and value < minimum):
        suffix = "" if minimum is None else f" at least {minimum}"
        raise ValueError(f"{name} must be an exact integer{suffix}")
    return value


def _sha_int(value: int) -> str:
    if value < 0:
        raise ValueError("only nonnegative packed integers may be hashed")
    raw = value.to_bytes(max(1, (value.bit_length() + 7) // 8), "little")
    digest = hashlib.sha256()
    digest.update(len(raw).to_bytes(8, "little"))
    digest.update(raw)
    return digest.hexdigest()


def _sha_values(values: list[int]) -> str:
    return hashlib.sha256(",".join(str(value) for value in values).encode("ascii")).hexdigest()


def _pack_positions(length: int, positions: list[int], digit_bytes: int) -> int:
    encoded = bytearray(length * digit_bytes)
    for position in positions:
        encoded[position * digit_bytes] = 1
    return int.from_bytes(encoded, "little")


def _digit_bytes_for(maximum_coefficient: int) -> int:
    """Choose a byte-aligned base whose half is strictly above the count."""
    _integer(maximum_coefficient, "maximum coefficient", minimum=1)
    width = 1
    while (1 << (8 * width - 1)) <= maximum_coefficient:
        width += 1
    return width


def _block_inputs(first_even: int, target_count: int, palette_cap: int) -> dict:
    _integer(first_even, "first even", minimum=6)
    _integer(target_count, "target count", minimum=1)
    _integer(palette_cap, "palette cap", minimum=3)
    if first_even % 2:
        raise ValueError("first even must be even")
    last_even = first_even + 2 * (target_count - 1)
    capped = min(palette_cap, first_even - 3)
    flags = sieve(capped)
    palette = [p for p in range(3, capped + 1, 2) if flags[p]]
    if not palette:
        raise ValueError("palette has no odd primes")
    alpha, beta = palette[0], palette[-1]
    segment_lo, segment_hi = first_even - beta, last_even - alpha
    # Both endpoints are odd and segment_lo is at least 3 by palette clamping.
    if not (segment_lo >= 3 and segment_lo % 2 and segment_hi % 2):
        raise RuntimeError("internal segment endpoint construction failed")
    base_limit = isqrt(segment_hi)
    base_flags = sieve(base_limit)
    base_primes = [p for p in range(2, base_limit + 1) if base_flags[p]]
    segment_flags = segmented_flags(segment_lo, segment_hi, base_primes)
    segment_primes = [n for n in range(segment_lo, segment_hi + 1, 2)
                      if segment_flags[n - segment_lo]]
    palette_slots = (beta - alpha) // 2 + 1
    segment_slots = (segment_hi - segment_lo) // 2 + 1
    digit_bytes = _digit_bytes_for(len(palette))
    return {"first_even": first_even, "target_count": target_count,
            "last_even": last_even, "palette_cap": palette_cap,
            "effective_palette_cap": capped, "palette": palette,
            "alpha": alpha, "beta": beta, "segment_lo": segment_lo,
            "segment_hi": segment_hi, "base_limit": base_limit,
            "base_primes": base_primes, "segment_primes": segment_primes,
            "palette_slots": palette_slots, "segment_slots": segment_slots,
            "digit_bytes": digit_bytes, "digit_bits": 8 * digit_bytes}


def certify_block(first_even: int, target_count: int = 1000,
                  palette_cap: int = 1000, *, include_counts: bool = False) -> dict:
    """Produce an independently replayable finite restricted-pair certificate.

    The sentinel mask is the default block decision authority.  Expanding every
    coefficient is a diagnostic option for tests and investigations only.
    """
    if type(include_counts) is not bool:
        raise ValueError("include_counts must be a boolean")
    data = _block_inputs(first_even, target_count, palette_cap)
    alpha, segment_lo = data["alpha"], data["segment_lo"]
    width = data["digit_bytes"]
    palette_positions = [(p - alpha) // 2 for p in data["palette"]]
    segment_positions = [(p - segment_lo) // 2 for p in data["segment_primes"]]
    packed_a = _pack_positions(data["palette_slots"], palette_positions, width)
    packed_b = _pack_positions(data["segment_slots"], segment_positions, width)
    if len(data["palette"]) >= (1 << (data["digit_bits"] - 1)):
        raise RuntimeError("palette size violates the borrow-free convolution bound")
    product = packed_a * packed_b
    start_coefficient = (first_even - alpha - segment_lo) // 2
    mask = (1 << (data["digit_bits"] * target_count)) - 1
    extracted = (product >> (data["digit_bits"] * start_coefficient)) & mask
    positives, all_sentinels = positive_digit_mask(extracted, data["digit_bits"], target_count)
    zero_sentinels = all_sentinels ^ positives
    unresolved = []
    while zero_sentinels:
        lowest = zero_sentinels & -zero_sentinels
        digit_index = (lowest.bit_length() - 1) // data["digit_bits"]
        unresolved.append(first_even + 2 * digit_index)
        zero_sentinels ^= lowest
    result = {
        "schema": 1,
        "method": "segmented_asymmetric_packed_prime_convolution",
        "first_even": first_even,
        "target_count": target_count,
        "last_even": data["last_even"],
        "palette_cap": palette_cap,
        "effective_palette_cap": data["effective_palette_cap"],
        "palette_min": data["alpha"], "palette_max": data["beta"],
        "palette_prime_count": len(data["palette"]),
        "palette_prime_sha256": _sha_values(data["palette"]),
        "segment_lo": segment_lo, "segment_hi": data["segment_hi"],
        "segment_prime_count": len(data["segment_primes"]),
        "segment_prime_sha256": _sha_values(data["segment_primes"]),
        "base_prime_limit": data["base_limit"],
        "base_prime_count": len(data["base_primes"]),
        "base_prime_sha256": _sha_values(data["base_primes"]),
        "digit_bytes": width, "digit_bits": data["digit_bits"],
        "start_coefficient": start_coefficient,
        "packed_palette_sha256": _sha_int(packed_a),
        "packed_segment_sha256": _sha_int(packed_b),
        "packed_product_sha256": _sha_int(product),
        "positive_sentinel_sha256": _sha_int(positives),
        "include_counts": include_counts,
        "positive_target_count": positives.bit_count(),
        "unresolved": unresolved,
        "all_positive": not unresolved,
        "scope": ("the borrow-free sentinel mask is the finite block decision authority; "
                  "an unresolved target is a palette miss, not a Goldbach disproof"),
    }
    if include_counts:
        coefficients = [(extracted >> (data["digit_bits"] * index))
                        & ((1 << data["digit_bits"]) - 1)
                        for index in range(target_count)]
        if not all(value < (1 << (data["digit_bits"] - 1)) for value in coefficients):
            raise RuntimeError("packed coefficient exceeded its borrow-free digit bound")
        result["restricted_ordered_counts"] = coefficients
        result["restricted_counts_sha256"] = _sha_values(coefficients)
    return result


_RECEIPT_KEYS = frozenset({
    "schema", "method", "first_even", "target_count", "last_even", "palette_cap",
    "effective_palette_cap", "palette_min", "palette_max", "palette_prime_count",
    "palette_prime_sha256", "segment_lo", "segment_hi", "segment_prime_count",
    "segment_prime_sha256", "base_prime_limit", "base_prime_count", "base_prime_sha256",
    "digit_bytes", "digit_bits", "start_coefficient", "packed_palette_sha256",
    "packed_segment_sha256", "packed_product_sha256", "positive_sentinel_sha256",
    "include_counts", "positive_target_count", "unresolved",
    "all_positive", "scope",
})
_COUNT_DIAGNOSTIC_KEYS = frozenset({"restricted_ordered_counts", "restricted_counts_sha256"})


def replay_certificate(receipt: dict) -> dict:
    """Rebuild and compare every deterministic receipt field; trust no old sieve."""
    if not isinstance(receipt, dict) or type(receipt.get("include_counts")) is not bool:
        raise ValueError("receipt shape or count-diagnostic mode is invalid")
    expected_keys = _RECEIPT_KEYS | (_COUNT_DIAGNOSTIC_KEYS if receipt["include_counts"] else frozenset())
    if set(receipt) != expected_keys:
        raise ValueError("receipt keys are incomplete or unexpected")
    for key in ("schema", "first_even", "target_count", "last_even", "palette_cap",
                "effective_palette_cap", "palette_min", "palette_max", "palette_prime_count",
                "segment_lo", "segment_hi", "segment_prime_count", "base_prime_limit",
                "base_prime_count", "digit_bytes", "digit_bits", "start_coefficient",
                "positive_target_count"):
        _integer(receipt[key], key)
    if receipt["first_even"] < 6 or receipt["first_even"] % 2 or receipt["target_count"] < 1:
        raise ValueError("receipt target parameters are invalid")
    if receipt["palette_cap"] < 3 or type(receipt["all_positive"]) is not bool:
        raise ValueError("receipt palette or status is invalid")
    if not isinstance(receipt["unresolved"], list) or any(type(value) is not int for value in receipt["unresolved"]):
        raise ValueError("receipt unresolved positions are invalid")
    if receipt["include_counts"] and (not isinstance(receipt["restricted_ordered_counts"], list) or
            len(receipt["restricted_ordered_counts"]) != receipt["target_count"] or
            any(type(value) is not int or value < 0 for value in receipt["restricted_ordered_counts"])):
        raise ValueError("receipt count diagnostics are invalid")
    if any(not isinstance(receipt[key], str) for key in expected_keys
           if key.endswith("sha256")) or not isinstance(receipt["scope"], str):
        raise ValueError("receipt hashes or scope are invalid")
    fresh = certify_block(receipt["first_even"], receipt["target_count"], receipt["palette_cap"],
                          include_counts=receipt["include_counts"])
    if fresh != receipt:
        raise ValueError("receipt does not match a fresh exact computation")
    return {"status": "passed", "target_count": fresh["target_count"],
            "positive_target_count": fresh["positive_target_count"],
            "unresolved_count": len(fresh["unresolved"])}


def output_document(first_even: int, target_count: int, palette_cap: int) -> dict:
    """The serializable CLI document; its nested receipt remains replayable."""
    receipt = certify_block(first_even, target_count, palette_cap)
    return {"receipt": receipt, "verification": replay_certificate(receipt)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=6)
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--cap", type=int, default=1000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = output_document(args.first, args.count, args.cap)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
