"""Locate cancellation in the unequal active Dirichlet kernel by distance.

For unequal row integers n,n', their active contribution is

 log(n/a)log(n'/b) K_I(n-n'),
 K_I(r)=sum_(h in I_m)e_m(-hr).

This probe decomposes the exact unequal matrix into cyclic-distance bands

 1<=|r|_m<=H, H<|r|_m<=2H, 2H<|r|_m<=4H, ... .

It records each band's projection against the equality-collision matrix and
the cumulative residual.  The concrete hypothesis is that cancellation is
localized near the physical scale H.  A residual that falls only after many
large-distance bands falsifies that mechanism.  The direct pair enumeration
is intentionally restricted to modest prime moduli.
"""

import math

import numpy as np

from active_cross_component_probe import _row_components
from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from near_cutoff_geometric_bound import _active_modes


def _distance_edges(modulus, shift_length):
    edges = [0, shift_length]
    while edges[-1] < modulus // 2:
        edges.append(min(2 * edges[-1], modulus // 2))
    return tuple(edges)


def unequal_distance_bands(modulus, shift_length, ell_first, row_count,
                           divisor_left):
    """Return an exact distance-band receipt for one modest prime modulus."""
    if any(type(value) is not int for value in (
            modulus, shift_length, ell_first, row_count, divisor_left)):
        raise ValueError("all arguments must be integers")
    if (modulus > 20000 or not 2 <= shift_length <= divisor_left
            or 2 * divisor_left >= modulus
            or ell_first < 1 or row_count < 1):
        raise ValueError("require prime m<=20000, 2<=H<=U, 2U<m, valid rows")
    flags = _prime_flags(modulus)
    if not flags[modulus]:
        raise ValueError("modulus must be prime")
    mobius = _mobius_values(2 * divisor_left)
    divisors = tuple(a for a in range(divisor_left + 1, 2 * divisor_left + 1)
                     if mobius[a])
    divisor_array = np.array(divisors, dtype=float)
    totients = np.array([_totient(a) for a in divisors], dtype=float)
    modes = _active_modes(modulus, shift_length)
    rho = len(modes) / (modulus - 1)
    indicator = np.zeros(modulus)
    indicator[np.array(modes, dtype=int)] = 1
    kernel = np.fft.fft(indicator)
    edges = _distance_edges(modulus, shift_length)
    band_count = len(edges) - 1
    equality = np.zeros((len(divisors), len(divisors)), dtype=complex)
    unequal_exact = np.zeros_like(equality)
    bands = [np.zeros_like(equality) for _ in range(band_count)]
    frame = np.zeros(len(divisors))

    for ell in range(ell_first, ell_first + row_count):
        row_equality, row_unequal, _, _ = _row_components(
            modulus, shift_length, ell, divisors)
        equality += (1 - rho) * row_equality
        unequal_exact += (1 - rho) * row_unequal
        integers = []
        weights = []
        for divisor in divisors:
            first = modulus * ell // divisor + 1
            last = (modulus * (ell + 1) - 1) // divisor
            cofactors = np.arange(first, last + 1, dtype=np.int64)
            integers.append(divisor * cofactors)
            weights.append(np.log(cofactors))
        for left_index in range(len(divisors)):
            for right_index in range(len(divisors)):
                differences = ((integers[left_index][:, None]
                                - integers[right_index][None, :]) % modulus)
                nonzero = differences != 0
                residues = differences[nonzero]
                distances = np.minimum(residues, modulus - residues)
                products = (weights[left_index][:, None]
                            * weights[right_index][None, :])[nonzero]
                values = products * kernel[residues]
                band_indices = np.searchsorted(
                    np.array(edges[1:]), distances, side="left")
                real = np.bincount(
                    band_indices, weights=np.real(values), minlength=band_count)
                imaginary = np.bincount(
                    band_indices, weights=np.imag(values), minlength=band_count)
                for band_index in range(band_count):
                    bands[band_index][left_index, right_index] += (
                        (1 - rho) * (real[band_index]
                                     + 1j * imaginary[band_index]))
        logs = np.log(modulus * ell / divisor_array)
        frame += rho * modulus ** 2 * logs ** 2 * (
            totients / divisor_array ** 2)

    scale = np.sqrt(frame)
    normalized_equality = equality / (scale[:, None] * scale[None, :])
    normalized_unequal = unequal_exact / (scale[:, None] * scale[None, :])
    normalized_bands = [
        band / (scale[:, None] * scale[None, :]) for band in bands]
    np.fill_diagonal(normalized_equality, 0)
    np.fill_diagonal(normalized_unequal, 0)
    for band in normalized_bands:
        np.fill_diagonal(band, 0)
    equality_norm_squared = float(np.vdot(
        normalized_equality, normalized_equality).real)
    equality_norm = math.sqrt(equality_norm_squared)
    cumulative = normalized_equality.copy()
    band_receipts = []
    for band_index, band in enumerate(normalized_bands):
        cumulative += band
        band_receipts.append({
            "distance_left_open": edges[band_index],
            "distance_right_closed": edges[band_index + 1],
            "band_frobenius_over_equality": float(
                np.linalg.norm(band) / equality_norm),
            "negative_projection_on_equality": float(
                -np.vdot(normalized_equality, band).real
                / equality_norm_squared),
            "cumulative_residual_over_equality": float(
                np.linalg.norm(cumulative) / equality_norm),
        })
    reconstructed = sum(bands, np.zeros_like(unequal_exact))
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "ell_first": ell_first,
        "row_count": row_count,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisor_count": len(divisors),
        "distance_bands": band_receipts,
        "unequal_reconstruction_error_max": float(
            np.max(np.abs(reconstructed - unequal_exact))),
        "final_raw_residual_over_equality": float(
            np.linalg.norm(normalized_equality + normalized_unequal)
            / equality_norm),
        "near_H_localization_proved": False,
    }


if __name__ == "__main__":
    result = unequal_distance_bands(1009, 5, 9, 8, 8)
    for key, value in result.items():
        print(f"{key}: {value}")
