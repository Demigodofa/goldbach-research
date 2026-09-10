"""Reproduce the finite lag decomposition in mobius_covariance_additive_kernel.

This is a floating diagnostic, not asymptotic evidence.  It retains the exact
U=1 tail coefficient, hard interval, prime-modulus range, centered kernel, and
(log m)^2/m weights for the d=1 block.
"""

import math

import numpy as np


def _prime_flags(limit):
    flags = np.ones(limit + 1, dtype=bool)
    flags[:2] = False
    for p in range(2, math.isqrt(limit) + 1):
        if flags[p]:
            flags[p * p:limit + 1:p] = False
    return flags


def _mobius_values(limit):
    flags = _prime_flags(limit)
    values = np.ones(limit + 1, dtype=np.int8)
    for p in np.flatnonzero(flags):
        values[p:limit + 1:p] *= -1
        if p * p <= limit:
            values[p * p:limit + 1:p * p] = 0
    return values


def finite_actual_tail_lag_probe(N=200000):
    """Return the weighted d=1 lag components for J=(N/8,7N/8]."""
    if type(N) is not int or N < 1024:
        raise ValueError("integer N>=1024 required")
    H, M, V = int(N ** 0.1), int(N ** 0.59), int(N ** 0.15)
    low, high = N // 8, 7 * N // 8
    if H < 2:
        raise ValueError("N must make H>=2")

    mobius = _mobius_values(high)
    tail = np.zeros(high + 1, dtype=float)
    for a in range(V + 1, high + 1):
        coefficient = int(mobius[a])
        if coefficient == 0:
            continue
        first_b, last_b = low // a + 1, high // a
        if first_b > last_b:
            continue
        b = np.arange(first_b, last_b + 1, dtype=np.int64)
        tail[a * b] += coefficient * np.log(b)

    flags = _prime_flags(2 * M)
    primes = [m for m in range(M + 1, 2 * M + 1) if flags[m]]
    integers = np.arange(low + 1, high + 1, dtype=np.int64)
    coefficients = tail[low + 1:high + 1]
    keys = ("off", "principal_diagonal", "literal_residue_diagonal",
            "off_diagonal", "near_1_to_H", "near_H_to_2H",
            "leading_W_off_diagonal", "centering_off_diagonal",
            "full", "band")
    totals = {key: 0.0 for key in keys}
    positive_off = negative_off = 0

    for prime in primes:
        residues = np.bincount(integers % prime, weights=coefficients,
                               minlength=prime)
        residues[0] = 0.0
        modes = np.array([
            h for h in range(1, prime)
            if prime / (2 * math.pi * H) < min(h, prime - h)
            < prime / (math.pi * H)
        ], dtype=int)
        band_size = len(modes)
        indicator = np.zeros(prime)
        indicator[modes] = 1.0
        transform = np.fft.fft(residues)
        centered = transform + residues.sum() / (prime - 1)
        band = float(np.sum(np.abs(centered[modes]) ** 2))
        full = float(np.sum(np.abs(centered[1:]) ** 2))
        off = band - band_size / (prime - 1) * full

        W = np.fft.ifft(indicator) * prime
        correlation = np.fft.ifft(np.abs(transform) ** 2).real
        distances = np.minimum(np.arange(prime),
                               prime - np.arange(prime))
        literal_diagonal = float(np.sum(
            residues[1:] ** 2
            * (2 * W[1:].real / (prime - 1)
               + 2 * band_size / (prime - 1) ** 2)
        ))
        leading = float(np.sum((W[1:] * correlation[1:]).real))
        near_one = float(np.sum((W[(distances > 0) & (distances <= H)]
                                 * correlation[(distances > 0)
                                               & (distances <= H)]).real))
        near_two = float(np.sum((W[(distances > H) & (distances <= 2 * H)]
                                 * correlation[(distances > H)
                                               & (distances <= 2 * H)]).real))
        off_diagonal = off - literal_diagonal
        centering = off_diagonal - leading
        weight = math.log(prime) ** 2 / prime
        values = {
            "off": off,
            "principal_diagonal": band - off,
            "literal_residue_diagonal": literal_diagonal,
            "off_diagonal": off_diagonal,
            "near_1_to_H": near_one,
            "near_H_to_2H": near_two,
            "leading_W_off_diagonal": leading,
            "centering_off_diagonal": centering,
            "full": full,
            "band": band,
        }
        for key, value in values.items():
            totals[key] += weight * value
        positive_off += off > 0
        negative_off += off < 0

    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "prime_count": len(primes),
        "positive_off": positive_off,
        "negative_off": negative_off,
        **totals,
        "off_over_principal_diagonal": (
            totals["off"] / totals["principal_diagonal"]),
    }


if __name__ == "__main__":
    for name, value in finite_actual_tail_lag_probe().items():
        print(f"{name}: {value}")
