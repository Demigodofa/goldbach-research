"""Audit the q286 adverse-pair/complement plane near the tight boundary.

The direct adverse-pair sign selector failed.  This receipt checks whether
the coupled plane formed by the named pair (1,7),(4,4) and the six-channel
repair complement gives a stronger finite locator for the near-boundary hole.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-adverse-pair-near-boundary-falsifier.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pair-complement-plane-audit.json")
STRESS_TARGET = 1222142
TIGHT_CLEAR_TARGET = 1242118
EPSILONS = (0.0025, 0.005, 0.01, 0.02, 0.03, 0.05)
STRESS_RECTANGLES = (
    (0.005, 0.005),
    (0.01, 0.01),
    (0.02, 0.02),
    (0.03, 0.03),
    (0.05, 0.05),
    (0.01, 0.02),
    (0.02, 0.01),
    (0.01, 0.03),
    (0.03, 0.01),
)
TIGHT_TWO_PADS = (0.0, 0.005, 0.01, 0.02, 0.03, 0.05)
SCALAR_METRICS = (
    ("pair_sum", "adverse_pair_sum_to_principal"),
    ("complement_sum", "repair_complement_sum_to_principal"),
    ("volatile_total", "volatile_total_sum_to_principal"),
    ("pair_abs_share", "adverse_pair_abs_share"),
    ("pair_abs_to_complement_abs_ratio",
     "adverse_pair_to_repair_complement_abs_ratio"),
    ("absolute_above_floor_signed_surplus",
     "absolute_above_floor_signed_surplus"),
)


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


def compact_row(row):
    return {
        "target": int(row["target"]),
        "classification": (
            "clear" if row["dominant_floor_passes"] else "deficit"),
        "absolute_above_floor_signed_surplus": float(
            row["absolute_above_floor_signed_surplus"]),
        "adverse_pair_sum_to_principal": float(
            row["adverse_pair_sum_to_principal"]),
        "repair_complement_sum_to_principal": float(
            row["repair_complement_sum_to_principal"]),
        "volatile_total_sum_to_principal": float(
            row["volatile_total_sum_to_principal"]),
        "adverse_pair_abs_share": float(row["adverse_pair_abs_share"]),
        "adverse_pair_to_repair_complement_abs_ratio": float(
            row["adverse_pair_to_repair_complement_abs_ratio"]),
    }


def selector_record(rows, center, key, epsilon):
    selected = tuple(
        row for row in rows if abs(float(row[key]) - float(center[key]))
        <= epsilon)
    clear_targets = tuple(
        int(row["target"]) for row in selected if row["dominant_floor_passes"])
    deficit_targets = tuple(
        int(row["target"]) for row in selected
        if not row["dominant_floor_passes"])
    return {
        "epsilon": float(epsilon),
        "selected_count": len(selected),
        "deficit_targets": deficit_targets,
        "clear_false_positive_targets": clear_targets,
        "selected_targets": tuple(int(row["target"]) for row in selected),
    }


def stress_rectangle_record(rows, stress, pair_epsilon, complement_epsilon):
    selected = tuple(
        row for row in rows
        if abs(row["adverse_pair_sum_to_principal"]
               - stress["adverse_pair_sum_to_principal"]) <= pair_epsilon
        and abs(row["repair_complement_sum_to_principal"]
                - stress["repair_complement_sum_to_principal"])
        <= complement_epsilon)
    clear_targets = tuple(
        int(row["target"]) for row in selected if row["dominant_floor_passes"])
    deficit_targets = tuple(
        int(row["target"]) for row in selected
        if not row["dominant_floor_passes"])
    return {
        "pair_epsilon": float(pair_epsilon),
        "complement_epsilon": float(complement_epsilon),
        "selected_count": len(selected),
        "deficit_targets": deficit_targets,
        "clear_false_positive_targets": clear_targets,
        "selected_targets": tuple(int(row["target"]) for row in selected),
    }


def tight_two_rectangle_record(rows, stress, tight_clear, pad):
    pair_low, pair_high = sorted((
        stress["adverse_pair_sum_to_principal"],
        tight_clear["adverse_pair_sum_to_principal"]))
    complement_low, complement_high = sorted((
        stress["repair_complement_sum_to_principal"],
        tight_clear["repair_complement_sum_to_principal"]))
    selected = tuple(
        row for row in rows
        if pair_low - pad <= row["adverse_pair_sum_to_principal"]
        <= pair_high + pad
        and complement_low - pad <= row["repair_complement_sum_to_principal"]
        <= complement_high + pad)
    clear_targets = tuple(
        int(row["target"]) for row in selected if row["dominant_floor_passes"])
    deficit_targets = tuple(
        int(row["target"]) for row in selected
        if not row["dominant_floor_passes"])
    return {
        "pad": float(pad),
        "pair_low": float(pair_low - pad),
        "pair_high": float(pair_high + pad),
        "complement_low": float(complement_low - pad),
        "complement_high": float(complement_high + pad),
        "selected_count": len(selected),
        "deficit_targets": deficit_targets,
        "clear_false_positive_targets": clear_targets,
        "selected_targets": tuple(int(row["target"]) for row in selected),
    }


def main():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = tuple(source["row_records"])
    stress = next(row for row in rows if row["target"] == STRESS_TARGET)
    tight_clear = next(
        row for row in rows if row["target"] == TIGHT_CLEAR_TARGET)
    deficit_rows = tuple(
        row for row in rows if not row["dominant_floor_passes"])
    clear_rows = tuple(row for row in rows if row["dominant_floor_passes"])
    if tuple(int(row["target"]) for row in deficit_rows) != (STRESS_TARGET,):
        raise AssertionError("top-20 deficit set drifted")
    if not tight_clear["dominant_floor_passes"]:
        raise AssertionError("tight clear target drifted")

    scalar_neighborhoods = {}
    for metric_name, key in SCALAR_METRICS:
        records = tuple(
            selector_record(rows, stress, key, epsilon)
            for epsilon in EPSILONS)
        scalar_neighborhoods[metric_name] = {
            "stress_value": float(stress[key]),
            "records": records,
            "first_false_positive_epsilon": next(
                (record["epsilon"] for record in records
                 if record["clear_false_positive_targets"]),
                None),
            "stress_isolated_epsilons": tuple(
                record["epsilon"] for record in records
                if record["selected_targets"] == (STRESS_TARGET,)),
        }

    stress_rectangles = tuple(
        stress_rectangle_record(rows, stress, pair_eps, complement_eps)
        for pair_eps, complement_eps in STRESS_RECTANGLES)
    tight_two_rectangles = tuple(
        tight_two_rectangle_record(rows, stress, tight_clear, pad)
        for pad in TIGHT_TWO_PADS)

    tight_two_base_rectangle = tight_two_rectangles[0]
    first_stress_rectangle_false_positive = next(
        (record for record in stress_rectangles
         if record["clear_false_positive_targets"]),
        None)
    if first_stress_rectangle_false_positive is None:
        raise AssertionError(
            "stress-centered rectangles no longer show false positives")
    if TIGHT_CLEAR_TARGET not in tight_two_base_rectangle[
            "clear_false_positive_targets"]:
        raise AssertionError(
            "tight two rectangle no longer contains closest clear")
    if 0.03 != first_stress_rectangle_false_positive["pair_epsilon"]:
        raise AssertionError("first square false-positive threshold drifted")

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_adverse_pair_falsifier": str(SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite pair/complement plane diagnostic only; the checked "
            "stress-centered plane boxes expose a narrow local locator but "
            "do not prove a stable selector, an adverse-pair theorem, a "
            "pointwise character-sum estimate, or Goldbach"),
        "candidate": (
            "After pair sign fails, the coupled plane of named-pair sum "
            "against six-channel repair-complement sum might isolate the "
            "tight q286 near-boundary deficit more sharply than either "
            "coordinate alone."),
        "mechanism": (
            "Use the exact top-20 q286 near-boundary row ledger and view "
            "each row as a point (pair sum, repair-complement sum).  Check "
            "stress-centered scalar neighborhoods, stress-centered plane "
            "rectangles, and the rectangle spanned by the tight deficit "
            "1222142 and closest clear 1242118."),
        "prediction": (
            "If the pair/complement plane is a simple theorem handle, a "
            "non-tuned rectangle or scalar band should separate the lone "
            "deficit from nearby clears across the checked near-boundary "
            "rows."),
        "falsifier": (
            "The simple-plane handle fails if the tight clear lies in the "
            "same natural pair/complement rectangle or if modestly widened "
            "stress-centered boxes immediately collect clear rows."),
        "novelty_label": "new-to-this-task",
        "arithmetic_modulus": source["arithmetic_modulus"],
        "support": source["support"],
        "adverse_pair": source["adverse_pair"],
        "volatile_labels": source["volatile_labels"],
        "top20_row_count": len(rows),
        "deficit_targets": tuple(int(row["target"]) for row in deficit_rows),
        "clear_count": len(clear_rows),
        "stress_row": compact_row(stress),
        "tight_clear_row": compact_row(tight_clear),
        "row_records": tuple(
            compact_row(row) for row in sorted(
                rows, key=lambda item: item[
                    "absolute_above_floor_signed_surplus"])),
        "scalar_neighborhoods": scalar_neighborhoods,
        "stress_centered_rectangles": stress_rectangles,
        "tight_two_spanning_rectangles": tight_two_rectangles,
        "plane_summaries": {
            "pair_sum": summarize(
                row["adverse_pair_sum_to_principal"] for row in rows),
            "repair_complement_sum": summarize(
                row["repair_complement_sum_to_principal"] for row in rows),
            "volatile_total_sum": summarize(
                row["volatile_total_sum_to_principal"] for row in rows),
            "pair_abs_share": summarize(
                row["adverse_pair_abs_share"] for row in rows),
            "pair_abs_to_complement_abs_ratio": summarize(
                row["adverse_pair_to_repair_complement_abs_ratio"]
                for row in rows),
        },
        "correlations": {
            "pearson_abs_surplus_vs_pair_sum": pearson(
                (row["absolute_above_floor_signed_surplus"] for row in rows),
                (row["adverse_pair_sum_to_principal"] for row in rows)),
            "pearson_abs_surplus_vs_repair_complement_sum": pearson(
                (row["absolute_above_floor_signed_surplus"] for row in rows),
                (row["repair_complement_sum_to_principal"] for row in rows)),
            "pearson_abs_surplus_vs_volatile_total_sum": pearson(
                (row["absolute_above_floor_signed_surplus"] for row in rows),
                (row["volatile_total_sum_to_principal"] for row in rows)),
            "pearson_abs_surplus_vs_pair_abs_share": pearson(
                (row["absolute_above_floor_signed_surplus"] for row in rows),
                (row["adverse_pair_abs_share"] for row in rows)),
            "pearson_abs_surplus_vs_pair_abs_to_complement_abs_ratio": pearson(
                (row["absolute_above_floor_signed_surplus"] for row in rows),
                (row["adverse_pair_to_repair_complement_abs_ratio"]
                 for row in rows)),
        },
        "summary": {
            "stress_centered_local_locator": (
                "Square pair/complement boxes centered at 1222142 with "
                "epsilons .005, .01, and .02 select only the finite stress "
                "deficit on the checked top-20 set."),
            "first_square_false_positive": (
                "The .03 by .03 stress-centered square selects clear rows "
                "1242118, 1222048, and 1242136 along with the deficit."),
            "tight_two_rectangle": (
                "The natural rectangle spanned by the two tightest rows "
                "already contains one deficit and one clear, so the plane is "
                "not a classification theorem by itself."),
            "live_target": (
                "The plane is a useful diagnostic for where the q286 hole is "
                "narrowest, but a proof still needs an arithmetic reason for "
                "the allowed pair/complement band or a stronger signed "
                "aggregate estimate."),
        },
        "interpretation": {
            "hole_status": (
                "The loop is tightening locally: pair-plus-complement geometry "
                "isolates the stress row at very small finite bands, then "
                "admits nearby clears as soon as the band is modestly widened."),
            "route_status": (
                "Preserve pair/complement plane geometry as a finite locator "
                "and theorem-obligation shaper, not as a proved selector."),
            "remaining_theorem": (
                "Prove a row-dependent arithmetic placement bound for actual "
                "binary-prime residue weights, or derive a signed aggregate "
                "inequality explaining why the stress row sits in the narrow "
                "allowed plane box."),
        },
        "pair_complement_plane_audit_measured": True,
        "stress_centered_plane_local_locator_observed": True,
        "simple_pair_complement_plane_selector_theorem_proved": False,
        "adverse_pair_theorem_proved": False,
        "volatile_rim_theorem_proved": False,
        "selected_fixture_classifier_theorem_proved": False,
        "pointwise_character_sum_estimate_proved": False,
        "goldbach_proved": False,
    }

    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
