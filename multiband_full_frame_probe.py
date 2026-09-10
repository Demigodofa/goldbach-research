"""Test coercivity of the exact full Gram across several divisor bands.

On one dyadic band, the positive gcd-feature Gram dominates the totient frame
because the feature d=a is unique to coordinate a.  Across a union (V,B], a
can divide a larger retained divisor, so that simple uniqueness proof fails.

This probe forms the exact full-frequency Gram G, the frozen gcd-feature Gram
P0, and the block totient frame F for every squarefree V<a<=B.  The minimum
eigenvalues of F^(-1/2)GF^(-1/2) and F^(-1/2)P0F^(-1/2) are the finite
coercivity falsifiers.  Collapse toward zero would prevent directly assembling
the pairwise active bounds across bands.  This is finite evidence only.
"""

import math

import numpy as np

from divisor_active_full_gram import _full_collision_gram
from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values


def multiband_full_frame_probe(modulus, ell, divisor_lower, divisor_upper):
    """Return exact and ideal generalized eigenvalue receipts on (V,B]."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all arguments must be integers")
    if (ell < 1 or divisor_lower < 2
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid multiband ranges")
    flags = _prime_flags(modulus)
    if not flags[modulus]:
        raise ValueError("modulus must be prime")
    mobius = _mobius_values(divisor_upper)
    divisors = tuple(a for a in range(divisor_lower + 1, divisor_upper + 1)
                     if mobius[a])
    if not divisors:
        raise ValueError("the squarefree divisor range must be nonempty")
    divisor_array = np.array(divisors, dtype=float)
    logs = np.log(modulus * ell / divisor_array)
    totients = np.array([_totient(a) for a in divisors], dtype=float)
    frame = modulus ** 2 * logs ** 2 * totients / divisor_array ** 2
    gcd_matrix = np.array([
        [math.gcd(left, right) for right in divisors]
        for left in divisors], dtype=float)
    ideal = (modulus ** 2 * logs[:, None] * logs[None, :]
             * (gcd_matrix - 1)
             / (divisor_array[:, None] * divisor_array[None, :]))
    exact = _full_collision_gram(modulus, ell, divisors)
    scale = np.sqrt(frame)
    ideal_normalized = ideal / (scale[:, None] * scale[None, :])
    exact_normalized = exact / (scale[:, None] * scale[None, :])
    ideal_values = np.linalg.eigvalsh(
        (ideal_normalized + ideal_normalized.T) / 2)
    exact_values = np.linalg.eigvalsh(
        (exact_normalized + exact_normalized.T) / 2)
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "divisor_count": len(divisors),
        "scale_ratio": divisor_upper / divisor_lower,
        "ideal_over_block_frame_min": float(ideal_values[0]),
        "ideal_over_block_frame_max": float(ideal_values[-1]),
        "exact_over_block_frame_min": float(exact_values[0]),
        "exact_over_block_frame_max": float(exact_values[-1]),
        "exact_block_frame_condition_number": float(
            exact_values[-1] / exact_values[0]),
        "multiband_lower_frame_proved": False,
    }


if __name__ == "__main__":
    for key, value in multiband_full_frame_probe(1009, 9, 8, 64).items():
        print(f"{key}: {value}")
