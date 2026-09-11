"""Frequency-resolved partial Fourier form of the resonant source correlation."""

import itertools
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
ALTERNATE_FAMILIES = ((35, 143), (65, 77))
ALTERNATE_LAGS = (130, 110)


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


def _divisor_stratum_sign_cells(
        frequencies, common, divisor_stratum_totals, tolerance):
    cells = {}
    total_stratum_mass = float(sum(
        np.sum(np.abs(totals))
        for totals in divisor_stratum_totals.values()))
    for divisor, totals in divisor_stratum_totals.items():
        for frequency, value in zip(frequencies, totals):
            key = (math.gcd(int(frequency), common), divisor)
            cells.setdefault(key, []).append(value)

    rows = {}
    for key, values in cells.items():
        values = np.asarray(values, dtype=np.complex128)
        absolute_mass = float(np.sum(np.abs(values)))
        real_mass = float(np.sum(np.abs(values.real)))
        imaginary_mass = float(np.sum(np.abs(values.imag)))
        positive_mass = float(np.sum(np.maximum(values.real, 0.0)))
        negative_mass = float(np.sum(np.maximum(-values.real, 0.0)))
        signed_mass = positive_mass + negative_mass
        opposite_sign_mass_fraction = (
            min(positive_mass, negative_mass) / signed_mass
            if signed_mass else 0.0)
        active = bool(
            absolute_mass > tolerance * max(1.0, total_stratum_mass))
        real_by_symmetry = bool(
            imaginary_mass / max(1.0, absolute_mass) <= tolerance)
        stable_sign = bool(
            active and real_by_symmetry
            and opposite_sign_mass_fraction <= tolerance)
        rows[key] = {
            "frequency_count": len(values),
            "absolute_mass": absolute_mass,
            "real_absolute_mass": real_mass,
            "imaginary_absolute_mass": imaginary_mass,
            "positive_real_mass": positive_mass,
            "negative_real_mass": negative_mass,
            "opposite_sign_mass_fraction": opposite_sign_mass_fraction,
            "active": active,
            "real_by_conjugate_symmetry": real_by_symmetry,
            "stable_real_sign": stable_sign,
        }
    active_rows = tuple(row for row in rows.values() if row["active"])
    return {
        "cells": rows,
        "active_cell_count": len(active_rows),
        "real_cell_count": sum(
            row["real_by_conjugate_symmetry"] for row in active_rows),
        "stable_sign_cell_count": sum(
            row["stable_real_sign"] for row in active_rows),
        "maximum_imaginary_mass_relative_to_cell_mass": max(
            (row["imaginary_absolute_mass"]
             / max(1.0, row["absolute_mass"])
             for row in active_rows), default=0.0),
        "maximum_opposite_sign_mass_fraction": max(
            (row["opposite_sign_mass_fraction"] for row in active_rows),
            default=0.0),
        "all_active_cells_are_real": all(
            row["real_by_conjugate_symmetry"] for row in active_rows),
        "all_active_cells_have_stable_sign": all(
            row["stable_real_sign"] for row in active_rows),
    }


