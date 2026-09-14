"""Build a compact q286 filter-order audit evidence file.

This freezes the current "which filter comes first?" diagnostic without
storing the full 40k-row receipt.  The output is finite evidence only.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-filter-order-audit.json"
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_filter_order_audit_receipt,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def targets_with(receipt, predicate):
    return {
        target for target, row in receipt["target_rows"].items()
        if predicate in row["passed_predicates"]
    }


def compact_order(row):
    return {
        "order": row["order"],
        "predicates": row["predicates"],
        "final_survivor_count": row["final_survivor_count"],
        "first_final_survivor_targets": row["final_survivor_targets"][:20],
        "stage_counts": tuple({
            "predicate": stage["predicate"],
            "input_count": stage["input_count"],
            "survivor_count": stage["survivor_count"],
            "rejected_count": stage["rejected_count"],
            "survivor_fraction_of_input": (
                stage["survivor_fraction_of_input"]),
            "survivor_fraction_of_total": (
                stage["survivor_fraction_of_total"]),
        } for stage in row["stages"]),
    }


def main():
    receipt = q286_first_three_filter_order_audit_receipt(
        cycle_count=8, targets_per_cycle=5005,
        tail_threshold=.3, complement_floor=.3)
    first_three = targets_with(receipt, "first_three_tail")
    first_two = targets_with(receipt, "first_two_active")
    full_nonpositive = targets_with(receipt, "full_nonpositive")
    complement_floor = targets_with(receipt, "complement_floor")
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite q286 filter-order audit only; no eventual theorem, "
            "signed prime-correlation estimate, or Goldbach proof"),
        "parameters": {
            "start": receipt["start"],
            "cycle_count": receipt["cycle_count"],
            "targets_per_cycle": receipt["targets_per_cycle"],
            "tested_target_count": receipt["tested_target_count"],
            "first_two_threshold": receipt["first_two_threshold"],
            "tail_threshold": receipt["tail_threshold"],
            "complement_floor": receipt["complement_floor"],
        },
        "predicate_counts": receipt["predicate_counts"],
        "selectivity_rank": receipt["selectivity_rank"],
        "ordered_filter_rows": tuple(
            compact_order(row) for row in receipt["ordered_filter_rows"]),
        "difference_targets": {
            "first_three_tail_not_first_two_active": tuple(
                sorted(first_three - first_two)),
            "first_two_active_not_first_three_tail_count": (
                len(first_two - first_three)),
            "first_two_active_not_first_three_tail_first20": tuple(
                sorted(first_two - first_three)[:20]),
            "full_nonpositive_not_first_three_tail": tuple(
                sorted(full_nonpositive - first_three)),
            "first_three_tail_below_complement_floor": tuple(
                sorted(first_three - complement_floor)),
        },
        "interpretation": {
            "first_three_vs_active_selector": (
                "On this eight-period fixture, first_three_tail has one "
                "more target than active_selector, so the first_two filter "
                "is almost redundant after the first-three tail filter."),
            "full_nonpositive_vs_first_three": (
                "Only three full-nonpositive targets are outside the "
                "first-three tail; the nonrescued minority is essentially "
                "the hard residual inside the first-three tail on this "
                "finite fixture."),
            "complement_floor_vs_first_three": (
                "The complement .3 floor is very coarse globally but removes "
                "only eleven first-three tail targets on this fixture, so it "
                "is not the first sorting cloth for the tail problem."),
        },
        "filter_order_audit_measured": True,
        "filter_order_theorem_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
