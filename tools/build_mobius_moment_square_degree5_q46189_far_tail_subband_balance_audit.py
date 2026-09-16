"""Audit whether Q46189 signed balance localizes to far or tail.

The far-tail sign-budget audit found a finite positive-share separator for
the combined far+tail band.  This receipt splits that budget into its two
sub-bands to decide whether the theorem-shaped target should remain combined
or narrow to a single distance range.
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
SOURCE_SIGN_BUDGET = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-far-tail-sign-budget-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-far-tail-subband-balance-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-far-tail-subband-balance-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def bucket_metrics(bucket, diagonal):
    positive = bucket["positive_contribution_sum"] / diagonal
    negative = bucket["negative_contribution_sum"] / diagonal
    total = bucket["component_active_contribution"] / diagonal
    absolute = positive - negative
    return {
        "total_over_diagonal": total,
        "positive_over_diagonal": positive,
        "negative_over_diagonal": negative,
        "absolute_over_diagonal": absolute,
        "positive_fraction_of_absolute": (
            positive / absolute if absolute else None),
    }


def row_summary(row, role):
    diagonal = row["diagonal_half_contribution"]
    buckets = {
        bucket["bucket"]: bucket
        for bucket in row["distance_bucket_contributions"]
    }
    return {
        "role": role,
        "reduced_denominator": row["reduced_denominator"],
        "ratio_minus_half": row["ratio_minus_half"],
        "half_margin": row["component_half_margin_active_minus_half_full"],
        "far_band": bucket_metrics(buckets["far_10A_to_100A"], diagonal),
        "tail_band": bucket_metrics(buckets["tail_over_100A"], diagonal),
        "near_band": bucket_metrics(buckets["near_1_to_A"], diagonal),
        "middle_band": bucket_metrics(buckets["middle_A_to_10A"], diagonal),
    }


def midpoint(a, b):
    return 0.5 * (a + b)


def min_by(rows, band, field):
    return min(rows, key=lambda row: row[band][field])


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
    adverse = row_summary(
        decompose_row(
            DENOMINATOR,
            cells_by_denominator[DENOMINATOR],
            row_count,
            active_row_start,
            by_q[DENOMINATOR],
            "q46189_adverse"),
        "q46189_adverse")
    replacements = [
        row_summary(
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

    min_far_share = min_by(
        replacements, "far_band", "positive_fraction_of_absolute")
    min_far_total = min_by(
        replacements, "far_band", "total_over_diagonal")
    min_tail_share = min_by(
        replacements, "tail_band", "positive_fraction_of_absolute")
    min_tail_total = min_by(
        replacements, "tail_band", "total_over_diagonal")
    far_share_separator = midpoint(
        adverse["far_band"]["positive_fraction_of_absolute"],
        min_far_share["far_band"]["positive_fraction_of_absolute"])
    far_total_separator = midpoint(
        adverse["far_band"]["total_over_diagonal"],
        min_far_total["far_band"]["total_over_diagonal"])
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_far_tail_subband_balance",
        "source_one_coordinate_ledger": str(SOURCE_LEDGER),
        "source_far_tail_sign_budget_audit": str(SOURCE_SIGN_BUDGET),
        "question": (
            "Does the far-tail positive-share separator localize to the far "
            "band, the tail band, or only their combination?"),
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
            row["far_band"]["positive_fraction_of_absolute"]),
        "separation_summary": {
            "adverse_far_positive_fraction": (
                adverse["far_band"]["positive_fraction_of_absolute"]),
            "minimum_replacement_far_positive_fraction": (
                min_far_share["far_band"][
                    "positive_fraction_of_absolute"]),
            "minimum_replacement_far_positive_fraction_denominator": (
                min_far_share["reduced_denominator"]),
            "far_positive_fraction_gap": (
                min_far_share["far_band"][
                    "positive_fraction_of_absolute"]
                - adverse["far_band"][
                    "positive_fraction_of_absolute"]),
            "far_positive_fraction_separator": far_share_separator,
            "adverse_far_total_over_diagonal": (
                adverse["far_band"]["total_over_diagonal"]),
            "minimum_replacement_far_total_over_diagonal": (
                min_far_total["far_band"]["total_over_diagonal"]),
            "minimum_replacement_far_total_denominator": (
                min_far_total["reduced_denominator"]),
            "far_total_gap": (
                min_far_total["far_band"]["total_over_diagonal"]
                - adverse["far_band"]["total_over_diagonal"]),
            "far_total_separator": far_total_separator,
            "all_replacements_above_far_positive_fraction_separator": all(
                row["far_band"]["positive_fraction_of_absolute"]
                > far_share_separator
                for row in replacements),
            "adverse_below_far_positive_fraction_separator": (
                adverse["far_band"]["positive_fraction_of_absolute"]
                < far_share_separator),
            "all_replacements_above_far_total_separator": all(
                row["far_band"]["total_over_diagonal"]
                > far_total_separator
                for row in replacements),
            "adverse_below_far_total_separator": (
                adverse["far_band"]["total_over_diagonal"]
                < far_total_separator),
        },
        "tail_non_separator": {
            "adverse_tail_positive_fraction": (
                adverse["tail_band"]["positive_fraction_of_absolute"]),
            "minimum_replacement_tail_positive_fraction": (
                min_tail_share["tail_band"][
                    "positive_fraction_of_absolute"]),
            "minimum_replacement_tail_positive_fraction_denominator": (
                min_tail_share["reduced_denominator"]),
            "adverse_tail_total_over_diagonal": (
                adverse["tail_band"]["total_over_diagonal"]),
            "minimum_replacement_tail_total_over_diagonal": (
                min_tail_total["tail_band"]["total_over_diagonal"]),
            "minimum_replacement_tail_total_denominator": (
                min_tail_total["reduced_denominator"]),
            "tail_positive_fraction_separates": False,
            "tail_total_separates": False,
            "reason": (
                "Replacement q=40755 is worse than Q=46189 by both tail "
                "positive share and tail total, so the separator is not a "
                "tail-only effect."),
        },
        "classification": {
            "far_positive_share_separates_finite_family": (
                adverse["far_band"]["positive_fraction_of_absolute"]
                < far_share_separator
                and all(row["far_band"][
                        "positive_fraction_of_absolute"]
                    > far_share_separator
                    for row in replacements)),
            "far_total_pressure_separates_finite_family": (
                adverse["far_band"]["total_over_diagonal"]
                < far_total_separator
                and all(row["far_band"]["total_over_diagonal"]
                        > far_total_separator
                        for row in replacements)),
            "tail_positive_share_separates": False,
            "tail_total_pressure_separates": False,
            "finite_selected_family_diagnostic_only": True,
        },
        "candidate_next_action": {
            "name": "far-band signed-balance lower bound",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The source-admissible replacement rows keep enough positive "
                "mass in the far band A*10..A*100 to avoid the Q=46189 "
                "overpayment."),
            "prediction": (
                "A theorem route should first target the far band alone; tail "
                "control is not the finite separator."),
            "falsifier": (
                "A source-admissible replacement row with far-band positive "
                "share or total pressure at or below the finite separator "
                "falsifies this narrowed target."),
            "smallest_next_test": (
                "Classify the residue distances contributing positive far-"
                "band mass and test whether their distribution differs "
                "structurally from Q=46189."),
        },
        "decision": (
            "The broad signed-balance separator localizes to the far band.  "
            "Tail is a non-separator: q=40755 is worse than Q=46189 in tail "
            "positive share and tail total.  The next theorem-shaped target "
            "is therefore a far-band signed-balance lower bound."),
        "finite_far_tail_subband_balance_audit_only": True,
        "finite_diagnostic_only": True,
        "far_band_positive_share_theorem_proved": False,
        "far_band_pressure_theorem_proved": False,
        "tail_band_pressure_theorem_proved": False,
        "far_tail_positive_share_theorem_proved": False,
        "replacement_residue_gap_bound_theorem_proved": False,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    summary = receipt["separation_summary"]
    tail = receipt["tail_non_separator"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 far-tail sub-band balance audit",
        "",
        "## Question",
        "",
        "Does the far-tail positive-share separator localize to the far band,",
        "the tail band, or only their combination?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_far_tail_subband_balance_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-far-tail-subband-balance-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"Q far positive share:                {summary['adverse_far_positive_fraction']}",
        f"min replacement far positive share:  {summary['minimum_replacement_far_positive_fraction']}",
        f"far positive-share gap:              {summary['far_positive_fraction_gap']}",
        f"Q far total / diag:                  {summary['adverse_far_total_over_diagonal']}",
        f"min replacement far total / diag:    {summary['minimum_replacement_far_total_over_diagonal']}",
        f"far total gap:                       {summary['far_total_gap']}",
        f"Q tail positive share:               {tail['adverse_tail_positive_fraction']}",
        f"min replacement tail positive share: {tail['minimum_replacement_tail_positive_fraction']}",
        f"Q tail total / diag:                 {tail['adverse_tail_total_over_diagonal']}",
        f"min replacement tail total / diag:   {tail['minimum_replacement_tail_total_over_diagonal']}",
        "```",
        "",
        "## Decision",
        "",
        "The broad signed-balance separator localizes to the far band.  Tail is",
        "a non-separator: `q=40755` is worse than `Q=46189` in tail positive",
        "share and tail total.  The next theorem-shaped target is therefore a",
        "far-band signed-balance lower bound.",
        "",
        "This is finite selected-family diagnostic evidence only.  It proves no",
        "far-band positive-share theorem, far-band pressure theorem, tail-band",
        "pressure theorem, far-tail positive-share theorem, replacement",
        "residue-gap bound theorem, coordinate-00 residue-gap sign theorem,",
        "strict-central Goldbach theorem, or Goldbach proof.",
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
        "far_positive_fraction_gap": (
            receipt["separation_summary"][
                "far_positive_fraction_gap"]),
        "far_total_gap": (
            receipt["separation_summary"]["far_total_gap"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
