"""Split the remaining active-band lag covariance by Mobius divisor scale.

Owner: Kevin's Goldbach research.  Purpose: test whether the small active term
isolated by ``mobius_lag_spectral_probe.py`` has a separately controllable
factor diagonal or only becomes small after cross-band cancellation.  This is
an exact finite d=1 decomposition at tiny H,V, not an asymptotic estimate.

Partition V<a<=N into dyadic bands A_i=(U_i,2U_i] (with the last endpoint
truncated at N), and put

 c_i(n)=sum_(a|n, U_i<a<=min(2U_i,N)) mu(a)log(n/a).       (1)

Then c(n)=sum_i c_i(n) is exactly the Mobius tail.  Form Phi^i_(m,l)(h) from
c_i(m*l+r) by the same centered residue transform as before.  For a dyadic
lag block D_j, define the active factor matrix

 X_(j,i,k)=sum_(M<m<=2M, m prime) (log m)^2/m*(1-rho_m)*2 Re
   sum_(Delta in D_j) sum_(A<=l<2A-Delta) sum_(h in I_m)
   Phi^i_(m,l)(h) conjugate(Phi^k_(m,l+Delta)(h)).        (2)

The ordered matrix sum is the exact active term D_j.  Its diagonal is
sum_i X_(j,i,i); the remaining ordered entries are the cross-band term.  A
positive diagonal comparable to the H^-1 Cauchy budget P_j falsifies the
proposed route of paying the factor diagonal before estimating interactions.
"""

import math

import numpy as np

from mobius_covariance_lag_probe import _mobius_values
from mobius_covariance_endpoint_probe import _prime_flags


def _dyadic_mobius_tails(N, cutoff):
    """Return ((left,right),...) and exact c_i(n) arrays from (1)."""
    bands = []
    left = cutoff
    while left < N:
        right = min(2 * left, N)
        bands.append((left, right))
        left = right
    mobius = _mobius_values(N)
    tails = np.zeros((len(bands), N + 1))
    for band_index, (left, right) in enumerate(bands):
        for divisor in range(left + 1, right + 1):
            coefficient = int(mobius[divisor])
            if coefficient == 0:
                continue
            cofactors = np.arange(1, N // divisor + 1, dtype=np.int64)
            tails[band_index, divisor * cofactors] += (
                coefficient * np.log(cofactors))
    return tuple(bands), tails


def finite_active_factor_probe(N=32000, cofactor_left=None):
    """Return the exact factor diagonal/cross split of every active D_j."""
    if type(N) is not int or N < 1024 or N % 32:
        raise ValueError("N must be an integer multiple of 32 and at least 1024")
    H, M, V = int(N ** .1), int(N ** .59), int(N ** .15)
    if cofactor_left is None:
        cofactor_left = (N + 8 * M - 1) // (8 * M)
    if type(cofactor_left) is not int or cofactor_left < 2:
        raise ValueError("cofactor_left must be an integer at least two")
    flags = _prime_flags(2 * M)
    primes = tuple(prime for prime in range(M + 1, 2 * M + 1)
                   if flags[prime])
    if not primes:
        raise ValueError("the prime companion range must be nonempty")
    if (8 * primes[0] * cofactor_left < N
            or 16 * primes[-1] * cofactor_left > 7 * N):
        raise ValueError("the aligned block leaves the central annulus")

    bands, tails = _dyadic_mobius_tails(N, V)
    starts = []
    start = 1
    while start < cofactor_left:
        starts.append(start)
        start *= 2
    diagonal_totals = np.zeros((len(starts), len(bands)))
    active_totals = np.zeros(len(starts))
    principal_cauchy = np.zeros(len(starts))

    for prime in primes:
        modes = np.array([
            h for h in range(1, prime)
            if prime / (2 * math.pi * H) < min(h, prime - h)
            < prime / (math.pi * H)
        ], dtype=int)
        rho = len(modes) / (prime - 1)
        rows = np.zeros((len(bands), cofactor_left, prime))
        for row_index, ell in enumerate(
                range(cofactor_left, 2 * cofactor_left)):
            rows[:, row_index, 1:] = tails[
                :, prime * ell + 1:prime * (ell + 1)]
        transforms = np.fft.fft(rows, axis=2)
        centered = transforms + rows.sum(axis=2)[:, :, None] / (prime - 1)
        active = centered[:, :, modes]
        total_active = np.sum(active, axis=0)
        total_values = np.sum(centered[:, :, 1:], axis=0)
        energies = np.sum(np.abs(total_values) ** 2, axis=1)
        weight = math.log(prime) ** 2 / prime

        for block_index, block_start in enumerate(starts):
            block_stop = min(2 * block_start, cofactor_left)
            local_diagonal = np.zeros(len(bands))
            local_total = 0.0
            local_cauchy = 0.0
            for delta in range(block_start, block_stop):
                left, right = active[:, :-delta, :], active[:, delta:, :]
                local_diagonal += 2 * np.real(np.sum(
                    left * np.conjugate(right), axis=(1, 2)))
                local_total += 2 * float(np.real(np.sum(
                    total_active[:-delta]
                    * np.conjugate(total_active[delta:]))))
                local_cauchy += 2 * float(np.sum(np.sqrt(
                    energies[:-delta] * energies[delta:])))
            diagonal_totals[block_index] += (
                weight * (1 - rho) * local_diagonal)
            active_totals[block_index] += weight * (1 - rho) * local_total
            principal_cauchy[block_index] += weight * rho * local_cauchy

    blocks = []
    for block_index, block_start in enumerate(starts):
        budget = principal_cauchy[block_index]
        diagonal_entries = diagonal_totals[block_index] / budget
        total = float(active_totals[block_index] / budget)
        diagonal = float(np.sum(diagonal_entries))
        blocks.append({
            "lag_first": block_start,
            "lag_last": min(2 * block_start, cofactor_left) - 1,
            "active_band_ratio": total,
            "factor_diagonal_ratio": diagonal,
            "factor_cross_ratio": total - diagonal,
            "positive_diagonal_mass_ratio": float(np.sum(
                np.maximum(diagonal_entries, 0))),
            "negative_diagonal_mass_ratio": float(-np.sum(
                np.minimum(diagonal_entries, 0))),
            "diagonal_band_ratios": tuple(float(value)
                                          for value in diagonal_entries),
        })
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "cofactor_left": cofactor_left,
        "prime_count": len(primes),
        "factor_bands": bands,
        "blocks": tuple(blocks),
        "factor_diagonal_bound_proved": False,
    }


if __name__ == "__main__":
    for key, value in finite_active_factor_probe().items():
        print(f"{key}: {value}")
