"""Audit selected q286 (3,1) deficits against same-residue fresh targets.

The residue-collision audit showed selected deficits stay below selected
clear controls with the same residue modulo 143. This receipt widens the
same-residue comparison to the frozen fresh predeclared target population.

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

from tools.build_q286_alternate_reference_channel_audit import (  # noqa: E402
    DEFICIT_REFERENCES,
)
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    contribution_map,
    label_tuple,
)
from tools.build_q286_fresh_window_channel_watchlist_audit import (  # noqa: E402
    FRESH_WINDOW_SPECS,
    collect_targets,
)
from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)


EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-centered-3-1-same-residue-fresh-population-audit.json"

CHANNEL = (3, 1)
CHANNEL_KEY = "3,1"
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


def row_key(row):
    return row["weighted_centered_channel_value"], row["target"]


def compact_row(row):
    out = {
        "target": row["target"],
        "target_mod_143": row["target_mod_143"],
        "target_mod_286": row["target_mod_286"],
        "role": row["role"],
        "empirical_channel_value": row["empirical_channel_value"],
        "local_channel_delta_relative_to_base": (
            row["local_channel_delta_relative_to_base"]),
        "centered_channel_value": row["centered_channel_value"],
        "weighted_centered_channel_value": (
            row["weighted_centered_channel_value"]),
    }
    for key in ("window_start", "window_index", "offset"):
        if key in row:
            out[key] = row[key]
    return out


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
            "weighted_centered_channel_value": centered * weight,
        })
    return rows


def comparison_scope(deficit, rows, scope_id, predicate):
    comparison_rows = [
        row for row in rows
        if row["target"] != deficit["target"]
        and row["target_mod_143"] == deficit["target_mod_143"]
        and predicate(row)
    ]
    comparison_rows = sorted(comparison_rows, key=row_key)
    gap_rows = []
    for row in comparison_rows:
        local_gap = (
            row["local_channel_delta_relative_to_base"]
            - deficit["local_channel_delta_relative_to_base"])
        weighted_gap = (
            row["weighted_centered_channel_value"]
            - deficit["weighted_centered_channel_value"])
        gap_rows.append({
            "comparison_target": row["target"],
            "comparison_role": row["role"],
            "local_gap": local_gap,
            "empirical_gap_comparison_minus_deficit": (
                row["empirical_channel_value"]
                - deficit["empirical_channel_value"]),
            "centered_gap_comparison_minus_deficit": (
                row["centered_channel_value"]
                - deficit["centered_channel_value"]),
            "weighted_gap_comparison_minus_deficit": weighted_gap,
            "comparison_above_deficit": weighted_gap > TOLERANCE,
        })
    failing = [
        row for row in gap_rows
        if not row["comparison_above_deficit"]]
    return {
        "scope_id": scope_id,
        "comparison_count": len(comparison_rows),
        "all_comparisons_above_deficit": bool(gap_rows) and not failing,
        "failing_comparison_count": len(failing),
        "weighted_gap_summary": finite_summary(
            row["weighted_gap_comparison_minus_deficit"]
            for row in gap_rows),
        "minimum_comparison_row": (
            compact_row(comparison_rows[0]) if comparison_rows else None),
        "maximum_comparison_row": (
            compact_row(comparison_rows[-1]) if comparison_rows else None),
        "first_12_gap_rows": gap_rows[:12],
        "failing_gap_rows": failing[:20],
    }


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
    fresh_targets, fresh_metadata = collect_targets(FRESH_WINDOW_SPECS)
    roles = {}
    for target in DEFICIT_REFERENCES:
        roles[int(target)] = {
            "target": int(target),
            "role": "selected_deficit_reference",
            "target_mod_143": int(target) % 143,
            "target_mod_286": int(target) % 286,
        }
    for target, row in fresh_metadata.items():
        roles[int(target)] = {
            **row,
            "role": "fresh_predeclared_target",
        }
    targets = tuple(sorted(roles))
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=targets,
        dominant_modes=(1, 2), tail_threshold=.3, top_channel_count=40)
    rows = centered_rows(
        targets, roles, profile, labels, local_rows_by_residue, lp_vector)
    selected_deficits = [
        row for row in rows if row["role"] == "selected_deficit_reference"]

    deficit_rows = []
    for deficit in sorted(selected_deficits, key=lambda row: row["target"]):
        scopes = [
            comparison_scope(
                deficit, rows, "same_residue_fresh_predeclared_targets",
                lambda row: row["role"] == "fresh_predeclared_target"),
        ]
        deficit_rows.append({
            "deficit": compact_row(deficit),
            "scopes": scopes,
            "fresh_population_passes": scopes[0][
                "all_comparisons_above_deficit"],
        })

    fresh_failures = [
        row for row in deficit_rows if not row["fresh_population_passes"]]

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lp_cone_audit": str(LP_SOURCE.relative_to(ROOT)),
        "channel": list(CHANNEL),
        "channel_key": CHANNEL_KEY,
        "status_boundary": (
            "finite same-residue population audit only; no stress-classifier "
            "theorem, signed correlation theorem, pointwise character-sum "
            "theorem, or Goldbach proof."),
        "mechanism": (
            "Within each residue modulo 143, the local q286 channel vector is "
            "identical. Same-residue gaps in centered (3,1) therefore measure "
            "empirical/correlation-side separation after local subtraction."),
        "prediction": (
            "If the selected-deficit (3,1) stress-reference signal is not "
            "only due to handpicked same-residue clear controls, selected "
            "deficit references should remain below broader same-residue "
            "fresh predeclared populations."),
        "falsifier": (
            "Any fresh predeclared same-residue target at or below a selected "
            "deficit in weighted centered (3,1) falsifies the fresh-population "
            "version for that reference."),
        "target_role_counts": {
            role: sum(1 for row in rows if row["role"] == role)
            for role in sorted({row["role"] for row in rows})
        },
        "deficit_rows": deficit_rows,
        "all_selected_deficits_pass_same_residue_fresh_population": (
            not fresh_failures),
        "fresh_population_failures": [
            row["deficit"]["target"] for row in fresh_failures],
        "decision": (
            "The fresh predeclared same-residue population supports the "
            "selected-deficit (3,1) signal beyond handpicked same-residue "
            "clear controls if all_selected_deficits_pass_same_residue_fresh_"
            "population is true."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
