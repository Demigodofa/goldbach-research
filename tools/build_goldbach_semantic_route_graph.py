"""Build the current Goldbach semantic route graph.

The graph is a derived navigation artifact.  It organizes the active theorem
targets, falsifiers, HOLDs, and proof obligations without replacing the linear
human handoff or the authoritative evidence receipts.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"

BRIDGE_GATE = EVIDENCE / "goldbach-bridge-acceptance-gate-audit.json"
POINTWISE_ADVERSE = EVIDENCE / "q286-wbss-pointwise-adverse-drag-theorem-target.json"
RAW_ADVERSE = EVIDENCE / "q286-wbss-raw-adverse-drag-theorem-target.json"
L2_HOLD = EVIDENCE / "q286-wbss-zero-mass-l2-logical-bridge-audit.json"
SOURCE_WINDOW = (
    EVIDENCE / "mobius-moment-square-degree5-source-admissible-window-audit.json")
BROAD_PHASE = (
    EVIDENCE / "mobius-moment-square-degree5-checked-scale-phase-curve-sweep.json")
OUT = EVIDENCE / "goldbach-semantic-route-graph.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def node(node_id, node_type, title, status, **properties):
    return {
        "id": node_id,
        "type": node_type,
        "title": title,
        "status": status,
        **properties,
    }


def edge(source, relation, target, **properties):
    return {
        "source": source,
        "relation": relation,
        "target": target,
        **properties,
    }


def proof_obligation_nodes(pointwise):
    nodes = []
    edges = []
    for index, obligation in enumerate(pointwise["proof_obligations"], 1):
        node_id = f"proof-obligation:{index}"
        nodes.append(node(
            node_id,
            "proof_obligation",
            f"Proof obligation {index}",
            "open",
            statement=obligation,
        ))
        edges.append(edge(
            "theorem-target:pointwise-adverse-drag",
            "requires",
            node_id,
            ordinal=index,
        ))
    return nodes, edges


def build_receipt():
    bridge = load_json(BRIDGE_GATE)
    pointwise = load_json(POINTWISE_ADVERSE)
    raw = load_json(RAW_ADVERSE)
    l2 = load_json(L2_HOLD)
    source = load_json(SOURCE_WINDOW)
    broad = load_json(BROAD_PHASE)

    pointwise_summary = pointwise["finite_calibration"]["summary"]
    raw_summary = raw["finite_calibration"]["summary"]
    l2_status = bridge["zero_mass_l2_status"]
    source_status = bridge["metric_soft_source_window_status"]
    failure = broad["failure_rows"][0]

    nodes = [
        node(
            "gate:current-bridge-acceptance",
            "bridge_gate",
            "Current Goldbach bridge acceptance gate",
            "active",
            evidence=str(BRIDGE_GATE.relative_to(ROOT)),
            finite_evidence_is_acceptance_condition=False,
            current_required_bridge=bridge["acceptance_gate"][
                "current_required_bridge"],
        ),
        node(
            "theorem-target:raw-adverse-drag",
            "theorem_target",
            "Raw q286-WBSS adverse-drag estimate",
            "live_unproved",
            evidence=str(RAW_ADVERSE.relative_to(ROOT)),
            statement=raw["acceptance_condition"][
                "required_universal_statement"],
            checked_rows=raw_summary["row_count"],
            finite_rows_pass_gate=(
                raw_summary[
                    "raw_adverse_drag_not_below_raw_local_main_count"] == 0),
            worst_checked_ratio=raw_summary[
                "raw_adverse_drag_ratio_summary"]["maximum"],
            worst_checked_target=raw_summary[
                "largest_raw_adverse_drag_ratio_row"]["target"],
            theorem_proved=raw["raw_adverse_drag_theorem_proved"],
        ),
        node(
            "theorem-target:pointwise-adverse-drag",
            "theorem_target",
            "Pointwise unnormalized adverse-drag estimate",
            "live_unproved",
            evidence=str(POINTWISE_ADVERSE.relative_to(ROOT)),
            statement=pointwise["acceptance_condition"][
                "required_universal_statement"],
            checked_rows=pointwise_summary["row_count"],
            checked_rows_failing=pointwise_summary[
                "adverse_drag_not_below_local_main_count"],
            worst_checked_ratio=pointwise_summary[
                "adverse_drag_ratio_summary"]["maximum"],
            worst_checked_target=pointwise_summary[
                "tightest_adverse_drag_row"]["target"],
            universal_bound_open=pointwise["universal_bound_open"],
            theorem_proved=pointwise[
                "pointwise_adverse_drag_theorem_proved"],
        ),
        node(
            "hold:l2-logical-bridge",
            "hold",
            "q286 aggregate L2 logical bridge",
            "hold_not_confirmed",
            evidence=str(L2_HOLD.relative_to(ROOT)),
            zero_mass_sanity_confirmed=l2_status[
                "zero_mass_arithmetic_sanity_confirmed_on_checked_rows"],
            raw_strict_shape_noncircular=l2_status[
                "raw_strict_l2_shape_is_noncircular"],
            logical_bridge_confirmed=l2_status[
                "l2_logical_bridge_confirmed"],
            row_local_cap_violations=l2_status[
                "observed_row_local_cap_violations"],
            global_min_cap_violations=l2_status[
                "observed_global_min_cap_violations"],
            theorem_proved=l2["aggregate_l2_theorem_proved"],
        ),
        node(
            "finite-diagnostic:source-admissible-window",
            "finite_audit",
            "Metric-soft source-admissible window audit",
            "finite_diagnostic",
            evidence=str(SOURCE_WINDOW.relative_to(ROOT)),
            all_source_starts_pass=source["all_source_starts_pass"],
            failing_translated_start_count=source[
                "failing_active_row_start_count"],
            source_start_failure_count=source[
                "source_start_failure_count"],
            minimum_source_start_slack=source[
                "minimum_source_start_canonical_slack"],
            theorem_proved=source[
                "source_admissible_window_theorem_proved"],
        ),
        node(
            "finite-falsifier:broad-phase-translation",
            "finite_falsifier",
            "Broad checked-scale phase-curve translation falsifier",
            "falsified",
            evidence=str(BROAD_PHASE.relative_to(ROOT)),
            falsified_statement=(
                "active/full dominance for every checked scale, prime, "
                "and translated active row start 0..2A"),
            scale_modulus=failure["scale_modulus"],
            prime_modulus=failure["prime_modulus"],
            active_row_start=failure["active_row_start"],
            label=failure["label"],
            ratio=failure["active_over_full_ratio"],
            slack=failure["dominance_slack_above_one_half"],
        ),
        node(
            "rule:finite-evidence-not-acceptance",
            "acceptance_rule",
            "Finite evidence is not acceptance",
            "active",
            invalid_closeouts=bridge["acceptance_gate"]["invalid_closeouts"],
        ),
        node(
            "open-gap:source-window-implication",
            "open_gap",
            "Source-window implication theorem",
            "open",
            statement=(
                "Metric-soft source-window dominance needs a separate "
                "source-backed implication before it can function as a "
                "Goldbach bridge."),
        ),
        node(
            "target:goldbach",
            "conjecture_target",
            "Goldbach conjecture",
            "open",
            proved=False,
        ),
    ]

    obligation_nodes, obligation_edges = proof_obligation_nodes(pointwise)
    nodes.extend(obligation_nodes)

    edges = [
        edge("gate:current-bridge-acceptance", "selects-live-target",
             "theorem-target:raw-adverse-drag"),
        edge("gate:current-bridge-acceptance", "selects-live-target",
             "theorem-target:pointwise-adverse-drag"),
        edge("gate:current-bridge-acceptance", "blocks-finite-closeout",
             "rule:finite-evidence-not-acceptance"),
        edge("hold:l2-logical-bridge", "blocks-route",
             "theorem-target:pointwise-adverse-drag",
             reason="L2 is not the confirmed bridge; raw adverse drag remains live."),
        edge("hold:l2-logical-bridge", "reactivates-only-if",
             "proof-obligation:strict-raw-l2-theorem",
             statement=(
                 "A strict raw pointwise L2 theorem is proved without "
                 "assuming positive mass first.")),
        edge("theorem-target:raw-adverse-drag", "raw-form-of",
             "theorem-target:pointwise-adverse-drag"),
        edge("theorem-target:pointwise-adverse-drag", "would-imply",
             "target:goldbach",
             boundary=(
                 "Only after the universal sufficiently-large theorem and "
                 "finite remainder are independently verified.")),
        edge("finite-diagnostic:source-admissible-window", "supports",
             "open-gap:source-window-implication"),
        edge("finite-diagnostic:source-admissible-window", "not-acceptance-for",
             "target:goldbach"),
        edge("finite-falsifier:broad-phase-translation", "falsifies",
             "candidate:broad-all-translation-dominance"),
        edge("finite-falsifier:broad-phase-translation", "narrows-to",
             "finite-diagnostic:source-admissible-window"),
        edge("rule:finite-evidence-not-acceptance", "blocks-closeout-of",
             "target:goldbach"),
        edge("rule:finite-evidence-not-acceptance", "blocks-closeout-of",
             "theorem-target:pointwise-adverse-drag"),
        edge("gate:current-bridge-acceptance", "classifies",
             "hold:l2-logical-bridge"),
        edge("gate:current-bridge-acceptance", "classifies",
             "finite-diagnostic:source-admissible-window"),
        *obligation_edges,
    ]

    graph = {
        "schema_version": 1,
        "status": "GRAPH_current_goldbach_semantic_route",
        "source_commit": source_commit(),
        "question": (
            "Can the active Goldbach route be represented as a semantic "
            "dependency graph while keeping human-facing notes linear?"),
        "answer": (
            "Yes.  This graph keeps active theorem targets, finite "
            "diagnostics, falsifiers, HOLDs, and proof obligations in one "
            "machine-facing structure.  It is derived from receipts and is "
            "not mathematical authority."),
        "authority_boundary": (
            "Derived navigation graph only.  The owning repo commit, evidence "
            "receipts, tests, notes, and cited mathematics remain authority."),
        "human_linear_sources": [
            "RESEARCH_GOAL.md",
            "REFRESH_HANDOFF.md",
            "notes/goldbach-bridge-acceptance-gate-audit.md",
            "notes/goldbach-bridge-semantic-route-graph.md",
        ],
        "machine_sources": [
            str(BRIDGE_GATE.relative_to(ROOT)),
            str(RAW_ADVERSE.relative_to(ROOT)),
            str(POINTWISE_ADVERSE.relative_to(ROOT)),
            str(L2_HOLD.relative_to(ROOT)),
            str(SOURCE_WINDOW.relative_to(ROOT)),
            str(BROAD_PHASE.relative_to(ROOT)),
        ],
        "nodes": nodes,
        "edges": edges,
        "projection_views": {
            "branch_map": {
                "nexus": "target:goldbach",
                "trunk": "gate:current-bridge-acceptance",
                "shape_boundary": (
                    "This is not a pure tree.  Branches can loop back to "
                    "gates, holds, or dead-end rules when evidence changes "
                    "or when a route repeats the same failed acceptance "
                    "condition."),
                "live_branches": [
                    {
                        "id": "branch:raw-adverse-drag",
                        "node": "theorem-target:raw-adverse-drag",
                        "description": (
                            "Live sufficient bridge route if the universal "
                            "raw pointwise inequality is proved."),
                        "twigs": [
                            "proof-obligation:1",
                            "proof-obligation:2",
                            "proof-obligation:3",
                            "proof-obligation:4",
                        ],
                    },
                    {
                        "id": "branch:source-window",
                        "node": "finite-diagnostic:source-admissible-window",
                        "description": (
                            "Alive as geometry guidance, but not a Goldbach "
                            "bridge without a source-window implication "
                            "theorem."),
                        "twigs": ["open-gap:source-window-implication"],
                    },
                ],
                "held_branches": [
                    {
                        "id": "branch:aggregate-l2",
                        "node": "hold:l2-logical-bridge",
                        "description": (
                            "Held because zero-mass sanity and raw "
                            "non-circularity do not establish the L2 bridge, "
                            "and normalized finite caps fail."),
                        "reactivates_only_if": (
                            "strict raw pointwise L2 theorem, not another "
                            "normalized finite scan"),
                    },
                ],
                "dead_ends": [
                    {
                        "id": "dead-end:broad-all-translation-dominance",
                        "node": "finite-falsifier:broad-phase-translation",
                        "description": (
                            "Falsified by M=149, p=163, active row start 1 "
                            "under the unchanged broad translated-window "
                            "quantifier."),
                    },
                    {
                        "id": "dead-end:finite-evidence-acceptance",
                        "node": "rule:finite-evidence-not-acceptance",
                        "description": (
                            "Finite passes cannot close Goldbach or the "
                            "bridge target without a universal theorem and "
                            "finite remainder threshold."),
                    },
                ],
            },
            "cycle_or_return_signals": [
                {
                    "cycle": [
                        "finite q286 adverse-drag calibration",
                        "gate:current-bridge-acceptance",
                        "rule:finite-evidence-not-acceptance",
                        "theorem-target:pointwise-adverse-drag",
                    ],
                    "meaning": (
                        "More finite adverse-drag passes return to the same "
                        "acceptance gate until a universal theorem or finite "
                        "remainder threshold exists."),
                    "action": (
                        "Do not continue this loop for comfort; use finite "
                        "rows only to falsify or calibrate a named theorem "
                        "attempt."),
                },
                {
                    "cycle": [
                        "normalized aggregate L2 scan",
                        "hold:l2-logical-bridge",
                        "proof-obligation:strict-raw-l2-theorem",
                        "hold:l2-logical-bridge",
                    ],
                    "meaning": (
                        "Normalized L2 data loops back to HOLD unless the "
                        "changed condition is a strict raw pointwise L2 "
                        "theorem."),
                    "action": (
                        "Treat repeated normalized L2 scans as churn under "
                        "unchanged conditions."),
                },
                {
                    "cycle": [
                        "metric-soft source-window evidence",
                        "open-gap:source-window-implication",
                        "finite-diagnostic:source-admissible-window",
                    ],
                    "meaning": (
                        "Source-window evidence loops until an implication "
                        "theorem is supplied; the finite pattern alone does "
                        "not reach Goldbach."),
                    "action": (
                        "Either prove/falsify the source-window implication "
                        "or keep the lane as geometry guidance."),
                },
            ],
            "by_theorem_attempt": [
                {
                    "name": "raw adverse-drag bridge",
                    "nodes": [
                        "theorem-target:raw-adverse-drag",
                        "theorem-target:pointwise-adverse-drag",
                        "proof-obligation:1",
                        "proof-obligation:2",
                        "proof-obligation:3",
                        "proof-obligation:4",
                    ],
                    "state": "live_unproved",
                    "next_use": (
                        "Focus proof work on the universal pointwise "
                        "unnormalized estimate and its explicit threshold."),
                },
                {
                    "name": "aggregate L2 bridge",
                    "nodes": ["hold:l2-logical-bridge"],
                    "state": "hold_not_confirmed",
                    "next_use": (
                        "Do not spend more finite-normalized L2 effort unless "
                        "the changed condition is a strict raw pointwise L2 "
                        "theorem attempt."),
                },
                {
                    "name": "metric-soft source-window route",
                    "nodes": [
                        "finite-diagnostic:source-admissible-window",
                        "open-gap:source-window-implication",
                        "finite-falsifier:broad-phase-translation",
                    ],
                    "state": "finite_guidance_needs_implication",
                    "next_use": (
                        "Use as source-window geometry guidance, not as a "
                        "Goldbach bridge without an implication theorem."),
                },
            ],
            "by_result_state": {
                "live_unproved": [
                    "theorem-target:raw-adverse-drag",
                    "theorem-target:pointwise-adverse-drag",
                ],
                "hold": ["hold:l2-logical-bridge"],
                "falsified": ["finite-falsifier:broad-phase-translation"],
                "finite_diagnostic": [
                    "finite-diagnostic:source-admissible-window"],
                "open_gap": [
                    "open-gap:source-window-implication",
                    "proof-obligation:1",
                    "proof-obligation:2",
                    "proof-obligation:3",
                    "proof-obligation:4",
                ],
            },
            "by_evidence_weight": [
                {
                    "node": "theorem-target:pointwise-adverse-drag",
                    "weight": "finite-348-row-calibration",
                    "return_status": (
                        "useful calibration, not acceptance; theorem gap open"),
                },
                {
                    "node": "hold:l2-logical-bridge",
                    "weight": "negative-348-row-diagnostic",
                    "return_status": (
                        "low return for more normalized finite L2 scans "
                        "because row-local and global caps already fail"),
                },
                {
                    "node": "finite-diagnostic:source-admissible-window",
                    "weight": "finite-440-start-map",
                    "return_status": (
                        "positive for admissible source-window direction, "
                        "thin as bridge evidence"),
                },
                {
                    "node": "finite-falsifier:broad-phase-translation",
                    "weight": "single-row-falsifier",
                    "return_status": (
                        "high return: permanently blocks the broad "
                        "all-translation quantifier under unchanged setup"),
                },
            ],
            "churn_or_low_return_flags": [
                {
                    "area": "normalized aggregate L2 finite scans",
                    "reason": (
                        "zero-mass sanity is already separated from bridge; "
                        "observed normalized caps fail on checked rows"),
                    "recommended_action": (
                        "sleep unless replaced by a raw strict pointwise "
                        "theorem shape"),
                },
                {
                    "area": "all-translated active-window dominance",
                    "reason": (
                        "one checked row finitely falsifies the broad "
                        "quantifier"),
                    "recommended_action": (
                        "do not retry without a changed admissibility "
                        "definition or source-window implication"),
                },
            ],
            "thin_or_frontier_flags": [
                {
                    "area": "source-window implication theorem",
                    "reason": (
                        "source windows pass finitely, but no theorem links "
                        "metric-soft source-window dominance to Goldbach"),
                    "recommended_action": (
                        "derive or falsify the implication before treating "
                        "this route as a bridge"),
                },
                {
                    "area": "universal pointwise raw adverse-drag bound",
                    "reason": (
                        "finite rows calibrate ratios, but the universal "
                        "fixed-modulus binary-prime correlation estimate is "
                        "still open"),
                    "recommended_action": (
                        "attack proof obligation 3 or build a falsifier for "
                        "a proposed analytic bound"),
                },
            ],
        },
        "node_count": len(nodes),
        "edge_count": len(edges),
        "goldbach_proved": False,
        "semantic_graph_authoritative": False,
        "decision": (
            "Use this graph as a compact route map for the current active "
            "family: raw pointwise adverse-drag is live and unproved; L2 is "
            "held; broad translated dominance is finitely falsified; "
            "source-window evidence is useful but needs an implication "
            "theorem; finite evidence is not acceptance."),
    }
    return graph


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    graph = load_json(OUT)
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": graph["status"],
        "node_count": graph["node_count"],
        "edge_count": graph["edge_count"],
        "goldbach_proved": graph["goldbach_proved"],
        "semantic_graph_authoritative": graph["semantic_graph_authoritative"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
