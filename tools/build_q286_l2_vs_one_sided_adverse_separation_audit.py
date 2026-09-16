"""Compare symmetric aggregate L2 failures with one-sided adverse drag.

The raw-sum ledger leaves three possible proof shapes alive: direct witness,
raw adverse envelope, and aggregate raw L2.  This audit asks whether the
finite L2 cap failures are actually the same obstruction as the one-sided
adverse envelope, or whether symmetric L2 is rejecting rows that the adverse
gate handles comfortably.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
L2_OBSERVED = (
    Path("evidence")
    / "q286-wbss-multiplicative-character-l2-observed-moment-audit.json"
)
RAW_ADVERSE = Path("evidence/q286-wbss-raw-adverse-drag-theorem-target.json")
RAW_LEDGER = Path("evidence/q286-raw-sum-expansion-ledger.json")
OUT = Path("evidence/q286-l2-vs-one-sided-adverse-separation-audit.json")
NOTE = Path("notes/q286-l2-vs-one-sided-adverse-separation-audit.md")


def load(path: Path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def summary(values):
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": sum(values) / len(values),
    }


def pearson(xs, ys):
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    var_x = sum((x - mean_x) ** 2 for x in xs)
    var_y = sum((y - mean_y) ** 2 for y in ys)
    if var_x == 0 or var_y == 0:
        return None
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    return cov / math.sqrt(var_x * var_y)


def build_receipt():
    l2 = load(L2_OBSERVED)
    raw = load(RAW_ADVERSE)
    ledger = load(RAW_LEDGER)

    raw_by_target = {
        row["target"]: row for row in raw["finite_calibration"]["rows"]
    }
    joined = []
    for row in l2["rows"]:
        target = row["target"]
        raw_row = raw_by_target[target]
        joined.append({
            "target": target,
            "source": row["source"],
            "local_main": row["local_main"],
            "aggregate_character_moment_l2": (
                row["aggregate_character_moment_l2"]),
            "row_local_l2_cap": row["row_local_l2_cap"],
            "ratio_to_row_local_l2_cap": row["ratio_to_row_local_l2_cap"],
            "exceeds_row_local_l2_cap": row["exceeds_row_local_l2_cap"],
            "exceeds_global_min_l2_cap": row["exceeds_global_min_l2_cap"],
            "raw_adverse_drag_ratio": raw_row["raw_adverse_drag_ratio"],
            "raw_adverse_gate_gap": raw_row["raw_adverse_gate_gap"],
            "raw_gate_gap_positive": raw_row["raw_gate_gap_positive"],
            "raw_local_main": raw_row["raw_local_main"],
            "raw_adverse_drag": raw_row["raw_adverse_drag"],
        })

    row_l2_violations = [
        row for row in joined if row["exceeds_row_local_l2_cap"]
    ]
    global_l2_violations = [
        row for row in joined if row["exceeds_global_min_l2_cap"]
    ]
    all_l2_ratios = [row["ratio_to_row_local_l2_cap"] for row in joined]
    all_adverse_ratios = [row["raw_adverse_drag_ratio"] for row in joined]
    row_l2_violation_adverse_ratios = [
        row["raw_adverse_drag_ratio"] for row in row_l2_violations
    ]
    global_l2_violation_adverse_ratios = [
        row["raw_adverse_drag_ratio"] for row in global_l2_violations
    ]
    row_l2_violation_gaps = [
        row["raw_adverse_gate_gap"] for row in row_l2_violations
    ]
    worst_adverse_on_l2_violation = max(
        row_l2_violations,
        key=lambda row: (row["raw_adverse_drag_ratio"], row["target"]),
    )
    worst_l2_ratio_row = max(
        joined,
        key=lambda row: (row["ratio_to_row_local_l2_cap"], row["target"]),
    )

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q286_l2_vs_one_sided_adverse_separation",
        "source_receipts": {
            "l2_observed_moment_audit": str(L2_OBSERVED),
            "raw_adverse_drag_theorem_target": str(RAW_ADVERSE),
            "raw_sum_expansion_ledger": str(RAW_LEDGER),
        },
        "question": (
            "Are the finite aggregate L2 cap failures the same obstruction as "
            "the raw one-sided adverse envelope, or does symmetric L2 reject "
            "rows that the one-sided adverse gate handles?"),
        "candidate": {
            "name": "one-sided adverse route over symmetric aggregate L2",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The proof target only needs harmful projected mass to stay "
                "below local main.  Symmetric aggregate L2 charges helpful "
                "and harmful character moments alike, so it may be too strong "
                "as the immediate bridge."),
            "prediction": (
                "Many row-local aggregate L2 violations should still have "
                "positive raw adverse gates, with weak correlation between "
                "L2-ratio and adverse-drag ratio."),
            "falsifier": (
                "If L2 violations coincide with adverse-gate failures or "
                "near-failures, then abandoning L2 as the main bridge would "
                "discard the true obstruction."),
            "smallest_test": (
                "Join the 348-row observed L2 audit to the 348-row raw "
                "adverse target by target N and compare violation flags, "
                "adverse ratios, and raw gate gaps."),
        },
        "population": {
            "joined_row_count": len(joined),
            "row_local_l2_cap_violation_count": len(row_l2_violations),
            "global_min_l2_cap_violation_count": len(global_l2_violations),
            "raw_adverse_gate_failure_count": sum(
                not row["raw_gate_gap_positive"] for row in joined),
            "row_local_l2_violations_with_positive_adverse_gate": sum(
                row["raw_gate_gap_positive"] for row in row_l2_violations),
            "global_l2_violations_with_positive_adverse_gate": sum(
                row["raw_gate_gap_positive"] for row in global_l2_violations),
        },
        "separation_metrics": {
            "all_rows_raw_adverse_ratio": summary(all_adverse_ratios),
            "row_l2_violation_raw_adverse_ratio": summary(
                row_l2_violation_adverse_ratios),
            "global_l2_violation_raw_adverse_ratio": summary(
                global_l2_violation_adverse_ratios),
            "row_l2_violation_raw_gate_gap": summary(
                row_l2_violation_gaps),
            "pearson_row_l2_ratio_vs_raw_adverse_ratio": pearson(
                all_l2_ratios, all_adverse_ratios),
            "row_l2_violations_with_adverse_ratio_below_0_05": sum(
                row["raw_adverse_drag_ratio"] < 0.05
                for row in row_l2_violations),
            "row_l2_violations_with_adverse_ratio_below_0_10": sum(
                row["raw_adverse_drag_ratio"] < 0.10
                for row in row_l2_violations),
        },
        "extreme_rows": {
            "worst_adverse_ratio_among_row_l2_violations": (
                worst_adverse_on_l2_violation),
            "worst_row_local_l2_ratio": worst_l2_ratio_row,
        },
        "route_decision": {
            "symmetric_l2_is_too_strong_as_immediate_bridge": True,
            "why": (
                "All row-local L2-cap violations still have positive raw "
                "adverse gates, and most have small adverse ratios.  The "
                "finite obstruction to L2 is therefore not the finite "
                "obstruction to the one-sided adverse route."),
            "l2_retained_as": (
                "reservoir for future structured moment estimates, not the "
                "next acceptance bridge"),
            "preferred_next_theorem_shape": (
                "Prove a one-sided raw adverse projection bound, ideally "
                "per-modulus or componentwise, rather than a symmetric "
                "aggregate L2 bound over all active characters."),
            "required_universal_statement": ledger["acceptance_condition"][
                "required_universal_estimate"],
        },
        "decision": (
            "The checked rows separate the aggregate L2 obstruction from the "
            "one-sided adverse envelope.  The row-local L2 cap fails on 120 "
            "rows, but every one of those rows still has positive raw adverse "
            "gate gap; 77 of the 120 have adverse ratio below 0.05, and the "
            "Pearson correlation between row-local L2 ratio and adverse ratio "
            "is weak.  This demotes symmetric aggregate L2 as the immediate "
            "bridge and promotes one-sided raw adverse projection control as "
            "the sharper theorem target."),
        "finite_separation_audit_only": True,
        "aggregate_l2_theorem_proved": False,
        "one_sided_adverse_projection_theorem_proved": False,
        "raw_adverse_envelope_theorem_proved": False,
        "raw_witness_theorem_proved": False,
        "universal_raw_pointwise_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    pop = receipt["population"]
    sep = receipt["separation_metrics"]
    worst = receipt["extreme_rows"][
        "worst_adverse_ratio_among_row_l2_violations"]
    lines = [
        "# q286 L2 versus one-sided adverse separation audit",
        "",
        "## Question",
        "",
        receipt["question"],
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_q286_l2_vs_one_sided_adverse_separation_audit.py",
        "evidence/q286-l2-vs-one-sided-adverse-separation-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"joined rows:                              {pop['joined_row_count']}",
        f"row-local L2 cap violations:              {pop['row_local_l2_cap_violation_count']}",
        f"global-minimum L2 cap violations:         {pop['global_min_l2_cap_violation_count']}",
        f"raw adverse gate failures:                {pop['raw_adverse_gate_failure_count']}",
        f"row-local L2 violations with positive gate:{pop['row_local_l2_violations_with_positive_adverse_gate']}",
        f"max adverse ratio on L2 violations:       {sep['row_l2_violation_raw_adverse_ratio']['maximum']}",
        f"min raw gate gap on L2 violations:        {sep['row_l2_violation_raw_gate_gap']['minimum']}",
        f"L2/adverse Pearson:                       {sep['pearson_row_l2_ratio_vs_raw_adverse_ratio']}",
        f"L2 violations with adverse ratio < .05:   {sep['row_l2_violations_with_adverse_ratio_below_0_05']}",
        f"L2 violations with adverse ratio < .10:   {sep['row_l2_violations_with_adverse_ratio_below_0_10']}",
        "```",
        "",
        "The worst adverse ratio among row-local L2 violations is at target",
        f"`{worst['target']}`: adverse ratio `{worst['raw_adverse_drag_ratio']}`,",
        f"row-local L2 ratio `{worst['ratio_to_row_local_l2_cap']}`, and raw",
        f"gate gap `{worst['raw_adverse_gate_gap']}`.",
        "",
        "## Interpretation",
        "",
        "The finite L2 cap failures are not the same finite obstruction as the",
        "one-sided adverse envelope.  Symmetric L2 charges all character moment",
        "mass, including helpful directions.  The adverse envelope only charges",
        "harmful projected mass.  On the checked rows, the latter is much less",
        "stressed.",
        "",
        "## Decision",
        "",
        receipt["decision"],
        "",
        "This is finite separation evidence only.  It proves no aggregate L2",
        "theorem, one-sided adverse projection theorem, raw adverse-envelope",
        "theorem, strict-central Goldbach theorem, or Goldbach proof.",
        "",
    ]
    NOTE.write_text("\n".join(lines), encoding="utf-8")


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    write_note(receipt)
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "row_local_l2_cap_violation_count": receipt["population"][
            "row_local_l2_cap_violation_count"],
        "raw_adverse_gate_failure_count": receipt["population"][
            "raw_adverse_gate_failure_count"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
