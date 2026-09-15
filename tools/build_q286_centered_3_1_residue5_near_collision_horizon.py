"""Probe the centered (3,1) residue-5 near-collision horizon.

The available same-residue audit found the tightest checked gate at reference
164598 versus target 8000140, both residue 5 modulo 143. This receipt tests a
predeclared one-residue micro-horizon around 8000140.

Finite evidence only: this proves no selected-stress theorem, signed
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
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)
from tools.build_q286_centered_3_1_available_same_residue_population_audit import (  # noqa: E402
    load_json,
)
from tools.build_q286_centered_3_1_same_residue_fresh_population_audit import (  # noqa: E402
    CHANNEL,
    CHANNEL_KEY,
    TOLERANCE,
)
from tools.build_q286_far_singleton_channel_stability_audit import (  # noqa: E402
    LOCAL_SOURCE,
    LP_SOURCE,
    contribution_map,
    label_tuple,
)


EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-centered-3-1-residue5-near-collision-horizon.json"

REFERENCE_TARGET = 164_598
CENTER_TARGET = 8_000_140
OFFSET_RADIUS = 50
STEP = 286


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


def horizon_targets():
    return tuple(
        CENTER_TARGET + STEP * offset
        for offset in range(-OFFSET_RADIUS, OFFSET_RADIUS + 1))


def centered_row(target, role, offset, profile, labels, local_rows_by_residue,
                 lp_vector):
    label_index = labels.index(CHANNEL)
    weight = float(lp_vector[label_index])
    contributions = contribution_map(profile["target_rows"][int(target)])
    empirical = float(contributions[CHANNEL])
    local_relative_to_base = float(
        local_rows_by_residue[int(target) % 143]["local_delta_vector"][
            label_index])
    centered = empirical - local_relative_to_base
    return {
        "target": int(target),
        "target_mod_143": int(target) % 143,
        "target_mod_286": int(target) % 286,
        "role": role,
        "offset_from_center_in_286_steps": offset,
        "empirical_channel_value": empirical,
        "local_channel_delta_relative_to_base": local_relative_to_base,
        "centered_channel_value": centered,
        "lp_weight": weight,
        "weighted_centered_channel_value": centered * weight,
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

    targets = horizon_targets()
    if any(target % 143 != REFERENCE_TARGET % 143 for target in targets):
        raise AssertionError("horizon contains a nonmatching residue")
    if CENTER_TARGET not in targets:
        raise AssertionError("near-collision center target missing")

    sample_targets = (REFERENCE_TARGET,) + targets
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=sample_targets,
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=40)

    reference = centered_row(
        REFERENCE_TARGET,
        "selected_deficit_reference",
        None,
        profile,
        labels,
        local_rows_by_residue,
        lp_vector)
    rows = [
        centered_row(
            target,
            "residue5_near_collision_horizon_target",
            offset,
            profile,
            labels,
            local_rows_by_residue,
            lp_vector)
        for offset, target in zip(
            range(-OFFSET_RADIUS, OFFSET_RADIUS + 1), targets)
    ]
    for row in rows:
        row["weighted_gap_above_reference"] = (
            row["weighted_centered_channel_value"]
            - reference["weighted_centered_channel_value"])
        row["empirical_gap_above_reference"] = (
            row["empirical_channel_value"]
            - reference["empirical_channel_value"])
        row["centered_gap_above_reference"] = (
            row["centered_channel_value"]
            - reference["centered_channel_value"])
        row["local_gap"] = (
            row["local_channel_delta_relative_to_base"]
            - reference["local_channel_delta_relative_to_base"])
        row["passes_reference_gate"] = (
            row["weighted_gap_above_reference"] > TOLERANCE)

    ranked = sorted(
        rows,
        key=lambda row: (row["weighted_gap_above_reference"], row["target"]))
    failing = [row for row in ranked if not row["passes_reference_gate"]]
    center_row = next(row for row in rows if row["target"] == CENTER_TARGET)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_local_singular_audit": str(LOCAL_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lp_cone_audit": str(LP_SOURCE.relative_to(ROOT)),
        "channel": list(CHANNEL),
        "channel_key": CHANNEL_KEY,
        "reference_target": REFERENCE_TARGET,
        "center_target": CENTER_TARGET,
        "step": STEP,
        "offset_radius": OFFSET_RADIUS,
        "target_count": len(rows),
        "residue_mod_143": REFERENCE_TARGET % 143,
        "status_boundary": (
            "finite residue-5 near-collision horizon only; no selected-stress "
            "theorem, signed correlation theorem, pointwise character-sum "
            "theorem, or Goldbach proof."),
        "mechanism": (
            "All horizon targets share the selected reference residue modulo "
            "143, so the local q286 (3,1) coordinate cancels. The checked "
            "gap is empirical/correlation-side."),
        "prediction": (
            "If the 164598/8000140 near-collision is not already a local "
            "finite counterexample, the predeclared residue-5 micro-horizon "
            "around 8000140 should remain above reference 164598 in weighted "
            "centered (3,1)."),
        "falsifier": (
            "Any horizon target with weighted centered (3,1) value at or "
            "below reference 164598 falsifies this finite residue-5 horizon "
            "version of the selected-reference gap."),
        "reference_row": reference,
        "center_row": center_row,
        "all_horizon_targets_pass_reference_gate": not failing,
        "failing_target_count": len(failing),
        "failing_rows": failing,
        "weighted_gap_summary": finite_summary(
            row["weighted_gap_above_reference"] for row in rows),
        "empirical_gap_summary": finite_summary(
            row["empirical_gap_above_reference"] for row in rows),
        "local_gap_summary": finite_summary(row["local_gap"] for row in rows),
        "tightest_rows": ranked[:12],
        "widest_rows": ranked[-12:],
        "decision": (
            "Read all_horizon_targets_pass_reference_gate. A pass strengthens "
            "the finite selected-reference (3,1) evidence around the current "
            "tightest available-population near-collision; a failure clips "
            "the selected-reference gap to a smaller finite scope."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
