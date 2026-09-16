"""Preserve the q286 signed-weight proof-engine sleep/HOLD boundary.

A sequence of q286-WBSS audits now blocks the unchanged proof-engine
conjunction:

* support-only positivity fails,
* normalized aggregate L2 is not a confirmed logical bridge,
* the principal local factor is T_N-dependent,
* no named pointwise signed-region source theorem pays the exact target.

This receipt preserves that negative result without discarding reusable
components.  It is a lane-level sleep/HOLD, not a proof of Goldbach and not a
global failure of the q286 coefficient structure.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
PRINCIPAL = EVIDENCE / "q286-wbss-signed-weight-principal-factor-audit.json"
L2_LOGICAL = EVIDENCE / "q286-wbss-zero-mass-l2-logical-bridge-audit.json"
FLOOR = EVIDENCE / "q286-wbss-single-weight-major-arc-floor-audit.json"
NEGATIVE = EVIDENCE / "q286-wbss-negative-region-mass-threshold-audit.json"
SOURCE_FIT = EVIDENCE / "q286-wbss-signed-region-source-fit-audit.json"
SIGNED_TARGET = EVIDENCE / "q286-wbss-signed-weight-circle-target.json"
K286_STRESS = (
    EVIDENCE / "q286-wbss-k286-quarter-residual-lift-depth-stress.json")
OUT = EVIDENCE / "q286-wbss-signed-weight-proof-engine-sleep-hold.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    principal = load_json(PRINCIPAL)
    l2 = load_json(L2_LOGICAL)
    floor = load_json(FLOOR)
    negative = load_json(NEGATIVE)
    source_fit = load_json(SOURCE_FIT)
    signed = load_json(SIGNED_TARGET)
    k286 = load_json(K286_STRESS)

    local_summary = principal["local_factor_summary"]
    obstruction = principal["signed_weight_obstruction_summary"]
    l2_failures = l2["observed_l2_failures"]
    k286_summary = k286["finite_stress"]["summary"]

    blocked_conjunctions = [
        {
            "id": "support_only_single_weight_positive_floor",
            "status": floor["status"],
            "blocked": True,
            "evidence": (
                "All 5005 even target residues have negative admissible "
                "q286 weights; zero have a pointwise positive floor."),
            "reactivate_only_if": (
                "A different signed weight or transformed residue support "
                "has an independently verified pointwise positive floor, or "
                "the route stops being support-only and supplies a raw "
                "signed-distribution theorem."),
        },
        {
            "id": "normalized_l2_as_bridge",
            "status": l2["status"],
            "blocked": True,
            "evidence": (
                "Observed normalized aggregate L2 has finite cap violations "
                f"on {l2_failures['row_local_cap_exceeding_row_count']} "
                "row-local checked rows and lacks a universal raw moment "
                "theorem."),
            "reactivate_only_if": (
                "A source-backed pointwise raw twisted binary-prime moment "
                "theorem is proved, with explicit threshold and finite "
                "remainder, or a materially different raw Hilbert norm target "
                "is derived."),
        },
        {
            "id": "principal_local_factor_as_independent_support",
            "status": principal["status"],
            "blocked": True,
            "evidence": (
                "M(a)>0 on all even residues, but the principal term is "
                "T_N*M(a); it vanishes when T_N=0."),
            "reactivate_only_if": (
                "A major/minor arc estimate proves a strict raw weighted "
                "witness directly, rather than using M(a) only after "
                "positive mass exists."),
        },
        {
            "id": "named_external_signed_region_bridge",
            "status": source_fit["status"],
            "blocked": True,
            "evidence": (
                "No currently named source theorem pays the exact pointwise, "
                "strict-central, log-weighted q286 signed-region inequality."),
            "reactivate_only_if": (
                "A primary-source theorem or derived corollary is found that "
                "matches the exact fixed finite-modulus signed binary-prime "
                "weight for every sufficiently large covered N."),
        },
    ]

    return {
        "schema_version": 1,
        "receipt": "q286-wbss-signed-weight-proof-engine-sleep-hold",
        "source_commit": source_commit(),
        "sources": {
            "signed_weight_principal_factor_audit": str(
                PRINCIPAL.relative_to(ROOT)),
            "signed_weight_principal_factor_status": principal["status"],
            "zero_mass_l2_logical_bridge_audit": str(
                L2_LOGICAL.relative_to(ROOT)),
            "zero_mass_l2_logical_bridge_status": l2["status"],
            "single_weight_major_arc_floor_audit": str(
                FLOOR.relative_to(ROOT)),
            "single_weight_major_arc_floor_status": floor["status"],
            "negative_region_mass_threshold_audit": str(
                NEGATIVE.relative_to(ROOT)),
            "negative_region_mass_threshold_status": negative["status"],
            "signed_region_source_fit_audit": str(
                SOURCE_FIT.relative_to(ROOT)),
            "signed_region_source_fit_status": source_fit["status"],
            "signed_weight_circle_target": str(
                SIGNED_TARGET.relative_to(ROOT)),
            "signed_weight_circle_status": signed["status"],
            "k286_quarter_residual_lift_depth_stress": str(
                K286_STRESS.relative_to(ROOT)),
            "k286_quarter_residual_status": k286["status"],
        },
        "status": "SLEEP_q286_signed_weight_proof_engine_until_raw_estimate",
        "question": (
            "After the support-floor, L2 bridge, principal-factor, and "
            "source-fit audits, should the unchanged q286 signed-weight "
            "proof-engine route remain active?"),
        "answer": (
            "No, not as a standalone proof engine.  The unchanged conjunction "
            "is blocked: support-only positivity fails, normalized L2 is not "
            "a confirmed raw bridge, local-factor positivity is T_N-dependent, "
            "and no named pointwise signed-region source theorem pays the "
            "exact target.  Preserve q286 as coefficient structure, finite "
            "calibration, visualization substrate, and a raw-witness theorem "
            "target, but sleep the proof-engine route until a genuinely raw "
            "pointwise estimate is supplied."),
        "sleep_scope": {
            "sleep_exact_family": (
                "q286 as proof engine via local-factor positivity, support-"
                "only signed weight, normalized aggregate L2, or named broad "
                "AP sources without an exact raw pointwise signed binary-"
                "prime theorem"),
            "not_slept": [
                "raw direct W_phi(N)>0 theorem target",
                "raw adverse_drag_raw(N)<local_main_raw(N) theorem target",
                "K_286 finite falsifier/calibration lane",
                "coefficient/visual structure for finding a new signed weight",
                "future primary-source pointwise weighted binary-prime theorem",
            ],
            "attention_state": "dormant_until_changed_condition",
            "epistemic_state": "supported_HOLD_for_exact_conjunction",
        },
        "blocked_conjunctions": blocked_conjunctions,
        "preserved_components": {
            "positive_local_factors": {
                "state": "supported_component_not_bridge",
                "minimum_M": local_summary["local_factor_M_summary"][
                    "minimum"],
                "maximum_M": local_summary["local_factor_M_summary"][
                    "maximum"],
                "use": (
                    "May still be the main coefficient in a raw weighted "
                    "circle-method estimate, but cannot create support alone."),
            },
            "signed_shape_margin": {
                "state": "supported_component_not_distribution_theorem",
                "shape_threshold_minimum": obstruction[
                    "shape_threshold_minimum"],
                "minimum_local_uniform_shape_margin": obstruction[
                    "minimum_local_uniform_shape_margin"],
                "use": (
                    "Useful target for a raw signed-region distribution "
                    "theorem; not itself a theorem about prime-pair mass."),
            },
            "k286_quarter_residual_calibration": {
                "state": "finite_falsifier_calibration",
                "row_count": k286_summary["row_count"],
                "max_companion_residual_fraction": k286_summary[
                    "companion_residual_fraction_summary"]["maximum"],
                "minimum_quarter_margin": k286_summary[
                    "quarter_residual_companion_margin_ratio_summary"][
                        "minimum"],
                "use": (
                    "Finite calibration for theorem-shape constants; not a "
                    "universal bound."),
            },
            "visualization_substrate": {
                "state": "reservoir",
                "use": (
                    "Linked 3D scatter/table may help notice structure; it "
                    "cannot replace a universal pointwise raw estimate."),
            },
        },
        "reactivation_triggers": [
            {
                "trigger": "raw_pointwise_weighted_binary_prime_theorem",
                "description": (
                    "A primary-source or repo-proved theorem gives a pointwise "
                    "major/minor arc estimate for the exact signed q286 "
                    "weight, every sufficiently large covered N, with finite "
                    "remainder."),
            },
            {
                "trigger": "materially_new_signed_weight",
                "description": (
                    "A new coefficient transformation changes the negative-"
                    "weight obstruction, the principal factor, or the raw "
                    "adverse-drag theorem target in a way the existing "
                    "falsifiers do not cover."),
            },
            {
                "trigger": "raw_moment_theorem_for_active_characters",
                "description": (
                    "A universal pointwise unnormalized active-character "
                    "moment theorem pays the aggregate L2 or signed witness "
                    "target without first assuming T_N>0."),
            },
            {
                "trigger": "explicit_positive_mass_theorem_labeled_as_such",
                "description": (
                    "A separate strict-central positive-mass theorem is "
                    "proved; q286 may then be reused honestly as conditional "
                    "distribution/control, not as the support-creating proof."),
            },
        ],
        "candidate": {
            "name": "q286 signed-weight proof-engine sleep boundary",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Preserve the failed conjunction as a no-good constraint "
                "while retaining its useful components and exact reactivation "
                "triggers."),
            "prediction": (
                "Future unchanged q286 local-factor, normalized L2, or "
                "support-only retries will not move the Goldbach bridge unless "
                "one of the raw reactivation triggers fires."),
            "falsifier": (
                "A raw pointwise signed weighted binary-prime theorem or a "
                "materially new signed weight outside the recorded no-good "
                "constraints reactivates the lane."),
            "smallest_next_action": (
                "Move attention to a different proof engine or a true raw "
                "circle-method estimate; keep q286 as a coefficient/visual "
                "reservoir."),
        },
        "decision": (
            "SLEEP_q286_signed_weight_proof_engine_until_raw_estimate.  The "
            "exact current q286 signed-weight proof-engine conjunction is "
            "dormant until a changed condition supplies a raw pointwise "
            "estimate, a materially new signed weight, or an explicitly "
            "labeled positive-mass theorem.  This preserves useful q286 "
            "components without letting finite diagnostics or normalized "
            "conditional statements masquerade as a Goldbach bridge."),
        "status_boundary": (
            "Lane-level sleep/HOLD only.  No signed-weight major/minor arc "
            "estimate, raw weighted witness theorem, active-character moment "
            "theorem, positive-mass theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof is "
            "established."),
        "signed_weight_major_arc_estimate_proved": False,
        "raw_weighted_witness_theorem_proved": False,
        "active_character_moment_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "blocked_conjunction_count": len(receipt["blocked_conjunctions"]),
        "reactivation_trigger_count": len(receipt["reactivation_triggers"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
