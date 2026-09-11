"""Exact Boolean inclusion-exclusion identity for conductor packets.

Let a Hilbert-space signal be partitioned into packets ``a,b,c,d`` according
to whether a source term uses neither selected conductor, only the left one,
only the right one, or both.  The Boolean mixed difference of its energy is

    ||a+b+c+d||^2 - ||a+b||^2 - ||a+c||^2 + ||a||^2

      = ||d||^2 + 2 Re(<b,c> + <a+b+c,d>).

This follows by expanding the four squared norms and cancelling like terms.
It holds in any real or complex Hilbert space, so it applies separately to
the full-residue and active-window energy inner products.  The identity has
no fixed sign: the positive mixed-packet square competes with two interference
terms.  It therefore organizes the finite stabilization mechanism without
supplying the missing uniform signed estimate.
"""

import math

import numpy as np


def boolean_energy_interaction_receipt(neither, left, right, both):
    """Evaluate both sides and the direct Cauchy lower bound."""
    packets = tuple(
        np.asarray(packet, dtype=complex)
        for packet in (neither, left, right, both))
    if not packets[0].size or any(
            packet.shape != packets[0].shape for packet in packets[1:]):
        raise ValueError("packets must be nonempty arrays of the same shape")
    neither, left, right, both = packets

    def energy(vector):
        return float(np.vdot(vector, vector).real)

    baseline = neither + left + right + both
    exclude_left = neither + right
    exclude_right = neither + left
    exclude_both = neither
    boolean_difference = (
        energy(baseline) - energy(exclude_right)
        - energy(exclude_left) + energy(exclude_both))

    mixed_packet_square = energy(both)
    direct_single_interference = 2 * float(np.vdot(left, right).real)
    mixed_packet_interference = 2 * float(
        np.vdot(neither + left + right, both).real)
    expanded = (
        mixed_packet_square
        + direct_single_interference
        + mixed_packet_interference)
    cauchy_lower_bound = (
        mixed_packet_square
        - 2 * float(np.linalg.norm(left)) * float(np.linalg.norm(right))
        - 2 * float(np.linalg.norm(neither + left + right))
        * float(np.linalg.norm(both)))
    return {
        "boolean_energy_difference": boolean_difference,
        "mixed_packet_square": mixed_packet_square,
        "direct_single_packet_interference": direct_single_interference,
        "mixed_packet_interference": mixed_packet_interference,
        "expanded_energy_difference": expanded,
        "identity_residual": boolean_difference - expanded,
        "cauchy_lower_bound": cauchy_lower_bound,
        "exact_boolean_energy_interaction_identity_proved": True,
        "boolean_energy_interaction_nonnegative_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


def mixed_packet_high_q_obstruction_receipt(
        left_conductor, right_conductor, modulus, row_count):
    """Certify when every direct mixed-conductor pair misses ``q>mR``."""
    values = (left_conductor, right_conductor, modulus, row_count)
    if any(type(value) is not int or value < 1 for value in values):
        raise ValueError("conductors, modulus, and row count must be integers")
    if left_conductor < 2 or right_conductor < 2:
        raise ValueError("conductors must be at least two")
    if left_conductor == right_conductor:
        raise ValueError("conductors must be distinct")
    common_denominator = math.lcm(left_conductor, right_conductor)
    threshold = modulus * row_count
    forced_zero = common_denominator <= threshold
    return {
        "left_conductor": left_conductor,
        "right_conductor": right_conductor,
        "common_denominator": common_denominator,
        "high_q_threshold": threshold,
        "maximum_possible_reduced_denominator": common_denominator,
        "mixed_packet_zero_in_high_q_signal_proved": forced_zero,
        "mixed_packet_presence_proved": False,
        "signed_prime_correlation_proved": False,
    }
