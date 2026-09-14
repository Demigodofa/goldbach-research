"""Build q286 volatile undo-repair channel evidence.

The adverse-undo receipt identifies minimal added volatile channels that undo
fragile deficit-row clauses.  This derivative receipt asks whether those
adverse additions are terminal, or whether further volatile channels repair
the deficit classification again.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUBSET_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-subset-ablation.json")
ADVERSE_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-adverse-undo-channels.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-undo-repair-channels.json")


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


def repair_event(target, row, clause_record, adverse_record, labels):
    clause = frozenset(
        label_tuple(label) for label in clause_record["subset_labels"])
    adverse = frozenset(
        label_tuple(label) for label in adverse_record["subset_labels"])
    adverse_superset = clause | adverse
    if satisfies_row(row, adverse_superset):
        raise AssertionError(
            f"adverse addition unexpectedly satisfies target {target}")

    remaining = tuple(label for label in labels if label not in adverse_superset)
    repairing_additions = tuple(
        subset for subset in all_subsets(remaining)
        if subset and satisfies_row(row, adverse_superset | subset))
    minimal_repairs = minimal_sets(repairing_additions)
    nearest_repairs = sorted(
        repairing_additions,
        key=lambda subset: (
            abs(margin_to_floor(row, adverse_superset | subset)),
            len(subset),
            sorted(subset)))[:8]
    return {
        "target": target,
        "clause": subset_record(clause, labels, row),
        "minimal_adverse_addition": subset_record(adverse, labels),
        "adverse_superset": subset_record(adverse_superset, labels, row),
        "remaining_channel_count": len(remaining),
        "repairing_addition_count": len(repairing_additions),
        "minimal_repair_addition_count": len(minimal_repairs),
        "minimal_repair_additions": tuple(
            subset_record(repair, labels) for repair in minimal_repairs),
        "nearest_repairing_supersets": tuple(
            {
                **subset_record(adverse_superset | repair, labels, row),
                "repair_addition": subset_record(repair, labels),
            }
            for repair in nearest_repairs),
    }


def repair_rows_for_target(target_row, row, labels):
    target = int(target_row["target"])
    events = []
    for clause_row in target_row["clause_rows"]:
        for adverse in clause_row["minimal_adverse_additions"]:
            events.append(repair_event(
                target, row, clause_row["clause"], adverse, labels))

    repair_counter = Counter()
    size_counter = Counter()
    for event in events:
        for repair in event["minimal_repair_additions"]:
            repair_labels = tuple(
                label_tuple(label) for label in repair["subset_labels"])
            size_counter[len(repair_labels)] += 1
            for label in repair_labels:
                repair_counter[label] += 1

    return {
        "target": target,
        "target_mod_286": row["target_mod_286"],
        "adverse_event_count": len(events),
        "events_without_minimal_repair": sum(
            1 for event in events
            if not event["minimal_repair_additions"]),
        "minimal_repair_addition_count": sum(
            event["minimal_repair_addition_count"] for event in events),
        "minimal_repair_addition_size_counts": {
            str(size): size_counter[size]
            for size in sorted(size_counter)
        },
        "minimal_repair_channel_frequency": tuple({
            "label": label,
            "minimal_repair_addition_count": repair_counter[label],
        } for label in labels if repair_counter[label]),
        "repair_events": tuple(events),
    }


def main():
    subset_payload = json.loads(SUBSET_SOURCE.read_text(encoding="utf-8"))
    adverse_payload = json.loads(ADVERSE_SOURCE.read_text(encoding="utf-8"))
    labels = tuple(label_tuple(label) for label in subset_payload[
        "volatile_labels"])
    target_rows = {
        int(target): row
        for target, row in subset_payload["target_rows"].items()
    }

    undo_rows = tuple(
        repair_rows_for_target(
            target_row, target_rows[int(target_row["target"])], labels)
        for target_row in adverse_payload["undo_rows"])
    hard_targets = tuple(adverse_payload["hard_deficit_targets"])
    hard_rows = tuple(
        row for row in undo_rows if row["target"] in hard_targets)

    event_count = sum(row["adverse_event_count"] for row in undo_rows)
    repair_count = sum(
        row["minimal_repair_addition_count"] for row in undo_rows)
    repairless_count = sum(
        row["events_without_minimal_repair"] for row in undo_rows)
    repair_size_counter = Counter()
    repair_counter = Counter()
    target_repair_counter = defaultdict(Counter)
    for row in undo_rows:
        for event in row["repair_events"]:
            for repair in event["minimal_repair_additions"]:
                repair_labels = tuple(
                    label_tuple(label) for label in repair["subset_labels"])
                repair_size_counter[len(repair_labels)] += 1
                for label in repair_labels:
                    repair_counter[label] += 1
                    target_repair_counter[row["target"]][label] += 1

    if event_count != 26:
        raise AssertionError(f"unexpected adverse event count: {event_count}")
    if repairless_count != 0:
        raise AssertionError("an adverse event has no minimal repair")
    if repair_count != 52:
        raise AssertionError(f"unexpected minimal repair count: {repair_count}")
    if repair_size_counter != Counter({1: 50, 3: 2}):
        raise AssertionError(
            f"unexpected repair size distribution: {repair_size_counter}")
    if target_repair_counter[1222142] != Counter({
            (1, 1): 10,
            (1, 3): 6,
            (1, 5): 4,
            (2, 4): 10,
            (3, 3): 4,
            (4, 10): 6,
    }):
        raise AssertionError("1222142 repair frequency changed")
    if target_repair_counter[13822] != Counter({(4, 4): 1}):
        raise AssertionError("13822 repair frequency changed")
    if target_repair_counter[164598] != Counter({
            (1, 7): 1,
            (4, 10): 1,
    }):
        raise AssertionError("164598 repair frequency changed")

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_subset_ablation": str(SUBSET_SOURCE.relative_to(ROOT)),
        "source_adverse_undo_channels": str(
            ADVERSE_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite volatile undo-repair diagnostic only; no volatile-rim "
            "theorem, stable-core theorem, selected-fixture classifier "
            "theorem, pointwise character-sum estimate, or Goldbach proof is "
            "established"),
        "candidate": (
            "Adverse volatile additions may not be terminal blockers; they "
            "may have small named repair additions that restore the deficit "
            "classification."),
        "mechanism": (
            "Starting from each fragile minimal clause plus one minimal "
            "adverse addition, enumerate remaining volatile additions and "
            "keep the inclusion-minimal additions that repair the row "
            "classification."),
        "prediction": (
            "If repairs are small and recurrent, the theorem target becomes "
            "ordered adverse/repair control rather than pure non-undo.  If "
            "repairs are absent or diffuse, the Boolean-clause route should "
            "give way to a signed aggregate theorem."),
        "falsifier": (
            "A repairless adverse event, a drift in the adverse-event count, "
            "or a non-small diffuse repair family would falsify this repair "
            "compression."),
        "novelty_label": "new-to-this-task",
        "arithmetic_modulus": adverse_payload["arithmetic_modulus"],
        "support": adverse_payload["support"],
        "dominant_modes": adverse_payload["dominant_modes"],
        "tail_threshold": adverse_payload["tail_threshold"],
        "volatile_labels": labels,
        "volatile_channel_count": len(labels),
        "selected_adverse_event_count": event_count,
        "selected_events_without_minimal_repair": repairless_count,
        "selected_minimal_repair_addition_count": repair_count,
        "selected_minimal_repair_addition_size_counts": {
            str(size): repair_size_counter[size]
            for size in sorted(repair_size_counter)
        },
        "selected_minimal_repair_channel_frequency": tuple({
            "label": label,
            "minimal_repair_addition_count": repair_counter[label],
        } for label in labels if repair_counter[label]),
        "hard_deficit_targets": hard_targets,
        "undo_repair_rows": undo_rows,
        "hard_undo_repair_rows": hard_rows,
        "summary": {
            "selected_fixture": (
                "all 26 adverse events have at least one minimal repair; "
                "50 of 52 minimal repairs are single-channel additions and "
                "the remaining two are three-channel additions"),
            "hard_rows": (
                "the three hard deficit rows have 22 adverse events, all "
                "with one-channel minimal repairs"),
            "target_13822": (
                "the adverse addition (1,5) is repaired by adding (4,4)"),
            "target_164598": (
                "the adverse pair (1,1),(1,3) is repaired by adding either "
                "(1,7) or (4,10)"),
            "target_1222142": (
                "the 20 adverse events each have two one-channel repairs; "
                "repair frequencies are (1,1):10, (2,4):10, (1,3):6, "
                "(4,10):6, (1,5):4, and (3,3):4"),
        },
        "interpretation": {
            "hole_status": (
                "The finite q286 hole is tighter but not closed: the named "
                "adverse additions are themselves repairable by small named "
                "channel sets on the selected fixture."),
            "route_status": (
                "Pure non-undo is demoted as a complete finite explanation; "
                "the live Boolean route is now an ordered clause/adverse/"
                "repair control problem."),
            "remaining_theorem": (
                "Prove that actual binary-prime residue weights enforce the "
                "right ordered adverse/repair balance, or replace the "
                "Boolean ledger with a full signed aggregate arithmetic-"
                "placement theorem."),
        },
        "volatile_undo_repair_channels_measured": True,
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
