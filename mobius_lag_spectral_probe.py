"""Diagonalize the aligned dyadic-lag covariance in a second Fourier variable.

Owner: Kevin's Goldbach research.  Purpose: identify the exact tensor
resonance left by ``mobius_dyadic_lag_gate.py``.  This is an algebraic identity
plus finite d=1 evidence at tiny H,V, not an asymptotic estimate.

For fixed m write u=l-A, 0<=u<A, and zero-pad the row sequence to any length
L>=2A-1.  With Phi_(m,l)(h) and I_m as in the dyadic gate, put

 Psi_m(k,h)=sum_(u=0)^(A-1) Phi_(m,A+u)(h)e_L(-k*u),
 G_m(k)=sum_(h in I_m)|Psi_m(k,h)|^2
        -rho_m sum_(h=1)^(m-1)|Psi_m(k,h)|^2,             (1)

where rho_m=|I_m|/(m-1).  For

 D_j={Delta: 2^j<=Delta<min(2^(j+1),A)},
 W_j(k)=2 sum_(Delta in D_j) cos(2*pi*k*Delta/L),         (2)

the exact linear-autocorrelation identity is

 C_j(m)=L^(-1) sum_(k=0)^(L-1) W_j(k)G_m(k).             (3)

Thus positive dyadic covariance comes from the two reinforcing quadrants
W_j,G_m>0 and W_j,G_m<0, opposed by the other two quadrants.  The first
quadrant is the direct tensor resonance: excess active-h energy lies where the
dyadic row-frequency multiplier is positive.  Formula (3) proves no saving.

There is also an exact reduction.  Split C_j=D_j+O_j into h in I_m and h
outside I_m, retaining coefficients 1-rho_m and -rho_m.  Pairwise Cauchy gives

 max(O_j,0) <= sum_m (log m)^2/m * rho_m * 2
   sum_(Delta in D_j,l) sqrt(E_(m,l)E_(m,l+Delta)) = P_j. (4)

Consequently max(C_j,0)<=max(D_j,0)+P_j.  The outside-band term is already at
the required H^-1 scale; the only new estimate needed for the dyadic sublemma
is max(D_j,0)<<N^epsilon*P_j for the signed active-band autocorrelation.
"""

import math

import numpy as np

from mobius_covariance_endpoint_probe import _actual_tail, _prime_flags


def dyadic_spectral_decomposition(values, active_columns, padding_factor=4):
    """Return both sides of (3) for an arbitrary A by F complex array."""
    values = np.asarray(values)
    if values.ndim != 2 or values.shape[0] < 2 or values.shape[1] < 1:
        raise ValueError("values must be an A by F array with A>=2 and F>=1")
    active_columns = np.asarray(active_columns, dtype=int)
    if (active_columns.ndim != 1 or not len(active_columns)
            or np.any(active_columns < 0)
            or np.any(active_columns >= values.shape[1])
            or len(np.unique(active_columns)) != len(active_columns)):
        raise ValueError("active_columns must be distinct valid column indices")

    if type(padding_factor) is not int or padding_factor < 2:
        raise ValueError("padding_factor must be an integer at least two")
    A, frequency_count = values.shape
    length = padding_factor * A
    rho = len(active_columns) / frequency_count
    row_transform = np.fft.fft(values, n=length, axis=0)
    power = np.abs(row_transform) ** 2
    excess = (np.sum(power[:, active_columns], axis=1)
              - rho * np.sum(power, axis=1))
    blocks = []
    block_start = 1
    row_frequencies = np.arange(length)
    while block_start < A:
        block_stop = min(2 * block_start, A)
        deltas = np.arange(block_start, block_stop)
        multiplier = 2 * np.sum(np.cos(
            2 * math.pi * row_frequencies[:, None] * deltas[None, :] / length
        ), axis=1)
        product = multiplier * excess / length

        direct = 0.0
        for delta in deltas:
            left, right = values[:-delta], values[delta:]
            direct += 2 * float(np.real(
                np.sum(left[:, active_columns]
                       * np.conjugate(right[:, active_columns]))
                - rho * np.sum(left * np.conjugate(right))))

        quadrants = {}
        for w_sign, w_mask in (("w_positive", multiplier > 0),
                               ("w_negative", multiplier < 0)):
            for g_sign, g_mask in (("g_positive", excess > 0),
                                   ("g_negative", excess < 0)):
                quadrants[f"{w_sign}_{g_sign}"] = float(np.sum(
                    product[w_mask & g_mask]))
        blocks.append({
            "lag_first": block_start,
            "lag_last": block_stop - 1,
            "direct_covariance": direct,
            "spectral_covariance": float(np.sum(product)),
            "identity_error": float(np.sum(product) - direct),
            "quadrants": quadrants,
        })
        block_start *= 2
    return {
        "row_count": A,
        "frequency_count": frequency_count,
        "padding_length": length,
        "rho": rho,
        "blocks": tuple(blocks),
    }


