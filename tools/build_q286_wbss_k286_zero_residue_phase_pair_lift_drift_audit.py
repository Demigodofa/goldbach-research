"""Audit lift drift of K_286 phase pairs within repeated target residues.

The K_286 phase-pair audit falsified a single fixed conjugate-pair theorem.
This receipt asks the next smaller question: if the leading phase pairs move,
are they at least determined by the target residue modulo 10010 on the
finite zero-lane L2-violating rows?

Finite diagnostic only.  Two checked lifts of a residue class do not prove or
disprove an asymptotic target-residue theorem.
"""

from __future__ import annotations

import collections
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
PHASE_PAIR_SOURCE = (
    EVIDENCE / "q286-wbss-k286-zero-residue-k286-phase-pair-audit.json")
RAW_PROBE_SOURCE = (
    EVIDENCE / "q286-wbss-k286-zero-residue-raw-horizon-probe.json")
OUT = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-phase-pair-lift-drift-audit.json")

sys.path.insert(0, str(ROOT))

from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def phase_labels(row):
    return {
        "top_adverse_pair": (
            row["top_adverse_pair"]["pair_label"]
            if row["top_adverse_pair"] is not None else None),
        "top_rescue_pair": (
            row["top_rescue_pair"]["pair_label"]
            if row["top_rescue_pair"] is not None else None),
        "top_abs_pair": row["top_abs_pair"]["pair_label"],
    }


def row_record(row, raw_by_target):
    raw = raw_by_target[int(row["target"])]
    labels = phase_labels(row)
    return {
        "target": row["target"],
        "target_residue": row["target_residue"],
        "target_mod_286": row["target_mod_286"],
        "lift_index": raw["lift_index"],
        "block_index_after_raw_horizon": raw[
            "block_index_after_raw_horizon"],
        "k286_signed_error": row["k286_signed_error"],
        "k286_component_sign": (
            "adverse" if row["k286_component_is_adverse"]
            else "rescue" if row["k286_component_is_rescue"]
            else "zero"),
        "pair_real_cancellation_ratio": row[
            "pair_real_cancellation_ratio"],
        "top_abs_pair_fraction_of_envelope": row[
            "top_abs_pair_fraction_of_envelope"],
        **labels,
    }


def group_rows(rows):
    grouped = collections.defaultdict(list)
    for row in rows:
        grouped[int(row["target_residue"])].append(row)
    return {
        residue: sorted(items, key=lambda item: item["target"])
        for residue, items in grouped.items()
    }


def repeated_residue_record(residue, rows):
    top_adverse = {row["top_adverse_pair"] for row in rows}
    top_rescue = {row["top_rescue_pair"] for row in rows}
    top_abs = {row["top_abs_pair"] for row in rows}
    signs = {row["k286_component_sign"] for row in rows}
    return {
        "target_residue": residue,
        "row_count": len(rows),
        "targets": [row["target"] for row in rows],
        "lift_indices": [row["lift_index"] for row in rows],
        "rows": rows,
        "stable_top_adverse_pair": len(top_adverse) == 1,
        "stable_top_rescue_pair": len(top_rescue) == 1,
        "stable_top_abs_pair": len(top_abs) == 1,
        "stable_k286_component_sign": len(signs) == 1,
        "top_adverse_pairs": sorted(top_adverse),
        "top_rescue_pairs": sorted(top_rescue),
        "top_abs_pairs": sorted(top_abs),
        "k286_component_signs": sorted(signs),
        "cancellation_ratio_summary": finite_summary(
            row["pair_real_cancellation_ratio"] for row in rows),
        "top_abs_pair_fraction_summary": finite_summary(
            row["top_abs_pair_fraction_of_envelope"] for row in rows),
    }


def summarize_rows(rows):
    groups = group_rows(rows)
    repeated = [
        repeated_residue_record(residue, residue_rows)
        for residue, residue_rows in sorted(groups.items())
        if len(residue_rows) > 1
    ]
    singleton = [
        residue for residue, residue_rows in groups.items()
        if len(residue_rows) == 1
    ]
    return {
        "violating_row_count": len(rows),
        "distinct_target_residue_count": len(groups),
        "repeated_target_residue_count": len(repeated),
        "singleton_target_residue_count": len(singleton),
        "repeated_target_residue_rows": sum(
            row["row_count"] for row in repeated),
        "stable_top_adverse_pair_repeated_residue_count": sum(
            row["stable_top_adverse_pair"] for row in repeated),
        "stable_top_rescue_pair_repeated_residue_count": sum(
            row["stable_top_rescue_pair"] for row in repeated),
        "stable_top_abs_pair_repeated_residue_count": sum(
            row["stable_top_abs_pair"] for row in repeated),
        "stable_k286_component_sign_repeated_residue_count": sum(
            row["stable_k286_component_sign"] for row in repeated),
        "repeated_residue_records": repeated,
        "singleton_target_residues": sorted(singleton),
        "target_residue_alone_explains_top_adverse_pairs": all(
            row["stable_top_adverse_pair"] for row in repeated),
        "target_residue_alone_explains_top_rescue_pairs": all(
            row["stable_top_rescue_pair"] for row in repeated),
        "target_residue_alone_explains_top_abs_pairs": all(
            row["stable_top_abs_pair"] for row in repeated),
        "target_residue_alone_explains_k286_component_sign": all(
            row["stable_k286_component_sign"] for row in repeated),
    }


