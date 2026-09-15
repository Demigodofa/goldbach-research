"""Search for independent descriptors of the q286 low-(3,1) broad pocket.

The scalar-selected broad low-33 and strict low-24 reference groups pass the
fresh centered-(3,1) target test, but they are chosen by the scalar being
tested.  This receipt asks whether a small independent descriptor built from
q286 filter/correlation features or CRT residue data can explain the same
groups without using centered (3,1).

Finite evidence only: descriptor searches here are diagnostics.  They prove no
stress theorem, signed correlation theorem, pointwise character-sum theorem, or
Goldbach theorem.
"""

from __future__ import annotations

import itertools
import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-low-3-1-independent-descriptor-audit.json"

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_filter_order_audit_receipt,
)

PREDICATE_NAMES = (
    "first_two_active",
    "first_three_tail",
    "complement_positive",
    "complement_floor",
)
CONTINUOUS_FEATURES = (
    "first_two_modes_to_principal_ratio",
    "first_three_modes_to_principal_ratio",
    "complement_to_principal_ratio",
    "full_action_to_principal_ratio",
)
ROUND_THRESHOLDS = {
    "first_two_modes_to_principal_ratio": (-0.8, -0.7, -0.6, -0.5, -0.4,
                                           -0.3),
    "first_three_modes_to_principal_ratio": (-1.0, -0.9, -0.8, -0.7, -0.6,
                                             -0.5, -0.4, -0.3),
    "complement_to_principal_ratio": (0.3, 0.4, 0.5, 0.6, 0.7, 0.8),
    "full_action_to_principal_ratio": (-0.20, -0.15, -0.10, -0.075, -0.05,
                                       -0.025, 0.0),
}
TARGET_LABELS = (
    "low_centered_3_1_selected_max_threshold",
    "low_centered_3_1_selected_min_threshold",
)
THRESHOLD_SOURCE = (
    EVIDENCE / "q286-centered-3-1-threshold-subclass-audit.json")
TRAIN_CYCLES = (0, 1, 2, 3)
HOLDOUT_CYCLES = (4, 5, 6, 7)
MIN_SUPPORT = 5


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def refs_for_threshold(threshold_payload, name):
    return set(
        int(target)
        for target in next(
            row for row in threshold_payload["threshold_subclasses"]
            if row["name"] == name)["references"])


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


