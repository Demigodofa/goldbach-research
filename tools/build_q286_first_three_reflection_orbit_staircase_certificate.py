"""Build q286 evidence for the three-branch pressure/ratio staircase.

For B=-negative_orbit_contribution and R=positive/B, any branch satisfying
(1-R)*B <= .3 certifies first_three >= -.3.  Kevin's rational staircase uses

- B <= 1,     R >= 7/10
- B <= 21/20, R >= 5/7
- B <= 5/4,  R >= 19/25

which are all exact .3-loss certificates.  The builder tests the union of
these branches on early and late q286 horizons.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-reflection-orbit-staircase-certificate.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_reflection_orbit_dual_rectangle_receipt,
)


STAIRCASE = ((1.0, 0.70), (21.0 / 20.0, 5.0 / 7.0), (1.25, 0.76))


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
        "union_certified_target_count": (
            receipt["union_certified_target_count"]),
        "union_uncertified_target_count": (
            receipt["union_uncertified_target_count"]),
        "union_uncertified_tail_target_count": (
            receipt["union_uncertified_tail_target_count"]),
        "union_uncertified_clear_target_count": (
            receipt["union_uncertified_clear_target_count"]),
        "rectangle_rows": receipt["rectangle_rows"],
        "intersection_fail_sets": receipt["intersection_fail_sets"],
        "minimum_exact_curve_margin_row": (
            receipt["minimum_exact_curve_margin_row"]),
        "worst_union_uncertified_row": (
            receipt["worst_union_uncertified_row"]),
        "all_tail_targets_union_uncertified": (
            receipt["all_tail_targets_union_uncertified"]),
        "union_certificate_has_tail_counterexample": (
            receipt["union_certificate_has_tail_counterexample"]),
    }


def main():
    horizons = {
        "early_cycles_0_15": q286_first_three_reflection_orbit_dual_rectangle_receipt(
            start=10000, cycle_count=16, targets_per_cycle=5005,
            tail_threshold=.3, rectangles=STAIRCASE),
        "late_cycles_0_7": q286_first_three_reflection_orbit_dual_rectangle_receipt(
            start=1120120, cycle_count=8, targets_per_cycle=5005,
            tail_threshold=.3, rectangles=STAIRCASE),
        "holdout_start_1200200_cycles_0_7": (
            q286_first_three_reflection_orbit_dual_rectangle_receipt(
                start=1200200, cycle_count=8, targets_per_cycle=5005,
                tail_threshold=.3, rectangles=STAIRCASE)),
    }
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite staircase-certificate diagnostic only; the staircase "
            "branches are sufficient conditions on measured rows, but no "
            "eventual staircase theorem, first-three tail bound, signed "
            "prime-correlation estimate, or Goldbach proof is established"),
        "tail_threshold": .3,
        "staircase_branches": STAIRCASE,
        "algebraic_statement": (
            "Each branch satisfies (1-R)*B <= .3, so any branch certifies "
            "first_three >= -.3."),
        "horizon_rows": {
            label: compact(receipt) for label, receipt in horizons.items()},
        "interpretation": {
            "changed_under_evidence": (
                "The three-branch rational staircase certifies every target "
                "in the late 8-cycle horizon starting at 1120120, including "
                "the prior dual-rectangle intersection row 1157462.  In the "
                "holdout starting at 1200200 it leaves exactly two targets "
                "uncertified, the tail target 1222142 and clear target "
                "1242118.  Early tails remain outside the staircase."),
            "remaining_theorem": (
                "A possible next theorem target is an eventual staircase "
                "occupancy result in (B,R)-space, plus finite checking for "
                "the early rows outside the staircase."),
        },
        "first_three_reflection_orbit_staircase_certificate_measured": True,
        "eventual_staircase_bounds_proved": False,
        "eventual_first_three_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
