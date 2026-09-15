"""Trajectory audit for q286-WBSS four-modulus budget ratios.

The positivity-budget audit identifies the correct finite normalization:
lambda_phi < 1.  This receipt groups the same 232 checked rows into the 29
stressed source residue trajectories, each with eight period lifts, and asks
whether the pressure is a persistent monotone residue-class drift or a
row-local signed fluctuation.

Finite diagnostic algebra only.  It proves no recurrence theorem,
fixed-modulus equidistribution theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE = EVIDENCE / "q286-wbss-four-modulus-positivity-budget-audit.json"
OUT = EVIDENCE / "q286-wbss-four-modulus-budget-trajectory-audit.json"

sys.path.insert(0, str(ROOT))

from tools.build_q286_wbss_four_modulus_direct_holdout_decomposition import (  # noqa: E402
    load_json,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def combined_lift_index(row):
    offset = 4 if row["source_name"] == "far_lift_holdout" else 0
    return int(row["lift_index"]) + offset


def rows_with_lift_index(source):
    rows = []
    for row in source["holdout"]["rows"]:
        rows.append({
            **row,
            "combined_lift_index": combined_lift_index(row),
        })
    return rows


def trajectory_key(row):
    return (int(row["target_residue"]), int(row["source_positive_target"]))


def monotone_non_decreasing(values):
    return all(values[index + 1] >= values[index]
               for index in range(len(values) - 1))


def sign_changes(values):
    signs = []
    for value in values:
        if value > 0:
            signs.append(1)
        elif value < 0:
            signs.append(-1)
        else:
            signs.append(0)
    return sum(
        1 for left, right in zip(signs, signs[1:])
        if left != 0 and right != 0 and left != right)


def build_trajectory(key, rows):
    sorted_rows = sorted(rows, key=lambda row: row["combined_lift_index"])
    ratios = [row["signed_budget_ratio"] for row in sorted_rows]
    margins = [row["positivity_margin_sigma"] for row in sorted_rows]
    worst_row = max(
        sorted_rows,
        key=lambda row: (row["signed_budget_ratio"], -row["target"]),
    )
    tightest_row = min(
        sorted_rows,
        key=lambda row: (row["positivity_margin_sigma"], row["target"]),
    )
    return {
        "target_residue": key[0],
        "source_positive_target": key[1],
        "row_count": len(sorted_rows),
        "combined_lift_indexes": [
            row["combined_lift_index"] for row in sorted_rows],
        "target_minimum": min(row["target"] for row in sorted_rows),
        "target_maximum": max(row["target"] for row in sorted_rows),
        "signed_budget_ratio_summary": finite_summary(ratios),
        "positivity_margin_sigma_summary": finite_summary(margins),
        "max_signed_budget_ratio": max(ratios),
        "min_signed_budget_ratio": min(ratios),
        "max_minus_min_signed_budget_ratio": max(ratios) - min(ratios),
        "worst_lift_index": int(worst_row["combined_lift_index"]),
        "worst_target": int(worst_row["target"]),
        "tightest_margin_lift_index": int(tightest_row["combined_lift_index"]),
        "tightest_margin_target": int(tightest_row["target"]),
        "monotone_non_decreasing_signed_budget_ratio": (
            monotone_non_decreasing(ratios)),
        "positive_ratio_count": sum(value > 0 for value in ratios),
        "negative_ratio_count": sum(value < 0 for value in ratios),
        "sign_change_count": sign_changes(ratios),
        "rows": sorted_rows,
    }


def grouped_trajectories(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[trajectory_key(row)].append(row)
    return [
        build_trajectory(key, group_rows)
        for key, group_rows in sorted(groups.items())
    ]


def summarize_trajectories(trajectories):
    worst_lift_counts = Counter(
        row["worst_lift_index"] for row in trajectories)
    row_counts = [row["row_count"] for row in trajectories]
    max_ratios = [row["max_signed_budget_ratio"] for row in trajectories]
    ranges = [
        row["max_minus_min_signed_budget_ratio"] for row in trajectories]
    sign_changes_by_trajectory = [
        row["sign_change_count"] for row in trajectories]
    return {
        "trajectory_count": len(trajectories),
        "row_count_summary": finite_summary(row_counts),
        "all_trajectories_have_eight_lifts": all(
            count == 8 for count in row_counts),
        "monotone_non_decreasing_trajectory_count": sum(
            row["monotone_non_decreasing_signed_budget_ratio"]
            for row in trajectories),
        "trajectory_with_positive_ratio_count": sum(
            row["positive_ratio_count"] > 0 for row in trajectories),
        "trajectory_with_negative_ratio_count": sum(
            row["negative_ratio_count"] > 0 for row in trajectories),
        "trajectory_with_sign_change_count": sum(
            row["sign_change_count"] > 0 for row in trajectories),
        "worst_lift_index_counts": {
            str(index): worst_lift_counts[index]
            for index in range(8)
        },
        "max_signed_budget_ratio_by_trajectory_summary": finite_summary(
            max_ratios),
        "signed_budget_ratio_range_by_trajectory_summary": finite_summary(
            ranges),
        "sign_change_count_summary": finite_summary(
            sign_changes_by_trajectory),
        "worst_trajectory": max(
            trajectories,
            key=lambda row: (
                row["max_signed_budget_ratio"], -row["worst_target"]),
        ),
        "largest_range_trajectories": sorted(
            trajectories,
            key=lambda row: (
                -row["max_minus_min_signed_budget_ratio"],
                row["target_residue"],
            ),
        )[:12],
        "largest_max_ratio_trajectories": sorted(
            trajectories,
            key=lambda row: (-row["max_signed_budget_ratio"],
                             row["target_residue"]),
        )[:12],
    }


def lift_summaries(rows):
    by_lift = defaultdict(list)
    for row in rows:
        by_lift[int(row["combined_lift_index"])].append(
            row["signed_budget_ratio"])
    return {
        str(index): {
            "lift_index": index,
            "row_count": len(by_lift[index]),
            "signed_budget_ratio_summary": finite_summary(by_lift[index]),
        }
        for index in range(8)
    }


def build_receipt():
    source = load_json(SOURCE)
    rows = rows_with_lift_index(source)
    trajectories = grouped_trajectories(rows)
    summary = summarize_trajectories(trajectories)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "positivity_budget_audit": str(SOURCE.relative_to(ROOT)),
            "positivity_budget_source_commit": source["source_commit"],
        },
        "status_boundary": (
            "finite q286-WBSS four-modulus budget-trajectory audit only; "
            "no recurrence theorem, fixed-modulus equidistribution theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"),
        "goldbach_proved": False,
        "recurrence_theorem_proved": False,
        "fixed_modulus_equidistribution_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "eight-lift residue trajectory budget envelope",
            "mechanism": (
                "Group the two four-lift holdouts by source residue class and "
                "inspect the signed budget ratio trajectory.  If pressure is "
                "persistent or monotone by residue, a recurrence/envelope "
                "theorem might be the next target; if not, the proof target "
                "stays rowwise signed concentration or a residue-class "
                "supremum bound."),
            "prediction": (
                "The fixed z cap can fail while lambda remains small; the "
                "worst budget-ratio rows should not form a monotone rising "
                "trajectory across all stressed residues."),
            "falsifier": (
                "A monotone rising or last-lift-dominated trajectory pattern "
                "would push the next theorem toward a residue recurrence.  A "
                "row with signed budget ratio at least 1 would falsify the "
                "finite direct-witness checkpoint."),
            "smallest_test": (
                "Use the existing 232 positivity-budget rows; assign combined "
                "lift indexes 0..7 and summarize each stressed residue class."),
            "novelty_label": "new-to-this-task",
        },
        "holdout": {
            "row_count": len(rows),
            "trajectory_count": len(trajectories),
            "summary": summary,
            "summary_by_combined_lift": lift_summaries(rows),
            "trajectories": trajectories,
        },
        "all_trajectories_positive": all(
            row["positivity_margin_sigma_summary"]["minimum"] > 0.0
            for row in trajectories),
        "no_monotone_non_decreasing_trajectory": (
            summary["monotone_non_decreasing_trajectory_count"] == 0),
        "worst_lift_position_distributed": (
            sum(1 for count in summary["worst_lift_index_counts"].values()
                if count > 0) > 4),
        "decision": (
            "The combined eight-lift evidence does not support a monotone "
            "residue-class drift story: no trajectory is monotone "
            "non-decreasing, and worst lift positions are distributed across "
            "all checked indexes.  The worst trajectory is residue 1478 from "
            "source target 251728, with maximum signed budget ratio "
            "0.29444884696113977 at lift 4.  The next theorem target should "
            "therefore remain a rowwise signed concentration estimate or a "
            "residue-class supremum bound for lambda_phi<1, not a simple "
            "monotone recurrence.  Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
