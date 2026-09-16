"""Build the current Goldbach bridge acceptance-gate audit.

This derived receipt keeps three nearby facts separate:

* zero-mass arithmetic sanity for the q286 L2 lane,
* non-circular theorem shapes that are still unproved,
* finite diagnostics that are useful but not acceptance.

It proves no Goldbach theorem.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
L2_BRIDGE = EVIDENCE / "q286-wbss-zero-mass-l2-logical-bridge-audit.json"
POINTWISE_ADVERSE = EVIDENCE / "q286-wbss-pointwise-adverse-drag-theorem-target.json"
RAW_ADVERSE = EVIDENCE / "q286-wbss-raw-adverse-drag-theorem-target.json"
SOURCE_WINDOW = (
    EVIDENCE / "mobius-moment-square-degree5-source-admissible-window-audit.json")
OUT = EVIDENCE / "goldbach-bridge-acceptance-gate-audit.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    l2 = load_json(L2_BRIDGE)
    pointwise = load_json(POINTWISE_ADVERSE)
    raw = load_json(RAW_ADVERSE)
    source = load_json(SOURCE_WINDOW)

    l2_classification = l2["l2_bridge_classification"]
    l2_failures = l2["observed_l2_failures"]
    pointwise_summary = pointwise["finite_calibration"]["summary"]
    raw_summary = raw["finite_calibration"]["summary"]

    live_gate = (
        "Prove a universal pointwise unnormalized estimate, preferably "
        "A_raw_-(N) < L_raw(N) or equivalently adverse_drag(N) < "
        "local_main(N), for every sufficiently large covered even N; then "
        "verify the finite remainder independently.")

    return {
        "schema_version": 1,
        "status": "GATE_current_goldbach_bridge_acceptance",
        "source_commit": source_commit(),
        "sources": {
            "l2_bridge": str(L2_BRIDGE.relative_to(ROOT)),
            "l2_bridge_status": l2["status"],
            "pointwise_adverse_drag": str(
                POINTWISE_ADVERSE.relative_to(ROOT)),
            "raw_adverse_drag": str(RAW_ADVERSE.relative_to(ROOT)),
            "source_admissible_window": str(SOURCE_WINDOW.relative_to(ROOT)),
            "source_admissible_window_status": source["status"],
        },
        "question": (
            "What is currently accepted as a logical bridge toward Goldbach, "
            "and what remains only finite arithmetic or theorem-shaped but "
            "unproved evidence?"),
        "answer": (
            "The checked zero-mass arithmetic audit is real but finite; the "
            "raw strict aggregate-L2 shape is non-circular as a theorem "
            "shape but its bridge is not confirmed; normalized observed L2 "
            "already has finite cap violations.  The live bridge target is "
            "a universal pointwise unnormalized adverse-drag estimate.  The "
            "metric-soft source-window audit is useful source-window "
            "evidence, not a Goldbach bridge by itself."),
        "bridge_table": [
            {
                "route": "q286 raw adverse-drag",
                "state": "live_theorem_target",
                "non_circular_shape": True,
                "logical_bridge_confirmed": False,
                "finite_evidence_role": "calibration_and_falsifier_only",
                "required_universal_statement": raw[
                    "acceptance_condition"][
                        "required_universal_statement"],
                "checked_row_count": raw_summary["row_count"],
                "finite_rows_pass_gate": (
                    raw_summary[
                        "raw_adverse_drag_not_below_raw_local_main_count"]
                    == 0),
                "worst_checked_ratio": raw_summary[
                    "raw_adverse_drag_ratio_summary"]["maximum"],
                "worst_checked_target": raw_summary[
                    "largest_raw_adverse_drag_ratio_row"]["target"],
                "theorem_proved": raw["raw_adverse_drag_theorem_proved"],
            },
            {
                "route": "q286 normalized/aggregate L2",
                "state": "hold_not_confirmed",
                "non_circular_shape": l2_classification[
                    "raw_strict_aggregate_l2_shape_is_noncircular"],
                "logical_bridge_confirmed": l2_classification[
                    "logical_bridge_confirmed"],
                "finite_evidence_role": (
                    "zero_mass_sanity_only; observed_normalized_cap_has_"
                    "violations"),
                "checked_row_count": l2_failures["row_count"],
                "row_local_cap_violations": l2_failures[
                    "row_local_cap_exceeding_row_count"],
                "global_min_cap_violations": l2_failures[
                    "global_min_cap_exceeding_row_count"],
                "worst_row_local_ratio": l2_failures[
                    "worst_row_local_ratio"],
                "theorem_proved": l2["aggregate_l2_theorem_proved"],
            },
            {
                "route": "metric-soft source-admissible window",
                "state": "finite_source_window_evidence",
                "non_circular_shape": None,
                "logical_bridge_confirmed": False,
                "finite_evidence_role": (
                    "source-window/admissible-window diagnostic only"),
                "checked_start_count": source["total_active_row_starts"],
                "failing_start_count": source[
                    "failing_active_row_start_count"],
                "source_start_failure_count": source[
                    "source_start_failure_count"],
                "minimum_source_start_slack": source[
                    "minimum_source_start_canonical_slack"],
                "theorem_proved": source[
                    "source_admissible_window_theorem_proved"],
            },
        ],
        "zero_mass_l2_status": {
            "zero_mass_arithmetic_sanity_confirmed_on_checked_rows": l2[
                "zero_mass_check"][
                    "arithmetic_sanity_confirmed_on_checked_rows"],
            "raw_strict_l2_shape_is_noncircular": l2_classification[
                "raw_strict_aggregate_l2_shape_is_noncircular"],
            "l2_logical_bridge_confirmed": l2_classification[
                "logical_bridge_confirmed"],
            "observed_row_local_cap_violations": l2_failures[
                "row_local_cap_exceeding_row_count"],
            "observed_global_min_cap_violations": l2_failures[
                "global_min_cap_exceeding_row_count"],
        },
        "pointwise_adverse_drag_status": {
            "required_statement": pointwise["acceptance_condition"][
                "required_universal_statement"],
            "finite_evidence_is_acceptance_condition": pointwise[
                "acceptance_condition"][
                    "finite_evidence_is_acceptance_condition"],
            "checked_rows": pointwise_summary["row_count"],
            "checked_rows_with_adverse_below_local": pointwise_summary[
                "adverse_drag_below_local_main_count"],
            "checked_rows_failing_adverse_below_local": pointwise_summary[
                "adverse_drag_not_below_local_main_count"],
            "worst_checked_ratio": pointwise_summary[
                "adverse_drag_ratio_summary"]["maximum"],
            "worst_checked_target": pointwise_summary[
                "tightest_adverse_drag_row"]["target"],
            "universal_bound_open": pointwise["universal_bound_open"],
        },
        "metric_soft_source_window_status": {
            "broad_all_translation_quantifier_falsified": (
                source["broad_failure_row_count"] > 0),
            "all_source_starts_pass": source["all_source_starts_pass"],
            "failing_translated_start_count": source[
                "failing_active_row_start_count"],
            "source_start_failure_count": source[
                "source_start_failure_count"],
            "role": (
                "Finite source-window guidance for a local theorem target; "
                "not a logical bridge to Goldbach without a separate "
                "source-backed implication."),
        },
        "acceptance_gate": {
            "finite_evidence_is_acceptance_condition": False,
            "current_required_bridge": live_gate,
            "invalid_closeouts": [
                "checked-row zero-mass sanity alone",
                "normalized L2 after assuming positive mass",
                "another finite horizon pass",
                "fitted residual constants such as .125, .126, or .13",
                "source-window metric-soft dominance without a Goldbach "
                "implication theorem",
            ],
            "finite_remainder_position": (
                "Finite verification becomes acceptance only after a "
                "universal sufficiently-large theorem supplies an explicit "
                "threshold N0."),
        },
        "decision": (
            "TARGET_pointwise_unnormalized_bridge_not_finite_acceptance.  "
            "The current accepted bridge target is universal, pointwise, and "
            "raw/unnormalized.  L2 remains a HOLD unless it proves a strict "
            "raw theorem; finite zero-mass and observed L2 receipts do not "
            "confirm the bridge.  Metric-soft source-window evidence remains "
            "useful but separate from the q286-to-Goldbach logical bridge."),
        "status_boundary": (
            "Bridge acceptance-gate audit only.  No aggregate L2 theorem, "
            "source-window theorem, raw adverse-drag theorem, q286 threshold "
            "theorem, strict-central Goldbach theorem, or Goldbach proof is "
            "established."),
        "aggregate_l2_theorem_proved": False,
        "source_window_theorem_proved": False,
        "raw_adverse_drag_theorem_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "l2_bridge_confirmed": receipt["zero_mass_l2_status"][
            "l2_logical_bridge_confirmed"],
        "pointwise_universal_bound_open": receipt[
            "pointwise_adverse_drag_status"]["universal_bound_open"],
        "finite_evidence_is_acceptance_condition": receipt[
            "acceptance_gate"]["finite_evidence_is_acceptance_condition"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
