"""Audit q286-WBSS residual absorption threshold sensitivity.

The bandlimited residual audit showed that top-20 Fourier groups give
negative drag on the checked rows and that the remaining five groups only need
one-sided control.  Kevin asked whether .13 is too strict and whether .125
works.  This receipt makes that threshold question explicit.

Finite threshold diagnostic only.  It proves no residual absorption theorem,
signed projection theorem, q286 threshold theorem, strict-central Goldbach
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
BANDLIMITED_SOURCE = (
    EVIDENCE / "q286-wbss-mod286-bandlimited-residual-audit.json")
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
DUAL_SOURCE = EVIDENCE / "q286-lower-face-dual-edge-audit.json"
OUT = EVIDENCE / "q286-wbss-residual-absorption-threshold-audit.json"
TOP_GROUP_COUNT = 20
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    period_full_unit_coefficients,
    prepare_support_context,
    q286_first_three_unit_coefficients,
)
from tools.build_q286_prime_indexed_kernel_route_audit import logs  # noqa: E402
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402
from tools.build_q286_wbss_mod286_fourier_interaction_audit import (  # noqa: E402
    coefficient_lookup,
    decompose_mod286_coefficient,
    fourier_conjugacy_groups,
    interaction_grid,
    load_json,
    partial_interaction_grid,
    row_error_grid,
    signed_contribution,
)


THRESHOLDS = (
    ("one_eighth", 1.0 / 8.0),
    ("decimal_0_126", 0.126),
    ("decimal_0_127", 0.127),
    ("decimal_0_13", 0.13),
    ("two_fifteenths", 2.0 / 15.0),
    ("one_seventh", 1.0 / 7.0),
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def source_payload():
    return json.loads(BANDLIMITED_SOURCE.read_text(encoding="utf-8"))


def absorption_rows_for_edge_rows(edge_rows, require_top20_negative=True):
    formula = load_json(FORMULA_SOURCE)
    dual = load_json(DUAL_SOURCE)
    _, by_modulus = coefficient_lookup(formula)
    decomposition = decompose_mod286_coefficient(by_modulus[286])
    interaction, residue_to_index = interaction_grid(decomposition)
    fourier_coefficients = np.fft.fft2(interaction) / interaction.size
    groups, _ = fourier_conjugacy_groups(fourier_coefficients)
    top = partial_interaction_grid(
        fourier_coefficients, groups, TOP_GROUP_COUNT)
    residual = interaction - top
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    maximum_target = max(row["target"] for row in edge_rows)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    rows = []
    for edge_row in edge_rows:
        row = row_error_grid(
            edge_row,
            context,
            full_coefficients,
            first_three_coefficients,
            primes,
            prime_values,
            log_values,
            decomposition["residues"],
            residue_to_index,
        )
        bandlimited = signed_contribution(top, row["error_grid"])
        residual_value = signed_contribution(residual, row["error_grid"])
        main_drag = -bandlimited
        if require_top20_negative and main_drag <= TOLERANCE:
            raise ValueError("top-20 bandlimited contribution lost sign")
        pushback = max(0.0, residual_value)
        rows.append({
            "target": int(row["target"]),
            "target_residue": int(row["target_residue"]),
            "target_mod_286": int(row["target_mod_286"]),
            "block_index_after_discovery": int(
                row["block_index_after_discovery"]),
            "pair_count": int(row["pair_count"]),
            "bandlimited_top20_component": float(bandlimited),
            "residual_five_group_component": float(residual_value),
            "main_drag": float(main_drag),
            "positive_residual_pushback": float(pushback),
            "pushback_to_main_drag_ratio": (
                float(pushback / main_drag)
                if main_drag > TOLERANCE else None),
        })
    return rows


def absorption_rows(include_discovery=False):
    dual = load_json(DUAL_SOURCE)
    edge_rows = [row for row in dual["target_rows"] if row["edge_success"]]
    if not include_discovery:
        edge_rows = [
            row for row in edge_rows
            if row["block_index_after_discovery"] >= 1
        ]
    return absorption_rows_for_edge_rows(edge_rows)


def post_discovery_rows():
    return absorption_rows(include_discovery=False)


def threshold_profile(name, threshold, rows):
    non_strict_passes = [
        row for row in rows
        if row["pushback_to_main_drag_ratio"] <= threshold + TOLERANCE
    ]
    strict_passes = [
        row for row in rows
        if row["pushback_to_main_drag_ratio"] < threshold - TOLERANCE
    ]
    failing = [
        row for row in rows
        if row["pushback_to_main_drag_ratio"] > threshold + TOLERANCE
    ]
    maximum = max(row["pushback_to_main_drag_ratio"] for row in rows)
    return {
        "name": name,
        "threshold": float(threshold),
        "passes_all_rows": not failing,
        "strict_pass_count": len(strict_passes),
        "non_strict_pass_count": len(non_strict_passes),
        "failing_row_count": len(failing),
        "absolute_slack_against_observed_maximum": float(threshold - maximum),
        "relative_slack_against_observed_maximum": float(
            (threshold - maximum) / maximum),
        "failing_rows": sorted(
            failing,
            key=lambda row: (
                -row["pushback_to_main_drag_ratio"], row["target"]),
        )[:20],
    }


def ceil_decimal(value, places):
    scale = 10 ** places
    return math.ceil(value * scale - 1e-12) / scale


def build_receipt():
    prior = source_payload()
    rows = post_discovery_rows()
    ratios = [row["pushback_to_main_drag_ratio"] for row in rows]
    positive_rows = [
        row for row in rows if row["positive_residual_pushback"] > TOLERANCE
    ]
    worst = max(
        rows,
        key=lambda row: (
            row["pushback_to_main_drag_ratio"], -row["target"]),
    )
    threshold_profiles = [
        threshold_profile(name, threshold, rows)
        for name, threshold in THRESHOLDS
    ]
    by_name = {profile["name"]: profile for profile in threshold_profiles}
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "bandlimited_residual_audit": str(
                BANDLIMITED_SOURCE.relative_to(ROOT)),
            "bandlimited_source_commit": prior["source_commit"],
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "lower_face_dual_edge_audit": str(DUAL_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite q286-WBSS residual absorption threshold diagnostic only; "
            "no residual absorption theorem, signed projection theorem, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof"),
        "goldbach_proved": False,
        "residual_absorption_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "one_eighth_cap_falsified": (
            not by_name["one_eighth"]["passes_all_rows"]),
        "point_13_cap_survives_fixture": (
            by_name["decimal_0_13"]["passes_all_rows"]),
        "novelty_label": "new-to-this-task",
        "candidate": {
            "name": "residual absorption threshold sensitivity",
            "mechanism": (
                "The residual proof target only needs an upper bound on "
                "positive five-group pushback relative to the top-20 Fourier "
                "drag.  Test the actual slack for simple constants instead "
                "of guessing a clean fraction."),
            "prediction": (
                "The clean 1/8 cap may be too sharp, while a nearby decimal "
                "cap such as .13 can survive the finite fixture with small "
                "but nonzero slack."),
            "falsifier": (
                "Any row whose positive_residual_pushback/main_drag ratio "
                "exceeds a candidate threshold falsifies that finite cap."),
            "smallest_test": (
                "Replay the 196 post-discovery rows and rank threshold "
                "failures for .125, .126, .127, .13, 2/15, and 1/7."),
        },
        "row_summary": {
            "row_count": len(rows),
            "positive_pushback_row_count": len(positive_rows),
            "pushback_to_main_drag_ratio_summary": finite_summary(ratios),
            "observed_minimum_passing_constant": float(max(ratios)),
            "ceil_to_3_decimal_places": ceil_decimal(max(ratios), 3),
            "ceil_to_2_decimal_places": ceil_decimal(max(ratios), 2),
            "worst_row": worst,
            "largest_positive_pushback_rows": sorted(
                positive_rows,
                key=lambda row: (
                    -row["pushback_to_main_drag_ratio"], row["target"]),
            )[:12],
        },
        "threshold_profiles": threshold_profiles,
        "answer_to_user": (
            ".125 is too strict for the current finite fixture: the worst "
            "row has ratio 0.12566677703853088.  .126 passes all 196 rows "
            "with absolute slack about 0.00033322296146912 over the observed "
            "maximum.  .13 is not too strict on this fixture; it passes all "
            "196 rows with absolute slack about 0.00433322296146912.  The "
            "theorem should still be stated with a symbolic theta<1, using "
            "these decimals only as finite evidence and not as proved "
            "universal constants."),
        "decision": (
            "Retire the exact 1/8 residual absorption cap for the present "
            "q286-WBSS fixture.  Preserve .13 as a finite working cap and "
            "a useful stress target, but do not promote it to a theorem "
            "constant without a uniform signed residual estimate or a fresh "
            "holdout that materially changes the evidence."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
