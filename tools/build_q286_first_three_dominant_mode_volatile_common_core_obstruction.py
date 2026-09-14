"""Build q286 volatile common-core obstruction evidence.

The volatile row-threshold receipt turns each selected row into a subset
inequality.  This derivative receipt asks whether the hardest deficit rows
share a proper volatile core, or whether the full eight-channel rim is still
needed even before clear-side constraints are imposed.
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
THRESHOLD_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-row-thresholds.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-common-core-obstruction.json")


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


def label_key(label):
    return str(tuple(label))


def all_subsets(labels):
    labels = tuple(labels)
    for size in range(len(labels) + 1):
        for combo in combinations(labels, size):
            yield frozenset(combo)


def subset_sum(row, subset):
    contributions = row["volatile_channel_contributions"]
    return math.fsum(contributions[label_key(label)] for label in subset)


def satisfies_row(row, subset):
    target_passes = bool(row["dominant_floor_passes"])
    stable_margin = row["stable_core_sum_to_principal"] + .3
    predicted_passes = (stable_margin + subset_sum(row, subset)) >= 0.0
    return predicted_passes == target_passes


def subset_record(subset, labels):
    subset = frozenset(subset)
    mask = 0
    for index, label in enumerate(labels):
        if label in subset:
            mask |= 1 << index
    return {
        "mask": mask,
        "subset_size": len(subset),
        "subset_labels": tuple(sorted(subset)),
    }


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


def group_summary(name, targets, satisfying_by_target, labels):
    intersection = set.intersection(
        *(satisfying_by_target[target] for target in targets))
    union = set.union(*(satisfying_by_target[target] for target in targets))
    sorted_intersection = sorted(
        intersection, key=lambda subset: (len(subset), sorted(subset)))
    minimum_size = len(sorted_intersection[0]) if sorted_intersection else None
    full_subset = frozenset(labels)
    return {
        "name": name,
        "targets": tuple(targets),
        "target_count": len(targets),
        "intersection_count": len(intersection),
        "union_count": len(union),
        "jaccard_index": (
            len(intersection) / len(union) if union else None),
        "minimum_intersection_subset_size": minimum_size,
        "proper_common_subset_exists": any(
            len(subset) < len(labels) for subset in intersection),
        "full_volatile_subset_is_common": full_subset in intersection,
        "intersection_subset_sample": tuple(
            subset_record(subset, labels) for subset in sorted_intersection[:12]),
    }


def pairwise_summary(targets, satisfying_by_target, labels):
    rows = []
    for left, right in combinations(targets, 2):
        intersection = (
            satisfying_by_target[left] & satisfying_by_target[right])
        union = satisfying_by_target[left] | satisfying_by_target[right]
        sorted_intersection = sorted(
            intersection, key=lambda subset: (len(subset), sorted(subset)))
        rows.append({
            "targets": (left, right),
            "intersection_count": len(intersection),
            "union_count": len(union),
            "jaccard_index": len(intersection) / len(union),
            "minimum_intersection_subset_size": (
                len(sorted_intersection[0]) if sorted_intersection else None),
            "proper_common_subset_exists": any(
                len(subset) < len(labels) for subset in intersection),
            "intersection_subset_sample": tuple(
                subset_record(subset, labels)
                for subset in sorted_intersection[:8]),
        })
    return tuple(rows)


def channel_frequency(target, satisfying_subsets, labels):
    total = len(satisfying_subsets)
    rows = []
    for label in labels:
        count = sum(1 for subset in satisfying_subsets if label in subset)
        rows.append({
            "target": target,
            "label": label,
            "satisfying_subset_count": count,
            "frequency": count / total if total else None,
        })
    return tuple(sorted(
        rows,
        key=lambda row: (-row["satisfying_subset_count"], row["label"])))


def main():
    subset_payload = json.loads(SUBSET_SOURCE.read_text(encoding="utf-8"))
    threshold_payload = json.loads(
        THRESHOLD_SOURCE.read_text(encoding="utf-8"))
    labels = tuple(label_tuple(label) for label in subset_payload[
        "volatile_labels"])
    target_rows = {
        int(target): row
        for target, row in subset_payload["target_rows"].items()
    }
    stored_by_target = {
        int(row["target"]): row
        for row in threshold_payload["row_thresholds"]
    }

    satisfying_by_target = {}
    all_subsets_list = tuple(all_subsets(labels))
    for target, row in sorted(target_rows.items()):
        satisfying = {
            subset for subset in all_subsets_list
            if satisfies_row(row, subset)
        }
        stored = stored_by_target[target]
        if len(satisfying) != stored["satisfying_subset_count"]:
            raise AssertionError(
                f"satisfying count mismatch for {target}: "
                f"{len(satisfying)} != {stored['satisfying_subset_count']}")
        minimum_size = min(len(subset) for subset in satisfying)
        if minimum_size != stored["minimum_satisfying_subset_size"]:
            raise AssertionError(
                f"minimum subset size mismatch for {target}: "
                f"{minimum_size} != "
                f"{stored['minimum_satisfying_subset_size']}")
        satisfying_by_target[target] = satisfying

    clear_targets = tuple(sorted(
        target for target, row in target_rows.items()
        if row["dominant_floor_passes"]))
    deficit_targets = tuple(sorted(
        target for target, row in target_rows.items()
        if not row["dominant_floor_passes"]))
    hard_deficit_targets = tuple(
        row["target"]
        for row in sorted(
            (stored_by_target[target] for target in deficit_targets),
            key=lambda row: (
                row["satisfying_subset_count"],
                -row["minimum_satisfying_subset_size"],
                row["target"]))[:3])
    all_row_targets = tuple(sorted(target_rows))

    all_row_intersection = set.intersection(
        *(satisfying_by_target[target] for target in all_row_targets))
    source_exact_count = subset_payload["exact_subset_count"]
    if len(all_row_intersection) != source_exact_count:
        raise AssertionError(
            "all-row intersection no longer matches source exact-subset "
            f"count: {len(all_row_intersection)} != {source_exact_count}")

    full_subset = frozenset(labels)
    if full_subset not in all_row_intersection:
        raise AssertionError("full volatile subset does not satisfy all rows")

    group_summaries = (
        group_summary(
            "hardest_three_deficit_rows",
            hard_deficit_targets,
            satisfying_by_target,
            labels),
        group_summary(
            "all_deficit_rows",
            deficit_targets,
            satisfying_by_target,
            labels),
        group_summary(
            "all_clear_rows",
            clear_targets,
            satisfying_by_target,
            labels),
        group_summary(
            "all_selected_rows",
            all_row_targets,
            satisfying_by_target,
            labels),
    )
    by_target = []
    for target in all_row_targets:
        stored = stored_by_target[target]
        satisfying = satisfying_by_target[target]
        by_target.append({
            "target": target,
            "target_mod_286": stored["target_mod_286"],
            "dominant_floor_passes": stored["dominant_floor_passes"],
            "satisfying_subset_count": len(satisfying),
            "minimum_satisfying_subset_size": min(
                len(subset) for subset in satisfying),
            "necessary_channels_across_satisfying_subsets": tuple(sorted(
                set.intersection(*map(set, satisfying)) if satisfying
                else set())),
            "channel_frequency": channel_frequency(
                target, satisfying, labels),
        })

    hard_summary = group_summaries[0]
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_subset_ablation": str(SUBSET_SOURCE.relative_to(ROOT)),
        "source_row_thresholds": str(THRESHOLD_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite volatile common-core obstruction only; no volatile-rim "
            "theorem, stable-core theorem, selected-fixture classifier "
            "theorem, pointwise character-sum estimate, or Goldbach proof is "
            "established"),
        "candidate": (
            "A small row-invariant volatile core might satisfy the hard "
            "deficit-row thresholds while the clear rows remain tolerant."),
        "mechanism": (
            "Intersect the satisfying volatile-subset families for hard "
            "deficit rows after fixing the stable core."),
        "prediction": (
            "A proper common hard-deficit subset would narrow the missing "
            "volatile theorem; if the only common subset is the full rim, "
            "the selected fixture needs row-specific or full-package control."),
        "falsifier": (
            "A proper volatile subset satisfying all hardest deficit-row "
            "thresholds falsifies the common-core obstruction."),
        "novelty_label": "new-to-this-task",
        "arithmetic_modulus": threshold_payload["arithmetic_modulus"],
        "support": threshold_payload["support"],
        "dominant_modes": threshold_payload["dominant_modes"],
        "tail_threshold": threshold_payload["tail_threshold"],
        "volatile_labels": labels,
        "volatile_channel_count": len(labels),
        "tested_subset_count": len(all_subsets_list),
        "clear_targets": clear_targets,
        "deficit_targets": deficit_targets,
        "hard_deficit_targets": hard_deficit_targets,
        "group_summaries": group_summaries,
        "hard_deficit_pairwise_overlap": pairwise_summary(
            hard_deficit_targets, satisfying_by_target, labels),
        "by_target": tuple(by_target),
        "all_selected_common_subset_count": len(all_row_intersection),
        "all_selected_common_subset_sample": tuple(
            subset_record(subset, labels)
            for subset in sorted(
                all_row_intersection,
                key=lambda subset: (len(subset), sorted(subset)))[:12]),
        "source_exact_subset_count_matches": (
            len(all_row_intersection) == source_exact_count),
        "hard_deficit_proper_common_subset_exists": (
            hard_summary["proper_common_subset_exists"]),
        "hard_deficit_common_subset_count": hard_summary[
            "intersection_count"],
        "hard_deficit_minimum_common_subset_size": hard_summary[
            "minimum_intersection_subset_size"],
        "interpretation": {
            "common_core": (
                "The hardest three selected deficit rows have exactly one "
                "common satisfying volatile subset, and it is the full "
                "eight-channel rim."
                if (
                    hard_summary["intersection_count"] == 1
                    and not hard_summary["proper_common_subset_exists"])
                else (
                    "A proper common hard-deficit subset remains available "
                    "on this fixture.")),
            "clear_side": (
                "Clear rows are not the binding common-core obstruction: "
                "many volatile subsets preserve all selected clears."),
            "remaining_theorem": (
                "The next non-circular theorem must explain row-specific "
                "signed volatile action, prove a full-package aggregate "
                "inequality, or replace this split with a stronger arithmetic "
                "placement theorem."),
        },
        "volatile_common_core_obstruction_measured": True,
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
