"""Test an exact dyadic-lag sublemma for the aligned Mobius covariance.

Owner: Kevin's Goldbach research.  Purpose: turn the broad-lag observation
into one quantified arithmetic question.  This is a finite d=1 diagnostic at
tiny H,V, not an asymptotic estimate.

Put H=floor(N^.1), M=floor(N^.59), V=floor(N^.15), and fix an integer A with
J_m=(m*A,2*m*A] inside [N/8,7*N/8] for every prime M<m<=2M.  For A<=l<2A,
1<=r<m, define

 c_(m,l)(r)=sum_(a|m*l+r, a>V) mu(a) log((m*l+r)/a),
 Phi_(m,l)(h)=sum_(r=1)^(m-1)c_(m,l)(r)
                 [e_m(-h*r)+1/(m-1)],                    (1)
 E_(m,l)=sum_(h=1)^(m-1)|Phi_(m,l)(h)|^2.                (2)

Let I_m={1<=h<m: m/(2*pi*H)<min(h,m-h)<m/(pi*H)},
R_m=|I_m| and rho_m=R_m/(m-1).  For a dyadic lag block

 D_j={Delta: 2^j<=Delta<min(2^(j+1),A)},                 (3)

put

 C_j=sum_(M<m<=2M, m prime) (log m)^2/m * 2 Re
       sum_(Delta in D_j) sum_(A<=l<2A-Delta)
       {sum_(h in I_m) Phi_(m,l)(h) conj(Phi_(m,l+Delta)(h))
        -rho_m sum_(h=1)^(m-1)
              Phi_(m,l)(h) conj(Phi_(m,l+Delta)(h))},    (4)

 P_j=sum_m (log m)^2/m * rho_m * 2
       sum_(Delta in D_j) sum_l sqrt(E_(m,l)E_(m,l+Delta)). (5)

The concrete proposed sublemma is: for every epsilon>0, uniformly in j and
admissible A,

                  max(C_j,0) <= C_epsilon*N^epsilon*P_j. (6)

The right side is the H^-1-scale share of the coefficient-blind Cauchy
baseline.  Summing (6) costs only O(log A), but the same-row term and d>1
transfer remain separate obligations.  Resonant arbitrary row coefficients
make C_j/P_j about 1/rho_m, so (6) can only be true by using the fixed
Mobius--log arithmetic.
"""

import math

import numpy as np

from mobius_covariance_endpoint_probe import _actual_tail, _prime_flags


def finite_dyadic_lag_gate(N=32000, cofactor_left=None):
    """Return the exact finite C_j/P_j receipts for (3)--(6)."""
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

    starts = []
    start = 1
    while start < cofactor_left:
        starts.append(start)
        start *= 2
    covariance = np.zeros(len(starts))
    principal_cauchy = np.zeros(len(starts))
    positive_modulus_covariance = np.zeros(len(starts))
    absolute_modulus_covariance = np.zeros(len(starts))
    positive_modulus_count = np.zeros(len(starts), dtype=int)
    tail = _actual_tail(N, V, 0, N)
    prime_count = 0

    for prime in primes:
        prime_count += 1
        modes = np.array([
            h for h in range(1, prime)
            if prime / (2 * math.pi * H) < min(h, prime - h)
            < prime / (math.pi * H)
        ], dtype=int)
        rho = len(modes) / (prime - 1)
        rows = np.zeros((cofactor_left, prime))
        for index, ell in enumerate(range(cofactor_left, 2 * cofactor_left)):
            rows[index, 1:] = tail[prime * ell + 1:prime * (ell + 1)]
        transforms = np.fft.fft(rows, axis=1)
        centered = transforms + rows.sum(axis=1)[:, None] / (prime - 1)
        energies = np.sum(np.abs(centered[:, 1:]) ** 2, axis=1)
        weight = math.log(prime) ** 2 / prime

        for block_index, block_start in enumerate(starts):
            block_stop = min(2 * block_start, cofactor_left)
            local_covariance = 0.0
            local_cauchy = 0.0
            for delta in range(block_start, block_stop):
                left = centered[:cofactor_left - delta]
                right = centered[delta:]
                band_cross = float(np.real(np.sum(
                    left[:, modes] * np.conjugate(right[:, modes]))))
                full_cross = float(np.real(np.sum(
                    left[:, 1:] * np.conjugate(right[:, 1:]))))
                local_covariance += 2 * (band_cross - rho * full_cross)
                local_cauchy += 2 * float(np.sum(np.sqrt(
                    energies[:cofactor_left - delta] * energies[delta:])))
            covariance[block_index] += weight * local_covariance
            principal_cauchy[block_index] += weight * rho * local_cauchy
            positive_modulus_covariance[block_index] += (
                weight * max(local_covariance, 0.0))
            absolute_modulus_covariance[block_index] += (
                weight * abs(local_covariance))
            positive_modulus_count[block_index] += local_covariance > 0

    blocks = []
    for index, block_start in enumerate(starts):
        block_stop = min(2 * block_start, cofactor_left)
        ratio = covariance[index] / principal_cauchy[index]
        absolute_mass = absolute_modulus_covariance[index]
        blocks.append({
            "lag_first": block_start,
            "lag_last": block_stop - 1,
            "covariance": float(covariance[index]),
            "principal_cauchy_budget": float(principal_cauchy[index]),
            "signed_ratio": float(ratio),
            "positive_ratio": float(max(ratio, 0.0)),
            "positive_modulus_count": int(positive_modulus_count[index]),
            "positive_modulus_ratio": float(
                positive_modulus_covariance[index]
                / principal_cauchy[index]),
            "absolute_modulus_ratio": float(
                absolute_mass / principal_cauchy[index]),
            "aggregate_to_absolute_fraction": float(
                abs(covariance[index]) / absolute_mass
                if absolute_mass else 0.0),
        })
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "cofactor_left": cofactor_left,
        "prime_count": prime_count,
        "blocks": tuple(blocks),
        "maximum_positive_ratio": max(block["positive_ratio"]
                                      for block in blocks),
        "dyadic_h_inverse_sublemma_proved": False,
    }


if __name__ == "__main__":
    for key, value in finite_dyadic_lag_gate().items():
        print(f"{key}: {value}")
