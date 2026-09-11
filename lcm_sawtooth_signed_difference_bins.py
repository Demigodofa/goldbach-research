"""Decompose the exact frozen-log boundary by reduced difference denominator.

Each off-diagonal pair of primitive frequencies contributes

    c_i conjugate(c_j) A^-1 sum_(ell=L)^(L+A-1) e((f_i-f_j)ell).

This module bins those signed contributions by the reduced denominator of
``f_i-f_j`` and records the corresponding termwise-absolute envelope.  A
small signed bin with a large envelope is direct finite evidence of signed
cancellation.  It does not by itself separate the conductor-coefficient signs
from the rational phases.  It is not an asymptotic estimate or the outer prime
sum.
"""

import math

import numpy as np

from lcm_sawtooth_exact_gcd_factorization import (
    sawtooth_gcd_mobius_transform,
)
from lcm_sawtooth_incomplete_frequency import _quadratic_support_data
from lcm_sawtooth_reduced_difference_mass import (
    _reduced_difference_denominator,
    _validate_inputs,
)


def _stable_geometric_sum(modulus, denominator, numerators):
    length = modulus - 1
    sine_residue = (numerators * length) % (2 * denominator)
    amplitude = (
        np.sin(np.pi * sine_residue / denominator)
        / np.sin(np.pi * numerators / denominator))
    phase = np.exp(1j * np.pi * numerators * modulus / denominator)
    return phase * amplitude


def _signed_frequency_data(
        modulus, ell_freeze, divisor_lower, divisor_upper,
        replace_conductor_signs=False):
    logarithm = math.log(modulus * ell_freeze)
    denominators = []
    numerators = []
    coefficients = []
    frequencies = []
    for denominator, polynomial in _quadratic_support_data(
            divisor_lower, divisor_upper)[1]:
        if sawtooth_gcd_mobius_transform(modulus, denominator) <= 0:
            continue
        structured_sum = ((polynomial[0] * logarithm + polynomial[1])
                          * logarithm + polynomial[2])
        if replace_conductor_signs:
            structured_sum = abs(structured_sum)
        candidates = np.arange(1, denominator, dtype=np.int64)
        primitive = candidates[np.gcd(candidates, denominator) == 1]
        local_coefficients = structured_sum * _stable_geometric_sum(
            modulus, denominator, primitive)
        positive = np.abs(local_coefficients) > 0
        denominators.append(np.full(
            int(np.sum(positive)), denominator, dtype=np.int64))
        numerators.append(primitive[positive])
        coefficients.append(local_coefficients[positive])
        frequencies.append(
            ((modulus * primitive[positive]) % denominator) / denominator)
    return (np.concatenate(denominators), np.concatenate(numerators),
            np.concatenate(coefficients), np.concatenate(frequencies))


def signed_difference_bin_receipt(
        modulus, ell_first, row_count, ell_freeze,
        divisor_lower, divisor_upper, replace_conductor_signs=False):
    """Exactly bin the frozen-log signed boundary and absolute envelope."""
    _validate_inputs(
        modulus, ell_freeze, row_count, divisor_lower, divisor_upper)
    if type(ell_first) is not int or ell_first < 1:
        raise ValueError("ell_first must be a positive integer")
    if type(replace_conductor_signs) is not bool:
        raise ValueError("replace_conductor_signs must be Boolean")
    denominators, numerators, coefficients, frequencies = (
        _signed_frequency_data(
            modulus, ell_freeze, divisor_lower, divisor_upper,
            replace_conductor_signs))
    complete_energy = float(np.sum(np.abs(coefficients) ** 2))
    thresholds = np.array(
        (modulus * row_count // 4,
         modulus * row_count,
         4 * modulus * row_count), dtype=np.int64)
    signed_bins = np.zeros(4, dtype=complex)
    absolute_bins = np.zeros(4, dtype=float)
    chunk_size = 64
    for first in range(0, len(coefficients), chunk_size):
        left_d = denominators[first:first + chunk_size, None]
        left_k = numerators[first:first + chunk_size, None]
        reduced = _reduced_difference_denominator(
            left_d, left_k,
            denominators[None, :], numerators[None, :])
        difference = (
            frequencies[first:first + chunk_size, None]
            - frequencies[None, :])
        kernel = np.ones(difference.shape, dtype=complex)
        off_diagonal = reduced > 1
        roots = np.exp(2j * np.pi * difference[off_diagonal])
        kernel[off_diagonal] = (
            np.exp(2j * np.pi * difference[off_diagonal] * ell_first)
            * (1 - roots ** row_count)
            / (row_count * (1 - roots)))
        contributions = (
            coefficients[first:first + chunk_size, None]
            * np.conjugate(coefficients[None, :]) * kernel)
        bins = np.digitize(reduced, thresholds, right=True)
        for index in range(4):
            selected = bins == index
            if index == 0:
                selected &= off_diagonal
            signed_bins[index] += np.sum(contributions[selected])
            absolute_bins[index] += float(np.sum(
                np.abs(contributions[selected])))

    row_values = np.array([
        np.sum(coefficients * np.exp(2j * np.pi * frequencies * ell))
        for ell in range(ell_first, ell_first + row_count)])
    incomplete_energy = float(np.mean(np.abs(row_values) ** 2))
    boundary = incomplete_energy - complete_energy
    signed_real = signed_bins.real / complete_energy
    absolute = absolute_bins / complete_energy
    high_q_signed = float(np.sum(signed_real[2:]))
    high_q_absolute = float(np.sum(absolute[2:]))
    return {
        "modulus": modulus,
        "ell_range": (ell_first, ell_first + row_count - 1),
        "ell_freeze": ell_freeze,
        "divisor_range": (divisor_lower, divisor_upper),
        "conductor_coefficient_mode": (
            "absolute" if replace_conductor_signs else "actual"),
        "positive_frequency_count": len(coefficients),
        "difference_modulus_thresholds": tuple(int(x) for x in thresholds),
        "signed_boundary_bins_over_complete": tuple(
            float(x) for x in signed_real),
        "absolute_envelope_bins_over_complete": tuple(
            float(x) for x in absolute),
        "high_Q_signed_over_complete": high_q_signed,
        "high_Q_absolute_over_complete": high_q_absolute,
        "high_Q_net_over_absolute": (
            abs(high_q_signed) / high_q_absolute
            if high_q_absolute else 0.0),
        "total_boundary_over_complete": boundary / complete_energy,
        "bin_reconstruction_error_over_complete": abs(
            boundary - float(np.sum(signed_bins.real))) / complete_energy,
        "ordered_pair_imaginary_error_over_complete": abs(
            float(np.sum(signed_bins.imag))) / complete_energy,
        "finite_signed_frequency_measurement": True,
        "signed_boundary_asymptotic_bound_proved": False,
        "prime_averaged_cancellation_proved": False,
    }


if __name__ == "__main__":
    for modulus in (251, 373, 499):
        for replace_signs in (False, True):
            print(signed_difference_bin_receipt(
                modulus, 46, 46, 69, 4, 20, replace_signs))
