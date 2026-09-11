"""Separate incomplete-row and varying-log effects from complete covariance.

For one prime ``m`` and the truncated squarefree divisor interval ``D``, the
lcm coefficient has an exact quadratic dependence on ``L=log(m*ell)``:

    K_q(L)=A_q*L^2+B_q*L+C_q.                            (1)

This permits a row sweep without rebuilding the divisor-pair sum.  Freezing
``K_q`` at one row, the probe compares

    A^(-1) sum_(ell in I) |sum_q K_q d_(m,q)(ell)|^2    (2)

with the exact complete-common-period quadratic form from
``lcm_sawtooth_cross_covariance.py``.  Their difference is the exact finite
boundary excess for that frozen vector.  Replacing the frozen values in (2)
by (1) separately measures the effect of the slowly varying logarithms.

This is a finite falsifier.  It supplies no bound for the boundary excess or
for its average over prime ``m``.
"""

import math
import statistics

from lcm_sawtooth_cross_covariance import cyclic_sawtooth_covariance
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values


def _lcm_coefficient_polynomials(divisors, mobius):
    polynomials = {}
    for left in divisors:
        left_log = math.log(left)
        for right in divisors:
            q = math.lcm(left, right)
            sign = int(mobius[left]) * int(mobius[right])
            right_log = math.log(right)
            quadratic, linear, constant = polynomials.get(
                q, (0.0, 0.0, 0.0))
            polynomials[q] = (
                quadratic + sign,
                linear - sign * (left_log + right_log),
                constant + sign * left_log * right_log,
            )
    return polynomials


def _evaluate_polynomial(polynomial, logarithm):
    quadratic, linear, constant = polynomial
    return (quadratic * logarithm + linear) * logarithm + constant


def _cyclic_discrepancy(modulus, ell, period):
    X = modulus * ell
    return ((X + modulus - 1) // period - X // period
            - (modulus - 1) / period)


