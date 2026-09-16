"""Audit a full-character triangle route for the q286 residual functional.

The residual lower-tail target is

    aligned(N) + <nu_N, h_a> > 0.

One analytic escape would be to expand the target-specific residual h_a in
Dirichlet characters modulo 10010 and then control every character discrepancy
|<nu_N, chi>|.  This receipt quantifies that source theorem.  If the required
per-character discrepancy is far below the actual row's character scale, then
the full-character triangle route is too broad and the next proof object must
keep signed/structured cancellation between channels.

Finite theorem-budget audit only.  It proves no character-sum theorem, signed
binary-prime correlation theorem, q286 threshold theorem, strict-central
Goldbach theorem, or Goldbach proof.
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
RESIDUAL_SOURCE = (
    EVIDENCE / "q286-orthogonal-residual-sign-split-budget-audit.json")
OUT = EVIDENCE / "q286-residual-character-triangle-budget-audit.json"
PERIOD = 10010
FACTOR_PRIMES = (5, 7, 11, 13)
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_frequency_resolved_fourier import (  # noqa: E402
    _unit_character_table,
)
from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    SELECTED_TARGETS,
    combined_fixed_strict_central_coefficient_receipt,
    period_full_unit_coefficients,
    prepare_support_context,
    q286_first_three_unit_coefficients,
)
from tools.build_q286_lower_face_overlap_audit import (  # noqa: E402
    actual_orbit_measure,
)
from tools.build_q286_orthogonal_residual_norm_certificate import (  # noqa: E402
    residual_operator,
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


def support_label(label):
    support = tuple(
        prime for prime, exponent in zip(FACTOR_PRIMES, label)
        if exponent != 0)
    return "principal" if not support else "x".join(str(p) for p in support)


def residual_unit_values(operator, units):
    unit_index = {unit: index for index, unit in enumerate(units)}
    values = np.zeros(len(units), dtype=np.complex128)
    for residual_value, orbit in zip(
            operator["residual"], operator["orbit_data"]["orbits"]):
        for unit in orbit:
            values[unit_index[unit]] = residual_value
    return values


def actual_unit_discrepancy(target, units, primes, prime_values, log_values):
    _, total_weight, weights = prime_indexed_residue_weights(
        target, primes, prime_values, log_values, PERIOD)
    if total_weight <= TOLERANCE:
        raise AssertionError(f"target {target} has no strict-central mass")
    mu = np.asarray(weights, dtype=np.float64) / float(total_weight)
    admissible = tuple(
        unit for unit in units
        if math.gcd((target - unit) % PERIOD, PERIOD) == 1)
    uniform = np.zeros(PERIOD, dtype=np.float64)
    for unit in admissible:
        uniform[unit] = 1.0 / len(admissible)
    return np.asarray(
        [mu[unit] - uniform[unit] for unit in units], dtype=np.complex128)


def support_summaries(coefficients, labels, active):
    grouped = {}
    for coefficient, label, is_active in zip(coefficients, labels, active):
        if not is_active:
            continue
        key = support_label(label)
        row = grouped.setdefault(
            key, {"support_label": key, "character_count": 0,
                  "coefficient_l1": 0.0, "coefficient_l2_square": 0.0,
                  "coefficient_linf": 0.0})
        magnitude = abs(coefficient)
        row["character_count"] += 1
        row["coefficient_l1"] += float(magnitude)
        row["coefficient_l2_square"] += float(magnitude * magnitude)
        row["coefficient_linf"] = max(row["coefficient_linf"], float(magnitude))
    rows = []
    for row in grouped.values():
        row["coefficient_l2"] = math.sqrt(row.pop("coefficient_l2_square"))
        rows.append(row)
    rows.sort(key=lambda row: row["coefficient_l1"], reverse=True)
    return rows


def row_budget(target, operator, units, labels, character_table, primes,
               prime_values, log_values):
    residual_values = residual_unit_values(operator, units)
    coefficients = (
        np.conjugate(character_table) @ residual_values / len(units))
    reconstruction = character_table.T @ coefficients
    reconstruction_error = float(
        np.linalg.norm(reconstruction - residual_values)
        / max(1.0, float(np.linalg.norm(residual_values))))
    active = np.abs(coefficients) > TOLERANCE

    discrepancy = actual_unit_discrepancy(
        target, units, primes, prime_values, log_values)
    channel_discrepancies = character_table @ discrepancy
    signed_residual_action = float(np.real(
        np.dot(coefficients, channel_discrepancies)))
    triangle_bound = float(np.sum(
        np.abs(coefficients[active])
        * np.abs(channel_discrepancies[active])))
    l1_burden = float(np.sum(np.abs(coefficients[active])))
    l2_burden = float(np.linalg.norm(coefficients[active]))
    linf_burden = float(np.max(np.abs(coefficients[active])))
    max_actual_channel_discrepancy = float(
        np.max(np.abs(channel_discrepancies[active])))

    orbit_data = operator["orbit_data"]
    actual = actual_orbit_measure(
        target,
        {
            "orbits": orbit_data["orbits"],
            "first_three": orbit_data["first_three_coefficients"],
            "full": orbit_data["full_coefficients"],
        },
        primes,
        prime_values,
        log_values,
    )
    masses = np.asarray(actual["masses"], dtype=np.float64)
    first_three = float(np.dot(operator["first_three"], masses))
    aligned = operator["uniform_full"] + operator["alpha"] * first_three
    full = float(np.dot(operator["full"], masses))
    budget = (
        aligned / l1_burden
        if aligned > TOLERANCE and l1_burden > TOLERANCE else 0.0)
    return {
        "target": int(target),
        "target_residue": int(target % PERIOD),
        "target_mod_286": int(target % 286),
        "actual_full_action": full,
        "aligned_only_full_action": aligned,
        "signed_residual_action_from_characters": signed_residual_action,
        "character_reconstruction_error": reconstruction_error,
        "active_character_count": int(np.sum(active)),
        "total_character_count": int(len(coefficients)),
        "coefficient_l1_burden": l1_burden,
        "coefficient_l2_burden": l2_burden,
        "coefficient_linf_burden": linf_burden,
        "triangle_abs_bound_on_residual": triangle_bound,
        "triangle_bound_to_aligned_margin_ratio": (
            triangle_bound / aligned if aligned > TOLERANCE else None),
        "uniform_per_character_discrepancy_budget": budget,
        "max_actual_character_discrepancy": max_actual_channel_discrepancy,
        "max_actual_to_uniform_budget_ratio": (
            max_actual_channel_discrepancy / budget
            if budget > TOLERANCE else None),
        "triangle_bound_certifies_row": bool(
            aligned > triangle_bound + TOLERANCE),
        "actual_full_positive": bool(full > TOLERANCE),
        "support_l1_rows": support_summaries(coefficients, labels, active)[:8],
    }


def build_receipt():
    residual_source = load_json(RESIDUAL_SOURCE)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    units = tuple(
        residue for residue in range(PERIOD)
        if math.gcd(residue, PERIOD) == 1)
    _, labels, character_table = _unit_character_table(PERIOD, units)
    maximum_target = max(SELECTED_TARGETS)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    operators = {
        int(target % PERIOD): residual_operator(
            int(target % PERIOD),
            context,
            full_coefficients,
            first_three_coefficients,
        )
        for target in SELECTED_TARGETS
    }
    rows = [
        row_budget(
            int(target), operators[int(target % PERIOD)], units, labels,
            character_table, primes, prime_values, log_values)
        for target in SELECTED_TARGETS
    ]
    positive_rows = [row for row in rows if row["actual_full_positive"]]
    tight = min(
        positive_rows,
        key=lambda row: (
            row["uniform_per_character_discrepancy_budget"],
            row["target"],
        ),
    )
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "residual_sign_split_budget": str(
                RESIDUAL_SOURCE.relative_to(ROOT)),
            "residual_sign_split_source_commit": (
                residual_source["source_commit"]),
        },
        "status": "HOLD_full_character_triangle_route_too_broad",
        "status_boundary": (
            "finite residual character-budget audit only; no character-sum "
            "theorem, signed binary-prime correlation theorem, q286 threshold "
            "theorem, strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "character_sum_theorem_proved": False,
        "signed_binary_prime_correlation_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "full-period residual character triangle source theorem",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Zero-extend the target-specific residual h_a to U_10010, "
                "expand it in period characters, and use per-character "
                "bounds |<nu_N,chi>| <= eps to force "
                "<nu_N,h_a> > -aligned."),
            "prediction": (
                "If the full character route is viable, the uniform "
                "per-character discrepancy budget aligned/L1(hhat) should be "
                "comparable to actual character-discrepancy scales, and the "
                "triangle absolute bound should certify at least the easy "
                "positive rows."),
            "falsifier": (
                "If the expansion activates essentially all characters and "
                "the triangle absolute bound overwhelms the aligned margin at "
                "the tight row, the full-character theorem is too broad as an "
                "acceptance route."),
            "smallest_test": (
                "Compute the exact period-character expansion of h_a and the "
                "uniform per-character budget aligned/L1(hhat) on the seven "
                "frozen signed-pair operator targets."),
        },
        "character_convention": {
            "period": PERIOD,
            "unit_group_order": len(units),
            "expansion": (
                "h_a(u)=sum_chi c_chi chi(u) on U_10010, with h_a set to "
                "zero outside the admissible reflected support A_a."),
            "channel_discrepancy": (
                "Delta_chi(N)=sum_u (mu_N(u)-u_a(u)) chi(u)."),
            "triangle_sufficient_condition": (
                "If |Delta_chi(N)| <= eps for every active chi and "
                "eps < aligned(N)/sum|c_chi|, then full(N)>0."),
        },
        "summary": {
            "selected_target_count": len(rows),
            "actual_full_positive_count": len(positive_rows),
            "triangle_certified_positive_count": sum(
                row["triangle_bound_certifies_row"] for row in positive_rows),
            "active_character_count_summary": finite_summary(
                row["active_character_count"] for row in rows),
            "coefficient_l1_burden_summary": finite_summary(
                row["coefficient_l1_burden"] for row in rows),
            "uniform_budget_summary_on_positive_rows": finite_summary(
                row["uniform_per_character_discrepancy_budget"]
                for row in positive_rows),
            "max_actual_to_uniform_budget_ratio_summary": finite_summary(
                row["max_actual_to_uniform_budget_ratio"]
                for row in positive_rows),
            "triangle_bound_to_aligned_margin_ratio_summary": finite_summary(
                row["triangle_bound_to_aligned_margin_ratio"]
                for row in positive_rows),
            "maximum_character_reconstruction_error": max(
                row["character_reconstruction_error"] for row in rows),
            "tightest_positive_uniform_budget_row": tight,
        },
        "decision": (
            "The full-period character triangle route is too broad.  "
            "Zero-extending the target-specific residual activates nearly the "
            "entire U_10010 character basis, and the tight positive row needs "
            "a uniform per-character discrepancy budget on the order of "
            "aligned/L1(hhat), far below its actual maximum character "
            "discrepancy.  The triangle bound does not explain the tight row; "
            "progress must keep signed structure between channels, use a much "
            "smaller residual dictionary, or source a genuinely one-sided "
            "estimate for <nu_N,h_a> rather than bounding all character "
            "channels independently.  Goldbach remains open."),
        "target_rows": rows,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
