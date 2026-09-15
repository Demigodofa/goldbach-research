"""Audit the character-frequency burden of the q286 centered error.

The local main-term audit left one real bridge gap:

    RawFull(N) = LocalMain_a(N) + CenteredError_a(N),
    CenteredError_a(N) > -LocalMain_a(N).

This receipt decomposes the fixed centered coefficient into Dirichlet
character supports on U_10010.  The aim is to identify which lower CRT moduli
an analytic signed-prime correlation theorem would actually need to control.
It is a finite coefficient audit only, not a prime-correlation estimate.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-centered-character-burden-audit.json"
PERIOD = 10010
TOLERANCE = 1e-8
FACTOR_PRIMES = (5, 7, 11, 13)

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_frequency_resolved_fourier import (  # noqa: E402
    _unit_character_table,
)
from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
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
    values = tuple(float(value) for value in values)
    if not values:
        return {
            "count": 0,
            "minimum": None,
            "maximum": None,
            "mean": None,
        }
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def support_label(support):
    if not support:
        return "principal"
    return "x".join(str(prime) for prime in support)


def natural_modulus(support):
    modulus = 2
    for prime in support:
        modulus *= prime
    return modulus


def admissible_units(target_residue, units):
    return tuple(
        unit for unit in units
        if math.gcd((target_residue - unit) % PERIOD, PERIOD) == 1)


def build_receipt(tolerance=TOLERANCE):
    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    units = tuple(
        residue for residue in range(PERIOD)
        if math.gcd(residue, PERIOD) == 1)
    if tuple(coefficient["aggregate_coefficient_by_unit_residue"]) != units:
        raise AssertionError("unexpected unit residue ordering")

    values = np.asarray([
        complex(coefficient["aggregate_coefficient_by_unit_residue"][unit])
        for unit in units
    ], dtype=np.complex128)
    principal_mean = complex(np.mean(values))
    centered = values - principal_mean
    _, labels, character_table = _unit_character_table(PERIOD, units)
    character_coefficients = (
        np.conjugate(character_table) @ centered / len(units))

    support_to_indices = {}
    for index, label in enumerate(labels):
        support = tuple(
            prime for prime, exponent in zip(FACTOR_PRIMES, label)
            if exponent != 0)
        support_to_indices.setdefault(support, []).append(index)

    total_energy = float(np.sum(np.abs(character_coefficients) ** 2))
    if total_energy <= tolerance:
        raise AssertionError("expected nonzero centered character energy")

    components = {"principal": np.full(
        len(units), principal_mean, dtype=np.complex128)}
    support_rows = []
    reconstructed = np.array(components["principal"], copy=True)
    for support, indices in sorted(support_to_indices.items()):
        if not support:
            continue
        masked = np.zeros_like(character_coefficients)
        masked[indices] = character_coefficients[indices]
        energy = float(np.sum(np.abs(masked) ** 2))
        if energy <= tolerance:
            continue
        component = character_table.T @ masked
        components[support_label(support)] = component
        reconstructed += component

        modulus = natural_modulus(support)
        grouped = {}
        for unit, value in zip(units, component):
            grouped.setdefault(unit % modulus, []).append(value)
        grouped_means = {
            residue: sum(items, 0.0j) / len(items)
            for residue, items in grouped.items()}
        descent_error = max(
            abs(value - grouped_means[unit % modulus])
            for unit, value in zip(units, component))
        component_scale = max(1.0, float(np.linalg.norm(component)))
        support_rows.append({
            "support": support,
            "support_label": support_label(support),
            "natural_modulus": modulus,
            "character_count": len(indices),
            "unit_residue_count": len(grouped_means),
            "energy": energy,
            "energy_fraction": energy / total_energy,
            "component_l2": float(np.linalg.norm(component)),
            "descent_relative_error": float(
                descent_error / component_scale),
            "descends_to_natural_modulus": bool(
                descent_error / component_scale <= tolerance),
        })

    support_rows.sort(key=lambda row: row["energy_fraction"], reverse=True)
    reconstruction_error = float(
        np.linalg.norm(reconstructed - values)
        / max(1.0, float(np.linalg.norm(values))))

    cumulative = 0.0
    dominant_support_rows = []
    for row in support_rows:
        cumulative += row["energy_fraction"]
        dominant_support_rows.append(row)
        if cumulative >= 0.99:
            break

    local_ratios_by_component = {
        label: [] for label in components
    }
    full_local_ratios = []
    removal_minima = {
        label: math.inf for label in components if label != "principal"
    }
    removal_nonpositive_counts = {
        label: 0 for label in components if label != "principal"
    }
    unit_index = {unit: index for index, unit in enumerate(units)}
    target_rows = []
    for target_residue in range(0, PERIOD, 2):
        support = admissible_units(target_residue, units)
        indices = [unit_index[unit] for unit in support]
        local_by_component = {}
        for label, component in components.items():
            local_mean = complex(np.mean(component[indices]))
            ratio = local_mean.real / principal_mean.real
            local_by_component[label] = ratio
            local_ratios_by_component[label].append(ratio)
        full_ratio = math.fsum(local_by_component.values())
        full_local_ratios.append(full_ratio)
        for label in removal_minima:
            removed_ratio = full_ratio - local_by_component[label]
            removal_minima[label] = min(removal_minima[label], removed_ratio)
            if removed_ratio <= tolerance:
                removal_nonpositive_counts[label] += 1
        target_rows.append({
            "target_residue": target_residue,
            "admissible_support_size": len(support),
            "full_local_to_principal_ratio": full_ratio,
            "component_local_to_principal_ratios": local_by_component,
        })

    weakest_local_row = min(
        target_rows, key=lambda row: row["full_local_to_principal_ratio"])
    support_local_rows = []
    for row in support_rows:
        label = row["support_label"]
        ratios = local_ratios_by_component[label]
        support_local_rows.append({
            **row,
            "local_contribution_to_principal_ratio_summary": finite_summary(
                ratios),
            "local_contribution_abs_ratio_summary": finite_summary(
                abs(ratio) for ratio in ratios),
            "removing_component_minimum_full_local_ratio": (
                removal_minima[label]),
            "removing_component_nonpositive_local_count": (
                removal_nonpositive_counts[label]),
        })

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "arithmetic_period": PERIOD,
        "unit_group_order": len(units),
        "factor_primes": FACTOR_PRIMES,
        "assembled_quotients": coefficient["assembled_quotients"],
        "principal_mean": principal_mean,
        "total_centered_character_energy": total_energy,
        "support_rows": support_local_rows,
        "dominant_99_percent_energy_support_rows": dominant_support_rows,
        "dominant_99_percent_energy_support_count": len(
            dominant_support_rows),
        "dominant_99_percent_energy_fraction": math.fsum(
            row["energy_fraction"] for row in dominant_support_rows),
        "nonzero_natural_moduli": sorted(
            row["natural_modulus"] for row in support_rows),
        "largest_support_energy_fraction": support_rows[0][
            "energy_fraction"],
        "top_three_support_energy_fraction": math.fsum(
            row["energy_fraction"] for row in support_rows[:3]),
        "maximum_support_descent_relative_error": max(
            row["descent_relative_error"] for row in support_rows),
        "component_reconstruction_relative_error": reconstruction_error,
        "all_nonzero_supports_descend_to_lower_moduli": all(
            row["descends_to_natural_modulus"] for row in support_rows),
        "full_modulus_10010_support_present": any(
            row["natural_modulus"] == PERIOD for row in support_rows),
        "even_target_residue_count": len(target_rows),
        "full_local_to_principal_ratio_summary": finite_summary(
            full_local_ratios),
        "weakest_local_main_row": weakest_local_row,
        "support_component_removal_nonpositive_counts": (
            removal_nonpositive_counts),
        "candidate_mechanism": (
            "The q286 centered-error burden is character-broad inside a few "
            "lower CRT supports rather than genuinely full-modulus 10010."),
        "prediction": (
            "A proof attempt should first seek signed binary-prime "
            "correlation estimates for the dominant natural moduli 286, 154, "
            "and 70, then bound the small remaining supports as a tail."),
        "falsifier": (
            "Substantial centered-character energy on the full 10010 support "
            "or a long tail of many comparable supports would falsify this "
            "lower-modulus compression."),
        "smallest_new_problem": (
            "Prove a three-dominant-support q286 signed-correlation theorem "
            "for natural moduli 286, 154, and 70, with an explicit tail bound "
            "for the remaining lower supports, strong enough that the total "
            "centered error is greater than minus the positive local main "
            "term in every even residue modulo 10010."),
        "decision": (
            "Keep the local positive-main-term signed-witness route, but "
            "replace a vague q10010 uniformity demand with a lower-modulus "
            "character-correlation burden dominated by three CRT supports."),
        "status_boundary": (
            "finite coefficient-spectrum audit only; no binary-prime "
            "correlation theorem, no q286 threshold theorem, no "
            "strict-central Goldbach theorem, and no Goldbach proof"),
        "centered_character_burden_measured": True,
        "three_dominant_support_problem_defined": True,
        "pointwise_centered_error_estimate_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(json_ready(receipt), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(json.dumps(json_ready({
        "wrote": str(OUT.relative_to(ROOT)),
        "dominant_99_percent_energy_support_count": (
            receipt["dominant_99_percent_energy_support_count"]),
        "dominant_99_percent_energy_fraction": (
            receipt["dominant_99_percent_energy_fraction"]),
        "top_three_support_energy_fraction": (
            receipt["top_three_support_energy_fraction"]),
        "nonzero_natural_moduli": receipt["nonzero_natural_moduli"],
        "full_modulus_10010_support_present": (
            receipt["full_modulus_10010_support_present"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }), sort_keys=True))


if __name__ == "__main__":
    main()
