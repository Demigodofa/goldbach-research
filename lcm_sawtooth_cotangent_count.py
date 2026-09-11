"""Exact cotangent-count attribution in fully resonant source sectors."""

import itertools
import math

import numpy as np

from lcm_sawtooth_cotangent_parity import (
    _combine_components,
    _endpoint_cotangent_parity_modes,
    _source_coefficient_relative_error,
)
from lcm_sawtooth_orientation_rank import _oriented_family_source_modes
from lcm_sawtooth_resonant_source_sectors import (
    _direct_fully_resonant_totals,
    _frequency_batch,
    _frequency_entries,
    _quotient_sector_batches,
)
from lcm_sawtooth_source_ramanujan import (
    _prime_power_factors,
    _primitive_numerators,
)


def _one_orientation_count_source_modes(
        period, conductor, odd_partner):
    doubled_partner = 2 * odd_partner
    if (math.gcd(conductor, doubled_partner) != 1
            or conductor * doubled_partner != period):
        raise ValueError("count split requires coprime product denominators")
    sources = ({}, {}, {})
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
            for left_count, left_modes in enumerate(left_parts):
                for right_count, right_modes in enumerate(right_parts):
                    count = left_count + right_count
                    combined = sources[count].setdefault(source_residue, {})
                    for left_frequency, left_coefficient in left_modes:
                        for right_frequency, right_coefficient in right_modes:
                            frequency = (
                                left_frequency - right_frequency) % period
                            combined[frequency] = (
                                combined.get(frequency, 0.0j)
                                + left_coefficient
                                * np.conjugate(right_coefficient))
    return sources


def _shapley_values(players, game_values):
    player_count = len(players)
    factorial = math.factorial
    denominator = factorial(player_count)
    values = {}
    for player in players:
        others = tuple(value for value in players if value != player)
        contribution = 0.0
        for subset_size in range(len(others) + 1):
            weight = (
                factorial(subset_size)
                * factorial(player_count - subset_size - 1)
                / denominator)
            for subset in itertools.combinations(others, subset_size):
                base = frozenset(subset)
                contribution += weight * (
                    game_values[base | {player}] - game_values[base])
        values[player] = contribution
    return values


