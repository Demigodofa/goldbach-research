"""Audit local main-term positivity for the raw q286 signed witness.

The raw q286 signed-witness route can only become a Goldbach bridge if its
fixed coefficient has a positive local singular main term for every target
residue.  This receipt averages the assembled coefficient over the admissible
support A_a={r in U_10010:gcd(a-r,10010)=1} for every even residue a.

This is a coefficient-side theorem-shaping audit only.  It proves no
equidistribution of binary prime pairs, no pointwise error estimate, and no
Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-local-main-term-positivity-audit.json"
PERIOD = 10010
TOLERANCE = 1e-8

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, np.generic):
        return json_ready(value.item())
    if isinstance(value, complex):
        return {
            "real": float(value.real),
            "imag": float(value.imag),
        }
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def finite_summary(values):
    values = tuple(float(value) for value in values)
    if not values:
        return {
            "count": 0,
            "minimum": None,
            "maximum": None,
            "mean": None,
        }
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def admissible_units(target_residue, units):
    return tuple(
        unit for unit in units
        if math.gcd((target_residue - unit) % PERIOD, PERIOD) == 1)


def build_receipt(tolerance=TOLERANCE):
    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    units = tuple(
        residue for residue in range(PERIOD)
        if math.gcd(residue, PERIOD) == 1)
    if tuple(coefficient["aggregate_coefficient_by_unit_residue"]) != units:
        raise AssertionError("unexpected unit residue ordering")

    coefficient_by_unit = {
        unit: complex(coefficient["aggregate_coefficient_by_unit_residue"][unit])
        for unit in units
    }
    principal_mean = complex(coefficient["aggregate_principal_mean"])
    if principal_mean.real <= tolerance:
        raise AssertionError("expected positive real principal mean")

    target_rows = []
    for target_residue in range(0, PERIOD, 2):
        support = admissible_units(target_residue, units)
        support_values = [coefficient_by_unit[unit] for unit in support]
        local_mean = math.fsum(value.real for value in support_values) / len(
            support_values)
        local_imag_mean = math.fsum(
            value.imag for value in support_values) / len(support_values)
        centered_deviation = local_mean - principal_mean.real
        ratio = local_mean / principal_mean.real
        target_rows.append({
            "target_residue": target_residue,
            "admissible_support_size": len(support),
            "local_main_term_mean": local_mean,
            "local_main_term_imag_mean": local_imag_mean,
            "local_main_term_to_principal_ratio": ratio,
            "local_centered_deviation_to_principal_ratio": (
                centered_deviation / principal_mean.real),
            "local_main_term_positive": bool(local_mean > tolerance),
            "local_error_ratio_needed_for_positive_raw_action": (
                "centered_error(N).real/local_main_term_action(N).real > -1"),
        })

    nonpositive_rows = [
        row for row in target_rows
        if not row["local_main_term_positive"]
    ]
    minimum_row = min(
        target_rows, key=lambda row: row[
            "local_main_term_to_principal_ratio"])
    maximum_row = max(
        target_rows, key=lambda row: row[
            "local_main_term_to_principal_ratio"])

    selected_residues = sorted({
        14138 % PERIOD,
        14996 % PERIOD,
        88346 % PERIOD,
        90080 % PERIOD,
        94856 % PERIOD,
        1222142 % PERIOD,
        1240888 % PERIOD,
        1242118 % PERIOD,
        1379072 % PERIOD,
        194384 % PERIOD,
    })

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "arithmetic_period": PERIOD,
        "unit_group_order": len(units),
        "even_target_residue_count": len(target_rows),
        "assembled_quotients": coefficient["assembled_quotients"],
        "principal_mean": principal_mean,
        "admissible_support_size_summary": finite_summary(
            row["admissible_support_size"] for row in target_rows),
        "local_main_term_summary": finite_summary(
            row["local_main_term_mean"] for row in target_rows),
        "local_main_term_imag_abs_summary": finite_summary(
            abs(row["local_main_term_imag_mean"]) for row in target_rows),
        "local_main_term_to_principal_ratio_summary": finite_summary(
            row["local_main_term_to_principal_ratio"]
            for row in target_rows),
        "local_centered_deviation_to_principal_ratio_summary": finite_summary(
            row["local_centered_deviation_to_principal_ratio"]
            for row in target_rows),
        "minimum_local_ratio_row": minimum_row,
        "maximum_local_ratio_row": maximum_row,
        "nonpositive_local_main_term_count": len(nonpositive_rows),
        "nonpositive_local_main_term_residues": [
            row["target_residue"] for row in nonpositive_rows],
        "all_even_residue_local_main_terms_positive": bool(
            not nonpositive_rows),
        "selected_target_residue_rows": [
            row for row in target_rows
            if row["target_residue"] in selected_residues
        ],
        "candidate_mechanism": (
            "The raw signed witness decomposes into a positive local "
            "main term plus a centered binary-prime correlation error for "
            "each even residue modulo 10010."),
        "prediction": (
            "If a fixed-modulus binary Goldbach-in-progressions theorem "
            "controls the centered error below the local main term, then "
            "the raw q286 signed action is eventually positive in every "
            "even residue class."),
        "falsifier": (
            "Any even residue with local_main_term_mean <= 0 falsifies this "
            "local-main-term bridge for the current assembled coefficient."),
        "smallest_new_problem": (
            "For every even residue a modulo 10010, prove RawFull(N) = "
            "LocalMain_a(N) + CenteredError_a(N) with LocalMain_a(N)>0 and "
            "CenteredError_a(N) > -LocalMain_a(N) for all sufficiently large "
            "N == a mod 10010, then finite-check the remaining targets."),
        "decision": (
            "If all local means are positive, preserve the signed-witness "
            "route and move the open gap to a pointwise centered-error "
            "estimate for the exact coefficient. If any local mean is "
            "nonpositive, the existing coefficient cannot supply an eventual "
            "positive-main-term q286 bridge in that residue."),
        "status_boundary": (
            "finite local coefficient audit only; no binary-prime "
            "equidistribution theorem, no q286 threshold theorem, no "
            "strict-central Goldbach theorem, and no Goldbach proof"),
        "local_main_term_positivity_measured": True,
        "pointwise_centered_error_estimate_proved": False,
        "eventual_signed_witness_threshold_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(json_ready(receipt), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(json.dumps(json_ready({
        "wrote": str(OUT.relative_to(ROOT)),
        "nonpositive_local_main_term_count": (
            receipt["nonpositive_local_main_term_count"]),
        "minimum_local_ratio_target_residue": (
            receipt["minimum_local_ratio_row"]["target_residue"]),
        "minimum_local_ratio": (
            receipt["minimum_local_ratio_row"][
                "local_main_term_to_principal_ratio"]),
        "maximum_local_ratio": (
            receipt["maximum_local_ratio_row"][
                "local_main_term_to_principal_ratio"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }), sort_keys=True))


if __name__ == "__main__":
    main()
