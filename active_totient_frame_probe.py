"""Test the active divisor Gram against the proven positive totient frame.

For a complete row and D_U={U<a<=2U:mu(a)^2=1}, put

 F_(a,m,l)=m^2 log(ml/a)^2 phi(a)/a^2.

The full-frequency denominator satisfies G_full >= (1-o(1))F in the
near-cutoff band by ``near_cutoff_full_frame_bound.py``.  Thus a sufficient
same-row numerator estimate is, for arbitrary complex c_a,

 sum_(m,l) (log m)^2/m*(1-rho_m)
   sum_(h in I_m)|sum_a c_a u_(a,m,l)(h)|^2
 <=C_eps N^eps sum_(m,l) (log m)^2/m*rho_m
   sum_a |c_a|^2 F_(a,m,l).                              (1)

This exact finite probe records the largest generalized eigenvalue, the
absolute Schur row sum, and the fixed Mobius quotient.  Growth proportional
to |D_U| falsifies the coefficient-uniform route.  Passing finite cases does
not prove (1) or handle shifted rows.
"""

import math

import numpy as np

from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from mobius_cross_divisor_gram import _progression_vectors
from near_cutoff_geometric_bound import _active_modes


def _active_frame_receipt(active, frame, coefficients):
    scale = np.sqrt(frame)
    normalized = active / (scale[:, None] * scale[None, :])
    normalized = (normalized + np.conjugate(normalized.T)) / 2
    eigenvalues = np.linalg.eigvalsh(normalized)
    row_sums = np.sum(np.abs(normalized), axis=1)
    diagonal = np.real(np.diag(normalized))
    fixed_numerator = float(np.real(coefficients @ active @ coefficients))
    fixed_denominator = float(np.dot(coefficients ** 2, frame))
    return {
        "mobius_active_over_frame": fixed_numerator / fixed_denominator,
        "largest_active_over_frame_eigenvalue": float(eigenvalues[-1]),
        "smallest_active_over_frame_eigenvalue": float(eigenvalues[0]),
        "active_frame_schur_row_sum_max": float(np.max(row_sums)),
        "active_frame_diagonal_max": float(np.max(diagonal)),
        "active_frame_off_diagonal_row_sum_max": float(
            np.max(row_sums - diagonal)),
        "schur_over_actual_eigenvalue": float(
            np.max(row_sums) / eigenvalues[-1]),
        "active_totient_frame_bound_proved": False,
    }


def finite_active_totient_frame(N=32000, cofactor_left=None,
                                divisor_left=None, modulus_limit=None):
    """Aggregate the two sides of (1) over exact project ranges."""
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
    divisor_array = np.array(divisors, dtype=float)
    totients = np.array([_totient(a) for a in divisors], dtype=float)
    active = np.zeros((len(divisors), len(divisors)), dtype=complex)
    frame = np.zeros(len(divisors))
    for modulus in primes:
        rho = len(_active_modes(modulus, H)) / (modulus - 1)
        weight = math.log(modulus) ** 2 / modulus
        for ell in range(cofactor_left, 2 * cofactor_left):
            _, vectors = _progression_vectors(modulus, H, ell, divisors)
            active += weight * (1 - rho) * (
                vectors @ np.conjugate(vectors.T))
            logs = np.log(modulus * ell / divisor_array)
            frame += weight * rho * modulus ** 2 * logs ** 2 * (
                totients / divisor_array ** 2)
    active = (active + np.conjugate(active.T)) / 2
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "cofactor_left": cofactor_left,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisors": divisors,
        "prime_count": len(primes),
        **_active_frame_receipt(active, frame, coefficients),
    }


def single_modulus_active_totient_frame(modulus, shift_length, ell_first,
                                         row_count, divisor_left):
    """Stress (1) without prime averaging on consecutive complete rows."""
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
    divisor_array = np.array(divisors, dtype=float)
    totients = np.array([_totient(a) for a in divisors], dtype=float)
    active = np.zeros((len(divisors), len(divisors)), dtype=complex)
    frame = np.zeros(len(divisors))
    rho = len(_active_modes(modulus, shift_length)) / (modulus - 1)
    for ell in range(ell_first, ell_first + row_count):
        _, vectors = _progression_vectors(
            modulus, shift_length, ell, divisors)
        active += (1 - rho) * vectors @ np.conjugate(vectors.T)
        logs = np.log(modulus * ell / divisor_array)
        frame += rho * modulus ** 2 * logs ** 2 * (
            totients / divisor_array ** 2)
    active = (active + np.conjugate(active.T)) / 2
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "rho": rho,
        "ell_first": ell_first,
        "row_count": row_count,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisors": divisors,
        **_active_frame_receipt(active, frame, coefficients),
    }


if __name__ == "__main__":
    for key, value in finite_active_totient_frame().items():
        print(f"{key}: {value}")
