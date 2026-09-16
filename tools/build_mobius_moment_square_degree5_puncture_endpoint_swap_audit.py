"""Build the degree-5 puncture endpoint-swap audit."""

import json
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
from tools.build_mobius_moment_square_degree5_puncture_denominator_cause_audit import (  # noqa: E402
    OUTPUT as DENOMINATOR_CAUSE,
    pair_indices,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _residue_cells_by_denominator,
)


OUTPUT = Path(
    "evidence/"
    "mobius-moment-square-degree5-puncture-endpoint-swap-audit.json")


def single_row_component_contribution(
        reduced_denominator, cells, row_index, row_count, left, right):
    residues = np.asarray([cell[0] for cell in cells], dtype=np.int64)
    values = np.asarray([cell[1] for cell in cells], dtype=complex)
    phases = np.exp(
        2j * np.pi
        * ((row_index * residues) % reduced_denominator)
        / reduced_denominator)
    transform = phases @ values
    return float(
        2
        * (reduced_denominator / row_count)
        * (transform[left] * np.conjugate(transform[right])).real)


def swap_rows(cells_by_denominator, row_count, left, right, outgoing, incoming):
    rows = []
    for reduced_denominator, cells in sorted(cells_by_denominator.items()):
        outgoing_contribution = single_row_component_contribution(
            reduced_denominator, cells, outgoing, row_count, left, right)
        incoming_contribution = single_row_component_contribution(
            reduced_denominator, cells, incoming, row_count, left, right)
        delta = incoming_contribution - outgoing_contribution
        rows.append({
            "reduced_denominator": reduced_denominator,
            "residue_cell_count": len(cells),
            "outgoing_row": outgoing,
            "incoming_row": incoming,
            "outgoing_row_contribution": outgoing_contribution,
            "incoming_row_contribution": incoming_contribution,
            "incoming_minus_outgoing": delta,
        })
    total_delta = sum(row["incoming_minus_outgoing"] for row in rows)
    for row in rows:
        row["signed_share_of_total_delta"] = (
            row["incoming_minus_outgoing"] / total_delta
            if total_delta else None)
    return sorted(
        rows,
        key=lambda row: abs(row["incoming_minus_outgoing"]),
        reverse=True)


def endpoint_swap_summary(puncture):
    scale_modulus = puncture["scale_modulus"]
    prime_modulus = puncture["prime_modulus"]
    label = puncture["label"]
    left, right = pair_indices(label)
    parameters = scale_parameters(scale_modulus)
    row_count = parameters["row_count"]
    _, cells_by_denominator = _residue_cells_by_denominator(
        prime_modulus,
        row_count,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    failure_start = puncture["failure_start"]
    left_neighbor_start = puncture["left_neighbor_start"]
    right_neighbor_start = puncture["right_neighbor_start"]
    source_start = puncture["source_active_row_start"]
    left_swap = swap_rows(
        cells_by_denominator,
        row_count,
        left,
        right,
        outgoing=left_neighbor_start,
        incoming=left_neighbor_start + row_count,
    )
    right_swap = swap_rows(
        cells_by_denominator,
        row_count,
        left,
        right,
        outgoing=right_neighbor_start + row_count - 1,
        incoming=failure_start,
    )
    source_gap = swap_rows(
        cells_by_denominator,
        row_count,
        left,
        right,
        outgoing=source_start,
        incoming=failure_start,
    )
    return {
        "scale_modulus": scale_modulus,
        "prime_modulus": prime_modulus,
        "label": label,
        "row_count": row_count,
        "failure_start": failure_start,
        "left_neighbor_start": left_neighbor_start,
        "right_neighbor_start": right_neighbor_start,
        "source_active_row_start": source_start,
        "left_neighbor_to_failure_swap": {
            "window_delta": "start1 - start0",
            "outgoing_row": left_neighbor_start,
            "incoming_row": left_neighbor_start + row_count,
            "denominator_rows": left_swap,
            "total_delta": sum(row["incoming_minus_outgoing"]
                               for row in left_swap),
            "dominant_denominator": left_swap[0]["reduced_denominator"],
        },
        "right_neighbor_to_failure_swap": {
            "window_delta": "start1 - start2",
            "outgoing_row": right_neighbor_start + row_count - 1,
            "incoming_row": failure_start,
            "denominator_rows": right_swap,
            "total_delta": sum(row["incoming_minus_outgoing"]
                               for row in right_swap),
            "dominant_denominator": right_swap[0]["reduced_denominator"],
        },
        "source_to_failure_endpoint_probe": {
            "not_a_window_swap": True,
            "outgoing_row": source_start,
            "incoming_row": failure_start,
            "denominator_rows": source_gap,
            "total_delta": sum(row["incoming_minus_outgoing"]
                               for row in source_gap),
            "dominant_denominator": source_gap[0]["reduced_denominator"],
        },
    }


def build_receipt():
    denominator_receipt = json.loads(
        DENOMINATOR_CAUSE.read_text(encoding="utf-8"))
    summaries = [
        endpoint_swap_summary(puncture)
        for puncture in denominator_receipt["puncture_summaries"]
    ]
    summary = summaries[0]
    return {
        "status": "AUDIT_degree5_puncture_endpoint_swap",
        "question": (
            "Is the isolated translated puncture explained by the single-row "
            "endpoint swaps between adjacent active windows?"),
        "source_denominator_cause_audit": str(DENOMINATOR_CAUSE),
        "puncture_summaries": summaries,
        "puncture_count": len(summaries),
        "answer": (
            "Yes, for the adjacent comparisons.  Start 1 minus start 0 is the "
            "incoming row 32 minus outgoing row 0; that swap is dominated by "
            "q=30030.  Start 1 minus start 2 is incoming row 1 minus outgoing "
            "row 33; that swap is dominated by q=10010 and q=6006, with "
            "q=30030 partly offsetting the failure."),
        "decision": (
            "The next source-admissibility target can be sharpened from a whole "
            "window phase statement to an endpoint-swap/denominator-phase "
            "statement for adjacent translated windows.  This blocks a purely "
            "bulk-window explanation.  It remains finite: no endpoint-swap "
            "theorem or source-window implication theorem is proved."),
        "candidate": {
            "name": "endpoint-swap denominator-phase admissibility",
            "mechanism": (
                "Adjacent translated window failures may be governed by a "
                "small number of incoming/outgoing row phase swaps inside the "
                "reduced-denominator ledger."),
            "prediction": (
                "Any future singleton translated puncture should have adjacent "
                "failure deltas equal to explicit endpoint swaps and should "
                "localize to a small denominator set."),
            "falsifier": (
                "A future adjacent puncture whose failure delta cannot be "
                "accounted for by the endpoint swap, or whose endpoint swap is "
                "diffuse across many denominators, falsifies this mechanism."),
            "novelty_label": "new-to-this-task",
        },
        "left_neighbor_swap_dominant_denominator": (
            summary["left_neighbor_to_failure_swap"][
                "dominant_denominator"]),
        "right_neighbor_swap_dominant_denominator": (
            summary["right_neighbor_to_failure_swap"][
                "dominant_denominator"]),
        "finite_endpoint_swap_audit_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "endpoint_swap_theorem_proved": False,
        "denominator_phase_theorem_proved": False,
        "source_window_implication_theorem_proved": False,
        "source_admissible_window_theorem_proved": False,
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
