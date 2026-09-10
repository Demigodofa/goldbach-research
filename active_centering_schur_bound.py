"""Bound the active progression-centering correction by the totient frame.

For a complete row put

 r_a(h)=sum_(ml<ab<m(l+1)) log(b)e_m(-hab),
 S_a=sum_(ml<ab<m(l+1)) log(b),
 u_a(h)=r_a(h)+S_a/(m-1).

The centering part of the active Gram is exactly

 C_(a,b)=(1-rho){S_a/(m-1) conj(Q_b)
                  +S_b/(m-1) Q_a
                  +|I|S_aS_b/(m-1)^2},                 (1)

where Q_a=sum_(h in I)r_a(h).  The b-values in one progression occupy
distinct residues modulo the prime m.  With W_a=log(ml/a)+1/l and the
two-interval Dirichlet bound from ``crt_pair_discrepancy_bound.py``,

 S_a <= (m/a+1)W_a,
 |Q_a| <= 4m(1+log m)W_a.                              (2)

Equations (1)--(2) give the exact entry majorant implemented below.  Schur
then proves, on a dyadic band U<a,b<=2U,

 ||C||_(rho F)
 <<_eps N^eps{H U log(m)/m*(1+U/m)+1/m}.                (3)

At the project exponents the leading term is N^(-.34+eps).  This module
handles only the additive +S_a/(m-1) correction in the same complete row.
"""

import math

import numpy as np

from active_cross_component_probe import _row_components
from crt_pair_discrepancy_bound import dirichlet_residue_l1_bound
from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from near_cutoff_geometric_bound import _active_modes


def _require_prime(modulus):
    flags = _prime_flags(modulus)
    if not flags[modulus]:
        raise ValueError("modulus must be prime")


def _entry_bound_precomputed(modulus, rho, active_count, ell, left, right,
                             left_log, right_log, left_phi, right_phi):
    left_weight = left_log + 1 / ell
    right_weight = right_log + 1 / ell
    left_sum = (modulus / left + 1) * left_weight
    right_sum = (modulus / right + 1) * right_weight
    left_constant = left_sum / (modulus - 1)
    right_constant = right_sum / (modulus - 1)
    kernel_l1 = dirichlet_residue_l1_bound(modulus)
    left_frequency_sum = kernel_l1 * left_weight
    right_frequency_sum = kernel_l1 * right_weight
    centering = (1 - rho) * (
        left_constant * right_frequency_sum
        + right_constant * left_frequency_sum
        + active_count * left_constant * right_constant)
    frame_scale = (rho * modulus ** 2 * left_log * right_log
                   * math.sqrt(left_phi * right_phi) / (left * right))
    return centering / frame_scale


def centering_normalized_entry_bound(modulus, shift_length, ell,
                                     left, right):
    """Return the explicit frame-normalized majorant from (1)--(2)."""
    if any(type(value) is not int for value in (
            modulus, shift_length, ell, left, right)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= left < modulus
            or not 2 <= shift_length <= right < modulus or ell < 1):
        raise ValueError("require 2<=H<=a,b<m and ell>=1")
    _require_prime(modulus)
    modes = _active_modes(modulus, shift_length)
    if not modes:
        raise ValueError("the active frequency band must be nonempty")
    rho = len(modes) / (modulus - 1)
    left_log = math.log(modulus * ell / left)
    right_log = math.log(modulus * ell / right)
    return _entry_bound_precomputed(
        modulus, rho, len(modes), ell, left, right,
        left_log, right_log, _totient(left), _totient(right))


def row_centering_schur_bound(modulus, shift_length, ell, divisor_left,
                              compare_exact=False):
    """Return a rigorous normalized Schur bound for one complete row."""
    if any(type(value) is not int for value in (
            modulus, shift_length, ell, divisor_left)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= divisor_left
            or 2 * divisor_left >= modulus or ell < 1):
        raise ValueError("require 2<=H<=U, 2U<m, and ell>=1")
    _require_prime(modulus)
    modes = _active_modes(modulus, shift_length)
    if not modes:
        raise ValueError("the active frequency band must be nonempty")
    rho = len(modes) / (modulus - 1)
    mobius = _mobius_values(2 * divisor_left)
    divisors = tuple(a for a in range(divisor_left + 1, 2 * divisor_left + 1)
                     if mobius[a])
    logs = {a: math.log(modulus * ell / a) for a in divisors}
    totients = {a: _totient(a) for a in divisors}
    row_sums = tuple(sum(
        _entry_bound_precomputed(
            modulus, rho, len(modes), ell, left, right,
            logs[left], logs[right], totients[left], totients[right])
        for right in divisors)
        for left in divisors)
    result = {
        "modulus": modulus,
        "shift_length": shift_length,
        "ell": ell,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisor_count": len(divisors),
        "proved_centering_schur_bound": max(row_sums),
        "worst_divisor": divisors[row_sums.index(max(row_sums))],
        "centering_o_one_theorem": True,
        "shifted_rows_proved": False,
    }
    if compare_exact:
        centering = (1 - rho) * _row_components(
            modulus, shift_length, ell, divisors)[2]
        divisor_array = np.array(divisors, dtype=float)
        frame = (rho * modulus ** 2
                 * np.array([logs[a] for a in divisors]) ** 2
                 * np.array([totients[a] for a in divisors])
                 / divisor_array ** 2)
        normalized = centering / np.sqrt(frame[:, None] * frame[None, :])
        exact_rows = np.sum(np.abs(normalized), axis=1)
        result["exact_centering_schur_row_sum"] = float(np.max(exact_rows))
        result["proved_over_exact"] = (
            result["proved_centering_schur_bound"]
            / result["exact_centering_schur_row_sum"])
    return result


def near_cutoff_centering_schur_bound(N):
    """Maximize the row certificate over every saved project prime and row."""
    if type(N) is not int or N < 32000:
        raise ValueError("N must be an integer at least 32000")
    H, M, V = int(N ** .1), int(N ** .59), int(N ** .15)
    cofactor_left = (N + 8 * M - 1) // (8 * M)
    flags = _prime_flags(2 * M)
    primes = tuple(m for m in range(M + 1, 2 * M + 1) if flags[m])
    worst = None
    for modulus in primes:
        for ell in range(cofactor_left, 2 * cofactor_left):
            receipt = row_centering_schur_bound(
                modulus, H, ell, V, compare_exact=False)
            bound = receipt["proved_centering_schur_bound"]
            if worst is None or bound > worst["bound"]:
                worst = {
                    "bound": bound,
                    "modulus": modulus,
                    "ell": ell,
                    "divisor": receipt["worst_divisor"],
                }
    if worst is None:
        raise ValueError("the prime companion range must be nonempty")
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "cofactor_left": cofactor_left,
        "prime_count": len(primes),
        "uniform_proved_centering_schur_bound": worst["bound"],
        "worst_modulus": worst["modulus"],
        "worst_ell": worst["ell"],
        "worst_divisor": worst["divisor"],
        "centering_o_one_theorem": True,
        "shifted_rows_proved": False,
    }


if __name__ == "__main__":
    for key, value in near_cutoff_centering_schur_bound(32000).items():
        print(f"{key}: {value}")
