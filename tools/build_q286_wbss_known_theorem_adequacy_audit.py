"""Audit whether known-style external theorems pay the q286-WBSS budget.

The previous receipt records the exact coefficient-discrepancy budget needed
to prove adverse_drag(N) < local_main(N).  This derived receipt compares that
budget with source-backed theorem shapes currently on the table.  It is a
theorem adequacy audit, not a proof import.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
COEFFICIENT_HOLD = (
    EVIDENCE / "q286-wbss-coefficient-discrepancy-budget-hold.json")
OUT = EVIDENCE / "q286-wbss-known-theorem-adequacy-audit.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def evaluated_sources():
    return [
        {
            "id": "BMOR_2018_explicit_AP_prime_counts",
            "source": (
                "Bennett, Martin, O'Bryant, Rechnitzer, Explicit bounds "
                "for primes in arithmetic progressions"),
            "public_locator": "https://arxiv.org/abs/1802.00085",
            "shape": "one_dimensional_prime_counts_in_AP",
            "what_it_supplies": (
                "Explicit estimates for pi(x;q,a), theta(x;q,a), and "
                "psi(x;q,a) in individual prime residue classes."),
            "why_not_enough": (
                "The q286-WBSS budget is a binary convolution/residue-pair "
                "statement for the actual partner N-p.  Marginal prime "
                "counts in p mod q do not control the signed correlation "
                "between p and N-p."),
            "pays_q286_wbss_budget": False,
        },
        {
            "id": "BHMS_2017_Goldbach_AP_averages",
            "source": (
                "Bhowmik, Halupczok, Matsumoto, Suzuki, Goldbach "
                "Representations in Arithmetic Progressions and zeros of "
                "Dirichlet L-functions"),
            "public_locator": "https://arxiv.org/abs/1704.06103",
            "shape": "average_Goldbach_representations_in_AP",
            "what_it_supplies": (
                "Average-order Goldbach-in-progressions information and "
                "relations with zeros of Dirichlet L-functions."),
            "why_not_enough": (
                "Average asymptotics, even when informative about zeros, do "
                "not give the every-sufficiently-large-N pointwise "
                "one-sided discrepancy bound needed here."),
            "pays_q286_wbss_budget": False,
        },
        {
            "id": "Salmensuu_2021_almost_all_AP_Goldbach",
            "source": (
                "Salmensuu, The Goldbach conjecture with summands in "
                "arithmetic progressions"),
            "public_locator": "https://arxiv.org/abs/2106.00778",
            "shape": "almost_all_moduli_residue_classes_and_targets",
            "what_it_supplies": (
                "Almost-all representation results over moduli, residue "
                "classes, and natural numbers."),
            "why_not_enough": (
                "Almost-all coverage does not imply the q286-WBSS "
                "pointwise bound for every sufficiently large covered even "
                "target."),
            "pays_q286_wbss_budget": False,
        },
        {
            "id": "Lichtman_2023_level_distribution_upper_bounds",
            "source": (
                "Lichtman, Primes in arithmetic progressions to large "
                "moduli, and Goldbach beyond the square-root barrier"),
            "public_locator": "https://arxiv.org/abs/2309.08522",
            "shape": "level_of_distribution_and_upper_bounds",
            "what_it_supplies": (
                "Improved distribution levels for primes and applications "
                "to upper bounds for Goldbach representations."),
            "why_not_enough": (
                "Upper bounds and level-of-distribution improvements do not "
                "provide a positive lower bound or one-sided signed "
                "discrepancy estimate for each fixed q286-WBSS target."),
            "pays_q286_wbss_budget": False,
        },
    ]


def build_receipt():
    hold = load_json(COEFFICIENT_HOLD)
    budget = hold["coefficient_budget"]
    sources = evaluated_sources()
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "coefficient_discrepancy_hold": str(
                COEFFICIENT_HOLD.relative_to(ROOT)),
            "coefficient_discrepancy_hold_source_commit": hold[
                "source_commit"],
        },
        "status": "HOLD_external_known_theorems_do_not_pay_budget",
        "status_boundary": (
            "source-backed theorem adequacy audit only; it imports no proof "
            "of a q286-WBSS pointwise discrepancy theorem, threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "known_source_pays_budget": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "fixed_modulus_binary_prime_discrepancy_theorem_proved": False,
        "universal_bound_open": True,
        "active_budget": {
            "direct_one_sided_condition": budget[
                "component_bound_template"],
            "per_residue_condition": budget[
                "direct_sufficient_inequality"],
            "minimum_local_main": budget[
                "minimum_local_main_over_even_residues"],
            "total_l1_norm": budget["total_l1_norm"],
            "equal_eta_cap": budget["global_equal_residue_error_cap"],
        },
        "evaluated_sources": sources,
        "adequacy_matrix": {
            source["id"]: {
                "pays_q286_wbss_budget": source[
                    "pays_q286_wbss_budget"],
                "blocking_mismatch": source["shape"],
            }
            for source in sources
        },
        "sufficient_external_theorem_shape": {
            "full_per_residue_version": (
                "For each d in {70,130,154,286}, every projected residue s, "
                "and every sufficiently large covered even N, prove "
                "|Delta_{d,s}(N)| <= eta_d(N) with "
                "sum_d L1_d*eta_d(N) < local_main(N)."),
            "narrow_one_sided_version": (
                "For each d, prove max(0,-E_d(N)) <= B_d(N) pointwise with "
                "sum_d max(0,B_d(N)) < local_main(N)."),
            "why_full_AP_asymptotic_would_be_strong": (
                "A positive pointwise asymptotic for every fixed residue-pair "
                "channel would imply the budget, but that is already a "
                "binary Goldbach-in-progressions-strength input rather than "
                "a small local q286 lemma."),
        },
        "candidate": {
            "name": "signed-character budget instead of full AP uniformity",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Decompose the four q286-WBSS coefficient projections into "
                "Dirichlet-character or finite Fourier modes and try to "
                "bound only the adverse signed combination, not every "
                "residue-pair channel separately."),
            "prediction": (
                "If the coefficient support is spectrally sparse or has "
                "cancellations invisible to per-residue L1, a direct "
                "one-sided character estimate may require less than full "
                "pointwise AP Goldbach."),
            "falsifier": (
                "If the adverse WBSS coefficient family has substantial "
                "weight across enough nonprincipal character channels that "
                "each needs an individual pointwise binary-prime asymptotic, "
                "then this route collapses back to the known Goldbach-strength "
                "input."),
            "smallest_test": (
                "Build a character-mode burden audit for the four WBSS "
                "projected coefficient families and measure whether the "
                "adverse budget is concentrated in few modes or spread across "
                "many hard channels."),
        },
        "decision": (
            "Known checked theorem shapes do not currently pay the q286-WBSS "
            "coefficient-discrepancy budget.  One-dimensional AP prime-count "
            "bounds miss binary correlation, average and almost-all "
            "Goldbach-in-AP results miss the every-large-N quantifier, and "
            "upper-bound/distribution results miss the required positive "
            "one-sided lower control.  The next non-finite route is a "
            "signed-character burden audit to see whether the WBSS adverse "
            "combination is narrower than full fixed-modulus pointwise "
            "Goldbach in progressions."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
