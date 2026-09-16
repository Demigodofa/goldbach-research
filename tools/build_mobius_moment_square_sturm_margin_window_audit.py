"""Audit the usable Sturm-margin window for serialized half-frame polynomials."""

import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


SOURCE_CURVE = Path("evidence/mobius-moment-square-half-frame-curve-audit.json")
PROVENANCE = Path("evidence/mobius-moment-square-coefficient-provenance-audit.json")
OUTPUT = Path("evidence/mobius-moment-square-sturm-margin-window-audit.json")
TIGHT_MARGIN = sp.Rational(427, 1000)
ROBUST_MARGIN = sp.Rational(21, 50)
BRACKET_DENOMINATOR = 10**6


def rational_poly_from_coefficients(coefficients, variable):
    polynomial = sum(
        sp.Rational(str(coefficient)) * variable ** degree
        for degree, coefficient in enumerate(coefficients))
    return sp.Poly(polynomial, variable, domain=sp.QQ)


def root_count_for_shift(coefficients, margin):
    variable = sp.symbols("t")
    polynomial = rational_poly_from_coefficients(coefficients, variable)
    shifted = sp.Poly(polynomial.as_expr() - margin, variable, domain=sp.QQ)
    return int(sp.polys.polytools.count_roots(
        shifted, sp.S.NegativeInfinity, sp.S.Infinity))


def polynomial_minimum(coefficients, precision=80):
    variable = sp.symbols("t")
    polynomial = rational_poly_from_coefficients(coefficients, variable)
    derivative = polynomial.diff()
    candidates = [sp.Float(0, precision)]
    for root in sp.nroots(derivative.as_expr(), n=precision, maxsteps=200):
        if abs(sp.im(root)) < sp.Float("1e-50"):
            candidates.append(sp.re(root))

    evaluations = []
    for parameter in candidates:
        value = sp.N(polynomial.as_expr().subs(variable, parameter), precision)
        evaluations.append((value, parameter))
    evaluations.sort(key=lambda item: item[0])
    return evaluations[0], evaluations[:5]


def decimal_string(value, digits=40):
    return str(sp.N(value, digits))


def margin_bracket(value, denominator=BRACKET_DENOMINATOR):
    scaled = int(sp.floor(value * denominator))
    return sp.Rational(scaled, denominator), sp.Rational(scaled + 1, denominator)


def source_rows():
    receipt = json.loads(SOURCE_CURVE.read_text(encoding="utf-8"))
    return {
        row["scale_modulus"]: row["polynomial_coefficients_low_to_high"]
        for row in receipt["scale_results"]
    }


def provenance_rows():
    receipt = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    return {
        row["scale_modulus"]: [
            degree_row["half_frame_coefficient"]
            for degree_row in row["degree_coefficients"]]
        for row in receipt["scale_results"]
    }


def coefficient_family_receipt(scale, family_name, coefficients):
    (minimum_value, minimizing_parameter), evaluations = polynomial_minimum(
        coefficients)
    floor_margin, ceiling_margin = margin_bracket(minimum_value)
    return {
        "scale_modulus": scale,
        "coefficient_family": family_name,
        "critical_margin_estimate": float(minimum_value),
        "critical_margin_estimate_decimal": decimal_string(minimum_value),
        "minimizing_parameter_estimate": float(minimizing_parameter),
        "minimizing_parameter_estimate_decimal": decimal_string(
            minimizing_parameter, digits=30),
        "slack_above_tight_margin": float(minimum_value - TIGHT_MARGIN),
        "slack_above_tight_margin_decimal": decimal_string(
            minimum_value - TIGHT_MARGIN),
        "slack_above_robust_margin": float(minimum_value - ROBUST_MARGIN),
        "slack_above_robust_margin_decimal": decimal_string(
            minimum_value - ROBUST_MARGIN),
        "tight_margin_root_count": root_count_for_shift(
            coefficients, TIGHT_MARGIN),
        "robust_margin_root_count": root_count_for_shift(
            coefficients, ROBUST_MARGIN),
        "critical_margin_floor_1e6_rational": str(floor_margin),
        "critical_margin_floor_1e6_root_count": root_count_for_shift(
            coefficients, floor_margin),
        "critical_margin_ceiling_1e6_rational": str(ceiling_margin),
        "critical_margin_ceiling_1e6_root_count": root_count_for_shift(
            coefficients, ceiling_margin),
        "smallest_stationary_evaluations": [
            {
                "value_decimal": decimal_string(value),
                "parameter_decimal": decimal_string(parameter, digits=30),
            }
            for value, parameter in evaluations
        ],
    }


