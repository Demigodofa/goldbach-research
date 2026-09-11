"""Compare the best axial Schur response with the exact frame margin.

For the trace/traceless half-frame difference

    H = [[a,b],[b.T,C]],

the exact eliminating response is ``v=-C^{-1}b.T`` and the trace Schur margin
is ``s=a+b*v``.  Let ``v_ax`` be the coefficient vector of the best
Frobenius axial approximation to the traceless tensor represented by ``v``.
Completing the square gives the exact finite identity

    s = q(v_ax) - (v_ax-v).T C (v_ax-v),

where ``q(w)=a+2*b*w+w.T*C*w``.  This separates a one-axis trial value from a
nonaxial energy error.  The module measures that decomposition; it proves no
uniform bounds for either term.
"""

import numpy as np

from lcm_sawtooth_arithmetic_covariance_basis import (
    covariance_inverse_root,
    project_one_frequency_covariance,
)
from lcm_sawtooth_axial_schur_response import (
    lifted_symmetric_matrix,
    projective_axial_distance,
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


def symmetric_matrix_coordinates(matrix):
    """Return the repository's six direct symmetric-matrix coordinates."""
    matrix = np.asarray(matrix, dtype=float)
    if matrix.shape != (3, 3):
        raise ValueError("matrix must be 3 by 3")
    return np.array((
        matrix[0, 0], matrix[0, 1], matrix[0, 2],
        matrix[1, 1], matrix[1, 2], matrix[2, 2],
    ))


def best_axial_approximation(matrix):
    """Return the Frobenius projection onto the closest axial tensor ray."""
    axial = projective_axial_distance(matrix)
    axis = np.asarray(axial["selected_axis"])
    generator = np.outer(axis, axis) - np.eye(3) / 3
    matrix = np.asarray(matrix, dtype=float)
    coefficient = float(np.sum(matrix * generator) / np.sum(generator ** 2))
    approximation = coefficient * generator
    return approximation, coefficient, axial


def project_axial_schur_energy_receipt(scale_modulus):
    """Measure the axial trial/nonaxial error decomposition on one block."""
    frame = project_prime_block_lifted_endpoint_scan(scale_modulus)
    covariance, _ = project_one_frequency_covariance(scale_modulus, frame)
    arithmetic_transform, _ = covariance_inverse_root(covariance)
    lifted_arithmetic = symmetric_square_transform(arithmetic_transform)
    trace_traceless = trace_traceless_transform()
    traceless_basis = trace_traceless[:, 1:]
    transform = lifted_arithmetic @ trace_traceless
    active = np.asarray(
        frame["aggregate_active_window_residue_energy_gram"])
    full = np.asarray(frame["aggregate_full_residue_energy_gram"])
    difference = transform.T @ (active - .5 * full) @ transform
    difference = (difference + difference.T) / 2
    trace_value = float(difference[0, 0])
    cross = difference[0, 1:]
    traceless = difference[1:, 1:]
    if np.linalg.eigvalsh(traceless)[0] <= 0:
        raise ArithmeticError("traceless block must be positive definite")
    response = -np.linalg.solve(traceless, cross)
    response_tensor = lifted_symmetric_matrix(traceless_basis @ response)
    axial_tensor, axial_coefficient, axial = best_axial_approximation(
        response_tensor)
    axial_response = traceless_basis.T @ symmetric_matrix_coordinates(
        axial_tensor)
    residual = axial_response - response
    schur_margin = trace_value + float(cross @ response)
    nonaxial_energy_error = float(residual @ traceless @ residual)
    axial_trial_value = float(
        trace_value + 2 * cross @ axial_response
        + axial_response @ traceless @ axial_response)
    identity_error = abs(
        schur_margin - (axial_trial_value - nonaxial_energy_error))
    response_energy = float(response @ traceless @ response)
    return {
        "scale_modulus": scale_modulus,
        "prime_count": frame["prime_count"],
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        "schur_response_projective_axial_distance": axial[
            "projective_axial_frobenius_distance"],
        "axial_coefficient": axial_coefficient,
        "schur_margin": schur_margin,
        "axial_trial_value": axial_trial_value,
        "nonaxial_energy_error": nonaxial_energy_error,
        "completion_identity_absolute_error": identity_error,
        "nonaxial_error_over_schur_margin": (
            nonaxial_energy_error / schur_margin),
        "nonaxial_error_over_axial_trial_value": (
            nonaxial_energy_error / axial_trial_value),
        "nonaxial_error_over_response_energy": (
            nonaxial_energy_error / response_energy),
        "finite_axial_energy_decomposition_measured": True,
        "uniform_axial_trial_lower_bound_proved": False,
        "uniform_nonaxial_energy_bound_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(project_axial_schur_energy_receipt(127))
