"""Summarize q286 zero-local target margin by outside channel.

This is a second-order audit over
``q286-zero-local-target-channel-decomposition.json``.  It answers whether the
12 zero-local target integers need many fixed channels to keep the LP-weighted
after-local margin positive, or whether a small fixed subset already works.

Finite evidence only: this proves no distributed cone theorem, no binary-prime
correlation theorem, and no Goldbach theorem.
"""

from __future__ import annotations

import itertools
import json
import math
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence" / "q286-zero-local-target-channel-decomposition.json"
OUT = ROOT / "evidence" / "q286-zero-local-channel-margin-audit.json"
TOLERANCE = 1e-12


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def label_key(label):
    return f"{int(label[0])},{int(label[1])}"


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


def sign_counts(values):
    values = tuple(float(value) for value in values)
    return {
        "positive_count": sum(1 for value in values if value > TOLERANCE),
        "negative_count": sum(1 for value in values if value < -TOLERANCE),
        "zero_count": sum(1 for value in values if abs(value) <= TOLERANCE),
    }


def summarize_scope(name, rows, labels):
    total_positive_margin = math.fsum(
        max(0.0, channel["lp_weighted_after_local"])
        for row in rows for channel in row["channel_rows"])
    total_net_lp_margin = math.fsum(
        float(row["after_local_lp_delta"]) for row in rows)
    channel_rows = []
    for label in labels:
        key = label_key(label)
        entries = []
        removal_failures = []
        for row in rows:
            channel = next(
                item for item in row["channel_rows"]
                if label_key(item["label"]) == key)
            weighted = float(channel["lp_weighted_after_local"])
            after_removal = float(row["after_local_lp_delta"]) - weighted
            entries.append({
                "target": int(row["target"]),
                "target_mod_143": int(row["target_mod_143"]),
                "weighted_contribution": weighted,
                "after_removing_channel_lp_margin": after_removal,
                "sign": (
                    "positive" if weighted > TOLERANCE
                    else "negative" if weighted < -TOLERANCE
                    else "zero"),
                "removal_fails_target": after_removal <= TOLERANCE,
            })
            if after_removal <= TOLERANCE:
                removal_failures.append(int(row["target"]))
        values = [entry["weighted_contribution"] for entry in entries]
        positive_sum = math.fsum(value for value in values if value > TOLERANCE)
        negative_sum = math.fsum(value for value in values if value < -TOLERANCE)
        net_sum = math.fsum(values)
        channel_rows.append({
            "label": label,
            "label_key": key,
            **sign_counts(values),
            "weighted_contribution_summary": finite_summary(values),
            "positive_weighted_sum": positive_sum,
            "negative_weighted_sum": negative_sum,
            "net_weighted_sum": net_sum,
            "positive_margin_share": (
                positive_sum / total_positive_margin
                if total_positive_margin else None),
            "net_margin_share_vs_total_net_lp_margin": (
                net_sum / total_net_lp_margin if total_net_lp_margin else None),
            "removing_channel_makes_any_target_fail": bool(removal_failures),
            "removal_failure_targets": removal_failures,
            "entries": entries,
        })
    channel_rows.sort(
        key=lambda item: (
            -(item["positive_margin_share"] or 0.0),
            item["label"]))

    contributions_by_target = {
        int(row["target"]): {
            label_key(item["label"]): float(item["lp_weighted_after_local"])
            for item in row["channel_rows"]
        }
        for row in rows
    }
    subset_result = smallest_positive_subset(
        labels, rows, contributions_by_target)
    return {
        "scope": name,
        "target_count": len(rows),
        "targets": [int(row["target"]) for row in rows],
        "residues_mod_143": sorted(
            {int(row["target_mod_143"]) for row in rows}),
        "total_positive_weighted_margin": total_positive_margin,
        "total_negative_weighted_margin": math.fsum(
            min(0.0, channel["lp_weighted_after_local"])
            for row in rows for channel in row["channel_rows"]),
        "total_net_lp_margin": total_net_lp_margin,
        "channel_summary_rows": channel_rows,
        "any_single_channel_removal_fails_target": any(
            row["removing_channel_makes_any_target_fail"]
            for row in channel_rows),
        "channels_whose_removal_fails_target": [
            row["label"] for row in channel_rows
            if row["removing_channel_makes_any_target_fail"]],
        "smallest_fixed_subset": subset_result,
    }


