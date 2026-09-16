"""Build the weak-scale degree-5 active-window translation stress audit."""

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
from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    PAIRS,
    THRESHOLD,
    dominance_row,
    scale_parameters,
    sign_counts,
)


WEAK_SCALE = 167
ROW_START_OFFSETS = (-2, -1, 0, 1, 2)
OUTPUT = Path(
    "evidence/mobius-moment-square-degree5-active-window-translation-stress.json")


def active_row_starts():
    base = scale_parameters(WEAK_SCALE)["row_count"]
    return [base + offset for offset in ROW_START_OFFSETS]


def summarize_active_row_start(active_row_start):
    parameters = scale_parameters(WEAK_SCALE)
    divisor_lower, divisor_upper = parameters["divisor_range"]
    flags = _prime_flags(2 * WEAK_SCALE)
    dominance_rows = []
    failure_rows = []
    for prime_modulus in range(WEAK_SCALE, 2 * WEAK_SCALE + 1):
        if not flags[prime_modulus]:
            continue
        receipt = lifted_endpoint_residue_gram_receipt(
            prime_modulus,
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
                prime_modulus,
                f"{left_label},{right_label}",
                active_contribution,
                full_contribution,
                half_contribution,
            )
            row["active_row_start"] = active_row_start
            row["active_row_stop"] = (
                active_row_start + parameters["row_count"])
            row["active_row_start_offset"] = (
                active_row_start - parameters["row_count"])
            component_rows.append(row)
            dominance_rows.append(row)
        active_total = sum(
            row["active_contribution"] for row in component_rows)
        full_total = sum(
            row["full_contribution"] for row in component_rows)
        half_total = sum(
            row["half_frame_contribution"] for row in component_rows)
        total_row = dominance_row(
            WEAK_SCALE,
            prime_modulus,
            "TOTAL",
            active_total,
            full_total,
            half_total,
        )
        total_row["active_row_start"] = active_row_start
        total_row["active_row_stop"] = (
            active_row_start + parameters["row_count"])
        total_row["active_row_start_offset"] = (
            active_row_start - parameters["row_count"])
        dominance_rows.append(total_row)
        for row in [*component_rows, total_row]:
            if not row["dominates_one_half_signed_full"]:
                failure_rows.append(row)
    slacks = [
        row["dominance_slack_above_one_half"]
        for row in dominance_rows
    ]
    return {
        "scale_modulus": WEAK_SCALE,
        "row_count": parameters["row_count"],
        "ell_freeze": parameters["ell_freeze"],
        "active_row_start": active_row_start,
        "active_row_stop": active_row_start + parameters["row_count"],
        "active_row_start_offset": active_row_start - parameters["row_count"],
        "divisor_range": parameters["divisor_range"],
        "prime_count": len({
            row["prime_modulus"] for row in dominance_rows
        }),
        "dominance_row_count": len(dominance_rows),
        "component_row_count": sum(
            1 for row in dominance_rows if row["label"] != "TOTAL"),
        "degree5_total_row_count": sum(
            1 for row in dominance_rows if row["label"] == "TOTAL"),
        "dominance_slack_sign_counts": sign_counts(slacks),
        "all_rows_dominate_one_half_signed_full": all(
            row["dominates_one_half_signed_full"]
            for row in dominance_rows),
        "minimum_dominance_slack_above_one_half": min(slacks),
        "maximum_dominance_slack_above_one_half": max(slacks),
        "weakest_dominance_row": min(
            dominance_rows,
            key=lambda row: row["dominance_slack_above_one_half"]),
        "strongest_dominance_row": max(
            dominance_rows,
            key=lambda row: row["dominance_slack_above_one_half"]),
        "failure_rows": failure_rows,
    }


def build_receipt():
    parameters = scale_parameters(WEAK_SCALE)
    window_summaries = [
        summarize_active_row_start(active_row_start)
        for active_row_start in active_row_starts()
    ]
    all_failures = []
    for summary in window_summaries:
        all_failures.extend(summary["failure_rows"])
    weakest = min(
        (summary["weakest_dominance_row"] for summary in window_summaries),
        key=lambda row: row["dominance_slack_above_one_half"])
    strongest = max(
        (summary["strongest_dominance_row"] for summary in window_summaries),
        key=lambda row: row["dominance_slack_above_one_half"])
    row_count = sum(
        summary["dominance_row_count"] for summary in window_summaries)
    component_count = sum(
        summary["component_row_count"] for summary in window_summaries)
    total_count = sum(
        summary["degree5_total_row_count"] for summary in window_summaries)
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
        "status": "STRESS_degree5_active_window_translation_dominance",
        "question": (
            "Does the weak-block degree-5 active/full dominance target depend "
            "delicately on the exact active row interval [35,70), or does it "
            "survive small translations of that row window?"),
        "scale_modulus": WEAK_SCALE,
        "threshold": THRESHOLD,
        "base_parameters": {
            "row_count": parameters["row_count"],
            "ell_freeze": parameters["ell_freeze"],
            "active_row_start": parameters["row_count"],
            "active_row_stop": 2 * parameters["row_count"],
            "divisor_range": parameters["divisor_range"],
        },
        "active_row_start_offsets": ROW_START_OFFSETS,
        "active_row_starts": active_row_starts(),
        "window_summaries": window_summaries,
        "prime_count_per_window": window_summaries[0]["prime_count"],
        "window_count": len(window_summaries),
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
            "If the weak-block one-prime degree-5 dominance phenomenon is "
            "not only a fitted active-row interval effect, nearby translated "
            "row starts should retain positive slack above one half."),
        "falsifier": (
            "Any checked component or degree-5 total row for active row starts "
            "33 through 37 whose signed full contribution is negative but "
            "whose active/full ratio is at or below one half, or any row "
            "losing the negative signed-full premise, is a concrete finite "
            "falsifier for this active-window translation stress."),
        "decision": (
            "The weak-scale active-window translation stress survives on the "
            "checked window: every component and degree-5 total row for "
            "active row starts 33 through 37 retains positive active/full "
            "dominance slack above one half.  This reduces concern that the "
            "finite weak-block result is only an exact active interval fit, "
            "but it remains finite perturbation evidence rather than a "
            "theorem."),
        "finite_active_window_translation_stress_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
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
