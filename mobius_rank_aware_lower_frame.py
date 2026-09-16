"""Rank-aware active/full lower-frame diagnostics.

The Mobius active/full target naturally compares two positive-semidefinite
quadratic forms

    A = active-window energy,    F = full-period energy.

When ``F`` is singular, full-Gram whitening is the wrong theorem shape.  The
correct finite linear-algebra question is whether ``A >= c*F`` on the quotient
by the nullspace of ``F`` after allowing harmless movement in that nullspace.

This module records that quotient calculation.  It proves no uniform Mobius
estimate; it makes the finite theorem obligation explicit and testable.
"""

import numpy as np


def _symmetric(matrix):
    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be square")
    return (matrix + matrix.T) / 2


def rank_aware_lower_frame_receipt(active, full, target=.5):
    """Return the quotient lower-frame data for ``active >= target*full``.

    The computation first diagonally equilibrates the full form where its
    diagonal is positive, then diagonalizes the equilibrated full matrix.
    On the positive eigenspace it computes two quantities:

    * the raw positive-range minimum, with null coordinates frozen at zero;
    * the Schur-minimized quotient minimum, after optimizing harmless full-null
      coordinates against the active form.

    A positive active direction inside the full nullspace is harmless for the
    inequality itself but changes the minimizing quotient.  A coupling to an
    active-null direction would be an obstruction; for a true PSD active form
    it should be zero up to numerical tolerance.
    """
    active = _symmetric(active)
    full = _symmetric(full)
    if active.shape != full.shape:
        raise ValueError("active and full must have the same shape")
    if target < 0:
        raise ValueError("target must be nonnegative")

    diagonal = np.diag(full)
    diagonal_scale = max(float(np.max(diagonal)), 1.0)
    active_diagonal = diagonal > (
        diagonal_scale * np.finfo(float).eps * 100)
    coordinate_scale = np.ones(len(diagonal))
    coordinate_scale[active_diagonal] = (
        diagonal[active_diagonal] ** -.5)
    scaling = np.outer(coordinate_scale, coordinate_scale)
    active = active * scaling
    full = full * scaling

    full_values, full_vectors = np.linalg.eigh(full)
    full_scale = max(float(full_values[-1]), 1.0)
    tolerance = full_scale * np.finfo(float).eps * 1000
    positive = full_values > tolerance
    rank = int(np.count_nonzero(positive))
    nullity = int(len(full_values) - rank)
    active_scale = max(float(np.linalg.eigvalsh(active)[-1]), 1.0)
    active_tolerance = active_scale * np.finfo(float).eps * 10000

    if rank == 0:
        null_active = active
        null_values = np.linalg.eigvalsh(null_active)
        null_maximum = float(null_values[-1]) if len(null_values) else 0.0
        return {
            "dimension": active.shape[0],
            "target_lower_frame_constant": target,
            "full_rank": rank,
            "full_nullity": nullity,
            "positive_range_nonvacuous": False,
            "raw_positive_range_minimum": float("inf"),
            "schur_minimized_positive_range_minimum": float("inf"),
            "full_null_active_minimum": float(null_values[0]),
            "full_null_active_maximum": null_maximum,
            "active_positive_full_null_direction": bool(
                null_maximum > active_tolerance),
            "null_coupling_to_active_null_norm": 0.0,
            "quotient_minimum_exceeds_target": False,
            "one_half_lower_frame_certified_with_null_coupling_tolerance": (
                False),
            "rank_aware_quotient_checked": True,
            "uniform_active_full_lower_frame_proved": False,
        }

    positive_vectors = full_vectors[:, positive]
    null_vectors = full_vectors[:, ~positive]
    active_pp = positive_vectors.T @ active @ positive_vectors
    denominator_root = np.diag(full_values[positive] ** -.5)
    raw_whitened = denominator_root @ active_pp @ denominator_root
    raw_values = np.linalg.eigvalsh((raw_whitened + raw_whitened.T) / 2)

    if nullity:
        active_nn = null_vectors.T @ active @ null_vectors
        active_pn = positive_vectors.T @ active @ null_vectors
        null_values, null_basis = np.linalg.eigh(
            (active_nn + active_nn.T) / 2)
        null_positive = null_values > active_tolerance
        null_zero = ~null_positive
        if np.any(null_positive):
            null_inverse = (
                (null_basis[:, null_positive]
                 / null_values[null_positive])
                @ null_basis[:, null_positive].T)
        else:
            null_inverse = np.zeros_like(active_nn)
        if np.any(null_zero):
            null_coupling = float(np.linalg.norm(
                active_pn @ null_basis[:, null_zero], ord=2))
        else:
            null_coupling = 0.0
        schur = active_pp - active_pn @ null_inverse @ active_pn.T
        null_minimum = float(null_values[0])
        null_maximum = float(null_values[-1])
    else:
        schur = active_pp
        null_coupling = 0.0
        null_minimum = 0.0
        null_maximum = 0.0

    schur_whitened = denominator_root @ schur @ denominator_root
    schur_values = np.linalg.eigvalsh(
        (schur_whitened + schur_whitened.T) / 2)
    quotient_minimum = float(max(schur_values[0], 0.0))
    certified = (
        quotient_minimum >= target
        and null_coupling <= active_tolerance * 100)

    return {
        "dimension": active.shape[0],
        "target_lower_frame_constant": target,
        "full_rank": rank,
        "full_nullity": nullity,
        "positive_range_nonvacuous": True,
        "raw_positive_range_minimum": float(max(raw_values[0], 0.0)),
        "schur_minimized_positive_range_minimum": quotient_minimum,
        "full_null_active_minimum": null_minimum,
        "full_null_active_maximum": null_maximum,
        "active_positive_full_null_direction": bool(
            null_maximum > active_tolerance),
        "null_coupling_to_active_null_norm": null_coupling,
        "quotient_minimum_exceeds_target": bool(
            quotient_minimum >= target),
        "one_half_lower_frame_certified_with_null_coupling_tolerance": bool(
            certified),
        "rank_aware_quotient_checked": True,
        "uniform_active_full_lower_frame_proved": False,
    }