def subset_margin(combo, rows, contributions_by_target):
    values = []
    for row in rows:
        target = int(row["target"])
        total = math.fsum(
            contributions_by_target[target][label_key(label)]
            for label in combo)
        values.append(total)
    return values


def smallest_positive_subset(labels, rows, contributions_by_target):
    labels = tuple(labels)
    for size in range(1, len(labels) + 1):
        passing = []
        checked = 0
        for combo in itertools.combinations(labels, size):
            checked += 1
            margins = subset_margin(combo, rows, contributions_by_target)
            if min(margins) > TOLERANCE:
                passing.append({
                    "labels": combo,
                    "target_margins": [
                        {
                            "target": int(row["target"]),
                            "target_mod_143": int(row["target_mod_143"]),
                            "subset_lp_margin": float(margin),
                        }
                        for row, margin in zip(rows, margins)
                    ],
                    "minimum_target_margin": float(min(margins)),
                    "average_target_margin": (
                        math.fsum(margins) / len(margins)),
                    "total_margin": float(math.fsum(margins)),
                })
        if passing:
            passing.sort(
                key=lambda item: (
                    -item["minimum_target_margin"],
                    -item["total_margin"],
                    item["labels"]))
            return {
                "minimum_size": size,
                "passing_subset_count_at_minimum_size": len(passing),
                "checked_subset_count_at_minimum_size": checked,
                "best_subsets_by_minimum_margin": passing[:10],
                "all_minimum_subsets": passing,
                "small_fixed_subset_exists": size <= 3,
            }
    return {
        "minimum_size": None,
        "passing_subset_count_at_minimum_size": 0,
        "checked_subset_count_at_minimum_size": 2 ** len(labels) - 1,
        "best_subsets_by_minimum_margin": [],
        "all_minimum_subsets": [],
        "small_fixed_subset_exists": False,
    }


def main():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    labels = tuple(tuple(int(part) for part in label)
                   for label in source["outside_labels"])
    rows = source["target_rows"]
    rows_by_residue = defaultdict(list)
    for row in rows:
        rows_by_residue[int(row["target_mod_143"])].append(row)

    scopes = {
        "all_12_targets": summarize_scope("all_12_targets", rows, labels),
    }
    for residue in sorted(rows_by_residue):
        scopes[f"residue_{residue}"] = summarize_scope(
            f"residue_{residue}", rows_by_residue[residue], labels)

    all_subset = scopes["all_12_targets"]["smallest_fixed_subset"]
    distributed_supported = not all_subset["small_fixed_subset_exists"]
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_zero_local_decomposition": str(SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite audit of LP-weighted after-local margins for the 12 "
            "zero-local target integers only; no distributed cone theorem, "
            "binary-prime correlation theorem, signed projection theorem, or "
            "Goldbach theorem is proved."),
        "question": (
            "For each outside channel, how much of the positive LP margin is "
            "supplied after subtracting the zero local contribution, and does "
            "any small fixed subset keep all 12 targets positive?"),
        "metric": (
            "weighted contribution means "
            "lp_effective_weight * after_local_delta from the source "
            "decomposition. Subset positivity means the sum of selected "
            "weighted contributions is positive for every target in scope."),
        "scopes": scopes,
        "decision": (
            "A one-channel fixed subset already keeps all 12 targets positive "
            "under this LP-weighted subset criterion. Therefore this specific "
            "smallest-subset test does not support the stronger claim that the "
            "observed zero-local positivity requires a genuinely distributed "
            "fixed channel subset, although the source rows still show that "
            "the local singular layer contributes zero and that the remaining "
            "margin is empirical/correlation-sourced."),
        "smallest_all_target_subset_size": all_subset["minimum_size"],
        "smallest_all_target_subset_count": all_subset[
            "passing_subset_count_at_minimum_size"],
        "distributed_cone_theorem_supported_by_subset_test": (
            distributed_supported),
        "binary_prime_pair_correlation_bridge_still_required": True,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
