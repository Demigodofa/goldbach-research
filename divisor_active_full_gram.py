"""Compare the divisor active Gram with its exact full-frequency collision Gram.

Owner: Kevin's Goldbach research.  Purpose: test an H^(-1) spectral estimate
on the restricted divisor-progression subspace.  This is an exact finite gate,
not a proved uniform matrix inequality.

Put H=floor(N^.1), M=floor(N^.59), V=floor(N^.15),
A0=ceil(N/(8M)), and let U=2^j V with H<=U and 2U<M.  For

 D_U={a in Z: U<a<=2U and mu(a)^2=1},

arbitrary complex coefficients (c_a)_(a in D_U), and
u_(a,m,l)(h) from ``mobius_cross_divisor_gram.py``, define

 A=sum_(M<m<=2M,m prime) (log m)^2/m*(1-rho_m)
     sum_(A0<=l<2A0) Gram_(h in I_m)(u_a,u_a'),          (1)

 P=sum_m (log m)^2/m*rho_m
     sum_l Gram_(1<=h<m)(u_a,u_a').                      (2)

The concrete matrix question is

 sum_(M<m<=2M, m prime) (log m)^2/m*(1-rho_m)
   sum_(A0<=l<2A0) sum_(h in I_m)
     |sum_(a in D_U)c_a*u_(a,m,l)(h)|^2
 <=C_epsilon*N^epsilon
 sum_(M<m<=2M, m prime) (log m)^2/m*rho_m
   sum_(A0<=l<2A0) sum_(1<=h<m)
     |sum_(a in D_U)c_a*u_(a,m,l)(h)|^2,                (3)

where I_m={1<=h<m:m/(2*pi*H)<min(h,m-h)<m/(pi*H)} and
rho_m=|I_m|/(m-1).  The constant is to be independent of N, j, and c.
We record the largest generalized eigenvalue, which chooses the worst
resonant c, and the fixed Mobius Rayleigh quotient c_a=mu(a).

The denominator has an exact arithmetic form.  If

 f_a(r)=1_(a|m*l+r) log((m*l+r)/a), 1<=r<m,
 S_a=sum_r f_a(r),

then u_a(h) is the nonzero Fourier transform of
f_a(r)-S_a/(m-1).  Parseval gives

 sum_(h=1)^(m-1)u_a(h)conj(u_a'(h))
 =m{sum_(m*l<n<m*(l+1),[a,a']|n)
       log(n/a)log(n/a')-S_a*S_a'/(m-1)}.                (4)

Thus P is computed from common multiples, without a numerical full-frequency
sum.  An eigenvalue growing like H or the divisor count falsifies this route.
"""

import math

import numpy as np

from mobius_covariance_lag_probe import _mobius_values
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_cross_divisor_gram import _progression_vectors
from near_cutoff_geometric_bound import _active_modes


def _full_collision_gram(modulus, ell, divisors):
    """Return the real Gram matrix in (3) by exact common-multiple ranges."""
    sums = np.zeros(len(divisors))
    for index, divisor in enumerate(divisors):
        first = modulus * ell // divisor + 1
        last = (modulus * (ell + 1) - 1) // divisor
        cofactors = np.arange(first, last + 1, dtype=np.int64)
        sums[index] = float(np.sum(np.log(cofactors)))

    gram = np.empty((len(divisors), len(divisors)))
    for left_index, left in enumerate(divisors):
        for right_index in range(left_index, len(divisors)):
            right = divisors[right_index]
            common = math.lcm(left, right)
            first = modulus * ell // common + 1
            last = (modulus * (ell + 1) - 1) // common
            multiples = common * np.arange(first, last + 1, dtype=np.int64)
            collision = float(np.sum(
                np.log(multiples / left) * np.log(multiples / right)))
            value = modulus * (
                collision - sums[left_index] * sums[right_index]
                / (modulus - 1))
            gram[left_index, right_index] = value
            gram[right_index, left_index] = value
    return gram


