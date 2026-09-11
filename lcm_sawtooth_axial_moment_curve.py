"""Fit the axial Schur direction to the polynomial moment curve.

The three original degree parameters select

    lambda_2*A*L^2 + lambda_1*B*L + lambda_0*C.

On the one-parameter curve ``lambda=(t^2,t,1)``, this is the same conductor
quadratic evaluated at ``t*L``.  This module maps the distinguished axial
Schur axis from arithmetic-whitened coordinates back to the original degree
parameters and finds its exact finite projective best fit to that curve.

The stationary points of squared correlation with ``(t^2,t,1)`` are roots of
``2*p'(t)*d(t)-p(t)*d'(t)``, where ``p=lambda dot (t^2,t,1)`` and
``d=t^4+t^2+1``.  The projective limit at infinity is also checked.  A close
finite fit does not identify ``t`` analytically or prove persistence.
"""

import math

import numpy as np
from numpy.polynomial import Polynomial

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


def moment_curve_projective_fit(vector):
    """Return the closest real projective point ``(t^2,t,1)``."""
    vector = np.asarray(vector, dtype=float)
    if vector.shape != (3,) or not np.linalg.norm(vector):
        raise ValueError("vector must be a nonzero three-vector")
    variable = Polynomial((0.0, 1.0))
    correlation = (
        vector[0] * variable ** 2 + vector[1] * variable + vector[2])
    curve_square = variable ** 4 + variable ** 2 + 1
    stationary = (
        2 * correlation.deriv() * curve_square
        - correlation * curve_square.deriv())
    candidates = []
    for root in stationary.roots():
        if abs(root.imag) <= 1e-9:
            candidates.append(float(root.real))

    vector_norm = float(np.linalg.norm(vector))
    best_distance = float(np.linalg.norm(vector[1:])) / vector_norm
    best_correlation = abs(float(vector[0])) / vector_norm
    best_parameter = None
    for parameter in candidates:
        curve = np.array((parameter ** 2, parameter, 1.0))
        cosine = abs(float(vector @ curve)) / (
            vector_norm * float(np.linalg.norm(curve)))
        projection = float(vector @ curve) / float(curve @ curve) * curve
        distance = float(np.linalg.norm(vector - projection)) / vector_norm
        if distance < best_distance:
            best_distance = distance
            best_correlation = cosine
            best_parameter = parameter
    return {
        "best_parameter": best_parameter,
        "projective_moment_curve_distance": best_distance,
        "projective_moment_curve_correlation": best_correlation,
        "real_stationary_parameters": tuple(sorted(candidates)),
        "infinite_parameter_selected": best_parameter is None,
    }


def axial_moment_curve_fit_from_frame(frame, arithmetic_transform):
    """Fit the axial response using a supplied arithmetic transform."""
    arithmetic_transform = np.asarray(arithmetic_transform, dtype=float)
    if arithmetic_transform.shape != (3, 3):
        raise ValueError("arithmetic transform must be 3 by 3")
    trace_traceless = trace_traceless_transform()
    transform = symmetric_square_transform(
        arithmetic_transform) @ trace_traceless
    active = np.asarray(
        frame["aggregate_active_window_residue_energy_gram"])
    full = np.asarray(frame["aggregate_full_residue_energy_gram"])
    difference = transform.T @ (active - .5 * full) @ transform
    difference = (difference + difference.T) / 2
    response = -np.linalg.solve(
        difference[1:, 1:], difference[0, 1:])
    response_tensor = lifted_symmetric_matrix(
        trace_traceless[:, 1:] @ response)
    axial = projective_axial_distance(response_tensor)
    whitened_axis = np.asarray(axial["selected_axis"])
    original_axis = arithmetic_transform @ whitened_axis
    fit = moment_curve_projective_fit(original_axis)

    actual_in_whitened = np.linalg.solve(
        arithmetic_transform, np.ones(3))
    actual_in_whitened /= np.linalg.norm(actual_in_whitened)
    actual_cosine = abs(float(whitened_axis @ actual_in_whitened))
    actual_distance = math.sqrt(max(0.0, 1 - actual_cosine ** 2))
    return {
        "original_parameter_axis": tuple(
            float(value) for value in original_axis),
        "original_axis_normalized_constant_one": tuple(
            float(value) for value in original_axis / original_axis[2]),
        "actual_selector_projective_distance": actual_distance,
        "actual_selector_angle_degrees": math.degrees(
            math.asin(actual_distance)),
        **fit,
    }


def project_axial_moment_curve_receipt(
        scale_modulus, excluded_conductors=()):
    """Fit the complete-block axial response axis in original coordinates."""
    excluded_conductors = tuple(excluded_conductors)
    frame = project_prime_block_lifted_endpoint_scan(
        scale_modulus, excluded_conductors)
    covariance, _ = project_one_frequency_covariance(
        scale_modulus, frame, excluded_conductors)
    arithmetic_transform, _ = covariance_inverse_root(covariance)
    fit = axial_moment_curve_fit_from_frame(frame, arithmetic_transform)
    return {
        "scale_modulus": scale_modulus,
        "prime_count": frame["prime_count"],
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        "excluded_conductors": tuple(sorted(set(excluded_conductors))),
        **fit,
        "moment_curve_selects_scaled_logarithm_proved": True,
        "uniform_moment_curve_alignment_proved": False,
        "effective_log_parameter_formula_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(project_axial_moment_curve_receipt(127))
