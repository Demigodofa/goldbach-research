"""Audit the q286 residual support-order sign bridge.

The signed-tail bridge made the support-size <= 2 mask the cleaner finite
target.  This receipt asks whether that split has a non-circular shape: does
the low-order base, aligned plus support packets of order at most two, already
separate the frozen positive and nonpositive rows before the high-order tail
is added?

Finite bridge audit only.  It proves no low-order base theorem, high-order
tail domination theorem, signed packet theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SUPPORT_SOURCE = (
    EVIDENCE / "q286-residual-character-support-packet-budget-audit.json")
SIGNED_TAIL_SOURCE = (
    EVIDENCE / "q286-residual-structural-mask-signed-tail-bridge-audit.json")
OUT = EVIDENCE / "q286-residual-support-order-sign-bridge-audit.json"
TOLERANCE = 1e-10


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def support_order(label):
    return len(label.split("x"))


def evaluate_row(row):
    low_order_signed = 0.0
    low_order_abs = 0.0
    high_order_signed = 0.0
    high_order_abs = 0.0
    low_order_labels = []
    high_order_labels = []
    for packet in row["packet_rows"]:
        value = float(packet["signed_packet_action"])
        label = packet["support_label"]
        if support_order(label) <= 2:
            low_order_signed += value
            low_order_abs += abs(value)
            low_order_labels.append(label)
        else:
            high_order_signed += value
            high_order_abs += abs(value)
            high_order_labels.append(label)

    aligned = float(row["aligned_only_full_action"])
    low_order_base = aligned + low_order_signed
    full = float(row["actual_full_action"])
    reconstruction_error = low_order_base + high_order_signed - full
    base_positive = low_order_base > TOLERANCE
    full_positive = bool(row["actual_full_positive"])
    adverse_ratio = None
    if base_positive and high_order_signed < -TOLERANCE:
        adverse_ratio = -high_order_signed / low_order_base
    abs_ratio = None
    if base_positive and high_order_abs > TOLERANCE:
        abs_ratio = high_order_abs / low_order_base
    return {
        "target": int(row["target"]),
        "target_mod_286": int(row["target_mod_286"]),
        "target_residue": int(row["target_residue"]),
        "actual_full_action": full,
        "actual_full_positive": full_positive,
        "aligned_only_full_action": aligned,
        "low_order_signed_action": low_order_signed,
        "low_order_abs_action": low_order_abs,
        "low_order_base_action": low_order_base,
        "low_order_base_positive": base_positive,
        "high_order_signed_tail": high_order_signed,
        "high_order_abs_tail": high_order_abs,
        "high_order_tail_is_adverse": bool(high_order_signed < -TOLERANCE),
        "high_order_adverse_to_base_ratio": adverse_ratio,
        "high_order_abs_to_base_ratio": abs_ratio,
        "signed_reconstruction_error": reconstruction_error,
        "low_order_labels": sorted(low_order_labels),
        "high_order_labels": sorted(high_order_labels),
        "low_order_base_sign_matches_full_sign": bool(
            base_positive == full_positive),
    }


def finite_summary(values):
    values = list(values)
    if not values:
        return None
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": math.fsum(values) / len(values),
    }


def build_receipt():
    support = load_json(SUPPORT_SOURCE)
    signed_tail = load_json(SIGNED_TAIL_SOURCE)
    rows = [evaluate_row(row) for row in support["target_rows"]]
    positive_rows = [row for row in rows if row["actual_full_positive"]]
    nonpositive_rows = [row for row in rows if not row["actual_full_positive"]]
    base_positive_rows = [row for row in rows if row["low_order_base_positive"]]
    mismatches = [
        row for row in rows
        if not row["low_order_base_sign_matches_full_sign"]
    ]
    adverse_base_positive_rows = [
        row for row in base_positive_rows
        if row["high_order_adverse_to_base_ratio"] is not None
    ]
    tight_base = min(
        positive_rows,
        key=lambda row: (row["low_order_base_action"], row["target"]),
    )
    closest_nonpositive_base = max(
        nonpositive_rows,
        key=lambda row: (row["low_order_base_action"], -row["target"]),
    )
    tight_tail_domination = max(
        adverse_base_positive_rows,
        key=lambda row: (
            row["high_order_adverse_to_base_ratio"], -row["target"]),
    )
    tight_abs_domination = max(
        base_positive_rows,
        key=lambda row: (row["high_order_abs_to_base_ratio"] or -1.0,
                         -row["target"]),
    )
    all_row_high_order_adverse_envelope = max(
        max(0.0, -row["high_order_signed_tail"]) for row in rows)
    all_row_envelope_margin_at_tight_base = (
        tight_base["low_order_base_action"]
        - all_row_high_order_adverse_envelope)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "support_packet_budget": str(SUPPORT_SOURCE.relative_to(ROOT)),
            "support_packet_budget_source_commit": support["source_commit"],
            "signed_tail_bridge": str(SIGNED_TAIL_SOURCE.relative_to(ROOT)),
            "signed_tail_bridge_status": signed_tail["status"],
        },
        "status": "CANDIDATE_support_order_sign_bridge_survives_fixture",
        "status_boundary": (
            "finite support-order sign bridge audit only; no low-order base "
            "theorem, high-order tail domination theorem, signed packet "
            "theorem, q286 threshold theorem, strict-central Goldbach theorem, "
            "or Goldbach proof"),
        "goldbach_proved": False,
        "low_order_base_theorem_proved": False,
        "high_order_tail_domination_theorem_proved": False,
        "signed_packet_theorem_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "universal_bound_open": True,
        "acceptance_condition": {
            "finite_evidence_is_acceptance_condition": False,
            "required_acceptance_condition": (
                "for every sufficiently large eligible even N, prove the "
                "low-order base is positive and the high-order support tail "
                "is greater than the negative of that base, or prove an "
                "equivalent pointwise signed lower bound"),
            "target": (
                "LowOrderBase(N) + HighOrderTail(N) > 0, hence "
                "AdverseDrag(N) < LocalMain(N) in the q286 residual scale"),
        },
        "candidate": {
            "name": "support-order low-base plus high-tail domination",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Filter support packets by conductor-support order.  The "
                "low-order base keeps the aligned term plus all support "
                "packets of size one or two; the high-order tail is the "
                "signed sum over support sizes three and four."),
            "prediction": (
                "If support-size <=2 is a theorem-shaped split, the low-order "
                "base should separate the frozen positive rows from the "
                "nonpositive stress rows before the high-order tail is added, "
                "and the high-order tail should consume less than the positive "
                "base on selected rows."),
            "falsifier": (
                "A sign mismatch between low-order base and full action, or "
                "an adverse high-order tail at least as large as the positive "
                "low-order base, breaks this bridge on the fixture."),
            "smallest_test": (
                "Compute low-order base, high-order signed tail, and tail-to-"
                "base ratios on the seven frozen support-packet rows."),
        },
        "support_order_convention": {
            "low_order": "support size <= 2",
            "high_order_tail": "support size >= 3",
            "low_order_base": (
                "aligned_only_full_action + sum signed_packet_action over "
                "support size <= 2"),
            "high_order_tail_domination_sufficient_condition": (
                "high_order_signed_tail > -low_order_base"),
        },
        "rows": rows,
        "summary": {
            "row_count": len(rows),
            "actual_full_positive_count": len(positive_rows),
            "actual_full_nonpositive_count": len(nonpositive_rows),
            "low_order_base_positive_count": len(base_positive_rows),
            "low_order_base_sign_mismatch_count": len(mismatches),
            "low_order_base_sign_mismatch_targets": [
                row["target"] for row in mismatches],
            "low_order_base_summary_on_positive_rows": finite_summary(
                row["low_order_base_action"] for row in positive_rows),
            "low_order_base_summary_on_nonpositive_rows": finite_summary(
                row["low_order_base_action"] for row in nonpositive_rows),
            "high_order_signed_tail_summary_on_positive_rows": finite_summary(
                row["high_order_signed_tail"] for row in positive_rows),
            "high_order_abs_tail_summary_on_positive_rows": finite_summary(
                row["high_order_abs_tail"] for row in positive_rows),
            "tight_low_order_base_positive_row": tight_base,
            "closest_nonpositive_low_order_base_row": (
                closest_nonpositive_base),
            "tight_high_order_adverse_to_base_row": (
                tight_tail_domination),
            "tight_high_order_abs_to_base_row": tight_abs_domination,
            "maximum_high_order_adverse_to_base_ratio_on_base_positive_rows": (
                tight_tail_domination["high_order_adverse_to_base_ratio"]),
            "maximum_high_order_abs_to_base_ratio_on_base_positive_rows": (
                tight_abs_domination["high_order_abs_to_base_ratio"]),
            "all_row_high_order_adverse_envelope": (
                all_row_high_order_adverse_envelope),
            "all_row_high_order_envelope_margin_at_tight_positive_base": (
                all_row_envelope_margin_at_tight_base),
            "maximum_reconstruction_error": max(
                abs(row["signed_reconstruction_error"]) for row in rows),
        },
        "decision": (
            "The support-order split survives the seven-row fixture as a "
            "candidate bridge.  The low-order base sign agrees with the full "
            "action sign on all seven frozen rows: five base-positive rows are "
            "the five full-positive rows, and the two nonpositive stress rows "
            "are base-negative.  The tight positive row is target 94856, with "
            "low-order base about 0.05371 and high-order signed tail about "
            "-0.04113, so the adverse high-order tail consumes about 76.58% "
            "of the base and leaves full action about 0.01258.  An "
            "unqualified all-row high-order adverse envelope still fails: the "
            "worst high-order adverse tail over all rows is about 0.23468, "
            "well above the tight positive base.  Thus the next theorem target "
            "is not a global adverse envelope; it is a pointwise low-order "
            "base positivity theorem plus a high-order signed-tail domination "
            "theorem on the same mathematically named class.  Goldbach remains "
            "open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
