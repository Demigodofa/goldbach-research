"""Build q286 volatile adverse-absorption ladder evidence.

The critical-dependency audit showed that target 1222142 needs all six repair
channels when both adverse channels are present.  This receipt asks where that
requirement turns on: base-only, either single adverse channel, or the full
adverse pair.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAGNITUDE_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-polarity-magnitude-ledger.json")
DEPENDENCY_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-critical-dependency-audit.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-adverse-absorption-ladder.json")
TOL = 1e-12


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


def contribution_map(row):
    return {
        label_tuple(item["label"]): float(item["contribution_to_principal"])
        for item in row["volatile_channel_contributions"]
    }


def strict_exceeds(total, threshold):
    return total > threshold + TOL


def bundle_record(labels, magnitudes, indexes, threshold):
    chosen = tuple(labels[index] for index in indexes)
    total = sum(magnitudes[label] for label in chosen)
    return {
        "labels": chosen,
        "size": len(chosen),
        "magnitude": total,
        "threshold": threshold,
        "slack_over_threshold": total - threshold,
    }


def sufficient_bundles(labels, magnitudes, threshold):
    records = []
    for size in range(len(labels) + 1):
        for indexes in combinations(range(len(labels)), size):
            record = bundle_record(labels, magnitudes, indexes, threshold)
            if strict_exceeds(record["magnitude"], threshold):
                records.append(record)
    return tuple(records)


def is_proper_subset(left, right):
    return set(left["labels"]) < set(right["labels"])


def minimal_bundles(labels, magnitudes, threshold):
    sufficient = sufficient_bundles(labels, magnitudes, threshold)
    minimal = tuple(
        record for record in sufficient
        if not any(is_proper_subset(other, record) for other in sufficient))
    return tuple(sorted(
        minimal,
        key=lambda item: (
            item["size"],
            item["slack_over_threshold"],
            item["labels"])))


def best_insufficient_bundle(labels, magnitudes, threshold):
    best = None
    for size in range(len(labels) + 1):
        for indexes in combinations(range(len(labels)), size):
            record = bundle_record(labels, magnitudes, indexes, threshold)
            if strict_exceeds(record["magnitude"], threshold):
                continue
            if best is None or record["magnitude"] > best["magnitude"]:
                best = record
    return best


def row_threshold(row, adverse_magnitude):
    base = float(row["base_margin_without_volatile"])
    if row["dominant_floor_passes"]:
        return -base + adverse_magnitude
    return base + adverse_magnitude


def step_record(row, repair_labels, adverse_subset, magnitudes):
    adverse_magnitude = sum(magnitudes[label] for label in adverse_subset)
    threshold = row_threshold(row, adverse_magnitude)
    minimal = minimal_bundles(repair_labels, magnitudes, threshold)
    best_near_miss = best_insufficient_bundle(
        repair_labels, magnitudes, threshold)
    if minimal:
        minimum_size = min(bundle["size"] for bundle in minimal)
        maximum_size = max(bundle["size"] for bundle in minimal)
        full_bundle_unique = (
            len(minimal) == 1
            and set(minimal[0]["labels"]) == set(repair_labels))
    else:
        minimum_size = None
        maximum_size = None
        full_bundle_unique = False
    return {
        "adverse_subset": adverse_subset,
        "adverse_subset_size": len(adverse_subset),
        "adverse_magnitude": adverse_magnitude,
        "repair_threshold": threshold,
        "minimal_sufficient_repair_bundles": minimal,
        "minimal_sufficient_repair_bundle_count": len(minimal),
        "minimum_repair_bundle_size": minimum_size,
        "maximum_repair_bundle_size": maximum_size,
        "full_repair_bundle_is_unique": full_bundle_unique,
        "proper_repair_bundle_exists": (
            minimum_size is not None and minimum_size < len(repair_labels)),
        "best_insufficient_repair_bundle": best_near_miss,
    }


def row_ladder(row):
    contributions = contribution_map(row)
    magnitudes = {
        label: abs(contribution)
        for label, contribution in contributions.items()
    }
    repair_labels = tuple(
        label_tuple(label) for label in row["sign_expected_repair_channels"])
    adverse_labels = tuple(
        label_tuple(label) for label in row["sign_expected_adverse_channels"])
    steps = []
    for size in range(len(adverse_labels) + 1):
        for adverse_subset in combinations(adverse_labels, size):
            steps.append(
                step_record(row, repair_labels, adverse_subset, magnitudes))
    minimum_sizes = tuple(
        step["minimum_repair_bundle_size"] for step in steps)
    first_full_forced = next(
        (step for step in steps if step["full_repair_bundle_is_unique"]),
        None)
    return {
        "target": row["target"],
        "target_mod_286": row["target_mod_286"],
        "dominant_floor_passes": row["dominant_floor_passes"],
        "base_margin_without_volatile": row["base_margin_without_volatile"],
        "repair_magnitude": row["repair_magnitude"],
        "required_repair_magnitude": row["required_repair_magnitude"],
        "signed_magnitude_surplus": row["signed_magnitude_surplus"],
        "adverse_magnitude": row["adverse_magnitude"],
        "repair_to_required_ratio": row["repair_to_required_ratio"],
        "repair_labels": repair_labels,
        "adverse_labels": adverse_labels,
        "repair_channel_count": len(repair_labels),
        "adverse_channel_count": len(adverse_labels),
        "ladder_steps": tuple(steps),
        "minimum_repair_bundle_sizes_by_adverse_step": minimum_sizes,
        "first_full_repair_forced_step": first_full_forced,
    }


def aggregate(rows):
    counts = Counter()
    for row in rows:
        counts["target_count"] += 1
        counts["ladder_step_count"] += len(row["ladder_steps"])
        counts["full_repair_forced_step_count"] += sum(
            1 for step in row["ladder_steps"]
            if step["full_repair_bundle_is_unique"])
        counts["proper_repair_step_count"] += sum(
            1 for step in row["ladder_steps"]
            if step["proper_repair_bundle_exists"])
        counts["minimal_repair_bundle_count"] += sum(
            step["minimal_sufficient_repair_bundle_count"]
            for step in row["ladder_steps"])
    return dict(counts)


def dependency_row_by_target(payload):
    return {int(row["target"]): row for row in payload["rows"]}


def main():
    magnitude_payload = json.loads(
        MAGNITUDE_SOURCE.read_text(encoding="utf-8"))
    dependency_payload = json.loads(
        DEPENDENCY_SOURCE.read_text(encoding="utf-8"))
    rows = tuple(row_ladder(row) for row in magnitude_payload["rows"])
    by_target = {row["target"]: row for row in rows}
    dependency_by_target = dependency_row_by_target(dependency_payload)

    stress = by_target[1222142]
    stress_steps = {
        tuple(step["adverse_subset"]): step
        for step in stress["ladder_steps"]
    }
    expected_stress_min_sizes = (4, 5, 5, 6)
    if stress["minimum_repair_bundle_sizes_by_adverse_step"] != (
            expected_stress_min_sizes):
        raise AssertionError("1222142 adverse ladder sizes changed")
    full_adverse = tuple(stress["adverse_labels"])
    if not stress_steps[full_adverse]["full_repair_bundle_is_unique"]:
        raise AssertionError("1222142 full adverse step no longer forces all")
    if stress_steps[()]["minimum_repair_bundle_size"] != 4:
        raise AssertionError("1222142 base-only step changed")
    for singleton in ((1, 7), (4, 4)):
        if stress_steps[(singleton,)]["minimum_repair_bundle_size"] != 5:
            raise AssertionError("1222142 singleton adverse step changed")
    if not dependency_by_target[1222142][
            "repair_bundle_summary"]["full_bundle_is_unique"]:
        raise AssertionError("dependency audit drifted for 1222142")

    hard_targets = tuple(magnitude_payload["hard_deficit_targets"])
    hard_rows = tuple(row for row in rows if row["target"] in hard_targets)
    deficit_rows = tuple(
        row for row in rows if not row["dominant_floor_passes"])
    clear_rows = tuple(row for row in rows if row["dominant_floor_passes"])

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_polarity_magnitude_ledger": str(
            MAGNITUDE_SOURCE.relative_to(ROOT)),
        "source_critical_dependency_audit": str(
            DEPENDENCY_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite volatile adverse-absorption ladder only; no "
            "volatile-rim theorem, stable-core theorem, selected-fixture "
            "classifier theorem, pointwise character-sum estimate, or "
            "Goldbach proof is established"),
        "candidate": (
            "The six-channel repair requirement at 1222142 may turn on only "
            "after the two adverse channels are absorbed together, rather "
            "than being forced by the base margin or by either singleton "
            "adverse channel alone."),
        "mechanism": (
            "For each row, enumerate the adverse-channel subsets and compute "
            "the required repair threshold after absorbing that adverse "
            "magnitude.  Then enumerate the inclusion-minimal repair bundles "
            "that beat the threshold at each adverse step."),
        "prediction": (
            "If the critical balance has internal ladder structure, "
            "1222142 should show a rising minimum repair-bundle size from "
            "base-only to singleton-adverse to full-adverse steps."),
        "falsifier": (
            "If 1222142 needs the full six-channel repair bundle before both "
            "adverse channels are present, or if a proper repair bundle "
            "survives the full adverse pair, this adverse-absorption ladder "
            "does not explain where the all-critical dependency turns on."),
        "novelty_label": "new-to-this-task",
        "arithmetic_modulus": magnitude_payload["arithmetic_modulus"],
        "support": magnitude_payload["support"],
        "dominant_modes": magnitude_payload["dominant_modes"],
        "tail_threshold": magnitude_payload["tail_threshold"],
        "volatile_labels": magnitude_payload["volatile_labels"],
        "volatile_channel_count": magnitude_payload["volatile_channel_count"],
        "rows": rows,
        "hard_deficit_targets": hard_targets,
        "hard_rows": hard_rows,
        "aggregates": {
            "selected": aggregate(rows),
            "deficit": aggregate(deficit_rows),
            "clear": aggregate(clear_rows),
            "hard_deficit": aggregate(hard_rows),
        },
        "summary": {
            "target_1222142": (
                "The minimum sufficient repair-bundle sizes are 4 with no "
                "adverse channel, 5 with either singleton adverse channel, "
                "and 6 only when both adverse channels (1,7) and (4,4) are "
                "absorbed together."),
            "where_full_dependency_turns_on": (
                "For 1222142, the full six-channel repair bundle is forced "
                "exactly at the full adverse-pair step, not at base-only or "
                "singleton-adverse steps."),
            "nearest_full_step_margin": (
                "The full adverse-pair step has signed surplus about "
                "0.0088331796; the nearest five-channel repair near miss "
                "falls short by about 0.0021056957."),
        },
        "interpretation": {
            "hole_status": (
                "The q286 stress-row hole has a finite adverse-absorption "
                "ladder: the two adverse channels jointly raise the repair "
                "requirement from four to five to all six repair channels."),
            "route_status": (
                "A local theorem can target the full adverse-pair absorption "
                "step directly, rather than treating all six repair channels "
                "as equally forced at every lower threshold."),
            "remaining_theorem": (
                "Prove the adverse-pair absorption ladder from actual "
                "binary-prime residue weights uniformly, or replace this "
                "local ladder with a signed aggregate arithmetic-placement "
                "theorem."),
        },
        "volatile_adverse_absorption_ladder_measured": True,
        "full_repair_for_1222142_forced_before_full_adverse_pair": False,
        "repair_compression_for_1222142_full_adverse_pair_found": False,
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
