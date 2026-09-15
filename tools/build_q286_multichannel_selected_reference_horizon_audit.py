"""Audit frozen multichannel margins on selected-reference horizons.

The residue-5 multichannel horizon rescued a scalar (3,1) failure against
reference 164598.  This receipt repeats the same style of horizon test for all
five selected stable/volatile dominant-floor failure references, using each
reference's tightest same-residue available comparison as the horizon center.

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
    channel_summaries,
    finite_summary,
    label_key,
    smallest_positive_subset,
    subset_margin,
    summarize_subset,
)
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    contribution_map,
    label_tuple,
)


EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-multichannel-selected-reference-horizon-audit.json"

AVAILABLE_SOURCE = (
    EVIDENCE
    / "q286-centered-3-1-available-same-residue-population-audit.json")
RESIDUE5_MULTICHANNEL_SOURCE = (
    EVIDENCE / "q286-centered-3-1-residue5-multichannel-horizon.json")

STEP = 286
OFFSET_RADIUS = 50


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def horizon_targets(center):
    return tuple(
        int(center) + STEP * offset
        for offset in range(-OFFSET_RADIUS, OFFSET_RADIUS + 1))


def all_available_scope(deficit_row):
    return next(
        row for row in deficit_row["scope_rows"]
        if row["scope_id"] == "same_residue_all_available_nonselection_targets")


def horizon_specs(available_payload):
    specs = []
    for row in available_payload["deficit_rows"]:
        deficit = row["deficit"]
        scope = all_available_scope(row)
        center = int(scope["minimum_comparison_target"])
        reference = int(deficit["target"])
        if center % 143 != reference % 143:
            raise AssertionError(
                f"horizon center {center} mismatches reference {reference}")
        specs.append({
            "reference_target": reference,
            "reference_mod_143": reference % 143,
            "reference_mod_286": reference % 286,
            "horizon_center": center,
            "center_mod_143": center % 143,
            "center_mod_286": center % 286,
            "source_scope_id": scope["scope_id"],
            "source_minimum_weighted_3_1_gap": (
                scope["weighted_gap_summary"]["minimum"]),
            "source_minimum_weighted_centered_3_1_value": (
                scope["minimum_weighted_centered_channel_value"]),
            "horizon_targets": list(horizon_targets(center)),
        })
    return sorted(specs, key=lambda item: item["reference_target"])


def build_comparison_row(spec, target, offset, profile, labels,
                         local_rows_by_residue, lp_vector,
                         reference_contribs, reference_local):
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
        "reference_target": spec["reference_target"],
        "reference_mod_143": spec["reference_mod_143"],
        "target": int(target),
        "target_mod_143": int(target) % 143,
        "target_mod_286": int(target) % 286,
        "horizon_center": spec["horizon_center"],
        "offset_from_center_in_286_steps": int(offset),
        "weighted_gap_by_label": {
            key: value["lp_weighted_gap"] for key, value in by_label.items()
        },
        "channel_rows": list(by_label.values()),
    }


def summarize_reference(spec, rows, labels):
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
    return {
        **{key: value for key, value in spec.items()
           if key != "horizon_targets"},
        "target_count": len(rows),
        "subset_results": subset_results,
        "channel_summary_rows": channel_summaries(labels, rows),
        "scalar_3_1_passes_horizon": subset_by_name[
            "scalar_3_1"]["all_targets_pass"],
        "kevin_watchlist_4_passes_horizon": subset_by_name[
            "kevin_watchlist_4"]["all_targets_pass"],
        "kevin_watchlist_without_3_1_passes_horizon": subset_by_name[
            "kevin_watchlist_without_3_1"]["all_targets_pass"],
        "frozen_full_17_lp_passes_horizon": subset_by_name[
            "frozen_full_17_lp"]["all_targets_pass"],
    }


def summarize_subset_across_references(name, labels, rows):
    margins = [subset_margin(row, labels) for row in rows]
    enriched = []
    for row, margin in zip(rows, margins):
        enriched.append({
            "reference_target": row["reference_target"],
            "target": row["target"],
            "horizon_center": row["horizon_center"],
            "offset_from_center_in_286_steps": (
                row["offset_from_center_in_286_steps"]),
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
        "failing_rows": failing[:40],
        "weighted_gap_summary": finite_summary(margins),
        "tightest_rows": ranked[:20],
        "widest_rows": ranked[-20:],
    }


def smallest_positive_subset_across_references(labels, rows):
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
                            "horizon_center": row["horizon_center"],
                            "offset_from_center_in_286_steps": (
                                row["offset_from_center_in_286_steps"]),
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
    available_payload = load_json(AVAILABLE_SOURCE)
    labels = tuple(label_tuple(label) for label in local_payload["outside_labels"])
    lp_vector = np.asarray(
        lp_payload["selected_lp_effective_vector"], dtype=np.float64)
    local_rows_by_residue = {
        int(row["n_mod_143"]): row
        for row in local_payload["local_residue_rows"]
    }

    specs = horizon_specs(available_payload)
    expected_references = tuple(sorted(int(target) for target in DEFICIT_REFERENCES))
    actual_references = tuple(spec["reference_target"] for spec in specs)
    if actual_references != expected_references:
        raise AssertionError((actual_references, expected_references))

    sample_targets = set()
    for spec in specs:
        sample_targets.add(spec["reference_target"])
        sample_targets.update(spec["horizon_targets"])
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=tuple(sorted(sample_targets)),
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=40)

    reference_results = []
    all_comparison_rows = []
    for spec in specs:
        reference_contribs = contribution_map(
            profile["target_rows"][spec["reference_target"]])
        reference_local = np.asarray(
            local_rows_by_residue[
                spec["reference_target"] % 143]["local_delta_vector"],
            dtype=np.float64)
        rows = [
            build_comparison_row(
                spec,
                target,
                offset,
                profile,
                labels,
                local_rows_by_residue,
                lp_vector,
                reference_contribs,
                reference_local)
            for offset, target in zip(
                range(-OFFSET_RADIUS, OFFSET_RADIUS + 1),
                spec["horizon_targets"])
        ]
        if any(row["target_mod_143"] != spec["reference_mod_143"]
               for row in rows):
            raise AssertionError("horizon contains a nonmatching residue")
        reference_results.append(summarize_reference(spec, rows, labels))
        all_comparison_rows.extend(rows)

    aggregate_subset_results = [
        summarize_subset_across_references(
            "scalar_3_1", (SCALAR_LABEL,), all_comparison_rows),
        summarize_subset_across_references(
            "kevin_watchlist_4", WATCHLIST_LABELS, all_comparison_rows),
        summarize_subset_across_references(
            "kevin_watchlist_without_3_1",
            tuple(label for label in WATCHLIST_LABELS if label != SCALAR_LABEL),
            all_comparison_rows),
        summarize_subset_across_references(
            "frozen_full_17_lp", labels, all_comparison_rows),
    ]
    aggregate_by_name = {row["name"]: row for row in aggregate_subset_results}

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lp_cone_audit": str(LP_SOURCE.relative_to(ROOT)),
        "source_available_same_residue_population_audit": str(
            AVAILABLE_SOURCE.relative_to(ROOT)),
        "source_residue5_multichannel_horizon": str(
            RESIDUE5_MULTICHANNEL_SOURCE.relative_to(ROOT)),
        "step": STEP,
        "offset_radius": OFFSET_RADIUS,
        "selected_reference_count": len(specs),
        "horizon_target_count_per_reference": 2 * OFFSET_RADIUS + 1,
        "comparison_row_count": len(all_comparison_rows),
        "outside_labels": [list(label) for label in labels],
        "watchlist_labels": [list(label) for label in WATCHLIST_LABELS],
        "status_boundary": (
            "finite selected-reference multichannel horizon audit only; the "
            "smallest-subset scan is post-hoc diagnostic and proves no "
            "selected-stress theorem, signed correlation theorem, pointwise "
            "character-sum theorem, or Goldbach theorem."),
        "mechanism": (
            "Each selected deficit reference is paired with the tightest "
            "same-residue available comparison already recorded by the "
            "centered (3,1) population audit. The receipt scans center + "
            "286*k for -50<=k<=50, so the q286 local vector cancels within "
            "each reference horizon. Frozen LP-weighted after-local channel "
            "gaps are aggregated without refitting."),
        "prediction": (
            "If the residue-5 rescue reflects a reusable distributed "
            "signed-correlation cone, Kevin's pre-existing watchlist and the "
            "frozen full 17-channel LP vector should remain positive across "
            "all selected-reference horizons, even when scalar (3,1) fails."),
        "falsifier": (
            "Any nonpositive margin in a pre-existing subset falsifies that "
            "subset as an all-selected-reference horizon rescue. A passing "
            "post-hoc subset is diagnostic only until a non-post-hoc channel "
            "selection rule is supplied."),
        "reference_results": reference_results,
        "aggregate_subset_results": aggregate_subset_results,
        "aggregate_channel_summary_rows": channel_summaries(
            labels, all_comparison_rows),
        "aggregate_smallest_positive_fixed_subset": (
            smallest_positive_subset_across_references(
                labels, all_comparison_rows)),
        "scalar_3_1_passes_all_horizons": aggregate_by_name[
            "scalar_3_1"]["all_targets_pass"],
        "kevin_watchlist_4_passes_all_horizons": aggregate_by_name[
            "kevin_watchlist_4"]["all_targets_pass"],
        "kevin_watchlist_without_3_1_passes_all_horizons": aggregate_by_name[
            "kevin_watchlist_without_3_1"]["all_targets_pass"],
        "frozen_full_17_lp_passes_all_horizons": aggregate_by_name[
            "frozen_full_17_lp"]["all_targets_pass"],
        "decision": (
            "Read the aggregate pass flags and per-reference failures. A "
            "watchlist/full-LP pass preserves the distributed-cone route "
            "across alternate selected deficit references; a failure clips the "
            "corresponding frozen multichannel rescue to narrower fixtures."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
