"""Build the degree-5 puncture denominator-cause audit."""

import json
import sys
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


OUTPUT = Path(
    "evidence/"
    "mobius-moment-square-degree5-puncture-denominator-cause-audit.json")
PUNCTURE_AUDIT = Path(
    "evidence/mobius-moment-square-degree5-translated-puncture-audit.json")


def pair_indices(label):
    for left, right, left_label, right_label in PAIRS:
        if label == f"{left_label},{right_label}":
            return left, right
    raise ValueError(f"unknown pair label: {label}")


def full_component_contribution(reduced_denominator, cells, left, right):
    gram = np.zeros((6, 6), dtype=float)
    for _, value in cells:
        gram += reduced_denominator * np.outer(
            value, np.conjugate(value)).real
    return float(2 * gram[left, right])


def active_component_contribution(
        reduced_denominator, cells, row_count, active_row_start, left, right):
    rows = np.arange(
        active_row_start, active_row_start + row_count, dtype=np.int64)
    residues = np.asarray([cell[0] for cell in cells], dtype=np.int64)
    values = np.asarray([cell[1] for cell in cells], dtype=complex)
    transforms = np.zeros((row_count, 6), dtype=complex)
    for first in range(0, len(residues), 8192):
        selected_residues = residues[first:first + 8192]
        phases = np.exp(
            2j * np.pi
            * ((rows[:, None] * selected_residues[None, :])
               % reduced_denominator)
            / reduced_denominator)
        transforms += phases @ values[first:first + 8192]
    gram = (
        reduced_denominator / row_count
        * (transforms.T @ np.conjugate(transforms)).real)
    return float(2 * gram[left, right])


def denominator_rows_for_start(
        cells_by_denominator, row_count, active_row_start, left, right):
    rows = []
    for reduced_denominator, cells in sorted(cells_by_denominator.items()):
        active = active_component_contribution(
            reduced_denominator,
            cells,
            row_count,
            active_row_start,
            left,
            right,
        )
        full = full_component_contribution(
            reduced_denominator, cells, left, right)
        half_frame = active - THRESHOLD * full
        rows.append({
            "reduced_denominator": reduced_denominator,
            "residue_cell_count": len(cells),
            "active_row_start": active_row_start,
            "active_contribution": active,
            "full_contribution": full,
            "active_over_full_ratio": active / full if full else None,
            "half_frame_contribution": half_frame,
        })
    return rows


def transition_rows(start_rows, comparison_rows):
    by_denominator = {
        row["reduced_denominator"]: row for row in start_rows
    }
    comparison_by_denominator = {
        row["reduced_denominator"]: row for row in comparison_rows
    }
    transitions = []
    for reduced_denominator in sorted(by_denominator):
        row = by_denominator[reduced_denominator]
        comparison = comparison_by_denominator[reduced_denominator]
        transitions.append({
            "reduced_denominator": reduced_denominator,
            "residue_cell_count": row["residue_cell_count"],
            "half_frame_at_failure": row["half_frame_contribution"],
            "half_frame_at_comparison": comparison["half_frame_contribution"],
            "failure_minus_comparison_half_frame": (
                row["half_frame_contribution"]
                - comparison["half_frame_contribution"]),
            "active_at_failure": row["active_contribution"],
            "active_at_comparison": comparison["active_contribution"],
            "failure_minus_comparison_active": (
                row["active_contribution"]
                - comparison["active_contribution"]),
        })
    total_delta = sum(
        row["failure_minus_comparison_half_frame"] for row in transitions)
    for row in transitions:
        row["signed_share_of_total_delta"] = (
            row["failure_minus_comparison_half_frame"] / total_delta
            if total_delta else None)
    return sorted(
        transitions,
        key=lambda row: abs(row["failure_minus_comparison_half_frame"]),
        reverse=True,
    )


