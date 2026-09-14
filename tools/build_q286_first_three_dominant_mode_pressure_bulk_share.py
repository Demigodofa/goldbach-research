"""Build q286 dominant-mode pressure bulk-share evidence.

The pressure-channel autopsy demoted a single recurring channel.  This
builder asks the next sharper question: whether negative pressure is carried
by just the top few negative channels or by a broader multi-channel tail.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pressure-bulk-share.json")
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


def share(values, pressure, count):
    return (
        math.fsum(values[:count]) / pressure
        if pressure > 0.0 else math.nan)


def compact_channel(channel):
    return {
        "representative_label": channel["representative_label"],
        "contribution_to_principal_ratio": (
            channel["contribution_to_principal_ratio"]),
        "absolute_contribution_to_principal_ratio": (
            channel["absolute_contribution_to_principal_ratio"]),
    }


def main():
    receipt = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=SAMPLE_TARGETS,
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=25)
    target_rows = {}
    top1_shares = []
    top3_shares = []
    top5_shares = []
    top10_shares = []
    for target in SAMPLE_TARGETS:
        source_row = receipt["target_rows"][target]
        pressure = source_row["negative_channel_pressure_to_principal"]
        negative_values = [
            abs(channel["contribution_to_principal_ratio"])
            for channel in source_row["top_negative_real_channels"]]
        row = {
            "target": target,
            "target_mod_286": source_row["target_mod_286"],
            "dominant_sum_to_principal": (
                source_row["dominant_character_sum_to_principal_ratio"]),
            "dominant_floor_passes": source_row["dominant_floor_passes"],
            "negative_pressure_to_principal": pressure,
            "positive_offset_to_principal": (
                source_row["positive_channel_offset_to_principal"]),
            "positive_offset_slack_to_floor": (
                source_row["positive_offset_slack_to_floor"]),
            "negative_real_channel_count": (
                source_row["negative_real_channel_count"]),
            "positive_real_channel_count": (
                source_row["positive_real_channel_count"]),
            "top1_negative_pressure_share": share(
                negative_values, pressure, 1),
            "top3_negative_pressure_share": share(
                negative_values, pressure, 3),
            "top5_negative_pressure_share": share(
                negative_values, pressure, 5),
            "top10_negative_pressure_share": share(
                negative_values, pressure, 10),
            "top_negative_real_channels": [
                compact_channel(channel)
                for channel in source_row["top_negative_real_channels"]],
        }
        target_rows[target] = row
        top1_shares.append(row["top1_negative_pressure_share"])
        top3_shares.append(row["top3_negative_pressure_share"])
        top5_shares.append(row["top5_negative_pressure_share"])
        top10_shares.append(row["top10_negative_pressure_share"])

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite named-row pressure bulk-share diagnostic only; no top-k "
            "pressure theorem, multi-channel envelope theorem, pointwise "
            "character-sum estimate, signed-projection theorem, or Goldbach "
            "proof is established"),
        "mechanism": (
            "After one-channel pressure was demoted, test whether the "
            "negative pressure is still top-heavy enough for a small top-k "
            "channel theorem or whether pressure is distributed across a "
            "larger channel tail."),
        "falsifier": (
            "If top-one/top-three/top-five channels carry only a minority or "
            "moderate share of pressure on the named rows, a small top-k "
            "pressure theorem is too narrow for the observed ledger."),
        "sample_targets": SAMPLE_TARGETS,
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "active_real_channel_count": receipt["active_real_channel_count"],
        "dominant_floor_failure_targets": (
            receipt["dominant_floor_failure_targets"]),
        "dominant_floor_pass_targets": receipt["dominant_floor_pass_targets"],
        "top1_share_range": {
            "minimum": min(top1_shares),
            "maximum": max(top1_shares),
        },
        "top3_share_range": {
            "minimum": min(top3_shares),
            "maximum": max(top3_shares),
        },
        "top5_share_range": {
            "minimum": min(top5_shares),
            "maximum": max(top5_shares),
        },
        "top10_share_range": {
            "minimum": min(top10_shares),
            "maximum": max(top10_shares),
        },
        "maximum_top3_share_row": max(
            target_rows.values(),
            key=lambda row: row["top3_negative_pressure_share"]),
        "minimum_top3_share_row": min(
            target_rows.values(),
            key=lambda row: row["top3_negative_pressure_share"]),
        "target_rows": target_rows,
        "maximum_real_channel_identity_error": (
            receipt["maximum_real_channel_identity_error"]),
        "interpretation": {
            "observed_shape": (
                "Negative pressure is not concentrated in one or three "
                "channels on the named rows.  Top-five channels still leave "
                "a substantial tail on several rows."),
            "remaining_theorem": (
                "The pressure branch now points to a bulk multi-channel or "
                "residue-dependent envelope for the negative real-channel "
                "ledger, not a one-channel or tiny top-k bound."),
        },
        "dominant_mode_pressure_bulk_share_measured": True,
        "small_topk_pressure_theorem_proved": False,
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
