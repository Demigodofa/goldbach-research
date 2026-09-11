"""Ramanujan reconstruction of one complete prime-class lag correlation.

The canonical packet core is periodic in the frame residue modulo ``Q``.
For one leading lag, this module builds every source coefficient from the
endpoint form of its primitive-root sum, Fourier expands the resulting
``Q``-periodic correlation, and replaces averaging over unit classes by
integer Ramanujan sums.  This is an exact finite-period identity, not a
prime-distribution estimate.
"""

import math

import numpy as np

from lcm_sawtooth_prime_class_core import (
    _canonical_periodic_geometric_sum,
    _family_arithmetic_core_packet,
)


def _endpoint_geometric_sum(frame_residue, denominator, numerators):
    """Use (e_D(a*p)-e_D(a))/(e_D(a)-1) at primitive roots."""
    numerators = np.asarray(numerators, dtype=np.int64)
    root_angles = 2j * np.pi * numerators / denominator
    remainder = (frame_residue - 1) % denominator
    return (
        np.exp(root_angles) * np.expm1(root_angles * remainder)
        / np.expm1(root_angles))


def _mobius(value):
    if type(value) is not int or value < 1:
        raise ValueError("Mobius input must be a positive integer")
    result = 1
    prime = 2
    remaining = value
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            result = -result
            if remaining % prime == 0:
                return 0
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        result = -result
    return result


def _euler_phi(value):
    result = value
    prime = 2
    remaining = value
    while prime * prime <= remaining:
        if remaining % prime == 0:
            result -= result // prime
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        result -= result // remaining
    return result


def _ramanujan_sum(modulus, frequency):
    common = math.gcd(modulus, frequency)
    quotient = modulus // common
    return _mobius(quotient) * _euler_phi(modulus) // _euler_phi(quotient)


def _interval_kernel(modulus, row_count, lag):
    if lag % modulus == 0:
        return 1.0 + 0.0j
    lag %= modulus
    return (
        np.exp(1j * np.pi * (3 * row_count - 1) * lag / modulus)
        * np.sin(np.pi * row_count * lag / modulus)
        / (row_count * np.sin(np.pi * lag / modulus)))


