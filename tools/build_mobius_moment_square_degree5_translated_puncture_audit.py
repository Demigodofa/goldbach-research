"""Build the degree-5 translated puncture audit.

This audit keeps the source-window lane honest after the broad translated
phase-curve falsifier.  It checks whether the lone translated failure behaves
like a monotone edge-distance effect or like an isolated puncture.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_checked_scale_phase_curve_sweep import (  # noqa: E402
    _active_gram,
    _dominance_rows_for_start,
    _residue_cells_by_denominator,
    active_row_start_sweep,
)
from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    scale_parameters,
    sign_counts,
)
from tools.build_mobius_moment_square_degree5_source_admissible_window_audit import (  # noqa: E402
    contiguous_intervals,
)


SOURCE_ADMISSIBLE = Path(
    "evidence/mobius-moment-square-degree5-source-admissible-window-audit.json")
PHASE_SWEEP = Path(
    "evidence/mobius-moment-square-degree5-checked-scale-phase-curve-sweep.json")
OUTPUT = Path(
    "evidence/mobius-moment-square-degree5-translated-puncture-audit.json")


def rows_for_failure(scale_modulus, prime_modulus, label):
    parameters = scale_parameters(scale_modulus)
    divisor_lower, divisor_upper = parameters["divisor_range"]
    full, cells_by_denominator = _residue_cells_by_denominator(
        prime_modulus,
        parameters["row_count"],
        parameters["ell_freeze"],
        divisor_lower,
        divisor_upper,
    )
    rows = []
    for active_row_start in active_row_start_sweep(scale_modulus):
        active = _active_gram(
            cells_by_denominator, parameters["row_count"], active_row_start)
        start_rows = _dominance_rows_for_start(
            scale_modulus,
            prime_modulus,
            active_row_start,
            parameters["row_count"],
            active,
            full,
        )
        rows.extend(row for row in start_rows if row["label"] == label)
    return rows


def row_by_start(rows):
    return {row["active_row_start"]: row for row in rows}


def puncture_summary(failure_row):
    scale_modulus = failure_row["scale_modulus"]
    prime_modulus = failure_row["prime_modulus"]
    label = failure_row["label"]
    parameters = scale_parameters(scale_modulus)
    source_start = parameters["row_count"]
    rows = rows_for_failure(scale_modulus, prime_modulus, label)
    by_start = row_by_start(rows)
    failing_starts = [
        row["active_row_start"]
        for row in rows
        if not row["dominates_one_half_signed_full"]
    ]
    passing_starts = [
        row["active_row_start"]
        for row in rows
        if row["dominates_one_half_signed_full"]
    ]
    source_connected_interval = None
    for interval in contiguous_intervals(passing_starts):
        if interval["start"] <= source_start <= interval["stop"]:
            source_connected_interval = interval
            break
    failure_start = failure_row["active_row_start"]
    neighbor_starts = sorted({
        start for start in [failure_start - 1, failure_start + 1]
        if start in by_start
    })
    neighbor_rows = [by_start[start] for start in neighbor_starts]
    pass_intervals = contiguous_intervals(passing_starts)
    slacks = [row["dominance_slack_above_one_half"] for row in rows]
    return {
        "scale_modulus": scale_modulus,
        "prime_modulus": prime_modulus,
        "label": label,
        "row_count": parameters["row_count"],
        "source_active_row_start": source_start,
        "active_row_start_range": [
            min(by_start),
            max(by_start),
        ],
        "failure_start": failure_start,
        "failure_start_offset": failure_row["active_row_start_offset"],
        "failing_active_row_starts": failing_starts,
        "failing_start_count": len(failing_starts),
        "passing_active_row_start_intervals": pass_intervals,
        "source_connected_passing_interval": source_connected_interval,
        "source_start_row": by_start[source_start],
        "failure_row": by_start[failure_start],
        "neighbor_rows": neighbor_rows,
        "left_far_edge_row": by_start[min(by_start)],
        "minimum_slack": min(slacks),
        "maximum_slack": max(slacks),
        "slack_sign_counts": sign_counts(slacks),
        "is_singleton_puncture": len(failing_starts) == 1,
        "puncture_is_not_left_edge": failure_start != min(by_start),
        "left_far_edge_passes": by_start[min(by_start)][
            "dominates_one_half_signed_full"],
        "right_neighbor_passes": by_start.get(failure_start + 1, {}).get(
            "dominates_one_half_signed_full"),
        "source_start_passes": by_start[source_start][
            "dominates_one_half_signed_full"],
        "source_start_slack": by_start[source_start][
            "dominance_slack_above_one_half"],
        "source_start_ratio": by_start[source_start]["active_over_full_ratio"],
        "distance_to_source_at_failure": abs(source_start - failure_start),
        "distance_to_source_at_left_far_edge": abs(source_start - min(by_start)),
        "nonconvex_pass_set_detected": (
            len(failing_starts) == 1
            and failure_start != min(by_start)
            and by_start[min(by_start)]["dominates_one_half_signed_full"]
            and by_start[failure_start + 1][
                "dominates_one_half_signed_full"]
        ),
    }


def build_receipt():
    source_receipt = json.loads(SOURCE_ADMISSIBLE.read_text(encoding="utf-8"))
    phase_receipt = json.loads(PHASE_SWEEP.read_text(encoding="utf-8"))
    punctures = [
        puncture_summary(row)
        for row in source_receipt["broad_failure_rows"]
    ]
    nonconvex = [
        row for row in punctures if row["nonconvex_pass_set_detected"]
    ]
    return {
        "status": "AUDIT_degree5_translated_puncture",
        "question": (
            "Does the lone broad translated-window failure behave like a "
            "monotone distance-from-source edge effect, or like an isolated "
            "puncture in an otherwise passing translated row-start profile?"),
        "source_admissible_audit": str(SOURCE_ADMISSIBLE),
        "phase_curve_sweep": str(PHASE_SWEEP),
        "source_admissible_status": source_receipt["status"],
        "phase_curve_status": phase_receipt["status"],
        "puncture_summaries": punctures,
        "puncture_count": len(punctures),
        "nonconvex_puncture_count": len(nonconvex),
        "single_failure_nonconvex_puncture_detected": len(nonconvex) == len(
            punctures) and bool(punctures),
        "answer": (
            "The finite failure is an isolated translated puncture.  For the "
            "failing profile M=149, p=163, component (00,12), start 0 passes, "
            "start 1 fails, and starts 2..64 pass.  The source start 32 is "
            "deep inside the source-connected passing interval 2..64."),
        "prediction": (
            "If the source-window route is real, admissibility should be tied "
            "to the actual source construction or another arithmetic exclusion, "
            "not to a naive monotone distance-from-source interval model."),
        "falsifier": (
            "A future broad translated failure whose source-connected pass "
            "interval disappears, whose canonical source start fails, or whose "
            "failure forms a persistent boundary band rather than a puncture "
            "would falsify this finite puncture interpretation."),
        "decision": (
            "Keep the source-window/admissible-window route alive, but do not "
            "model the translated pass set as a simple centered interval around "
            "the source.  The next theorem-shaped target needs an arithmetic "
            "source-admissibility condition or an implication theorem, not a "
            "distance-only translated-window rule."),
        "finite_translated_puncture_audit_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_window_implication_theorem_proved": False,
        "source_admissible_window_theorem_proved": False,
        "phase_curve_theorem_proved": False,
        "active_window_translation_theorem_proved": False,
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
