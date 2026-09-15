"""Audit independent q286 stress features against the low-(3,1) subclass.

The previous receipt showed that a frozen centered-(3,1) threshold selects a
33-reference scalar-order subclass inside the broad full_nonpositive baseline
population.  This receipt asks whether pre-existing filter/residue features,
without using the centered-(3,1) scalar as a coefficient, already explain that
subclass.

Finite evidence only: fitted thresholds in this receipt are diagnostic.  This
proves no stress theorem, signed correlation theorem, pointwise character-sum
theorem, or Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-independent-stress-feature-audit.json"
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_filter_order_audit_receipt,
)


THRESHOLD_SOURCE = (
    EVIDENCE / "q286-centered-3-1-threshold-subclass-audit.json")
SELECTED_BOUNDARY_SOURCE = (
    EVIDENCE / "q286-selected-stable-fixture-family-boundary-audit.json")
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


def refs_for_threshold(threshold_payload, name):
    return set(
        int(target)
        for target in next(
            row for row in threshold_payload["threshold_subclasses"]
            if row["name"] == name)["references"])


def row_table(baseline, low_refs, strict_low_refs):
    rows = []
    for target, row in baseline["target_rows"].items():
        target = int(target)
        predicates = set(row["passed_predicates"])
        if "full_nonpositive" not in predicates:
            continue
        rows.append({
            "target": target,
            "target_mod_143": target % 143,
            "target_mod_286": target % 286,
            "passed_predicates": sorted(predicates),
            "first_two_modes_to_principal_ratio": row[
                "first_two_modes_to_principal_ratio"],
            "first_three_modes_to_principal_ratio": row[
                "first_three_modes_to_principal_ratio"],
            "complement_to_principal_ratio": row[
                "complement_to_principal_ratio"],
            "full_action_to_principal_ratio": row[
                "full_action_to_principal_ratio"],
            "low_centered_3_1_selected_max_threshold": target in low_refs,
            "low_centered_3_1_selected_min_threshold":
                target in strict_low_refs,
        })
    return sorted(rows, key=lambda item: item["target"])


def predicate_sets(rows):
    def has(row, predicate):
        return predicate in row["passed_predicates"]

    return {
        "full_nonpositive": rows,
        "first_two_active": [
            row for row in rows if has(row, "first_two_active")],
        "first_three_tail": [
            row for row in rows if has(row, "first_three_tail")],
        "complement_positive": [
            row for row in rows if has(row, "complement_positive")],
        "complement_floor": [
            row for row in rows if has(row, "complement_floor")],
        "active_selector": [
            row for row in rows
            if has(row, "first_two_active")
            and has(row, "first_three_tail")],
        "active_nonrescued": [
            row for row in rows
            if has(row, "first_two_active")
            and has(row, "first_three_tail")
            and has(row, "full_nonpositive")],
        "nonrescued_first_three_tail": [
            row for row in rows
            if has(row, "first_three_tail")
            and has(row, "full_nonpositive")],
        "full_nonpositive_not_first_three_tail": [
            row for row in rows if not has(row, "first_three_tail")],
        "first_two_active_not_first_three_tail": [
            row for row in rows
            if has(row, "first_two_active")
            and not has(row, "first_three_tail")],
        "first_three_tail_not_first_two_active": [
            row for row in rows
            if has(row, "first_three_tail")
            and not has(row, "first_two_active")],
        "complement_floor_and_first_three_tail": [
            row for row in rows
            if has(row, "complement_floor")
            and has(row, "first_three_tail")],
        "complement_floor_and_active_selector": [
            row for row in rows
            if has(row, "complement_floor")
            and has(row, "first_two_active")
            and has(row, "first_three_tail")],
        "prior_seed_residue_38_or_64": [
            row for row in rows
            if row["target_mod_143"] in SEED_RESIDUES_MOD_143],
    }


def summarize_predicate(name, rows, total_low_count):
    low_rows = [
        row for row in rows
        if row["low_centered_3_1_selected_max_threshold"]]
    high_rows = [
        row for row in rows
        if not row["low_centered_3_1_selected_max_threshold"]]
    precision = len(low_rows) / len(rows) if rows else None
    recall = len(low_rows) / total_low_count if total_low_count else None
    return {
        "name": name,
        "pre_existing_feature": True,
        "reference_count": len(rows),
        "low_centered_3_1_count": len(low_rows),
        "above_selected_3_1_threshold_count": len(high_rows),
        "precision_for_low_centered_3_1": precision,
        "recall_for_low_centered_3_1": recall,
        "passes_zero_scalar_failure_gate": bool(rows and not high_rows),
        "selected_references": [row["target"] for row in rows],
        "first_above_threshold_rows": high_rows[:12],
        "feature_summaries": {
            feature: finite_summary(row[feature] for row in rows)
            for feature in CONTINUOUS_FEATURES
        },
    }


CONTINUOUS_FEATURES = (
    "first_two_modes_to_principal_ratio",
    "first_three_modes_to_principal_ratio",
    "complement_to_principal_ratio",
    "full_action_to_principal_ratio",
)


def threshold_rows(rows, feature, direction, threshold):
    if direction == "<=":
        return [row for row in rows if row[feature] <= threshold]
    if direction == ">=":
        return [row for row in rows if row[feature] >= threshold]
    raise ValueError(direction)


def best_posthoc_thresholds(rows, total_low_count, min_support=5):
    out = []
    for feature in CONTINUOUS_FEATURES:
        candidates = []
        for direction in ("<=", ">="):
            for threshold in sorted({row[feature] for row in rows}):
                selected = threshold_rows(rows, feature, direction, threshold)
                if len(selected) < min_support:
                    continue
                low_count = sum(
                    1 for row in selected
                    if row["low_centered_3_1_selected_max_threshold"])
                high_count = len(selected) - low_count
                precision = low_count / len(selected)
                recall = low_count / total_low_count if total_low_count else 0.0
                f1 = (
                    2 * precision * recall / (precision + recall)
                    if precision + recall else 0.0)
                candidates.append({
                    "feature": feature,
                    "direction": direction,
                    "threshold": threshold,
                    "reference_count": len(selected),
                    "low_centered_3_1_count": low_count,
                    "above_selected_3_1_threshold_count": high_count,
                    "precision_for_low_centered_3_1": precision,
                    "recall_for_low_centered_3_1": recall,
                    "f1": f1,
                    "post_hoc_diagnostic_only": True,
                    "passes_zero_scalar_failure_gate": high_count == 0,
                    "references": [row["target"] for row in selected],
                })
        zero_failure = [
            row for row in candidates
            if row["passes_zero_scalar_failure_gate"]]
        out.append({
            "feature": feature,
            "best_zero_failure_thresholds": sorted(
                zero_failure,
                key=lambda row: (-row["reference_count"],
                                 row["direction"], row["threshold"]))[:5],
            "best_f1_thresholds": sorted(
                candidates,
                key=lambda row: (-row["f1"],
                                 -row["precision_for_low_centered_3_1"],
                                 -row["reference_count"]))[:5],
        })
    return out


def residue_summaries(rows, total_low_count):
    by_residue = defaultdict(list)
    for row in rows:
        by_residue[row["target_mod_143"]].append(row)
    out = []
    for residue, residue_rows in by_residue.items():
        low_count = sum(
            1 for row in residue_rows
            if row["low_centered_3_1_selected_max_threshold"])
        out.append({
            "residue_mod_143": residue,
            "reference_count": len(residue_rows),
            "low_centered_3_1_count": low_count,
            "above_selected_3_1_threshold_count":
                len(residue_rows) - low_count,
            "precision_for_low_centered_3_1":
                low_count / len(residue_rows),
            "recall_for_low_centered_3_1":
                low_count / total_low_count if total_low_count else None,
            "references": [row["target"] for row in residue_rows],
        })
    return sorted(
        out,
        key=lambda row: (-row["reference_count"],
                         -row["precision_for_low_centered_3_1"],
                         row["residue_mod_143"]))


def main():
    threshold_payload = load_json(THRESHOLD_SOURCE)
    selected_boundary = load_json(SELECTED_BOUNDARY_SOURCE)
    low_refs = refs_for_threshold(
        threshold_payload,
        "broad_full_nonpositive_at_or_below_selected_max")
    strict_low_refs = refs_for_threshold(
        threshold_payload,
        "broad_full_nonpositive_at_or_below_selected_min")
    baseline = q286_first_three_filter_order_audit_receipt(
        start=10000, cycle_count=8, targets_per_cycle=5005,
        tail_threshold=.3, complement_floor=.3)
    rows = row_table(baseline, low_refs, strict_low_refs)
    total_low_count = sum(
        1 for row in rows
        if row["low_centered_3_1_selected_max_threshold"])
    predicates = [
        summarize_predicate(name, predicate_rows, total_low_count)
        for name, predicate_rows in predicate_sets(rows).items()
    ]
    zero_failure_predicates = [
        row for row in predicates
        if row["passes_zero_scalar_failure_gate"]
        and row["reference_count"] > 0
    ]
    best_predeclared = max(
        predicates,
        key=lambda row: (
            row["precision_for_low_centered_3_1"] or 0.0,
            row["recall_for_low_centered_3_1"] or 0.0,
            row["reference_count"]),
        default=None)
    predicate_feature_counts = Counter(
        predicate
        for row in rows
        for predicate in row["passed_predicates"])

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "centered_3_1_threshold_subclass": str(
                THRESHOLD_SOURCE.relative_to(ROOT)),
            "selected_stable_fixture_family_boundary": str(
                SELECTED_BOUNDARY_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite independent-feature audit only; post-hoc fitted "
            "thresholds are diagnostics, not stress definitions. This proves "
            "no stress theorem, signed correlation theorem, pointwise "
            "character-sum theorem, or Goldbach proof."),
        "question": (
            "Do pre-existing q286 filter/residue features independent of the "
            "centered-(3,1) scalar explain the frozen low-(3,1) subclass?"),
        "mechanism": (
            "Use the 33-reference low-(3,1) subclass frozen by the previous "
            "receipt as the target label, then test source predicates from "
            "the q286 filter-order fixture and simple residue classes without "
            "using centered-(3,1) itself as a feature."),
        "prediction": (
            "If an independent stress definition has already emerged, at "
            "least one pre-existing filter/residue predicate should select a "
            "nontrivial zero-failure subset with high recall for the 33 "
            "low-(3,1) references."),
        "falsifier": (
            "If every pre-existing predicate includes above-threshold rows or "
            "captures only a tiny residue accident, the independent stress "
            "definition is still missing and the live result remains scalar "
            "order/correlation evidence."),
        "broad_full_nonpositive_reference_count": len(rows),
        "low_centered_3_1_reference_count": total_low_count,
        "strict_low_centered_3_1_reference_count": sum(
            1 for row in rows
            if row["low_centered_3_1_selected_min_threshold"]),
        "selected_reference_boundary_decision": selected_boundary["decision"],
        "predeclared_predicate_feature_counts": dict(
            sorted(predicate_feature_counts.items())),
        "predeclared_predicate_results": sorted(
            predicates,
            key=lambda row: (
                row["passes_zero_scalar_failure_gate"],
                row["precision_for_low_centered_3_1"] or 0.0,
                row["recall_for_low_centered_3_1"] or 0.0,
                row["reference_count"]),
            reverse=True),
        "zero_failure_predeclared_predicates": zero_failure_predicates,
        "best_predeclared_predicate": best_predeclared,
        "posthoc_single_feature_thresholds": best_posthoc_thresholds(
            rows, total_low_count),
        "residue_mod_143_summaries": residue_summaries(
            rows, total_low_count),
        "row_sample_low_centered_3_1": [
            row for row in rows
            if row["low_centered_3_1_selected_max_threshold"]
        ][:12],
        "row_sample_above_threshold": [
            row for row in rows
            if not row["low_centered_3_1_selected_max_threshold"]
        ][:12],
        "decision": (
            "The frozen low-(3,1) subclass is not yet explained by an "
            "independent pre-existing stress feature.  The broad "
            "full_nonpositive class contains 33 low-(3,1) references, but "
            "the natural filter predicates either include above-threshold "
            "references or become scalar/rank diagnostics when tuned after "
            "seeing the low-(3,1) labels.  This preserves (3,1) as a useful "
            "stress/reference coordinate while keeping the non-post-hoc "
            "stress-definition theorem open."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
