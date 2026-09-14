"""Build q286 volatile forced-channel attribution evidence.

The common-core obstruction shows that the hardest selected deficit rows share
only the full volatile rim.  This derivative receipt asks whether that full
rim is opaque, or whether its channels can be attributed to smaller row and
group obligations.
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
COMMON_CORE_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-common-core-obstruction.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-forced-channel-attribution.json")


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


def margin_to_floor(row, subset):
    return row["stable_core_sum_to_principal"] + .3 + subset_sum(row, subset)


def satisfies_row(row, subset):
    target_passes = bool(row["dominant_floor_passes"])
    predicted_passes = margin_to_floor(row, subset) >= 0.0
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


def classify_subset(name, subset, target_rows, labels):
    rows = []
    false_positive_targets = []
    false_negative_targets = []
    for target, row in sorted(target_rows.items()):
        margin = margin_to_floor(row, subset)
        expected_passes = bool(row["dominant_floor_passes"])
        predicted_passes = margin >= 0.0
        ok = predicted_passes == expected_passes
        if ok is False and expected_passes is False:
            false_positive_targets.append(target)
        if ok is False and expected_passes is True:
            false_negative_targets.append(target)
        rows.append({
            "target": target,
            "target_mod_286": row["target_mod_286"],
            "expected_dominant_floor_passes": expected_passes,
            "predicted_dominant_floor_passes": predicted_passes,
            "margin_to_floor": margin,
            "matches_expected_classification": ok,
        })
    return {
        "name": name,
        **subset_record(subset, labels),
        "false_positive_targets": tuple(false_positive_targets),
        "false_negative_targets": tuple(false_negative_targets),
        "mismatch_targets": tuple(
            row["target"] for row in rows
            if not row["matches_expected_classification"]),
        "exact_selected_classification": not (
            false_positive_targets or false_negative_targets),
        "rows": tuple(rows),
    }


def channel_attribution(labels, necessary_by_target, combination_hinge):
    rows = []
    for label in labels:
        forced_by = tuple(
            target for target, necessary in sorted(necessary_by_target.items())
            if label in necessary)
        if forced_by:
            attribution = "individually_necessary_for_rows"
        elif label in combination_hinge:
            attribution = "combination_hinge"
        else:
            attribution = "not_forced_by_this_hard_row_attribution"
        rows.append({
            "label": label,
            "attribution": attribution,
            "individually_necessary_for_targets": forced_by,
        })
    return tuple(rows)


def main():
    subset_payload = json.loads(SUBSET_SOURCE.read_text(encoding="utf-8"))
    threshold_payload = json.loads(
        THRESHOLD_SOURCE.read_text(encoding="utf-8"))
    common_payload = json.loads(
        COMMON_CORE_SOURCE.read_text(encoding="utf-8"))
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

    all_subsets_list = tuple(all_subsets(labels))
    satisfying_by_target = {}
    necessary_by_target = {}
    for target, row in sorted(target_rows.items()):
        satisfying = {
            subset for subset in all_subsets_list
            if satisfies_row(row, subset)
        }
        stored = stored_by_target[target]
        if len(satisfying) != stored["satisfying_subset_count"]:
            raise AssertionError(f"satisfying count mismatch for {target}")
        necessary = set.intersection(*map(set, satisfying))
        stored_necessary = {
            label_tuple(label)
            for label in stored[
                "necessary_channels_across_row_satisfying_subsets"]
        }
        if necessary != stored_necessary:
            raise AssertionError(f"necessary-channel mismatch for {target}")
        satisfying_by_target[target] = satisfying
        necessary_by_target[target] = necessary

    hard_targets = tuple(common_payload["hard_deficit_targets"])
    if hard_targets != (13822, 1222142, 164598):
        raise AssertionError(
            f"unexpected hard target order from common source: {hard_targets}")
    full_subset = frozenset(labels)
    hard_common = set.intersection(
        *(satisfying_by_target[target] for target in hard_targets))
    if hard_common != {full_subset}:
        raise AssertionError(
            "hard targets no longer share exactly the full volatile rim")

    row_forced_targets = (13822, 164598)
    row_forced_union = frozenset().union(
        *(necessary_by_target[target] for target in row_forced_targets))
    if len(row_forced_union) != len(labels) - 1:
        raise AssertionError(
            "the selected row-forced union is no longer a seven-channel set")
    combination_hinge = full_subset - row_forced_union
    if combination_hinge != {(4, 10)}:
        raise AssertionError(
            f"unexpected combination hinge: {sorted(combination_hinge)}")

    forced_subset_row = classify_subset(
        "row_forced_union_from_13822_and_164598",
        row_forced_union,
        target_rows,
        labels)
    full_subset_row = classify_subset(
        "full_volatile_rim",
        full_subset,
        target_rows,
        labels)
    hinge_added_row = classify_subset(
        "row_forced_union_plus_combination_hinge",
        row_forced_union | combination_hinge,
        target_rows,
        labels)
    if forced_subset_row["mismatch_targets"] != (1222142,):
        raise AssertionError(
            "seven-channel row-forced union no longer has exactly target "
            f"1222142 as its mismatch: {forced_subset_row['mismatch_targets']}")
    if full_subset_row["exact_selected_classification"] is not True:
        raise AssertionError("full volatile rim no longer classifies exactly")

    hard_rows = []
    for target in hard_targets:
        hard_rows.append({
            "target": target,
            "dominant_floor_passes": target_rows[target][
                "dominant_floor_passes"],
            "satisfying_subset_count": len(satisfying_by_target[target]),
            "minimum_satisfying_subset_size": stored_by_target[target][
                "minimum_satisfying_subset_size"],
            "necessary_channels": tuple(sorted(
                necessary_by_target[target])),
            "row_forced_union_margin_to_floor": margin_to_floor(
                target_rows[target], row_forced_union),
            "full_rim_margin_to_floor": margin_to_floor(
                target_rows[target], full_subset),
            "hinge_channel_contribution": subset_sum(
                target_rows[target], combination_hinge),
        })

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_subset_ablation": str(SUBSET_SOURCE.relative_to(ROOT)),
        "source_row_thresholds": str(THRESHOLD_SOURCE.relative_to(ROOT)),
        "source_common_core_obstruction": str(
            COMMON_CORE_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite volatile forced-channel attribution only; no "
            "volatile-rim theorem, stable-core theorem, selected-fixture "
            "classifier theorem, pointwise character-sum estimate, or "
            "Goldbach proof is established"),
        "candidate": (
            "The full volatile rim may decompose into row-attributed hard "
            "obligations rather than being an opaque eight-channel object."),
        "mechanism": (
            "Use rowwise necessary channels from satisfying-subset families, "
            "then test the union of individually forced hard-row channels "
            "against the remaining hard target."),
        "prediction": (
            "If the seven channels forced by 13822 and 164598 almost classify "
            "the fixture, the missing eighth channel is a combination hinge "
            "rather than an independent row necessity."),
        "falsifier": (
            "If the row-forced union has more than one mismatch, or if adding "
            "the hinge does not restore exact selected classification, this "
            "attribution fails."),
        "novelty_label": "new-to-this-task",
        "arithmetic_modulus": threshold_payload["arithmetic_modulus"],
        "support": threshold_payload["support"],
        "dominant_modes": threshold_payload["dominant_modes"],
        "tail_threshold": threshold_payload["tail_threshold"],
        "volatile_labels": labels,
        "volatile_channel_count": len(labels),
        "tested_subset_count": len(all_subsets_list),
        "hard_deficit_targets": hard_targets,
        "row_forced_targets": row_forced_targets,
        "row_forced_union": subset_record(row_forced_union, labels),
        "combination_hinge": subset_record(combination_hinge, labels),
        "hard_common_subset_count": len(hard_common),
        "hard_common_subset": subset_record(next(iter(hard_common)), labels),
        "hard_rows": tuple(hard_rows),
        "channel_attribution": channel_attribution(
            labels, necessary_by_target, combination_hinge),
        "row_forced_union_classification": forced_subset_row,
        "full_volatile_rim_classification": full_subset_row,
        "hinge_added_classification": hinge_added_row,
        "source_common_core_matches": (
            common_payload["hard_deficit_common_subset_count"] == 1
            and common_payload[
                "hard_deficit_proper_common_subset_exists"] is False),
        "interpretation": {
            "row_attribution": (
                "Five channels are individually necessary for 13822 and two "
                "different channels are individually necessary for 164598."),
            "combination_hinge": (
                "The remaining channel (4,10) is not individually necessary "
                "for those two rows, but adding it is what changes 1222142 "
                "from a false positive to a correctly classified deficit."),
            "remaining_theorem": (
                "A non-circular theorem can now target the five-channel "
                "13822 obligation, the two-channel 164598 obligation, and "
                "the (4,10) combination hinge for 1222142, or replace this "
                "decomposition with an aggregate arithmetic-placement proof."),
        },
        "volatile_forced_channel_attribution_measured": True,
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
