"""Audit the logical status of the q286 active-selector L2 route.

Kevin's question is not whether another finite window passes.  It is whether
the L2 target is actually non-circular.  This derived receipt separates three
states that were easy to blur:

* valid sufficient theorem shape;
* non-circular if proved as an external pointwise arithmetic estimate;
* not currently confirmed, and too strong as a practical finite bridge.

Finite/logical audit only.  No L2 theorem, active-selector rarity theorem,
strict-central existence theorem, or Goldbach proof is established.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-active-selector-l2-bridge-status-audit.json"

RESIDUE_PAIR_SOURCE = (
    EVIDENCE / "q286-first-three-residue-pair-correlation-obligation.json")
SIGNED_PROJECTION_SOURCE = (
    EVIDENCE / "q286-first-three-signed-projection-obligation.json")
ORBIT_UNIFORMITY_SOURCE = (
    EVIDENCE / "q286-first-three-orbit-uniformity-budget.json")
POST_FAILURE_HOLDOUT_SOURCE = (
    EVIDENCE / "q286-active-lane-post-failure-cycle-holdout.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sample_l2_rows(signed_projection):
    rows = []
    for target, row in sorted(
            signed_projection["sample_rows"].items(),
            key=lambda item: int(item[0])):
        rows.append({
            "target": int(target),
            "target_mod_286": int(row["target_mod_286"]),
            "tail_target": bool(row["tail_target"]),
            "first_three_to_principal_ratio": float(
                row["first_three_to_principal_ratio"]),
            "generic_l2_uniformity_certificate_holds": bool(
                row["generic_l2_uniformity_certificate_holds"]),
            "signed_projection_certificate_holds": bool(
                row["signed_projection_certificate_holds"]),
            "l2_budget_utilization": float(row["l2_budget_utilization"]),
            "orthogonal_delta_l2_fraction": float(
                row["orthogonal_delta_l2_fraction"]),
            "cosine_margin_to_threshold": float(
                row["cosine_margin_to_threshold"]),
        })
    return rows


def build_receipt():
    residue_pair = load_json(RESIDUE_PAIR_SOURCE)
    signed_projection = load_json(SIGNED_PROJECTION_SOURCE)
    orbit_uniformity = load_json(ORBIT_UNIFORMITY_SOURCE)
    post_failure = load_json(POST_FAILURE_HOLDOUT_SOURCE)

    clear_l2_fail_signed_pass = [
        row for row in sample_l2_rows(signed_projection)
        if (not row["tail_target"]
            and not row["generic_l2_uniformity_certificate_holds"]
            and row["signed_projection_certificate_holds"])
    ]
    sample_rows = sample_l2_rows(signed_projection)

    return {
        "schema_version": 1,
        "receipt": "q286-active-selector-l2-bridge-status-audit",
        "source_commit": source_commit(),
        "sources": {
            "residue_pair_correlation_obligation": str(
                RESIDUE_PAIR_SOURCE.relative_to(ROOT)),
            "signed_projection_obligation": str(
                SIGNED_PROJECTION_SOURCE.relative_to(ROOT)),
            "orbit_uniformity_budget": str(
                ORBIT_UNIFORMITY_SOURCE.relative_to(ROOT)),
            "post_failure_cycle_holdout": str(
                POST_FAILURE_HOLDOUT_SOURCE.relative_to(ROOT)),
        },
        "question": (
            "Is the q286 active-selector L2 rarity target genuinely "
            "non-circular, and is it actually confirmed?"),
        "short_answer": (
            "The L2 smallness statement is a valid non-circular sufficient "
            "theorem shape if it is proved as a pointwise arithmetic estimate "
            "for actual strict-central binary-prime residue weights with "
            "T_N>0.  It is not confirmed: no such theorem is proved, the "
            "finite scouts only measure windows, and clear sample rows already "
            "show generic L2 uniformity is stronger than necessary."),
        "l2_sufficient_theorem_shape": {
            "normalized_statement": (
                "For even N == a mod 286 with T_N=sum_u W_N(u)>0, if "
                "||W_N - T_N/|A_a|||_2 / T_N <= 0.3 / ||gamma_a||_2, "
                "then first_three(N) >= -0.3."),
            "minimum_l2_relative_error_sufficient": float(
                residue_pair["minimum_l2_relative_error_sufficient"]),
            "maximum_l2_relative_error_sufficient": float(
                residue_pair["maximum_l2_relative_error_sufficient"]),
            "minimum_linf_relative_error_sufficient": float(
                residue_pair[
                    "minimum_pointwise_linf_relative_error_sufficient"]),
            "maximum_linf_relative_error_sufficient": float(
                residue_pair[
                    "maximum_pointwise_linf_relative_error_sufficient"]),
            "even_target_residue_count": int(
                residue_pair["even_target_residue_count"]),
            "maximum_centered_coefficient_mean_error": float(
                residue_pair["maximum_local_coefficient_mean_error"]),
        },
        "non_circularity_classification": {
            "valid_sufficient_implication": True,
            "non_circular_as_external_arithmetic_premise": True,
            "confirmed_by_current_work": False,
            "proves_strict_central_existence": False,
            "proves_goldbach": False,
            "why_not_circular": (
                "The premise is a statement about actual residue weights "
                "W_N(u) before applying the active selector; it does not say "
                "'assume first_three >= -0.3'.  If proved uniformly from "
                "prime-pair distribution, it would exclude active-selector "
                "tails without reusing the desired conclusion."),
            "normalization_boundary": (
                "The L2 premise is normalized by T_N and therefore only has "
                "content when T_N>0.  It can control residue distribution "
                "conditional on strict-central prime-pair mass; it cannot by "
                "itself prove that such mass exists.  A positive main-term "
                "AP theorem would be a separate Goldbach-strength input."),
            "why_not_confirmed": (
                "The repository has coefficient identities and finite window "
                "measurements, but no pointwise theorem proving the L2 bound "
                "for every sufficiently large target."),
        },
        "sample_stress": {
            "sample_targets": [
                int(target) for target in signed_projection["sample_targets"]],
            "sample_rows": sample_rows,
            "clear_rows_that_fail_l2_but_pass_signed_projection": (
                clear_l2_fail_signed_pass),
            "clear_l2_fail_signed_pass_count": len(
                clear_l2_fail_signed_pass),
            "tail_sample_targets": [
                int(target) for target in signed_projection[
                    "signed_projection_failure_targets"]],
            "interpretation": (
                "Generic L2 uniformity is sufficient but too blunt: clear "
                "rows can fail the L2 budget and still pass because their "
                "deviation is mostly orthogonal or favorably aligned relative "
                "to the q286 coefficient vector."),
        },
        "zero_mass_status": {
            "zero_mass_defect_found": False,
            "zero_mass_checked_here": False,
            "meaning": (
                "This active-selector L2 audit is a normalized rarity audit, "
                "not a zero-mass existence proof.  If T_N=0, the normalized "
                "L2 ratio and first_three selector are not the right bridge; "
                "one must use an unnormalized positive witness or a separate "
                "strict-central existence theorem."),
        },
        "post_failure_context": {
            "scanned_target_count": int(post_failure["scanned_target_count"]),
            "active_selector_count": int(
                post_failure["active_selector_count"]),
            "active_targets": post_failure["active_targets"],
            "active_targets_not_in_source_summary": (
                post_failure["active_targets_not_in_source_summary"]),
            "decision_relevance": (
                "The post-failure holdout supports active-selector rarity as "
                "a theorem obligation, but it does not prove the L2 premise."),
        },
        "decision": (
            "HOLD_L2_is_valid_sufficient_non_circular_shape_but_unconfirmed. "
            "Do not treat L2 as an accepted bridge.  Use it only as a theorem "
            "target or replace it with the sharper signed-projection/"
            "anti-alignment obligation."),
        "next_action": (
            "Prefer the coefficient-sensitive signed-projection theorem "
            "<delta_N,c_a> >= -0.3, or its residue-pair correlation form, over "
            "plain L2 uniformity.  Plain L2 should sleep unless a genuine "
            "pointwise fixed-modulus binary-prime discrepancy theorem is "
            "proved or cited."),
        "status_boundary": (
            "Logical bridge-status audit only; this proves no L2 discrepancy "
            "theorem, active-selector rarity theorem, strict-central prime-pair "
            "existence theorem, q286 threshold theorem, or Goldbach proof."),
        "goldbach_proved": False,
        "l2_discrepancy_theorem_proved": False,
        "active_selector_rarity_theorem_proved": False,
        "strict_central_prime_pair_existence_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
