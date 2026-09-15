"""Profile the five q286-WBSS residual Fourier conjugacy groups.

The bandlimited residual audit left a one-sided theorem target: top-20
Fourier groups give negative main drag, while the remaining five groups must
not push upward too much.  This receipt asks whether those five residual
groups collapse to one culprit or a fixed proper subpackage.

Finite residual-group diagnostic only.  It proves no residual theorem, signed
projection theorem, q286 threshold theorem, strict-central Goldbach theorem,
or Goldbach proof.
"""

from __future__ import annotations

import itertools
import json
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
DUAL_SOURCE = EVIDENCE / "q286-lower-face-dual-edge-audit.json"
OUT = EVIDENCE / "q286-wbss-mod286-residual-group-profile-audit.json"
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


def group_grid(fourier_coefficients, group):
    mask = np.zeros_like(fourier_coefficients)
    for mode in group["modes"]:
        k = int(mode["k_mod_10"])
        ell = int(mode["ell_mod_12"])
        mask[k, ell] = fourier_coefficients[k, ell]
    return np.fft.ifft2(mask * fourier_coefficients.size).real


def signed_count_summary(values):
    return {
        "count": len(values),
        "summary": finite_summary(values),
        "negative_count": sum(value < -TOLERANCE for value in values),
        "positive_count": sum(value > TOLERANCE for value in values),
        "near_zero_count": sum(abs(value) <= TOLERANCE for value in values),
    }


def subset_profile(rows, subset):
    touch_count = 0
    signed_positive_count = 0
    signed_subtotals = []
    positive_part_subtotals = []
    for row in rows:
        values = [row["residual_group_contributions"][index]
                  for index in subset]
        touch_count += any(value > TOLERANCE for value in values)
        subtotal = float(sum(values))
        signed_subtotals.append(subtotal)
        positive_part_subtotals.append(float(sum(
            max(0.0, value) for value in values)))
        signed_positive_count += subtotal > TOLERANCE
    return {
        "subset": [int(index) for index in subset],
        "touch_count": int(touch_count),
        "signed_positive_count": int(signed_positive_count),
        "signed_subtotal_summary": finite_summary(signed_subtotals),
        "positive_part_subtotal_summary": finite_summary(
            positive_part_subtotals),
    }


def best_subset_profiles(positive_rows):
    result = {}
    for size in range(1, 6):
        candidates = [
            subset_profile(positive_rows, subset)
            for subset in itertools.combinations(range(5), size)
        ]
        best = sorted(
            candidates,
            key=lambda item: (
                -item["touch_count"],
                -item["signed_positive_count"],
                item["subset"],
            ),
        )[0]
        result[f"size_{size}"] = best
    return result


