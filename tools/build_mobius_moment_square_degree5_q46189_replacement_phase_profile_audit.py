"""Profile Q=46189 replacement-family phase ratios.

The group-payment receipt showed that ten three-of-four high-prime
replacement denominators pay the Q=46189 adverse margin.  This derived audit
asks whether those paying rows share the same coordinate structure as Q=46189,
but with the active/full cross ratio on the paying side of one half.
"""

from __future__ import annotations

import cmath
import json
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    PAIRS,
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
from tools.build_mobius_moment_square_degree5_source_margin_denominator_audit import (  # noqa: E402
    label_rows_from_denominator,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _residue_cells_by_denominator,
)


OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-replacement-phase-profile-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-replacement-phase-profile-audit.md")
SOURCE_GROUP_PAYMENT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-group-payment-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def active_transforms(reduced_denominator, residues, values, row_count,
                      active_row_start):
    rows_window = np.arange(
        active_row_start, active_row_start + row_count, dtype=np.int64)
    transforms = np.zeros((row_count, values.shape[1]), dtype=complex)
    for first in range(0, len(residues), 8192):
        selected_residues = residues[first:first + 8192]
        phases = np.exp(
            2j * np.pi
            * ((rows_window[:, None] * selected_residues[None, :])
               % reduced_denominator)
            / reduced_denominator)
        transforms += phases @ values[first:first + 8192]
    return transforms


def phase_profile(reduced_denominator, cells, row_count, active_row_start,
                  label_row):
    residues = np.asarray([cell[0] for cell in cells], dtype=np.int64)
    values = np.asarray([cell[1] for cell in cells], dtype=complex)
    transforms = active_transforms(
        reduced_denominator, residues, values, row_count, active_row_start)
    left, right, left_label, right_label = next(
        pair for pair in PAIRS if f"{pair[2]},{pair[3]}" == TARGET_LABEL)
    x = values[:, left]
    y = values[:, right]
    tx = transforms[:, left]
    ty = transforms[:, right]
    scalar = np.vdot(x, y) / np.vdot(x, x)
    scalar_residual = np.linalg.norm(y - scalar * x) / np.linalg.norm(y)
    full_cross = reduced_denominator * float(np.vdot(y, x).real)
    active_cross = (
        reduced_denominator / row_count * float(np.vdot(ty, tx).real))
    ratio = active_cross / full_cross
    ratio_minus_half = ratio - 0.5
    full_contribution = label_row["full_contribution"]
    active_contribution = label_row["active_contribution"]
    margin = label_row["unnormalized_margin_full_over_2_minus_active"]
    return {
        "reduced_denominator": reduced_denominator,
        "factorization": factor_integer(reduced_denominator),
        "label": f"{left_label},{right_label}",
        "residue_cell_count": len(cells),
        "active_row_start": active_row_start,
        "active_row_stop": active_row_start + row_count - 1,
        "active_contribution": active_contribution,
        "full_contribution": full_contribution,
        "active_cross": active_cross,
        "full_cross": full_cross,
        "active_over_full_cross_ratio": ratio,
        "ratio_minus_half": ratio_minus_half,
        "half_threshold_defect": 0.5 - ratio,
        "margin_full_over_2_minus_active": margin,
        "margin_sign_matches_negative_full_ratio_side": (
            (margin > 0 and full_contribution < 0 and ratio > 0.5)
            or (margin < 0 and full_contribution < 0 and ratio < 0.5)
            or (margin == 0 and ratio == 0.5)),
        "full_cross_negative": full_contribution < 0,
        "best_scalar_right_over_left_real": float(scalar.real),
        "best_scalar_right_over_left_imag": float(scalar.imag),
        "best_scalar_abs": float(abs(scalar)),
        "best_scalar_phase": float(cmath.phase(scalar)),
        "relative_scalar_residual": float(scalar_residual),
    }


def replacement_index(group_receipt):
    result = {}
    for row in group_receipt["replacement_family_rows"]:
        result[row["reduced_denominator"]] = row
    return result


