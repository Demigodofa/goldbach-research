"""Triage Watanabe arXiv Goldbach PDF as external inspiration, not proof.

Kevin downloaded arXiv:1811.02415v7, titled "Definitive Proof of Goldbach's
Conjecture."  This receipt records what can safely be reused: a rough-number
product baseline and an error-envelope diagnostic.  It also records what is
not accepted: the claimed proof and the broad lower-bound story.

The finite checks here are intentionally modest.  They test the paper on its
own ordered-pair convention up to a fixed bound and preserve both helpful and
adverse outcomes.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOWNLOAD_PDF = Path(
    r"C:\Users\KevinPenfield\Downloads\1811.02415v7.pdf")
OUT = Path("evidence") / "external-watanabe-goldbach-paper-triage.json"
NOTE = Path("notes") / "external-watanabe-goldbach-paper-triage.md"
CHECK_LIMIT = 200000


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def prime_sieve(limit):
    prime = [True] * (limit + 1)
    prime[0] = prime[1] = False
    for p in range(2, int(limit ** 0.5) + 1):
        if prime[p]:
            for value in range(p * p, limit + 1, p):
                prime[value] = False
    return prime


def lprime_less(prime, x):
    value = int(math.ceil(x)) - 1
    while value >= 2 and not prime[value]:
        value -= 1
    return value


def rough_relative_to_sqrt(n, primes):
    root = math.sqrt(n)
    for p in primes:
        if p >= root:
            return True
        if p >= 3 and n % p == 0:
            return False
    return True


def ordered_goldbach_count(n, prime):
    return sum(
        1 for x in range(3, n - 2, 2)
        if prime[x] and prime[n - x])


def pi_star(n, prime, primes):
    pair_count = n // 2 - 2
    upper = lprime_less(prime, math.sqrt(n))
    product = 1.0
    for p in primes:
        if p < 3:
            continue
        if p > upper:
            break
        product *= (p - 2) / p
    return pair_count * product


def emax(n, prime, primes):
    upper = lprime_less(prime, math.sqrt(n))
    total = 0.0
    for p in primes:
        if p < 3:
            continue
        if p > upper:
            break
        total += (3 * p - 3) / p
    return total


def first_lower_bound_counterexamples(prime, primes):
    counterexamples = []
    for index, p in enumerate(primes):
        if p < 3 or index + 1 >= len(primes):
            continue
        lower = p * p + 1
        upper = primes[index + 1] * primes[index + 1] - 1
        if lower > CHECK_LIMIT:
            break
        upper = min(upper, CHECK_LIMIT)
        start = lower if lower % 2 == 0 else lower + 1
        values = []
        for n in range(start, upper + 1, 2):
            values.append({
                "n": n,
                "ordered_prime_pair_count": ordered_goldbach_count(n, prime),
                "rough_relative_to_sqrt": rough_relative_to_sqrt(n, primes),
            })
        if not values:
            continue
        rough_values = [
            row for row in values if row["rough_relative_to_sqrt"]]
        if not rough_values:
            continue
        minimum = min(row["ordered_prime_pair_count"] for row in values)
        rough_minimum = min(
            row["ordered_prime_pair_count"] for row in rough_values)
        if rough_minimum > minimum:
            counterexamples.append({
                "prime_square_block_start_prime": p,
                "block_range": [lower, upper],
                "nonrough_minimum_row": next(
                    row for row in values
                    if (not row["rough_relative_to_sqrt"]
                        and row["ordered_prime_pair_count"] == minimum)),
                "rough_minimum_row": next(
                    row for row in rough_values
                    if row["ordered_prime_pair_count"] == rough_minimum),
            })
            if len(counterexamples) >= 10:
                break
    return counterexamples


def run_checks():
    prime = prime_sieve(CHECK_LIMIT)
    primes = [value for value, is_prime in enumerate(prime) if is_prime]
    rough_rows_checked = 0
    first_error_envelope_failures = []
    first_positive_lower_bound_failures = []
    for n in range(6, CHECK_LIMIT + 1, 2):
        if not rough_relative_to_sqrt(n, primes):
            continue
        rough_rows_checked += 1
        actual = ordered_goldbach_count(n, prime)
        approximation = pi_star(n, prime, primes)
        envelope = emax(n, prime, primes)
        if abs(actual - approximation) > envelope + 1e-9:
            first_error_envelope_failures.append({
                "n": n,
                "actual_ordered_prime_pairs": actual,
                "pi_star": approximation,
                "emax": envelope,
                "absolute_error": abs(actual - approximation),
            })
            if len(first_error_envelope_failures) >= 10:
                break
        if n >= 624 and approximation - envelope <= 0:
            first_positive_lower_bound_failures.append({
                "n": n,
                "pi_star_minus_emax": approximation - envelope,
                "pi_star": approximation,
                "emax": envelope,
            })
    return {
        "check_limit": CHECK_LIMIT,
        "rough_rows_checked": rough_rows_checked,
        "first_error_envelope_failures": first_error_envelope_failures,
        "first_positive_lower_bound_failures_after_622": (
            first_positive_lower_bound_failures[:10]),
        "lower_bound_counterexamples_by_prime_square_block": (
            first_lower_bound_counterexamples(prime, primes)),
    }


def build_receipt():
    checks = run_checks()
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "TRIAGE_external_watanabe_goldbach_paper",
        "local_pdf": str(DOWNLOAD_PDF),
        "public_source": {
            "arxiv_id": "1811.02415v7",
            "doi": "10.48550/arXiv.1811.02415",
            "url": "https://arxiv.org/abs/1811.02415",
            "title": "Definitive Proof of Goldbach's Conjecture",
            "author": "Kenneth A. Watanabe",
            "date_in_pdf": "2025-08-12",
            "license_in_pdf_metadata": (
                "http://arxiv.org/licenses/nonexclusive-distrib/1.0/"),
        },
        "question": (
            "Does the downloaded Watanabe arXiv PDF help the active Goldbach "
            "research route, and can any part be reused with attribution?"),
        "paper_mechanism_summary": (
            "The paper uses ordered Goldbach pair counts, identifies even "
            "numbers not divisible by small primes below sqrt(n) as a proposed "
            "low-pair family, approximates their ordered prime-pair count by "
            "|P(n)| times product_{3<=p<=l(sqrt(n))}(p-2)/p, and proposes an "
            "error envelope emax(n) <= 3*pi(sqrt(n))."),
        "finite_checks": checks,
        "classification": {
            "public_arxiv_source_can_be_cited_with_attribution": True,
            "accepted_as_goldbach_proof": False,
            "peer_review_status_verified": False,
            "rough_product_baseline_useful_as_diagnostic": True,
            "error_envelope_no_failure_found_to_check_limit": (
                len(checks["first_error_envelope_failures"]) == 0),
            "pi_star_minus_emax_no_failure_found_after_622_to_check_limit": (
                len(checks[
                    "first_positive_lower_bound_failures_after_622"]) == 0),
            "broad_rough_lower_bound_story_refuted_in_checked_blocks": (
                len(checks[
                    "lower_bound_counterexamples_by_prime_square_block"]) > 0),
            "finite_external_source_triage_only": True,
        },
        "candidate_reuse": {
            "name": "roughness-product baseline diagnostic",
            "novelty_label": "external-source-inspired",
            "mechanism": (
                "Use the product of (p-2)/p over small primes as a roughness "
                "baseline for external comparison against our replacement "
                "packet compensation audits."),
            "prediction": (
                "Rows that are all-high/no-small or otherwise avoid small "
                "prime support should look worse under both the roughness "
                "baseline and the source-pair compensation metrics."),
            "falsifier": (
                "If roughness-product ordering disagrees systematically with "
                "kernel overpayment risk, it is only a visualization/triage "
                "feature and should not guide theorem obligations."),
            "smallest_next_test": (
                "Add roughness-product features to the 35-row Q46189 packet "
                "landscape and compare them to off_diagonal/diagonal_half, "
                "middle-loss, and source-pair compensation ranks."),
        },
        "decision": (
            "The PDF is useful as an external-source diagnostic, not as a "
            "proof.  The product baseline and error-envelope idea can be "
            "used with attribution as a feature to compare against our packet "
            "geometry.  The paper's broad lower-bound story is not accepted: "
            "finite prime-square block checks found non-rough rows with fewer "
            "ordered prime pairs than the rough minimum in the same block.  "
            "Goldbach remains unproved."),
        "external_paper_triage_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
    }


def write_note(receipt):
    checks = receipt["finite_checks"]
    lines = [
        "# External Watanabe Goldbach paper triage",
        "",
        "## Source",
        "",
        "```text",
        "local PDF: C:/Users/KevinPenfield/Downloads/1811.02415v7.pdf",
        "arXiv:    https://arxiv.org/abs/1811.02415",
        "title:    Definitive Proof of Goldbach's Conjecture",
        "author:   Kenneth A. Watanabe",
        "license:  arXiv non-exclusive distribution license in PDF metadata",
        "```",
        "",
        "## Decision",
        "",
        "This source can be cited and used as external inspiration with",
        "attribution.  It is not accepted here as a proof of Goldbach.",
        "",
        "The useful part is a roughness-product baseline: approximate the",
        "ordered prime-pair count for even numbers avoiding small prime",
        "divisibility by multiplying `|P(n)|` by",
        "`prod (p-2)/p` over small primes.",
        "",
        "The dangerous part is the promotion from finite/product heuristics",
        "and postulates to a universal proof.  The repo should not adopt that",
        "promotion.",
        "",
        "## Finite Checks",
        "",
        "```text",
        f"check limit:                                  {checks['check_limit']}",
        f"rough rows checked:                           {checks['rough_rows_checked']}",
        f"error-envelope failures found:                {len(checks['first_error_envelope_failures'])}",
        f"Pi-star-minus-emax failures after 622 found:  {len(checks['first_positive_lower_bound_failures_after_622'])}",
        f"rough lower-bound block counterexamples:      {len(checks['lower_bound_counterexamples_by_prime_square_block'])}",
        "```",
        "",
        "The broad lower-bound story has checked counterexamples.  Example:",
        "",
        "```json",
        json.dumps(
            checks["lower_bound_counterexamples_by_prime_square_block"][:3],
            indent=2,
        ),
        "```",
        "",
        "## Candidate Reuse",
        "",
        "Use the roughness-product baseline as a diagnostic feature for the",
        "`Q=46189` packet landscape.  Compare it to the current kernel metrics:",
        "`off_diagonal/diagonal_half`, `middle_A_to_10A`, non-middle",
        "compensation, and source-pair mirror-block ranks.",
        "",
        "This is finite external-source triage only.  It proves no lower-bound",
        "theorem, no error-envelope theorem, no replacement-packet theorem, no",
        "strict-central Goldbach theorem, and no Goldbach proof.",
        "",
    ]
    NOTE.write_text("\n".join(lines), encoding="utf-8")


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    write_note(receipt)
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "rough_rows_checked": (
            receipt["finite_checks"]["rough_rows_checked"]),
        "error_envelope_failures": len(
            receipt["finite_checks"]["first_error_envelope_failures"]),
        "rough_lower_bound_counterexamples": len(
            receipt["finite_checks"][
                "lower_bound_counterexamples_by_prime_square_block"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
