"""Decompose source-start half-frame margins by reduced denominator.

The theorem-obligation audit reduced the target to the pointwise unnormalized
margin ``full/2 - active > 0``.  This receipt inspects the tightest prime block
at each checked source scale and asks whether that positive margin is
denominator-local, diffuse, or cancellation-dependent.
"""

from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    PAIRS,
    THRESHOLD,
    scale_parameters,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _residue_cells_by_denominator,
)


THEOREM_OBLIGATION = (
    Path("evidence")
    / "mobius-moment-square-degree5-prime-block-theorem-obligation-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-source-margin-denominator-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def label_rows_from_denominator(
        reduced_denominator, cells, row_count, active_row_start):
    rows_window = np.arange(
        active_row_start, active_row_start + row_count, dtype=np.int64)
    residues = np.asarray([cell[0] for cell in cells], dtype=np.int64)
    values = np.asarray([cell[1] for cell in cells], dtype=complex)
    full_gram = np.zeros((6, 6), dtype=float)
    for _, value in cells:
        full_gram += reduced_denominator * np.outer(
            value, np.conjugate(value)).real
    transforms = np.zeros((row_count, 6), dtype=complex)
    for first in range(0, len(residues), 8192):
        selected_residues = residues[first:first + 8192]
        phases = np.exp(
            2j * np.pi
            * ((rows_window[:, None] * selected_residues[None, :])
               % reduced_denominator)
            / reduced_denominator)
        transforms += phases @ values[first:first + 8192]
    active_gram = (
        reduced_denominator / row_count
        * (transforms.T @ np.conjugate(transforms)).real)
    rows = []
    component_rows = []
    for left, right, left_label, right_label in PAIRS:
        label = f"{left_label},{right_label}"
        active = float(2 * active_gram[left, right])
        full = float(2 * full_gram[left, right])
        half_frame = active - THRESHOLD * full
        margin = -half_frame
        row = {
            "reduced_denominator": reduced_denominator,
            "residue_cell_count": len(cells),
            "label": label,
            "active_contribution": active,
            "full_contribution": full,
            "half_frame_contribution": half_frame,
            "unnormalized_margin_full_over_2_minus_active": margin,
        }
        component_rows.append(row)
        rows.append(row)
    rows.append({
        "reduced_denominator": reduced_denominator,
        "residue_cell_count": len(cells),
        "label": "TOTAL",
        "active_contribution": sum(
            row["active_contribution"] for row in component_rows),
        "full_contribution": sum(
            row["full_contribution"] for row in component_rows),
        "half_frame_contribution": sum(
            row["half_frame_contribution"] for row in component_rows),
        "unnormalized_margin_full_over_2_minus_active": sum(
            row["unnormalized_margin_full_over_2_minus_active"]
            for row in component_rows),
    })
    return rows


def denominator_summary(rows, label):
    selected = [row for row in rows if row["label"] == label]
    total_margin = sum(
        row["unnormalized_margin_full_over_2_minus_active"]
        for row in selected)
    positive = [
        row for row in selected
        if row["unnormalized_margin_full_over_2_minus_active"] > 0]
    negative = [
        row for row in selected
        if row["unnormalized_margin_full_over_2_minus_active"] < 0]
    positive_sum = sum(
        row["unnormalized_margin_full_over_2_minus_active"]
        for row in positive)
    negative_sum = sum(
        row["unnormalized_margin_full_over_2_minus_active"]
        for row in negative)
    largest_positive = max(
        positive,
        key=lambda row: row["unnormalized_margin_full_over_2_minus_active"],
        default=None)
    largest_negative = min(
        negative,
        key=lambda row: row["unnormalized_margin_full_over_2_minus_active"],
        default=None)
    top_absolute = sorted(
        selected,
        key=lambda row: abs(
            row["unnormalized_margin_full_over_2_minus_active"]),
        reverse=True)[:6]
    return {
        "label": label,
        "reduced_denominator_count": len(selected),
        "total_unnormalized_margin": total_margin,
        "positive_denominator_count": len(positive),
        "negative_denominator_count": len(negative),
        "positive_margin_sum": positive_sum,
        "negative_margin_sum": negative_sum,
        "cancellation_ratio_abs_negative_over_positive": (
            abs(negative_sum) / positive_sum if positive_sum else None),
        "largest_positive_denominator": largest_positive,
        "largest_negative_denominator": largest_negative,
        "top_absolute_denominator_rows": top_absolute,
    }


