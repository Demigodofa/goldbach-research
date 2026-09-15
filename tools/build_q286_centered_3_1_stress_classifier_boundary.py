"""Freeze the finite boundary for centered (3,1) as a stress classifier.

Kevin asked whether `(3,1)` might be a stress-classifier lemma, with 13822
as a strong negative reference.  The checked q286 receipts now support a
narrow selected-reference classifier reading and falsify the broad
full_nonpositive reading.  This builder records that distinction in one
derived receipt without refitting coefficients or recomputing profiles.

Finite evidence only: this proves no stress-class theorem, signed correlation
theorem, pointwise character-sum theorem, or Goldbach theorem.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-centered-3-1-stress-classifier-boundary.json"

REFERENCE_LEMMA = EVIDENCE / "q286-centered-3-1-reference-lemma-audit.json"
FRESH_UNSEEN = EVIDENCE / "q286-watchlist-fresh-unseen-window-audit.json"
STRESS_CLASS = EVIDENCE / "q286-centered-3-1-stress-class-audit.json"
PROVENANCE = EVIDENCE / "q286-selected-deficit-provenance-audit.json"

FOCUS_REFERENCE = 13_822


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def subset_result(rows, name):
    return next(row for row in rows if row["name"] == name)


def class_result(payload, label_key, class_id):
    channel = next(
        row for row in payload["channel_results"]
        if row["label_key"] == label_key)
    return next(row for row in channel["class_results"]
                if row["class_id"] == class_id)


def compact_subset(row):
    summary = row["weighted_gap_summary"]
    return {
        "name": row["name"],
        "passes_all_targets": row["all_targets_pass"],
        "failing_target_count": row["failing_target_count"],
        "minimum_margin": summary["minimum"],
        "average_margin": summary["mean"],
        "maximum_margin": summary["maximum"],
    }


def compact_reference(row):
    return {
        "reference": row["reference_target"],
        "reference_mod_143": row["reference_mod_143"],
        "scalar_3_1": compact_subset(
            subset_result(row["subset_results"], "scalar_3_1")),
        "kevin_watchlist_4": compact_subset(
            subset_result(row["subset_results"], "kevin_watchlist_4")),
        "kevin_watchlist_without_3_1": compact_subset(
            subset_result(
                row["subset_results"], "kevin_watchlist_without_3_1")),
        "frozen_full_17_lp": compact_subset(
            subset_result(row["subset_results"], "frozen_full_17_lp")),
    }


def main():
    reference_lemma = load_json(REFERENCE_LEMMA)
    fresh_unseen = load_json(FRESH_UNSEEN)
    stress_class = load_json(STRESS_CLASS)
    provenance = load_json(PROVENANCE)

    full_nonpositive = class_result(stress_class, "3,1", "full_nonpositive")
    active_nonrescued = class_result(
        stress_class, "3,1", "active_nonrescued")
    fresh_scalar = subset_result(fresh_unseen["subset_results"], "scalar_3_1")
    fresh_watchlist = subset_result(
        fresh_unseen["subset_results"], "kevin_watchlist_4")
    fresh_without_3_1 = subset_result(
        fresh_unseen["subset_results"], "kevin_watchlist_without_3_1")
    fresh_full_lp = subset_result(
        fresh_unseen["subset_results"], "frozen_full_17_lp")
    focus_fresh = next(
        row for row in fresh_unseen["reference_results"]
        if row["reference_target"] == FOCUS_REFERENCE)
    focus_provenance = next(
        row for row in provenance["selected_deficit_rows"]
        if row["target"] == FOCUS_REFERENCE)

    selected_finite_passes = (
        reference_lemma["selected_deficit_references_all_pass"]
        and fresh_unseen["scalar_3_1_passes_unseen_windows"])
    broad_falsified = (
        not stress_class["channel_3_1_full_nonpositive_separator_passes"])

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "reference_lemma": str(REFERENCE_LEMMA.relative_to(ROOT)),
            "fresh_unseen_watchlist": str(FRESH_UNSEEN.relative_to(ROOT)),
            "stress_class": str(STRESS_CLASS.relative_to(ROOT)),
            "selected_deficit_provenance": str(
                PROVENANCE.relative_to(ROOT)),
        },
        "channel": [3, 1],
        "channel_key": "3,1",
        "focus_reference": FOCUS_REFERENCE,
        "status_boundary": (
            "finite derived boundary receipt only; no selected-stress "
            "theorem, broad stress-class theorem, signed correlation "
            "theorem, pointwise character-sum theorem, or Goldbach proof."),
        "mechanism": (
            "Read checked q286 evidence across selected-reference, "
            "fresh-unseen, independent full_nonpositive stress-class, and "
            "selected-deficit provenance receipts. No channel coefficients "
            "are refit and no references are reselected here."),
        "claim_supported_finitely": (
            "Centered (3,1) is a useful finite selected-stress reference "
            "classifier coordinate for the five pre-existing selected "
            "dominant-floor deficit references."),
        "claim_falsified_finitely": (
            "Centered (3,1) classifies every row in the independent "
            "baseline full_nonpositive q286 stress predicate."),
        "selected_reference_evidence": {
            "original_fresh_target_count_per_reference":
                reference_lemma["fresh_target_count_per_reference"],
            "original_selected_deficit_references_all_pass":
                reference_lemma["selected_deficit_references_all_pass"],
            "fresh_unseen_comparison_row_count":
                fresh_unseen["comparison_row_count"],
            "fresh_unseen_target_count": fresh_unseen["fresh_target_count"],
            "scalar_3_1_fresh_unseen": compact_subset(fresh_scalar),
            "kevin_watchlist_4_fresh_unseen":
                compact_subset(fresh_watchlist),
            "kevin_watchlist_without_3_1_fresh_unseen":
                compact_subset(fresh_without_3_1),
            "frozen_full_17_lp_fresh_unseen":
                compact_subset(fresh_full_lp),
            "reference_rows": [
                compact_reference(row)
                for row in fresh_unseen["reference_results"]
            ],
        },
        "focus_reference_13822": {
            **reference_lemma["focus_reference_13822"],
            "fresh_unseen": compact_reference(focus_fresh),
            "selected_fixture": {
                "dominant_floor_passes":
                    focus_provenance[
                        "selected_fixture_dominant_floor_passes"],
                "dominant_margin_to_floor":
                    focus_provenance[
                        "selected_fixture_dominant_margin_to_floor"],
                "stable_core_margin_to_floor":
                    focus_provenance["stable_core_margin_to_floor"],
                "volatile_rim_sum_to_principal":
                    focus_provenance["volatile_rim_sum_to_principal"],
            },
        },
        "broad_full_nonpositive_falsifier": {
            "baseline_filter_window":
                stress_class["baseline_filter_window"],
            "full_nonpositive": {
                "target_count": full_nonpositive["target_count"],
                "below_fresh_min_count":
                    full_nonpositive["below_fresh_min_count"],
                "at_or_above_fresh_min_count":
                    full_nonpositive["at_or_above_fresh_min_count"],
                "separator_passes_class":
                    full_nonpositive["separator_passes_class"],
                "maximum_counterexample_target":
                    full_nonpositive["maximum_row"]["target"],
                "maximum_weighted_centered_value":
                    full_nonpositive["maximum_row"][
                        "weighted_centered_channel_value"],
            },
            "active_nonrescued": {
                "target_count": active_nonrescued["target_count"],
                "below_fresh_min_count":
                    active_nonrescued["below_fresh_min_count"],
                "at_or_above_fresh_min_count":
                    active_nonrescued["at_or_above_fresh_min_count"],
                "separator_passes_class":
                    active_nonrescued["separator_passes_class"],
            },
            "holdout_class_counts": stress_class["holdout_class_counts"],
        },
        "decision": {
            "selected_reference_classifier_finite_status":
                "supported_on_checked_selected_references"
                if selected_finite_passes else "falsified",
            "broad_full_nonpositive_classifier_finite_status":
                "falsified" if broad_falsified else "not_falsified",
            "next_obligation": (
                "Do not promote `(3,1)` to a broad stress theorem. Either "
                "define a new non-post-hoc stress predicate that captures "
                "the selected references and faces fresh holdout rows, or "
                "replace the classifier language with a signed "
                "empirical/correlation estimate for the selected family."),
        },
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
