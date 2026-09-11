"""Projected count-four correlation in Ramanujan-interval Fourier modes."""

import math
from fractions import Fraction

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
TWO_PRIME_QUOTIENT_LAGS = {
    35: 286,
    55: 182,
    65: 154,
    77: 130,
    91: 110,
    143: 70,
}
COUNT_FOUR_RECOMBINATION_TARGETS = {
    35: .16118908808873234,
    55: .3024507788824479,
    65: .014327564985042195,
    77: .06505818067801658,
    91: .5047491987897079,
    143: .09820822341044044,
}
THREE_PRIME_QUOTIENT_LAGS = {
    385: 156,
    455: 22,
    715: 14,
    1001: 240,
}
THREE_PRIME_COUNT_FOUR_RECOMBINATION_TARGETS = {
    385: .11745372514454311,
    455: .4861020851341751,
    715: .21612322122320057,
    1001: .4110607307856016,
}
ALTERNATE_GEOMETRY_FAMILIES = ((35, 143), (65, 77))
ALTERNATE_GEOMETRY_COUNT_FOUR_RECOMBINATION_TARGETS = {
    35: .012964790897655157,
    55: .022032024950575643,
    65: .05159105243056866,
    77: .5443296939839037,
    91: .4838958192651274,
    143: .4693160590983769,
}
NEW_PERIOD_FAMILIES = ((15, 77), (35, 33))
NEW_PERIOD_QUOTIENT_LAGS = {
    15: 154,
    21: 110,
    33: 70,
    35: 66,
    55: 42,
    77: 30,
}
NEW_PERIOD_COUNT_FOUR_RECOMBINATION_TARGETS = {
    15: .19063100974135774,
    21: .4546991458454955,
    33: .8543139343134691,
    35: .8244946861984153,
    55: .74187635170919,
    77: .47766150264034346,
}
NEW_PERIOD_ANALOG_FAMILIES = ((77, 15), (33, 35))
NEW_PERIOD_ANALOG_COUNT_FOUR_RECOMBINATION_TARGETS = {
    15: .34979821428574304,
    21: .2045342414078927,
    33: .2913249193588369,
    35: .16215960958670428,
    55: .2541893677464353,
    77: .3018103161208625,
}
BRIDGE_CONFIRMATION_FAMILIES = ((21, 55), (55, 21))
BRIDGE_CONFIRMATION_COUNT_FOUR_RECOMBINATION_TARGETS = {
    15: .19999999999999582,
    21: .7500000000000012,
    33: .41666666666666624,
    35: .29999999999999455,
    55: .7692307692307678,
    77: .6249999999999973,
}


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


def _q2310_exact_projected_signed_total(lag, families):
    period = 2310
    common = math.gcd(lag, period)
    quotient = period // common
    quotient_weights = np.asarray(tuple(
        _ramanujan_sum(quotient, frequency)
        for frequency in range(period)), dtype=np.int64)
    tables = []
    for conductor, odd_partner in families:
        left = _imaginary_transform_table(
            conductor, period).astype(np.int64)
        right = _imaginary_transform_table(
            2 * odd_partner, period).astype(np.int64)
        tables.append((left, right[(-np.arange(period)) % period]))
    unscaled_numerator = 0
    for spatial_frequency in range(period):
        if math.gcd(spatial_frequency, common) != 1:
            continue
        products = quotient_weights.copy()
        for left, negative_right in tables:
            products *= np.roll(left, -spatial_frequency) - left
            products *= (
                np.roll(negative_right, -spatial_frequency)
                - negative_right)
        unscaled_numerator += sum(int(value) for value in products)
    return (
        Fraction(
            common * unscaled_numerator,
            16 * period * period),
        unscaled_numerator)


