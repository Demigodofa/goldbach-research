"""Find which q286-WBSS tail support marginals close the dominant cone gap.

The marginal-cone audit showed that exact dominant support projections
modulo 70, 154, and 286 force positivity on 21/24 stress rows but fail on
three rows.  Exact projections to all coefficient supports force positivity
on 24/24 rows.

This receipt tests every subset of the remaining tail supports:

    10, 14, 22, 26, 130

added to the dominant supports.  A subset is useful only if the LP minimum
signed expectation is positive for every stress row and both coefficient
families.  This separates a small tail-control theorem target from the
coefficient-complete restatement.

Finite LP cone audit only.  It proves no tail-support projection theorem,
signed discrepancy theorem, q286 threshold theorem, strict-central Goldbach
theorem, or Goldbach theorem.
"""

from __future__ import annotations

import itertools
import json
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
MARGINAL_SOURCE = EVIDENCE / "q286-wbss-marginal-cone-gap-audit.json"
DUAL_SOURCE = EVIDENCE / "q286-lower-face-dual-edge-audit.json"
OUT = EVIDENCE / "q286-wbss-tail-support-minimal-cone-audit.json"
DOMINANT = (70, 154, 286)
TAIL = (10, 14, 22, 26, 130)
TOLERANCE = 1e-9

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    orbit_coefficients,
    period_full_unit_coefficients,
    prepare_support_context,
    q286_first_three_unit_coefficients,
)
from tools.build_q286_lower_face_overlap_audit import actual_orbit_measure  # noqa: E402
from tools.build_q286_prime_indexed_kernel_route_audit import logs  # noqa: E402
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402
from tools.build_q286_wbss_marginal_cone_gap_audit import (  # noqa: E402
    equality_system,
    solve_minimum_expectation,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def tail_subsets():
    for size in range(len(TAIL) + 1):
        for subset in itertools.combinations(TAIL, size):
            yield subset


def build_problem_rows():
    marginal = load_json(MARGINAL_SOURCE)
    dual = load_json(DUAL_SOURCE)
    targets = tuple(int(target) for target in marginal["selected_targets"])
    dual_by_target = {
        int(row["target"]): row
        for row in dual["target_rows"]
        if row["edge_success"]
    }
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    primes = np.asarray(_prime_table(max(targets)), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(max(targets))

    rows = []
    for target in targets:
        edge_row = dual_by_target[target]
        orbit_data = orbit_coefficients(
            int(edge_row["target_residue"]),
            context,
            full_coefficients,
            first_three_coefficients,
        )
        coefficients = {
            "orbits": orbit_data["orbits"],
            "first_three": np.asarray(
                orbit_data["first_three_coefficients"], dtype=np.float64),
            "full": np.asarray(
                orbit_data["full_coefficients"], dtype=np.float64),
        }
        actual = actual_orbit_measure(
            target, coefficients, primes, prime_values, log_values)
        actual_mass = np.asarray(actual["masses"], dtype=np.float64)
        slope = float(edge_row["slope"])
        intercept = float(edge_row["intercept"])
        required = float(edge_row["required_edge_gap_for_positivity"])
        gap = coefficients["full"] - (slope * coefficients["first_three"]
                                      + intercept)
        rows.append({
            "target": target,
            "target_residue": int(edge_row["target_residue"]),
            "target_mod_286": int(edge_row["target_mod_286"]),
            "orbits": orbit_data["orbits"],
            "actual_mass": actual_mass,
            "actual_pair_count": int(actual["pair_count"]),
            "families": {
                "full": coefficients["full"],
                "edge_beta": gap - required,
            },
        })
    return rows


def evaluate_subset(problem_rows, subset):
    moduli = tuple(sorted(set(DOMINANT + tuple(subset))))
    family_rows = {}
    for family in ("full", "edge_beta"):
        rows = []
        for row in problem_rows:
            solved = solve_minimum_expectation(
                row["orbits"], row["actual_mass"], row["families"][family],
                moduli)
            a_eq, _, _ = equality_system(
                row["orbits"], row["actual_mass"], moduli)
            span_solution, *_ = np.linalg.lstsq(
                a_eq.T, row["families"][family], rcond=None)
            span_residual = row["families"][family] - a_eq.T @ span_solution
            span_scale = max(1.0, float(np.linalg.norm(
                row["families"][family])))
            if not solved["lp_success"]:
                raise RuntimeError(
                    f"LP failed for {family} {row['target']} {moduli}: "
                    f"{solved['lp_message']}")
            rows.append({
                "target": row["target"],
                "target_residue": row["target_residue"],
                "target_mod_286": row["target_mod_286"],
                "minimum_signed_expectation": (
                    solved["minimum_signed_expectation"]),
                "bad_measure_feasible": solved["bad_measure_feasible"],
                "synthetic_l1_from_actual": solved[
                    "synthetic_l1_from_actual"],
                "coefficient_projection_span_relative_l2_residual": float(
                    np.linalg.norm(span_residual) / span_scale),
                "coefficient_projection_span_max_abs_residual": float(
                    np.max(np.abs(span_residual))),
            })
        bad_rows = [row for row in rows if row["bad_measure_feasible"]]
        family_rows[family] = {
            "bad_measure_feasible_count": len(bad_rows),
            "positive_forced_count": len(rows) - len(bad_rows),
            "minimum_signed_expectation_summary": finite_summary(
                row["minimum_signed_expectation"] for row in rows),
            "bad_targets": [row["target"] for row in bad_rows],
            "coefficient_projection_span_relative_l2_residual_summary":
                finite_summary(
                    row["coefficient_projection_span_relative_l2_residual"]
                    for row in rows),
            "coefficient_projection_span_max_abs_residual_summary":
                finite_summary(
                    row["coefficient_projection_span_max_abs_residual"]
                    for row in rows),
            "tightest_row": min(
                rows, key=lambda row: row["minimum_signed_expectation"]),
        }
    return {
        "tail_subset": list(subset),
        "moduli": list(moduli),
        "tail_subset_size": len(subset),
        "families": family_rows,
        "bad_measure_feasible_count_both_families": max(
            family_rows["full"]["bad_measure_feasible_count"],
            family_rows["edge_beta"]["bad_measure_feasible_count"]),
        "forces_both_families_positive": (
            family_rows["full"]["bad_measure_feasible_count"] == 0
            and family_rows["edge_beta"]["bad_measure_feasible_count"] == 0),
    }


def per_target_minimal_closers(subset_rows):
    result = {}
    for family in ("full", "edge_beta"):
        targets = sorted({
            target
            for row in subset_rows
            for target in row["families"][family]["bad_targets"]
        } | {
            row["families"][family]["tightest_row"]["target"]
            for row in subset_rows
        })
        entries = {}
        for target in targets:
            closing = []
            for row in subset_rows:
                if target not in row["families"][family]["bad_targets"]:
                    closing.append(row["tail_subset"])
            min_size = min((len(item) for item in closing), default=None)
            entries[str(target)] = [
                item for item in closing if len(item) == min_size
            ][:12]
        result[family] = entries
    return result


def build_receipt():
    problem_rows = build_problem_rows()
    subset_rows = [evaluate_subset(problem_rows, subset)
                   for subset in tail_subsets()]
    closers = [row for row in subset_rows
               if row["forces_both_families_positive"]]
    min_closer_size = min((row["tail_subset_size"] for row in closers),
                          default=None)
    minimal_closers = [
        row for row in closers if row["tail_subset_size"] == min_closer_size
    ]
    by_size = {}
    for size in range(len(TAIL) + 1):
        group = [row for row in subset_rows if row["tail_subset_size"] == size]
        by_size[str(size)] = {
            "subset_count": len(group),
            "both_family_closer_count": sum(
                row["forces_both_families_positive"] for row in group),
            "best_bad_count_both_families": min(
                row["bad_measure_feasible_count_both_families"]
                for row in group),
            "best_subsets": [
                {
                    "tail_subset": row["tail_subset"],
                    "bad_measure_feasible_count_both_families": row[
                        "bad_measure_feasible_count_both_families"],
                    "full_span_l2_residual_max": row["families"]["full"][
                        "coefficient_projection_span_relative_l2_residual_summary"][
                            "maximum"],
                    "edge_beta_span_l2_residual_max": row[
                        "families"]["edge_beta"][
                            "coefficient_projection_span_relative_l2_residual_summary"][
                                "maximum"],
                    "full_bad_targets": row["families"]["full"]["bad_targets"],
                    "edge_beta_bad_targets": row[
                        "families"]["edge_beta"]["bad_targets"],
                }
                for row in sorted(
                    group,
                    key=lambda row: (
                        row["bad_measure_feasible_count_both_families"],
                        row["tail_subset"],
                    ),
                )[:8]
            ],
        }
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "marginal_cone_gap": str(MARGINAL_SOURCE.relative_to(ROOT)),
            "lower_face_dual_edge_audit": str(DUAL_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite tail-support minimal-cone LP audit only; no "
            "tail-support projection theorem, signed discrepancy theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"
        ),
        "goldbach_proved": False,
        "tail_support_projection_theorem_proved": False,
        "signed_discrepancy_theorem_proved": False,
        "dominant_support_moduli": list(DOMINANT),
        "tail_support_moduli": list(TAIL),
        "selected_targets": [row["target"] for row in problem_rows],
        "candidate": {
            "name": "minimal tail support closure for q286-WBSS",
            "mechanism": (
                "The coefficient energy is dominated by moduli 70, 154, and "
                "286, but the prior LP found three stress rows where those "
                "marginals alone still permit synthetic bad measures.  Add "
                "tail support projections one subset at a time to find the "
                "smallest non-renaming repair target."
            ),
            "prediction": (
                "If a small tail subset closes all stress rows, the next "
                "theorem can target dominant supports plus that named tail. "
                "If only the complete tail closes, the bridge is close to "
                "the full signed-projection problem."
            ),
            "falsifier": (
                "Any remaining bad LP optimum under a proposed subset "
                "falsifies that subset as a complete proof bridge."
            ),
        },
        "summary_by_tail_subset_size": by_size,
        "minimum_tail_subset_size_for_both_families": min_closer_size,
        "minimal_tail_subsets_for_both_families": [
            {
                "tail_subset": row["tail_subset"],
                "moduli": row["moduli"],
                "full_minimum_summary": row["families"]["full"][
                    "minimum_signed_expectation_summary"],
                "edge_beta_minimum_summary": row["families"]["edge_beta"][
                    "minimum_signed_expectation_summary"],
                "full_span_l2_residual_max": row["families"]["full"][
                    "coefficient_projection_span_relative_l2_residual_summary"][
                        "maximum"],
                "edge_beta_span_l2_residual_max": row[
                    "families"]["edge_beta"][
                        "coefficient_projection_span_relative_l2_residual_summary"][
                            "maximum"],
            }
            for row in minimal_closers
        ],
        "per_target_minimal_closers": per_target_minimal_closers(subset_rows),
        "all_subset_rows": subset_rows,
        "decision": (
            "The dominant-support crack is now a finite minimal-tail problem. "
            "A small closing subset would be a genuine narrowing; requiring "
            "every tail support would show the cone is nearly the same as "
            "the full coefficient-support projection problem."
        ),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
