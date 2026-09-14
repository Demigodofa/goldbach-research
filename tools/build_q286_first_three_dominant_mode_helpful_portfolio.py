"""Build q286 dominant-mode helpful-channel portfolio evidence.

This artifact tests whether the recurrent helpful channels from the swing-pair
decomposition form a fixed portfolio that explains selected clear rows under
pressure, or whether the route still needs full signed-channel structure.
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
    / "q286-first-three-dominant-mode-helpful-portfolio.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_helpful_portfolio_receipt,
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
            "dominant_sum_to_principal": row["dominant_sum_to_principal"],
            "portfolio_sum_to_principal": row["portfolio_sum_to_principal"],
            "nonportfolio_sum_to_principal": (
                row["nonportfolio_sum_to_principal"]),
            "required_nonportfolio_for_floor": (
                row["required_nonportfolio_for_floor"]),
            "nonportfolio_slack_to_floor": (
                row["nonportfolio_slack_to_floor"]),
        }
        for target, row in rows.items()
    }


def compact_portfolio(row):
    return {
        "name": row["name"],
        "channel_labels": row["channel_labels"],
        "channel_count": row["channel_count"],
        "deficit_portfolio_summary": row["deficit_portfolio_summary"],
        "clear_portfolio_summary": row["clear_portfolio_summary"],
        "deficit_nonportfolio_summary": row[
            "deficit_nonportfolio_summary"],
        "clear_nonportfolio_summary": row["clear_nonportfolio_summary"],
        "minimum_positive_delta_share_row": (
            row["minimum_positive_delta_share_row"]),
        "clear_min_exceeds_deficit_max_on_samples": (
            row["clear_min_exceeds_deficit_max_on_samples"]),
        "pair_rows": row["pair_rows"],
        "target_rows": compact_target_rows(row["target_rows"]),
    }


def main():
    receipt = q286_first_three_dominant_mode_helpful_portfolio_receipt()
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite fixed-portfolio diagnostic only; selected rows and pairs "
            "are measured exactly, but no portfolio theorem, signed-channel "
            "offset theorem, pointwise character-sum estimate, fixed-modulus "
            "AP theorem, signed projection theorem, or Goldbach proof is "
            "established"),
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "active_real_channel_count": receipt["active_real_channel_count"],
        "pair_targets": receipt["pair_targets"],
        "sample_targets": receipt["sample_targets"],
        "recurrent_min_pair_count": receipt["recurrent_min_pair_count"],
        "portfolio_rows": {
            name: compact_portfolio(row)
            for name, row in receipt["portfolio_rows"].items()},
        "maximum_row_reconstruction_error": (
            receipt["maximum_row_reconstruction_error"]),
        "maximum_swing_reconstruction_error": (
            receipt["maximum_swing_reconstruction_error"]),
        "interpretation": {
            "mechanism_tested": (
                "Use fixed helpful-channel labels learned from the selected "
                "swing pairs, then measure whether their contribution "
                "separates clear rows from deficits."),
            "boundary": (
                "A separating finite sample is not a theorem; it only names "
                "a candidate arithmetic portfolio whose recurrence must be "
                "proved or falsified outside the selected fixture."),
            "remaining_theorem": (
                "Prove a portfolio-level lower bound under pressure, classify "
                "the true deficits as finite/boundary rows, or reduce the "
                "claim to a fixed-modulus binary-prime character-sum theorem."),
        },
        "helpful_portfolio_contribution_measured": True,
        "universal_portfolio_separates_clear_from_deficit_on_samples": (
            receipt[
                "universal_portfolio_separates_clear_from_deficit_on_samples"]),
        "recurrent_portfolio_separates_clear_from_deficit_on_samples": (
            receipt[
                "recurrent_portfolio_separates_clear_from_deficit_on_samples"]),
        "fixed_portfolio_theorem_proved": False,
        "eventual_signed_channel_offset_theorem_proved": False,
        "pointwise_character_sum_estimate_proved": False,
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
