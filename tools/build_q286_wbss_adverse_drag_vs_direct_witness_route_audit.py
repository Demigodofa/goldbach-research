"""Compare the q286-WBSS adverse-drag route with the direct witness route.

The pointwise adverse-drag target

    adverse_drag(N) < local_main(N)

is a sufficient condition for direct positivity of the q286-WBSS signed
witness, but it is stronger than direct positivity because it discards all
helpful projected terms.  This derived receipt measures that strength gap on
the current finite calibration population.

Finite route-comparison evidence only.  It proves no adverse-drag theorem,
direct signed-witness theorem, q286 threshold theorem, strict-central Goldbach
theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE = EVIDENCE / "q286-wbss-pointwise-adverse-drag-theorem-target.json"
OUT = EVIDENCE / "q286-wbss-adverse-drag-vs-direct-witness-route-audit.json"
TOLERANCE = 1e-12


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


def compare_row(row):
    local_main = float(row["local_main"])
    adverse_drag = float(row["adverse_drag"])
    direct_witness = float(row["actual_formula_expectation"])
    adverse_only_witness = local_main - adverse_drag
    positive_projected_help = direct_witness - adverse_only_witness
    return {
        **row,
        "direct_witness": direct_witness,
        "adverse_only_witness": adverse_only_witness,
        "positive_projected_help": positive_projected_help,
        "adverse_only_witness_positive": bool(
            adverse_only_witness > TOLERANCE),
        "direct_witness_positive": bool(direct_witness > TOLERANCE),
        "positive_help_needed_for_direct_positivity": bool(
            direct_witness > TOLERANCE
            and adverse_only_witness <= TOLERANCE),
        "adverse_only_fraction_of_direct_witness": (
            adverse_only_witness / direct_witness
            if direct_witness > TOLERANCE else None),
        "positive_help_fraction_of_direct_witness": (
            positive_projected_help / direct_witness
            if direct_witness > TOLERANCE else None),
    }


def summarize_rows(rows):
    positive = [row for row in rows if row["direct_witness_positive"]]
    return {
        "row_count": len(rows),
        "target_minimum": min(row["target"] for row in rows),
        "target_maximum": max(row["target"] for row in rows),
        "direct_witness_positive_count": sum(
            row["direct_witness_positive"] for row in rows),
        "adverse_only_witness_positive_count": sum(
            row["adverse_only_witness_positive"] for row in rows),
        "positive_help_needed_for_direct_positivity_count": sum(
            row["positive_help_needed_for_direct_positivity"]
            for row in rows),
        "direct_witness_summary": finite_summary(
            row["direct_witness"] for row in rows),
        "adverse_only_witness_summary": finite_summary(
            row["adverse_only_witness"] for row in rows),
        "positive_projected_help_summary": finite_summary(
            row["positive_projected_help"] for row in rows),
        "adverse_drag_ratio_summary": finite_summary(
            row["adverse_drag_ratio"] for row in rows),
        "lambda_phi_summary": finite_summary(
            row["lambda_phi"] for row in rows),
        "adverse_only_fraction_of_direct_summary": finite_summary(
            row["adverse_only_fraction_of_direct_witness"]
            for row in positive),
        "positive_help_fraction_of_direct_summary": finite_summary(
            row["positive_help_fraction_of_direct_witness"]
            for row in positive),
        "largest_positive_help_fraction_row": max(
            positive,
            key=lambda row: (
                row["positive_help_fraction_of_direct_witness"],
                -row["target"],
            ),
        ),
        "smallest_adverse_only_fraction_row": min(
            positive,
            key=lambda row: (
                row["adverse_only_fraction_of_direct_witness"],
                row["target"],
            ),
        ),
        "tightest_adverse_drag_ratio_row": max(
            rows,
            key=lambda row: (row["adverse_drag_ratio"], -row["target"]),
        ),
        "tightest_adverse_only_witness_row": min(
            rows,
            key=lambda row: (row["adverse_only_witness"], row["target"]),
        ),
    }


def build_receipt():
    source = load_json(SOURCE)
    rows = [
        compare_row(row)
        for row in source["finite_calibration"]["rows"]
    ]
    summary = summarize_rows(rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "pointwise_adverse_drag_theorem_target": str(
                SOURCE.relative_to(ROOT)),
            "pointwise_target_source_commit": source["source_commit"],
        },
        "status": "HOLD_adverse_drag_is_valid_stricter_route_not_theorem",
        "status_boundary": (
            "finite route-comparison audit only; no pointwise adverse-drag "
            "theorem, direct signed-witness theorem, fixed-modulus "
            "binary-prime correlation theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "direct_signed_witness_theorem_proved": False,
        "fixed_modulus_binary_prime_correlation_theorem_proved": False,
        "universal_bound_open": True,
        "logical_relations": {
            "adverse_drag_implies_direct_witness": (
                "If A_-(N)<M(N), then M(N)+sum_d E_d(N)>=M(N)-A_-(N)>0."),
            "direct_witness_does_not_imply_adverse_drag": (
                "Direct positivity allows helpful projected terms to pay for "
                "larger adverse terms; adverse-drag is a stricter sufficient "
                "route, not an equivalent restatement."),
            "why_this_matters": (
                "If one-sided adverse bounds are source-backed, they avoid "
                "relying on delicate cross-modulus cancellation.  If only "
                "signed cancellation can be proved, the direct witness route "
                "is the better theorem object."),
        },
        "candidate": {
            "name": "adverse-drag lead target versus direct signed witness",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Measure how much finite direct positivity depends on helpful "
                "projected terms that the adverse-drag theorem target would "
                "discard."),
            "prediction": (
                "If the adverse-drag route is not wildly over-tight, the "
                "adverse-only witness should retain most of the direct "
                "witness and no checked row should need positive projected "
                "help merely to stay positive."),
            "falsifier": (
                "If many positive rows need positive projected help for "
                "positivity, or if the adverse-only witness is usually a tiny "
                "fraction of the direct witness, then adverse-drag should not "
                "lead the theorem search."),
            "smallest_test": (
                "Compare direct witness, adverse-only witness, and positive "
                "projected help on the existing 348-row calibration set."),
        },
        "finite_route_comparison": {
            "role": (
                "finite calibration of theorem-route cost; not an acceptance "
                "condition"),
            "summary": summary,
            "rows": rows,
        },
        "decision": (
            "The adverse-drag target earns its keep as a lead sufficient "
            "route on the checked calibration set: all 348 rows remain "
            "positive after helpful projected terms are discarded, and no row "
            "needs positive projected help for direct positivity.  The route "
            "is still genuinely stricter than direct B_Phi(N)>0: the "
            "adverse-only witness can drop to about 73.68 percent of the "
            "direct witness, so proving it may be harder than proving a "
            "signed-cancellation theorem.  Next theorem work should prefer "
            "adverse-drag only if it can be tied to source-backed one-sided "
            "binary-prime projection control; otherwise the direct signed "
            "witness remains the clean target.  Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
