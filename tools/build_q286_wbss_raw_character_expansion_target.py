"""Build the exact raw character-expanded q286-WBSS theorem target.

The source-theorem fit audit left one useful next move: write the exact raw
character-expanded theorem target before trying another finite scan.  This
receipt records the target and its collapse/sleep test.  It proves no character
moment theorem and no Goldbach theorem.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE_FIT = EVIDENCE / "q286-wbss-source-theorem-fit-audit.json"
STRICT_HOLD = EVIDENCE / "q286-wbss-strict-raw-gap-analytic-hold.json"
CHAR_PAYMENT = EVIDENCE / "q286-wbss-multiplicative-character-payment-audit.json"
CHAR_L2_PAYMENT = (
    EVIDENCE / "q286-wbss-multiplicative-character-l2-payment-audit.json")
OBSERVED_L2 = (
    EVIDENCE
    / "q286-wbss-multiplicative-character-l2-observed-moment-audit.json")
OUT = EVIDENCE / "q286-wbss-raw-character-expansion-target.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    source_fit = load_json(SOURCE_FIT)
    strict_hold = load_json(STRICT_HOLD)
    char_payment = load_json(CHAR_PAYMENT)
    char_l2 = load_json(CHAR_L2_PAYMENT)
    observed = load_json(OBSERVED_L2)

    char_budget = char_payment["character_budget"]
    l2_budget = char_l2["character_l2_budget"]
    observed_summary = observed["summary"]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "source_theorem_fit_audit": str(SOURCE_FIT.relative_to(ROOT)),
            "source_theorem_fit_status": source_fit["status"],
            "strict_raw_gap_analytic_hold": str(
                STRICT_HOLD.relative_to(ROOT)),
            "strict_raw_gap_analytic_hold_status": strict_hold["status"],
            "multiplicative_character_payment_audit": str(
                CHAR_PAYMENT.relative_to(ROOT)),
            "multiplicative_character_payment_status": char_payment[
                "status"],
            "multiplicative_character_l2_payment_audit": str(
                CHAR_L2_PAYMENT.relative_to(ROOT)),
            "multiplicative_character_l2_payment_status": char_l2["status"],
            "observed_l2_moment_audit": str(OBSERVED_L2.relative_to(ROOT)),
            "observed_l2_moment_status": observed["status"],
        },
        "status": "TARGET_raw_character_expanded_q286_WBSS_theorem",
        "status_boundary": (
            "raw character-expanded theorem target only; no pointwise raw "
            "twisted binary-prime moment theorem, strict raw-gap theorem, "
            "positive-mass theorem, q286 threshold theorem, strict-central "
            "Goldbach theorem, or Goldbach proof is established"),
        "goldbach_proved": False,
        "raw_character_moment_theorem_proved": False,
        "strict_raw_gap_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "universal_bound_open": True,
        "raw_character_definitions": {
            "central_mass": (
                "T_N=sum_{N/3<p<2N/3, p and N-p prime} "
                "log(p)log(N-p)."),
            "raw_projection_delta": (
                "Delta_raw_{d,s}(N)=Pi_raw_{N,d}(s)-T_N*U_{a,d}(s), "
                "where Pi_raw_{N,d}(s) is the raw strict-central log-pair "
                "mass with left prime p == s mod d, and U_{a,d} is the "
                "local-uniform projected mass for a=N mod 10010."),
            "raw_character_moment": (
                "D_raw_{d,chi}(N)=sum_s chi(s)*Delta_raw_{d,s}(N) "
                "over the active multiplicative characters for "
                "d in {70,130,154,286}."),
            "projected_error_expansion": (
                "E_raw_d(N)=sum_chi c_hat_{d,chi}*D_raw_{d,chi}(N), "
                "using the same finite character coefficients as the "
                "multiplicative-character payment audit."),
            "raw_witness": (
                "W_phi(N)=T_N*M(a)+sum_d E_raw_d(N)."),
            "strict_raw_gap": (
                "G_raw(N)=T_N*M(a)-sum_d max(0,-E_raw_d(N))."),
        },
        "principal_and_error_roles": {
            "principal_main": (
                "T_N*M(a), where M(a)>0 is the local-uniform q286-WBSS "
                "main term for the target residue."),
            "nonprincipal_twisted_moments": (
                "D_raw_{d,chi}(N) for the active nonprincipal character "
                "package."),
            "strict_central_truncation": (
                "The prime sum is restricted to N/3<p<2N/3; any circle "
                "method proof must estimate this truncated interval, not "
                "only the full p<N convolution."),
            "finite_remainder": (
                "Any theorem needs an explicit threshold N0 and a separate "
                "finite verification below N0."),
        },
        "sufficient_raw_theorem_shapes": {
            "aggregate_L2": {
                "statement": (
                    "For every sufficiently large covered even N, prove "
                    "C2*sqrt(sum_{d,chi}|D_raw_{d,chi}(N)|^2) < T_N*M(a)."),
                "C2": l2_budget["aggregate_character_l2"],
                "normalized_equivalent_when_T_N_positive": (
                    "sqrt(sum|D_{d,chi}(N)|^2) < "
                    "0.10930746469603118 using normalized moments."),
                "non_circular": True,
                "why": (
                    "If T_N=0 then every raw character moment is zero and "
                    "both sides are zero, so the strict inequality fails; "
                    "a proof of the strict inequality therefore creates "
                    "strict-central support."),
            },
            "aggregate_L1": {
                "statement": (
                    "For every sufficiently large covered even N, prove "
                    "sum_{d,chi}|c_hat_{d,chi}|*theta_raw_{d,chi}(N) "
                    "< T_N*M(a), with |D_raw_{d,chi}(N)|<=theta_raw_{d,chi}(N)."),
                "total_character_l1": char_budget["total_character_l1"],
                "uniform_normalized_cap_when_T_N_positive": (
                    char_budget["equal_character_moment_cap"]),
                "non_circular": True,
                "why": (
                    "The strict raw inequality fails at zero support; no "
                    "normalized measure needs to be assumed first."),
            },
            "direct_signed_sum": {
                "statement": (
                    "Prove W_phi(N)=T_N*M(a)+sum_{d,chi}"
                    "c_hat_{d,chi}D_raw_{d,chi}(N)>0 directly."),
                "non_circular": True,
                "why": (
                    "A zero-support row has W_phi(N)=0, so strict positivity "
                    "forces a strict-central prime pair."),
            },
        },
        "coefficient_package": {
            "active_complex_character_count": (
                char_budget["active_character_count"]),
            "active_real_channel_count": (
                char_budget["active_real_channel_count"]),
            "total_character_l1": char_budget["total_character_l1"],
            "equal_character_moment_cap_normalized": (
                char_budget["equal_character_moment_cap"]),
            "aggregate_character_l2": l2_budget[
                "aggregate_character_l2"],
            "aggregate_character_moment_l2_cap_normalized": l2_budget[
                "aggregate_character_moment_l2_cap"],
            "per_modulus_active_character_count": {
                modulus: row["active_character_count"]
                for modulus, row in char_budget["per_modulus"].items()
            },
        },
        "finite_diagnostic_boundary": {
            "observed_l2_row_count": observed_summary["row_count"],
            "observed_row_local_l2_cap_violations": observed_summary[
                "row_local_cap_exceeding_row_count"],
            "observed_global_min_l2_cap_violations": observed_summary[
                "global_min_cap_exceeding_row_count"],
            "role": (
                "These are finite diagnostics and falsifiers for premature "
                "claims that the normalized L2 cap already holds at the "
                "checked scale. They are not acceptance conditions and do "
                "not refute an eventual sufficiently-large theorem."),
        },
        "collapse_or_sleep_test": {
            "collapse_condition": (
                "If the proposed circle-method proof first needs an "
                "independent pointwise lower bound T_N>=P(N)>0 for every "
                "covered N, and the character estimates only operate after "
                "that mass is known, then the route has collapsed to "
                "ordinary strict-central binary Goldbach plus decoration."),
            "survival_condition": (
                "The route survives only if the raw character inequality "
                "itself is proved strictly, or if the positive-mass input is "
                "separately sourced and honestly labeled Goldbach-strength."),
            "sleep_decision_if_collapsed": (
                "Sleep q286 as a proof engine and preserve it as coefficient "
                "structure if no raw character theorem can be stated without "
                "first assuming pointwise strict-central prime-pair mass."),
        },
        "candidate": {
            "name": "raw active-character q286-WBSS theorem target",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Turn the q286-WBSS coefficient package into raw twisted "
                "binary-prime moments so strict positivity, not normalized "
                "distribution after support exists, is the theorem target."),
            "prediction": (
                "A viable proof will bound the raw active-character package "
                "below the raw principal main or prove the direct signed raw "
                "sum positive."),
            "falsifier": (
                "If every route to the raw principal main requires already "
                "proving T_N>0 pointwise, the q286 character expansion has "
                "not reduced the Goldbach-strength core."),
            "smallest_next_test": (
                "Attempt a symbolic major/minor arc decomposition for "
                "D_raw_{d,chi}(N), keeping the strict-central interval and "
                "checking whether the principal positive term is created by "
                "the same estimate or imported as T_N>0."),
        },
        "decision": (
            "The exact raw character-expanded q286-WBSS target is now "
            "defined.  The strongest clean payment is "
            "C2*||D_raw(N)||_2 < T_N*M(a), with C2 about 5.5251064487, or "
            "a direct proof W_phi(N)>0.  This target is non-circular only in "
            "raw strict form: at zero support both sides are zero and the "
            "strict inequality fails.  No theorem proving the target is "
            "currently present, so the next proof attempt must attack the "
            "raw twisted binary-prime moments directly or put the q286 lane "
            "to sleep if it requires pointwise T_N>0 first."),
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
            receipt["coefficient_package"][
                "active_complex_character_count"]),
        "aggregate_character_l2": (
            receipt["coefficient_package"]["aggregate_character_l2"]),
        "observed_row_local_l2_cap_violations": (
            receipt["finite_diagnostic_boundary"][
                "observed_row_local_l2_cap_violations"]),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
