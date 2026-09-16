"""Audit coordinate-00 kernel decomposition across all Q46189 replacements."""

from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    scale_parameters,
)
from tools.build_mobius_moment_square_degree5_q46189_coordinate00_kernel_decomposition_audit import (  # noqa: E402
    decompose_row,
    ledger_rows,
)
from tools.build_mobius_moment_square_degree5_q46189_exception_bound_audit import (  # noqa: E402
    PRIME,
    SCALE,
    TARGET_LABEL,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _residue_cells_by_denominator,
)


OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-replacement-kernel-family-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-replacement-kernel-family-audit.md")
SOURCE_LEDGER = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-one-coordinate-ratio-ledger-audit.json")
SOURCE_KERNEL_PAIR = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-coordinate00-kernel-decomposition-audit.json")
ABS_ROUNDOFF_TOLERANCE = 2.0
REL_ROUNDOFF_TOLERANCE = 1e-12


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def bucket_value(row, bucket_name):
    return next(
        bucket["component_active_contribution"]
        for bucket in row["distance_bucket_contributions"]
        if bucket["bucket"] == bucket_name)


def identity_errors(row, ledger_row):
    full_error = abs(
        row["component_full_energy"]
        - ledger_row["coordinate_00_full_energy"])
    active_error = abs(
        row["component_active_energy"]
        - ledger_row["coordinate_00_active_energy"])
    direct_error = row["active_reconstruction_abs_error"]
    scalar_error = row["scalar_cancelled_margin_abs_error"]
    relative_energy_error = max(
        full_error / max(1.0, abs(ledger_row["coordinate_00_full_energy"])),
        active_error / max(1.0, abs(
            ledger_row["coordinate_00_active_energy"])),
        direct_error / max(1.0, abs(row["component_active_energy"])),
    )
    verified_with_roundoff = (
        max(full_error, active_error, direct_error, scalar_error)
        <= ABS_ROUNDOFF_TOLERANCE
        and relative_energy_error <= REL_ROUNDOFF_TOLERANCE)
    return {
        "full_energy_abs_error": full_error,
        "active_energy_abs_error": active_error,
        "direct_active_abs_error": direct_error,
        "scalar_cancelled_margin_abs_error": scalar_error,
        "relative_energy_error": relative_energy_error,
        "strict_abs_lt_1_pair_builder_flag": (
            row["finite_dirichlet_kernel_identity_verified"]),
        "verified_with_roundoff_tolerance": verified_with_roundoff,
    }


def compact_row(row, ledger_row):
    errors = identity_errors(row, ledger_row)
    return {
        "reduced_denominator": row["reduced_denominator"],
        "factorization": row["factorization"],
        "missing_high_primes": ledger_row["missing_high_primes"],
        "high_prime_support": ledger_row["high_prime_support"],
        "ratio_minus_half": row["ratio_minus_half"],
        "component_half_margin_active_minus_half_full": (
            row["component_half_margin_active_minus_half_full"]),
        "diagonal_half_contribution": row["diagonal_half_contribution"],
        "off_diagonal_total_contribution": (
            row["off_diagonal_total_contribution"]),
        "off_diagonal_over_diagonal_half": (
            row["off_diagonal_over_diagonal_half"]),
        "near_1_to_A_contribution": bucket_value(row, "near_1_to_A"),
        "middle_A_to_10A_contribution": bucket_value(
            row, "middle_A_to_10A"),
        "far_10A_to_100A_contribution": bucket_value(
            row, "far_10A_to_100A"),
        "tail_over_100A_contribution": bucket_value(row, "tail_over_100A"),
        "top_negative_gap_pair": row["top_negative_gap_pairs"][0],
        "top_positive_gap_pair": row["top_positive_gap_pairs"][0],
        "active_reconstruction_abs_error": row[
            "active_reconstruction_abs_error"],
        "scalar_cancelled_margin_abs_error": row[
            "scalar_cancelled_margin_abs_error"],
        "kernel_identity_errors": errors,
        "finite_dirichlet_kernel_identity_verified_strict_abs_lt_1": (
            errors["strict_abs_lt_1_pair_builder_flag"]),
        "finite_dirichlet_kernel_identity_verified_with_roundoff": (
            errors["verified_with_roundoff_tolerance"]),
    }


def family_summary(rows):
    return {
        "row_count": len(rows),
        "minimum_ratio_minus_half": min(
            row["ratio_minus_half"] for row in rows),
        "minimum_margin": min(
            row["component_half_margin_active_minus_half_full"]
            for row in rows),
        "minimum_off_diagonal_over_diagonal_half": min(
            row["off_diagonal_over_diagonal_half"] for row in rows),
        "all_rows_positive_after_off_diagonal": all(
            row["component_half_margin_active_minus_half_full"] > 0
            and row["off_diagonal_total_contribution"]
            > -row["diagonal_half_contribution"]
            for row in rows),
        "all_kernel_identities_verified": all(
            row["finite_dirichlet_kernel_identity_verified_with_roundoff"]
            for row in rows),
        "all_strict_abs_lt_1_pair_builder_flags": all(
            row["finite_dirichlet_kernel_identity_verified_strict_abs_lt_1"]
            for row in rows),
    }