def _generalized_receipt(numerator, denominator, coefficients):
    """Return fixed-vector and extremal generalized Rayleigh quotients."""
    denominator_values, denominator_vectors = np.linalg.eigh(denominator)
    tolerance = max(1.0, denominator_values[-1]) * 1e-11
    if denominator_values[0] <= tolerance:
        raise ValueError("the full-frequency Gram is not numerically positive")
    inverse_root = ((denominator_vectors / np.sqrt(denominator_values))
                    @ np.conjugate(denominator_vectors.T))
    normalized = inverse_root @ numerator @ inverse_root
    normalized = (normalized + np.conjugate(normalized.T)) / 2
    eigenvalues = np.linalg.eigvalsh(normalized)
    fixed_numerator = float(np.real(
        coefficients @ numerator @ coefficients))
    fixed_denominator = float(np.real(
        coefficients @ denominator @ coefficients))
    return {
        "mobius_active_energy": fixed_numerator,
        "mobius_rho_full_energy": fixed_denominator,
        "mobius_active_over_rho_full": fixed_numerator / fixed_denominator,
        "uniform_largest_generalized_eigenvalue": float(eigenvalues[-1]),
        "uniform_smallest_generalized_eigenvalue": float(eigenvalues[0]),
        "denominator_condition_number": float(
            denominator_values[-1] / denominator_values[0]),
    }


def finite_active_full_comparison(N=32000, cofactor_left=None,
                                  divisor_left=None, modulus_limit=None):
    """Aggregate (1)--(3) and return the exact finite matrix comparison."""
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
    primes = tuple(prime for prime in range(M + 1, 2 * M + 1)
                   if flags[prime])
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
    active_gram = np.zeros((len(divisors), len(divisors)), dtype=complex)
    rho_full_gram = np.zeros((len(divisors), len(divisors)))

    for modulus in primes:
        rho = len(_active_modes(modulus, H)) / (modulus - 1)
        base_weight = math.log(modulus) ** 2 / modulus
        for ell in range(cofactor_left, 2 * cofactor_left):
            _, vectors = _progression_vectors(modulus, H, ell, divisors)
            active_gram += (base_weight * (1 - rho)
                            * vectors @ np.conjugate(vectors.T))
            rho_full_gram += (base_weight * rho
                              * _full_collision_gram(modulus, ell, divisors))

    active_gram = (active_gram + np.conjugate(active_gram.T)) / 2
    rho_full_gram = (rho_full_gram + rho_full_gram.T) / 2
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "cofactor_left": cofactor_left,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisors": divisors,
        "prime_count": len(primes),
        **_generalized_receipt(active_gram, rho_full_gram, coefficients),
        "active_full_matrix_bound_proved": False,
    }


def single_modulus_active_full_comparison(modulus, shift_length, ell_first,
                                          row_count, divisor_left):
    """Stress the same matrix inequality at larger H for one prime modulus."""
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
    active_gram = np.zeros((len(divisors), len(divisors)), dtype=complex)
    rho_full_gram = np.zeros((len(divisors), len(divisors)))
    rho = len(_active_modes(modulus, shift_length)) / (modulus - 1)
    for ell in range(ell_first, ell_first + row_count):
        _, vectors = _progression_vectors(
            modulus, shift_length, ell, divisors)
        active_gram += (1 - rho) * vectors @ np.conjugate(vectors.T)
        rho_full_gram += rho * _full_collision_gram(
            modulus, ell, divisors)
    active_gram = (active_gram + np.conjugate(active_gram.T)) / 2
    rho_full_gram = (rho_full_gram + rho_full_gram.T) / 2
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "rho": rho,
        "ell_first": ell_first,
        "row_count": row_count,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisor_count": len(divisors),
        **_generalized_receipt(active_gram, rho_full_gram, coefficients),
        "active_full_matrix_bound_proved": False,
    }


if __name__ == "__main__":
    for key, value in finite_active_full_comparison().items():
        print(f"{key}: {value}")
