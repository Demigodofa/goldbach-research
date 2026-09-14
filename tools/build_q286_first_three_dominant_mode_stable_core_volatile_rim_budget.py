"""Build q286 stable-core/volatile-rim budget evidence.

The sign-stability diagnostic leaves a narrower candidate: stable helpful core
plus a bounded volatile rim.  This builder quantifies that budget on the two
named tail-to-clear comparisons.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAIR_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pairwise-channel-swing.json")
SIGN_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pairwise-swing-sign-stability.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-stable-core-volatile-rim-budget.json")


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


def main():
    pair_payload = json.loads(PAIR_SOURCE.read_text(encoding="utf-8"))
    sign_payload = json.loads(SIGN_SOURCE.read_text(encoding="utf-8"))
    pair_rows = pair_payload["pair_rows"]
    if len(pair_rows) != 2:
        raise ValueError("expected exactly two pair rows")
    stable_core_sums = (
        (
            sign_payload["stable_positive_first_pair_swing_sum"],
            sign_payload["stable_negative_first_pair_swing_sum"],
            sign_payload["flip_first_pair_swing_sum"],
        ),
        (
            sign_payload["stable_positive_second_pair_swing_sum"],
            sign_payload["stable_negative_second_pair_swing_sum"],
            sign_payload["flip_second_pair_swing_sum"],
        ),
    )

    rows = []
    for pair, (stable_positive, stable_negative, volatile_rim) in zip(
            pair_rows, stable_core_sums):
        tail_floor_margin = (
            pair["tail_row"]["dominant_sum_to_principal"] + 0.3)
        clear_floor_margin = (
            pair["clear_row"]["dominant_sum_to_principal"] + 0.3)
        stable_core = stable_positive + stable_negative
        stable_core_margin = tail_floor_margin + stable_core
        final_margin = tail_floor_margin + stable_core + volatile_rim
        allowed_volatile_drag = -stable_core_margin
        actual_volatile_drag = (
            -volatile_rim if volatile_rim < 0.0 else 0.0)
        budget = -allowed_volatile_drag
        rows.append({
            "tail_target": pair["tail_target"],
            "clear_target": pair["clear_target"],
            "tail_floor_margin": tail_floor_margin,
            "clear_floor_margin": clear_floor_margin,
            "tail_positive_offset_slack_to_floor": (
                pair["tail_row"]["positive_offset_slack_to_floor"]),
            "clear_positive_offset_slack_to_floor": (
                pair["clear_row"]["positive_offset_slack_to_floor"]),
            "stable_positive_swing_sum": stable_positive,
            "stable_negative_swing_sum": stable_negative,
            "stable_core_net_swing": stable_core,
            "volatile_rim_net_swing": volatile_rim,
            "stable_core_margin_to_floor": stable_core_margin,
            "final_floor_margin_reconstructed": final_margin,
            "clear_floor_margin_reconstruction_error": abs(
                final_margin - clear_floor_margin),
            "stable_core_alone_clears_tail": bool(
                stable_core_margin >= 0.0),
            "allowed_volatile_rim_lower_bound": allowed_volatile_drag,
            "actual_volatile_drag": actual_volatile_drag,
            "volatile_drag_budget": budget,
            "volatile_drag_budget_used_fraction": (
                actual_volatile_drag / budget if budget > 0.0 else math.nan),
            "volatile_rim_within_budget": bool(
                volatile_rim >= allowed_volatile_drag),
        })

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_evidence": (
            str(PAIR_SOURCE.relative_to(ROOT)),
            str(SIGN_SOURCE.relative_to(ROOT)),
        ),
        "status_boundary": (
            "finite derivative stable-core/volatile-rim budget diagnostic "
            "only; no stable-core theorem, volatile-rim bound, coupled "
            "pressure/offset curve theorem, pointwise character-sum estimate, "
            "or Goldbach proof is established"),
        "mechanism": (
            "After fixed sign partition was demoted, quantify whether the "
            "stable core alone clears the named tail and how much negative "
            "volatile-rim swing can be tolerated."),
        "falsifier": (
            "If stable-core slack is nonpositive or the volatile rim exceeds "
            "the allowed drag budget, the stable-core plus bounded-rim route "
            "fails on the named pair."),
        "pair_targets": sign_payload["pair_targets"],
        "stable_positive_channel_count": (
            sign_payload["stable_positive_channel_count"]),
        "stable_negative_channel_count": (
            sign_payload["stable_negative_channel_count"]),
        "sign_flip_channel_count": sign_payload["sign_flip_channel_count"],
        "budget_rows": rows,
        "all_stable_core_rows_clear_tail": all(
            row["stable_core_alone_clears_tail"] for row in rows),
        "all_volatile_rims_within_budget": all(
            row["volatile_rim_within_budget"] for row in rows),
        "maximum_clear_floor_margin_reconstruction_error": max(
            row["clear_floor_margin_reconstruction_error"] for row in rows),
        "interpretation": {
            "stable_core": (
                "On both named comparisons, the stable core alone would move "
                "the tail above the floor."),
            "volatile_rim": (
                "The volatile rim is net harmful on both comparisons but "
                "remains inside the finite named budget."),
            "remaining_theorem": (
                "A future proof target can be phrased as a positive stable "
                "core surplus plus an upper bound on volatile-rim drag, but "
                "this diagnostic proves neither bound uniformly."),
        },
        "stable_core_volatile_rim_budget_measured": True,
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
