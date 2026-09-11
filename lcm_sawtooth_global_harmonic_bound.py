"""Bound the entire complete-period conductor sum by residual harmonic mass.

For one three-way conductor assignment, write

    T = sum_(alpha,beta) eps_(alpha,beta) W_(alpha,beta)
                              /lcm(alpha,beta),

where ``|eps|<=1`` and ``W=L_a L_b>=0``. Weighted Cauchy gives

    |T|^2 <= [sum W^2/lcm(alpha,beta)]
             [sum 1/lcm(alpha,beta)].                    (1)

For any rectangular upper bounds ``alpha<=A``, ``beta<=C``, the gcd divisor
identity proves

    sum 1/lcm(alpha,beta)
      = sum_e phi(e)/e^2 H_floor(A/e) H_floor(C/e)
      <= H_A H_C H_min(A,C).                             (2)

Restrictions from squarefreeness, coprimality, and the hard lower endpoint
only decrease the positive second factor.

There are ``3^omega(d)`` conductor assignments.  In the primitive-frequency
sum, ``0<=H_m(d)<=F_m(d)<=m*d``.  A pair of lcm ``q`` appears once for each
``d|q``, and

    sum_(d|q) 3^omega(d) = 4^omega(q).                   (3)

Equations (1)-(3) therefore bound the full complete-period energy by

    m H_B^3 max_(q)4^omega(q)
      sum_(a,b) L_a^2 L_b^2/lcm(a,b).                   (4)

The last pair mass is the existing totient-divisor identity.  Every extra
factor in (4) is subpower in the project range.  This controls all primitive
conductors at once and does not require a retained residual base pair.
"""

import math

from divisor_full_frame_probe import _totient
from lcm_sawtooth_exact_gcd_factorization import (
    _squarefree_divisors_with_complement_mobius,
    lcm_sawtooth_exact_gcd_factorization_probe,
    sawtooth_gcd_kernel_numerator,
    sawtooth_gcd_mobius_transform,
)
from lcm_sawtooth_high_d_assignment import _squarefree_prime_factors
from lcm_sawtooth_structured_divisor_sum import _coefficient_data
from mobius_covariance_endpoint_probe import _prime_flags


def rectangular_lcm_harmonic_receipt(left_limit, right_limit):
    """Evaluate the exact sum in (2) and its triple-harmonic bound."""
    if (type(left_limit) is not int or type(right_limit) is not int
            or left_limit < 1 or right_limit < 1):
        raise ValueError("limits must be positive integers")
    direct = sum(
        1 / math.lcm(left, right)
        for left in range(1, left_limit + 1)
        for right in range(1, right_limit + 1))
    expanded = 0.0
    for common in range(1, min(left_limit, right_limit) + 1):
        expanded += (_totient(common) / common ** 2
                     * sum(1 / value for value in range(
                         1, left_limit // common + 1))
                     * sum(1 / value for value in range(
                         1, right_limit // common + 1)))
    left_harmonic = sum(1 / value for value in range(1, left_limit + 1))
    right_harmonic = sum(1 / value for value in range(1, right_limit + 1))
    minimum_harmonic = sum(
        1 / value for value in range(
            1, min(left_limit, right_limit) + 1))
    bound = left_harmonic * right_harmonic * minimum_harmonic
    return {
        "limits": (left_limit, right_limit),
        "direct_lcm_harmonic_sum": direct,
        "gcd_expanded_lcm_harmonic_sum": expanded,
        "triple_harmonic_bound": bound,
        "rectangular_lcm_harmonic_identity_proved": True,
        "triple_harmonic_bound_proved": True,
    }


def global_complete_period_harmonic_bound_receipt(
        modulus, ell, divisor_lower, divisor_upper):
    """Evaluate every term in the global bound (4)."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid global harmonic ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")

    _, divisors, coefficients, lcm_coefficients = _coefficient_data(
        modulus, ell, divisor_lower, divisor_upper)
    logarithms = {value: abs(coefficients[value]) for value in divisors}
    reciprocal_pair_mass = sum(
        logarithms[left] ** 2 * logarithms[right] ** 2
        / math.lcm(left, right)
        for left in divisors for right in divisors)
    maximum_four_to_omega = max(
        4 ** len(_squarefree_prime_factors(q))
        for q in lcm_coefficients)
    harmonic_B = sum(
        1 / value for value in range(1, divisor_upper + 1))
    proved_bound = (
        modulus * harmonic_B ** 3 * maximum_four_to_omega
        * reciprocal_pair_mass)

    primitive_divisors = {
        divisor
        for q in lcm_coefficients
        for divisor, _ in _squarefree_divisors_with_complement_mobius(q)}
    maximum_h_over_md = max(
        sawtooth_gcd_mobius_transform(modulus, divisor)
        / (modulus * divisor)
        for divisor in primitive_divisors)
    h_bounded_by_f = all(
        sawtooth_gcd_mobius_transform(modulus, divisor)
        <= sawtooth_gcd_kernel_numerator(modulus, divisor)
        for divisor in primitive_divisors)

    exact = lcm_sawtooth_exact_gcd_factorization_probe(
        modulus, ell, divisor_lower, divisor_upper)
    exact_energy = exact["exact_signed_complete_energy"]
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "exact_complete_period_energy": exact_energy,
        "reciprocal_lcm_pair_mass": reciprocal_pair_mass,
        "harmonic_B": harmonic_B,
        "maximum_four_to_omega": maximum_four_to_omega,
        "maximum_H_m_over_m_d": maximum_h_over_md,
        "proved_global_harmonic_upper_bound": proved_bound,
        "actual_over_proved_global_bound": exact_energy / proved_bound,
        "primitive_weight_bounded_by_F_verified": h_bounded_by_f,
        "residual_weighted_cauchy_proved": True,
        "primitive_weight_H_m_le_m_d_proved": True,
        "assignment_divisor_sum_four_to_omega_proved": True,
        "global_complete_period_harmonic_bound_proved": True,
        "incomplete_row_covariance_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
    }


if __name__ == "__main__":
    for controls in (
            (251, 69, 4, 20),
            (503, 113, 4, 29),
            (1009, 183, 5, 42)):
        print(global_complete_period_harmonic_bound_receipt(*controls))
