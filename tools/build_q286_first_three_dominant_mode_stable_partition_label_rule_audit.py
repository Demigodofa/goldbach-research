"""Audit simple label rules for the q286 stable/volatile partition.

The named holdout kept the stable-core route alive.  This builder checks
whether the frozen stable-positive, stable-negative, and volatile channel sets
are explained by simple label geometry such as coordinate equality, parity,
thresholds, or rectangles.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIGN_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pairwise-swing-sign-stability.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-stable-partition-label-rule-audit.json")


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


def candidate_rules(labels):
    first_values = sorted({a for a, _ in labels})
    second_values = sorted({b for _, b in labels})
    rules = []

    def add(name, kind, selected):
        rules.append({
            "name": name,
            "kind": kind,
            "selected": frozenset(selected),
        })

    for value in first_values:
        add(f"first == {value}", "first_equality",
            (label for label in labels if label[0] == value))
    for value in second_values:
        add(f"second == {value}", "second_equality",
            (label for label in labels if label[1] == value))
    for value in first_values:
        add(f"first <= {value}", "first_threshold",
            (label for label in labels if label[0] <= value))
        add(f"first >= {value}", "first_threshold",
            (label for label in labels if label[0] >= value))
    for value in second_values:
        add(f"second <= {value}", "second_threshold",
            (label for label in labels if label[1] <= value))
        add(f"second >= {value}", "second_threshold",
            (label for label in labels if label[1] >= value))
    for parity in (0, 1):
        add(f"first % 2 == {parity}", "first_parity",
            (label for label in labels if label[0] % 2 == parity))
        add(f"second % 2 == {parity}", "second_parity",
            (label for label in labels if label[1] % 2 == parity))
    for modulus in (3, 4):
        for residue in range(modulus):
            add(f"first % {modulus} == {residue}", "first_mod",
                (label for label in labels if label[0] % modulus == residue))
            add(f"second % {modulus} == {residue}", "second_mod",
                (label for label in labels if label[1] % modulus == residue))
    for a0 in first_values:
        for a1 in first_values:
            if a0 > a1:
                continue
            for b0 in second_values:
                for b1 in second_values:
                    if b0 > b1:
                        continue
                    add(
                        f"{a0} <= first <= {a1} and {b0} <= second <= {b1}",
                        "rectangle",
                        (label for label in labels
                         if a0 <= label[0] <= a1
                         and b0 <= label[1] <= b1))
    return rules


def score_rule(rule, target, all_labels):
    selected = set(rule["selected"])
    target = set(target)
    true_positive = selected & target
    false_positive = selected - target
    false_negative = target - selected
    true_negative = set(all_labels) - selected - false_negative
    precision = (
        len(true_positive) / len(selected) if selected else math.nan)
    recall = (
        len(true_positive) / len(target) if target else math.nan)
    f1 = (
        2 * precision * recall / (precision + recall)
        if selected and target and precision + recall > 0 else 0.0)
    exact = bool(not false_positive and not false_negative)
    return {
        "name": rule["name"],
        "kind": rule["kind"],
        "selected_count": len(selected),
        "target_count": len(target),
        "true_positive_count": len(true_positive),
        "false_positive_count": len(false_positive),
        "false_negative_count": len(false_negative),
        "true_negative_count": len(true_negative),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "exact_match": exact,
        "selected_labels": tuple(sorted(selected)),
        "false_positive_labels": tuple(sorted(false_positive)),
        "false_negative_labels": tuple(sorted(false_negative)),
    }


def best_scores(rules, target, all_labels):
    scored = [score_rule(rule, target, all_labels) for rule in rules]
    scored.sort(key=lambda row: (
        row["exact_match"],
        row["f1"],
        -row["false_positive_count"],
        -row["false_negative_count"],
        -row["selected_count"],
        row["name"]), reverse=True)
    return scored


def main():
    source = json.loads(SIGN_SOURCE.read_text(encoding="utf-8"))
    all_labels = tuple(sorted(
        label_tuple(row["representative_label"])
        for row in source["channel_rows"]))
    classes = {
        "stable_positive": tuple(sorted(
            label_tuple(label)
            for label in source["stable_positive_labels"])),
        "stable_negative": tuple(sorted(
            label_tuple(label)
            for label in source["stable_negative_labels"])),
        "volatile": tuple(sorted(
            label_tuple(label)
            for label in source["sign_flip_labels"])),
    }
    rules = candidate_rules(all_labels)
    class_rows = {}
    exact_matches = {}
    for name, labels in classes.items():
        scored = best_scores(rules, labels, all_labels)
        class_rows[name] = {
            "target_labels": labels,
            "best_rules": tuple(scored[:10]),
        }
        exact_matches[name] = tuple(
            row for row in scored if row["exact_match"])

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_evidence": str(SIGN_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite label-rule audit only; no label-geometry theorem, "
            "stable-core theorem, volatile-rim theorem, pointwise "
            "character-sum estimate, or Goldbach proof is established"),
        "mechanism": (
            "Test whether the frozen q286 stable/volatile partition is "
            "explained by simple representative-label geometry."),
        "falsifier": (
            "If no tested coordinate, parity, threshold, modular, or "
            "rectangle rule exactly captures a partition class, then that "
            "simple label-geometry route is not enough for this fixture."),
        "all_labels": all_labels,
        "tested_rule_count": len(rules),
        "class_rows": class_rows,
        "exact_match_counts": {
            name: len(rows) for name, rows in exact_matches.items()
        },
        "any_exact_simple_rule": any(exact_matches.values()),
        "tested_rule_kinds": tuple(sorted({rule["kind"] for rule in rules})),
        "interpretation": {
            "simple_label_geometry": (
                "If exact_match_counts are zero, the stable/volatile classes "
                "are not explained by the tested simple label rules."),
            "remaining_theorem": (
                "A proof must use arithmetic action of the channel sums, a "
                "richer structured partition, or lower-support/complement "
                "rescue rather than only simple representative-label geometry."),
        },
        "stable_partition_label_rule_audit_measured": True,
        "simple_label_geometry_theorem_proved": False,
        "stable_core_theorem_proved": False,
        "volatile_rim_bound_proved": False,
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
