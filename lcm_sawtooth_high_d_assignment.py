"""Three-way prime assignment and residual geometry for high conductors.

For squarefree ``d|lcm(a,b)``, assign each prime of ``d`` uniquely to
``a only``, ``b only``, or ``both`` and write

    d=d_L*d_R*d_C,
    a=d_L*d_C*alpha,  b=d_R*d_C*beta.                  (1)

The three factors are pairwise coprime, ``(alpha*beta,d)=1``, and

    lcm(a,b)=d*lcm(alpha,beta),
    mu(a)mu(b)=mu(d_L*d_R)mu(alpha)mu(beta).            (2)

Consequently the structured primitive coordinate is exactly

    S_d = d^(-1) sum_(d_L*d_R*d_C=d) mu(d_L*d_R)
          sum_(alpha,beta) mu(alpha)mu(beta)L_a L_b
                            /lcm(alpha,beta),           (3)

with the original hard ranges on ``a,b``. Moreover
``lcm(alpha,beta)<=B^2/(d*d_C)<=B^2/d``. This is a short residual modulus
when the dominant primitive conductor ``d`` is near the prime scale.
"""

import math

from lcm_sawtooth_exact_gcd_factorization import (
    _squarefree_divisors_with_complement_mobius,
    sawtooth_gcd_mobius_transform,
)
from lcm_sawtooth_structured_divisor_sum import _coefficient_data
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values


def _squarefree_prime_factors(value):
    if type(value) is not int or value < 1:
        raise ValueError("value must be a positive integer")
    remaining = value
    factors = []
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            factors.append(prime)
            if remaining % prime == 0:
                raise ValueError("value must be squarefree")
        prime += 1 if prime == 2 else 2
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def three_way_prime_assignments(value):
    """Return all ordered ``(d_L,d_R,d_C)`` factorizations in (1)."""
    assignments = [(1, 1, 1)]
    for prime in _squarefree_prime_factors(value):
        assignments = [
            updated
            for left, right, common in assignments
            for updated in (
                (left * prime, right, common),
                (left, right * prime, common),
                (left, right, common * prime),
            )]
    return tuple(assignments)


def high_d_assignment_expansion(
        modulus, ell, divisor_lower, divisor_upper, target_divisor):
    """Compare the direct structured sum with the exact expansion (3)."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper, target_divisor)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus
            or target_divisor < 1 or target_divisor > divisor_upper ** 2):
        raise ValueError("invalid high-d assignment ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")
    factors = _squarefree_prime_factors(target_divisor)
    mobius, divisors, _, lcm_coefficients = _coefficient_data(
        modulus, ell, divisor_lower, divisor_upper)
    direct = sum(coefficient / q
                 for q, coefficient in lcm_coefficients.items()
                 if q % target_divisor == 0)
    X = modulus * ell
    expanded = 0.0
    active_assignments = 0
    maximum_residual_lcm = 0
    for left_part, right_part, common_part in three_way_prime_assignments(
            target_divisor):
        left_base = left_part * common_part
        right_base = right_part * common_part
        assignment_sum = 0.0
        for alpha in range(1, divisor_upper // left_base + 1):
            left = left_base * alpha
            if (not mobius[alpha] or math.gcd(alpha, target_divisor) != 1
                    or left <= divisor_lower):
                continue
            for beta in range(1, divisor_upper // right_base + 1):
                right = right_base * beta
                if (not mobius[beta]
                        or math.gcd(beta, target_divisor) != 1
                        or right <= divisor_lower):
                    continue
                residual_lcm = math.lcm(alpha, beta)
                if math.lcm(left, right) != target_divisor * residual_lcm:
                    raise ArithmeticError("residual lcm identity failed")
                maximum_residual_lcm = max(
                    maximum_residual_lcm, residual_lcm)
                assignment_sum += (
                    int(mobius[alpha]) * int(mobius[beta])
                    * math.log(X / left) * math.log(X / right)
                    / residual_lcm)
        if assignment_sum:
            active_assignments += 1
        expanded += int(mobius[left_part * right_part]) * assignment_sum
    expanded /= target_divisor
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "target_divisor": target_divisor,
        "target_prime_factor_count": len(factors),
        "assignment_count": 3 ** len(factors),
        "active_assignment_count": active_assignments,
        "direct_structured_sum": direct,
        "assignment_expanded_sum": expanded,
        "identity_error": direct - expanded,
        "maximum_residual_lcm": maximum_residual_lcm,
        "residual_lcm_upper_bound": divisor_upper ** 2 / target_divisor,
        "three_way_assignment_identity_proved": True,
        "residual_lcm_bound_proved": True,
        "high_d_structured_sum_bound_proved": False,
    }


def high_d_residual_geometry_probe(
        modulus, ell, divisor_lower, divisor_upper):
    """Locate positive primitive energy by the maximum remaining lcm q/d."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid residual-geometry ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")
    _, divisors, _, lcm_coefficients = _coefficient_data(
        modulus, ell, divisor_lower, divisor_upper)
    if not divisors:
        raise ValueError("the divisor interval has no squarefree values")
    structured_sums = {}
    multiples = {}
    for q, coefficient in lcm_coefficients.items():
        for divisor, _ in _squarefree_divisors_with_complement_mobius(q):
            structured_sums[divisor] = structured_sums.get(divisor, 0.0) + (
                coefficient / q)
            multiples.setdefault(divisor, []).append(q)
    entries = []
    total_energy = 0.0
    for divisor, value in structured_sums.items():
        energy = sawtooth_gcd_mobius_transform(
            modulus, divisor) * value ** 2
        total_energy += energy
        if divisor > divisor_upper and energy > 0:
            entries.append({
                "divisor": divisor,
                "energy": energy,
                "maximum_residual_lcm": max(
                    q // divisor for q in multiples[divisor]),
                "multiple_count": len(set(multiples[divisor])),
            })
    if total_energy <= 0 or not entries:
        raise ArithmeticError("no positive high-d residual energy")
    entries.sort(key=lambda entry: entry["energy"], reverse=True)
    thresholds = (1, 2, 4, 8, 16, 32, 64)
    fractions = {
        threshold: sum(
            entry["energy"] for entry in entries
            if entry["maximum_residual_lcm"] <= threshold) / total_energy
        for threshold in thresholds}
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "total_complete_period_energy": total_energy,
        "high_d_entry_count": len(entries),
        "energy_fraction_by_maximum_residual_lcm": fractions,
        "top_high_d_entries": tuple({
            "divisor": entry["divisor"],
            "energy_fraction": entry["energy"] / total_energy,
            "maximum_residual_lcm": entry["maximum_residual_lcm"],
            "multiple_count": entry["multiple_count"],
        } for entry in entries[:8]),
        "three_way_residual_geometry_measured": True,
        "high_d_structured_sum_bound_proved": False,
    }


