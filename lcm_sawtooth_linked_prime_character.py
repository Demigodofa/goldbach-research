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


def _complex_fsum(values):
    values = tuple(values)
    return complex(
        math.fsum(value.real for value in values),
        math.fsum(value.imag for value in values))


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


def _affine_reflection_projection(
        common, units, additive_unit_values, target_residue):
    unit_column = {int(unit): index for index, unit in enumerate(units)}
    admissible_columns = np.asarray(tuple(
        column for column, unit in enumerate(units)
        if math.gcd((target_residue - int(unit)) % common, common) == 1),
        dtype=np.int64)
    reflected_columns = np.asarray(tuple(
        unit_column[(target_residue - int(units[column])) % common]
        for column in admissible_columns), dtype=np.int64)
    reflected_twice_columns = np.asarray(tuple(
        unit_column[(target_residue - int(units[column])) % common]
        for column in reflected_columns), dtype=np.int64)
    admissible_values = additive_unit_values[admissible_columns]
    reflected_values = additive_unit_values[reflected_columns]
    symmetric_values = (admissible_values + reflected_values) / 2
    antisymmetric_values = (admissible_values - reflected_values) / 2
    source_energy = float(np.sum(np.abs(admissible_values) ** 2))
    symmetric_source_energy = float(np.sum(np.abs(symmetric_values) ** 2))
    antisymmetric_source_energy = float(
        np.sum(np.abs(antisymmetric_values) ** 2))
    return {
        "admissible_columns": admissible_columns,
        "symmetric_values": symmetric_values,
        "antisymmetric_values": antisymmetric_values,
        "source_energy": source_energy,
        "symmetric_source_energy": symmetric_source_energy,
        "antisymmetric_source_energy": antisymmetric_source_energy,
        "reflection_covariance": np.vdot(
            admissible_values, reflected_values),
        "is_involution": bool(np.array_equal(
            reflected_twice_columns, admissible_columns)),
        "energy_error": abs(
            source_energy - symmetric_source_energy
            - antisymmetric_source_energy),
        "orthogonality_error": abs(
            np.vdot(symmetric_values, antisymmetric_values)),
    }


def _principal_character_row(character_labels):
    zero_label = tuple(0 for _ in character_labels[0])
    matches = tuple(
        index for index, label in enumerate(character_labels)
        if label == zero_label)
    if len(matches) != 1:
        raise AssertionError("expected exactly one principal character label")
    return matches[0]


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
    _, character_labels, character_table = _unit_character_table(
        common, units)
    group_order = len(units)
    trivial_character_row = _principal_character_row(character_labels)
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
    source_unit_mean = complex(np.mean(additive_unit_values))
    principal_character_source_mean = complex(
        gauss_coefficients[trivial_character_row] / group_order)
    unit_linked_prime_pair_weight = math.fsum(
        unit_residue_weights.values())
    constant_source_linked_prime_correlation = (
        source_unit_mean * unit_linked_prime_pair_weight)
    principal_character_linked_prime_correlation = (
        gauss_coefficients[trivial_character_row]
        * character_prime_correlation[trivial_character_row]
        / group_order)
    centered_source_linked_prime_correlation = (
        direct_unit_correlation - constant_source_linked_prime_correlation)
    source_mean_scale = max(1.0, abs(source_unit_mean))
    principal_channel_scale = max(
        1.0, direct_triangle_mass,
        abs(constant_source_linked_prime_correlation))
    projection = _affine_reflection_projection(
        common, units, additive_unit_values, target % common)
    admissible_columns = projection["admissible_columns"]
    symmetric_values = projection["symmetric_values"]
    antisymmetric_values = projection["antisymmetric_values"]
    source_energy = projection["source_energy"]
    symmetric_source_energy = projection["symmetric_source_energy"]
    antisymmetric_source_energy = projection["antisymmetric_source_energy"]
    affine_reflection_is_involution = projection["is_involution"]
    projector_energy_error = projection["energy_error"]
    projector_orthogonality_error = projection["orthogonality_error"]
    projector_energy_scale = max(1.0, source_energy)
    admissible_column_by_unit = {
        int(units[column]): index
        for index, column in enumerate(admissible_columns)}
    symmetrized_linked_prime_correlation = 0.0j
    antisymmetric_linked_prime_correlation = 0.0j
    for prime, weight in pairs:
        if (math.gcd(prime, common) == 1
                and prime % common in admissible_column_by_unit):
            column = admissible_column_by_unit[prime % common]
            symmetrized_linked_prime_correlation += (
                weight * symmetric_values[column])
            antisymmetric_linked_prime_correlation += (
                weight * antisymmetric_values[column])
    residue_cauchy_envelope = math.sqrt(
        float(np.sum(np.abs(additive_unit_values) ** 2))
        * math.fsum(weight * weight for weight in unit_residue_weights.values()))
    cauchy_identity_error = abs(cauchy_envelope - residue_cauchy_envelope)
    cauchy_scale = max(1.0, cauchy_envelope, residue_cauchy_envelope)
    minus_one_column = unit_column[common - 1]
    character_parities = np.real_if_close(
        character_table[:, minus_one_column]).real
    even_mask = character_parities > 0
    odd_mask = character_parities < 0
    even_character_correlation = (
        gauss_coefficients[even_mask]
        @ character_prime_correlation[even_mask] / group_order)
    odd_character_correlation = (
        gauss_coefficients[odd_mask]
        @ character_prime_correlation[odd_mask] / group_order)
    parity_reconstruction_error = abs(
        even_character_correlation + odd_character_correlation
        - character_reconstruction)
    total_pair_weight = math.fsum(weight for _, weight in pairs)
    maximum_odd_prime_correlation_relative_to_pair_weight = (
        float(np.max(np.abs(character_prime_correlation[odd_mask])))
        / max(1.0, total_pair_weight))
    pair_symmetric_interval = upper == target - lower
    odd_pair_cancellation_applicable = bool(
        target % common == 0 and pair_symmetric_interval
        and not nonunit_primes)
    affine_reflection_cancellation_applicable = bool(
        pair_symmetric_interval and not nonunit_primes)
    symmetrized_reconstruction_error = abs(
        symmetrized_linked_prime_correlation - direct_unit_correlation)
    antisymmetric_cancellation_error = abs(
        antisymmetric_linked_prime_correlation)

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
        "unit_residues": units,
        "character_prime_correlation_values": (
            character_prime_correlation),
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
        "source_unit_mean": source_unit_mean,
        "additive_unit_source_values": additive_unit_values,
        "principal_character_source_mean": (
            principal_character_source_mean),
        "source_mean_principal_character_relative_error": (
            abs(source_unit_mean - principal_character_source_mean)
            / source_mean_scale),
        "unit_linked_prime_pair_weight": unit_linked_prime_pair_weight,
        "constant_source_linked_prime_correlation": (
            constant_source_linked_prime_correlation),
        "principal_character_linked_prime_correlation": (
            principal_character_linked_prime_correlation),
        "principal_character_constant_component_relative_error": (
            abs(principal_character_linked_prime_correlation
                - constant_source_linked_prime_correlation)
            / principal_channel_scale),
        "centered_source_linked_prime_correlation": (
            centered_source_linked_prime_correlation),
        "centered_plus_constant_reconstruction_relative_error": (
            abs(centered_source_linked_prime_correlation
                + constant_source_linked_prime_correlation
                - direct_unit_correlation)
            / principal_channel_scale),
        "constant_source_is_principal_character_channel": bool(
            abs(source_unit_mean - principal_character_source_mean)
            / source_mean_scale <= tolerance
            and abs(principal_character_linked_prime_correlation
                    - constant_source_linked_prime_correlation)
            / principal_channel_scale <= tolerance),
        "admissible_residue_count": len(admissible_columns),
        "affine_reflection_is_involution": affine_reflection_is_involution,
        "symmetric_source_energy": symmetric_source_energy,
        "antisymmetric_source_energy": antisymmetric_source_energy,
        "symmetric_source_energy_fraction": (
            symmetric_source_energy / source_energy
            if source_energy else None),
        "antisymmetric_source_energy_fraction": (
            antisymmetric_source_energy / source_energy
            if source_energy else None),
        "affine_projector_energy_relative_error": (
            projector_energy_error / projector_energy_scale),
        "affine_projector_orthogonality_relative_error": (
            projector_orthogonality_error / projector_energy_scale),
        "symmetrized_linked_prime_correlation": (
            symmetrized_linked_prime_correlation),
        "antisymmetric_linked_prime_correlation": (
            antisymmetric_linked_prime_correlation),
        "affine_symmetrized_reconstruction_natural_scale_relative_error": (
            symmetrized_reconstruction_error / reconstruction_scale),
        "affine_antisymmetric_cancellation_natural_scale_relative_error": (
            antisymmetric_cancellation_error / reconstruction_scale),
        "affine_reflection_cancellation_applicable": (
            affine_reflection_cancellation_applicable),
        "affine_symmetric_source_reconstructs_unit_correlation": (
            bool(symmetrized_reconstruction_error / reconstruction_scale
                 <= tolerance)
            if affine_reflection_cancellation_applicable else None),
        "affine_antisymmetric_source_cancels": (
            bool(antisymmetric_cancellation_error / reconstruction_scale
                 <= tolerance)
            if affine_reflection_cancellation_applicable else None),
        "target_divisible_by_common_modulus": target % common == 0,
        "pair_symmetric_interval": pair_symmetric_interval,
        "even_character_count": int(np.sum(even_mask)),
        "odd_character_count": int(np.sum(odd_mask)),
        "even_character_unit_correlation": even_character_correlation,
        "odd_character_unit_correlation": odd_character_correlation,
        "parity_decomposition_natural_scale_relative_error": (
            parity_reconstruction_error / reconstruction_scale),
        "maximum_odd_prime_correlation_relative_to_pair_weight": (
            maximum_odd_prime_correlation_relative_to_pair_weight),
        "odd_character_pair_cancellation_applicable": (
            odd_pair_cancellation_applicable),
        "all_odd_character_prime_correlations_cancel": (
            bool(maximum_odd_prime_correlation_relative_to_pair_weight
                 <= tolerance)
            if odd_pair_cancellation_applicable else None),
        "even_characters_reconstruct_unit_correlation": (
            bool(abs(even_character_correlation - direct_unit_correlation)
                 / reconstruction_scale <= tolerance)
            if odd_pair_cancellation_applicable else None),
    }


