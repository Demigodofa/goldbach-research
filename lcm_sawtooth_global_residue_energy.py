"""Measure the full high-Q residue energy and the loss in row averaging.

The exact-Q additive transform satisfies

    C_Q=A^-1 sum_(ell in I) T_Q(ell).

Jensen bounds ``Q|C_Q|^2`` by the active-window mean of ``Q|T_Q|^2``.
This receipt sums that comparison over every high-Q packet and separately
measures active-window versus full-period L2 energy.  It identifies whether
spectral equidistribution alone is strong enough; it proves no asymptotic
estimate. It also expands the normalized row-mean quotient exactly into
signed correlations at every positive row lag.
"""

from lcm_sawtooth_fixed_q_residue import fixed_q_residue_receipt
from lcm_sawtooth_signed_difference_bins import signed_difference_bin_receipt


def global_residue_energy_receipt(
        modulus, ell_first, row_count, ell_freeze,
        divisor_lower, divisor_upper):
    signed = signed_difference_bin_receipt(
        modulus, ell_first, row_count, ell_freeze,
        divisor_lower, divisor_upper, False)
    denominators = signed["high_Q_denominators"]
    if not denominators:
        raise ValueError("the fixture has no high-Q packets")
    residue = fixed_q_residue_receipt(
        modulus, ell_first, row_count, ell_freeze,
        divisor_lower, divisor_upper, denominators)
    packets = residue["packets"]
    full_weighted = sum(
        packet["Q_weighted_residue_l2_over_complete_squared"]
        for packet in packets)
    active_weighted = sum(
        packet["Q_weighted_residue_l2_over_complete_squared"]
        * packet["active_window_transform_l2_over_full_period"]
        for packet in packets)
    packet_square = signed[
        "high_Q_Q_weighted_packet_square_over_complete_squared"]
    active_transform_energy = sum(
        packet["denominator"]
        * packet[
            "active_window_transform_energy_over_complete_squared"]
        for packet in packets)
    lag_contributions = tuple(
        (
            lag,
            2 * sum(
                packet["denominator"]
                * packet[
                    "active_window_lag_inner_products_over_complete_squared"
                ][lag - 1].real
                for packet in packets)
            / active_transform_energy,
        )
        for lag in range(1, row_count))
    lag_values = tuple(value for _, value in lag_contributions)
    absolute_lag_sum = sum(abs(value) for value in lag_values)
    ranked_lags = tuple(sorted(
        lag_contributions, key=lambda item: abs(item[1]), reverse=True))
    row_mean_ratio = row_count * packet_square / active_weighted
    ratios = tuple(
        packet["active_window_transform_l2_over_full_period"]
        for packet in packets)
    return {
        "modulus": modulus,
        "ell_range": (ell_first, ell_first + row_count - 1),
        "ell_freeze": ell_freeze,
        "divisor_range": (divisor_lower, divisor_upper),
        "high_Q_packet_count": len(denominators),
        "global_Q_weighted_residue_l2_over_complete_squared": full_weighted,
        "active_window_Q_weighted_l2_over_complete_squared": active_weighted,
        "packet_Q_weighted_square_over_complete_squared": packet_square,
        "weighted_active_window_over_full_period": (
            active_weighted / full_weighted),
        "packet_square_over_active_window_l2": (
            packet_square / active_weighted),
        "row_count_scaled_packet_square_over_active_window_l2": (
            row_mean_ratio),
        "normalized_aggregate_lag_contributions": lag_contributions,
        "largest_absolute_aggregate_lag_contributions": ranked_lags[:10],
        "absolute_aggregate_lag_contribution_sum": absolute_lag_sum,
        "top_five_absolute_lag_mass_fraction": (
            sum(abs(value) for _, value in ranked_lags[:5])
            / absolute_lag_sum if absolute_lag_sum else 0.0),
        "first_five_absolute_lag_mass_fraction": (
            sum(abs(value) for value in lag_values[:5])
            / absolute_lag_sum if absolute_lag_sum else 0.0),
        "lag_expansion_reconstruction_error": abs(
            1 + sum(lag_values) - row_mean_ratio),
        "active_window_ratio_minimum": min(ratios),
        "active_window_ratio_maximum": max(ratios),
        "finite_global_residue_energy_measurement": True,
        "window_l2_equidistribution_bound_proved": False,
        "row_mean_cancellation_bound_proved": False,
    }


if __name__ == "__main__":
    print(global_residue_energy_receipt(251, 46, 46, 69, 4, 20))
