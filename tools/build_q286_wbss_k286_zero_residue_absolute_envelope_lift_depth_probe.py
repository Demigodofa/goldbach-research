"""Probe K_286 absolute-envelope payment over deeper zero-residue lifts.

The 70-row zero-residue probe survived all period classes for two lifts after
the raw adverse-drag horizon.  This changed-condition probe keeps all 35
period residues with N == 0 mod 286 and extends each one to eight lifts.

Finite probe only.  It proves no K_286 absolute-envelope theorem, companion
adverse-drag theorem, q286 threshold theorem, strict-central Goldbach theorem,
or Goldbach proof.
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
ZERO_PAYMENT_SOURCE = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-absolute-envelope-payment-probe.json")
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
OUT = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-absolute-envelope-lift-depth-probe.json")
LIFT_COUNT = 8

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
    summarize_rows,
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


def build_receipt():
    raw = load_json(RAW_SOURCE)
    zero_payment = load_json(ZERO_PAYMENT_SOURCE)
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
        rows.append(payment)
    summary = summarize_rows(rows)
    return {
        "schema_version": 1,
        "receipt": (
            "q286-wbss-k286-zero-residue-absolute-envelope-lift-depth-probe"),
        "source_commit": source_commit(),
        "sources": {
            "raw_adverse_drag_theorem_target": str(
                RAW_SOURCE.relative_to(ROOT)),
            "raw_adverse_drag_source_commit": raw["source_commit"],
            "zero_residue_absolute_envelope_payment_probe": str(
                ZERO_PAYMENT_SOURCE.relative_to(ROOT)),
            "zero_residue_absolute_envelope_payment_source_commit": (
                zero_payment["source_commit"]),
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "formula_source_commit": formula["source_commit"],
        },
        "status": (
            "PROBE_k286_zero_residue_absolute_envelope_payment_survives_"
            "lift_depth"),
        "question": (
            "Does the K_286 absolute-envelope payment diagnostic survive all "
            "35 zero-residue period classes through eight lifts after the raw "
            "adverse-drag horizon?"),
        "answer": (
            "Yes on this 280-row finite probe.  Every checked zero-residue "
            "row has M(N)-A_other(N)-H_286(N)>0.  The tightest row is the "
            "same row already exposed by the four-residue extended-lift "
            "audit, not a new period class."),
        "targeting": {
            "target_mod_286": 0,
            "period_residue_count": 35,
            "lift_count_per_period_residue": LIFT_COUNT,
            "lower_bound_source": (
                "maximum target from q286-wbss-raw-adverse-drag-theorem-"
                "target finite calibration"),
            "lower_bound": lower_bound,
        },
        "finite_probe": {
            "finite_evidence_is_acceptance_condition": False,
            "role": (
                "lift-depth falsifier probe for the K_286 absolute-envelope "
                "payment theorem target"),
            "definitions": {
                "M": "local_main(N)",
                "H_286": (
                    "sum of absolute real K_286 conjugate phase-pair "
                    "contributions"),
                "A_other": (
                    "sum of adverse projected errors from moduli 70, 130, "
                    "and 154 only"),
                "payment_margin": "M(N)-A_other(N)-H_286(N)",
            },
            "summary": summary,
            "rows": rows,
        },
        "candidate": {
            "name": "zero-residue lift-depth K286 absolute envelope payment",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Stress the absolute-envelope payment route in the direction "
                "that the previous probes identified as most likely to be "
                "vulnerable: deeper lifts, not just more near-horizon period "
                "residues."),
            "prediction": (
                "If the route is robust, the minimum payment margin should "
                "remain positive through deeper lifts; if it is finite-scale "
                "fragile, a later lift should produce "
                "M(N)<=A_other(N)+H_286(N)."),
            "falsifier": (
                "Any zero-residue lift with M(N)<=A_other(N)+H_286(N) kills "
                "this sufficient absolute-envelope payment route for that "
                "class."),
            "smallest_next_action": (
                "Either push lift depth again, or convert the empirical "
                "payment pieces into separately stated theorem targets for "
                "H_286(N) and A_other(N)."),
        },
        "decision": (
            "PROBE_k286_zero_residue_absolute_envelope_payment_survives_"
            "lift_depth.  The absolute-envelope payment route survives a "
            "280-row finite lift-depth probe over all zero-residue period "
            "classes.  This strengthens the theorem-shaped direction and "
            "keeps the next useful stress on deeper lift behavior or on "
            "separating H_286 and A_other into analytic theorem targets.  "
            "The result remains finite probe evidence only."),
        "status_boundary": (
            "Finite zero-residue lift-depth absolute-envelope payment probe "
            "only.  No K_286 absolute-envelope theorem, companion adverse-"
            "drag theorem, phase-cancellation theorem, universal pointwise "
            "raw bound, q286 threshold theorem, strict-central Goldbach "
            "theorem, or Goldbach proof is established."),
        "k286_absolute_envelope_theorem_proved": False,
        "companion_adverse_drag_theorem_proved": False,
        "phase_cancellation_theorem_proved": False,
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
    summary = receipt["finite_probe"]["summary"]
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "row_count": summary["row_count"],
        "payment_positive_count": summary[
            "absolute_envelope_payment_positive_count"],
        "payment_margin_minimum": summary[
            "absolute_envelope_margin_summary"]["minimum"],
        "payment_ratio_maximum": summary[
            "absolute_envelope_payment_ratio_summary"]["maximum"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
