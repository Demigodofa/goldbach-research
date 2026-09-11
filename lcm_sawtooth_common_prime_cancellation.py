"""Test whether common assigned conductor primes explain residual cancellation.

For every ``d|lcm(a,b)``, split the pair contribution according to whether a
prime of ``d`` divides both ``a`` and ``b``.  If
``d_C=gcd(d,gcd(a,b))``, this gives

    K_(dr)/(dr) = z_separate(d,r) + z_common(d,r).

The resulting energy accounting separates cancellation across residuals from
interaction between the two assignment classes.  It is an exact diagnostic,
not an estimate for the Mobius sums.

Because
``mu(a)mu(b)=mu(d)mu(d_C)mu(alpha)mu(beta)``, multiplying each pair term by
``mu(d_C)`` removes only the alternating common-part sign.  The resulting
sign-aligned quotient is a counterfactual diagnostic and is not the original
coefficient system.
"""

import math
import statistics

from lcm_sawtooth_exact_gcd_factorization import (
    _squarefree_divisors_with_complement_mobius,
    sawtooth_gcd_mobius_transform,
)
from lcm_sawtooth_structured_divisor_sum import _coefficient_data
from mobius_covariance_endpoint_probe import _prime_flags


def _scope_metrics(coordinates, modulus, include_divisor):
    actual_numerator = actual_diagonal = 0.0
    separated_numerator = separated_diagonal = 0.0
    class_numerators = [0.0, 0.0]
    class_diagonals = [0.0, 0.0]
    sign_aligned_numerator = sign_aligned_diagonal = 0.0
    coordinate_count = 0
    for divisor, q_components in coordinates.items():
        if len(q_components) < 2 or not include_divisor(divisor):
            continue
        weight = sawtooth_gcd_mobius_transform(modulus, divisor)
        if weight <= 0:
            continue
        coordinate_count += 1
        actual_terms = tuple(
            separate + common
            for separate, common, _ in q_components.values())
        sign_aligned_terms = tuple(
            aligned for _, _, aligned in q_components.values())
        actual_numerator += weight * sum(actual_terms) ** 2
        actual_diagonal += weight * sum(
            term ** 2 for term in actual_terms)
        sign_aligned_numerator += weight * sum(sign_aligned_terms) ** 2
        sign_aligned_diagonal += weight * sum(
            term ** 2 for term in sign_aligned_terms)
        for feature in (0, 1):
            feature_terms = tuple(
                components[feature] for components in q_components.values())
            numerator = weight * sum(feature_terms) ** 2
            diagonal = weight * sum(term ** 2 for term in feature_terms)
            separated_numerator += numerator
            separated_diagonal += diagonal
            class_numerators[feature] += numerator
            class_diagonals[feature] += diagonal
    if actual_diagonal <= 0 or separated_diagonal <= 0:
        raise ArithmeticError("scope has no positive multi-residual diagonal")
    if separated_numerator <= 0:
        raise ArithmeticError("scope has zero feature-separated numerator")
    class_ratios = tuple(
        class_numerators[index] / class_diagonals[index]
        if class_diagonals[index] else 0.0
        for index in (0, 1))
    cross_numerator = actual_numerator - sum(class_numerators)
    cross_diagonal = actual_diagonal - sum(class_diagonals)

    def correlation(cross_term, components):
        product = components[0] * components[1]
        return cross_term / (2 * math.sqrt(product)) if product > 0 else 0.0

    collapsed_feature_correlation = correlation(
        cross_numerator, class_numerators)
    diagonal_feature_correlation = correlation(
        cross_diagonal, class_diagonals)
    actual_ratio = actual_numerator / actual_diagonal
    within_feature_ratio = separated_numerator / separated_diagonal
    cross_feature_numerator_factor = (
        actual_numerator / separated_numerator)
    cross_feature_diagonal_factor = actual_diagonal / separated_diagonal
    cross_feature_interference_factor = (
        cross_feature_numerator_factor / cross_feature_diagonal_factor)
    factored_ratio = (
        within_feature_ratio * cross_feature_numerator_factor
        / cross_feature_diagonal_factor)
    return {
        "coordinate_count": coordinate_count,
        "actual_numerator": actual_numerator,
        "actual_diagonal": actual_diagonal,
        "actual_residual_quotient": actual_ratio,
        "feature_separated_numerator": separated_numerator,
        "feature_separated_diagonal": separated_diagonal,
        "within_feature_residual_quotient": within_feature_ratio,
        "cross_feature_numerator_factor": cross_feature_numerator_factor,
        "cross_feature_diagonal_factor": cross_feature_diagonal_factor,
        "cross_feature_interference_factor": (
            cross_feature_interference_factor),
        "collapsed_feature_cross_term": cross_numerator,
        "diagonal_feature_cross_term": cross_diagonal,
        "collapsed_feature_correlation": collapsed_feature_correlation,
        "diagonal_feature_correlation": diagonal_feature_correlation,
        "common_sign_aligned_residual_quotient": (
            sign_aligned_numerator / sign_aligned_diagonal
            if sign_aligned_diagonal else 0.0),
        "common_sign_aligned_over_actual_quotient": (
            (sign_aligned_numerator / sign_aligned_diagonal) / actual_ratio
            if sign_aligned_diagonal else 0.0),
        "factored_actual_quotient": factored_ratio,
        "factorization_error": actual_ratio - factored_ratio,
        "separate_class_residual_quotient": class_ratios[0],
        "common_class_residual_quotient": class_ratios[1],
        "separate_class_diagonal_fraction": (
            class_diagonals[0] / separated_diagonal),
        "common_class_diagonal_fraction": (
            class_diagonals[1] / separated_diagonal),
    }


