"""Finite covariance test for actual-shaped affine endpoint families.

Owner: Kevin's Goldbach research.  Purpose: determine whether the freedom in
the arbitrary ``J_m`` sufficient conjecture is present in the underlying
prime-product transfer.  This is a finite diagnostic, not an asymptotic bound.

If the prime companion is m, the shift is r, and an actual dyadic cofactor
block is A<n<=2A, then k=m*n gives the exact conjugated prime interval

    J^C_(m,r)=(m*A+r, 2*m*A+r],                            (1)

where p=k+r.  In the reflected form p=N-k+r, the corresponding integer prime
set is

    N-2*m*A+r <= p < N-m*A+r,

or, in the common (L,R] convention,

    J^R_(m,r)=(N-2*m*A+r-1, N-m*A+r-1].                   (2)

Thus the physical endpoints are affine in m and r with a common cofactor
block; they are not arbitrary independent choices.  The later maximal-prefix
bound safely forgets this relation, and ``active_band_energy_conjecture.py``
explicitly states the resulting arbitrary-family estimate only as a sufficient
surrogate with a missing endpoint/kernel transfer.

More exactly, expanding the short divisor d|n and writing n=d*l gives q=dm
and

    floor(A/d)+1 <= l <= floor(2A/d).                      (3)

The conjugated primes are q*l+r and the reflected primes are N-q*l+r.  Hence
their progression-index interval depends only on A and d, not on m, and both
physical endpoints are aligned to the same residue modulo q.  This exact
alignment is absent from an arbitrary ``J_m`` selector.

For the finite test choose M=floor(N^.59), H=floor(N^.1), and
A=ceil(N/(8M)).  Then (A,2A] models the critical complementary exponent .41
and both (1) and (2) lie in the central annulus for the tested N.  It need not
be one of the literal finite detector blocks.  We retain the
exact d=1 coefficient mu_>V*log, V=floor(N^.15), residue-zero mask, angular
active modes, and outer (log m)^2/m weights.  Testing r=-H,0,H probes the
endpoint motion across the effective shift width; it does not replace the
actual Schwartz-weighted sum over every r.

MEASURED RESULTS.
At N=32000 every admissible A=9,...,15 and all six orientation/shift families
had negative aggregate OFF/DIAG; the range was -.289474 to -.009879. At
N=200000 every admissible A=19,...,32 was again negative, with range -.163491
to -.000267. For the default A, N=1200000 gave -.1569 for the conjugated and
-.1775 for the reflected family, essentially unchanged by r=-H,0,H. This
contrasts with the earlier arbitrary per-modulus selector's positive aggregate
ratios .1383,.1161,.0600. It is an actual-shaped clue that endpoint alignment
removes that adversarial selection mechanism, but the nearly zero finite margin
and omitted weighted r-sum prohibit a sign theorem, power saving, or trend.
"""

import math

import numpy as np

from mobius_covariance_endpoint_probe import _actual_tail, _prime_flags


def progression_index_interval(cofactor_left, divisor):
    """Exact l-range (3) after n=d*l in A<n<=2A."""
    if (type(cofactor_left) is not int or type(divisor) is not int
            or cofactor_left < 1 or divisor < 1):
        raise ValueError("positive integer cofactor_left and divisor required")
    first = cofactor_left // divisor + 1
    last = (2 * cofactor_left) // divisor
    return first, last


def _interval_covariance(tail, prime, H, low, high):
    if not 0 <= low < high < len(tail):
        raise ValueError("interval must lie inside the precomputed tail")
    integers = np.arange(low + 1, high + 1, dtype=np.int64)
    residues = np.bincount(
        integers % prime,
        weights=tail[low + 1:high + 1],
        minlength=prime,
    )
    residues[0] = 0.0
    transform = np.fft.fft(residues)
    centered = transform + residues.sum() / (prime - 1)
    modes = np.array([
        h for h in range(1, prime)
        if prime / (2 * math.pi * H) < min(h, prime - h)
        < prime / (math.pi * H)
    ], dtype=int)
    band = float(np.sum(np.abs(centered[modes]) ** 2))
    full = float(np.sum(np.abs(centered[1:]) ** 2))
    diagonal = len(modes) / (prime - 1) * full
    return band - diagonal, diagonal


def finite_structured_endpoint_probe(N=32000, cofactor_left=None):
    """Measure conjugated/reflected affine endpoint families at r=-H,0,H."""
    if type(N) is not int or N < 1024 or N % 32:
        raise ValueError("N must be an integer multiple of 32 and at least 1024")
    H, M, V = int(N ** .1), int(N ** .59), int(N ** .15)
    if cofactor_left is None:
        cofactor_left = (N + 8 * M - 1) // (8 * M)
    if type(cofactor_left) is not int or cofactor_left < 1:
        raise ValueError("cofactor_left must be a positive integer")
    tail = _actual_tail(N, V, 0, N)
    flags = _prime_flags(2 * M)
    primes = tuple(m for m in range(M + 1, 2 * M + 1) if flags[m])
    central_low, central_high = N // 8, 7 * N // 8
    output = {}

    for shift in (-H, 0, H):
        for reflected in (False, True):
            total_off = total_diagonal = 0.0
            positive = 0
            smallest_ratio, largest_ratio = float("inf"), -float("inf")
            for prime in primes:
                if reflected:
                    low = N - 2 * prime * cofactor_left + shift - 1
                    high = N - prime * cofactor_left + shift - 1
                else:
                    low = prime * cofactor_left + shift
                    high = 2 * prime * cofactor_left + shift
                if low < central_low or high > central_high:
                    raise ArithmeticError("chosen affine family left the central annulus")
                off, diagonal = _interval_covariance(tail, prime, H, low, high)
                weight = math.log(prime) ** 2 / prime
                total_off += weight * off
                total_diagonal += weight * diagonal
                positive += off > 0
                ratio = off / diagonal
                smallest_ratio = min(smallest_ratio, ratio)
                largest_ratio = max(largest_ratio, ratio)
            label = ("reflected" if reflected else "conjugated", shift)
            output[label] = {
                "off_over_diagonal": total_off / total_diagonal,
                "positive_modulus_count": positive,
                "individual_ratio_min": smallest_ratio,
                "individual_ratio_max": largest_ratio,
            }

    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "cofactor_block": (cofactor_left, 2 * cofactor_left),
        "prime_count": len(primes),
        "families": output,
        "arbitrary_interval_family_needed_by_physical_endpoints": False,
        "actual_weighted_shift_sum_estimated": False,
    }


if __name__ == "__main__":
    for key, value in finite_structured_endpoint_probe().items():
        print(f"{key}: {value}")
