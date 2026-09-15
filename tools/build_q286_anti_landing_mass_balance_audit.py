"""Separate mass balance from coefficient-weighted anti-landing for q286.

The edge-minorant obstruction shows that the rescue coefficient
gap-required has positive and negative regions.  This derived receipt asks
whether actual rescue is explained by a simple mass-majority cone

    mass(positive coefficients) > mass(negative coefficients),

or whether it genuinely needs coefficient-weighted landing:

    avg_positive_coeff / avg_negative_coeff
      > mass_negative / mass_positive.

Finite diagnostic only.  It proves no anti-landing theorem, signed
prime-correlation estimate, q286 threshold theorem, strict-central Goldbach
theorem, or Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE = EVIDENCE / "q286-edge-minorant-obstruction-audit.json"
OUT = EVIDENCE / "q286-anti-landing-mass-balance-audit.json"
TOLERANCE = 1e-12


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


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


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def classify_row(row):
    mass_positive = float(row["actual_mass_on_positive_rescue_coefficients"])
    mass_negative = float(row["actual_mass_on_negative_rescue_coefficients"])
    positive = float(row["positive_rescue_contribution"])
    negative = float(row["negative_rescue_drag"])
    avg_positive = positive / mass_positive if mass_positive > TOLERANCE else None
    avg_negative = negative / mass_negative if mass_negative > TOLERANCE else None
    coefficient_lift = (
        avg_positive / avg_negative
        if avg_positive is not None and avg_negative is not None
        and avg_negative > TOLERANCE else None)
    required_lift = (
        mass_negative / mass_positive
        if mass_positive > TOLERANCE else None)
    lift_surplus = (
        coefficient_lift - required_lift
        if coefficient_lift is not None and required_lift is not None
        else None)
    return {
        "target": int(row["target"]),
        "target_residue": int(row["target_residue"]),
        "target_mod_286": int(row["target_mod_286"]),
        "block_index_after_discovery": int(
            row["block_index_after_discovery"]),
        "mass_positive": mass_positive,
        "mass_negative": mass_negative,
        "mass_positive_minus_negative": mass_positive - mass_negative,
        "mass_balance_ratio": (
            mass_positive / mass_negative
            if mass_negative > TOLERANCE else None),
        "mass_majority_pass": bool(mass_positive > mass_negative),
        "average_positive_rescue_coefficient": avg_positive,
        "average_negative_rescue_coefficient": avg_negative,
        "coefficient_lift_ratio": coefficient_lift,
        "required_lift_ratio_from_mass_split": required_lift,
        "coefficient_lift_surplus": lift_surplus,
        "weighted_landing_pass": bool(
            lift_surplus is not None and lift_surplus > 0.0),
        "positive_to_negative_rescue_ratio": float(
            row["positive_to_negative_rescue_ratio"]),
        "rescue_margin_from_signed_parts": float(
            row["rescue_margin_from_signed_parts"]),
        "signed_part_identity_error": float(
            row["signed_part_identity_error"]),
    }


def build_receipt():
    source = load_json(SOURCE)
    rows = [classify_row(row) for row in source["target_rows"]]
    post = [row for row in rows if row["block_index_after_discovery"] >= 1]
    discovery = [row for row in rows if row["block_index_after_discovery"] < 1]

    def summarize(bucket):
        majority_pass = sum(row["mass_majority_pass"] for row in bucket)
        weighted_pass = sum(row["weighted_landing_pass"] for row in bucket)
        rescued_without_majority = sum(
            (not row["mass_majority_pass"]) and row["weighted_landing_pass"]
            for row in bucket)
        return {
            "row_count": len(bucket),
            "mass_majority_pass_count": majority_pass,
            "mass_majority_fail_count": len(bucket) - majority_pass,
            "weighted_landing_pass_count": weighted_pass,
            "rescued_without_mass_majority_count": rescued_without_majority,
            "mass_positive_summary": finite_summary(
                row["mass_positive"] for row in bucket),
            "mass_negative_summary": finite_summary(
                row["mass_negative"] for row in bucket),
            "mass_positive_minus_negative_summary": finite_summary(
                row["mass_positive_minus_negative"] for row in bucket),
            "mass_balance_ratio_summary": finite_summary(
                row["mass_balance_ratio"] for row in bucket),
            "average_positive_rescue_coefficient_summary": finite_summary(
                row["average_positive_rescue_coefficient"] for row in bucket),
            "average_negative_rescue_coefficient_summary": finite_summary(
                row["average_negative_rescue_coefficient"] for row in bucket),
            "coefficient_lift_ratio_summary": finite_summary(
                row["coefficient_lift_ratio"] for row in bucket),
            "required_lift_ratio_from_mass_split_summary": finite_summary(
                row["required_lift_ratio_from_mass_split"] for row in bucket),
            "coefficient_lift_surplus_summary": finite_summary(
                row["coefficient_lift_surplus"] for row in bucket),
            "positive_to_negative_rescue_ratio_summary": finite_summary(
                row["positive_to_negative_rescue_ratio"] for row in bucket),
            "signed_part_identity_error_summary": finite_summary(
                row["signed_part_identity_error"] for row in bucket),
        }

    post_fail_majority = [
        row for row in post if not row["mass_majority_pass"]]
    tightest_lift = sorted(
        post,
        key=lambda row: (row["coefficient_lift_surplus"], row["target"]))[:20]
    largest_negative_mass = sorted(
        post,
        key=lambda row: (-row["mass_negative"], row["target"]))[:20]

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "edge_minorant_obstruction_audit": str(SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite anti-landing mass-balance diagnostic only; no mass-balance "
            "theorem, coefficient-weighted anti-landing theorem, signed "
            "prime-correlation theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"
        ),
        "goldbach_proved": False,
        "mass_balance_theorem_proved": False,
        "coefficient_weighted_anti_landing_theorem_proved": False,
        "mass_majority_candidate_falsified": True,
        "curiosity_status": "changed-under-evidence",
        "novelty_label": "new-to-this-task",
        "candidate": {
            "mechanism": (
                "If rescue only needed more mass on positive pointwise "
                "coefficients than negative ones, a cone theorem could ignore "
                "coefficient magnitudes.  Otherwise the proof must compare "
                "weighted landing averages on the two regions."
            ),
            "prediction": (
                "Some actual rows should rescue despite having less mass on "
                "the positive side, showing that coefficient lift rather than "
                "mass majority is doing real work."
            ),
            "falsifier": (
                "If every rescued post-boundary row had positive mass greater "
                "than negative mass, the mass-majority cone would remain a "
                "candidate simplification."
            ),
            "smallest_test": (
                "Use the edge-minorant obstruction rows and compare mass "
                "majority with the exact coefficient-lift inequality."
            ),
        },
        "decision": (
            "Mass majority is not the theorem: 18 checked post-discovery rows "
            "rescue despite carrying more mass on negative pointwise rescue "
            "coefficients than positive ones.  The surviving target is a "
            "coefficient-weighted anti-landing inequality comparing average "
            "positive rescue strength to average negative drag."
        ),
        "summary": {
            "target_row_count": len(rows),
            "post_discovery_target_count": len(post),
            "discovery_target_count": len(discovery),
            "all_rows": summarize(rows),
            "post_discovery_rows": summarize(post),
            "discovery_rows": summarize(discovery),
            "post_discovery_rows_rescued_without_mass_majority":
                post_fail_majority,
            "tightest_post_discovery_coefficient_lift_rows": tightest_lift,
            "largest_post_discovery_negative_mass_rows": largest_negative_mass,
        },
        "target_rows": rows,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
