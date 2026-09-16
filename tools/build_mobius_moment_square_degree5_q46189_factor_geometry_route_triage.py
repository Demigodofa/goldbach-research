"""Triage factor geometry for the Q46189 kernel boundary.

The low-order bucket co-occurrence relaxation is too weak.  This receipt asks
whether the next non-post-hoc invariant should be a source/factor geometry
statement, and which simple factor signals are already ruled out.

The audit is deliberately finite: it summarizes the checked packet landscape,
tests scalar source-pair coefficient sorting as an explanatory shortcut, and
names the remaining theorem obligation as replacement-packet bucket
compensation rather than another fitted distance selector.
"""

from __future__ import annotations

import json
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_KERNEL = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-packet-kernel-sign-landscape-audit.json")
SOURCE_RATIO = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-packet-ratio-landscape-audit.json")
SOURCE_COOCCURRENCE = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-kernel-cooccurrence-relaxation-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-factor-geometry-route-triage.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-factor-geometry-route-triage.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_joined_rows():
    kernel = json.loads(SOURCE_KERNEL.read_text(encoding="utf-8"))
    ratio = json.loads(SOURCE_RATIO.read_text(encoding="utf-8"))
    ratio_by_q = {
        row["reduced_denominator"]: row for row in ratio["rows"]
    }
    rows = []
    for row in kernel["rows"]:
        q = row["reduced_denominator"]
        ratio_row = ratio_by_q[q]
        buckets = {
            bucket["bucket"]: bucket["contribution_over_diagonal_half"]
            for bucket in row["distance_bucket_contributions"]
        }
        rows.append({
            "reduced_denominator": q,
            "role": row["role"],
            "factorization": row["factorization"],
            "high_prime_support": row["high_prime_support"],
            "missing_high_primes": row["missing_high_primes"],
            "small_prime_support": row["small_prime_support"],
            "high_prime_support_count": len(row["high_prime_support"]),
            "missing_high_prime_count": len(row["missing_high_primes"]),
            "small_prime_support_count": len(row["small_prime_support"]),
            "off_diagonal_over_diagonal_half": (
                row["off_diagonal_over_diagonal_half"]),
            "ratio_minus_half": row["ratio_minus_half"],
            "off_diagonal_overpays_diagonal_half": (
                row["off_diagonal_overpays_diagonal_half"]),
            "raw_scalar_real": ratio_row["raw_scalar_real"],
            "ordered_source_conductor_pair_count": (
                ratio_row["ordered_source_conductor_pair_count"]),
            "ordered_source_conductor_pairs": (
                ratio_row["ordered_source_conductor_pairs"]),
            "bucket_vector": buckets,
        })
    return rows


def compact_row(row):
    return {
        "reduced_denominator": row["reduced_denominator"],
        "role": row["role"],
        "missing_high_primes": row["missing_high_primes"],
        "small_prime_support": row["small_prime_support"],
        "off_diagonal_over_diagonal_half": (
            row["off_diagonal_over_diagonal_half"]),
        "ratio_minus_half": row["ratio_minus_half"],
        "raw_scalar_real": row["raw_scalar_real"],
    }


def class_summary(rows, key_name, key_fn):
    groups = defaultdict(list)
    for row in rows:
        groups[key_fn(row)].append(row)
    output = []
    for key, members in sorted(groups.items(), key=lambda item: str(item[0])):
        weakest = min(
            members, key=lambda row: row["off_diagonal_over_diagonal_half"])
        strongest = max(
            members, key=lambda row: row["off_diagonal_over_diagonal_half"])
        output.append({
            key_name: key if not isinstance(key, tuple) else list(key),
            "row_count": len(members),
            "minimum_off_diagonal_row": compact_row(weakest),
            "maximum_off_diagonal_row": compact_row(strongest),
            "all_rows_keep_diagonal_surplus": all(
                row["off_diagonal_over_diagonal_half"] > -1.0
                for row in members),
        })
    return output


