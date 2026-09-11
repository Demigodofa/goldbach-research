"""Sparse divisor factorization of the absolute complete-covariance majorant.

The proved pairwise bound gives

    |Cov_m(q,r)| <= gcd(q,r)^2/(4*q*r).

Using ``g^2=sum_(d|g) J_2(d)`` therefore yields the exact factorization

    (1/4) sum_(q,r) |K_q K_r| gcd(q,r)^2/(q*r)
      = (1/4) sum_d J_2(d)(sum_(d|q)|K_q|/q)^2.         (1)

The right side is sparse in the divisors of the lcm support.  It bounds the
absolute value of the full complete-period covariance form, but may be much
larger than its signed value or diagonal.  The finite probe below tests that
loss rather than assuming it is harmless.
"""

import math
import statistics
from functools import lru_cache

from lcm_sawtooth_cross_covariance import cyclic_sawtooth_covariance
from lcm_sawtooth_incomplete_covariance import (
    _evaluate_polynomial,
    _lcm_coefficient_polynomials,
)
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values


@lru_cache(maxsize=None)
def _squarefree_divisor_jordan_pairs(value):
    """Return all ``(d,J_2(d))`` for a squarefree positive integer."""
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
    output = [(1, 1)]
    for factor in factors:
        output += [
            (divisor * factor, jordan * (factor ** 2 - 1))
            for divisor, jordan in output]
    return tuple(output)


def lcm_sawtooth_gcd_majorant_probe(
        modulus, ell, divisor_lower, divisor_upper):
    """Compare the sparse absolute majorant (1) with the exact diagonal."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid gcd-majorant ranges")
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
        for q, polynomial in polynomials.items()
    }
    divisor_sums = {}
    for q, coefficient in coefficients.items():
        for divisor, jordan in _squarefree_divisor_jordan_pairs(q):
            previous_sum, previous_jordan = divisor_sums.get(
                divisor, (0.0, jordan))
            if previous_jordan != jordan:
                raise ArithmeticError("inconsistent Jordan totient")
            divisor_sums[divisor] = (
                previous_sum + abs(coefficient) / q, jordan)
    sparse_majorant = .25 * sum(
        jordan * value ** 2 for value, jordan in divisor_sums.values())
    diagonal = sum(
        coefficient ** 2 * cyclic_sawtooth_covariance(
            modulus, q, q)["covariance"]
        for q, coefficient in coefficients.items())
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "divisor_count": len(divisors),
        "distinct_lcm_count": len(coefficients),
        "sparse_gcd_majorant": sparse_majorant,
        "complete_period_diagonal_energy": diagonal,
        "gcd_majorant_over_diagonal": (
            sparse_majorant / diagonal if diagonal else 0.0),
        "sparse_gcd_factorization_proved": True,
        "gcd_majorant_subpower_bound_proved": False,
    }


def project_gcd_majorant_scale_probe(scale_modulus, prime_sample_count=8):
    """Sample (1) at M=N^.59, A=N^.41, V=N^.15, B=N^.32."""
    if (type(scale_modulus) is not int or type(prime_sample_count) is not int
            or scale_modulus < 17 or prime_sample_count < 2):
        raise ValueError("invalid project-scale controls")
    inferred_N = scale_modulus ** (1 / .59)
    ell = int(1.5 * inferred_N ** .41)
    divisor_lower = int(inferred_N ** .15)
    divisor_upper = int(inferred_N ** .32)
    flags = _prime_flags(2 * scale_modulus)
    available = tuple(
        value for value in range(scale_modulus, 2 * scale_modulus + 1)
        if flags[value])
    if len(available) < prime_sample_count:
        raise ValueError("not enough primes in the scale interval")
    indices = tuple(round(
        index * (len(available) - 1) / (prime_sample_count - 1))
        for index in range(prime_sample_count))
    moduli = tuple(available[index] for index in indices)
    cells = tuple(lcm_sawtooth_gcd_majorant_probe(
        modulus, ell, divisor_lower, divisor_upper) for modulus in moduli)
    ratios = tuple(float(cell["gcd_majorant_over_diagonal"])
                   for cell in cells)
    return {
        "scale_modulus": scale_modulus,
        "inferred_N": inferred_N,
        "sampled_moduli": moduli,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "ratio_minimum": min(ratios),
        "ratio_median": statistics.median(ratios),
        "ratio_maximum": max(ratios),
        "ratio_mean": statistics.fmean(ratios),
        "finite_absolute_gcd_majorant_measurement": True,
        "gcd_majorant_subpower_bound_proved": False,
    }


if __name__ == "__main__":
    for scale in (251, 503, 1009, 2003, 4001, 8009, 16001):
        print(project_gcd_majorant_scale_probe(scale))
