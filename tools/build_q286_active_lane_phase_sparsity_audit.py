"""Audit whether q286 source-summary failures show a phase transition.

The source-summary coupled-slack audit found 143 nonpositive rows under the
frozen selected-late constants.  This derived audit asks whether those failures
support a meaningful phase/scale theorem target or merely reflect sparse later
source summaries.

Finite diagnostic only.  It proves no phase theorem, active-lane theorem,
pointwise adverse-drag theorem, q286 threshold theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import math
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE = EVIDENCE / "q286-active-lane-source-summary-coupled-slack-audit.json"
OUT = EVIDENCE / "q286-active-lane-phase-sparsity-audit.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def finite_summary(values):
    vals = [float(value) for value in values]
    if not vals:
        return {"count": 0, "minimum": None, "mean": None, "maximum": None}
    return {
        "count": len(vals),
        "minimum": min(vals),
        "mean": math.fsum(vals) / len(vals),
        "maximum": max(vals),
    }


def correlation(left, right):
    xs = [float(value) for value in left]
    ys = [float(value) for value in right]
    if len(xs) != len(ys) or len(xs) < 2:
        return None
    x_mean = math.fsum(xs) / len(xs)
    y_mean = math.fsum(ys) / len(ys)
    x_var = math.fsum((value - x_mean) ** 2 for value in xs)
    y_var = math.fsum((value - y_mean) ** 2 for value in ys)
    if x_var == 0.0 or y_var == 0.0:
        return None
    return math.fsum(
        (x - x_mean) * (y - y_mean) for x, y in zip(xs, ys)
    ) / math.sqrt(x_var * y_var)


def block_summary(rows):
    by_block = defaultdict(list)
    for row in rows:
        by_block[row["block_index_after_discovery"]].append(row)
    result = []
    for block in sorted(by_block):
        block_rows = by_block[block]
        failing = [
            row for row in block_rows
            if not row["strict_closure_margin_positive"]]
        result.append({
            "block_index_after_discovery": block,
            "row_count": len(block_rows),
            "positive_count": len(block_rows) - len(failing),
            "nonpositive_count": len(failing),
            "minimum_target": min(row["target"] for row in block_rows),
            "maximum_target": max(row["target"] for row in block_rows),
            "maximum_failing_target": (
                max((row["target"] for row in failing), default=None)),
            "minimum_strict_margin": min(
                row["strict_closure_margin_to_calibrated_endpoint"]
                for row in block_rows),
            "maximum_strict_margin": max(
                row["strict_closure_margin_to_calibrated_endpoint"]
                for row in block_rows),
        })
    return result


def residue_summary(rows):
    by_residue = defaultdict(list)
    for row in rows:
        by_residue[row["target_mod_286"]].append(row)
    classes = []
    for residue in sorted(by_residue):
        residue_rows = by_residue[residue]
        positive = sum(row["strict_closure_margin_positive"]
                       for row in residue_rows)
        classes.append({
            "target_mod_286": residue,
            "row_count": len(residue_rows),
            "positive_count": positive,
            "nonpositive_count": len(residue_rows) - positive,
            "mixed_sign": 0 < positive < len(residue_rows),
        })
    return {
        "residue_class_count": len(classes),
        "pure_positive_class_count": sum(
            row["positive_count"] == row["row_count"] for row in classes),
        "pure_nonpositive_class_count": sum(
            row["positive_count"] == 0 for row in classes),
        "mixed_sign_class_count": sum(row["mixed_sign"] for row in classes),
        "classes": classes,
    }


def sign_change_targets(rows):
    if not rows:
        return []
    changes = []
    previous = rows[0]["strict_closure_margin_positive"]
    for row in rows[1:]:
        current = row["strict_closure_margin_positive"]
        if current != previous:
            changes.append(row["target"])
        previous = current
    return changes


def build_receipt():
    source = load_json(SOURCE)
    rows = sorted(source["rows"], key=lambda row: row["target"])
    positive_rows = [
        row for row in rows if row["strict_closure_margin_positive"]]
    failing_rows = [
        row for row in rows if not row["strict_closure_margin_positive"]]
    largest_failure = max(failing_rows, key=lambda row: row["target"])
    first_positive = min(positive_rows, key=lambda row: row["target"])
    suffix_rows = [
        row for row in rows if row["target"] > largest_failure["target"]]
    changes = sign_change_targets(rows)
    block_rows = block_summary(rows)
    residue = residue_summary(rows)
    log_targets = [math.log(row["target"]) for row in rows]

    return {
        "schema_version": 1,
        "receipt": "q286-active-lane-phase-sparsity-audit",
        "generated_from_commit": source_commit(),
        "sources": {
            "source_summary_coupled_slack": str(SOURCE.relative_to(ROOT)),
            "source_summary_coupled_slack_commit": source[
                "generated_from_commit"],
        },
        "row_count": len(rows),
        "positive_count": len(positive_rows),
        "nonpositive_count": len(failing_rows),
        "target_range": {
            "minimum": min(row["target"] for row in rows),
            "maximum": max(row["target"] for row in rows),
        },
        "positive_target_range": {
            "minimum": first_positive["target"],
            "maximum": max(row["target"] for row in positive_rows),
        },
        "nonpositive_target_range": {
            "minimum": min(row["target"] for row in failing_rows),
            "maximum": largest_failure["target"],
        },
        "largest_failing_target_row": largest_failure,
        "first_positive_target_row": first_positive,
        "pass_only_suffix_after_largest_failure": {
            "threshold_target_exclusive": largest_failure["target"],
            "first_suffix_target": (
                suffix_rows[0]["target"] if suffix_rows else None),
            "suffix_row_count": len(suffix_rows),
            "suffix_all_positive": all(
                row["strict_closure_margin_positive"]
                for row in suffix_rows),
            "suffix_targets": [row["target"] for row in suffix_rows],
        },
        "sign_change_count_in_target_order": len(changes),
        "sign_change_targets_in_target_order": changes,
        "block_summary": block_rows,
        "all_blocks_8_and_later_positive": all(
            row["nonpositive_count"] == 0
            for row in block_rows
            if row["block_index_after_discovery"] >= 8),
        "block_8_and_later_row_count": sum(
            row["row_count"] for row in block_rows
            if row["block_index_after_discovery"] >= 8),
        "block_7_is_mixed": next(
            row for row in block_rows
            if row["block_index_after_discovery"] == 7)[
                "positive_count"] > 0
            and next(
                row for row in block_rows
                if row["block_index_after_discovery"] == 7)[
                    "nonpositive_count"] > 0,
        "residue_mod_286_summary": residue,
        "correlations": {
            "log_target_vs_strict_margin": correlation(
                log_targets,
                (row["strict_closure_margin_to_calibrated_endpoint"]
                 for row in rows)),
            "log_target_vs_driver_margin": correlation(
                log_targets,
                (row["driver_margin_to_calibrated_floor"]
                 for row in rows)),
            "log_target_vs_channel_contribution": correlation(
                log_targets,
                (row["channel_margin_contribution_to_strict_closure"]
                 for row in rows)),
            "log_target_vs_full_action": correlation(
                log_targets,
                (row["full_action_to_principal_ratio"] for row in rows)),
            "log_target_vs_payment_ratio_on_negative_driver_rows": correlation(
                (math.log(row["target"]) for row in rows
                 if row["channel_payment_ratio_to_driver_deficit"] is not None),
                (row["channel_payment_ratio_to_driver_deficit"]
                 for row in rows
                 if row["channel_payment_ratio_to_driver_deficit"] is not None)),
        },
        "strict_margin_summary": finite_summary(
            row["strict_closure_margin_to_calibrated_endpoint"]
            for row in rows),
        "candidate": {
            "name": "finite source-summary phase/sparsity separator",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Separate the broadened coupled-slack failures by target "
                "order, block, and residue class to see whether they support "
                "a phase/scale theorem target."),
            "prediction": (
                "A genuine phase candidate should show failures confined "
                "below a finite scale with enough later active rows to make "
                "the boundary informative, and not merely a sparse suffix."),
            "falsifier": (
                "Many sign changes before the suffix, mixed residue classes, "
                "or very few later active rows would demote the phase story "
                "to a finite sparsity observation."),
            "smallest_test": (
                "Read the source-summary coupled-slack receipt; compute the "
                "largest failing target, pass-only suffix size, sign changes, "
                "block counts, residue mixing, and log-target correlations."),
        },
        "decision": (
            "The finite source-summary fixture has a pass-only suffix after "
            "target 647392, but this is not strong enough to promote a phase "
            "theorem.  There are 77 sign changes before the suffix, block 7 "
            "is mixed, and the pass-only suffix has only 11 rows.  Treat this "
            "as a phase/sparsity HOLD: useful as a next stress target, not as "
            "evidence that all sufficiently large active rows pass."),
        "status_boundary": (
            "Finite phase/sparsity diagnostic only.  It proves no phase "
            "transition theorem, active-lane theorem, pointwise adverse-drag "
            "theorem, q286 threshold theorem, strict-central Goldbach theorem, "
            "or Goldbach proof."),
        "goldbach_proved": False,
        "phase_transition_theorem_proved": False,
        "active_lane_theorem_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
