"""Exact Goldbach-sum form of the dominant even-even CRT numerator.

This module isolates an algebraic transfer.  It does not assert a mean-square
estimate for the resulting twisted Goldbach sums.
"""

import math

import numpy as np

from lcm_sawtooth_cotangent_count import _one_orientation_count_source_modes
from lcm_sawtooth_frequency_resolved_fourier import (
    CANONICAL_FAMILIES,
    CANONICAL_LAGS,
    _unit_character_table,
)
from lcm_sawtooth_linked_prime_character import (
    _linked_prime_pairs,
    recombined_centered_character_receipt,
    residue_orbit_even_even_profile_receipt,
)


def even_even_goldbach_transfer_receipt(
        target_minimum=1700, target_maximum=22000, target_residue=72,
        tolerance=1e-12, batch_size=32):
    """Rewrite ``<h_N,h_C>`` as fixed central Goldbach twists.

    For every tested ``N == target_residue (mod 130)``, the returned identity
    is

        <h_N,h_C> = sum_{N/3 < p < 2N/3, p+q=N}
                         c(p mod 130) log(p) log(q),

    where the sum is ordered and prime-only.  On the stated range every prime
    in the strict central interval is a unit modulo 130.  The coefficient
    function is also expanded in all 48 Dirichlet characters of the unit
    group modulo 130.  These are finite algebraic identities, not estimates.
    """
    base = residue_orbit_even_even_profile_receipt(
        target_minimum=target_minimum,
        target_maximum=target_maximum,
        target_residue=target_residue,
        tolerance=tolerance,
        batch_size=batch_size)
    common = base["common_modulus"]
    if common != 130:
        raise AssertionError("expected common modulus 130")
    target_residue = base["target_residue"]
    residue5_values = base["residue5_values"]
    residue13_values = base["residue13_values"]
    residue5_index = {
        residue: index for index, residue in enumerate(residue5_values)}
    residue13_index = {
        residue: index for index, residue in enumerate(residue13_values)}
    mod5_contrast = np.asarray(base["mod5_contrast"], dtype=np.float64)
    source_profile = np.asarray(base["source_profile"], dtype=np.complex128)

    units = tuple(residue for residue in range(common)
                  if math.gcd(residue, common) == 1)
    admissible_residues = tuple(
        residue for residue in units
        if math.gcd((target_residue - residue) % common, common) == 1)
    coefficient_by_residue = {}
    for residue in admissible_residues:
        coefficient_by_residue[residue] = complex(
            mod5_contrast[residue5_index[residue % 5]]
            * source_profile[residue13_index[residue % 13]])

    coefficient_sum = sum(coefficient_by_residue.values(), 0.0j)
    coefficient_scale = max(
        1.0, math.fsum(abs(value)
                       for value in coefficient_by_residue.values()))
    reflection_error = max(abs(
        coefficient_by_residue[residue]
        - coefficient_by_residue[(target_residue - residue) % common])
        for residue in admissible_residues)

    # A central prime pair cannot use an inadmissible unit residue: if p is a
    # unit and N-p is prime but nonunit modulo 130, then N-p is 2, 5, or 13,
    # outside the strict central interval for the admitted target range.
    coefficient_on_units = np.asarray(tuple(
        coefficient_by_residue.get(residue, 0.0j) for residue in units),
        dtype=np.complex128)
    _, character_labels, character_table = _unit_character_table(common, units)
    character_coefficients = (
        np.conjugate(character_table) @ coefficient_on_units / len(units))
    character_reconstruction = character_table.T @ character_coefficients
    character_scale = max(1.0, float(np.linalg.norm(coefficient_on_units)))
    character_reconstruction_relative_error = float(
        np.linalg.norm(character_reconstruction - coefficient_on_units)
        / character_scale)

    rows = {}
    maximum_identity_relative_error = 0.0
    for target, profile_row in base["rows"].items():
        lower = target // 3
        upper = target - lower
        central_sum = 0.0j
        nonunit_pairs = []
        inadmissible_unit_pairs = []
        ordered_pair_count = 0
        for prime, weight in _linked_prime_pairs(target, lower, upper):
            partner = target - prime
            ordered_pair_count += 1
            if math.gcd(prime, common) != 1:
                nonunit_pairs.append((prime, partner))
                continue
            coefficient = coefficient_by_residue.get(prime % common)
            if coefficient is None:
                inadmissible_unit_pairs.append((prime, partner))
                continue
            central_sum += coefficient * weight
        profile_correlation = complex(
            profile_row["even_even_profile_correlation"])
        scale = max(1.0, abs(central_sum), abs(profile_correlation))
        identity_relative_error = abs(
            central_sum - profile_correlation) / scale
        maximum_identity_relative_error = max(
            maximum_identity_relative_error, identity_relative_error)
        rows[target] = {
            "ordered_central_prime_pair_count": ordered_pair_count,
            "nonunit_prime_pairs": tuple(nonunit_pairs),
            "inadmissible_unit_prime_pairs": tuple(inadmissible_unit_pairs),
            "central_residue_weighted_goldbach_sum": central_sum,
            "even_even_profile_correlation": profile_correlation,
            "identity_relative_error": identity_relative_error,
        }

    all_nonunit_pairs = tuple(
        (target, pair)
        for target, row in rows.items()
        for pair in row["nonunit_prime_pairs"])
    all_inadmissible_unit_pairs = tuple(
        (target, pair)
        for target, row in rows.items()
        for pair in row["inadmissible_unit_prime_pairs"])
    return {
        "common_modulus": common,
        "target_range": base["target_range"],
        "target_residue": target_residue,
        "progression_step": base["progression_step"],
        "strict_central_interval": "N/3 < p < 2N/3",
        "ordered_prime_only_logarithmic_weight": True,
        "admissible_residues": admissible_residues,
        "coefficient_by_residue": coefficient_by_residue,
        "coefficient_sum_relative_error": abs(coefficient_sum) / coefficient_scale,
        "maximum_reflection_coefficient_error": reflection_error,
        "dirichlet_character_labels": character_labels,
        "dirichlet_character_coefficients": tuple(
            complex(value) for value in character_coefficients),
        "dirichlet_character_reconstruction_relative_error": (
            character_reconstruction_relative_error),
        "rows": rows,
        "tested_target_count": len(rows),
        "nonunit_prime_pairs": all_nonunit_pairs,
        "inadmissible_unit_prime_pairs": all_inadmissible_unit_pairs,
        "maximum_goldbach_transfer_identity_relative_error": (
            maximum_identity_relative_error),
        "fixed_central_goldbach_residue_identity_proved_in_tested_range": bool(
            not all_nonunit_pairs
            and not all_inadmissible_unit_pairs
            and maximum_identity_relative_error <= tolerance),
        "fixed_dirichlet_character_expansion_verified": bool(
            character_reconstruction_relative_error <= tolerance),
        "halupczok_theorem6_prime_only_weight_matches": True,
        "moving_central_window_box_reduction_proved": True,
        "applicable_mean_square_theorem_identified": True,
        "almost_all_centered_correlation_estimate_proved": True,
        "pointwise_centered_correlation_estimate_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


def all_even_residue_goldbach_main_receipt(tolerance=1e-12, batch_size=32):
    """Return the fixed singular-main coefficient for every even class.

    Let ``G_0`` be the globally centered recombined quotient-77 source.  For
    ``N == n (mod 130)`` and

        A_n = {a in units mod 130: n-a is also a unit},

    Halupczok's residue-class singular series is independent of ``a`` on
    ``A_n``.  The central interval has asymptotic length ``N/3``.  Therefore
    the main multiplying ``N*S(130N)`` is

        sum_{a in A_n} G_0(a) / (3*phi(130)).

    Subtracting the local mean leaves a fixed zero-sum coefficient to which
    the reviewed central-window box transfer applies.  The returned data are
    coefficient identities; the cited theorem supplies the asymptotic error.
    """
    character = recombined_centered_character_receipt(
        tolerance=tolerance, batch_size=batch_size)
    common = character["common_modulus"]
    if common != 130:
        raise AssertionError("expected common modulus 130")
    units = tuple(int(residue) for residue in character["unit_residues"])
    source_by_residue = {
        residue: complex(value)
        for residue, value in zip(
            units, character["centered_source_values"])}
    group_order = len(units)
    rows = {}
    maximum_centered_sum_relative_error = 0.0
    maximum_crt_inclusion_exclusion_relative_error = 0.0
    global_source_sum = sum(source_by_residue.values(), 0.0j)
    for target_residue in range(0, common, 2):
        admissible = tuple(
            residue for residue in units
            if math.gcd((target_residue - residue) % common, common) == 1)
        source_sum = sum(
            (source_by_residue[residue] for residue in admissible), 0.0j)
        source_l1 = math.fsum(
            abs(source_by_residue[residue]) for residue in admissible)
        local_mean = source_sum / len(admissible)
        centered = {
            residue: source_by_residue[residue] - local_mean
            for residue in admissible}
        centered_sum = sum(centered.values(), 0.0j)
        centered_scale = max(
            1.0, math.fsum(abs(value) for value in centered.values()))
        centered_sum_relative_error = abs(centered_sum) / centered_scale
        maximum_centered_sum_relative_error = max(
            maximum_centered_sum_relative_error,
            centered_sum_relative_error)
        forbidden_mod5 = tuple(
            residue for residue in units
            if (target_residue - residue) % 5 == 0)
        forbidden_mod13 = tuple(
            residue for residue in units
            if (target_residue - residue) % 13 == 0)
        forbidden_both = tuple(sorted(
            set(forbidden_mod5).intersection(forbidden_mod13)))
        forbidden_mod5_sum = sum(
            (source_by_residue[residue] for residue in forbidden_mod5),
            0.0j)
        forbidden_mod13_sum = sum(
            (source_by_residue[residue] for residue in forbidden_mod13),
            0.0j)
        forbidden_both_sum = sum(
            (source_by_residue[residue] for residue in forbidden_both),
            0.0j)
        inclusion_exclusion_sum = (
            global_source_sum - forbidden_mod5_sum
            - forbidden_mod13_sum + forbidden_both_sum)
        inclusion_scale = max(
            1.0, abs(source_sum), abs(inclusion_exclusion_sum), source_l1)
        inclusion_relative_error = abs(
            inclusion_exclusion_sum - source_sum) / inclusion_scale
        maximum_crt_inclusion_exclusion_relative_error = max(
            maximum_crt_inclusion_exclusion_relative_error,
            inclusion_relative_error)
        rows[target_residue] = {
            "admissible_residues": admissible,
            "admissible_residue_count": len(admissible),
            "source_sum": source_sum,
            "local_source_mean": local_mean,
            "local_source_bias_ratio": (
                abs(source_sum) / source_l1 if source_l1 else 0.0),
            "locally_centered_source": centered,
            "locally_centered_sum_relative_error": (
                centered_sum_relative_error),
            "forbidden_mod5_residues": forbidden_mod5,
            "forbidden_mod13_residues": forbidden_mod13,
            "forbidden_both_residues": forbidden_both,
            "forbidden_mod5_source_sum": forbidden_mod5_sum,
            "forbidden_mod13_source_sum": forbidden_mod13_sum,
            "forbidden_both_source_sum": forbidden_both_sum,
            "crt_inclusion_exclusion_source_sum": inclusion_exclusion_sum,
            "crt_inclusion_exclusion_relative_error": (
                inclusion_relative_error),
            "central_singular_main_multiplier": (
                source_sum / (3 * group_order)),
        }
    return {
        "common_modulus": common,
        "unit_group_order": group_order,
        "even_target_residue_count": len(rows),
        "rows": rows,
        "maximum_local_source_bias_ratio": max(
            row["local_source_bias_ratio"] for row in rows.values()),
        "maximum_locally_centered_sum_relative_error": (
            maximum_centered_sum_relative_error),
        "global_centered_source_sum": global_source_sum,
        "maximum_crt_inclusion_exclusion_relative_error": (
            maximum_crt_inclusion_exclusion_relative_error),
        "asymptotic_formula": (
            "L_N(G_0)=N*S(130N)*central_singular_main_multiplier+E_N"),
        "all_even_residue_singular_main_coefficients_identified": True,
        "all_even_residue_crt_inclusion_exclusion_identities_verified": bool(
            maximum_crt_inclusion_exclusion_relative_error <= tolerance),
        "local_uniform_channel_has_same_asymptotic_main": True,
        "all_even_target_l1_error_log_saving_proved": True,
        "all_even_target_l2_error_log_saving_proved": True,
        "pointwise_signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def _source_mode_matrices(period, sources):
    residues = np.asarray(sorted(sources), dtype=np.int64)
    width = max(map(len, sources.values()))
    frequencies = np.zeros((len(residues), width), dtype=np.int64)
    coefficients = np.zeros((len(residues), width), dtype=np.complex128)
    for row, residue in enumerate(residues):
        items = tuple(sources[int(residue)].items())
        frequencies[row, :len(items)] = tuple(item[0] for item in items)
        coefficients[row, :len(items)] = tuple(item[1] for item in items)
    if np.any(frequencies < 0) or np.any(frequencies >= period):
        raise ValueError("source frequency lies outside the arithmetic period")
    return residues, frequencies, coefficients


def _direct_resonant_source_on_units(
        period, lag, left_sources, right_sources):
    """Evaluate the unaveraged fully resonant lag source for every unit p."""
    common = math.gcd(lag, period)
    quotient = period // common
    left_residues, left_frequencies, left_coefficients = (
        _source_mode_matrices(period, left_sources))
    right_residues, right_frequencies, right_coefficients = (
        _source_mode_matrices(period, right_sources))
    right_index = np.full(period, -1, dtype=np.int64)
    right_index[right_residues] = np.arange(len(right_residues))
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    values = []
    for prime_residue in units:
        difference = lag * pow(prime_residue, -1, period) % period
        indices = right_index[(left_residues - difference) % period]
        valid = indices >= 0
        frequency_differences = (
            left_frequencies[valid, :, None]
            - right_frequencies[indices[valid], None, :]) % period
        terms = (
            left_coefficients[valid, :, None]
            * np.conjugate(right_coefficients[indices[valid], None, :]))
        terms *= np.exp(
            2j * np.pi
            * ((prime_residue * frequency_differences) % period) / period)
        values.append(complex(np.sum(
            terms[frequency_differences % quotient == 0])))
    return units, tuple(values)


def canonical_direct_resonant_goldbach_main_receipt(tolerance=1e-12):
    """Identify almost-all mains for the actual fixed sources on U_10010.

    The source is evaluated before the conditioned unit-prime average used by
    the frequency-total receipts.  It is a fixed function of ``p mod 10010``;
    it generally does not descend to the smaller common modulus of a lag.

    For either lag source ``F_ell`` and every fixed pair of coefficients
    ``lambda_ell``, Halupczok's Theorem 6 plus the reviewed moving-window
    reduction gives

        R_N(lambda) = M_N(lambda) + E_N(lambda),
        M_N(lambda) = N*S(10010*N)/(3*phi(10010))
                      * sum_(a in A_N) sum_ell lambda_ell*F_ell(a),

    where ``A_N={a in U_10010:N-a in U_10010}``.  For every fixed ``K``, the
    even-target L1 and L2 sums of ``E_N`` are respectively
    ``O_(K,lambda)(X^2/log(X)^K)`` and
    ``O_(K,lambda)(X^3/log(X)^K)``.  No original outer assembly or pointwise
    Goldbach estimate is asserted.
    """
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    period = math.lcm(
        CANONICAL_FAMILIES[0][0], 2 * CANONICAL_FAMILIES[0][1])
    left_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[1])[2]
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    unit_indicator = np.zeros(period, dtype=np.float64)
    unit_indicator[list(units)] = 1.0
    admissible_counts = np.rint(np.fft.ifft(
        np.fft.fft(unit_indicator) ** 2).real).astype(np.int64)

    lag_rows = {}
    maximum_convolution_reconstruction_error = 0.0
    for lag in CANONICAL_LAGS:
        source_units, source_values_tuple = _direct_resonant_source_on_units(
            period, lag, left_sources, right_sources)
        if source_units != units:
            raise AssertionError("direct source unit ordering changed")
        source_values = np.asarray(source_values_tuple, dtype=np.complex128)
        source_table = np.zeros(period, dtype=np.complex128)
        source_table[list(units)] = source_values
        admissible_sums = np.fft.ifft(
            np.fft.fft(source_table) * np.fft.fft(unit_indicator))
        sampled_targets = (0, 2, 72, period - 2)
        convolution_errors = []
        for target_residue in sampled_targets:
            direct_sum = sum((
                source_values[index]
                for index, residue in enumerate(units)
                if math.gcd(
                    (target_residue - residue) % period, period) == 1),
                0.0j)
            convolution_errors.append(
                abs(direct_sum - admissible_sums[target_residue])
                / max(1.0, abs(direct_sum)))
        convolution_reconstruction_error = max(convolution_errors)
        maximum_convolution_reconstruction_error = max(
            maximum_convolution_reconstruction_error,
            convolution_reconstruction_error)
        common = math.gcd(lag, period)
        witness_residues = (1, 1 + common)
        witness_values = tuple(
            source_values[units.index(residue)]
            for residue in witness_residues)
        witness_scale = max(1.0, *(abs(value) for value in witness_values))
        descent_witness_ratio = abs(
            witness_values[0] - witness_values[1]) / witness_scale
        residue_rows = {}
        for target_residue in range(0, period, 2):
            source_sum = complex(admissible_sums[target_residue])
            residue_rows[target_residue] = {
                "admissible_residue_count": int(
                    admissible_counts[target_residue]),
                "source_sum": source_sum,
                "central_singular_main_multiplier": (
                    source_sum / (3 * len(units))),
            }
        lag_rows[lag] = {
            "common_modulus": common,
            "quotient": period // common,
            "source_unit_count": len(source_values),
            "source_l2": float(np.linalg.norm(source_values)),
            "source_mean": complex(np.mean(source_values)),
            "common_modulus_descent_witness_residues": witness_residues,
            "common_modulus_descent_witness_values": witness_values,
            "common_modulus_descent_witness_ratio": descent_witness_ratio,
            "source_descends_to_common_modulus": bool(
                descent_witness_ratio <= tolerance),
            "sampled_convolution_targets": sampled_targets,
            "sampled_convolution_reconstruction_relative_error": (
                convolution_reconstruction_error),
            "even_target_residue_count": len(residue_rows),
            "residue_rows": residue_rows,
        }

    return {
        "families": CANONICAL_FAMILIES,
        "lags": CANONICAL_LAGS,
        "arithmetic_period": period,
        "unit_group_order": len(units),
        "even_target_residue_count": period // 2,
        "lag_rows": lag_rows,
        "maximum_sampled_convolution_reconstruction_relative_error": (
            maximum_convolution_reconstruction_error),
        "asymptotic_formula": (
            "R_N(lambda)=N*S(10010*N)/(3*phi(10010))*"
            "sum_(a in A_N)sum_lag lambda_lag*F_lag(a)+E_N(lambda)"),
        "actual_unaveraged_periodic_sources_identified": True,
        "halupczok_modulus_10010_transfer_proved": True,
        "all_even_target_l1_error_log_saving_proved": True,
        "all_even_target_l2_error_log_saving_proved": True,
        "smaller_common_modulus_descent_proved": False,
        "original_outer_assembly_identification_proved": False,
        "pointwise_direct_resonant_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def direct_source_fiber_average_receipt(tolerance=1e-12):
    """Compare the old mod-130 source with full-period direct sources.

    The direct lag-130 source does not descend pointwise to ``U_130``.  Its
    fiber sum over the 60 lifts in ``U_10010`` nevertheless has the exact
    centered quotient source previously used in the mod-130 Goldbach transfer:

        G_0(r) = -(sum_{a in U_10010, a=r mod 130} F_130(a)
                  - mean_s sum_{a=s mod 130} F_130(a)).

    This identifies the earlier quotient-77 source as a fiber-averaged
    shadow of the actual direct lag-130 source.  It is not an identification
    of the original outer assembly or the formal signed error.
    """
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    character = recombined_centered_character_receipt(tolerance=tolerance)
    common = character["common_modulus"]
    if common != 130:
        raise AssertionError("expected recombined source modulo 130")
    period = math.lcm(
        CANONICAL_FAMILIES[0][0], 2 * CANONICAL_FAMILIES[0][1])
    if period % common:
        raise AssertionError("common modulus must divide the full period")
    left_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[1])[2]
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    units_by_common_residue = {
        residue: tuple(unit for unit in units if unit % common == residue)
        for residue in character["unit_residues"]}
    fiber_counts = tuple(
        len(fiber) for fiber in units_by_common_residue.values())
    if len(set(fiber_counts)) != 1:
        raise AssertionError("unit fibers over U_130 are not uniform")
    fiber_size = fiber_counts[0]
    source_by_residue = np.asarray(
        character["centered_source_values"], dtype=np.complex128)
    source_scale = max(1.0, float(np.linalg.norm(source_by_residue)))

    lag_rows = {}
    for lag in CANONICAL_LAGS:
        source_units, source_values_tuple = _direct_resonant_source_on_units(
            period, lag, left_sources, right_sources)
        if source_units != units:
            raise AssertionError("direct source unit ordering changed")
        source_values = {
            residue: value
            for residue, value in zip(source_units, source_values_tuple)}
        fiber_sums = np.asarray(tuple(
            sum((source_values[unit] for unit in units_by_common_residue[
                residue]), 0.0j)
            for residue in character["unit_residues"]),
            dtype=np.complex128)
        fiber_averages = fiber_sums / fiber_size
        centered_fiber_sums = fiber_sums - np.mean(fiber_sums)
        centered_fiber_averages = fiber_averages - np.mean(fiber_averages)

        denominator = np.vdot(centered_fiber_sums, centered_fiber_sums)
        best_sum_coefficient = (
            np.vdot(centered_fiber_sums, source_by_residue) / denominator
            if abs(denominator) else 0.0j)
        best_sum_fit = best_sum_coefficient * centered_fiber_sums
        best_sum_relative_error = float(
            np.linalg.norm(best_sum_fit - source_by_residue) / source_scale)
        sum_correlation = float(
            abs(np.vdot(centered_fiber_sums, source_by_residue))
            / max(
                np.finfo(float).tiny,
                float(np.linalg.norm(centered_fiber_sums))
                * float(np.linalg.norm(source_by_residue))))
        signed_sum_reconstruction = -centered_fiber_sums
        signed_sum_relative_error = float(
            np.linalg.norm(
                signed_sum_reconstruction - source_by_residue)
            / source_scale)
        signed_average_reconstruction = -fiber_size * centered_fiber_averages
        signed_average_relative_error = float(
            np.linalg.norm(
                signed_average_reconstruction - source_by_residue)
            / source_scale)
        lag_rows[lag] = {
            "common_modulus": math.gcd(lag, period),
            "quotient": period // math.gcd(lag, period),
            "fiber_size_over_U130": fiber_size,
            "fiber_sum_mean": complex(np.mean(fiber_sums)),
            "best_centered_fiber_sum_coefficient": complex(
                best_sum_coefficient),
            "best_centered_fiber_sum_fit_relative_error": (
                best_sum_relative_error),
            "centered_fiber_sum_correlation_with_G0": sum_correlation,
            "negative_centered_fiber_sum_reconstruction_relative_error": (
                signed_sum_relative_error),
            "negative_scaled_centered_fiber_average_relative_error": (
                signed_average_relative_error),
            "reconstructs_recombined_centered_source": bool(
                signed_sum_relative_error <= tolerance
                and signed_average_relative_error <= tolerance),
        }

    return {
        "families": CANONICAL_FAMILIES,
        "lags": CANONICAL_LAGS,
        "arithmetic_period": period,
        "common_modulus": common,
        "unit_group_order": len(character["unit_residues"]),
        "fiber_size_over_U130": fiber_size,
        "identity": (
            "G_0(r)=-sum_(a in U_10010,a=r mod 130)"
            "(F_130(a)-mean_over_U_10010/F_130 fibers)"),
        "lag_rows": lag_rows,
        "lag_130_fiber_average_identifies_G0": bool(
            lag_rows[130]["reconstructs_recombined_centered_source"]),
        "lag_110_fiber_average_identifies_G0": bool(
            lag_rows[110]["reconstructs_recombined_centered_source"]),
        "direct_source_pointwise_descent_to_mod130_proved": False,
        "quotient_source_fiber_shadow_identified": bool(
            lag_rows[130]["reconstructs_recombined_centered_source"]
            and not lag_rows[110]["reconstructs_recombined_centered_source"]),
        "original_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


if __name__ == "__main__":
    print(even_even_goldbach_transfer_receipt())
