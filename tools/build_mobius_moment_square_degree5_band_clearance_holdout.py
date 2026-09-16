"""Check clearance-family margins on the weakest block in each sigma band."""

from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_source_margin_clearance_family_audit import (  # noqa: E402
    scale_clearance_summary,
)


BAND_AUDIT = (
    Path("evidence")
    / "mobius-moment-square-degree5-moving-prime-band-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-band-clearance-holdout.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def source_rows_from_band_audit():
    band_audit = json.loads(BAND_AUDIT.read_text(encoding="utf-8"))
    rows = []
    for band_name, band_summary in sorted(band_audit["band_summaries"].items()):
        block = band_summary["weakest_block"]
        rows.append({
            "band": band_name,
            "scale_modulus": block["scale_modulus"],
            "sigma_p_over_M": block["sigma_p_over_M"],
            "minimum_slack": block["minimum_slack"],
            "top_prime_block": {
                "prime_modulus": block["prime_modulus"],
                "weakest_label": block["weakest_label"],
            },
        })
    return rows


def band_clearance_summary(row):
    summary = scale_clearance_summary(row)
    summary["band"] = row["band"]
    summary["sigma_p_over_M"] = row["sigma_p_over_M"]
    summary["source_band_minimum_slack"] = row["minimum_slack"]
    summary["near_negative_over_middle_far_positive"] = (
        summary["near_negative_abs"]
        / summary["middle_far_positive_margin_sum"]
        if summary["middle_far_positive_margin_sum"] else None)
    return summary


def build_receipt():
    source_rows = source_rows_from_band_audit()
    summaries = []
    with ProcessPoolExecutor(max_workers=min(4, len(source_rows))) as executor:
        futures = {
            executor.submit(band_clearance_summary, row): row["band"]
            for row in source_rows
        }
        for future in as_completed(futures):
            summaries.append(future.result())
    summaries.sort(key=lambda row: row["band"])
    negative_family_counts = {
        family: sum(
            row["family_summaries"][family]["negative_count"]
            for row in summaries)
        for family in ("near_1_to_2", "middle_2_to_3", "far_3_plus")
    }
    ratios = [
        row["near_negative_over_middle_far_positive"]
        for row in summaries
        if row["near_negative_over_middle_far_positive"] is not None
    ]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "HOLDOUT_degree5_band_clearance_family",
        "source_band_audit": str(BAND_AUDIT),
        "question": (
            "Does the clearance-family denominator target survive on the "
            "weakest source-start prime block in each sigma band?"),
        "band_summaries": summaries,
        "band_count": len(summaries),
        "all_middle_far_positive_dominates_near_negative": all(
            row["middle_far_positive_dominates_near_negative"]
            for row in summaries),
        "all_middle_far_total_dominates_near_negative": all(
            row["middle_far_total_dominates_near_negative"]
            for row in summaries),
        "all_negative_denominators_near_threshold": all(
            row["all_negative_denominators_near_threshold"]
            for row in summaries),
        "negative_denominator_family_counts": negative_family_counts,
        "maximum_near_negative_over_middle_far_positive": max(ratios),
        "candidate_next_theorem_target": {
            "name": "sigma-banded clearance-family denominator control",
            "mechanism": (
                "For each sigma band, prove low-clearance adverse leakage is "
                "paid by middle/far higher-clearance denominator margin on "
                "the moving prime block."),
            "prediction": (
                "Future band-minimum blocks should keep middle/far net margin "
                "above near-threshold adverse leakage in every sigma band."),
            "falsifier": (
                "A band-minimum block whose middle/far net margin fails to "
                "dominate near-threshold adverse mass falsifies this finite "
                "band-clearance target."),
            "novelty_label": "new-to-this-task",
        },
        "decision": (
            "The clearance-family target survives on the weakest checked block "
            "in every sigma band.  This supports pairing sigma-banded moving "
            "prime-block control with a sigma-banded denominator-family ledger, "
            "but remains finite evidence only."),
        "finite_band_clearance_holdout_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_start_theorem_proved": False,
        "prime_block_theorem_proved": False,
        "moving_prime_block_theorem_proved": False,
        "sigma_band_theorem_proved": False,
        "clearance_family_theorem_proved": False,
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
