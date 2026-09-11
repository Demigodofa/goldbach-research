"""Lift the structured endpoint comparison to six polynomial coordinates.

For a fixed divisor support write the conductor coefficient as

    S_d(lambda) = sum_(j=0)^2 b_(d,j) lambda_j.

Every ordered frequency-pair coefficient is then linear in the six symmetric
monomials

    y=(lambda_0^2,lambda_0 lambda_1,lambda_0 lambda_2,
       lambda_1^2,lambda_1 lambda_2,lambda_2^2).

This module constructs exact positive semidefinite 6 by 6 matrices ``N``,
``D_full``, and ``D_active``.  The first is the Q-weighted high-Q endpoint
pair-square envelope, while the others are the full-period and active-window
exact-residue energies

    D_full   = sum_(Q>mA) Q sum_((r,Q)=1) |D_Q(r)|^2,
    D_active = sum_(Q>mA) Q A^-1 sum_(A<=ell<2A)|T_Q(ell)|^2.

The generalized eigenvalue is a sufficient relaxation: arbitrary vectors in
R^6 need not be rank-one symmetric squares of a vector in R^3.
"""

import math

import numpy as np

from lcm_sawtooth_exact_gcd_factorization import (
    sawtooth_gcd_mobius_transform,
)
from lcm_sawtooth_incomplete_frequency import (
    _active_modes,
    _quadratic_support_data,
)
from lcm_sawtooth_reduced_difference_mass import _validate_inputs
from lcm_sawtooth_signed_difference_bins import _stable_geometric_sum
from mobius_covariance_endpoint_probe import _prime_flags


def _symmetric_pair_coordinates(left, right):
    """Return coefficients of ``(left.lambda)(right.lambda)``."""
    return np.column_stack((
        left[:, 0] * right[:, 0],
        left[:, 0] * right[:, 1] + left[:, 1] * right[:, 0],
        left[:, 0] * right[:, 2] + left[:, 2] * right[:, 0],
        left[:, 1] * right[:, 1],
        left[:, 1] * right[:, 2] + left[:, 2] * right[:, 1],
        left[:, 2] * right[:, 2],
    ))


def _generalized_psd_receipt(numerator, denominator):
    """Return the sharp ratio on the positive range of a PSD denominator."""
    numerator = (numerator + numerator.T) / 2
    denominator = (denominator + denominator.T) / 2
    diagonal = np.diag(denominator)
    diagonal_scale = max(float(np.max(diagonal)), 1.0)
    active_diagonal = diagonal > (
        diagonal_scale * np.finfo(float).eps * 100)
    coordinate_scale = np.ones(len(diagonal))
    coordinate_scale[active_diagonal] = (
        diagonal[active_diagonal] ** -.5)
    scaling = np.outer(coordinate_scale, coordinate_scale)
    numerator = numerator * scaling
    denominator = denominator * scaling
    values, vectors = np.linalg.eigh(denominator)
    scale = max(float(values[-1]), 1.0)
    tolerance = scale * np.finfo(float).eps * 1000
    positive = values > tolerance
    null = vectors[:, ~positive]
    null_numerator = (
        float(np.linalg.eigvalsh(null.T @ numerator @ null)[-1])
        if null.shape[1] else 0.0)
    numerator_scale = max(
        float(np.linalg.eigvalsh(numerator)[-1]), 1.0)
    null_positive = null_numerator > (
        numerator_scale * np.finfo(float).eps * 10000)
    if not np.any(positive):
        ratio = float("inf") if null_positive else 0.0
        rank = 0
    elif null_positive:
        ratio = float("inf")
        rank = int(np.count_nonzero(positive))
    else:
        inverse_root = vectors[:, positive] / np.sqrt(values[positive])
        whitened = inverse_root.T @ numerator @ inverse_root
        ratio = float(np.linalg.eigvalsh(
            (whitened + whitened.T) / 2)[-1])
        rank = int(np.count_nonzero(positive))
    return {
        "largest_generalized_eigenvalue": ratio,
        "denominator_rank": rank,
        "denominator_nullity": int(denominator.shape[0] - rank),
        "largest_nullspace_numerator_eigenvalue": null_numerator,
        "numerator_positive_denominator_null_direction": bool(null_positive),
        "diagonal_equilibration_applied": True,
    }


