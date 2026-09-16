"""Compare direct q286-WBSS sign-split budgets to anti-landing budgets.

After the anti-landing source-budget audit showed a near-sharp edge rescue
budget, the natural escape is to bypass that edge construction and prove the
raw direct witness B_Phi(N)>0 by splitting the coefficient into positive and
negative cells:

    P_phi(N) = E_mu max(phi,0)
    D_phi(N) = E_mu max(-phi,0)
    B_phi(N) = P_phi(N)-D_phi(N).

This receipt computes the same source-theorem error budget for that direct
sign split.  If it is materially looser than anti-landing, direct witness
positivity should lead.  If it is as sharp or sharper, a naive sign-split
proof is not the escape; the proof needs an adapted signed estimate.

Finite theorem-budget audit only.  It proves no direct witness theorem,
signed binary-prime correlation theorem, q286 threshold theorem,
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
DUAL_SOURCE = EVIDENCE / "q286-lower-face-dual-edge-audit.json"
ANTI_SOURCE = EVIDENCE / "q286-anti-landing-source-budget-audit.json"
OUT = EVIDENCE / "q286-direct-witness-sign-split-budget-audit.json"
TOLERANCE = 1e-12

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


def split_budget(target, target_residue, target_mod_286, block_index,
                 actual_masses, phi, family):
    positive = np.maximum(phi, 0.0)
    negative = np.maximum(-phi, 0.0)
    positive_contribution = float(np.dot(actual_masses, positive))
    negative_drag = float(np.dot(actual_masses, negative))
    witness = positive_contribution - negative_drag
    if negative_drag <= TOLERANCE:
        ratio = None
        positive_loss_budget = 1.0
        negative_inflation_budget = None
        symmetric_budget = 1.0
    else:
        ratio = positive_contribution / negative_drag
        if ratio <= 1.0 + TOLERANCE:
            positive_loss_budget = 0.0
            negative_inflation_budget = 0.0
            symmetric_budget = 0.0
        else:
            positive_loss_budget = 1.0 - 1.0 / ratio
            negative_inflation_budget = ratio - 1.0
            symmetric_budget = (ratio - 1.0) / (ratio + 1.0)
    return {
        "target": int(target),
        "target_residue": int(target_residue),
        "target_mod_286": int(target_mod_286),
        "block_index_after_discovery": int(block_index),
        "coefficient_family": family,
        "positive_coefficient_orbit_count": int(np.sum(phi > TOLERANCE)),
        "negative_coefficient_orbit_count": int(np.sum(phi < -TOLERANCE)),
        "zero_coefficient_orbit_count": int(np.sum(np.abs(phi) <= TOLERANCE)),
        "actual_mass_on_positive_coefficients": float(
            np.sum(actual_masses[phi > TOLERANCE])),
        "actual_mass_on_negative_coefficients": float(
            np.sum(actual_masses[phi < -TOLERANCE])),
        "positive_contribution": positive_contribution,
        "negative_drag": negative_drag,
        "direct_witness": witness,
        "positive_to_negative_ratio": ratio,
        "positive_loss_budget_if_negative_exact": positive_loss_budget,
        "negative_inflation_budget_if_positive_exact": (
            negative_inflation_budget),
        "symmetric_relative_error_budget": symmetric_budget,
        "direct_witness_positive": bool(witness > TOLERANCE),
        "needs_sub_percent_symmetric_control": bool(symmetric_budget < 0.01),
        "needs_sub_five_percent_symmetric_control": bool(
            symmetric_budget < 0.05),
    }


def build_rows():
    dual = load_json(DUAL_SOURCE)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    maximum_target = max(row["target"] for row in dual["target_rows"])
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)

    rows = []
    for edge_row in dual["target_rows"]:
        if (not edge_row["edge_success"]
                or edge_row["block_index_after_discovery"] < 1):
            continue
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
            int(edge_row["target"]), coefficients, primes, prime_values,
            log_values)
        actual_masses = np.asarray(actual["masses"], dtype=np.float64)
        slope = float(edge_row["slope"])
        intercept = float(edge_row["intercept"])
        required = float(edge_row["required_edge_gap_for_positivity"])
        gap = coefficients["full"] - (
            slope * coefficients["first_three"] + intercept)
        beta = gap - required
        for family, phi in (("full", coefficients["full"]),
                            ("edge_beta", beta)):
            rows.append(split_budget(
                edge_row["target"],
                edge_row["target_residue"],
                edge_row["target_mod_286"],
                edge_row["block_index_after_discovery"],
                actual_masses,
                phi,
                family,
            ))
    return rows


def summarize(rows):
    return {
        "row_count": len(rows),
        "direct_witness_positive_count": sum(
            row["direct_witness_positive"] for row in rows),
        "needs_sub_percent_symmetric_control_count": sum(
            row["needs_sub_percent_symmetric_control"] for row in rows),
        "needs_sub_five_percent_symmetric_control_count": sum(
            row["needs_sub_five_percent_symmetric_control"] for row in rows),
        "positive_to_negative_ratio_summary": finite_summary(
            row["positive_to_negative_ratio"] for row in rows),
        "direct_witness_summary": finite_summary(
            row["direct_witness"] for row in rows),
        "positive_contribution_summary": finite_summary(
            row["positive_contribution"] for row in rows),
        "negative_drag_summary": finite_summary(
            row["negative_drag"] for row in rows),
        "symmetric_relative_error_budget_summary": finite_summary(
            row["symmetric_relative_error_budget"] for row in rows),
        "positive_loss_budget_if_negative_exact_summary": finite_summary(
            row["positive_loss_budget_if_negative_exact"] for row in rows),
        "negative_inflation_budget_if_positive_exact_summary": finite_summary(
            row["negative_inflation_budget_if_positive_exact"]
            for row in rows),
        "tightest_symmetric_budget_row": min(
            rows,
            key=lambda row: (
                row["symmetric_relative_error_budget"], row["target"]),
        ),
    }


def build_receipt():
    anti = load_json(ANTI_SOURCE)
    rows = build_rows()
    by_family = {
        family: [row for row in rows if row["coefficient_family"] == family]
        for family in ("full", "edge_beta")
    }
    anti_tight = anti["summary"]["post_discovery_rows"][
        "tightest_symmetric_budget_row"]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "lower_face_dual_edge_audit": str(DUAL_SOURCE.relative_to(ROOT)),
            "anti_landing_source_budget_audit": str(
                ANTI_SOURCE.relative_to(ROOT)),
            "anti_landing_source_commit": anti["source_commit"],
        },
        "status": "HOLD_direct_sign_split_not_escape_from_sharp_correlation",
        "status_boundary": (
            "finite direct-witness sign-split budget audit only; no direct "
            "witness theorem, signed binary-prime correlation theorem, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof"),
        "goldbach_proved": False,
        "direct_witness_theorem_proved": False,
        "signed_binary_prime_correlation_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "raw direct-witness positive/negative sign split",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Bypass the dual-edge anti-landing construction and try to "
                "prove B_Phi(N)>0 directly by bounding mass landing on "
                "positive and negative coefficient cells."),
            "prediction": (
                "If this is a useful escape from the near-sharp anti-landing "
                "route, the direct sign split should have a looser source "
                "budget than the anti-landing split."),
            "falsifier": (
                "If the direct sign split is as sharp or sharper, then a "
                "naive positive/negative coefficient landing theorem is not "
                "the escape hatch; the proof needs a more adapted signed "
                "estimate."),
            "smallest_test": (
                "Compute P=max(phi,0) and D=max(-phi,0) source-error budgets "
                "for the full and edge-beta coefficients on the same 196 "
                "post-discovery rows."),
        },
        "budget_formulas": anti["budget_formulas"],
        "anti_landing_reference": {
            "tightest_target": anti_tight["target"],
            "tightest_ratio": anti_tight[
                "positive_to_negative_rescue_ratio"],
            "tightest_symmetric_budget": anti_tight[
                "symmetric_relative_error_budget"],
        },
        "summary": {
            "post_discovery_row_count": len(by_family["full"]),
            "full": summarize(by_family["full"]),
            "edge_beta": summarize(by_family["edge_beta"]),
        },
        "decision": (
            "The raw direct-witness sign split does not relax the hard source "
            "budget.  For the full coefficient, the tightest post-discovery "
            "row is target 94856 with P/D about 1.0145084567 and symmetric "
            "relative-error budget about 0.00720198, which is even tighter "
            "than the anti-landing edge budget 0.00948145.  The edge-beta "
            "sign split reproduces the anti-landing budget.  Therefore a "
            "naive positive-versus-negative coefficient landing proof of "
            "direct B_Phi(N)>0 is not an easier route.  The next proof object "
            "must be a more adapted signed binary-prime correlation estimate, "
            "not broad L1, mass-majority, AP counts, or raw sign-split "
            "landing.  Goldbach remains open."),
        "target_rows": rows,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
