"""Finite endpoint stress test for the actual d=1 Mobius covariance.

The conjectural inequality is uniform in every hard interval J_m.  This probe
uses the exact U=1 tail and scans every pair of endpoints on the N/32 grid
inside [N/8,7N/8] whose separation is at least N/16.  It reports both common
windows and the adversarial family obtained by choosing a window separately
for each prime modulus.  It is a floating finite diagnostic, not an asymptotic
estimate or a proof about intervals off the grid.

MEASURED RESULTS.
Every common grid window had negative aggregate OFF at all three tested
scales.  Allowing the theorem's actual interval-family freedom and selecting
the most positive window separately for every m changed the sign:

 N=32000,   H=2: 62/68 positive selections,  OFF/DIAG=+0.138274;
 N=200000,  H=3: 157/171 positive selections, OFF/DIAG=+0.116086;
 N=1200000, H=4: 374/444 positive selections, OFF/DIAG=+0.059999.

For N=200000 the 276 common-window ratios range from -0.293706 to -0.031212,
and the full interval gives -0.041560.  Individual window/modulus ratios range
from -0.554915 to +0.425614.  For N=1200000 the common full interval gives
-0.039048 and individual ratios range from -0.512901 to +0.303681.

These measurements reject aggregate nonpositivity as a finite uniform-family
mechanism: the displayed per-m choices are admissible grid intervals with the
unchanged Mobius--log coefficient.  They do not falsify the magnitude target;
the positive adversarial aggregate remains a small fraction of DIAG and no
asymptotic trend follows from H=2,3,4 or the tiny cutoffs V=4,6,8.
"""

import math

import numpy as np

from mobius_covariance_lag_probe import _mobius_values, _prime_flags


def _actual_tail(N, cutoff, low, high):
    mobius = _mobius_values(high)
    tail = np.zeros(high + 1, dtype=float)
    for a in range(cutoff + 1, high + 1):
        coefficient = int(mobius[a])
        if coefficient == 0:
            continue
        first_b, last_b = low // a + 1, high // a
        if first_b > last_b:
            continue
        b = np.arange(first_b, last_b + 1, dtype=np.int64)
        tail[a * b] += coefficient * np.log(b)
    return tail


def finite_endpoint_scan(N=200000):
    """Scan the exact N/32 endpoint grid and return weighted OFF/DIAG receipts."""
    if type(N) is not int or N < 1024 or N % 32:
        raise ValueError("N must be an integer multiple of 32 and at least 1024")
    H, M, V = int(N ** 0.1), int(N ** 0.59), int(N ** 0.15)
    low, high, step = N // 8, 7 * N // 8, N // 32
    endpoints = tuple(range(low, high + 1, step))
    windows = tuple((left, right) for left in range(len(endpoints))
                    for right in range(left + 2, len(endpoints)))
    tail = _actual_tail(N, V, low, high)
    flags = _prime_flags(2 * M)
    primes = tuple(m for m in range(M + 1, 2 * M + 1) if flags[m])

    common_off = np.zeros(len(windows))
    common_diagonal = np.zeros(len(windows))
    chosen_off_total = chosen_off_diagonal = 0.0
    chosen_ratio_off = chosen_ratio_diagonal = 0.0
    positive_best_count = 0
    individual_ratio_min = float("inf")
    individual_ratio_max = -float("inf")

    for prime in primes:
        snapshots = [np.zeros(prime)]
        running = np.zeros(prime)
        cursor = low
        for endpoint in endpoints[1:]:
            integers = np.arange(cursor + 1, endpoint + 1, dtype=np.int64)
            running = running + np.bincount(
                integers % prime, weights=tail[cursor + 1:endpoint + 1],
                minlength=prime,
            )
            snapshots.append(running.copy())
            cursor = endpoint

        modes = np.array([
            h for h in range(1, prime)
            if prime / (2 * math.pi * H) < min(h, prime - h)
            < prime / (math.pi * H)
        ], dtype=int)
        band_size = len(modes)
        off_values = np.empty(len(windows))
        diagonal_values = np.empty(len(windows))
        for index, (left, right) in enumerate(windows):
            residues = snapshots[right] - snapshots[left]
            residues[0] = 0.0
            transform = np.fft.fft(residues)
            centered = transform + residues.sum() / (prime - 1)
            band = float(np.sum(np.abs(centered[modes]) ** 2))
            full = float(np.sum(np.abs(centered[1:]) ** 2))
            diagonal = band_size / (prime - 1) * full
            off_values[index] = band - diagonal
            diagonal_values[index] = diagonal

        weight = math.log(prime) ** 2 / prime
        common_off += weight * off_values
        common_diagonal += weight * diagonal_values

        best_off = int(np.argmax(off_values))
        chosen_off_total += weight * off_values[best_off]
        chosen_off_diagonal += weight * diagonal_values[best_off]
        positive_best_count += off_values[best_off] > 0

        ratios = np.divide(off_values, diagonal_values,
                           out=np.full_like(off_values, -np.inf),
                           where=diagonal_values > 0)
        best_ratio = int(np.argmax(ratios))
        chosen_ratio_off += weight * off_values[best_ratio]
        chosen_ratio_diagonal += weight * diagonal_values[best_ratio]
        individual_ratio_min = min(individual_ratio_min, float(np.min(ratios)))
        individual_ratio_max = max(individual_ratio_max, float(np.max(ratios)))

    common_ratios = common_off / common_diagonal
    common_max = int(np.argmax(common_ratios))
    common_min = int(np.argmin(common_ratios))
    full_interval = windows.index((0, len(endpoints) - 1))

    def interval(index):
        left, right = windows[index]
        return (endpoints[left], endpoints[right])

    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "prime_count": len(primes),
        "endpoint_count": len(endpoints),
        "window_count": len(windows),
        "common_positive_window_count": int(np.sum(common_off > 0)),
        "common_max_ratio": float(common_ratios[common_max]),
        "common_max_interval": interval(common_max),
        "common_min_ratio": float(common_ratios[common_min]),
        "common_min_interval": interval(common_min),
        "common_full_interval_ratio": float(common_ratios[full_interval]),
        "per_modulus_best_off_positive_count": int(positive_best_count),
        "per_modulus_best_off_ratio": float(
            chosen_off_total / chosen_off_diagonal),
        "per_modulus_best_ratio_aggregate": (
            float(chosen_ratio_off / chosen_ratio_diagonal)),
        "individual_window_ratio_min": individual_ratio_min,
        "individual_window_ratio_max": individual_ratio_max,
    }


if __name__ == "__main__":
    for name, value in finite_endpoint_scan().items():
        print(f"{name}: {value}")
