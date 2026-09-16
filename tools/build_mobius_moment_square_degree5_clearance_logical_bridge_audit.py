"""Audit the logical bridge behind the degree-5 clearance target.

The band-clearance holdout is a useful finite decomposition, but it is not by
itself a theorem bridge: it reuses the same signed denominator ledger whose
positivity we want to prove.  This receipt separates the finite observation
from the independent pointwise estimates that would make the route
non-circular.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
BAND_CLEARANCE = (
    EVIDENCE / "mobius-moment-square-degree5-band-clearance-holdout.json")
SOURCE_CLEARANCE = (
    EVIDENCE
    / "mobius-moment-square-degree5-source-margin-clearance-family-audit.json")
MOVING_BAND = (
    EVIDENCE / "mobius-moment-square-degree5-moving-prime-band-audit.json")
OUT = (
    EVIDENCE
    / "mobius-moment-square-degree5-clearance-logical-bridge-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    band = load_json(BAND_CLEARANCE)
    source = load_json(SOURCE_CLEARANCE)
    moving = load_json(MOVING_BAND)

    finite_decomposition_confirmed = (
        band["all_middle_far_total_dominates_near_negative"]
        and source["all_middle_far_total_dominates_near_negative"]
    )
    false_shortcut_confirmed = (
        not band["all_negative_denominators_near_threshold"]
        and not source["all_negative_denominators_near_threshold"]
    )
    bridge_confirmed = (
        band["clearance_family_theorem_proved"]
        or source["clearance_family_theorem_proved"]
    )
    maximum_ratio = max(
        band["maximum_near_negative_over_middle_far_positive"],
        source["maximum_near_negative_over_middle_far_positive"],
    )

    return {
        "schema_version": 1,
        "receipt": "mobius-moment-square-degree5-clearance-logical-bridge",
        "source_commit": source_commit(),
        "status": "HOLD_clearance_logical_bridge_not_confirmed",
        "sources": {
            "band_clearance_holdout": str(BAND_CLEARANCE.relative_to(ROOT)),
            "band_clearance_status": band["status"],
            "source_clearance_family_audit": str(
                SOURCE_CLEARANCE.relative_to(ROOT)),
            "source_clearance_family_status": source["status"],
            "moving_prime_band_audit": str(MOVING_BAND.relative_to(ROOT)),
            "moving_prime_band_status": moving["status"],
        },
        "question": (
            "Does the sigma-band clearance evidence already provide a "
            "non-circular theorem bridge, or only a finite decomposition of "
            "the same signed margin ledger?"),
        "answer": (
            "Only the finite decomposition is confirmed.  A non-circular "
            "bridge would require independent pointwise estimates bounding "
            "near-threshold adverse leakage above and middle/far clearance "
            "margin below, uniformly in the moving prime block."),
        "finite_evidence": {
            "band_minimum_blocks_checked": band["band_count"],
            "tight_source_blocks_checked": source["scale_count"],
            "all_band_minima_clearance_positive": (
                band["all_middle_far_total_dominates_near_negative"]),
            "all_tight_source_blocks_clearance_positive": (
                source["all_middle_far_total_dominates_near_negative"]),
            "finite_decomposition_confirmed": finite_decomposition_confirmed,
            "maximum_near_negative_over_middle_far_positive": maximum_ratio,
            "band_maximum_ratio": (
                band["maximum_near_negative_over_middle_far_positive"]),
            "source_maximum_ratio": (
                source["maximum_near_negative_over_middle_far_positive"]),
            "negative_denominator_family_counts": {
                "band_holdout": band["negative_denominator_family_counts"],
                "tight_source_blocks": (
                    source["negative_denominator_family_counts"]),
            },
        },
        "logical_bridge_classification": {
            "non_circular_theorem_shape_defined": True,
            "logical_bridge_confirmed": bridge_confirmed,
            "finite_evidence_is_acceptance_condition": False,
            "false_all_negative_near_shortcut_confirmed": (
                false_shortcut_confirmed),
            "why_not_confirmed": (
                "The receipts compute exact signed family sums from the "
                "target ledger.  They do not prove an independent upper bound "
                "for adverse near-threshold terms or an independent lower "
                "bound for middle/far terms."),
            "current_hold": (
                "HOLD_for_independent_pointwise_clearance_estimates"),
        },
        "pointwise_unnormalized_target": {
            "source_parameters": (
                "For source scale M, moving prime p in [M,2M], row count "
                "A=int((M**(1/.59))**.41), and component label ell."),
            "margin_components": {
                "m_Q": (
                    "m_Q(M,p,ell)=full_Q(M,p,ell)/2-active_Q(M,p,ell) "
                    "for each reduced denominator Q"),
                "A_near": (
                    "sum_{p*A < Q < 2*p*A} max(0,-m_Q(M,p,ell))"),
                "G_middle_far": (
                    "sum_{Q >= 2*p*A} m_Q(M,p,ell)"),
            },
            "sufficient_pointwise_inequality": (
                "G_middle_far(M,p,ell) > A_near(M,p,ell) for every "
                "sufficiently large source-admissible row, with finite "
                "remainder checked separately."),
            "why_this_is_stronger_than_total_margin": (
                "Near-positive terms are discarded.  Proving the inequality "
                "from independent estimates would imply positive total "
                "margin without assuming it."),
        },
        "required_independent_obligations": [
            {
                "id": "moving_prime_sigma_coverage",
                "statement": (
                    "Cover every sufficiently large source-admissible prime "
                    "block p in [M,2M] by sigma bands, including endpoints."),
                "not_supplied_by": "finite seven-sweep moving-band audit",
            },
            {
                "id": "near_adverse_upper_bound",
                "statement": (
                    "Prove a pointwise upper bound for A_near(M,p,ell) "
                    "without using total margin positivity."),
                "not_supplied_by": "observed near-negative sums",
            },
            {
                "id": "middle_far_lower_bound",
                "statement": (
                    "Prove a pointwise lower bound for G_middle_far(M,p,ell) "
                    "without reusing the target positivity claim."),
                "not_supplied_by": "observed middle/far exact ledger sums",
            },
            {
                "id": "comparison_margin",
                "statement": (
                    "Show lower_bound(G_middle_far) exceeds "
                    "upper_bound(A_near) by an explicit positive margin."),
                "not_supplied_by": "finite safety ratio alone",
            },
            {
                "id": "finite_remainder",
                "statement": (
                    "After a threshold theorem, verify all smaller source "
                    "scales by exact computation."),
                "not_supplied_by": "current theorem-shaped holdout",
            },
        ],
        "invalid_substitutes": [
            "finite clearance ratios",
            "the false all-negative-near shortcut",
            "total denominator margin already known positive",
            "a fitted residual constant",
            "a normalized estimate that assumes positive Goldbach mass first",
        ],
        "candidate_next_action": {
            "name": "independent near-vs-middlefar denominator bounds",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Bound adverse near-threshold denominator phases and "
                "middle/far clearance margin by separate analytic estimates, "
                "then compare them pointwise."),
            "prediction": (
                "If the finite pattern is structural, the first successful "
                "bound will not need the all-negative-near shortcut and will "
                "keep endpoint sigma bands in scope."),
            "falsifier": (
                "A source-admissible block where independent middle/far lower "
                "bounds cannot exceed near-adverse upper bounds falsifies this "
                "proof route, even if the exact finite ledger is positive."),
            "smallest_next_test": (
                "For the M=229,p=379 middle-band exception, derive an exact "
                "symbolic or interval upper bound for the lone adverse "
                "middle-family denominator Q=46189 and compare it to the "
                "positive middle/far ledger without using total positivity."),
        },
        "decision": (
            "HOLD_clearance_logical_bridge_not_confirmed.  The clearance "
            "family split is useful finite structure, but the theorem bridge "
            "requires independent pointwise unnormalized estimates.  Future "
            "work should target near-adverse upper bounds and middle/far "
            "lower bounds, not broader finite scans or the false "
            "all-negative-near shortcut."),
        "status_boundary": (
            "Logical bridge audit only.  No source-start theorem, "
            "prime-block theorem, moving-prime theorem, sigma-band theorem, "
            "clearance-family theorem, strict-central Goldbach theorem, or "
            "Goldbach proof is established."),
        "source_start_theorem_proved": False,
        "prime_block_theorem_proved": False,
        "moving_prime_block_theorem_proved": False,
        "sigma_band_theorem_proved": False,
        "clearance_family_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "finite_decomposition_confirmed": receipt["finite_evidence"][
            "finite_decomposition_confirmed"],
        "logical_bridge_confirmed": receipt[
            "logical_bridge_classification"]["logical_bridge_confirmed"],
        "maximum_ratio": receipt["finite_evidence"][
            "maximum_near_negative_over_middle_far_positive"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
