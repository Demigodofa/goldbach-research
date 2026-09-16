"""Build the character-expanded K_286 theorem target.

The centered-support source-fit audit left a precise next bridge: expand the
dominant_286 bucket into its natural modulus 286 character package and state
the raw pointwise lower bound an analytic proof would have to establish.

This receipt is a theorem target only.  It proves no character-moment estimate,
no centered-error estimate, no q286 threshold theorem, and no Goldbach theorem.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
LEDGER = EVIDENCE / "q286-wbss-centered-support-inequality-ledger.json"
CHARACTER_BURDEN = EVIDENCE / "q286-centered-character-burden-audit.json"
SOURCE_FIT = EVIDENCE / "q286-wbss-centered-support-source-fit-audit.json"
RAW_DECOMPOSITION = (
    EVIDENCE / "q286-wbss-raw-character-circle-decomposition.json")
OUT = EVIDENCE / "q286-wbss-k286-character-expansion-target.json"

BUCKET = "dominant_286"
SUPPORT_LABEL = "11x13"
NATURAL_MODULUS = 286


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def select_ledger_bucket(ledger):
    return next(
        row for row in ledger["bucket_obligations"]
        if row["bucket"] == BUCKET)


def select_support_row(character_burden):
    return next(
        row for row in character_burden["support_rows"]
        if row["support_label"] == SUPPORT_LABEL)


def build_receipt():
    ledger = load_json(LEDGER)
    character_burden = load_json(CHARACTER_BURDEN)
    source_fit = load_json(SOURCE_FIT)
    raw = load_json(RAW_DECOMPOSITION)
    bucket = select_ledger_bucket(ledger)
    support = select_support_row(character_burden)

    beta = bucket["allocated_negative_budget_ratio"]
    required_bound = f"K_286(N) >= -{beta}*P0_a(N)"

    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-character-expansion-target",
        "source_commit": source_commit(),
        "sources": {
            "centered_support_inequality_ledger": str(
                LEDGER.relative_to(ROOT)),
            "centered_support_inequality_ledger_status": ledger["status"],
            "centered_character_burden_audit": str(
                CHARACTER_BURDEN.relative_to(ROOT)),
            "centered_support_source_fit_audit": str(
                SOURCE_FIT.relative_to(ROOT)),
            "centered_support_source_fit_status": source_fit["status"],
            "raw_character_circle_decomposition": str(
                RAW_DECOMPOSITION.relative_to(ROOT)),
            "raw_character_circle_decomposition_status": raw["status"],
        },
        "status": "TARGET_k286_character_expansion_bridge_unproved",
        "question": (
            "What exact character-expanded theorem target would pay the "
            "dominant_286 centered-support bucket obligation?"),
        "answer": (
            "The dominant_286 bucket is the support-11x13 part of the fixed "
            "centered coefficient.  It descends to natural modulus 286 and "
            "is spanned by 99 nonprincipal characters whose 11 and 13 "
            "components are both nontrivial.  A proof must show a raw "
            "pointwise lower bound K_286(N) >= -beta_286*P0_a(N) for every "
            "sufficiently large covered even N, before normalizing by actual "
            "strict-central mass T_N."),
        "target_bucket": {
            "bucket": BUCKET,
            "support_label": SUPPORT_LABEL,
            "natural_modulus": NATURAL_MODULUS,
            "support_primes": support["support"],
            "character_count": support["character_count"],
            "unit_residue_count": support["unit_residue_count"],
            "energy_fraction": support["energy_fraction"],
            "descent_relative_error": support["descent_relative_error"],
            "descends_to_natural_modulus": (
                support["descends_to_natural_modulus"]),
            "allocated_negative_budget_ratio": beta,
            "required_raw_lower_bound": required_bound,
        },
        "character_set": {
            "notation": (
                "X_286(11x13)={chi modulo 286: chi is trivial on the "
                "factor 2, nontrivial on 11, and nontrivial on 13}."),
            "count_formula": "(11-2)*(13-2)=99.",
            "principal_character_included": False,
            "why_nonprincipal": (
                "The 11x13 support label excludes the all-zero character "
                "label.  The principal term belongs to the ordinary local "
                "main, not to K_286."),
        },
        "finite_coefficient_package": {
            "coefficient_symbol": "c_{a,chi}^{286}",
            "coefficient_origin": (
                "finite projection of the fixed centered q286-WBSS "
                "coefficient onto X_286(11x13), inherited from the centered "
                "character burden audit"),
            "support_component": (
                "Phi_{286,a}(r)=sum_{chi in X_286(11x13)} "
                "c_{a,chi}^{286} chi(r), for r in U_286."),
            "coefficient_reconstruction": (
                "The finite component descends to residues modulo 286 with "
                "relative descent error 8.520857820502405e-17."),
            "local_contribution_to_principal_ratio_summary": (
                support["local_contribution_to_principal_ratio_summary"]),
            "removing_component_minimum_full_local_ratio": (
                support["removing_component_minimum_full_local_ratio"]),
        },
        "raw_moments": {
            "strict_central_interval": "I_N={n integer: N/3<n<2N/3}.",
            "prime_log_weight": (
                "P(n)=log(n) if n is prime, and P(n)=0 otherwise."),
            "untwisted_mass": (
                "C_0(N)=sum_{p in I_N, N-p prime} log(p)log(N-p)."),
            "twisted_pair_mass": (
                "C_chi(N)=sum_{p in I_N, N-p prime} "
                "log(p)log(N-p)chi(p mod 286)."),
            "local_uniform_character_mean": (
                "U_{a,chi}^{286}=|A_a|^{-1} sum_{r in A_a} "
                "chi(r mod 286), where a=N mod 10010 and A_a is the "
                "strict-central admissible unit support projected to 286."),
            "actual_centered_moment": (
                "D_chi^T(N)=C_chi(N)-U_{a,chi}^{286}*C_0(N)."),
            "proof_scale_moment": (
                "D_chi^P(N)=C_chi(N)-U_{a,chi}^{286}*P0_a(N)."),
            "bucket_sum": (
                "K_286(N)=sum_{chi in X_286(11x13)} "
                "c_{a,chi}^{286} D_chi^P(N)."),
        },
        "principal_and_nonprincipal_terms": {
            "centered_bucket_principal_term_found": False,
            "principal_term_status": (
                "No standalone positive principal term lives in K_286.  "
                "The positive principal/local main is outside this bucket; "
                "K_286 is an adverse or helpful nonprincipal correction "
                "against that main."),
            "nonprincipal_terms_to_control": 99,
            "P0_scale_warning": (
                "Using P0_a(N) rather than actual C_0(N) is a proof-scale "
                "target.  A circle-method proof must create P0_a(N) and "
                "control the C_0(N)-P0_a(N) mismatch inside the same raw "
                "argument; it is not allowed to divide by or assume T_N>0 "
                "first."),
        },
        "theorem_obligation": {
            "quantifier": "every sufficiently large covered even N",
            "target_residue_parameter": "a=N mod 10010",
            "required_pointwise_inequality": required_bound,
            "sufficient_role_in_ledger": (
                "This pays only the dominant_286 bucket.  The ledger still "
                "also needs dominant_154, dominant_70, and tail lower "
                "bounds, or a sharper combined inequality."),
            "finite_remainder": (
                "Any analytic theorem must state an explicit N0 and pair "
                "with finite verification below N0."),
        },
        "zero_mass_and_collapse_check": {
            "if_T_N_is_zero": (
                "C_0(N)=0 and every C_chi(N)=0, so the actual centered "
                "moments D_chi^T(N) vanish.  The proof-scale target cannot "
                "be certified by normalized distribution data at zero mass."),
            "L2_status": (
                "The L2 target is not confirmed as a logical bridge.  It is "
                "a possible sufficient raw estimate only if proved "
                "pointwise before importing T_N>0."),
            "collapses_if": (
                "A route first proves or assumes T_N>0 and then studies the "
                "normalized residue distribution.  That is strict-central "
                "Goldbach-strength input plus q286 decoration."),
            "survives_if": (
                "A raw major/minor arc proof establishes K_286(N) above the "
                "allocated negative budget, or a stronger combined "
                "adverse-drag inequality, without first assuming T_N>0."),
        },
        "candidate": {
            "name": "dominant_286 character-expanded raw bucket target",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Turn the largest centered support into 99 fixed-modulus "
                "twisted binary-prime sums at natural modulus 286, making "
                "the analytic burden exact enough to accept, reject, or "
                "sharpen."),
            "prediction": (
                "If the q286 route is real, the combined 11x13 character "
                "package should admit a pointwise one-sided lower bound "
                "below 0.1759037368828583 of the ordinary principal scale."),
            "falsifier": (
                "A theorem obstruction or computed counterfamily showing "
                "K_286(N)<-0.1759037368828583*P0_a(N) infinitely often "
                "would falsify this sufficient bucket target."),
            "smallest_next_test": (
                "Compute or symbolically package the 99 coefficients "
                "c_{a,chi}^{286} and ask whether known fixed-modulus "
                "twisted Goldbach estimates can control their weighted sum "
                "pointwise."),
        },
        "decision": (
            "TARGET_k286_character_expansion_bridge_unproved.  The "
            "dominant_286 theorem target is now explicit: prove the "
            "99-character modulus-286 raw lower bound "
            f"{required_bound} for every sufficiently large covered even N.  "
            "This is a nonfinite, pointwise, unnormalized analytic "
            "obligation; the present artifact proves no such estimate and "
            "does not confirm L2 as a logical bridge."),
        "status_boundary": (
            "Theorem-target receipt only; not a theorem.  No K_286 lower "
            "bound, major/minor arc estimate, pointwise centered-error "
            "estimate, signed prime-correlation theorem, q286 threshold "
            "theorem, strict-central Goldbach theorem, or Goldbach proof is "
            "established."),
        "goldbach_proved": False,
        "k286_pointwise_lower_bound_proved": False,
        "major_minor_arc_estimate_proved": False,
        "pointwise_centered_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "universal_pointwise_bound_proved": False,
        "L2_logical_bridge_confirmed": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "bucket": receipt["target_bucket"]["bucket"],
        "support_label": receipt["target_bucket"]["support_label"],
        "natural_modulus": receipt["target_bucket"]["natural_modulus"],
        "character_count": receipt["target_bucket"]["character_count"],
        "required_raw_lower_bound": (
            receipt["target_bucket"]["required_raw_lower_bound"]),
        "L2_logical_bridge_confirmed": (
            receipt["L2_logical_bridge_confirmed"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
