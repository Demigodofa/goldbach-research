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
    linked_prime_centering_receipt,
    _linked_prime_pairs,
    recombined_centered_character_receipt,
    residue_orbit_even_even_profile_receipt,
)


def _complex_fsum(values):
    values = tuple(values)
    return complex(
        math.fsum(value.real for value in values),
        math.fsum(value.imag for value in values))


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
            _complex_fsum(source_values[unit]
                          for unit in units_by_common_residue[residue])
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


def centered_outer_fiber_shadow_receipt(
        targets=(1000, 1002), tolerance=1e-12, batch_size=32):
    """Identify the surviving centered outer channel on fixture targets.

    This composes two finite identities: the linked-prime centering receipt
    recombines quotient 77 into ``G_0``, and ``G_0`` is the lag-130 fiber
    shadow of the direct full-period source.  The result is a target-level
    equality for the centered part of the tested outer assembly, while the
    principal constant term and the formal signed error remain separate.
    """
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    centering = linked_prime_centering_receipt(
        targets=targets, tolerance=tolerance, batch_size=batch_size)
    common = 130
    period = math.lcm(
        CANONICAL_FAMILIES[0][0], 2 * CANONICAL_FAMILIES[0][1])
    left_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[1])[2]
    source_units, source_values_tuple = _direct_resonant_source_on_units(
        period, 130, left_sources, right_sources)
    quotient77_source_row = next(
        row for (quotient, _, target), row in centering["rows"].items()
        if quotient == 77 and target == centering["targets"][0])
    units130 = tuple(int(unit) for unit in quotient77_source_row[
        "unit_residues"])
    source_values = {
        residue: value
        for residue, value in zip(source_units, source_values_tuple)}
    fiber_sums = np.asarray(tuple(
        _complex_fsum(source_values[unit] for unit in source_units
                      if unit % common == residue)
        for residue in units130), dtype=np.complex128)
    fiber_shadow = -(fiber_sums - np.mean(fiber_sums))
    fiber_shadow_by_residue = {
        residue: value for residue, value in zip(units130, fiber_shadow)}

    quotient77 = centering["quotient_summaries"][77]
    quotient91 = centering["quotient_summaries"][91]
    rows = {}
    maximum_shadow_relative_error = 0.0
    maximum_shadow_natural_scale_relative_error = 0.0
    for target in centering["targets"]:
        lower = target // 3
        upper = target - lower
        fiber_shadow_terms = []
        fiber_shadow_natural_scale = 0.0
        nonunit_prime_pairs = []
        inadmissible_unit_pairs = []
        for prime, weight in _linked_prime_pairs(target, lower, upper):
            partner = target - prime
            if math.gcd(prime, common) != 1:
                nonunit_prime_pairs.append((prime, partner))
                continue
            coefficient = fiber_shadow_by_residue.get(prime % common)
            if coefficient is None:
                inadmissible_unit_pairs.append((prime, partner))
                continue
            fiber_shadow_terms.append(coefficient * weight)
            fiber_shadow_natural_scale += abs(coefficient * weight)
        fiber_shadow_sum = _complex_fsum(fiber_shadow_terms)
        centered_correlation = quotient77["target_summaries"][target][
            "recombined_centered_source_correlation"]
        scale = max(
            1.0, abs(fiber_shadow_sum), abs(centered_correlation))
        relative_error = abs(
            fiber_shadow_sum - centered_correlation) / scale
        maximum_shadow_relative_error = max(
            maximum_shadow_relative_error, relative_error)
        natural_scale = max(
            1.0, fiber_shadow_natural_scale, abs(centered_correlation))
        natural_scale_relative_error = abs(
            fiber_shadow_sum - centered_correlation) / natural_scale
        maximum_shadow_natural_scale_relative_error = max(
            maximum_shadow_natural_scale_relative_error,
            natural_scale_relative_error)
        constant_correlation = quotient77["target_summaries"][target][
            "recombined_constant_source_correlation"]
        direct_correlation = quotient77["target_summaries"][target][
            "recombined_direct_unit_correlation"]
        rows[target] = {
            "strict_central_interval": (lower, upper),
            "fiber_shadow_weighted_goldbach_sum": fiber_shadow_sum,
            "recombined_quotient77_centered_correlation": (
                centered_correlation),
            "fiber_shadow_centered_relative_error": relative_error,
            "fiber_shadow_centered_natural_scale": natural_scale,
            "fiber_shadow_centered_natural_scale_relative_error": (
                natural_scale_relative_error),
            "recombined_quotient77_constant_correlation": (
                constant_correlation),
            "recombined_quotient77_direct_correlation": (
                direct_correlation),
            "constant_plus_shadow_reconstruction_relative_error": (
                abs(constant_correlation + fiber_shadow_sum
                    - direct_correlation)
                / max(
                    1.0, abs(constant_correlation),
                    abs(fiber_shadow_sum), abs(direct_correlation))),
            "nonunit_prime_pairs": tuple(nonunit_prime_pairs),
            "inadmissible_unit_pairs": tuple(inadmissible_unit_pairs),
        }
    maximum_quotient91_direct_ratio = max(
        row["recombined_direct_relative_to_natural_scale"]
        for row in quotient91["target_summaries"].values())
    return {
        "families": CANONICAL_FAMILIES,
        "arithmetic_period": period,
        "common_modulus": common,
        "targets": centering["targets"],
        "rows": rows,
        "maximum_fiber_shadow_centered_relative_error": (
            maximum_shadow_relative_error),
        "maximum_fiber_shadow_centered_natural_scale_relative_error": (
            maximum_shadow_natural_scale_relative_error),
        "maximum_quotient91_direct_relative_to_natural_scale": (
            maximum_quotient91_direct_ratio),
        "quotient77_centered_channel_is_lag130_fiber_shadow": bool(
            maximum_shadow_relative_error <= tolerance),
        "quotient91_recombined_channel_cancels_on_fixtures": bool(
            maximum_quotient91_direct_ratio <= tolerance),
        "constant_principal_channel_retained_separately": True,
        "full_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def all_residue_centered_outer_fiber_shadow_receipt(
        target_minimum=10000, target_maximum=30000,
        natural_tolerance=1e-12, signed_tolerance=1e-9,
        exact_tolerance=1e-12, batch_size=32):
    """Test the centered fiber-shadow bridge on all even classes mod 130.

    One target with a strict-central prime pair is selected in each even
    residue class.  Natural-scale error tests the coefficient identity without
    punishing signed cancellation; signed-scale error is retained as a
    diagnostic.
    """
    if (type(target_minimum) is not int or type(target_maximum) is not int
            or target_minimum < 20 or target_maximum < target_minimum):
        raise ValueError("require integer target bounds with 20<=min<=max")
    if (not math.isfinite(natural_tolerance) or natural_tolerance < 0
            or not math.isfinite(signed_tolerance) or signed_tolerance < 0
            or not math.isfinite(exact_tolerance) or exact_tolerance < 0):
        raise ValueError("tolerances must be finite and nonnegative")
    targets = []
    missing_residues = []
    for residue in range(0, 130, 2):
        first = target_minimum + (residue - target_minimum) % 130
        selected = None
        for target in range(first, target_maximum + 1, 130):
            if _linked_prime_pairs(
                    target, target // 3, target - target // 3):
                selected = target
                break
        if selected is None:
            missing_residues.append(residue)
        else:
            targets.append(selected)
    if missing_residues:
        raise ValueError(
            "target range misses strict-central pairs for residues "
            f"{tuple(missing_residues)}")
    base = centered_outer_fiber_shadow_receipt(
        targets=tuple(targets), tolerance=exact_tolerance,
        batch_size=batch_size)
    maximum_bad_prime_terms = max(
        len(row["nonunit_prime_pairs"]) + len(row["inadmissible_unit_pairs"])
        for row in base["rows"].values())
    return {
        "target_range": (target_minimum, target_maximum),
        "selected_targets": tuple(targets),
        "selected_target_count": len(targets),
        "covered_even_residue_count": len({target % 130
                                           for target in targets}),
        "base_receipt": base,
        "natural_tolerance": natural_tolerance,
        "signed_tolerance": signed_tolerance,
        "maximum_bad_prime_terms_per_target": maximum_bad_prime_terms,
        "all_even_residue_classes_sampled": bool(
            len(targets) == 65
            and len({target % 130 for target in targets}) == 65),
        "all_residue_natural_scale_bridge_passes": bool(
            base[
                "maximum_fiber_shadow_centered_natural_scale_relative_error"]
            <= natural_tolerance),
        "all_residue_signed_scale_diagnostic_passes": bool(
            base["maximum_fiber_shadow_centered_relative_error"]
            <= signed_tolerance),
        "quotient91_recombined_channel_cancels_on_samples": bool(
            base["quotient91_recombined_channel_cancels_on_fixtures"]),
        "full_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def symbolic_centered_outer_fiber_shadow_receipt(
        tolerance=1e-12, batch_size=32):
    """Prove the centered channel bridge as a coefficient identity.

    The finite target checks are consequences of this stronger fixed-vector
    statement.  The quotient-77 recombined centered source on ``U_130`` equals
    the lag-130 fiber shadow.  Since every strict central prime in an even
    target ``N>=40`` is greater than 13, central prime pairs have no nonunit
    modulo-130 terms, so the coefficient identity transfers to all such
    centered target correlations.
    """
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    centering = linked_prime_centering_receipt(
        tolerance=tolerance, batch_size=batch_size)
    first_target = centering["targets"][0]
    common = 130
    period = math.lcm(
        CANONICAL_FAMILIES[0][0], 2 * CANONICAL_FAMILIES[0][1])
    left_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[1])[2]
    source_units, source_values_tuple = _direct_resonant_source_on_units(
        period, 130, left_sources, right_sources)
    quotient77_source_rows = tuple(
        row for (quotient, _, target), row in centering["rows"].items()
        if quotient == 77 and target == first_target)
    quotient91_source_rows = tuple(
        row for (quotient, _, target), row in centering["rows"].items()
        if quotient == 91 and target == first_target)
    units130 = tuple(int(unit) for unit in quotient77_source_rows[0][
        "unit_residues"])
    quotient77_source = sum((
        row["additive_unit_source_values"] for row in quotient77_source_rows),
        np.zeros_like(quotient77_source_rows[0][
            "additive_unit_source_values"]))
    quotient77_centered = quotient77_source - np.mean(quotient77_source)
    quotient91_source = sum((
        row["additive_unit_source_values"] for row in quotient91_source_rows),
        np.zeros_like(quotient91_source_rows[0][
            "additive_unit_source_values"]))
    quotient91_sectorwise_l2 = math.fsum(
        float(np.linalg.norm(row["additive_unit_source_values"]))
        for row in quotient91_source_rows)

    source_values = {
        residue: value
        for residue, value in zip(source_units, source_values_tuple)}
    fiber_sums = np.asarray(tuple(
        _complex_fsum(source_values[unit] for unit in source_units
                      if unit % common == residue)
        for residue in units130), dtype=np.complex128)
    fiber_shadow = -(fiber_sums - np.mean(fiber_sums))
    vector_scale = max(
        1.0, float(np.linalg.norm(fiber_shadow)),
        float(np.linalg.norm(quotient77_centered)))
    coefficient_error = float(
        np.linalg.norm(quotient77_centered - fiber_shadow) / vector_scale)
    quotient91_scale = max(1.0, quotient91_sectorwise_l2)
    quotient91_relative_l2 = float(
        np.linalg.norm(quotient91_source) / quotient91_scale)
    return {
        "families": CANONICAL_FAMILIES,
        "arithmetic_period": period,
        "common_modulus": common,
        "unit_group_order": len(units130),
        "fiber_size_over_U130": len(source_units) // len(units130),
        "quotient77_divisor_row_count": len(quotient77_source_rows),
        "quotient91_divisor_row_count": len(quotient91_source_rows),
        "quotient77_centered_fiber_shadow_relative_error": (
            coefficient_error),
        "quotient91_recombined_source_relative_l2": (
            quotient91_relative_l2),
        "central_unit_threshold": 40,
        "central_unit_threshold_reason": (
            "if N>=40 and N/3<p<2N/3, then p and N-p exceed 13, "
            "so central prime pairs are units modulo 130"),
        "target_correlation_identity": (
            "for every even N>=40, the strict-central quotient-77 centered "
            "unit correlation equals sum log(p)log(N-p)G_shadow(p mod 130)"
        ),
        "quotient77_centered_coefficient_identity_proved": bool(
            coefficient_error <= tolerance),
        "quotient91_recombined_source_cancels_symbolically": bool(
            quotient91_relative_l2 <= tolerance),
        "all_strict_central_targets_above_threshold_covered_by_identity": bool(
            coefficient_error <= tolerance),
        "endpoint_or_noncentral_terms_analyzed": False,
        "full_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def symbolic_principal_plus_centered_channel_receipt(
        tolerance=1e-12, rational_tolerance=1e-10, batch_size=32):
    """Split the quotient-77 channel into a constant plus fiber shadow.

    The principal component is a scalar multiple of the strict-central unit
    pair weight.  The centered component is the already identified lag-130
    fiber shadow.  This still describes only the strict-central quotient-77
    channel, not endpoints or the full formal signed error.
    """
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    if not math.isfinite(rational_tolerance) or rational_tolerance < 0:
        raise ValueError("rational_tolerance must be finite and nonnegative")
    centered = symbolic_centered_outer_fiber_shadow_receipt(
        tolerance=tolerance, batch_size=batch_size)
    centering = linked_prime_centering_receipt(
        tolerance=tolerance, batch_size=batch_size)
    first_target = centering["targets"][0]
    common = centered["common_modulus"]
    period = centered["arithmetic_period"]
    left_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[1])[2]
    source_units, source_values_tuple = _direct_resonant_source_on_units(
        period, 130, left_sources, right_sources)
    quotient77_source_rows = tuple(
        row for (quotient, _, target), row in centering["rows"].items()
        if quotient == 77 and target == first_target)
    units130 = tuple(int(unit) for unit in quotient77_source_rows[0][
        "unit_residues"])
    quotient77_source = sum((
        row["additive_unit_source_values"] for row in quotient77_source_rows),
        np.zeros_like(quotient77_source_rows[0][
            "additive_unit_source_values"]))
    principal_constant = complex(np.mean(quotient77_source))

    source_values = {
        residue: value
        for residue, value in zip(source_units, source_values_tuple)}
    fiber_sums = np.asarray(tuple(
        _complex_fsum(source_values[unit] for unit in source_units
                      if unit % common == residue)
        for residue in units130), dtype=np.complex128)
    fiber_shadow = -(fiber_sums - np.mean(fiber_sums))
    reconstructed_source = principal_constant + fiber_shadow
    source_scale = max(
        1.0, float(np.linalg.norm(quotient77_source)),
        float(np.linalg.norm(reconstructed_source)))
    source_decomposition_error = float(
        np.linalg.norm(quotient77_source - reconstructed_source)
        / source_scale)
    constant_rational = (-3143, 16)
    rational_constant_error = abs(
        principal_constant - constant_rational[0] / constant_rational[1])
    return {
        "families": CANONICAL_FAMILIES,
        "arithmetic_period": period,
        "common_modulus": common,
        "unit_group_order": len(units130),
        "principal_constant": principal_constant,
        "principal_constant_rational_witness": constant_rational,
        "principal_constant_rational_error": rational_constant_error,
        "principal_constant_rational_tolerance": rational_tolerance,
        "quotient77_source_equals_constant_plus_fiber_shadow_error": (
            source_decomposition_error),
        "centered_bridge_receipt": centered,
        "strict_central_channel_formula": (
            "direct_q77(N)=c0*W_unit(N)+"
            "sum_(N/3<p<2N/3)log(p)log(N-p)G_shadow(p mod 130)"
        ),
        "central_unit_threshold": centered["central_unit_threshold"],
        "principal_constant_channel_identified": bool(
            source_decomposition_error <= tolerance
            and rational_constant_error <= rational_tolerance),
        "centered_channel_identified": bool(
            centered[
                "quotient77_centered_coefficient_identity_proved"]),
        "strict_central_quotient77_channel_identified_for_N_ge_40": bool(
            source_decomposition_error <= tolerance
            and centered[
                "quotient77_centered_coefficient_identity_proved"]),
        "endpoint_or_noncentral_terms_analyzed": False,
        "full_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


if __name__ == "__main__":
    print(even_even_goldbach_transfer_receipt())
