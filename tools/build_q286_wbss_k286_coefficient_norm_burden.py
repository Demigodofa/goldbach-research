"""Build the exact K_286 coefficient/norm burden.

The K_286 character-expansion target names a 99-character support space.  This
receipt computes the actual natural-modulus coefficient vector, its active
support, principal-normalized norms, and the sufficient raw moment caps that
would pay the allocated K_286 budget.

It is a coefficient and theorem-target audit only.  It proves no twisted
prime-pair moment estimate, no pointwise K_286 lower bound, and no Goldbach
theorem.
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
K286_TARGET = EVIDENCE / "q286-wbss-k286-character-expansion-target.json"
OUT = EVIDENCE / "q286-wbss-k286-coefficient-norm-burden.json"
PERIOD = 10010
MODULUS = 286
FACTOR_PRIMES = (5, 7, 11, 13)
SUPPORT = (11, 13)
TOLERANCE = 1e-8

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


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


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


def support_for_label(label):
    return tuple(
        prime for prime, exponent in zip(FACTOR_PRIMES, label)
        if exponent != 0)


def coefficient_package(tolerance=TOLERANCE):
    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period_units = tuple(
        residue for residue in range(PERIOD)
        if math.gcd(residue, PERIOD) == 1)
    values = np.asarray([
        coefficient["aggregate_coefficient_by_unit_residue"][unit]
        for unit in period_units
    ], dtype=np.complex128)
    principal_mean = complex(np.mean(values))
    centered = values - principal_mean

    _, period_labels, period_character_table = _unit_character_table(
        PERIOD, period_units)
    period_character_coefficients = (
        np.conjugate(period_character_table) @ centered / len(period_units))
    support_indices = [
        index for index, label in enumerate(period_labels)
        if support_for_label(label) == SUPPORT]
    masked = np.zeros_like(period_character_coefficients)
    masked[support_indices] = period_character_coefficients[support_indices]
    component = period_character_table.T @ masked

    grouped = {}
    for unit, value in zip(period_units, component):
        grouped.setdefault(unit % MODULUS, []).append(value)
    lower_values = {
        residue: sum(items, 0.0j) / len(items)
        for residue, items in grouped.items()}
    descent_error = max(
        abs(value - lower_values[unit % MODULUS])
        for unit, value in zip(period_units, component))
    descent_relative_error = float(
        descent_error / max(1.0, float(np.linalg.norm(component))))

    units = tuple(sorted(lower_values))
    coefficient_values = np.asarray([
        lower_values[unit] for unit in units
    ], dtype=np.complex128)
    _, labels, character_table = _unit_character_table(MODULUS, units)
    natural_coefficients = (
        np.conjugate(character_table) @ coefficient_values / len(units))
    reconstruction = character_table.T @ natural_coefficients
    reconstruction_relative_error = float(
        np.linalg.norm(reconstruction - coefficient_values)
        / max(1.0, float(np.linalg.norm(coefficient_values))))

    available_mask = np.asarray([
        label[0] != 0 and label[1] != 0 for label in labels
    ], dtype=bool)
    active_mask = available_mask & (np.abs(natural_coefficients) > tolerance)
    inactive_available = np.abs(natural_coefficients[
        available_mask & ~active_mask])
    outside_support = np.abs(natural_coefficients[~available_mask])

    normalized = natural_coefficients / principal_mean
    active_normalized = normalized[active_mask]
    active_raw = natural_coefficients[active_mask]
    matrix = np.zeros((10, 12), dtype=np.complex128)
    for label, value in zip(labels, normalized):
        matrix[label] = value
    active_matrix = matrix[1:, 1:]
    singular_values = np.linalg.svd(active_matrix, compute_uv=False)
    singular_energy = singular_values ** 2
    total_singular_energy = float(np.sum(singular_energy))
    cumulative = np.cumsum(singular_energy) / total_singular_energy

    coefficient_by_label = {
        tuple(label): value
        for label, value in zip(labels, normalized)
    }
    conjugate_errors = []
    for label in coefficient_by_label:
        conjugate_label = (
            (-label[0]) % 10,
            (-label[1]) % 12,
        )
        if conjugate_label in coefficient_by_label:
            conjugate_errors.append(abs(
                coefficient_by_label[conjugate_label]
                - np.conjugate(coefficient_by_label[label])))

    ranked = sorted(
        (
            (label, raw, normed)
            for label, raw, normed, active in zip(
                labels, natural_coefficients, normalized, active_mask)
            if active
        ),
        key=lambda item: abs(item[2]),
        reverse=True)
    top_rows = []
    for label, raw, normed in ranked[:12]:
        top_rows.append({
            "label_11_13": label,
            "raw_coefficient": complex(raw),
            "principal_normalized_coefficient": complex(normed),
            "normalized_abs": float(abs(normed)),
        })

    raw_l1 = float(np.sum(np.abs(active_raw)))
    raw_l2 = float(np.sqrt(np.sum(np.abs(active_raw) ** 2)))
    raw_linf = float(np.max(np.abs(active_raw)))
    normalized_l1 = float(np.sum(np.abs(active_normalized)))
    normalized_l2 = float(np.sqrt(np.sum(np.abs(active_normalized) ** 2)))
    normalized_linf = float(np.max(np.abs(active_normalized)))

    return {
        "principal_mean": principal_mean,
        "period_unit_count": len(period_units),
        "natural_unit_count": len(units),
        "available_character_count": int(np.sum(available_mask)),
        "active_nonzero_character_count": int(np.sum(active_mask)),
        "zero_available_character_count": int(
            np.sum(available_mask) - np.sum(active_mask)),
        "max_abs_zero_available_coefficient": (
            float(np.max(inactive_available))
            if len(inactive_available) else 0.0),
        "max_abs_outside_11x13_coefficient": (
            float(np.max(outside_support)) if len(outside_support) else 0.0),
        "descent_relative_error": descent_relative_error,
        "reconstruction_relative_error": reconstruction_relative_error,
        "raw_norms": {
            "l1": raw_l1,
            "l2": raw_l2,
            "linf": raw_linf,
        },
        "principal_normalized_norms": {
            "l1": normalized_l1,
            "l2": normalized_l2,
            "linf": normalized_linf,
        },
        "singular_structure": {
            "matrix_shape": active_matrix.shape,
            "numerical_rank": int(np.sum(singular_values > tolerance)),
            "effective_singular_rank": float(
                total_singular_energy * total_singular_energy
                / float(np.sum(singular_energy ** 2))),
            "singular_values": [float(value) for value in singular_values],
            "singular_energy_fractions": [
                float(value / total_singular_energy)
                for value in singular_energy
            ],
            "cumulative_singular_energy_fractions": [
                float(value) for value in cumulative
            ],
            "top_two_singular_energy_fraction": float(cumulative[1]),
        },
        "conjugate_symmetry": {
            "max_principal_normalized_conjugate_error": (
                max(conjugate_errors) if conjugate_errors else 0.0),
            "error_summary": finite_summary(conjugate_errors),
        },
        "top_principal_normalized_coefficients": top_rows,
    }


def build_receipt():
    target = load_json(K286_TARGET)
    beta = target["target_bucket"]["allocated_negative_budget_ratio"]
    package = coefficient_package()
    norms = package["principal_normalized_norms"]

    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-coefficient-norm-burden",
        "source_commit": source_commit(),
        "sources": {
            "k286_character_expansion_target": str(
                K286_TARGET.relative_to(ROOT)),
            "k286_character_expansion_status": target["status"],
        },
        "status": "TARGET_k286_coefficient_norm_burden_unproved",
        "question": (
            "What exact coefficient norms must a raw analytic theorem pay "
            "for the dominant K_286 bucket?"),
        "answer": (
            "The nominal 11x13 character support has 99 available characters, "
            "but the natural-modulus coefficient vector has 50 nonzero entries "
            "above tolerance.  In principal-normalized coordinates its L1 norm "
            "is 32.42815568567079 and its L2 norm is 4.628530101718351.  A "
            "uniform absolute moment cap would need |delta_chi| <= "
            "0.00542441385158965, while an aggregate L2 moment theorem would "
            "need ||delta||_2 <= 0.038004233097145394.  The top two singular "
            "directions carry 0.9760410444893588 of coefficient energy, so a "
            "two-mode structured theorem is now a sharper target than "
            "treating 99 characters independently."),
        "target_bucket": target["target_bucket"],
        "coefficient_package": package,
        "normalized_moment_notation": {
            "coefficient": (
                "kappa_chi = c_{a,chi}^{286}/principal_mean."),
            "moment": (
                "delta_chi(N)=D_chi^P(N)/P0_a(N), using the proof-scale "
                "raw moment from the K_286 target."),
            "target": (
                "Re sum_chi kappa_chi*delta_chi(N) >= "
                f"-{beta}."),
        },
        "sufficient_burdens": {
            "direct_signed_sum": (
                "Prove Re sum_chi kappa_chi*delta_chi(N) >= "
                f"-{beta} pointwise for every sufficiently large covered N."),
            "uniform_linf_moment_cap": {
                "statement": (
                    "It is sufficient, but likely much stronger than "
                    "necessary, to prove max_chi |delta_chi(N)| <= beta/"
                    "||kappa||_1."),
                "required_cap": beta / norms["l1"],
                "coefficient_norm_used": norms["l1"],
            },
            "aggregate_l2_moment_cap": {
                "statement": (
                    "It is sufficient to prove sqrt(sum_chi |delta_chi(N)|^2) "
                    "<= beta/||kappa||_2."),
                "required_cap": beta / norms["l2"],
                "coefficient_norm_used": norms["l2"],
            },
            "dominant_two_singular_mode_target": {
                "statement": (
                    "A sharper possible theorem separates the first two "
                    "singular directions from the residual seven directions "
                    "instead of paying all active characters independently."),
                "top_two_singular_energy_fraction": (
                    package["singular_structure"][
                        "top_two_singular_energy_fraction"]),
                "residual_singular_energy_fraction": (
                    1.0 - package["singular_structure"][
                        "top_two_singular_energy_fraction"]),
            },
        },
        "candidate": {
            "name": "K_286 two-mode coefficient burden",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use the exact coefficient matrix at natural modulus 286 to "
                "replace a 99-character theorem target with 50 active "
                "coefficients and a dominant two-singular-direction payment."),
            "prediction": (
                "A viable analytic theorem should exploit the two dominant "
                "singular modes; treating all characters by triangle "
                "inequality demands a very small 0.0054244 uniform moment cap."),
            "falsifier": (
                "If the first two singular moment combinations cannot be "
                "controlled better than the whole 50-character package, this "
                "compression is only descriptive and does not help the proof."),
            "smallest_next_test": (
                "Write the two leading singular left/right vectors as explicit "
                "linear combinations of characters, then ask whether their "
                "twisted binary-prime moments have a special parity, "
                "divisibility, or reflection form."),
        },
        "decision": (
            "TARGET_k286_coefficient_norm_burden_unproved.  The dominant "
            "K_286 bucket is no longer just a 99-character nominal target: it "
            "has 50 active natural-modulus coefficients, principal-normalized "
            "L1 norm 32.42815568567079, L2 norm 4.628530101718351, and a "
            "top-two singular energy fraction 0.9760410444893588.  This gives "
            "precise sufficient raw moment caps, but proves no such pointwise "
            "moment theorem."),
        "status_boundary": (
            "Coefficient/norm theorem-target audit only; not a theorem.  No "
            "twisted binary-prime moment estimate, K_286 lower bound, "
            "major/minor arc estimate, pointwise centered-error estimate, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof is established."),
        "goldbach_proved": False,
        "k286_pointwise_lower_bound_proved": False,
        "twisted_prime_pair_moment_theorem_proved": False,
        "major_minor_arc_estimate_proved": False,
        "pointwise_centered_error_estimate_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "universal_pointwise_bound_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(json_ready(build_receipt()), indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "available_character_count": (
            receipt["coefficient_package"]["available_character_count"]),
        "active_nonzero_character_count": (
            receipt["coefficient_package"][
                "active_nonzero_character_count"]),
        "normalized_l1": (
            receipt["coefficient_package"][
                "principal_normalized_norms"]["l1"]),
        "normalized_l2": (
            receipt["coefficient_package"][
                "principal_normalized_norms"]["l2"]),
        "top_two_singular_energy_fraction": (
            receipt["coefficient_package"]["singular_structure"][
                "top_two_singular_energy_fraction"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
