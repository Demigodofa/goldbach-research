"""Stress-test the frozen Q46189 50A..60A selector on unused denominators.

The selector-provenance audit established that 50A..60A was selected after
examining slices.  This receipt treats the selector as frozen and asks a
stronger finite question: does the same block survive same-source reduced
denominators that were not part of the original replacement witness family?
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    scale_parameters,
)
from tools.build_mobius_moment_square_degree5_q46189_50a60a_distance_profile_audit import (  # noqa: E402
    band_metric,
    paired_distance_values,
)
from tools.build_mobius_moment_square_degree5_q46189_exception_bound_audit import (  # noqa: E402
    DENOMINATOR,
    PRIME,
    SCALE,
    TARGET_LABEL,
)
from tools.build_mobius_moment_square_degree5_q46189_group_payment_audit import (  # noqa: E402
    HIGH_PRIMES,
    factor_integer,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _residue_cells_by_denominator,
)


SOURCE_LEDGER = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-one-coordinate-ratio-ledger-audit.json")
SOURCE_SELECTOR_HOLDOUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-selector-provenance-holdout-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-frozen-selector-unused-denominator-holdout.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-frozen-selector-unused-denominator-holdout.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def arithmetic_profile(reduced_denominator):
    factors = factor_integer(reduced_denominator)
    support = {int(prime) for prime in factors}
    high_support = sorted(set(HIGH_PRIMES) & support)
    return {
        "factorization": factors,
        "high_prime_support": high_support,
        "missing_high_primes": sorted(set(HIGH_PRIMES) - support),
        "small_prime_support": sorted(support - set(HIGH_PRIMES)),
        "high_prime_support_count": len(high_support),
    }


def holdout_row(q, values, adverse_metric, lower, upper):
    metric = band_metric(values, lower, upper)
    share_gap = (
        metric["positive_fraction_of_absolute"]
        - adverse_metric["positive_fraction_of_absolute"])
    total_gap = (
        metric["total_over_diagonal"]
        - adverse_metric["total_over_diagonal"])
    return {
        "reduced_denominator": q,
        **arithmetic_profile(q),
        "metric": metric,
        "positive_fraction_gap_vs_q46189": share_gap,
        "total_gap_vs_q46189": total_gap,
        "passes_positive_fraction_separator": share_gap > 0,
        "passes_total_pressure_separator": total_gap > 0,
        "passes_both_frozen_50A_to_60A_tests": (
            share_gap > 0 and total_gap > 0),
    }


def finite_summary(rows):
    if not rows:
        return {
            "row_count": 0,
            "minimum_positive_fraction_gap": None,
            "minimum_total_gap": None,
            "weakest_positive_fraction_row": None,
            "weakest_total_row": None,
        }
    weakest_share = min(
        rows, key=lambda row: row["positive_fraction_gap_vs_q46189"])
    weakest_total = min(rows, key=lambda row: row["total_gap_vs_q46189"])
    return {
        "row_count": len(rows),
        "minimum_positive_fraction_gap": (
            weakest_share["positive_fraction_gap_vs_q46189"]),
        "minimum_total_gap": weakest_total["total_gap_vs_q46189"],
        "weakest_positive_fraction_row": weakest_share,
        "weakest_total_row": weakest_total,
    }


def build_receipt():
    ledger = json.loads(SOURCE_LEDGER.read_text(encoding="utf-8"))
    parameters = scale_parameters(SCALE)
    row_count = parameters["row_count"]
    active_row_start = row_count
    lower = 50 * row_count + 1
    upper = 60 * row_count
    _, cells_by_denominator = _residue_cells_by_denominator(
        PRIME,
        row_count,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    original_replacement_qs = [
        row["reduced_denominator"]
        for row in ledger["replacement_one_coordinate_rows"]
    ]
    discovery_denominators = sorted(
        {DENOMINATOR, *original_replacement_qs})
    adverse_values, _diagonal = paired_distance_values(
        DENOMINATOR,
        cells_by_denominator[DENOMINATOR],
        row_count,
        active_row_start,
    )
    adverse_metric = band_metric(adverse_values, lower, upper)
    candidate_qs = [
        q for q in sorted(cells_by_denominator)
        if q not in discovery_denominators and q // 2 >= upper
    ]
    rows = []
    for q in candidate_qs:
        values, _diagonal = paired_distance_values(
            q, cells_by_denominator[q], row_count, active_row_start)
        rows.append(holdout_row(q, values, adverse_metric, lower, upper))

    failed_share = [
        row for row in rows
        if not row["passes_positive_fraction_separator"]
    ]
    failed_total = [
        row for row in rows if not row["passes_total_pressure_separator"]]
    failed_both = [
        row for row in rows
        if not row["passes_both_frozen_50A_to_60A_tests"]
    ]
    rows_by_share = sorted(
        rows, key=lambda row: row["positive_fraction_gap_vs_q46189"])
    rows_by_total = sorted(rows, key=lambda row: row["total_gap_vs_q46189"])
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_frozen_selector_unused_denominator_holdout",
        "source_one_coordinate_ledger": str(SOURCE_LEDGER),
        "source_selector_provenance_holdout": str(SOURCE_SELECTOR_HOLDOUT),
        "question": (
            "After freezing the post-hoc 50A..60A selector, does it survive "
            "same-source reduced denominators not used in the discovery "
            "replacement family?"),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": row_count,
            "active_row_start": active_row_start,
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "frozen_selector": "50A_to_60A",
            "frozen_distance_range": [lower, upper],
            "original_replacement_denominators": original_replacement_qs,
            "discovery_denominators_excluded": discovery_denominators,
        },
        "adverse_q46189_metric": adverse_metric,
        "unused_same_source_denominator_count": len(rows),
        "unused_same_source_denominators": candidate_qs,
        "all_rows": rows,
        "failure_summary": {
            "positive_fraction_failure_count": len(failed_share),
            "total_pressure_failure_count": len(failed_total),
            "both_test_failure_count": len(failed_both),
            "positive_fraction_failures": failed_share,
            "total_pressure_failures": failed_total,
            "both_test_failures": failed_both,
        },
        "weakest_rows": {
            "by_positive_fraction_gap": rows_by_share[:5],
            "by_total_gap": rows_by_total[:5],
        },
        "summary": finite_summary(rows),
        "classification": {
            "selector_was_frozen_before_this_holdout": True,
            "same_source_unused_denominator_stress_only": True,
            "fresh_source_admissible_conductor_theorem_proved": False,
            "frozen_selector_survives_all_unused_same_source_denominators": (
                len(failed_both) == 0),
            "frozen_selector_fails_at_least_one_unused_same_source_denominator": (
                len(failed_both) > 0),
            "counterexample_denominator_to_too_broad_selector_claim": (
                failed_both[0]["reduced_denominator"]
                if failed_both else None),
            "post_hoc_selector_demoted_without_admissibility_filter": (
                len(failed_both) > 0),
            "natural_selector_theorem_proved": False,
            "finite_diagnostic_only": True,
        },
        "candidate_next_action": {
            "name": "admissibility-filter or abandon 50A..60A as theorem lane",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The frozen block may be detecting a narrower conductor "
                "geometry of the original replacement family, not a universal "
                "same-source denominator law."),
            "prediction": (
                "A legitimate theorem route must either define a natural "
                "admissibility class excluding the failing denominator before "
                "testing, or abandon the 50A..60A selector as a general rule."),
            "falsifier": (
                "Any predeclared class that still contains denominator 16302 "
                "cannot claim the 50A..60A positive-share separator."),
            "smallest_next_test": (
                "Trace the original replacement construction exactly and ask "
                "whether denominator 16302 is reachable or unreachable under "
                "that construction."),
        },
        "decision": (
            "The frozen 50A..60A selector fails as a too-broad held-out "
            "same-source denominator rule.  Among 24 unused same-source "
            "denominators, q=16302 has positive-fraction gap "
            "-0.07517830702507916 versus Q=46189, even though its total "
            "pressure gap remains positive.  Therefore the selector remains "
            "post-hoc finite evidence unless a natural, predeclared "
            "admissibility filter excludes the failing denominator for "
            "structural reasons."),
        "finite_frozen_selector_holdout_audit_only": True,
        "finite_diagnostic_only": True,
        "natural_selector_theorem_proved": False,
        "fresh_conductor_holdout_proved": False,
        "distance_slice_positive_share_theorem_proved": False,
        "distance_slice_pressure_theorem_proved": False,
        "replacement_residue_gap_bound_theorem_proved": False,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    summary = receipt["summary"]
    failures = receipt["failure_summary"]
    weakest = summary["weakest_positive_fraction_row"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 frozen selector unused-denominator holdout",
        "",
        "## Question",
        "",
        "After freezing the post-hoc `50A..60A` selector, does it survive",
        "same-source reduced denominators that were not part of the original",
        "replacement-family discovery set?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_frozen_selector_unused_denominator_holdout.py",
        "evidence/mobius-moment-square-degree5-q46189-frozen-selector-unused-denominator-holdout.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"frozen selector:                     {receipt['fixture']['frozen_selector']}",
        f"distance range:                      {receipt['fixture']['frozen_distance_range']}",
        f"unused same-source denominators:     {receipt['unused_same_source_denominator_count']}",
        f"positive-fraction failures:          {failures['positive_fraction_failure_count']}",
        f"total-pressure failures:             {failures['total_pressure_failure_count']}",
        f"both-test failures:                  {failures['both_test_failure_count']}",
        f"minimum positive-fraction gap:       {summary['minimum_positive_fraction_gap']}",
        f"minimum total-pressure gap:          {summary['minimum_total_gap']}",
        f"weakest denominator:                 {weakest['reduced_denominator']}",
        f"weakest factorization:               {weakest['factorization']}",
        f"weakest positive fraction:           {weakest['metric']['positive_fraction_of_absolute']}",
        f"Q46189 positive fraction:            {receipt['adverse_q46189_metric']['positive_fraction_of_absolute']}",
        f"weakest total / diag:                {weakest['metric']['total_over_diagonal']}",
        f"Q46189 total / diag:                 {receipt['adverse_q46189_metric']['total_over_diagonal']}",
        "```",
        "",
        "## Decision",
        "",
        "The frozen selector fails as a too-broad same-source denominator rule.",
        "The denominator `16302 = 2*3*11*13*19` has a lower positive-fraction",
        "share than `Q=46189` in the frozen block.  Its total-pressure gap still",
        "clears, so this is a targeted failure of the positive-share separator,",
        "not a total-pressure failure.",
        "",
        "This demotes the natural-boundary story unless a structural admissibility",
        "filter is defined before looking at the test set.  A valid next step is",
        "to trace the original replacement construction and state whether",
        "`q=16302` is reachable or unreachable under that construction.  If it",
        "is reachable, the `50A..60A` selector cannot be a theorem lane in its",
        "current form.  If it is unreachable, the reason must be explicit and",
        "predeclared before testing any further held-out conductors.",
        "",
        "This proves no natural selector theorem, fresh-conductor theorem,",
        "distance-slice theorem, replacement residue-gap theorem, strict-central",
        "Goldbach theorem, or Goldbach proof.",
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
        "unused_same_source_denominator_count": (
            receipt["unused_same_source_denominator_count"]),
        "positive_fraction_failure_count": (
            receipt["failure_summary"]["positive_fraction_failure_count"]),
        "total_pressure_failure_count": (
            receipt["failure_summary"]["total_pressure_failure_count"]),
        "counterexample_denominator": (
            receipt["classification"][
                "counterexample_denominator_to_too_broad_selector_claim"]),
        "natural_selector_theorem_proved": (
            receipt["natural_selector_theorem_proved"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
