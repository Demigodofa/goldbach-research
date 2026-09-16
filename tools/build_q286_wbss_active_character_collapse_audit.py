"""Classify the q286 active-character route after source-fit closure.

After the Bauer-Wang source-fit audit, the q286 route has no named external
pointwise bridge.  The remaining question is whether the raw active-character
target is an executable next proof engine, or whether it is itself a
Goldbach-strength theorem target that should be slept until a genuinely new
raw estimate or proof engine appears.

This is a logical dependency audit.  It proves no character-moment theorem and
no Goldbach theorem.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
RAW_TARGET = EVIDENCE / "q286-wbss-raw-character-expansion-target.json"
SLEEP_HOLD = EVIDENCE / "q286-wbss-signed-weight-proof-engine-sleep-hold.json"
BAUER_WANG = EVIDENCE / "q286-wbss-bauer-wang-source-fit-audit.json"
SOURCE_SCOUT = EVIDENCE / "q286-wbss-raw-pointwise-source-scout.json"
PRINCIPAL = EVIDENCE / "q286-wbss-signed-weight-principal-factor-audit.json"
L2_LOGICAL = EVIDENCE / "q286-wbss-zero-mass-l2-logical-bridge-audit.json"
OUT = EVIDENCE / "q286-wbss-active-character-collapse-audit.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    raw = load_json(RAW_TARGET)
    sleep = load_json(SLEEP_HOLD)
    bauer = load_json(BAUER_WANG)
    scout = load_json(SOURCE_SCOUT)
    principal = load_json(PRINCIPAL)
    l2 = load_json(L2_LOGICAL)

    l2_shape = raw["sufficient_raw_theorem_shapes"]["aggregate_L2"]
    direct_shape = raw["sufficient_raw_theorem_shapes"]["direct_signed_sum"]
    coefficient = raw["coefficient_package"]
    local = principal["local_factor_summary"]["local_factor_M_summary"]

    route_rows = [
        {
            "id": "direct_signed_sum_W_phi_positive",
            "candidate_statement": direct_shape["statement"],
            "logical_status": "valid_but_goldbach_strength",
            "creates_support_if_proved": True,
            "why": (
                "W_phi(N) is a sum over strict-central prime-pair terms.  "
                "If W_phi(N)>0, at least one strict-central term is present, "
                "so the theorem implies strict-central Goldbach for the "
                "covered target."),
            "missing_input": (
                "a pointwise raw signed weighted binary-prime theorem for "
                "every sufficiently large covered N"),
        },
        {
            "id": "raw_aggregate_L2_less_than_TN_main",
            "candidate_statement": l2_shape["statement"],
            "logical_status": "non_circular_shape_but_theorem_missing",
            "creates_support_if_proved": True,
            "why": l2_shape["why"],
            "missing_input": (
                "a universal pointwise unnormalized active-character moment "
                "estimate strong enough to beat T_N*M(a)"),
        },
        {
            "id": "P0_scaled_major_arc_replacement",
            "candidate_statement": (
                "Replace T_N*M(a) by a positive predicted main P0_a(N)*M(a) "
                "and prove the q286 signed weighted sum has that positive "
                "main plus smaller error."),
            "logical_status": "possible_raw_theorem_but_unproved",
            "creates_support_if_proved": True,
            "why": (
                "A direct signed-weight major/minor arc theorem with positive "
                "P0-scale main would create support without first normalizing "
                "by T_N.  But no such binary-prime theorem is available in "
                "the repository or the checked source-fit path."),
            "missing_input": (
                "a bespoke fixed-modulus signed binary Goldbach major/minor "
                "arc estimate with explicit threshold and finite remainder"),
        },
        {
            "id": "normalized_character_distribution_after_TN_positive",
            "candidate_statement": (
                "Assume or prove T_N>0 first, then control normalized "
                "character moments or residue distribution."),
            "logical_status": "conditional_decoration",
            "creates_support_if_proved": False,
            "why": (
                "The normalized measure exists only after strict-central "
                "prime-pair mass is present.  It can refine a positive-mass "
                "theorem, but it cannot be the support-creating bridge."),
            "missing_input": (
                "a separate positive-mass theorem honestly labeled as "
                "Goldbach-strength input"),
        },
    ]

    return {
        "schema_version": 1,
        "receipt": "q286-wbss-active-character-collapse-audit",
        "source_commit": source_commit(),
        "sources": {
            "raw_character_expansion_target": str(
                RAW_TARGET.relative_to(ROOT)),
            "raw_character_expansion_status": raw["status"],
            "signed_weight_sleep_hold": str(SLEEP_HOLD.relative_to(ROOT)),
            "signed_weight_sleep_status": sleep["status"],
            "bauer_wang_source_fit_audit": str(BAUER_WANG.relative_to(ROOT)),
            "bauer_wang_source_fit_status": bauer["status"],
            "raw_pointwise_source_scout": str(SOURCE_SCOUT.relative_to(ROOT)),
            "raw_pointwise_source_scout_status": scout["status"],
            "signed_weight_principal_factor_audit": str(
                PRINCIPAL.relative_to(ROOT)),
            "signed_weight_principal_factor_status": principal["status"],
            "zero_mass_l2_logical_bridge_audit": str(
                L2_LOGICAL.relative_to(ROOT)),
            "zero_mass_l2_logical_bridge_status": l2["status"],
        },
        "status": (
            "SLEEP_active_character_route_until_independent_raw_theorem_"
            "or_new_engine"),
        "question": (
            "After closing named source-fit routes, should the raw "
            "active-character target remain the active q286 proof engine?"),
        "answer": (
            "No, not as an engine that lowers the problem.  The raw "
            "active-character target is logically clean only when stated as "
            "a strict unnormalized theorem, but proving that theorem would "
            "itself create strict-central Goldbach support for every covered "
            "target.  Without a new raw major/minor arc theorem, q286 remains "
            "coefficient structure and a conditional distribution tool."),
        "raw_active_character_package": {
            "active_complex_character_count": (
                coefficient["active_complex_character_count"]),
            "active_real_channel_count": (
                coefficient["active_real_channel_count"]),
            "aggregate_character_l2": coefficient[
                "aggregate_character_l2"],
            "normalized_l2_cap_when_mass_positive": coefficient[
                "aggregate_character_moment_l2_cap_normalized"],
            "minimum_local_factor_M": local["minimum"],
            "maximum_local_factor_M": local["maximum"],
        },
        "route_classification": route_rows,
        "source_fit_closure": {
            "checked_source_count": scout["fit_summary"][
                "checked_source_count"],
            "direct_raw_pointwise_bridge_count": scout["fit_summary"][
                "direct_raw_pointwise_bridge_count"],
            "bauer_wang_fit": bauer["fit_summary"][
                "fit_to_q286_raw_pointwise_trigger"],
            "bauer_wang_reactivates_lane": bauer["fit_summary"][
                "reactivates_q286_signed_weight_lane"],
            "meaning": (
                "The named AP-Goldbach source route is closed as a direct "
                "wake-up source for q286.  A future use would need a new "
                "derivation, not another metadata-level source fit."),
        },
        "logical_implications": {
            "W_phi_positive_implies_strict_central_support": True,
            "raw_L2_strict_inequality_implies_strict_central_support": True,
            "normalized_L2_requires_support_first": True,
            "principal_local_factor_creates_support_by_itself": False,
            "why_q286_does_not_lower_current_core": (
                "The remaining q286 theorem targets are support-creating raw "
                "binary-prime statements.  That is the same difficulty class "
                "as the missing pointwise strict-central positive-mass input, "
                "unless a new signed-weight major/minor arc estimate is "
                "actually supplied."),
        },
        "candidate": {
            "name": "q286 active-character route collapse classifier",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Treat q286 as asleep unless it supplies a raw positive "
                "weighted binary-prime theorem directly; normalized or "
                "T_N-dependent variants are preserved only as conditional "
                "tools after positive mass."),
            "prediction": (
                "Further unchanged q286 active-character work will restate a "
                "Goldbach-strength raw theorem target unless a new analytic "
                "estimate or a materially new signed weight changes the "
                "principal term."),
            "falsifier": (
                "An explicit raw signed-weight major/minor arc estimate with "
                "positive P0-scale main and smaller error, independent of a "
                "prior T_N>0 theorem, reactivates q286 as a proof engine."),
            "smallest_next_action": (
                "Switch to a proof engine whose first obligation is not "
                "already pointwise strict-central positivity, or state the "
                "raw signed-weight major/minor arc theorem as a separate "
                "Goldbach-strength target before attempting it."),
        },
        "decision": (
            "SLEEP_active_character_route_until_independent_raw_theorem_or_"
            "new_engine.  The raw active-character package remains useful "
            "structure, but it is not the active proof engine after the "
            "source-fit closure.  A direct W_phi(N)>0 or raw aggregate L2 "
            "theorem would be non-circular, but proving it would itself be a "
            "pointwise strict-central binary-prime theorem and therefore "
            "does not lower current core obligation.  The next evidence-"
            "bearing Goldbach move should therefore switch proof engines or "
            "introduce a genuinely new raw signed-weight theorem; more "
            "finite q286 evidence is not an acceptance condition."),
        "status_boundary": (
            "Logical dependency HOLD only.  No active-character moment "
            "theorem, signed-weight major/minor arc estimate, raw weighted "
            "witness theorem, positive-mass theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof is "
            "established."),
        "active_character_moment_theorem_proved": False,
        "signed_weight_major_arc_estimate_proved": False,
        "raw_weighted_witness_theorem_proved": False,
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
        "route_count": len(receipt["route_classification"]),
        "direct_raw_pointwise_bridge_count": (
            receipt["source_fit_closure"][
                "direct_raw_pointwise_bridge_count"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