def residual_bessel_probe(modulus, ell, divisor_lower, divisor_upper):
    """Evaluate the exact residual-modulus Bessel quotient.

    The numerator is the full complete-period energy and the denominator is
    its diagonal, both written with the same nonnegative primitive weights H_d.
    """
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid residual-Bessel ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")
    _, divisors, _, lcm_coefficients = _coefficient_data(
        modulus, ell, divisor_lower, divisor_upper)
    if not divisors:
        raise ValueError("the divisor interval has no squarefree values")
    residual_terms = {}
    for q, coefficient in lcm_coefficients.items():
        for divisor, _ in _squarefree_divisors_with_complement_mobius(q):
            residual_terms.setdefault(divisor, []).append(coefficient / q)
    numerator = denominator = 0.0
    singleton_numerator = singleton_denominator = 0.0
    multi_numerator = multi_denominator = 0.0
    positive_weight_coordinate_count = 0
    maximum_all_coordinate_residual_count = 0
    maximum_positive_weight_residual_count = 0
    for divisor, terms in residual_terms.items():
        weight = sawtooth_gcd_mobius_transform(modulus, divisor)
        coordinate_numerator = weight * sum(terms) ** 2
        coordinate_denominator = weight * sum(term ** 2 for term in terms)
        numerator += coordinate_numerator
        denominator += coordinate_denominator
        distinct_count = len(terms)
        maximum_all_coordinate_residual_count = max(
            maximum_all_coordinate_residual_count, distinct_count)
        if weight > 0:
            positive_weight_coordinate_count += 1
            maximum_positive_weight_residual_count = max(
                maximum_positive_weight_residual_count, distinct_count)
        if distinct_count == 1:
            singleton_numerator += coordinate_numerator
            singleton_denominator += coordinate_denominator
        else:
            multi_numerator += coordinate_numerator
            multi_denominator += coordinate_denominator
    if denominator <= 0:
        raise ArithmeticError("residual-Bessel diagonal must be positive")
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "primitive_coordinate_count": len(residual_terms),
        "positive_weight_primitive_coordinate_count": (
            positive_weight_coordinate_count),
        "maximum_all_coordinate_residual_support_count": (
            maximum_all_coordinate_residual_count),
        "maximum_positive_weight_residual_support_count": (
            maximum_positive_weight_residual_count),
        "complete_period_energy": numerator,
        "diagonal_energy": denominator,
        "complete_over_diagonal": numerator / denominator,
        "singleton_numerator_fraction": singleton_numerator / numerator,
        "singleton_diagonal_fraction": singleton_denominator / denominator,
        "multi_residual_bessel_ratio": (
            multi_numerator / multi_denominator
            if multi_denominator else 0.0),
        "numerator_component_error": (
            numerator - singleton_numerator - multi_numerator),
        "denominator_component_error": (
            denominator - singleton_denominator - multi_denominator),
        "exact_residual_bessel_reformulation_proved": True,
        "residual_bessel_subpower_bound_proved": False,
    }


if __name__ == "__main__":
    for modulus, ell, lower, upper in (
            (251, 69, 4, 20), (503, 113, 4, 29),
            (1009, 183, 5, 42), (2003, 295, 6, 61),
            (4001, 477, 8, 89), (8009, 774, 9, 130),
            (16001, 1252, 11, 190)):
        result = high_d_residual_geometry_probe(
            modulus, ell, lower, upper)
        print({key: result[key] for key in (
            "modulus", "divisor_range",
            "energy_fraction_by_maximum_residual_lcm",
            "top_high_d_entries")})
        bessel = residual_bessel_probe(modulus, ell, lower, upper)
        print({key: bessel[key] for key in (
            "modulus", "complete_over_diagonal",
            "singleton_numerator_fraction", "singleton_diagonal_fraction",
            "multi_residual_bessel_ratio",
            "maximum_positive_weight_residual_support_count")})
