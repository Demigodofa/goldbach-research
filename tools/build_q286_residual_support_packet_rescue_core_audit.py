"""Audit fixed rescue cores for the q286 residual support-packet route.

The support-packet budget audit found that 15 conductor-support packets give a
meaningful signed dictionary, while adverse-only packet envelopes fail.  This
receipt asks the next narrower question: can a small fixed set of signed rescue
packets certify the positive rows if all other packets are paid by a fitted
adverse envelope?

Finite theorem-budget audit only.  It proves no rescue-core theorem, packet
theorem, character-sum theorem, signed binary-prime correlation theorem, q286
threshold theorem, strict-central Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import itertools
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE = EVIDENCE / "q286-residual-character-support-packet-budget-audit.json"
OUT = EVIDENCE / "q286-residual-support-packet-rescue-core-audit.json"
TOLERANCE = 1e-10


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def packet_action(row, label):
    for packet in row["packet_rows"]:
        if packet["support_label"] == label:
            return float(packet["signed_packet_action"])
    return 0.0


def adverse_envelope(rows, labels):
    return {
        label: max(max(0.0, -packet_action(row, label)) for row in rows)
        for label in labels
    }


def evaluate_core(rows, labels, envelope, core):
    core_set = set(core)
    tail_envelope = math.fsum(
        envelope[label] for label in labels if label not in core_set)
    row_results = []
    for row in rows:
        core_signed = math.fsum(packet_action(row, label) for label in core)
        core_abs = math.fsum(abs(packet_action(row, label)) for label in core)
        margin = row["aligned_only_full_action"] + core_signed - tail_envelope
        row_results.append({
            "target": row["target"],
            "aligned_only_full_action": row["aligned_only_full_action"],
            "core_signed_action": core_signed,
            "core_abs_action": core_abs,
            "tail_adverse_envelope": tail_envelope,
            "rescue_core_margin": margin,
            "core_relative_error_budget_with_tail_exact": (
                margin / core_abs if core_abs > TOLERANCE else None),
            "certified": bool(margin > TOLERANCE),
        })
    tight = min(
        row_results,
        key=lambda result: (result["rescue_core_margin"], result["target"]))
    return {
        "core": list(core),
        "core_size": len(core),
        "tail_packet_count": len(labels) - len(core),
        "tail_adverse_envelope": tail_envelope,
        "minimum_margin": tight["rescue_core_margin"],
        "certified_positive_row_count": sum(
            result["certified"] for result in row_results),
        "all_positive_rows_certified": all(
            result["certified"] for result in row_results),
        "tight_row": tight,
        "row_results": row_results,
    }


def best_cores_by_size(rows, labels, envelope):
    results = []
    minimal_certifying = None
    certifying_counts = {}
    for size in range(len(labels) + 1):
        best = None
        count = 0
        for core in itertools.combinations(labels, size):
            result = evaluate_core(rows, labels, envelope, core)
            if best is None or result["minimum_margin"] > best["minimum_margin"]:
                best = result
            if result["all_positive_rows_certified"]:
                count += 1
                if minimal_certifying is None:
                    minimal_certifying = result
        certifying_counts[str(size)] = count
        results.append(best)
    return results, certifying_counts, minimal_certifying


def finite_summary(values):
    finite = [
        float(value) for value in values
        if value is not None and math.isfinite(float(value))]
    if not finite:
        return {"count": 0, "minimum": None, "mean": None, "maximum": None}
    return {
        "count": len(finite),
        "minimum": min(finite),
        "mean": math.fsum(finite) / len(finite),
        "maximum": max(finite),
    }


def build_receipt():
    source = load_json(SOURCE)
    positive_rows = [
        row for row in source["target_rows"] if row["actual_full_positive"]]
    labels = sorted({
        packet["support_label"]
        for row in positive_rows
        for packet in row["packet_rows"]
    })
    envelope = adverse_envelope(positive_rows, labels)
    best_by_size, counts, minimal = best_cores_by_size(
        positive_rows, labels, envelope)
    if minimal is None:
        raise AssertionError("expected at least the full packet set to certify")
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "support_packet_budget": str(SOURCE.relative_to(ROOT)),
            "support_packet_budget_source_commit": source["source_commit"],
        },
        "status": "HOLD_minimal_rescue_core_is_near_sharp_finite_fit",
        "status_boundary": (
            "finite rescue-core theorem-budget audit only; no rescue-core "
            "theorem, support-packet theorem, character-sum theorem, signed "
            "binary-prime correlation theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "rescue_core_theorem_proved": False,
        "support_packet_theorem_proved": False,
        "signed_binary_prime_correlation_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "fixed signed rescue core plus adverse packet tail",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Keep a fixed subset of support packets with signed action, "
                "and pay every omitted packet by its worst observed adverse "
                "value on the positive finite rows."),
            "prediction": (
                "If a small fixed core carries the useful signed structure, "
                "some low-cardinality subset should certify every positive row "
                "with meaningful margin after the adverse tail is paid."),
            "falsifier": (
                "If no small subset certifies, or if the first certifying "
                "subset has only near-zero margin and a fitted tail envelope, "
                "then the smaller core is not yet a robust theorem route."),
            "smallest_test": (
                "Brute-force all fixed support-packet cores and evaluate "
                "aligned + signed_core - adverse_tail_envelope on the five "
                "actual full-positive frozen rows."),
        },
        "positive_row_count": len(positive_rows),
        "packet_labels": labels,
        "positive_row_adverse_envelope": envelope,
        "certifying_core_count_by_size": counts,
        "best_core_by_size": best_by_size,
        "minimal_certifying_core": minimal,
        "summary": {
            "minimum_certifying_core_size": minimal["core_size"],
            "minimal_certifying_core": minimal["core"],
            "minimal_core_tail_packet_count": minimal["tail_packet_count"],
            "minimal_core_tail_adverse_envelope": (
                minimal["tail_adverse_envelope"]),
            "minimal_core_minimum_margin": minimal["minimum_margin"],
            "minimal_core_tight_target": minimal["tight_row"]["target"],
            "minimal_core_tight_relative_budget": (
                minimal["tight_row"][
                    "core_relative_error_budget_with_tail_exact"]),
            "certifying_core_counts_through_size_5": {
                str(size): counts[str(size)] for size in range(6)
            },
            "best_margin_by_size_through_5": [
                {
                    "core_size": row["core_size"],
                    "core": row["core"],
                    "minimum_margin": row["minimum_margin"],
                    "all_positive_rows_certified": (
                        row["all_positive_rows_certified"]),
                }
                for row in best_by_size[:6]
            ],
            "minimal_core_relative_budget_summary": finite_summary(
                result["core_relative_error_budget_with_tail_exact"]
                for result in minimal["row_results"]),
        },
        "decision": (
            "A fixed rescue core exists, but it is near-sharp and finite-fit.  "
            "No core of size 0 through 4 certifies all five positive rows.  "
            "Exactly one size-5 core certifies them: 11x13, 5, 5x7, 5x7x13, "
            "and 7.  Its tight row is again target 94856, with margin about "
            "0.0005799 and a relative core budget about 0.01023 when the "
            "adverse tail envelope is treated as exact.  This narrows the "
            "signed packet route to a possible positive-rescue theorem, but "
            "it does not provide a robust universal bridge: the tail envelope "
            "is fitted to the finite positive rows and the tight margin is "
            "near sub-percent.  The next proof object must either give a "
            "source-backed lower bound for this rescue core plus a universal "
            "adverse-tail bound, or abandon the small-core route for a broader "
            "signed packet package.  Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
