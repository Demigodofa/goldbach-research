"""Build the q286 orthogonal-rescue decomposition.

The signed pair-correlation definition freezes two coefficient functionals:
first-three pressure and full action.  This receipt decomposes the centered
full-action coefficient into the uniform-weighted projection onto the
first-three coefficient plus an orthogonal residual:

    gamma_full_centered = alpha * gamma_F3 + h
    <h, gamma_F3>_u = 0.

For an actual target row:

    full = uniform_full + alpha * first_three + <nu_N, h>.

This isolates the next theorem obligation.  The q286 hole closes when the
orthogonal residual does not erase the positive aligned-only margin.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-orthogonal-rescue-decomposition.json"
L1_SOURCE = ROOT / "evidence" / "q286-cone-duality-l1-uniformity-candidate.json"
PERIOD = 10010
MODULUS = 286
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    SELECTED_TARGETS,
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


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set)):
        return [json_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, np.generic):
        return json_ready(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def finite_summary(values):
    finite = tuple(float(value) for value in values if math.isfinite(float(value)))
    if not finite:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None}
    return {
        "count": len(finite),
        "minimum": min(finite),
        "maximum": max(finite),
        "mean": math.fsum(finite) / len(finite),
    }


def load_actual_rows():
    receipt = json.loads(L1_SOURCE.read_text(encoding="utf-8"))
    return {int(row["target"]): row for row in receipt["target_rows"]}


def weighted_inner(weight, left, right):
    return float(np.dot(weight, left * right))


def weighted_norm(weight, vector):
    return math.sqrt(max(0.0, weighted_inner(weight, vector, vector)))


def residue_operator(target_residue, context, full_coefficients,
                     first_three_coefficients):
    orbit_data = orbit_coefficients(
        target_residue, context, full_coefficients, first_three_coefficients)
    uniform = orbit_data["uniform_orbit_mass"]
    first_three = orbit_data["first_three_coefficients"]
    full = orbit_data["full_coefficients"]
    uniform_full = float(np.dot(full, uniform))
    uniform_first_three = float(np.dot(first_three, uniform))
    centered_full = full - uniform_full
    denominator = weighted_inner(uniform, first_three, first_three)
    if abs(denominator) <= TOLERANCE:
        raise AssertionError("first-three coefficient has zero weighted norm")
    alpha = weighted_inner(uniform, first_three, centered_full) / denominator
    residual = centered_full - alpha * first_three
    return {
        "target_residue": int(target_residue),
        "target_mod_286": int(target_residue % MODULUS),
        "uniform_full_action_to_principal": uniform_full,
        "uniform_first_three_to_principal": uniform_first_three,
        "projection_alpha": alpha,
        "first_three_weighted_norm": weighted_norm(uniform, first_three),
        "centered_full_weighted_norm": weighted_norm(uniform, centered_full),
        "orthogonal_residual_weighted_norm": weighted_norm(uniform, residual),
        "orthogonality_error": abs(weighted_inner(uniform, residual, first_three)),
        "aligned_full_zero_first_three_floor": (
            -uniform_full / alpha if alpha > TOLERANCE else None),
        "residual_to_first_three_norm_ratio": (
            weighted_norm(uniform, residual) / weighted_norm(uniform, first_three)),
        "reflection_orbit_count": len(uniform),
    }


def target_decomposition(target, operator, actual):
    first_three = float(actual["actual_first_three_to_principal_ratio"])
    full = float(actual["actual_full_action_to_principal_ratio"])
    aligned_only = (
        operator["uniform_full_action_to_principal"]
        + operator["projection_alpha"] * first_three)
    orthogonal_residual = full - aligned_only
    required_residual_lower_bound = -aligned_only
    return {
        "target": int(target),
        "target_residue": int(target % PERIOD),
        "target_mod_286": int(target % MODULUS),
        "actual_first_three_to_principal_ratio": first_three,
        "actual_full_action_to_principal_ratio": full,
        "uniform_full_action_to_principal": (
            operator["uniform_full_action_to_principal"]),
        "projection_alpha": operator["projection_alpha"],
        "aligned_only_full_action_to_principal": aligned_only,
        "orthogonal_residual_action_to_principal": orthogonal_residual,
        "required_orthogonal_residual_lower_bound_for_positive_full": (
            required_residual_lower_bound),
        "orthogonal_residual_surplus_to_positive_full": (
            orthogonal_residual - required_residual_lower_bound),
        "aligned_only_positive": aligned_only > 0.0,
        "actual_full_positive": full > 0.0,
        "orthogonal_residual_erases_aligned_margin": (
            aligned_only > 0.0
            and orthogonal_residual <= required_residual_lower_bound
            + TOLERANCE),
        "actual_bad_branch": bool(actual["actual_bad_branch"]),
    }


def main():
    actual_rows = load_actual_rows()
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    residues = tuple(dict.fromkeys(target % PERIOD for target in SELECTED_TARGETS))
    operators = {
        residue: residue_operator(
            residue, context, full_coefficients, first_three_coefficients)
        for residue in residues
    }
    target_rows = [
        target_decomposition(
            target, operators[target % PERIOD], actual_rows[target])
        for target in SELECTED_TARGETS
    ]
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "coefficient decomposition and theorem-obligation artifact only; "
            "it proves no orthogonal residual bound, no signed "
            "pair-correlation theorem, no q286 threshold theorem, and no "
            "Goldbach proof."),
        "definition": (
            "For each target residue a, decompose the centered full-action "
            "coefficient in the uniform-weighted orbit inner product as "
            "gamma_full_centered = alpha_a*gamma_F3 + h_a with "
            "<h_a,gamma_F3>_u=0.  Then "
            "full(N)=uniform_full_a+alpha_a*F3(N)+<nu_N,h_a>."),
        "mechanism": (
            "The aligned component explains why first-three pressure opens the "
            "hole.  The remaining theorem must lower-bound the orthogonal "
            "residual so it cannot erase the aligned-only positive margin."),
        "prediction": (
            "If the post-boundary prime-pair discrepancy has "
            "<nu_N,h_a> > -uniform_full_a-alpha_a*F3(N), then the q286 full "
            "action is positive even when F3(N)<=-0.3."),
        "falsifier": (
            "A future proposed residual cone is falsified if an LP finds a "
            "reflected nonnegative synthetic measure with aligned-only margin "
            "positive but orthogonal residual below the required lower bound."),
        "residue_operator_rows": list(operators.values()),
        "target_rows": target_rows,
        "summary": {
            "selected_target_count": len(target_rows),
            "selected_residue_count": len(operators),
            "projection_alpha_summary": finite_summary(
                row["projection_alpha"] for row in operators.values()),
            "uniform_full_summary": finite_summary(
                row["uniform_full_action_to_principal"]
                for row in operators.values()),
            "orthogonality_error_summary": finite_summary(
                row["orthogonality_error"] for row in operators.values()),
            "aligned_full_zero_first_three_floor_summary": finite_summary(
                row["aligned_full_zero_first_three_floor"]
                for row in operators.values()
                if row["aligned_full_zero_first_three_floor"] is not None),
            "orthogonal_residual_action_summary": finite_summary(
                row["orthogonal_residual_action_to_principal"]
                for row in target_rows),
            "aligned_only_positive_target_count": sum(
                1 for row in target_rows if row["aligned_only_positive"]),
            "actual_full_positive_target_count": sum(
                1 for row in target_rows if row["actual_full_positive"]),
            "orthogonal_residual_erases_aligned_margin_targets": [
                row["target"] for row in target_rows
                if row["orthogonal_residual_erases_aligned_margin"]
            ],
            "actual_bad_branch_targets": [
                row["target"] for row in target_rows
                if row["actual_bad_branch"]
            ],
        },
        "decision": (
            "The next theorem is not a global uniformity theorem.  It is a "
            "one-residual signed moment lower bound: after finite boundary "
            "exceptions, show the orthogonal residual action cannot be "
            "negative enough to erase the aligned-only margin."),
        "next_obligation": (
            "Test a predeclared residual cone or source a large-sieve/explicit "
            "formula estimate for <nu_N,h_a>.  Preserve unchanged generic "
            "variance and L1 cones as demoted unless they control this "
            "specific residual functional."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
