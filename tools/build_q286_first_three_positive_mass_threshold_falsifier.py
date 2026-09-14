"""Build q286 evidence falsifying a positive-mass-only separator.

The positive-orbit landing profile showed that clear holdout rows near the
-.3 boundary had more mass on positive orbit classes.  This builder tests the
simple separator

    positive_orbit_mass_fraction >= .49

on multiple q286 horizons.  It is intentionally a falsifier: high-mass tails
and low-mass clear rows show that mass share alone is not the missing theorem.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-positive-mass-threshold-falsifier.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_positive_mass_threshold_falsifier_receipt,
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
        "near_window": receipt["near_window"],
        "positive_mass_floor": receipt["positive_mass_floor"],
        "tested_target_count": receipt["tested_target_count"],
        "near_boundary_target_count": receipt["near_boundary_target_count"],
        "near_boundary_tail_target_count": (
            receipt["near_boundary_tail_target_count"]),
        "near_boundary_clear_target_count": (
            receipt["near_boundary_clear_target_count"]),
        "high_positive_mass_tail_counterexample_count": (
            receipt["high_positive_mass_tail_counterexample_count"]),
        "low_positive_mass_clear_exception_count": (
            receipt["low_positive_mass_clear_exception_count"]),
        "high_positive_mass_clear_count": (
            receipt["high_positive_mass_clear_count"]),
        "low_positive_mass_tail_count": receipt["low_positive_mass_tail_count"],
        "first_high_positive_mass_tail_counterexamples": (
            receipt["first_high_positive_mass_tail_counterexamples"]),
        "first_low_positive_mass_clear_exceptions": (
            receipt["first_low_positive_mass_clear_exceptions"]),
        "positive_mass_floor_certifies_clear_on_this_window": (
            receipt["positive_mass_floor_certifies_clear_on_this_window"]),
        "positive_mass_floor_catches_all_clear_rows_on_this_window": (
            receipt["positive_mass_floor_catches_all_clear_rows_on_this_window"]),
    }


def main():
    horizons = {
        "early_cycles_0_15": q286_first_three_positive_mass_threshold_falsifier_receipt(
            start=10000, cycle_count=16, targets_per_cycle=5005,
            positive_mass_floor=.49),
        "next_cycles_8_15": q286_first_three_positive_mass_threshold_falsifier_receipt(
            start=90080, cycle_count=8, targets_per_cycle=5005,
            positive_mass_floor=.49),
        "late_start_1120120_cycles_0_7": (
            q286_first_three_positive_mass_threshold_falsifier_receipt(
                start=1120120, cycle_count=8, targets_per_cycle=5005,
                positive_mass_floor=.49)),
        "holdout_start_1200200_cycles_0_7": (
            q286_first_three_positive_mass_threshold_falsifier_receipt(
                start=1200200, cycle_count=8, targets_per_cycle=5005,
                positive_mass_floor=.49)),
    }
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite falsifier for a positive-mass-only separator; no "
            "eventual exact-curve theorem, signed prime-correlation "
            "estimate, or Goldbach proof is established"),
        "horizon_rows": {
            label: compact(receipt) for label, receipt in horizons.items()},
        "interpretation": {
            "changed_under_evidence": (
                "The .49 positive-mass separator happens to split the "
                "1200200 holdout boundary rows, but it fails immediately on "
                "earlier horizons, with both high-positive-mass tails and "
                "low-positive-mass clear rows."),
            "remaining_theorem": (
                "Mass allocation remains relevant near the exact curve, but "
                "a proof must use landing means, orbit coefficients, residue "
                "structure, or another arithmetic constraint in addition to "
                "positive-mass share."),
        },
        "positive_mass_threshold_falsifier_measured": True,
        "positive_mass_threshold_theorem_proved": False,
        "eventual_exact_curve_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