def _projected_fourier_identity_row(
        period, lag, families, left_sources, right_sources, tolerance):
    row = _projected_fourier_total(
        period, lag, families[0], families[1])
    direct_frequency_totals = _direct_fully_resonant_totals(
        period, lag, left_sources, right_sources)
    direct_total = complex(np.sum(direct_frequency_totals))
    direct_recombined_absolute_mass = float(np.sum(
        np.abs(direct_frequency_totals)))
    raw_signed_frequency_coherence = (
        abs(direct_total) / direct_recombined_absolute_mass
        if direct_recombined_absolute_mass else None)
    if (raw_signed_frequency_coherence is not None
            and raw_signed_frequency_coherence > 1 + tolerance):
        raise AssertionError("frequency coherence exceeds one beyond tolerance")
    reconstruction_error = abs(row["signed_total"] - direct_total)
    reconstruction_natural_scale_relative_error = (
        reconstruction_error / max(1.0, row["absolute_fourier_mass"]))
    row.update({
        "direct_conditioned_total": (direct_total.real, direct_total.imag),
        "direct_recombined_absolute_mass": (
            direct_recombined_absolute_mass),
        "raw_signed_frequency_coherence": raw_signed_frequency_coherence,
        "signed_frequency_coherence": (
            min(1.0, raw_signed_frequency_coherence)
            if raw_signed_frequency_coherence is not None else None),
        "reconstruction_absolute_error": reconstruction_error,
        "reconstruction_natural_scale_relative_error": (
            reconstruction_natural_scale_relative_error),
        "projected_fourier_identity_passes": bool(
            reconstruction_natural_scale_relative_error <= tolerance),
    })
    return row


def _average_ranks(values):
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    start = 0
    while start < len(order):
        stop = start + 1
        while stop < len(order) and values[order[stop]] == values[order[start]]:
            stop += 1
        average_rank = (start + stop - 1) / 2
        for position in range(start, stop):
            ranks[order[position]] = average_rank
        start = stop
    return tuple(ranks)


def _pearson_correlation(left, right):
    left_mean = math.fsum(left) / len(left)
    right_mean = math.fsum(right) / len(right)
    centered_left = tuple(value - left_mean for value in left)
    centered_right = tuple(value - right_mean for value in right)
    denominator = math.sqrt(
        math.fsum(value * value for value in centered_left)
        * math.fsum(value * value for value in centered_right))
    if denominator == 0:
        return None
    return math.fsum(
        left_value * right_value
        for left_value, right_value in zip(
            centered_left, centered_right)) / denominator


def _spearman_correlation(left, right):
    return _pearson_correlation(_average_ranks(left), _average_ranks(right))


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
        rows[lag] = _projected_fourier_identity_row(
            period, lag, families, left_sources, right_sources, tolerance)

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


