"""Build q286 volatile-row threshold evidence.

The volatile channel criticality map identifies deletion witnesses.  This
derivative builder rewrites every selected row as a stable-core margin plus a
volatile-subset threshold inequality, so the remaining theorem target is an
explicit finite list of rowwise signed conditions.
"""

from __future__ import annotations

from itertools import combinations
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUBSET_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-subset-ablation.json")
CRITICALITY_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-channel-criticality.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-row-thresholds.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set)):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def label_tuple(label):
    return tuple(int(part) for part in label)


def all_subsets(labels):
    labels = tuple(labels)
    for size in range(len(labels) + 1):
        for combo in combinations(labels, size):
            yield combo


def subset_sum(row, subset):
    contributions = row["volatile_channel_contributions"]
    return math.fsum(contributions[str(label)] for label in subset)


def summarize(values):
    values = tuple(values)
    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None}
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def compact_subset_row(row, target_passes):
    return {
        "subset_labels": row["subset_labels"],
        "subset_size": row["subset_size"],
        "volatile_subset_sum": row["volatile_subset_sum"],
        "margin_to_floor": row["margin_to_floor"],
        "satisfies_row_classification": row[
            "satisfies_row_classification"],
        "slack_for_classification": (
            row["margin_to_floor"] if target_passes
            else -row["margin_to_floor"]),
    }


