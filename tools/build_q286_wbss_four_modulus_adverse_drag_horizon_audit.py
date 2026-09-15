"""Adverse-drag audit for the q286-WBSS aggregate lambda horizon.

The aggregate lambda horizon showed that the full four-modulus signed witness
stays positive on 232 fresh lifted rows.  This receipt asks a stronger finite
question: if every helpful positive projected term is discarded, does the local
main term still beat the adverse projected drag?

Finite horizon evidence only.  It proves no one-sided signed concentration
theorem, fixed-modulus equidistribution theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import itertools
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
HORIZON_SOURCE = (
    EVIDENCE / "q286-wbss-four-modulus-lambda-horizon-holdout.json")
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
OUT = EVIDENCE / "q286-wbss-four-modulus-adverse-drag-horizon-audit.json"
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
    signed_error_terms,
)
from tools.build_q286_wbss_four_modulus_variance_scale_far_lift_holdout import (  # noqa: E402
    orbit_formula_values,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def row_adverse_drag(row, context, full_coefficients,
                     first_three_coefficients, primes, prime_values,
                     log_values, alpha0, by_modulus):
    orbit_data = orbit_coefficients(
        int(row["target_residue"]),
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
        int(row["target"]),
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
    terms, details = signed_error_terms(
        orbit_data["orbits"], actual_mass, uniform_mass, by_modulus)
    total_signed_error = float(math.fsum(terms.values()))
    negative_drag = float(math.fsum(-value for value in terms.values()
                                    if value < -TOLERANCE))
    positive_help = float(math.fsum(value for value in terms.values()
                                    if value > TOLERANCE))
    adverse_only_expectation = float(local_main - negative_drag)
    signed_abs_envelope = float(math.fsum(abs(value)
                                          for value in terms.values()))
    moduli = sorted(terms, key=int)
    subset_rows = []
    for size in range(1, len(moduli) + 1):
        for subset in itertools.combinations(moduli, size):
            expectation = float(local_main + math.fsum(terms[key]
                                                       for key in subset))
            subset_rows.append({
                "moduli": list(subset),
                "expectation": expectation,
                "positive": bool(expectation > TOLERANCE),
            })
    minimum_subset = min(
        subset_rows, key=lambda item: (item["expectation"], item["moduli"]))
    return {
        "target": int(row["target"]),
        "target_residue": int(row["target_residue"]),
        "target_mod_286": int(row["target_mod_286"]),
        "lift_index": int(row["lift_index"]),
        "source_positive_target": int(row["source_positive_target"]),
        "pair_count": int(actual["pair_count"]),
        "local_uniform_main_term": local_main,
        "actual_formula_expectation": actual_expectation,
        "formula_reconstruction_error": (
            float(abs(actual_expectation - row["actual_formula_expectation"]))
            if "actual_formula_expectation" in row else None),
        "signed_error_by_modulus": {key: float(value)
                                    for key, value in terms.items()},
        "projection_details_by_modulus": details,
        "total_signed_projection_error": total_signed_error,
        "lambda_phi": float(-total_signed_error / local_main),
        "positive_modulus_help": positive_help,
        "negative_modulus_drag": negative_drag,
        "negative_drag_ratio": float(negative_drag / local_main),
        "adverse_only_expectation": adverse_only_expectation,
        "adverse_only_positive": bool(
            adverse_only_expectation > TOLERANCE),
        "signed_error_abs_envelope": signed_abs_envelope,
        "signed_cancellation_ratio": (
            float(abs(total_signed_error) / signed_abs_envelope)
            if signed_abs_envelope > TOLERANCE else None),
        "minimum_projected_subset_expectation": minimum_subset,
        "all_projected_subsets_positive": all(
            item["positive"] for item in subset_rows),
        "projected_subset_count": len(subset_rows),
    }


def summarize_rows(rows):
    return {
        "row_count": len(rows),
        "actual_positive_count": sum(
            row["actual_formula_expectation"] > TOLERANCE for row in rows),
        "adverse_only_positive_count": sum(
            row["adverse_only_positive"] for row in rows),
        "adverse_only_nonpositive_count": sum(
            not row["adverse_only_positive"] for row in rows),
        "all_projected_subsets_positive_count": sum(
            row["all_projected_subsets_positive"] for row in rows),
        "projected_subset_checks": sum(
            row["projected_subset_count"] for row in rows),
        "actual_expectation_summary": finite_summary(
            row["actual_formula_expectation"] for row in rows),
        "lambda_phi_summary": finite_summary(
            row["lambda_phi"] for row in rows),
        "negative_drag_ratio_summary": finite_summary(
            row["negative_drag_ratio"] for row in rows),
        "adverse_only_expectation_summary": finite_summary(
            row["adverse_only_expectation"] for row in rows),
        "positive_modulus_help_summary": finite_summary(
            row["positive_modulus_help"] for row in rows),
        "negative_modulus_drag_summary": finite_summary(
            row["negative_modulus_drag"] for row in rows),
        "signed_cancellation_ratio_summary": finite_summary(
            row["signed_cancellation_ratio"] for row in rows),
        "formula_reconstruction_error_summary": finite_summary(
            row["formula_reconstruction_error"] for row in rows),
        "largest_negative_drag_row": max(
            rows,
            key=lambda row: (row["negative_drag_ratio"], -row["target"]),
        ),
        "tightest_adverse_only_row": min(
            rows,
            key=lambda row: (row["adverse_only_expectation"], row["target"]),
        ),
        "lowest_subset_expectation_row": min(
            rows,
            key=lambda row: (
                row["minimum_projected_subset_expectation"]["expectation"],
                row["target"],
            ),
        ),
        "largest_negative_drag_rows": sorted(
            rows,
            key=lambda row: (-row["negative_drag_ratio"], row["target"]),
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
    moduli = sorted(rows[0]["signed_error_by_modulus"], key=int)
    for modulus in moduli:
        values = [row["signed_error_by_modulus"][modulus] for row in rows]
        removed = [
            row["actual_formula_expectation"]
            - row["signed_error_by_modulus"][modulus]
            for row in rows
        ]
        only = [
            row["local_uniform_main_term"]
            + row["signed_error_by_modulus"][modulus]
            for row in rows
        ]
        result[modulus] = {
            "negative_count": sum(value < -TOLERANCE for value in values),
            "positive_count": sum(value > TOLERANCE for value in values),
            "signed_error_summary": finite_summary(values),
            "removed_nonpositive_count": sum(
                value <= TOLERANCE for value in removed),
            "removed_expectation_summary": finite_summary(removed),
            "only_nonpositive_count": sum(
                value <= TOLERANCE for value in only),
            "only_expectation_summary": finite_summary(only),
        }
    return result


def build_receipt():
    horizon = load_json(HORIZON_SOURCE)
    formula = load_json(FORMULA_SOURCE)
    alpha0, by_modulus = coefficient_lookup(formula)
    source_rows = horizon["holdout"]["rows"]
    maximum_target = max(row["target"] for row in source_rows)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    rows = [
        row_adverse_drag(
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
            "lambda_horizon_holdout": str(HORIZON_SOURCE.relative_to(ROOT)),
            "lambda_horizon_source_commit": horizon["source_commit"],
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "formula_source_commit": formula["source_commit"],
        },
        "status_boundary": (
            "finite q286-WBSS four-modulus adverse-drag horizon audit only; "
            "no one-sided signed concentration theorem, fixed-modulus "
            "equidistribution theorem, q286 threshold theorem, strict-central "
            "Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "one_sided_signed_concentration_theorem_proved": False,
        "fixed_modulus_equidistribution_theorem_proved": False,
        "universal_negative_drag_bound_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "four-modulus one-sided adverse-drag envelope",
            "mechanism": (
                "Decompose the successful lambda horizon into the four "
                "projected errors and discard every helpful positive term. "
                "The finite certificate is local_main - total_negative_drag "
                "> 0, which is stronger than relying on signed cancellation."),
            "prediction": (
                "If the aggregate route is theorem-shaped, the adverse-only "
                "envelope should stay below the local main term on the fresh "
                "horizon, and no single projected modulus should be essential."),
            "falsifier": (
                "Any row with local_main <= total_negative_drag would kill "
                "the adverse-drag finite certificate. A nonpositive "
                "single-modulus removal or subset expectation would show "
                "essential dependence on a smaller projected package."),
            "smallest_test": (
                "Replay the 232-row lambda horizon and compute the four "
                "signed projected errors, all single-modulus removals, and "
                "all nonempty projected subsets."),
            "novelty_label": "new-to-this-task",
        },
        "holdout": {
            "target_count": len(rows),
            "target_minimum": min(row["target"] for row in rows),
            "target_maximum": max(row["target"] for row in rows),
            "summary": summary,
            "modulus_summaries": modulus_summary(rows),
            "rows": rows,
        },
        "adverse_drag_certificate_survives_horizon": (
            summary["adverse_only_nonpositive_count"] == 0),
        "all_projected_subsets_survive_horizon": (
            summary["all_projected_subsets_positive_count"] == len(rows)),
        "single_modulus_dependence_detected": any(
            stats["removed_nonpositive_count"] > 0
            or stats["only_nonpositive_count"] > 0
            for stats in modulus_summary(rows).values()
        ),
        "decision": (
            "The successful aggregate lambda horizon has a stronger finite "
            "one-sided certificate: even after discarding all helpful positive "
            "projected terms, local main beats total adverse projected drag on "
            "every checked row.  All single-modulus removals, single-modulus "
            "only expectations, and nonempty projected subsets are positive "
            "on this horizon.  This demotes explanations that require "
            "delicate signed cancellation or one essential projected modulus. "
            "The open theorem target is a source-backed bound on the "
            "one-sided adverse four-modulus drag relative to local main. "
            "Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
