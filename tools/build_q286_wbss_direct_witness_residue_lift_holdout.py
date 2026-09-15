"""Replay the fresh residue-lift holdout against the raw q286-WBSS witness.

The previous residue-lift holdout demoted the top-20 Fourier plus residual
absorption split: many lifted rows lost top-20 negative sign stability.  This
receipt asks the narrower next question: does the unsplit q286-WBSS signed
witness itself remain positive on the same lifted targets?

Finite targeted holdout only.  It proves no q286-WBSS theorem, signed
projection theorem, q286 threshold theorem, strict-central Goldbach theorem,
or Goldbach proof.
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
RESIDUAL_SOURCE = (
    EVIDENCE / "q286-wbss-residual-absorption-residue-lift-holdout.json")
OUT = EVIDENCE / "q286-wbss-direct-witness-residue-lift-holdout.json"
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
from tools.build_q286_prime_indexed_row_filter_order_audit import (  # noqa: E402
    optimized_filter_row,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402
from tools.build_q286_wbss_residual_absorption_residue_lift_holdout import (  # noqa: E402
    FRESH_LIFT_COUNT,
    PERIOD,
    holdout_edge_rows,
    positive_source_rows,
)
from tools.build_q286_wbss_residual_absorption_threshold_audit import (  # noqa: E402
    absorption_rows,
    absorption_rows_for_edge_rows,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def direct_row(edge_row, split_row, context, full_coefficients,
               first_three_coefficients, primes, prime_values, log_values):
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
    uniform = np.asarray(orbit_data["uniform_orbit_mass"], dtype=np.float64)
    actual = actual_orbit_measure(
        int(edge_row["target"]),
        coefficients,
        primes,
        prime_values,
        log_values,
    )
    actual_mass = np.asarray(actual["masses"], dtype=np.float64)
    uniform_mean = float(np.dot(uniform, coefficients["full"]))
    actual_expectation = float(actual["full"])
    signed_error = actual_expectation - uniform_mean
    lambda_phi = -signed_error / uniform_mean
    filter_row = optimized_filter_row(
        int(edge_row["target"]),
        context,
        primes,
        prime_values,
        log_values,
    )
    return {
        "target": int(edge_row["target"]),
        "target_residue": int(edge_row["target_residue"]),
        "target_mod_286": int(edge_row["target_mod_286"]),
        "block_index_after_discovery": int(
            edge_row["block_index_after_discovery"]),
        "lift_index": int(edge_row["lift_index"]),
        "source_positive_target": int(edge_row["source_positive_target"]),
        "source_pushback_to_main_drag_ratio": float(
            edge_row["source_pushback_to_main_drag_ratio"]),
        "pair_count": int(actual["pair_count"]),
        "total_weight": float(actual["total_weight"]),
        "orbit_count": int(len(uniform)),
        "actual_l1_distance_from_uniform": float(
            np.sum(np.abs(actual_mass - uniform))),
        "actual_effective_support": float(actual["effective_support"]),
        "uniform_mean": uniform_mean,
        "actual_expectation": actual_expectation,
        "signed_error_from_uniform_mean": signed_error,
        "lambda_phi": float(lambda_phi),
        "positivity_margin_ratio": float(1.0 - lambda_phi),
        "actual_over_uniform_mean": float(
            actual_expectation / uniform_mean),
        "actual_positive": bool(actual_expectation > TOLERANCE),
        "top20_nonnegative": bool(
            split_row["bandlimited_top20_component"] >= -TOLERANCE),
        "bandlimited_top20_component": float(
            split_row["bandlimited_top20_component"]),
        "residual_five_group_component": float(
            split_row["residual_five_group_component"]),
        "top20_plus_residual_mod286_error": float(
            split_row["bandlimited_top20_component"]
            + split_row["residual_five_group_component"]),
        "reference_first_three_to_principal_ratio": float(
            filter_row["first_three_modes_to_principal_ratio"]),
        "reference_full_action_to_principal_ratio": float(
            filter_row["full_action_to_principal_ratio"]),
        "first_three_reconstruction_error": float(
            abs(actual["first_three"]
                - filter_row["first_three_modes_to_principal_ratio"])),
        "full_reconstruction_error": float(
            abs(actual_expectation
                - filter_row["full_action_to_principal_ratio"])),
    }


def lift_rows():
    all_source_rows = absorption_rows(include_discovery=True)
    source_rows = positive_source_rows(all_source_rows)
    base_edge_rows, lower_bound = holdout_edge_rows(
        source_rows, all_source_rows, lift_count=FRESH_LIFT_COUNT)
    split_rows = absorption_rows_for_edge_rows(
        base_edge_rows, require_top20_negative=False)
    split_by_target = {row["target"]: row for row in split_rows}
    rows = []
    for row in base_edge_rows:
        lift_index = (row["target"] - min(
            other["target"] for other in base_edge_rows
            if other["target_residue"] == row["target_residue"])) // PERIOD
        rows.append({
            **row,
            "lift_index": int(lift_index),
            "source_maximum_target": int(lower_bound),
            "split_row": split_by_target[row["target"]],
        })
    return rows


def summarize(rows):
    worst = min(rows, key=lambda row: (
        row["actual_expectation"], row["target"]))
    tight = min(rows, key=lambda row: (
        row["positivity_margin_ratio"], row["target"]))
    top20_failed = [row for row in rows if row["top20_nonnegative"]]
    top20_failed_positive = [
        row for row in top20_failed if row["actual_positive"]]
    return {
        "row_count": len(rows),
        "actual_positive_count": sum(row["actual_positive"] for row in rows),
        "actual_nonpositive_count": sum(
            not row["actual_positive"] for row in rows),
        "top20_nonnegative_count": len(top20_failed),
        "top20_nonnegative_but_raw_positive_count": len(
            top20_failed_positive),
        "pair_count_summary": finite_summary(row["pair_count"] for row in rows),
        "uniform_mean_summary": finite_summary(
            row["uniform_mean"] for row in rows),
        "actual_expectation_summary": finite_summary(
            row["actual_expectation"] for row in rows),
        "lambda_phi_summary": finite_summary(
            row["lambda_phi"] for row in rows),
        "positivity_margin_ratio_summary": finite_summary(
            row["positivity_margin_ratio"] for row in rows),
        "actual_over_uniform_mean_summary": finite_summary(
            row["actual_over_uniform_mean"] for row in rows),
        "actual_l1_distance_summary": finite_summary(
            row["actual_l1_distance_from_uniform"] for row in rows),
        "maximum_first_three_reconstruction_error": max(
            row["first_three_reconstruction_error"] for row in rows),
        "maximum_full_reconstruction_error": max(
            row["full_reconstruction_error"] for row in rows),
        "minimum_actual_expectation_row": worst,
        "tightest_lambda_row": tight,
        "largest_lambda_rows": sorted(
            rows, key=lambda row: (-row["lambda_phi"], row["target"]))[:20],
    }


def build_receipt():
    source = load_json(RESIDUAL_SOURCE)
    prepared = lift_rows()
    maximum_target = max(row["target"] for row in prepared)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)

    rows = [
        direct_row(
            row,
            row["split_row"],
            context,
            full_coefficients,
            first_three_coefficients,
            primes,
            prime_values,
            log_values,
        )
        for row in prepared
    ]
    summary = summarize(rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "residual_absorption_residue_lift_holdout": str(
                RESIDUAL_SOURCE.relative_to(ROOT)),
            "residual_source_commit": source["source_commit"],
        },
        "status_boundary": (
            "finite targeted q286-WBSS direct-witness residue-lift holdout "
            "only; same lifted rows as the residual-absorption holdout, no "
            "q286-WBSS theorem, signed projection theorem, q286 threshold "
            "theorem, strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "wbss_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "universal_bound_open": True,
        "selection_boundary": (
            "Rows are the targeted positive-residual source residue classes "
            "from the prior 230-row dual-edge population lifted to later "
            "targets. This is adversarial finite evidence, not an unbiased "
            "asymptotic sample."),
        "candidate": {
            "name": "direct raw q286-WBSS residue-lift holdout",
            "mechanism": (
                "Test the unsplit q286-WBSS signed witness on the exact fresh "
                "lifted rows that broke the top-20/residual decomposition."),
            "prediction": (
                "If the previous failure is a bad decomposition rather than "
                "a bad witness, the raw full action should stay positive even "
                "on rows where the top-20 component loses sign."),
            "falsifier": (
                "Any lifted row with actual full q286-WBSS expectation <= 0 "
                "falsifies the raw direct witness on this finite holdout."),
            "smallest_test": (
                "Reuse the 116 lifted targets from the residual holdout and "
                "compute the full normalized q286-WBSS expectation directly "
                "from strict-central prime-pair orbit mass."),
            "novelty_label": "new-to-this-task",
        },
        "holdout": {
            "lift_count_per_residue": FRESH_LIFT_COUNT,
            "target_count": len(rows),
            "target_minimum": min(row["target"] for row in rows),
            "target_maximum": max(row["target"] for row in rows),
            "summary": summary,
            "rows": rows,
        },
        "direct_witness_survives_holdout": (
            summary["actual_nonpositive_count"] == 0),
        "split_failure_interpreted_as_decomposition_failure": (
            summary["actual_nonpositive_count"] == 0
            and summary["top20_nonnegative_count"] > 0),
        "decision": (
            "The targeted residue-lift holdout demotes the top-20 plus "
            "residual absorption split, but it does not demote the unsplit "
            "q286-WBSS signed witness on these rows: every lifted row has "
            "positive full action. Therefore the next theorem target should "
            "avoid pointwise top-20 sign stability and focus on direct "
            "coefficient-aligned signed anti-alignment, an aggregate "
            "projection inequality, or a source-backed fixed-modulus binary "
            "prime correlation theorem. Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
