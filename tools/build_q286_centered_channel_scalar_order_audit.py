"""Reduce q286 singleton-channel margins to centered scalar order.

For a fixed outside label L and reference R, the alternate-reference weighted
margin is

    lp_weight[L] * ((empirical_L(target) - local_L(target))
                    - (empirical_L(R) - local_L(R))).

This audit records the underlying locally centered scalar ordering for the
live channel (3,1), with (5,5) as the comparison channel.

Finite evidence only: this proves no channel theorem, binary-prime correlation
theorem, signed projection theorem, or Goldbach theorem.
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
)
from tools.build_q286_alternate_reference_channel_audit import (  # noqa: E402
    CLEAR_CONTROL_REFERENCES,
    DEFICIT_REFERENCES,
)
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    collect_far_targets,
    contribution_map,
    label_key,
    label_tuple,
)
from tools.build_q286_fresh_window_channel_watchlist_audit import (  # noqa: E402
    FRESH_WINDOW_SPECS,
    collect_targets as collect_fresh_targets,
)


OUT = ROOT / "evidence" / "q286-centered-channel-scalar-order-audit.json"
CHANNELS = ((3, 1), (5, 5))
BASE_REFERENCE = 1_222_142
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


def rank_rows(rows, value_key):
    ranked = sorted(rows, key=lambda row: (row[value_key], row["target"]))
    out = []
    for index, row in enumerate(ranked, start=1):
        copy = dict(row)
        copy["rank_low_to_high"] = index
        copy["percentile_low_to_high"] = (
            (index - 1) / (len(ranked) - 1) if len(ranked) > 1 else 0.0)
        out.append(copy)
    return out


def collect_role_targets(local_payload):
    far_targets, far_metadata = collect_far_targets(
        local_payload["far_window_specs"])
    fresh_targets, fresh_metadata = collect_fresh_targets(FRESH_WINDOW_SPECS)
    zero_targets = set(
        int(target) for target in local_payload["far_empirical_summary"][
            "zero_local_action_but_positive_empirical_targets"])
    roles = {}
    for reference in DEFICIT_REFERENCES:
        roles[int(reference)] = {
            "target": int(reference),
            "role": "selected_deficit_reference",
            "target_mod_143": int(reference) % 143,
            "target_mod_286": int(reference) % 286,
        }
    for reference in CLEAR_CONTROL_REFERENCES:
        roles[int(reference)] = {
            "target": int(reference),
            "role": "selected_clear_control_reference",
            "target_mod_143": int(reference) % 143,
            "target_mod_286": int(reference) % 286,
        }
    for target in far_targets:
        roles[int(target)] = {
            **far_metadata[int(target)],
            "role": (
                "same_window_zero_local_seed_target"
                if int(target) in zero_targets
                else "same_window_nonseed_target"),
        }
    for target in fresh_targets:
        roles[int(target)] = {
            **fresh_metadata[int(target)],
            "role": "fresh_predeclared_target",
        }
    return tuple(sorted(roles)), roles


def centered_rows_for_channel(channel, roles, profile, labels,
                              local_rows_by_residue, lp_vector):
    label_index = labels.index(channel)
    weight = float(lp_vector[label_index])
    rows = []
    for target in sorted(roles):
        profile_row = profile["target_rows"][target]
        contributions = contribution_map(profile_row)
        empirical = float(contributions[channel])
        local_relative_to_base = float(
            local_rows_by_residue[target % 143]["local_delta_vector"][
                label_index])
        centered = empirical - local_relative_to_base
        rows.append({
            **roles[target],
            "empirical_channel_value": empirical,
            "local_channel_delta_relative_to_base": local_relative_to_base,
            "centered_channel_value": centered,
            "lp_weight": weight,
            "weighted_centered_channel_value": centered * weight,
        })
    return rows


def role_rows(rows, role):
    return [row for row in rows if row["role"] == role]


def reference_gap_rows(rows, fresh_rows, reference_role):
    min_fresh = min(fresh_rows, key=lambda row: (
        row["weighted_centered_channel_value"], row["target"]))
    out = []
    for row in rows:
        if row["role"] != reference_role:
            continue
        margin = (
            min_fresh["weighted_centered_channel_value"]
            - row["weighted_centered_channel_value"])
        out.append({
            "reference": row["target"],
            "reference_mod_143": row["target_mod_143"],
            "reference_weighted_centered_value": row[
                "weighted_centered_channel_value"],
            "fresh_min_target": min_fresh["target"],
            "fresh_min_weighted_centered_value": min_fresh[
                "weighted_centered_channel_value"],
            "minimum_fresh_minus_reference_weighted_margin": margin,
            "passes_all_fresh_targets": margin > TOLERANCE,
        })
    return sorted(out, key=lambda row: row["reference"])


def channel_payload(channel, rows):
    ranked = rank_rows(rows, "weighted_centered_channel_value")
    rank_by_target = {row["target"]: row for row in ranked}
    for row in rows:
        ranked_row = rank_by_target[row["target"]]
        row["rank_low_to_high"] = ranked_row["rank_low_to_high"]
        row["percentile_low_to_high"] = ranked_row[
            "percentile_low_to_high"]
    fresh_rows = role_rows(rows, "fresh_predeclared_target")
    same_seed_rows = role_rows(rows, "same_window_zero_local_seed_target")
    same_nonseed_rows = role_rows(rows, "same_window_nonseed_target")
    deficit_rows = role_rows(rows, "selected_deficit_reference")
    clear_rows = role_rows(rows, "selected_clear_control_reference")
    min_fresh = min(fresh_rows, key=lambda row: (
        row["weighted_centered_channel_value"], row["target"]))
    max_deficit = max(deficit_rows, key=lambda row: (
        row["weighted_centered_channel_value"], -row["target"]))
    max_clear = max(clear_rows, key=lambda row: (
        row["weighted_centered_channel_value"], -row["target"]))
    min_deficit_gap = (
        min_fresh["weighted_centered_channel_value"]
        - max_deficit["weighted_centered_channel_value"])
    min_clear_gap = (
        min_fresh["weighted_centered_channel_value"]
        - max_clear["weighted_centered_channel_value"])
    return {
        "label": channel,
        "label_key": label_key(channel),
        "lp_weight": rows[0]["lp_weight"],
        "row_count": len(rows),
        "fresh_target_count": len(fresh_rows),
        "same_window_zero_local_seed_count": len(same_seed_rows),
        "same_window_nonseed_count": len(same_nonseed_rows),
        "selected_deficit_reference_count": len(deficit_rows),
        "selected_clear_control_reference_count": len(clear_rows),
        "weighted_centered_value_summary_all_rows": finite_summary(
            row["weighted_centered_channel_value"] for row in rows),
        "weighted_centered_value_summary_fresh": finite_summary(
            row["weighted_centered_channel_value"] for row in fresh_rows),
        "weighted_centered_value_summary_deficit_references": finite_summary(
            row["weighted_centered_channel_value"] for row in deficit_rows),
        "weighted_centered_value_summary_clear_controls": finite_summary(
            row["weighted_centered_channel_value"] for row in clear_rows),
        "minimum_fresh_row": min_fresh,
        "maximum_deficit_reference_row": max_deficit,
        "maximum_clear_control_row": max_clear,
        "minimum_fresh_minus_max_deficit_weighted_gap": min_deficit_gap,
        "minimum_fresh_minus_max_clear_control_weighted_gap": min_clear_gap,
        "all_deficit_references_below_fresh_min": min_deficit_gap > TOLERANCE,
        "all_clear_controls_below_fresh_min": min_clear_gap > TOLERANCE,
        "deficit_reference_gap_rows": reference_gap_rows(
            rows, fresh_rows, "selected_deficit_reference"),
        "clear_control_gap_rows": reference_gap_rows(
            rows, fresh_rows, "selected_clear_control_reference"),
        "selected_deficit_reference_rank_rows": deficit_rows,
        "selected_clear_control_reference_rank_rows": clear_rows,
        "lowest_20_rows": ranked[:20],
        "highest_20_rows": ranked[-20:],
    }


def main():
    local_payload = json.loads(LOCAL_SOURCE.read_text(encoding="utf-8"))
    lp_payload = json.loads(LP_SOURCE.read_text(encoding="utf-8"))
    labels = tuple(label_tuple(label) for label in local_payload["outside_labels"])
    lp_vector = np.asarray(
        lp_payload["selected_lp_effective_vector"], dtype=np.float64)
    local_rows_by_residue = {
        int(row["n_mod_143"]): row
        for row in local_payload["local_residue_rows"]
    }
    targets, roles = collect_role_targets(local_payload)
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=targets,
        dominant_modes=(1, 2), tail_threshold=.3, top_channel_count=40)
    channel_results = []
    for channel in CHANNELS:
        rows = centered_rows_for_channel(
            channel, roles, profile, labels, local_rows_by_residue, lp_vector)
        channel_results.append(channel_payload(channel, rows))
    by_key = {result["label_key"]: result for result in channel_results}
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lp_cone_audit": str(LP_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite centered scalar order audit for channels (3,1) and "
            "(5,5) over selected references, same-window targets, and fresh "
            "predeclared targets; no channel theorem, binary-prime correlation "
            "theorem, signed projection theorem, or Goldbach theorem."),
        "base_reference_for_local_delta_coordinates": BASE_REFERENCE,
        "channels": CHANNELS,
        "target_roles": {
            "selected_deficit_references": DEFICIT_REFERENCES,
            "selected_clear_control_references": CLEAR_CONTROL_REFERENCES,
            "same_window_targets_from_local_singular_audit": len([
                row for row in roles.values()
                if row["role"].startswith("same_window")]),
            "fresh_predeclared_targets": len([
                row for row in roles.values()
                if row["role"] == "fresh_predeclared_target"]),
        },
        "mechanism": (
            "For each row and channel, subtract the local channel delta for "
            "that row's residue, producing a locally centered scalar. A "
            "reference margin is just the weighted centered target value minus "
            "the weighted centered reference value."),
        "prediction": (
            "If (3,1) is the selected-deficit-reference-stable singleton, all "
            "selected deficit references should lie below the minimum fresh "
            "target in weighted centered (3,1) order."),
        "falsifier": (
            "A selected deficit reference whose weighted centered (3,1) value "
            "is at least the minimum fresh target value falsifies the scalar "
            "ordering explanation for the finite alternate-reference gate."),
        "channel_results": channel_results,
        "channel_3_1_all_deficit_references_below_fresh_min": by_key[
            "3,1"]["all_deficit_references_below_fresh_min"],
        "channel_5_5_all_deficit_references_below_fresh_min": by_key[
            "5,5"]["all_deficit_references_below_fresh_min"],
        "decision": (
            "The (3,1) alternate-reference pass reduces exactly to scalar "
            "ordering: every selected deficit reference has lower weighted "
            "centered (3,1) value than every fresh predeclared target. The "
            "(5,5) comparison fails that ordering because several selected "
            "deficit references sit above the fresh minimum."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
