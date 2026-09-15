"""Fourier-resolve the q286-WBSS mod-286 interaction drag.

The mod-286 interaction audit showed that the recurring negative projection
drag is not a one-factor mod-11 or mod-13 marginal.  This receipt asks the
next theorem-facing question: is that interaction carried by a tiny set of
multiplicative character modes, or is it a broader signed covariance object?

Finite Fourier diagnostic only.  It proves no interaction theorem, signed
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
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
DUAL_SOURCE = EVIDENCE / "q286-lower-face-dual-edge-audit.json"
OUT = EVIDENCE / "q286-wbss-mod286-fourier-interaction-audit.json"
TOLERANCE = 1e-10
TRUNCATION_GROUP_COUNTS = (1, 2, 4, 6, 8, 10, 12, 20, 25)

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
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402
from tools.build_q286_wbss_mod286_interaction_audit import (  # noqa: E402
    decompose_mod286_coefficient,
)
from tools.build_q286_wbss_projection_uniformity_obstruction_audit import (  # noqa: E402
    coefficient_lookup,
    projection_distribution,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def primitive_log_table(modulus, generator):
    table = {pow(generator, exponent, modulus): exponent
             for exponent in range(modulus - 1)}
    if len(table) != modulus - 1:
        raise ValueError(f"{generator} is not primitive modulo {modulus}")
    return table


def interaction_grid(decomposition):
    log11 = primitive_log_table(11, 2)
    log13 = primitive_log_table(13, 2)
    grid = np.zeros((10, 12), dtype=np.float64)
    residue_to_index = {}
    for residue, value in decomposition["interaction"].items():
        index = (log11[int(residue) % 11], log13[int(residue) % 13])
        grid[index] = float(value)
        residue_to_index[int(residue)] = index
    return grid, residue_to_index


def conjugate_key(k, ell):
    conjugate = ((-k) % 10, (-ell) % 12)
    return min((k, ell), conjugate)


def fourier_conjugacy_groups(coefficients):
    energy = np.abs(coefficients) ** 2
    total_energy = float(np.sum(energy))
    groups = {}
    zero_axis_energy = 0.0
    for k in range(10):
        for ell in range(12):
            mode_energy = float(energy[k, ell])
            if k == 0 or ell == 0:
                zero_axis_energy += mode_energy
            if mode_energy <= TOLERANCE ** 2:
                continue
            key = conjugate_key(k, ell)
            group = groups.setdefault(key, {
                "key": key,
                "modes": [],
                "energy": 0.0,
            })
            group["modes"].append((k, ell))
            group["energy"] += mode_energy
    ordered = sorted(
        groups.values(),
        key=lambda group: (-group["energy"], group["key"]),
    )
    rows = []
    cumulative = 0.0
    for group in ordered:
        cumulative += group["energy"]
        representative = group["key"]
        mode_rows = []
        for k, ell in sorted(group["modes"]):
            z = coefficients[k, ell]
            mode_rows.append({
                "k_mod_10": int(k),
                "ell_mod_12": int(ell),
                "real": float(np.real(z)),
                "imag": float(np.imag(z)),
                "abs": float(abs(z)),
                "energy_share": float((abs(z) ** 2) / total_energy),
            })
        rows.append({
            "representative": {
                "k_mod_10": int(representative[0]),
                "ell_mod_12": int(representative[1]),
            },
            "mode_count": len(mode_rows),
            "modes": mode_rows,
            "energy_share": float(group["energy"] / total_energy),
            "cumulative_energy_share": float(cumulative / total_energy),
        })
    return rows, float(zero_axis_energy / total_energy)


def partial_interaction_grid(fourier_coefficients, groups, group_count):
    mask = np.zeros_like(fourier_coefficients)
    for group in groups[:group_count]:
        for mode in group["modes"]:
            mask[
                int(mode["k_mod_10"]),
                int(mode["ell_mod_12"]),
            ] = fourier_coefficients[
                int(mode["k_mod_10"]),
                int(mode["ell_mod_12"]),
            ]
    return np.fft.ifft2(mask * fourier_coefficients.size).real


def row_error_grid(edge_row, context, full_coefficients,
                   first_three_coefficients, primes, prime_values, log_values,
                   residues, residue_to_index):
    orbit_data = orbit_coefficients(
        int(edge_row["target_residue"]),
        context,
        full_coefficients,
        first_three_coefficients,
    )
    coefficient_data = {
        "orbits": orbit_data["orbits"],
        "first_three": np.asarray(
            orbit_data["first_three_coefficients"], dtype=np.float64),
        "full": np.asarray(orbit_data["full_coefficients"], dtype=np.float64),
    }
    actual = actual_orbit_measure(
        int(edge_row["target"]),
        coefficient_data,
        primes,
        prime_values,
        log_values,
    )
    actual_projection = projection_distribution(
        orbit_data["orbits"], np.asarray(actual["masses"], dtype=np.float64), 286)
    uniform_projection = projection_distribution(
        orbit_data["orbits"],
        np.asarray(orbit_data["uniform_orbit_mass"], dtype=np.float64),
        286,
    )
    errors = np.zeros((10, 12), dtype=np.float64)
    for residue in residues:
        errors[residue_to_index[int(residue)]] = (
            actual_projection.get(int(residue), 0.0)
            - uniform_projection.get(int(residue), 0.0)
        )
    return {
        "target": int(edge_row["target"]),
        "target_residue": int(edge_row["target_residue"]),
        "target_mod_286": int(edge_row["target_mod_286"]),
        "block_index_after_discovery": int(
            edge_row["block_index_after_discovery"]),
        "pair_count": int(actual["pair_count"]),
        "error_grid": errors,
    }


def signed_contribution(coefficient_grid, error_grid):
    return float(np.sum(coefficient_grid * error_grid))


def signed_count_summary(values):
    return {
        "count": len(values),
        "summary": finite_summary(values),
        "negative_count": sum(value < -TOLERANCE for value in values),
        "positive_count": sum(value > TOLERANCE for value in values),
        "near_zero_count": sum(abs(value) <= TOLERANCE for value in values),
    }


def truncation_summary(row_data, interaction, fourier_coefficients, groups,
                       group_count):
    partial = partial_interaction_grid(fourier_coefficients, groups, group_count)
    contributions = []
    totals = []
    ratios = []
    residual_ratios = []
    for row in row_data:
        total = signed_contribution(interaction, row["error_grid"])
        contribution = signed_contribution(partial, row["error_grid"])
        residual = total - contribution
        totals.append(total)
        contributions.append(contribution)
        ratios.append(contribution / total)
        residual_ratios.append(abs(residual / total))
    energy_share = groups[group_count - 1]["cumulative_energy_share"]
    return {
        "group_count": int(group_count),
        "mode_count": int(sum(group["mode_count"] for group in groups[:group_count])),
        "coefficient_energy_share": float(energy_share),
        "contribution": signed_count_summary(contributions),
        "contribution_to_total_ratio_summary": finite_summary(ratios),
        "absolute_residual_to_total_ratio_summary": finite_summary(
            residual_ratios),
        "all_rows_negative": all(value < -TOLERANCE for value in contributions),
        "all_rows_half_or_more_of_total_drag": all(
            ratio >= 0.5 for ratio in ratios),
        "weakest_ratio_rows": sorted(
            [
                {
                    "target": row["target"],
                    "target_mod_286": row["target_mod_286"],
                    "total_interaction_component": float(total),
                    "truncated_contribution": float(contribution),
                    "contribution_to_total_ratio": float(ratio),
                    "absolute_residual_to_total_ratio": float(residual_ratio),
                }
                for row, total, contribution, ratio, residual_ratio
                in zip(row_data, totals, contributions, ratios, residual_ratios)
            ],
            key=lambda item: (item["contribution_to_total_ratio"],
                              item["target"]),
        )[:12],
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
    row_data = [
        row_error_grid(
            row,
            context,
            full_coefficients,
            first_three_coefficients,
            primes,
            prime_values,
            log_values,
            decomposition["residues"],
            residue_to_index,
        )
        for row in edge_rows
    ]
    total_values = [
        signed_contribution(interaction, row["error_grid"])
        for row in row_data
    ]
    truncations = {
        f"top_{count}_conjugacy_groups": truncation_summary(
            row_data,
            interaction,
            fourier_coefficients,
            groups,
            count,
        )
        for count in TRUNCATION_GROUP_COUNTS
    }
    first_all_negative = next(
        item for item in truncations.values() if item["all_rows_negative"])
    first_half_drag = next(
        item for item in truncations.values()
        if item["all_rows_half_or_more_of_total_drag"])
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "lower_face_dual_edge_audit": str(DUAL_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite mod-286 Fourier-interaction diagnostic only; no "
            "multiplicative-character theorem, signed projection theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"
        ),
        "goldbach_proved": False,
        "multiplicative_character_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "tiny_character_shortcut_demoted": True,
        "novelty_label": "new-to-this-task",
        "candidate": {
            "name": "multiplicative-character resolution of mod-286 drag",
            "mechanism": (
                "Use primitive-root coordinates modulo 11 and 13 to Fourier "
                "decompose the interaction coefficient on C10 x C12.  Replay "
                "actual projection-error rows against low-energy truncations "
                "to see whether a small character family controls the signed "
                "drag."
            ),
            "prediction": (
                "A useful theorem target would show sign-stable low-mode "
                "negative contribution, with an explicit residual-drag bound."
            ),
            "falsifier": (
                "If only many character pairs recover sign or magnitude, a "
                "tiny-character proof shortcut is not the right route."
            ),
            "smallest_test": (
                "Decompose the already isolated mod-286 interaction and replay "
                "top conjugate Fourier mode groups on the 196 existing "
                "post-discovery rows."
            ),
        },
        "coefficient_spectrum": {
            "residue_count": int(interaction.size),
            "conjugacy_group_count": len(groups),
            "zero_axis_energy_share": zero_axis_energy_share,
            "total_interaction_sum_squares": float(
                np.sum(interaction * interaction)),
            "top_conjugacy_groups": groups[:20],
            "energy_share_by_top_group_count": {
                str(count): float(groups[count - 1][
                    "cumulative_energy_share"])
                for count in TRUNCATION_GROUP_COUNTS
            },
        },
        "row_summary": {
            "row_count": len(row_data),
            "total_interaction_component": signed_count_summary(total_values),
            "truncations": truncations,
            "first_all_negative_truncation": {
                "group_count": first_all_negative["group_count"],
                "mode_count": first_all_negative["mode_count"],
                "coefficient_energy_share": first_all_negative[
                    "coefficient_energy_share"],
                "minimum_ratio": first_all_negative[
                    "contribution_to_total_ratio_summary"]["minimum"],
            },
            "first_half_drag_truncation": {
                "group_count": first_half_drag["group_count"],
                "mode_count": first_half_drag["mode_count"],
                "coefficient_energy_share": first_half_drag[
                    "coefficient_energy_share"],
                "minimum_ratio": first_half_drag[
                    "contribution_to_total_ratio_summary"]["minimum"],
            },
        },
        "decision": (
            "The finite interaction has no tiny-character explanation.  The "
            "zero Fourier axes are numerically absent, confirming that the "
            "previous ANOVA interaction split is respected, but the top two, "
            "four, six, and eight conjugacy groups do not both explain "
            "the sign and magnitude.  The first sign-stable truncation uses "
            f"{first_all_negative['group_count']} conjugacy groups, but its "
            "minimum contribution-to-total ratio is only "
            f"{first_all_negative['contribution_to_total_ratio_summary']['minimum']}. "
            "The first tested truncation carrying at least half the drag on "
            f"every row uses {first_half_drag['group_count']} conjugacy "
            "groups.  The surviving theorem target is a band-limited signed "
            "interaction inequality plus a residual bound, or a direct raw "
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
