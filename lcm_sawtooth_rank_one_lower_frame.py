"""Compare the relaxed lifted lower-frame extremizer with rank-one lifts.

The six-coordinate relaxation identifies a vector

    y=(a^2,ab,ac,b^2,bc,c^2)

with a symmetric 3 by 3 matrix.  Actual polynomial lifts are its rank-one PSD
matrices ``lambda lambda^T``.  Since a quadratic quotient is unchanged by
``y -> -y``, projective proximity uses the best signed rank-one symmetric
matrix.

This module measures that proximity and minimizes the active/full quotient
directly on the rank-one surface.  The optimizer uses a deterministic
Fibonacci sphere followed by analytic projected-gradient refinement; its
output is finite numerical evidence, not a proof of the global minimum.
"""

import math

import numpy as np

from lcm_sawtooth_lifted_endpoint_frame import (
    _generalized_psd_receipt,
    lifted_endpoint_residue_gram_receipt,
)


def _rank_one_lifts(parameters):
    parameters = np.asarray(parameters, dtype=float)
    return np.column_stack((
        parameters[:, 0] ** 2,
        parameters[:, 0] * parameters[:, 1],
        parameters[:, 0] * parameters[:, 2],
        parameters[:, 1] ** 2,
        parameters[:, 1] * parameters[:, 2],
        parameters[:, 2] ** 2,
    ))


def _lifted_symmetric_matrix(vector):
    vector = np.asarray(vector, dtype=float)
    if vector.shape != (6,):
        raise ValueError("vector must have six coordinates")
    return np.array((
        (vector[0], vector[1], vector[2]),
        (vector[1], vector[3], vector[4]),
        (vector[2], vector[4], vector[5]),
    ))


def _projective_rank_one_distance(vector):
    """Return relative Frobenius distance to the best signed rank-one ray."""
    matrix = _lifted_symmetric_matrix(vector)
    eigenvalues = np.linalg.eigvalsh(matrix)
    squared = eigenvalues ** 2
    if not np.sum(squared):
        return 0.0, eigenvalues
    distance = math.sqrt(
        max(0.0, 1 - float(np.max(squared) / np.sum(squared))))
    return distance, eigenvalues


def _rank_one_quotient(parameter, numerator, denominator):
    lift = _rank_one_lifts(np.asarray(parameter)[None, :])[0]
    denominator_value = float(lift @ denominator @ lift)
    if denominator_value <= 0:
        return float("inf")
    return float(lift @ numerator @ lift) / denominator_value


