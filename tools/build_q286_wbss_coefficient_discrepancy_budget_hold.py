"""Record the q286-WBSS coefficient-discrepancy theorem obligation.

The active q286-WBSS target is no longer another finite pass.  A proof route
needs a universal, pointwise, unnormalized estimate proving

    adverse_drag(N) < local_main(N)

for every sufficiently large covered even N, plus finite remainder
verification.  This receipt turns that target into an exact coefficient
discrepancy budget and records the current state as HOLD: the required
fixed-modulus binary-prime discrepancy theorem is not present.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
POINTWISE_SOURCE = (
    EVIDENCE / "q286-wbss-pointwise-adverse-drag-theorem-target.json")
OUT = EVIDENCE / "q286-wbss-coefficient-discrepancy-budget-hold.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def coefficient_budget(formula):
    projection = formula["projection_error_budget"]
    l1_by_modulus = {
        str(modulus): float(value)
        for modulus, value in projection["l1_norm_by_modulus"].items()
    }
    l1_total = sum(l1_by_modulus.values())
    min_main = float(projection["minimum_local_uniform_main_term"])
    equal_eta = min_main / l1_total
    return {
        "moduli": ["70", "130", "154", "286"],
        "l1_norm_by_modulus": l1_by_modulus,
        "total_l1_norm": l1_total,
        "minimum_local_main_over_even_residues": min_main,
        "global_equal_residue_error_cap": equal_eta,
        "source_global_equal_residue_error_cap": float(
            projection["sufficient_uniform_projection_error_bound"]),
        "worst_even_residue_local_main_row": projection[
            "worst_local_uniform_row"],
        "derivation": (
            "For each modulus d, write "
            "Delta_{d,s}(N)=Pi_{N,d}(s)-U_{a,d}(s).  If "
            "|Delta_{d,s}(N)|<=eta_d(N) for every projected residue s, then "
            "|E_d(N)|<=L1_d*eta_d(N).  Therefore "
            "adverse_drag(N)<=sum_d L1_d*eta_d(N)."),
        "direct_sufficient_inequality": (
            "sum_d L1_d*eta_d(N) < local_main(N)"),
        "component_bound_template": (
            "Equivalently, any pointwise one-sided bounds "
            "max(0,-E_d(N))<=B_d(N) are enough when "
            "sum_d max(0,B_d(N)) < local_main(N)."),
        "strong_uniform_corollary": (
            "The stronger target |Delta_{d,s}(N)| < "
            "0.0016192946592982506 for every d,s and every sufficiently "
            "large covered N would imply the coefficient-budget inequality "
            "on every even residue, using the current four-modulus formula."),
    }


def finite_context(pointwise):
    summary = pointwise["finite_calibration"]["summary"]
    tightest = summary["tightest_adverse_drag_row"]
    falsifier = pointwise["finite_calibration"][
        "fresh_fixed_component_constant_falsifier"]
    return {
        "finite_evidence_is_acceptance_condition": False,
        "role": "calibration_and_falsifier_only",
        "checked_row_count": int(summary["row_count"]),
        "target_minimum": int(summary["target_minimum"]),
        "target_maximum": int(summary["target_maximum"]),
        "checked_rows_with_adverse_drag_below_local_main": int(
            summary["adverse_drag_below_local_main_count"]),
        "tightest_known_adverse_drag_target": int(tightest["target"]),
        "tightest_known_adverse_drag_ratio": float(
            tightest["adverse_drag_ratio"]),
        "tightest_known_adverse_drag": float(tightest["adverse_drag"]),
        "tightest_known_local_main": float(tightest["local_main"]),
        "tightest_known_adverse_only_expectation": float(
            tightest["adverse_only_expectation"]),
        "frozen_component_constants_rejected": bool(
            falsifier["individual_frozen_component_suprema_falsified"]),
        "modulus_286_exceeding_row_count": int(
            falsifier["modulus_286_exceeding_row_count"]),
    }


def build_receipt():
    formula = load_json(FORMULA_SOURCE)
    pointwise = load_json(POINTWISE_SOURCE)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "four_modulus_projection_formula_source_commit": formula[
                "source_commit"],
            "pointwise_adverse_drag_target": str(
                POINTWISE_SOURCE.relative_to(ROOT)),
            "pointwise_adverse_drag_target_source_commit": pointwise[
                "source_commit"],
        },
        "status": "HOLD_for_pointwise_prime_pair_correlation_estimate",
        "status_boundary": (
            "coefficient-discrepancy theorem obligation only; current "
            "finite rows calibrate and falsify candidate theorem shapes but "
            "do not prove a universal pointwise estimate. No fixed-modulus "
            "binary-prime discrepancy theorem, pointwise adverse-drag "
            "theorem, q286 threshold theorem, strict-central Goldbach "
            "theorem, or Goldbach proof is established"),
        "goldbach_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "fixed_modulus_binary_prime_discrepancy_theorem_proved": False,
        "fixed_modulus_equidistribution_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "universal_bound_open": True,
        "acceptance_condition": {
            "required_statement": (
                "For every sufficiently large covered even N, prove the "
                "unnormalized pointwise inequality "
                "adverse_drag(N) < local_main(N), then verify the finite "
                "remainder below the explicit threshold."),
            "finite_evidence_is_acceptance_condition": False,
            "normalization_boundary": (
                "The comparison is between raw terms in the q286-WBSS "
                "signed expectation scale, not a fitted finite ratio such "
                "as .125, .126, or .13."),
        },
        "definitions": {
            "projected_residue_discrepancy": (
                "Delta_{d,s}(N)=Pi_{N,d}(s)-U_{a,d}(s), where a=N mod "
                "10010, Pi is the actual strict-central binary-prime left "
                "prime residue mass modulo d, and U is the matching local "
                "uniform residue mass."),
            "projected_error": (
                "E_d(N)=sum_s c_{d,s}(a)*Delta_{d,s}(N)."),
            "adverse_drag": (
                "A_-(N)=sum_d max(0,-E_d(N))."),
            "local_main": "M(N)=local_main(N)=<u_a,phi_a>.",
        },
        "coefficient_budget": coefficient_budget(formula),
        "finite_context": finite_context(pointwise),
        "missing_theorem": {
            "name": (
                "pointwise fixed-modulus binary-prime residue discrepancy "
                "estimate"),
            "needed_form": (
                "Prove explicit functions eta_d(N), or sharper one-sided "
                "B_d(N), from analytic number theory rather than from the "
                "checked rows."),
            "sufficient_eta_condition": (
                "sum_d L1_d*eta_d(N) < local_main(N) for every sufficiently "
                "large covered even N."),
            "sufficient_one_sided_condition": (
                "sum_d max(0,B_d(N)) < local_main(N), where "
                "max(0,-E_d(N)) <= B_d(N) is proved pointwise."),
            "current_source_status": (
                "No source-backed theorem in this repository proves either "
                "condition for all sufficiently large covered even N."),
        },
        "rejected_acceptance_substitutes": [
            "more finite q286 rows",
            "a fitted residual absorption constant",
            "frozen per-modulus adverse constants copied from checked rows",
            "lambda_phi<1 on checked rows",
            "a theorem stated only for average or almost-all N",
            "a normalized finite ratio without an unnormalized pointwise bound",
        ],
        "candidate": {
            "name": "coefficient-weighted discrepancy budget",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Translate adverse drag into weighted residue-discrepancy "
                "control using the exact four-modulus coefficient L1 norms."),
            "prediction": (
                "A valid proof must pay either a direct one-sided budget "
                "for E_d(N) or a stronger per-residue discrepancy budget; "
                "finite fitted constants will continue to drift."),
            "falsifier": (
                "A covered even N with adverse_drag(N)>=local_main(N) "
                "falsifies this q286-WBSS sufficient route. A published or "
                "proved discrepancy bound weaker than the displayed budget "
                "does not close it."),
            "smallest_test": (
                "Try to source or prove eta_d(N) bounds for d=70,130,154,286 "
                "that beat the displayed coefficient budget pointwise."),
        },
        "decision": (
            "The q286-WBSS bridge now has an exact analytic payment request: "
            "prove a pointwise coefficient-discrepancy budget strong enough "
            "that sum_d L1_d*eta_d(N) < local_main(N), or prove the sharper "
            "one-sided bounds sum_d max(0,B_d(N)) < local_main(N). The "
            "current repository does not contain that theorem, so the state "
            "is HOLD for a pointwise prime-pair correlation estimate. "
            "Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
