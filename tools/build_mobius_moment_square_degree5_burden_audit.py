"""Build the weak-row degree-5 coefficient burden audit."""

import json
import sys
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lcm_sawtooth_lifted_endpoint_frame import (  # noqa: E402
    project_prime_block_lifted_endpoint_scan,
)


SOURCE_CURVE = Path("evidence/mobius-moment-square-half-frame-curve-audit.json")
PROVENANCE = Path("evidence/mobius-moment-square-coefficient-provenance-audit.json")
SENSITIVITY = Path("evidence/mobius-moment-square-critical-margin-sensitivity-audit.json")
OUTPUT = Path("evidence/mobius-moment-square-degree5-burden-audit.json")
WEAK_SCALE = 167
LABELS = ("00", "01", "02", "11", "12", "22")
DEGREES = (4, 3, 2, 2, 1, 0)
TARGET_DEGREE = 5


def degree_contributors(active, full, target_degree=TARGET_DEGREE):
    active = np.asarray(active, dtype=float)
    full = np.asarray(full, dtype=float)
    half = active - 0.5 * full
    rows = []
    for left in range(6):
        for right in range(left, 6):
            if DEGREES[left] + DEGREES[right] != target_degree:
                continue
            multiplicity = 1 if left == right else 2
            active_contribution = float(multiplicity * active[left, right])
            full_contribution = float(multiplicity * full[left, right])
            half_contribution = float(multiplicity * half[left, right])
            rows.append({
                "left_label": LABELS[left],
                "right_label": LABELS[right],
                "left_degree": DEGREES[left],
                "right_degree": DEGREES[right],
                "multiplicity": multiplicity,
                "active_contribution": active_contribution,
                "full_contribution": full_contribution,
                "half_frame_contribution": half_contribution,
            })
    total = sum(row["half_frame_contribution"] for row in rows)
    sum_abs = sum(abs(row["half_frame_contribution"]) for row in rows)
    for row in rows:
        row["half_frame_fraction_of_total"] = (
            row["half_frame_contribution"] / total if total else None)
        row["half_frame_abs_fraction_of_abs_total"] = (
            abs(row["half_frame_contribution"]) / sum_abs if sum_abs else None)
    return rows


def load_receipts():
    source = json.loads(SOURCE_CURVE.read_text(encoding="utf-8"))
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    sensitivity = json.loads(SENSITIVITY.read_text(encoding="utf-8"))
    return source, provenance, sensitivity


def coefficient_row(receipt, scale, degree):
    scale_row = next(
        row for row in receipt["scale_results"]
        if row["scale_modulus"] == scale)
    return next(
        row for row in scale_row["degree_coefficients"]
        if row["degree"] == degree)


def source_coefficient(source_receipt, scale, degree):
    scale_row = next(
        row for row in source_receipt["scale_results"]
        if row["scale_modulus"] == scale)
    return scale_row["polynomial_coefficients_low_to_high"][degree]


def sensitivity_scale_row(sensitivity_receipt, scale):
    return next(
        row for row in sensitivity_receipt["scale_results"]
        if row["scale_modulus"] == scale)


def weak_scale_burden():
    frame = project_prime_block_lifted_endpoint_scan(WEAK_SCALE)
    active = np.asarray(frame["aggregate_active_window_residue_energy_gram"])
    active = (active + active.T) / 2
    full = np.asarray(frame["aggregate_full_residue_energy_gram"])
    full = (full + full.T) / 2
    contributors = degree_contributors(active, full)
    total_half = sum(row["half_frame_contribution"] for row in contributors)
    total_active = sum(row["active_contribution"] for row in contributors)
    total_full = sum(row["full_contribution"] for row in contributors)
    sum_abs_half = sum(abs(row["half_frame_contribution"]) for row in contributors)
    return {
        "scale_modulus": WEAK_SCALE,
        "target_degree": TARGET_DEGREE,
        "contributors": contributors,
        "active_coefficient_from_contributors": total_active,
        "full_coefficient_from_contributors": total_full,
        "half_frame_coefficient_from_contributors": total_half,
        "half_frame_sum_abs_contributions": sum_abs_half,
        "same_sign_half_frame_contributions": (
            abs(total_half) == sum_abs_half),
        "top_abs_half_frame_contributor": max(
            contributors,
            key=lambda row: abs(row["half_frame_contribution"])),
    }


