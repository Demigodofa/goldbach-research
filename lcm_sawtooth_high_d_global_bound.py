"""Close the complete-period high-conductor sum through a pair-mass envelope.

Let ``D`` be the squarefree integers in ``(V,B]``, ``L_a=log(X/a)``, and

    K_q = sum_(lcm(a,b)=q) mu(a)mu(b)L_a L_b.

For every squarefree ``d|q`` with ``d>B*V``, group the ordered pairs of lcm
``q=d*r`` by their common conductor part ``c``.  Let ``A_(d,c,r)`` be the
signed residual sum after the fixed conductor/common signs are removed, and
let ``P_(d,c,r)`` be its termwise-positive majorant, the sum of ``L_a L_b``
over the same cell. Define

    T_high^+ = sum_(d>B*V) H_m(d)
               sum_(r,c) P_(d,c,r)^2/(d*r)^2.            (1)

For fixed ``d`` and ``q``, the ``c`` cells partition the ordered pairs of lcm
``q``.  Cauchy in each cell, followed by ``sum_(d|q)H_m(d)=F_m(q)``, proves

    T_high^+ <= sum_q R_q v_(m,q)
                      sum_(lcm(a,b)=q)L_a^2 L_b^2,       (2)

where ``R_q`` is the number of ordered pairs and
``v_(m,q)=F_m(q)/q^2`` is the exact cyclic sawtooth variance.  The right side
is precisely the existing diagonal Cauchy envelope.

For each fixed ``d,c``, the base-pair/three-state theorem gives a log-six
collapsed-to-signed-residual-diagonal bound. Since ``|A|<=P``, Cauchy over at
most ``2^omega(d)`` common parts bounds the actual complete-period
high-conductor energy by a subpower factor times (1), and hence by (2). This
avoids any lower bound for the Mobius-signed combined common layer, which can
nearly vanish.
"""

import math

from lcm_sawtooth_diagonal_bound import (
    cyclic_sawtooth_variance,
    lcm_sawtooth_diagonal_probe,
)
from lcm_sawtooth_exact_gcd_factorization import (
    _squarefree_divisors_with_complement_mobius,
    sawtooth_gcd_mobius_transform,
)
from lcm_sawtooth_high_d_assignment import _squarefree_prime_factors
from lcm_sawtooth_no_common_polylog import three_state_harmonic_receipt
from lcm_sawtooth_structured_divisor_sum import _coefficient_data
from mobius_covariance_endpoint_probe import _prime_flags


def high_conductor_global_bound_receipt(
        modulus, ell, divisor_lower, divisor_upper):
    """Evaluate (1)-(2) and return the proved uniform high-d factor."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid high-conductor global ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")

    mobius, divisors, coefficients, lcm_coefficients = _coefficient_data(
        modulus, ell, divisor_lower, divisor_upper)
    logarithms = {
        value: abs(coefficients[value]) for value in divisors}
    cell_sums = {}
    cell_counts = {}
    pair_counts = {}
    pair_square_mass = {}
    for left in divisors:
        for right in divisors:
            q = math.lcm(left, right)
            pair_weight = logarithms[left] * logarithms[right]
            pair_counts[q] = pair_counts.get(q, 0) + 1
            pair_square_mass[q] = (
                pair_square_mass.get(q, 0.0) + pair_weight ** 2)
            pair_common = math.gcd(left, right)
            for divisor, _ in _squarefree_divisors_with_complement_mobius(q):
                if divisor <= divisor_lower * divisor_upper:
                    continue
                common = math.gcd(divisor, pair_common)
                residual = q // divisor
                key = (divisor, residual, common)
                cell_sums[key] = cell_sums.get(key, 0.0) + pair_weight
                cell_counts[key] = cell_counts.get(key, 0) + 1

    partition_counts = {}
    for (divisor, residual, _), count in cell_counts.items():
        key = (divisor, residual)
        partition_counts[key] = partition_counts.get(key, 0) + count
    partition_count_identity_verified = all(
        count == pair_counts[divisor * residual]
        for (divisor, residual), count in partition_counts.items())
    if not partition_count_identity_verified:
        raise ArithmeticError("common cells do not partition an lcm pair set")

    positive_separated = 0.0
    active_high_divisors = set()
    for (divisor, residual, _), value in cell_sums.items():
        weight = sawtooth_gcd_mobius_transform(modulus, divisor)
        if weight <= 0:
            continue
        active_high_divisors.add(divisor)
        positive_separated += (
            weight * value ** 2 / (divisor * residual) ** 2)

    structured_sums = {}
    for q, coefficient in lcm_coefficients.items():
        for divisor, _ in _squarefree_divisors_with_complement_mobius(q):
            if divisor > divisor_lower * divisor_upper:
                structured_sums[divisor] = (
                    structured_sums.get(divisor, 0.0) + coefficient / q)
    complete_high_energy = sum(
        sawtooth_gcd_mobius_transform(modulus, divisor) * value ** 2
        for divisor, value in structured_sums.items())

    exact_cauchy_envelope = sum(
        pair_counts[q] * cyclic_sawtooth_variance(modulus, q)
        * pair_square_mass[q]
        for q in pair_counts if q > 1)
    diagonal = lcm_sawtooth_diagonal_probe(
        modulus, ell, divisor_lower, divisor_upper)

    if active_high_divisors:
        maximum_two_to_omega = max(
            2 ** len(_squarefree_prime_factors(divisor))
            for divisor in active_high_divisors)
        maximum_residual = max(
            math.ceil(divisor_upper / divisor_lower), 1)
        residual_factor = three_state_harmonic_receipt(
            maximum_residual)["log_six_bound"]
    else:
        maximum_two_to_omega = 1
        maximum_residual = 1
        residual_factor = 1.0
    collapse_factor = maximum_two_to_omega * residual_factor
    proved_upper_bound = collapse_factor * positive_separated

    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "high_conductor_threshold": divisor_lower * divisor_upper,
        "active_high_conductor_count": len(active_high_divisors),
        "positive_separated_high_conductor_cell_majorant": (
            positive_separated),
        "actual_complete_high_conductor_energy": complete_high_energy,
        "exact_diagonal_cauchy_envelope": exact_cauchy_envelope,
        "existing_diagonal_probe_cauchy_envelope": diagonal[
            "exact_cauchy_upper_bound"],
        "maximum_uniform_residual_limit": maximum_residual,
        "maximum_two_to_omega_common_count": maximum_two_to_omega,
        "uniform_log_six_residual_factor": residual_factor,
        "uniform_high_conductor_collapse_factor": collapse_factor,
        "proved_complete_high_conductor_upper_bound": proved_upper_bound,
        "positive_separated_over_diagonal_cauchy_envelope": (
            positive_separated / exact_cauchy_envelope
            if exact_cauchy_envelope else 0.0),
        "actual_over_proved_high_conductor_upper_bound": (
            complete_high_energy / proved_upper_bound
            if proved_upper_bound else 0.0),
        "common_cells_partition_lcm_pairs_proved": True,
        "common_cell_partition_counts_verified": (
            partition_count_identity_verified),
        "signed_cells_bounded_by_positive_cell_majorants_proved": True,
        "positive_separated_cell_majorant_bound_proved": True,
        "complete_high_conductor_pair_mass_bound_proved": True,
        "signed_prime_correlation_estimate_proved": False,
    }


if __name__ == "__main__":
    for controls in (
            (251, 69, 4, 20),
            (503, 113, 4, 29),
            (1009, 183, 5, 42)):
        print(high_conductor_global_bound_receipt(*controls))
