"""Exact sparse factorization of the complete-period sawtooth covariance.

The one-variable identity proved in ``lcm_sawtooth_cross_covariance.py`` is

    Cov_m(q,r)=F_m(gcd(q,r))/(q*r),
    F_m(g)=s_g*(g-s_g),  s_g=(m-1) mod g.                (1)

Let ``H_m=mu*F_m`` under divisor convolution, so
``F_m(g)=sum_(d|g)H_m(d)``. Then every real coefficient vector satisfies

    sum_(q,r) x_q*x_r*Cov_m(q,r)
      = sum_d H_m(d)(sum_(d|q)x_q/q)^2.                 (2)

The transform has the primitive-frequency formula

    H_m(d)=sum_(1<=k<d,(k,d)=1)
             |sum_(0<=x<m-1) exp(2*pi*i*k*x/d)|^2 >= 0. (3)

Indeed Parseval gives ``F_m(g)`` as the total nonzero Fourier energy of an
interval modulo ``g``; grouping frequencies by their reduced denominator
gives (3). Thus (2) is an exact positive sum-of-squares factorization. The
same identity with ``|x_q|`` gives the termwise-absolute covariance form
because (1) is nonnegative. Formula (2) replaces the dense lcm-pair
covariance calculation by divisor sums.
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


def sawtooth_gcd_kernel_numerator(modulus, divisor):
    """Return ``F_m(divisor)`` in (1)."""
    if (type(modulus) is not int or type(divisor) is not int
            or modulus < 2 or divisor < 1):
        raise ValueError("modulus and divisor must be positive integers")
    residue = (modulus - 1) % divisor
    return residue * (divisor - residue)


@lru_cache(maxsize=None)
def _squarefree_divisors_with_complement_mobius(value):
    """Return ``(e,mu(value/e))`` for every divisor of squarefree ``value``."""
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
    output = [(1, -1 if len(factors) % 2 else 1)]
    for factor in factors:
        output += [(divisor * factor, -sign)
                   for divisor, sign in output]
    return tuple(output)


def sawtooth_gcd_mobius_transform(modulus, divisor):
    """Return ``H_m(divisor)=sum_(e|divisor)mu(divisor/e)F_m(e)``."""
    return sum(
        sign * sawtooth_gcd_kernel_numerator(modulus, factor)
        for factor, sign in _squarefree_divisors_with_complement_mobius(
            divisor))


def lcm_sawtooth_exact_gcd_factorization_probe(
        modulus, ell, divisor_lower, divisor_upper):
    """Evaluate both exact forms in (2) for the actual Mobius coefficients."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid exact-gcd-factorization ranges")
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

    signed_divisor_sums = {}
    absolute_divisor_sums = {}
    transform_weights = {}
    for q, coefficient in coefficients.items():
        for divisor, _ in _squarefree_divisors_with_complement_mobius(q):
            signed_divisor_sums[divisor] = (
                signed_divisor_sums.get(divisor, 0.0) + coefficient / q)
            absolute_divisor_sums[divisor] = (
                absolute_divisor_sums.get(divisor, 0.0)
                + abs(coefficient) / q)
            if divisor not in transform_weights:
                transform_weights[divisor] = sawtooth_gcd_mobius_transform(
                    modulus, divisor)
                if transform_weights[divisor] < 0:
                    raise ArithmeticError(
                        "primitive-frequency weight must be nonnegative")
    signed_energy = sum(
        transform_weights[divisor] * value ** 2
        for divisor, value in signed_divisor_sums.items())
    absolute_energy = sum(
        transform_weights[divisor] * value ** 2
        for divisor, value in absolute_divisor_sums.items())
    diagonal = sum(
        coefficient ** 2 * cyclic_sawtooth_covariance(
            modulus, q, q)["covariance"]
        for q, coefficient in coefficients.items())
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "distinct_lcm_count": len(coefficients),
        "transform_divisor_count": len(transform_weights),
        "zero_transform_weight_count": sum(
            weight == 0 for weight in transform_weights.values()),
        "positive_transform_weight_count": sum(
            weight > 0 for weight in transform_weights.values()),
        "exact_signed_complete_energy": signed_energy,
        "exact_termwise_absolute_complete_energy": absolute_energy,
        "complete_period_diagonal_energy": diagonal,
        "signed_energy_over_diagonal": (
            signed_energy / diagonal if diagonal else 0.0),
        "absolute_energy_over_diagonal": (
            absolute_energy / diagonal if diagonal else 0.0),
        "absolute_over_signed_energy": (
            absolute_energy / signed_energy if signed_energy else 0.0),
        "one_variable_gcd_kernel_proved": True,
        "primitive_frequency_weights_nonnegative_proved": True,
        "exact_sparse_gcd_factorization_proved": True,
        "subpower_factorized_bound_proved": False,
    }


def project_exact_gcd_scale_probe(scale_modulus, prime_sample_count=8):
    """Sample the exact sparse ratios at the saved project exponents."""
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
    cells = tuple(lcm_sawtooth_exact_gcd_factorization_probe(
        modulus, ell, divisor_lower, divisor_upper) for modulus in moduli)

    def summary(key):
        values = tuple(float(cell[key]) for cell in cells)
        return (min(values), statistics.median(values), max(values))

    return {
        "scale_modulus": scale_modulus,
        "sampled_moduli": moduli,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "signed_ratio_min_median_max": summary(
            "signed_energy_over_diagonal"),
        "absolute_ratio_min_median_max": summary(
            "absolute_energy_over_diagonal"),
        "absolute_over_signed_min_median_max": summary(
            "absolute_over_signed_energy"),
        "finite_exact_gcd_factorization_measurement": True,
        "subpower_factorized_bound_proved": False,
    }


if __name__ == "__main__":
    for scale in (251, 503, 1009, 2003, 4001, 8009, 16001):
        print(project_exact_gcd_scale_probe(scale))
