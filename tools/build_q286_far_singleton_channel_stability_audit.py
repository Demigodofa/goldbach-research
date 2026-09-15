"""Audit singleton channel stability after local subtraction on q286 far rows.

The zero-local channel-margin audit found that one-channel LP-weighted subsets
already keep the 12 zero-local target integers positive.  This follow-up asks
whether that singleton stability persists on the full far-stress fixture.

Finite evidence only: this proves no distributed cone theorem, binary-prime
correlation theorem, signed projection theorem, or Goldbach theorem.
"""

from __future__ import annotations

import itertools
import json
import math
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
LOCAL_SOURCE = ROOT / "evidence" / "q286-lp-cone-local-singular-audit.json"
LP_SOURCE = ROOT / "evidence" / "q286-low-frequency-lp-cone-audit.json"
ZERO_LOCAL_MARGIN_SOURCE = (
    ROOT / "evidence" / "q286-zero-local-channel-margin-audit.json")
OUT = ROOT / "evidence" / "q286-far-singleton-channel-stability-audit.json"
STRESS_TARGET = 1222142
WATCHLIST_LABELS = ((5, 5), (3, 1), (3, 11), (3, 7))
TOLERANCE = 1e-12
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def label_tuple(label):
    return tuple(int(part) for part in label)


def label_key(label):
    return f"{int(label[0])},{int(label[1])}"


def contribution_map(row):
    return {
        label_tuple(item["representative_label"]): float(
            item["contribution_to_principal_ratio"])
        for item in row["real_channel_contribution_rows"]
    }


def finite_summary(values):
    values = tuple(float(value) for value in values)
    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None}
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def collect_far_targets(window_specs):
    targets = []
    metadata = {}
    for window_index, (start, count) in enumerate(window_specs):
        for offset in range(int(count)):
            target = int(start) + 2 * offset
            targets.append(target)
            metadata[target] = {
                "target": target,
                "window_index": int(window_index),
                "window_start": int(start),
                "target_mod_143": target % 143,
                "target_mod_286": target % 286,
            }
    return tuple(targets), metadata


def row_weighted_map(row):
    return {
        label_key(item["label"]): float(item["lp_weighted_after_local"])
        for item in row["channel_rows"]
    }


def sign(value):
    if value > TOLERANCE:
        return "positive"
    if value < -TOLERANCE:
        return "negative"
    return "zero"


def channel_summary(labels, rows):
    summaries = []
    total_positive = math.fsum(
        max(0.0, value)
        for row in rows for value in row["weighted_by_label"].values())
    total_net = math.fsum(float(row["after_local_lp_delta"]) for row in rows)
    for label in labels:
        key = label_key(label)
        values = [row["weighted_by_label"][key] for row in rows]
        positive_values = [value for value in values if value > TOLERANCE]
        negative_values = [value for value in values if value < -TOLERANCE]
        zero_values = [value for value in values if abs(value) <= TOLERANCE]
        failure_targets = [
            row["target"] for row in rows
            if row["after_local_lp_delta"] - row["weighted_by_label"][key]
            <= TOLERANCE
        ]
        positive_targets = [
            row["target"] for row in rows if row["weighted_by_label"][key] > TOLERANCE]
        negative_targets = [
            row["target"] for row in rows if row["weighted_by_label"][key] < -TOLERANCE]
        summaries.append({
            "label": label,
            "label_key": key,
            "positive_count": len(positive_values),
            "negative_count": len(negative_values),
            "zero_count": len(zero_values),
            "weighted_contribution_summary": finite_summary(values),
            "positive_weighted_sum": math.fsum(positive_values),
            "negative_weighted_sum": math.fsum(negative_values),
            "net_weighted_sum": math.fsum(values),
            "positive_margin_share": (
                math.fsum(positive_values) / total_positive
                if total_positive else None),
            "net_margin_share_vs_total_net_lp_margin": (
                math.fsum(values) / total_net if total_net else None),
            "singleton_passes_scope": len(negative_values) == 0 and not zero_values,
            "removing_channel_makes_any_target_fail": bool(failure_targets),
            "removal_failure_count": len(failure_targets),
            "removal_failure_targets_first_20": failure_targets[:20],
            "positive_targets_first_20": positive_targets[:20],
            "negative_targets_first_20": negative_targets[:20],
        })
    summaries.sort(
        key=lambda item: (
            not item["singleton_passes_scope"],
            -(item["positive_margin_share"] or 0.0),
            item["label"]))
    return summaries


