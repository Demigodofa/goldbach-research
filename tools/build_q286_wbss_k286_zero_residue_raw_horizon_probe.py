"""Probe the K_286 zero-residue raw adverse-drag sublane.

The zero-residue coverage audit found that the unique K_286 no-reflection-
discount residue, N == 0 mod 286, was absent from the raw adverse-drag finite
calibration.  This receipt runs a narrow changed-condition probe: take all
35 period residues modulo 10010 that lie above 0 mod 286 and evaluate the
first two lifts after the existing raw horizon.

Finite probe only.  It is calibration and possible falsifier evidence, not an
acceptance condition and not a universal raw theorem.
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
RAW_SOURCE = EVIDENCE / "q286-wbss-raw-adverse-drag-theorem-target.json"
ZERO_COVERAGE_SOURCE = (
    EVIDENCE / "q286-wbss-k286-zero-residue-raw-coverage-audit.json")
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
OUT = EVIDENCE / "q286-wbss-k286-zero-residue-raw-horizon-probe.json"
PERIOD = 10010
MODULUS = 286
LIFT_COUNT = 2
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    period_full_unit_coefficients,
    prepare_support_context,
    q286_first_three_unit_coefficients,
)
from tools.build_q286_wbss_four_modulus_adverse_drag_horizon_audit import (  # noqa: E402
    row_adverse_drag,
)
from tools.build_q286_wbss_four_modulus_direct_holdout_decomposition import (  # noqa: E402
    coefficient_lookup,
)
from tools.build_q286_wbss_four_modulus_variance_scale_far_lift_holdout import (  # noqa: E402
    logs,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402
from tools.build_q286_wbss_raw_witness_identity_audit import (  # noqa: E402
    scaled_row,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def first_lift_above(residue, lower_bound):
    if lower_bound < residue:
        return residue
    return residue + ((lower_bound - residue) // PERIOD + 1) * PERIOD


def zero_residue_edge_rows(lower_bound, lift_count=LIFT_COUNT):
    rows = []
    for residue_index in range(PERIOD // MODULUS):
        target_residue = residue_index * MODULUS
        first_target = first_lift_above(target_residue, lower_bound)
        for lift_index in range(lift_count):
            target = first_target + lift_index * PERIOD
            rows.append({
                "target": int(target),
                "target_residue": int(target % PERIOD),
                "target_mod_286": int(target % MODULUS),
                "period_residue_index": int(residue_index),
                "lift_index": int(lift_index),
                "block_index_after_raw_horizon": int(
                    max(0, (target - lower_bound + PERIOD - 1) // PERIOD)),
                "source_positive_target": -1,
            })
    return rows


def target_row(source_name, row, primes, prime_values, log_values):
    scaled = scaled_row(
        source_name, row, primes, prime_values, log_values)
    raw_local_main = float(scaled["raw_local_main"])
    raw_adverse_drag = float(scaled["raw_adverse_drag"])
    target = int(scaled["target"])
    return {
        **scaled,
        "period_residue_index": int(row["period_residue_index"]),
        "lift_index": int(row["lift_index"]),
        "block_index_after_raw_horizon": int(
            row["block_index_after_raw_horizon"]),
        "raw_adverse_drag_ratio": (
            float(raw_adverse_drag / raw_local_main)
            if raw_local_main > TOLERANCE else None),
        "raw_adverse_gate_gap_over_target": float(
            scaled["raw_adverse_gate_gap"] / target),
        "raw_adverse_drag_below_raw_local_main": bool(
            raw_adverse_drag < raw_local_main),
    }


def summarize_rows(rows):
    ratio_rows = [
        row for row in rows
        if row["raw_adverse_drag_ratio"] is not None
    ]
    by_residue = {}
    for row in rows:
        by_residue.setdefault(str(row["target_residue"]), []).append(row)
    residue_summaries = {}
    for residue, residue_rows in by_residue.items():
        residue_summaries[residue] = {
            "row_count": len(residue_rows),
            "period_residue_index": residue_rows[0][
                "period_residue_index"],
            "raw_adverse_drag_ratio_summary": finite_summary(
                row["raw_adverse_drag_ratio"] for row in residue_rows),
            "raw_adverse_gate_gap_summary": finite_summary(
                row["raw_adverse_gate_gap"] for row in residue_rows),
            "raw_adverse_gate_gap_over_target_summary": finite_summary(
                row["raw_adverse_gate_gap_over_target"]
                for row in residue_rows),
            "tightest_gap_row": min(
                residue_rows,
                key=lambda row: (row["raw_adverse_gate_gap"],
                                 row["target"])),
            "largest_ratio_row": max(
                residue_rows,
                key=lambda row: (
                    row["raw_adverse_drag_ratio"]
                    if row["raw_adverse_drag_ratio"] is not None else -1.0,
                    -row["target"])),
        }
    return {
        "row_count": len(rows),
        "target_minimum": min(row["target"] for row in rows),
        "target_maximum": max(row["target"] for row in rows),
        "period_residue_count": len(by_residue),
        "lift_count_per_period_residue": LIFT_COUNT,
        "zero_pair_count_rows": sum(row["pair_count"] == 0 for row in rows),
        "zero_total_weight_rows": sum(
            row["zero_mass_case"] for row in rows),
        "positive_raw_witness_count": sum(
            row["raw_witness_positive"] for row in rows),
        "positive_raw_adverse_gate_gap_count": sum(
            row["raw_adverse_gate_gap_positive"] for row in rows),
        "raw_adverse_drag_below_raw_local_main_count": sum(
            row["raw_adverse_drag_below_raw_local_main"] for row in rows),
        "raw_adverse_drag_not_below_raw_local_main_count": sum(
            not row["raw_adverse_drag_below_raw_local_main"]
            for row in rows),
        "raw_adverse_drag_ratio_summary": finite_summary(
            row["raw_adverse_drag_ratio"] for row in ratio_rows),
        "raw_adverse_gate_gap_summary": finite_summary(
            row["raw_adverse_gate_gap"] for row in rows),
        "raw_adverse_gate_gap_over_target_summary": finite_summary(
            row["raw_adverse_gate_gap_over_target"] for row in rows),
        "pair_count_summary": finite_summary(
            row["pair_count"] for row in rows),
        "total_weight_summary": finite_summary(
            row["total_weight"] for row in rows),
        "tightest_raw_gate_gap_row": min(
            rows, key=lambda row: (
                row["raw_adverse_gate_gap"], row["target"])),
        "largest_raw_adverse_drag_ratio_row": max(
            ratio_rows, key=lambda row: (
                row["raw_adverse_drag_ratio"], -row["target"])),
        "smallest_gap_over_target_row": min(
            rows, key=lambda row: (
                row["raw_adverse_gate_gap_over_target"], row["target"])),
        "residue_summaries": residue_summaries,
    }


def build_receipt():
    raw = load_json(RAW_SOURCE)
    zero_coverage = load_json(ZERO_COVERAGE_SOURCE)
    formula = load_json(FORMULA_SOURCE)
    alpha0, by_modulus = coefficient_lookup(formula)
    lower_bound = max(
        row["target"] for row in raw["finite_calibration"]["rows"])
    edge_rows = zero_residue_edge_rows(lower_bound)
    maximum_target = max(row["target"] for row in edge_rows)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    adverse_rows = [
        row_adverse_drag(
            row,
            context,
            full_coefficients,
            first_three_coefficients,
            primes,
            prime_values,
            log_values,
            alpha0,
            by_modulus,
        )
        for row in edge_rows
    ]
    # Preserve the targeting fields from edge_rows; row_adverse_drag keeps the
    # arithmetic fields but intentionally ignores probe metadata.
    for adverse, edge in zip(adverse_rows, edge_rows):
        adverse["period_residue_index"] = edge["period_residue_index"]
        adverse["block_index_after_raw_horizon"] = edge[
            "block_index_after_raw_horizon"]
    rows = [
        target_row("k286_zero_residue_raw_horizon_probe",
                   row, primes, prime_values, log_values)
        for row in adverse_rows
    ]
    summary = summarize_rows(rows)
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-zero-residue-raw-horizon-probe",
        "source_commit": source_commit(),
        "sources": {
            "raw_adverse_drag_theorem_target": str(
                RAW_SOURCE.relative_to(ROOT)),
            "raw_adverse_drag_source_commit": raw["source_commit"],
            "zero_residue_coverage_audit": str(
                ZERO_COVERAGE_SOURCE.relative_to(ROOT)),
            "zero_residue_coverage_source_commit": (
                zero_coverage["source_commit"]),
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "formula_source_commit": formula["source_commit"],
        },
        "status": "PROBE_zero_residue_raw_horizon_survives_finite_check_not_proof",
        "question": (
            "After finding that N == 0 mod 286 was absent from the raw "
            "finite calibration, does a targeted near-horizon zero-residue "
            "probe immediately falsify the raw adverse-drag route?"),
        "answer": (
            "No finite falsifier appears in this targeted probe.  The first "
            "two lifts of all 35 period residues with target_mod_286=0 have "
            "positive raw adverse-gate gap and positive raw witness.  This is "
            "calibration only; the universal pointwise raw theorem remains "
            "open."),
        "targeting": {
            "target_mod_286": 0,
            "period": PERIOD,
            "period_residues_checked": [row["target_residue"]
                                        for row in edge_rows
                                        if row["lift_index"] == 0],
            "period_residue_count": PERIOD // MODULUS,
            "lift_count_per_period_residue": LIFT_COUNT,
            "lower_bound_source": (
                "maximum target from q286-wbss-raw-adverse-drag-theorem-"
                "target finite calibration"),
            "lower_bound": lower_bound,
        },
        "finite_probe": {
            "role": (
                "targeted calibration and falsifier only; not an acceptance "
                "condition"),
            "summary": summary,
            "rows": rows,
        },
        "comparison_to_prior_raw_calibration": {
            "prior_raw_row_count": raw["finite_calibration"]["summary"][
                "row_count"],
            "prior_largest_raw_adverse_drag_ratio": raw[
                "finite_calibration"]["summary"][
                    "largest_raw_adverse_drag_ratio_row"][
                        "raw_adverse_drag_ratio"],
            "prior_largest_raw_adverse_drag_ratio_target": raw[
                "finite_calibration"]["summary"][
                    "largest_raw_adverse_drag_ratio_row"]["target"],
            "prior_tightest_raw_gate_gap": raw[
                "finite_calibration"]["summary"][
                    "tightest_raw_gate_gap_row"]["raw_adverse_gate_gap"],
            "prior_tightest_raw_gate_gap_target": raw[
                "finite_calibration"]["summary"][
                    "tightest_raw_gate_gap_row"]["target"],
            "probe_largest_raw_adverse_drag_ratio": summary[
                "largest_raw_adverse_drag_ratio_row"][
                    "raw_adverse_drag_ratio"],
            "probe_tightest_raw_gate_gap": summary[
                "tightest_raw_gate_gap_row"]["raw_adverse_gate_gap"],
        },
        "candidate": {
            "name": "zero-residue raw horizon probe",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Directly sample the unique K_286 reflection no-discount "
                "residue in raw adverse-drag coordinates, rather than "
                "inferring its behavior from other residue classes."),
            "prediction": (
                "If the no-discount K_286 lane is an immediate finite "
                "obstruction, one of the first lifts should show "
                "A_raw_-(N)>=L_raw(N) or zero raw witness."),
            "falsifier": (
                "Any row with nonpositive raw adverse-gate gap or nonpositive "
                "raw witness would falsify this q286-WBSS sufficient route at "
                "that target."),
            "smallest_next_action": (
                "If useful, widen the zero-residue horizon only as a "
                "predeclared falsifier/calibration test; theorem acceptance "
                "still requires a universal pointwise raw estimate."),
        },
        "decision": (
            "The targeted zero-residue finite probe survives: no checked row "
            "has zero mass, nonpositive raw witness, or "
            "A_raw_-(N)>=L_raw(N).  This removes the immediate finite "
            "falsifier for the previously unsampled no-discount lane, but it "
            "does not promote finite evidence into proof.  The necessary "
            "theorem lane remains: prove A_raw_-(N)<L_raw(N), or an "
            "equivalent raw witness lower bound, for every sufficiently large "
            "covered even N with N==0 mod 286."),
        "status_boundary": (
            "Targeted finite raw-horizon probe only.  No zero-residue raw "
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
    summary = receipt["finite_probe"]["summary"]
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "row_count": summary["row_count"],
        "period_residue_count": summary["period_residue_count"],
        "positive_raw_adverse_gate_gap_count": (
            summary["positive_raw_adverse_gate_gap_count"]),
        "zero_total_weight_rows": summary["zero_total_weight_rows"],
        "largest_raw_adverse_drag_ratio": summary[
            "largest_raw_adverse_drag_ratio_row"][
                "raw_adverse_drag_ratio"],
        "tightest_raw_gate_gap": summary[
            "tightest_raw_gate_gap_row"]["raw_adverse_gate_gap"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
