"""Build a theorem-obligation audit for source-start prime-block control.

This does not add another scale.  It turns the six-scale finite morphology into
the exact pointwise inequalities a proof would need to replace finite
acceptance: full contribution negative, and the unnormalized half-frame margin
``full/2 - active`` positive for every source-start prime block row.
"""

from __future__ import annotations

import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
MORPHOLOGY = (
    EVIDENCE
    / "mobius-moment-square-degree5-source-start-stress-morphology-audit.json")
OUT = (
    EVIDENCE
    / "mobius-moment-square-degree5-prime-block-theorem-obligation-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def receipt_path(scale):
    return (
        EVIDENCE
        / f"mobius-moment-square-degree5-source-start-m{scale}"
          "-full-prime-sweep.json")


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def iter_rows(receipt):
    for prime_row in receipt["scale_result"]["prime_rows"]:
        prime = prime_row["prime_modulus"]
        for row in prime_row["component_rows"] + [prime_row["degree5_total_row"]]:
            record = dict(row)
            record["prime_modulus"] = prime
            record["unnormalized_half_frame_margin"] = (
                -record["half_frame_contribution"])
            yield record


def block_records(scale, rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["prime_modulus"]].append(row)
    blocks = []
    for prime, block_rows in grouped.items():
        sorted_rows = sorted(
            block_rows, key=lambda row: row["dominance_slack_above_one_half"])
        slacks = [row["dominance_slack_above_one_half"] for row in block_rows]
        margins = [row["unnormalized_half_frame_margin"] for row in block_rows]
        blocks.append({
            "scale_modulus": scale,
            "prime_modulus": prime,
            "minimum_slack": min(slacks),
            "maximum_slack": max(slacks),
            "slack_spread": max(slacks) - min(slacks),
            "minimum_unnormalized_half_frame_margin": min(margins),
            "weakest_label": sorted_rows[0]["label"],
            "labels_by_slack": [row["label"] for row in sorted_rows],
        })
    return sorted(blocks, key=lambda block: block["minimum_slack"])


def scale_obligation_record(summary):
    scale = summary["scale_modulus"]
    receipt = load_json(receipt_path(scale))
    rows = list(iter_rows(receipt))
    blocks = block_records(scale, rows)
    top = blocks[0]
    second = blocks[1]
    block_gap = second["minimum_slack"] - top["minimum_slack"]
    gap_to_spread_factor = (
        block_gap / top["slack_spread"] if top["slack_spread"] else None)
    full_sign_failures = [
        row for row in rows if not row["full_contribution_negative"]]
    margin_failures = [
        row for row in rows if row["unnormalized_half_frame_margin"] <= 0]
    return {
        "scale_modulus": scale,
        "source_receipt": str(receipt_path(scale).relative_to(ROOT)),
        "prime_row_count": receipt["prime_row_count"],
        "dominance_row_count": len(rows),
        "top_prime_block": top,
        "second_prime_block": second,
        "top_to_second_block_slack_gap": block_gap,
        "top_block_slack_spread": top["slack_spread"],
        "top_gap_to_internal_spread_factor": gap_to_spread_factor,
        "all_rows_have_negative_full_contribution": not full_sign_failures,
        "all_rows_have_positive_unnormalized_half_frame_margin": (
            not margin_failures),
        "minimum_unnormalized_half_frame_margin": min(
            row["unnormalized_half_frame_margin"] for row in rows),
        "minimum_dominance_slack_above_one_half": min(
            row["dominance_slack_above_one_half"] for row in rows),
        "full_sign_failure_count": len(full_sign_failures),
        "unnormalized_margin_failure_count": len(margin_failures),
    }


def build_receipt():
    morphology = load_json(MORPHOLOGY)
    scale_records = [
        scale_obligation_record(summary)
        for summary in morphology["scale_summaries"]
    ]
    block_gaps = [
        row["top_to_second_block_slack_gap"] for row in scale_records]
    top_spreads = [row["top_block_slack_spread"] for row in scale_records]
    margins = [
        row["minimum_unnormalized_half_frame_margin"]
        for row in scale_records
    ]
    tightest_primes = [
        row["top_prime_block"]["prime_modulus"] for row in scale_records]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_degree5_prime_block_theorem_obligation",
        "source_morphology_audit": str(MORPHOLOGY.relative_to(ROOT)),
        "question": (
            "What universal pointwise theorem would replace the six-scale "
            "finite source-start prime-block morphology evidence?"),
        "scales": morphology["scales"],
        "scale_count": len(scale_records),
        "checked_dominance_row_count": sum(
            row["dominance_row_count"] for row in scale_records),
        "scale_obligation_records": scale_records,
        "all_checked_rows_have_negative_full_contribution": all(
            row["all_rows_have_negative_full_contribution"]
            for row in scale_records),
        "all_checked_rows_have_positive_unnormalized_half_frame_margin": all(
            row["all_rows_have_positive_unnormalized_half_frame_margin"]
            for row in scale_records),
        "minimum_checked_dominance_slack_above_one_half": min(
            row["minimum_dominance_slack_above_one_half"]
            for row in scale_records),
        "minimum_checked_unnormalized_half_frame_margin": min(margins),
        "minimum_top_to_second_block_slack_gap": min(block_gaps),
        "minimum_top_gap_to_internal_spread_factor": min(
            row["top_gap_to_internal_spread_factor"]
            for row in scale_records
            if row["top_gap_to_internal_spread_factor"] is not None),
        "maximum_top_block_slack_spread": max(top_spreads),
        "tightest_prime_counts": dict(Counter(tightest_primes)),
        "pointwise_unnormalized_theorem_target": {
            "name": "source-start prime-block lower-frame control",
            "statement_shape": (
                "For every sufficiently large source scale M and every prime "
                "p in [M,2M], every tracked component row and the degree-5 "
                "TOTAL row should satisfy full(M,p,label)<0 and "
                "full/2 - active > 0, i.e. "
                "full(M,p,label)/2 - active(M,p,label) > 0, at the "
                "canonical source start.  A stronger usable version needs a "
                "positive lower envelope for the minimum block margin over p."),
            "why_unnormalized": (
                "Because full<0, the normalized check active/full>1/2 is "
                "equivalent to the pointwise unnormalized inequality "
                "full/2 - active > 0."),
            "current_finite_floor": (
                "The checked floor is the minimum of full/2-active across "
                "the six complete source-start sweeps; it is not a universal "
                "constant."),
        },
        "proof_obligations": [
            {
                "id": "source_start.full_negative",
                "needed": (
                    "Prove full(M,p,label)<0 uniformly for all relevant "
                    "source-start rows."),
                "finite_status": "passes on checked six-scale fixture",
                "theorem_status": "open",
            },
            {
                "id": "source_start.unnormalized_half_frame_margin",
                "needed": (
                    "Prove full(M,p,label)/2-active(M,p,label)>0 uniformly, "
                    "or prove a stronger explicit lower envelope by prime "
                    "block."),
                "finite_status": "passes on checked six-scale fixture",
                "theorem_status": "open",
            },
            {
                "id": "prime_block.lower_envelope",
                "needed": (
                    "Control the minimum over labels inside each prime block, "
                    "then the minimum over primes p in [M,2M]."),
                "finite_status": (
                    "top blocks are coherent; the smallest top-to-second "
                    "slack gap is narrow enough that exact winner claims "
                    "should remain diagnostic only."),
                "theorem_status": "open",
            },
        ],
        "decision": (
            "The next mathematical target is not another raw finite acceptance "
            "threshold.  It is a pointwise unnormalized inequality: "
            "full/2-active>0, with full<0, first by prime block and then over "
            "all primes in the source-start interval.  The persistent p=599 "
            "winner is only a diagnostic because the checked block-separation "
            "gap can be small."),
        "finite_obligation_audit_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_start_theorem_proved": False,
        "prime_block_theorem_proved": False,
        "source_window_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
    }


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
