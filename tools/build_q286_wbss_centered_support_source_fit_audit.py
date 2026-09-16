"""Audit source-theorem fit for the q286 centered-support ledger.

The centered-support inequality ledger names four raw bucket obligations:
dominant_286, dominant_154, dominant_70, and tail.  This receipt checks
whether the named source-shaped theorem families currently in the project pay
those obligations.

It is a source-fit audit only.  It imports no external theorem as sufficient,
proves no centered-error estimate, and proves no Goldbach theorem.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
LEDGER = EVIDENCE / "q286-wbss-centered-support-inequality-ledger.json"
KNOWN_ADEQUACY = EVIDENCE / "q286-wbss-known-theorem-adequacy-audit.json"
SIGNED_REGION_FIT = EVIDENCE / "q286-wbss-signed-region-source-fit-audit.json"
OUT = EVIDENCE / "q286-wbss-centered-support-source-fit-audit.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def external_source_rows():
    return [
        {
            "id": "BMOR_2018_explicit_AP_prime_counts",
            "source": (
                "Bennett, Martin, O'Bryant, Rechnitzer, Explicit bounds "
                "for primes in arithmetic progressions, arXiv:1802.00085"),
            "shape": "one_dimensional_AP_prime_counts",
            "fit_to_centered_support_ledger": "insufficient",
            "useful_part": (
                "Explicit fixed-modulus prime counts in individual AP "
                "classes."),
            "mismatch": (
                "The bucket obligations are raw signed binary-prime "
                "correlations K_B(N) for the coupled pair p and N-p.  "
                "Marginal counts for p in a residue class do not control the "
                "centered reflected convolution or one-sided negative bucket "
                "drag."),
        },
        {
            "id": "BHMS_2017_Goldbach_AP_averages",
            "source": (
                "Bhowmik, Halupczok, Matsumoto, Suzuki, Goldbach "
                "Representations in Arithmetic Progressions and zeros of "
                "Dirichlet L-functions, arXiv:1704.06103"),
            "shape": "average_AP_Goldbach_representation_information",
            "fit_to_centered_support_ledger": "insufficient_as_direct_bridge",
            "useful_part": (
                "Relevant AP Goldbach and L-function context."),
            "mismatch": (
                "Average representation information does not give a "
                "pointwise every-sufficiently-large-N lower bound for each "
                "signed bucket K_B(N)."),
        },
        {
            "id": "Salmensuu_2021_almost_all_AP_Goldbach",
            "source": (
                "Salmensuu, Goldbach's problem with primes in arithmetic "
                "progressions, arXiv:2106.00778"),
            "shape": "almost_all_binary_AP_Goldbach",
            "fit_to_centered_support_ledger": "insufficient_as_direct_bridge",
            "useful_part": (
                "Shows AP-restricted binary Goldbach has strong almost-all "
                "machinery."),
            "mismatch": (
                "The ledger needs every sufficiently large covered target, "
                "with no exceptional target left unpaid, and it needs signed "
                "bucket inequalities rather than mere representation."),
        },
        {
            "id": "Halupczok_2012_AP_Goldbach_mean_value",
            "source": (
                "Halupczok, Goldbach representations in arithmetic "
                "progressions and zeros of Dirichlet L-functions, "
                "arXiv:1212.4406"),
            "shape": "mean_value_AP_Goldbach_representation_result",
            "fit_to_centered_support_ledger": "insufficient_as_direct_bridge",
            "useful_part": (
                "Relevant mean-value and L-function framework for AP "
                "Goldbach."),
            "mismatch": (
                "Mean-value control does not supply the required pointwise "
                "one-sided lower bounds for dominant_286, dominant_154, "
                "dominant_70, and tail."),
        },
        {
            "id": "Lichtman_2023_distribution_upper_bounds",
            "source": (
                "Lichtman, Primes in arithmetic progressions to large "
                "moduli, and Goldbach beyond the square-root barrier, "
                "arXiv:2309.08522"),
            "shape": "level_of_distribution_and_upper_bound_result",
            "fit_to_centered_support_ledger": "insufficient_as_direct_bridge",
            "useful_part": (
                "Relevant modern distribution and Goldbach upper-bound "
                "context."),
            "mismatch": (
                "Distribution levels and upper bounds do not provide the "
                "positive pointwise lower bucket control needed to keep "
                "centered error above the negative budget."),
        },
        {
            "id": "ordinary_strict_central_positive_mass_theorem",
            "source": (
                "hypothetical or external pointwise theorem proving "
                "P0_a(N)>0 / T_N>0"),
            "shape": "ordinary_positive_mass_only",
            "fit_to_centered_support_ledger": "insufficient_without_bucket_bounds",
            "useful_part": (
                "Would create ordinary strict-central support."),
            "mismatch": (
                "Positive ordinary mass alone does not bound the signed "
                "centered placement of that mass.  The combined coefficient "
                "is sign-indefinite on every target support, so the mass "
                "could still concentrate in adverse bucket regions without a "
                "separate raw signed-correlation estimate."),
        },
    ]


def bucket_fit_rows(ledger):
    rows = []
    for bucket in ledger["bucket_obligations"]:
        rows.append({
            "bucket": bucket["bucket"],
            "natural_moduli": bucket["natural_moduli"],
            "support_labels": bucket["support_labels"],
            "allocated_negative_budget_ratio": bucket[
                "allocated_negative_budget_ratio"],
            "required_raw_lower_bound": (
                f"K_{bucket['bucket']}(N) >= "
                f"-{bucket['allocated_negative_budget_ratio']}*P0_a(N)"),
            "source_fit_status": "no_named_source_bridge",
            "missing_theorem_shape": (
                "pointwise raw signed binary-prime correlation lower bound "
                "for this fixed support bucket, valid for every sufficiently "
                "large covered N before dividing by actual T_N"),
        })
    return rows


def build_receipt():
    ledger = load_json(LEDGER)
    known = load_json(KNOWN_ADEQUACY)
    signed = load_json(SIGNED_REGION_FIT)
    bucket_rows = bucket_fit_rows(ledger)
    sources = external_source_rows()

    return {
        "schema_version": 1,
        "receipt": "q286-wbss-centered-support-source-fit-audit",
        "source_commit": source_commit(),
        "sources": {
            "centered_support_inequality_ledger": str(
                LEDGER.relative_to(ROOT)),
            "centered_support_ledger_status": ledger["status"],
            "known_theorem_adequacy_audit": str(
                KNOWN_ADEQUACY.relative_to(ROOT)),
            "known_theorem_adequacy_status": known["status"],
            "signed_region_source_fit_audit": str(
                SIGNED_REGION_FIT.relative_to(ROOT)),
            "signed_region_source_fit_status": signed["status"],
        },
        "status": "SOURCE_FIT_no_existing_centered_bucket_bridge",
        "question": (
            "Do currently named source-shaped theorem families pay the four "
            "q286 centered-support raw bucket inequalities?"),
        "answer": (
            "No.  The ledger obligations require pointwise raw lower bounds "
            "for signed centered binary-prime correlations in buckets 286, "
            "154, 70, and tail.  The named source families either control "
            "one-dimensional marginal AP counts, average/almost-all AP "
            "Goldbach behavior, upper-bound/distribution information, or "
            "ordinary positive mass without the signed bucket placement."),
        "required_theorem_shape": {
            "quantifier": "every sufficiently large covered even N",
            "raw_scale": (
                "K_B(N) >= -beta_B*P0_a(N), before division by actual T_N"),
            "bucket_set": ["dominant_286", "dominant_154",
                           "dominant_70", "tail"],
            "ordinary_mass_boundary": (
                "A theorem proving P0_a(N)>0 or T_N>0 is not enough unless "
                "it also proves the signed centered bucket lower bounds in "
                "the same raw argument or supplies them as a corollary."),
            "finite_remainder": (
                "Any successful theorem still needs an explicit threshold "
                "N0 and finite verification below N0."),
        },
        "ledger_budget": {
            "weakest_local_factor_ratio": ledger["budget_model"][
                "weakest_local_factor_ratio"],
            "allocated_negative_budget_total": ledger["budget_model"][
                "allocated_negative_budget_total"],
            "unallocated_reserve_ratio": ledger["budget_model"][
                "unallocated_reserve_ratio"],
            "bucket_count": len(bucket_rows),
        },
        "bucket_source_fit_table": bucket_rows,
        "source_fit_table": sources,
        "fit_summary": {
            "evaluated_source_count": len(sources),
            "bucket_obligation_count": len(bucket_rows),
            "external_direct_bridge_count": 0,
            "ordinary_positive_mass_is_sufficient": False,
            "all_buckets_paid_by_named_sources": False,
            "analytic_hold": (
                "Need a new pointwise raw signed-correlation theorem for "
                "the four centered buckets, or a sharper source-backed "
                "inequality replacing this sufficient ledger."),
        },
        "sleep_conditions": [
            "the route invokes AP marginals without reflected binary-pair "
            "correlation",
            "the route invokes average or almost-all AP Goldbach with "
            "exceptional covered targets",
            "the route proves ordinary T_N>0 but not the centered bucket "
            "lower bounds",
            "the route divides by T_N before producing raw bucket control",
        ],
        "surviving_work": {
            "bespoke_bucket_circle_method": (
                "For each bucket B, expand K_B(N) into the finite character "
                "package at its natural modulus and prove the allocated raw "
                "lower bound pointwise."),
            "sharper_ledger": (
                "Replace the sufficient beta allocation with a "
                "source-backed inequality that uses cancellations between "
                "buckets rather than independent bucket lower bounds."),
            "source_fit_next": (
                "Search for or derive pointwise fixed-modulus signed "
                "Goldbach-in-progressions estimates for the exact bucket "
                "weights."),
        },
        "candidate": {
            "name": "four-bucket source-fit HOLD",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use the centered-support ledger as a non-moving theorem "
                "target and reject adjacent source theorems whose quantifiers "
                "or observables do not pay the raw bucket bounds."),
            "prediction": (
                "Known AP-count, average, almost-all, and positive-mass-only "
                "sources will not pay the raw centered bucket obligations."),
            "falsifier": (
                "A source-backed theorem that proves the four K_B lower "
                "bounds, or a stronger combined centered-error inequality, "
                "for every sufficiently large covered N would falsify this "
                "HOLD."),
            "smallest_next_test": (
                "Write the character-expanded formula for K_d(N) for the "
                "dominant_286 bucket and identify the exact principal and "
                "nonprincipal terms a bespoke circle-method proof must "
                "control."),
        },
        "decision": (
            "SOURCE_FIT_no_existing_centered_bucket_bridge.  No named source "
            "family currently pays the four raw centered-support bucket "
            "inequalities.  Ordinary positive mass would not be enough: it "
            "does not control where mass lands against the sign-indefinite "
            "centered bucket weights.  The next evidence-bearing step is a "
            "character-expanded K_286 target, or a sharper combined ledger "
            "that reduces the source theorem required."),
        "status_boundary": (
            "Source-fit audit only; this is not a theorem.  No source theorem "
            "is promoted to a centered bucket bridge, no major/minor arc "
            "estimate, pointwise centered-error estimate, signed "
            "prime-correlation theorem, positive-mass theorem, q286 threshold "
            "theorem, strict-central Goldbach theorem, or Goldbach proof is "
            "established."),
        "goldbach_proved": False,
        "external_pointwise_bridge_found": False,
        "ordinary_positive_mass_suffices": False,
        "source_theorem_fit_proved": False,
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
        "evaluated_source_count": (
            receipt["fit_summary"]["evaluated_source_count"]),
        "bucket_obligation_count": (
            receipt["fit_summary"]["bucket_obligation_count"]),
        "external_direct_bridge_count": (
            receipt["fit_summary"]["external_direct_bridge_count"]),
        "ordinary_positive_mass_suffices": (
            receipt["ordinary_positive_mass_suffices"]),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
