"""Decompose the fixed-Mobius row ratio and measure its weighted variance.

For the squarefree divisor interval ``D=(V,B]``, put

    w(n)=sum_(a in D, a|n) mu(a) log(n/a)

on the strict row ``X<n<X+m``, ``X=m*ell``.  The exact fixed-vector full
collision Gram divided by its diagonal totient frame is

    R = m[sum_n w(n)^2-(sum_n w(n))^2/(m-1)]
        / [m^2 sum_(a in D) phi(a)log(X/a)^2/a^2].       (1)

This module splits ``R`` into the frozen ideal ratio, the exact CRT collision
count error from ``mobius_lcm_coefficient_collapse.py``, and a residual that
contains log variation and centering differences.  It then measures all four
under the exact active-lag vertex weight

    alpha_(m,ell)=rho_m*m*log(m)^2*F_(m,ell).            (2)

The finite moments are falsifiers for a possible variance-to-lag proof.  They
are not asymptotic estimates, and the graph degree factor remains separate.
"""

import math

from divisor_full_frame_probe import _totient
from mobius_covariance_lag_probe import _mobius_values
from mobius_lcm_coefficient_collapse import mobius_lcm_signed_count_probe
from near_cutoff_geometric_bound import _active_modes
from weighted_lag_graph_lemma import weighted_geometric_variance_bound


def mobius_row_ratio_components(
        modulus, ell, shift_length, divisor_lower, divisor_upper):
    """Return the exact, ideal, frozen-collision, and residual row ratios."""
    if type(shift_length) is not int or shift_length < 2:
        raise ValueError("shift_length must be an integer at least two")
    base = mobius_lcm_signed_count_probe(
        modulus, ell, divisor_lower, divisor_upper)
    active_count = len(_active_modes(modulus, shift_length))
    if not active_count:
        raise ValueError("the modulus must have a nonempty active band")
    X = modulus * ell
    mobius = _mobius_values(divisor_upper)
    divisors = tuple(
        value for value in range(divisor_lower + 1, divisor_upper + 1)
        if mobius[value])
    logarithms = {value: math.log(X / value) for value in divisors}
    frame_base = base["totient_frame_base"]

    row_values = [0.0] * (modulus - 1)
    for divisor in divisors:
        first = X // divisor + 1
        last = (X + modulus - 1) // divisor
        for cofactor in range(first, last + 1):
            position = divisor * cofactor - X - 1
            row_values[position] += mobius[divisor] * math.log(cofactor)
    collision = sum(value ** 2 for value in row_values)
    row_sum = sum(row_values)
    exact_ratio = (collision - row_sum ** 2 / (modulus - 1))
    exact_ratio /= modulus * frame_base

    ideal_ratio = sum(
        mobius[left] * mobius[right]
        * logarithms[left] * logarithms[right]
        * (math.gcd(left, right) - 1) / (left * right)
        for left in divisors for right in divisors)
    ideal_ratio /= frame_base
    collision_ratio = base["frozen_count_error_over_totient_frame"]
    residual_ratio = exact_ratio - ideal_ratio - collision_ratio
    rho = active_count / (modulus - 1)
    vertex_weight = (rho * modulus * math.log(modulus) ** 2 * frame_base)
    frame_energy = modulus ** 2 * frame_base
    outer_weight = rho * math.log(modulus) ** 2 / modulus
    return {
        "modulus": modulus,
        "ell": ell,
        "shift_length": shift_length,
        "divisor_range": (divisor_lower, divisor_upper),
        "vertex_weight": vertex_weight,
        "frame_energy": frame_energy,
        "outer_weight": outer_weight,
        "exact_row_ratio": exact_ratio,
        "ideal_row_ratio": ideal_ratio,
        "frozen_collision_ratio": collision_ratio,
        "log_centering_residual_ratio": residual_ratio,
        "component_identity_error": (
            exact_ratio - ideal_ratio - collision_ratio - residual_ratio),
        "row_ratio_asymptotic_estimate_proved": False,
    }


