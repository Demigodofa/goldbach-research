"""Split aligned Mobius covariance into point, same-row, and cross-row terms.

Owner: Kevin's Goldbach research.  Purpose: locate cancellation or
reinforcement after the physical q-aligned endpoint reduction.  This is a
floating d=1 diagnostic at tiny H,V, not an asymptotic estimate.

For J_m=(mA,2mA] and nonzero residues 1<=r<m, write

    C_l(r)=r_V(m*l+r),                 A<=l<2A,
    Phi_l(h)=sum_r C_l(r)[e_m(-h*r)+1/(m-1)].              (1)

Then the exact covariance bilinear form between rows l1,l2 is

    Q(l1,l2)=sum_(h in I_m)Phi_l1(h)conj(Phi_l2(h))
      -R/(m-1)sum_(1<=h<m)Phi_l1(h)conj(Phi_l2(h)).        (2)

The total OFF is the ordered sum of (2).  Split it into:

* point: l1=l2 and r=s in the residue-kernel expansion;
* same-row nonpoint: l1=l2 and r!=s;
* cross-row: l1!=l2, with all residues retained.           (3)

MEASURED RESULTS, NORMALIZED BY THE TOTAL PRINCIPAL BASELINE.

 N       A      total       point          same-row nonpoint   cross-row
 32000   9    -.228310    +5.64e-7             -2.990264       +2.761953
 200000 19   -.160433    +1.42e-7             -2.768728       +2.608294
 200000 30   -.003395    +1.02e-8             -3.729491       +3.726097
 1200000 39  -.156924    -1.05e-8             -4.886587       +4.729663

Thus the literal diagonal is harmless in these tests, but the l1!=l2 family
reinforces rather than cancels and is comparable to a large negative
same-row term.  The small final covariance is their signed difference.  This
falsifies a mechanism based on cancellation of every off-diagonal family; it
does not falsify the target magnitude estimate or prove persistent signs.
Triangle-bounding either large component would destroy the observed gain.
"""

import math

import numpy as np

from mobius_covariance_endpoint_probe import _actual_tail, _prime_flags


def finite_aligned_covariance_split(N=32000, cofactor_left=None):
    """Return the exact finite decomposition (3), aggregated over prime m."""
    if type(N) is not int or N < 1024 or N % 32:
        raise ValueError("N must be an integer multiple of 32 and at least 1024")
    H, M, V = int(N ** .1), int(N ** .59), int(N ** .15)
    if cofactor_left is None:
        cofactor_left = (N + 8 * M - 1) // (8 * M)
    if type(cofactor_left) is not int or cofactor_left < 1:
        raise ValueError("cofactor_left must be a positive integer")
    if 2 * (2 * M) * cofactor_left > 7 * N // 8:
        raise ValueError("the aligned block can leave the central annulus")

    tail = _actual_tail(N, V, 0, N)
    flags = _prime_flags(2 * M)
    totals = {name: 0.0 for name in (
        "total_off", "point", "same_row_nonpoint", "cross_row",
        "principal_baseline")}
    prime_count = 0

    for prime in range(M + 1, 2 * M + 1):
        if not flags[prime]:
            continue
        prime_count += 1
        modes = np.array([
            h for h in range(1, prime)
            if prime / (2 * math.pi * H) < min(h, prime - h)
            < prime / (math.pi * H)
        ], dtype=int)
        band_size = len(modes)
        indicator = np.zeros(prime)
        indicator[modes] = 1.0
        band_kernel = np.fft.ifft(indicator) * prime
        rows = []
        same_row = point = 0.0

        for ell in range(cofactor_left, 2 * cofactor_left):
            row = np.zeros(prime)
            row[1:] = tail[prime * ell + 1:prime * (ell + 1)]
            transform = np.fft.fft(row)
            centered = transform + row.sum() / (prime - 1)
            band = float(np.sum(np.abs(centered[modes]) ** 2))
            full = float(np.sum(np.abs(centered[1:]) ** 2))
            same_row += band - band_size / (prime - 1) * full
            point += float(np.sum(
                row[1:] ** 2
                * (2 * band_kernel[1:].real / (prime - 1)
                   + 2 * band_size / (prime - 1) ** 2)))
            rows.append(row)

        combined = np.sum(rows, axis=0)
        transform = np.fft.fft(combined)
        centered = transform + combined.sum() / (prime - 1)
        band = float(np.sum(np.abs(centered[modes]) ** 2))
        full = float(np.sum(np.abs(centered[1:]) ** 2))
        principal = band_size / (prime - 1) * full
        total = band - principal
        weight = math.log(prime) ** 2 / prime
        totals["total_off"] += weight * total
        totals["point"] += weight * point
        totals["same_row_nonpoint"] += weight * (same_row - point)
        totals["cross_row"] += weight * (total - same_row)
        totals["principal_baseline"] += weight * principal

    principal = totals["principal_baseline"]
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "cofactor_left": cofactor_left,
        "prime_count": prime_count,
        **totals,
        "normalized": {name: totals[name] / principal for name in (
            "total_off", "point", "same_row_nonpoint", "cross_row")},
        "recombination_error": (totals["total_off"] - totals["point"]
                                - totals["same_row_nonpoint"]
                                - totals["cross_row"]),
        "signed_off_diagonal_estimate_proved": False,
    }


if __name__ == "__main__":
    for key, value in finite_aligned_covariance_split().items():
        print(f"{key}: {value}")
