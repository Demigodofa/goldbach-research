"""Audit the far-tail sign budget behind the Q46189 pressure separator.

The pressure-separation audit found that Q=46189 is separated from every
source-admissible replacement by broad far+tail and non-middle pressure.  This
receipt asks whether that separation comes from a larger negative envelope or
from signed balance inside the broad residue-gap budget.
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
from tools.build_mobius_moment_square_degree5_q46189_coordinate00_kernel_decomposition_audit import (  # noqa: E402
    decompose_row,
    ledger_rows,
)
from tools.build_mobius_moment_square_degree5_q46189_exception_bound_audit import (  # noqa: E402
    DENOMINATOR,
    PRIME,
    SCALE,
    TARGET_LABEL,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _residue_cells_by_denominator,
)


SOURCE_LEDGER = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-one-coordinate-ratio-ledger-audit.json")
SOURCE_PRESSURE = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-residue-gap-pressure-separation-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-far-tail-sign-budget-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-far-tail-sign-budget-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def bucket_dict(row):
    return {
        bucket["bucket"]: bucket
        for bucket in row["distance_bucket_contributions"]
    }


def budget(buckets, names, diagonal):
    positive = sum(
        buckets[name]["positive_contribution_sum"] for name in names)
    negative = sum(
        buckets[name]["negative_contribution_sum"] for name in names)
    total = sum(
        buckets[name]["component_active_contribution"] for name in names)
    absolute = positive - negative
    return {
        "total_over_diagonal": total / diagonal,
        "positive_over_diagonal": positive / diagonal,
        "negative_over_diagonal": negative / diagonal,
        "absolute_over_diagonal": absolute / diagonal,
        "positive_fraction_of_absolute": (
            positive / absolute if absolute else None),
        "negative_fraction_of_absolute": (
            -negative / absolute if absolute else None),
    }


def summarize(row, role):
    diagonal = row["diagonal_half_contribution"]
    buckets = bucket_dict(row)
    return {
        "role": role,
        "reduced_denominator": row["reduced_denominator"],
        "ratio_minus_half": row["ratio_minus_half"],
        "half_margin": row["component_half_margin_active_minus_half_full"],
        "diagonal_half_contribution": diagonal,
        "off_diagonal_over_diagonal_half": (
            row["off_diagonal_over_diagonal_half"]),
        "far_tail_budget": budget(
            buckets, ["far_10A_to_100A", "tail_over_100A"], diagonal),
        "nonmiddle_budget": budget(
            buckets,
            ["near_1_to_A", "far_10A_to_100A", "tail_over_100A"],
            diagonal),
        "middle_budget": budget(
            buckets, ["middle_A_to_10A"], diagonal),
    }


def midpoint(a, b):
    return 0.5 * (a + b)


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
    adverse = summarize(
        decompose_row(
            DENOMINATOR,
            cells_by_denominator[DENOMINATOR],
            row_count,
            active_row_start,
            by_q[DENOMINATOR],
            "q46189_adverse"),
        "q46189_adverse")
    replacements = [
        summarize(
            decompose_row(
                ledger_row["reduced_denominator"],
                cells_by_denominator[ledger_row["reduced_denominator"]],
                row_count,
                active_row_start,
                by_q[ledger_row["reduced_denominator"]],
                "replacement"),
            "replacement")
        for ledger_row in ledger["replacement_one_coordinate_rows"]
    ]
    min_far_tail_positive_share = min(
        replacements,
        key=lambda row:
        row["far_tail_budget"]["positive_fraction_of_absolute"])
    min_nonmiddle_positive_share = min(
        replacements,
        key=lambda row:
        row["nonmiddle_budget"]["positive_fraction_of_absolute"])
    min_far_tail_negative = min(
        replacements,
        key=lambda row: row["far_tail_budget"]["negative_over_diagonal"])
    min_nonmiddle_negative = min(
        replacements,
        key=lambda row: row["nonmiddle_budget"]["negative_over_diagonal"])
    far_tail_share_separator = midpoint(
        adverse["far_tail_budget"]["positive_fraction_of_absolute"],
        min_far_tail_positive_share[
            "far_tail_budget"]["positive_fraction_of_absolute"])
    nonmiddle_share_separator = midpoint(
        adverse["nonmiddle_budget"]["positive_fraction_of_absolute"],
        min_nonmiddle_positive_share[
            "nonmiddle_budget"]["positive_fraction_of_absolute"])
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_far_tail_sign_budget",
        "source_one_coordinate_ledger": str(SOURCE_LEDGER),
        "source_pressure_separation_audit": str(SOURCE_PRESSURE),
        "question": (
            "Does the Q=46189 broad far-tail/non-middle separator come from a "
            "larger negative envelope or from signed balance inside the "
            "broad residue-gap budget?"),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": row_count,
            "active_row_start": active_row_start,
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "replacement_row_count": len(replacements),
        },
        "adverse_row": adverse,
        "replacement_rows": sorted(
            replacements,
            key=lambda row:
            row["far_tail_budget"]["positive_fraction_of_absolute"]),
        "separation_summary": {
            "adverse_far_tail_positive_fraction": (
                adverse["far_tail_budget"][
                    "positive_fraction_of_absolute"]),
            "minimum_replacement_far_tail_positive_fraction": (
                min_far_tail_positive_share["far_tail_budget"][
                    "positive_fraction_of_absolute"]),
            "minimum_replacement_far_tail_positive_fraction_denominator": (
                min_far_tail_positive_share["reduced_denominator"]),
            "far_tail_positive_fraction_gap": (
                min_far_tail_positive_share["far_tail_budget"][
                    "positive_fraction_of_absolute"]
                - adverse["far_tail_budget"][
                    "positive_fraction_of_absolute"]),
            "far_tail_positive_fraction_separator": (
                far_tail_share_separator),
            "adverse_below_far_tail_positive_fraction_separator": (
                adverse["far_tail_budget"][
                    "positive_fraction_of_absolute"]
                < far_tail_share_separator),
            "all_replacements_above_far_tail_positive_fraction_separator": (
                all(row["far_tail_budget"][
                        "positive_fraction_of_absolute"]
                    > far_tail_share_separator
                    for row in replacements)),
            "adverse_nonmiddle_positive_fraction": (
                adverse["nonmiddle_budget"][
                    "positive_fraction_of_absolute"]),
            "minimum_replacement_nonmiddle_positive_fraction": (
                min_nonmiddle_positive_share["nonmiddle_budget"][
                    "positive_fraction_of_absolute"]),
            "minimum_replacement_nonmiddle_positive_fraction_denominator": (
                min_nonmiddle_positive_share["reduced_denominator"]),
            "nonmiddle_positive_fraction_gap": (
                min_nonmiddle_positive_share["nonmiddle_budget"][
                    "positive_fraction_of_absolute"]
                - adverse["nonmiddle_budget"][
                    "positive_fraction_of_absolute"]),
            "nonmiddle_positive_fraction_separator": (
                nonmiddle_share_separator),
            "adverse_below_nonmiddle_positive_fraction_separator": (
                adverse["nonmiddle_budget"][
                    "positive_fraction_of_absolute"]
                < nonmiddle_share_separator),
            "all_replacements_above_nonmiddle_positive_fraction_separator": (
                all(row["nonmiddle_budget"][
                        "positive_fraction_of_absolute"]
                    > nonmiddle_share_separator
                    for row in replacements)),
        },
        "non_separators": {
            "far_tail_negative_envelope": {
                "adverse_negative_over_diagonal": (
                    adverse["far_tail_budget"]["negative_over_diagonal"]),
                "minimum_replacement_negative_over_diagonal": (
                    min_far_tail_negative[
                        "far_tail_budget"]["negative_over_diagonal"]),
                "minimum_replacement_denominator": (
                    min_far_tail_negative["reduced_denominator"]),
                "separates_adverse_from_replacements": False,
                "reason": (
                    "Replacement q=53295 has a slightly more negative "
                    "far-tail envelope than Q=46189, but its positive "
                    "far-tail offset almost cancels that envelope."),
            },
            "nonmiddle_negative_envelope": {
                "adverse_negative_over_diagonal": (
                    adverse["nonmiddle_budget"]["negative_over_diagonal"]),
                "minimum_replacement_negative_over_diagonal": (
                    min_nonmiddle_negative[
                        "nonmiddle_budget"]["negative_over_diagonal"]),
                "minimum_replacement_denominator": (
                    min_nonmiddle_negative["reduced_denominator"]),
                "separates_adverse_from_replacements": False,
                "reason": (
                    "The non-middle negative envelope is nearly tied with "
                    "replacement q=53295, so a negative-envelope-only theorem "
                    "would miss the signed-balance distinction."),
            },
        },
        "classification": {
            "far_tail_positive_share_separates_finite_family": (
                adverse["far_tail_budget"][
                    "positive_fraction_of_absolute"]
                < far_tail_share_separator
                and all(row["far_tail_budget"][
                        "positive_fraction_of_absolute"]
                    > far_tail_share_separator
                    for row in replacements)),
            "nonmiddle_positive_share_separates_finite_family": (
                adverse["nonmiddle_budget"][
                    "positive_fraction_of_absolute"]
                < nonmiddle_share_separator
                and all(row["nonmiddle_budget"][
                        "positive_fraction_of_absolute"]
                    > nonmiddle_share_separator
                    for row in replacements)),
            "far_tail_negative_envelope_separates": False,
            "nonmiddle_negative_envelope_separates": False,
            "finite_selected_family_diagnostic_only": True,
        },
        "candidate_next_action": {
            "name": "broad signed-balance lower bound",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Source-admissible replacements may survive because positive "
                "broad far-tail/non-middle mass occupies a larger share of the "
                "absolute broad budget than in the adverse Q row."),
            "prediction": (
                "A source-admissible family theorem should control signed "
                "balance or positive-share, not just the negative envelope."),
            "falsifier": (
                "A source-admissible replacement with far-tail positive share "
                "at or below the adverse/replacement separator falsifies this "
                "finite sign-budget mechanism."),
            "smallest_next_test": (
                "Derive the residue-class condition that forces positive "
                "far-tail share above the finite separator, or find a fresh "
                "source-admissible row below it."),
        },
        "decision": (
            "The broad pressure separator is a signed-balance effect.  The "
            "negative far-tail envelope alone does not separate Q=46189 from "
            "the replacements; q=53295 is slightly worse by that metric.  The "
            "finite separator is the positive share of the broad absolute "
            "budget, especially in far+tail."),
        "finite_far_tail_sign_budget_audit_only": True,
        "finite_diagnostic_only": True,
        "far_tail_positive_share_theorem_proved": False,
        "nonmiddle_positive_share_theorem_proved": False,
        "far_tail_pressure_theorem_proved": False,
        "replacement_residue_gap_bound_theorem_proved": False,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    summary = receipt["separation_summary"]
    non_sep = receipt["non_separators"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 far-tail sign-budget audit",
        "",
        "## Question",
        "",
        "Does the `Q=46189` broad far-tail/non-middle separator come from a",
        "larger negative envelope or from signed balance inside the broad",
        "residue-gap budget?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_far_tail_sign_budget_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-far-tail-sign-budget-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"Q far-tail positive share:              {summary['adverse_far_tail_positive_fraction']}",
        f"min replacement far-tail positive share:{summary['minimum_replacement_far_tail_positive_fraction']}",
        f"far-tail positive-share gap:            {summary['far_tail_positive_fraction_gap']}",
        f"Q non-middle positive share:            {summary['adverse_nonmiddle_positive_fraction']}",
        f"min replacement non-middle positive share:{summary['minimum_replacement_nonmiddle_positive_fraction']}",
        f"non-middle positive-share gap:          {summary['nonmiddle_positive_fraction_gap']}",
        "```",
        "",
        "The negative-envelope shortcut fails:",
        "",
        "```text",
        f"Q far-tail negative / diag:             {non_sep['far_tail_negative_envelope']['adverse_negative_over_diagonal']}",
        f"min replacement far-tail negative / diag:{non_sep['far_tail_negative_envelope']['minimum_replacement_negative_over_diagonal']}",
        f"Q non-middle negative / diag:           {non_sep['nonmiddle_negative_envelope']['adverse_negative_over_diagonal']}",
        f"min replacement non-middle negative / diag:{non_sep['nonmiddle_negative_envelope']['minimum_replacement_negative_over_diagonal']}",
        "```",
        "",
        "## Decision",
        "",
        "The broad pressure separator is a signed-balance effect.  The negative",
        "far-tail envelope alone does not separate `Q=46189` from the",
        "replacements; `q=53295` is slightly worse by that metric.  The finite",
        "separator is the positive share of the broad absolute budget,",
        "especially in far+tail.",
        "",
        "The next theorem-shaped target is a broad signed-balance lower bound.",
        "This is finite selected-family diagnostic evidence only.  It proves no",
        "far-tail positive-share theorem, non-middle positive-share theorem,",
        "far-tail pressure theorem, replacement residue-gap bound theorem,",
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
        "far_tail_positive_share_gap": (
            receipt["separation_summary"][
                "far_tail_positive_fraction_gap"]),
        "nonmiddle_positive_share_gap": (
            receipt["separation_summary"][
                "nonmiddle_positive_fraction_gap"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
