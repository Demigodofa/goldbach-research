"""Test whether an exact-Q packet is controlled by its Ramanujan mean.

For a fixed reduced difference denominator Q, define

    D_Q(r)=sum_(f_i-f_j=r/Q) c_i conjugate(c_j),  (r,Q)=1.

Then the boundary packet is exactly

    C_Q=sum_((r,Q)=1) D_Q(r) K_A(r/Q).

The constant-residue projection replaces ``D_Q(r)`` by its mean.  Its kernel
factor is the short average of the Ramanujan sum ``c_Q(ell)``.  Comparing this
projection with the exact packet tests the simplest possible Ramanujan-sum
mechanism without discarding the nonconstant residue data.
"""

import math

import numpy as np

from lcm_sawtooth_signed_difference_bins import (
    _signed_frequency_data,
)
from lcm_sawtooth_reduced_difference_mass import _validate_inputs


def _prime_factors(value):
    factors = []
    candidate = 2
    while candidate * candidate <= value:
        if value % candidate == 0:
            factors.append(candidate)
            while value % candidate == 0:
                value //= candidate
        candidate += 1 if candidate == 2 else 2
    if value > 1:
        factors.append(value)
    return tuple(factors)


def _euler_phi(value):
    result = value
    for factor in _prime_factors(value):
        result -= result // factor
    return result


def _mobius(value):
    sign = 1
    candidate = 2
    while candidate * candidate <= value:
        if value % candidate == 0:
            value //= candidate
            sign = -sign
            if value % candidate == 0:
                return 0
        candidate += 1 if candidate == 2 else 2
    if value > 1:
        sign = -sign
    return sign


