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


def _window_lag_data(packet_left, packet_right, row_counts):
    """Return near-lag sums and masked lag vectors for exact kernels."""
    packet_left = np.asarray(packet_left, dtype=complex)
    packet_right = np.asarray(packet_right, dtype=complex)
    row_counts = tuple(row_counts)
    if (packet_left.ndim != 1 or packet_right.shape != packet_left.shape
            or len(packet_left) < 2 or not row_counts
            or any(type(row_count) is not int or row_count < 1
                   for row_count in row_counts)):
        raise ValueError("invalid packet window inputs")
    denominator = len(packet_left)
    correlation = np.fft.ifft(
        np.fft.fft(packet_left) * np.conjugate(np.fft.fft(packet_right)))
    lags = np.arange(denominator)
    nonzero = lags != 0
    active_lags = lags[nonzero]
    distances = np.minimum(lags, denominator - lags)
    results = []
    lag_vectors = {}
    for row_count in row_counts:
        kernel = np.ones(denominator, dtype=complex)
        kernel[nonzero] = (
            np.exp(
                1j * np.pi * (3 * row_count - 1)
                * active_lags / denominator)
            * np.sin(np.pi * row_count * active_lags / denominator)
            / (row_count * np.sin(np.pi * active_lags / denominator)))
        contributions = 2 * denominator * (kernel * correlation).real
        near = distances * row_count <= denominator
        near[0] = False
        masked = np.where(near, contributions, 0.0)
        results.append(float(np.sum(masked)))
        lag_vectors[row_count] = masked
    return tuple(results), lag_vectors


def _window_signed_cores(packet_left, packet_right, row_counts):
    """Evaluate near-lag signed cores with exact interval kernels."""
    return _window_lag_data(packet_left, packet_right, row_counts)[0]


def _window_signed_core(packet_left, packet_right, row_count):
    return _window_signed_cores(packet_left, packet_right, (row_count,))[0]


