"""Bound the diagonal Fourier energy of the truncated lcm count error.

Let ``D`` be the squarefree integers in ``(V,B]``, put
``L_a=log(X/a)`` with ``X=m*ell``, and define

    K_q=sum_(a,b in D, lcm(a,b)=q) mu(a)mu(b)L_a L_b.    (1)

For the cyclic count discrepancy as the row rotates modulo ``q``, its exact
full-period variance is

    v_(m,q)=theta(1-theta), theta=((m-1) mod q)/q.       (2)

The diagonal frequency energy is ``E_diag=sum_q K_q^2 v_(m,q)``.  If ``R_q``
counts the ordered pairs in (1), Cauchy, (2), and squarefreeness give

    E_diag
      <= sum_q R_q v_(m,q) sum_(lcm(a,b)=q)L_a^2 L_b^2
      <= m R_max sum_(a,b in D) L_a^2 L_b^2/lcm(a,b),   (3)

where ``R_max=max R_q``.  Every prime of squarefree ``q`` is assigned to
``a only``, ``b only``, or ``both``, so ``R_q<=3^omega(q)=q^o(1)``.  Finally

    sum_(a,b) L_a^2 L_b^2/lcm(a,b)
      =sum_(d<=B) phi(d)[sum_(a in D,d|a)L_a^2/a]^2.    (4)

Equations (3)-(4) give the needed subpower-scale diagonal bound after the
existing totient-frame lower estimate.  They do not bound cross-q Fourier
covariances on an incomplete prime-row sample.
"""

import math

from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values


def cyclic_sawtooth_variance(modulus, period):
    """Return (2), the exact mean square over one complete row period."""
    if (type(modulus) is not int or type(period) is not int
            or modulus < 2 or period < 2 or math.gcd(modulus, period) != 1):
        raise ValueError(
            "modulus and period must be coprime integers at least two")
    theta = ((modulus - 1) % period) / period
    return theta * (1 - theta)


def lcm_sawtooth_diagonal_probe(
        modulus, ell, divisor_lower, divisor_upper):
    """Evaluate every term in (1)-(4) and the explicit inequalities (3)."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (modulus < 2 or ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid diagonal-probe ranges")
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
    multiplicities = {}
    pair_square_mass = {}
    reciprocal_pair_mass = 0.0
    for left in divisors:
        for right in divisors:
            q = math.lcm(left, right)
            coefficients[q] = coefficients.get(q, 0.0) + (
                mobius[left] * mobius[right]
                * logarithms[left] * logarithms[right])
            multiplicities[q] = multiplicities.get(q, 0) + 1
            square_mass = logarithms[left] ** 2 * logarithms[right] ** 2
            pair_square_mass[q] = pair_square_mass.get(q, 0.0) + square_mass
            reciprocal_pair_mass += square_mass / q

    diagonal_energy = sum(
        coefficient ** 2 * cyclic_sawtooth_variance(modulus, q)
        for q, coefficient in coefficients.items() if q > 1)
    exact_cauchy_bound = sum(
        multiplicities[q] * cyclic_sawtooth_variance(modulus, q)
        * pair_square_mass[q]
        for q in coefficients if q > 1)
    maximum_multiplicity = max(multiplicities.values())
    reciprocal_bound = modulus * maximum_multiplicity * reciprocal_pair_mass

    gcd_decomposition = 0.0
    for common in range(1, divisor_upper + 1):
        inner = sum(logarithms[value] ** 2 / value
                    for value in divisors if value % common == 0)
        gcd_decomposition += _totient(common) * inner ** 2

    maximum_three_to_omega = 1
    for q in coefficients:
        remaining = q
        omega = 0
        prime = 2
        while prime * prime <= remaining:
            if remaining % prime == 0:
                omega += 1
                while remaining % prime == 0:
                    remaining //= prime
            prime += 1 if prime == 2 else 2
        if remaining > 1:
            omega += 1
        maximum_three_to_omega = max(maximum_three_to_omega, 3 ** omega)

    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "divisor_count": len(divisors),
        "distinct_lcm_count": len(coefficients),
        "diagonal_fourier_energy": diagonal_energy,
        "exact_cauchy_upper_bound": exact_cauchy_bound,
        "reciprocal_lcm_pair_mass": reciprocal_pair_mass,
        "gcd_decomposition_pair_mass": gcd_decomposition,
        "maximum_lcm_pair_multiplicity": maximum_multiplicity,
        "maximum_three_to_omega": maximum_three_to_omega,
        "reciprocal_multiplicity_upper_bound": reciprocal_bound,
        "diagonal_bound_proved": True,
        "cross_lcm_covariance_bound_proved": False,
    }
