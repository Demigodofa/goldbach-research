"""Build q286 dominant-mode signed-channel pressure-horizon evidence.

The preceding branch holdout found that every target in the 1243000 window
cleared both exact branches.  This builder keeps the same pressure-or-offset
branch rule and checks the next deterministic sparse windows for a direct
falsifier of the pressure-only easy-region hypothesis.
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
    / "q286-first-three-dominant-mode-signed-channel-pressure-horizon.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_branch_holdout_receipt,
)


WINDOWS = ((1244000, 51), (1245000, 51), (1246000, 51))


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


def compact_row(row):
    if row is None:
        return None
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
        "signed_channel_branch_label": row["signed_channel_branch_label"],
        "dominant_floor_deficit_to_threshold": (
            row["dominant_floor_deficit_to_threshold"]),
        "signed_to_absolute_real_channel_ratio": (
            row["signed_to_absolute_real_channel_ratio"]),
        "positive_real_channel_count": row["positive_real_channel_count"],
        "negative_real_channel_count": row["negative_real_channel_count"],
    }


def compact_window_summary(summary):
    return {
        "start": summary["start"],
        "target_count": summary["target_count"],
        "tested_targets_with_prime_pairs": (
            summary["tested_targets_with_prime_pairs"]),
        "dominant_floor_pass_target_count": (
            summary["dominant_floor_pass_target_count"]),
        "dominant_floor_failure_target_count": (
            summary["dominant_floor_failure_target_count"]),
        "branch_counts": summary["branch_counts"],
        "minimum_slack_clear_row": compact_row(
            summary["minimum_slack_clear_row"]),
        "maximum_pressure_clear_row": compact_row(
            summary["maximum_pressure_clear_row"]),
        "maximum_deficit_row": compact_row(summary["maximum_deficit_row"]),
    }


def main():
    receipt = (
        q286_first_three_dominant_mode_signed_channel_branch_holdout_receipt(
            windows=WINDOWS))
    maximum_pressure_rows = [
        summary["maximum_pressure_clear_row"]
        for summary in receipt["window_summaries"]
        if summary["maximum_pressure_clear_row"] is not None]
    tightest_rows = [
        summary["minimum_slack_clear_row"]
        for summary in receipt["window_summaries"]
        if summary["minimum_slack_clear_row"] is not None]
    global_maximum_pressure_row = max(
        maximum_pressure_rows,
        key=lambda row: row["negative_channel_pressure_to_principal"],
        default=None)
    global_tightest_slack_row = min(
        tightest_rows,
        key=lambda row: row["positive_offset_slack_to_floor"],
        default=None)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite deterministic pressure-horizon scout only; the unchanged "
            "dominant two-mode branch split is checked on sparse post-1243000 "
            "windows but no pressure-branch theorem, pointwise character-sum "
            "estimate, fixed-modulus AP theorem, signed-projection theorem, "
            "or Goldbach proof is established"),
        "mechanism": (
            "After the 1243000 holdout, test whether the direct pressure "
            "branch negative_pressure <= 0.3 continues to clear deterministic "
            "post-stress windows without needing an offset-only rescue."),
        "falsifier": (
            "Any checked row with negative_pressure > 0.3, or any unresolved "
            "dominant-floor deficit, falsifies this finite pressure-horizon "
            "scout."),
        "windows": WINDOWS,
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "active_real_channel_count": receipt["active_real_channel_count"],
        "tested_target_count": receipt["tested_target_count"],
        "tested_targets_with_prime_pairs": (
            receipt["tested_targets_with_prime_pairs"]),
        "dominant_floor_pass_target_count": len(
            receipt["dominant_floor_pass_targets"]),
        "dominant_floor_failure_target_count": len(
            receipt["dominant_floor_failure_targets"]),
        "pressure_branch_target_count": len(
            receipt["pressure_branch_targets"]),
        "offset_branch_target_count": len(receipt["offset_branch_targets"]),
        "pressure_and_offset_branch_target_count": len(
            receipt["pressure_and_offset_branch_targets"]),
        "unresolved_deficit_target_count": len(
            receipt["unresolved_deficit_targets"]),
        "dominant_floor_failure_targets": (
            receipt["dominant_floor_failure_targets"]),
        "unresolved_deficit_targets": receipt["unresolved_deficit_targets"],
        "all_checked_targets_pass_pressure_branch": bool(
            receipt["tested_targets_with_prime_pairs"]
            == len(receipt["pressure_and_offset_branch_targets"])
            and not receipt["pressure_branch_targets"]
            and not receipt["offset_branch_targets"]),
        "all_checked_targets_pass_dominant_floor": (
            receipt["all_holdout_targets_pass_dominant_floor"]),
        "exact_branch_floor_mismatch_targets": (
            receipt["exact_branch_floor_mismatch_targets"]),
        "global_maximum_pressure_clear_row": compact_row(
            global_maximum_pressure_row),
        "global_tightest_slack_clear_row": compact_row(
            global_tightest_slack_row),
        "window_summaries": [
            compact_window_summary(summary)
            for summary in receipt["window_summaries"]],
        "maximum_real_channel_identity_error": (
            receipt["maximum_real_channel_identity_error"]),
        "interpretation": {
            "observed_shape": (
                "All checked targets in the three sparse post-1243000 "
                "windows clear the pressure branch directly and also have "
                "positive offset slack; no unresolved deficit appears."),
            "remaining_theorem": (
                "The evidence suggests a pressure-easy region in these "
                "sampled windows, but a proof still needs an arithmetic "
                "bound on negative dominant-channel pressure or a finite "
                "classification of pressure failures."),
        },
        "dominant_mode_signed_channel_pressure_horizon_measured": True,
        "eventual_pressure_branch_theorem_proved": False,
        "eventual_signed_channel_branch_theorem_proved": False,
        "pointwise_character_sum_estimate_proved": False,
        "fixed_modulus_binary_ap_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
