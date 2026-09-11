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