def legendre_symbol(n, p):
    n %= p
    if n == 0:
        return 0
    value = pow(n, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def broad_rows(threshold_payload):
    low_refs = refs_for_threshold(
        threshold_payload,
        "broad_full_nonpositive_at_or_below_selected_max")
    strict_low_refs = refs_for_threshold(
        threshold_payload,
        "broad_full_nonpositive_at_or_below_selected_min")
    baseline = q286_first_three_filter_order_audit_receipt(
        start=10000,
        cycle_count=8,
        targets_per_cycle=5005,
        tail_threshold=.3,
        complement_floor=.3)
    rows = []
    for target, row in baseline["target_rows"].items():
        target = int(target)
        predicates = set(row["passed_predicates"])
        if "full_nonpositive" not in predicates:
            continue
        rows.append({
            "target": target,
            "cycle": int(row["cycle"]),
            "target_mod_11": target % 11,
            "target_mod_13": target % 13,
            "target_mod_22": target % 22,
            "target_mod_26": target % 26,
            "target_mod_143": target % 143,
            "target_mod_286": target % 286,
            "legendre_11": legendre_symbol(target, 11),
            "legendre_13": legendre_symbol(target, 13),
            "legendre_product_11_13": (
                legendre_symbol(target, 11)
                * legendre_symbol(target, 13)),
            "passed_predicates": sorted(predicates),
            "first_two_modes_to_principal_ratio": float(
                row["first_two_modes_to_principal_ratio"]),
            "first_three_modes_to_principal_ratio": float(
                row["first_three_modes_to_principal_ratio"]),
            "complement_to_principal_ratio": float(
                row["complement_to_principal_ratio"]),
            "full_action_to_principal_ratio": float(
                row["full_action_to_principal_ratio"]),
            "low_centered_3_1_selected_max_threshold": target in low_refs,
            "low_centered_3_1_selected_min_threshold":
                target in strict_low_refs,
        })
    return sorted(rows, key=lambda row: (row["cycle"], row["target"]))


def make_atom(name, family, predeclared, predicate, description):
    return {
        "name": name,
        "family": family,
        "predeclared_without_centered_3_1": predeclared,
        "description": description,
        "predicate": predicate,
    }


def build_atoms(rows):
    atoms = []
    for predicate in PREDICATE_NAMES:
        atoms.append(make_atom(
            f"predicate:{predicate}",
            "filter_predicate",
            True,
            lambda row, predicate=predicate: predicate in row[
                "passed_predicates"],
            f"source filter predicate {predicate}"))

    for modulus in (11, 13, 22, 26):
        residues = sorted({row[f"target_mod_{modulus}"] for row in rows})
        for residue in residues:
            atoms.append(make_atom(
                f"target_mod_{modulus}=={residue}",
                f"crt_residue_mod_{modulus}",
                True,
                lambda row, modulus=modulus, residue=residue:
                    row[f"target_mod_{modulus}"] == residue,
                f"target residue {residue} modulo {modulus}"))

    for key in ("legendre_11", "legendre_13", "legendre_product_11_13"):
        for value in (-1, 0, 1):
            atoms.append(make_atom(
                f"{key}=={value}",
                "quadratic_character_sign",
                True,
                lambda row, key=key, value=value: row[key] == value,
                f"{key} equals {value}"))

    for feature, thresholds in ROUND_THRESHOLDS.items():
        for threshold in thresholds:
            atoms.append(make_atom(
                f"{feature}<={threshold:g}",
                "round_numeric_filter_threshold",
                True,
                lambda row, feature=feature, threshold=threshold:
                    row[feature] <= threshold,
                f"{feature} at or below round threshold {threshold:g}"))
            atoms.append(make_atom(
                f"{feature}>={threshold:g}",
                "round_numeric_filter_threshold",
                True,
                lambda row, feature=feature, threshold=threshold:
                    row[feature] >= threshold,
                f"{feature} at or above round threshold {threshold:g}"))

    residue_counts = {}
    for row in rows:
        residue_counts[row["target_mod_143"]] = (
            residue_counts.get(row["target_mod_143"], 0) + 1)
    for residue, count in sorted(residue_counts.items()):
        if count >= 2:
            atoms.append(make_atom(
                f"target_mod_143=={residue}",
                "exploratory_exact_residue_mod_143",
                False,
                lambda row, residue=residue:
                    row["target_mod_143"] == residue,
                f"exact residue {residue} modulo 143; support {count}"))
    return atoms


def selected_rows(rows, descriptor):
    predicates = descriptor["predicates"]
    return [
        row for row in rows
        if all(predicate(row) for predicate in predicates)
    ]


def evaluate_descriptor(descriptor, rows, target_label):
    selected = selected_rows(rows, descriptor)
    low = [row for row in selected if row[target_label]]
    above = [row for row in selected if not row[target_label]]
    total_low = sum(1 for row in rows if row[target_label])
    precision = len(low) / len(selected) if selected else None
    recall = len(low) / total_low if total_low else None
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision is not None and recall is not None
        and precision + recall else 0.0)
    return {
        "descriptor": descriptor["name"],
        "families": descriptor["families"],
        "predeclared_without_centered_3_1":
            descriptor["predeclared_without_centered_3_1"],
        "target_label": target_label,
        "reference_count": len(selected),
        "low_count": len(low),
        "above_threshold_count": len(above),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "passes_zero_failure_gate": bool(selected and not above),
        "references": [row["target"] for row in selected],
        "feature_summaries": {
            feature: finite_summary(row[feature] for row in selected)
            for feature in CONTINUOUS_FEATURES
        },
    }


def descriptor_from_atoms(atoms):
    return {
        "name": " AND ".join(atom["name"] for atom in atoms),
        "families": sorted({atom["family"] for atom in atoms}),
        "predeclared_without_centered_3_1": all(
            atom["predeclared_without_centered_3_1"] for atom in atoms),
        "predicates": tuple(atom["predicate"] for atom in atoms),
        "descriptions": [atom["description"] for atom in atoms],
    }


def descriptor_search(rows, atoms, target_label, max_size=2):
    results = []
    for size in range(1, max_size + 1):
        for combo in itertools.combinations(atoms, size):
            descriptor = descriptor_from_atoms(combo)
            result = evaluate_descriptor(descriptor, rows, target_label)
            if result["reference_count"] >= MIN_SUPPORT:
                result["atom_count"] = size
                result["descriptions"] = descriptor["descriptions"]
                results.append(result)
    return results


