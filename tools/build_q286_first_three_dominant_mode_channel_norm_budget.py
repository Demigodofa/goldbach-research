"""Build q286 dominant-mode channel norm budget evidence.

This artifact records simple sufficient Linf/L2 bounds for the 25 real
dominant mode-1/mode-2 q286 character channels, then checks whether those
bounds certify the current near-boundary sample rows.
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
    / "q286-first-three-dominant-mode-channel-norm-budget.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_channel_norm_budget_receipt,
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
    receipt = q286_first_three_dominant_mode_channel_norm_budget_receipt(
        sample_targets=(1222142, 1242118, 1240888),
        dominant_modes=(1, 2),
        tail_threshold=.3)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite norm-budget diagnostic only; records sufficient Linf/L2 "
            "conditions for the dominant two-mode q286 character obligation "
            "and active sample stress.  It proves no pointwise character-sum "
            "estimate, fixed-modulus AP theorem, q286 signed-projection "
            "theorem, or Goldbach proof."),
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "sample_targets": receipt["sample_targets"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "active_real_channel_count": receipt["active_real_channel_count"],
        "dominant_real_channel_l1_to_principal_mean": (
            receipt["dominant_real_channel_l1_to_principal_mean"]),
        "dominant_real_channel_l2_to_principal_mean": (
            receipt["dominant_real_channel_l2_to_principal_mean"]),
        "linf_sufficient_relative_channel_sum": (
            receipt["linf_sufficient_relative_channel_sum"]),
        "l2_sufficient_relative_channel_sum": (
            receipt["l2_sufficient_relative_channel_sum"]),
        "linf_certified_targets": receipt["linf_certified_targets"],
        "l2_certified_targets": receipt["l2_certified_targets"],
        "bound_failure_but_dominant_floor_pass_targets": (
            receipt["bound_failure_but_dominant_floor_pass_targets"]),
        "maximum_linf_budget_utilization_row": (
            receipt["maximum_linf_budget_utilization_row"]),
        "maximum_l2_budget_utilization_row": (
            receipt["maximum_l2_budget_utilization_row"]),
        "target_rows": receipt["target_rows"],
        "interpretation": {
            "what_changed": (
                "The exact 25-channel obligation now has explicit independent "
                "Linf and L2 sufficient thresholds."),
            "sample_fact": (
                "No current near-boundary sample row is certified by either "
                "generic channel norm budget; the two near-clear rows fail "
                "both budgets while their signed dominant sums still clear "
                "the -0.3 floor."),
            "route_effect": (
                "Generic independent channel smallness is too blunt at the "
                "active scale.  A proof needs signed channel cancellation, "
                "structured correlations among channels, a stronger "
                "prime-pair input, or complement/lower-support rescue."),
        },
        "dominant_mode_channel_norm_budget_measured": True,
        "generic_independent_channel_norm_bound_sufficient": True,
        "generic_independent_channel_norm_bound_demoted_on_samples": (
            receipt[
                "generic_independent_channel_norm_bound_demoted_on_samples"]),
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
