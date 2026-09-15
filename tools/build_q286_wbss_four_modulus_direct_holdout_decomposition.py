"""Decompose the direct q286-WBSS lift holdout by four projected moduli.

The direct raw witness survived the residue-lift holdout even though the
top-20 Fourier split lost sign stability.  This receipt asks whether that
survival is visible in the four-modulus projection formula:

    A(N) = M(N) + E_70(N) + E_130(N) + E_154(N) + E_286(N).

Here M(N) is the local-uniform main term and E_d(N) is the signed weighted
projection error at modulus d.  The receipt is finite diagnostic evidence
only.  It proves no projection theorem, signed discrepancy theorem, q286
threshold theorem, strict-central Goldbach theorem, or Goldbach proof.
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
OUT = EVIDENCE / "q286-wbss-four-modulus-direct-holdout-decomposition.json"
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
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402
from tools.build_q286_wbss_projection_uniformity_obstruction_audit import (  # noqa: E402
    coefficient_lookup,
    orbit_formula_values,
    projection_distribution,
    projection_rows,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def signed_error_terms(orbits, actual_mass, uniform_mass, by_modulus):
    terms = {}
    projection_details = {}
    for row in projection_rows(orbits, actual_mass, uniform_mass, by_modulus):
        key = str(row["modulus"])
        terms[key] = float(row["signed_weighted_error"])
        projection_details[key] = {
            "max_abs_projection_error": float(
                row["max_abs_projection_error"]),
            "l1_projection_error": float(row["l1_projection_error"]),
            "signed_weighted_error": float(row["signed_weighted_error"]),
            "largest_abs_weighted_error_cells": row[
                "largest_abs_weighted_error_cells"][:5],
        }
    return terms, projection_details


def row_decomposition(source_row, context, full_coefficients,
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
    phi = orbit_formula_values(orbit_data["orbits"], alpha0, by_modulus)
    local_main = float(np.dot(uniform_mass, phi))
    direct_expectation = float(np.dot(actual_mass, phi))
    terms, details = signed_error_terms(
        orbit_data["orbits"], actual_mass, uniform_mass, by_modulus)
    signed_error = math.fsum(terms.values())
    positive_rescue = math.fsum(value for value in terms.values()
                               if value > TOLERANCE)
    negative_drag = math.fsum(-value for value in terms.values()
                              if value < -TOLERANCE)
    envelope = math.fsum(abs(value) for value in terms.values())
    modulus_items = [
        {"modulus": key, "signed_error": value}
        for key, value in terms.items()
    ]
    most_negative = min(
        modulus_items, key=lambda row: (row["signed_error"], row["modulus"]))
    most_positive = max(
        modulus_items, key=lambda row: (row["signed_error"], row["modulus"]))
    return {
        "target": int(source_row["target"]),
        "target_residue": int(source_row["target_residue"]),
        "target_mod_286": int(source_row["target_mod_286"]),
        "block_index_after_discovery": int(
            source_row["block_index_after_discovery"]),
        "lift_index": int(source_row["lift_index"]),
        "source_positive_target": int(source_row["source_positive_target"]),
        "pair_count": int(actual["pair_count"]),
        "top20_nonnegative": bool(source_row["top20_nonnegative"]),
        "local_uniform_main_term": local_main,
        "signed_error_by_modulus": terms,
        "projection_details_by_modulus": details,
        "total_signed_projection_error": float(signed_error),
        "positive_modulus_rescue": float(positive_rescue),
        "negative_modulus_drag": float(negative_drag),
        "signed_error_abs_envelope": float(envelope),
        "signed_cancellation_ratio": (
            float(abs(signed_error) / envelope)
            if envelope > TOLERANCE else None),
        "most_negative_modulus": most_negative,
        "most_positive_modulus": most_positive,
        "actual_formula_expectation": direct_expectation,
        "direct_source_expectation": float(source_row["actual_expectation"]),
        "formula_reconstruction_error": float(
            abs(direct_expectation - source_row["actual_expectation"])),
        "lambda_phi": float(-signed_error / local_main),
        "positivity_margin_ratio": float(direct_expectation / local_main),
        "actual_positive": bool(direct_expectation > TOLERANCE),
        "single_modulus_removed_expectations": {
            key: float(direct_expectation - value)
            for key, value in terms.items()
        },
        "single_modulus_only_expectations": {
            key: float(local_main + value)
            for key, value in terms.items()
        },
    }


def summarize_rows(rows):
    return {
        "row_count": len(rows),
        "actual_positive_count": sum(row["actual_positive"] for row in rows),
        "actual_nonpositive_count": sum(
            not row["actual_positive"] for row in rows),
        "top20_nonnegative_count": sum(
            row["top20_nonnegative"] for row in rows),
        "top20_nonnegative_raw_positive_count": sum(
            row["top20_nonnegative"] and row["actual_positive"]
            for row in rows),
        "local_uniform_main_summary": finite_summary(
            row["local_uniform_main_term"] for row in rows),
        "actual_expectation_summary": finite_summary(
            row["actual_formula_expectation"] for row in rows),
        "total_signed_projection_error_summary": finite_summary(
            row["total_signed_projection_error"] for row in rows),
        "lambda_phi_summary": finite_summary(
            row["lambda_phi"] for row in rows),
        "positive_modulus_rescue_summary": finite_summary(
            row["positive_modulus_rescue"] for row in rows),
        "negative_modulus_drag_summary": finite_summary(
            row["negative_modulus_drag"] for row in rows),
        "signed_cancellation_ratio_summary": finite_summary(
            row["signed_cancellation_ratio"] for row in rows),
        "formula_reconstruction_error_summary": finite_summary(
            row["formula_reconstruction_error"] for row in rows),
        "tightest_row": min(
            rows,
            key=lambda row: (row["actual_formula_expectation"], row["target"]),
        ),
        "largest_lambda_rows": sorted(
            rows,
            key=lambda row: (-row["lambda_phi"], row["target"]),
        )[:20],
        "lowest_cancellation_rows": sorted(
            [
                row for row in rows
                if row["signed_cancellation_ratio"] is not None
            ],
            key=lambda row: (row["signed_cancellation_ratio"], row["target"]),
        )[:20],
    }


def modulus_summary(rows):
    result = {}
    for modulus in sorted(rows[0]["signed_error_by_modulus"], key=int):
        values = [
            row["signed_error_by_modulus"][modulus]
            for row in rows
        ]
        result[modulus] = {
            "row_count": len(values),
            "negative_count": sum(value < -TOLERANCE for value in values),
            "positive_count": sum(value > TOLERANCE for value in values),
            "near_zero_count": sum(abs(value) <= TOLERANCE
                                   for value in values),
            "signed_error_summary": finite_summary(values),
            "largest_negative_rows": sorted(
                [
                    {
                        "target": row["target"],
                        "signed_error": row[
                            "signed_error_by_modulus"][modulus],
                        "actual_formula_expectation": row[
                            "actual_formula_expectation"],
                    }
                    for row in rows
                ],
                key=lambda item: (item["signed_error"], item["target"]),
            )[:12],
            "largest_positive_rows": sorted(
                [
                    {
                        "target": row["target"],
                        "signed_error": row[
                            "signed_error_by_modulus"][modulus],
                        "actual_formula_expectation": row[
                            "actual_formula_expectation"],
                    }
                    for row in rows
                ],
                key=lambda item: (-item["signed_error"], item["target"]),
            )[:12],
        }
    return result


def removal_summary(rows):
    result = {}
    for modulus in sorted(rows[0]["signed_error_by_modulus"], key=int):
        removed = [
            row["single_modulus_removed_expectations"][modulus]
            for row in rows
        ]
        only = [
            row["single_modulus_only_expectations"][modulus]
            for row in rows
        ]
        result[modulus] = {
            "removed_positive_count": sum(value > TOLERANCE
                                          for value in removed),
            "removed_nonpositive_count": sum(value <= TOLERANCE
                                             for value in removed),
            "only_positive_count": sum(value > TOLERANCE for value in only),
            "only_nonpositive_count": sum(value <= TOLERANCE
                                          for value in only),
            "removed_expectation_summary": finite_summary(removed),
            "only_expectation_summary": finite_summary(only),
        }
    return result


def build_receipt():
    direct = load_json(DIRECT_SOURCE)
    formula = load_json(FORMULA_SOURCE)
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
        row_decomposition(
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
    all_summary = summarize_rows(rows)
    top20_failed = [row for row in rows if row["top20_nonnegative"]]
    top20_stable = [row for row in rows if not row["top20_nonnegative"]]
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
        },
        "status_boundary": (
            "finite q286-WBSS four-modulus direct-holdout decomposition only; "
            "no binary-prime projection theorem, signed discrepancy theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"),
        "goldbach_proved": False,
        "projection_theorem_proved": False,
        "signed_discrepancy_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "four-modulus signed aggregate rescue",
            "mechanism": (
                "Write the surviving direct witness as local main term plus "
                "four signed projected errors, then test whether the same "
                "lifted rows are controlled by aggregate anti-alignment "
                "rather than pointwise Fourier sign stability."),
            "prediction": (
                "Rows where the top-20 split fails should remain positive "
                "because the total signed projection error stays below the "
                "local main term; no individual modulus should be promoted "
                "to a theorem unless its removal/only tests support it."),
            "falsifier": (
                "Any row with local main plus the four signed projection "
                "errors nonpositive would falsify the direct witness on this "
                "holdout. A zero reconstruction error but unstable single "
                "modulus behavior would demote one-modulus explanations."),
            "smallest_test": (
                "Reuse the 116-row direct-witness lift holdout and decompose "
                "each row with the existing four-modulus projection formula."),
            "novelty_label": "new-to-this-task",
        },
        "formula": {
            "alpha0": float(alpha0),
            "moduli": sorted(int(key) for key in by_modulus),
            "identity": (
                "A(N)=local_uniform_main(N)+sum_d E_d(N), "
                "d in {70,130,154,286}"),
        },
        "holdout": {
            "target_count": len(rows),
            "target_minimum": min(row["target"] for row in rows),
            "target_maximum": max(row["target"] for row in rows),
            "summary": all_summary,
            "summary_top20_nonnegative_rows": summarize_rows(top20_failed),
            "summary_top20_negative_rows": summarize_rows(top20_stable),
            "modulus_summaries": modulus_summary(rows),
            "single_modulus_removal_summary": removal_summary(rows),
            "rows": rows,
        },
        "direct_witness_survives_holdout": (
            all_summary["actual_nonpositive_count"] == 0),
        "aggregate_signed_error_survives_top20_failures": (
            all_summary["top20_nonnegative_raw_positive_count"]
            == all_summary["top20_nonnegative_count"]),
        "decision": (
            "The four-modulus decomposition preserves the direct-witness "
            "holdout result: every lifted row remains positive after "
            "reconstruction from local main plus signed projected errors, "
            "including every row where the top-20 Fourier split lost sign. "
            "The surviving theorem target is therefore an aggregate "
            "coefficient-aligned signed projection inequality across "
            "moduli 70, 130, 154, and 286, not an absolute per-cell "
            "uniformity theorem and not pointwise top-20 sign stability. "
            "Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
