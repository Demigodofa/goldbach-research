"""Build q286 first-three reflection-orbit cap evidence.

The receipt quantifies how small every reflection-orbit mass would need to be
to force the first-three active-selector rarity bound by geometry alone, then
compares that cap with actual strict-central prime-pair orbit concentrations
on the first q286 period.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-first-three-reflection-orbit-cap.json"
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_reflection_orbit_cap_receipt,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main():
    receipt = q286_first_three_reflection_orbit_cap_receipt(
        start=10000, cycle_count=1, targets_per_cycle=5005,
        tail_threshold=.3, include_rows=False)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite diagnostic only; orbit caps are sufficient conditions, "
            "not necessary conditions, and this proves neither q286 rarity "
            "nor Goldbach"),
        "start": receipt["start"],
        "cycle_count": receipt["cycle_count"],
        "targets_per_cycle": receipt["targets_per_cycle"],
        "tested_target_count": receipt["tested_target_count"],
        "tested_targets_with_prime_pairs": (
            receipt["tested_targets_with_prime_pairs"]),
        "tail_threshold": receipt["tail_threshold"],
        "minimum_sufficient_max_orbit_mass_row": (
            receipt["minimum_sufficient_max_orbit_mass_row"]),
        "maximum_sufficient_max_orbit_mass_row": (
            receipt["maximum_sufficient_max_orbit_mass_row"]),
        "cap_certified_target_count": receipt["cap_certified_target_count"],
        "cap_violation_target_count": receipt["cap_violation_target_count"],
        "first_cap_violation_targets": (
            receipt["first_cap_violation_targets"]),
        "tail_target_count": receipt["tail_target_count"],
        "tail_targets": receipt["tail_targets"],
        "worst_cap_ratio_row": receipt["worst_cap_ratio_row"],
        "maximum_orbit_mass_row": receipt["maximum_orbit_mass_row"],
        "minimum_first_three_row": receipt["minimum_first_three_row"],
        "interpretation": {
            "changed_under_evidence": (
                "A reflection-orbit mass cap sufficient to force "
                "first_three >= -0.3 would require every orbit to carry only "
                "about 1.68% to 2.68% of the mass, depending on target "
                "residue.  Actual first-period strict-central prime-pair "
                "weights exceed the sufficient cap on every tested target."),
            "remaining_theorem": (
                "A successful rarity route must use signed cancellation or "
                "arithmetic distribution across reflection orbits, not only "
                "a uniform maximum-orbit-mass bound."),
        },
        "first_three_reflection_orbit_cap_measured": True,
        "reflection_orbit_cap_rarity_theorem_proved": False,
        "signed_orbit_cancellation_required": (
            receipt["signed_orbit_cancellation_required"]),
        "eventual_first_three_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
