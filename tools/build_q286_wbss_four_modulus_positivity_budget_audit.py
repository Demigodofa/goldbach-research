"""Audit the sigma budget behind q286-WBSS four-modulus positivity.

The far-lift holdout falsified the narrower finite observation that adverse
iid-scale z stayed below 3.  This receipt records the correct normalization:

    positivity_budget_sigma = local_main / iid_standard_error

and

    positivity <=> iid_z_score > -positivity_budget_sigma
               <=> lambda_phi < 1.

This is finite diagnostic algebra on existing receipts.  It proves no
independence theorem, fixed-modulus equidistribution theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
INITIAL_SOURCE = (
    EVIDENCE / "q286-wbss-four-modulus-variance-scale-audit.json")
FAR_SOURCE = (
    EVIDENCE / "q286-wbss-four-modulus-variance-scale-far-lift-holdout.json")
OUT = EVIDENCE / "q286-wbss-four-modulus-positivity-budget-audit.json"
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from tools.build_q286_wbss_four_modulus_direct_holdout_decomposition import (  # noqa: E402
    load_json,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def enrich_row(source_name, row):
    standard_error = float(row["iid_standard_error"])
    local_main = float(row["local_uniform_main_term"])
    iid_z = float(row["iid_z_score"])
    budget = local_main / standard_error
    sigma_margin = float(row["actual_formula_expectation"]) / standard_error
    signed_budget_ratio = -iid_z / budget
    adverse_budget_ratio = max(0.0, signed_budget_ratio)
    return {
        "source_name": source_name,
        "target": int(row["target"]),
        "target_residue": int(row["target_residue"]),
        "target_mod_286": int(row["target_mod_286"]),
        "lift_index": int(row["lift_index"]),
        "source_positive_target": int(row["source_positive_target"]),
        "pair_count": int(row["pair_count"]),
        "local_uniform_main_term": local_main,
        "actual_formula_expectation": float(row["actual_formula_expectation"]),
        "iid_standard_error": standard_error,
        "iid_z_score": iid_z,
        "adverse_iid_z_score": float(row["adverse_iid_z_score"]),
        "lambda_phi": float(row["lambda_phi"]),
        "positivity_budget_sigma": float(budget),
        "positivity_margin_sigma": sigma_margin,
        "signed_budget_ratio": float(signed_budget_ratio),
        "adverse_budget_ratio": float(adverse_budget_ratio),
        "lambda_budget_abs_error": abs(
            signed_budget_ratio - float(row["lambda_phi"])),
        "actual_positive": bool(row["actual_positive"]),
        "z_below_three": bool(float(row["adverse_iid_z_score"]) < 3.0),
        "budget_clears_adverse_z": bool(
            float(row["adverse_iid_z_score"]) < budget),
        "signed_ratio_below_one": bool(signed_budget_ratio < 1.0 - TOLERANCE),
    }


def receipt_rows(source_name, receipt):
    return [
        enrich_row(source_name, row)
        for row in receipt["holdout"]["rows"]
    ]


def summarize_rows(rows):
    z_cap_failures = [
        row for row in rows if not row["z_below_three"]]
    budget_tightest = min(
        rows,
        key=lambda row: (row["positivity_margin_sigma"], row["target"]),
    )
    ratio_tightest = max(
        rows,
        key=lambda row: (row["signed_budget_ratio"], -row["target"]),
    )
    return {
        "row_count": len(rows),
        "actual_positive_count": sum(row["actual_positive"] for row in rows),
        "actual_nonpositive_count": sum(
            not row["actual_positive"] for row in rows),
        "z_below_three_failure_count": len(z_cap_failures),
        "budget_failure_count": sum(
            not row["budget_clears_adverse_z"] for row in rows),
        "signed_ratio_failure_count": sum(
            not row["signed_ratio_below_one"] for row in rows),
        "positivity_budget_sigma_summary": finite_summary(
            row["positivity_budget_sigma"] for row in rows),
        "positivity_margin_sigma_summary": finite_summary(
            row["positivity_margin_sigma"] for row in rows),
        "iid_z_score_summary": finite_summary(
            row["iid_z_score"] for row in rows),
        "adverse_iid_z_score_summary": finite_summary(
            row["adverse_iid_z_score"] for row in rows),
        "signed_budget_ratio_summary": finite_summary(
            row["signed_budget_ratio"] for row in rows),
        "adverse_budget_ratio_summary": finite_summary(
            row["adverse_budget_ratio"] for row in rows),
        "lambda_budget_abs_error_summary": finite_summary(
            row["lambda_budget_abs_error"] for row in rows),
        "tightest_sigma_margin_row": budget_tightest,
        "largest_signed_budget_ratio_row": ratio_tightest,
        "largest_z_cap_failure_rows": sorted(
            z_cap_failures,
            key=lambda row: (-row["adverse_iid_z_score"], row["target"]),
        )[:20],
        "largest_signed_budget_ratio_rows": sorted(
            rows,
            key=lambda row: (-row["signed_budget_ratio"], row["target"]),
        )[:20],
    }


def source_summaries(rows):
    result = {}
    for source_name in sorted({row["source_name"] for row in rows}):
        source_rows = [row for row in rows if row["source_name"] == source_name]
        result[source_name] = summarize_rows(source_rows)
    return result


def build_receipt():
    initial = load_json(INITIAL_SOURCE)
    far = load_json(FAR_SOURCE)
    rows = (
        receipt_rows("initial_residue_lift_holdout", initial)
        + receipt_rows("far_lift_holdout", far)
    )
    summary = summarize_rows(rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "initial_variance_scale_audit": str(
                INITIAL_SOURCE.relative_to(ROOT)),
            "initial_source_commit": initial["source_commit"],
            "far_lift_holdout": str(FAR_SOURCE.relative_to(ROOT)),
            "far_source_commit": far["source_commit"],
        },
        "status_boundary": (
            "finite q286-WBSS four-modulus positivity-budget audit only; "
            "algebraic normalization of existing finite receipts, no "
            "independence theorem, fixed-modulus equidistribution theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"),
        "goldbach_proved": False,
        "independence_theorem_proved": False,
        "fixed_modulus_equidistribution_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "four-modulus positivity sigma budget",
            "mechanism": (
                "Replace an absolute adverse-z ceiling by the row's available "
                "main-term sigma budget.  The exact finite relation is "
                "signed_budget_ratio = -iid_z / budget = lambda_phi, and "
                "positivity is signed_budget_ratio < 1."),
            "prediction": (
                "Rows may violate a fixed z<3 shortcut but still have large "
                "positive sigma margin because the local main term supplies a "
                "larger sigma budget."),
            "falsifier": (
                "Any row with nonpositive sigma margin, signed budget ratio "
                "at least 1, or mismatch from lambda_phi would falsify this "
                "finite algebraic checkpoint."),
            "smallest_test": (
                "Replay the initial and far-lift variance-scale receipts and "
                "compute budget, margin, and budget-ratio fields without new "
                "prime-orbit recomputation."),
            "novelty_label": "new-to-this-task",
        },
        "formula": {
            "positivity_budget_sigma": (
                "local_uniform_main_term / iid_standard_error"),
            "positivity_margin_sigma": (
                "actual_formula_expectation / iid_standard_error"),
            "signed_budget_ratio": (
                "-iid_z_score / positivity_budget_sigma"),
            "lambda_equivalence": (
                "signed_budget_ratio equals lambda_phi up to floating error"),
            "positivity_condition": (
                "positivity_margin_sigma > 0 iff signed_budget_ratio < 1"),
        },
        "holdout": {
            "source_count": 2,
            "target_count": len(rows),
            "summary": summary,
            "summary_by_source": source_summaries(rows),
            "rows": rows,
        },
        "z_below_three_cap_falsified": (
            summary["z_below_three_failure_count"] > 0),
        "positivity_budget_survives_combined_holdouts": (
            summary["budget_failure_count"] == 0
            and summary["signed_ratio_failure_count"] == 0),
        "decision": (
            "The fixed adverse-z cap is the wrong theorem target: it has "
            "finite failures.  The useful finite invariant is the positivity "
            "budget ratio, which is just lambda_phi in variance-scale "
            "coordinates.  On the combined 232 checked rows it remains below "
            "1 with numerical-zero reconstruction of the lambda relation, so "
            "the next theorem target is a signed estimate proving "
            "lambda_phi<1, equivalently adverse z below the row's growing "
            "main-term sigma budget.  This is finite algebraic evidence only; "
            "Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
