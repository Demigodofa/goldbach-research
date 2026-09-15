"""Triage the current q286 non-circular theorem routes.

This is a derived receipt.  It does not recompute the expensive q286 rows; it
compares the latest WBSS aggregate L2 obstruction with the structured
component-pair closure receipt and records which route is currently the
sharper theorem obligation.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
NOTES = ROOT / "notes"
OUT = EVIDENCE / "q286-non-circular-route-triage-audit.json"
WBSS_L2_SOURCE = (
    EVIDENCE / "q286-wbss-multiplicative-character-l2-observed-moment-audit.json")
WBSS_POINTWISE_SOURCE = (
    EVIDENCE / "q286-wbss-pointwise-adverse-drag-theorem-target.json")
COMPONENT_CLOSURE_SOURCE = (
    EVIDENCE / "q286-active-lane-strict-closure-margin-census-selected-late.json")
COMPONENT_NOTE_SOURCE = NOTES / "q286-component-pair-theorem-obligation.md"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def tightest_component_row(rows):
    return min(
        rows.items(),
        key=lambda item: (
            float(item[1]["strict_closure_margin_to_calibrated_endpoint"]),
            int(item[0]),
        ),
    )


def build_receipt():
    wbss_l2 = load_json(WBSS_L2_SOURCE)
    wbss_pointwise = load_json(WBSS_POINTWISE_SOURCE)
    component = load_json(COMPONENT_CLOSURE_SOURCE)
    component_note = COMPONENT_NOTE_SOURCE.read_text(encoding="utf-8")

    target, row = tightest_component_row(component["target_rows"])
    component_tail_count = int(component["tail_target_count"])
    component_positive_count = len(component["positive_strict_margin_targets"])
    component_margin = float(row["strict_closure_margin_to_calibrated_endpoint"])
    wbss_local_violations = int(
        wbss_l2["summary"]["row_local_cap_exceeding_row_count"])
    wbss_checked_rows = int(wbss_l2["summary"]["row_count"])

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "wbss_l2_observed_moment_audit": str(
                WBSS_L2_SOURCE.relative_to(ROOT)),
            "wbss_pointwise_target": str(
                WBSS_POINTWISE_SOURCE.relative_to(ROOT)),
            "component_pair_strict_closure": str(
                COMPONENT_CLOSURE_SOURCE.relative_to(ROOT)),
            "component_pair_note": str(
                COMPONENT_NOTE_SOURCE.relative_to(ROOT)),
        },
        "status": "HOLD_component_pair_is_sharper_current_theorem_obligation",
        "status_boundary": (
            "route-triage receipt only; it chooses a next theorem obligation "
            "from existing evidence and proves no fixed-modulus character "
            "estimate, pointwise adverse-drag theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "non_circular_bridge_confirmed": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "component_pair_closure_theorem_proved": False,
        "fixed_conductor_channel_theorem_proved": False,
        "universal_bound_open": True,
        "wbss_plain_l2_route": {
            "role": "reservoir_until_changed_condition",
            "target": wbss_l2["acceptance_condition"]["target"],
            "zero_mass_defect_found": False,
            "non_circular_bridge_confirmed": wbss_l2[
                "acceptance_condition"]["non_circular_bridge_confirmed"],
            "checked_rows": wbss_checked_rows,
            "row_local_l2_cap_violations": wbss_local_violations,
            "global_min_l2_cap_violations": int(
                wbss_l2["summary"]["global_min_cap_exceeding_row_count"]),
            "worst_row": wbss_l2["summary"]["largest_row_local_ratio_row"],
            "changed_conditions_to_reactivate": [
                (
                    "an external pointwise aggregate twisted binary-prime "
                    "moment theorem with an explicit threshold"),
                (
                    "a structured signed moment theorem that explains why "
                    "the 120 finite row-local violations are below-threshold"),
                "a different unnormalized signed estimate than plain aggregate L2",
            ],
            "decision": (
                "Plain aggregate L2 remains coefficient algebra and a "
                "possible asymptotic theorem shape, but it is not the next "
                "finite acceptance route: the checked population violates "
                "the row-local cap on "
                f"{wbss_local_violations}/{wbss_checked_rows} rows."),
        },
        "wbss_pointwise_route": {
            "required_universal_statement": wbss_pointwise[
                "acceptance_condition"]["required_universal_statement"],
            "normalization_boundary": wbss_pointwise[
                "acceptance_condition"]["normalization_boundary"],
            "still_valid_as_definition": True,
            "decision": (
                "The unnormalized adverse-drag inequality remains the correct "
                "acceptance condition for WBSS, but no current L2 bridge pays "
                "it non-circularly."),
        },
        "component_pair_route": {
            "role": "sharper_current_theorem_obligation",
            "active_selector": component["selector"],
            "scanned_target_count": int(component["scanned_target_count"]),
            "tail_target_count": component_tail_count,
            "positive_strict_margin_targets": component[
                "positive_strict_margin_targets"],
            "positive_strict_margin_count": component_positive_count,
            "all_tail_targets_have_positive_strict_margin": component[
                "all_tail_targets_have_positive_strict_margin"],
            "calibrated_combined_floor_driver_floor": float(component[
                "calibrated_combined_floor_driver_floor"]),
            "calibrated_normalized_real_channel_linf_bound": float(component[
                "calibrated_normalized_real_channel_linf_bound"]),
            "calibrated_real_channel_l1_to_principal_mean": float(component[
                "calibrated_real_channel_l1_to_principal_mean"]),
            "tightest_selected_margin_target": int(target),
            "tightest_selected_margin": component_margin,
            "tightest_selected_margin_row": row,
            "active_conductors_35_77_named_in_note": (
                "conductor `35` or `77`" in component_note
                or "conductors `35` or `77`" in component_note
                or "conductors `35` and `77`" in component_note),
            "remaining_proof_obligations": [
                (
                    "define or prove eventual active-selector exclusion, or "
                    "stress every active-selector row found by the unchanged "
                    "selector"),
                (
                    "prove the combined-driver floor on the active lane, "
                    "not just on the three selected late targets"),
                (
                    "prove a pointwise fixed-conductor channel estimate strong "
                    "enough for normalized Linf <= 0.05885324711081062 on the "
                    "16 active real channels"),
                (
                    "verify a finite remainder after any eventual threshold "
                    "is proved"),
            ],
            "decision": (
                "This route has a narrower non-circular theorem obligation "
                "than the failed WBSS plain L2 cap: a driver floor plus fixed "
                "conductor real-channel control on the active selector.  It "
                "is still selected finite evidence and proves no theorem."),
        },
        "route_decision": {
            "next_best_non_circular_target": (
                "component-pair active-lane driver floor plus fixed-conductor "
                "real-channel bound"),
            "sleep_or_reservoir": [
                "plain aggregate WBSS L2 finite cap checks",
                "more fitted component suprema",
                "more normalized finite ratios without a theorem object",
            ],
            "smallest_next_test": (
                "Either prove/falsify the active-selector rarity statement, "
                "or take the unchanged component-pair closure scalar to the "
                "next predeclared active rows with scanned, selected, "
                "stressed, passed, failed, and not-applicable counts separated."),
            "why_this_changes_next_action": (
                "The L2 route failed as an already-valid bridge, while the "
                "component-pair route localizes the missing theorem to an "
                "explicit active selector, a driver floor, and a fixed "
                "conductor channel bound."),
        },
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
