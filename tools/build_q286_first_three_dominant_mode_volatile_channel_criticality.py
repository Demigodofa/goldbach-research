"""Build q286 volatile-channel leave-one-out criticality evidence.

The volatile subset ablation showed that no proper subset of the eight
volatile channels gives exact selected-fixture classification.  This
derivative builder records which selected rows each individual volatile
channel protects under leave-one-out deletion.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-subset-ablation.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-channel-criticality.json")


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


def contribution_for(row, label):
    return row["volatile_channel_contributions"][str(label)]


def margin_without_channel(row, label):
    full_margin = (
        row["stable_core_sum_to_principal"]
        + row["full_volatile_sum_to_principal"]
        + .3)
    return full_margin - contribution_for(row, label)


def classify_without_channel(row, label):
    return margin_without_channel(row, label) >= 0.0


def main():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    labels = tuple(label_tuple(label) for label in source["volatile_labels"])
    target_rows = {
        int(target): row for target, row in source["target_rows"].items()
    }

    leave_one_out_rows = []
    channels_with_false_negatives = []
    pure_deficit_blocker_channels = []
    all_error_targets = set()

    for label in labels:
        false_positive_targets = []
        false_negative_targets = []
        changed_rows = []
        for target, row in sorted(target_rows.items()):
            full_margin = (
                row["stable_core_sum_to_principal"]
                + row["full_volatile_sum_to_principal"]
                + .3)
            reduced_margin = margin_without_channel(row, label)
            reduced_passes = reduced_margin >= 0.0
            full_passes = bool(row["dominant_floor_passes"])
            if reduced_passes == full_passes:
                continue
            changed = {
                "target": target,
                "target_mod_286": row["target_mod_286"],
                "dominant_floor_passes": full_passes,
                "full_margin_to_floor": full_margin,
                "margin_without_channel": reduced_margin,
                "removed_channel_contribution": contribution_for(
                    row, label),
                "error_type": (
                    "false_positive" if reduced_passes
                    else "false_negative"),
            }
            changed_rows.append(changed)
            all_error_targets.add(target)
            if reduced_passes:
                false_positive_targets.append(target)
            else:
                false_negative_targets.append(target)

        row = {
            "removed_channel_label": label,
            "changed_row_count": len(changed_rows),
            "false_positive_targets": tuple(false_positive_targets),
            "false_negative_targets": tuple(false_negative_targets),
            "false_positive_count": len(false_positive_targets),
            "false_negative_count": len(false_negative_targets),
            "leave_one_out_exact_classification": bool(not changed_rows),
            "changed_rows": tuple(changed_rows),
        }
        leave_one_out_rows.append(row)
        if false_negative_targets:
            channels_with_false_negatives.append(label)
        else:
            pure_deficit_blocker_channels.append(label)

    row_criticality = []
    for target, row in sorted(target_rows.items()):
        critical_channels = []
        for label in labels:
            if classify_without_channel(row, label) != bool(
                    row["dominant_floor_passes"]):
                critical_channels.append(label)
        row_criticality.append({
            "target": target,
            "target_mod_286": row["target_mod_286"],
            "dominant_floor_passes": row["dominant_floor_passes"],
            "critical_volatile_channels": tuple(critical_channels),
            "critical_volatile_channel_count": len(critical_channels),
        })

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_evidence": str(SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite leave-one-out volatile-channel criticality diagnostic "
            "only; no volatile-rim theorem, stable-core theorem, "
            "selected-fixture classifier theorem, pointwise character-sum "
            "estimate, or Goldbach proof is established"),
        "mechanism": (
            "Delete each volatile channel from the full volatile rim while "
            "holding the stable core and the other volatile channels fixed."),
        "prediction": (
            "If every volatile channel has a selected-row witness, the full "
            "volatile package is leave-one-out critical on this fixture.  "
            "False negatives identify channels that also support selected "
            "clears, not only block selected deficits."),
        "falsifier": (
            "A volatile channel whose leave-one-out deletion still gives "
            "exact selected-fixture classification falsifies leave-one-out "
            "criticality for the full rim."),
        "arithmetic_modulus": source["arithmetic_modulus"],
        "support": source["support"],
        "dominant_modes": source["dominant_modes"],
        "tail_threshold": source["tail_threshold"],
        "active_real_channel_count": source["active_real_channel_count"],
        "sample_targets": source["sample_targets"],
        "clear_targets": source["clear_targets"],
        "failure_targets": source["failure_targets"],
        "volatile_labels": labels,
        "volatile_channel_count": len(labels),
        "leave_one_out_rows": tuple(leave_one_out_rows),
        "row_criticality": tuple(row_criticality),
        "leave_one_out_exact_channel_count": sum(
            1 for row in leave_one_out_rows
            if row["leave_one_out_exact_classification"]),
        "all_volatile_channels_leave_one_out_critical": all(
            not row["leave_one_out_exact_classification"]
            for row in leave_one_out_rows),
        "channels_with_clear_false_negative_on_deletion": tuple(
            channels_with_false_negatives),
        "pure_deficit_blocker_channels_on_deletion": tuple(
            pure_deficit_blocker_channels),
        "total_leave_one_out_changed_rows": sum(
            row["changed_row_count"] for row in leave_one_out_rows),
        "targets_hit_by_any_leave_one_out_error": tuple(
            sorted(all_error_targets)),
        "interpretation": {
            "criticality": (
                "If all_volatile_channels_leave_one_out_critical is true, "
                "every volatile channel has at least one selected-row witness "
                "against deletion."),
            "mixed_role": (
                "Channels with clear false negatives on deletion cannot be "
                "treated as pure deficit blockers on this fixture."),
            "remaining_theorem": (
                "A proof route must explain signed row-specific volatile "
                "action, not just a uniform negative volatile cap."),
        },
        "volatile_channel_criticality_measured": True,
        "volatile_leave_one_out_criticality_theorem_proved": False,
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