def scale_receipt(scale, source_coefficients, provenance_coefficients):
    source = coefficient_family_receipt(
        scale, "source_curve_serialized", source_coefficients)
    provenance = coefficient_family_receipt(
        scale, "coefficient_provenance_serialized", provenance_coefficients)
    return {
        "scale_modulus": scale,
        "source_curve_serialized": source,
        "coefficient_provenance_serialized": provenance,
        "provenance_minus_source_critical_margin": (
            provenance["critical_margin_estimate"]
            - source["critical_margin_estimate"]),
        "both_serializations_root_free_at_robust_margin": (
            source["robust_margin_root_count"] == 0
            and provenance["robust_margin_root_count"] == 0),
        "both_serializations_root_free_at_tight_margin": (
            source["tight_margin_root_count"] == 0
            and provenance["tight_margin_root_count"] == 0),
    }


def build_receipt():
    source_by_scale = source_rows()
    provenance_by_scale = provenance_rows()
    rows = [
        scale_receipt(
            scale, source_by_scale[scale], provenance_by_scale[scale])
        for scale in sorted(source_by_scale)
    ]
    weakest_source = min(
        (row["source_curve_serialized"] for row in rows),
        key=lambda item: item["critical_margin_estimate"])
    weakest_provenance = min(
        (row["coefficient_provenance_serialized"] for row in rows),
        key=lambda item: item["critical_margin_estimate"])
    weakest_gap = min(
        rows,
        key=lambda row: row["provenance_minus_source_critical_margin"])
    return {
        "status": "MEASURE_serialized_sturm_margin_window",
        "question": (
            "How much actual serialized-coefficient margin separates the "
            "tight 427/1000 Sturm certificate from the robust 21/50 "
            "certificate, and which row controls the window?"),
        "source_curve_audit": str(SOURCE_CURVE),
        "coefficient_provenance_audit": str(PROVENANCE),
        "coefficient_interpretation": (
            "Each decimal coefficient is rationalized with Rational(str(x)) "
            "before Sturm/root-count and high-precision stationary-point "
            "calculation.  This audits serialized polynomial families, not "
            "an exact symbolic active/full Gram theorem."),
        "tight_margin": float(TIGHT_MARGIN),
        "tight_margin_rational": str(TIGHT_MARGIN),
        "robust_margin": float(ROBUST_MARGIN),
        "robust_margin_rational": str(ROBUST_MARGIN),
        "critical_margin_bracket_denominator": BRACKET_DENOMINATOR,
        "scale_results": rows,
        "all_source_curve_serialized_root_free_at_tight_margin": all(
            row["source_curve_serialized"]["tight_margin_root_count"] == 0
            for row in rows),
        "all_provenance_serialized_root_free_at_tight_margin": all(
            row["coefficient_provenance_serialized"][
                "tight_margin_root_count"] == 0
            for row in rows),
        "all_source_curve_serialized_root_free_at_robust_margin": all(
            row["source_curve_serialized"]["robust_margin_root_count"] == 0
            for row in rows),
        "all_provenance_serialized_root_free_at_robust_margin": all(
            row["coefficient_provenance_serialized"][
                "robust_margin_root_count"] == 0
            for row in rows),
        "weakest_source_curve_serialized_margin": weakest_source,
        "weakest_provenance_serialized_margin": weakest_provenance,
        "largest_provenance_below_source_gap_row": weakest_gap,
        "decision": (
            "The controlling scale is M=167.  The rationalized source-curve "
            "serialized polynomial has critical margin about "
            "0.42701050918658, barely above 427/1000.  The independently "
            "serialized coefficient-provenance polynomial has critical "
            "margin about 0.42698189905807, about 1.81e-5 below 427/1000.  "
            "The robust 21/50 margin still leaves about 0.006981899 of "
            "provenance slack.  A universal route must therefore prove an "
            "unnormalized pointwise lower bound with explicit coefficient "
            "control, not rely on the tight rounded margin."),
        "finite_serialized_margin_window_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
        "critical_margin_theorem_proved": False,
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
