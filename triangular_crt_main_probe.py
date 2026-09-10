"""Test a triangular CRT main term for the complete raw active kernel.

Let R=m-1 and freeze logarithms at L_a=log(ml/a).  For signed difference r,
the smooth CRT pair-count model is

 C0_(a,b)(r)=1_(g|r)*(R-|r|)/q*L_a*L_b,
 g=gcd(a,b), q=lcm(a,b), |r|<R.                         (1)

Its complete active convolution uses

 T_g(h)=sum_(|r|<R,g|r)(R-|r|)e_m(-hr).                (2)

Writing R=gJ+s, 0<=s<g, and z=e_m(-hg), the exact sampled Fejer formula is

 T_g(h)=g*|sum_(j=0)^(J-1)z^j|^2+s*sum_(t=-J)^J z^t.  (3)

The probe compares (1)--(3) with the exact raw equality-plus-unequal Gram.
The concrete hypothesis is that the CRT main is already killed by the active
band and the exact remainder is small relative to the equality collision.
This finite test does not bound that remainder uniformly.
"""

import cmath
import math

import numpy as np

from active_cross_component_probe import _row_components
from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from near_cutoff_geometric_bound import _active_modes


def _triangular_kernel_direct(modulus, gcd_value, mode):
    R = modulus - 1
    limit = (R - 1) // gcd_value
    differences = gcd_value * np.arange(-limit, limit + 1, dtype=np.int64)
    return np.sum((R - np.abs(differences)) * np.exp(
        -2j * math.pi * mode * differences / modulus))


def _triangular_kernel_fejer(modulus, gcd_value, mode):
    """Return (3) by exact finite geometric-series quotients."""
    R = modulus - 1
    length, remainder = divmod(R, gcd_value)
    z = cmath.exp(-2j * math.pi * mode * gcd_value / modulus)
    denominator = 1 - z
    progression = (1 - z ** length) / denominator
    symmetric = (z ** (-length) * (1 - z ** (2 * length + 1))
                 / denominator)
    return gcd_value * abs(progression) ** 2 + remainder * symmetric


def triangular_crt_main_probe(modulus, shift_length, ell_first,
                              row_count, divisor_left):
    """Compare the exact raw active Gram with (1)--(3)."""
    if any(type(value) is not int for value in (
            modulus, shift_length, ell_first, row_count, divisor_left)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= divisor_left
            or 2 * divisor_left >= modulus
            or ell_first < 1 or row_count < 1):
        raise ValueError("invalid single-modulus ranges")
    flags = _prime_flags(modulus)
    if not flags[modulus]:
        raise ValueError("modulus must be prime")
    mobius = _mobius_values(2 * divisor_left)
    divisors = tuple(a for a in range(divisor_left + 1, 2 * divisor_left + 1)
                     if mobius[a])
    divisor_array = np.array(divisors, dtype=float)
    totients = np.array([_totient(a) for a in divisors], dtype=float)
    modes = _active_modes(modulus, shift_length)
    rho = len(modes) / (modulus - 1)
    gcd_values = {math.gcd(a, b) for a in divisors for b in divisors}
    triangular_sums = {
        gcd_value: float(np.real(sum(
            _triangular_kernel_fejer(modulus, gcd_value, mode)
            for mode in modes)))
        for gcd_value in gcd_values
    }
    exact_raw = np.zeros((len(divisors), len(divisors)), dtype=complex)
    main = np.zeros_like(exact_raw)
    equality = np.zeros_like(exact_raw)
    frame = np.zeros(len(divisors))
    for ell in range(ell_first, ell_first + row_count):
        row_equality, row_unequal, _, _ = _row_components(
            modulus, shift_length, ell, divisors)
        equality += (1 - rho) * row_equality
        exact_raw += (1 - rho) * (row_equality + row_unequal)
        logs = np.log(modulus * ell / divisor_array)
        for left_index, left in enumerate(divisors):
            for right_index, right in enumerate(divisors):
                gcd_value = math.gcd(left, right)
                main[left_index, right_index] += (
                    (1 - rho) * logs[left_index] * logs[right_index]
                    / math.lcm(left, right) * triangular_sums[gcd_value])
        frame += rho * modulus ** 2 * logs ** 2 * (
            totients / divisor_array ** 2)
    scale = np.sqrt(frame)
    normalized_equality = equality / (scale[:, None] * scale[None, :])
    normalized_exact = exact_raw / (scale[:, None] * scale[None, :])
    normalized_main = main / (scale[:, None] * scale[None, :])
    normalized_remainder = normalized_exact - normalized_main
    for matrix in (normalized_equality, normalized_exact,
                   normalized_main, normalized_remainder):
        np.fill_diagonal(matrix, 0)
    equality_norm = np.linalg.norm(normalized_equality)

    def frobenius_ratio(matrix):
        return float(np.linalg.norm(matrix) / equality_norm)

    def row_sum(matrix):
        return float(np.max(np.sum(np.abs(matrix), axis=1)))

    exact_norm = np.linalg.norm(normalized_exact)
    main_norm = np.linalg.norm(normalized_main)
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "ell_first": ell_first,
        "row_count": row_count,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisor_count": len(divisors),
        "exact_raw_frobenius_over_equality": frobenius_ratio(normalized_exact),
        "triangular_main_frobenius_over_equality":
            frobenius_ratio(normalized_main),
        "remainder_frobenius_over_equality":
            frobenius_ratio(normalized_remainder),
        "exact_raw_schur_row_sum": row_sum(normalized_exact),
        "triangular_main_schur_row_sum": row_sum(normalized_main),
        "remainder_schur_row_sum": row_sum(normalized_remainder),
        "exact_main_frobenius_cosine": float(
            np.vdot(normalized_exact, normalized_main).real
            / (exact_norm * main_norm)),
        "triangular_main_theorem_proved": False,
        "remainder_theorem_proved": False,
    }


if __name__ == "__main__":
    for key, value in triangular_crt_main_probe(1009, 5, 9, 8, 8).items():
        print(f"{key}: {value}")
