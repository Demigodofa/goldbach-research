"""Classify the raw adverse-ratio theorem route.

The raw phase-space locator exposed a natural finite stress statistic:

    D_high_minus_raw(N) / B_low_raw(N).

This receipt records the exact theorem shape that would make that statistic
useful.  It is a logical target and finite calibration only; it proves no
adverse-ratio theorem, raw lower-bound theorem, positive-mass theorem, or
Goldbach result.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
PHASE_SOURCE = (
    EVIDENCE / "q286-residual-support-order-raw-bound-phase-space.json")
RAW_TARGET_SOURCE = (
    EVIDENCE / "q286-residual-support-order-single-raw-bound-target.json")
OUT = EVIDENCE / "q286-residual-support-order-raw-adverse-ratio-target.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def finite_summary(values):
    values = [float(value) for value in values]
    return {
        "count": len(values),
        "minimum": min(values),
        "mean": sum(values) / len(values),
        "maximum": max(values),
    }


def compact_row(row):
    ratio = float(row["adverse_drag_ratio_to_low_order"] or 0.0)
    return {
        "target": int(row["target"]),
        "target_mod_286": int(row["color_target_mod_286"]),
        "target_mod_period": int(row["color_target_mod_period"]),
        "lift_index": int(row["lift_index"]),
        "ordered_central_prime_pair_count": int(
            row["y_ordered_central_prime_pair_count"]),
        "strict_central_total_weight": float(
            row["strict_central_total_weight"]),
        "raw_low_order_base": float(row["raw_low_order_base"]),
        "raw_adverse_drag": float(row["raw_adverse_drag"]),
        "raw_high_order_tail": float(row["raw_high_order_tail"]),
        "raw_pointwise_margin": float(row["z_raw_pointwise_margin"]),
        "adverse_drag_ratio_to_low_order": ratio,
        "ratio_slack_to_one": 1.0 - ratio,
    }


def build_receipt():
    phase = load_json(PHASE_SOURCE)
    single_raw = load_json(RAW_TARGET_SOURCE)
    rows = phase["phase_space_points"]
    ratios = [
        float(row["adverse_drag_ratio_to_low_order"] or 0.0)
        for row in rows
    ]
    nonzero_adverse = [
        row for row in rows if float(row["raw_adverse_drag"]) > 0.0]
    positive_low = [
        row for row in rows if float(row["raw_low_order_base"]) > 0.0]
    smallest_low = min(
        rows, key=lambda row: (
            float(row["raw_low_order_base"]), int(row["target"])))
    largest_ratio = max(
        rows, key=lambda row: (
            float(row["adverse_drag_ratio_to_low_order"] or 0.0),
            -int(row["target"])))
    tightest_raw_margin = min(
        rows, key=lambda row: (
            float(row["z_raw_pointwise_margin"]), int(row["target"])))
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "raw_bound_phase_space": str(PHASE_SOURCE.relative_to(ROOT)),
            "single_raw_bound_target": str(
                RAW_TARGET_SOURCE.relative_to(ROOT)),
        },
        "status": "TARGET_raw_adverse_ratio_plus_positive_low_order",
        "status_boundary": (
            "logical theorem-target and finite calibration only; no raw "
            "adverse-ratio theorem, positive low-order theorem, raw "
            "lower-bound theorem, q286 threshold theorem, strict-central "
            "Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "raw_adverse_ratio_theorem_proved": False,
        "positive_low_order_theorem_proved": False,
        "raw_lower_bound_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "theorem_target": {
            "eligible_domain": single_raw["theorem_target"][
                "eligible_domain"],
            "raw_low_order_base": "B_low_raw(N)",
            "raw_adverse_drag": "D_high_minus_raw(N)=max(0,-T_high_raw(N))",
            "ratio": "rho_raw(N)=D_high_minus_raw(N)/B_low_raw(N)",
            "sufficient_conditions": [
                "B_low_raw(N)>0",
                "rho_raw(N)<=rho_*<1 for every sufficiently large eligible N",
            ],
            "conclusion": (
                "R_raw(N)=B_low_raw(N)*(1-rho_raw(N))>0, hence the raw "
                "support-order witness is positive."),
            "zero_support_boundary": (
                "If strict-central support is empty, all raw prime-pair sums "
                "in this witness vanish.  Then B_low_raw(N)=0 and the ratio "
                "is undefined rather than a shortcut.  A theorem proving "
                "B_low_raw(N)>0 is already support/existence-strength for "
                "this witness family."),
            "safe_use": (
                "Use the ratio target only together with an independent raw "
                "positive low-order lower bound, or fold both into one direct "
                "raw witness lower-bound theorem."),
        },
        "finite_calibration": {
            "finite_evidence_is_acceptance_condition": False,
            "row_count": len(rows),
            "positive_low_order_rows": len(positive_low),
            "nonpositive_low_order_targets": [
                int(row["target"]) for row in rows
                if float(row["raw_low_order_base"]) <= 0.0],
            "zero_adverse_drag_rows": len(rows) - len(nonzero_adverse),
            "nonzero_adverse_drag_rows": len(nonzero_adverse),
            "ratio_less_than_one_rows": sum(ratio < 1.0 for ratio in ratios),
            "ratio_not_less_than_one_targets": [
                int(row["target"]) for row, ratio in zip(rows, ratios)
                if ratio >= 1.0],
            "adverse_ratio_summary": finite_summary(ratios),
            "ratio_slack_to_one_summary": finite_summary(
                1.0 - ratio for ratio in ratios),
            "smallest_low_order_row": compact_row(smallest_low),
            "largest_adverse_ratio_row": compact_row(largest_ratio),
            "tightest_raw_margin_row": compact_row(tightest_raw_margin),
        },
        "route_decision": {
            "ratio_route_is_valid_sufficient_shape": True,
            "ratio_route_requires_positive_low_order": True,
            "positive_low_order_is_not_a_minor_side_condition": True,
            "single_raw_lower_bound_remains_cleaner": True,
            "recommended_next": (
                "Try to prove a raw positive low-order lower bound and a "
                "same-scale adverse-ratio upper bound only if both can be "
                "stated without dividing by an unproved mass.  Otherwise keep "
                "the single raw lower-bound target as the cleaner theorem."),
        },
        "decision": (
            "The adverse-ratio statistic is a useful theorem target, not a "
            "proof.  On the checked horizon the worst ratio is about "
            "0.132663 at target 164926, far below 1, but a universal ratio "
            "bound only proves positivity when paired with "
            "B_low_raw(N)>0.  Since zero strict-central support makes "
            "B_low_raw vanish, the positive low-order condition is "
            "support-strength, not a cheap side condition.  The clean route "
            "therefore remains a direct raw lower-bound theorem unless an "
            "independent raw low-order lower bound is proved."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
