"""Audit the moving-prime source-start stress by normalized position p/M."""

from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SCALES = (229, 251, 293, 331, 353, 379, 383)
OUT = (
    EVIDENCE
    / "mobius-moment-square-degree5-moving-prime-band-audit.json")

BANDS = (
    ("sigma_1_00_1_25", 1.00, 1.25),
    ("sigma_1_25_1_50", 1.25, 1.50),
    ("sigma_1_50_1_75", 1.50, 1.75),
    ("sigma_1_75_2_00", 1.75, 2.01),
)


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


def band_for_sigma(sigma):
    for name, lower, upper in BANDS:
        if lower <= sigma < upper:
            return name
    raise ValueError(f"sigma out of band range: {sigma}")


def load_sweep(scale):
    return json.loads(receipt_path(scale).read_text(encoding="utf-8"))


def block_records():
    blocks = []
    rows = []
    for scale in SCALES:
        receipt = load_sweep(scale)
        for prime_row in receipt["scale_result"]["prime_rows"]:
            prime = prime_row["prime_modulus"]
            sigma = prime / scale
            component_rows = prime_row["component_rows"]
            all_block_rows = component_rows + [prime_row["degree5_total_row"]]
            weakest = min(
                all_block_rows,
                key=lambda row: row["dominance_slack_above_one_half"])
            slacks = [
                row["dominance_slack_above_one_half"]
                for row in all_block_rows]
            record = {
                "scale_modulus": scale,
                "prime_modulus": prime,
                "sigma_p_over_M": sigma,
                "band": band_for_sigma(sigma),
                "minimum_slack": min(slacks),
                "maximum_slack": max(slacks),
                "slack_spread": max(slacks) - min(slacks),
                "weakest_label": weakest["label"],
                "labels_by_slack": [
                    row["label"]
                    for row in sorted(
                        all_block_rows,
                        key=lambda row: row[
                            "dominance_slack_above_one_half"])
                ],
            }
            blocks.append(record)
            for row in all_block_rows:
                row_record = dict(record)
                row_record.update({
                    "label": row["label"],
                    "active_over_full_ratio": row["active_over_full_ratio"],
                    "dominance_slack_above_one_half": (
                        row["dominance_slack_above_one_half"]),
                })
                rows.append(row_record)
    return blocks, rows


def compact_block(record):
    return {
        "scale_modulus": record["scale_modulus"],
        "prime_modulus": record["prime_modulus"],
        "sigma_p_over_M": record["sigma_p_over_M"],
        "band": record["band"],
        "minimum_slack": record["minimum_slack"],
        "weakest_label": record["weakest_label"],
        "labels_by_slack": record["labels_by_slack"],
    }


def compact_row(record):
    return {
        "scale_modulus": record["scale_modulus"],
        "prime_modulus": record["prime_modulus"],
        "sigma_p_over_M": record["sigma_p_over_M"],
        "band": record["band"],
        "label": record["label"],
        "dominance_slack_above_one_half": (
            record["dominance_slack_above_one_half"]),
        "active_over_full_ratio": record["active_over_full_ratio"],
    }


def summarize_band(name, blocks, rows):
    band_blocks = [block for block in blocks if block["band"] == name]
    band_rows = [row for row in rows if row["band"] == name]
    weakest_block = min(
        band_blocks, key=lambda item: item["minimum_slack"])
    weakest_row = min(
        band_rows, key=lambda item: item["dominance_slack_above_one_half"])
    return {
        "band": name,
        "block_count": len(band_blocks),
        "row_count": len(band_rows),
        "minimum_block_slack": weakest_block["minimum_slack"],
        "minimum_row_slack": weakest_row[
            "dominance_slack_above_one_half"],
        "weakest_block": compact_block(weakest_block),
        "weakest_row": compact_row(weakest_row),
        "weakest_label_counts": dict(Counter(
            block["weakest_label"] for block in band_blocks)),
    }


def build_receipt():
    blocks, rows = block_records()
    band_summaries = {
        name: summarize_band(name, blocks, rows)
        for name, _, _ in BANDS
    }
    weakest_block = min(blocks, key=lambda item: item["minimum_slack"])
    weakest_row = min(
        rows, key=lambda item: item["dominance_slack_above_one_half"])
    endpoint_band_names = {"sigma_1_00_1_25", "sigma_1_75_2_00"}
    endpoint_minimum = min(
        band_summaries[name]["minimum_block_slack"]
        for name in endpoint_band_names)
    interior_minimum = min(
        band_summaries[name]["minimum_block_slack"]
        for name in set(band_summaries) - endpoint_band_names)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_degree5_moving_prime_band_stress",
        "source_sweeps": [
            str(receipt_path(scale).relative_to(ROOT)) for scale in SCALES],
        "question": (
            "After fixed-prime stress is obstructed, where do the moving "
            "source-start prime-block stresses sit in sigma=p/M, and can "
            "endpoint bands be safely treated as irrelevant?"),
        "scales": list(SCALES),
        "scale_count": len(SCALES),
        "band_definitions": [
            {"name": name, "lower_inclusive": lower, "upper_exclusive": upper}
            for name, lower, upper in BANDS
        ],
        "prime_block_count": len(blocks),
        "dominance_row_count": len(rows),
        "band_summaries": band_summaries,
        "overall_weakest_block": compact_block(weakest_block),
        "overall_weakest_row": compact_row(weakest_row),
        "endpoint_minimum_block_slack": endpoint_minimum,
        "interior_minimum_block_slack": interior_minimum,
        "endpoint_bands_have_no_failures": endpoint_minimum > 0,
        "interior_bands_have_no_failures": interior_minimum > 0,
        "all_bands_have_positive_block_slack": all(
            summary["minimum_block_slack"] > 0
            for summary in band_summaries.values()),
        "endpoint_only_simplification_supported": False,
        "candidate_next_theorem_target": {
            "name": "sigma-banded moving prime-block lower-frame control",
            "mechanism": (
                "Prove source-start prime-block lower-frame control uniformly "
                "over sigma=p/M bands covering [1,2], rather than fixing one "
                "prime or discarding endpoints."),
            "prediction": (
                "Future complete sweeps should keep positive slack in each "
                "sigma band, with stress moving among bands rather than "
                "locking to a fixed prime."),
            "falsifier": (
                "A future complete sweep with a nonpositive block in any "
                "sigma band falsifies the current finite moving-band target."),
            "novelty_label": "new-to-this-task",
        },
        "decision": (
            "The seven-sweep fixture does not support reducing the theorem "
            "target to a fixed prime or to endpoint removal.  All sigma bands "
            "pass, but endpoint bands still contain relatively small slacks.  "
            "The next analytic target should be sigma-banded moving prime-"
            "block control across the whole interval [1,2]."),
        "finite_band_audit_only": True,
        "goldbach_proved": False,
        "source_start_theorem_proved": False,
        "prime_block_theorem_proved": False,
        "moving_prime_block_theorem_proved": False,
        "sigma_band_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
    }


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
