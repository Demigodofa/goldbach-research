"""Test an explicit centered degree basis for the active/full frame.

The six lifted coordinates are the symmetric square of three degree-labelled
parameters.  This module applies the fixed coefficient change induced by

    z = (L - mu) / s,

so that coefficients of ``a2*z^2 + a1*z + a0`` are written in the original
``(L^2,L,1)`` coefficient basis.  Its symmetric square gives a fully explicit
congruence on the six-coordinate Gram matrices.

For a project block, ``mu`` is the logarithmic midpoint
``log(sqrt(2)*M*ell_freeze)`` and ``s=log(2)/2`` maps the dyadic log interval
to a unit-scale interval.  The test asks whether diagonal scaling followed by
raw-coordinate Gershgorin can certify the candidate one-half lower frame in
this basis.  Failure rejects only this fixed basis certificate.
"""

import math

import numpy as np

from lcm_sawtooth_active_full_gershgorin import (
    coordinate_scaled_difference_gershgorin_receipt,
)
from lcm_sawtooth_lifted_endpoint_frame import (
    project_prime_block_lifted_endpoint_scan,
)


def centered_degree_parameter_transform(center, scale):
    """Map centered polynomial coefficients to the original degree basis."""
    if not (math.isfinite(center) and math.isfinite(scale)) or scale <= 0:
        raise ValueError("center must be finite and scale must be positive")
    inverse_scale = 1 / scale
    return np.array((
        (inverse_scale ** 2, 0.0, 0.0),
        (-2 * center * inverse_scale ** 2, inverse_scale, 0.0),
        (center ** 2 * inverse_scale ** 2,
         -center * inverse_scale, 1.0),
    ))


def _symmetric_pair_coordinates(left, right):
    return np.array((
        left[0] * right[0],
        left[0] * right[1] + left[1] * right[0],
        left[0] * right[2] + left[2] * right[0],
        left[1] * right[1],
        left[1] * right[2] + left[2] * right[1],
        left[2] * right[2],
    ))


def symmetric_square_transform(transform):
    """Return ``S`` satisfying ``lift(T*a)=S*lift(a)``."""
    transform = np.asarray(transform, dtype=float)
    if transform.shape != (3, 3):
        raise ValueError("transform must be a 3 by 3 matrix")
    pairs = ((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2))
    return np.vstack(tuple(
        _symmetric_pair_coordinates(transform[left], transform[right])
        for left, right in pairs))


def centered_basis_difference_gershgorin_receipt(
        active, full, center, scale, candidate=.5):
    """Apply the centered symmetric-square congruence and test Gershgorin."""
    transform = centered_degree_parameter_transform(center, scale)
    lifted_transform = symmetric_square_transform(transform)
    active = np.asarray(active, dtype=float)
    full = np.asarray(full, dtype=float)
    transformed_active = lifted_transform.T @ active @ lifted_transform
    transformed_full = lifted_transform.T @ full @ lifted_transform
    receipt = coordinate_scaled_difference_gershgorin_receipt(
        transformed_active, transformed_full, candidate=candidate)
    return {
        "center": center,
        "scale": scale,
        "degree_parameter_transform": tuple(
            tuple(float(value) for value in row) for row in transform),
        "symmetric_square_transform": tuple(
            tuple(float(value) for value in row)
            for row in lifted_transform),
        **receipt,
        "fixed_centered_basis_tested": True,
        "uniform_centered_basis_certificate_proved": False,
    }


def project_centered_basis_gershgorin_receipt(scale_modulus):
    """Test the logarithmic-midpoint basis on one complete prime block."""
    frame = project_prime_block_lifted_endpoint_scan(scale_modulus)
    center = math.log(
        math.sqrt(2) * scale_modulus * frame["ell_freeze"])
    scale = math.log(2) / 2
    centered = centered_basis_difference_gershgorin_receipt(
        frame["aggregate_active_window_residue_energy_gram"],
        frame["aggregate_full_residue_energy_gram"],
        center, scale)
    raw = coordinate_scaled_difference_gershgorin_receipt(
        frame["aggregate_active_window_residue_energy_gram"],
        frame["aggregate_full_residue_energy_gram"])
    return {
        "scale_modulus": scale_modulus,
        "prime_count": frame["prime_count"],
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        "exact_smallest_generalized_eigenvalue": frame[
            "aggregate_active_over_full_smallest_generalized_eigenvalue"],
        "raw_basis_gershgorin_lower_edge": raw[
            "scaled_difference_gershgorin_lower_edge"],
        **centered,
        "finite_complete_prime_block_measurement": True,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(project_centered_basis_gershgorin_receipt(127))
