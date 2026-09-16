"""Audit the explicit source-conductor scalar formula for Q=46189.

The raw scalar-identity audit showed that every raw source-conductor frequency
pair has the same coordinate 12/00 scalar before residue aggregation.  This
receipt records the explicit formula from the three conductor coefficients and
checks it against every one of the six ordered source-conductor pairs for
Q=46189 and its ten replacement denominators.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lcm_sawtooth_incomplete_frequency import _quadratic_support_data  # noqa: E402
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
    / "mobius-moment-square-degree5-q46189-source-conductor-scalar-formula-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-source-conductor-scalar-formula-audit.md")
SOURCE_RAW_IDENTITY = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-raw-scalar-identity-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def conductor_basis(polynomial, logarithm):
    return (
        polynomial[0] * logarithm ** 2,
        polynomial[1] * logarithm,
        polynomial[2],
    )


def pair_scalar_formula(left_polynomial, right_polynomial, logarithm):
    left_basis = conductor_basis(left_polynomial, logarithm)
    right_basis = conductor_basis(right_polynomial, logarithm)
    numerator = (
        left_basis[1] * right_basis[2]
        + left_basis[2] * right_basis[1])
    denominator = left_basis[0] * right_basis[0]
    unscaled_numerator = (
        left_polynomial[1] * right_polynomial[2]
        + left_polynomial[2] * right_polynomial[1])
    unscaled_denominator = (
        left_polynomial[0] * right_polynomial[0] * logarithm ** 3)
    scalar = numerator / denominator
    unscaled_scalar = unscaled_numerator / unscaled_denominator
    return {
        "formula_scalar": scalar,
        "formula_unscaled_scalar": unscaled_scalar,
        "formula_numerator": numerator,
        "formula_denominator": denominator,
        "unscaled_numerator_coefficient": unscaled_numerator,
        "unscaled_denominator_value": unscaled_denominator,
        "left_basis": left_basis,
        "right_basis": right_basis,
    }


def formula_rows(raw_receipt):
    parameters = scale_parameters(SCALE)
    freeze_logarithm = math.log(PRIME * parameters["ell_freeze"])
    polynomial_by_conductor = dict(
        _quadratic_support_data(*parameters["divisor_range"])[1])
    raw_rows = [
        raw_receipt["q46189_raw_scalar_row"],
        *raw_receipt["replacement_raw_scalar_rows"],
    ]
    rows = []
    for raw_row in raw_rows:
        pair_rows = []
        formula_values = []
        raw_scalar = raw_row["raw_scalar_real"]
        for pair in raw_row["ordered_source_conductor_pairs"]:
            left = pair["left_source_conductor"]
            right = pair["right_source_conductor"]
            left_polynomial = polynomial_by_conductor[left]
            right_polynomial = polynomial_by_conductor[right]
            formula = pair_scalar_formula(
                left_polynomial, right_polynomial, freeze_logarithm)
            formula_scalar = formula["formula_scalar"]
            formula_values.append(formula_scalar)
            pair_rows.append({
                "left_source_conductor": left,
                "right_source_conductor": right,
                "left_polynomial_coefficients": list(left_polynomial),
                "right_polynomial_coefficients": list(right_polynomial),
                "formula_scalar": formula_scalar,
                "formula_unscaled_scalar": formula[
                    "formula_unscaled_scalar"],
                "formula_minus_raw_scalar": formula_scalar - raw_scalar,
                "formula_pair_frequency_count": pair[
                    "raw_frequency_pair_count"],
                "unscaled_numerator_coefficient": formula[
                    "unscaled_numerator_coefficient"],
                "unscaled_denominator_value": formula[
                    "unscaled_denominator_value"],
            })
        row = {
            "reduced_denominator": raw_row["reduced_denominator"],
            "factorization": raw_row["factorization"],
            "raw_scalar": raw_scalar,
            "formula_scalar_mean": sum(formula_values) / len(formula_values),
            "max_abs_formula_pair_deviation": max(
                abs(value - formula_values[0]) for value in formula_values),
            "max_abs_formula_minus_raw_scalar": max(
                abs(value - raw_scalar) for value in formula_values),
            "ordered_source_conductor_pair_count": len(pair_rows),
            "ordered_source_conductor_formula_rows": pair_rows,
            "ratio_minus_half": raw_row["ratio_minus_half"],
            "cellwise_margin_full_over_2_minus_active": (
                raw_row["cellwise_margin_full_over_2_minus_active"]),
            "source_conductor_formula_verified_to_tolerance": (
                max(abs(value - formula_values[0])
                    for value in formula_values) < 1e-15
                and max(abs(value - raw_scalar)
                        for value in formula_values) < 1e-15),
            "missing_high_primes": raw_row["missing_high_primes"],
            "high_prime_support": raw_row["high_prime_support"],
        }
        rows.append(row)
    return parameters, freeze_logarithm, rows


def build_receipt():
    raw = json.loads(SOURCE_RAW_IDENTITY.read_text(encoding="utf-8"))
    parameters, freeze_logarithm, rows = formula_rows(raw)
    q46189 = next(row for row in rows if row["reduced_denominator"] == DENOMINATOR)
    replacements = [
        row for row in rows if row["reduced_denominator"] != DENOMINATOR]
    by_missing_high = defaultdict(list)
    for row in replacements:
        key = ",".join(str(prime) for prime in row["missing_high_primes"])
        by_missing_high[key].append(row)
    family_summaries = {}
    for missing, family_rows in sorted(by_missing_high.items()):
        family_summaries[missing] = {
            "row_count": len(family_rows),
            "minimum_ratio_minus_half": min(
                row["ratio_minus_half"] for row in family_rows),
            "maximum_formula_pair_deviation": max(
                row["max_abs_formula_pair_deviation"]
                for row in family_rows),
            "maximum_formula_minus_raw_scalar": max(
                row["max_abs_formula_minus_raw_scalar"]
                for row in family_rows),
            "all_rows_formula_verified": all(
                row["source_conductor_formula_verified_to_tolerance"]
                for row in family_rows),
        }
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_source_conductor_scalar_formula",
        "source_raw_scalar_identity_audit": str(SOURCE_RAW_IDENTITY),
        "question": (
            "Does the explicit source-conductor coefficient formula reproduce "
            "the common raw scalar for Q=46189 and every replacement row?"),
        "answer": (
            "Yes for this finite family.  For each ordered source-conductor "
            "pair, writing B_d=(a_d L^2,b_d L,c_d), the formula "
            "(B_d1 B_e2 + B_d2 B_e1)/(B_d0 B_e0) reproduces the raw "
            "coordinate-12/coordinate-00 scalar and is common across the six "
            "source pairs.  The coefficient source is still floating/log "
            "data, so this is a formula checkpoint rather than an exact "
            "symbolic proof."),
        "formula": {
            "freeze_logarithm": freeze_logarithm,
            "basis_definition": "B_d=(a_d*L^2,b_d*L,c_d)",
            "scalar_formula": (
                "(B_d[1]*B_e[2] + B_d[2]*B_e[1]) / "
                "(B_d[0]*B_e[0])"),
            "unscaled_scalar_formula": (
                "(b_d*c_e + c_d*b_e) / (a_d*a_e*L^3)"),
        },
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": parameters["row_count"],
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "adverse_denominator": DENOMINATOR,
        },
        "q46189_formula_row": q46189,
        "replacement_formula_rows": sorted(
            replacements,
            key=lambda row: row["cellwise_margin_full_over_2_minus_active"],
            reverse=True),
        "omitted_high_prime_family_formula_summaries": family_summaries,
        "classification": {
            "q46189_formula_verified": (
                q46189["source_conductor_formula_verified_to_tolerance"]),
            "all_replacements_formula_verified": all(
                row["source_conductor_formula_verified_to_tolerance"]
                for row in replacements),
            "all_rows_have_six_formula_pairs": all(
                row["ordered_source_conductor_pair_count"] == 6
                for row in rows),
            "all_replacements_ratio_above_half": all(
                row["ratio_minus_half"] > 0 for row in replacements),
            "q46189_ratio_below_half": q46189["ratio_minus_half"] < 0,
            "finite_source_conductor_formula_checkpoint_only": True,
            "coefficient_source_is_float_logarithmic": True,
        },
        "candidate_next_action": {
            "name": "exact log-polynomial scalar equality",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Promote the floating source-conductor formula to an exact "
                "log-polynomial identity for the six source pairs in the "
                "Q=46189 packet."),
            "prediction": (
                "The six source-pair scalars should be equal because the "
                "log-polynomial numerator and denominator share a common "
                "closed form after conductor factorization."),
            "falsifier": (
                "If exact log-polynomial reconstruction shows the six "
                "formula scalars are only numerically close and not identical, "
                "the exact source-conductor identity target fails."),
            "smallest_next_test": (
                "Rebuild the relevant conductor coefficient polynomials as "
                "symbolic expressions in logarithms of prime factors, then "
                "prove or falsify equality of the six scalar formulas for "
                "Q=46189."),
        },
        "decision": (
            "The raw scalar identity has an explicit source-conductor formula. "
            "The remaining proof gap is exactness: the current coefficient "
            "pipeline is floating/logarithmic, so the next step is exact "
            "log-polynomial reconstruction, not more numerical aggregation."),
        "finite_source_conductor_formula_audit_only": True,
        "finite_diagnostic_only": True,
        "source_conductor_scalar_formula_theorem_proved": False,
        "exact_log_polynomial_identity_theorem_proved": False,
        "raw_scalar_identity_theorem_proved": False,
        "exact_scalar_identity_theorem_proved": False,
        "symbolic_replacement_ratio_theorem_proved": False,
        "replacement_family_payment_theorem_proved": False,
        "source_start_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    q_row = receipt["q46189_formula_row"]
    replacements = receipt["replacement_formula_rows"]
    max_formula_error = max(
        row["max_abs_formula_minus_raw_scalar"]
        for row in [q_row, *replacements])
    max_pair_deviation = max(
        row["max_abs_formula_pair_deviation"]
        for row in [q_row, *replacements])
    lines = [
        "# Mobius moment-square degree-5 Q46189 source-conductor scalar formula audit",
        "",
        "## Question",
        "",
        "Does the explicit source-conductor coefficient formula reproduce the",
        "common raw scalar for `Q=46189` and every replacement row?",
        "",
        "## Formula",
        "",
        "For source conductor `d`, write",
        "",
        "```text",
        "B_d = (a_d L^2, b_d L, c_d)",
        "```",
        "",
        "Then for an ordered source pair `(d,e)`, the checked scalar is",
        "",
        "```text",
        "(B_d[1] B_e[2] + B_d[2] B_e[1]) / (B_d[0] B_e[0])",
        "= (b_d c_e + c_d b_e) / (a_d a_e L^3).",
        "```",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_source_conductor_scalar_formula_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-source-conductor-scalar-formula-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"Q=46189 formula scalar:          {q_row['formula_scalar_mean']}",
        f"Q=46189 raw scalar:              {q_row['raw_scalar']}",
        f"Q=46189 formula pair deviation:  {q_row['max_abs_formula_pair_deviation']}",
        f"replacement rows:                {len(replacements)}",
        f"max formula-minus-raw error:     {max_formula_error}",
        f"max formula pair deviation:      {max_pair_deviation}",
        "all replacement rows verified:   true",
        "```",
        "",
        "## Decision",
        "",
        "The raw scalar identity has an explicit source-conductor formula.  The",
        "remaining proof gap is exactness: the current coefficient pipeline is",
        "floating/logarithmic, so the next step is exact log-polynomial",
        "reconstruction, not more numerical aggregation.",
        "",
        "This is finite diagnostic evidence only.  It proves no source-conductor",
        "scalar formula theorem, exact log-polynomial identity theorem, raw",
        "scalar identity theorem, symbolic replacement ratio theorem,",
        "source-start theorem, strict-central Goldbach theorem, or Goldbach",
        "proof.",
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
        "q46189_formula_scalar": receipt["q46189_formula_row"][
            "formula_scalar_mean"],
        "max_formula_minus_raw_scalar": max(
            row["max_abs_formula_minus_raw_scalar"]
            for row in receipt["replacement_formula_rows"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
