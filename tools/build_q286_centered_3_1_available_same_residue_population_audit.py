"""Audit centered (3,1) same-residue gaps on available non-selection rows.

The signed-gap obligation was checked first on fresh predeclared windows.
This receipt widens the same-residue comparison to the already-used
same-window population while keeping the seed and nonseed groups separate.

Finite evidence only: this proves no stress-class theorem, signed correlation
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

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)
from tools.build_q286_alternate_reference_channel_audit import (  # noqa: E402
    CLEAR_CONTROL_REFERENCES,
    DEFICIT_REFERENCES,
)
from tools.build_q286_centered_3_1_same_residue_fresh_population_audit import (  # noqa: E402
    CHANNEL,
    CHANNEL_KEY,
    TOLERANCE,
    compact_row,
    comparison_scope,
    row_key,
)
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    collect_far_targets,
    contribution_map,
    label_tuple,
)
from tools.build_q286_fresh_window_channel_watchlist_audit import (  # noqa: E402
    FRESH_WINDOW_SPECS,
    collect_targets as collect_fresh_targets,
)


EVIDENCE = ROOT / "evidence"
OUT = (
    EVIDENCE
    / "q286-centered-3-1-available-same-residue-population-audit.json")


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


def collect_roles(local_payload):
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


def centered_rows(targets, roles, profile, labels, local_rows_by_residue,
                  lp_vector):
    label_index = labels.index(CHANNEL)
    weight = float(lp_vector[label_index])
    rows = []
    for target in sorted(targets):
        row = profile["target_rows"][int(target)]
        contributions = contribution_map(row)
        empirical = float(contributions[CHANNEL])
        local_relative_to_base = float(
            local_rows_by_residue[int(target) % 143]["local_delta_vector"][
                label_index])
        centered = empirical - local_relative_to_base
        rows.append({
            **roles[int(target)],
            "empirical_channel_value": empirical,
            "local_channel_delta_relative_to_base": local_relative_to_base,
            "centered_channel_value": centered,
            "lp_weight": weight,
            "weighted_centered_channel_value": centered * weight,
        })
    return rows


def scope_with_rows(deficit, rows, scope_id, role_names):
    role_names = tuple(role_names)
    return comparison_scope(
        deficit,
        rows,
        scope_id,
        lambda row: row["role"] in role_names)


def scope_from_gap_rows(scope):
    gaps = scope["first_12_gap_rows"] + scope["failing_gap_rows"]
    by_target = {row["comparison_target"]: row for row in gaps}
    values = list(by_target.values())
    return {
        "comparison_count": scope["comparison_count"],
        "all_comparisons_above_deficit": (
            scope["all_comparisons_above_deficit"]),
        "failing_comparison_count": scope["failing_comparison_count"],
        "weighted_gap_summary": scope["weighted_gap_summary"],
        "minimum_comparison_target": (
            scope["minimum_comparison_row"]["target"]
            if scope["minimum_comparison_row"] else None),
        "minimum_weighted_centered_channel_value": (
            scope["minimum_comparison_row"][
                "weighted_centered_channel_value"]
            if scope["minimum_comparison_row"] else None),
        "first_12_gap_rows": scope["first_12_gap_rows"],
        "failing_gap_rows": scope["failing_gap_rows"],
        "stored_gap_row_count": len(values),
    }


def all_gap_rows(scope):
    rows = {
        row["comparison_target"]: row for row in scope["first_12_gap_rows"]
    }
    rows.update({
        row["comparison_target"]: row for row in scope["failing_gap_rows"]
    })
    return tuple(rows.values())


def main():
    local_payload = load_json(LOCAL_SOURCE)
    lp_payload = load_json(LP_SOURCE)
    labels = tuple(label_tuple(label) for label in local_payload["outside_labels"])
    lp_vector = np.asarray(
        lp_payload["selected_lp_effective_vector"], dtype=np.float64)
    local_rows_by_residue = {
        int(row["n_mod_143"]): row
        for row in local_payload["local_residue_rows"]
    }

    targets, roles = collect_roles(local_payload)
    selected_residues = {
        roles[int(reference)]["target_mod_143"]
        for reference in DEFICIT_REFERENCES
    }
    targets = tuple(
        target for target in targets
        if roles[target]["role"].startswith("selected_")
        or roles[target]["target_mod_143"] in selected_residues)
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=targets,
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=40)
    rows = centered_rows(
        targets, roles, profile, labels, local_rows_by_residue, lp_vector)
    selected_deficits = [
        row for row in rows if row["role"] == "selected_deficit_reference"]

    scopes = (
        (
            "same_residue_same_window_zero_local_seed_targets",
            ("same_window_zero_local_seed_target",),
        ),
        (
            "same_residue_same_window_nonseed_targets",
            ("same_window_nonseed_target",),
        ),
        (
            "same_residue_same_window_all_targets",
            (
                "same_window_zero_local_seed_target",
                "same_window_nonseed_target",
            ),
        ),
        (
            "same_residue_fresh_predeclared_targets",
            ("fresh_predeclared_target",),
        ),
        (
            "same_residue_all_available_nonselection_targets",
            (
                "same_window_zero_local_seed_target",
                "same_window_nonseed_target",
                "fresh_predeclared_target",
            ),
        ),
    )

    deficit_rows = []
    all_scope_failures = []
    all_weighted_gaps = []
    for deficit in sorted(selected_deficits, key=lambda row: row["target"]):
        scope_rows = []
        for scope_id, role_names in scopes:
            scope = scope_with_rows(deficit, rows, scope_id, role_names)
            all_weighted_gaps.extend(
                row["weighted_gap_comparison_minus_deficit"]
                for row in all_gap_rows(scope))
            if scope["failing_comparison_count"]:
                all_scope_failures.append({
                    "reference": deficit["target"],
                    "scope_id": scope_id,
                    "failing_comparison_count": (
                        scope["failing_comparison_count"]),
                    "failing_gap_rows": scope["failing_gap_rows"],
                })
            scope_rows.append(scope_from_gap_rows(scope))
            scope_rows[-1]["scope_id"] = scope_id
        deficit_rows.append({
            "deficit": compact_row(deficit),
            "scope_rows": scope_rows,
        })

    scope_summaries = []
    for scope_id, _role_names in scopes:
        matching = [
            scope
            for deficit_row in deficit_rows
            for scope in deficit_row["scope_rows"]
            if scope["scope_id"] == scope_id
        ]
        compared = [
            scope for scope in matching if scope["comparison_count"] > 0]
        scope_summaries.append({
            "scope_id": scope_id,
            "reference_count_with_comparisons": len(compared),
            "total_comparison_count": sum(
                scope["comparison_count"] for scope in matching),
            "all_compared_references_pass": (
                bool(compared)
                and all(
                    scope["all_comparisons_above_deficit"]
                    for scope in compared)),
            "failing_reference_count": sum(
                1 for scope in matching
                if scope["failing_comparison_count"]),
            "minimum_weighted_gap": min(
                (
                    scope["weighted_gap_summary"]["minimum"]
                    for scope in matching
                    if scope["weighted_gap_summary"]["count"]
                ),
                default=None),
        })

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lp_cone_audit": str(LP_SOURCE.relative_to(ROOT)),
        "channel": list(CHANNEL),
        "channel_key": CHANNEL_KEY,
        "status_boundary": (
            "finite available-population same-residue audit only; no "
            "selected-stress theorem, signed correlation theorem, pointwise "
            "character-sum theorem, or Goldbach proof."),
        "mechanism": (
            "For same-residue comparisons modulo 143, the local q286 (3,1) "
            "coordinate is identical. Any remaining centered gap is therefore "
            "an empirical/correlation-side signed gap."),
        "prediction": (
            "If the selected-deficit (3,1) signed-gap obligation generalizes "
            "beyond fresh-window rows, selected deficit references should "
            "also sit below same-residue same-window seed and nonseed rows "
            "that were not selected as fresh comparisons."),
        "falsifier": (
            "Any available same-residue nonselection target with weighted "
            "centered (3,1) value at or below the selected deficit reference "
            "falsifies the corresponding finite population version."),
        "target_role_counts": {
            role: sum(1 for row in rows if row["role"] == role)
            for role in sorted({row["role"] for row in rows})
        },
        "profile_target_count_after_residue_filter": len(targets),
        "selected_reference_residues_mod_143": sorted(selected_residues),
        "scope_summaries": scope_summaries,
        "deficit_rows": deficit_rows,
        "failure_rows": all_scope_failures,
        "any_available_population_failure": bool(all_scope_failures),
        "stored_weighted_gap_summary": finite_summary(all_weighted_gaps),
        "decision": (
            "This receipt is the next finite falsifier/strengthening gate for "
            "the centered (3,1) signed-gap obligation. Read "
            "any_available_population_failure and the per-scope summaries; "
            "passing fresh windows alone must not be promoted if same-window "
            "seed or nonseed comparisons fail."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
