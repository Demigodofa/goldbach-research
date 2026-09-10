"""Prove the active/frame bound for any pair of complete near-cutoff rows.

Let the rows have indices l and l'.  For signed residue separation s=x-y,
the divisor progressions are compatible exactly when

 gcd(a,b) | s-m(l'-l).                                  (1)

The shifted triangular main is bounded by
``shifted_triangular_crt_main_bound.py``.  Its exact pair count differs from
the triangular density by at most one.  With

 L_a=log(ml/a), L'_b=log(ml'/b),

the log-weighted pair discrepancy for each compatible s is at most

 L_a L'_b +(m/lcm(a,b)+1)
   {L'_b/l+L_a/l'+1/(ll')}.                             (2)

The signed separations have multiplicity at most two modulo m, so the
Dirichlet L1 argument bounds (2) exactly as in the same-row theorem.

The cross-row centering identity is

 (1-rho){S_(a,l)conj(Q_(b,l'))/(m-1)
          +S_(b,l')Q_(a,l)/(m-1)
          +|I|S_(a,l)S_(b,l')/(m-1)^2}.                (3)

Distinct progression residues give the same L1 bounds for both Q terms.
Normalizing rows by their respective totient frames and applying rectangular
Schur proves a uniform operator estimate for every pair l,l' in the project
block.  This file does not yet perform the dyadic lag bookkeeping that sums
many such row pairs.
"""

import math

import numpy as np

from crt_pair_discrepancy_bound import dirichlet_residue_l1_bound
from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from mobius_cross_divisor_gram import _progression_vectors
from near_cutoff_geometric_bound import _active_modes
from triangular_crt_main_bound import _normalized_entry_bound


def _require_prime(modulus):
    flags = _prime_flags(modulus)
    if not flags[modulus]:
        raise ValueError("modulus must be prime")


def shifted_pair_error_bound(modulus, ell_left, ell_right, left, right):
    """Return the per-separation count/log error in (2)."""
    if any(type(value) is not int for value in (
            modulus, ell_left, ell_right, left, right)):
        raise ValueError("all arguments must be integers")
    if (ell_left < 1 or ell_right < 1
            or not 2 <= left < modulus or not 2 <= right < modulus):
        raise ValueError("invalid shifted pair ranges")
    _require_prime(modulus)
    left_log = math.log(modulus * ell_left / left)
    right_log = math.log(modulus * ell_right / right)
    common = math.lcm(left, right)
    return (left_log * right_log
            + (modulus / common + 1) * (
                right_log / ell_left
                + left_log / ell_right
                + 1 / (ell_left * ell_right)))


def _entry_majorants(modulus, rho, active_count, ell_left, ell_right,
                      left, right, left_log, right_log,
                      left_phi, right_phi, shift_length):
    common = math.lcm(left, right)
    pair_error = (left_log * right_log
                  + (modulus / common + 1) * (
                      right_log / ell_left
                      + left_log / ell_right
                      + 1 / (ell_left * ell_right)))
    kernel_l1 = dirichlet_residue_l1_bound(modulus)
    frame_scale = (rho * modulus ** 2 * left_log * right_log
                   * math.sqrt(left_phi * right_phi) / (left * right))
    discrepancy = ((1 - rho) * 2 * kernel_l1 * pair_error
                   / frame_scale)

    left_weight = left_log + 1 / ell_left
    right_weight = right_log + 1 / ell_right
    left_constant = ((modulus / left + 1) * left_weight
                     / (modulus - 1))
    right_constant = ((modulus / right + 1) * right_weight
                      / (modulus - 1))
    left_frequency_sum = kernel_l1 * left_weight
    right_frequency_sum = kernel_l1 * right_weight
    centering = ((1 - rho) * (
        left_constant * right_frequency_sum
        + right_constant * left_frequency_sum
        + active_count * left_constant * right_constant)
        / frame_scale)
    triangular = _normalized_entry_bound(
        modulus, shift_length, left, right)
    return triangular, discrepancy, centering


