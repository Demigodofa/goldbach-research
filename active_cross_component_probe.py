"""Decompose active cross-divisor energy into its exact mechanisms.

For raw progression transforms

 r_a(h)=sum_(ml<n<m(l+1),a|n) log(n/a)e_m(-hn),

the active Gram of u_a(h)=r_a(h)+S_a/(m-1) splits exactly as

 sum_(h in I)u_a(h)conj(u_b(h))
   = |I| sum_n f_a(n)f_b(n)                 [equality]
     + sum_(h in I) sum_(n!=n')             [unequal]
     + sum_(h in I)(u_a conj(u_b)-r_a conj(r_b)). [centering]

All terms retain the exact active modes, logs, endpoints, and outer weights.
The probe measures each off-diagonal matrix against the proven totient frame.
If the total is small only because equality and unequal pieces cancel, a proof
must retain their linkage; bounding them independently will lose the gain.
"""

import math

import numpy as np

from divisor_active_full_gram import _full_collision_gram
from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from mobius_cross_divisor_gram import _progression_vectors
from near_cutoff_geometric_bound import _active_modes


def _row_components(modulus, shift_length, ell, divisors):
    """Return equality, unequal, centering, and total active row Grams."""
    modes, centered_vectors = _progression_vectors(
        modulus, shift_length, ell, divisors)
    sums = np.empty(len(divisors))
    for index, divisor in enumerate(divisors):
        first = modulus * ell // divisor + 1
        last = (modulus * (ell + 1) - 1) // divisor
        sums[index] = float(np.sum(np.log(
            np.arange(first, last + 1, dtype=np.int64))))
    raw_vectors = centered_vectors - sums[:, None] / (modulus - 1)
    raw = raw_vectors @ np.conjugate(raw_vectors.T)
    total = centered_vectors @ np.conjugate(centered_vectors.T)
    collision = (_full_collision_gram(modulus, ell, divisors) / modulus
                 + np.outer(sums, sums) / (modulus - 1))
    equality = len(modes) * collision
    unequal = raw - equality
    centering = total - raw
    return equality, unequal, centering, total


def _component_receipt(equality, unequal, centering, total, frame):
    scale = np.sqrt(frame)
    names = ("equality", "unequal", "centering", "total")
    matrices = (equality, unequal, centering, total)
    receipt = {}
    row_arrays = {}
    off_diagonal_matrices = {}
    for name, matrix in zip(names, matrices):
        normalized = matrix / (scale[:, None] * scale[None, :])
        normalized = (normalized + np.conjugate(normalized.T)) / 2
        off_diagonal = normalized.copy()
        np.fill_diagonal(off_diagonal, 0)
        off_diagonal_matrices[name] = off_diagonal
        rows = np.sum(np.abs(off_diagonal), axis=1)
        row_arrays[name] = rows
        receipt[f"{name}_off_diagonal_row_sum_max"] = float(np.max(rows))
        receipt[f"{name}_off_diagonal_frobenius"] = float(
            np.linalg.norm(off_diagonal))
    worst_index = int(np.argmax(row_arrays["total"]))
    receipt["total_worst_row_index"] = worst_index
    for name in names:
        receipt[f"{name}_at_total_worst_row"] = float(
            row_arrays[name][worst_index])
    reconstruction = total - equality - unequal - centering
    receipt["reconstruction_error_max"] = float(np.max(np.abs(reconstruction)))
    component_sum = sum(
        receipt[f"{name}_off_diagonal_row_sum_max"]
        for name in ("equality", "unequal", "centering"))
    total_max = receipt["total_off_diagonal_row_sum_max"]
    receipt["separate_component_bound_over_total"] = (
        component_sum / total_max if total_max else 0.0)
    equality_norm = np.linalg.norm(off_diagonal_matrices["equality"])
    unequal_norm = np.linalg.norm(off_diagonal_matrices["unequal"])
    receipt["equality_unequal_frobenius_cosine"] = float(np.real(
        np.vdot(off_diagonal_matrices["equality"],
                off_diagonal_matrices["unequal"])
        / (equality_norm * unequal_norm)))
    receipt["equality_plus_unequal_over_equality_frobenius"] = float(
        np.linalg.norm(off_diagonal_matrices["equality"]
                       + off_diagonal_matrices["unequal"])
        / equality_norm)
    return receipt


