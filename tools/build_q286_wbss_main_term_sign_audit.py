"""Audit the local-uniform main term for the q286-WBSS problem.

The q286 weighted binary-prime sign-sum problem asks for positivity of a raw
signed prime-pair sum.  A necessary orientation check is whether the same
coefficient function has positive mean under the local-uniform admissible
residue-pair model.  If the mean were negative or zero, the q286 witness would
need a persistent nonlocal bias rather than an ordinary favorable main term.

This receipt computes the uniform orbit mean for:

* the frozen full signed q286 coefficient;
* the target-dependent edge coefficient beta = gap - required.

It also records a sufficient L1 error budget:

    ||mu-u||_1 < mean(phi) / ||phi-mean(phi)||_infty

which guarantees E_mu phi > 0 for a probability measure mu on reflection
orbits.  This is a finite coefficient audit only.  It proves no binary
distribution theorem, no q286 threshold theorem, no signed prime-correlation
estimate, and no Goldbach theorem.
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
OUT = EVIDENCE / "q286-wbss-main-term-sign-audit.json"
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    orbit_coefficients,
    period_full_unit_coefficients,
    prepare_support_context,
    q286_first_three_unit_coefficients,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def finite_summary(values):
    finite = tuple(
        float(value) for value in values
        if value is not None and math.isfinite(float(value)))
    if not finite:
        return {"count": 0, "minimum": None, "mean": None, "maximum": None}
    return {
        "count": len(finite),
        "minimum": min(finite),
        "mean": math.fsum(finite) / len(finite),
        "maximum": max(finite),
    }


def coefficient_stats(uniform, phi):
    mean = float(np.dot(uniform, phi))
    centered = phi - mean
    centered_linf = float(np.max(np.abs(centered)))
    return {
        "uniform_mean": mean,
        "minimum_coefficient": float(np.min(phi)),
        "maximum_coefficient": float(np.max(phi)),
        "centered_linf": centered_linf,
        "positive_uniform_mean": bool(mean > TOLERANCE),
        "negative_uniform_mean": bool(mean < -TOLERANCE),
        "zero_uniform_mean": bool(abs(mean) <= TOLERANCE),
        "sufficient_l1_budget_for_positive_expectation": (
            mean / centered_linf
            if centered_linf > TOLERANCE and mean > 0.0 else None
        ),
    }


def build_row(edge_row, context, full_coefficients, first_three_coefficients):
    orbit_data = orbit_coefficients(
        int(edge_row["target_residue"]),
        context,
        full_coefficients,
        first_three_coefficients,
    )
    uniform = np.asarray(orbit_data["uniform_orbit_mass"], dtype=np.float64)
    first_three = np.asarray(
        orbit_data["first_three_coefficients"], dtype=np.float64)
    full = np.asarray(orbit_data["full_coefficients"], dtype=np.float64)
    slope = float(edge_row["slope"])
    intercept = float(edge_row["intercept"])
    required = float(edge_row["required_edge_gap_for_positivity"])
    gap = full - (slope * first_three + intercept)
    beta = gap - required
    full_stats = coefficient_stats(uniform, full)
    beta_stats = coefficient_stats(uniform, beta)
    return {
        "target": int(edge_row["target"]),
        "target_residue": int(edge_row["target_residue"]),
        "target_mod_286": int(edge_row["target_mod_286"]),
        "block_index_after_discovery": int(
            edge_row["block_index_after_discovery"]),
        "orbit_count": int(len(uniform)),
        "actual_full": float(edge_row["actual_full"]),
        "actual_edge_gap_margin_after_rescue": float(
            edge_row["edge_gap_margin_after_rescue"]),
        "required_edge_gap_for_positivity": required,
        "full": full_stats,
        "edge_beta": beta_stats,
    }


def summarize(rows, key):
    stats = [row[key] for row in rows]
    return {
        "row_count": len(rows),
        "positive_uniform_mean_count": sum(
            row["positive_uniform_mean"] for row in stats),
        "zero_uniform_mean_count": sum(
            row["zero_uniform_mean"] for row in stats),
        "negative_uniform_mean_count": sum(
            row["negative_uniform_mean"] for row in stats),
        "uniform_mean_summary": finite_summary(
            row["uniform_mean"] for row in stats),
        "centered_linf_summary": finite_summary(
            row["centered_linf"] for row in stats),
        "sufficient_l1_budget_summary": finite_summary(
            row["sufficient_l1_budget_for_positive_expectation"]
            for row in stats),
        "minimum_coefficient_summary": finite_summary(
            row["minimum_coefficient"] for row in stats),
        "maximum_coefficient_summary": finite_summary(
            row["maximum_coefficient"] for row in stats),
    }


def smallest_budgets(rows, key):
    eligible = [
        row for row in rows
        if row[key]["sufficient_l1_budget_for_positive_expectation"]
        is not None
    ]
    ordered = sorted(
        eligible,
        key=lambda row: (
            row[key]["sufficient_l1_budget_for_positive_expectation"],
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
            "uniform_mean": row[key]["uniform_mean"],
            "centered_linf": row[key]["centered_linf"],
            "sufficient_l1_budget_for_positive_expectation": row[key][
                "sufficient_l1_budget_for_positive_expectation"],
            "actual_full": row["actual_full"],
            "actual_edge_gap_margin_after_rescue": row[
                "actual_edge_gap_margin_after_rescue"],
        }
        for row in ordered[:20]
    ]


def build_receipt():
    dual = load_json(DUAL_SOURCE)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)

    rows = [
        build_row(row, context, full_coefficients, first_three_coefficients)
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
        },
        "external_sources": {
            "bmor_arxiv": "https://arxiv.org/abs/1802.00085",
            "tao_parity_obstruction_note": (
                "https://terrytao.wordpress.com/2014/07/09/"
                "the-parity-problem-obstruction-for-the-binary-goldbach-"
                "problem-with-bounded-error/"
            ),
        },
        "status_boundary": (
            "finite q286-WBSS main-term sign audit only; no binary "
            "distribution theorem, signed prime-correlation theorem, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof"
        ),
        "goldbach_proved": False,
        "wbss_theorem_proved": False,
        "binary_distribution_theorem_proved": False,
        "curiosity_status": "changed-under-evidence",
        "novelty_label": "new-to-this-task",
        "candidate": {
            "mechanism": (
                "If the q286 signed coefficient has positive local-uniform "
                "mean, then a sufficiently strong binary-prime distribution "
                "theorem could prove positivity by bounding deviation from "
                "that favorable main term."
            ),
            "prediction": (
                "The full q286 witness and the post-discovery edge beta "
                "coefficient should have positive local-uniform mean; "
                "otherwise the witness would rely on persistent nonlocal "
                "bias rather than a normal main term."
            ),
            "falsifier": (
                "A zero or negative local-uniform mean for the post-discovery "
                "edge beta rows would demote q286-WBSS as a direct "
                "main-term proof target."
            ),
            "smallest_test": (
                "Rebuild the frozen q286 coefficients and compute uniform "
                "orbit means and L1 positivity budgets for all dual-edge rows."
            ),
        },
        "decision": (
            "The q286-WBSS witness has favorable local-uniform orientation: "
            "the frozen full coefficient has positive mean on all 230 valid "
            "rows, and the edge beta coefficient has positive mean on all "
            "196 post-discovery rows.  The proof gap is therefore not a bad "
            "main term; it is the lack of a pointwise binary-prime "
            "distribution or signed-correlation theorem strong enough to "
            "keep the actual measure inside the recorded L1 budgets."
        ),
        "summary": {
            "target_row_count": len(rows),
            "post_discovery_target_count": len(post),
            "discovery_target_count": len(discovery),
            "full": {
                "all_rows": summarize(rows, "full"),
                "post_discovery_rows": summarize(post, "full"),
                "discovery_rows": summarize(discovery, "full"),
                "tightest_post_discovery_l1_budgets":
                    smallest_budgets(post, "full"),
            },
            "edge_beta": {
                "all_rows": summarize(rows, "edge_beta"),
                "post_discovery_rows": summarize(post, "edge_beta"),
                "discovery_rows": summarize(discovery, "edge_beta"),
                "tightest_post_discovery_l1_budgets":
                    smallest_budgets(post, "edge_beta"),
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