def ramanujan_class_mean_receipt(
        families=((77, 65), (143, 35)), lag=182,
        first_row_count=28, second_row_count=34, tolerance=1e-12):
    """Reconstruct one unit-class mean correlation by Ramanujan sums."""
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
    if (type(lag) is not int or not 0 < lag < period
            or type(first_row_count) is not int or first_row_count < 1
            or type(second_row_count) is not int
            or second_row_count <= first_row_count):
        raise ValueError("invalid lag or row counts")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    units = np.asarray(tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1), dtype=np.int64)
    endpoint_correlations = np.zeros(period, dtype=complex)
    endpoint_inverse_correlations = np.zeros(period, dtype=complex)
    canonical_unit_correlations = []
    canonical_unit_inverse_correlations = []
    maximum_endpoint_packet_relative_error = 0.0
    for residue in range(period):
        endpoint_packets = tuple(
            _family_arithmetic_core_packet(
                residue, conductor, partner, _endpoint_geometric_sum)[0]
            for conductor, partner in families)
        endpoint_correlations[residue] = np.vdot(
            endpoint_packets[1], np.roll(endpoint_packets[0], -lag))
        endpoint_inverse_correlations[residue] = np.vdot(
            endpoint_packets[1], np.roll(endpoint_packets[0], lag))
        if math.gcd(residue, period) == 1:
            canonical_packets = tuple(
                _family_arithmetic_core_packet(
                    residue, conductor, partner)[0]
                for conductor, partner in families)
            maximum_endpoint_packet_relative_error = max(
                maximum_endpoint_packet_relative_error,
                *(float(np.max(
                    np.abs(endpoint - canonical)
                    / np.maximum(1.0, np.abs(canonical))))
                  for endpoint, canonical in zip(
                      endpoint_packets, canonical_packets)))
            canonical_unit_correlations.append(np.vdot(
                canonical_packets[1], np.roll(canonical_packets[0], -lag)))
            canonical_unit_inverse_correlations.append(np.vdot(
                canonical_packets[1], np.roll(canonical_packets[0], lag)))

    endpoint_unit_mean = complex(np.mean(endpoint_correlations[units]))
    endpoint_inverse_unit_mean = complex(
        np.mean(endpoint_inverse_correlations[units]))
    canonical_unit_mean = complex(np.mean(canonical_unit_correlations))
    canonical_inverse_unit_mean = complex(
        np.mean(canonical_unit_inverse_correlations))
    correlation_transform = np.fft.fft(endpoint_correlations)
    ramanujan_weights = np.asarray(tuple(
        _ramanujan_sum(period, frequency)
        for frequency in range(period)), dtype=np.int64)
    ramanujan_mean = complex(
        np.dot(correlation_transform, ramanujan_weights)
        / (period * len(units)))
    ramanujan_relative_error = (
        abs(ramanujan_mean - endpoint_unit_mean)
        / max(1.0, abs(endpoint_unit_mean)))
    endpoint_to_canonical_relative_error = (
        abs(endpoint_unit_mean - canonical_unit_mean)
        / max(1.0, abs(canonical_unit_mean)))
    inverse_conjugation_relative_error = (
        abs(canonical_inverse_unit_mean - np.conjugate(canonical_unit_mean))
        / max(1.0, abs(canonical_unit_mean)))

    kernel_change = (
        _interval_kernel(period, second_row_count, lag)
        - _interval_kernel(period, first_row_count, lag))
    inverse_lag = (-lag) % period
    inverse_kernel_change = (
        _interval_kernel(period, second_row_count, inverse_lag)
        - _interval_kernel(period, first_row_count, inverse_lag))

    def paired_reweighting(mean, inverse_mean):
        return float(2 * period * (
            (kernel_change * mean).real
            + (inverse_kernel_change * inverse_mean).real))

    endpoint_pair = paired_reweighting(
        endpoint_unit_mean, endpoint_inverse_unit_mean)
    canonical_pair = paired_reweighting(
        canonical_unit_mean, canonical_inverse_unit_mean)
    ramanujan_pair = paired_reweighting(
        ramanujan_mean, np.conjugate(ramanujan_mean))
    pair_relative_error = (
        abs(ramanujan_pair - canonical_pair)
        / max(1.0, abs(canonical_pair)))
    passes = bool(
        endpoint_to_canonical_relative_error <= tolerance
        and ramanujan_relative_error <= tolerance
        and inverse_conjugation_relative_error <= tolerance
        and pair_relative_error <= tolerance)
    return {
        "families": families,
        "arithmetic_period": period,
        "unit_class_count": len(units),
        "lag": lag,
        "inverse_lag": inverse_lag,
        "first_row_count": first_row_count,
        "second_row_count": second_row_count,
        "maximum_endpoint_packet_relative_error": (
            maximum_endpoint_packet_relative_error),
        "endpoint_packet_float_comparison_passes": bool(
            maximum_endpoint_packet_relative_error <= tolerance),
        "endpoint_unit_mean_correlation": (
            endpoint_unit_mean.real, endpoint_unit_mean.imag),
        "canonical_unit_mean_correlation": (
            canonical_unit_mean.real, canonical_unit_mean.imag),
        "endpoint_to_canonical_mean_relative_error": (
            endpoint_to_canonical_relative_error),
        "inverse_mean_conjugation_relative_error": (
            inverse_conjugation_relative_error),
        "ramanujan_reconstructed_mean_correlation": (
            ramanujan_mean.real, ramanujan_mean.imag),
        "ramanujan_mean_reconstruction_relative_error": (
            ramanujan_relative_error),
        "endpoint_direct_paired_common_reweighting": endpoint_pair,
        "canonical_direct_paired_common_reweighting": canonical_pair,
        "ramanujan_paired_common_reweighting": ramanujan_pair,
        "ramanujan_pair_reconstruction_relative_error": pair_relative_error,
        "finite_periodic_dft_ramanujan_identity_passes": passes,
        "source_term_ramanujan_reduction_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(ramanujan_class_mean_receipt())
