"""Audit reflection-even structure of the K_286 two-mode target.

The two-mode singular target asks for a pointwise lower bound on the first two
singular moment functionals.  Strict-central ordered prime pairs are invariant
under p -> N-p, so only the reflection-even part of a residue coefficient can
pair with a reflection-symmetric residue mass.

This receipt checks whether that algebraic symmetry materially simplifies the
K_286 two-mode burden.  It proves the odd-null identity for the finite
coefficient model, but proves no binary-prime moment theorem, no adverse-drag
bound, and no Goldbach theorem.
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
OUT = EVIDENCE / "q286-wbss-k286-two-mode-reflection-parity-audit.json"
MODULUS = 286
MODE_COUNT = 2
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_frequency_resolved_fourier import (  # noqa: E402
    _unit_character_table,
)
from tools.build_q286_wbss_k286_two_mode_singular_target import (  # noqa: E402
    normalized_k286_matrix,
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
    if isinstance(value, (tuple, list)):
        return [json_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, np.generic):
        return json_ready(value.item())
    if isinstance(value, complex):
        return {
            "real": float(value.real),
            "imag": float(value.imag),
        }
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def finite_summary(values):
    finite = tuple(float(value) for value in values
                   if value is not None and math.isfinite(float(value)))
    if not finite:
        return {
            "count": 0,
            "minimum": None,
            "maximum": None,
            "mean": None,
        }
    return {
        "count": len(finite),
        "minimum": min(finite),
        "maximum": max(finite),
        "mean": math.fsum(finite) / len(finite),
    }


def residue_mode_values(left, singular_values, right, mode_index, units,
                        labels, character_table, scaled=True):
    matrix = np.zeros((10, 12), dtype=np.complex128)
    mode = np.outer(left[:, mode_index], right[mode_index, :])
    if scaled:
        mode = singular_values[mode_index] * mode
    matrix[1:, 1:] = mode
    coefficients = np.asarray([matrix[label] for label in labels],
                              dtype=np.complex128)
    values = character_table.T @ coefficients
    return {
        int(unit): complex(value)
        for unit, value in zip(units, values)
    }


def admissible_units(target_residue, units):
    return tuple(
        unit for unit in units
        if math.gcd((target_residue - unit) % MODULUS, MODULUS) == 1)


def reflection_orbits(target_residue, units):
    unit_set = set(units)
    seen = set()
    orbits = []
    for unit in units:
        if unit in seen:
            continue
        reflected = (target_residue - unit) % MODULUS
        if reflected not in unit_set:
            raise AssertionError("reflection left admissible support")
        orbit = tuple(sorted({unit, reflected}))
        seen.update(orbit)
        orbits.append(orbit)
    return tuple(orbits)


def decompose_for_target(target_residue, values):
    units = tuple(sorted(values))
    admissible = admissible_units(target_residue, units)
    if not admissible:
        raise AssertionError("empty admissible residue set")
    local_mean = sum(values[unit] for unit in admissible) / len(admissible)
    centered = {
        unit: values[unit] - local_mean
        for unit in admissible
    }
    even = {}
    odd = {}
    orbits = reflection_orbits(target_residue, admissible)
    for orbit in orbits:
        if len(orbit) == 1:
            unit = orbit[0]
            even[unit] = centered[unit]
            odd[unit] = 0.0j
            continue
        left, right = orbit
        even_value = (centered[left] + centered[right]) / 2.0
        odd_value = (centered[left] - centered[right]) / 2.0
        even[left] = even_value
        even[right] = even_value
        odd[left] = odd_value
        odd[right] = -odd_value

    full_l2_sq = math.fsum(abs(centered[unit]) ** 2 for unit in admissible)
    even_l2_sq = math.fsum(abs(even[unit]) ** 2 for unit in admissible)
    odd_l2_sq = math.fsum(abs(odd[unit]) ** 2 for unit in admissible)
    if full_l2_sq <= TOLERANCE:
        even_energy_fraction = None
        odd_energy_fraction = None
    else:
        even_energy_fraction = even_l2_sq / full_l2_sq
        odd_energy_fraction = odd_l2_sq / full_l2_sq

    reconstruction_error = max(
        abs(centered[unit] - even[unit] - odd[unit])
        for unit in admissible)
    odd_pair_sum_error = max(
        abs(odd[unit] + odd[(target_residue - unit) % MODULUS])
        for unit in admissible)
    even_pair_difference_error = max(
        abs(even[unit] - even[(target_residue - unit) % MODULUS])
        for unit in admissible)

    return {
        "target_residue_mod_286": int(target_residue),
        "admissible_unit_count": len(admissible),
        "reflection_orbit_count": len(orbits),
        "fixed_orbit_count": sum(1 for orbit in orbits if len(orbit) == 1),
        "centered_full_l2": math.sqrt(full_l2_sq),
        "reflection_even_l2": math.sqrt(even_l2_sq),
        "reflection_odd_l2": math.sqrt(odd_l2_sq),
        "reflection_even_energy_fraction": even_energy_fraction,
        "reflection_odd_energy_fraction": odd_energy_fraction,
        "reflection_even_linf": max(abs(even[unit]) for unit in admissible),
        "reflection_odd_linf": max(abs(odd[unit]) for unit in admissible),
        "max_decomposition_reconstruction_error": reconstruction_error,
        "max_reflection_odd_pair_sum_error": odd_pair_sum_error,
        "max_reflection_even_pair_difference_error": (
            even_pair_difference_error),
        "largest_even_residue": max(
            (
                {
                    "unit_residue": int(unit),
                    "reflected_unit_residue": int(
                        (target_residue - unit) % MODULUS),
                    "value_abs": abs(even[unit]),
                    "value": even[unit],
                }
                for unit in admissible
            ),
            key=lambda row: row["value_abs"]),
        "largest_odd_residue": max(
            (
                {
                    "unit_residue": int(unit),
                    "reflected_unit_residue": int(
                        (target_residue - unit) % MODULUS),
                    "value_abs": abs(odd[unit]),
                    "value": odd[unit],
                }
                for unit in admissible
            ),
            key=lambda row: row["value_abs"]),
    }


def summarize_rows(rows):
    even_fractions = [
        row["reflection_even_energy_fraction"] for row in rows]
    odd_fractions = [
        row["reflection_odd_energy_fraction"] for row in rows]
    return {
        "target_residue_count": len(rows),
        "even_energy_fraction_summary": finite_summary(even_fractions),
        "odd_energy_fraction_summary": finite_summary(odd_fractions),
        "max_centered_full_l2": max(
            row["centered_full_l2"] for row in rows),
        "max_reflection_even_l2": max(
            row["reflection_even_l2"] for row in rows),
        "max_reflection_odd_l2": max(
            row["reflection_odd_l2"] for row in rows),
        "max_reflection_even_linf": max(
            row["reflection_even_linf"] for row in rows),
        "max_reflection_odd_linf": max(
            row["reflection_odd_linf"] for row in rows),
        "max_reconstruction_error": max(
            row["max_decomposition_reconstruction_error"] for row in rows),
        "max_reflection_odd_pair_sum_error": max(
            row["max_reflection_odd_pair_sum_error"] for row in rows),
        "max_reflection_even_pair_difference_error": max(
            row["max_reflection_even_pair_difference_error"] for row in rows),
        "worst_even_residue": max(
            rows,
            key=lambda row: row["reflection_even_energy_fraction"]),
        "best_odd_residue": max(
            rows,
            key=lambda row: row["reflection_odd_energy_fraction"]),
    }


def build_receipt():
    data = normalized_k286_matrix()
    matrix = data["active_matrix"]
    left, singular_values, right = np.linalg.svd(matrix, full_matrices=False)
    units = tuple(
        residue for residue in range(MODULUS)
        if math.gcd(residue, MODULUS) == 1)
    _, labels, character_table = _unit_character_table(MODULUS, units)

    mode_values = []
    for index in range(MODE_COUNT):
        mode_values.append(residue_mode_values(
            left, singular_values, right, index, units, labels,
            character_table, scaled=True))

    even_target_residues = tuple(range(0, MODULUS, 2))
    mode_rows = []
    for index, values in enumerate(mode_values):
        rows = [
            decompose_for_target(target_residue, values)
            for target_residue in even_target_residues
        ]
        mode_rows.append({
            "mode_index": index + 1,
            "singular_value": float(singular_values[index]),
            "scaled_mode": True,
            "rows": rows,
            "summary": summarize_rows(rows),
        })

    combined_values = {
        unit: sum(values[unit] for values in mode_values)
        for unit in units
    }
    combined_rows = [
        decompose_for_target(target_residue, combined_values)
        for target_residue in even_target_residues
    ]
    combined_summary = summarize_rows(combined_rows)
    reflection_fails_as_uniform_simplifier = (
        combined_summary["worst_even_residue"][
            "reflection_even_energy_fraction"] > 1.0 - 1e-9)

    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-two-mode-reflection-parity-audit",
        "source_commit": source_commit(),
        "status": "AUDIT_k286_two_mode_reflection_parity_not_proof",
        "question": (
            "Does ordered-pair reflection remove a universal part of the "
            "K_286 two-mode singular burden?"),
        "answer": (
            "Only partly.  Reflection-odd residue weights are algebraically "
            "invisible to any reflection-symmetric strict-central pair mass, "
            "and many target residues have a large odd component.  But target "
            "residue 0 mod 286 is essentially all reflection-even for the "
            "combined first two scaled modes, so reflection alone cannot be "
            "the universal two-mode bound."),
        "algebraic_identity": {
            "reflection_map": "r -> a-r mod 286",
            "centered_weight": (
                "gamma_a(r)=phi(r)-mean_{admissible r for a} phi(r)"),
            "even_part": (
                "gamma_even(r)=(gamma_a(r)+gamma_a(a-r))/2"),
            "odd_part": (
                "gamma_odd(r)=(gamma_a(r)-gamma_a(a-r))/2"),
            "odd_null_statement": (
                "If a signed or probability residue mass delta has "
                "delta(r)=delta(a-r), then sum_r delta(r)*gamma_odd(r)=0."),
            "identity_checked": True,
        },
        "target_residues_mod_286": list(even_target_residues),
        "mode_rows": mode_rows,
        "combined_top_two_scaled": {
            "description": (
                "Residue weights for sigma_1*u_1*vh_1 + "
                "sigma_2*u_2*vh_2, centered separately for each even target "
                "residue and decomposed into reflection-even/odd parts."),
            "rows": combined_rows,
            "summary": combined_summary,
        },
        "candidate": {
            "name": "K_286 two-mode reflection-even projection",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use ordered-pair reflection to discard the odd part of the "
                "two singular residue weights before asking for an analytic "
                "prime-pair moment estimate."),
            "prediction": (
                "If reflection is proof-relevant, the effective even burden "
                "should be uniformly smaller than the full two-mode burden "
                "for every even target residue."),
            "falsifier": (
                "A target residue whose two-mode coefficient is almost fully "
                "reflection-even means the symmetry does not by itself reduce "
                "the universal pointwise theorem target."),
            "smallest_next_test": (
                "After this falsifier, look for target-residue-specific "
                "analytic input: orbit mass control, raw adverse-drag major "
                "arc surplus, or a non-circular L2/moment theorem."),
        },
        "decision": (
            "AUDIT_k286_two_mode_reflection_parity_not_proof.  The odd-null "
            "identity is real structure, not decoration, but it is not a "
            "universal simplifier: residue 0 mod 286 keeps essentially the "
            "entire combined two-mode burden in the reflection-even subspace. "
            "The next acceptable route must be a pointwise unnormalized "
            "analytic estimate, not another finite-fit residual constant."),
        "status_boundary": (
            "Exact finite coefficient-geometry audit only.  It proves the "
            "reflection-odd algebraic null identity under reflection-symmetric "
            "mass, but no binary-prime moment theorem, no non-circular L2 "
            "target, no raw adverse-drag bound, no q286 threshold theorem, "
            "no strict-central Goldbach theorem, and no Goldbach proof."),
        "reflection_odd_null_identity_checked": True,
        "reflection_fails_as_universal_two_mode_simplifier": (
            reflection_fails_as_uniform_simplifier),
        "zero_mass_check_is_logical_bridge": False,
        "l2_target_non_circular_confirmed": False,
        "binary_prime_moment_theorem_proved": False,
        "raw_adverse_drag_bound_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
        "universal_pointwise_bound_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(json_ready(build_receipt()), indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8")
    receipt = json.loads(OUT.read_text(encoding="utf-8"))
    combined = receipt["combined_top_two_scaled"]["summary"]
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "combined_even_fraction_min": combined[
            "even_energy_fraction_summary"]["minimum"],
        "combined_even_fraction_max": combined[
            "even_energy_fraction_summary"]["maximum"],
        "combined_odd_fraction_max": combined[
            "odd_energy_fraction_summary"]["maximum"],
        "worst_even_target_residue": combined["worst_even_residue"][
            "target_residue_mod_286"],
        "best_odd_target_residue": combined["best_odd_residue"][
            "target_residue_mod_286"],
        "reflection_fails_as_universal_two_mode_simplifier": (
            receipt["reflection_fails_as_universal_two_mode_simplifier"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
