"""Exact Goldbach-sum form of the dominant even-even CRT numerator.

This module isolates an algebraic transfer.  It does not assert a mean-square
estimate for the resulting twisted Goldbach sums.
"""

import math
from functools import lru_cache
from fractions import Fraction

import numpy as np

from lcm_sawtooth_cotangent_count import _one_orientation_count_source_modes
from lcm_sawtooth_cotangent_transform import (
    _primitive_cotangent_transform_formula,
)
from lcm_sawtooth_frequency_resolved_fourier import (
    CANONICAL_FAMILIES,
    CANONICAL_LAGS,
    _partial_fourier_frequency_totals,
    _primitive_quadratic_character_fits,
    _unit_character_table,
)
from lcm_sawtooth_linked_prime_character import (
    linked_prime_centering_receipt,
    _linked_prime_character_row,
    _linked_prime_pairs,
    _prime_table,
    recombined_centered_character_receipt,
    residue_orbit_even_even_profile_receipt,
)
from lcm_sawtooth_projected_fourier_cancellation import (
    TWO_PRIME_QUOTIENT_LAGS,
    _family_transform_factors,
    two_prime_projected_fourier_holdout_receipt,
)
from lcm_sawtooth_ramanujan_class_mean import _ramanujan_sum


def _complex_fsum(values):
    values = tuple(values)
    return complex(
        math.fsum(value.real for value in values),
        math.fsum(value.imag for value in values))



def _largest_prime_factor(value):
    if type(value) is not int or value < 2:
        raise ValueError("value must be an integer at least two")
    remaining = value
    largest = None
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            largest = divisor
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1 if divisor == 2 else 2
    if remaining > 1:
        largest = remaining
    return largest


def _even_strict_central_unit_threshold(modulus):
    largest_factor = _largest_prime_factor(modulus)
    threshold = 3 * largest_factor + 1
    return threshold if threshold % 2 == 0 else threshold + 1


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



def count_four_outer_holdout_sector_receipt(
        minimum_nonzero_quotient=0.0, tolerance=1e-12):
    """Classify what the principal-plus-shadow channel does not cover.

    The reviewed strict-central bridge identifies the quotient-77 channel and
    the symbolic centered receipt explains the quotient-91 cancellation in the
    linked-prime slice.  The older count-four source table has six quotient
    sectors.  This receipt tests whether the remaining full-assembly gap can be
    treated as only endpoint/noncentral bookkeeping inside that slice.  It
    cannot: four holdout quotient sectors are live in the projected source
    table, so they need their own bridge or estimate.
    """
    if (not math.isfinite(minimum_nonzero_quotient)
            or minimum_nonzero_quotient < 0):
        raise ValueError(
            "minimum_nonzero_quotient must be finite and nonnegative")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    projected = two_prime_projected_fourier_holdout_receipt(
        tolerance=tolerance)
    discovery_quotients = tuple(projected["discovery_quotients"])
    holdout_quotients = tuple(projected["holdout_quotients"])
    if discovery_quotients != (77, 91):
        raise AssertionError("expected linked-prime discovery quotients 77,91")
    if set(projected["quotients"]) != set(TWO_PRIME_QUOTIENT_LAGS):
        raise AssertionError("projected quotient table changed")
    holdout_rows = {
        quotient: {
            "lag": TWO_PRIME_QUOTIENT_LAGS[quotient],
            "fourier_cancellation_quotient": (
                projected["fourier_cancellation_quotients"][quotient]),
            "count_four_recombination_quotient": (
                projected["count_four_recombination_quotients"][quotient]),
        }
        for quotient in holdout_quotients}
    live_holdouts = tuple(
        quotient for quotient, row in holdout_rows.items()
        if (row["fourier_cancellation_quotient"]
            > minimum_nonzero_quotient)
        and (row["count_four_recombination_quotient"]
             > minimum_nonzero_quotient))
    return {
        "families": projected["families"],
        "arithmetic_period": projected["arithmetic_period"],
        "all_count_four_quotients": projected["quotients"],
        "linked_prime_slice_quotients": discovery_quotients,
        "strict_central_principal_plus_shadow_quotient": 77,
        "linked_slice_cancelling_quotient": 91,
        "holdout_quotients": holdout_quotients,
        "holdout_rows": holdout_rows,
        "live_holdout_quotients": live_holdouts,
        "minimum_nonzero_quotient": minimum_nonzero_quotient,
        "all_projected_fourier_identities_pass": projected[
            "all_projected_fourier_identities_pass"],
        "holdout_spearman_correlation": projected[
            "holdout_spearman_correlation"],
        "all_six_spearman_correlation": projected[
            "all_six_spearman_correlation"],
        "all_holdout_count_four_sectors_are_live": bool(
            len(live_holdouts) == len(holdout_quotients)),
        "endpoint_only_residual_hypothesis_falsified": bool(
            len(live_holdouts) == len(holdout_quotients)),
        "full_outer_assembly_needs_holdout_sector_bridge": bool(
            len(live_holdouts) == len(holdout_quotients)),
        "full_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "pointwise_signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }



def holdout_lag_fiber_shadow_candidate_receipt(
        quotient=65, tolerance=1e-12):
    """Build the first fiber-shadow data for a live count-four holdout.

    This does not connect the holdout to the original outer assembly.  It only
    tests whether the direct full-period source has a nontrivial fixed residue
    shadow over the holdout's common modulus and whether strict-central prime
    pairs are units above an explicit small threshold.
    """
    if quotient not in TWO_PRIME_QUOTIENT_LAGS:
        raise ValueError("quotient must be one of the two-prime sectors")
    if quotient in (77, 91):
        raise ValueError("use a holdout quotient, not the linked-prime slice")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    period = math.lcm(
        CANONICAL_FAMILIES[0][0], 2 * CANONICAL_FAMILIES[0][1])
    lag = TWO_PRIME_QUOTIENT_LAGS[quotient]
    common = math.gcd(lag, period)
    if period // common != quotient:
        raise AssertionError("quotient-to-lag map is inconsistent")
    left_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[1])[2]
    source_units, source_values_tuple = _direct_resonant_source_on_units(
        period, lag, left_sources, right_sources)
    common_units = tuple(
        residue for residue in range(common)
        if math.gcd(residue, common) == 1)
    units_by_common_residue = {
        residue: tuple(unit for unit in source_units if unit % common == residue)
        for residue in common_units}
    fiber_counts = tuple(
        len(fiber) for fiber in units_by_common_residue.values())
    if len(set(fiber_counts)) != 1:
        raise AssertionError("unit fibers over the holdout common modulus vary")
    source_values = {
        residue: value
        for residue, value in zip(source_units, source_values_tuple)}
    fiber_sums = np.asarray(tuple(
        _complex_fsum(source_values[unit]
                      for unit in units_by_common_residue[residue])
        for residue in common_units), dtype=np.complex128)
    fiber_mean = complex(np.mean(fiber_sums))
    centered_fiber_sums = fiber_sums - fiber_mean
    fiber_shadow = -centered_fiber_sums
    centered_l2 = float(np.linalg.norm(centered_fiber_sums))
    fiber_l2 = float(np.linalg.norm(fiber_sums))
    max_centered_abs = float(np.max(np.abs(centered_fiber_sums)))
    max_internal_spread = 0.0
    for residue in common_units:
        fiber_values = np.asarray(tuple(
            source_values[unit]
            for unit in units_by_common_residue[residue]),
            dtype=np.complex128)
        max_internal_spread = max(
            max_internal_spread,
            float(np.max(np.abs(fiber_values - np.mean(fiber_values)))))
    descent_scale = max(1.0, max_internal_spread)
    threshold = _even_strict_central_unit_threshold(common)
    return {
        "families": CANONICAL_FAMILIES,
        "arithmetic_period": period,
        "quotient": quotient,
        "lag": lag,
        "common_modulus": common,
        "unit_group_order": len(common_units),
        "fiber_size_over_common_modulus": fiber_counts[0],
        "fiber_sum_mean": fiber_mean,
        "centered_fiber_sum_l2": centered_l2,
        "fiber_sum_l2": fiber_l2,
        "centered_to_total_fiber_l2_ratio": (
            centered_l2 / fiber_l2 if fiber_l2 else 0.0),
        "maximum_centered_fiber_sum_absolute_value": max_centered_abs,
        "maximum_internal_fiber_point_spread": max_internal_spread,
        "pointwise_descent_relative_witness": (
            max_internal_spread / descent_scale),
        "direct_source_pointwise_descends_to_common_modulus": bool(
            max_internal_spread <= tolerance),
        "fiber_shadow_sign_convention": (
            "negative centered fiber sum, matching the q77 convention"),
        "fiber_shadow_values": tuple(complex(value) for value in fiber_shadow),
        "central_unit_threshold": threshold,
        "central_unit_threshold_reason": (
            f"if N>={threshold} and N/3<p<2N/3, then p and N-p exceed "
            f"the largest prime factor {_largest_prime_factor(common)} "
            f"of modulus {common}"),
        "nonzero_fiber_shadow_candidate_available": bool(
            centered_l2 > tolerance),
        "linked_prime_or_outer_row_bridge_proved": False,
        "full_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "pointwise_signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }



def holdout_q65_active_row_bridge_receipt(
        targets=(1000, 1002), tolerance=1e-12,
        cancellation_tolerance=1e-10, batch_size=32):
    """Test and falsify the q77-style active-row bridge for q65.

    The q65 full-period source has a nonzero fiber shadow, but the active
    primitive-divisor rows selected by the linked-prime character machinery
    recombine to zero on ``U_154``.  This blocks only this exact bridge family;
    it does not rule out another count-four sector row or a different
    arithmetic estimate for q65.
    """
    targets = tuple(targets)
    if (not targets or any(type(target) is not int or target < 34
                           or target % 2 for target in targets)):
        raise ValueError("targets must be even integers at least 34")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    if (not math.isfinite(cancellation_tolerance)
            or cancellation_tolerance < 0):
        raise ValueError(
            "cancellation_tolerance must be finite and nonnegative")
    period = math.lcm(
        CANONICAL_FAMILIES[0][0], 2 * CANONICAL_FAMILIES[0][1])
    quotient = 65
    lag = TWO_PRIME_QUOTIENT_LAGS[quotient]
    common = math.gcd(lag, period)
    left_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[1])[2]
    frequencies, _, _, divisor_strata, _ = _partial_fourier_frequency_totals(
        period, lag, left_sources, right_sources, batch_size)
    fits = _primitive_quadratic_character_fits(
        frequencies, common, quotient, divisor_strata, tolerance)
    active_divisors = tuple(fits["active_divisors"])
    row_sets = {}
    recombined_sources = {}
    centered_correlations = {}
    for target in targets:
        rows = tuple(
            _linked_prime_character_row(
                common, quotient, frequencies, divisor_strata[divisor],
                target, target // 3, target - target // 3, tolerance)
            for divisor in active_divisors)
        row_sets[target] = rows
        recombined_sources[target] = sum(
            (row["additive_unit_source_values"] for row in rows),
            np.zeros_like(rows[0]["additive_unit_source_values"]))
        centered_correlations[target] = _complex_fsum(
            row["centered_source_linked_prime_correlation"]
            for row in rows)
    first_target = targets[0]
    units = tuple(int(unit) for unit in row_sets[first_target][0][
        "unit_residues"])
    common_units = tuple(
        residue for residue in range(common)
        if math.gcd(residue, common) == 1)
    if units != common_units:
        raise AssertionError("q65 row units are not ordered U_154 residues")
    recombined_source = recombined_sources[first_target]
    recombined_centered = recombined_source - np.mean(recombined_source)
    candidate = holdout_lag_fiber_shadow_candidate_receipt(
        quotient=quotient, tolerance=tolerance)
    fiber_shadow = np.asarray(candidate["fiber_shadow_values"],
                              dtype=np.complex128)
    source_l2 = float(np.linalg.norm(recombined_centered))
    shadow_l2 = float(np.linalg.norm(fiber_shadow))
    scale = max(1.0, source_l2, shadow_l2)
    same_sign_error = float(
        np.linalg.norm(recombined_centered - fiber_shadow) / scale)
    opposite_sign_error = float(
        np.linalg.norm(recombined_centered + fiber_shadow) / scale)
    denominator = np.vdot(fiber_shadow, fiber_shadow)
    best_scalar = (
        np.vdot(fiber_shadow, recombined_centered) / denominator
        if abs(denominator) else 0.0j)
    target_source_spread = max(
        float(np.linalg.norm(recombined_sources[target] - recombined_source))
        / max(1.0, float(np.linalg.norm(recombined_sources[target])),
              float(np.linalg.norm(recombined_source)))
        for target in targets)
    return {
        "families": CANONICAL_FAMILIES,
        "arithmetic_period": period,
        "quotient": quotient,
        "lag": lag,
        "common_modulus": common,
        "targets": targets,
        "active_divisors": active_divisors,
        "unit_group_order": len(units),
        "recombined_active_source_l2": source_l2,
        "fiber_shadow_l2": shadow_l2,
        "active_source_to_fiber_shadow_l2_ratio": (
            source_l2 / shadow_l2 if shadow_l2 else math.inf),
        "active_source_cancellation_tolerance": cancellation_tolerance,
        "same_sign_shadow_match_relative_error": same_sign_error,
        "opposite_sign_shadow_match_relative_error": opposite_sign_error,
        "best_scalar_to_fiber_shadow": complex(best_scalar),
        "maximum_target_source_vector_spread": target_source_spread,
        "centered_correlations": centered_correlations,
        "active_recombined_source_cancels": bool(
            source_l2 <= cancellation_tolerance),
        "active_row_bridge_matches_nonzero_fiber_shadow": False,
        "q65_active_linked_row_bridge_falsified": bool(
            source_l2 <= cancellation_tolerance and shadow_l2 > 1.0
            and min(same_sign_error, opposite_sign_error) > .9),
        "preserved_component": (
            "q65 nonzero fiber shadow remains available for a different "
            "count-four sector bridge"),
        "alternative_count_four_sector_bridge_ruled_out": False,
        "full_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "pointwise_signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }



def holdout_projected_spatial_fiber_bridge_receipt(
        quotient=65, tolerance=1e-12):
    """Identify a holdout fiber shadow in the projected-Fourier spatial layer.

    The active linked-prime rows cancel for q65, but the projected-Fourier
    holdout source is naturally indexed by spatial frequencies.  Grouping those
    spatial frequencies by residue modulo the holdout common modulus and
    centering tests whether the sector has a centered fiber-shadow vector.
    This is a source identity only; it is not yet a target prime-pair bridge
    or signed estimate.
    """
    if quotient not in TWO_PRIME_QUOTIENT_LAGS:
        raise ValueError("quotient must be one of the two-prime sectors")
    if quotient in (77, 91):
        raise ValueError("use a holdout quotient, not the linked-prime slice")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    period = math.lcm(
        CANONICAL_FAMILIES[0][0], 2 * CANONICAL_FAMILIES[0][1])
    lag = TWO_PRIME_QUOTIENT_LAGS[quotient]
    common = math.gcd(lag, period)
    quotient_weights = np.asarray(tuple(
        _ramanujan_sum(quotient, frequency)
        for frequency in range(period)), dtype=np.float64)
    left_table, left_negative_partner = _family_transform_factors(
        period, *CANONICAL_FAMILIES[0])
    right_table, right_negative_partner = _family_transform_factors(
        period, *CANONICAL_FAMILIES[1])
    spatial_frequencies = tuple(
        frequency for frequency in range(period)
        if math.gcd(frequency, common) == 1)
    scale_factor = common / (period * period)
    signed_by_spatial_frequency = []
    absolute_by_spatial_frequency = []
    for spatial_frequency in spatial_frequencies:
        left_transform = -.25 * (
            (np.roll(left_table, -spatial_frequency) - left_table)
            * (np.roll(left_negative_partner, -spatial_frequency)
               - left_negative_partner))
        right_transform = -.25 * (
            (np.roll(right_table, -spatial_frequency) - right_table)
            * (np.roll(right_negative_partner, -spatial_frequency)
               - right_negative_partner))
        summands = (
            scale_factor * quotient_weights * left_transform
            * right_transform)
        signed_by_spatial_frequency.append(float(np.sum(summands)))
        absolute_by_spatial_frequency.append(float(np.sum(np.abs(summands))))
    common_units = tuple(
        residue for residue in range(common)
        if math.gcd(residue, common) == 1)
    grouped_spatial_values = np.asarray(tuple(
        math.fsum(
            value for value, spatial_frequency
            in zip(signed_by_spatial_frequency, spatial_frequencies)
            if spatial_frequency % common == residue)
        for residue in common_units), dtype=np.float64)
    grouped_spatial_mean = float(np.mean(grouped_spatial_values))
    grouped_centered = grouped_spatial_values - grouped_spatial_mean
    candidate = holdout_lag_fiber_shadow_candidate_receipt(
        quotient=quotient, tolerance=tolerance)
    fiber_shadow = np.asarray(candidate["fiber_shadow_values"],
                              dtype=np.complex128)
    grouped_l2 = float(np.linalg.norm(grouped_centered))
    shadow_l2 = float(np.linalg.norm(fiber_shadow))
    comparison_scale = max(1.0, grouped_l2, shadow_l2)
    same_sign_error = float(
        np.linalg.norm(grouped_centered - fiber_shadow) / comparison_scale)
    opposite_sign_error = float(
        np.linalg.norm(grouped_centered + fiber_shadow) / comparison_scale)
    best_scalar = np.vdot(fiber_shadow, grouped_centered) / np.vdot(
        fiber_shadow, fiber_shadow)
    signed_total = math.fsum(signed_by_spatial_frequency)
    absolute_mass = math.fsum(absolute_by_spatial_frequency)
    return {
        "families": CANONICAL_FAMILIES,
        "arithmetic_period": period,
        "quotient": quotient,
        "lag": lag,
        "common_modulus": common,
        "spatial_frequency_count": len(spatial_frequencies),
        "unit_group_order": len(common_units),
        "grouped_spatial_sum": float(np.sum(grouped_spatial_values)),
        "grouped_spatial_mean": grouped_spatial_mean,
        "maximum_grouped_spatial_centered_absolute_value": float(
            np.max(np.abs(grouped_centered))),
        "projected_signed_total": signed_total,
        "projected_absolute_mass": absolute_mass,
        "projected_cancellation_quotient": (
            abs(signed_total) / absolute_mass if absolute_mass else None),
        "grouped_centered_spatial_values": tuple(
            float(value) for value in grouped_centered),
        "grouped_centered_spatial_l2": grouped_l2,
        "fiber_shadow_l2": shadow_l2,
        "same_sign_fiber_shadow_relative_error": same_sign_error,
        "opposite_sign_fiber_shadow_relative_error": opposite_sign_error,
        "best_scalar_to_fiber_shadow": complex(best_scalar),
        "projected_spatial_grouping_equals_negative_fiber_shadow": bool(
            opposite_sign_error <= tolerance),
        "active_linked_row_bridge_was_wrong_layer": True,
        "linked_prime_or_target_prime_pair_bridge_proved": False,
        "full_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "pointwise_signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def holdout_q55_projected_principal_channel_receipt(
        targets=(1000, 1002), tolerance=1e-9):
    """Identify q55 as a projected-spatial principal channel.

    Unlike q65, q55 has no material centered spatial shadow at this scale.  Its
    grouped spatial values are constant over ``U_182``.  The induced
    prime-residue coefficient is therefore that constant times the Ramanujan
    sum over unit spatial frequencies, which is fixed for unit prime residues.
    """
    targets = tuple(targets)
    if (not targets or any(type(target) is not int or target < 40
                           or target % 2 for target in targets)):
        raise ValueError("targets must be even integers at least 40")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    quotient = 55
    source = holdout_projected_spatial_fiber_bridge_receipt(
        quotient=quotient, tolerance=1e-12)
    common = source["common_modulus"]
    residues = tuple(
        residue for residue in range(common)
        if math.gcd(residue, common) == 1)
    constant_spatial_value = source["grouped_spatial_mean"]
    ramanujan_values = tuple(_ramanujan_sum(common, residue)
                             for residue in residues)
    if len(set(ramanujan_values)) != 1:
        raise AssertionError("unit Ramanujan values are not constant")
    principal_coefficient = constant_spatial_value * ramanujan_values[0]
    rows = {}
    maximum_target_relative_error = 0.0
    all_nonunit_pairs = []
    for target in targets:
        lower = target // 3
        upper = target - lower
        unit_weight = 0.0
        nonunit_pairs = []
        pair_count = 0
        exponential_sums = {residue: 0.0j for residue in residues}
        for prime, weight in _linked_prime_pairs(target, lower, upper):
            partner = target - prime
            pair_count += 1
            prime_residue = prime % common
            if math.gcd(prime_residue, common) != 1:
                nonunit_pairs.append((prime, partner))
                continue
            unit_weight += weight
            for residue in residues:
                exponential_sums[residue] += (
                    np.exp(2j * np.pi * residue * prime_residue / common)
                    * weight)
        principal_sum = principal_coefficient * unit_weight
        spatial_sum = _complex_fsum(
            constant_spatial_value * value
            for value in exponential_sums.values())
        scale = max(1.0, abs(principal_sum), abs(spatial_sum))
        relative_error = abs(principal_sum - spatial_sum) / scale
        maximum_target_relative_error = max(
            maximum_target_relative_error, relative_error)
        all_nonunit_pairs.extend((target, pair) for pair in nonunit_pairs)
        rows[target] = {
            "strict_central_interval": (lower, upper),
            "ordered_central_prime_pair_count": pair_count,
            "nonunit_prime_pairs": tuple(nonunit_pairs),
            "strict_central_unit_weight": unit_weight,
            "principal_prime_residue_sum": complex(principal_sum),
            "spatial_frequency_reconstructed_sum": complex(spatial_sum),
            "principal_spatial_relative_error": relative_error,
        }
    return {
        "families": source["families"],
        "arithmetic_period": source["arithmetic_period"],
        "quotient": quotient,
        "lag": source["lag"],
        "common_modulus": common,
        "unit_group_order": len(residues),
        "spatial_frequency_count": source["spatial_frequency_count"],
        "projected_signed_total": source["projected_signed_total"],
        "projected_absolute_mass": source["projected_absolute_mass"],
        "projected_cancellation_quotient": (
            source["projected_cancellation_quotient"]),
        "constant_grouped_spatial_value": constant_spatial_value,
        "maximum_centered_grouped_spatial_absolute_value": (
            source["maximum_grouped_spatial_centered_absolute_value"]),
        "centered_grouped_spatial_l2": source["grouped_centered_spatial_l2"],
        "ramanujan_unit_value": ramanujan_values[0],
        "principal_prime_residue_coefficient": principal_coefficient,
        "central_unit_threshold": _even_strict_central_unit_threshold(common),
        "rows": rows,
        "maximum_target_relative_error": maximum_target_relative_error,
        "nonunit_prime_pairs": tuple(all_nonunit_pairs),
        "q55_centered_shadow_cancels": bool(
            source["grouped_centered_spatial_l2"] <= tolerance),
        "q55_principal_channel_identified": bool(
            source["grouped_centered_spatial_l2"] <= tolerance
            and not all_nonunit_pairs
            and maximum_target_relative_error <= tolerance),
        "target_prime_pair_bridge_proved_symbolically": False,
        "full_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "pointwise_signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def holdout_q65_projected_spatial_fiber_bridge_receipt(tolerance=1e-12):
    return holdout_projected_spatial_fiber_bridge_receipt(
        quotient=65, tolerance=tolerance)


def holdout_naive_spatial_prime_coefficient_receipt(
        quotient=65, tolerance=1e-12):
    """Test whether holdout spatial values are prime-residue coefficients.

    The projected-spatial bridge identifies a fixed source vector indexed by
    spatial frequency residue modulo 154.  A tempting shortcut is to use that
    same vector directly as a coefficient on prime residues.  The actual
    residue coefficient obtained from a spatial source is its finite Fourier
    dual, so this receipt compares the naive same-index vector against that
    dual coefficient vector up to scalar normalization.
    """
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    source = holdout_projected_spatial_fiber_bridge_receipt(
        quotient=quotient, tolerance=tolerance)
    common = source["common_modulus"]
    residues = tuple(
        residue for residue in range(common)
        if math.gcd(residue, common) == 1)
    naive = np.asarray(source["grouped_centered_spatial_values"],
                       dtype=np.complex128)
    if len(residues) != len(naive):
        raise AssertionError("spatial vector and U_154 ordering disagree")
    phase = np.exp(
        2j * np.pi * np.outer(residues, residues) / common)
    dual = phase @ naive
    naive_l2 = float(np.linalg.norm(naive))
    dual_l2 = float(np.linalg.norm(dual))
    comparison_scale = max(1.0, naive_l2, dual_l2)
    same_index_error = float(np.linalg.norm(naive - dual) / comparison_scale)
    opposite_index_error = float(
        np.linalg.norm(naive + dual) / comparison_scale)
    scalar_denominator = np.vdot(dual, dual)
    best_scalar = (
        np.vdot(dual, naive) / scalar_denominator
        if abs(scalar_denominator) else 0.0j)
    best_scalar_error = float(
        np.linalg.norm(naive - best_scalar * dual)
        / max(1.0, naive_l2))
    return {
        "families": source["families"],
        "arithmetic_period": source["arithmetic_period"],
        "quotient": source["quotient"],
        "lag": source["lag"],
        "common_modulus": common,
        "unit_group_order": len(residues),
        "naive_spatial_prime_coefficient_l2": naive_l2,
        "fourier_dual_prime_coefficient_l2": dual_l2,
        "same_index_relative_error": same_index_error,
        "opposite_index_relative_error": opposite_index_error,
        "best_scalar_dual_to_naive": complex(best_scalar),
        "best_scalar_dual_to_naive_relative_error": best_scalar_error,
        "naive_spatial_is_fourier_dual_prime_coefficient": bool(
            best_scalar_error <= tolerance),
        "naive_same_index_prime_coefficient_falsified": bool(
            best_scalar_error > .1),
        "preserved_component": (
            "q65 projected-spatial source identity remains available; "
            "only the direct same-index prime-residue shortcut is blocked"),
        "target_prime_pair_bridge_proved": False,
        "full_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "pointwise_signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def holdout_q65_naive_spatial_prime_coefficient_receipt(tolerance=1e-12):
    return holdout_naive_spatial_prime_coefficient_receipt(
        quotient=65, tolerance=tolerance)


def holdout_dual_prime_target_sum_receipt(
        quotient=65, targets=(1000, 1002), tolerance=1e-12):
    """Transfer a centered holdout spatial source to target prime sums.

    This is still a finite target check, not an estimate.  It compares the
    tempting same-index coefficient against the Fourier-dual coefficient that
    a centered spatial-frequency source actually induces on prime residues.
    """
    targets = tuple(targets)
    if (not targets or any(type(target) is not int or target < 34
                           or target % 2 for target in targets)):
        raise ValueError("targets must be even integers at least 34")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    source = holdout_projected_spatial_fiber_bridge_receipt(
        quotient=quotient, tolerance=tolerance)
    common = source["common_modulus"]
    residues = tuple(
        residue for residue in range(common)
        if math.gcd(residue, common) == 1)
    spatial = np.asarray(source["grouped_centered_spatial_values"],
                         dtype=np.complex128)
    phase = np.exp(
        2j * np.pi * np.outer(residues, residues) / common)
    dual = phase @ spatial
    naive_by_residue = {
        residue: value for residue, value in zip(residues, spatial)}
    dual_by_residue = {
        residue: value for residue, value in zip(residues, dual)}

    rows = {}
    maximum_spatial_dual_relative_error = 0.0
    minimum_naive_dual_relative_error = math.inf
    all_nonunit_pairs = []
    for target in targets:
        lower = target // 3
        upper = target - lower
        naive_sum = 0.0j
        dual_sum = 0.0j
        spatial_sum = 0.0j
        natural_scale = 0.0
        nonunit_pairs = []
        pair_count = 0
        exponential_sums = {residue: 0.0j for residue in residues}
        for prime, weight in _linked_prime_pairs(target, lower, upper):
            partner = target - prime
            pair_count += 1
            prime_residue = prime % common
            if math.gcd(prime_residue, common) != 1:
                nonunit_pairs.append((prime, partner))
                continue
            naive_coefficient = naive_by_residue[prime_residue]
            dual_coefficient = dual_by_residue[prime_residue]
            naive_sum += naive_coefficient * weight
            dual_sum += dual_coefficient * weight
            natural_scale += abs(dual_coefficient * weight)
            for residue in residues:
                exponential_sums[residue] += (
                    np.exp(2j * np.pi * residue * prime_residue / common)
                    * weight)
        for residue, value in zip(residues, spatial):
            spatial_sum += value * exponential_sums[residue]
        scale = max(1.0, abs(spatial_sum), abs(dual_sum), natural_scale)
        spatial_dual_error = abs(spatial_sum - dual_sum) / scale
        naive_dual_scale = max(1.0, abs(naive_sum), abs(dual_sum))
        naive_dual_error = abs(naive_sum - dual_sum) / naive_dual_scale
        maximum_spatial_dual_relative_error = max(
            maximum_spatial_dual_relative_error, spatial_dual_error)
        minimum_naive_dual_relative_error = min(
            minimum_naive_dual_relative_error, naive_dual_error)
        all_nonunit_pairs.extend((target, pair) for pair in nonunit_pairs)
        rows[target] = {
            "strict_central_interval": (lower, upper),
            "ordered_central_prime_pair_count": pair_count,
            "nonunit_prime_pairs": tuple(nonunit_pairs),
            "naive_same_index_prime_residue_sum": complex(naive_sum),
            "fourier_dual_prime_residue_sum": complex(dual_sum),
            "spatial_frequency_reconstructed_sum": complex(spatial_sum),
            "spatial_dual_relative_error": spatial_dual_error,
            "naive_dual_relative_error": naive_dual_error,
            "dual_natural_scale": natural_scale,
        }
    return {
        "families": source["families"],
        "arithmetic_period": source["arithmetic_period"],
        "quotient": source["quotient"],
        "lag": source["lag"],
        "common_modulus": common,
        "targets": targets,
        "unit_group_order": len(residues),
        "central_unit_threshold": _even_strict_central_unit_threshold(common),
        "rows": rows,
        "maximum_spatial_dual_relative_error": (
            maximum_spatial_dual_relative_error),
        "minimum_naive_dual_relative_error": minimum_naive_dual_relative_error,
        "nonunit_prime_pairs": tuple(all_nonunit_pairs),
        "spatial_to_dual_target_transfer_verified_on_targets": bool(
            not all_nonunit_pairs
            and maximum_spatial_dual_relative_error <= tolerance),
        "naive_same_index_target_transfer_falsified": bool(
            minimum_naive_dual_relative_error > .1),
        "centered_component_only": True,
        "full_projected_spatial_action_included": False,
        "target_prime_pair_bridge_proved_symbolically": False,
        "full_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "pointwise_signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def holdout_q65_dual_prime_target_sum_receipt(
        targets=(1000, 1002), tolerance=1e-12):
    return holdout_dual_prime_target_sum_receipt(
        quotient=65, targets=targets, tolerance=tolerance)


def symbolic_holdout_dual_prime_coefficient_receipt(
        quotient=65, tolerance=1e-12):
    """Name the fixed centered Fourier-dual coefficient for central targets.

    Once the projected-spatial holdout source is grouped over its common unit
    group and centered, its action on a prime residue is the finite additive
    Fourier dual of that grouped centered spatial vector.  This coefficient is
    independent of the target.  The principal mean is handled separately.
    """
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    source = holdout_projected_spatial_fiber_bridge_receipt(
        quotient=quotient, tolerance=tolerance)
    common = source["common_modulus"]
    residues = tuple(
        residue for residue in range(common)
        if math.gcd(residue, common) == 1)
    spatial = np.asarray(source["grouped_centered_spatial_values"],
                         dtype=np.complex128)
    phase = np.exp(
        2j * np.pi * np.outer(residues, residues) / common)
    dual = phase @ spatial
    threshold = _even_strict_central_unit_threshold(common)
    coefficient_by_residue = {
        residue: complex(value) for residue, value in zip(residues, dual)}
    max_imaginary_part = max(abs(value.imag) for value in dual)
    return {
        "families": source["families"],
        "arithmetic_period": source["arithmetic_period"],
        "quotient": source["quotient"],
        "lag": source["lag"],
        "common_modulus": common,
        "unit_group_order": len(residues),
        "central_unit_threshold": threshold,
        "central_unit_threshold_reason": (
            f"if N>={threshold} and N/3<p<2N/3, then p and N-p exceed "
            f"the largest prime factor {_largest_prime_factor(common)} "
            f"of modulus {common}"),
        "spatial_source_l2": float(np.linalg.norm(spatial)),
        "fourier_dual_prime_coefficient_l2": float(np.linalg.norm(dual)),
        "maximum_dual_coefficient_imaginary_part": float(max_imaginary_part),
        "coefficient_by_unit_residue": coefficient_by_residue,
        "target_correlation_identity": (
            "for every even N above the central-unit threshold, the centered "
            "holdout projected-spatial target action on strict-central prime "
            "pairs is sum log(p)log(N-p)C_q(p mod common), where C_q is the "
            "fixed Fourier-dual coefficient"),
        "coefficient_depends_on_target_residue": False,
        "nonunit_central_prime_pair_correction_needed_for_N_ge_34": False,
        "symbolic_q65_dual_coefficient_transfer_proved": True,
        "q65_source_layer_bridge_proved": True,
        "centered_component_only": True,
        "principal_mean_component_included": False,
        "q65_positive_or_signed_estimate_proved": False,
        "full_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "pointwise_signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def symbolic_q65_dual_prime_coefficient_receipt(tolerance=1e-12):
    return symbolic_holdout_dual_prime_coefficient_receipt(
        quotient=65, tolerance=tolerance)


def holdout_full_projected_prime_coefficient_receipt(
        quotient=65, targets=(1000, 1002), tolerance=1e-9):
    """Transfer the full holdout projected-spatial source to prime residues.

    The full coefficient is a principal constant from the grouped spatial mean
    plus the finite Fourier dual of the grouped centered spatial vector.
    """
    targets = tuple(targets)
    if quotient not in TWO_PRIME_QUOTIENT_LAGS:
        raise ValueError("quotient must be one of the two-prime sectors")
    if quotient in (77, 91):
        raise ValueError("use a holdout quotient, not the linked-prime slice")
    if (not targets or any(type(target) is not int or target < 40
                           or target % 2 for target in targets)):
        raise ValueError("targets must be even integers at least 40")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    source = holdout_projected_spatial_fiber_bridge_receipt(
        quotient=quotient, tolerance=1e-12)
    common = source["common_modulus"]
    residues = tuple(
        residue for residue in range(common)
        if math.gcd(residue, common) == 1)
    centered = np.asarray(source["grouped_centered_spatial_values"],
                          dtype=np.complex128)
    raw_spatial = centered + source["grouped_spatial_mean"]
    phase = np.exp(
        2j * np.pi * np.outer(residues, residues) / common)
    centered_dual = phase @ centered
    ramanujan_values = tuple(_ramanujan_sum(common, residue)
                             for residue in residues)
    if len(set(ramanujan_values)) != 1:
        raise AssertionError("unit Ramanujan values are not constant")
    principal_coefficient = (
        source["grouped_spatial_mean"] * ramanujan_values[0])
    full_coefficient = centered_dual + principal_coefficient
    coefficient_by_residue = {
        residue: complex(value)
        for residue, value in zip(residues, full_coefficient)}

    rows = {}
    maximum_target_relative_error = 0.0
    all_nonunit_pairs = []
    for target in targets:
        lower = target // 3
        upper = target - lower
        coefficient_sum = 0.0j
        spatial_sum = 0.0j
        natural_scale = 0.0
        nonunit_pairs = []
        pair_count = 0
        exponential_sums = {residue: 0.0j for residue in residues}
        for prime, weight in _linked_prime_pairs(target, lower, upper):
            partner = target - prime
            pair_count += 1
            prime_residue = prime % common
            if math.gcd(prime_residue, common) != 1:
                nonunit_pairs.append((prime, partner))
                continue
            coefficient = coefficient_by_residue[prime_residue]
            coefficient_sum += coefficient * weight
            natural_scale += abs(coefficient * weight)
            for residue in residues:
                exponential_sums[residue] += (
                    np.exp(2j * np.pi * residue * prime_residue / common)
                    * weight)
        for value, residue in zip(raw_spatial, residues):
            spatial_sum += value * exponential_sums[residue]
        scale = max(1.0, abs(coefficient_sum), abs(spatial_sum), natural_scale)
        relative_error = abs(coefficient_sum - spatial_sum) / scale
        maximum_target_relative_error = max(
            maximum_target_relative_error, relative_error)
        all_nonunit_pairs.extend((target, pair) for pair in nonunit_pairs)
        rows[target] = {
            "strict_central_interval": (lower, upper),
            "ordered_central_prime_pair_count": pair_count,
            "nonunit_prime_pairs": tuple(nonunit_pairs),
            "full_prime_residue_sum": complex(coefficient_sum),
            "spatial_frequency_reconstructed_sum": complex(spatial_sum),
            "full_target_relative_error": relative_error,
            "full_target_natural_scale": natural_scale,
        }
    threshold = _even_strict_central_unit_threshold(common)
    return {
        "families": source["families"],
        "arithmetic_period": source["arithmetic_period"],
        "quotient": quotient,
        "lag": source["lag"],
        "common_modulus": common,
        "unit_group_order": len(residues),
        "spatial_frequency_count": source["spatial_frequency_count"],
        "projected_signed_total": source["projected_signed_total"],
        "projected_absolute_mass": source["projected_absolute_mass"],
        "projected_cancellation_quotient": (
            source["projected_cancellation_quotient"]),
        "grouped_spatial_mean": source["grouped_spatial_mean"],
        "centered_spatial_l2": source["grouped_centered_spatial_l2"],
        "centered_dual_coefficient_l2": float(np.linalg.norm(centered_dual)),
        "principal_prime_residue_coefficient": principal_coefficient,
        "full_prime_residue_coefficient_l2": float(
            np.linalg.norm(full_coefficient)),
        "maximum_full_coefficient_imaginary_part": float(
            max(abs(value.imag) for value in full_coefficient)),
        "coefficient_by_unit_residue": coefficient_by_residue,
        "central_unit_threshold": threshold,
        "central_unit_threshold_reason": (
            f"if N>={threshold} and N/3<p<2N/3, then p and N-p exceed "
            f"the largest prime factor {_largest_prime_factor(common)} "
            f"of modulus {common}"),
        "rows": rows,
        "maximum_target_relative_error": maximum_target_relative_error,
        "nonunit_prime_pairs": tuple(all_nonunit_pairs),
        "full_projected_spatial_target_transfer_verified_on_targets": bool(
            not all_nonunit_pairs
            and maximum_target_relative_error <= tolerance),
        "coefficient_depends_on_target_residue": False,
        "positive_or_signed_estimate_proved": False,
        "full_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "pointwise_signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def holdout_q65_full_projected_prime_coefficient_receipt(
        targets=(1000, 1002), tolerance=1e-9):
    return holdout_full_projected_prime_coefficient_receipt(
        quotient=65, targets=targets, tolerance=tolerance)


def combined_fixed_strict_central_coefficient_receipt(tolerance=1e-9):
    """Assemble the fixed strict-central channels on ``U_10010``.

    The assembled family includes the reviewed q77 principal-plus-fiber-shadow
    channel and the four live holdout channels q35, q55, q65, and q143.  This
    is a coefficient bookkeeping receipt only.  It does not estimate the
    resulting signed prime-residue correlations.
    """
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    period = math.lcm(
        CANONICAL_FAMILIES[0][0], 2 * CANONICAL_FAMILIES[0][1])
    period_units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    left_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[1])[2]

    q77_common = 130
    q77_units = tuple(
        residue for residue in range(q77_common)
        if math.gcd(residue, q77_common) == 1)
    q77_source_units, q77_source_values_tuple = (
        _direct_resonant_source_on_units(
            period, TWO_PRIME_QUOTIENT_LAGS[77],
            left_sources, right_sources))
    q77_source_values = {
        residue: value
        for residue, value in zip(q77_source_units, q77_source_values_tuple)}
    q77_fiber_sums = np.asarray(tuple(
        _complex_fsum(q77_source_values[unit] for unit in q77_source_units
                      if unit % q77_common == residue)
        for residue in q77_units), dtype=np.complex128)
    q77_shadow = -(q77_fiber_sums - np.mean(q77_fiber_sums))
    q77_principal = complex(-3143 / 16)
    component_coefficients = {
        77: {
            "common_modulus": q77_common,
            "central_unit_threshold": 40,
            "principal_coefficient": q77_principal,
            "centered_l2": float(np.linalg.norm(q77_shadow)),
            "coefficient_by_residue": {
                residue: q77_principal + value
                for residue, value in zip(q77_units, q77_shadow)},
        }}
    for quotient in (35, 55, 65, 143):
        receipt = holdout_full_projected_prime_coefficient_receipt(
            quotient=quotient, tolerance=tolerance)
        coefficient_values = np.asarray(tuple(
            receipt["coefficient_by_unit_residue"][residue]
            for residue in sorted(receipt["coefficient_by_unit_residue"])),
            dtype=np.complex128)
        component_coefficients[quotient] = {
            "common_modulus": receipt["common_modulus"],
            "central_unit_threshold": receipt["central_unit_threshold"],
            "principal_coefficient": (
                receipt["principal_prime_residue_coefficient"]),
            "centered_l2": receipt["centered_dual_coefficient_l2"],
            "full_l2": receipt["full_prime_residue_coefficient_l2"],
            "coefficient_by_residue": (
                receipt["coefficient_by_unit_residue"]),
            "maximum_fixture_transfer_error": (
                receipt["maximum_target_relative_error"]),
            "lifted_unit_mean": complex(np.mean(coefficient_values)),
        }

    lifted_components = {}
    for quotient, component in component_coefficients.items():
        common = component["common_modulus"]
        coefficients = component["coefficient_by_residue"]
        lifted_components[quotient] = np.asarray(tuple(
            coefficients[unit % common] for unit in period_units),
            dtype=np.complex128)
    aggregate = sum(lifted_components.values())
    aggregate_mean = complex(np.mean(aggregate))
    aggregate_centered = aggregate - aggregate_mean
    component_centered_l2 = {
        quotient: float(np.linalg.norm(values - np.mean(values)))
        for quotient, values in lifted_components.items()}
    sum_component_centered_l2 = math.fsum(component_centered_l2.values())
    aggregate_centered_l2 = float(np.linalg.norm(aggregate_centered))
    cancellation_ratio = (
        aggregate_centered_l2 / sum_component_centered_l2
        if sum_component_centered_l2 else 0.0)
    expected_principal_mean = _complex_fsum(
        component["principal_coefficient"]
        for component in component_coefficients.values())
    mean_error = abs(aggregate_mean - expected_principal_mean) / max(
        1.0, abs(expected_principal_mean))
    maximum_holdout_fixture_error = max(
        component.get("maximum_fixture_transfer_error", 0.0)
        for component in component_coefficients.values())
    return {
        "families": CANONICAL_FAMILIES,
        "arithmetic_period": period,
        "unit_group_order": len(period_units),
        "assembled_quotients": (35, 55, 65, 77, 143),
        "component_summaries": {
            quotient: {
                key: value for key, value in component.items()
                if key != "coefficient_by_residue"}
            for quotient, component in component_coefficients.items()},
        "aggregate_principal_mean": aggregate_mean,
        "expected_principal_mean": expected_principal_mean,
        "principal_mean_relative_error": mean_error,
        "component_centered_l2": component_centered_l2,
        "sum_component_centered_l2": sum_component_centered_l2,
        "aggregate_centered_l2": aggregate_centered_l2,
        "centered_cancellation_ratio": cancellation_ratio,
        "maximum_holdout_fixture_transfer_error": (
            maximum_holdout_fixture_error),
        "aggregate_coefficient_by_unit_residue": {
            residue: complex(value)
            for residue, value in zip(period_units, aggregate)},
        "component_coefficient_by_residue": {
            quotient: {
                residue: complex(value)
                for residue, value
                in component["coefficient_by_residue"].items()}
            for quotient, component in component_coefficients.items()},
        "fixed_coefficient_family_assembled": bool(
            mean_error <= tolerance
            and maximum_holdout_fixture_error <= tolerance),
        "all_components_are_fixed_before_target": True,
        "signed_prime_correlation_estimate_proved": False,
        "full_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def combined_coefficient_character_spectrum_receipt(
        top_count=12, tolerance=1e-9):
    """Measure Dirichlet-character concentration of the assembled coefficient.

    This is a finite spectral diagnostic on the explicit ``U_10010``
    coefficient vector.  It does not supply a prime-sum estimate.
    """
    if type(top_count) is not int or top_count <= 0:
        raise ValueError("top_count must be a positive integer")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    values = np.asarray(tuple(
        coefficient["aggregate_coefficient_by_unit_residue"][unit]
        for unit in units), dtype=np.complex128)
    centered = values - np.mean(values)
    _, labels, character_table = _unit_character_table(period, units)
    character_coefficients = (
        np.conjugate(character_table) @ centered / len(units))
    reconstruction = character_table.T @ character_coefficients
    reconstruction_error = float(
        np.linalg.norm(reconstruction - centered)
        / max(1.0, float(np.linalg.norm(centered))))
    energies = np.abs(character_coefficients) ** 2
    total_energy = float(np.sum(energies))
    order = tuple(
        int(index) for index in np.argsort(energies)[::-1])
    selected = order[:min(top_count, len(order))]
    top_rows = tuple({
        "rank": rank + 1,
        "label": labels[index],
        "coefficient": complex(character_coefficients[index]),
        "energy": float(energies[index]),
        "energy_fraction": (
            float(energies[index] / total_energy) if total_energy else 0.0),
    } for rank, index in enumerate(selected))
    cumulative_energy_fraction = (
        math.fsum(row["energy"] for row in top_rows) / total_energy
        if total_energy else 0.0)
    participation_ratio = (
        total_energy * total_energy / float(np.sum(energies ** 2))
        if total_energy else 0.0)
    nontrivial_count = int(np.sum(
        energies > total_energy * tolerance / len(energies)))
    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "unit_group_order": len(units),
        "assembled_quotients": coefficient["assembled_quotients"],
        "aggregate_centered_l2": coefficient["aggregate_centered_l2"],
        "character_reconstruction_relative_error": reconstruction_error,
        "total_character_energy": total_energy,
        "parseval_centered_l2_squared_over_phi": float(
            coefficient["aggregate_centered_l2"] ** 2 / len(units)),
        "top_count": len(top_rows),
        "top_character_rows": top_rows,
        "top_character_cumulative_energy_fraction": (
            cumulative_energy_fraction),
        "character_energy_participation_ratio": participation_ratio,
        "nontrivial_character_count_at_tolerance": nontrivial_count,
        "small_character_support_diagnostic_passes": bool(
            cumulative_energy_fraction >= .9),
        "broad_character_support_observed": bool(
            cumulative_energy_fraction < .9),
        "character_spectrum_measured": bool(
            reconstruction_error <= tolerance),
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def combined_coefficient_pairwise_gram_receipt(tolerance=1e-9):
    """Measure pairwise cancellation between lifted centered channel vectors."""
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    period = math.lcm(
        CANONICAL_FAMILIES[0][0], 2 * CANONICAL_FAMILIES[0][1])
    period_units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    left_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[0])[2]
    right_sources = _one_orientation_count_source_modes(
        period, *CANONICAL_FAMILIES[1])[2]

    q77_common = 130
    q77_units = tuple(
        residue for residue in range(q77_common)
        if math.gcd(residue, q77_common) == 1)
    q77_source_units, q77_source_values_tuple = (
        _direct_resonant_source_on_units(
            period, TWO_PRIME_QUOTIENT_LAGS[77],
            left_sources, right_sources))
    q77_source_values = {
        residue: value
        for residue, value in zip(q77_source_units, q77_source_values_tuple)}
    q77_fiber_sums = np.asarray(tuple(
        _complex_fsum(q77_source_values[unit] for unit in q77_source_units
                      if unit % q77_common == residue)
        for residue in q77_units), dtype=np.complex128)
    q77_shadow = -(q77_fiber_sums - np.mean(q77_fiber_sums))
    component_coefficients = {
        77: {
            residue: value for residue, value in zip(q77_units, q77_shadow)}}
    component_common = {77: q77_common}
    for quotient in (35, 55, 65, 143):
        receipt = holdout_full_projected_prime_coefficient_receipt(
            quotient=quotient, tolerance=tolerance)
        common = receipt["common_modulus"]
        component_common[quotient] = common
        principal = receipt["principal_prime_residue_coefficient"]
        component_coefficients[quotient] = {
            residue: complex(value) - principal
            for residue, value
            in receipt["coefficient_by_unit_residue"].items()}

    quotients = (77, 35, 55, 65, 143)
    vectors = {}
    for quotient in quotients:
        common = component_common[quotient]
        coefficients = component_coefficients[quotient]
        lifted = np.asarray(tuple(
            coefficients[unit % common] for unit in period_units),
            dtype=np.complex128)
        vectors[quotient] = lifted - np.mean(lifted)

    norms = {
        quotient: float(np.linalg.norm(vector))
        for quotient, vector in vectors.items()}
    gram = {}
    normalized = {}
    total_self_energy = math.fsum(value * value for value in norms.values())
    total_cross_term = 0.0
    minimum_normalized_pair = 1.0
    maximum_normalized_pair = -1.0
    for left in quotients:
        for right in quotients:
            inner = complex(np.vdot(vectors[left], vectors[right]))
            gram[(left, right)] = inner
            denominator = norms[left] * norms[right]
            normalized_value = (
                inner.real / denominator if denominator else 0.0)
            normalized[(left, right)] = normalized_value
            if left < right:
                cross = 2 * inner.real
                total_cross_term += cross
                minimum_normalized_pair = min(
                    minimum_normalized_pair, normalized_value)
                maximum_normalized_pair = max(
                    maximum_normalized_pair, normalized_value)
    aggregate = sum(vectors.values())
    aggregate_energy = float(np.vdot(aggregate, aggregate).real)
    energy_reconstruction_error = abs(
        total_self_energy + total_cross_term - aggregate_energy) / max(
            1.0, aggregate_energy)
    return {
        "families": CANONICAL_FAMILIES,
        "arithmetic_period": period,
        "unit_group_order": len(period_units),
        "quotients": quotients,
        "component_norms": norms,
        "component_self_energy_total": total_self_energy,
        "pairwise_gram": gram,
        "pairwise_normalized_real_gram": normalized,
        "total_cross_term": total_cross_term,
        "cross_term_to_self_energy_ratio": (
            total_cross_term / total_self_energy
            if total_self_energy else 0.0),
        "aggregate_centered_energy": aggregate_energy,
        "aggregate_centered_l2": math.sqrt(max(0.0, aggregate_energy)),
        "energy_reconstruction_relative_error": energy_reconstruction_error,
        "minimum_offdiagonal_normalized_real_gram": minimum_normalized_pair,
        "maximum_offdiagonal_normalized_real_gram": maximum_normalized_pair,
        "substantial_negative_pairwise_cancellation_observed": bool(
            minimum_normalized_pair < -.1),
        "net_negative_cross_term_observed": bool(total_cross_term < 0),
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def _exact_imaginary_transform_table(denominator, period):
    base = tuple(
        int(_primitive_cotangent_transform_formula(
            denominator, frequency).imag)
        for frequency in range(denominator))
    return np.asarray(tuple(
        base[frequency % denominator] for frequency in range(period)),
        dtype=np.int64)


def _exact_projected_grouped_spatial_values(quotient):
    if quotient not in TWO_PRIME_QUOTIENT_LAGS:
        raise ValueError("quotient must be one of the two-prime sectors")
    period = math.lcm(
        CANONICAL_FAMILIES[0][0], 2 * CANONICAL_FAMILIES[0][1])
    lag = TWO_PRIME_QUOTIENT_LAGS[quotient]
    common = math.gcd(lag, period)
    frequency_indices = np.arange(period)
    quotient_weights = np.asarray(tuple(
        _ramanujan_sum(quotient, frequency)
        for frequency in range(period)), dtype=np.int64)
    left_table = _exact_imaginary_transform_table(
        CANONICAL_FAMILIES[0][0], period)
    left_partner = _exact_imaginary_transform_table(
        2 * CANONICAL_FAMILIES[0][1], period)
    left_negative_partner = left_partner[(-frequency_indices) % period]
    right_table = _exact_imaginary_transform_table(
        CANONICAL_FAMILIES[1][0], period)
    right_partner = _exact_imaginary_transform_table(
        2 * CANONICAL_FAMILIES[1][1], period)
    right_negative_partner = right_partner[(-frequency_indices) % period]
    numerator_by_residue = {
        residue: 0 for residue in range(common)
        if math.gcd(residue, common) == 1}
    for spatial_frequency in range(period):
        if math.gcd(spatial_frequency, common) != 1:
            continue
        left_first = np.roll(left_table, -spatial_frequency) - left_table
        left_second = (
            np.roll(left_negative_partner, -spatial_frequency)
            - left_negative_partner)
        right_first = np.roll(right_table, -spatial_frequency) - right_table
        right_second = (
            np.roll(right_negative_partner, -spatial_frequency)
            - right_negative_partner)
        products = (
            quotient_weights * left_first * left_second
            * right_first * right_second)
        numerator_by_residue[spatial_frequency % common] += (
            common * int(np.sum(products, dtype=np.int64)))
    denominator = 16 * period * period
    residues = tuple(sorted(numerator_by_residue))
    values = tuple(
        Fraction(numerator_by_residue[residue], denominator)
        for residue in residues)
    return period, common, residues, values


def exact_projected_pairwise_gram_receipt():
    """Confirm projected channel cross terms with rational arithmetic.

    This exact receipt uses the projected-spatial count-four representation for
    the five non-q91 sectors and computes dual-coefficient inner products over
    ``U_10010`` through integer Ramanujan sums.  It is exact for this
    projected representation; it is not an independent proof that every
    endpoint/noncentral term of the original outer assembly has been included.
    """
    quotients = (77, 35, 55, 65, 143)
    grouped = {}
    period = None
    for quotient in quotients:
        row_period, common, residues, values = (
            _exact_projected_grouped_spatial_values(quotient))
        if period is None:
            period = row_period
        elif period != row_period:
            raise AssertionError("inconsistent arithmetic periods")
        mean = sum(values, Fraction(0, 1)) / len(values)
        grouped[quotient] = {
            "common_modulus": common,
            "residues": residues,
            "centered_values": tuple(value - mean for value in values),
        }
    gram = {}
    normalized = {}
    norms_squared = {}
    for left in quotients:
        left_row = grouped[left]
        for right in quotients:
            right_row = grouped[right]
            total = Fraction(0, 1)
            for left_residue, left_value in zip(
                    left_row["residues"], left_row["centered_values"]):
                left_multiplier = period // left_row["common_modulus"]
                for right_residue, right_value in zip(
                        right_row["residues"],
                        right_row["centered_values"]):
                    right_multiplier = period // right_row["common_modulus"]
                    frequency = (
                        right_residue * right_multiplier
                        - left_residue * left_multiplier) % period
                    total += (
                        left_value * right_value
                        * _ramanujan_sum(period, frequency))
            gram[(left, right)] = total
            if left == right:
                norms_squared[left] = total
    total_self_energy = sum(
        norms_squared[quotient] for quotient in quotients)
    total_cross_term = Fraction(0, 1)
    minimum_normalized_pair = 1.0
    maximum_normalized_pair = -1.0
    for left in quotients:
        for right in quotients:
            denominator = math.sqrt(
                float(norms_squared[left]) * float(norms_squared[right]))
            normalized_value = (
                float(gram[(left, right)]) / denominator
                if denominator else 0.0)
            normalized[(left, right)] = normalized_value
            if left < right:
                total_cross_term += 2 * gram[(left, right)]
                minimum_normalized_pair = min(
                    minimum_normalized_pair, normalized_value)
                maximum_normalized_pair = max(
                    maximum_normalized_pair, normalized_value)
    aggregate_energy = total_self_energy + total_cross_term
    return {
        "families": CANONICAL_FAMILIES,
        "arithmetic_period": period,
        "quotients": quotients,
        "component_norms_squared_exact": norms_squared,
        "component_norms": {
            quotient: math.sqrt(float(value))
            for quotient, value in norms_squared.items()},
        "pairwise_gram_exact": gram,
        "pairwise_normalized_real_gram": normalized,
        "component_self_energy_total_exact": total_self_energy,
        "component_self_energy_total": float(total_self_energy),
        "total_cross_term_exact": total_cross_term,
        "total_cross_term": float(total_cross_term),
        "cross_term_to_self_energy_ratio_exact": (
            total_cross_term / total_self_energy
            if total_self_energy else Fraction(0, 1)),
        "cross_term_to_self_energy_ratio": (
            float(total_cross_term / total_self_energy)
            if total_self_energy else 0.0),
        "aggregate_centered_energy_exact": aggregate_energy,
        "aggregate_centered_energy": float(aggregate_energy),
        "aggregate_centered_l2": math.sqrt(float(aggregate_energy)),
        "minimum_offdiagonal_normalized_real_gram": minimum_normalized_pair,
        "maximum_offdiagonal_normalized_real_gram": maximum_normalized_pair,
        "substantial_negative_pairwise_cancellation_observed": bool(
            minimum_normalized_pair < -.1),
        "net_negative_cross_term_observed": bool(total_cross_term < 0),
        "exact_projected_pairwise_gram_confirmed": True,
        "original_outer_assembly_fully_verified": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q77_original_strict_central_action_receipt(
        targets=(1000, 1002), tolerance=1e-12, batch_size=32):
    """Compare original q77 strict-central action to the assembled coefficient.

    The original linked-prime q77 rows give a coefficient vector on ``U_130``.
    The assembled family also includes a q77 component on ``U_130``: the
    principal constant ``-3143/16`` plus the lag-130 fiber shadow.  This receipt
    compares those coefficient vectors and their ordered strict-central
    prime-pair actions directly.  It does not include endpoint/noncentral terms
    or prove the remaining pointwise prime-correlation estimate.
    """
    targets = tuple(targets)
    if (not targets or any(type(target) is not int or target < 40
                           or target % 2 for target in targets)):
        raise ValueError("targets must be even integers at least 40")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    centering = linked_prime_centering_receipt(
        targets=targets, tolerance=tolerance, batch_size=batch_size)
    assembled = combined_fixed_strict_central_coefficient_receipt(
        tolerance=max(tolerance, 1e-9))
    period = assembled["arithmetic_period"]
    common = 130
    quotient = period // common
    assembled_q77 = assembled["component_coefficient_by_residue"][77]
    q77_summary = centering["quotient_summaries"][77]

    rows = {}
    maximum_vector_relative_error = 0.0
    maximum_action_relative_error = 0.0
    maximum_original_receipt_relative_error = 0.0
    maximum_principal_shadow_relative_error = 0.0
    all_nonunit_pairs = []
    unit_fiber_sizes = []
    for target in centering["targets"]:
        q77_source_rows = tuple(
            row for (row_quotient, _, row_target), row
            in centering["rows"].items()
            if row_quotient == 77 and row_target == target)
        if not q77_source_rows:
            raise AssertionError("missing q77 source rows for target")
        units130 = tuple(int(unit) for unit in q77_source_rows[0][
            "unit_residues"])
        quotient77_source = sum((
            row["additive_unit_source_values"] for row in q77_source_rows),
            np.zeros_like(q77_source_rows[0][
                "additive_unit_source_values"]))
        original_by_residue = {
            residue: complex(value)
            for residue, value in zip(units130, quotient77_source)}
        assembled_vector = np.asarray(tuple(
            assembled_q77[residue] for residue in units130),
            dtype=np.complex128)
        original_vector = np.asarray(tuple(
            original_by_residue[residue] for residue in units130),
            dtype=np.complex128)
        vector_scale = max(
            1.0, float(np.linalg.norm(original_vector)),
            float(np.linalg.norm(assembled_vector)))
        vector_relative_error = float(
            np.linalg.norm(original_vector - assembled_vector) / vector_scale)
        maximum_vector_relative_error = max(
            maximum_vector_relative_error, vector_relative_error)

        lower = target // 3
        upper = target - lower
        original_action_terms = []
        assembled_action_terms = []
        centered_action_terms = []
        principal_weight = 0.0
        nonunit_pairs = []
        for prime, weight in _linked_prime_pairs(target, lower, upper):
            partner = target - prime
            residue = prime % common
            if math.gcd(residue, common) != 1:
                nonunit_pairs.append((prime, partner))
                continue
            original_action_terms.append(original_by_residue[residue] * weight)
            assembled_action_terms.append(assembled_q77[residue] * weight)
            centered_action_terms.append(
                (assembled_q77[residue] + 3143 / 16) * weight)
            principal_weight += weight
        all_nonunit_pairs.extend((target, pair) for pair in nonunit_pairs)
        original_action = _complex_fsum(original_action_terms)
        assembled_action = _complex_fsum(assembled_action_terms)
        principal_action = complex(-3143 / 16) * principal_weight
        principal_shadow_action = (
            principal_action + _complex_fsum(centered_action_terms))
        original_receipt_action = q77_summary["target_summaries"][target][
            "recombined_direct_unit_correlation"]
        action_scale = max(
            1.0, abs(original_action), abs(assembled_action))
        action_relative_error = abs(
            original_action - assembled_action) / action_scale
        original_receipt_scale = max(
            1.0, abs(original_action), abs(original_receipt_action))
        original_receipt_relative_error = abs(
            original_action - original_receipt_action) / original_receipt_scale
        principal_shadow_scale = max(
            1.0, abs(assembled_action), abs(principal_shadow_action))
        principal_shadow_relative_error = abs(
            assembled_action - principal_shadow_action) / principal_shadow_scale
        maximum_action_relative_error = max(
            maximum_action_relative_error, action_relative_error)
        maximum_original_receipt_relative_error = max(
            maximum_original_receipt_relative_error,
            original_receipt_relative_error)
        maximum_principal_shadow_relative_error = max(
            maximum_principal_shadow_relative_error,
            principal_shadow_relative_error)
        unit_fiber_sizes.append(period // common)
        rows[target] = {
            "strict_central_interval": (lower, upper),
            "ordered_central_prime_pair_count": len(original_action_terms),
            "nonunit_prime_pairs": tuple(nonunit_pairs),
            "original_q77_strict_central_action": original_action,
            "assembled_q77_coefficient_action": assembled_action,
            "original_receipt_direct_unit_correlation": (
                original_receipt_action),
            "principal_unit_weight": principal_weight,
            "principal_action": principal_action,
            "principal_plus_shadow_action": principal_shadow_action,
            "coefficient_vector_relative_error": vector_relative_error,
            "assembled_action_relative_error": action_relative_error,
            "original_receipt_action_relative_error": (
                original_receipt_relative_error),
            "principal_plus_shadow_action_relative_error": (
                principal_shadow_relative_error),
        }

    return {
        "families": CANONICAL_FAMILIES,
        "arithmetic_period": period,
        "common_modulus": common,
        "quotient": quotient,
        "lag": TWO_PRIME_QUOTIENT_LAGS[77],
        "targets": centering["targets"],
        "unit_group_order": len(assembled_q77),
        "period_to_common_quotient_factor": quotient,
        "unit_fiber_size_over_U130": len(tuple(
            unit for unit in range(period)
            if math.gcd(unit, period) == 1 and unit % common == 1)),
        "strict_central_prime_residue_map": "p mod 10010 -> p mod 130",
        "ordered_pair_convention": "ordered; no factor 1/2 is inserted",
        "rows": rows,
        "maximum_coefficient_vector_relative_error": (
            maximum_vector_relative_error),
        "maximum_assembled_action_relative_error": (
            maximum_action_relative_error),
        "maximum_original_receipt_action_relative_error": (
            maximum_original_receipt_relative_error),
        "maximum_principal_plus_shadow_action_relative_error": (
            maximum_principal_shadow_relative_error),
        "nonunit_prime_pairs": tuple(all_nonunit_pairs),
        "q77_original_equals_assembled_coefficient_vector": bool(
            maximum_vector_relative_error <= tolerance),
        "q77_original_action_equals_assembled_coefficient_action": bool(
            not all_nonunit_pairs
            and maximum_action_relative_error <= tolerance
            and maximum_original_receipt_relative_error <= tolerance
            and maximum_principal_shadow_relative_error <= tolerance),
        "endpoint_or_noncentral_terms_analyzed": False,
        "full_outer_assembly_identification_proved": False,
        "formal_signed_error_identification_proved": False,
        "pointwise_signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def holdout_original_projected_action_audit_receipt(
        targets=(1000, 1002), tolerance=1e-9):
    """Audit holdout sector actions against assembled component coefficients.

    For q35, q55, q65, and q143, the source-side object is the projected
    count-four spatial-frequency action.  This receipt recomputes that action
    from grouped spatial residues, then compares it to the corresponding
    assembled prime-residue coefficient action.  It is independent of the q77
    linked-row audit and remains a finite action identity, not an estimate.
    """
    targets = tuple(targets)
    if (not targets or any(type(target) is not int or target < 40
                           or target % 2 for target in targets)):
        raise ValueError("targets must be even integers at least 40")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    assembled = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    component_maps = assembled["component_coefficient_by_residue"]
    quotients = (35, 55, 65, 143)
    quotient_rows = {}
    maximum_action_relative_error = 0.0
    all_nonunit_pairs = []
    for quotient in quotients:
        source = holdout_projected_spatial_fiber_bridge_receipt(
            quotient=quotient, tolerance=1e-12)
        common = source["common_modulus"]
        residues = tuple(
            residue for residue in range(common)
            if math.gcd(residue, common) == 1)
        spatial = np.asarray(source["grouped_centered_spatial_values"],
                             dtype=np.complex128)
        spatial = spatial + source["grouped_spatial_mean"]
        phase = np.exp(
            2j * np.pi * np.outer(residues, residues) / common)
        direct_dual = phase @ spatial
        assembled_vector = np.asarray(tuple(
            component_maps[quotient][residue] for residue in residues),
            dtype=np.complex128)
        vector_scale = max(
            1.0, float(np.linalg.norm(direct_dual)),
            float(np.linalg.norm(assembled_vector)))
        coefficient_vector_error = float(
            np.linalg.norm(direct_dual - assembled_vector) / vector_scale)

        target_rows = {}
        quotient_maximum_action_error = 0.0
        for target in targets:
            lower = target // 3
            upper = target - lower
            exponential_sums = {residue: 0.0j for residue in residues}
            assembled_terms = []
            pair_count = 0
            nonunit_pairs = []
            for prime, weight in _linked_prime_pairs(target, lower, upper):
                partner = target - prime
                prime_residue = prime % common
                pair_count += 1
                if math.gcd(prime_residue, common) != 1:
                    nonunit_pairs.append((prime, partner))
                    continue
                assembled_terms.append(
                    component_maps[quotient][prime_residue] * weight)
                for residue in residues:
                    exponential_sums[residue] += (
                        np.exp(
                            2j * np.pi * residue * prime_residue / common)
                        * weight)
            original_projected_action = _complex_fsum(
                value * exponential_sums[residue]
                for residue, value in zip(residues, spatial))
            assembled_action = _complex_fsum(assembled_terms)
            action_scale = max(
                1.0, abs(original_projected_action), abs(assembled_action))
            action_relative_error = abs(
                original_projected_action - assembled_action) / action_scale
            quotient_maximum_action_error = max(
                quotient_maximum_action_error, action_relative_error)
            maximum_action_relative_error = max(
                maximum_action_relative_error, action_relative_error)
            all_nonunit_pairs.extend((quotient, target, pair)
                                     for pair in nonunit_pairs)
            target_rows[target] = {
                "strict_central_interval": (lower, upper),
                "ordered_central_prime_pair_count": pair_count,
                "nonunit_prime_pairs": tuple(nonunit_pairs),
                "original_projected_spatial_action": (
                    original_projected_action),
                "assembled_component_coefficient_action": assembled_action,
                "action_relative_error": action_relative_error,
            }
        quotient_rows[quotient] = {
            "lag": source["lag"],
            "common_modulus": common,
            "unit_group_order": len(residues),
            "coefficient_vector_relative_error": coefficient_vector_error,
            "maximum_action_relative_error": (
                quotient_maximum_action_error),
            "rows": target_rows,
        }

    return {
        "families": CANONICAL_FAMILIES,
        "arithmetic_period": assembled["arithmetic_period"],
        "audited_quotients": quotients,
        "targets": targets,
        "quotient_rows": quotient_rows,
        "maximum_action_relative_error": maximum_action_relative_error,
        "nonunit_prime_pairs": tuple(all_nonunit_pairs),
        "holdout_original_projected_actions_equal_assembled_components": bool(
            not all_nonunit_pairs
            and maximum_action_relative_error <= tolerance
            and all(row["coefficient_vector_relative_error"] <= tolerance
                    for row in quotient_rows.values())),
        "q77_linked_row_audit_separate": True,
        "pointwise_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def combined_coefficient_admissible_main_receipt(tolerance=1e-9):
    """Compute local admissible mains for the assembled fixed coefficient."""
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    values = coefficient["aggregate_coefficient_by_unit_residue"]
    rows = {}
    real_values = []
    imaginary_values = []
    for target_residue in range(0, period, 2):
        admissible = tuple(
            residue for residue in units
            if math.gcd((target_residue - residue) % period, period) == 1)
        local_main = _complex_fsum(values[residue] for residue in admissible)
        rows[target_residue] = {
            "admissible_unit_count": len(admissible),
            "local_main_coefficient": local_main,
        }
        real_values.append(local_main.real)
        imaginary_values.append(abs(local_main.imag))
    minimum_row = min(rows, key=lambda residue: rows[residue][
        "local_main_coefficient"].real)
    maximum_row = max(rows, key=lambda residue: rows[residue][
        "local_main_coefficient"].real)
    negative_rows = tuple(
        residue for residue, row in rows.items()
        if row["local_main_coefficient"].real < -tolerance)
    near_zero_rows = tuple(
        residue for residue, row in rows.items()
        if abs(row["local_main_coefficient"].real) <= tolerance)
    sorted_by_main = tuple(sorted(
        rows.items(),
        key=lambda item: item[1]["local_main_coefficient"].real))
    quantile_indices = {
        "0%": 0,
        "1%": int(.01 * (len(sorted_by_main) - 1)),
        "5%": int(.05 * (len(sorted_by_main) - 1)),
        "10%": int(.10 * (len(sorted_by_main) - 1)),
        "25%": int(.25 * (len(sorted_by_main) - 1)),
        "50%": int(.50 * (len(sorted_by_main) - 1)),
        "75%": int(.75 * (len(sorted_by_main) - 1)),
        "90%": int(.90 * (len(sorted_by_main) - 1)),
        "95%": int(.95 * (len(sorted_by_main) - 1)),
        "99%": int(.99 * (len(sorted_by_main) - 1)),
        "100%": len(sorted_by_main) - 1,
    }
    local_main_quantiles = {
        label: {
            "residue": sorted_by_main[index][0],
            "real": sorted_by_main[index][1][
                "local_main_coefficient"].real,
            "admissible_unit_count": sorted_by_main[index][1][
                "admissible_unit_count"],
        }
        for label, index in quantile_indices.items()}
    admissible_count_histogram = {}
    for row in rows.values():
        count = row["admissible_unit_count"]
        admissible_count_histogram[count] = (
            admissible_count_histogram.get(count, 0) + 1)
    smallest_rows = tuple(
        (residue, row["admissible_unit_count"],
         row["local_main_coefficient"])
        for residue, row in sorted_by_main[:12])
    largest_rows = tuple(
        (residue, row["admissible_unit_count"],
         row["local_main_coefficient"])
        for residue, row in reversed(sorted_by_main[-12:]))
    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "even_target_residue_count": len(rows),
        "unit_group_order": len(units),
        "minimum_admissible_unit_count": min(
            row["admissible_unit_count"] for row in rows.values()),
        "maximum_admissible_unit_count": max(
            row["admissible_unit_count"] for row in rows.values()),
        "minimum_local_main_residue": minimum_row,
        "minimum_local_main_value": rows[minimum_row][
            "local_main_coefficient"],
        "maximum_local_main_residue": maximum_row,
        "maximum_local_main_value": rows[maximum_row][
            "local_main_coefficient"],
        "negative_local_main_residue_count": len(negative_rows),
        "negative_local_main_residues": negative_rows,
        "near_zero_local_main_residue_count": len(near_zero_rows),
        "maximum_local_main_imaginary_part": max(imaginary_values),
        "mean_local_main_real": math.fsum(real_values) / len(real_values),
        "minimum_to_mean_local_main_ratio": (
            rows[minimum_row]["local_main_coefficient"].real
            / (math.fsum(real_values) / len(real_values))),
        "local_main_quantiles": local_main_quantiles,
        "admissible_unit_count_histogram": dict(sorted(
            admissible_count_histogram.items())),
        "smallest_local_main_rows": smallest_rows,
        "largest_local_main_rows": largest_rows,
        "all_local_mains_positive": bool(not negative_rows),
        "fixed_positive_local_main_for_all_even_classes": bool(
            not negative_rows and not near_zero_rows),
        "rows": rows,
        "local_main_profile_measured": True,
        "pointwise_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def combined_coefficient_prime_correlation_diagnostic_receipt(
        target_minimum=10000, target_maximum=20008, tolerance=1e-9):
    """Stress the assembled coefficient against actual central prime pairs.

    This is a finite diagnostic, not an analytic estimate.  It compares the
    observed ordered strict-central prime-pair sum

        sum log(p)log(N-p) C(p mod 10010)

    with the residue-class local main ``sum_(a in A_N) C(a)`` through the
    normalization used by the Halupczok transfer.  A positive diagnostic does
    not prove pointwise control; a negative or tiny value would identify an
    immediate obstruction for the explicit coefficient.
    """
    if (type(target_minimum) is not int or type(target_maximum) is not int
            or target_minimum < 40 or target_maximum < target_minimum):
        raise ValueError("require integer target bounds with 40<=min<=max")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    first_target = target_minimum + (target_minimum % 2)
    targets = tuple(range(first_target, target_maximum + 1, 2))
    if not targets:
        raise ValueError("target range contains no even targets")
    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    coefficient_by_residue = coefficient[
        "aggregate_coefficient_by_unit_residue"]
    local_main_by_residue = {}
    for target_residue in range(0, period, 2):
        local_main_by_residue[target_residue] = _complex_fsum(
            coefficient_by_residue[residue]
            for residue in units
            if math.gcd((target_residue - residue) % period, period) == 1)

    primes = _prime_table(targets[-1])
    rows = {}
    real_values = []
    normalized_values = []
    negative_targets = []
    near_zero_targets = []
    bad_prime_pairs = []
    for target in targets:
        lower = target // 3
        upper = target - lower
        weighted_terms = []
        absolute_mass = 0.0
        pair_count = 0
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if not primes[prime] or not primes[partner]:
                continue
            pair_count += 1
            residue = prime % period
            if math.gcd(residue, period) != 1:
                bad_prime_pairs.append((target, (prime, partner)))
                continue
            term = (
                coefficient_by_residue[residue]
                * math.log(prime) * math.log(partner))
            weighted_terms.append(term)
            absolute_mass += abs(term)
        weighted_sum = _complex_fsum(weighted_terms)
        local_main = local_main_by_residue[target % period]
        normalized_model_scale = (
            target * local_main.real / (3 * len(units)))
        normalized_multiplier = (
            weighted_sum.real / normalized_model_scale
            if abs(normalized_model_scale) > tolerance else math.nan)
        real_values.append(weighted_sum.real)
        if math.isfinite(normalized_multiplier):
            normalized_values.append(normalized_multiplier)
        if weighted_sum.real < -tolerance:
            negative_targets.append(target)
        if abs(weighted_sum.real) <= tolerance:
            near_zero_targets.append(target)
        rows[target] = {
            "target_residue": target % period,
            "strict_central_interval": (lower, upper),
            "ordered_central_prime_pair_count": pair_count,
            "weighted_prime_correlation": weighted_sum,
            "absolute_term_mass": absolute_mass,
            "absolute_cancellation_ratio": (
                abs(weighted_sum) / absolute_mass if absolute_mass else None),
            "local_main_coefficient": local_main,
            "halupczok_normalized_multiplier_without_singular_series": (
                normalized_multiplier),
        }

    sorted_by_sum = tuple(sorted(
        rows.items(), key=lambda item: item[1][
            "weighted_prime_correlation"].real))
    sorted_by_normalized = tuple(sorted(
        rows.items(), key=lambda item: item[1][
            "halupczok_normalized_multiplier_without_singular_series"]))
    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "target_range": (targets[0], targets[-1]),
        "tested_target_count": len(targets),
        "covered_even_residue_count": len({target % period
                                           for target in targets}),
        "unit_group_order": len(units),
        "rows": rows,
        "minimum_weighted_sum_target": sorted_by_sum[0][0],
        "minimum_weighted_sum_value": sorted_by_sum[0][1][
            "weighted_prime_correlation"],
        "maximum_weighted_sum_target": sorted_by_sum[-1][0],
        "maximum_weighted_sum_value": sorted_by_sum[-1][1][
            "weighted_prime_correlation"],
        "minimum_normalized_multiplier_target": sorted_by_normalized[0][0],
        "minimum_normalized_multiplier": sorted_by_normalized[0][1][
            "halupczok_normalized_multiplier_without_singular_series"],
        "maximum_normalized_multiplier_target": sorted_by_normalized[-1][0],
        "maximum_normalized_multiplier": sorted_by_normalized[-1][1][
            "halupczok_normalized_multiplier_without_singular_series"],
        "mean_weighted_sum_real": math.fsum(real_values) / len(real_values),
        "mean_normalized_multiplier": (
            math.fsum(normalized_values) / len(normalized_values)
            if normalized_values else math.nan),
        "negative_weighted_sum_count": len(negative_targets),
        "negative_weighted_sum_targets": tuple(negative_targets),
        "near_zero_weighted_sum_count": len(near_zero_targets),
        "nonunit_or_inadmissible_prime_pairs": tuple(bad_prime_pairs),
        "all_sampled_weighted_sums_positive": bool(
            not negative_targets and not near_zero_targets),
        "finite_prime_correlation_diagnostic_measured": True,
        "pointwise_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def combined_coefficient_negative_residue_lift_receipt(
        base_target_minimum=10000, base_target_maximum=20008,
        additional_period_lifts=(0, 1, 4, 9, 19, 49), tolerance=1e-9):
    """Test whether first-cycle negative residue classes persist under lifts.

    This receipt is a finite stress test for a threshold-plus-finite-check
    route.  It first finds negative assembled-coefficient prime correlations in
    a base range, then recomputes the same target residues after adding full
    periods.  It is not an analytic prime-correlation estimate.
    """
    if (type(base_target_minimum) is not int
            or type(base_target_maximum) is not int
            or base_target_minimum < 40
            or base_target_maximum < base_target_minimum):
        raise ValueError("require integer base bounds with 40<=min<=max")
    additional_period_lifts = tuple(additional_period_lifts)
    if (not additional_period_lifts
            or any(type(lift) is not int or lift < 0
                   for lift in additional_period_lifts)):
        raise ValueError("additional_period_lifts must be nonnegative integers")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    coefficient_by_residue = coefficient[
        "aggregate_coefficient_by_unit_residue"]
    local_main_by_residue = {
        target_residue: _complex_fsum(
            coefficient_by_residue[residue]
            for residue in units
            if math.gcd((target_residue - residue) % period, period) == 1)
        for target_residue in range(0, period, 2)}

    first_base = base_target_minimum + (base_target_minimum % 2)
    base_targets = tuple(range(first_base, base_target_maximum + 1, 2))
    if not base_targets:
        raise ValueError("base range contains no even targets")
    maximum_target = max(
        target + max(additional_period_lifts) * period
        for target in base_targets)
    primes = _prime_table(maximum_target)

    def evaluate(target):
        lower = target // 3
        upper = target - lower
        weighted_terms = []
        pair_count = 0
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                pair_count += 1
                weighted_terms.append(
                    coefficient_by_residue[prime % period]
                    * math.log(prime) * math.log(partner))
        weighted_sum = _complex_fsum(weighted_terms)
        local_main = local_main_by_residue[target % period]
        normalized_scale = target * local_main.real / (3 * len(units))
        normalized = (
            weighted_sum.real / normalized_scale
            if abs(normalized_scale) > tolerance else math.nan)
        return {
            "target": target,
            "target_residue": target % period,
            "ordered_central_prime_pair_count": pair_count,
            "weighted_prime_correlation": weighted_sum,
            "halupczok_normalized_multiplier_without_singular_series": (
                normalized),
            "is_negative": bool(weighted_sum.real < -tolerance),
        }

    base_rows = {target: evaluate(target) for target in base_targets}
    negative_base_targets = tuple(
        target for target, row in base_rows.items()
        if row["is_negative"])
    lifted_rows = {}
    persistent_negative_residues = []
    minimum_lifted_normalized = math.inf
    minimum_lifted_target = None
    for base_target in negative_base_targets:
        residue = base_target % period
        rows = []
        has_lifted_negative = False
        for lift in additional_period_lifts:
            target = base_target + lift * period
            row = evaluate(target)
            row["additional_period_lift"] = lift
            rows.append(row)
            if lift and row["is_negative"]:
                has_lifted_negative = True
            if lift and row[
                    "halupczok_normalized_multiplier_without_singular_series"
                    ] < minimum_lifted_normalized:
                minimum_lifted_normalized = row[
                    "halupczok_normalized_multiplier_without_singular_series"]
                minimum_lifted_target = target
        if has_lifted_negative:
            persistent_negative_residues.append(residue)
        lifted_rows[residue] = tuple(rows)

    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "base_target_range": (base_targets[0], base_targets[-1]),
        "base_tested_target_count": len(base_targets),
        "base_covered_even_residue_count": len({target % period
                                                for target in base_targets}),
        "additional_period_lifts": additional_period_lifts,
        "base_negative_target_count": len(negative_base_targets),
        "base_negative_targets": negative_base_targets,
        "tested_negative_residue_count": len(lifted_rows),
        "lifted_rows_by_residue": lifted_rows,
        "persistent_lifted_negative_residue_count": len(
            persistent_negative_residues),
        "persistent_lifted_negative_residues": tuple(
            persistent_negative_residues),
        "minimum_lifted_normalized_multiplier_target": (
            minimum_lifted_target),
        "minimum_lifted_normalized_multiplier": (
            minimum_lifted_normalized
            if minimum_lifted_target is not None else math.nan),
        "negative_residue_lift_diagnostic_measured": True,
        "asymptotic_threshold_strategy_falsified": bool(
            persistent_negative_residues),
        "pointwise_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def combined_coefficient_period_cycle_envelope_receipt(
        base_target_minimum=10000, cycle_count=3,
        targets_per_cycle=None, tolerance=1e-9):
    """Scan period cycles for the assembled prime-correlation lower envelope.

    Each cycle advances by the arithmetic period while preserving the same
    order of even residue classes.  The receipt measures whether the finite
    negative first-cycle behavior persists across whole cycles.  It is a finite
    diagnostic, not a uniform pointwise theorem.
    """
    if (type(base_target_minimum) is not int or base_target_minimum < 40
            or base_target_minimum % 2):
        raise ValueError("base_target_minimum must be an even integer >=40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (targets_per_cycle is not None
            and (type(targets_per_cycle) is not int
                 or targets_per_cycle < 1)):
        raise ValueError("targets_per_cycle must be None or a positive integer")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    full_cycle_targets = period // 2
    per_cycle = (
        full_cycle_targets if targets_per_cycle is None
        else min(targets_per_cycle, full_cycle_targets))
    maximum_target = (
        base_target_minimum
        + (cycle_count - 1) * period
        + 2 * (per_cycle - 1))
    coefficient_by_residue = coefficient[
        "aggregate_coefficient_by_unit_residue"]
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    local_main_by_residue = {
        target_residue: _complex_fsum(
            coefficient_by_residue[residue]
            for residue in units
            if math.gcd((target_residue - residue) % period, period) == 1)
        for target_residue in range(0, period, 2)}
    primes = _prime_table(maximum_target)

    def evaluate(target):
        lower = target // 3
        upper = target - lower
        terms = []
        pair_count = 0
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                pair_count += 1
                terms.append(
                    coefficient_by_residue[prime % period]
                    * math.log(prime) * math.log(partner))
        weighted_sum = _complex_fsum(terms)
        local_main = local_main_by_residue[target % period]
        normalized_scale = target * local_main.real / (3 * len(units))
        normalized = (
            weighted_sum.real / normalized_scale
            if abs(normalized_scale) > tolerance else math.nan)
        return {
            "target": target,
            "target_residue": target % period,
            "ordered_central_prime_pair_count": pair_count,
            "weighted_prime_correlation": weighted_sum,
            "halupczok_normalized_multiplier_without_singular_series": (
                normalized),
            "is_negative": bool(weighted_sum.real < -tolerance),
        }

    cycle_rows = {}
    first_nonnegative_cycle = None
    global_minimum_row = None
    global_maximum_row = None
    for cycle_index in range(cycle_count):
        start = base_target_minimum + cycle_index * period
        rows = tuple(evaluate(start + 2 * offset)
                     for offset in range(per_cycle))
        negative_rows = tuple(row for row in rows if row["is_negative"])
        minimum_row = min(
            rows,
            key=lambda row: row[
                "halupczok_normalized_multiplier_without_singular_series"])
        maximum_row = max(
            rows,
            key=lambda row: row[
                "halupczok_normalized_multiplier_without_singular_series"])
        if first_nonnegative_cycle is None and not negative_rows:
            first_nonnegative_cycle = cycle_index
        if (global_minimum_row is None
                or minimum_row[
                    "halupczok_normalized_multiplier_without_singular_series"]
                < global_minimum_row[
                    "halupczok_normalized_multiplier_without_singular_series"]):
            global_minimum_row = minimum_row
        if (global_maximum_row is None
                or maximum_row[
                    "halupczok_normalized_multiplier_without_singular_series"]
                > global_maximum_row[
                    "halupczok_normalized_multiplier_without_singular_series"]):
            global_maximum_row = maximum_row
        cycle_rows[cycle_index] = {
            "target_range": (rows[0]["target"], rows[-1]["target"]),
            "tested_target_count": len(rows),
            "covered_even_residue_count": len({row["target_residue"]
                                               for row in rows}),
            "negative_weighted_sum_count": len(negative_rows),
            "minimum_normalized_multiplier_target": minimum_row["target"],
            "minimum_normalized_multiplier": minimum_row[
                "halupczok_normalized_multiplier_without_singular_series"],
            "maximum_normalized_multiplier_target": maximum_row["target"],
            "maximum_normalized_multiplier": maximum_row[
                "halupczok_normalized_multiplier_without_singular_series"],
            "mean_normalized_multiplier": math.fsum(
                row["halupczok_normalized_multiplier_without_singular_series"]
                for row in rows) / len(rows),
            "negative_targets": tuple(row["target"]
                                      for row in negative_rows),
        }

    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "base_target_minimum": base_target_minimum,
        "cycle_count": cycle_count,
        "targets_per_cycle": per_cycle,
        "full_cycle_targets": full_cycle_targets,
        "full_cycles_scanned": bool(per_cycle == full_cycle_targets),
        "cycle_rows": cycle_rows,
        "first_nonnegative_cycle_index": first_nonnegative_cycle,
        "first_nonnegative_cycle_target_range": (
            cycle_rows[first_nonnegative_cycle]["target_range"]
            if first_nonnegative_cycle is not None else None),
        "global_minimum_normalized_multiplier_target": (
            global_minimum_row["target"]),
        "global_minimum_normalized_multiplier": global_minimum_row[
            "halupczok_normalized_multiplier_without_singular_series"],
        "global_maximum_normalized_multiplier_target": (
            global_maximum_row["target"]),
        "global_maximum_normalized_multiplier": global_maximum_row[
            "halupczok_normalized_multiplier_without_singular_series"],
        "all_scanned_cycles_positive": all(
            row["negative_weighted_sum_count"] == 0
            for row in cycle_rows.values()),
        "period_cycle_envelope_measured": True,
        "pointwise_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def combined_coefficient_uniform_residue_margin_receipt(
        target_minimum=10000, target_maximum=10100, tolerance=1e-9):
    """Compute the uniform-residue discrepancy margin needed for positivity.

    For a fixed even residue ``n`` modulo ``10010``, let ``A_n`` be the unit
    residues for which ``n-a`` is also a unit and let ``C`` be the assembled
    coefficient.  If the actual strict-central prime-pair weights ``W_a`` obey

        |W_a - mean(W)| <= eta * mean(W)  for every a in A_n,

    then the real weighted sum is positive whenever

        eta < Re(sum_A C) / sum_A |C - mean_A(C)|.

    This receipt measures that sufficient margin for all `5005` even residue
    classes and compares it with finite observed prime-pair residue weights.
    It is not a proof that the required pointwise discrepancy bound holds.
    """
    if (type(target_minimum) is not int or type(target_maximum) is not int
            or target_minimum < 40 or target_maximum < target_minimum):
        raise ValueError("require integer target bounds with 40<=min<=max")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    first_target = target_minimum + (target_minimum % 2)
    targets = tuple(range(first_target, target_maximum + 1, 2))
    if not targets:
        raise ValueError("target range contains no even targets")

    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    coefficient_by_residue = coefficient[
        "aggregate_coefficient_by_unit_residue"]

    margin_rows = {}
    margins = []
    for target_residue in range(0, period, 2):
        admissible = tuple(
            residue for residue in units
            if math.gcd((target_residue - residue) % period, period) == 1)
        values = tuple(coefficient_by_residue[residue]
                       for residue in admissible)
        local_main = _complex_fsum(values)
        local_mean = local_main / len(values)
        centered_l1 = math.fsum(abs(value - local_mean) for value in values)
        margin = (
            local_main.real / centered_l1 if centered_l1 > tolerance
            else math.inf)
        margins.append(margin)
        margin_rows[target_residue] = {
            "admissible_unit_count": len(admissible),
            "local_main_coefficient": local_main,
            "admissible_mean_coefficient": local_mean,
            "centered_l1": centered_l1,
            "sufficient_uniform_relative_error_margin": margin,
        }

    primes = _prime_table(targets[-1])
    observed_rows = {}
    for target in targets:
        target_residue = target % period
        admissible = tuple(
            residue for residue in units
            if math.gcd((target_residue - residue) % period, period) == 1)
        weights_by_residue = {residue: 0.0 for residue in admissible}
        lower = target // 3
        upper = target - lower
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                residue = prime % period
                if residue in weights_by_residue:
                    weights_by_residue[residue] += (
                        math.log(prime) * math.log(partner))
        total_weight = math.fsum(weights_by_residue.values())
        mean_weight = total_weight / len(admissible)
        max_relative_discrepancy = (
            max(abs(value - mean_weight)
                for value in weights_by_residue.values()) / mean_weight
            if mean_weight > tolerance else math.inf)
        weighted_sum = _complex_fsum(
            coefficient_by_residue[residue] * weight
            for residue, weight in weights_by_residue.items())
        margin = margin_rows[target_residue][
            "sufficient_uniform_relative_error_margin"]
        observed_rows[target] = {
            "target_residue": target_residue,
            "ordered_central_prime_pair_weight": total_weight,
            "observed_residue_weight_mean": mean_weight,
            "maximum_observed_relative_residue_discrepancy": (
                max_relative_discrepancy),
            "sufficient_uniform_relative_error_margin": margin,
            "margin_condition_observed": bool(
                max_relative_discrepancy < margin),
            "weighted_prime_correlation": weighted_sum,
            "weighted_prime_correlation_positive": bool(
                weighted_sum.real > tolerance),
        }

    minimum_margin_residue = min(
        margin_rows,
        key=lambda residue: margin_rows[residue][
            "sufficient_uniform_relative_error_margin"])
    observed_margin_successes = tuple(
        target for target, row in observed_rows.items()
        if row["margin_condition_observed"])
    observed_positive_targets = tuple(
        target for target, row in observed_rows.items()
        if row["weighted_prime_correlation_positive"])
    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "even_target_residue_count": len(margin_rows),
        "target_range": (targets[0], targets[-1]),
        "tested_target_count": len(targets),
        "minimum_margin_residue": minimum_margin_residue,
        "minimum_sufficient_uniform_relative_error_margin": (
            margin_rows[minimum_margin_residue][
                "sufficient_uniform_relative_error_margin"]),
        "maximum_sufficient_uniform_relative_error_margin": max(margins),
        "mean_sufficient_uniform_relative_error_margin": (
            math.fsum(margins) / len(margins)),
        "margin_rows": margin_rows,
        "observed_rows": observed_rows,
        "observed_margin_condition_success_count": len(
            observed_margin_successes),
        "observed_positive_weighted_sum_count": len(
            observed_positive_targets),
        "uniform_residue_margin_computed": True,
        "required_pointwise_bound": (
            "for every even residue n, strict-central prime-pair weights "
            "over A_n must have max relative residue discrepancy below the "
            "listed sufficient margin"),
        "pointwise_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def combined_coefficient_support_descent_receipt(tolerance=1e-9):
    """Reconstruct CRT-support components and test lower-modulus descent.

    The full character spectrum is broad, but its CRT support may be
    low-dimensional.  For each support group, this receipt reconstructs the
    corresponding coefficient component on ``U_10010`` and tests whether it
    descends through the natural modulus ``2*prod(support primes)``.  Passing
    does not prove a prime-correlation estimate; it identifies the smaller
    moduli on which such estimates would need to act.
    """
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    values = np.asarray(tuple(
        coefficient["aggregate_coefficient_by_unit_residue"][unit]
        for unit in units), dtype=np.complex128)
    mean = complex(np.mean(values))
    centered = values - mean
    _, labels, character_table = _unit_character_table(period, units)
    character_coefficients = (
        np.conjugate(character_table) @ centered / len(units))
    factor_primes = (5, 7, 11, 13)
    support_to_indices = {}
    for index, label in enumerate(labels):
        support = tuple(
            prime for prime, exponent in zip(factor_primes, label)
            if exponent != 0)
        support_to_indices.setdefault(support, []).append(index)

    total_energy = float(np.sum(np.abs(character_coefficients) ** 2))
    support_rows = []
    reconstructed = np.full(len(units), mean, dtype=np.complex128)
    for support, indices in sorted(
            support_to_indices.items(),
            key=lambda item: sum(
                abs(character_coefficients[index]) ** 2
                for index in item[1]),
            reverse=True):
        masked = np.zeros_like(character_coefficients)
        masked[indices] = character_coefficients[indices]
        component = character_table.T @ masked
        reconstructed += component
        energy = float(np.sum(np.abs(masked) ** 2))
        modulus = 2
        for prime in support:
            modulus *= prime
        grouped = {}
        for unit, value in zip(units, component):
            grouped.setdefault(unit % modulus, []).append(value)
        grouped_means = {
            residue: _complex_fsum(values) / len(values)
            for residue, values in grouped.items()}
        descent_error = max(
            abs(value - grouped_means[unit % modulus])
            for unit, value in zip(units, component))
        component_scale = max(1.0, float(np.linalg.norm(component)))
        support_rows.append({
            "support": support,
            "natural_modulus": modulus,
            "character_count": len(indices),
            "unit_residue_count": len(grouped_means),
            "energy": energy,
            "energy_fraction": energy / total_energy if total_energy else 0.0,
            "component_l2": float(np.linalg.norm(component)),
            "descent_relative_error": descent_error / component_scale,
            "descends_to_natural_modulus": bool(
                descent_error / component_scale <= tolerance),
        })
    reconstruction_error = float(
        np.linalg.norm(reconstructed - values)
        / max(1.0, float(np.linalg.norm(values))))
    nonzero_rows = tuple(
        row for row in support_rows
        if row["energy_fraction"] > tolerance)
    natural_moduli = tuple(sorted({
        row["natural_modulus"] for row in nonzero_rows
        if row["support"]}))
    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "unit_group_order": len(units),
        "principal_mean": mean,
        "factor_primes": factor_primes,
        "total_character_energy": total_energy,
        "support_rows": tuple(support_rows),
        "nonzero_support_rows": nonzero_rows,
        "nonzero_natural_moduli": natural_moduli,
        "maximum_support_descent_relative_error": max(
            row["descent_relative_error"] for row in support_rows),
        "component_reconstruction_relative_error": reconstruction_error,
        "all_nonzero_supports_descend_to_lower_moduli": all(
            row["descends_to_natural_modulus"] for row in nonzero_rows),
        "full_modulus_uniformity_not_required_by_coefficient_structure": bool(
            period not in natural_moduli),
        "support_descent_measured": True,
        "pointwise_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def combined_coefficient_support_contribution_receipt(
        targets=(10424, 14138, 88346), tolerance=1e-9):
    """Decompose selected direct prime correlations by CRT support component."""
    targets = tuple(targets)
    if (not targets or any(type(target) is not int or target < 40
                           or target % 2 for target in targets)):
        raise ValueError("targets must be even integers at least 40")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    values = np.asarray(tuple(
        coefficient["aggregate_coefficient_by_unit_residue"][unit]
        for unit in units), dtype=np.complex128)
    mean = complex(np.mean(values))
    centered = values - mean
    _, labels, character_table = _unit_character_table(period, units)
    character_coefficients = (
        np.conjugate(character_table) @ centered / len(units))
    factor_primes = (5, 7, 11, 13)
    support_indices = {}
    for index, label in enumerate(labels):
        support = tuple(
            prime for prime, exponent in zip(factor_primes, label)
            if exponent != 0)
        support_indices.setdefault(support, []).append(index)
    components = {"principal": np.full(
        len(units), mean, dtype=np.complex128)}
    for support, indices in support_indices.items():
        if not support:
            continue
        masked = np.zeros_like(character_coefficients)
        masked[indices] = character_coefficients[indices]
        energy = float(np.sum(np.abs(masked) ** 2))
        if energy > tolerance:
            components[support] = character_table.T @ masked
    unit_index = {unit: index for index, unit in enumerate(units)}
    primes = _prime_table(max(targets))

    rows = {}
    maximum_reconstruction_error = 0.0
    for target in targets:
        lower = target // 3
        upper = target - lower
        contribution_sums = {name: 0.0j for name in components}
        pair_count = 0
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                pair_count += 1
                index = unit_index[prime % period]
                weight = math.log(prime) * math.log(partner)
                for name, component in components.items():
                    contribution_sums[name] += component[index] * weight
        reconstructed = _complex_fsum(contribution_sums.values())
        direct = _complex_fsum(
            coefficient["aggregate_coefficient_by_unit_residue"][prime % period]
            * math.log(prime) * math.log(target - prime)
            for prime in range(max(2, lower + 1), min(target, upper))
            if primes[prime] and primes[target - prime])
        reconstruction_error = abs(reconstructed - direct) / max(
            1.0, abs(reconstructed), abs(direct))
        maximum_reconstruction_error = max(
            maximum_reconstruction_error, reconstruction_error)
        sorted_contributions = tuple(
            (name, complex(value))
            for name, value in sorted(
                contribution_sums.items(),
                key=lambda item: abs(item[1].real),
                reverse=True))
        rows[target] = {
            "strict_central_interval": (lower, upper),
            "ordered_central_prime_pair_count": pair_count,
            "direct_weighted_prime_correlation": direct,
            "reconstructed_from_support_components": reconstructed,
            "support_reconstruction_relative_error": reconstruction_error,
            "contributions_by_support": {
                name: complex(value)
                for name, value in contribution_sums.items()},
            "contributions_sorted_by_real_magnitude": sorted_contributions,
            "largest_negative_support": next((
                name for name, value in sorted_contributions
                if value.real < -tolerance), None),
        }

    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "targets": targets,
        "component_labels": tuple(components),
        "rows": rows,
        "maximum_support_reconstruction_relative_error": (
            maximum_reconstruction_error),
        "support_contribution_diagnostic_measured": True,
        "pointwise_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def combined_coefficient_centered_error_envelope_receipt(
        base_target_minimum=10000, cycle_count=3,
        targets_per_cycle=None, tolerance=1e-9):
    """Measure the direct inequality principal + centered error > 0.

    The assembled coefficient has positive principal mean.  For actual
    strict-central prime pairs, write the direct weighted sum as

        principal_mean * W_unit(N) + centered_error(N).

    Positivity follows if the real centered-to-principal ratio is greater than
    ``-1``.  This receipt measures that ratio on finite period cycles; it does
    not prove the required pointwise bound.
    """
    if (type(base_target_minimum) is not int or base_target_minimum < 40
            or base_target_minimum % 2):
        raise ValueError("base_target_minimum must be an even integer >=40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (targets_per_cycle is not None
            and (type(targets_per_cycle) is not int
                 or targets_per_cycle < 1)):
        raise ValueError("targets_per_cycle must be None or a positive integer")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    full_cycle_targets = period // 2
    per_cycle = (
        full_cycle_targets if targets_per_cycle is None
        else min(targets_per_cycle, full_cycle_targets))
    maximum_target = (
        base_target_minimum
        + (cycle_count - 1) * period
        + 2 * (per_cycle - 1))
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    coefficient_by_residue = coefficient[
        "aggregate_coefficient_by_unit_residue"]
    principal_mean = _complex_fsum(
        coefficient_by_residue[unit] for unit in units) / len(units)
    centered_by_residue = {
        unit: coefficient_by_residue[unit] - principal_mean
        for unit in units}
    primes = _prime_table(maximum_target)

    def evaluate(target):
        lower = target // 3
        upper = target - lower
        unit_weight = 0.0
        centered_terms = []
        pair_count = 0
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                pair_count += 1
                weight = math.log(prime) * math.log(partner)
                unit_weight += weight
                centered_terms.append(centered_by_residue[prime % period]
                                      * weight)
        principal = principal_mean * unit_weight
        centered = _complex_fsum(centered_terms)
        total = principal + centered
        ratio = (
            centered.real / principal.real
            if abs(principal.real) > tolerance else math.nan)
        return {
            "target": target,
            "target_residue": target % period,
            "ordered_central_prime_pair_count": pair_count,
            "principal_contribution": principal,
            "centered_error": centered,
            "direct_weighted_prime_correlation": total,
            "centered_to_principal_real_ratio": ratio,
            "positive": bool(total.real > tolerance),
        }

    cycle_rows = {}
    global_minimum_row = None
    for cycle_index in range(cycle_count):
        start = base_target_minimum + cycle_index * period
        rows = tuple(evaluate(start + 2 * offset)
                     for offset in range(per_cycle))
        minimum_row = min(
            rows, key=lambda row: row["centered_to_principal_real_ratio"])
        negative_rows = tuple(row for row in rows if not row["positive"])
        if (global_minimum_row is None
                or minimum_row["centered_to_principal_real_ratio"]
                < global_minimum_row["centered_to_principal_real_ratio"]):
            global_minimum_row = minimum_row
        cycle_rows[cycle_index] = {
            "target_range": (rows[0]["target"], rows[-1]["target"]),
            "tested_target_count": len(rows),
            "negative_or_zero_weighted_sum_count": len(negative_rows),
            "minimum_centered_to_principal_target": minimum_row["target"],
            "minimum_centered_to_principal_ratio": minimum_row[
                "centered_to_principal_real_ratio"],
            "mean_centered_to_principal_ratio": math.fsum(
                row["centered_to_principal_real_ratio"] for row in rows)
            / len(rows),
            "negative_or_zero_targets": tuple(row["target"]
                                              for row in negative_rows),
        }

    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "principal_mean": principal_mean,
        "base_target_minimum": base_target_minimum,
        "cycle_count": cycle_count,
        "targets_per_cycle": per_cycle,
        "full_cycle_targets": full_cycle_targets,
        "full_cycles_scanned": bool(per_cycle == full_cycle_targets),
        "cycle_rows": cycle_rows,
        "global_minimum_centered_to_principal_target": (
            global_minimum_row["target"]),
        "global_minimum_centered_to_principal_ratio": (
            global_minimum_row["centered_to_principal_real_ratio"]),
        "all_scanned_targets_positive": all(
            row["negative_or_zero_weighted_sum_count"] == 0
            for row in cycle_rows.values()),
        "sufficient_pointwise_target": (
            "prove centered_error(N).real / principal(N).real > -1 "
            "for every remaining strict-central target"),
        "centered_error_envelope_measured": True,
        "pointwise_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def combined_coefficient_support_cycle_envelope_receipt(
        base_target_minimum=10000, cycle_count=3,
        targets_per_cycle=None, tolerance=1e-9):
    """Measure lower-modulus support ratios across period cycles."""
    if (type(base_target_minimum) is not int or base_target_minimum < 40
            or base_target_minimum % 2):
        raise ValueError("base_target_minimum must be an even integer >=40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (targets_per_cycle is not None
            and (type(targets_per_cycle) is not int
                 or targets_per_cycle < 1)):
        raise ValueError("targets_per_cycle must be None or a positive integer")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    full_cycle_targets = period // 2
    per_cycle = (
        full_cycle_targets if targets_per_cycle is None
        else min(targets_per_cycle, full_cycle_targets))
    maximum_target = (
        base_target_minimum
        + (cycle_count - 1) * period
        + 2 * (per_cycle - 1))
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    values = np.asarray(tuple(
        coefficient["aggregate_coefficient_by_unit_residue"][unit]
        for unit in units), dtype=np.complex128)
    principal_mean = complex(np.mean(values))
    centered = values - principal_mean
    _, labels, character_table = _unit_character_table(period, units)
    character_coefficients = (
        np.conjugate(character_table) @ centered / len(units))
    factor_primes = (5, 7, 11, 13)
    support_indices = {}
    for index, label in enumerate(labels):
        support = tuple(
            prime for prime, exponent in zip(factor_primes, label)
            if exponent != 0)
        support_indices.setdefault(support, []).append(index)
    components = {}
    for support, indices in support_indices.items():
        if not support:
            continue
        masked = np.zeros_like(character_coefficients)
        masked[indices] = character_coefficients[indices]
        energy = float(np.sum(np.abs(masked) ** 2))
        if energy > tolerance:
            components[support] = character_table.T @ masked
    unit_index = {unit: index for index, unit in enumerate(units)}
    primes = _prime_table(maximum_target)

    def evaluate(target):
        lower = target // 3
        upper = target - lower
        unit_weight = 0.0
        component_sums = {support: 0.0j for support in components}
        pair_count = 0
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                pair_count += 1
                weight = math.log(prime) * math.log(partner)
                unit_weight += weight
                unit = prime % period
                index = unit_index[unit]
                for support, component in components.items():
                    component_sums[support] += component[index] * weight
        principal = principal_mean * unit_weight
        ratios = {
            support: float(
                value.real / principal.real
                if abs(principal.real) > tolerance else math.nan)
            for support, value in component_sums.items()}
        centered_ratio = float(math.fsum(ratios.values()))
        return {
            "target": target,
            "target_residue": target % period,
            "ordered_central_prime_pair_count": pair_count,
            "principal_contribution": principal,
            "component_contributions": {
                support: complex(value)
                for support, value in component_sums.items()},
            "component_to_principal_ratios": ratios,
            "centered_to_principal_ratio": centered_ratio,
            "positive": bool(1 + centered_ratio > tolerance),
        }

    cycle_rows = {}
    global_support_minima = {
        support: None for support in components}
    global_centered_minimum = None
    for cycle_index in range(cycle_count):
        start = base_target_minimum + cycle_index * period
        rows = tuple(evaluate(start + 2 * offset)
                     for offset in range(per_cycle))
        centered_minimum = min(
            rows, key=lambda row: row["centered_to_principal_ratio"])
        if (global_centered_minimum is None
                or centered_minimum["centered_to_principal_ratio"]
                < global_centered_minimum["centered_to_principal_ratio"]):
            global_centered_minimum = centered_minimum
        support_summaries = {}
        for support in components:
            support_minimum = min(
                rows,
                key=lambda row: row[
                    "component_to_principal_ratios"][support])
            support_maximum = max(
                rows,
                key=lambda row: row[
                    "component_to_principal_ratios"][support])
            if (global_support_minima[support] is None
                    or support_minimum[
                        "component_to_principal_ratios"][support]
                    < global_support_minima[support][
                        "component_to_principal_ratios"][support]):
                global_support_minima[support] = support_minimum
            support_summaries[support] = {
                "minimum_ratio_target": support_minimum["target"],
                "minimum_ratio": support_minimum[
                    "component_to_principal_ratios"][support],
                "maximum_ratio_target": support_maximum["target"],
                "maximum_ratio": support_maximum[
                    "component_to_principal_ratios"][support],
                "mean_ratio": math.fsum(
                    row["component_to_principal_ratios"][support]
                    for row in rows) / len(rows),
            }
        cycle_rows[cycle_index] = {
            "target_range": (rows[0]["target"], rows[-1]["target"]),
            "tested_target_count": len(rows),
            "negative_or_zero_count": sum(
                1 for row in rows if not row["positive"]),
            "minimum_centered_ratio_target": centered_minimum["target"],
            "minimum_centered_ratio": centered_minimum[
                "centered_to_principal_ratio"],
            "support_summaries": support_summaries,
        }

    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "principal_mean": principal_mean,
        "cycle_count": cycle_count,
        "targets_per_cycle": per_cycle,
        "full_cycle_targets": full_cycle_targets,
        "component_supports": tuple(components),
        "cycle_rows": cycle_rows,
        "global_minimum_centered_ratio_target": (
            global_centered_minimum["target"]),
        "global_minimum_centered_ratio": global_centered_minimum[
            "centered_to_principal_ratio"],
        "global_support_minima": {
            support: {
                "target": row["target"],
                "ratio": row["component_to_principal_ratios"][support],
            }
            for support, row in global_support_minima.items()},
        "dominant_negative_support_at_global_minimum": min(
            global_centered_minimum["component_to_principal_ratios"],
            key=lambda support: global_centered_minimum[
                "component_to_principal_ratios"][support]),
        "support_cycle_envelope_measured": True,
        "pointwise_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def combined_coefficient_lower_modulus_deviation_receipt(
        targets=(10424, 14138, 88346),
        supports=((11, 13), (5, 7), (7, 11)), tolerance=1e-9):
    """Compare lower-modulus support actions with local predictions.

    This is the q286-focused diagnostic suggested by the support-cycle
    envelope.  For each selected CRT support component, it computes:

    * the actual strict-central prime-pair contribution;
    * the lower-modulus local prediction using the total prime-pair weight;
    * the deviation between actual and local prediction.

    The result identifies whether bad direct targets are explained by a bad
    lower-modulus local main or by a genuine prime-residue discrepancy.
    """
    targets = tuple(targets)
    supports = tuple(tuple(support) for support in supports)
    if (not targets or any(type(target) is not int or target < 40
                           or target % 2 for target in targets)):
        raise ValueError("targets must be even integers at least 40")
    valid_supports = {
        (13,), (11,), (11, 13), (7,), (7, 11),
        (5,), (5, 13), (5, 7)}
    if not supports or any(support not in valid_supports
                           for support in supports):
        raise ValueError("supports must be nonempty valid CRT supports")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    values = np.asarray(tuple(
        coefficient["aggregate_coefficient_by_unit_residue"][unit]
        for unit in units), dtype=np.complex128)
    principal_mean = complex(np.mean(values))
    centered = values - principal_mean
    _, labels, character_table = _unit_character_table(period, units)
    character_coefficients = (
        np.conjugate(character_table) @ centered / len(units))
    factor_primes = (5, 7, 11, 13)
    support_indices = {}
    for index, label in enumerate(labels):
        support = tuple(
            prime for prime, exponent in zip(factor_primes, label)
            if exponent != 0)
        support_indices.setdefault(support, []).append(index)

    component_by_support = {}
    lower_modulus_values = {}
    for support in supports:
        masked = np.zeros_like(character_coefficients)
        masked[support_indices[support]] = character_coefficients[
            support_indices[support]]
        component = character_table.T @ masked
        modulus = 2
        for prime in support:
            modulus *= prime
        grouped = {}
        for unit, value in zip(units, component):
            grouped.setdefault(unit % modulus, []).append(value)
        lower_values = {
            residue: _complex_fsum(values) / len(values)
            for residue, values in grouped.items()}
        component_by_support[support] = component
        lower_modulus_values[support] = (modulus, lower_values)
    unit_index = {unit: index for index, unit in enumerate(units)}
    primes = _prime_table(max(targets))

    rows = {}
    for target in targets:
        lower = target // 3
        upper = target - lower
        pairs = []
        total_weight = 0.0
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                weight = math.log(prime) * math.log(partner)
                pairs.append((prime, weight))
                total_weight += weight
        principal_contribution = principal_mean * total_weight
        support_rows = {}
        for support in supports:
            modulus, lower_values = lower_modulus_values[support]
            actual = _complex_fsum(
                lower_values[prime % modulus] * weight
                for prime, weight in pairs)
            admissible = tuple(
                residue for residue in lower_values
                if math.gcd((target - residue) % modulus, modulus) == 1)
            local_sum = _complex_fsum(lower_values[residue]
                                      for residue in admissible)
            predicted = local_sum * total_weight / len(admissible)
            deviation = actual - predicted
            weights_by_residue = {residue: 0.0 for residue in admissible}
            for prime, weight in pairs:
                residue = prime % modulus
                if residue in weights_by_residue:
                    weights_by_residue[residue] += weight
            mean_weight = total_weight / len(admissible)
            nonzero_residue_count = sum(
                1 for weight in weights_by_residue.values()
                if weight > tolerance)
            maximum_weight_ratio = (
                max(weights_by_residue.values()) / mean_weight
                if mean_weight > tolerance else math.inf)
            support_rows[support] = {
                "natural_modulus": modulus,
                "admissible_residue_count": len(admissible),
                "nonzero_prime_residue_count": nonzero_residue_count,
                "maximum_residue_weight_to_mean_ratio": (
                    maximum_weight_ratio),
                "actual_contribution": actual,
                "local_prediction": predicted,
                "deviation_from_local_prediction": deviation,
                "actual_to_principal_ratio": float(
                    actual.real / principal_contribution.real
                    if abs(principal_contribution.real) > tolerance
                    else math.nan),
                "local_prediction_to_principal_ratio": float(
                    predicted.real / principal_contribution.real
                    if abs(principal_contribution.real) > tolerance
                    else math.nan),
                "deviation_to_principal_ratio": float(
                    deviation.real / principal_contribution.real
                    if abs(principal_contribution.real) > tolerance
                    else math.nan),
                "local_prediction_has_bad_sign": bool(
                    predicted.real < -tolerance),
            }
        dominant_deviation_support = min(
            supports,
            key=lambda support: support_rows[support][
                "deviation_to_principal_ratio"])
        rows[target] = {
            "strict_central_interval": (lower, upper),
            "ordered_central_prime_pair_count": len(pairs),
            "total_prime_pair_weight": total_weight,
            "principal_contribution": principal_contribution,
            "support_rows": support_rows,
            "dominant_negative_deviation_support": (
                dominant_deviation_support),
            "dominant_negative_deviation_to_principal_ratio": (
                support_rows[dominant_deviation_support][
                    "deviation_to_principal_ratio"]),
        }

    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "targets": targets,
        "supports": supports,
        "rows": rows,
        "lower_modulus_deviation_measured": True,
        "any_support_local_prediction_has_bad_sign": bool(any(
            support_row["local_prediction_has_bad_sign"]
            for row in rows.values()
            for support_row in row["support_rows"].values())),
        "dominant_support_local_prediction_has_bad_sign": bool(any(
            row["support_rows"][
                row["dominant_negative_deviation_support"]][
                    "local_prediction_has_bad_sign"]
            for row in rows.values())),
        "q286_local_prediction_positive_on_all_targets": bool(
            (11, 13) in supports
            and all(not row["support_rows"][(11, 13)][
                "local_prediction_has_bad_sign"]
                    for row in rows.values())),
        "dominant_support_deviation_is_q286_on_all_targets": bool(all(
            row["dominant_negative_deviation_support"] == (11, 13)
            for row in rows.values())),
        "pointwise_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_residue_discrepancy_profile_receipt(
        targets=(10424, 14138, 88346), top_count=10, tolerance=1e-9):
    """Attribute the q286 deviation to individual residue fibers.

    The lower-modulus local prediction subtracts the uniform q286 residue
    model from the actual strict-central prime-pair weights.  This receipt
    expands the difference as

        sum_r (W_N(r)-mean_s W_N(s))*C_q286(r),

    where r ranges over admissible unit residues modulo 286.
    """
    targets = tuple(targets)
    if (not targets or any(type(target) is not int or target < 40
                           or target % 2 for target in targets)):
        raise ValueError("targets must be even integers at least 40")
    if type(top_count) is not int or top_count < 1:
        raise ValueError("top_count must be a positive integer")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    values = np.asarray(tuple(
        coefficient["aggregate_coefficient_by_unit_residue"][unit]
        for unit in units), dtype=np.complex128)
    principal_mean = complex(np.mean(values))
    centered = values - principal_mean
    _, labels, character_table = _unit_character_table(period, units)
    character_coefficients = (
        np.conjugate(character_table) @ centered / len(units))
    factor_primes = (5, 7, 11, 13)
    support_indices = {}
    for index, label in enumerate(labels):
        support = tuple(
            prime for prime, exponent in zip(factor_primes, label)
            if exponent != 0)
        support_indices.setdefault(support, []).append(index)

    support = (11, 13)
    masked = np.zeros_like(character_coefficients)
    masked[support_indices[support]] = character_coefficients[
        support_indices[support]]
    component = character_table.T @ masked
    modulus = 286
    grouped = {}
    for unit, value in zip(units, component):
        grouped.setdefault(unit % modulus, []).append(value)
    lower_values = {
        residue: _complex_fsum(values) / len(values)
        for residue, values in grouped.items()}
    primes = _prime_table(max(targets))

    rows = {}
    maximum_deviation_reconstruction_error = 0.0
    all_weight_coefficient_correlations_negative = True
    all_negative_coefficient_weights_overrepresented = True
    all_top_negative_lists_show_two_sided_imbalance = True
    for target in targets:
        lower = target // 3
        upper = target - lower
        pairs = []
        total_weight = 0.0
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                weight = math.log(prime) * math.log(partner)
                pairs.append((prime, weight))
                total_weight += weight
        principal_contribution = principal_mean * total_weight
        admissible = tuple(
            residue for residue in lower_values
            if math.gcd((target - residue) % modulus, modulus) == 1)
        weights_by_residue = {residue: 0.0 for residue in admissible}
        for prime, weight in pairs:
            residue = prime % modulus
            if residue in weights_by_residue:
                weights_by_residue[residue] += weight
        mean_weight = total_weight / len(admissible)
        actual = _complex_fsum(
            lower_values[prime % modulus] * weight
            for prime, weight in pairs)
        predicted = (
            _complex_fsum(lower_values[residue]
                          for residue in admissible)
            * mean_weight)
        deviation = actual - predicted
        residue_rows = []
        negative_coefficient_weight = 0.0
        negative_coefficient_uniform_weight = 0.0
        positive_coefficient_weight = 0.0
        positive_coefficient_uniform_weight = 0.0
        for residue in admissible:
            coefficient_value = lower_values[residue]
            weight = weights_by_residue[residue]
            weight_delta = weight - mean_weight
            contribution = coefficient_value * weight_delta
            coefficient_real = float(coefficient_value.real)
            if coefficient_real < -tolerance:
                negative_coefficient_weight += weight
                negative_coefficient_uniform_weight += mean_weight
            elif coefficient_real > tolerance:
                positive_coefficient_weight += weight
                positive_coefficient_uniform_weight += mean_weight
            residue_rows.append({
                "residue": residue,
                "coefficient": coefficient_value,
                "coefficient_real": coefficient_real,
                "prime_pair_weight": weight,
                "uniform_weight": mean_weight,
                "weight_delta": weight_delta,
                "weight_to_uniform_ratio": (
                    weight / mean_weight if mean_weight else math.inf),
                "deviation_contribution": contribution,
                "deviation_to_principal_ratio": float(
                    contribution.real / principal_contribution.real
                    if abs(principal_contribution.real) > tolerance
                    else math.nan),
            })
        reconstructed_deviation = _complex_fsum(
            row["deviation_contribution"] for row in residue_rows)
        deviation_reconstruction_error = abs(
            reconstructed_deviation - deviation) / max(1.0, abs(deviation))
        maximum_deviation_reconstruction_error = max(
            maximum_deviation_reconstruction_error,
            deviation_reconstruction_error)
        deltas = tuple(row["weight_delta"] for row in residue_rows)
        coefficient_reals = tuple(row["coefficient_real"]
                                  for row in residue_rows)
        dot = math.fsum(
            delta * coefficient_real
            for delta, coefficient_real in zip(deltas, coefficient_reals))
        delta_norm = math.sqrt(math.fsum(delta * delta for delta in deltas))
        coefficient_norm = math.sqrt(math.fsum(
            value * value for value in coefficient_reals))
        correlation = (
            dot / (delta_norm * coefficient_norm)
            if delta_norm and coefficient_norm else 0.0)
        cauchy_bound = delta_norm * coefficient_norm
        cauchy_bound_to_principal_ratio = (
            cauchy_bound / principal_contribution.real
            if abs(principal_contribution.real) > tolerance else math.nan)
        actual_abs_fraction_of_cauchy_bound = (
            abs(deviation.real) / cauchy_bound
            if cauchy_bound > tolerance else math.nan)
        relative_l2_deviation = (
            delta_norm / total_weight if total_weight > tolerance
            else math.nan)
        uniform_l2_weight = mean_weight * math.sqrt(len(admissible))
        coefficient_of_variation = (
            delta_norm / uniform_l2_weight
            if uniform_l2_weight > tolerance else math.nan)
        unit_principal_l2_threshold = (
            principal_mean.real / coefficient_norm
            if coefficient_norm > tolerance else math.inf)
        all_weight_coefficient_correlations_negative = bool(
            all_weight_coefficient_correlations_negative
            and correlation < -tolerance)
        negative_weight_ratio = (
            negative_coefficient_weight / negative_coefficient_uniform_weight
            if negative_coefficient_uniform_weight else math.nan)
        positive_weight_ratio = (
            positive_coefficient_weight / positive_coefficient_uniform_weight
            if positive_coefficient_uniform_weight else math.nan)
        all_negative_coefficient_weights_overrepresented = bool(
            all_negative_coefficient_weights_overrepresented
            and negative_weight_ratio > 1.0 + tolerance)
        top_negative = tuple(sorted(
            residue_rows,
            key=lambda row: row["deviation_contribution"].real)[:top_count])
        top_positive = tuple(sorted(
            residue_rows,
            key=lambda row: row["deviation_contribution"].real,
            reverse=True)[:top_count])
        top_negative_sum = _complex_fsum(
            row["deviation_contribution"] for row in top_negative)
        top_negative_underweighted_positive_count = sum(
            1 for row in top_negative
            if (row["coefficient_real"] > tolerance
                and row["weight_delta"] < -tolerance))
        top_negative_overweighted_negative_count = sum(
            1 for row in top_negative
            if (row["coefficient_real"] < -tolerance
                and row["weight_delta"] > tolerance))
        all_top_negative_lists_show_two_sided_imbalance = bool(
            all_top_negative_lists_show_two_sided_imbalance
            and top_negative_underweighted_positive_count > 0
            and top_negative_overweighted_negative_count > 0)
        rows[target] = {
            "strict_central_interval": (lower, upper),
            "ordered_central_prime_pair_count": len(pairs),
            "total_prime_pair_weight": total_weight,
            "principal_contribution": principal_contribution,
            "admissible_residue_count": len(admissible),
            "mean_residue_weight": mean_weight,
            "actual_contribution": actual,
            "local_prediction": predicted,
            "deviation_from_local_prediction": deviation,
            "reconstructed_deviation": reconstructed_deviation,
            "deviation_reconstruction_error": (
                deviation_reconstruction_error),
            "deviation_to_principal_ratio": float(
                deviation.real / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "residue_weight_l2_deviation": delta_norm,
            "q286_coefficient_real_l2": coefficient_norm,
            "cauchy_bound_to_principal_ratio": float(
                cauchy_bound_to_principal_ratio),
            "actual_abs_fraction_of_cauchy_bound": float(
                actual_abs_fraction_of_cauchy_bound),
            "l2_deviation_to_total_weight": float(relative_l2_deviation),
            "residue_weight_coefficient_of_variation": float(
                coefficient_of_variation),
            "unit_principal_l2_sufficiency_threshold": float(
                unit_principal_l2_threshold),
            "l2_sufficiency_for_unit_principal_satisfied": bool(
                relative_l2_deviation < unit_principal_l2_threshold),
            "weight_coefficient_real_correlation": correlation,
            "negative_coefficient_weight_to_uniform_ratio": (
                negative_weight_ratio),
            "positive_coefficient_weight_to_uniform_ratio": (
                positive_weight_ratio),
            "negative_minus_positive_weight_ratio": (
                negative_weight_ratio - positive_weight_ratio),
            "top_negative_deviation_rows": top_negative,
            "top_positive_deviation_rows": top_positive,
            "top_negative_underweighted_positive_count": (
                top_negative_underweighted_positive_count),
            "top_negative_overweighted_negative_count": (
                top_negative_overweighted_negative_count),
            "top_negative_deviation_to_total_deviation_ratio": float(
                top_negative_sum.real / deviation.real
                if abs(deviation.real) > tolerance else math.nan),
        }

    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "support": support,
        "natural_modulus": modulus,
        "targets": targets,
        "top_count": top_count,
        "rows": rows,
        "maximum_deviation_reconstruction_error": (
            maximum_deviation_reconstruction_error),
        "all_weight_coefficient_correlations_negative": bool(
            all_weight_coefficient_correlations_negative),
        "all_negative_coefficient_weights_overrepresented": bool(
            all_negative_coefficient_weights_overrepresented),
        "all_top_negative_lists_show_two_sided_imbalance": bool(
            all_top_negative_lists_show_two_sided_imbalance),
        "q286_residue_discrepancy_profile_measured": True,
        "pointwise_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_character_imbalance_receipt(
        targets=(10424, 14138, 88346), top_count=10, tolerance=1e-9):
    """Move the q286 residue discrepancy into character coordinates.

    This is the same q286 deviation as
    ``q286_residue_discrepancy_profile_receipt``, but written as a finite sum
    of nonprincipal Dirichlet-character imbalance terms modulo 286.  It names
    the exact character-sum object an analytic signed estimate would need to
    bound.
    """
    targets = tuple(targets)
    if (not targets or any(type(target) is not int or target < 40
                           or target % 2 for target in targets)):
        raise ValueError("targets must be even integers at least 40")
    if type(top_count) is not int or top_count < 1:
        raise ValueError("top_count must be a positive integer")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    period_units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    values = np.asarray(tuple(
        coefficient["aggregate_coefficient_by_unit_residue"][unit]
        for unit in period_units), dtype=np.complex128)
    principal_mean = complex(np.mean(values))
    centered = values - principal_mean
    _, period_labels, period_character_table = _unit_character_table(
        period, period_units)
    period_character_coefficients = (
        np.conjugate(period_character_table) @ centered / len(period_units))
    factor_primes = (5, 7, 11, 13)
    support_indices = {}
    for index, label in enumerate(period_labels):
        support = tuple(
            prime for prime, exponent in zip(factor_primes, label)
            if exponent != 0)
        support_indices.setdefault(support, []).append(index)

    support = (11, 13)
    masked = np.zeros_like(period_character_coefficients)
    masked[support_indices[support]] = period_character_coefficients[
        support_indices[support]]
    component = period_character_table.T @ masked
    modulus = 286
    grouped = {}
    for unit, value in zip(period_units, component):
        grouped.setdefault(unit % modulus, []).append(value)
    lower_values = {
        residue: _complex_fsum(values) / len(values)
        for residue, values in grouped.items()}

    units = tuple(sorted(lower_values))
    coefficient_values = np.asarray(tuple(
        lower_values[unit] for unit in units), dtype=np.complex128)
    odd_primes, labels, character_table = _unit_character_table(
        modulus, units)
    character_coefficients = (
        np.conjugate(character_table) @ coefficient_values / len(units))
    coefficient_reconstruction = character_table.T @ character_coefficients
    coefficient_reconstruction_error = float(
        np.linalg.norm(coefficient_reconstruction - coefficient_values)
        / max(1.0, np.linalg.norm(coefficient_values)))
    active_labels = tuple(
        label for label, value in zip(labels, character_coefficients)
        if abs(value) > tolerance)
    active_both_prime_support_count = sum(
        1 for label in active_labels if label[0] != 0 and label[1] != 0)
    active_character_energy = float(np.sum(
        np.abs(character_coefficients) ** 2))
    top_coefficient_rows = tuple({
        "label": label,
        "coefficient": complex(value),
        "energy_fraction": (
            float(abs(value) ** 2) / active_character_energy
            if active_character_energy else 0.0),
    } for value, label in sorted(
        zip(character_coefficients, labels),
        key=lambda item: abs(item[0]) ** 2,
        reverse=True)[:top_count])

    unit_index = {unit: index for index, unit in enumerate(units)}
    primes = _prime_table(max(targets))
    rows = {}
    maximum_deviation_reconstruction_error = 0.0
    for target in targets:
        lower = target // 3
        upper = target - lower
        total_weight = 0.0
        weights = np.zeros(len(units), dtype=np.float64)
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                weight = math.log(prime) * math.log(partner)
                total_weight += weight
                weights[unit_index[prime % modulus]] += weight
        principal_contribution = principal_mean * total_weight
        admissible_mask = np.asarray(tuple(
            math.gcd((target - unit) % modulus, modulus) == 1
            for unit in units), dtype=bool)
        admissible_count = int(np.sum(admissible_mask))
        mean_weight = total_weight / admissible_count
        weight_delta = np.zeros(len(units), dtype=np.float64)
        weight_delta[admissible_mask] = (
            weights[admissible_mask] - mean_weight)
        residue_deviation = _complex_fsum(
            coefficient_values[index] * weight_delta[index]
            for index in range(len(units)))
        imbalance_sums = character_table @ weight_delta
        character_contributions = character_coefficients * imbalance_sums
        character_deviation = _complex_fsum(character_contributions)
        deviation_reconstruction_error = abs(
            character_deviation - residue_deviation) / max(
                1.0, abs(residue_deviation))
        maximum_deviation_reconstruction_error = max(
            maximum_deviation_reconstruction_error,
            deviation_reconstruction_error)
        contribution_rows = tuple({
            "label": label,
            "coefficient": complex(coefficient_value),
            "imbalance_sum": complex(imbalance_sum),
            "contribution": complex(contribution),
            "contribution_to_principal_ratio": float(
                contribution.real / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
        } for label, coefficient_value, imbalance_sum, contribution in zip(
            labels, character_coefficients, imbalance_sums,
            character_contributions))
        top_negative = tuple(sorted(
            contribution_rows,
            key=lambda row: row["contribution"].real)[:top_count])
        top_positive = tuple(sorted(
            contribution_rows,
            key=lambda row: row["contribution"].real,
            reverse=True)[:top_count])
        top_negative_sum = _complex_fsum(
            row["contribution"] for row in top_negative)
        rows[target] = {
            "strict_central_interval": (lower, upper),
            "total_prime_pair_weight": total_weight,
            "admissible_residue_count": admissible_count,
            "principal_contribution": principal_contribution,
            "residue_deviation": residue_deviation,
            "character_deviation": character_deviation,
            "deviation_reconstruction_error": (
                deviation_reconstruction_error),
            "deviation_to_principal_ratio": float(
                residue_deviation.real / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "top_negative_character_rows": top_negative,
            "top_positive_character_rows": top_positive,
            "top_negative_character_to_total_deviation_ratio": float(
                top_negative_sum.real / residue_deviation.real
                if abs(residue_deviation.real) > tolerance else math.nan),
        }

    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "support": support,
        "natural_modulus": modulus,
        "odd_primes": odd_primes,
        "unit_group_order": len(units),
        "character_count": len(labels),
        "active_character_count": len(active_labels),
        "active_both_prime_support_count": active_both_prime_support_count,
        "active_labels_all_have_both_prime_support": bool(
            active_both_prime_support_count == len(active_labels)),
        "coefficient_reconstruction_error": (
            coefficient_reconstruction_error),
        "maximum_deviation_reconstruction_error": (
            maximum_deviation_reconstruction_error),
        "top_coefficient_character_rows": top_coefficient_rows,
        "targets": targets,
        "top_count": top_count,
        "rows": rows,
        "q286_character_imbalance_measured": True,
        "pointwise_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_character_matrix_structure_receipt(
        tolerance=1e-9, leading_count=6):
    """Measure rank structure in the q286 character coefficient matrix.

    The q286 support is naturally a matrix indexed by nontrivial characters
    modulo 11 and 13.  Low numerical rank would turn the 59 active characters
    into a small number of separable character-combination estimates.
    """
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    if type(leading_count) is not int or leading_count < 1:
        raise ValueError("leading_count must be a positive integer")

    character_receipt = q286_character_imbalance_receipt(
        targets=(10424,), top_count=120, tolerance=tolerance)
    matrix = np.zeros((10, 12), dtype=np.complex128)
    for row in character_receipt["top_coefficient_character_rows"]:
        first, second = row["label"]
        matrix[first, second] = row["coefficient"]
    active_matrix = matrix[1:, 1:]
    singular_values = np.linalg.svd(active_matrix, compute_uv=False)
    energies = singular_values ** 2
    total_energy = float(np.sum(energies))
    rank = int(np.sum(singular_values > tolerance))
    relative_rank = int(np.sum(
        singular_values > tolerance * max(1.0, float(singular_values[0]))))
    cumulative_energy = []
    running = 0.0
    for value in energies:
        running += float(value)
        cumulative_energy.append(running / total_energy if total_energy else 0.0)
    active_entries = int(np.sum(np.abs(active_matrix) > tolerance))
    return {
        "families": character_receipt["families"],
        "arithmetic_period": character_receipt["arithmetic_period"],
        "support": character_receipt["support"],
        "natural_modulus": character_receipt["natural_modulus"],
        "matrix_shape": active_matrix.shape,
        "active_character_count": (
            character_receipt["active_character_count"]),
        "active_entry_count": active_entries,
        "singular_values": tuple(float(value) for value in singular_values),
        "singular_energy_fractions": tuple(
            float(value / total_energy) if total_energy else 0.0
            for value in energies),
        "cumulative_singular_energy_fractions": tuple(cumulative_energy),
        "numerical_rank": rank,
        "relative_numerical_rank": relative_rank,
        "effective_singular_rank": (
            float(total_energy * total_energy / np.sum(energies ** 2))
            if total_energy else 0.0),
        "leading_singular_count": min(leading_count, len(singular_values)),
        "leading_singular_energy_fraction": (
            cumulative_energy[min(leading_count, len(singular_values)) - 1]
            if cumulative_energy else 0.0),
        "top_two_singular_energy_fraction": (
            cumulative_energy[1] if len(cumulative_energy) >= 2 else 0.0),
        "top_four_singular_energy_fraction": (
            cumulative_energy[3] if len(cumulative_energy) >= 4 else 0.0),
        "low_rank_compression_diagnostic_passes": bool(
            len(cumulative_energy) >= 2 and cumulative_energy[1] > .95),
        "exact_low_rank_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def dominant_support_character_matrix_structure_receipt(
        supports=((11, 13), (7, 11), (5, 7)),
        tolerance=1e-9, leading_count=6):
    """Measure separable character structure for dominant CRT supports."""
    supports = tuple(tuple(support) for support in supports)
    valid_supports = {(11, 13), (7, 11), (5, 7)}
    if not supports or any(support not in valid_supports
                           for support in supports):
        raise ValueError("supports must use dominant two-prime supports")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    if type(leading_count) is not int or leading_count < 1:
        raise ValueError("leading_count must be a positive integer")

    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    period_units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    values = np.asarray(tuple(
        coefficient["aggregate_coefficient_by_unit_residue"][unit]
        for unit in period_units), dtype=np.complex128)
    centered = values - np.mean(values)
    _, period_labels, period_character_table = _unit_character_table(
        period, period_units)
    period_character_coefficients = (
        np.conjugate(period_character_table) @ centered / len(period_units))
    factor_primes = (5, 7, 11, 13)
    support_indices = {}
    for index, label in enumerate(period_labels):
        support = tuple(
            prime for prime, exponent in zip(factor_primes, label)
            if exponent != 0)
        support_indices.setdefault(support, []).append(index)

    support_rows = {}
    for support in supports:
        masked = np.zeros_like(period_character_coefficients)
        masked[support_indices[support]] = period_character_coefficients[
            support_indices[support]]
        component = period_character_table.T @ masked
        modulus = 2
        for prime in support:
            modulus *= prime
        grouped = {}
        for unit, value in zip(period_units, component):
            grouped.setdefault(unit % modulus, []).append(value)
        lower_values = {
            residue: _complex_fsum(values) / len(values)
            for residue, values in grouped.items()}
        units = tuple(sorted(lower_values))
        coefficient_values = np.asarray(tuple(
            lower_values[unit] for unit in units), dtype=np.complex128)
        odd_primes, labels, character_table = _unit_character_table(
            modulus, units)
        character_coefficients = (
            np.conjugate(character_table) @ coefficient_values / len(units))
        reconstruction = character_table.T @ character_coefficients
        reconstruction_error = float(
            np.linalg.norm(reconstruction - coefficient_values)
            / max(1.0, np.linalg.norm(coefficient_values)))
        matrix = np.zeros(tuple(prime - 1 for prime in support),
                          dtype=np.complex128)
        for label, value in zip(labels, character_coefficients):
            matrix[label] = value
        active_matrix = matrix[tuple(
            slice(1, prime - 1) for prime in support)]
        singular_values = np.linalg.svd(active_matrix, compute_uv=False)
        energies = singular_values ** 2
        total_energy = float(np.sum(energies))
        cumulative = []
        running = 0.0
        for energy in energies:
            running += float(energy)
            cumulative.append(running / total_energy if total_energy else 0.0)
        active_labels = tuple(
            label for label, value in zip(labels, character_coefficients)
            if abs(value) > tolerance)
        both_support_count = sum(
            1 for label in active_labels
            if all(exponent != 0 for exponent in label))
        support_rows[support] = {
            "natural_modulus": modulus,
            "odd_primes": odd_primes,
            "unit_group_order": len(units),
            "character_count": len(labels),
            "active_character_count": len(active_labels),
            "active_both_prime_support_count": both_support_count,
            "active_labels_all_have_both_prime_support": bool(
                both_support_count == len(active_labels)),
            "matrix_shape": active_matrix.shape,
            "active_entry_count": int(np.sum(
                np.abs(active_matrix) > tolerance)),
            "coefficient_reconstruction_error": reconstruction_error,
            "singular_values": tuple(float(value)
                                     for value in singular_values),
            "singular_energy_fractions": tuple(
                float(energy / total_energy) if total_energy else 0.0
                for energy in energies),
            "cumulative_singular_energy_fractions": tuple(cumulative),
            "numerical_rank": int(np.sum(singular_values > tolerance)),
            "relative_numerical_rank": int(np.sum(
                singular_values
                > tolerance * max(1.0, float(singular_values[0])))),
            "effective_singular_rank": (
                float(total_energy * total_energy / np.sum(energies ** 2))
                if total_energy else 0.0),
            "leading_singular_count": min(
                leading_count, len(singular_values)),
            "leading_singular_energy_fraction": (
                cumulative[min(leading_count, len(singular_values)) - 1]
                if cumulative else 0.0),
            "top_two_singular_energy_fraction": (
                cumulative[1] if len(cumulative) >= 2
                else (cumulative[0] if cumulative else 0.0)),
            "top_four_singular_energy_fraction": (
                cumulative[3] if len(cumulative) >= 4
                else (cumulative[-1] if cumulative else 0.0)),
            "low_rank_compression_diagnostic_passes": bool(
                len(cumulative) >= 2 and cumulative[1] > .9),
        }
    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "supports": supports,
        "support_rows": support_rows,
        "all_supports_have_both_prime_character_support": bool(all(
            row["active_labels_all_have_both_prime_support"]
            for row in support_rows.values())),
        "all_supports_have_low_rank_compression": bool(all(
            row["low_rank_compression_diagnostic_passes"]
            for row in support_rows.values())),
        "dominant_support_character_matrix_structure_measured": True,
        "exact_low_rank_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def dominant_support_singular_tail_scan_receipt(
        start=10000, targets_per_cycle=501,
        support_modes=(((11, 13), 6), ((7, 11), 5), ((5, 7), 3)),
        tolerance=1e-9):
    """Scan principal-relative tails after dominant support singular modes."""
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    support_modes = tuple((tuple(support), mode)
                          for support, mode in support_modes)
    valid_supports = {(11, 13), (7, 11), (5, 7)}
    if (not support_modes or any(
            support not in valid_supports or type(mode) is not int
            or mode < 1 for support, mode in support_modes)):
        raise ValueError("support_modes must use positive dominant modes")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    period_units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    values = np.asarray(tuple(
        coefficient["aggregate_coefficient_by_unit_residue"][unit]
        for unit in period_units), dtype=np.complex128)
    principal_mean = complex(np.mean(values))
    centered = values - principal_mean
    _, period_labels, period_character_table = _unit_character_table(
        period, period_units)
    period_character_coefficients = (
        np.conjugate(period_character_table) @ centered / len(period_units))
    factor_primes = (5, 7, 11, 13)
    support_indices = {}
    for index, label in enumerate(period_labels):
        support = tuple(
            prime for prime, exponent in zip(factor_primes, label)
            if exponent != 0)
        support_indices.setdefault(support, []).append(index)

    support_data = {}
    for support, mode_count in support_modes:
        masked = np.zeros_like(period_character_coefficients)
        masked[support_indices[support]] = period_character_coefficients[
            support_indices[support]]
        component = period_character_table.T @ masked
        modulus = 2
        for prime in support:
            modulus *= prime
        grouped = {}
        for unit, value in zip(period_units, component):
            grouped.setdefault(unit % modulus, []).append(value)
        lower_values = {
            residue: _complex_fsum(values) / len(values)
            for residue, values in grouped.items()}
        units = tuple(sorted(lower_values))
        coefficient_values = np.asarray(tuple(
            lower_values[unit] for unit in units), dtype=np.complex128)
        _, labels, character_table = _unit_character_table(modulus, units)
        character_coefficients = (
            np.conjugate(character_table) @ coefficient_values / len(units))
        matrix = np.zeros(tuple(prime - 1 for prime in support),
                          dtype=np.complex128)
        for label, value in zip(labels, character_coefficients):
            matrix[label] = value
        active_matrix = matrix[tuple(
            slice(1, prime - 1) for prime in support)]
        left, singular_values, right = np.linalg.svd(
            active_matrix, full_matrices=False)
        if mode_count > len(singular_values):
            raise ValueError("mode count exceeds support singular rank")
        truncated_matrix = (
            (left[:, :mode_count] * singular_values[:mode_count])
            @ right[:mode_count, :])
        tail_matrix = active_matrix - truncated_matrix
        support_data[support] = {
            "natural_modulus": modulus,
            "mode_count": mode_count,
            "units": units,
            "unit_index": {unit: index for index, unit in enumerate(units)},
            "coefficient_values": coefficient_values,
            "character_table": character_table,
            "active_matrix": active_matrix,
            "truncated_matrix": truncated_matrix,
            "tail_matrix": tail_matrix,
            "singular_values": tuple(float(value)
                                     for value in singular_values),
            "truncated_energy_fraction": float(
                np.sum(singular_values[:mode_count] ** 2)
                / np.sum(singular_values ** 2)
                if np.sum(singular_values ** 2) else 0.0),
        }

    targets = tuple(start + 2 * index for index in range(targets_per_cycle))
    primes = _prime_table(max(targets))
    rows = {}
    worst_tail_target = None
    worst_dominant_tail_target = None
    worst_modeled_dominant_target = None
    for target in targets:
        lower = target // 3
        upper = target - lower
        pairs = []
        total_weight = 0.0
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                weight = math.log(prime) * math.log(partner)
                pairs.append((prime, weight))
                total_weight += weight
        principal_contribution = principal_mean * total_weight
        support_rows = {}
        combined_actual = 0j
        combined_local_prediction = 0j
        combined_modeled_deviation = 0j
        combined_tail = 0j
        for support, data in support_data.items():
            modulus = data["natural_modulus"]
            units = data["units"]
            unit_index = data["unit_index"]
            coefficient_values = data["coefficient_values"]
            weights = np.zeros(len(units), dtype=np.float64)
            for prime, weight in pairs:
                weights[unit_index[prime % modulus]] += weight
            admissible_mask = np.asarray(tuple(
                math.gcd((target - unit) % modulus, modulus) == 1
                for unit in units), dtype=bool)
            admissible_count = int(np.sum(admissible_mask))
            mean_weight = total_weight / admissible_count
            weight_delta = np.zeros(len(units), dtype=np.float64)
            weight_delta[admissible_mask] = (
                weights[admissible_mask] - mean_weight)
            actual = complex(np.sum(coefficient_values * weights))
            local_prediction = complex(np.sum(
                coefficient_values[admissible_mask]) * mean_weight)
            imbalance_matrix = (
                data["character_table"] @ weight_delta).reshape(
                    tuple(prime - 1 for prime in support))[tuple(
                        slice(1, prime - 1) for prime in support)]
            modeled_deviation = complex(np.sum(
                data["truncated_matrix"] * imbalance_matrix))
            tail = complex(np.sum(data["tail_matrix"] * imbalance_matrix))
            deviation = actual - local_prediction
            combined_actual += actual
            combined_local_prediction += local_prediction
            combined_modeled_deviation += modeled_deviation
            combined_tail += tail
            support_rows[support] = {
                "actual_contribution": actual,
                "local_prediction": local_prediction,
                "deviation": deviation,
                "modeled_deviation": modeled_deviation,
                "tail": tail,
                "tail_to_principal_ratio": float(
                    tail.real / principal_contribution.real
                    if abs(principal_contribution.real) > tolerance
                    else math.nan),
                "absolute_tail_to_principal_ratio": float(
                    abs(tail.real) / principal_contribution.real
                    if abs(principal_contribution.real) > tolerance
                    else math.nan),
                "tail_reconstruction_error": float(
                    abs(deviation - modeled_deviation - tail)
                    / max(1.0, abs(deviation))),
            }
        combined_model = combined_local_prediction + combined_modeled_deviation
        combined_tail_reconstruction_error = abs(
            combined_actual - combined_model - combined_tail) / max(
                1.0, abs(combined_actual))
        rows[target] = {
            "strict_central_interval": (lower, upper),
            "ordered_central_prime_pair_count": len(pairs),
            "total_prime_pair_weight": total_weight,
            "principal_contribution": principal_contribution,
            "support_rows": support_rows,
            "combined_dominant_actual": combined_actual,
            "combined_dominant_local_prediction": (
                combined_local_prediction),
            "combined_dominant_modeled_deviation": (
                combined_modeled_deviation),
            "combined_dominant_model": combined_model,
            "combined_dominant_tail": combined_tail,
            "combined_dominant_actual_to_principal_ratio": float(
                combined_actual.real / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "combined_model_to_principal_ratio": float(
                combined_model.real / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "combined_tail_to_principal_ratio": float(
                combined_tail.real / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "combined_abs_tail_to_principal_ratio": float(
                abs(combined_tail.real) / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "combined_tail_reconstruction_error": (
                combined_tail_reconstruction_error),
        }
        if (worst_tail_target is None
                or rows[target]["combined_abs_tail_to_principal_ratio"]
                > rows[worst_tail_target][
                    "combined_abs_tail_to_principal_ratio"]):
            worst_tail_target = target
        if rows[target]["combined_dominant_actual_to_principal_ratio"] < -tolerance:
            if (worst_dominant_tail_target is None
                    or rows[target]["combined_abs_tail_to_principal_ratio"]
                    > rows[worst_dominant_tail_target][
                        "combined_abs_tail_to_principal_ratio"]):
                worst_dominant_tail_target = target
        if (worst_modeled_dominant_target is None
                or rows[target]["combined_model_to_principal_ratio"]
                < rows[worst_modeled_dominant_target][
                    "combined_model_to_principal_ratio"]):
            worst_modeled_dominant_target = target

    negative_dominant_targets = tuple(
        target for target, row in rows.items()
        if row["combined_dominant_actual_to_principal_ratio"] < -tolerance)
    maximum_tail_reconstruction_error = max(
        row["combined_tail_reconstruction_error"] for row in rows.values())
    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "start": start,
        "targets_per_cycle": targets_per_cycle,
        "support_modes": support_modes,
        "support_rows": {
            support: {
                "natural_modulus": data["natural_modulus"],
                "mode_count": data["mode_count"],
                "truncated_energy_fraction": (
                    data["truncated_energy_fraction"]),
                "singular_values": data["singular_values"],
            }
            for support, data in support_data.items()},
        "rows": rows,
        "negative_combined_dominant_count": len(negative_dominant_targets),
        "worst_combined_tail_target": worst_tail_target,
        "worst_combined_abs_tail_to_principal_ratio": (
            rows[worst_tail_target][
                "combined_abs_tail_to_principal_ratio"]),
        "worst_negative_combined_tail_target": worst_dominant_tail_target,
        "worst_modeled_dominant_target": worst_modeled_dominant_target,
        "minimum_combined_model_to_principal_ratio": (
            rows[worst_modeled_dominant_target][
                "combined_model_to_principal_ratio"]),
        "maximum_tail_reconstruction_error": (
            maximum_tail_reconstruction_error),
        "combined_tail_under_point_one_principal_on_sample": bool(
            rows[worst_tail_target][
                "combined_abs_tail_to_principal_ratio"] < .1),
        "combined_dominant_singular_tail_scan_measured": True,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_singular_mode_approximation_receipt(
        targets=(10424, 14138, 88346), modes=(1, 2, 4, 9),
        tolerance=1e-9):
    """Test whether q286 singular coefficient modes explain bad deviations."""
    targets = tuple(targets)
    modes = tuple(modes)
    if (not targets or any(type(target) is not int or target < 40
                           or target % 2 for target in targets)):
        raise ValueError("targets must be even integers at least 40")
    if not modes or any(type(mode) is not int or mode < 1 for mode in modes):
        raise ValueError("modes must be positive integers")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    character_receipt = q286_character_imbalance_receipt(
        targets=(10424,), top_count=120, tolerance=tolerance)
    matrix = np.zeros((10, 12), dtype=np.complex128)
    for row in character_receipt["top_coefficient_character_rows"]:
        first, second = row["label"]
        matrix[first, second] = row["coefficient"]
    coefficient_matrix = matrix[1:, 1:]
    left, singular_values, right = np.linalg.svd(
        coefficient_matrix, full_matrices=False)
    energies = singular_values ** 2
    total_energy = float(np.sum(energies))
    maximum_mode = len(singular_values)
    if any(mode > maximum_mode for mode in modes):
        raise ValueError("mode count exceeds q286 singular rank")

    modulus = 286
    units = tuple(unit for unit in range(modulus)
                  if math.gcd(unit, modulus) == 1)
    _, labels, character_table = _unit_character_table(modulus, units)
    unit_index = {unit: index for index, unit in enumerate(units)}
    primes = _prime_table(max(targets))

    rows = {}
    maximum_full_reconstruction_error = 0.0
    top_two_signed_residual_fraction_maximum = 0.0
    top_four_signed_residual_fraction_maximum = 0.0
    top_four_cauchy_residual_fraction_maximum = 0.0
    for target in targets:
        lower = target // 3
        upper = target - lower
        weights = np.zeros(len(units), dtype=np.float64)
        total_weight = 0.0
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                weight = math.log(prime) * math.log(partner)
                total_weight += weight
                weights[unit_index[prime % modulus]] += weight
        admissible_mask = np.asarray(tuple(
            math.gcd((target - unit) % modulus, modulus) == 1
            for unit in units), dtype=bool)
        admissible_count = int(np.sum(admissible_mask))
        mean_weight = total_weight / admissible_count
        weight_delta = np.zeros(len(units), dtype=np.float64)
        weight_delta[admissible_mask] = (
            weights[admissible_mask] - mean_weight)
        imbalance_matrix = (
            character_table @ weight_delta).reshape(10, 12)[1:, 1:]
        total_deviation = complex(np.sum(
            coefficient_matrix * imbalance_matrix))
        principal_contribution = (
            character_receipt["rows"][10424]["principal_contribution"]
            * (total_weight / character_receipt["rows"][10424][
                "total_prime_pair_weight"]))
        mode_rows = {}
        for mode in modes:
            truncated = (
                (left[:, :mode] * singular_values[:mode])
                @ right[:mode, :])
            approximation = complex(np.sum(
                truncated * imbalance_matrix))
            residual_matrix = coefficient_matrix - truncated
            residual = total_deviation - approximation
            residual_cauchy = (
                float(np.linalg.norm(residual_matrix))
                * float(np.linalg.norm(imbalance_matrix)))
            residual_fraction = (
                residual.real / total_deviation.real
                if abs(total_deviation.real) > tolerance else math.nan)
            mode_rows[mode] = {
                "coefficient_energy_fraction": float(
                    np.sum(energies[:mode]) / total_energy
                    if total_energy else 0.0),
                "approximation": approximation,
                "residual": residual,
                "approximation_to_deviation_ratio": float(
                    approximation.real / total_deviation.real
                    if abs(total_deviation.real) > tolerance else math.nan),
                "signed_residual_to_deviation_ratio": float(
                    residual_fraction),
                "absolute_residual_to_abs_deviation_ratio": float(
                    abs(residual.real) / abs(total_deviation.real)
                    if abs(total_deviation.real) > tolerance else math.nan),
                "residual_cauchy_to_abs_deviation_ratio": float(
                    residual_cauchy / abs(total_deviation.real)
                    if abs(total_deviation.real) > tolerance else math.nan),
                "approximation_to_principal_ratio": float(
                    approximation.real / principal_contribution.real
                    if abs(principal_contribution.real) > tolerance
                    else math.nan),
                "residual_to_principal_ratio": float(
                    residual.real / principal_contribution.real
                    if abs(principal_contribution.real) > tolerance
                    else math.nan),
            }
        full_mode = maximum_mode
        full_matrix = (
            (left[:, :full_mode] * singular_values[:full_mode])
            @ right[:full_mode, :])
        full_deviation = complex(np.sum(full_matrix * imbalance_matrix))
        full_error = abs(full_deviation - total_deviation) / max(
            1.0, abs(total_deviation))
        maximum_full_reconstruction_error = max(
            maximum_full_reconstruction_error, full_error)
        if 2 in mode_rows:
            top_two_signed_residual_fraction_maximum = max(
                top_two_signed_residual_fraction_maximum,
                mode_rows[2]["absolute_residual_to_abs_deviation_ratio"])
        if 4 in mode_rows:
            top_four_signed_residual_fraction_maximum = max(
                top_four_signed_residual_fraction_maximum,
                mode_rows[4]["absolute_residual_to_abs_deviation_ratio"])
            top_four_cauchy_residual_fraction_maximum = max(
                top_four_cauchy_residual_fraction_maximum,
                mode_rows[4]["residual_cauchy_to_abs_deviation_ratio"])
        rows[target] = {
            "strict_central_interval": (lower, upper),
            "total_prime_pair_weight": total_weight,
            "admissible_residue_count": admissible_count,
            "total_deviation": total_deviation,
            "principal_contribution": principal_contribution,
            "deviation_to_principal_ratio": float(
                total_deviation.real / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "mode_rows": mode_rows,
            "full_singular_reconstruction_error": full_error,
        }

    return {
        "families": character_receipt["families"],
        "arithmetic_period": character_receipt["arithmetic_period"],
        "support": character_receipt["support"],
        "natural_modulus": modulus,
        "matrix_shape": coefficient_matrix.shape,
        "singular_values": tuple(float(value) for value in singular_values),
        "tested_modes": modes,
        "targets": targets,
        "rows": rows,
        "maximum_full_singular_reconstruction_error": (
            maximum_full_reconstruction_error),
        "top_two_signed_residual_fraction_maximum": (
            top_two_signed_residual_fraction_maximum),
        "top_four_signed_residual_fraction_maximum": (
            top_four_signed_residual_fraction_maximum),
        "top_four_cauchy_residual_fraction_maximum": (
            top_four_cauchy_residual_fraction_maximum),
        "top_two_modes_explain_sampled_signed_deviation": bool(
            2 in modes and top_two_signed_residual_fraction_maximum < .11),
        "top_four_modes_leave_small_sampled_signed_residual": bool(
            4 in modes and top_four_signed_residual_fraction_maximum < .02),
        "top_four_tail_paid_by_cauchy": bool(
            4 in modes and top_four_cauchy_residual_fraction_maximum < .05),
        "singular_mode_approximation_measured": True,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_leading_singular_mode_contribution_receipt(
        targets=(10424, 14138, 14680, 88346), mode_count=6,
        tolerance=1e-9):
    """Attribute q286 deviations to individual leading singular modes."""
    targets = tuple(targets)
    if (not targets or any(type(target) is not int or target < 40
                           or target % 2 for target in targets)):
        raise ValueError("targets must be even integers at least 40")
    if type(mode_count) is not int or mode_count < 1 or mode_count > 9:
        raise ValueError("mode_count must lie between 1 and 9")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    character_receipt = q286_character_imbalance_receipt(
        targets=targets, top_count=120, tolerance=tolerance)
    matrix = np.zeros((10, 12), dtype=np.complex128)
    for row in character_receipt["top_coefficient_character_rows"]:
        first, second = row["label"]
        matrix[first, second] = row["coefficient"]
    coefficient_matrix = matrix[1:, 1:]
    left, singular_values, right = np.linalg.svd(
        coefficient_matrix, full_matrices=False)
    modulus = 286
    units = tuple(unit for unit in range(modulus)
                  if math.gcd(unit, modulus) == 1)
    _, _, character_table = _unit_character_table(modulus, units)
    unit_index = {unit: index for index, unit in enumerate(units)}
    primes = _prime_table(max(targets))

    rows = {}
    maximum_reconstruction_error = 0.0
    common_negative_mode_indices = None
    for target in targets:
        lower = target // 3
        upper = target - lower
        total_weight = 0.0
        weights = np.zeros(len(units), dtype=np.float64)
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                weight = math.log(prime) * math.log(partner)
                total_weight += weight
                weights[unit_index[prime % modulus]] += weight
        admissible_mask = np.asarray(tuple(
            math.gcd((target - unit) % modulus, modulus) == 1
            for unit in units), dtype=bool)
        mean_weight = total_weight / int(np.sum(admissible_mask))
        weight_delta = np.zeros(len(units), dtype=np.float64)
        weight_delta[admissible_mask] = (
            weights[admissible_mask] - mean_weight)
        imbalance_matrix = (
            character_table @ weight_delta).reshape(10, 12)[1:, 1:]
        mode_rows = []
        modeled_sum = 0j
        for index in range(mode_count):
            mode_matrix = (
                singular_values[index]
                * np.outer(left[:, index], right[index, :]))
            contribution = complex(np.sum(mode_matrix * imbalance_matrix))
            modeled_sum += contribution
            mode_rows.append({
                "mode_index": index + 1,
                "singular_value": float(singular_values[index]),
                "contribution": contribution,
                "contribution_to_principal_ratio": float(
                    contribution.real
                    / character_receipt["rows"][target][
                        "principal_contribution"].real),
                "contribution_to_deviation_ratio": float(
                    contribution.real
                    / character_receipt["rows"][target][
                        "residue_deviation"].real
                    if abs(character_receipt["rows"][target][
                        "residue_deviation"].real) > tolerance
                    else math.nan),
            })
        total_deviation = character_receipt["rows"][target][
            "residue_deviation"]
        residual = total_deviation - modeled_sum
        reconstruction = modeled_sum + residual
        reconstruction_error = abs(reconstruction - total_deviation) / max(
            1.0, abs(total_deviation))
        maximum_reconstruction_error = max(
            maximum_reconstruction_error, reconstruction_error)
        negative_modes = tuple(
            row["mode_index"] for row in mode_rows
            if row["contribution_to_principal_ratio"] < -tolerance)
        if common_negative_mode_indices is None:
            common_negative_mode_indices = set(negative_modes)
        else:
            common_negative_mode_indices &= set(negative_modes)
        rows[target] = {
            "strict_central_interval": (lower, upper),
            "total_prime_pair_weight": total_weight,
            "principal_contribution": character_receipt["rows"][target][
                "principal_contribution"],
            "q286_deviation": total_deviation,
            "q286_deviation_to_principal_ratio": character_receipt[
                "rows"][target]["deviation_to_principal_ratio"],
            "mode_count": mode_count,
            "mode_rows": tuple(mode_rows),
            "modeled_sum": modeled_sum,
            "modeled_sum_to_principal_ratio": float(
                modeled_sum.real
                / character_receipt["rows"][target][
                    "principal_contribution"].real),
            "residual": residual,
            "residual_to_principal_ratio": float(
                residual.real
                / character_receipt["rows"][target][
                    "principal_contribution"].real),
            "absolute_residual_to_principal_ratio": float(
                abs(residual.real)
                / character_receipt["rows"][target][
                    "principal_contribution"].real),
            "negative_mode_indices": negative_modes,
            "largest_negative_mode_index": min(
                mode_rows,
                key=lambda row: row["contribution_to_principal_ratio"])[
                    "mode_index"],
            "largest_negative_mode_to_principal_ratio": min(
                row["contribution_to_principal_ratio"]
                for row in mode_rows),
            "mode_reconstruction_error": reconstruction_error,
        }

    return {
        "families": character_receipt["families"],
        "arithmetic_period": character_receipt["arithmetic_period"],
        "support": character_receipt["support"],
        "natural_modulus": modulus,
        "targets": targets,
        "mode_count": mode_count,
        "singular_values": tuple(float(value)
                                 for value in singular_values[:mode_count]),
        "rows": rows,
        "common_negative_mode_indices": tuple(sorted(
            common_negative_mode_indices or ())),
        "maximum_mode_reconstruction_error": maximum_reconstruction_error,
        "all_targets_have_multiple_negative_modes": bool(all(
            len(row["negative_mode_indices"]) > 1 for row in rows.values())),
        "single_mode_obstruction_found": bool(
            len(common_negative_mode_indices or ()) == 1),
        "leading_singular_mode_contribution_measured": True,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_leading_mode_cycle_profile_receipt(
        start=10000, targets_per_cycle=5005, mode_count=6,
        significant_negative_ratio=-.4, tolerance=1e-9):
    """Profile individual q286 singular modes across consecutive targets."""
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    if type(mode_count) is not int or mode_count < 1 or mode_count > 9:
        raise ValueError("mode_count must lie between 1 and 9")
    if (not math.isfinite(significant_negative_ratio)
            or significant_negative_ratio >= 0):
        raise ValueError(
            "significant_negative_ratio must be finite and negative")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    character_receipt = q286_character_imbalance_receipt(
        targets=(start,), top_count=120, tolerance=tolerance)
    matrix = np.zeros((10, 12), dtype=np.complex128)
    for row in character_receipt["top_coefficient_character_rows"]:
        first, second = row["label"]
        matrix[first, second] = row["coefficient"]
    coefficient_matrix = matrix[1:, 1:]
    left, singular_values, right = np.linalg.svd(
        coefficient_matrix, full_matrices=False)
    modulus = 286
    units = tuple(unit for unit in range(modulus)
                  if math.gcd(unit, modulus) == 1)
    _, _, character_table = _unit_character_table(modulus, units)
    unit_index = {unit: index for index, unit in enumerate(units)}
    targets = tuple(start + 2 * index for index in range(targets_per_cycle))
    primes = _prime_table(max(targets))

    mode_stats = {
        mode: {
            "minimum_contribution_to_principal_ratio": math.inf,
            "minimum_target": None,
            "maximum_contribution_to_principal_ratio": -math.inf,
            "maximum_target": None,
            "negative_count": 0,
            "positive_count": 0,
            "near_zero_count": 0,
            "negative_on_significant_count": 0,
            "positive_on_significant_count": 0,
            "sum_contribution_to_principal_ratio": 0.0,
        }
        for mode in range(1, mode_count + 1)}
    negative_targets = []
    significant_negative_targets = []
    minimum_q286_target = None
    minimum_q286_ratio = math.inf
    maximum_q286_target = None
    maximum_q286_ratio = -math.inf
    per_target_common_negative_modes = None
    significant_common_negative_modes = None

    for target in targets:
        lower = target // 3
        upper = target - lower
        total_weight = 0.0
        weights = np.zeros(len(units), dtype=np.float64)
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                weight = math.log(prime) * math.log(partner)
                total_weight += weight
                weights[unit_index[prime % modulus]] += weight
        if total_weight <= tolerance:
            continue
        principal_contribution = (
            character_receipt["rows"][start]["principal_contribution"]
            * (total_weight / character_receipt["rows"][start][
                "total_prime_pair_weight"]))
        admissible_mask = np.asarray(tuple(
            math.gcd((target - unit) % modulus, modulus) == 1
            for unit in units), dtype=bool)
        mean_weight = total_weight / int(np.sum(admissible_mask))
        weight_delta = np.zeros(len(units), dtype=np.float64)
        weight_delta[admissible_mask] = (
            weights[admissible_mask] - mean_weight)
        imbalance_matrix = (
            character_table @ weight_delta).reshape(10, 12)[1:, 1:]
        q286_deviation = complex(np.sum(
            coefficient_matrix * imbalance_matrix))
        q286_ratio = float(q286_deviation.real
                           / principal_contribution.real)
        if q286_ratio < minimum_q286_ratio:
            minimum_q286_ratio = q286_ratio
            minimum_q286_target = target
        if q286_ratio > maximum_q286_ratio:
            maximum_q286_ratio = q286_ratio
            maximum_q286_target = target
        is_negative = q286_ratio < -tolerance
        is_significant = q286_ratio <= significant_negative_ratio
        if is_negative:
            negative_targets.append(target)
        if is_significant:
            significant_negative_targets.append(target)
        target_negative_modes = set()
        for index in range(mode_count):
            mode = index + 1
            mode_matrix = (
                singular_values[index]
                * np.outer(left[:, index], right[index, :]))
            contribution = complex(np.sum(mode_matrix * imbalance_matrix))
            ratio = float(contribution.real / principal_contribution.real)
            stats = mode_stats[mode]
            stats["sum_contribution_to_principal_ratio"] += ratio
            if ratio < stats["minimum_contribution_to_principal_ratio"]:
                stats["minimum_contribution_to_principal_ratio"] = ratio
                stats["minimum_target"] = target
            if ratio > stats["maximum_contribution_to_principal_ratio"]:
                stats["maximum_contribution_to_principal_ratio"] = ratio
                stats["maximum_target"] = target
            if ratio < -tolerance:
                stats["negative_count"] += 1
                target_negative_modes.add(mode)
                if is_significant:
                    stats["negative_on_significant_count"] += 1
            elif ratio > tolerance:
                stats["positive_count"] += 1
                if is_significant:
                    stats["positive_on_significant_count"] += 1
            else:
                stats["near_zero_count"] += 1
        if per_target_common_negative_modes is None:
            per_target_common_negative_modes = set(target_negative_modes)
        else:
            per_target_common_negative_modes &= target_negative_modes
        if is_significant:
            if significant_common_negative_modes is None:
                significant_common_negative_modes = set(target_negative_modes)
            else:
                significant_common_negative_modes &= target_negative_modes

    tested_count = len(targets)
    for stats in mode_stats.values():
        stats["mean_contribution_to_principal_ratio"] = (
            stats["sum_contribution_to_principal_ratio"] / tested_count
            if tested_count else math.nan)
        stats["negative_fraction"] = (
            stats["negative_count"] / tested_count if tested_count else 0.0)
        stats["positive_fraction"] = (
            stats["positive_count"] / tested_count if tested_count else 0.0)
        stats["negative_on_significant_fraction"] = (
            stats["negative_on_significant_count"]
            / len(significant_negative_targets)
            if significant_negative_targets else 0.0)
        del stats["sum_contribution_to_principal_ratio"]

    return {
        "families": character_receipt["families"],
        "arithmetic_period": character_receipt["arithmetic_period"],
        "support": character_receipt["support"],
        "natural_modulus": modulus,
        "start": start,
        "targets_per_cycle": targets_per_cycle,
        "tested_target_count": tested_count,
        "mode_count": mode_count,
        "significant_negative_ratio": significant_negative_ratio,
        "negative_q286_deviation_count": len(negative_targets),
        "significant_negative_q286_deviation_targets": tuple(
            significant_negative_targets),
        "significant_negative_q286_deviation_count": len(
            significant_negative_targets),
        "minimum_q286_deviation_target": minimum_q286_target,
        "minimum_q286_deviation_ratio": minimum_q286_ratio,
        "maximum_q286_deviation_target": maximum_q286_target,
        "maximum_q286_deviation_ratio": maximum_q286_ratio,
        "mode_stats": mode_stats,
        "common_negative_mode_indices_all_targets": tuple(sorted(
            per_target_common_negative_modes or ())),
        "common_negative_mode_indices_significant_targets": tuple(sorted(
            significant_common_negative_modes or ())),
        "all_first_three_modes_negative_on_significant_targets": bool(
            {1, 2, 3}.issubset(significant_common_negative_modes or set())),
        "single_mode_negative_on_all_significant_targets": bool(
            len(significant_common_negative_modes or ()) == 1),
        "leading_mode_cycle_profile_measured": True,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_separable_mode_coefficient_receipt(
        mode_count=6, top_count=6, tolerance=1e-9):
    """Expose leading q286 singular modes as separable residue weights."""
    if type(mode_count) is not int or mode_count < 1 or mode_count > 9:
        raise ValueError("mode_count must lie between 1 and 9")
    if type(top_count) is not int or top_count < 1:
        raise ValueError("top_count must be a positive integer")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    character_receipt = q286_character_imbalance_receipt(
        targets=(10424,), top_count=120, tolerance=tolerance)
    matrix = np.zeros((10, 12), dtype=np.complex128)
    for row in character_receipt["top_coefficient_character_rows"]:
        first, second = row["label"]
        matrix[first, second] = row["coefficient"]
    coefficient_matrix = matrix[1:, 1:]
    left, singular_values, right = np.linalg.svd(
        coefficient_matrix, full_matrices=False)
    unit11 = tuple(residue for residue in range(11)
                   if math.gcd(residue, 11) == 1)
    unit13 = tuple(residue for residue in range(13)
                   if math.gcd(residue, 13) == 1)
    _, _, table11 = _unit_character_table(11, unit11)
    _, _, table13 = _unit_character_table(13, unit13)
    mode_rows = []
    maximum_factorization_error = 0.0
    for index in range(mode_count):
        left_coefficients = np.zeros(10, dtype=np.complex128)
        right_coefficients = np.zeros(12, dtype=np.complex128)
        left_coefficients[1:] = left[:, index]
        right_coefficients[1:] = right[index, :]
        left_residue_values = table11.T @ left_coefficients
        right_residue_values = table13.T @ right_coefficients
        separated_values = (
            singular_values[index]
            * left_residue_values[:, None]
            * right_residue_values[None, :])
        mode_matrix = (
            singular_values[index]
            * np.outer(left[:, index], right[index, :]))
        full_mode_matrix = np.zeros((10, 12), dtype=np.complex128)
        full_mode_matrix[1:, 1:] = mode_matrix
        reconstructed_values = (
            table11.T @ full_mode_matrix @ table13)
        factorization_error = float(
            np.linalg.norm(reconstructed_values - separated_values)
            / max(1.0, np.linalg.norm(separated_values)))
        maximum_factorization_error = max(
            maximum_factorization_error, factorization_error)
        residue_rows = []
        for left_position, left_residue in enumerate(unit11):
            for right_position, right_residue in enumerate(unit13):
                value = separated_values[left_position, right_position]
                residue_rows.append({
                    "residue_mod_11": left_residue,
                    "residue_mod_13": right_residue,
                    "coefficient": complex(value),
                    "coefficient_real": float(value.real),
                    "coefficient_abs": float(abs(value)),
                })
        top_abs = tuple(sorted(
            residue_rows,
            key=lambda row: row["coefficient_abs"],
            reverse=True)[:top_count])
        mode_rows.append({
            "mode_index": index + 1,
            "singular_value": float(singular_values[index]),
            "character_l2_energy": float(singular_values[index] ** 2),
            "left_residue_l2": float(np.linalg.norm(left_residue_values)),
            "right_residue_l2": float(np.linalg.norm(right_residue_values)),
            "left_residue_l1": float(np.sum(np.abs(left_residue_values))),
            "right_residue_l1": float(np.sum(np.abs(right_residue_values))),
            "separated_residue_l2": float(np.linalg.norm(separated_values)),
            "maximum_residue_abs": float(np.max(np.abs(separated_values))),
            "maximum_residue_real": float(np.max(separated_values.real)),
            "minimum_residue_real": float(np.min(separated_values.real)),
            "positive_real_residue_count": sum(
                1 for row in residue_rows
                if row["coefficient_real"] > tolerance),
            "negative_real_residue_count": sum(
                1 for row in residue_rows
                if row["coefficient_real"] < -tolerance),
            "near_zero_real_residue_count": sum(
                1 for row in residue_rows
                if abs(row["coefficient_real"]) <= tolerance),
            "top_abs_residue_rows": top_abs,
            "factorization_reconstruction_error": factorization_error,
        })
    return {
        "families": character_receipt["families"],
        "arithmetic_period": character_receipt["arithmetic_period"],
        "support": character_receipt["support"],
        "natural_modulus": character_receipt["natural_modulus"],
        "mode_count": mode_count,
        "top_count": top_count,
        "mode_rows": tuple(mode_rows),
        "maximum_factorization_reconstruction_error": (
            maximum_factorization_error),
        "all_modes_have_mixed_residue_signs": bool(all(
            row["positive_real_residue_count"] > 0
            and row["negative_real_residue_count"] > 0
            for row in mode_rows)),
        "separable_mode_coefficients_measured": True,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_leading_mode_character_shape_receipt(
        mode_count=3, top_count=5, tolerance=1e-9):
    """Measure whether leading q286 modes are sparse in character space."""
    if type(mode_count) is not int or mode_count < 1 or mode_count > 9:
        raise ValueError("mode_count must lie between 1 and 9")
    if type(top_count) is not int or top_count < 1:
        raise ValueError("top_count must be a positive integer")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    character_receipt = q286_character_imbalance_receipt(
        targets=(10424,), top_count=120, tolerance=tolerance)
    matrix = np.zeros((10, 12), dtype=np.complex128)
    for row in character_receipt["top_coefficient_character_rows"]:
        first, second = row["label"]
        matrix[first, second] = row["coefficient"]
    coefficient_matrix = matrix[1:, 1:]
    left, singular_values, right = np.linalg.svd(
        coefficient_matrix, full_matrices=False)

    mode_rows = []
    for index in range(mode_count):
        left_vector = left[:, index]
        right_vector = right[index, :]
        left_energy = np.abs(left_vector) ** 2
        right_energy = np.abs(right_vector) ** 2
        left_effective_count = float(1.0 / np.sum(left_energy ** 2))
        right_effective_count = float(1.0 / np.sum(right_energy ** 2))
        left_top = tuple({
            "character_exponent_mod_11": int(position + 1),
            "coefficient": complex(left_vector[position]),
            "energy_fraction": float(left_energy[position]),
        } for position in np.argsort(-left_energy)[:top_count])
        right_top = tuple({
            "character_exponent_mod_13": int(position + 1),
            "coefficient": complex(right_vector[position]),
            "energy_fraction": float(right_energy[position]),
        } for position in np.argsort(-right_energy)[:top_count])
        mode_rows.append({
            "mode_index": index + 1,
            "singular_value": float(singular_values[index]),
            "left_effective_character_count": left_effective_count,
            "right_effective_character_count": right_effective_count,
            "left_max_character_energy_fraction": float(np.max(left_energy)),
            "right_max_character_energy_fraction": float(np.max(right_energy)),
            "left_top_character_rows": left_top,
            "right_top_character_rows": right_top,
            "left_single_character_dominates": bool(
                np.max(left_energy) > 0.5),
            "right_single_character_dominates": bool(
                np.max(right_energy) > 0.5),
        })

    return {
        "arithmetic_period": 10010,
        "support": (11, 13),
        "natural_modulus": 286,
        "mode_count": mode_count,
        "top_count": top_count,
        "mode_rows": tuple(mode_rows),
        "minimum_left_effective_character_count": min(
            row["left_effective_character_count"] for row in mode_rows),
        "minimum_right_effective_character_count": min(
            row["right_effective_character_count"] for row in mode_rows),
        "maximum_side_character_energy_fraction": max(
            max(row["left_max_character_energy_fraction"],
                row["right_max_character_energy_fraction"])
            for row in mode_rows),
        "no_single_character_mode_found": not any(
            row["left_single_character_dominates"]
            or row["right_single_character_dominates"]
            for row in mode_rows),
        "leading_mode_character_shape_measured": True,
        "single_character_estimate_suffices": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_separable_mode_local_bias_receipt(
        start=10000, targets_per_cycle=5005, mode_count=6,
        significant_negative_ratio=-.4, tolerance=1e-9):
    """Split each leading q286 mode into local bias and prime deviation."""
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    if type(mode_count) is not int or mode_count < 1 or mode_count > 9:
        raise ValueError("mode_count must lie between 1 and 9")
    if (not math.isfinite(significant_negative_ratio)
            or significant_negative_ratio >= 0):
        raise ValueError(
            "significant_negative_ratio must be finite and negative")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    character_receipt = q286_character_imbalance_receipt(
        targets=(start,), top_count=120, tolerance=tolerance)
    matrix = np.zeros((10, 12), dtype=np.complex128)
    for row in character_receipt["top_coefficient_character_rows"]:
        first, second = row["label"]
        matrix[first, second] = row["coefficient"]
    coefficient_matrix = matrix[1:, 1:]
    left, singular_values, right = np.linalg.svd(
        coefficient_matrix, full_matrices=False)
    modulus = 286
    units = tuple(unit for unit in range(modulus)
                  if math.gcd(unit, modulus) == 1)
    _, _, character_table = _unit_character_table(modulus, units)
    unit_index = {unit: index for index, unit in enumerate(units)}
    targets = tuple(start + 2 * index for index in range(targets_per_cycle))
    primes = _prime_table(max(targets))

    mode_value_rows = []
    for index in range(mode_count):
        mode_matrix = (
            singular_values[index]
            * np.outer(left[:, index], right[index, :]))
        full_mode_matrix = np.zeros((10, 12), dtype=np.complex128)
        full_mode_matrix[1:, 1:] = mode_matrix
        mode_values = character_table.T @ full_mode_matrix.reshape(-1)
        mode_value_rows.append(mode_values)

    mode_stats = {
        mode: {
            "minimum_local_to_principal_ratio": math.inf,
            "minimum_local_target": None,
            "maximum_local_to_principal_ratio": -math.inf,
            "maximum_local_target": None,
            "minimum_deviation_to_principal_ratio": math.inf,
            "minimum_deviation_target": None,
            "maximum_deviation_to_principal_ratio": -math.inf,
            "maximum_deviation_target": None,
            "minimum_actual_to_principal_ratio": math.inf,
            "minimum_actual_target": None,
            "maximum_actual_to_principal_ratio": -math.inf,
            "maximum_actual_target": None,
            "local_negative_count": 0,
            "deviation_negative_count": 0,
            "actual_negative_count": 0,
            "local_negative_on_significant_count": 0,
            "deviation_negative_on_significant_count": 0,
            "actual_negative_on_significant_count": 0,
            "sum_local_to_principal_ratio": 0.0,
            "sum_deviation_to_principal_ratio": 0.0,
            "sum_actual_to_principal_ratio": 0.0,
        }
        for mode in range(1, mode_count + 1)}
    significant_targets = []
    maximum_mode_reconstruction_error = 0.0

    for target in targets:
        lower = target // 3
        upper = target - lower
        total_weight = 0.0
        weights = np.zeros(len(units), dtype=np.float64)
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                weight = math.log(prime) * math.log(partner)
                total_weight += weight
                weights[unit_index[prime % modulus]] += weight
        if total_weight <= tolerance:
            continue
        principal_contribution = (
            character_receipt["rows"][start]["principal_contribution"]
            * (total_weight / character_receipt["rows"][start][
                "total_prime_pair_weight"]))
        admissible_mask = np.asarray(tuple(
            math.gcd((target - unit) % modulus, modulus) == 1
            for unit in units), dtype=bool)
        mean_weight = total_weight / int(np.sum(admissible_mask))
        q286_deviation = complex(np.sum(
            coefficient_matrix
            * (character_table @ (
                weights - mean_weight * admissible_mask)).reshape(10, 12)[
                    1:, 1:]))
        q286_ratio = float(q286_deviation.real
                           / principal_contribution.real)
        is_significant = q286_ratio <= significant_negative_ratio
        if is_significant:
            significant_targets.append(target)

        modeled_deviation = 0j
        for index, mode_values in enumerate(mode_value_rows):
            mode = index + 1
            local_prediction = complex(
                np.sum(mode_values[admissible_mask]) * mean_weight)
            actual = complex(np.sum(mode_values * weights))
            deviation = actual - local_prediction
            modeled_deviation += deviation
            local_ratio = float(
                local_prediction.real / principal_contribution.real)
            deviation_ratio = float(
                deviation.real / principal_contribution.real)
            actual_ratio = float(
                actual.real / principal_contribution.real)
            stats = mode_stats[mode]
            stats["sum_local_to_principal_ratio"] += local_ratio
            stats["sum_deviation_to_principal_ratio"] += deviation_ratio
            stats["sum_actual_to_principal_ratio"] += actual_ratio
            if local_ratio < stats["minimum_local_to_principal_ratio"]:
                stats["minimum_local_to_principal_ratio"] = local_ratio
                stats["minimum_local_target"] = target
            if local_ratio > stats["maximum_local_to_principal_ratio"]:
                stats["maximum_local_to_principal_ratio"] = local_ratio
                stats["maximum_local_target"] = target
            if deviation_ratio < stats["minimum_deviation_to_principal_ratio"]:
                stats["minimum_deviation_to_principal_ratio"] = (
                    deviation_ratio)
                stats["minimum_deviation_target"] = target
            if deviation_ratio > stats["maximum_deviation_to_principal_ratio"]:
                stats["maximum_deviation_to_principal_ratio"] = (
                    deviation_ratio)
                stats["maximum_deviation_target"] = target
            if actual_ratio < stats["minimum_actual_to_principal_ratio"]:
                stats["minimum_actual_to_principal_ratio"] = actual_ratio
                stats["minimum_actual_target"] = target
            if actual_ratio > stats["maximum_actual_to_principal_ratio"]:
                stats["maximum_actual_to_principal_ratio"] = actual_ratio
                stats["maximum_actual_target"] = target
            if local_ratio < -tolerance:
                stats["local_negative_count"] += 1
                if is_significant:
                    stats["local_negative_on_significant_count"] += 1
            if deviation_ratio < -tolerance:
                stats["deviation_negative_count"] += 1
                if is_significant:
                    stats["deviation_negative_on_significant_count"] += 1
            if actual_ratio < -tolerance:
                stats["actual_negative_count"] += 1
                if is_significant:
                    stats["actual_negative_on_significant_count"] += 1
        maximum_mode_reconstruction_error = max(
            maximum_mode_reconstruction_error,
            abs(modeled_deviation - q286_deviation) / max(
                1.0, abs(q286_deviation)))

    tested_count = len(targets)
    significant_count = len(significant_targets)
    for stats in mode_stats.values():
        stats["mean_local_to_principal_ratio"] = (
            stats["sum_local_to_principal_ratio"] / tested_count)
        stats["mean_deviation_to_principal_ratio"] = (
            stats["sum_deviation_to_principal_ratio"] / tested_count)
        stats["mean_actual_to_principal_ratio"] = (
            stats["sum_actual_to_principal_ratio"] / tested_count)
        stats["local_negative_fraction"] = (
            stats["local_negative_count"] / tested_count)
        stats["deviation_negative_fraction"] = (
            stats["deviation_negative_count"] / tested_count)
        stats["actual_negative_fraction"] = (
            stats["actual_negative_count"] / tested_count)
        stats["local_negative_on_significant_fraction"] = (
            stats["local_negative_on_significant_count"] / significant_count
            if significant_count else 0.0)
        stats["deviation_negative_on_significant_fraction"] = (
            stats["deviation_negative_on_significant_count"]
            / significant_count if significant_count else 0.0)
        stats["actual_negative_on_significant_fraction"] = (
            stats["actual_negative_on_significant_count"] / significant_count
            if significant_count else 0.0)
        del stats["sum_local_to_principal_ratio"]
        del stats["sum_deviation_to_principal_ratio"]
        del stats["sum_actual_to_principal_ratio"]

    maximum_abs_mean_local = max(
        abs(stats["mean_local_to_principal_ratio"])
        for stats in mode_stats.values())
    maximum_abs_local = max(
        max(abs(stats["minimum_local_to_principal_ratio"]),
            abs(stats["maximum_local_to_principal_ratio"]))
        for stats in mode_stats.values())
    maximum_abs_deviation = max(
        max(abs(stats["minimum_deviation_to_principal_ratio"]),
            abs(stats["maximum_deviation_to_principal_ratio"]))
        for stats in mode_stats.values())

    return {
        "families": character_receipt["families"],
        "arithmetic_period": character_receipt["arithmetic_period"],
        "support": character_receipt["support"],
        "natural_modulus": modulus,
        "start": start,
        "targets_per_cycle": targets_per_cycle,
        "tested_target_count": tested_count,
        "mode_count": mode_count,
        "significant_negative_ratio": significant_negative_ratio,
        "significant_negative_q286_deviation_count": significant_count,
        "mode_stats": mode_stats,
        "maximum_mode_approximation_residual_fraction": (
            maximum_mode_reconstruction_error),
        "maximum_abs_mean_local_to_principal_ratio": (
            maximum_abs_mean_local),
        "maximum_abs_local_to_principal_ratio": maximum_abs_local,
        "maximum_abs_deviation_to_principal_ratio": maximum_abs_deviation,
        "local_bias_means_near_zero_on_sample": bool(
            maximum_abs_mean_local < 1e-12),
        "prime_deviation_range_exceeds_local_bias_range": bool(
            maximum_abs_deviation > maximum_abs_local),
        "all_modes_have_nonzero_local_bias": bool(all(
            abs(stats["mean_local_to_principal_ratio"]) > tolerance
            for stats in mode_stats.values())),
        "all_modes_have_prime_deviation_variation": bool(all(
            stats["minimum_deviation_to_principal_ratio"] < -tolerance
            and stats["maximum_deviation_to_principal_ratio"] > tolerance
            for stats in mode_stats.values())),
        "separable_mode_local_bias_measured": True,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_leading_mode_lift_decay_receipt(
        base_targets=(10424, 12118, 14138, 14680),
        lifts=(0, 1, 4, 9, 19, 49), mode_count=6, tolerance=1e-9):
    """Measure leading q286 mode decay across period lifts."""
    base_targets = tuple(base_targets)
    lifts = tuple(lifts)
    if (not base_targets or any(
            type(target) is not int or target < 40 or target % 2
            for target in base_targets)):
        raise ValueError("base_targets must be even integers at least 40")
    if not lifts or any(type(lift) is not int or lift < 0 for lift in lifts):
        raise ValueError("lifts must be nonnegative integers")
    if type(mode_count) is not int or mode_count < 1 or mode_count > 9:
        raise ValueError("mode_count must lie between 1 and 9")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    period = 10010
    targets = tuple(dict.fromkeys(
        base + period * lift
        for base in base_targets
        for lift in lifts))
    contribution = q286_leading_singular_mode_contribution_receipt(
        targets=targets, mode_count=mode_count, tolerance=tolerance)

    rows = {}
    all_base_targets_improve_after_zero_lift = True
    maximum_lifted_first_three_abs_ratio = 0.0
    maximum_lifted_six_mode_abs_ratio = 0.0
    maximum_lifted_residual_abs_ratio = 0.0
    for base in base_targets:
        lift_rows = {}
        zero_first_three_abs = None
        zero_six_abs = None
        best_lift = None
        best_first_three_abs = math.inf
        for lift in lifts:
            target = base + period * lift
            row = contribution["rows"][target]
            mode_ratios = tuple(
                mode_row["contribution_to_principal_ratio"]
                for mode_row in row["mode_rows"])
            first_two = math.fsum(mode_ratios[:min(2, len(mode_ratios))])
            first_three = math.fsum(mode_ratios[:min(3, len(mode_ratios))])
            six_sum = math.fsum(mode_ratios)
            first_three_abs = abs(first_three)
            six_abs = abs(six_sum)
            residual_abs = abs(row["residual_to_principal_ratio"])
            if lift == 0:
                zero_first_three_abs = first_three_abs
                zero_six_abs = six_abs
            else:
                maximum_lifted_first_three_abs_ratio = max(
                    maximum_lifted_first_three_abs_ratio, first_three_abs)
                maximum_lifted_six_mode_abs_ratio = max(
                    maximum_lifted_six_mode_abs_ratio, six_abs)
                maximum_lifted_residual_abs_ratio = max(
                    maximum_lifted_residual_abs_ratio, residual_abs)
            if first_three_abs < best_first_three_abs:
                best_first_three_abs = first_three_abs
                best_lift = lift
            lift_rows[lift] = {
                "target": target,
                "q286_deviation_to_principal_ratio": (
                    row["q286_deviation_to_principal_ratio"]),
                "first_two_mode_to_principal_ratio": first_two,
                "first_three_mode_to_principal_ratio": first_three,
                "six_mode_to_principal_ratio": six_sum,
                "six_mode_residual_to_principal_ratio": (
                    row["residual_to_principal_ratio"]),
                "six_mode_abs_residual_to_principal_ratio": residual_abs,
                "mode_to_principal_ratios": mode_ratios,
            }
        lifted_first_three_values = tuple(
            abs(lift_rows[lift]["first_three_mode_to_principal_ratio"])
            for lift in lifts if lift != 0)
        lifted_six_values = tuple(
            abs(lift_rows[lift]["six_mode_to_principal_ratio"])
            for lift in lifts if lift != 0)
        first_three_improves = bool(
            zero_first_three_abs is not None and lifted_first_three_values
            and min(lifted_first_three_values) < zero_first_three_abs)
        six_mode_improves = bool(
            zero_six_abs is not None and lifted_six_values
            and min(lifted_six_values) < zero_six_abs)
        all_base_targets_improve_after_zero_lift = bool(
            all_base_targets_improve_after_zero_lift
            and first_three_improves)
        rows[base] = {
            "lift_rows": lift_rows,
            "zero_first_three_abs_ratio": zero_first_three_abs,
            "minimum_lifted_first_three_abs_ratio": (
                min(lifted_first_three_values)
                if lifted_first_three_values else math.nan),
            "zero_six_mode_abs_ratio": zero_six_abs,
            "minimum_lifted_six_mode_abs_ratio": (
                min(lifted_six_values) if lifted_six_values else math.nan),
            "best_first_three_lift": best_lift,
            "first_three_improves_after_zero_lift": first_three_improves,
            "six_mode_improves_after_zero_lift": six_mode_improves,
        }

    return {
        "families": contribution["families"],
        "arithmetic_period": contribution["arithmetic_period"],
        "support": contribution["support"],
        "natural_modulus": contribution["natural_modulus"],
        "base_targets": base_targets,
        "lifts": lifts,
        "mode_count": mode_count,
        "rows": rows,
        "maximum_mode_reconstruction_error": (
            contribution["maximum_mode_reconstruction_error"]),
        "all_base_targets_first_three_improve_after_zero_lift": bool(
            all_base_targets_improve_after_zero_lift),
        "maximum_lifted_first_three_abs_ratio": (
            maximum_lifted_first_three_abs_ratio),
        "maximum_lifted_six_mode_abs_ratio": (
            maximum_lifted_six_mode_abs_ratio),
        "maximum_lifted_residual_abs_ratio": (
            maximum_lifted_residual_abs_ratio),
        "lifted_first_three_under_half_principal": bool(
            maximum_lifted_first_three_abs_ratio < .5),
        "lifted_six_modes_under_half_principal": bool(
            maximum_lifted_six_mode_abs_ratio < .5),
        "leading_mode_lift_decay_measured": True,
        "eventual_decay_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_significant_lift_envelope_receipt(
        start=10000, targets_per_cycle=5005, lifts=(0, 1, 4, 9, 19, 49),
        mode_count=6, significant_negative_ratio=-.4,
        max_base_targets=None, tolerance=1e-9):
    """Stress period-lift behavior for significant q286 lower-tail bases."""
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    if not lifts or any(type(lift) is not int or lift < 0 for lift in lifts):
        raise ValueError("lifts must be nonnegative integers")
    if type(mode_count) is not int or mode_count < 1 or mode_count > 9:
        raise ValueError("mode_count must lie between 1 and 9")
    if (not math.isfinite(significant_negative_ratio)
            or significant_negative_ratio >= 0):
        raise ValueError(
            "significant_negative_ratio must be finite and negative")
    if (max_base_targets is not None
            and (type(max_base_targets) is not int or max_base_targets < 1)):
        raise ValueError("max_base_targets must be None or positive")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    profile = q286_leading_mode_cycle_profile_receipt(
        start=start, targets_per_cycle=targets_per_cycle,
        mode_count=mode_count,
        significant_negative_ratio=significant_negative_ratio,
        tolerance=tolerance)
    base_targets = profile["significant_negative_q286_deviation_targets"]
    selected_base_targets = (
        base_targets[:max_base_targets]
        if max_base_targets is not None else base_targets)
    if not selected_base_targets:
        return {
            "families": profile["families"],
            "arithmetic_period": profile["arithmetic_period"],
            "support": profile["support"],
            "natural_modulus": profile["natural_modulus"],
            "start": start,
            "targets_per_cycle": targets_per_cycle,
            "lifts": tuple(lifts),
            "mode_count": mode_count,
            "significant_negative_ratio": significant_negative_ratio,
            "available_base_target_count": 0,
            "selected_base_target_count": 0,
            "rows": {},
            "significant_lift_envelope_measured": True,
            "eventual_decay_proved": False,
            "signed_prime_correlation_estimate_proved": False,
            "formal_signed_error_identification_proved": False,
            "goldbach_proved": False,
        }
    lift_receipt = q286_leading_mode_lift_decay_receipt(
        base_targets=selected_base_targets, lifts=tuple(lifts),
        mode_count=mode_count, tolerance=tolerance)

    worst_lifted_first_three_base = max(
        selected_base_targets,
        key=lambda base: max(
            abs(row["first_three_mode_to_principal_ratio"])
            for lift, row in lift_receipt["rows"][base][
                "lift_rows"].items() if lift != 0))
    worst_lifted_six_base = max(
        selected_base_targets,
        key=lambda base: max(
            abs(row["six_mode_to_principal_ratio"])
            for lift, row in lift_receipt["rows"][base][
                "lift_rows"].items() if lift != 0))
    worst_lifted_q286_base = max(
        selected_base_targets,
        key=lambda base: max(
            abs(row["q286_deviation_to_principal_ratio"])
            for lift, row in lift_receipt["rows"][base][
                "lift_rows"].items() if lift != 0))
    worst_lifted_residual_base = max(
        selected_base_targets,
        key=lambda base: max(
            abs(row["six_mode_residual_to_principal_ratio"])
            for lift, row in lift_receipt["rows"][base][
                "lift_rows"].items() if lift != 0))
    maximum_lifted_q286_abs_ratio = max(
        abs(row["q286_deviation_to_principal_ratio"])
        for base in selected_base_targets
        for lift, row in lift_receipt["rows"][base]["lift_rows"].items()
        if lift != 0)
    zero_first_three_ratios = tuple(
        lift_receipt["rows"][base]["zero_first_three_abs_ratio"]
        for base in selected_base_targets)
    minimum_lifted_first_three_ratios = tuple(
        lift_receipt["rows"][base]["minimum_lifted_first_three_abs_ratio"]
        for base in selected_base_targets)
    improved_count = sum(
        1 for base in selected_base_targets
        if lift_receipt["rows"][base][
            "first_three_improves_after_zero_lift"])
    return {
        "families": profile["families"],
        "arithmetic_period": profile["arithmetic_period"],
        "support": profile["support"],
        "natural_modulus": profile["natural_modulus"],
        "start": start,
        "targets_per_cycle": targets_per_cycle,
        "lifts": tuple(lifts),
        "mode_count": mode_count,
        "significant_negative_ratio": significant_negative_ratio,
        "available_base_target_count": len(base_targets),
        "selected_base_target_count": len(selected_base_targets),
        "selected_base_targets": selected_base_targets,
        "rows": lift_receipt["rows"],
        "improved_first_three_base_count": improved_count,
        "improved_first_three_base_fraction": (
            improved_count / len(selected_base_targets)),
        "maximum_zero_first_three_abs_ratio": max(zero_first_three_ratios),
        "maximum_minimum_lifted_first_three_abs_ratio": max(
            minimum_lifted_first_three_ratios),
        "worst_lifted_first_three_base": worst_lifted_first_three_base,
        "maximum_lifted_first_three_abs_ratio": (
            lift_receipt["maximum_lifted_first_three_abs_ratio"]),
        "worst_lifted_six_base": worst_lifted_six_base,
        "maximum_lifted_six_mode_abs_ratio": (
            lift_receipt["maximum_lifted_six_mode_abs_ratio"]),
        "worst_lifted_q286_base": worst_lifted_q286_base,
        "maximum_lifted_q286_abs_ratio": maximum_lifted_q286_abs_ratio,
        "worst_lifted_residual_base": worst_lifted_residual_base,
        "maximum_lifted_residual_abs_ratio": (
            lift_receipt["maximum_lifted_residual_abs_ratio"]),
        "all_selected_bases_improve_after_zero_lift": bool(
            improved_count == len(selected_base_targets)),
        "all_selected_minimum_lifted_first_three_under_point_one": bool(
            max(minimum_lifted_first_three_ratios) < .1),
        "all_lifted_six_modes_under_half_principal": (
            lift_receipt["lifted_six_modes_under_half_principal"]),
        "significant_lift_envelope_measured": True,
        "eventual_decay_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_leading_mode_period_envelope_receipt(
        start=10000, cycle_count=4, targets_per_cycle=501,
        mode_count=6, significant_negative_ratio=-.4, tolerance=1e-9):
    """Scan two-sided q286 leading-mode envelopes by period cycle."""
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    if type(mode_count) is not int or mode_count < 1 or mode_count > 9:
        raise ValueError("mode_count must lie between 1 and 9")
    if (not math.isfinite(significant_negative_ratio)
            or significant_negative_ratio >= 0):
        raise ValueError(
            "significant_negative_ratio must be finite and negative")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    period = 10010
    targets = tuple(
        start + period * cycle + 2 * index
        for cycle in range(cycle_count)
        for index in range(targets_per_cycle))
    contribution = q286_leading_singular_mode_contribution_receipt(
        targets=targets, mode_count=mode_count, tolerance=tolerance)

    cycle_rows = {}
    worst_abs_q286_target = None
    worst_abs_first_three_target = None
    worst_abs_six_mode_target = None
    worst_abs_residual_target = None
    for cycle in range(cycle_count):
        cycle_targets = targets[
            cycle * targets_per_cycle:(cycle + 1) * targets_per_cycle]
        rows = {target: contribution["rows"][target]
                for target in cycle_targets}
        derived = {}
        for target, row in rows.items():
            mode_ratios = tuple(
                mode_row["contribution_to_principal_ratio"]
                for mode_row in row["mode_rows"])
            first_three = math.fsum(mode_ratios[:min(3, mode_count)])
            six_sum = math.fsum(mode_ratios[:mode_count])
            derived[target] = {
                "q286_ratio": row["q286_deviation_to_principal_ratio"],
                "first_three_ratio": first_three,
                "six_mode_ratio": six_sum,
                "residual_ratio": row["residual_to_principal_ratio"],
            }
        min_q286_target = min(
            cycle_targets, key=lambda target: derived[target]["q286_ratio"])
        max_q286_target = max(
            cycle_targets, key=lambda target: derived[target]["q286_ratio"])
        max_abs_q286_target = max(
            cycle_targets, key=lambda target: abs(
                derived[target]["q286_ratio"]))
        max_abs_first_three_target = max(
            cycle_targets, key=lambda target: abs(
                derived[target]["first_three_ratio"]))
        max_abs_six_mode_target = max(
            cycle_targets, key=lambda target: abs(
                derived[target]["six_mode_ratio"]))
        max_abs_residual_target = max(
            cycle_targets, key=lambda target: abs(
                derived[target]["residual_ratio"]))
        for candidate_name, candidate in (
                ("q286", max_abs_q286_target),
                ("first_three", max_abs_first_three_target),
                ("six", max_abs_six_mode_target),
                ("residual", max_abs_residual_target)):
            if candidate_name == "q286" and (
                    worst_abs_q286_target is None
                    or abs(derived[candidate]["q286_ratio"])
                    > abs(contribution["rows"][
                        worst_abs_q286_target][
                            "q286_deviation_to_principal_ratio"])):
                worst_abs_q286_target = candidate
            elif candidate_name == "first_three" and (
                    worst_abs_first_three_target is None
                    or abs(derived[candidate]["first_three_ratio"])
                    > abs(cycle_rows[
                        worst_abs_first_three_target[0]][
                            "target_rows"][
                                worst_abs_first_three_target[1]][
                                    "first_three_ratio"])):
                worst_abs_first_three_target = (cycle, candidate)
            elif candidate_name == "six" and (
                    worst_abs_six_mode_target is None
                    or abs(derived[candidate]["six_mode_ratio"])
                    > abs(cycle_rows[
                        worst_abs_six_mode_target[0]][
                            "target_rows"][
                                worst_abs_six_mode_target[1]][
                                    "six_mode_ratio"])):
                worst_abs_six_mode_target = (cycle, candidate)
            elif candidate_name == "residual" and (
                    worst_abs_residual_target is None
                    or abs(derived[candidate]["residual_ratio"])
                    > abs(cycle_rows[
                        worst_abs_residual_target[0]][
                            "target_rows"][
                                worst_abs_residual_target[1]][
                                    "residual_ratio"])):
                worst_abs_residual_target = (cycle, candidate)
        cycle_rows[cycle] = {
            "target_range": (cycle_targets[0], cycle_targets[-1]),
            "tested_target_count": len(cycle_targets),
            "negative_q286_deviation_count": sum(
                1 for target in cycle_targets
                if derived[target]["q286_ratio"] < -tolerance),
            "significant_negative_q286_count": sum(
                1 for target in cycle_targets
                if (derived[target]["q286_ratio"]
                    <= significant_negative_ratio)),
            "minimum_q286_target": min_q286_target,
            "minimum_q286_ratio": derived[min_q286_target]["q286_ratio"],
            "maximum_q286_target": max_q286_target,
            "maximum_q286_ratio": derived[max_q286_target]["q286_ratio"],
            "maximum_abs_q286_target": max_abs_q286_target,
            "maximum_abs_q286_ratio": abs(
                derived[max_abs_q286_target]["q286_ratio"]),
            "maximum_abs_first_three_target": max_abs_first_three_target,
            "maximum_abs_first_three_ratio": abs(
                derived[max_abs_first_three_target]["first_three_ratio"]),
            "maximum_abs_six_mode_target": max_abs_six_mode_target,
            "maximum_abs_six_mode_ratio": abs(
                derived[max_abs_six_mode_target]["six_mode_ratio"]),
            "maximum_abs_residual_target": max_abs_residual_target,
            "maximum_abs_residual_ratio": abs(
                derived[max_abs_residual_target]["residual_ratio"]),
            "target_rows": derived,
        }

    worst_first_three_cycle, worst_first_three_target = (
        worst_abs_first_three_target)
    worst_six_cycle, worst_six_target = worst_abs_six_mode_target
    worst_residual_cycle, worst_residual_target = worst_abs_residual_target
    return {
        "families": contribution["families"],
        "arithmetic_period": contribution["arithmetic_period"],
        "support": contribution["support"],
        "natural_modulus": contribution["natural_modulus"],
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "tested_target_count": len(targets),
        "mode_count": mode_count,
        "significant_negative_ratio": significant_negative_ratio,
        "cycle_rows": cycle_rows,
        "worst_abs_q286_target": worst_abs_q286_target,
        "worst_abs_q286_ratio": abs(contribution["rows"][
            worst_abs_q286_target]["q286_deviation_to_principal_ratio"]),
        "worst_abs_first_three_target": worst_first_three_target,
        "worst_abs_first_three_cycle": worst_first_three_cycle,
        "worst_abs_first_three_ratio": cycle_rows[
            worst_first_three_cycle]["target_rows"][
                worst_first_three_target]["first_three_ratio"],
        "worst_abs_six_mode_target": worst_six_target,
        "worst_abs_six_mode_cycle": worst_six_cycle,
        "worst_abs_six_mode_ratio": cycle_rows[
            worst_six_cycle]["target_rows"][
                worst_six_target]["six_mode_ratio"],
        "worst_abs_residual_target": worst_residual_target,
        "worst_abs_residual_cycle": worst_residual_cycle,
        "worst_abs_residual_ratio": cycle_rows[
            worst_residual_cycle]["target_rows"][
                worst_residual_target]["residual_ratio"],
        "maximum_mode_reconstruction_error": (
            contribution["maximum_mode_reconstruction_error"]),
        "six_mode_residual_under_point_one_principal": bool(
            abs(cycle_rows[worst_residual_cycle]["target_rows"][
                worst_residual_target]["residual_ratio"]) < .1),
        "leading_modes_under_two_principal_on_sample": bool(
            abs(cycle_rows[worst_six_cycle]["target_rows"][
                worst_six_target]["six_mode_ratio"]) < 2.0),
        "leading_mode_period_envelope_measured": True,
        "eventual_decay_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def reduced_full_lower_envelope_receipt(
        start=10000, targets_per_cycle=501, q286_mode_count=6,
        tolerance=1e-9, selected_targets=None):
    """Measure the full action with q286 replaced by leading modes plus tail."""
    if selected_targets is None:
        if type(start) is not int or start < 40 or start % 2:
            raise ValueError("start must be an even integer at least 40")
        if (type(targets_per_cycle) is not int or targets_per_cycle < 1
                or targets_per_cycle > 5005):
            raise ValueError("targets_per_cycle must lie between 1 and 5005")
        targets = tuple(start + 2 * index for index in range(
            targets_per_cycle))
    else:
        selected_targets = tuple(dict.fromkeys(selected_targets))
        if (not selected_targets
                or any(type(target) is not int or target < 40
                       or target % 2 for target in selected_targets)):
            raise ValueError(
                "selected_targets must be even integers at least 40")
        targets = selected_targets
        start = targets[0]
        targets_per_cycle = len(targets)
    if (type(q286_mode_count) is not int or q286_mode_count < 1
            or q286_mode_count > 9):
        raise ValueError("q286_mode_count must lie between 1 and 9")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    period_units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    aggregate_values = np.asarray(tuple(
        coefficient["aggregate_coefficient_by_unit_residue"][unit]
        for unit in period_units), dtype=np.complex128)
    principal_mean = complex(np.mean(aggregate_values))
    centered = aggregate_values - principal_mean
    _, period_labels, period_character_table = _unit_character_table(
        period, period_units)
    period_character_coefficients = (
        np.conjugate(period_character_table) @ centered / len(period_units))
    factor_primes = (5, 7, 11, 13)
    support_indices = {}
    for index, label in enumerate(period_labels):
        support = tuple(
            prime for prime, exponent in zip(factor_primes, label)
            if exponent != 0)
        support_indices.setdefault(support, []).append(index)

    support_order = (
        (13,), (11,), (11, 13), (7,), (7, 11),
        (5,), (5, 13), (5, 7))
    support_data = {}
    for support in support_order:
        masked = np.zeros_like(period_character_coefficients)
        masked[support_indices[support]] = period_character_coefficients[
            support_indices[support]]
        component = period_character_table.T @ masked
        modulus = 2
        for prime in support:
            modulus *= prime
        grouped = {}
        for unit, value in zip(period_units, component):
            grouped.setdefault(unit % modulus, []).append(value)
        lower_values = {
            residue: _complex_fsum(values) / len(values)
            for residue, values in grouped.items()}
        data = {
            "natural_modulus": modulus,
            "units": tuple(sorted(lower_values)),
            "lower_values": lower_values,
        }
        if support == (11, 13):
            units = data["units"]
            coefficient_values = np.asarray(tuple(
                lower_values[unit] for unit in units), dtype=np.complex128)
            _, labels, character_table = _unit_character_table(
                modulus, units)
            character_coefficients = (
                np.conjugate(character_table) @ coefficient_values
                / len(units))
            matrix = np.zeros((10, 12), dtype=np.complex128)
            for label, value in zip(labels, character_coefficients):
                matrix[label] = value
            q286_matrix = matrix[1:, 1:]
            left, singular_values, right = np.linalg.svd(
                q286_matrix, full_matrices=False)
            truncated = (
                (left[:, :q286_mode_count]
                 * singular_values[:q286_mode_count])
                @ right[:q286_mode_count, :])
            data.update({
                "unit_index": {
                    unit: index for index, unit in enumerate(units)},
                "coefficient_values": coefficient_values,
                "character_table": character_table,
                "q286_matrix": q286_matrix,
                "q286_truncated_matrix": truncated,
                "q286_tail_matrix": q286_matrix - truncated,
                "q286_singular_energy_fraction": float(
                    np.sum(singular_values[:q286_mode_count] ** 2)
                    / np.sum(singular_values ** 2)),
            })
        support_data[support] = data

    primes = _prime_table(max(targets))
    rows = {}
    maximum_reconstruction_error = 0.0
    for target in targets:
        lower = target // 3
        upper = target - lower
        pairs = []
        total_weight = 0.0
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                weight = math.log(prime) * math.log(partner)
                pairs.append((prime, weight))
                total_weight += weight
        principal_contribution = principal_mean * total_weight
        exact_non_q286_support = 0j
        q286_actual = 0j
        q286_local = 0j
        q286_modeled_deviation = 0j
        q286_tail = 0j
        small_support_contribution = 0j
        support_rows = {}
        for support in support_order:
            data = support_data[support]
            modulus = data["natural_modulus"]
            lower_values = data["lower_values"]
            actual = _complex_fsum(
                lower_values[prime % modulus] * weight
                for prime, weight in pairs)
            if support == (11, 13):
                units = data["units"]
                weights = np.zeros(len(units), dtype=np.float64)
                for prime, weight in pairs:
                    weights[data["unit_index"][prime % modulus]] += weight
                admissible_mask = np.asarray(tuple(
                    math.gcd((target - unit) % modulus, modulus) == 1
                    for unit in units), dtype=bool)
                mean_weight = total_weight / int(np.sum(admissible_mask))
                local = complex(np.sum(
                    data["coefficient_values"][admissible_mask])
                    * mean_weight)
                weight_delta = np.zeros(len(units), dtype=np.float64)
                weight_delta[admissible_mask] = (
                    weights[admissible_mask] - mean_weight)
                imbalance_matrix = (
                    data["character_table"] @ weight_delta).reshape(10, 12)[
                        1:, 1:]
                modeled_deviation = complex(np.sum(
                    data["q286_truncated_matrix"] * imbalance_matrix))
                tail = complex(np.sum(
                    data["q286_tail_matrix"] * imbalance_matrix))
                q286_actual = actual
                q286_local = local
                q286_modeled_deviation = modeled_deviation
                q286_tail = tail
                support_rows[support] = {
                    "actual_contribution": actual,
                    "local_prediction": local,
                    "modeled_deviation": modeled_deviation,
                    "tail": tail,
                    "tail_to_principal_ratio": float(
                        tail.real / principal_contribution.real
                        if abs(principal_contribution.real) > tolerance
                        else math.nan),
                    "tail_reconstruction_error": float(
                        abs(actual - local - modeled_deviation - tail)
                        / max(1.0, abs(actual - local))),
                }
            else:
                exact_non_q286_support += actual
                if support not in ((7, 11), (5, 7)):
                    small_support_contribution += actual
                support_rows[support] = {
                    "actual_contribution": actual,
                    "actual_to_principal_ratio": float(
                        actual.real / principal_contribution.real
                        if abs(principal_contribution.real) > tolerance
                        else math.nan),
                }
        full_action = principal_contribution + exact_non_q286_support + q286_actual
        reduced_model = (
            principal_contribution + exact_non_q286_support
            + q286_local + q286_modeled_deviation)
        reconstruction_error = abs(
            full_action - reduced_model - q286_tail) / max(
                1.0, abs(full_action))
        maximum_reconstruction_error = max(
            maximum_reconstruction_error, reconstruction_error)
        rows[target] = {
            "strict_central_interval": (lower, upper),
            "ordered_central_prime_pair_count": len(pairs),
            "total_prime_pair_weight": total_weight,
            "principal_contribution": principal_contribution,
            "support_rows": support_rows,
            "full_action": full_action,
            "reduced_model": reduced_model,
            "q286_tail": q286_tail,
            "small_support_contribution": small_support_contribution,
            "full_action_to_principal_ratio": float(
                full_action.real / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "reduced_model_to_principal_ratio": float(
                reduced_model.real / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "q286_tail_to_principal_ratio": float(
                q286_tail.real / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "absolute_q286_tail_to_principal_ratio": float(
                abs(q286_tail.real) / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "small_support_to_principal_ratio": float(
                small_support_contribution.real
                / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "reconstruction_error": reconstruction_error,
        }

    worst_full_target = min(
        targets, key=lambda target: rows[target][
            "full_action_to_principal_ratio"])
    worst_model_target = min(
        targets, key=lambda target: rows[target][
            "reduced_model_to_principal_ratio"])
    worst_tail_target = max(
        targets, key=lambda target: rows[target][
            "absolute_q286_tail_to_principal_ratio"])
    negative_full_targets = tuple(
        target for target in targets
        if rows[target]["full_action_to_principal_ratio"] <= 0)
    negative_model_targets = tuple(
        target for target in targets
        if rows[target]["reduced_model_to_principal_ratio"] <= 0)
    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "start": start,
        "targets_per_cycle": targets_per_cycle,
        "selected_targets": (
            targets if selected_targets is not None else None),
        "q286_mode_count": q286_mode_count,
        "q286_singular_energy_fraction": support_data[(11, 13)][
            "q286_singular_energy_fraction"],
        "tested_target_count": len(targets),
        "support_order": support_order,
        "rows": rows,
        "negative_full_action_count": len(negative_full_targets),
        "negative_reduced_model_count": len(negative_model_targets),
        "worst_full_action_target": worst_full_target,
        "minimum_full_action_to_principal_ratio": rows[
            worst_full_target]["full_action_to_principal_ratio"],
        "worst_reduced_model_target": worst_model_target,
        "minimum_reduced_model_to_principal_ratio": rows[
            worst_model_target]["reduced_model_to_principal_ratio"],
        "worst_q286_tail_target": worst_tail_target,
        "maximum_abs_q286_tail_to_principal_ratio": rows[
            worst_tail_target]["absolute_q286_tail_to_principal_ratio"],
        "maximum_reconstruction_error": maximum_reconstruction_error,
        "q286_tail_under_point_one_principal_on_sample": bool(
            rows[worst_tail_target][
                "absolute_q286_tail_to_principal_ratio"] < .1),
        "reduced_full_lower_envelope_measured": True,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def reduced_full_lower_envelope_cycle_scan_receipt(
        start=10000, cycle_count=4, targets_per_cycle=501,
        q286_mode_count=6, tolerance=1e-9):
    """Scan reduced/full lower-envelope agreement across period windows."""
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    if (type(q286_mode_count) is not int or q286_mode_count < 1
            or q286_mode_count > 9):
        raise ValueError("q286_mode_count must lie between 1 and 9")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    first = reduced_full_lower_envelope_receipt(
        start=start, targets_per_cycle=targets_per_cycle,
        q286_mode_count=q286_mode_count, tolerance=tolerance)
    period = first["arithmetic_period"]
    receipts = [first]
    for cycle in range(1, cycle_count):
        receipts.append(reduced_full_lower_envelope_receipt(
            start=start + cycle * period,
            targets_per_cycle=targets_per_cycle,
            q286_mode_count=q286_mode_count,
            tolerance=tolerance))

    cycle_rows = {}
    global_worst_full = None
    global_worst_model = None
    global_worst_tail = None
    maximum_reconstruction_error = 0.0
    all_full_negatives_captured = True
    all_signs_agree = True
    all_tails_small = True
    total_full_negatives = 0
    total_model_negatives = 0
    for cycle, receipt in enumerate(receipts):
        rows = receipt["rows"]
        targets = tuple(sorted(rows))
        full_negatives = tuple(
            target for target in targets
            if rows[target]["full_action_to_principal_ratio"] <= 0)
        model_negatives = tuple(
            target for target in targets
            if rows[target]["reduced_model_to_principal_ratio"] <= 0)
        full_set = set(full_negatives)
        model_set = set(model_negatives)
        extra_model = tuple(sorted(model_set - full_set))
        missing_model = tuple(sorted(full_set - model_set))
        all_full_negatives_captured = (
            all_full_negatives_captured and not missing_model)
        all_signs_agree = (
            all_signs_agree and not extra_model and not missing_model)
        all_tails_small = (
            all_tails_small
            and receipt["q286_tail_under_point_one_principal_on_sample"])
        total_full_negatives += len(full_negatives)
        total_model_negatives += len(model_negatives)
        maximum_reconstruction_error = max(
            maximum_reconstruction_error,
            receipt["maximum_reconstruction_error"])
        worst_full = receipt["worst_full_action_target"]
        worst_model = receipt["worst_reduced_model_target"]
        worst_tail = receipt["worst_q286_tail_target"]
        if (global_worst_full is None
                or rows[worst_full]["full_action_to_principal_ratio"]
                < global_worst_full[1]):
            global_worst_full = (
                worst_full,
                rows[worst_full]["full_action_to_principal_ratio"],
                cycle)
        if (global_worst_model is None
                or rows[worst_model]["reduced_model_to_principal_ratio"]
                < global_worst_model[1]):
            global_worst_model = (
                worst_model,
                rows[worst_model]["reduced_model_to_principal_ratio"],
                cycle)
        if (global_worst_tail is None
                or rows[worst_tail]["absolute_q286_tail_to_principal_ratio"]
                > global_worst_tail[1]):
            global_worst_tail = (
                worst_tail,
                rows[worst_tail]["absolute_q286_tail_to_principal_ratio"],
                cycle)
        cycle_rows[cycle] = {
            "start": targets[0],
            "end": targets[-1],
            "tested_target_count": len(targets),
            "negative_full_action_count": len(full_negatives),
            "negative_reduced_model_count": len(model_negatives),
            "full_negative_targets": full_negatives,
            "reduced_model_negative_targets": model_negatives,
            "extra_model_negative_targets": extra_model,
            "full_negative_not_model_targets": missing_model,
            "worst_full_action_target": worst_full,
            "minimum_full_action_to_principal_ratio": rows[
                worst_full]["full_action_to_principal_ratio"],
            "worst_reduced_model_target": worst_model,
            "minimum_reduced_model_to_principal_ratio": rows[
                worst_model]["reduced_model_to_principal_ratio"],
            "worst_q286_tail_target": worst_tail,
            "maximum_abs_q286_tail_to_principal_ratio": rows[
                worst_tail]["absolute_q286_tail_to_principal_ratio"],
            "maximum_reconstruction_error": (
                receipt["maximum_reconstruction_error"]),
        }

    return {
        "arithmetic_period": period,
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "q286_mode_count": q286_mode_count,
        "tested_target_count": cycle_count * targets_per_cycle,
        "cycle_rows": cycle_rows,
        "total_negative_full_action_count": total_full_negatives,
        "total_negative_reduced_model_count": total_model_negatives,
        "all_full_negatives_captured_by_reduced_model": bool(
            all_full_negatives_captured),
        "all_reduced_and_full_signs_agree": bool(all_signs_agree),
        "q286_tail_under_point_one_principal_on_sample": bool(
            all_tails_small),
        "worst_full_action_target": global_worst_full[0],
        "worst_full_action_cycle": global_worst_full[2],
        "minimum_full_action_to_principal_ratio": global_worst_full[1],
        "worst_reduced_model_target": global_worst_model[0],
        "worst_reduced_model_cycle": global_worst_model[2],
        "minimum_reduced_model_to_principal_ratio": global_worst_model[1],
        "worst_q286_tail_target": global_worst_tail[0],
        "worst_q286_tail_cycle": global_worst_tail[2],
        "maximum_abs_q286_tail_to_principal_ratio": global_worst_tail[1],
        "maximum_reconstruction_error": maximum_reconstruction_error,
        "reduced_full_lower_envelope_cycle_scan_measured": True,
        "eventual_lower_envelope_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_first_two_mode_lower_tail_receipt(
        start=10000, cycle_count=4, targets_per_cycle=501,
        tolerance=1e-9, selected_targets=None):
    """Measure how much of the reduced lower tail is explained by modes 1-2."""
    if selected_targets is None:
        if type(start) is not int or start < 40 or start % 2:
            raise ValueError("start must be an even integer at least 40")
        if type(cycle_count) is not int or cycle_count < 1:
            raise ValueError("cycle_count must be a positive integer")
        if (type(targets_per_cycle) is not int or targets_per_cycle < 1
                or targets_per_cycle > 5005):
            raise ValueError("targets_per_cycle must lie between 1 and 5005")
    else:
        selected_targets = tuple(dict.fromkeys(selected_targets))
        if (not selected_targets
                or any(type(target) is not int or target < 40
                       or target % 2 for target in selected_targets)):
            raise ValueError(
                "selected_targets must be even integers at least 40")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    if selected_targets is None:
        first = reduced_full_lower_envelope_receipt(
            start=start, targets_per_cycle=targets_per_cycle,
            q286_mode_count=6, tolerance=tolerance)
        period = first["arithmetic_period"]
        full_rows = {0: first}
        targets = list(sorted(first["rows"]))
        for cycle in range(1, cycle_count):
            receipt = reduced_full_lower_envelope_receipt(
                start=start + cycle * period,
                targets_per_cycle=targets_per_cycle,
                q286_mode_count=6, tolerance=tolerance)
            full_rows[cycle] = receipt
            targets.extend(sorted(receipt["rows"]))
    else:
        first = reduced_full_lower_envelope_receipt(
            q286_mode_count=6, tolerance=tolerance,
            selected_targets=selected_targets)
        period = first["arithmetic_period"]
        start = selected_targets[0]
        cycle_count = 1
        targets_per_cycle = len(selected_targets)
        full_rows = {0: first}
        targets = list(selected_targets)
    mode_receipt = q286_leading_singular_mode_contribution_receipt(
        targets=tuple(targets), mode_count=6, tolerance=tolerance)

    cycle_rows = {}
    global_rows = {}
    negative_full_count = 0
    negative_full_with_negative_first_two = 0
    negative_full_with_negative_first_three = 0
    first_two_capture_ratios = []
    first_three_capture_ratios = []
    worst_first_two = None
    worst_first_three = None
    worst_without_first_two = None
    worst_without_first_three = None
    worst_remaining_after_first_two = None
    worst_remaining_after_first_three = None
    full_nonpositive_without_first_two_count = 0
    full_nonpositive_without_first_three_count = 0
    for cycle, receipt in full_rows.items():
        row_targets = tuple(sorted(receipt["rows"]))
        full_negative_targets = []
        cycle_capture_ratios = []
        cycle_first_three_capture_ratios = []
        cycle_nonpositive_without_first_two = []
        cycle_nonpositive_without_first_three = []
        for target in row_targets:
            full_row = receipt["rows"][target]
            mode_row = mode_receipt["rows"][target]
            mode_ratios = tuple(
                row["contribution_to_principal_ratio"]
                for row in mode_row["mode_rows"])
            first_two = mode_ratios[0] + mode_ratios[1]
            first_three = first_two + mode_ratios[2]
            modes_three_to_six = sum(mode_ratios[2:])
            without_first_two = (
                full_row["full_action_to_principal_ratio"] - first_two)
            without_first_three = (
                full_row["full_action_to_principal_ratio"] - first_three)
            remaining_after_first_two = (
                full_row["reduced_model_to_principal_ratio"] - first_two)
            remaining_after_first_three = (
                full_row["reduced_model_to_principal_ratio"] - first_three)
            reduced_model_tail_gap = (
                full_row["full_action_to_principal_ratio"]
                - full_row["reduced_model_to_principal_ratio"])
            if without_first_two <= 0:
                full_nonpositive_without_first_two_count += 1
                cycle_nonpositive_without_first_two.append(target)
            if without_first_three <= 0:
                full_nonpositive_without_first_three_count += 1
                cycle_nonpositive_without_first_three.append(target)
            if full_row["full_action_to_principal_ratio"] <= 0:
                full_negative_targets.append(target)
                negative_full_count += 1
                if first_two < 0:
                    negative_full_with_negative_first_two += 1
                if first_three < 0:
                    negative_full_with_negative_first_three += 1
                if abs(full_row["full_action_to_principal_ratio"]) > tolerance:
                    capture = (
                        -first_two
                        / abs(full_row["full_action_to_principal_ratio"]))
                    capture_three = (
                        -first_three
                        / abs(full_row["full_action_to_principal_ratio"]))
                    first_two_capture_ratios.append(capture)
                    first_three_capture_ratios.append(capture_three)
                    cycle_capture_ratios.append(capture)
                    cycle_first_three_capture_ratios.append(capture_three)
            summary = {
                "cycle": cycle,
                "full_action_to_principal_ratio": full_row[
                    "full_action_to_principal_ratio"],
                "reduced_model_to_principal_ratio": full_row[
                    "reduced_model_to_principal_ratio"],
                "q286_deviation_to_principal_ratio": mode_row[
                    "q286_deviation_to_principal_ratio"],
                "mode_1_to_principal_ratio": mode_ratios[0],
                "mode_2_to_principal_ratio": mode_ratios[1],
                "first_two_modes_to_principal_ratio": first_two,
                "first_three_modes_to_principal_ratio": first_three,
                "modes_three_to_six_to_principal_ratio": modes_three_to_six,
                "six_mode_residual_to_principal_ratio": mode_row[
                    "residual_to_principal_ratio"],
                "full_without_first_two_to_principal_ratio": (
                    without_first_two),
                "full_without_first_three_to_principal_ratio": (
                    without_first_three),
                "reduced_without_first_two_to_principal_ratio": (
                    remaining_after_first_two),
                "reduced_without_first_three_to_principal_ratio": (
                    remaining_after_first_three),
                "full_minus_reduced_to_principal_ratio": (
                    reduced_model_tail_gap),
            }
            global_rows[target] = summary
            if worst_first_two is None or first_two < worst_first_two[1]:
                worst_first_two = (target, first_two, cycle)
            if worst_first_three is None or first_three < worst_first_three[1]:
                worst_first_three = (target, first_three, cycle)
            if (worst_without_first_two is None
                    or without_first_two < worst_without_first_two[1]):
                worst_without_first_two = (target, without_first_two, cycle)
            if (worst_without_first_three is None
                    or without_first_three < worst_without_first_three[1]):
                worst_without_first_three = (
                    target, without_first_three, cycle)
            if (worst_remaining_after_first_two is None
                    or remaining_after_first_two
                    < worst_remaining_after_first_two[1]):
                worst_remaining_after_first_two = (
                    target, remaining_after_first_two, cycle)
            if (worst_remaining_after_first_three is None
                    or remaining_after_first_three
                    < worst_remaining_after_first_three[1]):
                worst_remaining_after_first_three = (
                    target, remaining_after_first_three, cycle)
        cycle_rows[cycle] = {
            "start": row_targets[0],
            "end": row_targets[-1],
            "tested_target_count": len(row_targets),
            "negative_full_action_count": len(full_negative_targets),
            "negative_full_targets": tuple(full_negative_targets),
            "negative_full_with_negative_first_two_count": sum(
                1 for target in full_negative_targets
                if global_rows[target][
                    "first_two_modes_to_principal_ratio"] < 0),
            "negative_full_with_negative_first_three_count": sum(
                1 for target in full_negative_targets
                if global_rows[target][
                    "first_three_modes_to_principal_ratio"] < 0),
            "full_nonpositive_without_first_two_count": len(
                cycle_nonpositive_without_first_two),
            "full_nonpositive_without_first_three_count": len(
                cycle_nonpositive_without_first_three),
            "full_nonpositive_without_first_two_targets": tuple(
                cycle_nonpositive_without_first_two),
            "full_nonpositive_without_first_three_targets": tuple(
                cycle_nonpositive_without_first_three),
            "minimum_first_two_capture_on_negative_full_targets": (
                min(cycle_capture_ratios) if cycle_capture_ratios
                else math.nan),
            "maximum_first_two_capture_on_negative_full_targets": (
                max(cycle_capture_ratios) if cycle_capture_ratios
                else math.nan),
            "minimum_first_three_capture_on_negative_full_targets": (
                min(cycle_first_three_capture_ratios)
                if cycle_first_three_capture_ratios else math.nan),
            "maximum_first_three_capture_on_negative_full_targets": (
                max(cycle_first_three_capture_ratios)
                if cycle_first_three_capture_ratios else math.nan),
        }

    return {
        "arithmetic_period": period,
        "support": (11, 13),
        "natural_modulus": 286,
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "selected_targets": (
            tuple(targets) if selected_targets is not None else None),
        "tested_target_count": len(targets),
        "cycle_rows": cycle_rows,
        "rows": global_rows,
        "negative_full_action_count": negative_full_count,
        "negative_full_with_negative_first_two_count": (
            negative_full_with_negative_first_two),
        "negative_full_with_negative_first_three_count": (
            negative_full_with_negative_first_three),
        "full_nonpositive_without_first_two_count": (
            full_nonpositive_without_first_two_count),
        "full_nonpositive_without_first_three_count": (
            full_nonpositive_without_first_three_count),
        "minimum_first_two_capture_on_negative_full_targets": (
            min(first_two_capture_ratios) if first_two_capture_ratios
            else math.nan),
        "maximum_first_two_capture_on_negative_full_targets": (
            max(first_two_capture_ratios) if first_two_capture_ratios
            else math.nan),
        "minimum_first_three_capture_on_negative_full_targets": (
            min(first_three_capture_ratios) if first_three_capture_ratios
            else math.nan),
        "maximum_first_three_capture_on_negative_full_targets": (
            max(first_three_capture_ratios) if first_three_capture_ratios
            else math.nan),
        "worst_first_two_mode_target": worst_first_two[0],
        "worst_first_two_mode_cycle": worst_first_two[2],
        "minimum_first_two_modes_to_principal_ratio": worst_first_two[1],
        "worst_first_three_mode_target": worst_first_three[0],
        "worst_first_three_mode_cycle": worst_first_three[2],
        "minimum_first_three_modes_to_principal_ratio": worst_first_three[1],
        "worst_full_without_first_two_target": worst_without_first_two[0],
        "worst_full_without_first_two_cycle": worst_without_first_two[2],
        "minimum_full_without_first_two_to_principal_ratio": (
            worst_without_first_two[1]),
        "worst_full_without_first_three_target": (
            worst_without_first_three[0]),
        "worst_full_without_first_three_cycle": (
            worst_without_first_three[2]),
        "minimum_full_without_first_three_to_principal_ratio": (
            worst_without_first_three[1]),
        "worst_reduced_without_first_two_target": (
            worst_remaining_after_first_two[0]),
        "worst_reduced_without_first_two_cycle": (
            worst_remaining_after_first_two[2]),
        "minimum_reduced_without_first_two_to_principal_ratio": (
            worst_remaining_after_first_two[1]),
        "worst_reduced_without_first_three_target": (
            worst_remaining_after_first_three[0]),
        "worst_reduced_without_first_three_cycle": (
            worst_remaining_after_first_three[2]),
        "minimum_reduced_without_first_three_to_principal_ratio": (
            worst_remaining_after_first_three[1]),
        "first_two_mode_lower_tail_measured": True,
        "first_two_modes_alone_prove_lower_envelope": False,
        "eventual_lower_envelope_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_ap_discrepancy_proxy_receipt(
        start=10000, targets_per_cycle=501, selected_targets=None,
        top_count=8, tolerance=1e-9):
    """Compare first-three q286 modes with ordinary AP discrepancy proxies."""
    if selected_targets is None:
        if type(start) is not int or start < 40 or start % 2:
            raise ValueError("start must be an even integer at least 40")
        if (type(targets_per_cycle) is not int or targets_per_cycle < 1
                or targets_per_cycle > 5005):
            raise ValueError("targets_per_cycle must lie between 1 and 5005")
        targets = tuple(start + 2 * index for index in range(
            targets_per_cycle))
    else:
        selected_targets = tuple(dict.fromkeys(selected_targets))
        if (not selected_targets
                or any(type(target) is not int or target < 40
                       or target % 2 for target in selected_targets)):
            raise ValueError(
                "selected_targets must be even integers at least 40")
        targets = selected_targets
        start = targets[0]
        targets_per_cycle = len(targets)
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    if type(top_count) is not int or top_count < 1:
        raise ValueError("top_count must be a positive integer")

    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    period_units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    aggregate_values = np.asarray(tuple(
        coefficient["aggregate_coefficient_by_unit_residue"][unit]
        for unit in period_units), dtype=np.complex128)
    principal_mean = complex(np.mean(aggregate_values))

    character_receipt = q286_character_imbalance_receipt(
        targets=(10424,), top_count=120, tolerance=tolerance)
    matrix = np.zeros((10, 12), dtype=np.complex128)
    for row in character_receipt["top_coefficient_character_rows"]:
        first, second = row["label"]
        matrix[first, second] = row["coefficient"]
    coefficient_matrix = matrix[1:, 1:]
    left, singular_values, right = np.linalg.svd(
        coefficient_matrix, full_matrices=False)
    truncated_matrix = (
        (left[:, :3] * singular_values[:3]) @ right[:3, :])

    modulus = 286
    units = tuple(unit for unit in range(modulus)
                  if math.gcd(unit, modulus) == 1)
    _, labels, character_table = _unit_character_table(modulus, units)
    mode_coefficients = np.zeros(len(labels), dtype=np.complex128)
    for index, label in enumerate(labels):
        first, second = label
        if first and second:
            mode_coefficients[index] = truncated_matrix[
                first - 1, second - 1]
    mode_values = character_table.T @ mode_coefficients
    unit_index = {unit: index for index, unit in enumerate(units)}

    primes = _prime_table(max(targets))
    rows = {}
    negative_first_three_targets = []
    worst_negative_first_three = None
    worst_required_uniform = None
    worst_required_uniform_negative = None
    worst_l2_alignment = None
    worst_l2_alignment_negative = None
    maximum_reconstruction_error = 0.0
    for target in targets:
        weights = np.zeros(len(units), dtype=np.float64)
        total_weight = 0.0
        lower = target // 3
        upper = target - lower
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                weight = math.log(prime) * math.log(partner)
                weights[unit_index[prime % modulus]] += weight
                total_weight += weight
        admissible_mask = np.asarray(tuple(
            math.gcd((target - unit) % modulus, modulus) == 1
            for unit in units), dtype=bool)
        admissible_count = int(np.sum(admissible_mask))
        mean_weight = total_weight / admissible_count
        delta = np.zeros(len(units), dtype=np.float64)
        delta[admissible_mask] = weights[admissible_mask] - mean_weight
        coefficients = mode_values[admissible_mask]
        deltas = delta[admissible_mask]
        first_three = complex(np.sum(mode_values * delta))
        imbalance_matrix = (
            character_table @ delta).reshape(10, 12)[1:, 1:]
        matrix_first_three = complex(np.sum(
            truncated_matrix * imbalance_matrix))
        reconstruction_error = abs(first_three - matrix_first_three) / max(
            1.0, abs(first_three))
        maximum_reconstruction_error = max(
            maximum_reconstruction_error, reconstruction_error)
        principal_contribution = principal_mean * total_weight
        l1_envelope = mean_weight * float(np.sum(np.abs(coefficients)))
        l2_envelope = float(
            np.linalg.norm(deltas) * np.linalg.norm(coefficients))
        maximum_relative_residue_deviation = float(
            np.max(np.abs(deltas)) / mean_weight
            if abs(mean_weight) > tolerance else math.nan)
        rms_relative_residue_deviation = float(
            np.linalg.norm(deltas) / (mean_weight * math.sqrt(
                admissible_count))
            if abs(mean_weight) > tolerance else math.nan)
        required_uniform_error = float(
            abs(first_three.real) / l1_envelope
            if l1_envelope > tolerance else math.nan)
        l2_alignment = float(
            abs(first_three.real) / l2_envelope
            if l2_envelope > tolerance else math.nan)
        first_three_ratio = float(
            first_three.real / principal_contribution.real
            if abs(principal_contribution.real) > tolerance else math.nan)
        residue_rows = []
        for position, unit in enumerate(units):
            if not admissible_mask[position]:
                continue
            contribution = mode_values[position] * delta[position]
            residue_rows.append({
                "residue_mod_286": unit,
                "coefficient": complex(mode_values[position]),
                "coefficient_real": float(mode_values[position].real),
                "prime_pair_weight": float(weights[position]),
                "weight_delta": float(delta[position]),
                "relative_weight_delta": float(
                    delta[position] / mean_weight
                    if abs(mean_weight) > tolerance else math.nan),
                "real_contribution": float(contribution.real),
                "contribution_to_principal_ratio": float(
                    contribution.real / principal_contribution.real
                    if abs(principal_contribution.real) > tolerance
                    else math.nan),
            })
        total_abs_real_contribution = math.fsum(
            abs(row["real_contribution"]) for row in residue_rows)
        negative_real_contribution = math.fsum(
            row["real_contribution"] for row in residue_rows
            if row["real_contribution"] < 0)
        positive_real_contribution = math.fsum(
            row["real_contribution"] for row in residue_rows
            if row["real_contribution"] > 0)
        largest_negative_rows = tuple(sorted(
            residue_rows, key=lambda row: row["real_contribution"])[
                :top_count])
        largest_positive_rows = tuple(sorted(
            residue_rows, key=lambda row: row["real_contribution"],
            reverse=True)[:top_count])
        largest_abs_rows = tuple(sorted(
            residue_rows, key=lambda row: abs(row["real_contribution"]),
            reverse=True)[:top_count])
        top_abs_sum = math.fsum(
            abs(row["real_contribution"]) for row in largest_abs_rows)
        signed_cancellation_ratio = float(
            first_three.real / total_abs_real_contribution
            if total_abs_real_contribution > tolerance else math.nan)
        top_abs_energy_fraction = float(
            top_abs_sum / total_abs_real_contribution
            if total_abs_real_contribution > tolerance else math.nan)
        row = {
            "strict_central_interval": (lower, upper),
            "admissible_residue_count": admissible_count,
            "total_prime_pair_weight": total_weight,
            "mean_admissible_residue_weight": mean_weight,
            "first_three_mode_contribution": first_three,
            "first_three_mode_to_principal_ratio": first_three_ratio,
            "maximum_relative_residue_deviation": (
                maximum_relative_residue_deviation),
            "rms_relative_residue_deviation": (
                rms_relative_residue_deviation),
            "uniform_l1_ap_envelope": l1_envelope,
            "l2_ap_envelope": l2_envelope,
            "uniform_l1_ap_envelope_to_principal_ratio": float(
                l1_envelope / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "l2_ap_envelope_to_principal_ratio": float(
                l2_envelope / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "required_uniform_relative_error_for_actual_first_three": (
                required_uniform_error),
            "first_three_l2_alignment_ratio": l2_alignment,
            "negative_real_contribution_to_principal_ratio": float(
                negative_real_contribution / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "positive_real_contribution_to_principal_ratio": float(
                positive_real_contribution / principal_contribution.real
                if abs(principal_contribution.real) > tolerance
                else math.nan),
            "signed_to_absolute_real_contribution_ratio": (
                signed_cancellation_ratio),
            "top_abs_real_contribution_fraction": top_abs_energy_fraction,
            "largest_negative_residue_rows": largest_negative_rows,
            "largest_positive_residue_rows": largest_positive_rows,
            "largest_abs_residue_rows": largest_abs_rows,
            "mode_reconstruction_error": reconstruction_error,
        }
        rows[target] = row
        if first_three_ratio < 0:
            negative_first_three_targets.append(target)
            if (worst_required_uniform_negative is None
                    or required_uniform_error
                    > worst_required_uniform_negative[1]):
                worst_required_uniform_negative = (
                    target, required_uniform_error)
            if (worst_l2_alignment_negative is None
                    or l2_alignment > worst_l2_alignment_negative[1]):
                worst_l2_alignment_negative = (target, l2_alignment)
        if (worst_negative_first_three is None
                or first_three_ratio < worst_negative_first_three[1]):
            worst_negative_first_three = (target, first_three_ratio)
        if (worst_required_uniform is None
                or required_uniform_error > worst_required_uniform[1]):
            worst_required_uniform = (target, required_uniform_error)
        if (worst_l2_alignment is None
                or l2_alignment > worst_l2_alignment[1]):
            worst_l2_alignment = (target, l2_alignment)

    return {
        "arithmetic_period": period,
        "support": (11, 13),
        "natural_modulus": modulus,
        "start": start,
        "targets_per_cycle": targets_per_cycle,
        "selected_targets": (
            targets if selected_targets is not None else None),
        "tested_target_count": len(targets),
        "rows": rows,
        "negative_first_three_mode_count": len(negative_first_three_targets),
        "negative_first_three_mode_targets": tuple(
            negative_first_three_targets),
        "worst_negative_first_three_target": worst_negative_first_three[0],
        "minimum_first_three_mode_to_principal_ratio": (
            worst_negative_first_three[1]),
        "largest_required_uniform_error_target": worst_required_uniform[0],
        "largest_required_uniform_relative_error_for_actual_first_three": (
            worst_required_uniform[1]),
        "largest_required_uniform_error_negative_first_three_target": (
            worst_required_uniform_negative[0]
            if worst_required_uniform_negative is not None else None),
        "largest_required_uniform_relative_error_on_negative_first_three": (
            worst_required_uniform_negative[1]
            if worst_required_uniform_negative is not None else math.nan),
        "largest_l2_alignment_target": worst_l2_alignment[0],
        "largest_first_three_l2_alignment_ratio": worst_l2_alignment[1],
        "largest_l2_alignment_negative_first_three_target": (
            worst_l2_alignment_negative[0]
            if worst_l2_alignment_negative is not None else None),
        "largest_l2_alignment_ratio_on_negative_first_three": (
            worst_l2_alignment_negative[1]
            if worst_l2_alignment_negative is not None else math.nan),
        "maximum_mode_reconstruction_error": maximum_reconstruction_error,
        "first_three_ap_discrepancy_proxy_measured": True,
        "ordinary_ap_discrepancy_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_full_negative_driver_receipt(
        start=10000, targets_per_cycle=5005, driver_residues=(133, 153),
        top_count=8, tolerance=1e-9):
    """Summarize q286 first-three residue drivers on full-action negatives."""
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    driver_residues = tuple(driver_residues)
    if (not driver_residues
            or any(type(residue) is not int or math.gcd(residue, 286) != 1
                   for residue in driver_residues)):
        raise ValueError("driver_residues must be units modulo 286")
    if type(top_count) is not int or top_count < 1:
        raise ValueError("top_count must be a positive integer")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    full_receipt = reduced_full_lower_envelope_receipt(
        start=start, targets_per_cycle=targets_per_cycle,
        q286_mode_count=6, tolerance=tolerance)
    full_negative_targets = tuple(
        target for target, row in full_receipt["rows"].items()
        if row["full_action_to_principal_ratio"] <= 0)
    if full_negative_targets:
        proxy = q286_first_three_ap_discrepancy_proxy_receipt(
            selected_targets=full_negative_targets, top_count=top_count,
            tolerance=tolerance)
    else:
        proxy = None

    residue_top_negative_counts = {residue: 0 for residue in driver_residues}
    residue_empty_top_negative_counts = {
        residue: 0 for residue in driver_residues}
    residue_occupancy_counts = {
        residue: {
            "admissible_count": 0,
            "admissible_empty_count": 0,
            "admissible_positive_count": 0,
            "inadmissible_count": 0,
        } for residue in driver_residues}
    all_driver_residues_in_top_negative_count = 0
    all_driver_residues_empty_top_negative_count = 0
    all_driver_residues_admissible_count = 0
    all_driver_residues_admissible_empty_count = 0
    top_abs_fractions = []
    target_rows = {}
    primes = _prime_table(max(full_negative_targets)) if full_negative_targets else ()
    for target in full_negative_targets:
        proxy_row = proxy["rows"][target]
        top_negative_by_residue = {
            row["residue_mod_286"]: row
            for row in proxy_row["largest_negative_residue_rows"]}
        lower = target // 3
        upper = target - lower
        occupancy_rows = []
        all_admissible = True
        all_admissible_empty = True
        for residue in driver_residues:
            admissible = math.gcd((target - residue) % 286, 286) == 1
            pair_count = 0
            pair_weight = 0.0
            first_pair = None
            if admissible:
                residue_occupancy_counts[residue]["admissible_count"] += 1
                for prime in range(max(2, lower + 1), min(target, upper)):
                    partner = target - prime
                    if (prime % 286 == residue
                            and primes[prime] and primes[partner]):
                        weight = math.log(prime) * math.log(partner)
                        pair_count += 1
                        pair_weight += weight
                        if first_pair is None:
                            first_pair = (prime, partner)
                if pair_count:
                    residue_occupancy_counts[residue][
                        "admissible_positive_count"] += 1
                    all_admissible_empty = False
                else:
                    residue_occupancy_counts[residue][
                        "admissible_empty_count"] += 1
            else:
                residue_occupancy_counts[residue]["inadmissible_count"] += 1
                all_admissible = False
                all_admissible_empty = False
            occupancy_rows.append({
                "residue_mod_286": residue,
                "admissible_for_target": admissible,
                "strict_central_prime_pair_count": pair_count,
                "strict_central_prime_pair_weight": pair_weight,
                "first_strict_central_pair": first_pair,
            })
        if all_admissible:
            all_driver_residues_admissible_count += 1
        if all_admissible and all_admissible_empty:
            all_driver_residues_admissible_empty_count += 1
        present = tuple(
            residue for residue in driver_residues
            if residue in top_negative_by_residue)
        empty = tuple(
            residue for residue in present
            if (top_negative_by_residue[residue][
                    "relative_weight_delta"] <= -1 + tolerance))
        for residue in present:
            residue_top_negative_counts[residue] += 1
        for residue in empty:
            residue_empty_top_negative_counts[residue] += 1
        if len(present) == len(driver_residues):
            all_driver_residues_in_top_negative_count += 1
        if len(empty) == len(driver_residues):
            all_driver_residues_empty_top_negative_count += 1
        top_abs_fractions.append(proxy_row["top_abs_real_contribution_fraction"])
        target_rows[target] = {
            "full_action_to_principal_ratio": full_receipt["rows"][target][
                "full_action_to_principal_ratio"],
            "first_three_mode_to_principal_ratio": proxy_row[
                "first_three_mode_to_principal_ratio"],
            "top_abs_real_contribution_fraction": proxy_row[
                "top_abs_real_contribution_fraction"],
            "driver_residues_in_top_negative": present,
            "empty_driver_residues_in_top_negative": empty,
            "driver_residue_occupancy_rows": tuple(occupancy_rows),
            "driver_residue_rows": tuple(
                top_negative_by_residue[residue]
                for residue in present),
        }

    return {
        "arithmetic_period": full_receipt["arithmetic_period"],
        "support": (11, 13),
        "natural_modulus": 286,
        "start": start,
        "targets_per_cycle": targets_per_cycle,
        "top_count": top_count,
        "driver_residues": driver_residues,
        "full_negative_target_count": len(full_negative_targets),
        "full_negative_targets": full_negative_targets,
        "target_rows": target_rows,
        "driver_residue_top_negative_counts": (
            residue_top_negative_counts),
        "driver_residue_empty_top_negative_counts": (
            residue_empty_top_negative_counts),
        "driver_residue_occupancy_counts": residue_occupancy_counts,
        "all_driver_residues_in_top_negative_count": (
            all_driver_residues_in_top_negative_count),
        "all_driver_residues_empty_top_negative_count": (
            all_driver_residues_empty_top_negative_count),
        "all_driver_residues_admissible_count": (
            all_driver_residues_admissible_count),
        "all_driver_residues_admissible_empty_count": (
            all_driver_residues_admissible_empty_count),
        "minimum_top_abs_real_contribution_fraction": (
            min(top_abs_fractions) if top_abs_fractions else math.nan),
        "mean_top_abs_real_contribution_fraction": (
            math.fsum(top_abs_fractions) / len(top_abs_fractions)
            if top_abs_fractions else math.nan),
        "maximum_top_abs_real_contribution_fraction": (
            max(top_abs_fractions) if top_abs_fractions else math.nan),
        "full_negative_driver_measured": True,
        "driver_residues_explain_all_negatives": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_driver_residue_lift_occupancy_receipt(
        base_targets=None, start=10000, targets_per_cycle=5005,
        lifts=(0, 1, 4, 9, 19, 49), driver_residues=(133, 153),
        tolerance=1e-9):
    """Track q286 driver-residue strict-central occupancy across lifts."""
    if base_targets is None:
        if type(start) is not int or start < 40 or start % 2:
            raise ValueError("start must be an even integer at least 40")
        if (type(targets_per_cycle) is not int or targets_per_cycle < 1
                or targets_per_cycle > 5005):
            raise ValueError("targets_per_cycle must lie between 1 and 5005")
    else:
        base_targets = tuple(dict.fromkeys(base_targets))
        if (not base_targets
                or any(type(target) is not int or target < 40
                       or target % 2 for target in base_targets)):
            raise ValueError("base_targets must be even integers at least 40")
        start = min(base_targets)
        targets_per_cycle = len(base_targets)
    lifts = tuple(lifts)
    if not lifts or any(type(lift) is not int or lift < 0 for lift in lifts):
        raise ValueError("lifts must be nonnegative integers")
    driver_residues = tuple(driver_residues)
    if (not driver_residues
            or any(type(residue) is not int or math.gcd(residue, 286) != 1
                   for residue in driver_residues)):
        raise ValueError("driver_residues must be units modulo 286")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    if base_targets is None:
        base_receipt = reduced_full_lower_envelope_receipt(
            start=start, targets_per_cycle=targets_per_cycle,
            q286_mode_count=6, tolerance=tolerance)
        period = base_receipt["arithmetic_period"]
        base_targets = tuple(
            target for target, row in base_receipt["rows"].items()
            if row["full_action_to_principal_ratio"] <= 0)
    else:
        period = 10010
    lifted_targets = tuple(dict.fromkeys(
        base + lift * period for base in base_targets for lift in lifts))
    action_receipt = reduced_full_lower_envelope_receipt(
        selected_targets=lifted_targets, q286_mode_count=6,
        tolerance=tolerance)
    primes = _prime_table(max(lifted_targets))

    lift_rows = {
        lift: {
            "target_count": 0,
            "negative_full_action_count": 0,
            "all_driver_residues_admissible_count": 0,
            "all_driver_residues_admissible_empty_count": 0,
            "any_driver_residue_positive_count": 0,
            "all_driver_residues_positive_count": 0,
        } for lift in lifts}
    target_rows = {}
    negative_with_all_empty = []
    positive_with_all_empty = []
    first_full_positive_lifts = {}
    first_any_driver_positive_lifts = {}
    first_all_driver_positive_lifts = {}
    first_not_all_driver_admissible_empty_lifts = {}
    for base in base_targets:
        per_lift = {}
        for lift in lifts:
            target = base + lift * period
            action_ratio = action_receipt["rows"][target][
                "full_action_to_principal_ratio"]
            lower = target // 3
            upper = target - lower
            occupancy_rows = []
            all_admissible = True
            all_admissible_empty = True
            any_positive = False
            all_positive = True
            for residue in driver_residues:
                admissible = math.gcd((target - residue) % 286, 286) == 1
                pair_count = 0
                pair_weight = 0.0
                first_pair = None
                if admissible:
                    for prime in range(max(2, lower + 1), min(target, upper)):
                        partner = target - prime
                        if (prime % 286 == residue
                                and primes[prime] and primes[partner]):
                            weight = math.log(prime) * math.log(partner)
                            pair_count += 1
                            pair_weight += weight
                            if first_pair is None:
                                first_pair = (prime, partner)
                else:
                    all_admissible = False
                if pair_count:
                    any_positive = True
                    all_admissible_empty = False
                else:
                    all_positive = False
                    if not admissible:
                        all_admissible_empty = False
                occupancy_rows.append({
                    "residue_mod_286": residue,
                    "admissible_for_target": admissible,
                    "strict_central_prime_pair_count": pair_count,
                    "strict_central_prime_pair_weight": pair_weight,
                    "first_strict_central_pair": first_pair,
                })
            lift_rows[lift]["target_count"] += 1
            if action_ratio <= 0:
                lift_rows[lift]["negative_full_action_count"] += 1
            elif base not in first_full_positive_lifts:
                first_full_positive_lifts[base] = lift
            if all_admissible:
                lift_rows[lift][
                    "all_driver_residues_admissible_count"] += 1
            if all_admissible and all_admissible_empty:
                lift_rows[lift][
                    "all_driver_residues_admissible_empty_count"] += 1
                if action_ratio <= 0:
                    negative_with_all_empty.append((base, lift, target))
                else:
                    positive_with_all_empty.append((base, lift, target))
            elif base not in first_not_all_driver_admissible_empty_lifts:
                first_not_all_driver_admissible_empty_lifts[base] = lift
            if any_positive:
                lift_rows[lift]["any_driver_residue_positive_count"] += 1
                if base not in first_any_driver_positive_lifts:
                    first_any_driver_positive_lifts[base] = lift
            if all_positive:
                lift_rows[lift]["all_driver_residues_positive_count"] += 1
                if base not in first_all_driver_positive_lifts:
                    first_all_driver_positive_lifts[base] = lift
            per_lift[lift] = {
                "target": target,
                "full_action_to_principal_ratio": action_ratio,
                "all_driver_residues_admissible": all_admissible,
                "all_driver_residues_admissible_empty": (
                    all_admissible and all_admissible_empty),
                "any_driver_residue_positive": any_positive,
                "all_driver_residues_positive": all_positive,
                "driver_residue_occupancy_rows": tuple(occupancy_rows),
            }
        target_rows[base] = per_lift

    return {
        "arithmetic_period": period,
        "support": (11, 13),
        "natural_modulus": 286,
        "base_targets": base_targets,
        "base_target_count": len(base_targets),
        "lifts": lifts,
        "driver_residues": driver_residues,
        "tested_target_count": len(lifted_targets),
        "lift_rows": lift_rows,
        "target_rows": target_rows,
        "negative_with_all_driver_residues_empty_count": len(
            negative_with_all_empty),
        "positive_with_all_driver_residues_empty_count": len(
            positive_with_all_empty),
        "negative_with_all_driver_residues_empty_rows": tuple(
            negative_with_all_empty),
        "positive_with_all_driver_residues_empty_rows": tuple(
            positive_with_all_empty),
        "first_full_positive_lift_by_base": first_full_positive_lifts,
        "first_any_driver_positive_lift_by_base": (
            first_any_driver_positive_lifts),
        "first_all_driver_positive_lift_by_base": (
            first_all_driver_positive_lifts),
        "first_not_all_driver_admissible_empty_lift_by_base": (
            first_not_all_driver_admissible_empty_lifts),
        "base_targets_without_positive_full_action_lift_count": (
            len(base_targets) - len(first_full_positive_lifts)),
        "base_targets_without_any_driver_positive_lift_count": (
            len(base_targets) - len(first_any_driver_positive_lifts)),
        "base_targets_without_all_driver_positive_lift_count": (
            len(base_targets) - len(first_all_driver_positive_lifts)),
        "base_targets_without_not_all_driver_admissible_empty_lift_count": (
            len(base_targets)
            - len(first_not_all_driver_admissible_empty_lifts)),
        "maximum_first_full_positive_lift": (
            max(first_full_positive_lifts.values())
            if first_full_positive_lifts else None),
        "maximum_first_any_driver_positive_lift": (
            max(first_any_driver_positive_lifts.values())
            if first_any_driver_positive_lifts else None),
        "maximum_first_all_driver_positive_lift": (
            max(first_all_driver_positive_lifts.values())
            if first_all_driver_positive_lifts else None),
        "maximum_first_not_all_driver_admissible_empty_lift": (
            max(first_not_all_driver_admissible_empty_lifts.values())
            if first_not_all_driver_admissible_empty_lifts else None),
        "driver_residue_lift_occupancy_measured": True,
        "driver_residue_hitting_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_singular_mode_lower_tail_stress_receipt(
        targets=(10424, 10664, 10814, 14138, 14732, 58736, 88346, 125504),
        tolerance=1e-9):
    """Stress-test q286 singular modes beyond the original bad targets."""
    approximation = q286_singular_mode_approximation_receipt(
        targets=targets, modes=(2, 4, 9), tolerance=tolerance)
    negative_targets = tuple(
        target for target, row in approximation["rows"].items()
        if row["deviation_to_principal_ratio"] < -tolerance)
    nonnegative_targets = tuple(
        target for target, row in approximation["rows"].items()
        if row["deviation_to_principal_ratio"] >= -tolerance)
    max_negative_top_four_residual = max(
        (approximation["rows"][target]["mode_rows"][4][
            "absolute_residual_to_abs_deviation_ratio"]
         for target in negative_targets), default=0.0)
    max_negative_top_two_residual = max(
        (approximation["rows"][target]["mode_rows"][2][
            "absolute_residual_to_abs_deviation_ratio"]
         for target in negative_targets), default=0.0)
    worst_all_top_four_target = max(
        approximation["rows"],
        key=lambda target: approximation["rows"][target]["mode_rows"][4][
            "absolute_residual_to_abs_deviation_ratio"])
    worst_negative_top_four_target = (
        max(
            negative_targets,
            key=lambda target: approximation["rows"][target]["mode_rows"][4][
                "absolute_residual_to_abs_deviation_ratio"])
        if negative_targets else None)
    worst_top_four_cauchy_target = max(
        approximation["rows"],
        key=lambda target: approximation["rows"][target]["mode_rows"][4][
            "residual_cauchy_to_abs_deviation_ratio"])
    return {
        "families": approximation["families"],
        "arithmetic_period": approximation["arithmetic_period"],
        "support": approximation["support"],
        "natural_modulus": approximation["natural_modulus"],
        "targets": targets,
        "negative_q286_deviation_targets": negative_targets,
        "nonnegative_q286_deviation_targets": nonnegative_targets,
        "rows": approximation["rows"],
        "maximum_full_singular_reconstruction_error": (
            approximation["maximum_full_singular_reconstruction_error"]),
        "maximum_negative_top_two_signed_residual_fraction": (
            max_negative_top_two_residual),
        "maximum_negative_top_four_signed_residual_fraction": (
            max_negative_top_four_residual),
        "worst_all_top_four_residual_target": worst_all_top_four_target,
        "worst_negative_top_four_residual_target": (
            worst_negative_top_four_target),
        "worst_top_four_cauchy_target": worst_top_four_cauchy_target,
        "top_four_modes_control_sampled_negative_lower_tail": bool(
            negative_targets and max_negative_top_four_residual < .06),
        "top_four_modes_control_all_sampled_targets": bool(
            approximation["top_four_signed_residual_fraction_maximum"] < .06),
        "top_four_tail_paid_by_cauchy_on_sample": bool(
            approximation["top_four_cauchy_residual_fraction_maximum"] < .05),
        "singular_mode_lower_tail_stress_measured": True,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def q286_singular_mode_cycle_scan_receipt(
        start=10000, cycle_count=4, targets_per_cycle=251,
        significant_negative_ratio=-.4, tolerance=1e-9):
    """Scan whether q286 singular modes control sampled lower tails."""
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    if (not math.isfinite(significant_negative_ratio)
            or significant_negative_ratio >= 0):
        raise ValueError(
            "significant_negative_ratio must be finite and negative")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    period = 10010
    targets = tuple(
        start + cycle * period + 2 * index
        for cycle in range(cycle_count)
        for index in range(targets_per_cycle))
    approximation = q286_singular_mode_approximation_receipt(
        targets=targets, modes=(2, 4, 6, 9), tolerance=tolerance)
    cycle_rows = {}
    global_negative_targets = []
    global_significant_negative_targets = []
    global_nonnegative_targets = []
    worst_negative_top_four = None
    worst_significant_negative_top_four = None
    worst_significant_negative_top_six = None
    worst_all_top_four = None
    worst_negative_top_two = None
    worst_top_four_principal_residual = None
    worst_top_six_principal_residual = None
    for cycle in range(cycle_count):
        cycle_targets = targets[
            cycle * targets_per_cycle:(cycle + 1) * targets_per_cycle]
        negative_targets = tuple(
            target for target in cycle_targets
            if approximation["rows"][target][
                "deviation_to_principal_ratio"] < -tolerance)
        nonnegative_targets = tuple(
            target for target in cycle_targets
            if approximation["rows"][target][
                "deviation_to_principal_ratio"] >= -tolerance)
        significant_negative_targets = tuple(
            target for target in negative_targets
            if approximation["rows"][target][
                "deviation_to_principal_ratio"]
            <= significant_negative_ratio)
        global_negative_targets.extend(negative_targets)
        global_significant_negative_targets.extend(
            significant_negative_targets)
        global_nonnegative_targets.extend(nonnegative_targets)
        if negative_targets:
            cycle_worst_negative_top_four = max(
                negative_targets,
                key=lambda target: approximation["rows"][target][
                    "mode_rows"][4][
                        "absolute_residual_to_abs_deviation_ratio"])
            cycle_worst_negative_top_two = max(
                negative_targets,
                key=lambda target: approximation["rows"][target][
                    "mode_rows"][2][
                        "absolute_residual_to_abs_deviation_ratio"])
            if (worst_negative_top_four is None
                    or approximation["rows"][cycle_worst_negative_top_four][
                        "mode_rows"][4][
                            "absolute_residual_to_abs_deviation_ratio"]
                    > approximation["rows"][worst_negative_top_four][
                        "mode_rows"][4][
                            "absolute_residual_to_abs_deviation_ratio"]):
                worst_negative_top_four = cycle_worst_negative_top_four
            if (worst_negative_top_two is None
                    or approximation["rows"][cycle_worst_negative_top_two][
                        "mode_rows"][2][
                            "absolute_residual_to_abs_deviation_ratio"]
                    > approximation["rows"][worst_negative_top_two][
                        "mode_rows"][2][
                            "absolute_residual_to_abs_deviation_ratio"]):
                worst_negative_top_two = cycle_worst_negative_top_two
        if significant_negative_targets:
            cycle_worst_significant_negative_top_four = max(
                significant_negative_targets,
                key=lambda target: approximation["rows"][target][
                    "mode_rows"][4][
                        "absolute_residual_to_abs_deviation_ratio"])
            cycle_worst_significant_negative_top_six = max(
                significant_negative_targets,
                key=lambda target: approximation["rows"][target][
                    "mode_rows"][6][
                        "absolute_residual_to_abs_deviation_ratio"])
            if (worst_significant_negative_top_four is None
                    or approximation["rows"][
                        cycle_worst_significant_negative_top_four][
                            "mode_rows"][4][
                                "absolute_residual_to_abs_deviation_ratio"]
                    > approximation["rows"][
                        worst_significant_negative_top_four][
                            "mode_rows"][4][
                                "absolute_residual_to_abs_deviation_ratio"]):
                worst_significant_negative_top_four = (
                    cycle_worst_significant_negative_top_four)
            if (worst_significant_negative_top_six is None
                    or approximation["rows"][
                        cycle_worst_significant_negative_top_six][
                            "mode_rows"][6][
                                "absolute_residual_to_abs_deviation_ratio"]
                    > approximation["rows"][
                        worst_significant_negative_top_six][
                            "mode_rows"][6][
                                "absolute_residual_to_abs_deviation_ratio"]):
                worst_significant_negative_top_six = (
                    cycle_worst_significant_negative_top_six)
        cycle_worst_top_four_principal_residual = max(
            cycle_targets,
            key=lambda target: abs(approximation["rows"][target][
                "mode_rows"][4]["residual_to_principal_ratio"]))
        if (worst_top_four_principal_residual is None
                or abs(approximation["rows"][
                    cycle_worst_top_four_principal_residual]["mode_rows"][4][
                        "residual_to_principal_ratio"])
                > abs(approximation["rows"][
                    worst_top_four_principal_residual]["mode_rows"][4][
                        "residual_to_principal_ratio"])):
            worst_top_four_principal_residual = (
                cycle_worst_top_four_principal_residual)
        cycle_worst_top_six_principal_residual = max(
            cycle_targets,
            key=lambda target: abs(approximation["rows"][target][
                "mode_rows"][6]["residual_to_principal_ratio"]))
        if (worst_top_six_principal_residual is None
                or abs(approximation["rows"][
                    cycle_worst_top_six_principal_residual]["mode_rows"][6][
                        "residual_to_principal_ratio"])
                > abs(approximation["rows"][
                    worst_top_six_principal_residual]["mode_rows"][6][
                        "residual_to_principal_ratio"])):
            worst_top_six_principal_residual = (
                cycle_worst_top_six_principal_residual)
        cycle_worst_all_top_four = max(
            cycle_targets,
            key=lambda target: approximation["rows"][target][
                "mode_rows"][4]["absolute_residual_to_abs_deviation_ratio"])
        if (worst_all_top_four is None
                or approximation["rows"][cycle_worst_all_top_four][
                    "mode_rows"][4][
                        "absolute_residual_to_abs_deviation_ratio"]
                > approximation["rows"][worst_all_top_four]["mode_rows"][4][
                    "absolute_residual_to_abs_deviation_ratio"]):
            worst_all_top_four = cycle_worst_all_top_four
        cycle_rows[cycle] = {
            "target_range": (cycle_targets[0], cycle_targets[-1]),
            "tested_target_count": len(cycle_targets),
            "negative_q286_deviation_count": len(negative_targets),
            "significant_negative_q286_deviation_count": len(
                significant_negative_targets),
            "nonnegative_q286_deviation_count": len(nonnegative_targets),
            "minimum_q286_deviation_target": min(
                cycle_targets,
                key=lambda target: approximation["rows"][target][
                    "deviation_to_principal_ratio"]),
            "minimum_q286_deviation_ratio": min(
                approximation["rows"][target][
                    "deviation_to_principal_ratio"]
                for target in cycle_targets),
            "worst_negative_top_four_residual_target": (
                cycle_worst_negative_top_four if negative_targets else None),
            "worst_negative_top_four_residual_fraction": (
                approximation["rows"][cycle_worst_negative_top_four][
                    "mode_rows"][4][
                        "absolute_residual_to_abs_deviation_ratio"]
                if negative_targets else 0.0),
            "worst_significant_negative_top_four_residual_target": (
                cycle_worst_significant_negative_top_four
                if significant_negative_targets else None),
            "worst_significant_negative_top_four_residual_fraction": (
                approximation["rows"][
                    cycle_worst_significant_negative_top_four]["mode_rows"][4][
                        "absolute_residual_to_abs_deviation_ratio"]
                if significant_negative_targets else 0.0),
            "worst_significant_negative_top_six_residual_target": (
                cycle_worst_significant_negative_top_six
                if significant_negative_targets else None),
            "worst_significant_negative_top_six_residual_fraction": (
                approximation["rows"][
                    cycle_worst_significant_negative_top_six]["mode_rows"][6][
                        "absolute_residual_to_abs_deviation_ratio"]
                if significant_negative_targets else 0.0),
            "worst_top_four_principal_residual_target": (
                cycle_worst_top_four_principal_residual),
            "worst_top_four_abs_residual_to_principal_ratio": abs(
                approximation["rows"][
                    cycle_worst_top_four_principal_residual]["mode_rows"][4][
                        "residual_to_principal_ratio"]),
            "worst_top_six_principal_residual_target": (
                cycle_worst_top_six_principal_residual),
            "worst_top_six_abs_residual_to_principal_ratio": abs(
                approximation["rows"][
                    cycle_worst_top_six_principal_residual]["mode_rows"][6][
                        "residual_to_principal_ratio"]),
            "worst_all_top_four_residual_target": (
                cycle_worst_all_top_four),
            "worst_all_top_four_residual_fraction": (
                approximation["rows"][cycle_worst_all_top_four][
                    "mode_rows"][4][
                        "absolute_residual_to_abs_deviation_ratio"]),
        }

    maximum_negative_top_four = (
        approximation["rows"][worst_negative_top_four]["mode_rows"][4][
            "absolute_residual_to_abs_deviation_ratio"]
        if worst_negative_top_four is not None else 0.0)
    maximum_negative_top_two = (
        approximation["rows"][worst_negative_top_two]["mode_rows"][2][
            "absolute_residual_to_abs_deviation_ratio"]
        if worst_negative_top_two is not None else 0.0)
    maximum_significant_negative_top_four = (
        approximation["rows"][worst_significant_negative_top_four][
            "mode_rows"][4]["absolute_residual_to_abs_deviation_ratio"]
        if worst_significant_negative_top_four is not None else 0.0)
    maximum_significant_negative_top_six = (
        approximation["rows"][worst_significant_negative_top_six][
            "mode_rows"][6]["absolute_residual_to_abs_deviation_ratio"]
        if worst_significant_negative_top_six is not None else 0.0)
    maximum_all_top_four = (
        approximation["rows"][worst_all_top_four]["mode_rows"][4][
            "absolute_residual_to_abs_deviation_ratio"])
    maximum_top_four_abs_principal_residual = abs(
        approximation["rows"][worst_top_four_principal_residual][
            "mode_rows"][4]["residual_to_principal_ratio"])
    maximum_top_six_abs_principal_residual = abs(
        approximation["rows"][worst_top_six_principal_residual][
            "mode_rows"][6]["residual_to_principal_ratio"])
    return {
        "families": approximation["families"],
        "arithmetic_period": approximation["arithmetic_period"],
        "support": approximation["support"],
        "natural_modulus": approximation["natural_modulus"],
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "significant_negative_ratio": significant_negative_ratio,
        "tested_modes": (2, 4, 6, 9),
        "tested_target_count": len(targets),
        "cycle_rows": cycle_rows,
        "negative_q286_deviation_count": len(global_negative_targets),
        "significant_negative_q286_deviation_count": len(
            global_significant_negative_targets),
        "nonnegative_q286_deviation_count": len(global_nonnegative_targets),
        "worst_negative_top_two_residual_target": worst_negative_top_two,
        "worst_negative_top_two_residual_fraction": maximum_negative_top_two,
        "worst_negative_top_four_residual_target": worst_negative_top_four,
        "worst_negative_top_four_residual_fraction": maximum_negative_top_four,
        "worst_significant_negative_top_four_residual_target": (
            worst_significant_negative_top_four),
        "worst_significant_negative_top_four_residual_fraction": (
            maximum_significant_negative_top_four),
        "worst_significant_negative_top_six_residual_target": (
            worst_significant_negative_top_six),
        "worst_significant_negative_top_six_residual_fraction": (
            maximum_significant_negative_top_six),
        "worst_all_top_four_residual_target": worst_all_top_four,
        "worst_all_top_four_residual_fraction": maximum_all_top_four,
        "worst_top_four_principal_residual_target": (
            worst_top_four_principal_residual),
        "worst_top_four_abs_residual_to_principal_ratio": (
            maximum_top_four_abs_principal_residual),
        "worst_top_six_principal_residual_target": (
            worst_top_six_principal_residual),
        "worst_top_six_abs_residual_to_principal_ratio": (
            maximum_top_six_abs_principal_residual),
        "top_four_modes_control_sampled_negative_lower_tail": bool(
            global_negative_targets and maximum_negative_top_four < .1),
        "top_four_modes_control_significant_sampled_negative_tail": bool(
            global_significant_negative_targets
            and maximum_significant_negative_top_four < .1),
        "top_six_modes_control_significant_sampled_negative_tail": bool(
            global_significant_negative_targets
            and maximum_significant_negative_top_six < .1),
        "top_four_principal_residual_under_point_one_on_sample": bool(
            maximum_top_four_abs_principal_residual < .1),
        "top_six_principal_residual_under_point_one_on_sample": bool(
            maximum_top_six_abs_principal_residual < .1),
        "top_four_modes_control_all_sampled_targets": bool(
            maximum_all_top_four < .1),
        "singular_mode_cycle_scan_measured": True,
        "signed_prime_correlation_estimate_proved": False,
        "formal_signed_error_identification_proved": False,
        "goldbach_proved": False,
    }


def combined_coefficient_character_support_receipt(tolerance=1e-9):
    """Group assembled character energy by CRT/conductor support."""
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    values = np.asarray(tuple(
        coefficient["aggregate_coefficient_by_unit_residue"][unit]
        for unit in units), dtype=np.complex128)
    centered = values - np.mean(values)
    _, labels, character_table = _unit_character_table(period, units)
    character_coefficients = (
        np.conjugate(character_table) @ centered / len(units))
    energies = np.abs(character_coefficients) ** 2
    total_energy = float(np.sum(energies))
    factor_primes = (5, 7, 11, 13)
    support_energy = {}
    size_energy = {}
    for label, energy in zip(labels, energies):
        support = tuple(
            prime for prime, exponent in zip(factor_primes, label)
            if exponent != 0)
        support_energy[support] = (
            support_energy.get(support, 0.0) + float(energy))
        size_energy[len(support)] = (
            size_energy.get(len(support), 0.0) + float(energy))
    support_rows = tuple(
        {
            "support": support,
            "energy": energy,
            "energy_fraction": energy / total_energy if total_energy else 0.0,
        }
        for support, energy in sorted(
            support_energy.items(), key=lambda item: item[1], reverse=True))
    size_rows = {
        size: {
            "energy": energy,
            "energy_fraction": energy / total_energy if total_energy else 0.0,
        }
        for size, energy in sorted(size_energy.items())}
    full_support = factor_primes
    full_support_fraction = (
        support_energy.get(full_support, 0.0) / total_energy
        if total_energy else 0.0)
    lower_support_fraction = 1.0 - full_support_fraction
    leading_support_fraction = (
        support_rows[0]["energy_fraction"] if support_rows else 0.0)
    return {
        "families": coefficient["families"],
        "arithmetic_period": period,
        "unit_group_order": len(units),
        "factor_primes": factor_primes,
        "total_character_energy": total_energy,
        "support_energy_rows": support_rows,
        "support_size_energy_rows": size_rows,
        "full_support_energy_fraction": full_support_fraction,
        "lower_support_energy_fraction": lower_support_fraction,
        "leading_support": support_rows[0]["support"] if support_rows else (),
        "leading_support_energy_fraction": leading_support_fraction,
        "full_support_dominates": bool(full_support_fraction > .5),
        "low_dimensional_support_diagnostic_passes": bool(
            lower_support_fraction > .75),
        "character_support_grouping_measured": True,
        "signed_prime_correlation_estimate_proved": False,
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


def q286_high_positive_residue_cover_receipt(
        start=10000,
        targets_per_cycle=5005,
        selected_targets=None,
        top_count=24,
        tolerance=1e-09):
    """Greedy cover of lower-tail targets by empty positive q286 residues.

    This is a diagnostic receipt, not a theorem.  It asks whether the observed
    full-action negative targets are covered by a small set of residues whose
    first-three q286 coefficient is positive but whose strict-central residue
    weight is zero/deficient among the largest negative contribution rows.
    """
    if selected_targets is None:
        negative_receipt = q286_first_three_full_negative_driver_receipt(
            start=start,
            targets_per_cycle=targets_per_cycle,
            top_count=min(8, top_count),
            tolerance=tolerance)
        targets = tuple(negative_receipt["full_negative_targets"])
        target_source = "full_negative_targets"
    else:
        negative_receipt = None
        targets = tuple(selected_targets)
        target_source = "selected_targets"

    ap_receipt = q286_first_three_ap_discrepancy_proxy_receipt(
        start=start,
        targets_per_cycle=targets_per_cycle,
        selected_targets=targets,
        top_count=top_count,
        tolerance=tolerance)

    rows = ap_receipt["rows"]
    target_candidate_residues = {}
    residue_presence_counts = {}
    residue_score_sums = {}
    residue_target_rows = {}

    for target in targets:
        candidate_residues = []
        row = rows[target]
        for residue_row in row["largest_negative_residue_rows"]:
            if residue_row["coefficient_real"] <= tolerance:
                continue
            if residue_row["weight_delta"] >= -tolerance:
                continue
            if abs(residue_row["prime_pair_weight"]) > tolerance:
                continue
            residue = residue_row["residue_mod_286"]
            candidate_residues.append(residue)
            residue_presence_counts[residue] = (
                residue_presence_counts.get(residue, 0) + 1)
            residue_score_sums[residue] = residue_score_sums.get(
                residue, 0.0) + abs(
                    residue_row["contribution_to_principal_ratio"])
            residue_target_rows.setdefault(residue, []).append((
                target,
                residue_row["contribution_to_principal_ratio"]))
        target_candidate_residues[target] = tuple(candidate_residues)

    remaining_targets = set(targets)
    greedy_cover_rows = []
    while remaining_targets:
        candidate_pool = set()
        for target in remaining_targets:
            candidate_pool.update(target_candidate_residues[target])
        if not candidate_pool:
            break
        best_residue = max(
            candidate_pool,
            key=lambda residue: (
                len({
                    target for target in remaining_targets
                    if residue in target_candidate_residues[target]
                }),
                residue_score_sums.get(residue, 0.0),
                -residue))
        hit_targets = tuple(sorted(
            target for target in remaining_targets
            if best_residue in target_candidate_residues[target]))
        greedy_cover_rows.append({
            "residue_mod_286": best_residue,
            "newly_covered_target_count": len(hit_targets),
            "newly_covered_targets": hit_targets,
            "top_negative_presence_count": residue_presence_counts[
                best_residue],
            "absolute_contribution_to_principal_ratio_sum": (
                residue_score_sums[best_residue]),
        })
        remaining_targets.difference_update(hit_targets)

    top_presence_rows = tuple(
        {
            "residue_mod_286": residue,
            "top_negative_presence_count": count,
            "absolute_contribution_to_principal_ratio_sum": (
                residue_score_sums[residue]),
        }
        for residue, count in sorted(
            residue_presence_counts.items(),
            key=lambda item: (
                -item[1],
                -residue_score_sums[item[0]],
                item[0]))
    )

    return {
        "start": start,
        "targets_per_cycle": targets_per_cycle,
        "natural_modulus": 286,
        "support": (11, 13),
        "top_count": top_count,
        "target_source": target_source,
        "tested_target_count": len(targets),
        "target_candidate_residues": target_candidate_residues,
        "top_presence_rows": top_presence_rows,
        "greedy_cover_rows": tuple(greedy_cover_rows),
        "uncovered_targets": tuple(sorted(remaining_targets)),
        "uncovered_target_count": len(remaining_targets),
        "greedy_cover_residue_count": len(greedy_cover_rows),
        "negative_receipt_used": negative_receipt is not None,
        "ap_tested_target_count": ap_receipt["tested_target_count"],
        "high_positive_residue_cover_measured": True,
        "observed_top_rows_cover_all_targets": len(remaining_targets) == 0,
        "driver_residue_hitting_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_high_positive_cover_margin_receipt(
        selected_targets,
        top_count=24,
        cover_residues=(133, 153),
        start=10000,
        targets_per_cycle=5005,
        tolerance=1e-09):
    """Measure how much cover-residue weight would flip bad targets.

    For each selected target, this compares the full assembled action ratio
    with the local slope of adding strict-central prime-pair weight in the
    selected high-positive q286 residue channels.  The output is a finite
    diagnostic only; it is not a lower-bound theorem for those channels.
    """
    targets = tuple(selected_targets)
    ap_receipt = q286_first_three_ap_discrepancy_proxy_receipt(
        start=start,
        targets_per_cycle=targets_per_cycle,
        selected_targets=targets,
        top_count=top_count,
        tolerance=tolerance)
    lower_receipt = q286_first_two_mode_lower_tail_receipt(
        start=start,
        targets_per_cycle=targets_per_cycle,
        selected_targets=targets,
        tolerance=tolerance)

    target_rows = {}
    margin_rows = []
    missing_targets = []
    for target in targets:
        ap_row = ap_receipt["rows"][target]
        lower_row = lower_receipt["rows"][target]
        full_ratio = lower_row["full_action_to_principal_ratio"]
        residue_rows = []
        for residue_row in ap_row["largest_negative_residue_rows"]:
            residue = residue_row["residue_mod_286"]
            if residue not in cover_residues:
                continue
            if residue_row["coefficient_real"] <= tolerance:
                continue
            if residue_row["weight_delta"] >= -tolerance:
                continue
            slope = (
                residue_row["contribution_to_principal_ratio"]
                / residue_row["weight_delta"])
            required_full_weight = (
                max(0.0, -full_ratio / slope)
                if slope > tolerance else None)
            required_first_three_weight = (
                max(
                    0.0,
                    -ap_row["first_three_mode_to_principal_ratio"] / slope)
                if slope > tolerance else None)
            out_row = {
                "target": target,
                "residue_mod_286": residue,
                "prime_pair_weight": residue_row["prime_pair_weight"],
                "weight_delta": residue_row["weight_delta"],
                "coefficient_to_principal_weight_slope": slope,
                "full_action_to_principal_ratio": full_ratio,
                "first_three_mode_to_principal_ratio": (
                    ap_row["first_three_mode_to_principal_ratio"]),
                "required_weight_to_flip_full_action": (
                    required_full_weight),
                "required_weight_to_cancel_first_three": (
                    required_first_three_weight),
            }
            residue_rows.append(out_row)
            margin_rows.append(out_row)
        if not residue_rows:
            missing_targets.append(target)
        target_rows[target] = {
            "full_action_to_principal_ratio": full_ratio,
            "cover_residue_rows": tuple(residue_rows),
            "minimum_required_weight_to_flip_full_action": (
                min(
                    row["required_weight_to_flip_full_action"]
                    for row in residue_rows
                    if row["required_weight_to_flip_full_action"] is not None)
                if residue_rows else None),
        }

    finite_full_rows = tuple(
        row for row in margin_rows
        if row["required_weight_to_flip_full_action"] is not None)
    finite_first_three_rows = tuple(
        row for row in margin_rows
        if row["required_weight_to_cancel_first_three"] is not None)
    worst_full_row = (
        max(
            finite_full_rows,
            key=lambda row: row["required_weight_to_flip_full_action"])
        if finite_full_rows else None)
    worst_first_three_row = (
        max(
            finite_first_three_rows,
            key=lambda row: row["required_weight_to_cancel_first_three"])
        if finite_first_three_rows else None)
    min_target_requirements = tuple(
        row["minimum_required_weight_to_flip_full_action"]
        for row in target_rows.values()
        if row["minimum_required_weight_to_flip_full_action"] is not None)

    return {
        "start": start,
        "targets_per_cycle": targets_per_cycle,
        "natural_modulus": 286,
        "support": (11, 13),
        "top_count": top_count,
        "cover_residues": tuple(cover_residues),
        "tested_target_count": len(targets),
        "margin_row_count": len(margin_rows),
        "target_rows": target_rows,
        "margin_rows": tuple(margin_rows),
        "missing_target_count": len(missing_targets),
        "missing_targets": tuple(missing_targets),
        "maximum_required_weight_to_flip_full_action": (
            worst_full_row["required_weight_to_flip_full_action"]
            if worst_full_row else None),
        "worst_required_weight_to_flip_full_action_row": worst_full_row,
        "maximum_required_weight_to_cancel_first_three": (
            worst_first_three_row["required_weight_to_cancel_first_three"]
            if worst_first_three_row else None),
        "worst_required_weight_to_cancel_first_three_row": (
            worst_first_three_row),
        "maximum_target_minimum_required_weight_to_flip_full_action": (
            max(min_target_requirements) if min_target_requirements else None),
        "high_positive_cover_margin_measured": True,
        "cover_residue_occupancy_lower_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_cover_pair_compensation_portfolio_receipt(
        selected_targets=(25036, 25306, 25372, 25582, 26002, 26722),
        top_count=24,
        tolerance=1e-09):
    """Profile compensation when the q286 cover pair remains empty.

    The default targets are the observed positive full-action lift-1 cases from
    q286_driver_residue_lift_occupancy_receipt(lifts=(0, 1, 2)) where cover
    residues 133 and 153 remain admissible-empty.  The receipt measures whether
    top positive first-three q286 residue rows form a small portfolio, and how
    much positivity is supplied outside the first-three modes.
    """
    targets = tuple(selected_targets)
    ap_receipt = q286_first_three_ap_discrepancy_proxy_receipt(
        selected_targets=targets,
        top_count=top_count,
        tolerance=tolerance)
    lower_receipt = q286_first_two_mode_lower_tail_receipt(
        selected_targets=targets,
        targets_per_cycle=5005,
        tolerance=tolerance)

    target_positive_residues = {}
    positive_presence_counts = {}
    positive_direction_counts = {}
    positive_score_sums = {}
    target_rows = {}
    for target in targets:
        ap_row = ap_receipt["rows"][target]
        lower_row = lower_receipt["rows"][target]
        positive_residues = []
        positive_rows = []
        for residue_row in ap_row["largest_positive_residue_rows"]:
            if residue_row["contribution_to_principal_ratio"] <= tolerance:
                continue
            residue = residue_row["residue_mod_286"]
            positive_residues.append(residue)
            positive_presence_counts[residue] = (
                positive_presence_counts.get(residue, 0) + 1)
            positive_score_sums[residue] = positive_score_sums.get(
                residue, 0.0) + residue_row[
                    "contribution_to_principal_ratio"]
            positive_rows.append({
                "residue_mod_286": residue,
                "coefficient_real": residue_row["coefficient_real"],
                "weight_delta": residue_row["weight_delta"],
                "relative_weight_delta": residue_row[
                    "relative_weight_delta"],
                "contribution_to_principal_ratio": residue_row[
                    "contribution_to_principal_ratio"],
                "prime_pair_weight": residue_row["prime_pair_weight"],
            })
        target_positive_residues[target] = tuple(positive_residues)
        target_rows[target] = {
            "full_action_to_principal_ratio": lower_row[
                "full_action_to_principal_ratio"],
            "first_three_modes_to_principal_ratio": lower_row[
                "first_three_modes_to_principal_ratio"],
            "full_without_first_three_to_principal_ratio": lower_row[
                "full_without_first_three_to_principal_ratio"],
            "reduced_without_first_three_to_principal_ratio": lower_row[
                "reduced_without_first_three_to_principal_ratio"],
            "positive_real_contribution_to_principal_ratio": ap_row[
                "positive_real_contribution_to_principal_ratio"],
            "negative_real_contribution_to_principal_ratio": ap_row[
                "negative_real_contribution_to_principal_ratio"],
            "top_positive_residue_rows": tuple(positive_rows),
        }

    remaining_targets = set(targets)
    greedy_rows = []
    while remaining_targets:
        candidates = set()
        for target in remaining_targets:
            candidates.update(target_positive_residues[target])
        if not candidates:
            break
        best_residue = max(
            candidates,
            key=lambda residue: (
                len({
                    target for target in remaining_targets
                    if residue in target_positive_residues[target]
                }),
                positive_score_sums.get(residue, 0.0),
                -residue))
        hit_targets = tuple(sorted(
            target for target in remaining_targets
            if best_residue in target_positive_residues[target]))
        greedy_rows.append({
            "residue_mod_286": best_residue,
            "newly_covered_target_count": len(hit_targets),
            "newly_covered_targets": hit_targets,
            "top_positive_presence_count": positive_presence_counts[
                best_residue],
            "positive_contribution_to_principal_ratio_sum": (
                positive_score_sums[best_residue]),
        })
        remaining_targets.difference_update(hit_targets)

    top_presence_rows = tuple(
        {
            "residue_mod_286": residue,
            "top_positive_presence_count": count,
            "positive_contribution_to_principal_ratio_sum": (
                positive_score_sums[residue]),
        }
        for residue, count in sorted(
            positive_presence_counts.items(),
            key=lambda item: (
                -item[1],
                -positive_score_sums[item[0]],
                item[0]))
    )
    without_first_three_values = tuple(
        row["full_without_first_three_to_principal_ratio"]
        for row in target_rows.values())
    first_three_values = tuple(
        row["first_three_modes_to_principal_ratio"]
        for row in target_rows.values())

    return {
        "natural_modulus": 286,
        "support": (11, 13),
        "tested_target_count": len(targets),
        "top_count": top_count,
        "target_rows": target_rows,
        "top_positive_presence_rows": top_presence_rows,
        "greedy_positive_portfolio_rows": tuple(greedy_rows),
        "uncovered_targets": tuple(sorted(remaining_targets)),
        "uncovered_target_count": len(remaining_targets),
        "greedy_positive_portfolio_residue_count": len(greedy_rows),
        "minimum_full_without_first_three_to_principal_ratio": (
            min(without_first_three_values)
            if without_first_three_values else None),
        "maximum_full_without_first_three_to_principal_ratio": (
            max(without_first_three_values)
            if without_first_three_values else None),
        "maximum_first_three_modes_to_principal_ratio": (
            max(first_three_values) if first_three_values else None),
        "all_first_three_modes_negative": all(
            value < -tolerance for value in first_three_values),
        "compensation_portfolio_measured": True,
        "single_positive_residue_portfolio_observed": (
            len(greedy_rows) == 1 and len(remaining_targets) == 0),
        "compensation_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_positive_both_empty_compensation_cover_receipt(
        start=10000,
        targets_per_cycle=5005,
        selected_targets=None,
        top_count=24,
        driver_residues=(133, 153),
        tolerance=1e-09):
    """Cover positive targets where the q286 cover pair remains empty.

    With selected_targets omitted, this scans one full q286 arithmetic period
    for targets whose full action is positive while all driver residues are
    locally admissible but empty.  It then greedily covers those targets by top
    positive first-three q286 residue contribution rows.  This is finite
    evidence for compensation structure, not a proof of compensation.
    """
    if selected_targets is None:
        period_targets = tuple(
            range(start, start + 2 * targets_per_cycle, 2))
        occupancy_receipt = q286_driver_residue_lift_occupancy_receipt(
            base_targets=period_targets,
            start=start,
            targets_per_cycle=targets_per_cycle,
            lifts=(0,),
            driver_residues=driver_residues,
            tolerance=tolerance)
        targets = tuple(
            row[2]
            for row in occupancy_receipt[
                "positive_with_all_driver_residues_empty_rows"])
        negative_both_empty_count = occupancy_receipt[
            "negative_with_all_driver_residues_empty_count"]
        target_source = "positive_with_all_driver_residues_empty_rows"
    else:
        occupancy_receipt = None
        targets = tuple(selected_targets)
        negative_both_empty_count = None
        target_source = "selected_targets"

    ap_receipt = q286_first_three_ap_discrepancy_proxy_receipt(
        start=start,
        targets_per_cycle=targets_per_cycle,
        selected_targets=targets,
        top_count=top_count,
        tolerance=tolerance)

    target_positive_residues = {}
    positive_presence_counts = {}
    positive_direction_counts = {}
    positive_score_sums = {}
    target_rows = {}
    for target in targets:
        ap_row = ap_receipt["rows"][target]
        residue_rows = []
        residues = []
        for residue_row in ap_row["largest_positive_residue_rows"]:
            if residue_row["contribution_to_principal_ratio"] <= tolerance:
                continue
            residue = residue_row["residue_mod_286"]
            residues.append(residue)
            positive_presence_counts[residue] = (
                positive_presence_counts.get(residue, 0) + 1)
            direction_counts = positive_direction_counts.setdefault(
                residue,
                {
                    "negative_coefficient_deficit_count": 0,
                    "positive_coefficient_surplus_count": 0,
                    "other_positive_contribution_count": 0,
                    "zero_prime_pair_weight_count": 0,
                    "positive_prime_pair_weight_count": 0,
                })
            if (residue_row["coefficient_real"] < -tolerance
                    and residue_row["weight_delta"] < -tolerance):
                direction_counts[
                    "negative_coefficient_deficit_count"] += 1
            elif (residue_row["coefficient_real"] > tolerance
                  and residue_row["weight_delta"] > tolerance):
                direction_counts[
                    "positive_coefficient_surplus_count"] += 1
            else:
                direction_counts["other_positive_contribution_count"] += 1
            if abs(residue_row["prime_pair_weight"]) <= tolerance:
                direction_counts["zero_prime_pair_weight_count"] += 1
            else:
                direction_counts["positive_prime_pair_weight_count"] += 1
            positive_score_sums[residue] = positive_score_sums.get(
                residue, 0.0) + residue_row[
                    "contribution_to_principal_ratio"]
            residue_rows.append({
                "residue_mod_286": residue,
                "coefficient_real": residue_row["coefficient_real"],
                "weight_delta": residue_row["weight_delta"],
                "relative_weight_delta": residue_row[
                    "relative_weight_delta"],
                "contribution_to_principal_ratio": residue_row[
                    "contribution_to_principal_ratio"],
                "prime_pair_weight": residue_row["prime_pair_weight"],
            })
        target_positive_residues[target] = tuple(residues)
        target_rows[target] = {
            "first_three_mode_to_principal_ratio": ap_row[
                "first_three_mode_to_principal_ratio"],
            "positive_real_contribution_to_principal_ratio": ap_row[
                "positive_real_contribution_to_principal_ratio"],
            "negative_real_contribution_to_principal_ratio": ap_row[
                "negative_real_contribution_to_principal_ratio"],
            "top_positive_residue_rows": tuple(residue_rows),
        }

    remaining_targets = set(targets)
    greedy_rows = []
    while remaining_targets:
        candidates = set()
        for target in remaining_targets:
            candidates.update(target_positive_residues[target])
        if not candidates:
            break
        best_residue = max(
            candidates,
            key=lambda residue: (
                len({
                    target for target in remaining_targets
                    if residue in target_positive_residues[target]
                }),
                positive_score_sums.get(residue, 0.0),
                -residue))
        hit_targets = tuple(sorted(
            target for target in remaining_targets
            if best_residue in target_positive_residues[target]))
        greedy_rows.append({
            "residue_mod_286": best_residue,
            "newly_covered_target_count": len(hit_targets),
            "newly_covered_targets": hit_targets,
            "top_positive_presence_count": positive_presence_counts[
                best_residue],
            "positive_contribution_to_principal_ratio_sum": (
                positive_score_sums[best_residue]),
        })
        remaining_targets.difference_update(hit_targets)

    top_presence_rows = tuple(
        {
            "residue_mod_286": residue,
            "top_positive_presence_count": count,
            **positive_direction_counts[residue],
            "positive_contribution_to_principal_ratio_sum": (
                positive_score_sums[residue]),
        }
        for residue, count in sorted(
            positive_presence_counts.items(),
            key=lambda item: (
                -item[1],
                -positive_score_sums[item[0]],
                item[0]))
    )

    return {
        "start": start,
        "targets_per_cycle": targets_per_cycle,
        "natural_modulus": 286,
        "support": (11, 13),
        "driver_residues": tuple(driver_residues),
        "top_count": top_count,
        "target_source": target_source,
        "tested_target_count": len(targets),
        "negative_both_empty_count": negative_both_empty_count,
        "target_rows": target_rows,
        "top_positive_presence_rows": top_presence_rows,
        "greedy_positive_portfolio_rows": tuple(greedy_rows),
        "uncovered_targets": tuple(sorted(remaining_targets)),
        "uncovered_target_count": len(remaining_targets),
        "greedy_positive_portfolio_residue_count": len(greedy_rows),
        "occupancy_receipt_used": occupancy_receipt is not None,
        "ap_tested_target_count": ap_receipt["tested_target_count"],
        "positive_both_empty_compensation_cover_measured": True,
        "single_compensator_proved": False,
        "compensation_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_residue_portfolio_local_admissibility_receipt(
        portfolios=None):
    """Exact local admissibility audit for q286 residue portfolios."""
    from math import gcd
    if portfolios is None:
        portfolios = {
            "cover_pair": (133, 153),
            "six_case_marker": (263,),
            "broad_positive_portfolio": (179, 29, 167, 241, 109),
            "combined_cover_and_positive_portfolio": (
                133, 153, 179, 29, 167, 241, 109),
        }
    portfolio_rows = {}
    for name, residues in portfolios.items():
        residues = tuple(residues)
        all_inadmissible_classes = []
        all_admissible_count = 0
        at_least_one_admissible_count = 0
        for target_class in range(143):
            admissible_flags = tuple(
                gcd(target_class - residue, 143) == 1
                for residue in residues)
            if all(admissible_flags):
                all_admissible_count += 1
            if any(admissible_flags):
                at_least_one_admissible_count += 1
            else:
                all_inadmissible_classes.append(target_class)
        portfolio_rows[name] = {
            "residues": residues,
            "residue_mod_11_13_rows": tuple(
                {
                    "residue_mod_286": residue,
                    "mod_11": residue % 11,
                    "mod_13": residue % 13,
                }
                for residue in residues),
            "all_admissible_class_count": all_admissible_count,
            "at_least_one_admissible_class_count": (
                at_least_one_admissible_count),
            "all_inadmissible_class_count": len(
                all_inadmissible_classes),
            "all_inadmissible_classes_mod_143": tuple(
                all_inadmissible_classes),
        }
    return {
        "natural_modulus": 286,
        "target_class_modulus": 143,
        "portfolio_rows": portfolio_rows,
        "residue_portfolio_local_admissibility_measured": True,
        "prime_pair_occupancy_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_positive_both_empty_compensation_min_cover_receipt(
        top_count=24,
        max_cover_size=5,
        selected_targets=None,
        start=10000,
        targets_per_cycle=5005,
        driver_residues=(133, 153),
        max_examples=10,
        tolerance=1e-09):
    """Exact set-cover search for positive both-empty compensation rows."""
    from itertools import combinations
    base_receipt = q286_positive_both_empty_compensation_cover_receipt(
        start=start,
        targets_per_cycle=targets_per_cycle,
        selected_targets=selected_targets,
        top_count=top_count,
        driver_residues=driver_residues,
        tolerance=tolerance)
    targets = tuple(base_receipt["target_rows"])
    target_index = {target: index for index, target in enumerate(targets)}
    residue_bitsets = {}
    residue_score_sums = {}
    for target, row in base_receipt["target_rows"].items():
        bit = 1 << target_index[target]
        for residue_row in row["top_positive_residue_rows"]:
            residue = residue_row["residue_mod_286"]
            residue_bitsets[residue] = residue_bitsets.get(residue, 0) | bit
            residue_score_sums[residue] = residue_score_sums.get(
                residue, 0.0) + residue_row[
                    "contribution_to_principal_ratio"]

    full_cover = (1 << len(targets)) - 1
    candidate_residues = tuple(sorted(
        residue_bitsets,
        key=lambda residue: (
            -residue_bitsets[residue].bit_count(),
            -residue_score_sums[residue],
            residue)))
    exact_search_rows = []
    minimum_cover_size = None
    minimum_cover_examples = ()
    for cover_size in range(1, max_cover_size + 1):
        checked_count = 0
        examples = []
        for combo in combinations(candidate_residues, cover_size):
            checked_count += 1
            covered = 0
            for residue in combo:
                covered |= residue_bitsets[residue]
            if covered == full_cover:
                examples.append(combo)
                if len(examples) >= max_examples:
                    break
        exact_search_rows.append({
            "cover_size": cover_size,
            "checked_combination_count": checked_count,
            "found_cover_prefix_count": len(examples),
            "cover_examples": tuple(examples),
        })
        if examples:
            minimum_cover_size = cover_size
            minimum_cover_examples = tuple(examples)
            break

    return {
        "start": start,
        "targets_per_cycle": targets_per_cycle,
        "natural_modulus": 286,
        "support": (11, 13),
        "driver_residues": tuple(driver_residues),
        "top_count": top_count,
        "tested_target_count": len(targets),
        "candidate_residue_count": len(candidate_residues),
        "candidate_residues": candidate_residues,
        "greedy_positive_portfolio_rows": base_receipt[
            "greedy_positive_portfolio_rows"],
        "exact_search_rows": tuple(exact_search_rows),
        "minimum_observed_cover_size": minimum_cover_size,
        "minimum_observed_cover_examples": minimum_cover_examples,
        "max_cover_size_searched": max_cover_size,
        "minimum_cover_proved_up_to_max_size": (
            minimum_cover_size is not None),
        "observed_set_cover_measured": True,
        "compensation_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_positive_both_empty_remainder_compensation_receipt(
        selected_targets=None,
        start=10000,
        targets_per_cycle=5005,
        top_count=24,
        driver_residues=(133, 153),
        tolerance=1e-09):
    """Measure remainder compensation for positive both-empty targets."""
    if selected_targets is None:
        cover_receipt = q286_positive_both_empty_compensation_cover_receipt(
            start=start,
            targets_per_cycle=targets_per_cycle,
            selected_targets=None,
            top_count=top_count,
            driver_residues=driver_residues,
            tolerance=tolerance)
        targets = tuple(cover_receipt["target_rows"])
        target_source = "positive_both_empty_default_receipt"
    else:
        cover_receipt = None
        targets = tuple(selected_targets)
        target_source = "selected_targets"

    lower_receipt = q286_first_two_mode_lower_tail_receipt(
        start=start,
        targets_per_cycle=targets_per_cycle,
        selected_targets=targets,
        tolerance=tolerance)

    target_rows = {}
    first_three_values = []
    without_first_three_values = []
    full_values = []
    for target in targets:
        row = lower_receipt["rows"][target]
        first_three = row["first_three_modes_to_principal_ratio"]
        without_first_three = row[
            "full_without_first_three_to_principal_ratio"]
        full_ratio = row["full_action_to_principal_ratio"]
        first_three_values.append(first_three)
        without_first_three_values.append(without_first_three)
        full_values.append(full_ratio)
        target_rows[target] = {
            "full_action_to_principal_ratio": full_ratio,
            "first_three_modes_to_principal_ratio": first_three,
            "full_without_first_three_to_principal_ratio": (
                without_first_three),
            "first_three_negative": first_three < -tolerance,
            "full_without_first_three_positive": (
                without_first_three > tolerance),
        }

    return {
        "start": start,
        "targets_per_cycle": targets_per_cycle,
        "natural_modulus": 286,
        "support": (11, 13),
        "driver_residues": tuple(driver_residues),
        "target_source": target_source,
        "tested_target_count": len(targets),
        "target_rows": target_rows,
        "first_three_negative_count": sum(
            1 for value in first_three_values if value < -tolerance),
        "first_three_positive_count": sum(
            1 for value in first_three_values if value > tolerance),
        "full_without_first_three_positive_count": sum(
            1 for value in without_first_three_values
            if value > tolerance),
        "minimum_first_three_modes_to_principal_ratio": (
            min(first_three_values) if first_three_values else None),
        "maximum_first_three_modes_to_principal_ratio": (
            max(first_three_values) if first_three_values else None),
        "minimum_full_without_first_three_to_principal_ratio": (
            min(without_first_three_values)
            if without_first_three_values else None),
        "maximum_full_without_first_three_to_principal_ratio": (
            max(without_first_three_values)
            if without_first_three_values else None),
        "minimum_full_action_to_principal_ratio": (
            min(full_values) if full_values else None),
        "maximum_full_action_to_principal_ratio": (
            max(full_values) if full_values else None),
        "cover_receipt_used": cover_receipt is not None,
        "remainder_compensation_measured": True,
        "remainder_compensation_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_to_complement_ratio_receipt(
        start=10000,
        cycle_count=8,
        targets_per_cycle=5005,
        selected_targets=None,
        tolerance=1e-09):
    """Measure the first-three q286 tail against its positive complement."""
    lower_receipt = q286_first_two_mode_lower_tail_receipt(
        start=start,
        cycle_count=cycle_count,
        targets_per_cycle=targets_per_cycle,
        selected_targets=selected_targets,
        tolerance=tolerance)
    ratio_rows = []
    target_rows = {}
    for target, row in lower_receipt["rows"].items():
        complement = row["full_without_first_three_to_principal_ratio"]
        first_three = row["first_three_modes_to_principal_ratio"]
        if complement > tolerance and first_three < -tolerance:
            ratio = -first_three / complement
        else:
            ratio = 0.0
        out_row = {
            "target": target,
            "cycle": row["cycle"],
            "tail_to_complement_ratio": ratio,
            "full_action_to_principal_ratio": row[
                "full_action_to_principal_ratio"],
            "first_three_modes_to_principal_ratio": first_three,
            "full_without_first_three_to_principal_ratio": complement,
            "reduced_without_first_three_to_principal_ratio": row[
                "reduced_without_first_three_to_principal_ratio"],
        }
        ratio_rows.append(out_row)
        target_rows[target] = out_row
    sorted_ratio_rows = tuple(sorted(
        ratio_rows,
        key=lambda item: item["tail_to_complement_ratio"],
        reverse=True))
    return {
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "natural_modulus": 286,
        "support": (11, 13),
        "tested_target_count": len(ratio_rows),
        "target_rows": target_rows,
        "top_tail_to_complement_rows": sorted_ratio_rows[:20],
        "maximum_tail_to_complement_ratio": (
            sorted_ratio_rows[0]["tail_to_complement_ratio"]
            if sorted_ratio_rows else None),
        "worst_tail_to_complement_target": (
            sorted_ratio_rows[0]["target"] if sorted_ratio_rows else None),
        "ratio_greater_than_one_count": sum(
            1 for row in ratio_rows
            if row["tail_to_complement_ratio"] > 1.0 + tolerance),
        "ratio_greater_than_point_nine_count": sum(
            1 for row in ratio_rows
            if row["tail_to_complement_ratio"] > 0.9 + tolerance),
        "ratio_greater_than_point_five_count": sum(
            1 for row in ratio_rows
            if row["tail_to_complement_ratio"] > 0.5 + tolerance),
        "full_action_negative_count": sum(
            1 for row in ratio_rows
            if row["full_action_to_principal_ratio"] <= tolerance),
        "first_three_to_complement_ratio_measured": True,
        "relative_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_tail_complement_lift_profile_receipt(
        bases=(14138, 16388, 10424, 15026, 17522),
        lifts=tuple(range(8)),
        period=10010,
        tolerance=1e-09):
    """Profile tail/complement ratios under arithmetic-period lifts."""
    bases = tuple(bases)
    lifts = tuple(lifts)
    targets = tuple(base + period * lift for base in bases for lift in lifts)
    ratio_receipt = q286_first_three_to_complement_ratio_receipt(
        selected_targets=targets,
        tolerance=tolerance)
    base_rows = {}
    gt_one_count = 0
    gt_point_nine_count = 0
    for base in bases:
        lift_rows = []
        for lift in lifts:
            target = base + period * lift
            row = ratio_receipt["target_rows"][target]
            tail_ratio = row["tail_to_complement_ratio"]
            if tail_ratio > 1.0 + tolerance:
                gt_one_count += 1
            if tail_ratio > 0.9 + tolerance:
                gt_point_nine_count += 1
            lift_rows.append({
                "lift": lift,
                "target": target,
                "tail_to_complement_ratio": tail_ratio,
                "full_action_to_principal_ratio": row[
                    "full_action_to_principal_ratio"],
                "first_three_modes_to_principal_ratio": row[
                    "first_three_modes_to_principal_ratio"],
                "full_without_first_three_to_principal_ratio": row[
                    "full_without_first_three_to_principal_ratio"],
            })
        base_rows[base] = {
            "lift_rows": tuple(lift_rows),
            "ratio_greater_than_one_lifts": tuple(
                row["lift"] for row in lift_rows
                if row["tail_to_complement_ratio"] > 1.0 + tolerance),
            "maximum_tail_to_complement_ratio": max(
                row["tail_to_complement_ratio"] for row in lift_rows),
        }
    return {
        "bases": bases,
        "lifts": lifts,
        "period": period,
        "tested_target_count": len(targets),
        "base_rows": base_rows,
        "ratio_greater_than_one_count": gt_one_count,
        "ratio_greater_than_point_nine_count": gt_point_nine_count,
        "maximum_tail_to_complement_ratio": ratio_receipt[
            "maximum_tail_to_complement_ratio"],
        "worst_tail_to_complement_target": ratio_receipt[
            "worst_tail_to_complement_target"],
        "tail_complement_lift_profile_measured": True,
        "persistent_bad_residue_class_proved": False,
        "relative_tail_bound_proved": False,
        "goldbach_proved": False,
    }


def q286_boundary_layer_clearance_receipt(
        bases=(14138, 16388, 10424, 15026, 17522),
        lifts=(0, 1),
        period=10010,
        top_count=8,
        tolerance=1e-09):
    """Compare hard q286 boundary-layer bases before and after lifting."""
    bases = tuple(bases)
    lifts = tuple(lifts)
    targets = tuple(base + period * lift for base in bases for lift in lifts)
    profile_receipt = q286_tail_complement_lift_profile_receipt(
        bases=bases,
        lifts=lifts,
        period=period,
        tolerance=tolerance)
    occupancy_receipt = q286_driver_residue_lift_occupancy_receipt(
        base_targets=bases,
        lifts=lifts,
        tolerance=tolerance)
    ap_receipt = q286_first_three_ap_discrepancy_proxy_receipt(
        selected_targets=targets,
        top_count=top_count,
        tolerance=tolerance)

    base_rows = {}
    cleared_by_lift_one_count = 0
    lift_one_driver_any_positive_count = 0
    lift_one_driver_all_empty_count = 0
    lift_one_complement_positive_count = 0
    for base in bases:
        lift_rows = []
        for lift in lifts:
            target = base + period * lift
            profile_row = next(
                row for row in profile_receipt[
                    "base_rows"][base]["lift_rows"]
                if row["lift"] == lift)
            occupancy_row = occupancy_receipt["target_rows"][base][lift]
            ap_row = ap_receipt["rows"][target]
            lift_rows.append({
                "lift": lift,
                "target": target,
                "tail_to_complement_ratio": profile_row[
                    "tail_to_complement_ratio"],
                "full_action_to_principal_ratio": profile_row[
                    "full_action_to_principal_ratio"],
                "first_three_modes_to_principal_ratio": profile_row[
                    "first_three_modes_to_principal_ratio"],
                "full_without_first_three_to_principal_ratio": profile_row[
                    "full_without_first_three_to_principal_ratio"],
                "driver_any_positive": occupancy_row[
                    "any_driver_residue_positive"],
                "driver_all_positive": occupancy_row[
                    "all_driver_residues_positive"],
                "driver_all_admissible_empty": occupancy_row[
                    "all_driver_residues_admissible_empty"],
                "total_prime_pair_weight": ap_row[
                    "total_prime_pair_weight"],
                "mean_admissible_residue_weight": ap_row[
                    "mean_admissible_residue_weight"],
                "admissible_residue_count": ap_row[
                    "admissible_residue_count"],
            })
        lift_zero = lift_rows[0]
        lift_one = lift_rows[1] if len(lift_rows) > 1 else None
        if (lift_one is not None
                and lift_zero["tail_to_complement_ratio"] > 1.0
                and lift_one["tail_to_complement_ratio"] <= 1.0):
            cleared_by_lift_one_count += 1
        if lift_one is not None and lift_one["driver_any_positive"]:
            lift_one_driver_any_positive_count += 1
        if (lift_one is not None
                and lift_one["driver_all_admissible_empty"]):
            lift_one_driver_all_empty_count += 1
        if (lift_one is not None and lift_one[
                "full_without_first_three_to_principal_ratio"] > tolerance):
            lift_one_complement_positive_count += 1
        base_rows[base] = {
            "lift_rows": tuple(lift_rows),
            "ratio_clears_by_lift_one": (
                lift_one is not None
                and lift_zero["tail_to_complement_ratio"] > 1.0
                and lift_one["tail_to_complement_ratio"] <= 1.0),
            "complement_growth_lift_zero_to_one": (
                lift_one[
                    "full_without_first_three_to_principal_ratio"]
                - lift_zero[
                    "full_without_first_three_to_principal_ratio"]
                if lift_one is not None else None),
            "mean_weight_growth_lift_zero_to_one": (
                lift_one["mean_admissible_residue_weight"]
                - lift_zero["mean_admissible_residue_weight"]
                if lift_one is not None else None),
        }

    return {
        "bases": bases,
        "lifts": lifts,
        "period": period,
        "tested_target_count": len(targets),
        "base_rows": base_rows,
        "cleared_by_lift_one_count": cleared_by_lift_one_count,
        "lift_one_driver_any_positive_count": (
            lift_one_driver_any_positive_count),
        "lift_one_driver_all_admissible_empty_count": (
            lift_one_driver_all_empty_count),
        "lift_one_complement_positive_count": (
            lift_one_complement_positive_count),
        "boundary_layer_clearance_measured": True,
        "driver_occupancy_explains_all_clearance": False,
        "monotone_lift_growth_theorem_proved": False,
        "goldbach_proved": False,
    }


def q286_complement_cycle_envelope_receipt(
        start=10000,
        cycle_count=8,
        targets_per_cycle=5005,
        tolerance=1e-09):
    """Summarize q286 complement lower envelope by arithmetic-period cycle."""
    lower_receipt = q286_first_two_mode_lower_tail_receipt(
        start=start,
        cycle_count=cycle_count,
        targets_per_cycle=targets_per_cycle,
        tolerance=tolerance)
    by_cycle = {}
    for target, row in lower_receipt["rows"].items():
        by_cycle.setdefault(row["cycle"], []).append((target, row))

    cycle_rows = []
    after_first_cycle_min_rows = []
    for cycle in sorted(by_cycle):
        entries = by_cycle[cycle]
        min_complement_target, min_complement_row = min(
            entries,
            key=lambda item: item[1][
                "full_without_first_three_to_principal_ratio"])
        min_reduced_target, min_reduced_row = min(
            entries,
            key=lambda item: item[1][
                "reduced_without_first_three_to_principal_ratio"])
        min_full_target, min_full_row = min(
            entries,
            key=lambda item: item[1]["full_action_to_principal_ratio"])
        out_row = {
            "cycle": cycle,
            "target_count": len(entries),
            "full_action_negative_count": sum(
                1 for _, row in entries
                if row["full_action_to_principal_ratio"] <= tolerance),
            "full_without_first_three_nonpositive_count": sum(
                1 for _, row in entries
                if row[
                    "full_without_first_three_to_principal_ratio"]
                <= tolerance),
            "minimum_full_without_first_three_target": (
                min_complement_target),
            "minimum_full_without_first_three_to_principal_ratio": (
                min_complement_row[
                    "full_without_first_three_to_principal_ratio"]),
            "minimum_reduced_without_first_three_target": min_reduced_target,
            "minimum_reduced_without_first_three_to_principal_ratio": (
                min_reduced_row[
                    "reduced_without_first_three_to_principal_ratio"]),
            "minimum_full_action_target": min_full_target,
            "minimum_full_action_to_principal_ratio": (
                min_full_row["full_action_to_principal_ratio"]),
            "first_three_at_minimum_complement_to_principal_ratio": (
                min_complement_row[
                    "first_three_modes_to_principal_ratio"]),
        }
        cycle_rows.append(out_row)
        if cycle > 0:
            after_first_cycle_min_rows.append(out_row)

    global_min_row = min(
        cycle_rows,
        key=lambda row: row[
            "minimum_full_without_first_three_to_principal_ratio"])
    after_first_min_row = (
        min(
            after_first_cycle_min_rows,
            key=lambda row: row[
                "minimum_full_without_first_three_to_principal_ratio"])
        if after_first_cycle_min_rows else None)

    return {
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "natural_modulus": 286,
        "support": (11, 13),
        "tested_target_count": lower_receipt["tested_target_count"],
        "cycle_rows": tuple(cycle_rows),
        "global_minimum_complement_cycle": global_min_row["cycle"],
        "global_minimum_complement_target": global_min_row[
            "minimum_full_without_first_three_target"],
        "global_minimum_complement_to_principal_ratio": global_min_row[
            "minimum_full_without_first_three_to_principal_ratio"],
        "after_first_cycle_minimum_complement_cycle": (
            after_first_min_row["cycle"] if after_first_min_row else None),
        "after_first_cycle_minimum_complement_target": (
            after_first_min_row[
                "minimum_full_without_first_three_target"]
            if after_first_min_row else None),
        "after_first_cycle_minimum_complement_to_principal_ratio": (
            after_first_min_row[
                "minimum_full_without_first_three_to_principal_ratio"]
            if after_first_min_row else None),
        "total_full_action_negative_count": sum(
            row["full_action_negative_count"] for row in cycle_rows),
        "total_full_without_first_three_nonpositive_count": sum(
            row["full_without_first_three_nonpositive_count"]
            for row in cycle_rows),
        "complement_cycle_envelope_measured": True,
        "eventual_complement_lower_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_boundary_component_split_receipt(
        targets=(14138, 24148),
        mode_count=6,
        tolerance=1e-09):
    """Component split for q286 boundary-layer clearance targets."""
    targets = tuple(targets)
    lower_receipt = q286_first_two_mode_lower_tail_receipt(
        selected_targets=targets,
        targets_per_cycle=5005,
        tolerance=tolerance)
    mode_receipt = q286_leading_singular_mode_contribution_receipt(
        targets=targets,
        mode_count=mode_count,
        tolerance=tolerance)
    target_rows = {}
    for target in targets:
        lower_row = lower_receipt["rows"][target]
        mode_rows = tuple({
            "mode_index": row["mode_index"],
            "contribution_to_principal_ratio": row[
                "contribution_to_principal_ratio"],
        } for row in mode_receipt["rows"][target]["mode_rows"])
        first_three = lower_row[
            "first_three_modes_to_principal_ratio"]
        complement = lower_row[
            "full_without_first_three_to_principal_ratio"]
        q286_after_first_three = (
            lower_row["q286_deviation_to_principal_ratio"] - first_three)
        reduced_after_first_three = lower_row[
            "reduced_without_first_three_to_principal_ratio"]
        target_rows[target] = {
            "full_action_to_principal_ratio": lower_row[
                "full_action_to_principal_ratio"],
            "reduced_model_to_principal_ratio": lower_row[
                "reduced_model_to_principal_ratio"],
            "q286_deviation_to_principal_ratio": lower_row[
                "q286_deviation_to_principal_ratio"],
            "first_three_modes_to_principal_ratio": first_three,
            "q286_after_first_three_to_principal_ratio": (
                q286_after_first_three),
            "full_without_first_three_to_principal_ratio": complement,
            "reduced_without_first_three_to_principal_ratio": (
                reduced_after_first_three),
            "full_minus_reduced_to_principal_ratio": lower_row[
                "full_minus_reduced_to_principal_ratio"],
            "mode_rows": mode_rows,
        }
    return {
        "targets": targets,
        "mode_count": mode_count,
        "natural_modulus": 286,
        "support": (11, 13),
        "target_rows": target_rows,
        "minimum_full_without_first_three_target": min(
            targets,
            key=lambda target: target_rows[target][
                "full_without_first_three_to_principal_ratio"]),
        "maximum_full_without_first_three_target": max(
            targets,
            key=lambda target: target_rows[target][
                "full_without_first_three_to_principal_ratio"]),
        "boundary_component_split_measured": True,
        "component_lower_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_boundary_complement_support_split_receipt(
        targets=(14138, 24148),
        mode_count=6,
        tolerance=1e-09):
    """Split the boundary complement by lower-modulus support.

    The complement measured by ``q286_boundary_component_split_receipt`` is the
    full assembled strict-central action after removing the first three q286
    separable modes.  This receipt identifies which lower-modulus support
    components create that complement.  It is a diagnostic only: it does not
    prove a lower bound for those components.
    """
    targets = tuple(targets)
    if (not targets or any(type(target) is not int or target < 40
                           or target % 2 for target in targets)):
        raise ValueError("targets must be even integers at least 40")
    if (type(mode_count) is not int or mode_count < 3
            or mode_count > 9):
        raise ValueError("mode_count must lie between 3 and 9")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    support_receipt = combined_coefficient_support_contribution_receipt(
        targets=targets, tolerance=tolerance)
    deviation_receipt = combined_coefficient_lower_modulus_deviation_receipt(
        targets=targets, tolerance=tolerance)
    boundary_receipt = q286_boundary_component_split_receipt(
        targets=targets, mode_count=mode_count, tolerance=tolerance)

    target_rows = {}
    maximum_reconstruction_error = 0.0
    for target in targets:
        support_row = support_receipt["rows"][target]
        boundary_row = boundary_receipt["target_rows"][target]
        contributions = support_row["contributions_by_support"]
        principal = contributions["principal"]
        if abs(principal.real) <= tolerance:
            raise ArithmeticError("principal contribution is too small")
        support_ratios = {
            support: complex(value).real / principal.real
            for support, value in contributions.items()
            if support != "principal"
        }
        non_q286_support_sum = math.fsum(
            ratio for support, ratio in support_ratios.items()
            if support != (11, 13))
        first_three = boundary_row[
            "first_three_modes_to_principal_ratio"]
        q286_actual = support_ratios[(11, 13)]
        q286_actual_after_first_three = q286_actual - first_three
        reconstructed = (
            1.0 + non_q286_support_sum + q286_actual_after_first_three)
        complement = boundary_row[
            "full_without_first_three_to_principal_ratio"]
        reconstruction_error = abs(reconstructed - complement)
        maximum_reconstruction_error = max(
            maximum_reconstruction_error, reconstruction_error)

        sorted_support_ratios = tuple(
            (support, ratio)
            for support, ratio in sorted(
                support_ratios.items(),
                key=lambda item: abs(item[1]),
                reverse=True))
        positive_supports = tuple(
            (support, ratio) for support, ratio in sorted_support_ratios
            if ratio > 0)
        negative_supports = tuple(
            (support, ratio) for support, ratio in sorted_support_ratios
            if ratio < 0)
        q286_deviation_row = deviation_receipt[
            "rows"][target]["support_rows"][(11, 13)]
        target_rows[target] = {
            "full_action_to_principal_ratio": boundary_row[
                "full_action_to_principal_ratio"],
            "full_without_first_three_to_principal_ratio": complement,
            "support_reconstructed_without_first_three_to_principal_ratio": (
                reconstructed),
            "support_reconstruction_error": reconstruction_error,
            "principal_to_principal_ratio": 1.0,
            "support_ratios_to_principal": support_ratios,
            "support_ratios_sorted_by_absolute_size": sorted_support_ratios,
            "non_q286_support_sum_to_principal_ratio": non_q286_support_sum,
            "q286_actual_to_principal_ratio": q286_actual,
            "q286_local_prediction_to_principal_ratio": q286_deviation_row[
                "local_prediction_to_principal_ratio"],
            "q286_deviation_to_principal_ratio": boundary_row[
                "q286_deviation_to_principal_ratio"],
            "first_three_modes_to_principal_ratio": first_three,
            "q286_actual_after_first_three_to_principal_ratio": (
                q286_actual_after_first_three),
            "q286_deviation_after_first_three_to_principal_ratio": (
                boundary_row[
                    "q286_after_first_three_to_principal_ratio"]),
            "dominant_positive_centered_support": (
                positive_supports[0][0] if positive_supports else None),
            "dominant_negative_centered_support": (
                negative_supports[0][0] if negative_supports else None),
        }
    return {
        "targets": targets,
        "mode_count": mode_count,
        "arithmetic_period": support_receipt["arithmetic_period"],
        "natural_q286_modulus": 286,
        "natural_q70_modulus": 70,
        "natural_q154_modulus": 154,
        "target_rows": target_rows,
        "maximum_support_reconstruction_error": (
            maximum_reconstruction_error),
        "minimum_complement_target": min(
            targets,
            key=lambda target: target_rows[target][
                "full_without_first_three_to_principal_ratio"]),
        "maximum_complement_target": max(
            targets,
            key=lambda target: target_rows[target][
                "full_without_first_three_to_principal_ratio"]),
        "boundary_complement_support_split_measured": True,
        "component_lower_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_removed_support_envelope_receipt(
        start=10000, cycle_count=1, targets_per_cycle=501,
        tolerance=1e-9, selected_targets=None):
    """Scan support components after removing q286 modes 1..3.

    This receipt turns the boundary-complement split into a finite lower-tail
    scanner.  It keeps the principal and every lower-modulus support explicit,
    removes only the first three q286 separable modes, and records whether the
    resulting complement remains positive on the tested targets.
    """
    if selected_targets is None:
        if type(start) is not int or start < 40 or start % 2:
            raise ValueError("start must be an even integer at least 40")
        if type(cycle_count) is not int or cycle_count < 1:
            raise ValueError("cycle_count must be a positive integer")
        if (type(targets_per_cycle) is not int or targets_per_cycle < 1
                or targets_per_cycle > 5005):
            raise ValueError("targets_per_cycle must lie between 1 and 5005")
    else:
        selected_targets = tuple(dict.fromkeys(selected_targets))
        if (not selected_targets
                or any(type(target) is not int or target < 40
                       or target % 2 for target in selected_targets)):
            raise ValueError(
                "selected_targets must be even integers at least 40")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    if selected_targets is None:
        first = reduced_full_lower_envelope_receipt(
            start=start, targets_per_cycle=targets_per_cycle,
            q286_mode_count=6, tolerance=tolerance)
        period = first["arithmetic_period"]
        full_rows_by_cycle = {0: first}
        targets = list(sorted(first["rows"]))
        for cycle in range(1, cycle_count):
            receipt = reduced_full_lower_envelope_receipt(
                start=start + cycle * period,
                targets_per_cycle=targets_per_cycle,
                q286_mode_count=6, tolerance=tolerance)
            full_rows_by_cycle[cycle] = receipt
            targets.extend(sorted(receipt["rows"]))
    else:
        first = reduced_full_lower_envelope_receipt(
            q286_mode_count=6, tolerance=tolerance,
            selected_targets=selected_targets)
        period = first["arithmetic_period"]
        start = selected_targets[0]
        cycle_count = 1
        targets_per_cycle = len(selected_targets)
        full_rows_by_cycle = {0: first}
        targets = list(selected_targets)

    mode_receipt = q286_leading_singular_mode_contribution_receipt(
        targets=tuple(targets), mode_count=6, tolerance=tolerance)

    rows = {}
    cycle_rows = {}
    global_minimum = None
    global_minimum_without_q70 = None
    nonpositive_targets = []
    nonpositive_without_q70_targets = []
    dominant_positive_counts = {}
    dominant_negative_counts = {}
    for cycle, receipt in full_rows_by_cycle.items():
        row_targets = tuple(sorted(receipt["rows"]))
        cycle_minimum = None
        cycle_nonpositive = []
        for target in row_targets:
            full_row = receipt["rows"][target]
            principal = full_row["principal_contribution"].real
            if abs(principal) <= tolerance:
                raise ArithmeticError("principal contribution is too small")
            support_rows = full_row["support_rows"]
            mode_ratios = tuple(
                row["contribution_to_principal_ratio"]
                for row in mode_receipt["rows"][target]["mode_rows"])
            first_three = math.fsum(mode_ratios[:3])
            support_ratios = {
                support: (
                    support_rows[support]["actual_contribution"].real
                    / principal)
                if support == (11, 13)
                else support_rows[support]["actual_to_principal_ratio"]
                for support in receipt["support_order"]}
            q286_after_first_three = support_ratios[(11, 13)] - first_three
            q70 = support_ratios[(5, 7)]
            q154 = support_ratios[(7, 11)]
            small = full_row["small_support_to_principal_ratio"]
            non_q286 = math.fsum(
                ratio for support, ratio in support_ratios.items()
                if support != (11, 13))
            complement = (
                full_row["full_action_to_principal_ratio"] - first_three)
            reconstructed = 1.0 + non_q286 + q286_after_first_three
            without_q70 = complement - q70
            centered_terms = (
                ((11, 13), q286_after_first_three),
                ((5, 7), q70),
                ((7, 11), q154),
                ("small_supports", small),
            )
            positive_terms = tuple(
                item for item in centered_terms if item[1] > 0)
            negative_terms = tuple(
                item for item in centered_terms if item[1] < 0)
            dominant_positive = (
                max(positive_terms, key=lambda item: item[1])[0]
                if positive_terms else None)
            dominant_negative = (
                min(negative_terms, key=lambda item: item[1])[0]
                if negative_terms else None)
            if dominant_positive is not None:
                dominant_positive_counts[dominant_positive] = (
                    dominant_positive_counts.get(dominant_positive, 0) + 1)
            if dominant_negative is not None:
                dominant_negative_counts[dominant_negative] = (
                    dominant_negative_counts.get(dominant_negative, 0) + 1)
            summary = {
                "cycle": cycle,
                "full_action_to_principal_ratio": full_row[
                    "full_action_to_principal_ratio"],
                "first_three_modes_to_principal_ratio": first_three,
                "full_without_first_three_to_principal_ratio": complement,
                "support_reconstructed_without_first_three_to_principal_ratio": (
                    reconstructed),
                "support_reconstruction_error": abs(
                    reconstructed - complement),
                "without_q70_to_principal_ratio": without_q70,
                "q286_after_first_three_to_principal_ratio": (
                    q286_after_first_three),
                "q70_to_principal_ratio": q70,
                "q154_to_principal_ratio": q154,
                "small_support_to_principal_ratio": small,
                "non_q286_support_sum_to_principal_ratio": non_q286,
                "dominant_positive_complement_term": dominant_positive,
                "dominant_negative_complement_term": dominant_negative,
            }
            rows[target] = summary
            if complement <= tolerance:
                nonpositive_targets.append(target)
                cycle_nonpositive.append(target)
            if without_q70 <= tolerance:
                nonpositive_without_q70_targets.append(target)
            if global_minimum is None or complement < global_minimum[1]:
                global_minimum = (target, complement, cycle)
            if (global_minimum_without_q70 is None
                    or without_q70 < global_minimum_without_q70[1]):
                global_minimum_without_q70 = (target, without_q70, cycle)
            if cycle_minimum is None or complement < cycle_minimum[1]:
                cycle_minimum = (target, complement)
        cycle_rows[cycle] = {
            "start": row_targets[0],
            "end": row_targets[-1],
            "tested_target_count": len(row_targets),
            "minimum_complement_target": cycle_minimum[0],
            "minimum_complement_to_principal_ratio": cycle_minimum[1],
            "nonpositive_complement_count": len(cycle_nonpositive),
            "nonpositive_complement_targets": tuple(cycle_nonpositive),
        }

    return {
        "arithmetic_period": period,
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "selected_targets": (
            tuple(targets) if selected_targets is not None else None),
        "tested_target_count": len(targets),
        "rows": rows,
        "cycle_rows": cycle_rows,
        "minimum_complement_target": global_minimum[0],
        "minimum_complement_cycle": global_minimum[2],
        "minimum_complement_to_principal_ratio": global_minimum[1],
        "nonpositive_complement_count": len(nonpositive_targets),
        "nonpositive_complement_targets": tuple(nonpositive_targets),
        "minimum_without_q70_target": global_minimum_without_q70[0],
        "minimum_without_q70_cycle": global_minimum_without_q70[2],
        "minimum_without_q70_to_principal_ratio": (
            global_minimum_without_q70[1]),
        "nonpositive_without_q70_count": len(nonpositive_without_q70_targets),
        "dominant_positive_term_counts": dominant_positive_counts,
        "dominant_negative_term_counts": dominant_negative_counts,
        "maximum_support_reconstruction_error": max(
            row["support_reconstruction_error"] for row in rows.values()),
        "first_three_removed_support_envelope_measured": True,
        "eventual_complement_lower_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_removed_support_gram_receipt(
        start=10000, cycle_count=1, targets_per_cycle=501,
        tolerance=1e-9, selected_targets=None):
    """Measure Gram matrices for the first-three-removed support vectors.

    The first-three-removed support envelope keeps principal plus q70, q154,
    q286-after-first-three, and smaller supports explicit.  This receipt
    measures centered correlations and raw cosines among those moving
    principal-relative component vectors.  It is finite evidence only, not a
    vector-envelope theorem.
    """
    envelope = q286_first_three_removed_support_envelope_receipt(
        start=start, cycle_count=cycle_count, targets_per_cycle=targets_per_cycle,
        tolerance=tolerance, selected_targets=selected_targets)
    component_labels = (
        "q286_after_first_three", "q70", "q154",
        "small_supports", "non_q286", "complement")
    row_keys = {
        "q286_after_first_three": (
            "q286_after_first_three_to_principal_ratio"),
        "q70": "q70_to_principal_ratio",
        "q154": "q154_to_principal_ratio",
        "small_supports": "small_support_to_principal_ratio",
        "non_q286": "non_q286_support_sum_to_principal_ratio",
        "complement": "full_without_first_three_to_principal_ratio",
    }
    ordered_targets = tuple(sorted(envelope["rows"]))
    vectors = {
        label: tuple(envelope["rows"][target][row_keys[label]]
                     for target in ordered_targets)
        for label in component_labels}

    def dot(left, right):
        return math.fsum(a * b for a, b in zip(left, right))

    def mean(values):
        return math.fsum(values) / len(values)

    def centered(values):
        average = mean(values)
        return tuple(value - average for value in values)

    def cosine(left, right):
        norm = math.sqrt(dot(left, left) * dot(right, right))
        return dot(left, right) / norm if norm > tolerance else math.nan

    centered_vectors = {
        label: centered(values) for label, values in vectors.items()}
    component_stats = {}
    for label, values in vectors.items():
        component_stats[label] = {
            "mean": mean(values),
            "minimum": min(values),
            "maximum": max(values),
            "rms": math.sqrt(dot(values, values) / len(values)),
            "centered_rms": math.sqrt(
                dot(centered_vectors[label], centered_vectors[label])
                / len(values)),
        }

    centered_correlation = {}
    raw_cosine = {}
    for left in component_labels:
        for right in component_labels:
            centered_correlation[(left, right)] = cosine(
                centered_vectors[left], centered_vectors[right])
            raw_cosine[(left, right)] = cosine(vectors[left], vectors[right])

    q70_q154 = centered_correlation[("q70", "q154")]
    non_q286_complement = centered_correlation[("non_q286", "complement")]
    return {
        "arithmetic_period": envelope["arithmetic_period"],
        "start": envelope["start"],
        "cycle_count": envelope["cycle_count"],
        "targets_per_cycle": envelope["targets_per_cycle"],
        "selected_targets": envelope["selected_targets"],
        "tested_target_count": envelope["tested_target_count"],
        "component_labels": component_labels,
        "component_stats": component_stats,
        "centered_correlation_matrix": centered_correlation,
        "raw_cosine_matrix": raw_cosine,
        "q70_q154_centered_correlation": q70_q154,
        "non_q286_complement_centered_correlation": non_q286_complement,
        "q70_and_q154_nearly_orthogonal_on_sample": bool(
            abs(q70_q154) < .1),
        "non_q286_tracks_complement_motion_on_sample": bool(
            non_q286_complement > .9),
        "minimum_complement_target": envelope["minimum_complement_target"],
        "minimum_complement_to_principal_ratio": envelope[
            "minimum_complement_to_principal_ratio"],
        "nonpositive_complement_count": envelope[
            "nonpositive_complement_count"],
        "first_three_removed_support_gram_measured": True,
        "eventual_vector_envelope_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_removed_vector_stress_receipt(
        start=10000, cycle_count=1, targets_per_cycle=501,
        tolerance=1e-9, selected_targets=None):
    """Stress-test norm-only control of the post-first-three support vector.

    The post-first-three complement has the form ``1 + sum(component_j)`` in
    principal-relative units.  This receipt asks whether the measured finite
    lower envelope is explained by component norms alone, or by the pointwise
    alignment of the component vector with the all-ones summation direction.
    """
    envelope = q286_first_three_removed_support_envelope_receipt(
        start=start, cycle_count=cycle_count, targets_per_cycle=targets_per_cycle,
        tolerance=tolerance, selected_targets=selected_targets)
    component_labels = (
        "q286_after_first_three", "q70", "q154", "small_supports")
    row_keys = {
        "q286_after_first_three": (
            "q286_after_first_three_to_principal_ratio"),
        "q70": "q70_to_principal_ratio",
        "q154": "q154_to_principal_ratio",
        "small_supports": "small_support_to_principal_ratio",
    }
    ordered_targets = tuple(sorted(envelope["rows"]))
    vectors = {
        label: tuple(envelope["rows"][target][row_keys[label]]
                     for target in ordered_targets)
        for label in component_labels}

    def dot(left, right):
        return math.fsum(a * b for a, b in zip(left, right))

    def mean(values):
        return math.fsum(values) / len(values)

    means = {label: mean(values) for label, values in vectors.items()}
    centered = {
        label: tuple(value - means[label] for value in values)
        for label, values in vectors.items()}
    variances = {
        label: dot(values, values) / len(values)
        for label, values in centered.items()}

    covariance_matrix = {}
    for left in component_labels:
        for right in component_labels:
            covariance_matrix[(left, right)] = dot(
                centered[left], centered[right]) / len(ordered_targets)
    support_sum = tuple(
        math.fsum(vectors[label][index] for label in component_labels)
        for index in range(len(ordered_targets)))
    complement = tuple(1.0 + value for value in support_sum)
    mean_support_sum = mean(support_sum)
    mean_complement = 1.0 + mean_support_sum
    centered_support_sum = tuple(value - mean_support_sum
                                 for value in support_sum)
    support_sum_variance = dot(centered_support_sum, centered_support_sum) / len(
        ordered_targets)
    diagonal_variance_sum = math.fsum(variances.values())
    cross_term_total = support_sum_variance - diagonal_variance_sum
    normalized_cross_term_total = (
        cross_term_total / diagonal_variance_sum
        if diagonal_variance_sum > tolerance else math.nan)
    component_box_lower_bound = 1.0 + math.fsum(
        min(vectors[label]) for label in component_labels)
    rms_only_lower_bound = mean_complement - math.sqrt(
        max(0, len(ordered_targets) - 1) * support_sum_variance)
    max_centered_vector_norm = 0.0
    worst_norm_target = None
    target_rows = {}
    for index, target in enumerate(ordered_targets):
        centered_vector = tuple(centered[label][index]
                                for label in component_labels)
        centered_norm = math.sqrt(math.fsum(
            value * value for value in centered_vector))
        max_centered_vector_norm = max(max_centered_vector_norm, centered_norm)
        if (worst_norm_target is None or centered_norm > target_rows[
                worst_norm_target]["centered_vector_norm"]):
            worst_norm_target = target
        centered_sum = math.fsum(centered_vector)
        sum_direction_cosine = (
            centered_sum / (2.0 * centered_norm)
            if centered_norm > tolerance else math.nan)
        target_rows[target] = {
            "component_vector": tuple(vectors[label][index]
                                      for label in component_labels),
            "centered_component_vector": centered_vector,
            "centered_vector_norm": centered_norm,
            "centered_support_sum": centered_sum,
            "sum_direction_cosine": sum_direction_cosine,
            "support_sum_to_principal_ratio": support_sum[index],
            "complement_to_principal_ratio": complement[index],
        }
    finite_max_norm_lower_bound = mean_complement - 2.0 * max_centered_vector_norm
    minimum_target = min(
        ordered_targets, key=lambda target: target_rows[target][
            "complement_to_principal_ratio"])
    return {
        "arithmetic_period": envelope["arithmetic_period"],
        "start": envelope["start"],
        "cycle_count": envelope["cycle_count"],
        "targets_per_cycle": envelope["targets_per_cycle"],
        "selected_targets": envelope["selected_targets"],
        "tested_target_count": envelope["tested_target_count"],
        "component_labels": component_labels,
        "component_means": means,
        "component_centered_variances": variances,
        "centered_covariance_matrix": covariance_matrix,
        "variance_decomposition": {
            "diagonal_variance_sum": diagonal_variance_sum,
            "cross_term_total": cross_term_total,
            "normalized_cross_term_total": normalized_cross_term_total,
            "support_sum_variance": support_sum_variance,
        },
        "mean_support_sum_to_principal_ratio": mean_support_sum,
        "mean_complement_to_principal_ratio": mean_complement,
        "component_box_lower_bound": component_box_lower_bound,
        "rms_only_lower_bound": rms_only_lower_bound,
        "finite_max_norm_lower_bound": finite_max_norm_lower_bound,
        "maximum_centered_vector_norm": max_centered_vector_norm,
        "maximum_centered_vector_norm_target": worst_norm_target,
        "minimum_complement_target": minimum_target,
        "minimum_complement_row": target_rows[minimum_target],
        "minimum_complement_to_principal_ratio": target_rows[
            minimum_target]["complement_to_principal_ratio"],
        "nonpositive_complement_count": envelope[
            "nonpositive_complement_count"],
        "target_rows": target_rows,
        "box_bound_certifies_positive_complement_on_sample": bool(
            component_box_lower_bound > tolerance),
        "rms_bound_certifies_positive_complement_on_sample": bool(
            rms_only_lower_bound > tolerance),
        "max_norm_bound_certifies_positive_complement_on_sample": bool(
            finite_max_norm_lower_bound > tolerance),
        "first_three_removed_vector_stress_measured": True,
        "norm_only_lower_bound_proved": False,
        "eventual_vector_envelope_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_removed_low_tail_lift_receipt(
        base_targets=(14138, 14732, 12578, 12944, 16388),
        lifts=(0, 1, 4, 9, 19, 49), threshold=.3,
        tolerance=1e-9):
    """Follow low post-first-three complement targets through period lifts.

    This receipt tests whether the pointwise support-vector lower tail is a
    persistent residue-class obstruction or an early/boundary-scale alignment
    that clears under arithmetic-period lifts.  It uses the same component
    vectors as ``q286_first_three_removed_vector_stress_receipt``.
    """
    base_targets = tuple(dict.fromkeys(base_targets))
    lifts = tuple(dict.fromkeys(lifts))
    if (not base_targets
            or any(type(target) is not int or target < 40 or target % 2
                   for target in base_targets)):
        raise ValueError("base_targets must be even integers at least 40")
    if (not lifts or any(type(lift) is not int or lift < 0
                         for lift in lifts)):
        raise ValueError("lifts must be nonnegative integers")
    if not math.isfinite(threshold) or threshold <= 0:
        raise ValueError("threshold must be finite and positive")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    period = 10010
    selected_targets = tuple(
        base + lift * period for base in base_targets for lift in lifts)
    stress = q286_first_three_removed_vector_stress_receipt(
        selected_targets=selected_targets, tolerance=tolerance)
    period = stress["arithmetic_period"]
    base_rows = {}
    global_minimum = None
    targets_below_threshold = []
    for base in base_targets:
        lift_rows = {}
        for lift in lifts:
            target = base + lift * period
            row = stress["target_rows"][target]
            vector = row["component_vector"]
            lift_row = {
                "target": target,
                "complement_to_principal_ratio": row[
                    "complement_to_principal_ratio"],
                "support_sum_to_principal_ratio": row[
                    "support_sum_to_principal_ratio"],
                "centered_vector_norm": row["centered_vector_norm"],
                "sum_direction_cosine": row["sum_direction_cosine"],
                "component_vector": vector,
                "component_sign_pattern": "".join(
                    "+" if value > tolerance else "-"
                    if value < -tolerance else "0" for value in vector),
                "below_threshold": bool(
                    row["complement_to_principal_ratio"] < threshold),
            }
            lift_rows[lift] = lift_row
            if lift_row["below_threshold"]:
                targets_below_threshold.append(target)
            if (global_minimum is None or lift_row[
                    "complement_to_principal_ratio"] < global_minimum[2]):
                global_minimum = (
                    base, lift, lift_row["complement_to_principal_ratio"],
                    target)
        minimum_lift = min(
            lifts, key=lambda lift: lift_rows[lift][
                "complement_to_principal_ratio"])
        first_lift_at_or_above_threshold = next((
            lift for lift in lifts
            if lift_rows[lift]["complement_to_principal_ratio"] >= threshold),
            None)
        base_rows[base] = {
            "lift_rows": lift_rows,
            "minimum_complement_lift": minimum_lift,
            "minimum_complement_target": lift_rows[minimum_lift]["target"],
            "minimum_complement_to_principal_ratio": lift_rows[
                minimum_lift]["complement_to_principal_ratio"],
            "first_lift_at_or_above_threshold": (
                first_lift_at_or_above_threshold),
            "all_lifts_positive": all(
                row["complement_to_principal_ratio"] > tolerance
                for row in lift_rows.values()),
            "below_threshold_lifts": tuple(
                lift for lift in lifts if lift_rows[lift][
                    "below_threshold"]),
        }

    return {
        "arithmetic_period": period,
        "base_targets": base_targets,
        "lifts": lifts,
        "threshold": threshold,
        "tested_target_count": len(selected_targets),
        "base_rows": base_rows,
        "global_minimum_base": global_minimum[0],
        "global_minimum_lift": global_minimum[1],
        "global_minimum_target": global_minimum[3],
        "global_minimum_complement_to_principal_ratio": global_minimum[2],
        "targets_below_threshold": tuple(targets_below_threshold),
        "target_below_threshold_count": len(targets_below_threshold),
        "all_tested_lifts_positive": all(
            row["all_lifts_positive"] for row in base_rows.values()),
        "every_base_clears_threshold_on_tested_lifts": all(
            row["first_lift_at_or_above_threshold"] is not None
            for row in base_rows.values()),
        "first_three_removed_low_tail_lift_measured": True,
        "persistent_low_tail_obstruction_proved": False,
        "eventual_lift_clearance_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_removed_low_tail_auto_lift_receipt(
        base_start=10000, base_targets_per_cycle=5005,
        low_threshold=.3, lifts=(0, 1, 2, 3), tolerance=1e-9):
    """Select all low post-first-three bases and test their period lifts.

    This receipt widens the low-tail lift falsifier from named bottom cases to
    every base target in a finite window whose post-first-three complement lies
    below ``low_threshold``.  It tests whether the selected low-tail alignments
    persist under arithmetic-period lifts.
    """
    if type(base_start) is not int or base_start < 40 or base_start % 2:
        raise ValueError("base_start must be an even integer at least 40")
    if (type(base_targets_per_cycle) is not int
            or base_targets_per_cycle < 1 or base_targets_per_cycle > 5005):
        raise ValueError(
            "base_targets_per_cycle must lie between 1 and 5005")
    if not math.isfinite(low_threshold) or low_threshold <= 0:
        raise ValueError("low_threshold must be finite and positive")
    lifts = tuple(dict.fromkeys(lifts))
    if (not lifts or any(type(lift) is not int or lift < 0
                         for lift in lifts)):
        raise ValueError("lifts must be nonnegative integers")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    base_scan = q286_first_three_removed_vector_stress_receipt(
        start=base_start, cycle_count=1,
        targets_per_cycle=base_targets_per_cycle, tolerance=tolerance)
    selected_bases = tuple(
        target for target in sorted(base_scan["target_rows"])
        if base_scan["target_rows"][target][
            "complement_to_principal_ratio"] < low_threshold)
    if selected_bases:
        lift_receipt = q286_first_three_removed_low_tail_lift_receipt(
            base_targets=selected_bases, lifts=lifts, threshold=low_threshold,
            tolerance=tolerance)
        first_clear_lifts = tuple(
            row["first_lift_at_or_above_threshold"]
            for row in lift_receipt["base_rows"].values())
        maximum_first_clear_lift = max(
            lift for lift in first_clear_lifts if lift is not None)
        below_counts_by_lift = {
            lift: sum(
                1 for row in lift_receipt["base_rows"].values()
                if lift in row["below_threshold_lifts"])
            for lift in lifts}
        all_clear = lift_receipt[
            "every_base_clears_threshold_on_tested_lifts"]
        global_minimum_target = lift_receipt["global_minimum_target"]
        global_minimum_value = lift_receipt[
            "global_minimum_complement_to_principal_ratio"]
    else:
        lift_receipt = None
        first_clear_lifts = tuple()
        maximum_first_clear_lift = None
        below_counts_by_lift = {lift: 0 for lift in lifts}
        all_clear = True
        global_minimum_target = base_scan["minimum_complement_target"]
        global_minimum_value = base_scan[
            "minimum_complement_to_principal_ratio"]

    return {
        "arithmetic_period": base_scan["arithmetic_period"],
        "base_start": base_start,
        "base_targets_per_cycle": base_targets_per_cycle,
        "low_threshold": low_threshold,
        "lifts": lifts,
        "base_scan_minimum_target": base_scan[
            "minimum_complement_target"],
        "base_scan_minimum_complement_to_principal_ratio": base_scan[
            "minimum_complement_to_principal_ratio"],
        "selected_base_targets": selected_bases,
        "selected_base_count": len(selected_bases),
        "tested_lift_target_count": len(selected_bases) * len(lifts),
        "lift_receipt": lift_receipt,
        "first_clear_lifts": first_clear_lifts,
        "maximum_first_clear_lift": maximum_first_clear_lift,
        "below_threshold_counts_by_lift": below_counts_by_lift,
        "all_selected_bases_clear_threshold_on_tested_lifts": all_clear,
        "global_minimum_lifted_target": global_minimum_target,
        "global_minimum_lifted_complement_to_principal_ratio": (
            global_minimum_value),
        "first_three_removed_low_tail_auto_lift_measured": True,
        "persistent_low_tail_obstruction_proved": False,
        "eventual_lift_clearance_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_removed_low_tail_multi_period_receipt(
        base_start=10000, cycle_count=4, targets_per_cycle=5005,
        low_threshold=.3, lifts=(0, 1), tolerance=1e-9):
    """Select low post-first-three bases across many periods and lift once.

    This is the efficient recurrence version of the auto-lift check: it scans
    multiple base periods in one support-vector stress receipt, selects every
    target whose post-first-three complement lies below ``low_threshold``, and
    then tests all selected bases through the requested period lifts in one
    lift receipt.
    """
    if type(base_start) is not int or base_start < 40 or base_start % 2:
        raise ValueError("base_start must be an even integer at least 40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    if not math.isfinite(low_threshold) or low_threshold <= 0:
        raise ValueError("low_threshold must be finite and positive")
    lifts = tuple(dict.fromkeys(lifts))
    if (not lifts or any(type(lift) is not int or lift < 0
                         for lift in lifts)):
        raise ValueError("lifts must be nonnegative integers")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    base_scan = q286_first_three_removed_vector_stress_receipt(
        start=base_start, cycle_count=cycle_count,
        targets_per_cycle=targets_per_cycle, tolerance=tolerance)
    period = base_scan["arithmetic_period"]
    selected_bases = tuple(
        target for target in sorted(base_scan["target_rows"])
        if base_scan["target_rows"][target][
            "complement_to_principal_ratio"] < low_threshold)
    selected_by_cycle = {cycle: [] for cycle in range(cycle_count)}
    for target in selected_bases:
        cycle = (target - base_start) // period
        selected_by_cycle[cycle].append(target)
    selected_counts_by_cycle = {
        cycle: len(targets) for cycle, targets in selected_by_cycle.items()}
    cycle_minimum_rows = {}
    for cycle in range(cycle_count):
        cycle_targets = tuple(
            target for target in base_scan["target_rows"]
            if (base_start + cycle * period
                <= target
                <= base_start + cycle * period
                + 2 * (targets_per_cycle - 1)))
        minimum_target = min(
            cycle_targets,
            key=lambda target: base_scan["target_rows"][target][
                "complement_to_principal_ratio"])
        cycle_minimum_rows[cycle] = {
            "minimum_complement_target": minimum_target,
            "minimum_complement_to_principal_ratio": base_scan[
                "target_rows"][minimum_target][
                    "complement_to_principal_ratio"],
            "selected_below_threshold_count": selected_counts_by_cycle[
                cycle],
        }

    if selected_bases:
        lift_receipt = q286_first_three_removed_low_tail_lift_receipt(
            base_targets=selected_bases, lifts=lifts, threshold=low_threshold,
            tolerance=tolerance)
        first_clear_lifts = tuple(
            row["first_lift_at_or_above_threshold"]
            for row in lift_receipt["base_rows"].values())
        finite_first_clear_lifts = tuple(
            lift for lift in first_clear_lifts if lift is not None)
        maximum_first_clear_lift = (
            max(finite_first_clear_lifts) if finite_first_clear_lifts
            else None)
        below_threshold_counts_by_lift = {
            lift: sum(
                1 for row in lift_receipt["base_rows"].values()
                if lift in row["below_threshold_lifts"])
            for lift in lifts}
        all_clear = lift_receipt[
            "every_base_clears_threshold_on_tested_lifts"]
        all_positive = lift_receipt["all_tested_lifts_positive"]
        global_minimum_lifted_target = lift_receipt[
            "global_minimum_target"]
        global_minimum_lifted_value = lift_receipt[
            "global_minimum_complement_to_principal_ratio"]
    else:
        lift_receipt = None
        first_clear_lifts = tuple()
        maximum_first_clear_lift = None
        below_threshold_counts_by_lift = {lift: 0 for lift in lifts}
        all_clear = True
        all_positive = True
        global_minimum_lifted_target = base_scan[
            "minimum_complement_target"]
        global_minimum_lifted_value = base_scan[
            "minimum_complement_to_principal_ratio"]

    return {
        "arithmetic_period": period,
        "base_start": base_start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "low_threshold": low_threshold,
        "lifts": lifts,
        "base_scan_tested_target_count": base_scan[
            "tested_target_count"],
        "base_scan_minimum_target": base_scan[
            "minimum_complement_target"],
        "base_scan_minimum_complement_to_principal_ratio": base_scan[
            "minimum_complement_to_principal_ratio"],
        "cycle_minimum_rows": cycle_minimum_rows,
        "selected_base_targets": selected_bases,
        "selected_base_count": len(selected_bases),
        "selected_base_counts_by_cycle": selected_counts_by_cycle,
        "tested_lift_target_count": len(selected_bases) * len(lifts),
        "lift_receipt": lift_receipt,
        "first_clear_lifts": first_clear_lifts,
        "maximum_first_clear_lift": maximum_first_clear_lift,
        "below_threshold_counts_by_lift": below_threshold_counts_by_lift,
        "all_selected_bases_clear_threshold_on_tested_lifts": all_clear,
        "all_selected_lift_targets_positive": all_positive,
        "global_minimum_lifted_target": global_minimum_lifted_target,
        "global_minimum_lifted_complement_to_principal_ratio": (
            global_minimum_lifted_value),
        "first_three_removed_low_tail_multi_period_measured": True,
        "persistent_low_tail_obstruction_proved": False,
        "eventual_lift_clearance_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_removed_complement_threshold_horizon_receipt(
        start=10000, cycle_count=8, targets_per_cycle=5005,
        thresholds=(.3, .4, .5), tolerance=1e-9):
    """Summarize complement cycle minima against fixed thresholds.

    This receipt uses ``q286_complement_cycle_envelope_receipt`` to scan the
    post-first-three complement and records where finite cycle minima fall
    below selected thresholds.  It is a horizon diagnostic only, not an
    eventual lower-bound theorem.
    """
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    thresholds = tuple(thresholds)
    if (not thresholds or any(not math.isfinite(threshold)
                              or threshold <= 0
                              for threshold in thresholds)):
        raise ValueError("thresholds must be positive finite numbers")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    envelope = q286_complement_cycle_envelope_receipt(
        start=start, cycle_count=cycle_count,
        targets_per_cycle=targets_per_cycle, tolerance=tolerance)
    period = 10010
    cycle_rows = {}
    for row in envelope["cycle_rows"]:
        cycle_start = start + row["cycle"] * period
        cycle_rows[row["cycle"]] = {
            "start": cycle_start,
            "end": cycle_start + 2 * (row["target_count"] - 1),
            "target_count": row["target_count"],
            "minimum_complement_target": row[
                "minimum_full_without_first_three_target"],
            "minimum_complement_to_principal_ratio": row[
                "minimum_full_without_first_three_to_principal_ratio"],
            "full_action_negative_count": row[
                "full_action_negative_count"],
            "complement_nonpositive_count": row[
                "full_without_first_three_nonpositive_count"],
        }

    threshold_rows = {}
    for threshold in thresholds:
        cycles_below = tuple(
            cycle for cycle, row in cycle_rows.items()
            if row["minimum_complement_to_principal_ratio"] < threshold)
        targets_below = tuple(
            cycle_rows[cycle]["minimum_complement_target"]
            for cycle in cycles_below)
        threshold_rows[threshold] = {
            "cycle_count_below_threshold": len(cycles_below),
            "cycles_below_threshold": cycles_below,
            "cycle_minimum_targets_below_threshold": targets_below,
            "last_cycle_below_threshold": (
                max(cycles_below) if cycles_below else None),
            "first_cycle_at_or_above_threshold_after_start": next((
                cycle for cycle in sorted(cycle_rows)
                if cycle_rows[cycle][
                    "minimum_complement_to_principal_ratio"] >= threshold),
                None),
            "all_cycles_at_or_above_threshold": bool(
                not cycles_below),
        }

    return {
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "thresholds": thresholds,
        "arithmetic_period": period,
        "tested_target_count": envelope["tested_target_count"],
        "cycle_rows": cycle_rows,
        "threshold_rows": threshold_rows,
        "global_minimum_complement_cycle": envelope[
            "global_minimum_complement_cycle"],
        "global_minimum_complement_target": envelope[
            "global_minimum_complement_target"],
        "global_minimum_complement_to_principal_ratio": envelope[
            "global_minimum_complement_to_principal_ratio"],
        "after_first_cycle_minimum_complement_cycle": envelope[
            "after_first_cycle_minimum_complement_cycle"],
        "after_first_cycle_minimum_complement_target": envelope[
            "after_first_cycle_minimum_complement_target"],
        "after_first_cycle_minimum_complement_to_principal_ratio": envelope[
            "after_first_cycle_minimum_complement_to_principal_ratio"],
        "total_full_action_negative_count": envelope[
            "total_full_action_negative_count"],
        "total_complement_nonpositive_count": envelope[
            "total_full_without_first_three_nonpositive_count"],
        "first_three_removed_complement_threshold_horizon_measured": True,
        "eventual_threshold_horizon_proved": False,
        "eventual_complement_lower_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_tail_threshold_horizon_receipt(
        start=10000, cycle_count=8, targets_per_cycle=5005,
        negative_tail_thresholds=(.3, .5, .75, 1.0), tolerance=1e-9):
    """Summarize q286 first-three negative tail against thresholds.

    The post-first-three complement horizon gives possible positive buffers.
    This receipt measures the matching obstruction: where the first three q286
    separable modes fall below ``-threshold``.  Passing finite checks here does
    not prove a signed prime-correlation estimate.
    """
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    negative_tail_thresholds = tuple(negative_tail_thresholds)
    if (not negative_tail_thresholds
            or any(not math.isfinite(threshold) or threshold <= 0
                   for threshold in negative_tail_thresholds)):
        raise ValueError(
            "negative_tail_thresholds must be positive finite numbers")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    receipt = q286_first_two_mode_lower_tail_receipt(
        start=start, cycle_count=cycle_count,
        targets_per_cycle=targets_per_cycle, tolerance=tolerance)
    cycle_rows = {}
    global_minimum = None
    for cycle in sorted(receipt["cycle_rows"]):
        targets = tuple(
            target for target, row in receipt["rows"].items()
            if row["cycle"] == cycle)
        minimum_target = min(
            targets, key=lambda target: receipt["rows"][target][
                "first_three_modes_to_principal_ratio"])
        minimum_value = receipt["rows"][minimum_target][
            "first_three_modes_to_principal_ratio"]
        negative_count = sum(
            1 for target in targets
            if receipt["rows"][target][
                "first_three_modes_to_principal_ratio"] < -tolerance)
        cycle_threshold_counts = {
            threshold: sum(
                1 for target in targets
                if receipt["rows"][target][
                    "first_three_modes_to_principal_ratio"] < -threshold)
            for threshold in negative_tail_thresholds}
        cycle_rows[cycle] = {
            "start": receipt["cycle_rows"][cycle]["start"],
            "end": receipt["cycle_rows"][cycle]["end"],
            "tested_target_count": len(targets),
            "minimum_first_three_target": minimum_target,
            "minimum_first_three_to_principal_ratio": minimum_value,
            "negative_first_three_count": negative_count,
            "threshold_counts": cycle_threshold_counts,
            "full_action_negative_count": receipt[
                "cycle_rows"][cycle]["negative_full_action_count"],
        }
        if global_minimum is None or minimum_value < global_minimum[2]:
            global_minimum = (cycle, minimum_target, minimum_value)

    threshold_rows = {}
    for threshold in negative_tail_thresholds:
        cycles_with_hits = tuple(
            cycle for cycle, row in cycle_rows.items()
            if row["threshold_counts"][threshold] > 0)
        threshold_rows[threshold] = {
            "target_count_below_negative_threshold": sum(
                row["threshold_counts"][threshold]
                for row in cycle_rows.values()),
            "cycle_count_with_hits": len(cycles_with_hits),
            "cycles_with_hits": cycles_with_hits,
            "last_cycle_with_hit": (
                max(cycles_with_hits) if cycles_with_hits else None),
            "all_cycles_clear_negative_threshold": bool(
                not cycles_with_hits),
        }

    return {
        "arithmetic_period": receipt["arithmetic_period"],
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "negative_tail_thresholds": negative_tail_thresholds,
        "tested_target_count": receipt["tested_target_count"],
        "cycle_rows": cycle_rows,
        "threshold_rows": threshold_rows,
        "global_minimum_first_three_cycle": global_minimum[0],
        "global_minimum_first_three_target": global_minimum[1],
        "global_minimum_first_three_to_principal_ratio": global_minimum[2],
        "negative_full_action_count": receipt[
            "negative_full_action_count"],
        "full_nonpositive_without_first_three_count": receipt[
            "full_nonpositive_without_first_three_count"],
        "first_three_tail_threshold_horizon_measured": True,
        "uniform_first_three_tail_bound_proved": False,
        "eventual_first_three_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_tail_mode_only_horizon_receipt(
        start=10000, cycle_count=8, targets_per_cycle=5005,
        negative_tail_thresholds=(.3,), tolerance=1e-9):
    """Measure the q286 first-three tail without full-action recombination.

    This is a cheaper horizon scanner for the question "does the first-three
    tail appear in this cycle?"  It intentionally does not measure complement
    rescue or full-action negativity; use the cooccurrence or floor-candidate
    receipts when those quantities matter.
    """
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    negative_tail_thresholds = tuple(negative_tail_thresholds)
    if (not negative_tail_thresholds
            or any(not math.isfinite(threshold) or threshold <= 0
                   for threshold in negative_tail_thresholds)):
        raise ValueError(
            "negative_tail_thresholds must be positive finite numbers")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    period = 10010
    rows = {}
    cycle_rows = {}
    global_minimum = None
    threshold_targets = {
        threshold: []
        for threshold in negative_tail_thresholds}
    for cycle in range(cycle_count):
        cycle_start = start + cycle * period
        targets = tuple(
            cycle_start + 2 * index for index in range(targets_per_cycle))
        mode_receipt = q286_leading_singular_mode_contribution_receipt(
            targets=targets, mode_count=3, tolerance=tolerance)
        cycle_minimum = None
        cycle_threshold_counts = {
            threshold: 0
            for threshold in negative_tail_thresholds}
        for target in targets:
            first_three = math.fsum(
                row["contribution_to_principal_ratio"]
                for row in mode_receipt["rows"][target]["mode_rows"][:3])
            rows[target] = {
                "cycle": cycle,
                "first_three_modes_to_principal_ratio": first_three,
            }
            if cycle_minimum is None or first_three < cycle_minimum[1]:
                cycle_minimum = (target, first_three)
            if global_minimum is None or first_three < global_minimum[2]:
                global_minimum = (cycle, target, first_three)
            for threshold in negative_tail_thresholds:
                if first_three < -threshold:
                    cycle_threshold_counts[threshold] += 1
                    threshold_targets[threshold].append(target)
        cycle_rows[cycle] = {
            "start": targets[0],
            "end": targets[-1],
            "tested_target_count": len(targets),
            "minimum_first_three_target": cycle_minimum[0],
            "minimum_first_three_to_principal_ratio": cycle_minimum[1],
            "threshold_counts": cycle_threshold_counts,
        }

    threshold_rows = {}
    for threshold in negative_tail_thresholds:
        targets_below = tuple(threshold_targets[threshold])
        cycles_with_hits = tuple(
            cycle for cycle, row in cycle_rows.items()
            if row["threshold_counts"][threshold] > 0)
        threshold_rows[threshold] = {
            "target_count_below_negative_threshold": len(targets_below),
            "targets_below_negative_threshold": targets_below,
            "cycle_count_with_hits": len(cycles_with_hits),
            "cycles_with_hits": cycles_with_hits,
            "last_cycle_with_hit": (
                max(cycles_with_hits) if cycles_with_hits else None),
            "all_cycles_clear_negative_threshold": bool(
                not cycles_with_hits),
        }

    return {
        "arithmetic_period": period,
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "negative_tail_thresholds": negative_tail_thresholds,
        "tested_target_count": cycle_count * targets_per_cycle,
        "cycle_rows": cycle_rows,
        "threshold_rows": threshold_rows,
        "rows": rows,
        "global_minimum_first_three_cycle": global_minimum[0],
        "global_minimum_first_three_target": global_minimum[1],
        "global_minimum_first_three_to_principal_ratio": global_minimum[2],
        "first_three_tail_mode_only_horizon_measured": True,
        "complement_rescue_measured": False,
        "full_action_negativity_measured": False,
        "eventual_first_three_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


@lru_cache(maxsize=None)
def _q286_first_three_mode_linear_data(tolerance):
    """Precompute the linear q286 first-three mode functional."""
    character_receipt = q286_character_imbalance_receipt(
        targets=(10424,), top_count=120, tolerance=tolerance)
    matrix = np.zeros((10, 12), dtype=np.complex128)
    for row in character_receipt["top_coefficient_character_rows"]:
        first, second = row["label"]
        matrix[first, second] = row["coefficient"]
    coefficient_matrix = matrix[1:, 1:]
    left, singular_values, right = np.linalg.svd(
        coefficient_matrix, full_matrices=False)
    first_three_matrix = np.zeros((10, 12), dtype=np.complex128)
    for index in range(3):
        first_three_matrix[1:, 1:] += (
            singular_values[index]
            * np.outer(left[:, index], right[index, :]))

    modulus = 286
    units = tuple(unit for unit in range(modulus)
                  if math.gcd(unit, modulus) == 1)
    _, _, character_table = _unit_character_table(modulus, units)
    linear_coefficients = first_three_matrix.reshape(-1) @ character_table
    sample_row = character_receipt["rows"][10424]
    principal_mean = (
        sample_row["principal_contribution"]
        / sample_row["total_prime_pair_weight"])
    unit_index_by_residue = np.full(modulus, -1, dtype=np.int16)
    for index, unit in enumerate(units):
        unit_index_by_residue[unit] = index
    admissible_masks = {}
    admissible_counts = {}
    for target_residue in range(modulus):
        mask = np.asarray(tuple(
            math.gcd((target_residue - unit) % modulus, modulus) == 1
            for unit in units), dtype=bool)
        admissible_masks[target_residue] = mask
        admissible_counts[target_residue] = int(np.sum(mask))
    return {
        "modulus": modulus,
        "units": units,
        "linear_coefficients": linear_coefficients,
        "principal_mean": principal_mean,
        "unit_index_by_residue": unit_index_by_residue,
        "admissible_masks": admissible_masks,
        "admissible_counts": admissible_counts,
        "singular_values": tuple(float(value) for value in singular_values[:3]),
    }


def _q286_first_three_tail_fast_scan_receipt(
        start=10000, cycle_count=8, targets_per_cycle=5005,
        negative_tail_thresholds=(.3,), tolerance=1e-9,
        include_rows=True):
    """Accelerated q286 first-three tail scanner.

    This receipt measures the same first-three singular-mode ratio as
    ``q286_first_three_tail_mode_only_horizon_receipt`` but precomputes the
    q286 first-three linear functional, slices the precomputed prime table for
    central candidates, and uses NumPy residue accumulation for the
    strict-central prime-pair weights.  It still proves only the checked finite
    window.
    """
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    negative_tail_thresholds = tuple(negative_tail_thresholds)
    if (not negative_tail_thresholds
            or any(not math.isfinite(threshold) or threshold <= 0
                   for threshold in negative_tail_thresholds)):
        raise ValueError(
            "negative_tail_thresholds must be positive finite numbers")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    if type(include_rows) is not bool:
        raise ValueError("include_rows must be boolean")

    period = 10010
    maximum_target = (
        start + (cycle_count - 1) * period
        + 2 * (targets_per_cycle - 1))
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    log_values = np.zeros(maximum_target + 1, dtype=np.float64)
    prime_indices = np.nonzero(primes)[0]
    log_values[prime_indices] = np.log(prime_indices)

    data = _q286_first_three_mode_linear_data(tolerance)
    modulus = data["modulus"]
    unit_index_by_residue = data["unit_index_by_residue"]
    linear_coefficients = data["linear_coefficients"]
    principal_mean = data["principal_mean"]
    admissible_masks = data["admissible_masks"]
    admissible_counts = data["admissible_counts"]
    unit_count = len(data["units"])

    rows = {} if include_rows else None
    cycle_rows = {}
    global_minimum = None
    threshold_targets = {
        threshold: []
        for threshold in negative_tail_thresholds}
    for cycle in range(cycle_count):
        cycle_start = start + cycle * period
        targets = tuple(
            cycle_start + 2 * index for index in range(targets_per_cycle))
        cycle_minimum = None
        cycle_threshold_counts = {
            threshold: 0
            for threshold in negative_tail_thresholds}
        for target in targets:
            lower = target // 3
            upper = target - lower
            first = max(2, lower + 1)
            last = min(target, upper)
            left_index = int(np.searchsorted(
                prime_indices, first, side="left"))
            right_index = int(np.searchsorted(
                prime_indices, last, side="left"))
            prime_values = prime_indices[left_index:right_index]
            partner_values = target - prime_values
            pair_mask = primes[partner_values]
            selected_primes = prime_values[pair_mask]
            selected_partners = partner_values[pair_mask]
            residue_indices = unit_index_by_residue[
                selected_primes % modulus]
            residue_weights = np.bincount(
                residue_indices,
                weights=(
                    log_values[selected_primes]
                    * log_values[selected_partners]),
                minlength=unit_count)
            total_weight = float(np.sum(residue_weights))
            principal = principal_mean.real * total_weight
            if abs(principal) > tolerance:
                target_residue = target % modulus
                admissible_mask = admissible_masks[target_residue]
                mean_weight = (
                    total_weight / admissible_counts[target_residue])
                weight_delta = np.zeros(unit_count, dtype=np.float64)
                weight_delta[admissible_mask] = (
                    residue_weights[admissible_mask] - mean_weight)
                first_three = float(
                    (linear_coefficients @ weight_delta).real / principal)
            else:
                first_three = math.nan
            if include_rows:
                rows[target] = {
                    "cycle": cycle,
                    "first_three_modes_to_principal_ratio": first_three,
                }
            if (cycle_minimum is None
                    or first_three < cycle_minimum[1]):
                cycle_minimum = (target, first_three)
            if (global_minimum is None
                    or first_three < global_minimum[2]):
                global_minimum = (cycle, target, first_three)
            for threshold in negative_tail_thresholds:
                if first_three < -threshold:
                    cycle_threshold_counts[threshold] += 1
                    threshold_targets[threshold].append(target)
        cycle_rows[cycle] = {
            "start": targets[0],
            "end": targets[-1],
            "tested_target_count": len(targets),
            "minimum_first_three_target": cycle_minimum[0],
            "minimum_first_three_to_principal_ratio": cycle_minimum[1],
            "threshold_counts": cycle_threshold_counts,
        }

    threshold_rows = {}
    for threshold in negative_tail_thresholds:
        targets_below = tuple(threshold_targets[threshold])
        cycles_with_hits = tuple(
            cycle for cycle, row in cycle_rows.items()
            if row["threshold_counts"][threshold] > 0)
        threshold_rows[threshold] = {
            "target_count_below_negative_threshold": len(targets_below),
            "targets_below_negative_threshold": targets_below,
            "cycle_count_with_hits": len(cycles_with_hits),
            "cycles_with_hits": cycles_with_hits,
            "last_cycle_with_hit": (
                max(cycles_with_hits) if cycles_with_hits else None),
            "all_cycles_clear_negative_threshold": bool(
                not cycles_with_hits),
        }

    return {
        "arithmetic_period": period,
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "negative_tail_thresholds": negative_tail_thresholds,
        "tested_target_count": cycle_count * targets_per_cycle,
        "cycle_rows": cycle_rows,
        "threshold_rows": threshold_rows,
        "rows": rows if include_rows else {},
        "target_rows_included": include_rows,
        "global_minimum_first_three_cycle": global_minimum[0],
        "global_minimum_first_three_target": global_minimum[1],
        "global_minimum_first_three_to_principal_ratio": global_minimum[2],
        "singular_values": data["singular_values"],
        "first_three_tail_mode_only_fast_horizon_measured": True,
        "complement_rescue_measured": False,
        "full_action_negativity_measured": False,
        "eventual_first_three_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_tail_mode_only_fast_horizon_receipt(
        start=10000, cycle_count=8, targets_per_cycle=5005,
        negative_tail_thresholds=(.3,), tolerance=1e-9):
    """Accelerated q286 first-three tail scanner with per-target rows."""
    return _q286_first_three_tail_fast_scan_receipt(
        start=start, cycle_count=cycle_count,
        targets_per_cycle=targets_per_cycle,
        negative_tail_thresholds=negative_tail_thresholds,
        tolerance=tolerance, include_rows=True)


def q286_first_three_weighted_discrepancy_norm_receipt(
        start=10000, cycle_count=1, targets_per_cycle=5005,
        theorem_threshold=.2, tolerance=1e-9, include_rows=False):
    """Measure q286 first-three discrepancy norms against coefficient bounds.

    The first-three contribution is a signed dot product between the centered
    q286 coefficient vector and the centered strict-central residue weights.
    This finite diagnostic compares the actual signed value with the crude
    sup-norm and L2 Cauchy sufficient conditions.  It proves only the checked
    finite window.
    """
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    if not math.isfinite(theorem_threshold) or theorem_threshold <= 0:
        raise ValueError("theorem_threshold must be positive and finite")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    if type(include_rows) is not bool:
        raise ValueError("include_rows must be boolean")

    period = 10010
    maximum_target = (
        start + (cycle_count - 1) * period
        + 2 * (targets_per_cycle - 1))
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    log_values = np.zeros(maximum_target + 1, dtype=np.float64)
    prime_indices = np.nonzero(primes)[0]
    log_values[prime_indices] = np.log(prime_indices)

    data = _q286_first_three_mode_linear_data(tolerance)
    modulus = data["modulus"]
    unit_index_by_residue = data["unit_index_by_residue"]
    linear_coefficients = np.asarray(
        data["linear_coefficients"].real, dtype=np.float64)
    principal_mean = float(data["principal_mean"].real)
    admissible_masks = data["admissible_masks"]
    admissible_counts = data["admissible_counts"]
    unit_count = len(data["units"])

    coefficient_rows = {}
    for target_residue in range(modulus):
        admissible_mask = admissible_masks[target_residue]
        if admissible_counts[target_residue] == 0:
            coefficient_rows[target_residue] = {
                "admissible_count": 0,
                "centered_coefficient_l1": 0.0,
                "centered_coefficient_l2": 0.0,
                "linf_sufficient_relative_delta": math.inf,
                "l2_sufficient_relative_delta": math.inf,
            }
            continue
        centered_coefficients = (
            linear_coefficients[admissible_mask]
            - float(np.mean(linear_coefficients[admissible_mask])))
        centered_l1 = float(np.sum(np.abs(centered_coefficients)))
        centered_l2 = float(np.linalg.norm(centered_coefficients))
        coefficient_rows[target_residue] = {
            "admissible_count": admissible_counts[target_residue],
            "centered_coefficient_l1": centered_l1,
            "centered_coefficient_l2": centered_l2,
            "linf_sufficient_relative_delta": (
                theorem_threshold * principal_mean / centered_l1
                if centered_l1 > tolerance else math.inf),
            "l2_sufficient_relative_delta": (
                theorem_threshold * principal_mean / centered_l2
                if centered_l2 > tolerance else math.inf),
        }

    aligned_global_cycle_base = (
        (start - 10000) // period
        if (start - 10000) % period == 0 else None)
    rows = {} if include_rows else None
    tail_targets = []
    linf_certified_clear_count = 0
    l2_certified_clear_count = 0
    negative_target_count = 0
    negative_l2_utilization_thresholds = (.125, .25, .375, .5, .75)
    l2_ratio_thresholds = (1.0, 2.0, 3.0)
    negative_l2_utilization_counts = {
        threshold: 0 for threshold in negative_l2_utilization_thresholds}
    l2_ratio_exceedance_counts = {
        threshold: 0 for threshold in l2_ratio_thresholds}
    top_negative_alignment_rows = []
    minimum_first_three_row = None
    maximum_linf_ratio_row = None
    maximum_l2_ratio_row = None
    maximum_linf_relative_delta_row = None
    maximum_l2_negative_utilization_row = None
    maximum_linf_negative_utilization_row = None

    for cycle in range(cycle_count):
        cycle_start = start + cycle * period
        for target_offset in range(targets_per_cycle):
            target = cycle_start + 2 * target_offset
            lower = target // 3
            upper = target - lower
            first = max(2, lower + 1)
            last = min(target, upper)
            left_index = int(np.searchsorted(
                prime_indices, first, side="left"))
            right_index = int(np.searchsorted(
                prime_indices, last, side="left"))
            prime_values = prime_indices[left_index:right_index]
            partner_values = target - prime_values
            pair_mask = primes[partner_values]
            selected_primes = prime_values[pair_mask]
            selected_partners = partner_values[pair_mask]
            residue_indices = unit_index_by_residue[
                selected_primes % modulus]
            residue_weights = np.bincount(
                residue_indices,
                weights=(
                    log_values[selected_primes]
                    * log_values[selected_partners]),
                minlength=unit_count)
            total_weight = float(np.sum(residue_weights))
            if total_weight <= tolerance:
                continue
            target_residue = target % modulus
            admissible_mask = admissible_masks[target_residue]
            mean_weight = total_weight / admissible_counts[target_residue]
            weight_delta = np.zeros(unit_count, dtype=np.float64)
            weight_delta[admissible_mask] = (
                residue_weights[admissible_mask] - mean_weight)
            admissible_delta = weight_delta[admissible_mask]
            coefficient_row = coefficient_rows[target_residue]
            first_three = float(
                (linear_coefficients @ weight_delta)
                / (principal_mean * total_weight))
            linf_relative_delta = float(
                np.max(np.abs(admissible_delta)) / total_weight)
            l2_relative_delta = float(
                np.linalg.norm(admissible_delta) / total_weight)
            linf_bound = (
                coefficient_row["centered_coefficient_l1"]
                * linf_relative_delta / principal_mean)
            l2_bound = (
                coefficient_row["centered_coefficient_l2"]
                * l2_relative_delta / principal_mean)
            linf_ratio = (
                linf_relative_delta
                / coefficient_row["linf_sufficient_relative_delta"])
            l2_ratio = (
                l2_relative_delta
                / coefficient_row["l2_sufficient_relative_delta"])
            negative_part = max(0.0, -first_three)
            linf_negative_utilization = (
                negative_part / linf_bound if linf_bound > tolerance else 0.0)
            l2_negative_utilization = (
                negative_part / l2_bound if l2_bound > tolerance else 0.0)
            l2_alignment_cosine = (
                first_three / l2_bound if l2_bound > tolerance else math.nan)
            if linf_bound <= theorem_threshold:
                linf_certified_clear_count += 1
            if l2_bound <= theorem_threshold:
                l2_certified_clear_count += 1
            if first_three < 0:
                negative_target_count += 1
                for threshold in negative_l2_utilization_thresholds:
                    if l2_negative_utilization >= threshold:
                        negative_l2_utilization_counts[threshold] += 1
            for threshold in l2_ratio_thresholds:
                if l2_ratio > threshold:
                    l2_ratio_exceedance_counts[threshold] += 1
            if first_three < -theorem_threshold:
                tail_targets.append(target)

            row = {
                "target": target,
                "local_cycle": cycle,
                "global_cycle": (
                    aligned_global_cycle_base + cycle
                    if aligned_global_cycle_base is not None else None),
                "target_offset": target_offset,
                "target_mod_286": target_residue,
                "total_prime_pair_weight": total_weight,
                "first_three_to_principal_ratio": first_three,
                "linf_relative_delta": linf_relative_delta,
                "l2_relative_delta": l2_relative_delta,
                "linf_bound_to_principal": linf_bound,
                "l2_bound_to_principal": l2_bound,
                "linf_to_sufficient_ratio": linf_ratio,
                "l2_to_sufficient_ratio": l2_ratio,
                "l2_alignment_cosine": l2_alignment_cosine,
                "linf_negative_bound_utilization": (
                    linf_negative_utilization),
                "l2_negative_bound_utilization": l2_negative_utilization,
            }
            if first_three < 0:
                top_negative_alignment_rows.append(row)
                top_negative_alignment_rows.sort(
                    key=lambda item: item["l2_negative_bound_utilization"],
                    reverse=True)
                del top_negative_alignment_rows[10:]
            if include_rows:
                rows[target] = row
            if (minimum_first_three_row is None
                    or first_three < minimum_first_three_row[
                        "first_three_to_principal_ratio"]):
                minimum_first_three_row = row
            if (maximum_linf_ratio_row is None
                    or linf_ratio > maximum_linf_ratio_row[
                        "linf_to_sufficient_ratio"]):
                maximum_linf_ratio_row = row
            if (maximum_l2_ratio_row is None
                    or l2_ratio > maximum_l2_ratio_row[
                        "l2_to_sufficient_ratio"]):
                maximum_l2_ratio_row = row
            if (maximum_linf_relative_delta_row is None
                    or linf_relative_delta > maximum_linf_relative_delta_row[
                        "linf_relative_delta"]):
                maximum_linf_relative_delta_row = row
            if (maximum_linf_negative_utilization_row is None
                    or linf_negative_utilization
                    > maximum_linf_negative_utilization_row[
                        "linf_negative_bound_utilization"]):
                maximum_linf_negative_utilization_row = row
            if (maximum_l2_negative_utilization_row is None
                    or l2_negative_utilization
                    > maximum_l2_negative_utilization_row[
                        "l2_negative_bound_utilization"]):
                maximum_l2_negative_utilization_row = row

    linf_thresholds = tuple(
        row["linf_sufficient_relative_delta"]
        for row in coefficient_rows.values()
        if math.isfinite(row["linf_sufficient_relative_delta"]))
    l2_thresholds = tuple(
        row["l2_sufficient_relative_delta"]
        for row in coefficient_rows.values()
        if math.isfinite(row["l2_sufficient_relative_delta"]))
    return {
        "arithmetic_period": period,
        "start": start,
        "aligned_global_cycle_base": aligned_global_cycle_base,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "theorem_threshold": theorem_threshold,
        "tested_target_count": cycle_count * targets_per_cycle,
        "target_rows_included": include_rows,
        "rows": rows if include_rows else {},
        "coefficient_rows": coefficient_rows,
        "minimum_linf_sufficient_relative_delta": min(linf_thresholds),
        "maximum_linf_sufficient_relative_delta": max(linf_thresholds),
        "minimum_l2_sufficient_relative_delta": min(l2_thresholds),
        "maximum_l2_sufficient_relative_delta": max(l2_thresholds),
        "tail_target_count": len(tail_targets),
        "tail_targets": tuple(tail_targets),
        "negative_target_count": negative_target_count,
        "linf_certified_clear_count": linf_certified_clear_count,
        "l2_certified_clear_count": l2_certified_clear_count,
        "negative_l2_utilization_thresholds": (
            negative_l2_utilization_thresholds),
        "negative_l2_utilization_counts": (
            negative_l2_utilization_counts),
        "l2_ratio_thresholds": l2_ratio_thresholds,
        "l2_ratio_exceedance_counts": l2_ratio_exceedance_counts,
        "top_negative_alignment_rows": tuple(top_negative_alignment_rows),
        "minimum_first_three_row": minimum_first_three_row,
        "maximum_linf_to_sufficient_ratio_row": maximum_linf_ratio_row,
        "maximum_l2_to_sufficient_ratio_row": maximum_l2_ratio_row,
        "maximum_linf_relative_delta_row": maximum_linf_relative_delta_row,
        "maximum_linf_negative_utilization_row": (
            maximum_linf_negative_utilization_row),
        "maximum_l2_negative_utilization_row": (
            maximum_l2_negative_utilization_row),
        "first_three_weighted_discrepancy_norm_measured": True,
        "eventual_weighted_discrepancy_estimate_proved": False,
        "eventual_first_three_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_selected_first_three_alignment_receipt(
        targets=(10424, 10664, 10814, 14138, 14732, 58736, 88346,
                 125504, 448346, 1222142, 3304702, 3305200),
        theorem_threshold=.2, alignment_ceiling=.375, tolerance=1e-9):
    """Check weighted q286 alignment on an explicit selected target set.

    This finite diagnostic is for falsifying candidate alignment ceilings on
    known bad, near-bad, or hand-selected targets.  It proves no eventual
    estimate.
    """
    targets = tuple(targets)
    if (not targets or any(type(target) is not int or target < 40
                           or target % 2 for target in targets)):
        raise ValueError("targets must be nonempty even integers at least 40")
    if not math.isfinite(theorem_threshold) or theorem_threshold <= 0:
        raise ValueError("theorem_threshold must be positive and finite")
    if not math.isfinite(alignment_ceiling) or alignment_ceiling <= 0:
        raise ValueError("alignment_ceiling must be positive and finite")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    maximum_target = max(targets)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    log_values = np.zeros(maximum_target + 1, dtype=np.float64)
    prime_indices = np.nonzero(primes)[0]
    log_values[prime_indices] = np.log(prime_indices)

    data = _q286_first_three_mode_linear_data(tolerance)
    modulus = data["modulus"]
    unit_index_by_residue = data["unit_index_by_residue"]
    linear_coefficients = np.asarray(
        data["linear_coefficients"].real, dtype=np.float64)
    principal_mean = float(data["principal_mean"].real)
    admissible_masks = data["admissible_masks"]
    admissible_counts = data["admissible_counts"]
    unit_count = len(data["units"])

    coefficient_rows = {}
    for target_residue in range(modulus):
        admissible_mask = admissible_masks[target_residue]
        if admissible_counts[target_residue] == 0:
            coefficient_rows[target_residue] = {
                "admissible_count": 0,
                "centered_coefficient_l1": 0.0,
                "centered_coefficient_l2": 0.0,
                "linf_sufficient_relative_delta": math.inf,
                "l2_sufficient_relative_delta": math.inf,
            }
            continue
        centered_coefficients = (
            linear_coefficients[admissible_mask]
            - float(np.mean(linear_coefficients[admissible_mask])))
        centered_l1 = float(np.sum(np.abs(centered_coefficients)))
        centered_l2 = float(np.linalg.norm(centered_coefficients))
        coefficient_rows[target_residue] = {
            "admissible_count": admissible_counts[target_residue],
            "centered_coefficient_l1": centered_l1,
            "centered_coefficient_l2": centered_l2,
            "linf_sufficient_relative_delta": (
                theorem_threshold * principal_mean / centered_l1
                if centered_l1 > tolerance else math.inf),
            "l2_sufficient_relative_delta": (
                theorem_threshold * principal_mean / centered_l2
                if centered_l2 > tolerance else math.inf),
        }

    target_rows = {}
    tail_targets = []
    negative_targets = []
    alignment_ceiling_violations = []
    maximum_negative_alignment_row = None
    maximum_l2_ratio_row = None
    for target in targets:
        lower = target // 3
        upper = target - lower
        first = max(2, lower + 1)
        last = min(target, upper)
        left_index = int(np.searchsorted(
            prime_indices, first, side="left"))
        right_index = int(np.searchsorted(
            prime_indices, last, side="left"))
        prime_values = prime_indices[left_index:right_index]
        partner_values = target - prime_values
        pair_mask = primes[partner_values]
        selected_primes = prime_values[pair_mask]
        selected_partners = partner_values[pair_mask]
        residue_indices = unit_index_by_residue[
            selected_primes % modulus]
        residue_weights = np.bincount(
            residue_indices,
            weights=(
                log_values[selected_primes]
                * log_values[selected_partners]),
            minlength=unit_count)
        total_weight = float(np.sum(residue_weights))
        target_residue = target % modulus
        admissible_mask = admissible_masks[target_residue]
        mean_weight = total_weight / admissible_counts[target_residue]
        weight_delta = np.zeros(unit_count, dtype=np.float64)
        weight_delta[admissible_mask] = (
            residue_weights[admissible_mask] - mean_weight)
        admissible_delta = weight_delta[admissible_mask]
        coefficient_row = coefficient_rows[target_residue]
        first_three = float(
            (linear_coefficients @ weight_delta)
            / (principal_mean * total_weight))
        linf_relative_delta = float(
            np.max(np.abs(admissible_delta)) / total_weight)
        l2_relative_delta = float(
            np.linalg.norm(admissible_delta) / total_weight)
        linf_bound = (
            coefficient_row["centered_coefficient_l1"]
            * linf_relative_delta / principal_mean)
        l2_bound = (
            coefficient_row["centered_coefficient_l2"]
            * l2_relative_delta / principal_mean)
        linf_ratio = (
            linf_relative_delta
            / coefficient_row["linf_sufficient_relative_delta"])
        l2_ratio = (
            l2_relative_delta
            / coefficient_row["l2_sufficient_relative_delta"])
        negative_part = max(0.0, -first_three)
        linf_negative_utilization = (
            negative_part / linf_bound if linf_bound > tolerance else 0.0)
        l2_negative_utilization = (
            negative_part / l2_bound if l2_bound > tolerance else 0.0)
        row = {
            "target": target,
            "local_cycle": 0,
            "global_cycle": None,
            "target_offset": 0,
            "target_mod_286": target_residue,
            "total_prime_pair_weight": total_weight,
            "first_three_to_principal_ratio": first_three,
            "linf_relative_delta": linf_relative_delta,
            "l2_relative_delta": l2_relative_delta,
            "linf_bound_to_principal": linf_bound,
            "l2_bound_to_principal": l2_bound,
            "linf_to_sufficient_ratio": linf_ratio,
            "l2_to_sufficient_ratio": l2_ratio,
            "l2_alignment_cosine": (
                first_three / l2_bound if l2_bound > tolerance else math.nan),
            "linf_negative_bound_utilization": (
                linf_negative_utilization),
            "l2_negative_bound_utilization": l2_negative_utilization,
        }
        target_rows[target] = row
        if row["first_three_to_principal_ratio"] < -theorem_threshold:
            tail_targets.append(target)
        if row["first_three_to_principal_ratio"] < 0:
            negative_targets.append(target)
        if row["l2_negative_bound_utilization"] >= alignment_ceiling:
            alignment_ceiling_violations.append(target)
        if (maximum_negative_alignment_row is None
                or row["l2_negative_bound_utilization"]
                > maximum_negative_alignment_row[
                    "l2_negative_bound_utilization"]):
            maximum_negative_alignment_row = row
        if (maximum_l2_ratio_row is None
                or row["l2_to_sufficient_ratio"]
                > maximum_l2_ratio_row["l2_to_sufficient_ratio"]):
            maximum_l2_ratio_row = row

    return {
        "targets": targets,
        "tested_target_count": len(targets),
        "theorem_threshold": theorem_threshold,
        "alignment_ceiling": alignment_ceiling,
        "target_rows": target_rows,
        "tail_target_count": len(tail_targets),
        "tail_targets": tuple(tail_targets),
        "negative_target_count": len(negative_targets),
        "negative_targets": tuple(negative_targets),
        "alignment_ceiling_violation_count": (
            len(alignment_ceiling_violations)),
        "alignment_ceiling_violation_targets": tuple(
            alignment_ceiling_violations),
        "maximum_negative_alignment_row": maximum_negative_alignment_row,
        "maximum_l2_to_sufficient_ratio_row": maximum_l2_ratio_row,
        "selected_first_three_alignment_measured": True,
        "eventual_alignment_ceiling_proved": False,
        "eventual_first_three_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_tail_alignment_window_receipt(
        start=10000, cycle_count=8, targets_per_cycle=5005,
        tail_threshold=.3, theorem_threshold=.2, alignment_ceiling=.375,
        tolerance=1e-9):
    """Find q286 first-three tail targets, then test alignment on them.

    This finite diagnostic focuses the weighted-alignment test on the sparse
    tail targets found by the validated fast scanner.  It proves only the
    checked finite window.
    """
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    if not math.isfinite(tail_threshold) or tail_threshold <= 0:
        raise ValueError("tail_threshold must be positive and finite")
    if not math.isfinite(theorem_threshold) or theorem_threshold <= 0:
        raise ValueError("theorem_threshold must be positive and finite")
    if not math.isfinite(alignment_ceiling) or alignment_ceiling <= 0:
        raise ValueError("alignment_ceiling must be positive and finite")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    horizon = _q286_first_three_tail_fast_scan_receipt(
        start=start, cycle_count=cycle_count,
        targets_per_cycle=targets_per_cycle,
        negative_tail_thresholds=(tail_threshold,),
        tolerance=tolerance, include_rows=False)
    tail_targets = horizon["threshold_rows"][tail_threshold][
        "targets_below_negative_threshold"]
    if tail_targets:
        alignment = q286_selected_first_three_alignment_receipt(
            targets=tail_targets, theorem_threshold=theorem_threshold,
            alignment_ceiling=alignment_ceiling, tolerance=tolerance)
    else:
        alignment = {
            "targets": (),
            "tested_target_count": 0,
            "theorem_threshold": theorem_threshold,
            "alignment_ceiling": alignment_ceiling,
            "target_rows": {},
            "tail_target_count": 0,
            "tail_targets": (),
            "negative_target_count": 0,
            "negative_targets": (),
            "alignment_ceiling_violation_count": 0,
            "alignment_ceiling_violation_targets": (),
            "maximum_negative_alignment_row": None,
            "maximum_l2_to_sufficient_ratio_row": None,
            "selected_first_three_alignment_measured": True,
            "eventual_alignment_ceiling_proved": False,
            "eventual_first_three_tail_bound_proved": False,
            "signed_prime_correlation_estimate_proved": False,
            "goldbach_proved": False,
        }

    return {
        "arithmetic_period": horizon["arithmetic_period"],
        "start": start,
        "aligned_global_cycle_base": (
            (start - 10000) // horizon["arithmetic_period"]
            if (start - 10000) % horizon["arithmetic_period"] == 0
            else None),
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "tail_threshold": tail_threshold,
        "theorem_threshold": theorem_threshold,
        "alignment_ceiling": alignment_ceiling,
        "tested_target_count": horizon["tested_target_count"],
        "tail_target_count": len(tail_targets),
        "tail_targets": tail_targets,
        "tail_cycles": horizon["threshold_rows"][tail_threshold][
            "cycles_with_hits"],
        "source_fast_horizon_receipt": horizon,
        "alignment_receipt": alignment,
        "alignment_ceiling_violation_count": (
            alignment["alignment_ceiling_violation_count"]),
        "alignment_ceiling_violation_targets": (
            alignment["alignment_ceiling_violation_targets"]),
        "maximum_negative_alignment_row": (
            alignment["maximum_negative_alignment_row"]),
        "first_three_tail_alignment_window_measured": True,
        "eventual_alignment_ceiling_proved": False,
        "eventual_first_three_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_selected_alignment_complement_certificate_receipt(
        targets=(14138, 70526, 1379072, 1426262, 3305200),
        theorem_threshold=.2, alignment_ceiling=.4, tolerance=1e-9):
    """Compare complement margins with the q286 alignment-bound target.

    If an alignment theorem gave
    ``first_three >= -alignment_ceiling * l2_bound``, then targets with
    ``complement > alignment_ceiling * l2_bound`` would be positive after
    recombination.  This finite diagnostic measures that sufficient condition
    on selected targets and records failures as theorem-shaping obstructions.
    """
    targets = tuple(targets)
    if (not targets or any(type(target) is not int or target < 40
                           or target % 2 for target in targets)):
        raise ValueError("targets must be nonempty even integers at least 40")
    if not math.isfinite(theorem_threshold) or theorem_threshold <= 0:
        raise ValueError("theorem_threshold must be positive and finite")
    if not math.isfinite(alignment_ceiling) or alignment_ceiling <= 0:
        raise ValueError("alignment_ceiling must be positive and finite")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    alignment = q286_selected_first_three_alignment_receipt(
        targets=targets, theorem_threshold=theorem_threshold,
        alignment_ceiling=alignment_ceiling, tolerance=tolerance)
    lower = q286_first_two_mode_lower_tail_receipt(
        selected_targets=targets, targets_per_cycle=len(targets),
        tolerance=tolerance)

    target_rows = {}
    certified_targets = []
    failed_targets = []
    actual_negative_targets = []
    worst_certificate_margin_row = None
    for target in targets:
        alignment_row = alignment["target_rows"][target]
        lower_row = lower["rows"][target]
        first_three = lower_row["first_three_modes_to_principal_ratio"]
        if abs(first_three - alignment_row[
                "first_three_to_principal_ratio"]) > 1e-8:
            raise ArithmeticError("alignment/lower first-three mismatch")
        complement = lower_row["full_without_first_three_to_principal_ratio"]
        full = lower_row["full_action_to_principal_ratio"]
        recombined = first_three + complement
        if abs(recombined - full) > 1e-8:
            raise ArithmeticError("first-three/complement recombination failed")
        alignment_bound = (
            alignment_ceiling * alignment_row["l2_bound_to_principal"])
        certificate_margin = complement - alignment_bound
        row = {
            "target": target,
            "first_three_to_principal_ratio": first_three,
            "complement_to_principal_ratio": complement,
            "full_action_to_principal_ratio": full,
            "l2_bound_to_principal": alignment_row[
                "l2_bound_to_principal"],
            "alignment_ceiling_bound_to_principal": alignment_bound,
            "certificate_margin_to_principal": certificate_margin,
            "certified_positive_by_alignment_complement": bool(
                certificate_margin > tolerance),
            "actual_full_action_positive": bool(full > tolerance),
            "l2_negative_bound_utilization": alignment_row[
                "l2_negative_bound_utilization"],
            "l2_to_sufficient_ratio": alignment_row[
                "l2_to_sufficient_ratio"],
        }
        target_rows[target] = row
        if row["certified_positive_by_alignment_complement"]:
            certified_targets.append(target)
        else:
            failed_targets.append(target)
        if not row["actual_full_action_positive"]:
            actual_negative_targets.append(target)
        if (worst_certificate_margin_row is None
                or certificate_margin
                < worst_certificate_margin_row[
                    "certificate_margin_to_principal"]):
            worst_certificate_margin_row = row

    return {
        "targets": targets,
        "tested_target_count": len(targets),
        "theorem_threshold": theorem_threshold,
        "alignment_ceiling": alignment_ceiling,
        "target_rows": target_rows,
        "certified_target_count": len(certified_targets),
        "certified_targets": tuple(certified_targets),
        "failed_certificate_target_count": len(failed_targets),
        "failed_certificate_targets": tuple(failed_targets),
        "actual_negative_target_count": len(actual_negative_targets),
        "actual_negative_targets": tuple(actual_negative_targets),
        "worst_certificate_margin_row": worst_certificate_margin_row,
        "source_alignment_receipt": alignment,
        "source_lower_tail_receipt": lower,
        "alignment_complement_certificate_measured": True,
        "eventual_alignment_ceiling_proved": False,
        "eventual_complement_bound_proved": False,
        "eventual_first_three_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_tail_hit_residue_profile_receipt(
        start=10000, cycle_count=8, targets_per_cycle=5005,
        negative_tail_thresholds=(.3,), tolerance=1e-9):
    """Classify q286 first-three tail hits by residue and cycle position.

    This is a finite diagnostic over the validated fast mode-only scanner.  It
    does not add complement rescue information; use the rescue-floor receipt on
    nonempty cycles when full recombination matters.
    """
    horizon = q286_first_three_tail_mode_only_fast_horizon_receipt(
        start=start, cycle_count=cycle_count,
        targets_per_cycle=targets_per_cycle,
        negative_tail_thresholds=negative_tail_thresholds,
        tolerance=tolerance)
    period = horizon["arithmetic_period"]
    aligned_global_cycle_base = (
        (start - 10000) // period
        if (start - 10000) % period == 0 else None)

    threshold_profiles = {}
    for threshold in horizon["negative_tail_thresholds"]:
        tail_targets = horizon["threshold_rows"][threshold][
            "targets_below_negative_threshold"]
        residue_counts_mod_286 = {}
        residue_counts_mod_10010 = {}
        offset_counts = {}
        cycle_counts = {}
        cycle_mod_11_counts = {}
        cycle_mod_13_counts = {}
        hit_rows = []
        for target in tail_targets:
            local_cycle = horizon["rows"][target]["cycle"]
            cycle_start = start + local_cycle * period
            target_offset = (target - cycle_start) // 2
            global_cycle = (
                aligned_global_cycle_base + local_cycle
                if aligned_global_cycle_base is not None else None)
            first_three = horizon["rows"][target][
                "first_three_modes_to_principal_ratio"]
            residue_mod_286 = target % 286
            residue_mod_10010 = target % period
            for counts, key in (
                    (residue_counts_mod_286, residue_mod_286),
                    (residue_counts_mod_10010, residue_mod_10010),
                    (offset_counts, target_offset),
                    (cycle_counts, local_cycle)):
                counts[key] = counts.get(key, 0) + 1
            if global_cycle is not None:
                cycle_mod_11 = global_cycle % 11
                cycle_mod_13 = global_cycle % 13
                cycle_mod_11_counts[cycle_mod_11] = (
                    cycle_mod_11_counts.get(cycle_mod_11, 0) + 1)
                cycle_mod_13_counts[cycle_mod_13] = (
                    cycle_mod_13_counts.get(cycle_mod_13, 0) + 1)
            else:
                cycle_mod_11 = None
                cycle_mod_13 = None
            hit_rows.append({
                "target": target,
                "local_cycle": local_cycle,
                "global_cycle": global_cycle,
                "cycle_mod_11": cycle_mod_11,
                "cycle_mod_13": cycle_mod_13,
                "target_offset": target_offset,
                "target_mod_286": residue_mod_286,
                "target_mod_10010": residue_mod_10010,
                "first_three_modes_to_principal_ratio": first_three,
            })

        repeated_mod_286 = tuple(
            residue for residue, count in sorted(
                residue_counts_mod_286.items())
            if count > 1)
        repeated_mod_10010 = tuple(
            residue for residue, count in sorted(
                residue_counts_mod_10010.items())
            if count > 1)
        threshold_profiles[threshold] = {
            "tail_target_count": len(tail_targets),
            "tail_targets": tail_targets,
            "hit_rows": tuple(hit_rows),
            "cycle_counts": dict(sorted(cycle_counts.items())),
            "cycle_mod_11_counts": dict(sorted(cycle_mod_11_counts.items())),
            "cycle_mod_13_counts": dict(sorted(cycle_mod_13_counts.items())),
            "target_offset_counts": dict(sorted(offset_counts.items())),
            "residue_counts_mod_286": dict(sorted(
                residue_counts_mod_286.items())),
            "residues_with_multiple_hits_mod_286": repeated_mod_286,
            "residue_counts_mod_10010": dict(sorted(
                residue_counts_mod_10010.items())),
            "residues_with_multiple_hits_mod_10010": repeated_mod_10010,
            "single_residue_mod_286_explains_all_hits": bool(
                len(residue_counts_mod_286) == 1 if tail_targets else False),
            "single_period_residue_explains_all_hits": bool(
                len(residue_counts_mod_10010) == 1
                if tail_targets else False),
        }

    return {
        "arithmetic_period": period,
        "start": start,
        "aligned_global_cycle_base": aligned_global_cycle_base,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "negative_tail_thresholds": horizon["negative_tail_thresholds"],
        "tested_target_count": horizon["tested_target_count"],
        "threshold_profiles": threshold_profiles,
        "global_minimum_first_three_cycle": (
            horizon["global_minimum_first_three_cycle"]),
        "global_minimum_first_three_target": (
            horizon["global_minimum_first_three_target"]),
        "global_minimum_first_three_to_principal_ratio": (
            horizon["global_minimum_first_three_to_principal_ratio"]),
        "source_fast_horizon_receipt": horizon,
        "first_three_tail_hit_residue_profile_measured": True,
        "complement_rescue_measured": False,
        "full_action_negativity_measured": False,
        "eventual_first_three_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_tail_threshold_ladder_receipt(
        start=10000, cycle_count=32, targets_per_cycle=5005,
        negative_tail_thresholds=(.2, .25, .275, .3), block_size=32,
        tolerance=1e-9):
    """Summarize q286 first-three tail counts across nested thresholds.

    This finite diagnostic asks whether tail disappearance is just a chosen
    threshold artifact or part of a wider envelope.  It uses the validated fast
    mode-only scanner and proves only the checked finite window.
    """
    if type(block_size) is not int or block_size < 1:
        raise ValueError("block_size must be a positive integer")
    horizon = _q286_first_three_tail_fast_scan_receipt(
        start=start, cycle_count=cycle_count,
        targets_per_cycle=targets_per_cycle,
        negative_tail_thresholds=negative_tail_thresholds,
        tolerance=tolerance, include_rows=False)
    period = horizon["arithmetic_period"]
    aligned_global_cycle_base = (
        (start - 10000) // period
        if (start - 10000) % period == 0 else None)

    threshold_rows = {}
    cleared_thresholds = []
    for threshold in horizon["negative_tail_thresholds"]:
        row = horizon["threshold_rows"][threshold]
        local_cycles = row["cycles_with_hits"]
        global_cycles = (
            tuple(aligned_global_cycle_base + cycle
                  for cycle in local_cycles)
            if aligned_global_cycle_base is not None else None)
        if row["target_count_below_negative_threshold"] == 0:
            cleared_thresholds.append(threshold)
        threshold_rows[threshold] = {
            "tail_target_count": row[
                "target_count_below_negative_threshold"],
            "local_cycles_with_hits": local_cycles,
            "global_cycles_with_hits": global_cycles,
            "last_local_cycle_with_hit": row["last_cycle_with_hit"],
            "last_global_cycle_with_hit": (
                (aligned_global_cycle_base + row["last_cycle_with_hit"])
                if (aligned_global_cycle_base is not None
                    and row["last_cycle_with_hit"] is not None)
                else None),
            "all_cycles_clear_negative_threshold": row[
                "all_cycles_clear_negative_threshold"],
        }

    block_rows = {}
    for block_start in range(0, cycle_count, block_size):
        block_end = min(cycle_count, block_start + block_size) - 1
        cycle_items = tuple(
            (cycle, horizon["cycle_rows"][cycle])
            for cycle in range(block_start, block_end + 1))
        block_minimum_cycle, block_minimum_row = min(
            cycle_items,
            key=lambda item: item[1][
                "minimum_first_three_to_principal_ratio"])
        threshold_counts = {
            threshold: sum(
                row["threshold_counts"][threshold]
                for _, row in cycle_items)
            for threshold in horizon["negative_tail_thresholds"]}
        local_cycles_by_threshold = {
            threshold: tuple(
                cycle for cycle, row in cycle_items
                if row["threshold_counts"][threshold] > 0)
            for threshold in horizon["negative_tail_thresholds"]}
        global_cycles_by_threshold = (
            {
                threshold: tuple(
                    aligned_global_cycle_base + cycle
                    for cycle in local_cycles)
                for threshold, local_cycles
                in local_cycles_by_threshold.items()
            }
            if aligned_global_cycle_base is not None else None)
        block_rows[block_start // block_size] = {
            "local_cycle_range": (block_start, block_end),
            "global_cycle_range": (
                (aligned_global_cycle_base + block_start,
                 aligned_global_cycle_base + block_end)
                if aligned_global_cycle_base is not None else None),
            "threshold_counts": threshold_counts,
            "local_cycles_by_threshold": local_cycles_by_threshold,
            "global_cycles_by_threshold": global_cycles_by_threshold,
            "minimum_first_three_local_cycle": block_minimum_cycle,
            "minimum_first_three_global_cycle": (
                aligned_global_cycle_base + block_minimum_cycle
                if aligned_global_cycle_base is not None else None),
            "minimum_first_three_target": block_minimum_row[
                "minimum_first_three_target"],
            "minimum_first_three_to_principal_ratio": block_minimum_row[
                "minimum_first_three_to_principal_ratio"],
        }

    strongest_cleared_threshold = (
        min(cleared_thresholds) if cleared_thresholds else None)
    return {
        "arithmetic_period": period,
        "start": start,
        "aligned_global_cycle_base": aligned_global_cycle_base,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "negative_tail_thresholds": horizon["negative_tail_thresholds"],
        "block_size": block_size,
        "tested_target_count": horizon["tested_target_count"],
        "threshold_rows": threshold_rows,
        "cleared_thresholds": tuple(cleared_thresholds),
        "strongest_cleared_threshold": strongest_cleared_threshold,
        "block_rows": block_rows,
        "global_minimum_first_three_cycle": (
            horizon["global_minimum_first_three_cycle"]),
        "global_minimum_first_three_target": (
            horizon["global_minimum_first_three_target"]),
        "global_minimum_first_three_to_principal_ratio": (
            horizon["global_minimum_first_three_to_principal_ratio"]),
        "source_fast_horizon_receipt": horizon,
        "first_three_tail_threshold_ladder_measured": True,
        "eventual_first_three_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_complement_cooccurrence_receipt(
        start=10000, cycle_count=8, targets_per_cycle=5005,
        negative_tail_thresholds=(.3, .5, .75, 1.0), tolerance=1e-9):
    """Measure co-occurrence of q286 first-three tail and complement.

    Independent lower envelopes are too weak: the first-three q286 tail falls
    below negative thresholds long after the post-first-three complement is
    positive.  This receipt measures the pointwise recombination
    ``first_three + complement`` and records how often large negative tails are
    rescued by correspondingly large complement values.
    """
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    negative_tail_thresholds = tuple(negative_tail_thresholds)
    if (not negative_tail_thresholds
            or any(not math.isfinite(threshold) or threshold <= 0
                   for threshold in negative_tail_thresholds)):
        raise ValueError(
            "negative_tail_thresholds must be positive finite numbers")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    lower = q286_first_two_mode_lower_tail_receipt(
        start=start, cycle_count=cycle_count,
        targets_per_cycle=targets_per_cycle, tolerance=tolerance)
    rows = {}
    first_three_values = []
    complement_values = []
    recombined_values = []
    negative_full_targets = []
    rescued_negative_tail_targets = []
    for target in sorted(lower["rows"]):
        row = lower["rows"][target]
        first_three = row["first_three_modes_to_principal_ratio"]
        complement = row["full_without_first_three_to_principal_ratio"]
        recombined = first_three + complement
        full = row["full_action_to_principal_ratio"]
        if abs(recombined - full) > 1e-8:
            raise ArithmeticError("first-three/complement recombination failed")
        first_three_values.append(first_three)
        complement_values.append(complement)
        recombined_values.append(recombined)
        if recombined <= tolerance:
            negative_full_targets.append(target)
        if first_three < -negative_tail_thresholds[0] and recombined > tolerance:
            rescued_negative_tail_targets.append(target)
        rows[target] = {
            "cycle": row["cycle"],
            "first_three_to_principal_ratio": first_three,
            "complement_to_principal_ratio": complement,
            "recombined_to_principal_ratio": recombined,
            "full_action_to_principal_ratio": full,
            "complement_minus_negative_tail_to_principal_ratio": recombined,
            "negative_full_action": bool(recombined <= tolerance),
        }

    def dot(left, right):
        return math.fsum(a * b for a, b in zip(left, right))

    def mean(values):
        return math.fsum(values) / len(values)

    def centered(values):
        average = mean(values)
        return tuple(value - average for value in values)

    def corr(left, right):
        left_centered = centered(left)
        right_centered = centered(right)
        denominator = math.sqrt(
            dot(left_centered, left_centered)
            * dot(right_centered, right_centered))
        return dot(left_centered, right_centered) / denominator if denominator else math.nan

    threshold_rows = {}
    for threshold in negative_tail_thresholds:
        tail_targets = tuple(
            target for target, row in rows.items()
            if row["first_three_to_principal_ratio"] < -threshold)
        negative_tail_and_negative_full = tuple(
            target for target in tail_targets
            if rows[target]["negative_full_action"])
        rescued_targets = tuple(
            target for target in tail_targets
            if not rows[target]["negative_full_action"])
        if tail_targets:
            min_complement_target = min(
                tail_targets,
                key=lambda target: rows[target][
                    "complement_to_principal_ratio"])
            min_recombined_target = min(
                tail_targets,
                key=lambda target: rows[target][
                    "recombined_to_principal_ratio"])
            mean_complement = mean(tuple(
                rows[target]["complement_to_principal_ratio"]
                for target in tail_targets))
            mean_recombined = mean(tuple(
                rows[target]["recombined_to_principal_ratio"]
                for target in tail_targets))
        else:
            min_complement_target = None
            min_recombined_target = None
            mean_complement = math.nan
            mean_recombined = math.nan
        threshold_rows[threshold] = {
            "tail_target_count": len(tail_targets),
            "tail_targets": tail_targets,
            "negative_full_count_inside_tail": len(
                negative_tail_and_negative_full),
            "rescued_tail_target_count": len(rescued_targets),
            "rescued_tail_targets": rescued_targets,
            "rescued_tail_fraction": (
                len(rescued_targets) / len(tail_targets)
                if tail_targets else math.nan),
            "minimum_complement_target_inside_tail": min_complement_target,
            "minimum_complement_inside_tail": (
                rows[min_complement_target]["complement_to_principal_ratio"]
                if min_complement_target is not None else math.nan),
            "minimum_recombined_target_inside_tail": min_recombined_target,
            "minimum_recombined_inside_tail": (
                rows[min_recombined_target]["recombined_to_principal_ratio"]
                if min_recombined_target is not None else math.nan),
            "mean_complement_inside_tail": mean_complement,
            "mean_recombined_inside_tail": mean_recombined,
            "negative_tail_and_negative_full_targets": (
                negative_tail_and_negative_full),
        }

    minimum_full_target = min(
        rows, key=lambda target: rows[target][
            "full_action_to_principal_ratio"])
    minimum_recombined_target = min(
        rows, key=lambda target: rows[target][
            "recombined_to_principal_ratio"])
    minimum_complement_target = min(
        rows, key=lambda target: rows[target][
            "complement_to_principal_ratio"])
    minimum_first_three_target = min(
        rows, key=lambda target: rows[target][
            "first_three_to_principal_ratio"])
    return {
        "arithmetic_period": lower["arithmetic_period"],
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "negative_tail_thresholds": negative_tail_thresholds,
        "tested_target_count": lower["tested_target_count"],
        "rows": rows,
        "threshold_rows": threshold_rows,
        "negative_full_action_count": len(negative_full_targets),
        "negative_full_action_targets": tuple(negative_full_targets),
        "rescued_negative_tail_target_count_at_first_threshold": len(
            rescued_negative_tail_targets),
        "minimum_full_action_target": minimum_full_target,
        "minimum_full_action_to_principal_ratio": rows[
            minimum_full_target]["full_action_to_principal_ratio"],
        "minimum_recombined_margin_target": minimum_recombined_target,
        "minimum_recombined_margin_to_principal_ratio": rows[
            minimum_recombined_target]["recombined_to_principal_ratio"],
        "minimum_complement_target": minimum_complement_target,
        "minimum_complement_to_principal_ratio": rows[
            minimum_complement_target]["complement_to_principal_ratio"],
        "minimum_first_three_target": minimum_first_three_target,
        "minimum_first_three_to_principal_ratio": rows[
            minimum_first_three_target]["first_three_to_principal_ratio"],
        "first_three_complement_centered_correlation": corr(
            first_three_values, complement_values),
        "first_three_full_centered_correlation": corr(
            first_three_values, recombined_values),
        "complement_full_centered_correlation": corr(
            complement_values, recombined_values),
        "first_three_complement_cooccurrence_measured": True,
        "pointwise_cooccurrence_estimate_proved": False,
        "eventual_cooccurrence_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_nonrescued_first_three_tail_classification_receipt(
        start=10000, cycle_count=8, targets_per_cycle=5005,
        threshold=.3, lift_offsets=(0, 1), tolerance=1e-9):
    """Classify non-rescued targets inside a negative first-three tail.

    A target is non-rescued here when the first three q286 modes are below
    ``-threshold`` and the full recombined action is still nonpositive.  The
    receipt records cycle/residue/severity structure and checks selected
    same-residue period lifts for persistence of the failure.
    """
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    if not math.isfinite(threshold) or threshold <= 0:
        raise ValueError("threshold must be finite and positive")
    lift_offsets = tuple(dict.fromkeys(lift_offsets))
    if (not lift_offsets or any(type(lift) is not int or lift < 0
                                for lift in lift_offsets)):
        raise ValueError("lift_offsets must be nonnegative integers")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    cooccurrence = q286_first_three_complement_cooccurrence_receipt(
        start=start, cycle_count=cycle_count,
        targets_per_cycle=targets_per_cycle,
        negative_tail_thresholds=(threshold,), tolerance=tolerance)
    threshold_row = cooccurrence["threshold_rows"][threshold]
    nonrescued_targets = tuple(
        threshold_row["negative_tail_and_negative_full_targets"])
    period = cooccurrence["arithmetic_period"]

    cycle_counts = {cycle: 0 for cycle in range(cycle_count)}
    residue_counts = {}
    severity_counts = {
        "below_.5": 0,
        "below_.75": 0,
        "below_1.0": 0,
    }
    target_rows = {}
    for target in nonrescued_targets:
        row = cooccurrence["rows"][target]
        cycle = row["cycle"]
        residue = target % period
        cycle_counts[cycle] = cycle_counts.get(cycle, 0) + 1
        residue_counts[residue] = residue_counts.get(residue, 0) + 1
        first_three = row["first_three_to_principal_ratio"]
        if first_three < -.5:
            severity_counts["below_.5"] += 1
        if first_three < -.75:
            severity_counts["below_.75"] += 1
        if first_three < -1.0:
            severity_counts["below_1.0"] += 1
        target_rows[target] = {
            "cycle": cycle,
            "residue_mod_period": residue,
            "first_three_to_principal_ratio": first_three,
            "complement_to_principal_ratio": row[
                "complement_to_principal_ratio"],
            "full_action_to_principal_ratio": row[
                "full_action_to_principal_ratio"],
        }

    residues_with_multiple_hits = tuple(sorted(
        residue for residue, count in residue_counts.items() if count > 1))
    max_hits_per_residue = max(residue_counts.values()) if residue_counts else 0

    lift_rows = {}
    lift_negative_counts = {lift: 0 for lift in lift_offsets}
    if nonrescued_targets:
        selected_lift_targets = tuple(
            target + lift * period
            for target in nonrescued_targets for lift in lift_offsets)
        lift_receipt = q286_first_two_mode_lower_tail_receipt(
            selected_targets=selected_lift_targets, tolerance=tolerance)
        for target in nonrescued_targets:
            rows_by_lift = {}
            for lift in lift_offsets:
                lifted_target = target + lift * period
                row = lift_receipt["rows"][lifted_target]
                first_three = row["first_three_modes_to_principal_ratio"]
                complement = row[
                    "full_without_first_three_to_principal_ratio"]
                full = row["full_action_to_principal_ratio"]
                rows_by_lift[lift] = {
                    "target": lifted_target,
                    "first_three_to_principal_ratio": first_three,
                    "complement_to_principal_ratio": complement,
                    "full_action_to_principal_ratio": full,
                    "negative_full_action": bool(full <= tolerance),
                    "tail_below_threshold": bool(first_three < -threshold),
                }
                if full <= tolerance:
                    lift_negative_counts[lift] += 1
            first_positive_lift = next((
                lift for lift in lift_offsets
                if rows_by_lift[lift]["full_action_to_principal_ratio"]
                > tolerance), None)
            lift_rows[target] = {
                "lift_rows": rows_by_lift,
                "first_positive_lift": first_positive_lift,
                "negative_full_lifts": tuple(
                    lift for lift in lift_offsets
                    if rows_by_lift[lift]["negative_full_action"]),
                "tail_below_threshold_lifts": tuple(
                    lift for lift in lift_offsets
                    if rows_by_lift[lift]["tail_below_threshold"]),
            }
    else:
        selected_lift_targets = tuple()

    worst_targets = tuple(
        target for target, _ in sorted(
            ((target, row["full_action_to_principal_ratio"])
             for target, row in target_rows.items()),
            key=lambda item: item[1])[:10])
    maximum_first_positive_lift = max((
        row["first_positive_lift"] for row in lift_rows.values()
        if row["first_positive_lift"] is not None), default=None)
    return {
        "arithmetic_period": period,
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "threshold": threshold,
        "lift_offsets": lift_offsets,
        "tested_target_count": cooccurrence["tested_target_count"],
        "tail_target_count": threshold_row["tail_target_count"],
        "nonrescued_target_count": len(nonrescued_targets),
        "rescued_tail_target_count": threshold_row[
            "rescued_tail_target_count"],
        "rescue_fraction": threshold_row["rescued_tail_fraction"],
        "nonrescued_targets": nonrescued_targets,
        "target_rows": target_rows,
        "cycle_counts": cycle_counts,
        "residue_counts": residue_counts,
        "residues_with_multiple_hits": residues_with_multiple_hits,
        "max_hits_per_residue": max_hits_per_residue,
        "severity_counts": severity_counts,
        "worst_nonrescued_targets": worst_targets,
        "selected_lift_targets": selected_lift_targets,
        "lift_rows": lift_rows,
        "lift_negative_counts_by_offset": lift_negative_counts,
        "maximum_first_positive_lift": maximum_first_positive_lift,
        "all_nonrescued_clear_by_first_positive_lift": bool(
            all(row["first_positive_lift"] is not None
                for row in lift_rows.values()) if lift_rows else True),
        "nonrescued_first_three_tail_classification_measured": True,
        "nonrescued_classification_theorem_proved": False,
        "eventual_lift_clearance_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_nonrescued_first_three_tail_cycle_horizon_receipt(
        start=10000, cycle_count=8, targets_per_cycle=5005,
        threshold=.3, tolerance=1e-9):
    """Scan cycles for non-rescued first-three tail recurrence.

    This receipt isolates the finite horizon question suggested by the
    non-rescued classifier: after which checked cycle does every target with
    ``first_three < -threshold`` have positive recombined full action?
    It is a finite horizon diagnostic, not an eventual theorem.
    """
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    if not math.isfinite(threshold) or threshold <= 0:
        raise ValueError("threshold must be finite and positive")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    period = None
    cycle_rows = {}
    total_negative_full = 0
    total_tail_targets = 0
    total_nonrescued = 0
    global_minimum_full = None
    global_minimum_tail_recombined = None
    for cycle in range(cycle_count):
        cycle_start = start if period is None else start + cycle * period
        receipt = q286_first_three_complement_cooccurrence_receipt(
            start=cycle_start, cycle_count=1,
            targets_per_cycle=targets_per_cycle,
            negative_tail_thresholds=(threshold,), tolerance=tolerance)
        if period is None:
            period = receipt["arithmetic_period"]
        threshold_row = receipt["threshold_rows"][threshold]
        tail_targets = threshold_row["tail_target_count"]
        nonrescued = threshold_row["negative_full_count_inside_tail"]
        minimum_full_target = receipt["minimum_full_action_target"]
        minimum_full_value = receipt[
            "minimum_full_action_to_principal_ratio"]
        minimum_tail_target = threshold_row[
            "minimum_recombined_target_inside_tail"]
        minimum_tail_value = threshold_row[
            "minimum_recombined_inside_tail"]
        if ((cycle_start - 10000) % period == 0):
            global_cycle = (cycle_start - 10000) // period
        else:
            global_cycle = None

        total_negative_full += receipt["negative_full_action_count"]
        total_tail_targets += tail_targets
        total_nonrescued += nonrescued
        if (global_minimum_full is None
                or minimum_full_value < global_minimum_full[2]):
            global_minimum_full = (
                cycle, minimum_full_target, minimum_full_value)
        if (tail_targets and (
                global_minimum_tail_recombined is None
                or minimum_tail_value
                < global_minimum_tail_recombined[2])):
            global_minimum_tail_recombined = (
                cycle, minimum_tail_target, minimum_tail_value)

        cycle_rows[cycle] = {
            "start": cycle_start,
            "end": cycle_start + 2 * (targets_per_cycle - 1),
            "global_cycle": global_cycle,
            "tested_target_count": receipt["tested_target_count"],
            "full_action_negative_count": receipt[
                "negative_full_action_count"],
            "minimum_full_action_target": minimum_full_target,
            "minimum_full_action_to_principal_ratio": minimum_full_value,
            "tail_target_count": tail_targets,
            "tail_targets": threshold_row["tail_targets"],
            "nonrescued_tail_target_count": nonrescued,
            "rescued_tail_target_count": threshold_row[
                "rescued_tail_target_count"],
            "rescued_tail_targets": threshold_row[
                "rescued_tail_targets"],
            "minimum_tail_recombined_target": minimum_tail_target,
            "minimum_tail_recombined_to_principal_ratio": (
                minimum_tail_value),
            "tail_targets_all_rescued": bool(nonrescued == 0),
            "negative_tail_and_negative_full_targets": threshold_row[
                "negative_tail_and_negative_full_targets"],
        }

    cycles_with_nonrescued = tuple(
        cycle for cycle, row in cycle_rows.items()
        if row["nonrescued_tail_target_count"] > 0)
    cycles_with_full_negative = tuple(
        cycle for cycle, row in cycle_rows.items()
        if row["full_action_negative_count"] > 0)
    suffix_clear_start_cycle = None
    for cycle in sorted(cycle_rows):
        if all(cycle_rows[later]["nonrescued_tail_target_count"] == 0
               for later in range(cycle, cycle_count)):
            suffix_clear_start_cycle = cycle
            break
    suffix_clear_global_cycle = (
        cycle_rows[suffix_clear_start_cycle]["global_cycle"]
        if suffix_clear_start_cycle is not None else None)
    last_nonrescued_cycle = (
        max(cycles_with_nonrescued) if cycles_with_nonrescued else None)
    first_cycle_after_last_nonrescued = (
        last_nonrescued_cycle + 1
        if last_nonrescued_cycle is not None
        and last_nonrescued_cycle + 1 in cycle_rows else None)

    return {
        "arithmetic_period": period,
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "threshold": threshold,
        "tested_target_count": cycle_count * targets_per_cycle,
        "cycle_rows": cycle_rows,
        "total_full_action_negative_count": total_negative_full,
        "total_tail_target_count": total_tail_targets,
        "total_nonrescued_tail_target_count": total_nonrescued,
        "cycles_with_full_action_negatives": cycles_with_full_negative,
        "cycles_with_nonrescued_tail_targets": cycles_with_nonrescued,
        "last_cycle_with_nonrescued_tail_target": last_nonrescued_cycle,
        "first_cycle_after_last_nonrescued_tail_target": (
            first_cycle_after_last_nonrescued),
        "suffix_clear_start_cycle": suffix_clear_start_cycle,
        "suffix_clear_global_cycle": suffix_clear_global_cycle,
        "all_cycles_clear_nonrescued_tail": bool(
            not cycles_with_nonrescued),
        "global_minimum_full_action_cycle": global_minimum_full[0],
        "global_minimum_full_action_target": global_minimum_full[1],
        "global_minimum_full_action_to_principal_ratio": (
            global_minimum_full[2]),
        "global_minimum_tail_recombined_cycle": (
            global_minimum_tail_recombined[0]
            if global_minimum_tail_recombined is not None else None),
        "global_minimum_tail_recombined_target": (
            global_minimum_tail_recombined[1]
            if global_minimum_tail_recombined is not None else None),
        "global_minimum_tail_recombined_to_principal_ratio": (
            global_minimum_tail_recombined[2]
            if global_minimum_tail_recombined is not None else math.nan),
        "nonrescued_first_three_tail_cycle_horizon_measured": True,
        "eventual_nonrescued_tail_clearance_proved": False,
        "eventual_complement_rescue_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_tail_rescue_profile_receipt(
        start=10000, cycle_count=1, targets_per_cycle=5005,
        threshold=.3, tolerance=1e-9):
    """Profile complement rescue on the first-three negative tail.

    This is the mechanism-facing companion to the non-rescued horizon receipt.
    It keeps the exact tail targets and summarizes deficit depth, complement
    buffer, and recombined margin on the selected finite cycle window.
    """
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    if not math.isfinite(threshold) or threshold <= 0:
        raise ValueError("threshold must be finite and positive")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    cooccurrence = q286_first_three_complement_cooccurrence_receipt(
        start=start, cycle_count=cycle_count,
        targets_per_cycle=targets_per_cycle,
        negative_tail_thresholds=(threshold,), tolerance=tolerance)
    period = cooccurrence["arithmetic_period"]
    cycle_rows = {}
    tail_rows = {}
    global_tail_targets = []
    global_rescued_targets = []
    global_nonrescued_targets = []
    for cycle in range(cycle_count):
        cycle_tail_targets = tuple(
            target for target, row in cooccurrence["rows"].items()
            if row["cycle"] == cycle
            and row["first_three_to_principal_ratio"] < -threshold)
        cycle_rescued_targets = tuple(
            target for target in cycle_tail_targets
            if not cooccurrence["rows"][target]["negative_full_action"])
        cycle_nonrescued_targets = tuple(
            target for target in cycle_tail_targets
            if cooccurrence["rows"][target]["negative_full_action"])
        global_tail_targets.extend(cycle_tail_targets)
        global_rescued_targets.extend(cycle_rescued_targets)
        global_nonrescued_targets.extend(cycle_nonrescued_targets)

        for target in cycle_tail_targets:
            row = cooccurrence["rows"][target]
            first_three = row["first_three_to_principal_ratio"]
            complement = row["complement_to_principal_ratio"]
            full = row["full_action_to_principal_ratio"]
            tail_rows[target] = {
                "cycle": cycle,
                "deficit_to_principal_ratio": -first_three,
                "first_three_to_principal_ratio": first_three,
                "complement_to_principal_ratio": complement,
                "full_action_to_principal_ratio": full,
                "rescue_margin_to_principal_ratio": full,
                "complement_minus_threshold_to_principal_ratio": (
                    complement - threshold),
                "complement_minus_deficit_to_principal_ratio": (
                    complement + first_three),
                "rescued": bool(full > tolerance),
                "nonrescued": bool(full <= tolerance),
            }

        if cycle_tail_targets:
            deepest_deficit_target = max(
                cycle_tail_targets,
                key=lambda target: tail_rows[target][
                    "deficit_to_principal_ratio"])
            minimum_complement_target = min(
                cycle_tail_targets,
                key=lambda target: tail_rows[target][
                    "complement_to_principal_ratio"])
            minimum_margin_target = min(
                cycle_tail_targets,
                key=lambda target: tail_rows[target][
                    "full_action_to_principal_ratio"])
            maximum_deficit = tail_rows[
                deepest_deficit_target]["deficit_to_principal_ratio"]
            minimum_complement = tail_rows[
                minimum_complement_target]["complement_to_principal_ratio"]
            minimum_margin = tail_rows[
                minimum_margin_target]["full_action_to_principal_ratio"]
        else:
            deepest_deficit_target = None
            minimum_complement_target = None
            minimum_margin_target = None
            maximum_deficit = math.nan
            minimum_complement = math.nan
            minimum_margin = math.nan

        cycle_start = start + cycle * period
        cycle_rows[cycle] = {
            "start": cycle_start,
            "end": cycle_start + 2 * (targets_per_cycle - 1),
            "global_cycle": (
                (cycle_start - 10000) // period
                if (cycle_start - 10000) % period == 0 else None),
            "tail_target_count": len(cycle_tail_targets),
            "tail_targets": cycle_tail_targets,
            "rescued_tail_target_count": len(cycle_rescued_targets),
            "rescued_tail_targets": cycle_rescued_targets,
            "nonrescued_tail_target_count": len(cycle_nonrescued_targets),
            "nonrescued_tail_targets": cycle_nonrescued_targets,
            "all_tail_targets_rescued": bool(not cycle_nonrescued_targets),
            "deepest_deficit_target": deepest_deficit_target,
            "maximum_deficit_to_principal_ratio": maximum_deficit,
            "minimum_complement_target": minimum_complement_target,
            "minimum_complement_to_principal_ratio": minimum_complement,
            "minimum_rescue_margin_target": minimum_margin_target,
            "minimum_rescue_margin_to_principal_ratio": minimum_margin,
        }

    if global_tail_targets:
        global_deepest_deficit_target = max(
            global_tail_targets,
            key=lambda target: tail_rows[target][
                "deficit_to_principal_ratio"])
        global_minimum_complement_target = min(
            global_tail_targets,
            key=lambda target: tail_rows[target][
                "complement_to_principal_ratio"])
        global_minimum_margin_target = min(
            global_tail_targets,
            key=lambda target: tail_rows[target][
                "full_action_to_principal_ratio"])
    else:
        global_deepest_deficit_target = None
        global_minimum_complement_target = None
        global_minimum_margin_target = None

    return {
        "arithmetic_period": period,
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "threshold": threshold,
        "tested_target_count": cooccurrence["tested_target_count"],
        "cycle_rows": cycle_rows,
        "tail_rows": tail_rows,
        "tail_targets": tuple(global_tail_targets),
        "rescued_tail_targets": tuple(global_rescued_targets),
        "nonrescued_tail_targets": tuple(global_nonrescued_targets),
        "tail_target_count": len(global_tail_targets),
        "rescued_tail_target_count": len(global_rescued_targets),
        "nonrescued_tail_target_count": len(global_nonrescued_targets),
        "all_tail_targets_rescued": bool(not global_nonrescued_targets),
        "deepest_deficit_target": global_deepest_deficit_target,
        "minimum_complement_target": global_minimum_complement_target,
        "minimum_rescue_margin_target": global_minimum_margin_target,
        "first_three_tail_rescue_profile_measured": True,
        "eventual_complement_rescue_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def q286_first_three_tail_rescue_floor_candidate_receipt(
        start=10000, cycle_count=1, targets_per_cycle=5005,
        threshold=.3, complement_floor=.63, rescue_margin_floor=.3,
        deficit_ceiling=None, tolerance=1e-9):
    """Test finite candidate floors on the first-three tail rescue profile.

    The candidate is a finite falsifier for a possible eventual theorem:
    every target in the first-three negative tail should have complement above
    ``complement_floor`` and recombined margin above ``rescue_margin_floor``;
    optionally, the first-three deficit should stay below ``deficit_ceiling``.
    Passing this receipt proves only the checked finite window.
    """
    if type(start) is not int or start < 40 or start % 2:
        raise ValueError("start must be an even integer at least 40")
    if type(cycle_count) is not int or cycle_count < 1:
        raise ValueError("cycle_count must be a positive integer")
    if (type(targets_per_cycle) is not int or targets_per_cycle < 1
            or targets_per_cycle > 5005):
        raise ValueError("targets_per_cycle must lie between 1 and 5005")
    if not math.isfinite(threshold) or threshold <= 0:
        raise ValueError("threshold must be finite and positive")
    if (not math.isfinite(complement_floor)
            or complement_floor < 0):
        raise ValueError("complement_floor must be finite and nonnegative")
    if (not math.isfinite(rescue_margin_floor)
            or rescue_margin_floor < 0):
        raise ValueError(
            "rescue_margin_floor must be finite and nonnegative")
    if (deficit_ceiling is not None
            and (not math.isfinite(deficit_ceiling)
                 or deficit_ceiling <= 0)):
        raise ValueError("deficit_ceiling must be positive finite or None")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    profile = q286_first_three_tail_rescue_profile_receipt(
        start=start, cycle_count=cycle_count,
        targets_per_cycle=targets_per_cycle, threshold=threshold,
        tolerance=tolerance)
    complement_violations = tuple(
        target for target, row in profile["tail_rows"].items()
        if row["complement_to_principal_ratio"]
        < complement_floor - tolerance)
    margin_violations = tuple(
        target for target, row in profile["tail_rows"].items()
        if row["rescue_margin_to_principal_ratio"]
        < rescue_margin_floor - tolerance)
    if deficit_ceiling is None:
        deficit_violations = tuple()
    else:
        deficit_violations = tuple(
            target for target, row in profile["tail_rows"].items()
            if row["deficit_to_principal_ratio"]
            > deficit_ceiling + tolerance)
    violating_targets = tuple(sorted(set(
        complement_violations + margin_violations + deficit_violations)))

    cycle_rows = {}
    for cycle, row in profile["cycle_rows"].items():
        cycle_tail_targets = row["tail_targets"]
        cycle_complement_violations = tuple(
            target for target in cycle_tail_targets
            if target in complement_violations)
        cycle_margin_violations = tuple(
            target for target in cycle_tail_targets
            if target in margin_violations)
        cycle_deficit_violations = tuple(
            target for target in cycle_tail_targets
            if target in deficit_violations)
        cycle_rows[cycle] = {
            "global_cycle": row["global_cycle"],
            "tail_target_count": row["tail_target_count"],
            "nonrescued_tail_target_count": row[
                "nonrescued_tail_target_count"],
            "minimum_complement_to_principal_ratio": row[
                "minimum_complement_to_principal_ratio"],
            "minimum_rescue_margin_to_principal_ratio": row[
                "minimum_rescue_margin_to_principal_ratio"],
            "maximum_deficit_to_principal_ratio": row[
                "maximum_deficit_to_principal_ratio"],
            "complement_floor_violations": cycle_complement_violations,
            "rescue_margin_floor_violations": cycle_margin_violations,
            "deficit_ceiling_violations": cycle_deficit_violations,
            "candidate_floor_passed": bool(
                not cycle_complement_violations
                and not cycle_margin_violations
                and not cycle_deficit_violations),
        }

    return {
        "arithmetic_period": profile["arithmetic_period"],
        "start": start,
        "cycle_count": cycle_count,
        "targets_per_cycle": targets_per_cycle,
        "threshold": threshold,
        "complement_floor": complement_floor,
        "rescue_margin_floor": rescue_margin_floor,
        "deficit_ceiling": deficit_ceiling,
        "tested_target_count": profile["tested_target_count"],
        "tail_target_count": profile["tail_target_count"],
        "nonrescued_tail_target_count": profile[
            "nonrescued_tail_target_count"],
        "cycle_rows": cycle_rows,
        "complement_floor_violations": complement_violations,
        "rescue_margin_floor_violations": margin_violations,
        "deficit_ceiling_violations": deficit_violations,
        "violating_targets": violating_targets,
        "candidate_floor_passed": bool(not violating_targets),
        "profile_receipt": profile,
        "first_three_tail_rescue_floor_candidate_measured": True,
        "eventual_rescue_floor_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }
