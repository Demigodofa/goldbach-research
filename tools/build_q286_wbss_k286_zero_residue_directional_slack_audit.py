"""Measure directional slack after the zero-residue L2 bridge fails.

The observed character-moment audit shows that plain aggregate active-
character L2 is not the zero-lane bridge: some rows exceed the sufficient L2
cap while the raw adverse gate remains positive.  This receipt measures how
much of the Cauchy L2 threat is actually realized as adverse drag.

Finite diagnostic only.  A small observed directional-efficiency ratio is a
candidate theorem target, not a theorem.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OBSERVED_SOURCE = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-observed-character-moment-audit.json")
OUT = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-directional-slack-audit.json")
TOLERANCE = 1e-12

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


def directional_row(row):
    cauchy_threat = row["ratio_to_zero_residue_local_l2_cap"]
    actual_adverse = row["raw_adverse_drag_ratio"]
    efficiency = (
        actual_adverse / cauchy_threat
        if cauchy_threat > TOLERANCE else None)
    overstatement = (
        cauchy_threat / actual_adverse
        if actual_adverse > TOLERANCE else None)
    return {
        "source": row["source"],
        "target": row["target"],
        "target_residue": row["target_residue"],
        "target_mod_286": row["target_mod_286"],
        "period_residue_index": row["period_residue_index"],
        "aggregate_character_moment_l2": (
            row["aggregate_character_moment_l2"]),
        "zero_residue_local_aggregate_l2_cap": (
            row["zero_residue_local_aggregate_l2_cap"]),
        "cauchy_l2_threat_ratio_to_local_main": cauchy_threat,
        "raw_adverse_drag_ratio_to_local_main": actual_adverse,
        "directional_efficiency_actual_over_cauchy": efficiency,
        "cauchy_overstatement_factor": overstatement,
        "cauchy_minus_actual_adverse_ratio": (
            cauchy_threat - actual_adverse),
        "raw_adverse_gate_gap_over_target": (
            row["raw_adverse_gate_gap_over_target"]),
        "exceeds_zero_residue_local_l2_cap": (
            row["exceeds_zero_residue_local_l2_cap"]),
        "raw_adverse_gate_gap_positive": (
            row["raw_adverse_gate_gap_positive"]),
        "character_moment_l2_by_modulus": (
            row["character_moment_l2_by_modulus"]),
    }


def summarize_rows(rows):
    violating = [
        row for row in rows if row["exceeds_zero_residue_local_l2_cap"]]
    nonviolating = [
        row for row in rows if not row["exceeds_zero_residue_local_l2_cap"]]
    positive_adverse = [
        row for row in rows
        if row["raw_adverse_drag_ratio_to_local_main"] > TOLERANCE]
    return {
        "row_count": len(rows),
        "local_l2_cap_exceeding_row_count": len(violating),
        "local_l2_cap_nonexceeding_row_count": len(nonviolating),
        "positive_raw_adverse_count": len(positive_adverse),
        "zero_raw_adverse_count": len(rows) - len(positive_adverse),
        "positive_raw_adverse_gate_gap_count": sum(
            row["raw_adverse_gate_gap_positive"] for row in rows),
        "cauchy_l2_threat_ratio_summary": finite_summary(
            row["cauchy_l2_threat_ratio_to_local_main"] for row in rows),
        "raw_adverse_drag_ratio_summary": finite_summary(
            row["raw_adverse_drag_ratio_to_local_main"] for row in rows),
        "directional_efficiency_summary": finite_summary(
            row["directional_efficiency_actual_over_cauchy"]
            for row in rows),
        "violating_l2_cap_directional_efficiency_summary": finite_summary(
            row["directional_efficiency_actual_over_cauchy"]
            for row in violating),
        "violating_l2_cap_cauchy_threat_summary": finite_summary(
            row["cauchy_l2_threat_ratio_to_local_main"]
            for row in violating),
        "violating_l2_cap_raw_adverse_ratio_summary": finite_summary(
            row["raw_adverse_drag_ratio_to_local_main"]
            for row in violating),
        "nonviolating_l2_cap_directional_efficiency_summary": finite_summary(
            row["directional_efficiency_actual_over_cauchy"]
            for row in nonviolating),
        "cauchy_minus_actual_adverse_ratio_summary": finite_summary(
            row["cauchy_minus_actual_adverse_ratio"] for row in rows),
        "largest_directional_efficiency_row": max(
            rows,
            key=lambda row: (
                row["directional_efficiency_actual_over_cauchy"],
                -row["target"])),
        "smallest_violating_directional_efficiency_row": min(
            violating,
            key=lambda row: (
                row["directional_efficiency_actual_over_cauchy"],
                row["target"])),
        "largest_l2_threat_violating_row": max(
            violating,
            key=lambda row: (
                row["cauchy_l2_threat_ratio_to_local_main"],
                -row["target"])),
        "largest_violating_raw_adverse_row": max(
            violating,
            key=lambda row: (
                row["raw_adverse_drag_ratio_to_local_main"],
                -row["target"])),
    }


def build_receipt():
    observed = load_json(OBSERVED_SOURCE)
    rows = [
        directional_row(row)
        for row in observed["finite_diagnostic"]["rows"]
    ]
    summary = summarize_rows(rows)
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-zero-residue-directional-slack-audit",
        "source_commit": source_commit(),
        "sources": {
            "observed_character_moment_audit": str(
                OBSERVED_SOURCE.relative_to(ROOT)),
            "observed_character_moment_source_commit": (
                observed["source_commit"]),
        },
        "status": "DIAGNOSTIC_zero_residue_directional_slack_observed",
        "question": (
            "When aggregate active-character L2 exceeds the sufficient "
            "zero-lane cap, how much of that Cauchy threat becomes actual "
            "raw adverse drag?"),
        "answer": (
            "Very little on the finite probe.  On the 18 cap-violating rows, "
            "actual raw adverse drag averages about 5.47% of the Cauchy L2 "
            "threat; the largest L2-threat row realizes about 1.85% of it."),
        "finite_diagnostic": {
            "finite_evidence_is_acceptance_condition": False,
            "role": (
                "directional diagnostic for the signed/phase-aware theorem "
                "target after the plain aggregate L2 bridge failed"),
            "formula": {
                "cauchy_l2_threat_ratio_to_local_main": (
                    "aggregate_character_moment_l2 / "
                    "zero_residue_local_aggregate_l2_cap"),
                "directional_efficiency_actual_over_cauchy": (
                    "raw_adverse_drag_ratio_to_local_main / "
                    "cauchy_l2_threat_ratio_to_local_main"),
            },
            "summary": summary,
            "rows": rows,
        },
        "candidate": {
            "name": "zero-residue coefficient-direction nonalignment bound",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Prove that the binary-prime character error vector has small "
                "projection onto the adverse WBSS coefficient direction even "
                "when its aggregate active-character L2 norm is not small "
                "enough for a blunt Cauchy payment."),
            "prediction": (
                "Large aggregate L2 rows can remain safe if their signed "
                "coefficient-direction efficiency stays bounded well below "
                "1/local Cauchy threat."),
            "falsifier": (
                "A sufficiently large row with both L2-threat ratio >= 1 and "
                "directional efficiency near 1 would collapse this mechanism "
                "back to the failed aggregate-L2 route."),
            "smallest_next_action": (
                "Decompose directional efficiency by modulus and character "
                "phase on the 18 L2-cap-violating rows."),
        },
        "decision": (
            "DIAGNOSTIC_zero_residue_directional_slack_observed.  The failed "
            "plain L2 bridge leaves a sharper possible route: prove a "
            "pointwise coefficient-direction nonalignment estimate, or a "
            "direct raw witness estimate.  The finite directional efficiencies "
            "are small, especially on the largest L2-threat row, but they are "
            "not a universal bound."),
        "status_boundary": (
            "Finite directional-slack diagnostic only.  No coefficient-"
            "direction nonalignment theorem, no signed/phase-aware character "
            "theorem, no universal pointwise raw bound, no q286 threshold "
            "theorem, no strict-central Goldbach theorem, and no Goldbach "
            "proof is established."),
        "coefficient_direction_nonalignment_theorem_proved": False,
        "signed_phase_character_theorem_proved": False,
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
        "row_count": summary["row_count"],
        "local_l2_cap_exceeding_row_count": (
            summary["local_l2_cap_exceeding_row_count"]),
        "violating_directional_efficiency_mean": summary[
            "violating_l2_cap_directional_efficiency_summary"]["mean"],
        "largest_l2_threat_target": summary[
            "largest_l2_threat_violating_row"]["target"],
        "largest_l2_threat_directional_efficiency": summary[
            "largest_l2_threat_violating_row"][
                "directional_efficiency_actual_over_cauchy"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
