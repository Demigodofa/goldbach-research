"""Audit the mass boundary in the q286-WBSS pointwise gate.

The logic bridge gate correctly demoted normalized L2.  This follow-up checks
whether the surviving pointwise adverse-drag statement is genuinely mass-free.

It is not, as currently encoded: the four-modulus WBSS formulas use the
normalized actual strict-central orbit measure mu_N.  They are excellent
conditional distribution statements once strict-central prime-pair mass exists,
but they do not by themselves create that mass.  A Goldbach bridge must either
pair them with a positive-mass theorem or rawize the witness and prove a direct
positive unnormalized weighted sum.

This is a theorem-target correction only.  It proves no positive-mass theorem,
raw witness theorem, pointwise adverse-drag theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-wbss-rawization-obligation-audit.json"

POINTWISE_SOURCE = (
    EVIDENCE / "q286-wbss-pointwise-adverse-drag-theorem-target.json")
LOGIC_GATE_SOURCE = EVIDENCE / "q286-wbss-logic-bridge-gate-audit.json"
L2_SOURCE = (
    EVIDENCE / "q286-wbss-multiplicative-character-l2-observed-moment-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def finite_summary(values):
    vals = [float(value) for value in values]
    return {
        "count": len(vals),
        "minimum": min(vals),
        "mean": sum(vals) / len(vals),
        "maximum": max(vals),
    }


def build_receipt():
    pointwise = load_json(POINTWISE_SOURCE)
    logic = load_json(LOGIC_GATE_SOURCE)
    l2 = load_json(L2_SOURCE)

    definitions = pointwise["definitions"]
    rows = pointwise["finite_calibration"]["rows"]
    zero = l2["zero_mass_check"]

    uses_normalized_mu = "mu_N" in definitions["projected_errors"]
    local_main_has_no_mass_factor = (
        "T_N" not in definitions["local_main"]
        and "pair" not in definitions["local_main"].lower())

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "pointwise_adverse_drag_target": str(
                POINTWISE_SOURCE.relative_to(ROOT)),
            "logic_bridge_gate": str(LOGIC_GATE_SOURCE.relative_to(ROOT)),
            "l2_observed_moment_zero_mass_check": str(
                L2_SOURCE.relative_to(ROOT)),
        },
        "status": "CORRECTION_pointwise_gate_requires_mass_or_raw_witness",
        "status_boundary": (
            "logical rawization obligation only; no positive-mass theorem, "
            "raw witness theorem, pointwise adverse-drag theorem, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof"),
        "goldbach_proved": False,
        "positive_mass_theorem_proved": False,
        "raw_witness_theorem_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "question": (
            "Does the surviving pointwise adverse-drag gate avoid the "
            "positive-mass problem, or does it still need rawization?"),
        "answer": (
            "As currently encoded, the q286-WBSS pointwise gate is still "
            "conditional on strict-central prime-pair mass.  Its projected "
            "errors use the normalized actual orbit measure mu_N, and the "
            "local main M(N)=<u_a,phi_a> has no raw pair-count factor.  Thus "
            "A_-(N)<M(N) is a distribution/anti-alignment theorem once "
            "mu_N exists.  A Goldbach bridge needs either a separate theorem "
            "T_N>0 or a direct raw unnormalized witness theorem."),
        "mass_boundary_audit": {
            "projected_errors_definition": definitions["projected_errors"],
            "local_main_definition": definitions["local_main"],
            "uses_normalized_actual_measure_mu_N": uses_normalized_mu,
            "local_main_has_no_pair_count_factor": local_main_has_no_mass_factor,
            "finite_zero_mass_check_passed": (
                zero["zero_pair_count"] == 0
                and zero["zero_actual_mass_count"] == 0),
            "finite_zero_pair_count": int(zero["zero_pair_count"]),
            "finite_zero_actual_mass_count": int(zero["zero_actual_mass_count"]),
            "finite_zero_mass_meaning": zero["decision"],
            "logical_consequence": (
                "The checked rows have mass, so the normalized diagnostics "
                "are arithmetically meaningful there.  This finite fact does "
                "not supply a universal positive-mass theorem."),
        },
        "finite_calibration": {
            "finite_evidence_is_acceptance_condition": False,
            "row_count": len(rows),
            "local_main_summary": finite_summary(
                row["local_main"] for row in rows),
            "actual_formula_expectation_summary": finite_summary(
                row["actual_formula_expectation"] for row in rows),
            "adverse_drag_summary": finite_summary(
                row["adverse_drag"] for row in rows),
            "adverse_drag_ratio_summary": finite_summary(
                row["adverse_drag_ratio"] for row in rows),
            "positive_actual_formula_rows": sum(
                row["actual_formula_expectation"] > 0.0 for row in rows),
        },
        "corrected_theorem_paths": {
            "path_A_raw_witness": {
                "statement": (
                    "Prove a direct raw weighted witness W_Phi(N)>0 for every "
                    "sufficiently large covered even N."),
                "why_it_closes_mass_gap": (
                    "If no strict-central prime pair exists, every raw "
                    "summand is absent and W_Phi(N)=0.  Strict raw positivity "
                    "therefore forces nonempty support."),
                "status": "preferred_clean_bridge_but_unproved",
            },
            "path_B_positive_mass_plus_distribution": {
                "statement": (
                    "Prove T_N>0 for every sufficiently large covered even N, "
                    "then prove the normalized distribution inequality "
                    "A_-(N)<M(N) for those N."),
                "why_it_closes_mass_gap": (
                    "T_N>0 makes mu_N well-defined; the pointwise "
                    "anti-alignment theorem then proves the frozen WBSS "
                    "expectation positive on existing mass."),
                "status": "two_theorem_bridge_unproved",
            },
            "path_C_rawized_adverse_drag": {
                "statement": (
                    "Multiply the normalized decomposition by a proved raw "
                    "mass lower bound and bound raw adverse drag below raw "
                    "local main."),
                "why_it_closes_mass_gap": (
                    "This is only non-circular if the raw mass lower bound "
                    "does not already assume the desired prime-pair support."),
                "status": "possible_but_requires_independent_mass_input",
            },
        },
        "route_decision": {
            "previous_logic_gate_still_useful": True,
            "previous_logic_gate_needs_correction": True,
            "l2_remains_reservoir": logic["route_decision"]["l2_status"],
            "active_acceptance_rephrased": (
                "direct raw unnormalized witness positivity, or positive "
                "strict-central mass plus normalized pointwise adverse-drag "
                "control"),
            "smallest_next_step": (
                "Build or reject a raw WBSS witness identity W_Phi(N) whose "
                "strict positivity forces a strict-central prime pair without "
                "first normalizing by existing mass."),
        },
        "decision": (
            "Correct the bridge boundary.  The current pointwise "
            "adverse-drag inequality is a valid conditional distribution "
            "target, not a standalone Goldbach bridge, because it is stated "
            "through the normalized actual orbit measure mu_N.  The next "
            "proof object should be a raw unnormalized witness theorem "
            "W_Phi(N)>0, or a two-theorem package consisting of positive "
            "strict-central mass plus normalized adverse-drag control."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
