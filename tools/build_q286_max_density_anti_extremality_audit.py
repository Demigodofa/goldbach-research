"""Audit a q286 maximum-density anti-extremality cone.

The convex-envelope audit showed that support/reflection/coefficient geometry
admits synthetic bad measures.  This receipt asks how concentrated such a bad
measure must be.  For each tested residue, solve

    minimize lambda
    subject to mu in the support/reflection simplex,
               F3(mu) <= -0.3,
               Full(mu) <= 0,
               mu(orbit) <= lambda * uniform(orbit).

If an actual row has max_orbit_density_multiple below this lambda, then a
maximum-density theorem would exclude the bad branch for that row.  If actual
rows exceed the threshold, this cone is too crude and the theorem must use
coefficient-sensitive or multi-orbit landing structure.

Finite diagnostic only.  It proves no maximum-density theorem, no signed
prime-correlation estimate, no q286 threshold theorem, and no Goldbach proof.
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
OUT = EVIDENCE / "q286-max-density-anti-extremality-audit.json"
CONVEX_SOURCE = EVIDENCE / "q286-convex-envelope-obstruction-audit.json"
TAIL_THRESHOLD = 0.3
PERIOD = 10010
MODULUS = 286
TOLERANCE = 1e-8

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    orbit_coefficients,
    period_full_unit_coefficients,
    prepare_support_context,
    q286_first_three_unit_coefficients,
)
from tools.build_q286_convex_envelope_obstruction_audit import (  # noqa: E402
    actual_source_rows,
    finite_summary,
    json_ready,
    load_json,
)
from tools.build_q286_prime_indexed_kernel_route_audit import (  # noqa: E402
    logs,
    prime_indexed_residue_weights,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def coefficient_row(target_residue, context, full_coefficients,
                    first_three_coefficients):
    orbit_data = orbit_coefficients(
        target_residue, context, full_coefficients, first_three_coefficients)
    return {
        "target_residue": int(target_residue),
        "target_mod_286": int(target_residue % MODULUS),
        "orbits": orbit_data["orbits"],
        "uniform": np.asarray(
            orbit_data["uniform_orbit_mass"], dtype=np.float64),
        "first_three": np.asarray(
            orbit_data["first_three_coefficients"], dtype=np.float64),
        "full": np.asarray(
            orbit_data["full_coefficients"], dtype=np.float64),
    }


def solve_minimum_bad_density(coefficients):
    first_three = coefficients["first_three"]
    full = coefficients["full"]
    uniform = coefficients["uniform"]
    count = len(uniform)
    objective = np.zeros(count + 1, dtype=np.float64)
    objective[-1] = 1.0

    a_ub = [
        np.r_[first_three, 0.0],
        np.r_[full, 0.0],
    ]
    b_ub = [-TAIL_THRESHOLD, 0.0]
    for index, uniform_mass in enumerate(uniform):
        row = np.zeros(count + 1, dtype=np.float64)
        row[index] = 1.0
        row[-1] = -float(uniform_mass)
        a_ub.append(row)
        b_ub.append(0.0)

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
    }
    if not result.success:
        return row
    masses = result.x[:count]
    density_multiples = np.divide(
        masses, uniform, out=np.zeros_like(masses), where=uniform > 0)
    active = np.flatnonzero(masses > TOLERANCE)
    row.update({
        "minimum_bad_max_density_multiple": float(result.x[-1]),
        "bad_first_three": float(np.dot(first_three, masses)),
        "bad_full": float(np.dot(full, masses)),
        "bad_support_size": int(len(active)),
        "bad_entropy": entropy(masses),
        "bad_effective_support": effective_support(masses),
        "largest_bad_density_orbits": tuple(
            {
                "orbit": coefficients["orbits"][index],
                "mass": float(masses[index]),
                "uniform_mass": float(uniform[index]),
                "density_multiple": float(density_multiples[index]),
                "first_three_coefficient": float(first_three[index]),
                "full_coefficient": float(full[index]),
            }
            for index in np.argsort(-density_multiples)[:12]
            if masses[index] > TOLERANCE),
    })
    return row


def entropy(masses):
    positive = np.asarray(
        [float(value) for value in masses if value > 0.0],
        dtype=np.float64)
    if len(positive) == 0:
        return 0.0
    return float(-np.dot(positive, np.log(positive)))


def effective_support(masses):
    square_sum = float(np.dot(masses, masses))
    if square_sum <= 0.0:
        return 0.0
    return 1.0 / square_sum


def actual_row(row, coefficients, primes, prime_values, log_values):
    target = int(row["target"])
    count, total, weights = prime_indexed_residue_weights(
        target, primes, prime_values, log_values, PERIOD)
    if total <= TOLERANCE:
        return {
            "target": target,
            "pair_count": int(count),
            "total_weight": float(total),
            "actual_measure_available": False,
        }
    residue_measure = np.asarray(weights, dtype=np.float64) / float(total)
    orbit_masses = np.asarray([
        math.fsum(float(residue_measure[unit]) for unit in orbit)
        for orbit in coefficients["orbits"]
    ], dtype=np.float64)
    uniform = coefficients["uniform"]
    density_multiples = np.divide(
        orbit_masses, uniform, out=np.zeros_like(orbit_masses),
        where=uniform > 0)
    first_three = float(np.dot(coefficients["first_three"], orbit_masses))
    full = float(np.dot(coefficients["full"], orbit_masses))
    return {
        "target": target,
        "target_residue": int(target % PERIOD),
        "target_mod_286": int(row["target_mod_286"]),
        "block_index_after_discovery": int(row["block_index_after_discovery"]),
        "pair_count": int(count),
        "total_weight": float(total),
        "actual_measure_available": True,
        "actual_first_three": first_three,
        "actual_full": full,
        "actual_full_positive": bool(full > TOLERANCE),
        "actual_max_orbit_density_multiple": float(np.max(density_multiples)),
        "actual_entropy": entropy(orbit_masses),
        "actual_effective_support": effective_support(orbit_masses),
        "largest_actual_density_orbits": tuple(
            {
                "orbit": coefficients["orbits"][index],
                "mass": float(orbit_masses[index]),
                "uniform_mass": float(uniform[index]),
                "density_multiple": float(density_multiples[index]),
                "first_three_coefficient": float(
                    coefficients["first_three"][index]),
                "full_coefficient": float(coefficients["full"][index]),
            }
            for index in np.argsort(-density_multiples)[:12]
            if orbit_masses[index] > TOLERANCE),
    }


def build_receipt():
    convex = load_json(CONVEX_SOURCE)
    rows = actual_source_rows(load_json(
        EVIDENCE / "q286-nonprincipal-drag-envelope-audit.json"))
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    residues = tuple(dict.fromkeys(int(row["target"]) % PERIOD for row in rows))
    coefficient_by_residue = {
        residue: coefficient_row(
            residue, context, full_coefficients, first_three_coefficients)
        for residue in residues
    }
    residue_rows = tuple({
        "target_residue": int(residue),
        "target_mod_286": int(residue % MODULUS),
        "reflection_orbit_count": len(
            coefficient_by_residue[residue]["orbits"]),
        **solve_minimum_bad_density(coefficient_by_residue[residue]),
    } for residue in residues)
    threshold_by_residue = {
        row["target_residue"]: row.get("minimum_bad_max_density_multiple")
        for row in residue_rows
    }
    maximum_target = max(int(row["target"]) for row in rows)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    target_rows = []
    for row in rows:
        target_row = actual_row(
            row, coefficient_by_residue[int(row["target"]) % PERIOD],
            primes, prime_values, log_values)
        threshold = threshold_by_residue[target_row["target_residue"]]
        target_row["minimum_bad_max_density_multiple"] = threshold
        target_row["passes_max_density_certificate"] = (
            threshold is not None
            and target_row["actual_measure_available"]
            and target_row["actual_max_orbit_density_multiple"]
            < threshold - TOLERANCE)
        if threshold is not None and target_row["actual_measure_available"]:
            target_row["actual_to_minimum_bad_density_ratio"] = (
                target_row["actual_max_orbit_density_multiple"] / threshold)
        target_rows.append(target_row)

    post_rows = tuple(
        row for row in target_rows if row["block_index_after_discovery"] >= 1)
    discovery_rows = tuple(
        row for row in target_rows if row["block_index_after_discovery"] == 0)
    certified = tuple(
        row for row in target_rows if row["passes_max_density_certificate"])
    post_certified = tuple(
        row for row in post_rows if row["passes_max_density_certificate"])
    residue_thresholds = tuple(
        row["minimum_bad_max_density_multiple"] for row in residue_rows
        if row.get("minimum_bad_max_density_multiple") is not None)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "convex_envelope_obstruction": str(
                CONVEX_SOURCE.relative_to(ROOT)),
            "nonprincipal_drag_envelope":
                "evidence/q286-nonprincipal-drag-envelope-audit.json",
        },
        "status_boundary": (
            "finite maximum-density anti-extremality diagnostic only; it "
            "proves no maximum-density theorem, signed prime-correlation "
            "estimate, q286 threshold theorem, strict-central Goldbach "
            "theorem, or Goldbach theorem."),
        "candidate_cone": {
            "name": "q286 maximum-density anti-extremality cone",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Synthetic lower-envelope failures are sparse/concentrated. "
                "Constrain every reflection orbit by a density multiple "
                "mu(orbit) <= lambda*u_a(orbit)."),
            "prediction": (
                "If actual prime-pair measures have max orbit density below "
                "the minimum bad density threshold, the bad branch is "
                "excluded without requiring global L1 closeness."),
            "falsifier": (
                "If actual positive rows exceed the minimum bad density "
                "threshold, max-density alone is too crude as a proof cone."),
            "smallest_test": (
                "Use the same pre-existing tight rows as the convex-envelope "
                "audit; solve one LP per target residue for the minimum bad "
                "max-density multiple and compare actual rows to it."),
        },
        "bad_branch": {
            "first_three_at_most": -TAIL_THRESHOLD,
            "full_at_most": 0.0,
        },
        "residue_rows": residue_rows,
        "target_rows": tuple(target_rows),
        "prior_convex_summary": convex["summary"],
        "summary": {
            "target_row_count": len(target_rows),
            "residue_count": len(residue_rows),
            "lp_success_count": sum(row["lp_success"] for row in residue_rows),
            "minimum_bad_max_density_multiple_summary": finite_summary(
                residue_thresholds),
            "bad_support_size_summary": finite_summary(
                row.get("bad_support_size") for row in residue_rows
                if row.get("bad_support_size") is not None),
            "bad_effective_support_summary": finite_summary(
                row.get("bad_effective_support") for row in residue_rows
                if row.get("bad_effective_support") is not None),
            "actual_max_orbit_density_multiple_summary": finite_summary(
                row.get("actual_max_orbit_density_multiple")
                for row in target_rows),
            "actual_effective_support_summary": finite_summary(
                row.get("actual_effective_support") for row in target_rows),
            "actual_certificate_pass_count": len(certified),
            "post_discovery_target_count": len(post_rows),
            "post_discovery_certificate_pass_count": len(post_certified),
            "discovery_target_count": len(discovery_rows),
            "actual_to_minimum_bad_density_ratio_summary": finite_summary(
                row.get("actual_to_minimum_bad_density_ratio")
                for row in target_rows),
            "post_discovery_actual_to_minimum_bad_density_ratio_summary":
                finite_summary(
                    row.get("actual_to_minimum_bad_density_ratio")
                    for row in post_rows),
            "worst_actual_to_threshold_rows": tuple(sorted(
                (
                    row for row in target_rows
                    if "actual_to_minimum_bad_density_ratio" in row),
                key=lambda item: (
                    -item["actual_to_minimum_bad_density_ratio"],
                    item["target"]))[:20]),
            "tightest_certificate_rows": tuple(sorted(
                (
                    row for row in target_rows
                    if "actual_to_minimum_bad_density_ratio" in row),
                key=lambda item: (
                    item["minimum_bad_max_density_multiple"]
                    - item["actual_max_orbit_density_multiple"],
                    item["target"]))[:20]),
        },
        "decision": (
            "If actual rows pass this cone, max-density is a plausible "
            "anti-extremality theorem target.  If many actual rows fail it, "
            "the next cone must use multi-orbit or coefficient-sensitive "
            "landing, not only a maximum atom bound."),
        "next_obligation": (
            "Compare this max-density threshold with available fixed-modulus "
            "upper bounds for binary prime pairs in residue orbits.  If those "
            "bounds cannot reach the measured threshold, try a top-k/entropy "
            "or signed-moment cone."),
        "maximum_density_theorem_proved": False,
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
        "actual_certificate_pass_count": (
            payload["summary"]["actual_certificate_pass_count"]),
        "post_discovery_certificate_pass_count": (
            payload["summary"]["post_discovery_certificate_pass_count"]),
        "goldbach_proved": payload["goldbach_proved"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
