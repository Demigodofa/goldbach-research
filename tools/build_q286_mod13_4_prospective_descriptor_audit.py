"""Prospectively test the q286 mod-13 low-(3,1) descriptor.

The previous independent descriptor audit found that, inside the broad
``full_nonpositive`` reference population, ``target_mod_13 == 4`` was a small
zero-failure pocket for the scalar low-(3,1) threshold.  This receipt freezes
that descriptor before moving to the next unused q286 cycle block.

Finite evidence only: this is a stress-classifier pocket test, not a stress
theorem, signed prime-correlation theorem, pointwise character-sum theorem, or
Goldbach proof.
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
OUT = EVIDENCE / "q286-mod13-4-prospective-descriptor-audit.json"
THRESHOLD_SOURCE = (
    EVIDENCE / "q286-centered-3-1-threshold-subclass-audit.json")
DESCRIPTOR_SOURCE = (
    EVIDENCE / "q286-low-3-1-independent-descriptor-audit.json")
SELECTED_STABLE_SOURCE = (
    EVIDENCE / "q286-selected-stable-fixture-family-boundary-audit.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
    q286_first_three_filter_order_audit_receipt,
)
from tools.build_q286_centered_3_1_residue5_multichannel_horizon import (  # noqa: E402
    SCALAR_LABEL,
)
from tools.build_q286_centered_3_1_stress_class_audit import (  # noqa: E402
    predicate_sets,
)
from tools.build_q286_centered_3_1_threshold_subclass_audit import (  # noqa: E402
    centered_row,
    finite_summary,
    rank_rows,
)
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    label_tuple,
)


DISCOVERY_START = 10000
DISCOVERY_CYCLES = 8
TARGETS_PER_CYCLE = 5005
TAIL_THRESHOLD = .3
COMPLEMENT_FLOOR = .3
FROZEN_DESCRIPTOR = "target_mod_13==4"
FROZEN_DESCRIPTOR_MODULUS = 13
FROZEN_DESCRIPTOR_RESIDUE = 4
TOLERANCE = 1e-12


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def selected_descriptor_row(descriptor_payload):
    return descriptor_payload["decision_metrics"][
        "best_low_33_predeclared_descriptor"]


def get_thresholds(threshold_payload):
    return {
        "selected_max_threshold": float(
            threshold_payload["selected_max_threshold"]),
        "selected_min_threshold": float(
            threshold_payload["selected_min_threshold"]),
        "fresh_min_weighted_centered_3_1": float(
            threshold_payload["fresh_min_weighted_centered_3_1"]),
    }


def classify_row(row, thresholds):
    value = float(row["weighted_centered_channel_value"])
    return {
        "low_selected_max_threshold": (
            value <= thresholds["selected_max_threshold"] + TOLERANCE),
        "strict_low_selected_min_threshold": (
            value <= thresholds["selected_min_threshold"] + TOLERANCE),
        "below_fresh_min_threshold": (
            value < thresholds["fresh_min_weighted_centered_3_1"]
            - TOLERANCE),
        "above_or_equal_fresh_min_threshold": (
            value >= thresholds["fresh_min_weighted_centered_3_1"]
            - TOLERANCE),
    }


def cycle_counts(rows):
    out = {}
    for row in rows:
        cycle = int(row["cycle"])
        if cycle not in out:
            out[cycle] = {
                "cycle": cycle,
                "reference_count": 0,
                "mod13_4_count": 0,
                "low_selected_max_count": 0,
                "strict_low_selected_min_count": 0,
                "above_or_equal_fresh_min_count": 0,
            }
        out[cycle]["reference_count"] += 1
        out[cycle]["mod13_4_count"] += int(
            row["target_mod_13"] == FROZEN_DESCRIPTOR_RESIDUE)
        out[cycle]["low_selected_max_count"] += int(
            row["low_selected_max_threshold"])
        out[cycle]["strict_low_selected_min_count"] += int(
            row["strict_low_selected_min_threshold"])
        out[cycle]["above_or_equal_fresh_min_count"] += int(
            row["above_or_equal_fresh_min_threshold"])
    return [out[key] for key in sorted(out)]


def summarize_reference_group(name, rows, total_low_selected,
                              total_strict_low, total_broad):
    values = [float(row["weighted_centered_channel_value"]) for row in rows]
    low_rows = [row for row in rows if row["low_selected_max_threshold"]]
    strict_low_rows = [
        row for row in rows if row["strict_low_selected_min_threshold"]]
    above_selected_rows = [
        row for row in rows if not row["low_selected_max_threshold"]]
    above_fresh_rows = [
        row for row in rows if row["above_or_equal_fresh_min_threshold"]]
    return {
        "name": name,
        "reference_count": len(rows),
        "references": [int(row["target"]) for row in rows],
        "weighted_centered_3_1_summary": finite_summary(values),
        "low_selected_max_count": len(low_rows),
        "strict_low_selected_min_count": len(strict_low_rows),
        "above_selected_max_count": len(above_selected_rows),
        "above_or_equal_fresh_min_count": len(above_fresh_rows),
        "precision_for_low_selected_max": (
            len(low_rows) / len(rows) if rows else None),
        "recall_for_low_selected_max": (
            len(low_rows) / total_low_selected
            if total_low_selected else None),
        "coverage_of_broad_full_nonpositive": (
            len(rows) / total_broad if total_broad else None),
        "recall_for_strict_low_selected_min": (
            len(strict_low_rows) / total_strict_low
            if total_strict_low else None),
        "passes_selected_max_zero_failure_gate": (
            (not above_selected_rows) if rows else None),
        "passes_fresh_min_zero_failure_gate": (
            (not above_fresh_rows) if rows else None),
        "failing_rows_against_selected_max": above_selected_rows[:20],
        "failing_rows_against_fresh_min": above_fresh_rows[:20],
        "lowest_rows": rows[:12],
        "highest_rows": rows[-12:],
    }


def residue_table(rows, total_low_selected, total_strict_low, total_broad):
    out = []
    for residue in range(FROZEN_DESCRIPTOR_MODULUS):
        subset = [
            row for row in rows
            if row["target_mod_13"] == residue
        ]
        out.append(summarize_reference_group(
            f"target_mod_13=={residue}",
            subset,
            total_low_selected,
            total_strict_low,
            total_broad))
    return out


def selected_witness_summary(payload):
    return payload.get("focus_reference_13822")


def main():
    threshold_payload = load_json(THRESHOLD_SOURCE)
    descriptor_payload = load_json(DESCRIPTOR_SOURCE)
    selected_stable_payload = load_json(SELECTED_STABLE_SOURCE)
    local_payload = load_json(LOCAL_SOURCE)
    lp_payload = load_json(LP_SOURCE)
    thresholds = get_thresholds(threshold_payload)
    descriptor_row = selected_descriptor_row(descriptor_payload)
    if descriptor_row["descriptor"] != FROZEN_DESCRIPTOR:
        raise AssertionError(
            f"expected frozen descriptor {FROZEN_DESCRIPTOR}, got "
            f"{descriptor_row['descriptor']}")
    if not descriptor_row["predeclared_without_centered_3_1"]:
        raise AssertionError("frozen descriptor must be independent")

    discovery = q286_first_three_filter_order_audit_receipt(
        start=DISCOVERY_START,
        cycle_count=DISCOVERY_CYCLES,
        targets_per_cycle=TARGETS_PER_CYCLE,
        tail_threshold=TAIL_THRESHOLD,
        complement_floor=COMPLEMENT_FLOOR)
    period = int(discovery["arithmetic_period"])
    prospective_start = DISCOVERY_START + DISCOVERY_CYCLES * period
    prospective = q286_first_three_filter_order_audit_receipt(
        start=prospective_start,
        cycle_count=DISCOVERY_CYCLES,
        targets_per_cycle=TARGETS_PER_CYCLE,
        tail_threshold=TAIL_THRESHOLD,
        complement_floor=COMPLEMENT_FLOOR)
    broad_targets = tuple(sorted(predicate_sets(prospective)[
        "full_nonpositive"]))

    labels = tuple(label_tuple(label) for label in local_payload[
        "outside_labels"])
    lp_vector = np.asarray(
        lp_payload["selected_lp_effective_vector"], dtype=np.float64)
    local_rows_by_residue = {
        int(row["n_mod_143"]): row
        for row in local_payload["local_residue_rows"]
    }

    rows = []
    if broad_targets:
        profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
            sample_targets=broad_targets,
            dominant_modes=(1, 2),
            tail_threshold=TAIL_THRESHOLD,
            top_channel_count=40)
        raw_rows = []
        for target in broad_targets:
            base = centered_row(
                target, profile, labels, local_rows_by_residue, lp_vector)
            raw_rows.append({
                **base,
                **classify_row(base, thresholds),
                "cycle": int(prospective["target_rows"][target]["cycle"]),
                "target_mod_11": target % 11,
                "target_mod_13": target % 13,
                "target_mod_143": target % 143,
                "target_mod_286": target % 286,
                "passed_predicates": prospective["target_rows"][target][
                    "passed_predicates"],
                "full_action_to_principal_ratio": prospective[
                    "target_rows"][target]["full_action_to_principal_ratio"],
                "first_two_modes_to_principal_ratio": prospective[
                    "target_rows"][target][
                        "first_two_modes_to_principal_ratio"],
                "first_three_modes_to_principal_ratio": prospective[
                    "target_rows"][target][
                        "first_three_modes_to_principal_ratio"],
                "complement_to_principal_ratio": prospective[
                    "target_rows"][target]["complement_to_principal_ratio"],
            })
        rows = rank_rows(raw_rows)

    total_low_selected = sum(
        1 for row in rows if row["low_selected_max_threshold"])
    total_strict_low = sum(
        1 for row in rows if row["strict_low_selected_min_threshold"])
    total_broad = len(rows)
    descriptor_rows = [
        row for row in rows
        if row["target_mod_13"] == FROZEN_DESCRIPTOR_RESIDUE]
    descriptor_summary = summarize_reference_group(
        FROZEN_DESCRIPTOR,
        descriptor_rows,
        total_low_selected,
        total_strict_low,
        total_broad)
    residues = residue_table(
        rows, total_low_selected, total_strict_low, total_broad)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "threshold_subclass": str(THRESHOLD_SOURCE.relative_to(ROOT)),
            "independent_descriptor": str(
                DESCRIPTOR_SOURCE.relative_to(ROOT)),
            "selected_stable_fixture_family_boundary": str(
                SELECTED_STABLE_SOURCE.relative_to(ROOT)),
            "local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
            "low_frequency_lp_cone": str(LP_SOURCE.relative_to(ROOT)),
            "filter_order_receipt":
                "q286_first_three_filter_order_audit_receipt",
            "signed_channel_profile_receipt":
                "q286_first_three_dominant_mode_signed_channel_profile_receipt",
        },
        "status_boundary": (
            "finite prospective descriptor audit only; this tests whether "
            "the frozen target_mod_13==4 pocket generalizes to a later q286 "
            "cycle block. It proves no stress theorem, signed correlation "
            "theorem, pointwise character-sum theorem, or Goldbach proof."),
        "question": (
            "Does the independent target_mod_13==4 pocket continue to "
            "select low weighted centered-(3,1) full_nonpositive references "
            "on a fresh predeclared q286 cycle block?"),
        "mechanism": (
            "Freeze the prior best low-33 predeclared descriptor "
            "target_mod_13==4 before testing. Then derive the prospective "
            "start from the q286 arithmetic period after the original eight "
            "selection cycles and evaluate all prospective full_nonpositive "
            "references by weighted locally centered (3,1)."),
        "prediction": (
            "If target_mod_13==4 is a genuine small stress-classifier pocket, "
            "its prospective full_nonpositive rows should stay below the "
            "frozen selected-max and fresh-min centered-(3,1) thresholds."),
        "falsifier": (
            "Any prospective target_mod_13==4 full_nonpositive row above the "
            "selected-max threshold or at/above the fresh-min threshold "
            "falsifies the zero-failure pocket. No prospective support leaves "
            "the descriptor untested on this block."),
        "discovery_window": {
            "start": int(discovery["start"]),
            "cycle_count": int(discovery["cycle_count"]),
            "targets_per_cycle": int(discovery["targets_per_cycle"]),
            "arithmetic_period": period,
            "full_nonpositive_count": int(discovery[
                "predicate_counts"]["full_nonpositive"]),
        },
        "prospective_window": {
            "start": int(prospective["start"]),
            "cycle_count": int(prospective["cycle_count"]),
            "targets_per_cycle": int(prospective["targets_per_cycle"]),
            "tested_target_count": int(prospective["tested_target_count"]),
            "predicate_counts": prospective["predicate_counts"],
        },
        "frozen_descriptor": {
            "descriptor": FROZEN_DESCRIPTOR,
            "source_reference_count": int(descriptor_row["reference_count"]),
            "source_low_count": int(descriptor_row["low_count"]),
            "source_above_threshold_count": int(
                descriptor_row["above_threshold_count"]),
            "source_precision": float(descriptor_row["precision"]),
            "source_recall": float(descriptor_row["recall"]),
            "source_references": descriptor_row["references"],
        },
        "thresholds": thresholds,
        "reference_13822_witness": selected_witness_summary(
            selected_stable_payload),
        "prospective_full_nonpositive_reference_count": total_broad,
        "prospective_low_selected_max_count": total_low_selected,
        "prospective_strict_low_selected_min_count": total_strict_low,
        "prospective_cycle_counts": cycle_counts(rows),
        "prospective_descriptor_result": descriptor_summary,
        "prospective_mod13_residue_results": residues,
        "lowest_prospective_full_nonpositive_rows": rows[:20],
        "highest_prospective_full_nonpositive_rows": rows[-20:],
        "decision_metrics": {
            "descriptor_test_status": (
                "tested"
                if descriptor_summary["reference_count"]
                else "untested_no_prospective_full_nonpositive_support"),
            "descriptor_support_count": int(
                descriptor_summary["reference_count"]),
            "descriptor_above_selected_max_count": int(
                descriptor_summary["above_selected_max_count"]),
            "descriptor_above_or_equal_fresh_min_count": int(
                descriptor_summary["above_or_equal_fresh_min_count"]),
            "descriptor_precision_for_low_selected_max": (
                descriptor_summary["precision_for_low_selected_max"]),
            "descriptor_recall_for_low_selected_max": (
                descriptor_summary["recall_for_low_selected_max"]),
            "descriptor_passes_selected_max_zero_failure_gate": (
                descriptor_summary[
                    "passes_selected_max_zero_failure_gate"]),
            "descriptor_passes_fresh_min_zero_failure_gate": (
                descriptor_summary["passes_fresh_min_zero_failure_gate"]),
        },
        "decision": (
            "If descriptor_support_count is nonzero and both zero-failure "
            "gates pass, preserve target_mod_13==4 as a finite prospective "
            "low-(3,1) stress-classifier pocket. If either gate fails, close "
            "this pocket as a one-fixture artifact. If support is zero, mark "
            "it as untested on this prospective block."),
        "next_obligation": (
            "A passing pocket still needs a broader independent family or a "
            "signed correlation estimate before it can become a theorem "
            "route. A failing pocket sends the route back to distributed "
            "cone/correlation rather than scalar classifier language."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
