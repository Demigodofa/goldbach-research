"""Audit predeclared lift-and-project dictionaries for q286 rank-1 holes.

The AI unit-distance method-transfer note suggests a modest Goldbach analogue:
try a lifted representation only where a local q286 hole is already glowing.
This receipt freezes simple channel-label dictionaries before scoring them
against the existing full-window rank-1/residual-drag fixture.

The dictionaries are not proof objects.  They are finite candidates for
explaining the Octave rank-1 outside direction without target-specific row
fitting, and for predicting the known high residual-drag rows.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RANK1_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-octave-rank1-audit.json")
FULL_WINDOW_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-full-window-audit.json")
OUT = ROOT / "evidence" / "q286-lift-project-dictionary-audit.json"
STRESS_TARGET = 1222142
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


def collect_full_window_targets(window_specs):
    targets = []
    target_metadata = {}
    seen = set()
    for window_index, (start, count) in enumerate(window_specs):
        census = q286_first_three_dominant_mode_above_floor_holdout_census_receipt(
            start=int(start), target_count=int(count), target_step=2,
            closest_count=min(20, int(count)), include_rows=True)
        role = "primary" if window_index == 0 else "stress"
        for row in census["target_rows"]:
            target = int(row["target"])
            if target in seen:
                continue
            seen.add(target)
            targets.append(target)
            target_metadata[target] = {
                "window_index": int(window_index),
                "window_start": int(start),
                "window_role": role,
                "target_mod_286": int(row["target_mod_286"]),
                "target_mod_10010": target % 10010,
                "absolute_above_floor_signed_surplus": float(
                    row["absolute_above_floor_signed_surplus"]),
                "dominant_floor_passes": bool(row["dominant_floor_passes"]),
            }
    return tuple(targets), target_metadata


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


def normalize(vector):
    vector = np.asarray(vector, dtype=np.float64)
    norm = float(np.linalg.norm(vector))
    if norm == 0.0 or not math.isfinite(norm):
        return None
    return vector / norm


def canonicalize(vector, reference):
    vector = normalize(vector)
    if vector is None:
        return None
    if float(np.dot(vector, reference)) < 0:
        vector = -vector
    return vector


def centered(values):
    values = np.asarray(values, dtype=np.float64)
    return values - float(np.mean(values))


def named_features(labels):
    a = np.asarray([label[0] for label in labels], dtype=np.float64)
    b = np.asarray([label[1] for label in labels], dtype=np.float64)
    phase_a = 2.0 * math.pi * a / 10.0
    phase_b = 2.0 * math.pi * b / 12.0
    return {
        "constant": np.ones(len(labels), dtype=np.float64),
        "a_centered": centered(a),
        "b_centered": centered(b),
        "a_bilinear_centered": centered(a * b),
        "a_quadratic_centered": centered(a * a),
        "b_quadratic_centered": centered(b * b),
        "cos_a_1": np.cos(phase_a),
        "sin_a_1": np.sin(phase_a),
        "cos_a_2": np.cos(2.0 * phase_a),
        "sin_a_2": np.sin(2.0 * phase_a),
        "cos_b_1": np.cos(phase_b),
        "sin_b_1": np.sin(phase_b),
        "cos_b_2": np.cos(2.0 * phase_b),
        "sin_b_2": np.sin(2.0 * phase_b),
        "cos_sum_1": np.cos(phase_a + phase_b),
        "sin_sum_1": np.sin(phase_a + phase_b),
        "cos_diff_1": np.cos(phase_a - phase_b),
        "sin_diff_1": np.sin(phase_a - phase_b),
        "same_parity": np.asarray(
            [1.0 if (label[0] - label[1]) % 2 == 0 else -1.0
             for label in labels], dtype=np.float64),
        "edge_a": np.asarray(
            [1.0 if label[0] in (1, 5) else -1.0 for label in labels],
            dtype=np.float64),
        "edge_b": np.asarray(
            [1.0 if label[1] in (1, 11) else -1.0 for label in labels],
            dtype=np.float64),
        "claude_order_weight": np.asarray(
            [(math.gcd(label[0], 10) / 10.0)
             * (math.gcd(label[1], 12) / 12.0)
             for label in labels], dtype=np.float64),
        "primitive_root_2_realpart": np.cos(phase_a + phase_b),
        "gemini_legendre_product_sign": np.asarray(
            [(-1.0) ** (int(label[0] // 5) + int(label[1] // 6))
             for label in labels], dtype=np.float64),
    }


def dictionary_specs():
    return (
        {
            "id": "constant_sum",
            "kind": "single_predeclared_feature",
            "feature_names": ("constant",),
            "mechanism": "All outside channels contribute through one uniform lifted mass coordinate.",
        },
        {
            "id": "label_lattice_linear_polynomial",
            "kind": "predeclared_subspace_projection",
            "feature_names": (
                "constant", "a_centered", "b_centered",
                "a_bilinear_centered"),
            "mechanism": "A low-degree label-lattice polynomial acts as a coarse ray-class coordinate.",
        },
        {
            "id": "label_lattice_quadratic_polynomial",
            "kind": "predeclared_subspace_projection",
            "feature_names": (
                "constant", "a_centered", "b_centered",
                "a_bilinear_centered", "a_quadratic_centered",
                "b_quadratic_centered"),
            "mechanism": "A slightly richer low-degree label-lattice polynomial explains curvature in the channel labels.",
        },
        {
            "id": "separate_low_frequency_characters",
            "kind": "predeclared_subspace_projection",
            "feature_names": (
                "constant", "cos_a_1", "sin_a_1", "cos_b_1",
                "sin_b_1"),
            "mechanism": "Separate low-frequency character phases on the C10 and C12 factors carry the direction.",
        },
        {
            "id": "separate_two_harmonic_characters",
            "kind": "predeclared_subspace_projection",
            "feature_names": (
                "constant", "cos_a_1", "sin_a_1", "cos_a_2",
                "sin_a_2", "cos_b_1", "sin_b_1", "cos_b_2",
                "sin_b_2"),
            "mechanism": "Two harmonics on each factor form a small ray-class Fourier dictionary.",
        },
        {
            "id": "sum_difference_coupled_phases",
            "kind": "predeclared_subspace_projection",
            "feature_names": (
                "constant", "cos_sum_1", "sin_sum_1", "cos_diff_1",
                "sin_diff_1"),
            "mechanism": "The lifted direction is a coupled phase on the product label torus.",
        },
        {
            "id": "full_low_frequency_lift",
            "kind": "predeclared_subspace_projection",
            "feature_names": (
                "constant", "cos_a_1", "sin_a_1", "cos_a_2",
                "sin_a_2", "cos_b_1", "sin_b_1", "cos_b_2",
                "sin_b_2", "cos_sum_1", "sin_sum_1", "cos_diff_1",
                "sin_diff_1"),
            "mechanism": "A compact low-frequency lift across separate and coupled label phases explains the shadow.",
        },
        {
            "id": "edge_and_parity_lift",
            "kind": "predeclared_subspace_projection",
            "feature_names": (
                "constant", "same_parity", "edge_a", "edge_b"),
            "mechanism": "Boundary and parity classes of the label grid, rather than smooth phase, carry the direction.",
        },
        {
            "id": "claude_order_weight_lift",
            "kind": "single_predeclared_feature",
            "feature_names": ("claude_order_weight",),
            "mechanism": "Claude-proposed product of inverse character orders gcd(a,10)/10 * gcd(b,12)/12 on the C10 x C12 label factors.",
        },
        {
            "id": "primitive_root_2_realpart",
            "kind": "single_predeclared_feature",
            "feature_names": ("primitive_root_2_realpart",),
            "mechanism": "Real part of the primitive-root-2 phase heuristic cos(2*pi*a/10 + 2*pi*b/12), included as a negative-control version of Claude's discarded candidate.",
        },
        {
            "id": "gemini_legendre_product_sign",
            "kind": "single_predeclared_feature",
            "feature_names": ("gemini_legendre_product_sign",),
            "mechanism": "Gemini-proposed Legendre-product sign vector (-1)^(floor(a/5)+floor(b/6)) on the folded C10 x C12 labels.",
        },
    )


def average_ranks(values):
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    start = 0
    while start < len(indexed):
        end = start + 1
        while end < len(indexed) and indexed[end][1] == indexed[start][1]:
            end += 1
        rank = (start + 1 + end) / 2.0
        for index in range(start, end):
            ranks[indexed[index][0]] = rank
        start = end
    return np.asarray(ranks, dtype=np.float64)


def pearson(x, y):
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    dx = x - float(np.mean(x))
    dy = y - float(np.mean(y))
    denom = float(np.linalg.norm(dx) * np.linalg.norm(dy))
    if denom == 0.0:
        return None
    return float(np.dot(dx, dy) / denom)


def spearman(x, y):
    return pearson(average_ranks(tuple(x)), average_ranks(tuple(y)))


def claude_order_weight_diagnostic(labels, rank1_vector, features,
                                   volatile_labels):
    order_weights = np.asarray(features["claude_order_weight"],
                               dtype=np.float64)
    primitive_root = np.asarray(features["primitive_root_2_realpart"],
                                dtype=np.float64)
    by_label = {
        label: {
            "label": label,
            "order_weight": float(weight),
            "rank1_loading": float(loading),
            "primitive_root_2_realpart": float(root_value),
        }
        for label, weight, loading, root_value in zip(
            labels, order_weights, rank1_vector, primitive_root)
    }
    tie_groups = {}
    for label, weight in zip(labels, order_weights):
        tie_groups.setdefault(float(weight), []).append(label)
    tie_rows = []
    for weight, group in sorted(tie_groups.items(), reverse=True):
        if len(group) < 2:
            continue
        loadings = [by_label[label]["rank1_loading"] for label in group]
        tie_rows.append({
            "order_weight": weight,
            "labels": tuple(group),
            "rank1_loading_range": max(loadings) - min(loadings),
            "rank1_loading_minimum": min(loadings),
            "rank1_loading_maximum": max(loadings),
        })
    outside_even = tuple(
        label for label in labels if (label[0] + label[1]) % 2 == 0)
    volatile_even = tuple(
        label for label in volatile_labels
        if (label[0] + label[1]) % 2 == 0)
    return {
        "source": "manual Claude response pasted by Kevin on 2026-09-14",
        "review_role": "SequentialAdversarial",
        "claim_outside_labels_even_parity": True,
        "outside_even_parity_count": len(outside_even),
        "outside_label_count": len(labels),
        "outside_all_even_parity": len(outside_even) == len(labels),
        "volatile_even_parity_count": len(volatile_even),
        "volatile_label_count": len(volatile_labels),
        "volatile_all_even_parity": len(volatile_even) == len(volatile_labels),
        "parity_separates_outside_from_volatile": (
            len(outside_even) == len(labels)
            and len(volatile_even) == 0),
        "parity_correction": (
            "The pasted parity observation holds for the 17 outside labels, "
            "but it does not separate outside from volatile here because the "
            "actual removed volatile labels are also all even parity."),
        "order_weight_formula": "gcd(a,10)/10 * gcd(b,12)/12",
        "order_weight_by_label": tuple(
            by_label[label] for label in labels),
        "spearman_rank1_vs_order_weight": spearman(
            rank1_vector, order_weights),
        "pearson_rank1_vs_order_weight": pearson(
            rank1_vector, order_weights),
        "spearman_rank1_vs_primitive_root_2_realpart": spearman(
            rank1_vector, primitive_root),
        "pearson_rank1_vs_primitive_root_2_realpart": pearson(
            rank1_vector, primitive_root),
        "order_weight_tie_rows": tuple(tie_rows),
        "maximum_rank1_loading_range_inside_order_weight_tie": max(
            (row["rank1_loading_range"] for row in tie_rows),
            default=0.0),
    }


def projection_dictionary(spec, features, reference):
    columns = [features[name] for name in spec["feature_names"]]
    matrix = np.column_stack(columns)
    if spec["kind"] == "single_predeclared_feature":
        vector = matrix[:, 0]
        coefficients = (1.0,)
    else:
        coefficients_array, *_ = np.linalg.lstsq(matrix, reference, rcond=None)
        vector = matrix @ coefficients_array
        coefficients = tuple(float(value) for value in coefficients_array)
    vector = canonicalize(vector, reference)
    if vector is None:
        raise AssertionError(f"zero dictionary vector for {spec['id']}")
    return vector, coefficients


def high_drag_set(rows):
    return {
        int(row["target"]) for row in rows
        if row["residual_drag_to_rank1_ratio"] >= HIGH_DRAG_RATIO_THRESHOLD
    }


def evaluate_dictionary(spec, vector, coefficients, rows, reference_high_drag):
    vector_sum = float(np.sum(vector))
    rank1_reference = np.asarray(
        [row["rank1_reference_delta_vector"] for row in rows],
        dtype=np.float64)
    deltas = np.asarray(
        [row["outside_delta_vector"] for row in rows], dtype=np.float64)
    dictionary_delta_vector = (deltas @ vector) * vector_sum

    scored_rows = []
    for row, dictionary_delta in zip(rows, dictionary_delta_vector):
        full_delta = float(row["full_outside_delta_to_stress"])
        residual = full_delta - float(dictionary_delta)
        residual_drag = max(0.0, -residual)
        ratio = (
            residual_drag / float(dictionary_delta)
            if dictionary_delta > 0 else math.inf)
        delta_to_full_ratio = (
            float(dictionary_delta) / full_delta
            if full_delta != 0.0 else math.inf)
        scored_rows.append({
            "target": int(row["target"]),
            "target_mod_286": int(row["target_mod_286"]),
            "target_mod_10010": int(row["target_mod_10010"]),
            "full_outside_delta_to_stress": full_delta,
            "dictionary_reconstructed_outside_delta": float(dictionary_delta),
            "dictionary_delta_to_full_delta_ratio": delta_to_full_ratio,
            "residual_after_dictionary_row_sum": residual,
            "residual_drag": residual_drag,
            "residual_drag_to_dictionary_ratio": ratio,
            "reference_rank1_reconstructed_outside_delta": float(
                row["rank1_reconstructed_outside_delta"]),
            "reference_rank1_residual_drag_to_rank1_ratio": float(
                row["residual_drag_to_rank1_ratio"]),
        })

    nonpositive_rows = tuple(
        row for row in scored_rows
        if row["dictionary_reconstructed_outside_delta"] <= 0)
    rows_by_ratio = tuple(sorted(
        scored_rows,
        key=lambda row: (
            math.inf if not math.isfinite(
                row["residual_drag_to_dictionary_ratio"])
            else row["residual_drag_to_dictionary_ratio"],
            row["residual_drag"],
            -row["target"]),
        reverse=True))
    predicted_high_drag = {
        row["target"] for row in rows_by_ratio[:len(reference_high_drag)]
    }
    overlap = predicted_high_drag & reference_high_drag
    cap_failures = tuple(
        row for row in scored_rows
        if row["residual_drag_to_dictionary_ratio"] > CAP_TO_TEST)
    reference_flat = rank1_reference.reshape(-1)
    approx_matrix = np.outer(deltas @ vector, vector)
    approx_flat = approx_matrix.reshape(-1)
    matrix_denom = (
        float(np.linalg.norm(reference_flat))
        * float(np.linalg.norm(approx_flat)))
    matrix_cosine = (
        None if matrix_denom == 0.0
        else float(np.dot(reference_flat, approx_flat) / matrix_denom))
    return {
        "id": spec["id"],
        "kind": spec["kind"],
        "mechanism": spec["mechanism"],
        "feature_names": spec["feature_names"],
        "projection_coefficients": coefficients,
        "dictionary_vector": tuple(float(value) for value in vector),
        "dictionary_vector_sum": vector_sum,
        "rank1_direction_cosine": float(np.dot(vector, rows[0]["rank1_vector"])),
        "rank1_direction_explained_fraction": float(
            np.dot(vector, rows[0]["rank1_vector"]) ** 2),
        "rank1_matrix_replay_cosine": matrix_cosine,
        "dictionary_reconstructed_delta_summary": finite_summary(
            row["dictionary_reconstructed_outside_delta"]
            for row in scored_rows),
        "dictionary_delta_to_full_delta_ratio_summary": finite_summary(
            row["dictionary_delta_to_full_delta_ratio"]
            for row in scored_rows),
        "residual_drag_ratio_summary": finite_summary(
            row["residual_drag_to_dictionary_ratio"]
            for row in scored_rows),
        "nonpositive_dictionary_delta_count": len(nonpositive_rows),
        "nonpositive_dictionary_delta_targets": tuple(
            row["target"] for row in nonpositive_rows[:40]),
        "cap_tested": CAP_TO_TEST,
        "cap_failure_count": len(cap_failures),
        "cap_failure_targets": tuple(row["target"] for row in cap_failures[:40]),
        "worst_residual_drag_ratio_row": rows_by_ratio[0],
        "top_predicted_high_drag_targets": tuple(
            row["target"] for row in rows_by_ratio[:len(reference_high_drag)]),
        "reference_high_drag_targets": tuple(sorted(reference_high_drag)),
        "high_drag_overlap_count_at_reference_k": len(overlap),
        "high_drag_recall_at_reference_k": (
            len(overlap) / len(reference_high_drag)
            if reference_high_drag else None),
        "high_drag_precision_at_reference_k": (
            len(overlap) / len(predicted_high_drag)
            if predicted_high_drag else None),
        "passes_local_hole_tightening_gate": bool(
            float(np.dot(vector, rows[0]["rank1_vector"])) >= 0.9
            and len(nonpositive_rows) == 0
            and len(cap_failures) == 0
            and len(overlap) >= math.ceil(0.7 * len(reference_high_drag))),
        "rows_by_residual_drag_ratio": rows_by_ratio[:25],
    }


def main():
    rank1_payload = json.loads(RANK1_SOURCE.read_text(encoding="utf-8"))
    full_payload = json.loads(FULL_WINDOW_SOURCE.read_text(encoding="utf-8"))
    outside_labels = tuple(
        label_tuple(row["label"])
        for row in rank1_payload["rank1_right_singular_vector_by_channel"])
    volatile_labels = tuple(
        label_tuple(label)
        for label in rank1_payload["volatile_labels_removed"])
    rank1_vector = np.asarray([
        float(row["rank1_right_singular_vector_loading"])
        for row in rank1_payload["rank1_right_singular_vector_by_channel"]
    ], dtype=np.float64)
    rank1_vector = canonicalize(rank1_vector, rank1_vector)
    if rank1_vector is None or len(outside_labels) != 17:
        raise AssertionError("rank-1 outside-vector source drifted")

    window_specs = tuple(
        tuple(int(value) for value in spec)
        for spec in full_payload["window_specs"])
    targets, target_metadata = collect_full_window_targets(window_specs)
    if len(targets) != int(full_payload["full_window_target_count"]):
        raise AssertionError("full-window target count drifted")
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=targets, dominant_modes=(1, 2), tail_threshold=.3,
        top_channel_count=40)
    stress_contributions = contribution_map(
        profile["target_rows"][STRESS_TARGET])

    rows = []
    deficit_targets = []
    for target in targets:
        profile_row = profile["target_rows"][target]
        if not profile_row["dominant_floor_passes"]:
            deficit_targets.append(target)
            continue
        contributions = contribution_map(profile_row)
        outside_delta_vector = tuple(
            contributions[label] - stress_contributions[label]
            for label in outside_labels)
        full_delta = math.fsum(outside_delta_vector)
        rank1_scalar = float(np.dot(outside_delta_vector, rank1_vector))
        rank1_reference_delta_vector = tuple(
            rank1_scalar * value for value in rank1_vector)
        rank1_delta = math.fsum(rank1_reference_delta_vector)
        residual = full_delta - rank1_delta
        rows.append({
            **target_metadata[target],
            "target": int(target),
            "outside_delta_vector": outside_delta_vector,
            "full_outside_delta_to_stress": full_delta,
            "rank1_reconstructed_outside_delta": rank1_delta,
            "residual_after_rank1_row_sum": residual,
            "residual_drag_to_rank1_ratio": (
                max(0.0, -residual) / rank1_delta),
            "rank1_reference_delta_vector": rank1_reference_delta_vector,
            "rank1_vector": rank1_vector,
        })

    if tuple(deficit_targets) != (STRESS_TARGET,):
        raise AssertionError("deficit target set drifted")
    reference_high_drag = high_drag_set(rows)
    if len(reference_high_drag) != 10:
        raise AssertionError("reference high-drag set drifted")

    features = named_features(outside_labels)
    claude_diagnostic = claude_order_weight_diagnostic(
        outside_labels, rank1_vector, features, volatile_labels)
    dictionary_rows = []
    for spec in dictionary_specs():
        vector, coefficients = projection_dictionary(spec, features, rank1_vector)
        dictionary_rows.append(
            evaluate_dictionary(
                spec, vector, coefficients, rows, reference_high_drag))

    best_by_cosine = max(
        dictionary_rows,
        key=lambda row: row["rank1_direction_cosine"])
    best_by_high_drag = max(
        dictionary_rows,
        key=lambda row: (
            row["high_drag_overlap_count_at_reference_k"],
            row["rank1_direction_cosine"]))
    passing = tuple(
        row for row in dictionary_rows
        if row["passes_local_hole_tightening_gate"])
    falsified = tuple(
        row for row in dictionary_rows
        if not row["passes_local_hole_tightening_gate"])

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_octave_rank1_audit": str(RANK1_SOURCE.relative_to(ROOT)),
        "source_full_window_residual_drag_audit": str(
            FULL_WINDOW_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite lift-and-project dictionary audit only; candidate "
            "dictionaries are predeclared channel-label subspaces scored "
            "against the existing q286 full-window fixture.  This proves no "
            "lifted dictionary theorem, no residual-bound theorem, no signed "
            "projection theorem, and no Goldbach theorem."),
        "candidate": (
            "A simple lifted dictionary on the q286 outside-channel label "
            "lattice might explain the frozen Octave rank-1 outside direction "
            "and predict high residual-drag rows without target-specific "
            "fitting."),
        "mechanism": (
            "Construct fixed low-frequency, polynomial, parity, and edge "
            "feature subspaces on the 17 outside real-channel labels.  Project "
            "the frozen rank-1 right singular vector onto each predeclared "
            "subspace, replay the resulting dictionary vector across the "
            "full-window clear-minus-stress outside-channel delta rows, and "
            "score positivity, 0.75 residual-drag cap survival, and high-drag "
            "target overlap."),
        "prediction": (
            "A useful local hole-tightening dictionary should have high cosine "
            "with the frozen rank-1 direction, keep reconstructed outside "
            "deltas positive on all full-window clears, preserve the 0.75 "
            "residual-drag cap, and recover most rank-1 high-drag rows among "
            "its top-k predicted high-drag rows."),
        "falsifier": (
            "This predeclared dictionary family is falsified as the immediate "
            "local explanation if no candidate passes cosine >= 0.9, all-row "
            "positive reconstructed delta, no 0.75 cap failures, and at least "
            "70 percent recall of the rank-1 high-drag set at k=10."),
        "novelty_label": "new-to-this-task",
        "creative_tool_check": (
            "inventive-synthesis staged because a representation shift could "
            "change the next q286 test; preserve-hypotheses remains available "
            "if this family fails with useful components."),
        "window_specs": window_specs,
        "stress_target": STRESS_TARGET,
        "clear_count": len(rows),
        "outside_labels": outside_labels,
        "volatile_labels_removed": volatile_labels,
        "reference_rank1_vector": tuple(float(value) for value in rank1_vector),
        "reference_high_drag_ratio_threshold": HIGH_DRAG_RATIO_THRESHOLD,
        "reference_high_drag_targets": tuple(sorted(reference_high_drag)),
        "dictionary_count": len(dictionary_rows),
        "dictionary_rows": tuple(sorted(
            dictionary_rows,
            key=lambda row: (
                row["passes_local_hole_tightening_gate"],
                row["rank1_direction_cosine"],
                row["high_drag_overlap_count_at_reference_k"]),
            reverse=True)),
        "best_dictionary_by_rank1_cosine": {
            "id": best_by_cosine["id"],
            "rank1_direction_cosine": (
                best_by_cosine["rank1_direction_cosine"]),
            "high_drag_overlap_count_at_reference_k": (
                best_by_cosine["high_drag_overlap_count_at_reference_k"]),
            "cap_failure_count": best_by_cosine["cap_failure_count"],
            "nonpositive_dictionary_delta_count": (
                best_by_cosine["nonpositive_dictionary_delta_count"]),
        },
        "best_dictionary_by_high_drag_overlap": {
            "id": best_by_high_drag["id"],
            "rank1_direction_cosine": (
                best_by_high_drag["rank1_direction_cosine"]),
            "high_drag_overlap_count_at_reference_k": (
                best_by_high_drag["high_drag_overlap_count_at_reference_k"]),
            "cap_failure_count": best_by_high_drag["cap_failure_count"],
            "nonpositive_dictionary_delta_count": (
                best_by_high_drag["nonpositive_dictionary_delta_count"]),
        },
        "passing_dictionary_count": len(passing),
        "passing_dictionary_ids": tuple(row["id"] for row in passing),
        "falsified_dictionary_count": len(falsified),
        "falsified_dictionary_ids": tuple(row["id"] for row in falsified),
        "predeclared_family_passes_local_hole_tightening_gate": bool(passing),
        "claude_order_weight_diagnostic": claude_diagnostic,
        "summary": {
            "result": (
                "The audit records whether simple lifted label dictionaries "
                "explain the q286 rank-1 outside direction and high-drag rows "
                "well enough to tighten the current hole."),
            "boundary": (
                "A pass would be a finite local explanation candidate only; "
                "a failure retires this simple dictionary family without "
                "retiring richer row-dependent or number-field lifts."),
        },
        "interpretation": {
            "next_if_passes": (
                "Freeze a new holdout denominator and test the passing "
                "dictionary without refitting."),
            "next_if_fails": (
                "Record the failure as evidence that the q286 rank-1 shadow "
                "is not explained by these simple label-lattice lifts; move "
                "to row-dependent arithmetic balance or a richer lifted "
                "number-field/ray-class dictionary."),
        },
        "lift_project_dictionary_audit_measured": True,
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
