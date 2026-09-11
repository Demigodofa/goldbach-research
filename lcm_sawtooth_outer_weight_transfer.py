"""Transfer a dyadic lifted PSD inequality to the saved outer weights.

Let ``N_m,D_m`` be positive semidefinite matrices and suppose

    sum_m N_m <= C sum_m D_m

in Loewner order.  For positive scalar weights ``w_m``, positivity gives

    sum_m w_m N_m
      <= w_max sum_m N_m
      <= C w_max sum_m D_m
      <= C (w_max / w_min) sum_m w_m D_m.                 (1)

Thus the four outer-prime weights used by the project require no separate
matrix estimate if their distortion on ``[M,2M]`` is bounded.  This module
records exact finite distortions and elementary analytic upper bounds.

For odd prime ``m`` and fixed ``H``, the active set has size ``2 L_m``, where

    L_m = #{s integer: m/(2*pi*H) < s < m/(pi*H)}.

The interval has length ``m/(2*pi*H)``, so ``a-1 <= L_m <= a+1`` for
``a=m/(2*pi*H)``.  This bounds the distortion of
``rho_m=2 L_m/(m-1)`` explicitly.  The result transfers an unweighted
uniform or subpower inequality; it does not prove that input inequality.

For the project choice ``H=floor(M^(10/59))`` and ``M>=17``, put
``x=M/(pi H)``.  If ``M<60`` then ``H=1``; if ``M>=60`` then
``x>=M^(49/59)/pi``.  Hence always ``x>=17/pi>5``.  The rho-distortion bound
below is at most

    (2 + 1/16) * (2 + 6/(17/pi - 2)) < 8.

Also ``log(2M)/log(M) <= log(34)/log(17)``.  Consequently the four weight
distortions are bounded uniformly by ``1,2,16,25``.
"""

import math

from mobius_covariance_endpoint_probe import _prime_flags
from near_cutoff_geometric_bound import _active_modes


WEIGHT_MODES = (
    "unweighted",
    "log_squared_over_m",
    "rho_log_squared_over_m",
    "rho_m_log_squared",
)

UNIFORM_PROJECT_DISTORTION_BOUND = {
    "unweighted": 1.0,
    "log_squared_over_m": 2.0,
    "rho_log_squared_over_m": 16.0,
    "rho_m_log_squared": 25.0,
}


def _active_mode_count_formula(modulus, shift_length):
    """Count the symmetric strict active interval for an odd modulus."""
    if modulus % 2 != 1 or shift_length < 1:
        raise ValueError("require an odd modulus and positive shift length")
    lower = modulus / (2 * math.pi * shift_length)
    positive_half = max(
        0, math.ceil(2 * lower) - math.floor(lower) - 1)
    return 2 * positive_half


def project_outer_weights(scale_modulus, modulus):
    """Return the four established positive weights for one project block."""
    if (type(scale_modulus) is not int or scale_modulus < 17
            or type(modulus) is not int
            or not scale_modulus <= modulus <= 2 * scale_modulus):
        raise ValueError("require integer M>=17 and M<=m<=2M")
    inferred_N = scale_modulus ** (1 / .59)
    shift_length = int(inferred_N ** .1)
    active_size = len(_active_modes(modulus, shift_length))
    if (modulus % 2 == 1
            and active_size != _active_mode_count_formula(
                modulus, shift_length)):
        raise ArithmeticError("active-mode count formula disagrees")
    rho = active_size / (modulus - 1)
    logarithmic_weight = math.log(modulus) ** 2 / modulus
    return {
        "unweighted": 1.0,
        "log_squared_over_m": logarithmic_weight,
        "rho_log_squared_over_m": rho * logarithmic_weight,
        "rho_m_log_squared": (
            rho * modulus * math.log(modulus) ** 2),
    }


def dyadic_outer_weight_distortion_receipt(scale_modulus):
    """Give exact prime-block distortions and proved dyadic upper bounds."""
    if type(scale_modulus) is not int or scale_modulus < 17:
        raise ValueError("scale_modulus must be an integer at least 17")
    inferred_N = scale_modulus ** (1 / .59)
    shift_length = int(inferred_N ** .1)
    if scale_modulus / (math.pi * shift_length) <= 2:
        raise ValueError("active interval is too short for the positive bound")
    flags = _prime_flags(2 * scale_modulus)
    primes = tuple(
        modulus for modulus in range(scale_modulus, 2 * scale_modulus + 1)
        if flags[modulus])
    if not primes:
        raise ArithmeticError("prime block is empty")
    weight_rows = tuple(
        project_outer_weights(scale_modulus, modulus)
        for modulus in primes)
    exact = {
        mode: (max(row[mode] for row in weight_rows)
               / min(row[mode] for row in weight_rows))
        for mode in WEIGHT_MODES
    }

    M = scale_modulus
    H = shift_length
    logarithm_ratio = math.log(2 * M) / math.log(M)
    rho_upper = (2 * M / (math.pi * H) + 2) / (M - 1)
    rho_lower = (M / (math.pi * H) - 2) / (2 * M - 1)
    rho_distortion = rho_upper / rho_lower
    analytic = {
        "unweighted": 1.0,
        "log_squared_over_m": 2 / logarithm_ratio ** 2,
        "rho_log_squared_over_m": (
            rho_distortion * 2 / logarithm_ratio ** 2),
        "rho_m_log_squared": (
            rho_distortion * 2 * logarithm_ratio ** 2),
    }
    return {
        "scale_modulus": M,
        "shift_length": H,
        "prime_count": len(primes),
        "exact_prime_block_distortion": exact,
        "analytic_dyadic_distortion_bound": analytic,
        "uniform_project_distortion_bound": dict(
            UNIFORM_PROJECT_DISTORTION_BOUND),
        "rho_dyadic_distortion_bound": rho_distortion,
        "positive_weight_transfer_identity_proved": True,
        "unweighted_lifted_inequality_proved": False,
        "signed_prime_correlation_estimate_proved": False,
    }


if __name__ == "__main__":
    print(dyadic_outer_weight_distortion_receipt(127))
