"""Fit and hold out a q286 low-frequency LP cone certificate candidate.

Kevin asked whether linear programming should be used.  This receipt makes
that precise without promoting optimization to proof: solve a bounded LP in
the same predeclared low-frequency channel basis that survived holdout, enforce
the residual-drag cap inequalities on the original training denominator, then
freeze the vector and replay it on two heldout denominators.

This is finite optimization evidence only.  It proves no LP certificate
theorem, low-frequency theorem, signed projection theorem, or Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
DICTIONARY_SOURCE = ROOT / "evidence" / "q286-lift-project-dictionary-audit.json"
FULL_WINDOW_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-full-window-audit.json")
LOW_HOLDOUT_SOURCE = ROOT / "evidence" / "q286-low-frequency-lift-holdout.json"
HORIZON_SOURCE = ROOT / "evidence" / "q286-low-frequency-lift-horizon-holdout.json"
OUT = ROOT / "evidence" / "q286-low-frequency-lp-cone-audit.json"
STRESS_TARGET = 1222142
HIGH_DRAG_RATIO_THRESHOLD = 0.2
CAP_TO_TEST = 0.75
L1_MULTIPLIERS = (1.0, 1.5, 2.0, 4.0, 8.0)
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_above_floor_holdout_census_receipt,
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)


CHANNEL_FEATURE_NAMES = (
    "constant",
    "cos_a_1", "sin_a_1", "cos_a_2", "sin_a_2",
    "cos_b_1", "sin_b_1", "cos_b_2", "sin_b_2",
    "cos_sum_1", "sin_sum_1", "cos_diff_1", "sin_diff_1",
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


def channel_features(label):
    a, b = label
    theta_a = 2.0 * math.pi * a / 10.0
    theta_b = 2.0 * math.pi * b / 12.0
    return np.asarray([
        1.0,
        math.cos(theta_a), math.sin(theta_a),
        math.cos(2.0 * theta_a), math.sin(2.0 * theta_a),
        math.cos(theta_b), math.sin(theta_b),
        math.cos(2.0 * theta_b), math.sin(2.0 * theta_b),
        math.cos(theta_a + theta_b), math.sin(theta_a + theta_b),
        math.cos(theta_a - theta_b), math.sin(theta_a - theta_b),
    ], dtype=np.float64)


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


def collect_targets(window_specs, role):
    targets = []
    metadata = {}
    seen = set()
    for window_index, (start, count) in enumerate(window_specs):
        census = q286_first_three_dominant_mode_above_floor_holdout_census_receipt(
            start=int(start), target_count=int(count), target_step=2,
            closest_count=min(20, int(count)), include_rows=True)
        for row in census["target_rows"]:
            target = int(row["target"])
            if target in seen:
                continue
            seen.add(target)
            targets.append(target)
            metadata[target] = {
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
    return tuple(targets), metadata


def build_rows(targets, metadata, profile, outside_labels, stress_contributions,
               rank1_vector, low_frequency_effective_vector):
    rows = []
    deficits = []
    rank1_sum = float(np.sum(rank1_vector))
    for target in targets:
        profile_row = profile["target_rows"][target]
        if not profile_row["dominant_floor_passes"]:
            deficits.append(metadata[target])
            continue
        contributions = contribution_map(profile_row)
        delta = np.asarray([
            contributions[label] - stress_contributions[label]
            for label in outside_labels
        ], dtype=np.float64)
        full_delta = float(np.sum(delta))
        rank1_delta = float(np.dot(delta, rank1_vector) * rank1_sum)
        low_delta = float(np.dot(delta, low_frequency_effective_vector))
        rows.append({
            **metadata[target],
            "outside_delta_vector": delta,
            "full_outside_delta_to_stress": full_delta,
            "rank1_reconstructed_outside_delta": rank1_delta,
            "rank1_residual_drag_to_rank1_ratio": (
                max(0.0, -(full_delta - rank1_delta)) / rank1_delta
                if rank1_delta > 0 else math.inf),
            "low_frequency_reconstructed_outside_delta": low_delta,
            "low_frequency_residual_drag_to_low_frequency_ratio": (
                max(0.0, -(full_delta - low_delta)) / low_delta
                if low_delta > 0 else math.inf),
        })
    return tuple(rows), tuple(deficits)


def solve_lp(rows, feature_matrix, target_sum, base_l1, multiplier):
    row_feature = np.asarray([
        row["outside_delta_vector"] @ feature_matrix for row in rows
    ], dtype=np.float64)
    feature_sums = np.sum(feature_matrix, axis=0)
    feature_count = feature_matrix.shape[1]
    variable_count = 2 * feature_count + 1
    gamma_index = variable_count - 1

    objective = np.zeros(variable_count, dtype=np.float64)
    objective[gamma_index] = -1.0

    a_ub = []
    b_ub = []
    for row, features in zip(rows, row_feature):
        # reconstructed >= gamma  ->  -features*c+ + features*c- + gamma <= 0
        lower = np.zeros(variable_count, dtype=np.float64)
        lower[:feature_count] = -features
        lower[feature_count:2 * feature_count] = features
        lower[gamma_index] = 1.0
        a_ub.append(lower)
        b_ub.append(0.0)

        # reconstructed <= 4*full_delta - gamma
        upper = np.zeros(variable_count, dtype=np.float64)
        upper[:feature_count] = features
        upper[feature_count:2 * feature_count] = -features
        upper[gamma_index] = 1.0
        a_ub.append(upper)
        b_ub.append(4.0 * row["full_outside_delta_to_stress"])

    l1 = np.zeros(variable_count, dtype=np.float64)
    l1[:2 * feature_count] = 1.0
    a_ub.append(l1)
    b_ub.append(base_l1 * multiplier)

    equality = np.zeros(variable_count, dtype=np.float64)
    equality[:feature_count] = feature_sums
    equality[feature_count:2 * feature_count] = -feature_sums

    result = linprog(
        objective,
        A_ub=np.asarray(a_ub, dtype=np.float64),
        b_ub=np.asarray(b_ub, dtype=np.float64),
        A_eq=np.asarray([equality], dtype=np.float64),
        b_eq=np.asarray([target_sum], dtype=np.float64),
        bounds=[(0.0, None)] * (2 * feature_count) + [(None, None)],
        method="highs",
    )
    record = {
        "l1_multiplier": float(multiplier),
        "l1_bound": float(base_l1 * multiplier),
        "solver_success": bool(result.success),
        "solver_status": int(result.status),
        "solver_message": result.message,
        "objective_minimum_training_slack": None,
    }
    if not result.success:
        return record, None, None
    coeff = result.x[:feature_count] - result.x[feature_count:2 * feature_count]
    vector = feature_matrix @ coeff
    record.update({
        "objective_minimum_training_slack": float(result.x[gamma_index]),
        "coefficient_l1": float(np.sum(np.abs(coeff))),
        "coefficient_l2": float(np.linalg.norm(coeff)),
        "coefficient_linf": float(np.max(np.abs(coeff))),
        "effective_vector_sum": float(np.sum(vector)),
    })
    return record, coeff, vector


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


def main():
    dictionary_payload = json.loads(
        DICTIONARY_SOURCE.read_text(encoding="utf-8"))
    full_payload = json.loads(FULL_WINDOW_SOURCE.read_text(encoding="utf-8"))
    low_holdout_payload = json.loads(
        LOW_HOLDOUT_SOURCE.read_text(encoding="utf-8"))
    horizon_payload = json.loads(HORIZON_SOURCE.read_text(encoding="utf-8"))
    dictionary = next(
        row for row in dictionary_payload["dictionary_rows"]
        if row["id"] == "full_low_frequency_lift")
    outside_labels = tuple(
        label_tuple(label) for label in dictionary_payload["outside_labels"])
    rank1_vector = np.asarray(
        dictionary_payload["reference_rank1_vector"], dtype=np.float64)
    low_frequency_vector = np.asarray(
        dictionary["dictionary_vector"], dtype=np.float64)
    low_frequency_effective_vector = (
        float(np.sum(low_frequency_vector)) * low_frequency_vector)
    feature_matrix = np.asarray(
        [channel_features(label) for label in outside_labels],
        dtype=np.float64)
    base_coeff, *_ = np.linalg.lstsq(
        feature_matrix, low_frequency_effective_vector, rcond=None)
    base_l1 = float(np.sum(np.abs(base_coeff)))
    target_sum = float(np.sum(low_frequency_effective_vector))

    training_window_specs = tuple(
        tuple(int(value) for value in spec)
        for spec in full_payload["window_specs"])
    heldout_window_specs = tuple(
        tuple(int(value) for value in spec)
        for spec in low_holdout_payload["window_specs"])
    horizon_window_specs = tuple(
        tuple(int(value) for value in spec)
        for spec in horizon_payload["window_specs"])
    train_targets, train_meta = collect_targets(training_window_specs, "training")
    heldout_targets, heldout_meta = collect_targets(heldout_window_specs, "heldout")
    horizon_targets, horizon_meta = collect_targets(horizon_window_specs, "horizon")

    sample_targets = tuple(dict.fromkeys(
        (STRESS_TARGET,) + train_targets + heldout_targets + horizon_targets))
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=sample_targets, dominant_modes=(1, 2),
        tail_threshold=.3, top_channel_count=40)
    stress_contributions = contribution_map(
        profile["target_rows"][STRESS_TARGET])

    train_rows, train_deficits = build_rows(
        train_targets, train_meta, profile, outside_labels,
        stress_contributions, rank1_vector, low_frequency_effective_vector)
    heldout_rows, heldout_deficits = build_rows(
        heldout_targets, heldout_meta, profile, outside_labels,
        stress_contributions, rank1_vector, low_frequency_effective_vector)
    horizon_rows, horizon_deficits = build_rows(
        horizon_targets, horizon_meta, profile, outside_labels,
        stress_contributions, rank1_vector, low_frequency_effective_vector)
    if tuple(row["target"] for row in train_deficits) != (STRESS_TARGET,):
        raise AssertionError("training deficit set drifted")
    if heldout_deficits or horizon_deficits:
        raise AssertionError("heldout or horizon deficit set drifted")

    lp_records = []
    successful = []
    for multiplier in L1_MULTIPLIERS:
        record, coeff, vector = solve_lp(
            train_rows, feature_matrix, target_sum, base_l1, multiplier)
        if vector is not None:
            train_scored = score_rows(train_rows, vector, "lp")
            record["training_summary"] = model_summary(train_scored, "lp")
            record["rank1_direction_cosine"] = cosine(vector, rank1_vector)
            record["low_frequency_direction_cosine"] = cosine(
                vector, low_frequency_effective_vector)
            successful.append((record, coeff, vector))
        lp_records.append(record)
    if not successful:
        selected_record = None
        selected_coeff = None
        selected_vector = None
    else:
        selected_record, selected_coeff, selected_vector = max(
            successful,
            key=lambda item: (
                item[0]["objective_minimum_training_slack"],
                -item[0]["l1_multiplier"]))

    if selected_vector is None:
        heldout_summary = None
        horizon_summary = None
        selected_scored_train = ()
        selected_scored_heldout = ()
        selected_scored_horizon = ()
        lp_passes_holdouts = False
    else:
        selected_scored_train = score_rows(train_rows, selected_vector, "lp")
        selected_scored_heldout = score_rows(
            heldout_rows, selected_vector, "lp")
        selected_scored_horizon = score_rows(
            horizon_rows, selected_vector, "lp")
        selected_record["training_summary"] = model_summary(
            selected_scored_train, "lp")
        heldout_summary = model_summary(selected_scored_heldout, "lp")
        horizon_summary = model_summary(selected_scored_horizon, "lp")
        lp_passes_holdouts = (
            heldout_summary["nonpositive_delta_count"] == 0
            and horizon_summary["nonpositive_delta_count"] == 0
            and heldout_summary["cap_record"]["failing_count"] == 0
            and horizon_summary["cap_record"]["failing_count"] == 0)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_lift_project_dictionary_audit": str(
            DICTIONARY_SOURCE.relative_to(ROOT)),
        "source_full_window_audit": str(FULL_WINDOW_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lift_holdout": str(
            LOW_HOLDOUT_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lift_horizon_holdout": str(
            HORIZON_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite LP cone audit only; it fits on the original q286 "
            "full-window denominator and replays the selected vector on two "
            "heldout denominators.  This proves no LP certificate theorem, "
            "low-frequency theorem, residual-bound theorem, signed projection "
            "theorem, or Goldbach theorem."),
        "candidate": (
            "A bounded LP in the low-frequency channel basis may find a static "
            "signed-cone vector whose reconstructed outside deltas satisfy the "
            "residual-drag cap more robustly than the frozen projection vector."),
        "mechanism": (
            "Use the same 13 low-frequency channel features as "
            "full_low_frequency_lift.  Fix total effective vector sum to the "
            "frozen low-frequency replay scale, bound coefficient L1 size by "
            "multiples of the frozen vector's least-squares coefficient L1, "
            "and maximize the minimum training slack in "
            "0 < reconstructed_delta < 4*exact_outside_delta."),
        "prediction": (
            "If the low-frequency hole can be converted into a finite cone "
            "certificate, the LP-selected vector should improve training slack "
            "without introducing nonpositive deltas or 0.75 cap failures on "
            "the heldout and horizon denominators."),
        "falsifier": (
            "If no bounded L1 LP is feasible with positive slack, or if the "
            "selected vector fails positivity or the 0.75 cap on either "
            "heldout denominator, demote this static low-frequency LP cone "
            "as a stable q286 certificate route."),
        "novelty_label": "new-to-this-task",
        "training_window_specs": training_window_specs,
        "heldout_window_specs": heldout_window_specs,
        "horizon_window_specs": horizon_window_specs,
        "stress_target": STRESS_TARGET,
        "outside_labels": outside_labels,
        "channel_feature_names": CHANNEL_FEATURE_NAMES,
        "l1_multipliers": L1_MULTIPLIERS,
        "base_low_frequency_coefficient_l1": base_l1,
        "fixed_effective_vector_sum": target_sum,
        "training_clear_count": len(train_rows),
        "training_deficit_targets": tuple(
            row["target"] for row in train_deficits),
        "heldout_clear_count": len(heldout_rows),
        "horizon_clear_count": len(horizon_rows),
        "lp_candidate_records": lp_records,
        "selected_lp_record": selected_record,
        "selected_lp_coefficients": (
            None if selected_coeff is None
            else tuple(float(value) for value in selected_coeff)),
        "selected_lp_effective_vector": (
            None if selected_vector is None
            else tuple(float(value) for value in selected_vector)),
        "selected_lp_rank1_direction_cosine": (
            None if selected_vector is None else cosine(selected_vector, rank1_vector)),
        "selected_lp_low_frequency_direction_cosine": (
            None if selected_vector is None
            else cosine(selected_vector, low_frequency_effective_vector)),
        "heldout_summary": heldout_summary,
        "horizon_summary": horizon_summary,
        "selected_training_rows_by_residual_drag_ratio": (
            tuple(selected_record["training_summary"]["rows_by_residual_drag_ratio"])
            if selected_record else ()),
        "selected_heldout_rows_by_residual_drag_ratio": (
            tuple(heldout_summary["rows_by_residual_drag_ratio"])
            if heldout_summary else ()),
        "selected_horizon_rows_by_residual_drag_ratio": (
            tuple(horizon_summary["rows_by_residual_drag_ratio"])
            if horizon_summary else ()),
        "interpretation": {
            "lp_static_cone_passes_holdouts": lp_passes_holdouts,
            "next_if_passes": (
                "Treat the LP vector as a finite cone-certificate candidate "
                "only.  The next theorem target is a non-optimized arithmetic "
                "description of the same inequalities or a proof that the "
                "basis constraints imply them uniformly."),
            "next_if_fails": (
                "Close the static low-frequency LP cone shortcut and move to "
                "row-dependent signed cones or actual character-sum magnitude "
                "constraints."),
        },
        "low_frequency_lp_cone_audit_measured": True,
        "static_lp_cone_certificate_survives_two_holdouts": lp_passes_holdouts,
        "lp_certificate_theorem_proved": False,
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
