"""Tensor sectors of the fully resonant source-frequency contribution."""

import math

import numpy as np

from lcm_sawtooth_source_ramanujan import (
    _conditioned_unit_exponential_sum,
    _family_source_modes,
    _prime_power_factors,
)


def _frequency_entries(sources, primes):
    entries = {}
    for residue, modes in sources.items():
        index = tuple(residue % prime - 1 for prime in primes)
        for frequency, coefficient in modes.items():
            entries.setdefault(frequency, []).append((index, coefficient))
    return entries


def _frequency_batch(entries, frequencies, shape):
    batch = np.zeros((len(frequencies),) + shape, dtype=complex)
    for row, frequency in enumerate(frequencies):
        for index, coefficient in entries[frequency]:
            batch[(row,) + index] = coefficient
    return batch


def _quotient_sector_batches(batch, primes, quotient_primes):
    components = {(): batch}
    for prime in quotient_primes:
        axis = primes.index(prime) + 1
        next_components = {}
        for sector, component in components.items():
            constant = np.broadcast_to(
                np.mean(component, axis=axis, keepdims=True),
                component.shape)
            next_components[sector] = constant
            next_components[sector + (prime,)] = component - constant
        components = next_components
    return components


def _direct_fully_resonant_totals(
        period, lag, left_sources, right_sources):
    common = math.gcd(lag, period)
    quotient = period // common
    totals = np.zeros(period, dtype=complex)
    for left_residue, left_modes in left_sources.items():
        for reduced_difference in range(quotient):
            if math.gcd(reduced_difference, quotient) != 1:
                continue
            difference = common * reduced_difference
            right_modes = right_sources.get(
                (left_residue - difference) % period)
            if right_modes is None:
                continue
            for left_frequency, left_coefficient in left_modes.items():
                for right_frequency, right_coefficient in right_modes.items():
                    frequency = (
                        left_frequency - right_frequency) % period
                    if frequency % quotient != 0:
                        continue
                    totals[frequency] += (
                        left_coefficient
                        * np.conjugate(right_coefficient)
                        * _conditioned_unit_exponential_sum(
                            period, lag, difference, frequency))
    return totals


