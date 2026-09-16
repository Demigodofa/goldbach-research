"""Build the full M=353 prime-row source-start sweep with resume support.

The stress-morphology audit across M=229, 251, 293, and 331 suggests that
source-start stress is prime-block coherent rather than controlled by a single
fixed attention prime.  This runner tests the next fresh scale, M=353, as the
first prospective falsifier of that morphology.
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
    / "mobius-moment-square-degree5-source-start-m353-full-prime-sweep.json")
CHECKPOINT = (
    ROOT
    / "evidence"
    / "mobius-moment-square-degree5-source-start-m353-full-prime-sweep.partial.json")
SCALE_MODULUS = 353
PRIOR_STRESS_PRIMES = (379, 461, 599, 647)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def m353_prime_moduli():
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
    expected = m353_prime_moduli()
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
    expected = m353_prime_moduli()
    completed = [row["prime_modulus"] for row in prime_rows]
    pending = expected[len(completed):]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "PARTIAL_degree5_source_start_m353_full_prime_rows",
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
        "prime_block_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
    }


def prime_block_records(scale_result):
    blocks = []
    for prime_row in scale_result["prime_rows"]:
        rows = prime_row["component_rows"] + [prime_row["degree5_total_row"]]
        weakest = min(
            rows, key=lambda row: row["dominance_slack_above_one_half"])
        slacks = [row["dominance_slack_above_one_half"] for row in rows]
        blocks.append({
            "prime_modulus": prime_row["prime_modulus"],
            "prime_over_scale": prime_row["prime_modulus"] / SCALE_MODULUS,
            "tail_fraction": (
                (2 * SCALE_MODULUS - prime_row["prime_modulus"])
                / SCALE_MODULUS),
            "minimum_slack": min(slacks),
            "maximum_slack": max(slacks),
            "slack_spread": max(slacks) - min(slacks),
            "weakest_label": weakest["label"],
            "labels_by_slack": [
                row["label"]
                for row in sorted(
                    rows,
                    key=lambda item: item["dominance_slack_above_one_half"])
            ],
        })
    return sorted(blocks, key=lambda block: block["minimum_slack"])


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
    blocks = prime_block_records(scale_result)
    tightest_prime = blocks[0]["prime_modulus"]
    top_four_rows = sorted(
        all_rows, key=lambda row: row["dominance_slack_above_one_half"])[:4]
    prior_stress_rows = {}
    for prime in PRIOR_STRESS_PRIMES:
        prime_rows_for_stress = [
            row for row in all_rows if row["prime_modulus"] == prime
        ]
        if prime_rows_for_stress:
            prior_stress_rows[str(prime)] = min(
                prime_rows_for_stress,
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
        "status": "SWEEP_degree5_source_start_m353_full_prime_rows",
        "question": (
            "Does the next fresh complete source-start sweep M=353 preserve "
            "signed active/full dominance and the prime-block stress "
            "morphology seen at M=229, 251, 293, and 331?"),
        "scale_modulus": SCALE_MODULUS,
        "prime_interval": [SCALE_MODULUS, 2 * SCALE_MODULUS],
        "prior_stress_primes": list(PRIOR_STRESS_PRIMES),
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
        "prior_stress_prime_weakest_rows": prior_stress_rows,
        "tightest_prime_blocks": blocks[:4],
        "top_four_rows": top_four_rows,
        "top_four_rows_form_single_prime_block": (
            len({row["prime_modulus"] for row in top_four_rows}) == 1),
        "top_four_prime_modulus": tightest_prime,
        "top_four_labels": [
            row["label"] for row in top_four_rows
        ],
        "top_four_labels_match_component_total_block": (
            {row["label"] for row in top_four_rows}
            == {"00,12", "01,02", "01,11", "TOTAL"}),
        "total_elapsed_seconds": total_elapsed_seconds,
        "checkpoint_path": str(CHECKPOINT.relative_to(ROOT)),
        "checkpoint_removed_after_success": not CHECKPOINT.exists(),
        "resumable_runner_used": True,
        "full_sweep_completed": True,
        "prediction": (
            "If prime-block morphology persists, the tightest four rows of "
            "M=353 should come from one prime block containing the three "
            "tracked components and TOTAL, rather than splitting across "
            "unrelated primes."),
        "falsifier": (
            "Positive dominance can still survive while morphology fails: the "
            "finite morphology is falsified if the tightest rows split across "
            "different primes or isolate one component far below its prime "
            "companions."),
        "decision": (
            "Filled by generated receipt consumer after the sweep is inspected."),
        "one_full_fresh_scale_sweep_only": True,
        "finite_sweep_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_window_theorem_proved": False,
        "source_start_theorem_proved": False,
        "prime_block_theorem_proved": False,
        "all_fresh_scales_swept": False,
        "active_window_translation_theorem_proved": False,
        "endpoint_swap_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
    }


def build_receipt():
    expected = m353_prime_moduli()
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
        if receipt["top_four_rows_form_single_prime_block"]:
            morphology_sentence = (
                "The tightest rows remain a coherent prime block.")
        else:
            morphology_sentence = (
                "The tightest rows split across primes, so the finite "
                "prime-block morphology is falsified for M=353.")
        receipt["decision"] = (
            "The full M=353 prime-row source-start sweep survives signed "
            f"dominance.  {morphology_sentence} This is one complete fresh "
            "scale only and proves no universal theorem.")
    else:
        receipt["decision"] = (
            "The full M=353 prime-row source-start sweep found at least one "
            "signed active/full failure.  This is a finite falsifier for the "
            "M=353 full fresh-scale source-start sweep.")
    return receipt


def main():
    receipt = build_receipt()
    write_json_atomic(OUT, receipt)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
