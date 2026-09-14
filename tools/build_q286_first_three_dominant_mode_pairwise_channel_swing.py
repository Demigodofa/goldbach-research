"""Build q286 dominant-mode pairwise channel-swing evidence.

The pressure/offset scalar falsifier leaves the coupled curve
``P >= B - 0.3`` as the live scalar target.  This builder checks whether
tail-to-clear movement near that curve is explained by one dominant real
channel or by a broader signed-channel swing.
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
    / "q286-first-three-dominant-mode-pairwise-channel-swing.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)


PAIR_TARGETS = (
    (1222142, 1242118),
    (1222142, 1240888),
)
SAMPLE_TARGETS = tuple(dict.fromkeys(
    target for pair in PAIR_TARGETS for target in pair))


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


def channel_map(row):
    return {
        tuple(channel["representative_label"]): channel
        for channel in row["real_channel_contribution_rows"]
    }


def compact_row(row):
    return {
        "target": row["target"],
        "target_mod_286": row["target_mod_286"],
        "dominant_floor_passes": row["dominant_floor_passes"],
        "dominant_sum_to_principal": (
            row["dominant_character_sum_to_principal_ratio"]),
        "negative_pressure_B": row["negative_channel_pressure_to_principal"],
        "positive_offset_P": row["positive_channel_offset_to_principal"],
        "positive_to_negative_pressure_ratio_R": (
            row["positive_to_negative_pressure_ratio"]),
        "positive_offset_slack_to_floor": (
            row["positive_offset_slack_to_floor"]),
    }


def share(values, count):
    total = math.fsum(values)
    if total <= 0.0:
        return math.nan
    return math.fsum(values[:count]) / total


def build_pair(tail, clear):
    tail_channels = channel_map(tail)
    clear_channels = channel_map(clear)
    swing_rows = []
    for label in sorted(set(tail_channels) | set(clear_channels)):
        tail_contribution = tail_channels.get(
            label, {"contribution_to_principal_ratio": 0.0})[
                "contribution_to_principal_ratio"]
        clear_contribution = clear_channels.get(
            label, {"contribution_to_principal_ratio": 0.0})[
                "contribution_to_principal_ratio"]
        delta = clear_contribution - tail_contribution
        swing_rows.append({
            "representative_label": label,
            "tail_contribution_to_principal": tail_contribution,
            "clear_contribution_to_principal": clear_contribution,
            "clear_minus_tail_swing_to_principal": delta,
            "helps_clear_relative_to_tail": bool(delta > 0.0),
        })
    positive_rows = sorted(
        (row for row in swing_rows
         if row["clear_minus_tail_swing_to_principal"] > 0.0),
        key=lambda row: row["clear_minus_tail_swing_to_principal"],
        reverse=True)
    negative_rows = sorted(
        (row for row in swing_rows
         if row["clear_minus_tail_swing_to_principal"] < 0.0),
        key=lambda row: row["clear_minus_tail_swing_to_principal"])
    positive_values = [
        row["clear_minus_tail_swing_to_principal"]
        for row in positive_rows]
    negative_values = [
        -row["clear_minus_tail_swing_to_principal"]
        for row in negative_rows]
    positive_sum = math.fsum(positive_values)
    negative_sum = -math.fsum(negative_values)
    total_swing = (
        clear["dominant_character_sum_to_principal_ratio"]
        - tail["dominant_character_sum_to_principal_ratio"])
    return {
        "tail_target": tail["target"],
        "clear_target": clear["target"],
        "tail_row": compact_row(tail),
        "clear_row": compact_row(clear),
        "dominant_sum_swing_to_principal": total_swing,
        "slack_swing_to_floor": (
            clear["positive_offset_slack_to_floor"]
            - tail["positive_offset_slack_to_floor"]),
        "negative_pressure_reduction_component": (
            tail["negative_channel_pressure_to_principal"]
            - clear["negative_channel_pressure_to_principal"]),
        "positive_offset_increase_component": (
            clear["positive_channel_offset_to_principal"]
            - tail["positive_channel_offset_to_principal"]),
        "positive_swing_channel_count": len(positive_rows),
        "negative_swing_channel_count": len(negative_rows),
        "positive_swing_sum": positive_sum,
        "negative_swing_sum": negative_sum,
        "net_swing_reconstruction_error": abs(
            positive_sum + negative_sum - total_swing),
        "top1_positive_swing_share": share(positive_values, 1),
        "top3_positive_swing_share": share(positive_values, 3),
        "top5_positive_swing_share": share(positive_values, 5),
        "top1_negative_drag_share": share(negative_values, 1),
        "top3_negative_drag_share": share(negative_values, 3),
        "top5_negative_drag_share": share(negative_values, 5),
        "top_positive_swing_channels": positive_rows[:10],
        "top_negative_drag_channels": negative_rows[:10],
        "channel_swing_rows": swing_rows,
    }


def main():
    receipt = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=SAMPLE_TARGETS,
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=25)
    rows = receipt["target_rows"]
    pair_rows = tuple(
        build_pair(rows[tail], rows[clear])
        for tail, clear in PAIR_TARGETS)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite named-pair channel-swing diagnostic only; no pairwise "
            "recurrence theorem, single-channel swing theorem, coupled "
            "pressure/offset curve theorem, pointwise character-sum estimate, "
            "or Goldbach proof is established"),
        "mechanism": (
            "After scalar offset and global ratio floors were falsified, test "
            "whether tail-to-clear movement near the coupled curve is "
            "explained by one dominant real channel or by a broader signed "
            "multi-channel swing."),
        "falsifier": (
            "If top positive channel swings carry only a minority of helpful "
            "tail-to-clear movement, a one-channel swing theorem is too "
            "narrow for the named pair."),
        "pair_targets": PAIR_TARGETS,
        "sample_targets": SAMPLE_TARGETS,
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "active_real_channel_count": receipt["active_real_channel_count"],
        "dominant_floor_failure_targets": (
            receipt["dominant_floor_failure_targets"]),
        "dominant_floor_pass_targets": receipt["dominant_floor_pass_targets"],
        "pair_rows": pair_rows,
        "maximum_real_channel_identity_error": (
            receipt["maximum_real_channel_identity_error"]),
        "interpretation": {
            "observed_shape": (
                "The named tail-to-clear swings are signed multi-channel "
                "balances.  The largest helpful channel is not enough to "
                "explain the rescue by itself."),
            "remaining_theorem": (
                "The live pressure/offset route remains a coupled aggregate "
                "channel theorem, pressure subregion split, or lower-support "
                "rescue, not a one-channel swing certificate."),
        },
        "dominant_mode_pairwise_channel_swing_measured": True,
        "single_channel_swing_theorem_proved": False,
        "coupled_pressure_offset_curve_proved": False,
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