def _lifted_frequency_data(
        modulus, ell_freeze, divisor_lower, divisor_upper):
    logarithm = math.log(modulus * ell_freeze)
    powers = np.array((logarithm ** 2, logarithm, 1.0))
    denominators = []
    numerators = []
    geometrics = []
    coordinates = []
    for denominator, polynomial in _quadratic_support_data(
            divisor_lower, divisor_upper)[1]:
        if sawtooth_gcd_mobius_transform(modulus, denominator) <= 0:
            continue
        candidates = np.arange(1, denominator, dtype=np.int64)
        primitive = candidates[np.gcd(candidates, denominator) == 1]
        geometric = _stable_geometric_sum(
            modulus, denominator, primitive)
        positive = np.abs(geometric) > 0
        primitive = primitive[positive]
        geometric = geometric[positive]
        basis = np.asarray(polynomial, dtype=float) * powers
        denominators.append(np.full(
            len(primitive), denominator, dtype=np.int64))
        numerators.append(primitive)
        geometrics.append(geometric)
        coordinates.append(np.repeat(
            basis[None, :], len(primitive), axis=0))
    if not geometrics:
        raise ArithmeticError("no positive primitive frequencies")
    return (
        np.concatenate(denominators),
        np.concatenate(numerators),
        np.concatenate(geometrics),
        np.concatenate(coordinates),
    )


