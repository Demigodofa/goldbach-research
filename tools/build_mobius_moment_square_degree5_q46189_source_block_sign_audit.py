"""Audit all-row source-block interaction sign candidates for Q46189.

The preceding pattern map suggested testing whether input-side source-block
topology predicts the sign of the first off-diagonal non-middle interaction.
This receipt performs that all-row test and keeps the failed curvature baseline
visible.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
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
from tools.build_mobius_moment_square_degree5_q46189_source_factor_pattern_map_audit import (  # noqa: E402
    enrich_rows,
    source_block_matrix,
)


SOURCE_PATTERN_MAP = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-source-factor-pattern-map-audit.json")
SOURCE_SYNTHESIS = Path("evidence") / "goldbach-three-candidate-synthesis-audit.json"
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-source-block-sign-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-source-block-sign-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def sign(value):
    if value is None:
        return None
    if abs(value) < 1e-15:
        return 0
    return 1 if value > 0 else -1


def mirror_blocks(ordered_pairs):
    seen = []
    for a, b in ordered_pairs:
        u, v = sorted((a, b))
        if (u, v) not in seen:
            seen.append((u, v))
    return sorted(seen)


def first_off_diagonal(matrix):
    labels = []
    for item in matrix["block_interactions_by_middle_loss"]:
        for side in ("left_block", "right_block"):
            block = tuple(tuple(pair) for pair in item[side])
            if block not in labels:
                labels.append(block)
    labels = sorted(labels)
    if len(labels) < 2:
        return None
    left, right = labels[0], labels[1]
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


def row_features(row, parameters):
    q = row["reduced_denominator"]
    matrix = source_block_matrix(q, parameters)
    blocks = mirror_blocks(matrix["ordered_source_pairs"])
    gaps = [b - a for a, b in blocks]
    small = [a for a, _ in blocks]
    large = [b for _, b in blocks]
    interaction = first_off_diagonal(matrix)
    features = {
        "block_count": len(blocks),
        "missing_count": row["missing_count"],
        "support_count": row["support_count"],
        "small_over_missing_product": row.get("small_over_missing_product"),
    }
    if len(blocks) >= 2:
        features.update({
            "first_small": small[0],
            "second_small": small[1],
            "first_large": large[0],
            "second_large": large[1],
            "first_gap": gaps[0],
            "second_gap": gaps[1],
            "first_gap_drop": gaps[0] - gaps[1],
            "first_small_step": small[1] - small[0],
            "first_large_step": large[1] - large[0],
        })
    if len(blocks) == 3:
        features.update({
            "third_small": small[2],
            "third_large": large[2],
            "third_gap": gaps[2],
            "second_gap_drop": gaps[1] - gaps[2],
            "source_gap_curvature": gaps[0] - 2 * gaps[1] + gaps[2],
            "middle_gap_excess": gaps[1] - (gaps[0] + gaps[2]) / 2,
            "small_middle_offset": small[1] - (small[0] + small[2]) / 2,
            "large_middle_offset": large[1] - (large[0] + large[2]) / 2,
        })
    return {
        "reduced_denominator": q,
        "source_blocks": [list(block) for block in blocks],
        "source_gaps": gaps,
        "missing_high_primes": row.get("missing_high_primes") or [],
        "small_prime_support": row.get("small_prime_support") or [],
        "aggregate_middle_A_to_10A": row["middle_A_to_10A"],
        "aggregate_non_middle_sum": row["non_middle_sum"],
        "first_off_diagonal_interaction": interaction,
        "first_off_diagonal_non_middle_sign": (
            sign(interaction["non_middle_sum"]) if interaction else None),
        "features": features,
    }


def decision_stumps(rows):
    feature_names = sorted({
        name
        for row in rows
        for name, value in row["features"].items()
        if isinstance(value, (int, float)) and value is not None
    })
    best = []
    for name in feature_names:
        available = [
            row for row in rows
            if row["features"].get(name) is not None
            and row["first_off_diagonal_non_middle_sign"] in (-1, 1)
        ]
        values = sorted({row["features"][name] for row in available})
        if len(values) < 2:
            continue
        thresholds = [(a + b) / 2 for a, b in zip(values, values[1:])]
        for threshold in thresholds:
            for polarity in (1, -1):
                matched = 0
                mismatches = []
                for row in available:
                    value = row["features"][name]
                    predicted = 1 if polarity * value > polarity * threshold else -1
                    actual = row["first_off_diagonal_non_middle_sign"]
                    if predicted == actual:
                        matched += 1
                    else:
                        mismatches.append(row["reduced_denominator"])
                best.append({
                    "feature": name,
                    "threshold": threshold,
                    "polarity": polarity,
                    "rule": (
                        f"predict + if {name} "
                        f"{'>' if polarity == 1 else '<'} {threshold}"),
                    "valid_row_count": len(available),
                    "match_count": matched,
                    "mismatch_count": len(available) - matched,
                    "accuracy": matched / len(available),
                    "mismatch_denominators": mismatches,
                })
    return sorted(
        best,
        key=lambda item: (
            item["match_count"],
            item["accuracy"],
            -item["mismatch_count"],
            item["feature"],
        ),
        reverse=True,
    )


def curvature_baseline(rows):
    checked = []
    for row in rows:
        curvature = row["features"].get("source_gap_curvature")
        actual = row["first_off_diagonal_non_middle_sign"]
        if curvature is None or curvature == 0 or actual not in (-1, 1):
            continue
        predicted = -1 if curvature > 0 else 1
        checked.append({
            "reduced_denominator": row["reduced_denominator"],
            "source_gap_curvature": curvature,
            "predicted_sign": predicted,
            "actual_sign": actual,
            "matched": predicted == actual,
        })
    return {
        "valid_row_count": len(checked),
        "match_count": sum(row["matched"] for row in checked),
        "mismatch_count": sum(not row["matched"] for row in checked),
        "mismatch_denominators": [
            row["reduced_denominator"] for row in checked
            if not row["matched"]
        ],
    }


def build_receipt():
    parameters = scale_parameters(SCALE)
    rows = [row_features(row, parameters) for row in enrich_rows()]
    stumps = decision_stumps(rows)
    sign_counts = Counter(
        row["first_off_diagonal_non_middle_sign"] for row in rows)
    block_counts = Counter(row["features"]["block_count"] for row in rows)
    five_block_rows = [
        row["reduced_denominator"] for row in rows
        if row["features"]["block_count"] != 3
    ]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_source_block_sign",
        "source_pattern_map": str(SOURCE_PATTERN_MAP),
        "source_synthesis_audit": str(SOURCE_SYNTHESIS),
        "question": (
            "Across all 34 Q46189 replacement rows, can input-side "
            "source-block topology predict the sign of the first "
            "off-diagonal non-middle interaction?"),
        "row_count": len(rows),
        "source_block_count_distribution": dict(sorted(block_counts.items())),
        "non_three_block_rows": five_block_rows,
        "first_off_diagonal_sign_counts": {
            "positive": sign_counts[1],
            "negative": sign_counts[-1],
            "zero": sign_counts[0],
            "missing": sign_counts[None],
        },
        "curvature_baseline": curvature_baseline(rows),
        "best_single_feature_rules": stumps[:12],
        "best_rule": stumps[0],
        "tracked_rows": {
            str(q): next(row for row in rows if row["reduced_denominator"] == q)
            for q in (38038, 41990, 17290, 22610)
        },
        "rows": rows,
        "classification": {
            "all_rows_have_3x3_source_block_matrix": False,
            "source_gap_curvature_universal_sign_rule_falsified": True,
            "single_feature_input_side_sign_rule_established": (
                stumps[0]["mismatch_count"] == 0),
            "source_block_interaction_sign_theorem_proved": False,
            "finite_source_block_sign_audit_only": True,
        },
        "decision": (
            "The all-row audit does not establish an input-side sign rule.  "
            "The earlier 3x3 assumption fails on the checked landscape: "
            "32 rows have three source blocks, but rows 17290 and 22610 have "
            "five.  The failed source-gap curvature baseline remains failed "
            "with 13 matches and 19 mismatches on the 32 three-block rows.  "
            "The best single-feature input-side threshold reaches only "
            f"{stumps[0]['match_count']}/{stumps[0]['valid_row_count']} "
            "matches, so it is a weak finite classifier, not a theorem "
            "target.  The source-block matrix remains useful as a diagnostic "
            "object, but the first-off-diagonal sign invariant should not be "
            "promoted without a stronger variable-size matrix theorem."),
        "candidate_next_action": {
            "name": "variable-size source-block matrix invariant or sleep",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The correct object is not a uniform 3x3 first-cross sign "
                "rule over all replacement rows.  Any surviving theorem "
                "target must either restrict to a predeclared three-block "
                "subfamily or handle variable-size source-block matrices."),
            "prediction": (
                "A real invariant should predict a row-level matrix margin, "
                "not just the first off-diagonal sign, and should explain the "
                "five-block negative rows without fitting to bucket outputs."),
            "falsifier": (
                "If no input-side variable-size matrix statistic beats the "
                "weak single-feature stumps while preserving a predeclared "
                "falsifier, this Q46189 sign-invariant lane should sleep."),
            "smallest_next_test": (
                "Test a full-matrix input-side statistic against the signed "
                "row margin, using the best single-feature stump and failed "
                "curvature rule as baselines."),
        },
        "finite_diagnostic_only": True,
        "source_block_interaction_sign_theorem_proved": False,
        "source_factor_isolation_theorem_proved": False,
        "replacement_packet_compensation_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    best = receipt["best_rule"]
    curvature = receipt["curvature_baseline"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 source-block sign audit",
        "",
        "## Question",
        "",
        "Across all `34` Q46189 replacement rows, can input-side source-block",
        "topology predict the sign of the first off-diagonal non-middle",
        "interaction?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_source_block_sign_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-source-block-sign-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"replacement rows:                         {receipt['row_count']}",
        f"source-block count distribution:          {receipt['source_block_count_distribution']}",
        f"non-3x3 rows:                             {receipt['non_three_block_rows']}",
        f"first off-diagonal positive signs:        {receipt['first_off_diagonal_sign_counts']['positive']}",
        f"first off-diagonal negative signs:        {receipt['first_off_diagonal_sign_counts']['negative']}",
        f"curvature baseline matches:               {curvature['match_count']} / {curvature['valid_row_count']}",
        f"curvature baseline mismatches:            {curvature['mismatch_count']} / {curvature['valid_row_count']}",
        f"best single-feature rule:                 {best['rule']}",
        f"best single-feature matches:              {best['match_count']} / {best['valid_row_count']}",
        f"best single-feature mismatches:           {best['mismatch_count']} / {best['valid_row_count']}",
        "```",
        "",
        "The audit falsifies the uniform `3x3` premise for the whole",
        "replacement landscape: rows `17290` and `22610` have five source",
        "blocks.  On the `32` three-block rows, the source-gap curvature rule",
        "from the three-candidate synthesis audit remains mostly wrong.",
        "",
        "## Decision",
        "",
        "Do not promote a first-off-diagonal source-block sign invariant.  The",
        "best one-feature input-side threshold is only a weak finite",
        "classifier, and the original `3x3` object is not even well-formed for",
        "all checked rows.  The source-block matrix remains a useful diagnostic",
        "object, but any theorem-shaped next step must be a variable-size",
        "matrix invariant or a predeclared restriction to a genuine three-block",
        "subfamily.",
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
    OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    write_note(receipt)
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "row_count": receipt["row_count"],
        "block_count_distribution": receipt["source_block_count_distribution"],
        "curvature_matches": receipt["curvature_baseline"]["match_count"],
        "curvature_valid": receipt["curvature_baseline"]["valid_row_count"],
        "best_rule_matches": receipt["best_rule"]["match_count"],
        "best_rule_valid": receipt["best_rule"]["valid_row_count"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
