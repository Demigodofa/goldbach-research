"""Test reduced-prime-class bias in the doubled-partner packet core.

The transferred ``Q=10010`` packets contain an explicit real polynomial
direction factor and an arithmetic packet.  This module removes the former,
evaluates the latter with a canonical periodic geometric sum, and averages
the resulting near-lag signed core over every unit class modulo ``Q``.
It is a finite periodic calculation, not a prime-distribution estimate.
"""

import math

import numpy as np

from lcm_sawtooth_partner_doubling_transfer import (
    _matched_doubled_packet,
    _packet_lag_contributions,
    _project_fragile_direction,
)
from lcm_sawtooth_incomplete_frequency import _quadratic_support_data
from lcm_sawtooth_lifted_endpoint_frame import _symmetric_pair_coordinates


def _canonical_periodic_geometric_sum(
        frame_modulus, denominator, numerators):
    """Evaluate the root sum after removing its complete periods."""
    remainder = (frame_modulus - 1) % denominator
    numerators = np.asarray(numerators, dtype=np.int64)
    if remainder == 0:
        return np.zeros(numerators.shape, dtype=complex)
    return (
        np.exp(
            1j * np.pi * numerators * (remainder + 1) / denominator)
        * np.sin(np.pi * numerators * remainder / denominator)
        / np.sin(np.pi * numerators / denominator))


