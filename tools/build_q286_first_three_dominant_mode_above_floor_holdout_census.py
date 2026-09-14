"""Build q286 dominant-mode above-floor holdout census evidence."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-above-floor-holdout-census.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_above_floor_holdout_census_receipt,
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
    receipt = (
        q286_first_three_dominant_mode_above_floor_holdout_census_receipt())
    stress_starts = (1220000, 1221000, 1222000, 1240000, 1242000)
    stress_receipts = tuple(
        q286_first_three_dominant_mode_above_floor_holdout_census_receipt(
            start=start, target_count=101, closest_count=5)
        for start in stress_starts)

    def compact_census(item):
        return {
            "start": item["start"],
            "target_count": item["target_count"],
            "target_step": item["target_step"],
            "evaluated_target_count": item["evaluated_target_count"],
            "dominant_floor_pass_count": item["dominant_floor_pass_count"],
            "dominant_floor_deficit_count": (
                item["dominant_floor_deficit_count"]),
            "above_floor_signed_surplus_summary": (
                item["above_floor_signed_surplus_summary"]),
            "absolute_above_floor_signed_surplus_summary": (
                item["absolute_above_floor_signed_surplus_summary"]),
            "margin_band_counts": item["margin_band_counts"],
            "closest_margin_rows": item["closest_margin_rows"],
            "most_negative_surplus_rows": item[
                "most_negative_surplus_rows"],
            "maximum_above_floor_threshold_identity_error": (
                item["maximum_above_floor_threshold_identity_error"]),
        }

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite holdout census for the frozen q286 dominant-mode "
            "above-floor threshold margin; not a uniform margin theorem, "
            "signed prime-correlation theorem, or Goldbach proof"),
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "start": receipt["start"],
        "target_count": receipt["target_count"],
        "target_step": receipt["target_step"],
        "evaluated_target_count": receipt["evaluated_target_count"],
        "skipped_targets": receipt["skipped_targets"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "ordered_channel_labels": receipt["ordered_channel_labels"],
        "ordered_channel_count": receipt["ordered_channel_count"],
        "active_real_channel_count": receipt["active_real_channel_count"],
        "residual_channel_count": receipt["residual_channel_count"],
        "above_floor_signed_surplus_summary": (
            receipt["above_floor_signed_surplus_summary"]),
        "above_floor_pass_surplus_summary": (
            receipt["above_floor_pass_surplus_summary"]),
        "above_floor_deficit_surplus_summary": (
            receipt["above_floor_deficit_surplus_summary"]),
        "absolute_above_floor_signed_surplus_summary": (
            receipt["absolute_above_floor_signed_surplus_summary"]),
        "dominant_sum_summary": receipt["dominant_sum_summary"],
        "nonportfolio_residual_sum_summary": (
            receipt["nonportfolio_residual_sum_summary"]),
        "above_floor_threshold_identity_error_summary": (
            receipt["above_floor_threshold_identity_error_summary"]),
        "maximum_above_floor_threshold_identity_error": (
            receipt["maximum_above_floor_threshold_identity_error"]),
        "dominant_floor_pass_count": receipt["dominant_floor_pass_count"],
        "dominant_floor_deficit_count": (
            receipt["dominant_floor_deficit_count"]),
        "margin_band_counts": receipt["margin_band_counts"],
        "closest_margin_rows": receipt["closest_margin_rows"],
        "most_negative_surplus_rows": receipt["most_negative_surplus_rows"],
        "most_positive_surplus_rows": receipt["most_positive_surplus_rows"],
        "residue_bucket_rows_by_closest_margin": (
            receipt["residue_bucket_rows_by_closest_margin"]),
        "primary_holdout_census": compact_census(receipt),
        "stress_neighborhood_censuses": [
            compact_census(item) for item in stress_receipts],
        "interpretation": {
            "mechanism_tested": (
                "Freeze the eleven-channel q286 dominant-mode staircase from "
                "the selected stress fixture and apply it unchanged to a "
                "fresh contiguous holdout block."),
            "prediction": (
                "If a useful margin theorem is nearby, the census should show "
                "structured, non-tiny above-floor threshold surplus rather "
                "than arbitrary near-zero residual hits."),
            "falsifier": (
                "Fresh near-zero rows or alternating signs in the holdout "
                "block refute any comfortable uniform surplus gap for the "
                "frozen portfolio and force a sharper arithmetic condition."),
            "boundary": (
                "The threshold sign still reconstructs the fixed-stage slack "
                "algebraically.  The evidence is the finite holdout margin "
                "distribution, not an independent proof of the sign."),
            "stress_neighborhood_boundary": (
                "The secondary windows are deterministic stress-neighborhood "
                "comparisons.  They are not all independent holdouts because "
                "some include previously selected near-boundary targets."),
        },
        "holdout_census_measured": True,
        "frozen_portfolio_uniform_margin_theorem_proved": False,
        "above_floor_threshold_theorem_proved": False,
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
