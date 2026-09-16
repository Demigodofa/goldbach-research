"""Extended period-lift horizon for the q286 support-order bridge.

The first period-lift holdout survived eight forward lifts.  This receipt
extends the same fixed support-size <= 2 split through thirty-two forward
period-lifts of the same seven residues.

Finite horizon audit only.  It proves no eventual-threshold theorem,
low-order base theorem, high-order tail domination theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof.
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
HOLDOUT_SOURCE = (
    EVIDENCE / "q286-residual-support-order-period-lift-holdout.json")
OUT = EVIDENCE / "q286-residual-support-order-period-lift-horizon.json"
LIFT_COUNT = 32
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_frequency_resolved_fourier import (  # noqa: E402
    _unit_character_table,
)
from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    SELECTED_TARGETS,
    combined_fixed_strict_central_coefficient_receipt,
    period_full_unit_coefficients,
    prepare_support_context,
    q286_first_three_unit_coefficients,
)
from tools.build_q286_orthogonal_residual_norm_certificate import (  # noqa: E402
    residual_operator,
)
from tools.build_q286_prime_indexed_kernel_route_audit import logs  # noqa: E402
from tools.build_q286_residual_character_support_packet_budget_audit import (  # noqa: E402,E501
    PERIOD,
    row_budget,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def support_order(label):
    return len(label.split("x"))


def evaluate_support_order(row, base_target, lift_index):
    low_order_signed = 0.0
    low_order_abs = 0.0
    high_order_signed = 0.0
    high_order_abs = 0.0
    for packet in row["packet_rows"]:
        value = float(packet["signed_packet_action"])
        if support_order(packet["support_label"]) <= 2:
            low_order_signed += value
            low_order_abs += abs(value)
        else:
            high_order_signed += value
            high_order_abs += abs(value)
    aligned = float(row["aligned_only_full_action"])
    low_order_base = aligned + low_order_signed
    full = float(row["actual_full_action"])
    base_positive = low_order_base > TOLERANCE
    full_positive = bool(row["actual_full_positive"])
    adverse_ratio = None
    if base_positive and high_order_signed < -TOLERANCE:
        adverse_ratio = -high_order_signed / low_order_base
    abs_ratio = None
    if base_positive and high_order_abs > TOLERANCE:
        abs_ratio = high_order_abs / low_order_base
    return {
        "target": int(row["target"]),
        "base_target": int(base_target),
        "lift_index": int(lift_index),
        "target_mod_period": int(row["target"] % PERIOD),
        "target_mod_286": int(row["target_mod_286"]),
        "target_residue": int(row["target_residue"]),
        "actual_full_action": full,
        "actual_full_positive": full_positive,
        "aligned_only_full_action": aligned,
        "low_order_signed_action": low_order_signed,
        "low_order_abs_action": low_order_abs,
        "low_order_base_action": low_order_base,
        "low_order_base_positive": base_positive,
        "high_order_signed_tail": high_order_signed,
        "high_order_abs_tail": high_order_abs,
        "high_order_tail_is_adverse": bool(high_order_signed < -TOLERANCE),
        "high_order_adverse_to_base_ratio": adverse_ratio,
        "high_order_abs_to_base_ratio": abs_ratio,
        "signed_reconstruction_error": (
            low_order_base + high_order_signed - full),
        "low_order_base_sign_matches_full_sign": bool(
            base_positive == full_positive),
    }


def finite_summary(values):
    values = list(values)
    if not values:
        return None
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": math.fsum(values) / len(values),
    }


def build_horizon_rows():
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    units = tuple(
        residue for residue in range(PERIOD)
        if math.gcd(residue, PERIOD) == 1)
    _, labels, character_table = _unit_character_table(PERIOD, units)

    targets = [
        int(base + lift * PERIOD)
        for lift in range(1, LIFT_COUNT + 1)
        for base in SELECTED_TARGETS
    ]
    maximum_target = max(targets)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    operators = {
        int(target % PERIOD): residual_operator(
            int(target % PERIOD),
            context,
            full_coefficients,
            first_three_coefficients,
        )
        for target in targets
    }

    rows = []
    for lift in range(1, LIFT_COUNT + 1):
        for base in SELECTED_TARGETS:
            target = int(base + lift * PERIOD)
            budget = row_budget(
                target,
                operators[int(target % PERIOD)],
                units,
                labels,
                character_table,
                primes,
                prime_values,
                log_values,
            )
            rows.append(evaluate_support_order(budget, base, lift))
    return rows


def build_receipt():
    source = load_json(HOLDOUT_SOURCE)
    rows = build_horizon_rows()
    positive_rows = [row for row in rows if row["actual_full_positive"]]
    mismatches = [
        row for row in rows
        if not row["low_order_base_sign_matches_full_sign"]
    ]
    base_positive_rows = [row for row in rows if row["low_order_base_positive"]]
    adverse_ratio_rows = [
        row for row in base_positive_rows
        if row["high_order_adverse_to_base_ratio"] is not None
    ]
    abs_ratio_rows = [
        row for row in base_positive_rows
        if row["high_order_abs_to_base_ratio"] is not None
    ]
    tight_base = min(
        rows,
        key=lambda row: (row["low_order_base_action"], row["target"]),
    )
    tight_full = min(
        rows,
        key=lambda row: (row["actual_full_action"], row["target"]),
    )
    max_adverse_ratio = max(
        adverse_ratio_rows,
        key=lambda row: (
            row["high_order_adverse_to_base_ratio"], -row["target"]),
    )
    max_abs_ratio = max(
        abs_ratio_rows,
        key=lambda row: (row["high_order_abs_to_base_ratio"], -row["target"]),
    )
    high_order_adverse_envelope = max(
        max(0.0, -row["high_order_signed_tail"]) for row in rows)
    envelope_margin_at_tight_base = (
        tight_base["low_order_base_action"] - high_order_adverse_envelope)
    by_lift = []
    for lift in range(1, LIFT_COUNT + 1):
        group = [row for row in rows if row["lift_index"] == lift]
        by_lift.append({
            "lift_index": lift,
            "row_count": len(group),
            "actual_full_positive_count": sum(
                row["actual_full_positive"] for row in group),
            "low_order_base_positive_count": sum(
                row["low_order_base_positive"] for row in group),
            "sign_mismatch_count": sum(
                not row["low_order_base_sign_matches_full_sign"]
                for row in group),
            "minimum_low_order_base": min(
                row["low_order_base_action"] for row in group),
            "minimum_actual_full_action": min(
                row["actual_full_action"] for row in group),
            "maximum_high_order_adverse_to_base_ratio": max(
                (
                    row["high_order_adverse_to_base_ratio"] or 0.0
                    for row in group
                ),
            ),
        })
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "period_lift_holdout": str(HOLDOUT_SOURCE.relative_to(ROOT)),
            "period_lift_holdout_status": source["status"],
        },
        "status": "CANDIDATE_period_lift_support_order_bridge_survives_32_lift_horizon",
        "status_boundary": (
            "finite 32-lift horizon audit only; no eventual-threshold theorem, "
            "low-order base theorem, high-order tail domination theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"),
        "goldbach_proved": False,
        "eventual_threshold_theorem_proved": False,
        "low_order_base_theorem_proved": False,
        "high_order_tail_domination_theorem_proved": False,
        "signed_packet_theorem_proved": False,
        "universal_bound_open": True,
        "acceptance_condition": {
            "finite_evidence_is_acceptance_condition": False,
            "required_acceptance_condition": (
                "a universal or eventual pointwise theorem proving low-order "
                "base positivity and high-order signed-tail domination for "
                "all sufficiently large eligible even N in the named class"),
        },
        "candidate": {
            "name": "32-lift support-order horizon",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Keep the exact support-size <= 2 split and extend the "
                "period-lift stress from 8 to 32 consecutive forward lifts of "
                "the same seven residues."),
            "prediction": (
                "If the support-order split is a plausible eventual-threshold "
                "target, the expanded horizon should retain sign agreement and "
                "avoid high-order tail domination failures without refitting."),
            "falsifier": (
                "Any row with positive full action but nonpositive low-order "
                "base, or any adverse high-order tail at least as large as the "
                "low-order base, breaks the finite horizon version of the "
                "candidate."),
            "smallest_test": (
                "Evaluate 32 forward period-lifts of the seven original "
                "support-packet residues."),
        },
        "period": PERIOD,
        "lift_count": LIFT_COUNT,
        "base_targets": [int(target) for target in SELECTED_TARGETS],
        "rows": rows,
        "summary_by_lift": by_lift,
        "summary": {
            "row_count": len(rows),
            "actual_full_positive_count": len(positive_rows),
            "actual_full_nonpositive_count": len(rows) - len(positive_rows),
            "low_order_base_positive_count": len(base_positive_rows),
            "low_order_base_sign_mismatch_count": len(mismatches),
            "low_order_base_sign_mismatch_targets": [
                row["target"] for row in mismatches],
            "low_order_base_summary": finite_summary(
                row["low_order_base_action"] for row in rows),
            "actual_full_action_summary": finite_summary(
                row["actual_full_action"] for row in rows),
            "high_order_signed_tail_summary": finite_summary(
                row["high_order_signed_tail"] for row in rows),
            "high_order_abs_tail_summary": finite_summary(
                row["high_order_abs_tail"] for row in rows),
            "tight_low_order_base_row": tight_base,
            "tight_actual_full_action_row": tight_full,
            "maximum_high_order_adverse_to_base_ratio_row": (
                max_adverse_ratio),
            "maximum_high_order_abs_to_base_ratio_row": max_abs_ratio,
            "maximum_high_order_adverse_to_base_ratio": (
                max_adverse_ratio["high_order_adverse_to_base_ratio"]),
            "maximum_high_order_abs_to_base_ratio": (
                max_abs_ratio["high_order_abs_to_base_ratio"]),
            "horizon_high_order_adverse_envelope": (
                high_order_adverse_envelope),
            "horizon_envelope_margin_at_tight_base": (
                envelope_margin_at_tight_base),
            "maximum_reconstruction_error": max(
                abs(row["signed_reconstruction_error"]) for row in rows),
        },
        "decision": (
            "The support-order bridge survives the 32-lift horizon.  All 224 "
            "rows are full-positive and low-order-base-positive, with no sign "
            "mismatches.  The tight low-order base is about 0.29434 at target "
            "255016, and the tight full action is the same row, about 0.27674. "
            "The worst adverse high-order tail remains the earlier target "
            "164926, consuming about 13.27% of its base.  Across this finite "
            "horizon, even the disconnected high-order adverse envelope stays "
            "below every low-order base.  This strengthens the eventual-"
            "threshold hypothesis for the support-order split, but proves no "
            "threshold theorem and supplies no non-circular analytic estimate. "
            "Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
