"""Source-level CRT/Ramanujan evaluation of one packet correlation lag.

Unlike the generic periodic projection, this module expands the primitive-root
endpoint terms before averaging over frame residues.  The congruence selecting
one correlation lag is solved by CRT, leaving a Ramanujan sum on the conductor
side.  Unit frame classes are not enumerated by the source calculation.
"""

import math

import numpy as np

from lcm_sawtooth_ramanujan_class_mean import _ramanujan_sum


LEADING_LAG_CANONICAL_TARGETS = {
    140: (-16521.656388184376, -726.4019852849893),
    154: (-8510.359796742974, -411.64495068670993),
    156: (6097.158242471013, 298.754919837435),
    182: (-25042.404948829204, -1431.9765245642232),
    240: (-18481.48402179967, -1394.7176473717648),
}


def _primitive_numerators(denominator):
    return tuple(
        value for value in range(1, denominator)
        if math.gcd(value, denominator) == 1)


def _endpoint_modes(period, denominator, numerator):
    """Return frequency coefficients of G_(p,D)(a) as a function of p."""
    root = np.exp(2j * np.pi * numerator / denominator)
    denominator_value = root - 1
    frequency = numerator * (period // denominator) % period
    return (
        (frequency, 1 / denominator_value),
        (0, -root / denominator_value),
    )


def _family_source_modes(period, conductor, odd_partner):
    """Map each unreduced source residue to its endpoint Fourier modes."""
    doubled_partner = 2 * odd_partner
    if math.lcm(conductor, doubled_partner) != period:
        raise ValueError("family must have the requested source period")
    denominators = (conductor, doubled_partner)
    numerators = tuple(_primitive_numerators(value) for value in denominators)
    sources = {}
    source_pair_count = 0
    for left_index, right_index in ((0, 1), (1, 0)):
        left_denominator = denominators[left_index]
        right_denominator = denominators[right_index]
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
                source_pair_count += 1
    return sources, source_pair_count


def _conditioned_unit_exponential_sum(period, lag, difference, frequency):
    """Sum e_Q(frequency*p) over units satisfying p*difference=lag."""
    lag %= period
    difference %= period
    common = math.gcd(lag, period)
    quotient = period // common
    if math.gcd(common, quotient) != 1:
        raise ValueError("the simple CRT factorization requires coprime parts")
    if math.gcd(difference, period) != common:
        return 0.0j
    reduced_difference = (difference // common) % quotient
    reduced_lag = (lag // common) % quotient
    fixed_class = (
        reduced_lag * pow(reduced_difference, -1, quotient)) % quotient
    phase_class = (
        fixed_class * pow(common, -1, quotient)) % quotient
    phase = np.exp(2j * np.pi * (frequency % quotient)
                   * phase_class / quotient)
    return phase * _ramanujan_sum(common, frequency)


def source_ramanujan_mean_receipt(
        families=((77, 65), (143, 35)), lag=182,
        canonical_target=(-25042.404948829146, -1431.9765245642259),
        minimum_factor_seven_signed_fraction=.75,
        maximum_source_mode_cancellation_quotient=.10, tolerance=1e-12):
    """Evaluate a lag mean from source modes and conditioned CRT sums."""
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
    if not 0 < minimum_factor_seven_signed_fraction <= 1:
        raise ValueError("factor-seven fraction must lie in (0,1]")
    if not 0 < maximum_source_mode_cancellation_quotient <= 1:
        raise ValueError("cancellation quotient must lie in (0,1]")
    target = complex(*canonical_target)

    left_sources, left_pair_count = _family_source_modes(
        period, *families[0])
    right_sources, right_pair_count = _family_source_modes(
        period, *families[1])
    common = math.gcd(lag, period)
    quotient = period // common
    reduced_differences = tuple(
        value for value in range(quotient)
        if math.gcd(value, quotient) == 1)
    conditioned_cache = {}
    total = 0.0j
    absolute_mode_contribution_mass = 0.0
    frequency_gcd_totals = {}
    matched_source_residue_pairs = 0
    expanded_mode_products = 0
    for left_residue, left_modes in left_sources.items():
        for reduced_difference in reduced_differences:
            difference = common * reduced_difference
            right_residue = (left_residue - difference) % period
            right_modes = right_sources.get(right_residue)
            if right_modes is None:
                continue
            matched_source_residue_pairs += 1
            for left_frequency, left_coefficient in left_modes.items():
                for right_frequency, right_coefficient in right_modes.items():
                    frequency = (left_frequency - right_frequency) % period
                    cache_key = (reduced_difference, frequency)
                    conditioned_sum = conditioned_cache.get(cache_key)
                    if conditioned_sum is None:
                        conditioned_sum = _conditioned_unit_exponential_sum(
                            period, lag, difference, frequency)
                        conditioned_cache[cache_key] = conditioned_sum
                    contribution = (
                        left_coefficient
                        * np.conjugate(right_coefficient)
                        * conditioned_sum)
                    total += contribution
                    absolute_mode_contribution_mass += abs(contribution)
                    frequency_gcd = math.gcd(frequency, common)
                    frequency_gcd_totals[frequency_gcd] = (
                        frequency_gcd_totals.get(frequency_gcd, 0.0j)
                        + contribution)
                    expanded_mode_products += 1

    unit_class_count = math.prod(
        prime_power - prime_power // prime
        for prime, prime_power in _prime_power_factors(period))
    source_mean = complex(total / unit_class_count)
    normalized_absolute_mode_contribution_mass = (
        absolute_mode_contribution_mass / unit_class_count)
    source_mode_cancellation_quotient = (
        abs(source_mean) / normalized_absolute_mode_contribution_mass
        if normalized_absolute_mode_contribution_mass > 0 else None)
    frequency_gcd_means = {
        divisor: complex(subtotal / unit_class_count)
        for divisor, subtotal in sorted(frequency_gcd_totals.items())}
    common_primes = tuple(prime for prime, _ in _prime_power_factors(common))
    prime_frequency_means = {
        prime: sum(
            subtotal for divisor, subtotal in frequency_gcd_means.items()
            if divisor % prime == 0)
        for prime in common_primes}
    prime_frequency_signed_real_fractions = {
        prime: abs(subtotal.real) / max(1.0, abs(source_mean.real))
        for prime, subtotal in prime_frequency_means.items()}
    frequency_equal_share_means = {prime: 0.0j for prime in common_primes}
    for divisor, subtotal in frequency_gcd_means.items():
        active_primes = tuple(
            prime for prime in common_primes if divisor % prime == 0)
        if active_primes:
            share = subtotal / len(active_primes)
            for prime in active_primes:
                frequency_equal_share_means[prime] += share
    empty_frequency_mean = frequency_gcd_means.get(1, 0.0j)
    equal_share_reconstruction = (
        empty_frequency_mean + sum(frequency_equal_share_means.values()))
    equal_share_reconstruction_relative_error = (
        abs(equal_share_reconstruction - source_mean)
        / max(1.0, abs(source_mean)))
    largest_absolute_equal_share_prime = (
        max(common_primes,
            key=lambda prime: abs(frequency_equal_share_means[prime]))
        if common_primes else None)
    factor_seven_has_largest_absolute_equal_share = (
        largest_absolute_equal_share_prime == 7)
    factor_seven_mean = prime_frequency_means.get(7, 0.0j)
    factor_seven_signed_fraction = (
        abs(factor_seven_mean.real) / max(1.0, abs(source_mean.real)))
    factor_seven_signed_fraction_passes = bool(
        source_mean.real < 0
        and factor_seven_mean.real < 0
        and factor_seven_signed_fraction
        >= minimum_factor_seven_signed_fraction)
    relative_error = abs(source_mean - target) / max(1.0, abs(target))
    return {
        "families": families,
        "arithmetic_period": period,
        "lag": lag,
        "gcd_lag_period": common,
        "quotient_period": quotient,
        "unit_class_count": unit_class_count,
        "left_source_pair_count": left_pair_count,
        "right_source_pair_count": right_pair_count,
        "left_source_residue_count": len(left_sources),
        "right_source_residue_count": len(right_sources),
        "matched_source_residue_pairs": matched_source_residue_pairs,
        "expanded_mode_products": expanded_mode_products,
        "conditioned_sum_cache_size": len(conditioned_cache),
        "source_ramanujan_mean_correlation": (
            source_mean.real, source_mean.imag),
        "normalized_absolute_mode_contribution_mass": (
            normalized_absolute_mode_contribution_mass),
        "source_mode_cancellation_quotient": (
            source_mode_cancellation_quotient),
        "maximum_source_mode_cancellation_quotient": (
            maximum_source_mode_cancellation_quotient),
        "source_mode_cancellation_gate_passes": bool(
            source_mode_cancellation_quotient is not None
            and source_mode_cancellation_quotient
            <= maximum_source_mode_cancellation_quotient),
        "frequency_gcd_mean_correlations": {
            divisor: (subtotal.real, subtotal.imag)
            for divisor, subtotal in frequency_gcd_means.items()},
        "factor_seven_frequency_mean_correlation": (
            factor_seven_mean.real, factor_seven_mean.imag),
        "prime_frequency_mean_correlations": {
            prime: (subtotal.real, subtotal.imag)
            for prime, subtotal in prime_frequency_means.items()},
        "prime_frequency_signed_real_fractions": (
            prime_frequency_signed_real_fractions),
        "empty_frequency_mean_correlation": (
            empty_frequency_mean.real, empty_frequency_mean.imag),
        "frequency_equal_share_mean_correlations": {
            prime: (subtotal.real, subtotal.imag)
            for prime, subtotal in frequency_equal_share_means.items()},
        "equal_share_reconstruction_relative_error": (
            equal_share_reconstruction_relative_error),
        "largest_absolute_equal_share_prime": (
            largest_absolute_equal_share_prime),
        "factor_seven_has_largest_absolute_equal_share": (
            factor_seven_has_largest_absolute_equal_share),
        "factor_seven_signed_real_fraction": factor_seven_signed_fraction,
        "minimum_factor_seven_signed_fraction": (
            minimum_factor_seven_signed_fraction),
        "factor_seven_signed_fraction_passes": (
            factor_seven_signed_fraction_passes),
        "canonical_unit_mean_target": (target.real, target.imag),
        "source_to_canonical_relative_error": relative_error,
        "source_term_ramanujan_reduction_proved": bool(
            relative_error <= tolerance),
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def _prime_power_factors(value):
    factors = []
    prime = 2
    remaining = value
    while prime * prime <= remaining:
        if remaining % prime == 0:
            prime_power = 1
            while remaining % prime == 0:
                remaining //= prime
                prime_power *= prime
            factors.append((prime, prime_power))
        prime += 1
    if remaining > 1:
        factors.append((remaining, remaining))
    return tuple(factors)


def leading_lag_source_receipt(tolerance=1e-12):
    """Test the source reduction on the five leading finite lag pairs."""
    results = {
        lag: source_ramanujan_mean_receipt(
            lag=lag, canonical_target=target, tolerance=tolerance)
        for lag, target in LEADING_LAG_CANONICAL_TARGETS.items()}
    maximum_relative_error = max(
        result["source_to_canonical_relative_error"]
        for result in results.values())
    return {
        "lags": tuple(results),
        "lag_gcds": {
            lag: result["gcd_lag_period"]
            for lag, result in results.items()},
        "source_mean_correlations": {
            lag: result["source_ramanujan_mean_correlation"]
            for lag, result in results.items()},
        "source_to_canonical_relative_errors": {
            lag: result["source_to_canonical_relative_error"]
            for lag, result in results.items()},
        "source_mode_cancellation_quotients": {
            lag: result["source_mode_cancellation_quotient"]
            for lag, result in results.items()},
        "maximum_source_mode_cancellation_quotient": max(
            result["source_mode_cancellation_quotient"]
            for result in results.values()),
        "all_source_mode_cancellation_gates_pass": all(
            result["source_mode_cancellation_gate_passes"]
            for result in results.values()),
        "maximum_source_to_canonical_relative_error": maximum_relative_error,
        "all_leading_lag_source_reductions_pass": bool(
            maximum_relative_error <= tolerance),
        "unit_frame_classes_enumerated_by_source_calculation": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(source_ramanujan_mean_receipt())
