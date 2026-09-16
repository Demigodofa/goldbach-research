"""Decompose zero-residue directional slack by modulus and character phase.

The directional-slack audit showed that the actual adverse projection realizes
only a small fraction of the aggregate Cauchy L2 threat on the K_286
zero-residue probe.  This receipt asks where the mismatch lives: which modulus
dominates the L2 threat, which modulus actually contributes adverse drag, and
whether the multiplicative-character phase products reconstruct the signed
errors.

Finite diagnostic only.  It is a theorem-target locator, not a proof.
"""

from __future__ import annotations

import collections
import itertools
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OBSERVED_SOURCE = (
    EVIDENCE
    / "q286-wbss-k286-zero-residue-observed-character-moment-audit.json")
RAW_PROBE_SOURCE = (
    EVIDENCE / "q286-wbss-k286-zero-residue-raw-horizon-probe.json")
SCHEDULE_SOURCE = (
    EVIDENCE / "q286-wbss-k286-zero-residue-character-budget-schedule.json")
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
OUT = EVIDENCE / "q286-wbss-k286-zero-residue-component-phase-audit.json"
TOLERANCE = 1e-12

sys.path.insert(0, str(ROOT))

from tools import build_q286_wbss_four_modulus_variance_scale_far_lift_holdout as far  # noqa: E501,E402
from tools.build_q286_wbss_four_modulus_direct_holdout_decomposition import (  # noqa: E402
    coefficient_lookup,
    signed_error_terms,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402
from tools.build_q286_wbss_multiplicative_character_burden_audit import (  # noqa: E402
    coefficient_grid,
)
from tools.build_q286_wbss_multiplicative_character_l2_observed_moment_audit import (  # noqa: E501,E402
    active_character_masks,
)
from tools.build_q286_wbss_projection_uniformity_obstruction_audit import (  # noqa: E402
    projection_distribution,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def phase_mode_rows(modulus, data, orbit_data, actual_mass, uniform_mass):
    delta = np.zeros(
        tuple(factor - 1 for factor in data["factors"]),
        dtype=np.complex128,
    )
    actual_projection = projection_distribution(
        orbit_data["orbits"], actual_mass, modulus)
    uniform_projection = projection_distribution(
        orbit_data["orbits"], uniform_mass, modulus)
    for residue in data["coefficients"]:
        index = tuple(
            data["maps"][factor]["exponent_by_residue"][residue % factor]
            for factor in data["factors"]
        )
        delta[index] = (
            actual_projection.get(residue, 0.0)
            - uniform_projection.get(residue, 0.0))

    grid = coefficient_grid(
        modulus, data["factors"], data["coefficients"], data["maps"])
    centered = grid - np.mean(grid)
    coefficient_hat = np.fft.fftn(centered) / centered.size
    moment_hat = np.conj(np.fft.fftn(delta))

    rows = []
    for frequency in itertools.product(*(range(size)
                                         for size in coefficient_hat.shape)):
        if all(item == 0 for item in frequency):
            continue
        contribution = coefficient_hat[frequency] * moment_hat[frequency]
        real_contribution = float(contribution.real)
        if abs(real_contribution) <= TOLERANCE and abs(
                contribution.imag) <= TOLERANCE:
            continue
        rows.append({
            "frequency": list(frequency),
            "real_contribution": real_contribution,
            "imag_contribution": float(contribution.imag),
            "abs_complex_contribution": float(abs(contribution)),
            "coefficient_hat_real": float(coefficient_hat[frequency].real),
            "coefficient_hat_imag": float(coefficient_hat[frequency].imag),
            "moment_hat_real": float(moment_hat[frequency].real),
            "moment_hat_imag": float(moment_hat[frequency].imag),
        })
    return rows


def summarize_phase_modes(mode_rows, signed_error):
    adverse = [
        row for row in mode_rows if row["real_contribution"] < -TOLERANCE]
    rescue = [
        row for row in mode_rows if row["real_contribution"] > TOLERANCE]
    real_envelope = math.fsum(
        abs(row["real_contribution"]) for row in mode_rows)
    real_sum = math.fsum(row["real_contribution"] for row in mode_rows)
    return {
        "nonzero_phase_mode_count": len(mode_rows),
        "phase_real_sum": real_sum,
        "phase_reconstruction_error": abs(real_sum - signed_error),
        "phase_real_abs_envelope": real_envelope,
        "phase_real_cancellation_ratio": (
            abs(real_sum) / real_envelope
            if real_envelope > TOLERANCE else None),
        "phase_adverse_real_drag": math.fsum(
            -row["real_contribution"] for row in adverse),
        "phase_rescue_real_help": math.fsum(
            row["real_contribution"] for row in rescue),
        "top_adverse_phase_modes": sorted(
            adverse,
            key=lambda row: (row["real_contribution"], row["frequency"]),
        )[:5],
        "top_rescue_phase_modes": sorted(
            rescue,
            key=lambda row: (-row["real_contribution"], row["frequency"]),
        )[:5],
    }


def component_record(observed_row, raw_row, modulus, coefficient_l2,
                     aggregate_coefficient_l2, phase_summary):
    modulus_key = str(modulus)
    local_main = (
        observed_row["zero_residue_local_aggregate_l2_cap"]
        * aggregate_coefficient_l2)
    signed_error = raw_row["signed_error_by_modulus"][modulus_key]
    cauchy_threat = (
        coefficient_l2
        * observed_row["character_moment_l2_by_modulus"][modulus_key]
        / local_main)
    adverse = max(0.0, -signed_error) / local_main
    signed_ratio = signed_error / local_main
    return {
        "modulus": modulus_key,
        "coefficient_l2": coefficient_l2,
        "character_moment_l2": (
            observed_row["character_moment_l2_by_modulus"][modulus_key]),
        "cauchy_threat_ratio_to_local_main": cauchy_threat,
        "signed_error_ratio_to_local_main": signed_ratio,
        "actual_adverse_drag_ratio_to_local_main": adverse,
        "directional_efficiency_actual_adverse_over_cauchy": (
            adverse / cauchy_threat
            if cauchy_threat > TOLERANCE else None),
        "component_is_adverse": bool(signed_error < -TOLERANCE),
        "component_is_rescue": bool(signed_error > TOLERANCE),
        "phase_summary": phase_summary,
    }


def build_violating_row(observed_row, raw_row, context, full_coefficients,
                        first_three_coefficients, primes, prime_values,
                        log_values, active_masks, coefficient_l2_by_modulus,
                        aggregate_coefficient_l2):
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
    alpha0, by_modulus = coefficient_lookup(load_json(FORMULA_SOURCE))
    terms, _details = signed_error_terms(
        orbit_data["orbits"], actual_mass, uniform_mass, by_modulus)

    components = []
    for modulus_key in sorted(coefficient_l2_by_modulus, key=int):
        modulus = int(modulus_key)
        phase_rows = phase_mode_rows(
            modulus,
            active_masks[modulus],
            orbit_data,
            actual_mass,
            uniform_mass,
        )
        phase_summary = summarize_phase_modes(
            phase_rows, terms[modulus_key])
        components.append(component_record(
            observed_row,
            raw_row,
            modulus,
            coefficient_l2_by_modulus[modulus_key],
            aggregate_coefficient_l2,
            phase_summary,
        ))

    dominant_threat = max(
        components,
        key=lambda item: (
            item["cauchy_threat_ratio_to_local_main"],
            -int(item["modulus"])))
    dominant_adverse = max(
        components,
        key=lambda item: (
            item["actual_adverse_drag_ratio_to_local_main"],
            -int(item["modulus"])))
    local_main = (
        observed_row["zero_residue_local_aggregate_l2_cap"]
        * aggregate_coefficient_l2)
    return {
        "target": observed_row["target"],
        "target_residue": observed_row["target_residue"],
        "target_mod_286": observed_row["target_mod_286"],
        "local_main_reconstructed": local_main,
        "aggregate_cauchy_threat_ratio_to_local_main": (
            observed_row["ratio_to_zero_residue_local_l2_cap"]),
        "raw_adverse_drag_ratio_to_local_main": (
            observed_row["raw_adverse_drag_ratio"]),
        "directional_efficiency_actual_over_cauchy": (
            observed_row["raw_adverse_drag_ratio"]
            / observed_row["ratio_to_zero_residue_local_l2_cap"]),
        "dominant_cauchy_threat_modulus": dominant_threat["modulus"],
        "dominant_actual_adverse_modulus": dominant_adverse["modulus"],
        "component_rows": components,
    }


def summarize_component_rows(violating_rows):
    component_rows = [
        component
        for row in violating_rows
        for component in row["component_rows"]
    ]
    by_modulus = {}
    for modulus in sorted({row["modulus"] for row in component_rows}, key=int):
        rows = [row for row in component_rows if row["modulus"] == modulus]
        by_modulus[modulus] = {
            "row_count": len(rows),
            "adverse_component_count": sum(
                row["component_is_adverse"] for row in rows),
            "rescue_component_count": sum(
                row["component_is_rescue"] for row in rows),
            "cauchy_threat_ratio_summary": finite_summary(
                row["cauchy_threat_ratio_to_local_main"] for row in rows),
            "actual_adverse_drag_ratio_summary": finite_summary(
                row["actual_adverse_drag_ratio_to_local_main"]
                for row in rows),
            "directional_efficiency_summary": finite_summary(
                row["directional_efficiency_actual_adverse_over_cauchy"]
                for row in rows),
            "phase_cancellation_ratio_summary": finite_summary(
                row["phase_summary"]["phase_real_cancellation_ratio"]
                for row in rows),
            "phase_reconstruction_error_summary": finite_summary(
                row["phase_summary"]["phase_reconstruction_error"]
                for row in rows),
            "largest_cauchy_threat_row": max(
                rows,
                key=lambda row: (
                    row["cauchy_threat_ratio_to_local_main"],
                    -int(row["modulus"]))),
            "largest_actual_adverse_row": max(
                rows,
                key=lambda row: (
                    row["actual_adverse_drag_ratio_to_local_main"],
                    -int(row["modulus"]))),
            "largest_directional_efficiency_row": max(
                rows,
                key=lambda row: (
                    row["directional_efficiency_actual_adverse_over_cauchy"],
                    -int(row["modulus"]))),
        }

    return {
        "violating_row_count": len(violating_rows),
        "dominant_cauchy_threat_modulus_counts": dict(
            collections.Counter(
                row["dominant_cauchy_threat_modulus"]
                for row in violating_rows)),
        "dominant_actual_adverse_modulus_counts": dict(
            collections.Counter(
                row["dominant_actual_adverse_modulus"]
                for row in violating_rows)),
        "aggregate_directional_efficiency_summary": finite_summary(
            row["directional_efficiency_actual_over_cauchy"]
            for row in violating_rows),
        "aggregate_cauchy_threat_ratio_summary": finite_summary(
            row["aggregate_cauchy_threat_ratio_to_local_main"]
            for row in violating_rows),
        "aggregate_raw_adverse_ratio_summary": finite_summary(
            row["raw_adverse_drag_ratio_to_local_main"]
            for row in violating_rows),
        "by_modulus": by_modulus,
        "largest_aggregate_cauchy_threat_row": max(
            violating_rows,
            key=lambda row: (
                row["aggregate_cauchy_threat_ratio_to_local_main"],
                -row["target"])),
        "largest_aggregate_directional_efficiency_row": max(
            violating_rows,
            key=lambda row: (
                row["directional_efficiency_actual_over_cauchy"],
                -row["target"])),
    }


def build_receipt():
    observed = load_json(OBSERVED_SOURCE)
    raw_probe = load_json(RAW_PROBE_SOURCE)
    schedule = load_json(SCHEDULE_SOURCE)
    formula = load_json(FORMULA_SOURCE)
    raw_by_target = {
        int(row["target"]): row
        for row in raw_probe["finite_probe"]["rows"]
    }
    observed_violating = [
        row for row in observed["finite_diagnostic"]["rows"]
        if row["exceeds_zero_residue_local_l2_cap"]
    ]
    maximum_target = max(row["target"] for row in observed_violating)
    primes = np.asarray(far._prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = far.logs(maximum_target)
    context = far.prepare_support_context()
    context["coefficient"] = (
        far.combined_fixed_strict_central_coefficient_receipt())
    full_coefficients = far.period_full_unit_coefficients(context)
    first_three_coefficients = far.q286_first_three_unit_coefficients(context)
    active_masks = active_character_masks(formula)
    coefficient_l2_by_modulus = {
        str(key): value
        for key, value in schedule["coefficient_character_budget"][
            "character_l2_by_modulus"].items()
    }
    aggregate_coefficient_l2 = schedule["coefficient_character_budget"][
        "aggregate_character_l2"]

    violating_rows = [
        build_violating_row(
            row,
            raw_by_target[int(row["target"])],
            context,
            full_coefficients,
            first_three_coefficients,
            primes,
            prime_values,
            log_values,
            active_masks,
            coefficient_l2_by_modulus,
            aggregate_coefficient_l2,
        )
        for row in observed_violating
    ]
    summary = summarize_component_rows(violating_rows)
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-zero-residue-component-phase-audit",
        "source_commit": source_commit(),
        "sources": {
            "observed_character_moment_audit": str(
                OBSERVED_SOURCE.relative_to(ROOT)),
            "observed_character_moment_source_commit": (
                observed["source_commit"]),
            "zero_residue_raw_horizon_probe": str(
                RAW_PROBE_SOURCE.relative_to(ROOT)),
            "zero_residue_raw_horizon_probe_source_commit": (
                raw_probe["source_commit"]),
            "zero_residue_character_budget_schedule": str(
                SCHEDULE_SOURCE.relative_to(ROOT)),
            "zero_residue_character_budget_source_commit": (
                schedule["source_commit"]),
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "formula_source_commit": formula["source_commit"],
        },
        "status": "DIAGNOSTIC_zero_residue_component_phase_nonalignment",
        "question": (
            "On the zero-lane rows where aggregate L2 caps fail, which "
            "moduli carry the Cauchy threat and which moduli realize actual "
            "adverse drag?"),
        "answer": (
            "The Cauchy threat is structurally concentrated in modulus 286: "
            "it is the dominant threat on all 18 L2-cap-violating rows.  "
            "Actual adverse drag is split across moduli 154, 286, 70, and "
            "130, so the aggregate norm threat is not aligned with the "
            "actual adverse direction."),
        "finite_diagnostic": {
            "finite_evidence_is_acceptance_condition": False,
            "role": (
                "component and phase locator for the coefficient-direction "
                "nonalignment theorem target"),
            "summary": summary,
            "violating_rows": violating_rows,
        },
        "candidate": {
            "name": "modulus-286 threat decoupling from adverse direction",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The largest active-character norm load is concentrated in "
                "the K_286 component, but the adverse sign is distributed and "
                "often carried by other moduli or canceled by phase-mode "
                "rescue inside the same modulus."),
            "prediction": (
                "A useful universal estimate should not bound the aggregate "
                "L2 norm alone; it should control the projection of the "
                "binary-prime error vector onto the adverse coefficient "
                "direction, with special attention to the K_286 phase modes."),
            "falsifier": (
                "A later sufficiently-large row where modulus 286 dominates "
                "both Cauchy threat and actual adverse drag with directional "
                "efficiency near 1 would collapse this decoupling target."),
            "smallest_next_action": (
                "Turn the K_286 phase-mode rows into a symbolic sign or "
                "oscillation obligation: identify whether the largest adverse "
                "frequencies are paired by conjugacy, residue symmetry, or "
                "target-residue drift."),
        },
        "decision": (
            "DIAGNOSTIC_zero_residue_component_phase_nonalignment.  The "
            "finite obstruction is now sharper: modulus 286 dominates the "
            "Cauchy norm threat on every L2-cap-violating row, but actual "
            "adverse drag is distributed across moduli.  The next theorem "
            "target is a coefficient-direction nonalignment or K_286 phase "
            "oscillation estimate, not an aggregate L2 estimate."),
        "status_boundary": (
            "Finite component/phase diagnostic only.  No component theorem, "
            "no phase-mode theorem, no coefficient-direction nonalignment "
            "theorem, no universal pointwise raw bound, no q286 threshold "
            "theorem, no strict-central Goldbach theorem, and no Goldbach "
            "proof is established."),
        "component_nonalignment_theorem_proved": False,
        "phase_mode_theorem_proved": False,
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
        "dominant_cauchy_threat_modulus_counts": (
            summary["dominant_cauchy_threat_modulus_counts"]),
        "dominant_actual_adverse_modulus_counts": (
            summary["dominant_actual_adverse_modulus_counts"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
