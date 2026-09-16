"""Moment-square diagnostics for Mobius lower-frame nullspaces.

The rank-aware lower-frame receipt isolated ``M=167`` as the checked scale
where the full Gram is rank deficient but the quotient lower-frame minimum
still survives.  This module tests whether such a null direction has
additional structure: proximity to the symmetric square of the moment curve

    lambda(t) = (t^2, t, 1).

In six symmetric coordinates this curve is

    (t^4, t^3, t^2, t^2, t, 1).

The calculation is finite evidence only.  It does not prove eventual support
activation or a uniform nullspace theorem.
"""

import numpy as np
from numpy.polynomial import Polynomial

from lcm_sawtooth_axial_schur_response import lifted_symmetric_matrix


def moment_square_vector(parameter):
    """Return the six-coordinate square of ``(t^2,t,1)``."""
    parameter = float(parameter)
    return np.array((
        parameter ** 4,
        parameter ** 3,
        parameter ** 2,
        parameter ** 2,
        parameter,
        1.0,
    ))


def moment_square_projective_fit(vector):
    """Fit a six-vector to the projective moment-square curve."""
    vector = np.asarray(vector, dtype=float)
    if vector.shape != (6,) or not np.linalg.norm(vector):
        raise ValueError("vector must be a nonzero six-vector")
    variable = Polynomial((0.0, 1.0))
    correlation = (
        vector[0] * variable ** 4
        + vector[1] * variable ** 3
        + (vector[2] + vector[3]) * variable ** 2
        + vector[4] * variable
        + vector[5])
    curve_square = (
        variable ** 8 + variable ** 6
        + 2 * variable ** 4 + variable ** 2 + 1)
    stationary = (
        2 * correlation.deriv() * curve_square
        - correlation * curve_square.deriv())
    candidates = []
    for root in stationary.roots():
        if abs(root.imag) <= 1e-8:
            candidates.append(float(root.real))

    vector_norm = float(np.linalg.norm(vector))
    best_parameter = None
    best_distance = float(np.linalg.norm(vector[1:])) / vector_norm
    best_correlation = abs(float(vector[0])) / vector_norm
    best_projection = np.array((1.0, 0.0, 0.0, 0.0, 0.0, 0.0))
    for parameter in candidates:
        curve = moment_square_vector(parameter)
        projection = float(vector @ curve) / float(curve @ curve) * curve
        distance = float(np.linalg.norm(vector - projection) / vector_norm)
        correlation_value = abs(float(vector @ curve)) / (
            vector_norm * float(np.linalg.norm(curve)))
        if distance < best_distance:
            best_parameter = parameter
            best_distance = distance
            best_correlation = correlation_value
            best_projection = curve / float(np.linalg.norm(curve))
    return {
        "best_parameter": best_parameter,
        "projective_moment_square_distance": best_distance,
        "projective_moment_square_correlation": best_correlation,
        "moment_square_projection_unit": tuple(
            float(value) for value in best_projection),
        "real_stationary_parameters": tuple(sorted(candidates)),
        "infinite_parameter_selected": best_parameter is None,
    }


def symmetric_matrix_rank_shape(vector):
    """Return rank-one diagnostics for a six-coordinate symmetric matrix."""
    matrix = lifted_symmetric_matrix(vector)
    values = np.linalg.eigvalsh(matrix)
    scale = max(abs(float(values[-1])), 1.0)
    return {
        "symmetric_matrix_eigenvalues": tuple(
            float(value) for value in values),
        "symmetric_matrix_trace": float(np.trace(matrix)),
        "symmetric_matrix_determinant": float(np.linalg.det(matrix)),
        "second_over_largest_eigenvalue": float(values[-2] / scale),
        "smallest_over_largest_eigenvalue": float(values[0] / scale),
        "nearly_rank_one_positive_semidefinite": bool(
            values[0] >= -scale * 1e-8
            and abs(values[-2]) <= scale * 1e-3),
    }
