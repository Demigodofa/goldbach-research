"""Test the arithmetic transfer from an odd partner d to its double 2d.

For odd d, reduction modulo d maps the primitive residues modulo 2d
bijectively onto the primitive residues modulo d.  The geometric sum at 2d
is an exact half-interval sum with an endpoint phase factor.  This module
checks that identity and tests the stronger, falsifiable proposal that the
doubled frequency vector and polynomial vector are each scalar transfers of
their base-d counterparts.
"""

import math

import numpy as np

from lcm_sawtooth_incomplete_frequency import _quadratic_support_data
from lcm_sawtooth_signed_difference_bins import _stable_geometric_sum
from mobius_covariance_lag_probe import _prime_flags


def _relative_best_scalar_residual(source, target):
    source = np.asarray(source, dtype=complex)
    target = np.asarray(target, dtype=complex)
    if source.shape != target.shape or source.ndim != 1:
        raise ValueError("source and target must be matching vectors")
    source_energy = float(np.vdot(source, source).real)
    target_norm = float(np.linalg.norm(target))
    if not source_energy:
        return (0j, 0.0) if not target_norm else (None, 1.0)
    if not target_norm:
        return 0j, 0.0
    scalar = np.vdot(source, target) / source_energy
    residual = float(np.linalg.norm(target - scalar * source) / target_norm)
    return complex(scalar), residual


def doubled_partner_geometric_receipt(
        prime_modulus, odd_partner, tolerance=1e-12):
    """Verify the primitive lift and half-interval geometric identity."""
    if (type(prime_modulus) is not int or prime_modulus < 3
            or prime_modulus % 2 == 0
            or not _prime_flags(prime_modulus)[prime_modulus]):
        raise ValueError("prime_modulus must be an odd prime")
    if (type(odd_partner) is not int or odd_partner < 3
            or odd_partner % 2 == 0):
        raise ValueError("odd_partner must be an odd integer at least three")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")

    base = np.arange(1, odd_partner, dtype=np.int64)
    base = base[np.gcd(base, odd_partner) == 1]
    lifted = np.where(base % 2 == 1, base, base + odd_partner)
    lift_is_bijection = bool(
        len(np.unique(lifted)) == len(base)
        and np.all(np.gcd(lifted, 2 * odd_partner) == 1)
        and np.array_equal(lifted % odd_partner, base))
    direct = _stable_geometric_sum(
        prime_modulus, 2 * odd_partner, lifted)
    doubled_complete_period = bool(
        (prime_modulus - 1) % (2 * odd_partner) == 0)
    if doubled_complete_period:
        direct = np.zeros_like(direct)
    half_length = (prime_modulus - 1) // 2
    half_sine_residue = (lifted * half_length) % (2 * odd_partner)
    half_sum = (
        np.exp(1j * np.pi * lifted * (half_length + 1) / odd_partner)
        * np.sin(np.pi * half_sine_residue / odd_partner)
        / np.sin(np.pi * lifted / odd_partner))
    endpoint_factor = 1 + np.exp(-1j * np.pi * lifted / odd_partner)
    factored = endpoint_factor * half_sum
    identity_error = float(np.max(np.abs(direct - factored)))
    identity_relative_error = float(np.max(
        np.abs(direct - factored) / np.maximum(1.0, np.abs(direct))))
    base_geometric = _stable_geometric_sum(
        prime_modulus, odd_partner, base)
    base_complete_period = bool(
        (prime_modulus - 1) % odd_partner == 0)
    if base_complete_period:
        base_geometric = np.zeros_like(base_geometric)
    scalar, scalar_residual = _relative_best_scalar_residual(
        base_geometric, direct)
    return {
        "prime_modulus": prime_modulus,
        "odd_partner": odd_partner,
        "doubled_partner": 2 * odd_partner,
        "primitive_residue_count": len(base),
        "primitive_odd_lift_is_bijection_proved": lift_is_bijection,
        "half_interval_length": half_length,
        "base_geometric_is_complete_period_zero": base_complete_period,
        "doubled_geometric_is_complete_period_zero": (
            doubled_complete_period),
        "both_geometric_vectors_are_exactly_zero": bool(
            base_complete_period and doubled_complete_period),
        "half_interval_factorization_maximum_error": identity_error,
        "half_interval_factorization_maximum_relative_error": (
            identity_relative_error),
        "best_full_geometric_transfer_scalar": (
            None if scalar is None else
            (float(scalar.real), float(scalar.imag))),
        "best_full_geometric_transfer_relative_residual": scalar_residual,
        "exact_half_interval_geometric_identity_test_passes": bool(
            lift_is_bijection and identity_relative_error <= tolerance),
        "single_scalar_full_geometric_transfer_test_passes": bool(
            scalar_residual <= tolerance),
    }


