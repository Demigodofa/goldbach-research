"""Build q286 volatile boundary-cut graph evidence.

The undo-repair receipt is local to fragile clauses plus adverse additions.
This diagnostic enumerates every one-channel edge in the eight-channel
volatile Boolean cube and records the boundary cut between correct and
incorrect selected-row classifications.
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
REPAIR_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-undo-repair-channels.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-boundary-cut-graph.json")


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


def passes_floor(row, subset):
    return margin_to_floor(row, subset) >= 0.0


def correct_classification(row, subset):
    return passes_floor(row, subset) == bool(row["dominant_floor_passes"])


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
        record["passes_floor"] = passes_floor(row, subset)
        record["correct_classification"] = correct_classification(row, subset)
    return record


def channel_frequency(counter, labels):
    return tuple({
        "label": label,
        "boundary_edge_count": counter[label],
    } for label in labels if counter[label])


def boundary_row(target, row, labels, subsets):
    direction_counts = Counter()
    channel_by_direction = {
        "correct_to_wrong": Counter(),
        "wrong_to_correct": Counter(),
    }
    edges = []
    for subset in subsets:
        for label in labels:
            if label in subset:
                continue
            superset = subset | {label}
            source_correct = correct_classification(row, subset)
            dest_correct = correct_classification(row, superset)
            if source_correct == dest_correct:
                continue
            direction = (
                "correct_to_wrong"
                if source_correct and not dest_correct
                else "wrong_to_correct")
            direction_counts[direction] += 1
            channel_by_direction[direction][label] += 1
            edges.append({
                "direction": direction,
                "added_channel": label,
                "source": subset_record(subset, labels, row),
                "destination": subset_record(superset, labels, row),
                "absolute_destination_margin": abs(
                    margin_to_floor(row, superset)),
            })

    correct_count = sum(
        1 for subset in subsets if correct_classification(row, subset))
    nearest_edges = tuple(sorted(
        edges,
        key=lambda edge: (
            edge["absolute_destination_margin"],
            edge["direction"],
            edge["added_channel"],
            edge["source"]["subset_size"],
            edge["source"]["mask"]))[:12])
    return {
        "target": target,
        "target_mod_286": row["target_mod_286"],
        "dominant_floor_passes": bool(row["dominant_floor_passes"]),
        "correct_subset_count": correct_count,
        "wrong_subset_count": len(subsets) - correct_count,
        "boundary_edge_count": len(edges),
        "correct_to_wrong_edge_count": direction_counts["correct_to_wrong"],
        "wrong_to_correct_edge_count": direction_counts["wrong_to_correct"],
        "correct_to_wrong_channel_frequency": channel_frequency(
            channel_by_direction["correct_to_wrong"], labels),
        "wrong_to_correct_channel_frequency": channel_frequency(
            channel_by_direction["wrong_to_correct"], labels),
        "nearest_boundary_edges": nearest_edges,
    }


def aggregate_rows(rows, labels):
    counts = Counter()
    channel_counts = {
        "correct_to_wrong": Counter(),
        "wrong_to_correct": Counter(),
    }
    for row in rows:
        counts["targets"] += 1
        counts["correct_subset_count"] += row["correct_subset_count"]
        counts["wrong_subset_count"] += row["wrong_subset_count"]
        counts["boundary_edge_count"] += row["boundary_edge_count"]
        counts["correct_to_wrong_edge_count"] += row[
            "correct_to_wrong_edge_count"]
        counts["wrong_to_correct_edge_count"] += row[
            "wrong_to_correct_edge_count"]
        for item in row["correct_to_wrong_channel_frequency"]:
            channel_counts["correct_to_wrong"][label_tuple(item["label"])] += (
                item["boundary_edge_count"])
        for item in row["wrong_to_correct_channel_frequency"]:
            channel_counts["wrong_to_correct"][label_tuple(item["label"])] += (
                item["boundary_edge_count"])
    return {
        "target_count": counts["targets"],
        "correct_subset_count": counts["correct_subset_count"],
        "wrong_subset_count": counts["wrong_subset_count"],
        "boundary_edge_count": counts["boundary_edge_count"],
        "correct_to_wrong_edge_count": counts["correct_to_wrong_edge_count"],
        "wrong_to_correct_edge_count": counts["wrong_to_correct_edge_count"],
        "correct_to_wrong_channel_frequency": channel_frequency(
            channel_counts["correct_to_wrong"], labels),
        "wrong_to_correct_channel_frequency": channel_frequency(
            channel_counts["wrong_to_correct"], labels),
    }


def frequency_map(items):
    return {
        label_tuple(item["label"]): int(item["boundary_edge_count"])
        for item in items
    }


def main():
    subset_payload = json.loads(SUBSET_SOURCE.read_text(encoding="utf-8"))
    repair_payload = json.loads(REPAIR_SOURCE.read_text(encoding="utf-8"))
    labels = tuple(label_tuple(label) for label in subset_payload[
        "volatile_labels"])
    subsets = tuple(all_subsets(labels))
    target_rows = {
        int(target): row
        for target, row in subset_payload["target_rows"].items()
    }
    rows = tuple(
        boundary_row(target, row, labels, subsets)
        for target, row in sorted(target_rows.items()))
    by_target = {row["target"]: row for row in rows}
    hard_targets = tuple(repair_payload["hard_deficit_targets"])
    hard_rows = tuple(row for row in rows if row["target"] in hard_targets)
    deficit_rows = tuple(
        row for row in rows if not row["dominant_floor_passes"])
    clear_rows = tuple(row for row in rows if row["dominant_floor_passes"])

    if by_target[1222142]["correct_to_wrong_edge_count"] != 32:
        raise AssertionError("1222142 adverse boundary count changed")
    if frequency_map(by_target[1222142][
            "correct_to_wrong_channel_frequency"]) != {
                (1, 7): 16,
                (4, 4): 16,
            }:
        raise AssertionError("1222142 adverse boundary polarity changed")
    if frequency_map(by_target[1222142][
            "wrong_to_correct_channel_frequency"]) != {
                (1, 1): 16,
                (1, 3): 20,
                (1, 5): 22,
                (2, 4): 16,
                (3, 3): 22,
                (4, 10): 20,
            }:
        raise AssertionError("1222142 repair boundary polarity changed")
    if by_target[13822]["correct_to_wrong_edge_count"] != 1:
        raise AssertionError("13822 adverse boundary count changed")
    if by_target[164598]["correct_to_wrong_edge_count"] != 4:
        raise AssertionError("164598 adverse boundary count changed")
    if by_target[1240888]["boundary_edge_count"] != 0:
        raise AssertionError("1240888 should remain boundary-free")

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_subset_ablation": str(SUBSET_SOURCE.relative_to(ROOT)),
        "source_undo_repair_channels": str(REPAIR_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite volatile boundary-cut diagnostic only; no volatile-rim "
            "theorem, stable-core theorem, selected-fixture classifier "
            "theorem, pointwise character-sum estimate, or Goldbach proof is "
            "established"),
        "candidate": (
            "The clause/adverse/repair pattern may reflect a global polarity "
            "of the volatile Boolean boundary, not only local behavior near "
            "minimal clauses."),
        "mechanism": (
            "Enumerate every one-channel addition edge in the eight-channel "
            "volatile Boolean cube, keep edges that cross between correct and "
            "incorrect row classification, and count their channel labels by "
            "direction."),
        "prediction": (
            "If hard rows have concentrated boundary polarity, the theorem "
            "target can ask for signed channel placement across a small cut. "
            "If boundary roles are diffuse, the repair symmetry is local and "
            "the route should move toward a signed aggregate theorem."),
        "falsifier": (
            "A diffuse hard-row boundary or loss of the 1222142 two-adverse-"
            "channel polarity would falsify this cut-graph compression."),
        "novelty_label": "new-to-this-task",
        "arithmetic_modulus": subset_payload["arithmetic_modulus"],
        "support": subset_payload["support"],
        "dominant_modes": subset_payload["dominant_modes"],
        "tail_threshold": subset_payload["tail_threshold"],
        "volatile_labels": labels,
        "volatile_channel_count": len(labels),
        "subset_count": len(subsets),
        "single_addition_edge_count_per_target": len(labels) * 2 ** (
            len(labels) - 1),
        "selected_rows": rows,
        "deficit_rows": deficit_rows,
        "clear_rows": clear_rows,
        "hard_deficit_targets": hard_targets,
        "hard_rows": hard_rows,
        "aggregates": {
            "selected": aggregate_rows(rows, labels),
            "deficit": aggregate_rows(deficit_rows, labels),
            "clear": aggregate_rows(clear_rows, labels),
            "hard_deficit": aggregate_rows(hard_rows, labels),
        },
        "summary": {
            "target_1222142": (
                "Across the whole volatile cube, the only one-channel "
                "correct-to-wrong additions are (1,7) and (4,4), each with "
                "16 boundary edges; the six other volatile channels appear "
                "on the wrong-to-correct side."),
            "hard_deficit_rows": (
                "Hard rows have 37 correct-to-wrong boundary edges and 271 "
                "wrong-to-correct boundary edges."),
            "selected_deficit_rows": (
                "Selected deficit rows have 172 correct-to-wrong boundary "
                "edges and 424 wrong-to-correct boundary edges."),
            "selected_clear_rows": (
                "Selected clear rows have 191 correct-to-wrong boundary "
                "edges and 149 wrong-to-correct boundary edges; 1240888 is "
                "boundary-free because all volatile subsets classify it "
                "correctly."),
        },
        "interpretation": {
            "hole_status": (
                "The finite q286 hole tightens again: the hardest row's "
                "adverse side is globally two-channel in the volatile cube, "
                "while repair edges are spread over the complementary six "
                "channels."),
            "symmetry_status": (
                "The symmetry is real as a finite boundary polarity, but it "
                "is not a theorem until actual binary-prime residue weights "
                "are controlled uniformly."),
            "remaining_theorem": (
                "Prove the signed placement of actual prime-pair residue "
                "weights relative to this volatile boundary cut, or replace "
                "the Boolean cut picture with a full signed aggregate "
                "arithmetic-placement theorem."),
        },
        "volatile_boundary_cut_graph_measured": True,
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
