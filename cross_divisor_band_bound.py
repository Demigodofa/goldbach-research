"""A rectangular active-frame bound for two divisor scales.

Let squarefree a lie in (U,2U] and b in (W,2W], with
H<=U<=W.  Let both complete-row indices be comparable to a row scale A, as
they are in the project range A<=l_L,l_R<2A, and assume the central ranges
make log(ml_L/a) and log(ml_R/b) comparable to log N.  The shifted
triangular, CRT-discrepancy, and centering entry majorants from
``shifted_active_frame_bound.py`` remain valid.  Rectangular Schur is crucial:

* the triangular gcd row sum is O_eps(sqrt(W/U)N^eps), while its column sum
  is O_eps(sqrt(U/W)N^eps); their geometric mean loses no scale ratio;
* the count-error matrix contributes O_eps(H U W log(m)/m);
* logarithmic CRT variation contributes O_eps(H log(m)/A);
* centering contributes O_eps(H max(U,W)log(m)/m+1/m).

Consequently the cross-band active operator is O_eps(N^eps) whenever the
displayed polynomial losses are o(1).  In particular, with H=N^.1 and
m=N^.59, A=N^.41, every pair of bands satisfying
H<=U,W<=N^(.245-delta) is controlled for fixed delta>0.  This does not yet
assemble all such bands or address larger factors.
"""

import math

import numpy as np

from cross_divisor_band_probe import cross_divisor_band_probe
from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from near_cutoff_geometric_bound import _active_modes
from shifted_active_frame_bound import _entry_majorants


def row_cross_divisor_band_bound(modulus, shift_length,
                                 ell_left, ell_right,
                                 band_left, band_right,
                                 compare_exact=False):
    """Return the rigorous rectangular Schur certificate for two bands."""
    if any(type(value) is not int for value in (
            modulus, shift_length, ell_left, ell_right,
            band_left, band_right)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= min(band_left, band_right)
            or 2 * max(band_left, band_right) >= modulus
            or ell_left < 1 or ell_right < 1
            or modulus < 16 * math.pi * shift_length):
        raise ValueError("invalid cross-band theorem ranges")
    flags = _prime_flags(modulus)
    if not flags[modulus]:
        raise ValueError("modulus must be prime")

    mobius = _mobius_values(2 * max(band_left, band_right))
    left_divisors = tuple(
        a for a in range(band_left + 1, 2 * band_left + 1) if mobius[a])
    right_divisors = tuple(
        a for a in range(band_right + 1, 2 * band_right + 1) if mobius[a])
    modes = _active_modes(modulus, shift_length)
    rho = len(modes) / (modulus - 1)
    left_logs = {
        a: math.log(modulus * ell_left / a) for a in left_divisors}
    right_logs = {
        b: math.log(modulus * ell_right / b) for b in right_divisors}
    left_phi = {a: _totient(a) for a in left_divisors}
    right_phi = {b: _totient(b) for b in right_divisors}
    components = [np.empty((len(left_divisors), len(right_divisors)))
                  for _ in range(3)]
    for left_index, left in enumerate(left_divisors):
        for right_index, right in enumerate(right_divisors):
            values = _entry_majorants(
                modulus, rho, len(modes), ell_left, ell_right,
                left, right, left_logs[left], right_logs[right],
                left_phi[left], right_phi[right], shift_length)
            for matrix, value in zip(components, values):
                matrix[left_index, right_index] = value
    total = sum(components)

    def rectangular_schur(matrix):
        maximum_row = float(np.max(np.sum(matrix, axis=1)))
        maximum_column = float(np.max(np.sum(matrix, axis=0)))
        return math.sqrt(maximum_row * maximum_column)

    component_bounds = tuple(rectangular_schur(matrix)
                             for matrix in components)
    total_bound = rectangular_schur(total)
    result = {
        "modulus": modulus,
        "shift_length": shift_length,
        "rho": rho,
        "ell_left": ell_left,
        "ell_right": ell_right,
        "left_band": (band_left, 2 * band_left),
        "right_band": (band_right, 2 * band_right),
        "left_divisor_count": len(left_divisors),
        "right_divisor_count": len(right_divisors),
        "triangular_rectangular_schur_bound": component_bounds[0],
        "discrepancy_rectangular_schur_bound": component_bounds[1],
        "centering_rectangular_schur_bound": component_bounds[2],
        "proved_cross_band_active_frame_operator_bound": total_bound,
        "cross_band_active_frame_bound_proved": True,
        "all_lower_bands_assembled": False,
        "larger_factor_bands_proved": False,
    }
    if compare_exact:
        exact = cross_divisor_band_probe(
            modulus, shift_length, ell_left, ell_right,
            band_left, band_right)
        actual = exact["largest_cross_band_singular_value"]
        result["exact_cross_band_operator_norm"] = actual
        result["proved_over_exact"] = total_bound / actual
    return result


if __name__ == "__main__":
    for key, value in row_cross_divisor_band_bound(
            1009, 5, 9, 12, 8, 16, compare_exact=True).items():
        print(f"{key}: {value}")