def best_results(results, predeclared=None, limit=20):
    filtered = list(results)
    if predeclared is not None:
        filtered = [
            row for row in filtered
            if row["predeclared_without_centered_3_1"] is predeclared]
    return sorted(
        filtered,
        key=lambda row: (
            row["passes_zero_failure_gate"],
            row["precision"] or 0.0,
            row["recall"] or 0.0,
            row["reference_count"]),
        reverse=True)[:limit]


def generalization_rows(descriptors, train_rows, holdout_rows, target_label):
    out = []
    for descriptor in descriptors:
        train = evaluate_descriptor(descriptor, train_rows, target_label)
        if (train["reference_count"] < 2
                or not train["passes_zero_failure_gate"]):
            continue
        holdout = evaluate_descriptor(descriptor, holdout_rows, target_label)
        out.append({
            "descriptor": descriptor["name"],
            "families": descriptor["families"],
            "predeclared_without_centered_3_1":
                descriptor["predeclared_without_centered_3_1"],
            "target_label": target_label,
            "train": train,
            "holdout": holdout,
            "holdout_passes_zero_failure_gate": (
                holdout["passes_zero_failure_gate"]),
            "holdout_nonempty": holdout["reference_count"] > 0,
        })
    return sorted(
        out,
        key=lambda row: (
            row["holdout_passes_zero_failure_gate"],
            row["holdout_nonempty"],
            row["holdout"]["recall"] or 0.0,
            row["train"]["recall"] or 0.0,
            row["train"]["reference_count"]),
        reverse=True)[:40]


def cycle_counts(rows):
    out = {}
    for row in rows:
        cycle = row["cycle"]
        if cycle not in out:
            out[cycle] = {
                "cycle": cycle,
                "reference_count": 0,
                "low_33_count": 0,
                "strict_low_24_count": 0,
            }
        out[cycle]["reference_count"] += 1
        out[cycle]["low_33_count"] += int(
            row["low_centered_3_1_selected_max_threshold"])
        out[cycle]["strict_low_24_count"] += int(
            row["low_centered_3_1_selected_min_threshold"])
    return [out[key] for key in sorted(out)]


def zero_failure_rows(results):
    return [row for row in results if row["passes_zero_failure_gate"]]


def holdout_supported_zero_count(results, rows):
    count = 0
    rows_by_target = {row["target"]: row for row in rows}
    for result in zero_failure_rows(results):
        if any(
                rows_by_target[target]["cycle"] in HOLDOUT_CYCLES
                for target in result["references"]):
            count += 1
    return count