def family_summary(rows, adverse_margin):
    margins = [row["margin_full_over_2_minus_active"] for row in rows]
    ratios = [row["active_over_full_cross_ratio"] for row in rows]
    residuals = [row["relative_scalar_residual"] for row in rows]
    return {
        "row_count": len(rows),
        "positive_margin_sum": sum(margin for margin in margins if margin > 0),
        "payment_over_q46189_adverse": (
            sum(margin for margin in margins if margin > 0) / adverse_margin),
        "minimum_margin": min(margins),
        "maximum_margin": max(margins),
        "minimum_ratio_minus_half": min(
            row["ratio_minus_half"] for row in rows),
        "maximum_ratio_minus_half": max(
            row["ratio_minus_half"] for row in rows),
        "minimum_active_over_full_cross_ratio": min(ratios),
        "maximum_active_over_full_cross_ratio": max(ratios),
        "maximum_relative_scalar_residual": max(residuals),
        "all_rows_have_negative_full_cross": all(
            row["full_cross_negative"] for row in rows),
        "all_rows_ratio_above_half": all(
            row["active_over_full_cross_ratio"] > 0.5 for row in rows),
        "all_rows_margin_positive": all(
            row["margin_full_over_2_minus_active"] > 0 for row in rows),
        "all_rows_match_ratio_side": all(
            row["margin_sign_matches_negative_full_ratio_side"]
            for row in rows),
    }


