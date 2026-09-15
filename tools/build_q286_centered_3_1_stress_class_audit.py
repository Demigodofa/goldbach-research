"""Test centered (3,1) against a predeclared q286 stress class.

The previous centered scalar audit showed that selected deficit references sit
below every fresh target in locally centered (3,1) order. This audit widens the
reference population to the channel-independent ``full_nonpositive`` stress
class from the filter-order receipt.

Finite evidence only: this proves no stress-classifier theorem, binary-prime
correlation theorem, signed projection theorem, or Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
    q286_first_three_filter_order_audit_receipt,
)
from tools.build_q286_alternate_reference_channel_audit import (  # noqa: E402
    DEFICIT_REFERENCES,
)
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    contribution_map,
    label_key,
    label_tuple,
)


OUT = ROOT / "evidence" / "q286-centered-3-1-stress-class-audit.json"
CENTERED_SOURCE = (
    ROOT / "evidence" / "q286-centered-channel-scalar-order-audit.json")
CHANNELS = ((3, 1), (5, 5))
TOLERANCE = 1e-12


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def finite_summary(values):
    values = tuple(float(value) for value in values)
    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None}
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def targets_with(receipt, predicate):
    return {
        int(target) for target, row in receipt["target_rows"].items()
        if predicate in row["passed_predicates"]
    }


def predicate_sets(receipt):
    first_two = targets_with(receipt, "first_two_active")
    first_three = targets_with(receipt, "first_three_tail")
    full_nonpositive = targets_with(receipt, "full_nonpositive")
    return {
        "full_nonpositive": full_nonpositive,
        "nonrescued_first_three_tail": first_three & full_nonpositive,
        "active_nonrescued": first_two & first_three & full_nonpositive,
        "full_nonpositive_not_first_three_tail": (
            full_nonpositive - first_three),
    }


def centered_value(target, channel, profile, labels, local_rows_by_residue,
                   lp_vector):
    label_index = labels.index(channel)
    contributions = contribution_map(profile["target_rows"][target])
    empirical = float(contributions[channel])
    local = float(
        local_rows_by_residue[target % 143]["local_delta_vector"][
            label_index])
    weight = float(lp_vector[label_index])
    centered = empirical - local
    return {
        "target": target,
        "target_mod_143": target % 143,
        "target_mod_286": target % 286,
        "empirical_channel_value": empirical,
        "local_channel_delta_relative_to_base": local,
        "centered_channel_value": centered,
        "lp_weight": weight,
        "weighted_centered_channel_value": centered * weight,
    }


def enrich_rows(rows, receipt):
    out = []
    for row in rows:
        filter_row = receipt["target_rows"][row["target"]]
        out.append({
            **row,
            "cycle": filter_row["cycle"],
            "first_two_modes_to_principal_ratio": (
                filter_row["first_two_modes_to_principal_ratio"]),
            "first_three_modes_to_principal_ratio": (
                filter_row["first_three_modes_to_principal_ratio"]),
            "complement_to_principal_ratio": (
                filter_row["complement_to_principal_ratio"]),
            "full_action_to_principal_ratio": (
                filter_row["full_action_to_principal_ratio"]),
            "passed_predicates": filter_row["passed_predicates"],
            "selected_deficit_reference": (
                row["target"] in DEFICIT_REFERENCES),
        })
    return out


def summarize_class(class_id, targets, rows_by_target, fresh_min_row):
    rows = [rows_by_target[target] for target in sorted(targets)]
    ranked = sorted(
        rows,
        key=lambda row: (
            row["weighted_centered_channel_value"], row["target"]))
    ranked_rows = []
    for rank, row in enumerate(ranked, start=1):
        copy = dict(row)
        copy["rank_low_to_high_within_class"] = rank
        copy["below_fresh_min"] = (
            copy["weighted_centered_channel_value"]
            < fresh_min_row["weighted_centered_channel_value"] - TOLERANCE)
        ranked_rows.append(copy)
    failing = [
        row for row in ranked_rows
        if not row["below_fresh_min"]
    ]
    return {
        "class_id": class_id,
        "target_count": len(ranked_rows),
        "fresh_min_target": fresh_min_row["target"],
        "fresh_min_weighted_centered_value": (
            fresh_min_row["weighted_centered_channel_value"]),
        "below_fresh_min_count": len(ranked_rows) - len(failing),
        "at_or_above_fresh_min_count": len(failing),
        "separator_passes_class": not failing,
        "weighted_centered_value_summary": finite_summary(
            row["weighted_centered_channel_value"] for row in ranked_rows),
        "minimum_row": ranked_rows[0] if ranked_rows else None,
        "maximum_row": ranked_rows[-1] if ranked_rows else None,
        "first_at_or_above_fresh_min_rows": failing[:20],
        "selected_deficit_reference_rows": [
            row for row in ranked_rows if row["selected_deficit_reference"]],
        "lowest_12_rows": ranked_rows[:12],
        "highest_12_rows": ranked_rows[-12:],
    }


def main():
    local_payload = json.loads(LOCAL_SOURCE.read_text(encoding="utf-8"))
    lp_payload = json.loads(LP_SOURCE.read_text(encoding="utf-8"))
    centered_payload = json.loads(
        CENTERED_SOURCE.read_text(encoding="utf-8"))
    labels = tuple(label_tuple(label) for label in local_payload["outside_labels"])
    lp_vector = np.asarray(
        lp_payload["selected_lp_effective_vector"], dtype=np.float64)
    local_rows_by_residue = {
        int(row["n_mod_143"]): row
        for row in local_payload["local_residue_rows"]
    }
    fresh_min_by_label = {
        result["label_key"]: result["minimum_fresh_row"]
        for result in centered_payload["channel_results"]
    }

    baseline = q286_first_three_filter_order_audit_receipt(
        start=10000, cycle_count=8, targets_per_cycle=5005,
        tail_threshold=.3, complement_floor=.3)
    holdout = q286_first_three_filter_order_audit_receipt(
        start=90080, cycle_count=8, targets_per_cycle=5005,
        tail_threshold=.3, complement_floor=.3)
    baseline_sets = predicate_sets(baseline)
    holdout_sets = predicate_sets(holdout)

    profile_targets = tuple(sorted(baseline_sets["full_nonpositive"]))
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=profile_targets,
        dominant_modes=(1, 2), tail_threshold=.3, top_channel_count=40)

    channel_results = []
    for channel in CHANNELS:
        rows = enrich_rows([
            centered_value(
                target, channel, profile, labels, local_rows_by_residue,
                lp_vector)
            for target in profile_targets
        ], baseline)
        rows_by_target = {row["target"]: row for row in rows}
        channel_results.append({
            "label": channel,
            "label_key": label_key(channel),
            "fresh_min_row": fresh_min_by_label[label_key(channel)],
            "class_results": [
                summarize_class(
                    class_id, targets, rows_by_target,
                    fresh_min_by_label[label_key(channel)])
                for class_id, targets in baseline_sets.items()
            ],
        })

    result_by_label = {result["label_key"]: result for result in channel_results}
    full_nonpositive_3_1 = next(
        row for row in result_by_label["3,1"]["class_results"]
        if row["class_id"] == "full_nonpositive")
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_centered_scalar_order_audit": str(
            CENTERED_SOURCE.relative_to(ROOT)),
        "source_local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lp_cone_audit": str(LP_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite stress-class scalar-order audit only; no "
            "stress-classifier theorem, binary-prime correlation theorem, "
            "signed projection theorem, or Goldbach proof."),
        "baseline_filter_window": {
            "start": baseline["start"],
            "cycle_count": baseline["cycle_count"],
            "targets_per_cycle": baseline["targets_per_cycle"],
            "tested_target_count": baseline["tested_target_count"],
            "predicate_counts": baseline["predicate_counts"],
        },
        "holdout_filter_window": {
            "start": holdout["start"],
            "cycle_count": holdout["cycle_count"],
            "targets_per_cycle": holdout["targets_per_cycle"],
            "tested_target_count": holdout["tested_target_count"],
            "predicate_counts": holdout["predicate_counts"],
        },
        "class_definitions": {
            "full_nonpositive": (
                "Targets in the baseline filter-order fixture whose full "
                "q286 action to principal is nonpositive."),
            "nonrescued_first_three_tail": (
                "Baseline targets with first_three_tail and full_nonpositive."),
            "active_nonrescued": (
                "Baseline targets with first_two_active, first_three_tail, "
                "and full_nonpositive."),
            "full_nonpositive_not_first_three_tail": (
                "Baseline full_nonpositive targets outside first_three_tail."),
        },
        "holdout_class_counts": {
            key: len(value) for key, value in holdout_sets.items()
        },
        "mechanism": (
            "Use a channel-independent stress predicate from the existing "
            "filter-order receipt, then compare each stress row's weighted "
            "locally centered scalar value to the frozen fresh-window minimum "
            "from the centered scalar audit."),
        "prediction": (
            "If centered (3,1) is a stress-classifier coordinate for the "
            "predeclared full_nonpositive class, every full_nonpositive row "
            "should lie below the fresh-window minimum in centered (3,1) "
            "order."),
        "falsifier": (
            "Any full_nonpositive row whose centered (3,1) value is at least "
            "the frozen fresh-window minimum falsifies the broad classifier "
            "claim for this predeclared finite class."),
        "channel_results": channel_results,
        "channel_3_1_full_nonpositive_separator_passes": (
            full_nonpositive_3_1["separator_passes_class"]),
        "channel_3_1_full_nonpositive_at_or_above_fresh_min_count": (
            full_nonpositive_3_1["at_or_above_fresh_min_count"]),
        "decision": (
            "The broad centered-(3,1) stress-classifier reading is falsified "
            "on the baseline full_nonpositive class: many independently "
            "selected full-nonpositive rows sit at or above the fresh-window "
            "minimum. The previous selected-reference result survives only "
            "as a selected-deficit separator, not as a theorem for the whole "
            "full_nonpositive stress predicate."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
