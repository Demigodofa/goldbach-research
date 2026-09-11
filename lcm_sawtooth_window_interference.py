"""Split active-window packet interference into diagonal and off-diagonal.

For residue packets ``b_r,c_r`` modulo ``Q``, put

    B(ell)=sum_r b_r exp(2*pi*i*r*ell/Q),
    C(ell)=sum_r c_r exp(2*pi*i*r*ell/Q).

The active cross energy on ``R`` consecutive rows is

    (2Q/R) Re sum_ell B(ell) conjugate(C(ell))

and equals the full diagonal cross energy

    2Q Re sum_r b_r conjugate(c_r)

plus the terms ``r != s`` weighted by the normalized interval kernel

    K(h)=R^-1 sum_ell exp(2*pi*i*h*ell/Q).

For nonzero ``h mod Q``, geometric summation gives

    |K(h)| = |sin(pi*R*h/Q)| / (R*|sin(pi*h/Q)|)
           <= min(1, 1/(R*|sin(pi*h/Q)|)).

This identity exposes the off-diagonal phase sum but does not bound its signed
aggregate over primes.
"""

import cmath
import math

import numpy as np


def normalized_interval_kernel(
        residue_difference, denominator, row_first, row_count):
    """Return the normalized exponential kernel on consecutive rows."""
    if any(type(value) is not int for value in (
            residue_difference, denominator, row_first, row_count)):
        raise ValueError("kernel inputs must be integers")
    if denominator < 2 or row_count < 1:
        raise ValueError("require denominator at least two and positive rows")
    difference = residue_difference % denominator
    if not difference:
        return 1 + 0j
    root = cmath.exp(2j * math.pi * difference / denominator)
    return (
        root ** row_first * (1 - root ** row_count)
        / (row_count * (1 - root)))


def window_packet_interference_receipt(left, right, row_first, row_count):
    """Verify the diagonal/off-diagonal cross-energy decomposition."""
    left = np.asarray(left, dtype=complex)
    right = np.asarray(right, dtype=complex)
    if (left.ndim != 1 or right.shape != left.shape or len(left) < 2):
        raise ValueError("packets must be equal one-dimensional arrays")
    if (type(row_first) is not int or type(row_count) is not int
            or row_count < 1):
        raise ValueError("row range must be integral and nonempty")
    denominator = len(left)
    residues = np.arange(denominator)
    rows = np.arange(row_first, row_first + row_count)
    phases = np.exp(
        2j * np.pi * rows[:, None] * residues[None, :] / denominator)
    left_transform = phases @ left
    right_transform = phases @ right
    active_cross = float(
        2 * denominator / row_count
        * np.sum(left_transform * np.conjugate(right_transform)).real)
    diagonal_cross = float(
        2 * denominator * np.sum(left * np.conjugate(right)).real)

    kernel_cross = 0j
    maximum_kernel_bound_error = 0.0
    for left_residue in range(denominator):
        for right_residue in range(denominator):
            difference = left_residue - right_residue
            kernel = normalized_interval_kernel(
                difference, denominator, row_first, row_count)
            kernel_cross += (
                left[left_residue] * np.conjugate(right[right_residue])
                * kernel)
            if difference % denominator:
                sine = abs(math.sin(math.pi * difference / denominator))
                bound = min(1.0, 1 / (row_count * sine))
                maximum_kernel_bound_error = max(
                    maximum_kernel_bound_error, abs(kernel) - bound)
    kernel_cross = float(2 * denominator * kernel_cross.real)
    off_diagonal_cross = active_cross - diagonal_cross
    return {
        "denominator": denominator,
        "row_first": row_first,
        "row_count": row_count,
        "active_window_cross_energy": active_cross,
        "full_diagonal_cross_energy": diagonal_cross,
        "off_diagonal_window_cross_energy": off_diagonal_cross,
        "kernel_cross_energy": kernel_cross,
        "kernel_identity_residual": active_cross - kernel_cross,
        "diagonal_off_diagonal_residual": (
            active_cross - diagonal_cross - off_diagonal_cross),
        "maximum_interval_kernel_bound_error": maximum_kernel_bound_error,
        "exact_window_interference_decomposition_proved": True,
        "uniform_signed_off_diagonal_bound_proved": False,
        "signed_prime_correlation_proved": False,
    }
