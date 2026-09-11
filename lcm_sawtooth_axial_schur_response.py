"""Measure axial structure in the trace/traceless Schur response.

In the arithmetic-whitened symmetric-square coordinates, split the candidate
half-frame difference into trace and traceless blocks

    H = [[a, b], [b.T, C]].

Eliminating the traceless block uses the response ``v=-C^{-1}b.T``.  Map that
five-vector back to a traceless symmetric 3 by 3 tensor.  An axial tensor has
the form ``alpha*(u u.T-I/3)`` and hence eigenvalue pattern ``2:-1:-1`` up to
scale and permutation.

The projective Frobenius distance to this axial orbit is rotation invariant.
Small finite values would isolate a possible one-axis arithmetic mechanism;
they do not prove it persists uniformly or that replacing the response by its
best axial approximation preserves positivity.
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
from lcm_sawtooth_trace_traceless_block_frame import (
    trace_traceless_transform,
)


def lifted_symmetric_matrix(vector):
    vector = np.asarray(vector, dtype=float)
    if vector.shape != (6,):
        raise ValueError("vector must have six coordinates")
    return np.array((
        (vector[0], vector[1], vector[2]),
        (vector[1], vector[3], vector[4]),
        (vector[2], vector[4], vector[5]),
    ))


def projective_axial_distance(matrix):
    """Return distance to ``alpha*(u u.T-I/3)`` and tensor eigenvalues."""
    matrix = np.asarray(matrix, dtype=float)
    if matrix.shape != (3, 3):
        raise ValueError("matrix must be 3 by 3")
    matrix = (matrix + matrix.T) / 2
    norm = float(np.linalg.norm(matrix, "fro"))
    if not norm:
        raise ValueError("matrix must be nonzero")
    if abs(float(np.trace(matrix))) > norm * 1e-10:
        raise ValueError("matrix must be traceless")
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    patterns = (
        np.array((2.0, -1.0, -1.0)),
        np.array((-1.0, 2.0, -1.0)),
        np.array((-1.0, -1.0, 2.0)),
    )
    distances = []
    for pattern in patterns:
        cosine = abs(float(eigenvalues @ pattern)) / (
            float(np.linalg.norm(eigenvalues))
            * float(np.linalg.norm(pattern)))
        distances.append(math.sqrt(max(0.0, 1 - cosine ** 2)))
    selected = int(np.argmin(distances))
    return {
        "projective_axial_frobenius_distance": float(distances[selected]),
        "tensor_eigenvalues": tuple(float(value) for value in eigenvalues),
        "selected_axial_eigenvalue_index": selected,
        "selected_axis": tuple(
            float(value) for value in eigenvectors[:, selected]),
    }


def project_axial_schur_response_receipt(scale_modulus):
    """Measure raw and Schur-response axiality on a complete prime block."""
    frame = project_prime_block_lifted_endpoint_scan(scale_modulus)
    covariance, _ = project_one_frequency_covariance(scale_modulus, frame)
    arithmetic_transform, _ = covariance_inverse_root(covariance)
    lifted_arithmetic = symmetric_square_transform(arithmetic_transform)
    trace_traceless = trace_traceless_transform()
    transform = lifted_arithmetic @ trace_traceless
    active = np.asarray(
        frame["aggregate_active_window_residue_energy_gram"])
    full = np.asarray(frame["aggregate_full_residue_energy_gram"])
    difference = transform.T @ (active - .5 * full) @ transform
    difference = (difference + difference.T) / 2
    cross = difference[:1, 1:]
    traceless = difference[1:, 1:]
    traceless_values = np.linalg.eigvalsh(traceless)
    if traceless_values[0] <= 0:
        raise ArithmeticError("traceless block must be positive definite")
    response = -np.linalg.solve(traceless, cross.T)[:, 0]
    response_vector = trace_traceless[:, 1:] @ response
    response_axial = projective_axial_distance(
        lifted_symmetric_matrix(response_vector))
    return {
        "scale_modulus": scale_modulus,
        "prime_count": frame["prime_count"],
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        "traceless_block_smallest_eigenvalue": float(
            traceless_values[0]),
        "schur_response_coordinates": tuple(
            float(value) for value in response),
        "schur_response_tensor": tuple(
            tuple(float(value) for value in row)
            for row in lifted_symmetric_matrix(response_vector)),
        **response_axial,
        "finite_axial_response_measured": True,
        "uniform_axial_schur_response_proved": False,
        "axial_reduction_preserves_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(project_axial_schur_response_receipt(127))
