"""Score coefficient-weighted near resonances among endpoint modes.

For every primitive conductor ``d``, retain only ``k=1`` and ``k=d-1`` in
the exact frozen-log frequency expansion. For distinct modes, reduce their
difference to ``r/Q`` and retain the high-denominator main lobe

    Q > m A,    min(r,Q-r) <= Q/A.

The score groups the actual signed row-mean contributions by exact ``Q`` and
forms ``A sum_Q Q |C_Q(endpoint,near)|^2 / E^2``. It is a finite predictor for
exceptional row alignment, not an upper bound for the omitted modes.
"""

import math

import numpy as np

from lcm_sawtooth_reduced_difference_mass import _validate_inputs
from lcm_sawtooth_signed_difference_bins import _signed_frequency_data


def endpoint_reduced_denominator(left, right, left_sign, right_sign):
    """Return the reduced denominator of sign/difference endpoints."""
    if (any(type(value) is not int for value in (
            left, right, left_sign, right_sign))
            or left <= 1 or right <= 1
            or left_sign not in (-1, 1) or right_sign not in (-1, 1)):
        raise ValueError("invalid endpoint denominator inputs")
    common_factor = math.gcd(left, right)
    primitive_numerator = (
        left_sign * (right // common_factor)
        - right_sign * (left // common_factor))
    return math.lcm(left, right) // math.gcd(
        common_factor, abs(primitive_numerator))


def endpoint_resonance_score_receipt(
        modulus, ell_first, row_count, ell_freeze,
        divisor_lower, divisor_upper):
    """Return the exact endpoint/main-lobe score at one prime modulus."""
    _validate_inputs(
        modulus, ell_freeze, row_count, divisor_lower, divisor_upper)
    if type(ell_first) is not int or ell_first < 1:
        raise ValueError("ell_first must be a positive integer")

    denominators, numerators, coefficients, _ = _signed_frequency_data(
        modulus, ell_freeze, divisor_lower, divisor_upper, False)
    complete_energy = float(np.sum(np.abs(coefficients) ** 2))
    endpoint = (numerators == 1) | (numerators == denominators - 1)
    denominators = denominators[endpoint]
    numerators = numerators[endpoint]
    coefficients = coefficients[endpoint]

    left_d = denominators[:, None]
    left_k = numerators[:, None]
    common = np.lcm(left_d, denominators[None, :])
    difference_numerator = (
        left_k * (common // left_d)
        - numerators[None, :] * (common // denominators[None, :]))
    common_factor = np.gcd(np.abs(difference_numerator), common)
    reduced = common // common_factor
    reduced_numerator = np.zeros(reduced.shape, dtype=np.int64)
    nonzero = reduced > 1
    reduced_numerator[nonzero] = (
        modulus
        * (difference_numerator[nonzero] // common_factor[nonzero])
        % reduced[nonzero])
    circular = np.minimum(reduced_numerator, reduced - reduced_numerator)
    high_q = reduced > modulus * row_count
    selected = (
        high_q
        & (circular * row_count <= reduced))

    selected_q = reduced[selected]
    selected_r = reduced_numerator[selected]
    roots = np.exp(2j * np.pi * selected_r / selected_q)
    kernels = (
        np.exp(2j * np.pi * selected_r * ell_first / selected_q)
        * (1 - roots ** row_count)
        / (row_count * (1 - roots)))
    products = coefficients[:, None] * np.conjugate(coefficients[None, :])
    product_magnitudes = np.abs(products)
    contributions = products[selected] * kernels
    q_values, inverse, q_multiplicities = np.unique(
        selected_q, return_inverse=True, return_counts=True)
    grouped = (
        np.bincount(inverse, weights=contributions.real)
        + 1j * np.bincount(inverse, weights=contributions.imag))
    grouped_term_squares = np.bincount(
        inverse, weights=np.abs(contributions) ** 2)
    ranked = sorted(
        zip(q_values, grouped), key=lambda item: abs(item[1]), reverse=True)
    score = row_count * sum(
        int(q_value) * abs(value) ** 2
        for q_value, value in ranked) / complete_energy ** 2
    cauchy_score_bound = row_count * float(np.sum(
        q_values * q_multiplicities * grouped_term_squares)
        / complete_energy ** 2)
    direct_sum = np.sum(contributions)
    grouped_sum = np.sum(grouped)
    absolute_envelope = float(np.sum(np.abs(contributions)))
    high_q_product_weight = float(np.sum(product_magnitudes[high_q]))
    near_product_weight = float(np.sum(product_magnitudes[selected]))
    squared_product_weights = reduced * product_magnitudes ** 2
    high_q_Q_squared_product_weight = float(np.sum(
        squared_product_weights[high_q]))
    near_Q_squared_product_weight = float(np.sum(
        squared_product_weights[selected]))
    return {
        "modulus": modulus,
        "ell_range": (ell_first, ell_first + row_count - 1),
        "ell_freeze": ell_freeze,
        "divisor_range": (divisor_lower, divisor_upper),
        "complete_energy": complete_energy,
        "endpoint_frequency_count": len(coefficients),
        "high_Q_endpoint_ordered_pair_count": int(np.sum(high_q)),
        "near_high_Q_ordered_pair_count": int(np.sum(selected)),
        "near_high_Q_ordered_pair_fraction": float(
            np.sum(selected) / np.sum(high_q) if np.sum(high_q) else 0.0),
        "row_count_scaled_near_high_Q_pair_fraction": float(
            row_count * np.sum(selected) / np.sum(high_q)
            if np.sum(high_q) else 0.0),
        "high_Q_endpoint_coefficient_product_weight": high_q_product_weight,
        "near_high_Q_endpoint_coefficient_product_weight": (
            near_product_weight),
        "near_high_Q_coefficient_weight_fraction": float(
            near_product_weight / high_q_product_weight
            if high_q_product_weight else 0.0),
        "row_count_scaled_near_coefficient_weight_fraction": float(
            row_count * near_product_weight / high_q_product_weight
            if high_q_product_weight else 0.0),
        "high_Q_Q_weighted_squared_coefficient_product": (
            high_q_Q_squared_product_weight),
        "high_Q_Q_weighted_squared_coefficient_product_over_complete_squared": (
            high_q_Q_squared_product_weight / complete_energy ** 2),
        "near_high_Q_Q_weighted_squared_coefficient_product": (
            near_Q_squared_product_weight),
        "row_count_scaled_near_Q_squared_product_weight_fraction": float(
            row_count * near_Q_squared_product_weight
            / high_q_Q_squared_product_weight
            if high_q_Q_squared_product_weight else 0.0),
        "near_high_Q_exact_denominator_count": len(q_values),
        "maximum_near_exact_Q_ordered_pair_multiplicity": int(
            np.max(q_multiplicities) if len(q_multiplicities) else 0),
        "endpoint_near_Q_weighted_square_score": float(score),
        "endpoint_near_packet_cauchy_score_bound": cauchy_score_bound,
        "endpoint_near_packet_cauchy_slack": float(
            cauchy_score_bound / score if score else 0.0),
        "endpoint_near_signed_sum_over_complete": float(
            grouped_sum.real / complete_energy),
        "endpoint_near_imaginary_error_over_complete": float(
            abs(grouped_sum.imag) / complete_energy),
        "endpoint_near_absolute_envelope_over_complete": float(
            absolute_envelope / complete_energy),
        "largest_endpoint_near_packets": tuple(
            (int(q_value), complex(value / complete_energy))
            for q_value, value in ranked[:10]),
        "packet_grouping_error_over_complete": float(
            abs(direct_sum - grouped_sum) / complete_energy),
        "finite_endpoint_resonance_score": True,
        "endpoint_score_controls_all_modes_proved": False,
    }


if __name__ == "__main__":
    print(endpoint_resonance_score_receipt(509, 46, 46, 69, 4, 20))
