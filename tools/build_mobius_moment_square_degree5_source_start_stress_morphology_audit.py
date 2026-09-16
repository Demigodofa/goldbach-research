"""Summarize stress morphology across complete source-start sweeps.

The full M=331 sweep survived but moved the weakest row from the sentinel
prime p=461 to p=599.  This derived audit reads the complete fresh-scale
source-start sweeps and asks what should guide the next finite or theorem
target: fixed attention primes, endpoint position, component labels, or
prime-level stress blocks.
"""

from __future__ import annotations

import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = (
    EVIDENCE
    / "mobius-moment-square-degree5-source-start-stress-morphology-audit.json")
SCALES = (229, 251, 293, 331)
TOP_ROW_COUNT = 12
TOP_BLOCK_COUNT = 4


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


def load_receipt(scale):
    return json.loads(receipt_path(scale).read_text(encoding="utf-8"))


def row_records(receipt):
    rows = []
    for prime_row in receipt["scale_result"]["prime_rows"]:
        prime = prime_row["prime_modulus"]
        for row in prime_row["component_rows"] + [prime_row["degree5_total_row"]]:
            record = dict(row)
            record["prime_modulus"] = prime
            rows.append(record)
    return rows


def prime_blocks(scale, rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["prime_modulus"]].append(row)
    blocks = []
    for prime, prime_rows in grouped.items():
        slacks = [row["dominance_slack_above_one_half"] for row in prime_rows]
        ratios = [row["active_over_full_ratio"] for row in prime_rows]
        weakest = min(
            prime_rows,
            key=lambda row: row["dominance_slack_above_one_half"])
        blocks.append({
            "scale_modulus": scale,
            "prime_modulus": prime,
            "prime_over_scale": prime / scale,
            "tail_fraction": (2 * scale - prime) / scale,
            "minimum_slack": min(slacks),
            "maximum_slack": max(slacks),
            "slack_spread": max(slacks) - min(slacks),
            "minimum_ratio": min(ratios),
            "weakest_label": weakest["label"],
            "labels_by_slack": [
                row["label"]
                for row in sorted(
                    prime_rows,
                    key=lambda item: item["dominance_slack_above_one_half"])
            ],
        })
    return sorted(blocks, key=lambda block: block["minimum_slack"])


def scale_summary(scale):
    receipt = load_receipt(scale)
    rows = row_records(receipt)
    sorted_rows = sorted(
        rows, key=lambda row: row["dominance_slack_above_one_half"])
    blocks = prime_blocks(scale, rows)
    top_rows = sorted_rows[:TOP_ROW_COUNT]
    top_primes = [row["prime_modulus"] for row in top_rows]
    return {
        "scale_modulus": scale,
        "source_receipt": str(receipt_path(scale).relative_to(ROOT)),
        "source_status": receipt["status"],
        "prime_interval": receipt["prime_interval"],
        "prime_row_count": receipt["prime_row_count"],
        "dominance_row_count": receipt["dominance_row_count"],
        "all_rows_dominate_one_half_signed_full": (
            receipt["all_rows_dominate_one_half_signed_full"]),
        "weakest_row": receipt["weakest_dominance_row"],
        "weakest_prime_modulus": receipt[
            "weakest_dominance_row"]["prime_modulus"],
        "weakest_prime_over_scale": (
            receipt["weakest_dominance_row"]["prime_modulus"] / scale),
        "weakest_tail_fraction": (
            (2 * scale - receipt["weakest_dominance_row"]["prime_modulus"])
            / scale),
        "minimum_slack": receipt["minimum_dominance_slack_above_one_half"],
        "top_rows": [
            {
                "prime_modulus": row["prime_modulus"],
                "label": row["label"],
                "active_over_full_ratio": row["active_over_full_ratio"],
                "dominance_slack_above_one_half": (
                    row["dominance_slack_above_one_half"]),
                "prime_over_scale": row["prime_modulus"] / scale,
                "tail_fraction": (2 * scale - row["prime_modulus"]) / scale,
            }
            for row in top_rows
        ],
        "top_row_prime_counts": dict(Counter(top_primes)),
        "tightest_prime_blocks": blocks[:TOP_BLOCK_COUNT],
        "tightest_prime_block_is_row_coherent": (
            len({row["prime_modulus"] for row in top_rows[:4]}) == 1
            and set(blocks[0]["labels_by_slack"])
            == {"00,12", "01,02", "01,11", "TOTAL"}),
    }


