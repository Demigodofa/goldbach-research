"""Build the K_286 zero-residue raw theorem-payment schedule.

The zero-residue raw probe showed that the previously unsampled
N == 0 mod 286 lane is not an immediate finite failure.  This receipt turns
that lane into an exact coefficient-payment schedule: for each of the 35 period
residues modulo 10010 that lie over 0 mod 286, compute the local main term and
the sufficient uniform residue-discrepancy cap

    eta_a = local_main(a) / sum_d ||c_d||_1.

This is coefficient algebra and theorem-target sharpening only.  It proves no
binary-prime discrepancy theorem and no Goldbach theorem.
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
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
ZERO_PROBE_SOURCE = (
    EVIDENCE / "q286-wbss-k286-zero-residue-raw-horizon-probe.json")
OUT = EVIDENCE / "q286-wbss-k286-zero-residue-raw-budget-schedule.json"
PERIOD = 10010
MODULUS = 286

sys.path.insert(0, str(ROOT))

from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    orbit_coefficients,
    period_full_unit_coefficients,
    prepare_support_context,
    q286_first_three_unit_coefficients,
)
from tools.build_q286_wbss_four_modulus_direct_holdout_decomposition import (  # noqa: E402
    coefficient_lookup,
)
from tools.build_q286_wbss_four_modulus_variance_scale_far_lift_holdout import (  # noqa: E402
    orbit_formula_values,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def probe_rows_by_residue(zero_probe):
    by_residue = {}
    for row in zero_probe["finite_probe"]["rows"]:
        by_residue.setdefault(int(row["target_residue"]), []).append(row)
    return by_residue


def local_main_for_residue(target_residue, context, full_coefficients,
                           first_three_coefficients, alpha0, by_modulus):
    orbit_data = orbit_coefficients(
        target_residue,
        context,
        full_coefficients,
        first_three_coefficients,
    )
    uniform_mass = np.asarray(
        orbit_data["uniform_orbit_mass"], dtype=np.float64)
    phi = np.asarray(
        orbit_formula_values(orbit_data["orbits"], alpha0, by_modulus),
        dtype=np.float64)
    return {
        "local_uniform_main_term": float(np.dot(uniform_mass, phi)),
        "reflection_orbit_count": len(orbit_data["orbits"]),
        "admissible_unit_count": int(sum(len(orbit)
                                         for orbit in orbit_data["orbits"])),
    }


def summarize_probe_rows(rows):
    if not rows:
        return {
            "probe_row_count": 0,
            "largest_raw_adverse_drag_ratio": None,
            "tightest_raw_adverse_gate_gap": None,
            "smallest_raw_adverse_gate_gap_over_target": None,
        }
    return {
        "probe_row_count": len(rows),
        "largest_raw_adverse_drag_ratio": max(
            row["raw_adverse_drag_ratio"] for row in rows),
        "tightest_raw_adverse_gate_gap": min(
            row["raw_adverse_gate_gap"] for row in rows),
        "smallest_raw_adverse_gate_gap_over_target": min(
            row["raw_adverse_gate_gap_over_target"] for row in rows),
        "targets": [int(row["target"]) for row in rows],
    }


def build_receipt():
    formula = load_json(FORMULA_SOURCE)
    zero_probe = load_json(ZERO_PROBE_SOURCE)
    alpha0, by_modulus = coefficient_lookup(formula)
    projection_budget = formula["projection_error_budget"]
    l1_by_modulus = {
        str(modulus): float(value)
        for modulus, value in projection_budget[
            "l1_norm_by_modulus"].items()
    }
    total_l1 = math.fsum(l1_by_modulus.values())
    global_cap = float(projection_budget[
        "sufficient_uniform_projection_error_bound"])
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    probe_by_residue = probe_rows_by_residue(zero_probe)

    rows = []
    for residue_index in range(PERIOD // MODULUS):
        target_residue = residue_index * MODULUS
        local = local_main_for_residue(
            target_residue,
            context,
            full_coefficients,
            first_three_coefficients,
            alpha0,
            by_modulus,
        )
        local_main = local["local_uniform_main_term"]
        uniform_cap = local_main / total_l1
        probe_summary = summarize_probe_rows(
            probe_by_residue.get(target_residue, []))
        rows.append({
            "target_residue": target_residue,
            "target_mod_286": target_residue % MODULUS,
            "period_residue_index": residue_index,
            "local_uniform_main_term": local_main,
            "admissible_unit_count": local["admissible_unit_count"],
            "reflection_orbit_count": local["reflection_orbit_count"],
            "total_l1_norm": total_l1,
            "uniform_residue_error_cap": uniform_cap,
            "cap_relaxation_factor_vs_global_cap": uniform_cap / global_cap,
            "per_modulus_equal_caps": {
                modulus: local_main / l1
                for modulus, l1 in l1_by_modulus.items()
            },
            "probe_summary": probe_summary,
        })

    tightest = min(
        rows, key=lambda row: (
            row["uniform_residue_error_cap"], row["target_residue"]))
    loosest = max(
        rows, key=lambda row: (
            row["uniform_residue_error_cap"], -row["target_residue"]))
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-zero-residue-raw-budget-schedule",
        "source_commit": source_commit(),
        "sources": {
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "four_modulus_projection_formula_source_commit": (
                formula["source_commit"]),
            "zero_residue_raw_horizon_probe": str(
                ZERO_PROBE_SOURCE.relative_to(ROOT)),
            "zero_residue_raw_horizon_probe_source_commit": (
                zero_probe["source_commit"]),
        },
        "status": "TARGET_zero_residue_raw_discrepancy_budget_schedule_unproved",
        "question": (
            "For the necessary N == 0 mod 286 lane, what exact uniform "
            "residue-discrepancy payment would be sufficient for the raw "
            "adverse-drag theorem?"),
        "answer": (
            "The zero-residue lane is not worse than the all-residue global "
            "budget under the crude residue-L1 payment.  Its tightest period "
            "residues are 9724 and 286 mod 10010, with local main about "
            "0.714001940193 and uniform cap about 0.00191440934, which is "
            "about 1.18225 times looser than the global all-residue cap "
            "0.001619294659."),
        "definitions": {
            "uniform_residue_error_cap": (
                "eta_a=local_main(a)/sum_d ||c_d||_1.  If every projected "
                "residue discrepancy in the four-modulus package is bounded "
                "by eta_a for N in this period class, then "
                "A_raw_-(N)<L_raw(N) follows after raw scaling by T_N."),
            "role": (
                "A sufficient theorem-payment schedule, not a necessary "
                "condition and not finite acceptance."),
        },
        "coefficient_l1_budget": {
            "l1_norm_by_modulus": l1_by_modulus,
            "total_l1_norm": total_l1,
            "global_all_residue_uniform_cap": global_cap,
        },
        "zero_residue_schedule": {
            "target_mod_286": 0,
            "period": PERIOD,
            "period_residue_count": len(rows),
            "local_main_summary": finite_summary(
                row["local_uniform_main_term"] for row in rows),
            "uniform_cap_summary": finite_summary(
                row["uniform_residue_error_cap"] for row in rows),
            "cap_relaxation_vs_global_summary": finite_summary(
                row["cap_relaxation_factor_vs_global_cap"] for row in rows),
            "tightest_budget_row": tightest,
            "loosest_budget_row": loosest,
            "rows": rows,
        },
        "comparison_to_global_budget": {
            "zero_lane_tightest_cap": tightest[
                "uniform_residue_error_cap"],
            "global_all_residue_cap": global_cap,
            "zero_lane_tightest_cap_relaxation_factor": (
                tightest["uniform_residue_error_cap"] / global_cap),
            "zero_lane_is_worse_than_global_l1_budget": (
                tightest["uniform_residue_error_cap"] < global_cap),
            "interpretation": (
                "Under the blunt residue-L1 sufficient condition, the "
                "zero-residue no-reflection-discount lane is not the worst "
                "analytic payment.  Therefore the K_286 reflection obstruction "
                "is not captured by this crude total-L1 budget; a proof still "
                "needs signed/character moment control or a direct raw witness "
                "estimate."),
        },
        "candidate": {
            "name": "zero-residue raw discrepancy payment schedule",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Separate the necessary N==0 mod 286 lane into its 35 period "
                "residues and compute the exact local-main/L1 payment for "
                "each rather than inheriting the all-residue worst case."),
            "prediction": (
                "If zero-residue is the true analytic bottleneck in a blunt "
                "L1 theorem, its uniform cap should be tighter than the "
                "global all-residue cap."),
            "falsifier": (
                "If the zero-lane caps are all looser than the global cap, "
                "then the no-reflection-discount geometry is not visible in "
                "this crude residue-L1 payment."),
            "smallest_next_action": (
                "Stop treating blunt residue-L1 as the active explanation for "
                "the K_286 obstruction; target signed character moments or a "
                "direct raw witness theorem for N==0 mod 286."),
        },
        "decision": (
            "TARGET_zero_residue_raw_discrepancy_budget_schedule_unproved.  "
            "The exact zero-residue L1 payment schedule is now pinned.  It "
            "does not prove any prime-pair discrepancy theorem, but it shows "
            "that the zero lane is not worse than the global all-residue cap "
            "under the crude residue-L1 sufficient condition.  The K_286 "
            "no-reflection-discount difficulty therefore needs a sharper "
            "signed/character or direct raw-witness theorem, not more blunt "
            "L1 calibration."),
        "status_boundary": (
            "Coefficient-payment schedule only.  No zero-residue raw "
            "adverse-drag theorem, no universal pointwise raw estimate, no "
            "binary-prime moment theorem, no q286 threshold theorem, no "
            "strict-central Goldbach theorem, and no Goldbach proof is "
            "established."),
        "zero_residue_raw_adverse_drag_theorem_proved": False,
        "universal_pointwise_raw_bound_proved": False,
        "binary_prime_moment_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    schedule = receipt["zero_residue_schedule"]
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "period_residue_count": schedule["period_residue_count"],
        "tightest_target_residue": schedule["tightest_budget_row"][
            "target_residue"],
        "tightest_uniform_cap": schedule["tightest_budget_row"][
            "uniform_residue_error_cap"],
        "global_all_residue_cap": receipt["coefficient_l1_budget"][
            "global_all_residue_uniform_cap"],
        "zero_lane_is_worse_than_global_l1_budget": receipt[
            "comparison_to_global_budget"][
                "zero_lane_is_worse_than_global_l1_budget"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
