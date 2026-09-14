"""Build q286 evidence for Kevin's B<=1, R>=.70 certificate candidate.

Algebraically, if B=-negative_orbit_contribution <= 1 and
R=positive_orbit_contribution/B >= .70, then first_three >= -.3.  This
builder tests that clean rectangle on the same early and late horizons used by
the pressure/ratio cycle-horizon receipt.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-reflection-orbit-b1-r70-certificate.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_reflection_orbit_ratio_cycle_horizon_receipt,
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
        "tail_target_count": receipt["tail_target_count"],
        "certified_target_count": receipt["certified_target_count"],
        "certified_tail_target_count": (
            receipt["certified_tail_target_count"]),
        "uncertified_clear_target_count": (
            receipt["uncertified_clear_target_count"]),
        "uncertified_tail_target_count": (
            receipt["uncertified_tail_target_count"]),
        "pressure_ceiling_failure_count": (
            receipt["pressure_ceiling_failure_count"]),
        "compensation_ratio_floor_failure_count": (
            receipt["compensation_ratio_floor_failure_count"]),
        "all_certified_cycles": receipt["all_certified_cycles"],
        "no_tail_cycles": receipt["no_tail_cycles"],
        "no_pressure_or_ratio_failure_cycles": (
            receipt["no_pressure_or_ratio_failure_cycles"]),
        "minimum_ratio_row": receipt["minimum_ratio_row"],
        "maximum_pressure_row": receipt["maximum_pressure_row"],
        "worst_uncertified_tail_row": (
            receipt["worst_uncertified_tail_row"]),
        "cycle_rows": receipt["cycle_rows"],
        "ratio_certificate_has_certified_tail_counterexample": (
            receipt["ratio_certificate_has_certified_tail_counterexample"]),
    }


def main():
    horizons = {
        "early_cycles_0_15": q286_first_three_reflection_orbit_ratio_cycle_horizon_receipt(
            start=10000, cycle_count=16, targets_per_cycle=5005,
            tail_threshold=.3, pressure_ceiling=1.0,
            compensation_ratio_floor=.70),
        "late_cycles_0_7": q286_first_three_reflection_orbit_ratio_cycle_horizon_receipt(
            start=1120120, cycle_count=8, targets_per_cycle=5005,
            tail_threshold=.3, pressure_ceiling=1.0,
            compensation_ratio_floor=.70),
    }
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite candidate-certificate diagnostic only; no eventual "
            "pressure ceiling, compensation-ratio floor, first-three tail "
            "bound, signed prime-correlation estimate, or Goldbach proof is "
            "established"),
        "tail_threshold": .3,
        "pressure_ceiling": 1.0,
        "compensation_ratio_floor": .70,
        "algebraic_certificate_bound": -.3,
        "algebraic_statement": (
            "If B=-negative_orbit_contribution <= 1 and "
            "positive_orbit_contribution/B >= .70, then first_three >= -.3."),
        "horizon_rows": {
            label: compact(receipt) for label, receipt in horizons.items()},
        "interpretation": {
            "changed_under_evidence": (
                "The clean B<=1, R>=.70 rectangle removes the late ratio "
                "failures seen under the .76 floor, but introduces late "
                "pressure failures: late no-tail cycles have 211 clear "
                "uncertified targets, all due to B>1."),
            "remaining_theorem": (
                "This supports a pressure-dependent compensation boundary "
                "or a separate treatment of B>1 clear rows, rather than a "
                "single flat ratio floor."),
        },
        "first_three_reflection_orbit_b1_r70_certificate_measured": True,
        "eventual_pressure_ratio_bounds_proved": False,
        "eventual_first_three_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