def main():
    threshold_payload = load_json(THRESHOLD_SOURCE)
    rows = broad_rows(threshold_payload)
    atoms = build_atoms(rows)
    train_rows = [row for row in rows if row["cycle"] in TRAIN_CYCLES]
    holdout_rows = [row for row in rows if row["cycle"] in HOLDOUT_CYCLES]
    predeclared_atoms = [
        atom for atom in atoms if atom["predeclared_without_centered_3_1"]]

    all_results = {}
    predeclared_results = {}
    generalization = {}
    for label in TARGET_LABELS:
        results = descriptor_search(rows, atoms, label, max_size=2)
        pre_results = descriptor_search(
            rows, predeclared_atoms, label, max_size=2)
        descriptors = [
            descriptor_from_atoms(combo)
            for size in (1, 2)
            for combo in itertools.combinations(atoms, size)
        ]
        pre_descriptors = [
            descriptor for descriptor in descriptors
            if descriptor["predeclared_without_centered_3_1"]]
        all_results[label] = {
            "best_overall": best_results(results, None),
            "best_predeclared": best_results(pre_results, True),
            "zero_failure_overall": sorted(
                [row for row in results
                 if row["passes_zero_failure_gate"]],
                key=lambda row: (
                    -row["reference_count"], row["atom_count"],
                    row["descriptor"]))[:20],
            "zero_failure_predeclared": sorted(
                [row for row in pre_results
                 if row["passes_zero_failure_gate"]],
                key=lambda row: (
                    -row["reference_count"], row["atom_count"],
                    row["descriptor"]))[:20],
        }
        predeclared_results[label] = pre_results
        generalization[label] = {
            "predeclared_train_zero_failure_descriptors": (
                generalization_rows(
                    pre_descriptors, train_rows, holdout_rows, label)),
            "overall_train_zero_failure_descriptors": generalization_rows(
                descriptors, train_rows, holdout_rows, label),
        }

    strict_label = "low_centered_3_1_selected_min_threshold"
    low_label = "low_centered_3_1_selected_max_threshold"
    pre_low_zero = zero_failure_rows(predeclared_results[low_label])
    pre_strict_zero = zero_failure_rows(predeclared_results[strict_label])
    best_low = all_results[low_label]["best_predeclared"][0]
    best_strict = all_results[strict_label]["best_predeclared"][0]

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "threshold_subclass": str(THRESHOLD_SOURCE.relative_to(ROOT)),
            "filter_order_receipt":
                "q286_first_three_filter_order_audit_receipt",
        },
        "status_boundary": (
            "finite independent descriptor audit only; descriptors selected "
            "after seeing the low-(3,1) labels are diagnostics, not stress "
            "definitions. This proves no stress theorem, signed correlation "
            "theorem, pointwise character-sum theorem, or Goldbach proof."),
        "question": (
            "Can the scalar-selected q286 broad low-(3,1) groups be "
            "described by small independent arithmetic/filter/correlation "
            "features without using centered (3,1)?"),
        "mechanism": (
            "Within the 89 broad full_nonpositive references, label the "
            "low-33 and strict low-24 centered-(3,1) groups from the frozen "
            "threshold receipt. Search one- and two-atom descriptors from "
            "predeclared q286 filter predicates, round numeric filter "
            "thresholds, CRT residues, and quadratic-character signs. Exact "
            "mod-143 residue atoms are included only as exploratory "
            "post-hoc diagnostics."),
        "prediction": (
            "A useful independent family should produce a nontrivial "
            "zero-failure descriptor, preferably predeclared and with "
            "holdout support in later cycles. If only scalar-selected or "
            "post-hoc tiny residue descriptors survive, the stress theorem "
            "still lacks an independent family."),
        "falsifier": (
            "No predeclared descriptor with support at least five and zero "
            "above-threshold rows, or a train-zero descriptor that fails on "
            "later cycles, falsifies the simple independent-descriptor route "
            "for this fixture."),
        "broad_full_nonpositive_reference_count": len(rows),
        "low_33_count": sum(
            row["low_centered_3_1_selected_max_threshold"] for row in rows),
        "strict_low_24_count": sum(
            row["low_centered_3_1_selected_min_threshold"] for row in rows),
        "train_cycles": list(TRAIN_CYCLES),
        "holdout_cycles": list(HOLDOUT_CYCLES),
        "cycle_counts": cycle_counts(rows),
        "atom_count": len(atoms),
        "predeclared_atom_count": len(predeclared_atoms),
        "minimum_support": MIN_SUPPORT,
        "descriptor_results": all_results,
        "train_holdout_generalization": generalization,
        "decision_metrics": {
            "low_33_zero_failure_predeclared_descriptor_count": len(
                pre_low_zero),
            "low_33_zero_failure_predeclared_holdout_supported_count":
                holdout_supported_zero_count(
                    predeclared_results[low_label], rows),
            "strict_low_24_zero_failure_predeclared_descriptor_count": len(
                pre_strict_zero),
            "strict_low_24_zero_failure_predeclared_holdout_supported_count":
                holdout_supported_zero_count(
                    predeclared_results[strict_label], rows),
            "best_low_33_predeclared_descriptor": best_low,
            "best_strict_low_24_predeclared_descriptor": best_strict,
        },
        "decision": (
            "Read the predeclared zero-failure descriptor counts and the "
            "train/holdout table. If no predeclared descriptor survives with "
            "meaningful support, the broad low-(3,1) family remains a "
            "scalar-selected/correlation diagnostic rather than a "
            "non-post-hoc stress definition. Exploratory exact residue "
            "pockets may suggest future frozen tests, but cannot be promoted "
            "from this receipt alone."),
        "next_obligation": (
            "Freeze any promising independent descriptor before a new "
            "window/reference audit, or abandon classifier language and "
            "seek a direct signed correlation estimate for centered (3,1)."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
