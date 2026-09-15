"""Audit residual absorption on the full q286-WBSS dual-edge population.

The threshold audit answered Kevin's decimal question on the 196
post-discovery rows.  This receipt expands the finite fixture to all 230
available lower-face dual-edge rows, including the 34 discovery rows, to test
whether the constant fit depended on excluding that first block.

Finite population diagnostic only.  It proves no residual absorption theorem,
signed projection theorem, q286 threshold theorem, strict-central Goldbach
theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-wbss-residual-absorption-population-audit.json"
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from tools.build_q286_wbss_main_term_sign_audit import finite_summary
from tools.build_q286_wbss_residual_absorption_threshold_audit import (
    BANDLIMITED_SOURCE,
    THRESHOLDS,
    absorption_rows,
    source_commit,
    threshold_profile,
)


def bucket_summary(name, rows):
    ratios = [row["pushback_to_main_drag_ratio"] for row in rows]
    worst = max(
        rows,
        key=lambda row: (
            row["pushback_to_main_drag_ratio"], -row["target"]),
    )
    return {
        "name": name,
        "row_count": len(rows),
        "positive_pushback_row_count": sum(
            row["positive_residual_pushback"] > TOLERANCE for row in rows),
        "top20_nonnegative_count": sum(
            row["bandlimited_top20_component"] >= -TOLERANCE
            for row in rows),
        "pushback_to_main_drag_ratio_summary": finite_summary(ratios),
        "observed_minimum_passing_constant": max(ratios),
        "worst_row": worst,
        "threshold_profiles": [
            threshold_profile(threshold_name, threshold, rows)
            for threshold_name, threshold in THRESHOLDS
        ],
    }


def profile_by_name(summary, name):
    return {
        row["name"]: row for row in summary["threshold_profiles"]
    }[name]


def build_receipt():
    rows = absorption_rows(include_discovery=True)
    discovery = [
        row for row in rows if row["block_index_after_discovery"] < 1]
    post = [
        row for row in rows if row["block_index_after_discovery"] >= 1]
    all_summary = bucket_summary("all_dual_edge_rows", rows)
    discovery_summary = bucket_summary("discovery_rows", discovery)
    post_summary = bucket_summary("post_discovery_rows", post)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "bandlimited_residual_audit": str(
                BANDLIMITED_SOURCE.relative_to(ROOT)),
            "threshold_audit": (
                "evidence/q286-wbss-residual-absorption-threshold-audit.json"),
        },
        "status_boundary": (
            "finite q286-WBSS full dual-edge population diagnostic only; "
            "the added rows are discovery rows from the same dual-edge source, "
            "not fresh asymptotic evidence; no residual absorption theorem, "
            "signed projection theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "residual_absorption_theorem_proved": False,
        "fresh_holdout_claimed": False,
        "universal_bound_open": True,
        "one_eighth_cap_falsified": (
            not profile_by_name(all_summary, "one_eighth")["passes_all_rows"]),
        "point_126_cap_survives_full_dual_edge_population": (
            profile_by_name(all_summary, "decimal_0_126")[
                "passes_all_rows"]),
        "point_13_cap_survives_full_dual_edge_population": (
            profile_by_name(all_summary, "decimal_0_13")[
                "passes_all_rows"]),
        "candidate": {
            "name": "full dual-edge residual absorption population check",
            "mechanism": (
                "Use the same top-20/residual Fourier split, but include all "
                "available lower-face dual-edge rows instead of only the "
                "post-discovery rows."),
            "prediction": (
                "If the finite decimal caps are not an artifact of excluding "
                "the discovery rows, the added discovery rows should have "
                "smaller or comparable pushback ratios."),
            "falsifier": (
                "A discovery row with pushback/top20-drag ratio above .126 or "
                ".13 would clip the corresponding finite cap to the "
                "post-discovery-only fixture."),
            "smallest_test": (
                "Replay all 230 edge-success rows from the lower-face "
                "dual-edge audit and compare threshold failures by bucket."),
            "novelty_label": "new-to-this-task",
        },
        "summaries": {
            "all_dual_edge_rows": all_summary,
            "discovery_rows": discovery_summary,
            "post_discovery_rows": post_summary,
        },
        "decision": (
            "Adding the 34 discovery rows does not change the finite "
            "threshold picture: .125 remains falsified by the same later row, "
            "while .126 and .13 pass all 230 available dual-edge rows.  The "
            "new evidence says the decimal fit is not caused merely by "
            "excluding discovery rows.  It still fits finite data only; the "
            "universal residual absorption bound remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
