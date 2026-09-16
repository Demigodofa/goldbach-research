"""Quantify the source-theorem budget for q286 anti-landing.

The edge-minorant and anti-landing audits reduce a q286 rescue route to a
coefficient-weighted inequality:

    positive_rescue_contribution > negative_rescue_drag.

This receipt asks how sharp a future source-backed binary-prime landing
theorem would have to be.  It computes the relative slack tolerated by the
checked positive/negative contribution ratios.

Finite theorem-budget audit only.  It proves no anti-landing theorem, signed
binary-prime correlation theorem, q286 threshold theorem, strict-central
Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE = EVIDENCE / "q286-anti-landing-mass-balance-audit.json"
OUT = EVIDENCE / "q286-anti-landing-source-budget-audit.json"
TOLERANCE = 1e-12


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def finite_summary(values):
    finite = tuple(
        float(value) for value in values
        if value is not None and math.isfinite(float(value)))
    if not finite:
        return {"count": 0, "minimum": None, "mean": None, "maximum": None}
    return {
        "count": len(finite),
        "minimum": min(finite),
        "mean": math.fsum(finite) / len(finite),
        "maximum": max(finite),
    }


def budget_row(row):
    ratio = float(row["positive_to_negative_rescue_ratio"])
    if ratio <= 1.0 + TOLERANCE:
        positive_loss_budget = 0.0
        negative_inflation_budget = 0.0
        symmetric_relative_error_budget = 0.0
    else:
        positive_loss_budget = 1.0 - 1.0 / ratio
        negative_inflation_budget = ratio - 1.0
        symmetric_relative_error_budget = (ratio - 1.0) / (ratio + 1.0)
    return {
        **row,
        "positive_loss_budget_if_negative_exact": positive_loss_budget,
        "negative_inflation_budget_if_positive_exact": (
            negative_inflation_budget),
        "symmetric_relative_error_budget": symmetric_relative_error_budget,
        "needs_sub_percent_symmetric_control": bool(
            symmetric_relative_error_budget < 0.01),
        "needs_sub_five_percent_symmetric_control": bool(
            symmetric_relative_error_budget < 0.05),
        "source_theorem_interpretation": (
            "If a proof only knows P >= (1-eps)P_actual and "
            "D <= (1+eps)D_actual, this row survives when "
            "eps < (P/D-1)/(P/D+1)."),
    }


def summarize(bucket):
    return {
        "row_count": len(bucket),
        "mass_majority_fail_count": sum(
            not row["mass_majority_pass"] for row in bucket),
        "needs_sub_percent_symmetric_control_count": sum(
            row["needs_sub_percent_symmetric_control"] for row in bucket),
        "needs_sub_five_percent_symmetric_control_count": sum(
            row["needs_sub_five_percent_symmetric_control"] for row in bucket),
        "positive_to_negative_rescue_ratio_summary": finite_summary(
            row["positive_to_negative_rescue_ratio"] for row in bucket),
        "positive_loss_budget_if_negative_exact_summary": finite_summary(
            row["positive_loss_budget_if_negative_exact"] for row in bucket),
        "negative_inflation_budget_if_positive_exact_summary": finite_summary(
            row["negative_inflation_budget_if_positive_exact"]
            for row in bucket),
        "symmetric_relative_error_budget_summary": finite_summary(
            row["symmetric_relative_error_budget"] for row in bucket),
        "tightest_symmetric_budget_row": min(
            bucket,
            key=lambda row: (
                row["symmetric_relative_error_budget"], row["target"]),
        ),
        "tightest_positive_loss_budget_row": min(
            bucket,
            key=lambda row: (
                row["positive_loss_budget_if_negative_exact"],
                row["target"],
            ),
        ),
        "tightest_negative_inflation_budget_row": min(
            bucket,
            key=lambda row: (
                row["negative_inflation_budget_if_positive_exact"],
                row["target"],
            ),
        ),
    }


def build_receipt():
    source = load_json(SOURCE)
    rows = [budget_row(row) for row in source["target_rows"]]
    post = [row for row in rows if row["block_index_after_discovery"] >= 1]
    discovery = [
        row for row in rows if row["block_index_after_discovery"] < 1]
    tightest = sorted(
        post,
        key=lambda row: (
            row["symmetric_relative_error_budget"], row["target"]),
    )[:20]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "anti_landing_mass_balance_audit": str(SOURCE.relative_to(ROOT)),
            "anti_landing_source_commit": source["source_commit"],
        },
        "status": "HOLD_anti_landing_requires_near_sharp_source_control",
        "status_boundary": (
            "finite source-theorem budget audit only; no anti-landing "
            "theorem, signed binary-prime correlation theorem, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof"),
        "goldbach_proved": False,
        "anti_landing_theorem_proved": False,
        "signed_binary_prime_correlation_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "coefficient-weighted anti-landing source budget",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Treat the exact finite rescue as P>D, where P is positive "
                "rescue contribution and D is negative rescue drag.  Compute "
                "how much relative error a future source-backed theorem can "
                "tolerate while preserving P>D."),
            "prediction": (
                "If the route is genuinely near-sharp, the tightest rows "
                "will require percent-level or sub-percent control, making "
                "broad AP/L1-style estimates inadequate."),
            "falsifier": (
                "If all rows allow large symmetric relative error, then a "
                "coarse source-backed inequality might plausibly pay the "
                "anti-landing budget."),
            "smallest_test": (
                "Use the existing anti-landing mass-balance rows and compute "
                "one-sided and symmetric relative error budgets."),
        },
        "budget_formulas": {
            "positive_loss_if_negative_exact": (
                "P may be replaced by (1-eps)P while D is exact when "
                "eps < 1 - 1/(P/D)."),
            "negative_inflation_if_positive_exact": (
                "D may be replaced by (1+eps)D while P is exact when "
                "eps < P/D - 1."),
            "symmetric_relative_error": (
                "P >= (1-eps)P_actual and D <= (1+eps)D_actual imply "
                "P>D when eps < (P/D - 1)/(P/D + 1)."),
        },
        "summary": {
            "target_row_count": len(rows),
            "post_discovery_target_count": len(post),
            "discovery_target_count": len(discovery),
            "all_rows": summarize(rows),
            "post_discovery_rows": summarize(post),
            "discovery_rows": summarize(discovery),
            "tightest_post_discovery_source_budget_rows": tightest,
        },
        "decision": (
            "The coefficient-weighted anti-landing route is near-sharp.  On "
            "the post-discovery rows the tightest target is 94856, where "
            "P/D is about 1.0191444228.  A symmetric source theorem of the "
            "form P >= (1-eps)P_actual and D <= (1+eps)D_actual would need "
            "eps below about 0.00948145 on that row.  Therefore broad "
            "uniformity, mass-majority, and loose AP-count inputs cannot pay "
            "this bridge; a successful proof needs a sharp coefficient-"
            "weighted signed binary-prime landing estimate or a different "
            "direct witness argument.  Goldbach remains open."),
        "target_rows": rows,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
