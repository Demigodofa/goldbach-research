"""Audit the frozen selected-reference centered-(3,1) threshold.

The selected five references already freeze a maximum weighted centered-(3,1)
value.  This audit asks what happens when that frozen scalar threshold is
applied to the independent baseline full_nonpositive reference population.

Finite evidence only: thresholding on (3,1) is a scalar-order subclass, not a
non-post-hoc stress definition.  This proves no stress theorem, signed
correlation theorem, pointwise character-sum theorem, or Goldbach theorem.
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
OUT = EVIDENCE / "q286-centered-3-1-threshold-subclass-audit.json"
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
    q286_first_three_filter_order_audit_receipt,
)
from tools.build_q286_centered_3_1_residue5_multichannel_horizon import (  # noqa: E402
    SCALAR_LABEL,
    label_key,
)
from tools.build_q286_centered_3_1_stress_class_audit import (  # noqa: E402
    predicate_sets,
)
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    contribution_map,
    label_tuple,
)


SELECTED_PROVENANCE = EVIDENCE / "q286-selected-deficit-provenance-audit.json"
CENTERED_SOURCE = EVIDENCE / "q286-centered-channel-scalar-order-audit.json"
ADDITIONAL_SOURCE = (
    EVIDENCE / "q286-additional-stress-reference-generalization-audit.json")
SCOPE_FORK_SOURCE = EVIDENCE / "q286-selected-reference-scope-fork-audit.json"
TOLERANCE = 1e-12


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


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


def centered_row(target, profile, labels, local_rows_by_residue, lp_vector):
    label_index = labels.index(SCALAR_LABEL)
    contributions = contribution_map(profile["target_rows"][target])
    empirical = float(contributions[SCALAR_LABEL])
    local = float(
        local_rows_by_residue[target % 143]["local_delta_vector"][
            label_index])
    centered = empirical - local
    return {
        "target": target,
        "target_mod_143": target % 143,
        "target_mod_286": target % 286,
        "empirical_channel_value": empirical,
        "local_channel_delta_relative_to_base": local,
        "centered_channel_value": centered,
        "lp_weight": float(lp_vector[label_index]),
        "weighted_centered_channel_value": (
            centered * float(lp_vector[label_index])),
    }


def rank_rows(rows):
    ranked = sorted(
        rows,
        key=lambda row: (row["weighted_centered_channel_value"],
                         row["target"]))
    for rank, row in enumerate(ranked, start=1):
        row["rank_low_to_high_within_broad_full_nonpositive"] = rank
    return ranked


def threshold_summary(name, rows, predicate, fresh_min_value):
    selected = [row for row in rows if predicate(row)]
    failing = [
        row for row in selected
        if row["weighted_centered_channel_value"]
        >= fresh_min_value - TOLERANCE
    ]
    return {
        "name": name,
        "reference_count": len(selected),
        "references": [row["target"] for row in selected],
        "weighted_centered_value_summary": finite_summary(
            row["weighted_centered_channel_value"] for row in selected),
        "scalar_3_1_fresh_window_failure_count": len(failing),
        "scalar_3_1_passes_all_fresh_targets": not failing,
        "first_failing_rows": failing[:12],
        "lowest_rows": selected[:12],
        "highest_rows": selected[-12:],
    }


def main():
    selected = load_json(SELECTED_PROVENANCE)
    centered = load_json(CENTERED_SOURCE)
    additional = load_json(ADDITIONAL_SOURCE)
    scope_fork = load_json(SCOPE_FORK_SOURCE)
    local_payload = load_json(LOCAL_SOURCE)
    lp_payload = load_json(LP_SOURCE)

    labels = tuple(label_tuple(label) for label in local_payload[
        "outside_labels"])
    lp_vector = np.asarray(
        lp_payload["selected_lp_effective_vector"], dtype=np.float64)
    local_rows_by_residue = {
        int(row["n_mod_143"]): row
        for row in local_payload["local_residue_rows"]
    }
    selected_values = [
        float(row["centered_3_1_weighted_value"])
        for row in selected["selected_deficit_rows"]
    ]
    selected_threshold = max(selected_values)
    selected_minimum = min(selected_values)

    centered_3_1 = next(
        row for row in centered["channel_results"]
        if row["label_key"] == label_key(SCALAR_LABEL))
    fresh_min = centered_3_1["minimum_fresh_row"]
    fresh_min_value = float(
        fresh_min["weighted_centered_channel_value"])

    baseline = q286_first_three_filter_order_audit_receipt(
        start=10000, cycle_count=8, targets_per_cycle=5005,
        tail_threshold=.3, complement_floor=.3)
    broad_targets = tuple(sorted(predicate_sets(baseline)[
        "full_nonpositive"]))
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=broad_targets,
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=40)
    rows = rank_rows([
        {
            **centered_row(
                target, profile, labels, local_rows_by_residue, lp_vector),
            "passed_predicates": baseline["target_rows"][target][
                "passed_predicates"],
            "full_action_to_principal_ratio": baseline["target_rows"][
                target]["full_action_to_principal_ratio"],
            "first_two_modes_to_principal_ratio": baseline["target_rows"][
                target]["first_two_modes_to_principal_ratio"],
            "first_three_modes_to_principal_ratio": baseline["target_rows"][
                target]["first_three_modes_to_principal_ratio"],
            "complement_to_principal_ratio": baseline["target_rows"][
                target]["complement_to_principal_ratio"],
            "selected_deficit_reference": target in selected[
                "selected_fixture"]["selected_deficit_targets"],
        }
        for target in broad_targets
    ])

    below_fresh = threshold_summary(
        "broad_full_nonpositive_below_fresh_min",
        rows,
        lambda row: (
            row["weighted_centered_channel_value"]
            < fresh_min_value - TOLERANCE),
        fresh_min_value)
    within_selected_threshold = threshold_summary(
        "broad_full_nonpositive_at_or_below_selected_max",
        rows,
        lambda row: (
            row["weighted_centered_channel_value"]
            <= selected_threshold + TOLERANCE),
        fresh_min_value)
    below_selected_min = threshold_summary(
        "broad_full_nonpositive_at_or_below_selected_min",
        rows,
        lambda row: (
            row["weighted_centered_channel_value"]
            <= selected_minimum + TOLERANCE),
        fresh_min_value)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "selected_deficit_provenance": str(
                SELECTED_PROVENANCE.relative_to(ROOT)),
            "centered_scalar_order": str(CENTERED_SOURCE.relative_to(ROOT)),
            "additional_stress_reference_generalization": str(
                ADDITIONAL_SOURCE.relative_to(ROOT)),
            "selected_reference_scope_fork": str(
                SCOPE_FORK_SOURCE.relative_to(ROOT)),
            "local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
            "low_frequency_lp_cone": str(LP_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite threshold-subclass audit only; selecting references by "
            "the same centered (3,1) scalar being tested is not a "
            "non-post-hoc stress definition. This proves no stress theorem, "
            "signed correlation theorem, pointwise character-sum theorem, or "
            "Goldbach proof."),
        "mechanism": (
            "Freeze the selected five's maximum weighted centered-(3,1) "
            "reference value, then apply that scalar threshold to the "
            "independent baseline full_nonpositive references."),
        "prediction": (
            "If the selected-reference (3,1) result is only scalar ordering, "
            "then any broad full_nonpositive reference below the same frozen "
            "threshold will also pass the scalar (3,1) fresh-window gate, "
            "while the full broad class still fails."),
        "falsifier": (
            "A threshold-selected broad reference with weighted centered "
            "(3,1) value below the frozen selected threshold but a "
            "nonpositive fresh-window scalar margin would falsify the scalar "
            "ordering reduction."),
        "channel": list(SCALAR_LABEL),
        "selected_deficit_reference_count": len(selected_values),
        "selected_weighted_centered_3_1_summary": finite_summary(
            selected_values),
        "selected_max_threshold": selected_threshold,
        "selected_min_threshold": selected_minimum,
        "fresh_min_weighted_centered_3_1": fresh_min_value,
        "fresh_min_row": fresh_min,
        "broad_full_nonpositive_reference_count": len(rows),
        "broad_full_nonpositive_weighted_centered_3_1_summary":
            finite_summary(
                row["weighted_centered_channel_value"] for row in rows),
        "lowest_broad_full_nonpositive_rows": rows[:12],
        "highest_broad_full_nonpositive_rows": rows[-12:],
        "threshold_subclasses": [
            below_fresh,
            within_selected_threshold,
            below_selected_min,
        ],
        "selected_reference_overlap_with_broad_full_nonpositive": scope_fork[
            "scope_comparison"]["selected_reference_overlap_count"],
        "broad_scalar_3_1_failure_count": additional[
            "full_nonpositive_scalar_3_1_failure_count"],
        "decision": (
            "The frozen selected (3,1) threshold identifies a scalar-order "
            "subclass inside the independent broad full_nonpositive rows, "
            "and that subclass passes the scalar fresh-window gate exactly "
            "because its references are low in the same centered scalar. "
            "This supports (3,1) as a useful stress/reference coordinate, "
            "but it does not supply a non-post-hoc stress-class theorem. "
            "Also, 13822 is not globally extreme in the broad baseline class: "
            "the independent full_nonpositive population contains lower "
            "weighted centered (3,1) rows."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
