"""Build the scalar-cancelled Q=46189 one-coordinate ratio ledger.

The exact log-polynomial audit removed the source-pair phase scalar as a
floating gap.  This receipt isolates what remains: for each checked
denominator, the signed margin is the positive scalar magnitude times the
coordinate-00 full energy times the one-coordinate active/full ratio gap.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_q46189_exception_bound_audit import (  # noqa: E402
    DENOMINATOR,
    PRIME,
    SCALE,
    TARGET_LABEL,
)


OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-one-coordinate-ratio-ledger-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-one-coordinate-ratio-ledger-audit.md")
SOURCE_SCALAR_COLLAPSE = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-scalar-collapse-audit.json")
SOURCE_EXACT_LOG_IDENTITY = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-exact-log-polynomial-identity-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def scalar_rows_by_denominator(receipt):
    rows = [
        receipt["q46189_scalar_row"],
        *receipt["replacement_scalar_rows"],
    ]
    return {row["reduced_denominator"]: row for row in rows}


def exact_rows_by_denominator(receipt):
    rows = [
        receipt["q46189_exact_log_identity_row"],
        *receipt["replacement_exact_log_identity_rows"],
    ]
    return {row["reduced_denominator"]: row for row in rows}


def one_coordinate_row(scalar_row, exact_row):
    scalar = exact_row["exact_scalar_numeric_substitution"]
    if scalar >= 0:
        raise ArithmeticError("expected negative scalar after exact identity")
    full_00 = scalar_row["full_contribution"] / scalar
    active_00 = scalar_row["one_coordinate_active_over_full_ratio"] * full_00
    ratio_gap = scalar_row["one_coordinate_active_over_full_ratio"] - 0.5
    scalar_cancelled_margin = (-scalar) * full_00 * ratio_gap
    source_margin = scalar_row["margin_full_over_2_minus_active"]
    return {
        "reduced_denominator": scalar_row["reduced_denominator"],
        "factorization": scalar_row["factorization"],
        "missing_high_primes": exact_row["missing_high_primes"],
        "high_prime_support": exact_row["high_prime_support"],
        "common_log_numerator": exact_row["common_log_numerator"],
        "exact_scalar_numeric_substitution": scalar,
        "positive_scalar_magnitude": -scalar,
        "coordinate_00_full_energy": full_00,
        "coordinate_00_active_energy": active_00,
        "one_coordinate_active_over_full_ratio": (
            scalar_row["one_coordinate_active_over_full_ratio"]),
        "ratio_minus_half": ratio_gap,
        "scalar_cancelled_margin_full_over_2_minus_active": (
            scalar_cancelled_margin),
        "source_margin_full_over_2_minus_active": source_margin,
        "margin_reconstruction_abs_error": abs(
            scalar_cancelled_margin - source_margin),
        "full_contribution": scalar_row["full_contribution"],
        "full_contribution_negative": scalar_row[
            "full_contribution_negative"],
        "cross_ratio_reduction_abs_error": scalar_row[
            "ratio_reduction_abs_error"],
        "exact_log_pair_identity_verified": (
            exact_row["all_pair_scalar_expressions_equal"]
            and exact_row["common_log_numerator_equals_expected"]),
        "one_coordinate_sign_explains_margin": (
            (ratio_gap < 0 and source_margin < 0)
            or (ratio_gap > 0 and source_margin > 0)
            or (ratio_gap == 0 and source_margin == 0)),
    }


def positive_margin_summary(rows, adverse_margin):
    positive_sum = sum(
        row["scalar_cancelled_margin_full_over_2_minus_active"]
        for row in rows
        if row["scalar_cancelled_margin_full_over_2_minus_active"] > 0)
    return {
        "row_count": len(rows),
        "positive_margin_sum": positive_sum,
        "payment_over_q46189_adverse": positive_sum / adverse_margin,
        "minimum_ratio_minus_half": min(
            row["ratio_minus_half"] for row in rows),
        "maximum_ratio_minus_half": max(
            row["ratio_minus_half"] for row in rows),
        "minimum_positive_margin": min(
            row["scalar_cancelled_margin_full_over_2_minus_active"]
            for row in rows
            if row["scalar_cancelled_margin_full_over_2_minus_active"] > 0),
        "minimum_individual_payment_over_defect": min(
            row["scalar_cancelled_margin_full_over_2_minus_active"]
            / adverse_margin
            for row in rows
            if row["scalar_cancelled_margin_full_over_2_minus_active"] > 0),
        "all_rows_above_half": all(
            row["ratio_minus_half"] > 0 for row in rows),
        "all_rows_positive_margin": all(
            row["scalar_cancelled_margin_full_over_2_minus_active"] > 0
            for row in rows),
    }


def build_receipt():
    scalar = json.loads(SOURCE_SCALAR_COLLAPSE.read_text(encoding="utf-8"))
    exact = json.loads(SOURCE_EXACT_LOG_IDENTITY.read_text(encoding="utf-8"))
    scalar_by_q = scalar_rows_by_denominator(scalar)
    exact_by_q = exact_rows_by_denominator(exact)
    rows = [
        one_coordinate_row(scalar_by_q[denominator], exact_by_q[denominator])
        for denominator in sorted(scalar_by_q)
    ]
    q46189 = next(row for row in rows
                  if row["reduced_denominator"] == DENOMINATOR)
    replacements = [
        row for row in rows if row["reduced_denominator"] != DENOMINATOR]
    adverse_margin = -q46189[
        "scalar_cancelled_margin_full_over_2_minus_active"]
    by_missing_high = defaultdict(list)
    for row in replacements:
        key = ",".join(str(prime) for prime in row["missing_high_primes"])
        by_missing_high[key].append(row)
    family_summaries = {
        missing: positive_margin_summary(family_rows, adverse_margin)
        for missing, family_rows in sorted(by_missing_high.items())
    }
    replacement_summary = positive_margin_summary(
        replacements, adverse_margin)
    max_margin_error = max(row["margin_reconstruction_abs_error"]
                           for row in rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_one_coordinate_ratio_ledger",
        "source_scalar_collapse_audit": str(SOURCE_SCALAR_COLLAPSE),
        "source_exact_log_identity_audit": str(SOURCE_EXACT_LOG_IDENTITY),
        "question": (
            "After the exact source-conductor scalar is factored out, what "
            "one-coordinate active/full ratio ledger remains for Q=46189 and "
            "the replacement rows?"),
        "answer": (
            "For this selected finite family, every signed margin is accounted "
            "for by (-scalar) * full_00 * (active_00/full_00 - 1/2).  Q=46189 "
            "has a negative ratio gap, while all ten replacement rows have "
            "positive ratio gaps.  Thus the phase/scalar issue is closed for "
            "this family; the remaining theorem target is a coordinate-00 "
            "energy ratio inequality."),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "adverse_denominator": DENOMINATOR,
            "adverse_denominator_factorization": (
                q46189["factorization"]),
            "common_margin_formula": (
                "(-exact_scalar) * coordinate_00_full_energy "
                "* (coordinate_00_active_over_full_ratio - 1/2)"),
        },
        "q46189_one_coordinate_row": q46189,
        "replacement_one_coordinate_rows": sorted(
            replacements,
            key=lambda row: row[
                "scalar_cancelled_margin_full_over_2_minus_active"],
            reverse=True),
        "replacement_summary": replacement_summary,
        "omitted_high_prime_family_one_coordinate_summaries": (
            family_summaries),
        "classification": {
            "q46189_exact_phase_removed": (
                q46189["exact_log_pair_identity_verified"]
                and q46189["cross_ratio_reduction_abs_error"] < 1e-12),
            "q46189_one_coordinate_ratio_below_half": (
                q46189["ratio_minus_half"] < 0),
            "all_replacements_exact_phase_removed": all(
                row["exact_log_pair_identity_verified"]
                and row["cross_ratio_reduction_abs_error"] < 1e-12
                for row in replacements),
            "all_replacements_one_coordinate_ratio_above_half": all(
                row["ratio_minus_half"] > 0 for row in replacements),
            "all_margins_reconstructed_after_scalar_cancel": (
                max_margin_error < 0.05),
            "replacement_family_pays_q46189_defect_after_scalar_cancel": (
                replacement_summary["positive_margin_sum"]
                > adverse_margin),
            "each_omitted_high_prime_family_pays_after_scalar_cancel": all(
                summary["positive_margin_sum"] > adverse_margin
                for summary in family_summaries.values()),
            "finite_one_coordinate_ledger_only": True,
        },
        "candidate_next_action": {
            "name": "symbolic coordinate-00 energy ratio inequality",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Express coordinate-00 full and active energies by exact "
                "Dirichlet-kernel sums for the selected denominator family, "
                "then prove or falsify the half-threshold ratio signs without "
                "using the coordinate-12 phase scalar."),
            "prediction": (
                "The replacement rows should stay above one half because their "
                "coordinate-00 active window has constructive residue-kernel "
                "alignment, while Q=46189 has a small destructive deficit."),
            "falsifier": (
                "If exact coordinate-00 energy decomposition still requires "
                "hidden phase cancellation or loses the replacement signs, the "
                "one-coordinate theorem target is not isolated enough."),
            "smallest_next_test": (
                "For Q=46189 and the weakest replacement row, decompose "
                "coordinate-00 active-full half-margin into exact diagonal and "
                "off-diagonal residue-kernel terms and identify the sign-"
                "deciding terms."),
        },
        "decision": (
            "The exact scalar/log identity reduces the selected Q=46189 "
            "payment lane to a one-coordinate active/full ratio ledger.  The "
            "remaining obstruction is no longer phase alignment but an energy "
            "ratio inequality for coordinate 00.  No universal ratio theorem "
            "or Goldbach proof is established."),
        "finite_one_coordinate_ratio_ledger_audit_only": True,
        "finite_diagnostic_only": True,
        "symbolic_coordinate_00_energy_ratio_theorem_proved": False,
        "one_coordinate_active_full_ratio_theorem_proved": False,
        "replacement_family_payment_theorem_proved": False,
        "universal_source_conductor_scalar_formula_theorem_proved": False,
        "source_start_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    q_row = receipt["q46189_one_coordinate_row"]
    replacement = receipt["replacement_summary"]
    families = receipt[
        "omitted_high_prime_family_one_coordinate_summaries"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 one-coordinate ratio ledger audit",
        "",
        "## Question",
        "",
        "After the exact source-conductor scalar is factored out, what",
        "one-coordinate active/full ratio ledger remains for `Q=46189` and",
        "the replacement rows?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_one_coordinate_ratio_ledger_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-one-coordinate-ratio-ledger-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"Q=46189 ratio minus half:       {q_row['ratio_minus_half']}",
        f"Q=46189 scalar-cancel margin:   {q_row['scalar_cancelled_margin_full_over_2_minus_active']}",
        f"replacement rows:               {replacement['row_count']}",
        f"min replacement ratio gap:      {replacement['minimum_ratio_minus_half']}",
        f"replacement payment / defect:   {replacement['payment_over_q46189_adverse']}",
        f"minimum row payment / defect:   {replacement['minimum_individual_payment_over_defect']}",
        "```",
        "",
        "Omitted-high-prime family payment ratios after scalar cancellation:",
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
        "The exact scalar/log identity reduces the selected `Q=46189` payment",
        "lane to a one-coordinate active/full ratio ledger.  The remaining",
        "obstruction is no longer phase alignment but an energy-ratio",
        "inequality for coordinate `00`.",
        "",
        "This is a finite selected-family ledger only.  It proves no symbolic",
        "coordinate-00 energy ratio theorem, one-coordinate active/full ratio",
        "theorem, replacement-family payment theorem, universal source-",
        "conductor scalar formula theorem, strict-central Goldbach theorem, or",
        "Goldbach proof.",
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
        "q46189_ratio_minus_half": receipt[
            "q46189_one_coordinate_row"]["ratio_minus_half"],
        "replacement_payment_over_defect": receipt[
            "replacement_summary"]["payment_over_q46189_adverse"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
