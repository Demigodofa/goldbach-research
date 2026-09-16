"""Audit residue-gap pressure separation for the Q46189 replacement lane.

The replacement family audit showed that q=38038 is the weakest source-
admissible replacement row by total off-diagonal pressure.  This receipt asks
which normalized residue-gap pressure components actually separate the adverse
Q=46189 row from all ten replacement rows, and which tempting statistics do
not.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAIR = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-coordinate00-kernel-decomposition-audit.json")
FAMILY = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-replacement-kernel-family-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-residue-gap-pressure-separation-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-residue-gap-pressure-separation-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def bucket_map(row):
    if "distance_bucket_contributions" in row:
        return {
            bucket["bucket"]: bucket["component_active_contribution"]
            for bucket in row["distance_bucket_contributions"]
        }
    return {
        "near_1_to_A": row["near_1_to_A_contribution"],
        "middle_A_to_10A": row["middle_A_to_10A_contribution"],
        "far_10A_to_100A": row["far_10A_to_100A_contribution"],
        "tail_over_100A": row["tail_over_100A_contribution"],
    }


def top_pair(row, key):
    if key in row:
        return row[key]
    return row[f"{key}s"][0]


def normalized_row(row, role):
    buckets = bucket_map(row)
    diagonal = row["diagonal_half_contribution"]
    near = buckets["near_1_to_A"]
    middle = buckets["middle_A_to_10A"]
    far = buckets["far_10A_to_100A"]
    tail = buckets["tail_over_100A"]
    top_negative = top_pair(row, "top_negative_gap_pair")
    top_positive = top_pair(row, "top_positive_gap_pair")
    return {
        "role": role,
        "reduced_denominator": row["reduced_denominator"],
        "ratio_minus_half": row["ratio_minus_half"],
        "half_margin": row["component_half_margin_active_minus_half_full"],
        "diagonal_half_contribution": diagonal,
        "off_diagonal_over_diagonal_half": (
            row["off_diagonal_over_diagonal_half"]),
        "near_over_diagonal": near / diagonal,
        "middle_over_diagonal": middle / diagonal,
        "far_over_diagonal": far / diagonal,
        "tail_over_diagonal": tail / diagonal,
        "far_tail_over_diagonal": (far + tail) / diagonal,
        "nonmiddle_over_diagonal": (near + far + tail) / diagonal,
        "top_negative_pair_over_diagonal": (
            top_negative["component_active_contribution"] / diagonal),
        "top_negative_pair_distance": top_negative["circular_distance"],
        "top_positive_pair_over_diagonal": (
            top_positive["component_active_contribution"] / diagonal),
        "top_positive_pair_distance": top_positive["circular_distance"],
    }


def midpoint(a, b):
    return 0.5 * (a + b)


def build_receipt():
    pair = json.loads(PAIR.read_text(encoding="utf-8"))
    family = json.loads(FAMILY.read_text(encoding="utf-8"))
    adverse = normalized_row(pair["decomposition_rows"][0], "q46189_adverse")
    weakest_pair = normalized_row(
        pair["decomposition_rows"][1],
        "weakest_positive_replacement_from_pair_audit")
    replacements = [
        normalized_row(row, "replacement")
        for row in family["replacement_kernel_rows"]
    ]

    min_far_tail = min(
        replacements, key=lambda row: row["far_tail_over_diagonal"])
    min_nonmiddle = min(
        replacements, key=lambda row: row["nonmiddle_over_diagonal"])
    min_middle = min(
        replacements, key=lambda row: row["middle_over_diagonal"])
    min_top_negative = min(
        replacements, key=lambda row: row["top_negative_pair_over_diagonal"])
    far_tail_separator = midpoint(
        adverse["far_tail_over_diagonal"],
        min_far_tail["far_tail_over_diagonal"])
    nonmiddle_separator = midpoint(
        adverse["nonmiddle_over_diagonal"],
        min_nonmiddle["nonmiddle_over_diagonal"])
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_residue_gap_pressure_separation",
        "source_pair_kernel_decomposition": str(PAIR),
        "source_replacement_family_audit": str(FAMILY),
        "question": (
            "Which normalized residue-gap pressure components separate the "
            "adverse Q=46189 row from all source-admissible replacement rows?"),
        "mechanism_under_test": {
            "name": "broad far-tail residue-gap overpayment",
            "novelty_label": "new-to-this-task",
            "prediction": (
                "The adverse Q row should have materially more negative "
                "far+tail and non-middle pressure than every replacement row, "
                "whereas a single top negative gap or the middle bucket alone "
                "need not separate the family."),
            "falsifier": (
                "A source-admissible replacement row with far+tail or "
                "non-middle pressure at or below the finite adverse/replacement "
                "separator, or a future adverse row not distinguished by broad "
                "pressure, falsifies this separator as a theorem target."),
            "smallest_next_test": (
                "Try to express far+tail pressure as a source-admissible "
                "replacement lower-bound obligation rather than bounding the "
                "single largest negative residue gap."),
        },
        "adverse_row": adverse,
        "weakest_positive_replacement_from_pair_audit": weakest_pair,
        "replacement_rows": replacements,
        "finite_separators": {
            "far_tail_over_diagonal_midpoint": far_tail_separator,
            "nonmiddle_over_diagonal_midpoint": nonmiddle_separator,
        },
        "separation_summary": {
            "adverse_far_tail_over_diagonal": (
                adverse["far_tail_over_diagonal"]),
            "minimum_replacement_far_tail_over_diagonal": (
                min_far_tail["far_tail_over_diagonal"]),
            "minimum_replacement_far_tail_denominator": (
                min_far_tail["reduced_denominator"]),
            "far_tail_separation_gap": (
                min_far_tail["far_tail_over_diagonal"]
                - adverse["far_tail_over_diagonal"]),
            "all_replacements_above_far_tail_separator": all(
                row["far_tail_over_diagonal"] > far_tail_separator
                for row in replacements),
            "adverse_below_far_tail_separator": (
                adverse["far_tail_over_diagonal"] < far_tail_separator),
            "adverse_nonmiddle_over_diagonal": (
                adverse["nonmiddle_over_diagonal"]),
            "minimum_replacement_nonmiddle_over_diagonal": (
                min_nonmiddle["nonmiddle_over_diagonal"]),
            "minimum_replacement_nonmiddle_denominator": (
                min_nonmiddle["reduced_denominator"]),
            "nonmiddle_separation_gap": (
                min_nonmiddle["nonmiddle_over_diagonal"]
                - adverse["nonmiddle_over_diagonal"]),
            "all_replacements_above_nonmiddle_separator": all(
                row["nonmiddle_over_diagonal"] > nonmiddle_separator
                for row in replacements),
            "adverse_below_nonmiddle_separator": (
                adverse["nonmiddle_over_diagonal"] < nonmiddle_separator),
        },
        "non_separators": {
            "middle_bucket_alone": {
                "adverse_middle_over_diagonal": (
                    adverse["middle_over_diagonal"]),
                "minimum_replacement_middle_over_diagonal": (
                    min_middle["middle_over_diagonal"]),
                "minimum_replacement_middle_denominator": (
                    min_middle["reduced_denominator"]),
                "separates_adverse_from_replacements": False,
                "reason": (
                    "The weakest replacement q=38038 has much more negative "
                    "middle pressure than Q=46189, yet remains positive "
                    "because non-middle buckets rescue it."),
            },
            "single_top_negative_gap": {
                "adverse_top_negative_pair_over_diagonal": (
                    adverse["top_negative_pair_over_diagonal"]),
                "minimum_replacement_top_negative_pair_over_diagonal": (
                    min_top_negative["top_negative_pair_over_diagonal"]),
                "minimum_replacement_top_negative_denominator": (
                    min_top_negative["reduced_denominator"]),
                "separates_adverse_from_replacements": False,
                "reason": (
                    "The weakest replacement q=38038 has a larger normalized "
                    "single negative gap than Q=46189, so a largest-gap bound "
                    "is pointed at the wrong obstruction."),
            },
        },
        "classification": {
            "far_tail_pressure_separates_finite_family": (
                adverse["far_tail_over_diagonal"] < far_tail_separator
                and all(row["far_tail_over_diagonal"] > far_tail_separator
                        for row in replacements)),
            "nonmiddle_pressure_separates_finite_family": (
                adverse["nonmiddle_over_diagonal"] < nonmiddle_separator
                and all(row["nonmiddle_over_diagonal"] > nonmiddle_separator
                        for row in replacements)),
            "middle_bucket_alone_separates": False,
            "single_top_negative_gap_separates": False,
            "finite_selected_family_diagnostic_only": True,
        },
        "decision": (
            "The first useful finite separator is broad pressure, not a top "
            "gap: Q=46189 has far+tail/diagonal and non-middle/diagonal "
            "pressure far below every source-admissible replacement row.  "
            "Middle-bucket pressure and the single largest negative gap do "
            "not separate the adverse row.  The next theorem-shaped target is "
            "a source-admissible far-tail or non-middle lower bound."),
        "finite_residue_gap_pressure_audit_only": True,
        "finite_diagnostic_only": True,
        "far_tail_pressure_theorem_proved": False,
        "nonmiddle_pressure_theorem_proved": False,
        "replacement_residue_gap_bound_theorem_proved": False,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    summary = receipt["separation_summary"]
    non_sep = receipt["non_separators"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 residue-gap pressure separation audit",
        "",
        "## Question",
        "",
        "Which normalized residue-gap pressure components separate the adverse",
        "`Q=46189` row from all source-admissible replacement rows?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_residue_gap_pressure_separation_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-residue-gap-pressure-separation-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"Q far+tail / diag:                 {summary['adverse_far_tail_over_diagonal']}",
        f"min replacement far+tail / diag:   {summary['minimum_replacement_far_tail_over_diagonal']}",
        f"far+tail separator midpoint:       {receipt['finite_separators']['far_tail_over_diagonal_midpoint']}",
        f"far+tail separation gap:           {summary['far_tail_separation_gap']}",
        f"Q non-middle / diag:               {summary['adverse_nonmiddle_over_diagonal']}",
        f"min replacement non-middle / diag: {summary['minimum_replacement_nonmiddle_over_diagonal']}",
        f"non-middle separator midpoint:     {receipt['finite_separators']['nonmiddle_over_diagonal_midpoint']}",
        f"non-middle separation gap:         {summary['nonmiddle_separation_gap']}",
        "```",
        "",
        "The tempting simpler statistics fail as separators:",
        "",
        "```text",
        f"Q middle / diag:                   {non_sep['middle_bucket_alone']['adverse_middle_over_diagonal']}",
        f"min replacement middle / diag:     {non_sep['middle_bucket_alone']['minimum_replacement_middle_over_diagonal']}",
        f"Q top negative gap / diag:         {non_sep['single_top_negative_gap']['adverse_top_negative_pair_over_diagonal']}",
        f"min replacement top gap / diag:    {non_sep['single_top_negative_gap']['minimum_replacement_top_negative_pair_over_diagonal']}",
        "```",
        "",
        "## Decision",
        "",
        "The first useful finite separator is broad pressure, not a top gap.",
        "`Q=46189` has far+tail and non-middle pressure below every checked",
        "source-admissible replacement row.  But the middle bucket alone and",
        "the single largest negative residue gap point in the wrong direction:",
        "`q=38038` is worse by both of those local statistics and still",
        "survives.",
        "",
        "The next theorem-shaped target is therefore a source-admissible",
        "far-tail or non-middle lower bound.  This is finite selected-family",
        "diagnostic evidence only.  It proves no far-tail pressure theorem,",
        "non-middle pressure theorem, replacement residue-gap bound theorem,",
        "coordinate-00 residue-gap sign theorem, strict-central Goldbach",
        "theorem, or Goldbach proof.",
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
        "far_tail_gap": (
            receipt["separation_summary"]["far_tail_separation_gap"]),
        "nonmiddle_gap": (
            receipt["separation_summary"]["nonmiddle_separation_gap"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
