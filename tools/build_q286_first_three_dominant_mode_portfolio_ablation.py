"""Build q286 dominant-mode recurrent portfolio ablation evidence."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-portfolio-ablation.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_portfolio_ablation_receipt,
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


def compact_baseline_rows(rows):
    return {
        target: {
            "target": row["target"],
            "target_mod_286": row["target_mod_286"],
            "dominant_floor_passes": row["dominant_floor_passes"],
            "dominant_sum_to_principal": row[
                "dominant_sum_to_principal"],
            "full_portfolio_sum_to_principal": row[
                "full_portfolio_sum_to_principal"],
            "required_portfolio_for_floor": row[
                "required_portfolio_for_floor"],
            "full_portfolio_slack_to_floor": row[
                "full_portfolio_slack_to_floor"],
        }
        for target, row in rows.items()
    }


def compact_ablation_row(row):
    return {
        key: row[key]
        for key in (
            "removed_label",
            "remaining_channel_count",
            "all_original_clears_still_pass",
            "matches_full_floor_classification",
            "minimum_clear_slack",
            "maximum_failure_slack",
            "pass_targets_from_reduced_portfolio",
            "fail_targets_from_reduced_portfolio",
        )
    }


def compact_prefix_row(row):
    return {
        key: row[key]
        for key in (
            "channel_count",
            "channel_labels",
            "all_original_clears_still_pass",
            "matches_full_floor_classification",
            "minimum_clear_slack",
            "maximum_failure_slack",
            "pass_targets_from_prefix",
            "fail_targets_from_prefix",
        )
    }


def main():
    receipt = q286_first_three_dominant_mode_portfolio_ablation_receipt()
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite recurrent-portfolio ablation only; it tests selected "
            "q286 rows and proves no portfolio theorem, no fixed-modulus AP "
            "theorem, and no Goldbach theorem"),
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
        "baseline_target_rows": compact_baseline_rows(
            receipt["baseline_target_rows"]),
        "baseline_pass_targets": receipt["baseline_pass_targets"],
        "baseline_fail_targets": receipt["baseline_fail_targets"],
        "full_portfolio_summary": receipt["full_portfolio_summary"],
        "channel_rows": receipt["channel_rows"],
        "leave_one_out_rows": [
            compact_ablation_row(row)
            for row in receipt["leave_one_out_rows"]],
        "clear_essential_channel_labels": (
            receipt["clear_essential_channel_labels"]),
        "classification_essential_channel_labels": (
            receipt["classification_essential_channel_labels"]),
        "clear_essential_channel_count": (
            receipt["clear_essential_channel_count"]),
        "classification_essential_channel_count": (
            receipt["classification_essential_channel_count"]),
        "prefix_rows": [
            compact_prefix_row(row) for row in receipt["prefix_rows"]],
        "first_prefix_clearing_all_original_clears": (
            compact_prefix_row(
                receipt["first_prefix_clearing_all_original_clears"])
            if receipt["first_prefix_clearing_all_original_clears"]
            else None),
        "first_prefix_matching_classification": (
            compact_prefix_row(receipt["first_prefix_matching_classification"])
            if receipt["first_prefix_matching_classification"] else None),
        "all_leave_one_out_preserve_clear_passes": (
            receipt["all_leave_one_out_preserve_clear_passes"]),
        "all_leave_one_out_preserve_classification": (
            receipt["all_leave_one_out_preserve_classification"]),
        "interpretation": {
            "mechanism_tested": (
                "Remove or truncate channels from the fixed recurrent "
                "helpful portfolio and test the unchanged rowwise residual "
                "obligations."),
            "boundary": (
                "A finite ablation identifies load-bearing selected channels; "
                "it is not a uniform arithmetic lower-bound theorem."),
            "remaining_theorem": (
                "Prove a lower bound for the recurrent portfolio package, or "
                "derive a principled subportfolio theorem whose omitted "
                "channels are controlled by fixed-modulus prime-pair "
                "arithmetic."),
        },
        "portfolio_ablation_measured": True,
        "single_channel_portfolio_theorem_proved": False,
        "proper_subportfolio_theorem_proved": False,
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
