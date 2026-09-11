"""Support test for divisor levels in the primitive cotangent transform."""

import math

import numpy as np

from lcm_sawtooth_cotangent_transform import ENDPOINT_DENOMINATORS
from lcm_sawtooth_source_ramanujan import (
    _divisors,
    _mobius,
    _primitive_numerators,
)


def _linear_sawtooth(modulus, frequency):
    residue = frequency % modulus
    return 0 if residue == 0 else modulus - 2 * residue


def _divisor_level_inverse_direct(denominator, modulus, numerator):
    coefficient = _mobius(denominator // modulus)
    return sum(
        1j * coefficient * _linear_sawtooth(modulus, frequency)
        * np.exp(-2j * np.pi * numerator * frequency / denominator)
        for frequency in range(denominator)) / denominator


def _divisor_level_inverse_support_formula(
        denominator, modulus, numerator):
    support_step = denominator // modulus
    if numerator % support_step != 0:
        return 0.0
    reduced_numerator = (numerator // support_step) % modulus
    if reduced_numerator == 0:
        return 0.0
    return (
        _mobius(support_step)
        / math.tan(math.pi * reduced_numerator / modulus))


def mobius_divisor_support_receipt(
        denominators=ENDPOINT_DENOMINATORS, tolerance=1e-12):
    denominators = tuple(denominators)
    if (not denominators
            or any(type(value) is not int or value < 3
                   for value in denominators)):
        raise ValueError("denominators must be integers at least three")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    rows = {}
    for denominator in denominators:
        divisors = _divisors(denominator)
        maximum_support_formula_relative_error = 0.0
        for modulus in divisors:
            for numerator in range(denominator):
                direct = _divisor_level_inverse_direct(
                    denominator, modulus, numerator)
                formula = _divisor_level_inverse_support_formula(
                    denominator, modulus, numerator)
                maximum_support_formula_relative_error = max(
                    maximum_support_formula_relative_error,
                    abs(direct - formula) / max(1.0, abs(formula)))

        primitive_numerators = _primitive_numerators(denominator)
        proper_divisors = tuple(
            modulus for modulus in divisors if modulus < denominator)
        maximum_proper_level_absolute_value = max(
            (abs(_divisor_level_inverse_direct(
                denominator, modulus, numerator))
             for modulus in proper_divisors
             for numerator in primitive_numerators),
            default=0.0)
        maximum_terminal_level_relative_error = max(
            abs(_divisor_level_inverse_direct(
                denominator, denominator, numerator)
                - 1 / math.tan(math.pi * numerator / denominator))
            / max(1.0, abs(1 / math.tan(
                math.pi * numerator / denominator)))
            for numerator in primitive_numerators)
        exact_primitive_support_obstruction = all(
            numerator % (denominator // modulus) != 0
            for modulus in proper_divisors
            for numerator in primitive_numerators)
        rows[denominator] = {
            "maximum_support_formula_relative_error": (
                maximum_support_formula_relative_error),
            "maximum_proper_level_absolute_value": (
                maximum_proper_level_absolute_value),
            "maximum_terminal_level_relative_error": (
                maximum_terminal_level_relative_error),
            "exact_primitive_support_obstruction": (
                exact_primitive_support_obstruction),
            "support_reconstruction_passes": bool(
                exact_primitive_support_obstruction
                and maximum_support_formula_relative_error <= tolerance
                and maximum_proper_level_absolute_value <= tolerance
                and maximum_terminal_level_relative_error <= tolerance),
        }

    return {
        "denominators": denominators,
        "rows": rows,
        "all_support_reconstructions_pass": all(
            row["support_reconstruction_passes"]
            for row in rows.values()),
        "proper_divisor_mobius_signs_survive_at_primitive_inverse_indices": (
            False),
        "proposed_inverse_level_sign_mechanism_passes": False,
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(mobius_divisor_support_receipt())
