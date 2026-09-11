"""Frequency-resolved partial Fourier form of the resonant source correlation."""

import math

import numpy as np

from lcm_sawtooth_cotangent_count import (
    _one_orientation_count_source_modes,
)
from lcm_sawtooth_ramanujan_class_mean import _ramanujan_sum
from lcm_sawtooth_resonant_source_sectors import (
    _direct_fully_resonant_totals,
)
from lcm_sawtooth_source_ramanujan import _prime_power_factors


CANONICAL_FAMILIES = ((77, 65), (143, 35))
CANONICAL_LAGS = (130, 110)
EXACT_ZERO_FAMILIES = ((21, 55), (55, 21))
EXACT_ZERO_LAGS = (110, 42)


def _source_term_arrays(sources):
    residues = []
    frequencies = []
    coefficients = []
    for residue, modes in sources.items():
        for frequency, coefficient in modes.items():
            residues.append(residue)
            frequencies.append(frequency)
            coefficients.append(coefficient)
    return (
        np.asarray(residues, dtype=np.int64),
        np.asarray(frequencies, dtype=np.int64),
        np.asarray(coefficients, dtype=np.complex128),
    )


def _positive_source_transform_batch(period, terms, transform_frequencies):
    residues, source_frequencies, coefficients = terms
    transform_frequencies = np.asarray(transform_frequencies, dtype=np.int64)
    batch_size = len(transform_frequencies)
    transforms = np.zeros((batch_size, period), dtype=np.complex128)
    phases = np.exp(
        2j * np.pi
        * ((transform_frequencies[:, None] * residues[None, :]) % period)
        / period)
    weighted = phases * coefficients[None, :]
    flat_indices = (
        np.arange(batch_size, dtype=np.int64)[:, None] * period
        + source_frequencies[None, :])
    np.add.at(transforms.ravel(), flat_indices.ravel(), weighted.ravel())
    return transforms


def _partial_fourier_frequency_totals(
        period, lag, left_sources, right_sources, batch_size):
    common = math.gcd(lag, period)
    quotient = period // common
    resonant_frequencies = np.arange(0, period, quotient, dtype=np.int64)
    quotient_weights = np.asarray(tuple(
        _ramanujan_sum(quotient, frequency)
        for frequency in range(period)), dtype=np.float64)
    common_weights = np.asarray(tuple(
        _ramanujan_sum(common, int(frequency))
        for frequency in resonant_frequencies), dtype=np.float64)
    left_terms = _source_term_arrays(left_sources)
    right_terms = _source_term_arrays(right_sources)
    weighted_correlations = np.zeros(
        len(resonant_frequencies), dtype=np.complex128)
    divisor_stratum_correlations = {
        divisor: np.zeros(len(resonant_frequencies), dtype=np.complex128)
        for divisor in range(1, quotient + 1)
        if quotient % divisor == 0}
    sign_removed_correlations = np.zeros(
        len(resonant_frequencies), dtype=np.complex128)
    cauchy_natural_scale = 0.0

    for start in range(0, period, batch_size):
        stop = min(period, start + batch_size)
        transform_frequencies = np.arange(start, stop, dtype=np.int64)
        left = _positive_source_transform_batch(
            period, left_terms, transform_frequencies)
        right = _positive_source_transform_batch(
            period, right_terms, transform_frequencies)
        correlations = np.fft.ifft(
            np.fft.fft(left, axis=1)
            * np.conjugate(np.fft.fft(right, axis=1)),
            axis=1)
        weights = quotient_weights[start:stop]
        selected = correlations[:, resonant_frequencies]
        weighted_correlations += np.sum(
            weights[:, None] * selected, axis=0)
        sign_removed_correlations += np.sum(
            np.abs(weights)[:, None] * selected, axis=0)
        divisor_labels = np.gcd(transform_frequencies, quotient)
        for divisor in np.unique(divisor_labels):
            mask = divisor_labels == divisor
            divisor_stratum_correlations[int(divisor)] += np.sum(
                weights[mask, None] * selected[mask], axis=0)
        cauchy_natural_scale += float(np.sum(
            np.abs(weights)
            * np.linalg.norm(left, axis=1)
            * np.linalg.norm(right, axis=1)))

    totals = common_weights * weighted_correlations / period
    divisor_stratum_totals = {
        divisor: common_weights * correlations / period
        for divisor, correlations in divisor_stratum_correlations.items()}
    sign_removed_totals = (
        common_weights * sign_removed_correlations / period)
    natural_scales = np.maximum(
        1.0, np.abs(common_weights) * cauchy_natural_scale / period)
    return (
        resonant_frequencies, totals, natural_scales,
        divisor_stratum_totals, sign_removed_totals)


