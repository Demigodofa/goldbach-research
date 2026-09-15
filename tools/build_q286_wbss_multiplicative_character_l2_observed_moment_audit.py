"""Observed aggregate character moments versus the q286-WBSS L2 payment cap.

The L2 payment audit found a sharper theorem target:

    sqrt(sum_d ||D_d(N)||_2^2) < LocalMain(N) / ||c_hat||_2.

This receipt tests that target on the existing 348 checked rows.  It is a
finite diagnostic and falsifier for any claim that the aggregate L2 cap already
holds on the checked population.  It is not a proof or disproof of an eventual
sufficiently-large theorem with a higher threshold.
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
L2_PAYMENT_SOURCE = (
    EVIDENCE / "q286-wbss-multiplicative-character-l2-payment-audit.json")
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
OUT = (
    EVIDENCE
    / "q286-wbss-multiplicative-character-l2-observed-moment-audit.json")
TOLERANCE = 1e-12

sys.path.insert(0, str(ROOT))

from tools import build_q286_wbss_four_modulus_variance_scale_far_lift_holdout as far  # noqa: E501,E402
from tools.build_q286_wbss_four_modulus_direct_holdout_decomposition import (  # noqa: E402
    coefficient_lookup,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402
from tools.build_q286_wbss_multiplicative_character_burden_audit import (  # noqa: E402
    MODULUS_FACTORS,
    coefficient_grid,
    coefficient_rows_by_modulus,
    exponent_map,
    load_json,
)
from tools.build_q286_wbss_pointwise_adverse_drag_theorem_target import (  # noqa: E402
    FRESH_SOURCE,
    HORIZON_SOURCE,
    calibration_rows,
)
from tools.build_q286_wbss_projection_uniformity_obstruction_audit import (  # noqa: E402
    projection_distribution,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def active_character_masks(formula):
    coefficients = coefficient_rows_by_modulus(formula)
    maps = {
        factor: exponent_map(factor)
        for factors in MODULUS_FACTORS.values()
        for factor in factors
    }
    masks = {}
    for modulus, factors in MODULUS_FACTORS.items():
        grid = coefficient_grid(modulus, factors, coefficients[modulus], maps)
        transform = np.fft.fftn(grid - np.mean(grid)) / grid.size
        mask = np.abs(transform) ** 2 > 1e-20
        mask[(0,) * len(transform.shape)] = False
        masks[modulus] = {
            "mask": mask,
            "coefficients": coefficients[modulus],
            "maps": maps,
            "factors": factors,
        }
    return masks


def row_moments(row, context, full_coefficients, first_three_coefficients,
                primes, prime_values, log_values, active_masks):
    orbit_data = far.orbit_coefficients(
        int(row["target_residue"]),
        context,
        full_coefficients,
        first_three_coefficients,
    )
    coefficient_data = {
        "orbits": orbit_data["orbits"],
        "first_three": np.asarray(
            orbit_data["first_three_coefficients"], dtype=np.float64),
        "full": np.asarray(
            orbit_data["full_coefficients"], dtype=np.float64),
    }
    actual = far.actual_orbit_measure(
        int(row["target"]),
        coefficient_data,
        primes,
        prime_values,
        log_values,
    )
    actual_mass = np.asarray(actual["masses"], dtype=np.float64)
    uniform_mass = np.asarray(
        orbit_data["uniform_orbit_mass"], dtype=np.float64)

    l2_square = 0.0
    by_modulus = {}
    for modulus, data in active_masks.items():
        delta = np.zeros(
            tuple(factor - 1 for factor in data["factors"]),
            dtype=np.complex128,
        )
        actual_projection = projection_distribution(
            orbit_data["orbits"], actual_mass, modulus)
        uniform_projection = projection_distribution(
            orbit_data["orbits"], uniform_mass, modulus)
        for residue in data["coefficients"]:
            index = tuple(
                data["maps"][factor]["exponent_by_residue"][
                    residue % factor]
                for factor in data["factors"]
            )
            delta[index] = (
                actual_projection.get(residue, 0.0)
                - uniform_projection.get(residue, 0.0))
        # Coefficients use fft(c)/n, so the matching moment is the plus-sign
        # unnormalized character transform.  For real delta this is conj(fft).
        moments = np.conj(np.fft.fftn(delta))
        modulus_l2 = float(
            np.sqrt(np.sum(np.abs(moments[data["mask"]]) ** 2)))
        by_modulus[str(modulus)] = modulus_l2
        l2_square += modulus_l2 * modulus_l2

    aggregate_l2 = math.sqrt(l2_square)
    return {
        "pair_count": int(actual["pair_count"]),
        "actual_mass_sum": float(np.sum(actual_mass)),
        "uniform_mass_sum": float(np.sum(uniform_mass)),
        "character_moment_l2_by_modulus": by_modulus,
        "aggregate_character_moment_l2": aggregate_l2,
    }


def summarize_rows(rows):
    violating_local = [
        row for row in rows
        if row["exceeds_row_local_l2_cap"]
    ]
    violating_global = [
        row for row in rows
        if row["exceeds_global_min_l2_cap"]
    ]
    return {
        "row_count": len(rows),
        "target_minimum": min(row["target"] for row in rows),
        "target_maximum": max(row["target"] for row in rows),
        "zero_pair_count": sum(row["pair_count"] == 0 for row in rows),
        "zero_actual_mass_count": sum(
            abs(row["actual_mass_sum"]) <= TOLERANCE for row in rows),
        "nonunit_actual_mass_sum_count": sum(
            abs(row["actual_mass_sum"] - 1.0) > 1e-10 for row in rows),
        "nonunit_uniform_mass_sum_count": sum(
            abs(row["uniform_mass_sum"] - 1.0) > 1e-10 for row in rows),
        "global_min_cap_exceeding_row_count": len(violating_global),
        "row_local_cap_exceeding_row_count": len(violating_local),
        "max_target_exceeding_row_local_cap": (
            max(row["target"] for row in violating_local)
            if violating_local else None),
        "aggregate_character_moment_l2_summary": finite_summary(
            row["aggregate_character_moment_l2"] for row in rows),
        "row_local_l2_cap_summary": finite_summary(
            row["row_local_l2_cap"] for row in rows),
        "ratio_to_global_min_l2_cap_summary": finite_summary(
            row["ratio_to_global_min_l2_cap"] for row in rows),
        "ratio_to_row_local_l2_cap_summary": finite_summary(
            row["ratio_to_row_local_l2_cap"] for row in rows),
        "largest_row_local_ratio_row": max(
            rows,
            key=lambda row: (
                row["ratio_to_row_local_l2_cap"], -row["target"])),
        "largest_global_ratio_row": max(
            rows,
            key=lambda row: (
                row["ratio_to_global_min_l2_cap"], -row["target"])),
        "smallest_row_local_margin_row": min(
            rows,
            key=lambda row: (
                row["row_local_l2_margin"], row["target"])),
        "largest_row_local_cap_exceedance_rows": sorted(
            violating_local,
            key=lambda row: (
                -row["ratio_to_row_local_l2_cap"], row["target"]),
        )[:20],
    }


def build_receipt():
    l2_payment = load_json(L2_PAYMENT_SOURCE)
    formula = load_json(FORMULA_SOURCE)
    horizon = load_json(HORIZON_SOURCE)
    fresh = load_json(FRESH_SOURCE)
    source_rows = calibration_rows(horizon, fresh)
    _, _by_modulus = coefficient_lookup(formula)
    active_masks = active_character_masks(formula)

    maximum_target = max(row["target"] for row in source_rows)
    primes = np.asarray(far._prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = far.logs(maximum_target)
    context = far.prepare_support_context()
    context["coefficient"] = (
        far.combined_fixed_strict_central_coefficient_receipt())
    full_coefficients = far.period_full_unit_coefficients(context)
    first_three_coefficients = far.q286_first_three_unit_coefficients(context)

    coefficient_l2 = l2_payment["character_l2_budget"][
        "aggregate_character_l2"]
    global_cap = l2_payment["character_l2_budget"][
        "aggregate_character_moment_l2_cap"]
    rows = []
    for source_row in source_rows:
        moments = row_moments(
            source_row,
            context,
            full_coefficients,
            first_three_coefficients,
            primes,
            prime_values,
            log_values,
            active_masks,
        )
        row_local_cap = source_row["local_main"] / coefficient_l2
        aggregate_l2 = moments["aggregate_character_moment_l2"]
        rows.append({
            "source": source_row["source"],
            "target": int(source_row["target"]),
            "target_residue": int(source_row["target_residue"]),
            "target_mod_286": int(source_row["target_mod_286"]),
            "local_main": float(source_row["local_main"]),
            "pair_count": moments["pair_count"],
            "actual_mass_sum": moments["actual_mass_sum"],
            "uniform_mass_sum": moments["uniform_mass_sum"],
            "character_moment_l2_by_modulus": (
                moments["character_moment_l2_by_modulus"]),
            "aggregate_character_moment_l2": aggregate_l2,
            "global_min_l2_cap": global_cap,
            "row_local_l2_cap": row_local_cap,
            "row_local_l2_margin": row_local_cap - aggregate_l2,
            "ratio_to_global_min_l2_cap": aggregate_l2 / global_cap,
            "ratio_to_row_local_l2_cap": aggregate_l2 / row_local_cap,
            "exceeds_global_min_l2_cap": bool(
                aggregate_l2 > global_cap + TOLERANCE),
            "exceeds_row_local_l2_cap": bool(
                aggregate_l2 > row_local_cap + TOLERANCE),
        })

    summary = summarize_rows(rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "aggregate_character_l2_payment_audit": str(
                L2_PAYMENT_SOURCE.relative_to(ROOT)),
            "aggregate_character_l2_payment_status": l2_payment["status"],
            "adverse_drag_horizon_audit": str(
                HORIZON_SOURCE.relative_to(ROOT)),
            "component_envelope_fresh_holdout": str(
                FRESH_SOURCE.relative_to(ROOT)),
        },
        "status": "HOLD_l2_cap_requires_boundary_or_stronger_theorem",
        "status_boundary": (
            "finite observed character-moment diagnostic only; it falsifies "
            "using the aggregate L2 cap as already valid on the checked rows, "
            "but proves no asymptotic aggregate character-moment theorem, "
            "pointwise adverse-drag theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "aggregate_character_l2_bound_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "universal_bound_open": True,
        "zero_mass_check": {
            "zero_pair_count": summary["zero_pair_count"],
            "zero_actual_mass_count": summary["zero_actual_mass_count"],
            "nonunit_actual_mass_sum_count": (
                summary["nonunit_actual_mass_sum_count"]),
            "nonunit_uniform_mass_sum_count": (
                summary["nonunit_uniform_mass_sum_count"]),
            "decision": (
                "No checked row has zero strict-central pair count or zero "
                "actual mass; finite cap failures are not caused by a "
                "zero-mass normalization defect."),
        },
        "acceptance_condition": {
            "finite_evidence_is_acceptance_condition": False,
            "non_circular_bridge_confirmed": False,
            "what_is_confirmed": (
                "The aggregate L2 formula is an arithmetic coefficient "
                "identity and finite diagnostic.  A non-circular proof would "
                "still need an external pointwise aggregate twisted "
                "binary-prime moment estimate."),
            "target": "AdverseDrag(N) < LocalMain(N)",
        },
        "l2_cap": {
            "aggregate_coefficient_l2": coefficient_l2,
            "global_minimum_local_main_cap": global_cap,
            "row_local_cap_rule": (
                "row_local_l2_cap = LocalMain(row) / aggregate_coefficient_l2"),
        },
        "summary": summary,
        "rows": rows,
        "decision": (
            "The aggregate L2 theorem shape remains a useful asymptotic "
            "target, but the checked population falsifies any claim that the "
            "displayed cap already holds at this scale.  On the 348 checked "
            "rows, 301 exceed the global minimum-local-main cap and 120 also "
            "exceed their own row-local L2 cap.  The worst row is target "
            "1089544, with observed aggregate L2 about 0.209829 against a "
            "row-local cap about 0.134756.  No zero-mass defect explains the "
            "failure.  The route therefore requires either an explicit "
            "threshold beyond the finite violations, a stronger structured "
            "moment theorem than plain aggregate L2, or a different signed "
            "estimate."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
