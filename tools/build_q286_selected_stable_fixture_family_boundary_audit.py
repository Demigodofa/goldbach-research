"""Audit the q286 selected-stable fixture family boundary.

This receipt answers the narrow question raised after the broad stress
falsifier: whether centered (3,1) should be treated as a stress-classifier
lemma.  It uses only existing checked receipts and fits no new channel
coefficients.

Finite evidence only: this proves no selected-stress theorem, broad stress
theorem, signed correlation theorem, pointwise character-sum theorem, or
Goldbach theorem.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-selected-stable-fixture-family-boundary-audit.json"

PROVENANCE = EVIDENCE / "q286-selected-deficit-provenance-audit.json"
SUBCLASS = EVIDENCE / "q286-selected-stress-subclass-audit.json"
SUBCLASS_CHANNEL = (
    EVIDENCE / "q286-selected-stress-subclass-channel-decomposition.json")
ADDITIONAL = (
    EVIDENCE / "q286-additional-stress-reference-generalization-audit.json")
SCOPE_FORK = EVIDENCE / "q286-selected-reference-scope-fork-audit.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def subset_result(scope, name):
    return next(row for row in scope["subset_results"] if row["name"] == name)


def channel_result(scope, label_key):
    return next(
        row for row in scope["channel_summary_rows"]
        if row["label_key"] == label_key)


def keyed(rows, key="target"):
    return {row[key]: row for row in rows}


def selected_rows(provenance, subclass):
    subclass_by_target = {}
    for row in subclass["selected_deficit_references"]:
        subclass_by_target[row["target"]] = row["subclass"]

    rows = []
    for row in provenance["selected_deficit_rows"]:
        rows.append({
            "target": row["target"],
            "target_mod_143": row["target_mod_143"],
            "target_mod_286": row["target_mod_286"],
            "subclass": subclass_by_target[row["target"]],
            "centered_3_1_rank_low_to_high": (
                row["centered_3_1_rank_low_to_high"]),
            "centered_3_1_weighted_value": (
                row["centered_3_1_weighted_value"]),
            "selected_fixture_dominant_floor_passes": (
                row["selected_fixture_dominant_floor_passes"]),
            "selected_fixture_dominant_margin_to_floor": (
                row["selected_fixture_dominant_margin_to_floor"]),
            "stable_core_floor_passes": row["stable_core_floor_passes"],
            "stable_core_margin_to_floor": row[
                "stable_core_margin_to_floor"],
            "volatile_rim_sum_to_principal": row[
                "volatile_rim_sum_to_principal"],
            "volatile_clause_count": row["volatile_clause_count"],
            "volatile_minimum_clause_size": row[
                "volatile_minimum_clause_size"],
            "volatile_necessary_channels": row[
                "volatile_necessary_channels"],
        })
    return rows


def subclass_rows(subclass_channel):
    rows = []
    for scope in subclass_channel["subclass_results"]:
        scalar = subset_result(scope, "scalar_3_1")
        watchlist = subset_result(scope, "kevin_watchlist_4")
        without = subset_result(scope, "kevin_watchlist_without_3_1")
        full_lp = subset_result(scope, "frozen_full_17_lp")
        ch_3_1 = channel_result(scope, "3,1")
        rows.append({
            "subclass": scope["subclass"],
            "references": scope["references"],
            "comparison_count": scope["comparison_count"],
            "scalar_3_1_failures": scalar["failing_target_count"],
            "scalar_3_1_minimum": scalar[
                "weighted_gap_summary"]["minimum"],
            "scalar_3_1_mean": scalar["weighted_gap_summary"]["mean"],
            "kevin_watchlist_failures": watchlist[
                "failing_target_count"],
            "kevin_watchlist_minimum": watchlist[
                "weighted_gap_summary"]["minimum"],
            "watchlist_without_3_1_failures": without[
                "failing_target_count"],
            "watchlist_without_3_1_minimum": without[
                "weighted_gap_summary"]["minimum"],
            "frozen_full_17_lp_failures": full_lp[
                "failing_target_count"],
            "frozen_full_17_lp_minimum": full_lp[
                "weighted_gap_summary"]["minimum"],
            "channel_3_1_positive_count": ch_3_1["positive_count"],
            "channel_3_1_negative_count": ch_3_1["negative_count"],
            "channel_3_1_positive_margin_share": ch_3_1[
                "positive_margin_share"],
            "passing_singleton_count": scope[
                "smallest_positive_fixed_subset"][
                    "passing_subset_count_at_minimum_size"],
            "best_singletons": [
                {
                    "label_keys": row["label_keys"],
                    "minimum_target_margin": row[
                        "minimum_target_margin"],
                    "average_target_margin": row[
                        "average_target_margin"],
                }
                for row in scope["smallest_positive_fixed_subset"][
                    "best_subsets_by_minimum_margin"]
            ],
        })
    return rows


def target_scope_rows(subclass_channel):
    rows = []
    for scope in subclass_channel["target_scope_results"]:
        ch_3_1 = channel_result(scope, "3,1")
        rows.append({
            "scope_id": scope["scope_id"],
            "target_count": scope["target_count"],
            "comparison_count": scope["comparison_count"],
            "scalar_3_1_positive_count": ch_3_1["positive_count"],
            "scalar_3_1_negative_count": ch_3_1["negative_count"],
            "scalar_3_1_minimum": ch_3_1["minimum_margin"],
            "scalar_3_1_mean": ch_3_1["average_margin"],
            "scalar_3_1_positive_margin_share": ch_3_1[
                "positive_margin_share"],
        })
    return rows


def candidate_predicates(selected, subclass_channel, scope_fork):
    selected_targets = [row["target"] for row in selected]
    bottom_7 = [
        row["target"] for row in selected
        if row["centered_3_1_rank_low_to_high"] <= 7
    ]
    volatile = [
        row["target"] for row in selected
        if row["subclass"] == "volatile_overturn"
    ]
    stable = [
        row["target"] for row in selected
        if row["subclass"] == "stable_core_deficit"
    ]
    scope_cmp = scope_fork["scope_comparison"]
    total_selected_comparisons = (
        scope_fork["selected_reference_fixture"][
            "total_subclass_comparison_count"])
    return [
        {
            "name": "selected_fixture_dominant_floor_failure",
            "pre_existing_source_feature": True,
            "threshold_or_predicate": (
                "dominant_floor_passes == false in the selected "
                "stable-core classification fixture"),
            "captures_selected_count": len(selected_targets),
            "captured_selected_targets": selected_targets,
            "missed_selected_targets": [],
            "excludes_broad_full_nonpositive": True,
            "broad_support_evidence": (
                "scope fork overlap with broad full_nonpositive fixture is 0"),
            "finite_status": "supported_fixture_boundary",
            "theorem_boundary": (
                "fixture-bound; circular until converted into a prospective "
                "reference-generation rule and holdout-tested"),
        },
        {
            "name": "centered_3_1_selected_reference_classifier",
            "pre_existing_source_feature": True,
            "threshold_or_predicate": (
                "fresh unseen target-reference weighted centered (3,1) "
                "gap > 0 for the selected references"),
            "captures_selected_count": len(selected_targets),
            "captured_selected_targets": selected_targets,
            "missed_selected_targets": [],
            "selected_comparison_failures": (
                scope_cmp["selected_scalar_3_1_failures"]),
            "selected_comparison_count": total_selected_comparisons,
            "broad_comparison_failures": (
                scope_cmp["broad_scalar_3_1_failures"]),
            "finite_status": "supported_selected_reference_lemma",
            "theorem_boundary": (
                "not a broad stress theorem; broad full_nonpositive "
                "promotion is already falsified"),
        },
        {
            "name": "volatile_overturn",
            "pre_existing_source_feature": True,
            "threshold_or_predicate": (
                "stable core passes but volatile rim restores the deficit"),
            "captures_selected_count": len(volatile),
            "captured_selected_targets": volatile,
            "missed_selected_targets": sorted(set(selected_targets) - set(
                volatile)),
            "finite_status": "falsified_as_whole_selected_family",
            "theorem_boundary": (
                "valid subclass only; misses stable-core deficits"),
        },
        {
            "name": "stable_core_deficit",
            "pre_existing_source_feature": True,
            "threshold_or_predicate": "stable_core_floor_passes == false",
            "captures_selected_count": len(stable),
            "captured_selected_targets": stable,
            "missed_selected_targets": sorted(set(selected_targets) - set(
                stable)),
            "finite_status": "falsified_as_whole_selected_family",
            "theorem_boundary": (
                "valid subclass only; misses volatile-overturn deficits"),
        },
        {
            "name": "centered_3_1_bottom_7_in_selected_fixture",
            "pre_existing_source_feature": False,
            "threshold_or_predicate": (
                "centered_3_1_rank_low_to_high <= 7 inside the selected "
                "stable/volatile fixture"),
            "captures_selected_count": len(bottom_7),
            "captured_selected_targets": bottom_7,
            "missed_selected_targets": sorted(set(selected_targets) - set(
                bottom_7)),
            "finite_status": "post_hoc_candidate",
            "theorem_boundary": (
                "interesting rank feature only; must be frozen before any "
                "new windows or references are used"),
        },
        {
            "name": "target_residue_single_class",
            "pre_existing_source_feature": True,
            "threshold_or_predicate": "one target residue modulo 143 or 286",
            "captures_selected_count": max(
                [sum(1 for row in selected if row["target_mod_143"] == r)
                 for r in {row["target_mod_143"] for row in selected}]
                or [0]),
            "captured_selected_targets": [],
            "missed_selected_targets": selected_targets,
            "finite_status": "no_simple_single_residue_family",
            "theorem_boundary": (
                "selected targets occupy multiple residues; residue alone is "
                "not the family boundary"),
        },
        {
            "name": "baseline_full_nonpositive",
            "pre_existing_source_feature": True,
            "threshold_or_predicate": (
                "full_action_to_principal_ratio <= 0 in the baseline "
                "filter-order fixture"),
            "captures_selected_count": (
                scope_cmp["selected_reference_overlap_count"]),
            "captured_selected_targets": (
                scope_fork["broad_full_nonpositive_fixture"][
                    "selected_reference_overlap"]),
            "missed_selected_targets": selected_targets,
            "finite_status": "falsified_broad_promotion",
            "theorem_boundary": (
                "does not contain the selected five and does not preserve "
                "the scalar/watchlist margins"),
        },
    ]


def main():
    provenance = load_json(PROVENANCE)
    subclass = load_json(SUBCLASS)
    subclass_channel = load_json(SUBCLASS_CHANNEL)
    additional = load_json(ADDITIONAL)
    scope_fork = load_json(SCOPE_FORK)

    selected = selected_rows(provenance, subclass)
    subclasses = subclass_rows(subclass_channel)
    scopes = target_scope_rows(subclass_channel)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "selected_deficit_provenance": str(PROVENANCE.relative_to(ROOT)),
            "selected_stress_subclass": str(SUBCLASS.relative_to(ROOT)),
            "selected_stress_subclass_channel_decomposition": str(
                SUBCLASS_CHANNEL.relative_to(ROOT)),
            "additional_stress_reference_generalization": str(
                ADDITIONAL.relative_to(ROOT)),
            "selected_reference_scope_fork": str(
                SCOPE_FORK.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite family-boundary audit only; no selected-stress theorem, "
            "broad stress theorem, signed correlation theorem, pointwise "
            "character-sum theorem, or Goldbach proof."),
        "question": (
            "Can centered (3,1), including the strong selected witness 13822, "
            "be treated as a stress-classifier lemma?"),
        "mechanism": (
            "Compare source predicates already present in checked q286 "
            "receipts.  Preserve the selected-stable fixture, its two "
            "selected-stress subclasses, and the broad full_nonpositive "
            "fixture as separate populations."),
        "selected_reference_rows": selected,
        "subclass_boundary_rows": subclasses,
        "fresh_unseen_scope_rows": scopes,
        "candidate_family_boundaries": candidate_predicates(
            selected, subclass_channel, scope_fork),
        "focus_reference_13822": next(
            row for row in selected if row["target"] == 13822),
        "broad_full_nonpositive_falsifier": {
            "additional_reference_count": additional[
                "additional_reference_count"],
            "comparison_row_count": additional["comparison_row_count"],
            "scalar_3_1_failure_count": additional[
                "full_nonpositive_scalar_3_1_failure_count"],
            "watchlist_failure_count": additional[
                "full_nonpositive_watchlist_failure_count"],
            "selected_reference_overlap_count": scope_fork[
                "scope_comparison"]["selected_reference_overlap_count"],
        },
        "decision": (
            "Centered (3,1) is supported as a finite selected-reference "
            "stress-classifier coordinate: it has zero failures across the "
            "3,030 checked selected-reference fresh-unseen comparisons and "
            "removing it from Kevin's watchlist creates selected-fixture "
            "failures.  Reference 13822 is a volatile-overturn witness with "
            "centered (3,1) rank 2 and weighted value "
            "-0.028592853507378977.  The result is not a broad stress lemma: "
            "the 89 additional full_nonpositive references produce 32,661 "
            "scalar (3,1) failures and have zero overlap with the selected "
            "five."),
        "next_obligation": (
            "Freeze a prospective selected-stable reference-generation rule "
            "or bottom-rank candidate before seeing new rows; otherwise move "
            "from classifier language to a signed correlation estimate."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
