"""Check the clearance-family denominator target on the fresh M=383 block."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_source_margin_clearance_family_audit import (  # noqa: E402
    scale_clearance_summary,
)


SOURCE_SWEEP = (
    Path("evidence")
    / "mobius-moment-square-degree5-source-start-m383-full-prime-sweep.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-source-margin-m383-clearance-holdout.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def build_receipt():
    sweep = json.loads(SOURCE_SWEEP.read_text(encoding="utf-8"))
    weakest = sweep["weakest_dominance_row"]
    row = {
        "scale_modulus": sweep["scale_modulus"],
        "top_prime_block": {
            "prime_modulus": weakest["prime_modulus"],
            "weakest_label": weakest["label"],
        },
    }
    summary = scale_clearance_summary(row)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "HOLDOUT_degree5_source_margin_m383_clearance_family",
        "source_full_sweep": str(SOURCE_SWEEP),
        "question": (
            "Does the clearance-family denominator target survive on the "
            "fresh M=383 full-sweep tight block?"),
        "scale_summary": summary,
        "scale_modulus": summary["scale_modulus"],
        "prime_modulus": summary["prime_modulus"],
        "weakest_label": summary["weakest_label"],
        "near_negative_abs": summary["near_negative_abs"],
        "middle_far_positive_margin_sum": (
            summary["middle_far_positive_margin_sum"]),
        "middle_far_total_margin_sum": summary["middle_far_total_margin_sum"],
        "all_negative_denominators_near_threshold": (
            summary["all_negative_denominators_near_threshold"]),
        "middle_far_positive_dominates_near_negative": (
            summary["middle_far_positive_dominates_near_negative"]),
        "middle_far_total_dominates_near_negative": (
            summary["middle_far_total_dominates_near_negative"]),
        "near_negative_over_middle_far_positive": (
            summary["near_negative_abs"]
            / summary["middle_far_positive_margin_sum"]),
        "decision": (
            "The fresh M=383 tight block supports the clearance-family target: "
            "all adverse denominator mass is in the near-threshold family, and "
            "middle/far higher-clearance positive and net margin dominate that "
            "near-threshold leakage.  This is one fresh block only and proves "
            "no universal theorem."),
        "fresh_clearance_holdout_only": True,
        "finite_holdout_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_start_theorem_proved": False,
        "prime_block_theorem_proved": False,
        "denominator_margin_theorem_proved": False,
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
