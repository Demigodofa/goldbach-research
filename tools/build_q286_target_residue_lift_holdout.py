"""Train and hold out a target-residue q286 low-frequency tensor lift.

The prior heldout kept ``full_low_frequency_lift`` alive as a local tool but
not as a rank-1 explanation.  This receipt tests the next promised
representation shift: include predeclared target residue features from
``N mod 11`` and ``N mod 13`` before fitting, then freeze the coefficients and
score fresh heldout windows.

This is finite evidence only.  It proves no lifted dictionary theorem,
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
FULL_WINDOW_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-full-window-audit.json")
LOW_HOLDOUT_SOURCE = ROOT / "evidence" / "q286-low-frequency-lift-holdout.json"
OUT = ROOT / "evidence" / "q286-target-residue-lift-holdout.json"
STRESS_TARGET = 1222142
HIGH_DRAG_RATIO_THRESHOLD = 0.2
CAP_TO_TEST = 0.75
RIDGE_LAMBDA = 1e-4
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


def collect_targets(window_specs, role):
    targets = []
    target_metadata = {}
    seen = set()
    window_summaries = []
    for window_index, (start, count) in enumerate(window_specs):
        census = q286_first_three_dominant_mode_above_floor_holdout_census_receipt(
            start=int(start), target_count=int(count), target_step=2,
            closest_count=min(20, int(count)), include_rows=True)
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
                "target_mod_11": target % 11,
                "target_mod_13": target % 13,
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


def legendre_symbol(value, prime):
    residue = value % prime
    if residue == 0:
        return 0.0
    test = pow(residue, (prime - 1) // 2, prime)
    return -1.0 if test == prime - 1 else float(test)


def row_features(target):
    r11 = target % 11
    r13 = target % 13
    theta11 = 2.0 * math.pi * r11 / 11.0
    theta13 = 2.0 * math.pi * r13 / 13.0
    l11 = legendre_symbol(target, 11)
    l13 = legendre_symbol(target, 13)
    return np.asarray([
        1.0,
        math.cos(theta11), math.sin(theta11),
        math.cos(2.0 * theta11), math.sin(2.0 * theta11),
        l11,
        math.cos(theta13), math.sin(theta13),
        math.cos(2.0 * theta13), math.sin(2.0 * theta13),
        l13,
        l11 * l13,
        math.cos(theta11 + theta13), math.sin(theta11 + theta13),
        math.cos(theta11 - theta13), math.sin(theta11 - theta13),
    ], dtype=np.float64)


ROW_FEATURE_NAMES = (
    "constant",
    "cos_N_mod_11_1", "sin_N_mod_11_1",
    "cos_N_mod_11_2", "sin_N_mod_11_2",
    "legendre_N_11",
    "cos_N_mod_13_1", "sin_N_mod_13_1",
    "cos_N_mod_13_2", "sin_N_mod_13_2",
    "legendre_N_13",
    "legendre_product_N_11_13",
    "cos_sum_N_11_13", "sin_sum_N_11_13",
    "cos_diff_N_11_13", "sin_diff_N_11_13",
)


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


CHANNEL_FEATURE_NAMES = (
    "constant",
    "cos_a_1", "sin_a_1", "cos_a_2", "sin_a_2",
    "cos_b_1", "sin_b_1", "cos_b_2", "sin_b_2",
    "cos_sum_1", "sin_sum_1", "cos_diff_1", "sin_diff_1",
)


def build_rows(targets, metadata, profile, outside_labels, stress_contributions,
               rank1_vector, static_dictionary_vector):
    rank1_sum = float(np.sum(rank1_vector))
    static_sum = float(np.sum(static_dictionary_vector))
    rows = []
    deficits = []
    for target in targets:
        profile_row = profile["target_rows"][target]
        if not profile_row["dominant_floor_passes"]:
            deficits.append(metadata[target])
            continue
        contributions = contribution_map(profile_row)
        outside_delta_vector = np.asarray([
            contributions[label] - stress_contributions[label]
            for label in outside_labels
        ], dtype=np.float64)
        rank1_scalar = float(np.dot(outside_delta_vector, rank1_vector))
        rank1_vector_row = rank1_scalar * rank1_vector
        static_scalar = float(
            np.dot(outside_delta_vector, static_dictionary_vector))
        static_vector_row = static_scalar * static_dictionary_vector
        full_delta = float(np.sum(outside_delta_vector))
        rank1_delta = float(np.sum(rank1_vector_row))
        static_delta = float(np.sum(static_vector_row))
        rows.append({
            **metadata[target],
            "outside_delta_vector": outside_delta_vector,
            "full_outside_delta_to_stress": full_delta,
            "rank1_reference_delta_vector": rank1_vector_row,
            "rank1_reconstructed_outside_delta": rank1_delta,
            "rank1_residual_drag_to_rank1_ratio": (
                max(0.0, -(full_delta - rank1_delta)) / rank1_delta
                if rank1_delta > 0 else math.inf),
            "static_low_frequency_delta_vector": static_vector_row,
            "static_low_frequency_reconstructed_delta": static_delta,
            "static_low_frequency_residual_drag_ratio": (
                max(0.0, -(full_delta - static_delta)) / static_delta
                if static_delta > 0 else math.inf),
        })
    return tuple(rows), tuple(deficits)


def design_matrix(rows, outside_labels):
    channel_matrix = np.asarray(
        [channel_features(label) for label in outside_labels],
        dtype=np.float64)
    matrix_rows = []
    for row in rows:
        rf = row_features(row["target"])
        for channel_feature in channel_matrix:
            matrix_rows.append(np.kron(rf, channel_feature))
    return np.asarray(matrix_rows, dtype=np.float64)


def target_vector(rows):
    return np.asarray([
        value
        for row in rows
        for value in row["rank1_reference_delta_vector"]
    ], dtype=np.float64)


def fit_ridge(x, y, ridge_lambda):
    lhs = x.T @ x
    lhs += ridge_lambda * np.eye(lhs.shape[0], dtype=np.float64)
    rhs = x.T @ y
    return np.linalg.solve(lhs, rhs)


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


def cosine(a, b):
    a = np.asarray(a, dtype=np.float64).reshape(-1)
    b = np.asarray(b, dtype=np.float64).reshape(-1)
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    return None if denom == 0.0 else float(np.dot(a, b) / denom)


def cap_record(rows, ratio_key):
    failures = tuple(row for row in rows if row[ratio_key] > CAP_TO_TEST)
    return {
        "cap": CAP_TO_TEST,
        "passes": len(failures) == 0,
        "failing_count": len(failures),
        "failing_targets": tuple(row["target"] for row in failures[:40]),
        "maximum_excess": max(
            (row[ratio_key] - CAP_TO_TEST for row in failures), default=0.0),
    }


def add_model_predictions(rows, outside_labels, coefficients):
    channel_matrix = np.asarray(
        [channel_features(label) for label in outside_labels],
        dtype=np.float64)
    coefficient_matrix = np.asarray(coefficients, dtype=np.float64).reshape(
        len(ROW_FEATURE_NAMES), len(CHANNEL_FEATURE_NAMES))
    scored = []
    for row in rows:
        rf = row_features(row["target"])
        predicted_vector = channel_matrix @ (coefficient_matrix.T @ rf)
        predicted_delta = float(np.sum(predicted_vector))
        full_delta = float(row["full_outside_delta_to_stress"])
        residual = full_delta - predicted_delta
        drag = max(0.0, -residual)
        scored.append({
            "target": row["target"],
            "target_mod_11": row["target_mod_11"],
            "target_mod_13": row["target_mod_13"],
            "target_mod_286": row["target_mod_286"],
            "target_mod_10010": row["target_mod_10010"],
            "full_outside_delta_to_stress": full_delta,
            "rank1_reconstructed_outside_delta": (
                row["rank1_reconstructed_outside_delta"]),
            "rank1_residual_drag_to_rank1_ratio": (
                row["rank1_residual_drag_to_rank1_ratio"]),
            "static_low_frequency_reconstructed_delta": (
                row["static_low_frequency_reconstructed_delta"]),
            "static_low_frequency_residual_drag_ratio": (
                row["static_low_frequency_residual_drag_ratio"]),
            "target_residue_reconstructed_delta": predicted_delta,
            "target_residue_residual_after_row_sum": residual,
            "target_residue_residual_drag": drag,
            "target_residue_residual_drag_ratio": (
                drag / predicted_delta if predicted_delta > 0 else math.inf),
            "target_residue_delta_to_full_delta_ratio": (
                predicted_delta / full_delta if full_delta else math.inf),
        })
    return tuple(scored)


def model_summary(rows, predicted_matrix, reference_matrix, prefix):
    nonpositive = tuple(
        row for row in rows
        if row[f"{prefix}_reconstructed_delta"] <= 0)
    cap = cap_record(rows, f"{prefix}_residual_drag_ratio")
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
        "matrix_cosine_to_rank1_reference": cosine(
            predicted_matrix, reference_matrix),
        "reconstructed_delta_summary": finite_summary(
            row[f"{prefix}_reconstructed_delta"] for row in rows),
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
        "rows_by_residual_drag_ratio": rows_by_drag[:40],
    }


def static_summary(rows, matrix_key_prefix):
    prefix = matrix_key_prefix
    scored = []
    for row in rows:
        delta = row[f"{prefix}_reconstructed_delta"]
        full_delta = row["full_outside_delta_to_stress"]
        residual = full_delta - delta
        drag = max(0.0, -residual)
        scored.append({
            "target": row["target"],
            "target_mod_11": row["target_mod_11"],
            "target_mod_13": row["target_mod_13"],
            "target_mod_286": row["target_mod_286"],
            "target_mod_10010": row["target_mod_10010"],
            f"{prefix}_reconstructed_delta": delta,
            f"{prefix}_residual_drag": drag,
            f"{prefix}_residual_drag_ratio": (
                drag / delta if delta > 0 else math.inf),
            f"{prefix}_delta_to_full_delta_ratio": (
                delta / full_delta if full_delta else math.inf),
            "rank1_residual_drag_to_rank1_ratio": (
                row["rank1_residual_drag_to_rank1_ratio"]),
        })
    return tuple(scored)


def main():
    dictionary_payload = json.loads(
        DICTIONARY_SOURCE.read_text(encoding="utf-8"))
    full_payload = json.loads(FULL_WINDOW_SOURCE.read_text(encoding="utf-8"))
    holdout_payload = json.loads(LOW_HOLDOUT_SOURCE.read_text(encoding="utf-8"))
    dictionary = next(
        row for row in dictionary_payload["dictionary_rows"]
        if row["id"] == "full_low_frequency_lift")
    outside_labels = tuple(
        label_tuple(label) for label in dictionary_payload["outside_labels"])
    rank1_vector = np.asarray(
        dictionary_payload["reference_rank1_vector"], dtype=np.float64)
    static_dictionary_vector = np.asarray(
        dictionary["dictionary_vector"], dtype=np.float64)

    training_window_specs = tuple(
        tuple(int(value) for value in spec)
        for spec in full_payload["window_specs"])
    holdout_window_specs = tuple(
        tuple(int(value) for value in spec)
        for spec in holdout_payload["window_specs"])
    train_targets, train_meta, train_windows = collect_targets(
        training_window_specs, "training")
    hold_targets, hold_meta, hold_windows = collect_targets(
        holdout_window_specs, "heldout")
    sample_targets = tuple(dict.fromkeys(
        (STRESS_TARGET,) + train_targets + hold_targets))
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=sample_targets, dominant_modes=(1, 2),
        tail_threshold=.3, top_channel_count=40)
    stress_contributions = contribution_map(
        profile["target_rows"][STRESS_TARGET])

    train_rows, train_deficits = build_rows(
        train_targets, train_meta, profile, outside_labels,
        stress_contributions, rank1_vector, static_dictionary_vector)
    hold_rows, hold_deficits = build_rows(
        hold_targets, hold_meta, profile, outside_labels,
        stress_contributions, rank1_vector, static_dictionary_vector)
    if len(train_deficits) != 1 or train_deficits[0]["target"] != STRESS_TARGET:
        raise AssertionError("training deficit set drifted")
    if hold_deficits:
        raise AssertionError("heldout deficit set drifted")

    x_train = design_matrix(train_rows, outside_labels)
    y_train = target_vector(train_rows)
    coefficients = fit_ridge(x_train, y_train, RIDGE_LAMBDA)

    train_scored = add_model_predictions(train_rows, outside_labels, coefficients)
    hold_scored = add_model_predictions(hold_rows, outside_labels, coefficients)
    x_hold = design_matrix(hold_rows, outside_labels)
    train_predicted = x_train @ coefficients
    hold_predicted = x_hold @ coefficients
    train_reference = target_vector(train_rows)
    hold_reference = target_vector(hold_rows)

    train_target_summary = model_summary(
        train_scored, train_predicted, train_reference, "target_residue")
    hold_target_summary = model_summary(
        hold_scored, hold_predicted, hold_reference, "target_residue")

    static_train_rows = static_summary(train_rows, "static_low_frequency")
    static_hold_rows = static_summary(hold_rows, "static_low_frequency")
    static_train_matrix = np.asarray([
        value
        for row in train_rows
        for value in row["static_low_frequency_delta_vector"]
    ], dtype=np.float64)
    static_hold_matrix = np.asarray([
        value
        for row in hold_rows
        for value in row["static_low_frequency_delta_vector"]
    ], dtype=np.float64)
    static_train_summary = model_summary(
        static_train_rows, static_train_matrix, train_reference,
        "static_low_frequency")
    static_hold_summary = model_summary(
        static_hold_rows, static_hold_matrix, hold_reference,
        "static_low_frequency")

    holdout_improves_static = (
        hold_target_summary["matrix_cosine_to_rank1_reference"]
        > static_hold_summary["matrix_cosine_to_rank1_reference"]
        and hold_target_summary["high_drag_overlap_count_at_reference_k"]
        >= static_hold_summary["high_drag_overlap_count_at_reference_k"]
        and hold_target_summary["cap_record"]["failing_count"] == 0
        and hold_target_summary["nonpositive_delta_count"] == 0)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_lift_project_dictionary_audit": str(
            DICTIONARY_SOURCE.relative_to(ROOT)),
        "source_full_window_audit": str(FULL_WINDOW_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lift_holdout": str(
            LOW_HOLDOUT_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite target-residue lift training/holdout audit only; "
            "coefficients are trained on the original q286 full-window fixture "
            "and scored on fresh heldout windows.  This proves no target-residue "
            "lift theorem, residual-bound theorem, signed projection theorem, "
            "or Goldbach theorem."),
        "candidate": (
            "A target-residue tensor of N mod 11/13 features with the "
            "low-frequency q286 channel-label basis may explain more of the "
            "frozen rank-1 delta matrix than the static low-frequency vector."),
        "mechanism": (
            "Use predeclared row features from N mod 11 and N mod 13, including "
            "first two Fourier harmonics, Legendre symbols, and sum/difference "
            "phases.  Tensor them with the low-frequency channel-label features "
            "from the prior audit, fit ridge coefficients only on the original "
            "full-window rows, and replay the frozen model on fresh windows."),
        "prediction": (
            "If conductor-11/conductor-13 splitting is the missing ingredient, "
            "the heldout tensor lift should improve matrix cosine to the frozen "
            "rank-1 reference and preserve high-drag overlap without adding "
            "positivity or 0.75 cap failures."),
        "falsifier": (
            "If the residue tensor improves only on training rows or degrades "
            "heldout positivity, cap survival, or high-drag overlap relative to "
            "the static low-frequency lift, demote this residue-only extension "
            "as overfit or too weak."),
        "novelty_label": "new-to-this-task",
        "ridge_lambda": RIDGE_LAMBDA,
        "row_feature_names": ROW_FEATURE_NAMES,
        "channel_feature_names": CHANNEL_FEATURE_NAMES,
        "coefficient_count": int(len(coefficients)),
        "training_window_specs": training_window_specs,
        "heldout_window_specs": holdout_window_specs,
        "stress_target": STRESS_TARGET,
        "training_clear_count": len(train_rows),
        "training_deficit_targets": tuple(
            row["target"] for row in train_deficits),
        "heldout_clear_count": len(hold_rows),
        "heldout_deficit_targets": tuple(
            row["target"] for row in hold_deficits),
        "training_window_summaries": train_windows,
        "heldout_window_summaries": hold_windows,
        "outside_labels": outside_labels,
        "static_low_frequency_training_summary": static_train_summary,
        "static_low_frequency_heldout_summary": static_hold_summary,
        "target_residue_training_summary": train_target_summary,
        "target_residue_heldout_summary": hold_target_summary,
        "heldout_target_residue_improves_static_low_frequency": (
            holdout_improves_static),
        "coefficient_l2_norm": float(np.linalg.norm(coefficients)),
        "coefficient_linf_norm": float(np.max(np.abs(coefficients))),
        "summary": {
            "result": (
                "The audit records whether adding target residue phases to the "
                "low-frequency channel lift survives heldout scoring."),
            "boundary": (
                "A heldout improvement is a finite local tool only; a failure "
                "does not refute richer character-sum magnitude or splitting "
                "lifts."),
        },
        "interpretation": {
            "next_if_improves": (
                "Freeze another denominator and test whether the same "
                "target-residue tensor model keeps improving without refit."),
            "next_if_fails": (
                "Demote target-residue phases alone and use actual channel "
                "character-sum magnitudes or row-dependent signed cones."),
        },
        "target_residue_lift_holdout_measured": True,
        "target_residue_lift_theorem_proved": False,
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
