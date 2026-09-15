"""Build a first q286 cone-duality LP candidate.

This receipt tests the theorem-shaped cone:

    support + ordered-pair reflection + L1 distance from local uniform.

For each selected target residue modulo the assembled period M=10010, it asks
how close a reflected admissible probability measure can be to uniform while
still entering the bad q286 branch:

    first_three <= -0.3
    full_action <= 0

The resulting minimum L1 distance is a sufficient AP-uniformity budget: any
actual measure closer than that cannot be a bad row.  This is a cone-definition
and LP-duality diagnostic only.  It proves no AP theorem, no signed
prime-correlation theorem, no q286 threshold theorem, and no Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-cone-duality-l1-uniformity-candidate.json"
MODULUS = 286
PERIOD = 10010
TAIL_THRESHOLD = 0.3
TOLERANCE = 1e-8
SELECTED_TARGETS = (
    14138,
    14996,
    94856,
    1222142,
    1240888,
    1242118,
    1379072,
)

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    _prime_table,
    _unit_character_table,
)
from tools.build_q286_prime_indexed_kernel_route_audit import (  # noqa: E402
    logs,
    prime_indexed_residue_weights,
)
from tools.build_q286_prime_indexed_row_filter_order_audit import (  # noqa: E402
    optimized_filter_row,
    prepare_support_context,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, np.generic):
        return json_ready(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def finite_summary(values):
    finite = tuple(float(value) for value in values
                   if value is not None and math.isfinite(float(value)))
    if not finite:
        return {
            "count": 0,
            "minimum": None,
            "maximum": None,
            "mean": None,
        }
    return {
        "count": len(finite),
        "minimum": min(finite),
        "maximum": max(finite),
        "mean": math.fsum(finite) / len(finite),
    }


def q286_first_three_unit_coefficients(context):
    data = context["support_data"][(11, 13)]
    units = data["units"]
    _, labels, character_table = _unit_character_table(MODULUS, units)
    first_three_matrix = np.zeros((10, 12), dtype=np.complex128)
    first_three_matrix[1:, 1:] = sum(data["q286_mode_matrices"][:3])
    coefficients = []
    for column in range(len(units)):
        value = 0j
        for row, label in enumerate(labels):
            value += first_three_matrix[label] * character_table[row, column]
        coefficients.append(value)
    return {
        int(unit): complex(value)
        for unit, value in zip(units, coefficients)
    }


def period_full_unit_coefficients(context):
    coefficient = context["coefficient"]
    units = tuple(
        residue for residue in range(PERIOD)
        if math.gcd(residue, PERIOD) == 1)
    return {
        int(unit): complex(
            coefficient["aggregate_coefficient_by_unit_residue"][unit])
        for unit in units
    }


def admissible_units(target_residue):
    return tuple(
        residue for residue in range(PERIOD)
        if math.gcd(residue, PERIOD) == 1
        and math.gcd((target_residue - residue) % PERIOD, PERIOD) == 1)


def reflection_orbits(target_residue, units):
    unit_set = set(units)
    seen = set()
    orbits = []
    for unit in units:
        if unit in seen:
            continue
        reflected = (target_residue - unit) % PERIOD
        if reflected not in unit_set:
            raise AssertionError("reflection left admissible support")
        orbit = tuple(sorted({unit, reflected}))
        seen.update(orbit)
        orbits.append(orbit)
    return tuple(orbits)


def orbit_coefficients(target_residue, context, full_coefficients,
                       q286_first_three_coefficients):
    principal = float(context["principal_mean"].real)
    if abs(principal) <= TOLERANCE:
        raise AssertionError("principal normalization vanished")
    units = admissible_units(target_residue)
    orbits = reflection_orbits(target_residue, units)
    q286_target_residue = target_residue % MODULUS
    q286_units = context["support_data"][(11, 13)]["units"]
    q286_admissible = tuple(
        unit for unit in q286_units
        if math.gcd((q286_target_residue - unit) % MODULUS, MODULUS) == 1)
    q286_local_mean = complex(math.fsum(
        q286_first_three_coefficients[unit].real
        for unit in q286_admissible) / len(q286_admissible))
    first_three_by_period_unit = {
        unit: (
            q286_first_three_coefficients[unit % MODULUS]
            - q286_local_mean).real / principal
        for unit in units
    }
    full_by_period_unit = {
        unit: full_coefficients[unit].real / principal
        for unit in units
    }
    uniform_orbit_mass = np.asarray(
        [len(orbit) / len(units) for orbit in orbits], dtype=np.float64)
    first_three = np.asarray([
        math.fsum(first_three_by_period_unit[unit] for unit in orbit)
        / len(orbit)
        for orbit in orbits
    ], dtype=np.float64)
    full = np.asarray([
        math.fsum(full_by_period_unit[unit] for unit in orbit) / len(orbit)
        for orbit in orbits
    ], dtype=np.float64)
    return {
        "target_residue": int(target_residue),
        "admissible_units": units,
        "orbits": orbits,
        "uniform_orbit_mass": uniform_orbit_mass,
        "first_three_coefficients": first_three,
        "full_coefficients": full,
    }


def solve_nearest_bad(orbit_data):
    first_three = orbit_data["first_three_coefficients"]
    full = orbit_data["full_coefficients"]
    uniform = orbit_data["uniform_orbit_mass"]
    count = len(uniform)
    objective = np.r_[np.zeros(count), np.ones(count)]
    a_ub_rows = [
        np.r_[first_three, np.zeros(count)],
        np.r_[full, np.zeros(count)],
    ]
    b_ub = [-TAIL_THRESHOLD, 0.0]
    for index in range(count):
        row = np.zeros(2 * count)
        row[index] = 1.0
        row[count + index] = -1.0
        a_ub_rows.append(row)
        b_ub.append(float(uniform[index]))
        row = np.zeros(2 * count)
        row[index] = -1.0
        row[count + index] = -1.0
        a_ub_rows.append(row)
        b_ub.append(float(-uniform[index]))
    a_eq = np.zeros((1, 2 * count))
    a_eq[0, :count] = 1.0
    result = linprog(
        objective,
        A_ub=np.asarray(a_ub_rows, dtype=np.float64),
        b_ub=np.asarray(b_ub, dtype=np.float64),
        A_eq=a_eq,
        b_eq=np.asarray([1.0], dtype=np.float64),
        bounds=[(0.0, None)] * (2 * count),
        method="highs",
    )
    row = {
        "lp_success": bool(result.success),
        "lp_status": int(result.status),
        "lp_message": result.message,
    }
    if not result.success:
        return row
    masses = result.x[:count]
    deviations = masses - uniform
    first_three_value = float(np.dot(first_three, masses))
    full_value = float(np.dot(full, masses))
    l1 = float(np.sum(np.abs(deviations)))
    row.update({
        "minimum_bad_l1_from_uniform": l1,
        "minimum_bad_total_variation_from_uniform": 0.5 * l1,
        "bad_first_three_to_principal_ratio": first_three_value,
        "bad_full_action_to_principal_ratio": full_value,
        "bad_branch_slack": {
            "tail_slack": first_three_value + TAIL_THRESHOLD,
            "full_slack": full_value,
        },
        "largest_bad_orbit_masses": tuple(
            {
                "orbit": orbit_data["orbits"][index],
                "mass": float(masses[index]),
                "uniform_mass": float(uniform[index]),
                "signed_deviation": float(deviations[index]),
                "first_three_coefficient": float(first_three[index]),
                "full_coefficient": float(orbit_data[
                    "full_coefficients"][index]),
            }
            for index in np.argsort(-np.abs(deviations))[:12]),
    })
    return row


def actual_target_row(target, orbit_data, context, primes, prime_values,
                      log_values):
    count, total, weights = prime_indexed_residue_weights(
        target, primes, prime_values, log_values, PERIOD)
    if total <= TOLERANCE:
        return {
            "target": int(target),
            "pair_count": int(count),
            "total_weight": float(total),
            "actual_measure_available": False,
        }
    weight_by_residue = np.asarray(weights, dtype=np.float64) / total
    orbit_masses = np.asarray([
        math.fsum(float(weight_by_residue[unit]) for unit in orbit)
        for orbit in orbit_data["orbits"]
    ], dtype=np.float64)
    uniform = orbit_data["uniform_orbit_mass"]
    first_three = float(np.dot(
        orbit_data["first_three_coefficients"], orbit_masses))
    full = float(np.dot(orbit_data["full_coefficients"], orbit_masses))
    filter_row = optimized_filter_row(
        target, context, primes, prime_values, log_values)
    first_three_reference = float(
        filter_row["first_three_modes_to_principal_ratio"])
    full_reference = float(filter_row["full_action_to_principal_ratio"])
    return {
        "target": int(target),
        "target_residue": int(target % PERIOD),
        "pair_count": int(count),
        "total_weight": float(total),
        "actual_measure_available": True,
        "actual_l1_from_uniform": float(np.sum(np.abs(orbit_masses - uniform))),
        "actual_total_variation_from_uniform": float(
            0.5 * np.sum(np.abs(orbit_masses - uniform))),
        "actual_first_three_to_principal_ratio": first_three,
        "actual_full_action_to_principal_ratio": full,
        "reference_first_three_to_principal_ratio": first_three_reference,
        "reference_full_action_to_principal_ratio": full_reference,
        "first_three_reconstruction_error": abs(
            first_three - first_three_reference),
        "full_reconstruction_error": abs(full - full_reference),
        "actual_bad_branch": bool(
            first_three <= -TAIL_THRESHOLD + TOLERANCE
            and full <= TOLERANCE),
        "passes_l1_uniformity_certificate": None,
    }


def main():
    selected_targets = tuple(dict.fromkeys(int(t) for t in SELECTED_TARGETS))
    maximum_target = max(selected_targets)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)

    residue_rows = []
    target_rows = []
    maximum_reconstruction_error = 0.0
    for target_residue in tuple(dict.fromkeys(
            target % PERIOD for target in selected_targets)):
        orbit_data = orbit_coefficients(
            target_residue, context, full_coefficients,
            first_three_coefficients)
        lp_row = solve_nearest_bad(orbit_data)
        residue_rows.append({
            "target_residue": int(target_residue),
            "target_mod_286": int(target_residue % MODULUS),
            "admissible_unit_count": len(orbit_data["admissible_units"]),
            "reflection_orbit_count": len(orbit_data["orbits"]),
            **lp_row,
        })
    residue_by_mod = {row["target_residue"]: row for row in residue_rows}
    for target in selected_targets:
        orbit_data = orbit_coefficients(
            target % PERIOD, context, full_coefficients,
            first_three_coefficients)
        actual = actual_target_row(
            target, orbit_data, context, primes, prime_values, log_values)
        budget = residue_by_mod[target % PERIOD].get(
            "minimum_bad_l1_from_uniform")
        if budget is not None and actual["actual_measure_available"]:
            actual["passes_l1_uniformity_certificate"] = (
                actual["actual_l1_from_uniform"] < budget - TOLERANCE)
            actual["actual_l1_over_minimum_bad_l1"] = (
                actual["actual_l1_from_uniform"] / budget
                if budget > TOLERANCE else math.inf)
        maximum_reconstruction_error = max(
            maximum_reconstruction_error,
            actual.get("first_three_reconstruction_error", 0.0),
            actual.get("full_reconstruction_error", 0.0))
        target_rows.append(actual)

    feasible_rows = tuple(row for row in residue_rows if row["lp_success"])
    certified_targets = tuple(
        row for row in target_rows
        if row.get("passes_l1_uniformity_certificate") is True)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "cone-definition and LP-uniformity diagnostic only; it computes "
            "how strong an L1 AP-uniformity cone would need to be to exclude "
            "the q286 bad branch on selected residues. It proves no AP "
            "uniformity theorem, no signed prime-correlation theorem, no "
            "q286 threshold theorem, and no Goldbach theorem."),
        "candidate_cone": (
            "For each target residue a modulo 10010, K_a(rho) consists of "
            "nonnegative probability measures on admissible unit residues, "
            "symmetric under r -> a-r, with L1 distance at most rho from the "
            "local uniform admissible measure."),
        "bad_branch": {
            "first_three_to_principal_ratio_at_most": -TAIL_THRESHOLD,
            "full_action_to_principal_ratio_at_most": 0.0,
            "equivalent_form": (
                "On a first-three tail, full<=0 is the same failed rescue "
                "branch as C<=-F3 because full=F3+C."),
        },
        "prediction": (
            "If a fixed-modulus binary-prime AP theorem proves "
            "||mu_N-uniform||_1 below the computed minimum_bad_l1 for a "
            "target residue, then the bad branch is impossible for that "
            "residue."),
        "falsifier": (
            "A feasible LP point gives a synthetic reflected admissible "
            "measure in the bad branch, proving support/reflection alone is "
            "insufficient and quantifying the required L1 radius."),
        "selected_targets": selected_targets,
        "residue_rows": residue_rows,
        "target_rows": target_rows,
        "summary": {
            "selected_target_count": len(selected_targets),
            "selected_residue_count": len(residue_rows),
            "lp_feasible_bad_residue_count": len(feasible_rows),
            "lp_infeasible_bad_residue_count": (
                len(residue_rows) - len(feasible_rows)),
            "minimum_bad_l1_summary": finite_summary(
                row.get("minimum_bad_l1_from_uniform")
                for row in residue_rows),
            "minimum_bad_total_variation_summary": finite_summary(
                row.get("minimum_bad_total_variation_from_uniform")
                for row in residue_rows),
            "actual_l1_summary": finite_summary(
                row.get("actual_l1_from_uniform")
                for row in target_rows),
            "actual_targets_passing_l1_uniformity_certificate": tuple(
                row["target"] for row in certified_targets),
            "actual_target_certificate_pass_count": len(certified_targets),
            "maximum_reconstruction_error": maximum_reconstruction_error,
        },
        "decision": (
            "The L1-uniformity cone is a valid theorem target but must be "
            "checked against actual-row distances. If actual clear rows do "
            "not satisfy the sufficient L1 budgets, this cone is too strong "
            "as the main proof mechanism, though it remains a possible "
            "analytic sufficient condition after a finite boundary check."),
        "next_obligation": (
            "Either source an explicit AP/binary-Goldbach-in-progressions "
            "bound strong enough for these L1 budgets, or replace the L1 ball "
            "with a coefficient-sensitive cone such as signed character "
            "moments or q286 mass/landing inequalities."),
        "goldbach_proved": False,
    }
    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
