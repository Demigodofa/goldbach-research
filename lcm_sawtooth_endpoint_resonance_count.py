"""Count endpoint main-lobe resonances over complete project prime blocks."""

from lcm_sawtooth_endpoint_resonance_score import (
    endpoint_resonance_score_receipt,
)
from mobius_covariance_endpoint_probe import _prime_flags


def project_endpoint_resonance_count_receipt(scale_modulus):
    """Measure the unweighted endpoint-pair density on [M,2M]."""
    if type(scale_modulus) is not int or scale_modulus < 17:
        raise ValueError("scale_modulus must be an integer at least 17")
    inferred_N = scale_modulus ** (1 / .59)
    row_count = int(inferred_N ** .41)
    divisor_lower = int(inferred_N ** .15)
    divisor_upper = int(inferred_N ** .32)
    flags = _prime_flags(2 * scale_modulus)
    rows = []
    total_high_q = 0
    total_near = 0
    total_high_q_weight = 0.0
    total_near_weight = 0.0
    total_high_q_Q_squared_weight = 0.0
    total_near_Q_squared_weight = 0.0
    for modulus in range(scale_modulus, 2 * scale_modulus + 1):
        if not flags[modulus]:
            continue
        receipt = endpoint_resonance_score_receipt(
            modulus, row_count, row_count,
            row_count + row_count // 2,
            divisor_lower, divisor_upper)
        high_q = receipt["high_Q_endpoint_ordered_pair_count"]
        near = receipt["near_high_Q_ordered_pair_count"]
        total_high_q += high_q
        total_near += near
        high_q_weight = receipt[
            "high_Q_endpoint_coefficient_product_weight"]
        near_weight = receipt[
            "near_high_Q_endpoint_coefficient_product_weight"]
        total_high_q_weight += high_q_weight
        total_near_weight += near_weight
        total_high_q_Q_squared_weight += receipt[
            "high_Q_Q_weighted_squared_coefficient_product"]
        total_near_Q_squared_weight += receipt[
            "near_high_Q_Q_weighted_squared_coefficient_product"]
        rows.append({
            "modulus": modulus,
            "high_Q_endpoint_ordered_pair_count": high_q,
            "near_high_Q_ordered_pair_count": near,
            "row_count_scaled_near_pair_fraction": receipt[
                "row_count_scaled_near_high_Q_pair_fraction"],
            "Q_weighted_endpoint_square_score": receipt[
                "endpoint_near_Q_weighted_square_score"],
            "maximum_near_exact_Q_ordered_pair_multiplicity": receipt[
                "maximum_near_exact_Q_ordered_pair_multiplicity"],
            "row_count_scaled_near_coefficient_weight_fraction": receipt[
                "row_count_scaled_near_coefficient_weight_fraction"],
            "row_count_scaled_near_Q_squared_product_weight_fraction": receipt[
                "row_count_scaled_near_Q_squared_product_weight_fraction"],
        })
    if not rows or not total_high_q:
        raise ArithmeticError("prime block has no eligible endpoint pairs")
    aggregate_fraction = total_near / total_high_q
    return {
        "scale_modulus": scale_modulus,
        "inferred_N": inferred_N,
        "row_count": row_count,
        "divisor_range": (divisor_lower, divisor_upper),
        "prime_count": len(rows),
        "high_Q_endpoint_ordered_pair_count": total_high_q,
        "near_high_Q_ordered_pair_count": total_near,
        "aggregate_near_pair_fraction": aggregate_fraction,
        "row_count_scaled_aggregate_near_pair_fraction": (
            row_count * aggregate_fraction),
        "aggregate_near_coefficient_weight_fraction": (
            total_near_weight / total_high_q_weight),
        "row_count_scaled_aggregate_near_coefficient_weight_fraction": (
            row_count * total_near_weight / total_high_q_weight),
        "maximum_row_count_scaled_prime_coefficient_weight_fraction": max(
            row["row_count_scaled_near_coefficient_weight_fraction"]
            for row in rows),
        "row_count_scaled_aggregate_near_Q_squared_product_weight_fraction": (
            row_count * total_near_Q_squared_weight
            / total_high_q_Q_squared_weight),
        "maximum_row_count_scaled_prime_Q_squared_product_weight_fraction": (
            max(row[
                "row_count_scaled_near_Q_squared_product_weight_fraction"]
                for row in rows)),
        "maximum_near_exact_Q_ordered_pair_multiplicity": max(
            row["maximum_near_exact_Q_ordered_pair_multiplicity"]
            for row in rows),
        "maximum_row_count_scaled_prime_fraction": max(
            row["row_count_scaled_near_pair_fraction"] for row in rows),
        "top_resonance_count_rows": tuple(sorted(
            rows,
            key=lambda row: row["row_count_scaled_near_pair_fraction"],
            reverse=True)[:8]),
        "top_endpoint_square_score_rows": tuple(sorted(
            rows,
            key=lambda row: row["Q_weighted_endpoint_square_score"],
            reverse=True)[:8]),
        "finite_complete_prime_block_endpoint_count": True,
        "uniform_endpoint_resonance_count_bound_proved": False,
    }


if __name__ == "__main__":
    for scale in (251, 503, 1009, 2003):
        print(project_endpoint_resonance_count_receipt(scale))
