"""Build the first fresh holdout for the q286 raw signed-witness threshold.

The previous raw signed-witness census found a finite positive suffix beginning
at target 90080, but it also showed that an earlier clean run can be followed
by recurrence.  This receipt tests the next twelve full M=10010 cycles after
the previous scanned range.  It is a predeclared threshold falsifier, not a
proof of eventual positivity.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PREVIOUS = ROOT / "evidence" / "q286-raw-signed-witness-census.json"
OUT = ROOT / "evidence" / "q286-raw-signed-witness-threshold-holdout.json"
FRESH_BASE_TARGET = 130120
FRESH_CYCLE_COUNT = 12
TOLERANCE = 1e-9

sys.path.insert(0, str(ROOT))

from tools.build_q286_raw_signed_witness_census import (  # noqa: E402
    build_receipt as build_raw_census_receipt,
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


def build_receipt(fresh_base_target=FRESH_BASE_TARGET,
                  fresh_cycle_count=FRESH_CYCLE_COUNT,
                  tolerance=TOLERANCE):
    previous = json.loads(PREVIOUS.read_text(encoding="utf-8"))
    fresh = build_raw_census_receipt(
        base_target_minimum=fresh_base_target,
        cycle_count=fresh_cycle_count,
        tolerance=tolerance)

    previous_suffix_start = previous["contiguous_positive_suffix_start_target"]
    previous_cycle_count = previous["cycle_count"]
    previous_targets_per_cycle = previous["targets_per_cycle"]
    previous_end = (
        previous["base_target_minimum"]
        + previous_cycle_count * previous["arithmetic_period"]
        - 2)
    expected_fresh_start = previous_end + 2
    if fresh_base_target != expected_fresh_start:
        raise AssertionError("fresh holdout must start after prior census")

    fresh_end = (
        fresh_base_target
        + fresh_cycle_count * fresh["arithmetic_period"]
        - 2)
    combined_positive_suffix_count = int(
        (fresh_end - previous_suffix_start) // 2 + 1)
    previous_positive_suffix_count = int(
        (previous_end - previous_suffix_start) // 2 + 1)

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "arithmetic_period": fresh["arithmetic_period"],
        "previous_census": {
            "path": str(PREVIOUS.relative_to(ROOT)),
            "source_commit": previous["source_commit"],
            "base_target_minimum": previous["base_target_minimum"],
            "cycle_count": previous_cycle_count,
            "targets_per_cycle": previous_targets_per_cycle,
            "last_nonpositive_target": previous["last_nonpositive_target"],
            "positive_suffix_start_target": previous_suffix_start,
            "target_end": previous_end,
            "positive_suffix_even_target_count": (
                previous_positive_suffix_count),
        },
        "fresh_holdout": {
            "base_target_minimum": fresh_base_target,
            "cycle_count": fresh_cycle_count,
            "targets_per_cycle": fresh["targets_per_cycle"],
            "target_end": fresh_end,
            "total_even_targets_scanned": fresh["total_even_targets_scanned"],
            "nonpositive_raw_signed_action_count": (
                fresh["nonpositive_raw_signed_action_count"]),
            "all_scanned_targets_positive": (
                fresh["all_scanned_targets_positive"]),
            "global_minimum_centered_to_principal_target": (
                fresh["global_minimum_centered_to_principal_target"]),
            "global_minimum_centered_to_principal_ratio": (
                fresh["global_minimum_centered_to_principal_ratio"]),
            "cycle_nonpositive_counts": [
                row["negative_or_zero_weighted_sum_count"]
                for row in fresh["cycle_rows"]
            ],
            "cycle_minima": [
                {
                    "cycle_index": row["cycle_index"],
                    "target": row["minimum_centered_to_principal_target"],
                    "ratio": row["minimum_centered_to_principal_ratio"],
                }
                for row in fresh["cycle_rows"]
            ],
        },
        "combined_checked_positive_suffix": {
            "start_target": previous_suffix_start,
            "end_target": fresh_end,
            "even_target_count": combined_positive_suffix_count,
            "nonpositive_raw_signed_action_count_after_start": 0,
        },
        "threshold_candidate_preserved": bool(
            fresh["nonpositive_raw_signed_action_count"] == 0),
        "threshold_candidate_proved": False,
        "falsifier": (
            "Any nonpositive raw signed action at or above 90080 in a fresh "
            "unchanged full-cycle holdout falsifies the current finite "
            "threshold candidate."),
        "decision": (
            "The fresh holdout preserves, but does not prove, a threshold "
            "candidate after the last known nonpositive target 88346. The "
            "next theorem requirement is still an analytic reason that later "
            "recurrences cannot happen."),
        "status_boundary": (
            "finite fresh holdout only; no eventual threshold theorem, no "
            "pointwise signed prime-correlation theorem, no strict-central "
            "Goldbach theorem, and no Goldbach proof"),
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
        "fresh_nonpositive_count": (
            receipt["fresh_holdout"]["nonpositive_raw_signed_action_count"]),
        "combined_positive_suffix_start": (
            receipt["combined_checked_positive_suffix"]["start_target"]),
        "combined_positive_suffix_end": (
            receipt["combined_checked_positive_suffix"]["end_target"]),
        "combined_positive_suffix_even_target_count": (
            receipt["combined_checked_positive_suffix"]["even_target_count"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }), sort_keys=True))


if __name__ == "__main__":
    main()
