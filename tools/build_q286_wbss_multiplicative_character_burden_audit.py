"""Measure the multiplicative-character burden of the WBSS projections.

The additive Fourier burden audit showed that the coefficient load is not a
few additive modes.  This receipt repeats the burden test in the natural
Dirichlet-character coordinates of the unit groups for moduli
70, 130, 154, and 286.

It is finite coefficient algebra only.  It proves no character-sum theorem,
fixed-modulus binary-prime discrepancy theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import itertools
import json
import math
import subprocess
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
ADDITIVE_SOURCE = EVIDENCE / "q286-wbss-fourier-burden-audit.json"
OUT = EVIDENCE / "q286-wbss-multiplicative-character-burden-audit.json"
MODULUS_FACTORS = {
    70: (5, 7),
    130: (5, 13),
    154: (7, 11),
    286: (11, 13),
}
ENERGY_THRESHOLDS = [0.5, 0.75, 0.9, 0.95, 0.99]


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def primitive_root(prime):
    units = set(range(1, prime))
    for candidate in range(2, prime):
        generated = {pow(candidate, exponent, prime)
                     for exponent in range(prime - 1)}
        if generated == units:
            return candidate
    raise ValueError(f"no primitive root found for {prime}")


def exponent_map(prime):
    root = primitive_root(prime)
    return {
        "primitive_root": root,
        "exponent_by_residue": {
            pow(root, exponent, prime): exponent
            for exponent in range(prime - 1)
        },
        "residue_by_exponent": [
            pow(root, exponent, prime)
            for exponent in range(prime - 1)
        ],
    }


def coefficient_rows_by_modulus(formula):
    by_modulus = {modulus: {} for modulus in MODULUS_FACTORS}
    for row in formula["coefficient_table"]["rows"]:
        if row.get("kind") != "residue_projection":
            continue
        modulus = int(row["modulus"])
        if modulus in by_modulus:
            by_modulus[modulus][int(row["residue"])] = float(
                row["coefficient"])
    return by_modulus


def coefficient_grid(modulus, factors, coefficients, maps):
    shape = tuple(factor - 1 for factor in factors)
    grid = np.zeros(shape, dtype=np.complex128)
    for residue, value in coefficients.items():
        index = tuple(
            maps[factor]["exponent_by_residue"][residue % factor]
            for factor in factors
        )
        grid[index] = value
    return grid


def cover_counts(modes, total_energy):
    counts = {}
    for threshold in ENERGY_THRESHOLDS:
        running = 0.0
        count = 0
        for mode in modes:
            running += mode["energy"]
            count += 1
            if running / total_energy >= threshold:
                break
        counts[str(threshold)] = {
            "character_count": count,
            "energy_fraction": running / total_energy,
        }
    return counts


def effective_character_count(modes, total_energy):
    probabilities = [mode["energy"] / total_energy for mode in modes]
    collision = sum(p * p for p in probabilities)
    entropy = -sum(p * math.log(p) for p in probabilities if p > 0.0)
    return {
        "inverse_participation_count": 1.0 / collision,
        "entropy_effective_count": math.exp(entropy),
        "largest_character_fraction": max(probabilities),
    }


def character_rows(modulus, factors, coefficients, maps):
    grid = coefficient_grid(modulus, factors, coefficients, maps)
    mean = complex(np.mean(grid))
    centered = grid - mean
    transform = np.fft.fftn(centered) / centered.size
    reconstruction = np.fft.ifftn(transform * transform.size)
    energy = np.abs(transform) ** 2
    modes = []
    for frequency in itertools.product(*(range(size)
                                         for size in transform.shape)):
        if all(item == 0 for item in frequency):
            continue
        value = complex(transform[frequency])
        mode_energy = float(energy[frequency])
        modes.append({
            "frequency": list(frequency),
            "energy": mode_energy,
            "abs_coefficient": abs(value),
            "coefficient_real": value.real,
            "coefficient_imag": value.imag,
            "zero_axis": any(item == 0 for item in frequency),
        })
    modes.sort(key=lambda row: row["energy"], reverse=True)
    total_energy = sum(row["energy"] for row in modes)
    return {
        "modulus": modulus,
        "factors": list(factors),
        "unit_count": int(grid.size),
        "primitive_roots": {
            str(factor): maps[factor]["primitive_root"]
            for factor in factors
        },
        "support_count": len(coefficients),
        "unit_mean_removed_real": mean.real,
        "unit_mean_removed_imag": mean.imag,
        "nonprincipal_character_count": len(modes),
        "total_nonprincipal_energy": total_energy,
        "parseval_mean_square": float(np.mean(np.abs(centered) ** 2)),
        "parseval_error": abs(
            float(np.mean(np.abs(centered) ** 2)) - total_energy),
        "max_reconstruction_error": float(
            np.max(np.abs(reconstruction - centered))),
        "energy_cover_counts": cover_counts(modes, total_energy),
        "effective_character_count": effective_character_count(
            modes, total_energy),
        "zero_axis_nonzero_character_count": sum(
            1 for mode in modes
            if mode["zero_axis"] and mode["energy"] > 1e-20),
        "top_characters": modes[:12],
    }


def build_receipt():
    formula = load_json(FORMULA_SOURCE)
    additive = load_json(ADDITIVE_SOURCE)
    coefficient_by_modulus = coefficient_rows_by_modulus(formula)
    maps = {
        factor: exponent_map(factor)
        for factors in MODULUS_FACTORS.values()
        for factor in factors
    }
    per_modulus = {}
    all_modes = []
    for modulus, factors in MODULUS_FACTORS.items():
        row = character_rows(
            modulus, factors, coefficient_by_modulus[modulus], maps)
        per_modulus[str(modulus)] = row
        grid = coefficient_grid(
            modulus, factors, coefficient_by_modulus[modulus], maps)
        centered = grid - np.mean(grid)
        transform = np.fft.fftn(centered) / centered.size
        energy = np.abs(transform) ** 2
        for frequency in itertools.product(*(range(size)
                                             for size in transform.shape)):
            if all(item == 0 for item in frequency):
                continue
            all_modes.append({
                "modulus": modulus,
                "frequency": list(frequency),
                "energy": float(energy[frequency]),
                "zero_axis": any(item == 0 for item in frequency),
            })

    all_modes.sort(key=lambda row: row["energy"], reverse=True)
    total_energy = sum(row["energy"] for row in all_modes)
    energy_by_modulus = {
        modulus: row["total_nonprincipal_energy"]
        for modulus, row in per_modulus.items()
    }
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "four_modulus_projection_formula_source_commit": formula[
                "source_commit"],
            "additive_fourier_burden_audit": str(
                ADDITIVE_SOURCE.relative_to(ROOT)),
            "additive_fourier_burden_status": additive["status"],
        },
        "status": "HOLD_multiplicative_character_burden_broad",
        "status_boundary": (
            "finite multiplicative-character coefficient diagnostic only; "
            "it proves no character-sum bound, fixed-modulus binary-prime "
            "discrepancy theorem, pointwise adverse-drag theorem, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof"),
        "goldbach_proved": False,
        "multiplicative_character_theorem_proved": False,
        "fixed_modulus_binary_prime_discrepancy_theorem_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "universal_bound_open": True,
        "method": {
            "coordinate_choice": (
                "Use primitive-root exponent coordinates on each odd prime "
                "factor of the unit group: 70=(5,7), 130=(5,13), "
                "154=(7,11), and 286=(11,13)."),
            "transform": (
                "Subtract the unit-group mean and apply normalized finite "
                "Fourier transform on the exponent grid.  These are the "
                "multiplicative Dirichlet-character coordinates of the "
                "projected coefficient vector."),
            "interpretation_boundary": (
                "This only measures coefficient support in character space. "
                "A proof still needs pointwise binary-prime correlation "
                "bounds for the corresponding character sums."),
        },
        "global_summary": {
            "nonprincipal_character_count": len(all_modes),
            "total_nonprincipal_energy": total_energy,
            "energy_by_modulus": energy_by_modulus,
            "energy_fraction_by_modulus": {
                modulus: energy / total_energy
                for modulus, energy in energy_by_modulus.items()
            },
            "energy_cover_counts": cover_counts(all_modes, total_energy),
            "effective_character_count": effective_character_count(
                all_modes, total_energy),
            "top_characters": all_modes[:20],
        },
        "per_modulus": per_modulus,
        "comparison_to_additive_burden": {
            "additive_global_modes_for_99_percent": additive[
                "global_summary"]["energy_cover_counts"]["0.99"][
                    "mode_count"],
            "multiplicative_global_characters_for_99_percent": cover_counts(
                all_modes, total_energy)["0.99"]["character_count"],
            "additive_mod286_modes_for_99_percent": additive[
                "per_modulus"]["286"]["energy_cover_counts"]["0.99"][
                    "mode_count"],
            "multiplicative_mod286_characters_for_99_percent": (
                per_modulus["286"]["energy_cover_counts"]["0.99"][
                    "character_count"]),
        },
        "candidate": {
            "name": "multiplicative-character WBSS theorem package",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use Dirichlet-character coordinates rather than additive "
                "Fourier coordinates for the fixed-modulus AP theorem target."),
            "prediction": (
                "Multiplicative characters should compress the coefficient "
                "burden relative to additive modes, but the remaining burden "
                "may still be too broad for a small theorem."),
            "falsifier": (
                "If nearly all energy is carried by a few characters, the "
                "small signed-character route is alive; if many characters "
                "are required, the route remains a broad AP-correlation "
                "problem."),
            "smallest_test": (
                "Count characters needed to cover 90, 95, and 99 percent of "
                "centered coefficient energy."),
        },
        "decision": (
            "Multiplicative characters are the right language and compress "
            "the burden relative to additive Fourier modes, but not to a "
            "small theorem.  Globally, 99 percent of centered multiplicative "
            "energy still needs 77 nonprincipal characters; modulus 286 "
            "carries about 70.2 percent of total energy and needs 50 "
            "characters for 99 percent.  The next theorem target is therefore "
            "a broad multiplicative-character binary-prime correlation "
            "package, not a tiny signed-character shortcut."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
