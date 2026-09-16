"""Classify the strict raw-gap obligation for q286-WBSS.

The raw adverse-drag target

    A_raw_-(N) < L_raw(N)

is non-circular only because it is strict.  A homogeneous estimate such as
A_raw_-(N) <= rho L_raw(N), with rho < 1, is not by itself a Goldbach bridge:
if strict-central support is empty, both sides are zero and the homogeneous
estimate is still true.  To imply a witness, the proof must either establish
positive raw local main separately or prove an inhomogeneous positive raw gap

    G_raw(N) = L_raw(N) - A_raw_-(N) > 0.

This receipt records that obligation and finite calibration of plausible gap
scales.  It proves no strict raw-gap theorem, positive-mass theorem, or
Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
RAW_ADVERSE_SOURCE = (
    EVIDENCE / "q286-wbss-raw-adverse-drag-theorem-target.json")
OUT = EVIDENCE / "q286-wbss-strict-raw-gap-obligation.json"


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


def gap_row(row):
    target = int(row["target"])
    gap = float(row["raw_adverse_gate_gap"])
    raw_local_main = float(row["raw_local_main"])
    total_weight = float(row["total_weight"])
    log_target = math.log(target)
    return {
        "source": row["source"],
        "target": target,
        "target_residue": int(row["target_residue"]),
        "target_mod_286": int(row["target_mod_286"]),
        "pair_count": int(row["pair_count"]),
        "total_weight": total_weight,
        "raw_local_main": raw_local_main,
        "raw_adverse_drag": float(row["raw_adverse_drag"]),
        "strict_raw_gap": gap,
        "strict_raw_gap_positive": bool(gap > 0.0),
        "raw_adverse_drag_ratio": row["raw_adverse_drag_ratio"],
        "strict_raw_gap_over_target": float(gap / target),
        "strict_raw_gap_over_target_over_log": float(
            gap / (target / log_target)),
        "strict_raw_gap_over_sqrt_target": float(gap / math.sqrt(target)),
        "strict_raw_gap_over_total_weight": float(
            gap / total_weight if total_weight > 0.0 else 0.0),
        "raw_local_main_over_target": float(raw_local_main / target),
    }


def summarize_rows(rows):
    return {
        "row_count": len(rows),
        "target_minimum": min(row["target"] for row in rows),
        "target_maximum": max(row["target"] for row in rows),
        "positive_strict_raw_gap_count": sum(
            row["strict_raw_gap_positive"] for row in rows),
        "nonpositive_strict_raw_gap_count": sum(
            not row["strict_raw_gap_positive"] for row in rows),
        "strict_raw_gap_summary": finite_summary(
            row["strict_raw_gap"] for row in rows),
        "strict_raw_gap_over_target_summary": finite_summary(
            row["strict_raw_gap_over_target"] for row in rows),
        "strict_raw_gap_over_target_over_log_summary": finite_summary(
            row["strict_raw_gap_over_target_over_log"] for row in rows),
        "strict_raw_gap_over_sqrt_target_summary": finite_summary(
            row["strict_raw_gap_over_sqrt_target"] for row in rows),
        "strict_raw_gap_over_total_weight_summary": finite_summary(
            row["strict_raw_gap_over_total_weight"] for row in rows),
        "raw_local_main_over_target_summary": finite_summary(
            row["raw_local_main_over_target"] for row in rows),
        "tightest_strict_raw_gap_row": min(
            rows, key=lambda row: (row["strict_raw_gap"], row["target"])),
        "smallest_gap_over_target_row": min(
            rows, key=lambda row: (
                row["strict_raw_gap_over_target"], row["target"])),
        "smallest_gap_over_target_over_log_row": min(
            rows, key=lambda row: (
                row["strict_raw_gap_over_target_over_log"], row["target"])),
        "smallest_gap_over_sqrt_target_row": min(
            rows, key=lambda row: (
                row["strict_raw_gap_over_sqrt_target"], row["target"])),
        "smallest_gap_over_total_weight_row": min(
            rows, key=lambda row: (
                row["strict_raw_gap_over_total_weight"], row["target"])),
    }


def build_receipt():
    source = load_json(RAW_ADVERSE_SOURCE)
    rows = [
        gap_row(row)
        for row in source["finite_calibration"]["rows"]
    ]
    summary = summarize_rows(rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "raw_adverse_drag_theorem_target": str(
                RAW_ADVERSE_SOURCE.relative_to(ROOT)),
            "raw_adverse_drag_source_commit": source["source_commit"],
        },
        "status_boundary": (
            "q286-WBSS strict raw-gap obligation only; finite rows calibrate "
            "candidate scales but are not acceptance.  No strict raw-gap "
            "theorem, raw adverse-drag theorem, positive-mass theorem, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof"),
        "goldbach_proved": False,
        "strict_raw_gap_theorem_proved": False,
        "raw_adverse_drag_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "universal_bound_open": True,
        "definitions": {
            "strict_raw_gap": (
                "G_raw(N)=L_raw(N)-A_raw_-(N), where L_raw is the raw local "
                "main and A_raw_- is the one-sided raw adverse drag."),
            "homogeneous_ratio_boundary": (
                "A bound A_raw_-(N)<=rho*L_raw(N) with rho<1 is not alone a "
                "witness theorem, because a zero-support row has "
                "L_raw(N)=A_raw_-(N)=0 and still satisfies the homogeneous "
                "bound."),
            "sufficient_strict_gap_theorem": (
                "A theorem G_raw(N)>0, or G_raw(N)>=eta(N)>0, implies "
                "W_phi(N)>0 and forces strict-central support."),
        },
        "candidate": {
            "name": "strict raw q286-WBSS gap lower bound",
            "mechanism": (
                "Replace homogeneous ratio control by an actual positive raw "
                "gap lower bound, or explicitly pair any ratio bound with a "
                "separate positive raw-local-main theorem."),
            "prediction": (
                "A useful proof route will produce a positive lower scale for "
                "G_raw(N), not merely a relative inequality that remains true "
                "when all prime-pair mass is absent."),
            "falsifier": (
                "Any covered target with G_raw(N)<=0 falsifies this sufficient "
                "strict-gap route for the current coefficient."),
            "smallest_next_theorem_target": (
                "Prove G_raw(N)>0, preferably G_raw(N)>=eta(N)>0 with an "
                "explicit positive eta, for every sufficiently large covered "
                "even N; then verify the finite remainder."),
            "novelty_label": "new-to-this-task",
        },
        "finite_calibration": {
            "role": (
                "calibration_and_falsifier_only; fitted constants are not "
                "universal bounds"),
            "summary": summary,
            "rows": rows,
        },
        "decision": (
            "The next theorem obligation is strict raw gap, not just "
            "homogeneous raw adverse-ratio control.  A ratio theorem needs a "
            "separate positive raw-local-main or positive-mass theorem; a "
            "direct theorem G_raw(N)>0 would subsume that support obligation."),
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
        "positive_strict_raw_gap_count": summary[
            "positive_strict_raw_gap_count"],
        "nonpositive_strict_raw_gap_count": summary[
            "nonpositive_strict_raw_gap_count"],
        "tightest_strict_raw_gap_target": summary[
            "tightest_strict_raw_gap_row"]["target"],
        "tightest_strict_raw_gap": summary[
            "tightest_strict_raw_gap_row"]["strict_raw_gap"],
        "smallest_gap_over_target_target": summary[
            "smallest_gap_over_target_row"]["target"],
        "smallest_gap_over_target": summary[
            "smallest_gap_over_target_row"][
                "strict_raw_gap_over_target"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
