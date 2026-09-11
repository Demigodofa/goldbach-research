"""Falsify uniform weighted bounds with the exact covariance operator.

The sparse gcd majorant is useful on the actual Mobius vector, but it cannot
obey a uniform inequality relative to

    D_m(x)=sum_q |x_q|^2 v_(m,q).

Indeed ``q|(m-1)`` gives ``v_(m,q)=0`` while the coarse gcd majorant retains
the diagonal ``1/4``.  The true covariance row is identically zero there.

After deleting zero-variance coordinates, the correct absolute normalized
operator is

    R_(q,r)=|Cov_m(q,r)|/sqrt(v_(m,q)v_(m,r)).           (1)

Its largest eigenvalue is the sharp constant for the exact absolute
covariance form on the chosen lcm support.  This finite probe compares that
resonant direction with the actual Mobius coefficient vector.
"""

import math

import numpy as np

from lcm_sawtooth_cross_covariance import cyclic_sawtooth_covariance
from lcm_sawtooth_incomplete_covariance import (
    _evaluate_polynomial,
    _lcm_coefficient_polynomials,
)
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values


def lcm_sawtooth_normalized_operator_probe(
        modulus, ell, divisor_lower, divisor_upper):
    """Return the exact absolute-covariance generalized eigenvalue."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid normalized-operator ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")
    mobius = _mobius_values(divisor_upper)
    divisors = tuple(
        value for value in range(divisor_lower + 1, divisor_upper + 1)
        if mobius[value])
    if not divisors:
        raise ValueError("the divisor interval has no squarefree values")
    polynomials = _lcm_coefficient_polynomials(divisors, mobius)
    logarithm = math.log(modulus * ell)
    coefficients = {
        q: float(_evaluate_polynomial(polynomial, logarithm))
        for q, polynomial in polynomials.items()}
    variances = {
        q: float(cyclic_sawtooth_covariance(
            modulus, q, q)["covariance"])
        for q in coefficients}
    zero_variance_periods = tuple(
        q for q, variance in variances.items() if variance == 0)
    periods = tuple(q for q in coefficients if variances[q] > 0)
    if not periods:
        raise ArithmeticError("lcm support has no positive-variance periods")
    size = len(periods)
    signed = np.empty((size, size), dtype=float)
    absolute = np.empty((size, size), dtype=float)
    for left_index, left in enumerate(periods):
        for right_index in range(left_index, size):
            right = periods[right_index]
            covariance = float(cyclic_sawtooth_covariance(
                modulus, left, right)["covariance"])
            normalized = covariance / math.sqrt(
                variances[left] * variances[right])
            signed[left_index, right_index] = normalized
            signed[right_index, left_index] = normalized
            absolute[left_index, right_index] = abs(normalized)
            absolute[right_index, left_index] = abs(normalized)
    eigenvalues, eigenvectors = np.linalg.eigh(absolute)
    largest_eigenvalue = float(eigenvalues[-1])
    extremizer = eigenvectors[:, -1]
    actual_vector = np.array([
        coefficients[q] * math.sqrt(variances[q]) for q in periods],
        dtype=float)
    actual_norm_square = float(actual_vector @ actual_vector)
    signed_rayleigh = float(
        actual_vector @ signed @ actual_vector / actual_norm_square)
    absolute_rayleigh = float(
        np.abs(actual_vector) @ absolute @ np.abs(actual_vector)
        / actual_norm_square)
    overlap = float((np.abs(actual_vector) @ extremizer) ** 2
                    / actual_norm_square)
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "distinct_lcm_count": len(coefficients),
        "positive_variance_lcm_count": size,
        "zero_variance_lcm_count": len(zero_variance_periods),
        "zero_variance_periods": zero_variance_periods,
        "coarse_gcd_uniform_operator_bound_falsified": bool(
            zero_variance_periods),
        "absolute_normalized_operator_eigenvalue": largest_eigenvalue,
        "actual_mobius_signed_rayleigh_ratio": signed_rayleigh,
        "actual_mobius_absolute_rayleigh_ratio": absolute_rayleigh,
        "actual_mobius_extremizer_squared_overlap": overlap,
        "exact_normalized_operator_computed": True,
        "normalized_operator_subpower_bound_proved": False,
    }


if __name__ == "__main__":
    for modulus, ell, lower, upper in (
            (251, 69, 4, 20),
            (503, 113, 4, 29),
            (1009, 183, 5, 42),
            (2003, 295, 6, 61)):
        print(lcm_sawtooth_normalized_operator_probe(
            modulus, ell, lower, upper))
