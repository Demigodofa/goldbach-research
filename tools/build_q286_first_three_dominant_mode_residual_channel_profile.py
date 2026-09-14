"""Build q286 dominant-mode residual-channel profile evidence.

This artifact looks inside the nonportfolio residual left after the recurrent
helpful-channel portfolio is bolted onto the selected q286 dominant rows.
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
    / "q286-first-three-dominant-mode-residual-channel-profile.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_residual_channel_profile_receipt,
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


def compact_target_rows(rows):
    return {
        target: {
            "target": row["target"],
            "target_mod_286": row["target_mod_286"],
            "branch_label": row["branch_label"],
            "dominant_floor_passes": row["dominant_floor_passes"],
            "dominant_sum_to_principal": row[
                "dominant_sum_to_principal"],
            "residual_sum_to_principal": row[
                "residual_sum_to_principal"],
            "residual_positive_offset_to_principal": row[
                "residual_positive_offset_to_principal"],
            "residual_negative_pressure_to_principal": row[
                "residual_negative_pressure_to_principal"],
            "top_residual_channel_rows": row[
                "top_residual_channel_rows"],
        }
        for target, row in rows.items()
    }


def compact_channel(row):
    return {
        "representative_label": row["representative_label"],
        "absolute_contribution_sum": row["absolute_contribution_sum"],
        "failure_summary": row["failure_summary"],
        "clear_summary": row["clear_summary"],
        "clear_minus_failure_mean": row[
            "clear_minus_failure_mean"],
        "positive_targets": row["positive_targets"],
        "negative_targets": row["negative_targets"],
        "maximum_abs_row": row["maximum_abs_row"],
        "clear_min_exceeds_failure_max": (
            row["clear_min_exceeds_failure_max"]),
        "failure_min_exceeds_clear_max": (
            row["failure_min_exceeds_clear_max"]),
    }


def main():
    receipt = q286_first_three_dominant_mode_residual_channel_profile_receipt()
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite residual-channel profile only; it profiles the selected "
            "q286 residual channels after subtracting the recurrent helpful "
            "portfolio, but proves no residual-channel theorem, no portfolio "
            "lower-bound theorem, no fixed-modulus AP theorem, and no "
            "Goldbach theorem"),
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "active_real_channel_count": receipt["active_real_channel_count"],
        "pair_targets": receipt["pair_targets"],
        "sample_targets": receipt["sample_targets"],
        "portfolio_name": receipt["portfolio_name"],
        "portfolio_channel_labels": receipt["portfolio_channel_labels"],
        "portfolio_channel_count": receipt["portfolio_channel_count"],
        "residual_channel_labels": receipt["residual_channel_labels"],
        "residual_channel_count": receipt["residual_channel_count"],
        "target_rows": compact_target_rows(receipt["target_rows"]),
        "channel_rows": [
            compact_channel(row) for row in receipt["channel_rows"]],
        "pair_rows": receipt["pair_rows"],
        "separating_residual_channel_rows": [
            compact_channel(row)
            for row in receipt["separating_residual_channel_rows"]],
        "separating_residual_channel_count": (
            receipt["separating_residual_channel_count"]),
        "residual_negative_pressure_summary": (
            receipt["residual_negative_pressure_summary"]),
        "residual_positive_offset_summary": (
            receipt["residual_positive_offset_summary"]),
        "largest_residual_pressure_row": (
            receipt["largest_residual_pressure_row"]),
        "largest_positive_residual_offset_row": (
            receipt["largest_positive_residual_offset_row"]),
        "harshest_residual_sum_row": receipt["harshest_residual_sum_row"],
        "maximum_residual_identity_error": (
            receipt["maximum_residual_identity_error"]),
        "interpretation": {
            "mechanism_tested": (
                "After fixing the recurrent helpful portfolio, ask whether "
                "the residual channels form a smaller repeated obstruction or "
                "separate selected clear rows from selected deficits."),
            "falsifier_observed": (
                "The residual can be harshest on a passing row, so residual "
                "negativity alone does not classify failures on the selected "
                "fixture."),
            "remaining_theorem": (
                "The portfolio lower-bound theorem must either overcome "
                "adverse residual rows directly, or be paired with a genuine "
                "residual-channel estimate from fixed-modulus prime-pair "
                "arithmetic."),
        },
        "residual_channel_profile_measured": True,
        "residual_small_channel_theorem_proved": False,
        "residual_separation_theorem_proved": False,
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