def _ramanujan_sum(modulus, value):
    quotient = modulus // math.gcd(modulus, value)
    return (_mobius(quotient) * _euler_phi(modulus)
            // _euler_phi(quotient))


def _crt_tensor_metrics(modulus, units, values):
    """Measure rank concentration under every nontrivial prime CRT split."""
    metrics = []
    for factor in _prime_factors(modulus):
        if factor == 2:
            continue
        cofactor = modulus // factor
        if cofactor == 1:
            continue
        cofactor_candidates = np.arange(1, cofactor, dtype=np.int64)
        cofactor_units = cofactor_candidates[
            np.gcd(cofactor_candidates, cofactor) == 1]
        lookup = np.full(cofactor, -1, dtype=np.int64)
        lookup[cofactor_units] = np.arange(len(cofactor_units))
        matrix = np.zeros(
            (factor - 1, len(cofactor_units)), dtype=complex)
        matrix[units % factor - 1, lookup[units % cofactor]] = values
        singular_values = np.linalg.svd(matrix, compute_uv=False)
        energy = singular_values ** 2
        total = float(np.sum(energy))
        metrics.append({
            "prime_factor": factor,
            "tensor_shape": matrix.shape,
            "leading_singular_energy_fraction": float(
                energy[0] / total if total else 0.0),
            "effective_singular_rank": float(
                total ** 2 / np.sum(energy ** 2) if total else 0.0),
        })
    return tuple(metrics)


def fixed_q_residue_receipt(
        modulus, ell_first, row_count, ell_freeze,
        divisor_lower, divisor_upper, target_denominators):
    """Return the exact residue decomposition for named reduced denominators."""
    _validate_inputs(
        modulus, ell_freeze, row_count, divisor_lower, divisor_upper)
    if type(ell_first) is not int or ell_first < 1:
        raise ValueError("ell_first must be a positive integer")
    if (not isinstance(target_denominators, tuple)
            or not target_denominators
            or any(type(value) is not int or value <= 1
                   for value in target_denominators)
            or len(set(target_denominators)) != len(target_denominators)):
        raise ValueError("target_denominators must be distinct integers > 1")

    denominators, numerators, coefficients, _ = _signed_frequency_data(
        modulus, ell_freeze, divisor_lower, divisor_upper, False)
    complete_energy = float(np.sum(np.abs(coefficients) ** 2))
    residue_sums = {value: {} for value in target_denominators}
    chunk_size = 64
    for first in range(0, len(coefficients), chunk_size):
        left_d = denominators[first:first + chunk_size, None]
        left_k = numerators[first:first + chunk_size, None]
        common = np.lcm(left_d, denominators[None, :])
        difference_numerator = (
            left_k * (common // left_d)
            - numerators[None, :] * (common // denominators[None, :]))
        common_factor = np.gcd(np.abs(difference_numerator), common)
        reduced = common // common_factor
        products = (
            coefficients[first:first + chunk_size, None]
            * np.conjugate(coefficients[None, :]))
        for target in target_denominators:
            selected = reduced == target
            if not np.any(selected):
                continue
            residues = (
                modulus
                * (difference_numerator[selected] // common_factor[selected])
                % target).astype(np.int64)
            values = products[selected]
            unique, inverse = np.unique(residues, return_inverse=True)
            grouped = (
                np.bincount(inverse, weights=values.real)
                + 1j * np.bincount(inverse, weights=values.imag))
            destination = residue_sums[target]
            for residue, value in zip(unique, grouped):
                key = int(residue)
                destination[key] = destination.get(key, 0j) + value

    packets = []
    for target in target_denominators:
        residue_sum = residue_sums[target]
        if not residue_sum:
            raise ValueError(f"target denominator {target} is absent")
        candidates = np.arange(1, target, dtype=np.int64)
        units = candidates[np.gcd(candidates, target) == 1]
        values = np.array(
            [residue_sum.get(int(residue), 0j) for residue in units])
        roots = np.exp(2j * np.pi * units / target)
        kernels = (
            np.exp(2j * np.pi * units * ell_first / target)
            * (1 - roots ** row_count)
            / (row_count * (1 - roots)))
        packet = np.sum(values * kernels)
        mean_value = np.mean(values)
        kernel_sum = np.sum(kernels)
        constant_projection = mean_value * kernel_sum
        centered = values - mean_value
        residue_array = np.zeros(target, dtype=complex)
        residue_array[units] = values
        additive_transform = np.fft.ifft(residue_array) * target
        active_transform = additive_transform[
            np.arange(ell_first, ell_first + row_count) % target]
        full_transform_l2 = float(np.mean(np.abs(additive_transform) ** 2))
        active_transform_l2 = float(np.mean(np.abs(active_transform) ** 2))
        transform_packet = np.mean(active_transform)
        active_transform_energy = float(
            np.sum(np.abs(active_transform) ** 2))
        lag_inner_products = tuple(
            complex(np.sum(
                active_transform[lag:]
                * np.conjugate(active_transform[:-lag])))
            / complete_energy ** 2
            for lag in range(1, row_count))
        ramanujan_mean = sum(
            _ramanujan_sum(target, ell)
            for ell in range(ell_first, ell_first + row_count)) / row_count
        packets.append({
            "denominator": target,
            "primitive_residue_count": len(units),
            "represented_residue_count": len(residue_sum),
            "represented_residue_fraction": len(residue_sum) / len(units),
            "packet_over_complete": float(packet.real / complete_energy),
            "packet_absolute_square_over_complete_squared": float(
                abs(packet) ** 2 / complete_energy ** 2),
            "packet_imaginary_error_over_complete": float(
                abs(packet.imag) / complete_energy),
            "constant_projection_over_complete": float(
                constant_projection.real / complete_energy),
            "constant_projection_share_of_packet": float(
                abs(constant_projection) / abs(packet) if packet else 0.0),
            "centered_residue_l2_fraction": float(
                np.linalg.norm(centered) / np.linalg.norm(values)
                if np.linalg.norm(values) else 0.0),
            "additive_transform_packet_error_over_complete": float(
                abs(transform_packet - packet) / complete_energy),
            "additive_transform_parseval_relative_error": float(
                abs(full_transform_l2 - np.sum(np.abs(values) ** 2))
                / full_transform_l2 if full_transform_l2 else 0.0),
            "residue_l2_over_complete_squared": float(
                np.sum(np.abs(values) ** 2) / complete_energy ** 2),
            "Q_weighted_residue_l2_over_complete_squared": float(
                target * np.sum(np.abs(values) ** 2)
                / complete_energy ** 2),
            "active_window_transform_l2_over_full_period": (
                active_transform_l2 / full_transform_l2
                if full_transform_l2 else 0.0),
            "active_window_mean_square_over_l2": float(
                abs(transform_packet) ** 2 / active_transform_l2
                if active_transform_l2 else 0.0),
            "row_count_scaled_mean_square_over_l2": float(
                row_count * abs(transform_packet) ** 2 / active_transform_l2
                if active_transform_l2 else 0.0),
            "active_window_transform_energy_over_complete_squared": float(
                active_transform_energy / complete_energy ** 2),
            "active_window_transform_over_complete": tuple(
                complex(value / complete_energy)
                for value in active_transform),
            "active_window_lag_inner_products_over_complete_squared": (
                lag_inner_products),
            "crt_prime_split_metrics": _crt_tensor_metrics(
                target, units, centered),
            "ramanujan_kernel_sum": float(ramanujan_mean),
            "ramanujan_kernel_identity_error": float(
                abs(kernel_sum - ramanujan_mean)),
        })
    return {
        "modulus": modulus,
        "ell_range": (ell_first, ell_first + row_count - 1),
        "ell_freeze": ell_freeze,
        "divisor_range": (divisor_lower, divisor_upper),
        "complete_energy": complete_energy,
        "packets": tuple(packets),
        "exact_residue_packet_identity_proved": True,
        "constant_ramanujan_packet_bound_proved": False,
        "nonconstant_residue_bound_proved": False,
    }


if __name__ == "__main__":
    receipt = fixed_q_residue_receipt(
        251, 46, 46, 69, 4, 20,
        (15470, 43890, 14586, 21945, 15015))
    for packet in receipt["packets"]:
        print(packet)
