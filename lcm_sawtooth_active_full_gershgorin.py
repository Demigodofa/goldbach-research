"""Test a Gershgorin certificate for the lifted active/full lower frame.

For positive definite ``D_full``, diagonally equilibrate it, use its symmetric
eigendecomposition to whiten it to the identity, and write the transformed
active form as ``W``.  Gershgorin then proves

    D_active >= min_i(W_ii-sum_(j!=i)|W_ij|) D_full.

The finite certificate tests whether entrywise control could plausibly prove
the candidate one-half lower frame.  It does not bound those entries
uniformly in the project scale.
"""

import numpy as np

from lcm_sawtooth_lifted_endpoint_frame import (
    project_prime_block_lifted_endpoint_scan,
)


def whitened_gershgorin_lower_frame_receipt(active, full):
    active = np.asarray(active, dtype=float)
    full = np.asarray(full, dtype=float)
    if (active.ndim != 2 or active.shape[0] != active.shape[1]
            or full.shape != active.shape):
        raise ValueError("active and full must be same-size square matrices")
    active = (active + active.T) / 2
    full = (full + full.T) / 2
    diagonal = np.diag(full)
    diagonal_scale = max(float(np.max(diagonal)), 1.0)
    if np.any(diagonal <= diagonal_scale * np.finfo(float).eps * 100):
        raise ValueError("full matrix must have a positive diagonal")
    coordinate_scale = diagonal ** -.5
    scaling = np.outer(coordinate_scale, coordinate_scale)
    active_scaled = active * scaling
    full_scaled = full * scaling
    values, vectors = np.linalg.eigh(full_scaled)
    tolerance = max(float(values[-1]), 1.0) * np.finfo(float).eps * 1000
    if np.any(values <= tolerance):
        raise ValueError("full matrix must be positive definite")
    inverse_root = vectors / np.sqrt(values)
    whitened = inverse_root.T @ active_scaled @ inverse_root
    whitened = (whitened + whitened.T) / 2
    diagonal = np.diag(whitened)
    radii = np.sum(np.abs(whitened), axis=1) - np.abs(diagonal)
    lower_edges = diagonal - radii
    eigenvalues = np.linalg.eigvalsh(whitened)
    return {
        "dimension": active.shape[0],
        "whitened_active_matrix": tuple(
            tuple(float(value) for value in row) for row in whitened),
        "whitened_diagonal": tuple(float(value) for value in diagonal),
        "gershgorin_radii": tuple(float(value) for value in radii),
        "gershgorin_lower_edges": tuple(
            float(value) for value in lower_edges),
        "gershgorin_lower_frame_bound": float(np.min(lower_edges)),
        "exact_smallest_generalized_eigenvalue": float(eigenvalues[0]),
        "exact_largest_generalized_eigenvalue": float(eigenvalues[-1]),
        "one_half_lower_frame_certified": bool(np.min(lower_edges) >= .5),
        "uniform_entrywise_bound_proved": False,
    }


def coordinate_scaled_difference_gershgorin_receipt(
        active, full, candidate=.5):
    """Test diagonal scaling without the essential full-Gram whitening."""
    active = np.asarray(active, dtype=float)
    full = np.asarray(full, dtype=float)
    if (active.ndim != 2 or active.shape[0] != active.shape[1]
            or full.shape != active.shape or candidate < 0):
        raise ValueError("require same-size square matrices and candidate>=0")
    diagonal = np.diag(full)
    if np.any(diagonal <= 0):
        raise ValueError("full matrix must have a positive diagonal")
    coordinate_scale = diagonal ** -.5
    difference = (active - candidate * full) * np.outer(
        coordinate_scale, coordinate_scale)
    difference = (difference + difference.T) / 2
    difference_diagonal = np.diag(difference)
    radii = (
        np.sum(np.abs(difference), axis=1)
        - np.abs(difference_diagonal))
    lower_edges = difference_diagonal - radii
    return {
        "candidate_lower_frame_constant": candidate,
        "scaled_difference_diagonal": tuple(
            float(value) for value in difference_diagonal),
        "scaled_difference_radii": tuple(float(value) for value in radii),
        "scaled_difference_gershgorin_edges": tuple(
            float(value) for value in lower_edges),
        "scaled_difference_gershgorin_lower_edge": float(
            np.min(lower_edges)),
        "coordinate_scaled_gershgorin_certifies_candidate": bool(
            np.min(lower_edges) >= 0),
        "full_gram_whitening_applied": False,
    }


def project_aggregate_gershgorin_receipt(scale_modulus):
    frame = project_prime_block_lifted_endpoint_scan(scale_modulus)
    receipt = whitened_gershgorin_lower_frame_receipt(
        frame["aggregate_active_window_residue_energy_gram"],
        frame["aggregate_full_residue_energy_gram"])
    coordinate_scaled = coordinate_scaled_difference_gershgorin_receipt(
        frame["aggregate_active_window_residue_energy_gram"],
        frame["aggregate_full_residue_energy_gram"])
    return {
        "scale_modulus": scale_modulus,
        "prime_count": frame["prime_count"],
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        **receipt,
        "coordinate_scaled_one_half_receipt": coordinate_scaled,
        "finite_complete_prime_block_measurement": True,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(project_aggregate_gershgorin_receipt(127))
