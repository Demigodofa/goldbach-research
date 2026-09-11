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


def conductor_high_q_retention_obstruction(
        modulus, row_count, divisor_lower, divisor_upper, conductors):
    """Prove factor by factor when high-Q packets retain each conductor."""
    conductors = tuple(sorted(set(conductors)))
    if (len(conductors) != 2
            or any(type(value) is not int or value < 2 for value in conductors)):
        raise ValueError("require two distinct integer conductors")
    if (type(modulus) is not int or type(row_count) is not int
            or modulus < 2 or row_count < 1):
        raise ValueError("modulus and row_count must be positive integers")

    def prime_factors(value):
        factors = []
        divisor = 2
        while divisor * divisor <= value:
            if value % divisor == 0:
                factors.append(divisor)
                value //= divisor
                if value % divisor == 0:
                    raise ValueError("conductors must be squarefree")
            divisor += 1
        if value > 1:
            factors.append(value)
        return tuple(factors)

    support = tuple(
        denominator for denominator, _
        in _quadratic_support_data(divisor_lower, divisor_upper)[1])
    threshold = modulus * row_count
    conductor_rows = []
    for conductor, opposite in zip(conductors, reversed(conductors)):
        factor_rows = []
        for prime in prime_factors(conductor):
            upper_bound = max(
                math.lcm(conductor, denominator) // prime
                for denominator in support if denominator != opposite)
            factor_rows.append({
                "prime_factor": prime,
                "nondivisible_reduced_denominator_upper_bound": upper_bound,
                "prime_retained_by_high_q_cutoff": bool(
                    upper_bound <= threshold),
            })
        conductor_rows.append({
            "conductor": conductor,
            "factor_rows": tuple(factor_rows),
            "conductor_retained_by_high_q_cutoff": all(
                row["prime_retained_by_high_q_cutoff"]
                for row in factor_rows),
        })
    linked_core = math.lcm(*conductors)
    core_forced = all(
        row["conductor_retained_by_high_q_cutoff"]
        for row in conductor_rows)
    return {
        "linked_conductor_core": linked_core,
        "conductor_retention_high_q_threshold": threshold,
        "conductor_retention_rows": tuple(conductor_rows),
        "every_single_packet_retains_its_conductor_proved": bool(core_forced),
        "every_interfering_denominator_has_linked_core_proved": bool(
            core_forced),
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
    nonconductor_single_pair_count = 0
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
        nonconductor_single_pair_count += int(np.count_nonzero(
            ((selected_categories == 1)
             & (selected_reduced % conductors[0] != 0))
            | ((selected_categories == 2)
               & (selected_reduced % conductors[1] != 0))))

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
    return (packets, tuple(pair_counts), nonshared_single_pair_count,
            nonconductor_single_pair_count)


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


def _offdiagonal_lags_by_denominator(left, right, row_first, row_count):
    """Resolve direct packet interference by cyclic residue lag ``h=r-s``."""
    if (type(row_first) is not int or type(row_count) is not int
            or row_first < 0 or row_count < 1):
        raise ValueError("row range must be integral and nonempty")
    result = {}
    denominators = sorted({key[0] for key in left} | {key[0] for key in right})
    rows = np.arange(row_first, row_first + row_count, dtype=np.int64)
    for denominator in denominators:
        left_values = np.zeros(denominator, dtype=complex)
        right_values = np.zeros(denominator, dtype=complex)
        for (local_denominator, residue), value in left.items():
            if local_denominator == denominator:
                left_values[residue] += value
        for (local_denominator, residue), value in right.items():
            if local_denominator == denominator:
                right_values[residue] += value
        correlation = np.fft.ifft(
            np.fft.fft(left_values) * np.conjugate(np.fft.fft(right_values)))
        lags = np.arange(denominator, dtype=np.int64)
        kernel = np.mean(np.exp(
            2j * np.pi * rows[:, None] * lags[None, :] / denominator),
            axis=0)
        contributions = 2 * denominator * (kernel * correlation).real
        contributions[0] = 0.0
        result[denominator] = contributions
    return result


def classify_near_lag_mass(
        lag_contributions, row_count, minimum_absolute_mass_fraction=.75,
        minimum_passing_channel_count=2):
    """Test absolute-lag-mass concentration in the kernel main lobe."""
    lag_contributions = dict(lag_contributions)
    if not lag_contributions:
        raise ValueError("at least one lag channel is required")
    if type(row_count) is not int or row_count < 1:
        raise ValueError("row_count must be a positive integer")
    if not 0 < minimum_absolute_mass_fraction <= 1:
        raise ValueError("mass fraction threshold must lie in (0,1]")
    if (type(minimum_passing_channel_count) is not int
            or not 1 <= minimum_passing_channel_count <= len(lag_contributions)):
        raise ValueError("passing channel count must fit the channel set")

    channel_rows = []
    for denominator in sorted(lag_contributions):
        contributions = np.asarray(
            lag_contributions[denominator], dtype=float)
        if contributions.shape != (denominator,):
            raise ValueError("each lag array must have length Q")
        distances = np.minimum(
            np.arange(denominator),
            denominator - np.arange(denominator))
        near = distances * row_count <= denominator
        near[0] = False
        absolute_mass = float(np.sum(np.abs(contributions[1:])))
        if not absolute_mass:
            raise ArithmeticError("lag channel has zero absolute mass")
        near_mass = float(np.sum(np.abs(contributions[near])))
        fraction = near_mass / absolute_mass
        nonzero_lags = np.flatnonzero(np.abs(contributions) > 1e-12)
        ranked = sorted(
            nonzero_lags,
            key=lambda lag: abs(contributions[lag]), reverse=True)
        channel_rows.append({
            "reduced_denominator": denominator,
            "near_lag_maximum_cyclic_distance": denominator // row_count,
            "absolute_lag_mass": absolute_mass,
            "near_lag_absolute_mass": near_mass,
            "near_lag_absolute_mass_fraction": fraction,
            "signed_lag_sum": float(np.sum(contributions)),
            "near_lag_signed_sum": float(np.sum(contributions[near])),
            "far_lag_signed_sum": float(np.sum(contributions[~near])),
            "nonzero_lag_count": len(nonzero_lags),
            "near_lag_absolute_mass_hypothesis_passes": bool(
                fraction >= minimum_absolute_mass_fraction),
            "top_absolute_lags": tuple(
                (int(lag), int(distances[lag]), float(contributions[lag]),
                 float(abs(contributions[lag]) / absolute_mass))
                for lag in ranked[:10]),
        })
    passing = tuple(
        row["reduced_denominator"] for row in channel_rows
        if row["near_lag_absolute_mass_hypothesis_passes"])
    return {
        "near_lag_rule": "min(h,Q-h)*R<=Q",
        "minimum_near_lag_absolute_mass_fraction": (
            minimum_absolute_mass_fraction),
        "minimum_passing_near_lag_channel_count": (
            minimum_passing_channel_count),
        "near_lag_channel_rows": tuple(channel_rows),
        "near_lag_passing_denominators": passing,
        "near_lag_passing_channel_count": len(passing),
        "near_lag_absolute_mass_hypothesis_passes": bool(
            len(passing) >= minimum_passing_channel_count),
    }


def classify_crt_rank_one_near_lag_separation(
        lag_contributions, linked_core, row_count,
        minimum_rank_one_energy_fraction=.9,
        minimum_passing_channel_count=2):
    """Test rank-one CRT separation of the kernel-main-lobe lag term."""
    lag_contributions = dict(lag_contributions)
    if not lag_contributions:
        raise ValueError("at least one lag channel is required")
    if type(linked_core) is not int or linked_core < 2:
        raise ValueError("linked_core must be an integer at least two")
    if type(row_count) is not int or row_count < 1:
        raise ValueError("row_count must be a positive integer")
    if not 0 < minimum_rank_one_energy_fraction <= 1:
        raise ValueError("rank-one energy threshold must lie in (0,1]")
    if (type(minimum_passing_channel_count) is not int
            or not 1 <= minimum_passing_channel_count <= len(lag_contributions)):
        raise ValueError("passing channel count must fit the channel set")

    channel_rows = []
    for denominator in sorted(lag_contributions):
        contributions = np.asarray(
            lag_contributions[denominator], dtype=float)
        if contributions.shape != (denominator,):
            raise ValueError("each lag array must have length Q")
        if denominator % linked_core:
            raise ArithmeticError("interfering denominator lacks linked core")
        cofactor = denominator // linked_core
        if math.gcd(linked_core, cofactor) != 1:
            raise ArithmeticError("core and cofactor are not CRT-coprime")
        distances = np.minimum(
            np.arange(denominator),
            denominator - np.arange(denominator))
        near = distances * row_count <= denominator
        near[0] = False
        near_contributions = contributions.copy()
        near_contributions[~near] = 0.0
        matrix = np.empty((linked_core, cofactor), dtype=float)
        for lag, value in enumerate(near_contributions):
            matrix[lag % linked_core, lag % cofactor] = value
        reconstructed = np.empty(denominator, dtype=float)
        for lag in range(denominator):
            reconstructed[lag] = matrix[
                lag % linked_core, lag % cofactor]
        singular_values = np.linalg.svd(matrix, compute_uv=False)
        energy = float(np.sum(singular_values ** 2))
        if not energy:
            raise ArithmeticError("CRT lag matrix has zero energy")
        rank_one_fraction = float(singular_values[0] ** 2 / energy)
        channel_rows.append({
            "reduced_denominator": denominator,
            "linked_core": linked_core,
            "crt_cofactor": cofactor,
            "near_lag_rule": "min(h,Q-h)*R<=Q",
            "crt_reconstruction_maximum_error": float(np.max(np.abs(
                reconstructed - near_contributions))),
            "singular_values": tuple(float(value) for value in singular_values),
            "rank_one_frobenius_energy_fraction": rank_one_fraction,
            "crt_rank_one_near_lag_separation_hypothesis_passes": bool(
                rank_one_fraction >= minimum_rank_one_energy_fraction),
        })
    passing = tuple(
        row["reduced_denominator"] for row in channel_rows
        if row["crt_rank_one_near_lag_separation_hypothesis_passes"])
    return {
        "minimum_crt_rank_one_energy_fraction": (
            minimum_rank_one_energy_fraction),
        "minimum_passing_crt_channel_count": minimum_passing_channel_count,
        "crt_rank_one_near_lag_channel_rows": tuple(channel_rows),
        "crt_rank_one_near_lag_passing_denominators": passing,
        "crt_rank_one_near_lag_passing_channel_count": len(passing),
        "crt_rank_one_near_lag_separation_hypothesis_passes": bool(
            len(passing) >= minimum_passing_channel_count),
    }


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
    aggregate_lags = {}
    prime_contribution_rows = []
    mixed_pair_count = 0
    nonshared_single_pair_count = 0
    nonconductor_single_pair_count = 0
    for frame_row in baseline["rows"]:
        packets, pair_counts, nonshared_count, nonconductor_count = (
            _packet_residue_cells(
            frame_row["modulus"], baseline["row_count"],
            baseline["ell_freeze"], baseline["divisor_range"],
            original_direction, conductors, shared_prime))
        mixed_pair_count += pair_counts[3]
        nonshared_single_pair_count += nonshared_count
        nonconductor_single_pair_count += nonconductor_count
        contributions = _cross_by_denominator(
            packets[1], packets[2], baseline["row_count"])
        lag_contributions = _offdiagonal_lags_by_denominator(
            packets[1], packets[2], baseline["row_count"],
            baseline["row_count"])
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
            if denominator in aggregate_lags:
                aggregate_lags[denominator] += lag_contributions[denominator]
            else:
                aggregate_lags[denominator] = lag_contributions[denominator]
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
    selected_lags = {
        row["reduced_denominator"]: aggregate_lags[
            row["reduced_denominator"]]
        for row in nonzero_rows}
    lag_classification = classify_near_lag_mass(
        selected_lags, baseline["row_count"])
    retention = conductor_high_q_retention_obstruction(
        scale_modulus, baseline["row_count"], *baseline["divisor_range"],
        conductors)
    crt_classification = classify_crt_rank_one_near_lag_separation(
        selected_lags, retention["linked_conductor_core"],
        baseline["row_count"])
    lag_reconstruction_errors = tuple(
        (row["reduced_denominator"],
         float(np.sum(selected_lags[row["reduced_denominator"]])
               - row["off_diagonal_window_interference"]))
        for row in nonzero_rows)
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
        "lag_reconstruction_errors": lag_reconstruction_errors,
        "active_window_boolean_cross_rayleigh": active_total,
        "full_residue_boolean_cross_rayleigh": full_total,
        "off_diagonal_window_boolean_cross_rayleigh": off_diagonal_total,
        "active_matrix_reconstruction_residual": active_total - matrix_active,
        "full_matrix_reconstruction_residual": full_total - matrix_full,
        "mixed_packet_high_q_pair_count": mixed_pair_count,
        "nonshared_single_packet_high_q_pair_count": (
            nonshared_single_pair_count),
        "nonconductor_single_packet_high_q_pair_count": (
            nonconductor_single_pair_count),
        **classification,
        **primewise_classification,
        **lag_classification,
        **retention,
        **crt_classification,
        "linked_core_crt_near_lag_separation_hypothesis_passes": bool(
            retention["every_interfering_denominator_has_linked_core_proved"]
            and crt_classification[
                "crt_rank_one_near_lag_separation_hypothesis_passes"]),
        **obstruction,
        "finite_reduced_denominator_interference_measured": True,
        "uniform_signed_denominator_interference_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(project_reduced_denominator_interference_receipt(127))