def mobius_row_ratio_variance_probe(
        moduli, shift_length, ell_first, row_count,
        divisor_lower, divisor_upper):
    """Return frame-weighted moments of (1) and its three components."""
    if (not isinstance(moduli, (tuple, list)) or not moduli
            or any(type(value) is not int for value in moduli)
            or len(set(moduli)) != len(moduli)):
        raise ValueError("moduli must be distinct integers in a nonempty list")
    if (type(ell_first) is not int or type(row_count) is not int
            or ell_first < 1 or row_count < 1):
        raise ValueError("invalid row range")
    cells = tuple(
        mobius_row_ratio_components(
            modulus, ell, shift_length, divisor_lower, divisor_upper)
        for modulus in moduli
        for ell in range(ell_first, ell_first + row_count))
    total_weight = sum(cell["vertex_weight"] for cell in cells)
    if total_weight <= 0:
        raise ArithmeticError("row-ratio vertex weight must be positive")

    def moments(key):
        mean = sum(cell["vertex_weight"] * cell[key]
                   for cell in cells) / total_weight
        mean_square = sum(cell["vertex_weight"] * cell[key] ** 2
                          for cell in cells) / total_weight
        variance = max(0.0, mean_square - mean ** 2)
        return mean, mean_square, variance

    output = {
        "moduli": tuple(moduli),
        "shift_length": shift_length,
        "ell_range": (ell_first, ell_first + row_count - 1),
        "divisor_range": (divisor_lower, divisor_upper),
        "cell_count": len(cells),
    }
    for label, key in (
            ("exact", "exact_row_ratio"),
            ("ideal", "ideal_row_ratio"),
            ("collision", "frozen_collision_ratio"),
            ("residual", "log_centering_residual_ratio")):
        mean, mean_square, variance = moments(key)
        output[f"frame_weighted_{label}_mean"] = mean
        output[f"frame_weighted_{label}_mean_square"] = mean_square
        output[f"frame_weighted_{label}_variance"] = variance
        output[f"frame_weighted_{label}_standard_deviation"] = math.sqrt(
            variance)
    output["mobius_row_ratio_variance_bound_proved"] = False
    return output


def mobius_row_ratio_lag_graph_probe(
        moduli, shift_length, ell_first, row_count,
        divisor_lower, divisor_upper, lag_first, lag_stop):
    """Apply the proved variance lemma to exact fixed-Mobius finite rows."""
    if (not isinstance(moduli, (tuple, list)) or not moduli
            or any(type(value) is not int for value in moduli)
            or len(set(moduli)) != len(moduli)):
        raise ValueError("moduli must be distinct integers in a nonempty list")
    if (type(ell_first) is not int or type(row_count) is not int
            or ell_first < 1 or row_count < 2):
        raise ValueError("invalid row range")
    if (type(lag_first) is not int or type(lag_stop) is not int
            or not 1 <= lag_first < lag_stop <= row_count):
        raise ValueError("lag range must satisfy 1<=first<stop<=row_count")
    cells = []
    indices = {}
    for modulus in moduli:
        for ell in range(ell_first, ell_first + row_count):
            cell = mobius_row_ratio_components(
                modulus, ell, shift_length, divisor_lower, divisor_upper)
            indices[(modulus, ell)] = len(cells)
            cells.append(cell)
    edges = []
    for modulus in moduli:
        outer_weight = cells[indices[(modulus, ell_first)]]["outer_weight"]
        for delta in range(lag_first, lag_stop):
            for ell in range(
                    ell_first, ell_first + row_count - delta):
                left = cells[indices[(modulus, ell)]]
                right = cells[indices[(modulus, ell + delta)]]
                edges.append((
                    indices[(modulus, ell)],
                    indices[(modulus, ell + delta)],
                    outer_weight * math.sqrt(
                        left["frame_energy"] * right["frame_energy"]),
                ))
    graph = weighted_geometric_variance_bound(
        (cell["exact_row_ratio"] for cell in cells),
        (cell["vertex_weight"] for cell in cells), edges)
    return {
        "moduli": tuple(moduli),
        "shift_length": shift_length,
        "ell_range": (ell_first, ell_first + row_count - 1),
        "divisor_range": (divisor_lower, divisor_upper),
        "lag_range": (lag_first, lag_stop - 1),
        "cell_count": len(cells),
        "edge_count": len(edges),
        **graph,
        "finite_fixed_mobius_lag_certificate": graph[
            "variance_lower_bound"],
        "asymptotic_fixed_mobius_lag_frame_proved": False,
    }
