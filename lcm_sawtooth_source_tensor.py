"""CRT tensor decomposition of the finite source-residue difference graph."""

import math

import numpy as np

from lcm_sawtooth_ramanujan_class_mean import _mobius
from lcm_sawtooth_source_ramanujan import (
    _divisors,
    _family_source_modes,
    _prime_power_factors,
)


LEADING_LAG_PHASE_REMOVED_TARGETS = {
    140: (-85437 / 4, 0.0),
    154: (20185 / 9, 0.0),
    156: (12375 / 2, 0.0),
    182: (207647 / 60, 0.0),
    240: (-27225 / 2, 0.0),
}


def _source_value_tensor(period, primes, sources, sample, sample_modulus):
    shape = tuple(prime - 1 for prime in primes)
    tensor = np.zeros(shape, dtype=complex)
    vector = np.zeros(period, dtype=complex)
    for residue, modes in sources.items():
        value = sum(
            coefficient * np.exp(
                2j * np.pi * (frequency % sample_modulus)
                * sample / sample_modulus)
            for frequency, coefficient in modes.items())
        tensor[tuple(residue % prime - 1 for prime in primes)] = value
        vector[residue] = value
    return tensor, vector


def _quotient_sector_components(tensor, primes, quotient_primes):
    components = {(): tensor}
    for prime in quotient_primes:
        axis = primes.index(prime)
        next_components = {}
        for sector, component in components.items():
            constant = np.broadcast_to(
                np.mean(component, axis=axis, keepdims=True),
                component.shape)
            next_components[sector] = constant
            next_components[sector + (prime,)] = component - constant
        components = next_components
    return components


