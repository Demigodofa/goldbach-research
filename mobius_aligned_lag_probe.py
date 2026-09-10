"""Resolve the aligned cross-row covariance by progression-index lag.

Owner: Kevin's Goldbach research. Purpose: test whether the positive cross-row
reinforcement in ``mobius_aligned_covariance_probe.py`` is confined to bounded
Delta=l2-l1 or remains spread across the full cofactor block. This is finite
d=1 evidence at tiny H,V, not an asymptotic shifted-correlation estimate.

With Phi_l from that module, define the real ordered lag contribution

 Q_Delta=2 Re sum_(A<=l<2A-Delta) [
    sum_(h in I_m) Phi_l(h) conjugate(Phi_(l+Delta)(h))
   -R/(m-1) sum_(1<=h<m) Phi_l(h) conjugate(Phi_(l+Delta)(h)) ], (1)

for 1<=Delta<A. For Delta=0 omit the factor 2; this is the complete same-row
term. Summing Q_Delta over Delta=0,...,A-1 exactly recovers total OFF. The
outer aggregation retains every prime m in (M,2M] and weight (log m)^2/m.
"""

import math

import numpy as np

from mobius_covariance_endpoint_probe import _actual_tail, _prime_flags


def finite_aligned_lag_probe(N=32000, cofactor_left=None):
    """Return weighted Q_Delta and positive-mass location for one finite N."""
    if type(N) is not int or N < 1024 or N % 32:
        raise ValueError("N must be an integer multiple of 32 and at least 1024")
    H, M, V = int(N ** .1), int(N ** .59), int(N ** .15)
    if cofactor_left is None:
        cofactor_left = (N + 8 * M - 1) // (8 * M)
    if type(cofactor_left) is not int or cofactor_left < 2:
        raise ValueError("cofactor_left must be an integer at least two")
    if 4 * M * cofactor_left > 7 * N // 8:
        raise ValueError("the aligned block can leave the central annulus")

    tail = _actual_tail(N, V, 0, N)
    flags = _prime_flags(2 * M)
    lag_totals = np.zeros(cofactor_left)
    principal_total = 0.0
    prime_count = 0

    for prime in range(M + 1, 2 * M + 1):
        if not flags[prime]:
            continue
        prime_count += 1
        modes = np.array([
            h for h in range(1, prime)
            if prime / (2 * math.pi * H) < min(h, prime - h)
            < prime / (math.pi * H)
        ], dtype=int)
        band_size = len(modes)
        rows = np.zeros((cofactor_left, prime))
        for index, ell in enumerate(range(cofactor_left, 2 * cofactor_left)):
            rows[index, 1:] = tail[prime * ell + 1:prime * (ell + 1)]
        transforms = np.fft.fft(rows, axis=1)
        centered = transforms + rows.sum(axis=1)[:, None] / (prime - 1)

        local_lags = np.zeros(cofactor_left)
        for delta in range(cofactor_left):
            left = centered[:cofactor_left - delta]
            right = centered[delta:]
            band_cross = float(np.real(np.sum(
                left[:, modes] * np.conjugate(right[:, modes]))))
            full_cross = float(np.real(np.sum(
                left[:, 1:] * np.conjugate(right[:, 1:]))))
            value = band_cross - band_size / (prime - 1) * full_cross
            local_lags[delta] = value if delta == 0 else 2 * value

        combined = rows.sum(axis=0)
        combined_transform = np.fft.fft(combined)
        combined_centered = (combined_transform
                             + combined.sum() / (prime - 1))
        full = float(np.sum(np.abs(combined_centered[1:]) ** 2))
        principal = band_size / (prime - 1) * full
        weight = math.log(prime) ** 2 / prime
        lag_totals += weight * local_lags
        principal_total += weight * principal

    normalized = lag_totals / principal_total
    cross = normalized[1:]
    positive = np.maximum(cross, 0)
    positive_total = float(np.sum(positive))
    first_quarter = max(1, (cofactor_left - 1) // 4)
    last_half = max(1, (cofactor_left - 1) // 2)
    positive_lags = np.flatnonzero(cross > 0) + 1
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "cofactor_left": cofactor_left,
        "prime_count": prime_count,
        "normalized_lag_contributions": tuple(float(x) for x in normalized),
        "normalized_total_off": float(np.sum(normalized)),
        "normalized_same_row": float(normalized[0]),
        "normalized_cross_row": float(np.sum(cross)),
        "positive_cross_mass": positive_total,
        "positive_mass_first_quarter_fraction": (
            float(np.sum(positive[:first_quarter]) / positive_total)
            if positive_total else 0.0),
        "positive_mass_last_half_fraction": (
            float(np.sum(positive[last_half:]) / positive_total)
            if positive_total else 0.0),
        "peak_cross_lag": int(np.argmax(cross) + 1),
        "furthest_positive_lag": (int(positive_lags[-1])
                                  if positive_lags.size else None),
        "bounded_lag_cancellation_proved": False,
    }


if __name__ == "__main__":
    for key, value in finite_aligned_lag_probe().items():
        print(f"{key}: {value}")
