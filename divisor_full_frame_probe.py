"""Compare the exact full divisor Gram with a positive gcd frame.

Freeze log(n/a) on the row m*l<n<m*(l+1) at L_a=log(m*l/a).
Uniform divisibility then has covariance

 (gcd(a,a')-1)/(a*a')
   =sum_(d>1,d|a,d|a') phi(d)/(a*a').                 (1)

For a,a' in the same open-closed dyadic band (U,2U], d=a can divide only
a'=a.  Hence the ideal row Gram

 P0_(a,a')=m^2 L_a L_a' (gcd(a,a')-1)/(a*a')          (2)

dominates the diagonal frame

 F_aa=m^2 L_a^2 phi(a)/a^2.                            (3)

This probe aggregates the exact rho_m*(log m)^2/m weights and measures the
normalized perturbation E=P-P0.  If lambda_min(F^-1/2 E F^-1/2)>-1, then the
finite exact implication P >= (1+lambda_min(E_norm))*F is rigorous.  Uniform
control of that perturbation would prove the missing lower frame bound.
"""

import math

import numpy as np

from divisor_active_full_gram import _full_collision_gram
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from near_cutoff_geometric_bound import _active_modes


def _totient(value):
    result, remaining, prime = value, value, 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            result -= result // prime
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        result -= result // remaining
    return result


def _frame_receipt(exact, ideal, frame):
    scale = np.sqrt(frame)
    normalized_ideal = ideal / (scale[:, None] * scale[None, :])
    normalized_error = (exact - ideal) / (scale[:, None] * scale[None, :])
    normalized_exact = exact / (scale[:, None] * scale[None, :])
    ideal_values = np.linalg.eigvalsh(normalized_ideal)
    error_values = np.linalg.eigvalsh(normalized_error)
    exact_values = np.linalg.eigvalsh(normalized_exact)
    error_norm = max(abs(error_values[0]), abs(error_values[-1]))
    return {
        "ideal_over_frame_eigenvalue_min": float(ideal_values[0]),
        "ideal_over_frame_eigenvalue_max": float(ideal_values[-1]),
        "error_over_frame_eigenvalue_min": float(error_values[0]),
        "error_over_frame_eigenvalue_max": float(error_values[-1]),
        "error_over_frame_operator_norm": float(error_norm),
        "proved_exact_over_frame_lower": float(1 + error_values[0]),
        "actual_exact_over_frame_eigenvalue_min": float(exact_values[0]),
        "actual_exact_over_frame_eigenvalue_max": float(exact_values[-1]),
        "finite_lower_frame_certificate_survives": bool(error_values[0] > -1),
    }


def finite_full_frame_probe(N=32000, cofactor_left=None, divisor_left=None,
                            modulus_limit=None):
    """Aggregate (1)--(3) over the exact prime and complete-row ranges."""
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
    totients = np.array([_totient(a) for a in divisors], dtype=float)
    divisor_array = np.array(divisors, dtype=float)
    gcd_kernel = np.empty((len(divisors), len(divisors)))
    for left_index, left in enumerate(divisors):
        for right_index, right in enumerate(divisors):
            gcd_kernel[left_index, right_index] = (
                (math.gcd(left, right) - 1) / (left * right))

    exact = np.zeros_like(gcd_kernel)
    ideal = np.zeros_like(gcd_kernel)
    frame = np.zeros(len(divisors))
    for modulus in primes:
        rho = len(_active_modes(modulus, H)) / (modulus - 1)
        weight = math.log(modulus) ** 2 / modulus * rho
        for ell in range(cofactor_left, 2 * cofactor_left):
            logs = np.log(modulus * ell / divisor_array)
            exact += weight * _full_collision_gram(
                modulus, ell, divisors)
            ideal += weight * modulus ** 2 * (
                logs[:, None] * logs[None, :] * gcd_kernel)
            frame += weight * modulus ** 2 * logs ** 2 * (
                totients / divisor_array ** 2)
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "cofactor_left": cofactor_left,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisor_count": len(divisors),
        "prime_count": len(primes),
        **_frame_receipt(exact, ideal, frame),
    }


def single_modulus_full_frame_probe(modulus, shift_length, ell_first,
                                     row_count, divisor_left):
    """Apply the same frame comparison without prime averaging."""
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
    divisor_array = np.array(divisors, dtype=float)
    totients = np.array([_totient(a) for a in divisors], dtype=float)
    gcd_kernel = np.array([
        [(math.gcd(a, b) - 1) / (a * b) for b in divisors]
        for a in divisors], dtype=float)
    exact = np.zeros_like(gcd_kernel)
    ideal = np.zeros_like(gcd_kernel)
    frame = np.zeros(len(divisors))
    for ell in range(ell_first, ell_first + row_count):
        logs = np.log(modulus * ell / divisor_array)
        exact += _full_collision_gram(modulus, ell, divisors)
        ideal += modulus ** 2 * logs[:, None] * logs[None, :] * gcd_kernel
        frame += modulus ** 2 * logs ** 2 * totients / divisor_array ** 2
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "ell_first": ell_first,
        "row_count": row_count,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisor_count": len(divisors),
        **_frame_receipt(exact, ideal, frame),
    }


if __name__ == "__main__":
    for key, value in finite_full_frame_probe().items():
        print(f"{key}: {value}")
