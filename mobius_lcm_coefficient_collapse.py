"""Measure exact Mobius cancellation after grouping divisor pairs by lcm.

For squarefree ``q`` and ``L=log X``, the complete divisor cube satisfies

    sum_(lcm(a,b)=q) mu(a)mu(b) log(X/a)log(X/b)
      = mu(q) [L^2-sum_(p|q)(log p)^2].                 (1)

Indeed the bivariate local factor is
``-exp(u log p)-exp(v log p)+exp((u+v)log p)``.  At the origin its two first
derivatives vanish, while its mixed derivative contributes ``-(log p)^2``
relative to the local value ``-1``.  Formula (1) keeps the project polynomial
log weights and collapses a three-choice-per-prime pair sum to one coefficient.

The actual lower union ``V<a,b<=B`` truncates the divisor cube, especially
when ``q>B``.  The finite probe below groups that exact coefficient and
measures whether its L1 mass behaves more like the lcm count or the raw pair
count.  It is a falsifier, not an asymptotic Mobius estimate.
"""

import math

from mobius_covariance_lag_probe import _mobius_values
from mobius_covariance_endpoint_probe import _prime_flags


def _squarefree_prime_factors(value):
    factors = []
    remaining = value
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            factors.append(prime)
            if remaining % prime == 0:
                raise ValueError("q must be squarefree")
        prime += 1 if prime == 2 else 2
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def complete_lcm_log_coefficient(q, X):
    """Return the closed form (1)."""
    if type(q) is not int or q < 1:
        raise ValueError("q must be a positive integer")
    if isinstance(X, bool) or not isinstance(X, (int, float)) or X <= q:
        raise ValueError("X must be real and greater than q")
    factors = _squarefree_prime_factors(q)
    mobius = -1 if len(factors) % 2 else 1
    return mobius * (
        math.log(X) ** 2 - sum(math.log(prime) ** 2 for prime in factors))


def mobius_lcm_collapse_probe(X, divisor_lower, divisor_upper):
    """Group the exact truncated pair coefficient by its lcm."""
    if (isinstance(X, bool) or not isinstance(X, (int, float))
            or X <= divisor_upper):
        raise ValueError("X must be real and exceed the divisor range")
    if (type(divisor_lower) is not int or type(divisor_upper) is not int
            or divisor_lower < 1 or divisor_upper <= divisor_lower):
        raise ValueError("invalid divisor range")
    mobius = _mobius_values(divisor_upper)
    divisors = tuple(
        value for value in range(divisor_lower + 1, divisor_upper + 1)
        if mobius[value])
    if not divisors:
        raise ValueError("the divisor interval has no squarefree values")
    logarithms = {value: math.log(X / value) for value in divisors}
    groups = {}
    raw_pair_l1 = 0.0
    for left in divisors:
        left_coefficient = mobius[left] * logarithms[left]
        for right in divisors:
            coefficient = (left_coefficient * mobius[right]
                           * logarithms[right])
            q = math.lcm(left, right)
            groups[q] = groups.get(q, 0.0) + coefficient
            raw_pair_l1 += abs(coefficient)
    grouped_low_l1 = sum(
        abs(value) for q, value in groups.items() if q <= divisor_upper)
    grouped_high_l1 = sum(
        abs(value) for q, value in groups.items() if q > divisor_upper)
    grouped_l1 = grouped_low_l1 + grouped_high_l1
    log_scale = math.log(X) ** 2
    return {
        "X": float(X),
        "divisor_range": (divisor_lower, divisor_upper),
        "divisor_count": len(divisors),
        "raw_pair_l1": raw_pair_l1,
        "grouped_lcm_l1": grouped_l1,
        "grouped_lcm_l1_over_log_X_squared": grouped_l1 / log_scale,
        "grouped_lcm_l1_over_raw_pair_l1": grouped_l1 / raw_pair_l1,
        "grouped_low_lcm_l1": grouped_low_l1,
        "grouped_high_lcm_l1": grouped_high_l1,
        "grouped_high_lcm_l1_over_log_X_squared":
            grouped_high_l1 / log_scale,
        "high_lcm_fraction_of_grouped_l1": grouped_high_l1 / grouped_l1,
        "distinct_lcm_count": len(groups),
        "mobius_lcm_collapse_asymptotic_proved": False,
    }


def mobius_lcm_signed_count_probe(
        modulus, ell, divisor_lower, divisor_upper):
    """Correlate grouped Mobius coefficients with exact CRT count errors."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid signed-count ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")
    X = modulus * ell
    mobius = _mobius_values(divisor_upper)
    divisors = tuple(
        value for value in range(divisor_lower + 1, divisor_upper + 1)
        if mobius[value])
    if not divisors:
        raise ValueError("the divisor interval has no squarefree values")
    logarithms = {value: math.log(X / value) for value in divisors}
    groups = {}
    frame_base = 0.0
    for value in divisors:
        phi = value
        remaining = value
        prime = 2
        while prime * prime <= remaining:
            if remaining % prime == 0:
                phi -= phi // prime
                while remaining % prime == 0:
                    remaining //= prime
            prime += 1 if prime == 2 else 2
        if remaining > 1:
            phi -= phi // remaining
        frame_base += phi * logarithms[value] ** 2 / value ** 2
    for left in divisors:
        left_coefficient = mobius[left] * logarithms[left]
        for right in divisors:
            q = math.lcm(left, right)
            groups[q] = groups.get(q, 0.0) + (
                left_coefficient * mobius[right] * logarithms[right])

    signed = absolute = 0.0
    cyclic_signed = cyclic_absolute = 0.0
    low_signed = high_signed = 0.0
    low_absolute = high_absolute = 0.0
    interval_right = modulus * (ell + 1) - 1
    for q, coefficient in groups.items():
        count = interval_right // q - X // q
        discrepancy = count - modulus / q
        cyclic_discrepancy = count - (modulus - 1) / q
        term = coefficient * discrepancy
        cyclic_term = coefficient * cyclic_discrepancy
        signed += term
        absolute += abs(term)
        cyclic_signed += cyclic_term
        cyclic_absolute += abs(cyclic_term)
        if q <= divisor_upper:
            low_signed += term
            low_absolute += abs(term)
        else:
            high_signed += term
            high_absolute += abs(term)
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "divisor_count": len(divisors),
        "signed_grouped_count_error": signed,
        "absolute_grouped_count_error": absolute,
        "signed_to_absolute_count_error_ratio": (
            signed / absolute if absolute else 0.0),
        "cyclic_signed_grouped_count_error": cyclic_signed,
        "cyclic_absolute_grouped_count_error": cyclic_absolute,
        "cyclic_signed_to_absolute_ratio": (
            cyclic_signed / cyclic_absolute if cyclic_absolute else 0.0),
        "low_lcm_signed_count_error": low_signed,
        "high_lcm_signed_count_error": high_signed,
        "low_lcm_absolute_count_error": low_absolute,
        "high_lcm_absolute_count_error": high_absolute,
        "frozen_count_error_over_totient_frame":
            signed / (modulus * frame_base),
        "signed_lcm_count_cancellation_proved": False,
    }


if __name__ == "__main__":
    print(mobius_lcm_collapse_probe(123407, 5, 42))
