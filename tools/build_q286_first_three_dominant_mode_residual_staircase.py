"""Build q286 dominant-mode residual staircase evidence."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-residual-staircase.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_residual_staircase_receipt,
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
            "added_channel_label",
            "target_rows",
            "stage_pass_targets",
            "underrescued_clear_targets",
            "overrescued_failure_targets",
            "underrescued_clear_count",
            "overrescued_failure_count",
            "all_original_clears_pass",
            "no_original_failures_overrescued",
            "matches_full_dominant_floor_classification",
            "clear_slack_summary",
            "failure_slack_summary",
            "positive_remaining_requirement_summary",
            "worst_remaining_requirement_row",
            "tightest_stage_pass_row",
        )
    }


def main():
    receipt = q286_first_three_dominant_mode_residual_staircase_receipt()
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite residual staircase only; it tests selected q286 rows and "
            "proves no prefix lower-bound theorem, no tail classification "
            "theorem, no fixed-modulus AP theorem, and no Goldbach theorem"),
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "active_real_channel_count": receipt["active_real_channel_count"],
        "pair_targets": receipt["pair_targets"],
        "sample_targets": receipt["sample_targets"],
        "portfolio_name": receipt["portfolio_name"],
        "prefix_channel_labels": receipt["prefix_channel_labels"],
        "prefix_channel_count": receipt["prefix_channel_count"],
        "tail_channel_labels": receipt["tail_channel_labels"],
        "tail_channel_count": receipt["tail_channel_count"],
        "ordered_channel_labels": receipt["ordered_channel_labels"],
        "ordered_channel_count": receipt["ordered_channel_count"],
        "target_base_rows": receipt["target_base_rows"],
        "stage_rows": [
            compact_stage(stage) for stage in receipt["stage_rows"]],
        "added_channel_rows": receipt["added_channel_rows"],
        "prefix_stage": compact_stage(receipt["prefix_stage"]),
        "full_stage": compact_stage(receipt["full_stage"]),
        "first_stage_clearing_all_original_clears": compact_stage(
            receipt["first_stage_clearing_all_original_clears"]),
        "first_stage_eliminating_overrescued_failures": compact_stage(
            receipt["first_stage_eliminating_overrescued_failures"]),
        "first_stage_matching_classification": compact_stage(
            receipt["first_stage_matching_classification"]),
        "interpretation": {
            "mechanism_tested": (
                "Freeze the selected prefix/tail channel order and ask, "
                "after each cumulative bolt-on, which rows remain below the "
                "dominant-mode floor and by how much."),
            "boundary": (
                "Finite selected-fixture bookkeeping only; no uniform "
                "portfolio, tail, or binary-prime residue theorem is proved."),
            "remaining_theorem": (
                "Prove a prefix lower bound for true clear rows and prove "
                "tail/exclusion/complement control for prefix-overrescued "
                "deficits, or replace those with a fixed-modulus prime-pair "
                "correlation theorem."),
        },
        "residual_staircase_measured": True,
        "prefix_lower_bound_theorem_proved": False,
        "tail_classification_theorem_proved": False,
        "fixed_portfolio_lower_bound_theorem_proved": False,
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
