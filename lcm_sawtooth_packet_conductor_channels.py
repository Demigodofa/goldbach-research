"""Split one exact-Q packet by its unordered conductor pair.

For frequencies carried by primitive conductors ``d`` and ``e``, this receipt
groups their signed row-mean contribution according to ``{d,e}`` after the
difference frequency has been reduced to a named denominator ``Q``. It tests
whether several arithmetic conductor channels reinforce inside an exceptional
exact-Q packet. The finite decomposition proves no uniform packet estimate.
"""

import math

import numpy as np

from lcm_sawtooth_reduced_difference_mass import _validate_inputs
from lcm_sawtooth_signed_difference_bins import _signed_frequency_data


def packet_conductor_channel_receipt(
        modulus, ell_first, row_count, ell_freeze,
        divisor_lower, divisor_upper, target_denominator):
    """Return the exact signed conductor-channel split for one packet."""
    _validate_inputs(
        modulus, ell_freeze, row_count, divisor_lower, divisor_upper)
    if type(ell_first) is not int or ell_first < 1:
        raise ValueError("ell_first must be a positive integer")
    if type(target_denominator) is not int or target_denominator <= 1:
        raise ValueError("target_denominator must be an integer > 1")

    denominators, numerators, coefficients, _ = _signed_frequency_data(
        modulus, ell_freeze, divisor_lower, divisor_upper, False)
    complete_energy = float(np.sum(np.abs(coefficients) ** 2))
    channel_sums = {}
    channel_counts = {}
    channel_near_sums = {}
    channel_near_counts = {}
    channel_absolute_sums = {}
    channel_near_absolute_sums = {}
    channel_endpoint_sums = {}
    channel_term_magnitudes = {}
    channel_terms = {}
    chunk_size = 64
    for first in range(0, len(coefficients), chunk_size):
        left_d = denominators[first:first + chunk_size, None]
        left_k = numerators[first:first + chunk_size, None]
        common = np.lcm(left_d, denominators[None, :])
        difference_numerator = (
            left_k * (common // left_d)
            - numerators[None, :] * (common // denominators[None, :]))
        common_factor = np.gcd(np.abs(difference_numerator), common)
        reduced = common // common_factor
        selected = reduced == target_denominator
        if not np.any(selected):
            continue
        residues = (
            modulus
            * (difference_numerator[selected] // common_factor[selected])
            % target_denominator).astype(np.int64)
        roots = np.exp(2j * np.pi * residues / target_denominator)
        kernels = (
            np.exp(
                2j * np.pi * residues * ell_first / target_denominator)
            * (1 - roots ** row_count)
            / (row_count * (1 - roots)))
        products = (
            coefficients[first:first + chunk_size, None]
            * np.conjugate(coefficients[None, :]))
        contributions = products[selected] * kernels
        left_values = np.broadcast_to(left_d, common.shape)[selected]
        right_values = np.broadcast_to(
            denominators[None, :], common.shape)[selected]
        left_numerators = np.broadcast_to(
            left_k, common.shape)[selected]
        right_numerators = np.broadcast_to(
            numerators[None, :], common.shape)[selected]
        for left, right, left_numerator, right_numerator, residue, contribution in zip(
                left_values, right_values, left_numerators,
                right_numerators, residues, contributions):
            pair = tuple(sorted((int(left), int(right))))
            channel_sums[pair] = channel_sums.get(pair, 0j) + contribution
            channel_counts[pair] = channel_counts.get(pair, 0) + 1
            magnitude = abs(contribution)
            channel_absolute_sums[pair] = (
                channel_absolute_sums.get(pair, 0.0) + magnitude)
            channel_term_magnitudes.setdefault(pair, []).append(magnitude)
            channel_terms.setdefault(pair, []).append((
                magnitude, int(left), int(left_numerator), int(right),
                int(right_numerator), int(residue), contribution))
            circular_residue = min(
                int(residue), target_denominator - int(residue))
            if circular_residue * row_count <= target_denominator:
                channel_near_sums[pair] = (
                    channel_near_sums.get(pair, 0j) + contribution)
                channel_near_counts[pair] = (
                    channel_near_counts.get(pair, 0) + 1)
                channel_near_absolute_sums[pair] = (
                    channel_near_absolute_sums.get(pair, 0.0) + magnitude)
            if (int(left_numerator) in (1, int(left) - 1)
                    and int(right_numerator) in (1, int(right) - 1)):
                channel_endpoint_sums[pair] = (
                    channel_endpoint_sums.get(pair, 0j) + contribution)

    if not channel_sums:
        raise ValueError("target denominator is absent")
    ranked = sorted(
        channel_sums.items(), key=lambda item: abs(item[1]), reverse=True)
    total = sum(channel_sums.values())
    absolute_sum = sum(abs(value) for value in channel_sums.values())
    channels = []
    for pair, value in ranked:
        near_value = channel_near_sums.get(pair, 0j)
        term_magnitudes = sorted(
            channel_term_magnitudes[pair], reverse=True)
        term_absolute_sum = channel_absolute_sums[pair]
        ranked_terms = sorted(
            channel_terms[pair], key=lambda item: item[0], reverse=True)
        channels.append({
            "conductors": pair,
            "conductor_lcm": math.lcm(*pair),
            "ordered_term_count": channel_counts[pair],
            "contribution_over_complete": float(value.real / complete_energy),
            "imaginary_error_over_complete": float(
                abs(value.imag) / complete_energy),
            "absolute_channel_share": float(abs(value) / absolute_sum),
            "near_resonant_ordered_term_fraction": float(
                channel_near_counts.get(pair, 0) / channel_counts[pair]),
            "near_resonant_signed_channel_fraction": float(
                near_value.real / value.real if value.real else 0.0),
            "endpoint_mode_signed_channel_fraction": float(
                channel_endpoint_sums.get(pair, 0j).real / value.real
                if value.real else 0.0),
            "endpoint_mode_contribution_over_complete": complex(
                channel_endpoint_sums.get(pair, 0j) / complete_energy),
            "near_resonant_absolute_envelope_fraction": float(
                channel_near_absolute_sums.get(pair, 0.0)
                / term_absolute_sum if term_absolute_sum else 0.0),
            "top_five_term_absolute_envelope_fraction": float(
                sum(term_magnitudes[:5]) / term_absolute_sum
                if term_absolute_sum else 0.0),
            "largest_ordered_terms": tuple({
                "left_frequency": (left_numerator, left),
                "right_frequency": (right_numerator, right),
                "reduced_numerator": residue,
                "circular_reduced_numerator": min(
                    residue, target_denominator - residue),
                "contribution_over_complete": complex(
                    contribution / complete_energy),
                "absolute_envelope_share": float(
                    magnitude / term_absolute_sum),
            } for (
                magnitude, left, left_numerator, right, right_numerator,
                residue, contribution) in ranked_terms[:10]),
        })
    channels = tuple(channels)
    return {
        "modulus": modulus,
        "ell_range": (ell_first, ell_first + row_count - 1),
        "ell_freeze": ell_freeze,
        "divisor_range": (divisor_lower, divisor_upper),
        "target_denominator": target_denominator,
        "near_resonant_circular_numerator_threshold": (
            target_denominator / row_count),
        "channel_count": len(channels),
        "packet_over_complete": float(total.real / complete_energy),
        "packet_imaginary_error_over_complete": float(
            abs(total.imag) / complete_energy),
        "channel_coherence_ratio": float(
            abs(total) / absolute_sum if absolute_sum else 0.0),
        "largest_absolute_channel_share": channels[0][
            "absolute_channel_share"],
        "channels": channels,
        "exact_conductor_channel_decomposition_proved": True,
        "uniform_channel_reinforcement_proved": False,
    }


if __name__ == "__main__":
    print(packet_conductor_channel_receipt(
        499, 46, 46, 69, 4, 20, 62985))
