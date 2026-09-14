"""Build a q286 filter-order holdout comparison evidence file.

The baseline eight-period audit is stored in
``evidence/q286-filter-order-audit.json``.  This script applies the unchanged
filter-order receipt to the next contiguous eight q286 periods and stores a
compact comparison.  It is finite evidence only.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
BASELINE_PATH = EVIDENCE / "q286-filter-order-audit.json"
OUT = EVIDENCE / "q286-filter-order-holdout-8-15.json"
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


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def targets_with(receipt, predicate):
    return {
        target for target, row in receipt["target_rows"].items()
        if predicate in row["passed_predicates"]
    }


def compact_receipt(receipt):
    first_three = targets_with(receipt, "first_three_tail")
    first_two = targets_with(receipt, "first_two_active")
    full_nonpositive = targets_with(receipt, "full_nonpositive")
    complement_floor = targets_with(receipt, "complement_floor")
    return {
        "start": receipt["start"],
        "cycle_count": receipt["cycle_count"],
        "targets_per_cycle": receipt["targets_per_cycle"],
        "tested_target_count": receipt["tested_target_count"],
        "predicate_counts": receipt["predicate_counts"],
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
    }


def compact_baseline(payload):
    return {
        "start": payload["parameters"]["start"],
        "cycle_count": payload["parameters"]["cycle_count"],
        "targets_per_cycle": payload["parameters"]["targets_per_cycle"],
        "tested_target_count": payload["parameters"]["tested_target_count"],
        "predicate_counts": payload["predicate_counts"],
        "difference_targets": payload["difference_targets"],
    }


def main():
    baseline = load_json(BASELINE_PATH)
    holdout = q286_first_three_filter_order_audit_receipt(
        start=90080, cycle_count=8, targets_per_cycle=5005,
        tail_threshold=.3, complement_floor=.3)
    baseline_compact = compact_baseline(baseline)
    holdout_compact = compact_receipt(holdout)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite q286 filter-order holdout comparison only; no eventual "
            "rarity theorem, signed prime-correlation estimate, or Goldbach "
            "proof"),
        "baseline_window": baseline_compact,
        "holdout_window": holdout_compact,
        "comparison": {
            "first_three_tail_equals_active_selector_in_holdout": bool(
                holdout["predicate_counts"]["first_three_tail"]
                == holdout["predicate_counts"]["active_selector"]),
            "holdout_first_three_tail_not_first_two_active_count": len(
                holdout_compact["difference_targets"][
                    "first_three_tail_not_first_two_active"]),
            "holdout_full_nonpositive_count": (
                holdout["predicate_counts"]["full_nonpositive"]),
            "holdout_nonrescued_first_three_tail_count": (
                holdout["predicate_counts"][
                    "nonrescued_first_three_tail"]),
            "baseline_first_three_tail_not_first_two_active_count": len(
                baseline_compact["difference_targets"][
                    "first_three_tail_not_first_two_active"]),
            "baseline_full_nonpositive_count": (
                baseline_compact["predicate_counts"]["full_nonpositive"]),
            "baseline_nonrescued_first_three_tail_count": (
                baseline_compact["predicate_counts"][
                    "nonrescued_first_three_tail"]),
        },
        "interpretation": {
            "changed_under_evidence": (
                "The next contiguous eight-period holdout strengthens the "
                "finite navigation claim that first_three_tail is the coarse "
                "separator for the active selector: in the holdout it exactly "
                "equals active_selector, and no full-nonpositive targets "
                "occur."),
            "boundary": (
                "This is finite holdout evidence only.  It does not prove "
                "eventual first-three rarity, complement floor, strict "
                "closure, prime-correlation control, or Goldbach."),
        },
        "filter_order_holdout_measured": True,
        "filter_order_theorem_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
