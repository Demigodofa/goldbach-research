"""Audit whether centered (3,1) stress evidence is reference-specific.

The previous receipts showed that reference 13822 is a strong selected
deficit witness, but also that a scalar-selected low-(3,1) subclass extends
beyond the selected five.  This audit separates those readings by comparing
multiple frozen reference groups against three target groups:

* the 12 same-window zero-local seed targets,
* the 594 same-window nonseed targets,
* the 606 later fresh-predeclared targets.

Finite evidence only: this proves no stress theorem, signed correlation
theorem, pointwise character-sum theorem, or Goldbach theorem.
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
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-centered-3-1-reference-sensitivity-audit.json"
TOLERANCE = 1e-12

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
    q286_first_three_filter_order_audit_receipt,
)
from tools.build_q286_centered_3_1_stress_class_audit import (  # noqa: E402
    predicate_sets,
)
from tools.build_q286_centered_3_1_threshold_subclass_audit import (  # noqa: E402
    ADDITIONAL_SOURCE,
    CENTERED_SOURCE,
    SCOPE_FORK_SOURCE,
    SELECTED_PROVENANCE,
    centered_row,
    finite_summary,
    rank_rows,
)
from tools.build_q286_centered_channel_scalar_order_audit import (  # noqa: E402
    CHANNELS,
    collect_role_targets,
    centered_rows_for_channel,
)
from tools.build_q286_centered_3_1_residue5_multichannel_horizon import (  # noqa: E402
    SCALAR_LABEL,
    label_key,
)
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    label_tuple,
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def row_value(row):
    return float(row["weighted_centered_channel_value"])


def sorted_rows(rows):
    return sorted(rows, key=lambda row: (row_value(row), row["target"]))


def compact_row(row):
    out = {
        "target": int(row["target"]),
        "target_mod_143": int(row["target_mod_143"]),
        "target_mod_286": int(row["target_mod_286"]),
        "weighted_centered_3_1": row_value(row),
    }
    for key in ("role", "window_start", "window_index", "offset"):
        if key in row:
            out[key] = row[key]
    return out


def reference_group(name, rows, source, scalar_selected, predeclared):
    rows = sorted_rows(rows)
    return {
        "name": name,
        "source": source,
        "predeclared_without_centered_3_1": predeclared,
        "selected_by_centered_3_1_scalar": scalar_selected,
        "reference_count": len(rows),
        "contains_13822": any(int(row["target"]) == 13822 for row in rows),
        "reference_targets": [int(row["target"]) for row in rows],
        "weighted_centered_3_1_summary": finite_summary(
            row_value(row) for row in rows),
        "lowest_references": [compact_row(row) for row in rows[:12]],
        "highest_references": [compact_row(row) for row in rows[-12:]],
    }


def target_group(name, rows, source):
    rows = sorted_rows(rows)
    return {
        "name": name,
        "source": source,
        "target_count": len(rows),
        "weighted_centered_3_1_summary": finite_summary(
            row_value(row) for row in rows),
        "lowest_targets": [compact_row(row) for row in rows[:12]],
        "highest_targets": [compact_row(row) for row in rows[-12:]],
    }


def compare_group(reference_group_payload, reference_rows, target_group_payload,
                  target_rows):
    margins = []
    failing = []
    by_reference = {}
    for reference in reference_rows:
        reference_target = int(reference["target"])
        reference_value = row_value(reference)
        reference_margins = []
        reference_failing = []
        for target in target_rows:
            margin = row_value(target) - reference_value
            margins.append(margin)
            reference_margins.append(margin)
            if margin <= TOLERANCE:
                fail = {
                    "reference": reference_target,
                    "reference_value": reference_value,
                    "target": int(target["target"]),
                    "target_value": row_value(target),
                    "margin": float(margin),
                    "target_role": target.get("role"),
                    "target_mod_143": int(target["target_mod_143"]),
                    "reference_mod_143": int(reference["target_mod_143"]),
                }
                failing.append(fail)
                reference_failing.append(fail)
        by_reference[reference_target] = {
            "reference": reference_target,
            "reference_value": reference_value,
            "target_count": len(target_rows),
            "failure_count": len(reference_failing),
            "passes_all_targets": not reference_failing,
            "minimum_margin": min(reference_margins)
            if reference_margins else None,
            "average_margin": (
                math.fsum(reference_margins) / len(reference_margins)
                if reference_margins else None),
            "first_failures": sorted(
                reference_failing,
                key=lambda row: (row["margin"], row["target"]))[:8],
        }
    failing = sorted(
        failing,
        key=lambda row: (row["margin"], row["reference"], row["target"]))
    return {
        "reference_group": reference_group_payload["name"],
        "target_group": target_group_payload["name"],
        "reference_count": len(reference_rows),
        "target_count": len(target_rows),
        "comparison_count": len(margins),
        "all_margins_positive": not failing,
        "failure_count": len(failing),
        "failing_reference_count": sum(
            1 for row in by_reference.values()
            if not row["passes_all_targets"]),
        "margin_summary": finite_summary(margins),
        "tightest_failures": failing[:20],
        "per_reference": [
            by_reference[key] for key in sorted(by_reference)
        ],
    }


def rows_by_role(rows, role):
    return [row for row in rows if row.get("role") == role]


def build_scalar_role_rows(local_payload, lp_payload, labels,
                           local_rows_by_residue, lp_vector):
    targets, roles = collect_role_targets(local_payload)
    if SCALAR_LABEL not in CHANNELS:
        raise AssertionError("scalar channel missing from centered audit")
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=targets,
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=40)
    return centered_rows_for_channel(
        SCALAR_LABEL,
        roles,
        profile,
        labels,
        local_rows_by_residue,
        lp_vector)


def build_broad_full_nonpositive_rows(labels, local_rows_by_residue,
                                      lp_vector):
    baseline = q286_first_three_filter_order_audit_receipt(
        start=10000,
        cycle_count=8,
        targets_per_cycle=5005,
        tail_threshold=.3,
        complement_floor=.3)
    broad_targets = tuple(sorted(predicate_sets(baseline)[
        "full_nonpositive"]))
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=broad_targets,
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=40)
    return rank_rows([
        {
            **centered_row(
                target,
                profile,
                labels,
                local_rows_by_residue,
                lp_vector),
            "role": "broad_full_nonpositive_reference",
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
        }
        for target in broad_targets
    ])


def group_lookup(groups):
    return {row["name"]: row for row in groups}


def comparison_lookup(comparisons):
    return {
        (row["reference_group"], row["target_group"]): row
        for row in comparisons
    }


def main():
    local_payload = load_json(LOCAL_SOURCE)
    lp_payload = load_json(LP_SOURCE)
    threshold = load_json(
        EVIDENCE / "q286-centered-3-1-threshold-subclass-audit.json")
    selected_provenance = load_json(SELECTED_PROVENANCE)
    centered_scalar = load_json(CENTERED_SOURCE)
    scope_fork = load_json(SCOPE_FORK_SOURCE)
    additional = load_json(ADDITIONAL_SOURCE)

    labels = tuple(label_tuple(label) for label in local_payload[
        "outside_labels"])
    lp_vector = np.asarray(
        lp_payload["selected_lp_effective_vector"], dtype=np.float64)
    local_rows_by_residue = {
        int(row["n_mod_143"]): row
        for row in local_payload["local_residue_rows"]
    }
    scalar_role_rows = build_scalar_role_rows(
        local_payload, lp_payload, labels, local_rows_by_residue, lp_vector)
    broad_rows = build_broad_full_nonpositive_rows(
        labels, local_rows_by_residue, lp_vector)

    selected_deficit = rows_by_role(
        scalar_role_rows, "selected_deficit_reference")
    selected_clear = rows_by_role(
        scalar_role_rows, "selected_clear_control_reference")
    selected_without_13822 = [
        row for row in selected_deficit if int(row["target"]) != 13822]
    reference_13822 = [
        row for row in selected_deficit if int(row["target"]) == 13822]

    selected_threshold = float(threshold["selected_max_threshold"])
    selected_min = float(threshold["selected_min_threshold"])
    broad_low_33 = [
        row for row in broad_rows
        if row_value(row) <= selected_threshold + TOLERANCE]
    broad_strict_24 = [
        row for row in broad_rows
        if row_value(row) <= selected_min + TOLERANCE]
    broad_above = [
        row for row in broad_rows
        if row_value(row) > selected_threshold + TOLERANCE]

    reference_groups = [
        reference_group(
            "selected_deficit_five",
            selected_deficit,
            "q286-selected-deficit-provenance-audit",
            scalar_selected=False,
            predeclared=True),
        reference_group(
            "selected_deficit_excluding_13822",
            selected_without_13822,
            "selected_deficit_five with focus witness removed",
            scalar_selected=False,
            predeclared=True),
        reference_group(
            "reference_13822_only",
            reference_13822,
            "focus witness from selected_deficit_five",
            scalar_selected=False,
            predeclared=True),
        reference_group(
            "selected_clear_controls",
            selected_clear,
            "q286-centered-channel-scalar-order-audit clear controls",
            scalar_selected=False,
            predeclared=True),
        reference_group(
            "broad_low_33_at_or_below_selected_max",
            broad_low_33,
            "q286-centered-3-1-threshold-subclass-audit",
            scalar_selected=True,
            predeclared=False),
        reference_group(
            "broad_strict_low_24_at_or_below_selected_min",
            broad_strict_24,
            "q286-centered-3-1-threshold-subclass-audit",
            scalar_selected=True,
            predeclared=False),
        reference_group(
            "broad_above_selected_max_controls",
            broad_above,
            "broad full_nonpositive references above frozen selected max",
            scalar_selected=False,
            predeclared=True),
    ]

    same_seed = rows_by_role(
        scalar_role_rows, "same_window_zero_local_seed_target")
    same_nonseed = rows_by_role(
        scalar_role_rows, "same_window_nonseed_target")
    fresh = rows_by_role(scalar_role_rows, "fresh_predeclared_target")
    target_groups = [
        target_group(
            "same_window_zero_local_seed_12",
            same_seed,
            "q286-centered-channel-scalar-order-audit"),
        target_group(
            "same_window_nonseed_594",
            same_nonseed,
            "q286-centered-channel-scalar-order-audit"),
        target_group(
            "same_window_all_606",
            same_seed + same_nonseed,
            "q286-centered-channel-scalar-order-audit"),
        target_group(
            "fresh_predeclared_606",
            fresh,
            "q286-centered-channel-scalar-order-audit"),
    ]

    reference_rows_by_name = {
        "selected_deficit_five": selected_deficit,
        "selected_deficit_excluding_13822": selected_without_13822,
        "reference_13822_only": reference_13822,
        "selected_clear_controls": selected_clear,
        "broad_low_33_at_or_below_selected_max": broad_low_33,
        "broad_strict_low_24_at_or_below_selected_min": broad_strict_24,
        "broad_above_selected_max_controls": broad_above,
    }
    target_rows_by_name = {
        "same_window_zero_local_seed_12": same_seed,
        "same_window_nonseed_594": same_nonseed,
        "same_window_all_606": same_seed + same_nonseed,
        "fresh_predeclared_606": fresh,
    }
    comparisons = []
    for ref_group in reference_groups:
        for tgt_group in target_groups:
            comparisons.append(compare_group(
                ref_group,
                reference_rows_by_name[ref_group["name"]],
                tgt_group,
                target_rows_by_name[tgt_group["name"]]))

    c = comparison_lookup(comparisons)
    selected_fresh = c[("selected_deficit_five", "fresh_predeclared_606")]
    selected_without_fresh = c[(
        "selected_deficit_excluding_13822", "fresh_predeclared_606")]
    broad_low_fresh = c[(
        "broad_low_33_at_or_below_selected_max",
        "fresh_predeclared_606")]
    clear_fresh = c[("selected_clear_controls", "fresh_predeclared_606")]
    above_fresh = c[(
        "broad_above_selected_max_controls",
        "fresh_predeclared_606")]

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
            "low_frequency_lp_cone": str(LP_SOURCE.relative_to(ROOT)),
            "centered_scalar_order": str(CENTERED_SOURCE.relative_to(ROOT)),
            "threshold_subclass": (
                "evidence/q286-centered-3-1-threshold-subclass-audit.json"),
            "selected_deficit_provenance": str(
                SELECTED_PROVENANCE.relative_to(ROOT)),
            "selected_reference_scope_fork": str(
                SCOPE_FORK_SOURCE.relative_to(ROOT)),
            "additional_stress_reference_generalization": str(
                ADDITIONAL_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite centered-(3,1) reference-sensitivity audit only; "
            "scalar-selected broad groups are diagnostics, not "
            "non-post-hoc stress definitions. This proves no stress theorem, "
            "signed correlation theorem, pointwise character-sum theorem, or "
            "Goldbach proof."),
        "question": (
            "Is the centered (3,1) stress/reference signal specific to "
            "the large negative selected witness 13822, or does it persist "
            "across alternate selected and broad q286 deficit/stress "
            "references?"),
        "mechanism": (
            "For a reference R and target T, compare weighted locally "
            "centered scalar values: lp_weight(3,1) * "
            "((empirical(T)-local(T)) - (empirical(R)-local(R))). "
            "The same references are tested separately against the 12 "
            "zero-local seed targets, the 594 same-window nonseed targets, "
            "and the 606 fresh-predeclared targets."),
        "prediction": (
            "If 13822 alone explains the phenomenon, removing 13822 from the "
            "selected deficit references should create fresh-target failures. "
            "If the signal is scalar-family-level, selected deficits without "
            "13822 and the scalar-selected broad low references should still "
            "clear the fresh-predeclared targets, while clear controls and "
            "above-threshold broad controls should fail."),
        "falsifier": (
            "A nonpositive fresh-predeclared margin for "
            "selected_deficit_excluding_13822 would make the live result "
            "13822-specific. A positive fresh-predeclared pass for the clear "
            "controls or above-threshold broad controls would weaken the "
            "scalar-order discriminator."),
        "channel": list(SCALAR_LABEL),
        "selected_max_threshold": selected_threshold,
        "selected_min_threshold": selected_min,
        "fresh_min_weighted_centered_3_1": float(
            threshold["fresh_min_weighted_centered_3_1"]),
        "source_receipt_boundaries": {
            "centered_scalar_order_goldbach_proved": bool(
                centered_scalar["goldbach_proved"]),
            "threshold_subclass_goldbach_proved": bool(
                threshold["goldbach_proved"]),
            "selected_reference_overlap_with_broad_full_nonpositive": (
                threshold[
                    "selected_reference_overlap_with_broad_full_nonpositive"]),
            "scope_fork_broad_scalar_3_1_failure_count": (
                scope_fork["scope_comparison"][
                    "broad_scalar_3_1_failures"]),
            "additional_broad_scalar_3_1_failure_count": (
                additional["full_nonpositive_scalar_3_1_failure_count"]),
        },
        "reference_groups": reference_groups,
        "target_groups": target_groups,
        "comparison_results": comparisons,
        "focus_reference_13822": compact_row(reference_13822[0]),
        "reference_specific_decision": {
            "selected_deficit_five_fresh_failures": selected_fresh[
                "failure_count"],
            "selected_deficit_excluding_13822_fresh_failures": (
                selected_without_fresh["failure_count"]),
            "reference_13822_is_required_for_selected_fresh_pass": (
                not selected_without_fresh["all_margins_positive"]),
            "broad_low_33_fresh_failures": broad_low_fresh[
                "failure_count"],
            "selected_clear_control_fresh_failures": clear_fresh[
                "failure_count"],
            "broad_above_threshold_control_fresh_failures": above_fresh[
                "failure_count"],
        },
        "decision": (
            "Centered (3,1) is not just a 13822 accident for the fresh "
            "predeclared target group if selected_deficit_excluding_13822 "
            "has zero failures. The stronger broad-low pass remains "
            "scalar-selected, not independently stress-defined. Failures on "
            "clear controls and above-threshold broad controls preserve the "
            "reading that low centered (3,1) is the active discriminator. "
            "Any same-window seed/nonseed failures should be kept separate "
            "from the fresh-window claim."),
        "next_obligation": (
            "Replace scalar-selected reference groups with an independent "
            "arithmetic or correlation-defined family, or state the theorem "
            "as a signed correlation estimate rather than a stress "
            "classifier."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
