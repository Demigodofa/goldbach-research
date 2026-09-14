"""Build q286 evidence for positive-orbit landing near the -.3 boundary.

This receipt follows the boundary-pair autopsy and asks whether clear rows
near the exact curve are rescued by smaller negative pressure, by more
positive-side compensation, or by both.  It keeps the algebraic split

    first_three = -B + P

and further records the positive/negative orbit mass fractions and conditional
landing means.  The result is finite theorem-shaping evidence only.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-first-three-positive-orbit-landing-profile.json"
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_positive_orbit_landing_profile_receipt,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def compact(receipt):
    return {
        "start": receipt["start"],
        "cycle_count": receipt["cycle_count"],
        "targets_per_cycle": receipt["targets_per_cycle"],
        "tested_targets_with_prime_pairs": (
            receipt["tested_targets_with_prime_pairs"]),
        "near_window": receipt["near_window"],
        "near_boundary_target_count": receipt["near_boundary_target_count"],
        "near_boundary_tail_target_count": (
            receipt["near_boundary_tail_target_count"]),
        "near_boundary_clear_target_count": (
            receipt["near_boundary_clear_target_count"]),
        "near_boundary_targets": receipt["near_boundary_targets"],
        "reference_target": receipt["reference_target"],
        "reference_row": receipt["reference_row"],
        "pair_rows": receipt["pair_rows"],
        "balanced_pressure_and_compensation_targets": (
            receipt["balanced_pressure_and_compensation_targets"]),
        "positive_compensation_overcomes_worse_pressure_targets": (
            receipt[
                "positive_compensation_overcomes_worse_pressure_targets"]),
        "lower_pressure_only_targets": receipt["lower_pressure_only_targets"],
    }


def main():
    profiles = {
        "holdout_start_1200200_cycles_0_7": (
            q286_first_three_positive_orbit_landing_profile_receipt(
                start=1200200, cycle_count=8, targets_per_cycle=5005,
                near_window=(-.33, -.27), reference_target=1222142)),
        "witness_start_1222142_cycles_0_1": (
            q286_first_three_positive_orbit_landing_profile_receipt(
                start=1222142, cycle_count=2, targets_per_cycle=5005,
                near_window=(-.33, -.27), reference_target=1222142)),
    }
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite positive-orbit landing diagnostic only; no recurrence "
            "classification, exact-curve theorem, signed prime-correlation "
            "estimate, or Goldbach proof is established"),
        "profile_rows": {
            label: compact(receipt) for label, receipt in profiles.items()},
        "interpretation": {
            "changed_under_evidence": (
                "Near the -.3 boundary, clear rows split into different "
                "rescue types: 1242118 improves through both lower negative "
                "pressure and higher positive compensation, while 1240888 "
                "has worse negative pressure but is rescued by higher "
                "positive compensation."),
            "remaining_theorem": (
                "A possible next theorem target is a positive-orbit landing "
                "or mass-allocation estimate near the exact curve "
                "R>=1-.3/B.  A pressure-only theorem is too crude for the "
                "observed boundary rows."),
        },
        "positive_orbit_landing_profile_measured": True,
        "landing_classification_recurrence_proved": False,
        "eventual_exact_curve_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
