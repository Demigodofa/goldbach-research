"""Audit whether the q286 L2 target is a non-circular bridge.

Kevin flagged the key distinction: an arithmetic zero-mass check can pass
without establishing the logical bridge needed for Goldbach.  This receipt
separates three states:

* checked-row zero-mass normalization sanity,
* raw strict L2 non-circularity as a theorem shape,
* the still-missing universal pointwise raw L2 moment theorem.

It proves no aggregate L2 theorem, raw binary-prime theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
L2_PAYMENT = (
    EVIDENCE / "q286-wbss-multiplicative-character-l2-payment-audit.json")
OBSERVED_L2 = (
    EVIDENCE
    / "q286-wbss-multiplicative-character-l2-observed-moment-audit.json")
RAW_CHARACTER_TARGET = (
    EVIDENCE / "q286-wbss-raw-character-expansion-target.json")
STRICT_RAW_HOLD = (
    EVIDENCE / "q286-wbss-strict-raw-gap-analytic-hold.json")
SIGNED_WEIGHT_TARGET = (
    EVIDENCE / "q286-wbss-signed-weight-circle-target.json")
OUT = EVIDENCE / "q286-wbss-zero-mass-l2-logical-bridge-audit.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    l2_payment = load_json(L2_PAYMENT)
    observed = load_json(OBSERVED_L2)
    raw_target = load_json(RAW_CHARACTER_TARGET)
    strict_hold = load_json(STRICT_RAW_HOLD)
    signed_target = load_json(SIGNED_WEIGHT_TARGET)

    observed_summary = observed["summary"]
    l2_budget = l2_payment["character_l2_budget"]
    worst_row = observed_summary["largest_row_local_ratio_row"]
    raw_l2 = raw_target["sufficient_raw_theorem_shapes"]["aggregate_L2"]

    zero_mass_sanity_confirmed = (
        observed_summary["zero_pair_count"] == 0
        and observed_summary["zero_actual_mass_count"] == 0
        and observed_summary["nonunit_actual_mass_sum_count"] == 0
        and observed_summary["nonunit_uniform_mass_sum_count"] == 0
    )
    raw_strict_shape_noncircular = bool(raw_l2["non_circular"])
    l2_bridge_confirmed = (
        raw_target["raw_character_moment_theorem_proved"]
        and observed["aggregate_character_l2_bound_proved"]
    )

    return {
        "schema_version": 1,
        "receipt": "q286-wbss-zero-mass-l2-logical-bridge-audit",
        "source_commit": source_commit(),
        "sources": {
            "multiplicative_character_l2_payment_audit": str(
                L2_PAYMENT.relative_to(ROOT)),
            "multiplicative_character_l2_payment_status": l2_payment[
                "status"],
            "observed_l2_moment_audit": str(OBSERVED_L2.relative_to(ROOT)),
            "observed_l2_moment_status": observed["status"],
            "raw_character_expansion_target": str(
                RAW_CHARACTER_TARGET.relative_to(ROOT)),
            "raw_character_expansion_status": raw_target["status"],
            "strict_raw_gap_analytic_hold": str(
                STRICT_RAW_HOLD.relative_to(ROOT)),
            "strict_raw_gap_analytic_hold_status": strict_hold["status"],
            "signed_weight_circle_target": str(
                SIGNED_WEIGHT_TARGET.relative_to(ROOT)),
            "signed_weight_circle_status": signed_target["status"],
        },
        "status": "HOLD_l2_logical_bridge_not_confirmed",
        "question": (
            "Is the q286 aggregate L2 target actually confirmed as a "
            "non-circular bridge, or did only the arithmetic zero-mass "
            "sanity check pass?"),
        "answer": (
            "The zero-mass arithmetic sanity check is confirmed on the "
            "checked rows, and the raw strict aggregate-L2 theorem shape is "
            "non-circular in principle.  The bridge itself is not confirmed: "
            "the repository still lacks the required universal pointwise raw "
            "twisted binary-prime moment theorem, and the normalized observed "
            "L2 cap fails on many checked rows."),
        "zero_mass_check": {
            "checked_row_count": observed_summary["row_count"],
            "zero_pair_count": observed_summary["zero_pair_count"],
            "zero_actual_mass_count": observed_summary[
                "zero_actual_mass_count"],
            "nonunit_actual_mass_sum_count": observed_summary[
                "nonunit_actual_mass_sum_count"],
            "nonunit_uniform_mass_sum_count": observed_summary[
                "nonunit_uniform_mass_sum_count"],
            "arithmetic_sanity_confirmed_on_checked_rows": (
                zero_mass_sanity_confirmed),
            "scope": (
                "finite checked rows only; this does not prove positive mass "
                "or any universal theorem"),
        },
        "l2_bridge_classification": {
            "raw_strict_aggregate_l2_shape_is_noncircular": (
                raw_strict_shape_noncircular),
            "why_raw_strict_shape_is_noncircular": raw_l2["why"],
            "logical_bridge_confirmed": l2_bridge_confirmed,
            "reason_bridge_not_confirmed": (
                "No pointwise raw twisted binary-prime moment theorem is "
                "proved.  The existing observed L2 audit is finite and "
                "falsifies treating the displayed normalized cap as already "
                "valid on the checked scale."),
            "current_hold": strict_hold["status"],
        },
        "observed_l2_failures": {
            "row_count": observed_summary["row_count"],
            "global_min_cap_exceeding_row_count": observed_summary[
                "global_min_cap_exceeding_row_count"],
            "row_local_cap_exceeding_row_count": observed_summary[
                "row_local_cap_exceeding_row_count"],
            "max_target_exceeding_row_local_cap": observed_summary[
                "max_target_exceeding_row_local_cap"],
            "worst_row_local_ratio_target": worst_row["target"],
            "worst_row_local_ratio": worst_row[
                "ratio_to_row_local_l2_cap"],
            "worst_row_observed_aggregate_l2": worst_row[
                "aggregate_character_moment_l2"],
            "worst_row_local_l2_cap": worst_row["row_local_l2_cap"],
        },
        "coefficient_l2_target": {
            "aggregate_coefficient_l2": l2_budget[
                "aggregate_character_l2"],
            "global_minimum_local_main_cap": l2_budget[
                "aggregate_character_moment_l2_cap"],
            "raw_sufficient_statement": raw_l2["statement"],
            "normalized_equivalent_when_mass_positive": raw_l2[
                "normalized_equivalent_when_T_N_positive"],
        },
        "acceptance_condition": {
            "finite_evidence_is_acceptance_condition": False,
            "required_for_acceptance": (
                "Prove a universal pointwise unnormalized estimate such as "
                "C2*sqrt(sum|D_raw_{d,chi}(N)|^2) < T_N*M(a), or directly "
                "prove W_phi(N)>0, for every sufficiently large covered N; "
                "then verify the finite remainder."),
            "invalid_substitutes": [
                "checked-row zero-mass sanity",
                "normalized L2 cap after assuming T_N>0",
                "finite L2 observations",
                "fitted residual constants",
                "almost-all or averaged AP-Goldbach estimates",
            ],
        },
        "candidate": {
            "name": "raw aggregate-L2 logical bridge gate",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Gate future q286 L2 work on whether it proves a strict raw "
                "inequality that fails at zero support, instead of "
                "normalizing by mass first."),
            "prediction": (
                "A real bridge will create strict-central support inside the "
                "raw inequality; a merely normalized estimate will need "
                "positive mass imported first."),
            "falsifier": (
                "If a proposed L2 proof starts by assuming or separately "
                "proving T_N>0 before q286 enters, the q286 L2 lane has "
                "collapsed to a conditional distribution tool."),
            "smallest_next_action": (
                "Attempt the signed-weight major-arc local-factor "
                "decomposition and mark whether its positive term is raw or "
                "only T_N times a conditional normalized mean."),
        },
        "decision": (
            "HOLD_l2_logical_bridge_not_confirmed.  The zero-mass arithmetic "
            "audit is good on the checked rows, and the raw strict aggregate "
            "L2 target is non-circular as a theorem shape.  But the logical "
            "bridge is not established: no universal pointwise raw L2 moment "
            "theorem is proved, and the observed normalized cap has finite "
            "violations.  Future L2 work must stay raw and strict or be "
            "labeled conditional on a separate positive-mass theorem."),
        "status_boundary": (
            "Logical bridge audit only.  No aggregate L2 theorem, raw "
            "twisted binary-prime theorem, signed-weight circle-method "
            "estimate, positive-mass theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof is "
            "established."),
        "aggregate_l2_theorem_proved": False,
        "raw_twisted_binary_prime_theorem_proved": False,
        "signed_weight_circle_method_estimate_proved": False,
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
        "zero_mass_sanity_confirmed": receipt["zero_mass_check"][
            "arithmetic_sanity_confirmed_on_checked_rows"],
        "raw_l2_shape_noncircular": receipt["l2_bridge_classification"][
            "raw_strict_aggregate_l2_shape_is_noncircular"],
        "logical_bridge_confirmed": receipt["l2_bridge_classification"][
            "logical_bridge_confirmed"],
        "row_local_cap_violations": receipt["observed_l2_failures"][
            "row_local_cap_exceeding_row_count"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
