"""Audit the signed-tail bridge after structural-mask adverse-tail failure.

The previous structural-mask stress receipt rejected an unqualified all-row
adverse-tail envelope.  This receipt asks what survives if the tail is kept as
a signed object instead of being replaced by disconnected adverse suprema.

Finite bridge audit only.  It proves no signed-tail theorem, non-circular L2
bridge, structural-mask theorem, q286 threshold theorem, strict-central
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
STRUCTURAL_SOURCE = (
    EVIDENCE / "q286-residual-support-packet-structural-mask-audit.json")
TAIL_STRESS_SOURCE = (
    EVIDENCE / "q286-residual-structural-mask-tail-stress-audit.json")
L2_OBSERVED_SOURCE = (
    EVIDENCE / "q286-wbss-multiplicative-character-l2-observed-moment-audit.json")
OUT = (
    EVIDENCE / "q286-residual-structural-mask-signed-tail-bridge-audit.json")
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


def evaluate_mask(rows, labels, mask, name, rule):
    mask = set(mask)
    tail_labels = [label for label in labels if label not in mask]
    evaluated = []
    for row in rows:
        mask_signed = math.fsum(packet_action(row, label) for label in mask)
        mask_abs = math.fsum(abs(packet_action(row, label)) for label in mask)
        tail_signed = math.fsum(
            packet_action(row, label) for label in tail_labels)
        tail_abs = math.fsum(
            abs(packet_action(row, label)) for label in tail_labels)
        reconstructed = (
            float(row["aligned_only_full_action"]) + mask_signed
            + tail_signed)
        full = float(row["actual_full_action"])
        tail_budget = None
        if row["actual_full_positive"] and tail_abs > TOLERANCE:
            tail_budget = full / tail_abs
        evaluated.append({
            "target": int(row["target"]),
            "target_mod_286": int(row["target_mod_286"]),
            "target_residue": int(row["target_residue"]),
            "actual_full_action": full,
            "actual_full_positive": bool(row["actual_full_positive"]),
            "aligned_only_full_action": float(
                row["aligned_only_full_action"]),
            "mask_signed_action": mask_signed,
            "mask_abs_action": mask_abs,
            "tail_signed_action": tail_signed,
            "tail_abs_action": tail_abs,
            "signed_reconstruction_error": reconstructed - full,
            "tail_is_adverse": bool(tail_signed < -TOLERANCE),
            "signed_tail_relative_error_budget_with_aligned_mask_exact": (
                tail_budget),
        })

    positive = [row for row in evaluated if row["actual_full_positive"]]
    adverse_positive = [row for row in positive if row["tail_is_adverse"]]
    rows_with_budget = [
        row for row in positive
        if row["signed_tail_relative_error_budget_with_aligned_mask_exact"]
        is not None
    ]
    tight = None
    if rows_with_budget:
        tight = min(
            rows_with_budget,
            key=lambda row: (
                row[
                    "signed_tail_relative_error_budget_with_aligned_mask_exact"
                ],
                row["target"]),
        )
    elif positive:
        tight = min(
            positive,
            key=lambda row: (row["actual_full_action"], row["target"]))
    return {
        "name": name,
        "rule": rule,
        "mask": sorted_labels(mask),
        "tail_labels": sorted_labels(tail_labels),
        "mask_size": len(mask),
        "tail_packet_count": len(tail_labels),
        "positive_row_count": len(positive),
        "positive_rows_with_adverse_signed_tail": len(adverse_positive),
        "minimum_positive_signed_tail_budget": (
            tight["signed_tail_relative_error_budget_with_aligned_mask_exact"]
            if tight else None),
        "tight_positive_signed_tail_budget_row": tight,
        "maximum_reconstruction_error": max(
            abs(row["signed_reconstruction_error"]) for row in evaluated),
        "row_results": evaluated,
    }


def build_receipt():
    support = load_json(SUPPORT_SOURCE)
    structural = load_json(STRUCTURAL_SOURCE)
    tail_stress = load_json(TAIL_STRESS_SOURCE)
    l2_observed = load_json(L2_OBSERVED_SOURCE)
    rows = support["target_rows"]
    positive_rows = [row for row in rows if row["actual_full_positive"]]
    labels = sorted_labels({
        packet["support_label"]
        for row in rows
        for packet in row["packet_rows"]
    })

    two_subcube = structural["summary"][
        "smallest_two_subcube_certifying_mask"]["mask"]
    support_size_le_2 = structural["summary"]["support_size_le_2_mask"][
        "mask"]

    mask_rows = [
        evaluate_mask(
            rows,
            labels,
            two_subcube,
            "two_subcube",
            "(7=0 and 11=1) OR (11=0 and 13=0)",
        ),
        evaluate_mask(
            rows,
            labels,
            support_size_le_2,
            "support_size_le_2",
            "support size <= 2",
        ),
        evaluate_mask(
            rows,
            labels,
            labels,
            "full_15_packet",
            "all support packets retained; no tail",
        ),
    ]
    two = next(row for row in mask_rows if row["name"] == "two_subcube")
    le2 = next(row for row in mask_rows if row["name"] == "support_size_le_2")
    full = next(row for row in mask_rows if row["name"] == "full_15_packet")
    l2_summary = l2_observed["summary"]

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "support_packet_budget": str(SUPPORT_SOURCE.relative_to(ROOT)),
            "support_packet_budget_source_commit": support["source_commit"],
            "structural_mask_audit": str(STRUCTURAL_SOURCE.relative_to(ROOT)),
            "structural_mask_source_commit": structural["source_commit"],
            "tail_stress_audit": str(TAIL_STRESS_SOURCE.relative_to(ROOT)),
            "tail_stress_status": tail_stress["status"],
            "l2_observed_moment_audit": str(
                L2_OBSERVED_SOURCE.relative_to(ROOT)),
            "l2_observed_status": l2_observed["status"],
        },
        "status": "HOLD_signed_tail_bridge_requires_external_pointwise_theorem",
        "status_boundary": (
            "finite signed-tail bridge audit only; no signed-tail theorem, "
            "non-circular aggregate L2 bridge, structural-mask theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"),
        "goldbach_proved": False,
        "signed_tail_theorem_proved": False,
        "structural_mask_theorem_proved": False,
        "non_circular_l2_bridge_confirmed": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "universal_bound_open": True,
        "acceptance_condition": {
            "finite_evidence_is_acceptance_condition": False,
            "required_acceptance_condition": (
                "a universal pointwise unnormalized analytic estimate, on a "
                "mathematically named class, proving the signed/adverse "
                "residual contribution is smaller than the local main for "
                "every sufficiently large eligible even N"),
            "target": "AdverseDrag(N) < LocalMain(N)",
            "non_circular_bridge_status": (
                "not confirmed; the arithmetic decompositions and zero-mass "
                "checks are useful diagnostics, but an external pointwise "
                "twisted binary-prime estimate is still missing"),
        },
        "zero_mass_check": {
            "source": str(L2_OBSERVED_SOURCE.relative_to(ROOT)),
            "row_count": l2_summary["row_count"],
            "zero_pair_count": l2_summary["zero_pair_count"],
            "zero_actual_mass_count": l2_summary["zero_actual_mass_count"],
            "nonunit_actual_mass_sum_count": (
                l2_summary["nonunit_actual_mass_sum_count"]),
            "nonunit_uniform_mass_sum_count": (
                l2_summary["nonunit_uniform_mass_sum_count"]),
            "decision": (
                "The prior q286-WBSS L2 observed-moment audit did confirm no "
                "zero strict-central pair mass on its 348 checked rows.  That "
                "removes a normalization defect, but it does not confirm the "
                "non-circular analytic bridge."),
        },
        "candidate": {
            "name": "signed structural-tail pointwise theorem target",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "After the all-row adverse-tail envelope fails, keep the "
                "structural mask and omitted tail as signed packet sums.  The "
                "finite row budget measures how accurately a future pointwise "
                "signed-tail theorem would need to control the omitted tail."),
            "prediction": (
                "The signed-tail budget should be materially better than the "
                "failed all-row adverse envelope, and it should identify "
                "whether the two-subcube mask or the support-size <=2 mask is "
                "the cleaner theorem target."),
            "falsifier": (
                "If the signed-tail budget is sub-percent or worse than the "
                "full 15-packet signed budget, the structural split is not "
                "earning its keep as a proof target."),
            "smallest_test": (
                "For each structural mask, compute the exact signed omitted "
                "tail on the seven frozen rows and the relative error budget "
                "full_action / abs(tail) on positive rows."),
        },
        "mask_rows": mask_rows,
        "summary": {
            "positive_row_count": len(positive_rows),
            "two_subcube_all_row_adverse_tail_margin": (
                tail_stress["summary"]["two_subcube_all_tail_margin"]),
            "two_subcube_signed_tail_budget": (
                two["minimum_positive_signed_tail_budget"]),
            "two_subcube_tight_target": (
                two["tight_positive_signed_tail_budget_row"]["target"]),
            "two_subcube_tight_tail_signed_action": (
                two["tight_positive_signed_tail_budget_row"][
                    "tail_signed_action"]),
            "two_subcube_tight_tail_abs_action": (
                two["tight_positive_signed_tail_budget_row"][
                    "tail_abs_action"]),
            "support_size_le_2_all_row_adverse_tail_margin": (
                tail_stress["summary"]["support_size_le_2_all_tail_margin"]),
            "support_size_le_2_signed_tail_budget": (
                le2["minimum_positive_signed_tail_budget"]),
            "support_size_le_2_tight_target": (
                le2["tight_positive_signed_tail_budget_row"]["target"]),
            "full_15_packet_signed_budget": (
                support["all_rows_component_envelope"][
                    "tightest_positive_margin_row"][
                        "signed_packet_error_budget_with_aligned_exact"]),
            "full_15_packet_tight_target": (
                full["tight_positive_signed_tail_budget_row"]["target"]
                if full["tail_packet_count"] else 94856),
            "l2_zero_pair_count": l2_summary["zero_pair_count"],
            "l2_row_local_cap_exceeding_row_count": (
                l2_summary["row_local_cap_exceeding_row_count"]),
        },
        "decision": (
            "The unqualified all-row adverse-tail route remains rejected, but "
            "the signed-tail split is a sharper theorem target.  For the "
            "two-subcube mask, the all-row adverse-tail stress margin is "
            "about -0.33851, while exact signed-tail control on the tight "
            "positive row would need relative error below about 0.07569.  "
            "For the support-size <=2 mask, the corresponding signed-tail "
            "budget is about 0.24152, much looser, although its retained mask "
            "is less aligned with the earlier two-subcube structure.  The "
            "full 15-packet signed budget remains about 0.05545.  This says "
            "the next proof target should be a universal pointwise signed "
            "packet/tail estimate, preferably support-size <=2 or a similarly "
            "natural class, not a disconnected adverse-envelope theorem.  The "
            "zero-mass check from the L2 audit is clean on its finite rows, "
            "but the non-circular analytic bridge is not confirmed.  Goldbach "
            "remains open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
