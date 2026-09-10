"""Extend the triangular CRT main bound to two different complete rows.

Let the left row be m*l+x and the right row m*(l+Delta)+y, with
1<=x,y<=R=m-1, and put s=x-y.  For g=gcd(a,b), the two divisibility
conditions are compatible exactly when

 s == m*Delta (mod g).                                  (1)

Thus the shifted triangular kernel is

 T_(g,t)(h)=sum_(|s|<R, s==t mod g)(R-|s|)e_m(-hs),
 t=m*Delta mod g.                                      (2)

For residues r modulo g define

 A_r(h)=sum_(1<=x<=R, x==r mod g)e_m(-hx).

Counting pairs x-y=s gives the exact cross-correlation identity

 T_(g,t)(h)=sum_(r mod g) A_r(h)conj(A_(r-t)(h)).        (3)

Cauchy and permutation of the residue classes give

 |T_(g,t)(h)| <= sum_r |A_r(h)|^2 = T_(g,0)(h).         (4)

Consequently every active-frequency sum of the shifted main is bounded by
the already proved zero-shift Fejer estimate, uniformly in Delta.  The same
frame-normalized entry and Schur bounds therefore apply with no lag-count
factor.  This controls the shifted triangular density only; shifted CRT
count/log discrepancy and centering are separate terms.
"""

import cmath
import math

from mobius_covariance_endpoint_probe import _prime_flags
from near_cutoff_geometric_bound import _active_modes
from triangular_crt_main_bound import (
    row_triangular_main_bound,
    triangular_kernel_sum_bound,
)


def _require_prime(modulus):
    flags = _prime_flags(modulus)
    if not flags[modulus]:
        raise ValueError("modulus must be prime")


def shifted_triangular_kernel(modulus, gcd_value, residue, frequency):
    """Evaluate (2) directly for a finite identity/falsification check."""
    if any(type(value) is not int for value in (
            modulus, gcd_value, residue, frequency)):
        raise ValueError("all arguments must be integers")
    if (not 1 <= gcd_value < modulus
            or not 0 <= residue < gcd_value
            or not 1 <= frequency < modulus):
        raise ValueError("invalid kernel ranges")
    _require_prime(modulus)
    radius = modulus - 1
    return sum(
        (radius - abs(separation)) * cmath.exp(
            -2j * math.pi * frequency * separation / modulus)
        for separation in range(-radius + 1, radius)
        if (separation - residue) % gcd_value == 0)


def shifted_triangular_feature_kernel(modulus, gcd_value, residue,
                                       frequency):
    """Evaluate the residue-class cross-correlation on the right of (3)."""
    if any(type(value) is not int for value in (
            modulus, gcd_value, residue, frequency)):
        raise ValueError("all arguments must be integers")
    if (not 1 <= gcd_value < modulus
            or not 0 <= residue < gcd_value
            or not 1 <= frequency < modulus):
        raise ValueError("invalid kernel ranges")
    _require_prime(modulus)
    features = []
    for class_value in range(gcd_value):
        features.append(sum(
            cmath.exp(-2j * math.pi * frequency * value / modulus)
            for value in range(1, modulus)
            if value % gcd_value == class_value))
    return sum(
        features[class_value]
        * features[(class_value - residue) % gcd_value].conjugate()
        for class_value in range(gcd_value))


def shifted_kernel_active_sum_bound(modulus, shift_length, gcd_value,
                                    row_delta):
    """Return the zero-shift bound that dominates the shifted active sum."""
    if any(type(value) is not int for value in (
            modulus, shift_length, gcd_value, row_delta)):
        raise ValueError("all arguments must be integers")
    if row_delta < 0:
        raise ValueError("row_delta must be nonnegative")
    _require_prime(modulus)
    residue = modulus * row_delta % gcd_value
    bound = triangular_kernel_sum_bound(
        modulus, shift_length, gcd_value)
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "gcd_value": gcd_value,
        "row_delta": row_delta,
        "shifted_residue": residue,
        "proved_absolute_active_kernel_sum_bound": bound,
        "pointwise_shifted_by_zero_class_proved": True,
    }


def row_shifted_triangular_main_bound(modulus, shift_length, divisor_left,
                                      row_delta):
    """Return the unchanged frame Schur bound, now uniform in row_delta."""
    if type(row_delta) is not int or row_delta < 0:
        raise ValueError("row_delta must be a nonnegative integer")
    receipt = row_triangular_main_bound(
        modulus, shift_length, divisor_left)
    return {
        **receipt,
        "row_delta": row_delta,
        "shifted_triangular_main_bound_proved": True,
        "shifted_discrepancy_proved": False,
        "shifted_centering_proved": False,
    }


if __name__ == "__main__":
    modes = _active_modes(1009, 5)
    result = shifted_kernel_active_sum_bound(1009, 5, 14, 7)
    result["exact_shifted_active_absolute_sum"] = sum(abs(
        shifted_triangular_kernel(1009, 14, 1009 * 7 % 14, frequency))
        for frequency in modes)
    for key, value in result.items():
        print(f"{key}: {value}")