def build_receipt():
    rows = load_joined_rows()
    q_row = next(row for row in rows if row["reduced_denominator"] == 46189)
    nonadverse = [row for row in rows if row["reduced_denominator"] != 46189]
    weakest_nonadverse = min(
        nonadverse, key=lambda row: row["off_diagonal_over_diagonal_half"])

    scalar_false_positives = [
        row for row in nonadverse
        if row["raw_scalar_real"] <= q_row["raw_scalar_real"]
    ]
    most_negative_scalar = min(rows, key=lambda row: row["raw_scalar_real"])
    all_high_rows = [
        row for row in rows
        if row["high_prime_support_count"] == 4
        and row["small_prime_support_count"] == 0
    ]
    replacement_rows = [
        row for row in rows
        if row["high_prime_support_count"] < 4
        or row["small_prime_support_count"] > 0
    ]

    middle_bucket = "middle_A_to_10A"
    weakest_buckets = weakest_nonadverse["bucket_vector"]
    weakest_middle = weakest_buckets[middle_bucket]
    weakest_other_sum = sum(
        value for name, value in weakest_buckets.items()
        if name != middle_bucket)

    receipt = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_factor_geometry_route_triage",
        "source_packet_kernel_sign_landscape_audit": str(SOURCE_KERNEL),
        "source_packet_ratio_landscape_audit": str(SOURCE_RATIO),
        "source_kernel_cooccurrence_relaxation_audit": str(SOURCE_COOCCURRENCE),
        "question": (
            "After the 50A..60A selector is demoted and low-order bucket "
            "co-occurrence fails, which source/factor geometry signals remain "
            "useful for the Q46189 overpayment-exclusion route?"),
        "fixture": {
            "adverse_denominator": 46189,
            "target_bound": -1.0,
            "row_count": len(rows),
        },
        "q46189_row": compact_row(q_row),
        "weakest_nonadverse_row": compact_row(weakest_nonadverse),
        "all_high_factor_separator": {
            "all_high_no_small_row_count": len(all_high_rows),
            "all_high_no_small_rows": [compact_row(row) for row in all_high_rows],
            "replacement_row_count": len(replacement_rows),
            "all_replacement_rows_keep_diagonal_surplus": all(
                row["off_diagonal_over_diagonal_half"] > -1.0
                for row in replacement_rows),
            "finite_separator_observed": (
                len(all_high_rows) == 1
                and all_high_rows[0]["reduced_denominator"] == 46189),
        },
        "scalar_source_pair_coefficient_test": {
            "q46189_raw_scalar_real": q_row["raw_scalar_real"],
            "most_negative_raw_scalar_row": compact_row(most_negative_scalar),
            "nonadverse_rows_with_raw_scalar_at_most_q46189": [
                compact_row(row)
                for row in sorted(
                    scalar_false_positives,
                    key=lambda row: row["raw_scalar_real"])
            ],
            "false_positive_count": len(scalar_false_positives),
            "scalar_threshold_explains_boundary": (
                len(scalar_false_positives) == 0
                and most_negative_scalar["reduced_denominator"] == 46189),
        },
        "factor_class_summaries": {
            "by_missing_high_prime_set": class_summary(
                rows, "missing_high_primes",
                lambda row: tuple(row["missing_high_primes"])),
            "by_small_prime_support": class_summary(
                rows, "small_prime_support",
                lambda row: tuple(row["small_prime_support"])),
            "by_support_counts": class_summary(
                rows, "support_counts",
                lambda row: (
                    row["high_prime_support_count"],
                    row["small_prime_support_count"],
                )),
        },
        "weakest_replacement_compensation": {
            "denominator": weakest_nonadverse["reduced_denominator"],
            "missing_high_primes": weakest_nonadverse["missing_high_primes"],
            "small_prime_support": weakest_nonadverse["small_prime_support"],
            "bucket_vector": weakest_buckets,
            "middle_A_to_10A_contribution": weakest_middle,
            "sum_of_other_buckets": weakest_other_sum,
            "total_off_diagonal_over_diagonal_half": (
                weakest_nonadverse["off_diagonal_over_diagonal_half"]),
            "compensation_above_minus_one": (
                weakest_nonadverse["off_diagonal_over_diagonal_half"] + 1.0),
        },
        "classification": {
            "all_high_no_small_finite_separator_observed": (
                len(all_high_rows) == 1
                and all_high_rows[0]["reduced_denominator"] == 46189),
            "all_replacement_rows_keep_diagonal_surplus": all(
                row["off_diagonal_over_diagonal_half"] > -1.0
                for row in replacement_rows),
            "scalar_source_pair_coefficient_explanation_refuted": (
                len(scalar_false_positives) > 0
                and most_negative_scalar["reduced_denominator"] != 46189),
            "weakest_replacement_needs_bucket_compensation": (
                weakest_middle < -0.9 and weakest_other_sum > 0.0),
            "factor_geometry_triage_only": True,
            "finite_diagnostic_only": True,
        },
        "candidate_next_action": {
            "name": "replacement-packet bucket compensation theorem target",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use the natural replacement-packet geometry, not a fitted "
                "distance selector.  The finite separator is all-high/no-small "
                "versus replacement packets, but the tight replacement "
                "q=38038 survives only because adverse middle-band mass is "
                "compensated by the other buckets."),
            "prediction": (
                "A proof target should be a class-conditioned compensation "
                "inequality for replacement packets, beginning with the "
                "q=38038 missing-17 small-(2,7) packet, rather than a scalar "
                "source-pair coefficient or independent bucket caps."),
            "falsifier": (
                "A reachable replacement packet in the same natural class with "
                "middle-band loss and no compensating near/far/tail surplus "
                "would falsify this compensation route."),
            "smallest_next_test": (
                "Construct the exact symbolic bucket identity for q=38038 and "
                "compare it to Q=46189, tracking which source-conductor pair "
                "terms create the positive non-middle compensation."),
        },
        "decision": (
            "The all-high/no-small factor packet is the finite separator in "
            "this landscape, but that is only a route locator, not a theorem. "
            "A scalar source-pair coefficient does not explain the boundary: "
            "multiple nonadverse packets have raw scalar at least as negative "
            "as Q46189, and q=67830 is the most negative raw-scalar row while "
            "remaining far above the -1 kernel boundary.  The tight survivor "
            "q=38038 has a large middle-band loss around -0.94, compensated by "
            "the other buckets.  The next theorem-shaped target is therefore "
            "replacement-packet bucket compensation, starting with q=38038 "
            "versus Q46189."),
        "finite_factor_geometry_route_triage_only": True,
        "finite_diagnostic_only": True,
        "all_high_factor_separator_theorem_proved": False,
        "scalar_source_pair_coefficient_theorem_proved": False,
        "replacement_packet_compensation_theorem_proved": False,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }
    return receipt


