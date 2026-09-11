"""Localize the finite ``(77,143)`` packet interference by reduced denominator.

For a fixed lifted direction, split every high-Q ordered frequency-pair term
into packets using neither selected conductor, the left conductor only, the
right conductor only, or both.  When the mixed packet is absent, the Boolean
energy difference is exactly twice the real inner product of the two single
packets.  This module resolves that inner product by its reduced denominator
``Q`` in both the full residue space and the active row window.

The project test asks whether at least 75 percent of the absolute
off-diagonal-window interference for ``M=127`` and ``(77,143)`` lies on
denominators divisible by their shared prime 11.  A finite pass localizes the
observed reinforcement; it does not supply a signed prime-correlation bound.
"""

import math

import numpy as np

from lcm_sawtooth_arithmetic_covariance_basis import (
    covariance_inverse_root,
    project_one_frequency_covariance,
)
from lcm_sawtooth_centered_basis_gershgorin import symmetric_square_transform
from lcm_sawtooth_incomplete_frequency import _quadratic_support_data
from lcm_sawtooth_lifted_endpoint_frame import (
    _lifted_frequency_data,
    _symmetric_pair_coordinates,
    project_prime_block_lifted_endpoint_scan,
)
from lcm_sawtooth_trace_traceless_block_frame import trace_traceless_transform


def classify_shared_prime_denominator_mass(
        rows, shared_prime, minimum_absolute_mass_fraction=.75):
    """Apply the declared absolute-mass localization falsifier."""
    rows = tuple(rows)
    if not rows:
        raise ValueError("at least one denominator row is required")
    if (type(shared_prime) is not int or shared_prime < 2
            or any(shared_prime % divisor == 0
                   for divisor in range(2, math.isqrt(shared_prime) + 1))):
        raise ValueError("shared_prime must be prime")
    if not 0 < minimum_absolute_mass_fraction <= 1:
        raise ValueError("mass fraction threshold must lie in (0,1]")
    absolute_mass = sum(
        abs(row["off_diagonal_window_interference"]) for row in rows)
    if not absolute_mass:
        raise ArithmeticError("off-diagonal denominator mass is zero")
    shared_mass = sum(
        abs(row["off_diagonal_window_interference"])
        for row in rows if row["reduced_denominator"] % shared_prime == 0)
    fraction = shared_mass / absolute_mass
    return {
        "absolute_off_diagonal_mass": absolute_mass,
        "shared_prime_absolute_off_diagonal_mass": shared_mass,
        "shared_prime_absolute_mass_fraction": fraction,
        "minimum_absolute_mass_fraction": minimum_absolute_mass_fraction,
        "shared_prime_denominator_mass_hypothesis_passes": bool(
            fraction >= minimum_absolute_mass_fraction),
    }


def classify_primewise_denominator_signs(
        rows, denominators, contribution_tolerance=1e-12,
        minimum_positive_fraction=.75, maximum_positive_mass_share=.25,
        minimum_passing_channel_count=2):
    """Test primewise sign breadth separately on each selected Q-channel."""
    rows = tuple(rows)
    denominators = tuple(sorted(set(denominators)))
    if not rows or not denominators:
        raise ValueError("require contribution rows and denominators")
    if not math.isfinite(contribution_tolerance) or contribution_tolerance < 0:
        raise ValueError("contribution_tolerance must be finite and nonnegative")
    if not 0 < minimum_positive_fraction <= 1:
        raise ValueError("positive fraction threshold must lie in (0,1]")
    if not 0 < maximum_positive_mass_share <= 1:
        raise ValueError("positive mass share cap must lie in (0,1]")
    if (type(minimum_passing_channel_count) is not int
            or not 1 <= minimum_passing_channel_count <= len(denominators)):
        raise ValueError("passing channel count must fit the denominator set")

    channel_rows = []
    for denominator in denominators:
        selected = tuple(
            row for row in rows if row["reduced_denominator"] == denominator
            and abs(row["off_diagonal_window_interference"])
            > contribution_tolerance)
        if not selected:
            raise ArithmeticError("selected denominator has no nonzero primes")
        positive = tuple(
            row for row in selected
            if row["off_diagonal_window_interference"] > 0)
        positive_mass = sum(
            row["off_diagonal_window_interference"] for row in positive)
        negative_mass = -sum(
            row["off_diagonal_window_interference"] for row in selected
            if row["off_diagonal_window_interference"] < 0)
        positive_fraction = len(positive) / len(selected)
        if positive_mass:
            largest = max(
                positive,
                key=lambda row: row["off_diagonal_window_interference"])
            largest_modulus = largest["modulus"]
            largest_share = (
                largest["off_diagonal_window_interference"] / positive_mass)
        else:
            largest_modulus = None
            largest_share = float("inf")
        passes = bool(
            positive_fraction >= minimum_positive_fraction
            and largest_share <= maximum_positive_mass_share)
        channel_rows.append({
            "reduced_denominator": denominator,
            "nonzero_prime_count": len(selected),
            "positive_prime_count": len(positive),
            "positive_prime_fraction": positive_fraction,
            "positive_mass": positive_mass,
            "negative_mass": negative_mass,
            "signed_sum": positive_mass - negative_mass,
            "largest_positive_contributor": largest_modulus,
            "largest_positive_mass_share": largest_share,
            "primewise_broad_sign_hypothesis_passes": passes,
            "prime_contributions": tuple(
                (row["modulus"], row["off_diagonal_window_interference"])
                for row in selected),
        })
    passing = tuple(
        row["reduced_denominator"] for row in channel_rows
        if row["primewise_broad_sign_hypothesis_passes"])
    return {
        "contribution_tolerance": contribution_tolerance,
        "minimum_positive_fraction": minimum_positive_fraction,
        "maximum_positive_mass_share": maximum_positive_mass_share,
        "minimum_passing_channel_count": minimum_passing_channel_count,
        "primewise_denominator_rows": tuple(channel_rows),
        "passing_denominators": passing,
        "passing_channel_count": len(passing),
        "denominatorwise_prime_sign_hypothesis_passes": bool(
            len(passing) >= minimum_passing_channel_count),
    }


