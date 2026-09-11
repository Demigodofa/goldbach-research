"""Exact linked-prime functional after the resonant Gauss transfer."""

import math

import numpy as np

from lcm_sawtooth_cotangent_count import (
    _one_orientation_count_source_modes,
)
from lcm_sawtooth_frequency_resolved_fourier import (
    CANONICAL_FAMILIES,
    CANONICAL_LAGS,
    _partial_fourier_frequency_totals,
    _primitive_quadratic_character_fits,
    _unit_character_table,
)


LINKED_PRIME_TARGETS = (1000, 1002)


def _prime_table(limit):
    table = np.ones(limit + 1, dtype=bool)
    table[:2] = False
    for prime in range(2, math.isqrt(limit) + 1):
        if table[prime]:
            table[prime * prime:limit + 1:prime] = False
    return table


def _linked_prime_pairs(target, lower, upper):
    primes = _prime_table(target)
    return tuple(
        (prime, math.log(prime) * math.log(target - prime))
        for prime in range(max(2, lower + 1), min(target, upper))
        if primes[prime] and primes[target - prime])


def _linked_prime_character_row(
        common, quotient, frequencies, stratum_totals,
        target, lower, upper, tolerance):
    if not 0 <= lower < upper <= target:
        raise ValueError("require 0 <= lower < upper <= target")
    primitive_mask = np.asarray(tuple(
        math.gcd(int(frequency), common) == 1
        for frequency in frequencies), dtype=bool)
    units = frequencies[primitive_mask] // quotient
    values = stratum_totals[primitive_mask]
    _, _, character_table = _unit_character_table(common, units)
    group_order = len(units)
    coefficients = np.conjugate(character_table) @ values
    gauss_sums = character_table @ np.exp(2j * np.pi * units / common)
    gauss_coefficients = coefficients * gauss_sums
    unit_column = {int(unit): index for index, unit in enumerate(units)}

    pairs = _linked_prime_pairs(target, lower, upper)
    character_prime_correlation = np.zeros(
        group_order, dtype=np.complex128)
    direct_unit_correlation = 0.0j
    nonunit_correction = 0.0j
    direct_triangle_mass = 0.0
    unit_residue_weights = {int(unit): 0.0 for unit in units}
    nonunit_primes = []
    for prime, weight in pairs:
        additive_value = np.sum(
            values * np.exp(2j * np.pi * units * prime / common))
        if math.gcd(prime, common) == 1:
            column = unit_column[prime % common]
            character_prime_correlation += (
                weight * np.conjugate(character_table[:, column]))
            direct_unit_correlation += weight * additive_value
            direct_triangle_mass += weight * abs(additive_value)
            unit_residue_weights[prime % common] += weight
        else:
            nonunit_primes.append(prime)
            nonunit_correction += weight * additive_value

    character_reconstruction = (
        gauss_coefficients @ character_prime_correlation / group_order)
    direct_total = direct_unit_correlation + nonunit_correction
    reconstructed_total = character_reconstruction + nonunit_correction
    reconstruction_error = abs(reconstructed_total - direct_total)
    reconstruction_scale = max(
        1.0, direct_triangle_mass, abs(nonunit_correction))

    character_second_moment = float(np.sum(
        np.abs(character_prime_correlation) ** 2))
    positive_residue_second_moment = group_order * math.fsum(
        weight * weight for weight in unit_residue_weights.values())
    orthogonality_error = abs(
        character_second_moment - positive_residue_second_moment)
    orthogonality_scale = max(1.0, positive_residue_second_moment)
    cauchy_envelope = (
        float(np.linalg.norm(gauss_coefficients))
        * float(np.linalg.norm(character_prime_correlation))
        / group_order)
    additive_unit_values = np.asarray(tuple(
        np.sum(values * np.exp(2j * np.pi * units * unit / common))
        for unit in units), dtype=np.complex128)
    residue_cauchy_envelope = math.sqrt(
        float(np.sum(np.abs(additive_unit_values) ** 2))
        * math.fsum(weight * weight for weight in unit_residue_weights.values()))
    cauchy_identity_error = abs(cauchy_envelope - residue_cauchy_envelope)
    cauchy_scale = max(1.0, cauchy_envelope, residue_cauchy_envelope)

    endpoint_pairs = tuple(
        endpoint for endpoint in (lower, upper)
        if 2 <= endpoint < target
        and _prime_table(target)[endpoint]
        and _prime_table(target)[target - endpoint])
    return {
        "target": target,
        "interval": (lower, upper),
        "interval_convention": "lower < p < upper",
        "linked_prime_pair_count": len(pairs),
        "nonunit_prime_terms": tuple(nonunit_primes),
        "nonunit_correction": nonunit_correction,
        "excluded_endpoint_prime_pairs": endpoint_pairs,
        "direct_unit_correlation": direct_unit_correlation,
        "character_unit_correlation": character_reconstruction,
        "direct_total_with_nonunit_correction": direct_total,
        "character_total_with_nonunit_correction": reconstructed_total,
        "reconstruction_natural_scale_relative_error": (
            reconstruction_error / reconstruction_scale),
        "linked_prime_character_identity_passes": bool(
            reconstruction_error / reconstruction_scale <= tolerance),
        "character_prime_second_moment": character_second_moment,
        "positive_residue_class_second_moment": (
            positive_residue_second_moment),
        "orthogonality_second_moment_relative_error": (
            orthogonality_error / orthogonality_scale),
        "orthogonality_reduces_to_positive_residue_second_moment": bool(
            orthogonality_error / orthogonality_scale <= tolerance),
        "character_cauchy_envelope": cauchy_envelope,
        "residue_class_cauchy_envelope": residue_cauchy_envelope,
        "cauchy_envelope_relative_identity_error": (
            cauchy_identity_error / cauchy_scale),
        "actual_to_cauchy_envelope_ratio": (
            abs(direct_unit_correlation) / cauchy_envelope
            if cauchy_envelope else None),
        "cauchy_to_direct_triangle_ratio": (
            cauchy_envelope / direct_triangle_mass
            if direct_triangle_mass else None),
    }


