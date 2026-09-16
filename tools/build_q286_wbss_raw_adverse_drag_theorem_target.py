"""State the raw q286-WBSS adverse-drag theorem target.

The normalized pointwise adverse-drag gate was not a complete bridge because it
used the actual strict-central orbit measure.  The raw witness identity gives
the corresponding unnormalized quantities.  This receipt states the sufficient
theorem target entirely in raw sums:

    A_raw_-(N) < L_raw(N).

Both sides are zero when strict-central support is empty, so a strict theorem of
this shape would force support.  This is a theorem target and finite
calibration only; it proves no raw adverse-drag theorem, q286 threshold theorem,
or Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
RAW_SOURCE = EVIDENCE / "q286-wbss-raw-witness-identity-audit.json"
OUT = EVIDENCE / "q286-wbss-raw-adverse-drag-theorem-target.json"


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


def target_row(row):
    raw_local_main = float(row["raw_local_main"])
    raw_adverse_drag = float(row["raw_adverse_drag"])
    raw_gate_gap = float(row["raw_adverse_gate_gap"])
    ratio = (
        raw_adverse_drag / raw_local_main
        if raw_local_main > 0.0 else None
    )
    return {
        "source": row["source"],
        "target": int(row["target"]),
        "target_residue": int(row["target_residue"]),
        "target_mod_286": int(row["target_mod_286"]),
        "pair_count": int(row["pair_count"]),
        "total_weight": float(row["total_weight"]),
        "raw_local_main": raw_local_main,
        "raw_adverse_drag": raw_adverse_drag,
        "raw_adverse_gate_gap": raw_gate_gap,
        "raw_witness": float(row["raw_witness"]),
        "raw_adverse_drag_ratio": ratio,
        "raw_adverse_drag_below_raw_local_main": bool(
            raw_adverse_drag < raw_local_main),
        "raw_gate_gap_positive": bool(raw_gate_gap > 0.0),
    }


def summarize_rows(rows):
    ratio_rows = [
        row for row in rows
        if row["raw_adverse_drag_ratio"] is not None
    ]
    return {
        "row_count": len(rows),
        "target_minimum": min(row["target"] for row in rows),
        "target_maximum": max(row["target"] for row in rows),
        "positive_total_weight_count": sum(
            row["total_weight"] > 0.0 for row in rows),
        "zero_total_weight_count": sum(
            row["total_weight"] <= 0.0 for row in rows),
        "raw_adverse_drag_below_raw_local_main_count": sum(
            row["raw_adverse_drag_below_raw_local_main"] for row in rows),
        "raw_adverse_drag_not_below_raw_local_main_count": sum(
            not row["raw_adverse_drag_below_raw_local_main"]
            for row in rows),
        "positive_raw_gate_gap_count": sum(
            row["raw_gate_gap_positive"] for row in rows),
        "raw_local_main_summary": finite_summary(
            row["raw_local_main"] for row in rows),
        "raw_adverse_drag_summary": finite_summary(
            row["raw_adverse_drag"] for row in rows),
        "raw_gate_gap_summary": finite_summary(
            row["raw_adverse_gate_gap"] for row in rows),
        "raw_adverse_drag_ratio_summary": finite_summary(
            row["raw_adverse_drag_ratio"] for row in ratio_rows),
        "minimum_raw_local_main_row": min(
            rows, key=lambda row: (row["raw_local_main"], row["target"])),
        "maximum_raw_adverse_drag_row": max(
            rows, key=lambda row: (
                row["raw_adverse_drag"], -row["target"])),
        "tightest_raw_gate_gap_row": min(
            rows, key=lambda row: (
                row["raw_adverse_gate_gap"], row["target"])),
        "largest_raw_adverse_drag_ratio_row": max(
            ratio_rows, key=lambda row: (
                row["raw_adverse_drag_ratio"], -row["target"])),
    }


def build_receipt():
    source = load_json(RAW_SOURCE)
    rows = [
        target_row(row)
        for row in source["finite_calibration"]["rows"]
    ]
    summary = summarize_rows(rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "raw_witness_identity_audit": str(RAW_SOURCE.relative_to(ROOT)),
            "raw_witness_identity_source_commit": source["source_commit"],
        },
        "status_boundary": (
            "q286-WBSS raw adverse-drag theorem target only; finite rows are "
            "calibration and falsifier evidence, not acceptance.  No raw "
            "adverse-drag theorem, raw witness theorem, positive-mass theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"),
        "goldbach_proved": False,
        "raw_adverse_drag_theorem_proved": False,
        "raw_witness_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "universal_bound_open": True,
        "acceptance_condition": {
            "finite_evidence_is_acceptance_condition": False,
            "required_universal_statement": (
                "There exist an explicit threshold N0 and an explicit covered "
                "even-target class such that, for every covered even N>=N0, "
                "A_raw_-(N) < L_raw(N)."),
            "finite_remainder_requirement": (
                "After the universal raw inequality is proved, all covered "
                "even targets below N0 must be verified by an independent "
                "finite remainder check."),
        },
        "definitions": {
            "strict_central_total_weight": (
                "T_N=sum log(p)log(N-p) over strict-central prime pairs "
                "N/3<p<2N/3."),
            "raw_local_main": (
                "L_raw(N)=T_N*M(N), where M(N)=<u_a,phi_a> is the local "
                "q286-WBSS main term for a=N mod 10010."),
            "raw_projected_error": (
                "U_d(N)=T_N*E_d(N), equivalently the raw projected "
                "binary-prime discrepancy against the d-th WBSS projection."),
            "raw_adverse_drag": (
                "A_raw_-(N)=sum_d max(0,-U_d(N)) for d in "
                "{70,130,154,286}."),
            "sufficient_pointwise_inequality": (
                "A_raw_-(N)<L_raw(N) implies "
                "L_raw(N)+sum_d U_d(N)>0, hence W_phi(N)>0."),
            "zero_support_boundary": (
                "If strict-central support is empty, then T_N=0, "
                "L_raw(N)=0, U_d(N)=0, and A_raw_-(N)=0; the strict "
                "inequality cannot hold.  Therefore a proved strict raw "
                "adverse-drag inequality forces support."),
        },
        "candidate": {
            "name": "raw pointwise q286-WBSS adverse-drag estimate",
            "mechanism": (
                "Bound the one-sided raw projected binary-prime drag below the "
                "raw local main term at each target, without first normalizing "
                "by existing strict-central mass."),
            "prediction": (
                "A valid theorem will explain why the summed adverse raw "
                "projections cannot erase the q286-WBSS raw local main term."),
            "falsifier": (
                "Any covered target with A_raw_-(N)>=L_raw(N) falsifies this "
                "sufficient route for the current coefficient."),
            "smallest_next_theorem_target": (
                "Prove A_raw_-(N)<L_raw(N) for all sufficiently large covered "
                "even N, then verify the finite remainder."),
            "novelty_label": "new-to-this-task",
        },
        "finite_calibration": {
            "role": (
                "calibration_and_falsifier_only; not an acceptance condition"),
            "summary": summary,
            "rows": rows,
        },
        "decision": (
            "The q286-WBSS route now has a non-circular raw sufficient "
            "inequality target: A_raw_-(N)<L_raw(N).  The checked rows satisfy "
            "it, but this is finite calibration only.  A Goldbach-yielding "
            "bridge still needs a universal pointwise raw adverse-drag theorem "
            "or another direct raw witness lower bound."),
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
        "raw_adverse_drag_below_raw_local_main_count": summary[
            "raw_adverse_drag_below_raw_local_main_count"],
        "raw_adverse_drag_not_below_raw_local_main_count": summary[
            "raw_adverse_drag_not_below_raw_local_main_count"],
        "largest_raw_adverse_drag_ratio": summary[
            "largest_raw_adverse_drag_ratio_row"][
                "raw_adverse_drag_ratio"],
        "largest_raw_adverse_drag_ratio_target": summary[
            "largest_raw_adverse_drag_ratio_row"]["target"],
        "tightest_raw_gate_gap": summary[
            "tightest_raw_gate_gap_row"]["raw_adverse_gate_gap"],
        "tightest_raw_gate_gap_target": summary[
            "tightest_raw_gate_gap_row"]["target"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
