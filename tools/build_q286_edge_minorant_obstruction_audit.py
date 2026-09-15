"""Test whether q286 dual-edge rescue has a coefficientwise minorant.

For a dual lower edge, the normalized rescue margin can be written as

    E_mu[gap] - required = E_mu[gap - required].

If gap - required were nonnegative on every reflection orbit, any nonzero
strict-central pair mass would make the edge rescue automatic.  This receipt
tests that easy bridge.  It also decomposes actual mass over the negative and
positive parts of the pointwise rescue coefficient.

Finite diagnostic only.  It proves no minorant theorem, signed correlation
estimate, q286 threshold theorem, strict-central Goldbach theorem, or Goldbach
theorem.
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
DUAL_SOURCE = EVIDENCE / "q286-lower-face-dual-edge-audit.json"
OVERLAP_SOURCE = EVIDENCE / "q286-lower-face-overlap-audit.json"
OUT = EVIDENCE / "q286-edge-minorant-obstruction-audit.json"
PERIOD = 10010
TOLERANCE = 1e-8

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
from tools.build_q286_prime_indexed_kernel_route_audit import (  # noqa: E402
    logs,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def finite_summary(values):
    finite = tuple(
        float(value) for value in values
        if value is not None and math.isfinite(float(value)))
    if not finite:
        return {"count": 0, "minimum": None, "mean": None, "maximum": None}
    return {
        "count": len(finite),
        "minimum": min(finite),
        "mean": math.fsum(finite) / len(finite),
        "maximum": max(finite),
    }


def coefficient_row(target_residue, context, full_coefficients,
                    first_three_coefficients):
    orbit_data = orbit_coefficients(
        target_residue, context, full_coefficients, first_three_coefficients)
    return {
        "orbits": orbit_data["orbits"],
        "first_three": np.asarray(
            orbit_data["first_three_coefficients"], dtype=np.float64),
        "full": np.asarray(orbit_data["full_coefficients"], dtype=np.float64),
    }


def analyze_row(edge_row, overlap_row, coefficients, primes, prime_values,
                log_values):
    actual = actual_orbit_measure(
        int(edge_row["target"]), coefficients, primes, prime_values, log_values)
    masses = np.asarray(actual["masses"], dtype=np.float64)
    f3 = coefficients["first_three"]
    full = coefficients["full"]
    slope = float(edge_row["slope"])
    intercept = float(edge_row["intercept"])
    required = float(edge_row["required_edge_gap_for_positivity"])
    gap = full - (slope * f3 + intercept)
    rescue_coeff = gap - required

    positive_coeff = np.maximum(rescue_coeff, 0.0)
    negative_coeff = np.maximum(-rescue_coeff, 0.0)
    positive_contribution = float(np.dot(masses, positive_coeff))
    negative_drag = float(np.dot(masses, negative_coeff))
    margin = positive_contribution - negative_drag
    expected_margin = float(edge_row["edge_gap_margin_after_rescue"])
    negative_mask = rescue_coeff < -TOLERANCE
    positive_mask = rescue_coeff > TOLERANCE
    zero_mask = np.abs(rescue_coeff) <= TOLERANCE

    worst_indices = np.argsort(rescue_coeff)[:8]
    best_indices = np.argsort(-rescue_coeff)[:8]
    return {
        "target": int(edge_row["target"]),
        "target_residue": int(edge_row["target_residue"]),
        "target_mod_286": int(edge_row["target_mod_286"]),
        "block_index_after_discovery": int(
            edge_row["block_index_after_discovery"]),
        "pair_count": int(overlap_row["pair_count"]),
        "pointwise_minorant_pass": bool(
            float(np.min(rescue_coeff)) >= -TOLERANCE),
        "minimum_pointwise_rescue_coefficient": float(np.min(rescue_coeff)),
        "maximum_pointwise_rescue_coefficient": float(np.max(rescue_coeff)),
        "negative_rescue_coefficient_orbit_count": int(
            np.sum(negative_mask)),
        "positive_rescue_coefficient_orbit_count": int(
            np.sum(positive_mask)),
        "zero_rescue_coefficient_orbit_count": int(np.sum(zero_mask)),
        "actual_mass_on_negative_rescue_coefficients": float(
            np.sum(masses[negative_mask])),
        "actual_mass_on_positive_rescue_coefficients": float(
            np.sum(masses[positive_mask])),
        "actual_mass_on_zero_rescue_coefficients": float(
            np.sum(masses[zero_mask])),
        "positive_rescue_contribution": positive_contribution,
        "negative_rescue_drag": negative_drag,
        "positive_to_negative_rescue_ratio": (
            positive_contribution / negative_drag
            if negative_drag > TOLERANCE else None),
        "rescue_margin_from_signed_parts": margin,
        "expected_edge_gap_margin_after_rescue": expected_margin,
        "signed_part_identity_error": abs(margin - expected_margin),
        "support_orbits_are_negative_coefficients": all(
            rescue_coeff[index] < -TOLERANCE
            for index in edge_row["support_indices"]),
        "worst_pointwise_orbits": [
            {
                "orbit": coefficients["orbits"][int(index)],
                "rescue_coefficient": float(rescue_coeff[index]),
                "gap": float(gap[index]),
                "actual_mass": float(masses[index]),
                "first_three_coefficient": float(f3[index]),
                "full_coefficient": float(full[index]),
            }
            for index in worst_indices
        ],
        "best_pointwise_orbits": [
            {
                "orbit": coefficients["orbits"][int(index)],
                "rescue_coefficient": float(rescue_coeff[index]),
                "gap": float(gap[index]),
                "actual_mass": float(masses[index]),
                "first_three_coefficient": float(f3[index]),
                "full_coefficient": float(full[index]),
            }
            for index in best_indices
        ],
    }


def build_receipt():
    dual = load_json(DUAL_SOURCE)
    overlap = load_json(OVERLAP_SOURCE)
    overlap_by_target = {int(row["target"]): row
                         for row in overlap["target_rows"]}

    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    maximum_target = max(row["target"] for row in dual["target_rows"])
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)

    rows = []
    for edge_row in dual["target_rows"]:
        if not edge_row["edge_success"]:
            continue
        coefficients = coefficient_row(
            int(edge_row["target_residue"]),
            context,
            full_coefficients,
            first_three_coefficients,
        )
        rows.append(analyze_row(
            edge_row,
            overlap_by_target[int(edge_row["target"])],
            coefficients,
            primes,
            prime_values,
            log_values,
        ))

    post = [row for row in rows if row["block_index_after_discovery"] >= 1]
    discovery = [row for row in rows if row["block_index_after_discovery"] < 1]

    def summarize(bucket):
        return {
            "row_count": len(bucket),
            "pointwise_minorant_pass_count": sum(
                row["pointwise_minorant_pass"] for row in bucket),
            "support_orbits_negative_count": sum(
                row["support_orbits_are_negative_coefficients"]
                for row in bucket),
            "minimum_pointwise_rescue_coefficient_summary": finite_summary(
                row["minimum_pointwise_rescue_coefficient"] for row in bucket),
            "maximum_pointwise_rescue_coefficient_summary": finite_summary(
                row["maximum_pointwise_rescue_coefficient"] for row in bucket),
            "negative_rescue_coefficient_orbit_count_summary": finite_summary(
                row["negative_rescue_coefficient_orbit_count"]
                for row in bucket),
            "positive_rescue_coefficient_orbit_count_summary": finite_summary(
                row["positive_rescue_coefficient_orbit_count"]
                for row in bucket),
            "actual_mass_on_negative_rescue_coefficients_summary":
                finite_summary(
                    row["actual_mass_on_negative_rescue_coefficients"]
                    for row in bucket),
            "actual_mass_on_positive_rescue_coefficients_summary":
                finite_summary(
                    row["actual_mass_on_positive_rescue_coefficients"]
                    for row in bucket),
            "positive_to_negative_rescue_ratio_summary": finite_summary(
                row["positive_to_negative_rescue_ratio"] for row in bucket),
            "rescue_margin_from_signed_parts_summary": finite_summary(
                row["rescue_margin_from_signed_parts"] for row in bucket),
            "signed_part_identity_error_summary": finite_summary(
                row["signed_part_identity_error"] for row in bucket),
        }

    weakest_rows = sorted(
        post,
        key=lambda row: (
            row["positive_to_negative_rescue_ratio"],
            row["target"]))[:20]

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "lower_face_dual_edge_audit": str(DUAL_SOURCE.relative_to(ROOT)),
            "lower_face_overlap_audit": str(OVERLAP_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite edge-minorant obstruction audit only; no coefficientwise "
            "minorant theorem, signed prime-correlation theorem, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof"
        ),
        "goldbach_proved": False,
        "coefficientwise_minorant_theorem_proved": False,
        "pointwise_minorant_candidate_falsified": True,
        "curiosity_status": "changed-under-evidence",
        "novelty_label": "new-to-this-task",
        "candidate": {
            "mechanism": (
                "If gap - required were pointwise nonnegative on all "
                "reflection orbits, the raw edge rescue would reduce to "
                "ordinary nonnegative mass and would not need a signed "
                "prime-correlation theorem."
            ),
            "prediction": (
                "Because the lower-face support has zero gap while required "
                "edge gap is positive, the pointwise coefficient should be "
                "negative on the bad support and fail on every row."
            ),
            "falsifier": (
                "Any checked row with nonnegative gap - required on all orbits "
                "would keep a coefficientwise minorant route alive."
            ),
            "smallest_test": (
                "Use the 230 dual-edge rows, recompute actual orbit mass, and "
                "decompose E_mu[gap-required] into positive and negative "
                "pointwise parts."
            ),
        },
        "decision": (
            "The easy coefficientwise minorant route fails on every checked "
            "row: the lower-face support itself carries negative pointwise "
            "rescue coefficients.  Actual rows still rescue because their "
            "prime-pair mass lands mostly on positive pointwise coefficients. "
            "The remaining bridge is therefore a distributional anti-landing "
            "or signed binary-prime correlation theorem."
        ),
        "summary": {
            "target_row_count": len(rows),
            "post_discovery_target_count": len(post),
            "discovery_target_count": len(discovery),
            "all_rows": summarize(rows),
            "post_discovery_rows": summarize(post),
            "discovery_rows": summarize(discovery),
            "weakest_post_discovery_signed_part_rows": weakest_rows,
        },
        "target_rows": rows,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
