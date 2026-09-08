"""Exact finite Goldbach block certificates from a packed prime polynomial.

Integer multiplication performs the convolution.  A borrow-free sentinel
subtraction tests all the block's counts together.  Neither operation proves
positivity beyond the explicitly computed finite range.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json

from redistribution import sieve


def _even(value: int, name: str) -> None:
    if type(value) is not int or value < 6 or value % 2:
        raise ValueError(f"{name} must be an even exact integer at least 6")


def _positive(value: int, name: str) -> None:
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive exact integer")


def positive_digit_mask(packed: int, digit_bits: int, count: int) -> tuple[int, int]:
    """Return (positive sentinel bits, all sentinel bits) for one packed block.

    Every input digit must be strictly less than 2**(digit_bits-1).  This
    contract is checked in parallel and is essential to the exact test.
    """
    _positive(digit_bits, "digit_bits")
    _positive(count, "count")
    if digit_bits < 2 or type(packed) is not int or packed < 0:
        raise ValueError("nonnegative packed integer and at least two digit bits required")
    bits = digit_bits * count
    if packed >> bits:
        raise ValueError("packed value extends beyond declared digit count")
    base = 1 << digit_bits
    ones = ((1 << bits) - 1) // (base - 1)
    highs = (base // 2) * ones
    if packed & highs:
        raise ValueError("every coefficient must be strictly below half the base")
    positives = ((packed | highs) - ones) & highs
    return positives, highs


@dataclass(frozen=True)
class PrimeSquare:
    """Internal state from the builder; immutability is not input authentication."""
    last_even: int
    capacity_even: int
    digit_bits: int
    prime_count: int
    packed_prime: int
    packed_square: int


def _pack_primes(flags: bytearray, first_odd: int, last_odd: int,
                 digit_bytes: int) -> tuple[int, int, int]:
    """Pack only the given odd interval, returning polynomial, count, offset."""
    offset = (first_odd - 1) // 2
    slots = (last_odd - first_odd) // 2 + 1
    encoded = bytearray(slots * digit_bytes)
    count = 0
    for odd in range(first_odd, last_odd + 1, 2):
        if flags[odd]:
            encoded[((odd - first_odd) // 2) * digit_bytes] = 1
            count += 1
    return int.from_bytes(encoded, "little"), count, offset


def build_prime_square(last_even: int, capacity_even: int | None = None) -> PrimeSquare:
    """Compute all ordered odd-prime counts through last_even in one square.

    Capacity reserves sufficient digit width for later finite extensions.
    It is not a claim that prime inputs through that capacity were generated.
    """
    _even(last_even, "last_even")
    if capacity_even is None:
        capacity_even = last_even
    _even(capacity_even, "capacity_even")
    if capacity_even < last_even:
        raise ValueError("capacity must include the requested computed range")
    odd_slot_upper = (capacity_even - 4) // 2
    digit_bytes = max(1, (odd_slot_upper.bit_length() + 1 + 7) // 8)
    digit_bits = 8 * digit_bytes
    flags = sieve(last_even - 3)
    local, count, offset = _pack_primes(flags, 3, last_even - 3, digit_bytes)
    packed = local << (digit_bits * offset)
    return PrimeSquare(last_even, capacity_even, digit_bits, count, packed, packed * packed)


def extend_prime_square(previous: PrimeSquare, last_even: int) -> PrimeSquare:
    """Reuse the prior square by C_new=C_old+2*P_old*D+D**2.

    The new-prime polynomial is factored into a short low polynomial and a
    digit shift.  Prime discovery currently uses a fresh finite sieve; only
    the polynomial and its square are reused by this method.
    """
    _even(last_even, "last_even")
    if last_even <= previous.last_even:
        raise ValueError("extension must increase last_even")
    if last_even > previous.capacity_even:
        raise ValueError("extension exceeds reserved capacity; rebuild with a wider base")
    flags = sieve(last_even - 3)
    local, added, offset = _pack_primes(flags, previous.last_even - 1,
                                     last_even - 3, previous.digit_bits // 8)
    shift = offset * previous.digit_bits
    delta = local << shift
    square = (previous.packed_square
              + ((2 * previous.packed_prime * local) << shift)
              + ((local * local) << (2 * shift)))
    return PrimeSquare(last_even, previous.capacity_even, previous.digit_bits,
                       previous.prime_count + added, previous.packed_prime + delta, square)


def certify_block(computed: PrimeSquare, first_even: int, count: int) -> dict:
    """Test trusted builder state; enumerate only unresolved targets, if any.

    A receipt received from outside this builder pipeline must pass
    replay_certificate before being accepted as a certificate.
    """
    _even(first_even, "first_even")
    _positive(count, "count")
    last = first_even + 2 * (count - 1)
    if last > computed.last_even:
        raise ValueError("block extends beyond the computed prime range")
    width = computed.digit_bits
    start_index = first_even // 2 - 1
    extracted = ((computed.packed_square >> (width * start_index))
                 & ((1 << (width * count)) - 1))
    positives, highs = positive_digit_mask(extracted, width, count)
    zeros = highs ^ positives
    unresolved = []
    while zeros:
        low_bit = zeros & -zeros
        digit_index = (low_bit.bit_length() - 1) // width
        unresolved.append(first_even + 2 * digit_index)
        zeros ^= low_bit
    encoded = computed.packed_prime.to_bytes((computed.packed_prime.bit_length() + 7) // 8,
                                             "little")
    return {
        "method": "packed odd-prime square and simultaneous nonzero-digit test v1",
        "first_even": first_even, "last_even": last, "target_count": count,
        "computed_last_even": computed.last_even, "capacity_even": computed.capacity_even,
        "digit_bits": width, "encoded_odd_prime_count": computed.prime_count,
        "prime_polynomial_sha256": hashlib.sha256(encoded).hexdigest(),
        "certified_target_count": positives.bit_count(),
        "unresolved_targets": unresolved, "all_certified": positives == highs,
        "scope": "exact finite collective certificate; no unbounded positivity or speed claim",
    }


def replay_certificate(receipt: dict) -> bool:
    """Recompute the prime inputs and full square and compare the entire receipt."""
    if type(receipt) is not dict:
        raise ValueError("receipt object required")
    try:
        computed = build_prime_square(receipt["computed_last_even"], receipt["capacity_even"])
        expected = certify_block(computed, receipt["first_even"], receipt["target_count"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("invalid certificate parameters") from error
    # Canonical JSON comparison distinguishes e.g. true from integer 1.
    if json.dumps(receipt, sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("certificate does not match exact replay")
    return True
