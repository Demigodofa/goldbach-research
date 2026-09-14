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
    dominant_mode_portfolio_residual = load_json(
        "evidence/q286-first-three-dominant-mode-portfolio-residual-obligation.json")
    dominant_mode_residual_profile = load_json(
        "evidence/q286-first-three-dominant-mode-residual-channel-profile.json")
    dominant_mode_portfolio_ablation = load_json(
        "evidence/q286-first-three-dominant-mode-portfolio-ablation.json")
    dominant_mode_prefix_tail = load_json(
        "evidence/q286-first-three-dominant-mode-prefix-tail-classification.json")
    dominant_mode_tail_ablation = load_json(
        "evidence/q286-first-three-dominant-mode-tail-ablation.json")
    dominant_mode_residual_staircase = load_json(
        "evidence/q286-first-three-dominant-mode-residual-staircase.json")
    dominant_mode_staircase_geometry = load_json(
        "evidence/q286-first-three-dominant-mode-staircase-geometry-obstruction.json")
    dominant_mode_staircase_arithmetic_gap = load_json(
        "evidence/q286-first-three-dominant-mode-staircase-arithmetic-gap.json")
    dominant_mode_staircase_orbit_mass_gap = load_json(
        "evidence/q286-first-three-dominant-mode-staircase-orbit-mass-gap.json")
    dominant_mode_staircase_hinge = load_json(
        "evidence/q286-first-three-dominant-mode-staircase-hinge-decomposition.json")
    dominant_mode_staircase_hinge_threshold = load_json(
        "evidence/q286-first-three-dominant-mode-staircase-hinge-threshold.json")
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
                "id": "anchor.dominant_mode_portfolio_residual_obligation",
                "source": (
                    "evidence/q286-first-three-dominant-mode-portfolio-residual-obligation.json"),
                "statement": (
                    "The recurrent helpful portfolio plus the nonportfolio "
                    "residual reconstructs selected dominant rows exactly, "
                    "and the -0.3 floor is equivalent row by row to a "
                    "required portfolio lower bound."),
                "validation": (
                    "portfolio channel count "
                    f"{dominant_mode_portfolio_residual['portfolio_channel_count']}; "
                    "residual channel count "
                    f"{dominant_mode_portfolio_residual['residual_channel_count']}; "
                    "maximum identity error "
                    f"{dominant_mode_portfolio_residual['maximum_identity_error']}; "
                    "worst slack target "
                    f"{dominant_mode_portfolio_residual['worst_floor_slack_row']['target']} "
                    "with slack "
                    f"{dominant_mode_portfolio_residual['worst_floor_slack_row']['portfolio_slack_to_floor']}."),
                "proved_scope": (
                    "finite exact portfolio/residual obligation, not a "
                    "portfolio or residual theorem"),
            },
            {
                "id": "anchor.dominant_mode_residual_channel_profile",
                "source": (
                    "evidence/q286-first-three-dominant-mode-residual-channel-profile.json"),
                "statement": (
                    "The residual channels left after subtracting the "
                    "recurrent portfolio do not provide a one-channel "
                    "separator or a residual rescue on the selected pairs."),
                "validation": (
                    "residual channel count "
                    f"{dominant_mode_residual_profile['residual_channel_count']}; "
                    "separating residual channels "
                    f"{dominant_mode_residual_profile['separating_residual_channel_count']}; "
                    "harshest residual target "
                    f"{dominant_mode_residual_profile['harshest_residual_sum_row']['target']}; "
                    "maximum identity error "
                    f"{dominant_mode_residual_profile['maximum_residual_identity_error']}."),
                "proved_scope": (
                    "finite residual-channel diagnostic and demoted shortcut, "
                    "not a residual theorem"),
            },
            {
                "id": "anchor.dominant_mode_portfolio_ablation",
                "source": (
                    "evidence/q286-first-three-dominant-mode-portfolio-ablation.json"),
                "statement": (
                    "Ablating the recurrent portfolio separates the "
                    "clear-side lower-bound target from exact selected "
                    "deficit/clear classification."),
                "validation": (
                    "portfolio channel count "
                    f"{dominant_mode_portfolio_ablation['portfolio_channel_count']}; "
                    "clear-essential channels "
                    f"{dominant_mode_portfolio_ablation['clear_essential_channel_count']}; "
                    "classification-essential channels "
                    f"{dominant_mode_portfolio_ablation['classification_essential_channel_count']}; "
                    "first prefix clearing all original clears "
                    f"{dominant_mode_portfolio_ablation['first_prefix_clearing_all_original_clears']['channel_count']}; "
                    "first prefix matching classification "
                    f"{dominant_mode_portfolio_ablation['first_prefix_matching_classification']['channel_count']}."),
                "proved_scope": (
                    "finite recurrent-portfolio ablation, not a portfolio "
                    "lower-bound theorem"),
            },
            {
                "id": "anchor.dominant_mode_prefix_tail_classification",
                "source": (
                    "evidence/q286-first-three-dominant-mode-prefix-tail-classification.json"),
                "statement": (
                    "The recurrent portfolio splits into a clear-preserving "
                    "prefix and a classification tail with exact rowwise "
                    "tail obligation."),
                "validation": (
                    "prefix channel count "
                    f"{dominant_mode_prefix_tail['prefix_channel_count']}; "
                    "tail channel count "
                    f"{dominant_mode_prefix_tail['tail_channel_count']}; "
                    "overrescued failures "
                    f"{dominant_mode_prefix_tail['overrescued_failure_targets']}; "
                    "tail restores all overrescued failures "
                    f"{dominant_mode_prefix_tail['tail_restores_all_overrescued_failures']}"),
                "proved_scope": (
                    "finite exact prefix/tail diagnostic, not a prefix or "
                    "tail theorem"),
            },
            {
                "id": "anchor.dominant_mode_tail_ablation",
                "source": (
                    "evidence/q286-first-three-dominant-mode-tail-ablation.json"),
                "statement": (
                    "The selected classification tail is not compressed by "
                    "leave-one-out or prefix ablation."),
                "validation": (
                    "tail channel count "
                    f"{dominant_mode_tail_ablation['tail_channel_count']}; "
                    "classification-essential channels "
                    f"{dominant_mode_tail_ablation['classification_essential_channel_count']}; "
                    "first successful tail prefix "
                    f"{dominant_mode_tail_ablation['first_tail_prefix_matching_classification']['tail_prefix_channel_count']}."),
                "proved_scope": (
                    "finite tail ablation and demoted compression route, not "
                    "a tail theorem"),
            },
            {
                "id": "anchor.dominant_mode_residual_staircase",
                "source": (
                    "evidence/q286-first-three-dominant-mode-residual-staircase.json"),
                "statement": (
                    "The selected prefix/tail order is an exact cumulative "
                    "residual ledger: after each bolt-on, the remaining "
                    "rowwise portfolio requirement is measured."),
                "validation": (
                    "first stage clearing all selected clears "
                    f"{dominant_mode_residual_staircase['first_stage_clearing_all_original_clears']['stage_name']}; "
                    "first stage matching classification "
                    f"{dominant_mode_residual_staircase['first_stage_matching_classification']['stage_name']}; "
                    "prefix overrescued failures "
                    f"{dominant_mode_residual_staircase['prefix_stage']['overrescued_failure_targets']}; "
                    "full-stage maximum failure slack "
                    f"{dominant_mode_residual_staircase['full_stage']['failure_slack_summary']['maximum']}."),
                "proved_scope": (
                    "finite cumulative residual diagnostic, not a cumulative "
                    "portfolio theorem"),
            },
            {
                "id": "anchor.dominant_mode_staircase_geometry_obstruction",
                "source": (
                    "evidence/q286-first-three-dominant-mode-staircase-geometry-obstruction.json"),
                "statement": (
                    "Weak support, nonnegativity, total mass, and pair-swap "
                    "reflection geometry do not force the frozen residual "
                    "staircase classifications."),
                "validation": (
                    "full-stage pass breakable targets "
                    f"{dominant_mode_staircase_geometry['full_stage_pass_targets_breakable_by_weak_geometry']}; "
                    "full-stage fail breakable targets "
                    f"{dominant_mode_staircase_geometry['full_stage_fail_targets_breakable_by_weak_geometry']}; "
                    "full-stage forced targets "
                    f"{dominant_mode_staircase_geometry['full_stage_classification_forced_targets']}."),
                "proved_scope": (
                    "finite weak-geometry obstruction using synthetic "
                    "reflected weights, not prime-pair weights"),
            },
            {
                "id": "anchor.dominant_mode_staircase_arithmetic_gap",
                "source": (
                    "evidence/q286-first-three-dominant-mode-staircase-arithmetic-gap.json"),
                "statement": (
                    "Actual strict-central prime-pair rows are placed inside "
                    "the weak-geometry intervals; the remaining theorem is "
                    "one-sided arithmetic placement, not interval shrinkage."),
                "validation": (
                    "full-stage pass position range "
                    f"{dominant_mode_staircase_arithmetic_gap['full_stage']['pass_actual_position_summary']['minimum']}.."
                    f"{dominant_mode_staircase_arithmetic_gap['full_stage']['pass_actual_position_summary']['maximum']}; "
                    "full-stage fail position range "
                    f"{dominant_mode_staircase_arithmetic_gap['full_stage']['fail_actual_position_summary']['minimum']}.."
                    f"{dominant_mode_staircase_arithmetic_gap['full_stage']['fail_actual_position_summary']['maximum']}; "
                    "tightest pass target "
                    f"{dominant_mode_staircase_arithmetic_gap['full_stage_tightest_pass_row']['target']}; "
                    "tightest fail target "
                    f"{dominant_mode_staircase_arithmetic_gap['full_stage_tightest_fail_row']['target']}."),
                "proved_scope": (
                    "finite arithmetic-gap diagnostic, not a pointwise "
                    "prime-correlation theorem"),
            },
            {
                "id": "anchor.dominant_mode_staircase_orbit_mass_gap",
                "source": (
                    "evidence/q286-first-three-dominant-mode-staircase-orbit-mass-gap.json"),
                "statement": (
                    "The weak synthetic obstruction breaks selected rows by "
                    "concentrating mass on an extremal reflected orbit, but "
                    "actual strict-central prime-pair mass is not visibly "
                    "concentrated on those breaker orbits."),
                "validation": (
                    "full-stage breaker mass fraction range "
                    f"{dominant_mode_staircase_orbit_mass_gap['full_stage']['breaking_extremal_orbit_mass_fraction_summary']['minimum']}.."
                    f"{dominant_mode_staircase_orbit_mass_gap['full_stage']['breaking_extremal_orbit_mass_fraction_summary']['maximum']}; "
                    "top actual orbit mass range "
                    f"{dominant_mode_staircase_orbit_mass_gap['full_stage']['top_actual_orbit_mass_fraction_summary']['minimum']}.."
                    f"{dominant_mode_staircase_orbit_mass_gap['full_stage']['top_actual_orbit_mass_fraction_summary']['maximum']}; "
                    "breaker orbit top-actual count "
                    f"{dominant_mode_staircase_orbit_mass_gap['full_stage']['breaking_orbit_top_actual_count']}."),
                "proved_scope": (
                    "finite orbit-mass diagnostic, not an orbit-mass theorem "
                    "or pointwise prime-correlation theorem"),
            },
            {
                "id": "anchor.dominant_mode_staircase_hinge_decomposition",
                "source": (
                    "evidence/q286-first-three-dominant-mode-staircase-hinge-decomposition.json"),
                "statement": (
                    "The selected staircase slack decomposes exactly into "
                    "actual above-floor positive hinge minus below-floor "
                    "negative hinge; the sampled mechanism is mixed mass and "
                    "landing quality rather than one-dimensional mass or "
                    "landing control."),
                "validation": (
                    "maximum hinge identity error "
                    f"{dominant_mode_staircase_hinge['maximum_hinge_identity_error']}; "
                    "full-stage supporting mass range "
                    f"{dominant_mode_staircase_hinge['full_stage']['classification_supporting_mass_summary']['minimum']}.."
                    f"{dominant_mode_staircase_hinge['full_stage']['classification_supporting_mass_summary']['maximum']}; "
                    "opposing mass range "
                    f"{dominant_mode_staircase_hinge['full_stage']['classification_opposing_mass_summary']['minimum']}.."
                    f"{dominant_mode_staircase_hinge['full_stage']['classification_opposing_mass_summary']['maximum']}."),
                "proved_scope": (
                    "finite exact hinge identity and diagnostic, not a "
                    "hinge-balance theorem"),
            },
            {
                "id": "anchor.dominant_mode_staircase_hinge_threshold",
                "source": (
                    "evidence/q286-first-three-dominant-mode-staircase-hinge-threshold.json"),
                "statement": (
                    "The mixed hinge balance is exactly equivalent to a "
                    "support-mass threshold surplus "
                    "supporting_mass - L_o/(L_s+L_o) >= 0."),
                "validation": (
                    "full-stage surplus range "
                    f"{dominant_mode_staircase_hinge_threshold['full_stage']['hinge_support_mass_surplus_summary']['minimum']}.."
                    f"{dominant_mode_staircase_hinge_threshold['full_stage']['hinge_support_mass_surplus_summary']['maximum']}; "
                    "tightest surplus target "
                    f"{dominant_mode_staircase_hinge_threshold['full_stage_tightest_surplus_row']['target']}; "
                    "maximum threshold identity error "
                    f"{dominant_mode_staircase_hinge_threshold['maximum_hinge_threshold_identity_error']}."),
                "proved_scope": (
                    "finite exact threshold-obligation form; support side is "
                    "still inherited from finite classification"),
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
                    "equivalent portfolio/residual floor when norms are "
                    "nonzero."),
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
                    "equivalently prove the recurrent helpful-channel "
                    "portfolio or its clear-side prefix lower bound against "
                    "the rowwise residual requirement, plus a tail "
                    "classification package or separate exclusion/complement "
                    "theorem for prefix-overrescued deficits. "
                    "The norm budget, tiny-channel, small residual-channel "
                    "classifier, and geometry-only routes are demoted on the "
                    "current evidence; the residual staircase shows the tail "
                    "is signed rather than a monotone-positive reserve, and "
                    "the weak-geometry staircase obstruction shows support/"
                    "reflection constraints alone do not force the selected "
                    "classifications.  The arithmetic-gap receipt then shows "
                    "the remaining task is one-sided placement of actual "
                    "prime-pair rows inside a broad weak interval.  The "
                    "orbit-mass gap receipt sharpens that placement problem "
                    "to control of the extremal reflected breaker orbits "
                    "used by the weak synthetic witnesses.  The hinge "
                    "decomposition then shows the selected fixture is a "
                    "mixed mass-and-landing balance, not a one-dimensional "
                    "mass cap or landing floor."),
                "why_it_is_needed": (
                    "The current samples are not saved by cancellation among "
                    "the leading modes; the tail row is already below -0.3 "
                    "in modes 1+2, while the near-clear rows stay above it. "
                    "Support/reflection geometry alone is obstructed, and "
                    "selected clear rows can have large negative pressure."),
                "exact_obligation_source": (
                    "evidence/q286-first-three-dominant-mode-portfolio-residual-obligation.json"),
                "proved": False,
            },
            {
                "id": "joint.dangerous_reflection_orbit_mass_bound",
                "statement": (
                    "For the q286 dominant-mode staircase, prove a pointwise "
                    "bound or signed aggregate replacement controlling actual "
                    "strict-central prime-pair mass on the extremal reflected "
                    "orbits that would break each cumulative stage."),
                "why_it_is_needed": (
                    "Weak geometry fails by synthetic concentration on "
                    "specific breaker orbits.  On the selected fixture, those "
                    "breaker orbits are never the top actual mass orbit and "
                    "sometimes carry zero actual mass, but this is finite "
                    "evidence only."),
                "exact_obligation_source": (
                    "evidence/q286-first-three-dominant-mode-staircase-orbit-mass-gap.json"),
                "proved": False,
            },
            {
                "id": "joint.dominant_staircase_hinge_balance",
                "statement": (
                    "For the q286 dominant-mode staircase, prove the exact "
                    "row-dependent hinge balance: actual mass above each "
                    "row floor times positive landing quality must dominate "
                    "the below-floor hinge for pass rows, while the reverse "
                    "or an exclusion/complement mechanism handles deficit "
                    "rows."),
                "why_it_is_needed": (
                    "The full-stage selected rows are split between "
                    "mass-driven and landing-driven classifications; neither "
                    "a simple mass cap nor a simple landing floor matches the "
                    "observed finite mechanism."),
                "exact_obligation_source": (
                    "evidence/q286-first-three-dominant-mode-staircase-hinge-decomposition.json"),
                "proved": False,
            },
            {
                "id": "joint.dominant_staircase_hinge_threshold_surplus",
                "statement": (
                    "Prove a positive surplus over the landing-dependent "
                    "hinge threshold "
                    "supporting_mass >= opposing_landing / "
                    "(supporting_landing + opposing_landing), with a "
                    "non-circular arithmetic definition of the intended "
                    "support side."),
                "why_it_is_needed": (
                    "The selected full-stage surplus is tiny; the tightest "
                    "row has only about "
                    f"{dominant_mode_staircase_hinge_threshold['full_stage_tightest_surplus_row']['hinge_support_mass_surplus_to_threshold']} "
                    "mass fraction of slack over threshold."),
                "exact_obligation_source": (
                    "evidence/q286-first-three-dominant-mode-staircase-hinge-threshold.json"),
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
                "joint.dangerous_reflection_orbit_mass_bound",
                "joint.dominant_staircase_hinge_balance",
                "joint.dominant_staircase_hinge_threshold_surplus",
            ],
            "current_status": "not ready to condense into a proof",
        },
        "next_non_circular_action": (
            "Attack the first two dominant q286 first-three singular "
            "character coordinates directly: seek an arithmetic mechanism "
            "forcing the recurrent helpful-channel portfolio under large "
            "negative pressure while controlling the nonportfolio residual, "
            "classify the true deficit rows, or prove/cite that this joint "
            "requires an external fixed-modulus binary Goldbach/AP theorem.  "
            "A sharper near-term version is to prove that actual prime-pair "
            "mass cannot concentrate on the dangerous reflected breaker "
            "orbits identified by the weak-geometry obstruction, then prove "
            "the mixed hinge-balance inequality left after that localization. "
            "The narrowest current form is a positive support-mass surplus "
            "over the landing-dependent threshold, with the support side "
            "defined arithmetically rather than post hoc."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
