"""Summarize the finite centered (3,1) stress-reference lemma status.

Kevin noticed that reference 13822 is strongly negative in centered (3,1).
This receipt consolidates the existing checked q286 evidence into one scoped
answer: centered (3,1) is supported as a selected-deficit-reference separator,
but the arbitrary-reference and broad full_nonpositive classifier promotions
are already falsified.

Finite evidence only: this proves no stress-class theorem, signed projection
theorem, binary-prime correlation theorem, or Goldbach theorem.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-centered-3-1-reference-lemma-audit.json"

CENTERED_SOURCE = EVIDENCE / "q286-centered-channel-scalar-order-audit.json"
ALTERNATE_REFERENCE_SOURCE = (
    EVIDENCE / "q286-alternate-reference-channel-audit.json")
STRESS_CLASS_SOURCE = EVIDENCE / "q286-centered-3-1-stress-class-audit.json"
PROVENANCE_SOURCE = EVIDENCE / "q286-selected-deficit-provenance-audit.json"

CHANNEL_KEY = "3,1"
FOCUS_REFERENCE = 13_822


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def channel_result(payload, label_key):
    return next(row for row in payload["channel_results"]
                if row["label_key"] == label_key)


def reference_watchlist_row(reference_result, label_key):
    return next(row for row in reference_result["watchlist_summary"]
                if row["label_key"] == label_key)


def stress_class_result(payload, label_key, class_id):
    result = channel_result(payload, label_key)
    return next(row for row in result["class_results"]
                if row["class_id"] == class_id)


def centered_rank_row(result, target):
    rows = (
        result["selected_deficit_reference_rank_rows"]
        + result["selected_clear_control_reference_rank_rows"]
    )
    return next(row for row in rows if row["target"] == target)


def reference_summary(row):
    watch = row["watchlist_3_1"]
    stats = watch["weighted_contribution_summary"]
    return {
        "reference": row["reference"],
        "reference_role": row["reference_role"],
        "reference_mod_143": row["reference_mod_143"],
        "singleton_passes_fresh_windows": (
            row["live_singleton_candidate_passes"][CHANNEL_KEY]),
        "positive_count": watch["positive_count"],
        "negative_count": watch["negative_count"],
        "minimum_weighted_margin": stats["minimum"],
        "average_weighted_margin": stats["mean"],
        "maximum_weighted_margin": stats["maximum"],
    }


def main():
    centered = load_json(CENTERED_SOURCE)
    alternate = load_json(ALTERNATE_REFERENCE_SOURCE)
    stress_class = load_json(STRESS_CLASS_SOURCE)
    provenance = load_json(PROVENANCE_SOURCE)

    centered_3_1 = channel_result(centered, CHANNEL_KEY)
    full_nonpositive = stress_class_result(
        stress_class, CHANNEL_KEY, "full_nonpositive")

    alternate_rows = []
    for reference_result in alternate["reference_results"]:
        watch = reference_watchlist_row(reference_result, CHANNEL_KEY)
        alternate_rows.append({
            **reference_result,
            "watchlist_3_1": watch,
        })

    selected_reference_rows = [
        reference_summary(row) for row in alternate_rows
        if row["reference_role"] == "selected_deficit_reference"
    ]
    clear_reference_rows = [
        reference_summary(row) for row in alternate_rows
        if row["reference_role"] == "selected_clear_control_reference"
    ]
    focus_centered = centered_rank_row(centered_3_1, FOCUS_REFERENCE)
    focus_provenance = next(
        row for row in provenance["selected_deficit_rows"]
        if row["target"] == FOCUS_REFERENCE)
    focus_alternate = next(
        row for row in selected_reference_rows
        if row["reference"] == FOCUS_REFERENCE)

    selected_all_pass = all(
        row["singleton_passes_fresh_windows"]
        and row["positive_count"] == alternate["target_count_per_reference"]
        and row["negative_count"] == 0
        for row in selected_reference_rows)
    clear_all_fail = all(
        not row["singleton_passes_fresh_windows"]
        for row in clear_reference_rows)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_centered_scalar_order_audit": str(
            CENTERED_SOURCE.relative_to(ROOT)),
        "source_alternate_reference_audit": str(
            ALTERNATE_REFERENCE_SOURCE.relative_to(ROOT)),
        "source_centered_3_1_stress_class_audit": str(
            STRESS_CLASS_SOURCE.relative_to(ROOT)),
        "source_selected_deficit_provenance_audit": str(
            PROVENANCE_SOURCE.relative_to(ROOT)),
        "channel": [3, 1],
        "channel_key": CHANNEL_KEY,
        "focus_reference": FOCUS_REFERENCE,
        "status_boundary": (
            "finite q286 receipt only; no stress-classifier theorem, "
            "selected-deficit classifier theorem, signed projection theorem, "
            "binary-prime correlation theorem, or Goldbach proof."),
        "mechanism": (
            "Compare fresh predeclared q286 targets against reference rows "
            "using the LP-weighted locally centered (3,1) coordinate. This "
            "removes the stored local residue vector before testing margins."),
        "candidate_lemma": (
            "Centered (3,1) is a selected-deficit stress-reference separator: "
            "fresh predeclared targets have positive (3,1) margin against "
            "each selected stable/volatile dominant-floor failure reference."),
        "prediction": (
            "If the lemma is only a selected-deficit stress-reference fact, "
            "(3,1) should pass all selected deficit references, fail arbitrary "
            "clear-control references, and fail a broader independent stress "
            "class unless that class has the same source predicate."),
        "falsifier": (
            "A selected deficit reference with any nonpositive fresh-window "
            "(3,1) margin falsifies the finite selected-reference lemma. A "
            "passing full_nonpositive class would be new evidence for a "
            "broader classifier, but the current broad-class audit fails."),
        "fresh_target_count_per_reference": (
            alternate["target_count_per_reference"]),
        "selected_deficit_reference_rows": selected_reference_rows,
        "selected_deficit_references_all_pass": selected_all_pass,
        "clear_control_reference_rows": clear_reference_rows,
        "clear_control_references_all_fail_singleton": clear_all_fail,
        "centered_scalar_order_summary": {
            "fresh_min_target": centered_3_1["minimum_fresh_row"]["target"],
            "fresh_min_weighted_centered_value": (
                centered_3_1["minimum_fresh_row"][
                    "weighted_centered_channel_value"]),
            "all_deficit_references_below_fresh_min": (
                centered_3_1[
                    "all_deficit_references_below_fresh_min"]),
            "all_clear_controls_below_fresh_min": (
                centered_3_1["all_clear_controls_below_fresh_min"]),
            "minimum_fresh_minus_max_deficit_weighted_gap": (
                centered_3_1[
                    "minimum_fresh_minus_max_deficit_weighted_gap"]),
            "minimum_fresh_minus_max_clear_control_weighted_gap": (
                centered_3_1[
                    "minimum_fresh_minus_max_clear_control_weighted_gap"]),
        },
        "focus_reference_13822": {
            "target_mod_143": focus_provenance["target_mod_143"],
            "dominant_margin_to_floor": (
                focus_provenance[
                    "selected_fixture_dominant_margin_to_floor"]),
            "stable_core_margin_to_floor": (
                focus_provenance["stable_core_margin_to_floor"]),
            "volatile_rim_sum_to_principal": (
                focus_provenance["volatile_rim_sum_to_principal"]),
            "centered_3_1_rank_low_to_high": (
                focus_centered["rank_low_to_high"]),
            "centered_3_1_weighted_value": (
                focus_centered["weighted_centered_channel_value"]),
            "fresh_min_gap_against_13822": (
                focus_alternate["minimum_weighted_margin"]),
            "fresh_positive_count": focus_alternate["positive_count"],
            "fresh_negative_count": focus_alternate["negative_count"],
        },
        "broad_full_nonpositive_class_falsifier": {
            "class_id": "full_nonpositive",
            "target_count": full_nonpositive["target_count"],
            "below_fresh_min_count": (
                full_nonpositive["below_fresh_min_count"]),
            "at_or_above_fresh_min_count": (
                full_nonpositive["at_or_above_fresh_min_count"]),
            "separator_passes_class": (
                full_nonpositive["separator_passes_class"]),
            "maximum_target": full_nonpositive["maximum_row"]["target"],
            "maximum_weighted_centered_value": (
                full_nonpositive["maximum_row"][
                    "weighted_centered_channel_value"]),
        },
        "decision": (
            "The finite selected-reference lemma is supported for centered "
            "(3,1), and 13822 is a strong selected stress witness. The broad "
            "full_nonpositive classifier and arbitrary-reference promotions "
            "are falsified by existing audits, so this receipt must not be "
            "promoted beyond selected stable/volatile dominant-floor failure "
            "references without a new non-post-hoc class or a new holdout."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
