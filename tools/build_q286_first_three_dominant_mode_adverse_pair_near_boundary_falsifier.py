"""Test the named q286 adverse pair as a simple near-boundary selector.

The surviving stress-row target is the six-versus-two adverse-pair absorption
balance around channels (1,7) and (4,4).  This receipt checks the tempting
shortcut that the named pair's sign or magnitude alone selects the tight
near-boundary deficit rows.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-rank5-template-near-boundary-falsifier.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-adverse-pair-near-boundary-falsifier.json")
ADVERSE_PAIR = ((1, 7), (4, 4))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set)):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def label_tuple(label):
    return tuple(int(part) for part in label)


def sign_label(value, tolerance=1e-12):
    if value > tolerance:
        return "positive"
    if value < -tolerance:
        return "negative"
    return "zero"


def summarize(values):
    values = tuple(float(value) for value in values)
    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None}
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": float(math.fsum(values) / len(values)),
    }


def pearson(left, right):
    left = tuple(float(value) for value in left)
    right = tuple(float(value) for value in right)
    if len(left) != len(right):
        raise ValueError("correlation inputs must have the same length")
    if not left:
        return math.nan
    left_mean = math.fsum(left) / len(left)
    right_mean = math.fsum(right) / len(right)
    left_delta = tuple(value - left_mean for value in left)
    right_delta = tuple(value - right_mean for value in right)
    denominator = math.sqrt(
        math.fsum(value * value for value in left_delta)
        * math.fsum(value * value for value in right_delta))
    if denominator == 0:
        return math.nan
    return math.fsum(
        a * b for a, b in zip(left_delta, right_delta)) / denominator


def compact_selector_row(row):
    return {
        "target": row["target"],
        "dominant_floor_passes": row["dominant_floor_passes"],
        "absolute_above_floor_signed_surplus": row[
            "absolute_above_floor_signed_surplus"],
        "adverse_pair_sum_to_principal": row[
            "adverse_pair_sum_to_principal"],
        "repair_complement_sum_to_principal": row[
            "repair_complement_sum_to_principal"],
        "adverse_pair_sign": row["adverse_pair_sign"],
        "adverse_pair_abs_share": row["adverse_pair_abs_share"],
        "adverse_pair_to_repair_complement_abs_ratio": row[
            "adverse_pair_to_repair_complement_abs_ratio"],
    }


def main():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    volatile_labels = tuple(label_tuple(label) for label in source[
        "volatile_labels"])
    adverse_pair = tuple(label_tuple(label) for label in ADVERSE_PAIR)
    if any(label not in volatile_labels for label in adverse_pair):
        raise AssertionError("adverse pair is not contained in volatile labels")

    row_records = []
    for row in source["row_records"]:
        channel_map = {
            label_tuple(item["label"]): float(
                item["contribution_to_principal_ratio"])
            for item in row["volatile_channel_vector"]
        }
        pair_sum = math.fsum(channel_map[label] for label in adverse_pair)
        complement_sum = math.fsum(
            value for label, value in channel_map.items()
            if label not in adverse_pair)
        abs_total = abs(pair_sum) + abs(complement_sum)
        near_row = row["near_boundary_row"]
        row_records.append({
            "target": int(row["target"]),
            "dominant_floor_passes": bool(row["dominant_floor_passes"]),
            "absolute_above_floor_signed_surplus": float(
                near_row["absolute_above_floor_signed_surplus"]),
            "above_floor_signed_surplus_to_threshold": float(
                near_row["above_floor_signed_surplus_to_threshold"]),
            "dominant_sum_to_principal": float(
                near_row["dominant_sum_to_principal"]),
            "adverse_pair": adverse_pair,
            "adverse_pair_sum_to_principal": pair_sum,
            "repair_complement_sum_to_principal": complement_sum,
            "volatile_total_sum_to_principal": pair_sum + complement_sum,
            "adverse_pair_sign": sign_label(pair_sum),
            "repair_complement_sign": sign_label(complement_sum),
            "adverse_pair_abs_share": (
                abs(pair_sum) / abs_total if abs_total else math.nan),
            "adverse_pair_to_repair_complement_abs_ratio": (
                pair_sum / abs(complement_sum)
                if abs(complement_sum) else math.nan),
        })

    deficit_rows = tuple(
        row for row in row_records if not row["dominant_floor_passes"])
    clear_rows = tuple(
        row for row in row_records if row["dominant_floor_passes"])
    positive_pair_rows = tuple(
        row for row in row_records
        if row["adverse_pair_sum_to_principal"] > 0)
    positive_pair_clear_rows = tuple(
        row for row in positive_pair_rows if row["dominant_floor_passes"])
    negative_pair_clear_rows = tuple(
        row for row in clear_rows
        if row["adverse_pair_sum_to_principal"] <= 0)

    threshold_sign_audits = {}
    for threshold, audit in source["threshold_sign_audits"].items():
        near_targets = tuple(int(target) for target in audit["near_targets"])
        selected = tuple(
            row for row in row_records if row["target"] in near_targets)
        signs = tuple(row["adverse_pair_sign"] for row in selected)
        positive_clear_count = sum(
            1 for row in selected
            if row["dominant_floor_passes"]
            and row["adverse_pair_sum_to_principal"] > 0)
        threshold_sign_audits[threshold] = {
            "near_threshold": float(threshold),
            "near_targets": near_targets,
            "adverse_pair_signs": signs,
            "mixed_signs_on_near_rows": bool(len(set(signs)) > 1),
            "positive_pair_clear_count": positive_clear_count,
            "rows": tuple(compact_selector_row(row) for row in selected),
        }

    stress = next(row for row in row_records if row["target"] == 1222142)
    if len(deficit_rows) != 1 or deficit_rows[0]["target"] != 1222142:
        raise AssertionError("top-20 deficit set drifted")
    if stress["adverse_pair_sum_to_principal"] <= 0:
        raise AssertionError("stress row no longer has positive adverse pair")
    if not positive_pair_clear_rows:
        raise AssertionError("adverse-pair sign selector stopped having clear false positives")
    if not any(row["target"] == 1242118 for row in positive_pair_clear_rows):
        raise AssertionError("tight clear row 1242118 no longer shares positive adverse pair")

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_rank5_template_falsifier": str(SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite adverse-pair near-boundary falsifier only; it refutes "
            "the named pair sign as a simple selector on the checked top-20 "
            "rows and proves no adverse-pair theorem, volatile-rim theorem, "
            "pointwise character-sum estimate, or Goldbach proof"),
        "candidate": (
            "The named stress pair (1,7),(4,4) might itself act as a simple "
            "near-boundary or deficit selector."),
        "mechanism": (
            "Reuse the exact top-20 signed q286 channel rows from the "
            "rank-5-template falsifier, sum the named pair (1,7),(4,4), "
            "compare it with the six-channel complement, and audit whether "
            "pair sign or pair magnitude isolates the tight deficit."),
        "prediction": (
            "If the named pair alone is the selector, positive adverse-pair "
            "sum or a narrow pair magnitude band should pick out 1222142 "
            "without also selecting nearby clear rows."),
        "falsifier": (
            "The shortcut fails if positive pair sum also occurs on nearby "
            "clears, especially the closest clear 1242118."),
        "novelty_label": "new-to-this-task",
        "arithmetic_modulus": source["arithmetic_modulus"],
        "support": source["support"],
        "source_top20_target_order": source["target_order"],
        "volatile_labels": volatile_labels,
        "adverse_pair": adverse_pair,
        "row_records": tuple(row_records),
        "sign_summary": {
            "deficit_count": len(deficit_rows),
            "clear_count": len(clear_rows),
            "positive_adverse_pair_count": len(positive_pair_rows),
            "positive_adverse_pair_clear_false_positive_count": len(
                positive_pair_clear_rows),
            "negative_or_zero_adverse_pair_clear_count": len(
                negative_pair_clear_rows),
            "positive_adverse_pair_targets": tuple(
                row["target"] for row in positive_pair_rows),
            "positive_adverse_pair_clear_false_positive_targets": tuple(
                row["target"] for row in positive_pair_clear_rows),
        },
        "adverse_pair_sum_summary": summarize(
            row["adverse_pair_sum_to_principal"] for row in row_records),
        "repair_complement_sum_summary": summarize(
            row["repair_complement_sum_to_principal"]
            for row in row_records),
        "adverse_pair_abs_share_summary": summarize(
            row["adverse_pair_abs_share"] for row in row_records),
        "correlations": {
            "pearson_abs_surplus_vs_adverse_pair_sum": pearson(
                (row["absolute_above_floor_signed_surplus"]
                 for row in row_records),
                (row["adverse_pair_sum_to_principal"]
                 for row in row_records)),
            "pearson_abs_surplus_vs_repair_complement_sum": pearson(
                (row["absolute_above_floor_signed_surplus"]
                 for row in row_records),
                (row["repair_complement_sum_to_principal"]
                 for row in row_records)),
            "pearson_abs_surplus_vs_adverse_pair_abs_share": pearson(
                (row["absolute_above_floor_signed_surplus"]
                 for row in row_records),
                (row["adverse_pair_abs_share"] for row in row_records)),
        },
        "threshold_sign_audits": threshold_sign_audits,
        "summary": {
            "selector_result": (
                "The named adverse pair is not a simple checked "
                "near-boundary deficit selector on the top-20 rows."),
            "tightest_rows": (
                "The tight deficit 1222142 and the closest clear 1242118 "
                "both have positive (1,7),(4,4) pair sum."),
            "false_positive_result": (
                "Positive adverse-pair sum selects the deficit but also "
                "six checked clear rows."),
        },
        "interpretation": {
            "hole_status": (
                "The q286 hole is tighter: the pair remains central to the "
                "stress-row absorption balance, but pair sign alone is not "
                "the theorem."),
            "route_status": (
                "Do not replace the six-versus-two adverse-pair absorption "
                "target with a pair-sign selector without a changed "
                "mechanism."),
            "remaining_theorem": (
                "Control the named pair together with the six-channel repair "
                "complement from actual binary-prime residue weights, or "
                "replace both with a stronger signed aggregate theorem."),
        },
        "adverse_pair_near_boundary_falsifier_measured": True,
        "adverse_pair_sign_simple_selector_refuted": True,
        "adverse_pair_sign_selector_theorem_proved": False,
        "volatile_threshold_theorem_proved": False,
        "volatile_rim_theorem_proved": False,
        "selected_fixture_classifier_theorem_proved": False,
        "pointwise_character_sum_estimate_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }

    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
