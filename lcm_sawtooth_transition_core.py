"""Split transition conductors by whether the fixed-common theorem applies.

For ``B<d<=B*V`` and a common conductor part ``c|d``, the condition
``d*c>B*V`` is a uniform sufficient criterion for the fixed-layer base
argument. This probe separates those cells from the cells not covered by that
criterion while retaining their signed interference inside each primitive
coordinate. It then makes the sharper assignment-level split according to
whether both actual conductor bases are retained.
"""

import math

from lcm_sawtooth_exact_gcd_factorization import (
    _squarefree_divisors_with_complement_mobius,
    sawtooth_gcd_mobius_transform,
)
from lcm_sawtooth_structured_divisor_sum import _coefficient_data
from mobius_covariance_endpoint_probe import _prime_flags


def transition_common_core_probe(
        modulus, ell, divisor_lower, divisor_upper):
    """Measure two sufficient-control splits inside ``B<d<=B*V``."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid transition-core ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")

    mobius, divisors, coefficients, _ = _coefficient_data(
        modulus, ell, divisor_lower, divisor_upper)
    threshold = divisor_lower * divisor_upper
    cells = {}
    positive_cells = {}
    assignment_cells = {}
    positive_assignment_cells = {}
    for left in divisors:
        for right in divisors:
            q = math.lcm(left, right)
            pair_term = coefficients[left] * coefficients[right] / q
            positive_pair_term = abs(pair_term)
            pair_common = math.gcd(left, right)
            for divisor, _ in _squarefree_divisors_with_complement_mobius(q):
                if not divisor_upper < divisor <= threshold:
                    continue
                common = math.gcd(divisor, pair_common)
                residual = q // divisor
                controlled = divisor * common > threshold
                key = (divisor, residual, common, controlled)
                cells[key] = cells.get(key, 0.0) + pair_term
                positive_cells[key] = (
                    positive_cells.get(key, 0.0) + positive_pair_term)
                left_base = math.gcd(divisor, left)
                right_base = math.gcd(divisor, right)
                base_supported = (
                    left_base > divisor_lower
                    and right_base > divisor_lower)
                assignment_key = (
                    divisor, residual, left_base, right_base,
                    common, base_supported)
                assignment_cells[assignment_key] = (
                    assignment_cells.get(assignment_key, 0.0) + pair_term)
                positive_assignment_cells[assignment_key] = (
                    positive_assignment_cells.get(assignment_key, 0.0)
                    + positive_pair_term)

    by_divisor = {}
    for (divisor, residual, common, controlled), value in cells.items():
        entry = by_divisor.setdefault(divisor, {
            "controlled": {}, "core": {},
            "controlled_by_common": {}, "core_by_common": {},
            "positive_controlled": {}, "positive_core": {}})
        label = "controlled" if controlled else "core"
        entry[label][residual] = entry[label].get(residual, 0.0) + value
        common_label = f"{label}_by_common"
        common_residuals = entry[common_label].setdefault(common, {})
        common_residuals[residual] = (
            common_residuals.get(residual, 0.0) + value)
        positive_label = (
            "positive_controlled" if controlled else "positive_core")
        positive_key = (residual, common)
        entry[positive_label][positive_key] = (
            entry[positive_label].get(positive_key, 0.0)
            + positive_cells[(divisor, residual, common, controlled)])

    total_energy = controlled_energy = core_energy = cross_energy = 0.0
    controlled_positive_diagonal = core_positive_diagonal = 0.0
    core_separated_energy_by_common = {}
    core_positive_diagonal_by_common = {}
    positive_coordinate_count = 0
    for divisor, entry in by_divisor.items():
        weight = sawtooth_gcd_mobius_transform(modulus, divisor)
        if weight <= 0:
            continue
        positive_coordinate_count += 1
        controlled_sum = sum(entry["controlled"].values())
        core_sum = sum(entry["core"].values())
        total_energy += weight * (controlled_sum + core_sum) ** 2
        controlled_energy += weight * controlled_sum ** 2
        core_energy += weight * core_sum ** 2
        cross_energy += 2 * weight * controlled_sum * core_sum
        controlled_positive_diagonal += weight * sum(
            value ** 2 for value in entry["positive_controlled"].values())
        core_positive_diagonal += weight * sum(
            value ** 2 for value in entry["positive_core"].values())
        for common, residuals in entry["core_by_common"].items():
            core_separated_energy_by_common[common] = (
                core_separated_energy_by_common.get(common, 0.0)
                + weight * sum(residuals.values()) ** 2)
        for (residual, common), value in entry["positive_core"].items():
            core_positive_diagonal_by_common[common] = (
                core_positive_diagonal_by_common.get(common, 0.0)
                + weight * value ** 2)

    if total_energy <= 0:
        raise ArithmeticError("transition range has zero complete energy")
    component_error = (
        total_energy - controlled_energy - core_energy - cross_energy)

    assignment_by_divisor = {}
    double_low_assignment_count = 0
    for key, value in assignment_cells.items():
        (divisor, residual, left_base, right_base,
         common, base_supported) = key
        if (left_base <= divisor_lower
                and right_base <= divisor_lower):
            double_low_assignment_count += 1
        entry = assignment_by_divisor.setdefault(divisor, {
            "supported": {}, "one_sided": {},
            "positive_supported": {}, "positive_one_sided": {}})
        label = "supported" if base_supported else "one_sided"
        entry[label][residual] = entry[label].get(residual, 0.0) + value
        positive_label = f"positive_{label}"
        positive_key = (residual, left_base, right_base, common)
        entry[positive_label][positive_key] = (
            entry[positive_label].get(positive_key, 0.0)
            + positive_assignment_cells[key])

    assignment_total = supported_assignment_energy = 0.0
    one_sided_assignment_energy = assignment_cross_energy = 0.0
    supported_assignment_positive_diagonal = 0.0
    one_sided_assignment_positive_diagonal = 0.0
    for divisor, entry in assignment_by_divisor.items():
        weight = sawtooth_gcd_mobius_transform(modulus, divisor)
        if weight <= 0:
            continue
        supported_sum = sum(entry["supported"].values())
        one_sided_sum = sum(entry["one_sided"].values())
        assignment_total += weight * (supported_sum + one_sided_sum) ** 2
        supported_assignment_energy += weight * supported_sum ** 2
        one_sided_assignment_energy += weight * one_sided_sum ** 2
        assignment_cross_energy += (
            2 * weight * supported_sum * one_sided_sum)
        supported_assignment_positive_diagonal += weight * sum(
            value ** 2 for value in entry["positive_supported"].values())
        one_sided_assignment_positive_diagonal += weight * sum(
            value ** 2 for value in entry["positive_one_sided"].values())

    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "transition_conductor_range": (divisor_upper, threshold),
        "positive_weight_transition_coordinate_count": (
            positive_coordinate_count),
        "transition_complete_energy": total_energy,
        "fixed_common_controlled_energy": controlled_energy,
        "criterion_residual_core_energy": core_energy,
        "controlled_core_cross_energy": cross_energy,
        "component_reconstruction_error": component_error,
        "criterion_residual_core_energy_over_total": core_energy / total_energy,
        "controlled_energy_over_total": controlled_energy / total_energy,
        "cross_energy_over_total": cross_energy / total_energy,
        "controlled_positive_residual_diagonal": (
            controlled_positive_diagonal),
        "core_positive_residual_diagonal": core_positive_diagonal,
        "core_separated_energy_by_common": tuple(sorted(
            (common, value, value / sum(
                core_separated_energy_by_common.values())
             if sum(core_separated_energy_by_common.values()) else 0.0)
            for common, value in core_separated_energy_by_common.items())),
        "core_positive_diagonal_by_common": tuple(sorted(
            (common, value, value / core_positive_diagonal
             if core_positive_diagonal else 0.0)
            for common, value in core_positive_diagonal_by_common.items())),
        "assignment_split_total_energy": assignment_total,
        "base_supported_assignment_energy": supported_assignment_energy,
        "one_sided_assignment_energy": one_sided_assignment_energy,
        "assignment_supported_one_sided_cross_energy": (
            assignment_cross_energy),
        "assignment_split_reconstruction_error": (
            assignment_total - supported_assignment_energy
            - one_sided_assignment_energy - assignment_cross_energy),
        "one_sided_assignment_energy_over_transition_total": (
            one_sided_assignment_energy / total_energy),
        "base_supported_assignment_energy_over_transition_total": (
            supported_assignment_energy / total_energy),
        "base_supported_assignment_positive_diagonal": (
            supported_assignment_positive_diagonal),
        "one_sided_assignment_positive_diagonal": (
            one_sided_assignment_positive_diagonal),
        "double_low_assignment_count": double_low_assignment_count,
        "double_low_assignments_excluded_when_B_gt_V_squared": (
            divisor_upper > divisor_lower ** 2
            and double_low_assignment_count == 0),
        "base_supported_assignments_have_polylog_residual_bound": True,
        "one_sided_assignment_bound_proved": False,
        "transition_fixed_common_split_exact": True,
        "controlled_cells_have_fixed_common_polylog_bound": True,
        "criterion_residual_core_bound_proved": False,
    }


if __name__ == "__main__":
    for controls in (
            (251, 69, 4, 20),
            (503, 113, 4, 29),
            (1009, 183, 5, 42),
            (4001, 477, 8, 89),
            (16001, 1252, 11, 190)):
        print(transition_common_core_probe(*controls))
