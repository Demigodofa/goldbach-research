"""Consolidate the q286 selected-reference versus broad-stress fork.

Several receipts now say two things that can look contradictory if read too
quickly: scalar (3,1) is load-bearing for the selected five references, but it
fails badly on additional full_nonpositive references.  This audit records the
scope fork from existing checked receipts without fitting a new classifier.

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
OUT = EVIDENCE / "q286-selected-reference-scope-fork-audit.json"

PROVENANCE = EVIDENCE / "q286-selected-deficit-provenance-audit.json"
SUBCLASS_CHANNEL = (
    EVIDENCE / "q286-selected-stress-subclass-channel-decomposition.json")
ADDITIONAL = (
    EVIDENCE / "q286-additional-stress-reference-generalization-audit.json")
STRESS_CLASS = EVIDENCE / "q286-centered-3-1-stress-class-audit.json"


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


def sum_subset_failures(subclass_results, subset_name):
    return sum(
        subset_result(subclass, subset_name)["failing_target_count"]
        for subclass in subclass_results)


def selected_summary(provenance, subclass_channel):
    selected_rows = provenance["selected_deficit_rows"]
    subclasses = {
        row["subclass"]: row for row in subclass_channel["subclass_results"]
    }
    subclass_facts = {}
    for name, row in subclasses.items():
        scalar = subset_result(row, "scalar_3_1")
        watchlist = subset_result(row, "kevin_watchlist_4")
        without_3_1 = subset_result(row, "kevin_watchlist_without_3_1")
        subclass_facts[name] = {
            "references": row["references"],
            "comparison_count": row["comparison_count"],
            "scalar_3_1_failures": scalar["failing_target_count"],
            "scalar_3_1_minimum": scalar["weighted_gap_summary"][
                "minimum"],
            "watchlist_failures": watchlist["failing_target_count"],
            "watchlist_minimum": watchlist["weighted_gap_summary"][
                "minimum"],
            "watchlist_without_3_1_failures": without_3_1[
                "failing_target_count"],
            "passing_singletons": row["smallest_positive_fixed_subset"][
                "passing_subset_count_at_minimum_size"],
        }
    return {
        "source_predicate": (
            provenance["selected_fixture"]["deficit_source_predicate"]),
        "references": provenance["selected_fixture"][
            "selected_deficit_targets"],
        "reference_count": len(selected_rows),
        "in_baseline_filter_window_count": sum(
            1 for row in selected_rows if row["in_baseline_filter_window"]),
        "in_selected_stable_fixture_count": sum(
            1 for row in selected_rows if row["in_selected_stable_fixture"]),
        "dominant_floor_failures_in_selected_fixture": sum(
            1 for row in selected_rows
            if not row["selected_fixture_dominant_floor_passes"]),
        "centered_3_1_rank_low_to_high": [
            row["centered_3_1_rank_low_to_high"] for row in selected_rows],
        "centered_3_1_weighted_values": [
            row["centered_3_1_weighted_value"] for row in selected_rows],
        "subclass_facts": subclass_facts,
        "total_subclass_comparison_count": sum(
            row["comparison_count"]
            for row in subclass_channel["subclass_results"]),
        "total_scalar_3_1_failures": sum_subset_failures(
            subclass_channel["subclass_results"], "scalar_3_1"),
        "total_watchlist_failures": sum_subset_failures(
            subclass_channel["subclass_results"], "kevin_watchlist_4"),
        "total_watchlist_without_3_1_failures": sum_subset_failures(
            subclass_channel["subclass_results"],
            "kevin_watchlist_without_3_1"),
    }


def broad_summary(additional, stress_class):
    full = next(
        row for row in additional["class_results"]
        if row["class_id"] == "full_nonpositive")
    active = next(
        row for row in additional["class_results"]
        if row["class_id"] == "active_nonrescued")
    return {
        "source_predicate": "baseline full_nonpositive filter-order fixture",
        "reference_count": additional["additional_reference_count"],
        "comparison_count": additional["comparison_row_count"],
        "selected_reference_overlap": additional[
            "selected_deficit_references_in_full_nonpositive"],
        "fresh_target_count": additional["fresh_target_count"],
        "scalar_3_1_failures": additional[
            "full_nonpositive_scalar_3_1_failure_count"],
        "scalar_3_1_minimum": subset_result(
            full, "scalar_3_1")["weighted_gap_summary"]["minimum"],
        "watchlist_failures": additional[
            "full_nonpositive_watchlist_failure_count"],
        "watchlist_minimum": subset_result(
            full, "kevin_watchlist_4")["weighted_gap_summary"]["minimum"],
        "reference_pass_counts": full["reference_pass_counts"],
        "active_nonrescued_reference_pass_counts":
            active["reference_pass_counts"],
        "scalar_order_full_nonpositive_at_or_above_fresh_min_count":
            stress_class[
                "channel_3_1_full_nonpositive_at_or_above_fresh_min_count"],
        "scalar_order_full_nonpositive_separator_passes":
            stress_class[
                "channel_3_1_full_nonpositive_separator_passes"],
    }


def main():
    provenance = load_json(PROVENANCE)
    subclass_channel = load_json(SUBCLASS_CHANNEL)
    additional = load_json(ADDITIONAL)
    stress_class = load_json(STRESS_CLASS)

    selected = selected_summary(provenance, subclass_channel)
    broad = broad_summary(additional, stress_class)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "selected_deficit_provenance": str(PROVENANCE.relative_to(ROOT)),
            "selected_stress_subclass_channel_decomposition": str(
                SUBCLASS_CHANNEL.relative_to(ROOT)),
            "additional_stress_reference_generalization": str(
                ADDITIONAL.relative_to(ROOT)),
            "centered_3_1_stress_class": str(STRESS_CLASS.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite scope-fork audit only; this compares already checked "
            "receipts and fits no new classifier. It proves no selected-stress "
            "theorem, broad stress theorem, signed correlation theorem, "
            "pointwise character-sum theorem, or Goldbach proof."),
        "mechanism": (
            "Keep the selected-stable fixture and the baseline "
            "full_nonpositive fixture as separate source predicates. Compare "
            "their checked scalar/watchlist outcomes and overlap before "
            "trying to promote a stress-reference lemma."),
        "prediction": (
            "If the selected five are merely examples of the broad "
            "full_nonpositive stress population, scalar (3,1) and Kevin's "
            "watchlist should not separate the selected five while failing "
            "many additional broad references."),
        "falsifier": (
            "The selected-reference-to-broad-stress promotion is falsified "
            "when the selected five have zero scalar/watchlist failures but "
            "additional broad references have nonpositive fresh-unseen "
            "margins under the same frozen subsets."),
        "selected_reference_fixture": selected,
        "broad_full_nonpositive_fixture": broad,
        "scope_comparison": {
            "selected_references_are_subset_of_broad_full_nonpositive":
                selected["references"] == broad["selected_reference_overlap"],
            "selected_reference_overlap_count": len(
                broad["selected_reference_overlap"]),
            "selected_scalar_3_1_failures":
                selected["total_scalar_3_1_failures"],
            "broad_scalar_3_1_failures": broad["scalar_3_1_failures"],
            "selected_watchlist_failures": selected[
                "total_watchlist_failures"],
            "broad_watchlist_failures": broad["watchlist_failures"],
            "selected_watchlist_without_3_1_failures": selected[
                "total_watchlist_without_3_1_failures"],
            "broad_watchlist_without_3_1_reference_pass_count": broad[
                "reference_pass_counts"]["kevin_watchlist_without_3_1"],
        },
        "decision": (
            "The selected-five result and the broad full_nonpositive result "
            "are different finite statements.  The selected five have zero "
            "scalar (3,1) and watchlist failures across 3,030 fresh-unseen "
            "comparisons, and removing (3,1) from the watchlist fails the "
            "selected fixture.  The 89 additional broad references have "
            "32,661 scalar (3,1) failures and 11,634 watchlist failures.  "
            "Therefore the selected-reference lemma survives only as a "
            "narrow fixture statement; the broad stress-reference promotion "
            "is falsified."),
        "next_obligation": (
            "Define a sharper non-post-hoc selected-stress family from the "
            "selected-stable fixture itself, or replace classifier language "
            "with a signed empirical/correlation estimate that explains the "
            "selected five without claiming the broad full_nonpositive class."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
