"""Extract the q286 centered (3,1) signed-gap proof obligation.

The same-residue fresh-population audit shows selected deficit references are
below fresh targets after the identical local vector is subtracted. This
receipt converts that finite evidence into the exact inequality a theorem
would need to prove: within a fixed residue, the empirical (3,1) channel
value for future clear targets must stay above the selected stress reference.

Finite obligation extraction only: this proves no signed correlation theorem,
stress-class theorem, pointwise character-sum theorem, or Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-centered-3-1-signed-gap-obligation.json"

FRESH_POPULATION_SOURCE = (
    EVIDENCE
    / "q286-centered-3-1-same-residue-fresh-population-audit.json")
RESIDUE_COLLISION_SOURCE = (
    EVIDENCE / "q286-centered-3-1-residue-collision-audit.json")
REFERENCE_LEMMA_SOURCE = (
    EVIDENCE / "q286-centered-3-1-reference-lemma-audit.json")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def finite_summary(values):
    values = tuple(float(value) for value in values)
    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None}
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def main():
    fresh = load_json(FRESH_POPULATION_SOURCE)
    collision = load_json(RESIDUE_COLLISION_SOURCE)
    reference = load_json(REFERENCE_LEMMA_SOURCE)

    obligation_rows = []
    all_gap_rows = []
    for deficit_row in fresh["deficit_rows"]:
        deficit = deficit_row["deficit"]
        scope = deficit_row["scopes"][0]
        local_gaps = [
            float(row["local_gap"]) for row in scope["first_12_gap_rows"]]
        empirical_gaps = [
            float(row["empirical_gap_comparison_minus_deficit"])
            for row in scope["first_12_gap_rows"]]
        weighted_gaps = [
            float(row["weighted_gap_comparison_minus_deficit"])
            for row in scope["first_12_gap_rows"]]
        minimum_gap_row = min(
            scope["first_12_gap_rows"],
            key=lambda row: row["weighted_gap_comparison_minus_deficit"])
        all_gap_rows.extend(scope["first_12_gap_rows"])
        obligation_rows.append({
            "reference_target": deficit["target"],
            "reference_mod_143": deficit["target_mod_143"],
            "reference_mod_286": deficit["target_mod_286"],
            "reference_empirical_3_1_value": (
                deficit["empirical_channel_value"]),
            "reference_centered_3_1_value": (
                deficit["centered_channel_value"]),
            "reference_weighted_centered_3_1_value": (
                deficit["weighted_centered_channel_value"]),
            "fresh_same_residue_count": scope["comparison_count"],
            "local_gap_summary": finite_summary(local_gaps),
            "empirical_gap_summary": finite_summary(empirical_gaps),
            "weighted_gap_summary": finite_summary(weighted_gaps),
            "minimum_gap_row": minimum_gap_row,
            "finite_inequality_checked": (
                "for checked fresh targets T with T == R mod 143, "
                "empirical_3_1(T) - empirical_3_1(R) > 0; equivalently, "
                "centered_3_1(T) - centered_3_1(R) > 0 because the local "
                "gap is zero"),
            "all_checked_fresh_targets_satisfy": (
                scope["all_comparisons_above_deficit"]),
        })

    tightest = min(
        obligation_rows,
        key=lambda row: row["weighted_gap_summary"]["minimum"])

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_same_residue_fresh_population_audit": str(
            FRESH_POPULATION_SOURCE.relative_to(ROOT)),
        "source_same_residue_collision_audit": str(
            RESIDUE_COLLISION_SOURCE.relative_to(ROOT)),
        "source_reference_lemma_audit": str(
            REFERENCE_LEMMA_SOURCE.relative_to(ROOT)),
        "channel": [3, 1],
        "channel_key": "3,1",
        "status_boundary": (
            "finite signed-gap obligation extraction only; no signed "
            "correlation theorem, stress-class theorem, pointwise "
            "character-sum theorem, or Goldbach proof."),
        "mechanism": (
            "In same-residue comparisons modulo 143, the local q286 channel "
            "vector is identical. Therefore the centered (3,1) gap equals "
            "the empirical/correlation-side (3,1) gap, up to the fixed "
            "positive LP weight."),
        "theorem_obligation": (
            "For a non-post-hoc selected stress-reference family S and "
            "future targets T in the comparison family with T == R mod 143, "
            "prove empirical_3_1(T) - empirical_3_1(R) > 0 for every "
            "R in S, or prove a stronger residue-uniform lower bound that "
            "implies it."),
        "falsifier": (
            "Any same-residue fresh or future target T with weighted centered "
            "(3,1)(T) <= weighted centered (3,1)(R) for a selected stress "
            "reference R falsifies the corresponding finite or proposed "
            "uniform signed-gap claim."),
        "reference_lemma_selected_all_pass": (
            reference["selected_deficit_references_all_pass"]),
        "same_residue_collision_all_pairs_pass": (
            collision["same_residue_collision_all_pairs_pass"]),
        "same_residue_fresh_population_all_pass": (
            fresh["all_selected_deficits_pass_same_residue_fresh_population"]),
        "obligation_rows": obligation_rows,
        "checked_gap_count": len(all_gap_rows),
        "checked_reference_count": len(obligation_rows),
        "global_empirical_gap_summary": finite_summary(
            row["empirical_gap_comparison_minus_deficit"]
            for row in all_gap_rows),
        "global_weighted_gap_summary": finite_summary(
            row["weighted_gap_comparison_minus_deficit"]
            for row in all_gap_rows),
        "tightest_reference_target": tightest["reference_target"],
        "tightest_reference_mod_143": tightest["reference_mod_143"],
        "tightest_weighted_gap": tightest["weighted_gap_summary"]["minimum"],
        "tightest_empirical_gap": tightest["empirical_gap_summary"]["minimum"],
        "decision": (
            "The current theorem target is no longer a local-residue claim. "
            "It is a signed empirical/correlation gap claim for centered "
            "(3,1), with the tightest checked gate at reference 164598 and "
            "minimum weighted same-residue fresh gap about 0.00725833450694. "
            "The broad full_nonpositive classifier remains falsified."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
