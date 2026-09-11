"""Exact complete-period covariance for two cyclic CRT sawteeth.

For ``gcd(m,q)=1`` put ``s_q=(m-1) mod q`` and

    d_(m,q)(ell)
      = floor((m*ell+m-1)/q)-floor(m*ell/q)-(m-1)/q.

This is the centered indicator that ``m*ell mod q`` lies in the final
``s_q`` residue classes.  For ``g=gcd(q,r)``, let ``n_t`` and ``p_t`` count
those final intervals modulo ``g``.  Averaging over a complete common period
``lcm(q,r)`` gives the exact CRT formula

    Cov(q,r) = [g*sum_t n_t*p_t-s_q*s_r]/(q*r).          (1)

Writing ``n_t=s_q/g+e_t`` and ``p_t=s_r/g+f_t`` proves

    |Cov(q,r)| <= g^2/(4*q*r).                           (2)

In particular coprime moduli have zero covariance.  Thus complete-period
cross terms are supported only on shared prime factors.  This does not bound
the boundary term from the project's incomplete row interval.
"""

import math

from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values


def _terminal_residue_counts(length, modulus, residue_modulus):
    """Count residues modulo ``residue_modulus`` in the last ``length`` slots."""
    quotient, remainder = divmod(length, residue_modulus)
    counts = [quotient] * residue_modulus
    first_residue = (modulus - length) % residue_modulus
    for offset in range(remainder):
        counts[(first_residue + offset) % residue_modulus] += 1
    return tuple(counts)


def cyclic_sawtooth_covariance(modulus, left_period, right_period):
    """Return the exact covariance (1) and its deterministic bounds."""
    if any(type(value) is not int for value in (
            modulus, left_period, right_period)):
        raise ValueError("all inputs must be integers")
    if modulus < 2 or left_period < 2 or right_period < 2:
        raise ValueError("all inputs must be at least two")
    common_period = math.lcm(left_period, right_period)
    if math.gcd(modulus, common_period) != 1:
        raise ValueError("modulus must be coprime to both periods")

    common = math.gcd(left_period, right_period)
    left_length = (modulus - 1) % left_period
    right_length = (modulus - 1) % right_period
    left_counts = _terminal_residue_counts(
        left_length, left_period, common)
    right_counts = _terminal_residue_counts(
        right_length, right_period, common)
    compatible_pairs = sum(
        left * right for left, right in zip(left_counts, right_counts))
    covariance = (
        common * compatible_pairs - left_length * right_length
    ) / (left_period * right_period)
    left_variance = (left_length / left_period) * (
        1 - left_length / left_period)
    right_variance = (right_length / right_period) * (
        1 - right_length / right_period)
    gcd_bound = common ** 2 / (
        4 * left_period * right_period)
    cauchy_bound = math.sqrt(left_variance * right_variance)
    return {
        "modulus": modulus,
        "periods": (left_period, right_period),
        "common_period": common_period,
        "gcd": common,
        "terminal_lengths": (left_length, right_length),
        "compatible_pair_count": compatible_pairs,
        "covariance": covariance,
        "gcd_covariance_bound": gcd_bound,
        "cauchy_covariance_bound": cauchy_bound,
        "coprime_covariance_zero": common != 1 or covariance == 0,
        "complete_period_covariance_proved": True,
        "incomplete_row_boundary_bound_proved": False,
    }


def mobius_lcm_complete_covariance_probe(
        modulus, ell, divisor_lower, divisor_upper):
    """Evaluate (1) for every pair of actual truncated lcm coefficients."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid covariance-probe ranges")
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
    coefficients = {}
    for left in divisors:
        for right in divisors:
            q = math.lcm(left, right)
            coefficients[q] = coefficients.get(q, 0.0) + (
                mobius[left] * mobius[right]
                * logarithms[left] * logarithms[right])

    diagonal = 0.0
    off_diagonal = 0.0
    absolute_off_diagonal_bound = 0.0
    shared_factor_pair_count = 0
    periods = tuple(coefficients)
    for left in periods:
        left_coefficient = coefficients[left]
        for right in periods:
            covariance = cyclic_sawtooth_covariance(
                modulus, left, right)
            term = left_coefficient * coefficients[right] * covariance[
                "covariance"]
            if left == right:
                diagonal += term
            else:
                off_diagonal += term
                if covariance["gcd"] > 1:
                    shared_factor_pair_count += 1
                absolute_off_diagonal_bound += (
                    abs(left_coefficient * coefficients[right])
                    * min(covariance["gcd_covariance_bound"],
                          covariance["cauchy_covariance_bound"]))
    total = diagonal + off_diagonal
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "distinct_lcm_count": len(periods),
        "ordered_shared_factor_cross_pair_count": shared_factor_pair_count,
        "complete_period_diagonal_energy": diagonal,
        "complete_period_off_diagonal_energy": off_diagonal,
        "complete_period_total_energy": total,
        "total_over_diagonal": total / diagonal if diagonal else 0.0,
        "absolute_off_diagonal_gcd_bound": absolute_off_diagonal_bound,
        "complete_period_cross_covariance_identity_proved": True,
        "incomplete_prime_row_covariance_bound_proved": False,
    }


if __name__ == "__main__":
    for upper in (16, 24, 32, 48, 64):
        print(mobius_lcm_complete_covariance_probe(101, 101, 3, upper))
