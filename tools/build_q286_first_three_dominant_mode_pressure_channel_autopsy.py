"""Build q286 dominant-mode pressure-channel autopsy evidence.

The pressure-horizon scout suggests a post-stress pressure-easy region.  This
builder compares named high-pressure/tight rows with earlier near-boundary
rows to see whether the negative pressure is carried by a stable small set of
real q286 channels or by residue-dependent rotating channels.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pressure-channel-autopsy.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)


SAMPLE_TARGETS = (
    1222142,
    1242118,
    1240888,
    1243018,
    1243130,
    1244072,
    1244094,
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


def compact_channel(channel):
    return {
        "representative_label": channel["representative_label"],
        "contribution_to_principal_ratio": (
            channel["contribution_to_principal_ratio"]),
        "absolute_contribution_to_principal_ratio": (
            channel["absolute_contribution_to_principal_ratio"]),
        "real_formula_multiplier": channel["real_formula_multiplier"],
    }


def compact_row(row):
    return {
        "target": row["target"],
        "target_mod_286": row["target_mod_286"],
        "dominant_sum_to_principal": (
            row["dominant_character_sum_to_principal_ratio"]),
        "negative_pressure_to_principal": (
            row["negative_channel_pressure_to_principal"]),
        "positive_offset_to_principal": (
            row["positive_channel_offset_to_principal"]),
        "required_positive_offset_for_floor": (
            row["required_positive_offset_for_floor"]),
        "positive_offset_slack_to_floor": (
            row["positive_offset_slack_to_floor"]),
        "dominant_floor_passes": row["dominant_floor_passes"],
        "positive_real_channel_count": row["positive_real_channel_count"],
        "negative_real_channel_count": row["negative_real_channel_count"],
        "top_negative_real_channels": [
            compact_channel(channel)
            for channel in row["top_negative_real_channels"][:3]],
        "top_positive_real_channels": [
            compact_channel(channel)
            for channel in row["top_positive_real_channels"][:2]],
    }


def main():
    receipt = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=SAMPLE_TARGETS,
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=6)
    target_rows = {
        target: compact_row(receipt["target_rows"][target])
        for target in SAMPLE_TARGETS}

    top_negative_counter = Counter()
    top_negative_examples = defaultdict(list)
    for target in SAMPLE_TARGETS:
        for channel in target_rows[target]["top_negative_real_channels"]:
            label = tuple(channel["representative_label"])
            top_negative_counter[label] += 1
            top_negative_examples[label].append({
                "target": target,
                "contribution_to_principal_ratio": (
                    channel["contribution_to_principal_ratio"]),
            })

    common_top_negative_labels = [
        {
            "representative_label": label,
            "top_three_occurrence_count": count,
            "examples": top_negative_examples[label],
        }
        for label, count in top_negative_counter.most_common()
    ]
    maximum_pressure_row = max(
        target_rows.values(),
        key=lambda row: row["negative_pressure_to_principal"])
    minimum_pressure_row = min(
        target_rows.values(),
        key=lambda row: row["negative_pressure_to_principal"])
    post_stress_targets = (1243018, 1243130, 1244072, 1244094)
    post_stress_rows = [target_rows[target] for target in post_stress_targets]
    post_stress_maximum_pressure_row = max(
        post_stress_rows,
        key=lambda row: row["negative_pressure_to_principal"])

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite named-row pressure-channel autopsy only; no one-channel "
            "pressure theorem, multi-channel envelope theorem, pointwise "
            "character-sum estimate, signed-projection theorem, or Goldbach "
            "proof is established"),
        "mechanism": (
            "Check whether the post-stress pressure-easy rows are explained "
            "by disappearance of the same top negative channels seen in "
            "near-boundary rows, or whether top negative channels rotate by "
            "target residue."),
        "falsifier": (
            "A stable dominant top-negative label across the named rows would "
            "support a one-channel pressure route; rotating top labels demote "
            "that route and point to a multi-channel or residue-dependent "
            "pressure envelope."),
        "sample_targets": SAMPLE_TARGETS,
        "post_stress_targets": post_stress_targets,
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "active_real_channel_count": receipt["active_real_channel_count"],
        "dominant_floor_failure_targets": (
            receipt["dominant_floor_failure_targets"]),
        "dominant_floor_pass_targets": receipt["dominant_floor_pass_targets"],
        "maximum_pressure_row": maximum_pressure_row,
        "minimum_pressure_row": minimum_pressure_row,
        "post_stress_maximum_pressure_row": (
            post_stress_maximum_pressure_row),
        "common_top_negative_labels": common_top_negative_labels,
        "distinct_top_three_negative_label_count": len(top_negative_counter),
        "target_rows": target_rows,
        "maximum_real_channel_identity_error": (
            receipt["maximum_real_channel_identity_error"]),
        "interpretation": {
            "observed_shape": (
                "The top-three negative channels rotate across the named "
                "rows; no single label dominates the pressure ledger across "
                "the sample.  The post-stress high-pressure rows are below "
                "0.3, but they still use nontrivial negative-channel ledgers."),
            "remaining_theorem": (
                "A pressure proof should target a multi-channel or "
                "residue-dependent pressure envelope, not a one-channel "
                "bound.  The finite autopsy does not identify an external "
                "theorem proving that envelope."),
        },
        "dominant_mode_pressure_channel_autopsy_measured": True,
        "one_channel_pressure_theorem_proved": False,
        "multi_channel_pressure_envelope_proved": False,
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
