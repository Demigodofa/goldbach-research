"""Build q286 dominant-mode signed-channel branch sample evidence.

This widens the three-row signed-channel profile by reusing deterministic
near-boundary rows from the mass-matched q286 fixture.  It records whether
each row clears the dominant floor by the negative-pressure branch, the
positive-offset branch, both, or neither.
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
    / "q286-first-three-dominant-mode-signed-channel-branch-sample.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_branch_sample_receipt,
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
        "top_negative_real_channels": row["top_negative_real_channels"],
        "top_positive_real_channels": row["top_positive_real_channels"],
    }


def main():
    receipt = (
        q286_first_three_dominant_mode_signed_channel_branch_sample_receipt())
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite signed-channel branch sample only; the exact branch split "
            "classifies selected near-boundary rows but proves no eventual "
            "signed-channel branch theorem, pointwise character-sum estimate, "
            "fixed-modulus AP theorem, signed projection theorem, or Goldbach "
            "proof"),
        "sample_selection": {
            "rule": (
                "five lowest first-three tail rows from the recorded "
                "mass-matched near-boundary decomposition plus their paired "
                "clear rows, followed by the late holdout pair and the "
                "second clear holdout row"),
            "not_random": True,
            "not_independent_holdout": True,
        },
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "sample_targets": receipt["sample_targets"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "active_real_channel_count": receipt["active_real_channel_count"],
        "tested_target_count": receipt["tested_target_count"],
        "tested_targets_with_prime_pairs": (
            receipt["tested_targets_with_prime_pairs"]),
        "dominant_floor_pass_targets": (
            receipt["dominant_floor_pass_targets"]),
        "dominant_floor_failure_targets": (
            receipt["dominant_floor_failure_targets"]),
        "pressure_branch_targets": receipt["pressure_branch_targets"],
        "offset_branch_targets": receipt["offset_branch_targets"],
        "pressure_and_offset_branch_targets": (
            receipt["pressure_and_offset_branch_targets"]),
        "unresolved_deficit_targets": receipt["unresolved_deficit_targets"],
        "branch_counts_by_residue": receipt["branch_counts_by_residue"],
        "maximum_pressure_clear_row": compact_row(
            receipt["maximum_pressure_clear_row"]),
        "minimum_slack_clear_row": compact_row(
            receipt["minimum_slack_clear_row"]),
        "maximum_deficit_row": compact_row(receipt["maximum_deficit_row"]),
        "target_rows": {
            target: compact_row(row)
            for target, row in receipt["target_rows"].items()},
        "maximum_real_channel_identity_error": (
            receipt["maximum_real_channel_identity_error"]),
        "interpretation": {
            "what_changed": (
                "The branch split is no longer only the three original "
                "holdout rows.  It is checked on deterministic near-boundary "
                "tail/clear pairs from the existing mass-matched fixture."),
            "observed_shape": (
                "The sampled clear rows can require the offset branch even "
                "under large negative pressure.  The unresolved rows are true "
                "finite deficits of the same exact branch inequality."),
            "remaining_theorem": (
                "A proof must force either pressure below the floor or enough "
                "positive offset for actual binary-prime character channels. "
                "The receipt does not identify an external theorem proving "
                "that force."),
        },
        "dominant_mode_signed_channel_branch_sample_measured": True,
        "branch_split_exact_on_samples": receipt[
            "branch_split_exact_on_samples"],
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
