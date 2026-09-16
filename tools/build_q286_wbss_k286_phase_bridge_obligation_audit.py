"""State the K_286 phase bridge obligation after sparse concentration fails.

The phase-envelope concentration audit is useful only if it sharpens the next
universal theorem target.  This derived receipt connects that finite diagnostic
to the existing q286-WBSS logic bridge gate: finite phase broadness does not
prove the bridge, but it rules out tiny phase-label shortcuts and forces any
phase proof to be a broad signed-cancellation or distributional estimate.

No phase-envelope theorem, phase-cancellation theorem, pointwise adverse-drag
theorem, q286 threshold theorem, strict-central Goldbach theorem, or Goldbach
proof is established.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
PHASE_SOURCE = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-phase-envelope-concentration-audit.json")
LOGIC_SOURCE = EVIDENCE / "q286-wbss-logic-bridge-gate-audit.json"
POINTWISE_SOURCE = EVIDENCE / "q286-wbss-pointwise-adverse-drag-theorem-target.json"
OUT = EVIDENCE / "q286-wbss-k286-phase-bridge-obligation-audit.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    phase = load_json(PHASE_SOURCE)
    logic = load_json(LOGIC_SOURCE)
    pointwise = load_json(POINTWISE_SOURCE)
    phase_summary = phase["finite_diagnostic"]["summary"]
    logic_gate = logic["unnormalized_pointwise_gate"]
    pointwise_acceptance = pointwise["acceptance_condition"]
    cover90 = phase_summary["threshold_count_summaries"]["0.9"]
    cover75 = phase_summary["threshold_count_summaries"]["0.75"]
    cover50 = phase_summary["threshold_count_summaries"]["0.5"]
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-phase-bridge-obligation-audit",
        "source_commit": source_commit(),
        "sources": {
            "phase_envelope_concentration": str(
                PHASE_SOURCE.relative_to(ROOT)),
            "phase_envelope_source_commit": phase["source_commit"],
            "logic_bridge_gate": str(LOGIC_SOURCE.relative_to(ROOT)),
            "logic_bridge_source_commit": logic["source_commit"],
            "pointwise_adverse_drag_target": str(
                POINTWISE_SOURCE.relative_to(ROOT)),
            "pointwise_source_commit": pointwise["source_commit"],
        },
        "status": "TARGET_broad_k286_phase_cancellation_bridge_required",
        "question": (
            "After the finite K_286 phase envelope is broad, what exact "
            "non-circular theorem would a phase route have to prove?"),
        "answer": (
            "A phase route cannot be accepted from top-pair labels, small "
            "phase bands, or finite cover counts.  It must prove a universal "
            "pointwise lower bound for the signed K_286 phase sum, or the "
            "full unnormalized adverse-drag inequality A_-(N)<M(N), for every "
            "sufficiently large covered even N."),
        "finite_phase_diagnostic": {
            "finite_evidence_is_acceptance_condition": False,
            "row_count": phase_summary["row_count"],
            "pair_count_per_row": phase_summary["pair_count_summary"][
                "mean"],
            "cover_count_mean_50": cover50["mean"],
            "cover_count_mean_75": cover75["mean"],
            "cover_count_mean_90": cover90["mean"],
            "cover_count_min_90": cover90["minimum"],
            "cover_count_max_90": cover90["maximum"],
            "top_pair_fraction_mean": phase_summary[
                "top_pair_fraction_summary"]["mean"],
            "top_pair_fraction_max": phase_summary[
                "top_pair_fraction_summary"]["maximum"],
            "inverse_participation_count_mean": phase_summary[
                "inverse_participation_count_summary"]["mean"],
            "entropy_effective_count_mean": phase_summary[
                "entropy_effective_count_summary"]["mean"],
            "pair_cancellation_ratio_mean": phase_summary[
                "pair_cancellation_ratio_summary"]["mean"],
            "diagnostic_consequence": (
                "The checked rows require many of the 30 active conjugate "
                "pairs to cover the absolute envelope.  This is a falsifier "
                "for tiny sparse phase-label proofs, not a universal bound."),
        },
        "logical_bridge_boundary": {
            "zero_mass_check_status": (
                "finite diagnostic only; not a proof of positivity for "
                "unobserved N"),
            "l2_status": logic["route_decision"]["l2_status"],
            "active_acceptance_target": logic["route_decision"][
                "active_acceptance_target"],
            "required_universal_statement": logic_gate[
                "required_universal_statement"],
            "normalization_boundary": logic_gate["normalization_boundary"],
            "finite_remainder_requirement": pointwise_acceptance[
                "finite_remainder_requirement"],
        },
        "phase_theorem_obligation": {
            "signed_pair_sum_form": (
                "E_286(N)=sum_p P_p(N), where p ranges over the active "
                "K_286 conjugate phase pairs and P_p(N) is the real pair "
                "contribution at target N."),
            "acceptable_k286_subgoal": (
                "Prove E_286(N) >= -B_286(N) pointwise with companion bounds "
                "B_70(N), B_130(N), and B_154(N) such that "
                "B_70(N)+B_130(N)+B_154(N)+B_286(N) < M(N)."),
            "acceptable_full_goal": (
                "Prove A_-(N)=sum_d max(0,-E_d(N)) < M(N) directly for every "
                "sufficiently large covered even N."),
            "not_enough": [
                "a list of dominant phase-pair labels observed on finite rows",
                "a small phase band seeded by early lifts",
                "finite cover-count means such as 16.875 pairs for 90%",
                "a normalized L2 premise that first needs positive mass",
                "a fitted residual absorption constant",
            ],
            "smallest_next_theorem_move": (
                "Look for a source-backed signed correlation inequality that "
                "bounds the K_286 phase-pair sum as a whole; treat pair-label "
                "visualization as a locator for structure, not proof."),
        },
        "candidate": {
            "name": "broad K286 signed phase-cancellation theorem",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Exploit cancellation across many conjugate phase pairs "
                "instead of isolating a few labels.  The theorem target is a "
                "signed sum bound, not an absolute-envelope sparsity bound."),
            "prediction": (
                "Rows with broad absolute envelopes can still be safe when "
                "the signed pair sum has small adverse projection relative to "
                "the local main term."),
            "falsifier": (
                "A covered row family where the signed K_286 adverse component "
                "alone reaches the local main term, or where any proposed "
                "B_286 plus companion bounds exceed M(N), kills this route."),
            "visualization_role": (
                "A linked 3D scatter/table can help locate phase families, "
                "lift drift, and strange rows, but any discovered pattern must "
                "be converted into the pointwise inequalities above."),
        },
        "decision": (
            "TARGET_broad_k286_phase_cancellation_bridge_required.  The "
            "finite phase-envelope audit is useful because it rules out tiny "
            "sparse phase-label shortcuts and points toward broad signed "
            "phase cancellation.  It does not relax the logical gate: the "
            "route still needs a universal, pointwise, unnormalized estimate "
            "strong enough to imply A_-(N)<M(N), plus a finite remainder."),
        "status_boundary": (
            "Theorem-target audit only.  No broad phase-envelope theorem, no "
            "phase-cancellation theorem, no coefficient-direction nonalignment "
            "theorem, no universal pointwise raw bound, no q286 threshold "
            "theorem, no strict-central Goldbach theorem, and no Goldbach "
            "proof is established."),
        "broad_phase_envelope_theorem_proved": False,
        "phase_cancellation_theorem_proved": False,
        "coefficient_direction_nonalignment_theorem_proved": False,
        "universal_pointwise_raw_bound_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    diagnostic = receipt["finite_phase_diagnostic"]
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "row_count": diagnostic["row_count"],
        "cover_count_mean_90": diagnostic["cover_count_mean_90"],
        "active_acceptance_target": receipt[
            "logical_bridge_boundary"]["active_acceptance_target"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
