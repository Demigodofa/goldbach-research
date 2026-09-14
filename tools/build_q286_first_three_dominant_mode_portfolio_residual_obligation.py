"""Build q286 dominant-mode portfolio/residual obligation evidence.

This artifact bolts on the fixed helpful-channel portfolio and records the
exact residual theorem obligation target by target.
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
    / "q286-first-three-dominant-mode-portfolio-residual-obligation.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_portfolio_residual_obligation_receipt,
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
            "portfolio_sum_to_principal": row[
                "portfolio_sum_to_principal"],
            "nonportfolio_sum_to_principal": row[
                "nonportfolio_sum_to_principal"],
            "required_portfolio_for_floor": row[
                "required_portfolio_for_floor"],
            "portfolio_slack_to_floor": row[
                "portfolio_slack_to_floor"],
            "dominant_floor_slack": row["dominant_floor_slack"],
            "residual_sign": row["residual_sign"],
            "obligation_matches_dominant_floor": row[
                "obligation_matches_dominant_floor"],
        }
        for target, row in rows.items()
    }


def main():
    receipt = (
        q286_first_three_dominant_mode_portfolio_residual_obligation_receipt())
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite exact portfolio/residual diagnostic only; it rewrites the "
            "selected q286 dominant floor as a rowwise fixed-portfolio "
            "obligation, but proves no portfolio lower-bound theorem, no "
            "residual-channel theorem, no signed projection theorem, and no "
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
        "residual_channel_count": receipt["residual_channel_count"],
        "target_rows": compact_target_rows(receipt["target_rows"]),
        "pair_rows": receipt["pair_rows"],
        "dominant_floor_failure_targets": (
            receipt["dominant_floor_failure_targets"]),
        "dominant_floor_pass_targets": receipt[
            "dominant_floor_pass_targets"],
        "residual_negative_targets": receipt["residual_negative_targets"],
        "residual_positive_targets": receipt["residual_positive_targets"],
        "portfolio_slack_summary": receipt["portfolio_slack_summary"],
        "deficit_portfolio_slack_summary": (
            receipt["deficit_portfolio_slack_summary"]),
        "clear_portfolio_slack_summary": (
            receipt["clear_portfolio_slack_summary"]),
        "residual_summary": receipt["residual_summary"],
        "required_portfolio_summary": receipt[
            "required_portfolio_summary"],
        "worst_floor_slack_row": receipt["worst_floor_slack_row"],
        "largest_required_portfolio_row": receipt[
            "largest_required_portfolio_row"],
        "maximum_identity_error": receipt["maximum_identity_error"],
        "maximum_floor_identity_error": (
            receipt["maximum_floor_identity_error"]),
        "interpretation": {
            "mechanism_tested": (
                "Bolt the recurrent helpful-channel portfolio onto the "
                "selected q286 frame, subtract it exactly, and ask what "
                "portfolio lower bound remains after the residual is known."),
            "exact_equivalence": (
                "dominant_sum >= -threshold is equivalent row by row to "
                "portfolio_sum >= -threshold - nonportfolio_sum."),
            "remaining_theorem": (
                "Prove the recurrent portfolio lower bound against this "
                "row-dependent residual requirement, or prove an independent "
                "residual-channel bound that keeps the required portfolio "
                "inside a provable range."),
        },
        "all_obligations_match_dominant_floor": (
            receipt["all_obligations_match_dominant_floor"]),
        "portfolio_residual_obligation_measured": True,
        "fixed_portfolio_lower_bound_theorem_proved": False,
        "residual_channel_bound_theorem_proved": False,
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
