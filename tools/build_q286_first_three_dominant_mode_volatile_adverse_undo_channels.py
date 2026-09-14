"""Build q286 volatile adverse undo-channel evidence.

The clause-stability receipt shows that most minimal deficit clauses are
fragile under extra volatile channels.  This derivative receipt extracts the
inclusion-minimal added channel sets that undo each fragile clause.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUBSET_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-subset-ablation.json")
CLAUSE_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-minimal-clause-structure.json")
STABILITY_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-clause-stability.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-adverse-undo-channels.json")


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
    return math.fsum(
        row["volatile_channel_contributions"][label_key(label)]
        for label in subset)


def margin_to_floor(row, subset):
    return row["stable_core_sum_to_principal"] + .3 + subset_sum(row, subset)


def satisfies_row(row, subset):
    expected = bool(row["dominant_floor_passes"])
    actual = margin_to_floor(row, subset) >= 0.0
    return actual == expected


def subset_record(subset, labels, row=None):
    subset = frozenset(subset)
    mask = 0
    for index, label in enumerate(labels):
        if label in subset:
            mask |= 1 << index
    record = {
        "mask": mask,
        "subset_size": len(subset),
        "subset_labels": tuple(sorted(subset)),
    }
    if row is not None:
        record["margin_to_floor"] = margin_to_floor(row, subset)
        record["volatile_subset_sum"] = subset_sum(row, subset)
        record["satisfies_deficit_classification"] = satisfies_row(
            row, subset)
    return record


def minimal_sets(sets):
    sets = tuple(sets)
    return tuple(sorted(
        (
            item for item in sets
            if not any(other < item for other in sets)
        ),
        key=lambda item: (len(item), sorted(item))))


def minimal_clauses_for_target(clause_payload, target):
    for row in clause_payload["deficit_clause_rows"]:
        if int(row["target"]) == target:
            return tuple(
                frozenset(label_tuple(label)
                          for label in clause["subset_labels"])
                for clause in row["minimal_clauses"])
    raise KeyError(target)


def clause_undo_row(target, row, clause, labels, all_subsets_list):
    supersets = tuple(subset for subset in all_subsets_list if clause <= subset)
    failing_supersets = tuple(
        subset for subset in supersets if not satisfies_row(row, subset))
    added_sets = tuple(subset - clause for subset in failing_supersets)
    minimal_added = minimal_sets(added_sets)
    nearest_failing = sorted(
        failing_supersets,
        key=lambda subset: (
            abs(margin_to_floor(row, subset)),
            len(subset),
            sorted(subset)))[:8]
    return {
        "clause": subset_record(clause, labels, row),
        "superset_count": len(supersets),
        "failing_superset_count": len(failing_supersets),
        "minimal_adverse_addition_count": len(minimal_added),
        "minimal_adverse_additions": tuple(
            subset_record(added, labels) for added in minimal_added),
        "nearest_failing_supersets": tuple(
            {
                **subset_record(subset, labels, row),
                "added_channels": subset_record(subset - clause, labels),
            }
            for subset in nearest_failing),
    }


def target_undo_row(target, row, clauses, labels, all_subsets_list):
    clause_rows = tuple(
        clause_undo_row(target, row, clause, labels, all_subsets_list)
        for clause in clauses)
    fragile_rows = tuple(
        item for item in clause_rows if item["failing_superset_count"])
    stable_rows = tuple(
        item for item in clause_rows if not item["failing_superset_count"])
    adverse_counter = Counter()
    all_minimal_added = []
    for item in fragile_rows:
        for added in item["minimal_adverse_additions"]:
            added_labels = tuple(label_tuple(label)
                                 for label in added["subset_labels"])
            all_minimal_added.append(frozenset(added_labels))
            for label in added_labels:
                adverse_counter[label] += 1
    common_adverse_channels = (
        set.intersection(*map(set, all_minimal_added))
        if all_minimal_added else set())
    return {
        "target": target,
        "target_mod_286": row["target_mod_286"],
        "minimal_clause_count": len(clause_rows),
        "stable_clause_count": len(stable_rows),
        "fragile_clause_count": len(fragile_rows),
        "minimal_adverse_addition_count": len(all_minimal_added),
        "minimal_adverse_addition_size_counts": {
            str(size): sum(
                1 for added in all_minimal_added if len(added) == size)
            for size in range(len(labels) + 1)
            if any(len(added) == size for added in all_minimal_added)
        },
        "common_channels_across_minimal_adverse_additions": tuple(sorted(
            common_adverse_channels)),
        "adverse_channel_frequency": tuple({
            "label": label,
            "minimal_adverse_addition_count": adverse_counter[label],
        } for label in labels if adverse_counter[label]),
        "clause_rows": clause_rows,
    }


def main():
    subset_payload = json.loads(SUBSET_SOURCE.read_text(encoding="utf-8"))
    clause_payload = json.loads(CLAUSE_SOURCE.read_text(encoding="utf-8"))
    stability_payload = json.loads(
        STABILITY_SOURCE.read_text(encoding="utf-8"))
    labels = tuple(label_tuple(label) for label in subset_payload[
        "volatile_labels"])
    all_subsets_list = tuple(all_subsets(labels))
    target_rows = {
        int(target): row
        for target, row in subset_payload["target_rows"].items()
    }
    hard_targets = tuple(stability_payload["hard_deficit_targets"])

    undo_rows = []
    for target in clause_payload["deficit_targets"]:
        target = int(target)
        clauses = minimal_clauses_for_target(clause_payload, target)
        undo_rows.append(target_undo_row(
            target, target_rows[target], clauses, labels, all_subsets_list))

    by_target = {row["target"]: row for row in undo_rows}
    if by_target[1222142]["fragile_clause_count"] != 10:
        raise AssertionError("1222142 fragile clause count changed")
    target_1222142_adverse = {
        tuple(label_tuple(label) for label in item["subset_labels"])
        for clause in by_target[1222142]["clause_rows"]
        for item in clause["minimal_adverse_additions"]
    }
    expected_1222142 = {((1, 7),), ((4, 4),)}
    if target_1222142_adverse != expected_1222142:
        raise AssertionError(
            "1222142 minimal adverse additions changed: "
            f"{target_1222142_adverse}")
    if by_target[13822]["minimal_adverse_addition_count"] != 1:
        raise AssertionError("13822 adverse count changed")
    if by_target[164598]["minimal_adverse_addition_count"] != 1:
        raise AssertionError("164598 adverse count changed")

    hard_rows = tuple(row for row in undo_rows if row["target"] in hard_targets)
    hard_counter = Counter()
    for row in hard_rows:
        for item in row["adverse_channel_frequency"]:
            hard_counter[label_tuple(item["label"])] += item[
                "minimal_adverse_addition_count"]

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_subset_ablation": str(SUBSET_SOURCE.relative_to(ROOT)),
        "source_minimal_clause_structure": str(
            CLAUSE_SOURCE.relative_to(ROOT)),
        "source_clause_stability": str(STABILITY_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite volatile adverse undo-channel diagnostic only; no "
            "volatile-rim theorem, stable-core theorem, selected-fixture "
            "classifier theorem, pointwise character-sum estimate, or "
            "Goldbach proof is established"),
        "candidate": (
            "The non-undo obstruction may be controlled by a small set of "
            "named adverse channels rather than arbitrary volatile additions."),
        "mechanism": (
            "For each fragile minimal deficit-row clause, extract inclusion-"
            "minimal added channel sets whose superset fails the same row "
            "classification."),
        "prediction": (
            "If adverse additions are small and recurrent, they become a "
            "sharper non-undo theorem target; if they are diffuse, the clause "
            "route should give way to a signed aggregate theorem."),
        "falsifier": (
            "If the fragile-clause counts or minimal adverse additions drift "
            "from the clause-stability receipt, this undo-channel ledger is "
            "invalid."),
        "novelty_label": "new-to-this-task",
        "arithmetic_modulus": clause_payload["arithmetic_modulus"],
        "support": clause_payload["support"],
        "dominant_modes": clause_payload["dominant_modes"],
        "tail_threshold": clause_payload["tail_threshold"],
        "volatile_labels": labels,
        "volatile_channel_count": len(labels),
        "tested_subset_count": len(all_subsets_list),
        "hard_deficit_targets": hard_targets,
        "undo_rows": tuple(undo_rows),
        "hard_undo_rows": hard_rows,
        "hard_adverse_channel_frequency": tuple({
            "label": label,
            "minimal_adverse_addition_count": hard_counter[label],
        } for label in sorted(hard_counter)),
        "summary": {
            "target_13822": (
                "one fragile clause; its single minimal adverse addition is "
                "(1,5)"),
            "target_164598": (
                "one fragile clause; its single minimal adverse addition is "
                "the two-channel set (1,1),(1,3)"),
            "target_1222142": (
                "all ten clauses are fragile, and the only minimal adverse "
                "one-channel additions are (1,7) and (4,4), recurring for "
                "every clause"),
        },
        "interpretation": {
            "non_undo_target": (
                "The hardest disjunctive row 1222142 has a two-channel "
                "undo pattern: every minimal clause is vulnerable to adding "
                "either (1,7) or (4,4)."),
            "route_status": (
                "The clause route remains alive but narrower: it must pair "
                "clause forcing with control of named adverse additions."),
            "remaining_theorem": (
                "Prove a signed non-undo estimate for the adverse channels "
                "in the actual binary-prime residue weights, or replace the "
                "Boolean-clause route with a full signed aggregate theorem."),
        },
        "volatile_adverse_undo_channels_measured": True,
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