def _validate_case(families, lags, tolerance, batch_size):
    families = tuple(tuple(family) for family in families)
    lags = tuple(lags)
    if (len(families) != 2 or any(len(family) != 2 for family in families)
            or any(type(value) is not int or value < 3 or value % 2 == 0
                   for family in families for value in family)):
        raise ValueError("require two odd conductor-partner families")
    periods = tuple(
        math.lcm(conductor, 2 * odd_partner)
        for conductor, odd_partner in families)
    if len(set(periods)) != 1:
        raise ValueError("families must share one arithmetic period")
    period = periods[0]
    if (not lags or any(type(lag) is not int or not 0 < lag < period
                        for lag in lags)):
        raise ValueError("lags must lie strictly inside the period")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    if type(batch_size) is not int or batch_size < 1:
        raise ValueError("batch size must be a positive integer")
    factors = _prime_power_factors(period)
    if any(prime != prime_power for prime, prime_power in factors):
        raise ValueError("frequency resolution requires squarefree period")
    for lag in lags:
        common = math.gcd(lag, period)
        quotient = period // common
        if math.gcd(common, quotient) != 1:
            raise ValueError("frequency resolution requires coprime CRT parts")
    return families, lags, period


def frequency_resolved_fourier_case_receipt(
        families, lags, tolerance=1e-12, batch_size=32):
    families, lags, period = _validate_case(
        families, lags, tolerance, batch_size)
    left_sources = _one_orientation_count_source_modes(
        period, *families[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *families[1])[2]
    rows = {}
    for lag in lags:
        common = math.gcd(lag, period)
        quotient = period // common
        (frequencies, formula_totals, natural_scales,
         divisor_stratum_totals, sign_removed_totals) = (
            _partial_fourier_frequency_totals(
                period, lag, left_sources, right_sources, batch_size))
        direct = _direct_fully_resonant_totals(
            period, lag, left_sources, right_sources)[frequencies]
        errors = np.abs(formula_totals - direct)
        relative_errors = errors / natural_scales
        recombined_absolute_mass = float(np.sum(np.abs(formula_totals)))
        divisor_stratum_absolute_mass = float(sum(
            np.sum(np.abs(totals))
            for totals in divisor_stratum_totals.values()))
        sign_removed_absolute_mass = float(
            np.sum(np.abs(sign_removed_totals)))
        divisor_reconstruction_error = float(np.max(np.abs(
            sum(divisor_stratum_totals.values()) - formula_totals)))
        rows[quotient] = {
            "lag": lag,
            "gcd_lag_period": common,
            "resonant_frequency_count": len(frequencies),
            "maximum_absolute_error": float(np.max(errors)),
            "maximum_cauchy_scale_relative_error": float(
                np.max(relative_errors)),
            "direct_recombined_absolute_mass": float(np.sum(np.abs(direct))),
            "formula_recombined_absolute_mass": recombined_absolute_mass,
            "divisor_stratum_absolute_mass": divisor_stratum_absolute_mass,
            "within_frequency_divisor_coherence": (
                recombined_absolute_mass / divisor_stratum_absolute_mass
                if divisor_stratum_absolute_mass else None),
            "sign_removed_absolute_mass": sign_removed_absolute_mass,
            "sign_removal_mass_ratio": (
                sign_removed_absolute_mass / recombined_absolute_mass
                if recombined_absolute_mass else None),
            "maximum_divisor_stratum_reconstruction_absolute_error": (
                divisor_reconstruction_error),
            "divisor_stratum_reconstruction_passes": bool(
                divisor_reconstruction_error
                / max(1.0, divisor_stratum_absolute_mass) <= tolerance),
            "direct_signed_total": complex(np.sum(direct)),
            "formula_signed_total": complex(np.sum(formula_totals)),
            "every_frequency_reconstructs": bool(
                np.max(relative_errors) <= tolerance),
        }
    return {
        "families": families,
        "arithmetic_period": period,
        "quotients": tuple(rows),
        "rows": rows,
        "all_frequencies_reconstruct": all(
            row["every_frequency_reconstructs"] for row in rows.values()),
        "frequency_resolved_identity_proved": True,
        "uniform_frequency_resolved_bound_proved": False,
        "uniform_source_sum_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def frequency_resolved_fourier_receipt(tolerance=1e-12, batch_size=32):
    canonical = frequency_resolved_fourier_case_receipt(
        CANONICAL_FAMILIES, CANONICAL_LAGS, tolerance, batch_size)
    exact_zero = frequency_resolved_fourier_case_receipt(
        EXACT_ZERO_FAMILIES, EXACT_ZERO_LAGS, tolerance, batch_size)
    all_rows = tuple(canonical["rows"].values()) + tuple(
        exact_zero["rows"].values())
    sign_removal_consistently_increases_mass = all(
        row["sign_removal_mass_ratio"] > 1 for row in all_rows)
    return {
        "identity": (
            "b_n=1_(q|n)c_g(n)/Q sum_t c_q(t) "
            "sum_k Ftilde_L(t,k)conj(Ftilde_R(t,k-n))"),
        "canonical": canonical,
        "exact_zero": exact_zero,
        "all_frequencies_reconstruct": bool(
            canonical["all_frequencies_reconstruct"]
            and exact_zero["all_frequencies_reconstruct"]),
        "all_divisor_strata_reconstruct": all(
            row["divisor_stratum_reconstruction_passes"]
            for row in all_rows),
        "sign_removal_consistently_increases_mass": (
            sign_removal_consistently_increases_mass),
        "simple_ramanujan_sign_stratum_mechanism_supported": bool(
            sign_removal_consistently_increases_mass),
        "frequency_resolved_identity_proved": True,
        "divisor_stratum_decomposition_proved": True,
        "uniform_frequency_resolved_bound_proved": False,
        "uniform_source_sum_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }
