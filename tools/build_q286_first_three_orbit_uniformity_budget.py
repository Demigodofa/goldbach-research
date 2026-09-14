"""Build q286 first-three orbit-uniformity budget evidence.

This works backward from the mass/landing obligation.  Local uniform orbit
mass would make the centered first-three action vanish, so a small enough
distance from local uniformity is a rigorous sufficient theorem.  The receipt
records the exact L1/L2 budgets and checks whether selected real rows sit
inside those budgets.
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
    / "q286-first-three-orbit-uniformity-budget.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_orbit_uniformity_budget_receipt,
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
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def main():
    receipt = q286_first_three_orbit_uniformity_budget_receipt()
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "conditional orbit-uniformity theorem budget and finite stress "
            "diagnostic only; no orbit-uniformity theorem, mass/landing "
            "inequality, signed prime-correlation estimate, or Goldbach proof "
            "is established"),
        "generic_orbit_uniformity_conditional_theorem": (
            receipt["generic_orbit_uniformity_conditional_theorem"]),
        "tail_threshold": receipt["tail_threshold"],
        "sample_targets": receipt["sample_targets"],
        "even_target_residue_count": receipt["even_target_residue_count"],
        "minimum_sufficient_l1_distance_to_uniform": (
            receipt["minimum_sufficient_l1_distance_to_uniform"]),
        "maximum_sufficient_l1_distance_to_uniform": (
            receipt["maximum_sufficient_l1_distance_to_uniform"]),
        "minimum_sufficient_l2_distance_to_uniform": (
            receipt["minimum_sufficient_l2_distance_to_uniform"]),
        "maximum_sufficient_l2_distance_to_uniform": (
            receipt["maximum_sufficient_l2_distance_to_uniform"]),
        "maximum_uniform_reconstruction_error": (
            receipt["maximum_uniform_reconstruction_error"]),
        "clear_sample_uniformity_budget_failure_targets": (
            receipt["clear_sample_uniformity_budget_failure_targets"]),
        "tail_sample_uniformity_budget_failure_targets": (
            receipt["tail_sample_uniformity_budget_failure_targets"]),
        "sample_rows": receipt["sample_rows"],
        "residue_rows": receipt["residue_rows"],
        "interpretation": {
            "backward_theorem": (
                "A pointwise L1 or L2 orbit-uniformity estimate with the "
                "recorded residue-dependent constants would imply the "
                "first-three mass/landing inequality."),
            "stress_result": (
                "If clear samples also fail the sufficient uniformity budget, "
                "then generic orbit-uniformity is too strong as a practical "
                "route and the proof should stay coefficient-sensitive."),
        },
        "generic_uniformity_budget_too_strong_for_clear_samples": (
            receipt["generic_uniformity_budget_too_strong_for_clear_samples"]),
        "coefficient_sensitive_estimate_still_required": (
            receipt["coefficient_sensitive_estimate_still_required"]),
        "orbit_uniformity_budget_measured": True,
        "orbit_uniformity_theorem_proved": False,
        "mass_landing_inequality_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
