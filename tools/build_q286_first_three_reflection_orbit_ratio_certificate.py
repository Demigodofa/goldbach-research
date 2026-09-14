"""Build q286 first-three reflection-orbit ratio-certificate evidence.

The certificate is algebraic: if negative orbit pressure is at most 1.25 and
positive compensation is at least 0.76 of that pressure, then the q286
first-three ratio is at least -.3.  This builder measures that fixed
sufficient condition on baseline, intermediate, and late q286 periods.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-reflection-orbit-ratio-certificate.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_reflection_orbit_ratio_certificate_receipt,
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
        "first_uncertified_clear_targets": (
            receipt["first_uncertified_clear_targets"]),
        "first_uncertified_tail_targets": (
            receipt["first_uncertified_tail_targets"]),
        "first_pressure_ceiling_failure_targets": (
            receipt["first_pressure_ceiling_failure_targets"]),
        "first_compensation_ratio_floor_failure_targets": (
            receipt["first_compensation_ratio_floor_failure_targets"]),
        "minimum_ratio_row": receipt["minimum_ratio_row"],
        "maximum_pressure_row": receipt["maximum_pressure_row"],
        "minimum_certificate_margin_row": (
            receipt["minimum_certificate_margin_row"]),
        "worst_uncertified_tail_rows": (
            receipt["worst_uncertified_tail_rows"]),
        "nearest_uncertified_clear_rows": (
            receipt["nearest_uncertified_clear_rows"]),
        "nearest_certified_boundary_rows": (
            receipt["nearest_certified_boundary_rows"]),
        "ratio_certificate_all_targets_certified": (
            receipt["ratio_certificate_all_targets_certified"]),
        "ratio_certificate_has_certified_tail_counterexample": (
            receipt["ratio_certificate_has_certified_tail_counterexample"]),
    }


def main():
    windows = [
        ("baseline_first_period", 10000, 1),
        ("intermediate_holdout_first_period", 90080, 1),
        ("late_first_period", 1120120, 1),
    ]
    window_rows = {}
    for label, start, cycle_count in windows:
        receipt = q286_first_three_reflection_orbit_ratio_certificate_receipt(
            start=start, cycle_count=cycle_count, targets_per_cycle=5005,
            tail_threshold=.3, pressure_ceiling=1.25,
            compensation_ratio_floor=.76, include_rows=False)
        window_rows[label] = compact(receipt)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite diagnostic only; the pressure/ratio inequalities are "
            "measured on selected windows but are not proved eventually, and "
            "Goldbach is not proved"),
        "tail_threshold": .3,
        "pressure_ceiling": 1.25,
        "compensation_ratio_floor": .76,
        "algebraic_certificate_bound": -.3,
        "algebraic_statement": (
            "If B=-negative_orbit_contribution <= 1.25 and "
            "positive_orbit_contribution/B >= .76, then first_three >= -.3."),
        "window_rows": window_rows,
        "interpretation": {
            "changed_under_evidence": (
                "The fixed algebraic certificate covers every target in the "
                "late q286 period starting at 1120120, while baseline and "
                "intermediate periods retain explicit uncertified tail rows. "
                "This sharpens the theorem target to eventual pressure and "
                "compensation-ratio bounds, not another threshold ladder."),
            "falsifier": (
                "A later period with a first-three tail satisfying both fixed "
                "certificate inequalities would contradict the implementation "
                "or constants; a later no-tail period with many uncertified "
                "rows would demote the fixed constants as a useful eventual "
                "certificate."),
        },
        "first_three_reflection_orbit_ratio_certificate_measured": True,
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
