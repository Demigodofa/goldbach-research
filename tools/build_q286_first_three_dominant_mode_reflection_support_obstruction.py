"""Build q286 dominant-mode reflection-support obstruction evidence.

This artifact tests whether the first two singular q286 first-three modes can
be bounded from support, nonnegativity, total mass, and ordered prime-pair
reflection symmetry alone.  It is finite-vector obstruction evidence only.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-reflection-support-obstruction.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_reflection_support_obstruction_receipt,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main():
    receipt = (
        q286_first_three_dominant_mode_reflection_support_obstruction_receipt(
            dominant_modes=(1, 2), tail_threshold=.3, slack_factor=1.25))
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite-vector obstruction only; refutes a support/"
            "nonnegativity/total/reflection-only proof of the dominant "
            "mode-1/mode-2 lower bound, not arithmetic q286 rarity, not a "
            "pointwise character-sum estimate, and not Goldbach"),
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "slack_factor": receipt["slack_factor"],
        "even_target_residue_count": receipt["even_target_residue_count"],
        "obstructed_even_target_residue_count": (
            receipt["obstructed_even_target_residue_count"]),
        "positive_witness_even_target_residue_count": (
            receipt["positive_witness_even_target_residue_count"]),
        "all_even_target_residues_have_positive_reflection_witness": (
            receipt[
                "all_even_target_residues_have_positive_reflection_witness"]),
        "worst_extremal_row": receipt["worst_extremal_row"],
        "least_negative_extremal_row": (
            receipt["least_negative_extremal_row"]),
        "least_negative_positive_witness_row": (
            receipt["least_negative_positive_witness_row"]),
        "maximum_reflection_weight_error": (
            receipt["maximum_reflection_weight_error"]),
        "maximum_constructed_reconstruction_error": (
            receipt["maximum_constructed_reconstruction_error"]),
        "interpretation": {
            "changed_under_evidence": (
                "After throwing away mode 3 and keeping only singular modes "
                "1 and 2, every even target residue modulo 286 still admits a "
                "strictly positive reflected synthetic support weight with "
                "dominant mode sum below -0.3."),
            "remaining_theorem": (
                "The dominant two-mode projection needs actual prime-pair "
                "arithmetic, a stronger structural constraint than reflection "
                "symmetry, complement/lower-support rescue, or a fixed-modulus "
                "binary-prime character-sum input."),
        },
        "dominant_mode_reflection_support_obstruction_measured": True,
        "support_reflection_dominant_mode_theorem_refuted": (
            receipt["support_reflection_dominant_mode_theorem_refuted"]),
        "pointwise_character_sum_estimate_proved": False,
        "fixed_modulus_binary_ap_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