def lifted_endpoint_residue_gram_receipt(
        modulus, row_count, ell_freeze,
        divisor_lower, divisor_upper):
    """Construct the exact one-prime lifted endpoint and residue matrices."""
    _validate_inputs(
        modulus, ell_freeze, row_count, divisor_lower, divisor_upper)
    denominators, numerators, geometrics, coordinates = (
        _lifted_frequency_data(
            modulus, ell_freeze, divisor_lower, divisor_upper))
    endpoint = (
        (numerators == 1) | (numerators == denominators - 1))
    threshold = modulus * row_count
    numerator_gram = np.zeros((6, 6), dtype=float)
    residue_cells = {}
    chunk_size = 64
    for first in range(0, len(denominators), chunk_size):
        left_d = denominators[first:first + chunk_size, None]
        left_k = numerators[first:first + chunk_size, None]
        common = np.lcm(left_d, denominators[None, :])
        difference_numerator = (
            left_k * (common // left_d)
            - numerators[None, :] * (common // denominators[None, :]))
        common_factor = np.gcd(np.abs(difference_numerator), common)
        reduced = common // common_factor
        high_q = reduced > threshold
        if not np.any(high_q):
            continue
        residues = np.zeros(reduced.shape, dtype=np.int64)
        residues[high_q] = (
            modulus
            * (difference_numerator[high_q] // common_factor[high_q])
            % reduced[high_q])

        left_coordinates = np.broadcast_to(
            coordinates[first:first + chunk_size, None, :],
            (*reduced.shape, 3))[high_q]
        right_coordinates = np.broadcast_to(
            coordinates[None, :, :], (*reduced.shape, 3))[high_q]
        lifted = _symmetric_pair_coordinates(
            left_coordinates, right_coordinates)
        products = (
            geometrics[first:first + chunk_size, None]
            * np.conjugate(geometrics[None, :]))[high_q]

        endpoint_pairs = (
            np.broadcast_to(
                endpoint[first:first + chunk_size, None], reduced.shape)
            & np.broadcast_to(endpoint[None, :], reduced.shape))
        selected_endpoint = endpoint_pairs[high_q]
        if np.any(selected_endpoint):
            endpoint_lifted = lifted[selected_endpoint]
            weights = (
                reduced[high_q][selected_endpoint]
                * np.abs(products[selected_endpoint]) ** 2)
            numerator_gram += (
                endpoint_lifted.T * weights) @ endpoint_lifted

        keys = np.column_stack((reduced[high_q], residues[high_q]))
        unique, inverse = np.unique(keys, axis=0, return_inverse=True)
        weighted_lifted = products[:, None] * lifted
        grouped = np.empty((len(unique), 6), dtype=complex)
        for coordinate in range(6):
            grouped[:, coordinate] = (
                np.bincount(
                    inverse, weights=weighted_lifted[:, coordinate].real)
                + 1j * np.bincount(
                    inverse, weights=weighted_lifted[:, coordinate].imag))
        for key, value in zip(unique, grouped):
            integer_key = (int(key[0]), int(key[1]))
            if integer_key in residue_cells:
                residue_cells[integer_key] += value
            else:
                residue_cells[integer_key] = value

    denominator_gram = np.zeros((6, 6), dtype=float)
    cells_by_denominator = {}
    for key, value in residue_cells.items():
        reduced_denominator = key[0]
        denominator_gram += (
            reduced_denominator
            * np.outer(value, np.conjugate(value)).real)
        cells_by_denominator.setdefault(
            reduced_denominator, []).append((key[1], value))

    active_gram = np.zeros((6, 6), dtype=float)
    rows = np.arange(row_count, 2 * row_count, dtype=np.int64)
    residue_chunk_size = 8192
    for reduced_denominator, cells in cells_by_denominator.items():
        residues = np.asarray(
            [cell[0] for cell in cells], dtype=np.int64)
        values = np.asarray([cell[1] for cell in cells], dtype=complex)
        transforms = np.zeros((row_count, 6), dtype=complex)
        for first in range(0, len(residues), residue_chunk_size):
            selected_residues = residues[
                first:first + residue_chunk_size]
            phases = np.exp(
                2j * np.pi
                * ((rows[:, None] * selected_residues[None, :])
                   % reduced_denominator)
                / reduced_denominator)
            transforms += phases @ values[
                first:first + residue_chunk_size]
        active_gram += (
            reduced_denominator / row_count
            * (transforms.T @ np.conjugate(transforms)).real)

    generalized = _generalized_psd_receipt(
        numerator_gram, denominator_gram)
    active_generalized = _generalized_psd_receipt(
        numerator_gram, active_gram)
    actual_lift = np.ones(6)
    actual_numerator = float(
        actual_lift @ numerator_gram @ actual_lift)
    actual_denominator = float(
        actual_lift @ denominator_gram @ actual_lift)
    actual_active = float(actual_lift @ active_gram @ actual_lift)
    return {
        "modulus": modulus,
        "row_count": row_count,
        "ell_freeze": ell_freeze,
        "divisor_range": (divisor_lower, divisor_upper),
        "primitive_frequency_count": len(denominators),
        "endpoint_frequency_count": int(np.count_nonzero(endpoint)),
        "high_Q_residue_cell_count": len(residue_cells),
        "endpoint_pair_square_gram": tuple(
            tuple(float(value) for value in row) for row in numerator_gram),
        "full_residue_energy_gram": tuple(
            tuple(float(value) for value in row) for row in denominator_gram),
        "active_window_residue_energy_gram": tuple(
            tuple(float(value) for value in row) for row in active_gram),
        "actual_endpoint_pair_square_envelope": actual_numerator,
        "actual_full_residue_energy": actual_denominator,
        "actual_active_window_residue_energy": actual_active,
        "actual_endpoint_over_full_residue_energy": (
            actual_numerator / actual_denominator
            if actual_denominator else float("inf")),
        "actual_endpoint_over_active_window_residue_energy": (
            actual_numerator / actual_active
            if actual_active else float("inf")),
        "actual_active_window_over_full_residue_energy": (
            actual_active / actual_denominator
            if actual_denominator else float("inf")),
        "active_window_largest_generalized_eigenvalue": active_generalized[
            "largest_generalized_eigenvalue"],
        "active_window_denominator_rank": active_generalized[
            "denominator_rank"],
        "active_window_denominator_nullity": active_generalized[
            "denominator_nullity"],
        "active_window_largest_nullspace_numerator_eigenvalue": (
            active_generalized[
                "largest_nullspace_numerator_eigenvalue"]),
        "active_window_numerator_positive_denominator_null_direction": (
            active_generalized[
                "numerator_positive_denominator_null_direction"]),
        **generalized,
        "six_coordinate_symmetric_square_identity_proved": True,
        "lifted_space_equals_rank_one_polynomial_family_proved": False,
        "prime_averaged_lifted_bound_proved": False,
    }


def project_prime_block_lifted_endpoint_scan(scale_modulus):
    """Aggregate the lifted matrices over every prime in ``[M,2M]``."""
    if type(scale_modulus) is not int or scale_modulus < 17:
        raise ValueError("scale_modulus must be an integer at least 17")
    inferred_N = scale_modulus ** (1 / .59)
    row_count = int(inferred_N ** .41)
    divisor_lower = int(inferred_N ** .15)
    divisor_upper = int(inferred_N ** .32)
    shift_length = int(inferred_N ** .1)
    ell_freeze = row_count + row_count // 2
    flags = _prime_flags(2 * scale_modulus)
    numerator = np.zeros((6, 6), dtype=float)
    denominator = np.zeros((6, 6), dtype=float)
    active_denominator = np.zeros((6, 6), dtype=float)
    weighted_active_grams = {
        mode: [np.zeros((6, 6), dtype=float),
               np.zeros((6, 6), dtype=float)]
        for mode in (
            "unweighted", "log_squared_over_m",
            "rho_log_squared_over_m", "rho_m_log_squared")}
    rows = []
    for modulus in range(scale_modulus, 2 * scale_modulus + 1):
        if not flags[modulus]:
            continue
        receipt = lifted_endpoint_residue_gram_receipt(
            modulus, row_count, ell_freeze,
            divisor_lower, divisor_upper)
        numerator += np.asarray(receipt["endpoint_pair_square_gram"])
        denominator += np.asarray(receipt["full_residue_energy_gram"])
        active_denominator += np.asarray(
            receipt["active_window_residue_energy_gram"])
        prime_numerator = np.asarray(
            receipt["endpoint_pair_square_gram"])
        prime_active = np.asarray(
            receipt["active_window_residue_energy_gram"])
        logarithmic_weight = math.log(modulus) ** 2 / modulus
        rho = len(_active_modes(modulus, shift_length)) / (modulus - 1)
        outer_weights = {
            "unweighted": 1.0,
            "log_squared_over_m": logarithmic_weight,
            "rho_log_squared_over_m": rho * logarithmic_weight,
            "rho_m_log_squared": (
                rho * modulus * math.log(modulus) ** 2),
        }
        for mode, weight in outer_weights.items():
            weighted_active_grams[mode][0] += weight * prime_numerator
            weighted_active_grams[mode][1] += weight * prime_active
        rows.append({
            "modulus": modulus,
            "lifted_ratio": receipt["largest_generalized_eigenvalue"],
            "actual_ratio": receipt[
                "actual_endpoint_over_full_residue_energy"],
            "active_window_lifted_ratio": receipt[
                "active_window_largest_generalized_eigenvalue"],
            "active_window_actual_ratio": receipt[
                "actual_endpoint_over_active_window_residue_energy"],
        })
    if not rows:
        raise ArithmeticError("prime block is empty")
    generalized = _generalized_psd_receipt(numerator, denominator)
    active_generalized = _generalized_psd_receipt(
        numerator, active_denominator)
    actual_lift = np.ones(6)
    actual_numerator = float(actual_lift @ numerator @ actual_lift)
    actual_denominator = float(actual_lift @ denominator @ actual_lift)
    actual_active = float(
        actual_lift @ active_denominator @ actual_lift)
    weighted_active_receipts = {}
    for mode, (weighted_numerator, weighted_active) in (
            weighted_active_grams.items()):
        weighted_generalized = _generalized_psd_receipt(
            weighted_numerator, weighted_active)
        weighted_actual_numerator = float(
            actual_lift @ weighted_numerator @ actual_lift)
        weighted_actual_active = float(
            actual_lift @ weighted_active @ actual_lift)
        weighted_active_receipts[mode] = {
            "largest_generalized_eigenvalue": weighted_generalized[
                "largest_generalized_eigenvalue"],
            "actual_endpoint_over_active_window_residue_energy": (
                weighted_actual_numerator / weighted_actual_active
                if weighted_actual_active else float("inf")),
            "denominator_rank": weighted_generalized["denominator_rank"],
            "denominator_nullity": weighted_generalized[
                "denominator_nullity"],
            "largest_nullspace_numerator_eigenvalue": weighted_generalized[
                "largest_nullspace_numerator_eigenvalue"],
            "numerator_positive_denominator_null_direction": (
                weighted_generalized[
                    "numerator_positive_denominator_null_direction"]),
        }
    return {
        "scale_modulus": scale_modulus,
        "prime_count": len(rows),
        "row_count": row_count,
        "ell_freeze": ell_freeze,
        "divisor_range": (divisor_lower, divisor_upper),
        "rows": tuple(rows),
        "maximum_individual_lifted_ratio": max(
            row["lifted_ratio"] for row in rows),
        "maximum_individual_actual_ratio": max(
            row["actual_ratio"] for row in rows),
        "maximum_individual_active_window_lifted_ratio": max(
            row["active_window_lifted_ratio"] for row in rows),
        "maximum_individual_active_window_actual_ratio": max(
            row["active_window_actual_ratio"] for row in rows),
        "aggregate_actual_endpoint_over_full_residue_energy": (
            actual_numerator / actual_denominator
            if actual_denominator else float("inf")),
        "aggregate_actual_endpoint_over_active_window_residue_energy": (
            actual_numerator / actual_active
            if actual_active else float("inf")),
        "aggregate_actual_active_window_over_full_residue_energy": (
            actual_active / actual_denominator
            if actual_denominator else float("inf")),
        "aggregate_endpoint_pair_square_gram": tuple(
            tuple(float(value) for value in row) for row in numerator),
        "aggregate_full_residue_energy_gram": tuple(
            tuple(float(value) for value in row) for row in denominator),
        "aggregate_active_window_residue_energy_gram": tuple(
            tuple(float(value) for value in row)
            for row in active_denominator),
        "weighted_active_window_receipts": weighted_active_receipts,
        "active_window_largest_generalized_eigenvalue": active_generalized[
            "largest_generalized_eigenvalue"],
        "active_window_denominator_rank": active_generalized[
            "denominator_rank"],
        "active_window_denominator_nullity": active_generalized[
            "denominator_nullity"],
        "active_window_largest_nullspace_numerator_eigenvalue": (
            active_generalized[
                "largest_nullspace_numerator_eigenvalue"]),
        "active_window_numerator_positive_denominator_null_direction": (
            active_generalized[
                "numerator_positive_denominator_null_direction"]),
        **generalized,
        "finite_complete_prime_block_lifted_measurement": True,
        "uniform_lifted_endpoint_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
    }


if __name__ == "__main__":
    print(project_prime_block_lifted_endpoint_scan(127))
