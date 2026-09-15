"""Residual schedule for q286-WBSS multiplicative-character truncations.

The multiplicative-character burden audit showed that Dirichlet-character
coordinates compress the coefficient side, but not to a tiny theorem.  This
receipt asks the next theorem-facing question: if we keep the largest
characters and put the rest into a residual bucket, can the residual be
ignored by coefficient energy alone?

The answer is no.  Even aggressive truncations leave a residual whose crude
Cauchy bound is much larger than the local main term, so a proof needs either
an explicit residual character theorem or the full nonzero character package.
"""

from __future__ import annotations

import itertools
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
MULTIPLICATIVE_SOURCE = (
    EVIDENCE / "q286-wbss-multiplicative-character-burden-audit.json")
COEFFICIENT_HOLD = (
    EVIDENCE / "q286-wbss-coefficient-discrepancy-budget-hold.json")
OUT = EVIDENCE / "q286-wbss-multiplicative-residual-schedule-audit.json"
TOLERANCE = 1e-20

sys.path.insert(0, str(ROOT))

from tools.build_q286_wbss_multiplicative_character_burden_audit import (  # noqa: E402
    FORMULA_SOURCE,
    MODULUS_FACTORS,
    coefficient_grid,
    coefficient_rows_by_modulus,
    exponent_map,
    load_json,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def active_modes():
    formula = load_json(FORMULA_SOURCE)
    coefficients = coefficient_rows_by_modulus(formula)
    maps = {
        factor: exponent_map(factor)
        for factors in MODULUS_FACTORS.values()
        for factor in factors
    }
    rows = []
    for modulus, factors in MODULUS_FACTORS.items():
        grid = coefficient_grid(modulus, factors, coefficients[modulus], maps)
        centered = grid - np.mean(grid)
        transform = np.fft.fftn(centered) / centered.size
        energy = np.abs(transform) ** 2
        for frequency in itertools.product(*(range(size)
                                             for size in transform.shape)):
            if all(item == 0 for item in frequency):
                continue
            value = complex(transform[frequency])
            mode_energy = float(energy[frequency])
            if mode_energy <= TOLERANCE:
                continue
            rows.append({
                "modulus": modulus,
                "unit_count": int(grid.size),
                "frequency": list(frequency),
                "energy": mode_energy,
                "abs_coefficient": abs(value),
                "zero_axis": any(item == 0 for item in frequency),
            })
    rows.sort(key=lambda row: row["energy"], reverse=True)
    return rows


def residual_schedule(modes, local_main_minimum):
    total_energy = sum(row["energy"] for row in modes)
    key_counts = [27, 45, 60, 65, 77, 100, 120, len(modes)]
    schedule = []
    for keep_count in key_counts:
        selected = {
            (row["modulus"], tuple(row["frequency"]))
            for row in modes[:keep_count]
        }
        selected_energy = 0.0
        selected_by_modulus = {}
        residual_by_modulus = {}
        unit_count_by_modulus = {}
        for row in modes:
            key = str(row["modulus"])
            residual_by_modulus.setdefault(key, 0.0)
            selected_by_modulus.setdefault(key, 0)
            unit_count_by_modulus[key] = row["unit_count"]
            mode_key = (row["modulus"], tuple(row["frequency"]))
            if mode_key in selected:
                selected_energy += row["energy"]
                selected_by_modulus[key] += 1
            else:
                residual_by_modulus[key] += row["energy"]

        crude_by_modulus = {
            modulus: math.sqrt(
                unit_count_by_modulus[modulus]
                * (unit_count_by_modulus[modulus] - 1)
                * residual_energy)
            for modulus, residual_energy in residual_by_modulus.items()
        }
        crude_sum = sum(crude_by_modulus.values())
        schedule.append({
            "kept_character_count": keep_count,
            "selected_energy_fraction": selected_energy / total_energy,
            "selected_character_count_by_modulus": selected_by_modulus,
            "residual_energy_by_modulus": residual_by_modulus,
            "crude_probability_discrepancy_residual_bound_by_modulus": (
                crude_by_modulus),
            "crude_probability_discrepancy_residual_bound_sum": crude_sum,
            "minimum_local_main": local_main_minimum,
            "crude_residual_to_minimum_local_main_ratio": (
                crude_sum / local_main_minimum),
            "coefficient_residual_eliminated": crude_sum == 0.0,
        })
    return schedule


def build_receipt():
    multiplicative = load_json(MULTIPLICATIVE_SOURCE)
    coefficient_hold = load_json(COEFFICIENT_HOLD)
    modes = active_modes()
    local_main_minimum = coefficient_hold["coefficient_budget"][
        "minimum_local_main_over_even_residues"]
    schedule = residual_schedule(modes, local_main_minimum)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "multiplicative_character_burden_audit": str(
                MULTIPLICATIVE_SOURCE.relative_to(ROOT)),
            "multiplicative_character_burden_status": multiplicative[
                "status"],
            "coefficient_discrepancy_budget_hold": str(
                COEFFICIENT_HOLD.relative_to(ROOT)),
            "coefficient_discrepancy_hold_source_commit": coefficient_hold[
                "source_commit"],
        },
        "status": "HOLD_residual_character_bound_required",
        "status_boundary": (
            "finite multiplicative-character truncation schedule only; it "
            "proves no residual character bound, fixed-modulus binary-prime "
            "discrepancy theorem, pointwise adverse-drag theorem, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof"),
        "acceptance_condition": {
            "finite_evidence_is_acceptance_condition": False,
            "required_acceptance_condition": (
                "a universal pointwise analytic estimate, with a finite "
                "initial-range computation only as a separate coverage "
                "bridge"),
            "unnormalized_target": (
                "Prove AdverseDrag(N) < LocalMain(N) for every sufficiently "
                "large eligible even N, before any finite checked range is "
                "allowed to complete the route."),
            "why_this_receipt_is_not_enough": (
                "This receipt only measures coefficient residual schedules "
                "on the finite q286-WBSS fixture; it does not prove a "
                "uniform-in-N residual character estimate."),
        },
        "goldbach_proved": False,
        "residual_character_bound_proved": False,
        "multiplicative_character_theorem_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "fixed_modulus_binary_prime_discrepancy_theorem_proved": False,
        "universal_bound_open": True,
        "method": {
            "active_character_filter": (
                f"nonprincipal multiplicative characters with energy > "
                f"{TOLERANCE}"),
            "crude_residual_bound": (
                "For a residual coefficient vector c_res on n unit residues "
                "and an arbitrary probability-minus-uniform discrepancy "
                "delta, Cauchy gives |<c_res,delta>| <= "
                "sqrt(n*(n-1)*energy(c_res)).  The schedule sums this crude "
                "bound over the four projected moduli."),
            "interpretation_boundary": (
                "This is deliberately pessimistic.  A real proof may exploit "
                "arithmetic cancellation, but coefficient truncation alone "
                "does not prove the residual harmless."),
        },
        "active_nonzero_character_count": len(modes),
        "minimum_local_main": local_main_minimum,
        "schedule": schedule,
        "candidate": {
            "name": "multiplicative-character truncation plus residual bound",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Prove pointwise binary-prime correlation estimates for a "
                "top character package, then separately bound the omitted "
                "residual character tail."),
            "prediction": (
                "If coefficient energy truncation were enough, the crude "
                "residual bound after the 99 percent package would be below "
                "the local main.  If not, a residual theorem is mandatory."),
            "falsifier": (
                "A residual bound far above local main after high-energy "
                "truncation falsifies coefficient-only truncation as a proof "
                "route."),
            "smallest_test": (
                "Compare crude residual bounds at 90, 95, 99 percent and "
                "near-complete character packages to the minimum local main."),
        },
        "decision": (
            "Coefficient-energy truncation alone cannot close the q286-WBSS "
            "pointwise target.  Keeping the 77-character 99 percent package "
            "still leaves a crude residual bound about 46.26, more than 76 "
            "times the minimum local main.  Even keeping 120 active "
            "characters leaves a crude residual bound about 1.318, still "
            "above the minimum local main.  The route requires either an "
            "explicit residual character theorem or the full active nonzero "
            "multiplicative-character package."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