def write_note(receipt):
    scalar = receipt["scalar_source_pair_coefficient_test"]
    separator = receipt["all_high_factor_separator"]
    comp = receipt["weakest_replacement_compensation"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 factor-geometry route triage",
        "",
        "## Question",
        "",
        "After the `50A..60A` selector is demoted and low-order bucket",
        "co-occurrence fails, which source/factor geometry signals remain",
        "useful for the `Q=46189` overpayment-exclusion route?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_factor_geometry_route_triage.py",
        "evidence/mobius-moment-square-degree5-q46189-factor-geometry-route-triage.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"row count:                                  {receipt['fixture']['row_count']}",
        f"all-high/no-small rows:                     {separator['all_high_no_small_row_count']}",
        f"replacement rows:                           {separator['replacement_row_count']}",
        f"all replacement rows keep surplus:          {separator['all_replacement_rows_keep_diagonal_surplus']}",
        f"Q=46189 raw scalar:                         {scalar['q46189_raw_scalar_real']}",
        f"raw-scalar false positives:                 {scalar['false_positive_count']}",
        f"most negative raw-scalar denominator:       {scalar['most_negative_raw_scalar_row']['reduced_denominator']}",
        f"most negative raw scalar:                   {scalar['most_negative_raw_scalar_row']['raw_scalar_real']}",
        f"weakest replacement denominator:            {comp['denominator']}",
        f"weakest replacement off/diag-half:          {comp['total_off_diagonal_over_diagonal_half']}",
        f"weakest middle A..10A contribution:         {comp['middle_A_to_10A_contribution']}",
        f"weakest non-middle compensation:            {comp['sum_of_other_buckets']}",
        f"weakest margin above -1:                    {comp['compensation_above_minus_one']}",
        "```",
        "",
        "## Decision",
        "",
        "The all-high/no-small factor packet is the finite separator in this",
        "landscape, but that is only a route locator, not a theorem.  It",
        "identifies the natural class split: the adverse packet is",
        "`11*13*17*19`, while the checked replacement packets contain small",
        "prime support.",
        "",
        "A scalar source-pair coefficient does not explain the boundary.",
        "Several nonadverse packets have raw scalar at least as negative as",
        "`Q=46189`; the most negative raw-scalar row is `q=67830`, which",
        "still stays far above the `-1` kernel boundary.",
        "",
        "The tight survivor `q=38038` is the useful theorem target.  It has a",
        "large adverse `middle_A_to_10A` contribution, but near/far/tail",
        "terms compensate enough to keep the total at",
        "`-0.8472931845861708`.  The next theorem-shaped route is therefore",
        "replacement-packet bucket compensation, beginning with symbolic",
        "`q=38038` versus `Q=46189` source-conductor terms.",
        "",
        "This is finite diagnostic evidence only.  It proves no factor",
        "separator theorem, scalar coefficient theorem, replacement-packet",
        "compensation theorem, strict-central Goldbach theorem, or Goldbach",
        "proof.",
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
        "raw_scalar_false_positive_count": (
            receipt["scalar_source_pair_coefficient_test"][
                "false_positive_count"]),
        "weakest_replacement_denominator": (
            receipt["weakest_replacement_compensation"]["denominator"]),
        "weakest_replacement_off_diagonal": (
            receipt["weakest_replacement_compensation"][
                "total_off_diagonal_over_diagonal_half"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
