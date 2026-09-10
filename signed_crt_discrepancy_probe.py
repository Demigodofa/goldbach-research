"""Falsify cancellation in the signed CRT endpoint discrepancy.

Fix a prime modulus ``m``, a complete row ``ml<n<m(l+1)``, and squarefree
divisors ``U<a<=2U``.  For ``R=m-1`` and ``|s|<R``, let ``C_ab(s)`` count
pairs ``x,y in [1,R]`` with ``x-y=s``, ``a|(ml+x)``, and ``b|(ml+y)``.
If ``g=(a,b)`` and ``q=[a,b]``, compatibility is ``g|s`` and

    C_ab(s) = (R-|s|)/q + E_ab(s).

For the unique compatible residue ``y0 (mod q)`` and the allowed interval
``L<=y<=T``, the endpoint error is exactly

    E_ab(s) = {(L-1-y0)/q} - {(T-y0)/q}.                 (1)

Thus it has a sign and telescoping endpoint structure that the earlier
``|E_ab(s)|<1`` estimate discarded.  This probe constructs the exact active
matrix

    D_ab=(1-rho) sum_(h in I) sum_s E_ab(s)e_m(-hs)     (2)

as the exact unweighted progression Gram minus its triangular CRT density.
It normalizes by the totient frame and reports the largest absolute
eigenvalue, which is the exact finite maximum over arbitrary complex
coefficients.  It also reports the Mobius Rayleigh quotient and the much
larger unsigned endpoint certificate.

The concrete falsifier is growth of the signed operator on the scale
``H*U^2/m`` when ``U`` crosses ``sqrt(m/H)``.  Bounded or falling normalized
operators are evidence for cancellation, not a theorem.  Averaging several
prime moduli is available as a separate test of prime-modulus cancellation.
"""

import math

import numpy as np

from crt_pair_discrepancy_bound import dirichlet_residue_l1_bound
from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from near_cutoff_geometric_bound import _active_modes
from triangular_crt_main_probe import _triangular_kernel_fejer


def _fractional_part(value):
    return value - math.floor(value)


