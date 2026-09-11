"""Expose the exact primitive rational frequencies of an incomplete row.

For frozen lcm coefficients ``K_q`` and the centered count discrepancy
``d_(m,q)(ell)``, finite Fourier inversion gives

    sum_q K_q d_(m,q)(ell)
      = sum_(d>1) S_d sum_((k,d)=1) G_(m,d,k)e(k*m*ell/d),       (1)

where

    S_d=sum_(d|q)K_q/q,
    G_(m,d,k)=sum_(1<=t<m)e(k*t/d).                             (2)

The fractions ``k/d`` in (1) are reduced, so they are distinct.  Averaging
over a common complete period kills every cross-frequency term, while

    sum_((k,d)=1)|G_(m,d,k)|^2=H_m(d).

Thus the diagonal frequency energy is exactly the previously proved
primitive-conductor factorization.  On an incomplete interval, the only new
terms are Dirichlet-kernel interactions between distinct reduced fractions.
This module measures which of those interactions are near resonances; it does
not assert an asymptotic boundary estimate.
"""

import cmath
import math

import numpy as np

from lcm_sawtooth_exact_gcd_factorization import (
    _squarefree_divisors_with_complement_mobius,
    sawtooth_gcd_mobius_transform,
)
from lcm_sawtooth_incomplete_covariance import _cyclic_discrepancy
from lcm_sawtooth_incomplete_covariance import _lcm_coefficient_polynomials
from lcm_sawtooth_structured_divisor_sum import _coefficient_data
from mobius_covariance_endpoint_probe import _prime_flags


def _geometric_numerator(modulus, denominator, numerator):
    """Return ``G_(m,d,k)`` from (2)."""
    angle = 2 * math.pi * numerator / denominator
    root = cmath.exp(1j * angle)
    return root * (1 - root ** (modulus - 1)) / (1 - root)


def _interval_kernel(frequency, row_first, row_count):
    """Return the normalized exponential mean on the requested row interval."""
    return sum(
        cmath.exp(2j * math.pi * frequency * ell)
        for ell in range(row_first, row_first + row_count)
    ) / row_count


def _primitive_discrepancy_packet(modulus, ell, denominator):
    """Return the reduced-denominator packet by divisor Mobius inversion."""
    return sum(
        sign * divisor * _cyclic_discrepancy(modulus, ell, divisor)
        for divisor, sign in _squarefree_divisors_with_complement_mobius(
            denominator)
        if divisor > 1)


def _quadratic_curve_maximum(numerator, denominator, lower, upper):
    """Maximize ``v(t)^T N v(t)/v(t)^T D v(t)`` for v=(t^2,t,1)."""
    order = (2, 1, 0)
    numerator_ascending = np.zeros(5)
    denominator_ascending = np.zeros(5)
    for left in range(3):
        for right in range(3):
            degree = order[left] + order[right]
            numerator_ascending[degree] += numerator[left, right]
            denominator_ascending[degree] += denominator[left, right]
    derivative_numerator = np.polynomial.polynomial.polysub(
        np.polynomial.polynomial.polymul(
            np.polynomial.polynomial.polyder(numerator_ascending),
            denominator_ascending),
        np.polynomial.polynomial.polymul(
            numerator_ascending,
            np.polynomial.polynomial.polyder(denominator_ascending)))
    candidates = [lower, upper]
    for root in np.polynomial.polynomial.polyroots(derivative_numerator):
        if abs(root.imag) <= 1e-8 and lower <= root.real <= upper:
            candidates.append(float(root.real))

    def quotient(value):
        return (np.polynomial.polynomial.polyval(
            value, numerator_ascending)
                / np.polynomial.polynomial.polyval(
                    value, denominator_ascending))

    maximizing = max(candidates, key=quotient)
    return float(quotient(maximizing)), float(maximizing)