def two_prime_projected_fourier_holdout_receipt(
        minimum_holdout_spearman_correlation=.8, tolerance=1e-12):
    if not -1 <= minimum_holdout_spearman_correlation <= 1:
        raise ValueError("minimum Spearman correlation must lie in [-1,1]")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    families = ((77, 65), (143, 35))
    period = 10010
    left_sources = _one_orientation_count_source_modes(
        period, *families[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *families[1])[2]
    rows = {
        quotient: _projected_fourier_identity_row(
            period, lag, families, left_sources, right_sources, tolerance)
        for quotient, lag in TWO_PRIME_QUOTIENT_LAGS.items()}
    fourier_quotients = {
        quotient: row["fourier_cancellation_quotient"]
        for quotient, row in rows.items()}
    holdout_quotients = (35, 55, 65, 143)
    holdout_spearman = _spearman_correlation(
        tuple(fourier_quotients[q] for q in holdout_quotients),
        tuple(COUNT_FOUR_RECOMBINATION_TARGETS[q]
              for q in holdout_quotients))
    all_quotients = tuple(TWO_PRIME_QUOTIENT_LAGS)
    all_six_spearman = _spearman_correlation(
        tuple(fourier_quotients[q] for q in all_quotients),
        tuple(COUNT_FOUR_RECOMBINATION_TARGETS[q] for q in all_quotients))
    return {
        "families": families,
        "arithmetic_period": period,
        "quotients": tuple(TWO_PRIME_QUOTIENT_LAGS),
        "discovery_quotients": (77, 91),
        "holdout_quotients": holdout_quotients,
        "fourier_cancellation_quotients": fourier_quotients,
        "count_four_recombination_quotients": (
            COUNT_FOUR_RECOMBINATION_TARGETS.copy()),
        "holdout_spearman_correlation": holdout_spearman,
        "all_six_spearman_correlation": all_six_spearman,
        "minimum_holdout_spearman_correlation": (
            minimum_holdout_spearman_correlation),
        "holdout_rank_gate_passes": bool(
            holdout_spearman is not None
            and holdout_spearman >= minimum_holdout_spearman_correlation),
        "all_projected_fourier_identities_pass": all(
            row["projected_fourier_identity_passes"]
            for row in rows.values()),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def three_prime_projected_fourier_holdout_receipt(
        minimum_spearman_correlation=.8, tolerance=1e-12):
    if not -1 <= minimum_spearman_correlation <= 1:
        raise ValueError("minimum Spearman correlation must lie in [-1,1]")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    families = ((77, 65), (143, 35))
    period = 10010
    left_sources = _one_orientation_count_source_modes(
        period, *families[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *families[1])[2]
    rows = {
        quotient: _projected_fourier_identity_row(
            period, lag, families, left_sources, right_sources, tolerance)
        for quotient, lag in THREE_PRIME_QUOTIENT_LAGS.items()}
    fourier_quotients = {
        quotient: row["fourier_cancellation_quotient"]
        for quotient, row in rows.items()}
    quotients = tuple(THREE_PRIME_QUOTIENT_LAGS)
    spearman = _spearman_correlation(
        tuple(fourier_quotients[q] for q in quotients),
        tuple(THREE_PRIME_COUNT_FOUR_RECOMBINATION_TARGETS[q]
              for q in quotients))
    return {
        "families": families,
        "arithmetic_period": period,
        "quotients": quotients,
        "fourier_cancellation_quotients": fourier_quotients,
        "count_four_recombination_quotients": (
            THREE_PRIME_COUNT_FOUR_RECOMBINATION_TARGETS.copy()),
        "spearman_correlation": spearman,
        "minimum_spearman_correlation": minimum_spearman_correlation,
        "rank_gate_passes": bool(
            spearman is not None
            and spearman >= minimum_spearman_correlation),
        "maximum_reconstruction_natural_scale_relative_error": max(
            row["reconstruction_natural_scale_relative_error"]
            for row in rows.values()),
        "all_projected_fourier_identities_pass": all(
            row["projected_fourier_identity_passes"]
            for row in rows.values()),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def alternate_geometry_projected_fourier_holdout_receipt(
        minimum_spearman_correlation=.8, tolerance=1e-12):
    if not -1 <= minimum_spearman_correlation <= 1:
        raise ValueError("minimum Spearman correlation must lie in [-1,1]")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    families = ALTERNATE_GEOMETRY_FAMILIES
    period = 10010
    left_sources = _one_orientation_count_source_modes(
        period, *families[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *families[1])[2]
    rows = {
        quotient: _projected_fourier_identity_row(
            period, lag, families, left_sources, right_sources, tolerance)
        for quotient, lag in TWO_PRIME_QUOTIENT_LAGS.items()}
    fourier_quotients = {
        quotient: row["fourier_cancellation_quotient"]
        for quotient, row in rows.items()}
    quotients = tuple(TWO_PRIME_QUOTIENT_LAGS)
    spearman = _spearman_correlation(
        tuple(fourier_quotients[q] for q in quotients),
        tuple(ALTERNATE_GEOMETRY_COUNT_FOUR_RECOMBINATION_TARGETS[q]
              for q in quotients))
    return {
        "families": families,
        "arithmetic_period": period,
        "quotients": quotients,
        "fourier_cancellation_quotients": fourier_quotients,
        "count_four_recombination_quotients": (
            ALTERNATE_GEOMETRY_COUNT_FOUR_RECOMBINATION_TARGETS.copy()),
        "spearman_correlation": spearman,
        "minimum_spearman_correlation": minimum_spearman_correlation,
        "rank_gate_passes": bool(
            spearman is not None
            and spearman >= minimum_spearman_correlation),
        "maximum_reconstruction_natural_scale_relative_error": max(
            row["reconstruction_natural_scale_relative_error"]
            for row in rows.values()),
        "all_projected_fourier_identities_pass": all(
            row["projected_fourier_identity_passes"]
            for row in rows.values()),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def new_period_projected_fourier_holdout_receipt(
        minimum_spearman_correlation=.8, tolerance=1e-12):
    if not -1 <= minimum_spearman_correlation <= 1:
        raise ValueError("minimum Spearman correlation must lie in [-1,1]")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    families = NEW_PERIOD_FAMILIES
    period = 2310
    left_sources = _one_orientation_count_source_modes(
        period, *families[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *families[1])[2]
    rows = {
        quotient: _projected_fourier_identity_row(
            period, lag, families, left_sources, right_sources, tolerance)
        for quotient, lag in NEW_PERIOD_QUOTIENT_LAGS.items()}
    fourier_quotients = {
        quotient: row["fourier_cancellation_quotient"]
        for quotient, row in rows.items()}
    quotients = tuple(NEW_PERIOD_QUOTIENT_LAGS)
    spearman = _spearman_correlation(
        tuple(fourier_quotients[q] for q in quotients),
        tuple(NEW_PERIOD_COUNT_FOUR_RECOMBINATION_TARGETS[q]
              for q in quotients))
    return {
        "families": families,
        "arithmetic_period": period,
        "quotients": quotients,
        "fourier_cancellation_quotients": fourier_quotients,
        "count_four_recombination_quotients": (
            NEW_PERIOD_COUNT_FOUR_RECOMBINATION_TARGETS.copy()),
        "spearman_correlation": spearman,
        "minimum_spearman_correlation": minimum_spearman_correlation,
        "rank_gate_passes": bool(
            spearman is not None
            and spearman >= minimum_spearman_correlation),
        "maximum_reconstruction_natural_scale_relative_error": max(
            row["reconstruction_natural_scale_relative_error"]
            for row in rows.values()),
        "all_projected_fourier_identities_pass": all(
            row["projected_fourier_identity_passes"]
            for row in rows.values()),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def new_period_analog_projected_fourier_holdout_receipt(
        minimum_spearman_correlation=.8, tolerance=1e-12):
    if not -1 <= minimum_spearman_correlation <= 1:
        raise ValueError("minimum Spearman correlation must lie in [-1,1]")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    families = NEW_PERIOD_ANALOG_FAMILIES
    period = 2310
    left_sources = _one_orientation_count_source_modes(
        period, *families[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *families[1])[2]
    rows = {
        quotient: _projected_fourier_identity_row(
            period, lag, families, left_sources, right_sources, tolerance)
        for quotient, lag in NEW_PERIOD_QUOTIENT_LAGS.items()}
    fourier_quotients = {
        quotient: row["fourier_cancellation_quotient"]
        for quotient, row in rows.items()}
    quotients = tuple(NEW_PERIOD_QUOTIENT_LAGS)
    spearman = _spearman_correlation(
        tuple(fourier_quotients[q] for q in quotients),
        tuple(NEW_PERIOD_ANALOG_COUNT_FOUR_RECOMBINATION_TARGETS[q]
              for q in quotients))
    return {
        "families": families,
        "arithmetic_period": period,
        "quotients": quotients,
        "fourier_cancellation_quotients": fourier_quotients,
        "count_four_recombination_quotients": (
            NEW_PERIOD_ANALOG_COUNT_FOUR_RECOMBINATION_TARGETS.copy()),
        "spearman_correlation": spearman,
        "minimum_spearman_correlation": minimum_spearman_correlation,
        "rank_gate_passes": bool(
            spearman is not None
            and spearman >= minimum_spearman_correlation),
        "maximum_reconstruction_natural_scale_relative_error": max(
            row["reconstruction_natural_scale_relative_error"]
            for row in rows.values()),
        "all_projected_fourier_identities_pass": all(
            row["projected_fourier_identity_passes"]
            for row in rows.values()),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def q2310_bridge_distortion_receipt(
        minimum_failed_distortion=2.0,
        maximum_passing_distortion=1.5, tolerance=1e-12):
    if minimum_failed_distortion <= 1:
        raise ValueError("minimum failed distortion must exceed one")
    if maximum_passing_distortion < 1:
        raise ValueError("maximum passing distortion must be at least one")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    period = 2310
    geometries = {
        "failed_rank_geometry": (
            NEW_PERIOD_FAMILIES,
            NEW_PERIOD_COUNT_FOUR_RECOMBINATION_TARGETS),
        "passing_rank_geometry": (
            NEW_PERIOD_ANALOG_FAMILIES,
            NEW_PERIOD_ANALOG_COUNT_FOUR_RECOMBINATION_TARGETS),
    }
    geometry_rows = {}
    for name, (families, count_four_targets) in geometries.items():
        left_sources = _one_orientation_count_source_modes(
            period, *families[0])[2]
        right_sources = _one_orientation_count_source_modes(
            period, *families[1])[2]
        quotient_rows = {}
        for quotient, lag in NEW_PERIOD_QUOTIENT_LAGS.items():
            projected = _projected_fourier_identity_row(
                period, lag, families,
                left_sources, right_sources, tolerance)
            sector_quotient = count_four_targets[quotient]
            recombined_mass = projected[
                "direct_recombined_absolute_mass"]
            sectorwise_mass = recombined_mass / sector_quotient
            basis_inflation = (
                projected["absolute_fourier_mass"] / sectorwise_mass)
            frequency_coherence = projected[
                "raw_signed_frequency_coherence"]
            bridge_multiplier = basis_inflation / frequency_coherence
            bridge_identity_error = abs(
                bridge_multiplier
                - sector_quotient
                / projected["fourier_cancellation_quotient"])
            quotient_rows[quotient] = {
                "frequency_coherence": frequency_coherence,
                "basis_inflation": basis_inflation,
                "bridge_multiplier": bridge_multiplier,
                "bridge_identity_absolute_error": bridge_identity_error,
                "projected_fourier_identity_passes": projected[
                    "projected_fourier_identity_passes"],
            }
        multipliers = tuple(
            row["bridge_multiplier"] for row in quotient_rows.values())
        geometry_rows[name] = {
            "families": families,
            "quotients": quotient_rows,
            "bridge_distortion_range": max(multipliers) / min(multipliers),
            "maximum_bridge_identity_absolute_error": max(
                row["bridge_identity_absolute_error"]
                for row in quotient_rows.values()),
            "all_projected_fourier_identities_pass": all(
                row["projected_fourier_identity_passes"]
                for row in quotient_rows.values()),
        }
    failed_distortion = geometry_rows[
        "failed_rank_geometry"]["bridge_distortion_range"]
    passing_distortion = geometry_rows[
        "passing_rank_geometry"]["bridge_distortion_range"]
    return {
        "arithmetic_period": period,
        "geometries": geometry_rows,
        "minimum_failed_distortion": minimum_failed_distortion,
        "maximum_passing_distortion": maximum_passing_distortion,
        "failed_distortion_gate_passes": bool(
            failed_distortion >= minimum_failed_distortion),
        "passing_distortion_gate_passes": bool(
            passing_distortion <= maximum_passing_distortion),
        "exploratory_bridge_distortion_pattern_passes": bool(
            failed_distortion >= minimum_failed_distortion
            and passing_distortion <= maximum_passing_distortion),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def bridge_distortion_confirmation_receipt(
        maximum_stable_distortion=1.5,
        minimum_unstable_distortion=2.0,
        minimum_rank_correlation=.8, tolerance=1e-12):
    if maximum_stable_distortion < 1:
        raise ValueError("maximum stable distortion must be at least one")
    if minimum_unstable_distortion <= maximum_stable_distortion:
        raise ValueError("unstable distortion must exceed stable distortion")
    if not -1 <= minimum_rank_correlation <= 1:
        raise ValueError("minimum rank correlation must lie in [-1,1]")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    period = 2310
    families = BRIDGE_CONFIRMATION_FAMILIES
    left_sources = _one_orientation_count_source_modes(
        period, *families[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *families[1])[2]
    rows = {}
    for quotient, lag in NEW_PERIOD_QUOTIENT_LAGS.items():
        projected = _projected_fourier_identity_row(
            period, lag, families, left_sources, right_sources, tolerance)
        exact_signed_total, exact_unscaled_numerator = (
            _q2310_exact_projected_signed_total(lag, families))
        exact_signed_float = float(exact_signed_total)
        fourier_quotient = (
            abs(exact_signed_float) / projected["absolute_fourier_mass"])
        sector_quotient = (
            BRIDGE_CONFIRMATION_COUNT_FOUR_RECOMBINATION_TARGETS[quotient])
        recombined_mass = projected["direct_recombined_absolute_mass"]
        sectorwise_mass = recombined_mass / sector_quotient
        raw_frequency_coherence = (
            abs(exact_signed_float) / recombined_mass)
        basis_inflation = (
            projected["absolute_fourier_mass"] / sectorwise_mass)
        exact_zero = exact_unscaled_numerator == 0
        bridge_multiplier = (
            math.inf if exact_zero
            else basis_inflation / raw_frequency_coherence)
        bridge_identity_error = (
            None if exact_zero else abs(
                bridge_multiplier - sector_quotient / fourier_quotient))
        rows[quotient] = {
            "exact_unscaled_signed_numerator": exact_unscaled_numerator,
            "exact_signed_total": (
                exact_signed_total.numerator, exact_signed_total.denominator),
            "exact_zero_signed_total": exact_zero,
            "fourier_cancellation_quotient": fourier_quotient,
            "count_four_recombination_quotient": sector_quotient,
            "raw_frequency_coherence": raw_frequency_coherence,
            "frequency_coherence": min(1.0, raw_frequency_coherence),
            "basis_inflation": basis_inflation,
            "bridge_multiplier": bridge_multiplier,
            "bridge_identity_absolute_error": bridge_identity_error,
            "projected_fourier_identity_passes": projected[
                "projected_fourier_identity_passes"],
        }
    quotients = tuple(NEW_PERIOD_QUOTIENT_LAGS)
    rank_correlation = _spearman_correlation(
        tuple(rows[q]["fourier_cancellation_quotient"] for q in quotients),
        tuple(rows[q]["count_four_recombination_quotient"]
              for q in quotients))
    multipliers = tuple(rows[q]["bridge_multiplier"] for q in quotients)
    distortion = max(multipliers) / min(multipliers)
    predicted_rank_gate = (
        True if distortion <= maximum_stable_distortion
        else False if distortion >= minimum_unstable_distortion
        else None)
    observed_rank_gate = rank_correlation >= minimum_rank_correlation
    return {
        "families": families,
        "arithmetic_period": period,
        "quotients": quotients,
        "rows": rows,
        "exact_zero_quotients": tuple(
            q for q in quotients if rows[q]["exact_zero_signed_total"]),
        "spearman_correlation": rank_correlation,
        "minimum_rank_correlation": minimum_rank_correlation,
        "bridge_distortion_range": distortion,
        "maximum_stable_distortion": maximum_stable_distortion,
        "minimum_unstable_distortion": minimum_unstable_distortion,
        "predicted_rank_gate_passes": predicted_rank_gate,
        "observed_rank_gate_passes": observed_rank_gate,
        "distortion_classifier_is_conclusive": (
            predicted_rank_gate is not None),
        "distortion_classifier_prediction_matches": bool(
            predicted_rank_gate is not None
            and predicted_rank_gate == observed_rank_gate),
        "all_projected_fourier_identities_pass": all(
            row["projected_fourier_identity_passes"]
            for row in rows.values()),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(projected_fourier_cancellation_receipt())
