"""Audit multichannel rescue on the q286 residue-5 near-collision horizon.

The scalar centered (3,1) residue-5 horizon failed against reference 164598.
This receipt tests whether previously frozen multichannel objects rescue that
failure: Kevin's four-channel watchlist and the frozen 17-channel LP vector.

Finite evidence only: this proves no selected-stress theorem, signed
correlation theorem, pointwise character-sum theorem, or Goldbach theorem.
"""

from __future__ import annotations

import itertools
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    contribution_map,
    label_key,
    label_tuple,
)
from tools.build_q286_centered_3_1_residue5_near_collision_horizon import (  # noqa: E402
    CENTER_TARGET,
    OFFSET_RADIUS,
    REFERENCE_TARGET,
    STEP,
    horizon_targets,
)


EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-centered-3-1-residue5-multichannel-horizon.json"

WATCHLIST_LABELS = ((5, 5), (3, 1), (3, 11), (3, 7))
SCALAR_LABEL = (3, 1)
TOLERANCE = 1e-12


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


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


def build_row(target, offset, profile, labels, local_rows_by_residue,
              lp_vector, reference_contribs, reference_local):
    contributions = contribution_map(profile["target_rows"][int(target)])
    local = np.asarray(
        local_rows_by_residue[int(target) % 143]["local_delta_vector"],
        dtype=np.float64)
    local_gap = local - reference_local
    empirical_gap = np.asarray([
        float(contributions[label]) - float(reference_contribs[label])
        for label in labels
    ], dtype=np.float64)
    after_local_gap = empirical_gap - local_gap
    weighted_gap = after_local_gap * lp_vector
    by_label = {}
    for label, empirical, local_value, after_local, weighted in zip(
            labels, empirical_gap, local_gap, after_local_gap, weighted_gap):
        by_label[label_key(label)] = {
            "label": list(label),
            "empirical_gap": float(empirical),
            "local_gap": float(local_value),
            "after_local_gap": float(after_local),
            "lp_weighted_gap": float(weighted),
        }
    return {
        "target": int(target),
        "target_mod_143": int(target) % 143,
        "target_mod_286": int(target) % 286,
        "offset_from_center_in_286_steps": offset,
        "weighted_gap_by_label": {
            key: value["lp_weighted_gap"] for key, value in by_label.items()
        },
        "channel_rows": list(by_label.values()),
    }


def subset_margin(row, labels):
    keys = [label_key(label) for label in labels]
    return math.fsum(row["weighted_gap_by_label"][key] for key in keys)


def summarize_subset(name, labels, rows):
    margins = [subset_margin(row, labels) for row in rows]
    enriched = []
    for row, margin in zip(rows, margins):
        enriched.append({
            "target": row["target"],
            "target_mod_143": row["target_mod_143"],
            "target_mod_286": row["target_mod_286"],
            "offset_from_center_in_286_steps": (
                row["offset_from_center_in_286_steps"]),
            "subset_weighted_gap": float(margin),
            "passes_subset_gate": margin > TOLERANCE,
        })
    ranked = sorted(
        enriched, key=lambda row: (row["subset_weighted_gap"], row["target"]))
    failing = [row for row in ranked if not row["passes_subset_gate"]]
    return {
        "name": name,
        "labels": [list(label) for label in labels],
        "label_keys": [label_key(label) for label in labels],
        "label_count": len(labels),
        "all_targets_pass": not failing,
        "failing_target_count": len(failing),
        "failing_rows": failing,
        "weighted_gap_summary": finite_summary(margins),
        "tightest_rows": ranked[:12],
        "widest_rows": ranked[-12:],
    }


def channel_summaries(labels, rows):
    out = []
    for label in labels:
        key = label_key(label)
        values = [row["weighted_gap_by_label"][key] for row in rows]
        positives = [value for value in values if value > TOLERANCE]
        negatives = [value for value in values if value < -TOLERANCE]
        zeros = [value for value in values if abs(value) <= TOLERANCE]
        ranked = sorted(
            (
                {
                    "target": row["target"],
                    "offset_from_center_in_286_steps": (
                        row["offset_from_center_in_286_steps"]),
                    "lp_weighted_gap": row["weighted_gap_by_label"][key],
                }
                for row in rows
            ),
            key=lambda item: (item["lp_weighted_gap"], item["target"]))
        out.append({
            "label": list(label),
            "label_key": key,
            "positive_count": len(positives),
            "negative_count": len(negatives),
            "zero_count": len(zeros),
            "weighted_gap_summary": finite_summary(values),
            "tightest_rows": ranked[:5],
            "widest_rows": ranked[-5:],
        })
    return sorted(
        out,
        key=lambda row: (
            row["negative_count"],
            row["weighted_gap_summary"]["minimum"],
            row["label_key"]))


