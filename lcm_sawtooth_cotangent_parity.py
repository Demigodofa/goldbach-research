"""Cotangent-parity attribution in fully resonant source eigensectors."""

import math

import numpy as np

from lcm_sawtooth_resonant_source_sectors import (
    _direct_fully_resonant_totals,
    _frequency_batch,
    _frequency_entries,
    _quotient_sector_batches,
)
from lcm_sawtooth_orientation_rank import _oriented_family_source_modes
from lcm_sawtooth_source_ramanujan import (
    _prime_power_factors,
    _primitive_numerators,
)


def _endpoint_cotangent_parity_modes(period, denominator, numerator):
    frequency = numerator * (period // denominator) % period
    cotangent = 1 / math.tan(math.pi * numerator / denominator)
    return (
        ((frequency, -.5), (0, -.5)),
        ((frequency, -.5j * cotangent), (0, .5j * cotangent)),
    )


def _one_orientation_parity_source_modes(
        period, conductor, odd_partner):
    doubled_partner = 2 * odd_partner
    if (math.gcd(conductor, doubled_partner) != 1
            or conductor * doubled_partner != period):
        raise ValueError("parity split requires coprime product denominators")
    sources = ({}, {})
    for left_numerator in _primitive_numerators(conductor):
        left_parts = _endpoint_cotangent_parity_modes(
            period, conductor, left_numerator)
        left_source_frequency = (
            left_numerator * (period // conductor))
        for right_numerator in _primitive_numerators(doubled_partner):
            right_parts = _endpoint_cotangent_parity_modes(
                period, doubled_partner, right_numerator)
            right_source_frequency = (
                right_numerator * (period // doubled_partner))
            source_residue = (
                left_source_frequency - right_source_frequency) % period
            if math.gcd(source_residue, period) != 1:
                raise AssertionError("unexpected reduced source denominator")
            for left_parity, left_modes in enumerate(left_parts):
                for right_parity, right_modes in enumerate(right_parts):
                    parity = (left_parity + right_parity) % 2
                    combined = sources[parity].setdefault(source_residue, {})
                    for left_frequency, left_coefficient in left_modes:
                        for right_frequency, right_coefficient in right_modes:
                            frequency = (
                                left_frequency - right_frequency) % period
                            combined[frequency] = (
                                combined.get(frequency, 0.0j)
                                + left_coefficient
                                * np.conjugate(right_coefficient))
    return sources


def _combine_components(components):
    combined = {}
    for sources in components:
        for residue, modes in sources.items():
            combined_modes = combined.setdefault(residue, {})
            for frequency, coefficient in modes.items():
                combined_modes[frequency] = (
                    combined_modes.get(frequency, 0.0j) + coefficient)
    return combined


def _source_coefficient_relative_error(expected, actual):
    if expected.keys() != actual.keys():
        return math.inf
    if any(expected[residue].keys() != actual[residue].keys()
           for residue in expected):
        return math.inf
    return max(
        abs(expected[residue][frequency] - actual[residue][frequency])
        / max(1.0, abs(expected[residue][frequency]))
        for residue in expected for frequency in expected[residue])


def cotangent_parity_source_receipt(
        families=((77, 65), (143, 35)), lag=130, tolerance=1e-12):
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
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    factors = _prime_power_factors(period)
    if any(prime != prime_power for prime, prime_power in factors):
        raise ValueError("cotangent parity requires squarefree period")
    primes = tuple(prime for prime, _ in factors)
    common = math.gcd(lag, period)
    quotient = period // common
    if math.gcd(common, quotient) != 1:
        raise ValueError("cotangent parity requires coprime CRT parts")
    common_primes = tuple(prime for prime in primes if common % prime == 0)
    quotient_primes = tuple(prime for prime in primes if quotient % prime == 0)
    shape = tuple(prime - 1 for prime in primes)
    unit_class_count = math.prod(shape)
    sectors = tuple(
        tuple(prime for index, prime in enumerate(quotient_primes)
              if mask & (1 << index))
        for mask in range(1 << len(quotient_primes)))

    left_components = _one_orientation_parity_source_modes(
        period, *families[0])
    right_components = _one_orientation_parity_source_modes(
        period, *families[1])
    left_entries = tuple(
        _frequency_entries(sources, primes) for sources in left_components)
    right_entries = tuple(
        _frequency_entries(sources, primes) for sources in right_components)
    parity_sector_totals = {
        parity: {sector: np.zeros(period, dtype=complex) for sector in sectors}
        for parity in (0, 1)}

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
        for left_parity, (left_frequencies, left_sectors) in enumerate(
                left_data):
            if not left_frequencies:
                continue
            for right_parity, (right_frequencies, right_sectors) in enumerate(
                    right_data):
                if not right_frequencies:
                    continue
                parity = (left_parity + right_parity) % 2
                totals = parity_sector_totals[parity]
                for sector in sectors:
                    eigenvalue = math.prod(
                        -1 if prime in sector else prime - 2
                        for prime in quotient_primes)
                    pairings = (
                        left_sectors[sector].reshape(
                            len(left_frequencies), -1)
                        @ np.conjugate(right_sectors[sector]).reshape(
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

    def masses(included_parities):
        sector_values = {
            sector: sum(parity_sector_totals[parity][sector]
                        for parity in included_parities)
            for sector in sectors}
        sectorwise_mass = sum(
            float(np.sum(np.abs(values[resonant_frequencies])))
            for values in sector_values.values()) / unit_class_count
        recombined = sum(sector_values.values())
        recombined_mass = (
            float(np.sum(np.abs(recombined[resonant_frequencies])))
            / unit_class_count)
        return sectorwise_mass, recombined_mass, sectorwise_mass - recombined_mass

    even_sectorwise_mass, even_recombined_mass, even_loss = masses((0,))
    odd_sectorwise_mass, odd_recombined_mass, odd_loss = masses((1,))
    full_sectorwise_mass, full_recombined_mass, full_loss = masses((0, 1))
    odd_shapley_loss = .5 * (odd_loss + full_loss - even_loss)
    even_shapley_loss = full_loss - odd_shapley_loss
    odd_shapley_loss_fraction = (
        odd_shapley_loss / full_loss if full_loss > 0 else None)

    combined_left = _combine_components(left_components)
    combined_right = _combine_components(right_components)
    original_left = _oriented_family_source_modes(
        period, *families[0])[0]
    original_right = _oriented_family_source_modes(
        period, *families[1])[0]
    maximum_source_parity_reconstruction_relative_error = max(
        _source_coefficient_relative_error(original_left, combined_left),
        _source_coefficient_relative_error(original_right, combined_right))
    direct_totals = _direct_fully_resonant_totals(
        period, lag, combined_left, combined_right)
    reconstructed_totals = sum(
        values for totals in parity_sector_totals.values()
        for values in totals.values())
    errors = np.abs(
        reconstructed_totals[resonant_frequencies]
        - direct_totals[resonant_frequencies])
    natural_scale = np.maximum(
        1.0,
        sum(np.abs(values[resonant_frequencies])
            for totals in parity_sector_totals.values()
            for values in totals.values()))
    maximum_reconstruction_natural_scale_relative_error = float(np.max(
        errors / natural_scale))
    return {
        "families": families,
        "arithmetic_period": period,
        "lag": lag,
        "gcd_lag_period": common,
        "quotient_period": quotient,
        "quotient_primes": quotient_primes,
        "even_sectorwise_absolute_mass": even_sectorwise_mass,
        "even_recombined_absolute_mass": even_recombined_mass,
        "even_sector_recombination_loss": even_loss,
        "odd_sectorwise_absolute_mass": odd_sectorwise_mass,
        "odd_recombined_absolute_mass": odd_recombined_mass,
        "odd_sector_recombination_loss": odd_loss,
        "full_sectorwise_absolute_mass": full_sectorwise_mass,
        "full_recombined_absolute_mass": full_recombined_mass,
        "full_sector_recombination_loss": full_loss,
        "even_shapley_recombination_loss": even_shapley_loss,
        "odd_shapley_recombination_loss": odd_shapley_loss,
        "odd_shapley_recombination_loss_fraction": (
            odd_shapley_loss_fraction),
        "maximum_reconstruction_natural_scale_relative_error": (
            maximum_reconstruction_natural_scale_relative_error),
        "maximum_source_parity_reconstruction_relative_error": (
            maximum_source_parity_reconstruction_relative_error),
        "cotangent_parity_reconstruction_passes": bool(
            maximum_reconstruction_natural_scale_relative_error <= tolerance
            and maximum_source_parity_reconstruction_relative_error
            <= tolerance),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def cotangent_parity_discriminator_receipt(tolerance=1e-12):
    strong = cotangent_parity_source_receipt(lag=130, tolerance=tolerance)
    weak = cotangent_parity_source_receipt(lag=70, tolerance=tolerance)
    return {
        "strong_quotient": strong["quotient_period"],
        "weak_quotient": weak["quotient_period"],
        "strong_odd_shapley_loss_fraction": strong[
            "odd_shapley_recombination_loss_fraction"],
        "weak_odd_shapley_loss_fraction": weak[
            "odd_shapley_recombination_loss_fraction"],
        "minimum_strong_odd_shapley_loss_fraction": .75,
        "maximum_weak_odd_shapley_loss_fraction": .25,
        "strong_odd_cotangent_gate_passes": bool(
            strong["odd_shapley_recombination_loss_fraction"] >= .75),
        "weak_odd_cotangent_gate_passes": bool(
            weak["odd_shapley_recombination_loss_fraction"] <= .25),
        "cotangent_parity_discriminator_passes": bool(
            strong["odd_shapley_recombination_loss_fraction"] >= .75
            and weak["odd_shapley_recombination_loss_fraction"] <= .25),
        "both_reconstructions_pass": bool(
            strong["cotangent_parity_reconstruction_passes"]
            and weak["cotangent_parity_reconstruction_passes"]),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(cotangent_parity_discriminator_receipt())