def shared_prime_high_q_support_obstruction(
        modulus, row_count, divisor_lower, divisor_upper,
        conductors, shared_prime):
    """Bound Q after cancellation of the shared prime on each single packet."""
    conductors = tuple(sorted(set(conductors)))
    if (len(conductors) != 2
            or any(type(value) is not int or value < 2 for value in conductors)):
        raise ValueError("require two distinct integer conductors")
    if (type(shared_prime) is not int or shared_prime < 2
            or any(shared_prime % divisor == 0
                   for divisor in range(2, math.isqrt(shared_prime) + 1))):
        raise ValueError("shared_prime must be prime")
    if any(conductor % shared_prime for conductor in conductors):
        raise ValueError("shared_prime must divide both conductors")
    if type(modulus) is not int or type(row_count) is not int:
        raise ValueError("modulus and row_count must be integers")
    if modulus < 2 or row_count < 1:
        raise ValueError("modulus and row_count must be positive")

    support = tuple(
        denominator for denominator, _
        in _quadratic_support_data(divisor_lower, divisor_upper)[1])
    threshold = modulus * row_count
    side_bounds = []
    for conductor, opposite in zip(conductors, reversed(conductors)):
        candidates = tuple(
            math.lcm(conductor, denominator) // shared_prime
            for denominator in support if denominator != opposite)
        side_bounds.append(max(candidates))
    maximum = max(side_bounds)
    return {
        "high_q_threshold": threshold,
        "left_packet_nonshared_q_upper_bound": side_bounds[0],
        "right_packet_nonshared_q_upper_bound": side_bounds[1],
        "maximum_nonshared_q_upper_bound": maximum,
        "every_high_q_single_packet_denominator_has_shared_prime_proved": bool(
            maximum <= threshold),
    }


