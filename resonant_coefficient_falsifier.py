"""Attack the active/totient-frame inequality with resonant coefficients.

For one prime modulus and a consecutive block of complete rows, this module
forms the exact active Gram A and diagonal totient frame F used in
``active_totient_frame_probe.py``.  It then tests two adversarial choices:

* the generalized eigenvector, which is the strongest possible complex
  coefficient vector for the finite matrices; and
* a single-mode phase lock, chosen to maximize one exact (ell,h) sample under
  the same F norm and then scored against the complete active sum.

The coefficients c are normalized by sum_a F_a |c_a|^2=1.  The dimensionless
entries z_a=sqrt(F_a)c_a are also returned, so every tested vector can be
reconstructed without hiding the scale in F.  This is a falsifier, not an
asymptotic proof.
"""

import math

import numpy as np

from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from mobius_cross_divisor_gram import _progression_vectors
from near_cutoff_geometric_bound import _active_modes


def _quadratic(active, coefficients):
    """Energy of sum_a c_a u_a for the Gram convention in the project."""
    return float(np.real(
        coefficients @ active @ np.conjugate(coefficients)))


def _fix_global_phase(coefficients):
    pivot = int(np.argmax(np.abs(coefficients)))
    phase = np.exp(-1j * np.angle(coefficients[pivot]))
    return coefficients * phase


def _flat_phase_resonance(normalized):
    """Coordinate-ascent attack with equal F-normalized magnitudes."""
    size = len(normalized)
    indices = np.arange(size)
    starts = [np.ones(size, dtype=complex),
              ((-1.0) ** indices).astype(complex)]
    starts.extend(np.exp(2j * math.pi * frequency * indices / size)
                  for frequency in range(1, min(9, size)))
    generator = np.random.default_rng(20260910)
    starts.extend(np.exp(2j * math.pi * generator.random(size))
                  for _ in range(8))
    best = None
    for start in starts:
        vector = start / math.sqrt(size)
        for _ in range(100):
            previous = vector.copy()
            for index in range(size):
                residual = (normalized[index] @ vector
                            - normalized[index, index] * vector[index])
                if abs(residual):
                    vector[index] = residual / abs(residual) / math.sqrt(size)
            if np.linalg.norm(vector - previous) < 1e-12:
                break
        quotient = float(np.real(np.conjugate(vector) @ normalized @ vector))
        if best is None or quotient > best[0]:
            best = (quotient, vector.copy())
    return best


def single_modulus_resonant_falsifier(modulus, shift_length, ell_first,
                                       row_count, divisor_left):
    """Return exact worst-vector and single-mode resonance receipts."""
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
    modes = tuple(_active_modes(modulus, shift_length))
    rho = len(modes) / (modulus - 1)
    active = np.zeros((len(divisors), len(divisors)), dtype=complex)
    frame = np.zeros(len(divisors))
    samples = []

    for ell in range(ell_first, ell_first + row_count):
        returned_modes, vectors = _progression_vectors(
            modulus, shift_length, ell, divisors)
        active += (1 - rho) * vectors @ np.conjugate(vectors.T)
        logs = np.log(modulus * ell / divisor_array)
        frame += rho * modulus ** 2 * logs ** 2 * (
            totients / divisor_array ** 2)
        samples.extend((ell, int(mode), vectors[:, index].copy())
                       for index, mode in enumerate(returned_modes))

    active = (active + np.conjugate(active.T)) / 2
    root = np.sqrt(frame)
    normalized = active / (root[:, None] * root[None, :])
    normalized = (normalized + np.conjugate(normalized.T)) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(normalized)

    # If d is the top eigenvector of F^-1/2 A F^-1/2, then c=conj(d)/sqrt(F)
    # maximizes c^T A conj(c), the energy convention for sum_a c_a u_a.
    whitened = np.conjugate(eigenvectors[:, -1])
    coefficients = _fix_global_phase(whitened / root)
    whitened = coefficients * root
    eigen_quotient = _quadratic(active, coefficients)

    flat_quotient, flat_whitened_eigen_convention = _flat_phase_resonance(
        normalized)
    flat_coefficients = _fix_global_phase(
        np.conjugate(flat_whitened_eigen_convention) / root)
    flat_whitened = flat_coefficients * root
    flat_quotient = _quadratic(active, flat_coefficients)

    best_locked = None
    for ell, mode, sample in samples:
        candidate = np.conjugate(sample) / frame
        norm = math.sqrt(float(np.sum(frame * np.abs(candidate) ** 2)))
        if norm == 0:
            continue
        candidate = _fix_global_phase(candidate / norm)
        quotient = _quadratic(active, candidate)
        if best_locked is None or quotient > best_locked[0]:
            best_locked = (quotient, ell, mode, candidate)

    mu = np.array([mobius[a] for a in divisors], dtype=complex)
    mu /= math.sqrt(float(np.sum(frame * np.abs(mu) ** 2)))
    mobius_quotient = _quadratic(active, mu)
    locked_quotient, locked_ell, locked_mode, locked_coefficients = best_locked

    def packed(values):
        return tuple((a, float(np.real(value)), float(np.imag(value)))
                     for a, value in zip(divisors, values))

    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "rho": rho,
        "ell_range": (ell_first, ell_first + row_count - 1),
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisor_count": len(divisors),
        "frame_norm_of_resonant_coefficients": float(
            np.sum(frame * np.abs(coefficients) ** 2)),
        "optimal_resonant_quotient": eigen_quotient,
        "eigensolver_quotient": float(eigenvalues[-1]),
        "optimal_over_H": eigen_quotient / shift_length,
        "optimal_over_divisor_count": eigen_quotient / len(divisors),
        "resonant_coefficients": packed(coefficients),
        "resonant_whitened_coefficients": packed(whitened),
        "flat_frame_phase_resonant_quotient": flat_quotient,
        "flat_frame_phase_coefficients": packed(flat_coefficients),
        "flat_frame_phase_whitened_coefficients": packed(flat_whitened),
        "best_single_mode_locked_quotient": locked_quotient,
        "best_single_mode_ell": locked_ell,
        "best_single_mode_h": locked_mode,
        "single_mode_locked_coefficients": packed(locked_coefficients),
        "mobius_quotient": mobius_quotient,
        "inequality_falsified_at_constant_one": eigen_quotient > 1,
        "H_or_band_size_growth_seen": (
            eigen_quotient >= min(shift_length, len(divisors))),
        "uniform_asymptotic_inequality_proved": False,
    }


if __name__ == "__main__":
    for key, value in single_modulus_resonant_falsifier(
            1009, 5, 9, 8, 8).items():
        print(f"{key}: {value}")
