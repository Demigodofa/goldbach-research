"""Build the weak-row degree-5 primewise active/full dominance audit."""

import json
from pathlib import Path


PRIMEWISE_SIGN = Path(
    "evidence/mobius-moment-square-degree5-primewise-sign-audit.json")
OUTPUT = Path(
    "evidence/mobius-moment-square-degree5-primewise-dominance-audit.json")
THRESHOLD = 0.5


def dominance_row(prime_row, contributor):
    active = contributor["active_contribution"]
    full = contributor["full_contribution"]
    if full == 0:
        ratio = None
        slack = None
    else:
        ratio = active / full
        slack = ratio - THRESHOLD
    return {
        "prime_modulus": prime_row["prime_modulus"],
        "left_label": contributor["left_label"],
        "right_label": contributor["right_label"],
        "active_contribution": active,
        "full_contribution": full,
        "half_frame_contribution": (
            contributor["half_frame_contribution"]),
        "active_over_full_ratio": ratio,
        "dominance_slack_above_one_half": slack,
        "full_contribution_negative": full < 0,
        "active_contribution_negative": active < 0,
        "dominates_one_half_signed_full": (
            full < 0 and ratio is not None and ratio > THRESHOLD),
    }


def total_dominance_row(prime_row):
    active = sum(
        row["active_contribution"] for row in prime_row["contributors"])
    full = sum(
        row["full_contribution"] for row in prime_row["contributors"])
    ratio = active / full if full else None
    slack = None if ratio is None else ratio - THRESHOLD
    return {
        "prime_modulus": prime_row["prime_modulus"],
        "active_degree5_total": active,
        "full_degree5_total": full,
        "half_frame_degree5_total": (
            prime_row["degree5_half_frame_total"]),
        "active_over_full_ratio": ratio,
        "dominance_slack_above_one_half": slack,
        "full_contribution_negative": full < 0,
        "active_contribution_negative": active < 0,
        "dominates_one_half_signed_full": (
            full < 0 and ratio is not None and ratio > THRESHOLD),
    }


def sign_counts(values):
    return {
        "positive": sum(1 for value in values if value > 0),
        "zero": sum(1 for value in values if value == 0),
        "negative": sum(1 for value in values if value < 0),
    }


def component_summaries(component_rows):
    labels = sorted({
        (row["left_label"], row["right_label"])
        for row in component_rows
    })
    summaries = {}
    for left_label, right_label in labels:
        label = f"{left_label},{right_label}"
        rows = [
            row for row in component_rows
            if row["left_label"] == left_label
            and row["right_label"] == right_label
        ]
        slacks = [row["dominance_slack_above_one_half"] for row in rows]
        ratios = [row["active_over_full_ratio"] for row in rows]
        summaries[label] = {
            "row_count": len(rows),
            "all_signed_full_negative": all(
                row["full_contribution_negative"] for row in rows),
            "all_signed_active_negative": all(
                row["active_contribution_negative"] for row in rows),
            "all_rows_dominate_one_half_signed_full": all(
                row["dominates_one_half_signed_full"] for row in rows),
            "minimum_active_over_full_ratio": min(ratios),
            "maximum_active_over_full_ratio": max(ratios),
            "minimum_dominance_slack_above_one_half": min(slacks),
            "maximum_dominance_slack_above_one_half": max(slacks),
            "weakest_dominance_row": min(
                rows, key=lambda row: row[
                    "dominance_slack_above_one_half"]),
        }
    return summaries


def build_receipt():
    source = json.loads(PRIMEWISE_SIGN.read_text(encoding="utf-8"))
    component_rows = [
        dominance_row(prime_row, contributor)
        for prime_row in source["prime_rows"]
        for contributor in prime_row["contributors"]
    ]
    total_rows = [
        total_dominance_row(prime_row)
        for prime_row in source["prime_rows"]
    ]
    component_slacks = [
        row["dominance_slack_above_one_half"]
        for row in component_rows
    ]
    total_slacks = [
        row["dominance_slack_above_one_half"]
        for row in total_rows
    ]
    weakest_component = min(
        component_rows,
        key=lambda row: row["dominance_slack_above_one_half"])
    weakest_total = min(
        total_rows,
        key=lambda row: row["dominance_slack_above_one_half"])
    return {
        "status": "MEASURE_degree5_primewise_dominance_slack",
        "question": (
            "For the weak M=167 primewise degree-5 sign pass, how far above "
            "the signed one-half full-energy threshold do the active/full "
            "component ratios stay?"),
        "source_primewise_sign_audit": str(PRIMEWISE_SIGN),
        "scale_modulus": source["scale_modulus"],
        "prime_count": source["prime_count"],
        "row_count": source["row_count"],
        "ell_freeze": source["ell_freeze"],
        "divisor_range": source["divisor_range"],
        "threshold": THRESHOLD,
        "component_rows": component_rows,
        "component_summaries": component_summaries(component_rows),
        "degree5_total_rows": total_rows,
        "all_component_full_contributions_negative": all(
            row["full_contribution_negative"] for row in component_rows),
        "all_component_active_contributions_negative": all(
            row["active_contribution_negative"] for row in component_rows),
        "all_component_ratios_exceed_one_half": all(
            row["dominates_one_half_signed_full"]
            for row in component_rows),
        "all_degree5_total_ratios_exceed_one_half": all(
            row["dominates_one_half_signed_full"] for row in total_rows),
        "component_dominance_slack_sign_counts": sign_counts(
            component_slacks),
        "degree5_total_dominance_slack_sign_counts": sign_counts(
            total_slacks),
        "minimum_component_dominance_slack_above_one_half": (
            min(component_slacks)),
        "minimum_degree5_total_dominance_slack_above_one_half": (
            min(total_slacks)),
        "weakest_component_dominance_row": weakest_component,
        "weakest_degree5_total_dominance_row": weakest_total,
        "prediction": (
            "If the primewise sign localization is theorem-shaped rather "
            "than accidental, the equivalent active/full ratios should stay "
            "strictly above one half with a visible finite cushion."),
        "falsifier": (
            "Any checked component or degree-5 total with negative full "
            "contribution and active/full ratio at or below one half would "
            "falsify this finite dominance-slack test."),
        "decision": (
            "The weak M=167 block has positive dominance slack in every "
            "checked degree-5 component and total row.  The weakest component "
            "is (00,12) at prime 181, where active/full is about "
            "0.5563677490893767, leaving slack about 0.056367749089376695 "
            "above the signed one-half threshold.  Thus the finite sign "
            "localization can be restated as a quantitative one-prime "
            "active/full dominance target."),
        "finite_primewise_dominance_diagnostic_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
        "primewise_dominance_theorem_proved": False,
        "primewise_sign_theorem_proved": False,
        "degree5_coefficient_theorem_proved": False,
        "robust_margin_universal_theorem_proved": False,
        "coefficient_family_theorem_proved": False,
        "universal_sturm_certificate_theorem_proved": False,
        "moment_square_half_frame_curve_positivity_theorem_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "mobius_covariance_theorem_proved": False,
        "signed_prime_correlation_proved": False,
    }


def main():
    receipt = build_receipt()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
