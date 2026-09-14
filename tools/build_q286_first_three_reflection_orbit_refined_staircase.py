"""Build q286 evidence for the refined pressure/ratio staircase.

The first three-branch staircase left clear target 1242118 outside the
certificate while correctly leaving tail target 1222142 outside.  This builder
adds one exact rational step near B=1:

- B <= 101/100, R >= 71/101

Since (1-71/101)*(101/100) = 3/10, the step is a valid sufficient certificate
for first_three >= -.3.  The refinement is post-hoc relative to the 1200200
holdout, so its value is theorem-shaping rather than independent validation.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-reflection-orbit-refined-staircase.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_reflection_orbit_dual_rectangle_receipt,
)


REFINED_STAIRCASE = (
    (1.0, 0.70),
    (101.0 / 100.0, 71.0 / 101.0),
    (21.0 / 20.0, 5.0 / 7.0),
    (1.25, 0.76),
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
            tail_threshold=.3, rectangles=REFINED_STAIRCASE),
        "late_cycles_0_7": q286_first_three_reflection_orbit_dual_rectangle_receipt(
            start=1120120, cycle_count=8, targets_per_cycle=5005,
            tail_threshold=.3, rectangles=REFINED_STAIRCASE),
        "holdout_start_1200200_cycles_0_7": (
            q286_first_three_reflection_orbit_dual_rectangle_receipt(
                start=1200200, cycle_count=8, targets_per_cycle=5005,
                tail_threshold=.3, rectangles=REFINED_STAIRCASE)),
    }
    witness_targets = {}
    for target in (1222142, 1242118):
        receipt = q286_first_three_reflection_orbit_dual_rectangle_receipt(
            start=target, cycle_count=1, targets_per_cycle=1,
            tail_threshold=.3, rectangles=REFINED_STAIRCASE,
            include_rows=True)
        witness_targets[str(target)] = receipt["target_rows"][target]

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite post-hoc refined-staircase diagnostic only; the "
            "branches are sufficient conditions on measured rows, but no "
            "eventual staircase theorem, first-three tail bound, signed "
            "prime-correlation estimate, or Goldbach proof is established"),
        "tail_threshold": .3,
        "refined_staircase_branches": REFINED_STAIRCASE,
        "added_branch": (101.0 / 100.0, 71.0 / 101.0),
        "added_branch_algebra": (
            "(1-71/101)*(101/100)=3/10, so B<=101/100 and R>=71/101 "
            "certifies first_three>=-.3."),
        "horizon_rows": {
            label: compact(receipt) for label, receipt in horizons.items()},
        "witness_targets": witness_targets,
        "interpretation": {
            "changed_under_evidence": (
                "The added exact step certifies the clear holdout miss "
                "1242118 while leaving the genuine tail 1222142 uncertified. "
                "On the three recorded horizons it introduces no "
                "certified-tail counterexample."),
            "remaining_theorem": (
                "A possible next theorem target is an eventual refined "
                "staircase occupancy result or the exact curve "
                "R>=1-.3/B, plus finite checking for rows outside the "
                "certificate."),
        },
        "first_three_reflection_orbit_refined_staircase_measured": True,
        "post_hoc_relative_to_holdout_1200200": True,
        "eventual_refined_staircase_bounds_proved": False,
        "eventual_first_three_tail_bound_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
