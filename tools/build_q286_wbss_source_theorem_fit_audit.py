"""Audit source theorem fit for the q286-WBSS strict raw gap.

The strict raw analytic HOLD asks for a pointwise raw binary-prime estimate.
This receipt records whether currently named source-backed AP/Goldbach tools
fit that exact payment request.  It is a theorem-fit audit, not a literature
review and not a proof.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
STRICT_HOLD_SOURCE = EVIDENCE / "q286-wbss-strict-raw-gap-analytic-hold.json"
CHAR_L2_SOURCE = (
    EVIDENCE / "q286-wbss-multiplicative-character-l2-payment-audit.json")
OUT = EVIDENCE / "q286-wbss-source-theorem-fit-audit.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_fits():
    return [
        {
            "id": "BMOR_2018_AP_prime_counts",
            "source": (
                "Bennett, Martin, O'Bryant, Rechnitzer, Explicit bounds "
                "for primes in arithmetic progressions, Illinois J. Math. "
                "62 (2018), arXiv:1802.00085"),
            "url": "https://arxiv.org/abs/1802.00085",
            "source_type": (
                "explicit one-dimensional prime-count estimates in APs"),
            "useful_input": (
                "fixed-modulus endpoint counts for pi, theta, and psi"),
            "fit_to_q286_raw_gap": "insufficient",
            "mismatch": (
                "controls marginal prime occupancy by residue class, but "
                "does not control the reflected binary convolution p+(N-p), "
                "the q286 signed coefficient direction, or every target N"),
            "existing_repo_status": (
                "q286-ap-count-bridge-gap-audit already falsifies the "
                "count-only pigeonhole bridge in the valid q=286 range"),
        },
        {
            "id": "Salmensuu_2021_binary_AP_Goldbach_almost_all",
            "source": (
                "Salmensuu, Goldbach's problem with primes in arithmetic "
                "progressions, arXiv:2106.00778"),
            "url": "https://arxiv.org/abs/2106.00778",
            "source_type": (
                "binary Goldbach in arithmetic progressions with exceptional "
                "sets / almost-all quantifiers"),
            "useful_input": (
                "confirms that AP-restricted binary Goldbach has source "
                "literature beyond one-dimensional AP counts"),
            "fit_to_q286_raw_gap": "insufficient_as_direct_bridge",
            "mismatch": (
                "the q286 bridge needs every sufficiently large covered even "
                "N, an explicit finite-remainder threshold, the strict "
                "central interval, and a signed weighted coefficient sum.  "
                "An almost-all or exceptional-set theorem leaves unnamed "
                "targets and does not pay the pointwise raw gap"),
            "reactivation_condition": (
                "reactivate only if an explicit corollary is proved for the "
                "exact q286 coefficient family with no exceptional covered "
                "targets above a threshold"),
        },
        {
            "id": "Halupczok_2012_AP_Goldbach_mean_value",
            "source": (
                "Halupczok, Goldbach representations in arithmetic "
                "progressions and zeros of Dirichlet L-functions, "
                "arXiv:1212.4406"),
            "url": "https://arxiv.org/abs/1212.4406",
            "source_type": "mean-value / AP Goldbach representation results",
            "useful_input": (
                "relevant circle-method and L-function setting for AP "
                "Goldbach questions"),
            "fit_to_q286_raw_gap": "insufficient_as_direct_bridge",
            "mismatch": (
                "mean-value or averaged representation information does not "
                "give a pointwise lower bound for the signed q286-WBSS raw "
                "witness for every covered N"),
            "reactivation_condition": (
                "reactivate only if a pointwise fixed-modulus weighted "
                "binary-prime corollary is derived from it"),
        },
        {
            "id": "q286_active_character_L2_payment",
            "source": (
                "local q286-WBSS multiplicative-character L2 payment audit"),
            "url": (
                "evidence/q286-wbss-multiplicative-character-l2-payment-"
                "audit.json"),
            "source_type": "coefficient-side theorem target",
            "useful_input": (
                "aggregate active-character moment cap is much looser than "
                "per-residue L-infinity payment"),
            "fit_to_q286_raw_gap": "best_current_internal_target",
            "mismatch": (
                "still lacks the external pointwise twisted binary-prime "
                "moment theorem and still must be rawized or paired with "
                "positive mass"),
            "reactivation_condition": (
                "derive a raw circle-method theorem for the exact active "
                "character package, not just coefficient algebra"),
        },
    ]


def build_receipt():
    strict_hold = load_json(STRICT_HOLD_SOURCE)
    char_l2 = load_json(CHAR_L2_SOURCE)
    fits = source_fits()
    direct_fits = [
        item for item in fits
        if item["fit_to_q286_raw_gap"] in {
            "sufficient", "best_current_internal_target"}
    ]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "strict_raw_gap_analytic_hold": str(
                STRICT_HOLD_SOURCE.relative_to(ROOT)),
            "strict_raw_gap_analytic_hold_status": strict_hold["status"],
            "multiplicative_character_l2_payment_audit": str(
                CHAR_L2_SOURCE.relative_to(ROOT)),
            "multiplicative_character_l2_payment_status": char_l2["status"],
        },
        "status": "SOURCE_FIT_no_existing_direct_pointwise_bridge",
        "status_boundary": (
            "source theorem fit audit only; no external source is promoted to "
            "a q286 strict raw-gap theorem, no pointwise binary-prime "
            "convolution theorem is proved, and Goldbach remains open"),
        "goldbach_proved": False,
        "strict_raw_gap_theorem_proved": False,
        "external_pointwise_bridge_found": False,
        "binary_prime_convolution_theorem_proved": False,
        "universal_bound_open": True,
        "required_theorem_shape": {
            "pointwise": "every sufficiently large covered even N",
            "raw": (
                "unnormalized sum; zero-support rows must give zero, so a "
                "strict positive theorem creates support"),
            "weighted": (
                "exact q286-WBSS coefficient or an equivalent four-modulus / "
                "active-character expansion"),
            "strict_central": "prime p restricted to N/3 < p < 2N/3",
            "finite_remainder": (
                "explicit threshold N0 with separate verification below N0"),
        },
        "source_fit_table": fits,
        "fit_summary": {
            "evaluated_source_count": len(fits),
            "external_direct_bridge_count": 0,
            "internal_best_target": "q286_active_character_L2_payment",
            "character_l2_cap": char_l2["character_l2_budget"][
                "aggregate_character_moment_l2_cap"],
            "character_l2_status": char_l2["status"],
        },
        "candidate": {
            "name": "fixed-finite-modulus weighted circle-method bridge",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Expand the q286-WBSS coefficient into a finite active "
                "character package and try to prove a pointwise raw "
                "major-arc main term with minor-arc/twisted-character error "
                "smaller than the positive local main."),
            "prediction": (
                "If the candidate is real, it will produce an explicit raw "
                "lower bound for the signed q286-WBSS witness, not merely "
                "almost-all AP occupancy or normalized distribution."),
            "falsifier": (
                "If the argument needs an unproved pointwise lower bound for "
                "the unweighted strict-central binary Goldbach count before "
                "the signed witness is positive, then the route remains "
                "Goldbach-strength and cannot be accepted as an easier bridge."),
            "smallest_next_test": (
                "Write the exact raw character-expanded target B_phi(N) and "
                "separate which terms would be principal main, nonprincipal "
                "twisted moments, strict-central truncation error, and finite "
                "remainder."),
        },
        "decision": (
            "No currently named source theorem fits the q286 strict raw-gap "
            "payment as a direct bridge.  BMOR is one-dimensional AP input; "
            "Salmensuu and Halupczok are relevant but not pointwise exact "
            "q286 signed raw-gap theorems.  The next evidence-bearing move is "
            "therefore not another finite scan, but an exact raw "
            "character-expanded theorem target for a bespoke fixed-modulus "
            "weighted circle-method estimate, or a sleep decision if that "
            "target collapses to ordinary pointwise binary Goldbach."),
        "sleep_conditions": [
            "the next work only invokes almost-all or averaged theorems",
            "the next work uses one-dimensional AP marginals without binary "
            "convolution control",
            "the next work restates lambda_phi<1 or G_raw>0 without a new "
            "source theorem or exact raw character expansion",
        ],
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
        "internal_best_target": receipt["fit_summary"]["internal_best_target"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
