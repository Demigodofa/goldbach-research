"""State the q286-WBSS pointwise adverse-drag theorem target.

Finite horizon and holdout receipts are no longer an acceptance condition for
the q286-WBSS route.  They calibrate and falsify candidate theorem shapes.  A
successful bridge needs a universal pointwise analytic estimate, in
unnormalized form, strong enough to imply positivity:

    adverse_drag(N) < local_main(N)

for every sufficiently large covered even N, followed by finite verification
below the threshold.

This receipt formalizes that acceptance condition and records the finite rows
only as calibration/falsifier evidence.  It proves no pointwise theorem,
q286 threshold theorem, strict-central Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
HORIZON_SOURCE = (
    EVIDENCE / "q286-wbss-four-modulus-adverse-drag-horizon-audit.json")
FRESH_SOURCE = (
    EVIDENCE
    / "q286-wbss-four-modulus-component-envelope-fresh-holdout.json")
OUT = EVIDENCE / "q286-wbss-pointwise-adverse-drag-theorem-target.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def finite_summary(values):
    vals = [float(value) for value in values]
    return {
        "count": len(vals),
        "minimum": min(vals),
        "mean": sum(vals) / len(vals),
        "maximum": max(vals),
    }


def calibration_row(row, source_name):
    return {
        "source": source_name,
        "target": int(row["target"]),
        "target_residue": int(row["target_residue"]),
        "target_mod_286": int(row["target_mod_286"]),
        "local_main": float(row["local_uniform_main_term"]),
        "actual_formula_expectation": float(row["actual_formula_expectation"]),
        "adverse_drag": float(row["negative_modulus_drag"]),
        "adverse_drag_ratio": float(row["negative_drag_ratio"]),
        "adverse_only_expectation": float(row["adverse_only_expectation"]),
        "lambda_phi": float(row["lambda_phi"]),
        "signed_error_by_modulus": {
            key: float(value)
            for key, value in row["signed_error_by_modulus"].items()
        },
    }


def calibration_rows(horizon, fresh):
    rows = [
        calibration_row(row, "adverse_drag_horizon")
        for row in horizon["holdout"]["rows"]
    ]
    rows.extend(
        calibration_row(row, "frozen_component_envelope_fresh_holdout")
        for row in fresh["holdout"]["rows"]
    )
    return rows


def summarize_rows(rows):
    return {
        "row_count": len(rows),
        "target_minimum": min(row["target"] for row in rows),
        "target_maximum": max(row["target"] for row in rows),
        "positive_actual_count": sum(
            row["actual_formula_expectation"] > 0.0 for row in rows),
        "adverse_drag_below_local_main_count": sum(
            row["adverse_drag"] < row["local_main"] for row in rows),
        "adverse_drag_not_below_local_main_count": sum(
            row["adverse_drag"] >= row["local_main"] for row in rows),
        "lambda_phi_below_one_count": sum(
            row["lambda_phi"] < 1.0 for row in rows),
        "local_main_summary": finite_summary(
            row["local_main"] for row in rows),
        "adverse_drag_summary": finite_summary(
            row["adverse_drag"] for row in rows),
        "adverse_drag_ratio_summary": finite_summary(
            row["adverse_drag_ratio"] for row in rows),
        "adverse_only_expectation_summary": finite_summary(
            row["adverse_only_expectation"] for row in rows),
        "lambda_phi_summary": finite_summary(
            row["lambda_phi"] for row in rows),
        "tightest_adverse_drag_row": max(
            rows,
            key=lambda row: (row["adverse_drag_ratio"], -row["target"]),
        ),
        "tightest_adverse_only_expectation_row": min(
            rows,
            key=lambda row: (
                row["adverse_only_expectation"], row["target"]),
        ),
        "largest_lambda_row": max(
            rows,
            key=lambda row: (row["lambda_phi"], -row["target"]),
        ),
    }


def build_receipt():
    horizon = load_json(HORIZON_SOURCE)
    fresh = load_json(FRESH_SOURCE)
    rows = calibration_rows(horizon, fresh)
    summary = summarize_rows(rows)
    fresh_excess = fresh["holdout"]["modulus_excess_summary"]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "adverse_drag_horizon_audit": str(
                HORIZON_SOURCE.relative_to(ROOT)),
            "adverse_drag_source_commit": horizon["source_commit"],
            "component_envelope_fresh_holdout": str(
                FRESH_SOURCE.relative_to(ROOT)),
            "fresh_holdout_source_commit": fresh["source_commit"],
        },
        "status_boundary": (
            "q286-WBSS pointwise adverse-drag theorem target only; finite "
            "rows are calibration and falsifier evidence, not acceptance. "
            "No pointwise adverse-drag theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "fixed_modulus_equidistribution_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "universal_bound_open": True,
        "acceptance_condition": {
            "finite_evidence_is_acceptance_condition": False,
            "required_universal_statement": (
                "There exist an explicit threshold N0 and an explicit covered "
                "even-target class such that, for every covered even N>=N0, "
                "adverse_drag(N) < local_main(N)."),
            "finite_remainder_requirement": (
                "After the universal statement is proved, all covered even "
                "targets below N0 must be verified by an independent finite "
                "remainder check."),
            "normalization_boundary": (
                "The acceptance target is unnormalized and pointwise: "
                "adverse_drag(N) and local_main(N) must be compared as "
                "actual terms in the q286-WBSS signed expectation, not merely "
                "as a fitted decimal or finite normalized ratio."),
        },
        "definitions": {
            "moduli": ["70", "130", "154", "286"],
            "local_main": (
                "M(N)=<u_a,phi_a>, where a=N mod 10010 and u_a is the local "
                "uniform strict-central orbit measure for the q286-WBSS "
                "coefficient phi_a."),
            "projected_errors": (
                "E_d(N)=<mu_N-u_a,phi_{a,d}> for d in {70,130,154,286}, "
                "with mu_N the actual strict-central binary-prime orbit "
                "measure and phi_a=sum_d phi_{a,d}+constant as in the "
                "four-modulus projection formula."),
            "adverse_drag": (
                "A_-(N)=sum_d max(0,-E_d(N))."),
            "sufficient_pointwise_inequality": (
                "A_-(N) < M(N) implies M(N)+sum_d E_d(N)>0, hence the "
                "q286-WBSS signed witness is positive for that N."),
        },
        "candidate": {
            "name": "unnormalized pointwise adverse-drag estimate",
            "mechanism": (
                "Replace finite fitted constants and row-local empirical "
                "passes with a source-backed analytic estimate that bounds "
                "the actual one-sided projected binary-prime drag by the "
                "local main term at each target."),
            "prediction": (
                "A real theorem will explain why the one-sided sum of "
                "negative projected errors cannot reach the local main term, "
                "even though individual fitted component constants can drift."),
            "falsifier": (
                "Any actual covered row with adverse_drag(N)>=local_main(N) "
                "falsifies this sufficient route.  A finite pass without a "
                "uniform analytic estimate does not satisfy the route."),
            "smallest_test": (
                "Formally separate the universal pointwise inequality from "
                "finite calibration, and carry forward the fresh modulus-286 "
                "constant failure as a warning against accepting fitted "
                "component constants."),
            "novelty_label": "new-to-this-task",
        },
        "finite_calibration": {
            "role": (
                "calibration_and_falsifier_only; not an acceptance condition"),
            "summary": summary,
            "fresh_fixed_component_constant_falsifier": {
                "individual_frozen_component_suprema_falsified": fresh[
                    "individual_frozen_component_suprema_falsified"],
                "rows_with_any_modulus_exceeding_frozen_supremum": fresh[
                    "holdout"]["summary"][
                        "rows_with_any_modulus_exceeding_frozen_supremum"],
                "modulus_286_exceeding_row_count": fresh_excess["286"][
                    "exceeding_row_count"],
                "modulus_286_fresh_maximum_row": fresh_excess["286"][
                    "fresh_maximum_row"],
            },
            "rows": rows,
        },
        "not_sufficient_for_acceptance": [
            "another finite horizon pass",
            "a fitted decimal residual absorption constant",
            "a fixed list of per-modulus constants copied from checked rows",
            "lambda_phi<1 on checked rows without a source-backed estimate",
            "agreement between normalized finite ratios and local intuition",
        ],
        "proof_obligations": [
            (
                "Define the covered even-target class without post-hoc "
                "reference to the checked rows."),
            (
                "Prove M(N)>0 on that class from the four-modulus projection "
                "formula or a stronger source-backed local-main theorem."),
            (
                "Prove A_-(N)<M(N) pointwise for every sufficiently large "
                "covered even N, using fixed-modulus binary-prime correlation "
                "or an equivalent signed-discrepancy estimate."),
            (
                "Provide an explicit threshold N0 and independently verify "
                "the finite remainder below N0."),
        ],
        "decision": (
            "Finite evidence is demoted from acceptance condition to "
            "calibration/falsifier.  The active q286-WBSS theorem target is "
            "now the unnormalized pointwise estimate adverse_drag(N) < "
            "local_main(N) for every sufficiently large covered even N, plus "
            "a finite remainder.  The fresh holdout already shows why fixed "
            "per-modulus constants fitted on a finite horizon are not the "
            "right theorem object.  Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
