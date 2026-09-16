"""Audit Sturm-margin sensitivity to coefficient serialization."""

import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


SOURCE_CURVE = Path("evidence/mobius-moment-square-half-frame-curve-audit.json")
PROVENANCE = Path("evidence/mobius-moment-square-coefficient-provenance-audit.json")
OUTPUT = Path("evidence/mobius-moment-square-sturm-margin-sensitivity-audit.json")
MARGINS = (sp.Rational(427, 1000), sp.Rational(42, 100))


def rational_poly_from_coefficients(coefficients, variable, margin):
    polynomial = sum(
        sp.Rational(str(coefficient)) * variable ** degree
        for degree, coefficient in enumerate(coefficients))
    return sp.Poly(polynomial - margin, variable, domain=sp.QQ)


def root_count_for_coefficients(coefficients, margin):
    variable = sp.symbols("t")
    polynomial = rational_poly_from_coefficients(
        coefficients, variable, margin)
    return int(sp.polys.polytools.count_roots(
        polynomial, sp.S.NegativeInfinity, sp.S.Infinity))


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


def margin_receipt(margin, source_by_scale, provenance_by_scale):
    rows = []
    for scale in sorted(source_by_scale):
        source_roots = root_count_for_coefficients(
            source_by_scale[scale], margin)
        provenance_roots = root_count_for_coefficients(
            provenance_by_scale[scale], margin)
        rows.append({
            "scale_modulus": scale,
            "source_curve_real_root_count": source_roots,
            "provenance_serialized_real_root_count": provenance_roots,
            "source_curve_root_free": source_roots == 0,
            "provenance_serialized_root_free": provenance_roots == 0,
        })
    return {
        "margin": float(margin),
        "margin_rational": str(margin),
        "rows": rows,
        "source_curve_all_root_free": all(
            row["source_curve_root_free"] for row in rows),
        "provenance_serialized_all_root_free": all(
            row["provenance_serialized_root_free"] for row in rows),
        "failing_provenance_scales": [
            row["scale_modulus"] for row in rows
            if not row["provenance_serialized_root_free"]],
    }


def build_receipt():
    source_by_scale = source_rows()
    provenance_by_scale = provenance_rows()
    margin_results = [
        margin_receipt(margin, source_by_scale, provenance_by_scale)
        for margin in MARGINS
    ]
    tight = margin_results[0]
    robust = margin_results[1]
    return {
        "status": "FALSIFY_tight_margin_from_serialized_provenance_coefficients",
        "question": (
            "Does the tight 0.427 Sturm margin survive when the polynomial "
            "is rebuilt from the serialized coefficient-provenance receipt, "
            "or is a more conservative cross-artifact margin required?"),
        "source_curve_audit": str(SOURCE_CURVE),
        "coefficient_provenance_audit": str(PROVENANCE),
        "margin_results": margin_results,
        "tight_source_curve_margin_passes": (
            tight["source_curve_all_root_free"]),
        "tight_provenance_serialized_margin_passes": (
            tight["provenance_serialized_all_root_free"]),
        "robust_source_curve_margin_passes": (
            robust["source_curve_all_root_free"]),
        "robust_provenance_serialized_margin_passes": (
            robust["provenance_serialized_all_root_free"]),
        "decision": (
            "The source curve coefficients remain root-free at margin 0.427, "
            "but the serialized coefficient-provenance reconstruction does "
            "not: M=167 has two real roots after the 0.427 shift.  The "
            "conservative margin 0.42 is root-free for both the source curve "
            "coefficients and the serialized provenance coefficients.  A "
            "universal proof must therefore use exact coefficient derivations "
            "or a robust margin, not rounded provenance floats at the tight "
            "margin."),
        "finite_serialization_sensitivity_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
        "tight_margin_serialized_provenance_theorem_proved": False,
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
