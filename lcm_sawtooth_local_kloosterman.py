"""Local inverse-difference operators behind the source CRT phase.

For a prime ``r`` and nonzero local frequency ``a``, the matrix on
``F_r^*`` with entries ``1_(x!=y)e_r(a/(x-y))`` is a principal compression
of additive convolution on ``F_r``.  The full convolution eigenvalues are
ordinary Kloosterman sums and hence have magnitude at most ``2*sqrt(r)``.

Primary bound source: Topacogullari, arXiv:1506.02608v1, section 2, p. 4,
https://arxiv.org/pdf/1506.02608v1 (the prime-modulus specialization of the
displayed ordinary composite Kloosterman bound).
"""

import math

import numpy as np


def _local_inverse_difference_matrix(prime, frequency):
    residues = np.arange(1, prime, dtype=np.int64)
    differences = (residues[:, None] - residues[None, :]) % prime
    matrix = np.zeros((prime - 1, prime - 1), dtype=complex)
    off_diagonal = differences != 0
    inverses = np.asarray(tuple(
        pow(int(value), -1, prime)
        for value in differences[off_diagonal]), dtype=np.int64)
    matrix[off_diagonal] = np.exp(
        2j * np.pi * (frequency % prime) * inverses / prime)
    return matrix


def _full_convolution_eigenvalues(prime, frequency):
    values = []
    for dual_frequency in range(prime):
        values.append(sum(
            np.exp(2j * np.pi * (
                frequency * pow(difference, -1, prime)
                + dual_frequency * difference) / prime)
            for difference in range(1, prime)))
    return np.asarray(values, dtype=complex)


def local_kloosterman_receipt(
        primes=(5, 7, 11, 13), tolerance=1e-12):
    primes = tuple(primes)
    if (not primes or any(type(prime) is not int or prime < 3
                          for prime in primes)):
        raise ValueError("require odd primes")
    if any(any(prime % divisor == 0
               for divisor in range(2, math.isqrt(prime) + 1))
           for prime in primes):
        raise ValueError("every modulus must be prime")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    rows = {}
    all_pass = True
    for prime in primes:
        zero_matrix = _local_inverse_difference_matrix(prime, 0)
        zero_norm = float(np.linalg.svd(zero_matrix, compute_uv=False)[0])
        twisted_norms = []
        full_convolution_norms = []
        compression_excesses = []
        for frequency in range(1, prime):
            matrix = _local_inverse_difference_matrix(prime, frequency)
            local_norm = float(np.linalg.svd(matrix, compute_uv=False)[0])
            full_norm = float(np.max(np.abs(
                _full_convolution_eigenvalues(prime, frequency))))
            twisted_norms.append(local_norm)
            full_convolution_norms.append(full_norm)
            compression_excesses.append(local_norm - full_norm)
        weil_bound = 2 * math.sqrt(prime)
        row_pass = bool(
            abs(zero_norm - (prime - 2)) <= tolerance
            and max(compression_excesses) <= tolerance
            and max(full_convolution_norms) <= weil_bound + tolerance
            and max(twisted_norms) <= weil_bound + tolerance)
        all_pass = all_pass and row_pass
        rows[prime] = {
            "zero_frequency_operator_norm": zero_norm,
            "zero_frequency_reinforcing_eigenvalue": prime - 2,
            "minimum_nonzero_frequency_operator_norm": min(twisted_norms),
            "maximum_nonzero_frequency_operator_norm": max(twisted_norms),
            "maximum_full_convolution_kloosterman_norm": (
                max(full_convolution_norms)),
            "maximum_compression_excess": max(compression_excesses),
            "weil_bound": weil_bound,
            "maximum_twisted_to_zero_norm_ratio": (
                max(twisted_norms) / (prime - 2)),
            "all_nonzero_frequencies_have_one_norm": bool(
                max(twisted_norms) - min(twisted_norms) <= tolerance),
            "local_kloosterman_norm_gate_passes": row_pass,
        }
    return {
        "primes": primes,
        "rows": rows,
        "all_local_kloosterman_norm_gates_pass": bool(all_pass),
        "exact_crt_source_transfer_proved": False,
        "uniform_source_sum_estimate_proved": False,
        "prime_distribution_estimate_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(local_kloosterman_receipt())
