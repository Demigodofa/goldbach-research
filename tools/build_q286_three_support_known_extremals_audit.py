"""Audit the q286 three-support reduction on known extremal rows.

This extends the selected hard-row decomposition to every currently recorded
raw-action failure plus cycle minima and fresh holdout minima.  It is still a
finite diagnostic: the result can shape a theorem target, but it cannot prove
Goldbach or any eventual signed-prime correlation estimate.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-three-support-known-extremals-audit.json"

sys.path.insert(0, str(ROOT / "tools"))

from build_q286_three_support_action_decomposition import (  # noqa: E402
    DEFAULT_TARGETS,
    build_receipt as build_action_decomposition,
    json_ready,
)


def finite_summary(values):
    values = tuple(float(value) for value in values)
    if not values:
        return {
            "count": 0,
            "minimum": None,
            "maximum": None,
            "mean": None,
        }
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def add_target(target_sources, target, source):
    target = int(target)
    target_sources.setdefault(target, set()).add(source)


def load_json(relative_path):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def collect_targets():
    target_sources = {}
    source_counts = {
        "census_nonpositive_raw_action": 0,
        "census_cycle_minimum": 0,
        "fresh_holdout_cycle_minimum": 0,
        "fresh_holdout_global_minimum": 0,
        "selected_hard_fixture": 0,
    }

    census = load_json("evidence/q286-raw-signed-witness-census.json")
    for cycle in census["cycle_rows"]:
        for target in cycle["negative_or_zero_targets"]:
            add_target(target_sources, target, "census_nonpositive_raw_action")
            source_counts["census_nonpositive_raw_action"] += 1
        add_target(
            target_sources,
            cycle["minimum_centered_to_principal_target"],
            "census_cycle_minimum",
        )
        source_counts["census_cycle_minimum"] += 1

    threshold = load_json(
        "evidence/q286-raw-signed-witness-threshold-holdout.json")
    fresh_holdout = threshold["fresh_holdout"]
    for row in fresh_holdout["cycle_minima"]:
        add_target(
            target_sources,
            row["target"],
            "fresh_holdout_cycle_minimum",
        )
        source_counts["fresh_holdout_cycle_minimum"] += 1
    add_target(
        target_sources,
        fresh_holdout["global_minimum_centered_to_principal_target"],
        "fresh_holdout_global_minimum",
    )
    source_counts["fresh_holdout_global_minimum"] += 1

    for target in DEFAULT_TARGETS:
        add_target(target_sources, target, "selected_hard_fixture")
        source_counts["selected_hard_fixture"] += 1

    return {
        "targets": tuple(sorted(target_sources)),
        "target_sources": {
            str(target): sorted(sources)
            for target, sources in sorted(target_sources.items())
        },
        "source_counts_before_deduplication": source_counts,
        "source_unique_counts": {
            source: sum(
                source in sources for sources in target_sources.values())
            for source in source_counts
        },
    }


def source_summary(rows, target_sources):
    by_source = {}
    for row in rows:
        for source in target_sources[str(row["target"])]:
            bucket = by_source.setdefault(source, [])
            bucket.append(row)
    return {
        source: {
            "target_count": len(source_rows),
            "full_action_positive_count": sum(
                row["direct_action_positive"] for row in source_rows),
            "principal_plus_top_three_positive_count": sum(
                row["principal_plus_top_three_positive"]
                for row in source_rows),
            "tail_changes_sign_decision_count": sum(
                row["tail_changes_sign_decision"] for row in source_rows),
            "nonpositive_full_targets": [
                row["target"] for row in source_rows
                if not row["direct_action_positive"]],
            "nonpositive_principal_plus_top_three_targets": [
                row["target"] for row in source_rows
                if not row["principal_plus_top_three_positive"]],
            "tail_centered_to_principal_ratio_summary": finite_summary(
                row["tail_centered_to_principal_ratio"]
                for row in source_rows),
            "top_three_centered_to_principal_ratio_summary": finite_summary(
                row["top_three_centered_to_principal_ratio"]
                for row in source_rows),
            "full_action_to_principal_ratio_summary": finite_summary(
                row["full_action_to_principal_ratio"] for row in source_rows),
        }
        for source, source_rows in sorted(by_source.items())
    }


def build_receipt():
    collected = collect_targets()
    decomposition = build_action_decomposition(targets=collected["targets"])
    rows = decomposition["rows"]
    target_sources = collected["target_sources"]
    tail_changed_full_positive = [
        row["target"] for row in rows
        if row["direct_action_positive"]
        and not row["principal_plus_top_three_positive"]
    ]
    full_nonpositive_top_three_positive = [
        row["target"] for row in rows
        if not row["direct_action_positive"]
        and row["principal_plus_top_three_positive"]
    ]
    source_rows = source_summary(rows, target_sources)
    sign_mismatch_count = decomposition["tail_changes_sign_decision_count"]
    all_known_decisions_preserved = sign_mismatch_count == 0
    decision = (
        "Three-support action reduction survives every known raw failure, "
        "cycle minimum, fresh holdout minimum, and selected hard row.  The "
        "proof obligation can prioritize E_286, E_154, and E_70 while "
        "retaining E_tail as an explicit secondary bound."
        if all_known_decisions_preserved else
        "The tail changes at least one known extremal sign decision; E_tail "
        "cannot be demoted to a secondary bound for this theorem route."
    )
    return {
        "schema_version": 1,
        "source_commit": decomposition["source_commit"],
        "arithmetic_period": decomposition["arithmetic_period"],
        "target_selection": {
            "rule": (
                "deduplicated union of all recorded census raw-action "
                "nonpositive targets, census cycle minima, fresh holdout "
                "cycle minima, the fresh global minimum, and the frozen "
                "selected hard fixture"),
            "target_count": len(collected["targets"]),
            "targets": collected["targets"],
            "target_sources": target_sources,
            "source_counts_before_deduplication": (
                collected["source_counts_before_deduplication"]),
            "source_unique_counts": collected["source_unique_counts"],
        },
        "top_three_support_labels": (
            decomposition["top_three_support_labels"]),
        "top_three_natural_moduli": (
            decomposition["top_three_natural_moduli"]),
        "top_three_energy_fraction": (
            decomposition["top_three_energy_fraction"]),
        "tested_target_count": decomposition["tested_target_count"],
        "full_action_positive_count": (
            decomposition["full_action_positive_count"]),
        "principal_plus_top_three_positive_count": (
            decomposition["principal_plus_top_three_positive_count"]),
        "tail_changes_sign_decision_count": sign_mismatch_count,
        "tail_changed_sign_targets": (
            decomposition["tail_changed_sign_targets"]),
        "tail_changed_full_positive_targets": tail_changed_full_positive,
        "full_nonpositive_top_three_positive_targets": (
            full_nonpositive_top_three_positive),
        "nonpositive_full_targets": (
            decomposition["nonpositive_full_targets"]),
        "nonpositive_principal_plus_top_three_targets": (
            decomposition["nonpositive_principal_plus_top_three_targets"]),
        "tail_centered_to_principal_ratio_summary": (
            decomposition["tail_centered_to_principal_ratio_summary"]),
        "top_three_centered_to_principal_ratio_summary": (
            decomposition["top_three_centered_to_principal_ratio_summary"]),
        "full_action_to_principal_ratio_summary": (
            decomposition["full_action_to_principal_ratio_summary"]),
        "centered_error_to_local_main_ratio_summary": (
            decomposition["centered_error_to_local_main_ratio_summary"]),
        "maximum_support_reconstruction_relative_error": (
            decomposition["maximum_support_reconstruction_relative_error"]),
        "source_summaries": source_rows,
        "candidate_curiosity_mechanism": {
            "name": "frequency stress skeleton",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Instead of treating the q286 heat map as 17 channel labels, "
                "test whether its action-level stress lives on the three "
                "dominant CRT Fourier supports 286, 154, and 70."),
            "prediction": (
                "Known failures and near-failures should keep the same sign "
                "after dropping the small centered tail."),
            "falsifier": (
                "Any known extremal target whose sign is changed by the tail "
                "shows that the tail must remain part of the main theorem."),
            "smallest_next_test": (
                "If this audit survives, run a full-block later-window "
                "version before attempting an analytic tail inequality."),
        },
        "decision": decision,
        "status_boundary": (
            "finite known-extremal support-action audit only; no pointwise "
            "signed-prime correlation theorem, no q286 threshold theorem, "
            "no strict-central Goldbach theorem, and no Goldbach proof"),
        "known_extremals_audit_measured": True,
        "all_known_extremal_sign_decisions_preserved_by_top_three": (
            all_known_decisions_preserved),
        "three_support_action_reduction_proved": False,
        "pointwise_centered_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(json_ready(receipt), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(json.dumps(json_ready({
        "wrote": str(OUT.relative_to(ROOT)),
        "tested_target_count": receipt["tested_target_count"],
        "full_action_positive_count": receipt["full_action_positive_count"],
        "principal_plus_top_three_positive_count": (
            receipt["principal_plus_top_three_positive_count"]),
        "tail_changes_sign_decision_count": (
            receipt["tail_changes_sign_decision_count"]),
        "tail_changed_sign_targets": receipt["tail_changed_sign_targets"],
        "all_known_extremal_sign_decisions_preserved_by_top_three": (
            receipt[
                "all_known_extremal_sign_decisions_preserved_by_top_three"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }), sort_keys=True))


if __name__ == "__main__":
    main()
