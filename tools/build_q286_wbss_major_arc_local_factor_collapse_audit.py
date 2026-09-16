"""Audit the q286 signed-weight major-arc local-factor shape.

The signed-weight circle target asks whether q286 supplies a raw positive
major-arc term before ordinary strict-central mass is known.  This receipt
records the symbolic local-factor decomposition forced by the existing finite
coefficient audits.

It is not a circle-method estimate.  It proves no pointwise prime-correlation
bound, no positive-mass theorem, no q286 threshold theorem, and no Goldbach
proof.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SIGNED_TARGET = EVIDENCE / "q286-wbss-signed-weight-circle-target.json"
LOCAL_MAIN = EVIDENCE / "q286-local-main-term-positivity-audit.json"
CENTERED_BURDEN = EVIDENCE / "q286-centered-character-burden-audit.json"
SINGLE_FLOOR = EVIDENCE / "q286-wbss-single-weight-major-arc-floor-audit.json"
OUT = EVIDENCE / "q286-wbss-major-arc-local-factor-collapse-audit.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dominant_supports(centered):
    rows = centered["dominant_99_percent_energy_support_rows"]
    return [
        {
            "support_label": row["support_label"],
            "natural_modulus": row["natural_modulus"],
            "energy_fraction": row["energy_fraction"],
            "character_count": row["character_count"],
        }
        for row in rows
    ]


def build_receipt():
    target = load_json(SIGNED_TARGET)
    local = load_json(LOCAL_MAIN)
    centered = load_json(CENTERED_BURDEN)
    floor = load_json(SINGLE_FLOOR)
    local_ratio = local["local_main_term_to_principal_ratio_summary"]
    floor_summary = floor["target_residue_summary"]

    return {
        "schema_version": 1,
        "receipt": "q286-wbss-major-arc-local-factor-collapse-audit",
        "source_commit": source_commit(),
        "sources": {
            "signed_weight_circle_target": str(
                SIGNED_TARGET.relative_to(ROOT)),
            "signed_weight_circle_status": target["status"],
            "local_main_term_positivity_audit": str(
                LOCAL_MAIN.relative_to(ROOT)),
            "centered_character_burden_audit": str(
                CENTERED_BURDEN.relative_to(ROOT)),
            "single_weight_major_arc_floor_audit": str(
                SINGLE_FLOOR.relative_to(ROOT)),
            "single_weight_floor_status": floor["status"],
        },
        "status": (
            "LOCAL_FACTOR_principal_term_is_T_N_dependent_"
            "centered_error_open"),
        "question": (
            "Does the q286 signed weight produce an independent raw "
            "major-arc surplus, or does its principal local factor depend on "
            "ordinary strict-central binary-prime mass?"),
        "short_answer": (
            "No independent q286 source term was found in the symbolic local "
            "factor.  The coefficient-side principal term is a positive "
            "local factor m_a times the ordinary strict-central raw mass "
            "T_N, plus a centered signed-correlation error.  This keeps a "
            "raw circle-method route alive only if the same proof also "
            "creates the ordinary binary-prime main term and bounds the "
            "centered error pointwise."),
        "exact_local_factor_decomposition": {
            "admissible_support": (
                "A_a={u in U_10010: gcd(a-u,10010)=1}, a=N mod 10010."),
            "raw_residue_weights": (
                "W_N(u)=sum_{p in I_N, p==u mod 10010, N-p prime} "
                "log(p)log(N-p)."),
            "total_mass": "T_N=sum_{u in A_a} W_N(u).",
            "local_mean": "m_a=|A_a|^-1 sum_{u in A_a} Phi_a(u).",
            "centered_weight": "Phi_a^0(u)=Phi_a(u)-m_a.",
            "identity": (
                "W_phi(N)=m_a*T_N + "
                "sum_{u in A_a}(W_N(u)-T_N/|A_a|)*Phi_a^0(u)."),
            "zero_mass_behavior": (
                "If T_N=0, both the principal term and centered term vanish, "
                "so W_phi(N)=0."),
        },
        "local_factor_evidence": {
            "even_target_residue_count": local["even_target_residue_count"],
            "all_local_means_positive": local[
                "all_even_residue_local_main_terms_positive"],
            "nonpositive_local_main_term_count": local[
                "nonpositive_local_main_term_count"],
            "local_mean_ratio_minimum": local_ratio["minimum"],
            "local_mean_ratio_maximum": local_ratio["maximum"],
            "local_mean_ratio_mean": local_ratio["mean"],
            "weakest_target_residue": local[
                "minimum_local_ratio_row"]["target_residue"],
            "strongest_target_residue": local[
                "maximum_local_ratio_row"]["target_residue"],
        },
        "centered_error_burden": {
            "nonzero_natural_moduli": centered["nonzero_natural_moduli"],
            "full_modulus_10010_support_present": centered[
                "full_modulus_10010_support_present"],
            "all_nonzero_supports_descend_to_lower_moduli": centered[
                "all_nonzero_supports_descend_to_lower_moduli"],
            "dominant_99_percent_energy_fraction": centered[
                "dominant_99_percent_energy_fraction"],
            "dominant_supports": dominant_supports(centered),
            "top_three_support_energy_fraction": centered[
                "top_three_support_energy_fraction"],
        },
        "sign_indefiniteness_guard": {
            "single_weight_floor_status": floor["status"],
            "rows_with_negative_admissible_weight": floor_summary[
                "rows_with_negative_admissible_weight"],
            "rows_with_pointwise_positive_floor": floor_summary[
                "rows_with_pointwise_positive_floor"],
            "negative_weight_fraction_maximum": floor_summary[
                "negative_weight_fraction_summary"]["maximum"],
            "meaning": (
                "The positive local factor is not a coefficientwise "
                "minorant.  It cannot turn arbitrary support or arbitrary "
                "nonnegative residue mass into W_phi(N)>0."),
        },
        "major_arc_classifier": {
            "principal_term_shape": (
                "q286 principal local factor = m_a times the ordinary "
                "strict-central binary-prime principal mass for the same "
                "target residue."),
            "independent_q286_source_term_found": False,
            "survives_if": (
                "A raw major/minor arc proof establishes "
                "m_a*Main_0(N)+CenteredMain_a(N)+Error_a(N)>0 pointwise for "
                "every sufficiently large covered N, with the ordinary "
                "binary-prime main term and centered-error bound proved "
                "inside that same argument."),
            "collapses_if": (
                "The proof first imports or assumes T_N>0 or an ordinary "
                "strict-central Goldbach theorem, then uses q286 only to "
                "control conditional landing or normalized discrepancy."),
            "what_changed": (
                "The next bridge is no longer 'find a q286 positive main "
                "term'.  It is 'prove the centered lower-modulus signed "
                "correlations are smaller than the positive local factor in "
                "a raw pointwise circle-method estimate'."),
        },
        "candidate": {
            "name": "q286 local-factor centered-error bridge",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Split the signed weight into its positive admissible local "
                "mean and a centered lower-modulus character burden."),
            "prediction": (
                "If this route can work, the dominant centered supports "
                "286, 154, and 70 admit pointwise signed binary-prime "
                "correlation bounds below the weakest local factor ratio "
                "0.6039353780830684 after the tail is included."),
            "falsifier": (
                "A centered component or tail with unavoidable pointwise "
                "negative contribution below -m_a for infinitely many "
                "covered N would kill this coefficient as a proof engine."),
            "smallest_next_test": (
                "Build a symbolic centered-support inequality ledger: per "
                "modulus 286, 154, 70, and tail, state the exact pointwise "
                "correlation bound needed to keep the sum above -m_a."),
        },
        "decision": (
            "LOCAL_FACTOR_principal_term_is_T_N_dependent_centered_error_"
            "open.  The local factor audit confirms positive coefficient "
            "means on all 5005 even target residues, with ratios "
            "0.6039353780830684..1.5716524655081636.  But the principal "
            "term is m_a times ordinary strict-central binary-prime mass, "
            "not an independent q286 source term.  Because the coefficient "
            "is sign-indefinite on every target support, the route needs a "
            "raw pointwise centered-error/correlation theorem; otherwise it "
            "collapses to ordinary T_N>0 plus conditional q286 decoration."),
        "status_boundary": (
            "Symbolic local-factor decomposition and collapse classifier "
            "only; this is not a theorem.  No major/minor arc estimate, "
            "pointwise centered-error estimate, signed prime-correlation "
            "theorem, positive-mass theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof is "
            "established."),
        "goldbach_proved": False,
        "major_minor_arc_estimate_proved": False,
        "pointwise_centered_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "positive_mass_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "universal_pointwise_bound_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "independent_q286_source_term_found": (
            receipt["major_arc_classifier"][
                "independent_q286_source_term_found"]),
        "local_mean_ratio_minimum": (
            receipt["local_factor_evidence"]["local_mean_ratio_minimum"]),
        "dominant_99_percent_energy_fraction": (
            receipt["centered_error_burden"][
                "dominant_99_percent_energy_fraction"]),
        "major_minor_arc_estimate_proved": (
            receipt["major_minor_arc_estimate_proved"]),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
