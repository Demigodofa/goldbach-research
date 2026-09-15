"""Test whether q286-WBSS can be proved by blunt L1 uniformity.

The main-term sign audit found favorable local-uniform means and recorded the
sufficient condition

    ||mu-u||_1 < mean(phi) / ||phi-mean(phi)||_infty.

This receipt compares that sufficient L1 budget with the actual checked
strict-central binary-prime orbit measures.  If successful rows already have
L1 distances far above the budget, then a proof based on total L1 closeness to
uniform is too strong for the phenomenon being measured.

Finite diagnostic only.  It proves no binary distribution theorem, signed
correlation theorem, q286 threshold theorem, strict-central Goldbach theorem,
or Goldbach theorem.
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
DUAL_SOURCE = EVIDENCE / "q286-lower-face-dual-edge-audit.json"
MAIN_TERM_SOURCE = EVIDENCE / "q286-wbss-main-term-sign-audit.json"
OUT = EVIDENCE / "q286-wbss-l1-budget-obstruction-audit.json"
PERIOD = 10010
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
from tools.build_q286_wbss_main_term_sign_audit import (  # noqa: E402
    coefficient_stats,
    finite_summary,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def expectation_stats(uniform, actual_mass, phi):
    stats = coefficient_stats(uniform, phi)
    actual_expectation = float(np.dot(actual_mass, phi))
    signed_error = actual_expectation - stats["uniform_mean"]
    l1_distance = float(np.sum(np.abs(actual_mass - uniform)))
    budget = stats["sufficient_l1_budget_for_positive_expectation"]
    return {
        **stats,
        "actual_expectation": actual_expectation,
        "signed_error_from_uniform_mean": signed_error,
        "actual_positive": bool(actual_expectation > TOLERANCE),
        "actual_l1_distance_from_uniform": l1_distance,
        "actual_l1_within_sufficient_budget": bool(
            budget is not None and l1_distance < budget),
        "actual_l1_to_budget_ratio": (
            l1_distance / budget
            if budget is not None and budget > TOLERANCE else None),
    }


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
    uniform = np.asarray(orbit_data["uniform_orbit_mass"], dtype=np.float64)
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
    beta = gap - required
    full_stats = expectation_stats(uniform, actual_mass, coefficients["full"])
    beta_stats = expectation_stats(uniform, actual_mass, beta)
    return {
        "target": int(edge_row["target"]),
        "target_residue": int(edge_row["target_residue"]),
        "target_mod_286": int(edge_row["target_mod_286"]),
        "block_index_after_discovery": int(
            edge_row["block_index_after_discovery"]),
        "pair_count": int(actual["pair_count"]),
        "total_weight": float(actual["total_weight"]),
        "orbit_count": int(len(uniform)),
        "actual_l1_distance_from_uniform": float(
            np.sum(np.abs(actual_mass - uniform))),
        "actual_effective_support": float(actual["effective_support"]),
        "full": full_stats,
        "edge_beta": beta_stats,
    }


def summarize(rows, key):
    bucket = [row[key] for row in rows]
    return {
        "row_count": len(rows),
        "actual_positive_count": sum(row["actual_positive"]
                                     for row in bucket),
        "actual_l1_within_sufficient_budget_count": sum(
            row["actual_l1_within_sufficient_budget"] for row in bucket),
        "actual_l1_outside_sufficient_budget_count": sum(
            not row["actual_l1_within_sufficient_budget"] for row in bucket),
        "uniform_mean_summary": finite_summary(
            row["uniform_mean"] for row in bucket),
        "actual_expectation_summary": finite_summary(
            row["actual_expectation"] for row in bucket),
        "signed_error_from_uniform_mean_summary": finite_summary(
            row["signed_error_from_uniform_mean"] for row in bucket),
        "sufficient_l1_budget_summary": finite_summary(
            row["sufficient_l1_budget_for_positive_expectation"]
            for row in bucket),
        "actual_l1_distance_summary": finite_summary(
            row["actual_l1_distance_from_uniform"] for row in bucket),
        "actual_l1_to_budget_ratio_summary": finite_summary(
            row["actual_l1_to_budget_ratio"] for row in bucket),
    }


def extreme_rows(rows, key):
    ordered = sorted(
        rows,
        key=lambda row: (
            -(row[key]["actual_l1_to_budget_ratio"] or -1.0),
            row["target"],
        ),
    )
    return [
        {
            "target": row["target"],
            "target_residue": row["target_residue"],
            "target_mod_286": row["target_mod_286"],
            "block_index_after_discovery": row[
                "block_index_after_discovery"],
            "actual_l1_distance_from_uniform": row[
                "actual_l1_distance_from_uniform"],
            "sufficient_l1_budget_for_positive_expectation": row[key][
                "sufficient_l1_budget_for_positive_expectation"],
            "actual_l1_to_budget_ratio": row[key][
                "actual_l1_to_budget_ratio"],
            "uniform_mean": row[key]["uniform_mean"],
            "actual_expectation": row[key]["actual_expectation"],
            "actual_positive": row[key]["actual_positive"],
        }
        for row in ordered[:20]
    ]


def build_receipt():
    dual = load_json(DUAL_SOURCE)
    main_term = load_json(MAIN_TERM_SOURCE)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    maximum_target = max(row["target"] for row in dual["target_rows"])
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
        )
        for row in dual["target_rows"]
        if row["edge_success"]
    ]
    post = [row for row in rows if row["block_index_after_discovery"] >= 1]
    discovery = [row for row in rows
                 if row["block_index_after_discovery"] < 1]

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "lower_face_dual_edge_audit": str(DUAL_SOURCE.relative_to(ROOT)),
            "wbss_main_term_sign_audit": str(
                MAIN_TERM_SOURCE.relative_to(ROOT)),
        },
        "source_main_term_decision": main_term["decision"],
        "status_boundary": (
            "finite q286-WBSS L1-budget obstruction audit only; no binary "
            "distribution theorem, signed correlation theorem, q286 "
            "threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"
        ),
        "goldbach_proved": False,
        "l1_uniformity_bridge_theorem_proved": False,
        "blunt_l1_uniformity_bridge_falsified_as_explanation": True,
        "curiosity_status": "changed-under-evidence",
        "novelty_label": "new-to-this-task",
        "candidate": {
            "mechanism": (
                "A favorable local-uniform mean plus a small enough total-L1 "
                "deviation would force signed positivity."
            ),
            "prediction": (
                "If total-L1 uniformity is the correct bridge, checked "
                "positive rows should fall inside the sufficient L1 budgets."
            ),
            "falsifier": (
                "If checked positive rows have actual total-L1 distance far "
                "above the sufficient budgets, total-L1 uniformity is too "
                "strong and the bridge must be coefficient-specific."
            ),
            "smallest_test": (
                "Compare actual orbit L1 distance from local uniform against "
                "the full and edge-beta sufficient L1 budgets on the same "
                "dual-edge rows."
            ),
        },
        "decision": (
            "Blunt total-L1 uniformity is not the q286-WBSS bridge: on the "
            "196 post-discovery rows, actual L1 distance from local uniform "
            "ranges from 0.5533526980785324 to 1.574410774410774, while no "
            "row falls inside either the full-coefficient or edge-beta "
            "sufficient L1 budget.  The surviving theorem target must be a "
            "signed/correlation norm or direct B_Phi(N)>0 estimate, not "
            "ordinary L1 closeness to uniform."
        ),
        "summary": {
            "target_row_count": len(rows),
            "post_discovery_target_count": len(post),
            "discovery_target_count": len(discovery),
            "actual_l1_distance_summary": finite_summary(
                row["actual_l1_distance_from_uniform"] for row in rows),
            "post_discovery_actual_l1_distance_summary": finite_summary(
                row["actual_l1_distance_from_uniform"] for row in post),
            "full": {
                "all_rows": summarize(rows, "full"),
                "post_discovery_rows": summarize(post, "full"),
                "discovery_rows": summarize(discovery, "full"),
                "largest_post_discovery_l1_to_budget_ratios":
                    extreme_rows(post, "full"),
            },
            "edge_beta": {
                "all_rows": summarize(rows, "edge_beta"),
                "post_discovery_rows": summarize(post, "edge_beta"),
                "discovery_rows": summarize(discovery, "edge_beta"),
                "largest_post_discovery_l1_to_budget_ratios":
                    extreme_rows(post, "edge_beta"),
            },
        },
        "target_rows": rows,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
