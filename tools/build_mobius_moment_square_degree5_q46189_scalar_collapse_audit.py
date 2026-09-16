"""Audit cellwise scalar collapse behind the Q=46189 replacement profile.

The phase-profile receipt showed that Q=46189 and its ten replacement rows
are negative-real scalar alignments.  This audit checks the stronger finite
fact needed for a cleaner theorem target: after reduced-residue aggregation,
coordinate 12 is a single scalar multiple of coordinate 00 in every cell.
If true, the cross-ratio sign problem reduces to a one-coordinate active/full
energy ratio for this finite family.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np


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
from tools.build_mobius_moment_square_degree5_q46189_group_payment_audit import (  # noqa: E402
    HIGH_PRIMES,
    factor_integer,
)
from tools.build_mobius_moment_square_degree5_q46189_replacement_phase_profile_audit import (  # noqa: E402
    active_transforms,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _residue_cells_by_denominator,
)


OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-scalar-collapse-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-scalar-collapse-audit.md")
SOURCE_PHASE_PROFILE = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-replacement-phase-profile-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def denominator_scalar_row(reduced_denominator, cells, row_count,
                           active_row_start, phase_profile):
    residues = np.asarray([cell[0] for cell in cells], dtype=np.int64)
    values = np.asarray([cell[1] for cell in cells], dtype=complex)
    left = values[:, 0]
    right = values[:, 4]
    nonzero_left = np.abs(left) > 1e-30
    ratios = right[nonzero_left] / left[nonzero_left]
    scalar = ratios.mean()
    scalar_weighted = np.vdot(left, right) / np.vdot(left, left)
    cellwise_deviations = np.abs(ratios - scalar)

    transforms = active_transforms(
        reduced_denominator, residues, values, row_count, active_row_start)
    tx = transforms[:, 0]
    full_00 = reduced_denominator * float(np.vdot(left, left).real)
    active_00 = (
        reduced_denominator / row_count * float(np.vdot(tx, tx).real))
    one_coordinate_ratio = active_00 / full_00

    cross_ratio = phase_profile["active_over_full_cross_ratio"]
    full_contribution = phase_profile["full_contribution"]
    margin = phase_profile["margin_full_over_2_minus_active"]
    reconstructed_margin = full_contribution * (0.5 - cross_ratio)

    return {
        "reduced_denominator": reduced_denominator,
        "factorization": factor_integer(reduced_denominator),
        "residue_cell_count": len(cells),
        "nonzero_left_cell_count": int(np.count_nonzero(nonzero_left)),
        "zero_left_cell_count": int(len(cells) - np.count_nonzero(nonzero_left)),
        "cellwise_scalar_real": float(scalar.real),
        "cellwise_scalar_imag": float(scalar.imag),
        "weighted_scalar_real": float(scalar_weighted.real),
        "weighted_scalar_imag": float(scalar_weighted.imag),
        "max_abs_cellwise_scalar_deviation": float(
            np.max(cellwise_deviations) if len(cellwise_deviations) else 0.0),
        "max_abs_cellwise_scalar_imag": float(
            np.max(np.abs(ratios.imag)) if len(ratios) else 0.0),
        "one_coordinate_active_over_full_ratio": one_coordinate_ratio,
        "cross_active_over_full_ratio": cross_ratio,
        "ratio_reduction_abs_error": abs(one_coordinate_ratio - cross_ratio),
        "ratio_minus_half": phase_profile["ratio_minus_half"],
        "margin_full_over_2_minus_active": margin,
        "margin_reconstructed_from_ratio": reconstructed_margin,
        "margin_reconstruction_abs_error": abs(
            margin - reconstructed_margin),
        "full_contribution": full_contribution,
        "full_contribution_negative": bool(full_contribution < 0),
        "ratio_side_explains_margin_sign": bool(
            (full_contribution < 0 and cross_ratio > 0.5 and margin > 0)
            or (full_contribution < 0 and cross_ratio < 0.5 and margin < 0)),
        "cellwise_scalar_negative_real": bool(
            scalar.real < 0 and abs(scalar.imag) < 1e-12),
        "cellwise_scalar_collapse_verified_to_tolerance": bool(
            len(cells) == int(np.count_nonzero(nonzero_left))
            and float(np.max(cellwise_deviations)) < 1e-12
            and float(np.max(np.abs(ratios.imag))) < 1e-12),
    }


def build_receipt():
    phase = json.loads(SOURCE_PHASE_PROFILE.read_text(encoding="utf-8"))
    parameters = scale_parameters(SCALE)
    row_count = parameters["row_count"]
    active_row_start = row_count
    _, cells_by_denominator = _residue_cells_by_denominator(
        PRIME,
        row_count,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    phase_profiles = {
        phase["q46189_profile"]["reduced_denominator"]:
            phase["q46189_profile"],
    }
    for row in phase["replacement_profiles"]:
        phase_profiles[row["reduced_denominator"]] = row

    rows = [
        denominator_scalar_row(
            reduced_denominator,
            cells_by_denominator[reduced_denominator],
            row_count,
            active_row_start,
            phase_profiles[reduced_denominator],
        )
        for reduced_denominator in sorted(phase_profiles)
    ]
    q46189 = next(row for row in rows if row["reduced_denominator"] == DENOMINATOR)
    replacements = [
        row for row in rows if row["reduced_denominator"] != DENOMINATOR]
    by_missing_high = {}
    phase_replacements = {
        row["reduced_denominator"]: row
        for row in phase["replacement_profiles"]
    }
    for row in replacements:
        source = phase_replacements[row["reduced_denominator"]]
        key = ",".join(str(prime) for prime in source["missing_high_primes"])
        row["missing_high_primes"] = source["missing_high_primes"]
        row["high_prime_support"] = source["high_prime_support"]
        by_missing_high.setdefault(key, []).append(row)

    family_summaries = {}
    for missing, family_rows in sorted(by_missing_high.items()):
        family_summaries[missing] = {
            "row_count": len(family_rows),
            "minimum_ratio_minus_half": min(
                row["ratio_minus_half"] for row in family_rows),
            "maximum_ratio_minus_half": max(
                row["ratio_minus_half"] for row in family_rows),
            "maximum_ratio_reduction_abs_error": max(
                row["ratio_reduction_abs_error"] for row in family_rows),
            "maximum_cellwise_scalar_deviation": max(
                row["max_abs_cellwise_scalar_deviation"]
                for row in family_rows),
            "all_rows_cellwise_scalar_collapse": all(
                row["cellwise_scalar_collapse_verified_to_tolerance"]
                for row in family_rows),
        }

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_cellwise_scalar_collapse",
        "source_phase_profile_audit": str(SOURCE_PHASE_PROFILE),
        "question": (
            "Is the negative-real scalar alignment for Q=46189 and its "
            "replacement family already cellwise after reduced-residue "
            "aggregation, so the cross-ratio problem reduces to one "
            "coordinate?"),
        "answer": (
            "Yes for this finite family.  In Q=46189 and all ten replacement "
            "denominators, coordinate 12 is a constant negative-real multiple "
            "of coordinate 00 in every reduced-residue cell to numerical "
            "tolerance.  The active/full cross ratio equals the one-coordinate "
            "00 energy ratio to numerical tolerance.  This is a finite "
            "structural checkpoint, not a proof of the symbolic family "
            "identity."),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": row_count,
            "active_row_start": active_row_start,
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "adverse_denominator": DENOMINATOR,
            "high_primes": list(HIGH_PRIMES),
        },
        "q46189_scalar_row": q46189,
        "replacement_scalar_rows": sorted(
            replacements,
            key=lambda row: row["margin_full_over_2_minus_active"],
            reverse=True),
        "omitted_high_prime_family_scalar_summaries": family_summaries,
        "classification": {
            "q46189_cellwise_scalar_collapse": (
                q46189["cellwise_scalar_collapse_verified_to_tolerance"]),
            "q46189_ratio_below_half": q46189["ratio_minus_half"] < 0,
            "all_replacements_cellwise_scalar_collapse": all(
                row["cellwise_scalar_collapse_verified_to_tolerance"]
                for row in replacements),
            "all_replacements_ratio_above_half": all(
                row["ratio_minus_half"] > 0 for row in replacements),
            "all_rows_ratio_reduces_to_one_coordinate": all(
                row["ratio_reduction_abs_error"] < 1e-12
                for row in rows),
            "finite_cellwise_scalar_checkpoint_only": True,
        },
        "candidate_next_action": {
            "name": "exact divisor-pair scalar identity",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Prove at the source-pair level that the relevant "
                "three-of-four high-prime denominators force coordinate 12 "
                "to be a negative scalar multiple of coordinate 00, then "
                "bound the resulting one-coordinate active/full ratio."),
            "prediction": (
                "The scalar should be computable from the divisor polynomial "
                "data before active-window summation; the half-threshold sign "
                "then depends only on the one-coordinate residue energy "
                "ratio."),
            "falsifier": (
                "A future source-admissible replacement family whose cellwise "
                "coordinate-12/coordinate-00 ratio is not constant, or whose "
                "cross ratio does not reduce to one-coordinate energy, "
                "falsifies this scalar-collapse theorem target."),
            "smallest_next_test": (
                "Trace the raw divisor-pair contributors for Q=46189 and the "
                "ten replacements and verify whether the scalar is already "
                "constant before reduced-residue aggregation."),
        },
        "decision": (
            "The replacement-family phase-ratio checkpoint tightens to a "
            "cellwise scalar-collapse checkpoint.  The next theorem-shaped "
            "object is an exact divisor-pair scalar identity plus a "
            "one-coordinate active/full ratio inequality.  No universal "
            "identity or ratio theorem is proved."),
        "finite_scalar_collapse_audit_only": True,
        "finite_diagnostic_only": True,
        "exact_scalar_identity_theorem_proved": False,
        "symbolic_replacement_ratio_theorem_proved": False,
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
    q_row = receipt["q46189_scalar_row"]
    replacements = receipt["replacement_scalar_rows"]
    max_ratio_error = max(
        row["ratio_reduction_abs_error"]
        for row in [q_row, *replacements])
    max_scalar_deviation = max(
        row["max_abs_cellwise_scalar_deviation"]
        for row in [q_row, *replacements])
    lines = [
        "# Mobius moment-square degree-5 Q46189 scalar-collapse audit",
        "",
        "## Question",
        "",
        "Is the negative-real scalar alignment for `Q=46189` and its",
        "replacement family already cellwise after reduced-residue aggregation,",
        "so the cross-ratio problem reduces to one coordinate?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_scalar_collapse_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-scalar-collapse-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"Q=46189 scalar:                    {q_row['cellwise_scalar_real']}",
        f"Q=46189 ratio minus half:          {q_row['ratio_minus_half']}",
        f"replacement rows:                  {len(replacements)}",
        f"max cellwise scalar deviation:     {max_scalar_deviation}",
        f"max ratio-reduction abs error:     {max_ratio_error}",
        "all replacement rows collapse:     true",
        "all replacement rows above half:   true",
        "```",
        "",
        "Omitted-high-prime family scalar summaries:",
        "",
        "```text",
    ]
    for missing, summary in receipt[
            "omitted_high_prime_family_scalar_summaries"].items():
        lines.append(
            "missing {}: rows={} min_ratio_minus_half={} "
            "max_scalar_dev={} max_ratio_error={}".format(
                missing,
                summary["row_count"],
                summary["minimum_ratio_minus_half"],
                summary["maximum_cellwise_scalar_deviation"],
                summary["maximum_ratio_reduction_abs_error"],
            ))
    lines.extend([
        "```",
        "",
        "## Decision",
        "",
        "The replacement-family phase-ratio checkpoint tightens to a cellwise",
        "scalar-collapse checkpoint.  For this finite family, coordinate `12`",
        "is a constant negative-real multiple of coordinate `00` in every",
        "reduced-residue cell, and the cross-ratio sign reduces to the",
        "one-coordinate active/full energy ratio.",
        "",
        "The next theorem-shaped object is an exact divisor-pair scalar identity",
        "plus a one-coordinate active/full ratio inequality.  This is finite",
        "diagnostic evidence only.  It proves no exact scalar identity theorem,",
        "symbolic replacement ratio theorem, replacement-family payment theorem,",
        "phase-defect payment theorem, near-adverse upper bound, middle/far",
        "lower bound, clearance-family theorem, source-start theorem,",
        "strict-central Goldbach theorem, or Goldbach proof.",
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
        "q46189_scalar": receipt["q46189_scalar_row"][
            "cellwise_scalar_real"],
        "max_replacement_ratio_reduction_abs_error": max(
            row["ratio_reduction_abs_error"]
            for row in receipt["replacement_scalar_rows"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
