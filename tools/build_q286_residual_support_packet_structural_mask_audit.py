"""Audit structural masks for the q286 residual support-packet route.

The minimal five-packet rescue core is unique but near-sharp.  This receipt
asks whether a more theorem-shaped support-lattice rule can replace that
hand-picked finite mask.

Finite theorem-budget audit only.  It proves no structural-mask theorem,
support-packet theorem, character-sum theorem, signed binary-prime correlation
theorem, q286 threshold theorem, strict-central Goldbach theorem, or Goldbach
proof.
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
RESCUE_SOURCE = EVIDENCE / "q286-residual-support-packet-rescue-core-audit.json"
OUT = EVIDENCE / "q286-residual-support-packet-structural-mask-audit.json"
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


def evaluate_mask(rows, labels, envelope, mask, name=None, rule=None):
    mask = frozenset(mask)
    tail_envelope = math.fsum(
        envelope[label] for label in labels if label not in mask)
    row_results = []
    for row in rows:
        signed = math.fsum(packet_action(row, label) for label in mask)
        absolute = math.fsum(abs(packet_action(row, label)) for label in mask)
        margin = row["aligned_only_full_action"] + signed - tail_envelope
        row_results.append({
            "target": row["target"],
            "aligned_only_full_action": row["aligned_only_full_action"],
            "mask_signed_action": signed,
            "mask_abs_action": absolute,
            "tail_adverse_envelope": tail_envelope,
            "structural_mask_margin": margin,
            "mask_relative_error_budget_with_tail_exact": (
                margin / absolute if absolute > TOLERANCE else None),
            "certified": bool(margin > TOLERANCE),
        })
    tight = min(
        row_results,
        key=lambda result: (result["structural_mask_margin"],
                            result["target"]))
    return {
        "name": name,
        "rule": rule,
        "mask": sorted_labels(mask),
        "mask_size": len(mask),
        "tail_packet_count": len(labels) - len(mask),
        "tail_adverse_envelope": tail_envelope,
        "minimum_margin": tight["structural_mask_margin"],
        "certified_positive_row_count": sum(
            result["certified"] for result in row_results),
        "all_positive_rows_certified": all(
            result["certified"] for result in row_results),
        "tight_row": tight,
        "row_results": row_results,
    }


def subcube_mask(labels, pattern):
    selected = []
    for label in labels:
        bits = support_bits(label)
        ok = True
        for bit, requirement in zip(bits, pattern):
            if requirement == 1 and not bit:
                ok = False
            if requirement == -1 and bit:
                ok = False
        if ok:
            selected.append(label)
    return frozenset(selected)


def pattern_text(pattern):
    parts = []
    for prime, requirement in zip(PRIMES, pattern):
        if requirement == 1:
            parts.append(f"{prime}=1")
        elif requirement == -1:
            parts.append(f"{prime}=0")
    return "all" if not parts else " and ".join(parts)


def dnf_masks(labels, term_count):
    subcubes = []
    for pattern in itertools.product((-1, 0, 1), repeat=len(PRIMES)):
        mask = subcube_mask(labels, pattern)
        if mask:
            subcubes.append((pattern, mask))
    masks = {}
    for combo in itertools.combinations(range(len(subcubes)), term_count):
        mask = frozenset().union(*(subcubes[index][1] for index in combo))
        if mask and mask not in masks:
            masks[mask] = tuple(subcubes[index][0] for index in combo)
    return masks


def scan_dnf(rows, labels, envelope, term_count):
    masks = dnf_masks(labels, term_count)
    certified = []
    best = None
    for mask, patterns in masks.items():
        result = evaluate_mask(
            rows,
            labels,
            envelope,
            mask,
            name=f"best_{term_count}_subcube_dnf_candidate",
            rule=" OR ".join(f"({pattern_text(pattern)})"
                             for pattern in patterns),
        )
        result["subcube_patterns"] = [list(pattern) for pattern in patterns]
        if best is None or (
                result["minimum_margin"], result["mask_size"]) > (
                    best["minimum_margin"], best["mask_size"]):
            best = result
        if result["all_positive_rows_certified"]:
            certified.append(result)
    smallest = None
    if certified:
        smallest = min(
            certified,
            key=lambda result: (result["mask_size"],
                                -result["minimum_margin"],
                                result["mask"]))
    return {
        "term_count": term_count,
        "mask_count": len(masks),
        "certifying_mask_count": len(certified),
        "best_margin_mask": best,
        "smallest_certifying_mask": smallest,
    }


def weight_mask(labels, relation, threshold):
    if relation == "<=":
        return [label for label in labels
                if sum(support_bits(label)) <= threshold]
    if relation == ">=":
        return [label for label in labels
                if sum(support_bits(label)) >= threshold]
    raise ValueError(relation)


def monotone_violations(mask, labels, direction):
    mask = set(mask)
    violations = []
    for label in mask:
        label_set = {index for index, bit in enumerate(support_bits(label))
                     if bit}
        for other in labels:
            other_set = {
                index for index, bit in enumerate(support_bits(other)) if bit}
            if direction == "down" and other_set < label_set and other not in mask:
                violations.append([label, other])
            if direction == "up" and label_set < other_set and other not in mask:
                violations.append([label, other])
    return violations


def build_receipt():
    source = load_json(SOURCE)
    rescue = load_json(RESCUE_SOURCE)
    rows = [row for row in source["target_rows"] if row["actual_full_positive"]]
    labels = sorted_labels({
        packet["support_label"] for row in rows for packet in row["packet_rows"]
    })
    envelope = adverse_envelope(rows, labels)
    dnf1 = scan_dnf(rows, labels, envelope, 1)
    dnf2 = scan_dnf(rows, labels, envelope, 2)
    dnf3 = scan_dnf(rows, labels, envelope, 3)
    weight_rows = []
    for relation in ("<=", ">="):
        for threshold in range(1, len(PRIMES) + 1):
            mask = weight_mask(labels, relation, threshold)
            weight_rows.append(evaluate_mask(
                rows,
                labels,
                envelope,
                mask,
                name=f"support_size_{relation}_{threshold}",
                rule=f"support size {relation} {threshold}",
            ))
    minimal_core = rescue["summary"]["minimal_certifying_core"]
    minimal_core_row = evaluate_mask(
        rows,
        labels,
        envelope,
        minimal_core,
        name="minimal_arbitrary_rescue_core",
        rule="unique size-5 finite core from rescue-core audit",
    )
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "support_packet_budget": str(SOURCE.relative_to(ROOT)),
            "support_packet_budget_source_commit": source["source_commit"],
            "rescue_core_audit": str(RESCUE_SOURCE.relative_to(ROOT)),
            "rescue_core_source_commit": rescue["source_commit"],
        },
        "status": "CANDIDATE_two_subcube_structural_mask_survives_finitely",
        "status_boundary": (
            "finite structural-mask theorem-budget audit only; no structural-"
            "mask theorem, support-packet theorem, character-sum theorem, "
            "signed binary-prime correlation theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "structural_mask_theorem_proved": False,
        "support_packet_theorem_proved": False,
        "signed_binary_prime_correlation_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "two-subcube support-lattice rescue mask",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Replace the unique five-packet arbitrary core by a fixed "
                "Boolean rule on support factors.  Keep packets satisfying "
                "(11 present and 7 absent) OR (11 absent and 13 absent), and "
                "pay the omitted packets by the positive-row adverse envelope."),
            "prediction": (
                "If the rescue-core phenomenon has theorem shape, a simple "
                "support-lattice mask should certify the same positive rows "
                "with a less brittle margin than the unique five-packet core."),
            "falsifier": (
                "If every low-complexity support-lattice family fails or only "
                "the full 15-packet mask certifies, the rescue core is likely "
                "a finite fitted selection rather than a structural route."),
            "smallest_test": (
                "Enumerate one-, two-, and three-subcube DNF masks on the "
                "four support factors, plus support-size threshold masks, and "
                "compare certification margins on the five positive rows."),
        },
        "positive_row_count": len(rows),
        "packet_labels": labels,
        "positive_row_adverse_envelope": envelope,
        "minimal_arbitrary_rescue_core": minimal_core_row,
        "minimal_core_closure_violations": {
            "downward": monotone_violations(minimal_core, labels, "down"),
            "upward": monotone_violations(minimal_core, labels, "up"),
        },
        "dnf_scans": {
            "one_subcube": dnf1,
            "two_subcube": dnf2,
            "three_subcube": dnf3,
        },
        "support_size_threshold_masks": weight_rows,
        "summary": {
            "minimal_arbitrary_core_margin": (
                minimal_core_row["minimum_margin"]),
            "minimal_arbitrary_core_relative_budget": (
                minimal_core_row["tight_row"][
                    "mask_relative_error_budget_with_tail_exact"]),
            "minimal_core_downward_violation_count": len(
                monotone_violations(minimal_core, labels, "down")),
            "minimal_core_upward_violation_count": len(
                monotone_violations(minimal_core, labels, "up")),
            "one_subcube_certifying_mask_count": (
                dnf1["certifying_mask_count"]),
            "two_subcube_certifying_mask_count": (
                dnf2["certifying_mask_count"]),
            "smallest_two_subcube_certifying_mask": (
                dnf2["smallest_certifying_mask"]),
            "support_size_le_2_mask": next(
                row for row in weight_rows
                if row["name"] == "support_size_<=_2"),
        },
        "decision": (
            "The unique five-packet rescue core is not closure-natural: it has "
            "both downward and upward support-lattice violations.  A better "
            "finite theorem-shaped object exists, though still only finitely.  "
            "No nontrivial one-subcube mask certifies all five positive rows; "
            "the only one-subcube certificate is the full 15-packet mask.  "
            "Among two-subcube masks, the smallest certifying rule keeps seven "
            "packets, namely (11 present and 7 absent) OR (11 absent and 13 "
            "absent), and its tight margin at target 94856 is about 0.00550 "
            "with relative core budget about 0.09076.  The natural support-"
            "size <= 2 mask also certifies, with tight margin about 0.00402.  "
            "This promotes the next finite target from an arbitrary five-"
            "packet core to a structural support-lattice mask.  It still "
            "proves no theorem because the adverse tail envelope is fitted to "
            "the five positive rows and no source-backed signed correlation "
            "estimate is established.  Goldbach remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
