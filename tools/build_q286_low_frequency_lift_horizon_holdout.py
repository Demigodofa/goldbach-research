"""Replay the frozen q286 low-frequency lift on farther stress-marker windows.

The first low-frequency holdout kept ``full_low_frequency_lift`` alive on
fresh nearby windows.  This receipt moves the same frozen vector to a farther
denominator, including neighborhoods around previously named q286 stress
targets.  No refitting or target-specific projection is allowed.

This is finite evidence only.  It proves no low-frequency theorem,
residual-drag theorem, signed projection theorem, or Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DICTIONARY_SOURCE = ROOT / "evidence" / "q286-lift-project-dictionary-audit.json"
LOW_HOLDOUT_SOURCE = ROOT / "evidence" / "q286-low-frequency-lift-holdout.json"
OUT = ROOT / "evidence" / "q286-low-frequency-lift-horizon-holdout.json"
STRESS_TARGET = 1222142
WINDOW_SPECS = (
    (1426162, 101),
    (1500000, 101),
    (2200000, 101),
    (3305100, 101),
    (4304218, 101),
    (5000000, 101),
)
MARKER_TARGETS = (1426262, 3305200, 4304318)
HIGH_DRAG_RATIO_THRESHOLD = 0.2
CAP_TO_TEST = 0.75
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
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, np.generic):
        return json_ready(value.item())
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


def finite_summary(values):
    values = tuple(float(value) for value in values)
    finite = tuple(value for value in values if math.isfinite(value))
    if not finite:
        return {
            "count": len(values),
            "finite_count": 0,
            "nonfinite_count": len(values),
            "minimum": None,
            "maximum": None,
            "mean": None,
        }
    return {
        "count": len(values),
        "finite_count": len(finite),
        "nonfinite_count": len(values) - len(finite),
        "minimum": min(finite),
        "maximum": max(finite),
        "mean": math.fsum(finite) / len(finite),
    }


def min_record(rows, key):
    row = min(rows, key=lambda item: (item[key], item["target"]))
    return {"target": row["target"], "value": row[key]}


def max_record(rows, key):
    row = max(rows, key=lambda item: (item[key], -item["target"]))
    return {"target": row["target"], "value": row[key]}


def cap_record(rows, key, cap):
    failures = tuple(row for row in rows if row[key] > cap)
    return {
        "cap": cap,
        "passes": len(failures) == 0,
        "failing_count": len(failures),
        "failing_targets": tuple(row["target"] for row in failures[:80]),
        "maximum_excess": max(
            (row[key] - cap for row in failures), default=0.0),
    }


def selected_dictionary(dictionary_payload, dictionary_id):
    matches = [
        row for row in dictionary_payload["dictionary_rows"]
        if row["id"] == dictionary_id
    ]
    if len(matches) != 1:
        raise AssertionError(f"missing dictionary {dictionary_id}")
    return matches[0]


def collect_targets():
    targets = []
    metadata = {}
    seen = set()
    window_summaries = []
    for window_index, (start, count) in enumerate(WINDOW_SPECS):
        census = q286_first_three_dominant_mode_above_floor_holdout_census_receipt(
            start=start, target_count=count, target_step=2,
            closest_count=min(20, count), include_rows=True)
        window_rows = []
        for row in census["target_rows"]:
            target = int(row["target"])
            if target in seen:
                continue
            seen.add(target)
            targets.append(target)
            compact = {
                "target": target,
                "window_index": int(window_index),
                "window_start": int(start),
                "window_role": "horizon",
                "target_mod_286": int(row["target_mod_286"]),
                "target_mod_10010": target % 10010,
                "absolute_above_floor_signed_surplus": float(
                    row["absolute_above_floor_signed_surplus"]),
                "dominant_sum_to_principal": float(
                    row["dominant_sum_to_principal"]),
                "dominant_floor_passes": bool(row["dominant_floor_passes"]),
                "is_marker_target": target in MARKER_TARGETS,
            }
            metadata[target] = compact
            window_rows.append(compact)
        window_summaries.append({
            "window_index": int(window_index),
            "window_start": int(start),
            "target_count": int(count),
            "evaluated_target_count": len(window_rows),
            "marker_targets_present": tuple(
                row["target"] for row in window_rows
                if row["target"] in MARKER_TARGETS),
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
    return tuple(targets), metadata, tuple(window_summaries)


def cosine(a, b):
    a = np.asarray(a, dtype=np.float64).reshape(-1)
    b = np.asarray(b, dtype=np.float64).reshape(-1)
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    return None if denom == 0.0 else float(np.dot(a, b) / denom)


def main():
    dictionary_payload = json.loads(
        DICTIONARY_SOURCE.read_text(encoding="utf-8"))
    low_holdout_payload = json.loads(
        LOW_HOLDOUT_SOURCE.read_text(encoding="utf-8"))
    dictionary = selected_dictionary(
        dictionary_payload, "full_low_frequency_lift")
    outside_labels = tuple(
        label_tuple(label) for label in dictionary_payload["outside_labels"])
    rank1_vector = np.asarray(
        dictionary_payload["reference_rank1_vector"], dtype=np.float64)
    dictionary_vector = np.asarray(
        dictionary["dictionary_vector"], dtype=np.float64)
    if len(outside_labels) != 17:
        raise AssertionError("outside label count drifted")

    rank1_sum = float(np.sum(rank1_vector))
    dictionary_sum = float(np.sum(dictionary_vector))
    if rank1_sum <= 0.0 or dictionary_sum <= 0.0:
        raise AssertionError("canonical vector sign drifted")

    targets, metadata, window_summaries = collect_targets()
    missing_markers = tuple(
        target for target in MARKER_TARGETS if target not in metadata)
    if missing_markers:
        raise AssertionError(f"marker targets missing: {missing_markers}")

    sample_targets = tuple(dict.fromkeys((STRESS_TARGET,) + targets))
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=sample_targets, dominant_modes=(1, 2),
        tail_threshold=.3, top_channel_count=40)
    stress_contributions = contribution_map(
        profile["target_rows"][STRESS_TARGET])

    rows = []
    deficit_rows = []
    for target in targets:
        profile_row = profile["target_rows"][target]
        if not profile_row["dominant_floor_passes"]:
            deficit_rows.append(metadata[target])
            continue
        contributions = contribution_map(profile_row)
        outside_delta_vector = np.asarray([
            contributions[label] - stress_contributions[label]
            for label in outside_labels
        ], dtype=np.float64)
        rank1_scalar = float(np.dot(outside_delta_vector, rank1_vector))
        rank1_vector_row = rank1_scalar * rank1_vector
        dictionary_scalar = float(
            np.dot(outside_delta_vector, dictionary_vector))
        dictionary_vector_row = dictionary_scalar * dictionary_vector
        full_delta = float(np.sum(outside_delta_vector))
        rank1_delta = float(np.sum(rank1_vector_row))
        dictionary_delta = float(np.sum(dictionary_vector_row))
        rank1_residual = full_delta - rank1_delta
        dictionary_residual = full_delta - dictionary_delta
        rank1_drag = max(0.0, -rank1_residual)
        dictionary_drag = max(0.0, -dictionary_residual)
        rows.append({
            **metadata[target],
            "full_outside_delta_to_stress": full_delta,
            "rank1_reconstructed_outside_delta": rank1_delta,
            "rank1_residual_after_row_sum": rank1_residual,
            "rank1_residual_drag": rank1_drag,
            "rank1_residual_drag_to_rank1_ratio": (
                rank1_drag / rank1_delta if rank1_delta > 0 else math.inf),
            "low_frequency_reconstructed_outside_delta": dictionary_delta,
            "low_frequency_residual_after_row_sum": dictionary_residual,
            "low_frequency_residual_drag": dictionary_drag,
            "low_frequency_residual_drag_to_low_frequency_ratio": (
                dictionary_drag / dictionary_delta
                if dictionary_delta > 0 else math.inf),
            "low_frequency_delta_to_full_delta_ratio": (
                dictionary_delta / full_delta if full_delta else math.inf),
            "rank1_reference_delta_vector": rank1_vector_row,
            "low_frequency_delta_vector": dictionary_vector_row,
        })

    if not rows:
        raise AssertionError("no horizon clear rows")

    reference_high_drag = {
        row["target"] for row in rows
        if row["rank1_residual_drag_to_rank1_ratio"]
        >= HIGH_DRAG_RATIO_THRESHOLD
    }
    top_k = len(reference_high_drag)
    rank1_rows_by_drag = tuple(sorted(
        rows,
        key=lambda row: (
            row["rank1_residual_drag_to_rank1_ratio"],
            row["rank1_residual_drag"],
            -row["target"]),
        reverse=True))
    low_rows_by_drag = tuple(sorted(
        rows,
        key=lambda row: (
            row["low_frequency_residual_drag_to_low_frequency_ratio"],
            row["low_frequency_residual_drag"],
            -row["target"]),
        reverse=True))
    low_high_drag = {
        row["target"] for row in low_rows_by_drag[:top_k]
    } if top_k else set()
    high_drag_overlap = reference_high_drag & low_high_drag

    rank1_matrix = np.asarray([
        value
        for row in rows
        for value in row["rank1_reference_delta_vector"]
    ], dtype=np.float64)
    low_matrix = np.asarray([
        value
        for row in rows
        for value in row["low_frequency_delta_vector"]
    ], dtype=np.float64)
    exact_nonpositive = tuple(
        row for row in rows if row["full_outside_delta_to_stress"] <= 0)
    rank1_nonpositive = tuple(
        row for row in rows if row["rank1_reconstructed_outside_delta"] <= 0)
    low_nonpositive = tuple(
        row for row in rows
        if row["low_frequency_reconstructed_outside_delta"] <= 0)
    rank1_cap = cap_record(
        rows, "rank1_residual_drag_to_rank1_ratio", CAP_TO_TEST)
    low_cap = cap_record(
        rows, "low_frequency_residual_drag_to_low_frequency_ratio",
        CAP_TO_TEST)
    marker_rows = tuple(
        row for row in rows if row["target"] in MARKER_TARGETS)
    marker_deficits = tuple(
        row for row in deficit_rows if row["target"] in MARKER_TARGETS)

    passes_horizon_gate = (
        len(deficit_rows) == 0
        and len(exact_nonpositive) == 0
        and len(rank1_nonpositive) == 0
        and len(low_nonpositive) == 0
        and rank1_cap["failing_count"] == 0
        and low_cap["failing_count"] == 0
        and (
            not reference_high_drag
            or len(high_drag_overlap) >= math.ceil(
                0.6 * len(reference_high_drag))))

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_lift_project_dictionary_audit": str(
            DICTIONARY_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lift_holdout": str(
            LOW_HOLDOUT_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite horizon holdout only; the frozen full_low_frequency_lift "
            "and frozen rank-1 reference are replayed on later q286 windows "
            "without refitting.  This proves no low-frequency theorem, "
            "residual-bound theorem, signed projection theorem, or Goldbach "
            "theorem."),
        "candidate": (
            "The static low-frequency q286 channel-lattice lift remains a "
            "useful finite hole-tightening tool on farther windows, including "
            "neighborhoods of previously named stress-marker targets."),
        "mechanism": (
            "Keep the frozen full_low_frequency_lift vector from the original "
            "dictionary audit.  Recompute exact signed channel profiles on "
            "six later windows, subtract stress target 1222142 on the same "
            "17 outside channels, and compare exact outside deltas, frozen "
            "rank-1 replay, and frozen low-frequency replay."),
        "prediction": (
            "If the low-frequency shadow is not just a local denominator "
            "artifact, then the later-window replay should retain positive "
            "outside deltas, no 0.75 residual-drag cap failures, and meaningful "
            "overlap with the frozen rank-1 high-drag rows."),
        "falsifier": (
            "Any new horizon deficit, nonpositive exact/rank-1/low-frequency "
            "outside delta, 0.75 cap failure, or poor high-drag overlap demotes "
            "the frozen low-frequency vector as a stable q286 hole-tightening "
            "tool."),
        "novelty_label": "new-to-this-task",
        "window_specs": WINDOW_SPECS,
        "marker_targets": MARKER_TARGETS,
        "stress_target": STRESS_TARGET,
        "horizon_target_count": len(targets),
        "horizon_clear_count": len(rows),
        "horizon_deficit_count": len(deficit_rows),
        "horizon_deficit_targets": tuple(
            row["target"] for row in deficit_rows),
        "window_summaries": window_summaries,
        "outside_labels": outside_labels,
        "frozen_dictionary_id": dictionary["id"],
        "previous_heldout_gate_passed": low_holdout_payload[
            "predeclared_low_frequency_lift_passes_holdout_signal_gate"],
        "previous_heldout_clear_count": low_holdout_payload[
            "heldout_clear_count"],
        "reference_rank1_high_drag_count": len(reference_high_drag),
        "reference_rank1_high_drag_targets": tuple(
            sorted(reference_high_drag)),
        "low_frequency_top_k_high_drag_targets": tuple(
            row["target"] for row in low_rows_by_drag[:top_k]),
        "high_drag_overlap_count_at_reference_k": len(high_drag_overlap),
        "high_drag_recall_at_reference_k": (
            len(high_drag_overlap) / len(reference_high_drag)
            if reference_high_drag else None),
        "matrix_cosine_low_frequency_to_rank1_reference": cosine(
            low_matrix, rank1_matrix),
        "exact_nonpositive_outside_delta_count": len(exact_nonpositive),
        "exact_nonpositive_outside_delta_targets": tuple(
            row["target"] for row in exact_nonpositive),
        "rank1_nonpositive_delta_count": len(rank1_nonpositive),
        "rank1_nonpositive_delta_targets": tuple(
            row["target"] for row in rank1_nonpositive),
        "low_frequency_nonpositive_delta_count": len(low_nonpositive),
        "low_frequency_nonpositive_delta_targets": tuple(
            row["target"] for row in low_nonpositive),
        "rank1_cap_record": rank1_cap,
        "low_frequency_cap_record": low_cap,
        "full_outside_delta_summary": finite_summary(
            row["full_outside_delta_to_stress"] for row in rows),
        "rank1_reconstructed_delta_summary": finite_summary(
            row["rank1_reconstructed_outside_delta"] for row in rows),
        "rank1_residual_drag_ratio_summary": finite_summary(
            row["rank1_residual_drag_to_rank1_ratio"] for row in rows),
        "low_frequency_reconstructed_delta_summary": finite_summary(
            row["low_frequency_reconstructed_outside_delta"] for row in rows),
        "low_frequency_residual_drag_ratio_summary": finite_summary(
            row["low_frequency_residual_drag_to_low_frequency_ratio"]
            for row in rows),
        "low_frequency_delta_to_full_delta_ratio_summary": finite_summary(
            row["low_frequency_delta_to_full_delta_ratio"] for row in rows),
        "minimum_full_outside_delta": min_record(
            rows, "full_outside_delta_to_stress"),
        "minimum_rank1_reconstructed_delta": min_record(
            rows, "rank1_reconstructed_outside_delta"),
        "minimum_low_frequency_reconstructed_delta": min_record(
            rows, "low_frequency_reconstructed_outside_delta"),
        "maximum_rank1_residual_drag_ratio": max_record(
            rows, "rank1_residual_drag_to_rank1_ratio"),
        "maximum_low_frequency_residual_drag_ratio": max_record(
            rows, "low_frequency_residual_drag_to_low_frequency_ratio"),
        "marker_clear_rows": marker_rows,
        "marker_deficit_rows": marker_deficits,
        "rows_by_rank1_residual_drag_ratio": rank1_rows_by_drag[:80],
        "rows_by_low_frequency_residual_drag_ratio": low_rows_by_drag[:80],
        "interpretation": {
            "passes_horizon_signal_gate": passes_horizon_gate,
            "next_if_passes": (
                "Keep the frozen low-frequency lift as a finite stable tool, "
                "but seek a theorem through character-sum magnitudes, signed "
                "cones, or row-dependent arithmetic balance."),
            "next_if_fails": (
                "Demote the frozen low-frequency lift as a local-window tool "
                "and return to direct signed residue-weight structure."),
        },
        "low_frequency_horizon_holdout_measured": True,
        "predeclared_low_frequency_lift_passes_horizon_signal_gate": (
            passes_horizon_gate),
        "low_frequency_lift_theorem_proved": False,
        "rank1_residual_bound_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }

    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
