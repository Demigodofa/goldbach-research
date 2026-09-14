"""Build q286 dominant-mode above-floor threshold evidence."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-staircase-above-floor-threshold.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_staircase_above_floor_threshold_receipt,
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
            "above_floor_signed_surplus_summary",
            "above_floor_pass_surplus_summary",
            "above_floor_deficit_surplus_summary",
            "above_floor_threshold_identity_error_summary",
            "above_floor_threshold_sign_error_targets",
            "above_floor_threshold_sign_error_count",
            "above_floor_threshold_classifies_selected_rows",
        )
    }


def main():
    receipt = (
        q286_first_three_dominant_mode_staircase_above_floor_threshold_receipt())
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite above-floor threshold formulation only; it records an "
            "exact selected-fixture sign obligation and proves no threshold "
            "theorem, signed prime-correlation theorem, or Goldbach theorem"),
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
        "full_stage_tightest_pass_row": (
            receipt["full_stage_tightest_pass_row"]),
        "full_stage_tightest_deficit_row": (
            receipt["full_stage_tightest_deficit_row"]),
        "full_stage_smallest_absolute_surplus_row": (
            receipt["full_stage_smallest_absolute_surplus_row"]),
        "maximum_above_floor_threshold_identity_error": (
            receipt["maximum_above_floor_threshold_identity_error"]),
        "maximum_stage_sign_error_count": (
            receipt["maximum_stage_sign_error_count"]),
        "interpretation": {
            "mechanism_tested": (
                "Use the arithmetically defined above-floor orbit side, not "
                "the post-hoc classification-supporting side, and measure the "
                "signed surplus over the below-landing threshold."),
            "boundary": (
                "Finite selected-fixture sign formulation only.  Some "
                "intermediate stages may be degenerate or fail to match final "
                "classification; the full stage is the active theorem target."),
            "remaining_theorem": (
                "Prove the sign of the above-floor threshold surplus for the "
                "full q286 dominant staircase, or replace it with a signed "
                "aggregate, complement, or fixed-modulus prime-pair theorem."),
        },
        "above_floor_threshold_obligation_measured": True,
        "above_floor_threshold_theorem_proved": False,
        "hinge_threshold_theorem_proved": False,
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
