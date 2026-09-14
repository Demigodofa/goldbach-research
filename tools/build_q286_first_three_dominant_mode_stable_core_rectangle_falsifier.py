"""Build q286 stable-core one-parameter rectangle falsifier evidence.

The stable-core named holdout kept a coupled budget alive.  This derivative
builder checks whether that budget can be simplified to one independent
allowance A where every row has stable-core margin at least A and volatile
drag at most A.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-stable-core-named-holdout.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-stable-core-rectangle-falsifier.json")


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


def row_key(row):
    return (
        row["clear_target"],
        row["stable_core_margin_to_floor"],
        row["actual_volatile_drag"],
    )


def main():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = tuple(source["holdout_rows"])
    if not rows:
        raise RuntimeError("stable-core named holdout contains no rows")

    min_margin_row = min(
        rows, key=lambda row: row["stable_core_margin_to_floor"])
    max_drag_row = max(rows, key=lambda row: row["actual_volatile_drag"])
    min_stable_margin = min_margin_row["stable_core_margin_to_floor"]
    max_volatile_drag = max_drag_row["actual_volatile_drag"]
    feasible_one_parameter = bool(max_volatile_drag <= min_stable_margin)
    obstruction_gap = max_volatile_drag - min_stable_margin

    row_summaries = tuple({
        "clear_target": row["clear_target"],
        "clear_target_mod_286": row["clear_target_mod_286"],
        "stable_core_margin_to_floor": row[
            "stable_core_margin_to_floor"],
        "actual_volatile_drag": row["actual_volatile_drag"],
        "coupled_budget_slack": (
            row["stable_core_margin_to_floor"]
            - row["actual_volatile_drag"]),
        "passes_coupled_budget": row["volatile_rim_within_budget"],
    } for row in sorted(rows, key=row_key))

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_evidence": str(SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite derivative falsifier only; no stable-core theorem, "
            "volatile-rim theorem, one-parameter budget theorem, pointwise "
            "character-sum estimate, or Goldbach proof is established"),
        "mechanism": (
            "Attempt to simplify the surviving coupled stable-core / "
            "volatile-rim budget to one independent allowance A."),
        "tested_simplification": (
            "Find A such that every named clear row has stable-core margin "
            "at least A and volatile drag at most A; such an A would make a "
            "row-independent rectangle budget certify the coupled floor."),
        "falsifier": (
            "The simplification is falsified on the named fixture when the "
            "largest observed volatile drag is larger than the smallest "
            "observed stable-core margin."),
        "reference_target": source["reference_target"],
        "holdout_target_count": source["holdout_target_count"],
        "minimum_stable_core_margin_row": min_margin_row,
        "maximum_volatile_drag_row": max_drag_row,
        "minimum_stable_core_margin": min_stable_margin,
        "maximum_volatile_drag": max_volatile_drag,
        "one_parameter_rectangle_budget_exists_on_named_rows": (
            feasible_one_parameter),
        "one_parameter_rectangle_budget_falsified_on_named_rows": (
            not feasible_one_parameter),
        "one_parameter_obstruction_gap": obstruction_gap,
        "row_summaries": row_summaries,
        "all_coupled_rows_still_pass": all(
            row["passes_coupled_budget"] for row in row_summaries),
        "interpretation": {
            "closed_shortcut": (
                "The named fixture does not support replacing the coupled "
                "row-dependent inequality by one shared surplus/drag "
                "allowance."),
            "surviving_target": (
                "A proof must control volatile drag as a function of the "
                "available stable-core margin, split pressure subregions, or "
                "replace the route with lower-support/complement rescue."),
        },
        "stable_core_rectangle_falsifier_measured": True,
        "coupled_budget_still_alive_on_named_rows": all(
            row["passes_coupled_budget"] for row in row_summaries),
        "one_parameter_rectangle_budget_theorem_proved": False,
        "stable_core_theorem_proved": False,
        "volatile_rim_bound_proved": False,
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