def lcm_sawtooth_incomplete_covariance_probe(
        modulus, ell_first, row_count, ell_freeze,
        divisor_lower, divisor_upper):
    """Return the exact finite decomposition described in (1)-(2)."""
    if any(type(value) is not int for value in (
            modulus, ell_first, row_count, ell_freeze,
            divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell_first < 1 or row_count < 1 or ell_freeze < 1
            or divisor_lower < 1 or divisor_upper <= divisor_lower
            or divisor_upper >= modulus):
        raise ValueError("invalid incomplete-covariance ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")

    mobius = _mobius_values(divisor_upper)
    divisors = tuple(
        value for value in range(divisor_lower + 1, divisor_upper + 1)
        if mobius[value])
    if not divisors:
        raise ValueError("the divisor interval has no squarefree values")
    polynomials = _lcm_coefficient_polynomials(divisors, mobius)
    periods = tuple(polynomials)
    freeze_logarithm = math.log(modulus * ell_freeze)
    frozen_coefficients = {
        q: _evaluate_polynomial(polynomial, freeze_logarithm)
        for q, polynomial in polynomials.items()
    }

    frozen_square_sum = 0.0
    varying_square_sum = 0.0
    empirical_period_squares = {q: 0.0 for q in periods}
    for ell in range(ell_first, ell_first + row_count):
        row_logarithm = math.log(modulus * ell)
        frozen_sum = 0.0
        varying_sum = 0.0
        for q in periods:
            discrepancy = _cyclic_discrepancy(modulus, ell, q)
            empirical_period_squares[q] += discrepancy ** 2
            frozen_sum += frozen_coefficients[q] * discrepancy
            varying_sum += _evaluate_polynomial(
                polynomials[q], row_logarithm) * discrepancy
        frozen_square_sum += frozen_sum ** 2
        varying_square_sum += varying_sum ** 2
    frozen_incomplete_energy = frozen_square_sum / row_count
    varying_incomplete_energy = varying_square_sum / row_count
    empirical_diagonal = sum(
        frozen_coefficients[q] ** 2 * empirical_period_squares[q] / row_count
        for q in periods)

    complete_diagonal = 0.0
    complete_off_diagonal = 0.0
    for left in periods:
        for right in periods:
            term = (frozen_coefficients[left] * frozen_coefficients[right]
                    * cyclic_sawtooth_covariance(
                        modulus, left, right)["covariance"])
            if left == right:
                complete_diagonal += term
            else:
                complete_off_diagonal += term
    complete_energy = complete_diagonal + complete_off_diagonal
    boundary_excess = frozen_incomplete_energy - complete_energy
    varying_log_excess = varying_incomplete_energy - frozen_incomplete_energy
    return {
        "modulus": modulus,
        "ell_range": (ell_first, ell_first + row_count - 1),
        "ell_freeze": ell_freeze,
        "divisor_range": (divisor_lower, divisor_upper),
        "divisor_count": len(divisors),
        "distinct_lcm_count": len(periods),
        "frozen_incomplete_energy": frozen_incomplete_energy,
        "varying_log_incomplete_energy": varying_incomplete_energy,
        "empirical_incomplete_diagonal": empirical_diagonal,
        "complete_period_diagonal_energy": complete_diagonal,
        "complete_period_off_diagonal_energy": complete_off_diagonal,
        "complete_period_total_energy": complete_energy,
        "frozen_boundary_excess": boundary_excess,
        "varying_log_excess": varying_log_excess,
        "incomplete_total_over_complete_diagonal": (
            frozen_incomplete_energy / complete_diagonal
            if complete_diagonal else 0.0),
        "complete_total_over_complete_diagonal": (
            complete_energy / complete_diagonal if complete_diagonal else 0.0),
        "boundary_excess_over_complete_diagonal": (
            boundary_excess / complete_diagonal if complete_diagonal else 0.0),
        "varying_log_excess_over_complete_diagonal": (
            varying_log_excess / complete_diagonal
            if complete_diagonal else 0.0),
        "frozen_incomplete_over_empirical_diagonal": (
            frozen_incomplete_energy / empirical_diagonal
            if empirical_diagonal else 0.0),
        "exact_finite_boundary_decomposition": True,
        "incomplete_boundary_asymptotic_bound_proved": False,
        "prime_averaged_boundary_bound_proved": False,
    }


def project_boundary_scale_probe(scale_modulus, prime_sample_count=8):
    """Sample the exact boundary decomposition at the saved project exponents."""
    if (type(scale_modulus) is not int or type(prime_sample_count) is not int
            or scale_modulus < 17 or prime_sample_count < 2):
        raise ValueError("invalid project-scale controls")
    inferred_N = scale_modulus ** (1 / .59)
    row_count = int(inferred_N ** .41)
    divisor_lower = int(inferred_N ** .15)
    divisor_upper = int(inferred_N ** .32)
    if not 1 <= divisor_lower < divisor_upper < scale_modulus:
        raise ValueError("scale does not give a valid project divisor range")
    flags = _prime_flags(2 * scale_modulus)
    available = tuple(
        value for value in range(scale_modulus, 2 * scale_modulus + 1)
        if flags[value])
    if len(available) < prime_sample_count:
        raise ValueError("not enough primes in the requested scale interval")
    indices = tuple(round(
        index * (len(available) - 1) / (prime_sample_count - 1))
        for index in range(prime_sample_count))
    moduli = tuple(available[index] for index in indices)
    ell_freeze = row_count + row_count // 2
    cells = tuple(lcm_sawtooth_incomplete_covariance_probe(
        modulus, row_count, row_count, ell_freeze,
        divisor_lower, divisor_upper) for modulus in moduli)

    def summary(key):
        values = tuple(float(cell[key]) for cell in cells)
        return {
            "minimum": min(values),
            "median": statistics.median(values),
            "maximum": max(values),
            "mean": statistics.fmean(values),
            "maximum_absolute": max(abs(value) for value in values),
        }

    return {
        "scale_modulus": scale_modulus,
        "inferred_N": inferred_N,
        "sampled_moduli": moduli,
        "row_range": (row_count, 2 * row_count - 1),
        "divisor_range": (divisor_lower, divisor_upper),
        "boundary_ratio_summary": summary(
            "boundary_excess_over_complete_diagonal"),
        "varying_log_ratio_summary": summary(
            "varying_log_excess_over_complete_diagonal"),
        "incomplete_total_ratio_summary": summary(
            "incomplete_total_over_complete_diagonal"),
        "complete_total_ratio_summary": summary(
            "complete_total_over_complete_diagonal"),
        "finite_project_boundary_measurement": True,
        "prime_averaged_boundary_bound_proved": False,
    }


if __name__ == "__main__":
    for arguments in (
            (101, 47, 47, 70, 4, 20),
            (503, 75, 75, 112, 4, 29),
            (1009, 123, 123, 184, 5, 42)):
        result = lcm_sawtooth_incomplete_covariance_probe(*arguments)
        print({key: result[key] for key in (
            "modulus", "divisor_range", "distinct_lcm_count",
            "incomplete_total_over_complete_diagonal",
            "complete_total_over_complete_diagonal",
            "boundary_excess_over_complete_diagonal",
            "varying_log_excess_over_complete_diagonal")})
