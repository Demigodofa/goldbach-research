"""Test the q286 orthogonal residual Cauchy/chi-square certificate.

The orthogonal-rescue decomposition reduced q286 closure to one residual
functional:

    full = aligned_only + <nu_N,h_a>.

A natural next cone is a coefficient-sensitive chi-square ball around the
local uniform measure.  By Cauchy-Schwarz in the uniform-weighted orbit inner
product,

    |<nu,h_a>| <= ||nu||_{u^-1} ||h_a||_u.

Therefore aligned_only > 0 and

    ||nu||_{u^-1} < aligned_only / ||h_a||_u

is a sufficient certificate for full > 0.  This receipt checks whether the
actual selected rows satisfy that certificate.  It is a theorem-shaping norm
diagnostic only, not an analytic estimate for actual prime pairs.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-orthogonal-residual-norm-certificate.json"
L1_SOURCE = ROOT / "evidence" / "q286-cone-duality-l1-uniformity-candidate.json"
ORTHOGONAL_SOURCE = ROOT / "evidence" / "q286-orthogonal-rescue-decomposition.json"
PERIOD = 10010
MODULUS = 286
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    SELECTED_TARGETS,
    combined_fixed_strict_central_coefficient_receipt,
    orbit_coefficients,
    period_full_unit_coefficients,
    prepare_support_context,
    prime_indexed_residue_weights,
    q286_first_three_unit_coefficients,
)
from tools.build_q286_prime_indexed_kernel_route_audit import logs  # noqa: E402


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


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def weighted_inner(weight, left, right):
    return float(np.dot(weight, left * right))


def weighted_norm(weight, vector):
    return math.sqrt(max(0.0, weighted_inner(weight, vector, vector)))


def residual_operator(target_residue, context, full_coefficients,
                      first_three_coefficients):
    orbit_data = orbit_coefficients(
        target_residue, context, full_coefficients, first_three_coefficients)
    uniform = orbit_data["uniform_orbit_mass"]
    first_three = orbit_data["first_three_coefficients"]
    full = orbit_data["full_coefficients"]
    uniform_full = float(np.dot(full, uniform))
    centered_full = full - uniform_full
    denominator = weighted_inner(uniform, first_three, first_three)
    alpha = weighted_inner(uniform, first_three, centered_full) / denominator
    residual = centered_full - alpha * first_three
    return {
        "orbit_data": orbit_data,
        "uniform": uniform,
        "first_three": first_three,
        "full": full,
        "residual": residual,
        "uniform_full": uniform_full,
        "alpha": alpha,
        "residual_norm": weighted_norm(uniform, residual),
        "orthogonality_error": abs(weighted_inner(uniform, residual, first_three)),
    }


def actual_orbit_masses(target, orbit_data, primes, prime_values, log_values):
    count, total, weights = prime_indexed_residue_weights(
        target, primes, prime_values, log_values, PERIOD)
    if total <= TOLERANCE:
        raise AssertionError(f"target {target} has no strict-central mass")
    weight_by_residue = np.asarray(weights, dtype=np.float64) / float(total)
    orbit_masses = np.asarray([
        math.fsum(float(weight_by_residue[unit]) for unit in orbit)
        for orbit in orbit_data["orbits"]
    ], dtype=np.float64)
    return int(count), float(total), orbit_masses


def chi_square_norm(orbit_masses, uniform):
    discrepancy = orbit_masses - uniform
    return math.sqrt(float(np.sum(discrepancy * discrepancy / uniform)))


def target_row(target, operator, actual, primes, prime_values, log_values):
    count, total, orbit_masses = actual_orbit_masses(
        target, operator["orbit_data"], primes, prime_values, log_values)
    uniform = operator["uniform"]
    first_three = float(np.dot(operator["first_three"], orbit_masses))
    full = float(np.dot(operator["full"], orbit_masses))
    aligned_only = operator["uniform_full"] + operator["alpha"] * first_three
    residual_action = float(np.dot(operator["residual"], orbit_masses))
    required_lower = -aligned_only
    chi_norm = chi_square_norm(orbit_masses, uniform)
    residual_norm = operator["residual_norm"]
    required_chi_norm = (
        aligned_only / residual_norm
        if aligned_only > TOLERANCE and residual_norm > TOLERANCE else None)
    cauchy_abs_bound = chi_norm * residual_norm
    return {
        "target": int(target),
        "target_residue": int(target % PERIOD),
        "target_mod_286": int(target % MODULUS),
        "pair_count": count,
        "total_weight": total,
        "actual_first_three_to_principal_ratio": first_three,
        "actual_full_action_to_principal_ratio": full,
        "reference_first_three_to_principal_ratio": float(
            actual["actual_first_three_to_principal_ratio"]),
        "reference_full_action_to_principal_ratio": float(
            actual["actual_full_action_to_principal_ratio"]),
        "first_three_reconstruction_error": abs(
            first_three - float(actual["actual_first_three_to_principal_ratio"])),
        "full_reconstruction_error": abs(
            full - float(actual["actual_full_action_to_principal_ratio"])),
        "aligned_only_full_action_to_principal": aligned_only,
        "orthogonal_residual_action_to_principal": residual_action,
        "required_orthogonal_residual_lower_bound_for_positive_full": required_lower,
        "orthogonal_residual_surplus_to_positive_full": (
            residual_action - required_lower),
        "chi_square_norm_from_uniform": chi_norm,
        "orthogonal_residual_weighted_norm": residual_norm,
        "cauchy_abs_residual_bound": cauchy_abs_bound,
        "required_chi_square_norm_certificate_radius": required_chi_norm,
        "passes_orthogonal_residual_norm_certificate": (
            required_chi_norm is not None
            and chi_norm < required_chi_norm - TOLERANCE),
        "norm_certificate_ratio": (
            chi_norm / required_chi_norm
            if required_chi_norm and required_chi_norm > TOLERANCE else None),
        "actual_full_positive": full > 0.0,
        "actual_bad_branch": bool(actual["actual_bad_branch"]),
    }


def main():
    l1_receipt = load_json(L1_SOURCE)
    orthogonal_receipt = load_json(ORTHOGONAL_SOURCE)
    actual_rows = {int(row["target"]): row for row in l1_receipt["target_rows"]}
    selected_targets = tuple(int(target) for target in SELECTED_TARGETS)
    primes = np.asarray(_prime_table(max(selected_targets)), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(max(selected_targets))
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    residues = tuple(dict.fromkeys(target % PERIOD for target in selected_targets))
    operators = {
        residue: residual_operator(
            residue, context, full_coefficients, first_three_coefficients)
        for residue in residues
    }
    target_rows = [
        target_row(
            target, operators[target % PERIOD], actual_rows[target],
            primes, prime_values, log_values)
        for target in selected_targets
    ]
    certified = [
        row["target"] for row in target_rows
        if row["passes_orthogonal_residual_norm_certificate"]
    ]
    false_negatives = [
        row["target"] for row in target_rows
        if row["actual_full_positive"]
        and not row["passes_orthogonal_residual_norm_certificate"]
    ]
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "coefficient-sensitive norm diagnostic only; it proves no "
            "orthogonal residual bound, no signed pair-correlation theorem, "
            "no q286 threshold theorem, and no Goldbach proof."),
        "source_receipts": {
            "l1_uniformity": str(L1_SOURCE.relative_to(ROOT)),
            "orthogonal_rescue": str(ORTHOGONAL_SOURCE.relative_to(ROOT)),
            "orthogonal_rescue_source_commit": orthogonal_receipt["source_commit"],
        },
        "candidate_cone": (
            "For each target residue, require the chi-square norm "
            "||nu||_{u^-1} to be below aligned_only/||h_a||_u.  Then "
            "Cauchy-Schwarz forces |<nu,h_a>| below the aligned-only margin, "
            "so full action remains positive."),
        "prediction": (
            "If actual post-boundary prime-pair measures satisfy this "
            "coefficient-sensitive chi-square radius, residual overturn is "
            "impossible."),
        "falsifier": (
            "The cone is too blunt as a main proof route if actual full-positive "
            "rows fail the norm certificate by large factors."),
        "target_rows": target_rows,
        "summary": {
            "selected_target_count": len(target_rows),
            "selected_residue_count": len(operators),
            "certified_target_count": len(certified),
            "certified_targets": certified,
            "actual_full_positive_target_count": sum(
                1 for row in target_rows if row["actual_full_positive"]),
            "actual_full_positive_not_norm_certified_targets": false_negatives,
            "actual_bad_branch_targets": [
                row["target"] for row in target_rows if row["actual_bad_branch"]
            ],
            "chi_square_norm_summary": finite_summary(
                row["chi_square_norm_from_uniform"] for row in target_rows),
            "required_chi_square_radius_summary": finite_summary(
                row["required_chi_square_norm_certificate_radius"]
                for row in target_rows
                if row["required_chi_square_norm_certificate_radius"] is not None),
            "norm_certificate_ratio_summary": finite_summary(
                row["norm_certificate_ratio"] for row in target_rows
                if row["norm_certificate_ratio"] is not None),
            "maximum_reconstruction_error": max(
                max(row["first_three_reconstruction_error"],
                    row["full_reconstruction_error"])
                for row in target_rows),
        },
        "decision": (
            "The Cauchy/chi-square residual cone is valid as a sufficient "
            "condition but too strong for the measured rows.  It cannot be the "
            "main proof engine unless an analytic theorem gives a much sharper "
            "coefficient-specific bound than observed global chi-square size. "
            "The surviving route is a signed lower-tail estimate for "
            "<nu_N,h_a>, not a norm bound on all of nu_N."),
        "next_obligation": (
            "Replace norm control with a signed residual lower-tail cone: "
            "decompose h_a into sign/landing classes or source an explicit "
            "formula/large-sieve estimate for this one linear statistic."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
