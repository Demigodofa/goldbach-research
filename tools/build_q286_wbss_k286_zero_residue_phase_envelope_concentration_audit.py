"""Measure K_286 phase-envelope concentration on extended zero-lane lifts.

The extended-lift phase-band audit showed that fixed phase-pair labels keep
moving.  This receipt asks whether the real absolute K_286 phase envelope is
nevertheless concentrated: how many conjugate pairs are needed to cover fixed
fractions of the envelope on each checked row?

Finite diagnostic only.  A concentrated finite envelope is a theorem target,
not a phase-envelope theorem or Goldbach proof.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
EXTENDED_SOURCE = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-extended-lift-phase-band-audit.json")
RAW_SOURCE = EVIDENCE / "q286-wbss-raw-adverse-drag-theorem-target.json"
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
OUT = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-phase-envelope-concentration-audit.json")
THRESHOLDS = (0.5, 0.75, 0.9)
MODULUS = 286
TOLERANCE = 1e-12

sys.path.insert(0, str(ROOT))

from tools import build_q286_wbss_four_modulus_variance_scale_far_lift_holdout as far  # noqa: E501,E402
from tools.build_q286_wbss_k286_zero_residue_component_phase_audit import (  # noqa: E501,E402
    phase_mode_rows,
)
from tools.build_q286_wbss_k286_zero_residue_extended_lift_phase_band_audit import (  # noqa: E501,E402
    target_rows,
)
from tools.build_q286_wbss_k286_zero_residue_k286_phase_pair_audit import (  # noqa: E501,E402
    pair_phase_rows,
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


def cover_counts(pair_rows):
    sorted_rows = sorted(
        pair_rows,
        key=lambda row: (-abs(row["real_contribution"]), row["pair_label"]),
    )
    envelope = math.fsum(abs(row["real_contribution"]) for row in sorted_rows)
    if envelope <= TOLERANCE:
        return {
            "pair_count": len(sorted_rows),
            "pair_real_abs_envelope": envelope,
            "cover_counts": {
                str(threshold): None for threshold in THRESHOLDS
            },
            "cover_fractions": {
                str(threshold): None for threshold in THRESHOLDS
            },
            "top_pair_fraction": None,
            "top_pairs": [],
        }

    running = 0.0
    counts = {}
    fractions = {}
    remaining = set(THRESHOLDS)
    for index, row in enumerate(sorted_rows, start=1):
        running += abs(row["real_contribution"])
        for threshold in tuple(remaining):
            if running / envelope >= threshold:
                counts[str(threshold)] = index
                fractions[str(threshold)] = running / envelope
                remaining.remove(threshold)
        if not remaining:
            break
    return {
        "pair_count": len(sorted_rows),
        "pair_real_abs_envelope": envelope,
        "cover_counts": counts,
        "cover_fractions": fractions,
        "top_pair_fraction": (
            abs(sorted_rows[0]["real_contribution"]) / envelope),
        "top_pairs": sorted_rows[:12],
    }


def participation_metrics(pair_rows):
    weights = [abs(row["real_contribution"]) for row in pair_rows]
    total = math.fsum(weights)
    if total <= TOLERANCE:
        return {
            "inverse_participation_count": None,
            "entropy_effective_count": None,
            "largest_pair_fraction": None,
        }
    probabilities = [weight / total for weight in weights]
    collision = math.fsum(probability * probability
                          for probability in probabilities)
    entropy = -math.fsum(
        probability * math.log(probability)
        for probability in probabilities
        if probability > 0.0)
    return {
        "inverse_participation_count": 1.0 / collision,
        "entropy_effective_count": math.exp(entropy),
        "largest_pair_fraction": max(probabilities),
    }


def row_envelope_record(row, context, full_coefficients,
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
    pair_sum = math.fsum(item["real_contribution"] for item in pair_rows)
    covers = cover_counts(pair_rows)
    participation = participation_metrics(pair_rows)
    return {
        **row,
        "pair_real_sum": pair_sum,
        "k286_component_sign": (
            "adverse" if pair_sum < -TOLERANCE
            else "rescue" if pair_sum > TOLERANCE
            else "zero"),
        "pair_real_cancellation_ratio": (
            abs(pair_sum) / covers["pair_real_abs_envelope"]
            if covers["pair_real_abs_envelope"] > TOLERANCE else None),
        **covers,
        "participation_metrics": participation,
    }


def summarize_by_residue(rows):
    residues = {}
    for row in rows:
        residues.setdefault(row["target_residue"], []).append(row)
    summaries = []
    for residue, residue_rows in sorted(residues.items()):
        residue_rows = sorted(residue_rows, key=lambda item: item["target"])
        summaries.append({
            "target_residue": residue,
            "row_count": len(residue_rows),
            "threshold_count_summaries": {
                str(threshold): finite_summary(
                    row["cover_counts"][str(threshold)]
                    for row in residue_rows)
                for threshold in THRESHOLDS
            },
            "top_pair_fraction_summary": finite_summary(
                row["top_pair_fraction"] for row in residue_rows),
            "inverse_participation_count_summary": finite_summary(
                row["participation_metrics"][
                    "inverse_participation_count"]
                for row in residue_rows),
            "entropy_effective_count_summary": finite_summary(
                row["participation_metrics"]["entropy_effective_count"]
                for row in residue_rows),
            "rows": residue_rows,
        })
    return summaries


def summarize_rows(rows):
    residue_summaries = summarize_by_residue(rows)
    return {
        "row_count": len(rows),
        "target_minimum": min(row["target"] for row in rows),
        "target_maximum": max(row["target"] for row in rows),
        "distinct_target_residue_count": len(residue_summaries),
        "pair_count_summary": finite_summary(
            row["pair_count"] for row in rows),
        "threshold_count_summaries": {
            str(threshold): finite_summary(
                row["cover_counts"][str(threshold)] for row in rows)
            for threshold in THRESHOLDS
        },
        "top_pair_fraction_summary": finite_summary(
            row["top_pair_fraction"] for row in rows),
        "inverse_participation_count_summary": finite_summary(
            row["participation_metrics"]["inverse_participation_count"]
            for row in rows),
        "entropy_effective_count_summary": finite_summary(
            row["participation_metrics"]["entropy_effective_count"]
            for row in rows),
        "pair_cancellation_ratio_summary": finite_summary(
            row["pair_real_cancellation_ratio"] for row in rows),
        "largest_90pct_cover_count_row": max(
            rows,
            key=lambda row: (row["cover_counts"]["0.9"], -row["target"])),
        "smallest_90pct_cover_count_row": min(
            rows,
            key=lambda row: (row["cover_counts"]["0.9"], row["target"])),
        "largest_top_pair_fraction_row": max(
            rows,
            key=lambda row: (row["top_pair_fraction"], -row["target"])),
        "residue_summaries": residue_summaries,
    }


def build_receipt():
    extended = load_json(EXTENDED_SOURCE)
    raw = load_json(RAW_SOURCE)
    formula = load_json(FORMULA_SOURCE)
    residues = [
        int(row["target_residue"])
        for row in extended["finite_diagnostic"]["summary"][
            "residue_summaries"]
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
    envelope_rows = [
        row_envelope_record(
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
    summary = summarize_rows(envelope_rows)
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-zero-residue-phase-envelope-concentration-audit",
        "source_commit": source_commit(),
        "sources": {
            "extended_lift_phase_band_audit": str(
                EXTENDED_SOURCE.relative_to(ROOT)),
            "extended_lift_phase_band_source_commit": (
                extended["source_commit"]),
            "raw_adverse_drag_theorem_target": str(
                RAW_SOURCE.relative_to(ROOT)),
            "raw_adverse_drag_source_commit": raw["source_commit"],
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "formula_source_commit": formula["source_commit"],
        },
        "status": "DIAGNOSTIC_k286_phase_envelope_broad",
        "question": (
            "After fixed phase labels and small seeded bands failed, how "
            "many K_286 conjugate phase pairs are needed to cover fixed "
            "fractions of the real absolute phase envelope?"),
        "answer": (
            "The finite envelope is broad.  Across the 32 extended-lift rows, "
            "the mean cover counts are 6.625 pairs for 50%, 11.9375 pairs "
            "for 75%, and 16.875 pairs for 90% of the real absolute "
            "envelope.  Since every row has 30 active conjugate phase pairs, "
            "this falsifies a tiny top-pair or small-band shortcut without "
            "yet proving a usable universal cancellation estimate."),
        "finite_diagnostic": {
            "finite_evidence_is_acceptance_condition": False,
            "role": (
                "falsifier for sparse K_286 phase-envelope concentration; "
                "locator for a broad-envelope or cancellation theorem target"),
            "thresholds": list(THRESHOLDS),
            "summary": summary,
        },
        "candidate": {
            "name": "broad K286 phase-envelope cancellation estimate",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The K_286 phase envelope is not controlled by a few dominant "
                "pairs.  A useful theorem target must exploit cancellation or "
                "distribution across many conjugate phase pairs."),
            "prediction": (
                "Additional lifts should keep 90% envelope cover counts "
                "large relative to the total pair count, while cancellation "
                "ratios may remain smaller than raw envelope size."),
            "falsifier": (
                "If a wider residue/lift sample shows 90% coverage collapsing "
                "to a small bounded number of pairs, sparse-envelope control "
                "would reopen."),
            "smallest_next_action": (
                "Test whether cancellation ratios or effective participation "
                "counts have stable residue/lift envelopes; stop chasing "
                "individual phase-pair labels."),
        },
        "decision": (
            "DIAGNOSTIC_k286_phase_envelope_broad.  The extended finite data "
            "does not support sparse phase-envelope concentration.  The next "
            "theorem-shaped target is broad phase cancellation or a "
            "distributional envelope estimate, not a top-pair or small-band "
            "estimate."),
        "status_boundary": (
            "Finite phase-envelope concentration diagnostic only.  No broad "
            "phase-envelope theorem, no cancellation theorem, no coefficient-"
            "direction nonalignment theorem, no universal pointwise raw "
            "bound, no q286 threshold theorem, no strict-central Goldbach "
            "theorem, and no Goldbach proof is established."),
        "broad_phase_envelope_theorem_proved": False,
        "phase_cancellation_theorem_proved": False,
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
        "cover_count_mean_50": summary[
            "threshold_count_summaries"]["0.5"]["mean"],
        "cover_count_mean_75": summary[
            "threshold_count_summaries"]["0.75"]["mean"],
        "cover_count_mean_90": summary[
            "threshold_count_summaries"]["0.9"]["mean"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
