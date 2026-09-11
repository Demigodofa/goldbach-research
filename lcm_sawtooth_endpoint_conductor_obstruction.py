"""Bound endpoint mass and expose a conductor-energy-only obstruction.

Put ``n=m-1`` and

    G_(m,d)(k) = sum_(0<=x<n) exp(2*pi*i*k*x/d),
    H_m(d) = sum_((k,d)=1) |G_(m,d)(k)|^2.

For squarefree ``d`` the two endpoint modes satisfy

    E_end(d)/H_m(d)
      <= min(1, 2*pi^2*n*2^omega(d)/phi(d)).             (1)

The nontrivial case follows by counting primitive ``k<=d/(2n)``.  Each such
mode and its conjugate has size at least ``2n/pi``; inclusion-exclusion loses
at most ``2^omega(d)`` reduced residues.

This useful dilution does not make complete conductor energy alone sufficient
for the Q-weighted endpoint pair-square envelope.  If coprime squarefree
``d,e>=2n`` are also coprime to ``m``, normalize a coefficient vector by
``S_d=H_m(d)^(-1/2)``, ``S_e=H_m(e)^(-1/2)``.  All eight ordered cross-endpoint
pairs have reduced denominator ``de`` and

    endpoint envelope / (sum H_m(f)|S_f|^2)^2
      >= 32*n^2/pi^4.                                   (2)

Thus a generic subpower comparison with conductor energy squared is false.
The actual structured polynomial coefficient family and prime averaging are
not addressed by this obstruction.
"""

import math

from lcm_sawtooth_endpoint_resonance_score import (
    endpoint_reduced_denominator,
)
from lcm_sawtooth_exact_gcd_factorization import (
    sawtooth_gcd_mobius_transform,
)
from lcm_sawtooth_high_d_assignment import _squarefree_prime_factors


def _totient_from_factors(value, factors):
    result = value
    for prime in factors:
        result -= result // prime
    return result


def _endpoint_geometric_square(modulus, conductor):
    residue = (modulus - 1) % conductor
    if residue == 0:
        return 0.0
    return (
        math.sin(math.pi * residue / conductor)
        / math.sin(math.pi / conductor)
    ) ** 2


def endpoint_conductor_energy_bound_receipt(modulus, conductor):
    """Evaluate the proved endpoint dilution bound (1)."""
    if (type(modulus) is not int or type(conductor) is not int
            or modulus < 2 or conductor <= 1):
        raise ValueError("modulus and conductor must be integers in range")
    factors = _squarefree_prime_factors(conductor)
    totient = _totient_from_factors(conductor, factors)
    primitive_weight = sawtooth_gcd_mobius_transform(modulus, conductor)
    endpoint_count = 1 if conductor == 2 else 2
    endpoint_mass = (
        endpoint_count * _endpoint_geometric_square(modulus, conductor))
    if primitive_weight == 0:
        if endpoint_mass > 1e-18:
            raise ArithmeticError("zero primitive energy has endpoint mass")
        endpoint_fraction = 0.0
    else:
        endpoint_fraction = endpoint_mass / primitive_weight
    arithmetic_bound = (
        2 * math.pi ** 2 * (modulus - 1)
        * 2 ** len(factors) / totient)
    proved_bound = min(1.0, arithmetic_bound)
    if endpoint_fraction > proved_bound + 1e-10:
        raise ArithmeticError("endpoint conductor-energy bound failed")
    return {
        "modulus": modulus,
        "conductor": conductor,
        "squarefree_prime_factors": factors,
        "euler_phi": totient,
        "primitive_conductor_energy": primitive_weight,
        "endpoint_frequency_count": endpoint_count,
        "endpoint_frequency_energy": endpoint_mass,
        "endpoint_energy_fraction": endpoint_fraction,
        "proved_endpoint_energy_fraction_bound": proved_bound,
        "untruncated_arithmetic_bound": arithmetic_bound,
        "endpoint_dilution_bound_proved": True,
        "neighboring_primitive_frequency_mechanism_proved": True,
    }


def two_conductor_endpoint_obstruction_receipt(
        modulus, row_count, left_conductor, right_conductor):
    """Evaluate the normalized two-conductor lower bound (2)."""
    if any(type(value) is not int for value in (
            modulus, row_count, left_conductor, right_conductor)):
        raise ValueError("all inputs must be integers")
    if modulus < 3 or row_count < 1:
        raise ValueError("modulus and row_count are out of range")
    left_factors = _squarefree_prime_factors(left_conductor)
    right_factors = _squarefree_prime_factors(right_conductor)
    length = modulus - 1
    if (left_conductor <= 2 or right_conductor <= 2
            or math.gcd(left_conductor, right_conductor) != 1
            or math.gcd(modulus, left_conductor * right_conductor) != 1
            or min(left_conductor, right_conductor) < 2 * length
            or left_conductor * right_conductor <= modulus * row_count):
        raise ValueError("conductors do not satisfy the obstruction range")

    left_weight = sawtooth_gcd_mobius_transform(
        modulus, left_conductor)
    right_weight = sawtooth_gcd_mobius_transform(
        modulus, right_conductor)
    if left_weight <= 0 or right_weight <= 0:
        raise ArithmeticError("obstruction conductors need positive energy")
    left_endpoint = _endpoint_geometric_square(modulus, left_conductor)
    right_endpoint = _endpoint_geometric_square(modulus, right_conductor)
    left_normalized = left_endpoint / left_weight
    right_normalized = right_endpoint / right_weight

    signs = (-1, 1)
    denominators = tuple(
        endpoint_reduced_denominator(
            left_conductor, right_conductor, left_sign, right_sign)
        for left_sign in signs for right_sign in signs)
    if any(value != left_conductor * right_conductor
           for value in denominators):
        raise ArithmeticError("cross endpoint did not retain denominator de")

    # Four sign pairs in each ordered conductor direction.
    cross_endpoint_envelope = (
        8 * left_conductor * right_conductor
        * left_normalized * right_normalized)
    complete_conductor_energy = 2.0
    normalized_envelope = (
        cross_endpoint_envelope / complete_conductor_energy ** 2)
    proved_lower_bound = 32 * length ** 2 / math.pi ** 4
    if normalized_envelope + 1e-10 < proved_lower_bound:
        raise ArithmeticError("two-conductor obstruction bound failed")
    return {
        "modulus": modulus,
        "row_count": row_count,
        "conductors": (left_conductor, right_conductor),
        "conductor_prime_factors": (left_factors, right_factors),
        "cross_endpoint_reduced_denominators": denominators,
        "complete_conductor_energy": complete_conductor_energy,
        "cross_endpoint_Q_weighted_pair_square_envelope": (
            cross_endpoint_envelope),
        "normalized_cross_endpoint_envelope": normalized_envelope,
        "proved_normalized_lower_bound": proved_lower_bound,
        "two_conductor_endpoint_obstruction_proved": True,
        "generic_subpower_conductor_energy_comparison_refuted": True,
        "structured_polynomial_family_refuted": False,
        "prime_averaged_endpoint_bound_refuted": False,
    }


if __name__ == "__main__":
    print(endpoint_conductor_energy_bound_receipt(101, 2310))
    print(two_conductor_endpoint_obstruction_receipt(101, 10, 221, 437))