def partner_doubling_transfer_receipt(
        scale_modulus=127, odd_partners=(35, 65), tolerance=1e-12):
    """Test the d-to-2d scalar-transfer proposal on the project fixture."""
    odd_partners = tuple(sorted(set(odd_partners)))
    if (type(scale_modulus) is not int or scale_modulus < 3
            or not odd_partners):
        raise ValueError("require a positive scale and partner set")
    if any(type(value) is not int or value < 3 or value % 2 == 0
           for value in odd_partners):
        raise ValueError("all partners must be odd integers at least three")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    flags = _prime_flags(2 * scale_modulus)
    primes = tuple(
        value for value in range(scale_modulus, 2 * scale_modulus)
        if flags[value])
    if not primes:
        raise ArithmeticError("prime block is empty")
    support = dict(_quadratic_support_data(3, 13)[1])
    if any(value not in support or 2 * value not in support
           for value in odd_partners):
        raise ArithmeticError("partner and doubled partner must be in support")

    polynomial_rows = []
    for partner in odd_partners:
        scalar, residual = _relative_best_scalar_residual(
            support[partner], support[2 * partner])
        polynomial_rows.append({
            "odd_partner": partner,
            "doubled_partner": 2 * partner,
            "best_polynomial_transfer_scalar": (
                float(scalar.real), float(scalar.imag)),
            "best_polynomial_transfer_relative_residual": residual,
            "single_scalar_polynomial_transfer_test_passes": bool(
                residual <= tolerance),
        })
    geometric_rows = tuple(
        doubled_partner_geometric_receipt(prime, partner, tolerance)
        for prime in primes for partner in odd_partners)
    exact_half_identity = all(
        row["exact_half_interval_geometric_identity_test_passes"]
        for row in geometric_rows)
    scalar_geometric = all(
        row["single_scalar_full_geometric_transfer_test_passes"]
        for row in geometric_rows)
    scalar_polynomial = all(
        row["single_scalar_polynomial_transfer_test_passes"]
        for row in polynomial_rows)
    nontrivial_geometric_rows = tuple(
        row for row in geometric_rows
        if not row["both_geometric_vectors_are_exactly_zero"])
    return {
        "scale_modulus": scale_modulus,
        "prime_moduli": primes,
        "odd_partners": odd_partners,
        "tolerance": tolerance,
        "polynomial_transfer_rows": tuple(polynomial_rows),
        "geometric_transfer_rows": geometric_rows,
        "maximum_half_interval_factorization_error": max(
            row["half_interval_factorization_maximum_error"]
            for row in geometric_rows),
        "maximum_half_interval_factorization_relative_error": max(
            row["half_interval_factorization_maximum_relative_error"]
            for row in geometric_rows),
        "trivial_zero_geometric_channel_count": (
            len(geometric_rows) - len(nontrivial_geometric_rows)),
        "minimum_nontrivial_full_geometric_transfer_relative_residual": min(
            row["best_full_geometric_transfer_relative_residual"]
            for row in nontrivial_geometric_rows),
        "maximum_nontrivial_full_geometric_transfer_relative_residual": max(
            row["best_full_geometric_transfer_relative_residual"]
            for row in nontrivial_geometric_rows),
        "exact_primitive_lift_half_interval_identity_proved": bool(
            exact_half_identity),
        "single_scalar_geometric_transfer_all_channels_passes": bool(
            scalar_geometric),
        "single_scalar_polynomial_transfer_all_partners_passes": bool(
            scalar_polynomial),
        "single_scalar_partner_doubling_transfer_hypothesis_passes": bool(
            exact_half_identity and scalar_geometric and scalar_polynomial),
        "partner_doubling_transfer_assigns_favorable_sign_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(partner_doubling_transfer_receipt())
