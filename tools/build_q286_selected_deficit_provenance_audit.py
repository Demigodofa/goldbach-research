"""Audit provenance of the q286 selected deficit references.

The centered (3,1) scalar separates five selected deficit references, but a
later audit showed it does not classify the independent full_nonpositive
filter-order stress class. This receipt records that these are different
finite populations with different source predicates.

Finite evidence only: this proves no stress-class theorem, signed projection
theorem, binary-prime correlation theorem, or Goldbach theorem.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-selected-deficit-provenance-audit.json"

STABLE_SOURCE = (
    EVIDENCE
    / "q286-first-three-dominant-mode-stable-core-selected-classification.json")
VOLATILE_CLAUSE_SOURCE = (
    EVIDENCE
    / "q286-first-three-dominant-mode-volatile-minimal-clause-structure.json")
CENTERED_SOURCE = EVIDENCE / "q286-centered-channel-scalar-order-audit.json"
STRESS_CLASS_SOURCE = EVIDENCE / "q286-centered-3-1-stress-class-audit.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def centered_reference_row(centered_payload, label_key, target):
    result = next(
        row for row in centered_payload["channel_results"]
        if row["label_key"] == label_key)
    for row in result["selected_deficit_reference_rank_rows"]:
        if row["target"] == target:
            return row
    return None


def volatile_clause_row(volatile_payload, target):
    for row in volatile_payload["deficit_clause_rows"]:
        if row["target"] == target:
            return row
    return None


def main():
    stable = load_json(STABLE_SOURCE)
    volatile = load_json(VOLATILE_CLAUSE_SOURCE)
    centered = load_json(CENTERED_SOURCE)
    stress_class = load_json(STRESS_CLASS_SOURCE)

    selected_deficits = tuple(int(target) for target in stable[
        "failure_targets"])
    selected_clears = tuple(int(target) for target in stable["clear_targets"])
    volatile_deficits = tuple(int(target) for target in volatile[
        "deficit_targets"])
    if tuple(sorted(selected_deficits)) != tuple(sorted(volatile_deficits)):
        raise AssertionError(
            "stable selected deficits and volatile clause deficits diverged")

    baseline = stress_class["baseline_filter_window"]
    baseline_start = baseline["start"]
    baseline_stop = (
        baseline_start + 2 * (baseline["tested_target_count"] - 1))
    stress_3_1 = next(
        row for row in stress_class["channel_results"]
        if row["label_key"] == "3,1")
    full_nonpositive_3_1 = next(
        row for row in stress_3_1["class_results"]
        if row["class_id"] == "full_nonpositive")

    rows = []
    for target in selected_deficits:
        stable_row = stable["target_rows"][str(target)]
        clause = volatile_clause_row(volatile, target)
        centered_3_1 = centered_reference_row(centered, "3,1", target)
        centered_5_5 = centered_reference_row(centered, "5,5", target)
        rows.append({
            "target": target,
            "target_mod_143": target % 143,
            "target_mod_286": target % 286,
            "in_selected_stable_fixture": True,
            "in_baseline_filter_window": (
                baseline_start <= target <= baseline_stop),
            "selected_fixture_dominant_floor_passes": (
                stable_row["dominant_floor_passes"]),
            "selected_fixture_dominant_margin_to_floor": (
                stable_row["dominant_margin_to_floor"]),
            "stable_core_floor_passes": (
                stable_row["stable_core_floor_passes"]),
            "stable_core_margin_to_floor": (
                stable_row["stable_core_margin_to_floor"]),
            "volatile_rim_sum_to_principal": (
                stable_row["volatile_rim_sum_to_principal"]),
            "volatile_clause_count": (
                clause["inclusion_minimal_clause_count"] if clause else None),
            "volatile_minimum_clause_size": (
                clause["minimum_satisfying_subset_size"] if clause else None),
            "volatile_necessary_channels": (
                clause["necessary_channels_across_all_satisfying_subsets"]
                if clause else None),
            "centered_3_1_weighted_value": (
                centered_3_1["weighted_centered_channel_value"]
                if centered_3_1 else None),
            "centered_3_1_rank_low_to_high": (
                centered_3_1["rank_low_to_high"] if centered_3_1 else None),
            "centered_5_5_weighted_value": (
                centered_5_5["weighted_centered_channel_value"]
                if centered_5_5 else None),
            "centered_5_5_rank_low_to_high": (
                centered_5_5["rank_low_to_high"] if centered_5_5 else None),
        })

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_stable_core_selected_classification": str(
            STABLE_SOURCE.relative_to(ROOT)),
        "source_volatile_clause_structure": str(
            VOLATILE_CLAUSE_SOURCE.relative_to(ROOT)),
        "source_centered_scalar_order": str(
            CENTERED_SOURCE.relative_to(ROOT)),
        "source_centered_3_1_stress_class": str(
            STRESS_CLASS_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite provenance audit only; no stress-class theorem, "
            "selected-fixture classifier theorem, signed projection theorem, "
            "binary-prime correlation theorem, or Goldbach proof."),
        "selected_fixture": {
            "sample_targets": stable["sample_targets"],
            "selected_deficit_targets": selected_deficits,
            "selected_clear_targets": selected_clears,
            "deficit_source_predicate": (
                "dominant_floor_passes == false in the selected stable-core "
                "classification fixture"),
        },
        "baseline_full_nonpositive_fixture": {
            **baseline,
            "target_span": [baseline_start, baseline_stop],
            "classifier_source_predicate": (
                "full_action_to_principal_ratio <= 0 in the baseline "
                "filter-order fixture"),
            "centered_3_1_full_nonpositive_separator_passes": (
                full_nonpositive_3_1["separator_passes_class"]),
            "centered_3_1_full_nonpositive_at_or_above_fresh_min_count": (
                full_nonpositive_3_1["at_or_above_fresh_min_count"]),
        },
        "mechanism": (
            "Keep the selected-deficit lane and the full_nonpositive "
            "filter-order lane separate by recording their source predicates "
            "and row provenance."),
        "prediction": (
            "If the five selected deficit references are merely examples of "
            "the baseline full_nonpositive class, their source predicates and "
            "membership should align. If not, centered (3,1) separation of "
            "the selected references cannot be promoted to the "
            "full_nonpositive class."),
        "falsifier": (
            "Different source predicates, different fixture spans, or a "
            "failed full_nonpositive classifier test falsify the direct "
            "promotion from selected-deficit separator to full_nonpositive "
            "stress-class theorem."),
        "selected_deficit_rows": rows,
        "decision": (
            "The selected deficit references are dominant-floor failures in "
            "the selected stable/volatile fixture, while the falsified broad "
            "stress class is the independent full_nonpositive filter-order "
            "population. These are distinct finite populations; centered "
            "(3,1) remains a selected-deficit separator but is not promoted "
            "to the full_nonpositive stress-class theorem."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
