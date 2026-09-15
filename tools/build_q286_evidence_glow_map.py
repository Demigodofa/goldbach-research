"""Build a compact q286 evidence glow map from checked graph/evidence files.

The output is a visualization-ready data layer.  "Glow" means independent
recorded evidence layers overlap on the same target, mechanism, or theorem
gap.  It is not a proof score.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
NOTES = ROOT / "notes"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def add_hit(stacks, key, layer_id, weight, reason, value=None):
    stack = stacks.setdefault(key, {
        "id": key,
        "stack_weight": 0.0,
        "layers": [],
    })
    stack["stack_weight"] += weight
    hit = {"layer": layer_id, "weight": weight, "reason": reason}
    if value is not None:
        hit["value"] = value
    stack["layers"].append(hit)


def sorted_stacks(stacks):
    rows = []
    max_weight = max((row["stack_weight"] for row in stacks.values()), default=1.0)
    for row in stacks.values():
        row = dict(row)
        row["layer_count"] = len(row["layers"])
        row["glow"] = round(row["stack_weight"] / max_weight, 6)
        rows.append(row)
    return sorted(rows, key=lambda item: (-item["stack_weight"], item["id"]))


def main():
    graph = load_json(NOTES / "q286-closed-lanes-map.graph.json")
    denominator = load_json(EVIDENCE / "q286-active-lane-sampling-denominator-map.json")
    strict = load_json(
        EVIDENCE / "q286-active-lane-strict-closure-margin-census-selected-late.json")
    fixed = load_json(EVIDENCE / "q286-fixed-inequality-target-window-census.json")
    late_zero = load_json(EVIDENCE / "q286-tail-alignment-complement-window-233-264.json")
    portfolio_residual = load_json(
        EVIDENCE / "q286-first-three-dominant-mode-portfolio-residual-obligation.json")
    residual_profile = load_json(
        EVIDENCE / "q286-first-three-dominant-mode-residual-channel-profile.json")
    portfolio_ablation = load_json(
        EVIDENCE / "q286-first-three-dominant-mode-portfolio-ablation.json")
    prefix_tail = load_json(
        EVIDENCE / "q286-first-three-dominant-mode-prefix-tail-classification.json")
    tail_ablation = load_json(
        EVIDENCE / "q286-first-three-dominant-mode-tail-ablation.json")
    residual_staircase = load_json(
        EVIDENCE / "q286-first-three-dominant-mode-residual-staircase.json")
    staircase_geometry = load_json(
        EVIDENCE
        / "q286-first-three-dominant-mode-staircase-geometry-obstruction.json")
    staircase_arithmetic_gap = load_json(
        EVIDENCE
        / "q286-first-three-dominant-mode-staircase-arithmetic-gap.json")
    staircase_orbit_mass_gap = load_json(
        EVIDENCE
        / "q286-first-three-dominant-mode-staircase-orbit-mass-gap.json")
    staircase_hinge = load_json(
        EVIDENCE
        / "q286-first-three-dominant-mode-staircase-hinge-decomposition.json")
    staircase_hinge_threshold = load_json(
        EVIDENCE
        / "q286-first-three-dominant-mode-staircase-hinge-threshold.json")
    staircase_above_floor = load_json(
        EVIDENCE
        / "q286-first-three-dominant-mode-staircase-above-floor-threshold.json")
    above_floor_holdout = load_json(
        EVIDENCE
        / "q286-first-three-dominant-mode-above-floor-holdout-census.json")
    selector_audit = load_json(
        EVIDENCE
        / "q286-first-three-dominant-mode-near-boundary-selector-audit.json")
    outside_rank1 = load_json(
        EVIDENCE
        / "q286-first-three-dominant-mode-outside-plane-remainder-octave-rank1-audit.json")
    residual_drag = load_json(
        EVIDENCE
        / "q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-ledger.json")
    residual_drag_full_window = load_json(
        EVIDENCE
        / "q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-full-window-audit.json")
    residual_drag_channel_certificate = load_json(
        EVIDENCE
        / "q286-first-three-dominant-mode-residual-drag-channel-certificate-falsifier.json")
    lift_project_dictionary = load_json(
        EVIDENCE / "q286-lift-project-dictionary-audit.json")
    low_frequency_lift_holdout = load_json(
        EVIDENCE / "q286-low-frequency-lift-holdout.json")
    target_residue_lift_holdout = load_json(
        EVIDENCE / "q286-target-residue-lift-holdout.json")
    low_frequency_lift_horizon = load_json(
        EVIDENCE / "q286-low-frequency-lift-horizon-holdout.json")
    frobenius_lattice_claim = load_json(
        EVIDENCE / "q286-frobenius-lattice-claim-audit.json")
    low_frequency_lp_cone = load_json(
        EVIDENCE / "q286-low-frequency-lp-cone-audit.json")
    low_frequency_lp_cone_stress = load_json(
        EVIDENCE / "q286-low-frequency-lp-cone-stress-holdout.json")
    lp_cone_local_singular = load_json(
        EVIDENCE / "q286-lp-cone-local-singular-audit.json")
    zero_local_decomposition = load_json(
        EVIDENCE / "q286-zero-local-target-channel-decomposition.json")
    zero_local_margin_audit = load_json(
        EVIDENCE / "q286-zero-local-channel-margin-audit.json")
    far_singleton_channel_stability = load_json(
        EVIDENCE / "q286-far-singleton-channel-stability-audit.json")
    fresh_window_channel_watchlist = load_json(
        EVIDENCE / "q286-fresh-window-channel-watchlist-audit.json")
    alternate_reference_channel = load_json(
        EVIDENCE / "q286-alternate-reference-channel-audit.json")
    centered_channel_scalar_order = load_json(
        EVIDENCE / "q286-centered-channel-scalar-order-audit.json")
    centered_3_1_reference_lemma = load_json(
        EVIDENCE / "q286-centered-3-1-reference-lemma-audit.json")
    centered_3_1_residue_collision = load_json(
        EVIDENCE / "q286-centered-3-1-residue-collision-audit.json")
    centered_3_1_same_residue_fresh = load_json(
        EVIDENCE
        / "q286-centered-3-1-same-residue-fresh-population-audit.json")
    centered_3_1_signed_gap_obligation = load_json(
        EVIDENCE / "q286-centered-3-1-signed-gap-obligation.json")
    centered_3_1_available_same_residue = load_json(
        EVIDENCE
        / "q286-centered-3-1-available-same-residue-population-audit.json")
    centered_3_1_residue5_horizon = load_json(
        EVIDENCE / "q286-centered-3-1-residue5-near-collision-horizon.json")
    centered_3_1_residue5_multichannel = load_json(
        EVIDENCE / "q286-centered-3-1-residue5-multichannel-horizon.json")
    multichannel_selected_reference_horizon = load_json(
        EVIDENCE / "q286-multichannel-selected-reference-horizon-audit.json")
    watchlist_fresh_unseen_window = load_json(
        EVIDENCE / "q286-watchlist-fresh-unseen-window-audit.json")
    centered_3_1_stress_classifier_boundary = load_json(
        EVIDENCE / "q286-centered-3-1-stress-classifier-boundary.json")
    selected_stress_subclass = load_json(
        EVIDENCE / "q286-selected-stress-subclass-audit.json")
    selected_stress_subclass_channel_decomposition = load_json(
        EVIDENCE
        / "q286-selected-stress-subclass-channel-decomposition.json")
    additional_stress_reference_generalization = load_json(
        EVIDENCE
        / "q286-additional-stress-reference-generalization-audit.json")
    selected_reference_scope_fork = load_json(
        EVIDENCE / "q286-selected-reference-scope-fork-audit.json")
    selected_stable_fixture_family_boundary = load_json(
        EVIDENCE
        / "q286-selected-stable-fixture-family-boundary-audit.json")
    centered_3_1_threshold_subclass = load_json(
        EVIDENCE / "q286-centered-3-1-threshold-subclass-audit.json")
    independent_stress_feature = load_json(
        EVIDENCE / "q286-independent-stress-feature-audit.json")
    centered_3_1_stress_class = load_json(
        EVIDENCE / "q286-centered-3-1-stress-class-audit.json")
    selected_deficit_provenance = load_json(
        EVIDENCE / "q286-selected-deficit-provenance-audit.json")
    ap_count_bridge_gap = load_json(
        EVIDENCE / "q286-ap-count-bridge-gap-audit.json")

    target_stacks = {}
    mechanism_stacks = {}
    theorem_stacks = {}
    layers = []

    def layer(layer_id, label, kind, source, weight, boundary):
        layers.append({
            "id": layer_id,
            "label": label,
            "kind": kind,
            "source": source,
            "default_weight": weight,
            "boundary": boundary,
        })

    layer(
        "graph-target-roles",
        "Closed-lanes graph target roles",
        "graph_metadata",
        "notes/q286-closed-lanes-map.graph.json",
        1.0,
        "Graph role only; not a new computation.")
    for node in graph["nodes"]:
        if node.get("type") == "target":
            target_id = str(node["label"])
            add_hit(
                target_stacks,
                target_id,
                "graph-target-roles",
                1.0,
                node.get("status", "target_role"),
                node.get("role"))

    layer(
        "strict-closure-selected-late",
        "Selected late active rows have positive strict closure margin",
        "selected_stress",
        "evidence/q286-active-lane-strict-closure-margin-census-selected-late.json",
        3.0,
        "Finite selected-fixture evidence only.")
    for target, row in strict["target_rows"].items():
        add_hit(
            target_stacks,
            target,
            "strict-closure-selected-late",
            3.0,
            "positive strict closure margin",
            row["strict_closure_margin_to_calibrated_endpoint"])
        add_hit(
            mechanism_stacks,
            "channel-carried-strict-slack",
            "strict-closure-selected-late",
            3.0,
            "dominant margin source",
            row["dominant_strict_margin_source"])
    add_hit(
        theorem_stacks,
        "active-lane-strict-closure",
        "strict-closure-selected-late",
        3.0,
        "selected active rows pass calibrated strict closure")

    layer(
        "fixed-inequality-target-window",
        "Tiny active target window passes fixed inequality",
        "selected_local_window",
        "evidence/q286-fixed-inequality-target-window-census.json",
        2.0,
        "Tiny local window; not broad population evidence.")
    fixed_targets = fixed["stress_tested_targets"] if fixed["passing_target_count"] else ()
    for target in fixed_targets:
        add_hit(
            target_stacks,
            str(target),
            "fixed-inequality-target-window",
            2.0,
            "fixed inequality stressed and passed",
            fixed["target_rows"][str(target)]["worst_margin"])
    add_hit(
        mechanism_stacks,
        "fixed-component-pair-((5,7),(7,11))",
        "fixed-inequality-target-window",
        2.0,
        "active component pair stress path passed on tiny window")

    layer(
        "sampling-denominator-map",
        "Selector denominator map separates zero-hit scans from stress rows",
        "denominator_map",
        "evidence/q286-active-lane-sampling-denominator-map.json",
        1.5,
        "Denominator bookkeeping only; sample-size risk remains open.")
    add_hit(
        mechanism_stacks,
        "active-selector-rarity",
        "sampling-denominator-map",
        1.5,
        "zero active rows in broad selector and scout windows",
        {
            "necessary_condition_scout_scanned_target_count": (
                denominator["necessary_condition_scout_scanned_target_count"]),
            "large_contiguous_tail_window_scanned_target_count": (
                denominator.get("large_contiguous_tail_window_scanned_target_count", 0)),
        })
    add_hit(
        theorem_stacks,
        "sample-size-cherry-pick-risk",
        "sampling-denominator-map",
        1.5,
        "risk explicitly left open",
        {
            "sample_size_concern_closed": denominator["sample_size_concern_closed"],
            "cherry_picking_risk_closed": denominator["cherry_picking_risk_closed"],
        })

    layer(
        "post-232-zero-tail-window",
        "Cycles 233..264 have zero .2/.3 first-three tail rows",
        "large_zero_tail_window",
        "evidence/q286-tail-alignment-complement-window-233-264.json",
        2.0,
        "Large finite denominator window only; no stress rows.")
    add_hit(
        mechanism_stacks,
        "tail-thinning-after-cycle-232",
        "post-232-zero-tail-window",
        2.0,
        "zero .2 near-tail and zero .3 deep-tail rows",
        {
            "tested_target_count": late_zero["window"]["tested_target_count"],
            "near_tail_count": late_zero["near_tail_alignment_check"]["tail_target_count"],
            "deep_tail_count": late_zero["deep_tail_alignment_complement_check"][
                "tail_target_count"],
        })
    add_hit(
        theorem_stacks,
        "alignment-complement-route",
        "post-232-zero-tail-window",
        1.0,
        "no falsifier rows in adjacent post-232 window")

    layer(
        "portfolio-residual-obligation",
        "Recurrent portfolio is split from residual requirement",
        "selected_stress",
        "evidence/q286-first-three-dominant-mode-portfolio-residual-obligation.json",
        2.5,
        "Finite selected portfolio/residual split only; no lower-bound theorem.")
    for target, row in portfolio_residual["target_rows"].items():
        reason = (
            "portfolio/residual floor passed"
            if row["dominant_floor_passes"]
            else "portfolio/residual floor failed")
        add_hit(
            target_stacks,
            str(target),
            "portfolio-residual-obligation",
            2.5,
            reason,
            row["portfolio_slack_to_floor"])
    add_hit(
        mechanism_stacks,
        "recurrent-portfolio-versus-residual",
        "portfolio-residual-obligation",
        2.5,
        "dominant floor rewritten as rowwise portfolio lower bound",
        {
            "portfolio_channel_count": (
                portfolio_residual["portfolio_channel_count"]),
            "residual_channel_count": (
                portfolio_residual["residual_channel_count"]),
            "worst_target": (
                portfolio_residual["worst_floor_slack_row"]["target"]),
            "worst_slack": (
                portfolio_residual["worst_floor_slack_row"][
                    "portfolio_slack_to_floor"]),
        })
    add_hit(
        theorem_stacks,
        "portfolio-residual-lower-bound",
        "portfolio-residual-obligation",
        2.5,
        "prove recurrent portfolio lower bound or residual-channel bound")

    layer(
        "residual-channel-profile",
        "Residual channels do not provide selected-pair rescue",
        "selected_stress",
        "evidence/q286-first-three-dominant-mode-residual-channel-profile.json",
        2.0,
        "Finite residual-channel profile only; no residual theorem.")
    for target, row in residual_profile["target_rows"].items():
        add_hit(
            target_stacks,
            str(target),
            "residual-channel-profile",
            2.0,
            "residual signed pressure profiled",
            {
                "residual_sum": row["residual_sum_to_principal"],
                "residual_negative_pressure": (
                    row["residual_negative_pressure_to_principal"]),
                "dominant_floor_passes": row["dominant_floor_passes"],
            })
    add_hit(
        mechanism_stacks,
        "small-residual-channel-classifier-demoted",
        "residual-channel-profile",
        2.0,
        "no individual residual channel separates selected outcomes",
        {
            "separating_residual_channel_count": (
                residual_profile["separating_residual_channel_count"]),
            "harshest_residual_target": (
                residual_profile["harshest_residual_sum_row"]["target"]),
        })
    add_hit(
        theorem_stacks,
        "portfolio-residual-lower-bound",
        "residual-channel-profile",
        2.0,
        "residual pushes against clear side on selected pairs")

    layer(
        "portfolio-ablation",
        "Portfolio ablation splits lower-bound and classification targets",
        "selected_stress",
        "evidence/q286-first-three-dominant-mode-portfolio-ablation.json",
        2.0,
        "Finite recurrent-portfolio ablation only; no portfolio theorem.")
    for target, row in portfolio_ablation["baseline_target_rows"].items():
        add_hit(
            target_stacks,
            str(target),
            "portfolio-ablation",
            2.0,
            "portfolio ablation baseline row",
            {
                "full_portfolio_slack": (
                    row["full_portfolio_slack_to_floor"]),
                "dominant_floor_passes": row["dominant_floor_passes"],
            })
    add_hit(
        mechanism_stacks,
        "clear-side-prefix-versus-deficit-classification",
        "portfolio-ablation",
        2.0,
        "four-channel prefix clears selected clears but over-rescues deficits",
        {
            "clear_prefix_channel_count": (
                portfolio_ablation[
                    "first_prefix_clearing_all_original_clears"][
                    "channel_count"]),
            "classification_prefix_channel_count": (
                portfolio_ablation[
                    "first_prefix_matching_classification"][
                    "channel_count"]),
        })
    add_hit(
        theorem_stacks,
        "portfolio-residual-lower-bound",
        "portfolio-ablation",
        2.0,
        "separate clear-side lower bound from deficit exclusion")

    layer(
        "prefix-tail-classification",
        "Prefix lower bound and tail classification are split exactly",
        "selected_stress",
        "evidence/q286-first-three-dominant-mode-prefix-tail-classification.json",
        2.0,
        "Finite prefix/tail diagnostic only; no prefix or tail theorem.")
    for target, row in prefix_tail["target_rows"].items():
        add_hit(
            target_stacks,
            str(target),
            "prefix-tail-classification",
            2.0,
            "prefix/tail floor obligation",
            {
                "prefix_slack": row["prefix_slack_to_floor"],
                "tail_slack": row["tail_slack_to_full_floor"],
                "dominant_floor_passes": row["dominant_floor_passes"],
            })
    add_hit(
        mechanism_stacks,
        "prefix-lower-bound-plus-tail-classification",
        "prefix-tail-classification",
        2.0,
        "prefix over-rescues deficits and tail restores selected split",
        {
            "prefix_channel_count": prefix_tail["prefix_channel_count"],
            "tail_channel_count": prefix_tail["tail_channel_count"],
            "tail_restores_all_overrescued_failures": (
                prefix_tail["tail_restores_all_overrescued_failures"]),
        })
    add_hit(
        theorem_stacks,
        "portfolio-residual-lower-bound",
        "prefix-tail-classification",
        2.0,
        "prove prefix lower bound plus tail/exclusion theorem")

    layer(
        "tail-ablation",
        "Tail classification is not compressed on selected fixture",
        "selected_stress",
        "evidence/q286-first-three-dominant-mode-tail-ablation.json",
        2.0,
        "Finite tail ablation only; no tail theorem.")
    for row in tail_ablation["full_tail_rows"]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "tail-ablation",
            2.0,
            "tail ablation slack row",
            {
                "subtail_slack": row["subtail_slack_to_full_floor"],
                "dominant_floor_passes": row["dominant_floor_passes"],
            })
    add_hit(
        mechanism_stacks,
        "tail-package-not-compressed",
        "tail-ablation",
        2.0,
        "every selected tail channel is essential under leave-one-out",
        {
            "tail_channel_count": tail_ablation["tail_channel_count"],
            "classification_essential_channel_count": (
                tail_ablation["classification_essential_channel_count"]),
            "first_successful_tail_prefix": (
                tail_ablation[
                    "first_tail_prefix_matching_classification"][
                    "tail_prefix_channel_count"]),
        })
    add_hit(
        theorem_stacks,
        "portfolio-residual-lower-bound",
        "tail-ablation",
        2.0,
        "tail theorem remains seven-channel on selected evidence")

    layer(
        "residual-staircase",
        "Residual staircase records cumulative bolt-on leftovers",
        "selected_stress",
        "evidence/q286-first-three-dominant-mode-residual-staircase.json",
        2.0,
        "Finite cumulative residual ledger only; no portfolio theorem.")
    for stage in residual_staircase["stage_rows"]:
        for row in stage["target_rows"]:
            if (row["remaining_requirement_to_floor"] > 0
                    or row["stage_floor_passes"] != row[
                        "dominant_floor_passes"]):
                add_hit(
                    target_stacks,
                    str(row["target"]),
                    "residual-staircase",
                    2.0,
                    "cumulative residual stage row",
                    {
                        "stage": stage["stage_name"],
                        "remaining_requirement": (
                            row["remaining_requirement_to_floor"]),
                        "stage_floor_passes": row["stage_floor_passes"],
                        "dominant_floor_passes": (
                            row["dominant_floor_passes"]),
                    })
    add_hit(
        mechanism_stacks,
        "signed-cumulative-portfolio-staircase",
        "residual-staircase",
        2.0,
        "prefix clears selected clears but over-rescues deficits; full "
        "portfolio first matches classification",
        {
            "prefix_stage": residual_staircase["prefix_stage"]["stage_name"],
            "prefix_overrescued_failure_targets": (
                residual_staircase["prefix_stage"][
                    "overrescued_failure_targets"]),
            "first_matching_stage": (
                residual_staircase[
                    "first_stage_matching_classification"]["stage_name"]),
        })
    add_hit(
        theorem_stacks,
        "portfolio-residual-lower-bound",
        "residual-staircase",
        2.0,
        "tail is signed cumulative control, not monotone positive reserve")

    layer(
        "staircase-geometry-obstruction",
        "Weak reflected geometry does not force staircase classification",
        "finite_obstruction",
        "evidence/q286-first-three-dominant-mode-staircase-geometry-obstruction.json",
        2.0,
        "Synthetic reflected weights only; not actual prime-pair weights.")
    for target in (
            staircase_geometry[
                "full_stage_pass_targets_breakable_by_weak_geometry"]
            + staircase_geometry[
                "full_stage_fail_targets_breakable_by_weak_geometry"]):
        add_hit(
            target_stacks,
            str(target),
            "staircase-geometry-obstruction",
            2.0,
            "full-stage classification breakable by weak geometry")
    add_hit(
        mechanism_stacks,
        "weak-geometry-staircase-shortcut-closed",
        "staircase-geometry-obstruction",
        2.0,
        "support/nonnegative/total/reflection constraints force no selected "
        "full-stage classification",
        {
            "full_stage_forced_targets": (
                staircase_geometry[
                    "full_stage_classification_forced_targets"]),
            "prefix_clear_passes_forced": (
                staircase_geometry[
                    "prefix_stage_all_clear_passes_forced_by_geometry"]),
        })
    add_hit(
        theorem_stacks,
        "portfolio-residual-lower-bound",
        "staircase-geometry-obstruction",
        2.0,
        "actual prime-pair arithmetic or stronger residue constraints required")

    layer(
        "staircase-arithmetic-gap",
        "Actual prime-pair rows inside weak-geometry intervals",
        "selected_stress",
        "evidence/q286-first-three-dominant-mode-staircase-arithmetic-gap.json",
        2.0,
        "Finite arithmetic-gap diagnostic only; no pointwise theorem.")
    for row in staircase_arithmetic_gap["full_stage"]["target_rows"]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "staircase-arithmetic-gap",
            2.0,
            row["theorem_need"],
            {
                "actual_gap": row["actual_one_sided_arithmetic_gap"],
                "position": row["actual_position_in_weak_interval"],
                "uniform_correct": row["uniform_already_has_correct_sign"],
            })
    add_hit(
        mechanism_stacks,
        "actual-arithmetic-placement-inside-weak-cone",
        "staircase-arithmetic-gap",
        2.0,
        "actual margins are tiny relative to weak-geometry missing margins",
        {
            "pass_position_summary": (
                staircase_arithmetic_gap["full_stage"][
                    "pass_actual_position_summary"]),
            "fail_position_summary": (
                staircase_arithmetic_gap["full_stage"][
                    "fail_actual_position_summary"]),
            "missing_margin_summary": (
                staircase_arithmetic_gap["full_stage"][
                    "missing_margin_not_supplied_by_weak_geometry_summary"]),
        })
    add_hit(
        theorem_stacks,
        "portfolio-residual-lower-bound",
        "staircase-arithmetic-gap",
        2.0,
        "prove one-sided arithmetic placement inside broad weak interval")

    layer(
        "staircase-orbit-mass-gap",
        "Actual mass avoids weak breaker orbits on selected fixture",
        "selected_stress",
        "evidence/q286-first-three-dominant-mode-staircase-orbit-mass-gap.json",
        2.0,
        "Finite orbit-mass diagnostic only; no pointwise mass theorem.")
    for row in staircase_orbit_mass_gap["full_stage"]["target_rows"]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "staircase-orbit-mass-gap",
            2.0,
            "actual breaker-orbit mass measured",
            {
                "breaking_orbit": row["breaking_extremal_orbit"],
                "breaking_mass": (
                    row["breaking_extremal_orbit_actual_mass_fraction"]),
                "top_actual_orbit": row["top_actual_mass_orbit"],
                "top_actual_mass": row["top_actual_mass_orbit_fraction"],
                "breaking_orbit_is_top": (
                    row["breaking_orbit_is_top_actual_mass_orbit"]),
            })
    add_hit(
        mechanism_stacks,
        "actual-mass-avoids-extremal-breaker-orbits",
        "staircase-orbit-mass-gap",
        2.0,
        "breaker orbit is never the top actual mass orbit on selected rows",
        {
            "breaker_mass_summary": (
                staircase_orbit_mass_gap["full_stage"][
                    "breaking_extremal_orbit_mass_fraction_summary"]),
            "top_mass_summary": (
                staircase_orbit_mass_gap["full_stage"][
                    "top_actual_orbit_mass_fraction_summary"]),
            "breaking_orbit_top_actual_count": (
                staircase_orbit_mass_gap["full_stage"][
                    "breaking_orbit_top_actual_count"]),
        })
    add_hit(
        theorem_stacks,
        "dangerous-reflection-orbit-mass-bound",
        "staircase-orbit-mass-gap",
        2.0,
        "prove actual mass cannot concentrate on weak breaker orbits")

    layer(
        "staircase-hinge-decomposition",
        "Actual orbit mass decomposes into mixed hinge balance",
        "selected_stress",
        "evidence/q286-first-three-dominant-mode-staircase-hinge-decomposition.json",
        2.0,
        "Finite hinge diagnostic only; no hinge-balance theorem.")
    for row in staircase_hinge["full_stage"]["target_rows"]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "staircase-hinge-decomposition",
            2.0,
            "above-floor/below-floor hinge balance measured",
            {
                "supporting_mass": (
                    row["classification_supporting_mass_fraction"]),
                "opposing_mass": (
                    row["classification_opposing_mass_fraction"]),
                "supporting_hinge": (
                    row["classification_supporting_hinge_to_principal"]),
                "opposing_hinge": (
                    row["classification_opposing_hinge_to_principal"]),
                "hinge_margin": row["classification_hinge_margin"],
                "mass_driven": row["classification_mass_driven"],
                "landing_driven": row["classification_landing_driven"],
            })
    add_hit(
        mechanism_stacks,
        "mixed-mass-landing-hinge-balance",
        "staircase-hinge-decomposition",
        2.0,
        "selected rows split between mass-driven and landing-driven hinge "
        "classification",
        {
            "maximum_hinge_identity_error": (
                staircase_hinge["maximum_hinge_identity_error"]),
            "mass_driven_targets": (
                staircase_hinge["full_stage"][
                    "classification_mass_driven_targets"]),
            "landing_driven_targets": (
                staircase_hinge["full_stage"][
                    "classification_landing_driven_targets"]),
        })
    add_hit(
        theorem_stacks,
        "dominant-staircase-hinge-balance",
        "staircase-hinge-decomposition",
        2.0,
        "prove mixed actual-mass and landing-quality hinge balance")

    layer(
        "staircase-hinge-threshold",
        "Hinge balance rewritten as support-mass threshold surplus",
        "exact_obligation",
        "evidence/q286-first-three-dominant-mode-staircase-hinge-threshold.json",
        2.0,
        "Finite threshold-obligation form; support side not yet non-circular.")
    for row in staircase_hinge_threshold["full_stage"]["target_rows"]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "staircase-hinge-threshold",
            2.0,
            "support-mass surplus over landing-dependent threshold",
            {
                "supporting_mass": (
                    row["classification_supporting_mass_fraction"]),
                "threshold": row["hinge_support_mass_threshold"],
                "surplus": (
                    row["hinge_support_mass_surplus_to_threshold"]),
                "relative_surplus": (
                    row[
                        "hinge_support_mass_relative_surplus_to_threshold"]),
                "identity_error": row["hinge_threshold_identity_error"],
            })
    add_hit(
        mechanism_stacks,
        "tiny-positive-hinge-threshold-surplus",
        "staircase-hinge-threshold",
        2.0,
        "all selected full-stage rows clear the exact threshold with small "
        "positive surplus",
        {
            "surplus_summary": (
                staircase_hinge_threshold["full_stage"][
                    "hinge_support_mass_surplus_summary"]),
            "tightest_target": (
                staircase_hinge_threshold[
                    "full_stage_tightest_surplus_row"]["target"]),
            "maximum_identity_error": (
                staircase_hinge_threshold[
                    "maximum_hinge_threshold_identity_error"]),
        })
    add_hit(
        theorem_stacks,
        "dominant-staircase-hinge-threshold-surplus",
        "staircase-hinge-threshold",
        2.0,
        "prove positive surplus with non-circular support-side definition")

    layer(
        "staircase-above-floor-threshold",
        "Above-floor signed threshold gives non-post-hoc full-stage side",
        "exact_obligation",
        "evidence/q286-first-three-dominant-mode-staircase-above-floor-threshold.json",
        2.0,
        "Finite full-stage formulation; prefix sign errors remain.")
    for row in staircase_above_floor["full_stage"]["target_rows"]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "staircase-above-floor-threshold",
            2.0,
            "above-floor signed surplus measured",
            {
                "above_mass": row["above_floor_mass_fraction"],
                "threshold": row["above_floor_mass_threshold"],
                "signed_surplus": (
                    row["above_floor_signed_surplus_to_threshold"]),
                "predicts_pass": (
                    row["above_floor_threshold_predicts_pass"]),
                "identity_error": (
                    row["above_floor_threshold_identity_error"]),
            })
    add_hit(
        mechanism_stacks,
        "nonposthoc-above-floor-sign-surplus",
        "staircase-above-floor-threshold",
        2.0,
        "full stage is classified by the arithmetically defined above-floor "
        "signed surplus",
        {
            "pass_surplus_summary": (
                staircase_above_floor["full_stage"][
                    "above_floor_pass_surplus_summary"]),
            "deficit_surplus_summary": (
                staircase_above_floor["full_stage"][
                    "above_floor_deficit_surplus_summary"]),
            "maximum_stage_sign_error_count": (
                staircase_above_floor["maximum_stage_sign_error_count"]),
        })
    add_hit(
        theorem_stacks,
        "dominant-staircase-above-floor-threshold-sign",
        "staircase-above-floor-threshold",
        2.0,
        "prove full-stage above-floor surplus sign; prefix failures remain")

    layer(
        "above-floor-holdout-census",
        "Frozen above-floor staircase holdout and stress-neighborhood census",
        "holdout_census",
        "evidence/q286-first-three-dominant-mode-above-floor-holdout-census.json",
        1.5,
        "Finite margin census only; not a uniform margin theorem.")
    for row in above_floor_holdout["closest_margin_rows"]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "above-floor-holdout-census",
            1.5,
            "primary holdout closest above-floor margin",
            {
                "target_mod_286": row["target_mod_286"],
                "signed_surplus": (
                    row["above_floor_signed_surplus_to_threshold"]),
                "dominant_sum": row["dominant_sum_to_principal"],
            })
    for census in above_floor_holdout["stress_neighborhood_censuses"]:
        for row in census["closest_margin_rows"]:
            add_hit(
                target_stacks,
                str(row["target"]),
                "above-floor-holdout-census",
                1.5,
                "stress-neighborhood closest above-floor margin",
                {
                    "window_start": census["start"],
                    "target_mod_286": row["target_mod_286"],
                    "signed_surplus": (
                        row["above_floor_signed_surplus_to_threshold"]),
                })
    add_hit(
        mechanism_stacks,
        "sparse-near-boundary-above-floor-margins",
        "above-floor-holdout-census",
        1.5,
        "primary holdout is comfortably positive; stress neighborhoods recover "
        "known sparse tiny rows",
        {
            "primary_min_abs_surplus": (
                above_floor_holdout[
                    "absolute_above_floor_signed_surplus_summary"][
                    "minimum"]),
            "primary_deficit_count": (
                above_floor_holdout["dominant_floor_deficit_count"]),
            "stress_windows": tuple(
                {
                    "start": census["start"],
                    "deficit_count": census["dominant_floor_deficit_count"],
                    "min_abs_surplus": census[
                        "absolute_above_floor_signed_surplus_summary"][
                        "minimum"],
                }
                for census in above_floor_holdout[
                    "stress_neighborhood_censuses"]),
        })
    add_hit(
        theorem_stacks,
        "near-boundary-selector-theorem",
        "above-floor-holdout-census",
        1.5,
        "prove arithmetic selector/placement theorem for sparse tiny margins")

    layer(
        "near-boundary-selector-audit",
        "Simple selector audit for sparse above-floor margins",
        "finite_falsifier",
        "evidence/q286-first-three-dominant-mode-near-boundary-selector-audit.json",
        2.0,
        "Finite falsifier for simple selector families only.")
    for row in selector_audit["closest_overall_rows"][:12]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "near-boundary-selector-audit",
            2.0,
            "selector-audit closest margin row",
            {
                "window_start": row["window_start"],
                "target_mod_286": row["target_mod_286"],
                "target_mod_10010": row["target_mod_10010"],
                "signed_surplus": (
                    row["above_floor_signed_surplus_to_threshold"]),
            })
    for threshold, threshold_row in selector_audit[
            "threshold_rows"].items():
        residue_audit = threshold_row[
            "residue_mod_286_selector_audit"]
        for row in residue_audit["false_positive_examples"][:4]:
            add_hit(
                target_stacks,
                str(row["target"]),
                "near-boundary-selector-audit",
                1.0,
                "q286-residue selector false positive",
                {
                    "threshold": threshold,
                    "target_mod_286": row["target_mod_286"],
                    "abs_surplus": (
                        row["absolute_above_floor_signed_surplus"]),
                })
    add_hit(
        mechanism_stacks,
        "simple-near-boundary-selectors-refuted",
        "near-boundary-selector-audit",
        2.0,
        "q286 residue-only and scalar interval selectors have false positives",
        {
            "evaluated_target_count": (
                selector_audit["evaluated_target_count"]),
            "residue_only_refuted_thresholds": (
                selector_audit["residue_only_refuted_thresholds"]),
            "scalar_interval_refuted_thresholds": (
                selector_audit["scalar_interval_refuted_thresholds"]),
        })
    add_hit(
        theorem_stacks,
        "near-boundary-selector-theorem",
        "near-boundary-selector-audit",
        2.0,
        "selector must use finer prime-pair distribution than q286 residue or "
        "one scalar interval")

    layer(
        "outside-rank1-separator",
        "Frozen Octave rank-1 outside direction separates checked clears",
        "finite_svd_diagnostic",
        "evidence/q286-first-three-dominant-mode-outside-plane-remainder-octave-rank1-audit.json",
        2.5,
        "Finite SVD diagnostic only; rank-1 direction is not yet an arithmetic theorem.")
    for row in outside_rank1["rows_by_full_outside_delta"][:20]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "outside-rank1-separator",
            2.5,
            "small exact outside delta with positive rank-1 reconstruction",
            {
                "full_outside_delta": row["full_outside_delta_to_stress"],
                "rank1_reconstructed_delta": (
                    row["rank1_reconstructed_outside_delta"]),
                "residual_after_rank1": (
                    row["residual_after_rank1_row_sum"]),
            })
    add_hit(
        mechanism_stacks,
        "positive-rank1-outside-direction",
        "outside-rank1-separator",
        2.5,
        "rank-1 reconstruction is positive on every checked clear row",
        {
            "clear_count": outside_rank1["clear_count"],
            "rank1_energy_fraction": outside_rank1[
                "rank1_energy_fraction"],
            "minimum_rank1_target": (
                outside_rank1[
                    "rank1_minimum_reconstructed_outside_delta"][
                    "target"]),
        })
    add_hit(
        theorem_stacks,
        "rank1-outside-direction-arithmetic-meaning",
        "outside-rank1-separator",
        2.5,
        "identify the frozen rank-1 vector as a non-post-hoc arithmetic object")

    layer(
        "rank1-residual-drag-ledger",
        "Near-sharp residual drag after rank-1 reconstruction",
        "finite_ratio_diagnostic",
        "evidence/q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-ledger.json",
        2.5,
        "Finite residual-drag ratio only; no residual-bound theorem.")
    for row in residual_drag["rows_by_residual_drag_ratio"][:12]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "rank1-residual-drag-ledger",
            2.5,
            "high residual-drag ratio on original checked denominator",
            {
                "residual_drag_to_rank1_ratio": (
                    row["residual_drag_to_rank1_ratio"]),
                "residual_drag": row["residual_drag"],
                "rank1_reconstructed_delta": (
                    row["rank1_reconstructed_outside_delta"]),
            })
    add_hit(
        mechanism_stacks,
        "near-sharp-rank1-residual-drag-cap",
        "rank1-residual-drag-ledger",
        2.5,
        "0.75 residual-drag cap survives while 0.7 and half caps fail",
        {
            "worst_target": residual_drag["worst_residual_drag_row"][
                "target"],
            "maximum_ratio": residual_drag[
                "maximum_residual_drag_to_rank1_ratio"],
            "negative_residual_row_count": residual_drag[
                "negative_residual_row_count"],
        })
    add_hit(
        theorem_stacks,
        "rank1-residual-drag-bound",
        "rank1-residual-drag-ledger",
        2.5,
        "prove near-sharp residual-drag inequality or replace rank-1 proxy")

    layer(
        "rank1-residual-drag-full-window",
        "Rank-1 residual-drag cap survives the full six-window denominator",
        "finite_holdout_diagnostic",
        "evidence/q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-full-window-audit.json",
        3.0,
        "Full-window finite audit only; not a uniform denominator theorem.")
    for row in residual_drag_full_window["rows_by_residual_drag_ratio"][:20]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "rank1-residual-drag-full-window",
            3.0,
            "full-window high residual-drag row",
            {
                "residual_drag_to_rank1_ratio": (
                    row["residual_drag_to_rank1_ratio"]),
                "full_outside_delta": row["full_outside_delta_to_stress"],
                "window_start": row["window_start"],
            })
    add_hit(
        mechanism_stacks,
        "rank1-cap-survives-full-window",
        "rank1-residual-drag-full-window",
        3.0,
        "frozen rank-1 positivity plus 0.75 residual-drag cap survives all full-window clears",
        {
            "full_window_target_count": residual_drag_full_window[
                "full_window_target_count"],
            "clear_count": residual_drag_full_window["clear_count"],
            "deficit_targets": residual_drag_full_window["deficit_targets"],
            "maximum_ratio": residual_drag_full_window[
                "maximum_residual_drag_to_rank1_ratio"],
        })
    add_hit(
        theorem_stacks,
        "rank1-residual-drag-bound",
        "rank1-residual-drag-full-window",
        3.0,
        "full-window survival makes residual-drag theorem target more stable")

    layer(
        "residual-drag-channel-certificate-falsifier",
        "Small fixed outside-channel certificate is refuted",
        "finite_falsifier",
        "evidence/q286-first-three-dominant-mode-residual-drag-channel-certificate-falsifier.json",
        3.0,
        "Finite falsifier for one sparse proof shortcut only.")
    for row in residual_drag_channel_certificate["high_drag_rows_by_ratio"]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "residual-drag-channel-certificate-falsifier",
            3.0,
            "high-drag row resists one fixed five-channel certificate",
            {
                "residual_drag_to_rank1_ratio": (
                    row["residual_drag_to_rank1_ratio"]),
                "top_negative_residual_channels": (
                    row["top_negative_residual_channels"][:3]),
            })
    add_hit(
        mechanism_stacks,
        "small-fixed-channel-certificate-refuted",
        "residual-drag-channel-certificate-falsifier",
        3.0,
        "best fixed five-label subset covers only 0.3570706202 on its worst high-drag row",
        {
            "high_drag_row_count": residual_drag_channel_certificate[
                "high_drag_row_count"],
            "best_five_label_subset": (
                residual_drag_channel_certificate[
                    "best_fixed_subsets_on_high_drag_rows"][-1][
                    "labels"]),
            "best_five_minimum_share": (
                residual_drag_channel_certificate[
                    "best_fixed_subsets_on_high_drag_rows"][-1][
                    "minimum_row_share"]),
        })
    add_hit(
        theorem_stacks,
        "rank1-residual-drag-bound",
        "residual-drag-channel-certificate-falsifier",
        3.0,
        "tiny static bad-channel proof route is closed; use row-dependent balance or larger cone")

    layer(
        "lift-project-dictionary-audit",
        "Simple q286 lift-project dictionaries are demoted with one partial low-frequency signal",
        "finite_partial_falsifier",
        "evidence/q286-lift-project-dictionary-audit.json",
        2.5,
        "Finite dictionary audit only; no lifted dictionary theorem.")
    best_lift = lift_project_dictionary["best_dictionary_by_rank1_cosine"]
    for row in lift_project_dictionary["dictionary_rows"][0][
            "rows_by_residual_drag_ratio"][:10]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "lift-project-dictionary-audit",
            2.5,
            "high residual-drag row under best simple low-frequency lift",
            {
                "dictionary_ratio": (
                    row["residual_drag_to_dictionary_ratio"]),
                "reference_rank1_ratio": (
                    row["reference_rank1_residual_drag_to_rank1_ratio"]),
                "dictionary_delta_to_full_ratio": (
                    row["dictionary_delta_to_full_delta_ratio"]),
            })
    add_hit(
        mechanism_stacks,
        "simple-label-only-lift-demoted",
        "lift-project-dictionary-audit",
        2.5,
        "no simple label-only dictionary passes the local hole-tightening gate",
        {
            "passing_dictionary_count": lift_project_dictionary[
                "passing_dictionary_count"],
            "best_dictionary": best_lift["id"],
            "best_rank1_cosine": best_lift["rank1_direction_cosine"],
            "best_high_drag_overlap": best_lift[
                "high_drag_overlap_count_at_reference_k"],
            "claude_order_weight_cosine": next(
                row["rank1_direction_cosine"]
                for row in lift_project_dictionary["dictionary_rows"]
                if row["id"] == "claude_order_weight_lift"),
            "claude_order_weight_high_drag_overlap": next(
                row["high_drag_overlap_count_at_reference_k"]
                for row in lift_project_dictionary["dictionary_rows"]
                if row["id"] == "claude_order_weight_lift"),
        })
    add_hit(
        mechanism_stacks,
        "low-frequency-label-lattice-partial-signal",
        "lift-project-dictionary-audit",
        2.0,
        "full_low_frequency_lift keeps positivity and the 0.75 cap but misses the explanation gate")
    add_hit(
        theorem_stacks,
        "rank1-outside-direction-arithmetic-meaning",
        "lift-project-dictionary-audit",
        2.5,
        "simple label-only lifted dictionaries do not fully explain rank-1")

    layer(
        "low-frequency-lift-holdout",
        "Frozen low-frequency q286 lift survives fresh-window holdout",
        "finite_holdout_diagnostic",
        "evidence/q286-low-frequency-lift-holdout.json",
        3.0,
        "Finite heldout diagnostic only; no lifted dictionary theorem.")
    for row in low_frequency_lift_holdout[
            "rows_by_dictionary_residual_drag_ratio"][:12]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "low-frequency-lift-holdout",
            3.0,
            "heldout high residual-drag row under frozen low-frequency lift",
            {
                "dictionary_ratio": (
                    row["dictionary_residual_drag_to_dictionary_ratio"]),
                "rank1_ratio": (
                    row["rank1_residual_drag_to_rank1_ratio"]),
                "dictionary_delta_to_full_ratio": (
                    row["dictionary_delta_to_full_delta_ratio"]),
            })
    add_hit(
        mechanism_stacks,
        "low-frequency-label-lattice-heldout-survives",
        "low-frequency-lift-holdout",
        3.0,
        "frozen low-frequency lift has zero positivity/cap failures and 8/10 high-drag overlap on fresh rows",
        {
            "heldout_clear_count": low_frequency_lift_holdout[
                "heldout_clear_count"],
            "high_drag_overlap": low_frequency_lift_holdout[
                "high_drag_overlap_count_at_reference_k"],
            "reference_high_drag_count": low_frequency_lift_holdout[
                "reference_rank1_high_drag_count"],
            "maximum_dictionary_ratio": (
                low_frequency_lift_holdout[
                    "maximum_dictionary_residual_drag_ratio"]["value"]),
        })
    add_hit(
        theorem_stacks,
        "rank1-outside-direction-arithmetic-meaning",
        "low-frequency-lift-holdout",
        3.0,
        "low-frequency label-lattice signal survives heldout but still needs arithmetic theorem")

    layer(
        "target-residue-lift-holdout",
        "Target-residue tensor fails to improve static low-frequency q286 lift",
        "finite_falsifier",
        "evidence/q286-target-residue-lift-holdout.json",
        2.5,
        "Finite falsifier for one residue-augmented lift only.")
    add_hit(
        mechanism_stacks,
        "coarse-target-residue-lift-demoted",
        "target-residue-lift-holdout",
        2.5,
        "N mod 11/13 tensor features do not improve static low-frequency lift on heldout",
        {
            "static_heldout_cosine": target_residue_lift_holdout[
                "static_low_frequency_heldout_summary"][
                "matrix_cosine_to_rank1_reference"],
            "tensor_heldout_cosine": target_residue_lift_holdout[
                "target_residue_heldout_summary"][
                "matrix_cosine_to_rank1_reference"],
            "static_high_drag_overlap": target_residue_lift_holdout[
                "static_low_frequency_heldout_summary"][
                "high_drag_overlap_count_at_reference_k"],
            "tensor_high_drag_overlap": target_residue_lift_holdout[
                "target_residue_heldout_summary"][
                "high_drag_overlap_count_at_reference_k"],
        })
    add_hit(
        theorem_stacks,
        "rank1-outside-direction-arithmetic-meaning",
        "target-residue-lift-holdout",
        2.5,
        "coarse target residues alone do not explain the rank-1 shadow")

    layer(
        "low-frequency-lift-horizon-holdout",
        "Frozen low-frequency q286 lift survives farther stress-marker horizon",
        "finite_horizon_holdout_diagnostic",
        "evidence/q286-low-frequency-lift-horizon-holdout.json",
        3.0,
        "Finite horizon diagnostic only; no low-frequency theorem.")
    for row in low_frequency_lift_horizon[
            "rows_by_low_frequency_residual_drag_ratio"][:12]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "low-frequency-lift-horizon-holdout",
            3.0,
            "horizon high residual-drag row under frozen low-frequency lift",
            {
                "low_frequency_ratio": (
                    row[
                        "low_frequency_residual_drag_to_low_frequency_ratio"]),
                "rank1_ratio": (
                    row["rank1_residual_drag_to_rank1_ratio"]),
                "full_outside_delta": (
                    row["full_outside_delta_to_stress"]),
                "window_start": row["window_start"],
            })
    add_hit(
        mechanism_stacks,
        "low-frequency-label-lattice-horizon-survives",
        "low-frequency-lift-horizon-holdout",
        3.0,
        "frozen low-frequency lift has zero deficits, zero positivity/cap failures, and 2/3 high-drag overlap on farther stress-marker windows",
        {
            "horizon_clear_count": low_frequency_lift_horizon[
                "horizon_clear_count"],
            "high_drag_overlap": low_frequency_lift_horizon[
                "high_drag_overlap_count_at_reference_k"],
            "reference_high_drag_count": low_frequency_lift_horizon[
                "reference_rank1_high_drag_count"],
            "matrix_cosine": low_frequency_lift_horizon[
                "matrix_cosine_low_frequency_to_rank1_reference"],
            "maximum_low_frequency_ratio": (
                low_frequency_lift_horizon[
                    "maximum_low_frequency_residual_drag_ratio"]["value"]),
            "tight_target": (
                low_frequency_lift_horizon[
                    "maximum_low_frequency_residual_drag_ratio"]["target"]),
        })
    add_hit(
        theorem_stacks,
        "rank1-outside-direction-arithmetic-meaning",
        "low-frequency-lift-horizon-holdout",
        3.0,
        "low-frequency label-lattice signal survives farther horizon but still needs arithmetic theorem")

    layer(
        "frobenius-lattice-claim-audit",
        "Frobenius/GCD/parity rank-1 explanation rejected as stated",
        "finite_claim_falsifier",
        "evidence/q286-frobenius-lattice-claim-audit.json",
        2.5,
        "Finite claim audit only; richer character-lattice lifts remain open.")
    add_hit(
        mechanism_stacks,
        "frobenius-gcd-parity-rank1-shortcut-refuted",
        "frobenius-lattice-claim-audit",
        2.5,
        "Frobenius formula, gcd(17,120) projection, parity split, and unit-rank bridge do not force the observed rank-1 vector",
        {
            "claimed_formula_value": (
                frobenius_lattice_claim["frobenius_claim_check"][
                    "claim_value_q_times_half_minus_inverse_17"]),
            "g_2_17": frobenius_lattice_claim["frobenius_claim_check"][
                "frobenius_number_for_denominations_2_and_17"],
            "g_17_286": frobenius_lattice_claim["frobenius_claim_check"][
                "frobenius_number_for_denominations_17_and_286"],
            "gcd_17_120": frobenius_lattice_claim[
                "gcd_rank_claim_check"]["gcd_17_120"],
            "all_25_even_parity_count": frobenius_lattice_claim[
                "parity_axis_check"]["all_25_even_parity_count"],
            "unit_rank_Q_zeta_286": frobenius_lattice_claim[
                "ray_class_unit_claim_check"]["unit_rank_for_Q_zeta_286"],
        })
    add_hit(
        theorem_stacks,
        "rank1-outside-direction-arithmetic-meaning",
        "frobenius-lattice-claim-audit",
        2.5,
        "closed one arithmetic-sounding shortcut; actual character-sum mechanism still open")

    layer(
        "low-frequency-lp-cone-audit",
        "Bounded low-frequency LP cone survives training and two heldouts",
        "finite_optimization_certificate_candidate",
        "evidence/q286-low-frequency-lp-cone-audit.json",
        3.0,
        "Finite LP cone diagnostic only; no LP theorem or Goldbach proof.")
    for row in low_frequency_lp_cone[
            "selected_horizon_rows_by_residual_drag_ratio"][:12]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "low-frequency-lp-cone-audit",
            3.0,
            "horizon high residual-drag row under frozen LP cone vector",
            {
                "lp_ratio": row["lp_residual_drag_ratio"],
                "rank1_ratio": row["rank1_residual_drag_to_rank1_ratio"],
                "low_frequency_ratio": (
                    row[
                        "low_frequency_residual_drag_to_low_frequency_ratio"]),
                "window_start": row["window_start"],
            })
    add_hit(
        mechanism_stacks,
        "low-frequency-lp-cap-certificate-survives",
        "low-frequency-lp-cone-audit",
        3.0,
        "bounded LP in the same low-frequency C10 x C12 Fourier band has zero positivity/cap failures on training plus two heldouts",
        {
            "selected_l1_multiplier": low_frequency_lp_cone[
                "selected_lp_record"]["l1_multiplier"],
            "training_slack": low_frequency_lp_cone[
                "selected_lp_record"]["objective_minimum_training_slack"],
            "rank1_cosine": low_frequency_lp_cone[
                "selected_lp_rank1_direction_cosine"],
            "training_max_ratio": low_frequency_lp_cone[
                "selected_lp_record"]["training_summary"][
                "maximum_residual_drag_ratio"]["value"],
            "heldout_max_ratio": low_frequency_lp_cone[
                "heldout_summary"]["maximum_residual_drag_ratio"]["value"],
            "horizon_max_ratio": low_frequency_lp_cone[
                "horizon_summary"]["maximum_residual_drag_ratio"]["value"],
        })
    add_hit(
        theorem_stacks,
        "rank1-residual-drag-bound",
        "low-frequency-lp-cone-audit",
        3.0,
        "LP finds finite cap-certificate vector; a non-optimized arithmetic cone theorem is still needed")
    add_hit(
        theorem_stacks,
        "rank1-outside-direction-arithmetic-meaning",
        "low-frequency-lp-cone-audit",
        1.5,
        "LP vector is useful for cap but has only about 0.602 cosine to rank-1")

    layer(
        "low-frequency-lp-cone-stress-holdout",
        "Frozen low-frequency LP cone survives far stress holdout",
        "finite_holdout_certificate_candidate",
        "evidence/q286-low-frequency-lp-cone-stress-holdout.json",
        3.5,
        "Finite far stress holdout only; no LP theorem or Goldbach proof.")
    for row in low_frequency_lp_cone_stress[
            "selected_lp_rows_by_residual_drag_ratio"][:12]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "low-frequency-lp-cone-stress-holdout",
            3.5,
            "far stress row under frozen LP cone vector",
            {
                "lp_ratio": row["lp_residual_drag_ratio"],
                "lp_delta": row["lp_reconstructed_outside_delta"],
                "full_delta": row["full_outside_delta_to_stress"],
                "window_start": row["window_start"],
            })
    add_hit(
        mechanism_stacks,
        "low-frequency-lp-cap-certificate-survives",
        "low-frequency-lp-cone-stress-holdout",
        3.5,
        "same frozen LP vector has zero positivity/cap failures and zero residual drag on six far stress windows",
        {
            "far_stress_clear_count": low_frequency_lp_cone_stress[
                "far_stress_clear_count"],
            "lp_max_ratio": low_frequency_lp_cone_stress[
                "lp_summary"]["maximum_residual_drag_ratio"]["value"],
            "minimum_lp_delta": low_frequency_lp_cone_stress[
                "lp_summary"]["minimum_reconstructed_delta"]["value"],
            "minimum_lp_delta_target": low_frequency_lp_cone_stress[
                "lp_summary"]["minimum_reconstructed_delta"]["target"],
            "maximum_rank1_ratio": low_frequency_lp_cone_stress[
                "maximum_rank1_residual_drag_ratio"]["value"],
            "maximum_low_frequency_ratio": low_frequency_lp_cone_stress[
                "maximum_low_frequency_residual_drag_ratio"]["value"],
        })
    add_hit(
        theorem_stacks,
        "rank1-residual-drag-bound",
        "low-frequency-lp-cone-stress-holdout",
        3.5,
        "LP cap-certificate candidate survives far stress replay but still needs an arithmetic cone or endpoint theorem")
    add_hit(
        theorem_stacks,
        "interpolation-or-cone-endpoint-theorem",
        "low-frequency-lp-cone-stress-holdout",
        2.0,
        "Riesz-Thorin/logistic/Laplace analogies remain theorem-shaping until operator and endpoint arithmetic bounds exist")

    layer(
        "lp-cone-local-singular-audit",
        "Frozen LP cone has nonnegative local singular orientation",
        "finite_local_cone_diagnostic",
        "evidence/q286-lp-cone-local-singular-audit.json",
        3.0,
        "Finite local/admissibility audit only; no prime-pair theorem.")
    for target in lp_cone_local_singular["far_empirical_summary"][
            "zero_local_action_but_positive_empirical_targets"]:
        add_hit(
            target_stacks,
            str(target),
            "lp-cone-local-singular-audit",
            2.0,
            "positive empirical LP delta despite zero local LP action")
    add_hit(
        mechanism_stacks,
        "local-singular-cone-orientation-floor",
        "lp-cone-local-singular-audit",
        3.0,
        "local admissible residue measures give nonnegative LP action on all target residues mod 143",
        {
            "local_lp_negative_count": lp_cone_local_singular[
                "local_lp_negative_count"],
            "local_lp_zero_residues": lp_cone_local_singular[
                "local_lp_zero_residues"],
            "minimum_local_lp_action": lp_cone_local_singular[
                "local_lp_delta_action_summary"]["minimum"],
            "maximum_local_lp_action": lp_cone_local_singular[
                "local_lp_delta_action_summary"]["maximum"],
            "local_rank1_negative_count": lp_cone_local_singular[
                "local_rank1_negative_count"],
        })
    add_hit(
        theorem_stacks,
        "fixed-modulus-binary-prime-discrepancy",
        "lp-cone-local-singular-audit",
        3.0,
        "local cone orientation survives but empirical/local correlation is flat; quantitative binary-prime discrepancy remains")
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "lp-cone-local-singular-audit",
        3.0,
        "BMOR q286 AP-count constants are useful input but do not directly prove the signed 17-channel functional")

    layer(
        "zero-local-target-channel-decomposition",
        "Zero-local target rows decompose into signed 17-channel correlation",
        "finite_channel_decomposition",
        "evidence/q286-zero-local-target-channel-decomposition.json",
        3.0,
        "Finite 12-target decomposition only; no correlation theorem.")
    for row in zero_local_decomposition["target_rows"]:
        add_hit(
            target_stacks,
            str(row["target"]),
            "zero-local-target-channel-decomposition",
            2.5,
            "zero local action but positive after-local full and LP deltas",
            {
                "target_mod_143": row["target_mod_143"],
                "after_local_full": row["after_local_full_outside_delta"],
                "after_local_lp": row["after_local_lp_delta"],
                "positive_channel_count": row[
                    "after_local_vector_summary"]["positive_count"],
                "negative_channel_count": row[
                    "after_local_vector_summary"]["negative_count"],
            })
    add_hit(
        mechanism_stacks,
        "zero-local-target-correlation-decomposition",
        "zero-local-target-channel-decomposition",
        3.0,
        "12 target integers with zero local action remain positive after subtracting the local vector across all 17 outside channels",
        {
            "zero_local_target_count": zero_local_decomposition[
                "zero_local_target_count"],
            "zero_local_residues": zero_local_decomposition[
                "zero_local_target_residues_mod_143"],
            "after_local_full_minimum": zero_local_decomposition[
                "after_local_full_delta_summary"]["minimum"],
            "after_local_lp_minimum": zero_local_decomposition[
                "after_local_lp_delta_summary"]["minimum"],
            "positive_entry_count": zero_local_decomposition[
                "after_local_positive_entry_count"],
            "negative_entry_count": zero_local_decomposition[
                "after_local_negative_entry_count"],
        })
    add_hit(
        theorem_stacks,
        "fixed-modulus-binary-prime-discrepancy",
        "zero-local-target-channel-decomposition",
        3.0,
        "zero local contribution rows are carried by signed empirical 17-channel correlation")

    layer(
        "zero-local-channel-margin-audit",
        "Zero-local channel margins admit one-channel positive subsets",
        "finite_subset_audit",
        "evidence/q286-zero-local-channel-margin-audit.json",
        3.0,
        "Finite 12-target subset audit only; no distributed cone theorem.")
    all_scope = zero_local_margin_audit["scopes"]["all_12_targets"]
    add_hit(
        mechanism_stacks,
        "zero-local-target-correlation-decomposition",
        "zero-local-channel-margin-audit",
        2.0,
        "after-local LP margin is correlation-sourced but not forced to use a large fixed subset on these 12 targets",
        {
            "smallest_fixed_subset_size": zero_local_margin_audit[
                "smallest_all_target_subset_size"],
            "smallest_fixed_subset_count": zero_local_margin_audit[
                "smallest_all_target_subset_count"],
            "any_single_channel_removal_fails": all_scope[
                "any_single_channel_removal_fails_target"],
            "top_singleton": all_scope["smallest_fixed_subset"][
                "best_subsets_by_minimum_margin"][0]["labels"],
            "top_singleton_min_margin": all_scope["smallest_fixed_subset"][
                "best_subsets_by_minimum_margin"][0][
                    "minimum_target_margin"],
        })
    add_hit(
        theorem_stacks,
        "distributed-cone-correlation-theorem",
        "zero-local-channel-margin-audit",
        3.0,
        "smallest-subset test rejects the claim that these 12 LP-positive rows require a distributed fixed channel subset")

    layer(
        "far-singleton-channel-stability",
        "Same-window non-seed singleton channel stability",
        "finite_channel_holdout",
        "evidence/q286-far-singleton-channel-stability-audit.json",
        3.0,
        "Finite same-stress holdout only; no stress-independent theorem.")
    add_hit(
        mechanism_stacks,
        "same-stress-singleton-channel-candidates",
        "far-singleton-channel-stability",
        3.0,
        "seed/non-seed split leaves (5,5) and (3,1) as all-far same-stress singleton candidates",
        {
            "target_count": far_singleton_channel_stability["target_count"],
            "all_far_singleton_passing_count":
                far_singleton_channel_stability[
                    "all_far_singleton_passing_count"],
            "watchlist_passing":
                far_singleton_channel_stability[
                    "watchlist_all_far_passing_singletons"],
            "watchlist_failing":
                far_singleton_channel_stability[
                    "watchlist_all_far_failing_singletons"],
        })
    add_hit(
        theorem_stacks,
        "alternate-stress-channel-reference-gate",
        "far-singleton-channel-stability",
        2.0,
        "same stress reference can make channels look positive if the reference row is unusually low")

    layer(
        "fresh-window-channel-watchlist",
        "Fresh predeclared window watchlist replay",
        "finite_selection_bias_gate",
        "evidence/q286-fresh-window-channel-watchlist-audit.json",
        3.0,
        "Finite fresh-window same-stress audit only; no stress-independent theorem.")
    add_hit(
        mechanism_stacks,
        "same-stress-singleton-channel-candidates",
        "fresh-window-channel-watchlist",
        3.0,
        "fresh predeclared windows preserve (5,5), (3,1), and (3,7), while (3,11) fails once",
        {
            "target_count": fresh_window_channel_watchlist["target_count"],
            "predeclared_windows":
                fresh_window_channel_watchlist[
                    "predeclared_window_specs"],
            "watchlist_passes":
                fresh_window_channel_watchlist["watchlist_passes"],
            "surviving_watchlist_singletons":
                fresh_window_channel_watchlist[
                    "surviving_watchlist_singletons"],
            "failing_watchlist_singletons":
                fresh_window_channel_watchlist[
                    "failing_watchlist_singletons"],
        })
    add_hit(
        theorem_stacks,
        "alternate-stress-channel-reference-gate",
        "fresh-window-channel-watchlist",
        3.0,
        "fresh-window selection-bias gate passes under same stress but alternate stress references remain required")

    layer(
        "alternate-reference-channel-audit",
        "Alternate reference channel stability audit",
        "finite_reference_sensitivity_gate",
        "evidence/q286-alternate-reference-channel-audit.json",
        3.0,
        "Finite selected-reference audit only; no reference-independent theorem.")
    add_hit(
        mechanism_stacks,
        "same-stress-singleton-channel-candidates",
        "alternate-reference-channel-audit",
        2.0,
        "alternate references falsify the two-channel reference-independent reading",
        {
            "deficit_reference_all_live_candidates_pass":
                alternate_reference_channel[
                    "deficit_reference_all_live_candidates_pass"],
            "deficit_reference_failures":
                alternate_reference_channel["deficit_reference_failures"],
            "clear_control_reference_failures":
                alternate_reference_channel[
                    "clear_control_reference_failures"],
        })
    add_hit(
        theorem_stacks,
        "alternate-stress-channel-reference-gate",
        "alternate-reference-channel-audit",
        3.0,
        "(3,1) survives selected deficit references; (5,5) is reference-sensitive")

    layer(
        "centered-channel-scalar-order-audit",
        "Centered (3,1) scalar order separates selected deficit references",
        "finite_scalar_separator_gate",
        "evidence/q286-centered-channel-scalar-order-audit.json",
        3.0,
        "Finite selected-reference scalar-order audit only; no stress-classifier theorem.")
    add_hit(
        mechanism_stacks,
        "centered-3-1-selected-deficit-separator",
        "centered-channel-scalar-order-audit",
        3.0,
        "locally centered (3,1) puts selected deficit references below every fresh target",
        {
            "channel_3_1_all_deficit_below_fresh_min":
                centered_channel_scalar_order[
                    "channel_3_1_all_deficit_references_below_fresh_min"],
            "channel_5_5_all_deficit_below_fresh_min":
                centered_channel_scalar_order[
                    "channel_5_5_all_deficit_references_below_fresh_min"],
            "channel_3_1_gap":
                next(
                    result for result in centered_channel_scalar_order[
                        "channel_results"]
                    if result["label_key"] == "3,1")[
                        "minimum_fresh_minus_max_deficit_weighted_gap"],
            "channel_5_5_gap":
                next(
                    result for result in centered_channel_scalar_order[
                        "channel_results"]
                    if result["label_key"] == "5,5")[
                        "minimum_fresh_minus_max_deficit_weighted_gap"],
        })
    add_hit(
        target_stacks,
        "13822",
        "centered-channel-scalar-order-audit",
        2.0,
        "second-lowest locally centered (3,1) row in combined scalar order")
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "centered-channel-scalar-order-audit",
        3.0,
        "next gate is a non-post-hoc stress/deficit class, not selected references")

    layer(
        "centered-3-1-reference-lemma-audit",
        "Centered (3,1) selected-reference lemma is scoped",
        "finite_selected_reference_lemma",
        "evidence/q286-centered-3-1-reference-lemma-audit.json",
        3.0,
        "Finite selected-reference lemma only; broad promotions are falsified.")
    add_hit(
        mechanism_stacks,
        "centered-3-1-selected-deficit-separator",
        "centered-3-1-reference-lemma-audit",
        3.0,
        "all selected deficit references have 606/606 positive fresh-window (3,1) margins",
        {
            "selected_deficit_references_all_pass":
                centered_3_1_reference_lemma[
                    "selected_deficit_references_all_pass"],
            "clear_control_references_all_fail_singleton":
                centered_3_1_reference_lemma[
                    "clear_control_references_all_fail_singleton"],
            "focus_reference_13822":
                centered_3_1_reference_lemma["focus_reference_13822"],
            "broad_full_nonpositive_class_falsifier":
                centered_3_1_reference_lemma[
                    "broad_full_nonpositive_class_falsifier"],
        })
    add_hit(
        target_stacks,
        "13822",
        "centered-3-1-reference-lemma-audit",
        3.0,
        "strong selected stress witness: low centered (3,1), positive stable core, large negative volatile rim",
        centered_3_1_reference_lemma["focus_reference_13822"])
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "centered-3-1-reference-lemma-audit",
        3.0,
        "supports only selected stress-reference separation; arbitrary-reference and full_nonpositive promotions remain false")

    layer(
        "centered-3-1-residue-collision-audit",
        "Centered (3,1) same-residue collisions are nonlocal",
        "finite_local_residue_artifact_falsifier",
        "evidence/q286-centered-3-1-residue-collision-audit.json",
        3.0,
        "Finite same-residue selected-fixture audit only; no signed correlation theorem.")
    add_hit(
        mechanism_stacks,
        "centered-3-1-selected-deficit-separator",
        "centered-3-1-residue-collision-audit",
        3.0,
        "same-residue selected deficit/clear pairs split after identical local subtraction",
        {
            "same_residue_collision_all_pairs_pass":
                centered_3_1_residue_collision[
                    "same_residue_collision_all_pairs_pass"],
            "collision_pair_count":
                centered_3_1_residue_collision["collision_pair_count"],
            "deficits_with_same_residue_clear":
                centered_3_1_residue_collision[
                    "deficits_with_same_residue_clear"],
            "deficits_without_same_residue_clear":
                centered_3_1_residue_collision[
                    "deficits_without_same_residue_clear"],
            "weighted_gap_summary":
                centered_3_1_residue_collision[
                    "same_residue_weighted_gap_summary"],
        })
    add_hit(
        target_stacks,
        "13822",
        "centered-3-1-residue-collision-audit",
        2.5,
        "same-residue collision: 13822 stays below clear control 40420 after zero local gap",
        next(
            pair
            for row in centered_3_1_residue_collision["residue_rows"]
            for pair in row["pair_rows"]
            if pair["deficit_target"] == 13822))
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "centered-3-1-residue-collision-audit",
        3.0,
        "local-residue-only explanation is falsified on checked selected collisions; signed/correlation explanation still open")

    layer(
        "centered-3-1-same-residue-fresh-population-audit",
        "Centered (3,1) selected deficits stay below same-residue fresh targets",
        "finite_fresh_population_local_residue_falsifier",
        "evidence/q286-centered-3-1-same-residue-fresh-population-audit.json",
        3.0,
        "Finite same-residue fresh-window audit only; no signed correlation theorem.")
    add_hit(
        mechanism_stacks,
        "centered-3-1-selected-deficit-separator",
        "centered-3-1-same-residue-fresh-population-audit",
        3.0,
        "all selected deficits are below all same-residue fresh predeclared targets",
        {
            "all_selected_deficits_pass_same_residue_fresh_population":
                centered_3_1_same_residue_fresh[
                    "all_selected_deficits_pass_same_residue_fresh_population"],
            "fresh_population_failures":
                centered_3_1_same_residue_fresh[
                    "fresh_population_failures"],
            "target_role_counts":
                centered_3_1_same_residue_fresh["target_role_counts"],
        })
    for deficit_row in centered_3_1_same_residue_fresh["deficit_rows"]:
        target = str(deficit_row["deficit"]["target"])
        add_hit(
            target_stacks,
            target,
            "centered-3-1-same-residue-fresh-population-audit",
            2.5,
            "selected deficit below all same-residue fresh predeclared targets",
            deficit_row["scopes"][0]["weighted_gap_summary"])
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "centered-3-1-same-residue-fresh-population-audit",
        3.0,
        "fresh same-residue population rejects local-residue-only and selected-clear-only explanations")

    layer(
        "centered-3-1-signed-gap-obligation",
        "Centered (3,1) signed-gap obligation is explicit",
        "theorem_obligation",
        "evidence/q286-centered-3-1-signed-gap-obligation.json",
        3.0,
        "Finite theorem-obligation extraction only; no signed correlation theorem.")
    add_hit(
        mechanism_stacks,
        "centered-3-1-selected-deficit-separator",
        "centered-3-1-signed-gap-obligation",
        3.0,
        "same-residue local cancellation reduces the checked separator to an empirical/correlation gap",
        {
            "same_residue_fresh_population_all_pass":
                centered_3_1_signed_gap_obligation[
                    "same_residue_fresh_population_all_pass"],
            "checked_gap_count":
                centered_3_1_signed_gap_obligation[
                    "checked_gap_count"],
            "tightest_reference_target":
                centered_3_1_signed_gap_obligation[
                    "tightest_reference_target"],
            "tightest_weighted_gap":
                centered_3_1_signed_gap_obligation[
                    "tightest_weighted_gap"],
        })
    for row in centered_3_1_signed_gap_obligation["obligation_rows"]:
        add_hit(
            target_stacks,
            str(row["reference_target"]),
            "centered-3-1-signed-gap-obligation",
            2.5,
            "same-residue signed empirical/correlation gap remains positive on checked fresh targets",
            row["weighted_gap_summary"])
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "centered-3-1-signed-gap-obligation",
        3.0,
        "selected stress-reference route now requires a non-post-hoc signed empirical/correlation gap")
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "centered-3-1-signed-gap-obligation",
        2.0,
        "same-residue cancellation narrows the bridge from local AP counts to a signed channel correlation estimate")

    layer(
        "centered-3-1-available-same-residue-population-audit",
        "Centered (3,1) survives available same-residue nonselection rows",
        "finite_available_population_strengthening",
        "evidence/q286-centered-3-1-available-same-residue-population-audit.json",
        3.0,
        "Finite available-population audit only; no signed correlation theorem.")
    add_hit(
        mechanism_stacks,
        "centered-3-1-selected-deficit-separator",
        "centered-3-1-available-same-residue-population-audit",
        3.0,
        "same-residue seed/nonseed/fresh split has zero failures on checked selected references",
        {
            "profile_target_count_after_residue_filter":
                centered_3_1_available_same_residue[
                    "profile_target_count_after_residue_filter"],
            "any_available_population_failure":
                centered_3_1_available_same_residue[
                    "any_available_population_failure"],
            "selected_reference_residues_mod_143":
                centered_3_1_available_same_residue[
                    "selected_reference_residues_mod_143"],
            "all_available_scope":
                next(
                    row for row in centered_3_1_available_same_residue[
                        "scope_summaries"]
                    if row["scope_id"]
                    == "same_residue_all_available_nonselection_targets"),
        })
    add_hit(
        target_stacks,
        "164598",
        "centered-3-1-available-same-residue-population-audit",
        3.0,
        "tightest checked available same-residue gate: 164598 versus 8000140",
        {
            "comparison_target": 8000140,
            "weighted_gap": 0.0003925287417802202,
            "comparison_scope": "same-window nonseed",
        })
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "centered-3-1-available-same-residue-population-audit",
        3.0,
        "available population strengthens selected-reference route but exposes near-collision at 164598/8000140")
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "centered-3-1-available-same-residue-population-audit",
        2.0,
        "signed channel correlation estimate must explain the thin 164598/8000140 same-residue gap")

    layer(
        "centered-3-1-residue5-near-collision-horizon",
        "Centered (3,1) residue-5 micro-horizon falsifies scalar promotion",
        "finite_falsifier",
        "evidence/q286-centered-3-1-residue5-near-collision-horizon.json",
        3.0,
        "Finite residue-5 horizon falsifier only; no signed correlation theorem.")
    add_hit(
        mechanism_stacks,
        "centered-3-1-selected-deficit-separator-clipped",
        "centered-3-1-residue5-near-collision-horizon",
        3.0,
        "predeclared same-residue horizon has zero local gap but crosses below reference 164598",
        {
            "reference_target":
                centered_3_1_residue5_horizon["reference_target"],
            "center_target":
                centered_3_1_residue5_horizon["center_target"],
            "target_count":
                centered_3_1_residue5_horizon["target_count"],
            "failing_target_count":
                centered_3_1_residue5_horizon["failing_target_count"],
            "minimum_weighted_gap":
                centered_3_1_residue5_horizon[
                    "weighted_gap_summary"]["minimum"],
        })
    add_hit(
        target_stacks,
        "7988986",
        "centered-3-1-residue5-near-collision-horizon",
        3.0,
        "worst residue-5 horizon falsifier below selected reference 164598",
        centered_3_1_residue5_horizon["tightest_rows"][0])
    add_hit(
        target_stacks,
        "164598",
        "centered-3-1-residue5-near-collision-horizon",
        2.5,
        "selected reference no longer below all local residue-5 horizon targets",
        {
            "failing_target_count":
                centered_3_1_residue5_horizon["failing_target_count"],
            "worst_failing_target":
                centered_3_1_residue5_horizon["tightest_rows"][0]["target"],
            "worst_weighted_gap":
                centered_3_1_residue5_horizon[
                    "weighted_gap_summary"]["minimum"],
        })
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "centered-3-1-residue5-near-collision-horizon",
        3.0,
        "scalar residue-5 neighborhood promotion is falsified by five same-residue crossings")
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "centered-3-1-residue5-near-collision-horizon",
        2.0,
        "future bridge must use higher-dimensional signed correlation or a narrower non-post-hoc family")

    layer(
        "centered-3-1-residue5-multichannel-horizon",
        "Pre-existing multichannel sets rescue the scalar residue-5 failure",
        "finite_multichannel_rescue",
        "evidence/q286-centered-3-1-residue5-multichannel-horizon.json",
        3.0,
        "Finite multichannel horizon audit only; no signed correlation theorem.")
    add_hit(
        mechanism_stacks,
        "distributed-channel-rescue-of-scalar-3-1-failure",
        "centered-3-1-residue5-multichannel-horizon",
        3.0,
        "watchlist and full 17-channel LP stay positive on the same residue-5 horizon where scalar (3,1) fails",
        {
            "scalar_passes":
                centered_3_1_residue5_multichannel[
                    "scalar_3_1_passes_horizon"],
            "kevin_watchlist_passes":
                centered_3_1_residue5_multichannel[
                    "kevin_watchlist_4_passes_horizon"],
            "frozen_full_17_lp_passes":
                centered_3_1_residue5_multichannel[
                    "frozen_full_17_lp_passes_horizon"],
            "watchlist_minimum_margin":
                next(
                    row for row in centered_3_1_residue5_multichannel[
                        "subset_results"]
                    if row["name"] == "kevin_watchlist_4")[
                        "weighted_gap_summary"]["minimum"],
            "full_lp_minimum_margin":
                next(
                    row for row in centered_3_1_residue5_multichannel[
                        "subset_results"]
                    if row["name"] == "frozen_full_17_lp")[
                        "weighted_gap_summary"]["minimum"],
        })
    add_hit(
        target_stacks,
        "164598",
        "centered-3-1-residue5-multichannel-horizon",
        3.0,
        "selected reference remains below all residue-5 horizon targets after multichannel aggregation",
        {
            "reference_target":
                centered_3_1_residue5_multichannel["reference_target"],
            "target_count":
                centered_3_1_residue5_multichannel["target_count"],
            "watchlist_passes":
                centered_3_1_residue5_multichannel[
                    "kevin_watchlist_4_passes_horizon"],
            "full_lp_passes":
                centered_3_1_residue5_multichannel[
                    "frozen_full_17_lp_passes_horizon"],
        })
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "centered-3-1-residue5-multichannel-horizon",
        3.0,
        "finite rescue redirects the bridge toward a distributed signed-correlation cone")
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "centered-3-1-residue5-multichannel-horizon",
        2.0,
        "(3,1) remains a possible stress-reference classifier coordinate, not a scalar closure theorem")

    layer(
        "multichannel-selected-reference-horizon-audit",
        "Kevin watchlist passes alternate selected-reference horizons",
        "finite_multichannel_rescue_and_falsifier",
        "evidence/q286-multichannel-selected-reference-horizon-audit.json",
        3.5,
        "Finite selected-reference horizon audit only; no signed correlation theorem.")
    add_hit(
        mechanism_stacks,
        "kevin-watchlist-distributed-cone",
        "multichannel-selected-reference-horizon-audit",
        3.5,
        "four-channel watchlist passes all selected-reference horizons without refitting",
        {
            "comparison_row_count":
                multichannel_selected_reference_horizon[
                    "comparison_row_count"],
            "kevin_watchlist_passes_all_horizons":
                multichannel_selected_reference_horizon[
                    "kevin_watchlist_4_passes_all_horizons"],
            "kevin_watchlist_minimum_margin":
                next(
                    row for row in multichannel_selected_reference_horizon[
                        "aggregate_subset_results"]
                    if row["name"] == "kevin_watchlist_4")[
                        "weighted_gap_summary"]["minimum"],
        })
    add_hit(
        mechanism_stacks,
        "full-17-lp-overincluded-for-13822",
        "multichannel-selected-reference-horizon-audit",
        3.0,
        "frozen full 17-channel LP fails every row in the 13822 selected-reference horizon",
        {
            "frozen_full_17_lp_passes_all_horizons":
                multichannel_selected_reference_horizon[
                    "frozen_full_17_lp_passes_all_horizons"],
            "frozen_full_17_lp_failure_count":
                next(
                    row for row in multichannel_selected_reference_horizon[
                        "aggregate_subset_results"]
                    if row["name"] == "frozen_full_17_lp")[
                        "failing_target_count"],
            "minimum_full_lp_margin":
                next(
                    row for row in multichannel_selected_reference_horizon[
                        "aggregate_subset_results"]
                    if row["name"] == "frozen_full_17_lp")[
                        "weighted_gap_summary"]["minimum"],
        })
    add_hit(
        target_stacks,
        "13822",
        "multichannel-selected-reference-horizon-audit",
        3.5,
        "strong watchlist reference: full 17 LP fails but watchlist stays positive",
        {
            "watchlist_minimum_margin":
                next(
                    row for row in multichannel_selected_reference_horizon[
                        "reference_results"]
                    if row["reference_target"] == 13822)[
                        "subset_results"][1]["weighted_gap_summary"][
                            "minimum"],
            "full_lp_failing_rows":
                next(
                    row for row in multichannel_selected_reference_horizon[
                        "reference_results"]
                    if row["reference_target"] == 13822)[
                        "subset_results"][3]["failing_target_count"],
        })
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "multichannel-selected-reference-horizon-audit",
        3.0,
        "bridge narrows from full 17 LP to a fixed four-channel watchlist cone")
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "multichannel-selected-reference-horizon-audit",
        2.5,
        "(3,1) helps the selected watchlist but cannot be used as scalar closure")

    layer(
        "watchlist-fresh-unseen-window-audit",
        "Watchlist and scalar (3,1) pass fresh unseen selected-reference windows",
        "finite_fresh_unseen_watchlist_evidence",
        "evidence/q286-watchlist-fresh-unseen-window-audit.json",
        3.5,
        "Finite fresh unseen window audit only; no signed correlation theorem.")
    add_hit(
        mechanism_stacks,
        "centered-3-1-selected-stress-fresh-window-classifier",
        "watchlist-fresh-unseen-window-audit",
        3.5,
        "scalar (3,1) passes all fresh unseen comparisons against selected deficit references",
        {
            "comparison_row_count":
                watchlist_fresh_unseen_window["comparison_row_count"],
            "scalar_3_1_passes_unseen_windows":
                watchlist_fresh_unseen_window[
                    "scalar_3_1_passes_unseen_windows"],
            "scalar_3_1_minimum_margin":
                next(
                    row for row in watchlist_fresh_unseen_window[
                        "subset_results"]
                    if row["name"] == "scalar_3_1")[
                        "weighted_gap_summary"]["minimum"],
        })
    add_hit(
        mechanism_stacks,
        "kevin-watchlist-distributed-cone",
        "watchlist-fresh-unseen-window-audit",
        3.5,
        "four-channel watchlist passes all fresh unseen comparisons against selected deficit references",
        {
            "kevin_watchlist_4_passes_unseen_windows":
                watchlist_fresh_unseen_window[
                    "kevin_watchlist_4_passes_unseen_windows"],
            "kevin_watchlist_4_minimum_margin":
                next(
                    row for row in watchlist_fresh_unseen_window[
                        "subset_results"]
                    if row["name"] == "kevin_watchlist_4")[
                        "weighted_gap_summary"]["minimum"],
        })
    add_hit(
        mechanism_stacks,
        "full-17-lp-overincluded-for-13822",
        "watchlist-fresh-unseen-window-audit",
        3.0,
        "frozen full 17-channel LP fails fresh unseen comparisons, including all rows against 13822",
        {
            "frozen_full_17_lp_passes_unseen_windows":
                watchlist_fresh_unseen_window[
                    "frozen_full_17_lp_passes_unseen_windows"],
            "frozen_full_17_lp_failure_count":
                next(
                    row for row in watchlist_fresh_unseen_window[
                        "subset_results"]
                    if row["name"] == "frozen_full_17_lp")[
                        "failing_target_count"],
        })
    add_hit(
        target_stacks,
        "13822",
        "watchlist-fresh-unseen-window-audit",
        3.5,
        "selected stress witness: scalar (3,1) and watchlist pass unseen windows while full 17 LP fails",
        {
            "fresh_unseen_target_count":
                watchlist_fresh_unseen_window["fresh_target_count"],
            "full_lp_failing_rows_against_13822": 606,
        })
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "watchlist-fresh-unseen-window-audit",
        3.0,
        "fresh unseen evidence supports a selected low-dimensional watchlist cone rather than full 17 LP")
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "watchlist-fresh-unseen-window-audit",
        3.0,
        "(3,1) survives as selected-stress fresh-window classifier coordinate")

    layer(
        "centered-3-1-stress-classifier-boundary",
        "Centered (3,1) classifier boundary is explicit",
        "finite_scope_guard",
        "evidence/q286-centered-3-1-stress-classifier-boundary.json",
        3.5,
        "Finite derived boundary receipt only; no broad stress-classifier theorem.")
    add_hit(
        mechanism_stacks,
        "centered-3-1-selected-stress-fresh-window-classifier",
        "centered-3-1-stress-classifier-boundary",
        3.5,
        "selected-reference classifier supported while broad full_nonpositive classifier is falsified",
        {
            "selected_reference_status":
                centered_3_1_stress_classifier_boundary["decision"][
                    "selected_reference_classifier_finite_status"],
            "broad_full_nonpositive_status":
                centered_3_1_stress_classifier_boundary["decision"][
                    "broad_full_nonpositive_classifier_finite_status"],
            "scalar_3_1_fresh_unseen_minimum_margin":
                centered_3_1_stress_classifier_boundary[
                    "selected_reference_evidence"][
                        "scalar_3_1_fresh_unseen"]["minimum_margin"],
            "full_nonpositive_at_or_above":
                centered_3_1_stress_classifier_boundary[
                    "broad_full_nonpositive_falsifier"][
                        "full_nonpositive"]["at_or_above_fresh_min_count"],
        })
    add_hit(
        mechanism_stacks,
        "full-17-lp-overincluded-for-13822",
        "centered-3-1-stress-classifier-boundary",
        3.0,
        "13822 remains a strong selected stress witness while full 17 LP over-includes harmful channels",
        centered_3_1_stress_classifier_boundary["focus_reference_13822"][
            "fresh_unseen"]["frozen_full_17_lp"])
    add_hit(
        target_stacks,
        "13822",
        "centered-3-1-stress-classifier-boundary",
        3.5,
        "boundary witness: low centered (3,1), negative volatile rim, full 17 LP fails every fresh unseen row",
        centered_3_1_stress_classifier_boundary["focus_reference_13822"])
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "centered-3-1-stress-classifier-boundary",
        3.5,
        "scope guard: selected-reference support and full_nonpositive falsifier must remain separate")
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "centered-3-1-stress-classifier-boundary",
        2.0,
        "next bridge must use a non-post-hoc selected stress predicate or signed correlation estimate")

    layer(
        "selected-stress-subclass-audit",
        "Selected stress splits into stable-core and volatile-overturn subclasses",
        "finite_subclass_falsifier",
        "evidence/q286-selected-stress-subclass-audit.json",
        3.5,
        "Finite selected-stress subclass audit only; no selected-stress theorem.")
    add_hit(
        mechanism_stacks,
        "selected-stress-two-subclass-split",
        "selected-stress-subclass-audit",
        3.5,
        "volatile-overturn is real but does not capture all selected deficit references",
        {
            "subclass_counts":
                selected_stress_subclass["subclass_counts"],
            "volatile_overturn_captures_all":
                selected_stress_subclass[
                    "volatile_overturn_captures_all_selected_deficits"],
        })
    for subclass in selected_stress_subclass["subclass_results"]:
        add_hit(
            mechanism_stacks,
            "centered-3-1-selected-stress-fresh-window-classifier",
            "selected-stress-subclass-audit",
            2.5,
            f"scalar (3,1) and watchlist remain positive on {subclass['subclass']} fresh unseen comparisons",
            {
                "subclass": subclass["subclass"],
                "references": subclass["references"],
                "scalar_3_1":
                    next(
                        row for row in subclass["subset_results"]
                        if row["name"] == "scalar_3_1"),
                "kevin_watchlist_4":
                    next(
                        row for row in subclass["subset_results"]
                        if row["name"] == "kevin_watchlist_4"),
            })
    for target in (13822, 164598, 1222142):
        add_hit(
            target_stacks,
            str(target),
            "selected-stress-subclass-audit",
            2.5,
            "selected deficit belongs to volatile-overturn subclass")
    for target in (24424, 55864):
        add_hit(
            target_stacks,
            str(target),
            "selected-stress-subclass-audit",
            2.5,
            "selected deficit belongs to stable-core-deficit subclass")
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "selected-stress-subclass-audit",
        3.5,
        "one volatile-overturn predicate is falsified as the whole selected-stress class")
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "selected-stress-subclass-audit",
        2.5,
        "signed correlation bridge must explain both stable-core-deficit and volatile-overturn subclasses")

    layer(
        "selected-stress-subclass-channel-decomposition",
        "Selected stress subclasses decomposed across outside channels",
        "finite_channel_decomposition",
        "evidence/q286-selected-stress-subclass-channel-decomposition.json",
        3.5,
        "Finite subclass channel-decomposition only; no signed correlation theorem.")
    for subclass in selected_stress_subclass_channel_decomposition[
            "subclass_results"]:
        scalar = next(
            row for row in subclass["subset_results"]
            if row["name"] == "scalar_3_1")
        without_3_1 = next(
            row for row in subclass["subset_results"]
            if row["name"] == "kevin_watchlist_without_3_1")
        channel_3_1 = next(
            row for row in subclass["channel_summary_rows"]
            if row["label_key"] == "3,1")
        add_hit(
            mechanism_stacks,
            "centered-3-1-selected-stress-fresh-window-classifier",
            "selected-stress-subclass-channel-decomposition",
            3.5,
            f"scalar (3,1) is positive and load-bearing on {subclass['subclass']}",
            {
                "subclass": subclass["subclass"],
                "references": subclass["references"],
                "scalar_3_1_minimum": scalar[
                    "weighted_gap_summary"]["minimum"],
                "watchlist_without_3_1_failures":
                    without_3_1["failing_target_count"],
                "channel_3_1_positive_count":
                    channel_3_1["positive_count"],
                "channel_3_1_negative_count":
                    channel_3_1["negative_count"],
                "passing_singletons":
                    subclass["smallest_positive_fixed_subset"][
                        "passing_subset_count_at_minimum_size"],
            })
    seed_scope = next(
        row for row in selected_stress_subclass_channel_decomposition[
            "target_scope_results"]
        if row["scope_id"] == "fresh_unseen_prior_seed_residue_targets")
    nonseed_scope = next(
        row for row in selected_stress_subclass_channel_decomposition[
            "target_scope_results"]
        if row["scope_id"] == "fresh_unseen_nonseed_targets")
    add_hit(
        mechanism_stacks,
        "fresh-unseen-seed-nonseed-scope-guard",
        "selected-stress-subclass-channel-decomposition",
        3.0,
        "fresh unseen seed-residue rows are not the earlier 12 zero-local seed targets",
        {
            "fresh_unseen_prior_seed_residue_target_count":
                seed_scope["target_count"],
            "fresh_unseen_nonseed_target_count":
                nonseed_scope["target_count"],
            "seed_scope_note":
                selected_stress_subclass_channel_decomposition[
                    "fresh_unseen_seed_scope_note"],
        })
    for target in (13822, 164598, 1222142):
        add_hit(
            target_stacks,
            str(target),
            "selected-stress-subclass-channel-decomposition",
            3.0,
            "volatile-overturn reference still separated by scalar (3,1) and watchlist")
    for target in (24424, 55864):
        add_hit(
            target_stacks,
            str(target),
            "selected-stress-subclass-channel-decomposition",
            3.0,
            "stable-core-deficit reference still separated by scalar (3,1) and watchlist")
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "selected-stress-subclass-channel-decomposition",
        3.5,
        "(3,1) is load-bearing on selected subclasses but broad stress class remains unproved")
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "selected-stress-subclass-channel-decomposition",
        3.0,
        "channel decomposition narrows the bridge to a signed empirical/correlation estimate")

    layer(
        "additional-stress-reference-generalization-audit",
        "Additional full_nonpositive stress references falsify broad watchlist generalization",
        "validated_falsifier",
        "evidence/q286-additional-stress-reference-generalization-audit.json",
        3.5,
        "Finite additional-stress-reference audit only; no broad stress theorem.")
    full_nonpositive_generalization = next(
        row for row in additional_stress_reference_generalization[
            "class_results"]
        if row["class_id"] == "full_nonpositive")
    add_hit(
        mechanism_stacks,
        "centered-3-1-selected-stress-fresh-window-classifier",
        "additional-stress-reference-generalization-audit",
        2.5,
        "selected-reference (3,1) signal does not extend to broad full_nonpositive references",
        {
            "additional_reference_count":
                additional_stress_reference_generalization[
                    "additional_reference_count"],
            "scalar_3_1_failures":
                additional_stress_reference_generalization[
                    "full_nonpositive_scalar_3_1_failure_count"],
            "scalar_3_1_reference_passes":
                full_nonpositive_generalization["reference_pass_counts"][
                    "scalar_3_1"],
        })
    add_hit(
        mechanism_stacks,
        "kevin-watchlist-distributed-cone",
        "additional-stress-reference-generalization-audit",
        2.5,
        "four-channel watchlist fails as a broad full_nonpositive reference cone",
        {
            "watchlist_failures":
                additional_stress_reference_generalization[
                    "full_nonpositive_watchlist_failure_count"],
            "watchlist_reference_passes":
                full_nonpositive_generalization["reference_pass_counts"][
                    "kevin_watchlist_4"],
            "comparison_row_count":
                additional_stress_reference_generalization[
                    "comparison_row_count"],
        })
    add_hit(
        mechanism_stacks,
        "centered-3-1-broad-full-nonpositive-generalization-falsified",
        "additional-stress-reference-generalization-audit",
        3.5,
        "broad full_nonpositive stress-reference version has many nonpositive fresh-unseen margins",
        {
            "scalar_3_1_failure_count":
                additional_stress_reference_generalization[
                    "full_nonpositive_scalar_3_1_failure_count"],
            "watchlist_failure_count":
                additional_stress_reference_generalization[
                    "full_nonpositive_watchlist_failure_count"],
            "reference_pass_counts":
                full_nonpositive_generalization["reference_pass_counts"],
        })
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "additional-stress-reference-generalization-audit",
        3.5,
        "broad full_nonpositive stress-reference theorem route finitely falsified")
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "additional-stress-reference-generalization-audit",
        3.0,
        "bridge must distinguish selected deficits from broad full_nonpositive references")

    layer(
        "selected-reference-scope-fork-audit",
        "Selected-reference signal and broad stress falsifier are separated",
        "validated_scope_guard",
        "evidence/q286-selected-reference-scope-fork-audit.json",
        3.5,
        "Finite scope-fork audit only; no selected-stress theorem.")
    add_hit(
        mechanism_stacks,
        "selected-reference-scope-fork",
        "selected-reference-scope-fork-audit",
        3.5,
        "selected five have zero failures while broad full_nonpositive references fail heavily",
        selected_reference_scope_fork["scope_comparison"])
    add_hit(
        mechanism_stacks,
        "centered-3-1-selected-stress-fresh-window-classifier",
        "selected-reference-scope-fork-audit",
        2.5,
        "(3,1) remains a selected-reference coordinate, not a broad stress classifier",
        {
            "selected_failures":
                selected_reference_scope_fork["scope_comparison"][
                    "selected_scalar_3_1_failures"],
            "broad_failures":
                selected_reference_scope_fork["scope_comparison"][
                    "broad_scalar_3_1_failures"],
            "selected_overlap_count":
                selected_reference_scope_fork["scope_comparison"][
                    "selected_reference_overlap_count"],
        })
    add_hit(
        mechanism_stacks,
        "centered-3-1-broad-full-nonpositive-generalization-falsified",
        "selected-reference-scope-fork-audit",
        3.5,
        "scope fork blocks promotion from selected references to broad full_nonpositive population",
        selected_reference_scope_fork["broad_full_nonpositive_fixture"][
            "reference_pass_counts"])
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "selected-reference-scope-fork-audit",
        3.5,
        "next theorem must define a sharper selected-stress family or signed correlation estimate")
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "selected-reference-scope-fork-audit",
        3.0,
        "local-to-channel bridge must preserve selected/broad fixture distinction")

    layer(
        "selected-stable-fixture-family-boundary-audit",
        "Selected-stable fixture boundary preserves the narrow (3,1) lemma",
        "validated_scope_guard",
        "evidence/q286-selected-stable-fixture-family-boundary-audit.json",
        3.5,
        "Finite family-boundary audit only; no selected-stress theorem.")
    add_hit(
        mechanism_stacks,
        "selected-stable-fixture-boundary",
        "selected-stable-fixture-family-boundary-audit",
        3.5,
        "selected-stable dominant-floor failure is the current exact fixture boundary",
        {
            "candidate_boundaries":
                selected_stable_fixture_family_boundary[
                    "candidate_family_boundaries"],
            "focus_reference_13822":
                selected_stable_fixture_family_boundary[
                    "focus_reference_13822"],
        })
    add_hit(
        mechanism_stacks,
        "centered-3-1-selected-stress-fresh-window-classifier",
        "selected-stable-fixture-family-boundary-audit",
        3.0,
        "(3,1) is supported only as a selected-reference classifier coordinate",
        selected_stable_fixture_family_boundary[
            "broad_full_nonpositive_falsifier"])
    add_hit(
        mechanism_stacks,
        "centered-3-1-bottom-rank-prospective-candidate",
        "selected-stable-fixture-family-boundary-audit",
        2.0,
        "bottom-7 centered (3,1) rank captures the selected five but is post-hoc until frozen prospectively")
    add_hit(
        target_stacks,
        "13822",
        "selected-stable-fixture-family-boundary-audit",
        3.0,
        "volatile-overturn witness for the selected-reference (3,1) lemma",
        selected_stable_fixture_family_boundary["focus_reference_13822"])
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "selected-stable-fixture-family-boundary-audit",
        3.5,
        "preserve the selected-reference lemma but do not promote it to broad stress without a prospective family rule")
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "selected-stable-fixture-family-boundary-audit",
        3.0,
        "next bridge must explain why selected-stable fixture rows separate while broad full_nonpositive rows do not")

    layer(
        "centered-3-1-threshold-subclass-audit",
        "Frozen centered (3,1) threshold selects a broad scalar-order subclass",
        "validated_threshold_subclass",
        "evidence/q286-centered-3-1-threshold-subclass-audit.json",
        3.0,
        "Finite scalar-threshold subclass only; no non-post-hoc stress theorem.")
    broad_threshold = next(
        row for row in centered_3_1_threshold_subclass[
            "threshold_subclasses"]
        if row["name"] == "broad_full_nonpositive_at_or_below_selected_max")
    add_hit(
        mechanism_stacks,
        "centered-3-1-threshold-scalar-subclass",
        "centered-3-1-threshold-subclass-audit",
        3.0,
        "frozen selected-reference threshold captures 33 independent broad full_nonpositive rows with zero scalar failures",
        {
            "selected_max_threshold":
                centered_3_1_threshold_subclass[
                    "selected_max_threshold"],
            "fresh_min_weighted_centered_3_1":
                centered_3_1_threshold_subclass[
                    "fresh_min_weighted_centered_3_1"],
            "threshold_reference_count":
                broad_threshold["reference_count"],
            "threshold_scalar_failures":
                broad_threshold[
                    "scalar_3_1_fresh_window_failure_count"],
            "broad_reference_count":
                centered_3_1_threshold_subclass[
                    "broad_full_nonpositive_reference_count"],
        })
    add_hit(
        mechanism_stacks,
        "centered-3-1-selected-stress-fresh-window-classifier",
        "centered-3-1-threshold-subclass-audit",
        2.0,
        "(3,1) is stronger than a single selected witness but remains scalar-selected")
    add_hit(
        mechanism_stacks,
        "centered-3-1-broad-full-nonpositive-generalization-falsified",
        "centered-3-1-threshold-subclass-audit",
        2.0,
        "full broad class still has many scalar failures outside the low-(3,1) threshold subclass",
        {
            "broad_scalar_3_1_failure_count":
                centered_3_1_threshold_subclass[
                    "broad_scalar_3_1_failure_count"],
            "selected_overlap_count":
                centered_3_1_threshold_subclass[
                    "selected_reference_overlap_with_broad_full_nonpositive"],
        })
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "centered-3-1-threshold-subclass-audit",
        3.0,
        "threshold subclass works only because it is selected by centered (3,1); independent stress definition remains open")
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "centered-3-1-threshold-subclass-audit",
        2.5,
        "bridge must explain independent stress rows falling below the scalar threshold")

    layer(
        "independent-stress-feature-audit",
        "Pre-existing filter features do not explain the low-(3,1) subclass",
        "validated_falsifier",
        "evidence/q286-independent-stress-feature-audit.json",
        3.0,
        "Finite independent-feature audit only; no stress theorem.")
    add_hit(
        mechanism_stacks,
        "independent-filter-wrapper-for-centered-3-1-falsified",
        "independent-stress-feature-audit",
        3.0,
        "natural filter predicates include above-threshold rows and do not independently define the low-(3,1) subclass",
        {
            "broad_reference_count":
                independent_stress_feature[
                    "broad_full_nonpositive_reference_count"],
            "low_centered_3_1_reference_count":
                independent_stress_feature[
                    "low_centered_3_1_reference_count"],
            "zero_failure_predeclared_predicate_count":
                len(independent_stress_feature[
                    "zero_failure_predeclared_predicates"]),
            "best_predeclared_predicate":
                independent_stress_feature[
                    "best_predeclared_predicate"]["name"],
        })
    add_hit(
        mechanism_stacks,
        "centered-3-1-threshold-scalar-subclass",
        "independent-stress-feature-audit",
        2.0,
        "low-(3,1) subclass remains scalar-selected rather than independently stress-defined")
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "independent-stress-feature-audit",
        3.0,
        "simple independent filter/residue wrapper is demoted; richer family or signed correlation estimate needed")
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "independent-stress-feature-audit",
        2.5,
        "filter-order features alone do not supply the local-to-channel bridge")

    layer(
        "centered-3-1-stress-class-audit",
        "Centered (3,1) fails the full-nonpositive stress class",
        "finite_stress_class_falsifier",
        "evidence/q286-centered-3-1-stress-class-audit.json",
        3.0,
        "Finite stress-class falsifier only; no universal stress-classifier theorem.")
    add_hit(
        mechanism_stacks,
        "centered-3-1-full-nonpositive-classifier-falsified",
        "centered-3-1-stress-class-audit",
        3.0,
        "predeclared full_nonpositive rows are not uniformly low in centered (3,1)",
        {
            "full_nonpositive_count":
                centered_3_1_stress_class["baseline_filter_window"][
                    "predicate_counts"]["full_nonpositive"],
            "channel_3_1_fail_count":
                centered_3_1_stress_class[
                    "channel_3_1_full_nonpositive_at_or_above_fresh_min_count"],
            "channel_3_1_separator_passes":
                centered_3_1_stress_class[
                    "channel_3_1_full_nonpositive_separator_passes"],
            "holdout_full_nonpositive_count":
                centered_3_1_stress_class["holdout_class_counts"][
                    "full_nonpositive"],
        })
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "centered-3-1-stress-class-audit",
        3.0,
        "full_nonpositive classifier version falsified; a different predeclared class or signed estimate is needed")

    layer(
        "selected-deficit-provenance-audit",
        "Selected deficit provenance separates fixture populations",
        "finite_scope_guard",
        "evidence/q286-selected-deficit-provenance-audit.json",
        2.0,
        "Finite provenance audit only; guards against merging distinct stress populations.")
    add_hit(
        mechanism_stacks,
        "selected-deficit-versus-full-nonpositive-scope-guard",
        "selected-deficit-provenance-audit",
        2.0,
        "selected deficit references are stable/volatile dominant-floor failures, not the full_nonpositive population",
        {
            "selected_deficit_targets":
                selected_deficit_provenance["selected_fixture"][
                    "selected_deficit_targets"],
            "baseline_span":
                selected_deficit_provenance[
                    "baseline_full_nonpositive_fixture"]["target_span"],
            "deficit_source_predicate":
                selected_deficit_provenance["selected_fixture"][
                    "deficit_source_predicate"],
        })
    add_hit(
        theorem_stacks,
        "centered-3-1-stress-class-theorem",
        "selected-deficit-provenance-audit",
        2.0,
        "scope guard: selected-deficit separation cannot be promoted across fixture predicates")

    layer(
        "ap-count-bridge-gap-audit",
        "Raw AP-count pigeonhole bridge is too sparse",
        "finite_combinatorial_falsifier",
        "evidence/q286-ap-count-bridge-gap-audit.json",
        3.0,
        "Finite bridge-gap audit only; no binary convolution theorem.")
    add_hit(
        mechanism_stacks,
        "raw-ap-count-pigeonhole-bridge-falsified",
        "ap-count-bridge-gap-audit",
        3.0,
        "BMOR/AP marginal floors can be satisfied by disjoint reflected residue-slot subsets",
        {
            "corollary_threshold": ap_count_bridge_gap[
                "corollary_1_6"]["simple_pi_lower_valid_from"],
            "ratio_exceeds_one_only_below": ap_count_bridge_gap[
                "corollary_1_6"]["ratio_exceeds_1_only_for_x_less_than"],
            "max_sampled_bmor_ratio": ap_count_bridge_gap[
                "bmor_logspace_sample"]["maximum_sampled_ratio_row"][
                    "two_lower_bounds_to_slot_ratio"],
            "max_sampled_bmor_ratio_x": ap_count_bridge_gap[
                "bmor_logspace_sample"]["maximum_sampled_ratio_row"]["x"],
        })
    add_hit(
        theorem_stacks,
        "ap-count-to-17-channel-bridge",
        "ap-count-bridge-gap-audit",
        3.0,
        "raw AP counts alone are demoted; bridge needs binary convolution or signed character correlation")
    add_hit(
        theorem_stacks,
        "fixed-modulus-binary-prime-discrepancy",
        "ap-count-bridge-gap-audit",
        2.0,
        "count-only countermodels preserve the need for fixed-modulus pair correlation")

    layer(
        "conditional-proof-stack",
        "Three explicit q286 conditional theorem branches",
        "theorem_map",
        "notes/q286-conditional-proof-stack.md",
        2.0,
        "Conditional map only; all pointwise hypotheses remain open.")
    for theorem in (
            "rarity-plus-complement-floor",
            "alignment-plus-complement-tail",
            "active-lane-strict-closure"):
        add_hit(
            theorem_stacks,
            theorem,
            "conditional-proof-stack",
            2.0,
            "named conditional branch")

    try:
        source_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        source_commit = None

    output = {
        "schema_version": 1,
        "receipt": "q286-evidence-glow-map",
        "generated_from_commit": source_commit,
        "purpose": (
            "Visualization-ready stacked evidence map.  Brighter means more "
            "repo-backed evidence layers overlap; it does not mean proved."),
        "visual_encoding": {
            "target_shape": "circle",
            "mechanism_shape": "hexagon",
            "theorem_gap_shape": "diamond",
            "brightness": "stack_weight normalized within each stack family",
            "suggested_use": (
                "Render target/mechanism/theorem stacks together; repeated "
                "hits glow brighter while status_boundary text prevents "
                "mistaking finite evidence for proof."),
        },
        "layers": layers,
        "target_stacks": sorted_stacks(target_stacks),
        "mechanism_stacks": sorted_stacks(mechanism_stacks),
        "theorem_gap_stacks": sorted_stacks(theorem_stacks),
        "goldbach_proved": False,
        "status_boundary": (
            "Glow is a navigation and hypothesis-generation layer only.  It "
            "does not prove rarity, strict closure, pointwise signed prime "
            "correlation, outer assembly, or Goldbach."),
    }

    out_path = EVIDENCE / "q286-evidence-glow-map.json"
    with out_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(output, handle, indent=2)
        handle.write("\n")
    print(out_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
