"""Extend repeated K_286 phase-pair residues to test phase-band stability.

The lift-drift audit showed that target residue alone does not determine the
leading K_286 phase pair across the first two violating lifts.  This receipt
extends just the four repeated target residues to eight lifts each and asks
whether the phase-pair labels stabilize into a small band.

Finite diagnostic only.  This is a changed-condition probe, not an asymptotic
phase-band theorem.
"""

from __future__ import annotations

import collections
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
LIFT_DRIFT_SOURCE = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-phase-pair-lift-drift-audit.json")
RAW_SOURCE = EVIDENCE / "q286-wbss-raw-adverse-drag-theorem-target.json"
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
OUT = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-extended-lift-phase-band-audit.json")
PERIOD = 10010
MODULUS = 286
EXTENDED_LIFT_COUNT = 8
TOLERANCE = 1e-12

sys.path.insert(0, str(ROOT))

from tools import build_q286_wbss_four_modulus_variance_scale_far_lift_holdout as far  # noqa: E501,E402
from tools.build_q286_wbss_k286_zero_residue_component_phase_audit import (  # noqa: E501,E402
    phase_mode_rows,
)
from tools.build_q286_wbss_k286_zero_residue_k286_phase_pair_audit import (  # noqa: E501,E402
    pair_phase_rows,
)
from tools.build_q286_wbss_k286_zero_residue_raw_horizon_probe import (  # noqa: E402
    first_lift_above,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402
from tools.build_q286_wbss_multiplicative_character_l2_observed_moment_audit import (  # noqa: E501,E402
    active_character_masks,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def target_rows(residues, lower_bound):
    rows = []
    for residue in residues:
        first_target = first_lift_above(residue, lower_bound)
        for lift_index in range(EXTENDED_LIFT_COUNT):
            target = first_target + lift_index * PERIOD
            rows.append({
                "target": int(target),
                "target_residue": int(residue),
                "target_mod_286": int(target % MODULUS),
                "lift_index": int(lift_index),
                "block_index_after_raw_horizon": int(
                    max(0, (target - lower_bound + PERIOD - 1) // PERIOD)),
            })
    return rows


def top_pairs(pair_rows):
    adverse = [
        row for row in pair_rows
        if row["real_contribution"] < -TOLERANCE
    ]
    rescue = [
        row for row in pair_rows
        if row["real_contribution"] > TOLERANCE
    ]
    top_adverse = min(
        adverse,
        key=lambda row: (row["real_contribution"], row["pair_label"]),
    ) if adverse else None
    top_rescue = max(
        rescue,
        key=lambda row: (row["real_contribution"], row["pair_label"]),
    ) if rescue else None
    top_abs = max(
        pair_rows,
        key=lambda row: (abs(row["real_contribution"]), row["pair_label"]),
    )
    return top_adverse, top_rescue, top_abs


def row_phase_record(row, context, full_coefficients,
                     first_three_coefficients, primes, prime_values,
                     log_values, active_masks):
    orbit_data = far.orbit_coefficients(
        int(row["target_residue"]),
        context,
        full_coefficients,
        first_three_coefficients,
    )
    coefficient_data = {
        "orbits": orbit_data["orbits"],
        "first_three": np.asarray(
            orbit_data["first_three_coefficients"], dtype=np.float64),
        "full": np.asarray(
            orbit_data["full_coefficients"], dtype=np.float64),
    }
    actual = far.actual_orbit_measure(
        int(row["target"]),
        coefficient_data,
        primes,
        prime_values,
        log_values,
    )
    actual_mass = np.asarray(actual["masses"], dtype=np.float64)
    uniform_mass = np.asarray(
        orbit_data["uniform_orbit_mass"], dtype=np.float64)
    mode_rows = phase_mode_rows(
        MODULUS,
        active_masks[MODULUS],
        orbit_data,
        actual_mass,
        uniform_mass,
    )
    pair_rows = pair_phase_rows(mode_rows)
    pair_real_sum = math.fsum(item["real_contribution"] for item in pair_rows)
    pair_abs_envelope = math.fsum(
        abs(item["real_contribution"]) for item in pair_rows)
    top_adverse, top_rescue, top_abs = top_pairs(pair_rows)
    return {
        **row,
        "pair_real_sum": pair_real_sum,
        "k286_component_sign": (
            "adverse" if pair_real_sum < -TOLERANCE
            else "rescue" if pair_real_sum > TOLERANCE
            else "zero"),
        "pair_real_abs_envelope": pair_abs_envelope,
        "pair_real_cancellation_ratio": (
            abs(pair_real_sum) / pair_abs_envelope
            if pair_abs_envelope > TOLERANCE else None),
        "top_adverse_pair": (
            top_adverse["pair_label"] if top_adverse is not None else None),
        "top_rescue_pair": (
            top_rescue["pair_label"] if top_rescue is not None else None),
        "top_abs_pair": top_abs["pair_label"],
        "top_abs_pair_fraction_of_envelope": (
            abs(top_abs["real_contribution"]) / pair_abs_envelope
            if pair_abs_envelope > TOLERANCE else None),
        "top_pair_rows": sorted(
            pair_rows,
            key=lambda item: (-abs(item["real_contribution"]),
                              item["pair_label"]),
        )[:8],
    }


def label_counts(rows, key):
    return dict(sorted(
        collections.Counter(row[key] for row in rows).items(),
        key=lambda item: (-item[1], item[0]),
    ))


def residue_summary(residue, rows):
    first_two = rows[:2]
    later = rows[2:]
    first_two_top_abs_band = sorted({row["top_abs_pair"]
                                     for row in first_two})
    first_two_top_adverse_band = sorted({row["top_adverse_pair"]
                                         for row in first_two})
    first_two_top_rescue_band = sorted({row["top_rescue_pair"]
                                        for row in first_two})
    return {
        "target_residue": residue,
        "row_count": len(rows),
        "lift_indices": [row["lift_index"] for row in rows],
        "targets": [row["target"] for row in rows],
        "k286_component_sign_counts": label_counts(
            rows, "k286_component_sign"),
        "top_abs_pair_counts": label_counts(rows, "top_abs_pair"),
        "top_adverse_pair_counts": label_counts(rows, "top_adverse_pair"),
        "top_rescue_pair_counts": label_counts(rows, "top_rescue_pair"),
        "unique_top_abs_pair_count": len(
            {row["top_abs_pair"] for row in rows}),
        "unique_top_adverse_pair_count": len(
            {row["top_adverse_pair"] for row in rows}),
        "unique_top_rescue_pair_count": len(
            {row["top_rescue_pair"] for row in rows}),
        "first_two_top_abs_band": first_two_top_abs_band,
        "first_two_top_adverse_band": first_two_top_adverse_band,
        "first_two_top_rescue_band": first_two_top_rescue_band,
        "later_top_abs_covered_by_first_two_count": sum(
            row["top_abs_pair"] in first_two_top_abs_band for row in later),
        "later_top_adverse_covered_by_first_two_count": sum(
            row["top_adverse_pair"] in first_two_top_adverse_band
            for row in later),
        "later_top_rescue_covered_by_first_two_count": sum(
            row["top_rescue_pair"] in first_two_top_rescue_band
            for row in later),
        "later_row_count": len(later),
        "top_abs_pair_fraction_summary": finite_summary(
            row["top_abs_pair_fraction_of_envelope"] for row in rows),
        "pair_cancellation_ratio_summary": finite_summary(
            row["pair_real_cancellation_ratio"] for row in rows),
        "rows": rows,
    }


def summarize(rows):
    by_residue = collections.defaultdict(list)
    for row in rows:
        by_residue[row["target_residue"]].append(row)
    residue_summaries = [
        residue_summary(residue, sorted(items, key=lambda item: item["target"]))
        for residue, items in sorted(by_residue.items())
    ]
    return {
        "extended_residue_count": len(residue_summaries),
        "lift_count_per_residue": EXTENDED_LIFT_COUNT,
        "row_count": len(rows),
        "future_row_count_after_first_two": sum(
            row["later_row_count"] for row in residue_summaries),
        "future_top_abs_covered_by_first_two_count": sum(
            row["later_top_abs_covered_by_first_two_count"]
            for row in residue_summaries),
        "future_top_adverse_covered_by_first_two_count": sum(
            row["later_top_adverse_covered_by_first_two_count"]
            for row in residue_summaries),
        "future_top_rescue_covered_by_first_two_count": sum(
            row["later_top_rescue_covered_by_first_two_count"]
            for row in residue_summaries),
        "max_unique_top_abs_pair_count_by_residue": max(
            row["unique_top_abs_pair_count"] for row in residue_summaries),
        "max_unique_top_adverse_pair_count_by_residue": max(
            row["unique_top_adverse_pair_count"] for row in residue_summaries),
        "max_unique_top_rescue_pair_count_by_residue": max(
            row["unique_top_rescue_pair_count"] for row in residue_summaries),
        "top_abs_pair_fraction_summary": finite_summary(
            row["top_abs_pair_fraction_of_envelope"] for row in rows),
        "pair_cancellation_ratio_summary": finite_summary(
            row["pair_real_cancellation_ratio"] for row in rows),
        "residue_summaries": residue_summaries,
    }


def build_receipt():
    lift_drift = load_json(LIFT_DRIFT_SOURCE)
    raw = load_json(RAW_SOURCE)
    formula = load_json(FORMULA_SOURCE)
    residues = [
        int(row["target_residue"])
        for row in lift_drift["finite_diagnostic"]["summary"][
            "repeated_residue_records"]
    ]
    lower_bound = max(
        int(row["target"]) for row in raw["finite_calibration"]["rows"])
    rows = target_rows(residues, lower_bound)
    maximum_target = max(row["target"] for row in rows)
    primes = np.asarray(far._prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = far.logs(maximum_target)
    context = far.prepare_support_context()
    context["coefficient"] = (
        far.combined_fixed_strict_central_coefficient_receipt())
    full_coefficients = far.period_full_unit_coefficients(context)
    first_three_coefficients = far.q286_first_three_unit_coefficients(context)
    active_masks = active_character_masks(formula)
    phase_rows = [
        row_phase_record(
            row,
            context,
            full_coefficients,
            first_three_coefficients,
            primes,
            prime_values,
            log_values,
            active_masks,
        )
        for row in rows
    ]
    summary = summarize(phase_rows)
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-zero-residue-extended-lift-phase-band-audit",
        "source_commit": source_commit(),
        "sources": {
            "phase_pair_lift_drift_audit": str(
                LIFT_DRIFT_SOURCE.relative_to(ROOT)),
            "phase_pair_lift_drift_source_commit": (
                lift_drift["source_commit"]),
            "raw_adverse_drag_theorem_target": str(
                RAW_SOURCE.relative_to(ROOT)),
            "raw_adverse_drag_source_commit": raw["source_commit"],
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "formula_source_commit": formula["source_commit"],
        },
        "status": "DIAGNOSTIC_k286_small_phase_band_not_stable",
        "question": (
            "After the residue-only rule failed, do the first two lifts of "
            "each repeated residue define a small K_286 phase-pair band that "
            "covers later lifts?"),
        "answer": (
            "No.  Across four repeated residues extended to eight lifts each, "
            "the first-two-lift top-absolute pair bands cover only 3 of 24 "
            "later lifts; the top-adverse bands cover 8 of 24; and the "
            "top-rescue bands cover 8 of 24."),
        "finite_diagnostic": {
            "finite_evidence_is_acceptance_condition": False,
            "role": (
                "changed-condition falsifier for a small first-two-lift "
                "K_286 phase band; locator for broader moving-band or "
                "height-sensitive estimates"),
            "summary": summary,
        },
        "candidate": {
            "name": "broad moving K286 phase-band estimate",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The leading K_286 phase pairs keep drifting over additional "
                "lifts.  Any useful theorem target should control a moving "
                "band or aggregate phase envelope, not a small fixed band "
                "seeded by the first two lifts."),
            "prediction": (
                "Adding still more lifts will keep individual top pairs "
                "mobile, while coarse phase-envelope summaries may be more "
                "stable than labels."),
            "falsifier": (
                "If a larger phase band, defined by an arithmetic rule rather "
                "than fitted labels, covers almost all adverse contribution "
                "with bounded envelope, the moving-band route remains alive."),
            "smallest_next_action": (
                "Stop chasing top-label stability and test an envelope metric: "
                "how many conjugate pairs are needed per row to cover 50%, "
                "75%, and 90% of the K_286 real absolute envelope?"),
        },
        "decision": (
            "DIAGNOSTIC_k286_small_phase_band_not_stable.  The finite "
            "extended-lift check falsifies the small phase-band shortcut "
            "seeded by the first two lifts.  The next theorem-shaped target "
            "is an envelope or concentration estimate over moving K_286 "
            "phase pairs, not fixed labels."),
        "status_boundary": (
            "Finite extended-lift phase-band diagnostic only.  No moving-band "
            "phase theorem, no phase-envelope theorem, no coefficient-"
            "direction nonalignment theorem, no universal pointwise raw "
            "bound, no q286 threshold theorem, no strict-central Goldbach "
            "theorem, and no Goldbach proof is established."),
        "moving_band_phase_theorem_proved": False,
        "phase_envelope_theorem_proved": False,
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
        "row_count": summary["row_count"],
        "future_top_abs_covered_by_first_two_count": (
            summary["future_top_abs_covered_by_first_two_count"]),
        "future_row_count_after_first_two": (
            summary["future_row_count_after_first_two"]),
        "max_unique_top_abs_pair_count_by_residue": (
            summary["max_unique_top_abs_pair_count_by_residue"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
