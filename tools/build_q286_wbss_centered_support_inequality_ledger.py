"""Build the q286 centered-support inequality ledger.

The local-factor classifier reduced the q286-WBSS route to one raw problem:
the positive local factor must beat the centered signed correlations.  This
receipt turns that open bridge into explicit per-support theorem targets for
the dominant lower moduli 286, 154, 70, and the remaining tail.

This is a theorem-obligation ledger only.  It proves no centered-error bound,
no major/minor arc estimate, no positive-mass theorem, and no Goldbach proof.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
LOCAL_FACTOR = (
    EVIDENCE / "q286-wbss-major-arc-local-factor-collapse-audit.json")
CENTERED_BURDEN = EVIDENCE / "q286-centered-character-burden-audit.json"
OUT = EVIDENCE / "q286-wbss-centered-support-inequality-ledger.json"

DOMINANT_LABELS = ("11x13", "7x11", "5x7")
SUPPORT_NAME_BY_LABEL = {
    "11x13": "dominant_286",
    "7x11": "dominant_154",
    "5x7": "dominant_70",
}
SAFETY_RESERVE_FRACTION = 0.10


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def summary_to_max_abs(summary):
    return max(abs(float(summary["minimum"])), abs(float(summary["maximum"])))


def support_metric_rows(centered):
    rows = []
    for row in centered["support_rows"]:
        label = row["support_label"]
        name = SUPPORT_NAME_BY_LABEL.get(label, "tail")
        max_abs = summary_to_max_abs(
            row["local_contribution_to_principal_ratio_summary"])
        rows.append({
            "bucket": name,
            "support_label": label,
            "natural_modulus": row["natural_modulus"],
            "energy_fraction": row["energy_fraction"],
            "character_count": row["character_count"],
            "local_ratio_minimum": row[
                "local_contribution_to_principal_ratio_summary"]["minimum"],
            "local_ratio_maximum": row[
                "local_contribution_to_principal_ratio_summary"]["maximum"],
            "local_ratio_max_abs": max_abs,
        })
    return rows


def bucket_rows(centered, weakest_ratio):
    support_rows = support_metric_rows(centered)
    buckets = []
    for bucket in ("dominant_286", "dominant_154", "dominant_70", "tail"):
        parts = [row for row in support_rows if row["bucket"] == bucket]
        if not parts:
            continue
        buckets.append({
            "bucket": bucket,
            "support_labels": [row["support_label"] for row in parts],
            "natural_moduli": sorted({
                row["natural_modulus"] for row in parts
            }),
            "character_count": sum(row["character_count"] for row in parts),
            "energy_fraction": math.fsum(
                row["energy_fraction"] for row in parts),
            "coefficient_local_ratio_worst_negative": min(
                row["local_ratio_minimum"] for row in parts),
            "coefficient_local_ratio_largest_positive": max(
                row["local_ratio_maximum"] for row in parts),
            "coefficient_local_ratio_max_abs_sum": math.fsum(
                row["local_ratio_max_abs"] for row in parts),
        })

    total_abs = math.fsum(
        row["coefficient_local_ratio_max_abs_sum"] for row in buckets)
    total_budget = weakest_ratio * (1.0 - SAFETY_RESERVE_FRACTION)
    for row in buckets:
        allocation = (
            total_budget * row["coefficient_local_ratio_max_abs_sum"]
            / total_abs)
        row["sufficient_raw_lower_bound_normalized"] = -allocation
        row["allocated_negative_budget_ratio"] = allocation
        row["budget_formula"] = (
            "Prove component_raw(N) >= "
            "-allocated_negative_budget_ratio * P0_a(N), where P0_a(N) "
            "is the ordinary strict-central principal main scale produced "
            "inside the same raw circle-method argument.")
    return buckets


def build_receipt():
    local_factor = load_json(LOCAL_FACTOR)
    centered = load_json(CENTERED_BURDEN)
    weakest_ratio = local_factor["local_factor_evidence"][
        "local_mean_ratio_minimum"]
    buckets = bucket_rows(centered, weakest_ratio)
    allocated_total = math.fsum(
        row["allocated_negative_budget_ratio"] for row in buckets)
    reserve_ratio = weakest_ratio - allocated_total
    tail = next(row for row in buckets if row["bucket"] == "tail")

    return {
        "schema_version": 1,
        "receipt": "q286-wbss-centered-support-inequality-ledger",
        "source_commit": source_commit(),
        "sources": {
            "major_arc_local_factor_collapse_audit": str(
                LOCAL_FACTOR.relative_to(ROOT)),
            "major_arc_local_factor_status": local_factor["status"],
            "centered_character_burden_audit": str(
                CENTERED_BURDEN.relative_to(ROOT)),
        },
        "status": "TARGET_centered_support_inequality_ledger_open",
        "question": (
            "What exact lower-modulus centered signed-correlation bounds "
            "would keep the q286-WBSS centered error above the positive local "
            "factor?"),
        "answer": (
            "It is enough, but not proved, to bound the raw centered "
            "contributions from the dominant 286, 154, 70 supports and the "
            "tail below an allocated negative budget whose sum is strictly "
            "smaller than the weakest local factor ratio.  The ledger fixes "
            "one explicit 10 percent reserve budget so future theorem "
            "attempts have a non-moving target."),
        "raw_objects": {
            "ordinary_principal_scale": (
                "P0_a(N): the ordinary strict-central binary-prime principal "
                "main scale for N == a mod 10010, produced inside the same "
                "raw major/minor arc proof."),
            "local_factor": (
                "m_a_ratio = m_a / principal_mean, with weakest checked "
                "coefficient value 0.6039353780830684."),
            "component_raw_contribution": (
                "K_B(N)=sum_{u in A_a}(W_N(u)-P0_a(N)/|A_a|)*Phi_B(u) "
                "for support bucket B, expressed before any division by "
                "actual T_N."),
            "sufficient_ledger_inequality": (
                "For every sufficiently large covered N, prove "
                "K_B(N) >= -beta_B*P0_a(N) for B in {286,154,70,tail}, "
                "with sum_B beta_B < m_a_ratio for the target residue."),
            "zero_mass_boundary": (
                "The ledger is not a normalized T_N statement.  If a proof "
                "first assumes actual T_N>0, it collapses to conditional "
                "distribution control."),
        },
        "budget_model": {
            "name": "coefficient_max_abs_proportional_with_10_percent_reserve",
            "novelty_label": "new-to-this-task",
            "weakest_local_factor_ratio": weakest_ratio,
            "safety_reserve_fraction": SAFETY_RESERVE_FRACTION,
            "allocated_negative_budget_total": allocated_total,
            "unallocated_reserve_ratio": reserve_ratio,
            "budget_passes_weakest_local_factor": allocated_total < weakest_ratio,
            "why_this_model": (
                "Allocate a fixed sufficient budget in proportion to finite "
                "coefficient-side max-absolute local contribution sizes.  It "
                "is deliberately stronger than the rowwise finite behavior "
                "and exists only to make the next theorem target explicit."),
        },
        "bucket_obligations": buckets,
        "tail_detail": {
            "tail_supports": tail["support_labels"],
            "tail_natural_moduli": tail["natural_moduli"],
            "tail_energy_fraction": tail["energy_fraction"],
            "tail_allocated_negative_budget_ratio": (
                tail["allocated_negative_budget_ratio"]),
            "tail_bound_required": (
                "Either prove a combined tail lower bound at this budget, or "
                "split the tail supports 14,26,130,10,22 into separate raw "
                "bounds whose beta values sum no larger than the tail budget."),
        },
        "candidate": {
            "name": "centered-support raw inequality ledger",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Replace a vague signed-correlation theorem with four raw "
                "lower-bound obligations whose total negative allowance is "
                "strictly less than the weakest positive local factor."),
            "prediction": (
                "If the q286 lane can close, the dominant lower-modulus "
                "supports 286, 154, and 70 should admit pointwise raw "
                "correlation bounds below their allocated budgets, with a "
                "small combined tail bound."),
            "falsifier": (
                "A source-backed theorem that cannot reach these raw lower "
                "bounds, or a counterfamily forcing any bucket below its "
                "allocated budget infinitely often, leaves q286 open or "
                "collapses it to conditional distribution control."),
            "smallest_next_test": (
                "Attempt source-fitting for the four raw bucket inequalities: "
                "dominant_286, dominant_154, dominant_70, and tail."),
        },
        "decision": (
            "TARGET_centered_support_inequality_ledger_open.  The exact q286 "
            "next theorem target is now a four-bucket raw inequality ledger: "
            "prove component lower bounds for moduli 286, 154, 70, and the "
            "tail whose allocated beta values sum to "
            f"{allocated_total} < weakest local factor {weakest_ratio}.  "
            "This is stronger than finite row evidence and proves no "
            "pointwise centered-error theorem."),
        "status_boundary": (
            "Theorem-obligation ledger only; this is not a theorem.  No "
            "source theorem fit, major/minor arc estimate, pointwise "
            "centered-error estimate, signed prime-correlation theorem, "
            "positive-mass theorem, q286 threshold theorem, strict-central "
            "Goldbach theorem, or Goldbach proof is established."),
        "goldbach_proved": False,
        "source_theorem_fit_proved": False,
        "major_minor_arc_estimate_proved": False,
        "pointwise_centered_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "positive_mass_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "universal_pointwise_bound_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "allocated_negative_budget_total": (
            receipt["budget_model"]["allocated_negative_budget_total"]),
        "weakest_local_factor_ratio": (
            receipt["budget_model"]["weakest_local_factor_ratio"]),
        "unallocated_reserve_ratio": (
            receipt["budget_model"]["unallocated_reserve_ratio"]),
        "bucket_count": len(receipt["bucket_obligations"]),
        "pointwise_centered_error_estimate_proved": (
            receipt["pointwise_centered_error_estimate_proved"]),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
