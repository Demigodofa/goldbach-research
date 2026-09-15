"""Aggregate L2 character-payment budget for the q286-WBSS target.

The character-payment audit used an equal L-infinity cap on every active
multiplicative-character moment.  This receipt asks whether a stronger theorem
shape, an aggregate L2 bound on the active character moments, would give a
meaningfully looser analytic payment target.

It does.  This is still only coefficient algebra: the required aggregate L2
character-moment theorem is not proved here.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
PAYMENT_SOURCE = (
    EVIDENCE / "q286-wbss-multiplicative-character-payment-audit.json")
OUT = EVIDENCE / "q286-wbss-multiplicative-character-l2-payment-audit.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    payment = load_json(PAYMENT_SOURCE)
    minimum_local_main = payment["minimum_local_main"]
    per_modulus = payment["character_budget"]["per_modulus"]
    character_l2_by_modulus = {
        modulus: row["character_l2"]
        for modulus, row in per_modulus.items()
    }
    aggregate_l2_square = sum(
        value * value for value in character_l2_by_modulus.values())
    aggregate_character_l2 = math.sqrt(aggregate_l2_square)
    aggregate_l2_cap = minimum_local_main / aggregate_character_l2
    l_infinity_cap = payment["character_budget"][
        "equal_character_moment_cap"]
    residue_cap = payment["residue_budget"]["equal_residue_error_cap"]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "multiplicative_character_payment_audit": str(
                PAYMENT_SOURCE.relative_to(ROOT)),
            "multiplicative_character_payment_status": payment["status"],
        },
        "status": "HOLD_aggregate_character_l2_bound_required",
        "status_boundary": (
            "finite coefficient Hilbert-budget audit only; it proves no "
            "aggregate character-moment theorem, pointwise adverse-drag "
            "theorem, q286 threshold theorem, strict-central Goldbach theorem, "
            "or Goldbach proof"),
        "goldbach_proved": False,
        "aggregate_character_l2_bound_proved": False,
        "character_moment_bound_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "universal_bound_open": True,
        "acceptance_condition": {
            "finite_evidence_is_acceptance_condition": False,
            "required_acceptance_condition": (
                "a universal pointwise unnormalized aggregate L2 "
                "multiplicative-character moment estimate"),
            "sufficient_statement": (
                "For every sufficiently large eligible even N, prove "
                "sqrt(sum_d ||D_d(N)||_2^2) < aggregate_l2_cap, where D_d "
                "is the active multiplicative-character moment vector in the "
                "same unnormalized residue-mass scale."),
            "target": "AdverseDrag(N) < LocalMain(N)",
        },
        "method": {
            "cauchy_budget": (
                "For each modulus, |E_d(N)| <= ||c_hat_d||_2 ||D_d(N)||_2. "
                "Therefore adverse_drag(N) <= "
                "sqrt(sum_d ||c_hat_d||_2^2) * "
                "sqrt(sum_d ||D_d(N)||_2^2)."),
            "interpretation_boundary": (
                "This replaces an all-character L-infinity moment cap with "
                "an aggregate active-character L2 moment theorem.  The "
                "analytic theorem is still missing."),
        },
        "minimum_local_main": minimum_local_main,
        "character_l2_budget": {
            "character_l2_by_modulus": character_l2_by_modulus,
            "aggregate_character_l2_square": aggregate_l2_square,
            "aggregate_character_l2": aggregate_character_l2,
            "aggregate_character_moment_l2_cap": aggregate_l2_cap,
            "relaxation_factor_vs_character_linf_cap": (
                aggregate_l2_cap / l_infinity_cap),
            "relaxation_factor_vs_residue_linf_cap": (
                aggregate_l2_cap / residue_cap),
            "single_modulus_l2_cap_if_paid_alone": {
                modulus: minimum_local_main / value
                for modulus, value in character_l2_by_modulus.items()
            },
        },
        "candidate": {
            "name": "aggregate active-character L2 moment theorem",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use Cauchy in the full active multiplicative-character "
                "Hilbert space instead of demanding a uniform bound on every "
                "character moment separately."),
            "prediction": (
                "The aggregate L2 payment cap should be materially looser "
                "than the character L-infinity cap."),
            "falsifier": (
                "If aggregate Cauchy gives little or no relaxation, this "
                "theorem shape adds no value over the previous payment audit."),
            "smallest_test": (
                "Compute sqrt(sum ||c_hat_d||_2^2) and compare the resulting "
                "moment cap to the character L-infinity and residue caps."),
        },
        "decision": (
            "The aggregate active-character L2 theorem shape is materially "
            "better than the equal character-moment cap.  The coefficient "
            "Hilbert norm is about 5.5251, so an aggregate active-character "
            "moment L2 bound below about 0.109307 would pay the minimum local "
            "main.  This is about 8.90 times looser than the character "
            "L-infinity cap and about 67.5 times looser than the per-residue "
            "cap.  The route is now sharper, but still requires a universal "
            "pointwise aggregate fixed-modulus twisted binary-prime moment "
            "estimate; no such theorem is proved here."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