def puncture_denominator_summary(puncture):
    scale_modulus = puncture["scale_modulus"]
    prime_modulus = puncture["prime_modulus"]
    label = puncture["label"]
    left, right = pair_indices(label)
    parameters = scale_parameters(scale_modulus)
    full, cells_by_denominator = _residue_cells_by_denominator(
        prime_modulus,
        parameters["row_count"],
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    starts = sorted({
        puncture["failure_start"],
        puncture["failure_start"] - 1,
        puncture["failure_start"] + 1,
        puncture["source_active_row_start"],
    })
    starts = [start for start in starts if start >= 0]
    denominator_rows_by_start = {
        str(start): denominator_rows_for_start(
            cells_by_denominator,
            parameters["row_count"],
            start,
            left,
            right,
        )
        for start in starts
    }
    totals_by_start = {}
    for start, rows in denominator_rows_by_start.items():
        active = sum(row["active_contribution"] for row in rows)
        full_contribution = sum(row["full_contribution"] for row in rows)
        half_frame = sum(row["half_frame_contribution"] for row in rows)
        totals_by_start[start] = {
            "active_contribution": active,
            "full_contribution": full_contribution,
            "active_over_full_ratio": (
                active / full_contribution if full_contribution else None),
            "half_frame_contribution": half_frame,
            "dominates_one_half_signed_full": (
                full_contribution < 0
                and full_contribution
                and active / full_contribution > THRESHOLD),
        }
    failure_start = str(puncture["failure_start"])
    left_start = str(puncture["failure_start"] - 1)
    right_start = str(puncture["failure_start"] + 1)
    source_start = str(puncture["source_active_row_start"])
    left_transition = transition_rows(
        denominator_rows_by_start[failure_start],
        denominator_rows_by_start[left_start],
    )
    right_transition = transition_rows(
        denominator_rows_by_start[failure_start],
        denominator_rows_by_start[right_start],
    )
    source_transition = transition_rows(
        denominator_rows_by_start[failure_start],
        denominator_rows_by_start[source_start],
    )
    return {
        "scale_modulus": scale_modulus,
        "prime_modulus": prime_modulus,
        "label": label,
        "row_count": parameters["row_count"],
        "ell_freeze": parameters["ell_freeze"],
        "divisor_range": parameters["divisor_range"],
        "failure_start": puncture["failure_start"],
        "left_neighbor_start": puncture["failure_start"] - 1,
        "right_neighbor_start": puncture["failure_start"] + 1,
        "source_active_row_start": puncture["source_active_row_start"],
        "reduced_denominator_count": len(cells_by_denominator),
        "reduced_denominators": sorted(cells_by_denominator),
        "denominator_rows_by_start": denominator_rows_by_start,
        "totals_by_start": totals_by_start,
        "left_neighbor_transition": left_transition,
        "right_neighbor_transition": right_transition,
        "source_start_transition": source_transition,
        "dominant_left_neighbor_worsening_denominator": (
            left_transition[0]["reduced_denominator"]),
        "dominant_right_neighbor_worsening_denominator": (
            right_transition[0]["reduced_denominator"]),
        "dominant_source_gap_denominator": (
            source_transition[0]["reduced_denominator"]),
        "left_neighbor_transition_total_delta": sum(
            row["failure_minus_comparison_half_frame"]
            for row in left_transition),
        "right_neighbor_transition_total_delta": sum(
            row["failure_minus_comparison_half_frame"]
            for row in right_transition),
        "source_start_transition_total_delta": sum(
            row["failure_minus_comparison_half_frame"]
            for row in source_transition),
    }


def build_receipt():
    puncture_receipt = json.loads(PUNCTURE_AUDIT.read_text(encoding="utf-8"))
    summaries = [
        puncture_denominator_summary(puncture)
        for puncture in puncture_receipt["puncture_summaries"]
    ]
    summary = summaries[0]
    return {
        "status": "AUDIT_degree5_puncture_denominator_cause",
        "question": (
            "Can the isolated translated puncture be localized to reduced "
            "denominator contributions, or is it diffuse across the active "
            "window Gram?"),
        "source_puncture_audit": str(PUNCTURE_AUDIT),
        "puncture_summaries": summaries,
        "puncture_count": len(summaries),
        "answer": (
            "The puncture is denominator-local enough to change the next "
            "target.  For M=149, p=163, component (00,12), only four reduced "
            "denominators contribute: 6006, 10010, 15015, and 30030.  The "
            "failure relative to left neighbor start 0 is dominated by "
            "reduced denominator 30030; the failure relative to right neighbor "
            "start 2 is dominated by 10010 and 6006, partly offset by 30030."),
        "decision": (
            "A future arithmetic source-admissibility theorem should inspect "
            "reduced-denominator phase structure, not only row-start distance. "
            "The finite cause is not a single universal denominator obstruction: "
            "left and right neighbor comparisons localize to different dominant "
            "denominators.  This keeps the source-window lane alive as a "
            "denominator-phase theorem target, while blocking a simple "
            "distance-only or one-denominator explanation."),
        "candidate": {
            "name": "denominator-phase source admissibility",
            "mechanism": (
                "Passing source windows may be governed by phase alignment "
                "among a small reduced-denominator family rather than by "
                "monotone distance from the source start."),
            "prediction": (
                "Future translated punctures, if found, should localize to a "
                "small reduced-denominator transition ledger, and source starts "
                "should avoid the adverse phase combination."),
            "falsifier": (
                "A new puncture whose failure margin is diffuse across many "
                "reduced denominators, or whose source start shares the same "
                "adverse denominator-phase profile, would falsify this finite "
                "mechanism."),
            "novelty_label": "new-to-this-task",
        },
        "left_neighbor_dominant_denominator": (
            summary["dominant_left_neighbor_worsening_denominator"]),
        "right_neighbor_dominant_denominator": (
            summary["dominant_right_neighbor_worsening_denominator"]),
        "source_gap_dominant_denominator": (
            summary["dominant_source_gap_denominator"]),
        "finite_denominator_cause_audit_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_window_implication_theorem_proved": False,
        "source_admissible_window_theorem_proved": False,
        "denominator_phase_theorem_proved": False,
        "phase_curve_theorem_proved": False,
        "pointwise_universal_adverse_drag_estimate_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
    }


def main():
    receipt = build_receipt()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
