"""Sum the shifted near-cutoff pair theorem over one dyadic lag block.

Fix one prime m and one squarefree divisor band D_U.  For coefficient vectors
c_l on each complete row, let E_l be their exact full-frequency energy and

 B_(l,r)=(1-rho)sum_(h in I)Phi_l(h)conj(Phi_r(h)).      (1)

The shifted-pair theorem gives, uniformly in l,r,

 |B_(l,r)| <= eta*rho*sqrt(F_l(c_l)F_r(c_r)).           (2)

If every exact full Gram satisfies G_l>=kappa F_l, then

 |B_(l,r)| <= eta*rho/kappa*sqrt(E_l E_r).              (3)

For any lag set J define

 D_J=2 Re sum_(Delta in J,l) B_(l,l+Delta),
 P_J=2 rho sum_(Delta in J,l) sqrt(E_l E_(l+Delta)).     (4)

Termwise summation of (3) proves

 |D_J| <= (eta/kappa)P_J.                               (5)

Thus neither the number of rows nor the size of the lag block is lost.  At
the project exponents eta<<_eps N^eps and kappa>=1/2 eventually.  This closes
the dyadic active-lag bookkeeping for one near-cutoff divisor band.  It does
not combine different divisor bands or handle d>1.
"""

import math

import numpy as np

from divisor_active_full_gram import _full_collision_gram
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from mobius_cross_divisor_gram import _progression_vectors
from near_cutoff_full_frame_bound import row_lower_frame_bound
from near_cutoff_geometric_bound import _active_modes
from shifted_active_frame_bound import row_shifted_active_frame_bound


def dyadic_lag_band_receipt(modulus, shift_length, cofactor_left,
                            divisor_left, lag_first, lag_stop):
    """Return exact finite values and the rigorous implication (5)."""
    if any(type(value) is not int for value in (
            modulus, shift_length, cofactor_left, divisor_left,
            lag_first, lag_stop)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= divisor_left
            or 2 * divisor_left >= modulus
            or cofactor_left < 2
            or not 1 <= lag_first < lag_stop <= cofactor_left):
        raise ValueError("invalid dyadic lag ranges")
    flags = _prime_flags(modulus)
    if not flags[modulus]:
        raise ValueError("modulus must be prime")

    mobius = _mobius_values(2 * divisor_left)
    divisors = tuple(a for a in range(divisor_left + 1, 2 * divisor_left + 1)
                     if mobius[a])
    coefficients = np.array([mobius[a] for a in divisors], dtype=float)
    modes = _active_modes(modulus, shift_length)
    rho = len(modes) / (modulus - 1)
    rows = tuple(range(cofactor_left, 2 * cofactor_left))
    vectors = {}
    energies = {}
    lower_coefficients = []
    for ell in rows:
        _, vectors[ell] = _progression_vectors(
            modulus, shift_length, ell, divisors)
        full = _full_collision_gram(modulus, ell, divisors)
        energies[ell] = float(coefficients @ full @ coefficients)
        lower_coefficients.append(
            row_lower_frame_bound(modulus, ell, divisor_left)[
                "proved_frame_coefficient"])
    kappa = min(lower_coefficients)
    if kappa <= 0:
        raise ValueError("the explicit full-frame coefficient must be positive")

    pair_bounds = []
    active_sum = 0j
    energy_sum = 0.0
    pair_count = 0
    for delta in range(lag_first, lag_stop):
        for ell_left in range(cofactor_left, 2 * cofactor_left - delta):
            ell_right = ell_left + delta
            pair_count += 1
            pair_bounds.append(row_shifted_active_frame_bound(
                modulus, shift_length, ell_left, ell_right, divisor_left)[
                    "proved_shifted_active_frame_operator_bound"])
            left_value = coefficients @ vectors[ell_left]
            right_value = coefficients @ vectors[ell_right]
            active_sum += ((1 - rho) * left_value
                           @ np.conjugate(right_value))
            energy_sum += math.sqrt(
                energies[ell_left] * energies[ell_right])
    eta = max(pair_bounds)
    active_covariance = 2 * float(np.real(active_sum))
    principal_budget = 2 * rho * energy_sum
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "rho": rho,
        "cofactor_range": (cofactor_left, 2 * cofactor_left - 1),
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisor_count": len(divisors),
        "lag_range": (lag_first, lag_stop - 1),
        "pair_count": pair_count,
        "exact_signed_active_covariance": active_covariance,
        "principal_full_energy_budget": principal_budget,
        "exact_signed_active_over_budget": (
            active_covariance / principal_budget),
        "uniform_pair_frame_bound": eta,
        "uniform_full_frame_coefficient": kappa,
        "proved_absolute_active_over_budget": eta / kappa,
        "dyadic_lag_bookkeeping_proved": True,
        "cross_divisor_bands_proved": False,
        "d_greater_than_one_proved": False,
    }


if __name__ == "__main__":
    for key, value in dyadic_lag_band_receipt(
            1009, 5, 9, 8, 1, 2).items():
        print(f"{key}: {value}")
