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
    singular_mode_obligation = load_json(
        "evidence/q286-first-three-singular-mode-residue-obligation.json")
    dominant_mode_obstruction = load_json(
        "evidence/q286-first-three-dominant-mode-reflection-support-obstruction.json")
    dominant_mode_character_sum = load_json(
        "evidence/q286-first-three-dominant-mode-character-sum-obligation.json")
    dominant_mode_channel_budget = load_json(
        "evidence/q286-first-three-dominant-mode-channel-norm-budget.json")
    dominant_mode_signed_profile = load_json(
        "evidence/q286-first-three-dominant-mode-signed-channel-profile.json")
    dominant_mode_branch_sample = load_json(
        "evidence/q286-first-three-dominant-mode-signed-channel-branch-sample.json")
    dominant_mode_swing_pairs = load_json(
        "evidence/q286-first-three-dominant-mode-channel-swing-pairs.json")
    dominant_mode_helpful_portfolio = load_json(
        "evidence/q286-first-three-dominant-mode-helpful-portfolio.json")
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
                "id": "anchor.singular_mode_residue_obligation",
                "source": (
                    "evidence/q286-first-three-singular-mode-residue-obligation.json"),
                "statement": (
                    "Each rank-three q286 first-three singular mode is an "
                    "exact centered residue-discrepancy projection against "
                    "a mode coefficient gamma_{a,j}(u)."),
                "validation": (
                    "dominant modes "
                    f"{singular_mode_obligation['dominant_modes']} are "
                    "same-sign negative on "
                    f"{singular_mode_obligation['same_sign_dominant_target_count']} "
                    "sample rows; dominant-mode failure targets "
                    f"{singular_mode_obligation['dominant_mode_failure_targets']}; "
                    "maximum mode identity error "
                    f"{singular_mode_obligation['maximum_mode_identity_error']}."),
                "proved_scope": (
                    "exact finite singular-mode residue identity and sample "
                    "classification"),
            },
            {
                "id": "anchor.dominant_mode_reflection_support_obstruction",
                "source": (
                    "evidence/q286-first-three-dominant-mode-reflection-support-obstruction.json"),
                "statement": (
                    "Support, nonnegativity, total mass, and ordered "
                    "prime-pair reflection symmetry alone do not force the "
                    "dominant singular mode-1/mode-2 sum above -0.3."),
                "validation": (
                    "positive reflected synthetic witnesses exist for "
                    f"{dominant_mode_obstruction['positive_witness_even_target_residue_count']} "
                    "of "
                    f"{dominant_mode_obstruction['even_target_residue_count']} "
                    "even target residues modulo 286; least-negative "
                    "extremal row "
                    f"{dominant_mode_obstruction['least_negative_extremal_row']['target_residue']} "
                    "has ratio about "
                    f"{dominant_mode_obstruction['least_negative_extremal_row']['minimum_extremal_dominant_mode_to_principal_ratio']}."),
                "proved_scope": (
                    "finite-vector obstruction to a geometry-only dominant "
                    "mode proof"),
            },
            {
                "id": "anchor.dominant_mode_character_sum_obligation",
                "source": (
                    "evidence/q286-first-three-dominant-mode-character-sum-obligation.json"),
                "statement": (
                    "The surviving dominant singular mode-1/mode-2 residual "
                    "is an exact fixed-modulus q286 character-sum obligation."),
                "validation": (
                    "active complex characters "
                    f"{dominant_mode_character_sum['active_complex_character_count']}; "
                    "real channels "
                    f"{dominant_mode_character_sum['active_real_channel_count']}; "
                    "maximum real-channel identity error "
                    f"{dominant_mode_character_sum['maximum_real_channel_identity_error']}."),
                "proved_scope": (
                    "exact finite character-sum identity and theorem "
                    "obligation, not a pointwise estimate"),
            },
            {
                "id": "anchor.dominant_mode_channel_norm_budget",
                "source": (
                    "evidence/q286-first-three-dominant-mode-channel-norm-budget.json"),
                "statement": (
                    "Plain independent Linf/L2 smallness of the 25 real "
                    "dominant channels is sufficient but too blunt on the "
                    "current near-boundary samples."),
                "validation": (
                    "Linf threshold "
                    f"{dominant_mode_channel_budget['linf_sufficient_relative_channel_sum']}; "
                    "L2 threshold "
                    f"{dominant_mode_channel_budget['l2_sufficient_relative_channel_sum']}; "
                    "budget-failing but floor-passing targets "
                    f"{dominant_mode_channel_budget['bound_failure_but_dominant_floor_pass_targets']}."),
                "proved_scope": (
                    "finite sufficient-condition budget and sample demotion, "
                    "not a pointwise theorem"),
            },
            {
                "id": "anchor.dominant_mode_signed_channel_profile",
                "source": (
                    "evidence/q286-first-three-dominant-mode-signed-channel-profile.json"),
                "statement": (
                    "The 25 real dominant channels split into exact positive "
                    "offset and negative pressure ledgers."),
                "validation": (
                    "floor failures "
                    f"{dominant_mode_signed_profile['dominant_floor_failure_targets']}; "
                    "floor passes "
                    f"{dominant_mode_signed_profile['dominant_floor_pass_targets']}; "
                    "maximum real-channel identity error "
                    f"{dominant_mode_signed_profile['maximum_real_channel_identity_error']}."),
                "proved_scope": (
                    "finite signed-channel profile, not a cancellation "
                    "theorem"),
            },
            {
                "id": "anchor.dominant_mode_signed_channel_branch_sample",
                "source": (
                    "evidence/q286-first-three-dominant-mode-signed-channel-branch-sample.json"),
                "statement": (
                    "The exact pressure/offset branch split was checked on "
                    "deterministic near-boundary mass-matched samples."),
                "validation": (
                    "unresolved deficits "
                    f"{dominant_mode_branch_sample['unresolved_deficit_targets']}; "
                    "offset clears "
                    f"{dominant_mode_branch_sample['offset_branch_targets']}; "
                    "pressure-and-offset clears "
                    f"{dominant_mode_branch_sample['pressure_and_offset_branch_targets']}; "
                    "pressure-only clears "
                    f"{dominant_mode_branch_sample['pressure_branch_targets']}."),
                "proved_scope": (
                    "finite branch-sample classification, not an eventual "
                    "branch theorem"),
            },
            {
                "id": "anchor.dominant_mode_channel_swing_pairs",
                "source": (
                    "evidence/q286-first-three-dominant-mode-channel-swing-pairs.json"),
                "statement": (
                    "Selected deficit-to-clear swings decompose into a "
                    "recurrent but multi-channel helpful portfolio."),
                "validation": (
                    "universal helpful channels "
                    f"{dominant_mode_swing_pairs['universally_helpful_channel_rows'][:2]}; "
                    "maximum channels needed for 80 percent helpful delta "
                    f"{dominant_mode_swing_pairs['maximum_channel_count_for_80_percent_row']['helpful_channel_count_for_80_percent']}; "
                    "maximum reconstruction error "
                    f"{dominant_mode_swing_pairs['maximum_swing_reconstruction_error']}."),
                "proved_scope": (
                    "finite pairwise channel-swing decomposition, not an "
                    "offset theorem"),
            },
            {
                "id": "anchor.dominant_mode_helpful_portfolio",
                "source": (
                    "evidence/q286-first-three-dominant-mode-helpful-portfolio.json"),
                "statement": (
                    "Fixed helpful-channel portfolios separate the selected "
                    "clear rows from selected deficits, while preserving the "
                    "nonportfolio residual."),
                "validation": (
                    "universal separates "
                    f"{dominant_mode_helpful_portfolio['universal_portfolio_separates_clear_from_deficit_on_samples']}; "
                    "recurrent separates "
                    f"{dominant_mode_helpful_portfolio['recurrent_portfolio_separates_clear_from_deficit_on_samples']}; "
                    "recurrent channel count "
                    f"{dominant_mode_helpful_portfolio['portfolio_rows']['recurrent_helpful']['channel_count']}."),
                "proved_scope": (
                    "finite fixed-portfolio diagnostic, not a portfolio "
                    "lower-bound theorem"),
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
            {
                "id": "joint.dominant_singular_mode_projection",
                "statement": (
                    "Prove a pointwise lower bound for the combined q286 "
                    "singular-mode-1 and singular-mode-2 residue projection, "
                    "equivalently control the 25 real q286 character channels "
                    "now identified for that projection.  After the norm "
                    "budget demotion, either control negative-channel "
                    "pressure below 0.3 or prove enough positive offset when "
                    "that pressure exceeds 0.3; the wider branch sample "
                    "currently points toward the offset-under-pressure side, "
                    "and the swing-pair autopsy points to a recurrent "
                    "helpful-channel portfolio rather than one or two "
                    "channels; the fixed-portfolio diagnostic keeps the "
                    "nonportfolio residual explicit."),
                "why_it_is_needed": (
                    "The current samples are not saved by cancellation among "
                    "the leading modes; the tail row is already below -0.3 "
                    "in modes 1+2, while the near-clear rows stay above it. "
                    "Support/reflection geometry alone is obstructed, and "
                    "selected clear rows can have large negative pressure."),
                "exact_obligation_source": (
                    "evidence/q286-first-three-dominant-mode-character-sum-obligation.json"),
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
                "joint.dominant_singular_mode_projection",
            ],
            "current_status": "not ready to condense into a proof",
        },
        "next_non_circular_action": (
            "Attack the first two dominant q286 first-three singular "
            "character coordinates directly: seek an arithmetic mechanism "
            "forcing the recurrent helpful-channel portfolio under large "
            "negative pressure while controlling the nonportfolio residual, "
            "classify the true deficit rows, or prove/cite that this joint "
            "requires an external fixed-modulus binary Goldbach/AP theorem."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