def build_receipt():
    group = json.loads(SOURCE_GROUP_PAYMENT.read_text(encoding="utf-8"))
    parameters = scale_parameters(SCALE)
    row_count = parameters["row_count"]
    active_row_start = row_count
    _, cells_by_denominator = _residue_cells_by_denominator(
        PRIME,
        row_count,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    replacement_by_q = replacement_index(group)
    requested_denominators = sorted({DENOMINATOR, *replacement_by_q})
    profiles = []
    for reduced_denominator in requested_denominators:
        cells = cells_by_denominator[reduced_denominator]
        label_row = next(
            row for row in label_rows_from_denominator(
                reduced_denominator, cells, row_count, active_row_start)
            if row["label"] == TARGET_LABEL)
        profile = phase_profile(
            reduced_denominator, cells, row_count, active_row_start,
            label_row)
        if reduced_denominator in replacement_by_q:
            source_row = replacement_by_q[reduced_denominator]
            profile["replacement_family_row"] = source_row
            profile["high_prime_support"] = source_row["high_prime_support"]
            profile["missing_high_primes"] = source_row[
                "missing_high_primes"]
            profile["clearance_family"] = source_row["clearance_family"]
        else:
            profile["high_prime_support"] = list(HIGH_PRIMES)
            profile["missing_high_primes"] = []
            profile["clearance_family"] = "middle_2_to_3"
        profiles.append(profile)

    q46189 = next(
        row for row in profiles if row["reduced_denominator"] == DENOMINATOR)
    adverse_margin = -q46189["margin_full_over_2_minus_active"]
    replacements = [
        row for row in profiles if row["reduced_denominator"] != DENOMINATOR]
    by_missing_high = {}
    for row in replacements:
        key = ",".join(str(prime) for prime in row["missing_high_primes"])
        by_missing_high.setdefault(key, []).append(row)
    family_summaries = {
        missing: family_summary(rows, adverse_margin)
        for missing, rows in sorted(by_missing_high.items())
    }
    replacement_summary = family_summary(replacements, adverse_margin)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_replacement_phase_profile",
        "source_group_payment_audit": str(SOURCE_GROUP_PAYMENT),
        "question": (
            "Do the Q=46189 replacement-family payment rows share the same "
            "coordinate phase structure while moving to the paying side of "
            "the one-half active/full cross-ratio threshold?"),
        "answer": (
            "Yes for this finite ledger.  Q=46189 has negative full cross and "
            "ratio below one half, giving an adverse margin.  The ten "
            "replacement rows also have negative full cross, but each has "
            "active/full cross ratio above one half and therefore positive "
            "unnormalized margin.  The replacement rows are also negative-real "
            "scalar alignments to numerical precision, so the remaining gap "
            "is a symbolic ratio inequality rather than merely finding the "
            "right coordinate frame."),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": row_count,
            "active_row_start": active_row_start,
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "adverse_denominator": DENOMINATOR,
            "adverse_margin": adverse_margin,
            "high_primes": list(HIGH_PRIMES),
        },
        "q46189_profile": q46189,
        "replacement_profiles": sorted(
            replacements,
            key=lambda row: row["margin_full_over_2_minus_active"],
            reverse=True),
        "replacement_summary": replacement_summary,
        "omitted_high_prime_family_phase_summaries": family_summaries,
        "classification": {
            "q46189_ratio_below_half": (
                q46189["active_over_full_cross_ratio"] < 0.5),
            "q46189_margin_adverse": (
                q46189["margin_full_over_2_minus_active"] < 0),
            "all_replacements_ratio_above_half": (
                replacement_summary["all_rows_ratio_above_half"]),
            "all_replacements_margin_positive": (
                replacement_summary["all_rows_margin_positive"]),
            "all_replacements_have_negative_full_cross": (
                replacement_summary["all_rows_have_negative_full_cross"]),
            "all_replacements_scalar_negative_real": all(
                row["best_scalar_right_over_left_real"] < 0
                and abs(row["best_scalar_right_over_left_imag"]) < 1e-12
                and row["relative_scalar_residual"] < 1e-12
                for row in replacements),
            "all_omitted_high_prime_families_ratio_above_half": all(
                summary["all_rows_ratio_above_half"]
                for summary in family_summaries.values()),
            "finite_phase_profile_checkpoint_only": True,
        },
        "candidate_next_action": {
            "name": "symbolic replacement ratio inequality",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Turn the finite sign pattern into a denominator-family "
                "inequality: the adverse four-high-prime row lies below the "
                "one-half active/full ratio while each three-of-four "
                "replacement family lies above it with enough margin."),
            "prediction": (
                "A symbolic treatment should express the ratio displacement "
                "through the omitted high prime and small-prime insertions, "
                "rather than through total positivity."),
            "falsifier": (
                "If the ratio-above-half property fails for a source-"
                "admissible replacement family, or if payment relies on a "
                "diffuse positive row outside the replacement family, this "
                "specific theorem target fails."),
            "smallest_next_test": (
                "Derive exact algebraic numerator forms for Q=46189 and the "
                "ten replacement denominators and compare their signed "
                "distance from the one-half threshold family by family."),
        },
        "decision": (
            "The finite group-payment result has a phase-ratio explanation: "
            "Q=46189 is below the one-half threshold, while every checked "
            "replacement denominator is above it.  This strengthens the next "
            "symbolic target but proves no universal replacement inequality."),
        "finite_phase_profile_audit_only": True,
        "finite_diagnostic_only": True,
        "replacement_family_payment_theorem_proved": False,
        "symbolic_replacement_ratio_theorem_proved": False,
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
    q_row = receipt["q46189_profile"]
    summary = receipt["replacement_summary"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 replacement phase profile",
        "",
        "## Question",
        "",
        "Do the `Q=46189` replacement-family payment rows share the same",
        "coordinate phase structure while moving to the paying side of the",
        "one-half active/full cross-ratio threshold?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_replacement_phase_profile_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-replacement-phase-profile-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"M, p, label:                         {fixture['scale_modulus']}, {fixture['prime_modulus']}, {fixture['target_label']}",
        f"Q=46189 ratio minus half:            {q_row['ratio_minus_half']}",
        f"Q=46189 margin:                      {q_row['margin_full_over_2_minus_active']}",
        f"replacement rows:                    {summary['row_count']}",
        f"replacement ratio-minus-half min:    {summary['minimum_ratio_minus_half']}",
        f"replacement ratio-minus-half max:    {summary['maximum_ratio_minus_half']}",
        f"replacement positive margin sum:     {summary['positive_margin_sum']}",
        f"replacement payment / defect:        {summary['payment_over_q46189_adverse']}",
        f"max replacement scalar residual:     {summary['maximum_relative_scalar_residual']}",
        "```",
        "",
        "Omitted-high-prime family phase summaries:",
        "",
        "```text",
    ]
    for missing, family in receipt[
            "omitted_high_prime_family_phase_summaries"].items():
        lines.append(
            "missing {}: rows={} min_ratio_minus_half={} "
            "payment/defect={} max_scalar_residual={}".format(
                missing,
                family["row_count"],
                family["minimum_ratio_minus_half"],
                family["payment_over_q46189_adverse"],
                family["maximum_relative_scalar_residual"],
            ))
    lines.extend([
        "```",
        "",
        "## Decision",
        "",
        "The finite group-payment result has a phase-ratio explanation:",
        "`Q=46189` is below the one-half threshold, while every checked",
        "replacement denominator is above it.  This is evidence for a symbolic",
        "replacement ratio inequality as the next theorem target.",
        "",
        "This remains finite diagnostic evidence only.  It proves no symbolic",
        "replacement ratio theorem, replacement-family payment theorem,",
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
        "q46189_ratio_minus_half": (
            receipt["q46189_profile"]["ratio_minus_half"]),
        "replacement_min_ratio_minus_half": (
            receipt["replacement_summary"]["minimum_ratio_minus_half"]),
        "replacement_payment_over_defect": (
            receipt["replacement_summary"][
                "payment_over_q46189_adverse"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