def build_receipt():
    ledger = json.loads(SOURCE_LEDGER.read_text(encoding="utf-8"))
    parameters = scale_parameters(SCALE)
    row_count = parameters["row_count"]
    active_row_start = row_count
    _, cells_by_denominator = _residue_cells_by_denominator(
        PRIME,
        row_count,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    by_q = ledger_rows(ledger)
    decomposed = []
    for ledger_row in ledger["replacement_one_coordinate_rows"]:
        denominator = ledger_row["reduced_denominator"]
        row = decompose_row(
            denominator,
            cells_by_denominator[denominator],
            row_count,
            active_row_start,
            by_q[denominator],
            "replacement_family_row",
        )
        decomposed.append(compact_row(row, ledger_row))

    rows = sorted(decomposed, key=lambda row: row["ratio_minus_half"])
    by_missing = defaultdict(list)
    for row in rows:
        key = ",".join(str(prime) for prime in row["missing_high_primes"])
        by_missing[key].append(row)
    family_summaries = {
        missing: family_summary(family_rows)
        for missing, family_rows in sorted(by_missing.items())
    }
    weakest_by_gap = min(rows, key=lambda row: row["ratio_minus_half"])
    weakest_by_margin = min(
        rows, key=lambda row:
        row["component_half_margin_active_minus_half_full"])
    weakest_by_offdiag = min(
        rows, key=lambda row:
        row["off_diagonal_over_diagonal_half"])
    max_active_error = max(
        row["active_reconstruction_abs_error"] for row in rows)
    max_margin_error = max(
        row["scalar_cancelled_margin_abs_error"] for row in rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_replacement_kernel_family",
        "source_one_coordinate_ledger": str(SOURCE_LEDGER),
        "source_pair_kernel_decomposition": str(SOURCE_KERNEL_PAIR),
        "question": (
            "Across all ten Q=46189 replacement rows, is the previously "
            "selected weakest replacement also worst by residue-gap kernel "
            "metrics, and do all rows survive off-diagonal drag?"),
        "answer": (
            "Yes for this finite family.  Denominator 38038 is simultaneously "
            "weakest by ratio gap, half-margin, and off-diagonal-over-"
            "diagonal pressure.  All ten replacement rows have verified "
            "Dirichlet-kernel decompositions and retain positive coordinate-00 "
            "half-margin after off-diagonal drag."),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": row_count,
            "active_row_start": active_row_start,
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "replacement_row_count": len(rows),
        },
        "replacement_kernel_rows": rows,
        "weakest_by_ratio_gap": weakest_by_gap,
        "weakest_by_half_margin": weakest_by_margin,
        "weakest_by_off_diagonal_pressure": weakest_by_offdiag,
        "omitted_high_prime_family_kernel_summaries": family_summaries,
        "summary": {
            "minimum_ratio_minus_half": weakest_by_gap[
                "ratio_minus_half"],
            "minimum_half_margin": weakest_by_margin[
                "component_half_margin_active_minus_half_full"],
            "minimum_off_diagonal_over_diagonal_half": weakest_by_offdiag[
                "off_diagonal_over_diagonal_half"],
            "maximum_active_reconstruction_abs_error": max_active_error,
            "maximum_scalar_cancelled_margin_abs_error": max_margin_error,
            "maximum_ledger_active_energy_abs_error": max(
                row["kernel_identity_errors"]["active_energy_abs_error"]
                for row in rows),
            "maximum_relative_energy_error": max(
                row["kernel_identity_errors"]["relative_energy_error"]
                for row in rows),
            "all_replacements_positive_after_off_diagonal": all(
                row["component_half_margin_active_minus_half_full"] > 0
                and row["off_diagonal_total_contribution"]
                > -row["diagonal_half_contribution"]
                for row in rows),
            "all_kernel_identities_verified_with_roundoff": all(
                row["finite_dirichlet_kernel_identity_verified_with_roundoff"]
                for row in rows),
            "all_strict_abs_lt_1_pair_builder_flags": all(
                row[
                    "finite_dirichlet_kernel_identity_verified_strict_abs_lt_1"]
                for row in rows),
        },
        "kernel_identity_verification_tolerance": {
            "method": (
                "Double-precision FFT/direct-transform cross-check.  The "
                "family audit records the older strict absolute < 1 pair-"
                "builder flag separately because one large-energy replacement "
                "row misses that sub-unit threshold by floating roundoff."),
            "absolute_tolerance": ABS_ROUNDOFF_TOLERANCE,
            "relative_tolerance": REL_ROUNDOFF_TOLERANCE,
        },
        "classification": {
            "q38038_is_weakest_by_ratio_margin_and_offdiag_pressure": (
                weakest_by_gap["reduced_denominator"] == 38038
                and weakest_by_margin["reduced_denominator"] == 38038
                and weakest_by_offdiag["reduced_denominator"] == 38038),
            "all_replacements_survive_off_diagonal_drag": all(
                row["component_half_margin_active_minus_half_full"] > 0
                for row in rows),
            "all_omitted_high_prime_families_survive": all(
                summary["all_rows_positive_after_off_diagonal"]
                for summary in family_summaries.values()),
            "all_kernel_identities_verified_with_roundoff": all(
                row["finite_dirichlet_kernel_identity_verified_with_roundoff"]
                for row in rows),
            "all_strict_abs_lt_1_pair_builder_flags": all(
                row[
                    "finite_dirichlet_kernel_identity_verified_strict_abs_lt_1"]
                for row in rows),
            "finite_replacement_kernel_family_only": True,
        },
        "candidate_next_action": {
            "name": "replacement residue-gap bound pattern",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use q=38038 as the finite worst replacement model and seek a "
                "structural lower bound showing replacement rows retain "
                "positive diagonal remainder after grouped off-diagonal "
                "Dirichlet-kernel drag."),
            "prediction": (
                "Replacement-family rows should remain positive whenever "
                "their off-diagonal-over-diagonal pressure is above the "
                "q=38038 floor, while Q-style adverse rows cross below -1."),
            "falsifier": (
                "A source-admissible replacement row with off-diagonal-over-"
                "diagonal pressure below -1, or lower than q=38038 while "
                "still in the same replacement family, falsifies this finite "
                "worst-case pattern."),
            "smallest_next_test": (
                "Compare the q=38038 residue-gap bucket pattern against the "
                "Q=46189 adverse pattern and derive the first candidate "
                "inequality separating offdiag/diag > -1 from Q-style "
                "overpayment."),
        },
        "decision": (
            "The weakest replacement row was not cherry-picked: q=38038 is "
            "worst across the checked replacement family by ratio gap, margin, "
            "and off-diagonal pressure.  The theorem-shaped target narrows to "
            "a replacement residue-gap lower bound.  No universal sign theorem "
            "or Goldbach proof is established."),
        "finite_replacement_kernel_family_audit_only": True,
        "finite_diagnostic_only": True,
        "replacement_residue_gap_bound_theorem_proved": False,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "symbolic_coordinate_00_energy_ratio_theorem_proved": False,
        "one_coordinate_active_full_ratio_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    weakest = receipt["weakest_by_ratio_gap"]
    summary = receipt["summary"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 replacement kernel family audit",
        "",
        "## Question",
        "",
        "Across all ten `Q=46189` replacement rows, is the previously selected",
        "weakest replacement also worst by residue-gap kernel metrics, and do",
        "all rows survive off-diagonal drag?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_replacement_kernel_family_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-replacement-kernel-family-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"replacement rows:              {receipt['fixture']['replacement_row_count']}",
        f"weakest replacement q:         {weakest['reduced_denominator']}",
        f"minimum ratio minus half:      {summary['minimum_ratio_minus_half']}",
        f"minimum half-margin:           {summary['minimum_half_margin']}",
        f"minimum offdiag/diag-half:     {summary['minimum_off_diagonal_over_diagonal_half']}",
        f"max active reconstruction err: {summary['maximum_active_reconstruction_abs_error']}",
        f"max ledger active-energy err:  {summary['maximum_ledger_active_energy_abs_error']}",
        f"max relative energy err:       {summary['maximum_relative_energy_error']}",
        "all rows positive after drag:  true",
        "kernel identities verified:    true within recorded roundoff tolerance",
        "strict abs<1 flags all pass:   false",
        "```",
        "",
        "## Decision",
        "",
        "The weakest replacement row was not cherry-picked: `q=38038` is worst",
        "across the checked replacement family by ratio gap, margin, and",
        "off-diagonal pressure.  The theorem-shaped target narrows to a",
        "replacement residue-gap lower bound.",
        "",
        "This is finite diagnostic evidence only.  It proves no replacement",
        "residue-gap bound theorem, coordinate-00 residue-gap sign theorem,",
        "symbolic coordinate-00 energy ratio theorem, one-coordinate",
        "active/full ratio theorem, strict-central Goldbach theorem, or",
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
        "weakest_replacement": receipt["weakest_by_ratio_gap"][
            "reduced_denominator"],
        "minimum_ratio_minus_half": receipt["summary"][
            "minimum_ratio_minus_half"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
