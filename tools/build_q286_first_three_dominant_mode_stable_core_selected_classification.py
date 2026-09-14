"""Build q286 stable-core selected-fixture classification evidence.

The named holdout checked the stable core relative to one late tail.  This
builder applies the same stable/volatile partition absolutely to the older
selected deficit/clear fixture and records whether the stable core alone
classifies the q286 dominant floor.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIGN_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pairwise-swing-sign-stability.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-stable-core-selected-classification.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)


SAMPLE_TARGETS = (
    24424,
    13556,
    13822,
    40420,
    55864,
    164598,
    129706,
    1222142,
    1242118,
    1240888,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_ready(item) for item in value]
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def label_tuple(label):
    return tuple(int(part) for part in label)


def channel_map(row):
    return {
        label_tuple(channel["representative_label"]): (
            channel["contribution_to_principal_ratio"])
        for channel in row["real_channel_contribution_rows"]
    }


def summarize(values):
    values = tuple(values)
    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None}
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def main():
    sign_payload = json.loads(SIGN_SOURCE.read_text(encoding="utf-8"))
    stable_positive = tuple(
        label_tuple(label) for label in sign_payload["stable_positive_labels"])
    stable_negative = tuple(
        label_tuple(label) for label in sign_payload["stable_negative_labels"])
    volatile = tuple(
        label_tuple(label) for label in sign_payload["sign_flip_labels"])
    stable_core = stable_positive + stable_negative

    receipt = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=SAMPLE_TARGETS,
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=25)

    rows = {}
    clear_targets = []
    failure_targets = []
    stable_core_pass_targets = []
    stable_core_failure_targets = []
    stable_core_overrescued_failure_targets = []
    stable_core_preserved_clear_targets = []
    stable_core_missed_clear_targets = []
    volatile_restored_failure_targets = []
    volatile_preserved_clear_targets = []
    volatile_broke_clear_targets = []

    for target in SAMPLE_TARGETS:
        row = receipt["target_rows"][target]
        channels = channel_map(row)
        stable_positive_sum = math.fsum(
            channels.get(label, 0.0) for label in stable_positive)
        stable_negative_sum = math.fsum(
            channels.get(label, 0.0) for label in stable_negative)
        volatile_sum = math.fsum(
            channels.get(label, 0.0) for label in volatile)
        stable_sum = stable_positive_sum + stable_negative_sum
        reconstructed_sum = stable_sum + volatile_sum
        dominant_sum = row["dominant_character_sum_to_principal_ratio"]
        stable_margin = stable_sum + .3
        full_margin = reconstructed_sum + .3
        stable_passes = stable_margin >= 0.0
        full_passes = row["dominant_floor_passes"]

        if full_passes:
            clear_targets.append(target)
            if stable_passes:
                stable_core_preserved_clear_targets.append(target)
            else:
                stable_core_missed_clear_targets.append(target)
            if full_margin >= 0.0:
                volatile_preserved_clear_targets.append(target)
            else:
                volatile_broke_clear_targets.append(target)
        else:
            failure_targets.append(target)
            if stable_passes:
                stable_core_overrescued_failure_targets.append(target)
                if full_margin < 0.0:
                    volatile_restored_failure_targets.append(target)

        if stable_passes:
            stable_core_pass_targets.append(target)
        else:
            stable_core_failure_targets.append(target)

        rows[target] = {
            "target": target,
            "target_mod_286": row["target_mod_286"],
            "dominant_floor_passes": full_passes,
            "stable_core_floor_passes": stable_passes,
            "stable_positive_sum_to_principal": stable_positive_sum,
            "stable_negative_sum_to_principal": stable_negative_sum,
            "stable_core_sum_to_principal": stable_sum,
            "volatile_rim_sum_to_principal": volatile_sum,
            "stable_core_margin_to_floor": stable_margin,
            "full_margin_to_floor_reconstructed": full_margin,
            "dominant_margin_to_floor": dominant_sum + .3,
            "reconstruction_error": abs(reconstructed_sum - dominant_sum),
            "volatile_restores_stable_core_false_positive": bool(
                not full_passes and stable_passes and full_margin < 0.0),
            "stable_core_false_positive": bool(
                not full_passes and stable_passes),
            "stable_core_false_negative": bool(
                full_passes and not stable_passes),
        }

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_evidence": str(SIGN_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite selected-fixture classification diagnostic only; no "
            "stable-core theorem, volatile-rim theorem, coupled budget "
            "theorem, pointwise character-sum estimate, or Goldbach proof is "
            "established"),
        "mechanism": (
            "Apply the frozen stable-positive, stable-negative, and volatile "
            "q286 channel partition absolutely to the selected deficit/clear "
            "fixture."),
        "prediction": (
            "If the stable core is a genuine clear-side lower-bound package, "
            "it should preserve selected clears; if it is not enough for "
            "classification, it will over-rescue selected deficits until the "
            "volatile rim is restored."),
        "falsifier": (
            "A selected clear missed by the stable core falsifies stable-core "
            "clear preservation on this fixture; any stable-core false "
            "positive not restored by the volatile rim falsifies the tested "
            "stable/volatile selected classification."),
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "active_real_channel_count": receipt["active_real_channel_count"],
        "sample_targets": SAMPLE_TARGETS,
        "clear_targets": tuple(clear_targets),
        "failure_targets": tuple(failure_targets),
        "stable_positive_labels": stable_positive,
        "stable_negative_labels": stable_negative,
        "volatile_labels": volatile,
        "stable_core_channel_count": len(stable_core),
        "volatile_channel_count": len(volatile),
        "target_rows": rows,
        "stable_core_pass_targets": tuple(stable_core_pass_targets),
        "stable_core_failure_targets": tuple(stable_core_failure_targets),
        "stable_core_preserved_clear_targets": tuple(
            stable_core_preserved_clear_targets),
        "stable_core_missed_clear_targets": tuple(
            stable_core_missed_clear_targets),
        "stable_core_overrescued_failure_targets": tuple(
            stable_core_overrescued_failure_targets),
        "volatile_restored_failure_targets": tuple(
            volatile_restored_failure_targets),
        "volatile_preserved_clear_targets": tuple(
            volatile_preserved_clear_targets),
        "volatile_broke_clear_targets": tuple(volatile_broke_clear_targets),
        "all_selected_clears_preserved_by_stable_core": bool(
            not stable_core_missed_clear_targets),
        "stable_core_false_positive_count": len(
            stable_core_overrescued_failure_targets),
        "stable_core_false_negative_count": len(
            stable_core_missed_clear_targets),
        "volatile_restores_all_stable_core_false_positives": (
            tuple(stable_core_overrescued_failure_targets)
            == tuple(volatile_restored_failure_targets)),
        "stable_core_margin_summary": summarize(
            row["stable_core_margin_to_floor"] for row in rows.values()),
        "volatile_rim_sum_summary": summarize(
            row["volatile_rim_sum_to_principal"] for row in rows.values()),
        "clear_volatile_rim_sum_summary": summarize(
            row["volatile_rim_sum_to_principal"]
            for row in rows.values()
            if row["dominant_floor_passes"]),
        "failure_volatile_rim_sum_summary": summarize(
            row["volatile_rim_sum_to_principal"]
            for row in rows.values()
            if not row["dominant_floor_passes"]),
        "maximum_reconstruction_error": max(
            row["reconstruction_error"] for row in rows.values()),
        "interpretation": {
            "clear_side": (
                "The stable core preserves all selected clears if "
                "all_selected_clears_preserved_by_stable_core is true."),
            "classification_gap": (
                "Stable core alone is not a selected-fixture classifier when "
                "stable_core_false_positive_count is nonzero."),
            "volatile_role": (
                "The volatile rim is row-dependent classification structure, "
                "not merely disposable noise, if it restores every stable-core "
                "false positive while preserving all selected clears."),
            "remaining_theorem": (
                "Prove stable-core clear preservation plus a non-circular "
                "volatile/exclusion theorem, or replace this finite partition "
                "with a stronger arithmetic placement theorem."),
        },
        "stable_core_selected_classification_measured": True,
        "stable_core_clear_preservation_theorem_proved": False,
        "stable_core_selected_classifier_proved": False,
        "volatile_rim_classification_theorem_proved": False,
        "coupled_budget_theorem_proved": False,
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
