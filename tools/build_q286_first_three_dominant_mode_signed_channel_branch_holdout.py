"""Build q286 dominant-mode signed-channel branch holdout evidence.

This applies the exact branch split from the selected near-boundary sample to
the next nonoverlapping deterministic target window after the recorded
1242000 stress neighborhood.  It is denominator evidence for the branch
mechanism, not a proof of the eventual branch theorem.
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
    / "q286-first-three-dominant-mode-signed-channel-branch-holdout.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_branch_holdout_receipt,
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
        "dominant_floor_pass_targets": summary["dominant_floor_pass_targets"],
        "dominant_floor_failure_targets": (
            summary["dominant_floor_failure_targets"]),
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
            windows=((1243000, 101),)))
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite deterministic signed-channel branch holdout only; the "
            "unchanged branch split is checked on a fresh target window but "
            "no eventual signed-channel branch theorem, pointwise "
            "character-sum estimate, fixed-modulus AP theorem, signed "
            "projection theorem, or Goldbach proof is established"),
        "sample_selection": {
            "rule": (
                "next nonoverlapping 101 even-target window after the "
                "recorded 1242000 stress-neighborhood window"),
            "windows": receipt["windows"],
            "not_random": True,
            "not_proof_denominator": True,
        },
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
        "dominant_floor_failure_targets": (
            receipt["dominant_floor_failure_targets"]),
        "pressure_branch_target_count": len(
            receipt["pressure_branch_targets"]),
        "offset_branch_target_count": len(receipt["offset_branch_targets"]),
        "pressure_and_offset_branch_target_count": len(
            receipt["pressure_and_offset_branch_targets"]),
        "unresolved_deficit_target_count": len(
            receipt["unresolved_deficit_targets"]),
        "unresolved_deficit_targets": receipt["unresolved_deficit_targets"],
        "all_holdout_targets_pass_dominant_floor": (
            receipt["all_holdout_targets_pass_dominant_floor"]),
        "all_holdout_targets_clear_by_both_branches": (
            receipt["all_holdout_targets_clear_by_both_branches"]),
        "exact_branch_floor_mismatch_targets": (
            receipt["exact_branch_floor_mismatch_targets"]),
        "window_summaries": [
            compact_window_summary(summary)
            for summary in receipt["window_summaries"]],
        "minimum_slack_clear_row": compact_row(
            receipt["window_summaries"][0]["minimum_slack_clear_row"]),
        "maximum_pressure_clear_row": compact_row(
            receipt["window_summaries"][0]["maximum_pressure_clear_row"]),
        "target_rows": {
            target: compact_row(row)
            for target, row in receipt["target_rows"].items()},
        "maximum_real_channel_identity_error": (
            receipt["maximum_real_channel_identity_error"]),
        "interpretation": {
            "what_changed": (
                "The exact pressure-or-offset branch split is no longer only "
                "a selected near-boundary sample; it is applied unchanged to "
                "the next deterministic target window."),
            "observed_shape": (
                "Every checked target in this fresh window clears both the "
                "negative-pressure branch and the positive-offset branch.  "
                "No new unresolved deficit row is found."),
            "remaining_theorem": (
                "This is denominator evidence for the branch mechanism.  A "
                "proof still needs an arithmetic estimate forcing the branch "
                "condition, or a classification/rescue of all true deficits."),
        },
        "dominant_mode_signed_channel_branch_holdout_measured": True,
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
