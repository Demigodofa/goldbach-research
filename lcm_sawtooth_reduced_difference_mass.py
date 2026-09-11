"""Measure reduced frequency-difference denominators under exact energy weights.

For every active primitive frequency ``k/d`` give it positive mass

    |S_d|^2 |G_(m,d,k)|^2.

Two independent draws then give the natural Parseval product-energy model for
the difference frequency.  This module measures the denominator ``Q`` of the
reduced difference ``k/d-h/e`` and compares it with the conductor proxy
``lcm(d,e)``.  It is a positive-energy diagnostic, not the signed incomplete
boundary form or a prime-averaged estimate.
"""

import math

import numpy as np

from lcm_sawtooth_exact_gcd_factorization import (
    sawtooth_gcd_mobius_transform,
)
from lcm_sawtooth_incomplete_frequency import _quadratic_support_data
from mobius_covariance_endpoint_probe import _prime_flags


def _reduced_difference_denominator(left_d, left_k, right_d, right_k):
    common = np.lcm(left_d, right_d)
    numerator = left_k * (common // left_d) - right_k * (common // right_d)
    return common // np.gcd(np.abs(numerator), common)


def _actual_frequency_energy_data(
        modulus, ell_freeze, divisor_lower, divisor_upper):
    logarithm = math.log(modulus * ell_freeze)
    denominators = []
    numerators = []
    energies = []
    conductor_energy = 0.0
    for denominator, polynomial in _quadratic_support_data(
            divisor_lower, divisor_upper)[1]:
        primitive_weight = sawtooth_gcd_mobius_transform(
            modulus, denominator)
        if primitive_weight <= 0:
            continue
        structured_sum = ((polynomial[0] * logarithm + polynomial[1])
                          * logarithm + polynomial[2])
        conductor_energy += primitive_weight * structured_sum ** 2
        candidates = np.arange(1, denominator, dtype=np.int64)
        primitive = candidates[np.gcd(candidates, denominator) == 1]
        residue = (modulus - 1) % denominator
        phase_residue = (primitive * residue) % denominator
        geometric_square = (
            np.sin(np.pi * phase_residue / denominator)
            / np.sin(np.pi * primitive / denominator)) ** 2
        frequency_energy = structured_sum ** 2 * geometric_square
        positive = frequency_energy > 0
        denominators.append(np.full(
            int(np.sum(positive)), denominator, dtype=np.int64))
        numerators.append(primitive[positive])
        energies.append(frequency_energy[positive])
    if not energies:
        raise ArithmeticError("no positive primitive-frequency energy")
    denominators = np.concatenate(denominators)
    numerators = np.concatenate(numerators)
    energies = np.concatenate(energies)
    frequency_energy = float(np.sum(energies))
    return denominators, numerators, energies, conductor_energy, frequency_energy


def _validate_inputs(
        modulus, ell_freeze, row_count, divisor_lower, divisor_upper):
    if any(type(value) is not int for value in (
            modulus, ell_freeze, row_count,
            divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell_freeze < 1 or row_count < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid reduced-difference ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")


def reduced_difference_mass_receipt(
        modulus, ell_freeze, row_count, divisor_lower, divisor_upper,
        sample_count=200000, seed=20260911, exact=False):
    """Return exact or deterministic-sample positive mass above MA scales."""
    _validate_inputs(
        modulus, ell_freeze, row_count, divisor_lower, divisor_upper)
    if type(sample_count) is not int or sample_count < 1:
        raise ValueError("sample_count must be a positive integer")
    if type(seed) is not int or type(exact) is not bool:
        raise ValueError("seed must be an integer and exact must be Boolean")

    denominators, numerators, energies, conductor_energy, frequency_energy = (
        _actual_frequency_energy_data(
            modulus, ell_freeze, divisor_lower, divisor_upper))
    probabilities = energies / frequency_energy
    critical = modulus * row_count
    thresholds = np.array(
        (critical // 4, critical, critical * 4), dtype=np.int64)
    high_q = np.zeros(3, dtype=float)
    high_lcm = np.zeros(3, dtype=float)
    if exact:
        sample_count = len(energies) ** 2
        chunk_size = 128
        for first in range(0, len(energies), chunk_size):
            left_d = denominators[first:first + chunk_size, None]
            left_k = numerators[first:first + chunk_size, None]
            pair_probability = (
                probabilities[first:first + chunk_size, None]
                * probabilities[None, :])
            common = np.lcm(left_d, denominators[None, :])
            reduced = _reduced_difference_denominator(
                left_d, left_k,
                denominators[None, :], numerators[None, :])
            for index, threshold in enumerate(thresholds):
                high_q[index] += float(np.sum(
                    pair_probability[reduced > threshold]))
                high_lcm[index] += float(np.sum(
                    pair_probability[common > threshold]))
        standard_error_bounds = (0.0, 0.0, 0.0)
    else:
        generator = np.random.default_rng(seed)
        pairs = generator.choice(
            len(energies), size=(sample_count, 2), p=probabilities)
        left, right = pairs[:, 0], pairs[:, 1]
        common = np.lcm(denominators[left], denominators[right])
        reduced = _reduced_difference_denominator(
            denominators[left], numerators[left],
            denominators[right], numerators[right])
        for index, threshold in enumerate(thresholds):
            high_q[index] = float(np.mean(reduced > threshold))
            high_lcm[index] = float(np.mean(common > threshold))
        standard_error_bounds = tuple(
            math.sqrt(value * (1 - value) / sample_count)
            for value in high_q)

    return {
        "modulus": modulus,
        "ell_freeze": ell_freeze,
        "row_count": row_count,
        "divisor_range": (divisor_lower, divisor_upper),
        "positive_frequency_count": len(energies),
        "difference_modulus_thresholds": tuple(int(x) for x in thresholds),
        "reduced_Q_energy_fractions": tuple(float(x) for x in high_q),
        "conductor_lcm_energy_fractions": tuple(float(x) for x in high_lcm),
        "actual_fraction_Q_above_MA": float(high_q[1]),
        "actual_fraction_lcm_above_MA": float(high_lcm[1]),
        "Q_fraction_standard_errors": standard_error_bounds,
        "sample_count": sample_count,
        "seed": seed,
        "exact_enumeration": exact,
        "frequency_parseval_relative_error": abs(
            frequency_energy - conductor_energy) / conductor_energy,
        "positive_frequency_denominator_sparsity_proved": False,
        "signed_difference_modulus_cancellation_proved": False,
        "finite_positive_frequency_measurement": True,
    }


if __name__ == "__main__":
    print(reduced_difference_mass_receipt(101, 36, 24, 3, 12, exact=True))
    for controls in (
            (251, 69, 46, 4, 20),
            (503, 112, 75, 4, 29),
            (1009, 183, 122, 5, 42)):
        print(reduced_difference_mass_receipt(*controls))
