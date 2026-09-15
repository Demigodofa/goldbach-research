"""Audit whether the q286 full action is a count minorant.

The previous bridge pivot asks for an unnormalized object whose positivity
implies a Goldbach pair.  A signed raw action already has that implication if
it is proved strictly positive: with no prime pairs every weighted sum is
zero.  This receipt checks the stronger shortcut, namely whether the existing
q286 aggregate coefficient is a coefficientwise nonnegative lower-bound
minorant for the strict-central weighted count.

It is a coefficient-side finite audit only.  It proves no pointwise signed
prime-correlation estimate and no Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-unnormalized-witness-minorant-audit.json"
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

    values = np.asarray([
        complex(coefficient["aggregate_coefficient_by_unit_residue"][unit])
        for unit in units
    ], dtype=np.complex128)
    real_by_unit = {
        unit: float(value.real) for unit, value in zip(units, values)
    }
    real_values = values.real
    imag_abs = np.abs(values.imag)
    principal_mean = complex(coefficient["aggregate_principal_mean"])

    negative_units = [
        int(unit) for unit, value in zip(units, real_values)
        if value < -tolerance
    ]
    positive_units = [
        int(unit) for unit, value in zip(units, real_values)
        if value > tolerance
    ]
    zero_units = [
        int(unit) for unit, value in zip(units, real_values)
        if abs(value) <= tolerance
    ]

    target_rows = []
    for target_residue in range(0, PERIOD, 2):
        support = admissible_units(target_residue, units)
        support_values = [real_by_unit[unit] for unit in support]
        negative_count = sum(value < -tolerance for value in support_values)
        positive_count = sum(value > tolerance for value in support_values)
        target_rows.append({
            "target_residue": target_residue,
            "admissible_support_size": len(support),
            "minimum_coefficient": min(support_values),
            "maximum_coefficient": max(support_values),
            "negative_coefficient_count": negative_count,
            "positive_coefficient_count": positive_count,
            "has_negative_coefficient": bool(negative_count),
            "has_positive_coefficient": bool(positive_count),
        })

    global_min_index = int(np.argmin(real_values))
    global_max_index = int(np.argmax(real_values))
    real_min = float(real_values[global_min_index])
    real_max = float(real_values[global_max_index])
    if real_max <= tolerance:
        positive_scalar_to_unit_interval = None
    elif real_min >= -tolerance:
        positive_scalar_to_unit_interval = 1.0 / real_max
    else:
        positive_scalar_to_unit_interval = None

    every_even_support_sign_indefinite = all(
        row["has_negative_coefficient"] and row["has_positive_coefficient"]
        for row in target_rows)
    positive_raw_action_implication = (
        "If the unnormalized signed action "
        "sum_r W_N(r)c(r) is proved strictly positive, then T_N>0, because "
        "all W_N(r) are nonnegative and W_N(r)=0 for every r would make the "
        "signed action zero.")
    minorant_failure = (
        "The existing q286 aggregate coefficient is sign-indefinite on every "
        "even target residue support, so positive scalar multiples of it are "
        "not coefficientwise nonnegative minorants of T_N.")

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "arithmetic_period": PERIOD,
        "assembled_quotients": coefficient["assembled_quotients"],
        "unit_group_order": len(units),
        "principal_mean": principal_mean,
        "coefficient_real_summary": finite_summary(real_values),
        "coefficient_imag_abs_summary": finite_summary(imag_abs),
        "global_minimum_unit": int(units[global_min_index]),
        "global_maximum_unit": int(units[global_max_index]),
        "negative_unit_count": len(negative_units),
        "positive_unit_count": len(positive_units),
        "zero_unit_count": len(zero_units),
        "negative_unit_fraction": len(negative_units) / len(units),
        "raw_coefficient_is_nonnegative": bool(real_min >= -tolerance),
        "raw_coefficient_is_unit_interval_minorant": bool(
            real_min >= -tolerance and real_max <= 1.0 + tolerance),
        "positive_scalar_multiple_can_be_nonnegative_minorant": bool(
            positive_scalar_to_unit_interval is not None),
        "positive_scalar_to_unit_interval_if_available": (
            positive_scalar_to_unit_interval),
        "even_target_residue_count": len(target_rows),
        "admissible_support_size_summary": finite_summary(
            row["admissible_support_size"] for row in target_rows),
        "support_minimum_coefficient_summary": finite_summary(
            row["minimum_coefficient"] for row in target_rows),
        "support_maximum_coefficient_summary": finite_summary(
            row["maximum_coefficient"] for row in target_rows),
        "target_residue_supports_with_no_negative_coefficients": [
            row["target_residue"] for row in target_rows
            if not row["has_negative_coefficient"]
        ],
        "target_residue_supports_with_no_positive_coefficients": [
            row["target_residue"] for row in target_rows
            if not row["has_positive_coefficient"]
        ],
        "every_even_target_support_sign_indefinite": bool(
            every_even_support_sign_indefinite),
        "selected_target_rows": [
            row for row in target_rows
            if row["target_residue"] in (14138 % PERIOD, 14996 % PERIOD,
                                         94856 % PERIOD, 1222142 % PERIOD,
                                         1240888 % PERIOD, 1242118 % PERIOD,
                                         1379072 % PERIOD)
        ],
        "positive_raw_action_implication": positive_raw_action_implication,
        "minorant_failure": minorant_failure,
        "decision": (
            "Demote the coefficientwise nonnegative minorant shortcut for the "
            "existing q286 full-action coefficient. Preserve the signed "
            "witness route: a direct proof of positive unnormalized q286 "
            "action would imply a Goldbach pair, but it is a pointwise signed "
            "binary-prime correlation theorem, not a nonnegative sieve "
            "minorant."),
        "status_boundary": (
            "finite coefficient audit only; no q286 threshold theorem, no "
            "signed prime-correlation theorem, no strict-central Goldbach "
            "theorem, and no Goldbach proof"),
        "minorant_shortcut_falsified": bool(
            real_min < -tolerance
            and real_max > tolerance
            and every_even_support_sign_indefinite
            and positive_scalar_to_unit_interval is None),
        "signed_witness_route_preserved": True,
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
        "negative_unit_count": receipt["negative_unit_count"],
        "positive_unit_count": receipt["positive_unit_count"],
        "every_even_target_support_sign_indefinite": (
            receipt["every_even_target_support_sign_indefinite"]),
        "minorant_shortcut_falsified": (
            receipt["minorant_shortcut_falsified"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }), sort_keys=True))


if __name__ == "__main__":
    main()
