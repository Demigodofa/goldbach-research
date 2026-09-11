"""Dyadic localization of the exact multi-residual diagonal quotient.

For a primitive conductor ``d`` put ``y_(d,r)=K_(dr)/(dr)``.  This probe
localizes

    sum_d H_m(d) (sum_r y_(d,r))^2

and its diagonal to dyadic ranges of ``d``, retaining only coordinates with
at least two supported residuals.  A large quotient in one range would show
that the favorable global quotient merely averages over a resonant block.
"""

import statistics

from lcm_sawtooth_exact_gcd_factorization import (
    _squarefree_divisors_with_complement_mobius,
    sawtooth_gcd_mobius_transform,
)
from lcm_sawtooth_structured_divisor_sum import _coefficient_data
from mobius_covariance_endpoint_probe import _prime_flags


def _dyadic_lower(value):
    return 1 << (value.bit_length() - 1)


def dyadic_multi_residual_probe(
        modulus, ell, divisor_lower, divisor_upper):
    """Return exact all- and high-conductor multi-residual block quotients."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid residual-block ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")
    _, divisors, _, lcm_coefficients = _coefficient_data(
        modulus, ell, divisor_lower, divisor_upper)
    if not divisors:
        raise ValueError("the divisor interval has no squarefree values")

    residual_terms = {}
    for q, coefficient in lcm_coefficients.items():
        for divisor, _ in _squarefree_divisors_with_complement_mobius(q):
            residual_terms.setdefault(divisor, []).append(
                (q // divisor, coefficient / q))

    block_data = {}
    total_numerator = total_diagonal = 0.0
    high_numerator = high_diagonal = 0.0
    for divisor, residuals in residual_terms.items():
        if len(residuals) < 2:
            continue
        weight = sawtooth_gcd_mobius_transform(modulus, divisor)
        if weight <= 0:
            continue
        terms = tuple(term for _, term in residuals)
        numerator = weight * sum(terms) ** 2
        diagonal = weight * sum(term ** 2 for term in terms)
        total_numerator += numerator
        total_diagonal += diagonal
        if divisor > divisor_upper:
            high_numerator += numerator
            high_diagonal += diagonal
        lower = _dyadic_lower(divisor)
        entry = block_data.setdefault(lower, {
            "all_numerator": 0.0,
            "all_diagonal": 0.0,
            "all_coordinate_count": 0,
            "high_numerator": 0.0,
            "high_diagonal": 0.0,
            "high_coordinate_count": 0,
            "maximum_all_residual": 0,
            "maximum_high_residual": 0,
        })
        entry["all_numerator"] += numerator
        entry["all_diagonal"] += diagonal
        entry["all_coordinate_count"] += 1
        entry["maximum_all_residual"] = max(
            entry["maximum_all_residual"],
            max(residual for residual, _ in residuals))
        if divisor > divisor_upper:
            entry["high_numerator"] += numerator
            entry["high_diagonal"] += diagonal
            entry["high_coordinate_count"] += 1
            entry["maximum_high_residual"] = max(
                entry["maximum_high_residual"],
                max(residual for residual, _ in residuals))

    if total_diagonal <= 0 or high_diagonal <= 0:
        raise ArithmeticError("no positive multi-residual block diagonal")

    blocks = []
    for lower, entry in sorted(block_data.items()):
        all_diagonal = entry["all_diagonal"]
        high_diagonal_block = entry["high_diagonal"]
        blocks.append({
            "conductor_range": (lower, 2 * lower),
            "all_coordinate_count": entry["all_coordinate_count"],
            "all_quotient": (
                entry["all_numerator"] / all_diagonal
                if all_diagonal else 0.0),
            "all_diagonal_fraction": all_diagonal / total_diagonal,
            "high_coordinate_count": entry["high_coordinate_count"],
            "high_quotient": (
                entry["high_numerator"] / high_diagonal_block
                if high_diagonal_block else 0.0),
            "high_diagonal_fraction": high_diagonal_block / high_diagonal,
            "maximum_all_residual": entry["maximum_all_residual"],
            "maximum_high_residual": entry["maximum_high_residual"],
        })
    positive_high_blocks = [
        block for block in blocks if block["high_coordinate_count"]]
    largest_high_quotient_block = max(
        positive_high_blocks, key=lambda block: block["high_quotient"])
    largest_high_diagonal_block = max(
        positive_high_blocks, key=lambda block: block["high_diagonal_fraction"])
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "multi_residual_numerator": total_numerator,
        "multi_residual_diagonal": total_diagonal,
        "multi_residual_quotient": total_numerator / total_diagonal,
        "high_d_multi_residual_numerator": high_numerator,
        "high_d_multi_residual_diagonal": high_diagonal,
        "high_d_multi_residual_quotient": high_numerator / high_diagonal,
        "blocks": tuple(blocks),
        "largest_high_quotient_block": largest_high_quotient_block,
        "largest_high_diagonal_block": largest_high_diagonal_block,
        "dyadic_multi_residual_identity_proved": True,
        "dyadic_multi_residual_subpower_bound_proved": False,
    }


def project_dyadic_multi_residual_probe(
        scale_modulus, prime_sample_count=8):
    """Sample dyadic residual quotients at the saved project exponents."""
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
    cells = tuple(dyadic_multi_residual_probe(
        modulus, ell, divisor_lower, divisor_upper) for modulus in moduli)

    def summary(values):
        values = tuple(float(value) for value in values)
        return (min(values), statistics.median(values), max(values))

    worst_cell = max(
        cells,
        key=lambda cell: cell["largest_high_quotient_block"][
            "high_quotient"])
    worst_block = worst_cell["largest_high_quotient_block"]
    return {
        "scale_modulus": scale_modulus,
        "sampled_moduli": moduli,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "high_d_global_quotient_min_median_max": summary(
            cell["high_d_multi_residual_quotient"] for cell in cells),
        "largest_high_block_quotient_min_median_max": summary(
            cell["largest_high_quotient_block"]["high_quotient"]
            for cell in cells),
        "dominant_high_diagonal_block_quotient_min_median_max": summary(
            cell["largest_high_diagonal_block"]["high_quotient"]
            for cell in cells),
        "dominant_high_diagonal_block_fraction_min_median_max": summary(
            cell["largest_high_diagonal_block"]["high_diagonal_fraction"]
            for cell in cells),
        "worst_sampled_block": {
            "modulus": worst_cell["modulus"],
            "conductor_range": worst_block["conductor_range"],
            "quotient": worst_block["high_quotient"],
            "high_diagonal_fraction": worst_block[
                "high_diagonal_fraction"],
            "coordinate_count": worst_block["high_coordinate_count"],
        },
        "finite_project_dyadic_residual_measurement": True,
        "dyadic_multi_residual_subpower_bound_proved": False,
    }


if __name__ == "__main__":
    for scale in (251, 503, 1009, 2003, 4001, 8009, 16001):
        print(project_dyadic_multi_residual_probe(scale))
