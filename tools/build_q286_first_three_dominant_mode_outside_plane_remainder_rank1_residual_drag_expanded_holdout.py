"""Audit the frozen q286 rank-1 residual-drag cap on a wider holdout.

The previous residual-drag ledger used the 72-row denominator from the
pair/complement window holdout.  This receipt widens the same six windows to
the 20 closest-margin rows per window and applies the frozen Octave rank-1
outside direction without refitting it.
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
DRAG_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-ledger.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-expanded-holdout.json")
STRESS_TARGET = 1222142
EXPANDED_CLOSEST_COUNT = 20
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


def collect_expanded_rows(window_specs, closest_count):
    rows = []
    seen = set()
    window_summaries = []
    for window_index, (start, count) in enumerate(window_specs):
        census = q286_first_three_dominant_mode_above_floor_holdout_census_receipt(
            start=start, target_count=count, target_step=2,
            closest_count=min(closest_count, count), include_rows=False)
        role = "primary" if window_index == 0 else "stress"
        selected_rows = []
        for row in census["closest_margin_rows"]:
            target = int(row["target"])
            if target in seen:
                continue
            seen.add(target)
            expanded = {
                **row,
                "window_index": window_index,
                "window_start": int(start),
                "window_role": role,
                "target_mod_10010": target % 10010,
            }
            rows.append(expanded)
            selected_rows.append(expanded)
        window_summaries.append({
            "window_index": window_index,
            "window_start": int(start),
            "window_role": role,
            "target_count": int(count),
            "selected_closest_count": len(selected_rows),
            "selected_targets": tuple(row["target"] for row in selected_rows),
            "selected_deficit_targets": tuple(
                row["target"] for row in selected_rows
                if not row["dominant_floor_passes"]),
            "selected_minimum_abs_surplus": min(
                row["absolute_above_floor_signed_surplus"]
                for row in selected_rows),
            "selected_maximum_abs_surplus": max(
                row["absolute_above_floor_signed_surplus"]
                for row in selected_rows),
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
    drag_payload = json.loads(DRAG_SOURCE.read_text(encoding="utf-8"))
    window_specs = tuple(
        tuple(spec) for spec in drag_payload.get("window_specs", ())
    )
    if not window_specs:
        # The first drag ledger is derived from the rank-1 receipt, whose
        # source separator used the canonical six windows.  Keep the exact
        # list explicit if older evidence lacks the field.
        window_specs = (
            (1200200, 211), (1220000, 101), (1221000, 101),
            (1222000, 101), (1240000, 101), (1242000, 101))

    expanded_rows, window_summaries = collect_expanded_rows(
        window_specs, EXPANDED_CLOSEST_COUNT)
    targets = tuple(int(row["target"]) for row in expanded_rows)
    if len(targets) != 120:
        raise AssertionError("expanded closest-20 denominator drifted")
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
    for source_row in expanded_rows:
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
        if rank1_delta <= 0:
            raise AssertionError(f"rank-1 projection failed at {target}")
        rows.append({
            "target": target,
            "window_index": int(source_row["window_index"]),
            "window_start": int(source_row["window_start"]),
            "window_role": source_row["window_role"],
            "target_mod_286": int(source_row["target_mod_286"]),
            "target_mod_10010": int(source_row["target_mod_10010"]),
            "absolute_above_floor_signed_surplus": float(
                source_row["absolute_above_floor_signed_surplus"]),
            "full_outside_delta_to_stress": full_delta,
            "rank1_reconstructed_outside_delta": rank1_delta,
            "residual_after_rank1_row_sum": residual,
            "residual_drag": residual_drag,
            "residual_drag_to_rank1_ratio": residual_drag / rank1_delta,
            "full_delta_to_rank1_ratio": full_delta / rank1_delta,
        })

    if tuple(deficit_targets) != (STRESS_TARGET,):
        raise AssertionError("expanded holdout deficit set drifted")
    if len(rows) != 119:
        raise AssertionError("expanded holdout clear count drifted")

    rows_by_drag_ratio = tuple(sorted(
        rows,
        key=lambda row: (
            row["residual_drag_to_rank1_ratio"],
            row["residual_drag"],
            -row["target"]),
        reverse=True))
    worst = rows_by_drag_ratio[0]
    if worst["target"] != 1242118:
        raise AssertionError("expanded holdout worst row drifted")
    max_ratio = worst["residual_drag_to_rank1_ratio"]
    if not (0.7 < max_ratio < 0.75):
        raise AssertionError("expanded holdout max ratio left expected bracket")

    cap_records = tuple(cap_record(rows_by_drag_ratio, cap) for cap in CAPS)
    by_cap = {record["cap"]: record for record in cap_records}
    if by_cap[0.75]["failing_count"] != 0:
        raise AssertionError("expanded holdout 3/4 cap failed")
    if by_cap[0.7]["failing_targets"] != (1242118,):
        raise AssertionError("expanded holdout 0.7 cap failures drifted")
    if by_cap[0.5]["failing_targets"] != (1242118, 1222048):
        raise AssertionError("expanded holdout half-cap failures drifted")
    if by_cap[0.25]["failing_targets"] != (1242118, 1222048, 1220056):
        raise AssertionError("expanded holdout quarter-cap failures drifted")

    negative_residual_rows = tuple(
        row for row in rows if row["residual_after_rank1_row_sum"] < 0)
    nonnegative_residual_rows = tuple(
        row for row in rows if row["residual_after_rank1_row_sum"] >= 0)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_outside_plane_remainder_octave_rank1_audit": str(
            RANK1_SOURCE.relative_to(ROOT)),
        "source_rank1_residual_drag_ledger": str(
            DRAG_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite expanded-holdout rank-1 residual-drag audit only; the "
            "frozen rank-1 direction and checked 3/4 cap survive the closest-"
            "20 window expansion, but no residual-bound theorem, rank-1 "
            "theorem, signed projection theorem, or Goldbach proof is "
            "established"),
        "candidate": (
            "The finite 3/4 residual-drag cap might be stable beyond the "
            "original closest-12 denominator when the Octave rank-1 outside "
            "direction is frozen rather than refit."),
        "mechanism": (
            "Use the same six near-boundary windows, widen each retained "
            "closest-margin set from 12 to 20 rows, recompute exact q286 "
            "signed channel profiles, and apply the prior rank-1 right "
            "singular direction to each clear-minus-stress outside-channel "
            "delta vector."),
        "prediction": (
            "If the rank-1 plus residual-drag shape is not an artifact of the "
            "72-row denominator, then the frozen rank-1 projection should "
            "remain positive and the 0.75 residual-drag cap should survive "
            "on the wider closest-20 holdout."),
        "falsifier": (
            "A new clear row with nonpositive frozen rank-1 projection or "
            "residual drag above 0.75 times the rank-1 reconstructed outside "
            "delta would falsify this finite stability check."),
        "novelty_label": "new-to-this-task",
        "window_specs": window_specs,
        "expanded_closest_count_per_window": EXPANDED_CLOSEST_COUNT,
        "expanded_target_count": len(targets),
        "deficit_targets": tuple(deficit_targets),
        "clear_count": len(rows),
        "outside_label_count": len(outside_labels),
        "outside_labels": outside_labels,
        "rank1_source_energy_fraction": rank1_payload[
            "rank1_energy_fraction"],
        "rank1_vector_sum": rank1_vector_sum,
        "window_summaries": window_summaries,
        "negative_residual_row_count": len(negative_residual_rows),
        "nonnegative_residual_row_count": len(nonnegative_residual_rows),
        "maximum_residual_drag_to_rank1_ratio": max_ratio,
        "worst_residual_drag_row": worst,
        "cap_records": cap_records,
        "minimum_full_outside_delta": min_record(
            rows, "full_outside_delta_to_stress"),
        "maximum_full_outside_delta": max_record(
            rows, "full_outside_delta_to_stress"),
        "minimum_rank1_reconstructed_outside_delta": min_record(
            rows, "rank1_reconstructed_outside_delta"),
        "full_outside_delta_summary": summarize(
            row["full_outside_delta_to_stress"] for row in rows),
        "rank1_reconstructed_outside_delta_summary": summarize(
            row["rank1_reconstructed_outside_delta"] for row in rows),
        "residual_drag_summary": summarize(
            row["residual_drag"] for row in rows),
        "residual_drag_to_rank1_ratio_summary": summarize(
            row["residual_drag_to_rank1_ratio"] for row in rows),
        "rows_by_residual_drag_ratio": rows_by_drag_ratio,
        "rows_by_full_outside_delta": tuple(sorted(
            rows,
            key=lambda row: (
                row["full_outside_delta_to_stress"], row["target"]))),
        "summary": {
            "expanded_holdout": (
                "The closest-20 expansion has 120 targets, with the same lone "
                "deficit 1222142 and 119 checked clears."),
            "frozen_rank1_survives": (
                "The frozen Octave rank-1 outside direction stays positive "
                "on every expanded clear-minus-stress outside vector."),
            "three_quarter_cap_survives": (
                "The 0.75 residual-drag cap survives the expanded holdout; "
                "the worst row remains 1242118 with drag/rank1 about "
                "0.7421344693."),
            "lower_caps_still_fail": (
                "The 0.7, half-drag, and quarter-drag failures are unchanged "
                "from the 71-row ledger."),
        },
        "interpretation": {
            "hole_status": (
                "The loop tightened by surviving a non-refit denominator "
                "expansion, but the near-sharp 3/4 cap remains finite "
                "evidence rather than proof."),
            "route_status": (
                "The next theorem target can keep the frozen rank-1 outside "
                "direction plus residual-drag inequality, now stress-tested "
                "against the closest-20 window expansion."),
        },
        "rank1_residual_drag_expanded_holdout_measured": True,
        "expanded_holdout_lone_deficit_is_stress": True,
        "frozen_rank1_all_expanded_clears_positive": True,
        "three_quarter_residual_drag_cap_holds_on_expanded_holdout": True,
        "seven_tenths_residual_drag_cap_refuted_on_expanded_holdout": True,
        "half_residual_drag_cap_refuted_on_expanded_holdout": True,
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
