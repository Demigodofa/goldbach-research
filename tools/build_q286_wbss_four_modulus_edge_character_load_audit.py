"""Replay finite binary-prime rows against q286-WBSS edge characters.

The edge-character audit named the coefficient-side character obligations.
This receipt measures how the existing strict-central binary-prime rows load
those obligations: for each row, project actual-minus-local-uniform mass onto
the four CRT edge components and their conjugate character groups.

This is finite row-load evidence only.  It proves no character-sum bound,
binary-prime projection-control theorem, signed discrepancy theorem, q286
threshold theorem, strict-central Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import itertools
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
CHARACTER_SOURCE = (
    EVIDENCE / "q286-wbss-four-modulus-edge-character-audit.json")
DUAL_SOURCE = EVIDENCE / "q286-lower-face-dual-edge-audit.json"
OUT = EVIDENCE / "q286-wbss-four-modulus-edge-character-load-audit.json"
FACTORS = (5, 7, 11, 13)
EDGE_SUPPORTS = ((5, 7), (5, 13), (7, 11), (11, 13))
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
from tools.build_q286_wbss_four_modulus_edge_character_audit import (  # noqa: E402
    active_component_array,
    exponent_maps,
)
from tools.build_q286_wbss_four_modulus_factor_anova_audit import (  # noqa: E402
    anova_components,
    coefficient_tensor,
    json_ready,
    support_key,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def maps_with_inverse():
    maps = exponent_maps()
    for factor, data in maps.items():
        data["exponent_by_residue"] = {
            int(residue): exponent
            for exponent, residue in enumerate(data["residues_by_exponent"])
        }
    return maps


def conjugate_frequency(frequency, shape):
    return tuple((-item) % size for item, size in zip(frequency, shape))


def conjugate_key(frequency, shape):
    conjugate = conjugate_frequency(frequency, shape)
    return min(tuple(frequency), conjugate)


def character_groups(values):
    coefficients = np.fft.fftn(values) / values.size
    total_energy = float(np.sum(np.abs(coefficients) ** 2))
    groups = {}
    for frequency in itertools.product(
            *(range(size) for size in coefficients.shape)):
        value = complex(coefficients[frequency])
        if abs(value) <= TOLERANCE:
            continue
        if any(item == 0 for item in frequency):
            continue
        key = conjugate_key(frequency, coefficients.shape)
        group = groups.setdefault(key, {
            "key": key,
            "modes": [],
            "energy": 0.0,
        })
        group["modes"].append(frequency)
        group["energy"] += abs(value) ** 2

    ordered = []
    cumulative = 0.0
    for index, group in enumerate(sorted(
            groups.values(), key=lambda item: (-item["energy"], item["key"])),
            1):
        mask = np.zeros_like(coefficients)
        mode_rows = []
        for frequency in sorted(group["modes"]):
            value = complex(coefficients[frequency])
            mask[frequency] = value
            mode_rows.append({
                "frequency": list(frequency),
                "coefficient_real": value.real,
                "coefficient_imag": value.imag,
                "abs_coefficient": abs(value),
                "energy": abs(value) ** 2,
                "energy_share": (
                    abs(value) ** 2 / total_energy
                    if total_energy > TOLERANCE else None),
            })
        grid = np.fft.ifftn(mask * coefficients.size).real
        cumulative += group["energy"]
        ordered.append({
            "group_index": index,
            "representative_frequency": list(group["key"]),
            "mode_count": len(mode_rows),
            "modes": mode_rows,
            "coefficient_energy": group["energy"],
            "coefficient_energy_share": (
                group["energy"] / total_energy
                if total_energy > TOLERANCE else None),
            "cumulative_coefficient_energy_share": (
                cumulative / total_energy if total_energy > TOLERANCE else None),
            "grid": grid,
        })
    return ordered


def support_distribution(orbits, masses, support, maps):
    shape = tuple(factor - 1 for factor in support)
    distribution = np.zeros(shape, dtype=np.float64)
    for orbit, mass in zip(orbits, masses):
        contribution = float(mass) / len(orbit)
        for unit in orbit:
            index = tuple(
                maps[factor]["exponent_by_residue"][int(unit % factor)]
                for factor in support
            )
            distribution[index] += contribution
    return distribution


def coefficient_data_for_row(target_residue, context, full_coefficients,
                             first_three_coefficients):
    orbit_data = orbit_coefficients(
        target_residue,
        context,
        full_coefficients,
        first_three_coefficients,
    )
    return {
        "orbits": orbit_data["orbits"],
        "first_three": np.asarray(
            orbit_data["first_three_coefficients"], dtype=np.float64),
        "full": np.asarray(orbit_data["full_coefficients"], dtype=np.float64),
        "uniform": np.asarray(orbit_data["uniform_orbit_mass"],
                              dtype=np.float64),
    }


def edge_basis():
    tensor, _, _ = coefficient_tensor()
    components = anova_components(tensor)
    maps = maps_with_inverse()
    basis = {}
    for support in EDGE_SUPPORTS:
        values = active_component_array(components[support], support, maps).real
        groups = character_groups(values)
        basis[support_key(support)] = {
            "support": support,
            "values": values,
            "groups": groups,
            "group_count": len(groups),
            "mode_count": sum(group["mode_count"] for group in groups),
            "coefficient_energy": float(np.mean(values * values)),
        }
    return basis, maps


def signed_count_summary(values):
    values = [float(value) for value in values]
    return {
        "count": len(values),
        "summary": finite_summary(values),
        "negative_count": sum(value < -TOLERANCE for value in values),
        "positive_count": sum(value > TOLERANCE for value in values),
        "near_zero_count": sum(abs(value) <= TOLERANCE for value in values),
    }


def build_row(edge_row, context, full_coefficients, first_three_coefficients,
              primes, prime_values, log_values, basis, maps):
    coefficients = coefficient_data_for_row(
        int(edge_row["target_residue"]),
        context,
        full_coefficients,
        first_three_coefficients,
    )
    actual = actual_orbit_measure(
        int(edge_row["target"]),
        coefficients,
        primes,
        prime_values,
        log_values,
    )
    actual_masses = np.asarray(actual["masses"], dtype=np.float64)
    uniform_masses = coefficients["uniform"]
    edge_rows = []
    singleton_edge_sum = 0.0
    for key, edge in basis.items():
        support = edge["support"]
        actual_distribution = support_distribution(
            coefficients["orbits"], actual_masses, support, maps)
        uniform_distribution = support_distribution(
            coefficients["orbits"], uniform_masses, support, maps)
        error = actual_distribution - uniform_distribution
        direct = float(np.sum(edge["values"] * error))
        group_contributions = []
        for group in edge["groups"]:
            contribution = float(np.sum(group["grid"] * error))
            group_contributions.append({
                "group_index": group["group_index"],
                "representative_frequency": group["representative_frequency"],
                "mode_count": group["mode_count"],
                "coefficient_energy_share": (
                    group["coefficient_energy_share"]),
                "signed_contribution": contribution,
                "abs_contribution": abs(contribution),
            })
        group_sum = math.fsum(
            item["signed_contribution"] for item in group_contributions)
        singleton_edge_sum += direct
        edge_rows.append({
            "edge_key": key,
            "support": list(support),
            "signed_contribution": direct,
            "negative_drag": max(0.0, -direct),
            "positive_support": max(0.0, direct),
            "group_reconstruction_error": abs(direct - group_sum),
            "character_group_contributions": group_contributions,
            "largest_abs_group_contributions": sorted(
                group_contributions,
                key=lambda item: (
                    -item["abs_contribution"], item["group_index"]),
            )[:8],
        })
    return {
        "target": int(edge_row["target"]),
        "target_residue": int(edge_row["target_residue"]),
        "target_mod_286": int(edge_row["target_mod_286"]),
        "block_index_after_discovery": int(
            edge_row["block_index_after_discovery"]),
        "pair_count": int(actual["pair_count"]),
        "edge_rows": edge_rows,
        "edge_signed_contribution_sum": float(singleton_edge_sum),
        "edge_negative_drag_sum": float(math.fsum(
            row["negative_drag"] for row in edge_rows)),
        "edge_positive_support_sum": float(math.fsum(
            row["positive_support"] for row in edge_rows)),
        "dominant_abs_edge": max(
            edge_rows,
            key=lambda row: (abs(row["signed_contribution"]), row["edge_key"]),
        )["edge_key"],
        "max_group_reconstruction_error": max(
            row["group_reconstruction_error"] for row in edge_rows),
    }


def summarize_edge_rows(rows):
    by_edge = {}
    for key in (support_key(edge) for edge in EDGE_SUPPORTS):
        values = [
            edge["signed_contribution"]
            for row in rows for edge in row["edge_rows"]
            if edge["edge_key"] == key
        ]
        drags = [
            edge["negative_drag"]
            for row in rows for edge in row["edge_rows"]
            if edge["edge_key"] == key
        ]
        supports = [
            edge["positive_support"]
            for row in rows for edge in row["edge_rows"]
            if edge["edge_key"] == key
        ]
        by_edge[key] = {
            "signed_contribution": signed_count_summary(values),
            "negative_drag_summary": finite_summary(drags),
            "positive_support_summary": finite_summary(supports),
            "total_negative_drag": float(math.fsum(drags)),
            "total_positive_support": float(math.fsum(supports)),
            "total_abs_contribution": float(math.fsum(abs(v) for v in values)),
        }
    dominant_counts = {
        key: sum(row["dominant_abs_edge"] == key for row in rows)
        for key in by_edge
    }
    return {
        "row_count": len(rows),
        "edge_signed_contribution_sum": signed_count_summary(
            row["edge_signed_contribution_sum"] for row in rows),
        "edge_negative_drag_sum_summary": finite_summary(
            row["edge_negative_drag_sum"] for row in rows),
        "edge_positive_support_sum_summary": finite_summary(
            row["edge_positive_support_sum"] for row in rows),
        "dominant_abs_edge_counts": dominant_counts,
        "edge_summaries": by_edge,
        "maximum_group_reconstruction_error": max(
            row["max_group_reconstruction_error"] for row in rows),
        "largest_total_edge_drag_rows": sorted(
            rows,
            key=lambda row: (-row["edge_negative_drag_sum"], row["target"]),
        )[:12],
    }


def flatten_group_contributions(rows):
    totals = {}
    for row in rows:
        for edge in row["edge_rows"]:
            for group in edge["character_group_contributions"]:
                key = (
                    edge["edge_key"],
                    tuple(group["representative_frequency"]),
                )
                item = totals.setdefault(key, {
                    "edge_key": edge["edge_key"],
                    "representative_frequency": (
                        group["representative_frequency"]),
                    "mode_count": group["mode_count"],
                    "coefficient_energy_share": (
                        group["coefficient_energy_share"]),
                    "signed_total": 0.0,
                    "abs_total": 0.0,
                    "negative_count": 0,
                    "positive_count": 0,
                })
                contribution = group["signed_contribution"]
                item["signed_total"] += contribution
                item["abs_total"] += abs(contribution)
                item["negative_count"] += int(contribution < -TOLERANCE)
                item["positive_count"] += int(contribution > TOLERANCE)
    return sorted(
        totals.values(),
        key=lambda item: (-item["abs_total"], item["edge_key"],
                          item["representative_frequency"]),
    )


def summarize_groups(rows):
    groups = flatten_group_contributions(rows)
    total_abs = math.fsum(item["abs_total"] for item in groups)
    cumulative = 0.0
    thresholds = {0.5: None, 0.8: None, 0.9: None}
    ranked = []
    for index, item in enumerate(groups, 1):
        cumulative += item["abs_total"]
        share = item["abs_total"] / total_abs if total_abs > TOLERANCE else 0.0
        cumulative_share = (
            cumulative / total_abs if total_abs > TOLERANCE else 0.0)
        row = {
            **item,
            "rank": index,
            "finite_abs_load_share": share,
            "cumulative_finite_abs_load_share": cumulative_share,
        }
        ranked.append(row)
        for threshold in thresholds:
            if thresholds[threshold] is None and cumulative_share >= threshold:
                thresholds[threshold] = index
    return {
        "group_count_with_recorded_top_load": len(groups),
        "total_abs_group_load": float(total_abs),
        "rank_needed_for_50pct_abs_load": thresholds[0.5],
        "rank_needed_for_80pct_abs_load": thresholds[0.8],
        "rank_needed_for_90pct_abs_load": thresholds[0.9],
        "top_abs_load_groups": ranked[:20],
    }


def build_receipt():
    character_source = load_json(CHARACTER_SOURCE)
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
    rows = [
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
    post_rows = [
        row for row in rows if row["block_index_after_discovery"] >= 1]
    summary_all = summarize_edge_rows(rows)
    summary_post = summarize_edge_rows(post_rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "edge_character_audit": str(CHARACTER_SOURCE.relative_to(ROOT)),
            "edge_character_source_commit": character_source["source_commit"],
            "lower_face_dual_edge_audit": str(DUAL_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite q286-WBSS edge-character row-load diagnostic only; "
            "rankings are fixture prioritization, not universal bounds; "
            "no character-sum bound, binary-prime projection-control theorem, "
            "signed discrepancy theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "character_sum_bound_proved": False,
        "binary_prime_projection_control_theorem_proved": False,
        "signed_discrepancy_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "finite q286 edge-character binary-prime load ranking",
            "mechanism": (
                "Project actual-minus-local-uniform strict-central "
                "binary-prime mass onto each CRT edge and replay the exact "
                "edge-character coefficient groups."),
            "prediction": (
                "The same four edge supports remain necessary, but finite "
                "stress rows may identify a dominant edge or small group "
                "prefix worth attacking first analytically."),
            "falsifier": (
                "A group reconstruction mismatch, a missing edge load, or a "
                "need to invoke three/four-factor components would falsify "
                "this finite translation from coefficient obligations to "
                "binary-prime row loads."),
            "smallest_test": (
                "Replay all 230 available dual-edge rows and summarize the "
                "edge contributions and largest character-group loads."),
            "novelty_label": "new-to-this-task",
        },
        "edge_character_obligation_counts": (
            character_source["summary"]["edge_character_counts"]),
        "edge_basis_summary": {
            key: {
                "group_count": value["group_count"],
                "mode_count": value["mode_count"],
                "coefficient_energy": value["coefficient_energy"],
            }
            for key, value in basis.items()
        },
        "summaries": {
            "all_dual_edge_rows": summary_all,
            "post_discovery_rows": summary_post,
        },
        "finite_group_load_ranking": {
            "all_dual_edge_rows": summarize_groups(rows),
            "post_discovery_rows": summarize_groups(post_rows),
        },
        "edge_translation_verified": (
            summary_all["maximum_group_reconstruction_error"] < 1e-9
            and summary_post["maximum_group_reconstruction_error"] < 1e-9),
        "decision": (
            "The exact edge-character basis replays the finite binary-prime "
            "row loads without reconstruction loss.  This ranks where the "
            "existing data places signed edge stress, but it does not remove "
            "any universal character obligation: omitted groups would still "
            "need a theorem-level bound before they could be discarded.  "
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
