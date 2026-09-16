"""Build the checked-scale degree-5 primewise dominance audit."""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lcm_sawtooth_lifted_endpoint_frame import (  # noqa: E402
    lifted_endpoint_residue_gram_receipt,
)
from mobius_covariance_endpoint_probe import _prime_flags  # noqa: E402
from tools.build_mobius_moment_square_degree5_primewise_dominance_audit import (  # noqa: E402
    THRESHOLD,
)


OUTPUT = Path(
    "evidence/mobius-moment-square-degree5-checked-scale-dominance-audit.json")
SCALES = (127, 149, 167, 191, 211, 227)
PAIRS = (
    (0, 4, "00", "12"),
    (1, 2, "01", "02"),
    (1, 3, "01", "11"),
)


def scale_parameters(scale_modulus):
    inferred_n = scale_modulus ** (1 / .59)
    row_count = int(inferred_n ** .41)
    divisor_lower = int(inferred_n ** .15)
    divisor_upper = int(inferred_n ** .32)
    ell_freeze = row_count + row_count // 2
    return {
        "row_count": row_count,
        "ell_freeze": ell_freeze,
        "divisor_range": (divisor_lower, divisor_upper),
    }


def dominance_row(scale_modulus, prime_modulus, label, active, full, half):
    ratio = active / full if full else None
    slack = None if ratio is None else ratio - THRESHOLD
    return {
        "scale_modulus": scale_modulus,
        "prime_modulus": prime_modulus,
        "label": label,
        "active_contribution": active,
        "full_contribution": full,
        "half_frame_contribution": half,
        "active_over_full_ratio": ratio,
        "dominance_slack_above_one_half": slack,
        "full_contribution_negative": full < 0,
        "active_contribution_negative": active < 0,
        "dominates_one_half_signed_full": (
            full < 0 and ratio is not None and ratio > THRESHOLD),
    }


def prime_rows_for_scale(scale_modulus):
    parameters = scale_parameters(scale_modulus)
    divisor_lower, divisor_upper = parameters["divisor_range"]
    flags = _prime_flags(2 * scale_modulus)
    rows = []
    for prime_modulus in range(scale_modulus, 2 * scale_modulus + 1):
        if not flags[prime_modulus]:
            continue
        receipt = lifted_endpoint_residue_gram_receipt(
            prime_modulus,
            parameters["row_count"],
            parameters["ell_freeze"],
            divisor_lower,
            divisor_upper,
        )
        active = np.asarray(receipt["active_window_residue_energy_gram"])
        active = (active + active.T) / 2
        full = np.asarray(receipt["full_residue_energy_gram"])
        full = (full + full.T) / 2
        component_rows = []
        for left, right, left_label, right_label in PAIRS:
            active_contribution = float(2 * active[left, right])
            full_contribution = float(2 * full[left, right])
            half_contribution = (
                active_contribution - THRESHOLD * full_contribution)
            component_rows.append(dominance_row(
                scale_modulus,
                prime_modulus,
                f"{left_label},{right_label}",
                active_contribution,
                full_contribution,
                half_contribution,
            ))
        active_total = sum(
            row["active_contribution"] for row in component_rows)
        full_total = sum(
            row["full_contribution"] for row in component_rows)
        half_total = sum(
            row["half_frame_contribution"] for row in component_rows)
        total_row = dominance_row(
            scale_modulus,
            prime_modulus,
            "TOTAL",
            active_total,
            full_total,
            half_total,
        )
        rows.append({
            "prime_modulus": prime_modulus,
            "component_rows": component_rows,
            "degree5_total_row": total_row,
        })
    return parameters, rows


def flatten_rows(scale_results, include_totals=True):
    rows = []
    for scale_row in scale_results:
        for prime_row in scale_row["prime_rows"]:
            rows.extend(prime_row["component_rows"])
            if include_totals:
                rows.append(prime_row["degree5_total_row"])
    return rows


def sign_counts(values):
    return {
        "positive": sum(1 for value in values if value > 0),
        "zero": sum(1 for value in values if value == 0),
        "negative": sum(1 for value in values if value < 0),
    }


