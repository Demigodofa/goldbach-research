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
