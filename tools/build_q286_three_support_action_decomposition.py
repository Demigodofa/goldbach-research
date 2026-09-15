"""Decompose actual q286 raw actions into the three dominant supports.

The centered character-burden audit found that the fixed coefficient energy is
dominated by natural moduli 286, 154, and 70.  This receipt asks whether that
coefficient-side compression is also visible on actual hard prime-pair rows.

It is a finite diagnostic only.  It does not prove the signed-correlation
estimate needed for Goldbach.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-three-support-action-decomposition.json"
PERIOD = 10010
TOLERANCE = 1e-8
FACTOR_PRIMES = (5, 7, 11, 13)
DEFAULT_TARGETS = (
    14138,
    14996,
    88346,
    90080,
    94856,
    194384,
    1222142,
    1240888,
    1242118,
    1379072,
)

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_frequency_resolved_fourier import (  # noqa: E402
    _unit_character_table,
)
from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    _complex_fsum,
    _prime_table,
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


def build_components(tolerance):
    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    units = tuple(
        residue for residue in range(PERIOD)
        if math.gcd(residue, PERIOD) == 1)
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

    support_rows = []
    components = {
        "principal": np.full(len(units), principal_mean, dtype=np.complex128)
    }
    total_energy = float(np.sum(np.abs(character_coefficients) ** 2))
    for support, indices in sorted(support_to_indices.items()):
        if not support:
            continue
        masked = np.zeros_like(character_coefficients)
        masked[indices] = character_coefficients[indices]
        energy = float(np.sum(np.abs(masked) ** 2))
        if energy <= tolerance:
            continue
        label = support_label(support)
        component = character_table.T @ masked
        components[label] = component
        support_rows.append({
            "support": support,
            "support_label": label,
            "natural_modulus": natural_modulus(support),
            "character_count": len(indices),
            "energy": energy,
            "energy_fraction": energy / total_energy,
        })

    support_rows.sort(key=lambda row: row["energy_fraction"], reverse=True)
    top_three_labels = tuple(row["support_label"] for row in support_rows[:3])
    coefficient_by_unit = {
        unit: complex(value) for unit, value in zip(units, values)}
    local_mean_by_even_residue = {}
    for target_residue in range(0, PERIOD, 2):
        admissible = admissible_units(target_residue, units)
        local_mean_by_even_residue[target_residue] = (
            _complex_fsum(coefficient_by_unit[unit] for unit in admissible)
            / len(admissible))
    return {
        "coefficient": coefficient,
        "units": units,
        "components": components,
        "support_rows": support_rows,
        "top_three_labels": top_three_labels,
        "principal_mean": principal_mean,
        "coefficient_by_unit": coefficient_by_unit,
        "local_mean_by_even_residue": local_mean_by_even_residue,
    }


def build_receipt(targets=DEFAULT_TARGETS, tolerance=TOLERANCE):
    targets = tuple(int(target) for target in targets)
    if not targets or any(target < 40 or target % 2 for target in targets):
        raise ValueError("targets must be even integers >=40")
    built = build_components(tolerance)
    coefficient = built["coefficient"]
    units = built["units"]
    components = built["components"]
    support_rows = built["support_rows"]
    top_three_labels = built["top_three_labels"]
    principal_mean = built["principal_mean"]
    coefficient_by_unit = built["coefficient_by_unit"]
    local_mean_by_even_residue = built["local_mean_by_even_residue"]
    unit_index = {unit: index for index, unit in enumerate(units)}
    primes = _prime_table(max(targets))

    rows = []
    maximum_reconstruction_error = 0.0
    for target in targets:
        lower = target // 3
        upper = target - lower
        contribution_sums = {label: 0.0j for label in components}
        pair_count = 0
        total_weight = 0.0
        for prime in range(max(2, lower + 1), min(target, upper)):
            partner = target - prime
            if primes[prime] and primes[partner]:
                pair_count += 1
                weight = math.log(prime) * math.log(partner)
                total_weight += weight
                index = unit_index[prime % PERIOD]
                for label, component in components.items():
                    contribution_sums[label] += component[index] * weight

        direct = _complex_fsum(
            coefficient_by_unit[prime % PERIOD]
            * math.log(prime) * math.log(target - prime)
            for prime in range(max(2, lower + 1), min(target, upper))
            if primes[prime] and primes[target - prime])
        reconstructed = _complex_fsum(contribution_sums.values())
        reconstruction_error = abs(reconstructed - direct) / max(
            1.0, abs(reconstructed), abs(direct))
        maximum_reconstruction_error = max(
            maximum_reconstruction_error, reconstruction_error)

        principal = contribution_sums["principal"]
        top_three_centered = _complex_fsum(
            contribution_sums[label] for label in top_three_labels)
        tail = _complex_fsum(
            value for label, value in contribution_sums.items()
            if label not in ("principal", *top_three_labels))
        principal_plus_top_three = principal + top_three_centered
        target_residue = target % PERIOD
        local_main = (
            local_mean_by_even_residue[target_residue] * total_weight)
        centered_error = direct - local_main
        local_scale = local_main.real
        principal_scale = principal.real
        component_ratios = {
            label: (
                float(value.real / principal_scale)
                if abs(principal_scale) > tolerance else math.nan)
            for label, value in contribution_sums.items()
        }
        rows.append({
            "target": target,
            "target_residue": target_residue,
            "strict_central_interval": (lower, upper),
            "ordered_central_prime_pair_count": pair_count,
            "total_prime_pair_weight": total_weight,
            "principal_contribution": principal,
            "local_main_contribution": local_main,
            "top_three_centered_contribution": top_three_centered,
            "tail_centered_contribution": tail,
            "principal_plus_top_three_contribution": (
                principal_plus_top_three),
            "direct_weighted_prime_correlation": direct,
            "component_contributions_to_principal_ratio": component_ratios,
            "local_main_to_principal_ratio": (
                float(local_main.real / principal_scale)
                if abs(principal_scale) > tolerance else math.nan),
            "centered_error_to_local_main_ratio": (
                float(centered_error.real / local_scale)
                if abs(local_scale) > tolerance else math.nan),
            "top_three_centered_to_principal_ratio": (
                float(top_three_centered.real / principal_scale)
                if abs(principal_scale) > tolerance else math.nan),
            "tail_centered_to_principal_ratio": (
                float(tail.real / principal_scale)
                if abs(principal_scale) > tolerance else math.nan),
            "principal_plus_top_three_to_principal_ratio": (
                float(principal_plus_top_three.real / principal_scale)
                if abs(principal_scale) > tolerance else math.nan),
            "full_action_to_principal_ratio": (
                float(direct.real / principal_scale)
                if abs(principal_scale) > tolerance else math.nan),
            "direct_action_positive": bool(direct.real > tolerance),
            "principal_plus_top_three_positive": bool(
                principal_plus_top_three.real > tolerance),
            "tail_changes_sign_decision": bool(
                (principal_plus_top_three.real > tolerance)
                != (direct.real > tolerance)),
            "support_reconstruction_relative_error": reconstruction_error,
        })

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "arithmetic_period": PERIOD,
        "targets": targets,
        "assembled_quotients": coefficient["assembled_quotients"],
        "principal_mean": principal_mean,
        "support_rows": support_rows,
        "top_three_support_labels": top_three_labels,
        "top_three_natural_moduli": [
            row["natural_modulus"] for row in support_rows[:3]],
        "top_three_energy_fraction": math.fsum(
            row["energy_fraction"] for row in support_rows[:3]),
        "rows": rows,
        "tested_target_count": len(rows),
        "full_action_positive_count": sum(
            row["direct_action_positive"] for row in rows),
        "principal_plus_top_three_positive_count": sum(
            row["principal_plus_top_three_positive"] for row in rows),
        "tail_changes_sign_decision_count": sum(
            row["tail_changes_sign_decision"] for row in rows),
        "nonpositive_full_targets": [
            row["target"] for row in rows
            if not row["direct_action_positive"]],
        "nonpositive_principal_plus_top_three_targets": [
            row["target"] for row in rows
            if not row["principal_plus_top_three_positive"]],
        "tail_changed_sign_targets": [
            row["target"] for row in rows
            if row["tail_changes_sign_decision"]],
        "tail_centered_to_principal_ratio_summary": finite_summary(
            row["tail_centered_to_principal_ratio"] for row in rows),
        "top_three_centered_to_principal_ratio_summary": finite_summary(
            row["top_three_centered_to_principal_ratio"] for row in rows),
        "full_action_to_principal_ratio_summary": finite_summary(
            row["full_action_to_principal_ratio"] for row in rows),
        "centered_error_to_local_main_ratio_summary": finite_summary(
            row["centered_error_to_local_main_ratio"] for row in rows),
        "maximum_support_reconstruction_relative_error": (
            maximum_reconstruction_error),
        "candidate_mechanism": (
            "The coefficient-energy compression to moduli 286, 154, and 70 "
            "is action-level useful if principal plus those three supports "
            "preserves the sign of actual hard q286 rows."),
        "prediction": (
            "On hard rows, tail terms should be smaller than the three "
            "dominant supports and should rarely decide positivity."),
        "falsifier": (
            "If the tail changes the sign decision on the hard-row fixture, "
            "or if principal plus the three dominant supports is often "
            "nonpositive when the full action is positive, then the "
            "three-support theorem target is too narrow."),
        "decision": (
            "Use this finite diagnostic to decide whether the next theorem "
            "can prioritize E_286, E_154, and E_70 with a tail bound, or "
            "whether the small-energy tail must remain part of the main "
            "signed-correlation problem."),
        "status_boundary": (
            "finite selected-row support-action decomposition only; no "
            "pointwise signed-prime correlation theorem, no q286 threshold "
            "theorem, no strict-central Goldbach theorem, and no Goldbach "
            "proof"),
        "support_action_decomposition_measured": True,
        "three_support_action_reduction_proved": False,
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
        "tested_target_count": receipt["tested_target_count"],
        "full_action_positive_count": receipt["full_action_positive_count"],
        "principal_plus_top_three_positive_count": (
            receipt["principal_plus_top_three_positive_count"]),
        "tail_changes_sign_decision_count": (
            receipt["tail_changes_sign_decision_count"]),
        "tail_changed_sign_targets": receipt["tail_changed_sign_targets"],
        "goldbach_proved": receipt["goldbach_proved"],
    }), sort_keys=True))


if __name__ == "__main__":
    main()
