"""Audit the q286 coefficient-only convex envelope obstruction.

The landing-cone route needs an arithmetic reason actual strict-central
prime-pair measures avoid the bad lower face.  This receipt computes that
lower face directly: for a target residue and a fixed first-three value, solve

    min Full(mu)
    subject to support/reflection simplex and F3(mu) = observed F3.

If the coefficient-only lower envelope is far below the actual row, then the
remaining theorem is not a coefficient-geometry theorem.  It is an
anti-extremality or signed prime-correlation theorem for the actual measure.

Finite diagnostic only.  It proves no cone theorem, signed correlation
estimate, threshold theorem, or Goldbach theorem.
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
OUT = EVIDENCE / "q286-convex-envelope-obstruction-audit.json"
SOURCE = EVIDENCE / "q286-nonprincipal-drag-envelope-audit.json"
TAIL_THRESHOLD = 0.3
PERIOD = 10010
MODULUS = 286
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

from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    orbit_coefficients,
    period_full_unit_coefficients,
    prepare_support_context,
    q286_first_three_unit_coefficients,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


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
    finite = tuple(
        float(value) for value in values
        if value is not None and math.isfinite(float(value)))
    if not finite:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None}
    return {
        "count": len(finite),
        "minimum": min(finite),
        "maximum": max(finite),
        "mean": math.fsum(finite) / len(finite),
    }


def solve_linear(coefficients, objective, *, equalities=(), inequalities=()):
    count = len(objective)
    a_eq = [np.ones(count, dtype=np.float64)]
    b_eq = [1.0]
    for vector, value in equalities:
        a_eq.append(np.asarray(vector, dtype=np.float64))
        b_eq.append(float(value))
    a_ub = []
    b_ub = []
    for vector, value in inequalities:
        a_ub.append(np.asarray(vector, dtype=np.float64))
        b_ub.append(float(value))
    result = linprog(
        np.asarray(objective, dtype=np.float64),
        A_ub=(np.asarray(a_ub, dtype=np.float64) if a_ub else None),
        b_ub=(np.asarray(b_ub, dtype=np.float64) if b_ub else None),
        A_eq=np.asarray(a_eq, dtype=np.float64),
        b_eq=np.asarray(b_eq, dtype=np.float64),
        bounds=[(0.0, None)] * count,
        method="highs",
    )
    row = {
        "success": bool(result.success),
        "status": int(result.status),
        "message": result.message,
    }
    if not result.success:
        return row
    masses = result.x
    row.update({
        "objective_value": float(result.fun),
        "first_three_value": float(np.dot(coefficients["first_three"], masses)),
        "full_value": float(np.dot(coefficients["full"], masses)),
        "support_size": int(np.sum(masses > TOLERANCE)),
        "largest_orbit_masses": tuple(
            {
                "orbit": coefficients["orbits"][index],
                "mass": float(masses[index]),
                "first_three_coefficient": float(
                    coefficients["first_three"][index]),
                "full_coefficient": float(coefficients["full"][index]),
            }
            for index in np.argsort(-masses)[:8]
            if masses[index] > TOLERANCE),
    })
    return row


def coefficient_row(target_residue, context, full_coefficients,
                    first_three_coefficients):
    orbit_data = orbit_coefficients(
        target_residue, context, full_coefficients, first_three_coefficients)
    return {
        "target_residue": int(target_residue),
        "target_mod_286": int(target_residue % MODULUS),
        "orbits": orbit_data["orbits"],
        "first_three": np.asarray(
            orbit_data["first_three_coefficients"], dtype=np.float64),
        "full": np.asarray(orbit_data["full_coefficients"], dtype=np.float64),
    }


def actual_source_rows(source):
    rows = []
    for block in source["block_summaries"]:
        for key in ("largest_drag_to_margin_rows", "tightest_drag_surplus_rows"):
            rows.extend(block["envelope_summary"][key])
    for target in SELECTED_TARGETS:
        for block in source["block_summaries"]:
            for row in block["envelope_summary"]["tightest_drag_surplus_rows"]:
                if int(row["target"]) == target:
                    rows.append(row)
            for row in block["envelope_summary"]["largest_drag_to_margin_rows"]:
                if int(row["target"]) == target:
                    rows.append(row)
    dedup = {}
    for row in rows:
        dedup[int(row["target"])] = row
    return tuple(sorted(dedup.values(), key=lambda row: int(row["target"])))


def analyze_target(row, coefficients):
    first_three_value = float(row["first_three_modes_to_principal_ratio"])
    full_value = float(row["full_action_to_principal_ratio"])
    lower = solve_linear(
        coefficients,
        coefficients["full"],
        equalities=((coefficients["first_three"], first_three_value),),
    )
    upper = solve_linear(
        coefficients,
        -coefficients["full"],
        equalities=((coefficients["first_three"], first_three_value),),
    )
    if upper["success"]:
        upper["full_value"] = -upper["objective_value"]
    position = None
    if lower["success"] and upper["success"]:
        span = upper["full_value"] - lower["full_value"]
        if span > TOLERANCE:
            position = (full_value - lower["full_value"]) / span
    return {
        "target": int(row["target"]),
        "target_residue": int(row["target"] % PERIOD),
        "target_mod_286": int(row["target_mod_286"]),
        "block_index_after_discovery": int(row["block_index_after_discovery"]),
        "actual_first_three": first_three_value,
        "actual_full": full_value,
        "actual_full_positive": bool(full_value > TOLERANCE),
        "coefficient_lower_envelope": lower,
        "coefficient_upper_envelope": upper,
        "actual_surplus_above_lower_envelope": (
            full_value - lower["full_value"] if lower["success"] else None),
        "actual_position_between_envelopes": position,
    }


def analyze_residue(coefficients):
    tail_bad = solve_linear(
        coefficients,
        coefficients["full"],
        inequalities=((coefficients["first_three"], -TAIL_THRESHOLD),),
    )
    tail_failure = solve_linear(
        coefficients,
        coefficients["first_three"],
        inequalities=((coefficients["first_three"], -TAIL_THRESHOLD),
                      (coefficients["full"], 0.0)),
    )
    max_f3_with_full_nonpositive = solve_linear(
        coefficients,
        -coefficients["first_three"],
        inequalities=((coefficients["full"], 0.0),),
    )
    if max_f3_with_full_nonpositive["success"]:
        max_f3_with_full_nonpositive["first_three_value"] = (
            -max_f3_with_full_nonpositive["objective_value"])
    return {
        "target_residue": coefficients["target_residue"],
        "target_mod_286": coefficients["target_mod_286"],
        "reflection_orbit_count": len(coefficients["orbits"]),
        "first_three_coefficient_range": {
            "minimum": float(np.min(coefficients["first_three"])),
            "maximum": float(np.max(coefficients["first_three"])),
        },
        "full_coefficient_range": {
            "minimum": float(np.min(coefficients["full"])),
            "maximum": float(np.max(coefficients["full"])),
        },
        "minimum_full_on_tail_halfspace": tail_bad,
        "tail_and_full_failure_feasible": bool(tail_failure["success"]),
        "one_synthetic_tail_failure": tail_failure,
        "maximum_first_three_with_full_nonpositive": (
            max_f3_with_full_nonpositive),
    }


def build_receipt():
    source = load_json(SOURCE)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    actual_rows = actual_source_rows(source)
    residues = tuple(dict.fromkeys(
        int(row["target"]) % PERIOD for row in actual_rows))
    coefficient_by_residue = {
        residue: coefficient_row(
            residue, context, full_coefficients, first_three_coefficients)
        for residue in residues
    }
    residue_rows = tuple(
        analyze_residue(coefficient_by_residue[residue])
        for residue in residues)
    target_rows = tuple(
        analyze_target(row, coefficient_by_residue[int(row["target"]) % PERIOD])
        for row in actual_rows)
    post_rows = tuple(
        row for row in target_rows if row["block_index_after_discovery"] >= 1)
    discovery_rows = tuple(
        row for row in target_rows if row["block_index_after_discovery"] == 0)
    synthetic_failure_count = sum(
        row["tail_and_full_failure_feasible"] for row in residue_rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "nonprincipal_drag_envelope": str(SOURCE.relative_to(ROOT)),
            "coefficient_builder":
                "tools/build_q286_cone_duality_l1_uniformity_candidate.py",
        },
        "status_boundary": (
            "finite coefficient-envelope obstruction audit only; it proves no "
            "anti-extremality theorem, signed prime-correlation estimate, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach theorem."),
        "curiosity_synthesis": {
            "question": (
                "Is the remaining hole a lack of coefficient geometry, or a "
                "missing theorem that actual prime-pair measures avoid the "
                "lower convex face of that geometry?"),
            "candidate": "q286 coefficient-envelope anti-extremality problem",
            "mechanism": (
                "The reflection simplex pushes forward to a convex hull in "
                "the (F3, Full) plane.  LP gives the exact lower face."),
            "prediction": (
                "Support/reflection geometry should admit synthetic tail "
                "failures, while actual later rows should sit above the lower "
                "face; the gap is the theorem to prove."),
            "falsifier": (
                "If the bad branch is infeasible in the hull, coefficient "
                "geometry alone closes it.  If an actual later row lies on or "
                "below the lower face with Full<=0, the finite threshold "
                "candidate is falsified."),
            "smallest_test": (
                "Compute lower and upper Full envelopes at the observed F3 "
                "values for pre-existing tight rows from the drag-envelope "
                "receipt; no new target scan and no fitted row labels."),
            "novelty_label": "new-to-this-task",
        },
        "residue_rows": residue_rows,
        "target_rows": target_rows,
        "summary": {
            "target_row_count": len(target_rows),
            "residue_count": len(residue_rows),
            "synthetic_tail_failure_residue_count": synthetic_failure_count,
            "discovery_target_count": len(discovery_rows),
            "post_discovery_target_count": len(post_rows),
            "actual_surplus_above_lower_envelope_summary": finite_summary(
                row["actual_surplus_above_lower_envelope"]
                for row in target_rows),
            "post_discovery_actual_surplus_above_lower_envelope_summary":
                finite_summary(
                    row["actual_surplus_above_lower_envelope"]
                    for row in post_rows),
            "actual_position_between_envelopes_summary": finite_summary(
                row["actual_position_between_envelopes"]
                for row in target_rows),
            "post_discovery_position_between_envelopes_summary":
                finite_summary(
                    row["actual_position_between_envelopes"]
                    for row in post_rows),
            "minimum_full_on_tail_halfspace_summary": finite_summary(
                row["minimum_full_on_tail_halfspace"].get("full_value")
                for row in residue_rows
                if row["minimum_full_on_tail_halfspace"]["success"]),
        },
        "decision": (
            "If synthetic tail failures exist in every tested residue, the "
            "q286 proof cannot come from support/reflection/coefficient "
            "geometry alone.  The proof target becomes anti-extremality of "
            "actual prime-pair landing against the lower convex envelope."),
        "next_obligation": (
            "Define a source-backed arithmetic condition that lifts actual "
            "strict-central prime-pair measures away from the lower envelope: "
            "for example a signed two-prime AP estimate, a coefficient-matched "
            "moment inequality, or a transport entropy/maximum-density rule."),
        "anti_extremality_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "q286_threshold_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    payload = build_receipt()
    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(json.dumps({
        "wrote": str(OUT.relative_to(ROOT)),
        "target_row_count": payload["summary"]["target_row_count"],
        "residue_count": payload["summary"]["residue_count"],
        "synthetic_tail_failure_residue_count": (
            payload["summary"]["synthetic_tail_failure_residue_count"]),
        "goldbach_proved": payload["goldbach_proved"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