def crt_interval_count_error(lower, upper, residue, modulus):
    """Return the direct count and the exact fractional-part formula (1)."""
    if any(type(value) is not int for value in (
            lower, upper, residue, modulus)):
        raise ValueError("all arguments must be integers")
    if modulus < 1 or not 0 <= residue < modulus or upper < lower:
        raise ValueError("invalid interval or residue")
    count = ((upper - residue) // modulus
             - (lower - 1 - residue) // modulus)
    length = upper - lower + 1
    error = (_fractional_part((lower - 1 - residue) / modulus)
             - _fractional_part((upper - residue) / modulus))
    return count, error, count - length / modulus


def _squarefree_band(band_left):
    mobius = _mobius_values(2 * band_left)
    divisors = tuple(
        value for value in range(band_left + 1, 2 * band_left + 1)
        if mobius[value])
    return divisors, mobius


def _unweighted_progression_vectors(modulus, shift_length, ell, divisors):
    modes = np.array(_active_modes(modulus, shift_length), dtype=np.int64)
    vectors = np.zeros((len(divisors), len(modes)), dtype=complex)
    for index, divisor in enumerate(divisors):
        first = modulus * ell // divisor + 1
        last = (modulus * (ell + 1) - 1) // divisor
        cofactors = np.arange(first, last + 1, dtype=np.int64)
        positions = divisor * cofactors - modulus * ell
        vectors[index] = np.sum(np.exp(
            -2j * math.pi / modulus
            * modes[:, None] * positions[None, :]), axis=1)
    return modes, vectors


def _single_modulus_matrices(modulus, shift_length, ell, divisors):
    """Return exact discrepancy, frame, and unsigned endpoint matrix."""
    modes, vectors = _unweighted_progression_vectors(
        modulus, shift_length, ell, divisors)
    rho = len(modes) / (modulus - 1)
    exact = (1 - rho) * vectors @ np.conjugate(vectors.T)

    gcd_values = np.gcd.outer(divisors, divisors)
    triangular_by_gcd = {
        gcd_value: float(np.real(sum(
            _triangular_kernel_fejer(modulus, int(gcd_value), int(mode))
            for mode in modes)))
        for gcd_value in np.unique(gcd_values)
    }
    triangular = np.vectorize(triangular_by_gcd.get)(gcd_values)
    products = np.multiply.outer(divisors, divisors)
    lcm_values = products // gcd_values
    main = (1 - rho) * triangular / lcm_values
    discrepancy = exact - main
    discrepancy = (discrepancy + np.conjugate(discrepancy.T)) / 2

    divisor_array = np.array(divisors, dtype=float)
    frame = (rho * modulus ** 2
             * np.array([_totient(a) for a in divisors], dtype=float)
             / divisor_array ** 2)
    unsigned_entry = np.full(
        discrepancy.shape,
        (1 - rho) * 2 * dirichlet_residue_l1_bound(modulus),
        dtype=float)
    return discrepancy, frame, unsigned_entry, rho


def _normalized_receipt(discrepancy, frame, unsigned_entry, coefficients):
    scale = np.sqrt(frame)
    normalized = discrepancy / (scale[:, None] * scale[None, :])
    normalized = (normalized + np.conjugate(normalized.T)) / 2
    eigenvalues = np.linalg.eigvalsh(normalized)
    signed_norm = float(np.max(np.abs(eigenvalues)))
    exact_absolute_schur = float(np.max(np.sum(np.abs(normalized), axis=1)))
    normalized_unsigned = unsigned_entry / (
        scale[:, None] * scale[None, :])
    unsigned_schur = float(np.max(np.sum(normalized_unsigned, axis=1)))
    coefficient_energy = float(np.sum(frame * coefficients ** 2))
    mobius_value = abs(coefficients @ discrepancy @ coefficients)
    return {
        "signed_discrepancy_operator_norm": signed_norm,
        "signed_minimum_eigenvalue": float(eigenvalues[0]),
        "signed_maximum_eigenvalue": float(eigenvalues[-1]),
        "exact_entrywise_absolute_schur": exact_absolute_schur,
        "proved_unsigned_endpoint_schur": unsigned_schur,
        "unsigned_over_signed_operator": (
            unsigned_schur / signed_norm if signed_norm else math.inf),
        "mobius_signed_discrepancy_quotient": float(
            mobius_value / coefficient_energy),
    }


def signed_crt_discrepancy_probe(modulus, shift_length, ell, band_left):
    """Measure (2) for one prime modulus and one squarefree dyadic band."""
    if any(type(value) is not int for value in (
            modulus, shift_length, ell, band_left)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= band_left
            or 2 * band_left >= modulus or ell < 1):
        raise ValueError("require 2<=H<=U, 2U<m, and ell>=1")
    flags = _prime_flags(modulus)
    if not flags[modulus]:
        raise ValueError("modulus must be prime")
    divisors, mobius = _squarefree_band(band_left)
    discrepancy, frame, unsigned, rho = _single_modulus_matrices(
        modulus, shift_length, ell, divisors)
    coefficients = np.array([mobius[a] for a in divisors], dtype=float)
    heuristic = shift_length * band_left ** 2 / modulus
    receipt = _normalized_receipt(
        discrepancy, frame, unsigned, coefficients)
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "rho": rho,
        "ell": ell,
        "divisor_band": (band_left, 2 * band_left),
        "divisor_count": len(divisors),
        "absolute_endpoint_scale_HU2_over_m": heuristic,
        **receipt,
        "signed_operator_over_HU2_over_m": (
            receipt["signed_discrepancy_operator_norm"] / heuristic),
        "signed_discrepancy_bound_proved": False,
        "signed_prime_correlation_proved": False,
    }


def prime_averaged_signed_crt_discrepancy(
        moduli, shift_length, ell, band_left):
    """Test cancellation after summing (2) over specified prime moduli."""
    if not isinstance(moduli, (tuple, list)) or not moduli:
        raise ValueError("moduli must be a nonempty tuple or list")
    if any(type(value) is not int for value in moduli):
        raise ValueError("every modulus must be an integer")
    if any(type(value) is not int for value in (
            shift_length, ell, band_left)):
        raise ValueError("all other arguments must be integers")
    if (not 2 <= shift_length <= band_left or ell < 1
            or 2 * band_left >= min(moduli)):
        raise ValueError("invalid averaged-probe ranges")
    flags = _prime_flags(max(moduli))
    if any(not flags[modulus] for modulus in moduli):
        raise ValueError("every modulus must be prime")

    divisors, mobius = _squarefree_band(band_left)
    total_discrepancy = np.zeros(
        (len(divisors), len(divisors)), dtype=complex)
    total_frame = np.zeros(len(divisors), dtype=float)
    total_unsigned = np.zeros_like(total_discrepancy, dtype=float)
    for modulus in moduli:
        discrepancy, frame, unsigned, _ = _single_modulus_matrices(
            modulus, shift_length, ell, divisors)
        weight = math.log(modulus) ** 2 / modulus
        total_discrepancy += weight * discrepancy
        total_frame += weight * frame
        total_unsigned += weight * unsigned
    coefficients = np.array([mobius[a] for a in divisors], dtype=float)
    receipt = _normalized_receipt(
        total_discrepancy, total_frame, total_unsigned, coefficients)
    return {
        "moduli": tuple(moduli),
        "prime_count": len(moduli),
        "shift_length": shift_length,
        "ell": ell,
        "divisor_band": (band_left, 2 * band_left),
        "divisor_count": len(divisors),
        **receipt,
        "prime_average_cancellation_proved": False,
        "signed_prime_correlation_proved": False,
    }