def build_receipt():
    phase_pair = load_json(PHASE_PAIR_SOURCE)
    raw_probe = load_json(RAW_PROBE_SOURCE)
    raw_by_target = {
        int(row["target"]): row
        for row in raw_probe["finite_probe"]["rows"]
    }
    rows = [
        row_record(row, raw_by_target)
        for row in phase_pair["finite_diagnostic"]["rows"]
    ]
    summary = summarize_rows(rows)
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-zero-residue-phase-pair-lift-drift-audit",
        "source_commit": source_commit(),
        "sources": {
            "k286_phase_pair_audit": str(
                PHASE_PAIR_SOURCE.relative_to(ROOT)),
            "k286_phase_pair_source_commit": phase_pair["source_commit"],
            "zero_residue_raw_horizon_probe": str(
                RAW_PROBE_SOURCE.relative_to(ROOT)),
            "zero_residue_raw_horizon_probe_source_commit": (
                raw_probe["source_commit"]),
        },
        "status": "DIAGNOSTIC_k286_phase_pair_residue_only_rule_falsified",
        "question": (
            "Among zero-lane L2-cap-violating rows with repeated target "
            "residues, are the leading K_286 phase pairs determined by the "
            "target residue alone?"),
        "answer": (
            "No.  Four target residues have two violating lifts.  Only one "
            "of those four residues keeps the same top adverse pair, none "
            "keeps the same top rescue pair, and only one keeps the same top "
            "absolute pair across the two lifts."),
        "finite_diagnostic": {
            "finite_evidence_is_acceptance_condition": False,
            "role": (
                "falsifier for a target-residue-only K_286 phase-pair rule; "
                "locator for lift-dependent or band-estimate theorem targets"),
            "summary": summary,
            "rows": rows,
        },
        "candidate": {
            "name": "lift-dependent K286 phase band estimate",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The leading K_286 phase-pair labels change even within the "
                "same target residue when the lift changes.  A useful theorem "
                "therefore likely needs height-sensitive oscillation or a "
                "band/envelope estimate across moving phase pairs."),
            "prediction": (
                "Adding more lifts for the repeated residue classes should "
                "continue to show pair drift unless a larger phase band, not "
                "a single pair, is tracked."),
            "falsifier": (
                "If a broader lift sample shows the top pairs eventually "
                "settle by residue class, this finite two-lift falsifier "
                "would be only a low-height transient."),
            "smallest_next_action": (
                "Extend only the four repeated violating residues by several "
                "additional lifts and measure whether a small phase band is "
                "stable while individual top pairs drift."),
        },
        "decision": (
            "DIAGNOSTIC_k286_phase_pair_residue_only_rule_falsified.  Target "
            "residue alone does not determine the leading K_286 phase pairs "
            "on the finite repeated-lift rows.  The next theorem target is a "
            "lift-sensitive phase-band estimate or an extended-lift falsifier, "
            "not a target-residue-only phase-pair rule."),
        "status_boundary": (
            "Finite repeated-lift phase-pair diagnostic only.  No lift-"
            "dependent phase theorem, no phase-band theorem, no coefficient-"
            "direction nonalignment theorem, no universal pointwise raw "
            "bound, no q286 threshold theorem, no strict-central Goldbach "
            "theorem, and no Goldbach proof is established."),
        "lift_dependent_phase_theorem_proved": False,
        "phase_band_theorem_proved": False,
        "coefficient_direction_nonalignment_theorem_proved": False,
        "universal_pointwise_raw_bound_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    summary = receipt["finite_diagnostic"]["summary"]
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "repeated_target_residue_count": (
            summary["repeated_target_residue_count"]),
        "stable_top_adverse_pair_repeated_residue_count": (
            summary["stable_top_adverse_pair_repeated_residue_count"]),
        "stable_top_rescue_pair_repeated_residue_count": (
            summary["stable_top_rescue_pair_repeated_residue_count"]),
        "stable_top_abs_pair_repeated_residue_count": (
            summary["stable_top_abs_pair_repeated_residue_count"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
