"""Farther horizon holdout for the q286-WBSS aggregate lambda target.

The residual absorption and `11,13`-led splits failed as portable theorem
targets.  The surviving finite target is the aggregate four-modulus condition

    lambda_phi = -signed_projection_error / local_main < 1.

This receipt reuses the same stressed source residues, starts after the prior
far-lift maximum, and evaluates eight fresh period-lifts per residue.  It is
finite targeted evidence only.  It proves no signed concentration theorem,
fixed-modulus equidistribution theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import build_q286_wbss_four_modulus_variance_scale_far_lift_holdout as far


EVIDENCE = ROOT / "evidence"
PREVIOUS_SOURCE = (
    EVIDENCE / "q286-wbss-four-modulus-variance-scale-far-lift-holdout.json")
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
OUT = EVIDENCE / "q286-wbss-four-modulus-lambda-horizon-holdout.json"
HORIZON_LIFT_COUNT = 8
TOLERANCE = 1e-10


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def horizon_rows(previous, lift_count=HORIZON_LIFT_COUNT):
    return far.far_lift_rows(previous, lift_count=lift_count)


def summarize_horizon(rows):
    summary = far.summarize_rows(rows)
    summary["lambda_budget_failure_count"] = sum(
        row["lambda_phi"] >= 1.0 - TOLERANCE for row in rows)
    summary["positive_margin_ratio_summary"] = far.finite_summary(
        row["positivity_margin_ratio"] for row in rows)
    by_lift = {}
    for lift_index in sorted({row["lift_index"] for row in rows}):
        lift_rows = [row for row in rows if row["lift_index"] == lift_index]
        by_lift[str(lift_index)] = {
            "row_count": len(lift_rows),
            "actual_positive_count": sum(
                row["actual_positive"] for row in lift_rows),
            "lambda_phi_summary": far.finite_summary(
                row["lambda_phi"] for row in lift_rows),
            "adverse_iid_z_score_summary": far.finite_summary(
                row["adverse_iid_z_score"] for row in lift_rows),
            "minimum_expectation_row": min(
                lift_rows,
                key=lambda row: (
                    row["actual_formula_expectation"],
                    row["target"],
                ),
            ),
        }
    summary["summary_by_lift_index"] = by_lift
    return summary


def build_receipt():
    previous = far.load_json(PREVIOUS_SOURCE)
    formula = far.load_json(FORMULA_SOURCE)
    alpha0, by_modulus = far.coefficient_lookup(formula)
    edge_rows, lower_bound, source_residue_count = horizon_rows(previous)
    maximum_target = max(row["target"] for row in edge_rows)
    primes = np.asarray(far._prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = far.logs(maximum_target)
    context = far.prepare_support_context()
    context["coefficient"] = far.combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = far.period_full_unit_coefficients(context)
    first_three_coefficients = far.q286_first_three_unit_coefficients(context)
    rows = [
        far.row_variance_holdout(
            row,
            context,
            full_coefficients,
            first_three_coefficients,
            primes,
            prime_values,
            log_values,
            alpha0,
            by_modulus,
        )
        for row in edge_rows
    ]
    summary = summarize_horizon(rows)
    previous_summary = previous["holdout"]["summary"]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "previous_far_lift_holdout": str(PREVIOUS_SOURCE.relative_to(ROOT)),
            "previous_source_commit": previous["source_commit"],
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "formula_source_commit": formula["source_commit"],
        },
        "status_boundary": (
            "finite q286-WBSS aggregate-lambda farther horizon holdout only; "
            "no signed concentration theorem, fixed-modulus equidistribution "
            "theorem, q286 threshold theorem, strict-central Goldbach theorem, "
            "or Goldbach proof"),
        "goldbach_proved": False,
        "signed_concentration_theorem_proved": False,
        "fixed_modulus_equidistribution_theorem_proved": False,
        "universal_lambda_bound_proved": False,
        "universal_bound_open": True,
        "residual_absorption_constants_fit_finite_data_only": True,
        "candidate": {
            "name": "aggregate lambda horizon holdout",
            "mechanism": (
                "After the residual absorption splits failed, reuse the "
                "stressed source residues and test the unsplit four-modulus "
                "aggregate lambda condition farther past the previous "
                "far-lift maximum."),
            "prediction": (
                "If the aggregate route is more robust than the rowwise "
                "splits, direct positivity and lambda_phi < 1 should survive "
                "these fresh period-lifts even though no theorem is proved."),
            "falsifier": (
                "Any nonpositive direct witness row or any row with "
                "lambda_phi >= 1 falsifies this finite aggregate checkpoint. "
                "A new maximum lambda or z-score would tighten the theorem "
                "target even if positivity survives."),
            "smallest_test": (
                "Start after the prior far-lift maximum and evaluate the "
                "same 29 source residues for eight fresh period-lifts each."),
            "novelty_label": "new-to-this-task",
        },
        "previous_holdout": {
            "source_target_maximum": int(lower_bound),
            "row_count": previous_summary["row_count"],
            "maximum_lambda_phi": previous_summary[
                "lambda_phi_summary"]["maximum"],
            "maximum_adverse_iid_z_score": previous_summary[
                "adverse_iid_z_score_summary"]["maximum"],
        },
        "holdout": {
            "source_positive_residue_count": source_residue_count,
            "lift_count_per_residue": HORIZON_LIFT_COUNT,
            "target_count": len(rows),
            "target_minimum": min(row["target"] for row in rows),
            "target_maximum": maximum_target,
            "summary": summary,
            "rows": rows,
        },
        "direct_witness_survives_horizon_holdout": (
            summary["actual_nonpositive_count"] == 0),
        "lambda_budget_survives_horizon_holdout": (
            summary["lambda_budget_failure_count"] == 0),
        "previous_max_lambda_exceeded": (
            summary["lambda_phi_summary"]["maximum"]
            > previous_summary["lambda_phi_summary"]["maximum"]),
        "previous_max_adverse_z_exceeded": (
            summary["adverse_iid_z_score_summary"]["maximum"]
            > previous_summary["adverse_iid_z_score_summary"]["maximum"]),
        "decision": (
            "The farther horizon preserves the aggregate four-modulus "
            "lambda target on every checked row: the raw expectation stays "
            "positive and lambda_phi remains below 1.  Unlike the failed "
            "residual and 11,13-led splits, this does not require rowwise "
            "edge negativity.  It is still finite holdout evidence only; the "
            "open theorem target is a source-backed signed concentration or "
            "fixed-modulus equidistribution estimate proving lambda_phi < 1. "
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
