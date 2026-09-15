"""Fresh residue-lift holdout for the q286-WBSS 11,13 residual budget.

The 11,13 residual-budget audit fit one finite source population.  This
receipt chooses the residue classes where the other three edges pushed
upward, then tests their next period-lifts beyond the old maximum target with
fresh strict-central binary-prime measures.

Finite targeted holdout only.  It proves no 11,13 edge theorem, residual
theorem, character-sum bound, binary-prime projection-control theorem, signed
discrepancy theorem, q286 threshold theorem, strict-central Goldbach theorem,
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
BUDGET_SOURCE = (
    EVIDENCE / "q286-wbss-1113-edge-residual-budget-audit.json")
DUAL_SOURCE = EVIDENCE / "q286-lower-face-dual-edge-audit.json"
OUT = (
    EVIDENCE
    / "q286-wbss-1113-residual-budget-residue-lift-holdout.json")
PERIOD = 10010
FRESH_LIFT_COUNT = 4
TOLERANCE = 1e-10
THETA_THRESHOLDS = (
    ("zero", 0.0),
    ("one_twentieth", 0.05),
    ("one_tenth", 0.1),
    ("one_eighth", 0.125),
    ("one_quarter", 0.25),
    ("one_half", 0.5),
    ("three_quarters", 0.75),
    ("one", 1.0),
)

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    period_full_unit_coefficients,
    prepare_support_context,
    q286_first_three_unit_coefficients,
)
from tools.build_q286_prime_indexed_kernel_route_audit import logs  # noqa: E402
from tools.build_q286_wbss_1113_edge_residual_budget_audit import (  # noqa: E402
    budget_row,
    compute_load_rows,
)
from tools.build_q286_wbss_four_modulus_edge_character_load_audit import (  # noqa: E402
    build_row,
    edge_basis,
    load_json,
)
from tools.build_q286_wbss_four_modulus_factor_anova_audit import (  # noqa: E402
    json_ready,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def first_lift_above(residue, lower_bound):
    multiplier = math.floor((lower_bound - residue) / PERIOD) + 1
    target = residue + multiplier * PERIOD
    if target <= lower_bound:
        target += PERIOD
    if target % 2:
        raise ValueError("lifted target must be even")
    return target


def positive_source_rows(source_rows):
    positives = [
        row for row in source_rows
        if row["residual_positive_pushback"] > TOLERANCE
    ]
    by_residue = {}
    for row in positives:
        residue = row["target_residue"]
        current = by_residue.get(residue)
        if (current is None
                or row["positive_pushback_to_lead_drag_ratio"]
                > current["positive_pushback_to_lead_drag_ratio"]):
            by_residue[residue] = row
    return sorted(
        by_residue.values(),
        key=lambda row: (
            -row["positive_pushback_to_lead_drag_ratio"], row["target"]),
    )


def holdout_edge_rows(source_rows, all_source_rows,
                      lift_count=FRESH_LIFT_COUNT):
    lower_bound = max(row["target"] for row in all_source_rows)
    rows = []
    for source in source_rows:
        first_target = first_lift_above(source["target_residue"], lower_bound)
        for lift_index in range(lift_count):
            target = first_target + lift_index * PERIOD
            rows.append({
                "target": target,
                "target_residue": target % PERIOD,
                "target_mod_286": target % 286,
                "block_index_after_discovery": (
                    max(0, (target - lower_bound + PERIOD - 1) // PERIOD)),
                "source_positive_target": source["target"],
                "source_positive_pushback_to_lead_drag_ratio": (
                    source["positive_pushback_to_lead_drag_ratio"]),
            })
    return rows, lower_bound


def lift_index(row, lower_bound):
    return (row["target"] - first_lift_above(
        row["target_residue"], lower_bound)) // PERIOD


def threshold_profile(name, theta, rows):
    failing = [
        row for row in rows
        if not row["lead_edge_negative"]
        or row["positive_pushback_to_lead_drag_ratio"] is None
        or row["positive_pushback_to_lead_drag_ratio"] > theta + TOLERANCE
    ]
    return {
        "name": name,
        "theta": float(theta),
        "passes_all_rows": not failing,
        "failing_row_count": len(failing),
        "absolute_slack_against_observed_maximum": float(
            theta - max(row["positive_pushback_to_lead_drag_ratio"]
                        for row in rows
                        if row["positive_pushback_to_lead_drag_ratio"]
                        is not None)),
        "failing_rows": sorted(
            failing,
            key=lambda item: (
                -(item["positive_pushback_to_lead_drag_ratio"]
                  if item["positive_pushback_to_lead_drag_ratio"]
                  is not None else math.inf),
                item["target"],
            ),
        )[:20],
    }


def bucket_summary(name, rows):
    valid_ratio_rows = [
        row for row in rows
        if row["positive_pushback_to_lead_drag_ratio"] is not None
    ]
    worst_pushback = max(
        valid_ratio_rows,
        key=lambda row: (
            row["positive_pushback_to_lead_drag_ratio"], row["target"]),
    ) if valid_ratio_rows else None
    lead_nonnegative = [
        row for row in rows if not row["lead_edge_negative"]]
    summary = {
        "name": name,
        "row_count": len(rows),
        "lead_edge_negative_count": sum(
            row["lead_edge_negative"] for row in rows),
        "lead_edge_nonnegative_count": len(lead_nonnegative),
        "lead_edge_nonnegative_rows": sorted(
            lead_nonnegative,
            key=lambda row: (-row["lead_edge_signed_contribution"],
                             row["target"]),
        )[:20],
        "total_edge_negative_after_residual_count": sum(
            row["total_edge_negative_after_residual"] for row in rows),
        "residual_positive_pushback_row_count": sum(
            row["residual_positive_pushback"] > TOLERANCE
            for row in rows),
        "residual_negative_help_row_count": sum(
            row["residual_negative_help"] > TOLERANCE for row in rows),
        "positive_pushback_to_lead_drag_ratio_summary": finite_summary(
            row["positive_pushback_to_lead_drag_ratio"]
            for row in valid_ratio_rows),
        "abs_residual_load_to_lead_drag_ratio_summary": finite_summary(
            row["abs_residual_load_to_lead_drag_ratio"]
            for row in valid_ratio_rows),
        "signed_residual_to_lead_drag_ratio_summary": finite_summary(
            row["signed_residual_to_lead_drag_ratio"]
            for row in valid_ratio_rows),
        "lead_drag_margin_after_positive_pushback_summary": finite_summary(
            row["lead_drag_margin_after_positive_pushback"]
            for row in valid_ratio_rows),
        "observed_minimum_passing_theta_for_positive_pushback": (
            worst_pushback["positive_pushback_to_lead_drag_ratio"]
            if worst_pushback else None),
        "worst_positive_pushback_row": worst_pushback,
    }
    summary["theta_threshold_profiles"] = [
        threshold_profile(threshold_name, theta, rows)
        for threshold_name, theta in THETA_THRESHOLDS
    ]
    summary["largest_positive_pushback_rows"] = sorted(
        valid_ratio_rows,
        key=lambda row: (
            -row["positive_pushback_to_lead_drag_ratio"], row["target"]),
    )[:20]
    summary["source_ratio_to_holdout_ratio_summary"] = finite_summary(
        row["positive_pushback_to_lead_drag_ratio"]
        / max(row["source_positive_pushback_to_lead_drag_ratio"], TOLERANCE)
        for row in valid_ratio_rows
    )
    return summary


def profile_by_name(summary, name):
    return {
        row["name"]: row for row in summary["theta_threshold_profiles"]
    }[name]


def compute_holdout_rows(edge_rows):
    basis, maps = edge_basis()
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    maximum_target = max(row["target"] for row in edge_rows)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    return [
        build_row(
            row,
            context,
            full_coefficients,
            first_three_coefficients,
            primes,
            prime_values,
            log_values,
            basis,
            maps,
        )
        for row in edge_rows
    ]


def holdout_budget_row(row):
    edges = {
        edge["edge_key"]: float(edge["signed_contribution"])
        for edge in row["edge_rows"]
    }
    lead_signed = edges["11,13"]
    lead_drag = -lead_signed
    residual_edges = ("5,7", "5,13", "7,11")
    residual_values = [edges[edge] for edge in residual_edges]
    residual_signed_sum = math.fsum(residual_values)
    residual_positive_pushback = max(0.0, residual_signed_sum)
    residual_negative_help = max(0.0, -residual_signed_sum)
    residual_abs_load = math.fsum(abs(value) for value in residual_values)
    total_edge_signed = lead_signed + residual_signed_sum
    lead_negative = lead_drag > TOLERANCE
    return {
        "target": int(row["target"]),
        "target_residue": int(row["target_residue"]),
        "target_mod_286": int(row["target_mod_286"]),
        "block_index_after_discovery": int(
            row["block_index_after_discovery"]),
        "pair_count": int(row["pair_count"]),
        "lead_edge": "11,13",
        "lead_edge_negative": bool(lead_negative),
        "lead_edge_signed_contribution": lead_signed,
        "lead_edge_negative_drag": lead_drag if lead_negative else 0.0,
        "residual_edge_signed_contributions": {
            edge: edges[edge] for edge in residual_edges
        },
        "residual_edge_signed_sum": float(residual_signed_sum),
        "residual_positive_pushback": float(residual_positive_pushback),
        "residual_negative_help": float(residual_negative_help),
        "residual_abs_load": float(residual_abs_load),
        "positive_pushback_to_lead_drag_ratio": (
            float(residual_positive_pushback / lead_drag)
            if lead_negative else None),
        "abs_residual_load_to_lead_drag_ratio": (
            float(residual_abs_load / lead_drag)
            if lead_negative else None),
        "signed_residual_to_lead_drag_ratio": (
            float(residual_signed_sum / lead_drag)
            if lead_negative else None),
        "lead_drag_margin_after_positive_pushback": (
            float(lead_drag - residual_positive_pushback)
            if lead_negative else None),
        "total_edge_signed_contribution": float(total_edge_signed),
        "total_edge_negative_after_residual": bool(
            total_edge_signed < -TOLERANCE),
    }


def build_receipt():
    budget_source = load_json(BUDGET_SOURCE)
    source_budget_rows = [budget_row(row) for row in compute_load_rows()]
    selected_source_rows = positive_source_rows(source_budget_rows)
    edge_rows, lower_bound = holdout_edge_rows(
        selected_source_rows, source_budget_rows)
    load_rows = compute_holdout_rows(edge_rows)
    metadata_by_target = {row["target"]: row for row in edge_rows}
    holdout_rows = []
    for row in load_rows:
        computed = holdout_budget_row(row)
        metadata = metadata_by_target[computed["target"]]
        holdout_rows.append({
            **computed,
            "lift_index": int(lift_index(computed, lower_bound)),
            "source_positive_target": metadata["source_positive_target"],
            "source_positive_pushback_to_lead_drag_ratio": metadata[
                "source_positive_pushback_to_lead_drag_ratio"],
        })
    all_summary = bucket_summary("all_residue_lift_holdout_rows",
                                 holdout_rows)
    by_lift = {}
    for lift in range(FRESH_LIFT_COUNT):
        rows = [row for row in holdout_rows if row["lift_index"] == lift]
        by_lift[f"lift_{lift}"] = bucket_summary(f"lift_{lift}", rows)

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "edge_residual_budget_audit": str(
                BUDGET_SOURCE.relative_to(ROOT)),
            "edge_residual_budget_source_commit": (
                budget_source["source_commit"]),
            "lower_face_dual_edge_audit": str(DUAL_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite targeted q286-WBSS 11,13 residual-budget residue-lift "
            "holdout only; selected residue classes are adversarially chosen "
            "from prior positive residual pushback rows and only target "
            "values are fresh; no 11,13 edge theorem, residual theorem, "
            "character-sum bound, binary-prime projection-control theorem, "
            "signed discrepancy theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "fresh_holdout_claimed": True,
        "lead_edge_theorem_proved": False,
        "residual_budget_theorem_proved": False,
        "character_sum_bound_proved": False,
        "binary_prime_projection_control_theorem_proved": False,
        "universal_bound_open": True,
        "selection_boundary": (
            "Source residues are unique target residues whose prior residual "
            "edge sum pushed positively against the 11,13 lead drag.  This "
            "is a targeted stress holdout, not an unbiased sample."),
        "candidate": {
            "name": "q286 11,13 residual-budget residue-lift holdout",
            "mechanism": (
                "Keep the CRT coefficient geometry fixed modulo 10010, "
                "lift prior positive-pushback residues beyond the old maximum "
                "target, and recompute strict-central binary-prime measures."),
            "prediction": (
                "If the finite 11,13 residual-budget split is not just a "
                "source-population accident, positive residual pushback should "
                "remain below the 11,13 drag on these later lifted rows."),
            "falsifier": (
                "A lifted row whose positive residual-edge pushback reaches "
                "or exceeds the 11,13 drag falsifies the finite holdout route "
                "for this coefficient split."),
            "smallest_test": (
                "Select unique prior positive-pushback residues and test "
                "their next four period-lifts above the old maximum target."),
            "novelty_label": "new-to-this-task",
        },
        "source_population": {
            "row_count": len(source_budget_rows),
            "positive_pushback_row_count": sum(
                row["residual_positive_pushback"] > TOLERANCE
                for row in source_budget_rows),
            "unique_positive_residue_count": len(selected_source_rows),
            "old_maximum_target": lower_bound,
            "old_observed_minimum_passing_theta": budget_source[
                "summaries"]["all_dual_edge_rows"][
                    "observed_minimum_passing_theta_for_positive_pushback"],
        },
        "holdout": {
            "lift_count_per_residue": FRESH_LIFT_COUNT,
            "target_count": len(holdout_rows),
            "target_minimum": min(row["target"] for row in holdout_rows),
            "target_maximum": max(row["target"] for row in holdout_rows),
            "summary": all_summary,
            "summary_by_lift": by_lift,
        },
        "finite_1113_residual_budget_survives_holdout": (
            all_summary["lead_edge_negative_count"] == all_summary["row_count"]
            and all_summary["total_edge_negative_after_residual_count"]
            == all_summary["row_count"]),
        "point_5_theta_survives_holdout": profile_by_name(
            all_summary, "one_half")["passes_all_rows"],
        "point_25_theta_survives_holdout": profile_by_name(
            all_summary, "one_quarter")["passes_all_rows"],
        "lead_edge_route_demoted_by_holdout": (
            all_summary["lead_edge_negative_count"] < all_summary["row_count"]
            or all_summary["total_edge_negative_after_residual_count"]
            < all_summary["row_count"]),
        "decision": (
            "The targeted fresh residue-lift holdout falsifies the portable "
            "version of the 11,13-led residual-budget route for this "
            f"coefficient split: {all_summary['lead_edge_nonnegative_count']} "
            f"of {all_summary['row_count']} lifted rows lose negative 11,13 "
            "lead-edge drag, and even among rows with negative lead drag the "
            "largest positive-pushback ratio is "
            f"{all_summary['observed_minimum_passing_theta_for_positive_pushback']}. "
            "The source-population theta remains a finite diagnostic, but it "
            "should not be promoted into a theorem target without a changed "
            "mechanism.  The surviving path is a more global signed-witness "
            "estimate or a new aggregate inequality.  Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(json_ready(build_receipt()), indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
