"""Define the q286 signed support-tail control proof obligation.

This receipt is a theorem-shaping artifact, not a new broad scan.  It reads
the current q286 evidence and turns the last falsifier into the exact
principal-scaled inequalities that would be sufficient for the signed-witness
route to imply strict-central Goldbach after a finite check.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-signed-support-tail-control-definition.json"

KNOWN_EXTREMALS = EVIDENCE / "q286-three-support-known-extremals-audit.json"
CHARACTER_BURDEN = EVIDENCE / "q286-centered-character-burden-audit.json"
LOCAL_MAIN = EVIDENCE / "q286-local-main-term-positivity-audit.json"
LATER_TAIL_SOURCE = (
    EVIDENCE / "q286-later-tail-complement-source-decomposition.json")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def build_receipt():
    known = load_json(KNOWN_EXTREMALS)
    burden = load_json(CHARACTER_BURDEN)
    local = load_json(LOCAL_MAIN)
    later = load_json(LATER_TAIL_SOURCE)

    top_supports = tuple(known["top_three_support_labels"])
    tail_support_rows = [
        row for row in burden["support_rows"]
        if row["support_label"] not in top_supports
    ]
    top_three_energy = known["top_three_energy_fraction"]
    tail_energy = 1.0 - top_three_energy
    kill_targets = known["full_nonpositive_top_three_positive_targets"]
    rescue_targets = known["tail_changed_full_positive_targets"]
    pure_three_support_harmless_tail_falsified = (
        known["tail_changes_sign_decision_count"] > 0)
    tail_flip_orientation = (
        "negative_tail_kills_positive_principal_plus_top_three"
        if kill_targets and not rescue_targets else
        "mixed_or_rescue_tail_flips"
        if kill_targets or rescue_targets else
        "no_tail_sign_flips")

    local_metrics = {
        "even_residues_checked": local["even_target_residue_count"],
        "nonpositive_local_main_count": (
            local["nonpositive_local_main_term_count"]),
        "local_to_principal_ratio_minimum": (
            local["local_main_term_to_principal_ratio_summary"][
                "minimum"]),
        "local_to_principal_ratio_maximum": (
            local["local_main_term_to_principal_ratio_summary"][
                "maximum"]),
    }
    later_metrics = {
        "later_tail_target_count": later["target_count"],
        "principal_only_keeps_all_later_tail_rows_positive": (
            later["decision_metrics"][
                "principal_only_keeps_all_tail_rows_positive"]),
        "principal_only_minimum_margin": (
            later["decision_metrics"]["principal_only_minimum_margin"]),
        "nonprincipal_only_keeps_all_later_tail_rows_positive": (
            later["decision_metrics"][
                "nonprincipal_only_keeps_all_tail_rows_positive"]),
        "smallest_subset_without_principal_size": (
            later["decision_metrics"][
                "smallest_subset_without_principal_size"]),
    }

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "known_extremals": str(KNOWN_EXTREMALS.relative_to(ROOT)),
            "character_burden": str(CHARACTER_BURDEN.relative_to(ROOT)),
            "local_main": str(LOCAL_MAIN.relative_to(ROOT)),
            "later_tail_source": str(LATER_TAIL_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "theorem-definition and evidence-synthesis receipt only; no "
            "signed tail-control theorem, no q286 threshold theorem, no "
            "strict-central Goldbach theorem, and no Goldbach proof"),
        "question": (
            "After the pure three-support simplification failed on known "
            "extremals, what exact support-action inequalities remain "
            "Goldbach-relevant?"),
        "candidate_theorem": {
            "name": "q286 signed support-tail control",
            "novelty_label": "new-to-this-task",
            "objects": {
                "period": 10010,
                "action_decomposition": (
                    "A_N = P_N + D_N + R_N"),
                "principal": "P_N, the positive principal action",
                "dominant_support_action": (
                    "D_N = E_286(N)+E_154(N)+E_70(N)"),
                "tail_action": (
                    "R_N = E_14(N)+E_26(N)+E_130(N)+E_10(N)+E_22(N)"),
                "principal_scaled_form": (
                    "A_N/P_N = 1 + d_N + r_N"),
            },
            "sufficient_inequalities": [
                (
                    "dominant_margin: 1+d_N >= eta_a(N) > 0 for every "
                    "sufficiently large even N in residue a mod 10010"),
                (
                    "tail_lower_control: r_N > -eta_a(N), equivalently "
                    "R_N > -(P_N+D_N)"),
                (
                    "finite_remainder: directly verify the targets below "
                    "the threshold and any declared exceptional residues"),
            ],
            "goldbach_bridge": (
                "If A_N>0, then the strict-central weighted prime-pair mass "
                "T_N is positive, because no prime pairs would make every "
                "weighted signed action zero. Then N has a Goldbach pair."),
        },
        "evidence_inputs": {
            "top_three_support_labels": list(top_supports),
            "top_three_natural_moduli": (
                known["top_three_natural_moduli"]),
            "top_three_energy_fraction": top_three_energy,
            "tail_energy_fraction": tail_energy,
            "tail_support_rows": tail_support_rows,
            "local_main": local_metrics,
            "known_extremals": {
                "target_count": known["tested_target_count"],
                "full_action_positive_count": (
                    known["full_action_positive_count"]),
                "principal_plus_top_three_positive_count": (
                    known["principal_plus_top_three_positive_count"]),
                "tail_changes_sign_decision_count": (
                    known["tail_changes_sign_decision_count"]),
                "tail_flip_orientation": tail_flip_orientation,
                "negative_tail_kill_targets": kill_targets,
                "positive_tail_rescue_targets": rescue_targets,
                "fresh_holdout_cycle_minimum_tail_changes": (
                    known["source_summaries"][
                        "fresh_holdout_cycle_minimum"][
                            "tail_changes_sign_decision_count"]),
            },
            "later_tail_mode_decomposition": later_metrics,
        },
        "falsified_simplifications": [
            {
                "name": "ignore_support_tail_after_top_three",
                "status": "falsified_on_known_extremals",
                "reason": (
                    "The support tail changes 16 sign decisions on the "
                    "known-extremals fixture."),
            },
            {
                "name": "tail_as_rescue_on_known_extremals",
                "status": "wrong_sign_for_current_flips",
                "reason": (
                    "The observed support-tail flips are negative kills of "
                    "positive principal-plus-top-three partial sums; there "
                    "are zero positive-tail rescue flips in this receipt."),
            },
        ],
        "surviving_components": [
            {
                "name": "dominant_frequency_stress_skeleton",
                "status": "supported_as_compression_not_theorem",
                "reason": (
                    "The three dominant supports carry more than 99 percent "
                    "of centered coefficient energy and preserve the selected "
                    "10-row hard fixture, but not all known extremals."),
            },
            {
                "name": "later_principal_surplus_hint",
                "status": "supported_on_existing_later_tail_fixture",
                "reason": (
                    "On the existing 73 later tail rows, principal-only "
                    "margin stays positive, while nonprincipal-only does not. "
                    "This suggests a later inequality of the form "
                    "first-three/principal > -1 plus bounded nonprincipal "
                    "drag in that mode-level lane."),
            },
        ],
        "prediction": (
            "A future later-window support-action audit should show few or no "
            "negative-tail kills after the checked boundary failures.  If it "
            "does, the theorem can split into finite boundary verification "
            "plus an eventual signed tail-control bound."),
        "falsifier": (
            "Any predeclared later window with recurrent negative-tail kills "
            "near the current 16 early failures refutes a clean later "
            "tail-stable threshold and forces the tail into the main analytic "
            "correlation theorem at all ranges."),
        "smallest_next_test": (
            "Use the optimized row verifier to classify support-tail kill "
            "events on the already scanned positive suffix and one fresh "
            "later block, while keeping the theorem statement fixed before "
            "the scan."),
        "decision": (
            "Pivot from 'three supports plus negligible tail' to the exact "
            "principal-scaled inequalities 1+d_N>0 and r_N>-(1+d_N).  The "
            "tail is small in coefficient energy but mathematically decisive "
            "on known boundary failures."),
        "signed_support_tail_control_definition_written": True,
        "pure_three_support_harmless_tail_falsified": (
            pure_three_support_harmless_tail_falsified),
        "signed_tail_control_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    payload = build_receipt()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(json.dumps({
        "wrote": str(OUT.relative_to(ROOT)),
        "tail_flip_orientation": payload["evidence_inputs"][
            "known_extremals"]["tail_flip_orientation"],
        "tail_changes_sign_decision_count": payload["evidence_inputs"][
            "known_extremals"]["tail_changes_sign_decision_count"],
        "signed_tail_control_theorem_proved": (
            payload["signed_tail_control_theorem_proved"]),
        "goldbach_proved": payload["goldbach_proved"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
