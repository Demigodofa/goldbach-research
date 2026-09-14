"""Build q286 volatile sign-polarity profile evidence.

The volatile boundary-cut graph records which one-channel additions cross the
classification boundary.  This derivative profile checks whether those
directions are exactly explained by the signs of the eight volatile channel
contributions, and records the finite polarity shared by the tight tail/clear
pair 1222142 and 1242118.
"""

from __future__ import annotations

from collections import Counter
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUBSET_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-subset-ablation.json")
BOUNDARY_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-boundary-cut-graph.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-sign-polarity-profile.json")
ZERO_TOL = 1e-14


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


def boundary_frequency(items):
    return {
        label_tuple(item["label"]): int(item["boundary_edge_count"])
        for item in items
    }


def sign_name(value):
    if value > ZERO_TOL:
        return "positive"
    if value < -ZERO_TOL:
        return "negative"
    return "zero"


def expected_boundary_direction(row_passes, sign):
    if sign == "zero":
        return "none"
    if row_passes:
        return "wrong_to_correct" if sign == "positive" else "correct_to_wrong"
    return "correct_to_wrong" if sign == "positive" else "wrong_to_correct"


def profile_row(target, subset_row, boundary_row, labels):
    row_passes = bool(subset_row["dominant_floor_passes"])
    correct_to_wrong = boundary_frequency(
        boundary_row["correct_to_wrong_channel_frequency"])
    wrong_to_correct = boundary_frequency(
        boundary_row["wrong_to_correct_channel_frequency"])
    channels = []
    violation_count = 0
    dormant_signed_count = 0
    for label in labels:
        value = float(subset_row[
            "volatile_channel_contributions"][label_key(label)])
        sign = sign_name(value)
        expected = expected_boundary_direction(row_passes, sign)
        c2w = correct_to_wrong.get(label, 0)
        w2c = wrong_to_correct.get(label, 0)
        if c2w and expected != "correct_to_wrong":
            violation_count += 1
        if w2c and expected != "wrong_to_correct":
            violation_count += 1
        if sign != "zero" and c2w == 0 and w2c == 0:
            dormant_signed_count += 1
        channels.append({
            "label": label,
            "contribution_to_principal": value,
            "sign": sign,
            "expected_boundary_direction_from_sign": expected,
            "correct_to_wrong_edge_count": c2w,
            "wrong_to_correct_edge_count": w2c,
            "active_boundary_edge_count": c2w + w2c,
            "dormant_signed_channel": sign != "zero" and c2w == 0 and w2c == 0,
        })

    positive = tuple(
        item["label"] for item in channels if item["sign"] == "positive")
    negative = tuple(
        item["label"] for item in channels if item["sign"] == "negative")
    zero = tuple(item["label"] for item in channels if item["sign"] == "zero")
    adverse = tuple(
        item["label"] for item in channels
        if item["expected_boundary_direction_from_sign"] == "correct_to_wrong")
    repair = tuple(
        item["label"] for item in channels
        if item["expected_boundary_direction_from_sign"] == "wrong_to_correct")
    return {
        "target": target,
        "target_mod_286": subset_row["target_mod_286"],
        "dominant_floor_passes": row_passes,
        "positive_channel_count": len(positive),
        "negative_channel_count": len(negative),
        "zero_channel_count": len(zero),
        "positive_channels": positive,
        "negative_channels": negative,
        "zero_channels": zero,
        "sign_expected_adverse_channels": adverse,
        "sign_expected_repair_channels": repair,
        "boundary_direction_sign_violation_count": violation_count,
        "dormant_signed_channel_count": dormant_signed_count,
        "correct_to_wrong_edge_count": boundary_row[
            "correct_to_wrong_edge_count"],
        "wrong_to_correct_edge_count": boundary_row[
            "wrong_to_correct_edge_count"],
        "boundary_edge_count": boundary_row["boundary_edge_count"],
        "channels": tuple(channels),
    }


def aggregate(rows):
    counts = Counter()
    for row in rows:
        counts["target_count"] += 1
        counts["positive_channel_count"] += row["positive_channel_count"]
        counts["negative_channel_count"] += row["negative_channel_count"]
        counts["zero_channel_count"] += row["zero_channel_count"]
        counts["boundary_edge_count"] += row["boundary_edge_count"]
        counts["correct_to_wrong_edge_count"] += row[
            "correct_to_wrong_edge_count"]
        counts["wrong_to_correct_edge_count"] += row[
            "wrong_to_correct_edge_count"]
        counts["boundary_direction_sign_violation_count"] += row[
            "boundary_direction_sign_violation_count"]
        counts["dormant_signed_channel_count"] += row[
            "dormant_signed_channel_count"]
    return dict(counts)


