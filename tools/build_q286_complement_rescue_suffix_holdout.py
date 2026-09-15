"""Test the frozen q286 complement-rescue suffix on sampled holdout windows.

The preceding threshold-candidate audit selected the smallest finite suffix
``block_index_after_discovery >= 1`` from blocks 0..5.  This receipt freezes
that candidate and tests new q286 block-start windows beyond the last checked
start 410400.

Finite holdout evidence only: this is not a threshold theorem, signed
correlation theorem, pointwise character-sum theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
THRESHOLD_SOURCE = (
    EVIDENCE / "q286-complement-rescue-threshold-candidate-audit.json")
SCHEDULE_SOURCE = EVIDENCE / "q286-complement-rescue-margin-schedule.json"
OUT = EVIDENCE / "q286-complement-rescue-suffix-holdout.json"

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_two_mode_lower_tail_receipt,
    q286_first_three_filter_order_audit_receipt,
)
from tools.build_q286_complement_rescue_margin_schedule import (  # noqa: E402
    aggregate_schedule,
    block_start,
    block_summary,
    row_metrics,
    summarize_rows,
)
from tools.build_q286_mod13_4_prospective_descriptor_audit import (  # noqa: E402
    COMPLEMENT_FLOOR,
    DISCOVERY_CYCLES,
    TAIL_THRESHOLD,
    TARGETS_PER_CYCLE,
)


FROZEN_HOLDOUT_BLOCK_INDICES = (6, 7, 8, 9, 10, 11)
HOLDOUT_CYCLE_COUNT = 1
HOLDOUT_TARGETS_PER_CYCLE = 101
OFFSET_REPLAY_LIMIT = 12
TOLERANCE = 1e-9


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def run_block(period, block_index):
    start = block_start(period, block_index)
    receipt = q286_first_three_filter_order_audit_receipt(
        start=start,
        cycle_count=HOLDOUT_CYCLE_COUNT,
        targets_per_cycle=HOLDOUT_TARGETS_PER_CYCLE,
        tail_threshold=TAIL_THRESHOLD,
        complement_floor=COMPLEMENT_FLOOR)
    tail_targets = [
        int(target) for target, row in receipt["target_rows"].items()
        if "first_three_tail" in row["passed_predicates"]
    ]
    tail_rows = [
        row_metrics(target, receipt["target_rows"][target],
                    block_index, start)
        for target in sorted(tail_targets)
    ]
    return {
        "block_index_after_discovery": int(block_index),
        "start": int(start),
        "tail_rows": tail_rows,
        "summary": block_summary(block_index, start, receipt, tail_rows),
    }


def candidate_status(aggregate):
    tail = aggregate["first_three_tail"]
    active = aggregate["active_selector"]
    if tail["row_count"] == 0:
        return "untested_no_tail_support"
    if tail["failure_count"] or active["failure_count"]:
        return "falsified_on_holdout"
    return "passed_finite_holdout_not_theorem"


def selected_row_metrics(target, row, meta):
    first_two = float(row["first_two_modes_to_principal_ratio"])
    first_three = float(row["first_three_modes_to_principal_ratio"])
    complement = float(row["full_without_first_three_to_principal_ratio"])
    full = float(row["full_action_to_principal_ratio"])
    predicates = {
        "first_two_active": first_two < -0.2,
        "first_three_tail": first_three < -TAIL_THRESHOLD,
        "complement_positive": complement > TOLERANCE,
        "complement_floor": complement > COMPLEMENT_FLOOR,
        "full_positive": full > TOLERANCE,
        "full_nonpositive": full <= TOLERANCE,
    }
    required = max(0.0, -first_three)
    return {
        "target": int(target),
        "block_index_after_discovery": int(meta["block_index"]),
        "block_start": int(meta["block_start"]),
        "cycle": int(meta["offset"] // meta["period"]),
        "offset_from_block_start": int(meta["offset"]),
        "source_offset_target": int(meta["source_target"]),
        "source_offset_block_start": int(meta["source_block_start"]),
        "source_offset_cycle": int(meta["source_cycle"]),
        "target_mod_13": int(target) % 13,
        "target_mod_143": int(target) % 143,
        "target_mod_286": int(target) % 286,
        "first_two_modes_to_principal_ratio": first_two,
        "first_three_modes_to_principal_ratio": first_three,
        "complement_to_principal_ratio": complement,
        "full_action_to_principal_ratio": full,
        "required_complement_to_cancel_first_three": required,
        "complement_surplus_to_cancel_first_three": complement - required,
        "complement_to_required_ratio": (
            complement / required if required > TOLERANCE else float("inf")),
        "tail_depth_below_threshold": max(
            0.0, -TAIL_THRESHOLD - first_three),
        "rescue_margin_to_zero": full,
        "identity_error": abs((first_three + complement) - full),
        "first_two_active": predicates["first_two_active"],
        "first_three_tail": predicates["first_three_tail"],
        "complement_floor": predicates["complement_floor"],
        "full_positive": predicates["full_positive"],
        "full_nonpositive": predicates["full_nonpositive"],
        "passed_predicates": tuple(
            name for name, passed in predicates.items() if passed),
    }


def prior_tail_offsets(schedule):
    source_rows = (
        schedule["post_discovery_blocks"]["first_three_tail"][
            "tightest_rescue_rows"]
        + schedule["post_discovery_blocks"]["first_three_tail"][
            "deepest_tail_rows"])
    offsets = []
    seen = set()
    for row in source_rows:
        offset = int(row["target"]) - int(row["block_start"])
        if offset in seen:
            continue
        seen.add(offset)
        offsets.append({
            "offset": offset,
            "source_target": int(row["target"]),
            "source_block_start": int(row["block_start"]),
            "source_cycle": int(row["cycle"]),
            "source_first_three": float(
                row["first_three_modes_to_principal_ratio"]),
            "source_rescue_margin": float(row["rescue_margin_to_zero"]),
        })
        if len(offsets) >= OFFSET_REPLAY_LIMIT:
            break
    return offsets


def run_offset_replay(period, block_indices, holdout_starts, offsets):
    target_meta = {}
    for block_index, start in zip(block_indices, holdout_starts):
        for source in offsets:
            target = int(start) + int(source["offset"])
            target_meta[target] = {
                **source,
                "block_index": int(block_index),
                "block_start": int(start),
                "period": int(period),
            }
    receipt = q286_first_two_mode_lower_tail_receipt(
        selected_targets=tuple(sorted(target_meta)),
        tolerance=TOLERANCE,
        include_residue_weights=False)
    rows = [
        selected_row_metrics(target, receipt["rows"][target],
                             target_meta[target])
        for target in sorted(target_meta)
    ]
    tail_rows = [row for row in rows if row["first_three_tail"]]
    active_rows = [row for row in tail_rows if row["first_two_active"]]
    return {
        "source_offsets": offsets,
        "tested_target_count": len(rows),
        "all_rows": summarize_rows("all_offset_replay_rows", rows),
        "first_three_tail": summarize_rows(
            "offset_replay_first_three_tail", tail_rows),
        "active_selector": summarize_rows(
            "offset_replay_active_selector", active_rows),
        "predicate_full_nonpositive_count": sum(
            1 for row in rows if row["full_nonpositive"]),
        "target_rows": rows,
    }


def main():
    threshold = load_json(THRESHOLD_SOURCE)
    schedule = load_json(SCHEDULE_SOURCE)
    frozen_threshold = int(
        threshold["decision_metrics"]["smallest_supported_suffix_threshold"])
    period = int(schedule["schedule"]["arithmetic_period"])
    prior_starts = tuple(int(value) for value in schedule["schedule"]["starts"])
    last_prior_start = max(prior_starts)
    holdout_starts = tuple(
        block_start(period, index) for index in FROZEN_HOLDOUT_BLOCK_INDICES)
    assert min(holdout_starts) > last_prior_start

    blocks = [
        run_block(period, block_index)
        for block_index in FROZEN_HOLDOUT_BLOCK_INDICES
    ]
    holdout = aggregate_schedule(blocks, lambda block: True)
    offset_replay = run_offset_replay(
        period,
        FROZEN_HOLDOUT_BLOCK_INDICES,
        holdout_starts,
        prior_tail_offsets(schedule))
    tail = holdout["first_three_tail"]
    active = holdout["active_selector"]
    start_window_status = candidate_status(holdout)
    offset_status = candidate_status({
        "first_three_tail": offset_replay["first_three_tail"],
        "active_selector": offset_replay["active_selector"],
    })
    tightest_row = (
        tail["tightest_rescue_rows"][0] if tail["tightest_rescue_rows"]
        else None)
    deepest_row = (
        tail["deepest_tail_rows"][0] if tail["deepest_tail_rows"]
        else None)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "threshold_candidate": str(THRESHOLD_SOURCE.relative_to(ROOT)),
            "margin_schedule": str(SCHEDULE_SOURCE.relative_to(ROOT)),
            "filter_order_receipt":
                "q286_first_three_filter_order_audit_receipt",
        },
        "status_boundary": (
            "finite frozen-suffix sampled holdout only; no full-block "
            "verification, eventual threshold theorem, signed correlation "
            "theorem, pointwise character-sum theorem, or Goldbach proof."),
        "question": (
            "Does the frozen block_index_after_discovery >= 1 "
            "complement-rescue candidate survive sampled q286 block-start "
            "windows and prior-tail offset replays beyond the schedule that "
            "selected it?"),
        "mechanism": (
            "Keep the suffix threshold fixed from the prior audit, then test "
            "new later q286 block-start windows and prior tail offsets "
            "selected from the old schedule before seeing new rows.  The "
            "candidate passes a supported finite sampled holdout only if the "
            "offset replay has tail support and every first-three-tail and "
            "active-selector row has positive full_action_to_principal_ratio."),
        "prediction": (
            "If the post-discovery closure is a generalizing finite phase "
            "rather than a selected-window accident, later sampled holdout "
            "tail rows and replayed prior-tail offsets should continue to be "
            "rescued by the complement."),
        "falsifier": (
            "Any sampled holdout or prior-offset first-three-tail/"
            "active-selector row with full_action_to_principal_ratio <= 0 "
            "falsifies the frozen suffix candidate on that finite sample. "
            "Full-block falsification still requires full-block or "
            "optimized-convolution verification."),
        "frozen_candidate": {
            "condition": (
                f"block_index_after_discovery >= {frozen_threshold}"),
            "selected_from_blocks": schedule["schedule"]["block_indices"],
            "selected_from_starts": list(prior_starts),
            "last_selected_start": last_prior_start,
            "source_decision_status": (
                threshold["candidate_decisions"][1]["status"]),
        },
        "holdout_schedule": {
            "arithmetic_period": period,
            "block_indices": list(FROZEN_HOLDOUT_BLOCK_INDICES),
            "starts": list(holdout_starts),
            "cycle_count_per_block_start_window": HOLDOUT_CYCLE_COUNT,
            "targets_per_cycle": HOLDOUT_TARGETS_PER_CYCLE,
            "tested_target_count": sum(
                int(block["summary"]["tested_target_count"])
                for block in blocks),
        },
        "block_summaries": [block["summary"] for block in blocks],
        "block_start_window_holdout": holdout,
        "prior_tail_offset_replay_holdout": offset_replay,
        "decision_metrics": {
            "frozen_suffix_threshold": frozen_threshold,
            "block_start_window_candidate_status": start_window_status,
            "block_start_window_has_tail_support": tail["row_count"] > 0,
            "block_start_window_first_three_tail_count": tail["row_count"],
            "block_start_window_active_selector_count": active["row_count"],
            "block_start_window_first_three_tail_failure_count": (
                tail["failure_count"]),
            "block_start_window_active_selector_failure_count": (
                active["failure_count"]),
            "block_start_window_predicate_full_nonpositive_count": (
                holdout["predicate_full_nonpositive_count"]),
            "block_start_window_minimum_rescue_margin": (
                tail["rescue_margin_to_zero_summary"]["minimum"]),
            "block_start_window_minimum_complement_to_required_ratio": (
                tail["complement_to_required_ratio_summary"]["minimum"]),
            "block_start_window_maximum_identity_error": max(
                block["summary"]["first_three_tail"]["max_identity_error"]
                for block in blocks),
            "block_start_window_tightest_target": (
                tightest_row["target"] if tightest_row else None),
            "block_start_window_deepest_tail_target": (
                deepest_row["target"] if deepest_row else None),
            "offset_replay_candidate_status": offset_status,
            "offset_replay_source_offset_count": (
                len(offset_replay["source_offsets"])),
            "offset_replay_tested_target_count": (
                offset_replay["tested_target_count"]),
            "offset_replay_has_tail_support": (
                offset_replay["first_three_tail"]["row_count"] > 0),
            "offset_replay_first_three_tail_count": (
                offset_replay["first_three_tail"]["row_count"]),
            "offset_replay_active_selector_count": (
                offset_replay["active_selector"]["row_count"]),
            "offset_replay_first_three_tail_failure_count": (
                offset_replay["first_three_tail"]["failure_count"]),
            "offset_replay_active_selector_failure_count": (
                offset_replay["active_selector"]["failure_count"]),
            "offset_replay_predicate_full_nonpositive_count": (
                offset_replay["predicate_full_nonpositive_count"]),
            "offset_replay_minimum_rescue_margin": (
                offset_replay["first_three_tail"][
                    "rescue_margin_to_zero_summary"]["minimum"]),
            "offset_replay_minimum_complement_to_required_ratio": (
                offset_replay["first_three_tail"][
                    "complement_to_required_ratio_summary"]["minimum"]),
            "offset_replay_tightest_target": (
                offset_replay["first_three_tail"][
                    "tightest_rescue_rows"][0]["target"]
                if offset_replay["first_three_tail"][
                    "tightest_rescue_rows"] else None),
            "goldbach_proved": False,
        },
        "decision": (
            "The first-101 block-start windows can be support-starved.  The "
            "prior-tail offset replay is the supported sampled falsifier lane: "
            "if offset_replay_candidate_status is "
            "passed_finite_holdout_not_theorem, the frozen suffix survives a "
            "stronger finite sample, but still not a theorem."),
        "next_obligation": (
            "Turn the persistent post-discovery rescue into an explicit "
            "condition on q286 residue measures or prime-pair correlations, "
            "and build an optimized full-block verifier before treating these "
            "later starts as exhaustively checked."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
