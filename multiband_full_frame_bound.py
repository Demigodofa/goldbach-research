"""A subpower lower frame for a union of squarefree divisor bands.

Let D={a:V<a<=B, mu(a)^2=1}, x_a=c_a L_a/a, and

 y_d=sum_(a in D,d|a)x_a.

The frozen gcd-feature quadratic form and block totient frame are

 P0=sum_(d>1)phi(d)|y_d|^2,
 F=sum_(a in D)phi(a)|x_a|^2.                            (1)

Finite Mobius inversion over multiples gives

 x_a=sum_(k<=B/a)mu(k)y_(ak).                           (2)

Weighted Cauchy with weights 1/k gives

 |x_a|^2 <= H_(floor(B/V))
   sum_(k<=B/a)mu(k)^2 k|y_(ak)|^2.                     (3)

After d=ak, define

 C_D=max_(1<d<=B) phi(d)^(-1)
   sum_(a in D,a|d,mu(d/a)^2=1) phi(a)d/a.              (4)

Then (1)--(4) prove the explicit Loewner bound

 P0 >= F/[H_(floor(B/V)) C_D].                          (5)

Since C_D<=N^eps and H<=1+log N, this is P0>=N^-eps F.
The exact-minus-frozen entry bound from ``near_cutoff_full_frame_bound.py``
has normalized Schur norm

 eta <<_eps N^eps(B^2/m+B/l).                           (6)

For B<=N^(.245-delta), m=N^.59, and l=N^.41, (6) is a
power saving relative to (5).  Hence the exact full Gram satisfies
G>=N^-eps F after renaming eps.  This is a subpower coercivity theorem, not a
constant lower frame.
"""

import math

import numpy as np

from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from multiband_full_frame_probe import multiband_full_frame_probe
from near_cutoff_full_frame_bound import entry_error_bound


def _harmonic(number):
    return sum(1 / value for value in range(1, number + 1))


def multiband_full_frame_bound(modulus, ell,
                               divisor_lower, divisor_upper,
                               compare_exact=False):
    """Return the explicit inversion and perturbation certificates."""
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
    divisor_set = set(divisors)
    harmonic = _harmonic(divisor_upper // (divisor_lower + 1))
    feature_coefficient = 0.0
    feature_worst = None
    for feature in range(2, divisor_upper + 1):
        coefficient = 0.0
        for divisor in divisors:
            if feature % divisor == 0:
                quotient = feature // divisor
                if mobius[quotient]:
                    coefficient += _totient(divisor) * quotient
        normalized = coefficient / _totient(feature)
        if normalized > feature_coefficient:
            feature_coefficient = normalized
            feature_worst = feature
    ideal_lower = 1 / (harmonic * feature_coefficient)

    logs = {a: math.log(modulus * ell / a) for a in divisors}
    frame = {
        a: modulus ** 2 * logs[a] ** 2 * _totient(a) / a ** 2
        for a in divisors
    }
    perturbation_rows = tuple(sum(
        entry_error_bound(modulus, ell, left, right)
        / math.sqrt(frame[left] * frame[right])
        for right in divisors)
        for left in divisors)
    perturbation = max(perturbation_rows)
    result = {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "divisor_count": len(divisor_set),
        "harmonic_factor": harmonic,
        "feature_coefficient": feature_coefficient,
        "worst_feature": feature_worst,
        "proved_ideal_over_block_frame_lower": ideal_lower,
        "normalized_exact_minus_ideal_schur_bound": perturbation,
        "proved_exact_over_block_frame_lower": ideal_lower - perturbation,
        "finite_positive_exact_lower_frame": perturbation < ideal_lower,
        "asymptotic_subpower_multiband_lower_frame_proved": True,
        "constant_lower_frame_proved": False,
    }
    if compare_exact:
        exact = multiband_full_frame_probe(
            modulus, ell, divisor_lower, divisor_upper)
        result["actual_ideal_over_block_frame_min"] = (
            exact["ideal_over_block_frame_min"])
        result["actual_exact_over_block_frame_min"] = (
            exact["exact_over_block_frame_min"])
    return result


if __name__ == "__main__":
    for key, value in multiband_full_frame_bound(
            1009, 9, 8, 64, compare_exact=True).items():
        print(f"{key}: {value}")
