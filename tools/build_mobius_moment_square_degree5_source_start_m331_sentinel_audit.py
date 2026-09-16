"""Build an M=331 source-start sentinel audit.

The full M=331 sweep is substantially more expensive than the completed
M=229, M=251, and M=293 sweeps.  This audit checks a bounded sentinel set
including low, mid, high, and the current attention prime p=461, while
recording per-row runtime so a later full sweep can be run with progress and
resume support instead of as an opaque long job.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from time import perf_counter


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
    / "mobius-moment-square-degree5-source-start-m331-sentinel-audit.json")
SCALE_MODULUS = 331
ATTENTION_PRIME = 461


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def selected_sentinel_primes():
    primes = primes_in_range(SCALE_MODULUS, 2 * SCALE_MODULUS)
    mid_target = (3 * SCALE_MODULUS) // 2
    selected = [
        ("low", primes[0]),
        ("attention", ATTENTION_PRIME),
        ("mid", min(primes, key=lambda p: (abs(p - mid_target), p))),
        ("high", primes[-1]),
    ]
    deduped = []
    seen = set()
    for label, prime in selected:
        if prime not in primes:
            raise ValueError(f"sentinel prime {prime} outside prime interval")
        if prime in seen:
            continue
        seen.add(prime)
        deduped.append((label, prime))
    return deduped


def timed_source_start_prime_row(label, prime_modulus):
    start = perf_counter()
    print(f"computing M={SCALE_MODULUS} {label} p={prime_modulus}", flush=True)
    row = source_start_prime_row(SCALE_MODULUS, label, prime_modulus)
    row["sentinel_label"] = label
    row["elapsed_seconds"] = perf_counter() - start
    rows = row["component_rows"] + [row["degree5_total_row"]]
    row["weakest_dominance_row"] = min(
        rows, key=lambda item: item["dominance_slack_above_one_half"])
    row["minimum_dominance_slack_above_one_half"] = (
        row["weakest_dominance_row"]["dominance_slack_above_one_half"])
    print(
        "done M={} {} p={} seconds={:.3f} weakest={} slack={:.12g}".format(
            SCALE_MODULUS,
            label,
            prime_modulus,
            row["elapsed_seconds"],
            row["weakest_dominance_row"]["label"],
            row["minimum_dominance_slack_above_one_half"],
        ),
        flush=True,
    )
    return row


def build_receipt():
    start = perf_counter()
    prime_rows = [
        timed_source_start_prime_row(label, prime)
        for label, prime in selected_sentinel_primes()
    ]
    total_elapsed = perf_counter() - start
    scale_result = {
        "scale_modulus": SCALE_MODULUS,
        "selected_primes": [
            {
                "sentinel_label": row["sentinel_label"],
                "prime_modulus": row["prime_modulus"],
                "elapsed_seconds": row["elapsed_seconds"],
            }
            for row in prime_rows
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
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_degree5_source_start_m331_sentinel_rows",
        "question": (
            "Before paying for a full opaque M=331 sweep, do low, attention, "
            "mid, and high source-start sentinel rows survive signed active/"
            "full dominance, and does p=461 remain a local stress marker?"),
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
        "total_elapsed_seconds": total_elapsed,
        "full_sweep_completed": False,
        "full_sweep_runtime_blocker": (
            "A single M=331 row took about 40 seconds in the current builder; "
            "a full sweep should be rerun with per-prime progress and resume "
            "support before promotion."),
        "prediction": (
            "If the source-start lane remains stable at M=331, these sentinel "
            "rows should retain positive signed active/full slack.  If p=461 "
            "is the current local stress channel, the attention row should be "
            "the weakest or near the weakest sentinel row."),
        "falsifier": (
            "Any sentinel component or total row with negative full contribution "
            "and active/full ratio at or below one half falsifies this M=331 "
            "sentinel audit.  A weak row far from p=461 downgrades the p=461 "
            "attention interpretation."),
        "decision": (
            "Filled by generated receipt consumer after the audit is inspected."),
        "finite_sentinel_audit_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_window_theorem_proved": False,
        "source_start_theorem_proved": False,
        "active_window_translation_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
    }


def main():
    receipt = build_receipt()
    if receipt["all_rows_dominate_one_half_signed_full"]:
        if receipt["weakest_prime_equals_attention_prime"]:
            attention_sentence = "The weakest sentinel row is p=461."
        else:
            attention_sentence = (
                "The weakest sentinel row is not p=461, so the p=461 attention "
                "interpretation is downgraded in this sentinel set.")
        receipt["decision"] = (
            "The M=331 source-start sentinel audit survives: all selected "
            "sentinel rows have positive active/full dominance slack above "
            f"one half.  {attention_sentence} This is a finite sentinel audit "
            "only, not a full M=331 sweep and not a universal theorem.")
    else:
        receipt["decision"] = (
            "The M=331 source-start sentinel audit found at least one signed "
            "active/full failure.  This is a finite sentinel falsifier.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
