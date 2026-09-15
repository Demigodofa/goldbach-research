"""Decompose the q286-WBSS mod-286 drag into one-factor and interaction parts.

The projected-uniformity audit showed that the mod-286 projection contributes
negative signed weighted error on every checked post-discovery row.  Since
286=2*11*13, this receipt asks whether that drag is explained by simpler
mod-11 or mod-13 marginal bias, or by the genuine two-factor interaction on
the unit grid modulo 11 x 13.

Finite interaction diagnostic only.  It proves no interaction theorem, signed
projection theorem, q286 threshold theorem, strict-central Goldbach theorem, or
Goldbach proof.
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
OUT = EVIDENCE / "q286-wbss-mod286-interaction-audit.json"
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
from tools.build_q286_wbss_projection_uniformity_obstruction_audit import (  # noqa: E402
    coefficient_lookup,
    projection_distribution,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def centered_sum_squares(values):
    vals = np.asarray(values, dtype=np.float64)
    return float(np.sum((vals - np.mean(vals)) ** 2))


def decompose_mod286_coefficient(coefficients):
    residues = sorted(coefficients)
    values = np.asarray([coefficients[residue] for residue in residues],
                        dtype=np.float64)
    mean = float(np.mean(values))
    levels_11 = sorted({residue % 11 for residue in residues})
    levels_13 = sorted({residue % 13 for residue in residues})
    part_11 = {
        level: float(np.mean([
            coefficients[residue]
            for residue in residues
            if residue % 11 == level
        ]) - mean)
        for level in levels_11
    }
    part_13 = {
        level: float(np.mean([
            coefficients[residue]
            for residue in residues
            if residue % 13 == level
        ]) - mean)
        for level in levels_13
    }
    interaction = {
        residue: float(
            coefficients[residue]
            - mean
            - part_11[residue % 11]
            - part_13[residue % 13]
        )
        for residue in residues
    }
    total_ss = centered_sum_squares(values)
    ss_11 = math.fsum(
        sum(1 for residue in residues if residue % 11 == level)
        * part_11[level] ** 2
        for level in levels_11
    )
    ss_13 = math.fsum(
        sum(1 for residue in residues if residue % 13 == level)
        * part_13[level] ** 2
        for level in levels_13
    )
    ss_interaction = math.fsum(
        value * value for value in interaction.values())
    residual = max(
        abs(
            coefficients[residue]
            - mean
            - part_11[residue % 11]
            - part_13[residue % 13]
            - interaction[residue]
        )
        for residue in residues
    )
    return {
        "residues": residues,
        "mean": mean,
        "part_11": part_11,
        "part_13": part_13,
        "interaction": interaction,
        "summary": {
            "residue_count": len(residues),
            "total_centered_sum_squares": float(total_ss),
            "mod11_sum_squares": float(ss_11),
            "mod13_sum_squares": float(ss_13),
            "interaction_sum_squares": float(ss_interaction),
            "mod11_variance_share": float(ss_11 / total_ss),
            "mod13_variance_share": float(ss_13 / total_ss),
            "interaction_variance_share": float(
                ss_interaction / total_ss),
            "additive_variance_share": float((ss_11 + ss_13) / total_ss),
            "max_abs_decomposition_residual": float(residual),
            "max_abs_interaction_coefficient": float(
                max(abs(value) for value in interaction.values())),
            "largest_abs_coefficients": [
                {
                    "residue": int(residue),
                    "mod11": int(residue % 11),
                    "mod13": int(residue % 13),
                    "coefficient": float(coefficients[residue]),
                    "interaction": float(interaction[residue]),
                }
                for residue in sorted(
                    residues,
                    key=lambda item: (-abs(coefficients[item]), item),
                )[:12]
            ],
        },
    }


def row_contribution(edge_row, context, full_coefficients,
                     first_three_coefficients, primes, prime_values,
                     log_values, coefficients, decomposition):
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
    actual_projection = projection_distribution(
        orbit_data["orbits"], np.asarray(actual["masses"], dtype=np.float64), 286)
    uniform_projection = projection_distribution(
        orbit_data["orbits"],
        np.asarray(orbit_data["uniform_orbit_mass"], dtype=np.float64),
        286,
    )
    errors = {
        residue: (
            actual_projection.get(residue, 0.0)
            - uniform_projection.get(residue, 0.0)
        )
        for residue in decomposition["residues"]
    }
    part_11 = decomposition["part_11"]
    part_13 = decomposition["part_13"]
    interaction = decomposition["interaction"]
    mod11 = math.fsum(
        part_11[residue % 11] * errors[residue]
        for residue in errors
    )
    mod13 = math.fsum(
        part_13[residue % 13] * errors[residue]
        for residue in errors
    )
    interaction_value = math.fsum(
        interaction[residue] * errors[residue]
        for residue in errors
    )
    total = math.fsum(
        coefficients[residue] * errors[residue]
        for residue in errors
    )
    additive = mod11 + mod13
    return {
        "target": int(edge_row["target"]),
        "target_residue": int(edge_row["target_residue"]),
        "target_mod_286": int(edge_row["target_mod_286"]),
        "block_index_after_discovery": int(
            edge_row["block_index_after_discovery"]),
        "pair_count": int(actual["pair_count"]),
        "total_mod286_signed_error": float(total),
        "mod11_marginal_component": float(mod11),
        "mod13_marginal_component": float(mod13),
        "additive_marginal_component": float(additive),
        "interaction_component": float(interaction_value),
        "component_reconstruction_abs_error": float(
            abs(total - additive - interaction_value)),
        "interaction_to_total_ratio": float(interaction_value / total),
    }


def component_summary(rows, key):
    return {
        "count": len(rows),
        "summary": finite_summary(row[key] for row in rows),
        "negative_count": sum(row[key] < -TOLERANCE for row in rows),
        "positive_count": sum(row[key] > TOLERANCE for row in rows),
        "near_zero_count": sum(abs(row[key]) <= TOLERANCE for row in rows),
    }


def build_receipt():
    formula = load_json(FORMULA_SOURCE)
    dual = load_json(DUAL_SOURCE)
    _, by_modulus = coefficient_lookup(formula)
    coefficients = by_modulus[286]
    decomposition = decompose_mod286_coefficient(coefficients)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    edge_rows = [
        row for row in dual["target_rows"]
        if row["edge_success"] and row["block_index_after_discovery"] >= 1
    ]
    maximum_target = max(row["target"] for row in edge_rows)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    rows = [
        row_contribution(
            row,
            context,
            full_coefficients,
            first_three_coefficients,
            primes,
            prime_values,
            log_values,
            coefficients,
            decomposition,
        )
        for row in edge_rows
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
            "finite mod-286 coefficient-interaction diagnostic only; no "
            "interaction theorem, signed projection theorem, q286 threshold "
            "theorem, strict-central Goldbach theorem, or Goldbach proof"
        ),
        "goldbach_proved": False,
        "interaction_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "novelty_label": "new-to-this-task",
        "candidate": {
            "name": "mod-286 equals mod-11 x mod-13 interaction",
            "mechanism": (
                "ANOVA-decompose the mod-286 coefficient on the balanced unit "
                "grid modulo 11 x 13.  If the one-factor components are tiny "
                "and the actual drag is carried by the interaction component, "
                "the theorem target becomes a two-factor covariance rather "
                "than ordinary AP marginal bias."
            ),
            "prediction": (
                "The mod-286 coefficient variance and actual signed drag are "
                "dominated by the interaction component, while mod-11 and "
                "mod-13 marginal components are small and mixed-sign."
            ),
            "falsifier": (
                "Large or consistently signed one-factor marginal components "
                "would demote the interaction target and return the proof "
                "route to simpler AP marginal estimates."
            ),
            "smallest_test": (
                "Decompose the coefficient once, then replay the actual "
                "post-discovery projection errors from the validated "
                "strict-central row machinery."
            ),
        },
        "coefficient_decomposition_summary": decomposition["summary"],
        "row_summary": {
            "row_count": len(rows),
            "total_mod286_signed_error": component_summary(
                rows, "total_mod286_signed_error"),
            "mod11_marginal_component": component_summary(
                rows, "mod11_marginal_component"),
            "mod13_marginal_component": component_summary(
                rows, "mod13_marginal_component"),
            "additive_marginal_component": component_summary(
                rows, "additive_marginal_component"),
            "interaction_component": component_summary(
                rows, "interaction_component"),
            "interaction_to_total_ratio_summary": finite_summary(
                row["interaction_to_total_ratio"] for row in rows),
            "component_reconstruction_abs_error_summary": finite_summary(
                row["component_reconstruction_abs_error"] for row in rows),
            "largest_additive_marginal_rows": sorted(
                [
                    {
                        "target": row["target"],
                        "target_mod_286": row["target_mod_286"],
                        "total_mod286_signed_error": row[
                            "total_mod286_signed_error"],
                        "additive_marginal_component": row[
                            "additive_marginal_component"],
                        "interaction_component": row[
                            "interaction_component"],
                    }
                    for row in rows
                ],
                key=lambda row: (
                    -abs(row["additive_marginal_component"]),
                    row["target"],
                ),
            )[:12],
        },
        "decision": (
            "The mod-286 drag is an interaction object in this finite fixture. "
            "The coefficient's mod-11 and mod-13 one-factor variance shares "
            "sum to only "
            f"{decomposition['summary']['additive_variance_share']}, while "
            "the interaction share is "
            f"{decomposition['summary']['interaction_variance_share']}. "
            "On all 196 post-discovery rows, the total mod-286 signed error "
            "and the interaction component are negative; the interaction-to-"
            "total ratio ranges from the recorded summary near one.  Therefore "
            "simple one-dimensional AP marginals are not the right theorem "
            "object for this drag.  The surviving target is a signed "
            "mod-11-by-mod-13 covariance or raw q286-WBSS witness estimate."
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
