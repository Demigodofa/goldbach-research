"""Audit the finite scope of the Q=46189 replacement-family target.

The Q=46189 group-payment audit found a sharp payment pattern, but a theorem
target needs to know whether that pattern has multiple adverse middle/far
examples or only one current exemplar.  This derived receipt reads the existing
source-start and sigma-band clearance receipts and records the boundary.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-replacement-family-scope-boundary-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-replacement-family-scope-boundary-audit.md")
SOURCE_CLEARANCE = (
    Path("evidence")
    / "mobius-moment-square-degree5-source-margin-clearance-family-audit.json")
BAND_CLEARANCE = (
    Path("evidence")
    / "mobius-moment-square-degree5-band-clearance-holdout.json")
Q46189_PAYMENT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-group-payment-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def extract_rows(receipt, summary_key, count_key):
    rows = []
    for summary in receipt[summary_key]:
        counts = {
            family: summary["family_summaries"][family]["negative_count"]
            for family in ("near_1_to_2", "middle_2_to_3", "far_3_plus")
        }
        middle_negative = summary["family_summaries"]["middle_2_to_3"][
            "largest_negative"]
        rows.append({
            "band": summary.get("band"),
            "scale_modulus": summary["scale_modulus"],
            "prime_modulus": summary["prime_modulus"],
            "weakest_label": summary["weakest_label"],
            "negative_counts": counts,
            "middle_far_negative_count": (
                counts["middle_2_to_3"] + counts["far_3_plus"]),
            "largest_middle_negative": middle_negative,
            "near_negative_abs": summary["near_negative_abs"],
            "middle_far_positive_margin_sum": (
                summary["middle_far_positive_margin_sum"]),
            "near_negative_over_middle_far_positive": (
                summary["near_negative_abs"]
                / summary["middle_far_positive_margin_sum"]
                if summary["middle_far_positive_margin_sum"] else None),
        })
    middle_far_rows = [
        row for row in rows if row["middle_far_negative_count"] > 0]
    return {
        "checked_row_count": receipt[count_key],
        "negative_denominator_family_counts": (
            receipt["negative_denominator_family_counts"]),
        "middle_far_negative_row_count": len(middle_far_rows),
        "middle_far_negative_rows": middle_far_rows,
        "rows": rows,
        "maximum_near_negative_over_middle_far_positive": (
            receipt["maximum_near_negative_over_middle_far_positive"]),
    }


def same_middle_far_exception(source_scope, band_scope):
    source_rows = source_scope["middle_far_negative_rows"]
    band_rows = band_scope["middle_far_negative_rows"]
    if len(source_rows) != 1 or len(band_rows) != 1:
        return False
    source_negative = source_rows[0]["largest_middle_negative"]
    band_negative = band_rows[0]["largest_middle_negative"]
    return (
        source_rows[0]["scale_modulus"] == band_rows[0]["scale_modulus"]
        and source_rows[0]["prime_modulus"] == band_rows[0]["prime_modulus"]
        and source_rows[0]["weakest_label"] == band_rows[0]["weakest_label"]
        and source_negative["reduced_denominator"]
        == band_negative["reduced_denominator"])


def build_receipt():
    source = json.loads(SOURCE_CLEARANCE.read_text(encoding="utf-8"))
    band = json.loads(BAND_CLEARANCE.read_text(encoding="utf-8"))
    payment = json.loads(Q46189_PAYMENT.read_text(encoding="utf-8"))
    source_scope = extract_rows(source, "scale_summaries", "scale_count")
    band_scope = extract_rows(band, "band_summaries", "band_count")
    same_exception = same_middle_far_exception(source_scope, band_scope)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_replacement_family_scope_boundary",
        "source_clearance_audit": str(SOURCE_CLEARANCE),
        "band_clearance_holdout": str(BAND_CLEARANCE),
        "q46189_payment_audit": str(Q46189_PAYMENT),
        "question": (
            "After the Q=46189 replacement-family payment audit, how broad is "
            "the current checked support for middle/far adverse replacement "
            "families?"),
        "answer": (
            "The current checked support has exactly one middle/far adverse "
            "denominator row in the source-start clearance receipt and exactly "
            "one in the sigma-band holdout, and they are the same "
            "M=229,p=379,label=00,12,Q=46189 exception.  All remaining "
            "adverse denominator rows in these receipts are near-threshold.  "
            "So replacement-family payment is a sharp finite target, but not "
            "yet a broad holdout theorem pattern."),
        "source_scope": source_scope,
        "band_scope": band_scope,
        "classification": {
            "source_middle_far_adverse_examples": (
                source_scope["middle_far_negative_row_count"]),
            "band_middle_far_adverse_examples": (
                band_scope["middle_far_negative_row_count"]),
            "same_q46189_exception_in_source_and_band": same_exception,
            "q46189_payment_is_single_current_middle_far_exemplar": (
                same_exception
                and source_scope["middle_far_negative_row_count"] == 1
                and band_scope["middle_far_negative_row_count"] == 1),
            "near_threshold_adverse_rows_remain_primary_broad_obligation": (
                source_scope["negative_denominator_family_counts"][
                    "near_1_to_2"] > 0
                and band_scope["negative_denominator_family_counts"][
                    "near_1_to_2"] > 0),
        },
        "q46189_payment_summary": {
            "replacement_payment_over_defect": (
                payment["replacement_family_summary"][
                    "payment_over_q46189_adverse"]),
            "minimum_individual_payment_over_defect": (
                payment["replacement_family_summary"][
                    "minimum_individual_payment_over_defect"]),
            "each_omitted_high_prime_family_pays_defect": (
                payment["classification"][
                    "each_omitted_high_prime_family_pays_defect"]),
        },
        "candidate_next_action": {
            "name": "replacement-family theorem boundary split",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Treat Q=46189 as the single current middle/far adverse "
                "exemplar for replacement-family payment, while keeping "
                "near-threshold leakage as a separate upper-bound obligation."),
            "prediction": (
                "A real replacement-family theorem should either prove the "
                "Q=46189-style inequality symbolically or find additional "
                "middle/far adverse exemplars with the same replacement-family "
                "payment pattern."),
            "falsifier": (
                "A new middle/far adverse denominator whose replacement "
                "families fail to pay the defect would falsify the present "
                "replacement-family theorem target."),
            "smallest_next_test": (
                "Search deliberately for additional middle/far adverse rows "
                "outside the six tight source blocks, or derive the symbolic "
                "Q=46189 replacement-family inequality before promoting the "
                "pattern."),
        },
        "decision": (
            "The replacement-family payment route remains alive but narrow.  "
            "Do not promote it as a broad finite holdout pattern: current "
            "checked middle/far adverse support is the single Q=46189 "
            "exception.  The universal pointwise proof still also needs an "
            "independent near-threshold leakage upper bound."),
        "finite_scope_boundary_audit_only": True,
        "finite_diagnostic_only": True,
        "replacement_family_payment_theorem_proved": False,
        "phase_defect_payment_theorem_proved": False,
        "near_adverse_upper_bound_proved": False,
        "middle_far_lower_bound_proved": False,
        "clearance_family_theorem_proved": False,
        "source_start_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    source = receipt["source_scope"]
    band = receipt["band_scope"]
    q = receipt["q46189_payment_summary"]
    lines = [
        "# Mobius moment-square degree-5 replacement-family scope boundary audit",
        "",
        "## Question",
        "",
        "After the `Q=46189` replacement-family payment audit, how broad is the",
        "current checked support for middle/far adverse replacement families?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_replacement_family_scope_boundary_audit.py",
        "evidence/mobius-moment-square-degree5-replacement-family-scope-boundary-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"source-start checked blocks:                 {source['checked_row_count']}",
        f"source near negative denominators:           {source['negative_denominator_family_counts']['near_1_to_2']}",
        f"source middle/far negative rows:             {source['middle_far_negative_row_count']}",
        f"band checked blocks:                         {band['checked_row_count']}",
        f"band near negative denominators:             {band['negative_denominator_family_counts']['near_1_to_2']}",
        f"band middle/far negative rows:               {band['middle_far_negative_row_count']}",
        f"same middle/far exception:                   {receipt['classification']['same_q46189_exception_in_source_and_band']}",
        f"Q46189 replacement payment / defect:         {q['replacement_payment_over_defect']}",
        f"Q46189 minimum row payment / defect:         {q['minimum_individual_payment_over_defect']}",
        "```",
        "",
        "The only checked middle/far adverse row in both receipts is the same",
        "`M=229`, `p=379`, `label=00,12`, `Q=46189` exception.  All other",
        "adverse denominator rows in these receipts are near-threshold.",
        "",
        "## Decision",
        "",
        "Replacement-family payment remains a live theorem target, but it is narrow:",
        "the current checked middle/far adverse support is one exemplar.  Do not",
        "promote it as a broad finite holdout pattern.  The universal pointwise",
        "route still needs an independent near-threshold leakage upper bound, plus",
        "either a symbolic `Q=46189` replacement-family inequality or additional",
        "middle/far adverse examples.",
        "",
        "This proves no replacement-family payment theorem, phase-defect payment",
        "theorem, near-adverse upper bound, middle/far lower bound, clearance-family",
        "theorem, source-start theorem, strict-central Goldbach theorem, or Goldbach",
        "proof.",
        "",
    ]
    NOTE.write_text("\n".join(lines), encoding="utf-8")


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    write_note(receipt)
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "source_middle_far_examples": (
            receipt["classification"]["source_middle_far_adverse_examples"]),
        "band_middle_far_examples": (
            receipt["classification"]["band_middle_far_adverse_examples"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