def cotangent_count_source_receipt(
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
        raise ValueError("cotangent count requires squarefree period")
    primes = tuple(prime for prime, _ in factors)
    common = math.gcd(lag, period)
    quotient = period // common
    if math.gcd(common, quotient) != 1:
        raise ValueError("cotangent count requires coprime CRT parts")
    common_primes = tuple(prime for prime in primes if common % prime == 0)
    quotient_primes = tuple(prime for prime in primes if quotient % prime == 0)
    shape = tuple(prime - 1 for prime in primes)
    unit_class_count = math.prod(shape)
    sectors = tuple(
        tuple(prime for index, prime in enumerate(quotient_primes)
              if mask & (1 << index))
        for mask in range(1 << len(quotient_primes)))

    left_components = _one_orientation_count_source_modes(
        period, *families[0])
    right_components = _one_orientation_count_source_modes(
        period, *families[1])
    left_entries = tuple(
        _frequency_entries(sources, primes) for sources in left_components)
    right_entries = tuple(
        _frequency_entries(sources, primes) for sources in right_components)
    count_sector_totals = {
        count: {sector: np.zeros(period, dtype=complex) for sector in sectors}
        for count in range(5)}

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
        for left_count, (left_frequencies, left_sectors) in enumerate(
                left_data):
            if not left_frequencies:
                continue
            for right_count, (right_frequencies, right_sectors) in enumerate(
                    right_data):
                if not right_frequencies:
                    continue
                count = left_count + right_count
                totals = count_sector_totals[count]
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

    def masses(included_counts):
        if not included_counts:
            return 0.0, 0.0, 0.0
        sector_values = {
            sector: sum(count_sector_totals[count][sector]
                        for count in included_counts)
            for sector in sectors}
        sectorwise_mass = sum(
            float(np.sum(np.abs(values[resonant_frequencies])))
            for values in sector_values.values()) / unit_class_count
        recombined = sum(sector_values.values())
        recombined_mass = (
            float(np.sum(np.abs(recombined[resonant_frequencies])))
            / unit_class_count)
        return sectorwise_mass, recombined_mass, sectorwise_mass - recombined_mass

    exact_count_masses = {
        count: masses((count,)) for count in range(5)}
    even_players = (0, 2, 4)
    even_game_values = {}
    for subset_size in range(len(even_players) + 1):
        for subset in itertools.combinations(even_players, subset_size):
            even_game_values[frozenset(subset)] = masses(subset)[2]
    even_shapley_losses = _shapley_values(even_players, even_game_values)
    even_full_loss = even_game_values[frozenset(even_players)]
    even_full_sectorwise_mass, even_full_recombined_mass, _ = masses(
        even_players)
    full_sectorwise_mass, full_recombined_mass, full_recombination_loss = (
        masses(tuple(range(5))))
    even_shapley_loss_fractions = {
        count: (value / even_full_loss if even_full_loss != 0 else None)
        for count, value in even_shapley_losses.items()}

    combined_left = _combine_components(left_components)
    combined_right = _combine_components(right_components)
    original_left = _oriented_family_source_modes(
        period, *families[0])[0]
    original_right = _oriented_family_source_modes(
        period, *families[1])[0]
    maximum_source_count_reconstruction_relative_error = max(
        _source_coefficient_relative_error(original_left, combined_left),
        _source_coefficient_relative_error(original_right, combined_right))
    direct_totals = _direct_fully_resonant_totals(
        period, lag, combined_left, combined_right)
    reconstructed_totals = sum(
        values for totals in count_sector_totals.values()
        for values in totals.values())
    errors = np.abs(
        reconstructed_totals[resonant_frequencies]
        - direct_totals[resonant_frequencies])
    natural_scale = np.maximum(
        1.0,
        sum(np.abs(values[resonant_frequencies])
            for totals in count_sector_totals.values()
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
        "exact_count_sectorwise_masses": {
            count: values[0] for count, values in exact_count_masses.items()},
        "exact_count_recombined_masses": {
            count: values[1] for count, values in exact_count_masses.items()},
        "exact_count_recombination_losses": {
            count: values[2] for count, values in exact_count_masses.items()},
        "even_full_recombination_loss": even_full_loss,
        "even_full_sectorwise_mass": even_full_sectorwise_mass,
        "even_full_recombined_mass": even_full_recombined_mass,
        "even_count_shapley_recombination_losses": even_shapley_losses,
        "even_count_shapley_recombination_loss_fractions": (
            even_shapley_loss_fractions),
        "full_sectorwise_mass": full_sectorwise_mass,
        "full_recombined_mass": full_recombined_mass,
        "full_recombination_loss": full_recombination_loss,
        "full_recombination_quotient": (
            full_recombined_mass / full_sectorwise_mass
            if full_sectorwise_mass > 0 else None),
        "maximum_source_count_reconstruction_relative_error": (
            maximum_source_count_reconstruction_relative_error),
        "maximum_reconstruction_natural_scale_relative_error": (
            maximum_reconstruction_natural_scale_relative_error),
        "cotangent_count_reconstruction_passes": bool(
            maximum_source_count_reconstruction_relative_error <= tolerance
            and maximum_reconstruction_natural_scale_relative_error
            <= tolerance),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def cotangent_count_discriminator_receipt(tolerance=1e-12):
    strong = cotangent_count_source_receipt(lag=130, tolerance=tolerance)
    weak = cotangent_count_source_receipt(lag=70, tolerance=tolerance)
    strong_fraction = strong[
        "even_count_shapley_recombination_loss_fractions"][2]
    weak_fraction = weak[
        "even_count_shapley_recombination_loss_fractions"][2]
    return {
        "strong_quotient": strong["quotient_period"],
        "weak_quotient": weak["quotient_period"],
        "strong_count_two_shapley_loss_fraction": strong_fraction,
        "weak_count_two_shapley_loss_fraction": weak_fraction,
        "minimum_strong_count_two_shapley_loss_fraction": .75,
        "maximum_weak_count_two_shapley_loss_fraction": .25,
        "strong_count_two_gate_passes": bool(strong_fraction >= .75),
        "weak_count_two_gate_passes": bool(weak_fraction <= .25),
        "cotangent_count_discriminator_passes": bool(
            strong_fraction >= .75 and weak_fraction <= .25),
        "both_reconstructions_pass": bool(
            strong["cotangent_count_reconstruction_passes"]
            and weak["cotangent_count_reconstruction_passes"]),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def two_prime_cotangent_count_receipt(tolerance=1e-12):
    quotient_lags = {
        35: 286,
        55: 182,
        65: 154,
        77: 130,
        91: 110,
        143: 70,
    }
    results = {
        quotient: cotangent_count_source_receipt(
            lag=lag, tolerance=tolerance)
        for quotient, lag in quotient_lags.items()}
    count_four_recombination_quotients = {
        quotient: (
            result["exact_count_recombined_masses"][4]
            / result["exact_count_sectorwise_masses"][4])
        for quotient, result in results.items()}
    count_two_to_four_sector_mass_ratios = {
        quotient: (
            result["exact_count_sectorwise_masses"][2]
            / result["exact_count_sectorwise_masses"][4])
        for quotient, result in results.items()}
    full_recombination_quotients = {
        quotient: result["full_recombination_quotient"]
        for quotient, result in results.items()}
    mass_ratio_classifier_matches = {
        quotient: bool(
            (count_two_to_four_sector_mass_ratios[quotient] <= 1)
            == (full_recombination_quotients[quotient] <= .25))
        for quotient in quotient_lags}
    return {
        "quotients": tuple(quotient_lags),
        "count_four_recombination_quotients": (
            count_four_recombination_quotients),
        "count_two_to_four_sector_mass_ratios": (
            count_two_to_four_sector_mass_ratios),
        "count_four_shapley_loss_fractions": {
            quotient: result[
                "even_count_shapley_recombination_loss_fractions"][4]
            for quotient, result in results.items()},
        "full_recombination_quotients": full_recombination_quotients,
        "all_count_four_recombination_gates_pass": all(
            value <= .25
            for value in count_four_recombination_quotients.values()),
        "mass_ratio_classifier_matches": mass_ratio_classifier_matches,
        "all_mass_ratio_classifier_predictions_match": all(
            mass_ratio_classifier_matches.values()),
        "all_reconstructions_pass": all(
            result["cotangent_count_reconstruction_passes"]
            for result in results.values()),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def three_prime_cotangent_count_receipt(tolerance=1e-12):
    quotient_lags = {
        385: 156,
        455: 22,
        715: 14,
        1001: 240,
    }
    results = {
        quotient: cotangent_count_source_receipt(
            lag=lag, tolerance=tolerance)
        for quotient, lag in quotient_lags.items()}
    count_four_shares = {
        quotient: result[
            "even_count_shapley_recombination_loss_fractions"][4]
        for quotient, result in results.items()}
    count_four_recombination_quotients = {
        quotient: (
            result["exact_count_recombined_masses"][4]
            / result["exact_count_sectorwise_masses"][4])
        for quotient, result in results.items()}
    full_quotients = {
        quotient: result["full_recombination_quotient"]
        for quotient, result in results.items()}
    contains_five_predictions_match = {
        quotient: bool(
            ((quotient % 5 == 0) == (count_four_shares[quotient] >= .75)))
        for quotient in quotient_lags}
    return {
        "quotients": tuple(quotient_lags),
        "count_four_shapley_loss_fractions": count_four_shares,
        "count_four_recombination_quotients": (
            count_four_recombination_quotients),
        "full_recombination_quotients": full_quotients,
        "minimum_count_four_shapley_loss_fraction": .75,
        "leading_dimension_stability_gate_passes": bool(
            count_four_shares[385] >= .75
            and count_four_shares[1001] >= .75),
        "contains_five_predictions_match": contains_five_predictions_match,
        "all_contains_five_predictions_match": all(
            contains_five_predictions_match.values()),
        "all_reconstructions_pass": all(
            result["cotangent_count_reconstruction_passes"]
            for result in results.values()),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(cotangent_count_discriminator_receipt())
