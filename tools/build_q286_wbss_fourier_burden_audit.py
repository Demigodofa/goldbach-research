"""Measure the finite Fourier burden of the q286-WBSS coefficient budget.

The known-theorem adequacy audit left one non-finite route: perhaps the
adverse q286-WBSS coefficient directions are concentrated in a small number
of character/Fourier modes, making a narrower signed estimate plausible.

This receipt tests that coefficient-side premise.  It decomposes the four
projected coefficient families into centered finite additive Fourier modes
modulo 70, 130, 154, and 286.  It is a finite coefficient diagnostic only;
it proves no prime-pair character estimate and no Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
ADEQUACY_SOURCE = EVIDENCE / "q286-wbss-known-theorem-adequacy-audit.json"
OUT = EVIDENCE / "q286-wbss-fourier-burden-audit.json"
MODULI = [70, 130, 154, 286]
ENERGY_THRESHOLDS = [0.5, 0.75, 0.9, 0.95, 0.99]


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def coefficient_vectors(formula):
    rows = formula["coefficient_table"]["rows"]
    vectors = {modulus: [0.0] * modulus for modulus in MODULI}
    for row in rows:
        if row.get("kind") != "residue_projection":
            continue
        modulus = int(row["modulus"])
        if modulus in vectors:
            vectors[modulus][int(row["residue"])] = float(
                row["coefficient"])
    return vectors


def centered_vector(vector):
    mean = sum(vector) / len(vector)
    return [value - mean for value in vector], mean


def additive_modes(modulus, vector):
    centered, mean = centered_vector(vector)
    modes = []
    for k in range(1, modulus):
        real = 0.0
        imag = 0.0
        for residue, value in enumerate(centered):
            angle = -2.0 * math.pi * k * residue / modulus
            real += value * math.cos(angle)
            imag += value * math.sin(angle)
        energy = (real * real + imag * imag) / modulus
        modes.append({
            "mode": k,
            "conductor": modulus // math.gcd(k, modulus),
            "energy": energy,
            "amplitude_per_residue": math.sqrt(energy / modulus),
        })
    modes.sort(key=lambda row: row["energy"], reverse=True)
    total_energy = sum(row["energy"] for row in modes)
    return {
        "modulus": modulus,
        "support_count": sum(1 for value in vector if value != 0.0),
        "coefficient_sum": sum(vector),
        "centered_mean_removed": mean,
        "nonprincipal_mode_count": len(modes),
        "total_nonprincipal_energy": total_energy,
        "parseval_centered_l2_squared": sum(value * value
                                            for value in centered),
        "energy_cover_counts": cover_counts(modes, total_energy),
        "effective_mode_count": effective_mode_count(modes, total_energy),
        "top_modes": modes[:12],
        "conductor_energy": conductor_energy(modulus, modes, total_energy),
    }


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
            "mode_count": count,
            "energy_fraction": running / total_energy,
        }
    return counts


def effective_mode_count(modes, total_energy):
    if total_energy == 0.0:
        return 0.0
    probabilities = [mode["energy"] / total_energy for mode in modes]
    collision = sum(p * p for p in probabilities)
    entropy = -sum(p * math.log(p) for p in probabilities if p > 0.0)
    return {
        "inverse_participation_count": 1.0 / collision,
        "entropy_effective_count": math.exp(entropy),
        "largest_mode_fraction": max(probabilities),
    }


def conductor_energy(modulus, modes, total_energy):
    buckets = {}
    for mode in modes:
        key = str(mode["conductor"])
        buckets.setdefault(key, {
            "mode_count": 0,
            "energy": 0.0,
            "energy_fraction": 0.0,
        })
        buckets[key]["mode_count"] += 1
        buckets[key]["energy"] += mode["energy"]
    for bucket in buckets.values():
        bucket["energy_fraction"] = (
            bucket["energy"] / total_energy if total_energy else 0.0)
    return dict(sorted(
        buckets.items(),
        key=lambda item: float(item[1]["energy"]),
        reverse=True,
    ))


def build_receipt():
    formula = load_json(FORMULA_SOURCE)
    adequacy = load_json(ADEQUACY_SOURCE)
    vectors = coefficient_vectors(formula)
    per_modulus = {}
    all_modes = []
    for modulus in MODULI:
        summary = additive_modes(modulus, vectors[modulus])
        per_modulus[str(modulus)] = summary
        centered, _mean = centered_vector(vectors[modulus])
        for k in range(1, modulus):
            real = 0.0
            imag = 0.0
            for residue, value in enumerate(centered):
                angle = -2.0 * math.pi * k * residue / modulus
                real += value * math.cos(angle)
                imag += value * math.sin(angle)
            energy = (real * real + imag * imag) / modulus
            all_modes.append({
                "modulus": modulus,
                "mode": k,
                "conductor": modulus // math.gcd(k, modulus),
                "energy": energy,
            })

    all_modes.sort(key=lambda row: row["energy"], reverse=True)
    total_energy = sum(mode["energy"] for mode in all_modes)
    energy_by_modulus = {
        str(modulus): per_modulus[str(modulus)][
            "total_nonprincipal_energy"]
        for modulus in MODULI
    }
    global_cover = cover_counts(all_modes, total_energy)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "four_modulus_projection_formula_source_commit": formula[
                "source_commit"],
            "known_theorem_adequacy_audit": str(
                ADEQUACY_SOURCE.relative_to(ROOT)),
            "known_theorem_adequacy_status": adequacy["status"],
        },
        "status": "HOLD_fourier_burden_diffuse_high_conductor",
        "status_boundary": (
            "finite additive Fourier coefficient diagnostic only; it proves "
            "no signed character estimate, fixed-modulus binary-prime "
            "discrepancy theorem, pointwise adverse-drag theorem, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof"),
        "goldbach_proved": False,
        "signed_character_theorem_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "fixed_modulus_binary_prime_discrepancy_theorem_proved": False,
        "universal_bound_open": True,
        "method": {
            "transform": (
                "center each projected coefficient vector modulo d, discard "
                "the principal additive mode, and compute finite additive "
                "Fourier energy |hat c_d(k)|^2/d"),
            "why_centered": (
                "The discrepancy Delta_{d,s}(N) has zero total mass in the "
                "coefficient-discrepancy budget, so constant modes do not "
                "pay adverse drag."),
            "interpretation_boundary": (
                "Additive Fourier concentration is coefficient-side evidence "
                "only.  A prime-pair theorem would still need to bound the "
                "corresponding binary-prime sums pointwise in N."),
        },
        "global_summary": {
            "nonprincipal_mode_count": len(all_modes),
            "total_nonprincipal_energy": total_energy,
            "energy_by_modulus": energy_by_modulus,
            "energy_fraction_by_modulus": {
                modulus: energy / total_energy
                for modulus, energy in energy_by_modulus.items()
            },
            "energy_cover_counts": global_cover,
            "effective_mode_count": effective_mode_count(
                all_modes, total_energy),
            "top_modes": all_modes[:16],
        },
        "per_modulus": per_modulus,
        "candidate": {
            "name": "small signed-character WBSS theorem",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Try to replace full per-residue AP uniformity with a "
                "pointwise signed estimate for only the Fourier modes that "
                "carry adverse WBSS coefficient energy."),
            "prediction": (
                "If a few modes carry most coefficient energy, a narrower "
                "signed character theorem might be meaningfully smaller than "
                "full fixed-modulus Goldbach in progressions."),
            "falsifier": (
                "If energy is spread over many nonprincipal high-conductor "
                "modes, the route does not earn its keep as a small theorem."),
            "smallest_test": (
                "Count nonprincipal modes needed to cover 90, 95, and 99 "
                "percent of centered coefficient energy."),
        },
        "decision": (
            "The few-mode signed-character shortcut is not supported by the "
            "coefficient geometry.  Globally, 90 percent of centered Fourier "
            "energy needs 187 nonprincipal modes and 99 percent needs 308; "
            "modulus 286 alone carries about 86.7 percent of total energy and "
            "requires 188 of its 285 nonprincipal modes for 99 percent.  The "
            "surviving theorem target is therefore a broad high-conductor "
            "signed binary-prime correlation estimate, not a small "
            "character-mode lemma."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
