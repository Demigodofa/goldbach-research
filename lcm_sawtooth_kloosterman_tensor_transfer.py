"""CRT transfer from the constrained source sum to local Kloosterman blocks."""

import math

import numpy as np

from lcm_sawtooth_source_ramanujan import (
    _conditioned_unit_exponential_sum,
    _prime_power_factors,
)


LEADING_LAGS = (140, 154, 156, 182, 240)
REPRESENTATIVE_FREQUENCIES = (
    0, 1, 2, 5, 7, 10, 11, 13, 26, 35, 55,
    70, 77, 91, 130, 143, 154, 182, 385, 1001, 10009)


def _prime_ramanujan_sum(prime, frequency):
    return prime - 1 if frequency % prime == 0 else -1


def _tensor_conditioned_difference_entry(
        period, lag, difference, frequency):
    common = math.gcd(lag, period)
    quotient = period // common
    reduced_lag = lag // common
    value = 1.0 + 0.0j
    for prime, prime_power in _prime_power_factors(period):
        if prime != prime_power:
            raise ValueError("tensor transfer currently requires squarefree Q")
        local_difference = difference % prime
        if common % prime == 0:
            if local_difference != 0:
                return 0.0j
            value *= _prime_ramanujan_sum(prime, frequency)
        else:
            if local_difference == 0:
                return 0.0j
            local_frequency = (
                (frequency % prime)
                * (reduced_lag % prime)
                * pow(quotient // prime, -1, prime)) % prime
            value *= np.exp(
                2j * np.pi * local_frequency
                * pow(local_difference, -1, prime) / prime)
    return complex(value)


def _local_weil_tensor_bound(period, lag, frequency):
    common = math.gcd(lag, period)
    bound = 1.0
    zero_frequency_degree = 1
    for prime, _ in _prime_power_factors(period):
        if common % prime == 0:
            bound *= abs(_prime_ramanujan_sum(prime, frequency))
        else:
            zero_frequency_degree *= prime - 2
            bound *= (
                prime - 2 if frequency % prime == 0
                else min(prime - 2, 2 * math.sqrt(prime)))
    return bound, zero_frequency_degree


def kloosterman_tensor_transfer_receipt(
        period=10010, lags=LEADING_LAGS,
        frequencies=REPRESENTATIVE_FREQUENCIES, tolerance=1e-12):
    if type(period) is not int or period < 3:
        raise ValueError("period must be an integer at least three")
    factors = _prime_power_factors(period)
    if any(prime != prime_power for prime, prime_power in factors):
        raise ValueError("period must be squarefree")
    lags = tuple(lags)
    frequencies = tuple(frequencies)
    if (not lags or any(type(lag) is not int or not 0 < lag < period
                        for lag in lags)):
        raise ValueError("lags must lie strictly inside the period")
    if not frequencies or any(type(value) is not int for value in frequencies):
        raise ValueError("frequencies must be nonempty integers")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    maximum_entry_relative_error = 0.0
    tested_nonzero_entries = 0
    rows = {}
    for lag in lags:
        common = math.gcd(lag, period)
        quotient = period // common
        allowed_differences = tuple(
            common * reduced for reduced in range(quotient)
            if math.gcd(reduced, quotient) == 1)
        for frequency in frequencies:
            for difference in allowed_differences:
                direct = _conditioned_unit_exponential_sum(
                    period, lag, difference, frequency)
                tensor = _tensor_conditioned_difference_entry(
                    period, lag, difference, frequency)
                maximum_entry_relative_error = max(
                    maximum_entry_relative_error,
                    abs(tensor - direct) / max(1.0, abs(direct)))
                tested_nonzero_entries += 1
        nonresonant_bound, degree = _local_weil_tensor_bound(period, lag, 1)
        resonant_bound, resonant_degree = _local_weil_tensor_bound(
            period, lag, 0)
        if degree != resonant_degree:
            raise AssertionError("inconsistent quotient graph degree")
        rows[lag] = {
            "gcd_lag_period": common,
            "quotient_period": quotient,
            "allowed_difference_count": len(allowed_differences),
            "zero_quotient_frequency_degree": degree,
            "fully_nonresonant_local_weil_bound": nonresonant_bound,
            "fully_nonresonant_to_zero_degree_ratio": (
                nonresonant_bound / degree),
            "fully_resonant_local_bound": resonant_bound,
        }
    return {
        "arithmetic_period": period,
        "prime_factors": tuple(prime for prime, _ in factors),
        "lags": lags,
        "representative_frequencies": frequencies,
        "tested_nonzero_kernel_entries": tested_nonzero_entries,
        "maximum_entry_relative_error": maximum_entry_relative_error,
        "rows": rows,
        "exact_finite_crt_kloosterman_tensor_identity_passes": bool(
            maximum_entry_relative_error <= tolerance),
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(kloosterman_tensor_transfer_receipt())