def row_shifted_active_frame_bound(modulus, shift_length, ell_left,
                                   ell_right, divisor_left,
                                   compare_exact=False):
    """Return a rigorous rectangular Schur bound for one pair of rows."""
    if any(type(value) is not int for value in (
            modulus, shift_length, ell_left, ell_right, divisor_left)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= divisor_left
            or 2 * divisor_left >= modulus
            or ell_left < 1 or ell_right < 1
            or modulus < 16 * math.pi * shift_length):
        raise ValueError(
            "require 2<=H<=U, 2U<m, positive rows, and m>=16*pi*H")
    _require_prime(modulus)
    modes = _active_modes(modulus, shift_length)
    if not modes:
        raise ValueError("the active frequency band must be nonempty")
    rho = len(modes) / (modulus - 1)
    mobius = _mobius_values(2 * divisor_left)
    divisors = tuple(a for a in range(divisor_left + 1, 2 * divisor_left + 1)
                     if mobius[a])
    left_logs = {a: math.log(modulus * ell_left / a) for a in divisors}
    right_logs = {a: math.log(modulus * ell_right / a) for a in divisors}
    totients = {a: _totient(a) for a in divisors}
    main = np.empty((len(divisors), len(divisors)))
    discrepancy = np.empty_like(main)
    centering = np.empty_like(main)
    for left_index, left in enumerate(divisors):
        for right_index, right in enumerate(divisors):
            values = _entry_majorants(
                modulus, rho, len(modes), ell_left, ell_right,
                left, right, left_logs[left], right_logs[right],
                totients[left], totients[right], shift_length)
            main[left_index, right_index] = values[0]
            discrepancy[left_index, right_index] = values[1]
            centering[left_index, right_index] = values[2]
    total = main + discrepancy + centering
    maximum_row = float(np.max(np.sum(total, axis=1)))
    maximum_column = float(np.max(np.sum(total, axis=0)))
    operator_bound = math.sqrt(maximum_row * maximum_column)
    result = {
        "modulus": modulus,
        "shift_length": shift_length,
        "rho": rho,
        "ell_left": ell_left,
        "ell_right": ell_right,
        "row_delta": ell_right - ell_left,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisor_count": len(divisors),
        "triangular_entry_schur_bound": float(max(
            np.max(np.sum(main, axis=1)),
            np.max(np.sum(main, axis=0)))),
        "discrepancy_entry_schur_bound": float(max(
            np.max(np.sum(discrepancy, axis=1)),
            np.max(np.sum(discrepancy, axis=0)))),
        "centering_entry_schur_bound": float(max(
            np.max(np.sum(centering, axis=1)),
            np.max(np.sum(centering, axis=0)))),
        "proved_shifted_active_frame_operator_bound": operator_bound,
        "shifted_pair_active_frame_theorem": True,
        "dyadic_lag_sum_proved": False,
        "signed_prime_correlation_proved": False,
    }
    if compare_exact:
        _, left_vectors = _progression_vectors(
            modulus, shift_length, ell_left, divisors)
        _, right_vectors = _progression_vectors(
            modulus, shift_length, ell_right, divisors)
        exact = ((1 - rho) * left_vectors
                 @ np.conjugate(right_vectors.T))
        divisor_array = np.array(divisors, dtype=float)
        phi_array = np.array([totients[a] for a in divisors], dtype=float)
        left_frame = (rho * modulus ** 2
                      * np.array([left_logs[a] for a in divisors]) ** 2
                      * phi_array / divisor_array ** 2)
        right_frame = (rho * modulus ** 2
                       * np.array([right_logs[a] for a in divisors]) ** 2
                       * phi_array / divisor_array ** 2)
        normalized = exact / np.sqrt(
            left_frame[:, None] * right_frame[None, :])
        exact_operator = float(np.linalg.svd(
            normalized, compute_uv=False)[0])
        result["exact_shifted_active_frame_operator_norm"] = exact_operator
        result["proved_over_exact"] = operator_bound / exact_operator
    return result


if __name__ == "__main__":
    for key, value in row_shifted_active_frame_bound(
            1009, 5, 9, 12, 8, compare_exact=True).items():
        print(f"{key}: {value}")
