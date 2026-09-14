"""Build q286 pairwise swing sign-stability evidence.

The pairwise channel-swing diagnostic showed broad tail-to-clear movement.
This derivative builder asks whether the broad movement at least has a stable
helpful/harmful channel partition across the two named clear comparisons.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pairwise-channel-swing.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pairwise-swing-sign-stability.json")


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
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def label_key(row):
    return tuple(row["representative_label"])


def sign(value, tolerance):
    if value > tolerance:
        return 1
    if value < -tolerance:
        return -1
    return 0


def main():
    source_payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    pair_rows = source_payload["pair_rows"]
    if len(pair_rows) != 2:
        raise ValueError("expected exactly two pair rows")
    tolerance = 1e-12
    maps = []
    for pair in pair_rows:
        maps.append({
            label_key(row): row["clear_minus_tail_swing_to_principal"]
            for row in pair["channel_swing_rows"]
        })
    all_labels = sorted(set(maps[0]) | set(maps[1]))
    rows = []
    stable_positive_rows = []
    stable_negative_rows = []
    flip_rows = []
    zero_rows = []
    for label in all_labels:
        first_delta = maps[0].get(label, 0.0)
        second_delta = maps[1].get(label, 0.0)
        first_sign = sign(first_delta, tolerance)
        second_sign = sign(second_delta, tolerance)
        row = {
            "representative_label": label,
            "first_pair_swing": first_delta,
            "second_pair_swing": second_delta,
            "first_pair_sign": first_sign,
            "second_pair_sign": second_sign,
            "same_nonzero_sign": bool(
                first_sign != 0 and first_sign == second_sign),
            "sign_flips": bool(
                first_sign != 0 and second_sign != 0
                and first_sign != second_sign),
            "zero_in_either_pair": bool(first_sign == 0 or second_sign == 0),
        }
        rows.append(row)
        if row["same_nonzero_sign"] and first_sign > 0:
            stable_positive_rows.append(row)
        elif row["same_nonzero_sign"] and first_sign < 0:
            stable_negative_rows.append(row)
        elif row["sign_flips"]:
            flip_rows.append(row)
        else:
            zero_rows.append(row)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_evidence": str(SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite derivative sign-stability diagnostic only; no stable "
            "partition theorem, stable-core theorem, coupled pressure/offset "
            "curve theorem, pointwise character-sum estimate, or Goldbach "
            "proof is established"),
        "mechanism": (
            "After one-channel swing was demoted, test whether the broad "
            "tail-to-clear swing has a fixed helpful/harmful channel sign "
            "partition across the two named clear comparisons."),
        "falsifier": (
            "Any nonzero sign flips across the named comparisons refute a "
            "single fixed helpful/harmful partition on this fixture."),
        "pair_targets": source_payload["pair_targets"],
        "channel_count": len(rows),
        "stable_positive_channel_count": len(stable_positive_rows),
        "stable_negative_channel_count": len(stable_negative_rows),
        "stable_nonzero_channel_count": (
            len(stable_positive_rows) + len(stable_negative_rows)),
        "sign_flip_channel_count": len(flip_rows),
        "zero_channel_count": len(zero_rows),
        "stable_positive_labels": tuple(
            row["representative_label"] for row in stable_positive_rows),
        "stable_negative_labels": tuple(
            row["representative_label"] for row in stable_negative_rows),
        "sign_flip_labels": tuple(
            row["representative_label"] for row in flip_rows),
        "stable_positive_first_pair_swing_sum": math.fsum(
            row["first_pair_swing"] for row in stable_positive_rows),
        "stable_positive_second_pair_swing_sum": math.fsum(
            row["second_pair_swing"] for row in stable_positive_rows),
        "stable_negative_first_pair_swing_sum": math.fsum(
            row["first_pair_swing"] for row in stable_negative_rows),
        "stable_negative_second_pair_swing_sum": math.fsum(
            row["second_pair_swing"] for row in stable_negative_rows),
        "flip_first_pair_swing_sum": math.fsum(
            row["first_pair_swing"] for row in flip_rows),
        "flip_second_pair_swing_sum": math.fsum(
            row["second_pair_swing"] for row in flip_rows),
        "channel_rows": rows,
        "interpretation": {
            "fixed_partition": (
                "Demoted on the named fixture because nonzero channel sign "
                "flips occur across the two clear comparisons."),
            "stable_core": (
                "A narrower stable-core plus volatile-rim aggregate theorem "
                "is not refuted by this diagnostic, but it remains only a "
                "candidate theorem target."),
        },
        "pairwise_swing_sign_stability_measured": True,
        "fixed_helpful_harmful_partition_falsified_on_named_pairs": bool(
            flip_rows),
        "stable_core_theorem_proved": False,
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
