"""Build the raw character circle-method decomposition checkpoint.

This receipt answers Kevin's zero-mass/logical-bridge question for the q286
raw-character target.  It records the exact Fourier decomposition to attack,
then classifies what would be a genuine non-circular proof versus a collapse
to an already-Goldbach-strength positive-mass input.

No circle-method estimate, raw character moment theorem, strict raw-gap
theorem, strict-central Goldbach theorem, or Goldbach proof is established.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
RAW_TARGET = EVIDENCE / "q286-wbss-raw-character-expansion-target.json"
OUT = EVIDENCE / "q286-wbss-raw-character-circle-decomposition.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    raw = load_json(RAW_TARGET)
    package = raw["coefficient_package"]
    finite = raw["finite_diagnostic_boundary"]

    return {
        "schema_version": 1,
        "receipt": "q286-wbss-raw-character-circle-decomposition",
        "source_commit": source_commit(),
        "sources": {
            "raw_character_expansion_target": str(
                RAW_TARGET.relative_to(ROOT)),
            "raw_character_expansion_status": raw["status"],
        },
        "status": (
            "TARGET_raw_character_circle_method_decomposition_"
            "bridge_unproved"),
        "question": (
            "Can the raw q286-WBSS character target be written as an exact "
            "circle-method object whose strict positivity would be genuinely "
            "non-circular, and what collapses the route?"),
        "answer": (
            "Yes as a precise theorem target.  The raw moments are exact "
            "strict-central prime-pair Fourier coefficients.  But this is "
            "only a logical decomposition: no major/minor arc estimate has "
            "been proved.  The route survives only if strict positivity is "
            "proved directly for the raw witness or raw adverse-drag gap.  "
            "If the proof first assumes or separately proves T_N>0 and only "
            "then controls normalized character/L2 error, the q286 mechanism "
            "has not reduced the Goldbach-strength core."),
        "notation": {
            "e_alpha": "e(alpha*x)=exp(2*pi*i*alpha*x).",
            "strict_central_interval": "I_N={n integer: N/3<n<2N/3}.",
            "prime_log_weight": (
                "P(n)=log(n) if n is prime, and P(n)=0 otherwise.  This "
                "uses prime-only weights, not Lambda, so no prime-power "
                "correction is hidden in the identity."),
            "large_N_unit_condition": (
                "For N>3*286, every strict-central prime p>N/3 is coprime "
                "to d in {70,130,154,286}; smaller exceptions belong to the "
                "finite check below an explicit threshold."),
        },
        "exact_fourier_identities": {
            "untwisted_sum": (
                "P_N(alpha)=sum_{n in I_N} P(n)*e(alpha*n)."),
            "twisted_left_sum": (
                "P_{d,chi,N}(alpha)=sum_{n in I_N} "
                "P(n)*chi_d(n)*e(alpha*n)."),
            "central_mass": (
                "C_0(N)=int_0^1 P_N(alpha)*P_N(alpha)*e(-alpha*N)dalpha "
                "= T_N."),
            "twisted_pair_mass": (
                "C_{d,chi}(N)=int_0^1 "
                "P_{d,chi,N}(alpha)*P_N(alpha)*e(-alpha*N)dalpha "
                "= sum_{p in I_N, N-p prime} "
                "log(p)log(N-p)chi_d(p)."),
            "uniform_character_projection": (
                "U_{a,d,chi}=sum_s chi_d(s)*U_{a,d}(s), where "
                "a=N mod 10010 and U_{a,d} is the local-uniform projected "
                "mass from the raw target."),
            "raw_character_moment": (
                "D_raw_{d,chi}(N)=C_{d,chi}(N)-U_{a,d,chi}*C_0(N)."),
            "modulus_error": (
                "E_raw_d(N)=sum_chi c_hat_{d,chi}*D_raw_{d,chi}(N)."),
            "raw_witness": (
                "W_phi(N)=C_0(N)*M(a)+sum_{d,chi} "
                "c_hat_{d,chi}*(C_{d,chi}(N)-U_{a,d,chi}*C_0(N))."),
            "single_weight_form": (
                "W_phi(N)=int_0^1 Q_{a,N}(alpha)*P_N(alpha)"
                "*e(-alpha*N)dalpha, with "
                "Q_{a,N}(alpha)=sum_{n in I_N}P(n)*"
                "[M(a)+sum_{d,chi}c_hat_{d,chi}"
                "*(chi_d(n)-U_{a,d,chi})]*e(alpha*n)."),
        },
        "major_minor_arc_obligation": {
            "major_arc_task": (
                "Show the major arcs produce a positive main term for the "
                "actual single-weight witness W_phi(N), or for "
                "T_N*M(a) minus a proved adverse-drag envelope, with all "
                "local factors and strict-central truncation included."),
            "minor_arc_task": (
                "Bound the complementary arcs pointwise for every covered "
                "even N>=N0 strongly enough that they cannot erase the "
                "positive major-arc contribution."),
            "finite_remainder_task": (
                "Give an explicit N0 and verify the finite remainder below "
                "N0.  Finite q286 windows alone are diagnostics, not the "
                "acceptance condition."),
            "no_division_by_T_N_rule": (
                "A proof of strict positivity must not divide by T_N or use "
                "a normalized distribution ratio until strict-central mass "
                "has already been created inside the same argument or "
                "imported as an explicitly Goldbach-strength theorem."),
        },
        "zero_mass_check": {
            "if_T_N_is_zero": (
                "There are no strict-central prime pairs, so C_0(N)=0 and "
                "C_{d,chi}(N)=0 for every active character.  Therefore "
                "D_raw_{d,chi}(N)=0, E_raw_d(N)=0, W_phi(N)=0, and "
                "G_raw(N)=0."),
            "strict_L2_target_at_zero_mass": (
                "C2*sqrt(sum|D_raw|^2)<T_N*M(a) becomes 0<0, which is "
                "false."),
            "strict_witness_at_zero_mass": (
                "W_phi(N)>0 is false because W_phi(N)=0."),
            "conclusion": (
                "The raw strict targets are non-circular theorem shapes: if "
                "proved for all sufficiently large covered N, they force "
                "strict-central prime-pair support.  They are not confirmed "
                "by the present arithmetic decomposition."),
        },
        "universal_pointwise_targets": {
            "adverse_drag_less_than_local_main": (
                "For every covered even N>=N0, prove "
                "sum_d max(0,-E_raw_d(N)) < T_N*M(a), or prove a sharper "
                "component/signed envelope that implies it."),
            "aggregate_L2_raw": (
                raw["sufficient_raw_theorem_shapes"]["aggregate_L2"][
                    "statement"]),
            "direct_signed_witness": (
                raw["sufficient_raw_theorem_shapes"]["direct_signed_sum"][
                    "statement"]),
            "acceptance_condition": (
                "A universal, pointwise, unnormalized analytical estimate for "
                "every sufficiently large covered N, such as "
                "adverse_drag_raw(N)<local_main_raw(N), plus an explicit "
                "finite remainder.  Finite evidence is not an acceptance "
                "condition."),
        },
        "collapse_classifier": {
            "survives_as_q286_proof_engine_if": (
                "The same circle-method argument proves W_phi(N)>0, "
                "G_raw(N)>0, or adverse_drag_raw(N)<local_main_raw(N) "
                "without first assuming pointwise T_N>0."),
            "collapses_if": (
                "The proof first establishes or assumes T_N>0 for every "
                "sufficiently large N, and then applies q286 only as a "
                "conditional distribution or normalized L2 estimate."),
            "sleep_decision_if_collapsed": (
                "If all available analytic routes need T_N>0 before q286 has "
                "content, sleep q286 as a proof engine and preserve it as "
                "coefficient/visual structure for finding a sharper signed "
                "major-arc weight."),
            "logical_bridge_status": (
                "Arithmetic decomposition confirmed; logical bridge not "
                "proved.  L2 is a target, not an accepted bridge."),
        },
        "visualization_candidate": {
            "role": (
                "Exploratory only.  A linked 3D scatter/table may help notice "
                "structure, but visual clusters cannot replace the universal "
                "pointwise estimate."),
            "x_axis": "log(N).",
            "y_axis": (
                "A genuinely ordered analytic quantity, such as local main, "
                "driver margin, or normalized/raw moment size; not a residue "
                "label treated as numeric."),
            "z_axis": "Strict closure margin or adverse-drag margin.",
            "color": "Conductor, modulus family, or residue class.",
            "brightness": "Distance from failure.",
            "animation": "Successive N-windows or modulus/character changes.",
            "linked_table_payload": (
                "Exact N, residues, active channels, C_0, C_{d,chi}, "
                "D_raw, E_raw_d, local main, adverse drag, and coefficients."),
        },
        "inherited_numbers": {
            "active_complex_character_count": (
                package["active_complex_character_count"]),
            "active_real_channel_count": (
                package["active_real_channel_count"]),
            "aggregate_character_l2": package["aggregate_character_l2"],
            "aggregate_character_moment_l2_cap_normalized": (
                package["aggregate_character_moment_l2_cap_normalized"]),
            "observed_l2_row_count": finite["observed_l2_row_count"],
            "observed_row_local_l2_cap_violations": (
                finite["observed_row_local_l2_cap_violations"]),
            "observed_global_min_l2_cap_violations": (
                finite["observed_global_min_l2_cap_violations"]),
        },
        "candidate": {
            "name": "raw q286 single-weight circle-method witness",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Combine the q286 coefficients before integration so the "
                "proof target is one signed strict-central binary-prime "
                "convolution, not post-support normalized residue statistics."),
            "prediction": (
                "If q286 helps, the combined left-prime weight has a local "
                "major-arc surplus or an adverse-drag envelope smaller than "
                "the principal local main."),
            "falsifier": (
                "If the combined major term is only T_N times a positive "
                "constant and all error control is conditional on T_N>0, the "
                "route has not reduced the existence problem."),
            "smallest_next_test": (
                "Compute the finite single-weight coefficients by residue and "
                "check whether their average local major-arc factors suggest "
                "a positive singular-series target or only a T_N-dependent "
                "renormalization."),
        },
        "decision": (
            "TARGET_raw_character_circle_method_decomposition_bridge_"
            "unproved.  The raw q286 target is non-circular as a strict "
            "unnormalized theorem shape, because zero mass makes the strict "
            "inequalities false.  That does not confirm the L2 target or the "
            "logical bridge.  The needed result is a universal pointwise "
            "analytic estimate, such as adverse_drag_raw(N)<local_main_raw(N) "
            "or W_phi(N)>0, for every sufficiently large covered N.  A proof "
            "that first imports pointwise T_N>0 collapses to strict-central "
            "Goldbach-strength input plus q286 decoration."),
        "status_boundary": (
            "Circle-method decomposition and collapse classifier only; no "
            "major/minor arc estimate, raw character moment theorem, "
            "adverse-drag theorem, strict raw-gap theorem, positive-mass "
            "theorem, q286 threshold theorem, strict-central Goldbach theorem, "
            "or Goldbach proof is established."),
        "goldbach_proved": False,
        "circle_method_estimate_proved": False,
        "raw_character_moment_theorem_proved": False,
        "adverse_drag_theorem_proved": False,
        "strict_raw_gap_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "universal_pointwise_bound_proved": False,
        "finite_evidence_acceptance_condition": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "active_complex_character_count": (
            receipt["inherited_numbers"][
                "active_complex_character_count"]),
        "aggregate_character_l2": (
            receipt["inherited_numbers"]["aggregate_character_l2"]),
        "logical_bridge_status": (
            receipt["collapse_classifier"]["logical_bridge_status"]),
        "universal_pointwise_bound_proved": (
            receipt["universal_pointwise_bound_proved"]),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
