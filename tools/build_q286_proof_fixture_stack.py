"""Build the q286 proof-fixture stack.

The fixture stack is a theorem-navigation artifact.  It follows the workshop
rule: bolt the exact identities to the actual frame first, tack only named
unresolved joints, and condense only after the tacks survive validation.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-proof-fixture-stack.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(relative):
    with (ROOT / relative).open(encoding="utf-8") as handle:
        return json.load(handle)


def main():
    signed_projection = load_json(
        "evidence/q286-first-three-signed-projection-obligation.json")
    residue_pair = load_json(
        "evidence/q286-first-three-residue-pair-correlation-obligation.json")
    external_comparison = load_json(
        "evidence/q286-residue-pair-external-theorem-comparison.json")
    character_narrowing = load_json(
        "evidence/q286-residue-pair-character-mode-narrowing.json")
    orbit_uniformity = load_json(
        "evidence/q286-first-three-orbit-uniformity-budget.json")
    mass_landing = load_json(
        "evidence/q286-first-three-mass-landing-obligation.json")
    mass_pairs = load_json(
        "evidence/q286-first-three-mass-matched-pair-decomposition.json")
    matched_pair_count = sum(
        row["opposite_outcome_pair_count"]
        for row in mass_pairs["window_summaries"])

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "proof-navigation fixture only; records exact anchors, unresolved "
            "tacks, and condensation target.  It proves no q286 signed "
            "projection theorem, no full outer assembly, and no Goldbach "
            "theorem."),
        "workshop_rule": (
            "Do not fabricate the whole theorem from free-space measurements. "
            "Bolt exact identities to the actual q286 frame, tack only named "
            "unresolved theorem joints, validate each tack unchanged, then "
            "condense the assembly only after the joints are proved."),
        "bolted_anchors": [
            {
                "id": "anchor.mass_landing_identity",
                "source": (
                    "evidence/q286-first-three-mass-landing-obligation.json"),
                "statement": (
                    "For actual q286 first-three reflection-orbit mass, "
                    "first_three=P-B=m_plus*ell_plus-m_minus*ell_minus."),
                "validation": (
                    "maximum reconstruction errors below "
                    f"{mass_landing['maximum_mass_landing_reconstruction_error']}"
                    " and threshold slack identity errors below "
                    f"{mass_landing['maximum_threshold_slack_identity_error']}."),
                "proved_scope": "exact finite algebraic identity",
            },
            {
                "id": "anchor.signed_projection_identity",
                "source": (
                    "evidence/q286-first-three-signed-projection-obligation.json"),
                "statement": (
                    "With delta_N=mu_N-u_a and coefficient vector c_a, "
                    "first_three(N)=<delta_N,c_a>."),
                "validation": (
                    "maximum projection identity error "
                    f"{signed_projection['maximum_projection_identity_error']}."),
                "proved_scope": "exact finite algebraic identity",
            },
            {
                "id": "anchor.residue_pair_discrepancy_identity",
                "source": (
                    "evidence/q286-first-three-residue-pair-correlation-obligation.json"),
                "statement": (
                    "The signed-projection tack is exactly "
                    "sum(W_N(u)-T_N/|A_a|)*gamma_a(u) >= -tau*T_N "
                    "on q286 strict-central binary-prime residue weights."),
                "validation": (
                    "sample rows match the signed-projection receipt below "
                    f"{residue_pair['maximum_prior_signed_projection_receipt_error']}"
                    " and local centered coefficient sums are below "
                    f"{residue_pair['maximum_local_coefficient_mean_error']}."),
                "proved_scope": (
                    "exact finite algebraic identification of the missing "
                    "arithmetic theorem"),
            },
            {
                "id": "anchor.external_theorem_strength_comparison",
                "source": (
                    "evidence/q286-residue-pair-external-theorem-comparison.json"),
                "statement": (
                    "Checked average, almost-all, distribution, and "
                    "upper-bound AP-Goldbach sources do not supply the "
                    "pointwise q286 residue-pair obligation; full "
                    "fixed-modulus AP asymptotics would imply it."),
                "validation": (
                    "average results supply obligation = "
                    f"{external_comparison['comparison_result']['average_goldbach_ap_results_supply_q286_obligation']}; "
                    "almost-all results supply obligation = "
                    f"{external_comparison['comparison_result']['almost_all_goldbach_ap_results_supply_q286_obligation']}."),
                "proved_scope": (
                    "source-backed theorem-strength comparison, not proof"),
            },
            {
                "id": "anchor.character_mode_narrowing",
                "source": (
                    "evidence/q286-residue-pair-character-mode-narrowing.json"),
                "statement": (
                    "Near-boundary samples are almost perfectly same-sign "
                    "negative in the rank-three q286 first-three "
                    "character-mode ledger."),
                "validation": (
                    "same-sign sample count "
                    f"{character_narrowing['same_sign_mode_target_count']} "
                    "of "
                    f"{len(character_narrowing['sample_targets'])}; "
                    "character product count "
                    f"{character_narrowing['character_product_count']}."),
                "proved_scope": "finite theorem-shaping diagnostic",
            },
            {
                "id": "anchor.generic_uniformity_is_too_blunt",
                "source": (
                    "evidence/q286-first-three-orbit-uniformity-budget.json"),
                "statement": (
                    "Generic L1/L2 orbit uniformity is sufficient but too "
                    "strong for the active-scale clear rows."),
                "validation": (
                    "clear budget failures "
                    f"{orbit_uniformity['clear_sample_uniformity_budget_failure_targets']}"),
                "proved_scope": "finite demotion of this sufficient route",
            },
            {
                "id": "anchor.mass_landing_pair_stress",
                "source": (
                    "evidence/q286-first-three-mass-matched-pair-decomposition.json"),
                "statement": (
                    "Mass/landing decomposition shows positive landing quality "
                    "dominates broad matched pairs while holdout rescue can be "
                    "mass-help offset by landing-quality harm."),
                "validation": (
                    "matched pair count "
                    f"{matched_pair_count}"),
                "proved_scope": "finite diagnostic, not recurrence",
            },
        ],
        "tacked_unresolved_joints": [
            {
                "id": "joint.q286_first_three_signed_projection",
                "statement": (
                    "For all sufficiently large even N in the q286 "
                    "first-three lane, prove <delta_N,c_a> >= -0.3, or the "
                    "equivalent cosine floor when norms are nonzero."),
                "why_it_is_needed": (
                    "This is the currently sharpest first-three rarity target "
                    "after generic uniformity was demoted."),
                "known_finite_stress": {
                    "failure_targets": (
                        signed_projection[
                            "signed_projection_failure_targets"]),
                    "clear_uniformity_fail_projection_pass": (
                        signed_projection[
                            "generic_uniformity_fail_signed_projection_pass_targets"]),
                },
                "proved": False,
            },
            {
                "id": "joint.lower_support_or_complement_rescue",
                "statement": (
                    "After first-three control, prove the conditioned "
                    "complement/lower-support rescue needed by the active "
                    "q286 proof stack, or prove the exact external theorem "
                    "that supplies it."),
                "why_it_is_needed": (
                    "First-three rarity alone closes only one q286 lane, not "
                    "the full strict-central action or outer assembly."),
                "proved": False,
            },
            {
                "id": "joint.boundary_and_endpoint_assembly",
                "statement": (
                    "Finitely check boundary targets and prove endpoint, "
                    "noncentral, and outer assembly terms needed to convert "
                    "the q286 lane into a Goldbach theorem."),
                "why_it_is_needed": (
                    "The q286 first-three route is a source-operator lane, not "
                    "the final Goldbach theorem."),
                "proved": False,
            },
            {
                "id": "joint.external_prime_correlation_input",
                "statement": (
                    "Prove the q286 pointwise binary-prime residue "
                    "correlation theorem "
                    "sum_{u in A_a}(W_N(u)-T_N/|A_a|)*gamma_a(u) "
                    ">= -tau*T_N, or cite an external theorem strong enough "
                    "to imply it."),
                "why_it_is_needed": (
                    "The surviving tacks are arithmetic distribution claims "
                    "about actual prime-pair weights, not geometry-only "
                    "claims."),
                "exact_obligation_source": (
                    "evidence/q286-first-three-residue-pair-correlation-obligation.json"),
                "proved": False,
            },
        ],
        "condensation_target": {
            "short_statement": (
                "If the q286 signed-projection anti-alignment theorem, the "
                "conditioned lower-support/complement rescue, and the "
                "finite/endpoint/outer assembly joints are proved, condense "
                "the route into a single conditional Goldbach theorem stack."),
            "condense_only_after": [
                "joint.q286_first_three_signed_projection",
                "joint.lower_support_or_complement_rescue",
                "joint.boundary_and_endpoint_assembly",
                "joint.external_prime_correlation_input",
            ],
            "current_status": "not ready to condense into a proof",
        },
        "next_non_circular_action": (
            "Attack the first two dominant q286 first-three singular "
            "character coordinates directly: seek pointwise lower bounds or "
            "a structural exclusion of simultaneous strong negativity, or "
            "prove/cite that this joint requires an external fixed-modulus "
            "binary Goldbach/AP theorem."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
