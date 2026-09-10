"""Falsify cross-scale resonance between two dyadic divisor bands.

For squarefree divisors a in (U,2U] and b in (W,2W], this probe forms the
exact shifted active matrix between complete rows l_L and l_R and normalizes
its two sides by their respective rho-weighted totient frames.  The largest
singular value is the exact finite maximum over independent complex
coefficient vectors on the two bands.

The initial falsifier is growth like sqrt(max(U,W)/min(U,W)), which is the
loss suggested by bounding only one Schur direction of the gcd kernel.  A
matching opposite-direction estimate could cancel that loss in rectangular
Schur.  This probe is finite evidence, not a cross-band theorem.
"""

import math

import numpy as np

from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from mobius_cross_divisor_gram import _progression_vectors
from near_cutoff_geometric_bound import _active_modes


def cross_divisor_band_probe(modulus, shift_length, ell_left, ell_right,
                             band_left, band_right):
    """Return the exact two-frame normalized cross-band operator norm."""
    if any(type(value) is not int for value in (
            modulus, shift_length, ell_left, ell_right,
            band_left, band_right)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= min(band_left, band_right)
            or 2 * max(band_left, band_right) >= modulus
            or ell_left < 1 or ell_right < 1):
        raise ValueError("invalid cross-band ranges")
    flags = _prime_flags(modulus)
    if not flags[modulus]:
        raise ValueError("modulus must be prime")
    mobius = _mobius_values(2 * max(band_left, band_right))
    left_divisors = tuple(
        a for a in range(band_left + 1, 2 * band_left + 1) if mobius[a])
    right_divisors = tuple(
        a for a in range(band_right + 1, 2 * band_right + 1) if mobius[a])
    modes = _active_modes(modulus, shift_length)
    rho = len(modes) / (modulus - 1)
    _, left_vectors = _progression_vectors(
        modulus, shift_length, ell_left, left_divisors)
    _, right_vectors = _progression_vectors(
        modulus, shift_length, ell_right, right_divisors)
    active = ((1 - rho) * left_vectors
              @ np.conjugate(right_vectors.T))

    left_array = np.array(left_divisors, dtype=float)
    right_array = np.array(right_divisors, dtype=float)
    left_frame = (
        rho * modulus ** 2
        * np.log(modulus * ell_left / left_array) ** 2
        * np.array([_totient(a) for a in left_divisors]) / left_array ** 2)
    right_frame = (
        rho * modulus ** 2
        * np.log(modulus * ell_right / right_array) ** 2
        * np.array([_totient(a) for a in right_divisors]) / right_array ** 2)
    normalized = active / np.sqrt(
        left_frame[:, None] * right_frame[None, :])
    singular_values = np.linalg.svd(normalized, compute_uv=False)

    left_mu = np.array([mobius[a] for a in left_divisors], dtype=float)
    right_mu = np.array([mobius[a] for a in right_divisors], dtype=float)
    mobius_cross = abs(left_mu @ active @ right_mu)
    mobius_frame = math.sqrt(
        float(np.sum(left_frame * left_mu ** 2))
        * float(np.sum(right_frame * right_mu ** 2)))
    ratio = max(band_left, band_right) / min(band_left, band_right)
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "rho": rho,
        "ell_left": ell_left,
        "ell_right": ell_right,
        "row_delta": ell_right - ell_left,
        "left_band": (band_left, 2 * band_left),
        "right_band": (band_right, 2 * band_right),
        "left_divisor_count": len(left_divisors),
        "right_divisor_count": len(right_divisors),
        "band_scale_ratio": ratio,
        "largest_cross_band_singular_value": float(singular_values[0]),
        "singular_value_over_sqrt_scale_ratio": float(
            singular_values[0] / math.sqrt(ratio)),
        "mobius_cross_band_quotient": float(mobius_cross / mobius_frame),
        "cross_band_frame_bound_proved": False,
    }


if __name__ == "__main__":
    for key, value in cross_divisor_band_probe(
            1009, 5, 9, 12, 8, 16).items():
        print(f"{key}: {value}")
