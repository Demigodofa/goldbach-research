"""Lift a one-frequency arithmetic covariance basis to the active frame.

For every primitive supported frequency, the conductor calculation supplies a
three-vector ``b`` and geometric coefficient ``G``.  The positive matrix

    C = sum |G|^2 b b^T

is the unsummed one-frequency energy of the three degree-labelled parameters.
Whitening ``C`` is an explicit three-dimensional arithmetic normalization.
Its symmetric square is much more structured than whitening the final six by
six full-residue Gram directly.

This module tests whether that lifted basis, followed by diagonal scaling and
scalar Gershgorin, certifies ``D_active >= D_full/2``.  It is a finite
diagnostic.  Neither the covariance comparison nor the lower frame is proved
uniformly here.
"""

import numpy as np

from lcm_sawtooth_active_full_gershgorin import (
    coordinate_scaled_difference_gershgorin_receipt,
)
from lcm_sawtooth_centered_basis_gershgorin import (
    symmetric_square_transform,
)
from lcm_sawtooth_lifted_endpoint_frame import (
    _lifted_frequency_data,
    project_prime_block_lifted_endpoint_scan,
)
from mobius_covariance_endpoint_probe import _prime_flags


def weighted_coordinate_covariance(coordinates, weights):
    """Return ``sum weights[i] coordinates[i] coordinates[i]^T``."""
    coordinates = np.asarray(coordinates, dtype=float)
    weights = np.asarray(weights, dtype=float)
    if (coordinates.ndim != 2 or weights.shape != (coordinates.shape[0],)
            or np.any(weights < 0)):
        raise ValueError("require coordinate rows and matching nonnegative weights")
    return (coordinates.T * weights) @ coordinates


def covariance_inverse_root(covariance):
    """Return ``T`` with ``T.T @ covariance @ T`` equal to the identity."""
    covariance = np.asarray(covariance, dtype=float)
    if covariance.ndim != 2 or covariance.shape[0] != covariance.shape[1]:
        raise ValueError("covariance must be square")
    covariance = (covariance + covariance.T) / 2
    values, vectors = np.linalg.eigh(covariance)
    tolerance = max(float(values[-1]), 1.0) * np.finfo(float).eps * 1000
    if np.any(values <= tolerance):
        raise ValueError("covariance must be positive definite")
    return vectors / np.sqrt(values), values


def diagonally_equilibrated_spectrum(matrix):
    """Return the spectrum and condition number after diagonal scaling."""
    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be square")
    matrix = (matrix + matrix.T) / 2
    diagonal = np.diag(matrix)
    if np.any(diagonal <= 0):
        raise ValueError("matrix must have a positive diagonal")
    scale = diagonal ** -.5
    equilibrated = matrix * np.outer(scale, scale)
    values = np.linalg.eigvalsh((equilibrated + equilibrated.T) / 2)
    condition_number = (
        float(values[-1] / values[0])
        if values[0] > 0 else float("inf"))
    return values, condition_number


def project_one_frequency_covariance(scale_modulus, frame):
    """Aggregate the unsummed primitive-frequency covariance for a block."""
    covariance = np.zeros((3, 3), dtype=float)
    flags = _prime_flags(2 * scale_modulus)
    counted_primes = 0
    frequency_count = 0
    for modulus in range(scale_modulus, 2 * scale_modulus + 1):
        if not flags[modulus]:
            continue
        _, _, geometrics, coordinates = _lifted_frequency_data(
            modulus, frame["ell_freeze"], *frame["divisor_range"])
        covariance += weighted_coordinate_covariance(
            coordinates, np.abs(geometrics) ** 2)
        counted_primes += 1
        frequency_count += len(geometrics)
    if counted_primes != frame["prime_count"]:
        raise ArithmeticError("prime count disagrees with the frame scan")
    return covariance, frequency_count


def project_arithmetic_covariance_basis_receipt(scale_modulus):
    """Test the lifted one-frequency covariance basis on a prime block."""
    frame = project_prime_block_lifted_endpoint_scan(scale_modulus)
    covariance, frequency_count = project_one_frequency_covariance(
        scale_modulus, frame)
    transform, covariance_eigenvalues = covariance_inverse_root(covariance)
    whitened_covariance = transform.T @ covariance @ transform
    lifted_transform = symmetric_square_transform(transform)
    active = np.asarray(
        frame["aggregate_active_window_residue_energy_gram"])
    full = np.asarray(frame["aggregate_full_residue_energy_gram"])
    transformed_active = lifted_transform.T @ active @ lifted_transform
    transformed_full = lifted_transform.T @ full @ lifted_transform
    raw_full_spectrum, raw_full_condition = (
        diagonally_equilibrated_spectrum(full))
    arithmetic_full_spectrum, arithmetic_full_condition = (
        diagonally_equilibrated_spectrum(transformed_full))
    arithmetic = coordinate_scaled_difference_gershgorin_receipt(
        transformed_active, transformed_full)
    raw = coordinate_scaled_difference_gershgorin_receipt(active, full)
    return {
        "scale_modulus": scale_modulus,
        "prime_count": frame["prime_count"],
        "primitive_frequency_count": frequency_count,
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        "one_frequency_covariance": tuple(
            tuple(float(value) for value in row) for row in covariance),
        "one_frequency_covariance_eigenvalues": tuple(
            float(value) for value in covariance_eigenvalues),
        "covariance_whitening_max_error": float(np.max(np.abs(
            whitened_covariance - np.eye(3)))),
        "degree_parameter_transform": tuple(
            tuple(float(value) for value in row) for row in transform),
        "symmetric_square_transform": tuple(
            tuple(float(value) for value in row)
            for row in lifted_transform),
        "raw_basis_gershgorin_lower_edge": raw[
            "scaled_difference_gershgorin_lower_edge"],
        "raw_diagonally_equilibrated_full_spectrum": tuple(
            float(value) for value in raw_full_spectrum),
        "raw_diagonally_equilibrated_full_condition_number": (
            raw_full_condition),
        "arithmetic_diagonally_equilibrated_full_spectrum": tuple(
            float(value) for value in arithmetic_full_spectrum),
        "arithmetic_diagonally_equilibrated_full_condition_number": (
            arithmetic_full_condition),
        "exact_smallest_generalized_eigenvalue": frame[
            "aggregate_active_over_full_smallest_generalized_eigenvalue"],
        **arithmetic,
        "one_frequency_covariance_basis_tested": True,
        "uniform_covariance_basis_comparison_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(project_arithmetic_covariance_basis_receipt(127))