def smallest_positive_subset(labels, rows):
    labels = tuple(labels)
    for size in range(1, len(labels) + 1):
        passing = []
        checked = 0
        for combo in itertools.combinations(labels, size):
            checked += 1
            margins = [subset_margin(row, combo) for row in rows]
            if min(margins) > TOLERANCE:
                ranked = sorted(
                    zip(rows, margins),
                    key=lambda item: (item[1], item[0]["target"]))
                passing.append({
                    "labels": [list(label) for label in combo],
                    "label_keys": [label_key(label) for label in combo],
                    "minimum_target_margin": float(min(margins)),
                    "average_target_margin": (
                        math.fsum(margins) / len(margins)),
                    "worst_targets": [
                        {
                            "target": row["target"],
                            "offset_from_center_in_286_steps": (
                                row["offset_from_center_in_286_steps"]),
                            "subset_weighted_gap": float(margin),
                        }
                        for row, margin in ranked[:10]
                    ],
                })
        if passing:
            passing.sort(
                key=lambda item: (
                    -item["minimum_target_margin"],
                    item["label_keys"]))
            return {
                "minimum_size": size,
                "passing_subset_count_at_minimum_size": len(passing),
                "checked_subset_count_at_minimum_size": checked,
                "best_subsets_by_minimum_margin": passing[:20],
                "post_hoc_diagnostic_only": True,
            }
    return {
        "minimum_size": None,
        "passing_subset_count_at_minimum_size": 0,
        "checked_subset_count_at_minimum_size": 2 ** len(labels) - 1,
        "best_subsets_by_minimum_margin": [],
        "post_hoc_diagnostic_only": True,
    }


def main():
    local_payload = load_json(LOCAL_SOURCE)
    lp_payload = load_json(LP_SOURCE)
    labels = tuple(label_tuple(label) for label in local_payload["outside_labels"])
    lp_vector = np.asarray(
        lp_payload["selected_lp_effective_vector"], dtype=np.float64)
    local_rows_by_residue = {
        int(row["n_mod_143"]): row
        for row in local_payload["local_residue_rows"]
    }
    targets = horizon_targets()
    if any(target % 143 != REFERENCE_TARGET % 143 for target in targets):
        raise AssertionError("horizon contains a nonmatching residue")

    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=(REFERENCE_TARGET,) + targets,
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=40)
    reference_contribs = contribution_map(
        profile["target_rows"][REFERENCE_TARGET])
    reference_local = np.asarray(
        local_rows_by_residue[REFERENCE_TARGET % 143]["local_delta_vector"],
        dtype=np.float64)
    rows = [
        build_row(
            target,
            offset,
            profile,
            labels,
            local_rows_by_residue,
            lp_vector,
            reference_contribs,
            reference_local)
        for offset, target in zip(
            range(-OFFSET_RADIUS, OFFSET_RADIUS + 1), targets)
    ]

    subset_results = [
        summarize_subset("scalar_3_1", (SCALAR_LABEL,), rows),
        summarize_subset("kevin_watchlist_4", WATCHLIST_LABELS, rows),
        summarize_subset(
            "kevin_watchlist_without_3_1",
            tuple(label for label in WATCHLIST_LABELS if label != SCALAR_LABEL),
            rows),
        summarize_subset("frozen_full_17_lp", labels, rows),
    ]
    subset_by_name = {row["name"]: row for row in subset_results}

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lp_cone_audit": str(LP_SOURCE.relative_to(ROOT)),
        "source_scalar_horizon_receipt": (
            "evidence/q286-centered-3-1-residue5-near-collision-horizon.json"),
        "reference_target": REFERENCE_TARGET,
        "center_target": CENTER_TARGET,
        "step": STEP,
        "offset_radius": OFFSET_RADIUS,
        "target_count": len(rows),
        "residue_mod_143": REFERENCE_TARGET % 143,
        "outside_labels": [list(label) for label in labels],
        "watchlist_labels": [list(label) for label in WATCHLIST_LABELS],
        "status_boundary": (
            "finite multichannel horizon audit only; the smallest-subset "
            "scan is post-hoc diagnostic and does not prove a theorem, signed "
            "correlation estimate, pointwise character-sum estimate, or "
            "Goldbach."),
        "mechanism": (
            "The scalar (3,1) residue-5 horizon fails with zero local gap. "
            "This audit keeps the same horizon and reference but sums frozen "
            "LP-weighted after-local channel gaps over pre-existing channel "
            "sets."),
        "prediction": (
            "If the scalar failure is a projection artifact, the frozen "
            "17-channel LP vector or Kevin's pre-existing watchlist should "
            "remain positive on all horizon targets."),
        "falsifier": (
            "Any nonpositive multichannel margin in a pre-existing subset "
            "falsifies that subset as a residue-5 horizon rescue."),
        "subset_results": subset_results,
        "channel_summary_rows": channel_summaries(labels, rows),
        "smallest_positive_fixed_subset": smallest_positive_subset(labels, rows),
        "decision": (
            "Read subset_results. A full-LP pass would redirect the route "
            "from scalar (3,1) to higher-dimensional signed-correlation; a "
            "full-LP failure would clip the current frozen LP bridge on this "
            "same residue-5 horizon."),
        "frozen_full_17_lp_passes_horizon": subset_by_name[
            "frozen_full_17_lp"]["all_targets_pass"],
        "kevin_watchlist_4_passes_horizon": subset_by_name[
            "kevin_watchlist_4"]["all_targets_pass"],
        "scalar_3_1_passes_horizon": subset_by_name[
            "scalar_3_1"]["all_targets_pass"],
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
