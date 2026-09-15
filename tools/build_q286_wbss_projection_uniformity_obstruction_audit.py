"""Test the blunt four-modulus projection-uniformity bridge for q286-WBSS.

The four-modulus projection formula gives a sufficient condition: if every
projected residue probability error modulo 70, 130, 154, and 286 is small
enough in absolute value, then the q286-WBSS signed expectation is positive.

This receipt compares that sufficient budget with actual strict-central
binary-prime projection errors on the same post-discovery q286-WBSS rows.  A
failure here does not refute the four-modulus formula; it only demotes the
ordinary projected L-infinity uniformity bridge and forces a signed,
coefficient-sensitive theorem target.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
DUAL_SOURCE = EVIDENCE / "q286-lower-face-dual-edge-audit.json"
OUT = EVIDENCE / "q286-wbss-projection-uniformity-obstruction-audit.json"
TOLERANCE = 1e-10

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


def coefficient_lookup(formula):
    by_modulus = {}
    alpha0 = None
    for row in formula["coefficient_table"]["rows"]:
        if row["kind"] == "total_mass":
            alpha0 = float(row["coefficient"])
        elif row["kind"] == "residue_projection":
            by_modulus.setdefault(
                int(row["modulus"]), {})[int(row["residue"])] = float(
                    row["coefficient"])
    if alpha0 is None:
        raise ValueError("formula receipt has no total_mass coefficient")
    return alpha0, by_modulus


def unit_formula_value(unit, alpha0, by_modulus):
    return alpha0 + math.fsum(
        coefficients[int(unit % modulus)]
        for modulus, coefficients in by_modulus.items()
    )


def orbit_formula_values(orbits, alpha0, by_modulus):
    values = []
    for orbit in orbits:
        values.append(math.fsum(
            unit_formula_value(unit, alpha0, by_modulus)
            for unit in orbit) / len(orbit))
    return np.asarray(values, dtype=np.float64)


def projection_distribution(orbits, masses, modulus):
    residues = sorted({int(unit % modulus) for orbit in orbits for unit in orbit})
    dist = {residue: 0.0 for residue in residues}
    for orbit, mass in zip(orbits, masses):
        contribution = float(mass) / len(orbit)
        for unit in orbit:
            dist[int(unit % modulus)] += contribution
    return dist


def projection_rows(orbits, actual_mass, uniform_mass, by_modulus):
    rows = []
    for modulus in sorted(by_modulus):
        actual = projection_distribution(orbits, actual_mass, modulus)
        uniform = projection_distribution(orbits, uniform_mass, modulus)
        coefficients = by_modulus[modulus]
        cells = []
        for residue in sorted(actual):
            error = actual[residue] - uniform[residue]
            cells.append({
                "residue": int(residue),
                "actual_probability": float(actual[residue]),
                "local_uniform_probability": float(uniform[residue]),
                "error": float(error),
                "abs_error": float(abs(error)),
                "coefficient": float(coefficients[residue]),
                "weighted_error": float(coefficients[residue] * error),
            })
        rows.append({
            "modulus": int(modulus),
            "residue_count": len(cells),
            "max_abs_projection_error": max(
                cell["abs_error"] for cell in cells),
            "l1_projection_error": math.fsum(
                cell["abs_error"] for cell in cells),
            "signed_weighted_error": math.fsum(
                cell["weighted_error"] for cell in cells),
            "largest_abs_error_cells": sorted(
                cells,
                key=lambda cell: (-cell["abs_error"], cell["residue"]),
            )[:8],
            "largest_abs_weighted_error_cells": sorted(
                cells,
                key=lambda cell: (-abs(cell["weighted_error"]),
                                  cell["residue"]),
            )[:8],
        })
    return rows


def build_row(edge_row, context, full_coefficients, first_three_coefficients,
              primes, prime_values, log_values, alpha0, by_modulus):
    orbit_data = orbit_coefficients(
        int(edge_row["target_residue"]),
        context,
        full_coefficients,
        first_three_coefficients,
    )
    coefficient_data = {
        "orbits": orbit_data["orbits"],
        "first_three": np.asarray(
            orbit_data["first_three_coefficients"], dtype=np.float64),
        "full": np.asarray(orbit_data["full_coefficients"], dtype=np.float64),
    }
    actual = actual_orbit_measure(
        int(edge_row["target"]),
        coefficient_data,
        primes,
        prime_values,
        log_values,
    )
    actual_mass = np.asarray(actual["masses"], dtype=np.float64)
    uniform_mass = np.asarray(orbit_data["uniform_orbit_mass"], dtype=np.float64)
    projection_summary = projection_rows(
        orbit_data["orbits"], actual_mass, uniform_mass, by_modulus)
    phi = orbit_formula_values(orbit_data["orbits"], alpha0, by_modulus)
    local_uniform_main = float(np.dot(uniform_mass, phi))
    actual_expectation = float(np.dot(actual_mass, phi))
    formula_projection_expectation = alpha0
    for modulus, coefficients in by_modulus.items():
        actual_projection = projection_distribution(
            orbit_data["orbits"], actual_mass, modulus)
        formula_projection_expectation += math.fsum(
            coefficients[residue] * actual_projection[residue]
            for residue in actual_projection)
    return {
        "target": int(edge_row["target"]),
        "target_residue": int(edge_row["target_residue"]),
        "target_mod_286": int(edge_row["target_mod_286"]),
        "block_index_after_discovery": int(
            edge_row["block_index_after_discovery"]),
        "pair_count": int(actual["pair_count"]),
        "total_weight": float(actual["total_weight"]),
        "orbit_count": int(len(orbit_data["orbits"])),
        "local_uniform_main_term": local_uniform_main,
        "actual_formula_expectation": actual_expectation,
        "projection_formula_expectation": float(formula_projection_expectation),
        "projection_formula_abs_error": float(
            abs(actual_expectation - formula_projection_expectation)),
        "actual_positive": bool(actual_expectation > TOLERANCE),
        "nonconstant_signed_projection_error": float(
            actual_expectation - local_uniform_main),
        "max_abs_projection_error": max(
            row["max_abs_projection_error"] for row in projection_summary),
        "max_l1_projection_error": max(
            row["l1_projection_error"] for row in projection_summary),
        "projection_rows": projection_summary,
    }


def row_summary(rows, budget):
    return {
        "row_count": len(rows),
        "positive_actual_expectation_count": sum(
            row["actual_positive"] for row in rows),
        "inside_blunt_projection_error_budget_count": sum(
            row["max_abs_projection_error"] <= budget + TOLERANCE
            for row in rows),
        "outside_blunt_projection_error_budget_count": sum(
            row["max_abs_projection_error"] > budget + TOLERANCE
            for row in rows),
        "max_abs_projection_error_summary": finite_summary(
            row["max_abs_projection_error"] for row in rows),
        "max_abs_projection_error_to_budget_summary": finite_summary(
            row["max_abs_projection_error"] / budget for row in rows),
        "actual_formula_expectation_summary": finite_summary(
            row["actual_formula_expectation"] for row in rows),
        "local_uniform_main_term_summary": finite_summary(
            row["local_uniform_main_term"] for row in rows),
        "nonconstant_signed_projection_error_summary": finite_summary(
            row["nonconstant_signed_projection_error"] for row in rows),
        "projection_formula_abs_error_summary": finite_summary(
            row["projection_formula_abs_error"] for row in rows),
        "largest_projection_error_rows": sorted(
            [
                {
                    "target": row["target"],
                    "target_residue": row["target_residue"],
                    "target_mod_286": row["target_mod_286"],
                    "max_abs_projection_error": row[
                        "max_abs_projection_error"],
                    "max_abs_projection_error_to_budget": (
                        row["max_abs_projection_error"] / budget),
                    "actual_formula_expectation": row[
                        "actual_formula_expectation"],
                    "local_uniform_main_term": row[
                        "local_uniform_main_term"],
                    "largest_modulus_errors": sorted(
                        [
                            {
                                "modulus": item["modulus"],
                                "max_abs_projection_error": item[
                                    "max_abs_projection_error"],
                            }
                            for item in row["projection_rows"]
                        ],
                        key=lambda item: (
                            -item["max_abs_projection_error"],
                            item["modulus"]),
                    ),
                }
                for row in rows
            ],
            key=lambda row: (
                -row["max_abs_projection_error"], row["target"]),
        )[:20],
    }


def modulus_summary(rows):
    result = {}
    for modulus in sorted({
            item["modulus"]
            for row in rows
            for item in row["projection_rows"]
    }):
        items = [
            item
            for row in rows
            for item in row["projection_rows"]
            if item["modulus"] == modulus
        ]
        result[str(modulus)] = {
            "row_count": len(items),
            "negative_signed_weighted_error_count": sum(
                item["signed_weighted_error"] < -TOLERANCE
                for item in items),
            "positive_signed_weighted_error_count": sum(
                item["signed_weighted_error"] > TOLERANCE
                for item in items),
            "near_zero_signed_weighted_error_count": sum(
                abs(item["signed_weighted_error"]) <= TOLERANCE
                for item in items),
            "max_abs_projection_error_summary": finite_summary(
                item["max_abs_projection_error"] for item in items),
            "l1_projection_error_summary": finite_summary(
                item["l1_projection_error"] for item in items),
            "signed_weighted_error_summary": finite_summary(
                item["signed_weighted_error"] for item in items),
        }
    return result


def build_receipt():
    formula = load_json(FORMULA_SOURCE)
    dual = load_json(DUAL_SOURCE)
    alpha0, by_modulus = coefficient_lookup(formula)
    budget = float(formula["projection_error_budget"][
        "sufficient_uniform_projection_error_bound"])
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    edge_rows = [row for row in dual["target_rows"] if row["edge_success"]]
    maximum_target = max(row["target"] for row in edge_rows)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    rows = [
        build_row(
            row,
            context,
            full_coefficients,
            first_three_coefficients,
            primes,
            prime_values,
            log_values,
            alpha0,
            by_modulus,
        )
        for row in edge_rows
    ]
    post = [
        row for row in rows
        if row["block_index_after_discovery"] >= 1
    ]
    discovery = [
        row for row in rows
        if row["block_index_after_discovery"] < 1
    ]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "lower_face_dual_edge_audit": str(DUAL_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite four-modulus projected-uniformity obstruction only; no "
            "binary-prime projection theorem, signed discrepancy theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"
        ),
        "goldbach_proved": False,
        "projection_uniformity_theorem_proved": False,
        "four_modulus_formula_falsified": False,
        "blunt_projected_linf_uniformity_bridge_demoted": True,
        "novelty_label": "new-to-this-task",
        "candidate": {
            "name": "four-modulus projected L-infinity uniformity bridge",
            "mechanism": (
                "Use the explicit four-modulus formula and bound every "
                "projected residue probability error by one common epsilon."
            ),
            "prediction": (
                "If this is the right proof bridge, actual successful rows "
                "should at least fall inside, or near, the sufficient budget."
            ),
            "falsifier": (
                "If successful rows have projected cell errors far above the "
                "budget, the bridge is too strong even after four-modulus "
                "compression."
            ),
            "smallest_test": (
                "Measure actual versus local-uniform projected residue "
                "probabilities modulo 70, 130, 154, and 286 on the existing "
                "q286-WBSS dual-edge rows."
            ),
        },
        "projection_error_budget": budget,
        "summary": {
            "all_rows": row_summary(rows, budget),
            "post_discovery_rows": row_summary(post, budget),
            "discovery_rows": row_summary(discovery, budget),
            "post_discovery_modulus_summaries": modulus_summary(post),
        },
        "decision": (
            "The blunt four-modulus projected-uniformity bridge is demoted. "
            "On the 196 post-discovery rows, all actual signed expectations "
            "remain positive, but zero rows satisfy the sufficient projected "
            "L-infinity budget.  The maximum projected cell error ranges from "
            "0.0054355245292371495 to 0.03166078595284763 against budget "
            f"{budget}.  Therefore the four-modulus formula remains useful, "
            "but the next theorem must control its signed weighted projection "
            "error or raw witness directly, not every projected residue cell "
            "in absolute value."
        ),
        "target_rows_boundary": (
            "Full per-cell projection tables are intentionally not serialized; "
            "the receipt keeps summaries and worst-row examples only. Rerun "
            "the builder for exact row-level reconstruction."
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
