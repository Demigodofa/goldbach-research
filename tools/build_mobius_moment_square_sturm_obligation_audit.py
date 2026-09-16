"""Extract robust Sturm sign obligations for half-frame polynomials."""

import json
import math
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


SOURCE_CURVE = Path("evidence/mobius-moment-square-half-frame-curve-audit.json")
PROVENANCE = Path("evidence/mobius-moment-square-coefficient-provenance-audit.json")
OUTPUT = Path("evidence/mobius-moment-square-sturm-obligation-audit.json")
ROBUST_MARGIN = sp.Rational(21, 50)


def sign(value):
    if value > 0:
        return "+"
    if value < 0:
        return "-"
    return "0"


def variation_count(signs):
    nonzero = [item for item in signs if item != "0"]
    return sum(
        left != right
        for left, right in zip(nonzero, nonzero[1:]))


def rational_poly_from_coefficients(coefficients, variable, margin=ROBUST_MARGIN):
    polynomial = sum(
        sp.Rational(str(coefficient)) * variable ** degree
        for degree, coefficient in enumerate(coefficients))
    return sp.Poly(polynomial - margin, variable, domain=sp.QQ)


def sturm_obligations_for_coefficients(coefficients, margin=ROBUST_MARGIN):
    variable = sp.symbols("t")
    polynomial = rational_poly_from_coefficients(
        coefficients, variable, margin)
    sturm_sequence = [
        sp.Poly(expression, variable, domain=sp.QQ)
        for expression in sp.polys.polytools.sturm(
            polynomial.as_expr(), variable)
    ]
    obligations = []
    plus_signs = []
    minus_signs = []
    for index, sturm_polynomial in enumerate(sturm_sequence):
        degree = sturm_polynomial.degree()
        leading = sturm_polynomial.LC()
        plus = sign(leading)
        minus = sign(leading * ((-1) ** degree))
        plus_signs.append(plus)
        minus_signs.append(minus)
        leading_abs = abs(leading)
        obligations.append({
            "sequence_index": index,
            "degree": degree,
            "leading_coefficient_sign": plus,
            "plus_infinity_sign": plus,
            "minus_infinity_sign": minus,
            "leading_coefficient_abs_decimal": str(sp.N(leading_abs, 24)),
            "leading_coefficient_abs_log10": (
                math.log10(float(sp.N(leading_abs, 30)))
                if leading_abs else None),
            "leading_coefficient_nonzero": leading != 0,
        })

    return {
        "sturm_sequence_length": len(sturm_sequence),
        "obligations": obligations,
        "plus_infinity_sign_word": "".join(plus_signs),
        "minus_infinity_sign_word": "".join(minus_signs),
        "plus_infinity_variations": variation_count(plus_signs),
        "minus_infinity_variations": variation_count(minus_signs),
        "real_root_count_from_variations": (
            variation_count(minus_signs) - variation_count(plus_signs)),
        "all_leading_coefficients_nonzero": all(
            row["leading_coefficient_nonzero"] for row in obligations),
        "zero_leading_coefficient_indices": [
            row["sequence_index"] for row in obligations
            if not row["leading_coefficient_nonzero"]],
    }


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
    source = sturm_obligations_for_coefficients(source_coefficients)
    provenance = sturm_obligations_for_coefficients(provenance_coefficients)
    weakest_source = min(
        source["obligations"],
        key=lambda row: row["leading_coefficient_abs_log10"])
    weakest_provenance = min(
        provenance["obligations"],
        key=lambda row: row["leading_coefficient_abs_log10"])
    return {
        "scale_modulus": scale,
        "source_curve_serialized": source,
        "coefficient_provenance_serialized": provenance,
        "source_and_provenance_sign_words_match": (
            source["plus_infinity_sign_word"]
            == provenance["plus_infinity_sign_word"]
            and source["minus_infinity_sign_word"]
            == provenance["minus_infinity_sign_word"]),
        "source_and_provenance_variation_counts_match": (
            source["plus_infinity_variations"]
            == provenance["plus_infinity_variations"]
            and source["minus_infinity_variations"]
            == provenance["minus_infinity_variations"]),
        "source_variation_certificate_passes": (
            source["plus_infinity_variations"]
            == source["minus_infinity_variations"]
            and source["real_root_count_from_variations"] == 0
            and source["all_leading_coefficients_nonzero"]),
        "provenance_variation_certificate_passes": (
            provenance["plus_infinity_variations"]
            == provenance["minus_infinity_variations"]
            and provenance["real_root_count_from_variations"] == 0
            and provenance["all_leading_coefficients_nonzero"]),
        "weakest_source_leading_obligation": weakest_source,
        "weakest_provenance_leading_obligation": weakest_provenance,
    }


