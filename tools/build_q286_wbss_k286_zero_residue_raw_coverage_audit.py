"""Audit raw-gap coverage of the K_286 no-reflection-discount residue.

The K_286 two-mode reflection/parity audit found that target residue
0 mod 286 is the unique checked residue whose combined two-mode burden is
essentially all reflection-even.  This receipt asks whether the current raw
adverse-drag calibration horizon actually samples that no-discount lane.

It does not prove or disprove the raw adverse-drag theorem.  It identifies a
necessary sublane of the universal theorem and checks whether existing finite
raw evidence covers it.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
REFLECTION_SOURCE = (
    EVIDENCE / "q286-wbss-k286-two-mode-reflection-parity-audit.json")
RAW_SOURCE = EVIDENCE / "q286-wbss-raw-adverse-drag-theorem-target.json"
OUT = EVIDENCE / "q286-wbss-k286-zero-residue-raw-coverage-audit.json"
NO_DISCOUNT_THRESHOLD = 0.95


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def finite_summary(values):
    vals = [float(value) for value in values
            if value is not None and math.isfinite(float(value))]
    if not vals:
        return {
            "count": 0,
            "minimum": None,
            "mean": None,
            "maximum": None,
        }
    return {
        "count": len(vals),
        "minimum": min(vals),
        "mean": math.fsum(vals) / len(vals),
        "maximum": max(vals),
    }


def summarize_raw_classes(rows):
    by_residue = {}
    for row in rows:
        by_residue.setdefault(int(row["target_mod_286"]), []).append(row)

    class_rows = []
    for residue, class_items in sorted(by_residue.items()):
        ratios = [
            row["raw_adverse_drag_ratio"]
            for row in class_items
            if row["raw_adverse_drag_ratio"] is not None
        ]
        gaps = [row["raw_adverse_gate_gap"] for row in class_items]
        gap_over_target = [
            row["raw_adverse_gate_gap"] / row["target"]
            for row in class_items
        ]
        class_rows.append({
            "target_mod_286": residue,
            "row_count": len(class_items),
            "target_minimum": min(row["target"] for row in class_items),
            "target_maximum": max(row["target"] for row in class_items),
            "raw_adverse_drag_ratio_summary": finite_summary(ratios),
            "raw_adverse_gate_gap_summary": finite_summary(gaps),
            "raw_adverse_gate_gap_over_target_summary": finite_summary(
                gap_over_target),
        })
    return by_residue, class_rows


def build_receipt():
    reflection = load_json(REFLECTION_SOURCE)
    raw = load_json(RAW_SOURCE)
    reflection_rows = reflection["combined_top_two_scaled"]["rows"]
    no_discount_rows = [
        row for row in reflection_rows
        if row["reflection_even_energy_fraction"] >= NO_DISCOUNT_THRESHOLD
    ]
    residue_zero_reflection = next(
        row for row in reflection_rows
        if row["target_residue_mod_286"] == 0)

    raw_rows = raw["finite_calibration"]["rows"]
    by_raw_residue, raw_class_rows = summarize_raw_classes(raw_rows)
    raw_zero_rows = by_raw_residue.get(0, [])
    sampled_residues = sorted(by_raw_residue)
    missing_no_discount_residues = [
        int(row["target_residue_mod_286"])
        for row in no_discount_rows
        if int(row["target_residue_mod_286"]) not in by_raw_residue
    ]
    highest_ratio_class = max(
        raw_class_rows,
        key=lambda row: row["raw_adverse_drag_ratio_summary"]["maximum"])
    tightest_gap_over_target_class = min(
        raw_class_rows,
        key=lambda row: row[
            "raw_adverse_gate_gap_over_target_summary"]["minimum"])

    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-zero-residue-raw-coverage-audit",
        "source_commit": source_commit(),
        "sources": {
            "reflection_parity_audit": str(
                REFLECTION_SOURCE.relative_to(ROOT)),
            "reflection_parity_source_commit": reflection["source_commit"],
            "raw_adverse_drag_theorem_target": str(
                RAW_SOURCE.relative_to(ROOT)),
            "raw_adverse_drag_source_commit": raw["source_commit"],
        },
        "status": "AUDIT_zero_residue_no_discount_lane_uncovered_by_raw_finite_calibration",
        "question": (
            "Does the current raw adverse-drag calibration horizon sample the "
            "K_286 target residue where reflection gives no two-mode discount?"),
        "answer": (
            "No.  Target residue 0 mod 286 is the unique combined two-mode "
            "reflection no-discount residue at threshold 0.95, with even "
            "energy fraction 1.0, but the 348-row raw adverse-drag finite "
            "calibration contains 0 rows with target_mod_286=0."),
        "no_discount_definition": {
            "threshold": NO_DISCOUNT_THRESHOLD,
            "quantity": (
                "combined scaled first-two-singular-mode reflection-even "
                "energy fraction"),
            "reason": (
                "A universal raw theorem must handle every even target "
                "residue.  The no-discount residue is a necessary sublane "
                "because the reflection-odd null identity does not reduce the "
                "two-mode burden there."),
        },
        "reflection_no_discount_residues": [
            {
                "target_mod_286": int(row["target_residue_mod_286"]),
                "reflection_even_energy_fraction": row[
                    "reflection_even_energy_fraction"],
                "reflection_odd_energy_fraction": row[
                    "reflection_odd_energy_fraction"],
                "centered_full_l2": row["centered_full_l2"],
                "reflection_even_l2": row["reflection_even_l2"],
                "reflection_odd_l2": row["reflection_odd_l2"],
                "reflection_even_linf": row["reflection_even_linf"],
                "reflection_odd_linf": row["reflection_odd_linf"],
            }
            for row in no_discount_rows
        ],
        "residue_zero_reflection_row": {
            "target_mod_286": 0,
            "reflection_even_energy_fraction": (
                residue_zero_reflection["reflection_even_energy_fraction"]),
            "reflection_odd_energy_fraction": (
                residue_zero_reflection["reflection_odd_energy_fraction"]),
            "centered_full_l2": residue_zero_reflection[
                "centered_full_l2"],
            "reflection_even_l2": residue_zero_reflection[
                "reflection_even_l2"],
            "reflection_odd_l2": residue_zero_reflection[
                "reflection_odd_l2"],
        },
        "raw_calibration_coverage": {
            "row_count": len(raw_rows),
            "sampled_mod_286_residue_count": len(sampled_residues),
            "sampled_mod_286_residues": sampled_residues,
            "zero_residue_raw_row_count": len(raw_zero_rows),
            "missing_no_discount_residues": missing_no_discount_residues,
            "raw_class_rows": raw_class_rows,
            "highest_raw_adverse_drag_ratio_class": highest_ratio_class,
            "tightest_gap_over_target_class": tightest_gap_over_target_class,
        },
        "necessary_subtheorem": {
            "statement": (
                "For every sufficiently large covered even N with "
                "N == 0 mod 286, prove A_raw_-(N) < L_raw(N), or prove an "
                "equivalent direct raw witness lower bound W_phi(N)>0."),
            "why_necessary": (
                "The full universal q286-WBSS raw theorem quantifies over "
                "every covered even target; residue 0 mod 286 is included "
                "and is the unique K_286 two-mode no-discount reflection lane."),
            "finite_calibration_status": (
                "No current raw calibration row samples target_mod_286=0, "
                "so current finite raw margins cannot calibrate or falsify "
                "this necessary sublane."),
        },
        "candidate": {
            "name": "zero-residue no-discount raw subtheorem",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Treat the unique reflection-even K_286 two-mode residue as "
                "a separate necessary raw theorem lane instead of averaging "
                "it into finite rows that do not sample it."),
            "prediction": (
                "If the K_286 obstruction is real, N == 0 mod 286 will either "
                "require a different analytic input or become the first place "
                "where a proposed universal raw bound fails."),
            "falsifier": (
                "If a targeted zero-residue raw horizon shows the same or "
                "larger margin as ordinary residues and no new coefficient "
                "pressure, then the no-discount lane is not a distinct next "
                "proof bottleneck."),
            "smallest_next_test": (
                "Build a zero-residue raw horizon or derive an analytic "
                "subtheorem for N == 0 mod 286; use it only as calibration or "
                "falsifier, not as acceptance."),
        },
        "decision": (
            "The universal raw adverse-drag theorem now has a sharper "
            "necessary sublane: N == 0 mod 286.  Existing raw finite "
            "calibration does not sample that lane, while K_286 reflection "
            "geometry says it is the unique no-discount two-mode residue.  "
            "Do not use the 348-row raw margin summary as evidence that the "
            "hard K_286 no-discount lane has been calibrated."),
        "status_boundary": (
            "Coverage audit and necessary-subtheorem locator only.  No "
            "zero-residue raw adverse-drag theorem, no universal pointwise "
            "raw estimate, no binary-prime moment theorem, no q286 threshold "
            "theorem, no strict-central Goldbach theorem, and no Goldbach "
            "proof is established."),
        "zero_residue_raw_adverse_drag_theorem_proved": False,
        "universal_pointwise_raw_bound_proved": False,
        "binary_prime_moment_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    coverage = receipt["raw_calibration_coverage"]
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "raw_row_count": coverage["row_count"],
        "zero_residue_raw_row_count": (
            coverage["zero_residue_raw_row_count"]),
        "missing_no_discount_residues": (
            coverage["missing_no_discount_residues"]),
        "no_discount_residue_count": len(
            receipt["reflection_no_discount_residues"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