def project_common_prime_cancellation_probe(
        scale_modulus, prime_sample_count=8):
    """Sample the common/separate interference at project exponents."""
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
    cells = tuple(common_prime_cancellation_probe(
        modulus, ell, divisor_lower, divisor_upper) for modulus in moduli)

    def summary(scope, key):
        values = tuple(float(cell[scope][key]) for cell in cells)
        return (min(values), statistics.median(values), max(values))

    return {
        "scale_modulus": scale_modulus,
        "sampled_moduli": moduli,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "high_d_actual_quotient_min_median_max": summary(
            "high_d", "actual_residual_quotient"),
        "high_d_within_feature_quotient_min_median_max": summary(
            "high_d", "within_feature_residual_quotient"),
        "high_d_interference_factor_min_median_max": summary(
            "high_d", "cross_feature_interference_factor"),
        "dominant_actual_quotient_min_median_max": summary(
            "dominant_block", "actual_residual_quotient"),
        "dominant_within_feature_quotient_min_median_max": summary(
            "dominant_block", "within_feature_residual_quotient"),
        "dominant_interference_factor_min_median_max": summary(
            "dominant_block", "cross_feature_interference_factor"),
        "dominant_separate_quotient_min_median_max": summary(
            "dominant_block", "separate_class_residual_quotient"),
        "dominant_common_quotient_min_median_max": summary(
            "dominant_block", "common_class_residual_quotient"),
        "dominant_common_diagonal_fraction_min_median_max": summary(
            "dominant_block", "common_class_diagonal_fraction"),
        "dominant_collapsed_correlation_min_median_max": summary(
            "dominant_block", "collapsed_feature_correlation"),
        "dominant_diagonal_correlation_min_median_max": summary(
            "dominant_block", "diagonal_feature_correlation"),
        "dominant_sign_aligned_quotient_min_median_max": summary(
            "dominant_block", "common_sign_aligned_residual_quotient"),
        "dominant_sign_aligned_over_actual_min_median_max": summary(
            "dominant_block", "common_sign_aligned_over_actual_quotient"),
        "all_sampled_high_interference_is_cancelling": all(
            cell["high_d"]["cross_feature_interference_factor"] < 1
            for cell in cells),
        "all_sampled_dominant_interference_is_cancelling": all(
            cell["dominant_block"]["cross_feature_interference_factor"] < 1
            for cell in cells),
        "all_sampled_dominant_sign_alignment_increases_quotient": all(
            cell["dominant_block"][
                "common_sign_aligned_over_actual_quotient"] > 1
            for cell in cells),
        "finite_common_prime_interference_measurement": True,
        "common_part_sign_counterfactual_measured": True,
        "common_prime_cancellation_mechanism_proved": False,
    }


def common_prime_cancellation_probe(
        modulus, ell, divisor_lower, divisor_upper):
    """Decompose high and dominant-block residual energy by ``d_C>1``."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid common-prime ranges")
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
    coordinates = {}
    for left in divisors:
        for right in divisors:
            q = math.lcm(left, right)
            pair_term = coefficients[left] * coefficients[right] / q
            common_pair_part = math.gcd(left, right)
            for divisor in q_divisors[q]:
                components = coordinates.setdefault(
                    divisor, {}).setdefault(q, [0.0, 0.0, 0.0])
                common_assignment = math.gcd(divisor, common_pair_part)
                feature = int(common_assignment > 1)
                components[feature] += pair_term
                components[2] += pair_term * int(mobius[common_assignment])

    maximum_reconstruction_error = 0.0
    for divisor, q_components in coordinates.items():
        for q, components in q_components.items():
            maximum_reconstruction_error = max(
                maximum_reconstruction_error,
                abs(sum(components[:2]) - lcm_coefficients[q] / q))

    high_diagonal_by_block = {}
    for divisor, q_components in coordinates.items():
        if divisor <= divisor_upper or len(q_components) < 2:
            continue
        weight = sawtooth_gcd_mobius_transform(modulus, divisor)
        if weight <= 0:
            continue
        diagonal = weight * sum(
            (separate + common) ** 2
            for separate, common, _ in q_components.values())
        block = 1 << (divisor.bit_length() - 1)
        high_diagonal_by_block[block] = (
            high_diagonal_by_block.get(block, 0.0) + diagonal)
    if not high_diagonal_by_block:
        raise ArithmeticError("no positive high-conductor residual block")
    dominant_lower = max(high_diagonal_by_block, key=high_diagonal_by_block.get)
    high_metrics = _scope_metrics(
        coordinates, modulus, lambda divisor: divisor > divisor_upper)
    dominant_metrics = _scope_metrics(
        coordinates, modulus,
        lambda divisor: (
            divisor > divisor_upper
            and dominant_lower <= divisor < 2 * dominant_lower))
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "maximum_coefficient_reconstruction_error": (
            maximum_reconstruction_error),
        "high_d": high_metrics,
        "dominant_block_range": (dominant_lower, 2 * dominant_lower),
        "dominant_block": dominant_metrics,
        "common_prime_feature_decomposition_proved": True,
        "common_part_sign_counterfactual_measured": True,
        "common_prime_cancellation_mechanism_proved": False,
    }


if __name__ == "__main__":
    for scale in (251, 503, 1009, 2003, 4001, 8009, 16001):
        print(project_common_prime_cancellation_probe(scale))