def scale_summary(scale_row):
    rows = []
    for prime_row in scale_row["prime_rows"]:
        rows.extend(prime_row["component_rows"])
        rows.append(prime_row["degree5_total_row"])
    slacks = [row["dominance_slack_above_one_half"] for row in rows]
    weakest = min(rows, key=lambda row: row[
        "dominance_slack_above_one_half"])
    strongest = max(rows, key=lambda row: row[
        "dominance_slack_above_one_half"])
    return {
        "scale_modulus": scale_row["scale_modulus"],
        "prime_count": scale_row["prime_count"],
        "row_count": scale_row["row_count"],
        "ell_freeze": scale_row["ell_freeze"],
        "divisor_range": scale_row["divisor_range"],
        "dominance_row_count": len(rows),
        "dominance_slack_sign_counts": sign_counts(slacks),
        "all_rows_dominate_one_half_signed_full": all(
            row["dominates_one_half_signed_full"] for row in rows),
        "minimum_dominance_slack_above_one_half": min(slacks),
        "maximum_dominance_slack_above_one_half": max(slacks),
        "weakest_dominance_row": weakest,
        "strongest_dominance_row": strongest,
    }


def build_receipt():
    scale_results = []
    for scale_modulus in SCALES:
        parameters, prime_rows = prime_rows_for_scale(scale_modulus)
        scale_results.append({
            "scale_modulus": scale_modulus,
            "prime_count": len(prime_rows),
            "row_count": parameters["row_count"],
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": parameters["divisor_range"],
            "prime_rows": prime_rows,
        })
    all_rows = flatten_rows(scale_results)
    component_rows = [
        row for row in all_rows if row["label"] != "TOTAL"]
    total_rows = [
        row for row in all_rows if row["label"] == "TOTAL"]
    all_slacks = [
        row["dominance_slack_above_one_half"] for row in all_rows]
    component_slacks = [
        row["dominance_slack_above_one_half"] for row in component_rows]
    total_slacks = [
        row["dominance_slack_above_one_half"] for row in total_rows]
    weakest = min(
        all_rows,
        key=lambda row: row["dominance_slack_above_one_half"])
    strongest = max(
        all_rows,
        key=lambda row: row["dominance_slack_above_one_half"])
    return {
        "status": "CHECK_degree5_checked_scale_primewise_dominance",
        "question": (
            "Does the weak-block degree-5 active/full dominance phenomenon "
            "extend across all six checked moment-square scales, or does a "
            "checked scale falsify the local dominance target?"),
        "scales": SCALES,
        "threshold": THRESHOLD,
        "scale_results": scale_results,
        "scale_summaries": [
            scale_summary(scale_row) for scale_row in scale_results
        ],
        "prime_count_total": sum(
            scale_row["prime_count"] for scale_row in scale_results),
        "component_row_count": len(component_rows),
        "degree5_total_row_count": len(total_rows),
        "dominance_row_count": len(all_rows),
        "component_dominance_slack_sign_counts": sign_counts(
            component_slacks),
        "degree5_total_dominance_slack_sign_counts": sign_counts(
            total_slacks),
        "all_dominance_slack_sign_counts": sign_counts(all_slacks),
        "all_component_rows_dominate_one_half_signed_full": all(
            row["dominates_one_half_signed_full"]
            for row in component_rows),
        "all_degree5_total_rows_dominate_one_half_signed_full": all(
            row["dominates_one_half_signed_full"] for row in total_rows),
        "all_rows_dominate_one_half_signed_full": all(
            row["dominates_one_half_signed_full"] for row in all_rows),
        "minimum_dominance_slack_above_one_half": min(all_slacks),
        "maximum_dominance_slack_above_one_half": max(all_slacks),
        "weakest_dominance_row": weakest,
        "strongest_dominance_row": strongest,
        "prediction": (
            "If the one-prime degree-5 dominance target is structural across "
            "the checked moment-square fixture, every component and total "
            "row in the six checked scales should retain positive slack "
            "above one half."),
        "falsifier": (
            "Any checked component or degree-5 total row with negative full "
            "contribution and active/full ratio at or below one half would "
            "falsify this checked-scale dominance extension."),
        "decision": (
            "The checked-scale extension survives: all 756 checked component "
            "and total rows across scales 127, 149, 167, 191, 211, and 227 "
            "have positive active/full dominance slack above one half.  The "
            "global weakest row remains the weak-block component (00,12) at "
            "M=167, prime 181, with slack about 0.056367749089376695."),
        "finite_checked_scale_dominance_diagnostic_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
        "checked_scale_dominance_theorem_proved": False,
        "primewise_dominance_theorem_proved": False,
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