def single_modulus_cross_components(modulus, shift_length, ell_first,
                                     row_count, divisor_left):
    """Aggregate the exact decomposition over consecutive rows."""
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
    matrices = [np.zeros((len(divisors), len(divisors)), dtype=complex)
                for _ in range(4)]
    frame = np.zeros(len(divisors))
    rho = len(_active_modes(modulus, shift_length)) / (modulus - 1)
    for ell in range(ell_first, ell_first + row_count):
        row = _row_components(modulus, shift_length, ell, divisors)
        for accumulator, component in zip(matrices, row):
            accumulator += (1 - rho) * component
        logs = np.log(modulus * ell / divisor_array)
        frame += rho * modulus ** 2 * logs ** 2 * (
            totients / divisor_array ** 2)
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "rho": rho,
        "ell_first": ell_first,
        "row_count": row_count,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisors": divisors,
        **_component_receipt(*matrices, frame),
    }


def finite_cross_components(N=32000, cofactor_left=None,
                            divisor_left=None, modulus_limit=None):
    """Aggregate the decomposition over the exact prime and row ranges."""
    if type(N) is not int or N < 1024 or N % 32:
        raise ValueError("N must be an integer multiple of 32 and at least 1024")
    H, M, V = int(N ** .1), int(N ** .59), int(N ** .15)
    if cofactor_left is None:
        cofactor_left = (N + 8 * M - 1) // (8 * M)
    if divisor_left is None:
        divisor_left = V
    if (type(cofactor_left) is not int or cofactor_left < 2
            or type(divisor_left) is not int or divisor_left < H):
        raise ValueError("require integer cofactor_left>=2 and divisor_left>=H")
    if modulus_limit is not None and (
            type(modulus_limit) is not int or modulus_limit < 1):
        raise ValueError("modulus_limit must be a positive integer")
    flags = _prime_flags(2 * M)
    primes = tuple(m for m in range(M + 1, 2 * M + 1) if flags[m])
    if modulus_limit is not None:
        primes = primes[:modulus_limit]
    if not primes:
        raise ValueError("the prime companion range must be nonempty")
    if (8 * primes[0] * cofactor_left < N
            or 16 * primes[-1] * cofactor_left > 7 * N):
        raise ValueError("the aligned block leaves the central annulus")
    if 2 * divisor_left >= primes[0]:
        raise ValueError("the divisor band must lie below every modulus")
    mobius = _mobius_values(2 * divisor_left)
    divisors = tuple(a for a in range(divisor_left + 1, 2 * divisor_left + 1)
                     if mobius[a])
    divisor_array = np.array(divisors, dtype=float)
    totients = np.array([_totient(a) for a in divisors], dtype=float)
    matrices = [np.zeros((len(divisors), len(divisors)), dtype=complex)
                for _ in range(4)]
    frame = np.zeros(len(divisors))
    for modulus in primes:
        rho = len(_active_modes(modulus, H)) / (modulus - 1)
        weight = math.log(modulus) ** 2 / modulus
        for ell in range(cofactor_left, 2 * cofactor_left):
            row = _row_components(modulus, H, ell, divisors)
            for accumulator, component in zip(matrices, row):
                accumulator += weight * (1 - rho) * component
            logs = np.log(modulus * ell / divisor_array)
            frame += weight * rho * modulus ** 2 * logs ** 2 * (
                totients / divisor_array ** 2)
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "cofactor_left": cofactor_left,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisors": divisors,
        "prime_count": len(primes),
        **_component_receipt(*matrices, frame),
    }


if __name__ == "__main__":
    for key, value in finite_cross_components().items():
        print(f"{key}: {value}")
