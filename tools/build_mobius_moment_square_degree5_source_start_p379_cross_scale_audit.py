"""Build a p=379 cross-scale source-start stress audit.

The full M=229 and M=251 fresh sweeps both had their weakest row at prime
p=379, component (00,12).  This audit keeps p fixed and varies the scale M
across nearby checked and fresh source-start scales where p is in [M, 2M].
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
    source_start_prime_row,
)


OUT = (
    ROOT
    / "evidence"
    / "mobius-moment-square-degree5-source-start-p379-cross-scale-audit.json")
PRIME_MODULUS = 379
SCALE_MODULI = (191, 211, 227, 229, 251, 293, 331, 353, 379)
FULL_SWEEP_SCALES = (229, 251)
ORIGINAL_CHECKED_SCALES = (191, 211, 227)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def scale_class(scale_modulus):
    if scale_modulus in FULL_SWEEP_SCALES:
        return "fresh_full_sweep_scale"
    if scale_modulus in ORIGINAL_CHECKED_SCALES:
        return "original_checked_scale"
    return "fresh_unswept_scale"


def p379_scale_row(scale_modulus):
    if not (scale_modulus <= PRIME_MODULUS <= 2 * scale_modulus):
        raise ValueError(
            f"p={PRIME_MODULUS} outside [{scale_modulus}, {2 * scale_modulus}]")
    row = source_start_prime_row(scale_modulus, "p379", PRIME_MODULUS)
    row["scale_class"] = scale_class(scale_modulus)
    rows = row["component_rows"] + [row["degree5_total_row"]]
    weakest = min(rows, key=lambda item: item[
        "dominance_slack_above_one_half"])
    row["weakest_dominance_row"] = weakest
    row["minimum_dominance_slack_above_one_half"] = (
        weakest["dominance_slack_above_one_half"])
    return row


def build_receipt():
    scale_results = [
        p379_scale_row(scale_modulus)
        for scale_modulus in SCALE_MODULI
    ]
    all_rows = flatten_rows([{"prime_rows": scale_results}])
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
    weakest_scales = sorted(
        scale_results,
        key=lambda row: row["minimum_dominance_slack_above_one_half"])
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_degree5_source_start_p379_cross_scale_stress",
        "question": (
            "After p=379 was the weakest prime row in both full fresh sweeps "
            "M=229 and M=251, is p=379 a repeatable cross-scale source-start "
            "stress point across nearby scales?"),
        "prime_modulus": PRIME_MODULUS,
        "scale_moduli": SCALE_MODULI,
        "threshold": THRESHOLD,
        "scale_results": scale_results,
        "scale_count": len(scale_results),
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
        "weakest_scale_rows": [
            {
                "scale_modulus": row["scale_modulus"],
                "scale_class": row["scale_class"],
                "row_count": row["row_count"],
                "weakest_label": row["weakest_dominance_row"]["label"],
                "weakest_ratio": (
                    row["weakest_dominance_row"]["active_over_full_ratio"]),
                "weakest_slack": (
                    row["minimum_dominance_slack_above_one_half"]),
            }
            for row in weakest_scales
        ],
        "prediction": (
            "If p=379 is a real local stress channel, it should keep producing "
            "the weakest or near-weakest component, especially (00,12), across "
            "nearby source-start scales."),
        "falsifier": (
            "Any p=379 checked scale row with negative full contribution and "
            "active/full ratio at or below one half falsifies the finite p=379 "
            "cross-scale stress audit.  If p=379 is not systematically weak, "
            "the attention-point interpretation is downgraded."),
        "decision": (
            "Filled by generated receipt consumer after the audit is inspected."),
        "finite_attention_audit_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "p379_stress_theorem_proved": False,
        "source_window_theorem_proved": False,
        "source_start_theorem_proved": False,
        "active_window_translation_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
    }


def main():
    receipt = build_receipt()
    if receipt["all_rows_dominate_one_half_signed_full"]:
        receipt["decision"] = (
            "The p=379 cross-scale audit survives: every checked p=379 "
            "source-start component and total row has positive active/full "
            "dominance slack above one half.  The audit is finite attention "
            "evidence only and proves no universal theorem.")
    else:
        receipt["decision"] = (
            "The p=379 cross-scale audit found at least one signed active/full "
            "failure.  This is a finite p=379 source-start falsifier.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