def _legendre_symbol_on_unit(value, prime):
    residue = pow(int(value) % prime, (prime - 1) // 2, prime)
    if residue == 1:
        return 1
    if residue == prime - 1:
        return -1
    raise AssertionError("quadratic character evaluated off the unit group")


def _prime_divisors(value):
    divisors = []
    candidate = 2
    while candidate * candidate <= value:
        if value % candidate == 0:
            divisors.append(candidate)
            while value % candidate == 0:
                value //= candidate
        candidate += 1
    if value > 1:
        divisors.append(value)
    return tuple(divisors)


def _primitive_root_mod_prime(prime):
    order = prime - 1
    order_primes = _prime_divisors(order)
    for candidate in range(2, prime):
        if all(pow(candidate, order // factor, prime) != 1
               for factor in order_primes):
            return candidate
    raise AssertionError("odd prime has no primitive root")


def _unit_character_table(common, primitive_parameters):
    odd_primes = tuple(
        prime for prime, prime_power in _prime_power_factors(common)
        if prime == prime_power and prime % 2 == 1)
    local_logs = {}
    for prime in odd_primes:
        generator = _primitive_root_mod_prime(prime)
        log_table = {}
        value = 1
        for exponent in range(prime - 1):
            log_table[value] = exponent
            value = value * generator % prime
        local_logs[prime] = log_table
    labels = tuple(itertools.product(*(
        range(prime - 1) for prime in odd_primes)))
    table = np.ones(
        (len(labels), len(primitive_parameters)), dtype=np.complex128)
    for row, label in enumerate(labels):
        for prime, character_exponent in zip(odd_primes, label):
            logs = np.asarray(tuple(
                local_logs[prime][int(parameter) % prime]
                for parameter in primitive_parameters), dtype=np.float64)
            table[row] *= np.exp(
                2j * np.pi * character_exponent * logs / (prime - 1))
    return odd_primes, labels, table


def _primitive_character_energy(
        frequencies, common, quotient, divisor_stratum_totals,
        active_divisors, tolerance, leading_count=4):
    primitive_mask = np.asarray(tuple(
        math.gcd(int(frequency), common) == 1
        for frequency in frequencies), dtype=bool)
    primitive_parameters = frequencies[primitive_mask] // quotient
    odd_primes, labels, character_table = _unit_character_table(
        common, primitive_parameters)
    group_order = len(primitive_parameters)
    if len(labels) != group_order:
        raise AssertionError("character table does not span the unit group")
    rows = {}
    for divisor, totals in divisor_stratum_totals.items():
        values = totals[primitive_mask]
        coefficients = np.conjugate(character_table) @ values
        coefficient_energy = np.abs(coefficients) ** 2
        expected_energy = group_order * float(np.sum(np.abs(values) ** 2))
        actual_energy = float(np.sum(coefficient_energy))
        ranked = sorted(
            zip(coefficient_energy, labels),
            key=lambda item: (-item[0], item[1]))
        retained = ranked[:min(leading_count, len(ranked))]
        retained_energy = float(sum(item[0] for item in retained))
        cumulative_energy = 0.0
        characters_for_ninety_percent = 0
        for energy, _ in ranked:
            cumulative_energy += float(energy)
            characters_for_ninety_percent += 1
            if cumulative_energy >= .9 * actual_energy:
                break
        effective_character_rank = (
            actual_energy * actual_energy
            / float(np.sum(coefficient_energy ** 2))
            if actual_energy else 0.0)
        reconstruction = coefficients @ character_table / group_order
        reconstruction_error = float(np.max(np.abs(reconstruction - values)))
        reconstruction_scale = max(1.0, float(np.sum(np.abs(values))))
        rows[divisor] = {
            "active": divisor in active_divisors,
            "primitive_unit_count": group_order,
            "character_count": len(labels),
            "leading_character_count": len(retained),
            "leading_character_labels": tuple(item[1] for item in retained),
            "leading_character_energy_fraction": (
                retained_energy / actual_energy if actual_energy else 1.0),
            "characters_for_ninety_percent_energy": (
                characters_for_ninety_percent),
            "effective_character_rank": effective_character_rank,
            "parseval_relative_error": (
                abs(actual_energy - expected_energy)
                / max(1.0, expected_energy)),
            "reconstruction_natural_scale_relative_error": (
                reconstruction_error / reconstruction_scale),
            "character_expansion_reconstructs": bool(
                reconstruction_error / reconstruction_scale <= tolerance),
        }
    active_rows = tuple(rows[divisor] for divisor in active_divisors)
    return {
        "odd_character_primes": odd_primes,
        "unit_group_order": group_order,
        "character_count": len(labels),
        "active_divisors": tuple(active_divisors),
        "divisor_rows": rows,
        "minimum_leading_four_energy_fraction": min(
            (row["leading_character_energy_fraction"] for row in active_rows),
            default=1.0),
        "maximum_characters_for_ninety_percent_energy": max(
            (row["characters_for_ninety_percent_energy"]
             for row in active_rows), default=0),
        "effective_character_rank_range": (
            min((row["effective_character_rank"] for row in active_rows),
                default=0.0),
            max((row["effective_character_rank"] for row in active_rows),
                default=0.0)),
        "maximum_parseval_relative_error": max(
            (row["parseval_relative_error"] for row in active_rows),
            default=0.0),
        "maximum_reconstruction_natural_scale_relative_error": max(
            (row["reconstruction_natural_scale_relative_error"]
             for row in active_rows), default=0.0),
        "all_character_expansions_reconstruct": all(
            row["character_expansion_reconstructs"] for row in active_rows),
    }


def _primitive_gauss_transfer(
        frequencies, common, quotient, divisor_stratum_totals,
        active_divisors, tolerance, leading_count=4):
    primitive_mask = np.asarray(tuple(
        math.gcd(int(frequency), common) == 1
        for frequency in frequencies), dtype=bool)
    units = frequencies[primitive_mask] // quotient
    odd_primes, labels, character_table = _unit_character_table(common, units)
    group_order = len(units)
    additive_at_one = np.exp(2j * np.pi * units / common)
    gauss_sums = character_table @ additive_at_one
    additive_matrix = np.exp(
        2j * np.pi * ((units[:, None] * units[None, :]) % common) / common)
    rows = {}
    for divisor, totals in divisor_stratum_totals.items():
        values = totals[primitive_mask]
        coefficients = np.conjugate(character_table) @ values
        direct = additive_matrix @ values
        weighted_coefficients = coefficients * gauss_sums
        reconstructed = (
            weighted_coefficients @ np.conjugate(character_table)
            / group_order)
        errors = np.abs(reconstructed - direct)
        natural_scale = max(1.0, float(np.sum(np.abs(values))))
        weighted_energy = np.abs(weighted_coefficients) ** 2
        total_weighted_energy = float(np.sum(weighted_energy))
        ranked = sorted(
            zip(weighted_energy, labels),
            key=lambda item: (-item[0], item[1]))
        leading = ranked[:min(leading_count, len(ranked))]
        leading_energy = float(sum(item[0] for item in leading))
        cumulative_energy = 0.0
        characters_for_ninety_percent = 0
        for energy, _ in ranked:
            cumulative_energy += float(energy)
            characters_for_ninety_percent += 1
            if cumulative_energy >= .9 * total_weighted_energy:
                break
        rows[divisor] = {
            "active": divisor in active_divisors,
            "odd_character_primes": odd_primes,
            "character_count": len(labels),
            "leading_character_labels": tuple(item[1] for item in leading),
            "gauss_weighted_leading_four_energy_fraction": (
                leading_energy / total_weighted_energy
                if total_weighted_energy else 1.0),
            "gauss_weighted_characters_for_ninety_percent_energy": (
                characters_for_ninety_percent),
            "maximum_gauss_transfer_absolute_error": float(np.max(errors)),
            "maximum_gauss_transfer_natural_scale_relative_error": float(
                np.max(errors) / natural_scale),
            "gauss_transfer_reconstructs_every_unit": bool(
                np.max(errors) / natural_scale <= tolerance),
        }
    active_rows = tuple(rows[divisor] for divisor in active_divisors)
    return {
        "unit_group_order": group_order,
        "character_count": len(labels),
        "active_divisors": tuple(active_divisors),
        "divisor_rows": rows,
        "minimum_gauss_weighted_leading_four_energy_fraction": min(
            (row["gauss_weighted_leading_four_energy_fraction"]
             for row in active_rows), default=1.0),
        "gauss_weighted_characters_for_ninety_percent_energy_range": (
            min((row["gauss_weighted_characters_for_ninety_percent_energy"]
                 for row in active_rows), default=0),
            max((row["gauss_weighted_characters_for_ninety_percent_energy"]
                 for row in active_rows), default=0)),
        "maximum_gauss_transfer_natural_scale_relative_error": max(
            (row["maximum_gauss_transfer_natural_scale_relative_error"]
             for row in active_rows), default=0.0),
        "all_gauss_transfers_reconstruct_every_unit": all(
            row["gauss_transfer_reconstructs_every_unit"]
            for row in active_rows),
    }


def _primitive_quadratic_character_fits(
        frequencies, common, quotient, divisor_stratum_totals, tolerance):
    odd_primes = tuple(
        prime for prime, prime_power in _prime_power_factors(common)
        if prime == prime_power and prime % 2 == 1)
    primitive_mask = np.asarray(tuple(
        math.gcd(int(frequency), common) == 1
        for frequency in frequencies), dtype=bool)
    primitive_parameters = frequencies[primitive_mask] // quotient
    character_values = {}
    for subset_mask in range(1 << len(odd_primes)):
        character_primes = tuple(
            prime for index, prime in enumerate(odd_primes)
            if subset_mask & (1 << index))
        values = np.ones(len(primitive_parameters), dtype=np.float64)
        for prime in character_primes:
            values *= np.asarray(tuple(
                _legendre_symbol_on_unit(parameter, prime)
                for parameter in primitive_parameters), dtype=np.float64)
        character_values[character_primes] = values

    divisor_rows = {}
    for divisor, totals in divisor_stratum_totals.items():
        primitive_values = totals[primitive_mask].real
        absolute_mass = float(np.sum(np.abs(primitive_values)))
        fits = []
        for character_primes, characters in character_values.items():
            twisted = characters * primitive_values
            positive_mass = float(np.sum(np.maximum(twisted, 0.0)))
            negative_mass = float(np.sum(np.maximum(-twisted, 0.0)))
            signed_mass = positive_mass + negative_mass
            minority_fraction = (
                min(positive_mass, negative_mass) / signed_mass
                if signed_mass else 0.0)
            alignment = (
                abs(float(np.sum(twisted))) / signed_mass
                if signed_mass else 1.0)
            fits.append((
                minority_fraction, -alignment, character_primes,
                positive_mass, negative_mass))
        best = min(fits)
        divisor_rows[divisor] = {
            "primitive_absolute_mass": absolute_mass,
            "best_character_primes": best[2],
            "best_character_alignment": -best[1],
            "best_twisted_positive_mass": best[3],
            "best_twisted_negative_mass": best[4],
            "best_twisted_minority_mass_fraction": best[0],
            "perfect_quadratic_sign_fit": bool(best[0] <= tolerance),
        }
    total_primitive_mass = math.fsum(
        row["primitive_absolute_mass"] for row in divisor_rows.values())
    active_divisors = tuple(
        divisor for divisor, row in divisor_rows.items()
        if row["primitive_absolute_mass"]
        > tolerance * max(1.0, total_primitive_mass))
    for divisor, row in divisor_rows.items():
        row["active"] = divisor in active_divisors
    active_rows = tuple(divisor_rows[divisor] for divisor in active_divisors)
    return {
        "odd_character_primes": odd_primes,
        "candidate_character_count": len(character_values),
        "divisor_rows": divisor_rows,
        "active_divisors": active_divisors,
        "active_divisor_count": len(active_rows),
        "perfect_fit_divisor_count": sum(
            row["perfect_quadratic_sign_fit"] for row in active_rows),
        "maximum_best_twisted_minority_mass_fraction": max(
            (row["best_twisted_minority_mass_fraction"]
             for row in active_rows), default=0.0),
        "all_primitive_divisors_have_perfect_quadratic_sign_fit": all(
            row["perfect_quadratic_sign_fit"] for row in active_rows),
    }


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
        sign_cells = _divisor_stratum_sign_cells(
            frequencies, common, divisor_stratum_totals, tolerance)
        quadratic_fits = _primitive_quadratic_character_fits(
            frequencies, common, quotient,
            divisor_stratum_totals, tolerance)
        character_energy = _primitive_character_energy(
            frequencies, common, quotient, divisor_stratum_totals,
            quadratic_fits["active_divisors"], tolerance)
        gauss_transfer = _primitive_gauss_transfer(
            frequencies, common, quotient, divisor_stratum_totals,
            quadratic_fits["active_divisors"], tolerance)
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
            "divisor_stratum_sign_cells": sign_cells,
            "primitive_quadratic_character_fits": quadratic_fits,
            "primitive_dirichlet_character_energy": character_energy,
            "primitive_gauss_transfer": gauss_transfer,
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
    all_active_sign_cells_are_real = all(
        row["divisor_stratum_sign_cells"]["all_active_cells_are_real"]
        for row in all_rows)
    all_active_sign_cells_have_stable_sign = all(
        row["divisor_stratum_sign_cells"][
            "all_active_cells_have_stable_sign"]
        for row in all_rows)
    all_primitive_divisors_have_perfect_quadratic_sign_fit = all(
        row["primitive_quadratic_character_fits"][
            "all_primitive_divisors_have_perfect_quadratic_sign_fit"]
        for row in all_rows)
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
        "all_active_sign_cells_are_numerically_real": (
            all_active_sign_cells_are_real),
        "all_active_sign_cells_have_stable_sign": (
            all_active_sign_cells_have_stable_sign),
        "coarse_gcd_divisor_sign_table_supported": bool(
            all_active_sign_cells_are_real
            and all_active_sign_cells_have_stable_sign),
        "all_primitive_divisors_have_perfect_quadratic_sign_fit": (
            all_primitive_divisors_have_perfect_quadratic_sign_fit),
        "quadratic_character_sign_mechanism_supported": bool(
            all_primitive_divisors_have_perfect_quadratic_sign_fit),
        "frequency_resolved_identity_proved": True,
        "divisor_stratum_decomposition_proved": True,
        "uniform_frequency_resolved_bound_proved": False,
        "uniform_source_sum_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def quadratic_character_factor_reallocation_receipt(
        minimum_mod5_winning_cells=6, tolerance=1e-12, batch_size=32):
    if (type(minimum_mod5_winning_cells) is not int
            or not 0 <= minimum_mod5_winning_cells <= 8):
        raise ValueError("mod-5 winning-cell threshold must lie in [0,8]")
    alternate = frequency_resolved_fourier_case_receipt(
        ALTERNATE_FAMILIES, ALTERNATE_LAGS, tolerance, batch_size)
    winning_cells = []
    active_cells = []
    for quotient, row in alternate["rows"].items():
        fits = row["primitive_quadratic_character_fits"]
        divisor_rows = fits["divisor_rows"]
        for divisor in fits["active_divisors"]:
            fit = divisor_rows[divisor]
            active_cells.append((quotient, divisor))
            if 5 in fit["best_character_primes"]:
                winning_cells.append((quotient, divisor))
    all_eight_cells_are_active = len(active_cells) == 8
    passes = bool(
        all_eight_cells_are_active
        and len(winning_cells) >= minimum_mod5_winning_cells)
    return {
        "families": ALTERNATE_FAMILIES,
        "arithmetic_period": alternate["arithmetic_period"],
        "quotients": alternate["quotients"],
        "rows": alternate["rows"],
        "minimum_mod5_winning_cells": minimum_mod5_winning_cells,
        "active_primitive_divisor_cells": tuple(active_cells),
        "active_primitive_divisor_cell_count": len(active_cells),
        "all_eight_primitive_divisor_cells_are_active": (
            all_eight_cells_are_active),
        "mod5_winning_cells": tuple(winning_cells),
        "mod5_winning_cell_count": len(winning_cells),
        "mod5_factor_reallocation_prediction_passes": bool(passes),
        "orientation_stable_mod5_component_supported": bool(passes),
        "uniform_frequency_resolved_bound_proved": False,
        "uniform_source_sum_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def dirichlet_character_energy_holdout_receipt(
        minimum_leading_four_energy_fraction=.90,
        tolerance=1e-12, batch_size=32):
    if (not math.isfinite(minimum_leading_four_energy_fraction)
            or not 0 < minimum_leading_four_energy_fraction <= 1):
        raise ValueError("character-energy threshold must lie in (0,1]")
    cases = {
        "canonical": frequency_resolved_fourier_case_receipt(
            CANONICAL_FAMILIES, CANONICAL_LAGS, tolerance, batch_size),
        "alternate": frequency_resolved_fourier_case_receipt(
            ALTERNATE_FAMILIES, ALTERNATE_LAGS, tolerance, batch_size),
    }
    cells = []
    characters_for_ninety_percent = []
    effective_character_ranks = []
    for case_name, case in cases.items():
        for quotient, row in case["rows"].items():
            energy = row["primitive_dirichlet_character_energy"]
            for divisor in energy["active_divisors"]:
                fraction = energy["divisor_rows"][divisor][
                    "leading_character_energy_fraction"]
                cells.append((case_name, quotient, divisor, fraction))
                characters_for_ninety_percent.append(
                    energy["divisor_rows"][divisor][
                        "characters_for_ninety_percent_energy"])
                effective_character_ranks.append(
                    energy["divisor_rows"][divisor][
                        "effective_character_rank"])
    all_reconstruct = all(
        row["primitive_dirichlet_character_energy"][
            "all_character_expansions_reconstruct"]
        for case in cases.values() for row in case["rows"].values())
    passing_cells = tuple(
        cell[:3] for cell in cells
        if cell[3] >= minimum_leading_four_energy_fraction)
    all_cells_pass = bool(
        len(cells) == 16 and len(passing_cells) == len(cells))
    return {
        "minimum_leading_four_energy_fraction": (
            minimum_leading_four_energy_fraction),
        "cases": cases,
        "active_cell_count": len(cells),
        "passing_cells": passing_cells,
        "passing_cell_count": len(passing_cells),
        "minimum_observed_leading_four_energy_fraction": min(
            (cell[3] for cell in cells), default=None),
        "characters_for_ninety_percent_energy_range": (
            min(characters_for_ninety_percent, default=0),
            max(characters_for_ninety_percent, default=0)),
        "effective_character_rank_range": (
            min(effective_character_ranks, default=0.0),
            max(effective_character_ranks, default=0.0)),
        "all_character_expansions_reconstruct": bool(all_reconstruct),
        "all_sixteen_cells_pass_low_rank_gate": all_cells_pass,
        "four_character_low_rank_mechanism_supported": bool(all_cells_pass),
        "uniform_character_large_sieve_estimate_proved": False,
        "uniform_frequency_resolved_bound_proved": False,
        "signed_prime_correlation_proved": False,
    }


def gauss_prime_interface_receipt(
        minimum_gauss_weighted_leading_four_energy_fraction=.90,
        tolerance=1e-12, batch_size=32):
    if (not math.isfinite(
            minimum_gauss_weighted_leading_four_energy_fraction)
            or not 0 < minimum_gauss_weighted_leading_four_energy_fraction
            <= 1):
        raise ValueError("Gauss-weighted energy threshold must lie in (0,1]")
    cases = {
        "canonical": frequency_resolved_fourier_case_receipt(
            CANONICAL_FAMILIES, CANONICAL_LAGS, tolerance, batch_size),
        "alternate": frequency_resolved_fourier_case_receipt(
            ALTERNATE_FAMILIES, ALTERNATE_LAGS, tolerance, batch_size),
    }
    cells = []
    counts_for_ninety_percent = []
    for case_name, case in cases.items():
        for quotient, row in case["rows"].items():
            transfer = row["primitive_gauss_transfer"]
            for divisor in transfer["active_divisors"]:
                divisor_row = transfer["divisor_rows"][divisor]
                cells.append((
                    case_name, quotient, divisor,
                    divisor_row[
                        "gauss_weighted_leading_four_energy_fraction"]))
                counts_for_ninety_percent.append(
                    divisor_row[
                        "gauss_weighted_characters_for_ninety_percent_energy"])
    passing_cells = tuple(
        cell[:3] for cell in cells
        if cell[3] >= minimum_gauss_weighted_leading_four_energy_fraction)
    all_reconstruct = all(
        row["primitive_gauss_transfer"][
            "all_gauss_transfers_reconstruct_every_unit"]
        for case in cases.values() for row in case["rows"].values())
    all_cells_pass = bool(
        len(cells) == 16 and len(passing_cells) == len(cells))
    return {
        "identity": (
            "sum_r f_d(r)e_g(rp)=phi(g)^-1 sum_chi "
            "fhat_d(chi)tau_g(chi)conj(chi(p))"),
        "minimum_gauss_weighted_leading_four_energy_fraction": (
            minimum_gauss_weighted_leading_four_energy_fraction),
        "cases": cases,
        "active_cell_count": len(cells),
        "passing_cells": passing_cells,
        "passing_cell_count": len(passing_cells),
        "observed_gauss_weighted_leading_four_energy_fraction_range": (
            min((cell[3] for cell in cells), default=None),
            max((cell[3] for cell in cells), default=None)),
        "gauss_weighted_characters_for_ninety_percent_energy_range": (
            min(counts_for_ninety_percent, default=0),
            max(counts_for_ninety_percent, default=0)),
        "all_gauss_transfers_reconstruct_every_unit": bool(all_reconstruct),
        "all_sixteen_cells_pass_gauss_weighted_low_rank_gate": all_cells_pass,
        "gauss_weighted_four_character_mechanism_supported": bool(
            all_cells_pass),
        "two_linked_prime_character_estimate_proved": False,
        "uniform_frequency_resolved_bound_proved": False,
        "signed_prime_correlation_proved": False,
    }
