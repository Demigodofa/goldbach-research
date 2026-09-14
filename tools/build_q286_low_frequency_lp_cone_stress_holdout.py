"""Replay the frozen q286 low-frequency LP cone on far stress windows.

The previous LP cone audit fit a vector only on the original q286 training
denominator, then froze it and replayed it on two heldout denominators.  This
receipt does not refit.  It takes that selected LP effective vector and tests
it on farther predeclared q286 windows.

This is finite optimization evidence only.  It proves no LP certificate
theorem, interpolation theorem, residual-bound theorem, signed projection
theorem, or Goldbach theorem.
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
LP_SOURCE = ROOT / "evidence" / "q286-low-frequency-lp-cone-audit.json"
OUT = ROOT / "evidence" / "q286-low-frequency-lp-cone-stress-holdout.json"
STRESS_TARGET = 1222142
WINDOW_SPECS = (
    (6000000, 101),
    (8000000, 101),
    (10000000, 101),
    (12000000, 101),
    (16000000, 101),
    (20000000, 101),
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


def cosine(a, b):
    a = np.asarray(a, dtype=np.float64).reshape(-1)
    b = np.asarray(b, dtype=np.float64).reshape(-1)
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    return None if denom == 0.0 else float(np.dot(a, b) / denom)


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
                "window_role": "far_stress_holdout",
                "target_mod_286": int(row["target_mod_286"]),
                "target_mod_10010": target % 10010,
                "absolute_above_floor_signed_surplus": float(
                    row["absolute_above_floor_signed_surplus"]),
                "dominant_sum_to_principal": float(
                    row["dominant_sum_to_principal"]),
                "dominant_floor_passes": bool(row["dominant_floor_passes"]),
            }
            metadata[target] = compact
            window_rows.append(compact)
        window_summaries.append({
            "window_index": int(window_index),
            "window_start": int(start),
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
    return tuple(targets), metadata, tuple(window_summaries)


def score_rows(rows, effective_vector, prefix):
    scored = []
    for row in rows:
        full_delta = row["full_outside_delta_to_stress"]
        reconstructed = float(row["outside_delta_vector"] @ effective_vector)
        residual = full_delta - reconstructed
        drag = max(0.0, -residual)
        scored.append({
            "target": row["target"],
            "target_mod_286": row["target_mod_286"],
            "target_mod_10010": row["target_mod_10010"],
            "window_index": row["window_index"],
            "window_start": row["window_start"],
            "window_role": row["window_role"],
            "full_outside_delta_to_stress": full_delta,
            f"{prefix}_reconstructed_outside_delta": reconstructed,
            f"{prefix}_residual_after_row_sum": residual,
            f"{prefix}_residual_drag": drag,
            f"{prefix}_residual_drag_ratio": (
                drag / reconstructed if reconstructed > 0 else math.inf),
            f"{prefix}_delta_to_full_delta_ratio": (
                reconstructed / full_delta if full_delta else math.inf),
            "rank1_residual_drag_to_rank1_ratio": (
                row["rank1_residual_drag_to_rank1_ratio"]),
            "low_frequency_residual_drag_to_low_frequency_ratio": (
                row["low_frequency_residual_drag_to_low_frequency_ratio"]),
        })
    return tuple(scored)


def model_summary(rows, prefix):
    nonpositive = tuple(
        row for row in rows if row[f"{prefix}_reconstructed_outside_delta"] <= 0)
    cap = cap_record(rows, f"{prefix}_residual_drag_ratio", CAP_TO_TEST)
    rows_by_drag = tuple(sorted(
        rows,
        key=lambda row: (
            row[f"{prefix}_residual_drag_ratio"],
            row[f"{prefix}_residual_drag"],
            -row["target"]),
        reverse=True))
    reference_high_drag = {
        row["target"] for row in rows
        if row["rank1_residual_drag_to_rank1_ratio"]
        >= HIGH_DRAG_RATIO_THRESHOLD
    }
    top_k = len(reference_high_drag)
    predicted_high_drag = {
        row["target"] for row in rows_by_drag[:top_k]
    } if top_k else set()
    overlap = reference_high_drag & predicted_high_drag
    return {
        "clear_count": len(rows),
        "reconstructed_delta_summary": finite_summary(
            row[f"{prefix}_reconstructed_outside_delta"] for row in rows),
        "residual_drag_ratio_summary": finite_summary(
            row[f"{prefix}_residual_drag_ratio"] for row in rows),
        "delta_to_full_delta_ratio_summary": finite_summary(
            row[f"{prefix}_delta_to_full_delta_ratio"] for row in rows),
        "nonpositive_delta_count": len(nonpositive),
        "nonpositive_delta_targets": tuple(row["target"] for row in nonpositive),
        "cap_record": cap,
        "reference_high_drag_count": len(reference_high_drag),
        "reference_high_drag_targets": tuple(sorted(reference_high_drag)),
        "top_k_high_drag_targets": tuple(
            row["target"] for row in rows_by_drag[:top_k]),
        "high_drag_overlap_count_at_reference_k": len(overlap),
        "high_drag_recall_at_reference_k": (
            len(overlap) / len(reference_high_drag)
            if reference_high_drag else None),
        "minimum_reconstructed_delta": min_record(
            rows, f"{prefix}_reconstructed_outside_delta"),
        "maximum_residual_drag_ratio": max_record(
            rows, f"{prefix}_residual_drag_ratio"),
        "rows_by_residual_drag_ratio": rows_by_drag[:40],
    }


def build_rows(targets, metadata, profile, outside_labels,
               stress_contributions, rank1_vector,
               low_frequency_effective_vector):
    rows = []
    deficit_rows = []
    rank1_sum = float(np.sum(rank1_vector))
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
        full_delta = float(np.sum(outside_delta_vector))
        rank1_delta = float(np.dot(outside_delta_vector, rank1_vector)
                            * rank1_sum)
        low_frequency_delta = float(
            np.dot(outside_delta_vector, low_frequency_effective_vector))
        rows.append({
            **metadata[target],
            "outside_delta_vector": outside_delta_vector,
            "full_outside_delta_to_stress": full_delta,
            "rank1_reconstructed_outside_delta": rank1_delta,
            "rank1_residual_drag_to_rank1_ratio": (
                max(0.0, -(full_delta - rank1_delta)) / rank1_delta
                if rank1_delta > 0 else math.inf),
            "low_frequency_reconstructed_outside_delta": low_frequency_delta,
            "low_frequency_residual_drag_to_low_frequency_ratio": (
                max(0.0, -(full_delta - low_frequency_delta))
                / low_frequency_delta
                if low_frequency_delta > 0 else math.inf),
        })
    return tuple(rows), tuple(deficit_rows)


def main():
    dictionary_payload = json.loads(
        DICTIONARY_SOURCE.read_text(encoding="utf-8"))
    lp_payload = json.loads(LP_SOURCE.read_text(encoding="utf-8"))
    dictionary = selected_dictionary(
        dictionary_payload, "full_low_frequency_lift")
    outside_labels = tuple(
        label_tuple(label) for label in dictionary_payload["outside_labels"])
    rank1_vector = np.asarray(
        dictionary_payload["reference_rank1_vector"], dtype=np.float64)
    low_frequency_vector = np.asarray(
        dictionary["dictionary_vector"], dtype=np.float64)
    low_frequency_effective_vector = (
        float(np.sum(low_frequency_vector)) * low_frequency_vector)
    lp_effective_vector = np.asarray(
        lp_payload["selected_lp_effective_vector"], dtype=np.float64)
    if len(outside_labels) != 17:
        raise AssertionError("outside label count drifted")
    if lp_effective_vector.shape != (17,):
        raise AssertionError("selected LP vector shape drifted")

    targets, metadata, window_summaries = collect_targets()
    sample_targets = tuple(dict.fromkeys((STRESS_TARGET,) + targets))
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=sample_targets, dominant_modes=(1, 2),
        tail_threshold=.3, top_channel_count=40)
    stress_contributions = contribution_map(
        profile["target_rows"][STRESS_TARGET])
    rows, deficit_rows = build_rows(
        targets, metadata, profile, outside_labels, stress_contributions,
        rank1_vector, low_frequency_effective_vector)
    if not rows:
        raise AssertionError("no far stress clear rows")

    scored_lp = score_rows(rows, lp_effective_vector, "lp")
    lp_summary = model_summary(scored_lp, "lp")
    rank1_nonpositive = tuple(
        row for row in rows if row["rank1_reconstructed_outside_delta"] <= 0)
    low_frequency_nonpositive = tuple(
        row for row in rows
        if row["low_frequency_reconstructed_outside_delta"] <= 0)
    exact_nonpositive = tuple(
        row for row in rows if row["full_outside_delta_to_stress"] <= 0)
    rank1_cap = cap_record(
        rows, "rank1_residual_drag_to_rank1_ratio", CAP_TO_TEST)
    low_frequency_cap = cap_record(
        rows, "low_frequency_residual_drag_to_low_frequency_ratio",
        CAP_TO_TEST)
    stress_gate_passes = (
        len(deficit_rows) == 0
        and len(exact_nonpositive) == 0
        and len(rank1_nonpositive) == 0
        and len(low_frequency_nonpositive) == 0
        and lp_summary["nonpositive_delta_count"] == 0
        and rank1_cap["failing_count"] == 0
        and low_frequency_cap["failing_count"] == 0
        and lp_summary["cap_record"]["failing_count"] == 0)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_low_frequency_lp_cone_audit": str(
            LP_SOURCE.relative_to(ROOT)),
        "source_lift_project_dictionary_audit": str(
            DICTIONARY_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite far stress holdout only; the LP vector was fit in "
            "evidence/q286-low-frequency-lp-cone-audit.json and is replayed "
            "here without refit. This proves no LP certificate theorem, "
            "Riesz-Thorin/interpolation theorem, residual-bound theorem, "
            "signed projection theorem, or Goldbach theorem."),
        "candidate": (
            "The frozen low-frequency LP cone vector remains a finite "
            "residual-drag cap certificate candidate on far q286 stress "
            "windows well beyond the prior 5,000,000 horizon."),
        "mechanism": (
            "Use the selected LP effective vector from the bounded "
            "low-frequency Fourier band on C10 x C12. Recompute exact signed "
            "channel profiles on six farther windows, subtract the same "
            "stress row 1222142, and test positivity plus the 0.75 "
            "residual-drag cap without changing any coefficients."),
        "prediction": (
            "If the finite cone is not just local to the earlier denominators, "
            "all far stress rows should keep positive reconstructed deltas and "
            "zero 0.75 cap failures under the frozen LP vector."),
        "falsifier": (
            "Any dominant-floor deficit, nonpositive exact/rank1/"
            "low-frequency/LP reconstructed delta, or 0.75 cap failure "
            "demotes the static LP cone as a stable q286 certificate route."),
        "riesz_thorin_note": (
            "Riesz-Thorin remains theorem-shaping only here: the finite LP "
            "shadow suggests an interpolation-style norm control between "
            "crude L1/triangle and Fourier/L2 endpoints, but no actual "
            "operator endpoint bounds are proved by this receipt."),
        "novelty_label": "new-to-this-task",
        "window_specs": WINDOW_SPECS,
        "window_summaries": window_summaries,
        "stress_target": STRESS_TARGET,
        "far_stress_target_count": len(targets),
        "far_stress_clear_count": len(rows),
        "far_stress_deficit_count": len(deficit_rows),
        "far_stress_deficit_targets": tuple(
            row["target"] for row in deficit_rows),
        "outside_labels": outside_labels,
        "selected_lp_source_l1_multiplier": (
            lp_payload["selected_lp_record"]["l1_multiplier"]),
        "selected_lp_source_training_slack": (
            lp_payload["selected_lp_record"][
                "objective_minimum_training_slack"]),
        "selected_lp_rank1_direction_cosine": cosine(
            lp_effective_vector, rank1_vector),
        "selected_lp_low_frequency_direction_cosine": cosine(
            lp_effective_vector, low_frequency_effective_vector),
        "exact_nonpositive_outside_delta_count": len(exact_nonpositive),
        "exact_nonpositive_outside_delta_targets": tuple(
            row["target"] for row in exact_nonpositive),
        "rank1_nonpositive_delta_count": len(rank1_nonpositive),
        "rank1_nonpositive_delta_targets": tuple(
            row["target"] for row in rank1_nonpositive),
        "low_frequency_nonpositive_delta_count": len(low_frequency_nonpositive),
        "low_frequency_nonpositive_delta_targets": tuple(
            row["target"] for row in low_frequency_nonpositive),
        "rank1_cap_record": rank1_cap,
        "low_frequency_cap_record": low_frequency_cap,
        "lp_summary": lp_summary,
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
        "selected_lp_rows_by_residual_drag_ratio": (
            lp_summary["rows_by_residual_drag_ratio"]),
        "interpretation": {
            "static_lp_cone_certificate_survives_far_stress_holdout": (
                stress_gate_passes),
            "next_if_passes": (
                "Keep the LP cone as finite certificate evidence and try to "
                "replace its fitted coefficients with an arithmetic cone or "
                "interpolation-style endpoint theorem."),
            "next_if_fails": (
                "Close the static LP cone shortcut and move to row-dependent "
                "signed cones or stronger character-sum constraints."),
        },
        "low_frequency_lp_cone_stress_holdout_measured": True,
        "static_lp_cone_certificate_survives_far_stress_holdout": (
            stress_gate_passes),
        "lp_certificate_theorem_proved": False,
        "riesz_thorin_interpolation_theorem_connected": False,
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