def scale_margin_summary(obligation_row):
    scale = obligation_row["scale_modulus"]
    prime = obligation_row["top_prime_block"]["prime_modulus"]
    print(f"decomposing M={scale}, p={prime}", flush=True)
    parameters = scale_parameters(scale)
    _, cells_by_denominator = _residue_cells_by_denominator(
        prime,
        parameters["row_count"],
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    active_row_start = parameters["row_count"]
    denominator_rows = []
    for reduced_denominator, cells in sorted(cells_by_denominator.items()):
        denominator_rows.extend(label_rows_from_denominator(
            reduced_denominator, cells,
            parameters["row_count"],
            active_row_start))
    labels = ["00,12", "01,02", "01,11", "TOTAL"]
    label_summaries = {
        label: denominator_summary(denominator_rows, label)
        for label in labels
    }
    weakest_label = obligation_row["top_prime_block"]["weakest_label"]
    weakest_summary = label_summaries[weakest_label]
    return {
        "scale_modulus": scale,
        "prime_modulus": prime,
        "row_count": parameters["row_count"],
        "ell_freeze": parameters["ell_freeze"],
        "divisor_range": list(parameters["divisor_range"]),
        "active_row_start": active_row_start,
        "reduced_denominator_count": len(cells_by_denominator),
        "reduced_denominators": sorted(cells_by_denominator),
        "weakest_label": weakest_label,
        "label_summaries": label_summaries,
        "weakest_label_denominator_summary": weakest_summary,
        "top_prime_block": obligation_row["top_prime_block"],
    }


def build_receipt():
    obligation = json.loads(THEOREM_OBLIGATION.read_text(encoding="utf-8"))
    source_rows = obligation["scale_obligation_records"]
    scale_summaries = []
    with ProcessPoolExecutor(max_workers=min(3, len(source_rows))) as executor:
        futures = {
            executor.submit(scale_margin_summary, row): row["scale_modulus"]
            for row in source_rows
        }
        for future in as_completed(futures):
            scale_summaries.append(future.result())
    scale_summaries.sort(key=lambda row: row["scale_modulus"])
    cancellation_ratios = [
        row["weakest_label_denominator_summary"][
            "cancellation_ratio_abs_negative_over_positive"]
        for row in scale_summaries
    ]
    reduced_counts = [
        row["reduced_denominator_count"] for row in scale_summaries]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_degree5_source_margin_denominator_decomposition",
        "source_theorem_obligation_audit": str(THEOREM_OBLIGATION),
        "question": (
            "For the tightest checked source-start prime blocks, is the "
            "positive unnormalized margin full/2-active denominator-local, "
            "diffuse, or cancellation-dependent?"),
        "scale_summaries": scale_summaries,
        "scale_count": len(scale_summaries),
        "minimum_reduced_denominator_count": min(reduced_counts),
        "maximum_reduced_denominator_count": max(reduced_counts),
        "maximum_weakest_label_cancellation_ratio": max(
            ratio for ratio in cancellation_ratios if ratio is not None),
        "minimum_weakest_label_cancellation_ratio": min(
            ratio for ratio in cancellation_ratios if ratio is not None),
        "denominator_mechanism_observation": (
            "The checked margins are not a one-denominator certificate.  They "
            "must be controlled as a signed reduced-denominator ledger for "
            "each prime block."),
        "candidate_next_theorem_subtarget": {
            "name": "signed reduced-denominator margin ledger",
            "mechanism": (
                "Prove a positive lower bound for the sum of denominator "
                "margins full_q/2-active_q after grouping the reduced "
                "denominators into stable families, rather than requiring "
                "each individual denominator to be positive."),
            "prediction": (
                "Future tight source-start blocks should have positive total "
                "margin even when individual reduced denominators are adverse."),
            "falsifier": (
                "A tight source-start block whose total margin is positive "
                "only through a single unstable denominator, or whose source "
                "margin becomes negative after grouping into the proposed "
                "families, falsifies this subtarget."),
            "novelty_label": "new-to-this-task",
        },
        "finite_denominator_decomposition_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_start_theorem_proved": False,
        "prime_block_theorem_proved": False,
        "denominator_margin_theorem_proved": False,
        "source_window_theorem_proved": False,
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
