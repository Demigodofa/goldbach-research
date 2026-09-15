"""Audit actual q286 landing against the lower-envelope optimizer.

The max-density cone failed because actual prime-pair measures are naturally
concentrated.  This receipt tests a face-relative question instead.  For each
pre-existing tight row, solve the coefficient-only lower-envelope LP at the
row's observed first-three value, then compare the actual strict-central
prime-pair measure to that optimizer:

    min Full(lambda)
    subject to lambda >= 0, sum lambda = 1, F3(lambda) = F3(mu_N).

The proof hook is no longer "actual mass is close to uniform."  It is:
actual mass does not sit on the lower face; the transport from lower-face
mass to actual mass creates enough Full surplus.

Finite diagnostic only.  It proves no lower-face overlap theorem, signed
prime-correlation estimate, q286 threshold theorem, or Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-lower-face-overlap-audit.json"
NONPRINCIPAL_SOURCE = EVIDENCE / "q286-nonprincipal-drag-envelope-audit.json"
CONVEX_SOURCE = EVIDENCE / "q286-convex-envelope-obstruction-audit.json"
PERIOD = 10010
MODULUS = 286
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
from tools.build_q286_convex_envelope_obstruction_audit import (  # noqa: E402
    actual_source_rows,
    finite_summary,
    json_ready,
    load_json,
)
from tools.build_q286_max_density_anti_extremality_audit import (  # noqa: E402
    effective_support,
    entropy,
)
from tools.build_q286_prime_indexed_kernel_route_audit import (  # noqa: E402
    logs,
    prime_indexed_residue_weights,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def coefficient_row(target_residue, context, full_coefficients,
                    first_three_coefficients):
    orbit_data = orbit_coefficients(
        target_residue, context, full_coefficients, first_three_coefficients)
    return {
        "target_residue": int(target_residue),
        "target_mod_286": int(target_residue % MODULUS),
        "orbits": orbit_data["orbits"],
        "uniform": np.asarray(
            orbit_data["uniform_orbit_mass"], dtype=np.float64),
        "first_three": np.asarray(
            orbit_data["first_three_coefficients"], dtype=np.float64),
        "full": np.asarray(
            orbit_data["full_coefficients"], dtype=np.float64),
    }


def solve_lower_face(coefficients, first_three_value):
    count = len(coefficients["full"])
    a_eq = np.vstack((
        np.ones(count, dtype=np.float64),
        coefficients["first_three"],
    ))
    result = linprog(
        coefficients["full"],
        A_eq=a_eq,
        b_eq=np.asarray([1.0, first_three_value], dtype=np.float64),
        bounds=[(0.0, None)] * count,
        method="highs",
    )
    row = {
        "success": bool(result.success),
        "status": int(result.status),
        "message": result.message,
    }
    if not result.success:
        return row
    masses = np.asarray(result.x, dtype=np.float64)
    row.update({
        "masses": masses,
        "first_three": float(np.dot(coefficients["first_three"], masses)),
        "full": float(np.dot(coefficients["full"], masses)),
        "support_size": int(np.sum(masses > TOLERANCE)),
        "entropy": entropy(masses),
        "effective_support": effective_support(masses),
    })
    return row


def actual_orbit_measure(target, coefficients, primes, prime_values, log_values):
    count, total, weights = prime_indexed_residue_weights(
        target, primes, prime_values, log_values, PERIOD)
    if total <= TOLERANCE:
        raise ValueError(f"target {target} has no strict-central pair mass")
    residue_measure = np.asarray(weights, dtype=np.float64) / float(total)
    orbit_masses = np.asarray([
        math.fsum(float(residue_measure[unit]) for unit in orbit)
        for orbit in coefficients["orbits"]
    ], dtype=np.float64)
    return {
        "pair_count": int(count),
        "total_weight": float(total),
        "masses": orbit_masses,
        "first_three": float(np.dot(coefficients["first_three"], orbit_masses)),
        "full": float(np.dot(coefficients["full"], orbit_masses)),
        "entropy": entropy(orbit_masses),
        "effective_support": effective_support(orbit_masses),
    }


def signed_transport_summary(coefficients, actual, lower):
    delta = actual["masses"] - lower["masses"]
    full_coeff = coefficients["full"]
    first_three_coeff = coefficients["first_three"]
    contributions = delta * full_coeff
    positive = float(math.fsum(
        value for value in contributions if value > 0.0))
    negative = float(math.fsum(
        -value for value in contributions if value < 0.0))
    lower_support = lower["masses"] > TOLERANCE
    overlap = float(np.sum(np.minimum(actual["masses"], lower["masses"])))
    tv = float(0.5 * np.sum(np.abs(delta)))
    return {
        "total_variation_from_lower_face": tv,
        "overlap_with_lower_face_measure": overlap,
        "actual_mass_on_lower_face_support": float(
            np.sum(actual["masses"][lower_support])),
        "lower_face_support_size": int(np.sum(lower_support)),
        "lower_face_effective_support": lower["effective_support"],
        "actual_effective_support": actual["effective_support"],
        "actual_entropy_minus_lower_entropy": (
            actual["entropy"] - lower["entropy"]),
        "transport_full_positive_contribution": positive,
        "transport_full_negative_drag": negative,
        "transport_full_surplus": positive - negative,
        "transport_first_three_error": abs(float(np.dot(
            first_three_coeff, delta))),
        "transport_full_error": abs(
            (positive - negative) - (actual["full"] - lower["full"])),
        "positive_to_negative_transport_ratio": (
            positive / negative if negative > TOLERANCE else None),
        "largest_actual_minus_lower_orbits": tuple(
            {
                "orbit": coefficients["orbits"][index],
                "delta_mass": float(delta[index]),
                "actual_mass": float(actual["masses"][index]),
                "lower_mass": float(lower["masses"][index]),
                "first_three_coefficient": float(first_three_coeff[index]),
                "full_coefficient": float(full_coeff[index]),
                "full_transport_contribution": float(contributions[index]),
            }
            for index in np.argsort(-delta)[:10]
            if delta[index] > TOLERANCE),
        "largest_lower_minus_actual_orbits": tuple(
            {
                "orbit": coefficients["orbits"][index],
                "delta_mass": float(delta[index]),
                "actual_mass": float(actual["masses"][index]),
                "lower_mass": float(lower["masses"][index]),
                "first_three_coefficient": float(first_three_coeff[index]),
                "full_coefficient": float(full_coeff[index]),
                "full_transport_contribution": float(contributions[index]),
            }
            for index in np.argsort(delta)[:10]
            if delta[index] < -TOLERANCE),
    }


def analyze_target(row, coefficients, primes, prime_values, log_values):
    target = int(row["target"])
    actual = actual_orbit_measure(
        target, coefficients, primes, prime_values, log_values)
    lower = solve_lower_face(coefficients, actual["first_three"])
    if not lower["success"]:
        return {
            "target": target,
            "target_residue": int(target % PERIOD),
            "target_mod_286": int(row["target_mod_286"]),
            "lower_face_success": False,
            "lower_face_status": lower["status"],
            "lower_face_message": lower["message"],
        }
    transport = signed_transport_summary(coefficients, actual, lower)
    return {
        "target": target,
        "target_residue": int(target % PERIOD),
        "target_mod_286": int(row["target_mod_286"]),
        "block_index_after_discovery": int(row["block_index_after_discovery"]),
        "pair_count": actual["pair_count"],
        "total_weight": actual["total_weight"],
        "actual_first_three": actual["first_three"],
        "actual_full": actual["full"],
        "lower_face_first_three": lower["first_three"],
        "lower_face_full": lower["full"],
        "actual_surplus_above_lower_face": actual["full"] - lower["full"],
        "actual_full_positive": bool(actual["full"] > TOLERANCE),
        **transport,
    }


def build_receipt():
    rows = actual_source_rows(load_json(NONPRINCIPAL_SOURCE))
    convex = load_json(CONVEX_SOURCE)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    residues = tuple(dict.fromkeys(int(row["target"]) % PERIOD for row in rows))
    coefficient_by_residue = {
        residue: coefficient_row(
            residue, context, full_coefficients, first_three_coefficients)
        for residue in residues
    }
    maximum_target = max(int(row["target"]) for row in rows)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    target_rows = tuple(
        analyze_target(
            row, coefficient_by_residue[int(row["target"]) % PERIOD],
            primes, prime_values, log_values)
        for row in rows)
    post_rows = tuple(
        row for row in target_rows
        if row.get("block_index_after_discovery", 0) >= 1)
    discovery_rows = tuple(
        row for row in target_rows
        if row.get("block_index_after_discovery", 0) == 0)
    valid_rows = tuple(row for row in target_rows if row.get(
        "lower_face_support_size") is not None)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "nonprincipal_drag_envelope": str(
                NONPRINCIPAL_SOURCE.relative_to(ROOT)),
            "convex_envelope_obstruction": str(
                CONVEX_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite lower-face overlap diagnostic only; it proves no "
            "lower-face overlap theorem, signed prime-correlation estimate, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach theorem."),
        "candidate_cone": {
            "name": "q286 lower-face overlap/transport cone",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "At fixed observed F3, the coefficient-only lower face is the "
                "worst Full arrangement.  Actual prime-pair measures may be "
                "certified by limited overlap with that lower-face optimizer "
                "or by positive signed transport away from it."),
            "prediction": (
                "Actual post-discovery rows should have substantial total "
                "variation from the lower-face optimizer and positive "
                "transport surplus."),
            "falsifier": (
                "If actual positive post-discovery rows have high lower-face "
                "overlap and no positive transport surplus, this face-relative "
                "cone is not the right mechanism."),
            "smallest_test": (
                "Use the same pre-existing tight rows as the convex-envelope "
                "audit; solve the lower-envelope LP at each observed F3 and "
                "decompose actual-minus-lower-face transport."),
        },
        "target_rows": target_rows,
        "prior_convex_summary": convex["summary"],
        "summary": {
            "target_row_count": len(target_rows),
            "valid_target_row_count": len(valid_rows),
            "post_discovery_target_count": len(post_rows),
            "discovery_target_count": len(discovery_rows),
            "lower_face_support_size_summary": finite_summary(
                row.get("lower_face_support_size") for row in valid_rows),
            "actual_mass_on_lower_face_support_summary": finite_summary(
                row.get("actual_mass_on_lower_face_support")
                for row in valid_rows),
            "post_discovery_actual_mass_on_lower_face_support_summary":
                finite_summary(
                    row.get("actual_mass_on_lower_face_support")
                    for row in post_rows),
            "total_variation_from_lower_face_summary": finite_summary(
                row.get("total_variation_from_lower_face")
                for row in valid_rows),
            "post_discovery_total_variation_from_lower_face_summary":
                finite_summary(
                    row.get("total_variation_from_lower_face")
                    for row in post_rows),
            "actual_surplus_above_lower_face_summary": finite_summary(
                row.get("actual_surplus_above_lower_face")
                for row in valid_rows),
            "post_discovery_actual_surplus_above_lower_face_summary":
                finite_summary(
                    row.get("actual_surplus_above_lower_face")
                    for row in post_rows),
            "transport_positive_to_negative_ratio_summary": finite_summary(
                row.get("positive_to_negative_transport_ratio")
                for row in valid_rows),
            "post_discovery_transport_positive_to_negative_ratio_summary":
                finite_summary(
                    row.get("positive_to_negative_transport_ratio")
                    for row in post_rows),
            "transport_error_summary": finite_summary(
                max(row.get("transport_first_three_error", 0.0),
                    row.get("transport_full_error", 0.0))
                for row in valid_rows),
            "tightest_post_discovery_surplus_rows": tuple(sorted(
                post_rows,
                key=lambda item: (
                    item["actual_surplus_above_lower_face"],
                    item["target"]))[:20]),
            "largest_post_discovery_lower_support_overlap_rows": tuple(sorted(
                post_rows,
                key=lambda item: (
                    -item["actual_mass_on_lower_face_support"],
                    item["target"]))[:20]),
            "weakest_post_discovery_transport_ratio_rows": tuple(sorted(
                (
                    row for row in post_rows
                    if row.get("positive_to_negative_transport_ratio")
                    is not None),
                key=lambda item: (
                    item["positive_to_negative_transport_ratio"],
                    item["target"]))[:20]),
        },
        "decision": (
            "If actual rows have low overlap with the lower-face support and "
            "positive signed transport surplus, the next theorem candidate "
            "can be stated relative to the lower envelope rather than "
            "relative to uniform.  If not, demote this cone too."),
        "next_obligation": (
            "Turn the best surviving face-relative metric into a non-post-hoc "
            "arithmetic inequality, or show that it is only a restatement of "
            "the hard signed binary-prime correlation estimate."),
        "lower_face_overlap_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "q286_threshold_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    payload = build_receipt()
    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(json.dumps({
        "wrote": str(OUT.relative_to(ROOT)),
        "target_row_count": payload["summary"]["target_row_count"],
        "valid_target_row_count": payload["summary"]["valid_target_row_count"],
        "post_discovery_target_count": (
            payload["summary"]["post_discovery_target_count"]),
        "goldbach_proved": payload["goldbach_proved"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