def linked_prime_character_receipt(
        targets=LINKED_PRIME_TARGETS, tolerance=1e-12, batch_size=32):
    targets = tuple(targets)
    if (not targets
            or any(type(target) is not int or target < 20 or target % 2
                   for target in targets)):
        raise ValueError("targets must be even integers at least 20")
    if any(not _linked_prime_pairs(
            target, target // 3, 2 * target // 3)
           for target in targets):
        raise ValueError(
            "each target must have a linked-prime pair in its strict "
            "central interval")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    if type(batch_size) is not int or batch_size < 1:
        raise ValueError("batch size must be a positive integer")

    period = math.lcm(
        CANONICAL_FAMILIES[0][0], 2 * CANONICAL_FAMILIES[0][1])
    left_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[1])[2]
    rows = {}
    lag_components = {}
    for lag in CANONICAL_LAGS:
        common = math.gcd(lag, period)
        quotient = period // common
        (frequencies, _, _, divisor_strata, _) = (
            _partial_fourier_frequency_totals(
                period, lag, left_sources, right_sources, batch_size))
        lag_components[quotient] = (frequencies, divisor_strata)
        active = _primitive_quadratic_character_fits(
            frequencies, common, quotient, divisor_strata, tolerance)[
                "active_divisors"]
        for divisor in active:
            for target in targets:
                lower = target // 3
                upper = 2 * target // 3
                rows[(quotient, divisor, target)] = (
                    _linked_prime_character_row(
                        common, quotient, frequencies,
                        divisor_strata[divisor], target,
                        lower, upper, tolerance))

    # The central target fixtures have no nonunit prime p.  This separate row
    # proves the correction path rather than silently assuming it away.
    witness_lag = CANONICAL_LAGS[1]
    witness_common = math.gcd(witness_lag, period)
    witness_quotient = period // witness_common
    witness_frequencies, witness_strata = lag_components[witness_quotient]
    nonunit_witness = _linked_prime_character_row(
        witness_common, witness_quotient, witness_frequencies,
        witness_strata[1], 24, 1, 23, tolerance)

    all_rows = tuple(rows.values()) + (nonunit_witness,)
    main_rows = tuple(rows.values())
    cauchy_to_triangle_ratios = tuple(
        row["cauchy_to_direct_triangle_ratio"] for row in main_rows)
    actual_to_cauchy_ratios = tuple(
        row["actual_to_cauchy_envelope_ratio"] for row in main_rows)
    cauchy_improves_every_triangle = all(
        ratio < 1 for ratio in cauchy_to_triangle_ratios)
    return {
        "families": CANONICAL_FAMILIES,
        "arithmetic_period": period,
        "targets": targets,
        "rows": rows,
        "nonunit_correction_witness": nonunit_witness,
        "all_linked_prime_character_identities_pass": all(
            row["linked_prime_character_identity_passes"]
            for row in all_rows),
        "all_character_second_moments_are_positive_residue_moments": all(
            row[
                "orthogonality_reduces_to_positive_residue_second_moment"]
            for row in all_rows),
        "maximum_reconstruction_natural_scale_relative_error": max(
            float(row["reconstruction_natural_scale_relative_error"])
            for row in all_rows),
        "maximum_orthogonality_second_moment_relative_error": max(
            row["orthogonality_second_moment_relative_error"]
            for row in all_rows),
        "maximum_cauchy_envelope_relative_identity_error": max(
            row["cauchy_envelope_relative_identity_error"]
            for row in all_rows),
        "cauchy_to_direct_triangle_ratio_range": (
            min(cauchy_to_triangle_ratios),
            max(cauchy_to_triangle_ratios)),
        "actual_to_cauchy_envelope_ratio_range": (
            min(actual_to_cauchy_ratios),
            max(actual_to_cauchy_ratios)),
        "cauchy_improves_every_direct_triangle_bound": bool(
            cauchy_improves_every_triangle),
        "plain_per_target_character_cauchy_supplies_signed_saving": bool(
            cauchy_improves_every_triangle),
        "joint_coefficient_prime_phase_estimate_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }
