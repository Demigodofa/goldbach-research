"""Audit source-theorem fit for the q286 signed-region obligation.

The negative-region mass threshold audit left a precise theorem obligation:
prove raw positive weighted mass exceeds raw negative weighted mass for every
sufficiently large covered N.  This receipt checks whether the currently named
source-shaped tools already pay that exact obligation.

It is a source-fit audit only.  No external theorem is promoted to a q286
signed-region theorem, and Goldbach is not proved.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
NEGATIVE_REGION = (
    EVIDENCE / "q286-wbss-negative-region-mass-threshold-audit.json")
SOURCE_FIT = EVIDENCE / "q286-wbss-source-theorem-fit-audit.json"
CHAR_L2 = (
    EVIDENCE / "q286-wbss-multiplicative-character-l2-payment-audit.json")
OUT = EVIDENCE / "q286-wbss-signed-region-source-fit-audit.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_fit_rows():
    return [
        {
            "id": "BMOR_2018_AP_prime_counts",
            "source": (
                "Bennett, Martin, O'Bryant, Rechnitzer, Explicit bounds "
                "for primes in arithmetic progressions, Illinois J. Math. "
                "62 (2018), arXiv:1802.00085"),
            "source_type": (
                "explicit one-dimensional prime-count estimates in APs"),
            "fit_to_signed_region_obligation": "insufficient",
            "useful_part": (
                "Can bound marginal prime counts in residue classes."),
            "mismatch": (
                "The signed-region obligation is a reflected binary-prime "
                "convolution with weights on the left prime and a coupled "
                "condition that N-p is prime.  Marginal AP counts do not "
                "control where strict-central prime-pair mass lands inside "
                "positive and negative q286 regions."),
            "reactivation_condition": (
                "Only reactivate if combined with a separate pointwise "
                "binary-prime correlation theorem strong enough for the "
                "signed q286 regions."),
        },
        {
            "id": "Salmensuu_2021_binary_AP_Goldbach_almost_all",
            "source": (
                "Salmensuu, Goldbach's problem with primes in arithmetic "
                "progressions, arXiv:2106.00778"),
            "source_type": (
                "binary Goldbach in APs with exceptional-set or almost-all "
                "quantifiers"),
            "fit_to_signed_region_obligation": "insufficient_as_direct_bridge",
            "useful_part": (
                "Relevant AP-restricted binary Goldbach setting."),
            "mismatch": (
                "The q286 target needs every sufficiently large covered N, "
                "strict-central truncation, log weights, and the exact signed "
                "positive-region versus negative-region inequality.  An "
                "almost-all or exceptional-set theorem leaves possible "
                "covered targets unpaid."),
            "reactivation_condition": (
                "Reactivate only after deriving an explicit no-exception "
                "corollary for the exact finite q286 signed-region weight."),
        },
        {
            "id": "Halupczok_2012_AP_Goldbach_mean_value",
            "source": (
                "Halupczok, Goldbach representations in arithmetic "
                "progressions and zeros of Dirichlet L-functions, "
                "arXiv:1212.4406"),
            "source_type": "mean-value / AP Goldbach representation result",
            "fit_to_signed_region_obligation": "insufficient_as_direct_bridge",
            "useful_part": (
                "Relevant circle-method and L-function context for AP "
                "Goldbach."),
            "mismatch": (
                "Mean-value or averaged representation information does not "
                "prove the pointwise signed-region inequality for every "
                "covered N."),
            "reactivation_condition": (
                "Reactivate only if a pointwise fixed-modulus weighted "
                "binary-prime corollary is derived from it."),
        },
        {
            "id": "q286_active_character_L2_payment",
            "source": (
                "local q286-WBSS multiplicative-character L2 payment audit"),
            "source_type": "internal coefficient-side theorem target",
            "fit_to_signed_region_obligation": "related_unproved_target",
            "useful_part": (
                "Gives a clean aggregate raw character-moment payment shape."),
            "mismatch": (
                "It remains an unproved pointwise twisted binary-prime "
                "moment theorem.  It can be one sufficient path to signed "
                "region control, but it is not source evidence that the "
                "required inequality holds."),
            "reactivation_condition": (
                "Derive or cite a pointwise raw fixed-modulus character "
                "moment theorem with explicit constants and finite remainder."),
        },
        {
            "id": "q286_signed_region_shape_target",
            "source": (
                "local q286-WBSS negative-region mass threshold audit"),
            "source_type": "current internal theorem obligation",
            "fit_to_signed_region_obligation": "exact_target_not_theorem",
            "useful_part": (
                "Names the exact raw inequality: positive weighted mass must "
                "exceed negative weighted mass."),
            "mismatch": (
                "It is coefficient algebra and theorem shape only.  It does "
                "not prove prime-pair mass follows the needed signed shape."),
            "reactivation_condition": (
                "Use as the target for a bespoke circle-method or signed "
                "binary-prime correlation estimate."),
        },
    ]


def build_receipt():
    negative = load_json(NEGATIVE_REGION)
    prior_source_fit = load_json(SOURCE_FIT)
    char_l2 = load_json(CHAR_L2)
    rows = source_fit_rows()
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-signed-region-source-fit-audit",
        "source_commit": source_commit(),
        "sources": {
            "negative_region_mass_threshold_audit": str(
                NEGATIVE_REGION.relative_to(ROOT)),
            "negative_region_mass_threshold_status": negative["status"],
            "strict_raw_gap_source_fit_audit": str(
                SOURCE_FIT.relative_to(ROOT)),
            "strict_raw_gap_source_fit_status": prior_source_fit["status"],
            "multiplicative_character_l2_payment_audit": str(
                CHAR_L2.relative_to(ROOT)),
            "multiplicative_character_l2_payment_status": char_l2["status"],
        },
        "status": "SOURCE_FIT_no_existing_signed_region_pointwise_bridge",
        "question": (
            "Does any currently named source-shaped theorem pay the q286 "
            "raw signed-region obligation?"),
        "answer": (
            "No currently named source theorem directly pays it.  The "
            "surviving q286 target is more specific than one-dimensional AP "
            "counts, almost-all AP Goldbach, or averaged AP representation "
            "theorems.  It needs a pointwise, strict-central, log-weighted, "
            "fixed finite-modulus signed binary-prime correlation estimate."),
        "required_theorem_shape": {
            "quantifier": "every sufficiently large covered even N",
            "raw_inequality": (
                "sum_{u:phi(u)>0} P_N(u)phi(u) > "
                "sum_{u:phi(u)<0} P_N(u)(-phi(u))"),
            "strict_central": "N/3 < p < 2N/3",
            "binary": "both p and N-p prime, with log weights",
            "weighted": (
                "exact q286 signed-region weight or an equivalent "
                "four-modulus / active-character expansion"),
            "finite_remainder": (
                "explicit threshold N0 with separate verification below N0"),
            "normalization_boundary": (
                "A normalized negative-region mass statement is not enough "
                "unless it is embedded in a raw strict positivity proof or "
                "paired with an independently proved positive-mass theorem."),
        },
        "source_fit_table": rows,
        "fit_summary": {
            "evaluated_source_count": len(rows),
            "external_direct_bridge_count": 0,
            "internal_exact_target": "q286_signed_region_shape_target",
            "internal_related_unproved_target": "q286_active_character_L2_payment",
            "shape_threshold_minimum": negative["summary"][
                "shape_mass_threshold_summary"]["minimum"],
            "minimum_local_uniform_shape_margin": negative["summary"][
                "uniform_margin_to_shape_threshold_summary"]["minimum"],
            "robust_sign_mass_route_sleeping": True,
        },
        "sleep_conditions": [
            "the proposed proof uses only one-dimensional AP marginals",
            "the proposed proof is almost-all or averaged over N",
            "the proposed proof controls only total negative-region mass by a "
            "crude robust threshold",
            "the proposed proof divides by T_N without a raw strict "
            "positivity argument or a separately proved positive-mass theorem",
        ],
        "surviving_work": {
            "bespoke_circle_method_target": (
                "Prove a pointwise major/minor arc estimate for the exact "
                "signed q286 weight."),
            "character_moment_target": (
                "Prove raw active-character moment bounds strong enough to "
                "imply the signed-region inequality."),
            "region_correlation_target": (
                "Prove prime-pair mass has enough within-sign shape that "
                "positive weighted mass dominates negative weighted mass."),
        },
        "candidate": {
            "name": "signed-region source-fit HOLD",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use the negative-region threshold audit to ask for the exact "
                "source theorem needed, rather than accepting nearby AP "
                "theorems with weaker quantifiers or wrong observables."),
            "prediction": (
                "Named broad AP sources will be useful context but will not "
                "directly pay the raw signed-region inequality."),
            "falsifier": (
                "A source-backed pointwise theorem for the exact q286 signed "
                "finite-modulus binary-prime weight would falsify this HOLD."),
            "smallest_next_test": (
                "Try deriving a bespoke circle-method major/minor arc target "
                "for the exact signed q286 weight, or produce a no-go "
                "classifier if it collapses to proving T_N>0 first."),
        },
        "decision": (
            "SOURCE_FIT_no_existing_signed_region_pointwise_bridge.  The "
            "signed-region obligation is now exact, but no currently named "
            "external source theorem pays it directly.  BMOR is marginal AP "
            "input; Salmensuu and Halupczok are relevant but not pointwise "
            "exact weighted signed-region bridges; the local character-L2 "
            "target is related but unproved.  The next useful work is a "
            "bespoke fixed-modulus signed circle-method target or a collapse "
            "classifier if that target requires T_N>0 first."),
        "status_boundary": (
            "Source-fit audit only; no external pointwise bridge theorem, "
            "signed negative-region distribution theorem, raw adverse-drag "
            "theorem, positive-mass theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof is "
            "established."),
        "goldbach_proved": False,
        "external_pointwise_bridge_found": False,
        "signed_negative_region_distribution_theorem_proved": False,
        "raw_adverse_drag_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
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
        "evaluated_source_count": (
            receipt["fit_summary"]["evaluated_source_count"]),
        "external_direct_bridge_count": (
            receipt["fit_summary"]["external_direct_bridge_count"]),
        "minimum_local_uniform_shape_margin": (
            receipt["fit_summary"]["minimum_local_uniform_shape_margin"]),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
