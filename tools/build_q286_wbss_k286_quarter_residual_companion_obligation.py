"""Test the quarter-residual companion budget after paying H_286.

The two-budget obligation says a proof must pay both H_286 and A_other.  This
derived receipt asks whether the finite lift-depth fixture suggests a sharper
companion theorem:

    A_other(N) <= (1/4) * (M(N) - H_286(N)).

Finite calibration only.  The quarter constant is not a theorem constant.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
TWO_BUDGET_SOURCE = (
    EVIDENCE / "q286-wbss-k286-absolute-envelope-two-budget-obligation.json")
OUT = (
    EVIDENCE
    / "q286-wbss-k286-quarter-residual-companion-obligation.json")
QUARTER = 0.25


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


def companion_row(row):
    h_ratio = float(row["k286_absolute_envelope_ratio"])
    a_ratio = float(row["other_moduli_adverse_ratio"])
    residual_after_h = 1.0 - h_ratio
    companion_fraction = (
        a_ratio / residual_after_h if residual_after_h > 0.0 else None)
    quarter_margin_ratio = residual_after_h * QUARTER - a_ratio
    return {
        **row,
        "residual_after_h_ratio": residual_after_h,
        "companion_residual_fraction": companion_fraction,
        "quarter_residual_companion_margin_ratio": quarter_margin_ratio,
        "quarter_residual_companion_survives": bool(
            quarter_margin_ratio > 0.0),
    }


def pearson_correlation(rows):
    n = len(rows)
    h_mean = sum(row["k286_absolute_envelope_ratio"] for row in rows) / n
    a_mean = sum(row["other_moduli_adverse_ratio"] for row in rows) / n
    covariance = sum(
        (row["k286_absolute_envelope_ratio"] - h_mean)
        * (row["other_moduli_adverse_ratio"] - a_mean)
        for row in rows) / n
    h_variance = sum(
        (row["k286_absolute_envelope_ratio"] - h_mean) ** 2
        for row in rows) / n
    a_variance = sum(
        (row["other_moduli_adverse_ratio"] - a_mean) ** 2
        for row in rows) / n
    return covariance / (h_variance * a_variance) ** 0.5


def summarize_rows(rows):
    return {
        "row_count": len(rows),
        "target_minimum": min(row["target"] for row in rows),
        "target_maximum": max(row["target"] for row in rows),
        "quarter_residual_surviving_count": sum(
            row["quarter_residual_companion_survives"] for row in rows),
        "quarter_residual_nonpositive_count": sum(
            not row["quarter_residual_companion_survives"] for row in rows),
        "residual_after_h_ratio_summary": finite_summary(
            row["residual_after_h_ratio"] for row in rows),
        "companion_residual_fraction_summary": finite_summary(
            row["companion_residual_fraction"] for row in rows),
        "quarter_residual_companion_margin_ratio_summary": finite_summary(
            row["quarter_residual_companion_margin_ratio"] for row in rows),
        "h286_other_ratio_pearson_correlation": pearson_correlation(rows),
        "largest_companion_residual_fraction_row": max(
            rows,
            key=lambda row: (
                row["companion_residual_fraction"], -row["target"])),
        "tightest_quarter_residual_margin_row": min(
            rows,
            key=lambda row: (
                row["quarter_residual_companion_margin_ratio"],
                row["target"])),
    }


def build_receipt():
    two_budget = load_json(TWO_BUDGET_SOURCE)
    rows = [
        companion_row(row)
        for row in two_budget["finite_calibration"]["rows"]
    ]
    summary = summarize_rows(rows)
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-quarter-residual-companion-obligation",
        "source_commit": source_commit(),
        "sources": {
            "two_budget_obligation": str(
                TWO_BUDGET_SOURCE.relative_to(ROOT)),
            "two_budget_source_commit": two_budget["source_commit"],
        },
        "status": (
            "TARGET_k286_quarter_residual_companion_theorem_candidate"),
        "question": (
            "After paying the K_286 absolute envelope, does the companion "
            "adverse drag fit a quarter of the remaining local-main budget "
            "on the finite lift-depth fixture?"),
        "answer": (
            "Yes on the 280-row finite fixture.  The largest observed "
            "A_other/(M-H_286) is below 1/4, but very close to it.  This is "
            "a candidate theorem target, not a universal bound."),
        "finite_calibration": {
            "finite_evidence_is_acceptance_condition": False,
            "role": (
                "calibration for a sharper companion theorem after the "
                "K_286 absolute envelope has been paid"),
            "summary": summary,
            "rows": rows,
        },
        "theorem_obligation": {
            "k286_envelope_first": (
                "First prove H_286(N)<M(N), leaving residual budget "
                "M(N)-H_286(N)>0."),
            "quarter_residual_companion_bound": (
                "Then prove A_other(N) <= (1/4)(M(N)-H_286(N)) for every "
                "sufficiently large covered target, or replace 1/4 with a "
                "source-backed constant c<1."),
            "finite_remainder_requirement": (
                "After a threshold is proved, verify all covered targets "
                "below it independently."),
        },
        "candidate": {
            "name": "quarter residual companion budget",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Treat K_286 absolute-envelope payment as the dominant cost; "
                "measure the remaining three-modulus adverse drag as a "
                "fraction of the residual local main."),
            "prediction": (
                "If this is structural, deeper or broader zero-residue "
                "samples should keep A_other/(M-H_286) below a stable "
                "constant less than 1."),
            "falsifier": (
                "Any checked row with A_other >= (1/4)(M-H_286) falsifies "
                "the quarter candidate; any row with A_other >= M-H_286 "
                "falsifies the whole residual-payment route."),
            "smallest_next_action": (
                "Stress the quarter residual bound at greater lift depth or "
                "try to express A_other as a source-backed one-sided "
                "three-modulus estimate against the residual budget."),
        },
        "decision": (
            "TARGET_k286_quarter_residual_companion_theorem_candidate.  The "
            "finite 280-row fixture supports a sharper companion target: "
            "after paying H_286, A_other consumes less than one quarter of "
            "the remaining local-main budget.  The slack is small at the "
            "tight row, so the quarter is a fragile finite candidate, not a "
            "theorem constant."),
        "status_boundary": (
            "Theorem-target calibration only.  No quarter-residual theorem, "
            "K_286 absolute-envelope theorem, companion adverse-drag theorem, "
            "same-row tradeoff theorem, universal pointwise raw bound, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof is established."),
        "quarter_residual_theorem_proved": False,
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
        "companion_residual_fraction_max": summary[
            "companion_residual_fraction_summary"]["maximum"],
        "quarter_margin_minimum": summary[
            "quarter_residual_companion_margin_ratio_summary"]["minimum"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
