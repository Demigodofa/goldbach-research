"""Audit fresh residue-lifts of positive q286-WBSS residual pushback rows.

The full dual-edge population audit still used one finite source population.
This receipt chooses the residue classes that actually pushed upward there,
then tests their next four period-lifts beyond the old maximum target.  The
coefficient geometry is the same modulo 10010, but the strict-central
binary-prime orbit measures are recomputed at fresh target values.

Finite targeted holdout only.  It proves no residual absorption theorem,
signed projection theorem, q286 threshold theorem, strict-central Goldbach
theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
POPULATION_SOURCE = (
    EVIDENCE / "q286-wbss-residual-absorption-population-audit.json")
OUT = EVIDENCE / "q286-wbss-residual-absorption-residue-lift-holdout.json"
PERIOD = 10010
FRESH_LIFT_COUNT = 4
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from tools.build_q286_wbss_main_term_sign_audit import finite_summary
from tools.build_q286_wbss_residual_absorption_threshold_audit import (
    THRESHOLDS,
    absorption_rows,
    absorption_rows_for_edge_rows,
    source_commit,
    threshold_profile,
)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def first_lift_above(residue, lower_bound):
    multiplier = math.floor((lower_bound - residue) / PERIOD) + 1
    target = residue + multiplier * PERIOD
    if target <= lower_bound:
        target += PERIOD
    if target % 2:
        raise ValueError("lifted target must be even")
    return target


def positive_source_rows(rows):
    positives = [
        row for row in rows
        if row["positive_residual_pushback"] > TOLERANCE
    ]
    by_residue = {}
    for row in positives:
        key = row["target_residue"]
        current = by_residue.get(key)
        if (current is None
                or row["pushback_to_main_drag_ratio"]
                > current["pushback_to_main_drag_ratio"]):
            by_residue[key] = row
    return sorted(
        by_residue.values(),
        key=lambda row: (
            -row["pushback_to_main_drag_ratio"], row["target"]),
    )


def holdout_edge_rows(source_rows, all_source_rows, lift_count=FRESH_LIFT_COUNT):
    lower_bound = max(row["target"] for row in all_source_rows)
    rows = []
    for source in source_rows:
        first_target = first_lift_above(source["target_residue"], lower_bound)
        for lift_index in range(lift_count):
            target = first_target + lift_index * PERIOD
            rows.append({
                "target": target,
                "target_residue": target % PERIOD,
                "target_mod_286": target % 286,
                "block_index_after_discovery": (
                    max(0, (target - lower_bound + PERIOD - 1) // PERIOD)),
                "source_positive_target": source["target"],
                "source_pushback_to_main_drag_ratio": (
                    source["pushback_to_main_drag_ratio"]),
            })
    return rows, lower_bound


def lift_index(row, lower_bound):
    return (row["target"] - first_lift_above(
        row["target_residue"], lower_bound)) // PERIOD


def bucket_summary(name, rows):
    ratio_rows = [
        row for row in rows
        if row["pushback_to_main_drag_ratio"] is not None
    ]
    ratios = [row["pushback_to_main_drag_ratio"] for row in ratio_rows]
    top20_nonnegative_rows = [
        row for row in rows
        if row["bandlimited_top20_component"] >= -TOLERANCE
    ]
    worst = max(
        ratio_rows,
        key=lambda row: (
            row["pushback_to_main_drag_ratio"], -row["target"]),
    ) if ratio_rows else None
    threshold_profiles = []
    for threshold_name, threshold in THRESHOLDS:
        profile = threshold_profile(threshold_name, threshold, ratio_rows)
        failing = top20_nonnegative_rows + profile["failing_rows"]
        profile.update({
            "passes_all_theorem_conditions": not failing,
            "top20_nonnegative_failure_count": len(top20_nonnegative_rows),
            "theorem_failing_row_count": len(failing),
            "theorem_failing_rows": sorted(
                failing,
                key=lambda row: (
                    row["target"],
                    row.get("pushback_to_main_drag_ratio") is None,
                ),
            )[:20],
        })
        threshold_profiles.append(profile)
    return {
        "name": name,
        "row_count": len(rows),
        "positive_pushback_row_count": sum(
            row["positive_residual_pushback"] > TOLERANCE for row in rows),
        "top20_nonnegative_count": len(top20_nonnegative_rows),
        "top20_nonnegative_rows": sorted(
            top20_nonnegative_rows,
            key=lambda row: (row["bandlimited_top20_component"], row["target"]),
        )[:20],
        "pushback_to_main_drag_ratio_summary": finite_summary(ratios),
        "observed_minimum_passing_constant": max(ratios) if ratios else None,
        "worst_row": worst,
        "threshold_profiles": threshold_profiles,
    }


def profile_by_name(summary, name):
    return {
        row["name"]: row for row in summary["threshold_profiles"]
    }[name]


def build_receipt():
    population = load_json(POPULATION_SOURCE)
    all_source_rows = absorption_rows(include_discovery=True)
    source_rows = positive_source_rows(all_source_rows)
    edge_rows, lower_bound = holdout_edge_rows(source_rows, all_source_rows)
    fresh_rows = absorption_rows_for_edge_rows(
        edge_rows, require_top20_negative=False)
    metadata_by_target = {row["target"]: row for row in edge_rows}
    enriched_rows = []
    for row in fresh_rows:
        metadata = metadata_by_target[row["target"]]
        enriched_rows.append({
            **row,
            "lift_index": int(lift_index(row, lower_bound)),
            "source_positive_target": metadata["source_positive_target"],
            "source_pushback_to_main_drag_ratio": (
                metadata["source_pushback_to_main_drag_ratio"]),
        })

    all_summary = bucket_summary("all_residue_lift_holdout_rows", enriched_rows)
    by_lift = {}
    for index in range(FRESH_LIFT_COUNT):
        rows = [row for row in enriched_rows if row["lift_index"] == index]
        by_lift[f"lift_{index}"] = bucket_summary(f"lift_{index}", rows)

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "population_audit": str(POPULATION_SOURCE.relative_to(ROOT)),
            "population_source_commit": population["source_commit"],
        },
        "status_boundary": (
            "finite targeted q286-WBSS residue-lift holdout only; rows are "
            "selected from prior positive-pushback residue classes and "
            "recomputed at later targets, not an unbiased sample, asymptotic "
            "estimate, residual absorption theorem, signed projection theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"),
        "goldbach_proved": False,
        "residual_absorption_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "fresh_holdout_claimed": True,
        "universal_bound_open": True,
        "selection_boundary": (
            "The holdout is adversarially targeted: source residues are the "
            "unique residue classes with positive residual pushback in the "
            "full 230-row dual-edge population.  Only target values are fresh."),
        "candidate": {
            "name": "positive-residual residue-lift stress holdout",
            "mechanism": (
                "Keep the q286-WBSS coefficient geometry fixed modulo 10010 "
                "and test whether the same positive-residual residue classes "
                "remain controlled when lifted to later targets with fresh "
                "strict-central prime-pair measures."),
            "prediction": (
                "If .126/.13 are not purely artifacts of the original target "
                "values, the next four lifts of the positive-pushback residues "
                "should keep top-20 drag negative and stay below those caps."),
            "falsifier": (
                "Any lifted row with nonnegative top-20 contribution or "
                "pushback/top20-drag above .126 or .13 clips that finite cap "
                "to the older population."),
            "smallest_test": (
                "Take unique positive-pushback residue classes from the 230 "
                "dual-edge rows and evaluate their next four period-lifts "
                "above the old maximum target."),
            "novelty_label": "new-to-this-task",
        },
        "source_population": {
            "row_count": population["summaries"][
                "all_dual_edge_rows"]["row_count"],
            "positive_pushback_row_count": population["summaries"][
                "all_dual_edge_rows"]["positive_pushback_row_count"],
            "unique_positive_residue_count": len(source_rows),
            "old_maximum_target": lower_bound,
            "old_observed_minimum_passing_constant": population[
                "summaries"]["all_dual_edge_rows"][
                    "observed_minimum_passing_constant"],
        },
        "holdout": {
            "lift_count_per_residue": FRESH_LIFT_COUNT,
            "target_count": len(enriched_rows),
            "target_minimum": min(row["target"] for row in enriched_rows),
            "target_maximum": max(row["target"] for row in enriched_rows),
            "summary": all_summary,
            "summary_by_lift": by_lift,
            "largest_pushback_rows": sorted(
                [
                    row for row in enriched_rows
                    if row["pushback_to_main_drag_ratio"] is not None
                ],
                key=lambda row: (
                    -row["pushback_to_main_drag_ratio"], row["target"]),
            )[:20],
        },
        "one_eighth_cap_falsified_on_holdout": (
            not profile_by_name(all_summary, "one_eighth")[
                "passes_all_theorem_conditions"]),
        "top20_bandlimited_route_demoted_by_holdout": (
            all_summary["top20_nonnegative_count"] > 0),
        "point_126_cap_survives_holdout": profile_by_name(
            all_summary, "decimal_0_126")["passes_all_theorem_conditions"],
        "point_13_cap_survives_holdout": profile_by_name(
            all_summary, "decimal_0_13")["passes_all_theorem_conditions"],
        "decision": (
            "The fresh residue-lift holdout demotes the top-20 plus residual "
            "absorption route as a portable theorem skeleton.  The first "
            f"condition, top-20 negative drag, fails on "
            f"{all_summary['top20_nonnegative_count']} of "
            f"{all_summary['row_count']} lifted rows.  Even among rows where "
            "top-20 drag stays negative, the maximum positive "
            "pushback/top20-drag ratio is "
            f"{all_summary['observed_minimum_passing_constant']}.  Thus .126 "
            "and .13 do not survive this targeted fresh holdout.  The "
            "Fourier split remains a diagnostic of the original dual-edge "
            "population, but the next theorem should switch to a direct raw "
            "signed-witness estimate or a different aggregate inequality.  "
            "Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
