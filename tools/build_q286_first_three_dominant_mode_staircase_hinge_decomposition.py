"""Build q286 dominant-mode staircase hinge-decomposition evidence."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-staircase-hinge-decomposition.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_staircase_hinge_decomposition_receipt,
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


def compact_stage(stage):
    return {
        key: stage[key]
        for key in (
            "stage_index",
            "stage_name",
            "stage_role",
            "channel_labels",
            "channel_count",
            "target_rows",
            "hinge_identity_error_summary",
            "classification_supporting_mass_summary",
            "classification_opposing_mass_summary",
            "classification_supporting_hinge_summary",
            "classification_opposing_hinge_summary",
            "classification_mass_driven_targets",
            "classification_landing_driven_targets",
        )
    }


def main():
    receipt = (
        q286_first_three_dominant_mode_staircase_hinge_decomposition_receipt())
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite hinge-decomposition diagnostic only; exact sampled "
            "identities do not prove a hinge-balance theorem, pointwise "
            "arithmetic theorem, or Goldbach theorem"),
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "pair_targets": receipt["pair_targets"],
        "sample_targets": receipt["sample_targets"],
        "portfolio_name": receipt["portfolio_name"],
        "prefix_channel_labels": receipt["prefix_channel_labels"],
        "tail_channel_labels": receipt["tail_channel_labels"],
        "ordered_channel_labels": receipt["ordered_channel_labels"],
        "stage_rows": [
            compact_stage(stage) for stage in receipt["stage_rows"]],
        "prefix_stage": compact_stage(receipt["prefix_stage"]),
        "full_stage": compact_stage(receipt["full_stage"]),
        "full_stage_largest_opposing_mass_row": (
            receipt["full_stage_largest_opposing_mass_row"]),
        "full_stage_largest_supporting_hinge_row": (
            receipt["full_stage_largest_supporting_hinge_row"]),
        "full_stage_smallest_hinge_margin_row": (
            receipt["full_stage_smallest_hinge_margin_row"]),
        "maximum_hinge_identity_error": (
            receipt["maximum_hinge_identity_error"]),
        "interpretation": {
            "mechanism_tested": (
                "Decompose the selected q286 staircase slack into actual "
                "mass above the row floor times positive landing quality, "
                "minus actual mass below the row floor times negative landing "
                "quality."),
            "boundary": (
                "Finite selected-fixture identity and profile only."),
            "remaining_theorem": (
                "Prove a hinge-balance inequality for actual prime-pair mass "
                "and row-dependent action levels, or replace it with a "
                "stronger signed aggregate, complement, or fixed-modulus "
                "prime-pair theorem."),
        },
        "hinge_decomposition_measured": True,
        "hinge_balance_theorem_proved": False,
        "orbit_mass_theorem_proved": False,
        "arithmetic_gap_theorem_proved": False,
        "prefix_lower_bound_theorem_proved": False,
        "tail_classification_theorem_proved": False,
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
