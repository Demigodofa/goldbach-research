"""Two-dimensional Fourier factorization of cotangent-only source modes."""

import math

import numpy as np

from lcm_sawtooth_cotangent_count import (
    _one_orientation_count_source_modes,
)
from lcm_sawtooth_cotangent_transform import (
    _primitive_cotangent_transform_formula,
)
from lcm_sawtooth_ramanujan_class_mean import _ramanujan_sum


SOURCE_FOURIER_STEPS = (1, 70, 77, 91, 110, 130, 143)


def _direct_positive_source_transform(period, sources, spatial_step):
    collapsed = np.zeros(period, dtype=complex)
    for source_residue, modes in sources.items():
        collapsed[source_residue] = sum(
            coefficient * np.exp(
                2j * np.pi
                * ((spatial_step * spatial_frequency) % period) / period)
            for spatial_frequency, coefficient in modes.items())
    # NumPy's inverse FFT has the positive exponent and a 1/period factor.
    return period * np.fft.ifft(collapsed)


def _source_transform_factor_formula(
        period, conductor, odd_partner, source_frequency, spatial_step):
    doubled_partner = 2 * odd_partner
    left_at_shift = _primitive_cotangent_transform_formula(
        conductor, source_frequency + spatial_step)
    left_at_base = _primitive_cotangent_transform_formula(
        conductor, source_frequency)
    right_at_shift = _primitive_cotangent_transform_formula(
        doubled_partner, -source_frequency - spatial_step)
    right_at_base = _primitive_cotangent_transform_formula(
        doubled_partner, -source_frequency)
    return .25 * ((left_at_shift - left_at_base)
                  * (right_at_shift - right_at_base))


def _source_transform_factor_natural_scale(
        conductor, odd_partner, source_frequency, spatial_step,
        source_absolute_mass):
    doubled_partner = 2 * odd_partner
    left_at_shift = _primitive_cotangent_transform_formula(
        conductor, source_frequency + spatial_step)
    left_at_base = _primitive_cotangent_transform_formula(
        conductor, source_frequency)
    right_at_shift = _primitive_cotangent_transform_formula(
        doubled_partner, -source_frequency - spatial_step)
    right_at_base = _primitive_cotangent_transform_formula(
        doubled_partner, -source_frequency)
    return max(1.0, source_absolute_mass, .25 * (
        abs(left_at_shift * right_at_shift)
        + abs(left_at_shift * right_at_base)
        + abs(left_at_base * right_at_shift)
        + abs(left_at_base * right_at_base)))


def _unit_step_ramanujan_error(denominator, frequency):
    transform_difference = (
        _primitive_cotangent_transform_formula(denominator, frequency + 1)
        - _primitive_cotangent_transform_formula(denominator, frequency))
    ramanujan_boundary = 1j * (
        _ramanujan_sum(denominator, frequency)
        + _ramanujan_sum(denominator, frequency + 1))
    return abs(transform_difference - ramanujan_boundary)


def _ramanujan_interval_transform_difference(
        denominator, frequency, step):
    return 1j * (
        _ramanujan_sum(denominator, frequency)
        + _ramanujan_sum(denominator, frequency + step)
        + 2 * sum(
            _ramanujan_sum(denominator, frequency + offset)
            for offset in range(1, step)))


