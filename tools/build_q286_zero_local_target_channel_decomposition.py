"""Decompose the 12 q286 zero-local-action targets across outside channels.

The local singular audit found 12 far stress targets with zero local LP action
but positive empirical LP delta.  These are target integers, not neutral
channels.  This receipt subtracts the stored near-zero local delta vector and
prints the remaining empirical/correlation contribution across all 17 outside
channels for each target.

This is finite decomposition evidence only.  It proves no binary-prime
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
LOCAL_SINGULAR_SOURCE = (
    ROOT / "evidence" / "q286-lp-cone-local-singular-audit.json")
LP_SOURCE = ROOT / "evidence" / "q286-low-frequency-lp-cone-audit.json"
OUT = ROOT / "evidence" / "q286-zero-local-target-channel-decomposition.json"
STRESS_TARGET = 1222142
TOLERANCE = 1e-12
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def label_tuple(label):
    return tuple(int(part) for part in label)


def contribution_map(row):
    return {
        label_tuple(item["representative_label"]): float(
            item["contribution_to_principal_ratio"])
        for item in row["real_channel_contribution_rows"]
    }


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


def vector_summary(vector):
    positives = tuple(value for value in vector if value > TOLERANCE)
    negatives = tuple(value for value in vector if value < -TOLERANCE)
    zeros = len(vector) - len(positives) - len(negatives)
    return {
        "entry_count": len(vector),
        "positive_count": len(positives),
        "negative_count": len(negatives),
        "zero_count": zeros,
        "positive_sum": math.fsum(positives),
        "negative_sum": math.fsum(negatives),
        "l1": math.fsum(abs(value) for value in vector),
        "l2": float(np.linalg.norm(np.asarray(vector, dtype=np.float64))),
        "minimum": min(vector),
        "maximum": max(vector),
    }


def main():
    local_payload = json.loads(
        LOCAL_SINGULAR_SOURCE.read_text(encoding="utf-8"))
    lp_payload = json.loads(LP_SOURCE.read_text(encoding="utf-8"))
    outside_labels = tuple(
        label_tuple(label) for label in local_payload["outside_labels"])
    lp_effective_vector = np.asarray(
        lp_payload["selected_lp_effective_vector"], dtype=np.float64)
    if len(outside_labels) != 17 or lp_effective_vector.shape != (17,):
        raise AssertionError("outside labels or LP vector drifted")

    zero_targets = tuple(int(target) for target in local_payload[
        "far_empirical_summary"][
            "zero_local_action_but_positive_empirical_targets"])
    if len(zero_targets) != 12:
        raise AssertionError("zero-local target count drifted")
    zero_residues = tuple(sorted({target % 143 for target in zero_targets}))
    local_rows_by_residue = {
        int(row["n_mod_143"]): row
        for row in local_payload["local_residue_rows"]
    }
    zero_local_rows_by_residue = {
        residue: local_rows_by_residue[residue]
        for residue in zero_residues
    }

    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=(STRESS_TARGET,) + zero_targets,
        dominant_modes=(1, 2), tail_threshold=.3, top_channel_count=40)
    stress_contributions = contribution_map(
        profile["target_rows"][STRESS_TARGET])

    rows = []
    all_after_local_entries = []
    for target in zero_targets:
        profile_row = profile["target_rows"][target]
        if not profile_row["dominant_floor_passes"]:
            raise AssertionError(f"zero-local target is not a clear: {target}")
        contributions = contribution_map(profile_row)
        empirical_delta = np.asarray([
            contributions[label] - stress_contributions[label]
            for label in outside_labels
        ], dtype=np.float64)
        local_row = zero_local_rows_by_residue[target % 143]
        local_delta_vector = np.asarray(
            local_row["local_delta_vector"], dtype=np.float64)
        after_local = empirical_delta - local_delta_vector
        all_after_local_entries.extend(float(value) for value in after_local)
        channel_rows = []
        for label, empirical, local, residual, lp_weight in zip(
                outside_labels, empirical_delta, local_delta_vector,
                after_local, lp_effective_vector):
            channel_rows.append({
                "label": label,
                "empirical_delta": float(empirical),
                "local_delta": float(local),
                "after_local_delta": float(residual),
                "lp_effective_weight": float(lp_weight),
                "lp_weighted_after_local": float(residual * lp_weight),
                "sign_after_local": (
                    "positive" if residual > TOLERANCE
                    else "negative" if residual < -TOLERANCE
                    else "zero"),
            })
        full_after_local = float(np.sum(after_local))
        lp_after_local = float(after_local @ lp_effective_vector)
        rows.append({
            "target": target,
            "target_mod_143": target % 143,
            "target_mod_286": target % 286,
            "window_start": next(
                row["window_start"]
                for row in local_payload["far_empirical_summary"][
                    "rows_by_low_local_lp_action"]
                if int(row["target"]) == target),
            "local_delta_l2": float(np.linalg.norm(local_delta_vector)),
            "local_lp_action": float(local_delta_vector @ lp_effective_vector),
            "empirical_full_outside_delta": float(np.sum(empirical_delta)),
            "after_local_full_outside_delta": full_after_local,
            "empirical_lp_delta": float(empirical_delta @ lp_effective_vector),
            "after_local_lp_delta": lp_after_local,
            "after_local_vector_summary": vector_summary(
                tuple(float(value) for value in after_local)),
            "channel_rows": channel_rows,
            "channels_by_negative_after_local": sorted(
                channel_rows,
                key=lambda item: (item["after_local_delta"], item["label"])),
            "channels_by_lp_weighted_after_local": sorted(
                channel_rows,
                key=lambda item: (
                    -item["lp_weighted_after_local"], item["label"])),
        })

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_local_singular_audit": str(
            LOCAL_SINGULAR_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lp_cone_audit": str(
            LP_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite decomposition of the 12 zero-local-action target "
            "integers only; it subtracts the stored local delta vector and "
            "shows the remaining 17-channel empirical/correlation deltas. "
            "It proves no binary-prime correlation theorem, residual-bound "
            "theorem, signed projection theorem, or Goldbach theorem."),
        "correction": (
            "The 12 cases are target integers with zero local LP action, not "
            "12 neutral channels."),
        "candidate": (
            "Rows with zero local LP action but positive empirical LP delta "
            "expose the non-local/correlation contribution channel by channel."),
        "mechanism": (
            "For the 12 far targets whose residues have zero local LP action, "
            "subtract the corresponding local stress-relative character-moment "
            "delta vector, whose L2 norm is numerical zero, from the exact "
            "clear-minus-stress outside-channel delta vector."),
        "prediction": (
            "If the positivity is injected beyond the local singular layer, "
            "the after-local channel vectors should still have positive full "
            "and LP-weighted sums despite zero local action."),
        "falsifier": (
            "Any zero-local target whose after-local full or LP sum is "
            "nonpositive falsifies this finite non-local/correlation "
            "decomposition reading for that target."),
        "novelty_label": "new-to-this-task",
        "outside_labels": outside_labels,
        "zero_local_targets": zero_targets,
        "zero_local_target_count": len(zero_targets),
        "zero_local_target_residues_mod_143": zero_residues,
        "local_zero_rows_by_residue": {
            residue: {
                "local_delta_vector": tuple(
                    float(value) for value in row["local_delta_vector"]),
                "local_delta_l2": row["local_delta_l2"],
                "local_lp_action": row["local_lp_delta_action"],
                "local_low_frequency_action": (
                    row["local_low_frequency_delta_action"]),
                "local_rank1_action": row["local_rank1_delta_action"],
            }
            for residue, row in zero_local_rows_by_residue.items()
        },
        "target_rows": rows,
        "after_local_full_delta_summary": finite_summary(
            row["after_local_full_outside_delta"] for row in rows),
        "after_local_lp_delta_summary": finite_summary(
            row["after_local_lp_delta"] for row in rows),
        "after_local_entry_summary": finite_summary(all_after_local_entries),
        "after_local_positive_entry_count": sum(
            1 for value in all_after_local_entries if value > TOLERANCE),
        "after_local_negative_entry_count": sum(
            1 for value in all_after_local_entries if value < -TOLERANCE),
        "after_local_zero_entry_count": sum(
            1 for value in all_after_local_entries
            if abs(value) <= TOLERANCE),
        "all_after_local_full_sums_positive": all(
            row["after_local_full_outside_delta"] > TOLERANCE
            for row in rows),
        "all_after_local_lp_sums_positive": all(
            row["after_local_lp_delta"] > TOLERANCE for row in rows),
        "decision": (
            "The zero-local target rows are carried entirely by the empirical "
            "after-local channel vector at this resolution. This supports the "
            "claim that local singular support is insufficient and that the "
            "bridge must control binary prime-pair correlation across the "
            "17 outside channels."),
        "zero_local_target_channel_decomposition_measured": True,
        "local_layer_alone_explains_zero_residue_empirical_positive_rows": False,
        "binary_prime_pair_correlation_bridge_still_required": True,
        "rank1_residual_bound_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