def _rank_one_minimum(
        numerator, denominator, grid_size=100000,
        initial_parameters=()):
    """Deterministically scan and locally refine the rank-one quotient."""
    if type(grid_size) is not int or grid_size < 100:
        raise ValueError("grid_size must be an integer at least 100")
    indices = np.arange(grid_size)
    third = 1 - 2 * (indices + .5) / grid_size
    angle = math.pi * (3 - math.sqrt(5)) * indices
    radius = np.sqrt(1 - third ** 2)
    parameters = np.column_stack((
        radius * np.cos(angle), radius * np.sin(angle), third))
    lifts = _rank_one_lifts(parameters)
    numerators = np.einsum(
        "ni,ij,nj->n", lifts, numerator, lifts)
    denominators = np.einsum(
        "ni,ij,nj->n", lifts, denominator, lifts)
    scale = max(float(np.max(denominators)), 1.0)
    valid = denominators > scale * np.finfo(float).eps * 100
    quotients = np.full(grid_size, float("inf"))
    quotients[valid] = numerators[valid] / denominators[valid]
    seed_indices = np.argsort(quotients)[:20]
    seeds = [parameters[index].copy() for index in seed_indices]
    for initial in initial_parameters:
        initial = np.asarray(initial, dtype=float)
        if initial.shape != (3,) or not np.linalg.norm(initial):
            raise ValueError("each initial parameter must be a nonzero 3-vector")
        seeds.append(initial / np.linalg.norm(initial))
    best_value = float(quotients[seed_indices[0]])
    best_parameter = parameters[seed_indices[0]].copy()

    for seed in seeds:
        parameter = seed.copy()
        value = _rank_one_quotient(parameter, numerator, denominator)
        step = .2
        for _ in range(500):
            first, second, third = parameter
            lift = _rank_one_lifts(parameter[None, :])[0]
            numerator_value = float(lift @ numerator @ lift)
            denominator_value = float(lift @ denominator @ lift)
            lift_gradient = 2 * (
                (numerator @ lift) * denominator_value
                - (denominator @ lift) * numerator_value
            ) / denominator_value ** 2
            jacobian = np.array((
                (2 * first, 0, 0),
                (second, first, 0),
                (third, 0, first),
                (0, 2 * second, 0),
                (0, third, second),
                (0, 0, 2 * third),
            ))
            gradient = jacobian.T @ lift_gradient
            gradient -= parameter * float(parameter @ gradient)
            gradient_norm = float(np.linalg.norm(gradient))
            if gradient_norm < 1e-12:
                break
            local_step = step
            accepted = False
            for _ in range(30):
                candidate = parameter - local_step * gradient / gradient_norm
                candidate /= np.linalg.norm(candidate)
                candidate_value = _rank_one_quotient(
                    candidate, numerator, denominator)
                if candidate_value < value:
                    parameter = candidate
                    value = candidate_value
                    step = min(local_step * 1.4, .5)
                    accepted = True
                    break
                local_step *= .5
            if not accepted:
                break
        if value < best_value:
            best_value = value
            best_parameter = parameter.copy()
    return {
        "grid_minimum": float(np.min(quotients)),
        "refined_minimum": best_value,
        "minimizing_parameter": tuple(
            float(value) for value in best_parameter),
        "grid_size": grid_size,
        "seed_count": len(seeds),
    }


def rank_one_lower_frame_receipt(
        modulus, row_count, ell_freeze, divisor_lower, divisor_upper,
        grid_size=100000):
    base = lifted_endpoint_residue_gram_receipt(
        modulus, row_count, ell_freeze, divisor_lower, divisor_upper)
    active = np.asarray(base["active_window_residue_energy_gram"])
    full = np.asarray(base["full_residue_energy_gram"])
    relaxed = _generalized_psd_receipt(active, full)
    relaxed_vector = relaxed["smallest_generalized_eigenvector"]
    if relaxed_vector is None:
        raise ArithmeticError("full residue form has no positive direction")
    distance, matrix_eigenvalues = _projective_rank_one_distance(
        relaxed_vector)
    _, matrix_eigenvectors = np.linalg.eigh(
        _lifted_symmetric_matrix(relaxed_vector))
    dominant_parameter = matrix_eigenvectors[
        :, int(np.argmax(np.abs(matrix_eigenvalues)))]
    rank_one = _rank_one_minimum(
        active, full, grid_size=grid_size,
        initial_parameters=(dominant_parameter,))
    return {
        "modulus": modulus,
        "row_count": row_count,
        "ell_freeze": ell_freeze,
        "divisor_range": (divisor_lower, divisor_upper),
        "relaxed_minimum": relaxed["smallest_generalized_eigenvalue"],
        "relaxed_minimizer": relaxed_vector,
        "relaxed_matrix_eigenvalues": tuple(
            float(value) for value in matrix_eigenvalues),
        "projective_rank_one_frobenius_distance": distance,
        "actual_selector_active_over_full": base[
            "actual_active_window_over_full_residue_energy"],
        **rank_one,
        "rank_one_over_relaxed_minimum": (
            rank_one["refined_minimum"]
            / relaxed["smallest_generalized_eigenvalue"]),
        "rank_one_global_minimum_proved": False,
        "uniform_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(rank_one_lower_frame_receipt(151, 28, 42, 3, 13))
