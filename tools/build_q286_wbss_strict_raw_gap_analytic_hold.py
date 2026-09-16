"""Classify the analytic HOLD behind the q286-WBSS strict raw gap.

The strict raw-gap receipt shows that the non-circular bridge is

    G_raw(N) = L_raw(N) - A_raw_-(N) > 0.

This receipt records what kind of analytical theorem would actually pay that
gap.  In particular, normalized discrepancy estimates, finite fitted constants,
and one-dimensional AP estimates are not acceptance conditions.  A proof needs
either a direct positive raw signed binary-prime sum, or a positive mass theorem
plus one-sided raw projection control.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
STRICT_GAP_SOURCE = EVIDENCE / "q286-wbss-strict-raw-gap-obligation.json"
COEFFICIENT_HOLD_SOURCE = (
    EVIDENCE / "q286-wbss-coefficient-discrepancy-budget-hold.json")
OUT = EVIDENCE / "q286-wbss-strict-raw-gap-analytic-hold.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    strict_gap = load_json(STRICT_GAP_SOURCE)
    coefficient_hold = load_json(COEFFICIENT_HOLD_SOURCE)
    gap_summary = strict_gap["finite_calibration"]["summary"]
    budget = coefficient_hold["coefficient_budget"]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "strict_raw_gap_obligation": str(
                STRICT_GAP_SOURCE.relative_to(ROOT)),
            "strict_raw_gap_source_commit": strict_gap["source_commit"],
            "coefficient_discrepancy_budget_hold": str(
                COEFFICIENT_HOLD_SOURCE.relative_to(ROOT)),
            "coefficient_discrepancy_source_commit": coefficient_hold[
                "source_commit"],
        },
        "status": "HOLD_for_strict_raw_binary_pair_estimate",
        "status_boundary": (
            "strict raw-gap analytic HOLD only; no direct raw signed "
            "binary-prime estimate, positive-mass theorem, one-sided "
            "projection theorem, q286 threshold theorem, strict-central "
            "Goldbach theorem, or Goldbach proof is established"),
        "goldbach_proved": False,
        "strict_raw_gap_theorem_proved": False,
        "direct_raw_signed_binary_pair_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "one_sided_projection_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "universal_bound_open": True,
        "bridge": {
            "strict_raw_gap": (
                "G_raw(N)=L_raw(N)-A_raw_-(N)>0"),
            "raw_terms": (
                "L_raw(N)=T_N*M(a), E_raw_d(N)=T_N*E_d(N), and "
                "A_raw_-(N)=sum_d max(0,-E_raw_d(N))."),
            "zero_mass_barrier": (
                "If strict-central support is empty, then T_N=0, "
                "L_raw(N)=0, every E_raw_d(N)=0, and G_raw(N)=0.  "
                "Therefore any proof must create a strict positive raw "
                "quantity, not only a homogeneous or normalized inequality."),
        },
        "sufficient_analytic_routes": {
            "direct_signed_binary_pair_sum": {
                "statement": (
                    "Prove the raw q286-WBSS signed binary-prime witness "
                    "W_phi(N)>0, or the stronger lower bound "
                    "G_raw(N)>=eta(N)>0, for every sufficiently large "
                    "covered even N."),
                "non_circular": True,
                "separate_positive_mass_needed": False,
                "why": (
                    "The raw sum is zero on a zero-support row, so strict "
                    "positivity itself forces a strict-central prime pair."),
            },
            "mass_plus_one_sided_projection_control": {
                "statement": (
                    "Prove T_N>=P(N)>0 and pointwise one-sided bounds "
                    "max(0,-E_raw_d(N))<=B_d(N) with "
                    "sum_d B_d(N)<M(a)*P(N)."),
                "non_circular": True,
                "separate_positive_mass_needed": True,
                "why": (
                    "This proves G_raw(N)>=M(a)*P(N)-sum_d B_d(N)>0, "
                    "but the positive mass input is already "
                    "strict-central existence strength."),
            },
            "normalized_projection_discrepancy": {
                "statement": (
                    "Prove normalized bounds on Delta_{d,s}(N) or E_d(N)."),
                "non_circular": False,
                "separate_positive_mass_needed": True,
                "why": (
                    "A normalized measure mu_N is meaningful only after "
                    "T_N>0; the same inequality is vacuous at zero mass."),
            },
        },
        "coefficient_budget_inherited": {
            "moduli": budget["moduli"],
            "total_l1_norm": budget["total_l1_norm"],
            "minimum_local_main_over_even_residues": budget[
                "minimum_local_main_over_even_residues"],
            "global_equal_residue_error_cap": budget[
                "global_equal_residue_error_cap"],
            "role": (
                "A stronger per-residue discrepancy corollary; sufficient "
                "but not necessary, and still requires non-circular "
                "binary-prime pair control."),
        },
        "rejected_acceptance_substitutes": [
            {
                "name": "more finite q286 rows",
                "reason": (
                    "finite calibration can falsify a proposed theorem "
                    "shape but cannot establish the universal pointwise "
                    "raw gap"),
            },
            {
                "name": "fitted residual absorption constants",
                "reason": (
                    ".125, .126, .13, or similar constants fitted to "
                    "checked rows are not universal bounds"),
            },
            {
                "name": "normalized L2 or L1 discrepancy alone",
                "reason": (
                    "normalized estimates do not create T_N>0 and therefore "
                    "do not cross the zero-mass barrier"),
            },
            {
                "name": "one-dimensional AP prime estimates alone",
                "reason": (
                    "they constrain marginal prime counts but not the "
                    "pointwise binary-prime convolution or the signed "
                    "coefficient-weighted pair sum"),
            },
            {
                "name": "almost-all or averaged estimates",
                "reason": (
                    "Goldbach requires every sufficiently large covered "
                    "target plus a finite remainder, not unnamed exceptions"),
            },
        ],
        "finite_context": {
            "role": "calibration_and_falsifier_only",
            "row_count": gap_summary["row_count"],
            "positive_strict_raw_gap_count": gap_summary[
                "positive_strict_raw_gap_count"],
            "nonpositive_strict_raw_gap_count": gap_summary[
                "nonpositive_strict_raw_gap_count"],
            "tightest_strict_raw_gap_target": gap_summary[
                "tightest_strict_raw_gap_row"]["target"],
            "tightest_strict_raw_gap": gap_summary[
                "tightest_strict_raw_gap_row"]["strict_raw_gap"],
            "smallest_gap_over_target": gap_summary[
                "smallest_gap_over_target_row"][
                    "strict_raw_gap_over_target"],
            "smallest_gap_over_total_weight": gap_summary[
                "smallest_gap_over_total_weight_row"][
                    "strict_raw_gap_over_total_weight"],
        },
        "candidate": {
            "name": "strict raw binary-pair estimate",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Move the q286-WBSS bridge from normalized finite evidence "
                "to an unnormalized pointwise binary-prime sign-sum "
                "theorem."),
            "prediction": (
                "A successful next proof will either lower-bound the raw "
                "signed witness directly or explicitly prove positive "
                "strict-central mass before using projection discrepancy."),
            "falsifier": (
                "Any covered even N with G_raw(N)<=0 falsifies this "
                "specific q286-WBSS sufficient route."),
            "smallest_next_action": (
                "Source or prove a pointwise binary-prime correlation "
                "estimate for the four-modulus coefficient directions "
                "strong enough to imply G_raw(N)>0."),
        },
        "decision": (
            "The strict raw-gap correction converts the q286-WBSS bridge "
            "into a HOLD for a pointwise raw binary-prime estimate.  The "
            "repository currently has no theorem proving the needed direct "
            "signed sum, positive mass plus one-sided projection control, "
            "or fixed-modulus binary-prime convolution bound.  Future finite "
            "rows are useful only as falsifiers or calibration for a "
            "predeclared theorem implication."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "row_count": receipt["finite_context"]["row_count"],
        "tightest_strict_raw_gap_target": (
            receipt["finite_context"]["tightest_strict_raw_gap_target"]),
        "global_equal_residue_error_cap": (
            receipt["coefficient_budget_inherited"][
                "global_equal_residue_error_cap"]),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
