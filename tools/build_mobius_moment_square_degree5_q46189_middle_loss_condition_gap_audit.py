"""Audit whether tight middle-loss compensation is more than a singleton.

The all-replacement mirror audit refuted universal mirror-block positivity but
left a narrower candidate: q=38038 is the worst middle-loss row and still has
positive non-middle compensation.  This receipt tests the next danger: if the
"tight middle-loss" condition only selects q=38038 in the checked landscape,
then it is a locator, not yet a theorem-shaped condition.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MIRROR = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-all-replacement-mirror-compensation-audit.json")
SOURCE_FACTOR = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-factor-geometry-route-triage.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-middle-loss-condition-gap-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-middle-loss-condition-gap-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def factor_lookup():
    triage = json.loads(SOURCE_FACTOR.read_text(encoding="utf-8"))
    found = {}

    def walk(value):
        if isinstance(value, dict):
            q = value.get("reduced_denominator")
            if q is not None and q not in found:
                found[q] = {
                    "reduced_denominator": q,
                    "missing_high_primes": value.get("missing_high_primes"),
                    "small_prime_support": value.get("small_prime_support"),
                    "role": value.get("role"),
                    "raw_scalar_real": value.get("raw_scalar_real"),
                }
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(triage)
    return found


def compact_row(row, factors):
    q = row["reduced_denominator"]
    return {
        "reduced_denominator": q,
        "off_diagonal_over_diagonal_half": (
            row["off_diagonal_over_diagonal_half"]),
        "middle_A_to_10A": row["middle_A_to_10A"],
        "non_middle_sum": row["non_middle_sum"],
        "strongest_non_middle_mirror_block": (
            row["strongest_non_middle_mirror_block"]),
        "factor_geometry": factors.get(q),
    }


def pearson(rows, left_key, right_key):
    left = [row[left_key] for row in rows]
    right = [row[right_key] for row in rows]
    left_mean = sum(left) / len(left)
    right_mean = sum(right) / len(right)
    numerator = sum(
        (x - left_mean) * (y - right_mean)
        for x, y in zip(left, right))
    denominator = math.sqrt(
        sum((x - left_mean) ** 2 for x in left)
        * sum((y - right_mean) ** 2 for y in right))
    return numerator / denominator if denominator else None


def prefix_checks(sorted_by_middle):
    checks = []
    first_failure = None
    for k in range(1, len(sorted_by_middle) + 1):
        prefix = sorted_by_middle[:k]
        nonpositive = [
            row for row in prefix
            if row["non_middle_sum"] <= 0]
        check = {
            "prefix_size": k,
            "denominators": [
                row["reduced_denominator"] for row in prefix],
            "minimum_non_middle_sum": min(
                row["non_middle_sum"] for row in prefix),
            "nonpositive_non_middle_denominators": [
                row["reduced_denominator"] for row in nonpositive],
            "all_prefix_rows_have_positive_non_middle": (
                len(nonpositive) == 0),
        }
        if first_failure is None and nonpositive:
            first_failure = check
        if k <= 8 or k in (12, 17, len(sorted_by_middle)):
            checks.append(check)
    return checks, first_failure


def build_receipt():
    mirror = json.loads(SOURCE_MIRROR.read_text(encoding="utf-8"))
    factors = factor_lookup()
    rows = mirror["all_replacement_rows"]
    sorted_by_middle = sorted(rows, key=lambda row: row["middle_A_to_10A"])
    worst = sorted_by_middle[0]
    second = sorted_by_middle[1]
    prefix, first_failure = prefix_checks(sorted_by_middle)
    gap = second["middle_A_to_10A"] - worst["middle_A_to_10A"]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_middle_loss_condition_gap",
        "source_all_replacement_mirror_compensation_audit": str(SOURCE_MIRROR),
        "source_factor_geometry_route_triage": str(SOURCE_FACTOR),
        "question": (
            "Does the checked replacement landscape support a nontrivial "
            "middle-loss conditional compensation principle, or only the "
            "singleton q=38038 locator?"),
        "summary": {
            "replacement_row_count": len(rows),
            "worst_middle_loss_row": compact_row(worst, factors),
            "second_middle_loss_row": compact_row(second, factors),
            "middle_loss_isolation_gap": gap,
            "q38038_unique_worst_middle_loss": (
                worst["reduced_denominator"] == 38038),
            "smallest_middle_loss_prefix_failure": first_failure,
            "middle_loss_prefix_checks": prefix,
            "pearson_middle_loss_vs_non_middle_sum": pearson(
                rows, "middle_A_to_10A", "non_middle_sum"),
        },
        "classification": {
            "q38038_isolated_middle_loss_observed": (
                worst["reduced_denominator"] == 38038 and gap > 0),
            "middle_loss_threshold_compensation_singleton_only": (
                first_failure is not None
                and first_failure["prefix_size"] == 2),
            "any_two_row_middle_loss_condition_refuted": (
                first_failure is not None
                and first_failure["prefix_size"] == 2),
            "plain_middle_loss_monotonicity_refuted": (
                first_failure is not None),
            "source_factor_isolation_explanation_required": True,
            "finite_middle_loss_condition_gap_audit_only": True,
        },
        "candidate_next_action": {
            "name": "source-factor isolation theorem target",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "A middle-loss threshold broad enough to include even the "
                "second-worst row already includes q=41990, whose "
                "non-middle contribution is negative.  The checked target is "
                "therefore not monotone middle-loss compensation; it is the "
                "isolated source-factor geometry of q=38038."),
            "prediction": (
                "The next useful invariant should distinguish the "
                "missing-17 small-(2,7) packet q=38038 from the second "
                "middle-loss row q=41990, the missing-11 small-(2,5) packet, "
                "before it predicts compensation."),
            "falsifier": (
                "If a source-factor invariant cannot separate q=38038 from "
                "q=41990 without fitting to the observed output values, this "
                "conditional lane should sleep as a singleton locator."),
            "smallest_next_test": (
                "Compare the exact source-pair coordinate geometry of q=38038 "
                "and q=41990 and look for an input-side invariant explaining "
                "the 0.5077721983877355 middle-loss gap."),
        },
        "decision": (
            "The plain tight-middle-loss condition is not yet a nontrivial "
            "theorem target.  q=38038 is uniquely worst by middle loss and has "
            "positive non-middle compensation, but the prefix of the two worst "
            "middle-loss rows already fails because q=41990 has negative "
            "non-middle contribution.  The live target must shift from a "
            "middle-loss threshold to a source-factor isolation explanation "
            "for q=38038 versus q=41990."),
        "finite_middle_loss_condition_gap_audit_only": True,
        "finite_diagnostic_only": True,
        "middle_loss_compensation_theorem_proved": False,
        "source_factor_isolation_theorem_proved": False,
        "replacement_packet_compensation_theorem_proved": False,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    summary = receipt["summary"]
    worst = summary["worst_middle_loss_row"]
    second = summary["second_middle_loss_row"]
    first_failure = summary["smallest_middle_loss_prefix_failure"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 middle-loss condition gap audit",
        "",
        "## Question",
        "",
        "Does the checked replacement landscape support a nontrivial",
        "middle-loss conditional compensation principle, or only the singleton",
        "`q=38038` locator?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_middle_loss_condition_gap_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-middle-loss-condition-gap-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"replacement rows:                  {summary['replacement_row_count']}",
        f"worst middle-loss row:             {worst['reduced_denominator']}",
        f"worst middle A..10A:               {worst['middle_A_to_10A']}",
        f"worst non-middle sum:              {worst['non_middle_sum']}",
        f"second middle-loss row:            {second['reduced_denominator']}",
        f"second middle A..10A:              {second['middle_A_to_10A']}",
        f"second non-middle sum:             {second['non_middle_sum']}",
        f"middle-loss isolation gap:          {summary['middle_loss_isolation_gap']}",
        f"first prefix failure size:          {first_failure['prefix_size']}",
        f"first prefix failure denominator:   {first_failure['nonpositive_non_middle_denominators'][0]}",
        f"middle/non-middle Pearson:          {summary['pearson_middle_loss_vs_non_middle_sum']}",
        "```",
        "",
        "The second-worst middle-loss row is already a counterexample to a",
        "plain threshold principle: `q=41990` has negative non-middle",
        "contribution.  Thus the checked condition that works is singleton",
        "unless an input-side source-factor invariant explains why `q=38038`",
        "is isolated.",
        "",
        "## Decision",
        "",
        "The live target should not be a bare middle-loss threshold.  It must",
        "be a source-factor isolation explanation that distinguishes the",
        "missing-17 small-(2,7) packet `q=38038` from the missing-11",
        "small-(2,5) packet `q=41990` before making a compensation claim.",
        "",
        "This is finite diagnostic evidence only.  It proves no middle-loss",
        "compensation theorem, source-factor isolation theorem, replacement",
        "packet compensation theorem, strict-central Goldbach theorem, or",
        "Goldbach proof.",
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
    summary = receipt["summary"]
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "worst_middle_loss_row": summary["worst_middle_loss_row"][
            "reduced_denominator"],
        "second_middle_loss_row": summary["second_middle_loss_row"][
            "reduced_denominator"],
        "middle_loss_isolation_gap": summary["middle_loss_isolation_gap"],
        "first_prefix_failure_size": summary[
            "smallest_middle_loss_prefix_failure"]["prefix_size"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