def fully_resonant_source_sector_receipt(
        families=((77, 65), (143, 35)), lag=182,
        minimum_mean_zero_sector_mass_fraction=.75,
        minimum_sector_cross_frequency_coherence=.95,
        maximum_sector_recombination_quotient=.25,
        tolerance=1e-12):
    """Resolve q|n source terms into eigensectors of tensor_r(J-I)."""
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
    if not 0 < minimum_mean_zero_sector_mass_fraction <= 1:
        raise ValueError("mean-zero mass fraction must lie in (0,1]")
    if not 0 < minimum_sector_cross_frequency_coherence <= 1:
        raise ValueError("sector coherence must lie in (0,1]")
    if not 0 < maximum_sector_recombination_quotient <= 1:
        raise ValueError("sector recombination quotient must lie in (0,1]")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    factors = _prime_power_factors(period)
    if any(prime != prime_power for prime, prime_power in factors):
        raise ValueError("sector decomposition requires squarefree period")
    primes = tuple(prime for prime, _ in factors)
    common = math.gcd(lag, period)
    quotient = period // common
    if math.gcd(common, quotient) != 1:
        raise ValueError("sector decomposition requires coprime CRT parts")
    common_primes = tuple(prime for prime in primes if common % prime == 0)
    quotient_primes = tuple(prime for prime in primes if quotient % prime == 0)
    shape = tuple(prime - 1 for prime in primes)
    unit_class_count = math.prod(shape)

    left_sources, _ = _family_source_modes(period, *families[0])
    right_sources, _ = _family_source_modes(period, *families[1])
    left_entries = _frequency_entries(left_sources, primes)
    right_entries = _frequency_entries(right_sources, primes)
    sector_totals = {
        sector: np.zeros(period, dtype=complex)
        for mask in range(1 << len(quotient_primes))
        for sector in [tuple(
            prime for index, prime in enumerate(quotient_primes)
            if mask & (1 << index))]}

    for residue_class in range(quotient):
        left_frequencies = tuple(
            frequency for frequency in left_entries
            if frequency % quotient == residue_class)
        right_frequencies = tuple(
            frequency for frequency in right_entries
            if frequency % quotient == residue_class)
        if not left_frequencies or not right_frequencies:
            continue
        left_batch = _frequency_batch(left_entries, left_frequencies, shape)
        right_batch = _frequency_batch(right_entries, right_frequencies, shape)
        left_components = _quotient_sector_batches(
            left_batch, primes, quotient_primes)
        right_components = _quotient_sector_batches(
            right_batch, primes, quotient_primes)
        for sector in sector_totals:
            eigenvalue = math.prod(
                -1 if prime in sector else prime - 2
                for prime in quotient_primes)
            pairings = (
                left_components[sector].reshape(len(left_frequencies), -1)
                @ np.conjugate(right_components[sector]).reshape(
                    len(right_frequencies), -1).T)
            for left_index, left_frequency in enumerate(left_frequencies):
                for right_index, right_frequency in enumerate(right_frequencies):
                    frequency = (
                        left_frequency - right_frequency) % period
                    common_multiplier = math.prod(
                        prime - 1 if frequency % prime == 0 else -1
                        for prime in common_primes)
                    sector_totals[sector][frequency] += (
                        common_multiplier * eigenvalue
                        * pairings[left_index, right_index])

    direct_totals = _direct_fully_resonant_totals(
        period, lag, left_sources, right_sources)
    reconstructed_totals = sum(sector_totals.values())
    resonant_frequencies = np.arange(0, period, quotient)
    reconstruction_errors = np.abs(
        reconstructed_totals[resonant_frequencies]
        - direct_totals[resonant_frequencies])
    reconstruction_natural_scales = np.maximum(
        1.0,
        sum(np.abs(values[resonant_frequencies])
            for values in sector_totals.values()))
    maximum_reconstruction_relative_error = max(
        abs(reconstructed_totals[frequency] - direct_totals[frequency])
        / max(1.0, abs(direct_totals[frequency]))
        for frequency in resonant_frequencies)
    maximum_reconstruction_natural_scale_relative_error = float(np.max(
        reconstruction_errors / reconstruction_natural_scales))
    maximum_reconstruction_absolute_error = float(np.max(
        reconstruction_errors))
    maximum_off_resonant_sector_value = max(
        abs(values[frequency])
        for values in sector_totals.values()
        for frequency in range(period)
        if frequency % quotient != 0)
    sector_absolute_masses = {
        sector: float(np.sum(np.abs(values[resonant_frequencies])))
        / unit_class_count
        for sector, values in sector_totals.items()}
    sector_signed_means = {
        sector: complex(np.sum(values[resonant_frequencies]) / unit_class_count)
        for sector, values in sector_totals.items()}
    sector_cross_frequency_quotients = {
        sector: abs(sector_signed_means[sector]) / mass
        for sector, mass in sector_absolute_masses.items()
        if mass > 0}
    minimum_observed_sector_cross_frequency_coherence = min(
        sector_cross_frequency_quotients.values(), default=None)
    alternating_parity_sign_matches = {
        sector: bool(
            ((-1 if len(sector) % 2 == 0 else 1) * value.real > 0)
            and abs(value.imag) <= tolerance * max(1.0, abs(value.real)))
        for sector, value in sector_signed_means.items()}
    sectorwise_absolute_mass = sum(sector_absolute_masses.values())
    mean_zero_sector_mass = sum(
        mass for sector, mass in sector_absolute_masses.items() if sector)
    mean_zero_sector_mass_fraction = (
        mean_zero_sector_mass / sectorwise_absolute_mass
        if sectorwise_absolute_mass > 0 else None)
    direct_fully_resonant_absolute_mass = (
        float(np.sum(np.abs(direct_totals[resonant_frequencies])))
        / unit_class_count)
    reconstructed_fully_resonant_absolute_mass = (
        float(np.sum(np.abs(reconstructed_totals[resonant_frequencies])))
        / unit_class_count)
    sector_recombination_quotient = (
        reconstructed_fully_resonant_absolute_mass / sectorwise_absolute_mass
        if sectorwise_absolute_mass > 0 else None)
    return {
        "families": families,
        "arithmetic_period": period,
        "lag": lag,
        "gcd_lag_period": common,
        "quotient_period": quotient,
        "common_primes": common_primes,
        "quotient_primes": quotient_primes,
        "sector_eigenvalues": {
            sector: math.prod(
                -1 if prime in sector else prime - 2
                for prime in quotient_primes)
            for sector in sector_totals},
        "sector_absolute_masses": sector_absolute_masses,
        "sector_signed_mean_correlations": {
            sector: (value.real, value.imag)
            for sector, value in sector_signed_means.items()},
        "sector_cross_frequency_quotients": (
            sector_cross_frequency_quotients),
        "minimum_observed_sector_cross_frequency_coherence": (
            minimum_observed_sector_cross_frequency_coherence),
        "minimum_sector_cross_frequency_coherence": (
            minimum_sector_cross_frequency_coherence),
        "all_sector_cross_frequency_coherence_gates_pass": bool(
            minimum_observed_sector_cross_frequency_coherence is not None
            and minimum_observed_sector_cross_frequency_coherence
            >= minimum_sector_cross_frequency_coherence),
        "alternating_parity_sign_matches": alternating_parity_sign_matches,
        "all_alternating_parity_signs_match": all(
            alternating_parity_sign_matches.values()),
        "sectorwise_absolute_mass": sectorwise_absolute_mass,
        "mean_zero_sector_mass_fraction": mean_zero_sector_mass_fraction,
        "minimum_mean_zero_sector_mass_fraction": (
            minimum_mean_zero_sector_mass_fraction),
        "mean_zero_sector_mass_gate_passes": bool(
            mean_zero_sector_mass_fraction is not None
            and mean_zero_sector_mass_fraction
            >= minimum_mean_zero_sector_mass_fraction),
        "direct_fully_resonant_absolute_mass": (
            direct_fully_resonant_absolute_mass),
        "reconstructed_fully_resonant_absolute_mass": (
            reconstructed_fully_resonant_absolute_mass),
        "sector_recombination_quotient": sector_recombination_quotient,
        "maximum_sector_recombination_quotient": (
            maximum_sector_recombination_quotient),
        "sector_recombination_gate_passes": bool(
            sector_recombination_quotient is not None
            and sector_recombination_quotient
            <= maximum_sector_recombination_quotient),
        "maximum_reconstruction_absolute_error": (
            maximum_reconstruction_absolute_error),
        "maximum_reconstruction_relative_error": (
            maximum_reconstruction_relative_error),
        "maximum_reconstruction_natural_scale_relative_error": (
            maximum_reconstruction_natural_scale_relative_error),
        "maximum_off_resonant_sector_value": (
            maximum_off_resonant_sector_value),
        "fully_resonant_sector_identity_passes": bool(
            maximum_reconstruction_natural_scale_relative_error <= tolerance
            and maximum_off_resonant_sector_value <= tolerance),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def leading_lag_fully_resonant_sector_receipt(tolerance=1e-12):
    lags = (140, 154, 156, 182, 240)
    results = {
        lag: fully_resonant_source_sector_receipt(
            lag=lag, tolerance=tolerance)
        for lag in lags}
    return {
        "lags": lags,
        "quotient_primes": {
            lag: result["quotient_primes"]
            for lag, result in results.items()},
        "minimum_sector_cross_frequency_coherences": {
            lag: result[
                "minimum_observed_sector_cross_frequency_coherence"]
            for lag, result in results.items()},
        "sector_recombination_quotients": {
            lag: result["sector_recombination_quotient"]
            for lag, result in results.items()},
        "alternating_parity_sign_gates": {
            lag: result["all_alternating_parity_signs_match"]
            for lag, result in results.items()},
        "all_sector_cross_frequency_coherence_gates_pass": all(
            result["all_sector_cross_frequency_coherence_gates_pass"]
            for result in results.values()),
        "all_sector_recombination_gates_pass": all(
            result["sector_recombination_gate_passes"]
            for result in results.values()),
        "all_alternating_parity_sign_gates_pass": all(
            result["all_alternating_parity_signs_match"]
            for result in results.values()),
        "all_fully_resonant_sector_identities_pass": all(
            result["fully_resonant_sector_identity_passes"]
            for result in results.values()),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(fully_resonant_source_sector_receipt())