def _packet_residue_cells(
        modulus, row_count, ell_freeze, divisor_range,
        direction, conductors, shared_prime):
    """Group scalar high-Q packet coefficients by ``(category,Q,residue)``."""
    denominators, numerators, geometrics, coordinates = _lifted_frequency_data(
        modulus, ell_freeze, *divisor_range)
    threshold = modulus * row_count
    packets = {category: {} for category in range(4)}
    pair_counts = [0, 0, 0, 0]
    nonshared_single_pair_count = 0
    chunk_size = 64
    for first in range(0, len(denominators), chunk_size):
        left_d = denominators[first:first + chunk_size, None]
        right_d = denominators[None, :]
        left_k = numerators[first:first + chunk_size, None]
        common = np.lcm(left_d, right_d)
        difference = (
            left_k * (common // left_d)
            - numerators[None, :] * (common // right_d))
        common_factor = np.gcd(np.abs(difference), common)
        reduced = common // common_factor
        high_q = reduced > threshold
        if not np.any(high_q):
            continue
        residues = np.zeros_like(reduced)
        residues[high_q] = (
            modulus * (difference[high_q] // common_factor[high_q])
            % reduced[high_q])

        has_left = ((left_d == conductors[0])
                    | (right_d == conductors[0]))
        has_right = ((left_d == conductors[1])
                     | (right_d == conductors[1]))
        categories = has_left.astype(np.int8) + 2 * has_right.astype(np.int8)
        selected_categories = categories[high_q]
        selected_reduced = reduced[high_q]
        for category in range(4):
            pair_counts[category] += int(np.count_nonzero(
                selected_categories == category))
        nonshared_single_pair_count += int(np.count_nonzero(
            ((selected_categories == 1) | (selected_categories == 2))
            & (selected_reduced % shared_prime != 0)))

        left_coordinates = np.broadcast_to(
            coordinates[first:first + chunk_size, None, :],
            (*reduced.shape, 3))[high_q]
        right_coordinates = np.broadcast_to(
            coordinates[None, :, :], (*reduced.shape, 3))[high_q]
        lifted = _symmetric_pair_coordinates(left_coordinates, right_coordinates)
        products = (
            geometrics[first:first + chunk_size, None]
            * np.conjugate(geometrics[None, :]))[high_q]
        scalars = products * (lifted @ direction)
        keys = np.column_stack((
            selected_categories, selected_reduced, residues[high_q]))
        unique, inverse = np.unique(keys, axis=0, return_inverse=True)
        grouped = (
            np.bincount(inverse, weights=scalars.real)
            + 1j * np.bincount(inverse, weights=scalars.imag))
        for key, value in zip(unique, grouped):
            category, denominator, residue = (int(item) for item in key)
            cell = (denominator, residue)
            packets[category][cell] = packets[category].get(cell, 0j) + value
    return packets, tuple(pair_counts), nonshared_single_pair_count


def _cross_by_denominator(left, right, row_count):
    """Return active, full, and off-diagonal cross terms for each Q."""
    result = {}
    denominators = sorted({key[0] for key in left} | {key[0] for key in right})
    rows = np.arange(row_count, 2 * row_count, dtype=np.int64)
    for denominator in denominators:
        left_cells = {r: v for (q, r), v in left.items() if q == denominator}
        right_cells = {r: v for (q, r), v in right.items() if q == denominator}
        common_residues = left_cells.keys() & right_cells.keys()
        full = 2 * denominator * float(sum(
            (left_cells[residue] * np.conjugate(right_cells[residue])).real
            for residue in common_residues))

        def transform(cells):
            if not cells:
                return np.zeros(row_count, dtype=complex)
            residues = np.fromiter(cells.keys(), dtype=np.int64)
            values = np.fromiter(cells.values(), dtype=complex)
            phases = np.exp(
                2j * np.pi
                * ((rows[:, None] * residues[None, :]) % denominator)
                / denominator)
            return phases @ values

        left_transform = transform(left_cells)
        right_transform = transform(right_cells)
        active = (
            2 * denominator / row_count
            * float(np.sum(
                left_transform * np.conjugate(right_transform)).real))
        result[denominator] = (active, full, active - full)
    return result


def _require_no_mixed_high_q_packet(mixed_pair_count):
    """Guard the specialization of the Boolean identity to ``2 Re<b,c>``."""
    if type(mixed_pair_count) is not int or mixed_pair_count < 0:
        raise ValueError("mixed_pair_count must be a nonnegative integer")
    if mixed_pair_count:
        raise ArithmeticError(
            "mixed high-Q packet is nonempty; direct single-packet "
            "interference is not the complete Boolean cross term")


def project_reduced_denominator_interference_receipt(
        scale_modulus, conductors=(77, 143),
        minimum_absolute_mass_fraction=.75):
    """Resolve the aggregate fragile-direction packet interference by Q."""
    conductors = tuple(sorted(set(conductors)))
    if (len(conductors) != 2
            or any(type(value) is not int or value < 2 for value in conductors)):
        raise ValueError("require two distinct integer conductors")
    shared_prime = math.gcd(*conductors)
    if (shared_prime < 2
            or any(shared_prime % divisor == 0
                   for divisor in range(2, math.isqrt(shared_prime) + 1))):
        raise ValueError("the conductor gcd must be prime")

    exclusions = ((), (conductors[0],), (conductors[1],), conductors)
    frames = {
        excluded: project_prime_block_lifted_endpoint_scan(
            scale_modulus, excluded)
        for excluded in exclusions
    }
    baseline = frames[()]
    covariance, _ = project_one_frequency_covariance(scale_modulus, baseline)
    transform3, _ = covariance_inverse_root(covariance)
    transform6 = symmetric_square_transform(
        transform3) @ trace_traceless_transform()

    def transformed(frame, key):
        raw = np.asarray(frame[key])
        result = transform6.T @ raw @ transform6
        return (result + result.T) / 2

    active_matrices = {
        excluded: transformed(
            frame, "aggregate_active_window_residue_energy_gram")
        for excluded, frame in frames.items()
    }
    full_matrices = {
        excluded: transformed(frame, "aggregate_full_residue_energy_gram")
        for excluded, frame in frames.items()
    }
    differences = {
        excluded: active_matrices[excluded] - .5 * full_matrices[excluded]
        for excluded in exclusions
    }
    left = (conductors[0],)
    right = (conductors[1],)
    additive = differences[left] + differences[right] - differences[()]
    _, vectors = np.linalg.eigh(additive[1:, 1:])
    fragile = vectors[:, 0]
    original_direction = transform6[:, 1:] @ fragile

    aggregate = {}
    prime_contribution_rows = []
    mixed_pair_count = 0
    nonshared_single_pair_count = 0
    for frame_row in baseline["rows"]:
        packets, pair_counts, nonshared_count = _packet_residue_cells(
            frame_row["modulus"], baseline["row_count"],
            baseline["ell_freeze"], baseline["divisor_range"],
            original_direction, conductors, shared_prime)
        mixed_pair_count += pair_counts[3]
        nonshared_single_pair_count += nonshared_count
        contributions = _cross_by_denominator(
            packets[1], packets[2], baseline["row_count"])
        for denominator, values in contributions.items():
            prime_contribution_rows.append({
                "modulus": frame_row["modulus"],
                "reduced_denominator": denominator,
                "active_window_interference": values[0],
                "full_residue_interference": values[1],
                "off_diagonal_window_interference": values[2],
            })
            previous = aggregate.get(denominator, (0.0, 0.0, 0.0))
            aggregate[denominator] = tuple(
                old + new for old, new in zip(previous, values))
    _require_no_mixed_high_q_packet(mixed_pair_count)

    rows = tuple({
        "reduced_denominator": denominator,
        "divisible_by_shared_prime": bool(denominator % shared_prime == 0),
        "active_window_interference": values[0],
        "full_residue_interference": values[1],
        "off_diagonal_window_interference": values[2],
    } for denominator, values in sorted(aggregate.items()))
    classification = classify_shared_prime_denominator_mass(
        rows, shared_prime, minimum_absolute_mass_fraction)
    active_total = sum(
        row["active_window_interference"] for row in rows)
    full_total = sum(row["full_residue_interference"] for row in rows)
    off_diagonal_total = sum(
        row["off_diagonal_window_interference"] for row in rows)

    def boolean_cross(matrices):
        return (matrices[conductors] - matrices[left]
                - matrices[right] + matrices[()])

    matrix_active = float(
        fragile @ boolean_cross(active_matrices)[1:, 1:] @ fragile)
    matrix_full = float(
        fragile @ boolean_cross(full_matrices)[1:, 1:] @ fragile)
    obstruction = shared_prime_high_q_support_obstruction(
        scale_modulus, baseline["row_count"], *baseline["divisor_range"],
        conductors, shared_prime)
    nonzero_rows = tuple(
        row for row in rows
        if abs(row["off_diagonal_window_interference"]) > 1e-12)
    positive_rows = tuple(
        row for row in nonzero_rows
        if row["off_diagonal_window_interference"] > 0)
    primewise_classification = classify_primewise_denominator_signs(
        prime_contribution_rows,
        tuple(row["reduced_denominator"] for row in nonzero_rows))
    return {
        "scale_modulus": scale_modulus,
        "conductors": conductors,
        "shared_prime": shared_prime,
        "prime_count": baseline["prime_count"],
        "row_count": baseline["row_count"],
        "divisor_range": baseline["divisor_range"],
        "rows": rows,
        "nonzero_off_diagonal_denominators": tuple(
            row["reduced_denominator"] for row in nonzero_rows),
        "positive_nonzero_denominator_count": len(positive_rows),
        "nonzero_denominator_count": len(nonzero_rows),
        "prime_contribution_rows": tuple(prime_contribution_rows),
        "active_window_boolean_cross_rayleigh": active_total,
        "full_residue_boolean_cross_rayleigh": full_total,
        "off_diagonal_window_boolean_cross_rayleigh": off_diagonal_total,
        "active_matrix_reconstruction_residual": active_total - matrix_active,
        "full_matrix_reconstruction_residual": full_total - matrix_full,
        "mixed_packet_high_q_pair_count": mixed_pair_count,
        "nonshared_single_packet_high_q_pair_count": (
            nonshared_single_pair_count),
        **classification,
        **primewise_classification,
        **obstruction,
        "finite_reduced_denominator_interference_measured": True,
        "uniform_signed_denominator_interference_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(project_reduced_denominator_interference_receipt(127))
