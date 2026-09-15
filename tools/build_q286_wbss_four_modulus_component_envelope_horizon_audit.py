"""Componentwise envelope audit for q286-WBSS four-modulus adverse drag.

The rowwise adverse-drag audit showed that each checked horizon row survives
after deleting all helpful projected terms in that same row.  This derived
receipt asks a stricter finite question: if each modulus contributes its worst
observed adverse value anywhere in the 232-row horizon, does the disconnected
componentwise envelope still remain below the local main term?

Finite horizon evidence only.  It proves no per-modulus supremum theorem,
one-sided signed concentration theorem, fixed-modulus equidistribution theorem,
q286 threshold theorem, strict-central Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE = EVIDENCE / "q286-wbss-four-modulus-adverse-drag-horizon-audit.json"
OUT = (
    EVIDENCE
    / "q286-wbss-four-modulus-component-envelope-horizon-audit.json")
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_source():
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def component_suprema(rows):
    moduli = sorted(rows[0]["signed_error_by_modulus"], key=int)
    suprema = {}
    source_rows = {}
    for modulus in moduli:
        row = max(
            rows,
            key=lambda item: max(
                0.0, -item["signed_error_by_modulus"][modulus]),
        )
        value = max(0.0, -row["signed_error_by_modulus"][modulus])
        suprema[modulus] = float(value)
        source_rows[modulus] = {
            "target": int(row["target"]),
            "target_residue": int(row["target_residue"]),
            "target_mod_286": int(row["target_mod_286"]),
            "signed_error": float(row["signed_error_by_modulus"][modulus]),
            "adverse_value": float(value),
            "local_uniform_main_term": float(row["local_uniform_main_term"]),
            "rowwise_negative_modulus_drag": float(
                row["negative_modulus_drag"]),
            "rowwise_negative_drag_ratio": float(row["negative_drag_ratio"]),
        }
    return suprema, source_rows


def derived_rows(rows, envelope_sum):
    result = []
    for row in rows:
        expectation = float(row["local_uniform_main_term"] - envelope_sum)
        result.append({
            "target": int(row["target"]),
            "target_residue": int(row["target_residue"]),
            "target_mod_286": int(row["target_mod_286"]),
            "lift_index": int(row["lift_index"]),
            "source_positive_target": int(row["source_positive_target"]),
            "local_uniform_main_term": float(row["local_uniform_main_term"]),
            "actual_formula_expectation": float(
                row["actual_formula_expectation"]),
            "rowwise_adverse_only_expectation": float(
                row["adverse_only_expectation"]),
            "rowwise_negative_modulus_drag": float(
                row["negative_modulus_drag"]),
            "rowwise_negative_drag_ratio": float(
                row["negative_drag_ratio"]),
            "componentwise_envelope_expectation": expectation,
            "componentwise_envelope_ratio": float(
                envelope_sum / row["local_uniform_main_term"]),
            "componentwise_envelope_positive": bool(
                expectation > TOLERANCE),
            "signed_error_by_modulus": {
                key: float(value)
                for key, value in row["signed_error_by_modulus"].items()
            },
        })
    return result


def summarize_rows(rows):
    return {
        "row_count": len(rows),
        "componentwise_envelope_positive_count": sum(
            row["componentwise_envelope_positive"] for row in rows),
        "componentwise_envelope_nonpositive_count": sum(
            not row["componentwise_envelope_positive"] for row in rows),
        "local_uniform_main_term_summary": finite_summary(
            row["local_uniform_main_term"] for row in rows),
        "componentwise_envelope_expectation_summary": finite_summary(
            row["componentwise_envelope_expectation"] for row in rows),
        "componentwise_envelope_ratio_summary": finite_summary(
            row["componentwise_envelope_ratio"] for row in rows),
        "rowwise_negative_drag_ratio_summary": finite_summary(
            row["rowwise_negative_drag_ratio"] for row in rows),
        "tightest_componentwise_envelope_row": min(
            rows,
            key=lambda row: (
                row["componentwise_envelope_expectation"],
                row["target"],
            ),
        ),
        "largest_componentwise_ratio_row": max(
            rows,
            key=lambda row: (
                row["componentwise_envelope_ratio"],
                -row["target"],
            ),
        ),
        "largest_rowwise_negative_drag_ratio_row": max(
            rows,
            key=lambda row: (
                row["rowwise_negative_drag_ratio"],
                -row["target"],
            ),
        ),
    }


def build_receipt():
    source = load_source()
    source_rows = source["holdout"]["rows"]
    suprema, source_supremum_rows = component_suprema(source_rows)
    envelope_sum = float(math.fsum(suprema.values()))
    rows = derived_rows(source_rows, envelope_sum)
    summary = summarize_rows(rows)
    survives = summary["componentwise_envelope_nonpositive_count"] == 0
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "adverse_drag_horizon_audit": str(SOURCE.relative_to(ROOT)),
            "adverse_drag_source_commit": source["source_commit"],
        },
        "status_boundary": (
            "finite q286-WBSS disconnected componentwise envelope audit only; "
            "the component suprema are fitted to the 232 checked rows.  No "
            "per-modulus supremum theorem, one-sided signed concentration "
            "theorem, fixed-modulus equidistribution theorem, q286 threshold "
            "theorem, strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "per_modulus_supremum_theorem_proved": False,
        "one_sided_signed_concentration_theorem_proved": False,
        "fixed_modulus_equidistribution_theorem_proved": False,
        "universal_negative_drag_bound_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "disconnected componentwise adverse-drag envelope",
            "mechanism": (
                "Take the worst adverse signed error observed for each of "
                "the four projected moduli separately, sum those four "
                "component suprema, and subtract the sum from every row's "
                "local main term.  This destroys rowwise covariance and is "
                "therefore stricter than the rowwise adverse-drag audit."),
            "prediction": (
                "If the four-modulus route has theorem-shaped slack, even "
                "the disconnected sum of the four finite adverse suprema "
                "should stay below the smallest checked local main term."),
            "falsifier": (
                "Any checked row with local_main <= sum(component adverse "
                "suprema) falsifies this finite componentwise-envelope route."),
            "smallest_test": (
                "Read the 232-row adverse-drag horizon receipt, compute one "
                "adverse supremum for each of 70, 130, 154, and 286, then "
                "apply their sum to all 232 rows."),
            "novelty_label": "new-to-this-task",
        },
        "component_adverse_suprema": suprema,
        "component_adverse_supremum_rows": source_supremum_rows,
        "component_adverse_supremum_sum": envelope_sum,
        "holdout": {
            "target_count": len(rows),
            "target_minimum": min(row["target"] for row in rows),
            "target_maximum": max(row["target"] for row in rows),
            "summary": summary,
            "rows": rows,
        },
        "componentwise_envelope_survives_horizon": survives,
        "componentwise_route_blocked": not survives,
        "residual_absorption_boundary": (
            "Decimal residual absorption constants such as .125, .126, and "
            ".13 remain finite fixture fits only.  This receipt does not "
            "promote any residual absorption constant to a universal bound."),
        "decision": (
            "The disconnected componentwise finite envelope survives the "
            "232-row horizon: the sum of separately worst observed adverse "
            "modulus contributions stays below every checked local main "
            "term.  This sharpens the next theorem target from rowwise "
            "adverse drag to per-modulus adverse supremum control, while "
            "preserving the boundary that all constants here are finite-data "
            "evidence only.  Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
