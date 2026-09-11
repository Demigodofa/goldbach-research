"""Measure whether complete conductor energy avoids large difference moduli.

The joint prime-row phase bound becomes non-saving when the reduced frequency
difference denominator exceeds ``M*A``.  A possible escape from the ``B^4``
worst case is that the actual primitive-conductor energy might put negligible
mass on conductor pairs whose lcm already exceeds this critical scale.

For a conductor vector ``S_d`` define its positive complete energy

    E_d=H_m(d)|S_d|^2.

This probe measures the product-energy mass ``E_d E_e`` carried by pairs with
``lcm(d,e)>M*A``.  It is a necessary diagnostic for a sparsity-only argument,
not the actual signed frequency-pair boundary form.
"""

import math

import numpy as np

from lcm_sawtooth_exact_gcd_factorization import (
    sawtooth_gcd_mobius_transform,
)
from lcm_sawtooth_incomplete_frequency import _quadratic_support_data
from mobius_covariance_endpoint_probe import _prime_flags


def _large_lcm_pair_fractions(conductors, energy, thresholds):
    total = float(np.sum(energy)) ** 2
    if total <= 0:
        raise ArithmeticError("complete conductor energy must be positive")
    large = np.zeros(len(thresholds), dtype=float)
    chunk_size = 256
    for first in range(0, len(conductors), chunk_size):
        left_conductors = conductors[first:first + chunk_size, None]
        left_energy = energy[first:first + chunk_size, None]
        lcms = np.lcm(left_conductors, conductors[None, :])
        pair_energy = left_energy * energy[None, :]
        for index, threshold in enumerate(thresholds):
            large[index] += float(np.sum(pair_energy[lcms > threshold]))
    return tuple(float(value / total) for value in large)


def difference_modulus_energy_mass_receipt(
        modulus, ell_freeze, row_count, divisor_lower, divisor_upper):
    """Evaluate the high-lcm product-energy diagnostic for all three vectors."""
    if any(type(value) is not int for value in (
            modulus, ell_freeze, row_count,
            divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell_freeze < 1 or row_count < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid difference-modulus ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")

    _, support = _quadratic_support_data(divisor_lower, divisor_upper)
    logarithm = math.log(modulus * ell_freeze)
    active = []
    for divisor, polynomial in support:
        primitive_weight = sawtooth_gcd_mobius_transform(modulus, divisor)
        if primitive_weight <= 0:
            continue
        actual = ((polynomial[0] * logarithm + polynomial[1])
                  * logarithm + polynomial[2])
        active.append((divisor, primitive_weight, polynomial, actual))
    conductors = np.array([row[0] for row in active], dtype=np.int64)
    critical = modulus * row_count
    thresholds = (critical // 4, critical, critical * 4)
    labels = {
        "quadratic": np.array([
            weight * polynomial[0] ** 2
            for _, weight, polynomial, _ in active]),
        "linear": np.array([
            weight * polynomial[1] ** 2
            for _, weight, polynomial, _ in active]),
        "constant": np.array([
            weight * polynomial[2] ** 2
            for _, weight, polynomial, _ in active]),
        "actual": np.array([
            weight * actual ** 2
            for _, weight, _, actual in active]),
    }
    fractions = {
        label: _large_lcm_pair_fractions(
            conductors, energy, thresholds)
        for label, energy in labels.items()}
    return {
        "modulus": modulus,
        "ell_freeze": ell_freeze,
        "row_count": row_count,
        "divisor_range": (divisor_lower, divisor_upper),
        "positive_primitive_conductor_count": len(active),
        "difference_modulus_thresholds": thresholds,
        "large_lcm_pair_energy_fractions": fractions,
        "actual_fraction_above_MA": fractions["actual"][1],
        "minimum_component_fraction_above_MA": min(
            values[1] for values in fractions.values()),
        "complete_energy_sparsity_above_MA_proved": False,
        "signed_difference_modulus_cancellation_proved": False,
        "finite_positive_pair_mass_measurement": True,
    }


if __name__ == "__main__":
    for controls in (
            (251, 69, 46, 4, 20),
            (503, 112, 75, 4, 29),
            (1009, 183, 122, 5, 42),
            (4001, 715, 477, 8, 89),
            (16001, 1878, 1252, 11, 190)):
        print(difference_modulus_energy_mass_receipt(*controls))
