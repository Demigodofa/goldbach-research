"""Fresh holdout for the q286-WBSS componentwise envelope.

The component-envelope horizon audit fitted one adverse supremum for each of
the four projected moduli on 232 checked rows.  This receipt freezes those
values and tests the next four period-lifts of the same stressed source
residues.  It separates two questions:

1. Does the frozen sum envelope still stay below local main?
2. Do the individually fitted component suprema remain valid on fresh rows?

Finite targeted holdout only.  It proves no per-modulus supremum theorem,
one-sided signed concentration theorem, fixed-modulus equidistribution theorem,
q286 threshold theorem, strict-central Goldbach theorem, or Goldbach proof.
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
SOURCE = (
    EVIDENCE
    / "q286-wbss-four-modulus-component-envelope-horizon-audit.json")
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
OUT = (
    EVIDENCE
    / "q286-wbss-four-modulus-component-envelope-fresh-holdout.json")
FRESH_LIFT_COUNT = 4
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from tools import build_q286_wbss_four_modulus_variance_scale_far_lift_holdout as far  # noqa: E501,E402
from tools.build_q286_wbss_four_modulus_adverse_drag_horizon_audit import (  # noqa: E402
    row_adverse_drag,
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


def row_with_frozen_envelope(row, frozen_suprema, frozen_sum):
    modulus_excess = {}
    any_excess = False
    for modulus, frozen_value in sorted(frozen_suprema.items(), key=lambda x: int(x[0])):
        adverse_value = max(0.0, -row["signed_error_by_modulus"][modulus])
        excess = adverse_value - frozen_value
        exceeded = excess > TOLERANCE
        any_excess = any_excess or exceeded
        modulus_excess[modulus] = {
            "fresh_adverse_value": float(adverse_value),
            "frozen_adverse_supremum": float(frozen_value),
            "excess_over_frozen_supremum": float(excess),
            "exceeds_frozen_supremum": bool(exceeded),
        }
    expectation = float(row["local_uniform_main_term"] - frozen_sum)
    return {
        **row,
        "frozen_component_adverse_supremum_sum": float(frozen_sum),
        "frozen_componentwise_envelope_expectation": expectation,
        "frozen_componentwise_envelope_ratio": float(
            frozen_sum / row["local_uniform_main_term"]),
        "frozen_componentwise_envelope_positive": bool(
            expectation > TOLERANCE),
        "modulus_excess_over_frozen_suprema": modulus_excess,
        "any_modulus_exceeds_frozen_supremum": bool(any_excess),
    }


def modulus_excess_summary(rows, frozen_suprema):
    result = {}
    for modulus in sorted(frozen_suprema, key=int):
        excess_rows = [
            row for row in rows
            if row["modulus_excess_over_frozen_suprema"][modulus][
                "exceeds_frozen_supremum"]
        ]
        fresh_adverse_values = [
            row["modulus_excess_over_frozen_suprema"][modulus][
                "fresh_adverse_value"]
            for row in rows
        ]
        max_row = max(
            rows,
            key=lambda row: (
                row["modulus_excess_over_frozen_suprema"][modulus][
                    "fresh_adverse_value"],
                -row["target"],
            ),
        )
        result[modulus] = {
            "frozen_adverse_supremum": float(frozen_suprema[modulus]),
            "fresh_adverse_value_summary": finite_summary(
                fresh_adverse_values),
            "fresh_maximum_row": {
                "target": int(max_row["target"]),
                "target_residue": int(max_row["target_residue"]),
                "target_mod_286": int(max_row["target_mod_286"]),
                **max_row["modulus_excess_over_frozen_suprema"][modulus],
            },
            "exceeding_row_count": len(excess_rows),
            "exceeding_rows": [
                {
                    "target": int(row["target"]),
                    "target_residue": int(row["target_residue"]),
                    "target_mod_286": int(row["target_mod_286"]),
                    **row["modulus_excess_over_frozen_suprema"][modulus],
                }
                for row in sorted(
                    excess_rows,
                    key=lambda item: (
                        -item["modulus_excess_over_frozen_suprema"][modulus][
                            "excess_over_frozen_supremum"],
                        item["target"],
                    ),
                )[:20]
            ],
        }
    return result


def summarize_rows(rows):
    return {
        "row_count": len(rows),
        "actual_positive_count": sum(
            row["actual_formula_expectation"] > TOLERANCE for row in rows),
        "lambda_budget_failure_count": sum(
            row["lambda_phi"] >= 1.0 - TOLERANCE for row in rows),
        "frozen_componentwise_envelope_positive_count": sum(
            row["frozen_componentwise_envelope_positive"] for row in rows),
        "frozen_componentwise_envelope_nonpositive_count": sum(
            not row["frozen_componentwise_envelope_positive"]
            for row in rows),
        "rows_with_any_modulus_exceeding_frozen_supremum": sum(
            row["any_modulus_exceeds_frozen_supremum"] for row in rows),
        "local_uniform_main_term_summary": finite_summary(
            row["local_uniform_main_term"] for row in rows),
        "actual_expectation_summary": finite_summary(
            row["actual_formula_expectation"] for row in rows),
        "lambda_phi_summary": finite_summary(
            row["lambda_phi"] for row in rows),
        "negative_drag_ratio_summary": finite_summary(
            row["negative_drag_ratio"] for row in rows),
        "frozen_componentwise_envelope_expectation_summary": finite_summary(
            row["frozen_componentwise_envelope_expectation"]
            for row in rows),
        "frozen_componentwise_envelope_ratio_summary": finite_summary(
            row["frozen_componentwise_envelope_ratio"] for row in rows),
        "tightest_frozen_componentwise_envelope_row": min(
            rows,
            key=lambda row: (
                row["frozen_componentwise_envelope_expectation"],
                row["target"],
            ),
        ),
        "largest_frozen_componentwise_ratio_row": max(
            rows,
            key=lambda row: (
                row["frozen_componentwise_envelope_ratio"],
                -row["target"],
            ),
        ),
        "largest_rowwise_negative_drag_ratio_row": max(
            rows,
            key=lambda row: (
                row["negative_drag_ratio"],
                -row["target"],
            ),
        ),
        "largest_lambda_row": max(
            rows,
            key=lambda row: (row["lambda_phi"], -row["target"]),
        ),
    }


def build_receipt():
    source = load_json(SOURCE)
    formula = load_json(FORMULA_SOURCE)
    alpha0, by_modulus = far.coefficient_lookup(formula)
    seed_rows, lower_bound, source_residue_count = far.far_lift_rows(
        source, lift_count=FRESH_LIFT_COUNT)
    maximum_target = max(row["target"] for row in seed_rows)
    primes = np.asarray(far._prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = far.logs(maximum_target)
    context = far.prepare_support_context()
    context["coefficient"] = far.combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = far.period_full_unit_coefficients(context)
    first_three_coefficients = far.q286_first_three_unit_coefficients(context)
    frozen_suprema = source["component_adverse_suprema"]
    frozen_sum = float(source["component_adverse_supremum_sum"])
    rows = [
        row_with_frozen_envelope(
            row_adverse_drag(
                seed,
                context,
                full_coefficients,
                first_three_coefficients,
                primes,
                prime_values,
                log_values,
                alpha0,
                by_modulus,
            ),
            frozen_suprema,
            frozen_sum,
        )
        for seed in seed_rows
    ]
    summary = summarize_rows(rows)
    excess = modulus_excess_summary(rows, frozen_suprema)
    frozen_envelope_survives = (
        summary["frozen_componentwise_envelope_nonpositive_count"] == 0)
    individual_suprema_survive = all(
        item["exceeding_row_count"] == 0 for item in excess.values())
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "component_envelope_horizon_audit": str(SOURCE.relative_to(ROOT)),
            "component_envelope_source_commit": source["source_commit"],
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "formula_source_commit": formula["source_commit"],
        },
        "status_boundary": (
            "finite q286-WBSS frozen component-envelope fresh holdout only; "
            "no per-modulus supremum theorem, one-sided signed concentration "
            "theorem, fixed-modulus equidistribution theorem, q286 threshold "
            "theorem, strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "per_modulus_supremum_theorem_proved": False,
        "one_sided_signed_concentration_theorem_proved": False,
        "fixed_modulus_equidistribution_theorem_proved": False,
        "universal_negative_drag_bound_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "frozen componentwise envelope fresh holdout",
            "mechanism": (
                "Freeze the four component adverse suprema fitted on the "
                "232-row horizon and replay them on the next four lifts of "
                "the same stressed source residues.  Track both the frozen "
                "sum envelope and each individual frozen component bound."),
            "prediction": (
                "If the component-envelope route has portable slack, the "
                "frozen sum should stay below fresh local main terms.  If "
                "the literal per-modulus supremum constants are not stable, "
                "a fresh component will exceed its fitted value."),
            "falsifier": (
                "Any fresh row with local_main <= frozen_sum kills the "
                "frozen sum-envelope route.  Any fresh adverse component "
                "above its fitted supremum kills the literal fixed "
                "per-modulus-constant route."),
            "smallest_test": (
                "Use the next four period-lifts of the same 29 stressed "
                "source residues after target 1115822."),
            "novelty_label": "new-to-this-task",
        },
        "frozen_component_adverse_suprema": frozen_suprema,
        "frozen_component_adverse_supremum_sum": frozen_sum,
        "holdout": {
            "source_positive_residue_count": source_residue_count,
            "fresh_lift_count_per_residue": FRESH_LIFT_COUNT,
            "previous_target_maximum": int(lower_bound),
            "target_count": len(rows),
            "target_minimum": min(row["target"] for row in rows),
            "target_maximum": maximum_target,
            "summary": summary,
            "modulus_excess_summary": excess,
            "rows": rows,
        },
        "frozen_componentwise_envelope_survives_fresh_holdout": (
            frozen_envelope_survives),
        "individual_frozen_component_suprema_survive_fresh_holdout": (
            individual_suprema_survive),
        "individual_frozen_component_suprema_falsified": (
            not individual_suprema_survive),
        "residual_absorption_boundary": (
            "Decimal residual absorption constants such as .125, .126, and "
            ".13 remain finite fixture fits only.  This receipt does not "
            "promote any residual absorption constant to a universal bound."),
        "decision": (
            "The frozen componentwise sum-envelope survives the fresh "
            "four-lift holdout, but the literal individual frozen component "
            "suprema do not: modulus 286 exceeds its fitted horizon value "
            "on fresh rows.  Therefore the theorem target should not be a "
            "fixed list of per-modulus constants copied from the horizon. "
            "The surviving route is a sum-envelope or local-main-relative "
            "adverse-drag bound with fresh component slack.  Goldbach "
            "remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