def finite_mobius_lag_spectrum(N=32000, cofactor_left=None, padding_factor=4):
    """Aggregate (1)--(3) over the actual aligned Mobius--log rows."""
    if type(N) is not int or N < 1024 or N % 32:
        raise ValueError("N must be an integer multiple of 32 and at least 1024")
    H, M, V = int(N ** .1), int(N ** .59), int(N ** .15)
    if cofactor_left is None:
        cofactor_left = (N + 8 * M - 1) // (8 * M)
    if type(cofactor_left) is not int or cofactor_left < 2:
        raise ValueError("cofactor_left must be an integer at least two")
    if type(padding_factor) is not int or padding_factor < 2:
        raise ValueError("padding_factor must be an integer at least two")
    flags = _prime_flags(2 * M)
    primes = tuple(prime for prime in range(M + 1, 2 * M + 1)
                   if flags[prime])
    if not primes:
        raise ValueError("the prime companion range must be nonempty")
    if (8 * primes[0] * cofactor_left < N
            or 16 * primes[-1] * cofactor_left > 7 * N):
        raise ValueError("the aligned block leaves the central annulus")

    length = padding_factor * cofactor_left
    weighted_excess = np.zeros(length)
    weighted_active_part = np.zeros(length)
    weighted_outside_part = np.zeros(length)
    starts = []
    start = 1
    while start < cofactor_left:
        starts.append(start)
        start *= 2
    principal_cauchy = np.zeros(len(starts))
    tail = _actual_tail(N, V, 0, N)

    for prime in primes:
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
        values = centered[:, 1:]
        row_transform = np.fft.fft(values, n=length, axis=0)
        power = np.abs(row_transform) ** 2
        active_power = np.sum(power[:, modes - 1], axis=1)
        outside_power = np.sum(power, axis=1) - active_power
        active_part = (1 - rho) * active_power
        outside_part = -rho * outside_power
        excess = active_part + outside_part
        weight = math.log(prime) ** 2 / prime
        weighted_excess += weight * excess
        weighted_active_part += weight * active_part
        weighted_outside_part += weight * outside_part

        energies = np.sum(np.abs(values) ** 2, axis=1)
        for block_index, block_start in enumerate(starts):
            block_stop = min(2 * block_start, cofactor_left)
            local_cauchy = 0.0
            for delta in range(block_start, block_stop):
                local_cauchy += 2 * float(np.sum(np.sqrt(
                    energies[:-delta] * energies[delta:])))
            principal_cauchy[block_index] += weight * rho * local_cauchy

    row_frequencies = np.arange(length)
    blocks = []
    for block_index, block_start in enumerate(starts):
        block_stop = min(2 * block_start, cofactor_left)
        deltas = np.arange(block_start, block_stop)
        multiplier = 2 * np.sum(np.cos(
            2 * math.pi * row_frequencies[:, None] * deltas[None, :] / length
        ), axis=1)
        product = multiplier * weighted_excess / length
        active_product = multiplier * weighted_active_part / length
        outside_product = multiplier * weighted_outside_part / length
        budget = principal_cauchy[block_index]
        quadrants = {}
        for w_sign, w_mask in (("w_positive", multiplier > 0),
                               ("w_negative", multiplier < 0)):
            for g_sign, g_mask in (("g_positive", weighted_excess > 0),
                                   ("g_negative", weighted_excess < 0)):
                quadrants[f"{w_sign}_{g_sign}"] = float(
                    np.sum(product[w_mask & g_mask]) / budget)
        positive = float(np.sum(np.maximum(product, 0)) / budget)
        negative = float(-np.sum(np.minimum(product, 0)) / budget)
        blocks.append({
            "lag_first": block_start,
            "lag_last": block_stop - 1,
            "signed_ratio": float(np.sum(product) / budget),
            "active_band_signed_ratio": float(
                np.sum(active_product) / budget),
            "active_band_positive_spectral_ratio": float(
                np.sum(np.maximum(active_product, 0)) / budget),
            "outside_band_signed_ratio": float(
                np.sum(outside_product) / budget),
            "positive_spectral_ratio": positive,
            "negative_spectral_ratio": negative,
            "signed_to_absolute_fraction": (
                abs(positive - negative) / (positive + negative)
                if positive + negative else 0.0),
            "quadrant_ratios": quadrants,
        })
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "cofactor_left": cofactor_left,
        "prime_count": len(primes),
        "padding_length": length,
        "positive_excess_frequency_count": int(np.sum(weighted_excess > 0)),
        "maximum_weighted_excess": float(np.max(weighted_excess)),
        "minimum_weighted_excess": float(np.min(weighted_excess)),
        "blocks": tuple(blocks),
        "maximum_positive_active_band_ratio": max(
            max(block["active_band_signed_ratio"], 0.0) for block in blocks),
        "joint_spectral_saving_proved": False,
    }


if __name__ == "__main__":
    for key, value in finite_mobius_lag_spectrum().items():
        print(f"{key}: {value}")
