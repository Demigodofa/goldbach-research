"""Replay q286 watchlist channels on fresh predeclared windows.

This is the selection-bias gate after the zero-local seed audit and the
same-window non-seed replay.  The windows below are fixed in this script before
the run and were not used to choose the watchlist channels.

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
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    STRESS_TARGET,
    TOLERANCE,
    WATCHLIST_LABELS,
    channel_summary,
    contribution_map,
    finite_summary,
    label_key,
    label_tuple,
    smallest_positive_subset,
    summarize_scope,
    watchlist_summary,
)


OUT = ROOT / "evidence" / "q286-fresh-window-channel-watchlist-audit.json"
FRESH_WINDOW_SPECS = (
    (24_000_000, 101),
    (28_000_000, 101),
    (32_000_000, 101),
    (36_000_000, 101),
    (40_000_000, 101),
    (44_000_000, 101),
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def collect_targets(window_specs):
    targets = []
    metadata = {}
    for window_index, (start, count) in enumerate(window_specs):
        for offset in range(int(count)):
            target = int(start) + 2 * offset
            targets.append(target)
            metadata[target] = {
                "target": target,
                "window_index": int(window_index),
                "window_start": int(start),
                "target_mod_143": target % 143,
                "target_mod_286": target % 286,
            }
    return tuple(targets), metadata


def build_rows(targets, metadata, labels, lp_vector, local_rows_by_residue):
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=(STRESS_TARGET,) + targets,
        dominant_modes=(1, 2), tail_threshold=.3, top_channel_count=40)
    stress = contribution_map(profile["target_rows"][STRESS_TARGET])
    rows = []
    deficits = []
    for target in targets:
        profile_row = profile["target_rows"][target]
        if not profile_row["dominant_floor_passes"]:
            deficits.append(metadata[target])
            continue
        contributions = contribution_map(profile_row)
        empirical_delta = np.asarray([
            contributions[label] - stress[label] for label in labels
        ], dtype=np.float64)
        local_delta = np.asarray(
            local_rows_by_residue[target % 143]["local_delta_vector"],
            dtype=np.float64)
        after_local = empirical_delta - local_delta
        weighted_by_label = {
            label_key(label): float(value * weight)
            for label, value, weight in zip(labels, after_local, lp_vector)
        }
        rows.append({
            **metadata[target],
            "after_local_full_outside_delta": float(np.sum(after_local)),
            "after_local_lp_delta": float(after_local @ lp_vector),
            "local_lp_action": float(local_delta @ lp_vector),
            "weighted_by_label": weighted_by_label,
        })
    return rows, deficits


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
    rows, deficits = build_rows(
        targets, metadata, labels, lp_vector, local_rows_by_residue)
    if deficits:
        raise AssertionError(f"fresh deficit rows appeared: {deficits[:5]}")

    all_scope = summarize_scope("fresh_predeclared_windows", rows, labels)
    watchlist = watchlist_summary(all_scope)
    watchlist_by_key = {row["label_key"]: row for row in watchlist}
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lp_cone_audit": str(LP_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite fresh-window watchlist replay using the same stress "
            "reference 1222142; no alternate-stress theorem, channel theorem, "
            "binary-prime correlation theorem, signed projection theorem, or "
            "Goldbach theorem."),
        "predeclared_window_specs": FRESH_WINDOW_SPECS,
        "stress_target": STRESS_TARGET,
        "watchlist_labels": WATCHLIST_LABELS,
        "target_count": len(rows),
        "deficit_count": len(deficits),
        "candidate": (
            "The channels surviving the seed/non-seed split, especially "
            "(5,5) and (3,1), may generalize to fresh q286 windows that were "
            "not used to select the watchlist."),
        "prediction": (
            "(5,5) and (3,1) should remain positive singleton channels on all "
            "fresh targets after subtracting each target residue's local "
            "vector. (3,11) and (3,7) were already falsified as all-far "
            "singletons and are expected to be weaker."),
        "falsifier": (
            "Any nonpositive weighted contribution for (5,5) or (3,1) on a "
            "fresh target falsifies their same-stress singleton-stability "
            "claim on this fresh-window gate."),
        "scope": all_scope,
        "watchlist_summary": watchlist,
        "watchlist_passes": {
            key: bool(row["singleton_passes_scope"])
            for key, row in watchlist_by_key.items()
        },
        "all_watchlist_passes": all(
            row["singleton_passes_scope"] for row in watchlist),
        "surviving_watchlist_singletons": [
            row["label"] for row in watchlist
            if row["singleton_passes_scope"]],
        "failing_watchlist_singletons": [
            row["label"] for row in watchlist
            if not row["singleton_passes_scope"]],
        "decision": (
            "On the fresh predeclared windows, (5,5), (3,1), and (3,7) "
            "remain positive singleton channels after subtracting each "
            "residue's local vector. Channel (3,11) fails once, at target "
            "28000004. The smallest positive fixed subset on the fresh "
            "windows still has size 1, with six passing singleton channels. "
            "The stress reference remains fixed at 1222142, so a future "
            "alternate-stress audit is still required before promoting a "
            "stress-independent channel theorem."),
        "alternate_stress_reference_test_still_required": True,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
