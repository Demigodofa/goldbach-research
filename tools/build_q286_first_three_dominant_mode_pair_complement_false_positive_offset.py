"""Autopsy the q286 pair/complement false positive outside the plane.

The expanded window holdout found that clear row 1200302 lies inside the .02
stress-centered pair/complement square.  This derivative receipt asks what
separates that clear from stress row 1222142 when the two volatile plane
coordinates are already close.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NEAR_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-near-boundary-selector-audit.json")
HOLDOUT_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pair-complement-window-holdout.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pair-complement-false-positive-offset.json")
STRESS_TARGET = 1222142
FALSE_POSITIVE_TARGET = 1200302


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set)):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def collect_near_rows(payload):
    rows = {}
    for window in payload["window_rows"]:
        for row in window["closest_margin_rows"]:
            target = int(row["target"])
            if target in rows:
                continue
            rows[target] = {
                **row,
                "window_start": int(window["start"]),
                "window_role": window["window_role"],
                "target_mod_10010": target % 10010,
            }
    return rows


def holdout_rows_by_target(payload):
    rows = {}
    for key in ("nearest_plane_rows", "nearest_margin_rows"):
        for row in payload[key]:
            rows.setdefault(int(row["target"]), row)
    for square in payload["square_records"]:
        for row in square["selected_rows"]:
            rows.setdefault(int(row["target"]), row)
    return rows


def compact_row(near_row, plane_row):
    omitted = (
        near_row["dominant_sum_to_principal"]
        - plane_row["volatile_total_sum_to_principal"])
    return {
        "target": int(near_row["target"]),
        "classification": plane_row["classification"],
        "window_start": int(near_row["window_start"]),
        "window_role": near_row["window_role"],
        "target_mod_286": int(near_row["target_mod_286"]),
        "target_mod_10010": int(near_row["target_mod_10010"]),
        "above_floor_signed_surplus_to_threshold": float(
            near_row["above_floor_signed_surplus_to_threshold"]),
        "absolute_above_floor_signed_surplus": float(
            near_row["absolute_above_floor_signed_surplus"]),
        "dominant_sum_to_principal": float(
            near_row["dominant_sum_to_principal"]),
        "nonportfolio_residual_sum_to_principal": float(
            near_row["nonportfolio_residual_sum_to_principal"]),
        "required_portfolio_for_floor": float(
            near_row["required_portfolio_for_floor"]),
        "above_floor_mass_fraction": float(
            near_row["above_floor_mass_fraction"]),
        "above_floor_mass_threshold": float(
            near_row["above_floor_mass_threshold"]),
        "adverse_pair_sum_to_principal": float(
            plane_row["adverse_pair_sum_to_principal"]),
        "repair_complement_sum_to_principal": float(
            plane_row["repair_complement_sum_to_principal"]),
        "volatile_total_sum_to_principal": float(
            plane_row["volatile_total_sum_to_principal"]),
        "outside_pair_complement_plane_sum_to_principal": float(omitted),
        "stress_plane_l1_distance": float(
            plane_row["stress_plane_l1_distance"]),
        "stress_plane_linf_distance": float(
            plane_row["stress_plane_linf_distance"]),
    }


def delta_row(row, stress):
    full_delta = (
        row["dominant_sum_to_principal"]
        - stress["dominant_sum_to_principal"])
    plane_delta = (
        row["volatile_total_sum_to_principal"]
        - stress["volatile_total_sum_to_principal"])
    outside_delta = (
        row["outside_pair_complement_plane_sum_to_principal"]
        - stress["outside_pair_complement_plane_sum_to_principal"])
    surplus_delta = (
        row["above_floor_signed_surplus_to_threshold"]
        - stress["above_floor_signed_surplus_to_threshold"])
    outside_share = (
        outside_delta / full_delta if abs(full_delta) > 1e-12 else math.nan)
    return {
        "target": row["target"],
        "classification": row["classification"],
        "above_floor_signed_surplus_delta": surplus_delta,
        "dominant_sum_delta_to_stress": full_delta,
        "volatile_plane_total_delta_to_stress": plane_delta,
        "outside_pair_complement_plane_delta_to_stress": outside_delta,
        "outside_delta_share_of_dominant_delta": outside_share,
        "pair_delta_to_stress": (
            row["adverse_pair_sum_to_principal"]
            - stress["adverse_pair_sum_to_principal"]),
        "complement_delta_to_stress": (
            row["repair_complement_sum_to_principal"]
            - stress["repair_complement_sum_to_principal"]),
        "nonportfolio_residual_delta_to_stress": (
            row["nonportfolio_residual_sum_to_principal"]
            - stress["nonportfolio_residual_sum_to_principal"]),
        "above_floor_mass_fraction_delta_to_stress": (
            row["above_floor_mass_fraction"]
            - stress["above_floor_mass_fraction"]),
        "above_floor_mass_threshold_delta_to_stress": (
            row["above_floor_mass_threshold"]
            - stress["above_floor_mass_threshold"]),
    }


def square_by_epsilon(payload, epsilon):
    for square in payload["square_records"]:
        if abs(float(square["epsilon"]) - epsilon) < 1e-12:
            return square
    raise KeyError(epsilon)


def main():
    near_payload = json.loads(NEAR_SOURCE.read_text(encoding="utf-8"))
    holdout_payload = json.loads(HOLDOUT_SOURCE.read_text(encoding="utf-8"))
    near_by_target = collect_near_rows(near_payload)
    plane_by_target = holdout_rows_by_target(holdout_payload)
    square_002 = square_by_epsilon(holdout_payload, 0.02)
    square_003 = square_by_epsilon(holdout_payload, 0.03)
    selected_targets = tuple(dict.fromkeys(
        [STRESS_TARGET, FALSE_POSITIVE_TARGET]
        + [int(row["target"]) for row in square_003["selected_rows"]]))

    compact_rows = tuple(
        compact_row(near_by_target[target], plane_by_target[target])
        for target in selected_targets)
    stress = next(row for row in compact_rows
                  if row["target"] == STRESS_TARGET)
    false_positive = next(
        row for row in compact_rows if row["target"] == FALSE_POSITIVE_TARGET)
    delta_rows = tuple(
        delta_row(row, stress) for row in compact_rows
        if row["target"] != STRESS_TARGET)
    false_positive_delta = next(
        row for row in delta_rows
        if row["target"] == FALSE_POSITIVE_TARGET)

    if square_002["clear_false_positive_targets"] != [FALSE_POSITIVE_TARGET]:
        raise AssertionError(".02 false-positive target drifted")
    if false_positive["classification"] != "clear":
        raise AssertionError("false-positive row is no longer clear")
    if false_positive_delta[
            "volatile_plane_total_delta_to_stress"] >= 0:
        raise AssertionError("false positive is no longer plane-worse")
    if false_positive_delta[
            "outside_pair_complement_plane_delta_to_stress"] <= 0.2:
        raise AssertionError("outside-plane rescue no longer dominates")
    if false_positive_delta[
            "outside_delta_share_of_dominant_delta"] <= 1.0:
        raise AssertionError("outside-plane delta no longer exceeds full delta")

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_near_boundary_selector_audit": str(
            NEAR_SOURCE.relative_to(ROOT)),
        "source_pair_complement_window_holdout": str(
            HOLDOUT_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite false-positive offset autopsy only; it shows that the "
            ".02 pair/complement clear false positive is rescued outside the "
            "two-coordinate volatile plane and proves no arithmetic placement "
            "theorem, signed projection theorem, or Goldbach proof"),
        "candidate": (
            "The .02 pair/complement false positive might be separated from "
            "the stress row by the full dominant-channel remainder outside "
            "the named-pair/complement plane."),
        "mechanism": (
            "For rows in the .03 stress-centered square, compare the full "
            "dominant first-three sum with the two-coordinate volatile "
            "pair/complement total.  The difference is the measured "
            "outside-plane dominant contribution."),
        "prediction": (
            "If pair/complement geometry is only a microscope, then the clear "
            ".02 false positive should clear because of a large favorable "
            "outside-plane dominant contribution, not because the volatile "
            "plane total itself is better than the stress row."),
        "falsifier": (
            "This offset explanation fails if the false-positive row is "
            "rescued mostly by the pair/complement total rather than by the "
            "outside-plane dominant contribution."),
        "novelty_label": "new-to-this-task",
        "stress_target": STRESS_TARGET,
        "false_positive_target": FALSE_POSITIVE_TARGET,
        "audited_targets": selected_targets,
        "stress_row": stress,
        "false_positive_row": false_positive,
        "delta_rows_to_stress": delta_rows,
        "square_point_zero_two": square_002,
        "square_point_zero_three": square_003,
        "summary": {
            "false_positive_plane_position": (
                "Clear row 1200302 sits inside the .02 stress-centered "
                "pair/complement square, at plane L1 distance about "
                "0.0195523595 and Linf distance about 0.0115203663."),
            "false_positive_plane_total": (
                "Relative to stress row 1222142, 1200302 has volatile "
                "pair/complement total lower by about 0.0034883731, so the "
                "two-coordinate plane does not supply the clear-row rescue."),
            "outside_plane_rescue": (
                "The outside-plane dominant contribution improves by about "
                "0.2158368813, while the full dominant sum improves by about "
                "0.2123485082."),
            "next_target": (
                "The proof obligation moves from fixed pair/complement boxes "
                "to controlling the omitted dominant-channel remainder "
                "together with the volatile plane."),
        },
        "interpretation": {
            "hole_status": (
                "The .02 hole is not closing as a pure two-coordinate plane "
                "selector; the decisive rescue for the first clear false "
                "positive comes from outside that plane."),
            "route_status": (
                "Preserve pair/complement geometry as a local locator, but "
                "promote the next theorem obligation to a three-part balance: "
                "named pair, repair complement, and outside-plane dominant "
                "remainder."),
            "remaining_theorem": (
                "Prove a coefficient-sensitive arithmetic placement theorem "
                "for the full dominant channel sum, or derive a signed "
                "aggregate estimate that controls the outside-plane remainder "
                "near the dangerous pair/complement region."),
        },
        "pair_complement_false_positive_offset_measured": True,
        "point_zero_two_false_positive_rescued_outside_plane": True,
        "pair_complement_plane_total_rescue_explanation_refuted": True,
        "three_part_balance_theorem_proved": False,
        "arithmetic_placement_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }

    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
