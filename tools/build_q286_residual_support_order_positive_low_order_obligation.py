"""Classify the positive low-order obligation in the raw ratio route.

The adverse-ratio target is sufficient only with B_low_raw(N)>0.  This receipt
records what that condition means in the current raw-scale bridge:

    B_low_raw(N)
      = normalized_low_order_base(N) * principal_mean * total_weight(N).

Thus a normalized low-order positivity theorem would still need positive
strict-central mass, while a direct raw B_low_raw(N)>0 theorem already implies
nonempty support.  This is a theorem-target classifier only.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
RAW_SCALE_SOURCE = EVIDENCE / "q286-residual-support-order-raw-scale-bridge.json"
ADVERSE_RATIO_SOURCE = (
    EVIDENCE / "q286-residual-support-order-raw-adverse-ratio-target.json")
OUT = EVIDENCE / "q286-residual-support-order-positive-low-order-obligation.json"


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
    return {
        "target": int(row["target"]),
        "target_mod_286": int(row["target_mod_286"]),
        "target_mod_period": int(row["target_mod_period"]),
        "lift_index": int(row["lift_index"]),
        "ordered_central_prime_pair_count": int(
            row["ordered_central_prime_pair_count"]),
        "strict_central_total_weight": float(
            row["strict_central_total_weight"]),
        "principal_scale": float(row["principal_scale"]),
        "normalized_low_order_base": float(row["normalized_low_order_base"]),
        "raw_low_order_base": float(row["raw_low_order_base"]),
        "raw_adverse_drag": float(row["raw_adverse_drag"]),
        "raw_pointwise_margin": float(row["raw_pointwise_margin"]),
    }


def build_receipt():
    raw = load_json(RAW_SCALE_SOURCE)
    adverse = load_json(ADVERSE_RATIO_SOURCE)
    rows = raw["rows"]
    nonpositive_raw_low = [
        row for row in rows if float(row["raw_low_order_base"]) <= 0.0]
    nonpositive_normalized_low = [
        row for row in rows if float(row["normalized_low_order_base"]) <= 0.0]
    smallest_raw_low = min(
        rows, key=lambda row: (
            float(row["raw_low_order_base"]), int(row["target"])))
    smallest_normalized_low = min(
        rows, key=lambda row: (
            float(row["normalized_low_order_base"]), int(row["target"])))
    smallest_weight = min(
        rows, key=lambda row: (
            float(row["strict_central_total_weight"]), int(row["target"])))
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "raw_scale_bridge": str(RAW_SCALE_SOURCE.relative_to(ROOT)),
            "raw_adverse_ratio_target": str(
                ADVERSE_RATIO_SOURCE.relative_to(ROOT)),
        },
        "status": "TARGET_positive_low_order_is_support_strength",
        "status_boundary": (
            "logical positive-low-order obligation classifier only; no "
            "positive low-order theorem, positive-mass theorem, raw "
            "adverse-ratio theorem, raw lower-bound theorem, q286 threshold "
            "theorem, strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "positive_low_order_theorem_proved": False,
        "normalized_low_order_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "raw_adverse_ratio_theorem_proved": False,
        "raw_lower_bound_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "identity": {
            "raw_low_order_base": (
                "B_low_raw(N)=b_low_norm(N)*principal_mean*"
                "strict_central_total_weight(N)"),
            "principal_mean_real": float(raw["normalization_identity"][
                "principal_mean_real"]),
            "principal_mean_positive_on_current_context": bool(
                raw["normalization_identity"][
                    "principal_mean_positive_on_current_context"]),
            "zero_support_implication": (
                "If strict-central support is empty, "
                "strict_central_total_weight(N)=0, so B_low_raw(N)=0."),
        },
        "theorem_obligation": {
            "direct_raw_statement": (
                "Prove B_low_raw(N)>0 for every sufficiently large eligible "
                "N in the named q286 support-order period classes."),
            "factored_route_requirements": [
                "prove b_low_norm(N)>0 uniformly on the eligible classes",
                "prove strict_central_total_weight(N)>0 on the eligible classes",
                "prove principal_mean>0 in the relevant fixed context",
            ],
            "why_normalized_low_is_not_enough": (
                "Even a uniform theorem b_low_norm(N)>0 does not create "
                "prime-pair mass.  Multiplication by total_weight(N) still "
                "vanishes when strict-central support is empty."),
            "why_raw_low_positive_is_support_strength": (
                "A direct theorem B_low_raw(N)>0 forces at least one raw "
                "prime-pair contribution in this witness family, hence "
                "nonempty strict-central support."),
            "relationship_to_ratio_route": (
                adverse["route_decision"]["recommended_next"]),
        },
        "finite_calibration": {
            "finite_evidence_is_acceptance_condition": False,
            "row_count": len(rows),
            "positive_raw_low_order_rows": len(rows) - len(nonpositive_raw_low),
            "nonpositive_raw_low_order_targets": [
                int(row["target"]) for row in nonpositive_raw_low],
            "positive_normalized_low_order_rows": (
                len(rows) - len(nonpositive_normalized_low)),
            "nonpositive_normalized_low_order_targets": [
                int(row["target"]) for row in nonpositive_normalized_low],
            "raw_low_order_summary": finite_summary(
                row["raw_low_order_base"] for row in rows),
            "normalized_low_order_summary": finite_summary(
                row["normalized_low_order_base"] for row in rows),
            "strict_central_total_weight_summary": raw["finite_horizon"][
                "total_weight_summary"],
            "smallest_raw_low_order_row": compact_row(smallest_raw_low),
            "smallest_normalized_low_order_row": compact_row(
                smallest_normalized_low),
            "smallest_total_weight_row": compact_row(smallest_weight),
        },
        "route_decision": {
            "positive_low_order_can_replace_positive_mass": False,
            "direct_raw_low_order_positive_subsumes_support": True,
            "normalized_low_order_positive_still_needs_positive_mass": True,
            "split_ratio_route_has_two_goldbach_strength_inputs": True,
            "single_raw_lower_bound_remains_preferred": True,
            "recommended_next": (
                "Do not split the proof into ratio plus positive low-order "
                "unless there is an actual analytic lower bound for "
                "B_low_raw(N)>0 or for total_weight(N)>0.  The cleaner target "
                "remains the direct raw inequality R_raw(N)>0."),
        },
        "decision": (
            "The positive low-order requirement is now classified.  The "
            "checked rows all have B_low_raw(N)>0, and all have positive "
            "normalized low-order base, but the identity "
            "B_low_raw=b_low_norm*principal_mean*total_weight shows why this "
            "does not evade the support problem.  Normalized low-order "
            "positivity still needs positive strict-central mass; direct raw "
            "low-order positivity already implies nonempty support.  The "
            "split adverse-ratio route therefore has two theorem-strength "
            "inputs, so the single raw lower-bound theorem remains cleaner."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
