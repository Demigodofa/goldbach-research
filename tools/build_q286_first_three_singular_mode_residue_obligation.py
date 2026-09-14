"""Build q286 singular-mode residue obligation evidence.

This artifact splits the q286 first-three residue-pair obligation into the
first three singular character modes and records the exact residue-discrepancy
identity for each mode on the current near-boundary samples.

It is theorem-shaping evidence only, not a proof of the needed pointwise
character-sum estimates.
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
    / "q286-first-three-singular-mode-residue-obligation.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_singular_mode_residue_obligation_receipt,
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
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def main():
    receipt = q286_first_three_singular_mode_residue_obligation_receipt(
        sample_targets=(1222142, 1242118, 1240888),
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_contribution_count=6)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "exact q286 singular-mode residue-discrepancy obligations and "
            "finite sample checks only; no pointwise character-sum estimate, "
            "fixed-modulus binary AP theorem, q286 signed-projection theorem, "
            "or Goldbach proof is established"),
        "sample_targets": receipt["sample_targets"],
        "tail_threshold": receipt["tail_threshold"],
        "dominant_modes": receipt["dominant_modes"],
        "rank_three_singular_values": receipt["rank_three_singular_values"],
        "dominant_mode_residue_obligation": (
            receipt["dominant_mode_residue_obligation"]),
        "same_sign_dominant_target_count": (
            receipt["same_sign_dominant_target_count"]),
        "dominant_mode_failure_targets": (
            receipt["dominant_mode_failure_targets"]),
        "maximum_mode_identity_error": (
            receipt["maximum_mode_identity_error"]),
        "maximum_recombined_identity_error": (
            receipt["maximum_recombined_identity_error"]),
        "target_rows": receipt["target_rows"],
        "interpretation": {
            "what_changed": (
                "The prior character-mode narrowing is now expressed as "
                "mode-wise residue-discrepancy identities, so the first two "
                "dominant singular coordinates have exact local residual "
                "ledgers."),
            "sample_fact": (
                "Modes 1 and 2 are same-sign negative on all three samples, "
                "but their combined pressure falls below -0.3 only on tail "
                "1222142; the two clear rows remain above the floor before "
                "mode 3 is added."),
            "next_action": (
                "Attack the two-mode obligation directly: prove a pointwise "
                "lower bound for the combined mode-1/mode-2 residue "
                "projection, or classify the finite/residue conditions under "
                "which the tiny third mode and complement rescue the row."),
        },
        "singular_mode_residue_obligation_formalized": True,
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