def affine_reflection_selection_receipt(
        maximum_symmetric_energy_fraction=.75,
        targets=LINKED_PRIME_TARGETS, tolerance=1e-12, batch_size=32):
    if (not math.isfinite(maximum_symmetric_energy_fraction)
            or not 0 <= maximum_symmetric_energy_fraction <= 1):
        raise ValueError(
            "maximum symmetric energy fraction must lie in [0, 1]")
    base = linked_prime_character_receipt(
        targets=targets, tolerance=tolerance, batch_size=batch_size)
    rows = base["rows"]
    energy_fractions = tuple(
        row["symmetric_source_energy_fraction"] for row in rows.values())
    exact_selection_passes = all(
        row["affine_reflection_cancellation_applicable"]
        and row["affine_reflection_is_involution"]
        and row["affine_symmetric_source_reconstructs_unit_correlation"]
        and row["affine_antisymmetric_source_cancels"]
        and row["affine_projector_energy_relative_error"] <= tolerance
        and row["affine_projector_orthogonality_relative_error"] <= tolerance
        for row in rows.values())
    gate_pass_count = sum(
        fraction <= maximum_symmetric_energy_fraction
        for fraction in energy_fractions)
    return {
        "families": base["families"],
        "arithmetic_period": base["arithmetic_period"],
        "targets": base["targets"],
        "maximum_symmetric_energy_fraction_gate": (
            maximum_symmetric_energy_fraction),
        "rows": rows,
        "symmetric_source_energy_fraction_range": (
            min(energy_fractions), max(energy_fractions)),
        "energy_gate_pass_count": gate_pass_count,
        "energy_gate_cell_count": len(rows),
        "all_affine_reflection_selection_identities_pass": bool(
            exact_selection_passes),
        "all_symmetric_source_energy_fractions_pass_gate": bool(
            gate_pass_count == len(rows)),
        "target_uniform_affine_reflection_selection_identity_proved": bool(
            exact_selection_passes),
        "all_canonical_cells_remove_at_least_quarter_energy": bool(
            exact_selection_passes and gate_pass_count == len(rows)),
        "uniform_quarter_energy_removal_theorem_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def linked_prime_centering_receipt(
        targets=LINKED_PRIME_TARGETS, tolerance=1e-12, batch_size=32):
    base = linked_prime_character_receipt(
        targets=targets, tolerance=tolerance, batch_size=batch_size)
    rows = base["rows"]
    constant_to_triangle_ratios = tuple(
        abs(row["constant_source_linked_prime_correlation"])
        / row["unit_linked_prime_pair_weight"]
        for row in rows.values())
    centered_to_cauchy_ratios = tuple(
        abs(row["centered_source_linked_prime_correlation"])
        / row["character_cauchy_envelope"]
        for row in rows.values())
    quotient_summaries = {}
    for quotient in sorted({key[0] for key in rows}):
        quotient_rows = {
            key: row for key, row in rows.items() if key[0] == quotient}
        target_means = {
            target: sum((
                row["source_unit_mean"]
                for (row_quotient, _, row_target), row
                in quotient_rows.items()
                if row_quotient == quotient and row_target == target), 0.0j)
            for target in base["targets"]}
        target_summaries = {}
        for target in base["targets"]:
            target_rows = tuple(
                row for (_, _, row_target), row in quotient_rows.items()
                if row_target == target)
            recombined_direct = sum((
                row["direct_unit_correlation"] for row in target_rows),
                0.0j)
            recombined_constant = sum((
                row["constant_source_linked_prime_correlation"]
                for row in target_rows), 0.0j)
            recombined_centered = sum((
                row["centered_source_linked_prime_correlation"]
                for row in target_rows), 0.0j)
            scale = max(1.0, math.fsum(
                abs(row["direct_unit_correlation"])
                + abs(row["constant_source_linked_prime_correlation"])
                + abs(row["centered_source_linked_prime_correlation"])
                for row in target_rows))
            target_summaries[target] = {
                "recombined_direct_unit_correlation": recombined_direct,
                "recombined_constant_source_correlation": (
                    recombined_constant),
                "recombined_centered_source_correlation": (
                    recombined_centered),
                "divisor_recombination_natural_scale": scale,
                "recombined_direct_relative_to_natural_scale": (
                    abs(recombined_direct) / scale),
                "recombined_constant_relative_to_natural_scale": (
                    abs(recombined_constant) / scale),
                "centered_plus_constant_reconstruction_relative_error": (
                    abs(recombined_centered + recombined_constant
                        - recombined_direct) / scale),
            }
        mean_values = tuple(target_means.values())
        source_rows = tuple(
            row for (_, _, row_target), row in quotient_rows.items()
            if row_target == base["targets"][0])
        recombined_source_values = sum((
            row["additive_unit_source_values"] for row in source_rows),
            np.zeros_like(source_rows[0]["additive_unit_source_values"]))
        source_recombination_scale = max(1.0, math.fsum(
            float(np.linalg.norm(row["additive_unit_source_values"]))
            for row in source_rows))
        quotient_summaries[quotient] = {
            "recombined_source_mean": mean_values[0],
            "maximum_target_source_mean_spread": max(
                abs(value - mean_values[0]) for value in mean_values),
            "recombined_additive_source_l2": float(
                np.linalg.norm(recombined_source_values)),
            "divisor_sectorwise_additive_source_l2": (
                source_recombination_scale),
            "additive_source_recombination_quotient": (
                float(np.linalg.norm(recombined_source_values))
                / source_recombination_scale),
            "primitive_additive_source_cancels": bool(
                float(np.linalg.norm(recombined_source_values))
                / source_recombination_scale <= tolerance),
            "target_summaries": target_summaries,
        }
    return {
        "families": base["families"],
        "arithmetic_period": base["arithmetic_period"],
        "targets": base["targets"],
        "rows": rows,
        "quotient_summaries": quotient_summaries,
        "maximum_source_mean_principal_character_relative_error": max(
            row["source_mean_principal_character_relative_error"]
            for row in rows.values()),
        "maximum_principal_constant_component_relative_error": max(
            row["principal_character_constant_component_relative_error"]
            for row in rows.values()),
        "maximum_centered_reconstruction_relative_error": max(
            row["centered_plus_constant_reconstruction_relative_error"]
            for row in rows.values()),
        "constant_source_amplitude_range": (
            min(constant_to_triangle_ratios),
            max(constant_to_triangle_ratios)),
        "centered_to_original_cauchy_envelope_ratio_range": (
            min(centered_to_cauchy_ratios), max(centered_to_cauchy_ratios)),
        "all_constant_source_components_are_principal_channels": all(
            row["constant_source_is_principal_character_channel"]
            for row in rows.values()),
        "all_divisor_recombinations_reconstruct": all(
            row["centered_plus_constant_reconstruction_relative_error"]
            <= tolerance
            for summary in quotient_summaries.values()
            for row in summary["target_summaries"].values()),
        "cancelling_primitive_source_quotients": tuple(
            quotient for quotient, summary in quotient_summaries.items()
            if summary["primitive_additive_source_cancels"]),
        "constant_component_classification": (
            "principal Dirichlet character times the actual unit "
            "linked-prime pair weight"),
        "formal_dickman_main_identification_applicable": False,
        "formal_dickman_main_identification_reason": (
            "the residue source has (quotient, divisor, target) inputs; "
            "the formal Dickman main has (polynomial, cutoff, scale) "
            "inputs and no coefficient-preserving map is defined"),
        "centered_target_dispersion_estimate_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def recombined_centered_character_receipt(
        leading_count=4, minimum_leading_energy_fraction=.90,
        targets=LINKED_PRIME_TARGETS, tolerance=1e-12, batch_size=32):
    if type(leading_count) is not int or leading_count < 1:
        raise ValueError("leading count must be a positive integer")
    if (not math.isfinite(minimum_leading_energy_fraction)
            or not 0 <= minimum_leading_energy_fraction <= 1):
        raise ValueError("minimum leading energy fraction must lie in [0, 1]")
    centering = linked_prime_centering_receipt(
        targets=targets, tolerance=tolerance, batch_size=batch_size)
    quotient = 77
    first_target = centering["targets"][0]
    source_rows = tuple(
        row for (row_quotient, _, target), row in centering["rows"].items()
        if row_quotient == quotient and target == first_target)
    units = source_rows[0]["unit_residues"]
    recombined_source = sum((
        row["additive_unit_source_values"] for row in source_rows),
        np.zeros_like(source_rows[0]["additive_unit_source_values"]))
    source_mean = complex(np.mean(recombined_source))
    centered_source = recombined_source - source_mean
    common = centering["arithmetic_period"] // quotient
    _, character_labels, character_table = _unit_character_table(
        common, units)
    group_order = len(units)
    principal_row = _principal_character_row(character_labels)
    # This orientation expands G(p) against conjugate(chi(p)), matching
    # character_prime_correlation_values and the linked-prime identity.
    coefficients = character_table @ centered_source
    principal_coefficient = coefficients[principal_row]
    nonprincipal_rows = tuple(
        row for row in range(group_order) if row != principal_row)
    coefficient_energies = np.abs(coefficients) ** 2
    nonprincipal_energy = float(np.sum(
        coefficient_energies[list(nonprincipal_rows)]))
    ranked = sorted(
        ((float(coefficient_energies[row]), character_labels[row], row)
         for row in nonprincipal_rows),
        key=lambda item: (-item[0], item[1]))
    retained = ranked[:min(leading_count, len(ranked))]
    retained_energy = math.fsum(item[0] for item in retained)
    cumulative_energy = 0.0
    characters_for_ninety_percent = 0
    for energy, _, _ in ranked:
        cumulative_energy += energy
        characters_for_ninety_percent += 1
        if cumulative_energy >= .9 * nonprincipal_energy:
            break
    expected_energy = group_order * float(
        np.sum(np.abs(centered_source) ** 2))
    reconstruction = (
        coefficients @ np.conjugate(character_table) / group_order)
    reconstruction_scale = max(
        1.0, float(np.sum(np.abs(centered_source))))
    linked_rows = {}
    for target in centering["targets"]:
        prime_row = next(
            row for (row_quotient, _, row_target), row
            in centering["rows"].items()
            if row_quotient == quotient and row_target == target)
        character_value = (
            coefficients
            @ prime_row["character_prime_correlation_values"] / group_order)
        direct_value = centering["quotient_summaries"][quotient][
            "target_summaries"][target][
                "recombined_centered_source_correlation"]
        scale = max(1.0, math.fsum(
            abs(row["centered_source_linked_prime_correlation"])
            for (row_quotient, _, row_target), row
            in centering["rows"].items()
            if row_quotient == quotient and row_target == target))
        linked_rows[target] = {
            "direct_centered_correlation": direct_value,
            "character_centered_correlation": character_value,
            "reconstruction_natural_scale_relative_error": (
                abs(character_value - direct_value) / scale),
        }
    leading_energy_fraction = (
        retained_energy / nonprincipal_energy
        if nonprincipal_energy else 1.0)
    return {
        "families": centering["families"],
        "arithmetic_period": centering["arithmetic_period"],
        "quotient": quotient,
        "common_modulus": common,
        "targets": centering["targets"],
        "divisor_count": len(source_rows),
        "unit_residues": units,
        "centered_source_values": centered_source,
        "recombined_source_mean": source_mean,
        "principal_centered_coefficient": principal_coefficient,
        "principal_centered_coefficient_relative_error": (
            abs(principal_coefficient)
            / max(1.0, math.sqrt(expected_energy))),
        "leading_nonprincipal_character_count": len(retained),
        "leading_nonprincipal_character_labels": tuple(
            item[1] for item in retained),
        "leading_nonprincipal_energy_fraction": leading_energy_fraction,
        "minimum_leading_energy_fraction_gate": (
            minimum_leading_energy_fraction),
        "characters_for_ninety_percent_energy": (
            characters_for_ninety_percent),
        "effective_nonprincipal_character_rank": (
            nonprincipal_energy * nonprincipal_energy
            / float(np.sum(
                coefficient_energies[list(nonprincipal_rows)] ** 2))
            if nonprincipal_energy else 0.0),
        "parseval_relative_error": (
            abs(nonprincipal_energy - expected_energy)
            / max(1.0, expected_energy)),
        "reconstruction_natural_scale_relative_error": (
            float(np.max(np.abs(reconstruction - centered_source)))
            / reconstruction_scale),
        "linked_prime_rows": linked_rows,
        "maximum_linked_reconstruction_relative_error": max(
            row["reconstruction_natural_scale_relative_error"]
            for row in linked_rows.values()),
        "four_character_shortcut_gate_passes": bool(
            leading_count == 4
            and leading_energy_fraction
            >= minimum_leading_energy_fraction),
        "recombined_centered_character_expansion_proved": True,
        "centered_target_dispersion_estimate_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def recombined_centered_prime_phase_scan_receipt(
        target_minimum=1000, target_maximum=5000,
        maximum_phase_ratio=.25, maximum_local_bias_ratio=.15,
        tolerance=1e-12, batch_size=32):
    if (type(target_minimum) is not int or type(target_maximum) is not int
            or target_minimum < 20 or target_minimum % 2
            or target_maximum < target_minimum or target_maximum % 2):
        raise ValueError(
            "target bounds must be even integers with 20 <= minimum <= maximum")
    if (not math.isfinite(maximum_phase_ratio)
            or not 0 <= maximum_phase_ratio <= 1):
        raise ValueError("maximum phase ratio must lie in [0, 1]")
    if (not math.isfinite(maximum_local_bias_ratio)
            or not 0 <= maximum_local_bias_ratio <= 1):
        raise ValueError("maximum local bias ratio must lie in [0, 1]")
    character = recombined_centered_character_receipt(
        targets=LINKED_PRIME_TARGETS, tolerance=tolerance,
        batch_size=batch_size)
    common = character["common_modulus"]
    source_by_residue = {
        int(unit): value for unit, value in zip(
            character["unit_residues"],
            character["centered_source_values"])}
    primes = _prime_table(target_maximum)
    local_bias_rows = {}
    for target_residue in range(0, common, 2):
        admissible_residues = tuple(
            residue for residue in source_by_residue
            if math.gcd(
                (target_residue - residue) % common, common) == 1)
        source_sum = sum((
            source_by_residue[residue]
            for residue in admissible_residues), 0.0j)
        source_absolute_mass = math.fsum(
            abs(source_by_residue[residue])
            for residue in admissible_residues)
        bias_ratio = (
            abs(source_sum) / source_absolute_mass
            if source_absolute_mass else None)
        local_bias_rows[target_residue] = {
            "admissible_residue_count": len(admissible_residues),
            "admissible_source_sum": source_sum,
            "admissible_source_absolute_mass": source_absolute_mass,
            "local_bias_ratio": bias_ratio,
            "passes_local_bias_gate": (
                bool(bias_ratio <= maximum_local_bias_ratio)
                if bias_ratio is not None else None),
        }
    rows = {}
    contribution_rows = {}
    for target in range(target_minimum, target_maximum + 1, 2):
        lower = target // 3
        upper = target - lower
        contributions = []
        direct = 0.0j
        triangle = 0.0
        unit_residue_weights = {
            residue: 0.0 for residue in source_by_residue
            if math.gcd((target - residue) % common, common) == 1}
        nonunit_primes = []
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if not primes[prime] or not primes[partner]:
                continue
            weight = math.log(prime) * math.log(partner)
            if math.gcd(prime, common) != 1:
                nonunit_primes.append(prime)
                continue
            source_value = source_by_residue[prime % common]
            contribution = weight * source_value
            direct += contribution
            triangle += weight * abs(source_value)
            if prime % common in unit_residue_weights:
                unit_residue_weights[prime % common] += weight
            contributions.append((
                prime, partner, prime % common, weight,
                source_value, contribution))
        ratio = abs(direct) / triangle if triangle else None
        local_decomposition_applicable = not nonunit_primes
        total_unit_weight = math.fsum(unit_residue_weights.values())
        uniform_residue_weight = (
            total_unit_weight / len(unit_residue_weights)
            if unit_residue_weights else 0.0)
        local_main_correlation = (
            uniform_residue_weight * local_bias_rows[target % common][
                "admissible_source_sum"]
            if local_decomposition_applicable else None)
        discrepancy_correlation = (
            sum((
                (weight - uniform_residue_weight)
                * source_by_residue[residue]
                for residue, weight in unit_residue_weights.items()), 0.0j)
            if local_decomposition_applicable else None)
        decomposition_scale = max(
            1.0, triangle,
            abs(local_main_correlation or 0.0j),
            abs(discrepancy_correlation or 0.0j))
        decomposition_error = (
            abs(local_main_correlation + discrepancy_correlation - direct)
            / decomposition_scale
            if local_decomposition_applicable else None)
        rows[target] = {
            "target_residue": target % common,
            "linked_prime_pair_count": len(contributions),
            "nonunit_prime_terms": tuple(nonunit_primes),
            "direct_centered_correlation": direct,
            "direct_triangle_mass": triangle,
            "phase_cancellation_ratio": ratio,
            "total_unit_linked_prime_weight": total_unit_weight,
            "uniform_admissible_residue_weight": uniform_residue_weight,
            "local_uniform_main_correlation": local_main_correlation,
            "prime_residue_discrepancy_correlation": (
                discrepancy_correlation),
            "local_main_to_triangle_ratio": (
                abs(local_main_correlation) / triangle
                if local_main_correlation is not None and triangle else None),
            "discrepancy_to_triangle_ratio": (
                abs(discrepancy_correlation) / triangle
                if discrepancy_correlation is not None and triangle else None),
            "local_uniform_plus_discrepancy_relative_error": (
                decomposition_error),
            "local_residue_decomposition_applicable": (
                local_decomposition_applicable),
            "passes_phase_ratio_gate": (
                bool(ratio <= maximum_phase_ratio)
                if ratio is not None else None),
        }
        contribution_rows[target] = tuple(contributions)

    nonempty_targets = tuple(
        target for target, row in rows.items()
        if row["phase_cancellation_ratio"] is not None)
    worst_target = (
        max(nonempty_targets,
            key=lambda target: rows[target]["phase_cancellation_ratio"])
        if nonempty_targets else None)
    worst_contributions = (
        tuple(sorted(
            contribution_rows[worst_target],
            key=lambda item: (-abs(item[-1]), item[0])))
        if worst_target is not None else ())
    gate_pass_count = sum(
        rows[target]["passes_phase_ratio_gate"]
        for target in nonempty_targets)
    applicable_decomposition_rows = tuple(
        row for row in rows.values()
        if row["local_residue_decomposition_applicable"])
    nonzero_local_bias_rows = tuple(
        row for row in local_bias_rows.values()
        if row["local_bias_ratio"] is not None)
    worst_local_bias_residue = max(
        local_bias_rows,
        key=lambda residue: (
            local_bias_rows[residue]["local_bias_ratio"]
            if local_bias_rows[residue]["local_bias_ratio"] is not None
            else -1))
    return {
        "families": character["families"],
        "arithmetic_period": character["arithmetic_period"],
        "quotient": character["quotient"],
        "common_modulus": common,
        "target_range": (target_minimum, target_maximum),
        "interval_convention": "floor(N/3) < p < N-floor(N/3)",
        "maximum_phase_ratio_gate": maximum_phase_ratio,
        "maximum_local_bias_ratio_gate": maximum_local_bias_ratio,
        "rows": rows,
        "local_bias_rows": local_bias_rows,
        "tested_target_count": len(rows),
        "nonempty_target_count": len(nonempty_targets),
        "empty_target_count": len(rows) - len(nonempty_targets),
        "phase_gate_pass_count": gate_pass_count,
        "worst_target": worst_target,
        "worst_target_row": (
            rows[worst_target] if worst_target is not None else None),
        "worst_target_contributions": worst_contributions,
        "worst_local_bias_residue": worst_local_bias_residue,
        "worst_local_bias_row": local_bias_rows[
            worst_local_bias_residue],
        "all_even_residues_pass_local_bias_gate": all(
            row["passes_local_bias_gate"]
            for row in nonzero_local_bias_rows),
        "maximum_local_decomposition_relative_error": max(
            (row["local_uniform_plus_discrepancy_relative_error"]
             for row in applicable_decomposition_rows), default=0.0),
        "all_applicable_local_residue_decompositions_reconstruct": all(
            row["local_uniform_plus_discrepancy_relative_error"]
            <= tolerance for row in applicable_decomposition_rows),
        "all_prime_terms_are_units": all(
            not row["nonunit_prime_terms"] for row in rows.values()),
        "all_tested_nonempty_targets_pass_phase_gate": (
            bool(gate_pass_count == len(nonempty_targets))
            if nonempty_targets else None),
        "finite_range_phase_cancellation_measured": bool(
            nonempty_targets),
        "uniform_phase_cancellation_proved": False,
        "prime_residue_discrepancy_estimate_proved": False,
        "centered_target_dispersion_estimate_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def resonant_progression_discrepancy_receipt(
        target_minimum=1000, target_maximum=100000,
        target_residue=88, maximum_sqrt_pair_scaled_discrepancy=4.0,
        tolerance=1e-12, batch_size=32):
    if (type(target_minimum) is not int or type(target_maximum) is not int
            or target_minimum < 20 or target_minimum % 2
            or target_maximum < target_minimum or target_maximum % 2):
        raise ValueError(
            "target bounds must be even integers with 20 <= minimum <= maximum")
    if type(target_residue) is not int:
        raise ValueError("target residue must be an integer")
    if (not math.isfinite(maximum_sqrt_pair_scaled_discrepancy)
            or maximum_sqrt_pair_scaled_discrepancy < 0):
        raise ValueError(
            "scaled discrepancy gate must be finite and nonnegative")
    common = 130
    target_residue %= common
    if target_residue % 2:
        raise ValueError("target residue must be even modulo the common modulus")
    first_target = (
        target_minimum
        + (target_residue - target_minimum) % common)
    targets = tuple(range(first_target, target_maximum + 1, common))
    if not targets:
        raise ValueError(
            "target range must contain the selected residue progression")
    character = recombined_centered_character_receipt(
        targets=LINKED_PRIME_TARGETS, tolerance=tolerance,
        batch_size=batch_size)
    if character["common_modulus"] != common:
        raise AssertionError("unexpected recombined centered source modulus")
    source_by_residue = {
        int(unit): value for unit, value in zip(
            character["unit_residues"],
            character["centered_source_values"])}
    admissible_residues = tuple(
        residue for residue in source_by_residue
        if math.gcd((target_residue - residue) % common, common) == 1)
    admissible_source_sum = sum((
        source_by_residue[residue] for residue in admissible_residues),
        0.0j)
    primes = _prime_table(target_maximum)
    rows = {}
    residue_weight_rows = {}
    for target in targets:
        lower = target // 3
        upper = target - lower
        residue_weights = {residue: 0.0 for residue in admissible_residues}
        direct = 0.0j
        triangle = 0.0
        pair_count = 0
        nonunit_primes = []
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if not primes[prime] or not primes[partner]:
                continue
            if (math.gcd(prime, common) != 1
                    or math.gcd(partner, common) != 1):
                nonunit_primes.append(prime)
                continue
            weight = math.log(prime) * math.log(partner)
            residue = prime % common
            source_value = source_by_residue[residue]
            residue_weights[residue] += weight
            direct += weight * source_value
            triangle += weight * abs(source_value)
            pair_count += 1
        total_weight = math.fsum(residue_weights.values())
        uniform_weight = total_weight / len(admissible_residues)
        local_main = uniform_weight * admissible_source_sum
        discrepancy = sum((
            (weight - uniform_weight) * source_by_residue[residue]
            for residue, weight in residue_weights.items()), 0.0j)
        discrepancy_ratio = abs(discrepancy) / triangle if triangle else None
        scaled_discrepancy = (
            math.sqrt(pair_count) * discrepancy_ratio
            if discrepancy_ratio is not None else None)
        scale = max(1.0, triangle, abs(local_main), abs(discrepancy))
        rows[target] = {
            "linked_prime_pair_count": pair_count,
            "nonunit_prime_terms": tuple(nonunit_primes),
            "direct_centered_correlation": direct,
            "direct_triangle_mass": triangle,
            "local_uniform_main_correlation": local_main,
            "prime_residue_discrepancy_correlation": discrepancy,
            "discrepancy_to_triangle_ratio": discrepancy_ratio,
            "sqrt_pair_scaled_discrepancy": scaled_discrepancy,
            "local_uniform_plus_discrepancy_relative_error": (
                abs(local_main + discrepancy - direct) / scale),
            "passes_sqrt_pair_scaled_discrepancy_gate": (
                bool(scaled_discrepancy
                     <= maximum_sqrt_pair_scaled_discrepancy)
                if scaled_discrepancy is not None else None),
        }
        residue_weight_rows[target] = residue_weights

    nonempty_targets = tuple(
        target for target, row in rows.items()
        if row["sqrt_pair_scaled_discrepancy"] is not None)
    if not nonempty_targets:
        raise ValueError(
            "selected progression has no unit-supported linked-prime target")
    worst_target = max(
        nonempty_targets,
        key=lambda target: rows[target]["sqrt_pair_scaled_discrepancy"])
    worst_row = rows[worst_target]
    worst_total_weight = math.fsum(
        residue_weight_rows[worst_target].values())
    worst_uniform_weight = worst_total_weight / len(admissible_residues)
    worst_residue_contributions = tuple(sorted((
        (residue, weight, weight - worst_uniform_weight,
         source_by_residue[residue],
         (weight - worst_uniform_weight) * source_by_residue[residue])
        for residue, weight in residue_weight_rows[worst_target].items()),
        key=lambda item: (-abs(item[-1]), item[0])))
    dyadic_block_summaries = {}
    block_lower = target_minimum
    while block_lower <= target_maximum:
        block_upper = min(target_maximum + 1, 2 * block_lower)
        block_targets = tuple(
            target for target in nonempty_targets
            if block_lower <= target < block_upper)
        if block_targets:
            values = tuple(
                rows[target]["sqrt_pair_scaled_discrepancy"]
                for target in block_targets)
            maximum_target = max(
                block_targets,
                key=lambda target: rows[target][
                    "sqrt_pair_scaled_discrepancy"])
            dyadic_block_summaries[(block_lower, block_upper)] = {
                "target_count": len(block_targets),
                "maximum_scaled_discrepancy": max(values),
                "median_scaled_discrepancy": float(np.median(values)),
                "maximum_target": maximum_target,
            }
        block_lower *= 2
    gate_pass_count = sum(
        rows[target]["passes_sqrt_pair_scaled_discrepancy_gate"]
        for target in nonempty_targets)
    return {
        "families": character["families"],
        "arithmetic_period": character["arithmetic_period"],
        "quotient": character["quotient"],
        "common_modulus": common,
        "target_range": (target_minimum, target_maximum),
        "target_residue": target_residue,
        "progression_step": common,
        "maximum_sqrt_pair_scaled_discrepancy_gate": (
            maximum_sqrt_pair_scaled_discrepancy),
        "rows": rows,
        "tested_target_count": len(rows),
        "nonempty_target_count": len(nonempty_targets),
        "gate_pass_count": gate_pass_count,
        "worst_target": worst_target,
        "worst_target_row": worst_row,
        "worst_residue_discrepancy_contributions": (
            worst_residue_contributions),
        "dyadic_block_summaries": dyadic_block_summaries,
        "maximum_decomposition_relative_error": max(
            row["local_uniform_plus_discrepancy_relative_error"]
            for row in rows.values()),
        "all_prime_terms_are_units": all(
            not row["nonunit_prime_terms"] for row in rows.values()),
        "all_progression_targets_pass_scaled_discrepancy_gate": bool(
            gate_pass_count == len(nonempty_targets)),
        "finite_progression_discrepancy_measured": True,
        "square_root_discrepancy_bound_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def resonant_progression_diagonal_square_receipt(
        target_minimum=1000, target_maximum=100000,
        target_residue=88, maximum_pointwise_ratio=4.0,
        maximum_paired_pointwise_ratio=4.0,
        tolerance=1e-12, batch_size=32):
    if (type(target_minimum) is not int or type(target_maximum) is not int
            or target_minimum < 20 or target_minimum % 2
            or target_maximum < target_minimum or target_maximum % 2):
        raise ValueError(
            "target bounds must be even integers with 20 <= minimum <= maximum")
    if type(target_residue) is not int:
        raise ValueError("target residue must be an integer")
    if not math.isfinite(maximum_pointwise_ratio) or maximum_pointwise_ratio < 0:
        raise ValueError("pointwise ratio gate must be finite and nonnegative")
    if (not math.isfinite(maximum_paired_pointwise_ratio)
            or maximum_paired_pointwise_ratio < 0):
        raise ValueError(
            "paired pointwise ratio gate must be finite and nonnegative")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    if type(batch_size) is not int or batch_size < 1:
        raise ValueError("batch size must be a positive integer")
    common = 130
    target_residue %= common
    if target_residue % 2:
        raise ValueError("target residue must be even modulo the common modulus")
    first_target = (
        target_minimum
        + (target_residue - target_minimum) % common)
    targets = tuple(range(first_target, target_maximum + 1, common))
    if not targets:
        raise ValueError(
            "target range must contain the selected residue progression")
    character = recombined_centered_character_receipt(
        targets=LINKED_PRIME_TARGETS, tolerance=tolerance,
        batch_size=batch_size)
    if character["common_modulus"] != common:
        raise AssertionError("unexpected recombined centered source modulus")
    source_by_residue = {
        int(unit): value for unit, value in zip(
            character["unit_residues"],
            character["centered_source_values"])}
    admissible_residues = tuple(
        residue for residue in source_by_residue
        if math.gcd((target_residue - residue) % common, common) == 1)
    admissible_source_mean = sum((
        source_by_residue[residue] for residue in admissible_residues),
        0.0j) / len(admissible_residues)
    centered_source_by_residue = {
        residue: source_by_residue[residue] - admissible_source_mean
        for residue in admissible_residues}
    centered_source_sum = sum(centered_source_by_residue.values(), 0.0j)
    centered_source_scale = max(
        1.0,
        math.fsum(abs(value) for value in centered_source_by_residue.values()))
    primes = _prime_table(target_maximum)
    rows = {}
    for target in targets:
        lower = target // 3
        upper = target - lower
        discrepancy = 0.0j
        diagonal_square_function = 0.0
        paired_discrepancy = 0.0j
        paired_square_function = 0.0
        reflection_block_count = 0
        pair_count = 0
        nonunit_primes = []
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if not primes[prime] or not primes[partner]:
                continue
            if (math.gcd(prime, common) != 1
                    or math.gcd(partner, common) != 1):
                nonunit_primes.append(prime)
                continue
            weight = math.log(prime) * math.log(partner)
            centered_source = centered_source_by_residue[prime % common]
            term = weight * centered_source
            discrepancy += term
            diagonal_square_function += abs(term) ** 2
            pair_count += 1
            if prime <= partner:
                if prime < partner:
                    partner_source = centered_source_by_residue[
                        partner % common]
                    block_term = weight * (
                        centered_source + partner_source)
                else:
                    block_term = term
                paired_discrepancy += block_term
                paired_square_function += abs(block_term) ** 2
                reflection_block_count += 1
        diagonal_scale = math.sqrt(diagonal_square_function)
        pointwise_ratio = (
            abs(discrepancy) / diagonal_scale
            if diagonal_scale else None)
        paired_scale = math.sqrt(paired_square_function)
        paired_pointwise_ratio = (
            abs(paired_discrepancy) / paired_scale
            if paired_scale else None)
        reconstruction_scale = max(
            1.0, abs(discrepancy), abs(paired_discrepancy))
        rows[target] = {
            "linked_prime_pair_count": pair_count,
            "reflection_block_count": reflection_block_count,
            "nonunit_prime_terms": tuple(nonunit_primes),
            "centered_discrepancy_correlation": discrepancy,
            "diagonal_square_function": diagonal_square_function,
            "diagonal_scale": diagonal_scale,
            "pointwise_discrepancy_to_diagonal_ratio": pointwise_ratio,
            "paired_centered_discrepancy_correlation": paired_discrepancy,
            "paired_reflection_square_function": paired_square_function,
            "paired_reflection_scale": paired_scale,
            "pointwise_discrepancy_to_paired_ratio": (
                paired_pointwise_ratio),
            "ordered_to_paired_discrepancy_relative_error": (
                abs(discrepancy - paired_discrepancy)
                / reconstruction_scale),
            "passes_pointwise_diagonal_gate": (
                bool(pointwise_ratio <= maximum_pointwise_ratio)
                if pointwise_ratio is not None else None),
            "passes_paired_pointwise_gate": (
                bool(paired_pointwise_ratio
                     <= maximum_paired_pointwise_ratio)
                if paired_pointwise_ratio is not None else None),
        }

    nonempty_targets = tuple(
        target for target, row in rows.items()
        if row["pointwise_discrepancy_to_diagonal_ratio"] is not None)
    if not nonempty_targets:
        raise ValueError(
            "selected progression has no nonzero diagonal linked-prime target")
    worst_target = max(
        nonempty_targets,
        key=lambda target: rows[target][
            "pointwise_discrepancy_to_diagonal_ratio"])
    paired_nonempty_targets = tuple(
        target for target, row in rows.items()
        if row["pointwise_discrepancy_to_paired_ratio"] is not None)
    if not paired_nonempty_targets:
        raise ValueError(
            "selected progression has no nonzero paired linked-prime target")
    worst_paired_target = max(
        paired_nonempty_targets,
        key=lambda target: rows[target][
            "pointwise_discrepancy_to_paired_ratio"])
    dyadic_block_summaries = {}
    block_lower = target_minimum
    while block_lower <= target_maximum:
        block_upper = min(target_maximum + 1, 2 * block_lower)
        block_targets = tuple(
            target for target in nonempty_targets
            if block_lower <= target < block_upper)
        if block_targets:
            ratios = tuple(
                rows[target]["pointwise_discrepancy_to_diagonal_ratio"]
                for target in block_targets)
            summed_squared_discrepancy = math.fsum(
                abs(rows[target]["centered_discrepancy_correlation"]) ** 2
                for target in block_targets)
            summed_diagonal_square_function = math.fsum(
                rows[target]["diagonal_square_function"]
                for target in block_targets)
            summed_paired_square_function = math.fsum(
                rows[target]["paired_reflection_square_function"]
                for target in block_targets)
            paired_ratios = tuple(
                rows[target]["pointwise_discrepancy_to_paired_ratio"]
                for target in block_targets)
            maximum_target = max(
                block_targets,
                key=lambda target: rows[target][
                    "pointwise_discrepancy_to_diagonal_ratio"])
            dyadic_block_summaries[(block_lower, block_upper)] = {
                "target_count": len(block_targets),
                "maximum_pointwise_ratio": max(ratios),
                "median_pointwise_ratio": float(np.median(ratios)),
                "maximum_target": maximum_target,
                "summed_squared_discrepancy": summed_squared_discrepancy,
                "summed_diagonal_square_function": (
                    summed_diagonal_square_function),
                "summed_squared_to_diagonal_ratio": (
                    summed_squared_discrepancy
                    / summed_diagonal_square_function),
                "maximum_paired_pointwise_ratio": max(paired_ratios),
                "median_paired_pointwise_ratio": float(
                    np.median(paired_ratios)),
                "summed_paired_reflection_square_function": (
                    summed_paired_square_function),
                "summed_squared_to_paired_ratio": (
                    summed_squared_discrepancy
                    / summed_paired_square_function),
            }
        block_lower *= 2
    gate_pass_count = sum(
        rows[target]["passes_pointwise_diagonal_gate"]
        for target in nonempty_targets)
    paired_gate_pass_count = sum(
        rows[target]["passes_paired_pointwise_gate"]
        for target in paired_nonempty_targets)
    return {
        "families": character["families"],
        "arithmetic_period": character["arithmetic_period"],
        "quotient": character["quotient"],
        "common_modulus": common,
        "target_range": (target_minimum, target_maximum),
        "target_residue": target_residue,
        "progression_step": common,
        "admissible_residue_count": len(admissible_residues),
        "admissible_source_mean": admissible_source_mean,
        "centered_source_sum_relative_error": (
            abs(centered_source_sum) / centered_source_scale),
        "maximum_pointwise_ratio_gate": maximum_pointwise_ratio,
        "maximum_paired_pointwise_ratio_gate": (
            maximum_paired_pointwise_ratio),
        "rows": rows,
        "tested_target_count": len(rows),
        "nonempty_target_count": len(nonempty_targets),
        "gate_pass_count": gate_pass_count,
        "paired_gate_pass_count": paired_gate_pass_count,
        "worst_target": worst_target,
        "worst_target_row": rows[worst_target],
        "worst_paired_target": worst_paired_target,
        "worst_paired_target_row": rows[worst_paired_target],
        "dyadic_block_summaries": dyadic_block_summaries,
        "all_prime_terms_are_units": all(
            not row["nonunit_prime_terms"] for row in rows.values()),
        "all_progression_targets_pass_pointwise_diagonal_gate": bool(
            gate_pass_count == len(nonempty_targets)),
        "all_ordered_and_paired_discrepancies_reconstruct": all(
            row["ordered_to_paired_discrepancy_relative_error"] <= tolerance
            for row in rows.values()),
        "all_progression_targets_pass_paired_pointwise_gate": bool(
            paired_gate_pass_count == len(paired_nonempty_targets)),
        "finite_diagonal_square_function_measured": True,
        "finite_paired_reflection_square_function_measured": True,
        "pointwise_diagonal_bound_proved": False,
        "pointwise_paired_reflection_bound_proved": False,
        "averaged_diagonal_bound_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def all_residue_reflection_block_receipt(
        target_minimum=1000, target_maximum=20000,
        maximum_pointwise_ratio=4.0, tolerance=1e-12, batch_size=32):
    if (type(target_minimum) is not int or type(target_maximum) is not int
            or target_minimum < 20 or target_minimum % 2
            or target_maximum < target_minimum or target_maximum % 2):
        raise ValueError(
            "target bounds must be even integers with 20 <= minimum <= maximum")
    if not math.isfinite(maximum_pointwise_ratio) or maximum_pointwise_ratio < 0:
        raise ValueError("pointwise ratio gate must be finite and nonnegative")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    if type(batch_size) is not int or batch_size < 1:
        raise ValueError("batch size must be a positive integer")
    common = 130
    character = recombined_centered_character_receipt(
        targets=LINKED_PRIME_TARGETS, tolerance=tolerance,
        batch_size=batch_size)
    if character["common_modulus"] != common:
        raise AssertionError("unexpected recombined centered source modulus")
    source_by_residue = {
        int(unit): value for unit, value in zip(
            character["unit_residues"],
            character["centered_source_values"])}
    even_residues = tuple(range(0, common, 2))
    local_sources = {}
    for target_residue in even_residues:
        admissible_residues = tuple(
            residue for residue in source_by_residue
            if math.gcd(
                (target_residue - residue) % common, common) == 1)
        source_mean = sum((
            source_by_residue[residue] for residue in admissible_residues),
            0.0j) / len(admissible_residues)
        centered_source = {
            residue: source_by_residue[residue] - source_mean
            for residue in admissible_residues}
        centered_sum = sum(centered_source.values(), 0.0j)
        centered_scale = max(
            1.0, math.fsum(abs(value) for value in centered_source.values()))
        local_sources[target_residue] = {
            "admissible_residues": admissible_residues,
            "source_mean": source_mean,
            "centered_source": centered_source,
            "centered_source_sum_relative_error": (
                abs(centered_sum) / centered_scale),
        }

    primes = _prime_table(target_maximum)
    rows = {}
    for target in range(target_minimum, target_maximum + 1, 2):
        target_residue = target % common
        centered_source = local_sources[target_residue]["centered_source"]
        lower = target // 3
        discrepancy = 0.0j
        paired_square_function = 0.0
        reflection_block_count = 0
        ordered_pair_count = 0
        nonunit_primes = []
        for prime in range(max(2, lower + 1), target // 2 + 1):
            partner = target - prime
            if not primes[prime] or not primes[partner]:
                continue
            if (math.gcd(prime, common) != 1
                    or math.gcd(partner, common) != 1):
                nonunit_primes.append((prime, partner))
                continue
            weight = math.log(prime) * math.log(partner)
            if prime < partner:
                block_term = weight * (
                    centered_source[prime % common]
                    + centered_source[partner % common])
                ordered_pair_count += 2
            else:
                block_term = weight * centered_source[prime % common]
                ordered_pair_count += 1
            discrepancy += block_term
            paired_square_function += abs(block_term) ** 2
            reflection_block_count += 1
        paired_scale = math.sqrt(paired_square_function)
        pointwise_ratio = (
            abs(discrepancy) / paired_scale if paired_scale else None)
        rows[target] = {
            "target_residue": target_residue,
            "ordered_linked_prime_pair_count": ordered_pair_count,
            "reflection_block_count": reflection_block_count,
            "nonunit_prime_pairs": tuple(nonunit_primes),
            "centered_discrepancy_correlation": discrepancy,
            "paired_reflection_square_function": paired_square_function,
            "paired_reflection_scale": paired_scale,
            "pointwise_discrepancy_to_paired_ratio": pointwise_ratio,
            "passes_pointwise_gate": (
                bool(pointwise_ratio <= maximum_pointwise_ratio)
                if pointwise_ratio is not None else None),
        }

    nonempty_targets = tuple(
        target for target, row in rows.items()
        if row["pointwise_discrepancy_to_paired_ratio"] is not None)
    if not nonempty_targets:
        raise ValueError("target range has no nonzero paired linked-prime target")
    worst_target = max(
        nonempty_targets,
        key=lambda target: rows[target][
            "pointwise_discrepancy_to_paired_ratio"])
    residue_summaries = {}
    for target_residue in even_residues:
        residue_targets = tuple(
            target for target in nonempty_targets
            if rows[target]["target_residue"] == target_residue)
        if not residue_targets:
            residue_summaries[target_residue] = {
                "target_count": 0,
                "maximum_pointwise_ratio": None,
                "median_pointwise_ratio": None,
                "maximum_target": None,
                "summed_squared_to_paired_ratio": None,
            }
            continue
        ratios = tuple(
            rows[target]["pointwise_discrepancy_to_paired_ratio"]
            for target in residue_targets)
        summed_squared_discrepancy = math.fsum(
            abs(rows[target]["centered_discrepancy_correlation"]) ** 2
            for target in residue_targets)
        summed_paired_square_function = math.fsum(
            rows[target]["paired_reflection_square_function"]
            for target in residue_targets)
        maximum_target = max(
            residue_targets,
            key=lambda target: rows[target][
                "pointwise_discrepancy_to_paired_ratio"])
        residue_summaries[target_residue] = {
            "target_count": len(residue_targets),
            "maximum_pointwise_ratio": max(ratios),
            "median_pointwise_ratio": float(np.median(ratios)),
            "maximum_target": maximum_target,
            "summed_squared_discrepancy": summed_squared_discrepancy,
            "summed_paired_reflection_square_function": (
                summed_paired_square_function),
            "summed_squared_to_paired_ratio": (
                summed_squared_discrepancy / summed_paired_square_function),
        }
    dyadic_block_summaries = {}
    block_lower = target_minimum
    while block_lower <= target_maximum:
        block_upper = min(target_maximum + 1, 2 * block_lower)
        block_targets = tuple(
            target for target in nonempty_targets
            if block_lower <= target < block_upper)
        if block_targets:
            ratios = tuple(
                rows[target]["pointwise_discrepancy_to_paired_ratio"]
                for target in block_targets)
            summed_squared_discrepancy = math.fsum(
                abs(rows[target]["centered_discrepancy_correlation"]) ** 2
                for target in block_targets)
            summed_paired_square_function = math.fsum(
                rows[target]["paired_reflection_square_function"]
                for target in block_targets)
            maximum_target = max(
                block_targets,
                key=lambda target: rows[target][
                    "pointwise_discrepancy_to_paired_ratio"])
            dyadic_block_summaries[(block_lower, block_upper)] = {
                "target_count": len(block_targets),
                "maximum_pointwise_ratio": max(ratios),
                "median_pointwise_ratio": float(np.median(ratios)),
                "maximum_target": maximum_target,
                "summed_squared_discrepancy": summed_squared_discrepancy,
                "summed_paired_reflection_square_function": (
                    summed_paired_square_function),
                "summed_squared_to_paired_ratio": (
                    summed_squared_discrepancy
                    / summed_paired_square_function),
            }
        block_lower *= 2
    gate_pass_count = sum(
        rows[target]["passes_pointwise_gate"] for target in nonempty_targets)
    return {
        "families": character["families"],
        "arithmetic_period": character["arithmetic_period"],
        "quotient": character["quotient"],
        "common_modulus": common,
        "target_range": (target_minimum, target_maximum),
        "maximum_pointwise_ratio_gate": maximum_pointwise_ratio,
        "local_source_rows": local_sources,
        "rows": rows,
        "residue_summaries": residue_summaries,
        "dyadic_block_summaries": dyadic_block_summaries,
        "tested_target_count": len(rows),
        "nonempty_target_count": len(nonempty_targets),
        "empty_target_count": len(rows) - len(nonempty_targets),
        "gate_pass_count": gate_pass_count,
        "worst_target": worst_target,
        "worst_target_row": rows[worst_target],
        "maximum_centered_source_sum_relative_error": max(
            row["centered_source_sum_relative_error"]
            for row in local_sources.values()),
        "all_prime_terms_are_units": all(
            not row["nonunit_prime_pairs"] for row in rows.values()),
        "all_nonempty_targets_pass_pointwise_gate": bool(
            gate_pass_count == len(nonempty_targets)),
        "all_even_residue_classes_measured": all(
            row["target_count"] for row in residue_summaries.values()),
        "finite_all_residue_reflection_scan_measured": True,
        "uniform_residue_pointwise_bound_proved": False,
        "uniform_residue_averaged_bound_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def residue_orbit_reinforcement_receipt(
        target_minimum=1000, target_maximum=100000, target_residue=72,
        maximum_aggregate_orbit_ratio=1.0,
        tolerance=1e-12, batch_size=32):
    if (type(target_minimum) is not int or type(target_maximum) is not int
            or target_minimum < 20 or target_minimum % 2
            or target_maximum < target_minimum or target_maximum % 2):
        raise ValueError(
            "target bounds must be even integers with 20 <= minimum <= maximum")
    if type(target_residue) is not int:
        raise ValueError("target residue must be an integer")
    if (not math.isfinite(maximum_aggregate_orbit_ratio)
            or maximum_aggregate_orbit_ratio < 0):
        raise ValueError("aggregate orbit gate must be finite and nonnegative")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    if type(batch_size) is not int or batch_size < 1:
        raise ValueError("batch size must be a positive integer")
    common = 130
    target_residue %= common
    if target_residue % 2:
        raise ValueError("target residue must be even modulo the common modulus")
    first_target = (
        target_minimum
        + (target_residue - target_minimum) % common)
    targets = tuple(range(first_target, target_maximum + 1, common))
    if not targets:
        raise ValueError(
            "target range must contain the selected residue progression")
    character = recombined_centered_character_receipt(
        targets=LINKED_PRIME_TARGETS, tolerance=tolerance,
        batch_size=batch_size)
    if character["common_modulus"] != common:
        raise AssertionError("unexpected recombined centered source modulus")
    source_by_residue = {
        int(unit): value for unit, value in zip(
            character["unit_residues"],
            character["centered_source_values"])}
    admissible_residues = tuple(
        residue for residue in source_by_residue
        if math.gcd((target_residue - residue) % common, common) == 1)
    source_mean = sum((
        source_by_residue[residue] for residue in admissible_residues),
        0.0j) / len(admissible_residues)
    centered_source = {
        residue: source_by_residue[residue] - source_mean
        for residue in admissible_residues}
    centered_sum = sum(centered_source.values(), 0.0j)
    centered_scale = max(
        1.0, math.fsum(abs(value) for value in centered_source.values()))
    unseen = set(admissible_residues)
    reflection_orbits = []
    while unseen:
        residue = min(unseen)
        partner_residue = (target_residue - residue) % common
        if partner_residue not in unseen and partner_residue != residue:
            raise AssertionError("affine reflection did not preserve admissibility")
        orbit = tuple(sorted({residue, partner_residue}))
        reflection_orbits.append(orbit)
        unseen.difference_update(orbit)
    reflection_orbits = tuple(reflection_orbits)
    orbit_by_residue = {
        residue: orbit_index
        for orbit_index, orbit in enumerate(reflection_orbits)
        for residue in orbit}
    orbit_coefficients = tuple(
        sum((centered_source[residue] for residue in orbit), 0.0j)
        for orbit in reflection_orbits)
    orbit_coefficient_sum = sum(orbit_coefficients, 0.0j)

    primes = _prime_table(target_maximum)
    rows = {}
    orbit_term_rows = {}
    orbit_weight_discrepancy_rows = {}
    for target in targets:
        lower = target // 3
        residue_weights = {
            residue: 0.0 for residue in admissible_residues}
        paired_terms = []
        paired_square_function = 0.0
        ordered_total_weight = 0.0
        ordered_pair_count = 0
        reflection_block_count = 0
        nonunit_prime_pairs = []
        for prime in range(max(2, lower + 1), target // 2 + 1):
            partner = target - prime
            if not primes[prime] or not primes[partner]:
                continue
            if (math.gcd(prime, common) != 1
                    or math.gcd(partner, common) != 1):
                nonunit_prime_pairs.append((prime, partner))
                continue
            weight = math.log(prime) * math.log(partner)
            prime_residue = prime % common
            partner_residue = partner % common
            orbit_index = orbit_by_residue[prime_residue]
            if orbit_index != orbit_by_residue[partner_residue]:
                raise AssertionError("linked residues occupy different orbits")
            if prime < partner:
                residue_weights[prime_residue] += weight
                residue_weights[partner_residue] += weight
                block_term = weight * (
                    centered_source[prime_residue]
                    + centered_source[partner_residue])
            else:
                residue_weights[prime_residue] += weight
                block_term = weight * centered_source[prime_residue]
            paired_terms.append(block_term)
            paired_square_function += abs(block_term) ** 2
            reflection_block_count += 1
            if prime < partner:
                ordered_total_weight += 2 * weight
                ordered_pair_count += 2
            else:
                ordered_total_weight += weight
                ordered_pair_count += 1
        orbit_weights = tuple(
            residue_weights[orbit[0]] for orbit in reflection_orbits)
        orbit_weight_symmetry_errors = tuple(
            abs(residue_weights[orbit[0]] - residue_weights[orbit[1]])
            if len(orbit) == 2 else 0.0
            for orbit in reflection_orbits)
        uniform_ordered_residue_weight = (
            ordered_total_weight / len(admissible_residues))
        paired_discrepancy = _complex_fsum(paired_terms)
        orbit_weight_discrepancies = tuple(
            weight - uniform_ordered_residue_weight
            for weight in orbit_weights)
        orbit_terms = tuple(
            discrepancy * coefficient
            for discrepancy, coefficient in zip(
                orbit_weight_discrepancies, orbit_coefficients))
        orbit_discrepancy = _complex_fsum(orbit_terms)
        orbit_square_function = math.fsum(
            abs(term) ** 2 for term in orbit_terms)
        orbit_scale = math.sqrt(orbit_square_function)
        scale = max(
            1.0, abs(paired_discrepancy), abs(orbit_discrepancy))
        rows[target] = {
            "ordered_linked_prime_pair_count": ordered_pair_count,
            "reflection_block_count": reflection_block_count,
            "nonunit_prime_pairs": tuple(nonunit_prime_pairs),
            "ordered_total_weight": ordered_total_weight,
            "uniform_ordered_residue_weight": uniform_ordered_residue_weight,
            "maximum_orbit_residue_weight_symmetry_error": max(
                orbit_weight_symmetry_errors),
            "paired_centered_discrepancy_correlation": paired_discrepancy,
            "paired_reflection_square_function": paired_square_function,
            "orbit_centered_discrepancy_correlation": orbit_discrepancy,
            "orbit_discrepancy_square_function": orbit_square_function,
            "orbit_discrepancy_scale": orbit_scale,
            "pointwise_discrepancy_to_orbit_ratio": (
                abs(orbit_discrepancy) / orbit_scale
                if orbit_scale else None),
            "paired_to_orbit_reconstruction_relative_error": (
                abs(paired_discrepancy - orbit_discrepancy) / scale),
        }
        orbit_term_rows[target] = orbit_terms
        orbit_weight_discrepancy_rows[target] = orbit_weight_discrepancies

    nonempty_targets = tuple(
        target for target, row in rows.items()
        if row["pointwise_discrepancy_to_orbit_ratio"] is not None)
    if not nonempty_targets:
        raise ValueError(
            "selected progression has no nonzero orbit-discrepancy target")
    summed_squared_discrepancy = math.fsum(
        abs(rows[target]["orbit_centered_discrepancy_correlation"]) ** 2
        for target in nonempty_targets)
    summed_orbit_square_function = math.fsum(
        rows[target]["orbit_discrepancy_square_function"]
        for target in nonempty_targets)
    aggregate_orbit_ratio = (
        summed_squared_discrepancy / summed_orbit_square_function)
    summed_paired_square_function = math.fsum(
        rows[target]["paired_reflection_square_function"]
        for target in nonempty_targets)
    aggregate_paired_ratio = (
        summed_squared_discrepancy / summed_paired_square_function)
    worst_target = max(
        nonempty_targets,
        key=lambda target: rows[target][
            "pointwise_discrepancy_to_orbit_ratio"])
    orbit_pair_cross_terms = tuple(sorted((
        (
            reflection_orbits[left],
            reflection_orbits[right],
            2 * math.fsum(
                (orbit_term_rows[target][left]
                 * orbit_term_rows[target][right].conjugate()).real
                for target in nonempty_targets),
        )
        for left in range(len(reflection_orbits))
        for right in range(left + 1, len(reflection_orbits))),
        key=lambda item: (-item[2], item[0], item[1])))
    summed_cross_orbit_terms = math.fsum(
        item[2] for item in orbit_pair_cross_terms)
    cross_term_scale = max(
        1.0, summed_squared_discrepancy,
        summed_orbit_square_function, abs(summed_cross_orbit_terms))
    dyadic_block_summaries = {}
    block_lower = target_minimum
    while block_lower <= target_maximum:
        block_upper = min(target_maximum + 1, 2 * block_lower)
        block_targets = tuple(
            target for target in nonempty_targets
            if block_lower <= target < block_upper)
        if block_targets:
            block_squared_discrepancy = math.fsum(
                abs(rows[target][
                    "orbit_centered_discrepancy_correlation"]) ** 2
                for target in block_targets)
            block_orbit_square_function = math.fsum(
                rows[target]["orbit_discrepancy_square_function"]
                for target in block_targets)
            block_paired_square_function = math.fsum(
                rows[target]["paired_reflection_square_function"]
                for target in block_targets)
            maximum_target = max(
                block_targets,
                key=lambda target: rows[target][
                    "pointwise_discrepancy_to_orbit_ratio"])
            dyadic_block_summaries[(block_lower, block_upper)] = {
                "target_count": len(block_targets),
                "maximum_pointwise_orbit_ratio": rows[maximum_target][
                    "pointwise_discrepancy_to_orbit_ratio"],
                "maximum_target": maximum_target,
                "summed_squared_discrepancy": block_squared_discrepancy,
                "summed_orbit_square_function": (
                    block_orbit_square_function),
                "summed_paired_square_function": (
                    block_paired_square_function),
                "aggregate_orbit_ratio": (
                    block_squared_discrepancy
                    / block_orbit_square_function),
                "aggregate_paired_ratio": (
                    block_squared_discrepancy
                    / block_paired_square_function),
                "passes_aggregate_orbit_gate": bool(
                    block_squared_discrepancy / block_orbit_square_function
                    <= maximum_aggregate_orbit_ratio),
            }
        block_lower *= 2
    return {
        "families": character["families"],
        "arithmetic_period": character["arithmetic_period"],
        "quotient": character["quotient"],
        "common_modulus": common,
        "target_range": (target_minimum, target_maximum),
        "target_residue": target_residue,
        "progression_step": common,
        "admissible_residues": admissible_residues,
        "reflection_orbits": reflection_orbits,
        "orbit_coefficients": orbit_coefficients,
        "centered_source_sum_relative_error": (
            abs(centered_sum) / centered_scale),
        "orbit_coefficient_sum_relative_error": (
            abs(orbit_coefficient_sum) / centered_scale),
        "maximum_aggregate_orbit_ratio_gate": (
            maximum_aggregate_orbit_ratio),
        "rows": rows,
        "orbit_term_rows": orbit_term_rows,
        "orbit_weight_discrepancy_rows": orbit_weight_discrepancy_rows,
        "tested_target_count": len(rows),
        "nonempty_target_count": len(nonempty_targets),
        "aggregate_orbit_ratio": aggregate_orbit_ratio,
        "aggregate_paired_ratio": aggregate_paired_ratio,
        "net_cross_orbit_to_orbit_diagonal_ratio": (
            summed_cross_orbit_terms / summed_orbit_square_function),
        "cross_term_reconstruction_relative_error": abs(
            summed_orbit_square_function + summed_cross_orbit_terms
            - summed_squared_discrepancy) / cross_term_scale,
        "passes_full_aggregate_orbit_gate": bool(
            aggregate_orbit_ratio <= maximum_aggregate_orbit_ratio),
        "all_dyadic_blocks_pass_aggregate_orbit_gate": all(
            row["passes_aggregate_orbit_gate"]
            for row in dyadic_block_summaries.values()),
        "worst_target": worst_target,
        "worst_target_row": rows[worst_target],
        "orbit_pair_cross_terms": orbit_pair_cross_terms,
        "dyadic_block_summaries": dyadic_block_summaries,
        "maximum_reconstruction_relative_error": max(
            row["paired_to_orbit_reconstruction_relative_error"]
            for row in rows.values()),
        "maximum_orbit_residue_weight_symmetry_error": max(
            row["maximum_orbit_residue_weight_symmetry_error"]
            for row in rows.values()),
        "all_prime_terms_are_units": all(
            not row["nonunit_prime_pairs"] for row in rows.values()),
        "all_orbit_discrepancies_reconstruct": all(
            row["paired_to_orbit_reconstruction_relative_error"] <= tolerance
            for row in rows.values()),
        "all_two_element_orbit_residue_weights_match": all(
            row["maximum_orbit_residue_weight_symmetry_error"] <= tolerance
            for row in rows.values()),
        "finite_residue_orbit_reinforcement_measured": True,
        "orbit_reinforcement_bound_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def residue_orbit_sign_cube_receipt(
        target_minimum=1000, target_maximum=100000, target_residue=72,
        maximum_actual_upper_tail_fraction=.05,
        minimum_stable_dyadic_block_count=5,
        tolerance=1e-12, batch_size=32):
    if (not math.isfinite(maximum_actual_upper_tail_fraction)
            or not 0 <= maximum_actual_upper_tail_fraction <= 1):
        raise ValueError("upper-tail fraction gate must lie in [0, 1]")
    if (type(minimum_stable_dyadic_block_count) is not int
            or minimum_stable_dyadic_block_count < 0):
        raise ValueError(
            "minimum stable dyadic block count must be a nonnegative integer")
    base = residue_orbit_reinforcement_receipt(
        target_minimum=target_minimum,
        target_maximum=target_maximum,
        target_residue=target_residue,
        tolerance=tolerance,
        batch_size=batch_size)
    targets = tuple(base["orbit_term_rows"])
    orbit_terms = np.asarray(tuple(
        base["orbit_term_rows"][target] for target in targets),
        dtype=np.complex128)
    orbit_count = orbit_terms.shape[1]
    if orbit_count < 1:
        raise AssertionError("sign cube requires at least one orbit")
    covariance = orbit_terms.conjugate().T @ orbit_terms
    real_covariance = covariance.real
    denominator = float(np.trace(real_covariance))
    if denominator <= 0:
        raise ValueError("sign cube requires a positive orbit diagonal")
    pattern_count = 1 << (orbit_count - 1)
    pattern_indices = np.arange(pattern_count, dtype=np.uint32)
    signs = np.ones((pattern_count, orbit_count), dtype=np.float64)
    for column in range(1, orbit_count):
        signs[:, column] = np.where(
            (pattern_indices >> (column - 1)) & 1, -1.0, 1.0)
    ratios = np.einsum(
        "bi,ij,bj->b", signs, real_covariance, signs,
        optimize=True) / denominator
    actual_ratio = float(ratios[0])
    rank_tolerance = tolerance * max(1.0, abs(actual_ratio))
    at_or_above_actual = int(np.count_nonzero(
        ratios >= actual_ratio - rank_tolerance))
    actual_upper_tail_fraction = at_or_above_actual / pattern_count
    maximum_index = int(np.argmax(ratios))
    minimum_index = int(np.argmin(ratios))
    direct_denominator = math.fsum(
        base["rows"][target]["orbit_discrepancy_square_function"]
        for target in targets)
    dyadic_sign_cube_summaries = {}
    for block, block_row in base["dyadic_block_summaries"].items():
        block_lower, block_upper = block
        block_indices = tuple(
            index for index, target in enumerate(targets)
            if block_lower <= target < block_upper)
        block_terms = orbit_terms[np.asarray(block_indices, dtype=np.int64)]
        block_covariance = block_terms.conjugate().T @ block_terms
        block_real_covariance = block_covariance.real
        block_denominator = float(np.trace(block_real_covariance))
        block_ratios = np.einsum(
            "bi,ij,bj->b", signs, block_real_covariance, signs,
            optimize=True) / block_denominator
        block_actual_ratio = float(block_ratios[0])
        block_rank_tolerance = tolerance * max(
            1.0, abs(block_actual_ratio))
        block_at_or_above = int(np.count_nonzero(
            block_ratios >= block_actual_ratio - block_rank_tolerance))
        block_upper_tail_fraction = block_at_or_above / pattern_count
        block_maximum_index = int(np.argmax(block_ratios))
        dyadic_sign_cube_summaries[block] = {
            "target_count": len(block_indices),
            "pattern_count": pattern_count,
            "actual_ratio": block_actual_ratio,
            "base_actual_ratio": block_row["aggregate_orbit_ratio"],
            "actual_ratio_reconstruction_relative_error": abs(
                block_actual_ratio - block_row["aggregate_orbit_ratio"])
                / max(1.0, abs(block_row["aggregate_orbit_ratio"])),
            "patterns_at_or_above_actual": block_at_or_above,
            "actual_upper_tail_fraction": block_upper_tail_fraction,
            "passes_upper_tail_gate": bool(
                block_upper_tail_fraction
                <= maximum_actual_upper_tail_fraction),
            "maximum_ratio": float(block_ratios[block_maximum_index]),
            "maximum_sign_pattern": tuple(
                int(value) for value in signs[block_maximum_index]),
        }
    if minimum_stable_dyadic_block_count > len(dyadic_sign_cube_summaries):
        raise ValueError(
            "minimum stable dyadic block count exceeds measured blocks")
    stable_dyadic_block_count = sum(
        row["passes_upper_tail_gate"]
        for row in dyadic_sign_cube_summaries.values())
    return {
        "families": base["families"],
        "arithmetic_period": base["arithmetic_period"],
        "quotient": base["quotient"],
        "common_modulus": base["common_modulus"],
        "target_range": base["target_range"],
        "target_residue": base["target_residue"],
        "progression_step": base["progression_step"],
        "reflection_orbits": base["reflection_orbits"],
        "orbit_count": orbit_count,
        "global_sign_fixed_orbit": base["reflection_orbits"][0],
        "pattern_count": pattern_count,
        "maximum_actual_upper_tail_fraction_gate": (
            maximum_actual_upper_tail_fraction),
        "minimum_stable_dyadic_block_count_gate": (
            minimum_stable_dyadic_block_count),
        "actual_ratio": actual_ratio,
        "base_actual_ratio": base["aggregate_orbit_ratio"],
        "actual_ratio_reconstruction_relative_error": abs(
            actual_ratio - base["aggregate_orbit_ratio"])
            / max(1.0, abs(base["aggregate_orbit_ratio"])),
        "patterns_at_or_above_actual": at_or_above_actual,
        "actual_upper_tail_fraction": actual_upper_tail_fraction,
        "actual_signs_are_in_frozen_upper_tail": bool(
            actual_upper_tail_fraction
            <= maximum_actual_upper_tail_fraction),
        "minimum_ratio": float(ratios[minimum_index]),
        "minimum_sign_pattern": tuple(
            int(value) for value in signs[minimum_index]),
        "median_ratio": float(np.median(ratios)),
        "maximum_ratio": float(ratios[maximum_index]),
        "maximum_sign_pattern": tuple(
            int(value) for value in signs[maximum_index]),
        "orbit_diagonal": denominator,
        "orbit_diagonal_reconstruction_relative_error": abs(
            denominator - direct_denominator) / max(1.0, direct_denominator),
        "dyadic_sign_cube_summaries": dyadic_sign_cube_summaries,
        "stable_dyadic_block_count": stable_dyadic_block_count,
        "passes_dyadic_stability_gate": bool(
            stable_dyadic_block_count
            >= minimum_stable_dyadic_block_count),
        "finite_sign_cube_exhausted": True,
        "finite_dyadic_sign_cubes_exhausted": True,
        "source_sign_alignment_proved": False,
        "scale_stable_source_sign_alignment_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def residue_orbit_covariance_mode_receipt(
        target_minimum=1000, target_maximum=100000, target_residue=72,
        minimum_positive_spectral_concentration=.5,
        minimum_squared_mode_overlap=.5,
        minimum_stable_dyadic_block_count=5,
        tolerance=1e-12, batch_size=32):
    if (not math.isfinite(minimum_positive_spectral_concentration)
            or not 0 <= minimum_positive_spectral_concentration <= 1):
        raise ValueError("spectral concentration gate must lie in [0, 1]")
    if (not math.isfinite(minimum_squared_mode_overlap)
            or not 0 <= minimum_squared_mode_overlap <= 1):
        raise ValueError("squared mode overlap gate must lie in [0, 1]")
    if (type(minimum_stable_dyadic_block_count) is not int
            or minimum_stable_dyadic_block_count < 0):
        raise ValueError(
            "minimum stable dyadic block count must be a nonnegative integer")
    base = residue_orbit_reinforcement_receipt(
        target_minimum=target_minimum,
        target_maximum=target_maximum,
        target_residue=target_residue,
        tolerance=tolerance,
        batch_size=batch_size)
    targets = tuple(base["orbit_term_rows"])
    orbit_terms = np.asarray(tuple(
        base["orbit_term_rows"][target] for target in targets),
        dtype=np.complex128)

    def mode_summary(term_matrix):
        covariance = (term_matrix.conjugate().T @ term_matrix).real
        off_diagonal_covariance = covariance.copy()
        np.fill_diagonal(off_diagonal_covariance, 0.0)
        eigenvalues, eigenvectors = np.linalg.eigh(off_diagonal_covariance)
        leading_eigenvalue = float(eigenvalues[-1])
        second_eigenvalue = float(eigenvalues[-2])
        positive_threshold = tolerance * max(
            1.0, float(np.max(np.abs(eigenvalues))))
        positive_eigenvalues = eigenvalues[eigenvalues > positive_threshold]
        positive_spectral_mass = float(np.sum(positive_eigenvalues))
        if positive_spectral_mass <= 0:
            raise ValueError("off-diagonal covariance has no positive spectrum")
        return {
            "eigenvalues": tuple(float(value) for value in eigenvalues),
            "leading_eigenvector": eigenvectors[:, -1],
            "leading_eigenvalue": leading_eigenvalue,
            "second_eigenvalue": second_eigenvalue,
            "positive_eigenvalue_count": len(positive_eigenvalues),
            "positive_spectral_mass": positive_spectral_mass,
            "positive_spectral_concentration": (
                leading_eigenvalue / positive_spectral_mass),
            "relative_leading_eigengap": (
                (leading_eigenvalue - second_eigenvalue)
                / max(1.0, abs(leading_eigenvalue))),
            "off_diagonal_trace_error": abs(
                float(np.trace(off_diagonal_covariance))),
        }

    full = mode_summary(orbit_terms)
    full_vector = full["leading_eigenvector"]
    dyadic_mode_summaries = {}
    for block in base["dyadic_block_summaries"]:
        block_lower, block_upper = block
        block_indices = tuple(
            index for index, target in enumerate(targets)
            if block_lower <= target < block_upper)
        block_summary = mode_summary(
            orbit_terms[np.asarray(block_indices, dtype=np.int64)])
        block_vector = block_summary.pop("leading_eigenvector")
        squared_overlap = float(abs(np.dot(block_vector, full_vector)) ** 2)
        block_summary.update({
            "target_count": len(block_indices),
            "squared_overlap_with_full_mode": squared_overlap,
            "passes_mode_overlap_gate": bool(
                squared_overlap >= minimum_squared_mode_overlap),
            "leading_eigenvector": tuple(
                float(value) for value in block_vector),
        })
        dyadic_mode_summaries[block] = block_summary
    if minimum_stable_dyadic_block_count > len(dyadic_mode_summaries):
        raise ValueError(
            "minimum stable dyadic block count exceeds measured blocks")
    stable_dyadic_block_count = sum(
        row["passes_mode_overlap_gate"]
        for row in dyadic_mode_summaries.values())
    full_concentration_passes = bool(
        full["positive_spectral_concentration"]
        >= minimum_positive_spectral_concentration)
    overlap_count_passes = bool(
        stable_dyadic_block_count >= minimum_stable_dyadic_block_count)
    return {
        "families": base["families"],
        "arithmetic_period": base["arithmetic_period"],
        "quotient": base["quotient"],
        "common_modulus": base["common_modulus"],
        "target_range": base["target_range"],
        "target_residue": base["target_residue"],
        "progression_step": base["progression_step"],
        "reflection_orbits": base["reflection_orbits"],
        "orbit_count": len(base["reflection_orbits"]),
        "minimum_positive_spectral_concentration_gate": (
            minimum_positive_spectral_concentration),
        "minimum_squared_mode_overlap_gate": minimum_squared_mode_overlap,
        "minimum_stable_dyadic_block_count_gate": (
            minimum_stable_dyadic_block_count),
        "full_eigenvalues": full["eigenvalues"],
        "full_leading_eigenvector": tuple(
            float(value) for value in full_vector),
        "full_leading_eigenvalue": full["leading_eigenvalue"],
        "full_second_eigenvalue": full["second_eigenvalue"],
        "full_positive_eigenvalue_count": full[
            "positive_eigenvalue_count"],
        "full_positive_spectral_mass": full["positive_spectral_mass"],
        "full_positive_spectral_concentration": full[
            "positive_spectral_concentration"],
        "full_relative_leading_eigengap": full[
            "relative_leading_eigengap"],
        "full_off_diagonal_trace_error": full[
            "off_diagonal_trace_error"],
        "full_positive_spectral_concentration_passes_gate": (
            full_concentration_passes),
        "dyadic_mode_summaries": dyadic_mode_summaries,
        "stable_dyadic_block_count": stable_dyadic_block_count,
        "dyadic_mode_overlap_count_passes_gate": overlap_count_passes,
        "stable_rank_one_covariance_gate_passes": bool(
            full_concentration_passes and overlap_count_passes),
        "finite_covariance_modes_measured": True,
        "stable_rank_one_covariance_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def residue_orbit_covariance_subspace_receipt(
        target_minimum=1000, target_maximum=100000, target_residue=72,
        subspace_dimension=3,
        minimum_positive_spectral_concentration=.75,
        minimum_normalized_projector_overlap=.75,
        minimum_stable_dyadic_block_count=5,
        tolerance=1e-12, batch_size=32):
    if type(subspace_dimension) is not int or subspace_dimension < 1:
        raise ValueError("subspace dimension must be a positive integer")
    if (not math.isfinite(minimum_positive_spectral_concentration)
            or not 0 <= minimum_positive_spectral_concentration <= 1):
        raise ValueError("spectral concentration gate must lie in [0, 1]")
    if (not math.isfinite(minimum_normalized_projector_overlap)
            or not 0 <= minimum_normalized_projector_overlap <= 1):
        raise ValueError("projector overlap gate must lie in [0, 1]")
    if (type(minimum_stable_dyadic_block_count) is not int
            or minimum_stable_dyadic_block_count < 0):
        raise ValueError(
            "minimum stable dyadic block count must be a nonnegative integer")
    base = residue_orbit_reinforcement_receipt(
        target_minimum=target_minimum,
        target_maximum=target_maximum,
        target_residue=target_residue,
        tolerance=tolerance,
        batch_size=batch_size)
    targets = tuple(base["orbit_term_rows"])
    orbit_terms = np.asarray(tuple(
        base["orbit_term_rows"][target] for target in targets),
        dtype=np.complex128)
    orbit_count = orbit_terms.shape[1]
    if subspace_dimension >= orbit_count:
        raise ValueError(
            "subspace dimension must be smaller than the orbit count")

    def subspace_summary(term_matrix):
        covariance = (term_matrix.conjugate().T @ term_matrix).real
        off_diagonal_covariance = covariance.copy()
        np.fill_diagonal(off_diagonal_covariance, 0.0)
        eigenvalues, eigenvectors = np.linalg.eigh(off_diagonal_covariance)
        positive_threshold = tolerance * max(
            1.0, float(np.max(np.abs(eigenvalues))))
        positive_eigenvalues = eigenvalues[eigenvalues > positive_threshold]
        positive_spectral_mass = float(np.sum(positive_eigenvalues))
        if len(positive_eigenvalues) < subspace_dimension:
            raise ValueError(
                "off-diagonal covariance has fewer positive eigenvalues "
                "than the requested subspace dimension")
        top_eigenvalues = eigenvalues[-subspace_dimension:]
        cutoff_eigenvalue = float(eigenvalues[-subspace_dimension - 1])
        lowest_selected_eigenvalue = float(top_eigenvalues[0])
        absolute_cutoff_eigengap = (
            lowest_selected_eigenvalue - cutoff_eigenvalue)
        return {
            "eigenvalues": tuple(float(value) for value in eigenvalues),
            "basis": eigenvectors[:, -subspace_dimension:],
            "positive_eigenvalue_count": len(positive_eigenvalues),
            "positive_spectral_mass": positive_spectral_mass,
            "top_subspace_positive_spectral_concentration": float(
                np.sum(top_eigenvalues) / positive_spectral_mass),
            "lowest_selected_eigenvalue": lowest_selected_eigenvalue,
            "cutoff_eigenvalue": cutoff_eigenvalue,
            "absolute_cutoff_eigengap": absolute_cutoff_eigengap,
            "relative_cutoff_eigengap": (
                absolute_cutoff_eigengap
                / max(1.0, abs(lowest_selected_eigenvalue))),
            "off_diagonal_trace_error": abs(
                float(np.trace(off_diagonal_covariance))),
        }

    full = subspace_summary(orbit_terms)
    full_basis = full.pop("basis")
    dyadic_subspace_summaries = {}
    for block in base["dyadic_block_summaries"]:
        block_lower, block_upper = block
        block_indices = tuple(
            index for index, target in enumerate(targets)
            if block_lower <= target < block_upper)
        block_summary = subspace_summary(
            orbit_terms[np.asarray(block_indices, dtype=np.int64)])
        block_basis = block_summary.pop("basis")
        normalized_projector_overlap = float(
            np.linalg.norm(block_basis.T @ full_basis, ord="fro") ** 2
            / subspace_dimension)
        block_summary.update({
            "target_count": len(block_indices),
            "normalized_projector_overlap_with_full_subspace": (
                normalized_projector_overlap),
            "passes_projector_overlap_gate": bool(
                normalized_projector_overlap
                >= minimum_normalized_projector_overlap),
            "subspace_basis": tuple(
                tuple(float(value) for value in column)
                for column in block_basis.T),
        })
        dyadic_subspace_summaries[block] = block_summary
    if minimum_stable_dyadic_block_count > len(dyadic_subspace_summaries):
        raise ValueError(
            "minimum stable dyadic block count exceeds measured blocks")
    stable_dyadic_block_count = sum(
        row["passes_projector_overlap_gate"]
        for row in dyadic_subspace_summaries.values())
    full_concentration_passes = bool(
        full["top_subspace_positive_spectral_concentration"]
        >= minimum_positive_spectral_concentration)
    overlap_count_passes = bool(
        stable_dyadic_block_count >= minimum_stable_dyadic_block_count)
    return {
        "families": base["families"],
        "arithmetic_period": base["arithmetic_period"],
        "quotient": base["quotient"],
        "common_modulus": base["common_modulus"],
        "target_range": base["target_range"],
        "target_residue": base["target_residue"],
        "progression_step": base["progression_step"],
        "reflection_orbits": base["reflection_orbits"],
        "orbit_count": orbit_count,
        "subspace_dimension": subspace_dimension,
        "minimum_positive_spectral_concentration_gate": (
            minimum_positive_spectral_concentration),
        "minimum_normalized_projector_overlap_gate": (
            minimum_normalized_projector_overlap),
        "minimum_stable_dyadic_block_count_gate": (
            minimum_stable_dyadic_block_count),
        "full_eigenvalues": full["eigenvalues"],
        "full_subspace_basis": tuple(
            tuple(float(value) for value in column)
            for column in full_basis.T),
        "full_positive_eigenvalue_count": full[
            "positive_eigenvalue_count"],
        "full_positive_spectral_mass": full["positive_spectral_mass"],
        "full_top_subspace_positive_spectral_concentration": full[
            "top_subspace_positive_spectral_concentration"],
        "full_lowest_selected_eigenvalue": full[
            "lowest_selected_eigenvalue"],
        "full_cutoff_eigenvalue": full["cutoff_eigenvalue"],
        "full_absolute_cutoff_eigengap": full[
            "absolute_cutoff_eigengap"],
        "full_relative_cutoff_eigengap": full[
            "relative_cutoff_eigengap"],
        "full_off_diagonal_trace_error": full[
            "off_diagonal_trace_error"],
        "full_positive_spectral_concentration_passes_gate": (
            full_concentration_passes),
        "dyadic_subspace_summaries": dyadic_subspace_summaries,
        "stable_dyadic_block_count": stable_dyadic_block_count,
        "dyadic_projector_overlap_count_passes_gate": overlap_count_passes,
        "stable_covariance_subspace_gate_passes": bool(
            full_concentration_passes and overlap_count_passes),
        "finite_covariance_subspaces_measured": True,
        "stable_covariance_subspace_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def residue_orbit_adjacent_covariance_subspace_receipt(
        target_minimum=1000, target_maximum=100000, target_residue=72,
        subspace_dimension=4,
        minimum_normalized_projector_overlap=.75,
        minimum_stable_adjacent_pair_count=4,
        tolerance=1e-12, batch_size=32):
    if type(subspace_dimension) is not int or subspace_dimension < 1:
        raise ValueError("subspace dimension must be a positive integer")
    if (not math.isfinite(minimum_normalized_projector_overlap)
            or not 0 <= minimum_normalized_projector_overlap <= 1):
        raise ValueError("projector overlap gate must lie in [0, 1]")
    if (type(minimum_stable_adjacent_pair_count) is not int
            or minimum_stable_adjacent_pair_count < 0):
        raise ValueError(
            "minimum stable adjacent pair count must be a nonnegative integer")
    base = residue_orbit_covariance_subspace_receipt(
        target_minimum=target_minimum,
        target_maximum=target_maximum,
        target_residue=target_residue,
        subspace_dimension=subspace_dimension,
        minimum_positive_spectral_concentration=0,
        minimum_normalized_projector_overlap=0,
        minimum_stable_dyadic_block_count=0,
        tolerance=tolerance,
        batch_size=batch_size)
    blocks = tuple(base["dyadic_subspace_summaries"])
    if minimum_stable_adjacent_pair_count > len(blocks) - 1:
        raise ValueError(
            "minimum stable adjacent pair count exceeds measured pairs")
    bases = tuple(
        np.asarray(base["dyadic_subspace_summaries"][block][
            "subspace_basis"], dtype=np.float64).T
        for block in blocks)
    identity = np.eye(subspace_dimension)
    maximum_basis_orthonormality_error = max(
        float(np.linalg.norm(basis.T @ basis - identity, ord=2))
        for basis in bases)
    adjacent_pair_summaries = {}
    for index in range(len(blocks) - 1):
        left_block = blocks[index]
        right_block = blocks[index + 1]
        cross_basis = bases[index].T @ bases[index + 1]
        singular_values = np.linalg.svd(cross_basis, compute_uv=False)
        squared_canonical_correlations = singular_values ** 2
        normalized_projector_overlap = float(
            np.sum(squared_canonical_correlations) / subspace_dimension)
        adjacent_pair_summaries[(left_block, right_block)] = {
            "normalized_projector_overlap": normalized_projector_overlap,
            "squared_canonical_correlations": tuple(
                float(value) for value in squared_canonical_correlations),
            "minimum_squared_canonical_correlation": float(
                squared_canonical_correlations[-1]),
            "maximum_squared_canonical_correlation": float(
                squared_canonical_correlations[0]),
            "passes_projector_overlap_gate": bool(
                normalized_projector_overlap
                >= minimum_normalized_projector_overlap),
        }
    stable_adjacent_pair_count = sum(
        row["passes_projector_overlap_gate"]
        for row in adjacent_pair_summaries.values())
    return {
        "families": base["families"],
        "arithmetic_period": base["arithmetic_period"],
        "quotient": base["quotient"],
        "common_modulus": base["common_modulus"],
        "target_range": base["target_range"],
        "target_residue": base["target_residue"],
        "progression_step": base["progression_step"],
        "reflection_orbits": base["reflection_orbits"],
        "orbit_count": base["orbit_count"],
        "subspace_dimension": subspace_dimension,
        "dyadic_blocks": blocks,
        "minimum_normalized_projector_overlap_gate": (
            minimum_normalized_projector_overlap),
        "minimum_stable_adjacent_pair_count_gate": (
            minimum_stable_adjacent_pair_count),
        "adjacent_pair_summaries": adjacent_pair_summaries,
        "stable_adjacent_pair_count": stable_adjacent_pair_count,
        "local_covariance_subspace_coherence_gate_passes": bool(
            stable_adjacent_pair_count
            >= minimum_stable_adjacent_pair_count),
        "maximum_basis_orthonormality_error": (
            maximum_basis_orthonormality_error),
        "finite_adjacent_covariance_subspaces_measured": True,
        "local_covariance_subspace_coherence_proved": False,
        "asymptotic_covariance_subspace_stabilization_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def residue_orbit_prime_weight_covariance_receipt(
        target_minimum=1000, target_maximum=100000, target_residue=72,
        subspace_dimension=4,
        minimum_normalized_projector_overlap=.75,
        minimum_stable_adjacent_pair_count=4,
        tolerance=1e-12, batch_size=32):
    if type(subspace_dimension) is not int or subspace_dimension < 1:
        raise ValueError("subspace dimension must be a positive integer")
    if (not math.isfinite(minimum_normalized_projector_overlap)
            or not 0 <= minimum_normalized_projector_overlap <= 1):
        raise ValueError("projector overlap gate must lie in [0, 1]")
    if (type(minimum_stable_adjacent_pair_count) is not int
            or minimum_stable_adjacent_pair_count < 0):
        raise ValueError(
            "minimum stable adjacent pair count must be a nonnegative integer")
    base = residue_orbit_reinforcement_receipt(
        target_minimum=target_minimum,
        target_maximum=target_maximum,
        target_residue=target_residue,
        tolerance=tolerance,
        batch_size=batch_size)
    targets = tuple(base["orbit_term_rows"])
    discrepancy_rows = np.asarray(tuple(
        base["orbit_weight_discrepancy_rows"][target]
        for target in targets), dtype=np.float64)
    orbit_count = discrepancy_rows.shape[1]
    if subspace_dimension >= orbit_count:
        raise ValueError(
            "subspace dimension must be smaller than the orbit count")
    coefficients = np.asarray(base["orbit_coefficients"], dtype=np.complex128)
    reconstructed_terms = discrepancy_rows * coefficients[np.newaxis, :]
    measured_terms = np.asarray(tuple(
        base["orbit_term_rows"][target] for target in targets),
        dtype=np.complex128)
    factorization_scale = max(1.0, float(np.max(np.abs(measured_terms))))
    factorization_relative_error = float(
        np.max(np.abs(reconstructed_terms - measured_terms))
        / factorization_scale)

    def subspace_summary(row_matrix):
        covariance = row_matrix.T @ row_matrix
        off_diagonal_covariance = covariance.copy()
        np.fill_diagonal(off_diagonal_covariance, 0.0)
        eigenvalues, eigenvectors = np.linalg.eigh(off_diagonal_covariance)
        positive_threshold = tolerance * max(
            1.0, float(np.max(np.abs(eigenvalues))))
        positive_eigenvalues = eigenvalues[eigenvalues > positive_threshold]
        positive_spectral_mass = float(np.sum(positive_eigenvalues))
        if len(positive_eigenvalues) < subspace_dimension:
            raise ValueError(
                "prime-weight covariance has fewer positive eigenvalues "
                "than the requested subspace dimension")
        return {
            "eigenvalues": tuple(float(value) for value in eigenvalues),
            "basis": eigenvectors[:, -subspace_dimension:],
            "positive_eigenvalue_count": len(positive_eigenvalues),
            "top_subspace_positive_spectral_concentration": float(
                np.sum(eigenvalues[-subspace_dimension:])
                / positive_spectral_mass),
        }

    blocks = tuple(base["dyadic_block_summaries"])
    if minimum_stable_adjacent_pair_count > len(blocks) - 1:
        raise ValueError(
            "minimum stable adjacent pair count exceeds measured pairs")
    block_summaries = {}
    bases = []
    for block in blocks:
        block_lower, block_upper = block
        block_indices = np.asarray(tuple(
            index for index, target in enumerate(targets)
            if block_lower <= target < block_upper), dtype=np.int64)
        summary = subspace_summary(discrepancy_rows[block_indices])
        basis = summary.pop("basis")
        summary.update({
            "target_count": len(block_indices),
            "subspace_basis": tuple(
                tuple(float(value) for value in column)
                for column in basis.T),
        })
        block_summaries[block] = summary
        bases.append(basis)
    adjacent_pair_summaries = {}
    for index in range(len(blocks) - 1):
        cross_basis = bases[index].T @ bases[index + 1]
        squared_canonical_correlations = (
            np.linalg.svd(cross_basis, compute_uv=False) ** 2)
        normalized_projector_overlap = float(
            np.sum(squared_canonical_correlations) / subspace_dimension)
        adjacent_pair_summaries[(blocks[index], blocks[index + 1])] = {
            "normalized_projector_overlap": normalized_projector_overlap,
            "squared_canonical_correlations": tuple(
                float(value) for value in squared_canonical_correlations),
            "passes_projector_overlap_gate": bool(
                normalized_projector_overlap
                >= minimum_normalized_projector_overlap),
        }
    stable_adjacent_pair_count = sum(
        row["passes_projector_overlap_gate"]
        for row in adjacent_pair_summaries.values())
    return {
        "families": base["families"],
        "arithmetic_period": base["arithmetic_period"],
        "quotient": base["quotient"],
        "common_modulus": base["common_modulus"],
        "target_range": base["target_range"],
        "target_residue": base["target_residue"],
        "progression_step": base["progression_step"],
        "reflection_orbits": base["reflection_orbits"],
        "orbit_count": orbit_count,
        "subspace_dimension": subspace_dimension,
        "tested_target_count": len(targets),
        "orbit_term_factorization_relative_error": (
            factorization_relative_error),
        "orbit_term_factorization_passes": bool(
            factorization_relative_error <= tolerance),
        "dyadic_block_summaries": block_summaries,
        "minimum_normalized_projector_overlap_gate": (
            minimum_normalized_projector_overlap),
        "minimum_stable_adjacent_pair_count_gate": (
            minimum_stable_adjacent_pair_count),
        "adjacent_pair_summaries": adjacent_pair_summaries,
        "stable_adjacent_pair_count": stable_adjacent_pair_count,
        "prime_weight_local_subspace_gate_passes": bool(
            stable_adjacent_pair_count
            >= minimum_stable_adjacent_pair_count),
        "finite_prime_weight_covariances_measured": True,
        "prime_weight_covariance_stabilization_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def residue_orbit_conservation_covariance_receipt(
        target_minimum=1000, target_maximum=100000, target_residue=72,
        maximum_unexplained_frobenius_ratio=.5,
        minimum_explained_dyadic_block_count=5,
        tolerance=1e-12, batch_size=32):
    if (not math.isfinite(maximum_unexplained_frobenius_ratio)
            or not 0 <= maximum_unexplained_frobenius_ratio <= 1):
        raise ValueError("unexplained Frobenius ratio gate must lie in [0, 1]")
    if (type(minimum_explained_dyadic_block_count) is not int
            or minimum_explained_dyadic_block_count < 0):
        raise ValueError(
            "minimum explained dyadic block count must be nonnegative")
    base = residue_orbit_reinforcement_receipt(
        target_minimum=target_minimum,
        target_maximum=target_maximum,
        target_residue=target_residue,
        tolerance=tolerance,
        batch_size=batch_size)
    targets = tuple(base["orbit_weight_discrepancy_rows"])
    discrepancies = np.asarray(tuple(
        base["orbit_weight_discrepancy_rows"][target]
        for target in targets), dtype=np.float64)
    orbit_sizes = np.asarray(tuple(
        len(orbit) for orbit in base["reflection_orbits"]),
        dtype=np.float64)
    conservation_values = discrepancies @ orbit_sizes
    row_scales = np.maximum(
        1.0, np.sum(np.abs(discrepancies * orbit_sizes), axis=1))
    maximum_conservation_relative_error = float(
        np.max(np.abs(conservation_values) / row_scales))

    orbit_count = discrepancies.shape[1]
    pairs = tuple(
        (left, right)
        for left in range(orbit_count)
        for right in range(left + 1, orbit_count))
    constraint_matrix = np.zeros((orbit_count, len(pairs)), dtype=np.float64)
    for column, (left, right) in enumerate(pairs):
        constraint_matrix[left, column] = orbit_sizes[right]
        constraint_matrix[right, column] = orbit_sizes[left]
    constraint_rank = int(np.linalg.matrix_rank(constraint_matrix))
    if constraint_rank != orbit_count:
        raise ValueError("off-diagonal conservation constraint is rank deficient")

    dyadic_conservation_summaries = {}
    for block in base["dyadic_block_summaries"]:
        block_lower, block_upper = block
        block_indices = np.asarray(tuple(
            index for index, target in enumerate(targets)
            if block_lower <= target < block_upper), dtype=np.int64)
        block_rows = discrepancies[block_indices]
        covariance = block_rows.T @ block_rows
        diagonal = np.diag(covariance).copy()
        off_diagonal_covariance = covariance.copy()
        np.fill_diagonal(off_diagonal_covariance, 0.0)
        required_action = -(diagonal * orbit_sizes)
        minimum_norm_entries = np.linalg.lstsq(
            constraint_matrix, required_action, rcond=None)[0]
        forced_covariance = np.zeros_like(off_diagonal_covariance)
        for value, (left, right) in zip(minimum_norm_entries, pairs):
            forced_covariance[left, right] = value
            forced_covariance[right, left] = value
        unexplained_covariance = off_diagonal_covariance - forced_covariance
        off_diagonal_norm = float(
            np.linalg.norm(off_diagonal_covariance, ord="fro"))
        if off_diagonal_norm <= 0:
            raise ValueError("off-diagonal covariance has zero Frobenius norm")
        unexplained_norm = float(
            np.linalg.norm(unexplained_covariance, ord="fro"))
        forced_norm = float(np.linalg.norm(forced_covariance, ord="fro"))
        required_scale = max(1.0, float(np.linalg.norm(required_action)))
        decomposition_scale = max(1.0, off_diagonal_norm ** 2)
        unexplained_ratio = unexplained_norm / off_diagonal_norm
        dyadic_conservation_summaries[block] = {
            "target_count": len(block_indices),
            "empirical_covariance_conservation_relative_error": float(
                np.linalg.norm(covariance @ orbit_sizes) / required_scale),
            "forced_constraint_relative_error": float(
                np.linalg.norm(
                    forced_covariance @ orbit_sizes - required_action)
                / required_scale),
            "forced_to_empirical_frobenius_inner_product": float(
                np.sum(forced_covariance * off_diagonal_covariance)),
            "forced_frobenius_norm": forced_norm,
            "unexplained_frobenius_norm": unexplained_norm,
            "off_diagonal_frobenius_norm": off_diagonal_norm,
            "unexplained_frobenius_ratio": unexplained_ratio,
            "forced_squared_frobenius_fraction": (
                forced_norm ** 2 / off_diagonal_norm ** 2),
            "pythagorean_relative_error": abs(
                forced_norm ** 2 + unexplained_norm ** 2
                - off_diagonal_norm ** 2) / decomposition_scale,
            "passes_conservation_explanation_gate": bool(
                unexplained_ratio
                <= maximum_unexplained_frobenius_ratio),
        }
    if minimum_explained_dyadic_block_count > len(
            dyadic_conservation_summaries):
        raise ValueError(
            "minimum explained dyadic block count exceeds measured blocks")
    explained_dyadic_block_count = sum(
        row["passes_conservation_explanation_gate"]
        for row in dyadic_conservation_summaries.values())
    return {
        "families": base["families"],
        "arithmetic_period": base["arithmetic_period"],
        "quotient": base["quotient"],
        "common_modulus": base["common_modulus"],
        "target_range": base["target_range"],
        "target_residue": base["target_residue"],
        "progression_step": base["progression_step"],
        "reflection_orbits": base["reflection_orbits"],
        "orbit_sizes": tuple(int(value) for value in orbit_sizes),
        "orbit_count": orbit_count,
        "tested_target_count": len(targets),
        "off_diagonal_constraint_rank": constraint_rank,
        "maximum_conservation_relative_error": (
            maximum_conservation_relative_error),
        "maximum_unexplained_frobenius_ratio_gate": (
            maximum_unexplained_frobenius_ratio),
        "minimum_explained_dyadic_block_count_gate": (
            minimum_explained_dyadic_block_count),
        "dyadic_conservation_summaries": dyadic_conservation_summaries,
        "explained_dyadic_block_count": explained_dyadic_block_count,
        "conservation_covariance_mechanism_gate_passes": bool(
            explained_dyadic_block_count
            >= minimum_explained_dyadic_block_count),
        "finite_conservation_covariances_measured": True,
        "conservation_covariance_theorem_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def residue_orbit_crt_anova_receipt(
        target_minimum=1000, target_maximum=100000, target_residue=72,
        minimum_separable_energy_fraction=.75,
        minimum_separable_dyadic_block_count=5,
        tolerance=1e-12, batch_size=32):
    if (not math.isfinite(minimum_separable_energy_fraction)
            or not 0 <= minimum_separable_energy_fraction <= 1):
        raise ValueError("separable energy gate must lie in [0, 1]")
    if (type(minimum_separable_dyadic_block_count) is not int
            or minimum_separable_dyadic_block_count < 0):
        raise ValueError(
            "minimum separable dyadic block count must be nonnegative")
    base = residue_orbit_reinforcement_receipt(
        target_minimum=target_minimum,
        target_maximum=target_maximum,
        target_residue=target_residue,
        tolerance=tolerance,
        batch_size=batch_size)
    residue5_values = tuple(
        value for value in range(5)
        if value and (target_residue - value) % 5)
    residue13_values = tuple(
        value for value in range(13)
        if value and (target_residue - value) % 13)
    expected_cell_count = len(residue5_values) * len(residue13_values)
    if expected_cell_count != len(base["admissible_residues"]):
        raise AssertionError("admissible residues do not have CRT product size")
    residue5_index = {
        value: index for index, value in enumerate(residue5_values)}
    residue13_index = {
        value: index for index, value in enumerate(residue13_values)}
    crt_residues = {}
    for residue in base["admissible_residues"]:
        cell = (residue % 5, residue % 13)
        if cell in crt_residues:
            raise AssertionError("odd admissible CRT cell is not unique")
        if cell[0] not in residue5_index or cell[1] not in residue13_index:
            raise AssertionError("admissible residue lies outside CRT product")
        crt_residues[cell] = residue
    expected_cells = {
        (residue5, residue13)
        for residue5 in residue5_values
        for residue13 in residue13_values}
    if set(crt_residues) != expected_cells:
        raise AssertionError("admissible CRT product is incomplete")
    orbit_by_residue = {
        residue: orbit_index
        for orbit_index, orbit in enumerate(base["reflection_orbits"])
        for residue in orbit}

    targets = tuple(base["orbit_weight_discrepancy_rows"])
    target_energies = {}
    maximum_mean_relative_error = 0.0
    maximum_reconstruction_relative_error = 0.0
    maximum_energy_relative_error = 0.0
    maximum_orthogonality_relative_error = 0.0
    maximum_interaction_marginal_relative_error = 0.0
    maximum_reflection_symmetry_relative_error = 0.0
    interaction_tables = {}
    for target in targets:
        orbit_row = base["orbit_weight_discrepancy_rows"][target]
        table = np.empty(
            (len(residue5_values), len(residue13_values)),
            dtype=np.float64)
        for (residue5, residue13), residue in crt_residues.items():
            table[
                residue5_index[residue5],
                residue13_index[residue13]] = orbit_row[
                    orbit_by_residue[residue]]
        table_scale = max(1.0, float(np.sum(np.abs(table))))
        reflection_error = 0.0
        for row_index, residue5 in enumerate(residue5_values):
            partner5 = (target_residue - residue5) % 5
            for column_index, residue13 in enumerate(residue13_values):
                partner13 = (target_residue - residue13) % 13
                reflection_error = max(
                    reflection_error,
                    abs(table[row_index, column_index]
                        - table[residue5_index[partner5],
                                residue13_index[partner13]]))
        overall_mean = float(np.mean(table))
        row_component = (
            np.mean(table, axis=1, keepdims=True) - overall_mean)
        row_component = np.broadcast_to(row_component, table.shape)
        column_component = (
            np.mean(table, axis=0, keepdims=True) - overall_mean)
        column_component = np.broadcast_to(column_component, table.shape)
        interaction = table - overall_mean - row_component - column_component
        reconstruction = row_component + column_component + interaction
        total_energy = float(np.sum(table ** 2))
        if total_energy <= 0:
            raise ValueError("CRT discrepancy table has zero energy")
        row_energy = float(np.sum(row_component ** 2))
        column_energy = float(np.sum(column_component ** 2))
        interaction_energy = float(np.sum(interaction ** 2))
        energy_scale = max(1.0, total_energy)
        orthogonality_error = max(
            abs(float(np.sum(row_component * column_component))),
            abs(float(np.sum(row_component * interaction))),
            abs(float(np.sum(column_component * interaction))))
        interaction_marginal_error = max(
            float(np.max(np.abs(np.mean(interaction, axis=0)))),
            float(np.max(np.abs(np.mean(interaction, axis=1)))))
        target_energies[target] = {
            "total_energy": total_energy,
            "mod5_marginal_energy": row_energy,
            "mod13_marginal_energy": column_energy,
            "interaction_energy": interaction_energy,
        }
        interaction_tables[target] = tuple(
            tuple(float(value) for value in row) for row in interaction)
        maximum_mean_relative_error = max(
            maximum_mean_relative_error,
            abs(overall_mean) * table.size / table_scale)
        maximum_reconstruction_relative_error = max(
            maximum_reconstruction_relative_error,
            float(np.max(np.abs(table - reconstruction)))
            * table.size / table_scale)
        maximum_energy_relative_error = max(
            maximum_energy_relative_error,
            abs(row_energy + column_energy + interaction_energy
                - total_energy) / energy_scale)
        maximum_orthogonality_relative_error = max(
            maximum_orthogonality_relative_error,
            orthogonality_error / energy_scale)
        maximum_interaction_marginal_relative_error = max(
            maximum_interaction_marginal_relative_error,
            interaction_marginal_error * table.size / table_scale)
        maximum_reflection_symmetry_relative_error = max(
            maximum_reflection_symmetry_relative_error,
            reflection_error * table.size / table_scale)

    dyadic_crt_summaries = {}
    for block in base["dyadic_block_summaries"]:
        block_lower, block_upper = block
        block_targets = tuple(
            target for target in targets
            if block_lower <= target < block_upper)
        total_energy = math.fsum(
            target_energies[target]["total_energy"]
            for target in block_targets)
        mod5_energy = math.fsum(
            target_energies[target]["mod5_marginal_energy"]
            for target in block_targets)
        mod13_energy = math.fsum(
            target_energies[target]["mod13_marginal_energy"]
            for target in block_targets)
        interaction_energy = math.fsum(
            target_energies[target]["interaction_energy"]
            for target in block_targets)
        separable_fraction = (mod5_energy + mod13_energy) / total_energy
        dyadic_crt_summaries[block] = {
            "target_count": len(block_targets),
            "total_energy": total_energy,
            "mod5_marginal_energy_fraction": mod5_energy / total_energy,
            "mod13_marginal_energy_fraction": mod13_energy / total_energy,
            "separable_marginal_energy_fraction": separable_fraction,
            "interaction_energy_fraction": interaction_energy / total_energy,
            "passes_separable_energy_gate": bool(
                separable_fraction >= minimum_separable_energy_fraction),
        }
    if minimum_separable_dyadic_block_count > len(dyadic_crt_summaries):
        raise ValueError(
            "minimum separable dyadic block count exceeds measured blocks")
    separable_dyadic_block_count = sum(
        row["passes_separable_energy_gate"]
        for row in dyadic_crt_summaries.values())
    return {
        "families": base["families"],
        "arithmetic_period": base["arithmetic_period"],
        "quotient": base["quotient"],
        "common_modulus": base["common_modulus"],
        "target_range": base["target_range"],
        "target_residue": base["target_residue"],
        "progression_step": base["progression_step"],
        "reflection_orbits": base["reflection_orbits"],
        "residue5_values": residue5_values,
        "residue13_values": residue13_values,
        "crt_residue_cell_count": len(crt_residues),
        "tested_target_count": len(targets),
        "maximum_mean_relative_error": maximum_mean_relative_error,
        "maximum_reconstruction_relative_error": (
            maximum_reconstruction_relative_error),
        "maximum_energy_relative_error": maximum_energy_relative_error,
        "maximum_orthogonality_relative_error": (
            maximum_orthogonality_relative_error),
        "maximum_interaction_marginal_relative_error": (
            maximum_interaction_marginal_relative_error),
        "maximum_reflection_symmetry_relative_error": (
            maximum_reflection_symmetry_relative_error),
        "interaction_tables": interaction_tables,
        "minimum_separable_energy_fraction_gate": (
            minimum_separable_energy_fraction),
        "minimum_separable_dyadic_block_count_gate": (
            minimum_separable_dyadic_block_count),
        "dyadic_crt_summaries": dyadic_crt_summaries,
        "separable_dyadic_block_count": separable_dyadic_block_count,
        "crt_separable_marginal_mechanism_gate_passes": bool(
            separable_dyadic_block_count
            >= minimum_separable_dyadic_block_count),
        "finite_crt_anova_measured": True,
        "crt_separable_prime_discrepancy_theorem_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def residue_orbit_crt_parity_receipt(
        target_minimum=1000, target_maximum=100000, target_residue=72,
        minimum_odd_odd_energy_fraction=.75,
        minimum_odd_odd_dyadic_block_count=5,
        tolerance=1e-12, batch_size=32):
    if (not math.isfinite(minimum_odd_odd_energy_fraction)
            or not 0 <= minimum_odd_odd_energy_fraction <= 1):
        raise ValueError("odd-odd energy gate must lie in [0, 1]")
    if (type(minimum_odd_odd_dyadic_block_count) is not int
            or minimum_odd_odd_dyadic_block_count < 0):
        raise ValueError("minimum odd-odd dyadic block count must be nonnegative")
    base = residue_orbit_crt_anova_receipt(
        target_minimum=target_minimum,
        target_maximum=target_maximum,
        target_residue=target_residue,
        minimum_separable_energy_fraction=0,
        minimum_separable_dyadic_block_count=0,
        tolerance=tolerance,
        batch_size=batch_size)
    residue5_values = base["residue5_values"]
    residue13_values = base["residue13_values"]
    residue5_index = {
        value: index for index, value in enumerate(residue5_values)}
    residue13_index = {
        value: index for index, value in enumerate(residue13_values)}
    reflection5_indices = np.asarray(tuple(
        residue5_index[(target_residue - value) % 5]
        for value in residue5_values), dtype=np.int64)
    reflection13_indices = np.asarray(tuple(
        residue13_index[(target_residue - value) % 13]
        for value in residue13_values), dtype=np.int64)

    target_energies = {}
    maximum_global_reflection_relative_error = 0.0
    maximum_reconstruction_relative_error = 0.0
    maximum_energy_relative_error = 0.0
    maximum_orthogonality_relative_error = 0.0
    maximum_mixed_sector_energy_fraction = 0.0
    for target, values in base["interaction_tables"].items():
        interaction = np.asarray(values, dtype=np.float64)
        reflection5 = interaction[reflection5_indices, :]
        reflection13 = interaction[:, reflection13_indices]
        reflection_both = reflection5[:, reflection13_indices]
        even_even = (
            interaction + reflection5 + reflection13 + reflection_both) / 4
        even_odd = (
            interaction + reflection5 - reflection13 - reflection_both) / 4
        odd_even = (
            interaction - reflection5 + reflection13 - reflection_both) / 4
        odd_odd = (
            interaction - reflection5 - reflection13 + reflection_both) / 4
        reconstructed = even_even + even_odd + odd_even + odd_odd
        total_energy = float(np.sum(interaction ** 2))
        if total_energy <= 0:
            raise ValueError("CRT interaction has zero energy")
        even_even_energy = float(np.sum(even_even ** 2))
        even_odd_energy = float(np.sum(even_odd ** 2))
        odd_even_energy = float(np.sum(odd_even ** 2))
        odd_odd_energy = float(np.sum(odd_odd ** 2))
        energy_scale = max(1.0, total_energy)
        sectors = (even_even, even_odd, odd_even, odd_odd)
        orthogonality_error = max(
            abs(float(np.sum(sectors[left] * sectors[right])))
            for left in range(len(sectors))
            for right in range(left + 1, len(sectors)))
        target_energies[target] = {
            "total_interaction_energy": total_energy,
            "even_even_energy": even_even_energy,
            "even_odd_energy": even_odd_energy,
            "odd_even_energy": odd_even_energy,
            "odd_odd_energy": odd_odd_energy,
        }
        maximum_global_reflection_relative_error = max(
            maximum_global_reflection_relative_error,
            float(np.max(np.abs(interaction - reflection_both)))
            * interaction.size / max(1.0, float(np.sum(np.abs(interaction)))))
        maximum_reconstruction_relative_error = max(
            maximum_reconstruction_relative_error,
            float(np.max(np.abs(interaction - reconstructed)))
            * interaction.size / max(1.0, float(np.sum(np.abs(interaction)))))
        maximum_energy_relative_error = max(
            maximum_energy_relative_error,
            abs(even_even_energy + even_odd_energy + odd_even_energy
                + odd_odd_energy - total_energy) / energy_scale)
        maximum_orthogonality_relative_error = max(
            maximum_orthogonality_relative_error,
            orthogonality_error / energy_scale)
        maximum_mixed_sector_energy_fraction = max(
            maximum_mixed_sector_energy_fraction,
            (even_odd_energy + odd_even_energy) / total_energy)

    dyadic_parity_summaries = {}
    for block in base["dyadic_crt_summaries"]:
        block_lower, block_upper = block
        block_targets = tuple(
            target for target in target_energies
            if block_lower <= target < block_upper)
        total_energy = math.fsum(
            target_energies[target]["total_interaction_energy"]
            for target in block_targets)
        even_even_energy = math.fsum(
            target_energies[target]["even_even_energy"]
            for target in block_targets)
        even_odd_energy = math.fsum(
            target_energies[target]["even_odd_energy"]
            for target in block_targets)
        odd_even_energy = math.fsum(
            target_energies[target]["odd_even_energy"]
            for target in block_targets)
        odd_odd_energy = math.fsum(
            target_energies[target]["odd_odd_energy"]
            for target in block_targets)
        odd_odd_fraction = odd_odd_energy / total_energy
        dyadic_parity_summaries[block] = {
            "target_count": len(block_targets),
            "even_even_energy_fraction": even_even_energy / total_energy,
            "even_odd_energy_fraction": even_odd_energy / total_energy,
            "odd_even_energy_fraction": odd_even_energy / total_energy,
            "odd_odd_energy_fraction": odd_odd_fraction,
            "passes_odd_odd_energy_gate": bool(
                odd_odd_fraction >= minimum_odd_odd_energy_fraction),
        }
    if minimum_odd_odd_dyadic_block_count > len(dyadic_parity_summaries):
        raise ValueError(
            "minimum odd-odd dyadic block count exceeds measured blocks")
    odd_odd_dyadic_block_count = sum(
        row["passes_odd_odd_energy_gate"]
        for row in dyadic_parity_summaries.values())
    return {
        "families": base["families"],
        "arithmetic_period": base["arithmetic_period"],
        "quotient": base["quotient"],
        "common_modulus": base["common_modulus"],
        "target_range": base["target_range"],
        "target_residue": base["target_residue"],
        "progression_step": base["progression_step"],
        "residue5_values": residue5_values,
        "residue13_values": residue13_values,
        "reflection5_indices": tuple(
            int(value) for value in reflection5_indices),
        "reflection13_indices": tuple(
            int(value) for value in reflection13_indices),
        "tested_target_count": len(target_energies),
        "maximum_global_reflection_relative_error": (
            maximum_global_reflection_relative_error),
        "maximum_reconstruction_relative_error": (
            maximum_reconstruction_relative_error),
        "maximum_energy_relative_error": maximum_energy_relative_error,
        "maximum_orthogonality_relative_error": (
            maximum_orthogonality_relative_error),
        "maximum_mixed_sector_energy_fraction": (
            maximum_mixed_sector_energy_fraction),
        "minimum_odd_odd_energy_fraction_gate": (
            minimum_odd_odd_energy_fraction),
        "minimum_odd_odd_dyadic_block_count_gate": (
            minimum_odd_odd_dyadic_block_count),
        "dyadic_parity_summaries": dyadic_parity_summaries,
        "odd_odd_dyadic_block_count": odd_odd_dyadic_block_count,
        "odd_odd_interaction_mechanism_gate_passes": bool(
            odd_odd_dyadic_block_count
            >= minimum_odd_odd_dyadic_block_count),
        "finite_crt_parity_decomposition_measured": True,
        "odd_odd_prime_discrepancy_theorem_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def residue_orbit_crt_sector_correlation_receipt(
        target_minimum=1000, target_maximum=100000, target_residue=72,
        maximum_sector_square_function_ratio=1.0,
        minimum_cancelling_dyadic_block_count=5,
        tolerance=1e-12, batch_size=32):
    if (not math.isfinite(maximum_sector_square_function_ratio)
            or maximum_sector_square_function_ratio < 0):
        raise ValueError(
            "sector square-function ratio gate must be nonnegative")
    if (type(minimum_cancelling_dyadic_block_count) is not int
            or minimum_cancelling_dyadic_block_count < 0):
        raise ValueError(
            "minimum cancelling dyadic block count must be nonnegative")
    base = residue_orbit_reinforcement_receipt(
        target_minimum=target_minimum,
        target_maximum=target_maximum,
        target_residue=target_residue,
        tolerance=tolerance,
        batch_size=batch_size)
    residue5_values = tuple(
        value for value in range(5)
        if value and (target_residue - value) % 5)
    residue13_values = tuple(
        value for value in range(13)
        if value and (target_residue - value) % 13)
    residue5_index = {
        value: index for index, value in enumerate(residue5_values)}
    residue13_index = {
        value: index for index, value in enumerate(residue13_values)}
    reflection5_indices = np.asarray(tuple(
        residue5_index[(target_residue - value) % 5]
        for value in residue5_values), dtype=np.int64)
    reflection13_indices = np.asarray(tuple(
        residue13_index[(target_residue - value) % 13]
        for value in residue13_values), dtype=np.int64)
    orbit_by_residue = {
        residue: orbit_index
        for orbit_index, orbit in enumerate(base["reflection_orbits"])
        for residue in orbit}
    crt_residues = {
        (residue % 5, residue % 13): residue
        for residue in base["admissible_residues"]}
    if len(crt_residues) != len(residue5_values) * len(residue13_values):
        raise AssertionError("admissible CRT cells are incomplete")

    def lift_orbit_row(orbit_row, divide_by_orbit_size=False):
        table = np.empty(
            (len(residue5_values), len(residue13_values)),
            dtype=np.complex128 if divide_by_orbit_size else np.float64)
        for (residue5, residue13), residue in crt_residues.items():
            orbit_index = orbit_by_residue[residue]
            value = orbit_row[orbit_index]
            if divide_by_orbit_size:
                value /= len(base["reflection_orbits"][orbit_index])
            table[
                residue5_index[residue5],
                residue13_index[residue13]] = value
        return table

    def sector_components(table):
        overall_mean = np.mean(table)
        mod5_component = np.broadcast_to(
            np.mean(table, axis=1, keepdims=True) - overall_mean,
            table.shape)
        mod13_component = np.broadcast_to(
            np.mean(table, axis=0, keepdims=True) - overall_mean,
            table.shape)
        interaction = (
            table - overall_mean - mod5_component - mod13_component)
        reflection5 = interaction[reflection5_indices, :]
        reflection13 = interaction[:, reflection13_indices]
        reflection_both = reflection5[:, reflection13_indices]
        even_even = (
            interaction + reflection5 + reflection13 + reflection_both) / 4
        odd_odd = (
            interaction - reflection5 - reflection13 + reflection_both) / 4
        return {
            "mod5": mod5_component,
            "mod13": mod13_component,
            "even_even": even_even,
            "odd_odd": odd_odd,
        }

    source_table = lift_orbit_row(
        base["orbit_coefficients"], divide_by_orbit_size=True)
    source_components = sector_components(source_table)
    source_scale = max(1.0, float(np.sum(np.abs(source_table))))
    source_reconstructed = sum(
        source_components.values(), np.zeros_like(source_table))
    source_reconstruction_relative_error = float(
        np.max(np.abs(source_table - source_reconstructed))
        * source_table.size / source_scale)
    source_component_energy = {
        name: float(np.sum(np.abs(component) ** 2))
        for name, component in source_components.items()}
    source_energy = float(np.sum(np.abs(source_table) ** 2))
    source_energy_relative_error = abs(
        math.fsum(source_component_energy.values()) - source_energy
    ) / max(1.0, source_energy)

    component_names = ("mod5", "mod13", "even_even", "odd_odd")
    target_component_correlations = {}
    maximum_correlation_reconstruction_relative_error = 0.0
    for target, orbit_row in base["orbit_weight_discrepancy_rows"].items():
        discrepancy_table = lift_orbit_row(orbit_row)
        discrepancy_components = sector_components(discrepancy_table)
        correlations = {
            name: np.sum(
                discrepancy_components[name] * source_components[name])
            for name in component_names}
        reconstructed = sum(correlations.values(), 0.0j)
        measured = _complex_fsum(base["orbit_term_rows"][target])
        correlation_scale = max(
            1.0, abs(measured),
            math.fsum(abs(value) for value in correlations.values()))
        maximum_correlation_reconstruction_relative_error = max(
            maximum_correlation_reconstruction_relative_error,
            abs(reconstructed - measured) / correlation_scale)
        target_component_correlations[target] = {
            **correlations,
            "measured_total": measured,
            "reconstructed_total": reconstructed,
        }

    dyadic_sector_summaries = {}
    sector_pairs = tuple(
        (component_names[left], component_names[right])
        for left in range(len(component_names))
        for right in range(left + 1, len(component_names)))
    for block in base["dyadic_block_summaries"]:
        block_lower, block_upper = block
        block_targets = tuple(
            target for target in target_component_correlations
            if block_lower <= target < block_upper)
        total_squared_correlation = math.fsum(
            abs(target_component_correlations[target]["measured_total"]) ** 2
            for target in block_targets)
        component_squared_correlations = {
            name: math.fsum(
                abs(target_component_correlations[target][name]) ** 2
                for target in block_targets)
            for name in component_names}
        sector_square_function = math.fsum(
            component_squared_correlations.values())
        if sector_square_function <= 0:
            raise ValueError("CRT sector square function is zero")
        pairwise_cross_terms = {
            pair: 2 * math.fsum(
                (target_component_correlations[target][pair[0]]
                 * target_component_correlations[target][
                     pair[1]].conjugate()).real
                for target in block_targets)
            for pair in sector_pairs}
        net_cross_term = math.fsum(pairwise_cross_terms.values())
        reconstruction_scale = max(
            1.0, total_squared_correlation, sector_square_function,
            abs(net_cross_term))
        ratio = total_squared_correlation / sector_square_function
        dyadic_sector_summaries[block] = {
            "target_count": len(block_targets),
            "summed_squared_correlation": total_squared_correlation,
            "sector_square_function": sector_square_function,
            "sector_square_function_ratio": ratio,
            "component_squared_correlations": (
                component_squared_correlations),
            "pairwise_sector_cross_terms": pairwise_cross_terms,
            "net_sector_cross_term": net_cross_term,
            "cross_term_reconstruction_relative_error": abs(
                sector_square_function + net_cross_term
                - total_squared_correlation) / reconstruction_scale,
            "passes_sector_cancellation_gate": bool(
                ratio <= maximum_sector_square_function_ratio),
        }
    if minimum_cancelling_dyadic_block_count > len(dyadic_sector_summaries):
        raise ValueError(
            "minimum cancelling dyadic block count exceeds measured blocks")
    cancelling_dyadic_block_count = sum(
        row["passes_sector_cancellation_gate"]
        for row in dyadic_sector_summaries.values())
    return {
        "families": base["families"],
        "arithmetic_period": base["arithmetic_period"],
        "quotient": base["quotient"],
        "common_modulus": base["common_modulus"],
        "target_range": base["target_range"],
        "target_residue": base["target_residue"],
        "progression_step": base["progression_step"],
        "reflection_orbits": base["reflection_orbits"],
        "component_names": component_names,
        "tested_target_count": len(target_component_correlations),
        "source_reconstruction_relative_error": (
            source_reconstruction_relative_error),
        "source_energy_relative_error": source_energy_relative_error,
        "source_component_energy_fractions": {
            name: energy / source_energy
            for name, energy in source_component_energy.items()},
        "maximum_correlation_reconstruction_relative_error": (
            maximum_correlation_reconstruction_relative_error),
        "maximum_sector_square_function_ratio_gate": (
            maximum_sector_square_function_ratio),
        "minimum_cancelling_dyadic_block_count_gate": (
            minimum_cancelling_dyadic_block_count),
        "dyadic_sector_summaries": dyadic_sector_summaries,
        "cancelling_dyadic_block_count": cancelling_dyadic_block_count,
        "crt_sector_cancellation_gate_passes": bool(
            cancelling_dyadic_block_count
            >= minimum_cancelling_dyadic_block_count),
        "finite_crt_sector_correlations_measured": True,
        "crt_sector_cancellation_theorem_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def residue_orbit_even_even_profile_receipt(
        target_minimum=1000, target_maximum=100000, target_residue=72,
        maximum_profile_alignment=.75,
        tolerance=1e-12, batch_size=32):
    if (not math.isfinite(maximum_profile_alignment)
            or not 0 <= maximum_profile_alignment <= 1):
        raise ValueError("profile alignment gate must lie in [0, 1]")
    base = residue_orbit_reinforcement_receipt(
        target_minimum=target_minimum,
        target_maximum=target_maximum,
        target_residue=target_residue,
        tolerance=tolerance,
        batch_size=batch_size)
    residue5_values = tuple(
        value for value in range(5)
        if value and (target_residue - value) % 5)
    residue13_values = tuple(
        value for value in range(13)
        if value and (target_residue - value) % 13)
    if residue5_values != (1, 3, 4):
        raise ValueError("even-even profile expects A_5=(1,3,4)")
    residue5_index = {
        value: index for index, value in enumerate(residue5_values)}
    residue13_index = {
        value: index for index, value in enumerate(residue13_values)}
    reflection5_indices = np.asarray(tuple(
        residue5_index[(target_residue - value) % 5]
        for value in residue5_values), dtype=np.int64)
    reflection13_indices = np.asarray(tuple(
        residue13_index[(target_residue - value) % 13]
        for value in residue13_values), dtype=np.int64)
    orbit_by_residue = {
        residue: orbit_index
        for orbit_index, orbit in enumerate(base["reflection_orbits"])
        for residue in orbit}
    crt_residues = {
        (residue % 5, residue % 13): residue
        for residue in base["admissible_residues"]}
    if len(crt_residues) != len(residue5_values) * len(residue13_values):
        raise AssertionError("admissible CRT cells are incomplete")
    mod5_contrast = np.asarray((-2.0, 1.0, 1.0)) / math.sqrt(6.0)

    def lift_orbit_row(orbit_row, divide_by_orbit_size=False):
        table = np.empty(
            (len(residue5_values), len(residue13_values)),
            dtype=np.complex128 if divide_by_orbit_size else np.float64)
        for (residue5, residue13), residue in crt_residues.items():
            orbit_index = orbit_by_residue[residue]
            value = orbit_row[orbit_index]
            if divide_by_orbit_size:
                value /= len(base["reflection_orbits"][orbit_index])
            table[
                residue5_index[residue5],
                residue13_index[residue13]] = value
        return table

    def even_even_interaction(table):
        overall_mean = np.mean(table)
        mod5_component = np.broadcast_to(
            np.mean(table, axis=1, keepdims=True) - overall_mean,
            table.shape)
        mod13_component = np.broadcast_to(
            np.mean(table, axis=0, keepdims=True) - overall_mean,
            table.shape)
        interaction = (
            table - overall_mean - mod5_component - mod13_component)
        reflection5 = interaction[reflection5_indices, :]
        reflection13 = interaction[:, reflection13_indices]
        reflection_both = reflection5[:, reflection13_indices]
        return (
            interaction + reflection5 + reflection13 + reflection_both) / 4

    source_table = lift_orbit_row(
        base["orbit_coefficients"], divide_by_orbit_size=True)
    source_even_even = even_even_interaction(source_table)
    source_profile = mod5_contrast @ source_even_even
    source_profile_norm = float(np.linalg.norm(source_profile))
    if source_profile_norm <= 0:
        raise ValueError("source even-even profile has zero norm")
    source_reconstruction = np.outer(mod5_contrast, source_profile)
    source_scale = max(1.0, float(np.linalg.norm(source_even_even)))
    source_factorization_relative_error = float(
        np.linalg.norm(source_even_even - source_reconstruction)
        / source_scale)
    source_profile_mean_relative_error = abs(
        complex(np.sum(source_profile))) / max(
            1.0, float(np.sum(np.abs(source_profile))))
    source_profile_reflection_relative_error = float(
        np.max(np.abs(
            source_profile - source_profile[reflection13_indices]))
        * len(source_profile) / max(
            1.0, float(np.sum(np.abs(source_profile)))))

    rows = {}
    maximum_factorization_relative_error = 0.0
    maximum_profile_mean_relative_error = 0.0
    maximum_profile_reflection_relative_error = 0.0
    maximum_correlation_factorization_relative_error = 0.0
    for target, orbit_row in base["orbit_weight_discrepancy_rows"].items():
        discrepancy_table = lift_orbit_row(orbit_row)
        discrepancy_even_even = even_even_interaction(discrepancy_table)
        prime_profile = mod5_contrast @ discrepancy_even_even
        prime_profile_norm = float(np.linalg.norm(prime_profile))
        if prime_profile_norm <= 0:
            raise ValueError("prime even-even profile has zero norm")
        reconstructed = np.outer(mod5_contrast, prime_profile)
        component_scale = max(
            1.0, float(np.linalg.norm(discrepancy_even_even)))
        factorization_error = float(
            np.linalg.norm(discrepancy_even_even - reconstructed)
            / component_scale)
        direct_correlation = np.sum(
            discrepancy_even_even * source_even_even)
        profile_correlation = np.dot(prime_profile, source_profile)
        correlation_scale = max(
            1.0, abs(direct_correlation), abs(profile_correlation))
        correlation_error = abs(
            direct_correlation - profile_correlation) / correlation_scale
        alignment = float(
            abs(profile_correlation)
            / (prime_profile_norm * source_profile_norm))
        rows[target] = {
            "profile_alignment": alignment,
            "prime_profile_norm": prime_profile_norm,
            "even_even_profile_correlation": profile_correlation,
            "passes_profile_alignment_gate": bool(
                alignment <= maximum_profile_alignment),
        }
        maximum_factorization_relative_error = max(
            maximum_factorization_relative_error, factorization_error)
        maximum_profile_mean_relative_error = max(
            maximum_profile_mean_relative_error,
            abs(float(np.sum(prime_profile))) / max(
                1.0, float(np.sum(np.abs(prime_profile)))))
        maximum_profile_reflection_relative_error = max(
            maximum_profile_reflection_relative_error,
            float(np.max(np.abs(
                prime_profile - prime_profile[reflection13_indices])))
            * len(prime_profile) / max(
                1.0, float(np.sum(np.abs(prime_profile)))))
        maximum_correlation_factorization_relative_error = max(
            maximum_correlation_factorization_relative_error,
            float(correlation_error))

    dyadic_profile_summaries = {}
    for block in base["dyadic_block_summaries"]:
        block_lower, block_upper = block
        block_targets = tuple(
            target for target in rows
            if block_lower <= target < block_upper)
        maximum_target = max(
            block_targets, key=lambda target: rows[target]["profile_alignment"])
        alignments = tuple(rows[target]["profile_alignment"]
                           for target in block_targets)
        dyadic_profile_summaries[block] = {
            "target_count": len(block_targets),
            "maximum_profile_alignment": rows[maximum_target][
                "profile_alignment"],
            "maximum_target": maximum_target,
            "median_profile_alignment": float(np.median(alignments)),
            "all_targets_pass_profile_alignment_gate": all(
                rows[target]["passes_profile_alignment_gate"]
                for target in block_targets),
        }
    worst_target = max(
        rows, key=lambda target: rows[target]["profile_alignment"])
    violating_targets = tuple(
        target for target, row in rows.items()
        if not row["passes_profile_alignment_gate"])
    return {
        "families": base["families"],
        "arithmetic_period": base["arithmetic_period"],
        "quotient": base["quotient"],
        "common_modulus": base["common_modulus"],
        "target_range": base["target_range"],
        "target_residue": base["target_residue"],
        "progression_step": base["progression_step"],
        "residue5_values": residue5_values,
        "residue13_values": residue13_values,
        "mod5_contrast": tuple(float(value) for value in mod5_contrast),
        "source_profile": tuple(complex(value) for value in source_profile),
        "source_profile_norm": source_profile_norm,
        "source_factorization_relative_error": (
            source_factorization_relative_error),
        "source_profile_mean_relative_error": (
            source_profile_mean_relative_error),
        "source_profile_reflection_relative_error": (
            source_profile_reflection_relative_error),
        "maximum_prime_factorization_relative_error": (
            maximum_factorization_relative_error),
        "maximum_prime_profile_mean_relative_error": (
            maximum_profile_mean_relative_error),
        "maximum_prime_profile_reflection_relative_error": (
            maximum_profile_reflection_relative_error),
        "maximum_correlation_factorization_relative_error": (
            maximum_correlation_factorization_relative_error),
        "maximum_profile_alignment_gate": maximum_profile_alignment,
        "rows": rows,
        "tested_target_count": len(rows),
        "violating_targets": violating_targets,
        "violating_target_count": len(violating_targets),
        "worst_target": worst_target,
        "maximum_profile_alignment": rows[worst_target]["profile_alignment"],
        "dyadic_profile_summaries": dyadic_profile_summaries,
        "all_targets_pass_profile_alignment_gate": not violating_targets,
        "finite_even_even_profiles_measured": True,
        "uniform_even_even_profile_nonresonance_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def affine_reflection_residue_scan_receipt(
        maximum_symmetric_energy_fraction=.75,
        tolerance=1e-12, batch_size=32):
    if (not math.isfinite(maximum_symmetric_energy_fraction)
            or not 0 <= maximum_symmetric_energy_fraction <= 1):
        raise ValueError(
            "maximum symmetric energy fraction must lie in [0, 1]")
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
    source_cell_expected_totals = {}
    for lag in CANONICAL_LAGS:
        common = math.gcd(lag, period)
        quotient = period // common
        (frequencies, _, _, divisor_strata, _) = (
            _partial_fourier_frequency_totals(
                period, lag, left_sources, right_sources, batch_size))
        active = _primitive_quadratic_character_fits(
            frequencies, common, quotient, divisor_strata, tolerance)[
                "active_divisors"]
        primitive_mask = np.asarray(tuple(
            math.gcd(int(frequency), common) == 1
            for frequency in frequencies), dtype=bool)
        units = frequencies[primitive_mask] // quotient
        for divisor in active:
            values = divisor_strata[divisor][primitive_mask]
            additive_unit_values = np.asarray(tuple(
                np.sum(values * np.exp(
                    2j * np.pi * units * unit / common))
                for unit in units), dtype=np.complex128)
            source_cell_expected_totals[(quotient, divisor)] = {
                "summed_reflection_covariance": abs(
                    np.sum(additive_unit_values)) ** 2,
                "summed_admissible_source_energy": (
                    len(units)
                    * float(np.sum(np.abs(additive_unit_values) ** 2))),
            }
            for target_residue in range(0, common, 2):
                projection = _affine_reflection_projection(
                    common, units, additive_unit_values, target_residue)
                source_energy = projection["source_energy"]
                if source_energy == 0:
                    continue
                symmetric_fraction = (
                    projection["symmetric_source_energy"] / source_energy)
                scale = max(1.0, source_energy)
                rows[(quotient, divisor, target_residue)] = {
                    "common_modulus": common,
                    "target_residue": target_residue,
                    "admissible_residue_count": len(
                        projection["admissible_columns"]),
                    "symmetric_source_energy_fraction": symmetric_fraction,
                    "normalized_affine_reflection_covariance": (
                        2 * symmetric_fraction - 1),
                    "source_energy": source_energy,
                    "symmetric_source_energy": projection[
                        "symmetric_source_energy"],
                    "reflection_covariance": projection[
                        "reflection_covariance"],
                    "affine_reflection_is_involution": projection[
                        "is_involution"],
                    "affine_projector_energy_relative_error": (
                        projection["energy_error"] / scale),
                    "affine_projector_orthogonality_relative_error": (
                        projection["orthogonality_error"] / scale),
                    "passes_symmetric_energy_gate": bool(
                        symmetric_fraction
                        <= maximum_symmetric_energy_fraction),
                }

    minimum_key = min(
        rows, key=lambda key: rows[key][
            "symmetric_source_energy_fraction"])
    maximum_key = max(
        rows, key=lambda key: rows[key][
            "symmetric_source_energy_fraction"])
    gate_pass_count = sum(
        row["passes_symmetric_energy_gate"] for row in rows.values())
    exact_projection_passes = all(
        row["affine_reflection_is_involution"]
        and row["affine_projector_energy_relative_error"] <= tolerance
        and row["affine_projector_orthogonality_relative_error"] <= tolerance
        for row in rows.values())
    source_cell_summaries = {}
    for source_cell in sorted({key[:2] for key in rows}):
        fractions = tuple(
            row["symmetric_source_energy_fraction"]
            for key, row in rows.items() if key[:2] == source_cell)
        cell_rows = tuple(
            row for key, row in rows.items() if key[:2] == source_cell)
        summed_covariance = sum(
            (row["reflection_covariance"] for row in cell_rows), 0.0j)
        summed_source_energy = math.fsum(
            row["source_energy"] for row in cell_rows)
        summed_symmetric_energy = math.fsum(
            row["symmetric_source_energy"] for row in cell_rows)
        expected_totals = source_cell_expected_totals[source_cell]
        expected_covariance = expected_totals[
            "summed_reflection_covariance"]
        expected_source_energy = expected_totals[
            "summed_admissible_source_energy"]
        covariance_scale = max(1.0, expected_covariance)
        source_energy_scale = max(1.0, expected_source_energy)
        weighted_fraction = (
            summed_symmetric_energy / summed_source_energy)
        closed_form_weighted_fraction = (
            .5 + expected_covariance / (2 * expected_source_energy))
        source_cell_summaries[source_cell] = {
            "target_residue_count": len(fractions),
            "energy_gate_pass_count": sum(
                fraction <= maximum_symmetric_energy_fraction
                for fraction in fractions),
            "mean_symmetric_source_energy_fraction": (
                math.fsum(fractions) / len(fractions)),
            "symmetric_source_energy_fraction_range": (
                min(fractions), max(fractions)),
            "summed_reflection_covariance_relative_error": (
                abs(summed_covariance - expected_covariance)
                / covariance_scale),
            "summed_admissible_source_energy_relative_error": (
                abs(summed_source_energy - expected_source_energy)
                / source_energy_scale),
            "energy_weighted_mean_symmetric_fraction": weighted_fraction,
            "closed_form_energy_weighted_mean_symmetric_fraction": (
                closed_form_weighted_fraction),
            "closed_form_weighted_mean_relative_error": (
                abs(weighted_fraction - closed_form_weighted_fraction)
                / max(1.0, abs(closed_form_weighted_fraction))),
        }
    all_convolution_identities_pass = all(
        summary["summed_reflection_covariance_relative_error"] <= tolerance
        and summary[
            "summed_admissible_source_energy_relative_error"] <= tolerance
        and summary["closed_form_weighted_mean_relative_error"] <= tolerance
        for summary in source_cell_summaries.values())
    return {
        "families": CANONICAL_FAMILIES,
        "arithmetic_period": period,
        "common_moduli": tuple(sorted({
            row["common_modulus"] for row in rows.values()})),
        "maximum_symmetric_energy_fraction_gate": (
            maximum_symmetric_energy_fraction),
        "rows": rows,
        "source_cell_summaries": source_cell_summaries,
        "minimum_symmetric_energy_cell": (
            minimum_key, rows[minimum_key]),
        "maximum_symmetric_energy_cell": (
            maximum_key, rows[maximum_key]),
        "energy_gate_pass_count": gate_pass_count,
        "energy_gate_cell_count": len(rows),
        "all_affine_projection_identities_pass": bool(
            exact_projection_passes),
        "all_target_average_convolution_identities_pass": bool(
            all_convolution_identities_pass),
        "target_average_source_identity_proved_in_canonical_cells": bool(
            exact_projection_passes and all_convolution_identities_pass),
        "all_even_target_residues_in_canonical_cells_pass_gate": bool(
            exact_projection_passes and gate_pass_count == len(rows)),
        "uniform_all_source_energy_theorem_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def linked_prime_character_receipt(
        targets=LINKED_PRIME_TARGETS, tolerance=1e-12, batch_size=32):
    targets = tuple(targets)
    if (not targets
            or any(type(target) is not int or target < 20 or target % 2
                   for target in targets)):
        raise ValueError("targets must be even integers at least 20")
    if any(not _linked_prime_pairs(
            target, target // 3, target - target // 3)
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
                upper = target - lower
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


def linked_prime_parity_selection_receipt(tolerance=1e-12, batch_size=32):
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
    target_by_quotient = {77: 1040, 91: 1100}
    rows = {}
    for lag in CANONICAL_LAGS:
        common = math.gcd(lag, period)
        quotient = period // common
        target = target_by_quotient[quotient]
        lower = target // 3
        upper = target - lower
        (frequencies, _, _, divisor_strata, _) = (
            _partial_fourier_frequency_totals(
                period, lag, left_sources, right_sources, batch_size))
        active = _primitive_quadratic_character_fits(
            frequencies, common, quotient, divisor_strata, tolerance)[
                "active_divisors"]
        for divisor in active:
            rows[(quotient, divisor)] = _linked_prime_character_row(
                common, quotient, frequencies, divisor_strata[divisor],
                target, lower, upper, tolerance)
    return {
        "families": CANONICAL_FAMILIES,
        "arithmetic_period": period,
        "target_by_quotient": target_by_quotient,
        "rows": rows,
        "maximum_odd_prime_correlation_relative_to_pair_weight": max(
            row["maximum_odd_prime_correlation_relative_to_pair_weight"]
            for row in rows.values()),
        "maximum_parity_decomposition_natural_scale_relative_error": max(
            row["parity_decomposition_natural_scale_relative_error"]
            for row in rows.values()),
        "all_odd_character_prime_correlations_cancel": all(
            row["all_odd_character_prime_correlations_cancel"]
            for row in rows.values()),
        "all_even_characters_reconstruct_unit_correlations": all(
            row["even_characters_reconstruct_unit_correlation"]
            for row in rows.values()),
        "target_divisibility_parity_selection_proved": True,
        "uniform_target_parity_selection_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }
