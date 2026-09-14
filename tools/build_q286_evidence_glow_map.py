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