def primitive_frequency_receipt(
        modulus, ell_first, row_count, ell_freeze,
        divisor_lower, divisor_upper, decompose_pairs=True):
    """Verify (1) and split its incomplete boundary by Farey distance."""
    if any(type(value) is not int for value in (
            modulus, ell_first, row_count, ell_freeze,
            divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell_first < 1 or row_count < 1 or ell_freeze < 1
            or divisor_lower < 1 or divisor_upper <= divisor_lower
            or divisor_upper >= modulus):
        raise ValueError("invalid primitive-frequency ranges")
    if type(decompose_pairs) is not bool:
        raise ValueError("decompose_pairs must be Boolean")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")

    mobius, divisors, _, lcm_coefficients = _coefficient_data(
        modulus, ell_freeze, divisor_lower, divisor_upper)
    if not divisors:
        raise ValueError("the divisor interval has no squarefree values")

    structured_sums = {}
    for q, coefficient in lcm_coefficients.items():
        for divisor, _ in _squarefree_divisors_with_complement_mobius(q):
            if divisor > 1:
                structured_sums[divisor] = (
                    structured_sums.get(divisor, 0.0) + coefficient / q)

    frequencies = []
    primitive_parseval_error = 0.0
    for denominator, structured_sum in sorted(structured_sums.items()):
        local_square_mass = 0.0
        for numerator in range(1, denominator):
            if math.gcd(numerator, denominator) != 1:
                continue
            geometric = _geometric_numerator(
                modulus, denominator, numerator)
            local_square_mass += abs(geometric) ** 2
            frequency = ((modulus * numerator) % denominator) / denominator
            frequencies.append({
                "denominator": denominator,
                "numerator": numerator,
                "frequency": frequency,
                "coefficient": structured_sum * geometric,
            })
        primitive_parseval_error = max(
            primitive_parseval_error,
            abs(local_square_mass - sawtooth_gcd_mobius_transform(
                modulus, denominator)))

    direct_values = []
    frequency_values = []
    for ell in range(ell_first, ell_first + row_count):
        direct = sum(
            coefficient * _cyclic_discrepancy(modulus, ell, q)
            for q, coefficient in lcm_coefficients.items())
        expanded = sum(
            entry["coefficient"] * cmath.exp(
                2j * math.pi * entry["frequency"] * ell)
            for entry in frequencies)
        direct_values.append(direct)
        frequency_values.append(expanded)

    incomplete_energy = sum(
        abs(value) ** 2 for value in frequency_values) / row_count
    complete_energy = sum(
        abs(entry["coefficient"]) ** 2 for entry in frequencies)
    reconstruction_error = max(
        abs(direct - expanded)
        for direct, expanded in zip(direct_values, frequency_values))

    near_boundary = far_boundary = 0j
    pair_reconstruction_error = 0.0
    if decompose_pairs:
        for left_index, left in enumerate(frequencies):
            for right_index, right in enumerate(frequencies):
                if left_index == right_index:
                    continue
                difference = left["frequency"] - right["frequency"]
                distance = abs(difference - round(difference))
                contribution = (
                    left["coefficient"]
                    * right["coefficient"].conjugate()
                    * _interval_kernel(difference, ell_first, row_count))
                if distance <= 1 / row_count:
                    near_boundary += contribution
                else:
                    far_boundary += contribution
        pair_reconstruction_error = abs(
            incomplete_energy - complete_energy
            - (near_boundary + far_boundary).real)

    boundary = incomplete_energy - complete_energy
    return {
        "modulus": modulus,
        "ell_range": (ell_first, ell_first + row_count - 1),
        "ell_freeze": ell_freeze,
        "divisor_range": (divisor_lower, divisor_upper),
        "primitive_conductor_count": len(structured_sums),
        "primitive_frequency_count": len(frequencies),
        "maximum_row_reconstruction_error": reconstruction_error,
        "maximum_primitive_parseval_error": primitive_parseval_error,
        "incomplete_frequency_energy": incomplete_energy,
        "complete_primitive_energy": complete_energy,
        "incomplete_boundary_excess": boundary,
        "near_resonant_boundary_contribution": near_boundary.real,
        "far_boundary_contribution": far_boundary.real,
        "near_boundary_over_complete": (
            near_boundary.real / complete_energy if complete_energy else 0.0),
        "far_boundary_over_complete": (
            far_boundary.real / complete_energy if complete_energy else 0.0),
        "pair_boundary_reconstruction_error": pair_reconstruction_error,
        "near_resonance_threshold": 1 / row_count,
        "exact_primitive_frequency_factorization_proved": True,
        "incomplete_boundary_asymptotic_bound_proved": False,
    }


def primitive_conductor_operator_receipt(
        modulus, ell_first, row_count, ell_freeze,
        divisor_lower, divisor_upper):
    """Test the sharp incomplete-row operator on the conductor coordinates.

    The full nonzero Fourier packet for period ``d`` is

        d*d_(m,d)(ell)=sum_(e|d,e>1) Z_e(ell).

    Hence Mobius inversion gives the exact reduced-denominator packet

        Z_d(ell)=sum_(e|d,e>1)mu(d/e)e*d_(m,e)(ell).

    After normalizing column ``d`` by ``sqrt(H_m(d))``, the squared largest
    singular value of the row matrix is the sharp incomplete/complete energy
    ratio for arbitrary conductor coefficients.  The actual Mobius direction
    is evaluated separately.
    """
    if any(type(value) is not int for value in (
            modulus, ell_first, row_count, ell_freeze,
            divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell_first < 1 or row_count < 1 or ell_freeze < 1
            or divisor_lower < 1 or divisor_upper <= divisor_lower
            or divisor_upper >= modulus):
        raise ValueError("invalid conductor-operator ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")

    mobius, divisors, _, lcm_coefficients = _coefficient_data(
        modulus, ell_freeze, divisor_lower, divisor_upper)
    if not divisors:
        raise ValueError("the divisor interval has no squarefree values")
    structured_sums = {}
    for q, coefficient in lcm_coefficients.items():
        for divisor, _ in _squarefree_divisors_with_complement_mobius(q):
            if divisor > 1:
                structured_sums[divisor] = (
                    structured_sums.get(divisor, 0.0) + coefficient / q)

    active = []
    for divisor, structured_sum in sorted(structured_sums.items()):
        weight = sawtooth_gcd_mobius_transform(modulus, divisor)
        if weight > 0:
            active.append((divisor, structured_sum, weight))
    if not active:
        raise ArithmeticError("no positive primitive conductor weights")

    normalized_rows = np.array([
        [_primitive_discrepancy_packet(modulus, ell, divisor)
         / math.sqrt(weight)
         for divisor, _, weight in active]
        for ell in range(ell_first, ell_first + row_count)
    ], dtype=float) / math.sqrt(row_count)
    _, singular_values, right_singular = np.linalg.svd(
        normalized_rows, full_matrices=False)
    sharp_ratio = float(singular_values[0] ** 2)
    trace = float(np.sum(normalized_rows ** 2))
    rank_bound = min(row_count, len(active))
    trace_rank_lower_bound = trace / rank_bound

    actual_normalized = np.array([
        math.sqrt(weight) * structured_sum
        for _, structured_sum, weight in active], dtype=float)
    actual_complete = float(np.dot(actual_normalized, actual_normalized))
    actual_incomplete = float(np.dot(
        normalized_rows @ actual_normalized,
        normalized_rows @ actual_normalized))
    top_direction = right_singular[0]
    actual_unit = actual_normalized / math.sqrt(actual_complete)
    overlap = float(abs(np.dot(top_direction, actual_unit)) ** 2)

    # For fixed divisor support, every logarithmic coefficient vector is a
    # quadratic polynomial in log(X).  Measure the sharp operator only on
    # that three-dimensional structured span.
    lcm_polynomials = _lcm_coefficient_polynomials(divisors, mobius)
    polynomial_columns = []
    for divisor, _, weight in active:
        structured_polynomial = [0.0, 0.0, 0.0]
        for q, polynomial in lcm_polynomials.items():
            if q % divisor == 0:
                for index, coefficient in enumerate(polynomial):
                    structured_polynomial[index] += coefficient / q
        polynomial_columns.append([
            math.sqrt(weight) * value
            for value in structured_polynomial])
    polynomial_columns = np.array(polynomial_columns, dtype=float)
    polynomial_left, polynomial_singular, _ = np.linalg.svd(
        polynomial_columns, full_matrices=False)
    tolerance = max(polynomial_columns.shape) * np.finfo(float).eps * (
        polynomial_singular[0] if len(polynomial_singular) else 0.0)
    polynomial_rank = int(np.sum(polynomial_singular > tolerance))
    polynomial_basis = polynomial_left[:, :polynomial_rank]
    projected_singular = np.linalg.svd(
        normalized_rows @ polynomial_basis,
        compute_uv=False, full_matrices=False)
    structured_span_ratio = float(projected_singular[0] ** 2)
    polynomial_component_ratios = tuple(
        float(np.dot(normalized_rows @ polynomial_columns[:, index],
                     normalized_rows @ polynomial_columns[:, index])
              / np.dot(polynomial_columns[:, index],
                       polynomial_columns[:, index]))
        for index in range(3))
    complete_polynomial_gram = polynomial_columns.T @ polynomial_columns
    incomplete_polynomial_gram = (
        normalized_rows @ polynomial_columns).T @ (
            normalized_rows @ polynomial_columns)
    curve_ratio, curve_logarithm = _quadratic_curve_maximum(
        incomplete_polynomial_gram, complete_polynomial_gram,
        math.log(modulus * ell_first),
        math.log(modulus * (ell_first + row_count - 1)))

    degrees = np.array((2, 1, 0), dtype=int)
    row_logarithms = np.log(modulus * np.arange(
        ell_first, ell_first + row_count, dtype=float))
    base_polynomial_signals = normalized_rows @ polynomial_columns
    varying_signals = base_polynomial_signals * (
        row_logarithms[:, None] ** degrees[None, :])
    varying_incomplete_gram = varying_signals.T @ varying_signals
    varying_complete_gram = np.empty((3, 3), dtype=float)
    for left in range(3):
        for right in range(3):
            varying_complete_gram[left, right] = (
                complete_polynomial_gram[left, right]
                * float(np.mean(row_logarithms ** (
                    degrees[left] + degrees[right]))))
    denominator_values, denominator_vectors = np.linalg.eigh(
        varying_complete_gram)
    positive = denominator_values > (
        max(denominator_values) * np.finfo(float).eps * 100)
    inverse_square_root = (
        denominator_vectors[:, positive]
        / np.sqrt(denominator_values[positive]))
    varying_normalized_gram = (
        inverse_square_root.T @ varying_incomplete_gram
        @ inverse_square_root)
    varying_span_ratio = float(np.linalg.eigvalsh(
        (varying_normalized_gram + varying_normalized_gram.T) / 2)[-1])
    actual_selector = np.ones(3)
    actual_varying_incomplete = float(
        actual_selector @ varying_incomplete_gram @ actual_selector)
    actual_varying_complete = float(
        actual_selector @ varying_complete_gram @ actual_selector)

    return {
        "modulus": modulus,
        "ell_range": (ell_first, ell_first + row_count - 1),
        "ell_freeze": ell_freeze,
        "divisor_range": (divisor_lower, divisor_upper),
        "positive_primitive_conductor_count": len(active),
        "row_rank_upper_bound": rank_bound,
        "normalized_operator_trace": trace,
        "trace_rank_eigenvalue_lower_bound": trace_rank_lower_bound,
        "sharp_arbitrary_conductor_ratio": sharp_ratio,
        "actual_mobius_conductor_ratio": (
            actual_incomplete / actual_complete),
        "actual_top_resonance_squared_overlap": overlap,
        "quadratic_log_conductor_span_rank": polynomial_rank,
        "sharp_quadratic_log_span_ratio": structured_span_ratio,
        "quadratic_linear_constant_component_ratios": (
            polynomial_component_ratios),
        "sharp_project_log_curve_ratio": curve_ratio,
        "maximizing_project_logarithm": curve_logarithm,
        "sharp_row_varying_quadratic_span_ratio": varying_span_ratio,
        "actual_row_varying_incomplete_energy": actual_varying_incomplete,
        "actual_row_varying_complete_energy": actual_varying_complete,
        "actual_row_varying_energy_ratio": (
            actual_varying_incomplete / actual_varying_complete),
        "largest_eigenvalue_dominates_trace_rank_bound_verified": (
            sharp_ratio + 1e-10 >= trace_rank_lower_bound),
        "exact_conductor_packet_identity_proved": True,
        "uniform_conductor_operator_subpower_bound_proved": False,
        "actual_mobius_boundary_bound_proved": False,
    }


def project_prime_block_quadratic_scan(scale_modulus):
    """Scan every prime in ``[M,2M]`` on the project quadratic-log family."""
    if type(scale_modulus) is not int or scale_modulus < 17:
        raise ValueError("scale_modulus must be an integer at least 17")
    inferred_N = scale_modulus ** (1 / .59)
    row_count = int(inferred_N ** .41)
    divisor_lower = int(inferred_N ** .15)
    divisor_upper = int(inferred_N ** .32)
    flags = _prime_flags(2 * scale_modulus)
    rows = []
    for modulus in range(scale_modulus, 2 * scale_modulus + 1):
        if not flags[modulus]:
            continue
        receipt = primitive_conductor_operator_receipt(
            modulus, row_count, row_count,
            row_count + row_count // 2,
            divisor_lower, divisor_upper)
        rows.append({
            "modulus": modulus,
            "sharp_varying_span_ratio": receipt[
                "sharp_row_varying_quadratic_span_ratio"],
            "actual_varying_ratio": receipt[
                "actual_row_varying_energy_ratio"],
            "sharp_frozen_curve_ratio": receipt[
                "sharp_project_log_curve_ratio"],
        })
    if not rows:
        raise ArithmeticError("prime block is empty")
    return {
        "scale_modulus": scale_modulus,
        "inferred_N": inferred_N,
        "row_range": (row_count, 2 * row_count - 1),
        "divisor_range": (divisor_lower, divisor_upper),
        "prime_count": len(rows),
        "maximum_sharp_varying_span_ratio": max(
            row["sharp_varying_span_ratio"] for row in rows),
        "maximum_actual_varying_ratio": max(
            row["actual_varying_ratio"] for row in rows),
        "maximum_sharp_frozen_curve_ratio": max(
            row["sharp_frozen_curve_ratio"] for row in rows),
        "top_varying_span_rows": tuple(sorted(
            rows, key=lambda row: row["sharp_varying_span_ratio"],
            reverse=True)[:8]),
        "finite_whole_prime_block_scan": True,
        "row_varying_quadratic_span_bound_proved": False,
    }


if __name__ == "__main__":
    result = primitive_frequency_receipt(101, 47, 47, 70, 4, 14)
    print({key: result[key] for key in (
        "modulus", "divisor_range", "primitive_frequency_count",
        "incomplete_boundary_excess", "near_boundary_over_complete",
        "far_boundary_over_complete")})
    for controls in (
            (251, 47, 47, 70, 4, 20),
            (503, 75, 75, 112, 4, 29),
            (1009, 123, 123, 184, 5, 42)):
        result = primitive_conductor_operator_receipt(*controls)
        print({key: result[key] for key in (
            "modulus", "divisor_range", "positive_primitive_conductor_count",
            "trace_rank_eigenvalue_lower_bound",
            "sharp_arbitrary_conductor_ratio",
            "actual_mobius_conductor_ratio",
            "sharp_quadratic_log_span_ratio",
            "actual_top_resonance_squared_overlap")})
