"""Audit conjugate K_286 phase-pairs on zero-residue L2-violating rows.

The component-phase audit found that modulus 286 carries the Cauchy threat on
all 18 zero-lane rows where the aggregate character L2 cap fails.  This
receipt asks whether that K_286 structure collapses to one fixed conjugate
phase-pair, or whether the leading adverse/rescue pairs move with the target.

Finite diagnostic only.  A repeated phase-pair pattern is a theorem-target
locator, not a phase theorem or Goldbach proof.
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
COMPONENT_PHASE_SOURCE = (
    EVIDENCE / "q286-wbss-k286-zero-residue-component-phase-audit.json")
OBSERVED_SOURCE = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-observed-character-moment-audit.json")
RAW_PROBE_SOURCE = (
    EVIDENCE / "q286-wbss-k286-zero-residue-raw-horizon-probe.json")
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
OUT = EVIDENCE / "q286-wbss-k286-zero-residue-k286-phase-pair-audit.json"
MODULUS = 286
SHAPE = (10, 12)
TOLERANCE = 1e-12

sys.path.insert(0, str(ROOT))

from tools import build_q286_wbss_four_modulus_variance_scale_far_lift_holdout as far  # noqa: E501,E402
from tools.build_q286_wbss_k286_zero_residue_component_phase_audit import (  # noqa: E501,E402
    phase_mode_rows,
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


def neg_frequency(frequency):
    return tuple((size - item) % size
                 for item, size in zip(frequency, SHAPE))


def canonical_frequency(frequency):
    frequency = tuple(frequency)
    conjugate = neg_frequency(frequency)
    return min(frequency, conjugate)


def pair_label(canonical):
    conjugate = neg_frequency(canonical)
    return f"{canonical[0]},{canonical[1]}|{conjugate[0]},{conjugate[1]}"


def pair_phase_rows(mode_rows):
    grouped = {}
    for mode in mode_rows:
        canonical = canonical_frequency(mode["frequency"])
        record = grouped.setdefault(canonical, {
            "canonical_frequency": list(canonical),
            "conjugate_frequency": list(neg_frequency(canonical)),
            "pair_label": pair_label(canonical),
            "real_contribution": 0.0,
            "imag_contribution": 0.0,
            "abs_complex_contribution_sum": 0.0,
            "mode_count": 0,
        })
        record["real_contribution"] += mode["real_contribution"]
        record["imag_contribution"] += mode["imag_contribution"]
        record["abs_complex_contribution_sum"] += (
            mode["abs_complex_contribution"])
        record["mode_count"] += 1
    return list(grouped.values())


def row_pair_record(observed_row, raw_row, context, full_coefficients,
                    first_three_coefficients, primes, prime_values,
                    log_values, active_masks):
    orbit_data = far.orbit_coefficients(
        int(observed_row["target_residue"]),
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
        int(observed_row["target"]),
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
    pair_real_sum = math.fsum(row["real_contribution"] for row in pair_rows)
    pair_abs_envelope = math.fsum(
        abs(row["real_contribution"]) for row in pair_rows)
    signed_error = raw_row["signed_error_by_modulus"][str(MODULUS)]
    adverse_pairs = [
        row for row in pair_rows
        if row["real_contribution"] < -TOLERANCE
    ]
    rescue_pairs = [
        row for row in pair_rows
        if row["real_contribution"] > TOLERANCE
    ]
    top_adverse = min(
        adverse_pairs,
        key=lambda row: (row["real_contribution"], row["pair_label"]),
    ) if adverse_pairs else None
    top_rescue = max(
        rescue_pairs,
        key=lambda row: (row["real_contribution"], row["pair_label"]),
    ) if rescue_pairs else None
    top_abs = max(
        pair_rows,
        key=lambda row: (abs(row["real_contribution"]), row["pair_label"]),
    )
    return {
        "target": observed_row["target"],
        "target_residue": observed_row["target_residue"],
        "target_mod_286": observed_row["target_mod_286"],
        "k286_signed_error": signed_error,
        "k286_component_is_adverse": bool(signed_error < -TOLERANCE),
        "k286_component_is_rescue": bool(signed_error > TOLERANCE),
        "pair_count": len(pair_rows),
        "pair_real_sum": pair_real_sum,
        "pair_reconstruction_error": abs(pair_real_sum - signed_error),
        "pair_real_abs_envelope": pair_abs_envelope,
        "pair_real_cancellation_ratio": (
            abs(pair_real_sum) / pair_abs_envelope
            if pair_abs_envelope > TOLERANCE else None),
        "top_abs_pair_fraction_of_envelope": (
            abs(top_abs["real_contribution"]) / pair_abs_envelope
            if pair_abs_envelope > TOLERANCE else None),
        "top_adverse_pair": top_adverse,
        "top_rescue_pair": top_rescue,
        "top_abs_pair": top_abs,
        "pair_rows": sorted(
            pair_rows,
            key=lambda row: (-abs(row["real_contribution"]),
                             row["pair_label"]),
        )[:12],
    }


def label_counts(rows, key):
    counter = collections.Counter()
    for row in rows:
        item = row[key]
        if item is not None:
            counter[item["pair_label"]] += 1
    return dict(sorted(counter.items(), key=lambda item: (-item[1], item[0])))


def summarize_rows(rows):
    top_adverse_counts = label_counts(rows, "top_adverse_pair")
    top_rescue_counts = label_counts(rows, "top_rescue_pair")
    top_abs_counts = label_counts(rows, "top_abs_pair")
    max_top_adverse = max(top_adverse_counts.values())
    max_top_rescue = max(top_rescue_counts.values())
    max_top_abs = max(top_abs_counts.values())
    return {
        "violating_row_count": len(rows),
        "k286_adverse_component_count": sum(
            row["k286_component_is_adverse"] for row in rows),
        "k286_rescue_component_count": sum(
            row["k286_component_is_rescue"] for row in rows),
        "top_adverse_pair_counts": top_adverse_counts,
        "top_rescue_pair_counts": top_rescue_counts,
        "top_abs_pair_counts": top_abs_counts,
        "top_adverse_pair_max_row_count": max_top_adverse,
        "top_rescue_pair_max_row_count": max_top_rescue,
        "top_abs_pair_max_row_count": max_top_abs,
        "single_fixed_pair_dominates_top_adverse": bool(
            max_top_adverse > len(rows) // 2),
        "single_fixed_pair_dominates_top_rescue": bool(
            max_top_rescue > len(rows) // 2),
        "single_fixed_pair_dominates_top_abs": bool(
            max_top_abs > len(rows) // 2),
        "pair_reconstruction_error_summary": finite_summary(
            row["pair_reconstruction_error"] for row in rows),
        "pair_cancellation_ratio_summary": finite_summary(
            row["pair_real_cancellation_ratio"] for row in rows),
        "top_abs_pair_fraction_summary": finite_summary(
            row["top_abs_pair_fraction_of_envelope"] for row in rows),
        "largest_top_abs_pair_fraction_row": max(
            rows,
            key=lambda row: (
                row["top_abs_pair_fraction_of_envelope"], -row["target"])),
        "smallest_pair_cancellation_ratio_row": min(
            rows,
            key=lambda row: (
                row["pair_real_cancellation_ratio"], row["target"])),
        "largest_pair_cancellation_ratio_row": max(
            rows,
            key=lambda row: (
                row["pair_real_cancellation_ratio"], -row["target"])),
    }


def build_receipt():
    component_phase = load_json(COMPONENT_PHASE_SOURCE)
    observed = load_json(OBSERVED_SOURCE)
    raw_probe = load_json(RAW_PROBE_SOURCE)
    formula = load_json(FORMULA_SOURCE)
    raw_by_target = {
        int(row["target"]): row
        for row in raw_probe["finite_probe"]["rows"]
    }
    observed_by_target = {
        int(row["target"]): row
        for row in observed["finite_diagnostic"]["rows"]
    }
    targets = [
        int(row["target"])
        for row in component_phase["finite_diagnostic"]["violating_rows"]
    ]
    maximum_target = max(targets)
    primes = np.asarray(far._prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = far.logs(maximum_target)
    context = far.prepare_support_context()
    context["coefficient"] = (
        far.combined_fixed_strict_central_coefficient_receipt())
    full_coefficients = far.period_full_unit_coefficients(context)
    first_three_coefficients = far.q286_first_three_unit_coefficients(context)
    active_masks = active_character_masks(formula)
    rows = [
        row_pair_record(
            observed_by_target[target],
            raw_by_target[target],
            context,
            full_coefficients,
            first_three_coefficients,
            primes,
            prime_values,
            log_values,
            active_masks,
        )
        for target in targets
    ]
    summary = summarize_rows(rows)
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-zero-residue-k286-phase-pair-audit",
        "source_commit": source_commit(),
        "sources": {
            "component_phase_audit": str(
                COMPONENT_PHASE_SOURCE.relative_to(ROOT)),
            "component_phase_source_commit": (
                component_phase["source_commit"]),
            "observed_character_moment_audit": str(
                OBSERVED_SOURCE.relative_to(ROOT)),
            "observed_character_moment_source_commit": (
                observed["source_commit"]),
            "zero_residue_raw_horizon_probe": str(
                RAW_PROBE_SOURCE.relative_to(ROOT)),
            "zero_residue_raw_horizon_probe_source_commit": (
                raw_probe["source_commit"]),
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "formula_source_commit": formula["source_commit"],
        },
        "status": "DIAGNOSTIC_k286_phase_pair_single_mode_falsified",
        "question": (
            "On the zero-lane L2-cap-violating rows, does the K_286 phase "
            "nonalignment collapse to one fixed dominant conjugate phase-pair?"
        ),
        "answer": (
            "No.  The most common top adverse conjugate pair appears on only "
            "4 of 18 rows, the most common top rescue pair appears on only 4 "
            "of 18 rows, and the most common top absolute pair appears on "
            "only 3 of 18 rows."),
        "finite_diagnostic": {
            "finite_evidence_is_acceptance_condition": False,
            "role": (
                "falsifier for a single fixed K_286 phase-pair explanation; "
                "locator for a target-residue-dependent oscillation theorem"),
            "summary": summary,
            "rows": rows,
        },
        "candidate": {
            "name": "target-residue-dependent K286 conjugate-pair oscillation",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The relevant K_286 phase rescue is not carried by one fixed "
                "character pair; the leading adverse and rescue conjugate "
                "pairs drift with the target residue.  A theorem would need "
                "to exploit residue-dependent oscillation or a summed band of "
                "pairs, not a single-mode sign lemma."),
            "prediction": (
                "Extending the zero-lane probe should continue to show "
                "moving top K_286 pairs unless a hidden residue-period class "
                "is isolated."),
            "falsifier": (
                "A larger, residue-complete sufficiently-large sample where "
                "one conjugate pair dominates the adverse or rescue top pair "
                "on most rows would revive a single-mode theorem target."),
            "smallest_next_action": (
                "Group top K_286 phase-pairs by target residue modulo 10010 "
                "and by lift index to test whether the drift is deterministic "
                "in residue rather than random-looking."),
        },
        "decision": (
            "DIAGNOSTIC_k286_phase_pair_single_mode_falsified.  The K_286 "
            "component remains the right place to look, but the finite data "
            "does not support a single fixed conjugate phase-pair theorem.  "
            "The next theorem target is a target-residue-dependent oscillation "
            "or a band estimate over moving K_286 phase pairs."),
        "status_boundary": (
            "Finite K_286 conjugate phase-pair diagnostic only.  No phase-pair "
            "theorem, no target-residue oscillation theorem, no coefficient-"
            "direction nonalignment theorem, no universal pointwise raw "
            "bound, no q286 threshold theorem, no strict-central Goldbach "
            "theorem, and no Goldbach proof is established."),
        "phase_pair_theorem_proved": False,
        "target_residue_oscillation_theorem_proved": False,
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
        "violating_row_count": summary["violating_row_count"],
        "top_adverse_pair_max_row_count": (
            summary["top_adverse_pair_max_row_count"]),
        "top_rescue_pair_max_row_count": (
            summary["top_rescue_pair_max_row_count"]),
        "top_abs_pair_max_row_count": (
            summary["top_abs_pair_max_row_count"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
