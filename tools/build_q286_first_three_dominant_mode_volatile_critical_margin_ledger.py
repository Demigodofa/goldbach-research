"""Build q286 volatile critical-margin ledger evidence.

The polarity-magnitude ledger gives the rowwise surplus after repair pressure
beats adverse pressure.  This derivative receipt asks which individual
channels exceed that surplus, making them locally load-bearing or intolerable.
"""

from __future__ import annotations

from collections import Counter
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAGNITUDE_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-polarity-magnitude-ledger.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-critical-margin-ledger.json")


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


def critical_channel_records(row, labels, mode):
    contributions = contribution_map(row)
    surplus = float(row["signed_magnitude_surplus"])
    records = []
    for label in labels:
        magnitude = abs(contributions[label])
        remaining_surplus = surplus - magnitude
        records.append({
            "label": label,
            "contribution_to_principal": contributions[label],
            "magnitude_to_principal": magnitude,
            "signed_magnitude_surplus": surplus,
            "remaining_surplus_after_single_channel_loss": (
                remaining_surplus),
            "exceeds_surplus": magnitude > surplus,
            "mode": mode,
        })
    return tuple(records)


def row_criticality(row):
    repair_labels = tuple(
        label_tuple(label) for label in row["sign_expected_repair_channels"])
    adverse_labels = tuple(
        label_tuple(label) for label in row["sign_expected_adverse_channels"])
    repair_records = critical_channel_records(row, repair_labels, "repair")
    adverse_records = critical_channel_records(row, adverse_labels, "adverse")
    critical_repairs = tuple(
        item for item in repair_records if item["exceeds_surplus"])
    tolerable_repairs = tuple(
        item for item in repair_records if not item["exceeds_surplus"])
    intolerable_adverse = tuple(
        item for item in adverse_records if item["exceeds_surplus"])
    tolerable_adverse = tuple(
        item for item in adverse_records if not item["exceeds_surplus"])
    return {
        "target": row["target"],
        "target_mod_286": row["target_mod_286"],
        "dominant_floor_passes": row["dominant_floor_passes"],
        "signed_magnitude_surplus": row["signed_magnitude_surplus"],
        "repair_to_required_ratio": row["repair_to_required_ratio"],
        "repair_channel_count": len(repair_records),
        "critical_repair_channel_count": len(critical_repairs),
        "tolerable_repair_channel_count": len(tolerable_repairs),
        "adverse_channel_count": len(adverse_records),
        "intolerable_adverse_channel_count": len(intolerable_adverse),
        "tolerable_adverse_channel_count": len(tolerable_adverse),
        "critical_repair_channels": critical_repairs,
        "tolerable_repair_channels": tolerable_repairs,
        "intolerable_adverse_channels": intolerable_adverse,
        "tolerable_adverse_channels": tolerable_adverse,
    }


def aggregate(rows):
    counts = Counter()
    for row in rows:
        counts["target_count"] += 1
        counts["repair_channel_count"] += row["repair_channel_count"]
        counts["critical_repair_channel_count"] += row[
            "critical_repair_channel_count"]
        counts["adverse_channel_count"] += row["adverse_channel_count"]
        counts["intolerable_adverse_channel_count"] += row[
            "intolerable_adverse_channel_count"]
    return dict(counts)


def main():
    magnitude_payload = json.loads(
        MAGNITUDE_SOURCE.read_text(encoding="utf-8"))
    rows = tuple(
        row_criticality(row) for row in magnitude_payload["rows"])
    by_target = {row["target"]: row for row in rows}
    hard_targets = tuple(magnitude_payload["hard_deficit_targets"])
    hard_rows = tuple(row for row in rows if row["target"] in hard_targets)
    deficit_rows = tuple(
        row for row in rows if not row["dominant_floor_passes"])
    clear_rows = tuple(row for row in rows if row["dominant_floor_passes"])

    if by_target[1222142]["critical_repair_channel_count"] != 6:
        raise AssertionError("1222142 repair criticality changed")
    if by_target[1222142]["intolerable_adverse_channel_count"] != 2:
        raise AssertionError("1222142 adverse intolerance changed")
    if by_target[13556]["critical_repair_channel_count"] != 1:
        raise AssertionError("13556 repair criticality changed")
    if by_target[13556]["intolerable_adverse_channel_count"] != 6:
        raise AssertionError("13556 adverse intolerance changed")
    if by_target[1242118]["critical_repair_channel_count"] != 0:
        raise AssertionError("1242118 repair criticality changed")
    if by_target[1242118]["intolerable_adverse_channel_count"] != 4:
        raise AssertionError("1242118 adverse intolerance changed")
    if by_target[1240888]["repair_channel_count"] != 0:
        raise AssertionError("1240888 repair-channel count changed")
    selected_aggregate = aggregate(rows)
    if selected_aggregate["critical_repair_channel_count"] != 18:
        raise AssertionError("selected critical repair count changed")
    if selected_aggregate["intolerable_adverse_channel_count"] != 19:
        raise AssertionError("selected intolerable adverse count changed")

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_polarity_magnitude_ledger": str(
            MAGNITUDE_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite volatile critical-margin ledger only; no volatile-rim "
            "theorem, stable-core theorem, selected-fixture classifier "
            "theorem, pointwise character-sum estimate, or Goldbach proof is "
            "established"),
        "candidate": (
            "The quantitative signed-margin target may be sharpened by "
            "separating load-bearing repair channels from tolerable channels "
            "using each row's remaining surplus."),
        "mechanism": (
            "For each row, compare every repair-channel magnitude and every "
            "adverse-channel magnitude with the row's signed magnitude "
            "surplus.  A repair channel whose magnitude exceeds surplus is "
            "individually load-bearing under removal; an adverse channel "
            "whose magnitude exceeds surplus is individually intolerable "
            "under addition."),
        "prediction": (
            "If tight rows are all-critical, the theorem target needs named "
            "channel magnitudes, not just aggregate sign balance.  If tight "
            "rows have tolerable slack, the aggregate inequality may be the "
            "right level."),
        "falsifier": (
            "If 1222142 is not all-critical on both repair and adverse sides, "
            "or if selected critical counts drift from the magnitude ledger, "
            "this critical-margin compression is invalid."),
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
            "selected_fixture": (
                "18 of 39 repair channels are individually critical and "
                "19 of 41 adverse channels are individually intolerable."),
            "target_1222142": (
                "all six repair channels are individually load-bearing and "
                "both adverse channels are individually intolerable."),
            "target_13556": (
                "one of two repair channels is individually critical, and "
                "all six adverse channels are individually intolerable."),
            "target_1242118": (
                "neither repair channel is individually critical, but four "
                "of six adverse channels are individually intolerable."),
            "target_1240888": (
                "there are no repair channels; one of eight adverse channels "
                "is individually larger than the surplus, but the row remains "
                "clear under the actual full volatile package."),
        },
        "interpretation": {
            "hole_status": (
                "The finite q286 loop tightens to named critical channels: "
                "1222142 is an all-critical stress row, not a broad-reserve "
                "case."),
            "route_status": (
                "A proof must control individual load-bearing repair "
                "magnitudes as well as aggregate repair-versus-adverse "
                "balance, unless a stronger signed aggregate theorem replaces "
                "the channel ledger."),
            "remaining_theorem": (
                "Prove the critical repair/adverse channel magnitude bounds "
                "from actual binary-prime residue weights uniformly, or "
                "replace this with a full signed aggregate arithmetic-"
                "placement theorem."),
        },
        "volatile_critical_margin_ledger_measured": True,
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
