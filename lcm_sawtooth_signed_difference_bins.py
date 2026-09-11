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
    high_q_group_sums = {}
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
        high_q = reduced > thresholds[1]
        q_values, inverse = np.unique(reduced[high_q], return_inverse=True)
        q_contributions = contributions[high_q]
        grouped = (
            np.bincount(inverse, weights=q_contributions.real)
            + 1j * np.bincount(inverse, weights=q_contributions.imag))
        for q_value, contribution in zip(q_values, grouped):
            key = int(q_value)
            high_q_group_sums[key] = (
                high_q_group_sums.get(key, 0j) + contribution)

    row_values = np.array([
        np.sum(coefficients * np.exp(2j * np.pi * frequencies * ell))
        for ell in range(ell_first, ell_first + row_count)])
    incomplete_energy = float(np.mean(np.abs(row_values) ** 2))
    boundary = incomplete_energy - complete_energy
    signed_real = signed_bins.real / complete_energy
    absolute = absolute_bins / complete_energy
    high_q_signed = float(np.sum(signed_real[2:]))
    high_q_absolute = float(np.sum(absolute[2:]))
    fixed_q_residual = float(sum(
        abs(value) for value in high_q_group_sums.values()))
    fixed_q_residual_over_complete = fixed_q_residual / complete_energy
    ranked_packets = sorted(
        high_q_group_sums.items(), key=lambda item: abs(item[1]),
        reverse=True)
    packet_magnitudes = np.array(
        [abs(value) for _, value in ranked_packets], dtype=float)
    cumulative_packet_mass = np.cumsum(packet_magnitudes)

    def packet_count_for_fraction(fraction):
        if fixed_q_residual == 0:
            return 0
        return int(np.searchsorted(
            cumulative_packet_mass, fraction * fixed_q_residual) + 1)

    top_packet_shares = tuple(
        float(np.sum(packet_magnitudes[:count]) / fixed_q_residual)
        if fixed_q_residual else 0.0
        for count in (1, 5, 10, 20))
    effective_packet_count = (
        fixed_q_residual ** 2 / float(np.sum(packet_magnitudes ** 2))
        if fixed_q_residual else 0.0)
    reciprocal_q_sum = float(sum(
        1 / q_value for q_value in high_q_group_sums))
    q_weighted_packet_square_sum = float(sum(
        q_value * abs(value) ** 2
        for q_value, value in high_q_group_sums.items()))
    weighted_cauchy_bound = math.sqrt(
        reciprocal_q_sum * q_weighted_packet_square_sum)
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
        "high_Q_distinct_denominator_count": len(high_q_group_sums),
        "high_Q_denominators": tuple(sorted(high_q_group_sums)),
        "high_Q_top_1_5_10_20_packet_shares": top_packet_shares,
        "high_Q_half_mass_packet_count": packet_count_for_fraction(.5),
        "high_Q_ninety_percent_mass_packet_count": (
            packet_count_for_fraction(.9)),
        "high_Q_effective_packet_count": effective_packet_count,
        "high_Q_reciprocal_denominator_sum": reciprocal_q_sum,
        "high_Q_Q_weighted_packet_square_over_complete_squared": (
            q_weighted_packet_square_sum / complete_energy ** 2),
        "high_Q_weighted_cauchy_bound_over_complete": (
            weighted_cauchy_bound / complete_energy),
        "high_Q_weighted_cauchy_slack_over_packet_sum": (
            weighted_cauchy_bound / fixed_q_residual
            if fixed_q_residual else 0.0),
        "top_high_Q_packets": tuple(
            (int(q_value),
             float(abs(value) / complete_energy),
             float(value.real / complete_energy))
            for q_value, value in ranked_packets[:10]),
        "high_Q_fixed_Q_residual_over_complete": (
            fixed_q_residual_over_complete),
        "high_Q_within_Q_residual_over_pair_envelope": (
            fixed_q_residual_over_complete / high_q_absolute
            if high_q_absolute else 0.0),
        "high_Q_across_Q_residual": (
            abs(high_q_signed) / fixed_q_residual_over_complete
            if fixed_q_residual_over_complete else 0.0),
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
            receipt = signed_difference_bin_receipt(
                modulus, 46, 46, 69, 4, 20, replace_signs)
            print({key: receipt[key] for key in (
                "modulus", "conductor_coefficient_mode",
                "high_Q_signed_over_complete",
                "high_Q_absolute_over_complete",
                "high_Q_fixed_Q_residual_over_complete",
                "high_Q_top_1_5_10_20_packet_shares",
                "high_Q_half_mass_packet_count",
                "high_Q_ninety_percent_mass_packet_count",
                "high_Q_effective_packet_count",
                "high_Q_weighted_cauchy_bound_over_complete",
                "high_Q_weighted_cauchy_slack_over_packet_sum",
                "high_Q_within_Q_residual_over_pair_envelope",
                "high_Q_across_Q_residual",
                "high_Q_net_over_absolute")})