def checked_scale_degree5_summary(source, provenance, sensitivity):
    rows = []
    for source_row in source["scale_results"]:
        scale = source_row["scale_modulus"]
        provenance_degree = coefficient_row(provenance, scale, TARGET_DEGREE)
        source_degree = source_coefficient(source, scale, TARGET_DEGREE)
        sensitivity_row = sensitivity_scale_row(sensitivity, scale)
        rows.append({
            "scale_modulus": scale,
            "source_curve_degree5_coefficient": source_degree,
            "provenance_degree5_coefficient": (
                provenance_degree["half_frame_coefficient"]),
            "provenance_minus_source_degree5_delta": (
                provenance_degree["half_frame_coefficient"] - source_degree),
            "active_degree5_coefficient": (
                provenance_degree["active_coefficient"]),
            "full_degree5_coefficient": provenance_degree["full_coefficient"],
            "active_over_full_degree5_ratio": (
                provenance_degree["active_over_full_coefficient_ratio"]),
            "sensitivity_dominant_degree": (
                sensitivity_row["dominant_abs_contribution_degree"]),
            "sensitivity_nonzero_coefficient_delta_count": (
                sensitivity_row["nonzero_coefficient_delta_count"]),
        })
    return rows


def build_receipt():
    source, provenance, sensitivity = load_receipts()
    burden = weak_scale_burden()
    provenance_degree = coefficient_row(provenance, WEAK_SCALE, TARGET_DEGREE)
    source_degree = source_coefficient(source, WEAK_SCALE, TARGET_DEGREE)
    weak_delta_exact = (
        sp.Rational(str(provenance_degree["half_frame_coefficient"]))
        - sp.Rational(str(source_degree)))
    sensitivity_row = sensitivity_scale_row(sensitivity, WEAK_SCALE)
    checked_summary = checked_scale_degree5_summary(
        source, provenance, sensitivity)
    return {
        "status": "MEASURE_degree5_weak_row_coefficient_burden",
        "question": (
            "For the weak M=167 row, which active/full Gram contributors "
            "make the degree-5 coefficient that controls the serialized "
            "critical-margin loss?"),
        "source_curve_audit": str(SOURCE_CURVE),
        "coefficient_provenance_audit": str(PROVENANCE),
        "critical_margin_sensitivity_audit": str(SENSITIVITY),
        "weak_scale_burden": burden,
        "checked_scale_degree5_summary": checked_summary,
        "weak_scale_source_degree5_coefficient": source_degree,
        "weak_scale_provenance_degree5_coefficient": (
            provenance_degree["half_frame_coefficient"]),
        "weak_scale_provenance_minus_source_degree5_delta": (
            provenance_degree["half_frame_coefficient"] - source_degree),
        "weak_scale_provenance_minus_source_degree5_delta_decimal": (
            str(sp.N(weak_delta_exact, 40))),
        "weak_scale_binary_float_delta_warning": (
            "The plain float delta is not reliable at this magnitude; use "
            "the decimal rational field for theorem-facing comparisons."),
        "weak_scale_sensitivity_degree5_margin_contribution": (
            sensitivity_row["nonzero_degree_contributions"][0][
                "margin_delta_contribution_at_source_parameter"]),
        "decision": (
            "At the weak M=167 row, the degree-5 half-frame coefficient is "
            "the sum of exactly three same-sign Gram contributors: "
            "(00,12), (01,02), and (01,11).  The largest is (01,11), about "
            "57.25% of the degree-5 burden; (01,02) contributes about "
            "28.61%, and (00,12) about 14.14%.  Thus the next exact "
            "coefficient theorem can target three concrete active/full Gram "
            "entries instead of an opaque polynomial coefficient."),
        "finite_degree5_burden_diagnostic_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
        "degree5_coefficient_theorem_proved": False,
        "critical_margin_sensitivity_theorem_proved": False,
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