def prime_class_core_receipt(
        scale_modulus=127,
        families=((77, 65, 1), (143, 35, 2)),
        minimum_reinforcement_fraction=.25,
        polynomial_cycle_multiples=(1, 10, 100),
        maximum_final_cycle_relative_difference=.10,
        kernel_row_scales=(28, 34, 39, 50, 75),
        minimum_kernel_ratio_fraction=.50,
        minimum_lost_shell_component_fraction=.75,
        localized_inversion_pair_count=5,
        minimum_localized_pair_mass_fraction=.75,
        tolerance=1e-12):
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
    polynomial_cycle_multiples = tuple(polynomial_cycle_multiples)
    if (not polynomial_cycle_multiples
            or any(type(value) is not int or value < 1
                   for value in polynomial_cycle_multiples)
            or tuple(sorted(set(polynomial_cycle_multiples)))
            != polynomial_cycle_multiples):
        raise ValueError("cycle multiples must be strictly increasing")
    if not 0 <= maximum_final_cycle_relative_difference <= 1:
        raise ValueError("final-cycle difference must lie in [0,1]")
    kernel_row_scales = tuple(kernel_row_scales)
    if (not kernel_row_scales
            or any(type(value) is not int or value < 1
                   for value in kernel_row_scales)
            or tuple(sorted(set(kernel_row_scales))) != kernel_row_scales):
        raise ValueError("kernel row scales must be strictly increasing")
    if not 0 < minimum_kernel_ratio_fraction <= 1:
        raise ValueError("kernel ratio fraction must lie in (0,1]")
    if not 0 < minimum_lost_shell_component_fraction <= 1:
        raise ValueError("shell component fraction must lie in (0,1]")
    if (type(localized_inversion_pair_count) is not int
            or localized_inversion_pair_count < 1):
        raise ValueError("localized pair count must be positive")
    if not 0 < minimum_localized_pair_mass_fraction <= 1:
        raise ValueError("localized mass fraction must lie in (0,1]")
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
    if kernel_row_scales[0] != baseline["row_count"]:
        raise ValueError("first kernel scale must equal the baseline row count")

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

    def direction_product(frame_modulus):
        logarithm = math.log(frame_modulus * baseline["ell_freeze"])
        powers = np.asarray((logarithm ** 2, logarithm, 1.0))
        factors = []
        for conductor, partner, _ in families:
            conductor_coordinate = np.asarray(support[conductor]) * powers
            partner_coordinate = np.asarray(support[2 * partner]) * powers
            lifted_coordinate = _symmetric_pair_coordinates(
                conductor_coordinate[None, :],
                partner_coordinate[None, :])[0]
            factors.append(float(lifted_coordinate @ direction))
        return factors[0] * factors[1]

    signed_cores_by_scale = {
        row_scale: [] for row_scale in kernel_row_scales}
    mean_lag_sums = {
        row_scale: np.zeros(period)
        for row_scale in kernel_row_scales[:2]}
    representative_errors = []
    for residue in unit_classes:
        packets = []
        for conductor, partner, _ in families:
            first, unexpected_first = _family_arithmetic_core_packet(
                residue + period, conductor, partner)
            second, unexpected_second = _family_arithmetic_core_packet(
                residue + 2 * period, conductor, partner)
            if unexpected_first or unexpected_second:
                raise ArithmeticError("family has lower-denominator cells")
            representative_errors.append(float(np.max(np.abs(first - second))))
            packets.append(first)
        window_values, lag_vectors = _window_lag_data(
            packets[0], packets[1], kernel_row_scales)
        for row_scale, value in zip(kernel_row_scales, window_values):
            signed_cores_by_scale[row_scale].append(value)
        for row_scale in mean_lag_sums:
            mean_lag_sums[row_scale] += lag_vectors[row_scale]

    signed_cores_by_scale = {
        row_scale: np.asarray(values)
        for row_scale, values in signed_cores_by_scale.items()}
    signed_cores = signed_cores_by_scale[baseline["row_count"]]
    complete_mean = float(np.mean(signed_cores))
    mean_absolute = float(np.mean(np.abs(signed_cores)))
    reinforcement_fraction = (
        complete_mean / mean_absolute if mean_absolute else None)
    kernel_scale_rows = []
    for row_scale in kernel_row_scales:
        values = signed_cores_by_scale[row_scale]
        signed_mean = float(np.mean(values))
        absolute_mean = float(np.mean(np.abs(values)))
        kernel_scale_rows.append({
            "row_scale": row_scale,
            "actual_prime_high_denominator_row_count": sum(
                period > frame_row["modulus"] * row_scale
                for frame_row in baseline["rows"]),
            "complete_class_signed_core_mean": signed_mean,
            "complete_class_absolute_core_mean": absolute_mean,
            "signed_to_absolute_ratio": (
                signed_mean / absolute_mean if absolute_mean else None),
        })
    minimum_kernel_ratio = (
        minimum_kernel_ratio_fraction * reinforcement_fraction
        if reinforcement_fraction is not None else None)
    kernel_stability_passes = bool(
        minimum_kernel_ratio is not None
        and all(row["signed_to_absolute_ratio"] is not None
                and row["signed_to_absolute_ratio"] >= minimum_kernel_ratio
                for row in kernel_scale_rows))
    fully_retained_kernel_rows = tuple(
        row for row in kernel_scale_rows
        if row["actual_prime_high_denominator_row_count"]
        == len(baseline["rows"]))
    retained_kernel_stability_passes = bool(
        minimum_kernel_ratio is not None
        and len(fully_retained_kernel_rows) >= 2
        and all(row["signed_to_absolute_ratio"] is not None
                and row["signed_to_absolute_ratio"] >= minimum_kernel_ratio
                for row in fully_retained_kernel_rows))
    first_scale, second_scale = kernel_row_scales[:2]
    first_mean_lags = mean_lag_sums[first_scale] / len(unit_classes)
    second_mean_lags = mean_lag_sums[second_scale] / len(unit_classes)
    lag_distances = np.minimum(np.arange(period), period - np.arange(period))
    first_support = lag_distances * first_scale <= period
    second_support = lag_distances * second_scale <= period
    first_support[0] = False
    second_support[0] = False
    common_reweighting = float(np.sum(
        second_mean_lags[second_support]
        - first_mean_lags[second_support]))
    lost_boundary_shell = float(-np.sum(
        first_mean_lags[first_support & ~second_support]))
    observed_window_difference = float(
        np.sum(second_mean_lags) - np.sum(first_mean_lags))
    decomposed_window_difference = common_reweighting + lost_boundary_shell
    window_decomposition_relative_error = (
        abs(decomposed_window_difference - observed_window_difference)
        / max(1.0, abs(observed_window_difference)))
    component_absolute_mass = (
        abs(common_reweighting) + abs(lost_boundary_shell))
    lost_shell_component_fraction = (
        abs(lost_boundary_shell) / component_absolute_mass
        if component_absolute_mass else None)
    lost_shell_mechanism_passes = bool(
        window_decomposition_relative_error <= tolerance
        and observed_window_difference * lost_boundary_shell > 0
        and lost_shell_component_fraction is not None
        and lost_shell_component_fraction
        >= minimum_lost_shell_component_fraction)
    common_lag_delta = second_mean_lags - first_mean_lags
    paired_reweighting_rows = []
    for lag in range(1, period // 2 + 1):
        if not second_support[lag]:
            continue
        inverse = (-lag) % period
        value = float(common_lag_delta[lag])
        if inverse != lag:
            value += float(common_lag_delta[inverse])
        paired_reweighting_rows.append({
            "lag": lag,
            "inverse_lag": inverse,
            "paired_common_reweighting": value,
        })
    paired_reweighting_rows.sort(
        key=lambda row: abs(row["paired_common_reweighting"]), reverse=True)
    paired_reconstruction = sum(
        row["paired_common_reweighting"] for row in paired_reweighting_rows)
    paired_reconstruction_relative_error = (
        abs(paired_reconstruction - common_reweighting)
        / max(1.0, abs(common_reweighting)))
    paired_absolute_mass = sum(
        abs(row["paired_common_reweighting"])
        for row in paired_reweighting_rows)
    leading_pair_absolute_mass = sum(
        abs(row["paired_common_reweighting"])
        for row in paired_reweighting_rows[:localized_inversion_pair_count])
    leading_pair_mass_fraction = (
        leading_pair_absolute_mass / paired_absolute_mass
        if paired_absolute_mass else None)
    localized_pair_mechanism_passes = bool(
        paired_reconstruction_relative_error <= tolerance
        and leading_pair_mass_fraction is not None
        and leading_pair_mass_fraction >= minimum_localized_pair_mass_fraction)
    polynomial_cycle_rows = []
    for multiple in polynomial_cycle_multiples:
        weights = np.asarray(tuple(
            direction_product(multiple * period + residue)
            for residue in unit_classes))
        weighted_absolute = float(np.dot(weights, np.abs(signed_cores)))
        weighted_signed = float(np.dot(weights, signed_cores))
        weighted_ratio = (
            weighted_signed / weighted_absolute
            if weighted_absolute else None)
        polynomial_cycle_rows.append({
            "cycle_multiple": multiple,
            "cycle_start": multiple * period,
            "minimum_direction_polynomial_product": float(np.min(weights)),
            "maximum_direction_polynomial_product": float(np.max(weights)),
            "weighted_signed_core_sum": weighted_signed,
            "weighted_absolute_core_sum": weighted_absolute,
            "weighted_signed_to_absolute_ratio": weighted_ratio,
        })
    final_weighted_ratio = polynomial_cycle_rows[-1][
        "weighted_signed_to_absolute_ratio"]
    final_cycle_relative_difference = (
        abs(final_weighted_ratio - reinforcement_fraction)
        / abs(reinforcement_fraction)
        if reinforcement_fraction not in (None, 0) else None)
    polynomial_stability_passes = bool(
        all(row["minimum_direction_polynomial_product"] > 0
            and row["weighted_signed_to_absolute_ratio"] is not None
            and row["weighted_signed_to_absolute_ratio"] > 0
            for row in polynomial_cycle_rows)
        and final_cycle_relative_difference is not None
        and final_cycle_relative_difference
        <= maximum_final_cycle_relative_difference)
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
        "kernel_row_scales": kernel_row_scales,
        "minimum_kernel_ratio_fraction": minimum_kernel_ratio_fraction,
        "minimum_lost_shell_component_fraction": (
            minimum_lost_shell_component_fraction),
        "localized_inversion_pair_count": localized_inversion_pair_count,
        "minimum_localized_pair_mass_fraction": (
            minimum_localized_pair_mass_fraction),
        "minimum_kernel_signed_to_absolute_ratio": minimum_kernel_ratio,
        "kernel_scale_rows": tuple(kernel_scale_rows),
        "window_decomposition_first_row_scale": first_scale,
        "window_decomposition_second_row_scale": second_scale,
        "observed_window_signed_mean_difference": observed_window_difference,
        "common_lag_kernel_reweighting_component": common_reweighting,
        "lost_near_boundary_shell_component": lost_boundary_shell,
        "lost_shell_absolute_component_fraction": (
            lost_shell_component_fraction),
        "window_difference_decomposition_relative_error": (
            window_decomposition_relative_error),
        "common_support_inversion_pair_count": len(paired_reweighting_rows),
        "leading_common_reweighting_inversion_pairs": tuple(
            paired_reweighting_rows[:localized_inversion_pair_count]),
        "common_reweighting_paired_reconstruction_relative_error": (
            paired_reconstruction_relative_error),
        "leading_inversion_pair_absolute_mass_fraction": (
            leading_pair_mass_fraction),
        "fully_retained_kernel_row_scales": tuple(
            row["row_scale"] for row in fully_retained_kernel_rows),
        "maximum_source_packet_core_relative_error": max(source_errors),
        "maximum_period_representative_absolute_error": max(
            representative_errors),
        "complete_class_signed_core_mean": complete_mean,
        "complete_class_absolute_core_mean": mean_absolute,
        "complete_class_reinforcement_fraction": reinforcement_fraction,
        "positive_signed_core_class_fraction": float(np.mean(signed_cores > 0)),
        "minimum_class_signed_core": float(np.min(signed_cores)),
        "maximum_class_signed_core": float(np.max(signed_cores)),
        "polynomial_cycle_multiples": polynomial_cycle_multiples,
        "maximum_final_cycle_relative_difference": (
            maximum_final_cycle_relative_difference),
        "polynomial_cycle_rows": tuple(polynomial_cycle_rows),
        "final_cycle_to_unweighted_relative_difference": (
            final_cycle_relative_difference),
        "minimum_direction_polynomial_product": min(
            row["minimum_direction_polynomial_product"]
            for row in polynomial_cycle_rows),
        "maximum_direction_polynomial_product": max(
            row["maximum_direction_polynomial_product"]
            for row in polynomial_cycle_rows),
        "direction_polynomial_product_positive_on_representatives": bool(
            all(row["minimum_direction_polynomial_product"] > 0
                for row in polynomial_cycle_rows)),
        "normalized_arithmetic_core_periodicity_proved": periodicity_passes,
        "prime_class_reinforcement_hypothesis_passes": reinforcement_passes,
        "polynomial_weight_stability_hypothesis_passes": (
            polynomial_stability_passes),
        "fixed_q_kernel_window_stability_hypothesis_passes": (
            kernel_stability_passes),
        "fully_retained_kernel_window_stability_hypothesis_passes": (
            retained_kernel_stability_passes),
        "lost_near_boundary_shell_mechanism_hypothesis_passes": (
            lost_shell_mechanism_passes),
        "localized_inversion_pair_reweighting_hypothesis_passes": (
            localized_pair_mechanism_passes),
        "prime_class_reinforcement_proves_prime_distribution": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(prime_class_core_receipt())
