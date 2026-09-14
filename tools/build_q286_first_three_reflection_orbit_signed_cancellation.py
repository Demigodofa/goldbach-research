"""Build q286 first-three reflection-orbit signed-cancellation evidence.

The receipt follows the failed reflection-orbit cap route and measures the
actual signed decomposition over reflection orbits: negative orbit pressure,
positive orbit compensation, and the residual margin to the first-three
tail threshold.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-reflection-orbit-signed-cancellation.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_reflection_orbit_signed_cancellation_receipt,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main():
    receipt = q286_first_three_reflection_orbit_signed_cancellation_receipt(
        start=10000, cycle_count=1, targets_per_cycle=5005,
        tail_threshold=.3, include_rows=False)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite diagnostic only; the signed reflection-orbit "
            "decomposition identifies a compensation target but proves no "
            "eventual first-three rarity estimate and no Goldbach theorem"),
        "start": receipt["start"],
        "cycle_count": receipt["cycle_count"],
        "targets_per_cycle": receipt["targets_per_cycle"],
        "tested_target_count": receipt["tested_target_count"],
        "tested_targets_with_prime_pairs": (
            receipt["tested_targets_with_prime_pairs"]),
        "tail_threshold": receipt["tail_threshold"],
        "tail_target_count": receipt["tail_target_count"],
        "clear_target_count": receipt["clear_target_count"],
        "negative_pressure_target_count": (
            receipt["negative_pressure_target_count"]),
        "rescued_negative_pressure_target_count": (
            receipt["rescued_negative_pressure_target_count"]),
        "tail_negative_pressure_target_count": (
            receipt["tail_negative_pressure_target_count"]),
        "rescued_negative_pressure_fraction": (
            receipt["rescued_negative_pressure_fraction"]),
        "first_tail_targets": receipt["first_tail_targets"],
        "maximum_orbit_reconstruction_error": (
            receipt["maximum_orbit_reconstruction_error"]),
        "maximum_reflection_pair_weight_fraction_error": (
            receipt["maximum_reflection_pair_weight_fraction_error"]),
        "minimum_first_three_row": receipt["minimum_first_three_row"],
        "maximum_negative_pressure_row": (
            receipt["maximum_negative_pressure_row"]),
        "maximum_positive_compensation_row": (
            receipt["maximum_positive_compensation_row"]),
        "minimum_compensation_surplus_row": (
            receipt["minimum_compensation_surplus_row"]),
        "maximum_negative_mass_fraction_row": (
            receipt["maximum_negative_mass_fraction_row"]),
        "maximum_positive_mass_fraction_row": (
            receipt["maximum_positive_mass_fraction_row"]),
        "worst_first_three_rows": receipt["worst_first_three_rows"],
        "largest_negative_pressure_rows": (
            receipt["largest_negative_pressure_rows"]),
        "largest_positive_compensation_rows": (
            receipt["largest_positive_compensation_rows"]),
        "largest_compensation_deficit_rows": (
            receipt["largest_compensation_deficit_rows"]),
        "interpretation": {
            "changed_under_evidence": (
                "A uniform reflection-orbit mass cap is not the active "
                "phenomenon: in the first q286 period, 5002 of 5005 targets "
                "have negative orbit pressure already below the -.3 tail "
                "threshold before compensation, but 4030 of those are cleared "
                "by positive orbit contribution."),
            "remaining_theorem": (
                "The natural next theorem target is a pointwise arithmetic "
                "lower bound on positive-orbit compensation relative to "
                "negative-orbit pressure, or an explicit classification of "
                "the compensation-deficit rows."),
        },
        "first_three_reflection_orbit_signed_cancellation_measured": True,
        "reflection_orbit_cap_rarity_theorem_proved": False,
        "signed_orbit_cancellation_required": True,
        "eventual_first_three_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
