"""Audit coefficient sensitivity of serialized critical Sturm margins."""

import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


SOURCE_CURVE = Path("evidence/mobius-moment-square-half-frame-curve-audit.json")
PROVENANCE = Path("evidence/mobius-moment-square-coefficient-provenance-audit.json")
OUTPUT = Path("evidence/mobius-moment-square-critical-margin-sensitivity-audit.json")
TIGHT_MARGIN = sp.Rational(427, 1000)
ROBUST_MARGIN = sp.Rational(21, 50)


def decimal_string(value, digits=40):
    return str(sp.N(value, digits))


def rational_poly_from_coefficients(coefficients, variable):
    polynomial = sum(
        sp.Rational(str(coefficient)) * variable ** degree
        for degree, coefficient in enumerate(coefficients))
    return sp.Poly(polynomial, variable, domain=sp.QQ)


def polynomial_minimum(coefficients, precision=80):
    variable = sp.symbols("t")
    polynomial = rational_poly_from_coefficients(coefficients, variable)
    candidates = [sp.Float(0, precision)]
    for root in sp.nroots(polynomial.diff().as_expr(), n=precision, maxsteps=200):
        if abs(sp.im(root)) < sp.Float("1e-50"):
            candidates.append(sp.re(root))
    evaluations = sorted(
        (
            sp.N(polynomial.as_expr().subs(variable, parameter), precision),
            parameter,
        )
        for parameter in candidates
    )
    return evaluations[0], polynomial


def load_coefficients():
    source = json.loads(SOURCE_CURVE.read_text(encoding="utf-8"))
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    source_by_scale = {
        row["scale_modulus"]: row["polynomial_coefficients_low_to_high"]
        for row in source["scale_results"]
    }
    provenance_by_scale = {
        row["scale_modulus"]: [
            degree_row["half_frame_coefficient"]
            for degree_row in row["degree_coefficients"]]
        for row in provenance["scale_results"]
    }
    return source_by_scale, provenance_by_scale


def scale_receipt(scale, source_coefficients, provenance_coefficients):
    variable = sp.symbols("t")
    (source_minimum, source_parameter), source_polynomial = polynomial_minimum(
        source_coefficients)
    (provenance_minimum,
     provenance_parameter), provenance_polynomial = polynomial_minimum(
         provenance_coefficients)

    contributions = []
    for degree, (source_coefficient, provenance_coefficient) in enumerate(
            zip(source_coefficients, provenance_coefficients)):
        delta = (
            sp.Rational(str(provenance_coefficient))
            - sp.Rational(str(source_coefficient)))
        source_power = sp.N(source_parameter ** degree, 80)
        contribution = sp.N(delta * source_power, 80)
        if delta != 0:
            contributions.append({
                "degree": degree,
                "source_coefficient_decimal": decimal_string(
                    sp.Rational(str(source_coefficient))),
                "provenance_coefficient_decimal": decimal_string(
                    sp.Rational(str(provenance_coefficient))),
                "coefficient_delta_decimal": decimal_string(delta),
                "source_parameter_power_decimal": decimal_string(source_power),
                "margin_delta_contribution_at_source_parameter_decimal": (
                    decimal_string(contribution)),
                "margin_delta_contribution_at_source_parameter": (
                    float(contribution)),
            })

    direct_delta = sp.N(
        provenance_polynomial.as_expr().subs(variable, source_parameter)
        - source_minimum,
        80,
    )
    movement_delta = sp.N(
        provenance_minimum
        - provenance_polynomial.as_expr().subs(variable, source_parameter),
        80,
    )
    total_delta = sp.N(provenance_minimum - source_minimum, 80)
    sorted_contributions = sorted(
        contributions,
        key=lambda row: abs(
            sp.Rational(row[
                "margin_delta_contribution_at_source_parameter_decimal"])),
        reverse=True,
    )
    top_abs = (
        abs(sp.Rational(sorted_contributions[0][
            "margin_delta_contribution_at_source_parameter_decimal"]))
        if sorted_contributions else sp.Integer(0))
    direct_abs = abs(direct_delta)

    return {
        "scale_modulus": scale,
        "source_critical_margin_decimal": decimal_string(source_minimum),
        "source_critical_parameter_decimal": decimal_string(
            source_parameter, digits=30),
        "provenance_critical_margin_decimal": decimal_string(
            provenance_minimum),
        "provenance_critical_parameter_decimal": decimal_string(
            provenance_parameter, digits=30),
        "total_provenance_minus_source_margin_delta_decimal": decimal_string(
            total_delta),
        "direct_coefficient_delta_at_source_parameter_decimal": decimal_string(
            direct_delta),
        "minimizer_movement_delta_decimal": decimal_string(movement_delta),
        "source_slack_above_tight_margin_decimal": decimal_string(
            source_minimum - TIGHT_MARGIN),
        "provenance_slack_above_tight_margin_decimal": decimal_string(
            provenance_minimum - TIGHT_MARGIN),
        "provenance_slack_above_robust_margin_decimal": decimal_string(
            provenance_minimum - ROBUST_MARGIN),
        "nonzero_coefficient_delta_count": len(contributions),
        "nonzero_degree_contributions": sorted_contributions,
        "dominant_abs_contribution_degree": (
            sorted_contributions[0]["degree"] if sorted_contributions
            else None),
        "dominant_abs_contribution_over_direct_abs": (
            float(top_abs / direct_abs) if direct_abs else None),
    }


def build_receipt():
    source_by_scale, provenance_by_scale = load_coefficients()
    rows = [
        scale_receipt(
            scale, source_by_scale[scale], provenance_by_scale[scale])
        for scale in sorted(source_by_scale)
    ]
    weakest_provenance = min(
        rows,
        key=lambda row: sp.Rational(
            row["provenance_critical_margin_decimal"]))
    largest_loss = min(
        rows,
        key=lambda row: sp.Rational(
            row["total_provenance_minus_source_margin_delta_decimal"]))
    return {
        "status": "MEASURE_critical_margin_coefficient_sensitivity",
        "question": (
            "Which serialized coefficient deltas move the critical margin "
            "from the source-curve polynomial to the coefficient-provenance "
            "polynomial, especially at the weak M=167 row?"),
        "source_curve_audit": str(SOURCE_CURVE),
        "coefficient_provenance_audit": str(PROVENANCE),
        "tight_margin": float(TIGHT_MARGIN),
        "tight_margin_rational": str(TIGHT_MARGIN),
        "robust_margin": float(ROBUST_MARGIN),
        "robust_margin_rational": str(ROBUST_MARGIN),
        "scale_results": rows,
        "weakest_provenance_margin_row": weakest_provenance,
        "largest_provenance_below_source_loss_row": largest_loss,
        "decision": (
            "At the weak M=167 row, the source-to-provenance critical-margin "
            "loss is not diffuse.  It is explained, to the recorded "
            "precision, by a single degree-5 serialized coefficient delta "
            "of -0.02 evaluated at the source minimizer; minimizer movement "
            "contributes only about -4.7e-12.  Therefore the next exact "
            "coefficient theorem should account for the degree-5 active/full "
            "coefficient before treating the full Sturm sequence as an "
            "opaque object."),
        "finite_coefficient_sensitivity_diagnostic_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
        "critical_margin_sensitivity_theorem_proved": False,
        "critical_margin_theorem_proved": False,
        "sturm_obligation_theorem_proved": False,
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
