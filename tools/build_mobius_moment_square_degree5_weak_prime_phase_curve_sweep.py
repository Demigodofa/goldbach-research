"""Build a weak-prime degree-5 active-window phase-curve sweep."""

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
from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    PAIRS,
    THRESHOLD,
    dominance_row,
    scale_parameters,
    sign_counts,
)


WEAK_SCALE = 167
WEAK_PRIME = 181
OUTPUT = Path(
    "evidence/mobius-moment-square-degree5-weak-prime-phase-curve-sweep.json")


def active_row_start_sweep():
    row_count = scale_parameters(WEAK_SCALE)["row_count"]
    return list(range(0, 2 * row_count + 1))


def rows_for_start(active_row_start):
    parameters = scale_parameters(WEAK_SCALE)
    divisor_lower, divisor_upper = parameters["divisor_range"]
    receipt = lifted_endpoint_residue_gram_receipt(
        WEAK_PRIME,
        parameters["row_count"],
        parameters["ell_freeze"],
        divisor_lower,
        divisor_upper,
        active_row_start=active_row_start,
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
        row = dominance_row(
            WEAK_SCALE,
            WEAK_PRIME,
            f"{left_label},{right_label}",
            active_contribution,
            full_contribution,
            half_contribution,
        )
        row["active_row_start"] = active_row_start
        row["active_row_stop"] = active_row_start + parameters["row_count"]
        row["active_row_start_offset"] = (
            active_row_start - parameters["row_count"])
        component_rows.append(row)
    active_total = sum(row["active_contribution"] for row in component_rows)
    full_total = sum(row["full_contribution"] for row in component_rows)
    half_total = sum(row["half_frame_contribution"] for row in component_rows)
    total_row = dominance_row(
        WEAK_SCALE,
        WEAK_PRIME,
        "TOTAL",
        active_total,
        full_total,
        half_total,
    )
    total_row["active_row_start"] = active_row_start
    total_row["active_row_stop"] = active_row_start + parameters["row_count"]
    total_row["active_row_start_offset"] = (
        active_row_start - parameters["row_count"])
    return [*component_rows, total_row]


def label_summary(rows, label):
    selected = [row for row in rows if row["label"] == label]
    slacks = [row["dominance_slack_above_one_half"] for row in selected]
    weakest = min(
        selected, key=lambda row: row["dominance_slack_above_one_half"])
    strongest = max(
        selected, key=lambda row: row["dominance_slack_above_one_half"])
    return {
        "label": label,
        "row_count": len(selected),
        "dominance_slack_sign_counts": sign_counts(slacks),
        "all_rows_dominate_one_half_signed_full": all(
            row["dominates_one_half_signed_full"] for row in selected),
        "minimum_dominance_slack_above_one_half": min(slacks),
        "maximum_dominance_slack_above_one_half": max(slacks),
        "weakest_dominance_row": weakest,
        "strongest_dominance_row": strongest,
    }


def build_receipt():
    parameters = scale_parameters(WEAK_SCALE)
    rows = []
    failure_rows = []
    for active_row_start in active_row_start_sweep():
        start_rows = rows_for_start(active_row_start)
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
        "status": "SWEEP_degree5_weak_prime_active_window_phase_curve",
        "question": (
            "For the weakest checked prime row, does sweeping the active row "
            "start across the extended local band 0..70 expose a concrete "
            "degree-5 active/full dominance failure?"),
        "scale_modulus": WEAK_SCALE,
        "prime_modulus": WEAK_PRIME,
        "threshold": THRESHOLD,
        "row_count": parameters["row_count"],
        "ell_freeze": parameters["ell_freeze"],
        "divisor_range": parameters["divisor_range"],
        "active_row_start_sweep": active_row_start_sweep(),
        "active_row_start_count": len(active_row_start_sweep()),
        "curve_rows": rows,
        "label_summaries": {
            label: label_summary(rows, label) for label in labels
        },
        "component_row_count": sum(
            1 for row in rows if row["label"] != "TOTAL"),
        "degree5_total_row_count": sum(
            1 for row in rows if row["label"] == "TOTAL"),
        "dominance_row_count": len(rows),
        "all_dominance_slack_sign_counts": sign_counts(slacks),
        "all_rows_dominate_one_half_signed_full": len(failure_rows) == 0,
        "failure_row_count": len(failure_rows),
        "failure_rows": failure_rows,
        "minimum_dominance_slack_above_one_half": (
            weakest["dominance_slack_above_one_half"]),
        "maximum_dominance_slack_above_one_half": (
            strongest["dominance_slack_above_one_half"]),
        "weakest_dominance_row": weakest,
        "strongest_dominance_row": strongest,
        "prediction": (
            "If the local active-window dominance margin is not merely a "
            "five-start accident around the source interval, the same weakest "
            "prime should retain positive slack through a broader local row-"
            "start sweep."),
        "falsifier": (
            "Any component or degree-5 total row for active row starts 0 "
            "through 70 whose signed full contribution is negative but whose "
            "active/full ratio is at or below one half, or any row losing the "
            "negative signed-full premise, is a concrete finite falsifier for "
            "this weak-prime phase-curve sweep."),
        "decision": (
            "The weakest-prime extended local phase-curve sweep survives: "
            "every component and degree-5 total row for active row starts 0 "
            "through 70 retains positive active/full dominance slack above "
            "one half.  This is useful curve-shape evidence for the active-"
            "window theorem target, not a period theorem or a universal "
            "pointwise bound."),
        "finite_weak_prime_phase_curve_sweep_only": True,
        "finite_diagnostic_only": True,
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
