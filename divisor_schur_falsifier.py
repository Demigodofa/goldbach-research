"""Falsify a diagonal Schur/Gershgorin proof of the active/full inequality.

This probe uses the exact matrices from ``divisor_active_full_gram.py``.  If

    A <= C_eps N^eps P,

put D=diag(P), B=D^(-1/2) A D^(-1/2), and
Q=D^(-1/2) P D^(-1/2).  Schur and Gershgorin would give the explicit
certificate

    lambda_max(P^(-1/2) A P^(-1/2))
      <= max_i sum_j |B_ij|
         / min_i(1-sum_(j!=i)|Q_ij|),                  (1)

provided the denominator is positive.  A nonpositive denominator falsifies
this particular proof, though not the matrix inequality.  We also record the
valid hybrid bound max-row-sum(B)/lambda_min(Q), which shows the loss after
discarding numerator cancellation.
"""

import math

import numpy as np

from divisor_active_full_gram import (
    _full_collision_gram,
    _generalized_receipt,
)
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from mobius_cross_divisor_gram import _progression_vectors
from near_cutoff_geometric_bound import _active_modes


def _aggregate_matrices(N, cofactor_left=None, divisor_left=None,
                        modulus_limit=None):
    """Return the same exact A and P matrices as the active/full probe."""
    if type(N) is not int or N < 1024 or N % 32:
        raise ValueError("N must be an integer multiple of 32 and at least 1024")
    H, M, V = int(N ** .1), int(N ** .59), int(N ** .15)
    if cofactor_left is None:
        cofactor_left = (N + 8 * M - 1) // (8 * M)
    if divisor_left is None:
        divisor_left = V
    if (type(cofactor_left) is not int or cofactor_left < 2
            or type(divisor_left) is not int or divisor_left < H):
        raise ValueError("require integer cofactor_left>=2 and divisor_left>=H")
    if modulus_limit is not None and (
            type(modulus_limit) is not int or modulus_limit < 1):
        raise ValueError("modulus_limit must be a positive integer")

    flags = _prime_flags(2 * M)
    primes = tuple(m for m in range(M + 1, 2 * M + 1) if flags[m])
    if modulus_limit is not None:
        primes = primes[:modulus_limit]
    if not primes:
        raise ValueError("the prime companion range must be nonempty")
    if (8 * primes[0] * cofactor_left < N
            or 16 * primes[-1] * cofactor_left > 7 * N):
        raise ValueError("the aligned block leaves the central annulus")
    if 2 * divisor_left >= primes[0]:
        raise ValueError("the divisor band must lie below every modulus")

    mobius = _mobius_values(2 * divisor_left)
    divisors = tuple(a for a in range(divisor_left + 1, 2 * divisor_left + 1)
                     if mobius[a])
    coefficients = np.array([int(mobius[a]) for a in divisors], dtype=float)
    active = np.zeros((len(divisors), len(divisors)), dtype=complex)
    full = np.zeros((len(divisors), len(divisors)))
    for modulus in primes:
        rho = len(_active_modes(modulus, H)) / (modulus - 1)
        weight = math.log(modulus) ** 2 / modulus
        for ell in range(cofactor_left, 2 * cofactor_left):
            _, vectors = _progression_vectors(modulus, H, ell, divisors)
            active += weight * (1 - rho) * (
                vectors @ np.conjugate(vectors.T))
            full += weight * rho * _full_collision_gram(
                modulus, ell, divisors)
    active = (active + np.conjugate(active.T)) / 2
    full = (full + full.T) / 2
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "cofactor_left": cofactor_left,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisors": divisors,
        "prime_count": len(primes),
        "coefficients": coefficients,
        "active": active,
        "full": full,
    }


def _schur_receipt(active, full, coefficients):
    """Return the spectral data in (1) for two positive Gram matrices."""
    diagonal = np.real(np.diag(full))
    if np.any(diagonal <= 0):
        raise ValueError("full Gram diagonal must be positive")
    scale = np.sqrt(diagonal)
    normalized_active = active / (scale[:, None] * scale[None, :])
    normalized_full = full / (scale[:, None] * scale[None, :])
    active_row_sums = np.sum(np.abs(normalized_active), axis=1)
    full_off_diagonal = np.sum(np.abs(normalized_full), axis=1) - 1
    full_gershgorin_lower = float(np.min(1 - full_off_diagonal))
    full_exact_lower = float(np.linalg.eigvalsh(normalized_full)[0])
    active_schur_upper = float(np.max(active_row_sums))
    generalized = _generalized_receipt(active, full, coefficients)
    return {
        "active_schur_row_sum_max": active_schur_upper,
        "full_off_diagonal_row_sum_max": float(np.max(full_off_diagonal)),
        "full_gershgorin_lower": full_gershgorin_lower,
        "full_exact_normalized_eigenvalue_min": full_exact_lower,
        "gershgorin_certificate": (
            active_schur_upper / full_gershgorin_lower
            if full_gershgorin_lower > 0 else None),
        "schur_over_exact_full_bound": active_schur_upper / full_exact_lower,
        "actual_generalized_eigenvalue":
            generalized["uniform_largest_generalized_eigenvalue"],
        "diagonal_schur_gershgorin_proof_survives":
            full_gershgorin_lower > 0,
    }


def schur_falsifier(N=32000, cofactor_left=None, divisor_left=None,
                    modulus_limit=None):
    """Return the exact prime-averaged Schur/Gershgorin receipt."""
    data = _aggregate_matrices(
        N, cofactor_left, divisor_left, modulus_limit)
    active, full = data.pop("active"), data.pop("full")
    coefficients = data.pop("coefficients")
    return {**data, **_schur_receipt(active, full, coefficients)}


def single_modulus_schur_falsifier(modulus, shift_length, ell_first,
                                    row_count, divisor_left):
    """Stress (1) with no prime averaging, using consecutive complete rows."""
    if any(type(value) is not int for value in (
            modulus, shift_length, ell_first, row_count, divisor_left)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= divisor_left
            or 2 * divisor_left >= modulus
            or ell_first < 1 or row_count < 1):
        raise ValueError("invalid single-modulus ranges")
    flags = _prime_flags(modulus)
    if not flags[modulus]:
        raise ValueError("modulus must be prime")
    mobius = _mobius_values(2 * divisor_left)
    divisors = tuple(a for a in range(divisor_left + 1, 2 * divisor_left + 1)
                     if mobius[a])
    coefficients = np.array([int(mobius[a]) for a in divisors], dtype=float)
    active = np.zeros((len(divisors), len(divisors)), dtype=complex)
    full = np.zeros((len(divisors), len(divisors)))
    rho = len(_active_modes(modulus, shift_length)) / (modulus - 1)
    for ell in range(ell_first, ell_first + row_count):
        _, vectors = _progression_vectors(
            modulus, shift_length, ell, divisors)
        active += (1 - rho) * vectors @ np.conjugate(vectors.T)
        full += rho * _full_collision_gram(modulus, ell, divisors)
    active = (active + np.conjugate(active.T)) / 2
    full = (full + full.T) / 2
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "rho": rho,
        "ell_first": ell_first,
        "row_count": row_count,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisors": divisors,
        **_schur_receipt(active, full, coefficients),
    }


if __name__ == "__main__":
    for key, value in schur_falsifier().items():
        print(f"{key}: {value}")
