"""Hold out the q286 low-frequency lift from the dictionary audit.

The prior lift-project dictionary audit found one partial signal:
``full_low_frequency_lift``.  This builder freezes that vector and replays it
on fresh q286 windows without re-projecting or target-specific fitting.

The result is a finite holdout diagnostic only.  It proves no lifted
dictionary theorem, residual-drag theorem, signed projection theorem, or
Goldbach theorem.
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
RANK1_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-octave-rank1-audit.json")
OUT = ROOT / "evidence" / "q286-low-frequency-lift-holdout.json"
STRESS_TARGET = 1222142
WINDOW_SPECS = (
    (1260000, 101),
    (1261000, 101),
    (1262000, 101),
    (1280000, 101),
    (1281000, 101),
    (1282000, 101),
)
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


def collect_holdout_targets():
    targets = []
    target_metadata = {}
    seen = set()
    window_summaries = []
    for window_index, (start, count) in enumerate(WINDOW_SPECS):
        census = q286_first_three_dominant_mode_above_floor_holdout_census_receipt(
            start=start, target_count=count, target_step=2,
            closest_count=min(20, count), include_rows=True)
        role = "heldout"
        window_targets = []
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
                "window_role": role,
                "target_mod_286": int(row["target_mod_286"]),
                "target_mod_10010": target % 10010,
                "absolute_above_floor_signed_surplus": float(
                    row["absolute_above_floor_signed_surplus"]),
                "dominant_floor_passes": bool(row["dominant_floor_passes"]),
            }
            target_metadata[target] = compact
            window_targets.append(compact)
        window_summaries.append({
            "window_index": int(window_index),
            "window_start": int(start),
            "target_count": int(count),
            "evaluated_target_count": len(window_targets),
            "deficit_targets": tuple(
                row["target"] for row in window_targets
                if not row["dominant_floor_passes"]),
            "minimum_abs_surplus": min(
                row["absolute_above_floor_signed_surplus"]
                for row in window_targets),
            "maximum_abs_surplus": max(
                row["absolute_above_floor_signed_surplus"]
                for row in window_targets),
        })
    return tuple(targets), target_metadata, tuple(window_summaries)


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
        "failing_targets": tuple(row["target"] for row in failures[:40]),
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


def main():
    dictionary_payload = json.loads(
        DICTIONARY_SOURCE.read_text(encoding="utf-8"))
    rank1_payload = json.loads(RANK1_SOURCE.read_text(encoding="utf-8"))
    dictionary = selected_dictionary(
        dictionary_payload, "full_low_frequency_lift")

    outside_labels = tuple(
        label_tuple(row["label"])
        for row in rank1_payload["rank1_right_singular_vector_by_channel"])
    dictionary_vector = np.asarray(
        dictionary["dictionary_vector"], dtype=np.float64)
    rank1_vector = np.asarray(
        dictionary_payload["reference_rank1_vector"], dtype=np.float64)
    if len(outside_labels) != len(dictionary_vector) or len(outside_labels) != 17:
        raise AssertionError("outside label or vector length drifted")
    dictionary_sum = float(np.sum(dictionary_vector))
    rank1_sum = float(np.sum(rank1_vector))
    if dictionary_sum <= 0 or rank1_sum <= 0:
        raise AssertionError("canonical vector sums drifted")

    targets, target_metadata, window_summaries = collect_holdout_targets()
    sample_targets = tuple(dict.fromkeys((STRESS_TARGET,) + targets))
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=sample_targets, dominant_modes=(1, 2),
        tail_threshold=.3, top_channel_count=40)
    stress_contributions = contribution_map(
        profile["target_rows"][STRESS_TARGET])

    rows = []
    deficit_rows = []
    for target in targets:
        metadata = target_metadata[target]
        profile_row = profile["target_rows"][target]
        if not profile_row["dominant_floor_passes"]:
            deficit_rows.append(metadata)
            continue
        contributions = contribution_map(profile_row)
        outside_delta_vector = np.asarray([
            contributions[label] - stress_contributions[label]
            for label in outside_labels
        ], dtype=np.float64)
        full_delta = float(np.sum(outside_delta_vector))
        rank1_delta = float(np.dot(outside_delta_vector, rank1_vector)
                            * rank1_sum)
        dictionary_delta = float(np.dot(outside_delta_vector, dictionary_vector)
                                 * dictionary_sum)
        rank1_residual = full_delta - rank1_delta
        dictionary_residual = full_delta - dictionary_delta
        rank1_drag = max(0.0, -rank1_residual)
        dictionary_drag = max(0.0, -dictionary_residual)
        rows.append({
            **metadata,
            "full_outside_delta_to_stress": full_delta,
            "rank1_reconstructed_outside_delta": rank1_delta,
            "rank1_residual_after_row_sum": rank1_residual,
            "rank1_residual_drag": rank1_drag,
            "rank1_residual_drag_to_rank1_ratio": (
                rank1_drag / rank1_delta if rank1_delta > 0 else math.inf),
            "dictionary_reconstructed_outside_delta": dictionary_delta,
            "dictionary_residual_after_row_sum": dictionary_residual,
            "dictionary_residual_drag": dictionary_drag,
            "dictionary_residual_drag_to_dictionary_ratio": (
                dictionary_drag / dictionary_delta
                if dictionary_delta > 0 else math.inf),
            "dictionary_delta_to_full_delta_ratio": (
                dictionary_delta / full_delta if full_delta else math.inf),
        })

    if not rows:
        raise AssertionError("no held-out clear rows")

    reference_high_drag = {
        row["target"] for row in rows
        if row["rank1_residual_drag_to_rank1_ratio"]
        >= HIGH_DRAG_RATIO_THRESHOLD
    }
    rank1_rows_by_drag = tuple(sorted(
        rows,
        key=lambda row: (
            row["rank1_residual_drag_to_rank1_ratio"],
            row["rank1_residual_drag"],
            -row["target"]),
        reverse=True))
    dictionary_rows_by_drag = tuple(sorted(
        rows,
        key=lambda row: (
            row["dictionary_residual_drag_to_dictionary_ratio"],
            row["dictionary_residual_drag"],
            -row["target"]),
        reverse=True))
    top_k = len(reference_high_drag)
    predicted_high_drag = {
        row["target"] for row in dictionary_rows_by_drag[:top_k]
    } if top_k else set()
    overlap = reference_high_drag & predicted_high_drag
    dictionary_nonpositive = tuple(
        row for row in rows
        if row["dictionary_reconstructed_outside_delta"] <= 0)
    rank1_nonpositive = tuple(
        row for row in rows
        if row["rank1_reconstructed_outside_delta"] <= 0)
    dictionary_cap_failures = tuple(
        row for row in rows
        if row["dictionary_residual_drag_to_dictionary_ratio"] > CAP_TO_TEST)
    rank1_cap_failures = tuple(
        row for row in rows
        if row["rank1_residual_drag_to_rank1_ratio"] > CAP_TO_TEST)
    exact_nonpositive = tuple(
        row for row in rows if row["full_outside_delta_to_stress"] <= 0)

    passes_holdout_signal_gate = (
        len(dictionary_nonpositive) == 0
        and len(dictionary_cap_failures) == 0
        and (
            not reference_high_drag
            or len(overlap) >= math.ceil(0.6 * len(reference_high_drag))))

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_lift_project_dictionary_audit": str(
            DICTIONARY_SOURCE.relative_to(ROOT)),
        "source_octave_rank1_audit": str(RANK1_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite held-out low-frequency lift diagnostic only; the "
            "full_low_frequency_lift vector is frozen from the prior audit "
            "and replayed on fresh windows without re-projection.  This "
            "proves no lifted dictionary theorem, residual-bound theorem, "
            "signed projection theorem, or Goldbach theorem."),
        "candidate": (
            "The prior full_low_frequency_lift partial signal might survive "
            "fresh q286 windows as a local hole-tightening tool."),
        "mechanism": (
            "Reuse the frozen low-frequency dictionary vector from "
            "q286-lift-project-dictionary-audit.json.  Recompute exact q286 "
            "signed channel profiles on six fresh held-out windows, subtract "
            "stress row 1222142 on the same 17 outside channels, and compare "
            "exact outside deltas, frozen Octave rank-1 replay, and frozen "
            "low-frequency dictionary replay."),
        "prediction": (
            "A surviving tool should keep reconstructed outside deltas "
            "positive, avoid the 0.75 residual-drag cap failure, and recover "
            "most frozen-rank1 high-drag rows at the same k without refitting."),
        "falsifier": (
            "Any nonpositive low-frequency reconstructed outside delta, any "
            "held-out 0.75 cap failure, or poor overlap with the frozen-rank1 "
            "high-drag set demotes the low-frequency lift from partial signal "
            "to training-window artifact for this role."),
        "novelty_label": "new-to-this-task",
        "window_specs": WINDOW_SPECS,
        "stress_target": STRESS_TARGET,
        "heldout_target_count": len(targets),
        "heldout_clear_count": len(rows),
        "heldout_deficit_count": len(deficit_rows),
        "heldout_deficit_targets": tuple(row["target"] for row in deficit_rows),
        "window_summaries": window_summaries,
        "outside_labels": outside_labels,
        "frozen_dictionary_id": dictionary["id"],
        "frozen_dictionary_rank1_cosine_on_training": (
            dictionary["rank1_direction_cosine"]),
        "frozen_dictionary_high_drag_overlap_on_training": (
            dictionary["high_drag_overlap_count_at_reference_k"]),
        "frozen_dictionary_vector": tuple(
            float(value) for value in dictionary_vector),
        "reference_rank1_vector": tuple(float(value) for value in rank1_vector),
        "high_drag_ratio_threshold": HIGH_DRAG_RATIO_THRESHOLD,
        "reference_rank1_high_drag_targets": tuple(sorted(reference_high_drag)),
        "reference_rank1_high_drag_count": len(reference_high_drag),
        "dictionary_top_k_high_drag_targets": tuple(
            row["target"] for row in dictionary_rows_by_drag[:top_k]),
        "high_drag_overlap_count_at_reference_k": len(overlap),
        "high_drag_recall_at_reference_k": (
            len(overlap) / len(reference_high_drag)
            if reference_high_drag else None),
        "high_drag_precision_at_reference_k": (
            len(overlap) / len(predicted_high_drag)
            if predicted_high_drag else None),
        "exact_nonpositive_outside_delta_count": len(exact_nonpositive),
        "exact_nonpositive_outside_delta_targets": tuple(
            row["target"] for row in exact_nonpositive[:40]),
        "rank1_nonpositive_delta_count": len(rank1_nonpositive),
        "rank1_nonpositive_delta_targets": tuple(
            row["target"] for row in rank1_nonpositive[:40]),
        "dictionary_nonpositive_delta_count": len(dictionary_nonpositive),
        "dictionary_nonpositive_delta_targets": tuple(
            row["target"] for row in dictionary_nonpositive[:40]),
        "rank1_cap_record": cap_record(
            rows, "rank1_residual_drag_to_rank1_ratio", CAP_TO_TEST),
        "dictionary_cap_record": cap_record(
            rows, "dictionary_residual_drag_to_dictionary_ratio", CAP_TO_TEST),
        "full_outside_delta_summary": finite_summary(
            row["full_outside_delta_to_stress"] for row in rows),
        "rank1_reconstructed_delta_summary": finite_summary(
            row["rank1_reconstructed_outside_delta"] for row in rows),
        "rank1_residual_drag_ratio_summary": finite_summary(
            row["rank1_residual_drag_to_rank1_ratio"] for row in rows),
        "dictionary_reconstructed_delta_summary": finite_summary(
            row["dictionary_reconstructed_outside_delta"] for row in rows),
        "dictionary_residual_drag_ratio_summary": finite_summary(
            row["dictionary_residual_drag_to_dictionary_ratio"] for row in rows),
        "dictionary_delta_to_full_delta_ratio_summary": finite_summary(
            row["dictionary_delta_to_full_delta_ratio"] for row in rows),
        "minimum_full_outside_delta": min_record(
            rows, "full_outside_delta_to_stress"),
        "minimum_rank1_reconstructed_delta": min_record(
            rows, "rank1_reconstructed_outside_delta"),
        "minimum_dictionary_reconstructed_delta": min_record(
            rows, "dictionary_reconstructed_outside_delta"),
        "maximum_rank1_residual_drag_ratio": max_record(
            rows, "rank1_residual_drag_to_rank1_ratio"),
        "maximum_dictionary_residual_drag_ratio": max_record(
            rows, "dictionary_residual_drag_to_dictionary_ratio"),
        "rows_by_rank1_residual_drag_ratio": rank1_rows_by_drag[:80],
        "rows_by_dictionary_residual_drag_ratio": dictionary_rows_by_drag[:80],
        "summary": {
            "result": (
                "The frozen low-frequency lift is replayed on fresh q286 "
                "windows as a held-out test of the prior partial signal."),
            "theorem_boundary": (
                "A pass is finite survival only; a failure demotes this "
                "specific low-frequency lift and does not refute richer "
                "target-residue or number-field lifts."),
        },
        "interpretation": {
            "passes_holdout_signal_gate": passes_holdout_signal_gate,
            "next_if_passes": (
                "Promote only as a finite held-out tool: freeze a second "
                "denominator or add target-residue/splitting features before "
                "searching for a theorem statement."),
            "next_if_fails": (
                "Demote full_low_frequency_lift as a training-window artifact "
                "for q286 rank1 residual drag and return to row-dependent "
                "arithmetic balance or larger signed cones."),
        },
        "low_frequency_lift_holdout_measured": True,
        "predeclared_low_frequency_lift_passes_holdout_signal_gate": (
            passes_holdout_signal_gate),
        "lifted_dictionary_theorem_proved": False,
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
