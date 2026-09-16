"""Build the full M=229 prime-row source-start sweep.

The fresh prime-span holdout found that the interior row M=229, p=347 was
weaker than the first-prime row.  This audit checks every prime row in
[229, 458] at the same canonical source start.  It is one complete fresh
scale, not an asymptotic theorem.
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
    / "mobius-moment-square-degree5-source-start-m229-full-prime-sweep.json")
SCALE_MODULUS = 229


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def m229_prime_rows():
    prime_moduli = primes_in_range(SCALE_MODULUS, 2 * SCALE_MODULUS)
    return [
        source_start_prime_row(SCALE_MODULUS, f"ordinal-{index}", prime)
        for index, prime in enumerate(prime_moduli)
    ]


def build_receipt():
    prime_rows = m229_prime_rows()
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
        "status": "SWEEP_degree5_source_start_m229_full_prime_rows",
        "question": (
            "After the M=229 interior sampled prime row was weakest in the "
            "fresh prime-span holdout, do all canonical source-start prime "
            "rows for M=229 satisfy signed active/full dominance?"),
        "scale_modulus": SCALE_MODULUS,
        "prime_interval": [SCALE_MODULUS, 2 * SCALE_MODULUS],
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
        "prediction": (
            "If the narrowed source-start lane is stable across the whole "
            "fresh M=229 prime interval, every prime row in [229, 458] should "
            "retain positive signed active/full slack."),
        "falsifier": (
            "Any M=229 prime-row component or total row with negative full "
            "contribution and active/full ratio at or below one half falsifies "
            "this full-fresh-scale sweep."),
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
        receipt["decision"] = (
            "The full M=229 prime-row source-start sweep survives: every "
            "prime row in [229, 458] has positive active/full dominance slack "
            "above one half.  This is one complete fresh scale only and "
            "proves no universal theorem.")
    else:
        receipt["decision"] = (
            "The full M=229 prime-row source-start sweep found at least one "
            "signed active/full failure.  This is a finite falsifier for the "
            "M=229 full fresh-scale source-start sweep.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
