"""Build the K_286 two-mode singular moment target.

The coefficient/norm burden showed that the first two singular directions of
the principal-normalized K_286 coefficient matrix carry about 97.6 percent of
coefficient energy.  This receipt turns that observation into an exact theorem
target: the two leading singular moment functionals plus a separately bounded
residual.

It proves no moment estimate, no K_286 lower bound, and no Goldbach theorem.
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
NORM_BURDEN = EVIDENCE / "q286-wbss-k286-coefficient-norm-burden.json"
OUT = EVIDENCE / "q286-wbss-k286-two-mode-singular-target.json"
PERIOD = 10010
MODULUS = 286
FACTOR_PRIMES = (5, 7, 11, 13)
SUPPORT = (11, 13)
TOLERANCE = 1e-8
MODE_COUNT = 2

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


def support_for_label(label):
    return tuple(
        prime for prime, exponent in zip(FACTOR_PRIMES, label)
        if exponent != 0)


def normalized_k286_matrix(tolerance=TOLERANCE):
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
    units = tuple(sorted(lower_values))
    coefficient_values = np.asarray([
        lower_values[unit] for unit in units
    ], dtype=np.complex128)
    _, labels, character_table = _unit_character_table(MODULUS, units)
    natural_coefficients = (
        np.conjugate(character_table) @ coefficient_values / len(units))
    normalized = natural_coefficients / principal_mean
    matrix = np.zeros((10, 12), dtype=np.complex128)
    for label, value in zip(labels, normalized):
        matrix[label] = value
    return {
        "principal_mean": principal_mean,
        "labels": labels,
        "normalized_coefficients": normalized,
        "active_matrix": matrix[1:, 1:],
    }


def top_vector_entries(vector, offset, count=5):
    rows = []
    for index in np.argsort(-(np.abs(vector) ** 2))[:count]:
        rows.append({
            "character_exponent": int(index + offset),
            "coefficient": complex(vector[index]),
            "energy_fraction": float(abs(vector[index]) ** 2),
        })
    return rows


def top_mode_pair_rows(mode_matrix, count=8):
    rows = []
    for flat_index in np.argsort(-np.abs(mode_matrix).ravel())[:count]:
        row, column = np.unravel_index(flat_index, mode_matrix.shape)
        value = mode_matrix[row, column]
        rows.append({
            "character_label_11_13": (int(row + 1), int(column + 1)),
            "mode_coefficient": complex(value),
            "mode_coefficient_abs": float(abs(value)),
        })
    return rows


def build_receipt():
    norm = load_json(NORM_BURDEN)
    beta = norm["target_bucket"]["allocated_negative_budget_ratio"]
    aggregate_cap = norm["sufficient_burdens"][
        "aggregate_l2_moment_cap"]["required_cap"]
    data = normalized_k286_matrix()
    matrix = data["active_matrix"]
    left, singular_values, right = np.linalg.svd(
        matrix, full_matrices=False)
    reconstruction = left @ np.diag(singular_values) @ right
    reconstruction_error = float(
        np.linalg.norm(reconstruction - matrix)
        / max(1.0, float(np.linalg.norm(matrix))))

    top_values = singular_values[:MODE_COUNT]
    tail_values = singular_values[MODE_COUNT:]
    top_l2 = float(np.sqrt(np.sum(top_values ** 2)))
    tail_l2 = float(np.sqrt(np.sum(tail_values ** 2)))
    total_l2 = float(np.sqrt(np.sum(singular_values ** 2)))
    top_energy_fraction = float(np.sum(top_values ** 2)
                                / np.sum(singular_values ** 2))
    residual_budget_under_global_cap = tail_l2 * aggregate_cap
    two_mode_floor_after_residual_cap = (
        -beta + residual_budget_under_global_cap)

    mode_rows = []
    for index in range(MODE_COUNT):
        normalized_mode = np.outer(left[:, index], right[index, :])
        scaled_mode = singular_values[index] * normalized_mode
        mode_rows.append({
            "mode_index": index + 1,
            "singular_value": float(singular_values[index]),
            "singular_energy_fraction": float(
                singular_values[index] ** 2 / np.sum(singular_values ** 2)),
            "mode_moment_definition": (
                "mu_j(N)=sum_{alpha=1..9,beta=1..11} "
                "u_j(alpha)*vh_j(beta)*delta_{alpha,beta}(N)."),
            "left_vector_top_entries_mod_11": top_vector_entries(
                left[:, index], 1),
            "right_vector_top_entries_mod_13": top_vector_entries(
                right[index, :], 1),
            "top_scaled_character_pair_coefficients": top_mode_pair_rows(
                scaled_mode),
            "normalized_mode_frobenius_norm": float(
                np.linalg.norm(normalized_mode)),
            "scaled_mode_l1": float(np.sum(np.abs(scaled_mode))),
            "scaled_mode_l2": float(np.linalg.norm(scaled_mode)),
            "scaled_mode_linf": float(np.max(np.abs(scaled_mode))),
        })

    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-two-mode-singular-target",
        "source_commit": source_commit(),
        "sources": {
            "k286_coefficient_norm_burden": str(
                NORM_BURDEN.relative_to(ROOT)),
            "k286_coefficient_norm_burden_status": norm["status"],
        },
        "status": "TARGET_k286_two_mode_singular_target_unproved",
        "question": (
            "What exact two singular moment functionals replace generic "
            "K_286 character control?"),
        "answer": (
            "The principal-normalized K_286 coefficient matrix decomposes as "
            "K=sum_j sigma_j u_j vh_j.  The first two singular values are "
            "3.597046733129315 and 2.8233430589589674, carrying "
            "0.9760410444893588 of coefficient energy.  Thus the exact "
            "proof target can be split into two leading moment functionals "
            "mu_1, mu_2 and a residual with coefficient L2 norm "
            "0.7164353938945424."),
        "notation": {
            "character_indices": (
                "alpha=1..9 for nontrivial mod-11 character exponents and "
                "beta=1..11 for nontrivial mod-13 character exponents."),
            "normalized_moment": (
                "delta_{alpha,beta}(N)=D^P_{alpha,beta}(N)/P0_a(N)."),
            "svd_decomposition": (
                "kappa_{alpha,beta}=sum_j sigma_j*u_j(alpha)*vh_j(beta)."),
            "singular_moment": (
                "mu_j(N)=sum_{alpha,beta}u_j(alpha)*vh_j(beta)"
                "*delta_{alpha,beta}(N)."),
            "exact_functional": (
                "Re sum_{alpha,beta} kappa_{alpha,beta} delta_{alpha,beta}"
                "(N) = Re sum_j sigma_j*mu_j(N)."),
        },
        "singular_values": [float(value) for value in singular_values],
        "top_two_summary": {
            "top_two_l2": top_l2,
            "tail_l2": tail_l2,
            "total_l2": total_l2,
            "top_two_energy_fraction": top_energy_fraction,
            "full_reconstruction_relative_error": reconstruction_error,
        },
        "mode_rows": mode_rows,
        "sufficient_two_mode_split": {
            "global_l2_moment_cap": aggregate_cap,
            "tail_adverse_bound_under_global_cap": (
                residual_budget_under_global_cap),
            "two_mode_floor_required_if_tail_has_global_cap": (
                two_mode_floor_after_residual_cap),
            "statement": (
                "If the residual singular moments have L2 norm at most the "
                "global cap 0.038004233097145394, then it is sufficient to "
                "prove Re(sigma_1*mu_1(N)+sigma_2*mu_2(N)) >= "
                f"{two_mode_floor_after_residual_cap} for every sufficiently "
                "large covered even N."),
        },
        "candidate": {
            "name": "K_286 two singular moment target",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Replace broad character control by two explicit separable "
                "singular moment functionals and a small residual coefficient "
                "tail."),
            "prediction": (
                "If the singular compression is proof-relevant, mu_1 and "
                "mu_2 should have a fixed-modulus AP or reflection structure "
                "that is stronger than the full 50-character package."),
            "falsifier": (
                "If mu_1 and mu_2 require the same pointwise binary-prime AP "
                "control as all 50 active characters, the two-mode split is "
                "descriptive only."),
            "smallest_next_test": (
                "Inspect mu_1 and mu_2 as residue weights on U_11 x U_13 and "
                "test whether target reflection or character parity forces a "
                "one-sided sign relation."),
        },
        "decision": (
            "TARGET_k286_two_mode_singular_target_unproved.  The two leading "
            "singular moment functionals are now an exact target: prove a "
            "one-sided lower bound for Re(sigma_1*mu_1+sigma_2*mu_2), plus a "
            "residual cap, instead of paying all active K_286 characters "
            "independently.  This proves no such moment theorem."),
        "status_boundary": (
            "Two-mode singular theorem-target audit only; not a theorem.  No "
            "twisted binary-prime moment estimate, K_286 lower bound, "
            "major/minor arc estimate, pointwise centered-error estimate, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof is established."),
        "goldbach_proved": False,
        "two_mode_pointwise_lower_bound_proved": False,
        "residual_singular_moment_cap_proved": False,
        "twisted_prime_pair_moment_theorem_proved": False,
        "k286_pointwise_lower_bound_proved": False,
        "major_minor_arc_estimate_proved": False,
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
        "top_two_l2": receipt["top_two_summary"]["top_two_l2"],
        "tail_l2": receipt["top_two_summary"]["tail_l2"],
        "top_two_energy_fraction": (
            receipt["top_two_summary"]["top_two_energy_fraction"]),
        "two_mode_floor_required_if_tail_has_global_cap": (
            receipt["sufficient_two_mode_split"][
                "two_mode_floor_required_if_tail_has_global_cap"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
