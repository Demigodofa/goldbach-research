"""Stress the K_286 quarter-residual companion target at deeper lift depth.

The 280-row fixture suggested the finite candidate

    A_other(N) <= (1/4) * (M(N) - H_286(N)).

This changed-condition probe keeps the same 35 zero-residue period classes
and doubles the lift count from eight to sixteen.  It is a falsifier probe
only.  Passing it would not prove a quarter-residual theorem.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
RAW_SOURCE = EVIDENCE / "q286-wbss-raw-adverse-drag-theorem-target.json"
QUARTER_SOURCE = (
    EVIDENCE
    / "q286-wbss-k286-quarter-residual-companion-obligation.json")
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
OUT = (
    EVIDENCE
    / "q286-wbss-k286-quarter-residual-lift-depth-stress.json")
LIFT_COUNT = 16
QUARTER = 0.25

sys.path.insert(0, str(ROOT))

from tools import build_q286_wbss_four_modulus_variance_scale_far_lift_holdout as far  # noqa: E501,E402
from tools.build_q286_wbss_four_modulus_adverse_drag_horizon_audit import (  # noqa: E501,E402
    row_adverse_drag,
)
from tools.build_q286_wbss_four_modulus_direct_holdout_decomposition import (  # noqa: E501,E402
    coefficient_lookup,
)
from tools.build_q286_wbss_k286_absolute_envelope_payment_audit import (  # noqa: E501,E402
    payment_row,
)
from tools.build_q286_wbss_k286_quarter_residual_companion_obligation import (  # noqa: E501,E402
    finite_summary,
)
from tools.build_q286_wbss_k286_zero_residue_absolute_envelope_payment_probe import (  # noqa: E501,E402
    phase_row,
)
from tools.build_q286_wbss_k286_zero_residue_raw_horizon_probe import (  # noqa: E501,E402
    zero_residue_edge_rows,
)
from tools.build_q286_wbss_multiplicative_character_l2_observed_moment_audit import (  # noqa: E501,E402
    active_character_masks,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def companion_row(row):
    local_main = float(row["local_main"])
    h_ratio = float(row["k286_absolute_phase_envelope"] / local_main)
    a_ratio = float(row["other_moduli_adverse_drag"] / local_main)
    residual_after_h = 1.0 - h_ratio
    companion_fraction = (
        a_ratio / residual_after_h if residual_after_h > 0.0 else None)
    quarter_margin_ratio = residual_after_h * QUARTER - a_ratio
    return {
        "target": int(row["target"]),
        "target_residue": int(row["target_residue"]),
        "target_mod_286": int(row["target_mod_286"]),
        "period_residue_index": int(row["period_residue_index"]),
        "lift_index": int(row["lift_index"]),
        "block_index_after_raw_horizon": int(
            row["block_index_after_raw_horizon"]),
        "local_main": local_main,
        "k286_absolute_phase_envelope": float(
            row["k286_absolute_phase_envelope"]),
        "other_moduli_adverse_drag": float(
            row["other_moduli_adverse_drag"]),
        "k286_absolute_envelope_ratio": h_ratio,
        "other_moduli_adverse_ratio": a_ratio,
        "residual_after_h_ratio": residual_after_h,
        "companion_residual_fraction": companion_fraction,
        "quarter_residual_companion_margin_ratio": quarter_margin_ratio,
        "quarter_residual_companion_survives": bool(
            quarter_margin_ratio > 0.0),
        "residual_payment_route_survives": bool(
            residual_after_h > 0.0 and companion_fraction < 1.0),
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
        "residual_payment_route_surviving_count": sum(
            row["residual_payment_route_survives"] for row in rows),
        "residual_payment_route_failed_count": sum(
            not row["residual_payment_route_survives"] for row in rows),
        "k286_absolute_envelope_ratio_summary": finite_summary(
            row["k286_absolute_envelope_ratio"] for row in rows),
        "other_moduli_adverse_ratio_summary": finite_summary(
            row["other_moduli_adverse_ratio"] for row in rows),
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
    raw = load_json(RAW_SOURCE)
    quarter = load_json(QUARTER_SOURCE)
    formula = load_json(FORMULA_SOURCE)
    alpha0, by_modulus = coefficient_lookup(formula)
    lower_bound = max(
        int(row["target"]) for row in raw["finite_calibration"]["rows"])
    source_rows = zero_residue_edge_rows(lower_bound, lift_count=LIFT_COUNT)
    maximum_target = max(row["target"] for row in source_rows)
    primes = np.asarray(far._prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = far.logs(maximum_target)
    context = far.prepare_support_context()
    context["coefficient"] = (
        far.combined_fixed_strict_central_coefficient_receipt())
    full_coefficients = far.period_full_unit_coefficients(context)
    first_three_coefficients = far.q286_first_three_unit_coefficients(context)
    active_masks = active_character_masks(formula)
    rows = []
    for row in source_rows:
        adverse = row_adverse_drag(
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
        adverse["block_index_after_raw_horizon"] = row[
            "block_index_after_raw_horizon"]
        payment = payment_row(
            row,
            adverse,
            phase_row(
                row,
                context,
                full_coefficients,
                first_three_coefficients,
                primes,
                prime_values,
                log_values,
                active_masks,
            ),
        )
        payment["period_residue_index"] = row["period_residue_index"]
        rows.append(companion_row(payment))
    summary = summarize_rows(rows)
    quarter_survives = (
        summary["quarter_residual_nonpositive_count"] == 0)
    status = (
        "PROBE_k286_quarter_residual_survives_lift_depth_stress"
        if quarter_survives
        else "FALSIFIER_k286_quarter_residual_fails_lift_depth_stress")
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-quarter-residual-lift-depth-stress",
        "source_commit": source_commit(),
        "sources": {
            "raw_adverse_drag_theorem_target": str(
                RAW_SOURCE.relative_to(ROOT)),
            "raw_adverse_drag_source_commit": raw["source_commit"],
            "quarter_residual_companion_obligation": str(
                QUARTER_SOURCE.relative_to(ROOT)),
            "quarter_residual_companion_source_commit": (
                quarter["source_commit"]),
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "formula_source_commit": formula["source_commit"],
        },
        "status": status,
        "question": (
            "Does the fragile K_286 quarter-residual companion candidate "
            "survive all 35 zero-residue period classes through sixteen "
            "lifts after the raw adverse-drag horizon?"),
        "answer": (
            "Computed from the finite 560-row lift-depth stress fixture.  "
            "The result is a changed-condition falsifier probe only; it is "
            "not a theorem or a universal constant."),
        "targeting": {
            "target_mod_286": 0,
            "period_residue_count": 35,
            "lift_count_per_period_residue": LIFT_COUNT,
            "lower_bound_source": (
                "maximum target from q286-wbss-raw-adverse-drag-theorem-"
                "target finite calibration"),
            "lower_bound": lower_bound,
        },
        "finite_stress": {
            "finite_evidence_is_acceptance_condition": False,
            "role": (
                "changed-condition falsifier probe for the quarter-residual "
                "companion theorem candidate"),
            "tested_inequality": (
                "A_other(N) <= (1/4)(M(N)-H_286(N))"),
            "summary": summary,
            "rows": rows,
        },
        "candidate": {
            "name": "quarter residual companion budget lift-depth stress",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "If the quarter bound is structural rather than near-horizon "
                "calibration, doubling the lift depth should not produce a "
                "row where the three-modulus adverse drag consumes more "
                "than one quarter of the post-H_286 residual budget."),
            "prediction": (
                "The maximum A_other/(M-H_286) remains below 1/4 under a "
                "deeper zero-residue lift stress."),
            "falsifier": (
                "Any checked row with A_other >= (1/4)(M-H_286) falsifies "
                "the quarter constant as a finite theorem target for this "
                "changed condition; any row with A_other >= M-H_286 "
                "falsifies the residual-payment route on the fixture."),
            "smallest_next_action": (
                "If the quarter survives, try to replace finite calibration "
                "with a source-backed analytic one-sided estimate.  If it "
                "fails, preserve the failure row and use the observed ratio "
                "as a lower bound for any possible constant."),
        },
        "decision": (
            f"{status}.  The sixteen-lift stress is finite evidence only.  "
            "It does not establish a quarter-residual theorem, K_286 "
            "absolute-envelope theorem, companion adverse-drag theorem, "
            "universal pointwise raw estimate, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof."),
        "status_boundary": (
            "Finite changed-condition stress test only.  No quarter-residual "
            "theorem, K_286 absolute-envelope theorem, companion adverse-"
            "drag theorem, same-row tradeoff theorem, universal pointwise "
            "raw bound, q286 threshold theorem, strict-central Goldbach "
            "theorem, or Goldbach proof is established."),
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
    summary = receipt["finite_stress"]["summary"]
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "row_count": summary["row_count"],
        "companion_residual_fraction_max": summary[
            "companion_residual_fraction_summary"]["maximum"],
        "quarter_margin_minimum": summary[
            "quarter_residual_companion_margin_ratio_summary"]["minimum"],
        "quarter_residual_nonpositive_count": summary[
            "quarter_residual_nonpositive_count"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
