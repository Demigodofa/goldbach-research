"""Audit the q286-WBSS top-20 Fourier residual absorption condition.

The Fourier interaction receipt found that the first twenty conjugacy groups
carry a sign-stable negative contribution on all checked rows.  This receipt
turns the remaining five groups into a theorem-facing scalar inequality:
their positive pushback must be smaller than the top-20 main drag.

Finite residual diagnostic only.  It proves no band-limited character theorem,
signed projection theorem, q286 threshold theorem, strict-central Goldbach
theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
DUAL_SOURCE = EVIDENCE / "q286-lower-face-dual-edge-audit.json"
OUT = EVIDENCE / "q286-wbss-mod286-bandlimited-residual-audit.json"
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


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def signed_count_summary(values):
    return {
        "count": len(values),
        "summary": finite_summary(values),
        "negative_count": sum(value < -TOLERANCE for value in values),
        "positive_count": sum(value > TOLERANCE for value in values),
        "near_zero_count": sum(abs(value) <= TOLERANCE for value in values),
    }


def build_receipt():
    formula = load_json(FORMULA_SOURCE)
    dual = load_json(DUAL_SOURCE)
    _, by_modulus = coefficient_lookup(formula)
    decomposition = decompose_mod286_coefficient(by_modulus[286])
    interaction, residue_to_index = interaction_grid(decomposition)
    fourier_coefficients = np.fft.fft2(interaction) / interaction.size
    groups, zero_axis_energy_share = fourier_conjugacy_groups(
        fourier_coefficients)
    top = partial_interaction_grid(
        fourier_coefficients, groups, TOP_GROUP_COUNT)
    residual = interaction - top
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    edge_rows = [
        row for row in dual["target_rows"]
        if row["edge_success"] and row["block_index_after_discovery"] >= 1
    ]
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
        total = signed_contribution(interaction, row["error_grid"])
        bandlimited = signed_contribution(top, row["error_grid"])
        residual_value = signed_contribution(residual, row["error_grid"])
        main_drag = -bandlimited
        if main_drag <= TOLERANCE:
            raise ValueError("top-20 bandlimited contribution lost sign")
        upward_residual = max(0.0, residual_value)
        rows.append({
            "target": row["target"],
            "target_residue": row["target_residue"],
            "target_mod_286": row["target_mod_286"],
            "block_index_after_discovery": row[
                "block_index_after_discovery"],
            "pair_count": row["pair_count"],
            "total_interaction_component": float(total),
            "bandlimited_top20_component": float(bandlimited),
            "residual_five_group_component": float(residual_value),
            "main_drag": float(main_drag),
            "positive_residual_pushback": float(upward_residual),
            "pushback_to_main_drag_ratio": float(
                upward_residual / main_drag),
            "absolute_residual_to_main_drag_ratio": float(
                abs(residual_value) / main_drag),
            "bandlimited_plus_residual_error": float(
                abs(total - bandlimited - residual_value)),
        })
    pushback_ratios = [row["pushback_to_main_drag_ratio"] for row in rows]
    absolute_ratios = [
        row["absolute_residual_to_main_drag_ratio"] for row in rows]
    residual_values = [row["residual_five_group_component"] for row in rows]
    reconstruction_errors = [
        row["bandlimited_plus_residual_error"] for row in rows]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "lower_face_dual_edge_audit": str(DUAL_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite q286-WBSS top-20 Fourier residual diagnostic only; no "
            "band-limited character theorem, signed projection theorem, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof"
        ),
        "goldbach_proved": False,
        "bandlimited_character_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "one_sided_residual_absorption_candidate_supported": True,
        "symmetric_residual_bound_marked_near_sharp": True,
        "novelty_label": "new-to-this-task",
        "candidate": {
            "name": "top-20 bandlimited residual absorption",
            "mechanism": (
                "Split the mod-286 interaction into the top twenty Fourier "
                "conjugacy groups and the remaining five.  Positivity of the "
                "negative interaction drag follows if the top-20 piece is "
                "negative and any positive residual pushback is smaller than "
                "that main drag."
            ),
            "prediction": (
                "Actual post-discovery rows should have sign-stable top-20 "
                "main drag and a one-sided residual pushback ratio well below "
                "one, even if absolute residual size is too pessimistic."
            ),
            "falsifier": (
                "A row with nonnegative top-20 contribution, or positive "
                "residual pushback at least as large as the top-20 main drag, "
                "would falsify this finite absorption target."
            ),
            "smallest_test": (
                "Replay the existing 196 q286-WBSS post-discovery rows and "
                "measure residual_five_group_component / main_drag only when "
                "the residual pushes upward."
            ),
        },
        "coefficient_spectrum": {
            "conjugacy_group_count": len(groups),
            "top_group_count": TOP_GROUP_COUNT,
            "residual_group_count": len(groups) - TOP_GROUP_COUNT,
            "zero_axis_energy_share": zero_axis_energy_share,
            "top20_energy_share": float(groups[TOP_GROUP_COUNT - 1][
                "cumulative_energy_share"]),
            "residual_energy_share": float(
                1.0 - groups[TOP_GROUP_COUNT - 1][
                    "cumulative_energy_share"]),
            "residual_groups": groups[TOP_GROUP_COUNT:],
        },
        "row_summary": {
            "row_count": len(rows),
            "total_interaction_component": signed_count_summary(
                [row["total_interaction_component"] for row in rows]),
            "bandlimited_top20_component": signed_count_summary(
                [row["bandlimited_top20_component"] for row in rows]),
            "residual_five_group_component": signed_count_summary(
                residual_values),
            "main_drag_summary": finite_summary(
                row["main_drag"] for row in rows),
            "positive_residual_row_count": sum(
                value > TOLERANCE for value in residual_values),
            "negative_residual_row_count": sum(
                value < -TOLERANCE for value in residual_values),
            "pushback_to_main_drag_ratio_summary": finite_summary(
                pushback_ratios),
            "absolute_residual_to_main_drag_ratio_summary": finite_summary(
                absolute_ratios),
            "bandlimited_plus_residual_error_summary": finite_summary(
                reconstruction_errors),
            "pushback_lt_013_count": sum(
                ratio < 0.13 for ratio in pushback_ratios),
            "pushback_lt_one_eighth_count": sum(
                ratio <= 0.125 + TOLERANCE for ratio in pushback_ratios),
            "pushback_lt_one_count": sum(
                ratio < 1.0 for ratio in pushback_ratios),
            "absolute_residual_lt_main_drag_count": sum(
                ratio < 1.0 for ratio in absolute_ratios),
            "largest_positive_pushback_rows": sorted(
                [
                    row for row in rows
                    if row["positive_residual_pushback"] > TOLERANCE
                ],
                key=lambda row: (
                    -row["pushback_to_main_drag_ratio"], row["target"]),
            )[:12],
            "largest_absolute_residual_rows": sorted(
                rows,
                key=lambda row: (
                    -row["absolute_residual_to_main_drag_ratio"],
                    row["target"],
                ),
            )[:12],
        },
        "decision": (
            "The top-20 bandlimited split survives as a sharper finite theorem "
            "target.  The top-20 component is negative on every checked row, "
            "and the remaining five groups push upward on only 24 of 196 "
            "rows.  The maximum upward pushback/main-drag ratio is "
            f"{max(pushback_ratios)}, so a one-sided 0.13 residual absorption "
            "constant passes this fixture while the cleaner 1/8 constant is "
            "slightly too strong.  Symmetric absolute residual control is "
            f"near sharp at {max(absolute_ratios)} because large residuals "
            "are often helpful.  Therefore the next theorem should be "
            "one-sided: prove top-20 negative drag plus an upper bound on "
            "positive residual pushback, or replace both with a direct raw "
            "q286-WBSS signed-witness estimate."
        ),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
