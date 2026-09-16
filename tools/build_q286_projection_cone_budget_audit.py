"""Audit q286 projection-uniformity cones against the signed bad branch.

The raw sign-split and anti-landing routes both need sharp signed
binary-prime control.  A natural next attempt is to use lower-dimensional
equidistribution: force the reflected strict-central prime-pair measure to
look uniform after projection to small factors or to q286 itself.

This receipt asks three LP questions on the frozen signed-pair operator rows:

1. Do exact prime-factor marginals exclude the bad branch?
2. Does exact q286 projection uniformity exclude the bad branch?
3. If q286 projection uniformity is only approximate, how small must the
   projected total-variation/L-infinity error be before every bad synthetic
   measure is excluded?

Finite theorem-shaping audit only.  It proves no projection-uniformity
theorem, signed binary-prime correlation theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.
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
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-projection-cone-budget-audit.json"
PERIOD = 10010
PROJECTION_MODULUS = 286
PRIME_FACTOR_MODULI = (2, 5, 7, 11, 13)
TAIL_THRESHOLD = 0.3
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

from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    orbit_coefficients,
    period_full_unit_coefficients,
    prepare_support_context,
    q286_first_three_unit_coefficients,
)
from tools.build_q286_lower_face_overlap_audit import (  # noqa: E402
    actual_orbit_measure,
)
from tools.build_q286_prime_indexed_kernel_route_audit import logs  # noqa: E402


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def finite_summary(values):
    finite = tuple(
        float(value) for value in values
        if value is not None and math.isfinite(float(value)))
    if not finite:
        return {"count": 0, "minimum": None, "mean": None, "maximum": None}
    return {
        "count": len(finite),
        "minimum": min(finite),
        "mean": math.fsum(finite) / len(finite),
        "maximum": max(finite),
    }


def projection_matrix(orbit_data, modulus):
    orbits = orbit_data["orbits"]
    uniform = orbit_data["uniform_orbit_mass"]
    residues = sorted({unit % modulus for orbit in orbits for unit in orbit})
    rows = []
    for residue in residues:
        rows.append([
            sum(1 for unit in orbit if unit % modulus == residue) / len(orbit)
            for orbit in orbits
        ])
    matrix = np.asarray(rows, dtype=np.float64)
    uniform_projection = matrix @ uniform
    return residues, matrix, uniform_projection


def exact_projection_bad_feasibility(orbit_data, moduli):
    count = len(orbit_data["uniform_orbit_mass"])
    a_ub = np.vstack([
        orbit_data["first_three_coefficients"],
        orbit_data["full_coefficients"],
    ])
    b_ub = np.asarray([-TAIL_THRESHOLD, 0.0], dtype=np.float64)
    a_eq = [np.ones(count, dtype=np.float64)]
    b_eq = [1.0]
    projected_residue_counts = {}
    for modulus in moduli:
        residues, matrix, uniform_projection = projection_matrix(
            orbit_data, modulus)
        projected_residue_counts[str(modulus)] = len(residues)
        # One projected row per modulus is redundant with total mass.
        a_eq.extend(matrix[:-1])
        b_eq.extend(uniform_projection[:-1])
    result = linprog(
        np.zeros(count, dtype=np.float64),
        A_ub=a_ub,
        b_ub=b_ub,
        A_eq=np.vstack(a_eq),
        b_eq=np.asarray(b_eq, dtype=np.float64),
        bounds=[(0.0, None)] * count,
        method="highs",
    )
    row = {
        "bad_measure_feasible": bool(result.success),
        "lp_status": int(result.status),
        "lp_message": result.message,
        "equality_constraint_count": len(b_eq),
        "projection_residue_counts": projected_residue_counts,
    }
    if result.success:
        masses = result.x
        row.update({
            "bad_first_three": float(
                np.dot(orbit_data["first_three_coefficients"], masses)),
            "bad_full_action": float(
                np.dot(orbit_data["full_coefficients"], masses)),
            "synthetic_support_count": int(np.sum(masses > 1e-10)),
            "synthetic_max_orbit_mass": float(np.max(masses)),
            "synthetic_l1_from_full_uniform": float(np.sum(
                np.abs(masses - orbit_data["uniform_orbit_mass"]))),
        })
    return row


def minimum_bad_projected_l1(orbit_data, modulus):
    residues, matrix, uniform_projection = projection_matrix(
        orbit_data, modulus)
    count = len(orbit_data["uniform_orbit_mass"])
    projected_count = len(residues)
    objective = np.r_[np.zeros(count), np.ones(projected_count)]
    a_ub = [
        np.r_[orbit_data["first_three_coefficients"],
              np.zeros(projected_count)],
        np.r_[orbit_data["full_coefficients"], np.zeros(projected_count)],
    ]
    b_ub = [-TAIL_THRESHOLD, 0.0]
    for index in range(projected_count):
        row = np.zeros(count + projected_count)
        row[:count] = matrix[index]
        row[count + index] = -1.0
        a_ub.append(row)
        b_ub.append(float(uniform_projection[index]))
        row = np.zeros(count + projected_count)
        row[:count] = -matrix[index]
        row[count + index] = -1.0
        a_ub.append(row)
        b_ub.append(float(-uniform_projection[index]))
    a_eq = np.zeros((1, count + projected_count), dtype=np.float64)
    a_eq[0, :count] = 1.0
    result = linprog(
        objective,
        A_ub=np.asarray(a_ub, dtype=np.float64),
        b_ub=np.asarray(b_ub, dtype=np.float64),
        A_eq=a_eq,
        b_eq=np.asarray([1.0], dtype=np.float64),
        bounds=[(0.0, None)] * (count + projected_count),
        method="highs",
    )
    row = {
        "lp_success": bool(result.success),
        "lp_status": int(result.status),
        "lp_message": result.message,
        "projection_modulus": int(modulus),
        "projection_residue_count": projected_count,
    }
    if result.success:
        masses = result.x[:count]
        projected = matrix @ masses
        deltas = projected - uniform_projection
        row.update({
            "minimum_bad_projection_l1": float(np.sum(np.abs(deltas))),
            "minimum_bad_projection_total_variation": float(
                0.5 * np.sum(np.abs(deltas))),
            "minimum_bad_projection_linf_for_this_l1_solution": float(
                np.max(np.abs(deltas))),
            "bad_first_three": float(
                np.dot(orbit_data["first_three_coefficients"], masses)),
            "bad_full_action": float(
                np.dot(orbit_data["full_coefficients"], masses)),
            "synthetic_support_count": int(np.sum(masses > 1e-10)),
            "synthetic_max_orbit_mass": float(np.max(masses)),
        })
    return row


def minimum_bad_projected_linf(orbit_data, modulus):
    residues, matrix, uniform_projection = projection_matrix(
        orbit_data, modulus)
    count = len(orbit_data["uniform_orbit_mass"])
    objective = np.r_[np.zeros(count), 1.0]
    a_ub = [
        np.r_[orbit_data["first_three_coefficients"], 0.0],
        np.r_[orbit_data["full_coefficients"], 0.0],
    ]
    b_ub = [-TAIL_THRESHOLD, 0.0]
    for index in range(len(residues)):
        row = np.zeros(count + 1)
        row[:count] = matrix[index]
        row[-1] = -1.0
        a_ub.append(row)
        b_ub.append(float(uniform_projection[index]))
        row = np.zeros(count + 1)
        row[:count] = -matrix[index]
        row[-1] = -1.0
        a_ub.append(row)
        b_ub.append(float(-uniform_projection[index]))
    a_eq = np.zeros((1, count + 1), dtype=np.float64)
    a_eq[0, :count] = 1.0
    result = linprog(
        objective,
        A_ub=np.asarray(a_ub, dtype=np.float64),
        b_ub=np.asarray(b_ub, dtype=np.float64),
        A_eq=a_eq,
        b_eq=np.asarray([1.0], dtype=np.float64),
        bounds=[(0.0, None)] * (count + 1),
        method="highs",
    )
    row = {
        "lp_success": bool(result.success),
        "lp_status": int(result.status),
        "lp_message": result.message,
        "projection_modulus": int(modulus),
        "projection_residue_count": len(residues),
    }
    if result.success:
        masses = result.x[:count]
        projected = matrix @ masses
        deltas = projected - uniform_projection
        row.update({
            "minimum_bad_projection_linf": float(np.max(np.abs(deltas))),
            "bad_projection_l1_for_this_linf_solution": float(
                np.sum(np.abs(deltas))),
            "bad_first_three": float(
                np.dot(orbit_data["first_three_coefficients"], masses)),
            "bad_full_action": float(
                np.dot(orbit_data["full_coefficients"], masses)),
            "synthetic_support_count": int(np.sum(masses > 1e-10)),
            "synthetic_max_orbit_mass": float(np.max(masses)),
        })
    return row


def actual_projection_metrics(orbit_data, masses, modulus):
    _, matrix, uniform_projection = projection_matrix(orbit_data, modulus)
    projected = matrix @ masses
    deltas = projected - uniform_projection
    return {
        "actual_projection_l1": float(np.sum(np.abs(deltas))),
        "actual_projection_total_variation": float(
            0.5 * np.sum(np.abs(deltas))),
        "actual_projection_linf": float(np.max(np.abs(deltas))),
    }


def build_receipt():
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    maximum_target = max(SELECTED_TARGETS)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)

    rows = []
    for target in SELECTED_TARGETS:
        orbit_data = orbit_coefficients(
            target % PERIOD,
            context,
            full_coefficients,
            first_three_coefficients,
        )
        actual = actual_orbit_measure(
            target,
            {
                "orbits": orbit_data["orbits"],
                "first_three": orbit_data["first_three_coefficients"],
                "full": orbit_data["full_coefficients"],
            },
            primes,
            prime_values,
            log_values,
        )
        masses = np.asarray(actual["masses"], dtype=np.float64)
        min_l1 = minimum_bad_projected_l1(
            orbit_data, PROJECTION_MODULUS)
        min_linf = minimum_bad_projected_linf(
            orbit_data, PROJECTION_MODULUS)
        actual_projection = actual_projection_metrics(
            orbit_data, masses, PROJECTION_MODULUS)
        row = {
            "target": int(target),
            "target_residue": int(target % PERIOD),
            "target_mod_286": int(target % PROJECTION_MODULUS),
            "reflection_orbit_count": int(len(orbit_data["orbits"])),
            "actual_first_three": float(
                np.dot(orbit_data["first_three_coefficients"], masses)),
            "actual_full_action": float(
                np.dot(orbit_data["full_coefficients"], masses)),
            "prime_factor_exact_marginal_cone": (
                exact_projection_bad_feasibility(
                    orbit_data, PRIME_FACTOR_MODULI)),
            "exact_q286_projection_uniform_cone": (
                exact_projection_bad_feasibility(
                    orbit_data, (PROJECTION_MODULUS,))),
            "minimum_bad_q286_projection_l1": min_l1,
            "minimum_bad_q286_projection_linf": min_linf,
            "actual_q286_projection": actual_projection,
            "actual_tv_exceeds_minimum_bad_tv": bool(
                actual_projection["actual_projection_total_variation"]
                > min_l1["minimum_bad_projection_total_variation"]),
            "actual_linf_exceeds_minimum_bad_linf": bool(
                actual_projection["actual_projection_linf"]
                > min_linf["minimum_bad_projection_linf"]),
        }
        rows.append(row)

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "HOLD_projection_uniformity_sufficient_but_too_strong",
        "status_boundary": (
            "finite projection-cone LP audit only; no projection-uniformity "
            "theorem, signed binary-prime correlation theorem, q286 threshold "
            "theorem, strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "projection_uniformity_theorem_proved": False,
        "signed_binary_prime_correlation_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "q286 projection-uniformity cone",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Instead of controlling the full reflected residue measure, "
                "try to exclude the q286 bad branch using only exact or "
                "near-exact projection of that measure to lower moduli."),
            "prediction": (
                "If projection uniformity is the right analytic bridge, "
                "prime-factor or q286 projected constraints should exclude "
                "synthetic bad measures at tolerances comparable with the "
                "actual checked rows."),
            "falsifier": (
                "A feasible synthetic bad measure with the proposed projected "
                "constraints proves that those constraints are insufficient. "
                "If the sufficient q286 projection tolerance is far below the "
                "actual row deviations, plain projection uniformity is too "
                "strong as an acceptance condition."),
            "smallest_test": (
                "Run LP bad-branch feasibility under exact prime-factor "
                "marginals, exact q286 projection uniformity, and minimum "
                "q286 projected L1/Linf distance from uniform on the seven "
                "frozen signed-pair operator targets."),
        },
        "bad_branch_constraints": {
            "first_three_action_at_most": -TAIL_THRESHOLD,
            "full_action_at_most": 0.0,
        },
        "projection_modulus": PROJECTION_MODULUS,
        "prime_factor_moduli": list(PRIME_FACTOR_MODULI),
        "selected_targets": list(SELECTED_TARGETS),
        "summary": {
            "selected_target_count": len(rows),
            "prime_factor_exact_marginal_bad_feasible_count": sum(
                row["prime_factor_exact_marginal_cone"][
                    "bad_measure_feasible"]
                for row in rows),
            "exact_q286_projection_uniform_bad_feasible_count": sum(
                row["exact_q286_projection_uniform_cone"][
                    "bad_measure_feasible"]
                for row in rows),
            "actual_tv_exceeds_minimum_bad_tv_count": sum(
                row["actual_tv_exceeds_minimum_bad_tv"] for row in rows),
            "actual_linf_exceeds_minimum_bad_linf_count": sum(
                row["actual_linf_exceeds_minimum_bad_linf"] for row in rows),
            "minimum_bad_q286_projection_tv_summary": finite_summary(
                row["minimum_bad_q286_projection_l1"][
                    "minimum_bad_projection_total_variation"]
                for row in rows),
            "minimum_bad_q286_projection_linf_summary": finite_summary(
                row["minimum_bad_q286_projection_linf"][
                    "minimum_bad_projection_linf"]
                for row in rows),
            "actual_q286_projection_tv_summary": finite_summary(
                row["actual_q286_projection"][
                    "actual_projection_total_variation"]
                for row in rows),
            "actual_q286_projection_linf_summary": finite_summary(
                row["actual_q286_projection"]["actual_projection_linf"]
                for row in rows),
            "tightest_minimum_bad_tv_row": min(
                rows,
                key=lambda row: (
                    row["minimum_bad_q286_projection_l1"][
                        "minimum_bad_projection_total_variation"],
                    row["target"],
                ),
            ),
        },
        "decision": (
            "Prime-factor projection data is too weak: exact uniform "
            "marginals modulo 2,5,7,11,13 still allow synthetic bad measures "
            "on every frozen target.  Exact q286 projection uniformity is "
            "sufficient on these rows, but the quantitative q286 TV/Linf "
            "budgets are far stronger than the actual checked prime-pair "
            "projection deviations.  Therefore plain projection uniformity "
            "does not earn acceptance as the next bridge.  The proof object "
            "still has to be coefficient-sensitive signed binary-prime "
            "correlation, not only lower-dimensional AP equidistribution."),
        "target_rows": rows,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
