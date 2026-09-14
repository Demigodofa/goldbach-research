"""Build q286 mass-matched opposite-outcome midpoint decomposition evidence.

This keeps the existing near-boundary window and asks a narrower question than
another threshold scan: among opposite outcomes, when rows are matched first by
q286 target residue and then by reflection-orbit sign mask, which exact
midpoint product term explains the clear-minus-tail swing?
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-mass-matched-pair-decomposition.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_mass_matched_pair_decomposition_receipt,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {key: json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def compact_window(row):
    return {
        "window_label": row["window_label"],
        "start": row["start"],
        "cycle_count": row["cycle_count"],
        "targets_per_cycle": row["targets_per_cycle"],
        "tested_target_count": row["tested_target_count"],
        "near_boundary_target_count": row["near_boundary_target_count"],
        "near_boundary_tail_target_count": (
            row["near_boundary_tail_target_count"]),
        "near_boundary_clear_target_count": (
            row["near_boundary_clear_target_count"]),
        "opposite_outcome_pair_count": row["opposite_outcome_pair_count"],
        "same_target_mod_286_pair_count": (
            row["same_target_mod_286_pair_count"]),
        "same_sign_mask_pair_count": row["same_sign_mask_pair_count"],
        "fallback_pair_count": row["fallback_pair_count"],
        "not_applicable_reason": row["not_applicable_reason"],
        "mass_distance_min": row["mass_distance_min"],
        "mass_distance_mean": row["mass_distance_mean"],
        "mass_distance_max": row["mass_distance_max"],
        "maximum_midpoint_reconstruction_error": (
            row["maximum_midpoint_reconstruction_error"]),
        "sign_consistency_by_term": row["sign_consistency_by_term"],
    }


def main():
    receipt = q286_first_three_mass_matched_pair_decomposition_receipt()
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite mass-matched opposite-outcome decomposition; no "
            "mass-transfer theorem, eventual exact-curve theorem, signed "
            "prime-correlation estimate, or Goldbach proof is established"),
        "window_summaries": tuple(
            compact_window(row) for row in receipt["window_rows"]),
        "pair_rows": {
            row["window_label"]: row["pair_rows"]
            for row in receipt["window_rows"]},
        "aggregate_sign_consistency_by_term": (
            receipt["aggregate_sign_consistency_by_term"]),
        "maximum_midpoint_reconstruction_error": (
            receipt["maximum_midpoint_reconstruction_error"]),
        "interpretation": {
            "mechanism_tested": (
                "The clear-minus-tail swing is split exactly into positive "
                "mass transfer, positive landing quality, negative-pressure "
                "mass control, and negative-pressure landing control."),
            "useful_boundary": (
                "Matching is q286-residue-first and sign-mask-second.  The "
                "late window has no opposite-outcome near-boundary pairs, "
                "so it is recorded as not applicable instead of omitted."),
            "remaining_theorem": (
                "A proof would need an arithmetic estimate forcing a "
                "favorable combination of these product terms, not another "
                "standalone one-dimensional threshold."),
        },
        "mass_matched_pair_decomposition_measured": True,
        "mass_transfer_landing_quality_theorem_proved": False,
        "eventual_exact_curve_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
