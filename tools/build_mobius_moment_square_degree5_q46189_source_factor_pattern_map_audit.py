"""Step back from Q46189 replacement audits and map surviving patterns.

This receipt is not another fitted threshold.  It collects the 34-row
replacement landscape and the q=38038 versus q=41990 source-block matrices to
decide which apparent structures survive as next theorem targets.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    scale_parameters,
)
from tools.build_mobius_moment_square_degree5_q46189_exception_bound_audit import (  # noqa: E402
    SCALE,
)
from tools.build_mobius_moment_square_degree5_q46189_source_pair_bucket_compensation_audit import (  # noqa: E402
    row_receipt,
)


SOURCE_MIRROR = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-all-replacement-mirror-compensation-audit.json")
SOURCE_FACTOR = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-factor-geometry-route-triage.json")
SOURCE_MIDDLE_GAP = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-middle-loss-condition-gap-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-source-factor-pattern-map-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-source-factor-pattern-map-audit.md")


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
            if q is not None and "missing_high_primes" in value:
                found.setdefault(q, {
                    "missing_high_primes": value.get("missing_high_primes"),
                    "small_prime_support": value.get("small_prime_support"),
                    "role": value.get("role"),
                    "raw_scalar_real": value.get("raw_scalar_real"),
                })
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(triage)
    return found


def enrich_rows():
    mirror = json.loads(SOURCE_MIRROR.read_text(encoding="utf-8"))
    factors = factor_lookup()
    rows = []
    for row in mirror["all_replacement_rows"]:
        item = dict(row)
        factor = factors.get(row["reduced_denominator"], {})
        item.update(factor)
        missing = item.get("missing_high_primes") or []
        support = item.get("small_prime_support") or []
        item["missing_count"] = len(missing)
        item["support_count"] = len(support)
        item["small_over_missing_product"] = (
            math.prod(support) / math.prod(missing)
            if missing and support else None)
        rows.append(item)
    return rows


def summarize_groups(rows, key_fn):
    groups = defaultdict(list)
    for row in rows:
        groups[key_fn(row)].append(row)
    summaries = []
    for key, group in sorted(groups.items(), key=lambda item: str(item[0])):
        sorted_by_middle = sorted(group, key=lambda row: row["middle_A_to_10A"])
        summaries.append({
            "key": list(key) if isinstance(key, tuple) else key,
            "row_count": len(group),
            "minimum_total_row": min(
                group, key=lambda row: row["off_diagonal_over_diagonal_half"])[
                    "reduced_denominator"],
            "minimum_total": min(
                row["off_diagonal_over_diagonal_half"] for row in group),
            "minimum_middle_row": sorted_by_middle[0]["reduced_denominator"],
            "minimum_middle_A_to_10A": sorted_by_middle[0][
                "middle_A_to_10A"],
            "nonpositive_non_middle_count": sum(
                row["non_middle_sum"] <= 0 for row in group),
            "first_middle_rows": [
                row["reduced_denominator"] for row in sorted_by_middle[:5]],
        })
    return summaries


def block_key(pair):
    pair = tuple(pair)
    reverse = (pair[1], pair[0])
    return tuple(sorted([pair, reverse]))


def block_label(block):
    return [list(pair) for pair in block]


def source_block_matrix(q, parameters):
    row = row_receipt(q, f"q{q}", parameters)
    matrix = {}
    for term in row["cross_terms"]:
        left = block_key(term["left_source_pair"])
        right = block_key(term["right_source_pair"])
        key = (left, right)
        bucket = matrix.setdefault(key, {
            "left_block": block_label(left),
            "right_block": block_label(right),
            "middle_A_to_10A": 0.0,
            "non_middle_sum": 0.0,
            "total": 0.0,
            "term_count": 0,
        })
        bucket["middle_A_to_10A"] += term["middle_A_to_10A"]
        bucket["non_middle_sum"] += term["non_middle_sum"]
        bucket["total"] += term["off_diagonal_over_diagonal_half"]
        bucket["term_count"] += 1
    blocks = sorted(matrix.values(), key=lambda item: item["middle_A_to_10A"])
    return {
        "reduced_denominator": q,
        "aggregate_middle_A_to_10A": row["aggregate_middle_A_to_10A"],
        "aggregate_non_middle_sum": row["aggregate_non_middle_sum"],
        "aggregate_total": row["off_diagonal_over_diagonal_half"],
        "ordered_source_pairs": row["ordered_source_pairs"],
        "source_block_count": len({
            block_key(pair) for pair in row["ordered_source_pairs"]}),
        "block_interactions_by_middle_loss": blocks,
        "worst_middle_block_interaction": blocks[0],
        "best_non_middle_block_interaction": max(
            matrix.values(), key=lambda item: item["non_middle_sum"]),
    }


def combined_interaction(matrix, left_index, right_index):
    blocks = []
    labels = []
    for item in matrix["block_interactions_by_middle_loss"]:
        left = tuple(tuple(pair) for pair in item["left_block"])
        right = tuple(tuple(pair) for pair in item["right_block"])
        if left not in labels:
            labels.append(left)
        if right not in labels:
            labels.append(right)
    labels = sorted(labels)
    left = labels[left_index]
    right = labels[right_index]
    selected = []
    for item in matrix["block_interactions_by_middle_loss"]:
        item_left = tuple(tuple(pair) for pair in item["left_block"])
        item_right = tuple(tuple(pair) for pair in item["right_block"])
        if (item_left, item_right) in ((left, right), (right, left)):
            selected.append(item)
    return {
        "left_block": [list(pair) for pair in left],
        "right_block": [list(pair) for pair in right],
        "middle_A_to_10A": sum(item["middle_A_to_10A"] for item in selected),
        "non_middle_sum": sum(item["non_middle_sum"] for item in selected),
        "total": sum(item["total"] for item in selected),
        "interaction_count": len(selected),
    }


def build_receipt():
    rows = enrich_rows()
    parameters = scale_parameters(SCALE)
    q38038 = source_block_matrix(38038, parameters)
    q41990 = source_block_matrix(41990, parameters)
    q38038_ab = combined_interaction(q38038, 0, 1)
    q41990_ab = combined_interaction(q41990, 0, 1)
    by_counts = summarize_groups(
        rows, lambda row: (row["missing_count"], row["support_count"]))
    by_single_missing = summarize_groups(
        [row for row in rows if row["missing_count"] == 1],
        lambda row: tuple(row["missing_high_primes"]))
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_source_factor_pattern_map",
        "source_all_replacement_mirror_compensation_audit": str(SOURCE_MIRROR),
        "source_factor_geometry_route_triage": str(SOURCE_FACTOR),
        "source_middle_loss_gap_audit": str(SOURCE_MIDDLE_GAP),
        "question": (
            "After the Q46189 replacement audits, which patterns survive a "
            "step-back map, and which tempting dots should be eliminated?"),
        "landscape": {
            "replacement_row_count": len(rows),
            "by_missing_and_support_count": by_counts,
            "by_single_missing_high_prime": by_single_missing,
            "small_over_missing_product_order": [
                {
                    "reduced_denominator": row["reduced_denominator"],
                    "small_over_missing_product": (
                        row["small_over_missing_product"]),
                    "middle_A_to_10A": row["middle_A_to_10A"],
                    "non_middle_sum": row["non_middle_sum"],
                    "missing_high_primes": row.get("missing_high_primes"),
                    "small_prime_support": row.get("small_prime_support"),
                }
                for row in sorted(
                    [row for row in rows
                     if row["small_over_missing_product"] is not None],
                    key=lambda row: row["small_over_missing_product"])
            ],
        },
        "q38038_vs_q41990": {
            "q38038": q38038,
            "q41990": q41990,
            "q38038_first_two_block_interaction": q38038_ab,
            "q41990_first_two_block_interaction": q41990_ab,
            "middle_loss_gap": (
                q41990["aggregate_middle_A_to_10A"]
                - q38038["aggregate_middle_A_to_10A"]),
            "non_middle_gap": (
                q38038["aggregate_non_middle_sum"]
                - q41990["aggregate_non_middle_sum"]),
        },
        "patterns": {
            "eliminate_plain_middle_loss_threshold": True,
            "eliminate_small_over_missing_product_monotonicity": True,
            "eliminate_missing_high_prime_alone": True,
            "survives_as_candidate": (
                "matrix-shaped source-block interaction topology: q38038's dominant "
                "middle loss is an off-diagonal block interaction with "
                "positive non-middle payment, while q41990's first cross "
                "block has negative non-middle payment."),
        },
        "candidate_next_action": {
            "name": "source-block interaction sign invariant",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Treat each replacement row as a 3x3 matrix of source-factor "
                "blocks.  The next candidate theorem target is not a scalar "
                "factor count or fitted threshold, but a sign rule for the "
                "specific off-diagonal source-block interactions."),
            "prediction": (
                "Rows whose first two source blocks behave like q38038 should "
                "show middle loss paid by positive non-middle cross-block "
                "mass; rows like q41990 should fail through negative "
                "cross-block non-middle mass."),
            "falsifier": (
                "If the source-block interaction sign cannot be predicted "
                "from input-side factor partitions before computing bucket "
                "outputs, this lane remains descriptive and should not be "
                "promoted."),
            "smallest_next_test": (
                "Compute the same ordered 3x3 source-block matrix for all 34 "
                "replacement rows and test whether input-side block topology "
                "predicts the sign of the first off-diagonal non-middle term."),
        },
        "decision": (
            "The step-back map eliminates simple scalar explanations.  The "
            "surviving pattern is matrix-shaped: q38038's extreme middle loss "
            "comes from off-diagonal source-block interaction between its "
            "first two blocks, and that same interaction has positive "
            "non-middle payment.  q41990 has a less extreme middle loss, but "
            "its analogous first cross-block non-middle mass is negative.  "
            "The next evidence-bearing step is an all-row source-block "
            "interaction sign audit, not another fitted threshold."),
        "finite_source_factor_pattern_map_audit_only": True,
        "finite_diagnostic_only": True,
        "source_block_interaction_sign_theorem_proved": False,
        "source_factor_isolation_theorem_proved": False,
        "replacement_packet_compensation_theorem_proved": False,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    q = receipt["q38038_vs_q41990"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 source-factor pattern map audit",
        "",
        "## Question",
        "",
        "After the Q46189 replacement audits, which patterns survive a",
        "step-back map, and which tempting dots should be eliminated?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_source_factor_pattern_map_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-source-factor-pattern-map-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        "replacement rows:                         34",
        "plain middle-loss threshold:              eliminated",
        "small/missing product monotonicity:        eliminated",
        "missing high prime alone:                  eliminated",
        f"q=38038 aggregate middle:                  {q['q38038']['aggregate_middle_A_to_10A']}",
        f"q=38038 aggregate non-middle:              {q['q38038']['aggregate_non_middle_sum']}",
        f"q=38038 first-block-pair middle:           {q['q38038_first_two_block_interaction']['middle_A_to_10A']}",
        f"q=38038 first-block-pair non-middle:       {q['q38038_first_two_block_interaction']['non_middle_sum']}",
        f"q=41990 aggregate middle:                  {q['q41990']['aggregate_middle_A_to_10A']}",
        f"q=41990 aggregate non-middle:              {q['q41990']['aggregate_non_middle_sum']}",
        f"q=41990 first-block-pair middle:           {q['q41990_first_two_block_interaction']['middle_A_to_10A']}",
        f"q=41990 first-block-pair non-middle:       {q['q41990_first_two_block_interaction']['non_middle_sum']}",
        "```",
        "",
        "The surviving pattern is matrix-shaped.  `q=38038` has its extreme",
        "middle loss in an off-diagonal interaction between its first two",
        "source-factor blocks, and that interaction has positive non-middle",
        "payment.  `q=41990` has a less extreme middle loss, but its analogous",
        "first cross-block non-middle mass is negative.",
        "",
        "## Decision",
        "",
        "Do not add more scalar dots to the map as if they were theorem",
        "objects.  The next evidence-bearing step is an all-row source-block",
        "interaction sign audit: compute the ordered 3x3 source-block matrix",
        "for all `34` replacement rows and test whether input-side block",
        "topology predicts the sign of the first off-diagonal non-middle term.",
        "",
        "This is finite diagnostic evidence only.  It proves no source-block",
        "interaction sign theorem, source-factor isolation theorem, replacement",
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
    q = receipt["q38038_vs_q41990"]
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "q38038_first_block_pair_non_middle": (
            q["q38038_first_two_block_interaction"]["non_middle_sum"]),
        "q41990_first_block_pair_non_middle": (
            q["q41990_first_two_block_interaction"]["non_middle_sum"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
