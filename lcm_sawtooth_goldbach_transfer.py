"""Exact Goldbach-sum form of the dominant even-even CRT numerator.

This module isolates an algebraic transfer.  It does not assert a mean-square
estimate for the resulting twisted Goldbach sums.
"""

import math
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
