"""Build q286 pressure/offset scalar-separator falsifier evidence.

The bulk-share diagnostic says negative pressure is not top-k concentrated.
This builder checks the next tempting simplification: maybe a scalar positive
offset or offset/pressure ratio floor separates the named clear rows from the
named tail row.  The named fixture falsifies that simplification.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pressure-offset-scalar-falsifier.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)


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


def compact_row(source_row, tail_threshold):
    pressure = source_row["negative_channel_pressure_to_principal"]
    offset = source_row["positive_channel_offset_to_principal"]
    ratio = (
        offset / pressure
        if pressure > 0.0 else math.inf)
    required_ratio = (
        1.0 - tail_threshold / pressure
        if pressure > 0.0 else -math.inf)
    return {
        "target": source_row["target"],
        "target_mod_286": source_row["target_mod_286"],
        "dominant_sum_to_principal": (
            source_row["dominant_character_sum_to_principal_ratio"]),
        "dominant_floor_passes": source_row["dominant_floor_passes"],
        "negative_pressure_B": pressure,
        "positive_offset_P": offset,
        "positive_to_negative_pressure_ratio_R": ratio,
        "required_positive_offset_for_floor": (
            source_row["required_positive_offset_for_floor"]),
        "positive_offset_slack_to_floor": (
            source_row["positive_offset_slack_to_floor"]),
        "exact_required_ratio_for_threshold": required_ratio,
        "exact_curve_margin": ratio - required_ratio,
        "negative_real_channel_count": (
            source_row["negative_real_channel_count"]),
        "positive_real_channel_count": (
            source_row["positive_real_channel_count"]),
        "mean_negative_pressure_per_negative_channel": (
            pressure / source_row["negative_real_channel_count"]
            if source_row["negative_real_channel_count"] else math.nan),
        "mean_positive_offset_per_positive_channel": (
            offset / source_row["positive_real_channel_count"]
            if source_row["positive_real_channel_count"] else math.nan),
    }


def main():
    receipt = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=SAMPLE_TARGETS,
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=25)
    tail_threshold = receipt["tail_threshold"]
    rows = {
        target: compact_row(row, tail_threshold)
        for target, row in receipt["target_rows"].items()
    }
    tail_rows = [
        row for row in rows.values()
        if not row["dominant_floor_passes"]]
    clear_rows = [
        row for row in rows.values()
        if row["dominant_floor_passes"]]

    offset_counterexamples = []
    ratio_counterexamples = []
    pressure_excess_clear_rows = []
    for tail_row in tail_rows:
        for clear_row in clear_rows:
            if tail_row["positive_offset_P"] >= clear_row[
                    "positive_offset_P"]:
                offset_counterexamples.append({
                    "tail_target": tail_row["target"],
                    "clear_target": clear_row["target"],
                    "tail_positive_offset_P": tail_row[
                        "positive_offset_P"],
                    "clear_positive_offset_P": clear_row[
                        "positive_offset_P"],
                    "tail_minus_clear_positive_offset": (
                        tail_row["positive_offset_P"]
                        - clear_row["positive_offset_P"]),
                })
            if tail_row["positive_to_negative_pressure_ratio_R"] >= (
                    clear_row["positive_to_negative_pressure_ratio_R"]):
                ratio_counterexamples.append({
                    "tail_target": tail_row["target"],
                    "clear_target": clear_row["target"],
                    "tail_ratio_R": tail_row[
                        "positive_to_negative_pressure_ratio_R"],
                    "clear_ratio_R": clear_row[
                        "positive_to_negative_pressure_ratio_R"],
                    "tail_minus_clear_ratio": (
                        tail_row["positive_to_negative_pressure_ratio_R"]
                        - clear_row[
                            "positive_to_negative_pressure_ratio_R"]),
                })
    for clear_row in clear_rows:
        if clear_row["negative_pressure_B"] > tail_threshold:
            pressure_excess_clear_rows.append(clear_row)

    exact_curve_mismatches = [
        row["target"] for row in rows.values()
        if (row["exact_curve_margin"] >= -1e-9)
        != row["dominant_floor_passes"]]
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite named-row scalar-separator falsifier only; no scalar "
            "offset theorem, scalar ratio theorem, coupled pressure/offset "
            "curve theorem, pointwise character-sum estimate, or Goldbach "
            "proof is established"),
        "mechanism": (
            "After top-k negative pressure was demoted, test whether the "
            "positive rescue side can be separated by one scalar offset "
            "floor or one scalar offset/pressure ratio floor."),
        "falsifier": (
            "If a failing named row has at least as much positive offset or "
            "at least as high a positive/negative ratio as a clear named row, "
            "then that scalar floor cannot certify the clear row without also "
            "certifying the tail row."),
        "sample_targets": SAMPLE_TARGETS,
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": tail_threshold,
        "dominant_floor_failure_targets": (
            receipt["dominant_floor_failure_targets"]),
        "dominant_floor_pass_targets": receipt["dominant_floor_pass_targets"],
        "positive_offset_floor_counterexamples": offset_counterexamples,
        "positive_ratio_floor_counterexamples": ratio_counterexamples,
        "pressure_excess_clear_rows": pressure_excess_clear_rows,
        "exact_curve_mismatch_targets": exact_curve_mismatches,
        "target_rows": rows,
        "maximum_real_channel_identity_error": (
            receipt["maximum_real_channel_identity_error"]),
        "interpretation": {
            "scalar_offset_floor": (
                "Falsified on the named fixture: the tail row can have more "
                "positive offset than a clear row."),
            "scalar_ratio_floor": (
                "Falsified on the named fixture: the tail row can have a "
                "higher positive/negative pressure ratio than a clear row."),
            "pressure_only": (
                "The algebraic pressure-only sufficient condition remains "
                "B <= tau.  Named clear rows with B > tau show pressure "
                "excess is not itself failure."),
            "remaining_theorem": (
                "The viable scalar formulation is the coupled exact curve "
                "P >= B - tau, equivalently R >= 1 - tau/B when B > 0, "
                "or a stronger arithmetic theorem implying it."),
        },
        "dominant_mode_pressure_offset_scalar_falsifier_measured": True,
        "uniform_positive_offset_floor_falsified_on_named_rows": bool(
            offset_counterexamples),
        "uniform_positive_ratio_floor_falsified_on_named_rows": bool(
            ratio_counterexamples),
        "pressure_excess_implies_failure_falsified_on_named_rows": bool(
            pressure_excess_clear_rows),
        "coupled_pressure_offset_curve_proved": False,
        "scalar_offset_theorem_proved": False,
        "scalar_ratio_theorem_proved": False,
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