def subset_margins(combo, rows):
    keys = [label_key(label) for label in combo]
    return [
        math.fsum(row["weighted_by_label"][key] for key in keys)
        for row in rows
    ]


def smallest_positive_subset(labels, rows):
    labels = tuple(labels)
    for size in range(1, len(labels) + 1):
        passing = []
        checked = 0
        for combo in itertools.combinations(labels, size):
            checked += 1
            margins = subset_margins(combo, rows)
            if min(margins) > TOLERANCE:
                passing.append({
                    "labels": combo,
                    "minimum_target_margin": float(min(margins)),
                    "average_target_margin": math.fsum(margins) / len(margins),
                    "total_margin": float(math.fsum(margins)),
                    "worst_targets": [
                        {
                            "target": rows[index]["target"],
                            "target_mod_143": rows[index]["target_mod_143"],
                            "subset_lp_margin": float(margins[index]),
                        }
                        for index in np.argsort(np.asarray(margins))[:10]
                    ],
                })
        if passing:
            passing.sort(
                key=lambda item: (
                    -item["minimum_target_margin"],
                    -item["total_margin"],
                    item["labels"]))
            return {
                "minimum_size": size,
                "passing_subset_count_at_minimum_size": len(passing),
                "checked_subset_count_at_minimum_size": checked,
                "best_subsets_by_minimum_margin": passing[:20],
                "small_fixed_subset_exists": size <= 3,
            }
    return {
        "minimum_size": None,
        "passing_subset_count_at_minimum_size": 0,
        "checked_subset_count_at_minimum_size": 2 ** len(labels) - 1,
        "best_subsets_by_minimum_margin": [],
        "small_fixed_subset_exists": False,
    }


def summarize_scope(scope, rows, labels):
    total_positive = math.fsum(
        max(0.0, value)
        for row in rows for value in row["weighted_by_label"].values())
    total_negative = math.fsum(
        min(0.0, value)
        for row in rows for value in row["weighted_by_label"].values())
    total_net = math.fsum(float(row["after_local_lp_delta"]) for row in rows)
    channels = channel_summary(labels, rows)
    return {
        "scope": scope,
        "target_count": len(rows),
        "target_mod_143_count": len({row["target_mod_143"] for row in rows}),
        "total_positive_weighted_margin": total_positive,
        "total_negative_weighted_margin": total_negative,
        "total_net_lp_margin": total_net,
        "after_local_lp_delta_summary": finite_summary(
            row["after_local_lp_delta"] for row in rows),
        "after_local_full_delta_summary": finite_summary(
            row["after_local_full_outside_delta"] for row in rows),
        "channel_summary_rows": channels,
        "singleton_passing_channels": [
            row["label"] for row in channels if row["singleton_passes_scope"]],
        "singleton_passing_count": sum(
            1 for row in channels if row["singleton_passes_scope"]),
        "channels_whose_removal_fails_target": [
            row["label"] for row in channels
            if row["removing_channel_makes_any_target_fail"]],
        "any_single_channel_removal_fails_target": any(
            row["removing_channel_makes_any_target_fail"]
            for row in channels),
        "smallest_fixed_subset": smallest_positive_subset(labels, rows),
    }


def watchlist_summary(scope_summary):
    by_key = {
        row["label_key"]: row for row in scope_summary["channel_summary_rows"]
    }
    return [
        by_key[label_key(label)] for label in WATCHLIST_LABELS
    ]


