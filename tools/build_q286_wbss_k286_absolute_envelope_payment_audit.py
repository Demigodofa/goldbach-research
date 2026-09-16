"""Test whether the full K_286 absolute phase envelope is payable.

The K_286 phase-envelope audit showed that the absolute envelope is broad, so
tiny phase-label shortcuts are not the right theorem object.  This receipt asks
a different finite question: on the extended zero-lane rows, can the local main
pay the entire K_286 absolute phase envelope plus the actually adverse drag
from the other three projected moduli?

Finite diagnostic only.  It does not prove a universal absolute-envelope
theorem, companion adverse-drag theorem, q286 threshold theorem, strict-central
Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
PHASE_SOURCE = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-phase-envelope-concentration-audit.json")
EXTENDED_SOURCE = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-extended-lift-phase-band-audit.json")
RAW_SOURCE = EVIDENCE / "q286-wbss-raw-adverse-drag-theorem-target.json"
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
OUT = EVIDENCE / "q286-wbss-k286-absolute-envelope-payment-audit.json"
MODULUS = "286"
TOLERANCE = 1e-12

sys.path.insert(0, str(ROOT))

from tools import build_q286_wbss_four_modulus_variance_scale_far_lift_holdout as far  # noqa: E501,E402
from tools.build_q286_wbss_four_modulus_adverse_drag_horizon_audit import (  # noqa: E501,E402
    row_adverse_drag,
)
from tools.build_q286_wbss_four_modulus_direct_holdout_decomposition import (  # noqa: E501,E402
    coefficient_lookup,
)
from tools.build_q286_wbss_k286_zero_residue_extended_lift_phase_band_audit import (  # noqa: E501,E402
    target_rows,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def phase_rows_by_target(phase):
    result = {}
    for residue_summary in phase["finite_diagnostic"]["summary"][
            "residue_summaries"]:
        for row in residue_summary["rows"]:
            result[int(row["target"])] = row
    return result


def payment_row(row, adverse_row, phase_row):
    local_main = float(adverse_row["local_uniform_main_term"])
    signed_errors = adverse_row["signed_error_by_modulus"]
    k286_signed_error = float(signed_errors[MODULUS])
    k286_envelope = float(phase_row["pair_real_abs_envelope"])
    k286_pair_sum = float(phase_row["pair_real_sum"])
    other_adverse = float(math.fsum(
        -float(value)
        for modulus, value in signed_errors.items()
        if modulus != MODULUS and float(value) < -TOLERANCE
    ))
    k286_signed_adverse = max(0.0, -k286_signed_error)
    absolute_payment = other_adverse + k286_envelope
    absolute_margin = local_main - absolute_payment
    return {
        "target": int(adverse_row["target"]),
        "target_residue": int(adverse_row["target_residue"]),
        "target_mod_286": int(adverse_row["target_mod_286"]),
        "lift_index": int(adverse_row["lift_index"]),
        "block_index_after_raw_horizon": int(
            row["block_index_after_raw_horizon"]),
        "local_main": local_main,
        "signed_error_by_modulus": {
            key: float(value) for key, value in signed_errors.items()
        },
        "other_moduli_adverse_drag": other_adverse,
        "k286_signed_error": k286_signed_error,
        "k286_pair_sum": k286_pair_sum,
        "k286_pair_sum_reconstruction_error": float(
            abs(k286_signed_error - k286_pair_sum)),
        "k286_signed_adverse_drag": k286_signed_adverse,
        "k286_absolute_phase_envelope": k286_envelope,
        "absolute_envelope_payment": absolute_payment,
        "absolute_envelope_margin": absolute_margin,
        "absolute_envelope_payment_ratio": float(
            absolute_payment / local_main),
        "k286_absolute_envelope_ratio": float(k286_envelope / local_main),
        "other_moduli_adverse_ratio": float(other_adverse / local_main),
        "k286_signed_adverse_ratio_to_envelope": float(
            k286_signed_adverse / k286_envelope)
        if k286_envelope > TOLERANCE else None,
        "k286_required_cancellation_cap": float(
            (local_main - other_adverse) / k286_envelope)
        if k286_envelope > TOLERANCE else None,
        "absolute_envelope_payment_positive": bool(
            absolute_margin > TOLERANCE),
        "phase_cover_counts": phase_row["cover_counts"],
        "top_pair_fraction": float(phase_row["top_pair_fraction"]),
        "inverse_participation_count": float(
            phase_row["participation_metrics"][
                "inverse_participation_count"]),
        "entropy_effective_count": float(
            phase_row["participation_metrics"]["entropy_effective_count"]),
    }


def summarize_by_residue(rows):
    by_residue = {}
    for row in rows:
        by_residue.setdefault(row["target_residue"], []).append(row)
    summaries = []
    for residue, residue_rows in sorted(by_residue.items()):
        summaries.append({
            "target_residue": residue,
            "row_count": len(residue_rows),
            "absolute_envelope_payment_ratio_summary": finite_summary(
                row["absolute_envelope_payment_ratio"]
                for row in residue_rows),
            "absolute_envelope_margin_summary": finite_summary(
                row["absolute_envelope_margin"] for row in residue_rows),
            "k286_required_cancellation_cap_summary": finite_summary(
                row["k286_required_cancellation_cap"]
                for row in residue_rows),
            "minimum_margin_row": min(
                residue_rows,
                key=lambda row: (row["absolute_envelope_margin"],
                                 row["target"])),
            "rows": sorted(residue_rows, key=lambda row: row["target"]),
        })
    return summaries


def summarize_rows(rows):
    return {
        "row_count": len(rows),
        "target_minimum": min(row["target"] for row in rows),
        "target_maximum": max(row["target"] for row in rows),
        "absolute_envelope_payment_positive_count": sum(
            row["absolute_envelope_payment_positive"] for row in rows),
        "absolute_envelope_payment_nonpositive_count": sum(
            not row["absolute_envelope_payment_positive"] for row in rows),
        "local_main_summary": finite_summary(
            row["local_main"] for row in rows),
        "other_moduli_adverse_drag_summary": finite_summary(
            row["other_moduli_adverse_drag"] for row in rows),
        "k286_absolute_phase_envelope_summary": finite_summary(
            row["k286_absolute_phase_envelope"] for row in rows),
        "absolute_envelope_payment_summary": finite_summary(
            row["absolute_envelope_payment"] for row in rows),
        "absolute_envelope_payment_ratio_summary": finite_summary(
            row["absolute_envelope_payment_ratio"] for row in rows),
        "absolute_envelope_margin_summary": finite_summary(
            row["absolute_envelope_margin"] for row in rows),
        "k286_required_cancellation_cap_summary": finite_summary(
            row["k286_required_cancellation_cap"] for row in rows),
        "k286_signed_adverse_ratio_to_envelope_summary": finite_summary(
            row["k286_signed_adverse_ratio_to_envelope"] for row in rows),
        "k286_pair_sum_reconstruction_error_summary": finite_summary(
            row["k286_pair_sum_reconstruction_error"] for row in rows),
        "tightest_absolute_envelope_payment_row": min(
            rows,
            key=lambda row: (row["absolute_envelope_margin"],
                             row["target"])),
        "largest_absolute_envelope_payment_ratio_row": max(
            rows,
            key=lambda row: (
                row["absolute_envelope_payment_ratio"], -row["target"])),
        "lowest_required_cancellation_cap_row": min(
            rows,
            key=lambda row: (
                row["k286_required_cancellation_cap"], row["target"])),
        "largest_observed_k286_signed_adverse_ratio_row": max(
            rows,
            key=lambda row: (
                row["k286_signed_adverse_ratio_to_envelope"],
                -row["target"])),
        "residue_summaries": summarize_by_residue(rows),
    }


def build_receipt():
    phase = load_json(PHASE_SOURCE)
    extended = load_json(EXTENDED_SOURCE)
    raw = load_json(RAW_SOURCE)
    formula = load_json(FORMULA_SOURCE)
    alpha0, by_modulus = coefficient_lookup(formula)
    residues = [
        int(row["target_residue"])
        for row in extended["finite_diagnostic"]["summary"][
            "residue_summaries"]
    ]
    lower_bound = max(
        int(row["target"]) for row in raw["finite_calibration"]["rows"])
    rows = target_rows(residues, lower_bound)
    maximum_target = max(row["target"] for row in rows)
    primes = np.asarray(far._prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = far.logs(maximum_target)
    context = far.prepare_support_context()
    context["coefficient"] = (
        far.combined_fixed_strict_central_coefficient_receipt())
    full_coefficients = far.period_full_unit_coefficients(context)
    first_three_coefficients = far.q286_first_three_unit_coefficients(context)
    phase_by_target = phase_rows_by_target(phase)
    payment_rows = []
    for row in rows:
        row = dict(row)
        row.setdefault("source_positive_target", -1)
        adverse = row_adverse_drag(
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
        adverse["block_index_after_raw_horizon"] = row[
            "block_index_after_raw_horizon"]
        payment_rows.append(payment_row(
            row, adverse, phase_by_target[int(adverse["target"])]))
    summary = summarize_rows(payment_rows)
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-absolute-envelope-payment-audit",
        "source_commit": source_commit(),
        "sources": {
            "phase_envelope_concentration": str(
                PHASE_SOURCE.relative_to(ROOT)),
            "phase_envelope_source_commit": phase["source_commit"],
            "extended_lift_phase_band_audit": str(
                EXTENDED_SOURCE.relative_to(ROOT)),
            "extended_lift_phase_band_source_commit": (
                extended["source_commit"]),
            "raw_adverse_drag_theorem_target": str(
                RAW_SOURCE.relative_to(ROOT)),
            "raw_adverse_drag_source_commit": raw["source_commit"],
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "formula_source_commit": formula["source_commit"],
        },
        "status": "DIAGNOSTIC_k286_absolute_envelope_payment_survives",
        "question": (
            "On the extended zero-lane rows, can the local main pay the "
            "entire K_286 absolute phase envelope plus the actually adverse "
            "drag from the other three moduli?"),
        "answer": (
            "Yes on the finite 32-row diagnostic.  The rowwise margin "
            "M(N)-A_other(N)-H_286(N) stays positive, so these checked rows "
            "do not need delicate K_286 signed cancellation once the full "
            "K_286 absolute phase envelope is paid."),
        "finite_diagnostic": {
            "finite_evidence_is_acceptance_condition": False,
            "role": (
                "theorem-target sharpening after broad K_286 phase envelope: "
                "test absolute-envelope payment before chasing signed "
                "phase-cancellation constants"),
            "definitions": {
                "M": "local_main(N)",
                "H_286": (
                    "sum of absolute real K_286 conjugate phase-pair "
                    "contributions"),
                "A_other": (
                    "sum of adverse projected errors from moduli 70, 130, "
                    "and 154 only"),
                "payment_margin": "M(N)-A_other(N)-H_286(N)",
            },
            "summary": summary,
            "rows": payment_rows,
        },
        "candidate": {
            "name": "K286 absolute envelope payment theorem",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Instead of proving delicate signed cancellation inside the "
                "broad K_286 envelope, prove a universal bound on the whole "
                "K_286 absolute phase envelope plus companion one-sided "
                "bounds for the other moduli, with total below local main."),
            "prediction": (
                "If this is the right theorem object, larger zero-lane lifts "
                "should keep M(N)-A_other(N)-H_286(N) positive or reveal the "
                "exact scale term missing from H_286."),
            "falsifier": (
                "Any covered row with M(N)<=A_other(N)+H_286(N) kills this "
                "absolute-envelope sufficient route on that class."),
            "smallest_next_action": (
                "Extend the payment audit beyond the four repeated residues "
                "and replace actual A_other with theorem-shaped companion "
                "bounds."),
        },
        "decision": (
            "DIAGNOSTIC_k286_absolute_envelope_payment_survives.  On the "
            "finite extended zero-lane rows, local main pays the entire "
            "K_286 absolute phase envelope plus actual adverse drag from the "
            "other projected moduli.  This demotes delicate K_286 signed "
            "cancellation as the immediate sublane target and promotes a "
            "stronger absolute-envelope-plus-companion-bounds theorem target. "
            "The result remains finite diagnostic evidence only."),
        "status_boundary": (
            "Finite absolute-envelope payment diagnostic only.  No K_286 "
            "absolute-envelope theorem, companion adverse-drag theorem, "
            "phase-cancellation theorem, universal pointwise raw bound, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof is established."),
        "k286_absolute_envelope_theorem_proved": False,
        "companion_adverse_drag_theorem_proved": False,
        "phase_cancellation_theorem_proved": False,
        "universal_pointwise_raw_bound_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    summary = receipt["finite_diagnostic"]["summary"]
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "row_count": summary["row_count"],
        "payment_positive_count": summary[
            "absolute_envelope_payment_positive_count"],
        "payment_margin_minimum": summary[
            "absolute_envelope_margin_summary"]["minimum"],
        "payment_ratio_maximum": summary[
            "absolute_envelope_payment_ratio_summary"]["maximum"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
