"""Exact finite raw union bounds with a variable first-stage sieve cutoff.

Unlike cubic_sieve, this module never assumes residual multiplicity <=2.
The raw expression M-S1 is a lower bound at every cutoff, but need not be
positive. Its failure is not a Goldbach counterexample.
"""
from __future__ import annotations

from cubic_sieve import event_masks


def raw_union_profile(target: int, cutoffs: list[int]) -> list[dict]:
    """Reuse one exact event family to assess the requested presieve cutoffs."""
    if not isinstance(cutoffs, list) or not cutoffs:
        raise ValueError("a nonempty list of cutoffs is required")
    if any(type(z) is not int or z < 0 for z in cutoffs):
        raise ValueError("cutoffs must be nonnegative exact integers")
    built = event_masks(target)
    slots = built["M_slots"]
    masks = built["event_masks"]
    full = (1 << slots) - 1
    output = []
    for cutoff in cutoffs:
        pre_union = 0
        for prime, mask in masks.items():
            if prime <= cutoff:
                pre_union |= mask
        base = full & ~pre_union
        residual = [(prime, mask & base) for prime, mask in masks.items()
                    if prime > cutoff]
        M = base.bit_count()
        S1 = sum(mask.bit_count() for _, mask in residual)
        output.append({
            "target_even": target,
            "presieve_cutoff": cutoff,
            "candidate_count": slots,
            "M_after_presieve": M,
            "S1": S1,
            "raw_lower_bound": M - S1,
            "positive_certificate": M > S1,
            "pre_sieve_event_count": sum(prime <= cutoff for prime in masks),
            "residual_event_count": len(residual),
            "scope": "exact finite raw union lower bound; no two-overlap identity assumed",
        })
    return output
