"""Build q286 volatile minimal-clause structure evidence.

The forced-channel attribution decomposes the full volatile rim into hard-row
obligations.  This derivative receipt extracts the inclusion-minimal volatile
subsets satisfying each selected deficit-row threshold, giving an exact finite
clause structure for the current proof target.
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
ATTRIBUTION_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-forced-channel-attribution.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-minimal-clause-structure.json")


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
        record["volatile_subset_sum"] = subset_sum(row, subset)
        record["margin_to_floor"] = margin_to_floor(row, subset)
        record["slack_for_deficit_classification"] = -record[
            "margin_to_floor"]
    return record


def channel_frequency(subsets, labels):
    total = len(subsets)
    return tuple({
        "label": label,
        "minimal_clause_count": sum(
            1 for subset in subsets if label in subset),
        "frequency": (
            sum(1 for subset in subsets if label in subset) / total
            if total else None),
    } for label in labels)


def inclusion_minimal(subsets):
    return tuple(sorted(
        (
            subset for subset in subsets
            if not any(other < subset for other in subsets)
        ),
        key=lambda subset: (len(subset), sorted(subset))))


def selected_deficit_clause(row, labels, stored, all_subsets_list):
    satisfying = tuple(
        subset for subset in all_subsets_list if satisfies_row(row, subset))
    if len(satisfying) != stored["satisfying_subset_count"]:
        raise AssertionError(
            f"satisfying-subset count mismatch for {row['target']}")
    minimal = inclusion_minimal(satisfying)
    minimum_size = min(len(subset) for subset in satisfying)
    if minimum_size != stored["minimum_satisfying_subset_size"]:
        raise AssertionError(
            f"minimum satisfying size mismatch for {row['target']}")
    if min(len(subset) for subset in minimal) != minimum_size:
        raise AssertionError(
            f"minimal clause size mismatch for {row['target']}")
    necessary = (
        set.intersection(*map(set, satisfying)) if satisfying else set())
    stored_necessary = {
        label_tuple(label)
        for label in stored[
            "necessary_channels_across_row_satisfying_subsets"]
    }
    if necessary != stored_necessary:
        raise AssertionError(
            f"necessary-channel mismatch for {row['target']}")
    common_minimal_core = (
        set.intersection(*map(set, minimal)) if minimal else set())
    return {
        "target": row["target"],
        "target_mod_286": row["target_mod_286"],
        "stable_core_margin_to_floor": (
            row["stable_core_sum_to_principal"] + .3),
        "full_volatile_sum_to_principal": row[
            "full_volatile_sum_to_principal"],
        "full_margin_to_floor": margin_to_floor(row, frozenset(labels)),
        "satisfying_subset_count": len(satisfying),
        "minimum_satisfying_subset_size": minimum_size,
        "inclusion_minimal_clause_count": len(minimal),
        "inclusion_minimal_size_counts": {
            str(size): sum(1 for subset in minimal if len(subset) == size)
            for size in range(len(labels) + 1)
            if any(len(subset) == size for subset in minimal)
        },
        "necessary_channels_across_all_satisfying_subsets": tuple(
            sorted(necessary)),
        "common_core_across_minimal_clauses": tuple(
            sorted(common_minimal_core)),
        "minimal_clauses": tuple(
            subset_record(subset, labels, row) for subset in minimal),
        "channel_frequency_in_minimal_clauses": channel_frequency(
            minimal, labels),
    }


def main():
    subset_payload = json.loads(SUBSET_SOURCE.read_text(encoding="utf-8"))
    threshold_payload = json.loads(
        THRESHOLD_SOURCE.read_text(encoding="utf-8"))
    attribution_payload = json.loads(
        ATTRIBUTION_SOURCE.read_text(encoding="utf-8"))
    labels = tuple(label_tuple(label) for label in subset_payload[
        "volatile_labels"])
    target_rows = {
        int(target): row
        for target, row in subset_payload["target_rows"].items()
    }
    threshold_by_target = {
        int(row["target"]): row
        for row in threshold_payload["row_thresholds"]
    }
    all_subsets_list = tuple(all_subsets(labels))

    deficit_targets = tuple(sorted(
        target for target, row in target_rows.items()
        if not row["dominant_floor_passes"]))
    hard_targets = tuple(attribution_payload["hard_deficit_targets"])
    if hard_targets != (13822, 1222142, 164598):
        raise AssertionError(f"unexpected hard targets: {hard_targets}")

    deficit_clauses = tuple(
        selected_deficit_clause(
            target_rows[target],
            labels,
            threshold_by_target[target],
            all_subsets_list)
        for target in deficit_targets)
    hard_clauses = tuple(
        clause for clause in deficit_clauses
        if clause["target"] in hard_targets)

    clause_by_target = {
        clause["target"]: clause for clause in deficit_clauses
    }
    if clause_by_target[13822]["inclusion_minimal_clause_count"] != 2:
        raise AssertionError("13822 no longer has two minimal clauses")
    if clause_by_target[164598]["inclusion_minimal_clause_count"] != 2:
        raise AssertionError("164598 no longer has two minimal clauses")
    if clause_by_target[1222142]["inclusion_minimal_clause_count"] != 10:
        raise AssertionError("1222142 no longer has ten minimal clauses")
    if clause_by_target[1222142][
            "necessary_channels_across_all_satisfying_subsets"]:
        raise AssertionError("1222142 unexpectedly has necessary channels")

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_subset_ablation": str(SUBSET_SOURCE.relative_to(ROOT)),
        "source_row_thresholds": str(THRESHOLD_SOURCE.relative_to(ROOT)),
        "source_forced_channel_attribution": str(
            ATTRIBUTION_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite volatile minimal-clause structure only; no volatile-rim "
            "theorem, stable-core theorem, selected-fixture classifier "
            "theorem, pointwise character-sum estimate, or Goldbach proof is "
            "established"),
        "candidate": (
            "The row-specific volatile threshold obligations may have a "
            "small exact clause structure useful for theorem shaping."),
        "mechanism": (
            "Enumerate all volatile subsets and keep only inclusion-minimal "
            "satisfying subsets for each selected deficit row."),
        "prediction": (
            "Hard rows with few minimal clauses provide compact arithmetic "
            "targets; a hard row with no necessary channel requires a "
            "disjunctive or aggregate treatment."),
        "falsifier": (
            "A mismatch with the stored row-threshold satisfying counts, "
            "minimum sizes, or necessary-channel sets falsifies this clause "
            "extraction."),
        "novelty_label": "new-to-this-task",
        "arithmetic_modulus": threshold_payload["arithmetic_modulus"],
        "support": threshold_payload["support"],
        "dominant_modes": threshold_payload["dominant_modes"],
        "tail_threshold": threshold_payload["tail_threshold"],
        "volatile_labels": labels,
        "volatile_channel_count": len(labels),
        "tested_subset_count": len(all_subsets_list),
        "deficit_targets": deficit_targets,
        "hard_deficit_targets": hard_targets,
        "deficit_clause_rows": deficit_clauses,
        "hard_clause_rows": hard_clauses,
        "hard_clause_summary": {
            "target_13822": (
                "two six-channel clauses: common five-channel core plus "
                "either (4,4) or (4,10)"),
            "target_164598": (
                "two three-channel clauses: common (1,5),(4,4) core plus "
                "either (1,7) or (2,4)"),
            "target_1222142": (
                "ten four-channel clauses and no individually necessary "
                "volatile channel"),
        },
        "interpretation": {
            "compact_hard_rows": (
                "Rows 13822 and 164598 have compact DNF-like threshold "
                "targets with two minimal clauses each."),
            "disjunctive_hard_row": (
                "Row 1222142 cannot be reduced to an individually necessary "
                "channel on this fixture; it requires one of ten four-channel "
                "clauses or an aggregate replacement."),
            "remaining_theorem": (
                "The next proof route can target these exact clause families "
                "from binary-prime residue arithmetic, explain why the "
                "1222142 clauses are forced in the combined setting, or "
                "replace the clause view with a stronger signed aggregate "
                "theorem."),
        },
        "volatile_minimal_clause_structure_measured": True,
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
