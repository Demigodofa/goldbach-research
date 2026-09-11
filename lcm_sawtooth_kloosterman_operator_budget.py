"""Test whether local Kloosterman norms survive frequencywise triangle."""

import math

import numpy as np

from lcm_sawtooth_kloosterman_tensor_transfer import (
    LEADING_LAGS,
    _local_weil_tensor_bound,
)
from lcm_sawtooth_source_ramanujan import _family_source_modes


LEADING_LAG_NORMALIZED_ABSOLUTE_MODE_MASSES = {
    140: 749001.3358809067,
    154: 417286.7772685919,
    156: 493444.63911243196,
    182: 392973.25954838906,
    240: 904323.885919512,
}
CANONICAL_PERIOD = 10010
CANONICAL_FAMILIES = ((77, 65), (143, 35))


def _frequency_vector_norms(period, family):
    sources, _ = _family_source_modes(period, *family)
    squared_norms = np.zeros(period, dtype=float)
    for modes in sources.values():
        for frequency, coefficient in modes.items():
            squared_norms[frequency] += abs(coefficient) ** 2
    return np.sqrt(squared_norms)


def kloosterman_operator_budget_receipt(
        period=CANONICAL_PERIOD, families=CANONICAL_FAMILIES,
        lags=LEADING_LAGS, maximum_useful_bound_fraction=.10):
    families = tuple(families)
    if period != CANONICAL_PERIOD or families != CANONICAL_FAMILIES:
        raise ValueError(
            "absolute-mass comparator is frozen to the canonical fixture")
    lags = tuple(lags)
    if (not lags or any(lag not in LEADING_LAG_NORMALIZED_ABSOLUTE_MODE_MASSES
                        for lag in lags)):
        raise ValueError("require frozen leading-lag masses")
    if not 0 < maximum_useful_bound_fraction <= 1:
        raise ValueError("useful bound fraction must lie in (0,1]")

    left_norms = _frequency_vector_norms(period, families[0])
    right_norms = _frequency_vector_norms(period, families[1])
    right_indices = np.arange(period)
    active_left_frequencies = np.flatnonzero(left_norms)
    rows = {}
    all_useful = True
    for lag in lags:
        kernel_norm_bounds = np.asarray(tuple(
            _local_weil_tensor_bound(period, lag, frequency)[0]
            for frequency in range(period)), dtype=float)
        raw_operator_triangle_bound = 0.0
        for left_frequency in active_left_frequencies:
            raw_operator_triangle_bound += (
                left_norms[left_frequency]
                * np.dot(
                    right_norms,
                    kernel_norm_bounds[
                        (left_frequency - right_indices) % period]))
        unit_class_count = math.prod(
            prime_power - prime_power // prime
            for prime, prime_power in _prime_power_factors(period))
        normalized_bound = raw_operator_triangle_bound / unit_class_count
        absolute_mass = LEADING_LAG_NORMALIZED_ABSOLUTE_MODE_MASSES[lag]
        bound_to_absolute_mass_ratio = normalized_bound / absolute_mass
        useful = bound_to_absolute_mass_ratio <= maximum_useful_bound_fraction
        all_useful = all_useful and useful
        rows[lag] = {
            "normalized_frequency_triangle_operator_bound": normalized_bound,
            "normalized_absolute_mode_mass": absolute_mass,
            "bound_to_absolute_mode_mass_ratio": bound_to_absolute_mass_ratio,
            "frequency_triangle_operator_bound_is_useful": bool(useful),
        }
    return {
        "arithmetic_period": period,
        "lags": lags,
        "maximum_useful_bound_fraction": maximum_useful_bound_fraction,
        "active_left_frequency_count": int(np.count_nonzero(left_norms)),
        "active_right_frequency_count": int(np.count_nonzero(right_norms)),
        "rows": rows,
        "all_frequency_triangle_operator_bounds_are_useful": bool(all_useful),
        "cross_frequency_cancellation_estimate_proved": False,
        "uniform_source_sum_estimate_proved": False,
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


if __name__ == "__main__":
    print(kloosterman_operator_budget_receipt())
