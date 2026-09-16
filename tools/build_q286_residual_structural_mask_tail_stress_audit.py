"""Stress the q286 structural support-mask adverse-tail envelope.

The structural-mask audit found a seven-packet two-subcube mask that certifies
the five positive rows when the omitted tail is bounded by an adverse envelope
fitted only on those positive rows.  This receipt asks whether that tail bound
survives a harsher all-row stress envelope over the seven frozen signed-pair
operator targets.

Finite theorem-budget audit only.  It proves no structural-mask theorem,
tail-bound theorem, support-packet theorem, character-sum theorem, signed
binary-prime correlation theorem, q286 threshold theorem, strict-central
Goldbach theorem, or Goldbach proof.
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
MASK_SOURCE = (
    EVIDENCE / "q286-residual-support-packet-structural-mask-audit.json")
OUT = EVIDENCE / "q286-residual-structural-mask-tail-stress-audit.json"
PRIMES = ("5", "7", "11", "13")
TOLERANCE = 1e-10


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def support_bits(label):
    support = set(label.split("x"))
    return tuple(prime in support for prime in PRIMES)


def sorted_labels(labels):
    return sorted(labels, key=lambda label: (sum(support_bits(label)),
                                            support_bits(label)))


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


def evaluate_mask(mask, labels, envelope, evaluation_rows):
    mask = set(mask)
    tail_labels = [label for label in labels if label not in mask]
    tail_envelope = math.fsum(envelope[label] for label in tail_labels)
    rows = []
    for row in evaluation_rows:
        signed = math.fsum(packet_action(row, label) for label in mask)
        absolute = math.fsum(abs(packet_action(row, label)) for label in mask)
        margin = row["aligned_only_full_action"] + signed - tail_envelope
        rows.append({
            "target": row["target"],
            "actual_full_positive": row["actual_full_positive"],
            "aligned_only_full_action": row["aligned_only_full_action"],
            "mask_signed_action": signed,
            "mask_abs_action": absolute,
            "tail_adverse_envelope": tail_envelope,
            "tail_stress_margin": margin,
            "relative_budget_with_tail_exact": (
                margin / absolute if absolute > TOLERANCE else None),
            "certified": bool(margin > TOLERANCE),
        })
    tight = min(rows, key=lambda item: (item["tail_stress_margin"],
                                       item["target"]))
    return {
        "mask": sorted_labels(mask),
        "tail_labels": sorted_labels(tail_labels),
        "tail_adverse_envelope": tail_envelope,
        "minimum_margin": tight["tail_stress_margin"],
        "tight_row": tight,
        "certified_positive_row_count": sum(
            item["certified"] for item in rows
            if item["actual_full_positive"]),
        "positive_row_count": sum(
            item["actual_full_positive"] for item in rows),
        "all_positive_rows_certified": all(
            item["certified"] for item in rows
            if item["actual_full_positive"]),
        "row_results": rows,
    }


def build_receipt():
    support = load_json(SUPPORT_SOURCE)
    structural = load_json(MASK_SOURCE)
    all_rows = support["target_rows"]
    positive_rows = [row for row in all_rows if row["actual_full_positive"]]
    labels = sorted_labels({
        packet["support_label"]
        for row in all_rows
        for packet in row["packet_rows"]
    })
    positive_envelope = adverse_envelope(positive_rows, labels)
    all_envelope = adverse_envelope(all_rows, labels)
    two_subcube = structural["summary"][
        "smallest_two_subcube_certifying_mask"]["mask"]
    support_size_le_2 = structural["summary"]["support_size_le_2_mask"][
        "mask"]
    rows = []
    for name, mask in (
            ("two_subcube", two_subcube),
            ("support_size_le_2", support_size_le_2),
            ("full_15_packet", labels),
    ):
        rows.append({
            "name": name,
            "positive_row_tail": evaluate_mask(
                mask, labels, positive_envelope, positive_rows),
            "all_row_tail": evaluate_mask(
                mask, labels, all_envelope, positive_rows),
            "all_row_tail_on_all_targets": evaluate_mask(
                mask, labels, all_envelope, all_rows),
        })
    two = next(row for row in rows if row["name"] == "two_subcube")
    le2 = next(row for row in rows if row["name"] == "support_size_le_2")
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "support_packet_budget": str(SUPPORT_SOURCE.relative_to(ROOT)),
            "support_packet_budget_source_commit": support["source_commit"],
            "structural_mask_audit": str(MASK_SOURCE.relative_to(ROOT)),
            "structural_mask_source_commit": structural["source_commit"],
        },
        "status": "HOLD_all_row_tail_envelope_breaks_structural_masks",
        "status_boundary": (
            "finite structural-mask tail-stress audit only; no structural-"
            "mask theorem, tail-bound theorem, support-packet theorem, "
            "character-sum theorem, signed binary-prime correlation theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"),
        "goldbach_proved": False,
        "structural_mask_theorem_proved": False,
        "tail_bound_theorem_proved": False,
        "signed_binary_prime_correlation_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "unqualified structural-mask adverse-tail theorem",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Keep the structural support mask from the previous receipt, "
                "but replace the positive-row fitted adverse tail by a harsher "
                "componentwise envelope over all seven frozen rows."),
            "prediction": (
                "If the structural mask has a robust universal tail theorem "
                "shape, the all-row adverse envelope should still leave the "
                "positive rows certified, or at least remain close enough to "
                "identify a plausible slack target."),
            "falsifier": (
                "If the all-row envelope turns the tight positive row strongly "
                "negative, then an unqualified adverse-tail supremum is too "
                "broad; the route needs a mathematically defined positive "
                "class, signed tail control, or the full signed packet package."),
            "smallest_test": (
                "Evaluate the two-subcube and support-size <=2 masks with "
                "positive-row versus all-row adverse envelopes on the frozen "
                "support-packet rows."),
        },
        "positive_row_count": len(positive_rows),
        "all_target_count": len(all_rows),
        "mask_rows": rows,
        "summary": {
            "two_subcube_positive_tail_margin": (
                two["positive_row_tail"]["minimum_margin"]),
            "two_subcube_all_tail_margin": (
                two["all_row_tail"]["minimum_margin"]),
            "two_subcube_positive_tail_envelope": (
                two["positive_row_tail"]["tail_adverse_envelope"]),
            "two_subcube_all_tail_envelope": (
                two["all_row_tail"]["tail_adverse_envelope"]),
            "two_subcube_tail_envelope_increase": (
                two["all_row_tail"]["tail_adverse_envelope"]
                - two["positive_row_tail"]["tail_adverse_envelope"]),
            "two_subcube_tight_target": (
                two["all_row_tail"]["tight_row"]["target"]),
            "support_size_le_2_positive_tail_margin": (
                le2["positive_row_tail"]["minimum_margin"]),
            "support_size_le_2_all_tail_margin": (
                le2["all_row_tail"]["minimum_margin"]),
            "support_size_le_2_positive_tail_envelope": (
                le2["positive_row_tail"]["tail_adverse_envelope"]),
            "support_size_le_2_all_tail_envelope": (
                le2["all_row_tail"]["tail_adverse_envelope"]),
        },
        "decision": (
            "The structural support masks do not survive an unqualified "
            "all-row adverse-tail envelope.  For the seven-packet two-subcube "
            "mask, the fitted positive-row tail is about 0.16919 and leaves "
            "target 94856 with margin about +0.00550.  The all-row envelope "
            "jumps to about 0.51320 and drives the same target to about "
            "-0.33851.  The support-size <=2 mask similarly falls from about "
            "+0.00402 to about -0.18722.  Thus the previous structural mask "
            "remains useful only if the tail theorem is restricted to a "
            "mathematically defined positive/stable class, uses signed tail "
            "control, or is replaced by the broader signed packet package.  "
            "Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
