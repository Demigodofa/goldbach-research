"""Metric-aware moment-square support diagnostics.

The lower-frame support problem depends on the metric used to compare
six-coordinate vectors.  Raw Euclidean energy along

    (t^4,t^3,t^2,t^2,t,1)

can be positive while the same curve is nearly null in the diagonally
equilibrated full-Gram quotient used by the rank-aware lower-frame test.
This module records that distinction.
"""

import numpy as np
from numpy.polynomial import Polynomial

from mobius_moment_square_nullspace import moment_square_vector


def moment_square_quadratic_quotient_minimum(numerator, denominator):
    """Minimize ``y(t)^T numerator y(t) / y(t)^T denominator y(t)``."""
    numerator = np.asarray(numerator, dtype=float)
    denominator = np.asarray(denominator, dtype=float)
    if numerator.shape != (6, 6) or denominator.shape != (6, 6):
        raise ValueError("numerator and denominator must be 6 by 6")
    numerator = (numerator + numerator.T) / 2
    denominator = (denominator + denominator.T) / 2

    variable = Polynomial((0.0, 1.0))
    curve = (
        variable ** 4,
        variable ** 3,
        variable ** 2,
        variable ** 2,
        variable,
        Polynomial((1.0,)),
    )
    top = Polynomial((0.0,))
    bottom = Polynomial((0.0,))
    for left in range(6):
        for right in range(6):
            top += float(numerator[left, right]) * curve[left] * curve[right]
            bottom += (
                float(denominator[left, right])
                * curve[left] * curve[right])
    stationary = top.deriv() * bottom - top * bottom.deriv()
    candidates = []
    for root in stationary.roots():
        if abs(root.imag) <= 1e-7:
            candidates.append(float(root.real))

    def quotient(parameter):
        vector = moment_square_vector(parameter)
        denominator_value = float(vector @ denominator @ vector)
        if denominator_value <= 0:
            return float("inf")
        return float(vector @ numerator @ vector / denominator_value)

    best_parameter = None
    best_value = (
        float(numerator[0, 0] / denominator[0, 0])
        if denominator[0, 0] > 0 else float("inf"))
    for parameter in candidates:
        value = quotient(parameter)
        if value < best_value:
            best_value = value
            best_parameter = parameter
    return {
        "minimum_value": best_value,
        "minimizing_parameter": best_parameter,
        "real_stationary_parameters": tuple(sorted(candidates)),
        "infinite_parameter_selected": best_parameter is None,
    }


def diagonal_equilibration_metric(full):
    """Return the denominator metric induced by full-Gram equilibration."""
    full = np.asarray(full, dtype=float)
    if full.shape != (6, 6):
        raise ValueError("full must be 6 by 6")
    full = (full + full.T) / 2
    diagonal = np.diag(full)
    diagonal_scale = max(float(np.max(diagonal)), 1.0)
    active = diagonal > diagonal_scale * np.finfo(float).eps * 100
    scale = np.ones(6)
    scale[active] = diagonal[active] ** -.5
    return np.diag(1 / scale ** 2), scale
