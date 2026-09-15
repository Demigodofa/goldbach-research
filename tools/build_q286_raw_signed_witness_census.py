"""Build a finite census for the raw unnormalized q286 signed witness.

The signed-witness bridge says that proving the raw unnormalized q286 action
strictly positive would imply at least one strict-central prime pair: if there
are no strict-central prime pairs, every residue weight W_N(r) is zero and the
signed sum is zero.

This receipt tests the naive finite threshold version of that idea on complete
period cycles.  It is not an asymptotic estimate or a proof of Goldbach.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-raw-signed-witness-census.json"
BASE_TARGET_MINIMUM = 10000
CYCLE_COUNT = 12
TOLERANCE = 1e-9

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    combined_coefficient_centered_error_envelope_receipt,
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


def build_receipt(base_target_minimum=BASE_TARGET_MINIMUM,
                  cycle_count=CYCLE_COUNT, tolerance=TOLERANCE):
    base = combined_coefficient_centered_error_envelope_receipt(
        base_target_minimum=base_target_minimum,
        cycle_count=cycle_count,
        targets_per_cycle=None,
        tolerance=tolerance)

    cycle_rows = []
    all_nonpositive_targets = []
    positive_cycle_indices = []
    nonpositive_cycle_indices = []
    for cycle_index, row in sorted(
            base["cycle_rows"].items(), key=lambda item: int(item[0])):
        nonpositive_targets = tuple(row["negative_or_zero_targets"])
        compact = {
            "cycle_index": int(cycle_index),
            "target_range": tuple(row["target_range"]),
            "tested_target_count": row["tested_target_count"],
            "negative_or_zero_weighted_sum_count": (
                row["negative_or_zero_weighted_sum_count"]),
            "minimum_centered_to_principal_target": (
                row["minimum_centered_to_principal_target"]),
            "minimum_centered_to_principal_ratio": (
                row["minimum_centered_to_principal_ratio"]),
            "mean_centered_to_principal_ratio": (
                row["mean_centered_to_principal_ratio"]),
            "negative_or_zero_targets": nonpositive_targets,
        }
        cycle_rows.append(compact)
        all_nonpositive_targets.extend(nonpositive_targets)
        if nonpositive_targets:
            nonpositive_cycle_indices.append(int(cycle_index))
        else:
            positive_cycle_indices.append(int(cycle_index))

    total_targets = math.fsum(row["tested_target_count"] for row in cycle_rows)
    nonpositive_count = len(all_nonpositive_targets)
    last_nonpositive_target = (
        max(all_nonpositive_targets) if all_nonpositive_targets else None)
    contiguous_positive_suffix_start_cycle = None
    for row in reversed(cycle_rows):
        if row["negative_or_zero_weighted_sum_count"]:
            break
        contiguous_positive_suffix_start_cycle = row["cycle_index"]

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "arithmetic_period": base["arithmetic_period"],
        "principal_mean": base["principal_mean"],
        "base_target_minimum": base_target_minimum,
        "cycle_count": cycle_count,
        "targets_per_cycle": base["targets_per_cycle"],
        "full_cycles_scanned": base["full_cycles_scanned"],
        "total_even_targets_scanned": int(total_targets),
        "nonpositive_raw_signed_action_count": nonpositive_count,
        "nonpositive_raw_signed_action_fraction": (
            nonpositive_count / total_targets if total_targets else None),
        "all_scanned_targets_positive": base["all_scanned_targets_positive"],
        "global_minimum_centered_to_principal_target": (
            base["global_minimum_centered_to_principal_target"]),
        "global_minimum_centered_to_principal_ratio": (
            base["global_minimum_centered_to_principal_ratio"]),
        "nonpositive_cycle_indices": nonpositive_cycle_indices,
        "positive_cycle_indices": positive_cycle_indices,
        "last_nonpositive_target": last_nonpositive_target,
        "contiguous_positive_suffix_start_cycle": (
            contiguous_positive_suffix_start_cycle),
        "contiguous_positive_suffix_start_target": (
            base_target_minimum
            + contiguous_positive_suffix_start_cycle * base["arithmetic_period"]
            if contiguous_positive_suffix_start_cycle is not None else None),
        "cycle_minimum_ratio_summary": finite_summary(
            row["minimum_centered_to_principal_ratio"] for row in cycle_rows),
        "cycle_nonpositive_count_summary": finite_summary(
            row["negative_or_zero_weighted_sum_count"] for row in cycle_rows),
        "cycle_rows": cycle_rows,
        "signed_witness_implication": (
            "For any target, strict positivity of the raw unnormalized signed "
            "q286 action implies at least one strict-central prime pair, "
            "because all W_N(r) are nonnegative and absence of prime pairs "
            "makes the signed action exactly zero."),
        "falsified_candidate": (
            "The naive threshold candidate 'raw q286 signed action is "
            "positive for every even N>=10000' is falsified by finite rows."),
        "surviving_candidate": (
            "A later threshold or a residue-conditioned signed correlation "
            "theorem remains possible only after explicitly checking or "
            "excluding the finite nonpositive rows."),
        "status_boundary": (
            "finite raw-action census only; no threshold theorem, no pointwise "
            "signed prime-correlation theorem, no strict-central Goldbach "
            "theorem, and no Goldbach proof"),
        "raw_signed_witness_census_measured": True,
        "naive_from_10000_signed_witness_positivity_falsified": bool(
            nonpositive_count > 0),
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
        "total_even_targets_scanned": receipt["total_even_targets_scanned"],
        "nonpositive_raw_signed_action_count": (
            receipt["nonpositive_raw_signed_action_count"]),
        "last_nonpositive_target": receipt["last_nonpositive_target"],
        "contiguous_positive_suffix_start_cycle": (
            receipt["contiguous_positive_suffix_start_cycle"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }), sort_keys=True))


if __name__ == "__main__":
    main()
