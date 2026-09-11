"""Generalized operator test for exact common-part assignment layers.

For every common part ``c=d_C`` factor its sign from the pair coefficient and
write the dominant high-conductor residual data as

    y_(d,r) = sum_(c|d) mu(c) A_c(d,r).

The collapsed and residual-diagonal Gram matrices of the layer vectors are
positive semidefinite.  Their largest generalized eigenvalue is the worst
residual quotient available to an arbitrary combination of the same measured
layers.  Comparing it with the actual coefficient direction ``mu(c)`` tests
whether Mobius alternation avoids layer resonance.
"""

import math
import statistics

import numpy as np

from lcm_sawtooth_exact_gcd_factorization import (
    _squarefree_divisors_with_complement_mobius,
    sawtooth_gcd_mobius_transform,
)
from lcm_sawtooth_structured_divisor_sum import _coefficient_data
from mobius_covariance_endpoint_probe import _prime_flags


def common_layer_operator_probe(
        modulus, ell, divisor_lower, divisor_upper):
    """Compare the actual common-layer direction with its worst resonance."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid common-layer ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")
    mobius, divisors, coefficients, lcm_coefficients = _coefficient_data(
        modulus, ell, divisor_lower, divisor_upper)
    if not divisors:
        raise ValueError("the divisor interval has no squarefree values")

    q_divisors = {
        q: tuple(divisor for divisor, _
                 in _squarefree_divisors_with_complement_mobius(q))
        for q in lcm_coefficients}
    layers = {}
    for left in divisors:
        for right in divisors:
            q = math.lcm(left, right)
            pair_term = coefficients[left] * coefficients[right] / q
            common_pair_part = math.gcd(left, right)
            for divisor in q_divisors[q]:
                common_part = math.gcd(divisor, common_pair_part)
                sign_aligned_term = pair_term * int(mobius[common_part])
                layers.setdefault(divisor, {}).setdefault(q, {})[
                    common_part] = (
                        layers.setdefault(divisor, {}).setdefault(q, {}).get(
                            common_part, 0.0) + sign_aligned_term)

    diagonal_by_block = {}
    for divisor, q_layers in layers.items():
        if divisor <= divisor_upper or len(q_layers) < 2:
            continue
        weight = sawtooth_gcd_mobius_transform(modulus, divisor)
        if weight <= 0:
            continue
        diagonal = 0.0
        for common_layers in q_layers.values():
            actual_term = sum(
                int(mobius[common]) * value
                for common, value in common_layers.items())
            diagonal += weight * actual_term ** 2
        block = 1 << (divisor.bit_length() - 1)
        diagonal_by_block[block] = diagonal_by_block.get(block, 0.0) + diagonal
    if not diagonal_by_block:
        raise ArithmeticError("no positive dominant common-layer block")
    dominant_lower = max(diagonal_by_block, key=diagonal_by_block.get)

    active_common_parts = sorted({
        common
        for divisor, q_layers in layers.items()
        if (divisor > divisor_upper
            and dominant_lower <= divisor < 2 * dominant_lower
            and len(q_layers) >= 2
            and sawtooth_gcd_mobius_transform(modulus, divisor) > 0)
        for common_layers in q_layers.values()
        for common in common_layers})
    index = {common: position
             for position, common in enumerate(active_common_parts)}
    size = len(active_common_parts)
    collapsed_gram = np.zeros((size, size), dtype=float)
    diagonal_gram = np.zeros((size, size), dtype=float)
    absolute_collapsed_gram = np.zeros((size, size), dtype=float)
    absolute_diagonal_gram = np.zeros((size, size), dtype=float)
    coordinate_count = 0
    for divisor, q_layers in layers.items():
        if (divisor <= divisor_upper
                or not dominant_lower <= divisor < 2 * dominant_lower
                or len(q_layers) < 2):
            continue
        weight = sawtooth_gcd_mobius_transform(modulus, divisor)
        if weight <= 0:
            continue
        coordinate_count += 1
        collapsed_vector = np.zeros(size, dtype=float)
        absolute_collapsed_vector = np.zeros(size, dtype=float)
        for common_layers in q_layers.values():
            residual_vector = np.zeros(size, dtype=float)
            for common, value in common_layers.items():
                residual_vector[index[common]] = value
            collapsed_vector += residual_vector
            diagonal_gram += weight * np.outer(
                residual_vector, residual_vector)
            absolute_residual_vector = np.abs(residual_vector)
            absolute_collapsed_vector += absolute_residual_vector
            absolute_diagonal_gram += weight * np.outer(
                absolute_residual_vector, absolute_residual_vector)
        collapsed_gram += weight * np.outer(
            collapsed_vector, collapsed_vector)
        absolute_collapsed_gram += weight * np.outer(
            absolute_collapsed_vector, absolute_collapsed_vector)

    diagonal_eigenvalues, diagonal_eigenvectors = np.linalg.eigh(
        diagonal_gram)
    largest_diagonal_eigenvalue = float(diagonal_eigenvalues[-1])
    tolerance = max(1e-12, largest_diagonal_eigenvalue * 1e-10)
    retained = diagonal_eigenvalues > tolerance
    if not np.any(retained):
        raise ArithmeticError("common-layer diagonal Gram has zero rank")
    basis = diagonal_eigenvectors[:, retained]
    eigenvalues = diagonal_eigenvalues[retained]
    inverse_root = basis @ np.diag(eigenvalues ** -.5)
    normalized = inverse_root.T @ collapsed_gram @ inverse_root
    normalized_eigenvalues, normalized_eigenvectors = np.linalg.eigh(
        normalized)
    largest_generalized_eigenvalue = float(normalized_eigenvalues[-1])
    extremizer = normalized_eigenvectors[:, -1]

    absolute_diagonal_eigenvalues, absolute_diagonal_eigenvectors = (
        np.linalg.eigh(absolute_diagonal_gram))
    largest_absolute_diagonal_eigenvalue = float(
        absolute_diagonal_eigenvalues[-1])
    absolute_tolerance = max(
        1e-12, largest_absolute_diagonal_eigenvalue * 1e-10)
    absolute_retained = absolute_diagonal_eigenvalues > absolute_tolerance
    if not np.any(absolute_retained):
        raise ArithmeticError("absolute common-layer diagonal has zero rank")
    absolute_basis = absolute_diagonal_eigenvectors[:, absolute_retained]
    absolute_eigenvalues = absolute_diagonal_eigenvalues[absolute_retained]
    absolute_inverse_root = (
        absolute_basis @ np.diag(absolute_eigenvalues ** -.5))
    absolute_normalized = (
        absolute_inverse_root.T @ absolute_collapsed_gram
        @ absolute_inverse_root)
    largest_absolute_generalized_eigenvalue = float(
        np.linalg.eigvalsh(absolute_normalized)[-1])

    layer_diagonal = np.diag(diagonal_gram)
    if np.any(layer_diagonal <= 0):
        raise ArithmeticError("an active common layer has zero diagonal")
    layer_scale = layer_diagonal ** -.5
    layer_scaling = np.outer(layer_scale, layer_scale)
    layer_normalized_collapsed = collapsed_gram * layer_scaling
    layer_normalized_diagonal = diagonal_gram * layer_scaling
    layer_schur_row_sum = float(np.max(
        np.sum(np.abs(layer_normalized_collapsed), axis=1)))
    layer_diagonal_coercivity = float(
        np.linalg.eigvalsh(layer_normalized_diagonal)[0])
    layer_schur_over_coercivity = (
        layer_schur_row_sum / layer_diagonal_coercivity
        if layer_diagonal_coercivity > 0 else float("inf"))
    individual_layers = tuple({
        "common_part": common,
        "signed_residual_quotient": float(
            collapsed_gram[position, position]
            / diagonal_gram[position, position]),
        "absolute_residual_quotient": float(
            absolute_collapsed_gram[position, position]
            / absolute_diagonal_gram[position, position]),
        "separated_diagonal_fraction": float(
            diagonal_gram[position, position] / np.trace(diagonal_gram)),
    } for position, common in enumerate(active_common_parts))
    residual_budget_upper_bound = divisor_upper ** 2 / dominant_lower
    singleton_common_threshold = residual_budget_upper_bound / 2
    interactive_common_parts = tuple(
        common for common in active_common_parts
        if common <= singleton_common_threshold)
    singleton_common_parts = tuple(
        common for common in active_common_parts
        if common > singleton_common_threshold)
    individual_by_common = {
        layer["common_part"]: layer for layer in individual_layers}
    singleton_tail_verified = all(
        abs(individual_by_common[common]["signed_residual_quotient"] - 1)
        < 1e-9
        and abs(individual_by_common[common][
            "absolute_residual_quotient"] - 1) < 1e-9
        for common in singleton_common_parts)
    no_common_layer = individual_by_common[1]

    actual_coefficients = np.array(
        [int(mobius[common]) for common in active_common_parts], dtype=float)
    actual_numerator = float(
        actual_coefficients @ collapsed_gram @ actual_coefficients)
    actual_diagonal = float(
        actual_coefficients @ diagonal_gram @ actual_coefficients)
    actual_ratio = actual_numerator / actual_diagonal
    whitened_actual = (
        np.diag(eigenvalues ** .5) @ basis.T @ actual_coefficients)
    whitened_norm_square = float(whitened_actual @ whitened_actual)
    squared_overlap = float(
        (whitened_actual @ extremizer) ** 2 / whitened_norm_square)
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "dominant_block_range": (dominant_lower, 2 * dominant_lower),
        "coordinate_count": coordinate_count,
        "active_common_part_count": size,
        "diagonal_gram_rank": int(np.count_nonzero(retained)),
        "diagonal_gram_condition_on_retained_space": float(
            eigenvalues[-1] / eigenvalues[0]),
        "largest_common_layer_generalized_eigenvalue": (
            largest_generalized_eigenvalue),
        "largest_absolute_layer_generalized_eigenvalue": (
            largest_absolute_generalized_eigenvalue),
        "absolute_over_signed_generalized_eigenvalue": (
            largest_absolute_generalized_eigenvalue
            / largest_generalized_eigenvalue),
        "layer_diagonal_normalized_schur_row_sum": layer_schur_row_sum,
        "layer_diagonal_gram_coercivity": layer_diagonal_coercivity,
        "layer_schur_over_coercivity_bound": (
            layer_schur_over_coercivity),
        "individual_layers": individual_layers,
        "dominant_residual_budget_upper_bound": residual_budget_upper_bound,
        "singleton_common_part_strict_threshold": (
            singleton_common_threshold),
        "interactive_common_parts": interactive_common_parts,
        "singleton_common_parts": singleton_common_parts,
        "singleton_common_tail_verified": singleton_tail_verified,
        "no_common_layer_signed_quotient": no_common_layer[
            "signed_residual_quotient"],
        "no_common_layer_absolute_quotient": no_common_layer[
            "absolute_residual_quotient"],
        "no_common_layer_separated_diagonal_fraction": no_common_layer[
            "separated_diagonal_fraction"],
        "actual_mobius_common_layer_quotient": actual_ratio,
        "actual_extremizer_squared_overlap": squared_overlap,
        "common_layer_generalized_operator_computed": True,
        "large_common_part_singleton_tail_proved": True,
        "common_layer_subpower_bound_proved": False,
    }


def project_common_layer_operator_probe(
        scale_modulus, prime_sample_count=8):
    """Sample the common-layer generalized operator at project exponents."""
    if (type(scale_modulus) is not int or type(prime_sample_count) is not int
            or scale_modulus < 17 or prime_sample_count < 2):
        raise ValueError("invalid project-scale controls")
    inferred_N = scale_modulus ** (1 / .59)
    ell = int(1.5 * inferred_N ** .41)
    divisor_lower = int(inferred_N ** .15)
    divisor_upper = int(inferred_N ** .32)
    flags = _prime_flags(2 * scale_modulus)
    available = tuple(
        value for value in range(scale_modulus, 2 * scale_modulus + 1)
        if flags[value])
    if len(available) < prime_sample_count:
        raise ValueError("not enough primes in the scale interval")
    indices = tuple(round(
        index * (len(available) - 1) / (prime_sample_count - 1))
        for index in range(prime_sample_count))
    moduli = tuple(available[index] for index in indices)
    cells = tuple(common_layer_operator_probe(
        modulus, ell, divisor_lower, divisor_upper) for modulus in moduli)

    def summary(key):
        values = tuple(float(cell[key]) for cell in cells)
        return (min(values), statistics.median(values), max(values))

    return {
        "scale_modulus": scale_modulus,
        "sampled_moduli": moduli,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "largest_eigenvalue_min_median_max": summary(
            "largest_common_layer_generalized_eigenvalue"),
        "absolute_eigenvalue_min_median_max": summary(
            "largest_absolute_layer_generalized_eigenvalue"),
        "absolute_over_signed_eigenvalue_min_median_max": summary(
            "absolute_over_signed_generalized_eigenvalue"),
        "layer_schur_row_sum_min_median_max": summary(
            "layer_diagonal_normalized_schur_row_sum"),
        "layer_diagonal_coercivity_min_median_max": summary(
            "layer_diagonal_gram_coercivity"),
        "layer_schur_over_coercivity_min_median_max": summary(
            "layer_schur_over_coercivity_bound"),
        "interactive_common_part_count_min_median_max": (
            min(len(cell["interactive_common_parts"]) for cell in cells),
            statistics.median(
                len(cell["interactive_common_parts"]) for cell in cells),
            max(len(cell["interactive_common_parts"]) for cell in cells)),
        "no_common_signed_quotient_min_median_max": summary(
            "no_common_layer_signed_quotient"),
        "no_common_absolute_quotient_min_median_max": summary(
            "no_common_layer_absolute_quotient"),
        "no_common_diagonal_fraction_min_median_max": summary(
            "no_common_layer_separated_diagonal_fraction"),
        "all_singleton_common_tails_verified": all(
            cell["singleton_common_tail_verified"] for cell in cells),
        "actual_quotient_min_median_max": summary(
            "actual_mobius_common_layer_quotient"),
        "squared_overlap_min_median_max": summary(
            "actual_extremizer_squared_overlap"),
        "active_common_part_count_min_median_max": summary(
            "active_common_part_count"),
        "retained_condition_min_median_max": summary(
            "diagonal_gram_condition_on_retained_space"),
        "finite_project_common_layer_operator_measurement": True,
        "large_common_part_singleton_tail_proved": True,
        "common_layer_subpower_bound_proved": False,
    }


if __name__ == "__main__":
    for scale in (
            251, 503, 1009, 2003, 4001, 8009, 16001, 32003, 64007):
        print(project_common_layer_operator_probe(scale))
