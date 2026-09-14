"""Build q286 stable-core/volatile-rim named holdout evidence.

The stable-core/volatile-rim budget survived two near-boundary clear rows.
This builder freezes that partition and applies it to the broader named clear
rows already used in the pressure diagnostics.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIGN_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pairwise-swing-sign-stability.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-stable-core-named-holdout.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)


REFERENCE_TARGET = 1222142
SAMPLE_TARGETS = (
    1222142,
    1242118,
    1240888,
    1243018,
    1243130,
    1244072,
    1244094,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_ready(item) for item in value]
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def channel_map(row):
    return {
        tuple(channel["representative_label"]): (
            channel["contribution_to_principal_ratio"])
        for channel in row["real_channel_contribution_rows"]
    }


def build_row(reference, clear, stable_positive, stable_negative, volatile):
    reference_channels = channel_map(reference)
    clear_channels = channel_map(clear)

    def group_sum(labels):
        return math.fsum(
            clear_channels.get(label, 0.0)
            - reference_channels.get(label, 0.0)
            for label in labels)

    stable_positive_swing = group_sum(stable_positive)
    stable_negative_swing = group_sum(stable_negative)
    volatile_swing = group_sum(volatile)
    stable_core = stable_positive_swing + stable_negative_swing
    tail_margin = (
        reference["dominant_character_sum_to_principal_ratio"] + 0.3)
    clear_margin = clear["dominant_character_sum_to_principal_ratio"] + 0.3
    stable_core_margin = tail_margin + stable_core
    final_margin = stable_core_margin + volatile_swing
    volatile_drag = -volatile_swing if volatile_swing < 0.0 else 0.0
    budget = stable_core_margin if stable_core_margin > 0.0 else math.nan
    return {
        "reference_target": reference["target"],
        "clear_target": clear["target"],
        "clear_target_mod_286": clear["target_mod_286"],
        "clear_dominant_floor_passes": clear["dominant_floor_passes"],
        "reference_floor_margin": tail_margin,
        "clear_floor_margin": clear_margin,
        "stable_positive_swing_sum": stable_positive_swing,
        "stable_negative_swing_sum": stable_negative_swing,
        "stable_core_net_swing": stable_core,
        "volatile_rim_net_swing": volatile_swing,
        "stable_core_margin_to_floor": stable_core_margin,
        "final_floor_margin_reconstructed": final_margin,
        "clear_floor_margin_reconstruction_error": abs(
            final_margin - clear_margin),
        "stable_core_alone_clears_reference": bool(
            stable_core_margin >= 0.0),
        "volatile_rim_within_budget": bool(
            stable_core_margin >= 0.0
            and volatile_swing >= -stable_core_margin),
        "volatile_drag_budget": budget,
        "actual_volatile_drag": volatile_drag,
        "volatile_drag_budget_used_fraction": (
            volatile_drag / budget if budget and budget > 0.0 else math.nan),
    }


def main():
    sign_payload = json.loads(SIGN_SOURCE.read_text(encoding="utf-8"))
    stable_positive = tuple(
        tuple(label) for label in sign_payload["stable_positive_labels"])
    stable_negative = tuple(
        tuple(label) for label in sign_payload["stable_negative_labels"])
    volatile = tuple(
        tuple(label) for label in sign_payload["sign_flip_labels"])
    receipt = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=SAMPLE_TARGETS,
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=25)
    rows = receipt["target_rows"]
    reference = rows[REFERENCE_TARGET]
    holdout_rows = tuple(
        build_row(reference, rows[target],
                  stable_positive, stable_negative, volatile)
        for target in SAMPLE_TARGETS
        if target != REFERENCE_TARGET)
    failures = tuple(
        row for row in holdout_rows
        if not row["stable_core_alone_clears_reference"]
        or not row["volatile_rim_within_budget"])
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_evidence": str(SIGN_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite named-row stable-core holdout diagnostic only; no "
            "stable-core theorem, volatile-rim theorem, coupled curve theorem, "
            "pointwise character-sum estimate, or Goldbach proof is "
            "established"),
        "mechanism": (
            "Freeze the stable-positive, stable-negative, and volatile-rim "
            "labels derived from the two near-boundary clear comparisons and "
            "apply them to the broader named pressure fixture."),
        "falsifier": (
            "A named clear row where stable-core margin is nonpositive, or "
            "where volatile-rim drag exceeds stable-core margin, falsifies "
            "this fixed partition as a named-row holdout certificate."),
        "reference_target": REFERENCE_TARGET,
        "sample_targets": SAMPLE_TARGETS,
        "stable_positive_labels": stable_positive,
        "stable_negative_labels": stable_negative,
        "volatile_labels": volatile,
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "holdout_rows": holdout_rows,
        "failure_rows": failures,
        "holdout_target_count": len(holdout_rows),
        "failure_count": len(failures),
        "all_stable_core_rows_clear_reference": all(
            row["stable_core_alone_clears_reference"]
            for row in holdout_rows),
        "all_volatile_rims_within_budget": all(
            row["volatile_rim_within_budget"] for row in holdout_rows),
        "maximum_clear_floor_margin_reconstruction_error": max(
            row["clear_floor_margin_reconstruction_error"]
            for row in holdout_rows),
        "minimum_stable_core_margin_row": min(
            holdout_rows,
            key=lambda row: row["stable_core_margin_to_floor"]),
        "maximum_budget_used_row": max(
            holdout_rows,
            key=lambda row: (
                row["volatile_drag_budget_used_fraction"]
                if row["volatile_drag_budget_used_fraction"] is not None
                else -math.inf)),
        "interpretation": {
            "observed_shape": (
                "The frozen stable-core/volatile-rim partition survives the "
                "broader named clear fixture if failure_count is zero."),
            "remaining_theorem": (
                "A uniform proof still needs arithmetic estimates forcing "
                "stable-core surplus and bounding volatile-rim drag outside "
                "this finite fixture."),
        },
        "stable_core_named_holdout_measured": True,
        "stable_core_theorem_proved": False,
        "volatile_rim_bound_proved": False,
        "coupled_pressure_offset_curve_proved": False,
        "pointwise_character_sum_estimate_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
