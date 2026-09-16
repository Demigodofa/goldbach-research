"""Audit the q286 raw adverse-envelope definition boundary.

The adverse-alignment unification audit points back to q286 as the stronger
proof-shaped lane.  This receipt separates three states that are easy to blur:

* a normalized distribution inequality after strict-central mass exists;
* a formally raw strict inequality whose failure at zero support is useful;
* a theorem-ready raw estimate stated directly in unnormalized prime-pair sums.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_TARGET = Path("evidence/q286-wbss-raw-adverse-drag-theorem-target.json")
RAWIZATION = Path("evidence/q286-wbss-rawization-obligation-audit.json")
ZERO_MASS_L2 = Path("evidence/q286-wbss-zero-mass-l2-logical-bridge-audit.json")
PRINCIPAL = Path("evidence/q286-wbss-signed-weight-principal-factor-audit.json")
UNIFICATION = Path("evidence/goldbach-adverse-alignment-unification-audit.json")
OUT = Path("evidence/q286-raw-adverse-envelope-definition-audit.json")
NOTE = Path("notes/q286-raw-adverse-envelope-definition-audit.md")


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def build_receipt():
    raw = load(RAW_TARGET)
    rawization = load(RAWIZATION)
    zero_mass = load(ZERO_MASS_L2)
    principal = load(PRINCIPAL)
    unification = load(UNIFICATION)
    finite_rows = raw["finite_calibration"]["rows"]
    ratios = [row["raw_adverse_drag_ratio"] for row in finite_rows]
    gaps = [row["raw_adverse_gate_gap"] for row in finite_rows]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q286_raw_adverse_envelope_definition",
        "source_receipts": {
            "raw_adverse_drag_theorem_target": str(RAW_TARGET),
            "rawization_obligation": str(RAWIZATION),
            "zero_mass_l2_logical_bridge": str(ZERO_MASS_L2),
            "signed_weight_principal_factor": str(PRINCIPAL),
            "adverse_alignment_unification": str(UNIFICATION),
        },
        "question": (
            "Can the q286 adverse-envelope route be stated as a genuinely "
            "raw, non-circular theorem target, and exactly where do T_N or "
            "mu_N dependencies remain?"),
        "definitions_audit": {
            "strict_central_total_weight_T_N": {
                "definition": raw["definitions"]["strict_central_total_weight"],
                "classification": "raw_sum_but_unknown_support",
                "boundary": (
                    "T_N is a raw binary-prime sum, not a normalized "
                    "probability.  But any proof that first establishes "
                    "T_N>0 and only then applies q286 has become a two-theorem "
                    "bridge, not a standalone q286 bridge."),
            },
            "normalized_mu_N": {
                "definition": (
                    "mu_N is the actual strict-central binary-prime orbit "
                    "measure normalized by T_N."),
                "classification": "conditional_only",
                "boundary": rawization["mass_boundary_audit"][
                    "logical_consequence"],
            },
            "local_main_M": {
                "definition": (
                    "M(a)=<u_a,phi_a>, a local uniform q286-WBSS factor."),
                "classification": "positive_local_factor_not_support",
                "boundary": principal["principal_factorization"][
                    "if_T_N_zero"],
            },
            "raw_local_main_L_raw": {
                "definition": raw["definitions"]["raw_local_main"],
                "classification": "raw_form_but_T_N_factor",
                "boundary": (
                    "L_raw vanishes at zero support because it is T_N*M(a).  "
                    "A strict inequality with L_raw on the right can create "
                    "support, but the proof must not get L_raw positivity by "
                    "assuming T_N>0 first."),
            },
            "raw_projected_errors_U_d": {
                "definition": raw["definitions"]["raw_projected_error"],
                "classification": "theorem_ready_only_when_defined_directly",
                "boundary": (
                    "U_d is acceptable only when expressed as an unnormalized "
                    "projected binary-prime discrepancy.  The expression "
                    "T_N*E_d is just a finite-row or mass-positive shorthand "
                    "if E_d was first defined through mu_N."),
            },
            "raw_adverse_envelope_A_raw_minus": {
                "definition": raw["definitions"]["raw_adverse_drag"],
                "classification": "noncircular_strict_target_unproved",
                "boundary": raw["definitions"]["zero_support_boundary"],
            },
        },
        "three_bridge_states": {
            "conditional_distribution_state": {
                "statement": "A_-(N)<M(N) after mu_N exists.",
                "status": "not_a_goldbach_bridge_by_itself",
                "reason": rawization["decision"],
            },
            "formal_raw_strict_state": {
                "statement": "A_raw_-(N)<L_raw(N).",
                "status": "noncircular_theorem_shape_but_unproved",
                "reason": raw["decision"],
            },
            "theorem_ready_raw_sum_state": {
                "statement": (
                    "Define every U_d(N), L_raw(N), and W_phi(N) directly as "
                    "unnormalized sums or explicit local factors, then prove "
                    "the strict inequality pointwise without importing "
                    "positive mass as a premise."),
                "status": "required_next_theorem_form",
                "reason": zero_mass["l2_bridge_classification"][
                    "why_raw_strict_shape_is_noncircular"],
            },
        },
        "finite_calibration_summary": {
            "row_count": len(finite_rows),
            "finite_evidence_is_acceptance_condition": False,
            "maximum_raw_adverse_drag_ratio": max(ratios),
            "minimum_raw_adverse_gate_gap": min(gaps),
            "all_checked_raw_gate_gaps_positive": all(gap > 0 for gap in gaps),
            "role": raw["finite_calibration"]["role"],
        },
        "proof_obligation": {
            "required_universal_statement": raw["acceptance_condition"][
                "required_universal_statement"],
            "cleanest_route": rawization["corrected_theorem_paths"][
                "path_A_raw_witness"]["statement"],
            "acceptable_adverse_route": (
                "Prove A_raw_-(N)<L_raw(N) directly in raw sums for every "
                "covered sufficiently large even N; finite calibration may "
                "suggest constants but cannot supply them."),
            "not_acceptable_as_standalone": [
                "A normalized inequality A_-(N)<M(N) after assuming mu_N exists.",
                "Multiplying a normalized theorem by T_N after separately proving T_N>0, unless explicitly labeled as a two-theorem bridge.",
                "Using fitted finite adverse ratios as universal constants.",
            ],
        },
        "route_decision": {
            "q286_raw_adverse_envelope_noncircular_as_statement": True,
            "q286_raw_adverse_envelope_theorem_proved": False,
            "hidden_mu_N_dependency_removed_by_current_receipt": False,
            "why_not_removed": (
                "This audit clarifies definitions only.  It does not produce "
                "the required pointwise raw binary-prime discrepancy estimate."),
            "next_action": (
                "Build a raw-sum expansion ledger for U_d(N) and W_phi(N), "
                "with no mu_N notation, then ask what known or new analytic "
                "estimate could bound the one-sided adverse envelope."),
        },
        "decision": (
            "The q286 adverse-envelope route survives as a non-circular "
            "strict theorem shape only when it is stated directly in raw "
            "unnormalized sums.  The definitions L_raw=T_N*M(a) and "
            "U_d=T_N*E_d are dangerous if E_d is first introduced through "
            "mu_N: that is a mass-positive shorthand, not the theorem.  The "
            "next useful object is a raw-sum expansion ledger for U_d and "
            "W_phi, or else an explicit two-theorem bridge with a separate "
            "positive-mass theorem."),
        "finite_definition_audit_only": True,
        "positive_mass_theorem_proved": False,
        "raw_adverse_envelope_theorem_proved": False,
        "raw_weighted_witness_theorem_proved": False,
        "universal_raw_pointwise_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
        "unification_read": unification["decision"],
    }


def write_note(receipt):
    summary = receipt["finite_calibration_summary"]
    lines = [
        "# q286 raw adverse-envelope definition audit",
        "",
        "## Question",
        "",
        receipt["question"],
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_q286_raw_adverse_envelope_definition_audit.py",
        "evidence/q286-raw-adverse-envelope-definition-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"finite calibration rows:                  {summary['row_count']}",
        f"max checked raw adverse ratio:             {summary['maximum_raw_adverse_drag_ratio']}",
        f"min checked raw adverse gate gap:          {summary['minimum_raw_adverse_gate_gap']}",
        f"all checked raw gate gaps positive:        {summary['all_checked_raw_gate_gaps_positive']}",
        "finite evidence is acceptance condition:  false",
        "raw adverse-envelope theorem proved:      false",
        "```",
        "",
        "The strict statement `A_raw_-(N)<L_raw(N)` is non-circular in form:",
        "if strict-central support is empty, both sides are zero and the strict",
        "inequality fails.  A proof of the strict inequality would therefore",
        "create support.",
        "",
        "But the proof must be stated directly in raw sums.  `U_d=T_N*E_d` is",
        "only safe as shorthand after `U_d` is also defined without `mu_N`.",
        "Likewise `L_raw=T_N*M(a)` is a raw-form local main, but it cannot be",
        "made positive by assuming `T_N>0` unless the route is explicitly a",
        "two-theorem bridge.",
        "",
        "## Decision",
        "",
        receipt["decision"],
        "",
        "This is a definition-boundary audit only.  It proves no positive-mass",
        "theorem, raw adverse-envelope theorem, raw weighted witness theorem,",
        "strict-central Goldbach theorem, or Goldbach proof.",
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
        "noncircular_as_statement": receipt["route_decision"][
            "q286_raw_adverse_envelope_noncircular_as_statement"],
        "theorem_proved": receipt["raw_adverse_envelope_theorem_proved"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