def row_averaged_signed_crt_discrepancy(
        modulus, shift_length, ell_first, row_count, band_left):
    """Test cancellation after summing the endpoint error over rows."""
    if any(type(value) is not int for value in (
            modulus, shift_length, ell_first, row_count, band_left)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= band_left
            or 2 * band_left >= modulus or ell_first < 1 or row_count < 1):
        raise ValueError("invalid row-average ranges")
    flags = _prime_flags(modulus)
    if not flags[modulus]:
        raise ValueError("modulus must be prime")

    divisors, mobius = _squarefree_band(band_left)
    total_discrepancy = np.zeros(
        (len(divisors), len(divisors)), dtype=complex)
    total_frame = np.zeros(len(divisors), dtype=float)
    total_unsigned = np.zeros_like(total_discrepancy, dtype=float)
    for ell in range(ell_first, ell_first + row_count):
        discrepancy, frame, unsigned, _ = _single_modulus_matrices(
            modulus, shift_length, ell, divisors)
        total_discrepancy += discrepancy
        total_frame += frame
        total_unsigned += unsigned
    coefficients = np.array([mobius[a] for a in divisors], dtype=float)
    receipt = _normalized_receipt(
        total_discrepancy, total_frame, total_unsigned, coefficients)
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "ell_first": ell_first,
        "row_count": row_count,
        "divisor_band": (band_left, 2 * band_left),
        "divisor_count": len(divisors),
        **receipt,
        "row_average_cancellation_proved": False,
        "signed_prime_correlation_proved": False,
    }


def prime_row_averaged_signed_crt_discrepancy(
        moduli, shift_length, ell_first, row_count, band_left):
    """Test the joint prime-modulus and row average of the signed error."""
    if not isinstance(moduli, (tuple, list)) or not moduli:
        raise ValueError("moduli must be a nonempty tuple or list")
    if any(type(value) is not int for value in moduli):
        raise ValueError("every modulus must be an integer")
    if any(type(value) is not int for value in (
            shift_length, ell_first, row_count, band_left)):
        raise ValueError("all other arguments must be integers")
    if (not 2 <= shift_length <= band_left or ell_first < 1
            or row_count < 1 or 2 * band_left >= min(moduli)):
        raise ValueError("invalid joint-average ranges")
    flags = _prime_flags(max(moduli))
    if any(not flags[modulus] for modulus in moduli):
        raise ValueError("every modulus must be prime")

    divisors, mobius = _squarefree_band(band_left)
    total_discrepancy = np.zeros(
        (len(divisors), len(divisors)), dtype=complex)
    total_frame = np.zeros(len(divisors), dtype=float)
    total_unsigned = np.zeros_like(total_discrepancy, dtype=float)
    for modulus in moduli:
        weight = math.log(modulus) ** 2 / modulus
        for ell in range(ell_first, ell_first + row_count):
            discrepancy, frame, unsigned, _ = _single_modulus_matrices(
                modulus, shift_length, ell, divisors)
            total_discrepancy += weight * discrepancy
            total_frame += weight * frame
            total_unsigned += weight * unsigned
    coefficients = np.array([mobius[a] for a in divisors], dtype=float)
    receipt = _normalized_receipt(
        total_discrepancy, total_frame, total_unsigned, coefficients)
    return {
        "moduli": tuple(moduli),
        "prime_count": len(moduli),
        "shift_length": shift_length,
        "ell_first": ell_first,
        "row_count": row_count,
        "divisor_band": (band_left, 2 * band_left),
        "divisor_count": len(divisors),
        **receipt,
        "joint_prime_row_cancellation_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    for arguments in ((1009, 5, 9, 50), (1009, 5, 9, 100),
                      (1009, 5, 9, 200), (10007, 10, 31, 320),
                      (10007, 10, 31, 640), (10007, 10, 31, 1200)):
        print(signed_crt_discrepancy_probe(*arguments))
    print(prime_averaged_signed_crt_discrepancy(
        (1009, 1013, 1019, 1021, 1031), 5, 9, 100))
    print(row_averaged_signed_crt_discrepancy(1009, 5, 9, 16, 100))
