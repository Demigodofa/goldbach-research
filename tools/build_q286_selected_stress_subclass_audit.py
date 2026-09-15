"""Split selected q286 stress references by stable-core/volatile mechanism.

The centered (3,1) boundary receipt keeps `(3,1)` as a selected-reference
classifier coordinate but rejects the broad full_nonpositive stress-class
claim.  This receipt tests the next non-post-hoc candidate predicate:
stable core clears the floor, and the volatile rim overturns that clearance.

That predicate is natural in the existing stable/volatile decomposition, but
it is not allowed to silently become "the" selected-stress class.  This audit
records which selected references it captures, which selected references it
misses, and how the fixed channel subsets behave on fresh unseen rows by
subclass.

Finite evidence only: this proves no selected-stress theorem, signed
correlation theorem, pointwise character-sum theorem, or Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-selected-stress-subclass-audit.json"

PROVENANCE = EVIDENCE / "q286-selected-deficit-provenance-audit.json"
BOUNDARY = EVIDENCE / "q286-centered-3-1-stress-classifier-boundary.json"
FRESH_UNSEEN = EVIDENCE / "q286-watchlist-fresh-unseen-window-audit.json"

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


def subset_result(rows, name):
    return next(row for row in rows if row["name"] == name)


def classify_selected_reference(row):
    stable_margin = float(row["stable_core_margin_to_floor"])
    volatile_rim = float(row["volatile_rim_sum_to_principal"])
    dominant_margin = float(row["selected_fixture_dominant_margin_to_floor"])
    if stable_margin >= -TOLERANCE and dominant_margin < -TOLERANCE:
        if volatile_rim <= -stable_margin - TOLERANCE:
            return "volatile_overturn"
        return "stable_clear_but_nonvolatile_failure"
    if stable_margin < -TOLERANCE and dominant_margin < -TOLERANCE:
        return "stable_core_deficit"
    return "other"


def compact_reference(row):
    return {
        "target": row["target"],
        "target_mod_143": row["target_mod_143"],
        "target_mod_286": row["target_mod_286"],
        "stable_core_margin_to_floor": row["stable_core_margin_to_floor"],
        "volatile_rim_sum_to_principal": row[
            "volatile_rim_sum_to_principal"],
        "dominant_margin_to_floor": row[
            "selected_fixture_dominant_margin_to_floor"],
        "centered_3_1_weighted_value": row[
            "centered_3_1_weighted_value"],
        "centered_3_1_rank_low_to_high": row[
            "centered_3_1_rank_low_to_high"],
        "subclass": classify_selected_reference(row),
    }


def reference_summary(reference_row):
    return {
        "reference": reference_row["reference_target"],
        "reference_mod_143": reference_row["reference_mod_143"],
        "target_count": reference_row["target_count"],
        "scalar_3_1": compact_subset(
            subset_result(reference_row["subset_results"], "scalar_3_1")),
        "kevin_watchlist_4": compact_subset(
            subset_result(reference_row["subset_results"],
                          "kevin_watchlist_4")),
        "kevin_watchlist_without_3_1": compact_subset(
            subset_result(reference_row["subset_results"],
                          "kevin_watchlist_without_3_1")),
        "frozen_full_17_lp": compact_subset(
            subset_result(reference_row["subset_results"],
                          "frozen_full_17_lp")),
    }


def compact_subset(row):
    summary = row["weighted_gap_summary"]
    return {
        "name": row["name"],
        "passes": row["all_targets_pass"],
        "failing_target_count": row["failing_target_count"],
        "minimum_margin": summary["minimum"],
        "average_margin": summary["mean"],
        "maximum_margin": summary["maximum"],
    }


def aggregate_subset(reference_rows, subset_name):
    subset_rows = [
        subset_result(row["subset_results"], subset_name)
        for row in reference_rows
    ]
    counts = [row["weighted_gap_summary"]["count"] for row in subset_rows]
    means = [row["weighted_gap_summary"]["mean"] for row in subset_rows]
    total_count = sum(counts)
    weighted_mean = (
        math.fsum(count * mean for count, mean in zip(counts, means))
        / total_count if total_count else None)
    return {
        "name": subset_name,
        "reference_count": len(reference_rows),
        "comparison_count": total_count,
        "passes": all(row["all_targets_pass"] for row in subset_rows),
        "failing_target_count": sum(
            row["failing_target_count"] for row in subset_rows),
        "minimum_margin": min(
            (row["weighted_gap_summary"]["minimum"] for row in subset_rows),
            default=None),
        "average_margin": weighted_mean,
        "maximum_margin": max(
            (row["weighted_gap_summary"]["maximum"] for row in subset_rows),
            default=None),
    }


def aggregate_subclass(subclass, references, fresh_by_reference):
    reference_rows = [
        fresh_by_reference[reference["target"]]
        for reference in references
    ]
    return {
        "subclass": subclass,
        "reference_count": len(references),
        "references": [reference["target"] for reference in references],
        "reference_rows": [reference_summary(row) for row in reference_rows],
        "subset_results": [
            aggregate_subset(reference_rows, name)
            for name in (
                "scalar_3_1",
                "kevin_watchlist_4",
                "kevin_watchlist_without_3_1",
                "frozen_full_17_lp",
            )
        ],
        "stable_core_margin_summary": finite_summary(
            reference["stable_core_margin_to_floor"]
            for reference in references),
        "volatile_rim_summary": finite_summary(
            reference["volatile_rim_sum_to_principal"]
            for reference in references),
        "dominant_margin_summary": finite_summary(
            reference["dominant_margin_to_floor"]
            for reference in references),
    }


def main():
    provenance = load_json(PROVENANCE)
    boundary = load_json(BOUNDARY)
    fresh_unseen = load_json(FRESH_UNSEEN)

    selected_rows = [
        compact_reference(row)
        for row in provenance["selected_deficit_rows"]
    ]
    by_subclass = {}
    for row in selected_rows:
        by_subclass.setdefault(row["subclass"], []).append(row)

    fresh_by_reference = {
        row["reference_target"]: row
        for row in fresh_unseen["reference_results"]
    }
    subclass_results = [
        aggregate_subclass(subclass, rows, fresh_by_reference)
        for subclass, rows in sorted(by_subclass.items())
    ]
    volatile_overturn_refs = by_subclass.get("volatile_overturn", [])
    stable_core_deficit_refs = by_subclass.get("stable_core_deficit", [])
    selected_reference_count = len(selected_rows)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "selected_deficit_provenance": str(
                PROVENANCE.relative_to(ROOT)),
            "stress_classifier_boundary": str(BOUNDARY.relative_to(ROOT)),
            "fresh_unseen_watchlist": str(FRESH_UNSEEN.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite selected-stress subclass audit only; no selected-stress "
            "theorem, signed correlation theorem, pointwise character-sum "
            "theorem, or Goldbach proof."),
        "mechanism": (
            "Classify pre-existing selected deficit references by the frozen "
            "stable/volatile decomposition. The volatile-overturn predicate "
            "is stable_core_margin_to_floor >= 0 and volatile rim negative "
            "enough to make the dominant margin negative."),
        "prediction": (
            "If volatile-overturn is the whole non-post-hoc selected-stress "
            "predicate, it should capture all five selected deficit "
            "references. If it captures only a strict subclass, selected "
            "stress has multiple mechanisms."),
        "falsifier": (
            "Any selected deficit reference with negative stable-core margin "
            "is outside the volatile-overturn predicate and falsifies that "
            "predicate as the whole selected-stress class."),
        "selected_deficit_references": selected_rows,
        "subclass_counts": {
            subclass: len(rows) for subclass, rows in sorted(
                by_subclass.items())
        },
        "subclass_results": subclass_results,
        "volatile_overturn_captures_all_selected_deficits": (
            len(volatile_overturn_refs) == selected_reference_count),
        "volatile_overturn_reference_count": len(volatile_overturn_refs),
        "stable_core_deficit_reference_count": len(stable_core_deficit_refs),
        "boundary_receipt_decision": boundary["decision"],
        "decision": (
            "The volatile-overturn predicate is real but not the whole "
            "selected-stress class: it captures 13822, 164598, and 1222142, "
            "while 24424 and 55864 are stable-core deficits. Future theorem "
            "work should split selected stress into at least these two "
            "subclasses or move directly to a signed empirical/correlation "
            "estimate."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
