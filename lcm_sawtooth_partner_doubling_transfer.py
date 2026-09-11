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
from lcm_sawtooth_arithmetic_covariance_basis import (
    covariance_inverse_root,
    project_one_frequency_covariance,
)
from lcm_sawtooth_centered_basis_gershgorin import symmetric_square_transform
from lcm_sawtooth_lifted_endpoint_frame import (
    _symmetric_pair_coordinates,
    project_prime_block_lifted_endpoint_scan,
)
from lcm_sawtooth_reduced_denominator_interference import (
    _packet_residue_cells,
)
from lcm_sawtooth_signed_difference_bins import _stable_geometric_sum
from lcm_sawtooth_trace_traceless_block_frame import trace_traceless_transform
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
    base_half_factor = (
        1 + np.exp(2j * np.pi * base * half_length / odd_partner))
    doubled_endpoint_factor = (
        1 + np.exp(-1j * np.pi * lifted / odd_partner))
    diagonal_multiplier = doubled_endpoint_factor / base_half_factor
    base_half_prediction = base_half_factor * half_sum
    base_half_error = float(np.max(
        np.abs(base_geometric - base_half_prediction)
        / np.maximum(1.0, np.abs(base_geometric))))
    # Use the common half-sum representation for the numerical transfer.
    # Directly multiplying the independently rounded full-period base sum by
    # T amplifies its error when the base half factor is small.
    diagonal_prediction = diagonal_multiplier * base_half_prediction
    diagonal_error = float(np.max(
        np.abs(direct - diagonal_prediction)
        / np.maximum(1.0, np.abs(direct))))
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
        "minimum_base_half_factor_absolute_value": float(np.min(
            np.abs(base_half_factor))),
        "base_half_interval_factorization_maximum_relative_error": (
            base_half_error),
        "diagonal_transfer_maximum_relative_error": diagonal_error,
        "half_interval_factorization_maximum_error": identity_error,
        "half_interval_factorization_maximum_relative_error": (
            identity_relative_error),
        "best_full_geometric_transfer_scalar": (
            None if scalar is None else
            (float(scalar.real), float(scalar.imag))),
        "best_full_geometric_transfer_relative_residual": scalar_residual,
        "exact_half_interval_geometric_identity_test_passes": bool(
            lift_is_bijection and identity_relative_error <= tolerance),
        "exact_residue_diagonal_transfer_test_passes": bool(
            base_half_error <= tolerance and diagonal_error <= tolerance),
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
    exact_diagonal_transfer = all(
        row["exact_residue_diagonal_transfer_test_passes"]
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
        "maximum_residue_diagonal_transfer_relative_error": max(
            row["diagonal_transfer_maximum_relative_error"]
            for row in geometric_rows),
        "maximum_base_half_factorization_relative_error": max(
            row["base_half_interval_factorization_maximum_relative_error"]
            for row in geometric_rows),
        "minimum_base_half_factor_absolute_value": min(
            row["minimum_base_half_factor_absolute_value"]
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
        "exact_residue_dependent_diagonal_transfer_proved": bool(
            exact_diagonal_transfer),
        "single_scalar_geometric_transfer_all_channels_passes": bool(
            scalar_geometric),
        "single_scalar_polynomial_transfer_all_partners_passes": bool(
            scalar_polynomial),
        "single_scalar_partner_doubling_transfer_hypothesis_passes": bool(
            exact_half_identity and scalar_geometric and scalar_polynomial),
        "partner_doubling_transfer_assigns_favorable_sign_proved": False,
        "signed_prime_correlation_proved": False,
    }


def _project_fragile_direction(scale_modulus, conductors):
    exclusions = ((), (conductors[0],), (conductors[1],), conductors)
    frames = {
        excluded: project_prime_block_lifted_endpoint_scan(
            scale_modulus, excluded)
        for excluded in exclusions}
    baseline = frames[()]
    covariance, _ = project_one_frequency_covariance(scale_modulus, baseline)
    transform3, _ = covariance_inverse_root(covariance)
    transform6 = symmetric_square_transform(
        transform3) @ trace_traceless_transform()

    def transformed(frame, key):
        raw = np.asarray(frame[key])
        result = transform6.T @ raw @ transform6
        return (result + result.T) / 2

    active = {
        excluded: transformed(
            frame, "aggregate_active_window_residue_energy_gram")
        for excluded, frame in frames.items()}
    full = {
        excluded: transformed(
            frame, "aggregate_full_residue_energy_gram")
        for excluded, frame in frames.items()}
    differences = {
        excluded: active[excluded] - .5 * full[excluded]
        for excluded in exclusions}
    additive = (
        differences[(conductors[0],)] + differences[(conductors[1],)]
        - differences[()])
    _, vectors = np.linalg.eigh(additive[1:, 1:])
    return baseline, transform6[:, 1:] @ vectors[:, 0]


def _matched_doubled_packet(
        prime_modulus, ell_freeze, conductor, odd_partner, direction,
        support):
    """Build one doubled packet through the base primitive-residue lift."""
    doubled_partner = 2 * odd_partner
    doubled_q = math.lcm(conductor, doubled_partner)
    logarithm = math.log(prime_modulus * ell_freeze)
    powers = np.asarray((logarithm ** 2, logarithm, 1.0))
    conductor_coordinate = np.asarray(support[conductor]) * powers
    doubled_coordinate = np.asarray(support[doubled_partner]) * powers
    lifted_coordinate = _symmetric_pair_coordinates(
        conductor_coordinate[None, :], doubled_coordinate[None, :])[0]
    direction_factor = float(lifted_coordinate @ direction)

    conductor_numerators = np.arange(1, conductor, dtype=np.int64)
    conductor_numerators = conductor_numerators[
        np.gcd(conductor_numerators, conductor) == 1]
    partner_numerators = np.arange(1, odd_partner, dtype=np.int64)
    partner_numerators = partner_numerators[
        np.gcd(partner_numerators, odd_partner) == 1]
    lifted_partner_numerators = np.where(
        partner_numerators % 2 == 1,
        partner_numerators,
        partner_numerators + odd_partner)
    conductor_geometric = _stable_geometric_sum(
        prime_modulus, conductor, conductor_numerators)
    half_length = (prime_modulus - 1) // 2
    half_sine_residue = (
        lifted_partner_numerators * half_length) % (2 * odd_partner)
    half_sum = (
        np.exp(
            1j * np.pi * lifted_partner_numerators
            * (half_length + 1) / odd_partner)
        * np.sin(np.pi * half_sine_residue / odd_partner)
        / np.sin(np.pi * lifted_partner_numerators / odd_partner))
    base_factor = (
        1 + np.exp(
            2j * np.pi * partner_numerators * half_length / odd_partner))
    doubled_factor = (
        1 + np.exp(
            -1j * np.pi * lifted_partner_numerators / odd_partner))
    transfer = doubled_factor / base_factor
    base_half_prediction = base_factor * half_sum
    predicted_partner_geometric = transfer * base_half_prediction
    actual_partner_geometric = _stable_geometric_sum(
        prime_modulus, doubled_partner, lifted_partner_numerators)
    geometric_error = float(np.max(
        np.abs(actual_partner_geometric - predicted_partner_geometric)
        / np.maximum(1.0, np.abs(actual_partner_geometric))))

    predicted_packet = np.zeros(doubled_q, dtype=complex)
    unexpected_reduced_denominator_count = 0
    nonodd_residue_count = 0

    def add_orientation(left_denominator, left_numerators, left_geometric,
                        right_denominator, right_numerators, right_geometric):
        nonlocal unexpected_reduced_denominator_count, nonodd_residue_count
        common = math.lcm(left_denominator, right_denominator)
        differences = (
            left_numerators[:, None] * (common // left_denominator)
            - right_numerators[None, :] * (common // right_denominator))
        common_factors = np.gcd(np.abs(differences), common)
        reduced = common // common_factors
        unexpected_reduced_denominator_count += int(np.count_nonzero(
            reduced != doubled_q))
        selected = reduced == doubled_q
        residues = (
            prime_modulus * (differences // common_factors) % reduced)
        nonodd_residue_count += int(np.count_nonzero(
            selected & (residues % 2 == 0)))
        coefficients = (
            left_geometric[:, None] * np.conjugate(right_geometric[None, :])
            * direction_factor)
        flat_residues = residues[selected]
        flat_coefficients = coefficients[selected]
        predicted_packet.real[:] += np.bincount(
            flat_residues, weights=flat_coefficients.real,
            minlength=doubled_q)
        predicted_packet.imag[:] += np.bincount(
            flat_residues, weights=flat_coefficients.imag,
            minlength=doubled_q)

    add_orientation(
        conductor, conductor_numerators, conductor_geometric,
        doubled_partner, lifted_partner_numerators,
        predicted_partner_geometric)
    add_orientation(
        doubled_partner, lifted_partner_numerators,
        predicted_partner_geometric,
        conductor, conductor_numerators, conductor_geometric)
    return {
        "predicted_packet": predicted_packet,
        "doubled_q": doubled_q,
        "direction_factor": direction_factor,
        "diagonal_geometric_transfer_maximum_relative_error": (
            geometric_error),
        "unexpected_reduced_denominator_pair_count": (
            unexpected_reduced_denominator_count),
        "nonodd_doubled_residue_pair_count": nonodd_residue_count,
    }


def partner_packet_transfer_receipt(
        scale_modulus=127,
        families=((77, 65, 1), (143, 35, 2)), tolerance=1e-12):
    """Transfer matched (c,d) source pairs to their doubled packet."""
    families = tuple(families)
    conductors = tuple(sorted(family[0] for family in families))
    if (type(scale_modulus) is not int or scale_modulus < 3
            or len(families) != 2 or len(conductors) != 2
            or any(len(family) != 3 for family in families)
            or any(type(conductor) is not int or conductor < 3
                   or conductor % 2 == 0
                   or type(partner) is not int or partner < 3
                   or partner % 2 == 0 or category not in (1, 2)
                   for conductor, partner, category in families)):
        raise ValueError("require two conductor-partner-category families")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    baseline, direction = _project_fragile_direction(
        scale_modulus, conductors)
    support = dict(_quadratic_support_data(*baseline["divisor_range"])[1])
    rows = []
    for frame_row in baseline["rows"]:
        packets, _, _, _, _, _, _ = _packet_residue_cells(
            frame_row["modulus"], baseline["row_count"],
            baseline["ell_freeze"], baseline["divisor_range"],
            direction, conductors, math.gcd(*conductors))
        for conductor, partner, category in families:
            transfer = _matched_doubled_packet(
                frame_row["modulus"], baseline["ell_freeze"], conductor,
                partner, direction, support)
            doubled_q = transfer["doubled_q"]
            actual = np.zeros(doubled_q, dtype=complex)
            for (denominator, residue), value in packets[category].items():
                if denominator == doubled_q:
                    actual[residue] += value
            prediction = transfer.pop("predicted_packet")
            absolute_error = float(np.max(np.abs(actual - prediction)))
            relative_error = float(np.max(
                np.abs(actual - prediction)
                / np.maximum(1.0, np.abs(actual))))
            rows.append({
                "prime_modulus": frame_row["modulus"],
                "conductor": conductor,
                "odd_partner": partner,
                "doubled_partner": 2 * partner,
                "packet_category": category,
                "packet_reconstruction_maximum_absolute_error": (
                    absolute_error),
                "packet_reconstruction_maximum_relative_error": (
                    relative_error),
                "nonzero_actual_packet_cell_count": int(np.count_nonzero(
                    np.abs(actual) > tolerance)),
                **transfer,
            })
    reconstruction_passes = all(
        row["packet_reconstruction_maximum_relative_error"] <= tolerance
        and row["diagonal_geometric_transfer_maximum_relative_error"]
        <= tolerance
        and row["unexpected_reduced_denominator_pair_count"] == 0
        and row["nonodd_doubled_residue_pair_count"] == 0
        for row in rows)
    return {
        "scale_modulus": scale_modulus,
        "families": families,
        "prime_count": len(baseline["rows"]),
        "tolerance": tolerance,
        "packet_transfer_rows": tuple(rows),
        "maximum_packet_reconstruction_absolute_error": max(
            row["packet_reconstruction_maximum_absolute_error"]
            for row in rows),
        "maximum_packet_reconstruction_relative_error": max(
            row["packet_reconstruction_maximum_relative_error"]
            for row in rows),
        "maximum_term_geometric_transfer_relative_error": max(
            row["diagonal_geometric_transfer_maximum_relative_error"]
            for row in rows),
        "unexpected_reduced_denominator_pair_count": sum(
            row["unexpected_reduced_denominator_pair_count"] for row in rows),
        "nonodd_doubled_residue_pair_count": sum(
            row["nonodd_doubled_residue_pair_count"] for row in rows),
        "exact_doubled_packet_diagonal_transfer_test_passes": bool(
            reconstruction_passes),
        "packet_diagonal_transfer_assigns_favorable_sign_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(partner_doubling_transfer_receipt())
