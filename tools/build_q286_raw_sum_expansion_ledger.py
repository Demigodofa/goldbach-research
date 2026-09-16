"""Build the q286 raw-sum expansion ledger.

The preceding definition audit showed that the q286 adverse-envelope route is
only theorem-ready if the objects are stated directly as unnormalized raw sums.
This receipt records the earned raw expansion, labels the remaining logical
bridge, and keeps the q286/Q46189 adverse-alignment comparison in its proper
role: shared language, not merged proof.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RAW_CHARACTER = Path("evidence/q286-wbss-raw-character-expansion-target.json")
CIRCLE = Path("evidence/q286-wbss-raw-character-circle-decomposition.json")
RAW_WITNESS = Path("evidence/q286-wbss-raw-witness-identity-audit.json")
FOUR_MODULUS = Path("evidence/q286-wbss-four-modulus-projection-formula.json")
RAW_ADVERSE = Path("evidence/q286-wbss-raw-adverse-drag-theorem-target.json")
ZERO_MASS_L2 = Path("evidence/q286-wbss-zero-mass-l2-logical-bridge-audit.json")
RAWIZATION = Path("evidence/q286-wbss-rawization-obligation-audit.json")
UNIFICATION = Path("evidence/goldbach-adverse-alignment-unification-audit.json")
Q46189_MATRIX = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-source-matrix-margin-audit.json"
)

OUT = Path("evidence/q286-raw-sum-expansion-ledger.json")
NOTE = Path("notes/q286-raw-sum-expansion-ledger.md")


def load(path: Path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def summarize(values):
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": sum(values) / len(values),
    }


def build_receipt():
    raw_character = load(RAW_CHARACTER)
    circle = load(CIRCLE)
    raw_witness = load(RAW_WITNESS)
    four_modulus = load(FOUR_MODULUS)
    raw_adverse = load(RAW_ADVERSE)
    zero_mass_l2 = load(ZERO_MASS_L2)
    rawization = load(RAWIZATION)
    unification = load(UNIFICATION)
    q46189_matrix = load(Q46189_MATRIX)

    rows = raw_adverse["finite_calibration"]["rows"]
    adverse_ratios = [row["raw_adverse_drag_ratio"] for row in rows]
    gate_gaps = [row["raw_adverse_gate_gap"] for row in rows]

    raw_defs = raw_character["raw_character_definitions"]
    circle_ids = circle["exact_fourier_identities"]
    projection_formula = four_modulus["formula"]
    best_input = q46189_matrix[
        "best_feature_by_target"]["row_margin_above_failure"]
    best_matrix = q46189_matrix[
        "best_matrix_feature_by_target"]["row_margin_above_failure"]

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "LEDGER_q286_raw_sum_expansion",
        "source_receipts": {
            "raw_character_expansion_target": str(RAW_CHARACTER),
            "raw_character_circle_decomposition": str(CIRCLE),
            "raw_witness_identity_audit": str(RAW_WITNESS),
            "four_modulus_projection_formula": str(FOUR_MODULUS),
            "raw_adverse_drag_theorem_target": str(RAW_ADVERSE),
            "zero_mass_l2_logical_bridge_audit": str(ZERO_MASS_L2),
            "rawization_obligation_audit": str(RAWIZATION),
            "adverse_alignment_unification": str(UNIFICATION),
            "q46189_source_matrix_margin": str(Q46189_MATRIX),
        },
        "question": (
            "Can U_d(N), W_phi(N), and the q286 adverse envelope be written "
            "as direct raw sums with no mu_N notation, while preserving the "
            "zero-mass and L2 bridge boundaries?"),
        "raw_sum_ledger": {
            "strict_central_total_weight_T_N": {
                "formula": raw_defs["central_mass"],
                "classification": "raw_sum_unknown_support",
                "support_boundary": (
                    "If no strict-central prime pair exists, T_N=0.  The "
                    "ledger does not assume T_N>0."),
            },
            "raw_left_residue_mass_Pi_raw": {
                "formula": (
                    "Pi_raw_{N,d}(s)=sum_{N/3<p<2N/3, p and N-p prime, "
                    "p == s mod d} log(p)log(N-p)."),
                "classification": "raw_sum_by_residue",
                "source": "expanded from raw_projection_delta definition",
            },
            "local_uniform_projected_mass_U_a_d": {
                "formula": (
                    "U_{a,d}(s) is the local-uniform projected mass for "
                    "a=N mod 10010."),
                "classification": "local_factor_not_pair_support",
                "boundary": (
                    "This is a coefficient/local model term.  It may be "
                    "multiplied by T_N in a raw expression, but cannot create "
                    "strict-central support by itself."),
            },
            "raw_projection_delta": {
                "formula": raw_defs["raw_projection_delta"],
                "classification": "raw_discrepancy_vector",
            },
            "raw_character_moment": {
                "formula": raw_defs["raw_character_moment"],
                "circle_method_identity": circle_ids["raw_character_moment"],
                "classification": "raw_twisted_binary_prime_moment",
            },
            "raw_modulus_error_U_d": {
                "formula": (
                    "U_d(N)=E_raw_d(N)=sum_s alpha_{d,s}*"
                    "(Pi_raw_{N,d}(s)-T_N*U_{a,d}(s)); equivalently "
                    "E_raw_d(N)=sum_chi c_hat_{d,chi}*D_raw_{d,chi}(N)."),
                "classification": "theorem_ready_raw_sum",
                "boundary": (
                    "The notation U_d=T_N*E_d is allowed only as shorthand "
                    "after this direct raw discrepancy definition exists."),
            },
            "raw_local_main_L_raw": {
                "formula": raw_adverse["definitions"]["raw_local_main"],
                "classification": "raw_form_but_T_N_factor",
                "boundary": (
                    "L_raw vanishes when T_N=0.  It is a valid right-hand "
                    "side for a strict raw theorem, but not a separate "
                    "positive-mass theorem."),
            },
            "raw_witness_W_phi": {
                "direct_sum": (
                    "W_phi(N)=sum_{N/3<p<2N/3, p and N-p prime} "
                    "log(p)log(N-p)*phi_a(p mod 10010)."),
                "decomposition": raw_defs["raw_witness"],
                "circle_method_identity": circle_ids["raw_witness"],
                "classification": "direct_raw_witness_sum",
            },
            "raw_adverse_envelope_A_raw_minus": {
                "formula": raw_adverse["definitions"]["raw_adverse_drag"],
                "classification": "one_sided_raw_envelope_unproved",
            },
            "strict_raw_gap": {
                "formula": raw_defs["strict_raw_gap"],
                "classification": "noncircular_strict_target_unproved",
            },
        },
        "projection_formula_context": {
            "period": projection_formula["period"],
            "moduli": projection_formula["moduli"],
            "unit_coefficient_identity": projection_formula["identity"],
            "normalized_witness_formula": projection_formula[
                "normalized_witness"],
            "boundary": (
                "The normalized projection formula locates the coefficient "
                "span.  The theorem statement in this ledger uses the same "
                "coefficients inside raw sums."),
        },
        "logical_implication": {
            "adverse_drag_route": (
                "If A_raw_-(N)<L_raw(N), then sum_d U_d(N)>=-A_raw_-(N), "
                "so W_phi(N)=L_raw(N)+sum_d U_d(N)>0."),
            "raw_witness_route": rawization["corrected_theorem_paths"][
                "path_A_raw_witness"]["statement"],
            "zero_support_check": circle["zero_mass_check"],
            "noncircular_conclusion": (
                "At zero support, T_N=0, every Pi_raw, D_raw, U_d, "
                "A_raw_-, L_raw, and W_phi vanishes.  The strict inequalities "
                "therefore become false 0<0 or 0>0 statements; proving one "
                "would force strict-central support."),
        },
        "l2_bridge_status": {
            "raw_l2_statement": zero_mass_l2["coefficient_l2_target"][
                "raw_sufficient_statement"],
            "zero_mass_sanity_confirmed": zero_mass_l2[
                "l2_bridge_classification"][
                    "raw_strict_aggregate_l2_shape_is_noncircular"],
            "logical_bridge_confirmed": False,
            "reason": zero_mass_l2["decision"],
            "observed_l2_failures": zero_mass_l2["observed_l2_failures"],
            "classification": "target_only_not_acceptance_condition",
        },
        "finite_calibration_summary": {
            "row_count": len(rows),
            "raw_adverse_drag_ratio_summary": summarize(adverse_ratios),
            "raw_adverse_gate_gap_summary": summarize(gate_gaps),
            "all_checked_raw_gate_gaps_positive": all(
                gap > 0 for gap in gate_gaps),
            "finite_evidence_is_acceptance_condition": False,
        },
        "q286_q46189_bridge_read": {
            "shared_schema": unification["shared_schema"],
            "q286_role": (
                "proof-shaped raw adverse-envelope instantiation after this "
                "ledger, still missing the universal pointwise estimate"),
            "q46189_role": (
                "diagnostic/falsifier language for harmful source-block "
                "mass; not a proof input"),
            "q46189_best_input_feature": {
                "feature": best_input["feature"],
                "pearson": best_input["pearson"],
            },
            "q46189_best_matrix_feature": {
                "feature": best_matrix["feature"],
                "pearson": best_matrix["pearson"],
            },
            "combined_proof_established": False,
            "bridge_obligation": (
                "To combine them as mathematics rather than analogy, express "
                "Q46189 harmful source-block mass as raw projected-channel "
                "adverse mass plus a residual with a universal pointwise "
                "bound.  No such residual theorem is currently present."),
        },
        "acceptance_condition": {
            "required_universal_estimate": circle[
                "universal_pointwise_targets"]["acceptance_condition"],
            "acceptable_routes": [
                circle["universal_pointwise_targets"][
                    "adverse_drag_less_than_local_main"],
                circle["universal_pointwise_targets"][
                    "direct_signed_witness"],
                circle["universal_pointwise_targets"]["aggregate_L2_raw"],
            ],
            "invalid_substitutes": zero_mass_l2["acceptance_condition"][
                "invalid_substitutes"],
        },
        "decision": (
            "The q286 raw objects can now be stated as a direct raw-sum "
            "ledger with no mu_N notation in the theorem-ready statements.  "
            "This confirms the arithmetic decomposition and the zero-support "
            "non-circularity of the strict raw targets, but it does not prove "
            "the universal pointwise estimate.  The L2 target remains a raw "
            "candidate only, not a confirmed logical bridge.  Q46189 combines "
            "with q286 as adverse-alignment language, not as a theorem input "
            "until a residual bridge is proved."),
        "finite_ledger_only": True,
        "raw_sum_definitions_confirmed": True,
        "l2_logical_bridge_confirmed": False,
        "q286_q46189_combined_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "raw_adverse_envelope_theorem_proved": False,
        "raw_witness_theorem_proved": False,
        "universal_raw_pointwise_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    calib = receipt["finite_calibration_summary"]
    ratio = calib["raw_adverse_drag_ratio_summary"]
    gap = calib["raw_adverse_gate_gap_summary"]
    bridge = receipt["q286_q46189_bridge_read"]
    lines = [
        "# q286 raw-sum expansion ledger",
        "",
        "## Question",
        "",
        receipt["question"],
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_q286_raw_sum_expansion_ledger.py",
        "evidence/q286-raw-sum-expansion-ledger.json",
        "```",
        "",
        "## Raw Ledger",
        "",
        "The theorem-ready q286 route can be written without `mu_N`:",
        "",
        "```text",
        "T_N = sum_{N/3<p<2N/3, p and N-p prime} log(p)log(N-p)",
        "Pi_raw_{N,d}(s) = sum over the same pairs with p == s mod d",
        "U_d(N) = sum_s alpha_{d,s}(Pi_raw_{N,d}(s)-T_N U_{a,d}(s))",
        "L_raw(N) = T_N M(a)",
        "A_raw_-(N) = sum_d max(0,-U_d(N))",
        "W_phi(N) = L_raw(N)+sum_d U_d(N)",
        "```",
        "",
        "Equivalently, the character expansion uses",
        "",
        "```text",
        "D_raw_{d,chi}(N)=C_{d,chi}(N)-U_{a,d,chi} C_0(N)",
        "U_d(N)=E_raw_d(N)=sum_chi c_hat_{d,chi}D_raw_{d,chi}(N).",
        "```",
        "",
        "The direct witness is the unnormalized signed log-pair sum",
        "`W_phi(N)=sum log(p)log(N-p) phi_a(p mod 10010)` over strict-central",
        "prime pairs.",
        "",
        "## Zero-Mass Boundary",
        "",
        "If no strict-central pair exists, then every raw sum above vanishes.",
        "Thus the strict targets `A_raw_-(N)<L_raw(N)`, the aggregate raw L2",
        "target, and `W_phi(N)>0` all fail at zero support.  A proof of one",
        "of those strict raw statements would therefore create support.",
        "",
        "## L2 Status",
        "",
        "The L2 target is non-circular as a strict raw shape, but it is not",
        "confirmed as a logical bridge.  The existing zero-mass check is an",
        "arithmetic sanity check, not a pointwise theorem.",
        "",
        "## Finite Calibration",
        "",
        "```text",
        f"rows:                              {calib['row_count']}",
        f"max raw adverse ratio:             {ratio['maximum']}",
        f"min raw adverse gate gap:          {gap['minimum']}",
        f"all checked raw gaps positive:     {calib['all_checked_raw_gate_gaps_positive']}",
        "finite evidence is acceptance:     false",
        "```",
        "",
        "## q286 / Q46189 Bridge Read",
        "",
        "q286 and Q46189 remain compatible as adverse-alignment language: bad",
        "mass must not coherently align across all available channels.  They",
        "are not yet a merged theorem.  Q46189 would need a residual bridge:",
        "harmful source-block mass expressed as raw q286-style adverse mass",
        "plus a universally bounded residual.",
        "",
        f"Best Q46189 input feature remains `{bridge['q46189_best_input_feature']['feature']}`",
        f"with Pearson `{bridge['q46189_best_input_feature']['pearson']}`.",
        f"Best genuine matrix feature remains `{bridge['q46189_best_matrix_feature']['feature']}`",
        f"with Pearson `{bridge['q46189_best_matrix_feature']['pearson']}`.",
        "",
        "## Decision",
        "",
        receipt["decision"],
        "",
        "This proves no L2 bridge, q286/Q46189 combined theorem, raw adverse-",
        "envelope theorem, raw witness theorem, strict-central Goldbach theorem,",
        "or Goldbach proof.",
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
        "raw_sum_definitions_confirmed": (
            receipt["raw_sum_definitions_confirmed"]),
        "l2_logical_bridge_confirmed": (
            receipt["l2_logical_bridge_confirmed"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
