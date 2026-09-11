"""Compare explicit conductor-log statistics with the fitted axial scale.

For a conductor polynomial ``A_d L^2+B_d L+C_d``, its normalized vertex is

    t_d = -B_d/(2*A_d*L).

This module tests two positive, explicit candidates for the fitted moment-
curve parameter:

* the ``A_d^2 |G|^2``-weighted mean of ``t_d`` over every primitive frequency
  and prime in the complete block;
* the vertex of the largest conductor with nonzero quadratic coefficient,
  evaluated at the dyadic logarithmic midpoint.

The fitted parameter is supplied from the independently measured axial
moment-curve receipt.  These comparisons do not derive it.
"""

import math
from collections import defaultdict

import numpy as np

from lcm_sawtooth_incomplete_frequency import _quadratic_support_data
from lcm_sawtooth_lifted_endpoint_frame import _lifted_frequency_data
from mobius_covariance_endpoint_probe import _prime_flags


def project_effective_log_statistics(scale_modulus, fitted_parameter):
    """Compare two conductor-vertex statistics with a supplied fitted ``t``."""
    if (type(scale_modulus) is not int or scale_modulus < 17
            or not math.isfinite(fitted_parameter)):
        raise ValueError("require scale_modulus>=17 and a finite fit")
    inferred_n = scale_modulus ** (1 / .59)
    row_count = int(inferred_n ** .41)
    divisor_lower = int(inferred_n ** .15)
    divisor_upper = int(inferred_n ** .32)
    ell_freeze = row_count + row_count // 2
    flags = _prime_flags(2 * scale_modulus)

    weighted_vertex_sum = 0.0
    total_weight = 0.0
    conductor_weights = defaultdict(float)
    prime_count = 0
    for modulus in range(scale_modulus, 2 * scale_modulus + 1):
        if not flags[modulus]:
            continue
        conductors, _, geometrics, coordinates = _lifted_frequency_data(
            modulus, ell_freeze, divisor_lower, divisor_upper)
        logarithm = math.log(modulus * ell_freeze)
        leading = coordinates[:, 0] / logarithm ** 2
        positive_leading = np.abs(leading) > 1e-14
        vertices = -coordinates[positive_leading, 1] / (
            2 * coordinates[positive_leading, 0])
        weights = (
            leading[positive_leading] ** 2
            * np.abs(geometrics[positive_leading]) ** 2)
        weighted_vertex_sum += float(weights @ vertices)
        total_weight += float(np.sum(weights))
        for conductor, weight in zip(
                conductors[positive_leading], weights):
            conductor_weights[int(conductor)] += float(weight)
        prime_count += 1
    if not total_weight:
        raise ArithmeticError("vertex statistic has zero total weight")
    weighted_mean = weighted_vertex_sum / total_weight

    midpoint_logarithm = math.log(
        math.sqrt(2) * scale_modulus * ell_freeze)
    conductor_vertices = []
    for conductor, polynomial in _quadratic_support_data(
            divisor_lower, divisor_upper)[1]:
        quadratic, linear, _ = polynomial
        if abs(quadratic) <= 1e-14:
            continue
        conductor_vertices.append((
            conductor, -linear / (2 * quadratic * midpoint_logarithm)))
    if not conductor_vertices:
        raise ArithmeticError("no quadratic conductor polynomial")
    largest_conductor, largest_vertex = max(conductor_vertices)
    polynomials = dict(_quadratic_support_data(
        divisor_lower, divisor_upper)[1])
    maximum_weight_conductor = max(
        conductor_weights, key=conductor_weights.get)
    maximum_weight_polynomial = polynomials[maximum_weight_conductor]
    maximum_weight_vertex = -maximum_weight_polynomial[1] / (
        2 * maximum_weight_polynomial[0] * midpoint_logarithm)

    weighted_error = weighted_mean - fitted_parameter
    endpoint_error = largest_vertex - fitted_parameter
    maximum_weight_error = maximum_weight_vertex - fitted_parameter
    return {
        "scale_modulus": scale_modulus,
        "prime_count": prime_count,
        "row_count": row_count,
        "ell_freeze": ell_freeze,
        "divisor_range": (divisor_lower, divisor_upper),
        "fitted_moment_curve_parameter": fitted_parameter,
        "leading_energy_weighted_vertex_mean": weighted_mean,
        "weighted_vertex_mean_error": weighted_error,
        "weighted_vertex_mean_within_one_hundredth": bool(
            abs(weighted_error) <= .01),
        "largest_quadratic_conductor": largest_conductor,
        "largest_conductor_midpoint_vertex": largest_vertex,
        "largest_conductor_vertex_error": endpoint_error,
        "largest_conductor_vertex_within_one_hundredth": bool(
            abs(endpoint_error) <= .01),
        "maximum_weight_quadratic_conductor": maximum_weight_conductor,
        "maximum_weight_conductor_share": (
            conductor_weights[maximum_weight_conductor] / total_weight),
        "maximum_weight_conductor_midpoint_vertex": maximum_weight_vertex,
        "maximum_weight_conductor_vertex_error": maximum_weight_error,
        "maximum_weight_conductor_vertex_within_one_hundredth": bool(
            abs(maximum_weight_error) <= .01),
        "fitted_parameter_supplied_not_derived": True,
        "uniform_effective_log_formula_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(project_effective_log_statistics(127, .2795716513419446))
