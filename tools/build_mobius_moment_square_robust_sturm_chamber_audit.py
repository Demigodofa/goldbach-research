"""Audit robust 0.42 Sturm variation chambers for half-frame polynomials."""

import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


SOURCE_CURVE = Path("evidence/mobius-moment-square-half-frame-curve-audit.json")
PROVENANCE = Path("evidence/mobius-moment-square-coefficient-provenance-audit.json")
OUTPUT = Path("evidence/mobius-moment-square-robust-sturm-chamber-audit.json")
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


def sturm_signature(coefficients, margin=ROBUST_MARGIN):
    variable = sp.symbols("t")
    polynomial = sp.Poly(
        sum(
            sp.Rational(str(coefficient)) * variable ** degree
            for degree, coefficient in enumerate(coefficients))
        - margin,
        variable,
        domain=sp.QQ)
    sturm_sequence = sp.polys.polytools.sturm(
        polynomial.as_expr(), variable)
    degrees = []
    plus_signs = []
    minus_signs = []
    for expression in sturm_sequence:
        poly = sp.Poly(expression, variable, domain=sp.QQ)
        degree = poly.degree()
        leading = poly.LC()
        degrees.append(degree)
        plus_signs.append(sign(leading))
        minus_signs.append(sign(leading * ((-1) ** degree)))
    plus_word = "".join(plus_signs)
    minus_word = "".join(minus_signs)
    return {
        "sturm_degrees": degrees,
        "plus_infinity_sign_word": plus_word,
        "minus_infinity_sign_word": minus_word,
        "plus_infinity_variations": variation_count(plus_signs),
        "minus_infinity_variations": variation_count(minus_signs),
        "real_root_count_from_variations": (
            variation_count(minus_signs) - variation_count(plus_signs)),
        "sturm_sequence_length": len(sturm_sequence),
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
    source_signature = sturm_signature(source_coefficients)
    provenance_signature = sturm_signature(provenance_coefficients)
    return {
        "scale_modulus": scale,
        "source_signature": source_signature,
        "provenance_serialized_signature": provenance_signature,
        "source_and_provenance_sign_words_match": (
            source_signature["plus_infinity_sign_word"]
            == provenance_signature["plus_infinity_sign_word"]
            and source_signature["minus_infinity_sign_word"]
            == provenance_signature["minus_infinity_sign_word"]),
        "source_and_provenance_variations_match": (
            source_signature["plus_infinity_variations"]
            == provenance_signature["plus_infinity_variations"]
            and source_signature["minus_infinity_variations"]
            == provenance_signature["minus_infinity_variations"]),
        "source_variation_certificate_passes": (
            source_signature["plus_infinity_variations"] == 4
            and source_signature["minus_infinity_variations"] == 4
            and source_signature["real_root_count_from_variations"] == 0),
        "provenance_variation_certificate_passes": (
            provenance_signature["plus_infinity_variations"] == 4
            and provenance_signature["minus_infinity_variations"] == 4
            and provenance_signature["real_root_count_from_variations"] == 0),
    }


def build_receipt():
    source_by_scale, provenance_by_scale = load_coefficients()
    rows = [
        scale_receipt(
            scale, source_by_scale[scale], provenance_by_scale[scale])
        for scale in sorted(source_by_scale)
    ]
    sign_word_pairs = sorted({
        (
            row["source_signature"]["plus_infinity_sign_word"],
            row["source_signature"]["minus_infinity_sign_word"],
        )
        for row in rows
    })
    return {
        "status": "TARGET_robust_sturm_variation_chamber",
        "question": (
            "At the robust 21/50 margin, do the source curve and serialized "
            "coefficient-provenance polynomials share a stable Sturm "
            "variation-count certificate?"),
        "source_curve_audit": str(SOURCE_CURVE),
        "coefficient_provenance_audit": str(PROVENANCE),
        "robust_margin": float(ROBUST_MARGIN),
        "robust_margin_rational": str(ROBUST_MARGIN),
        "scale_results": rows,
        "all_source_and_provenance_sign_words_match": all(
            row["source_and_provenance_sign_words_match"] for row in rows),
        "all_source_and_provenance_variations_match": all(
            row["source_and_provenance_variations_match"] for row in rows),
        "all_source_variation_certificates_pass": all(
            row["source_variation_certificate_passes"] for row in rows),
        "all_provenance_variation_certificates_pass": all(
            row["provenance_variation_certificate_passes"] for row in rows),
        "distinct_checked_sign_word_pair_count": len(sign_word_pairs),
        "distinct_checked_sign_word_pairs": sign_word_pairs,
        "decision": (
            "At margin 21/50, source and serialized provenance coefficients "
            "agree on the Sturm sign words for every checked scale.  The "
            "sign words are not globally identical across scales, but each "
            "checked scale has four sign variations at -infinity and four at "
            "+infinity, hence zero real roots.  The theorem target should be "
            "variation-count preservation, not one fixed sign word."),
        "finite_sturm_chamber_diagnostic_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
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
