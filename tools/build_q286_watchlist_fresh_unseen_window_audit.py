"""Audit the fixed q286 watchlist on fresh unseen windows.

The selected-reference horizon audit found that Kevin's four-channel
watchlist survived all five selected deficit references, while scalar (3,1)
and the frozen full 17-channel LP did not.  This receipt tests the same fixed
watchlist on later fresh windows that were not used to select or replay the
watchlist.

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
from tools.build_q286_alternate_reference_channel_audit import (  # noqa: E402
    DEFICIT_REFERENCES,
)
from tools.build_q286_centered_3_1_residue5_multichannel_horizon import (  # noqa: E402
    SCALAR_LABEL,
    TOLERANCE,
    WATCHLIST_LABELS,
    finite_summary,
    label_key,
    subset_margin,
)
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    contribution_map,
    label_tuple,
)
from tools.build_q286_fresh_window_channel_watchlist_audit import (  # noqa: E402
    FRESH_WINDOW_SPECS,
    collect_targets,
)


EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-watchlist-fresh-unseen-window-audit.json"

SELECTED_REFERENCE_HORIZON_SOURCE = (
    EVIDENCE / "q286-multichannel-selected-reference-horizon-audit.json")

FRESH_UNSEEN_WINDOW_SPECS = (
    (48_000_000, 101),
    (52_000_000, 101),
    (56_000_000, 101),
    (60_000_000, 101),
    (64_000_000, 101),
    (68_000_000, 101),
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def reference_local_vector(local_rows_by_residue, reference):
    return np.asarray(
        local_rows_by_residue[int(reference) % 143]["local_delta_vector"],
        dtype=np.float64)


def dominant_sum_to_principal(profile_row):
    for key in (
            "dominant_sum_to_principal",
            "dominant_character_sum_to_principal_ratio",
            "dominant_mode_sum_to_principal_ratio"):
        if key in profile_row:
            return float(profile_row[key])
    raise KeyError("dominant sum field missing")


def build_comparison_rows(targets, metadata, references, profile, labels,
                          local_rows_by_residue, lp_vector):
    reference_contribs = {
        int(reference): contribution_map(profile["target_rows"][int(reference)])
        for reference in references
    }
    reference_locals = {
        int(reference): reference_local_vector(
            local_rows_by_residue, int(reference))
        for reference in references
    }
    rows = []
    fresh_target_rows = []
    for target in targets:
        profile_row = profile["target_rows"][int(target)]
        dominant_sum = dominant_sum_to_principal(profile_row)
        contributions = contribution_map(profile_row)
        target_local = np.asarray(
            local_rows_by_residue[int(target) % 143]["local_delta_vector"],
            dtype=np.float64)
        fresh_target_rows.append({
            **metadata[int(target)],
            "dominant_floor_passes": bool(
                profile_row["dominant_floor_passes"]),
            "dominant_sum_to_principal": dominant_sum,
            "dominant_margin_to_floor": float(dominant_sum + 0.3),
        })
        for reference in references:
            reference = int(reference)
            empirical_gap = np.asarray([
                float(contributions[label])
                - float(reference_contribs[reference][label])
                for label in labels
            ], dtype=np.float64)
            local_gap = target_local - reference_locals[reference]
            after_local_gap = empirical_gap - local_gap
            weighted_gap = after_local_gap * lp_vector
            rows.append({
                **metadata[int(target)],
                "reference_target": reference,
                "reference_mod_143": reference % 143,
                "reference_mod_286": reference % 286,
                "same_residue_as_reference": (
                    int(target) % 143 == reference % 143),
                "dominant_floor_passes": bool(
                    profile_row["dominant_floor_passes"]),
                "dominant_sum_to_principal": dominant_sum,
                "dominant_margin_to_floor": float(dominant_sum + 0.3),
                "after_local_full_outside_gap": float(np.sum(after_local_gap)),
                "after_local_lp_gap": float(after_local_gap @ lp_vector),
                "local_lp_gap": float(local_gap @ lp_vector),
                "weighted_gap_by_label": {
                    label_key(label): float(value)
                    for label, value in zip(labels, weighted_gap)
                },
            })
    return rows, fresh_target_rows


def summarize_subset(name, labels, rows):
    margins = [subset_margin(row, labels) for row in rows]
    enriched = []
    for row, margin in zip(rows, margins):
        enriched.append({
            "reference_target": row["reference_target"],
            "target": row["target"],
            "window_start": row["window_start"],
            "window_index": row["window_index"],
            "offset": row.get(
                "offset", (row["target"] - row["window_start"]) // 2),
            "target_mod_143": row["target_mod_143"],
            "same_residue_as_reference": row["same_residue_as_reference"],
            "dominant_floor_passes": row["dominant_floor_passes"],
            "dominant_margin_to_floor": row["dominant_margin_to_floor"],
            "subset_weighted_gap": float(margin),
            "passes_subset_gate": margin > TOLERANCE,
        })
    ranked = sorted(
        enriched,
        key=lambda row: (
            row["subset_weighted_gap"],
            row["reference_target"],
            row["target"]))
    failing = [row for row in ranked if not row["passes_subset_gate"]]
    return {
        "name": name,
        "labels": [list(label) for label in labels],
        "label_keys": [label_key(label) for label in labels],
        "label_count": len(labels),
        "all_targets_pass": not failing,
        "failing_target_count": len(failing),
        "failing_rows": failing[:80],
        "weighted_gap_summary": finite_summary(margins),
        "tightest_rows": ranked[:20],
        "widest_rows": ranked[-20:],
    }


def channel_summaries(labels, rows):
    total_positive = math.fsum(
        max(0.0, value)
        for row in rows for value in row["weighted_gap_by_label"].values())
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
                    "reference_target": row["reference_target"],
                    "target": row["target"],
                    "window_start": row["window_start"],
                    "offset": row.get(
                        "offset", (row["target"] - row["window_start"]) // 2),
                    "lp_weighted_gap": row["weighted_gap_by_label"][key],
                }
                for row in rows
            ),
            key=lambda item: (
                item["lp_weighted_gap"],
                item["reference_target"],
                item["target"]))
        out.append({
            "label": list(label),
            "label_key": key,
            "positive_count": len(positives),
            "negative_count": len(negatives),
            "zero_count": len(zeros),
            "weighted_gap_summary": finite_summary(values),
            "positive_weighted_sum": math.fsum(positives),
            "negative_weighted_sum": math.fsum(negatives),
            "positive_margin_share": (
                math.fsum(positives) / total_positive
                if total_positive else None),
            "tightest_rows": ranked[:8],
            "widest_rows": ranked[-8:],
        })
    return sorted(
        out,
        key=lambda row: (
            row["negative_count"],
            row["weighted_gap_summary"]["minimum"],
            row["label_key"]))


def summarize_by_reference(references, rows, labels):
    out = []
    for reference in references:
        reference_rows = [
            row for row in rows if row["reference_target"] == int(reference)]
        subset_results = [
            summarize_subset("scalar_3_1", (SCALAR_LABEL,), reference_rows),
            summarize_subset("kevin_watchlist_4", WATCHLIST_LABELS,
                             reference_rows),
            summarize_subset(
                "kevin_watchlist_without_3_1",
                tuple(label for label in WATCHLIST_LABELS
                      if label != SCALAR_LABEL),
                reference_rows),
            summarize_subset("frozen_full_17_lp", labels, reference_rows),
        ]
        by_name = {row["name"]: row for row in subset_results}
        out.append({
            "reference_target": int(reference),
            "reference_mod_143": int(reference) % 143,
            "reference_mod_286": int(reference) % 286,
            "target_count": len(reference_rows),
            "subset_results": subset_results,
            "scalar_3_1_passes": by_name["scalar_3_1"]["all_targets_pass"],
            "kevin_watchlist_4_passes": by_name[
                "kevin_watchlist_4"]["all_targets_pass"],
            "kevin_watchlist_without_3_1_passes": by_name[
                "kevin_watchlist_without_3_1"]["all_targets_pass"],
            "frozen_full_17_lp_passes": by_name[
                "frozen_full_17_lp"]["all_targets_pass"],
        })
    return out


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
                    key=lambda item: (
                        item[1],
                        item[0]["reference_target"],
                        item[0]["target"]))
                passing.append({
                    "labels": [list(label) for label in combo],
                    "label_keys": [label_key(label) for label in combo],
                    "minimum_target_margin": float(min(margins)),
                    "average_target_margin": (
                        math.fsum(margins) / len(margins)),
                    "worst_targets": [
                        {
                            "reference_target": row["reference_target"],
                            "target": row["target"],
                            "window_start": row["window_start"],
                            "offset": row.get(
                                "offset",
                                (row["target"] - row["window_start"]) // 2),
                            "subset_weighted_gap": float(margin),
                        }
                        for row, margin in ranked[:12]
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
    previous_payload = load_json(SELECTED_REFERENCE_HORIZON_SOURCE)
    labels = tuple(label_tuple(label) for label in local_payload["outside_labels"])
    lp_vector = np.asarray(
        lp_payload["selected_lp_effective_vector"], dtype=np.float64)
    local_rows_by_residue = {
        int(row["n_mod_143"]): row
        for row in local_payload["local_residue_rows"]
    }
    if set(FRESH_UNSEEN_WINDOW_SPECS) & set(tuple(row) for row in FRESH_WINDOW_SPECS):
        raise AssertionError("fresh unseen windows overlap prior fresh windows")

    targets, metadata = collect_targets(FRESH_UNSEEN_WINDOW_SPECS)
    references = tuple(int(reference) for reference in DEFICIT_REFERENCES)
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=tuple(sorted(set(targets) | set(references))),
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=40)
    rows, fresh_target_rows = build_comparison_rows(
        targets,
        metadata,
        references,
        profile,
        labels,
        local_rows_by_residue,
        lp_vector)

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
    fresh_deficits = [
        row for row in fresh_target_rows if not row["dominant_floor_passes"]]

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lp_cone_audit": str(LP_SOURCE.relative_to(ROOT)),
        "source_selected_reference_horizon_audit": str(
            SELECTED_REFERENCE_HORIZON_SOURCE.relative_to(ROOT)),
        "previous_selected_reference_horizon_source_commit": (
            previous_payload["source_commit"]),
        "prior_fresh_window_specs": [list(row) for row in FRESH_WINDOW_SPECS],
        "fresh_unseen_window_specs": [
            list(row) for row in FRESH_UNSEEN_WINDOW_SPECS],
        "selected_deficit_references": list(references),
        "fresh_target_count": len(targets),
        "comparison_row_count": len(rows),
        "fresh_deficit_target_count": len(fresh_deficits),
        "fresh_deficit_targets_first_20": fresh_deficits[:20],
        "outside_labels": [list(label) for label in labels],
        "watchlist_labels": [list(label) for label in WATCHLIST_LABELS],
        "status_boundary": (
            "finite fresh unseen window audit only; the smallest-subset scan "
            "is post-hoc diagnostic and proves no selected-stress theorem, "
            "signed correlation theorem, pointwise character-sum theorem, or "
            "Goldbach theorem."),
        "mechanism": (
            "Use later windows not used in the watchlist selection/replay "
            "lane. For every fresh target and selected deficit reference, "
            "compare locally centered channel values by subtracting the "
            "target-reference local q286 vector before applying the frozen LP "
            "weights. No channel selection or refitting is performed."),
        "prediction": (
            "If Kevin's fixed four-channel watchlist is a reusable "
            "distributed signed-correlation cone, it should stay positive "
            "against all selected deficit references on these unseen windows. "
            "Scalar (3,1), the no-(3,1) watchlist, and the full 17-channel LP "
            "are reported as falsifier comparators."),
        "falsifier": (
            "Any nonpositive watchlist margin on an unseen fresh target "
            "against a selected deficit reference falsifies this finite "
            "fresh-window generalization. Deficit fresh targets are recorded "
            "separately and would block promotion to a clear-target theorem."),
        "subset_results": subset_results,
        "reference_results": summarize_by_reference(references, rows, labels),
        "channel_summary_rows": channel_summaries(labels, rows),
        "smallest_positive_fixed_subset": smallest_positive_subset(labels, rows),
        "scalar_3_1_passes_unseen_windows": subset_by_name[
            "scalar_3_1"]["all_targets_pass"],
        "kevin_watchlist_4_passes_unseen_windows": subset_by_name[
            "kevin_watchlist_4"]["all_targets_pass"],
        "kevin_watchlist_without_3_1_passes_unseen_windows": subset_by_name[
            "kevin_watchlist_without_3_1"]["all_targets_pass"],
        "frozen_full_17_lp_passes_unseen_windows": subset_by_name[
            "frozen_full_17_lp"]["all_targets_pass"],
        "decision": (
            "Read the watchlist pass flag and any failing rows. A pass "
            "strengthens the fixed watchlist cone beyond the reused fresh "
            "windows; a failure clips it to the earlier selected-reference "
            "horizons. This receipt remains finite and cannot establish "
            "Goldbach or an asymptotic signed-correlation theorem."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
