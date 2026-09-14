"""Build q286 dominant-mode tail ablation evidence."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-tail-ablation.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_tail_ablation_receipt,
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


def compact_leave_one_out(row):
    return {
        key: row[key]
        for key in (
            "removed_label",
            "remaining_channel_count",
            "all_overrescued_failures_restored",
            "all_original_clears_preserved",
            "matches_full_tail_classification",
            "minimum_clear_slack",
            "maximum_failure_slack",
        )
    }


def compact_tail_prefix(row):
    return {
        key: row[key]
        for key in (
            "tail_prefix_channel_count",
            "tail_prefix_channel_labels",
            "all_overrescued_failures_restored",
            "all_original_clears_preserved",
            "matches_full_tail_classification",
            "minimum_clear_slack",
            "maximum_failure_slack",
        )
    }


def main():
    receipt = q286_first_three_dominant_mode_tail_ablation_receipt()
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite tail ablation only; it tests selected q286 rows and "
            "proves no tail classification theorem, no fixed-modulus AP "
            "theorem, and no Goldbach theorem"),
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
        "full_tail_rows": receipt["full_tail_rows"],
        "full_tail_clear_slack_summary": (
            receipt["full_tail_clear_slack_summary"]),
        "full_tail_failure_slack_summary": (
            receipt["full_tail_failure_slack_summary"]),
        "channel_rows": receipt["channel_rows"],
        "leave_one_out_rows": [
            compact_leave_one_out(row)
            for row in receipt["leave_one_out_rows"]],
        "restoration_essential_channel_labels": (
            receipt["restoration_essential_channel_labels"]),
        "classification_essential_channel_labels": (
            receipt["classification_essential_channel_labels"]),
        "restoration_essential_channel_count": (
            receipt["restoration_essential_channel_count"]),
        "classification_essential_channel_count": (
            receipt["classification_essential_channel_count"]),
        "tail_prefix_rows": [
            compact_tail_prefix(row)
            for row in receipt["tail_prefix_rows"]],
        "first_tail_prefix_restoring_failures": (
            compact_tail_prefix(
                receipt["first_tail_prefix_restoring_failures"])
            if receipt["first_tail_prefix_restoring_failures"] else None),
        "first_tail_prefix_matching_classification": (
            compact_tail_prefix(
                receipt["first_tail_prefix_matching_classification"])
            if receipt["first_tail_prefix_matching_classification"] else None),
        "all_leave_one_out_restore_failures": (
            receipt["all_leave_one_out_restore_failures"]),
        "all_leave_one_out_match_classification": (
            receipt["all_leave_one_out_match_classification"]),
        "interpretation": {
            "mechanism_tested": (
                "Ablate the classification tail left after the clear-side "
                "prefix and test whether a proper subtail still restores "
                "overrescued deficits while preserving clears."),
            "boundary": (
                "Finite selected-tail bookkeeping only; no uniform tail "
                "classification theorem is proved."),
            "remaining_theorem": (
                "Prove the required tail classification or replace it with a "
                "separate deficit exclusion/complement mechanism."),
        },
        "tail_ablation_measured": True,
        "proper_subtail_classification_theorem_proved": False,
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
