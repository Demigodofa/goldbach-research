"""Audit frozen q286 rank-1 residual drag on the full six-window denominator.

The closest-20 holdout kept the frozen Octave rank-1 outside direction and
the 0.75 residual-drag cap alive.  This receipt applies the same frozen
direction to every evaluated target in the six near-boundary windows.  It is
designed to record either survival or falsification without refitting.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RANK1_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-octave-rank1-audit.json")
EXPANDED_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-expanded-holdout.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-full-window-audit.json")
STRESS_TARGET = 1222142
CAPS = (0.2, 0.25, 0.5, 0.7, 0.75, 0.8, 1.0)
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_above_floor_holdout_census_receipt,
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set)):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def label_tuple(label):
    return tuple(int(part) for part in label)


def contribution_map(row):
    return {
        label_tuple(item["representative_label"]): float(
            item["contribution_to_principal_ratio"])
        for item in row["real_channel_contribution_rows"]
    }


def summarize(values):
    values = tuple(float(value) for value in values)
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def compact_census_row(row, window_index, window_start, window_role):
    target = int(row["target"])
    return {
        "target": target,
        "window_index": int(window_index),
        "window_start": int(window_start),
        "window_role": window_role,
        "target_mod_286": int(row["target_mod_286"]),
        "target_mod_10010": target % 10010,
        "absolute_above_floor_signed_surplus": float(
            row["absolute_above_floor_signed_surplus"]),
        "dominant_sum_to_principal": float(row["dominant_sum_to_principal"]),
        "dominant_floor_passes": bool(row["dominant_floor_passes"]),
    }


def collect_full_window_rows(window_specs):
    rows = []
    seen = set()
    window_summaries = []
    for window_index, (start, count) in enumerate(window_specs):
        census = q286_first_three_dominant_mode_above_floor_holdout_census_receipt(
            start=start, target_count=count, target_step=2,
            closest_count=min(20, count), include_rows=True)
        role = "primary" if window_index == 0 else "stress"
        window_rows = []
        for row in census["target_rows"]:
            compact = compact_census_row(row, window_index, start, role)
            target = compact["target"]
            if target in seen:
                continue
            seen.add(target)
            rows.append(compact)
            window_rows.append(compact)
        window_summaries.append({
            "window_index": int(window_index),
            "window_start": int(start),
            "window_role": role,
            "target_count": int(count),
            "evaluated_target_count": len(window_rows),
            "deficit_targets": tuple(
                row["target"] for row in window_rows
                if not row["dominant_floor_passes"]),
            "minimum_abs_surplus": min(
                row["absolute_above_floor_signed_surplus"]
                for row in window_rows),
            "maximum_abs_surplus": max(
                row["absolute_above_floor_signed_surplus"]
                for row in window_rows),
        })
    return tuple(rows), tuple(window_summaries)


def cap_record(rows, cap):
    failures = tuple(
        row for row in rows if row["residual_drag_to_rank1_ratio"] > cap)
    return {
        "cap": cap,
        "passes": len(failures) == 0,
        "failing_count": len(failures),
        "failing_targets": tuple(row["target"] for row in failures),
        "maximum_excess": max(
            (row["residual_drag_to_rank1_ratio"] - cap for row in failures),
            default=0.0),
    }


def min_record(rows, key):
    row = min(rows, key=lambda item: (item[key], item["target"]))
    return {"target": row["target"], "value": row[key]}


def max_record(rows, key):
    row = max(rows, key=lambda item: (item[key], -item["target"]))
    return {"target": row["target"], "value": row[key]}


def main():
    rank1_payload = json.loads(RANK1_SOURCE.read_text(encoding="utf-8"))
    expanded_payload = json.loads(
        EXPANDED_SOURCE.read_text(encoding="utf-8"))
    window_specs = tuple(
        tuple(int(value) for value in spec)
        for spec in expanded_payload["window_specs"])

    full_rows, window_summaries = collect_full_window_rows(window_specs)
    targets = tuple(row["target"] for row in full_rows)
    expected_count = sum(count for _start, count in window_specs)
    if len(targets) != expected_count:
        raise AssertionError("full-window target count drifted")
    if STRESS_TARGET not in targets:
        raise AssertionError("stress target missing")

    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=targets, dominant_modes=(1, 2), tail_threshold=.3,
        top_channel_count=40)
    stress_profile_row = profile["target_rows"][STRESS_TARGET]
    if stress_profile_row["dominant_floor_passes"]:
        raise AssertionError("stress target no longer deficit")
    stress_contributions = contribution_map(stress_profile_row)

    outside_labels = tuple(
        label_tuple(row["label"])
        for row in rank1_payload["rank1_right_singular_vector_by_channel"])
    rank1_vector = tuple(
        float(row["rank1_right_singular_vector_loading"])
        for row in rank1_payload["rank1_right_singular_vector_by_channel"])
    rank1_vector_sum = float(rank1_payload["rank1_right_vector_sum"])
    if len(outside_labels) != 17:
        raise AssertionError("outside label count drifted")
    if rank1_vector_sum <= 0:
        raise AssertionError("rank-1 vector sign is not canonical")

    rows = []
    deficit_targets = []
    for source_row in full_rows:
        target = int(source_row["target"])
        profile_row = profile["target_rows"][target]
        if not profile_row["has_strict_central_prime_pairs"]:
            raise AssertionError(f"target {target} lacks strict pairs")
        if not profile_row["dominant_floor_passes"]:
            deficit_targets.append(target)
            if target != STRESS_TARGET:
                continue
        if target == STRESS_TARGET:
            continue
        contributions = contribution_map(profile_row)
        outside_delta_vector = tuple(
            contributions[label] - stress_contributions[label]
            for label in outside_labels)
        full_delta = math.fsum(outside_delta_vector)
        rank1_delta = (
            math.fsum(
                value * loading
                for value, loading in zip(outside_delta_vector, rank1_vector))
            * rank1_vector_sum)
        residual = full_delta - rank1_delta
        residual_drag = max(0.0, -residual)
        rows.append({
            "target": target,
            "window_index": source_row["window_index"],
            "window_start": source_row["window_start"],
            "window_role": source_row["window_role"],
            "target_mod_286": source_row["target_mod_286"],
            "target_mod_10010": source_row["target_mod_10010"],
            "absolute_above_floor_signed_surplus": source_row[
                "absolute_above_floor_signed_surplus"],
            "full_outside_delta_to_stress": full_delta,
            "rank1_reconstructed_outside_delta": rank1_delta,
            "residual_after_rank1_row_sum": residual,
            "residual_drag": residual_drag,
            "residual_drag_to_rank1_ratio": (
                residual_drag / rank1_delta if rank1_delta > 0 else math.inf),
            "full_delta_to_rank1_ratio": (
                full_delta / rank1_delta if rank1_delta != 0 else math.inf),
        })

    if tuple(deficit_targets) != (STRESS_TARGET,):
        raise AssertionError("full-window deficit set drifted")

    clear_count = len(rows)
    if clear_count != expected_count - 1:
        raise AssertionError("full-window clear count drifted")
    nonpositive_rank1_rows = tuple(
        row for row in rows if row["rank1_reconstructed_outside_delta"] <= 0)
    nonpositive_full_rows = tuple(
        row for row in rows if row["full_outside_delta_to_stress"] <= 0)
    rows_by_drag_ratio = tuple(sorted(
        rows,
        key=lambda row: (
            row["residual_drag_to_rank1_ratio"],
            row["residual_drag"],
            -row["target"]),
        reverse=True))
    worst = rows_by_drag_ratio[0]
    cap_records = tuple(cap_record(rows_by_drag_ratio, cap) for cap in CAPS)
    by_cap = {record["cap"]: record for record in cap_records}

    negative_residual_rows = tuple(
        row for row in rows if row["residual_after_rank1_row_sum"] < 0)
    nonnegative_residual_rows = tuple(
        row for row in rows if row["residual_after_rank1_row_sum"] >= 0)
    cap_075_survives = by_cap[0.75]["failing_count"] == 0
    rank1_all_positive = len(nonpositive_rank1_rows) == 0
    exact_outside_all_positive = len(nonpositive_full_rows) == 0

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_outside_plane_remainder_octave_rank1_audit": str(
            RANK1_SOURCE.relative_to(ROOT)),
        "source_rank1_residual_drag_expanded_holdout": str(
            EXPANDED_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite full-window rank-1 residual-drag audit only; it applies "
            "the frozen rank-1 outside direction to the 716 targets from the "
            "six near-boundary windows and proves no residual-bound theorem, "
            "rank-1 theorem, signed projection theorem, or Goldbach proof"),
        "candidate": (
            "The frozen rank-1 outside direction and 0.75 residual-drag cap "
            "might survive all evaluated targets in the six near-boundary "
            "windows, not only the closest retained rows."),
        "mechanism": (
            "Use the full six window specs from the prior holdout, recompute "
            "exact q286 signed channel profiles for every target, subtract "
            "stress row 1222142 on the 17 outside channels, and apply the "
            "previous Octave rank-1 direction without refitting."),
        "prediction": (
            "If the finite rank-1 plus residual-drag shape is stable across "
            "the original window denominator, then every clear row should "
            "have positive frozen rank-1 outside delta and no row should "
            "exceed the 0.75 residual-drag cap."),
        "falsifier": (
            "Any clear row with nonpositive frozen rank-1 outside delta, "
            "nonpositive exact outside delta, or residual drag above 0.75 "
            "times rank-1 outside delta falsifies the corresponding finite "
            "full-window stability claim."),
        "novelty_label": "new-to-this-task",
        "window_specs": window_specs,
        "full_window_target_count": len(targets),
        "deficit_targets": tuple(deficit_targets),
        "clear_count": clear_count,
        "outside_label_count": len(outside_labels),
        "outside_labels": outside_labels,
        "rank1_source_energy_fraction": rank1_payload[
            "rank1_energy_fraction"],
        "rank1_vector_sum": rank1_vector_sum,
        "window_summaries": window_summaries,
        "nonpositive_rank1_row_count": len(nonpositive_rank1_rows),
        "nonpositive_rank1_targets": tuple(
            row["target"] for row in nonpositive_rank1_rows),
        "nonpositive_full_outside_delta_count": len(nonpositive_full_rows),
        "nonpositive_full_outside_delta_targets": tuple(
            row["target"] for row in nonpositive_full_rows),
        "negative_residual_row_count": len(negative_residual_rows),
        "nonnegative_residual_row_count": len(nonnegative_residual_rows),
        "maximum_residual_drag_to_rank1_ratio": worst[
            "residual_drag_to_rank1_ratio"],
        "worst_residual_drag_row": worst,
        "cap_records": cap_records,
        "minimum_full_outside_delta": min_record(
            rows, "full_outside_delta_to_stress"),
        "maximum_full_outside_delta": max_record(
            rows, "full_outside_delta_to_stress"),
        "minimum_rank1_reconstructed_outside_delta": min_record(
            rows, "rank1_reconstructed_outside_delta"),
        "maximum_rank1_reconstructed_outside_delta": max_record(
            rows, "rank1_reconstructed_outside_delta"),
        "full_outside_delta_summary": summarize(
            row["full_outside_delta_to_stress"] for row in rows),
        "rank1_reconstructed_outside_delta_summary": summarize(
            row["rank1_reconstructed_outside_delta"] for row in rows),
        "residual_drag_summary": summarize(
            row["residual_drag"] for row in rows),
        "residual_drag_to_rank1_ratio_summary": summarize(
            row["residual_drag_to_rank1_ratio"] for row in rows),
        "rank1_full_window_all_clears_positive": rank1_all_positive,
        "exact_outside_full_window_all_clears_positive": (
            exact_outside_all_positive),
        "three_quarter_residual_drag_cap_holds_on_full_window": (
            cap_075_survives),
        "rows_by_residual_drag_ratio": rows_by_drag_ratio[:80],
        "rows_by_full_outside_delta": tuple(sorted(
            rows,
            key=lambda row: (
                row["full_outside_delta_to_stress"], row["target"]))[:80]),
        "summary": {
            "full_window_denominator": (
                "The six original near-boundary windows contain 716 checked "
                "targets, with the same lone deficit 1222142."),
            "frozen_rank1": (
                "The frozen rank-1 outside direction is tested without "
                "refitting against every full-window clear row."),
            "cap_result": (
                "The receipt records whether the 0.75 residual-drag cap "
                "survives or fails on the full-window denominator."),
            "theorem_boundary": (
                "Survival would still be finite evidence only; failure would "
                "falsify this full-window cap while preserving smaller "
                "holdout results."),
        },
        "interpretation": {
            "route_status": (
                "Use this as the first full-window stress test of the frozen "
                "rank-1 plus residual-drag route.  Do not promote a surviving "
                "finite cap to a theorem without a non-post-hoc arithmetic "
                "proof."),
        },
        "rank1_residual_drag_full_window_audit_measured": True,
        "full_window_lone_deficit_is_stress": (
            tuple(deficit_targets) == (STRESS_TARGET,)),
        "frozen_rank1_all_full_window_clears_positive": rank1_all_positive,
        "three_quarter_residual_drag_cap_holds_on_full_window": (
            cap_075_survives),
        "rank1_residual_bound_theorem_proved": False,
        "outside_remainder_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }

    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
