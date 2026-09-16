"""Separate the K_286 absolute-envelope route into two theorem budgets.

The lift-depth probe shows that M(N)-A_other(N)-H_286(N)>0 on a 280-row
finite fixture.  This receipt turns that successful finite inequality into
the actual theorem obligation: prove a K_286 absolute-envelope bound and a
companion adverse-drag bound whose relative budgets have strict sum below 1.

Finite ratios in this receipt are calibration only.  They are not universal
constants and do not prove Goldbach.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
LIFT_DEPTH_SOURCE = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-absolute-envelope-lift-depth-probe.json")
OUT = EVIDENCE / "q286-wbss-k286-absolute-envelope-two-budget-obligation.json"


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
        "mean": sum(vals) / len(vals),
        "maximum": max(vals),
    }


def budget_row(row):
    local_main = float(row["local_main"])
    h_ratio = float(row["k286_absolute_phase_envelope"] / local_main)
    a_ratio = float(row["other_moduli_adverse_drag"] / local_main)
    return {
        "target": int(row["target"]),
        "target_residue": int(row["target_residue"]),
        "target_mod_286": int(row["target_mod_286"]),
        "period_residue_index": int(row["period_residue_index"]),
        "lift_index": int(row["lift_index"]),
        "local_main": local_main,
        "k286_absolute_phase_envelope": float(
            row["k286_absolute_phase_envelope"]),
        "other_moduli_adverse_drag": float(
            row["other_moduli_adverse_drag"]),
        "k286_absolute_envelope_ratio": h_ratio,
        "other_moduli_adverse_ratio": a_ratio,
        "two_budget_payment_ratio": h_ratio + a_ratio,
        "two_budget_margin_ratio": 1.0 - h_ratio - a_ratio,
        "absolute_envelope_margin": float(row["absolute_envelope_margin"]),
        "absolute_envelope_payment_ratio": float(
            row["absolute_envelope_payment_ratio"]),
        "k286_signed_adverse_ratio_to_envelope": (
            None if row["k286_signed_adverse_ratio_to_envelope"] is None
            else float(row["k286_signed_adverse_ratio_to_envelope"])),
    }


def summarize_rows(rows):
    return {
        "row_count": len(rows),
        "target_minimum": min(row["target"] for row in rows),
        "target_maximum": max(row["target"] for row in rows),
        "positive_two_budget_margin_count": sum(
            row["two_budget_margin_ratio"] > 0.0 for row in rows),
        "nonpositive_two_budget_margin_count": sum(
            row["two_budget_margin_ratio"] <= 0.0 for row in rows),
        "k286_absolute_envelope_ratio_summary": finite_summary(
            row["k286_absolute_envelope_ratio"] for row in rows),
        "other_moduli_adverse_ratio_summary": finite_summary(
            row["other_moduli_adverse_ratio"] for row in rows),
        "two_budget_payment_ratio_summary": finite_summary(
            row["two_budget_payment_ratio"] for row in rows),
        "two_budget_margin_ratio_summary": finite_summary(
            row["two_budget_margin_ratio"] for row in rows),
        "absolute_envelope_margin_summary": finite_summary(
            row["absolute_envelope_margin"] for row in rows),
        "largest_k286_absolute_envelope_ratio_row": max(
            rows,
            key=lambda row: (
                row["k286_absolute_envelope_ratio"], -row["target"])),
        "largest_other_moduli_adverse_ratio_row": max(
            rows,
            key=lambda row: (
                row["other_moduli_adverse_ratio"], -row["target"])),
        "largest_two_budget_payment_ratio_row": max(
            rows,
            key=lambda row: (
                row["two_budget_payment_ratio"], -row["target"])),
        "smallest_two_budget_margin_ratio_row": min(
            rows,
            key=lambda row: (row["two_budget_margin_ratio"], row["target"])),
    }


def build_receipt():
    lift_depth = load_json(LIFT_DEPTH_SOURCE)
    rows = [
        budget_row(row)
        for row in lift_depth["finite_probe"]["rows"]
    ]
    summary = summarize_rows(rows)
    max_h = summary["k286_absolute_envelope_ratio_summary"]["maximum"]
    max_a = summary["other_moduli_adverse_ratio_summary"]["maximum"]
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-absolute-envelope-two-budget-obligation",
        "source_commit": source_commit(),
        "sources": {
            "zero_residue_absolute_envelope_lift_depth_probe": str(
                LIFT_DEPTH_SOURCE.relative_to(ROOT)),
            "zero_residue_absolute_envelope_lift_depth_source_commit": (
                lift_depth["source_commit"]),
        },
        "status": "TARGET_k286_absolute_envelope_two_budget_theorem_required",
        "question": (
            "What universal theorem obligations are exposed by the surviving "
            "finite K_286 absolute-envelope payment probe?"),
        "answer": (
            "A proof route must separately bound the K_286 absolute phase "
            "envelope and the companion adverse drag from moduli 70, 130, "
            "and 154.  The needed theorem shape is H_286(N)<=h(N)M(N), "
            "A_other(N)<=a(N)M(N), and h(N)+a(N)<1 for every sufficiently "
            "large covered zero-residue target, plus finite remainder."),
        "finite_calibration": {
            "finite_evidence_is_acceptance_condition": False,
            "role": (
                "calibration for the two separate analytic budgets hidden "
                "inside the successful absolute-envelope payment inequality"),
            "summary": summary,
            "rows": rows,
        },
        "theorem_obligation": {
            "covered_class": (
                "covered even targets in the q286-WBSS zero-residue class "
                "N == 0 mod 286, or a broader class if the proof generalizes"),
            "k286_absolute_envelope_bound": (
                "Prove H_286(N) <= h(N) M(N), where H_286 is the absolute "
                "real K_286 conjugate phase-pair envelope."),
            "companion_adverse_drag_bound": (
                "Prove A_other(N) <= a(N) M(N), where A_other is the "
                "one-sided adverse drag from moduli 70, 130, and 154."),
            "strict_payment_condition": (
                "Prove h(N)+a(N) <= 1-epsilon(N) with epsilon(N)>0 for "
                "every sufficiently large covered target."),
            "finite_remainder_requirement": (
                "After an explicit threshold is proved, verify all covered "
                "targets below it independently."),
        },
        "finite_ratio_warning": {
            "separate_maxima_do_not_pay": bool(max_h + max_a >= 1.0),
            "sum_of_separate_finite_maxima": max_h + max_a,
            "reason": (
                "The finite maximum of H_286/M and the finite maximum of "
                "A_other/M occur on different rows.  Adding separate fitted "
                "maxima is not the theorem; the theorem must control their "
                "same-row sum."),
        },
        "candidate": {
            "name": "two-budget K286 absolute-envelope theorem",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Split the surviving payment margin into two analytic "
                "estimates: an absolute phase-envelope estimate for K_286 "
                "and a companion one-sided adverse estimate for the other "
                "moduli."),
            "prediction": (
                "A real proof should explain the same-row anti-alignment "
                "between large H_286/M and large A_other/M, or provide "
                "strong enough individual asymptotic bounds that their sum "
                "remains below 1."),
            "falsifier": (
                "A zero-residue row family with H_286(N)/M(N) + "
                "A_other(N)/M(N) >= 1 kills this sufficient route."),
            "smallest_next_action": (
                "Search for a same-row tradeoff between H_286/M and "
                "A_other/M, because separate finite maxima alone are a weak "
                "universal theorem shape."),
        },
        "decision": (
            "TARGET_k286_absolute_envelope_two_budget_theorem_required.  The "
            "280-row lift-depth probe exposes two separate universal "
            "obligations: bound H_286 relative to local main and bound "
            "A_other relative to local main with strict same-row sum below "
            "1.  Finite fitted ratios remain calibration only and do not "
            "prove either theorem."),
        "status_boundary": (
            "Theorem-obligation audit only.  No K_286 absolute-envelope "
            "theorem, companion adverse-drag theorem, same-row tradeoff "
            "theorem, universal pointwise raw bound, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof is "
            "established."),
        "k286_absolute_envelope_theorem_proved": False,
        "companion_adverse_drag_theorem_proved": False,
        "same_row_tradeoff_theorem_proved": False,
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
    summary = receipt["finite_calibration"]["summary"]
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "row_count": summary["row_count"],
        "max_h286_ratio": summary[
            "k286_absolute_envelope_ratio_summary"]["maximum"],
        "max_other_ratio": summary[
            "other_moduli_adverse_ratio_summary"]["maximum"],
        "max_same_row_sum": summary[
            "two_budget_payment_ratio_summary"]["maximum"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
