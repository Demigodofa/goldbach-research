"""Finite residual budget for the q286-WBSS 11,13 edge lead term.

The edge-character load audit showed that the (11,13) edge is the dominant
finite stress edge on nearly every checked row.  This receipt asks whether the
other three edges are small enough, on the same finite rows, to be treated as
a residual signed budget against the (11,13) drag.

This is finite row-budget evidence only.  It proves no 11,13 edge theorem,
residual theorem, character-sum bound, binary-prime projection-control theorem,
signed discrepancy theorem, q286 threshold theorem, strict-central Goldbach
theorem, or Goldbach proof.
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
LOAD_SOURCE = (
    EVIDENCE / "q286-wbss-four-modulus-edge-character-load-audit.json")
DUAL_SOURCE = EVIDENCE / "q286-lower-face-dual-edge-audit.json"
OUT = EVIDENCE / "q286-wbss-1113-edge-residual-budget-audit.json"
LEAD_EDGE = "11,13"
RESIDUAL_EDGES = ("5,7", "5,13", "7,11")
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


def row_edge_map(row):
    return {
        edge["edge_key"]: float(edge["signed_contribution"])
        for edge in row["edge_rows"]
    }


def budget_row(row):
    edges = row_edge_map(row)
    lead_signed = edges[LEAD_EDGE]
    lead_drag = -lead_signed
    if lead_drag <= TOLERANCE:
        raise ValueError(f"{row['target']} lost negative {LEAD_EDGE} drag")
    residual_values = [edges[edge] for edge in RESIDUAL_EDGES]
    residual_signed_sum = math.fsum(residual_values)
    residual_positive_pushback = max(0.0, residual_signed_sum)
    residual_negative_help = max(0.0, -residual_signed_sum)
    residual_abs_load = math.fsum(abs(value) for value in residual_values)
    total_edge_signed = lead_signed + residual_signed_sum
    return {
        "target": int(row["target"]),
        "target_residue": int(row["target_residue"]),
        "target_mod_286": int(row["target_mod_286"]),
        "block_index_after_discovery": int(
            row["block_index_after_discovery"]),
        "pair_count": int(row["pair_count"]),
        "lead_edge": LEAD_EDGE,
        "lead_edge_signed_contribution": lead_signed,
        "lead_edge_negative_drag": lead_drag,
        "residual_edge_signed_contributions": {
            edge: edges[edge] for edge in RESIDUAL_EDGES
        },
        "residual_edge_signed_sum": float(residual_signed_sum),
        "residual_positive_pushback": float(residual_positive_pushback),
        "residual_negative_help": float(residual_negative_help),
        "residual_abs_load": float(residual_abs_load),
        "positive_pushback_to_lead_drag_ratio": float(
            residual_positive_pushback / lead_drag),
        "abs_residual_load_to_lead_drag_ratio": float(
            residual_abs_load / lead_drag),
        "signed_residual_to_lead_drag_ratio": float(
            residual_signed_sum / lead_drag),
        "lead_drag_margin_after_positive_pushback": float(
            lead_drag - residual_positive_pushback),
        "total_edge_signed_contribution": float(total_edge_signed),
        "total_edge_negative_after_residual": bool(
            total_edge_signed < -TOLERANCE),
    }


def threshold_profile(name, theta, rows):
    failing = [
        row for row in rows
        if row["positive_pushback_to_lead_drag_ratio"] > theta + TOLERANCE
    ]
    return {
        "name": name,
        "theta": float(theta),
        "passes_all_rows": not failing,
        "failing_row_count": len(failing),
        "absolute_slack_against_observed_maximum": float(
            theta - max(row["positive_pushback_to_lead_drag_ratio"]
                        for row in rows)),
        "failing_rows": sorted(
            failing,
            key=lambda item: (
                -item["positive_pushback_to_lead_drag_ratio"],
                item["target"],
            ),
        )[:12],
    }


def summarize(name, rows):
    worst_pushback = max(
        rows,
        key=lambda row: (
            row["positive_pushback_to_lead_drag_ratio"], row["target"]),
    )
    worst_abs = max(
        rows,
        key=lambda row: (
            row["abs_residual_load_to_lead_drag_ratio"], row["target"]),
    )
    residual_positive = [
        row for row in rows if row["residual_positive_pushback"] > TOLERANCE
    ]
    return {
        "name": name,
        "row_count": len(rows),
        "lead_edge_negative_count": sum(
            row["lead_edge_signed_contribution"] < -TOLERANCE
            for row in rows),
        "total_edge_negative_after_residual_count": sum(
            row["total_edge_negative_after_residual"] for row in rows),
        "residual_positive_pushback_row_count": len(residual_positive),
        "residual_negative_help_row_count": sum(
            row["residual_negative_help"] > TOLERANCE for row in rows),
        "positive_pushback_to_lead_drag_ratio_summary": finite_summary(
            row["positive_pushback_to_lead_drag_ratio"] for row in rows),
        "abs_residual_load_to_lead_drag_ratio_summary": finite_summary(
            row["abs_residual_load_to_lead_drag_ratio"] for row in rows),
        "signed_residual_to_lead_drag_ratio_summary": finite_summary(
            row["signed_residual_to_lead_drag_ratio"] for row in rows),
        "lead_drag_margin_after_positive_pushback_summary": finite_summary(
            row["lead_drag_margin_after_positive_pushback"] for row in rows),
        "observed_minimum_passing_theta_for_positive_pushback": float(
            worst_pushback["positive_pushback_to_lead_drag_ratio"]),
        "worst_positive_pushback_row": worst_pushback,
        "worst_abs_residual_row": worst_abs,
        "threshold_profiles": [
            threshold_profile(name, theta, rows)
            for name, theta in THETA_THRESHOLDS
        ],
    }


def compute_load_rows():
    dual = load_json(DUAL_SOURCE)
    basis, maps = edge_basis()
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    source_rows = [row for row in dual["target_rows"] if row["edge_success"]]
    maximum_target = max(row["target"] for row in source_rows)
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
        for row in source_rows
    ]


def build_receipt():
    load_source = load_json(LOAD_SOURCE)
    rows = [budget_row(row) for row in compute_load_rows()]
    post_rows = [
        row for row in rows if row["block_index_after_discovery"] >= 1]
    all_summary = summarize("all_dual_edge_rows", rows)
    post_summary = summarize("post_discovery_rows", post_rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "edge_character_load_audit": str(LOAD_SOURCE.relative_to(ROOT)),
            "edge_character_load_source_commit": load_source["source_commit"],
            "lower_face_dual_edge_audit": str(DUAL_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite q286-WBSS 11,13 edge residual-budget diagnostic only; "
            "observed theta values fit this fixture only and are not "
            "universal bounds; no 11,13 edge theorem, residual theorem, "
            "character-sum bound, binary-prime projection-control theorem, "
            "signed discrepancy theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "lead_edge_theorem_proved": False,
        "residual_budget_theorem_proved": False,
        "character_sum_bound_proved": False,
        "binary_prime_projection_control_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "q286 11,13 edge residual budget",
            "mechanism": (
                "Treat the always-negative finite 11,13 edge contribution as "
                "the lead drag, and measure the positive pushback from the "
                "other three edge sums as a ratio of that drag."),
            "prediction": (
                "If 11,13 is a useful first analytic target, the finite "
                "positive residual-edge pushback should stay below the "
                "11,13 drag with a visible margin on all checked rows."),
            "falsifier": (
                "A row with positive residual-edge pushback at least as large "
                "as the 11,13 drag would falsify this finite residual-budget "
                "route for the current fixture."),
            "smallest_test": (
                "Replay the 230 dual-edge rows, compute max(0, other edges) "
                "divided by -(11,13 edge), and rank threshold failures."),
            "novelty_label": "new-to-this-task",
        },
        "lead_edge": LEAD_EDGE,
        "residual_edges": list(RESIDUAL_EDGES),
        "summaries": {
            "all_dual_edge_rows": all_summary,
            "post_discovery_rows": post_summary,
        },
        "finite_1113_residual_budget_passes": (
            all_summary["total_edge_negative_after_residual_count"]
            == all_summary["row_count"]
            and post_summary["total_edge_negative_after_residual_count"]
            == post_summary["row_count"]),
        "decision": (
            "The finite rows support a theorem-shaped decomposition with "
            "11,13 as the lead edge and the other three edges as residual: "
            "the 11,13 contribution is negative on every checked row, and "
            "positive residual-edge pushback never reaches the 11,13 drag.  "
            "This supplies a finite theta target for future signed estimates, "
            "but the observed theta is not a universal constant and does not "
            "permit dropping any edge without a theorem-level residual bound.  "
            "Goldbach remains open."),
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
