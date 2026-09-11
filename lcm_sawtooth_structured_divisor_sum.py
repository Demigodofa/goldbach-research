"""Expand the primitive-frequency divisor sums in the original coefficients.

Let ``c_a=mu(a)log(X/a)`` on the squarefree interval ``D=(V,B]`` and

    K_q=sum_(lcm(a,b)=q)c_a*c_b,
    S_d=sum_(d|q)K_q/q.                                  (1)

For squarefree ``d``, inclusion-exclusion and
``gcd(a,b)=sum_(e|a,e|b)phi(e)`` give the exact identity

    S_d = sum_(k|d) mu(k) sum_e phi(e)
            [sum_(a in D,e|a,(a,k)=1)c_a/a]^2.          (2)

Thus the complete-period energy is the positive dyadic sum
``sum_d H_m(d)S_d^2``, with ``H_m`` from the primitive-frequency
factorization. Formula (2) retains the previous polynomial/divisibility tools
inside the new arithmetic mechanism; it does not estimate the truncated
Mobius sums.
"""

import math

from divisor_full_frame_probe import _totient
from lcm_sawtooth_exact_gcd_factorization import (
    _squarefree_divisors_with_complement_mobius,
    sawtooth_gcd_mobius_transform,
)
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values


def _coefficient_data(modulus, ell, divisor_lower, divisor_upper):
    mobius = _mobius_values(max(divisor_upper, divisor_upper ** 2))
    divisors = tuple(
        value for value in range(divisor_lower + 1, divisor_upper + 1)
        if mobius[value])
    X = modulus * ell
    coefficients = {
        value: int(mobius[value]) * math.log(X / value)
        for value in divisors}
    lcm_coefficients = {}
    for left in divisors:
        for right in divisors:
            q = math.lcm(left, right)
            lcm_coefficients[q] = lcm_coefficients.get(q, 0.0) + (
                coefficients[left] * coefficients[right])
    return mobius, divisors, coefficients, lcm_coefficients


def structured_divisor_sum_expansion(
        modulus, ell, divisor_lower, divisor_upper, target_divisor):
    """Evaluate the direct side of (1) and expanded side of (2)."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper, target_divisor)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus
            or target_divisor < 1):
        raise ValueError("invalid structured-sum ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")
    mobius, divisors, coefficients, lcm_coefficients = _coefficient_data(
        modulus, ell, divisor_lower, divisor_upper)
    if not divisors:
        raise ValueError("the divisor interval has no squarefree values")
    if target_divisor >= len(mobius) or not mobius[target_divisor]:
        raise ValueError("target_divisor must be squarefree and at most B^2")
    direct = sum(value / q for q, value in lcm_coefficients.items()
                 if q % target_divisor == 0)
    expanded = 0.0
    for subset, _ in _squarefree_divisors_with_complement_mobius(
            target_divisor):
        inner_energy = 0.0
        for common in range(1, divisor_upper + 1):
            inner = sum(
                coefficients[value] / value for value in divisors
                if value % common == 0 and math.gcd(value, subset) == 1)
            inner_energy += _totient(common) * inner ** 2
        expanded += int(mobius[subset]) * inner_energy
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "target_divisor": target_divisor,
        "direct_structured_sum": direct,
        "expanded_structured_sum": expanded,
        "identity_error": direct - expanded,
        "original_divisor_expansion_proved": True,
        "structured_sum_asymptotic_bound_proved": False,
    }


def structured_divisor_energy_probe(
        modulus, ell, divisor_lower, divisor_upper):
    """Partition the exact positive energy ``sum_d H_m(d)S_d^2`` dyadically."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid structured-energy ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")
    _, divisors, _, lcm_coefficients = _coefficient_data(
        modulus, ell, divisor_lower, divisor_upper)
    if not divisors:
        raise ValueError("the divisor interval has no squarefree values")
    structured_sums = {}
    for q, coefficient in lcm_coefficients.items():
        for divisor, _ in _squarefree_divisors_with_complement_mobius(q):
            structured_sums[divisor] = structured_sums.get(divisor, 0.0) + (
                coefficient / q)
    dyadic_energy = {}
    low_energy = high_energy = total_energy = 0.0
    for divisor, value in structured_sums.items():
        contribution = sawtooth_gcd_mobius_transform(
            modulus, divisor) * value ** 2
        block = divisor.bit_length() - 1
        dyadic_energy[block] = dyadic_energy.get(block, 0.0) + contribution
        total_energy += contribution
        if divisor <= divisor_upper:
            low_energy += contribution
        else:
            high_energy += contribution
    active_blocks = {block: value for block, value in dyadic_energy.items()
                     if value > 0}
    if total_energy <= 0 or not active_blocks:
        raise ArithmeticError(
            "structured divisor support has zero complete-period energy")
    largest_block = max(active_blocks, key=active_blocks.get)
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "transform_divisor_count": len(structured_sums),
        "positive_complete_period_energy": total_energy,
        "low_d_energy_fraction": low_energy / total_energy,
        "high_d_energy_fraction": high_energy / total_energy,
        "dyadic_energy_fractions": {
            block: value / total_energy
            for block, value in sorted(active_blocks.items())},
        "largest_dyadic_block": (
            2 ** largest_block, 2 ** (largest_block + 1)),
        "largest_dyadic_energy_fraction": (
            active_blocks[largest_block] / total_energy),
        "positive_dyadic_factorization_proved": True,
        "dyadic_structured_sum_bound_proved": False,
    }


if __name__ == "__main__":
    for modulus, ell, lower, upper in (
            (251, 69, 4, 20), (503, 113, 4, 29),
            (1009, 183, 5, 42), (2003, 295, 6, 61),
            (4001, 477, 8, 89), (8009, 774, 9, 130),
            (16001, 1252, 11, 190)):
        result = structured_divisor_energy_probe(
            modulus, ell, lower, upper)
        print({key: result[key] for key in (
            "modulus", "divisor_range", "low_d_energy_fraction",
            "high_d_energy_fraction", "largest_dyadic_block",
            "largest_dyadic_energy_fraction")})
