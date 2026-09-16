"""Group source-start denominator margins by clearance above the cutoff.

The denominator decomposition showed that the tight source-start margins are
positive signed ledgers over reduced denominators Q.  This derived receipt asks
whether adverse denominator mass is structurally tied to the near-threshold
family Q just above p*A, where A is the source row count.
"""

from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    scale_parameters,
)
from tools.build_mobius_moment_square_degree5_source_margin_denominator_audit import (  # noqa: E402
    THEOREM_OBLIGATION,
    label_rows_from_denominator,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _residue_cells_by_denominator,
)


OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-source-margin-clearance-family-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def clearance_family(reduced_denominator, threshold):
    if reduced_denominator < 2 * threshold:
        return "near_1_to_2"
    if reduced_denominator < 3 * threshold:
        return "middle_2_to_3"
    return "far_3_plus"


def margin_summary(rows):
    positive = [
        row for row in rows
        if row["unnormalized_margin_full_over_2_minus_active"] > 0]
    negative = [
        row for row in rows
        if row["unnormalized_margin_full_over_2_minus_active"] < 0]
    positive_sum = sum(
        row["unnormalized_margin_full_over_2_minus_active"]
        for row in positive)
    negative_sum = sum(
        row["unnormalized_margin_full_over_2_minus_active"]
        for row in negative)
    total = positive_sum + negative_sum
    largest_positive = max(
        positive,
        key=lambda row: row["unnormalized_margin_full_over_2_minus_active"],
        default=None)
    largest_negative = min(
        negative,
        key=lambda row: row["unnormalized_margin_full_over_2_minus_active"],
        default=None)
    return {
        "row_count": len(rows),
        "positive_count": len(positive),
        "negative_count": len(negative),
        "positive_margin_sum": positive_sum,
        "negative_margin_sum": negative_sum,
        "total_margin": total,
        "abs_negative_over_positive": (
            abs(negative_sum) / positive_sum if positive_sum else None),
        "largest_positive": largest_positive,
        "largest_negative": largest_negative,
    }


def compact_denominator_row(row, threshold):
    if row is None:
        return None
    return {
        "reduced_denominator": row["reduced_denominator"],
        "clearance_ratio_q_over_pA": (
            row["reduced_denominator"] / threshold),
        "margin": row["unnormalized_margin_full_over_2_minus_active"],
    }


