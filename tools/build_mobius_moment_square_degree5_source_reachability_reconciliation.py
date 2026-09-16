"""Reconcile source-window evidence after the puncture reachability audit.

The broad translated-row sweep has one finite failure at M=149, p=163,
start 1.  The reachability audit shows that start is not produced by the
original checked-scale source mapping.  This receipt combines the two facts so
future work does not keep treating an unreachable translated start as a source
window obstruction.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE_ADMISSIBLE = (
    EVIDENCE
    / "mobius-moment-square-degree5-source-admissible-window-audit.json")
REACHABILITY = (
    EVIDENCE
    / "mobius-moment-square-degree5-puncture-reachability-audit.json")
OUT = (
    EVIDENCE
    / "mobius-moment-square-degree5-source-reachability-reconciliation.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def failure_key(row):
    return (
        int(row["scale_modulus"]),
        int(row["prime_modulus"]),
        row["label"],
        int(row["active_row_start"]),
    )


def reachability_key(row):
    return (
        int(row["scale_modulus"]),
        int(row["prime_modulus"]),
        row["label"],
        int(row["failure_start"]),
    )


def build_receipt():
    source = load_json(SOURCE_ADMISSIBLE)
    reachability = load_json(REACHABILITY)
    reachability_by_key = {
        reachability_key(row): row
        for row in reachability["puncture_summaries"]
    }
    classified_failures = []
    for row in source["broad_failure_rows"]:
        key = failure_key(row)
        reachability_row = reachability_by_key.get(key)
        if reachability_row is None:
            reachability_label = "UNCLASSIFIED"
            source_reachable = None
        else:
            reachability_label = reachability_row["reachability"]
            source_reachable = bool(
                reachability_row["reachable_from_original_source_mapping"])
        classified_failures.append({
            "scale_modulus": row["scale_modulus"],
            "prime_modulus": row["prime_modulus"],
            "label": row["label"],
            "active_row_start": row["active_row_start"],
            "dominance_slack_above_one_half": (
                row["dominance_slack_above_one_half"]),
            "reachability": reachability_label,
            "reachable_from_original_source_mapping": source_reachable,
            "source_active_row_start": (
                reachability_row["canonical_source_start"]
                if reachability_row else None),
        })

    reachable_failures = [
        row for row in classified_failures
        if row["reachable_from_original_source_mapping"] is True
    ]
    unclassified_failures = [
        row for row in classified_failures
        if row["reachable_from_original_source_mapping"] is None
    ]
    unreachable_failures = [
        row for row in classified_failures
        if row["reachable_from_original_source_mapping"] is False
    ]
    source_start_pass_rows = [
        {
            "scale_modulus": row["scale_modulus"],
            "source_active_row_start": row["source_active_row_start"],
            "source_start_minimum_canonical_slack": (
                row["source_start_minimum_canonical_slack"]),
            "source_start_minimum_canonical_ratio": (
                row["source_start_minimum_canonical_ratio"]),
            "source_connected_passing_interval": (
                row["source_connected_passing_interval"]),
        }
        for row in source["scale_summaries"]
    ]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": (
            "RECONCILE_degree5_source_reachability_after_translated_puncture"),
        "question": (
            "After the start-1 puncture was proved unreachable from the "
            "original source mapping, what remains of the source-window lane?"),
        "sources": {
            "source_admissible_window_audit": str(
                SOURCE_ADMISSIBLE.relative_to(ROOT)),
            "source_admissible_window_status": source["status"],
            "puncture_reachability_audit": str(
                REACHABILITY.relative_to(ROOT)),
            "puncture_reachability_status": reachability["status"],
        },
        "broad_translated_quantifier_falsified": (
            source["broad_failure_row_count"] > 0),
        "broad_failure_count": source["broad_failure_row_count"],
        "classified_broad_failures": classified_failures,
        "reachable_source_failure_count": len(reachable_failures),
        "unreachable_translated_failure_count": len(unreachable_failures),
        "unclassified_failure_count": len(unclassified_failures),
        "all_broad_failures_are_unreachable": (
            bool(classified_failures)
            and not reachable_failures
            and not unclassified_failures),
        "source_scale_count": source["scale_count"],
        "all_source_starts_pass": source["all_source_starts_pass"],
        "source_start_failure_count": source["source_start_failure_count"],
        "source_start_pass_rows": source_start_pass_rows,
        "minimum_source_start_canonical_slack": (
            source["minimum_source_start_canonical_slack"]),
        "minimum_source_start_canonical_ratio": (
            source["minimum_source_start_canonical_ratio"]),
        "weakest_source_start_scale": source["weakest_source_start_scale"],
        "decision": (
            "The broad all-translated-start theorem remains finitely "
            "falsified, but the known failure is unreachable from the original "
            "source mapping.  The source-window lane therefore survives as a "
            "narrower theorem target: prove canonical source-start control, "
            "or define a non-post-hoc arithmetic admissibility map that "
            "separates reachable starts from unreachable translated starts.  "
            "Endpoint-swap or denominator-phase analysis of start 1 is "
            "reservoir evidence unless such a map makes start 1 "
            "source-admissible."),
        "candidate_next_theorem_target": {
            "name": (
                "canonical source-start active/full lower-frame control"),
            "mechanism": (
                "Use only the active row window produced by the original "
                "checked-scale source mapping, not every translated start in "
                "0..2A."),
            "prediction": (
                "A future valid source theorem should control the canonical "
                "start row on every scale; failures at unreachable translated "
                "starts do not refute it."),
            "falsifier": (
                "Any checked or proved reachable source start with active/full "
                "dominance slack <= 0, or a source-connected pass interval "
                "missing the canonical start, falsifies this narrowed lane."),
            "novelty_label": "new-to-this-task",
        },
        "finite_reconciliation_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_window_theorem_proved": False,
        "source_admissible_window_theorem_proved": False,
        "active_window_translation_theorem_proved": False,
        "endpoint_swap_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
    }


def main():
    receipt = build_receipt()
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