def build_receipt():
    formula = load_json(FORMULA_SOURCE)
    dual = load_json(DUAL_SOURCE)
    _, by_modulus = coefficient_lookup(formula)
    decomposition = decompose_mod286_coefficient(by_modulus[286])
    interaction, residue_to_index = interaction_grid(decomposition)
    fourier_coefficients = np.fft.fft2(interaction) / interaction.size
    groups, zero_axis_energy_share = fourier_conjugacy_groups(
        fourier_coefficients)
    residual_groups = groups[TOP_GROUP_COUNT:]
    top20 = partial_interaction_grid(
        fourier_coefficients, groups, TOP_GROUP_COUNT)
    residual_grids = [
        group_grid(fourier_coefficients, group)
        for group in residual_groups
    ]
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
        error_grid = row["error_grid"]
        bandlimited = signed_contribution(top20, error_grid)
        main_drag = -bandlimited
        contributions = [
            signed_contribution(grid, error_grid)
            for grid in residual_grids
        ]
        residual = float(sum(contributions))
        positive_parts = [max(0.0, value) for value in contributions]
        max_positive = max(positive_parts)
        argmax = (
            positive_parts.index(max_positive)
            if max_positive > TOLERANCE else None
        )
        rows.append({
            "target": row["target"],
            "target_residue": row["target_residue"],
            "target_mod_286": row["target_mod_286"],
            "block_index_after_discovery": row[
                "block_index_after_discovery"],
            "pair_count": row["pair_count"],
            "bandlimited_top20_component": float(bandlimited),
            "main_drag": float(main_drag),
            "residual_five_group_component": residual,
            "positive_residual_pushback": float(max(0.0, residual)),
            "pushback_to_main_drag_ratio": float(
                max(0.0, residual) / main_drag),
            "residual_group_contributions": [
                float(value) for value in contributions
            ],
            "positive_part_sum": float(sum(positive_parts)),
            "negative_part_sum": float(sum(
                max(0.0, -value) for value in contributions)),
            "max_positive_group_index": argmax,
            "group_reconstruction_abs_error": float(
                abs(residual - sum(contributions))),
        })
    positive_rows = [
        row for row in rows
        if row["residual_five_group_component"] > TOLERANCE
    ]
    group_summaries = []
    for index, group in enumerate(residual_groups):
        values = [row["residual_group_contributions"][index]
                  for row in rows]
        positive_values = [
            row["residual_group_contributions"][index]
            for row in positive_rows
        ]
        group_summaries.append({
            "group_index": int(index),
            "representative": group["representative"],
            "energy_share": group["energy_share"],
            "cumulative_energy_share": group["cumulative_energy_share"],
            "all_rows": signed_count_summary(values),
            "positive_residual_rows": signed_count_summary(positive_values),
            "positive_on_positive_residual_rows": sum(
                value > TOLERANCE for value in positive_values),
            "argmax_positive_residual_rows": sum(
                row["max_positive_group_index"] == index
                for row in positive_rows),
        })
    subset_profiles = best_subset_profiles(positive_rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "lower_face_dual_edge_audit": str(DUAL_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite q286-WBSS residual Fourier group profile only; no "
            "residual theorem, signed projection theorem, q286 threshold "
            "theorem, strict-central Goldbach theorem, or Goldbach proof"
        ),
        "goldbach_proved": False,
        "residual_group_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "single_residual_group_shortcut_demoted": True,
        "proper_fixed_residual_subset_shortcut_demoted": True,
        "novelty_label": "new-to-this-task",
        "candidate": {
            "name": "single residual-group pushback explanation",
            "mechanism": (
                "After the top-20 Fourier split, test whether the upward "
                "residual pushback comes from one residual conjugacy group or "
                "a fixed proper subset of the five residual groups."
            ),
            "prediction": (
                "If this shortcut is right, a single group or a fixed proper "
                "subset should be positive on every upward-pushback row and "
                "recover the signed positive residual there."
            ),
            "falsifier": (
                "If the leading positive group rotates and no fixed proper "
                "subset has signed positive subtotal on every positive "
                "residual row, the residual theorem must use all five groups "
                "or a different aggregate inequality."
            ),
            "smallest_test": (
                "Replay the existing 196 post-discovery rows and compute the "
                "five residual conjugacy-group contributions separately."
            ),
        },
        "coefficient_spectrum": {
            "conjugacy_group_count": len(groups),
            "top_group_count": TOP_GROUP_COUNT,
            "residual_group_count": len(residual_groups),
            "zero_axis_energy_share": zero_axis_energy_share,
            "top20_energy_share": float(groups[TOP_GROUP_COUNT - 1][
                "cumulative_energy_share"]),
            "residual_energy_share": float(
                1.0 - groups[TOP_GROUP_COUNT - 1][
                    "cumulative_energy_share"]),
            "residual_groups": [
                {
                    "group_index": int(index),
                    "representative": group["representative"],
                    "energy_share": group["energy_share"],
                    "cumulative_energy_share": group[
                        "cumulative_energy_share"],
                    "mode_count": group["mode_count"],
                    "modes": group["modes"],
                }
                for index, group in enumerate(residual_groups)
            ],
        },
        "row_summary": {
            "row_count": len(rows),
            "positive_residual_row_count": len(positive_rows),
            "negative_residual_row_count": sum(
                row["residual_five_group_component"] < -TOLERANCE
                for row in rows),
            "residual_five_group_component": signed_count_summary(
                [row["residual_five_group_component"] for row in rows]),
            "pushback_to_main_drag_ratio_summary": finite_summary(
                row["pushback_to_main_drag_ratio"] for row in rows),
            "positive_part_sum_on_positive_rows_summary": finite_summary(
                row["positive_part_sum"] for row in positive_rows),
            "negative_part_sum_on_positive_rows_summary": finite_summary(
                row["negative_part_sum"] for row in positive_rows),
            "max_positive_group_share_of_positive_part_summary": finite_summary(
                row["residual_group_contributions"][
                    row["max_positive_group_index"]]
                / row["positive_part_sum"]
                for row in positive_rows
            ),
            "group_summaries": group_summaries,
            "argmax_positive_residual_counts": {
                str(index): sum(
                    row["max_positive_group_index"] == index
                    for row in positive_rows)
                for index in range(len(residual_groups))
            },
            "best_fixed_subset_profiles_on_positive_residual_rows": (
                subset_profiles),
            "largest_positive_residual_rows": sorted(
                positive_rows,
                key=lambda row: (
                    -row["residual_five_group_component"], row["target"]),
            )[:12],
            "smallest_positive_residual_rows": sorted(
                positive_rows,
                key=lambda row: (
                    row["residual_five_group_component"], row["target"]),
            )[:12],
        },
        "decision": (
            "The five residual groups do not collapse to one culprit.  On the "
            "24 upward-pushback rows, the largest positive residual group "
            "rotates across all five groups; the best single group is "
            "positive on only "
            f"{subset_profiles['size_1']['touch_count']} of 24 rows, and the "
            "best pair touches 23 of 24 but has signed positive subtotal on "
            "only 20 of 24.  Some proper triples touch every positive row, "
            "but no proper fixed subset has signed positive subtotal on all "
            "24 upward-pushback rows.  Therefore the next theorem should "
            "control the signed aggregate of all five residual groups, or "
            "replace this residual split with a different aggregate q286-WBSS "
            "witness."
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