def source_fourier_factorization_receipt(
        families=((77, 65), (143, 35)),
        spatial_steps=SOURCE_FOURIER_STEPS, tolerance=1e-12):
    families = tuple(families)
    spatial_steps = tuple(spatial_steps)
    if (len(families) != 2 or any(len(family) != 2 for family in families)
            or any(type(c) is not int or c < 3 or c % 2 == 0
                   or type(d) is not int or d < 3 or d % 2 == 0
                   for c, d in families)):
        raise ValueError("require two odd conductor-partner families")
    periods = tuple(math.lcm(c, 2 * d) for c, d in families)
    if len(set(periods)) != 1:
        raise ValueError("families must share one arithmetic period")
    period = periods[0]
    if (not spatial_steps
            or any(type(step) is not int or not 0 < step < period
                   for step in spatial_steps)):
        raise ValueError("spatial steps must lie strictly inside the period")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    endpoint_denominators = tuple(
        denominator
        for conductor, odd_partner in families
        for denominator in (conductor, 2 * odd_partner))
    ramanujan_rows = {}
    for denominator in endpoint_denominators:
        maximum_error = max(
            _unit_step_ramanujan_error(denominator, frequency)
            for frequency in range(denominator))
        interval_step_errors = {
            step: max(
                abs(
                    _primitive_cotangent_transform_formula(
                        denominator, frequency + step)
                    - _primitive_cotangent_transform_formula(
                        denominator, frequency)
                    - _ramanujan_interval_transform_difference(
                        denominator, frequency, step))
                for frequency in range(denominator))
            for step in spatial_steps}
        ramanujan_rows[denominator] = {
            "maximum_unit_step_absolute_error": maximum_error,
            "maximum_interval_step_absolute_error": max(
                interval_step_errors.values()),
            "interval_step_errors": interval_step_errors,
            "unit_step_ramanujan_identity_passes": bool(
                maximum_error <= tolerance),
            "all_interval_step_ramanujan_identities_pass": all(
                error <= tolerance
                for error in interval_step_errors.values()),
        }

    family_rows = {}
    for family in families:
        conductor, odd_partner = family
        count_two_sources = _one_orientation_count_source_modes(
            period, conductor, odd_partner)[2]
        source_absolute_mass = sum(
            abs(coefficient)
            for modes in count_two_sources.values()
            for coefficient in modes.values())
        step_rows = {}
        for spatial_step in spatial_steps:
            direct_values = _direct_positive_source_transform(
                period, count_two_sources, spatial_step)
            maximum_absolute_error = 0.0
            maximum_natural_scale_relative_error = 0.0
            for source_frequency, direct in enumerate(direct_values):
                formula = _source_transform_factor_formula(
                    period, conductor, odd_partner,
                    source_frequency, spatial_step)
                error = abs(direct - formula)
                maximum_absolute_error = max(maximum_absolute_error, error)
                maximum_natural_scale_relative_error = max(
                    maximum_natural_scale_relative_error,
                    error / _source_transform_factor_natural_scale(
                        conductor, odd_partner,
                        source_frequency, spatial_step,
                        source_absolute_mass))
            step_rows[spatial_step] = {
                "maximum_absolute_error": maximum_absolute_error,
                "maximum_natural_scale_relative_error": (
                    maximum_natural_scale_relative_error),
                "source_fourier_factorization_passes": bool(
                    maximum_natural_scale_relative_error <= tolerance),
            }
        family_rows[family] = {
            "steps": step_rows,
            "all_source_fourier_factorizations_pass": all(
                row["source_fourier_factorization_passes"]
                for row in step_rows.values()),
        }

    return {
        "families": families,
        "arithmetic_period": period,
        "spatial_steps": spatial_steps,
        "ramanujan_rows": ramanujan_rows,
        "family_rows": family_rows,
        "maximum_unit_step_ramanujan_error": max(
            row["maximum_unit_step_absolute_error"]
            for row in ramanujan_rows.values()),
        "maximum_interval_step_ramanujan_error": max(
            row["maximum_interval_step_absolute_error"]
            for row in ramanujan_rows.values()),
        "maximum_source_factorization_natural_scale_relative_error": max(
            step_row["maximum_natural_scale_relative_error"]
            for family_row in family_rows.values()
            for step_row in family_row["steps"].values()),
        "all_unit_step_ramanujan_identities_pass": all(
            row["unit_step_ramanujan_identity_passes"]
            for row in ramanujan_rows.values()),
        "all_interval_step_ramanujan_identities_pass": all(
            row["all_interval_step_ramanujan_identities_pass"]
            for row in ramanujan_rows.values()),
        "all_source_fourier_factorizations_pass": all(
            row["all_source_fourier_factorizations_pass"]
            for row in family_rows.values()),
        "finite_difference_ramanujan_factorization_identified": True,
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(source_fourier_factorization_receipt())
