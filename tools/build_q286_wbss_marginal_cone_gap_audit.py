"""Test lower-modulus marginal cones against the q286-WBSS signed problem.

The signed-discrepancy problem isolates the scalar threshold

    <mu_N, phi_a> > 0.

This receipt asks whether lower-dimensional AP-style marginal information can
force that scalar.  For stress-selected post-discovery rows, it fixes the
actual reflected orbit measure's projections to several predeclared modulus
families, then solves an LP minimizing the signed q286 expectation over all
nonnegative reflected measures with those same projections.

If the LP minimum is nonpositive, that marginal cone is insufficient: even
exact knowledge of those projections permits a synthetic bad arrangement.  If
the LP minimum is positive, that cone would imply the signed threshold for the
tested row, but only after a separate source-backed theorem supplies those
projection constraints for actual primes.

Finite cone falsifier only.  It proves no AP theorem, signed discrepancy
theorem, q286 threshold theorem, strict-central Goldbach theorem, or Goldbach
theorem.
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
SIGNED_SOURCE = EVIDENCE / "q286-wbss-signed-discrepancy-problem.json"
DUAL_SOURCE = EVIDENCE / "q286-lower-face-dual-edge-audit.json"
OUT = EVIDENCE / "q286-wbss-marginal-cone-gap-audit.json"
PERIOD = 10010
TOLERANCE = 1e-9
STRESS_ROW_COUNT_PER_FAMILY = 12

MARGINAL_CONES = {
    "support_reflection_only": (),
    "prime_factor_marginals": (5, 7, 11, 13),
    "q286_joint_marginal": (286,),
    "dominant_coefficient_support_marginals": (70, 154, 286),
    "all_coefficient_support_marginals": (
        10, 14, 22, 26, 70, 130, 154, 286),
}

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
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def selected_targets():
    source = load_json(SIGNED_SOURCE)
    picks = set()
    for family in ("full", "edge_beta"):
        rows = source["families"][family]["rows"]
        by_lambda = sorted(
            rows, key=lambda row: (-row["lambda_phi"], row["target"]))
        by_l1 = sorted(
            rows, key=lambda row: (-row["l1_worst_case_load"], row["target"]))
        picks.update(row["target"] for row in by_lambda[
            :STRESS_ROW_COUNT_PER_FAMILY])
        picks.update(row["target"] for row in by_l1[
            :STRESS_ROW_COUNT_PER_FAMILY // 2])
    return tuple(sorted(picks))


def projection_matrix(orbits, modulus):
    residues = sorted({
        int(unit % modulus)
        for orbit in orbits
        for unit in orbit
    })
    matrix = np.zeros((len(residues), len(orbits)), dtype=np.float64)
    for column, orbit in enumerate(orbits):
        scale = 1.0 / len(orbit)
        for unit in orbit:
            matrix[residues.index(int(unit % modulus)), column] += scale
    return residues, matrix


def equality_system(orbits, actual_mass, moduli):
    rows = [np.ones(len(orbits), dtype=np.float64)]
    rhs = [1.0]
    projection_summaries = {}
    for modulus in moduli:
        residues, matrix = projection_matrix(orbits, modulus)
        actual_projection = matrix @ actual_mass
        # Drop one residue per modulus; the total-mass row supplies the sum and
        # avoiding the redundant equality helps HiGHS' presolver.
        for row, value in zip(matrix[:-1], actual_projection[:-1]):
            rows.append(row)
            rhs.append(float(value))
        projection_summaries[str(modulus)] = {
            "residue_count": len(residues),
            "maximum_projection_mass": float(np.max(actual_projection)),
            "minimum_projection_mass": float(np.min(actual_projection)),
        }
    return np.asarray(rows, dtype=np.float64), np.asarray(rhs), projection_summaries


def solve_minimum_expectation(orbits, actual_mass, phi, moduli):
    a_eq, b_eq, projection_summaries = equality_system(
        orbits, actual_mass, moduli)
    result = linprog(
        np.asarray(phi, dtype=np.float64),
        A_eq=a_eq,
        b_eq=b_eq,
        bounds=[(0.0, None)] * len(orbits),
        method="highs",
    )
    row = {
        "lp_success": bool(result.success),
        "lp_status": int(result.status),
        "lp_message": result.message,
        "equality_count": int(a_eq.shape[0]),
        "projection_summaries": projection_summaries,
    }
    if not result.success:
        return row
    synthetic = np.asarray(result.x, dtype=np.float64)
    deviations = synthetic - actual_mass
    row.update({
        "minimum_signed_expectation": float(result.fun),
        "bad_measure_feasible": bool(result.fun <= TOLERANCE),
        "actual_signed_expectation": float(np.dot(actual_mass, phi)),
        "synthetic_l1_from_actual": float(np.sum(np.abs(deviations))),
        "synthetic_effective_support": float(
            1.0 / np.sum(synthetic * synthetic)
            if np.sum(synthetic * synthetic) > TOLERANCE else 0.0),
        "largest_synthetic_moves": [
            {
                "orbit": list(orbits[index]),
                "synthetic_mass": float(synthetic[index]),
                "actual_mass": float(actual_mass[index]),
                "move": float(deviations[index]),
                "coefficient": float(phi[index]),
            }
            for index in np.argsort(-np.abs(deviations))[:10]
            if abs(deviations[index]) > TOLERANCE
        ],
    })
    return row


def build_row(edge_row, context, full_coefficients, first_three_coefficients,
              primes, prime_values, log_values):
    orbit_data = orbit_coefficients(
        int(edge_row["target_residue"]),
        context,
        full_coefficients,
        first_three_coefficients,
    )
    coefficients = {
        "orbits": orbit_data["orbits"],
        "first_three": np.asarray(
            orbit_data["first_three_coefficients"], dtype=np.float64),
        "full": np.asarray(
            orbit_data["full_coefficients"], dtype=np.float64),
    }
    actual = actual_orbit_measure(
        int(edge_row["target"]),
        coefficients,
        primes,
        prime_values,
        log_values,
    )
    actual_mass = np.asarray(actual["masses"], dtype=np.float64)
    slope = float(edge_row["slope"])
    intercept = float(edge_row["intercept"])
    required = float(edge_row["required_edge_gap_for_positivity"])
    gap = coefficients["full"] - (slope * coefficients["first_three"]
                                  + intercept)
    families = {
        "full": coefficients["full"],
        "edge_beta": gap - required,
    }
    family_rows = {}
    for family, phi in families.items():
        cone_rows = {}
        for cone, moduli in MARGINAL_CONES.items():
            cone_rows[cone] = solve_minimum_expectation(
                orbit_data["orbits"], actual_mass, phi, moduli)
        family_rows[family] = {
            "actual_signed_expectation": float(np.dot(actual_mass, phi)),
            "cone_rows": cone_rows,
        }
    return {
        "target": int(edge_row["target"]),
        "target_residue": int(edge_row["target_residue"]),
        "target_mod_286": int(edge_row["target_mod_286"]),
        "block_index_after_discovery": int(
            edge_row["block_index_after_discovery"]),
        "pair_count": int(actual["pair_count"]),
        "total_weight": float(actual["total_weight"]),
        "orbit_count": int(len(orbit_data["orbits"])),
        "families": family_rows,
    }


def summarize(rows, family, cone):
    cone_rows = [row["families"][family]["cone_rows"][cone] for row in rows]
    feasible = [row for row in cone_rows if row["lp_success"]]
    bad = [row for row in feasible if row["bad_measure_feasible"]]
    positive = [row for row in feasible if not row["bad_measure_feasible"]]
    return {
        "row_count": len(rows),
        "lp_success_count": len(feasible),
        "bad_measure_feasible_count": len(bad),
        "positive_forced_count": len(positive),
        "minimum_signed_expectation_summary": finite_summary(
            row["minimum_signed_expectation"] for row in feasible),
        "synthetic_l1_from_actual_summary": finite_summary(
            row["synthetic_l1_from_actual"] for row in feasible),
    }


def first_examples(rows, family, cone, bad_flag):
    examples = []
    for row in rows:
        cone_row = row["families"][family]["cone_rows"][cone]
        if (cone_row["lp_success"]
                and cone_row["bad_measure_feasible"] == bad_flag):
            examples.append({
                "target": row["target"],
                "target_residue": row["target_residue"],
                "target_mod_286": row["target_mod_286"],
                "actual_signed_expectation": row["families"][family][
                    "actual_signed_expectation"],
                "minimum_signed_expectation": cone_row[
                    "minimum_signed_expectation"],
                "synthetic_l1_from_actual": cone_row[
                    "synthetic_l1_from_actual"],
            })
    return examples[:8]


def build_receipt():
    dual = load_json(DUAL_SOURCE)
    targets = selected_targets()
    dual_by_target = {
        int(row["target"]): row
        for row in dual["target_rows"]
        if row["edge_success"]
    }
    missing = [target for target in targets if target not in dual_by_target]
    if missing:
        raise ValueError(f"selected targets missing from dual audit: {missing}")

    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    maximum_target = max(targets)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)

    rows = [
        build_row(
            dual_by_target[target],
            context,
            full_coefficients,
            first_three_coefficients,
            primes,
            prime_values,
            log_values,
        )
        for target in targets
    ]
    summary = {}
    for family in ("full", "edge_beta"):
        summary[family] = {
            cone: summarize(rows, family, cone)
            for cone in MARGINAL_CONES
        }
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "signed_discrepancy_problem": str(SIGNED_SOURCE.relative_to(ROOT)),
            "lower_face_dual_edge_audit": str(DUAL_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite marginal-cone LP falsifier only; no lower-modulus "
            "projection theorem, AP theorem, signed discrepancy theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"
        ),
        "goldbach_proved": False,
        "marginal_cone_theorem_proved": False,
        "signed_discrepancy_theorem_proved": False,
        "candidate": {
            "name": "lower-modulus marginal cone for q286-WBSS",
            "mechanism": (
                "Replace total-L1 uniformity with exact projections of the "
                "actual reflected prime-pair orbit measure to fixed lower "
                "moduli before testing whether the signed bad state remains "
                "LP-feasible."
            ),
            "prediction": (
                "Prime-factor and q286-only projections should still permit "
                "synthetic bad arrangements; the full coefficient-support "
                "projection family should force positivity because it fixes "
                "all lower-modulus components used by the coefficient."
            ),
            "falsifier": (
                "A nonpositive LP optimum under a cone means that cone cannot "
                "prove the signed threshold, even with exact marginal data."
            ),
            "smallest_test": (
                "Stress-select rows from the prior signed-discrepancy receipt "
                "by highest lambda and largest L1 load, then solve the "
                "minimum-expectation LP under each cone."),
        },
        "marginal_cones": {
            name: list(moduli) for name, moduli in MARGINAL_CONES.items()
        },
        "selected_targets": targets,
        "selected_target_rule": (
            "Union of the top 12 post-discovery rows by lambda and top 6 by "
            "L1 worst-case load for each of full and edge-beta in "
            "q286-wbss-signed-discrepancy-problem.json."),
        "summary": summary,
        "examples": {
            family: {
                cone: {
                    "bad_measure_examples": first_examples(
                        rows, family, cone, True),
                    "positive_forced_examples": first_examples(
                        rows, family, cone, False),
                }
                for cone in MARGINAL_CONES
            }
            for family in ("full", "edge_beta")
        },
        "target_rows": rows,
        "decision": (
            "Exact lower-modulus marginals sharpen the theorem boundary.  "
            "Any cone with a nonpositive LP minimum is too weak as a proof "
            "bridge; a positive-forcing cone is only useful if a separate "
            "source-backed binary-prime projection theorem can put actual "
            "mu_N in that cone.  This separates AP-style projection data from "
            "the still-missing signed binary-prime correlation estimate."
        ),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
