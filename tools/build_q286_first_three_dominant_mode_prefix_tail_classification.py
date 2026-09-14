"""Build q286 dominant-mode prefix/tail classification evidence."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-prefix-tail-classification.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_prefix_tail_classification_receipt,
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
            "dominant_floor_passes": row["dominant_floor_passes"],
            "prefix_sum_to_principal": row["prefix_sum_to_principal"],
            "tail_sum_to_principal": row["tail_sum_to_principal"],
            "full_portfolio_sum_to_principal": row[
                "full_portfolio_sum_to_principal"],
            "prefix_slack_to_floor": row["prefix_slack_to_floor"],
            "required_tail_for_full_floor": row[
                "required_tail_for_full_floor"],
            "tail_slack_to_full_floor": row["tail_slack_to_full_floor"],
            "full_portfolio_slack_to_floor": row[
                "full_portfolio_slack_to_floor"],
            "prefix_overrescues_failure": row[
                "prefix_overrescues_failure"],
            "tail_restores_failure": row["tail_restores_failure"],
            "tail_preserves_clear": row["tail_preserves_clear"],
        }
        for target, row in rows.items()
    }


def main():
    receipt = (
        q286_first_three_dominant_mode_prefix_tail_classification_receipt())
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite prefix/tail portfolio diagnostic only; it proves no "
            "prefix lower-bound theorem, no tail classification theorem, no "
            "fixed-modulus AP theorem, and no Goldbach theorem"),
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
        "prefix_channel_labels": receipt["prefix_channel_labels"],
        "prefix_channel_count": receipt["prefix_channel_count"],
        "tail_channel_labels": receipt["tail_channel_labels"],
        "tail_channel_count": receipt["tail_channel_count"],
        "target_rows": compact_target_rows(receipt["target_rows"]),
        "pair_rows": receipt["pair_rows"],
        "clear_targets": receipt["clear_targets"],
        "failure_targets": receipt["failure_targets"],
        "overrescued_failure_targets": (
            receipt["overrescued_failure_targets"]),
        "tail_restored_failure_targets": (
            receipt["tail_restored_failure_targets"]),
        "tail_preserved_clear_targets": (
            receipt["tail_preserved_clear_targets"]),
        "all_prefix_clears_original_clears": (
            receipt["all_prefix_clears_original_clears"]),
        "all_prefix_overrescued_failures": (
            receipt["all_prefix_overrescued_failures"]),
        "tail_restores_all_overrescued_failures": (
            receipt["tail_restores_all_overrescued_failures"]),
        "tail_preserves_all_original_clears": (
            receipt["tail_preserves_all_original_clears"]),
        "prefix_summary": receipt["prefix_summary"],
        "tail_summary": receipt["tail_summary"],
        "clear_tail_slack_summary": receipt["clear_tail_slack_summary"],
        "failure_tail_slack_summary": (
            receipt["failure_tail_slack_summary"]),
        "maximum_reconstruction_error": (
            receipt["maximum_reconstruction_error"]),
        "maximum_tail_floor_identity_error": (
            receipt["maximum_tail_floor_identity_error"]),
        "interpretation": {
            "mechanism_tested": (
                "Split the recurrent portfolio into the first prefix that "
                "keeps selected clears passing and the remaining tail that "
                "restores selected deficit classification."),
            "exact_equivalence": (
                "With prefix fixed, full-floor recovery is exactly "
                "tail_sum >= -prefix_slack."),
            "remaining_theorem": (
                "Prove a prefix lower bound for true clear/rescue rows and a "
                "tail/exclusion/complement theorem that prevents over-rescued "
                "deficits from becoming false positives."),
        },
        "prefix_tail_classification_measured": True,
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
