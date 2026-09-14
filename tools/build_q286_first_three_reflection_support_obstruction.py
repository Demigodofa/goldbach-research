"""Build the q286 first-three reflection-support obstruction evidence file.

This records a finite-vector obstruction for the active-selector rarity route:
support, nonnegativity, total mass, and prime-pair reflection symmetry do not
force the q286 first-three term above the active `.3` threshold.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-first-three-reflection-support-obstruction.json"
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_reflection_support_obstruction_receipt,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main():
    receipt = q286_first_three_reflection_support_obstruction_receipt(
        tail_threshold=.3, slack_factor=1.25)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite-vector obstruction only; this refutes a support/"
            "nonnegativity/total/reflection-only rarity proof, not "
            "arithmetic q286 rarity and not Goldbach"),
        "tail_threshold": receipt["tail_threshold"],
        "slack_factor": receipt["slack_factor"],
        "arithmetic_modulus": receipt["arithmetic_modulus"],
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
                "The active-selector rarity proof cannot be obtained from "
                "q286 support, nonnegativity, total mass, and ordered "
                "prime-pair reflection symmetry alone.  Every even target "
                "residue modulo 286 admits a strictly positive reflected "
                "synthetic weight vector with first_three < -0.3."),
            "remaining_theorem": (
                "A successful rarity proof must use arithmetic distribution "
                "of binary prime-pair residue weights, a stronger structural "
                "constraint, or a finite-boundary plus pointwise discrepancy "
                "estimate."),
        },
        "first_three_reflection_support_obstruction_measured": True,
        "support_reflection_rarity_theorem_refuted": (
            receipt["support_reflection_rarity_theorem_refuted"]),
        "eventual_first_three_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
