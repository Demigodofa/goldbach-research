"""Build the full M=331 prime-row source-start sweep with resume support.

The M=331 sentinel audit survived but deliberately left the full 55-prime
interval open because each row is expensive in the current endpoint-frame
builder.  This runner pays that cost with per-prime progress and a checkpoint
file, so an interrupted sweep can resume without discarding completed rows.
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
    / "mobius-moment-square-degree5-source-start-m331-full-prime-sweep.json")
CHECKPOINT = (
    ROOT
    / "evidence"
    / "mobius-moment-square-degree5-source-start-m331-full-prime-sweep.partial.json")
SCALE_MODULUS = 331
ATTENTION_PRIME = 461


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def m331_prime_moduli():
    return primes_in_range(SCALE_MODULUS, 2 * SCALE_MODULUS)


def write_json_atomic(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    tmp.replace(path)


def timed_source_start_prime_row(ordinal, prime_modulus):
    start = perf_counter()
    print(
        f"computing M={SCALE_MODULUS} ordinal={ordinal} p={prime_modulus}",
        flush=True,
    )
    row = source_start_prime_row(
        SCALE_MODULUS, f"ordinal-{ordinal}", prime_modulus)
    row["ordinal"] = ordinal
    row["elapsed_seconds"] = perf_counter() - start
    rows = row["component_rows"] + [row["degree5_total_row"]]
    row["weakest_dominance_row"] = min(
        rows, key=lambda item: item["dominance_slack_above_one_half"])
    row["minimum_dominance_slack_above_one_half"] = (
        row["weakest_dominance_row"]["dominance_slack_above_one_half"])
    print(
        "done M={} ordinal={} p={} seconds={:.3f} weakest={} slack={:.12g}".
        format(
            SCALE_MODULUS,
            ordinal,
            prime_modulus,
            row["elapsed_seconds"],
            row["weakest_dominance_row"]["label"],
            row["minimum_dominance_slack_above_one_half"],
        ),
        flush=True,
    )
    return row


def load_checkpoint():
    if not CHECKPOINT.exists():
        return []
    checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    if checkpoint.get("scale_modulus") != SCALE_MODULUS:
        raise ValueError("checkpoint scale mismatch")
    if checkpoint.get("prime_interval") != [SCALE_MODULUS, 2 * SCALE_MODULUS]:
        raise ValueError("checkpoint interval mismatch")
    rows = checkpoint.get("completed_prime_rows", [])
    expected = m331_prime_moduli()
    seen = []
    for row in rows:
        prime = row["prime_modulus"]
        if prime not in expected:
            raise ValueError(f"checkpoint has unexpected prime {prime}")
        if prime in seen:
            raise ValueError(f"checkpoint repeats prime {prime}")
        seen.append(prime)
    if seen != expected[:len(seen)]:
        raise ValueError("checkpoint rows are not the expected prefix")
    return rows


def checkpoint_payload(prime_rows, run_elapsed_seconds):
    expected = m331_prime_moduli()
    completed = [row["prime_modulus"] for row in prime_rows]
    pending = expected[len(completed):]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "PARTIAL_degree5_source_start_m331_full_prime_rows",
        "scale_modulus": SCALE_MODULUS,
        "prime_interval": [SCALE_MODULUS, 2 * SCALE_MODULUS],
        "prime_moduli": expected,
        "completed_prime_moduli": completed,
        "pending_prime_moduli": pending,
        "completed_prime_count": len(completed),
        "pending_prime_count": len(pending),
        "completed_prime_rows": prime_rows,
        "run_elapsed_seconds": run_elapsed_seconds,
        "checkpoint_path": str(CHECKPOINT.relative_to(ROOT)),
        "resumable": True,
        "full_sweep_completed": False,
        "finite_partial_receipt_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_window_theorem_proved": False,
        "source_start_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
    }


def summarize_full_sweep(prime_rows, total_elapsed_seconds):
    scale_result = {
        "scale_modulus": SCALE_MODULUS,
        "prime_moduli": [row["prime_modulus"] for row in prime_rows],
        "prime_rows": prime_rows,
        "prime_row_count": len(prime_rows),
        "row_elapsed_seconds": [
            {
                "ordinal": row["ordinal"],
                "prime_modulus": row["prime_modulus"],
                "elapsed_seconds": row["elapsed_seconds"],
            }
            for row in prime_rows
        ],
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
        "status": "SWEEP_degree5_source_start_m331_full_prime_rows",
        "question": (
            "After the M=331 sentinel audit survived and identified p=461 as "
            "the weakest sentinel row, do all canonical source-start prime "
            "rows for M=331 satisfy signed active/full dominance?"),
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
        "total_elapsed_seconds": total_elapsed_seconds,
        "checkpoint_path": str(CHECKPOINT.relative_to(ROOT)),
        "checkpoint_removed_after_success": not CHECKPOINT.exists(),
        "resumable_runner_used": True,
        "full_sweep_completed": True,
        "prediction": (
            "If the source-start lane remains stable at M=331, every prime "
            "row in [331, 662] should retain positive signed active/full "
            "slack.  If p=461 is a durable local stress channel, the global "
            "weakest row should be p=461 or close to it."),
        "falsifier": (
            "Any M=331 prime-row component or total row with negative full "
            "contribution and active/full ratio at or below one half falsifies "
            "this full-fresh-scale sweep.  A weakest row far from p=461 "
            "downgrades the p=461 attention interpretation."),
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


def build_receipt():
    expected = m331_prime_moduli()
    prime_rows = load_checkpoint()
    completed = {row["prime_modulus"] for row in prime_rows}
    start = perf_counter()
    if prime_rows:
        print(
            f"resuming M={SCALE_MODULUS}: {len(prime_rows)}/"
            f"{len(expected)} rows already complete",
            flush=True,
        )
    for ordinal, prime in enumerate(expected):
        if prime in completed:
            continue
        row = timed_source_start_prime_row(ordinal, prime)
        prime_rows.append(row)
        completed.add(prime)
        write_json_atomic(
            CHECKPOINT, checkpoint_payload(prime_rows, perf_counter() - start))
    if CHECKPOINT.exists():
        CHECKPOINT.unlink()
    receipt = summarize_full_sweep(prime_rows, perf_counter() - start)
    if receipt["all_rows_dominate_one_half_signed_full"]:
        if receipt["weakest_prime_equals_attention_prime"]:
            attention_sentence = "The global weakest row is p=461."
        else:
            attention_sentence = (
                "The global weakest row is not p=461, so the p=461 attention "
                "interpretation is downgraded for this full scale.")
        receipt["decision"] = (
            "The full M=331 prime-row source-start sweep survives: every "
            "prime row in [331, 662] has positive active/full dominance slack "
            f"above one half.  {attention_sentence} This is one complete "
            "fresh scale only and proves no universal theorem.")
    else:
        receipt["decision"] = (
            "The full M=331 prime-row source-start sweep found at least one "
            "signed active/full failure.  This is a finite falsifier for the "
            "M=331 full fresh-scale source-start sweep.")
    return receipt


def main():
    receipt = build_receipt()
    write_json_atomic(OUT, receipt)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
