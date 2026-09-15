"""Farther residue-lift holdout for q286-WBSS four-modulus variance scale.

The first variance-scale audit showed moderate finite z-scores on the same
116 lifted rows used by the residual-absorption falsifier.  This receipt makes
one narrow changed-condition test: reuse the same stressed residue classes,
but start the lifts after the previous holdout maximum.

Finite targeted holdout only.  It proves no independence theorem,
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
PREVIOUS_SOURCE = (
    EVIDENCE / "q286-wbss-four-modulus-variance-scale-audit.json")
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
OUT = EVIDENCE / "q286-wbss-four-modulus-variance-scale-far-lift-holdout.json"
FAR_LIFT_COUNT = 4
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
from tools.build_q286_wbss_residual_absorption_residue_lift_holdout import (  # noqa: E402
    PERIOD,
    first_lift_above,
    positive_source_rows,
)
from tools.build_q286_wbss_residual_absorption_threshold_audit import (  # noqa: E402
    absorption_rows,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def far_lift_rows(previous, lift_count=FAR_LIFT_COUNT):
    all_source_rows = absorption_rows(include_discovery=True)
    source_rows = positive_source_rows(all_source_rows)
    lower_bound = int(previous["holdout"]["target_maximum"])
    rows = []
    for source in source_rows:
        first_target = first_lift_above(source["target_residue"], lower_bound)
        for lift_index in range(lift_count):
            target = first_target + lift_index * PERIOD
            rows.append({
                "target": int(target),
                "target_residue": int(target % PERIOD),
                "target_mod_286": int(target % 286),
                "block_index_after_previous_holdout": int(
                    max(0, (target - lower_bound + PERIOD - 1) // PERIOD)),
                "lift_index": int(lift_index),
                "source_positive_target": int(source["target"]),
                "source_pushback_to_main_drag_ratio": float(
                    source["pushback_to_main_drag_ratio"]),
            })
    return rows, lower_bound, len(source_rows)


def row_variance_holdout(edge_row, context, full_coefficients,
                         first_three_coefficients, primes, prime_values,
                         log_values, alpha0, by_modulus):
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
        "full": np.asarray(orbit_data["full_coefficients"], dtype=np.float64),
    }
    actual = actual_orbit_measure(
        int(edge_row["target"]),
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
    return {
        **edge_row,
        "pair_count": pair_count,
        "local_uniform_main_term": local_main,
        "actual_formula_expectation": actual_expectation,
        "direct_full_expectation": float(actual["full"]),
        "formula_reconstruction_error": float(
            abs(actual_expectation - actual["full"])),
        "total_signed_projection_error": signed_error,
        "lambda_phi": float(-signed_error / local_main),
        "positivity_margin_ratio": float(actual_expectation / local_main),
        "local_phi_variance": local_variance,
        "local_phi_standard_deviation": local_sd,
        "iid_standard_error": iid_standard_error,
        "iid_z_score": iid_z_score,
        "adverse_iid_z_score": (
            float(-iid_z_score)
            if iid_z_score is not None and iid_z_score < 0.0 else 0.0),
        "abs_iid_z_score": (
            float(abs(iid_z_score)) if iid_z_score is not None else None),
        "variance_scale_positive": bool(
            local_sd > TOLERANCE and pair_count > 0),
        "actual_positive": bool(actual_expectation > TOLERANCE),
    }


def summarize_rows(rows):
    adverse_rows = [row for row in rows if row["total_signed_projection_error"] < 0.0]
    return {
        "row_count": len(rows),
        "actual_positive_count": sum(row["actual_positive"] for row in rows),
        "actual_nonpositive_count": sum(
            not row["actual_positive"] for row in rows),
        "variance_scale_positive_count": sum(
            row["variance_scale_positive"] for row in rows),
        "local_uniform_main_summary": finite_summary(
            row["local_uniform_main_term"] for row in rows),
        "actual_expectation_summary": finite_summary(
            row["actual_formula_expectation"] for row in rows),
        "lambda_phi_summary": finite_summary(
            row["lambda_phi"] for row in rows),
        "local_phi_standard_deviation_summary": finite_summary(
            row["local_phi_standard_deviation"] for row in rows),
        "iid_z_score_summary": finite_summary(
            row["iid_z_score"] for row in rows),
        "abs_iid_z_score_summary": finite_summary(
            row["abs_iid_z_score"] for row in rows),
        "adverse_iid_z_score_summary": finite_summary(
            row["adverse_iid_z_score"] for row in rows),
        "formula_reconstruction_error_summary": finite_summary(
            row["formula_reconstruction_error"] for row in rows),
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
        "largest_abs_z_row": max(
            rows,
            key=lambda row: (row["abs_iid_z_score"], -row["target"]),
        ),
        "largest_lambda_rows": sorted(
            rows,
            key=lambda row: (-row["lambda_phi"], row["target"]),
        )[:20],
        "largest_adverse_z_rows": sorted(
            adverse_rows,
            key=lambda row: (-row["adverse_iid_z_score"], row["target"]),
        )[:20],
    }


def build_receipt():
    previous = load_json(PREVIOUS_SOURCE)
    formula = load_json(FORMULA_SOURCE)
    alpha0, by_modulus = coefficient_lookup(formula)
    edge_rows, lower_bound, source_residue_count = far_lift_rows(previous)
    maximum_target = max(row["target"] for row in edge_rows)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    rows = [
        row_variance_holdout(
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
    summary = summarize_rows(rows)
    previous_summary = previous["holdout"]["summary"]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "previous_variance_scale_audit": str(
                PREVIOUS_SOURCE.relative_to(ROOT)),
            "previous_source_commit": previous["source_commit"],
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "formula_source_commit": formula["source_commit"],
        },
        "status_boundary": (
            "finite q286-WBSS four-modulus far-lift holdout only; no "
            "independence theorem, fixed-modulus equidistribution theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"),
        "goldbach_proved": False,
        "independence_theorem_proved": False,
        "fixed_modulus_equidistribution_theorem_proved": False,
        "universal_bound_open": True,
        "residual_absorption_constants_fit_finite_data_only": True,
        "candidate": {
            "name": "four-modulus variance-scale far-lift stress holdout",
            "mechanism": (
                "Reuse the stressed positive-pushback residue classes, but "
                "lift them beyond the previous variance-scale holdout and "
                "measure the same explicit four-modulus coefficient function "
                "against local variance and actual strict-central pair count."),
            "prediction": (
                "If the variance-scale route is portable, the direct witness "
                "should remain positive and adverse z-scores should stay "
                "moderate on the farther lifts. A fixed below-3 cap is a "
                "separate finite subclaim and can fail without killing "
                "direct positivity."),
            "falsifier": (
                "A nonpositive direct witness row kills this far-lift direct "
                "checkpoint. A larger adverse z-score kills the narrower "
                "below-3 finite cap and forces a looser or arithmetic "
                "concentration target."),
            "smallest_test": (
                "Take the same 29 source residue classes and evaluate their "
                "next four period-lifts after the prior 116-row holdout."),
            "novelty_label": "new-to-this-task",
        },
        "previous_holdout": {
            "source_target_maximum": int(lower_bound),
            "row_count": previous_summary["row_count"],
            "maximum_lambda_phi": previous_summary[
                "lambda_phi_summary"]["maximum"],
            "maximum_adverse_iid_z_score": previous_summary[
                "adverse_iid_z_score_summary"]["maximum"],
        },
        "holdout": {
            "source_positive_residue_count": source_residue_count,
            "lift_count_per_residue": FAR_LIFT_COUNT,
            "target_count": len(rows),
            "target_minimum": min(row["target"] for row in rows),
            "target_maximum": max(row["target"] for row in rows),
            "summary": summary,
            "rows": rows,
        },
        "direct_witness_survives_far_lift_holdout": (
            summary["actual_nonpositive_count"] == 0),
        "below_three_adverse_z_cap_survives_far_lift_holdout": (
            summary["adverse_iid_z_score_summary"]["maximum"] < 3.0),
        "previous_max_lambda_exceeded": (
            summary["lambda_phi_summary"]["maximum"]
            > previous_summary["lambda_phi_summary"]["maximum"]),
        "previous_max_adverse_z_exceeded": (
            summary["adverse_iid_z_score_summary"]["maximum"]
            > previous_summary["adverse_iid_z_score_summary"]["maximum"]),
        "decision": (
            "The farther targeted lift preserves direct four-modulus "
            "positivity on every checked row, but it falsifies the narrower "
            "finite subclaim that adverse iid-scale z stays below 3.  The "
            "variance-scale route remains live only as a looser signed "
            "concentration/equidistribution target tied to local main-term "
            "positivity, not as a fixed three-sigma cap.  Residual absorption "
            "constants remain finite fits only, and Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
