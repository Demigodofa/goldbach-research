"""Build the full M=293 prime-row source-start sweep.

M=229 and M=251 survived full fresh-scale source-start sweeps, and a fixed
p=379 cross-scale audit made p=379 a lower-scale attention point.  This audit
checks the next fresh scale M=293 to see whether the full sweep survives and
whether its weakest row is still near that attention channel.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    flatten_rows,
    sign_counts,
)
from tools.build_mobius_moment_square_degree5_primewise_dominance_audit import (  # noqa: E402
    THRESHOLD,
)
from tools.build_mobius_moment_square_degree5_source_start_fresh_prime_span_holdout import (  # noqa: E402
    primes_in_range,
    source_start_prime_row,
)


OUT = (
    ROOT
    / "evidence"
    / "mobius-moment-square-degree5-source-start-m293-full-prime-sweep.json")
SCALE_MODULUS = 293
ATTENTION_PRIME = 379


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def m293_prime_rows():
    prime_moduli = primes_in_range(SCALE_MODULUS, 2 * SCALE_MODULUS)
    return [
        source_start_prime_row(SCALE_MODULUS, f"ordinal-{index}", prime)
        for index, prime in enumerate(prime_moduli)
    ]


def build_receipt():
    prime_rows = m293_prime_rows()
    scale_result = {
        "scale_modulus": SCALE_MODULUS,
        "prime_moduli": [
            row["prime_modulus"] for row in prime_rows
        ],
        "prime_rows": prime_rows,
        "prime_row_count": len(prime_rows),
    }
    all_rows = flatten_rows([scale_result])
    component_rows = [row for row in all_rows if row["label"] != "TOTAL"]
    total_rows = [row for row in all_rows if row["label"] == "TOTAL"]
    all_slacks = [
        row["dominance_slack_above_one_half"] for row in all_rows]
    weakest = min(
        all_rows,
        key=lambda row: row["dominance_slack_above_one_half"])
    strongest = max(
        all_rows,
        key=lambda row: row["dominance_slack_above_one_half"])
    attention_rows = [
        row for row in all_rows
        if row["prime_modulus"] == ATTENTION_PRIME
    ]
    attention_weakest = min(
        attention_rows,
        key=lambda row: row["dominance_slack_above_one_half"])
    scale_result.update({
        "component_row_count": len(component_rows),
        "degree5_total_row_count": len(total_rows),
        "dominance_row_count": len(all_rows),
        "all_rows_dominate_one_half_signed_full": all(
            row["dominates_one_half_signed_full"] for row in all_rows),
        "minimum_dominance_slack_above_one_half": min(all_slacks),
        "maximum_dominance_slack_above_one_half": max(all_slacks),
        "weakest_dominance_row": weakest,
        "strongest_dominance_row": strongest,
    })
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "SWEEP_degree5_source_start_m293_full_prime_rows",
        "question": (
            "After M=229 and M=251 survived full source-start sweeps and "
            "p=379 became a lower-scale attention point, do all canonical "
            "source-start prime rows for M=293 satisfy signed active/full "
            "dominance, and is the weakest row near p=379?"),
        "scale_modulus": SCALE_MODULUS,
        "prime_interval": [SCALE_MODULUS, 2 * SCALE_MODULUS],
        "attention_prime": ATTENTION_PRIME,
        "threshold": THRESHOLD,
        "scale_result": scale_result,
        "prime_row_count": len(prime_rows),
        "component_row_count": len(component_rows),
        "degree5_total_row_count": len(total_rows),
        "dominance_row_count": len(all_rows),
        "all_dominance_slack_sign_counts": sign_counts(all_slacks),
        "all_rows_dominate_one_half_signed_full": all(
            row["dominates_one_half_signed_full"] for row in all_rows),
        "minimum_dominance_slack_above_one_half": min(all_slacks),
        "maximum_dominance_slack_above_one_half": max(all_slacks),
        "weakest_dominance_row": weakest,
        "strongest_dominance_row": strongest,
        "attention_prime_weakest_row": attention_weakest,
        "weakest_prime_equals_attention_prime": (
            weakest["prime_modulus"] == ATTENTION_PRIME),
        "weakest_prime_distance_from_attention_prime": abs(
            weakest["prime_modulus"] - ATTENTION_PRIME),
        "prediction": (
            "If the source-start lane is stable across this next fresh scale, "
            "every prime row in [293, 586] should retain positive signed "
            "active/full slack.  If p=379 remains the controlling local stress "
            "channel, the global weakest row should be p=379 or very near it."),
        "falsifier": (
            "Any M=293 prime-row component or total row with negative full "
            "contribution and active/full ratio at or below one half falsifies "
            "this full-fresh-scale sweep.  A weakest row far from p=379 "
            "downgrades the p=379-local-stress interpretation."),
        "decision": (
            "Filled by generated receipt consumer after the sweep is inspected."),
        "one_full_fresh_scale_sweep_only": True,
        "finite_sweep_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_window_theorem_proved": False,
        "source_start_theorem_proved": False,
        "all_fresh_scales_swept": False,
        "active_window_translation_theorem_proved": False,
        "endpoint_swap_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
    }


def main():
    receipt = build_receipt()
    if receipt["all_rows_dominate_one_half_signed_full"]:
        if receipt["weakest_prime_equals_attention_prime"]:
            attention_sentence = "The global weakest row is p=379."
        else:
            attention_sentence = (
                "The global weakest row is not p=379, so the p=379-local "
                "stress interpretation is downgraded for this scale.")
        receipt["decision"] = (
            "The full M=293 prime-row source-start sweep survives: every "
            "prime row in [293, 586] has positive active/full dominance slack "
            f"above one half.  {attention_sentence} This is one complete "
            "fresh scale only and proves no universal theorem.")
    else:
        receipt["decision"] = (
            "The full M=293 prime-row source-start sweep found at least one "
            "signed active/full failure.  This is a finite falsifier for the "
            "M=293 full fresh-scale source-start sweep.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
