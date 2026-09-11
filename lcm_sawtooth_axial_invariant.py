"""Express traceless axial distance by one determinant invariant.

Let ``K`` be a nonzero real symmetric traceless 3 by 3 matrix and set

    J(K) = 3*sqrt(6)*|det(K)| / ||K||_F^3.

Then ``0<=J<=1`` and the projective Frobenius distance from ``K`` to the axial
orbit ``alpha*(u u.T-I/3)`` is exactly

    sin((1/3)*acos(J(K))).

Indeed, after diagonalizing and writing ``r=||K||_F``, every traceless
eigenvalue triple has the form

    lambda_j = sqrt(2/3)*r*cos(theta+2*pi*j/3).

The product identity gives ``3*sqrt(6)*det(K)/r^3=cos(3*theta)``.  Projective
axial rays occur every ``pi/3`` in this eigenvalue circle.  If ``phi<=pi/6``
is the angle to the nearest ray, then ``J=cos(3*phi)`` and the projective
distance is ``sin(phi)``.

This elementary identity turns a spectral closeness statement into a scalar
determinant/norm inequality.  It does not itself bound the project matrices.
"""

import math

import numpy as np

from lcm_sawtooth_axial_schur_response import (
    project_axial_schur_response_receipt,
    projective_axial_distance,
)


def normalized_traceless_determinant(matrix):
    """Return ``J(K)`` for a nonzero real symmetric traceless matrix."""
    matrix = np.asarray(matrix, dtype=float)
    if matrix.shape != (3, 3):
        raise ValueError("matrix must be 3 by 3")
    norm = float(np.linalg.norm(matrix, "fro"))
    if not norm:
        raise ValueError("matrix must be nonzero")
    if not np.allclose(matrix, matrix.T, rtol=0, atol=norm * 1e-12):
        raise ValueError("matrix must be symmetric")
    matrix = (matrix + matrix.T) / 2
    if abs(float(np.trace(matrix))) > norm * 1e-10:
        raise ValueError("matrix must be traceless")
    invariant = (
        3 * math.sqrt(6) * abs(float(np.linalg.det(matrix))) / norm ** 3)
    if invariant > 1 + 1e-10:
        raise ArithmeticError("traceless determinant invariant exceeds one")
    return min(1.0, invariant)


def axial_distance_from_determinant(matrix):
    """Return the exact axial-distance formula and an independent check."""
    invariant = normalized_traceless_determinant(matrix)
    determinant_distance = math.sin(math.acos(invariant) / 3)
    spectral = projective_axial_distance(matrix)[
        "projective_axial_frobenius_distance"]
    return {
        "normalized_absolute_determinant": invariant,
        "determinant_axial_distance": determinant_distance,
        "spectral_axial_distance": spectral,
        "distance_identity_absolute_error": abs(
            determinant_distance - spectral),
        "traceless_axial_determinant_identity_proved": True,
    }


def project_axial_invariant_receipt(scale_modulus):
    response = project_axial_schur_response_receipt(scale_modulus)
    invariant = axial_distance_from_determinant(
        response["schur_response_tensor"])
    return {
        "scale_modulus": scale_modulus,
        "prime_count": response["prime_count"],
        **invariant,
        "uniform_determinant_lower_bound_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(project_axial_invariant_receipt(127))
