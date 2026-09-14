"""Build q286 dominant-mode signed channel profile evidence.

This artifact records the positive/negative contribution ledger across the
25 real dominant mode-1/mode-2 q286 character channels.  It is finite
theorem-shaping evidence only.
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
    / "q286-first-three-dominant-mode-signed-channel-profile.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
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


def main():
    receipt = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=(1222142, 1242118, 1240888),
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=6)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite signed-channel profile only; records exact positive and "
            "negative channel contribution ledgers on selected samples.  It "
            "proves no signed channel cancellation theorem, pointwise "
            "character-sum estimate, fixed-modulus AP theorem, q286 "
            "signed-projection theorem, or Goldbach proof."),
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "sample_targets": receipt["sample_targets"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "active_real_channel_count": receipt["active_real_channel_count"],
        "dominant_floor_failure_targets": (
            receipt["dominant_floor_failure_targets"]),
        "dominant_floor_pass_targets": receipt["dominant_floor_pass_targets"],
        "maximum_negative_pressure_row": (
            receipt["maximum_negative_pressure_row"]),
        "minimum_positive_offset_slack_row": (
            receipt["minimum_positive_offset_slack_row"]),
        "minimum_signed_to_absolute_real_channel_row": (
            receipt["minimum_signed_to_absolute_real_channel_row"]),
        "maximum_real_channel_identity_error": (
            receipt["maximum_real_channel_identity_error"]),
        "target_rows": receipt["target_rows"],
        "interpretation": {
            "what_changed": (
                "The active samples now split into an exact signed ledger "
                "over 25 real channels instead of only norm budgets."),
            "sample_fact": (
                "Tail 1222142 has the largest negative channel pressure and "
                "insufficient positive offset.  Clear 1242118 has enough "
                "positive offset against its negative pressure, while clear "
                "1240888 clears mostly because its negative pressure is below "
                "the 0.3 floor even with little positive offset."),
            "route_effect": (
                "The next theorem target should control signed channel "
                "balance or negative-pressure regimes, not just independent "
                "channel size."),
        },
        "dominant_mode_signed_channel_profile_measured": True,
        "signed_channel_cancellation_theorem_proved": False,
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
