"""Projected count-four correlation in Ramanujan-interval Fourier modes."""

import math

import numpy as np

from lcm_sawtooth_cotangent_count import (
    _one_orientation_count_source_modes,
)
from lcm_sawtooth_cotangent_transform import (
    _primitive_cotangent_transform_formula,
)
from lcm_sawtooth_ramanujan_class_mean import _ramanujan_sum
from lcm_sawtooth_resonant_source_sectors import (
    _direct_fully_resonant_totals,
)


PROJECTED_LAGS = (130, 110)


def _imaginary_transform_table(denominator, period):
    base = np.asarray(tuple(
        _primitive_cotangent_transform_formula(
            denominator, frequency).imag
        for frequency in range(denominator)), dtype=np.float64)
    return base[np.arange(period) % denominator]


def _family_transform_factors(period, conductor, odd_partner):
    left = _imaginary_transform_table(conductor, period)
    right = _imaginary_transform_table(2 * odd_partner, period)
    negative_right = right[(-np.arange(period)) % period]
    return left, negative_right


def _projected_fourier_total(
        period, lag, left_family, right_family):
    common = math.gcd(lag, period)
    quotient = period // common
    if math.gcd(common, quotient) != 1:
        raise ValueError("projection requires coprime common and quotient")
    quotient_weights = np.asarray(tuple(
        _ramanujan_sum(quotient, frequency)
        for frequency in range(period)), dtype=np.float64)
    left_table, left_negative_partner = _family_transform_factors(
        period, *left_family)
    right_table, right_negative_partner = _family_transform_factors(
        period, *right_family)

    signed_by_spatial_frequency = []
    absolute_by_spatial_frequency = []
    contributing_spatial_frequencies = tuple(
        frequency for frequency in range(period)
        if math.gcd(frequency, common) == 1)
    scale = common / (period * period)
    for spatial_frequency in contributing_spatial_frequencies:
        left_transform = -.25 * (
            (np.roll(left_table, -spatial_frequency) - left_table)
            * (np.roll(left_negative_partner, -spatial_frequency)
               - left_negative_partner))
        right_transform = -.25 * (
            (np.roll(right_table, -spatial_frequency) - right_table)
            * (np.roll(right_negative_partner, -spatial_frequency)
               - right_negative_partner))
        summands = scale * quotient_weights * left_transform * right_transform
        signed_by_spatial_frequency.append(float(np.sum(summands)))
        absolute_by_spatial_frequency.append(float(np.sum(np.abs(summands))))
    signed_total = math.fsum(signed_by_spatial_frequency)
    absolute_mass = math.fsum(absolute_by_spatial_frequency)
    return {
        "gcd_lag_period": common,
        "quotient_period": quotient,
        "contributing_spatial_frequency_count": len(
            contributing_spatial_frequencies),
        "signed_total": signed_total,
        "absolute_fourier_mass": absolute_mass,
        "fourier_cancellation_quotient": (
            abs(signed_total) / absolute_mass if absolute_mass else None),
    }


def projected_fourier_cancellation_receipt(
        families=((77, 65), (143, 35)), lags=PROJECTED_LAGS,
        strong_maximum_cancellation_quotient=.25,
        weak_minimum_cancellation_quotient=.50, tolerance=1e-12):
    families = tuple(families)
    lags = tuple(lags)
    if (len(families) != 2 or any(len(family) != 2 for family in families)
            or any(type(c) is not int or c < 3 or c % 2 == 0
                   or type(d) is not int or d < 3 or d % 2 == 0
                   for c, d in families)):
        raise ValueError("require two odd conductor-partner families")
    periods = tuple(math.lcm(c, 2 * d) for c, d in families)
    if len(set(periods)) != 1:
        raise ValueError("families must share one arithmetic period")
    period = periods[0]
    if (len(lags) != 2
            or any(type(lag) is not int or not 0 < lag < period
                   for lag in lags)):
        raise ValueError("require two lags strictly inside the period")
    if not 0 < strong_maximum_cancellation_quotient <= 1:
        raise ValueError("strong maximum quotient must lie in (0,1]")
    if not 0 < weak_minimum_cancellation_quotient <= 1:
        raise ValueError("weak minimum quotient must lie in (0,1]")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    left_sources = _one_orientation_count_source_modes(
        period, *families[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *families[1])[2]
    rows = {}
    for lag in lags:
        row = _projected_fourier_total(
            period, lag, families[0], families[1])
        direct_frequency_totals = _direct_fully_resonant_totals(
            period, lag, left_sources, right_sources)
        direct_total = complex(np.sum(direct_frequency_totals))
        reconstruction_error = abs(row["signed_total"] - direct_total)
        reconstruction_natural_scale_relative_error = (
            reconstruction_error
            / max(1.0, row["absolute_fourier_mass"]))
        row.update({
            "direct_conditioned_total": (
                direct_total.real, direct_total.imag),
            "reconstruction_absolute_error": reconstruction_error,
            "reconstruction_natural_scale_relative_error": (
                reconstruction_natural_scale_relative_error),
            "projected_fourier_identity_passes": bool(
                reconstruction_natural_scale_relative_error <= tolerance),
        })
        rows[lag] = row

    strong_row = rows[lags[0]]
    weak_row = rows[lags[1]]
    strong_gate = bool(
        strong_row["fourier_cancellation_quotient"]
        <= strong_maximum_cancellation_quotient)
    weak_gate = bool(
        weak_row["fourier_cancellation_quotient"]
        >= weak_minimum_cancellation_quotient)
    return {
        "families": families,
        "arithmetic_period": period,
        "lags": lags,
        "rows": rows,
        "strong_quotient": strong_row["quotient_period"],
        "weak_quotient": weak_row["quotient_period"],
        "strong_maximum_cancellation_quotient": (
            strong_maximum_cancellation_quotient),
        "weak_minimum_cancellation_quotient": (
            weak_minimum_cancellation_quotient),
        "strong_cancellation_gate_passes": strong_gate,
        "weak_cancellation_gate_passes": weak_gate,
        "fourier_cancellation_discriminator_passes": bool(
            strong_gate and weak_gate),
        "all_projected_fourier_identities_pass": all(
            row["projected_fourier_identity_passes"]
            for row in rows.values()),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(projected_fourier_cancellation_receipt())
