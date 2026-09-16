"""Rawize the q286-WBSS witness target.

The pointwise adverse-drag route is only a Goldbach bridge after the normalized
strict-central measure has been removed from the theorem hypothesis.  This
receipt scales the normalized q286-WBSS quantities by the actual strict-central
log-pair mass

    T_N = sum_{p in (N/3,2N/3), p and N-p prime} log(p) log(N-p).

If T_N is zero, the raw witness is the empty sum and equals zero.  Therefore a
direct theorem W_phi(N)>0 is non-circular: it forces nonempty strict-central
support.  This audit is finite calibration of that identity only; it proves no
raw witness theorem, positive-mass theorem, q286 threshold theorem, or
Goldbach theorem.
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
HORIZON_SOURCE = (
    EVIDENCE / "q286-wbss-four-modulus-adverse-drag-horizon-audit.json")
FRESH_SOURCE = (
    EVIDENCE / "q286-wbss-four-modulus-component-envelope-fresh-holdout.json")
OUT = EVIDENCE / "q286-wbss-raw-witness-identity-audit.json"
PERIOD = 10010
TOLERANCE = 1e-8

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
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
    vals = [float(value) for value in values]
    return {
        "count": len(vals),
        "minimum": min(vals),
        "mean": math.fsum(vals) / len(vals),
        "maximum": max(vals),
    }


def source_rows(horizon, fresh):
    rows = [
        ("adverse_drag_horizon", row)
        for row in horizon["holdout"]["rows"]
    ]
    rows.extend(
        ("frozen_component_envelope_fresh_holdout", row)
        for row in fresh["holdout"]["rows"]
    )
    return rows


def scaled_row(source_name, row, primes, prime_values, log_values):
    count, total_weight, _ = prime_indexed_residue_weights(
        int(row["target"]),
        primes,
        prime_values,
        log_values,
        PERIOD,
    )
    local_main = float(row["local_uniform_main_term"])
    actual_expectation = float(row["actual_formula_expectation"])
    adverse_drag = float(row["negative_modulus_drag"])
    adverse_gap = float(row["adverse_only_expectation"])
    signed_errors = {
        key: float(value)
        for key, value in row["signed_error_by_modulus"].items()
    }
    signed_error_sum = float(math.fsum(signed_errors.values()))
    raw_signed_errors = {
        key: float(total_weight * value)
        for key, value in signed_errors.items()
    }
    raw_signed_error_sum = float(math.fsum(raw_signed_errors.values()))
    raw_local_main = float(total_weight * local_main)
    raw_witness = float(total_weight * actual_expectation)
    raw_adverse_drag = float(total_weight * adverse_drag)
    raw_adverse_gap = float(total_weight * adverse_gap)
    raw_adverse_gap_from_main = float(raw_local_main - raw_adverse_drag)

    return {
        "source": source_name,
        "target": int(row["target"]),
        "target_residue": int(row["target_residue"]),
        "target_mod_286": int(row["target_mod_286"]),
        "pair_count": int(count),
        "source_pair_count": int(row["pair_count"]),
        "pair_count_delta": int(count - int(row["pair_count"])),
        "total_weight": float(total_weight),
        "local_main": local_main,
        "actual_formula_expectation": actual_expectation,
        "signed_error_sum": signed_error_sum,
        "signed_error_by_modulus": signed_errors,
        "adverse_drag": adverse_drag,
        "adverse_gate_gap": adverse_gap,
        "raw_local_main": raw_local_main,
        "raw_signed_error_sum": raw_signed_error_sum,
        "raw_signed_error_by_modulus": raw_signed_errors,
        "raw_witness": raw_witness,
        "raw_adverse_drag": raw_adverse_drag,
        "raw_adverse_gate_gap": raw_adverse_gap,
        "raw_adverse_gate_gap_from_main": raw_adverse_gap_from_main,
        "raw_formula_reconstruction_error": float(abs(
            raw_witness - (raw_local_main + raw_signed_error_sum))),
        "raw_adverse_gap_reconstruction_error": float(abs(
            raw_adverse_gap - raw_adverse_gap_from_main)),
        "raw_witness_positive": bool(raw_witness > TOLERANCE),
        "raw_adverse_gate_gap_positive": bool(raw_adverse_gap > TOLERANCE),
        "zero_mass_case": bool(total_weight <= TOLERANCE),
    }


def summarize_rows(rows):
    return {
        "row_count": len(rows),
        "target_minimum": min(row["target"] for row in rows),
        "target_maximum": max(row["target"] for row in rows),
        "zero_pair_count_rows": sum(row["pair_count"] == 0 for row in rows),
        "zero_total_weight_rows": sum(
            row["total_weight"] <= TOLERANCE for row in rows),
        "positive_raw_witness_count": sum(
            row["raw_witness_positive"] for row in rows),
        "positive_raw_adverse_gate_gap_count": sum(
            row["raw_adverse_gate_gap_positive"] for row in rows),
        "pair_count_mismatch_count": sum(
            row["pair_count_delta"] != 0 for row in rows),
        "total_weight_summary": finite_summary(
            row["total_weight"] for row in rows),
        "raw_witness_summary": finite_summary(
            row["raw_witness"] for row in rows),
        "raw_adverse_gate_gap_summary": finite_summary(
            row["raw_adverse_gate_gap"] for row in rows),
        "raw_formula_reconstruction_error_summary": finite_summary(
            row["raw_formula_reconstruction_error"] for row in rows),
        "raw_adverse_gap_reconstruction_error_summary": finite_summary(
            row["raw_adverse_gap_reconstruction_error"] for row in rows),
        "minimum_total_weight_row": min(
            rows, key=lambda row: (row["total_weight"], row["target"])),
        "minimum_raw_witness_row": min(
            rows, key=lambda row: (row["raw_witness"], row["target"])),
        "minimum_raw_adverse_gate_gap_row": min(
            rows, key=lambda row: (
                row["raw_adverse_gate_gap"], row["target"])),
    }


def build_receipt():
    horizon = load_json(HORIZON_SOURCE)
    fresh = load_json(FRESH_SOURCE)
    rows_in = source_rows(horizon, fresh)
    maximum_target = max(row["target"] for _, row in rows_in)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    rows = [
        scaled_row(source_name, row, primes, prime_values, log_values)
        for source_name, row in rows_in
    ]
    summary = summarize_rows(rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "adverse_drag_horizon_audit": str(
                HORIZON_SOURCE.relative_to(ROOT)),
            "adverse_drag_source_commit": horizon["source_commit"],
            "component_envelope_fresh_holdout": str(
                FRESH_SOURCE.relative_to(ROOT)),
            "fresh_holdout_source_commit": fresh["source_commit"],
        },
        "status_boundary": (
            "q286-WBSS raw witness identity audit only; finite rows are "
            "calibration and falsifier evidence, not acceptance.  No raw "
            "witness theorem, positive-mass theorem, pointwise adverse-drag "
            "theorem, q286 threshold theorem, strict-central Goldbach theorem, "
            "or Goldbach proof"),
        "goldbach_proved": False,
        "raw_witness_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "universal_bound_open": True,
        "definitions": {
            "strict_central_total_weight": (
                "T_N=sum log(p)log(N-p) over strict-central prime pairs "
                "N/3<p<2N/3."),
            "raw_witness": (
                "W_phi(N)=T_N * <mu_N,phi_N> when T_N>0, equivalently the "
                "unnormalized strict-central signed log-pair sum.  If T_N=0 "
                "the raw sum is empty and equals 0."),
            "raw_adverse_gate": (
                "T_N*(M(N)-A_-(N)) where M is the q286-WBSS local main and "
                "A_-(N)=sum_d max(0,-E_d(N))."),
            "noncircular_bridge": (
                "A direct theorem W_phi(N)>0 cannot hold on a zero-mass row, "
                "so it forces at least one strict-central prime pair."),
        },
        "candidate": {
            "name": "direct raw q286-WBSS witness lower bound",
            "mechanism": (
                "Move the proof target from normalized actual orbit measure "
                "to the raw signed log-pair sum.  This removes the need to "
                "assume strict-central mass before deriving positivity."),
            "prediction": (
                "The checked rows preserve positivity after exact T_N scaling, "
                "and a real theorem would bound W_phi(N) directly below by a "
                "positive main term minus explicit raw adverse terms."),
            "falsifier": (
                "Any covered target with W_phi(N)<=0 falsifies the direct raw "
                "witness route for that coefficient.  Any reconstruction "
                "mismatch falsifies this finite identity audit."),
            "smallest_next_theorem_target": (
                "Prove a universal, pointwise, unnormalized estimate "
                "W_phi(N)>0 for every sufficiently large covered even N, then "
                "verify the finite remainder below the threshold."),
            "novelty_label": "new-to-this-task",
        },
        "finite_calibration": {
            "role": (
                "identity_calibration_and_falsifier_only; not an acceptance "
                "condition"),
            "summary": summary,
            "rows": rows,
        },
        "decision": (
            "Rawization repairs the logical bridge target but does not prove "
            "it.  The finite data confirm that the existing normalized q286-"
            "WBSS witness and adverse-gap rows scale to positive raw witnesses "
            "on the checked 348 targets.  A Goldbach-yielding proof still "
            "needs a universal pointwise raw lower bound or a separate "
            "positive-mass theorem followed by the normalized adverse-drag "
            "bound."),
    }


def main():
    EVIDENCE.mkdir(exist_ok=True)
    receipt = build_receipt()
    OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    summary = receipt["finite_calibration"]["summary"]
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "row_count": summary["row_count"],
        "target_minimum": summary["target_minimum"],
        "target_maximum": summary["target_maximum"],
        "positive_raw_witness_count": summary[
            "positive_raw_witness_count"],
        "positive_raw_adverse_gate_gap_count": summary[
            "positive_raw_adverse_gate_gap_count"],
        "zero_total_weight_rows": summary["zero_total_weight_rows"],
        "minimum_raw_witness_target": summary[
            "minimum_raw_witness_row"]["target"],
        "minimum_raw_witness": summary[
            "minimum_raw_witness_row"]["raw_witness"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
