"""Build the Mobius positive-range lower-frame / axial falsifier receipt.

This is a finite diagnostic for the post-q286 Mobius frontier.  It tests two
candidate theorem shapes:

* the rank-aware positive-range active/full lower frame;
* the axial Schur-response compression as a standalone certificate.

The first survives the checked nonvacuous scales.  The second fails because
the nonaxial energy can exceed the Schur margin even when the lower frame
itself remains strong.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lcm_sawtooth_active_full_gershgorin import (
    whitened_gershgorin_lower_frame_receipt,
)
from lcm_sawtooth_arithmetic_covariance_basis import (
    covariance_inverse_root,
    project_one_frequency_covariance,
)
from lcm_sawtooth_axial_invariant import axial_distance_from_determinant
from lcm_sawtooth_axial_moment_curve import (
    axial_moment_curve_fit_from_difference,
)
from lcm_sawtooth_axial_schur_energy import (
    best_axial_approximation,
    symmetric_matrix_coordinates,
)
from lcm_sawtooth_axial_schur_response import (
    lifted_symmetric_matrix,
)
from lcm_sawtooth_centered_basis_gershgorin import (
    symmetric_square_transform,
)
from lcm_sawtooth_lifted_endpoint_frame import (
    _generalized_psd_receipt,
    project_prime_block_lifted_endpoint_scan,
)
from lcm_sawtooth_trace_traceless_block_frame import (
    trace_traceless_transform,
)


OUTPUT = Path(
    "evidence/mobius-positive-range-lower-frame-axial-falsifier.json")
LOWER_FRAME_SCALES = (83, 101, 127, 149, 167, 191)
AXIAL_SCALES = (127, 149, 167, 191)
LOWER_FRAME_TARGET = 0.5


def _exception_receipt(exc):
    return {
        "ok": False,
        "exception_type": type(exc).__name__,
        "exception_message": str(exc),
    }


def positive_range_receipt(scale_modulus, frame):
    """Return active/full generalized data on the positive range of full."""
    active = np.asarray(frame["aggregate_active_window_residue_energy_gram"])
    full = np.asarray(frame["aggregate_full_residue_energy_gram"])
    comparison = _generalized_psd_receipt(active, full)
    nonvacuous = comparison["denominator_rank"] > 0
    certified = (
        nonvacuous
        and not comparison["numerator_positive_denominator_null_direction"]
        and comparison["smallest_generalized_eigenvalue"]
        >= LOWER_FRAME_TARGET)
    return {
        "scale_modulus": scale_modulus,
        "prime_count": frame["prime_count"],
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        "full_denominator_rank": comparison["denominator_rank"],
        "full_denominator_nullity": comparison["denominator_nullity"],
        "active_positive_full_null_direction": comparison[
            "numerator_positive_denominator_null_direction"],
        "largest_full_nullspace_active_eigenvalue": comparison[
            "largest_nullspace_numerator_eigenvalue"],
        "positive_range_smallest_generalized_eigenvalue": comparison[
            "smallest_generalized_eigenvalue"],
        "positive_range_largest_generalized_eigenvalue": comparison[
            "largest_generalized_eigenvalue"],
        "positive_range_nonvacuous": nonvacuous,
        "positive_range_one_half_certified": certified,
    }


def full_pd_whitened_receipt(scale_modulus, frame):
    """Try the stronger full-positive-definite whitening certificate."""
    try:
        receipt = whitened_gershgorin_lower_frame_receipt(
            frame["aggregate_active_window_residue_energy_gram"],
            frame["aggregate_full_residue_energy_gram"])
    except Exception as exc:  # noqa: BLE001 - receipt records exact failure.
        return {
            "scale_modulus": scale_modulus,
            **_exception_receipt(exc),
        }
    return {
        "scale_modulus": scale_modulus,
        "ok": True,
        "gershgorin_lower_frame_bound": receipt[
            "gershgorin_lower_frame_bound"],
        "exact_smallest_generalized_eigenvalue": receipt[
            "exact_smallest_generalized_eigenvalue"],
        "exact_largest_generalized_eigenvalue": receipt[
            "exact_largest_generalized_eigenvalue"],
        "whitened_diagonal": receipt["whitened_diagonal"],
        "gershgorin_radii": receipt["gershgorin_radii"],
        "gershgorin_lower_edges": receipt["gershgorin_lower_edges"],
        "one_half_lower_frame_certified": receipt[
            "one_half_lower_frame_certified"],
    }


def axial_receipt(scale_modulus, frame):
    """Return the axial Schur diagnostic for one scale."""
    covariance, _ = project_one_frequency_covariance(scale_modulus, frame)
    arithmetic_transform, _ = covariance_inverse_root(covariance)
    trace_traceless = trace_traceless_transform()
    transform = (
        symmetric_square_transform(arithmetic_transform)
        @ trace_traceless)
    active = np.asarray(frame["aggregate_active_window_residue_energy_gram"])
    full = np.asarray(frame["aggregate_full_residue_energy_gram"])
    difference = transform.T @ (active - .5 * full) @ transform
    difference = (difference + difference.T) / 2
    trace_value = float(difference[0, 0])
    cross = difference[0, 1:]
    traceless = difference[1:, 1:]
    if np.linalg.eigvalsh(traceless)[0] <= 0:
        raise ArithmeticError("traceless block must be positive definite")
    response = -np.linalg.solve(traceless, cross)
    response_tensor = lifted_symmetric_matrix(
        trace_traceless[:, 1:] @ response)
    axial_tensor, _, _ = best_axial_approximation(response_tensor)
    axial_response = trace_traceless[:, 1:].T @ symmetric_matrix_coordinates(
        axial_tensor)
    residual = axial_response - response
    schur_margin = trace_value + float(cross @ response)
    nonaxial_energy_error = float(residual @ traceless @ residual)
    axial_trial_value = float(
        trace_value + 2 * cross @ axial_response
        + axial_response @ traceless @ axial_response)
    invariant = axial_distance_from_determinant(response_tensor)
    moment = axial_moment_curve_fit_from_difference(
        difference, arithmetic_transform)
    standalone_certifies = (
        nonaxial_energy_error / schur_margin < 1)
    return {
        "scale_modulus": scale_modulus,
        "prime_count": frame["prime_count"],
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        "schur_margin": schur_margin,
        "axial_trial_value": axial_trial_value,
        "nonaxial_energy_error": nonaxial_energy_error,
        "nonaxial_error_over_schur_margin": (
            nonaxial_energy_error / schur_margin),
        "nonaxial_error_over_axial_trial_value": (
            nonaxial_energy_error / axial_trial_value),
        "determinant_axial_distance": invariant[
            "determinant_axial_distance"],
        "normalized_absolute_determinant": invariant[
            "normalized_absolute_determinant"],
        "moment_curve_parameter": moment["best_parameter"],
        "moment_curve_projective_distance": moment[
            "projective_moment_curve_distance"],
        "actual_selector_angle_degrees": moment[
            "actual_selector_angle_degrees"],
        "axial_standalone_schur_certificate": standalone_certifies,
    }


def build_receipt():
    frames = {
        scale: project_prime_block_lifted_endpoint_scan(scale)
        for scale in LOWER_FRAME_SCALES}
    lower_frame = [
        positive_range_receipt(scale, frames[scale])
        for scale in LOWER_FRAME_SCALES]
    full_pd = [
        full_pd_whitened_receipt(scale, frames[scale])
        for scale in LOWER_FRAME_SCALES]
    axial = [axial_receipt(scale, frames[scale]) for scale in AXIAL_SCALES]
    nonvacuous = [
        row for row in lower_frame if row["positive_range_nonvacuous"]]
    axial_failures = [
        row for row in axial
        if not row["axial_standalone_schur_certificate"]]
    full_pd_failures = [row for row in full_pd if not row["ok"]]
    return {
        "status": (
            "FALSIFY_axial_schur_compression_as_standalone_certificate__"
            "TARGET_positive_range_active_full_lower_frame"),
        "question": (
            "Does the six-coordinate active/full frontier reduce to a "
            "full-PD whitened Gershgorin theorem or an axial Schur-response "
            "certificate, or must the theorem be rank-aware on the positive "
            "range?"),
        "lower_frame_scales": LOWER_FRAME_SCALES,
        "axial_scales": AXIAL_SCALES,
        "target_lower_frame_constant": LOWER_FRAME_TARGET,
        "positive_range_results": lower_frame,
        "full_pd_whitened_gershgorin_results": full_pd,
        "axial_schur_results": axial,
        "positive_range_nonvacuous_scales": tuple(
            row["scale_modulus"] for row in nonvacuous),
        "positive_range_minimum_checked_eigenvalue": min(
            row["positive_range_smallest_generalized_eigenvalue"]
            for row in nonvacuous),
        "positive_range_one_half_survives_checked_nonvacuous_scales": all(
            row["positive_range_one_half_certified"]
            for row in nonvacuous),
        "full_pd_whitening_acceptance_condition_falsified_on_checked_scales": (
            bool(full_pd_failures)),
        "full_pd_whitening_failure_scales": tuple(
            row["scale_modulus"] for row in full_pd_failures),
        "axial_standalone_certificate_falsified_on_checked_scales": (
            bool(axial_failures)),
        "axial_failure_scales": tuple(
            row["scale_modulus"] for row in axial_failures),
        "largest_nonaxial_error_over_schur_margin": max(
            row["nonaxial_error_over_schur_margin"] for row in axial),
        "smallest_moment_curve_projective_distance": min(
            row["moment_curve_projective_distance"] for row in axial),
        "largest_moment_curve_projective_distance": max(
            row["moment_curve_projective_distance"] for row in axial),
        "decision": (
            "The axial moment-curve geometry remains useful structure, but "
            "it is not a standalone certificate: at several checked scales "
            "the nonaxial energy exceeds the Schur margin.  The active "
            "theorem target should be a rank-aware positive-range lower "
            "frame with nullspace control, not a naive full-PD whitening "
            "statement."),
        "goldbach_proved": False,
        "q286_reactivated": False,
        "mobius_covariance_theorem_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
        "finite_diagnostic_only": True,
    }


def main():
    receipt = build_receipt()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
