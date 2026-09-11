"""Compare endpoint-resonance scores with full aggregate row quotients."""

import numpy as np

from lcm_sawtooth_global_residue_energy import (
    global_residue_energy_receipt,
)


def _ordinal_ranks(values):
    order = np.argsort(values)
    ranks = np.empty(len(values), dtype=float)
    ranks[order] = np.arange(len(values), dtype=float)
    return ranks


def endpoint_resonance_scan_receipt(
        moduli, ell_first, row_count, ell_freeze,
        divisor_lower, divisor_upper, exceptional_count=2):
    """Return a finite rank comparison on a named prime fixture family."""
    if (not isinstance(moduli, tuple) or len(moduli) < 2
            or len(set(moduli)) != len(moduli)):
        raise ValueError("moduli must be at least two distinct integers")
    if (type(exceptional_count) is not int
            or not 1 <= exceptional_count < len(moduli)):
        raise ValueError("exceptional_count must be between 1 and len-1")
    rows = []
    for modulus in moduli:
        receipt = global_residue_energy_receipt(
            modulus, ell_first, row_count, ell_freeze,
            divisor_lower, divisor_upper)
        rows.append({
            "modulus": modulus,
            "full_row_quotient": receipt[
                "row_count_scaled_packet_square_over_active_window_l2"],
            "normalized_endpoint_score": receipt[
                "endpoint_near_score_over_active_window_l2"],
            "endpoint_pair_square_envelope_over_active_window_l2": receipt[
                "endpoint_pair_square_envelope_over_active_window_l2"],
            "endpoint_packet_cauchy_bound_over_active_window_l2": receipt[
                "endpoint_near_packet_cauchy_bound_over_active_window_l2"],
        })
    full = np.array([row["full_row_quotient"] for row in rows])
    endpoint = np.array([row["normalized_endpoint_score"] for row in rows])
    full_rank = _ordinal_ranks(full)
    endpoint_rank = _ordinal_ranks(endpoint)
    full_leaders = tuple(
        rows[index]["modulus"]
        for index in np.argsort(full)[-exceptional_count:][::-1])
    endpoint_leaders = tuple(
        rows[index]["modulus"]
        for index in np.argsort(endpoint)[-exceptional_count:][::-1])
    return {
        "fixture_count": len(rows),
        "exceptional_count": exceptional_count,
        "rows": tuple(rows),
        "full_quotient_leaders": full_leaders,
        "endpoint_score_leaders": endpoint_leaders,
        "exceptional_leader_sets_match": (
            set(full_leaders) == set(endpoint_leaders)),
        "raw_pearson_correlation": float(np.corrcoef(full, endpoint)[0, 1]),
        "spearman_rank_correlation": float(
            np.corrcoef(full_rank, endpoint_rank)[0, 1]),
        "endpoint_pair_square_envelope_ratio_range": (
            min(row["endpoint_pair_square_envelope_over_active_window_l2"]
                for row in rows),
            max(row["endpoint_pair_square_envelope_over_active_window_l2"]
                for row in rows)),
        "endpoint_packet_cauchy_bound_ratio_range": (
            min(row[
                "endpoint_packet_cauchy_bound_over_active_window_l2"]
                for row in rows),
            max(row[
                "endpoint_packet_cauchy_bound_over_active_window_l2"]
                for row in rows)),
        "finite_endpoint_score_scan": True,
        "endpoint_score_predicts_uniform_row_bound_proved": False,
    }


if __name__ == "__main__":
    print(endpoint_resonance_scan_receipt(
        (439, 457, 461, 463, 479, 487, 491, 499, 503, 509),
        46, 46, 69, 4, 20))
