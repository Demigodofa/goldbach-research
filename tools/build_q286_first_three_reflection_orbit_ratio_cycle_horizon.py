"""Build q286 pressure/ratio certificate cycle-horizon evidence.

The constants are fixed: negative pressure ceiling 1.25 and positive
compensation ratio floor .76.  The receipt scans consecutive q286 periods and
records which cycles still have tails, pressure failures, ratio failures, or
uncertified rows under that same algebraic certificate.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-reflection-orbit-ratio-cycle-horizon.json")
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
        "tested_target_count": receipt["tested_target_count"],
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
        "first_all_certified_cycle": receipt["first_all_certified_cycle"],
        "first_no_tail_cycle": receipt["first_no_tail_cycle"],
        "last_uncertified_tail_cycle": (
            receipt["last_uncertified_tail_cycle"]),
        "minimum_ratio_row": receipt["minimum_ratio_row"],
        "maximum_pressure_row": receipt["maximum_pressure_row"],
        "minimum_certificate_margin_row": (
            receipt["minimum_certificate_margin_row"]),
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
            tail_threshold=.3, pressure_ceiling=1.25,
            compensation_ratio_floor=.76),
        "late_cycles_0_7": q286_first_three_reflection_orbit_ratio_cycle_horizon_receipt(
            start=1120120, cycle_count=8, targets_per_cycle=5005,
            tail_threshold=.3, pressure_ceiling=1.25,
            compensation_ratio_floor=.76),
    }
    horizon_rows = {
        label: compact(receipt) for label, receipt in horizons.items()}
    representative = horizons["early_cycles_0_15"]
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite horizon diagnostic only; constants are fixed, but no "
            "eventual pressure ceiling, compensation-ratio floor, first-three "
            "tail bound, signed prime-correlation estimate, or Goldbach proof "
            "is established"),
        "tail_threshold": representative["tail_threshold"],
        "pressure_ceiling": representative["pressure_ceiling"],
        "compensation_ratio_floor": representative[
            "compensation_ratio_floor"],
        "algebraic_certificate_bound": (
            representative["algebraic_certificate_bound"]),
        "horizon_rows": horizon_rows,
        "interpretation": {
            "changed_under_evidence": (
                "The fixed pressure/ratio certificate is tracked by q286 "
                "cycle without retuning constants.  This separates early "
                "ratio/pressure failures from late no-tail cycles where the "
                ".76 ratio floor is sufficient for most but not all clear "
                "targets."),
            "remaining_theorem": (
                "A proof route can either prove eventual arithmetic bounds "
                "B<=1.25 and positive/B>=.76, or weaken/classify the ratio "
                "condition to cover the observed late clear exceptions."),
        },
        "first_three_reflection_orbit_ratio_cycle_horizon_measured": True,
        "ratio_certificate_algebraic_sufficient_condition": (
            representative[
                "ratio_certificate_algebraic_sufficient_condition"]),
        "ratio_certificate_has_certified_tail_counterexample": (
            any(receipt[
                "ratio_certificate_has_certified_tail_counterexample"]
                for receipt in horizons.values())),
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
