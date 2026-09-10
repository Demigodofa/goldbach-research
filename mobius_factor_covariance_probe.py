"""Finite covariance matrix for lower, balanced, and upper Mobius factors.

This probe keeps the exact d=1 U=1 tail on J=(N/8,7N/8], splitting its
divisor a into

 lower:   V<a<=floor(N^.41),
 balanced:floor(N^.41)<a<M,
 upper:   a>=M, where M=floor(N^.59).

For each component and each prime m it forms the exact centered additive
field.  It then records the full 3x3 principal and OFF covariance matrices,
including cross terms.  This is floating finite evidence at tiny V, not an
asymptotic estimate and not a proof that exponent cutoffs are literal
finite-N comparisons with m.

MEASURED RESULTS.
At N=200000,H=3,V=6, all 171 primes, the component OFF/DIAG ratios are

 lower -0.051785, balanced +0.006337, upper -0.006914.

At N=1200000,H=4,V=8, all 444 primes, they are

 lower -0.035441, balanced +0.002394, upper +0.005203.

The balanced component is close to uniform active-energy allocation at both
scales and shows no finite resonance.  But component principal diagonals sum
to 4.63 and 5.43 times the total diagonal because the factor ranges have large
cross terms.  Cross OFF is positive at H=3 and negative at H=4.  Thus this
probe motivates a balanced-box theorem but does not transfer it to the full
tail, establish a trend, or license dropping cross-regime covariance.
"""

import math

import numpy as np

from mobius_covariance_lag_probe import _mobius_values, _prime_flags


def finite_factor_covariance_probe(N=200000):
    """Return weighted 3x3 DIAG and OFF matrices for the exact central block."""
    if type(N) is not int or N < 1024:
        raise ValueError("integer N>=1024 required")
    H, M, V = int(N ** 0.1), int(N ** 0.59), int(N ** 0.15)
    first_cut, second_cut = int(N ** 0.41), M
    low, high = N // 8, 7 * N // 8
    mobius = _mobius_values(high)
    tails = np.zeros((3, high + 1), dtype=float)
    for a in range(V + 1, high + 1):
        coefficient = int(mobius[a])
        if coefficient == 0:
            continue
        first_b, last_b = low // a + 1, high // a
        if first_b > last_b:
            continue
        b = np.arange(first_b, last_b + 1, dtype=np.int64)
        component = 0 if a <= first_cut else (1 if a < second_cut else 2)
        tails[component, a * b] += coefficient * np.log(b)

    flags = _prime_flags(2 * M)
    primes = tuple(m for m in range(M + 1, 2 * M + 1) if flags[m])
    integers = np.arange(low + 1, high + 1, dtype=np.int64)
    diagonal = np.zeros((3, 3), dtype=complex)
    off = np.zeros((3, 3), dtype=complex)

    for prime in primes:
        modes = np.array([
            h for h in range(1, prime)
            if prime / (2 * math.pi * H) < min(h, prime - h)
            < prime / (math.pi * H)
        ], dtype=int)
        band_size = len(modes)
        fields = []
        for component in range(3):
            residues = np.bincount(
                integers % prime,
                weights=tails[component, low + 1:high + 1],
                minlength=prime,
            )
            residues[0] = 0.0
            transform = np.fft.fft(residues)
            fields.append(transform + residues.sum() / (prime - 1))
        weight = math.log(prime) ** 2 / prime
        for row in range(3):
            for column in range(3):
                full = np.vdot(fields[column][1:], fields[row][1:])
                band = np.vdot(fields[column][modes], fields[row][modes])
                principal = band_size / (prime - 1) * full
                diagonal[row, column] += weight * principal
                off[row, column] += weight * (band - principal)

    diagonal_real = diagonal.real
    off_real = off.real
    total_diagonal = float(np.sum(diagonal_real))
    total_off = float(np.sum(off_real))
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "first_cut": first_cut,
        "second_cut": second_cut,
        "prime_count": len(primes),
        "labels": ("lower", "balanced", "upper"),
        "principal_matrix": tuple(tuple(float(value) for value in row)
                                  for row in diagonal_real),
        "off_matrix": tuple(tuple(float(value) for value in row)
                            for row in off_real),
        "component_off_over_diagonal": tuple(
            float(off_real[index, index] / diagonal_real[index, index])
            for index in range(3)),
        "total_diagonal": total_diagonal,
        "total_off": total_off,
        "total_off_over_diagonal": total_off / total_diagonal,
        "component_diagonal_sum_over_total": (
            float(np.trace(diagonal_real) / total_diagonal)),
        "diagonal_component_off": float(np.trace(off_real)),
        "cross_component_off": float(total_off - np.trace(off_real)),
        "maximum_imaginary_roundoff": float(max(
            np.max(np.abs(diagonal.imag)), np.max(np.abs(off.imag)))),
    }


if __name__ == "__main__":
    for name, value in finite_factor_covariance_probe().items():
        print(f"{name}: {value}")
