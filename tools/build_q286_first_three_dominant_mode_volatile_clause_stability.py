"""Build q286 volatile minimal-clause stability evidence.

The minimal-clause receipt extracts inclusion-minimal satisfying volatile
subsets for selected deficit rows.  This derivative receipt checks whether
those clauses are stable under adding the remaining volatile channels, or
whether extra channels can undo the deficit classification.
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
CLAUSE_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-minimal-clause-structure.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-clause-stability.json")


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


def minimal_clauses_for_target(clause_payload, target):
    for row in clause_payload["deficit_clause_rows"]:
        if int(row["target"]) == target:
            return tuple(
                frozenset(label_tuple(label)
                          for label in clause["subset_labels"])
                for clause in row["minimal_clauses"])
    raise KeyError(target)


def clause_stability_row(target, row, minimal_clauses, all_subsets_list, labels):
    clause_rows = []
    for clause in minimal_clauses:
        supersets = tuple(
            subset for subset in all_subsets_list if clause <= subset)
        satisfying = tuple(
            subset for subset in supersets if satisfies_row(row, subset))
        failing = tuple(
            subset for subset in supersets if not satisfies_row(row, subset))
        nearest_failing = sorted(
            failing,
            key=lambda subset: (
                abs(margin_to_floor(row, subset)),
                len(subset),
                sorted(subset)))[:8]
        nearest_satisfying = sorted(
            satisfying,
            key=lambda subset: (
                -margin_to_floor(row, subset),
                len(subset),
                sorted(subset)))[:8]
        clause_rows.append({
            "clause": subset_record(clause, labels, row),
            "superset_count": len(supersets),
            "satisfying_superset_count": len(satisfying),
            "failing_superset_count": len(failing),
            "stable_under_all_supersets": len(failing) == 0,
            "nearest_failing_supersets": tuple(
                subset_record(subset, labels, row)
                for subset in nearest_failing),
            "nearest_satisfying_supersets": tuple(
                subset_record(subset, labels, row)
                for subset in nearest_satisfying),
        })
    stable_count = sum(
        1 for clause in clause_rows
        if clause["stable_under_all_supersets"])
    return {
        "target": target,
        "target_mod_286": row["target_mod_286"],
        "minimal_clause_count": len(clause_rows),
        "stable_clause_count": stable_count,
        "fragile_clause_count": len(clause_rows) - stable_count,
        "all_minimal_clauses_stable": stable_count == len(clause_rows),
        "any_minimal_clause_stable": stable_count > 0,
        "clause_rows": tuple(clause_rows),
    }


def main():
    subset_payload = json.loads(SUBSET_SOURCE.read_text(encoding="utf-8"))
    clause_payload = json.loads(CLAUSE_SOURCE.read_text(encoding="utf-8"))
    labels = tuple(label_tuple(label) for label in subset_payload[
        "volatile_labels"])
    all_subsets_list = tuple(all_subsets(labels))
    target_rows = {
        int(target): row
        for target, row in subset_payload["target_rows"].items()
    }
    deficit_targets = tuple(clause_payload["deficit_targets"])
    hard_targets = tuple(clause_payload["hard_deficit_targets"])

    stability_rows = []
    for target in deficit_targets:
        row = target_rows[target]
        clauses = minimal_clauses_for_target(clause_payload, target)
        stability = clause_stability_row(
            target, row, clauses, all_subsets_list, labels)
        stability_rows.append(stability)

    by_target = {row["target"]: row for row in stability_rows}
    if by_target[13822]["stable_clause_count"] != 1:
        raise AssertionError("13822 stable-clause count changed")
    if by_target[164598]["stable_clause_count"] != 1:
        raise AssertionError("164598 stable-clause count changed")
    if by_target[1222142]["stable_clause_count"] != 0:
        raise AssertionError("1222142 unexpectedly has a stable clause")
    if by_target[1222142]["fragile_clause_count"] != 10:
        raise AssertionError("1222142 fragile-clause count changed")

    hard_rows = tuple(
        row for row in stability_rows if row["target"] in hard_targets)
    fragile_hard_clause_count = sum(
        row["fragile_clause_count"] for row in hard_rows)
    stable_hard_clause_count = sum(
        row["stable_clause_count"] for row in hard_rows)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_subset_ablation": str(SUBSET_SOURCE.relative_to(ROOT)),
        "source_minimal_clause_structure": str(
            CLAUSE_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite volatile clause-stability diagnostic only; no "
            "volatile-rim theorem, stable-core theorem, selected-fixture "
            "classifier theorem, pointwise character-sum estimate, or "
            "Goldbach proof is established"),
        "candidate": (
            "Forcing one inclusion-minimal volatile clause might be enough "
            "to preserve a deficit row even after additional volatile "
            "channels are present."),
        "mechanism": (
            "For each minimal satisfying deficit-row clause, enumerate all "
            "volatile supersets and count which supersets still satisfy the "
            "row classification."),
        "prediction": (
            "Stable clauses can be theorem targets by themselves; fragile "
            "clauses require a separate non-undo or signed-aggregate bound."),
        "falsifier": (
            "A failing superset of a minimal satisfying clause falsifies the "
            "claim that the clause alone is sufficient under arbitrary extra "
            "volatile channels."),
        "novelty_label": "new-to-this-task",
        "arithmetic_modulus": clause_payload["arithmetic_modulus"],
        "support": clause_payload["support"],
        "dominant_modes": clause_payload["dominant_modes"],
        "tail_threshold": clause_payload["tail_threshold"],
        "volatile_labels": labels,
        "volatile_channel_count": len(labels),
        "tested_subset_count": len(all_subsets_list),
        "deficit_targets": deficit_targets,
        "hard_deficit_targets": hard_targets,
        "hard_stable_clause_count": stable_hard_clause_count,
        "hard_fragile_clause_count": fragile_hard_clause_count,
        "stability_rows": tuple(stability_rows),
        "hard_stability_rows": hard_rows,
        "summary": {
            "target_13822": (
                "one of two minimal clauses is stable under all supersets; "
                "the other has one failing superset"),
            "target_164598": (
                "one of two minimal clauses is stable under all supersets; "
                "the other has two failing supersets"),
            "target_1222142": (
                "all ten minimal clauses are fragile, each with five failing "
                "supersets"),
        },
        "interpretation": {
            "stable_clauses": (
                "Some compact hard-row clauses survive arbitrary addition of "
                "remaining volatile channels on this fixture."),
            "fragile_clauses": (
                "Minimality alone is not a theorem: extra volatile channels "
                "can undo deficit classification for 13822, 164598, and all "
                "ten 1222142 clauses."),
            "remaining_theorem": (
                "The next proof target must pair clause forcing with "
                "non-undo control for adverse extra channels, or abandon "
                "the Boolean-clause view in favor of a signed aggregate "
                "arithmetic-placement theorem."),
        },
        "volatile_clause_stability_measured": True,
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
