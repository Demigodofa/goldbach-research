"""Test a shared-factor quadratic-character phase hypothesis.

For a conductor pair sharing a prime ``p``, use the first half of the ordered
prime block to choose between ``chi_p(m)`` and ``-chi_p(m)`` by weighted
correlation.  The second half is held out before sign accuracy is measured.
This is a deliberately rigid test of one arithmetic phase label; failure does
not reject richer character or residue decompositions.
"""

import math

from lcm_sawtooth_signed_conductor_ablation import (
    project_primewise_pair_rayleigh_receipt,
)
from mobius_covariance_endpoint_probe import _prime_flags


def quadratic_character(value, prime):
    """Return the Legendre symbol of ``value`` modulo an odd prime."""
    if (type(value) is not int or type(prime) is not int or prime < 3
            or not _prime_flags(prime)[prime]):
        raise ValueError("require an integer value and an odd prime")
    residue = value % prime
    if not residue:
        return 0
    return 1 if pow(residue, (prime - 1) // 2, prime) == 1 else -1


def character_sign_holdout_receipt(
        rows, prime_factor, training_count, required_fraction=.75):
    """Choose orientation on training rows and score held-out signs."""
    rows = tuple(rows)
    if (type(training_count) is not int
            or not 0 < training_count < len(rows)):
        raise ValueError("training count must split a nonempty row sequence")
    if not 0 < required_fraction <= 1:
        raise ValueError("required fraction must lie in (0,1]")
    parsed = tuple((
        int(row["modulus"]),
        float(row["off_diagonal_window_cross_rayleigh"]),
        quadratic_character(int(row["modulus"]), prime_factor),
    ) for row in rows)
    training = parsed[:training_count]
    held_out = parsed[training_count:]
    training_score = sum(value * character for _, value, character in training)
    orientation = 1 if training_score >= 0 else -1

    def correct(row):
        _, value, character = row
        if not value or not character:
            return False
        return (1 if value > 0 else -1) == orientation * character

    training_correct = sum(correct(row) for row in training)
    held_out_correct = sum(correct(row) for row in held_out)
    all_correct = sum(correct(row) for row in parsed)
    required_count = math.ceil(required_fraction * len(held_out))
    fair_sign_tail = sum(
        math.comb(len(held_out), count)
        for count in range(held_out_correct, len(held_out) + 1)
    ) / 2 ** len(held_out)
    absolute_mass = sum(abs(value) for _, value, _ in parsed)
    if not absolute_mass:
        raise ArithmeticError("all tested phase contributions are zero")
    return {
        "prime_factor": prime_factor,
        "training_count": len(training),
        "held_out_count": len(held_out),
        "required_fraction": required_fraction,
        "required_held_out_correct_count": required_count,
        "training_weighted_character_score": training_score,
        "selected_character_orientation": orientation,
        "training_correct_sign_count": training_correct,
        "held_out_correct_sign_count": held_out_correct,
        "all_correct_sign_count": all_correct,
        "held_out_fair_sign_tail_probability": fair_sign_tail,
        "all_sample_weighted_character_correlation": (
            sum(value * character for _, value, character in parsed)
            / absolute_mass),
        "held_out_character_sign_hypothesis_passes": bool(
            held_out_correct >= required_count),
        "quadratic_character_mechanism_proved": False,
        "signed_prime_correlation_proved": False,
    }


def project_shared_factor_character_receipt(
        scale_modulus, conductors, prime_factor):
    """Run the fixed half-block holdout on a conductor pair."""
    conductors = tuple(sorted(set(conductors)))
    if (len(conductors) != 2 or any(
            type(conductor) is not int or conductor < 2
            for conductor in conductors)):
        raise ValueError("require two distinct integer conductors")
    quadratic_character(1, prime_factor)
    if any(conductor % prime_factor for conductor in conductors):
        raise ValueError("prime factor must divide two distinct conductors")
    primewise = project_primewise_pair_rayleigh_receipt(
        scale_modulus, conductors)
    holdout = character_sign_holdout_receipt(
        primewise["rows"], prime_factor, len(primewise["rows"]) // 2)
    return {
        "scale_modulus": scale_modulus,
        "conductors": conductors,
        **holdout,
        "uniform_character_phase_rule_proved": False,
        "signed_prime_correlation_proved": False,
    }


def project_cluster_shared_factor_character_receipt(
        scale_modulus, pair_factors):
    """Require the shared-factor rule to pass every selected pair."""
    pair_factors = tuple(pair_factors)
    if not pair_factors:
        raise ValueError("at least one pair-factor test is required")
    rows = tuple(
        project_shared_factor_character_receipt(
            scale_modulus, conductors, prime_factor)
        for conductors, prime_factor in pair_factors)
    passing = tuple(
        row["conductors"] for row in rows
        if row["held_out_character_sign_hypothesis_passes"])
    return {
        "scale_modulus": scale_modulus,
        "rows": rows,
        "passing_pairs": passing,
        "all_pairs_pass": len(passing) == len(rows),
        "shared_factor_character_cluster_hypothesis_passes": bool(
            len(passing) == len(rows)),
        "uniform_character_phase_rule_proved": False,
        "signed_prime_correlation_proved": False,
    }
