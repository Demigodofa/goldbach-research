"""Build q286 dominant-mode staircase geometry-obstruction evidence."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-staircase-geometry-obstruction.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_staircase_geometry_obstruction_receipt,
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
            "pass_targets_breakable_by_weak_geometry",
            "fail_targets_breakable_by_weak_geometry",
            "geometry_forced_classification_targets",
            "all_selected_classifications_forced_by_geometry",
            "any_selected_classification_forced_by_geometry",
        )
    }


def main():
    receipt = (
        q286_first_three_dominant_mode_staircase_geometry_obstruction_receipt())
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite weak-geometry obstruction only; synthetic reflected "
            "weights are not prime-pair weights and prove no prefix theorem, "
            "tail theorem, fixed-modulus AP theorem, or Goldbach theorem"),
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
        "full_stage_pass_targets_breakable_by_weak_geometry": (
            receipt["full_stage_pass_targets_breakable_by_weak_geometry"]),
        "full_stage_fail_targets_breakable_by_weak_geometry": (
            receipt["full_stage_fail_targets_breakable_by_weak_geometry"]),
        "full_stage_classification_forced_targets": (
            receipt["full_stage_classification_forced_targets"]),
        "full_stage_all_classifications_forced_by_geometry": (
            receipt["full_stage_all_classifications_forced_by_geometry"]),
        "full_stage_any_classification_forced_by_geometry": (
            receipt["full_stage_any_classification_forced_by_geometry"]),
        "prefix_stage_all_clear_passes_forced_by_geometry": (
            receipt["prefix_stage_all_clear_passes_forced_by_geometry"]),
        "interpretation": {
            "mechanism_tested": (
                "For each staircase stage, minimize and maximize the "
                "partial-channel action over nonnegative reflected weights "
                "with the same local admissible q286 support and total mass."),
            "boundary": (
                "Weak support/nonnegativity/total/reflection geometry only; "
                "does not model actual prime-pair arithmetic."),
            "remaining_theorem": (
                "Use actual binary-prime residue arithmetic, stronger "
                "residue-weight constraints, complement/lower-support rescue, "
                "or an external fixed-modulus theorem."),
        },
        "staircase_geometry_obstruction_measured": True,
        "support_nonnegativity_total_reflection_suffices_for_staircase": (
            receipt[
                "support_nonnegativity_total_reflection_suffices_for_staircase"]),
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