def main():
    source = json.loads(SUBSET_SOURCE.read_text(encoding="utf-8"))
    criticality = json.loads(CRITICALITY_SOURCE.read_text(encoding="utf-8"))
    labels = tuple(label_tuple(label) for label in source["volatile_labels"])
    target_rows = {
        int(target): row for target, row in source["target_rows"].items()
    }
    critical_by_target = {
        row["target"]: tuple(label_tuple(label)
                             for label in row["critical_volatile_channels"])
        for row in criticality["row_criticality"]
    }

    row_thresholds = []
    satisfying_counts = []
    minimal_satisfying_sizes = []
    for target, row in sorted(target_rows.items()):
        target_passes = bool(row["dominant_floor_passes"])
        stable_margin = row["stable_core_sum_to_principal"] + .3
        threshold = -stable_margin
        full_volatile_sum = row["full_volatile_sum_to_principal"]
        full_margin = stable_margin + full_volatile_sum
        subset_rows = []
        for subset in all_subsets(labels):
            value = subset_sum(row, subset)
            margin = stable_margin + value
            predicted_passes = margin >= 0.0
            satisfies = predicted_passes == target_passes
            subset_rows.append({
                "subset_labels": subset,
                "subset_size": len(subset),
                "volatile_subset_sum": value,
                "margin_to_floor": margin,
                "satisfies_row_classification": satisfies,
            })
        satisfying = [
            item for item in subset_rows
            if item["satisfies_row_classification"]]
        failing = [
            item for item in subset_rows
            if not item["satisfies_row_classification"]]
        minimum_size = min(item["subset_size"] for item in satisfying)
        minimal = [
            item for item in satisfying
            if item["subset_size"] == minimum_size]
        if target_passes:
            nearest_failing = sorted(
                failing,
                key=lambda item: (
                    abs(item["margin_to_floor"]),
                    item["subset_size"],
                    item["subset_labels"]),
            )[:8]
            nearest_satisfying = sorted(
                satisfying,
                key=lambda item: (
                    item["margin_to_floor"],
                    item["subset_size"],
                    item["subset_labels"]),
            )[:8]
        else:
            nearest_failing = sorted(
                failing,
                key=lambda item: (
                    abs(item["margin_to_floor"]),
                    item["subset_size"],
                    item["subset_labels"]),
            )[:8]
            nearest_satisfying = sorted(
                satisfying,
                key=lambda item: (
                    -item["margin_to_floor"],
                    item["subset_size"],
                    item["subset_labels"]),
            )[:8]
        all_satisfying_sets = [
            frozenset(item["subset_labels"]) for item in satisfying]
        necessary = (
            set.intersection(*map(set, all_satisfying_sets))
            if all_satisfying_sets else set())

        row_thresholds.append({
            "target": target,
            "target_mod_286": row["target_mod_286"],
            "dominant_floor_passes": target_passes,
            "stable_core_sum_to_principal": row[
                "stable_core_sum_to_principal"],
            "stable_core_margin_to_floor": stable_margin,
            "stable_core_alone_matches_row": (
                (stable_margin >= 0.0) == target_passes),
            "volatile_threshold_for_floor": threshold,
            "classification_condition": (
                "volatile_subset_sum >= threshold"
                if target_passes
                else "volatile_subset_sum < threshold"),
            "full_volatile_sum_to_principal": full_volatile_sum,
            "full_margin_to_floor": full_margin,
            "full_volatile_slack_for_row_classification": (
                full_margin if target_passes else -full_margin),
            "satisfying_subset_count": len(satisfying),
            "failing_subset_count": len(failing),
            "minimum_satisfying_subset_size": minimum_size,
            "minimal_satisfying_subset_count": len(minimal),
            "minimal_satisfying_subsets_sample": tuple(
                compact_subset_row(item, target_passes)
                for item in sorted(
                    minimal,
                    key=lambda item: (
                        item["subset_size"],
                        item["subset_labels"]))[:12]),
            "nearest_satisfying_subsets": tuple(
                compact_subset_row(item, target_passes)
                for item in nearest_satisfying),
            "nearest_failing_subsets": tuple(
                compact_subset_row(item, target_passes)
                for item in nearest_failing),
            "necessary_channels_across_row_satisfying_subsets": tuple(
                sorted(necessary)),
            "leave_one_out_critical_channels": critical_by_target.get(
                target, ()),
            "leave_one_out_critical_channel_count": len(
                critical_by_target.get(target, ())),
        })
        satisfying_counts.append(len(satisfying))
        minimal_satisfying_sizes.append(minimum_size)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_evidence": str(SUBSET_SOURCE.relative_to(ROOT)),
        "source_channel_criticality": str(
            CRITICALITY_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite volatile-row threshold diagnostic only; no volatile-rim "
            "theorem, stable-core theorem, selected-fixture classifier "
            "theorem, pointwise character-sum estimate, or Goldbach proof is "
            "established"),
        "mechanism": (
            "Rewrite selected-row classification as stable-core margin plus "
            "a volatile-subset sum crossing the zero floor."),
        "prediction": (
            "Rows with few satisfying volatile subsets or large minimal "
            "satisfying subset size are the hard row-specific theorem "
            "obligations; rows whose satisfying subset intersection is empty "
            "need aggregate rather than individually necessary channels."),
        "falsifier": (
            "A mismatch between full volatile classification and the stored "
            "dominant-floor classification falsifies this threshold ledger."),
        "arithmetic_modulus": source["arithmetic_modulus"],
        "support": source["support"],
        "dominant_modes": source["dominant_modes"],
        "tail_threshold": source["tail_threshold"],
        "active_real_channel_count": source["active_real_channel_count"],
        "sample_targets": source["sample_targets"],
        "volatile_labels": labels,
        "volatile_channel_count": len(labels),
        "row_thresholds": tuple(row_thresholds),
        "satisfying_subset_count_summary": summarize(satisfying_counts),
        "minimum_satisfying_subset_size_summary": summarize(
            minimal_satisfying_sizes),
        "hardest_rows_by_satisfying_subset_count": tuple(sorted(
            row_thresholds,
            key=lambda row: (
                row["satisfying_subset_count"],
                -row["minimum_satisfying_subset_size"],
                row["target"]))[:5]),
        "hardest_rows_by_minimum_satisfying_subset_size": tuple(sorted(
            row_thresholds,
            key=lambda row: (
                -row["minimum_satisfying_subset_size"],
                row["satisfying_subset_count"],
                row["target"]))[:5]),
        "all_full_volatile_rows_match_classification": all(
            row["full_volatile_slack_for_row_classification"] >= 0.0
            for row in row_thresholds),
        "interpretation": {
            "row_thresholds": (
                "Each selected row now has an explicit threshold inequality "
                "for the volatile subset sum."),
            "aggregate_boundary": (
                "The selected fixture is governed by aggregate subset sums; "
                "rowwise satisfying sets need not share individually "
                "necessary channels."),
            "remaining_theorem": (
                "Prove these signed row-threshold inequalities from actual "
                "binary-prime residue arithmetic, or replace them with a "
                "non-circular arithmetic placement theorem."),
        },
        "volatile_row_thresholds_measured": True,
        "volatile_threshold_theorem_proved": False,
        "volatile_rim_theorem_proved": False,
        "stable_core_theorem_proved": False,
        "selected_fixture_classifier_theorem_proved": False,
        "pointwise_character_sum_estimate_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
