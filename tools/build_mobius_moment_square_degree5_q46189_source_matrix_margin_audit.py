"""Audit variable-size source-matrix input features against Q46189 row margin.

The source-block sign audit showed that the uniform 3x3 first-cross sign
object is not well-formed for all replacement rows.  This receipt tests a more
honest variable-size source-matrix question: do simple input-side matrix
features correlate strongly enough with row margin to justify a theorem target?
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SIGN = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-source-block-sign-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-source-matrix-margin-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-source-matrix-margin-audit.md")


MATRIX_FEATURES = {
    "block_count",
    "gap_sum",
    "gap_mean",
    "gap_min",
    "gap_max",
    "gap_range",
    "center_span",
    "small_span",
    "large_span",
    "pair_center_sum",
    "pair_center_mean",
    "pair_center_min",
    "pair_center_max",
    "pair_gapdiff_sum",
    "pair_gapdiff_mean",
    "pair_gapdiff_min",
    "pair_gapdiff_max",
    "pair_gap_product_sum",
    "pair_gap_product_mean",
    "tension_sum",
    "tension_max",
}


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def pearson(xs, ys):
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    var_x = sum((x - mean_x) ** 2 for x in xs)
    var_y = sum((y - mean_y) ** 2 for y in ys)
    if var_x == 0 or var_y == 0:
        return None
    return sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / math.sqrt(
        var_x * var_y)


def matrix_features(row):
    blocks = [tuple(block) for block in row["source_blocks"]]
    gaps = [right - left for left, right in blocks]
    centers = [(left + right) / 2 for left, right in blocks]
    small = [left for left, _ in blocks]
    large = [right for _, right in blocks]
    pairs = []
    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            pairs.append({
                "center_distance": abs(centers[i] - centers[j]),
                "gap_difference": abs(gaps[i] - gaps[j]),
                "gap_product": gaps[i] * gaps[j],
            })
    center_distances = [pair["center_distance"] for pair in pairs] or [0.0]
    gap_differences = [pair["gap_difference"] for pair in pairs] or [0.0]
    gap_products = [pair["gap_product"] for pair in pairs] or [0.0]
    tension_values = [
        pair["gap_difference"] / (1 + pair["center_distance"])
        for pair in pairs
    ] or [0.0]
    return {
        "block_count": len(blocks),
        "missing_count": len(row["missing_high_primes"]),
        "support_count": len(row["small_prime_support"]),
        "gap_sum": sum(gaps),
        "gap_mean": sum(gaps) / len(gaps),
        "gap_min": min(gaps),
        "gap_max": max(gaps),
        "gap_range": max(gaps) - min(gaps),
        "center_span": max(centers) - min(centers),
        "small_span": max(small) - min(small),
        "large_span": max(large) - min(large),
        "pair_center_sum": sum(center_distances),
        "pair_center_mean": sum(center_distances) / len(center_distances),
        "pair_center_min": min(center_distances),
        "pair_center_max": max(center_distances),
        "pair_gapdiff_sum": sum(gap_differences),
        "pair_gapdiff_mean": sum(gap_differences) / len(gap_differences),
        "pair_gapdiff_min": min(gap_differences),
        "pair_gapdiff_max": max(gap_differences),
        "pair_gap_product_sum": sum(gap_products),
        "pair_gap_product_mean": sum(gap_products) / len(gap_products),
        "tension_sum": sum(tension_values),
        "tension_max": max(tension_values),
    }


def correlations(rows, targets):
    feature_names = sorted({
        name for row in rows for name, value in row["input_features"].items()
        if isinstance(value, (int, float))
    })
    by_target = {}
    for target_name, values in targets.items():
        entries = []
        for feature in feature_names:
            xs = [row["input_features"][feature] for row in rows]
            value = pearson(xs, values)
            if value is not None:
                entries.append({
                    "feature": feature,
                    "pearson": value,
                    "abs_pearson": abs(value),
                    "is_matrix_feature": feature in MATRIX_FEATURES,
                })
        by_target[target_name] = sorted(
            entries,
            key=lambda item: (item["abs_pearson"], item["feature"]),
            reverse=True,
        )
    return by_target


def build_receipt():
    source = json.loads((ROOT / SOURCE_SIGN).read_text(encoding="utf-8"))
    rows = []
    for row in source["rows"]:
        margin = (
            1
            + row["aggregate_middle_A_to_10A"]
            + row["aggregate_non_middle_sum"])
        enriched = {
            "reduced_denominator": row["reduced_denominator"],
            "source_blocks": row["source_blocks"],
            "missing_high_primes": row["missing_high_primes"],
            "small_prime_support": row["small_prime_support"],
            "aggregate_middle_A_to_10A": row["aggregate_middle_A_to_10A"],
            "aggregate_non_middle_sum": row["aggregate_non_middle_sum"],
            "row_margin_above_failure": margin,
        }
        enriched["input_features"] = matrix_features(row)
        rows.append(enriched)
    targets = {
        "row_margin_above_failure": [
            row["row_margin_above_failure"] for row in rows],
        "aggregate_non_middle_sum": [
            row["aggregate_non_middle_sum"] for row in rows],
        "aggregate_middle_A_to_10A": [
            row["aggregate_middle_A_to_10A"] for row in rows],
    }
    by_target = correlations(rows, targets)
    best_by_target = {}
    best_matrix_by_target = {}
    for target, entries in by_target.items():
        best_by_target[target] = entries[0]
        matrix_entries = [
            entry for entry in entries if entry["is_matrix_feature"]]
        best_matrix_by_target[target] = matrix_entries[0]
    tight_rows = sorted(
        rows, key=lambda row: row["row_margin_above_failure"])[:8]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_source_matrix_margin",
        "source_block_sign_audit": str(SOURCE_SIGN),
        "question": (
            "After the first-off-diagonal sign invariant failed, do "
            "variable-size input-side source-matrix features correlate "
            "strongly enough with row margin to justify a theorem target?"),
        "row_count": len(rows),
        "targets": targets,
        "rows": rows,
        "correlations_by_target": by_target,
        "best_feature_by_target": best_by_target,
        "best_matrix_feature_by_target": best_matrix_by_target,
        "tightest_rows_by_margin": [
            {
                "reduced_denominator": row["reduced_denominator"],
                "row_margin_above_failure": row["row_margin_above_failure"],
                "aggregate_middle_A_to_10A": row["aggregate_middle_A_to_10A"],
                "aggregate_non_middle_sum": row["aggregate_non_middle_sum"],
                "block_count": row["input_features"]["block_count"],
                "tension_sum": row["input_features"]["tension_sum"],
                "gap_sum": row["input_features"]["gap_sum"],
                "center_span": row["input_features"]["center_span"],
            }
            for row in tight_rows
        ],
        "classification": {
            "strong_input_feature_margin_correlation_found": (
                best_by_target["row_margin_above_failure"]["abs_pearson"]
                >= 0.5),
            "strong_matrix_feature_margin_correlation_found": (
                best_matrix_by_target[
                    "row_margin_above_failure"]["abs_pearson"] >= 0.5),
            "source_matrix_margin_theorem_target_earned": False,
            "finite_source_matrix_margin_audit_only": True,
        },
        "decision": (
            "The variable-size source-matrix scan does not earn a theorem "
            "target.  The strongest simple input feature correlation with "
            "row margin is only "
            f"{best_by_target['row_margin_above_failure']['pearson']}, "
            "from "
            f"{best_by_target['row_margin_above_failure']['feature']}; "
            "the strongest genuine matrix-shape feature correlation with "
            "row margin is only "
            f"{best_matrix_by_target['row_margin_above_failure']['pearson']}, "
            "from "
            f"{best_matrix_by_target['row_margin_above_failure']['feature']}. "
            "This demotes the Q46189 source-matrix lane from theorem target "
            "to diagnostic/falsifier status until a changed invariant is "
            "predeclared."),
        "candidate_next_action": {
            "name": "return to q286 raw adverse-envelope margin",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The Q46189 source-matrix path has now killed scalar, "
                "first-sign, curvature, and simple full-matrix input feature "
                "targets.  The cross-lane atlas points back to a raw "
                "pointwise adverse-envelope inequality as the cleaner "
                "theorem-shaped object."),
            "prediction": (
                "A useful next receipt should define raw L_raw and E_raw,d "
                "quantities precisely enough to test whether the finite q286 "
                "component envelope was normalization-dependent."),
            "falsifier": (
                "If the raw quantities cannot be defined without importing "
                "unknown prime-pair mass, the q286 adverse-envelope route "
                "also remains conditional rather than a Goldbach bridge."),
            "smallest_next_test": (
                "Write the raw adverse-envelope definition audit for q286: "
                "separate which terms are genuinely raw, which still depend "
                "on T_N or mu_N, and what universal estimate would be needed."),
        },
        "finite_diagnostic_only": True,
        "source_matrix_margin_theorem_proved": False,
        "source_block_interaction_sign_theorem_proved": False,
        "source_factor_isolation_theorem_proved": False,
        "replacement_packet_compensation_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    best = receipt["best_feature_by_target"]["row_margin_above_failure"]
    best_matrix = receipt["best_matrix_feature_by_target"][
        "row_margin_above_failure"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 source-matrix margin audit",
        "",
        "## Question",
        "",
        "After the first-off-diagonal sign invariant failed, do variable-size",
        "input-side source-matrix features correlate strongly enough with row",
        "margin to justify a theorem target?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_source_matrix_margin_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-source-matrix-margin-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"replacement rows:                         {receipt['row_count']}",
        f"best input feature for row margin:         {best['feature']}",
        f"best input feature Pearson:                {best['pearson']}",
        f"best matrix feature for row margin:        {best_matrix['feature']}",
        f"best matrix feature Pearson:               {best_matrix['pearson']}",
        "strong input correlation threshold met:    no",
        "strong matrix correlation threshold met:   no",
        "```",
        "",
        "The strongest row-margin signal among these simple input features is",
        "weak.  More importantly, the strongest genuine source-matrix shape",
        "feature is weaker still.  This does not disprove the existence of a",
        "deeper source-matrix invariant, but it does block promotion of the",
        "current obvious variable-size features into a theorem target.",
        "",
        "## Decision",
        "",
        "Demote the Q46189 source-matrix lane to diagnostic/falsifier status",
        "until a changed invariant is predeclared.  The next theorem-shaped",
        "move should return to the q286 raw adverse-envelope margin and test",
        "whether its quantities can be defined without normalization or hidden",
        "dependence on unknown prime-pair mass.",
        "",
        "This is finite diagnostic evidence only.  It proves no source-matrix",
        "margin theorem, source-block interaction sign theorem, strict-central",
        "Goldbach theorem, or Goldbach proof.",
        "",
    ]
    NOTE.write_text("\n".join(lines), encoding="utf-8")


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    write_note(receipt)
    best = receipt["best_feature_by_target"]["row_margin_above_failure"]
    best_matrix = receipt["best_matrix_feature_by_target"][
        "row_margin_above_failure"]
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "best_margin_feature": best["feature"],
        "best_margin_pearson": best["pearson"],
        "best_matrix_margin_feature": best_matrix["feature"],
        "best_matrix_margin_pearson": best_matrix["pearson"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