def build_receipt():
    source_by_scale, provenance_by_scale = load_coefficients()
    rows = [
        scale_receipt(
            scale, source_by_scale[scale], provenance_by_scale[scale])
        for scale in sorted(source_by_scale)
    ]
    flattened = []
    for row in rows:
        for family_key in (
                "source_curve_serialized",
                "coefficient_provenance_serialized"):
            family = row[family_key]
            for obligation in family["obligations"]:
                flattened.append({
                    "scale_modulus": row["scale_modulus"],
                    "coefficient_family": family_key,
                    **obligation,
                })
    weakest = min(
        flattened,
        key=lambda row: row["leading_coefficient_abs_log10"])
    sign_word_pairs = sorted({
        (
            row["source_curve_serialized"]["plus_infinity_sign_word"],
            row["source_curve_serialized"]["minus_infinity_sign_word"],
        )
        for row in rows
    })
    return {
        "status": "EXTRACT_robust_sturm_sign_obligations",
        "question": (
            "At robust margin 21/50, what exact nonzero leading-coefficient "
            "sign obligations must a universal Sturm proof preserve?"),
        "source_curve_audit": str(SOURCE_CURVE),
        "coefficient_provenance_audit": str(PROVENANCE),
        "robust_margin": float(ROBUST_MARGIN),
        "robust_margin_rational": str(ROBUST_MARGIN),
        "coefficient_interpretation": (
            "Each decimal coefficient is rationalized with Rational(str(x)); "
            "the obligations are for SymPy's canonical Sturm sequence of the "
            "serialized shifted polynomial P(t)-21/50."),
        "scale_results": rows,
        "all_source_and_provenance_sign_words_match": all(
            row["source_and_provenance_sign_words_match"] for row in rows),
        "all_source_and_provenance_variation_counts_match": all(
            row["source_and_provenance_variation_counts_match"]
            for row in rows),
        "all_source_variation_certificates_pass": all(
            row["source_variation_certificate_passes"] for row in rows),
        "all_provenance_variation_certificates_pass": all(
            row["provenance_variation_certificate_passes"] for row in rows),
        "distinct_checked_sign_word_pair_count": len(sign_word_pairs),
        "distinct_checked_sign_word_pairs": sign_word_pairs,
        "total_checked_leading_coefficient_obligations": len(flattened),
        "zero_leading_coefficient_obligation_count": sum(
            not row["leading_coefficient_nonzero"] for row in flattened),
        "weakest_checked_leading_obligation": weakest,
        "decision": (
            "The robust finite Sturm certificate has no zero leading "
            "coefficient signs in either serialization.  The weakest checked "
            "nondegeneracy is the final degree-0 Sturm constant at M=167 in "
            "the coefficient-provenance serialization, with absolute value "
            "about 8.004e-19.  Thus the theorem target is a parametric "
            "Sturm-sign/nonzero-leading-coefficient theorem at margin 21/50, "
            "not a single fixed sign word and not acceptance by finite "
            "evidence."),
        "finite_sturm_obligation_diagnostic_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
        "sturm_obligation_theorem_proved": False,
        "robust_sturm_variation_chamber_theorem_proved": False,
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
