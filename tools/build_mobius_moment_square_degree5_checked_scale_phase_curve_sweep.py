"""Build a checked-scale degree-5 active-window phase-curve sweep."""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mobius_covariance_endpoint_probe import _prime_flags  # noqa: E402
from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    PAIRS,
    SCALES,
    THRESHOLD,
    dominance_row,
    scale_parameters,
    sign_counts,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _active_gram,
    _residue_cells_by_denominator,
    label_summary,
)


OUTPUT = Path(
    "evidence/mobius-moment-square-degree5-checked-scale-phase-curve-sweep.json")


def active_row_start_sweep(scale_modulus):
    row_count = scale_parameters(scale_modulus)["row_count"]
    return list(range(0, 2 * row_count + 1))


def _dominance_rows_for_start(
        scale_modulus, prime_modulus, active_row_start,
        row_count, active, full):
    component_rows = []
    dominance_rows = []
    for left, right, left_label, right_label in PAIRS:
        active_contribution = float(2 * active[left, right])
        full_contribution = float(2 * full[left, right])
        half_contribution = (
            active_contribution - THRESHOLD * full_contribution)
        row = dominance_row(
            scale_modulus,
            prime_modulus,
            f"{left_label},{right_label}",
            active_contribution,
            full_contribution,
            half_contribution,
        )
        row["active_row_start"] = active_row_start
        row["active_row_stop"] = active_row_start + row_count
        row["active_row_start_offset"] = active_row_start - row_count
        component_rows.append(row)
        dominance_rows.append(row)
    active_total = sum(row["active_contribution"] for row in component_rows)
    full_total = sum(row["full_contribution"] for row in component_rows)
    half_total = sum(row["half_frame_contribution"] for row in component_rows)
    total_row = dominance_row(
        scale_modulus,
        prime_modulus,
        "TOTAL",
        active_total,
        full_total,
        half_total,
    )
    total_row["active_row_start"] = active_row_start
    total_row["active_row_stop"] = active_row_start + row_count
    total_row["active_row_start_offset"] = active_row_start - row_count
    dominance_rows.append(total_row)
    return dominance_rows


def prime_summary(scale_modulus, prime_modulus):
    parameters = scale_parameters(scale_modulus)
    divisor_lower, divisor_upper = parameters["divisor_range"]
    full, cells_by_denominator = _residue_cells_by_denominator(
        prime_modulus,
        parameters["row_count"],
        parameters["ell_freeze"],
        divisor_lower,
        divisor_upper,
    )
    rows = []
    failure_rows = []
    for active_row_start in active_row_start_sweep(scale_modulus):
        active = _active_gram(
            cells_by_denominator, parameters["row_count"], active_row_start)
        start_rows = _dominance_rows_for_start(
            scale_modulus,
            prime_modulus,
            active_row_start,
            parameters["row_count"],
            active,
            full,
        )
        rows.extend(start_rows)
        failure_rows.extend([
            row for row in start_rows
            if not row["dominates_one_half_signed_full"]
        ])
    slacks = [row["dominance_slack_above_one_half"] for row in rows]
    weakest = min(
        rows, key=lambda row: row["dominance_slack_above_one_half"])
    strongest = max(
        rows, key=lambda row: row["dominance_slack_above_one_half"])
    labels = [f"{left},{right}" for _, _, left, right in PAIRS]
    labels.append("TOTAL")
    return {
        "scale_modulus": scale_modulus,
        "prime_modulus": prime_modulus,
        "row_count": parameters["row_count"],
        "ell_freeze": parameters["ell_freeze"],
        "divisor_range": parameters["divisor_range"],
        "active_row_start_count": len(active_row_start_sweep(scale_modulus)),
        "component_row_count": sum(
            1 for row in rows if row["label"] != "TOTAL"),
        "degree5_total_row_count": sum(
            1 for row in rows if row["label"] == "TOTAL"),
        "dominance_row_count": len(rows),
        "dominance_slack_sign_counts": sign_counts(slacks),
        "all_rows_dominate_one_half_signed_full": len(failure_rows) == 0,
        "failure_row_count": len(failure_rows),
        "failure_rows": failure_rows,
        "minimum_dominance_slack_above_one_half": min(slacks),
        "maximum_dominance_slack_above_one_half": max(slacks),
        "weakest_dominance_row": weakest,
        "strongest_dominance_row": strongest,
        "label_summaries": {
            label: label_summary(rows, label) for label in labels
        },
    }


