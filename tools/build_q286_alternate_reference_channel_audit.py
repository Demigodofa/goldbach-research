"""Test q286 watchlist channels against alternate reference rows.

Earlier q286 singleton audits subtracted the same stress reference, 1222142.
This audit checks whether the live singleton channels are stable when the
reference row is changed to other selected deficit and clear-control rows.

Finite evidence only: this proves no reference-independent channel theorem,
binary-prime correlation theorem, signed projection theorem, or Goldbach.
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
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    TOLERANCE,
    WATCHLIST_LABELS,
    contribution_map,
    label_key,
    label_tuple,
    smallest_positive_subset,
    summarize_scope,
    watchlist_summary,
)
from tools.build_q286_fresh_window_channel_watchlist_audit import (  # noqa: E402
    FRESH_WINDOW_SPECS,
    collect_targets,
)


OUT = ROOT / "evidence" / "q286-alternate-reference-channel-audit.json"
BASE_REFERENCE = 1_222_142
DEFICIT_REFERENCES = (24_424, 13_822, 55_864, 164_598, 1_222_142)
CLEAR_CONTROL_REFERENCES = (13_556, 40_420, 129_706, 1_242_118, 1_240_888)
LIVE_SINGLETON_CANDIDATES = ((5, 5), (3, 1))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def build_rows_for_reference(targets, metadata, labels, lp_vector,
                             local_rows_by_residue, profile, reference):
    reference_row = profile["target_rows"][int(reference)]
    reference_contributions = contribution_map(reference_row)
    reference_local_delta = np.asarray(
        local_rows_by_residue[int(reference) % 143]["local_delta_vector"],
        dtype=np.float64)
    rows = []
    deficits = []
    for target in targets:
        profile_row = profile["target_rows"][target]
        if not profile_row["dominant_floor_passes"]:
            deficits.append(metadata[target])
            continue
        contributions = contribution_map(profile_row)
        empirical_delta = np.asarray([
            contributions[label] - reference_contributions[label]
            for label in labels
        ], dtype=np.float64)
        target_local_delta = np.asarray(
            local_rows_by_residue[target % 143]["local_delta_vector"],
            dtype=np.float64)
        local_delta_relative_to_reference = (
            target_local_delta - reference_local_delta)
        after_local = empirical_delta - local_delta_relative_to_reference
        weighted_by_label = {
            label_key(label): float(value * weight)
            for label, value, weight in zip(labels, after_local, lp_vector)
        }
        rows.append({
            **metadata[target],
            "reference": int(reference),
            "reference_mod_143": int(reference) % 143,
            "after_local_full_outside_delta": float(np.sum(after_local)),
            "after_local_lp_delta": float(after_local @ lp_vector),
            "local_lp_action_relative_to_reference": float(
                local_delta_relative_to_reference @ lp_vector),
            "weighted_by_label": weighted_by_label,
        })
    return rows, deficits


def summarize_reference(reference, role, rows, labels):
    scope = summarize_scope(
        f"fresh_targets_reference_{reference}", rows, labels)
    watchlist = watchlist_summary(scope)
    watchlist_by_key = {row["label_key"]: row for row in watchlist}
    live_candidate_rows = [
        watchlist_by_key[label_key(label)]
        for label in LIVE_SINGLETON_CANDIDATES
    ]
    return {
        "reference": int(reference),
        "reference_role": role,
        "reference_mod_143": int(reference) % 143,
        "scope": scope,
        "watchlist_summary": watchlist,
        "watchlist_passes": {
            key: bool(row["singleton_passes_scope"])
            for key, row in watchlist_by_key.items()
        },
        "live_singleton_candidate_passes": {
            label_key(row["label"]): bool(row["singleton_passes_scope"])
            for row in live_candidate_rows
        },
        "all_live_singleton_candidates_pass": all(
            row["singleton_passes_scope"] for row in live_candidate_rows),
        "failing_live_singleton_candidates": [
            row["label"] for row in live_candidate_rows
            if not row["singleton_passes_scope"]],
        "smallest_fixed_subset_up_to_full_search": scope[
            "smallest_fixed_subset"],
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
    targets, metadata = collect_targets(FRESH_WINDOW_SPECS)
    reference_roles = {
        **{reference: "selected_deficit_reference"
           for reference in DEFICIT_REFERENCES},
        **{reference: "selected_clear_control_reference"
           for reference in CLEAR_CONTROL_REFERENCES},
    }
    references = tuple(dict.fromkeys(
        DEFICIT_REFERENCES + CLEAR_CONTROL_REFERENCES))
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=references + targets,
        dominant_modes=(1, 2), tail_threshold=.3, top_channel_count=40)

    reference_results = []
    for reference in references:
        rows, deficits = build_rows_for_reference(
            targets, metadata, labels, lp_vector, local_rows_by_residue,
            profile, reference)
        if deficits:
            raise AssertionError(
                f"fresh deficit rows appeared for reference {reference}: "
                f"{deficits[:5]}")
        reference_results.append(summarize_reference(
            reference, reference_roles[reference], rows, labels))

    deficit_results = [
        result for result in reference_results
        if result["reference_role"] == "selected_deficit_reference"]
    clear_results = [
        result for result in reference_results
        if result["reference_role"] == "selected_clear_control_reference"]
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lp_cone_audit": str(LP_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite alternate-reference replay on the fresh predeclared "
            "windows only; no reference-independent channel theorem, "
            "binary-prime correlation theorem, signed projection theorem, or "
            "Goldbach theorem."),
        "fresh_window_specs": FRESH_WINDOW_SPECS,
        "target_count_per_reference": len(targets),
        "base_reference": BASE_REFERENCE,
        "deficit_references": DEFICIT_REFERENCES,
        "clear_control_references": CLEAR_CONTROL_REFERENCES,
        "watchlist_labels": WATCHLIST_LABELS,
        "live_singleton_candidates": LIVE_SINGLETON_CANDIDATES,
        "candidate": (
            "The same-stress singleton candidates (5,5) and (3,1) may be "
            "stable because of the q286 channel structure, not merely because "
            "reference row 1222142 is unusually low."),
        "prediction": (
            "(5,5) and (3,1) should remain positive singleton channels on the "
            "fresh windows when the reference is changed to other selected "
            "deficit rows. Clear-control references are reported separately "
            "because they are not stress deficits."),
        "falsifier": (
            "Any selected deficit reference for which (5,5) or (3,1) has a "
            "nonpositive weighted contribution on at least one fresh target "
            "falsifies reference-independent stability for that channel under "
            "this finite gate."),
        "reference_results": reference_results,
        "deficit_reference_all_live_candidates_pass": all(
            result["all_live_singleton_candidates_pass"]
            for result in deficit_results),
        "clear_control_reference_all_live_candidates_pass": all(
            result["all_live_singleton_candidates_pass"]
            for result in clear_results),
        "deficit_reference_failures": [
            {
                "reference": result["reference"],
                "failing_live_singleton_candidates": result[
                    "failing_live_singleton_candidates"],
            }
            for result in deficit_results
            if not result["all_live_singleton_candidates_pass"]
        ],
        "clear_control_reference_failures": [
            {
                "reference": result["reference"],
                "failing_live_singleton_candidates": result[
                    "failing_live_singleton_candidates"],
            }
            for result in clear_results
            if not result["all_live_singleton_candidates_pass"]
        ],
        "decision": (
            "Read the deficit_reference_* fields for the stress-reference "
            "gate. Clear-control references are diagnostic only; failure "
            "there shows the positive-channel claim depends on comparing "
            "against stress-like low rows, not arbitrary clear rows."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
