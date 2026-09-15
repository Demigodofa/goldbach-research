"""Audit same-residue collisions for the centered q286 (3,1) signal.

The selected-reference lemma says centered (3,1) is low on selected deficit
references. This receipt checks whether that can be explained by the local
residue vector alone. When a selected deficit and selected clear share the
same target residue modulo 143, the local channel subtraction is identical;
any remaining centered (3,1) gap is therefore empirical/correlation-side.

Finite evidence only: this proves no stress-class theorem, signed correlation
theorem, pointwise character-sum theorem, or Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-centered-3-1-residue-collision-audit.json"

CENTERED_SOURCE = EVIDENCE / "q286-centered-channel-scalar-order-audit.json"
PROVENANCE_SOURCE = EVIDENCE / "q286-selected-deficit-provenance-audit.json"
REFERENCE_LEMMA_SOURCE = (
    EVIDENCE / "q286-centered-3-1-reference-lemma-audit.json")

CHANNEL_KEY = "3,1"


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


def channel_result(payload):
    return next(row for row in payload["channel_results"]
                if row["label_key"] == CHANNEL_KEY)


def role_rows(result):
    rows = []
    for row in result["selected_deficit_reference_rank_rows"]:
        rows.append({**row, "selected_role": "deficit"})
    for row in result["selected_clear_control_reference_rank_rows"]:
        rows.append({**row, "selected_role": "clear_control"})
    return rows


def group_by_residue(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[int(row["target_mod_143"])].append(row)
    return dict(sorted(grouped.items()))


def compact_row(row):
    return {
        "target": row["target"],
        "target_mod_143": row["target_mod_143"],
        "target_mod_286": row["target_mod_286"],
        "selected_role": row["selected_role"],
        "empirical_channel_value": row["empirical_channel_value"],
        "local_channel_delta_relative_to_base": (
            row["local_channel_delta_relative_to_base"]),
        "centered_channel_value": row["centered_channel_value"],
        "lp_weight": row["lp_weight"],
        "weighted_centered_channel_value": (
            row["weighted_centered_channel_value"]),
        "rank_low_to_high": row["rank_low_to_high"],
    }


def collision_summary(residue, rows):
    deficits = [row for row in rows if row["selected_role"] == "deficit"]
    clears = [row for row in rows if row["selected_role"] == "clear_control"]
    pair_rows = []
    for deficit in deficits:
        for clear in clears:
            weighted_gap_clear_minus_deficit = (
                clear["weighted_centered_channel_value"]
                - deficit["weighted_centered_channel_value"])
            centered_gap_clear_minus_deficit = (
                clear["centered_channel_value"]
                - deficit["centered_channel_value"])
            empirical_gap_clear_minus_deficit = (
                clear["empirical_channel_value"]
                - deficit["empirical_channel_value"])
            local_gap_clear_minus_deficit = (
                clear["local_channel_delta_relative_to_base"]
                - deficit["local_channel_delta_relative_to_base"])
            pair_rows.append({
                "residue_mod_143": residue,
                "deficit_target": deficit["target"],
                "clear_target": clear["target"],
                "same_residue_local_gap": local_gap_clear_minus_deficit,
                "empirical_gap_clear_minus_deficit": (
                    empirical_gap_clear_minus_deficit),
                "centered_gap_clear_minus_deficit": (
                    centered_gap_clear_minus_deficit),
                "weighted_gap_clear_minus_deficit": (
                    weighted_gap_clear_minus_deficit),
                "deficit_weighted_centered_value": (
                    deficit["weighted_centered_channel_value"]),
                "clear_weighted_centered_value": (
                    clear["weighted_centered_channel_value"]),
                "deficit_lower_than_clear": (
                    weighted_gap_clear_minus_deficit > 0),
            })
    return {
        "residue_mod_143": residue,
        "row_count": len(rows),
        "deficit_count": len(deficits),
        "clear_control_count": len(clears),
        "has_deficit_clear_collision": bool(deficits and clears),
        "rows": [compact_row(row) for row in rows],
        "pair_rows": pair_rows,
        "all_deficits_lower_than_same_residue_clears": (
            bool(pair_rows)
            and all(row["deficit_lower_than_clear"] for row in pair_rows)),
        "weighted_gap_summary": finite_summary(
            row["weighted_gap_clear_minus_deficit"] for row in pair_rows),
    }


def main():
    centered = load_json(CENTERED_SOURCE)
    provenance = load_json(PROVENANCE_SOURCE)
    reference_lemma = load_json(REFERENCE_LEMMA_SOURCE)

    result = channel_result(centered)
    rows = role_rows(result)
    grouped = group_by_residue(rows)
    residue_rows = [
        collision_summary(residue, group_rows)
        for residue, group_rows in grouped.items()
    ]
    collision_rows = [
        row for row in residue_rows if row["has_deficit_clear_collision"]]
    all_pairs = [
        pair
        for row in collision_rows
        for pair in row["pair_rows"]
    ]

    selected_deficits = tuple(
        int(row["target"])
        for row in provenance["selected_deficit_rows"])
    deficits_with_same_residue_clear = tuple(sorted({
        pair["deficit_target"] for pair in all_pairs
    }))
    deficits_without_same_residue_clear = tuple(
        target for target in selected_deficits
        if target not in deficits_with_same_residue_clear)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_centered_scalar_order_audit": str(
            CENTERED_SOURCE.relative_to(ROOT)),
        "source_selected_deficit_provenance_audit": str(
            PROVENANCE_SOURCE.relative_to(ROOT)),
        "source_reference_lemma_audit": str(
            REFERENCE_LEMMA_SOURCE.relative_to(ROOT)),
        "channel": [3, 1],
        "channel_key": CHANNEL_KEY,
        "status_boundary": (
            "finite same-residue selected-fixture audit only; no "
            "stress-classifier theorem, signed correlation theorem, "
            "pointwise character-sum theorem, or Goldbach proof."),
        "mechanism": (
            "For rows with the same target residue modulo 143, the stored "
            "local q286 channel vector is identical. Therefore the centered "
            "(3,1) gap between a selected deficit and selected clear at the "
            "same residue is not caused by local residue subtraction."),
        "prediction": (
            "If the selected-deficit (3,1) signal is more than a local "
            "residue artifact, selected deficits that collide with selected "
            "clear controls at the same residue should remain lower in "
            "centered (3,1), with zero local gap and positive empirical gap "
            "from clear to deficit."),
        "falsifier": (
            "A same-residue selected deficit whose centered (3,1) value is "
            "not lower than a same-residue selected clear falsifies this "
            "finite collision check. A selected deficit with no same-residue "
            "clear remains untested by this audit."),
        "selected_deficit_targets": selected_deficits,
        "selected_clear_control_targets": tuple(
            int(row["target"])
            for row in result["selected_clear_control_reference_rank_rows"]),
        "residue_rows": residue_rows,
        "collision_residue_count": len(collision_rows),
        "collision_pair_count": len(all_pairs),
        "deficits_with_same_residue_clear": (
            deficits_with_same_residue_clear),
        "deficits_without_same_residue_clear": (
            deficits_without_same_residue_clear),
        "same_residue_collision_all_pairs_pass": (
            bool(all_pairs)
            and all(row["deficit_lower_than_clear"] for row in all_pairs)),
        "same_residue_weighted_gap_summary": finite_summary(
            row["weighted_gap_clear_minus_deficit"] for row in all_pairs),
        "smallest_same_residue_weighted_gap_pair": (
            min(all_pairs,
                key=lambda row: row["weighted_gap_clear_minus_deficit"])
            if all_pairs else None),
        "largest_same_residue_weighted_gap_pair": (
            max(all_pairs,
                key=lambda row: row["weighted_gap_clear_minus_deficit"])
            if all_pairs else None),
        "reference_lemma_selected_all_pass": (
            reference_lemma["selected_deficit_references_all_pass"]),
        "decision": (
            "The same-residue selected-fixture collisions support the "
            "non-local reading: four of the five selected deficit references "
            "have selected clear controls at the same residue, and all such "
            "deficit-clear pairs remain separated in centered (3,1) after "
            "the identical local contribution is subtracted. Reference "
            "1222142 has no same-residue selected clear in this fixture and "
            "therefore remains outside this specific collision check."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
