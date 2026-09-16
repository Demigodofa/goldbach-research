"""Reconcile the post-q286 Mobius target with existing boundary-operator work.

The post-q286 proof-engine triage correctly chose the Mobius incomplete
prime-row covariance route, but its smallest-next-test wording points at an
operator that older repository work had already derived.  This receipt prevents
future turns from rewinding the frontier: it recomputes small fixtures from the
existing operator chain and records the current theorem target.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lcm_sawtooth_active_full_gershgorin import (
    project_aggregate_gershgorin_receipt,
)
from lcm_sawtooth_axial_invariant import project_axial_invariant_receipt
from lcm_sawtooth_axial_moment_curve import (
    project_axial_moment_curve_receipt,
)
from lcm_sawtooth_axial_schur_energy import (
    project_axial_schur_energy_receipt,
)
from lcm_sawtooth_incomplete_frequency import (
    primitive_conductor_operator_receipt,
    project_prime_block_quadratic_scan,
)


EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "post-q286-mobius-frontier-reconciliation.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def build_receipt():
    operator = primitive_conductor_operator_receipt(
        101, 47, 47, 70, 4, 14)
    prime_block = project_prime_block_quadratic_scan(101)
    gershgorin = project_aggregate_gershgorin_receipt(127)
    axial_energy = project_axial_schur_energy_receipt(127)
    axial_invariant = project_axial_invariant_receipt(127)
    moment_curve = project_axial_moment_curve_receipt(127)

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "post_q286_triage": (
                "evidence/post-q286-proof-engine-triage.json"),
            "primitive_operator": "lcm_sawtooth_incomplete_frequency.py",
            "active_full_gershgorin": (
                "lcm_sawtooth_active_full_gershgorin.py"),
            "axial_schur_energy": "lcm_sawtooth_axial_schur_energy.py",
            "axial_invariant": "lcm_sawtooth_axial_invariant.py",
            "axial_moment_curve": "lcm_sawtooth_axial_moment_curve.py",
        },
        "status": "TARGET_mobius_six_coordinate_active_full_lower_frame",
        "status_boundary": (
            "frontier reconciliation only; it proves no uniform active/full "
            "lower frame, Mobius covariance theorem, signed prime-correlation "
            "estimate, q286 theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"),
        "goldbach_proved": False,
        "q286_reactivated": False,
        "mobius_covariance_theorem_proved": False,
        "signed_prime_correlation_proved": False,
        "boundary_operator_step_already_satisfied": {
            "exact_conductor_packet_identity_proved": (
                operator["exact_conductor_packet_identity_proved"]),
            "quadratic_log_conductor_span_rank": (
                operator["quadratic_log_conductor_span_rank"]),
            "actual_row_varying_energy_ratio": (
                operator["actual_row_varying_energy_ratio"]),
            "sharp_row_varying_quadratic_span_ratio": (
                operator["sharp_row_varying_quadratic_span_ratio"]),
            "uniform_conductor_operator_subpower_bound_proved": (
                operator["uniform_conductor_operator_subpower_bound_proved"]),
            "decision": (
                "Do not repeat the post-q286 wording as if the boundary "
                "operator remains to be derived.  The exact primitive "
                "frequency/operator reduction is already present; the "
                "unproved task is its uniform arithmetic bound."),
        },
        "prime_block_quadratic_span_evidence": {
            "scale_modulus": prime_block["scale_modulus"],
            "prime_count": prime_block["prime_count"],
            "maximum_sharp_varying_span_ratio": (
                prime_block["maximum_sharp_varying_span_ratio"]),
            "aggregate_prime_block_sharp_varying_span_ratio": (
                prime_block[
                    "aggregate_prime_block_sharp_varying_span_ratio"]),
            "aggregate_prime_block_actual_varying_ratio": (
                prime_block[
                    "aggregate_prime_block_actual_varying_ratio"]),
            "row_varying_quadratic_span_bound_proved": (
                prime_block["row_varying_quadratic_span_bound_proved"]),
        },
        "six_coordinate_lower_frame_evidence": {
            "scale_modulus": gershgorin["scale_modulus"],
            "prime_count": gershgorin["prime_count"],
            "gershgorin_lower_frame_bound": (
                gershgorin["gershgorin_lower_frame_bound"]),
            "exact_smallest_generalized_eigenvalue": (
                gershgorin["exact_smallest_generalized_eigenvalue"]),
            "one_half_lower_frame_certified": (
                gershgorin["one_half_lower_frame_certified"]),
            "uniform_active_full_lower_frame_proved": (
                gershgorin["uniform_active_full_lower_frame_proved"]),
        },
        "axial_schur_response_evidence": {
            "schur_margin": axial_energy["schur_margin"],
            "nonaxial_energy_error": axial_energy["nonaxial_energy_error"],
            "nonaxial_error_over_schur_margin": (
                axial_energy["nonaxial_error_over_schur_margin"]),
            "normalized_absolute_determinant": (
                axial_invariant["normalized_absolute_determinant"]),
            "determinant_axial_distance": (
                axial_invariant["determinant_axial_distance"]),
            "best_moment_curve_parameter": moment_curve["best_parameter"],
            "projective_moment_curve_distance": (
                moment_curve["projective_moment_curve_distance"]),
            "actual_selector_angle_degrees": (
                moment_curve["actual_selector_angle_degrees"]),
            "uniform_determinant_lower_bound_proved": (
                axial_invariant["uniform_determinant_lower_bound_proved"]),
            "effective_log_parameter_formula_proved": (
                moment_curve["effective_log_parameter_formula_proved"]),
        },
        "route_decision": {
            "active_frontier": (
                "six-coordinate active/full lower-frame theorem for the "
                "Mobius incomplete-row boundary, with the axial Schur-response "
                "pattern as the candidate compression"),
            "smallest_next_tests": [
                (
                    "prove or falsify uniform entrywise estimates for the "
                    "whitened aggregate active/full Gershgorin matrix"),
                (
                    "derive or falsify an explicit effective-log formula for "
                    "the moment-curve parameter in the axial Schur response"),
                (
                    "prove or falsify determinant/norm lower bounds and "
                    "nonaxial-energy upper bounds strong enough to preserve "
                    "the Schur margin"),
            ],
            "sleep_or_reservoir": [
                "post-q286 wording that says the boundary operator still needs derivation",
                "arbitrary-conductor-vector subpower route",
                "raw-coordinate Gershgorin",
                "fixed dyadic-centered raw-coordinate basis",
                "simple positive centroid formula for the effective log parameter",
            ],
            "why_this_changes_next_action": (
                "The first Mobius operator step is already present in the "
                "repository.  Continuing from the actual frontier means "
                "attacking the six-coordinate lower-frame/axial-response "
                "bounds, not rebuilding the boundary operator."),
        },
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