def main():
    subset_payload = json.loads(SUBSET_SOURCE.read_text(encoding="utf-8"))
    boundary_payload = json.loads(BOUNDARY_SOURCE.read_text(encoding="utf-8"))
    labels = tuple(label_tuple(label) for label in subset_payload[
        "volatile_labels"])
    subset_rows = {
        int(target): row
        for target, row in subset_payload["target_rows"].items()
    }
    boundary_rows = {
        int(row["target"]): row
        for row in boundary_payload["selected_rows"]
    }
    rows = tuple(
        profile_row(target, row, boundary_rows[target], labels)
        for target, row in sorted(subset_rows.items()))
    by_target = {row["target"]: row for row in rows}
    hard_targets = tuple(boundary_payload["hard_deficit_targets"])
    hard_rows = tuple(row for row in rows if row["target"] in hard_targets)
    deficit_rows = tuple(
        row for row in rows if not row["dominant_floor_passes"])
    clear_rows = tuple(row for row in rows if row["dominant_floor_passes"])

    violation_count = sum(
        row["boundary_direction_sign_violation_count"] for row in rows)
    if violation_count != 0:
        raise AssertionError(
            f"boundary/sign direction violations: {violation_count}")
    if tuple(by_target[1222142]["positive_channels"]) != (
            (1, 7), (4, 4)):
        raise AssertionError("1222142 positive polarity changed")
    if tuple(by_target[1242118]["positive_channels"]) != (
            (1, 7), (4, 4)):
        raise AssertionError("1242118 positive polarity changed")
    if by_target[1240888]["positive_channels"]:
        raise AssertionError("1240888 unexpectedly has positive channels")
    if tuple(by_target[1222142]["sign_expected_adverse_channels"]) != (
            (1, 7), (4, 4)):
        raise AssertionError("1222142 adverse polarity changed")
    if tuple(by_target[1242118]["sign_expected_repair_channels"]) != (
            (1, 7), (4, 4)):
        raise AssertionError("1242118 repair polarity changed")

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_subset_ablation": str(SUBSET_SOURCE.relative_to(ROOT)),
        "source_boundary_cut_graph": str(BOUNDARY_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite volatile sign-polarity diagnostic only; no volatile-rim "
            "theorem, stable-core theorem, selected-fixture classifier "
            "theorem, pointwise character-sum estimate, or Goldbach proof is "
            "established"),
        "candidate": (
            "The finite boundary-cut symmetry may be compressed to signed "
            "polarity of the volatile channel contributions, especially the "
            "shared positive pair (1,7),(4,4) on 1222142 and 1242118."),
        "mechanism": (
            "Compare each volatile channel contribution sign with its "
            "boundary-crossing direction in the full volatile cube.  Positive "
            "channels raise the row margin and negative channels lower it; "
            "the expected classification determines whether that is adverse "
            "or repairing."),
        "prediction": (
            "If boundary directions have no sign violations and the tight "
            "tail/clear pair shares a small polarity set, the next theorem "
            "target can be stated as signed channel polarity and magnitude "
            "control rather than an abstract Boolean cut."),
        "falsifier": (
            "A boundary edge whose direction contradicts its channel sign, "
            "or loss of the shared (1,7),(4,4) polarity on 1222142 and "
            "1242118, would falsify this compression."),
        "novelty_label": "new-to-this-task",
        "arithmetic_modulus": subset_payload["arithmetic_modulus"],
        "support": subset_payload["support"],
        "dominant_modes": subset_payload["dominant_modes"],
        "tail_threshold": subset_payload["tail_threshold"],
        "volatile_labels": labels,
        "volatile_channel_count": len(labels),
        "zero_tolerance": ZERO_TOL,
        "selected_rows": rows,
        "hard_deficit_targets": hard_targets,
        "hard_rows": hard_rows,
        "aggregates": {
            "selected": aggregate(rows),
            "deficit": aggregate(deficit_rows),
            "clear": aggregate(clear_rows),
            "hard_deficit": aggregate(hard_rows),
        },
        "summary": {
            "sign_direction_check": (
                "Every boundary-crossing direction matches the sign-predicted "
                "direction of its volatile channel contribution."),
            "target_1222142": (
                "positive channels are exactly (1,7) and (4,4), so those are "
                "the sign-expected adverse channels for this deficit row; "
                "the other six channels are sign-expected repair channels."),
            "target_1242118": (
                "positive channels are also exactly (1,7) and (4,4), but "
                "because this is a clear row they are sign-expected repair "
                "channels rather than adverse channels."),
            "target_1240888": (
                "all volatile channels are negative, yet the row is boundary-"
                "free because every volatile subset still classifies it "
                "correctly."),
        },
        "interpretation": {
            "symmetry_status": (
                "The remembered symmetry is finite and concrete: the tight "
                "tail 1222142 and tight clear 1242118 share the same positive "
                "volatile pair, while their expected classifications reverse "
                "whether that pair is adverse or repairing."),
            "route_status": (
                "The Boolean boundary-cut target compresses to signed channel "
                "polarity plus margin magnitude on this fixture."),
            "remaining_theorem": (
                "Prove the signed volatile channel polarity/magnitude behavior "
                "from actual binary-prime residue weights uniformly, or "
                "replace this channel-polarity picture with a full signed "
                "aggregate arithmetic-placement theorem."),
        },
        "volatile_sign_polarity_profile_measured": True,
        "boundary_direction_sign_violations": violation_count,
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