def main():
    local_payload = json.loads(LOCAL_SOURCE.read_text(encoding="utf-8"))
    lp_payload = json.loads(LP_SOURCE.read_text(encoding="utf-8"))
    zero_margin_payload = json.loads(
        ZERO_LOCAL_MARGIN_SOURCE.read_text(encoding="utf-8"))
    labels = tuple(label_tuple(label) for label in local_payload["outside_labels"])
    lp_vector = np.asarray(
        lp_payload["selected_lp_effective_vector"], dtype=np.float64)
    if lp_vector.shape != (17,):
        raise AssertionError("LP vector drifted")
    local_rows_by_residue = {
        int(row["n_mod_143"]): row
        for row in local_payload["local_residue_rows"]
    }
    targets, metadata = collect_far_targets(local_payload["far_window_specs"])
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=(STRESS_TARGET,) + targets,
        dominant_modes=(1, 2), tail_threshold=.3, top_channel_count=40)
    stress = contribution_map(profile["target_rows"][STRESS_TARGET])
    rows = []
    for target in targets:
        profile_row = profile["target_rows"][target]
        if not profile_row["dominant_floor_passes"]:
            continue
        contributions = contribution_map(profile_row)
        empirical_delta = np.asarray([
            contributions[label] - stress[label] for label in labels
        ], dtype=np.float64)
        local_delta = np.asarray(
            local_rows_by_residue[target % 143]["local_delta_vector"],
            dtype=np.float64)
        after_local = empirical_delta - local_delta
        weighted_by_label = {
            label_key(label): float(value * weight)
            for label, value, weight in zip(labels, after_local, lp_vector)
        }
        rows.append({
            **metadata[target],
            "after_local_full_outside_delta": float(np.sum(after_local)),
            "after_local_lp_delta": float(after_local @ lp_vector),
            "local_lp_action": float(local_delta @ lp_vector),
            "weighted_by_label": weighted_by_label,
            "sign_by_label": {
                key: sign(value) for key, value in weighted_by_label.items()
            },
        })
    if len(rows) != local_payload["far_empirical_summary"]["far_clear_count"]:
        raise AssertionError("far clear count drifted")

    rows_by_residue = defaultdict(list)
    for row in rows:
        rows_by_residue[row["target_mod_143"]].append(row)
    zero_residues = set(
        local_payload["local_lp_zero_residues"])
    zero_rows = [
        row for row in rows if row["target_mod_143"] in zero_residues]
    nonzero_rows = [
        row for row in rows if row["target_mod_143"] not in zero_residues]

    scopes = {
        "all_far_clear_targets": summarize_scope(
            "all_far_clear_targets", rows, labels),
        "zero_local_residue_targets": summarize_scope(
            "zero_local_residue_targets", zero_rows, labels),
        "nonzero_local_residue_targets": summarize_scope(
            "nonzero_local_residue_targets", nonzero_rows, labels),
    }
    for residue in (38, 64):
        scopes[f"residue_{residue}"] = summarize_scope(
            f"residue_{residue}", rows_by_residue[residue], labels)

    all_scope = scopes["all_far_clear_targets"]
    watchlist_all = watchlist_summary(all_scope)
    watchlist_passing = [
        row["label"] for row in watchlist_all if row["singleton_passes_scope"]]
    watchlist_failing = [
        row["label"] for row in watchlist_all if not row["singleton_passes_scope"]]
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lp_cone_audit": str(LP_SOURCE.relative_to(ROOT)),
        "source_zero_local_margin_audit": str(
            ZERO_LOCAL_MARGIN_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite full far-stress channel stability audit over 606 clear "
            "targets; no distributed cone theorem, binary-prime correlation "
            "theorem, signed projection theorem, or Goldbach theorem."),
        "candidate": (
            "The one-channel positivity seen on the 12 zero-local targets may "
            "persist across the full far-stress fixture after subtracting each "
            "target residue's local vector."),
        "prediction": (
            "If the zero-local singleton channels represent stable q286 "
            "correlation directions, some singleton channels should remain "
            "LP-weighted positive on all 606 far clear targets."),
        "falsifier": (
            "If every singleton channel has a nonpositive weighted contribution "
            "on at least one far target, the 12-row singleton effect is not a "
            "full-far-fixture singleton certificate."),
        "target_count": len(rows),
        "stress_target": STRESS_TARGET,
        "outside_labels": labels,
        "scopes": scopes,
        "watchlist_labels": WATCHLIST_LABELS,
        "watchlist_all_far_summary": watchlist_all,
        "watchlist_all_far_passing_singletons": watchlist_passing,
        "watchlist_all_far_failing_singletons": watchlist_failing,
        "zero_local_best_singleton_from_previous_audit": (
            zero_margin_payload["scopes"]["all_12_targets"][
                "smallest_fixed_subset"]["best_subsets_by_minimum_margin"][0]),
        "all_far_singleton_passing_count": all_scope[
            "singleton_passing_count"],
        "all_far_smallest_fixed_subset_size": all_scope[
            "smallest_fixed_subset"]["minimum_size"],
        "all_far_smallest_fixed_subset_count": all_scope[
            "smallest_fixed_subset"][
                "passing_subset_count_at_minimum_size"],
        "decision": (
            "The broad far-fixture replay preserves singleton stability for "
            "(5,5) and (3,1): both remain positive on all 606 clear targets "
            "after subtracting each residue's local vector. The same replay "
            "falsifies all-far singleton stability for (3,11) and (3,7): "
            "they pass on the 12 zero-local targets but have negative "
            "weighted contributions on 10 and 7 nonzero-local targets, "
            "respectively. The all-far smallest positive fixed subset still "
            "has size 1, with five passing singleton channels."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