def build_receipt():
    summaries = [scale_summary(scale) for scale in SCALES]
    weakest_sequence = [
        {
            "scale_modulus": item["scale_modulus"],
            "weakest_prime_modulus": item["weakest_prime_modulus"],
            "weakest_prime_over_scale": item["weakest_prime_over_scale"],
            "weakest_tail_fraction": item["weakest_tail_fraction"],
            "weakest_label": item["weakest_row"]["label"],
            "minimum_slack": item["minimum_slack"],
        }
        for item in summaries
    ]
    weakest_labels = [
        item["weakest_row"]["label"] for item in summaries]
    row_coherent = all(
        item["tightest_prime_block_is_row_coherent"] for item in summaries)
    all_pass = all(
        item["all_rows_dominate_one_half_signed_full"] for item in summaries)
    weakest_primes = [
        item["weakest_prime_modulus"] for item in summaries]
    fixed_prime_counter = Counter(weakest_primes)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_degree5_source_start_stress_morphology",
        "question": (
            "Across the complete fresh-scale source-start sweeps M=229, 251, "
            "293, and 331, what finite stress morphology should guide the "
            "next theorem target or falsifier?"),
        "scales": list(SCALES),
        "scale_count": len(SCALES),
        "scale_summaries": summaries,
        "all_complete_sweeps_pass_signed_dominance": all_pass,
        "weakest_sequence": weakest_sequence,
        "weakest_label_counts": dict(Counter(weakest_labels)),
        "weakest_prime_counts": dict(fixed_prime_counter),
        "single_fixed_weakest_prime_rule_survives": (
            len(fixed_prime_counter) == 1),
        "all_weakest_labels_are_0012": set(weakest_labels) == {"00,12"},
        "all_tightest_prime_blocks_are_row_coherent": row_coherent,
        "prime_block_morphology_prediction": (
            "The next complete source-start sweep should be tracked first at "
            "the prime-block level: when one prime is tight, all three "
            "components and TOTAL should bunch near the same slack before "
            "component labels become decisive."),
        "prime_block_morphology_falsifier": (
            "A future complete scale whose tightest rows are split across "
            "unrelated primes, or whose weakest row is not in a coherent "
            "four-row prime block, falsifies the row-coherent stress-block "
            "candidate."),
        "candidate_next_theorem_target": {
            "name": "source-start prime-block lower-frame control",
            "mechanism": (
                "Bound the source-start active/full ratio first by prime "
                "block, then treat component labels as a secondary spread "
                "inside each block."),
            "prediction": (
                "A future M=353 or larger full sweep should either produce a "
                "new coherent prime block of weak rows, or expose the first "
                "split-block falsifier of this morphology."),
            "falsifier": (
                "The next full source-start sweep has positive rows but its "
                "top four stress rows do not come from the same prime, or a "
                "single component is isolated far below its prime companions."),
            "novelty_label": "new-to-this-task",
        },
        "decision": (
            "The completed sweeps support prime-block stress tracking, not a "
            "single fixed-prime predictor.  All four weakest rows use label "
            "(00,12), but the weakest prime moves from 379 to 461 to 599, "
            "and each scale's tightest rows bunch by prime block.  Future "
            "finite work should track coherent prime blocks and use fixed "
            "attention primes only as secondary diagnostics."),
        "finite_morphology_audit_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_start_theorem_proved": False,
        "source_window_theorem_proved": False,
        "prime_block_theorem_proved": False,
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
