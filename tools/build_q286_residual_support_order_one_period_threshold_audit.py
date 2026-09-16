"""One-period threshold contrast for the q286 support-order bridge.

The original support-order fixture survived only as a signed-tail bridge: the
all-row high-order adverse envelope was too large for the tight positive base.
The 32-lift horizon showed that the same disconnected high-order envelope test
survives after one full period.  This receipt compares those two states.

Finite threshold-contrast audit only.  It proves no eventual-threshold theorem,
low-order base theorem, high-order tail domination theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
FIXTURE_SOURCE = EVIDENCE / "q286-residual-support-order-sign-bridge-audit.json"
HORIZON_SOURCE = (
    EVIDENCE / "q286-residual-support-order-period-lift-horizon.json")
OUT = EVIDENCE / "q286-residual-support-order-one-period-threshold-audit.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    fixture = load_json(FIXTURE_SOURCE)
    horizon = load_json(HORIZON_SOURCE)
    fixture_summary = fixture["summary"]
    horizon_summary = horizon["summary"]

    fixture_tight = fixture_summary["tight_low_order_base_positive_row"]
    horizon_tight = horizon_summary["tight_low_order_base_row"]
    fixture_envelope = fixture_summary["all_row_high_order_adverse_envelope"]
    horizon_envelope = horizon_summary["horizon_high_order_adverse_envelope"]
    fixture_margin = (
        fixture_summary[
            "all_row_high_order_envelope_margin_at_tight_positive_base"])
    horizon_margin = horizon_summary["horizon_envelope_margin_at_tight_base"]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "support_order_sign_bridge": str(FIXTURE_SOURCE.relative_to(ROOT)),
            "support_order_sign_bridge_status": fixture["status"],
            "period_lift_horizon": str(HORIZON_SOURCE.relative_to(ROOT)),
            "period_lift_horizon_status": horizon["status"],
        },
        "status": "CANDIDATE_one_period_threshold_removes_high_order_envelope_obstruction",
        "status_boundary": (
            "finite threshold-contrast audit only; no eventual-threshold "
            "theorem, low-order base theorem, high-order tail domination "
            "theorem, q286 threshold theorem, strict-central Goldbach theorem, "
            "or Goldbach proof"),
        "goldbach_proved": False,
        "eventual_threshold_theorem_proved": False,
        "low_order_base_theorem_proved": False,
        "high_order_tail_domination_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "universal_bound_open": True,
        "acceptance_condition": {
            "finite_evidence_is_acceptance_condition": False,
            "required_acceptance_condition": (
                "prove analytically that after the named one-period threshold "
                "the low-order base stays positive and the high-order tail "
                "envelope or signed tail stays below that base for every "
                "eligible target in the class"),
        },
        "candidate": {
            "name": "one-period support-order threshold",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use the original seven-row fixture as the finite remainder "
                "and test whether one full period lift moves the same residue "
                "classes into a regime where even the disconnected high-order "
                "adverse envelope is below every low-order base."),
            "prediction": (
                "The k=0 fixture should expose the envelope obstruction, while "
                "the k>=1 horizon should remove it without changing the "
                "support-size <=2 split."),
            "falsifier": (
                "If any k>=1 horizon row has nonpositive low-order base, a "
                "sign mismatch, or high-order envelope at least as large as "
                "the low-order base, the one-period threshold candidate fails "
                "on the checked horizon."),
            "smallest_test": (
                "Compare the original seven-row support-order fixture against "
                "the 32-lift horizon using the same disconnected high-order "
                "adverse envelope criterion."),
        },
        "threshold_convention": {
            "period": horizon["period"],
            "fixture_lift": 0,
            "horizon_lift_range": [1, horizon["lift_count"]],
            "low_order_base": (
                "aligned_only_full_action + support-size <= 2 packets"),
            "high_order_tail": "support-size >= 3 packets",
        },
        "fixture": {
            "row_count": fixture_summary["row_count"],
            "actual_full_positive_count": (
                fixture_summary["actual_full_positive_count"]),
            "low_order_base_positive_count": (
                fixture_summary["low_order_base_positive_count"]),
            "sign_mismatch_count": (
                fixture_summary["low_order_base_sign_mismatch_count"]),
            "tight_positive_target": fixture_tight["target"],
            "tight_low_order_base": fixture_tight["low_order_base_action"],
            "tight_full_action": fixture_tight["actual_full_action"],
            "high_order_adverse_envelope": fixture_envelope,
            "envelope_margin_at_tight_base": fixture_margin,
            "maximum_adverse_to_base_ratio": (
                fixture_summary[
                    "maximum_high_order_adverse_to_base_ratio_on_base_positive_rows"]),
            "envelope_survives": fixture_margin > 0.0,
        },
        "horizon": {
            "row_count": horizon_summary["row_count"],
            "actual_full_positive_count": (
                horizon_summary["actual_full_positive_count"]),
            "low_order_base_positive_count": (
                horizon_summary["low_order_base_positive_count"]),
            "sign_mismatch_count": (
                horizon_summary["low_order_base_sign_mismatch_count"]),
            "tight_low_order_base_target": horizon_tight["target"],
            "tight_low_order_base": horizon_tight["low_order_base_action"],
            "tight_full_action": horizon_tight["actual_full_action"],
            "high_order_adverse_envelope": horizon_envelope,
            "envelope_margin_at_tight_base": horizon_margin,
            "maximum_adverse_to_base_ratio": (
                horizon_summary["maximum_high_order_adverse_to_base_ratio"]),
            "envelope_survives": horizon_margin > 0.0,
        },
        "summary": {
            "fixture_envelope_survives": fixture_margin > 0.0,
            "horizon_envelope_survives": horizon_margin > 0.0,
            "one_period_threshold_candidate_survives_checked_horizon": (
                fixture_margin <= 0.0 and horizon_margin > 0.0),
            "fixture_envelope_margin": fixture_margin,
            "horizon_envelope_margin": horizon_margin,
            "fixture_tight_low_order_base": (
                fixture_tight["low_order_base_action"]),
            "horizon_tight_low_order_base": (
                horizon_tight["low_order_base_action"]),
            "base_growth_factor_vs_fixture_tight": (
                horizon_tight["low_order_base_action"]
                / fixture_tight["low_order_base_action"]),
            "adverse_ratio_drop_factor": (
                fixture_summary[
                    "maximum_high_order_adverse_to_base_ratio_on_base_positive_rows"]
                / horizon_summary["maximum_high_order_adverse_to_base_ratio"]),
        },
        "decision": (
            "The one-period threshold contrast survives as finite evidence.  "
            "At lift 0, the support-order split has correct signed structure, "
            "but the disconnected high-order adverse envelope fails: the "
            "tight positive base is about 0.05371 while the all-row high-order "
            "adverse envelope is about 0.23468.  Across lifts 1..32, the "
            "same fixed split has 224 positive low-order bases, no sign "
            "mismatches, and the high-order adverse envelope is only about "
            "0.06972 against a tight base about 0.29434.  This suggests a "
            "finite-remainder plus one-period-threshold theorem shape for "
            "these seven residue classes, but proves no such theorem and "
            "does not address all even N.  Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
