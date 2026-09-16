"""Build the degree-5 source-admissible row-window audit."""

import json
from pathlib import Path


BROAD_SWEEP = Path(
    "evidence/mobius-moment-square-degree5-checked-scale-phase-curve-sweep.json")
CANONICAL_DOMINANCE = Path(
    "evidence/mobius-moment-square-degree5-checked-scale-dominance-audit.json")
OUTPUT = Path(
    "evidence/mobius-moment-square-degree5-source-admissible-window-audit.json")


def contiguous_intervals(values):
    if not values:
        return []
    ordered = sorted(values)
    intervals = []
    start = previous = ordered[0]
    for value in ordered[1:]:
        if value == previous + 1:
            previous = value
            continue
        intervals.append({"start": start, "stop": previous})
        start = previous = value
    intervals.append({"start": start, "stop": previous})
    return intervals


def interval_containing(intervals, value):
    for interval in intervals:
        if interval["start"] <= value <= interval["stop"]:
            return interval
    return None


def scale_start_summary(broad_summary, canonical_summary):
    row_count = broad_summary["row_count"]
    active_starts = range(broad_summary["active_row_start_count"])
    failure_rows = broad_summary["failure_rows"]
    failing_starts = sorted({
        row["active_row_start"] for row in failure_rows
    })
    passing_starts = [
        start for start in active_starts if start not in failing_starts
    ]
    pass_intervals = contiguous_intervals(passing_starts)
    source_connected_interval = interval_containing(pass_intervals, row_count)
    canonical_min = canonical_summary["minimum_dominance_slack_above_one_half"]
    return {
        "scale_modulus": broad_summary["scale_modulus"],
        "row_count": row_count,
        "source_active_row_start": row_count,
        "active_row_start_count": broad_summary["active_row_start_count"],
        "active_row_start_range": [0, broad_summary["active_row_start_count"] - 1],
        "prime_count": broad_summary["prime_count"],
        "dominance_rows_per_start": (
            broad_summary["dominance_row_count"]
            // broad_summary["active_row_start_count"]),
        "failing_active_row_starts": failing_starts,
        "passing_active_row_start_intervals": pass_intervals,
        "source_connected_passing_interval": source_connected_interval,
        "source_connected_start_count": (
            0 if source_connected_interval is None
            else source_connected_interval["stop"]
            - source_connected_interval["start"] + 1),
        "source_start_passes": row_count not in failing_starts,
        "source_start_distance_from_nearest_failure": (
            None if not failing_starts
            else min(abs(row_count - start) for start in failing_starts)),
        "source_start_minimum_canonical_slack": canonical_min,
        "source_start_minimum_canonical_ratio": canonical_min + 0.5,
        "source_start_weakest_canonical_row": (
            canonical_summary["weakest_dominance_row"]),
        "failure_row_count": broad_summary["failure_row_count"],
        "failure_rows": failure_rows,
        "all_starts_pass": broad_summary["failure_row_count"] == 0,
    }


def build_receipt():
    broad = json.loads(BROAD_SWEEP.read_text(encoding="utf-8"))
    canonical = json.loads(CANONICAL_DOMINANCE.read_text(encoding="utf-8"))
    canonical_by_scale = {
        summary["scale_modulus"]: summary
        for summary in canonical["scale_summaries"]
    }
    scale_summaries = [
        scale_start_summary(
            broad_summary,
            canonical_by_scale[broad_summary["scale_modulus"]],
        )
        for broad_summary in broad["scale_summaries"]
    ]
    failing_scale_summaries = [
        summary for summary in scale_summaries
        if summary["failure_row_count"]
    ]
    source_slacks = [
        summary["source_start_minimum_canonical_slack"]
        for summary in scale_summaries
    ]
    source_start_blocked = [
        summary for summary in scale_summaries
        if not summary["source_start_passes"]
    ]
    total_start_count = sum(
        summary["active_row_start_count"] for summary in scale_summaries)
    failing_start_count = sum(
        len(summary["failing_active_row_starts"])
        for summary in scale_summaries)
    return {
        "status": "DERIVE_degree5_source_admissible_window_audit",
        "question": (
            "After the broad checked-scale row-start quantifier was finitely "
            "falsified, does the validated data still support a narrower "
            "source-admissible row-window target?"),
        "source_broad_sweep": str(BROAD_SWEEP),
        "source_canonical_dominance": str(CANONICAL_DOMINANCE),
        "broad_sweep_status": broad["status"],
        "canonical_dominance_status": canonical["status"],
        "scale_summaries": scale_summaries,
        "scale_count": len(scale_summaries),
        "total_active_row_starts": total_start_count,
        "failing_active_row_start_count": failing_start_count,
        "passing_active_row_start_count": (
            total_start_count - failing_start_count),
        "failing_scale_count": len(failing_scale_summaries),
        "failing_scale_summaries": failing_scale_summaries,
        "source_start_failure_count": len(source_start_blocked),
        "all_source_starts_pass": not source_start_blocked,
        "minimum_source_start_canonical_slack": min(source_slacks),
        "minimum_source_start_canonical_ratio": min(source_slacks) + 0.5,
        "weakest_source_start_scale": min(
            scale_summaries,
            key=lambda row: row["source_start_minimum_canonical_slack"]),
        "broad_failure_row_count": broad["failure_row_count"],
        "broad_failure_rows": broad["failure_rows"],
        "prediction": (
            "If the finite falsifier is a translated-window artifact rather "
            "than a source-window obstruction, the canonical source row start "
            "should remain inside a passing interval for every checked scale, "
            "and the failing translated starts should be explicitly excluded."),
        "falsifier": (
            "Any checked scale whose canonical source row start is itself a "
            "failing active row start, or whose source-connected passing "
            "interval is absent, would falsify this source-admissible finite "
            "interpretation."),
        "decision": (
            "The finite row-start map supports a narrower source-admissible "
            "target: all six canonical source starts pass, while the broad "
            "all-translation statement fails only at M=149, active row start "
            "1.  For M=149 the source-connected passing interval is starts "
            "2..64, containing the canonical source start 32.  The surviving "
            "theorem-shaped target should therefore prove source-window or "
            "admissible-window control, not all translated windows 0..2A."),
        "finite_source_admissible_window_diagnostic_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_admissible_window_theorem_proved": False,
        "pointwise_universal_adverse_drag_estimate_proved": False,
        "l2_logical_bridge_proved": False,
        "phase_curve_theorem_proved": False,
        "checked_scale_dominance_theorem_proved": False,
        "primewise_dominance_theorem_proved": False,
        "robust_margin_universal_theorem_proved": False,
        "signed_prime_correlation_proved": False,
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
