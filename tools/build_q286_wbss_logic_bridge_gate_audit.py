"""Classify the logical bridge status of q286-WBSS L2 and pointwise routes.

Kevin's correction is important: finite evidence is no longer an acceptance
condition, and an arithmetic audit is not automatically a logical bridge.  This
derived receipt separates:

* the finite zero-mass check;
* normalized L2 statements that only control existing prime-pair mass;
* the unnormalized pointwise adverse-drag theorem that would be a real bridge.

No L2 theorem, pointwise adverse-drag theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof is established.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-wbss-logic-bridge-gate-audit.json"

POINTWISE_SOURCE = (
    EVIDENCE / "q286-wbss-pointwise-adverse-drag-theorem-target.json")
ACTIVE_L2_SOURCE = (
    EVIDENCE / "q286-active-selector-l2-bridge-status-audit.json")
WBSS_L2_SOURCE = (
    EVIDENCE / "q286-wbss-multiplicative-character-l2-observed-moment-audit.json")
TRIAGE_SOURCE = EVIDENCE / "q286-non-circular-route-triage-audit.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    pointwise = load_json(POINTWISE_SOURCE)
    active_l2 = load_json(ACTIVE_L2_SOURCE)
    wbss_l2 = load_json(WBSS_L2_SOURCE)
    triage = load_json(TRIAGE_SOURCE)

    zero_mass = wbss_l2["zero_mass_check"]
    wbss_summary = wbss_l2["summary"]
    pointwise_acceptance = pointwise["acceptance_condition"]
    active_classification = active_l2["non_circularity_classification"]

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "pointwise_adverse_drag_target": str(
                POINTWISE_SOURCE.relative_to(ROOT)),
            "active_selector_l2_bridge_status": str(
                ACTIVE_L2_SOURCE.relative_to(ROOT)),
            "wbss_aggregate_l2_observed_moment": str(
                WBSS_L2_SOURCE.relative_to(ROOT)),
            "non_circular_route_triage": str(TRIAGE_SOURCE.relative_to(ROOT)),
        },
        "status": "TARGET_unnormalized_pointwise_bridge_not_L2_acceptance",
        "status_boundary": (
            "logical bridge gate only; no L2 discrepancy theorem, "
            "pointwise adverse-drag theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "l2_discrepancy_theorem_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "strict_central_prime_pair_existence_proved": False,
        "q286_threshold_theorem_proved": False,
        "universal_bound_open": True,
        "question": (
            "Does the finite zero-mass/L2 arithmetic audit actually confirm "
            "a non-circular bridge, or must the route be an unnormalized "
            "pointwise analytic estimate?"),
        "answer": (
            "The finite zero-mass check confirms only that the checked L2 "
            "failures are not normalization artifacts.  It does not confirm "
            "a non-circular bridge.  Normalized L2 can be a valid conditional "
            "distribution theorem for already-existing strict-central mass, "
            "but it cannot by itself create that mass.  The theorem-shaped "
            "acceptance gate is the unnormalized pointwise estimate "
            "adverse_drag(N)<local_main(N), with an explicit threshold and "
            "finite remainder."),
        "zero_mass_gate": {
            "finite_zero_mass_check_passed": (
                zero_mass["zero_pair_count"] == 0
                and zero_mass["zero_actual_mass_count"] == 0),
            "zero_pair_count": int(zero_mass["zero_pair_count"]),
            "zero_actual_mass_count": int(zero_mass["zero_actual_mass_count"]),
            "checked_rows": int(wbss_summary["row_count"]),
            "meaning": zero_mass["decision"],
            "bridge_consequence": (
                "This removes one finite diagnostic excuse for L2 cap "
                "failures.  It does not prove positivity for unobserved N, "
                "and it does not make a normalized L2 premise independent of "
                "strict-central mass."),
        },
        "normalized_l2_gate": {
            "valid_conditional_distribution_shape": bool(
                active_classification["valid_sufficient_implication"]),
            "non_circular_only_as_external_arithmetic_premise": bool(
                active_classification[
                    "non_circular_as_external_arithmetic_premise"]),
            "confirmed_by_current_work": bool(
                active_classification["confirmed_by_current_work"]),
            "proves_strict_central_existence": bool(
                active_classification["proves_strict_central_existence"]),
            "wbss_row_local_l2_cap_violations": int(
                wbss_summary["row_local_cap_exceeding_row_count"]),
            "wbss_global_minimum_l2_cap_violations": int(
                wbss_summary["global_min_cap_exceeding_row_count"]),
            "largest_row_local_ratio": float(
                wbss_summary["largest_row_local_ratio_row"][
                    "ratio_to_row_local_l2_cap"]),
            "largest_row_local_ratio_target": int(
                wbss_summary["largest_row_local_ratio_row"]["target"]),
            "classification": (
                "Do not use normalized L2 as a Goldbach bridge unless it is "
                "paired with an independent positive-mass theorem or replaced "
                "by an unnormalized estimate.  As currently stated, it can "
                "bound distribution of mass after mass exists; it does not "
                "prove the mass exists."),
        },
        "unnormalized_pointwise_gate": {
            "finite_evidence_is_acceptance_condition": bool(
                pointwise_acceptance["finite_evidence_is_acceptance_condition"]),
            "required_universal_statement": (
                pointwise_acceptance["required_universal_statement"]),
            "normalization_boundary": (
                pointwise_acceptance["normalization_boundary"]),
            "finite_remainder_requirement": (
                pointwise_acceptance["finite_remainder_requirement"]),
            "proof_obligations": pointwise["proof_obligations"],
            "why_this_is_the_bridge": (
                "It compares actual signed witness terms before dividing by "
                "strict-central prime-pair mass.  A proof of "
                "adverse_drag(N)<local_main(N) plus local_main(N)>0 forces a "
                "positive witness; if all strict-central prime-pair mass were "
                "zero, the positive unnormalized witness could not occur."),
        },
        "route_decision": {
            "finite_evidence_demoted_to": (
                "calibration, falsifier, and finite remainder after a theorem"),
            "l2_status": (
                "reservoir: arithmetically meaningful, not accepted as the "
                "bridge"),
            "active_acceptance_target": (
                "universal pointwise unnormalized adverse-drag inequality"),
            "smallest_next_theorem_move": (
                "Try to prove or falsify the unnormalized inequality "
                "A_-(N)<M(N) from fixed-modulus binary-prime correlation, "
                "or show that any available L2/character-moment theorem "
                "remains normalized by an unproved positive-mass term."),
            "triage_consistency": triage["route_decision"][
                "next_best_non_circular_target"],
        },
        "decision": (
            "The zero-mass check is real but finite.  The L2 target is not "
            "accepted as a non-circular bridge by current work: it is either "
            "a conditional distribution statement after strict-central mass "
            "exists, or it requires an external pointwise theorem not yet "
            "proved.  The active theorem gate is therefore the unnormalized "
            "pointwise estimate adverse_drag(N)<local_main(N) for every "
            "sufficiently large covered even N, plus a finite remainder."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
