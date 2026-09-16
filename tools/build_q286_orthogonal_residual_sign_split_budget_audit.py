"""Audit the q286 orthogonal-residual sign-split source budget.

The orthogonal-rescue decomposition writes

    full(N) = aligned(N) + <mu_N, h_a>.

Splitting the residual coefficient h_a into positive and negative cells gives

    full(N) = aligned(N) + P_h(N) - D_h(N).

This receipt asks whether that residual-specific sign split is materially
easier than the raw full-coefficient sign split.  If the tight rows still
require sub-percent source control, the residual split is a sharper theorem
object but not an escape from signed binary-prime correlation.

Finite theorem-budget audit only.  It proves no residual lower-tail theorem,
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
ORTHOGONAL_SOURCE = EVIDENCE / "q286-orthogonal-rescue-decomposition.json"
DIRECT_SOURCE = EVIDENCE / "q286-direct-witness-sign-split-budget-audit.json"
PROJECTION_SOURCE = EVIDENCE / "q286-projection-cone-budget-audit.json"
OUT = EVIDENCE / "q286-orthogonal-residual-sign-split-budget-audit.json"
PERIOD = 10010
TOLERANCE = 1e-12

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    SELECTED_TARGETS,
    combined_fixed_strict_central_coefficient_receipt,
    period_full_unit_coefficients,
    prepare_support_context,
    q286_first_three_unit_coefficients,
)
from tools.build_q286_lower_face_overlap_audit import (  # noqa: E402
    actual_orbit_measure,
)
from tools.build_q286_orthogonal_residual_norm_certificate import (  # noqa: E402
    residual_operator,
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


def budget_row(target, operator, primes, prime_values, log_values):
    orbit_data = operator["orbit_data"]
    actual = actual_orbit_measure(
        target,
        {
            "orbits": orbit_data["orbits"],
            "first_three": orbit_data["first_three_coefficients"],
            "full": orbit_data["full_coefficients"],
        },
        primes,
        prime_values,
        log_values,
    )
    masses = np.asarray(actual["masses"], dtype=np.float64)
    first_three = float(np.dot(operator["first_three"], masses))
    full = float(np.dot(operator["full"], masses))
    aligned = operator["uniform_full"] + operator["alpha"] * first_three
    residual = np.asarray(operator["residual"], dtype=np.float64)
    positive = np.maximum(residual, 0.0)
    negative = np.maximum(-residual, 0.0)
    positive_residual = float(np.dot(masses, positive))
    negative_residual = float(np.dot(masses, negative))
    residual_action = positive_residual - negative_residual
    reconstructed = aligned + residual_action
    surplus = reconstructed
    denominator = positive_residual + negative_residual
    if surplus <= TOLERANCE:
        positive_loss_budget = 0.0
        negative_inflation_budget = 0.0
        symmetric_budget = 0.0
    else:
        positive_loss_budget = (
            surplus / positive_residual
            if positive_residual > TOLERANCE else 1.0)
        negative_inflation_budget = (
            surplus / negative_residual
            if negative_residual > TOLERANCE else 1.0)
        symmetric_budget = (
            surplus / denominator if denominator > TOLERANCE else 1.0)
    ratio = (
        (aligned + positive_residual) / negative_residual
        if negative_residual > TOLERANCE else None)
    return {
        "target": int(target),
        "target_residue": int(target % PERIOD),
        "target_mod_286": int(target % 286),
        "actual_first_three": first_three,
        "aligned_only_full_action_to_principal": aligned,
        "positive_residual_contribution": positive_residual,
        "negative_residual_drag": negative_residual,
        "orthogonal_residual_action": residual_action,
        "actual_full_action": full,
        "reconstructed_full_action": reconstructed,
        "reconstruction_error": abs(full - reconstructed),
        "aligned_plus_positive_to_negative_ratio": ratio,
        "positive_loss_budget_if_negative_and_aligned_exact": (
            positive_loss_budget),
        "negative_inflation_budget_if_positive_and_aligned_exact": (
            negative_inflation_budget),
        "symmetric_positive_negative_error_budget_with_aligned_exact": (
            symmetric_budget),
        "actual_full_positive": bool(full > TOLERANCE),
        "needs_sub_percent_symmetric_control": bool(symmetric_budget < 0.01),
        "needs_sub_five_percent_symmetric_control": bool(
            symmetric_budget < 0.05),
        "interpretation": (
            "With aligned exact, P_h >= (1-eps)P_actual and "
            "D_h <= (1+eps)D_actual imply full>0 when "
            "eps < full_actual/(P_h+D_h)."),
    }


def summarize(rows):
    positive_rows = [row for row in rows if row["actual_full_positive"]]
    return {
        "target_count": len(rows),
        "actual_full_positive_count": len(positive_rows),
        "actual_full_nonpositive_count": len(rows) - len(positive_rows),
        "needs_sub_percent_symmetric_control_count": sum(
            row["needs_sub_percent_symmetric_control"] for row in positive_rows),
        "needs_sub_five_percent_symmetric_control_count": sum(
            row["needs_sub_five_percent_symmetric_control"]
            for row in positive_rows),
        "aligned_plus_positive_to_negative_ratio_summary": finite_summary(
            row["aligned_plus_positive_to_negative_ratio"]
            for row in positive_rows),
        "symmetric_error_budget_summary": finite_summary(
            row["symmetric_positive_negative_error_budget_with_aligned_exact"]
            for row in positive_rows),
        "positive_loss_budget_summary": finite_summary(
            row["positive_loss_budget_if_negative_and_aligned_exact"]
            for row in positive_rows),
        "negative_inflation_budget_summary": finite_summary(
            row["negative_inflation_budget_if_positive_and_aligned_exact"]
            for row in positive_rows),
        "tightest_positive_symmetric_budget_row": min(
            positive_rows,
            key=lambda row: (
                row[
                    "symmetric_positive_negative_error_budget_with_aligned_exact"],
                row["target"],
            ),
        ),
        "maximum_reconstruction_error": max(
            row["reconstruction_error"] for row in rows),
    }


def build_receipt():
    orthogonal = load_json(ORTHOGONAL_SOURCE)
    direct = load_json(DIRECT_SOURCE)
    projection = load_json(PROJECTION_SOURCE)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    maximum_target = max(SELECTED_TARGETS)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    operators = {
        int(target % PERIOD): residual_operator(
            int(target % PERIOD),
            context,
            full_coefficients,
            first_three_coefficients,
        )
        for target in SELECTED_TARGETS
    }
    rows = [
        budget_row(
            int(target), operators[int(target % PERIOD)], primes,
            prime_values, log_values)
        for target in SELECTED_TARGETS
    ]
    summary = summarize(rows)
    raw_full_reference = direct["summary"]["full"][
        "tightest_symmetric_budget_row"]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "orthogonal_rescue_decomposition": str(
                ORTHOGONAL_SOURCE.relative_to(ROOT)),
            "orthogonal_rescue_source_commit": orthogonal["source_commit"],
            "direct_witness_sign_split_budget": str(
                DIRECT_SOURCE.relative_to(ROOT)),
            "projection_cone_budget": str(
                PROJECTION_SOURCE.relative_to(ROOT)),
            "projection_cone_source_commit": projection["source_commit"],
        },
        "status": "HOLD_residual_sign_split_is_sharper_but_still_near_sharp",
        "status_boundary": (
            "finite residual sign-split source-budget audit only; no "
            "orthogonal residual lower-tail theorem, signed binary-prime "
            "correlation theorem, q286 threshold theorem, strict-central "
            "Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "orthogonal_residual_lower_tail_theorem_proved": False,
        "signed_binary_prime_correlation_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "orthogonal-residual positive/negative landing",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use the orthogonal decomposition full=aligned+<mu,h> and "
                "split only h into positive and negative residual cells.  "
                "The aligned component is kept exact in the finite budget, "
                "so the source theorem only pays the residual landing error."),
            "prediction": (
                "If the orthogonal residual route is a useful escape, its "
                "positive/negative source budget should be materially looser "
                "than the raw full-coefficient sign split."),
            "falsifier": (
                "If the tight residual row still needs sub-percent control, "
                "then residual sign landing is a better-shaped theorem object "
                "but not an escape from sharp signed correlation."),
            "smallest_test": (
                "Compute aligned+P_h>D_h budgets on the seven frozen "
                "signed-pair operator targets from the orthogonal-rescue "
                "decomposition."),
        },
        "budget_formulas": {
            "positive_loss_if_negative_and_aligned_exact": (
                "P_h may be replaced by (1-eps)P_h while D_h and aligned are "
                "exact when eps < full/(P_h)."),
            "negative_inflation_if_positive_and_aligned_exact": (
                "D_h may be replaced by (1+eps)D_h while P_h and aligned are "
                "exact when eps < full/(D_h)."),
            "symmetric_residual_landing_error_with_aligned_exact": (
                "P_h >= (1-eps)P_h_actual and "
                "D_h <= (1+eps)D_h_actual imply full>0 when "
                "eps < full_actual/(P_h+D_h)."),
        },
        "raw_full_sign_split_reference": {
            "tightest_target": raw_full_reference["target"],
            "tightest_symmetric_budget": raw_full_reference[
                "symmetric_relative_error_budget"],
        },
        "summary": summary,
        "decision": (
            "The orthogonal residual sign split is a sharper theorem object "
            "than raw full-coefficient landing, but it is still near-sharp.  "
            "The tight positive row is target 94856 with symmetric residual "
            "landing budget about 0.00939619 when the aligned component is "
            "treated as exact.  This is slightly looser than the raw full "
            "sign-split budget 0.00720198, but still requires sub-percent "
            "source control.  Therefore the residual route remains live only "
            "as a coefficient-specific signed lower-tail estimate for "
            "<nu_N,h_a>; broad AP counts, projection uniformity, global norm "
            "bounds, and raw residual sign landing do not close the bridge.  "
            "Goldbach remains open."),
        "target_rows": rows,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
