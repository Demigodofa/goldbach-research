"""Audit structured group payment for the Q=46189 phase defect.

The Q=46189 phase-defect audit falsified per-denominator nonadversity.  This
derived receipt asks whether the defect is paid by a narrow arithmetic family:
middle/far positive rows for the same component that contain exactly three of
the four high primes in 11*13*17*19.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    scale_parameters,
)
from tools.build_mobius_moment_square_degree5_q46189_exception_bound_audit import (  # noqa: E402
    DENOMINATOR,
    PRIME,
    SCALE,
    TARGET_LABEL,
)
from tools.build_mobius_moment_square_degree5_source_margin_denominator_audit import (  # noqa: E402
    label_rows_from_denominator,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _residue_cells_by_denominator,
)


OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-group-payment-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-group-payment-audit.md")
SOURCE_PHASE_DEFECT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-phase-defect-audit.json")
HIGH_PRIMES = (11, 13, 17, 19)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def factor_integer(value):
    n = value
    factors = {}
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors[str(divisor)] = factors.get(str(divisor), 0) + 1
            n //= divisor
        divisor += 1 if divisor == 2 else 2
    if n > 1:
        factors[str(n)] = factors.get(str(n), 0) + 1
    return factors


def clearance_family(reduced_denominator, threshold):
    if reduced_denominator < 2 * threshold:
        return "near_1_to_2"
    if reduced_denominator < 3 * threshold:
        return "middle_2_to_3"
    return "far_3_plus"


def compact_row(row, threshold, adverse_margin):
    factors = factor_integer(row["reduced_denominator"])
    support = {int(prime) for prime in factors}
    high_support = sorted(set(HIGH_PRIMES) & support)
    missing_high = sorted(set(HIGH_PRIMES) - support)
    margin = row["unnormalized_margin_full_over_2_minus_active"]
    return {
        "reduced_denominator": row["reduced_denominator"],
        "factorization": factors,
        "clearance_family": clearance_family(
            row["reduced_denominator"], threshold),
        "clearance_ratio_q_over_pA": row["reduced_denominator"] / threshold,
        "margin": margin,
        "payment_over_q46189_adverse": margin / adverse_margin,
        "high_prime_support": high_support,
        "missing_high_primes": missing_high,
        "small_prime_support": sorted(support - set(HIGH_PRIMES)),
    }


def margin_summary(rows, adverse_margin):
    positive_sum = sum(row["margin"] for row in rows if row["margin"] > 0)
    weakest = min(rows, key=lambda row: row["margin"], default=None)
    strongest = max(rows, key=lambda row: row["margin"], default=None)
    return {
        "row_count": len(rows),
        "positive_margin_sum": positive_sum,
        "payment_over_q46189_adverse": positive_sum / adverse_margin,
        "weakest_positive_payment_row": weakest,
        "strongest_positive_payment_row": strongest,
        "all_rows_individually_pay_defect": all(
            row["margin"] > adverse_margin for row in rows),
        "minimum_individual_payment_over_defect": (
            min(row["margin"] / adverse_margin for row in rows)
            if rows else None),
    }


def target_denominator_rows():
    parameters = scale_parameters(SCALE)
    row_count = parameters["row_count"]
    _, cells_by_denominator = _residue_cells_by_denominator(
        PRIME,
        row_count,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    rows = []
    for reduced_denominator, cells in sorted(cells_by_denominator.items()):
        for row in label_rows_from_denominator(
                reduced_denominator, cells, row_count, row_count):
            if row["label"] == TARGET_LABEL:
                rows.append(row)
    return parameters, rows


def build_receipt():
    phase = json.loads(SOURCE_PHASE_DEFECT.read_text(encoding="utf-8"))
    parameters, rows = target_denominator_rows()
    row_count = parameters["row_count"]
    threshold = PRIME * row_count
    q46189 = next(row for row in rows if row["reduced_denominator"] == DENOMINATOR)
    adverse_margin = -q46189["unnormalized_margin_full_over_2_minus_active"]
    middle_far_rows = [
        compact_row(row, threshold, adverse_margin)
        for row in rows
        if row["reduced_denominator"] >= 2 * threshold
    ]
    middle_far_positive = [
        row for row in middle_far_rows if row["margin"] > 0]
    replacement_rows = [
        row for row in middle_far_positive
        if len(row["high_prime_support"]) == 3
    ]
    by_missing_high = {}
    for row in replacement_rows:
        key = ",".join(str(prime) for prime in row["missing_high_primes"])
        by_missing_high.setdefault(key, []).append(row)
    family_summaries = {
        missing: margin_summary(group, adverse_margin)
        for missing, group in sorted(by_missing_high.items())
    }
    replacement_summary = margin_summary(replacement_rows, adverse_margin)
    all_middle_far_summary = margin_summary(
        middle_far_positive, adverse_margin)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_structured_group_payment",
        "source_phase_defect_audit": str(SOURCE_PHASE_DEFECT),
        "question": (
            "For the M=229, p=379, Q=46189 adverse denominator, do "
            "structured middle/far positive rows sharing three of the four "
            "high primes 11,13,17,19 already pay the defect without using "
            "total positivity?"),
        "answer": (
            "Yes for this finite ledger.  Ten positive middle/far rows contain "
            "exactly three of the four high primes from 11*13*17*19, and their "
            "sum is far larger than the Q=46189 adverse margin.  Stronger: "
            "each omitted-high-prime family separately pays the defect, and "
            "each individual replacement row is positive by more than the "
            "defect.  This is finite evidence for a replacement-family payment "
            "target, not a theorem."),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": row_count,
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "threshold_p_times_A": threshold,
            "adverse_denominator": DENOMINATOR,
            "adverse_denominator_factorization": factor_integer(DENOMINATOR),
            "q46189_half_threshold_defect": (
                phase["target_pair_summary"]["half_threshold_defect"]),
            "q46189_adverse_margin": adverse_margin,
        },
        "q46189_row": compact_row(q46189, threshold, adverse_margin),
        "middle_far_positive_summary": all_middle_far_summary,
        "replacement_family_definition": (
            "positive middle/far denominator rows for label 00,12 whose prime "
            "support contains exactly three of {11,13,17,19}"),
        "replacement_family_summary": replacement_summary,
        "replacement_family_rows": sorted(
            replacement_rows,
            key=lambda row: row["margin"],
            reverse=True),
        "omitted_high_prime_family_summaries": family_summaries,
        "classification": {
            "q46189_is_only_middle_far_negative_for_label": (
                sum(1 for row in middle_far_rows if row["margin"] < 0) == 1),
            "replacement_family_pays_defect": (
                replacement_summary["positive_margin_sum"] > adverse_margin),
            "each_omitted_high_prime_family_pays_defect": all(
                summary["positive_margin_sum"] > adverse_margin
                for summary in family_summaries.values()),
            "each_replacement_row_individually_pays_defect": (
                replacement_summary["all_rows_individually_pay_defect"]),
            "finite_group_payment_certificate_only": True,
        },
        "candidate_next_action": {
            "name": "replacement-family phase-defect payment theorem",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Replace one high prime in the adverse denominator tail by "
                "small-prime products that keep Q in the middle/far ledger, "
                "then prove the resulting grouped margins dominate the aligned "
                "negative denominator."),
            "prediction": (
                "For future source-admissible blocks, any Q-style aligned "
                "middle/far negative denominator with a high-prime tail should "
                "come with positive replacement families indexed by omitted "
                "high prime, and at least one family-level inequality should "
                "pay the phase defect pointwise."),
            "falsifier": (
                "A source-admissible block with a Q-style aligned negative "
                "middle/far denominator whose replacement families are absent "
                "or fail to dominate the defect falsifies this theorem target."),
            "smallest_next_test": (
                "Repeat this replacement-family ledger on the other tight "
                "sigma-band blocks, especially any block with middle/far "
                "adverse mass, and track whether omitted-high-prime family "
                "payment persists without total positivity."),
        },
        "decision": (
            "The Q=46189 exception has a sharper finite payment pattern: "
            "three-of-four high-prime replacement families pay the defect.  "
            "This narrows the theorem target from generic group payment to "
            "replacement-family phase-defect payment.  No universal pointwise "
            "estimate is proved."),
        "finite_group_payment_audit_only": True,
        "finite_diagnostic_only": True,
        "replacement_family_payment_theorem_proved": False,
        "phase_defect_payment_theorem_proved": False,
        "near_adverse_upper_bound_proved": False,
        "middle_far_lower_bound_proved": False,
        "clearance_family_theorem_proved": False,
        "source_start_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    fixture = receipt["fixture"]
    replacement = receipt["replacement_family_summary"]
    families = receipt["omitted_high_prime_family_summaries"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 group-payment audit",
        "",
        "## Question",
        "",
        "For the `M=229`, `p=379`, `Q=46189` adverse denominator, do",
        "structured middle/far positive rows sharing three of the four high",
        "primes `11,13,17,19` pay the defect without using total positivity?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_group_payment_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-group-payment-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"Q=46189 adverse margin:        {fixture['q46189_adverse_margin']}",
        f"replacement rows:              {replacement['row_count']}",
        f"replacement positive sum:       {replacement['positive_margin_sum']}",
        f"replacement payment / defect:   {replacement['payment_over_q46189_adverse']}",
        f"minimum row payment / defect:   {replacement['minimum_individual_payment_over_defect']}",
        "```",
        "",
        "Omitted-high-prime family payment ratios:",
        "",
        "```text",
    ]
    for missing, summary in families.items():
        lines.append(
            f"missing {missing}: {summary['payment_over_q46189_adverse']}")
    lines.extend([
        "```",
        "",
        "## Decision",
        "",
        "The finite payment pattern is sharper than generic group payment:",
        "three-of-four high-prime replacement families pay the `Q=46189`",
        "defect.  This narrows the possible theorem target to replacement-family",
        "phase-defect payment.",
        "",
        "This is still finite ledger evidence only.  It proves no replacement",
        "family payment theorem, phase-defect payment theorem, near-adverse",
        "upper bound, middle/far lower bound, clearance-family theorem,",
        "source-start theorem, strict-central Goldbach theorem, or Goldbach",
        "proof.",
        "",
    ])
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
        "replacement_payment_over_defect": (
            receipt["replacement_family_summary"][
                "payment_over_q46189_adverse"]),
        "minimum_replacement_row_payment_over_defect": (
            receipt["replacement_family_summary"][
                "minimum_individual_payment_over_defect"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