def _family_arithmetic_core_packet(
        frame_modulus, conductor, odd_partner):
    doubled_partner = 2 * odd_partner
    reduced_denominator = math.lcm(conductor, doubled_partner)
    conductor_numerators = np.arange(1, conductor, dtype=np.int64)
    conductor_numerators = conductor_numerators[
        np.gcd(conductor_numerators, conductor) == 1]
    partner_numerators = np.arange(1, doubled_partner, dtype=np.int64)
    partner_numerators = partner_numerators[
        np.gcd(partner_numerators, doubled_partner) == 1]
    conductor_geometric = _canonical_periodic_geometric_sum(
        frame_modulus, conductor, conductor_numerators)
    partner_geometric = _canonical_periodic_geometric_sum(
        frame_modulus, doubled_partner, partner_numerators)
    packet = np.zeros(reduced_denominator, dtype=complex)
    unexpected_denominator_count = 0

    def add_orientation(left_denominator, left_numerators, left_geometric,
                        right_denominator, right_numerators, right_geometric):
        nonlocal unexpected_denominator_count
        common = math.lcm(left_denominator, right_denominator)
        differences = (
            left_numerators[:, None] * (common // left_denominator)
            - right_numerators[None, :] * (common // right_denominator))
        common_factors = np.gcd(np.abs(differences), common)
        reduced = common // common_factors
        selected = reduced == reduced_denominator
        unexpected_denominator_count += int(np.count_nonzero(~selected))
        residues = (
            frame_modulus * (differences // common_factors) % reduced)
        coefficients = (
            left_geometric[:, None]
            * np.conjugate(right_geometric[None, :]))
        flat_residues = residues[selected]
        flat_coefficients = coefficients[selected]
        packet.real[:] += np.bincount(
            flat_residues, weights=flat_coefficients.real,
            minlength=reduced_denominator)
        packet.imag[:] += np.bincount(
            flat_residues, weights=flat_coefficients.imag,
            minlength=reduced_denominator)

    add_orientation(
        conductor, conductor_numerators, conductor_geometric,
        doubled_partner, partner_numerators, partner_geometric)
    add_orientation(
        doubled_partner, partner_numerators, partner_geometric,
        conductor, conductor_numerators, conductor_geometric)
    return packet, unexpected_denominator_count


def prime_class_core_receipt(
        scale_modulus=127,
        families=((77, 65, 1), (143, 35, 2)),
        minimum_reinforcement_fraction=.25, tolerance=1e-12):
    """Average the normalized signed core over all units modulo its period."""
    families = tuple(families)
    if (type(scale_modulus) is not int or scale_modulus < 3
            or len(families) != 2
            or any(len(family) != 3 for family in families)
            or any(type(c) is not int or c < 3 or c % 2 == 0
                   or type(d) is not int or d < 3 or d % 2 == 0
                   or category not in (1, 2)
                   for c, d, category in families)):
        raise ValueError("require two odd conductor-partner families")
    if not 0 < minimum_reinforcement_fraction <= 1:
        raise ValueError("reinforcement fraction must lie in (0,1]")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    conductors = tuple(sorted(c for c, _, _ in families))
    baseline, direction = _project_fragile_direction(
        scale_modulus, conductors)
    support = dict(_quadratic_support_data(*baseline["divisor_range"])[1])
    periods = tuple(math.lcm(c, 2 * d) for c, d, _ in families)
    if len(set(periods)) != 1:
        raise ValueError("families must share one arithmetic period")
    period = periods[0]

    source_errors = []
    for frame_row in baseline["rows"]:
        prime = frame_row["modulus"]
        for conductor, partner, _ in families:
            matched = _matched_doubled_packet(
                prime, baseline["ell_freeze"], conductor, partner,
                direction, support)
            core, unexpected = _family_arithmetic_core_packet(
                prime, conductor, partner)
            if unexpected:
                raise ArithmeticError("family has lower-denominator cells")
            normalized = (
                matched["predicted_packet"] / matched["direction_factor"])
            source_errors.append(float(np.max(
                np.abs(normalized - core)
                / np.maximum(1.0, np.abs(core)))))

    unit_classes = tuple(
        residue for residue in range(1, period)
        if math.gcd(residue, period) == 1)
    signed_cores = []
    representative_errors = []
    direction_products = []
    for residue in unit_classes:
        packets = []
        direction_factors = []
        logarithm = math.log(
            (residue + period) * baseline["ell_freeze"])
        powers = np.asarray((logarithm ** 2, logarithm, 1.0))
        for conductor, partner, _ in families:
            first, unexpected_first = _family_arithmetic_core_packet(
                residue + period, conductor, partner)
            second, unexpected_second = _family_arithmetic_core_packet(
                residue + 2 * period, conductor, partner)
            if unexpected_first or unexpected_second:
                raise ArithmeticError("family has lower-denominator cells")
            representative_errors.append(float(np.max(np.abs(first - second))))
            packets.append(first)
            conductor_coordinate = np.asarray(support[conductor]) * powers
            partner_coordinate = np.asarray(support[2 * partner]) * powers
            lifted_coordinate = _symmetric_pair_coordinates(
                conductor_coordinate[None, :],
                partner_coordinate[None, :])[0]
            direction_factors.append(float(lifted_coordinate @ direction))
        direction_products.append(direction_factors[0] * direction_factors[1])
        contributions = _packet_lag_contributions(
            packets[0], packets[1], baseline["row_count"],
            baseline["row_count"])
        lags = np.arange(period)
        near = (
            np.minimum(lags, period - lags) * baseline["row_count"]
            <= period)
        near[0] = False
        signed_cores.append(float(np.sum(contributions[near])))

    signed_cores = np.asarray(signed_cores)
    complete_mean = float(np.mean(signed_cores))
    mean_absolute = float(np.mean(np.abs(signed_cores)))
    reinforcement_fraction = (
        complete_mean / mean_absolute if mean_absolute else None)
    periodicity_passes = bool(
        max(source_errors) <= tolerance
        and max(representative_errors) <= tolerance)
    reinforcement_passes = bool(
        periodicity_passes
        and reinforcement_fraction is not None
        and complete_mean > 0
        and reinforcement_fraction >= minimum_reinforcement_fraction)
    return {
        "scale_modulus": scale_modulus,
        "families": families,
        "arithmetic_period": period,
        "reduced_residue_class_count": len(unit_classes),
        "minimum_reinforcement_fraction": minimum_reinforcement_fraction,
        "maximum_source_packet_core_relative_error": max(source_errors),
        "maximum_period_representative_absolute_error": max(
            representative_errors),
        "complete_class_signed_core_mean": complete_mean,
        "complete_class_absolute_core_mean": mean_absolute,
        "complete_class_reinforcement_fraction": reinforcement_fraction,
        "positive_signed_core_class_fraction": float(np.mean(signed_cores > 0)),
        "minimum_class_signed_core": float(np.min(signed_cores)),
        "maximum_class_signed_core": float(np.max(signed_cores)),
        "minimum_direction_polynomial_product": min(direction_products),
        "maximum_direction_polynomial_product": max(direction_products),
        "direction_polynomial_product_positive_on_representatives": bool(
            min(direction_products) > 0),
        "normalized_arithmetic_core_periodicity_proved": periodicity_passes,
        "prime_class_reinforcement_hypothesis_passes": reinforcement_passes,
        "prime_class_reinforcement_proves_prime_distribution": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(prime_class_core_receipt())
