"""Build q286 dominant-mode character-sum obligation evidence.

This artifact rewrites the surviving dominant singular mode-1/mode-2 q286
first-three residual as exact fixed-modulus character channels.  It is a
theorem-obligation receipt only, not a pointwise character-sum estimate.
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
    / "q286-first-three-dominant-mode-character-sum-obligation.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_character_sum_obligation_receipt,
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
    receipt = q286_first_three_dominant_mode_character_sum_obligation_receipt(
        sample_targets=(1222142, 1242118, 1240888),
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=6)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "exact q286 dominant-mode character-sum obligation and finite "
            "sample checks only; no pointwise character-sum estimate, "
            "fixed-modulus AP theorem, q286 signed-projection theorem, or "
            "Goldbach proof is established"),
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "dominant_singular_values": receipt["dominant_singular_values"],
        "active_complex_character_count": (
            receipt["active_complex_character_count"]),
        "active_real_channel_count": receipt["active_real_channel_count"],
        "active_self_conjugate_channel_count": (
            receipt["active_self_conjugate_channel_count"]),
        "dominant_character_coefficient_l1_to_principal_mean": (
            receipt["dominant_character_coefficient_l1_to_principal_mean"]),
        "dominant_character_coefficient_l2_to_principal_mean": (
            receipt["dominant_character_coefficient_l2_to_principal_mean"]),
        "dominant_character_coefficient_linf_to_principal_mean": (
            receipt["dominant_character_coefficient_linf_to_principal_mean"]),
        "dominant_real_channel_l1_to_principal_mean": (
            receipt["dominant_real_channel_l1_to_principal_mean"]),
        "dominant_real_channel_l2_to_principal_mean": (
            receipt["dominant_real_channel_l2_to_principal_mean"]),
        "maximum_conjugate_coefficient_error": (
            receipt["maximum_conjugate_coefficient_error"]),
        "maximum_complex_character_identity_error": (
            receipt["maximum_complex_character_identity_error"]),
        "maximum_real_channel_identity_error": (
            receipt["maximum_real_channel_identity_error"]),
        "real_channel_rows": receipt["real_channel_rows"],
        "target_rows": receipt["target_rows"],
        "interpretation": {
            "what_changed": (
                "After support/reflection geometry was obstructed, the "
                "dominant mode-1/mode-2 residual is now an exact q286 "
                "character-sum obligation with 50 active complex characters "
                "collapsing to 25 real conjugacy channels."),
            "sample_fact": (
                "The character-channel identity reproduces the residue "
                "obligation on 1222142, 1242118, and 1240888; the tail row "
                "is below -0.3 while the two near-clear rows remain above it."),
            "next_action": (
                "Seek pointwise control of these 25 real channels, a stronger "
                "arithmetic residue-weight constraint, or a theorem showing "
                "that complement/lower-support terms rescue the remaining "
                "dominant-mode deficits."),
        },
        "dominant_mode_character_sum_obligation": (
            receipt["dominant_mode_character_sum_obligation"]),
        "dominant_mode_character_sum_obligation_formalized": True,
        "single_character_or_tiny_channel_proof_found": (
            receipt["single_character_or_tiny_channel_proof_found"]),
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
