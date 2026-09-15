"""Recover the dual lower-edge certificate behind q286 lower-face optimizers.

For each checked row, the lower-face LP chooses two reflection orbits at the
observed first-three value.  This receipt converts that opaque LP answer into
an affine lower-edge certificate:

    gap(orbit) = Full(orbit) - slope * F3(orbit) - intercept >= 0.

Then Full(mu_N)>0 becomes the edge-gap rescue inequality:

    E_mu_N gap > -edge(F3(mu_N)).

This is a finite diagnostic only.  It proves no dual-edge theorem, signed
prime-correlation estimate, q286 threshold theorem, or Goldbach theorem.
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
OVERLAP_SOURCE = EVIDENCE / "q286-lower-face-overlap-audit.json"
SIGNATURE_SOURCE = EVIDENCE / "q286-lower-face-support-signature-audit.json"
OUT = EVIDENCE / "q286-lower-face-dual-edge-audit.json"
PERIOD = 10010
MODULUS = 286
TOLERANCE = 1e-8
GAP_TOLERANCE = 1e-7

sys.path.insert(0, str(ROOT))

from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    orbit_coefficients,
    period_full_unit_coefficients,
    prepare_support_context,
    q286_first_three_unit_coefficients,
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


def orbit_key(orbit):
    return tuple(sorted(int(unit) % PERIOD for unit in orbit))


def support_indices(coefficients, support_orbits):
    index_by_orbit = {
        orbit_key(orbit): index
        for index, orbit in enumerate(coefficients["orbits"])
    }
    return [index_by_orbit[orbit_key(item["orbit"])]
            for item in support_orbits]


def row_edge(row, signature_row, coefficients):
    support = signature_row["support_orbits"]
    indices = support_indices(coefficients, support)
    if len(indices) != 2:
        return {
            "target": int(row["target"]),
            "edge_success": False,
            "reason": "support was not a two-orbit edge",
        }

    x = coefficients["first_three"]
    y = coefficients["full"]
    i, j = indices
    dx = float(x[j] - x[i])
    dy = float(y[j] - y[i])
    if abs(dx) <= TOLERANCE:
        return {
            "target": int(row["target"]),
            "edge_success": False,
            "reason": "support first-three coordinates are degenerate",
        }

    slope = dy / dx
    intercept = float(y[i] - slope * x[i])
    gaps = y - (slope * x + intercept)
    support_gap_abs = [abs(float(gaps[index])) for index in indices]
    non_support_mask = np.ones(len(gaps), dtype=bool)
    non_support_mask[indices] = False
    positive_non_support_gaps = [
        float(value) for value in gaps[non_support_mask]
        if value > GAP_TOLERANCE
    ]
    near_zero_count = int(np.sum(np.abs(gaps) <= GAP_TOLERANCE))

    lower_edge_value = float(slope * row["actual_first_three"] + intercept)
    edge_formula_error = abs(lower_edge_value - float(row["lower_face_full"]))
    actual_edge_gap = float(row["actual_full"] - lower_edge_value)
    required_edge_gap = max(0.0, -lower_edge_value)
    rescue_ratio = (
        actual_edge_gap / required_edge_gap
        if required_edge_gap > TOLERANCE else None)

    return {
        "target": int(row["target"]),
        "target_residue": int(row["target_residue"]),
        "target_mod_286": int(row["target_mod_286"]),
        "block_index_after_discovery": int(
            row["block_index_after_discovery"]),
        "edge_success": True,
        "support_indices": [int(index) for index in indices],
        "support_orbits": support,
        "slope": float(slope),
        "intercept": float(intercept),
        "support_first_three_span": abs(dx),
        "support_full_span": abs(dy),
        "lower_edge_value_at_actual_f3": lower_edge_value,
        "lower_face_full": float(row["lower_face_full"]),
        "edge_formula_error": edge_formula_error,
        "minimum_gap_over_all_orbits": float(np.min(gaps)),
        "support_gap_error": max(support_gap_abs),
        "near_zero_gap_orbit_count": near_zero_count,
        "minimum_positive_non_support_gap": (
            min(positive_non_support_gaps)
            if positive_non_support_gaps else None),
        "actual_first_three": float(row["actual_first_three"]),
        "actual_full": float(row["actual_full"]),
        "actual_edge_gap": actual_edge_gap,
        "required_edge_gap_for_positivity": required_edge_gap,
        "edge_gap_rescue_ratio": rescue_ratio,
        "edge_gap_margin_after_rescue": (
            actual_edge_gap - required_edge_gap),
        "actual_surplus_above_lower_face": float(
            row["actual_surplus_above_lower_face"]),
        "actual_mass_on_lower_face_support": float(
            row["actual_mass_on_lower_face_support"]),
    }


def build_receipt():
    overlap = load_json(OVERLAP_SOURCE)
    signatures = load_json(SIGNATURE_SOURCE)
    signature_by_target = {
        int(row["target"]): row for row in signatures["target_rows"]
    }

    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)

    target_rows = []
    for row in overlap["target_rows"]:
        coefficients = coefficient_row(
            int(row["target_residue"]),
            context,
            full_coefficients,
            first_three_coefficients,
        )
        target_rows.append(row_edge(
            row, signature_by_target[int(row["target"])], coefficients))

    valid = [row for row in target_rows if row["edge_success"]]
    post = [row for row in valid if row["block_index_after_discovery"] >= 1]
    discovery = [
        row for row in valid if row["block_index_after_discovery"] < 1]

    def summarize(bucket):
        return {
            "row_count": len(bucket),
            "edge_formula_error_summary": finite_summary(
                row["edge_formula_error"] for row in bucket),
            "minimum_gap_over_all_orbits_summary": finite_summary(
                row["minimum_gap_over_all_orbits"] for row in bucket),
            "support_gap_error_summary": finite_summary(
                row["support_gap_error"] for row in bucket),
            "near_zero_gap_orbit_count_summary": finite_summary(
                row["near_zero_gap_orbit_count"] for row in bucket),
            "minimum_positive_non_support_gap_summary": finite_summary(
                row["minimum_positive_non_support_gap"] for row in bucket),
            "required_edge_gap_for_positivity_summary": finite_summary(
                row["required_edge_gap_for_positivity"] for row in bucket),
            "actual_edge_gap_summary": finite_summary(
                row["actual_edge_gap"] for row in bucket),
            "edge_gap_rescue_ratio_summary": finite_summary(
                row["edge_gap_rescue_ratio"] for row in bucket),
            "edge_gap_margin_after_rescue_summary": finite_summary(
                row["edge_gap_margin_after_rescue"] for row in bucket),
            "slope_summary": finite_summary(row["slope"] for row in bucket),
            "support_first_three_span_summary": finite_summary(
                row["support_first_three_span"] for row in bucket),
        }

    post_ratio_rows = sorted(
        (row for row in post if row["edge_gap_rescue_ratio"] is not None),
        key=lambda item: (item["edge_gap_rescue_ratio"], item["target"]))
    summary = {
        "target_row_count": len(target_rows),
        "valid_edge_row_count": len(valid),
        "post_discovery_target_count": len(post),
        "discovery_target_count": len(discovery),
        "invalid_edge_rows": [row for row in target_rows
                              if not row["edge_success"]],
        "all_rows": summarize(valid),
        "post_discovery_rows": summarize(post),
        "discovery_rows": summarize(discovery),
        "tightest_post_discovery_edge_rescue_rows": post_ratio_rows[:20],
        "post_rows_with_edge_gap_rescue_ratio_above_one": sum(
            row["edge_gap_rescue_ratio"] is not None
            and row["edge_gap_rescue_ratio"] > 1.0
            for row in post),
    }

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "lower_face_overlap_audit": str(OVERLAP_SOURCE.relative_to(ROOT)),
            "lower_face_support_signature_audit": str(
                SIGNATURE_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite lower-face dual-edge diagnostic only; no dual-edge "
            "theorem, signed prime-correlation theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"
        ),
        "goldbach_proved": False,
        "lower_face_dual_edge_theorem_proved": False,
        "curiosity_status": "aha-candidate",
        "novelty_label": "new-to-this-task",
        "candidate": {
            "mechanism": (
                "The LP lower-face optimizer is an affine lower edge in the "
                "(F3, Full) coefficient plane.  Full positivity is equivalent "
                "on these rows to actual prime-pair mass supplying more "
                "expected edge gap than the negative lower-edge value."
            ),
            "prediction": (
                "Held-out post-boundary rows should keep a valid affine lower "
                "edge and edge-gap rescue ratio above 1, with the tightest "
                "rows near the already observed margin."
            ),
            "falsifier": (
                "A post-boundary row with edge-gap rescue ratio <= 1, or with "
                "an invalid lower-edge certificate at the LP support, refutes "
                "this sufficient bridge in the tested q286 class."
            ),
            "smallest_next_test": (
                "Freeze the dual-edge formula and test the next predeclared "
                "q286 tail windows without changing the edge selector."
            ),
        },
        "decision": (
            "The lower-face bridge can be restated as a dual affine edge-gap "
            "rescue inequality.  This is sharper than a residue selector: the "
            "post-discovery rescue ratio is positive on every checked row but "
            "near-sharp at the weakest row, so the remaining theorem must "
            "control a pointwise signed binary-prime edge-gap expectation."
        ),
        "summary": summary,
        "target_rows": target_rows,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
