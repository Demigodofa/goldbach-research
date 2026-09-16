"""Try three candidate arithmetic/statistical objects against current patterns.

This is deliberately speculative but bounded.  Each candidate must name a
formula-like object, a mechanism, a prediction, a falsifier, and its present
status.  A failed candidate is preserved as a failed candidate, not promoted.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    scale_parameters,
)
from tools.build_mobius_moment_square_degree5_q46189_exception_bound_audit import (  # noqa: E402
    SCALE,
)
from tools.build_mobius_moment_square_degree5_q46189_source_factor_pattern_map_audit import (  # noqa: E402
    enrich_rows,
    source_block_matrix,
)


OUT = Path("evidence/goldbach-three-candidate-synthesis-audit.json")
NOTE = Path("notes/goldbach-three-candidate-synthesis-audit.md")
ATLAS = Path("evidence/goldbach-route-pattern-atlas.json")
COMPONENT = (
    Path("evidence")
    / "q286-wbss-four-modulus-component-envelope-horizon-audit.json")
RAW_TARGET = Path("evidence") / "q286-wbss-raw-adverse-drag-theorem-target.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def mirror_blocks(ordered_pairs):
    seen = []
    for a, b in ordered_pairs:
        u, v = sorted((a, b))
        if (u, v) not in seen:
            seen.append((u, v))
    return sorted(seen)


def source_gap_curvature(blocks):
    gaps = [v - u for u, v in blocks]
    if len(gaps) != 3:
        return None, gaps
    return gaps[0] - 2 * gaps[1] + gaps[2], gaps


def first_cross_non_middle(matrix):
    labels = []
    for item in matrix["block_interactions_by_middle_loss"]:
        for side in ("left_block", "right_block"):
            block = tuple(tuple(pair) for pair in item[side])
            if block not in labels:
                labels.append(block)
    labels = sorted(labels)
    if len(labels) < 2:
        return None
    left, right = labels[0], labels[1]
    selected = []
    for item in matrix["block_interactions_by_middle_loss"]:
        item_left = tuple(tuple(pair) for pair in item["left_block"])
        item_right = tuple(tuple(pair) for pair in item["right_block"])
        if (item_left, item_right) in ((left, right), (right, left)):
            selected.append(item)
    return sum(item["non_middle_sum"] for item in selected)


def sign(value):
    if value is None:
        return None
    if abs(value) < 1e-15:
        return 0
    return 1 if value > 0 else -1


def curvature_audit():
    parameters = scale_parameters(SCALE)
    rows = enrich_rows()
    checked = []
    for row in rows:
        q = row["reduced_denominator"]
        matrix = source_block_matrix(q, parameters)
        blocks = mirror_blocks(matrix["ordered_source_pairs"])
        curvature, gaps = source_gap_curvature(blocks)
        non_middle = first_cross_non_middle(matrix)
        predicted = None
        if curvature is not None and curvature != 0:
            predicted = -1 if curvature > 0 else 1
        actual = sign(non_middle)
        checked.append({
            "reduced_denominator": q,
            "source_gaps": gaps,
            "source_gap_curvature": curvature,
            "first_cross_non_middle": non_middle,
            "predicted_sign": predicted,
            "actual_sign": actual,
            "matched": predicted is not None and predicted == actual,
        })
    valid = [row for row in checked if row["predicted_sign"] is not None]
    return {
        "checked_row_count": len(checked),
        "valid_prediction_count": len(valid),
        "match_count": sum(row["matched"] for row in valid),
        "mismatch_count": sum(not row["matched"] for row in valid),
        "q38038": next(row for row in checked
                       if row["reduced_denominator"] == 38038),
        "q41990": next(row for row in checked
                       if row["reduced_denominator"] == 41990),
        "mismatches": [row for row in valid if not row["matched"]],
    }


def build_receipt():
    atlas = json.loads((ROOT / ATLAS).read_text(encoding="utf-8"))
    component = json.loads((ROOT / COMPONENT).read_text(encoding="utf-8"))
    raw_target = json.loads((ROOT / RAW_TARGET).read_text(encoding="utf-8"))
    curvature = curvature_audit()
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_goldbach_three_candidate_synthesis",
        "question": (
            "Can three new-to-this-task arithmetic or statistical objects be "
            "assembled from the current patterns, and do any earn a next test?"),
        "source_atlas": str(ATLAS),
        "attempts": [
            {
                "attempt": 1,
                "name": "raw adverse-envelope margin",
                "state": "live_candidate_unproved",
                "formula": (
                    "Delta_raw(N) = L_raw(N) - sum_d max(0, -E_raw,d(N)); "
                    "target Delta_raw(N) > 0 for all sufficiently large N."),
                "mechanism": (
                    "Separate each projected modulus' harmful signed "
                    "contribution, throw away helpful terms, and ask whether "
                    "raw local main still beats the disconnected adverse "
                    "envelope."),
                "current_evidence": [
                    component["decision"],
                    raw_target["decision"],
                ],
                "prediction": (
                    "The normalized finite component-envelope margin should "
                    "continue pointing to a raw per-modulus adverse supremum "
                    "theorem, not a cancellation-dependent theorem."),
                "falsifier": (
                    "A correctly raw row with Delta_raw(N) <= 0, or a proof "
                    "that E_raw,d cannot be bounded independently of the "
                    "unknown prime-pair mass, kills this as a standalone bridge."),
                "next_test": (
                    "Define the raw E_raw,d and L_raw objects explicitly and "
                    "check whether the existing finite component envelope is "
                    "an artifact of normalization."),
                "goldbach_proved": False,
            },
            {
                "attempt": 2,
                "name": "source-gap curvature sign rule",
                "state": "falsified_as_universal_sign_rule",
                "formula": (
                    "For ordered mirror source blocks (u_i,v_i), set "
                    "g_i=v_i-u_i and kappa=g_1-2*g_2+g_3.  Trial rule: "
                    "sign(first cross-block non-middle) = -sign(kappa)."),
                "mechanism": (
                    "The q=38038 versus q=41990 split suggested that "
                    "accelerating or decelerating contraction of source gaps "
                    "might control whether the first off-diagonal block pays "
                    "or drags."),
                "current_evidence": curvature,
                "prediction": (
                    "If the one-number curvature were structural, it would "
                    "predict first cross-block non-middle sign across the "
                    "replacement landscape."),
                "falsifier": (
                    "All-row mismatch rate materially above noise; observed "
                    f"{curvature['mismatch_count']} mismatches among "
                    f"{curvature['valid_prediction_count']} valid rows."),
                "next_test": (
                    "Do not promote kappa alone.  Use it only, if at all, as "
                    "one feature inside the fuller source-block interaction "
                    "audit."),
                "goldbach_proved": False,
            },
            {
                "attempt": 3,
                "name": "route-closure pressure score",
                "state": "triage_statistic_only",
                "formula": (
                    "score(route)=raw_pointwise + input_side_invariant + "
                    "predeclared_falsifier + finite_margin "
                    "- normalization_dependency - fitted_constant "
                    "- high_mode_diffusion - posthoc_selector."),
                "mechanism": (
                    "The research record has a repeated failure mode: a route "
                    "looks good finitely, then loses theorem value when it "
                    "depends on normalization, fitted constants, many hidden "
                    "Fourier modes, or post-hoc selectors.  This score keeps "
                    "that penalty explicit while choosing the next test."),
                "current_evidence": {
                    "q286_raw_adverse_drag_score": 3,
                    "q46189_source_block_matrix_score": 3,
                    "residual_absorption_constant_score": 0,
                    "small_fourier_mode_shortcut_score": -1,
                    "atlas_read": atlas["rill_read"],
                },
                "prediction": (
                    "The next useful work should come from routes scoring "
                    "high because they are raw or input-side and falsifiable, "
                    "not from routes scoring high only because finite data "
                    "looks clean."),
                "falsifier": (
                    "If this score repeatedly selects lanes that add no new "
                    "falsifier, no sharper theorem obligation, and no failed "
                    "candidate to retire, it is bookkeeping rather than math."),
                "next_test": (
                    "Use the score to justify the all-row source-block "
                    "interaction audit over another scalar or visual map."),
                "goldbach_proved": False,
            },
        ],
        "decision": (
            "Attempt 1 remains the clean q286 proof-shaped target but still "
            "requires raw definitions and a universal theorem.  Attempt 2 was "
            "a real new arithmetic statistic and failed as a universal "
            "one-number sign rule, which is useful because it blocks a cheap "
            "overfit.  Attempt 3 is only a route-selection statistic; it says "
            "to spend the next work on raw pointwise estimates or input-side "
            "matrix invariants, not more fitted scalar dots."),
        "candidate_next_action": (
            "Build the all-row source-block interaction sign audit, carrying "
            "source-gap curvature as a failed single-feature baseline."),
        "finite_synthesis_only": True,
        "new_to_this_task_candidate_synthesis": True,
        "universal_raw_pointwise_theorem_proved": False,
        "source_gap_curvature_theorem_proved": False,
        "route_closure_score_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    lines = [
        "# Goldbach three-candidate synthesis audit",
        "",
        "## Question",
        "",
        receipt["question"],
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_goldbach_three_candidate_synthesis_audit.py",
        "evidence/goldbach-three-candidate-synthesis-audit.json",
        "```",
        "",
        "## Attempts",
        "",
    ]
    for attempt in receipt["attempts"]:
        lines.extend([
            f"### Attempt {attempt['attempt']}: {attempt['name']}",
            "",
            f"State: `{attempt['state']}`.",
            "",
            f"Formula: {attempt['formula']}",
            "",
            f"Mechanism: {attempt['mechanism']}",
            "",
            f"Falsifier: {attempt['falsifier']}",
            "",
            f"Next test: {attempt['next_test']}",
            "",
        ])
    lines.extend([
        "## Decision",
        "",
        receipt["decision"],
        "",
        "This is finite candidate synthesis only.  It proves no universal raw",
        "pointwise theorem, source-gap curvature theorem, route-closure theorem,",
        "strict-central Goldbach theorem, or Goldbach proof.",
        "",
    ])
    NOTE.write_text("\n".join(lines), encoding="utf-8")


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    write_note(receipt)
    curvature = receipt["attempts"][1]["current_evidence"]
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "attempt_count": len(receipt["attempts"]),
        "curvature_matches": curvature["match_count"],
        "curvature_valid": curvature["valid_prediction_count"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