def scale_clearance_summary(obligation_row):
    scale = obligation_row["scale_modulus"]
    prime = obligation_row["top_prime_block"]["prime_modulus"]
    print(f"clearance families M={scale}, p={prime}", flush=True)
    parameters = scale_parameters(scale)
    row_count = parameters["row_count"]
    threshold = prime * row_count
    _, cells_by_denominator = _residue_cells_by_denominator(
        prime,
        row_count,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    denominator_rows = []
    for reduced_denominator, cells in sorted(cells_by_denominator.items()):
        denominator_rows.extend(label_rows_from_denominator(
            reduced_denominator, cells, row_count, row_count))
    weakest_label = obligation_row["top_prime_block"]["weakest_label"]
    weakest_rows = [
        row for row in denominator_rows if row["label"] == weakest_label]
    families = {"near_1_to_2": [], "middle_2_to_3": [], "far_3_plus": []}
    for row in weakest_rows:
        families[clearance_family(row["reduced_denominator"], threshold)].append(
            row)
    family_summaries = {
        family: margin_summary(rows)
        for family, rows in families.items()
    }
    total_summary = margin_summary(weakest_rows)
    near_negative = abs(
        family_summaries["near_1_to_2"]["negative_margin_sum"])
    middle_far_positive = (
        family_summaries["middle_2_to_3"]["positive_margin_sum"]
        + family_summaries["far_3_plus"]["positive_margin_sum"])
    middle_far_total = (
        family_summaries["middle_2_to_3"]["total_margin"]
        + family_summaries["far_3_plus"]["total_margin"])
    for summary in family_summaries.values():
        summary["largest_positive"] = compact_denominator_row(
            summary["largest_positive"], threshold)
        summary["largest_negative"] = compact_denominator_row(
            summary["largest_negative"], threshold)
    total_summary["largest_positive"] = compact_denominator_row(
        total_summary["largest_positive"], threshold)
    total_summary["largest_negative"] = compact_denominator_row(
        total_summary["largest_negative"], threshold)
    return {
        "scale_modulus": scale,
        "prime_modulus": prime,
        "weakest_label": weakest_label,
        "row_count_A": row_count,
        "threshold_p_times_A": threshold,
        "family_summaries": family_summaries,
        "total_summary": total_summary,
        "near_negative_abs": near_negative,
        "middle_far_positive_margin_sum": middle_far_positive,
        "middle_far_total_margin_sum": middle_far_total,
        "middle_far_positive_dominates_near_negative": (
            middle_far_positive > near_negative),
        "middle_far_total_dominates_near_negative": (
            middle_far_total > near_negative),
        "all_negative_denominators_near_threshold": (
            family_summaries["middle_2_to_3"]["negative_count"] == 0
            and family_summaries["far_3_plus"]["negative_count"] == 0),
    }


def build_receipt():
    obligation = json.loads(THEOREM_OBLIGATION.read_text(encoding="utf-8"))
    source_rows = obligation["scale_obligation_records"]
    scale_summaries = []
    with ProcessPoolExecutor(max_workers=min(3, len(source_rows))) as executor:
        futures = {
            executor.submit(scale_clearance_summary, row): row["scale_modulus"]
            for row in source_rows
        }
        for future in as_completed(futures):
            scale_summaries.append(future.result())
    scale_summaries.sort(key=lambda row: row["scale_modulus"])
    near_ratios = [
        row["family_summaries"]["near_1_to_2"]["abs_negative_over_positive"]
        for row in scale_summaries
        if row["family_summaries"]["near_1_to_2"][
            "abs_negative_over_positive"] is not None
    ]
    dominance_ratios = [
        row["near_negative_abs"] / row["middle_far_positive_margin_sum"]
        for row in scale_summaries
        if row["middle_far_positive_margin_sum"] > 0
    ]
    negative_family_counts = {
        family: sum(
            row["family_summaries"][family]["negative_count"]
            for row in scale_summaries)
        for family in ("near_1_to_2", "middle_2_to_3", "far_3_plus")
    }
    total_negative_count = sum(negative_family_counts.values())
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_degree5_source_margin_clearance_family",
        "source_theorem_obligation_audit": str(THEOREM_OBLIGATION),
        "question": (
            "For the tightest checked source-start prime blocks, how does "
            "adverse denominator mass split by clearance above the p*A cutoff, "
            "and is low-clearance leakage dominated by higher-clearance mass?"),
        "clearance_families": {
            "near_1_to_2": "p*A < Q < 2*p*A",
            "middle_2_to_3": "2*p*A <= Q < 3*p*A",
            "far_3_plus": "Q >= 3*p*A",
        },
        "scale_summaries": scale_summaries,
        "scale_count": len(scale_summaries),
        "all_negative_denominators_near_threshold": all(
            row["all_negative_denominators_near_threshold"]
            for row in scale_summaries),
        "all_middle_far_positive_dominates_near_negative": all(
            row["middle_far_positive_dominates_near_negative"]
            for row in scale_summaries),
        "all_middle_far_total_dominates_near_negative": all(
            row["middle_far_total_dominates_near_negative"]
            for row in scale_summaries),
        "negative_denominator_family_counts": negative_family_counts,
        "near_threshold_negative_denominator_fraction": (
            negative_family_counts["near_1_to_2"] / total_negative_count
            if total_negative_count else None),
        "maximum_near_family_abs_negative_over_positive": max(near_ratios),
        "maximum_near_negative_over_middle_far_positive": max(
            dominance_ratios),
        "candidate_next_theorem_subtarget": {
            "name": "near-threshold leakage versus higher-clearance dominance",
            "mechanism": (
                "Split the signed reduced-denominator margin ledger at "
                "multiples of p*A.  Treat low-clearance adverse leakage as "
                "the cost side and prove it is bounded by the net middle/far "
                "higher-clearance families."),
            "prediction": (
                "Future tight source-start blocks should have middle/far "
                "higher-clearance net margin large enough to dominate "
                "near-threshold adverse leakage, even if occasional "
                "middle-band denominators are adverse."),
            "falsifier": (
                "A tight source-start block whose middle/far net margin fails "
                "to dominate near-threshold adverse mass falsifies this "
                "family split."),
            "novelty_label": "new-to-this-task",
        },
        "finite_clearance_family_audit_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_start_theorem_proved": False,
        "prime_block_theorem_proved": False,
        "denominator_margin_theorem_proved": False,
        "clearance_family_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
    }


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
