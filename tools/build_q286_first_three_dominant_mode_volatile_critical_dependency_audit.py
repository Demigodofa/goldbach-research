"""Build q286 volatile critical-channel dependency audit evidence.

The critical-margin ledger says which individual channels are load-bearing.
This derivative receipt asks whether the signed magnitude inequality itself
compresses to smaller sufficient repair bundles, or whether the apparent
symmetry remains irreducible at the current selected-fixture level.
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
CRITICAL_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-critical-margin-ledger.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-critical-dependency-audit.json")
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


def bundle_labels(labels, indexes):
    return tuple(labels[index] for index in indexes)


def bundle_record(labels, magnitudes, indexes, threshold):
    chosen = bundle_labels(labels, indexes)
    total = sum(magnitudes[label] for label in chosen)
    return {
        "labels": chosen,
        "size": len(chosen),
        "magnitude": total,
        "threshold": threshold,
        "slack_over_threshold": total - threshold,
    }


def all_bundle_records(labels, magnitudes, threshold):
    records = []
    for size in range(len(labels) + 1):
        for indexes in combinations(range(len(labels)), size):
            record = bundle_record(labels, magnitudes, indexes, threshold)
            if strict_exceeds(record["magnitude"], threshold):
                records.append(record)
    return tuple(records)


def is_proper_subset(left, right):
    left_labels = set(left["labels"])
    right_labels = set(right["labels"])
    return left_labels < right_labels


def minimal_bundles(labels, magnitudes, threshold):
    sufficient = all_bundle_records(labels, magnitudes, threshold)
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


def bundle_summary(bundles, full_labels):
    if not bundles:
        return {
            "count": 0,
            "minimum_size": None,
            "maximum_size": None,
            "full_bundle_is_unique": False,
            "compressible": False,
        }
    sizes = [bundle["size"] for bundle in bundles]
    full_label_set = set(full_labels)
    full_bundle_is_unique = (
        len(bundles) == 1 and set(bundles[0]["labels"]) == full_label_set)
    return {
        "count": len(bundles),
        "minimum_size": min(sizes),
        "maximum_size": max(sizes),
        "full_bundle_is_unique": full_bundle_is_unique,
        "compressible": min(sizes) < len(full_labels),
    }


def row_dependency(row):
    contributions = contribution_map(row)
    magnitudes = {
        label: abs(contribution)
        for label, contribution in contributions.items()
    }
    repair_labels = tuple(
        label_tuple(label) for label in row["sign_expected_repair_channels"])
    adverse_labels = tuple(
        label_tuple(label) for label in row["sign_expected_adverse_channels"])
    repair_threshold = float(row["required_repair_magnitude"])
    adverse_threshold = float(row["signed_magnitude_surplus"])
    repair_bundles = minimal_bundles(
        repair_labels, magnitudes, repair_threshold)
    adverse_bundles = minimal_bundles(
        adverse_labels, magnitudes, adverse_threshold)
    best_repair_near_miss = best_insufficient_bundle(
        repair_labels, magnitudes, repair_threshold)
    best_adverse_tolerated = best_insufficient_bundle(
        adverse_labels, magnitudes, adverse_threshold)
    repair_summary = bundle_summary(repair_bundles, repair_labels)
    adverse_summary = bundle_summary(adverse_bundles, adverse_labels)
    return {
        "target": row["target"],
        "target_mod_286": row["target_mod_286"],
        "dominant_floor_passes": row["dominant_floor_passes"],
        "full_margin_to_floor": row["full_margin_to_floor"],
        "base_margin_without_volatile": row["base_margin_without_volatile"],
        "repair_magnitude": row["repair_magnitude"],
        "required_repair_magnitude": row["required_repair_magnitude"],
        "signed_magnitude_surplus": row["signed_magnitude_surplus"],
        "adverse_magnitude": row["adverse_magnitude"],
        "repair_to_required_ratio": row["repair_to_required_ratio"],
        "repair_channel_count": len(repair_labels),
        "adverse_channel_count": len(adverse_labels),
        "repair_labels": repair_labels,
        "adverse_labels": adverse_labels,
        "minimal_sufficient_repair_bundles": repair_bundles,
        "repair_bundle_summary": repair_summary,
        "best_insufficient_repair_bundle": best_repair_near_miss,
        "minimal_intolerable_adverse_bundles": adverse_bundles,
        "adverse_bundle_summary": adverse_summary,
        "best_tolerated_adverse_bundle": best_adverse_tolerated,
    }


def aggregate(rows):
    counts = Counter()
    for row in rows:
        counts["target_count"] += 1
        counts["repair_channel_count"] += row["repair_channel_count"]
        counts["adverse_channel_count"] += row["adverse_channel_count"]
        counts["minimal_sufficient_repair_bundle_count"] += row[
            "repair_bundle_summary"]["count"]
        counts["minimal_intolerable_adverse_bundle_count"] += row[
            "adverse_bundle_summary"]["count"]
        if row["repair_bundle_summary"]["full_bundle_is_unique"]:
            counts["full_repair_bundle_unique_count"] += 1
        if row["repair_bundle_summary"]["compressible"]:
            counts["repair_compressible_count"] += 1
        if row["adverse_bundle_summary"]["minimum_size"] == 1:
            counts["single_adverse_intolerable_count"] += 1
    return dict(counts)


def critical_row_by_target(payload):
    return {int(row["target"]): row for row in payload["rows"]}


def main():
    magnitude_payload = json.loads(
        MAGNITUDE_SOURCE.read_text(encoding="utf-8"))
    critical_payload = json.loads(
        CRITICAL_SOURCE.read_text(encoding="utf-8"))
    rows = tuple(row_dependency(row) for row in magnitude_payload["rows"])
    by_target = {row["target"]: row for row in rows}
    critical_rows = critical_row_by_target(critical_payload)

    stress = by_target[1222142]
    stress_repair = stress["repair_bundle_summary"]
    stress_adverse = stress["adverse_bundle_summary"]
    if not stress_repair["full_bundle_is_unique"]:
        raise AssertionError("1222142 repair bundle unexpectedly compresses")
    if stress_repair["minimum_size"] != 6:
        raise AssertionError("1222142 minimum repair bundle size changed")
    if stress_adverse["count"] != 2 or stress_adverse["minimum_size"] != 1:
        raise AssertionError("1222142 adverse singleton structure changed")
    stress_adverse_labels = {
        tuple(bundle["labels"][0]) for bundle in
        stress["minimal_intolerable_adverse_bundles"]
    }
    if stress_adverse_labels != {(1, 7), (4, 4)}:
        raise AssertionError("1222142 adverse labels changed")
    if critical_rows[1222142]["critical_repair_channel_count"] != 6:
        raise AssertionError("source critical ledger drifted for 1222142")
    if critical_rows[1222142]["intolerable_adverse_channel_count"] != 2:
        raise AssertionError("source adverse criticality drifted for 1222142")

    hard_targets = tuple(magnitude_payload["hard_deficit_targets"])
    hard_rows = tuple(row for row in rows if row["target"] in hard_targets)
    deficit_rows = tuple(
        row for row in rows if not row["dominant_floor_passes"])
    clear_rows = tuple(row for row in rows if row["dominant_floor_passes"])

    selected_aggregate = aggregate(rows)
    if selected_aggregate["target_count"] != 10:
        raise AssertionError("selected fixture size changed")

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_polarity_magnitude_ledger": str(
            MAGNITUDE_SOURCE.relative_to(ROOT)),
        "source_critical_margin_ledger": str(
            CRITICAL_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite volatile critical-dependency audit only; no "
            "volatile-rim theorem, stable-core theorem, selected-fixture "
            "classifier theorem, pointwise character-sum estimate, or "
            "Goldbach proof is established"),
        "candidate": (
            "The q286 volatile symmetry might compress from individual "
            "critical channels to smaller sufficient repair bundles or "
            "smaller intolerable adverse bundles."),
        "mechanism": (
            "For each selected row, enumerate every subset of sign-expected "
            "repair channels and retain the inclusion-minimal subsets whose "
            "total magnitude beats the row's required repair magnitude.  "
            "Separately enumerate inclusion-minimal adverse subsets whose "
            "total magnitude exceeds the signed surplus."),
        "prediction": (
            "If the loop is algebraically compressing, tight rows should "
            "have a proper repair bundle or a shared lower-dimensional "
            "adverse bundle.  If not, the stress row's full repair side "
            "should be the unique minimal sufficient bundle."),
        "falsifier": (
            "A proper sufficient repair bundle for 1222142, loss of the "
            "two singleton adverse bundle structure, or disagreement with "
            "the source critical-margin ledger would falsify this finite "
            "dependency audit."),
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
            "selected": selected_aggregate,
            "deficit": aggregate(deficit_rows),
            "clear": aggregate(clear_rows),
            "hard_deficit": aggregate(hard_rows),
        },
        "summary": {
            "target_1222142": (
                "The stress row has exactly one minimal sufficient repair "
                "bundle, and it is the full six-channel repair set.  Its "
                "two minimal intolerable adverse bundles are the singleton "
                "channels (1,7) and (4,4)."),
            "compression_result": (
                "The attractive lower-dimensional repair-compression route "
                "does not close for 1222142 at the current fixture level."),
            "loop_status": (
                "The q286 loop tightens further: the finite hole is not "
                "visibly infinite noise, but the tight stress row is also "
                "not reducible to a smaller repair bundle in this audit."),
        },
        "interpretation": {
            "hole_status": (
                "For 1222142, all six repair channels are jointly necessary "
                "in the signed magnitude abstraction, while either adverse "
                "channel alone can erase the surplus."),
            "route_status": (
                "A theorem must either control the full six-versus-two "
                "critical-channel balance for the stress row, or replace "
                "this local bundle ledger with a stronger signed aggregate "
                "arithmetic-placement theorem."),
            "remaining_theorem": (
                "Prove the critical repair/adverse bundle magnitude bounds "
                "from actual binary-prime residue weights uniformly, or "
                "find a nonlocal aggregate theorem that makes the bundle "
                "ledger unnecessary."),
        },
        "volatile_critical_dependency_audit_measured": True,
        "repair_compression_for_1222142_found": False,
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
