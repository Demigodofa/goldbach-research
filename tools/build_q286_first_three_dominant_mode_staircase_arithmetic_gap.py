"""Build q286 dominant-mode staircase arithmetic-gap evidence."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-staircase-arithmetic-gap.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_staircase_arithmetic_gap_receipt,
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
            "pass_actual_position_summary",
            "fail_actual_position_summary",
            "pass_actual_gap_summary",
            "fail_actual_gap_summary",
            "missing_margin_not_supplied_by_weak_geometry_summary",
            "uniform_correct_sign_targets",
            "uniform_correct_sign_count",
            "all_actual_rows_inside_weak_interval",
        )
    }


def main():
    receipt = q286_first_three_dominant_mode_staircase_arithmetic_gap_receipt()
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite arithmetic-gap diagnostic only; it records where actual "
            "prime-pair rows sit inside weak-geometry intervals and proves no "
            "pointwise arithmetic theorem, no tail theorem, and no Goldbach "
            "theorem"),
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
        "full_stage_tightest_fail_row": (
            receipt["full_stage_tightest_fail_row"]),
        "full_stage_widest_missing_geometry_margin_row": (
            receipt["full_stage_widest_missing_geometry_margin_row"]),
        "actual_prime_pair_rows_inside_weak_geometry_intervals": (
            receipt["actual_prime_pair_rows_inside_weak_geometry_intervals"]),
        "interpretation": {
            "mechanism_tested": (
                "Place the actual strict-central prime-pair rows inside the "
                "weak reflected-geometry min/max interval for each staircase "
                "stage."),
            "boundary": (
                "Finite selected arithmetic diagnostic; the one-sided "
                "prime-pair estimates remain unproved."),
            "remaining_theorem": (
                "For pass rows prove a one-sided lower bound for the relevant "
                "stage action; for deficit rows prove a one-sided upper bound "
                "or a replacement deficit-exclusion/complement theorem."),
        },
        "staircase_arithmetic_gap_measured": True,
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
