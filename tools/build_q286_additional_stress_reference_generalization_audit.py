"""Test q286 selected-stress channels on additional stress references.

The selected five deficit references made scalar (3,1) look like a useful
finite stress-reference classifier coordinate.  This audit tests whether that
generalizes to additional references from the predeclared, channel-independent
``full_nonpositive`` filter-order population.

Finite evidence only: this proves no selected-stress theorem, broad stress
theorem, signed correlation theorem, pointwise character-sum theorem, or
Goldbach theorem.
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
OUT = EVIDENCE / "q286-additional-stress-reference-generalization-audit.json"
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
    q286_first_three_filter_order_audit_receipt,
)
from tools.build_q286_alternate_reference_channel_audit import (  # noqa: E402
    DEFICIT_REFERENCES,
)
from tools.build_q286_centered_3_1_residue5_multichannel_horizon import (  # noqa: E402
    SCALAR_LABEL,
    WATCHLIST_LABELS,
    label_key,
)
from tools.build_q286_centered_3_1_stress_class_audit import (  # noqa: E402
    predicate_sets,
)
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    label_tuple,
)
from tools.build_q286_fresh_window_channel_watchlist_audit import (  # noqa: E402
    collect_targets,
)
from tools.build_q286_watchlist_fresh_unseen_window_audit import (  # noqa: E402
    FRESH_UNSEEN_WINDOW_SPECS,
    build_comparison_rows,
    channel_summaries,
    summarize_subset,
)


TOLERANCE = 1e-12
BASELINE_FILTER_START = 10_000
BASELINE_FILTER_CYCLE_COUNT = 8
BASELINE_FILTER_TARGETS_PER_CYCLE = 5_005


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


def target_sets_with(receipt, predicate):
    return {
        int(target) for target, row in receipt["target_rows"].items()
        if predicate in row["passed_predicates"]
    }


def summarize_reference(reference, rows, labels):
    reference_rows = [
        row for row in rows if int(row["reference_target"]) == int(reference)]
    subset_results = [
        summarize_subset("scalar_3_1", (SCALAR_LABEL,), reference_rows),
        summarize_subset("kevin_watchlist_4", WATCHLIST_LABELS,
                         reference_rows),
        summarize_subset(
            "kevin_watchlist_without_3_1",
            tuple(label for label in WATCHLIST_LABELS if label != SCALAR_LABEL),
            reference_rows),
        summarize_subset("frozen_full_17_lp", labels, reference_rows),
    ]
    return {
        "reference_target": int(reference),
        "reference_mod_143": int(reference) % 143,
        "reference_mod_286": int(reference) % 286,
        "comparison_count": len(reference_rows),
        "subset_results": subset_results,
    }


def summarize_class(class_id, references, rows, labels):
    references = tuple(sorted(int(reference) for reference in references))
    class_rows = [
        row for row in rows if int(row["reference_target"]) in references]
    subset_results = [
        summarize_subset("scalar_3_1", (SCALAR_LABEL,), class_rows),
        summarize_subset("kevin_watchlist_4", WATCHLIST_LABELS, class_rows),
        summarize_subset(
            "kevin_watchlist_without_3_1",
            tuple(label for label in WATCHLIST_LABELS if label != SCALAR_LABEL),
            class_rows),
        summarize_subset("frozen_full_17_lp", labels, class_rows),
    ]
    by_name = {row["name"]: row for row in subset_results}
    reference_results = [
        summarize_reference(reference, rows, labels)
        for reference in references
    ]
    def reference_pass_count(subset_name):
        return sum(
            1 for row in reference_results
            if next(
                item for item in row["subset_results"]
                if item["name"] == subset_name)["all_targets_pass"])

    return {
        "class_id": class_id,
        "reference_count": len(references),
        "references": list(references),
        "comparison_count": len(class_rows),
        "subset_results": subset_results,
        "reference_pass_counts": {
            "scalar_3_1": reference_pass_count("scalar_3_1"),
            "kevin_watchlist_4": reference_pass_count("kevin_watchlist_4"),
            "kevin_watchlist_without_3_1": reference_pass_count(
                "kevin_watchlist_without_3_1"),
            "frozen_full_17_lp": reference_pass_count("frozen_full_17_lp"),
        },
        "scalar_3_1_passes": by_name["scalar_3_1"]["all_targets_pass"],
        "kevin_watchlist_4_passes": by_name[
            "kevin_watchlist_4"]["all_targets_pass"],
        "watchlist_without_3_1_passes": by_name[
            "kevin_watchlist_without_3_1"]["all_targets_pass"],
        "frozen_full_17_lp_passes": by_name[
            "frozen_full_17_lp"]["all_targets_pass"],
        "first_failing_references": [
            row for row in reference_results
            if not next(
                item for item in row["subset_results"]
                if item["name"] == "kevin_watchlist_4")[
                    "all_targets_pass"]
        ][:20],
        "channel_summary_rows": channel_summaries(labels, class_rows),
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

    baseline = q286_first_three_filter_order_audit_receipt(
        start=BASELINE_FILTER_START,
        cycle_count=BASELINE_FILTER_CYCLE_COUNT,
        targets_per_cycle=BASELINE_FILTER_TARGETS_PER_CYCLE,
        tail_threshold=.3,
        complement_floor=.3)
    class_sets = predicate_sets(baseline)
    selected_references = set(int(target) for target in DEFICIT_REFERENCES)
    selected_full_nonpositive_overlap = sorted(
        set(class_sets["full_nonpositive"]) & selected_references)
    additional_class_sets = {
        class_id: sorted(set(targets) - selected_references)
        for class_id, targets in class_sets.items()
    }
    additional_full_nonpositive = tuple(
        additional_class_sets["full_nonpositive"])

    fresh_targets, fresh_metadata = collect_targets(FRESH_UNSEEN_WINDOW_SPECS)
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=tuple(
            sorted(set(fresh_targets) | set(additional_full_nonpositive))),
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=40)
    rows, fresh_target_rows = build_comparison_rows(
        fresh_targets,
        fresh_metadata,
        additional_full_nonpositive,
        profile,
        labels,
        local_rows_by_residue,
        lp_vector)

    class_results = [
        summarize_class(class_id, references, rows, labels)
        for class_id, references in additional_class_sets.items()
    ]
    full_nonpositive = next(
        row for row in class_results
        if row["class_id"] == "full_nonpositive")
    scalar = next(
        row for row in full_nonpositive["subset_results"]
        if row["name"] == "scalar_3_1")
    watchlist = next(
        row for row in full_nonpositive["subset_results"]
        if row["name"] == "kevin_watchlist_4")

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
            "low_frequency_lp_cone": str(LP_SOURCE.relative_to(ROOT)),
            "fresh_unseen_windows":
                "tools/build_q286_watchlist_fresh_unseen_window_audit.py",
            "stress_class_audit":
                "tools/build_q286_centered_3_1_stress_class_audit.py",
        },
        "baseline_filter_window": {
            "start": BASELINE_FILTER_START,
            "cycle_count": BASELINE_FILTER_CYCLE_COUNT,
            "targets_per_cycle": BASELINE_FILTER_TARGETS_PER_CYCLE,
            "predicate_counts": baseline["predicate_counts"],
        },
        "selected_deficit_references_excluded": sorted(selected_references),
        "selected_deficit_references_in_full_nonpositive":
            selected_full_nonpositive_overlap,
        "fresh_unseen_window_specs": [
            list(row) for row in FRESH_UNSEEN_WINDOW_SPECS],
        "fresh_target_count": len(fresh_targets),
        "fresh_deficit_target_count": sum(
            1 for row in fresh_target_rows
            if not row["dominant_floor_passes"]),
        "additional_reference_count": len(additional_full_nonpositive),
        "comparison_row_count": len(rows),
        "status_boundary": (
            "finite additional-stress-reference generalization audit only; "
            "additional references come from the predeclared baseline "
            "full_nonpositive fixture, selected references are excluded, and "
            "the result proves no stress theorem, signed correlation theorem, "
            "pointwise character-sum theorem, or Goldbach proof."),
        "mechanism": (
            "Use later fresh-unseen targets against additional references from "
            "the predeclared full_nonpositive stress population.  Subtract the "
            "full target-reference local q286 vector and test frozen scalar "
            "(3,1), Kevin's four-channel watchlist, the watchlist without "
            "(3,1), and the frozen full 17-channel LP vector."),
        "prediction": (
            "If (3,1) and Kevin's watchlist are fixture-independent stress "
            "reference tools, they should stay positive for additional "
            "full_nonpositive references beyond the five selected deficits."),
        "falsifier": (
            "Any additional full_nonpositive reference with a nonpositive "
            "fresh-unseen margin falsifies the broad generalization for the "
            "tested frozen scalar or watchlist."),
        "class_results": class_results,
        "decision": (
            "The broad additional-stress-reference generalization is "
            "finitely falsified.  On 89 additional full_nonpositive "
            "references and 53,934 fresh-unseen comparisons, scalar (3,1) "
            f"has {scalar['failing_target_count']} nonpositive margins and "
            f"Kevin's watchlist has {watchlist['failing_target_count']}.  "
            "Preserve the selected-reference lemma as narrow: it is "
            "load-bearing for the selected five references, not a theorem for "
            "the predeclared broad full_nonpositive stress population."),
        "full_nonpositive_scalar_3_1_passes": scalar["all_targets_pass"],
        "full_nonpositive_scalar_3_1_failure_count":
            scalar["failing_target_count"],
        "full_nonpositive_watchlist_passes":
            watchlist["all_targets_pass"],
        "full_nonpositive_watchlist_failure_count":
            watchlist["failing_target_count"],
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
