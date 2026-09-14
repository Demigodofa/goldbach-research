"""Autopsy the q286 first-three boundary pair 1222142/1242118.

The refined staircase was motivated by a nearby tail/clear split:

- 1222142 is just below the -.3 first-three threshold.
- 1242118 is clear but missed by the original three-step staircase.

This builder records the direct difference, the pressure/compensation split,
the other near-threshold holdout row, top reflection-orbit components, and
top q286 character-coordinate differences.  It also records that conductor
77 is not native to this q286 first-three layer; that conductor belongs to
separate lower-support component lanes and would need its own overlay test.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-first-three-boundary-pair-autopsy.json"
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_character_imbalance_receipt,
    q286_first_three_reflection_orbit_signed_cancellation_receipt,
)


TARGETS = (1222142, 1242118, 1240888)
REFERENCE_TARGET = 1222142


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def top_orbit_rows(row, limit=12):
    return tuple(sorted(
        row["orbit_rows"],
        key=lambda item: abs(item["signed_contribution_to_principal_ratio"]),
        reverse=True)[:limit])


def compact_signed_row(row):
    total_abs = math.fsum(
        abs(orbit["signed_contribution_to_principal_ratio"])
        for orbit in row["orbit_rows"])
    top5_abs = math.fsum(
        abs(orbit["signed_contribution_to_principal_ratio"])
        for orbit in top_orbit_rows(row, limit=5))
    return {
        "target": row["target"],
        "target_mod_286": row["target_mod_286"],
        "first_three_to_principal_ratio": (
            row["first_three_to_principal_ratio"]),
        "negative_pressure_B": (
            -row["negative_orbit_contribution_to_principal_ratio"]),
        "positive_compensation_to_principal_ratio": (
            row["positive_orbit_contribution_to_principal_ratio"]),
        "positive_to_negative_pressure_ratio_R": (
            row["positive_to_negative_pressure_ratio"]),
        "positive_compensation_surplus_to_threshold": (
            row["positive_compensation_surplus_to_threshold"]),
        "negative_orbit_mass_fraction": row["negative_orbit_mass_fraction"],
        "positive_orbit_mass_fraction": row["positive_orbit_mass_fraction"],
        "absolute_orbit_contribution_envelope": total_abs,
        "top5_absolute_orbit_contribution_share": (
            top5_abs / total_abs if total_abs else 0.0),
        "top_absolute_orbit_rows": top_orbit_rows(row),
    }


def signed_rows():
    rows = {}
    for target in TARGETS:
        receipt = q286_first_three_reflection_orbit_signed_cancellation_receipt(
            start=target, cycle_count=1, targets_per_cycle=1,
            include_rows=True, include_orbit_rows=True)
        rows[target] = receipt["target_rows"][target]
    return rows


def holdout_near_threshold_rows():
    receipt = q286_first_three_reflection_orbit_signed_cancellation_receipt(
        start=1200200, cycle_count=8, targets_per_cycle=5005,
        include_rows=True, include_orbit_rows=False)
    rows = []
    for target, row in receipt["target_rows"].items():
        first_three = row["first_three_to_principal_ratio"]
        if -.33 <= first_three <= -.27:
            rows.append({
                "target": target,
                "distance_to_threshold": abs(first_three + .3),
                "target_mod_286": row["target_mod_286"],
                "first_three_to_principal_ratio": first_three,
                "negative_pressure_B": (
                    -row["negative_orbit_contribution_to_principal_ratio"]),
                "positive_to_negative_pressure_ratio_R": (
                    row["positive_to_negative_pressure_ratio"]),
                "positive_compensation_surplus_to_threshold": (
                    row["positive_compensation_surplus_to_threshold"]),
            })
    rows.sort(key=lambda item: item["distance_to_threshold"])
    return tuple(rows)


def character_autopsy():
    receipt = q286_character_imbalance_receipt(
        targets=TARGETS, top_count=120)

    def compact_character_row(item):
        return {
            "label": item["label"],
            "contribution_to_principal_ratio": (
                item["contribution_to_principal_ratio"]),
            "coefficient": {
                "real": item["coefficient"].real,
                "imag": item["coefficient"].imag,
            },
            "imbalance_sum": {
                "real": item["imbalance_sum"].real,
                "imag": item["imbalance_sum"].imag,
            },
            "contribution": {
                "real": item["contribution"].real,
                "imag": item["contribution"].imag,
            },
        }

    maps = {}
    compact_rows = {}
    for target in TARGETS:
        row = receipt["rows"][target]
        character_rows = row["top_negative_character_rows"]
        maps[target] = {
            tuple(item["label"]): item["contribution_to_principal_ratio"]
            for item in character_rows}
        compact_rows[target] = {
            "deviation_to_principal_ratio": (
                row["deviation_to_principal_ratio"]),
            "top_negative_character_rows": tuple(
                compact_character_row(item)
                for item in row["top_negative_character_rows"][:10]),
            "top_positive_character_rows": tuple(
                compact_character_row(item)
                for item in row["top_positive_character_rows"][:10]),
        }
    diffs = {}
    for target in TARGETS:
        if target == REFERENCE_TARGET:
            continue
        target_diffs = []
        for label, value in maps[target].items():
            reference_value = maps[REFERENCE_TARGET][label]
            target_diffs.append({
                "label": label,
                "difference_to_reference": value - reference_value,
                "target_contribution_to_principal_ratio": value,
                "reference_contribution_to_principal_ratio": reference_value,
            })
        target_diffs.sort(
            key=lambda item: abs(item["difference_to_reference"]),
            reverse=True)
        diffs[target] = tuple(target_diffs[:16])
    return {
        "support": receipt["support"],
        "natural_modulus": receipt["natural_modulus"],
        "active_character_count": receipt["active_character_count"],
        "active_both_prime_support_count": (
            receipt["active_both_prime_support_count"]),
        "target_rows": compact_rows,
        "top_character_differences_from_reference": diffs,
    }


def pair_difference(rows, target):
    reference = rows[REFERENCE_TARGET]
    row = rows[target]
    pressure_reduction = (
        -reference["negative_orbit_contribution_to_principal_ratio"]
        + row["negative_orbit_contribution_to_principal_ratio"])
    compensation_increase = (
        row["positive_orbit_contribution_to_principal_ratio"]
        - reference["positive_orbit_contribution_to_principal_ratio"])
    first_three_swing = (
        row["first_three_to_principal_ratio"]
        - reference["first_three_to_principal_ratio"])
    return {
        "target": target,
        "reference_target": REFERENCE_TARGET,
        "first_three_swing_to_principal_ratio": first_three_swing,
        "pressure_reduction_component": pressure_reduction,
        "positive_compensation_increase_component": compensation_increase,
        "zero_orbit_component_change": (
            row["zero_orbit_contribution_to_principal_ratio"]
            - reference["zero_orbit_contribution_to_principal_ratio"]),
        "explained_swing_error": abs(
            first_three_swing
            - pressure_reduction
            - compensation_increase
            - (row["zero_orbit_contribution_to_principal_ratio"]
               - reference["zero_orbit_contribution_to_principal_ratio"])),
        "negative_mass_fraction_change": (
            row["negative_orbit_mass_fraction"]
            - reference["negative_orbit_mass_fraction"]),
        "positive_mass_fraction_change": (
            row["positive_orbit_mass_fraction"]
            - reference["positive_orbit_mass_fraction"]),
        "R_change": (
            row["positive_to_negative_pressure_ratio"]
            - reference["positive_to_negative_pressure_ratio"]),
    }


def main():
    rows = signed_rows()
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite boundary-row autopsy only; it identifies measured "
            "component differences but proves no recurrence pattern, "
            "pointwise estimate, or Goldbach theorem"),
        "reference_target": REFERENCE_TARGET,
        "targets": TARGETS,
        "near_threshold_window": [-.33, -.27],
        "holdout_start": 1200200,
        "holdout_cycle_count": 8,
        "holdout_targets_per_cycle": 5005,
        "holdout_near_threshold_rows": holdout_near_threshold_rows(),
        "signed_orbit_target_rows": {
            str(target): compact_signed_row(row)
            for target, row in rows.items()},
        "pair_differences_from_reference": {
            str(target): pair_difference(rows, target)
            for target in TARGETS if target != REFERENCE_TARGET},
        "character_autopsy": character_autopsy(),
        "conductor77_applicability": {
            "native_to_q286_first_three_layer": False,
            "reason": (
                "The q286 first-three character autopsy has support (11,13) "
                "on natural modulus 286.  Conductor 77 belongs to separate "
                "lower-support component lanes and requires a distinct "
                "overlay test before being claimed relevant here."),
        },
        "first_three_boundary_pair_autopsy_measured": True,
        "recurring_component_pattern_proved": False,
        "pointwise_signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
