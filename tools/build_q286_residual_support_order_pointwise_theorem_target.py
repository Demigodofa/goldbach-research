"""Pointwise theorem target for the q286 support-order route.

The period-lift evidence made the theorem shape sharper, but finite rows are
not the acceptance condition.  This receipt freezes the actual proof target:
after one full period, prove low-order base positivity and same-row high-order
tail domination by an external pointwise analytic estimate.

Logical/theorem-target audit only.  It proves no pointwise estimate, no
one-period threshold theorem, no q286 threshold theorem, and no Goldbach proof.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SIGN_SOURCE = EVIDENCE / "q286-residual-support-order-sign-bridge-audit.json"
HORIZON_SOURCE = (
    EVIDENCE / "q286-residual-support-order-period-lift-horizon.json")
THRESHOLD_SOURCE = (
    EVIDENCE / "q286-residual-support-order-one-period-threshold-audit.json")
L2_STATUS_SOURCE = EVIDENCE / "q286-active-selector-l2-bridge-status-audit.json"
OUT = EVIDENCE / "q286-residual-support-order-pointwise-theorem-target.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def row_margin(row):
    adverse = max(0.0, -float(row["high_order_signed_tail"]))
    base = float(row["low_order_base_action"])
    return {
        "target": int(row["target"]),
        "base_target": int(row.get("base_target", row["target"])),
        "lift_index": int(row.get("lift_index", 0)),
        "target_mod_period": int(row.get("target_mod_period",
                                         row["target_residue"])),
        "target_mod_286": int(row["target_mod_286"]),
        "low_order_base_action": base,
        "high_order_signed_tail": float(row["high_order_signed_tail"]),
        "same_row_adverse_drag": adverse,
        "pointwise_domination_margin": base - adverse,
        "actual_full_action": float(row["actual_full_action"]),
        "actual_full_positive": bool(row["actual_full_positive"]),
        "low_order_base_positive": bool(row["low_order_base_positive"]),
        "tail_domination_holds": bool(base > adverse),
    }


def fields_present(rows):
    keys = set()
    for row in rows:
        keys.update(row)
    return sorted(keys)


def build_receipt():
    sign = load_json(SIGN_SOURCE)
    horizon = load_json(HORIZON_SOURCE)
    threshold = load_json(THRESHOLD_SOURCE)
    l2_status = load_json(L2_STATUS_SOURCE)

    fixture_rows = [row_margin(row) for row in sign["rows"]]
    horizon_rows = [row_margin(row) for row in horizon["rows"]]
    horizon_failures = [
        row for row in horizon_rows
        if not (row["low_order_base_positive"]
                and row["tail_domination_holds"])
    ]
    fixture_positive_failures = [
        row for row in fixture_rows
        if row["actual_full_positive"] and not row["tail_domination_holds"]
    ]
    raw_count_fields = [
        field for field in fields_present(horizon["rows"])
        if "count" in field.lower() or "mass" in field.lower()
    ]
    tight_pointwise = min(
        horizon_rows,
        key=lambda row: (row["pointwise_domination_margin"], row["target"]),
    )
    tight_base = horizon["summary"]["tight_low_order_base_row"]
    worst_ratio = horizon["summary"][
        "maximum_high_order_adverse_to_base_ratio_row"]

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "support_order_sign_bridge": str(SIGN_SOURCE.relative_to(ROOT)),
            "period_lift_horizon": str(HORIZON_SOURCE.relative_to(ROOT)),
            "one_period_threshold_contrast": str(
                THRESHOLD_SOURCE.relative_to(ROOT)),
            "l2_bridge_status": str(L2_STATUS_SOURCE.relative_to(ROOT)),
        },
        "status": "TARGET_pointwise_support_order_theorem_required",
        "status_boundary": (
            "theorem-target/logical audit only; no pointwise analytic "
            "estimate, one-period threshold theorem, low-order base theorem, "
            "high-order tail domination theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "pointwise_analytic_estimate_proved": False,
        "one_period_threshold_theorem_proved": False,
        "low_order_base_theorem_proved": False,
        "high_order_tail_domination_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "acceptance_condition": {
            "finite_evidence_is_acceptance_condition": False,
            "required_acceptance_condition": (
                "For every sufficiently large eligible target in the named "
                "period classes, prove analytically and pointwise that "
                "B_low(N)>0 and D_high_minus(N)<B_low(N), where "
                "D_high_minus(N)=max(0,-T_high(N)).  A finite initial range "
                "may only serve as a separate remainder check."),
            "unnormalized_requirement": (
                "The proof must be stated for the actual unnormalized "
                "binary-prime sums or must explicitly multiply the normalized "
                "action identity by a separately proved positive mass.  The "
                "current support-order receipts do not carry a raw pair-count "
                "or raw mass theorem."),
        },
        "theorem_target": {
            "period": int(horizon["period"]),
            "eligible_base_targets": horizon["base_targets"],
            "eligible_lifts": "k >= 1 after separate finite-remainder check",
            "low_order_base": (
                "B_low(N) = aligned_only_full_action(N) + sum support-size "
                "<= 2 signed packets"),
            "high_order_tail": (
                "T_high(N) = sum support-size >= 3 signed packets"),
            "adverse_drag": "D_high_minus(N) = max(0, -T_high(N))",
            "sufficient_pointwise_inequality": (
                "B_low(N)>0 and D_high_minus(N)<B_low(N) imply "
                "B_low(N)+T_high(N)>0 on the support-order witness."),
            "why_same_row_is_weaker_than_disconnected_envelope": (
                "The previous envelope summed the worst observed adverse tail "
                "from any row against every row.  A theorem only needs "
                "same-row domination, but it must be analytic and universal."),
        },
        "finite_calibration": {
            "fixture_lift_zero": {
                "row_count": len(fixture_rows),
                "actual_full_positive_count": sign["summary"][
                    "actual_full_positive_count"],
                "positive_rows_failing_same_row_domination": [
                    row["target"] for row in fixture_positive_failures],
                "disconnected_envelope_survives": threshold["summary"][
                    "fixture_envelope_survives"],
                "interpretation": (
                    "lift 0 remains a finite fixture/remainder object, not "
                    "the proposed eventual theorem regime"),
            },
            "horizon_lifts_1_to_32": {
                "row_count": len(horizon_rows),
                "same_row_pointwise_failures": [
                    row["target"] for row in horizon_failures],
                "same_row_pointwise_fail_count": len(horizon_failures),
                "tight_pointwise_domination_row": tight_pointwise,
                "tight_low_order_base_row": {
                    "target": int(tight_base["target"]),
                    "lift_index": int(tight_base["lift_index"]),
                    "low_order_base_action": float(
                        tight_base["low_order_base_action"]),
                    "actual_full_action": float(
                        tight_base["actual_full_action"]),
                },
                "worst_high_order_adverse_to_base_ratio_row": {
                    "target": int(worst_ratio["target"]),
                    "lift_index": int(worst_ratio["lift_index"]),
                    "ratio": float(
                        worst_ratio["high_order_adverse_to_base_ratio"]),
                    "low_order_base_action": float(
                        worst_ratio["low_order_base_action"]),
                    "high_order_signed_tail": float(
                        worst_ratio["high_order_signed_tail"]),
                },
                "disconnected_envelope_margin": threshold["summary"][
                    "horizon_envelope_margin"],
                "disconnected_envelope_survives": threshold["summary"][
                    "horizon_envelope_survives"],
            },
            "logical_boundary": (
                "These rows are calibration and falsifier evidence.  They do "
                "not prove the required pointwise estimate for all large N."),
        },
        "normalization_and_zero_mass_boundary": {
            "raw_count_or_mass_fields_present_in_horizon_rows": (
                raw_count_fields),
            "raw_unnormalized_pair_count_theorem_present": False,
            "zero_mass_check_transfers_from_l2_route": False,
            "l2_status_short_answer": l2_status["short_answer"],
            "l2_zero_mass_meaning": l2_status["zero_mass_status"]["meaning"],
            "decision": (
                "The old L2 route remains only a valid non-circular premise "
                "if externally proved; it is not confirmed and it does not "
                "prove existence when the normalizing mass is zero.  The "
                "support-order route must therefore carry either an "
                "unnormalized pointwise estimate or a separate positive-mass "
                "theorem before any normalized action inequality can be "
                "promoted."),
        },
        "next_proof_obligations": [
            "Define the unnormalized support-order witness terms behind "
            "B_low(N) and T_high(N).",
            "Prove the positive-mass/nonzero strict-central denominator needed "
            "to pass between raw sums and normalized action scale, or avoid "
            "normalization entirely.",
            "Prove B_low(N)>0 for every sufficiently large eligible target in "
            "the seven named period classes.",
            "Prove max(0,-T_high(N))<B_low(N) same-row and pointwise for every "
            "sufficiently large eligible target.",
            "Verify the finite initial range separately; do not use it as the "
            "asymptotic acceptance condition.",
        ],
        "decision": (
            "Finite evidence is now demoted to calibration/falsifier status "
            "for the support-order lane.  The evidence identifies a precise "
            "candidate theorem after one period, but the missing bridge is an "
            "unnormalized pointwise analytic estimate or an equivalent "
            "positive-mass plus normalized-action theorem.  The L2 zero-mass "
            "audit does not fill this bridge.  Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
