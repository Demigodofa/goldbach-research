"""Primitive cotangent transforms and count-four sawtooth reconstruction."""

import math

import numpy as np

from lcm_sawtooth_cotangent_count import (
    _one_orientation_count_source_modes,
)
from lcm_sawtooth_cotangent_parity import (
    _source_coefficient_relative_error,
)
from lcm_sawtooth_resonant_source_sectors import (
    _direct_fully_resonant_totals,
    _frequency_batch,
    _frequency_entries,
    _quotient_sector_batches,
)
from lcm_sawtooth_source_ramanujan import (
    _divisors,
    _mobius,
    _prime_power_factors,
    _primitive_numerators,
)


ENDPOINT_DENOMINATORS = (77, 130, 143, 70)


def _primitive_cotangent_transform_formula(denominator, frequency):
    total = 0
    for modulus in _divisors(denominator):
        residue = frequency % modulus
        sawtooth_transform = (
            0 if residue == 0 else modulus - 2 * residue)
        total += _mobius(denominator // modulus) * sawtooth_transform
    return 1j * total


def _primitive_cotangent_transform_direct(denominator, frequency):
    return sum(
        (1 / math.tan(math.pi * numerator / denominator))
        * np.exp(2j * np.pi * numerator * frequency / denominator)
        for numerator in _primitive_numerators(denominator))


def _primitive_cotangent_inverse_transform_value(denominator, numerator):
    # The integer sawtooth is odd under n -> D-n. Pairing those terms
    # enforces the exactly real inverse and avoids subtracting rounded cosines.
    paired_terms = []
    for frequency in range(1, (denominator + 1) // 2):
        sawtooth_value = int(_primitive_cotangent_transform_formula(
            denominator, frequency).imag)
        angle_residue = (numerator * frequency) % denominator
        paired_terms.append(
            2 * sawtooth_value * math.sin(
                2 * math.pi * angle_residue / denominator))
    if denominator % 2 == 0:
        midpoint = int(_primitive_cotangent_transform_formula(
            denominator, denominator // 2).imag)
        if midpoint != 0:
            raise AssertionError("unpaired cotangent transform midpoint")
    return complex(math.fsum(paired_terms) / denominator, 0.0)


def _cotangent_from_sawtooth_transform(denominator, numerator):
    return float(_primitive_cotangent_inverse_transform_value(
        denominator, numerator).real)


def primitive_cotangent_transform_receipt(
        denominators=ENDPOINT_DENOMINATORS, tolerance=1e-12):
    denominators = tuple(denominators)
    if (not denominators
            or any(type(value) is not int or value < 3
                   for value in denominators)):
        raise ValueError("denominators must be integers at least three")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    rows = {}
    for denominator in denominators:
        maximum_transform_natural_scale_relative_error = 0.0
        for frequency in range(denominator):
            direct_terms = tuple(
                (1 / math.tan(math.pi * numerator / denominator))
                * np.exp(2j * np.pi * numerator * frequency / denominator)
                for numerator in _primitive_numerators(denominator))
            direct = sum(direct_terms)
            formula = _primitive_cotangent_transform_formula(
                denominator, frequency)
            natural_scale = max(
                1.0, sum(abs(term) for term in direct_terms))
            maximum_transform_natural_scale_relative_error = max(
                maximum_transform_natural_scale_relative_error,
                abs(direct - formula) / natural_scale)
        maximum_inverse_relative_error = max(
            abs(_primitive_cotangent_inverse_transform_value(
                denominator, numerator)
                - 1 / math.tan(math.pi * numerator / denominator))
            / max(1.0, abs(1 / math.tan(
                math.pi * numerator / denominator)))
            for numerator in _primitive_numerators(denominator))
        rows[denominator] = {
            "maximum_transform_natural_scale_relative_error": (
                maximum_transform_natural_scale_relative_error),
            "maximum_inverse_relative_error": maximum_inverse_relative_error,
            "primitive_cotangent_sawtooth_identity_passes": bool(
                maximum_transform_natural_scale_relative_error <= tolerance
                and maximum_inverse_relative_error <= tolerance),
        }
    return {
        "denominators": denominators,
        "rows": rows,
        "maximum_transform_natural_scale_relative_error": max(
            row["maximum_transform_natural_scale_relative_error"]
            for row in rows.values()),
        "maximum_inverse_relative_error": max(
            row["maximum_inverse_relative_error"]
            for row in rows.values()),
        "all_primitive_cotangent_sawtooth_identities_pass": all(
            row["primitive_cotangent_sawtooth_identity_passes"]
            for row in rows.values()),
    }


def _transformed_count_two_source_modes(
        period, conductor, odd_partner):
    doubled_partner = 2 * odd_partner
    if (math.gcd(conductor, doubled_partner) != 1
            or conductor * doubled_partner != period):
        raise ValueError("count-two transform requires coprime product parts")
    left_cotangents = {
        numerator: _cotangent_from_sawtooth_transform(
            conductor, numerator)
        for numerator in _primitive_numerators(conductor)}
    right_cotangents = {
        numerator: _cotangent_from_sawtooth_transform(
            doubled_partner, numerator)
        for numerator in _primitive_numerators(doubled_partner)}
    sources = {}
    for left_numerator, left_cotangent in left_cotangents.items():
        left_frequency = left_numerator * (period // conductor)
        left_modes = (
            (left_frequency, -.5j * left_cotangent),
            (0, .5j * left_cotangent),
        )
        for right_numerator, right_cotangent in right_cotangents.items():
            right_frequency = (
                right_numerator * (period // doubled_partner))
            right_modes = (
                (right_frequency, -.5j * right_cotangent),
                (0, .5j * right_cotangent),
            )
            source_residue = (left_frequency - right_frequency) % period
            combined = sources.setdefault(source_residue, {})
            for left_mode_frequency, left_coefficient in left_modes:
                for right_mode_frequency, right_coefficient in right_modes:
                    frequency = (
                        left_mode_frequency - right_mode_frequency) % period
                    combined[frequency] = (
                        combined.get(frequency, 0.0j)
                        + left_coefficient
                        * np.conjugate(right_coefficient))
    return sources


def _count_four_sector_totals(
        period, lag, left_sources, right_sources):
    factors = _prime_power_factors(period)
    primes = tuple(prime for prime, _ in factors)
    common = math.gcd(lag, period)
    quotient = period // common
    common_primes = tuple(prime for prime in primes if common % prime == 0)
    quotient_primes = tuple(prime for prime in primes if quotient % prime == 0)
    shape = tuple(prime - 1 for prime in primes)
    sectors = tuple(
        tuple(prime for index, prime in enumerate(quotient_primes)
              if mask & (1 << index))
        for mask in range(1 << len(quotient_primes)))
    left_entries = _frequency_entries(left_sources, primes)
    right_entries = _frequency_entries(right_sources, primes)
    totals = {
        sector: np.zeros(period, dtype=complex) for sector in sectors}
    for residue_class in range(quotient):
        left_frequencies = tuple(
            frequency for frequency in left_entries
            if frequency % quotient == residue_class)
        right_frequencies = tuple(
            frequency for frequency in right_entries
            if frequency % quotient == residue_class)
        if not left_frequencies or not right_frequencies:
            continue
        left_sectors = _quotient_sector_batches(
            _frequency_batch(left_entries, left_frequencies, shape),
            primes, quotient_primes)
        right_sectors = _quotient_sector_batches(
            _frequency_batch(right_entries, right_frequencies, shape),
            primes, quotient_primes)
        for sector in sectors:
            eigenvalue = math.prod(
                -1 if prime in sector else prime - 2
                for prime in quotient_primes)
            pairings = (
                left_sectors[sector].reshape(len(left_frequencies), -1)
                @ np.conjugate(right_sectors[sector]).reshape(
                    len(right_frequencies), -1).T)
            for left_row, left_frequency in enumerate(left_frequencies):
                for right_row, right_frequency in enumerate(right_frequencies):
                    frequency = (
                        left_frequency - right_frequency) % period
                    common_multiplier = math.prod(
                        prime - 1 if frequency % prime == 0 else -1
                        for prime in common_primes)
                    totals[sector][frequency] += (
                        common_multiplier * eigenvalue
                        * pairings[left_row, right_row])
    return quotient, sectors, totals


def cotangent_sawtooth_count_four_receipt(
        families=((77, 65), (143, 35)), lags=(130, 110), tolerance=1e-12):
    families = tuple(families)
    lags = tuple(lags)
    if (len(families) != 2 or any(len(family) != 2 for family in families)
            or any(type(c) is not int or c < 3 or c % 2 == 0
                   or type(d) is not int or d < 3 or d % 2 == 0
                   for c, d in families)):
        raise ValueError("require two odd conductor-partner families")
    periods = tuple(math.lcm(c, 2 * d) for c, d in families)
    if len(set(periods)) != 1:
        raise ValueError("families must share one arithmetic period")
    period = periods[0]
    factors = _prime_power_factors(period)
    if any(prime != prime_power for prime, prime_power in factors):
        raise ValueError("count-four transform requires squarefree period")
    if (not lags or any(type(lag) is not int or not 0 < lag < period
                        for lag in lags)):
        raise ValueError("lags must lie strictly inside the period")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    direct_left = _one_orientation_count_source_modes(
        period, *families[0])[2]
    direct_right = _one_orientation_count_source_modes(
        period, *families[1])[2]
    transformed_left = _transformed_count_two_source_modes(
        period, *families[0])
    transformed_right = _transformed_count_two_source_modes(
        period, *families[1])
    maximum_source_relative_error = max(
        _source_coefficient_relative_error(direct_left, transformed_left),
        _source_coefficient_relative_error(direct_right, transformed_right))
    rows = {}
    for lag in lags:
        quotient, sectors, direct_sectors = _count_four_sector_totals(
            period, lag, direct_left, direct_right)
        transformed_quotient, transformed_sectors, transformed_totals = (
            _count_four_sector_totals(
                period, lag, transformed_left, transformed_right))
        if (quotient != transformed_quotient
                or sectors != transformed_sectors):
            raise AssertionError("inconsistent transformed sector indexing")
        resonant_frequencies = np.arange(0, period, quotient)
        maximum_sector_natural_scale_relative_error = 0.0
        for frequency in resonant_frequencies:
            natural_scale = max(
                1.0,
                sum(abs(direct_sectors[sector][frequency])
                    for sector in sectors))
            maximum_sector_natural_scale_relative_error = max(
                maximum_sector_natural_scale_relative_error,
                max(abs(transformed_totals[sector][frequency]
                        - direct_sectors[sector][frequency]) / natural_scale
                    for sector in sectors))
        direct_conditioned = _direct_fully_resonant_totals(
            period, lag, direct_left, direct_right)
        sector_reconstruction = sum(direct_sectors.values())
        maximum_direct_reconstruction_natural_scale_relative_error = max(
            abs(sector_reconstruction[frequency]
                - direct_conditioned[frequency])
            / max(1.0, sum(abs(direct_sectors[sector][frequency])
                           for sector in sectors))
            for frequency in resonant_frequencies)
        rows[lag] = {
            "quotient_period": quotient,
            "maximum_sector_natural_scale_relative_error": (
                maximum_sector_natural_scale_relative_error),
            "maximum_direct_reconstruction_natural_scale_relative_error": (
                maximum_direct_reconstruction_natural_scale_relative_error),
            "count_four_sawtooth_reconstruction_passes": bool(
                maximum_source_relative_error <= tolerance
                and maximum_sector_natural_scale_relative_error <= tolerance
                and maximum_direct_reconstruction_natural_scale_relative_error
                <= tolerance),
        }
    return {
        "families": families,
        "arithmetic_period": period,
        "lags": lags,
        "maximum_source_relative_error": maximum_source_relative_error,
        "rows": rows,
        "all_count_four_sawtooth_reconstructions_pass": all(
            row["count_four_sawtooth_reconstruction_passes"]
            for row in rows.values()),
        "classical_two_cotangent_product_formula_used": False,
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(cotangent_sawtooth_count_four_receipt())
