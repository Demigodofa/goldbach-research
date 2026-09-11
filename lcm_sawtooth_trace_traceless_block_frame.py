"""Test a trace/traceless block certificate for the active lower frame.

After whitening the one-frequency three-coordinate arithmetic covariance, the
symmetric-square parameter space has the canonical decomposition

    Sym^2(R^3) = span(I) + Sym^2_0(R^3).

This module changes to one trace and five traceless coordinates, diagonally
scales the difference ``D_active-D_full/2``, and applies the two-block
Gershgorin bound

    lambda_min(H) >= min(lambda_min(A)-||B||,
                         lambda_min(C)-||B||)

for ``H=[[A,B],[B.T,C]]``.  It also reports the exact scalar Schur complement
as a diagnostic.  Computing its positivity is finite evidence, not a uniform
estimate of the trace/traceless interaction.
"""

import math

import numpy as np

from lcm_sawtooth_arithmetic_covariance_basis import (
    covariance_inverse_root,
    project_one_frequency_covariance,
)
from lcm_sawtooth_centered_basis_gershgorin import (
    symmetric_square_transform,
)
from lcm_sawtooth_lifted_endpoint_frame import (
    project_prime_block_lifted_endpoint_scan,
)


def trace_traceless_transform():
    """Return an orthonormal monomial-coordinate trace/traceless basis."""
    return np.column_stack((
        np.array((1, 0, 0, 1, 0, 1), dtype=float) / math.sqrt(3),
        np.array((1, 0, 0, -1, 0, 0), dtype=float) / math.sqrt(2),
        np.array((1, 0, 0, 1, 0, -2), dtype=float) / math.sqrt(6),
        np.array((0, 1, 0, 0, 0, 0), dtype=float),
        np.array((0, 0, 1, 0, 0, 0), dtype=float),
        np.array((0, 0, 0, 0, 1, 0), dtype=float),
    ))


def two_block_gershgorin_receipt(matrix, split):
    """Return the standard two-block lower bound for a symmetric matrix."""
    matrix = np.asarray(matrix, dtype=float)
    if (matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]
            or type(split) is not int or not 0 < split < matrix.shape[0]):
        raise ValueError("require a square matrix and an interior integer split")
    matrix = (matrix + matrix.T) / 2
    left = matrix[:split, :split]
    right = matrix[split:, split:]
    cross = matrix[:split, split:]
    left_minimum = float(np.linalg.eigvalsh(left)[0])
    right_minimum = float(np.linalg.eigvalsh(right)[0])
    cross_norm = float(np.linalg.svd(cross, compute_uv=False)[0])
    left_edge = left_minimum - cross_norm
    right_edge = right_minimum - cross_norm
    return {
        "left_block_smallest_eigenvalue": left_minimum,
        "right_block_smallest_eigenvalue": right_minimum,
        "cross_block_operator_norm": cross_norm,
        "left_block_gershgorin_edge": left_edge,
        "right_block_gershgorin_edge": right_edge,
        "two_block_gershgorin_lower_bound": min(left_edge, right_edge),
        "two_block_positive_semidefinite_certified": bool(
            min(left_edge, right_edge) >= 0),
    }


def project_trace_traceless_block_receipt(scale_modulus):
    """Test the natural 1+5 block split on a complete project prime block."""
    frame = project_prime_block_lifted_endpoint_scan(scale_modulus)
    covariance, _ = project_one_frequency_covariance(scale_modulus, frame)
    arithmetic_transform, _ = covariance_inverse_root(covariance)
    lifted_arithmetic = symmetric_square_transform(arithmetic_transform)
    trace_traceless = trace_traceless_transform()
    transform = lifted_arithmetic @ trace_traceless
    active = transform.T @ np.asarray(
        frame["aggregate_active_window_residue_energy_gram"]) @ transform
    full = transform.T @ np.asarray(
        frame["aggregate_full_residue_energy_gram"]) @ transform
    diagonal = np.diag(full)
    if np.any(diagonal <= 0):
        raise ArithmeticError("transformed full Gram has nonpositive diagonal")
    scale = diagonal ** -.5
    difference = (active - .5 * full) * np.outer(scale, scale)
    difference = (difference + difference.T) / 2
    block = two_block_gershgorin_receipt(difference, 1)
    traceless = difference[1:, 1:]
    cross = difference[:1, 1:]
    trace_schur_complement = float(
        difference[0, 0]
        - (cross @ np.linalg.solve(traceless, cross.T))[0, 0])
    exact_values = np.linalg.eigvalsh(difference)
    return {
        "scale_modulus": scale_modulus,
        "prime_count": frame["prime_count"],
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        "trace_traceless_transform": tuple(
            tuple(float(value) for value in row)
            for row in trace_traceless),
        "trace_schur_complement": trace_schur_complement,
        "exact_scaled_difference_smallest_eigenvalue": float(
            exact_values[0]),
        **block,
        "one_trace_five_traceless_split_tested": True,
        "uniform_trace_traceless_interaction_bound_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(project_trace_traceless_block_receipt(127))
