"""Decompose selected-stress subclass margins across q286 outside channels.

The selected-stress subclass audit split the five selected deficit references
into stable-core-deficit and volatile-overturn mechanisms.  This receipt
replays the fresh unseen selected-reference comparisons and summarizes the
LP-weighted after-local contribution of every outside channel inside each
subclass.

Finite evidence only: subset scans are diagnostics.  They prove no selected
stress theorem, signed correlation theorem, pointwise character-sum theorem,
or Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-selected-stress-subclass-channel-decomposition.json"
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)
from tools.build_q286_centered_3_1_residue5_multichannel_horizon import (  # noqa: E402
    SCALAR_LABEL,
    WATCHLIST_LABELS,
    label_key,
)
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    label_tuple,
)
from tools.build_q286_fresh_window_channel_watchlist_audit import (  # noqa: E402
    FRESH_WINDOW_SPECS,
    collect_targets,
)
from tools.build_q286_watchlist_fresh_unseen_window_audit import (  # noqa: E402
    FRESH_UNSEEN_WINDOW_SPECS,
    build_comparison_rows,
    channel_summaries,
    smallest_positive_subset,
    summarize_subset,
)


SUBCLASS_SOURCE = EVIDENCE / "q286-selected-stress-subclass-audit.json"
FRESH_UNSEEN_SOURCE = EVIDENCE / "q286-watchlist-fresh-unseen-window-audit.json"
SEED_RESIDUES_MOD_143 = (38, 64)


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


def summarize_watchlist_removals(rows):
    out = []
    for removed in WATCHLIST_LABELS:
        kept = tuple(label for label in WATCHLIST_LABELS if label != removed)
        summary = summarize_subset(
            f"watchlist_without_{label_key(removed).replace(',', '_')}",
            kept,
            rows)
        out.append({
            "removed_label": list(removed),
            "removed_label_key": label_key(removed),
            "remaining_label_keys": summary["label_keys"],
            "passes": summary["all_targets_pass"],
            "failing_target_count": summary["failing_target_count"],
            "minimum_margin": summary["weighted_gap_summary"]["minimum"],
            "average_margin": summary["weighted_gap_summary"]["mean"],
            "maximum_margin": summary["weighted_gap_summary"]["maximum"],
            "first_failing_rows": summary["failing_rows"][:12],
        })
    return out


def safe_smallest_positive_subset(labels, rows):
    if not rows:
        return {
            "minimum_size": None,
            "checked_subset_count_at_minimum_size": 0,
            "passing_subset_count_at_minimum_size": 0,
            "best_subsets_by_minimum_margin": [],
            "post_hoc_diagnostic_only": True,
            "empty_scope": True,
        }
    return smallest_positive_subset(labels, rows)


def summarize_reference_channels(rows, labels):
    out = []
    for row in channel_summaries(labels, rows):
        out.append({
            "label": row["label"],
            "label_key": row["label_key"],
            "positive_count": row["positive_count"],
            "negative_count": row["negative_count"],
            "zero_count": row["zero_count"],
            "minimum_margin": row["weighted_gap_summary"]["minimum"],
            "average_margin": row["weighted_gap_summary"]["mean"],
            "maximum_margin": row["weighted_gap_summary"]["maximum"],
            "positive_weighted_sum": row["positive_weighted_sum"],
            "negative_weighted_sum": row["negative_weighted_sum"],
            "positive_margin_share": row["positive_margin_share"],
            "tightest_rows": row["tightest_rows"][:5],
            "widest_rows": row["widest_rows"][-5:],
        })
    return out


def summarize_subclass(subclass_row, rows, labels):
    subclass = subclass_row["subclass"]
    references = set(int(reference) for reference in subclass_row["references"])
    subclass_rows = [
        row for row in rows if int(row["reference_target"]) in references]
    subset_results = [
        summarize_subset("scalar_3_1", (SCALAR_LABEL,), subclass_rows),
        summarize_subset("kevin_watchlist_4", WATCHLIST_LABELS, subclass_rows),
        summarize_subset(
            "kevin_watchlist_without_3_1",
            tuple(label for label in WATCHLIST_LABELS
                  if label != SCALAR_LABEL),
            subclass_rows),
        summarize_subset("frozen_full_17_lp", labels, subclass_rows),
    ]
    subset_by_name = {row["name"]: row for row in subset_results}
    smallest = safe_smallest_positive_subset(labels, subclass_rows)
    return {
        "subclass": subclass,
        "references": sorted(references),
        "comparison_count": len(subclass_rows),
        "subset_results": subset_results,
        "watchlist_removal_results": summarize_watchlist_removals(
            subclass_rows),
        "channel_summary_rows": summarize_reference_channels(
            subclass_rows, labels),
        "smallest_positive_fixed_subset": smallest,
        "scalar_3_1_passes": subset_by_name["scalar_3_1"][
            "all_targets_pass"],
        "kevin_watchlist_4_passes": subset_by_name["kevin_watchlist_4"][
            "all_targets_pass"],
        "watchlist_without_3_1_passes": subset_by_name[
            "kevin_watchlist_without_3_1"]["all_targets_pass"],
        "frozen_full_17_lp_passes": subset_by_name["frozen_full_17_lp"][
            "all_targets_pass"],
    }


def summarize_target_scope(scope_id, scope_description, target_filter, rows,
                           labels):
    scope_rows = [row for row in rows if target_filter(row)]
    scope_targets = sorted({int(row["target"]) for row in scope_rows})
    subset_results = [
        summarize_subset("scalar_3_1", (SCALAR_LABEL,), scope_rows),
        summarize_subset("kevin_watchlist_4", WATCHLIST_LABELS, scope_rows),
        summarize_subset(
            "kevin_watchlist_without_3_1",
            tuple(label for label in WATCHLIST_LABELS
                  if label != SCALAR_LABEL),
            scope_rows),
        summarize_subset("frozen_full_17_lp", labels, scope_rows),
    ]
    subset_by_name = {row["name"]: row for row in subset_results}
    return {
        "scope_id": scope_id,
        "scope_description": scope_description,
        "target_count": len(scope_targets),
        "targets": scope_targets,
        "comparison_count": len(scope_rows),
        "subset_results": subset_results,
        "watchlist_removal_results": summarize_watchlist_removals(scope_rows),
        "channel_summary_rows": summarize_reference_channels(
            scope_rows, labels),
        "smallest_positive_fixed_subset": safe_smallest_positive_subset(
            labels, scope_rows),
        "scalar_3_1_passes": subset_by_name["scalar_3_1"][
            "all_targets_pass"],
        "kevin_watchlist_4_passes": subset_by_name["kevin_watchlist_4"][
            "all_targets_pass"],
        "watchlist_without_3_1_passes": subset_by_name[
            "kevin_watchlist_without_3_1"]["all_targets_pass"],
        "frozen_full_17_lp_passes": subset_by_name["frozen_full_17_lp"][
            "all_targets_pass"],
    }


def target_scope_results(rows, labels):
    return [
        summarize_target_scope(
            "fresh_unseen_prior_seed_residue_targets",
            "Later fresh-unseen targets with n mod 143 in prior seed residues {38, 64}; this is not the earlier 12-row same-window zero-local seed population.",
            lambda row: int(row["target_mod_143"]) in SEED_RESIDUES_MOD_143,
            rows,
            labels),
        summarize_target_scope(
            "fresh_unseen_seed_residue_38",
            "Later fresh-unseen targets with n mod 143 = 38.",
            lambda row: int(row["target_mod_143"]) == 38,
            rows,
            labels),
        summarize_target_scope(
            "fresh_unseen_seed_residue_64",
            "Later fresh-unseen targets with n mod 143 = 64.",
            lambda row: int(row["target_mod_143"]) == 64,
            rows,
            labels),
        summarize_target_scope(
            "fresh_unseen_nonseed_targets",
            "Later fresh-unseen targets outside prior seed residues 38 and 64.",
            lambda row: int(row["target_mod_143"])
            not in SEED_RESIDUES_MOD_143,
            rows,
            labels),
    ]


def aggregate_channel_table(subclass_results):
    rows = []
    for subclass in subclass_results:
        for row in subclass["channel_summary_rows"]:
            rows.append({
                "subclass": subclass["subclass"],
                "label_key": row["label_key"],
                "positive_count": row["positive_count"],
                "negative_count": row["negative_count"],
                "minimum_margin": row["minimum_margin"],
                "average_margin": row["average_margin"],
                "maximum_margin": row["maximum_margin"],
                "positive_margin_share": row["positive_margin_share"],
            })
    return sorted(rows, key=lambda row: (row["subclass"], row["label_key"]))


def main():
    subclass_payload = load_json(SUBCLASS_SOURCE)
    fresh_unseen_payload = load_json(FRESH_UNSEEN_SOURCE)
    local_payload = load_json(LOCAL_SOURCE)
    lp_payload = load_json(LP_SOURCE)

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
    references = tuple(
        int(row["target"])
        for row in subclass_payload["selected_deficit_references"])
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
    subclass_results = [
        summarize_subclass(row, rows, labels)
        for row in subclass_payload["subclass_results"]
    ]
    target_scopes = target_scope_results(rows, labels)
    target_scope_by_id = {row["scope_id"]: row for row in target_scopes}

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "selected_stress_subclass": str(SUBCLASS_SOURCE.relative_to(ROOT)),
            "fresh_unseen_watchlist": str(FRESH_UNSEEN_SOURCE.relative_to(ROOT)),
            "local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
            "low_frequency_lp_cone": str(LP_SOURCE.relative_to(ROOT)),
        },
        "prior_fresh_unseen_source_commit":
            fresh_unseen_payload["source_commit"],
        "fresh_unseen_window_specs": [
            list(row) for row in FRESH_UNSEEN_WINDOW_SPECS],
        "seed_residues_mod_143": list(SEED_RESIDUES_MOD_143),
        "fresh_unseen_seed_scope_note": (
            "The 12 zero-local seed targets belong to the earlier same-window "
            "population.  These later fresh-unseen windows contain no target "
            "with residue 38 mod 143 and five targets with residue 64 mod "
            "143; empty seed-residue scopes are reported rather than "
            "silently merged."),
        "selected_deficit_references": list(references),
        "outside_labels": [list(label) for label in labels],
        "watchlist_labels": [list(label) for label in WATCHLIST_LABELS],
        "fresh_target_count": len(targets),
        "comparison_row_count": len(rows),
        "fresh_deficit_target_count": len(
            [row for row in fresh_target_rows
             if not row["dominant_floor_passes"]]),
        "status_boundary": (
            "finite subclass channel-decomposition audit only; smallest "
            "subsets, channel shares, seed/nonseed splits, and selected-stress "
            "subclasses are post-hoc diagnostics and prove no selected-stress "
            "theorem, signed correlation theorem, pointwise character-sum "
            "theorem, or Goldbach proof."),
        "mechanism": (
            "Replay fresh unseen selected-reference comparisons, subtract the "
            "target-reference local q286 vector, apply frozen LP weights, and "
            "summarize every outside channel separately for each selected "
            "stress subclass."),
        "prediction": (
            "If both selected-stress subclasses share one scalar signed "
            "correlation coordinate, the same smallest fixed subset should "
            "survive separately in each subclass. If channel shares differ, "
            "the theorem route must explain subclass-dependent channel "
            "balance."),
        "falsifier": (
            "A subclass where scalar (3,1) or the fixed watchlist has a "
            "nonpositive fresh unseen margin falsifies that finite subclass "
            "gate. Different smallest subsets do not falsify the gate, but "
            "they falsify a single-channel explanation for all mechanism "
            "details."),
        "target_scope_results": target_scopes,
        "subclass_results": subclass_results,
        "channel_table": aggregate_channel_table(subclass_results),
        "decision": (
            "Both selected-stress subclasses keep scalar (3,1) and Kevin's "
            "four-channel watchlist positive on fresh unseen comparisons. "
            "Scalar (3,1) is a passing singleton in each subclass and its "
            "removal from the four-channel watchlist makes both subclasses "
            "fail, but it is not the unique passing singleton in every "
            "subclass.  The later fresh-unseen batch contains "
            f"{target_scope_by_id['fresh_unseen_prior_seed_residue_targets']['target_count']} "
            "targets in prior seed residues 38/64 and "
            f"{target_scope_by_id['fresh_unseen_nonseed_targets']['target_count']} "
            "targets outside those residues; the 12 zero-local seed targets "
            "belong to the earlier same-window audit.  Channel shares differ "
            "enough that a theorem still needs a signed correlation estimate "
            "rather than a local or full-17 LP explanation."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
