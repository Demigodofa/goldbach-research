"""Build q286 dominant-channel swing-pair evidence.

This artifact compares selected deficit-to-clear near-boundary pairs and
decomposes the dominant mode-1/mode-2 swing into exact deltas across the 25
real q286 character channels.
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
    / "q286-first-three-dominant-mode-channel-swing-pairs.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_channel_swing_pair_receipt,
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


def compact_pair(row):
    return {
        "left_target": row["left_target"],
        "right_target": row["right_target"],
        "left_branch_label": row["left_branch_label"],
        "right_branch_label": row["right_branch_label"],
        "left_dominant_sum_to_principal": (
            row["left_dominant_sum_to_principal"]),
        "right_dominant_sum_to_principal": (
            row["right_dominant_sum_to_principal"]),
        "dominant_swing_to_principal": row["dominant_swing_to_principal"],
        "positive_channel_delta_sum": row["positive_channel_delta_sum"],
        "negative_channel_delta_sum": row["negative_channel_delta_sum"],
        "absolute_channel_delta_sum": row["absolute_channel_delta_sum"],
        "signed_to_absolute_delta_ratio": (
            row["signed_to_absolute_delta_ratio"]),
        "top_helpful_channel_share": row["top_helpful_channel_share"],
        "helpful_channel_count": row["helpful_channel_count"],
        "harmful_channel_count": row["harmful_channel_count"],
        "helpful_channel_count_for_50_percent": (
            row["helpful_channel_count_for_50_percent"]),
        "helpful_channel_count_for_80_percent": (
            row["helpful_channel_count_for_80_percent"]),
        "helpful_channel_count_for_90_percent": (
            row["helpful_channel_count_for_90_percent"]),
        "helpful_sums_by_type": row["helpful_sums_by_type"],
        "helpful_counts_by_type": row["helpful_counts_by_type"],
        "top_helpful_channel_rows": row["top_helpful_channel_rows"],
        "top_harmful_channel_rows": row["top_harmful_channel_rows"],
        "swing_reconstruction_error": row["swing_reconstruction_error"],
    }


def main():
    receipt = q286_first_three_dominant_mode_channel_swing_pair_receipt()
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite channel-swing pair diagnostic only; selected "
            "deficit-to-clear pairs are decomposed exactly, but no recurrence "
            "theorem, signed-channel offset theorem, pointwise character-sum "
            "estimate, fixed-modulus AP theorem, signed projection theorem, "
            "or Goldbach proof is established"),
        "pair_selection": {
            "rule": (
                "selected deficit-to-clear pairs from the mass-matched "
                "near-boundary fixture and late holdout rows; includes the "
                "two clear partners for the late deficit 1222142"),
            "not_random": True,
            "not_independent_holdout": True,
        },
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "active_real_channel_count": receipt["active_real_channel_count"],
        "pair_targets": receipt["pair_targets"],
        "sample_targets": receipt["sample_targets"],
        "pair_count": receipt["pair_count"],
        "deficit_to_clear_pair_count": (
            receipt["deficit_to_clear_pair_count"]),
        "pair_rows": tuple(compact_pair(row) for row in receipt["pair_rows"]),
        "channel_frequency_rows": receipt["channel_frequency_rows"],
        "recurrent_helpful_channel_rows": (
            receipt["recurrent_helpful_channel_rows"]),
        "universally_helpful_channel_rows": (
            receipt["universally_helpful_channel_rows"]),
        "minimum_top_helpful_share_row": compact_pair(
            receipt["minimum_top_helpful_share_row"]),
        "maximum_channel_count_for_80_percent_row": compact_pair(
            receipt["maximum_channel_count_for_80_percent_row"]),
        "maximum_swing_reconstruction_error": (
            receipt["maximum_swing_reconstruction_error"]),
        "interpretation": {
            "mechanism_tested": (
                "If offset forcing is low-dimensional, the helpful "
                "clear-minus-deficit channel deltas should concentrate in a "
                "small recurrent set of real q286 channels."),
            "falsifier": (
                "Diffuse pair-specific helpful channels would demote a "
                "tiny-channel offset lemma and keep the theorem target at "
                "full signed-channel structure."),
            "remaining_theorem": (
                "A proof would need an arithmetic reason why the helpful "
                "channel portfolio appears when pressure is high, or a proof "
                "that the unresolved deficits are finite/boundary rows."),
        },
        "dominant_channel_swing_pair_decomposition_measured": True,
        "recurrent_helpful_channels_observed": (
            receipt["recurrent_helpful_channels_observed"]),
        "single_or_two_channel_offset_theorem_demoted_on_samples": (
            receipt[
                "single_or_two_channel_offset_theorem_demoted_on_samples"]),
        "eventual_signed_channel_offset_theorem_proved": False,
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