def source_tensor_receipt(
        families=((77, 65), (143, 35)), lag=182,
        phase_removed_target=(207647 / 60, 0.0), tolerance=1e-12):
    families = tuple(families)
    if (len(families) != 2 or any(len(family) != 2 for family in families)
            or any(type(c) is not int or c < 3 or c % 2 == 0
                   or type(d) is not int or d < 3 or d % 2 == 0
                   for c, d in families)):
        raise ValueError("require two odd conductor-partner families")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    periods = tuple(math.lcm(c, 2 * d) for c, d in families)
    if len(periods) != 2 or len(set(periods)) != 1:
        raise ValueError("require two families with one source period")
    period = periods[0]
    if type(lag) is not int or not 0 < lag < period:
        raise ValueError("lag must lie strictly inside the period")
    common = math.gcd(lag, period)
    quotient = period // common
    period_factors = _prime_power_factors(period)
    if any(prime != prime_power for prime, prime_power in period_factors):
        raise ValueError("tensor decomposition currently requires squarefree Q")
    primes = tuple(prime for prime, _ in period_factors)
    quotient_primes = tuple(prime for prime in primes if quotient % prime == 0)
    left_sources, _ = _family_source_modes(period, *families[0])
    right_sources, _ = _family_source_modes(period, *families[1])
    differences = np.asarray(tuple(
        common * reduced for reduced in range(quotient)
        if math.gcd(reduced, quotient) == 1), dtype=np.int64)

    sample_sector_correlations = []
    maximum_sample_reconstruction_absolute_error = 0.0
    maximum_sample_natural_scale_relative_error = 0.0
    graph_degree = math.prod(prime - 2 for prime in quotient_primes)
    for sample in range(common):
        left_tensor, left_vector = _source_value_tensor(
            period, primes, left_sources, sample, common)
        right_tensor, right_vector = _source_value_tensor(
            period, primes, right_sources, sample, common)
        left_components = _quotient_sector_components(
            left_tensor, primes, quotient_primes)
        right_components = _quotient_sector_components(
            right_tensor, primes, quotient_primes)
        sector_correlations = {}
        for sector in left_components:
            eigenvalue = math.prod(
                -1 if prime in sector else prime - 2
                for prime in quotient_primes)
            sector_correlations[sector] = complex(
                eigenvalue * np.vdot(
                    right_components[sector], left_components[sector]))
        tensor_total = sum(sector_correlations.values())
        direct_correlation = np.fft.ifft(
            np.fft.fft(left_vector)
            * np.conjugate(np.fft.fft(right_vector)))
        direct_total = complex(np.sum(direct_correlation[differences]))
        absolute_error = abs(tensor_total - direct_total)
        natural_scale = max(
            1.0,
            graph_degree
            * float(np.linalg.norm(left_tensor.ravel()))
            * float(np.linalg.norm(right_tensor.ravel())))
        natural_scale_relative_error = absolute_error / natural_scale
        maximum_sample_reconstruction_absolute_error = max(
            maximum_sample_reconstruction_absolute_error, absolute_error)
        maximum_sample_natural_scale_relative_error = max(
            maximum_sample_natural_scale_relative_error,
            natural_scale_relative_error)
        sample_sector_correlations.append(sector_correlations)

    sector_phase_removed_totals = {
        sector: 0.0j for sector in sample_sector_correlations[0]}
    for divisor in _divisors(common):
        weight = _mobius(common // divisor)
        for sample_index in np.arange(divisor) * (common // divisor):
            for sector, value in sample_sector_correlations[
                    int(sample_index)].items():
                sector_phase_removed_totals[sector] += weight * value
    unit_class_count = math.prod(prime - 1 for prime in primes)
    sector_phase_removed_means = {
        sector: complex(value / unit_class_count)
        for sector, value in sector_phase_removed_totals.items()}
    tensor_phase_removed_mean = sum(sector_phase_removed_means.values())
    target = complex(*phase_removed_target)
    target_relative_error = (
        abs(tensor_phase_removed_mean - target)
        / max(1.0, abs(target)))
    return {
        "families": tuple(families),
        "arithmetic_period": period,
        "lag": lag,
        "gcd_lag_period": common,
        "quotient_period": quotient,
        "quotient_primes": quotient_primes,
        "sector_eigenvalues": {
            sector: math.prod(
                -1 if prime in sector else prime - 2
                for prime in quotient_primes)
            for sector in sector_phase_removed_means},
        "sector_phase_removed_mean_correlations": {
            sector: (value.real, value.imag)
            for sector, value in sector_phase_removed_means.items()},
        "tensor_phase_removed_mean_correlation": (
            tensor_phase_removed_mean.real, tensor_phase_removed_mean.imag),
        "graph_degree": graph_degree,
        "maximum_sample_reconstruction_absolute_error": (
            maximum_sample_reconstruction_absolute_error),
        "maximum_sample_natural_scale_relative_error": (
            maximum_sample_natural_scale_relative_error),
        "phase_removed_target_relative_error": target_relative_error,
        "tensor_difference_graph_identity_passes": bool(
            maximum_sample_natural_scale_relative_error <= tolerance
            and target_relative_error <= tolerance),
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


def leading_lag_source_tensor_receipt(tolerance=1e-12):
    results = {
        lag: source_tensor_receipt(
            lag=lag, phase_removed_target=target, tolerance=tolerance)
        for lag, target in LEADING_LAG_PHASE_REMOVED_TARGETS.items()}
    return {
        "lags": tuple(results),
        "quotient_primes": {
            lag: result["quotient_primes"]
            for lag, result in results.items()},
        "sector_phase_removed_mean_correlations": {
            lag: result["sector_phase_removed_mean_correlations"]
            for lag, result in results.items()},
        "maximum_sample_natural_scale_relative_error": max(
            result["maximum_sample_natural_scale_relative_error"]
            for result in results.values()),
        "maximum_phase_removed_target_relative_error": max(
            result["phase_removed_target_relative_error"]
            for result in results.values()),
        "all_tensor_difference_graph_identities_pass": all(
            result["tensor_difference_graph_identity_passes"]
            for result in results.values()),
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(source_tensor_receipt())
