"""Exact finite counts from a shorter earlier parity prefix.

Owner: Kevin's research. Purpose: combine the previously checked support
identity in notes/cubic-margin-structure.md with the parity bootstrap and
measure the SAME frozen 1000-target block. The evidence file retains exact
counts for future comparisons without repeating a full prime-square control.
Sol checked the mechanism, ranges, actual implementation and evidence on
2026-09-08. Four focused tests passed normally and with Python -O.

Let H=last-3 and z=floor(sqrt(last/2)). Square-start survivors are A=P+C.
Require H<(z+1)^3, z<=B and odd_floor(H/(z+1))<=B, where B is the last
odd integer classified by earlier truthful output parities. Then every C
entry is uniquely qr with known primes z<q<=r. Also 2*(z+1)^2>last, so
every composite exceeds last/2: [C*C]_N=C(N/2)=0 throughout the band.
Consequently G(N)=[A*A]_N-2[A*C]_N is EXACT, including prime diagonals.
This G need not equal the earlier CUBIC-cutoff bound L at the same target.

No exact G input is needed: recover_parity_primes reads L(2m) mod2 even
when the supplied values are negative. Its typing checks do not prove
parity truth; the canonical wrapper supplies it by induction from L(6)=1.
No ordinary full prime sieve or high prime polynomial square is called in
production. A,C still encode complete prime/composite information: this
does not avoid the arithmetic of classifying survivors using earlier factors.

For odd slots 3+2i, i=0..s-1, put bit i of a forward vector at slot i and
bit i of a reversed vector at slot s-1-i. The coefficient at target N is
popcount(forward & (reversed >> (s-1-(N-6)/2))). Thus each target uses two
exact nonnegative intersection counts followed by signed subtraction.
There is no packed-digit borrowing or high-prime square in this step.

This reuses an existing support identity, not a new positivity theorem or
historical novelty claim. Every finite target still requires computation.
Exactness never establishes that every future output will be positive.
The frozen block is separate from its earlier input prefix; the intervening
targets are not computed and the isolated counts are not a contiguous prefix.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from math import isqrt
from pathlib import Path
from time import perf_counter

from cubic_batch import _build_survivors
from parity_bound_bootstrap import _odd_floor, generate_prefix, recover_parity_primes


def _shape(first: int, count: int, cutoff: int | None = None) -> tuple[int, int, int, int]:
    if type(first) is not int or first < 6 or first % 2:
        raise ValueError("first must be an exact even integer at least6")
    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive exact integer")
    last = first + 2*(count-1)
    high = last-3
    z = isqrt(last//2) if cutoff is None else cutoff
    if type(z) is not int or z < 1:
        raise ValueError("cutoff must be a positive exact integer")
    if high >= (z+1)**3:
        raise ValueError("cutoff does not guarantee at most two residual prime factors")
    if 2*(z+1)**2 <= last:
        raise ValueError("residual composite-pair support can meet the target band")
    return last, high, z, _odd_floor(high//(z+1))


def required_prefix_end(first: int, count: int, *, cutoff: int | None = None) -> int:
    """Sufficient earlier output endpoint for the declared support construction.

    This is the smallest endpoint of form2B for odd B satisfying these
    sufficient input conditions, not an information-theoretic minimum.
    It must precede first; a very wide requested band may fail this condition.
    """
    _, _, z, cofactor = _shape(first, count, cutoff)
    bound = max(3, z, cofactor)
    if bound % 2 == 0:
        bound += 1
    endpoint = 2*bound
    if endpoint >= first:
        raise ValueError("required parity input would not precede every target")
    return endpoint


def reflected_counts(left: bytearray, right: bytearray, first: int, count: int) -> list[int]:
    """Exact ordered convolution coefficients of full binary odd-slot arrays.

    Slot zero means3. Arrays end at the same odd H. The returned coefficients
    concern arbitrary indicators; this helper does not certify primality.
    """
    if (not isinstance(left, bytearray) or not isinstance(right, bytearray)
            or not left or len(left) != len(right)
            or any(value not in (0, 1) for value in left)
            or any(value not in (0, 1) for value in right)):
        raise ValueError("require nonempty equal-length binary odd-slot arrays")
    if type(first) is not int or first < 6 or first % 2:
        raise ValueError("first must be an exact even integer at least6")
    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive exact integer")
    capacity = 2*len(left)+4
    if first+2*(count-1) > capacity:
        raise ValueError("target exceeds the declared full odd-slot range")
    table = bytes.maketrans(b"\x00\x01", b"01")
    forward = int(bytes(left).translate(table)[::-1], 2)
    reverse = int(bytes(right).translate(table), 2)
    first_shift = (capacity-first)//2
    return [(forward & (reverse >> (first_shift-i))).bit_count() for i in range(count)]


def support_exact_batch(bounds: list[int], first: int, count: int, *,
                        cutoff: int | None = None) -> dict:
    """Conditional exact ordered G counts from earlier truthful output PARITIES.

    A custom cutoff must satisfy the same cubic and strict support conditions.
    Values need not be exact counts, positive, or even lower bounds; only their
    labelled parities are used. Type/range checks do not authenticate that truth.
    """
    started = perf_counter()
    last, high, z, cofactor = _shape(first, count, cutoff)
    endpoint, classified, primes = recover_parity_primes(bounds)
    if first <= endpoint:
        raise ValueError("all target labels must follow the supplied parity prefix")
    if z > classified or cofactor > classified:
        raise ValueError("earlier parity prefix does not cover all factor inputs")
    recovered_at = perf_counter()
    survivors, composites, _ = _build_survivors(primes, z, high)
    # Guard the exact support premise on the constructed finite arrays too.
    if any(composites[:max(0, (last//2-1)//2)]):
        raise RuntimeError("constructed composite support reaches the lower half")
    built_at = perf_counter()
    ms = reflected_counts(survivors, survivors, first, count)
    acs = reflected_counts(survivors, composites, first, count)
    counts = [m-2*ac for m, ac in zip(ms, acs)]
    if any(value < 0 for value in counts):
        raise RuntimeError("negative exact count contradicts the conditional input meaning")
    minimum = min(range(count), key=counts.__getitem__)
    return {
        "first_even": first, "last_even": last, "target_count": count,
        "input_prefix_end": endpoint, "classified_last_odd": classified,
        "cutoff": z, "required_cofactor_limit": cofactor,
        "surviving_composites": sum(composites), "counts": counts,
        "counts_sha256": hashlib.sha256(
            ",".join(map(str, counts)).encode("ascii")).hexdigest(),
        "minimum_row": {"target_even": first+2*minimum, "G": counts[minimum],
                        "M": ms[minimum], "AC": acs[minimum]},
        "zero_targets": [first+2*i for i, value in enumerate(counts) if value == 0],
        "seconds": {"parity_recovery": recovered_at-started,
                    "construction": built_at-recovered_at,
                    "bitset_counts": perf_counter()-built_at,
                    "pipeline_total": perf_counter()-started},
        "input_meaning": "conditional on truthful earlier labelled Goldbach parities",
        "scope": "finite exact counts; no unbounded positivity or speed theorem",
    }


def canonical_experiment() -> dict:
    """Frozen exact-count block; charge all earlier parity generation."""
    started = perf_counter()
    first, count = 1002000, 1000
    endpoint = required_prefix_end(first, count)
    prefix = generate_prefix(endpoint)
    result = support_exact_batch(prefix["lower_bounds"], first, count)
    result["seconds"]["input_generation"] = prefix["seconds"]
    result["seconds"]["complete_total"] = perf_counter()-started
    result["input_meaning"] = prefix["input_meaning"]
    result["input_sha256"] = prefix["lower_bounds_sha256"]
    result["method"] = "support-exact square-start sieve with reflected bit counts"
    return result


def validate_frozen(result: dict) -> None:
    """Independent packed-prime-square control plus a same-block fast reference.

    Both ordinary prime sieves occur ONLY here, outside production timing.
    The fast reference shares reflected_counts, so the packed square is the
    independent coefficient algorithm. No timing is an asymptotic speed claim.
    """
    validation_started = perf_counter()
    from packed_goldbach import build_prime_square
    reference = build_prime_square(result["last_even"])
    width = reference.digit_bits
    count, first = result["target_count"], result["first_even"]
    packed = (reference.packed_square >> (width*(first//2-1))) & ((1 << (width*count))-1)
    raw = packed.to_bytes(width//8*count, "little")
    step = width//8
    control = [int.from_bytes(raw[i:i+step], "little") for i in range(0, len(raw), step)]
    if control != result["counts"]:
        raise RuntimeError("independent packed prime-square control disagrees")
    result["seconds"]["independent_full_square_validation"] = perf_counter()-validation_started

    fast_started = perf_counter()
    from redistribution import sieve
    flags = sieve(result["last_even"]-3)
    odd_flags = flags[3::2]
    fast = reflected_counts(odd_flags, odd_flags, first, count)
    if fast != control:
        raise RuntimeError("same-block sieve/bitset reference disagrees")
    result["seconds"]["same_block_sieve_bitset_reference"] = perf_counter()-fast_started
    result["validation"] = {
        "matched_targets": count,
        "independent_coefficients": "existing packed_goldbach full prime square",
        "fast_reference": "ordinary prime sieve plus the same reflected bit-count kernel",
        "timing_scope": "one run; full square also computes all earlier coefficients",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-controls", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = canonical_experiment()
    if args.check_controls:
        validate_frozen(result)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "counts"}, indent=2))


if __name__ == "__main__":
    main()