def scale_summary(scale_modulus):
    flags = _prime_flags(2 * scale_modulus)
    prime_summaries = [
        prime_summary(scale_modulus, prime_modulus)
        for prime_modulus in range(scale_modulus, 2 * scale_modulus + 1)
        if flags[prime_modulus]
    ]
    all_failures = []
    for summary in prime_summaries:
        all_failures.extend(summary["failure_rows"])
    weakest = min(
        (summary["weakest_dominance_row"] for summary in prime_summaries),
        key=lambda row: row["dominance_slack_above_one_half"])
    strongest = max(
        (summary["strongest_dominance_row"] for summary in prime_summaries),
        key=lambda row: row["dominance_slack_above_one_half"])
    row_count = sum(summary["dominance_row_count"]
                    for summary in prime_summaries)
    component_count = sum(summary["component_row_count"]
                          for summary in prime_summaries)
    total_count = sum(summary["degree5_total_row_count"]
                      for summary in prime_summaries)
    slack_sign_counts = {
        "positive": row_count - len(all_failures),
        "zero": sum(
            1 for row in all_failures
            if row["dominance_slack_above_one_half"] == 0),
        "negative": sum(
            1 for row in all_failures
            if row["dominance_slack_above_one_half"] < 0),
    }
    parameters = scale_parameters(scale_modulus)
    return {
        "scale_modulus": scale_modulus,
        "row_count": parameters["row_count"],
        "ell_freeze": parameters["ell_freeze"],
        "divisor_range": parameters["divisor_range"],
        "active_row_start_count": len(active_row_start_sweep(scale_modulus)),
        "prime_count": len(prime_summaries),
        "prime_summaries": prime_summaries,
        "component_row_count": component_count,
        "degree5_total_row_count": total_count,
        "dominance_row_count": row_count,
        "dominance_slack_sign_counts": slack_sign_counts,
        "all_rows_dominate_one_half_signed_full": len(all_failures) == 0,
        "failure_row_count": len(all_failures),
        "failure_rows": all_failures,
        "minimum_dominance_slack_above_one_half": (
            weakest["dominance_slack_above_one_half"]),
        "maximum_dominance_slack_above_one_half": (
            strongest["dominance_slack_above_one_half"]),
        "weakest_dominance_row": weakest,
        "strongest_dominance_row": strongest,
    }


def build_receipt():
    scale_summaries = [scale_summary(scale_modulus) for scale_modulus in SCALES]
    all_failures = []
    for summary in scale_summaries:
        all_failures.extend(summary["failure_rows"])
    weakest = min(
        (summary["weakest_dominance_row"] for summary in scale_summaries),
        key=lambda row: row["dominance_slack_above_one_half"])
    strongest = max(
        (summary["strongest_dominance_row"] for summary in scale_summaries),
        key=lambda row: row["dominance_slack_above_one_half"])
    row_count = sum(summary["dominance_row_count"]
                    for summary in scale_summaries)
    component_count = sum(summary["component_row_count"]
                          for summary in scale_summaries)
    total_count = sum(summary["degree5_total_row_count"]
                      for summary in scale_summaries)
    slack_sign_counts = {
        "positive": row_count - len(all_failures),
        "zero": sum(
            1 for row in all_failures
            if row["dominance_slack_above_one_half"] == 0),
        "negative": sum(
            1 for row in all_failures
            if row["dominance_slack_above_one_half"] < 0),
    }
    return {
        "status": "SWEEP_degree5_checked_scale_active_window_phase_curve",
        "question": (
            "Across every checked scale, prime row, and active row start in "
            "the extended local band 0..2A, does a degree-5 active/full "
            "dominance failure appear?"),
        "scales": SCALES,
        "threshold": THRESHOLD,
        "scale_summaries": scale_summaries,
        "scale_count": len(scale_summaries),
        "prime_count_total": sum(
            summary["prime_count"] for summary in scale_summaries),
        "component_row_count": component_count,
        "degree5_total_row_count": total_count,
        "dominance_row_count": row_count,
        "all_dominance_slack_sign_counts": slack_sign_counts,
        "all_rows_dominate_one_half_signed_full": len(all_failures) == 0,
        "failure_row_count": len(all_failures),
        "failure_rows": all_failures,
        "minimum_dominance_slack_above_one_half": (
            weakest["dominance_slack_above_one_half"]),
        "maximum_dominance_slack_above_one_half": (
            strongest["dominance_slack_above_one_half"]),
        "weakest_dominance_row": weakest,
        "strongest_dominance_row": strongest,
        "prediction": (
            "If the active-window phase-curve dominance target is not a "
            "weak-scale accident, every checked scale should retain positive "
            "slack through its broader local row-start sweep."),
        "falsifier": (
            "Any component or degree-5 total row for any checked scale, prime, "
            "and active row start 0 through 2A whose signed full contribution "
            "is negative but whose active/full ratio is at or below one half, "
            "or any row losing the negative signed-full premise, is a concrete "
            "finite falsifier for this checked-scale phase-curve sweep."),
        "decision": (
            "The broad checked-scale active-window phase-curve extension is "
            "falsified finitely: one checked row at M=149, prime 163, active "
            "row start 1, component (00,12), falls below the signed one-half "
            "threshold.  The source-window and weak-scale results survive as "
            "narrower finite facts, but active-window dominance cannot be "
            "promoted with the broad row-start quantifier tested here."),
        "finite_checked_scale_phase_curve_sweep_only": True,
        "finite_diagnostic_only": True,
        "finite_falsifier_found": len(all_failures) > 0,
        "broad_checked_scale_phase_curve_extension_falsified": (
            len(all_failures) > 0),
        "goldbach_proved": False,
        "q286_reactivated": False,
        "phase_curve_theorem_proved": False,
        "active_window_translation_theorem_proved": False,
        "ell_freeze_dominance_theorem_proved": False,
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
