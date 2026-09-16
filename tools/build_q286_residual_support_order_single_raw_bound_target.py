"""Classify the single raw-bound route for q286 support order.

The positive-mass classifier showed that the normalized denominator condition
is strict-central prime-pair existence in disguise.  This receipt records the
alternative: prove one unnormalized, pointwise lower-bound theorem directly.

Logical theorem-target audit only.  It proves no raw lower-bound theorem,
positive-mass theorem, q286 threshold theorem, strict-central Goldbach theorem,
or Goldbach proof.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
RAW_SCALE_SOURCE = EVIDENCE / "q286-residual-support-order-raw-scale-bridge.json"
POSITIVE_MASS_SOURCE = (
    EVIDENCE / "q286-residual-support-order-positive-mass-obligation.json")
OUT = EVIDENCE / "q286-residual-support-order-single-raw-bound-target.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    raw = load_json(RAW_SCALE_SOURCE)
    positive_mass = load_json(POSITIVE_MASS_SOURCE)
    horizon = raw["finite_horizon"]
    positive = positive_mass["finite_calibration"]
    tight = horizon["tight_raw_margin_row"]
    smallest_pair = positive["smallest_pair_count_row"]
    raw_failures = horizon["raw_domination_failure_targets"]

    row_count = int(horizon["row_count"])
    raw_margin_positive_count = row_count - len(raw_failures)

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "raw_scale_bridge": str(RAW_SCALE_SOURCE.relative_to(ROOT)),
            "positive_mass_obligation": str(
                POSITIVE_MASS_SOURCE.relative_to(ROOT)),
        },
        "status": "TARGET_single_raw_lower_bound_subsumes_positive_mass",
        "status_boundary": (
            "logical theorem-target audit only; no single raw lower-bound "
            "theorem, positive-mass theorem, raw pointwise estimate, "
            "one-period threshold theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "single_raw_lower_bound_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "raw_pointwise_estimate_proved": False,
        "one_period_threshold_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "theorem_target": {
            "eligible_domain": (
                "every sufficiently large eligible N in the named q286 "
                "support-order period classes, with any finite initial range "
                "verified separately"),
            "raw_low_order_base": "B_low_raw(N)",
            "raw_high_order_tail": "T_high_raw(N)",
            "raw_adverse_drag": "D_high_minus_raw(N)=max(0,-T_high_raw(N))",
            "raw_margin": (
                "R_raw(N)=B_low_raw(N)-D_high_minus_raw(N)"),
            "target_statement": (
                "Prove R_raw(N)>0 pointwise for every sufficiently large "
                "eligible N in the named period classes."),
            "support_order_witness": (
                "B_low_raw(N)+T_high_raw(N) is the raw support-order witness "
                "assembled from strict-central prime-pair weights."),
            "why_strict_raw_bound_implies_full_witness_positive": (
                "If T_high_raw(N)<0, then D_high_minus_raw(N)=-T_high_raw(N), "
                "so R_raw(N)>0 gives B_low_raw(N)+T_high_raw(N)>0.  If "
                "T_high_raw(N)>=0, then D_high_minus_raw(N)=0, so "
                "R_raw(N)>0 gives B_low_raw(N)>0 and the full witness is "
                "positive after adding the nonnegative tail."),
            "zero_mass_obstruction": (
                "If the strict-central prime-pair support is empty, every raw "
                "prime-pair sum used by this witness is zero.  Then "
                "B_low_raw(N)=T_high_raw(N)=D_high_minus_raw(N)=R_raw(N)=0, "
                "contradicting a strict raw lower bound."),
            "strict_central_existence_implication": (
                "Therefore a proved strict raw lower bound implies nonempty "
                "strict-central support, hence at least one prime pair "
                "N=p+(N-p) with N/3<p<2N/3 for that N."),
            "quantifier_boundary": (
                "This implication is only as broad as the theorem's eligible "
                "period classes plus its finite remainder verification."),
        },
        "route_decision": {
            "single_raw_bound_subsumes_positive_mass": True,
            "separate_positive_mass_can_sleep_if_raw_bound_proved": True,
            "route_is_still_goldbach_strength": True,
            "not_a_denominator_shortcut": True,
            "recommended_next": (
                "Seek a universal pointwise unnormalized analytical estimate "
                "for R_raw(N)>0 directly.  Keep a separate positive-mass "
                "lemma only if using normalized inequalities or an external "
                "strict-central existence theorem."),
        },
        "finite_calibration": {
            "finite_evidence_is_acceptance_condition": False,
            "row_count": row_count,
            "raw_margin_positive_rows": raw_margin_positive_count,
            "raw_domination_failure_targets": raw_failures,
            "positive_pair_count_rows": int(
                positive["positive_pair_count_rows"]),
            "positive_total_weight_rows": int(
                positive["positive_total_weight_rows"]),
            "zero_pair_count_targets": positive["zero_pair_count_targets"],
            "zero_or_negative_weight_targets": positive[
                "zero_or_negative_weight_targets"],
            "tight_raw_margin_row": {
                "target": int(tight["target"]),
                "raw_pointwise_margin": float(tight["raw_pointwise_margin"]),
                "raw_low_order_base": float(tight["raw_low_order_base"]),
                "raw_high_order_tail": float(tight["raw_high_order_tail"]),
                "raw_adverse_drag": float(tight["raw_adverse_drag"]),
                "ordered_central_prime_pair_count": int(
                    tight["ordered_central_prime_pair_count"]),
                "strict_central_total_weight": float(
                    tight["strict_central_total_weight"]),
            },
            "smallest_pair_count_row": {
                "target": int(smallest_pair["target"]),
                "ordered_central_prime_pair_count": int(
                    smallest_pair["ordered_central_prime_pair_count"]),
                "strict_central_total_weight": float(
                    smallest_pair["strict_central_total_weight"]),
            },
            "principal_mean_real": float(raw["normalization_identity"][
                "principal_mean_real"]),
            "principal_mean_imag_to_real": float(raw[
                "normalization_identity"]["principal_mean_imag_to_real"]),
        },
        "unproved_obligations": [
            "a universal pointwise unnormalized estimate R_raw(N)>0",
            "the finite initial-range closure outside the asymptotic theorem",
            "coverage of all even N if the named period classes do not already "
            "cover the desired range",
            "independent mathematical review before any proof promotion",
        ],
        "decision": (
            "A single strict raw lower-bound theorem would subsume the "
            "positive-mass obligation: zero strict-central support makes all "
            "raw witness terms vanish, so R_raw(N)>0 forces at least one "
            "strict-central prime pair.  This is the cleaner route because it "
            "avoids dividing by an unproved denominator, but it is still "
            "Goldbach-strength theorem work, not a finite-evidence acceptance "
            "condition and not a solved shortcut."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
