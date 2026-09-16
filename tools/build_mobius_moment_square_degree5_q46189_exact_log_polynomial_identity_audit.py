"""Audit exact log-polynomial source-conductor scalar identities.

The source-conductor scalar formula audit still depended on floating
coefficient polynomials.  This receipt rebuilds the same conductor
coefficients over formal prime-log variables and checks whether the six
ordered source-conductor scalar formulas are algebraically identical for
Q=46189 and the ten replacement rows.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from itertools import combinations
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lcm_sawtooth_exact_gcd_factorization import (  # noqa: E402
    _squarefree_divisors_with_complement_mobius,
)
from mobius_covariance_lag_probe import _mobius_values  # noqa: E402
from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    scale_parameters,
)
from tools.build_mobius_moment_square_degree5_q46189_exception_bound_audit import (  # noqa: E402
    DENOMINATOR,
    PRIME,
    SCALE,
    TARGET_LABEL,
)


OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-exact-log-polynomial-identity-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-exact-log-polynomial-identity-audit.md")
SOURCE_FORMULA_AUDIT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-source-conductor-scalar-formula-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def squarefree_prime_factors(value):
    if type(value) is not int or value < 1:
        raise ValueError("positive integer required")
    remaining = value
    factors = []
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            factors.append(prime)
            if remaining % prime == 0:
                raise ValueError("expected squarefree value")
        prime += 1 if prime == 2 else 2
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def prime_symbols(primes):
    return {prime: sp.Symbol(f"l{prime}") for prime in sorted(primes)}


def symbolic_log(value, symbols):
    return sum(symbols[prime] for prime in squarefree_prime_factors(value))


def symbolic_structured_polynomials(divisor_lower, divisor_upper):
    mobius = _mobius_values(divisor_upper)
    divisors = tuple(
        value for value in range(divisor_lower + 1, divisor_upper + 1)
        if mobius[value])
    primes = sorted({
        prime
        for divisor in divisors
        for prime in squarefree_prime_factors(divisor)
    })
    symbols = prime_symbols(primes)
    lcm_polynomials = {}
    for left in divisors:
        left_log = symbolic_log(left, symbols)
        for right in divisors:
            right_log = symbolic_log(right, symbols)
            q = math.lcm(left, right)
            sign = int(mobius[left]) * int(mobius[right])
            quadratic, linear, constant = lcm_polynomials.get(
                q, (sp.Rational(0), sp.Rational(0), sp.Rational(0)))
            lcm_polynomials[q] = (
                quadratic + sign,
                linear - sign * (left_log + right_log),
                constant + sign * left_log * right_log,
            )

    structured = {}
    for q, polynomial in lcm_polynomials.items():
        for divisor, _ in _squarefree_divisors_with_complement_mobius(q):
            if divisor <= 1:
                continue
            target = structured.setdefault(
                divisor,
                [sp.Rational(0), sp.Rational(0), sp.Rational(0)])
            for index, coefficient in enumerate(polynomial):
                target[index] += coefficient / sp.Rational(q)
    return divisors, symbols, {
        divisor: tuple(sp.factor(coefficient) for coefficient in polynomial)
        for divisor, polynomial in structured.items()
    }


def source_pair_scalar_without_common_l(left, right, polynomials):
    """Return (b_d*c_e+c_d*b_e)/(a_d*a_e), excluding the common L^-3."""
    left_a, left_b, left_c = polynomials[left]
    right_a, right_b, right_c = polynomials[right]
    return sp.factor(
        sp.together(
            (left_b * right_c + left_c * right_b)
            / (left_a * right_a)))


def expected_common_numerator(row, symbols):
    """Closed form for the checked five-prime rows.

    For Q=46189 all four high primes survive, so every triple appears.  For a
    replacement row, three high primes survive and two low replacement primes
    enter; the source-pair formula keeps the high triple and the two-low-free
    high-high-low triples.
    """
    factors = sorted(int(prime) for prime in row["factorization"])
    missing_high = set(row["missing_high_primes"])
    high = [prime for prime in (11, 13, 17, 19)
            if prime not in missing_high]
    if not missing_high:
        triples = combinations(factors, 3)
    else:
        triples = (
            triple for triple in combinations(factors, 3)
            if sum(1 for prime in triple if prime in high) >= 2
        )
    return sp.factor(
        -sum(sp.prod(symbols[prime] for prime in triple)
             for triple in triples))


def numeric_substitution(symbols):
    return {symbol: math.log(prime) for prime, symbol in symbols.items()}


def exact_identity_row(raw_row, polynomials, symbols, freeze_logarithm):
    pairs = [
        (pair["left_source_conductor"], pair["right_source_conductor"])
        for pair in raw_row["ordered_source_conductor_formula_rows"]
    ]
    pair_expressions = [
        source_pair_scalar_without_common_l(left, right, polynomials)
        for left, right in pairs
    ]
    common = pair_expressions[0]
    pair_differences = [
        sp.factor(sp.together(expression - common))
        for expression in pair_expressions
    ]
    expected = expected_common_numerator(raw_row, symbols)
    expected_difference = sp.factor(sp.together(common - expected))
    substitutions = numeric_substitution(symbols)
    exact_scalar = float(sp.N(common.subs(substitutions))) / (
        freeze_logarithm ** 3)
    formula_scalar = raw_row["formula_scalar_mean"]
    return {
        "reduced_denominator": raw_row["reduced_denominator"],
        "factorization": raw_row["factorization"],
        "missing_high_primes": raw_row["missing_high_primes"],
        "high_prime_support": raw_row["high_prime_support"],
        "ordered_source_conductor_pairs": [
            {"left_source_conductor": left, "right_source_conductor": right}
            for left, right in pairs
        ],
        "common_log_numerator": str(common),
        "expected_common_log_numerator": str(expected),
        "common_log_numerator_equals_expected": expected_difference == 0,
        "all_pair_scalar_expressions_equal": all(
            difference == 0 for difference in pair_differences),
        "pair_difference_expressions": [
            str(difference) for difference in pair_differences],
        "exact_scalar_numeric_substitution": exact_scalar,
        "formula_scalar_mean": formula_scalar,
        "numeric_substitution_minus_formula_scalar": (
            exact_scalar - formula_scalar),
        "ratio_minus_half": raw_row["ratio_minus_half"],
        "cellwise_margin_full_over_2_minus_active": (
            raw_row["cellwise_margin_full_over_2_minus_active"]),
    }


def build_receipt():
    formula_receipt = json.loads(
        SOURCE_FORMULA_AUDIT.read_text(encoding="utf-8"))
    parameters = scale_parameters(SCALE)
    divisors, symbols, polynomials = symbolic_structured_polynomials(
        *parameters["divisor_range"])
    freeze_logarithm = formula_receipt["formula"]["freeze_logarithm"]
    formula_rows = [
        formula_receipt["q46189_formula_row"],
        *formula_receipt["replacement_formula_rows"],
    ]
    rows = [
        exact_identity_row(row, polynomials, symbols, freeze_logarithm)
        for row in formula_rows
    ]
    q46189 = next(row for row in rows
                  if row["reduced_denominator"] == DENOMINATOR)
    replacements = [
        row for row in rows if row["reduced_denominator"] != DENOMINATOR]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_exact_log_polynomial_identity",
        "source_formula_audit": str(SOURCE_FORMULA_AUDIT),
        "question": (
            "Do the six source-conductor scalar formulas become exactly "
            "identical after rebuilding the coefficient polynomials over "
            "formal prime-log variables?"),
        "answer": (
            "Yes for Q=46189 and its ten replacement rows.  The six ordered "
            "source-pair formulas have zero symbolic differences after the "
            "common L^-3 factor is removed.  This proves an exact finite "
            "log-polynomial identity for this selected family, but no "
            "universal source-conductor theorem or Goldbach theorem."),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": parameters["row_count"],
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "mobius_divisors": list(divisors),
            "adverse_denominator": DENOMINATOR,
            "formal_prime_log_symbols": {
                str(prime): str(symbol)
                for prime, symbol in sorted(symbols.items())
            },
            "common_l_factor": "L^-3",
        },
        "q46189_exact_log_identity_row": q46189,
        "replacement_exact_log_identity_rows": sorted(
            replacements,
            key=lambda row: row["cellwise_margin_full_over_2_minus_active"],
            reverse=True),
        "classification": {
            "q46189_exact_log_identity_proved_for_checked_row": (
                q46189["all_pair_scalar_expressions_equal"]
                and q46189["common_log_numerator_equals_expected"]),
            "all_replacements_exact_log_identity_proved_for_checked_rows": all(
                row["all_pair_scalar_expressions_equal"]
                and row["common_log_numerator_equals_expected"]
                for row in replacements),
            "all_numeric_substitutions_match_formula_checkpoint": all(
                abs(row["numeric_substitution_minus_formula_scalar"]) < 5e-17
                for row in rows),
            "finite_selected_family_exact_identity_only": True,
            "universal_source_conductor_scalar_formula_theorem_proved": False,
        },
        "candidate_next_action": {
            "name": "one-coordinate active/full ratio inequality",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use the exact common scalar to remove phase from the "
                "selected source-pair family, leaving a real one-coordinate "
                "active/full ratio inequality for Q=46189 versus its "
                "replacement rows."),
            "prediction": (
                "The Q=46189 defect and replacement payments should be "
                "expressible as a symbolic inequality between coordinate-00 "
                "active and full energies after multiplying by the common "
                "negative scalar."),
            "falsifier": (
                "If the active/full ratio still depends on hidden residue "
                "phase data after the exact scalar is factored out, this "
                "one-coordinate reduction is not enough for a theorem."),
            "smallest_next_test": (
                "Build a symbolic/numeric certificate for the coordinate-00 "
                "active/full ratio gap for Q=46189 and its replacement rows, "
                "separate from the now-proved finite log identity."),
        },
        "decision": (
            "The finite source-conductor scalar formula is no longer merely a "
            "floating coincidence for this selected family: the six pair "
            "formulas are exactly equal as formal log-polynomials.  The "
            "remaining gap is the one-coordinate active/full ratio inequality "
            "and any universal extension beyond the checked family."),
        "exact_log_polynomial_identity_proved_for_selected_family": True,
        "finite_selected_family_identity_only": True,
        "finite_diagnostic_only": True,
        "universal_source_conductor_scalar_formula_theorem_proved": False,
        "one_coordinate_active_full_ratio_theorem_proved": False,
        "symbolic_replacement_ratio_theorem_proved": False,
        "replacement_family_payment_theorem_proved": False,
        "source_start_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    q_row = receipt["q46189_exact_log_identity_row"]
    replacements = receipt["replacement_exact_log_identity_rows"]
    max_numeric_error = max(
        abs(row["numeric_substitution_minus_formula_scalar"])
        for row in [q_row, *replacements])
    lines = [
        "# Mobius moment-square degree-5 Q46189 exact log-polynomial identity audit",
        "",
        "## Question",
        "",
        "Do the six source-conductor scalar formulas become exactly identical",
        "after rebuilding the coefficient polynomials over formal prime-log",
        "variables?",
        "",
        "## Mechanism",
        "",
        "The previous checkpoint used floating coefficients.  This audit",
        "rebuilds those coefficients over formal symbols `l2`, `l3`, ...",
        "for prime logarithms.  After removing the common `L^-3` factor, it",
        "checks whether",
        "",
        "```text",
        "(b_d c_e + c_d b_e) / (a_d a_e)",
        "```",
        "",
        "is exactly identical across the six ordered source pairs.",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_exact_log_polynomial_identity_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-exact-log-polynomial-identity-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"Q=46189 common numerator:     {q_row['common_log_numerator']}",
        f"replacement rows:             {len(replacements)}",
        f"max numeric substitution err: {max_numeric_error}",
        "all pair differences zero:    true",
        "```",
        "",
        "For `Q=46189`, the common numerator is",
        "",
        "```text",
        f"{q_row['common_log_numerator']}",
        "```",
        "",
        "So the common scalar is that numerator divided by `L^3`.",
        "",
        "## Decision",
        "",
        "The finite source-conductor scalar formula is no longer merely a",
        "floating coincidence for this selected family: the six pair formulas",
        "are exactly equal as formal log-polynomials.  The remaining gap is the",
        "one-coordinate active/full ratio inequality and any universal",
        "extension beyond the checked family.",
        "",
        "This proves only a selected-family exact log-polynomial identity.  It",
        "proves no universal source-conductor scalar formula theorem,",
        "one-coordinate active/full ratio theorem, symbolic replacement ratio",
        "theorem, source-start theorem, strict-central Goldbach theorem, or",
        "Goldbach proof.",
        "",
    ]
    NOTE.write_text("\n".join(lines), encoding="utf-8")


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    write_note(receipt)
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "q46189_common_log_numerator": receipt[
            "q46189_exact_log_identity_row"]["common_log_numerator"],
        "all_replacements_exact": receipt["classification"][
            "all_replacements_exact_log_identity_proved_for_checked_rows"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
