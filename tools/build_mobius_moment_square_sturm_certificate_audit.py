"""Build a Sturm certificate for checked half-frame curve polynomials."""

import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


INPUT = Path("evidence/mobius-moment-square-half-frame-curve-audit.json")
OUTPUT = Path("evidence/mobius-moment-square-sturm-certificate-audit.json")
CERTIFIED_MARGIN = sp.Rational(427, 1000)


def rational_polynomial(coefficients, variable):
    """Return the exact rational polynomial from JSON decimal coefficients."""
    terms = [
        sp.Rational(str(coefficient)) * variable ** degree
        for degree, coefficient in enumerate(coefficients)
    ]
    return sp.Poly(sum(terms), variable, domain=sp.QQ)


def sturm_certificate_row(source_row, margin=CERTIFIED_MARGIN):
    variable = sp.symbols("t")
    polynomial = rational_polynomial(
        source_row["polynomial_coefficients_low_to_high"], variable)
    shifted = sp.Poly(polynomial.as_expr() - margin, variable, domain=sp.QQ)
    real_root_count = sp.polys.polytools.count_roots(
        shifted, sp.S.NegativeInfinity, sp.S.Infinity)
    sturm_sequence = sp.polys.polytools.sturm(shifted.as_expr(), variable)
    sample_at_zero = shifted.eval(0)
    leading_coefficient = shifted.LC()
    leading_positive = bool(leading_coefficient > 0)
    sample_positive = bool(sample_at_zero > 0)
    root_free = int(real_root_count) == 0
    return {
        "scale_modulus": source_row["scale_modulus"],
        "certified_margin": float(margin),
        "certified_margin_rational": str(margin),
        "shifted_polynomial_degree": shifted.degree(),
        "shifted_polynomial_leading_coefficient_positive": leading_positive,
        "shifted_polynomial_value_at_zero_positive": sample_positive,
        "shifted_polynomial_value_at_zero_rational": str(sample_at_zero),
        "shifted_polynomial_real_root_count": int(real_root_count),
        "sturm_sequence_length": len(sturm_sequence),
        "certificate_passes": (
            leading_positive and sample_positive and root_free),
        "source_half_frame_curve_minimum": (
            source_row["half_frame_curve_minimum"]),
        "source_half_frame_curve_minimizing_parameter": (
            source_row["half_frame_curve_minimizing_parameter"]),
    }


def build_receipt():
    source = json.loads(INPUT.read_text(encoding="utf-8"))
    rows = [
        sturm_certificate_row(row)
        for row in source["scale_results"]
    ]
    weakest_source = min(
        rows, key=lambda row: row["source_half_frame_curve_minimum"])
    return {
        "status": "CERTIFY_checked_moment_square_half_frame_curve_margin",
        "question": (
            "Can the recorded checked half-frame curve polynomials be "
            "certified positive by a rational Sturm/root-count certificate, "
            "rather than only by floating minimization?"),
        "source_audit": str(INPUT),
        "certified_margin": float(CERTIFIED_MARGIN),
        "certified_margin_rational": str(CERTIFIED_MARGIN),
        "scale_results": rows,
        "all_shifted_polynomials_root_free": all(
            row["shifted_polynomial_real_root_count"] == 0 for row in rows),
        "all_certificates_pass": all(
            row["certificate_passes"] for row in rows),
        "weakest_source_curve_row": weakest_source,
        "decision": (
            "For the recorded rationalized degree-8 half-frame polynomials, "
            "P_M(t)-0.427 has zero real roots, positive leading coefficient, "
            "and positive value at t=0 on every checked scale.  This upgrades "
            "the finite curve check from optimizer evidence to an algebraic "
            "Sturm certificate for the recorded polynomials.  The universal "
            "proof target remains an analytic derivation of the coefficient "
            "family or a scale where this certificate fails."),
        "finite_polynomial_certificate_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
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
