"""Endpoint-orientation rank inside fully resonant tensor sectors."""

import math

import numpy as np

from lcm_sawtooth_resonant_source_sectors import (
    _direct_fully_resonant_totals,
    _frequency_batch,
    _frequency_entries,
    _quotient_sector_batches,
)
from lcm_sawtooth_source_ramanujan import (
    _endpoint_modes,
    _prime_power_factors,
    _primitive_numerators,
)


def _oriented_family_source_modes(period, conductor, odd_partner):
    doubled_partner = 2 * odd_partner
    if math.lcm(conductor, doubled_partner) != period:
        raise ValueError("family must have the requested source period")
    denominators = (conductor, doubled_partner)
    numerators = tuple(_primitive_numerators(value) for value in denominators)
    oriented_sources = []
    for left_index, right_index in ((0, 1), (1, 0)):
        left_denominator = denominators[left_index]
        right_denominator = denominators[right_index]
        sources = {}
        for left_numerator in numerators[left_index]:
            left_modes = _endpoint_modes(
                period, left_denominator, left_numerator)
            left_source_frequency = (
                left_numerator * (period // left_denominator))
            for right_numerator in numerators[right_index]:
                right_source_frequency = (
                    right_numerator * (period // right_denominator))
                source_residue = (
                    left_source_frequency - right_source_frequency) % period
                if math.gcd(source_residue, period) != 1:
                    raise AssertionError("unexpected reduced source denominator")
                right_modes = _endpoint_modes(
                    period, right_denominator, right_numerator)
                combined = sources.setdefault(source_residue, {})
                for left_frequency, left_coefficient in left_modes:
                    for right_frequency, right_coefficient in right_modes:
                        frequency = (
                            left_frequency - right_frequency) % period
                        combined[frequency] = (
                            combined.get(frequency, 0.0j)
                            + left_coefficient
                            * np.conjugate(right_coefficient))
        oriented_sources.append(sources)
    return tuple(oriented_sources)


def _combine_orientations(oriented_sources):
    combined_sources = {}
    for sources in oriented_sources:
        for residue, modes in sources.items():
            combined_modes = combined_sources.setdefault(residue, {})
            for frequency, coefficient in modes.items():
                combined_modes[frequency] = (
                    combined_modes.get(frequency, 0.0j) + coefficient)
    return combined_sources


def endpoint_orientation_symmetry_receipt(
        families=((77, 65), (143, 35)), tolerance=1e-10):
    """Check the Fourier form of H_(A,p;B,q)=H_(B,-q;A,-p)."""
    families = tuple(families)
    if (not families
            or any(len(family) != 2 for family in families)
            or any(type(c) is not int or c < 3 or c % 2 == 0
                   or type(d) is not int or d < 3 or d % 2 == 0
                   for c, d in families)):
        raise ValueError("require odd conductor-partner families")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    rows = {}
    for family in families:
        conductor, odd_partner = family
        doubled_partner = 2 * odd_partner
        if math.gcd(conductor, doubled_partner) != 1:
            raise ValueError("orientation symmetry receipt requires coprime parts")
        period = conductor * doubled_partner
        first, second = _oriented_family_source_modes(period, *family)
        residue_supports_match = first.keys() == second.keys()
        frequency_supports_match = bool(
            residue_supports_match
            and all(first[residue].keys() == second[residue].keys()
                    for residue in first))
        maximum_coefficient_relative_error = (
            max(
                abs(first[residue][frequency]
                    - second[residue][frequency])
                / max(1.0, abs(first[residue][frequency]),
                      abs(second[residue][frequency]))
                for residue in first
                for frequency in first[residue])
            if frequency_supports_match else math.inf)
        rows[family] = {
            "period": period,
            "source_residue_count": len(first),
            "residue_supports_match": residue_supports_match,
            "frequency_supports_match": frequency_supports_match,
            "maximum_coefficient_relative_error": (
                maximum_coefficient_relative_error),
            "orientation_symmetry_identity_passes": bool(
                frequency_supports_match
                and maximum_coefficient_relative_error <= tolerance),
        }
    return {
        "families": families,
        "rows": rows,
        "maximum_coefficient_relative_error": max(
            row["maximum_coefficient_relative_error"]
            for row in rows.values()),
        "all_orientation_symmetry_identities_pass": all(
            row["orientation_symmetry_identity_passes"]
            for row in rows.values()),
        "source_function_orientation_multiplicity": 2,
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def fully_resonant_orientation_rank_receipt(
        families=((77, 65), (143, 35)), lag=110,
        maximum_third_singular_value_ratio=1e-10,
        maximum_orientation_profile_residual=1e-12,
        tolerance=1e-12):
    families = tuple(families)
    if (len(families) != 2 or any(len(family) != 2 for family in families)
            or any(type(c) is not int or c < 3 or c % 2 == 0
                   or type(d) is not int or d < 3 or d % 2 == 0
                   for c, d in families)):
        raise ValueError("require two odd conductor-partner families")
    periods = tuple(math.lcm(c, 2 * d) for c, d in families)
    if len(set(periods)) != 1:
        raise ValueError("families must share one arithmetic period")
    period = periods[0]
    if type(lag) is not int or not 0 < lag < period:
        raise ValueError("lag must lie strictly inside the period")
    if (not math.isfinite(maximum_third_singular_value_ratio)
            or not 0 <= maximum_third_singular_value_ratio < 1):
        raise ValueError("third singular ratio must lie in [0,1)")
    if (not math.isfinite(maximum_orientation_profile_residual)
            or maximum_orientation_profile_residual < 0):
        raise ValueError("orientation residual must be finite and nonnegative")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    factors = _prime_power_factors(period)
    if any(prime != prime_power for prime, prime_power in factors):
        raise ValueError("orientation rank requires squarefree period")
    primes = tuple(prime for prime, _ in factors)
    common = math.gcd(lag, period)
    quotient = period // common
    if math.gcd(common, quotient) != 1:
        raise ValueError("orientation rank requires coprime CRT parts")
    common_primes = tuple(prime for prime in primes if common % prime == 0)
    quotient_primes = tuple(prime for prime in primes if quotient % prime == 0)
    shape = tuple(prime - 1 for prime in primes)
    unit_class_count = math.prod(shape)
    sectors = tuple(
        tuple(prime for index, prime in enumerate(quotient_primes)
              if mask & (1 << index))
        for mask in range(1 << len(quotient_primes)))

    left_orientations = _oriented_family_source_modes(
        period, *families[0])
    right_orientations = _oriented_family_source_modes(
        period, *families[1])
    left_entries = tuple(
        _frequency_entries(sources, primes)
        for sources in left_orientations)
    right_entries = tuple(
        _frequency_entries(sources, primes)
        for sources in right_orientations)
    orientation_sector_totals = {
        (left_index, right_index): {
            sector: np.zeros(period, dtype=complex) for sector in sectors}
        for left_index in range(2) for right_index in range(2)}

    for residue_class in range(quotient):
        left_data = []
        right_data = []
        for entries in left_entries:
            frequencies = tuple(
                frequency for frequency in entries
                if frequency % quotient == residue_class)
            components = (
                _quotient_sector_batches(
                    _frequency_batch(entries, frequencies, shape),
                    primes, quotient_primes)
                if frequencies else None)
            left_data.append((frequencies, components))
        for entries in right_entries:
            frequencies = tuple(
                frequency for frequency in entries
                if frequency % quotient == residue_class)
            components = (
                _quotient_sector_batches(
                    _frequency_batch(entries, frequencies, shape),
                    primes, quotient_primes)
                if frequencies else None)
            right_data.append((frequencies, components))
        for left_index, (left_frequencies, left_components) in enumerate(
                left_data):
            if not left_frequencies:
                continue
            for right_index, (right_frequencies, right_components) in enumerate(
                    right_data):
                if not right_frequencies:
                    continue
                totals = orientation_sector_totals[
                    (left_index, right_index)]
                for sector in sectors:
                    eigenvalue = math.prod(
                        -1 if prime in sector else prime - 2
                        for prime in quotient_primes)
                    pairings = (
                        left_components[sector].reshape(
                            len(left_frequencies), -1)
                        @ np.conjugate(right_components[sector]).reshape(
                            len(right_frequencies), -1).T)
                    for left_row, left_frequency in enumerate(left_frequencies):
                        for right_row, right_frequency in enumerate(
                                right_frequencies):
                            frequency = (
                                left_frequency - right_frequency) % period
                            common_multiplier = math.prod(
                                prime - 1 if frequency % prime == 0 else -1
                                for prime in common_primes)
                            totals[sector][frequency] += (
                                common_multiplier * eigenvalue
                                * pairings[left_row, right_row])

    resonant_frequencies = np.arange(0, period, quotient)
    feature_matrix = np.asarray([
        np.concatenate(tuple(
            totals[sector][resonant_frequencies] / unit_class_count
            for sector in sectors))
        for totals in orientation_sector_totals.values()])
    singular_values = np.linalg.svd(feature_matrix, compute_uv=False)
    third_singular_value_ratio = (
        float(singular_values[2] / singular_values[0])
        if singular_values[0] > 0 else None)
    orientation_pairs = tuple(orientation_sector_totals)
    reference_vector = feature_matrix[0]
    reference_norm_squared = float(np.vdot(
        reference_vector, reference_vector).real)
    orientation_pair_reference_scalars = {}
    orientation_pair_reference_residuals = {}
    for row, pair in zip(feature_matrix, orientation_pairs):
        scalar = (
            np.vdot(reference_vector, row) / reference_norm_squared
            if reference_norm_squared > 0 else 0.0j)
        orientation_pair_reference_scalars[pair] = complex(scalar)
        orientation_pair_reference_residuals[pair] = (
            float(np.linalg.norm(row - scalar * reference_vector))
            / max(1.0, float(np.linalg.norm(row))))

    combined_left = _combine_orientations(left_orientations)
    combined_right = _combine_orientations(right_orientations)
    direct_totals = _direct_fully_resonant_totals(
        period, lag, combined_left, combined_right)
    reconstructed_totals = sum(
        values
        for totals in orientation_sector_totals.values()
        for values in totals.values())
    reconstruction_errors = np.abs(
        reconstructed_totals[resonant_frequencies]
        - direct_totals[resonant_frequencies])
    reconstruction_scale = np.maximum(
        1.0,
        sum(np.abs(values[resonant_frequencies])
            for totals in orientation_sector_totals.values()
            for values in totals.values()))
    maximum_reconstruction_natural_scale_relative_error = float(np.max(
        reconstruction_errors / reconstruction_scale))
    orientation_pair_absolute_masses = {
        pair: sum(float(np.sum(np.abs(values[resonant_frequencies])))
                  for values in totals.values()) / unit_class_count
        for pair, totals in orientation_sector_totals.items()}
    return {
        "families": families,
        "arithmetic_period": period,
        "lag": lag,
        "gcd_lag_period": common,
        "quotient_period": quotient,
        "quotient_primes": quotient_primes,
        "orientation_pair_absolute_masses": orientation_pair_absolute_masses,
        "orientation_pair_reference_scalars": {
            pair: (value.real, value.imag)
            for pair, value in orientation_pair_reference_scalars.items()},
        "orientation_pair_reference_residuals": (
            orientation_pair_reference_residuals),
        "maximum_orientation_pair_reference_residual": max(
            orientation_pair_reference_residuals.values()),
        "maximum_orientation_profile_residual": (
            maximum_orientation_profile_residual),
        "orientation_profiles_identical_gate_passes": bool(
            max(orientation_pair_reference_residuals.values())
            <= maximum_orientation_profile_residual),
        "orientation_feature_singular_values": tuple(
            float(value) for value in singular_values),
        "third_singular_value_ratio": third_singular_value_ratio,
        "maximum_third_singular_value_ratio": (
            maximum_third_singular_value_ratio),
        "orientation_rank_two_gate_passes": bool(
            third_singular_value_ratio is not None
            and third_singular_value_ratio
            <= maximum_third_singular_value_ratio),
        "maximum_reconstruction_natural_scale_relative_error": (
            maximum_reconstruction_natural_scale_relative_error),
        "orientation_sector_reconstruction_passes": bool(
            maximum_reconstruction_natural_scale_relative_error <= tolerance),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(fully_resonant_orientation_rank_receipt())
