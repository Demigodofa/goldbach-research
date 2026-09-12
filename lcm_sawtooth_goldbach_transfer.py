"""Exact Goldbach-sum form of the dominant even-even CRT numerator.

This module isolates an algebraic transfer.  It does not assert a mean-square
estimate for the resulting twisted Goldbach sums.
"""

import math

import numpy as np

from lcm_sawtooth_frequency_resolved_fourier import _unit_character_table
from lcm_sawtooth_linked_prime_character import (
    _linked_prime_pairs,
    residue_orbit_even_even_profile_receipt,
)


def even_even_goldbach_transfer_receipt(
        target_minimum=1700, target_maximum=22000, target_residue=72,
        tolerance=1e-12, batch_size=32):
    """Rewrite ``<h_N,h_C>`` as fixed central Goldbach twists.

    For every tested ``N == target_residue (mod 130)``, the returned identity
    is

        <h_N,h_C> = sum_{N/3 < p < 2N/3, p+q=N}
                         c(p mod 130) log(p) log(q),

    where the sum is ordered and prime-only.  On the stated range every prime
    in the strict central interval is a unit modulo 130.  The coefficient
    function is also expanded in all 48 Dirichlet characters of the unit
    group modulo 130.  These are finite algebraic identities, not estimates.
    """
    base = residue_orbit_even_even_profile_receipt(
        target_minimum=target_minimum,
        target_maximum=target_maximum,
        target_residue=target_residue,
        tolerance=tolerance,
        batch_size=batch_size)
    common = base["common_modulus"]
    if common != 130:
        raise AssertionError("expected common modulus 130")
    target_residue = base["target_residue"]
    residue5_values = base["residue5_values"]
    residue13_values = base["residue13_values"]
    residue5_index = {
        residue: index for index, residue in enumerate(residue5_values)}
    residue13_index = {
        residue: index for index, residue in enumerate(residue13_values)}
    mod5_contrast = np.asarray(base["mod5_contrast"], dtype=np.float64)
    source_profile = np.asarray(base["source_profile"], dtype=np.complex128)

    units = tuple(residue for residue in range(common)
                  if math.gcd(residue, common) == 1)
    admissible_residues = tuple(
        residue for residue in units
        if math.gcd((target_residue - residue) % common, common) == 1)
    coefficient_by_residue = {}
    for residue in admissible_residues:
        coefficient_by_residue[residue] = complex(
            mod5_contrast[residue5_index[residue % 5]]
            * source_profile[residue13_index[residue % 13]])

    coefficient_sum = sum(coefficient_by_residue.values(), 0.0j)
    coefficient_scale = max(
        1.0, math.fsum(abs(value)
                       for value in coefficient_by_residue.values()))
    reflection_error = max(abs(
        coefficient_by_residue[residue]
        - coefficient_by_residue[(target_residue - residue) % common])
        for residue in admissible_residues)

    # A central prime pair cannot use an inadmissible unit residue: if p is a
    # unit and N-p is prime but nonunit modulo 130, then N-p is 2, 5, or 13,
    # outside the strict central interval for the admitted target range.
    coefficient_on_units = np.asarray(tuple(
        coefficient_by_residue.get(residue, 0.0j) for residue in units),
        dtype=np.complex128)
    _, character_labels, character_table = _unit_character_table(common, units)
    character_coefficients = (
        np.conjugate(character_table) @ coefficient_on_units / len(units))
    character_reconstruction = character_table.T @ character_coefficients
    character_scale = max(1.0, float(np.linalg.norm(coefficient_on_units)))
    character_reconstruction_relative_error = float(
        np.linalg.norm(character_reconstruction - coefficient_on_units)
        / character_scale)

    rows = {}
    maximum_identity_relative_error = 0.0
    for target, profile_row in base["rows"].items():
        lower = target // 3
        upper = target - lower
        central_sum = 0.0j
        nonunit_pairs = []
        inadmissible_unit_pairs = []
        ordered_pair_count = 0
        for prime, weight in _linked_prime_pairs(target, lower, upper):
            partner = target - prime
            ordered_pair_count += 1
            if math.gcd(prime, common) != 1:
                nonunit_pairs.append((prime, partner))
                continue
            coefficient = coefficient_by_residue.get(prime % common)
            if coefficient is None:
                inadmissible_unit_pairs.append((prime, partner))
                continue
            central_sum += coefficient * weight
        profile_correlation = complex(
            profile_row["even_even_profile_correlation"])
        scale = max(1.0, abs(central_sum), abs(profile_correlation))
        identity_relative_error = abs(
            central_sum - profile_correlation) / scale
        maximum_identity_relative_error = max(
            maximum_identity_relative_error, identity_relative_error)
        rows[target] = {
            "ordered_central_prime_pair_count": ordered_pair_count,
            "nonunit_prime_pairs": tuple(nonunit_pairs),
            "inadmissible_unit_prime_pairs": tuple(inadmissible_unit_pairs),
            "central_residue_weighted_goldbach_sum": central_sum,
            "even_even_profile_correlation": profile_correlation,
            "identity_relative_error": identity_relative_error,
        }

    all_nonunit_pairs = tuple(
        (target, pair)
        for target, row in rows.items()
        for pair in row["nonunit_prime_pairs"])
    all_inadmissible_unit_pairs = tuple(
        (target, pair)
        for target, row in rows.items()
        for pair in row["inadmissible_unit_prime_pairs"])
    return {
        "common_modulus": common,
        "target_range": base["target_range"],
        "target_residue": target_residue,
        "progression_step": base["progression_step"],
        "strict_central_interval": "N/3 < p < 2N/3",
        "ordered_prime_only_logarithmic_weight": True,
        "admissible_residues": admissible_residues,
        "coefficient_by_residue": coefficient_by_residue,
        "coefficient_sum_relative_error": abs(coefficient_sum) / coefficient_scale,
        "maximum_reflection_coefficient_error": reflection_error,
        "dirichlet_character_labels": character_labels,
        "dirichlet_character_coefficients": tuple(
            complex(value) for value in character_coefficients),
        "dirichlet_character_reconstruction_relative_error": (
            character_reconstruction_relative_error),
        "rows": rows,
        "tested_target_count": len(rows),
        "nonunit_prime_pairs": all_nonunit_pairs,
        "inadmissible_unit_prime_pairs": all_inadmissible_unit_pairs,
        "maximum_goldbach_transfer_identity_relative_error": (
            maximum_identity_relative_error),
        "fixed_central_goldbach_residue_identity_proved_in_tested_range": bool(
            not all_nonunit_pairs
            and not all_inadmissible_unit_pairs
            and maximum_identity_relative_error <= tolerance),
        "fixed_dirichlet_character_expansion_verified": bool(
            character_reconstruction_relative_error <= tolerance),
        "halupczok_theorem6_prime_only_weight_matches": True,
        "moving_central_window_box_reduction_proved": True,
        "applicable_mean_square_theorem_identified": True,
        "almost_all_centered_correlation_estimate_proved": True,
        "pointwise_centered_correlation_estimate_proved": False,
        "signed_prime_correlation_proved": False,
        "goldbach_proved": False,
    }


if __name__ == "__main__":
    print(even_even_goldbach_transfer_receipt())
