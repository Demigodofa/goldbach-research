"""Unify q286 and Q46189 lanes as an adverse-alignment schema.

This is not a proof and not a numeric merge of incompatible fixtures.  It
records the strongest common language currently visible: decompose a witness
into channels, isolate one-sided harmful mass, and ask whether a raw or local
structural budget beats the disconnected adverse envelope.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
Q286_RAW = Path("evidence/q286-wbss-raw-adverse-drag-theorem-target.json")
Q286_COMPONENT = (
    Path("evidence")
    / "q286-wbss-four-modulus-component-envelope-horizon-audit.json")
Q46189_SIGN = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-source-block-sign-audit.json")
Q46189_MATRIX = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-source-matrix-margin-audit.json")
ATLAS = Path("evidence/goldbach-route-pattern-atlas.json")
OUT = Path("evidence/goldbach-adverse-alignment-unification-audit.json")
NOTE = Path("notes/goldbach-adverse-alignment-unification-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def build_receipt():
    q286_raw = load(Q286_RAW)
    q286_component = load(Q286_COMPONENT)
    q46189_sign = load(Q46189_SIGN)
    q46189_matrix = load(Q46189_MATRIX)
    atlas = load(ATLAS)
    best_matrix = q46189_matrix[
        "best_matrix_feature_by_target"]["row_margin_above_failure"]
    best_feature = q46189_matrix[
        "best_feature_by_target"]["row_margin_above_failure"]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_goldbach_adverse_alignment_unification",
        "source_receipts": {
            "q286_raw_adverse_drag": str(Q286_RAW),
            "q286_component_envelope": str(Q286_COMPONENT),
            "q46189_source_block_sign": str(Q46189_SIGN),
            "q46189_source_matrix_margin": str(Q46189_MATRIX),
            "route_pattern_atlas": str(ATLAS),
        },
        "question": (
            "Can q286 and Q46189 be combined as versions of the same "
            "bad-mass-cannot-coherently-align principle?"),
        "answer": (
            "Yes as a shared theorem schema and research language; not yet "
            "as a proved theorem or a merged numeric formula."),
        "shared_schema": {
            "name": "adverse alignment envelope",
            "formula_template": (
                "Given a decomposition into channels C_N, define "
                "A_D(N)=sum_{c in C_N} max(0,-E_c(N)).  A sufficient bridge "
                "has the shape A_D(N) < B_D(N), where B_D(N) is a raw or "
                "local structural budget independent of already assuming the "
                "desired prime-pair support."),
            "interpretation": (
                "A counterexample-shaped obstruction would need harmful mass "
                "to align across all available channels strongly enough to "
                "beat the structural budget.  A proof would show that such "
                "coherent adverse alignment is impossible in the covered "
                "class."),
            "required_non_circularity": (
                "B_D and E_c must be raw, or the route must separately prove "
                "the positive mass it conditions on.  A normalized channel "
                "statement alone is not a Goldbach bridge."),
        },
        "q286_instantiation": {
            "channels": ["70", "130", "154", "286"],
            "budget": "L_raw(N), or normalized local main only as calibration",
            "adverse_object": "A_raw_-(N)=sum_d max(0,-U_d(N))",
            "current_strength": (
                "Strong finite theorem shape: raw sufficient inequality is "
                "non-circular in form, and the finite component envelope "
                "survives the checked horizon."),
            "key_evidence": [
                q286_raw["decision"],
                q286_component["decision"],
            ],
            "open_gap": (
                "A universal pointwise raw adverse-drag theorem is still "
                "unproved.  The finite component suprema are calibration, "
                "not theorem constants."),
        },
        "q46189_instantiation": {
            "channels": (
                "source-block and bucket interactions in the replacement "
                "packet matrix"),
            "budget": "row margin above the -1 failure boundary",
            "adverse_object": (
                "middle-band/source-block harmful mass and its surrounding "
                "non-middle compensation"),
            "current_strength": (
                "Useful diagnostic/falsifier language, but not theorem-ready "
                "after simple sign, curvature, and matrix-margin features "
                "failed or stayed weak."),
            "key_evidence": [
                q46189_sign["decision"],
                q46189_matrix["decision"],
            ],
            "open_gap": (
                "No pre-output input-side source-matrix invariant currently "
                "predicts row margin strongly enough to be promoted."),
            "best_input_feature": {
                "feature": best_feature["feature"],
                "pearson": best_feature["pearson"],
            },
            "best_matrix_feature": {
                "feature": best_matrix["feature"],
                "pearson": best_matrix["pearson"],
            },
        },
        "combined_read": {
            "what_matches": [
                "Both lanes separate harmful signed mass from a budget that must remain positive.",
                "Both lanes punish scalar shortcuts: one bad channel cannot be treated as the whole object.",
                "Both lanes point toward one-sided adverse envelopes rather than delicate cancellation as the proof object.",
            ],
            "what_does_not_match": [
                "q286 has a clearer raw inequality target; Q46189 currently has only diagnostic source-matrix evidence.",
                "The fixtures live in different coordinate systems, so their numeric constants should not be merged.",
                "Q46189 simple input-side matrix features are weak, so it cannot currently supply the missing q286 theorem.",
            ],
            "rill_intuition": (
                "The common story is real enough to guide search: a hard "
                "counterexample would need coherent adverse alignment across "
                "independent channels.  But the only presently theorem-shaped "
                "combined path is to formalize the q286 raw envelope and use "
                "Q46189 as a falsifier/analogy source, not as proof."),
        },
        "candidate_next_action": {
            "name": "q286 raw adverse-envelope definition audit",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Translate the shared adverse-alignment schema back into the "
                "stronger q286 raw setting: identify which quantities are "
                "actually raw, which depend on T_N or mu_N, and what "
                "universal estimate would make A_D(N)<B_D(N) a bridge."),
            "prediction": (
                "If the combination is useful, the raw q286 definition audit "
                "should isolate a non-circular theorem statement and expose "
                "exactly where current finite receipts are only calibration."),
            "falsifier": (
                "If the adverse envelope cannot be stated without hidden "
                "normalization or unknown support, the combined story remains "
                "conditional and should not be called a proof route."),
            "smallest_next_test": (
                "Build a q286 raw adverse-envelope definition audit from the "
                "raw-adverse-drag target and zero-mass/rawization receipts."),
        },
        "decision": (
            "q286 and Q46189 can be combined as a shared adverse-alignment "
            "schema: harmful signed mass should not coherently align across "
            "all available channels strongly enough to beat the relevant "
            "budget.  This is currently a useful research language, not a "
            "theorem.  q286 is the stronger proof-shaped instantiation; "
            "Q46189 supplies diagnostics and failed shortcut baselines."),
        "combined_as_shared_language_only": True,
        "merged_numeric_formula_established": False,
        "adverse_alignment_theorem_proved": False,
        "universal_raw_pointwise_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
        "atlas_rill_read": atlas["rill_read"],
    }


def write_note(receipt):
    q286 = receipt["q286_instantiation"]
    q46189 = receipt["q46189_instantiation"]
    lines = [
        "# Goldbach adverse-alignment unification audit",
        "",
        "## Question",
        "",
        receipt["question"],
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_goldbach_adverse_alignment_unification_audit.py",
        "evidence/goldbach-adverse-alignment-unification-audit.json",
        "```",
        "",
        "## Answer",
        "",
        receipt["answer"],
        "",
        "## Shared Schema",
        "",
        receipt["shared_schema"]["formula_template"],
        "",
        receipt["shared_schema"]["interpretation"],
        "",
        "## q286 Instantiation",
        "",
        f"Channels: `{q286['channels']}`.",
        "",
        f"Adverse object: `{q286['adverse_object']}`.",
        "",
        q286["current_strength"],
        "",
        "## Q46189 Instantiation",
        "",
        q46189["current_strength"],
        "",
        f"Best input feature: `{q46189['best_input_feature']['feature']}` "
        f"with Pearson `{q46189['best_input_feature']['pearson']}`.",
        "",
        f"Best matrix feature: `{q46189['best_matrix_feature']['feature']}` "
        f"with Pearson `{q46189['best_matrix_feature']['pearson']}`.",
        "",
        "## Decision",
        "",
        receipt["decision"],
        "",
        "This is a unifying research language only.  It proves no adverse-",
        "alignment theorem, universal raw pointwise theorem, strict-central",
        "Goldbach theorem, or Goldbach proof.",
        "",
    ]
    NOTE.write_text("\n".join(lines), encoding="utf-8")


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    write_note(receipt)
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "answer": receipt["answer"],
        "combined_as_shared_language_only": (
            receipt["combined_as_shared_language_only"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
