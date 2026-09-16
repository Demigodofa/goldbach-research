"""Audit observed active-character moments on the K_286 zero-residue lane.

The zero-residue character-budget schedule computed sufficient aggregate
active-character L2 caps for N == 0 mod 286.  This receipt tests those caps on
the 70-row targeted zero-residue raw probe.

Finite diagnostic only.  Passing or failing these finite caps is not proof of
an asymptotic theorem.  In particular, cap violations show that plain aggregate
L2 control is not the observed finite bridge on this lane; the raw adverse
gate can still be positive by signed structure.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
ZERO_PROBE_SOURCE = (
    EVIDENCE / "q286-wbss-k286-zero-residue-raw-horizon-probe.json")
ZERO_CHARACTER_SCHEDULE_SOURCE = (
    EVIDENCE / "q286-wbss-k286-zero-residue-character-budget-schedule.json")
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
OUT = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-observed-character-moment-audit.json")
TOLERANCE = 1e-12

sys.path.insert(0, str(ROOT))

from tools import build_q286_wbss_four_modulus_variance_scale_far_lift_holdout as far  # noqa: E501,E402
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402
from tools.build_q286_wbss_multiplicative_character_l2_observed_moment_audit import (  # noqa: E501,E402
    active_character_masks,
    row_moments,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def caps_by_residue(schedule):
    return {
        int(row["target_residue"]): row
        for row in schedule["zero_residue_character_schedule"]["rows"]
    }


def row_record(source_row, moment_row, cap_row, global_l2_cap):
    aggregate_l2 = moment_row["aggregate_character_moment_l2"]
    local_cap = cap_row["aggregate_character_l2_cap"]
    return {
        "source": source_row["source"],
        "target": int(source_row["target"]),
        "target_residue": int(source_row["target_residue"]),
        "target_mod_286": int(source_row["target_mod_286"]),
        "period_residue_index": int(cap_row["period_residue_index"]),
        "pair_count": int(source_row["pair_count"]),
        "actual_mass_sum": moment_row["actual_mass_sum"],
        "uniform_mass_sum": moment_row["uniform_mass_sum"],
        "raw_adverse_drag_ratio": source_row["raw_adverse_drag_ratio"],
        "raw_adverse_gate_gap": source_row["raw_adverse_gate_gap"],
        "raw_adverse_gate_gap_over_target": (
            source_row["raw_adverse_gate_gap_over_target"]),
        "raw_adverse_gate_gap_positive": (
            source_row["raw_adverse_gate_gap_positive"]),
        "character_moment_l2_by_modulus": (
            moment_row["character_moment_l2_by_modulus"]),
        "aggregate_character_moment_l2": aggregate_l2,
        "zero_residue_local_aggregate_l2_cap": local_cap,
        "global_aggregate_l2_cap": global_l2_cap,
        "ratio_to_zero_residue_local_l2_cap": aggregate_l2 / local_cap,
        "ratio_to_global_l2_cap": aggregate_l2 / global_l2_cap,
        "local_l2_cap_margin": local_cap - aggregate_l2,
        "exceeds_zero_residue_local_l2_cap": bool(
            aggregate_l2 > local_cap + TOLERANCE),
        "exceeds_global_l2_cap": bool(
            aggregate_l2 > global_l2_cap + TOLERANCE),
    }


def summarize_rows(rows):
    local_violations = [
        row for row in rows if row["exceeds_zero_residue_local_l2_cap"]]
    global_violations = [
        row for row in rows if row["exceeds_global_l2_cap"]]
    return {
        "row_count": len(rows),
        "target_minimum": min(row["target"] for row in rows),
        "target_maximum": max(row["target"] for row in rows),
        "zero_pair_count_rows": sum(row["pair_count"] == 0 for row in rows),
        "nonpositive_raw_adverse_gate_gap_count": sum(
            not row["raw_adverse_gate_gap_positive"] for row in rows),
        "local_l2_cap_exceeding_row_count": len(local_violations),
        "global_l2_cap_exceeding_row_count": len(global_violations),
        "aggregate_character_moment_l2_summary": finite_summary(
            row["aggregate_character_moment_l2"] for row in rows),
        "zero_residue_local_l2_cap_summary": finite_summary(
            row["zero_residue_local_aggregate_l2_cap"] for row in rows),
        "ratio_to_zero_residue_local_l2_cap_summary": finite_summary(
            row["ratio_to_zero_residue_local_l2_cap"] for row in rows),
        "ratio_to_global_l2_cap_summary": finite_summary(
            row["ratio_to_global_l2_cap"] for row in rows),
        "local_l2_cap_margin_summary": finite_summary(
            row["local_l2_cap_margin"] for row in rows),
        "largest_local_l2_ratio_row": max(
            rows,
            key=lambda row: (
                row["ratio_to_zero_residue_local_l2_cap"], -row["target"])),
        "smallest_local_l2_margin_row": min(
            rows,
            key=lambda row: (row["local_l2_cap_margin"], row["target"])),
        "largest_local_l2_cap_exceedance_rows": sorted(
            local_violations,
            key=lambda row: (
                -row["ratio_to_zero_residue_local_l2_cap"], row["target"]),
        )[:20],
    }


def build_receipt():
    zero_probe = load_json(ZERO_PROBE_SOURCE)
    schedule = load_json(ZERO_CHARACTER_SCHEDULE_SOURCE)
    formula = load_json(FORMULA_SOURCE)
    cap_by_residue = caps_by_residue(schedule)
    global_l2_cap = schedule["coefficient_character_budget"][
        "global_aggregate_character_l2_cap"]

    source_rows = zero_probe["finite_probe"]["rows"]
    active_masks = active_character_masks(formula)
    maximum_target = max(row["target"] for row in source_rows)
    primes = np.asarray(far._prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = far.logs(maximum_target)
    context = far.prepare_support_context()
    context["coefficient"] = (
        far.combined_fixed_strict_central_coefficient_receipt())
    full_coefficients = far.period_full_unit_coefficients(context)
    first_three_coefficients = far.q286_first_three_unit_coefficients(context)

    rows = []
    for source_row in source_rows:
        moments = row_moments(
            source_row,
            context,
            full_coefficients,
            first_three_coefficients,
            primes,
            prime_values,
            log_values,
            active_masks,
        )
        cap_row = cap_by_residue[int(source_row["target_residue"])]
        rows.append(row_record(source_row, moments, cap_row, global_l2_cap))

    summary = summarize_rows(rows)
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-zero-residue-observed-character-moment-audit",
        "source_commit": source_commit(),
        "sources": {
            "zero_residue_raw_horizon_probe": str(
                ZERO_PROBE_SOURCE.relative_to(ROOT)),
            "zero_residue_raw_horizon_probe_source_commit": (
                zero_probe["source_commit"]),
            "zero_residue_character_budget_schedule": str(
                ZERO_CHARACTER_SCHEDULE_SOURCE.relative_to(ROOT)),
            "zero_residue_character_budget_source_commit": (
                schedule["source_commit"]),
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "formula_source_commit": formula["source_commit"],
        },
        "status": "DIAGNOSTIC_zero_residue_plain_character_l2_not_observed_bridge",
        "question": (
            "On the targeted N == 0 mod 286 probe rows, does the observed "
            "aggregate active-character L2 moment stay below the sufficient "
            "zero-residue local caps?"),
        "answer": (
            "No.  The raw adverse-drag gate is positive on all 70 zero-lane "
            "probe rows, but 18 of those rows exceed their zero-residue "
            "local aggregate character L2 cap.  Plain aggregate L2 control is "
            "therefore not the observed finite bridge for this lane."),
        "finite_diagnostic": {
            "finite_evidence_is_acceptance_condition": False,
            "role": (
                "falsifier for claiming the displayed aggregate L2 cap already "
                "explains the checked zero-lane rows; calibration for a "
                "future structured signed theorem"),
            "summary": summary,
            "rows": rows,
        },
        "zero_mass_check": {
            "zero_pair_count_rows": summary["zero_pair_count_rows"],
            "nonpositive_raw_adverse_gate_gap_count": (
                summary["nonpositive_raw_adverse_gate_gap_count"]),
            "decision": (
                "No checked zero-lane row has zero pair count, and all keep "
                "positive raw adverse-gate gap.  L2 cap violations are not "
                "zero-mass bridge defects."),
        },
        "candidate": {
            "name": "zero-residue structured signed character theorem",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Replace plain aggregate moment size with a signed or "
                "phase-aware theorem controlling the character package in the "
                "specific coefficient direction needed by W_phi."),
            "prediction": (
                "Rows can violate plain aggregate L2 caps while still having "
                "positive raw witness because their character moments are not "
                "aligned with the adverse coefficient direction."),
            "falsifier": (
                "If rows that violate aggregate L2 also fail the raw "
                "adverse-gate inequality, the signed-structure explanation "
                "would not rescue the route.  Here they do not fail."),
            "smallest_next_action": (
                "Measure coefficient-direction alignment for the zero-lane "
                "violating rows: compare aggregate L2 load against actual "
                "adverse projection in the coefficient direction."),
        },
        "decision": (
            "DIAGNOSTIC_zero_residue_plain_character_l2_not_observed_bridge. "
            "The zero-lane raw probe survives, but plain aggregate active-"
            "character L2 does not explain it: 18/70 rows exceed their local "
            "L2 cap.  Therefore the next theorem-shaped move is not another "
            "norm-size budget; it is a signed/phase-aware character moment "
            "estimate or a direct raw witness theorem in the coefficient "
            "direction."),
        "status_boundary": (
            "Finite observed character-moment diagnostic only.  No zero-"
            "residue raw adverse-drag theorem, no aggregate character-moment "
            "theorem, no signed/phase-aware character theorem, no universal "
            "pointwise raw estimate, no q286 threshold theorem, no strict-"
            "central Goldbach theorem, and no Goldbach proof is established."),
        "zero_residue_raw_adverse_drag_theorem_proved": False,
        "aggregate_character_moment_theorem_proved": False,
        "signed_phase_character_theorem_proved": False,
        "universal_pointwise_raw_bound_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    summary = receipt["finite_diagnostic"]["summary"]
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "row_count": summary["row_count"],
        "local_l2_cap_exceeding_row_count": (
            summary["local_l2_cap_exceeding_row_count"]),
        "max_ratio_to_local_l2_cap": summary[
            "ratio_to_zero_residue_local_l2_cap_summary"]["maximum"],
        "largest_ratio_target": summary[
            "largest_local_l2_ratio_row"]["target"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
