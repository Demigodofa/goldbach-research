"""Test cross-divisor quasi-orthogonality in the active frequency band.

Owner: Kevin's Goldbach research.  Purpose: test the exact loss left after the
one-divisor geometric estimate in ``near_cutoff_geometric_bound.py``.  This is
finite evidence, not a uniform large-sieve theorem.

For squarefree V<a<=2V define, without the Mobius coefficient,

 u_(a,m,l)(h)=sum_(m*l<a*b<m*(l+1)) log(b)
                   [e_m(-h*a*b)+1/(m-1)], h in I_m.      (1)

Let w_m=(log m)^2(1-rho_m)/m and form the Hermitian Gram matrix

 G_(a,a')=sum_(M<m<=2M,m prime) w_m sum_(A<=l<2A)
              <u_(a,m,l),u_(a',m,l)>_(I_m).             (2)

The concrete quasi-orthogonality question is

 mu^T G mu <= C_epsilon*N^epsilon sum_a mu(a)^2 G_(a,a). (3)

Its left/right ratio is the Mobius Rayleigh quotient.  The largest eigenvalue
of diag(G)^(-1/2)Gdiag(G)^(-1/2) is the worst coefficient-uniform ratio.  A
Mobius quotient growing proportionally to the number of divisors falsifies
(3).  Passing this finite gate does not control l-lags or prove (3).
"""

import math

import numpy as np

from mobius_covariance_lag_probe import _mobius_values
from mobius_covariance_endpoint_probe import _prime_flags
from near_cutoff_geometric_bound import _active_modes


def _progression_vectors(modulus, shift_length, ell, divisors):
    """Return the exact vectors (1), one row per divisor."""
    modes = np.array(_active_modes(modulus, shift_length), dtype=np.int64)
    vectors = np.zeros((len(divisors), len(modes)), dtype=complex)
    for index, divisor in enumerate(divisors):
        if not 1 < divisor < modulus or math.gcd(divisor, modulus) != 1:
            raise ValueError("each divisor must lie in (1,m) and be coprime to m")
        first = modulus * ell // divisor + 1
        last = (modulus * (ell + 1) - 1) // divisor
        cofactors = np.arange(first, last + 1, dtype=np.int64)
        weights = np.log(cofactors)
        phases = np.exp(-2j * math.pi / modulus
                        * modes[:, None] * divisor * cofactors[None, :])
        vectors[index] = phases @ weights + np.sum(weights) / (modulus - 1)
    return modes, vectors


def finite_cross_divisor_gram(N=32000, cofactor_left=None,
                              divisor_left=None, modulus_limit=None):
    """Return (2)--(3) for one aligned block and one dyadic divisor band."""
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
    gram = np.zeros((len(divisors), len(divisors)), dtype=complex)

    for modulus in primes:
        modes = _active_modes(modulus, H)
        rho = len(modes) / (modulus - 1)
        weight = math.log(modulus) ** 2 / modulus * (1 - rho)
        for ell in range(cofactor_left, 2 * cofactor_left):
            _, vectors = _progression_vectors(modulus, H, ell, divisors)
            gram += weight * vectors @ np.conjugate(vectors.T)

    gram = (gram + np.conjugate(gram.T)) / 2
    diagonal = np.real(np.diag(gram))
    diagonal_energy = float(np.dot(coefficients ** 2, diagonal))
    mobius_energy = float(np.real(coefficients @ gram @ coefficients))
    normalized = (gram / np.sqrt(diagonal[:, None] * diagonal[None, :]))
    eigenvalues = np.linalg.eigvalsh(normalized)
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "cofactor_left": cofactor_left,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisors": divisors,
        "mobius_coefficients": tuple(int(value) for value in coefficients),
        "prime_count": len(primes),
        "diagonal_energy": diagonal_energy,
        "mobius_energy": mobius_energy,
        "mobius_rayleigh_ratio": mobius_energy / diagonal_energy,
        "mobius_off_diagonal_ratio": mobius_energy / diagonal_energy - 1,
        "uniform_largest_eigenvalue": float(eigenvalues[-1]),
        "uniform_smallest_eigenvalue": float(eigenvalues[0]),
        "divisor_quasi_orthogonality_proved": False,
    }


if __name__ == "__main__":
    for key, value in finite_cross_divisor_gram().items():
        print(f"{key}: {value}")
