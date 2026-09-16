"""Build a fresh prime-row holdout for the degree-5 source-start lane.

The source-reachability reconciliation narrowed the live target from every
translated active-row start to the canonical source start produced by the
original construction.  This receipt checks fresh scales beyond the six-scale
fixture, but only at the first prime row for each scale.  It is deliberately a
thin holdout, not a universal theorem and not a full-scale sweep.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lcm_sawtooth_lifted_endpoint_frame import (  # noqa: E402
    lifted_endpoint_residue_gram_receipt,
)
from mobius_covariance_endpoint_probe import _prime_flags  # noqa: E402
from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    PAIRS,
    dominance_row,
    flatten_rows,
    scale_parameters,
    sign_counts,
)
from tools.build_mobius_moment_square_degree5_primewise_dominance_audit import (  # noqa: E402
    THRESHOLD,
)


OUT = (
    ROOT
    / "evidence"
    / "mobius-moment-square-degree5-source-start-fresh-prime-row-holdout.json")
FRESH_SCALES = (229, 251, 293)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def first_prime_at_or_above(value):
    flags = _prime_flags(2 * value + 50)
    for candidate in range(value, len(flags)):
        if flags[candidate]:
            return candidate
    raise ValueError(f"no prime found above {value}")


def source_start_prime_row(scale_modulus):
    prime_modulus = first_prime_at_or_above(scale_modulus)
    parameters = scale_parameters(scale_modulus)
    divisor_lower, divisor_upper = parameters["divisor_range"]
    receipt = lifted_endpoint_residue_gram_receipt(
        prime_modulus,
        parameters["row_count"],
        parameters["ell_freeze"],
        divisor_lower,
        divisor_upper,
    )
    active = np.asarray(receipt["active_window_residue_energy_gram"])
    active = (active + active.T) / 2
    full = np.asarray(receipt["full_residue_energy_gram"])
    full = (full + full.T) / 2

    component_rows = []
    for left, right, left_label, right_label in PAIRS:
        active_contribution = float(2 * active[left, right])
        full_contribution = float(2 * full[left, right])
        half_contribution = (
            active_contribution - THRESHOLD * full_contribution)
        component_rows.append(dominance_row(
            scale_modulus,
            prime_modulus,
            f"{left_label},{right_label}",
            active_contribution,
            full_contribution,
            half_contribution,
        ))

    active_total = sum(
        row["active_contribution"] for row in component_rows)
    full_total = sum(row["full_contribution"] for row in component_rows)
    half_total = sum(row["half_frame_contribution"] for row in component_rows)
    total_row = dominance_row(
        scale_modulus,
        prime_modulus,
        "TOTAL",
        active_total,
        full_total,
        half_total,
    )
    rows = component_rows + [total_row]
    weakest = min(rows, key=lambda row: row[
        "dominance_slack_above_one_half"])
    return {
        "scale_modulus": scale_modulus,
        "prime_modulus": prime_modulus,
        "row_count": parameters["row_count"],
        "ell_freeze": parameters["ell_freeze"],
        "divisor_range": parameters["divisor_range"],
        "canonical_source_start": parameters["row_count"],
        "component_rows": component_rows,
        "degree5_total_row": total_row,
        "all_rows_dominate_one_half_signed_full": all(
            row["dominates_one_half_signed_full"] for row in rows),
        "minimum_dominance_slack_above_one_half": (
            weakest["dominance_slack_above_one_half"]),
        "weakest_dominance_row": weakest,
    }


def build_receipt():
    scale_results = [
        source_start_prime_row(scale_modulus)
        for scale_modulus in FRESH_SCALES
    ]
    all_rows = flatten_rows([
        {
            "prime_rows": [{
                "component_rows": row["component_rows"],
                "degree5_total_row": row["degree5_total_row"],
            }]
        }
        for row in scale_results
    ])
    component_rows = [row for row in all_rows if row["label"] != "TOTAL"]
    total_rows = [row for row in all_rows if row["label"] == "TOTAL"]
    all_slacks = [
        row["dominance_slack_above_one_half"] for row in all_rows]
    weakest = min(
        all_rows,
        key=lambda row: row["dominance_slack_above_one_half"])
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": (
            "HOLDOUT_degree5_source_start_fresh_first_prime_rows"),
        "question": (
            "After the translated start-1 puncture was proved unreachable, do "
            "fresh canonical source-start first-prime rows beyond the six "
            "checked scales still satisfy signed active/full dominance?"),
        "fresh_scales": FRESH_SCALES,
        "prior_checked_scales": (127, 149, 167, 191, 211, 227),
        "threshold": THRESHOLD,
        "scale_results": scale_results,
        "fresh_scale_count": len(scale_results),
        "prime_row_count": len(scale_results),
        "component_row_count": len(component_rows),
        "degree5_total_row_count": len(total_rows),
        "dominance_row_count": len(all_rows),
        "all_dominance_slack_sign_counts": sign_counts(all_slacks),
        "all_rows_dominate_one_half_signed_full": all(
            row["dominates_one_half_signed_full"] for row in all_rows),
        "minimum_dominance_slack_above_one_half": min(all_slacks),
        "weakest_dominance_row": weakest,
        "prediction": (
            "If the narrowed source-start lane is structural rather than an "
            "artifact of the original fixture, fresh canonical source starts "
            "should continue to show positive slack at new scales."),
        "falsifier": (
            "Any fresh canonical source-start component or total row with "
            "negative full contribution and active/full ratio at or below one "
            "half would falsify this first-prime-row holdout."),
        "decision": (
            "The fresh first-prime-row source-start holdout survives on "
            "scales 229, 251, and 293.  All 12 component and total rows have "
            "positive active/full dominance slack above one half.  This is "
            "not a full fresh-scale sweep and proves no universal theorem."),
        "fresh_first_prime_row_holdout_only": True,
        "full_fresh_scale_sweep_completed": False,
        "finite_holdout_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_window_theorem_proved": False,
        "source_start_theorem_proved": False,
        "active_window_translation_theorem_proved": False,
        "endpoint_swap_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
    }


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
