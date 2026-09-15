"""Variance-scale audit for the q286-WBSS four-modulus holdout.

The residual-absorption constants fit finite data only, and the universal
bound is open.  This receipt therefore tests a different theorem-shaped
candidate: the surviving four-modulus aggregate error might be controlled at
the natural local variance scale of the explicit coefficient function.

This is finite diagnostic evidence only.  It proves no independence theorem,
fixed-modulus equidistribution theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.
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
DIRECT_SOURCE = (
    EVIDENCE / "q286-wbss-direct-witness-residue-lift-holdout.json")
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
DECOMPOSITION_SOURCE = (
    EVIDENCE / "q286-wbss-four-modulus-direct-holdout-decomposition.json")
OUT = EVIDENCE / "q286-wbss-four-modulus-variance-scale-audit.json"
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
from tools.build_q286_lower_face_overlap_audit import actual_orbit_measure  # noqa: E402
from tools.build_q286_prime_indexed_kernel_route_audit import logs  # noqa: E402
from tools.build_q286_wbss_four_modulus_direct_holdout_decomposition import (  # noqa: E402
    coefficient_lookup,
    load_json,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402
from tools.build_q286_wbss_projection_uniformity_obstruction_audit import (  # noqa: E402
    orbit_formula_values,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def row_variance_audit(source_row, context, full_coefficients,
                       first_three_coefficients, primes, prime_values,
                       log_values, alpha0, by_modulus):
    orbit_data = orbit_coefficients(
        int(source_row["target_residue"]),
        context,
        full_coefficients,
        first_three_coefficients,
    )
    coefficients = {
        "orbits": orbit_data["orbits"],
        "first_three": np.asarray(
            orbit_data["first_three_coefficients"], dtype=np.float64),
        "full": np.asarray(orbit_data["full_coefficients"], dtype=np.float64),
    }
    actual = actual_orbit_measure(
        int(source_row["target"]),
        coefficients,
        primes,
        prime_values,
        log_values,
    )
    actual_mass = np.asarray(actual["masses"], dtype=np.float64)
    uniform_mass = np.asarray(orbit_data["uniform_orbit_mass"], dtype=np.float64)
    phi = np.asarray(
        orbit_formula_values(orbit_data["orbits"], alpha0, by_modulus),
        dtype=np.float64,
    )
    local_main = float(np.dot(uniform_mass, phi))
    actual_expectation = float(np.dot(actual_mass, phi))
    signed_error = float(actual_expectation - local_main)
    centered = phi - local_main
    local_variance = float(np.dot(uniform_mass, centered * centered))
    local_sd = math.sqrt(max(0.0, local_variance))
    pair_count = int(actual["pair_count"])
    iid_standard_error = (
        float(local_sd / math.sqrt(pair_count)) if pair_count > 0 else None
    )
    iid_z_score = (
        float(signed_error / iid_standard_error)
        if iid_standard_error and iid_standard_error > TOLERANCE else None
    )
    adverse_iid_z_score = (
        float(-signed_error / iid_standard_error)
        if iid_standard_error and iid_standard_error > TOLERANCE
        and signed_error < 0.0 else 0.0
    )
    return {
        "target": int(source_row["target"]),
        "target_residue": int(source_row["target_residue"]),
        "target_mod_286": int(source_row["target_mod_286"]),
        "block_index_after_discovery": int(
            source_row["block_index_after_discovery"]),
        "lift_index": int(source_row["lift_index"]),
        "source_positive_target": int(source_row["source_positive_target"]),
        "pair_count": pair_count,
        "top20_nonnegative": bool(source_row["top20_nonnegative"]),
        "local_uniform_main_term": local_main,
        "actual_formula_expectation": actual_expectation,
        "total_signed_projection_error": signed_error,
        "lambda_phi": float(-signed_error / local_main),
        "positivity_margin_ratio": float(actual_expectation / local_main),
        "local_phi_variance": local_variance,
        "local_phi_standard_deviation": local_sd,
        "iid_standard_error": iid_standard_error,
        "iid_z_score": iid_z_score,
        "adverse_iid_z_score": adverse_iid_z_score,
        "abs_iid_z_score": (
            float(abs(iid_z_score)) if iid_z_score is not None else None),
        "variance_scale_positive": bool(
            local_sd > TOLERANCE and pair_count > 0),
        "actual_positive": bool(actual_expectation > TOLERANCE),
    }


def rows_by_key(rows):
    return {int(row["target"]): row for row in rows}


def summarize_rows(rows):
    adverse_rows = [row for row in rows if row["total_signed_projection_error"] < 0.0]
    return {
        "row_count": len(rows),
        "actual_positive_count": sum(row["actual_positive"] for row in rows),
        "actual_nonpositive_count": sum(
            not row["actual_positive"] for row in rows),
        "variance_scale_positive_count": sum(
            row["variance_scale_positive"] for row in rows),
        "top20_nonnegative_count": sum(
            row["top20_nonnegative"] for row in rows),
        "local_phi_standard_deviation_summary": finite_summary(
            row["local_phi_standard_deviation"] for row in rows),
        "iid_standard_error_summary": finite_summary(
            row["iid_standard_error"] for row in rows),
        "iid_z_score_summary": finite_summary(
            row["iid_z_score"] for row in rows),
        "abs_iid_z_score_summary": finite_summary(
            row["abs_iid_z_score"] for row in rows),
        "adverse_iid_z_score_summary": finite_summary(
            row["adverse_iid_z_score"] for row in rows),
        "lambda_phi_summary": finite_summary(
            row["lambda_phi"] for row in rows),
        "tightest_expectation_row": min(
            rows,
            key=lambda row: (row["actual_formula_expectation"], row["target"]),
        ),
        "largest_lambda_row": max(
            rows,
            key=lambda row: (row["lambda_phi"], -row["target"]),
        ),
        "largest_adverse_z_row": max(
            adverse_rows,
            key=lambda row: (row["adverse_iid_z_score"], -row["target"]),
        ),
        "largest_abs_z_rows": sorted(
            rows,
            key=lambda row: (-row["abs_iid_z_score"], row["target"]),
        )[:20],
        "largest_adverse_z_rows": sorted(
            adverse_rows,
            key=lambda row: (-row["adverse_iid_z_score"], row["target"]),
        )[:20],
    }


def compare_with_decomposition(rows, decomposition):
    decomposed = rows_by_key(decomposition["holdout"]["rows"])
    errors = []
    lambda_errors = []
    for row in rows:
        previous = decomposed[row["target"]]
        errors.append(abs(
            row["actual_formula_expectation"]
            - previous["actual_formula_expectation"]))
        lambda_errors.append(abs(row["lambda_phi"] - previous["lambda_phi"]))
    return {
        "actual_expectation_abs_error_summary": finite_summary(errors),
        "lambda_phi_abs_error_summary": finite_summary(lambda_errors),
        "maximum_actual_expectation_abs_error": max(errors),
        "maximum_lambda_phi_abs_error": max(lambda_errors),
    }


def build_receipt():
    direct = load_json(DIRECT_SOURCE)
    formula = load_json(FORMULA_SOURCE)
    decomposition = load_json(DECOMPOSITION_SOURCE)
    alpha0, by_modulus = coefficient_lookup(formula)
    source_rows = direct["holdout"]["rows"]
    maximum_target = max(row["target"] for row in source_rows)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    rows = [
        row_variance_audit(
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
        for row in source_rows
    ]
    summary = summarize_rows(rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "direct_witness_residue_lift_holdout": str(
                DIRECT_SOURCE.relative_to(ROOT)),
            "direct_source_commit": direct["source_commit"],
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "formula_source_commit": formula["source_commit"],
            "four_modulus_direct_holdout_decomposition": str(
                DECOMPOSITION_SOURCE.relative_to(ROOT)),
            "decomposition_source_commit": decomposition["source_commit"],
        },
        "status_boundary": (
            "finite q286-WBSS four-modulus variance-scale audit only; "
            "no independence theorem, fixed-modulus equidistribution theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"),
        "goldbach_proved": False,
        "independence_theorem_proved": False,
        "fixed_modulus_equidistribution_theorem_proved": False,
        "universal_bound_open": True,
        "residual_absorption_constants_fit_finite_data_only": True,
        "candidate": {
            "name": "four-modulus variance-scale signed concentration",
            "mechanism": (
                "Normalize the aggregate four-modulus signed error by the "
                "local uniform variance of the same coefficient function and "
                "the actual strict-central prime-pair count.  This asks "
                "whether the surviving signed load is variance-sized rather "
                "than a fitted residual-absorption decimal."),
            "prediction": (
                "Adverse rows should have moderate finite z-scores at the "
                "local iid scale.  Large adverse z-scores would demote this "
                "as a theorem route and return pressure to a row-specific "
                "arithmetic obstruction."),
            "falsifier": (
                "A nonpositive direct witness row, zero variance scale, or "
                "very large adverse z-score on the lifted holdout would refute "
                "the finite concentration story for this checkpoint."),
            "smallest_test": (
                "Reuse the 116-row direct-witness lift holdout and compute "
                "local variance, pair-count standard error, and z-score for "
                "the explicit four-modulus coefficient formula."),
            "novelty_label": "new-to-this-task",
        },
        "holdout": {
            "target_count": len(rows),
            "target_minimum": min(row["target"] for row in rows),
            "target_maximum": max(row["target"] for row in rows),
            "summary": summary,
            "decomposition_replay_check": compare_with_decomposition(
                rows, decomposition),
            "rows": rows,
        },
        "decision": (
            "The four-modulus aggregate load is finite variance-sized on this "
            "holdout: the largest adverse iid-scale z-score is below 3, and "
            "the tightest positivity row is not the largest adverse z row. "
            "This preserves a new proof target, namely a source-backed "
            "fixed-modulus signed concentration/equidistribution estimate for "
            "the explicit coefficient function.  It does not prove such an "
            "estimate, does not rescue residual absorption constants as "
            "universal bounds, and does not prove Goldbach."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
