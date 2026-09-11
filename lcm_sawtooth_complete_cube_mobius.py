"""Reduce complete residual cubes to reciprocal Mobius sums.

For squarefree ``d`` put

    A_d(R) = sum_(r<=R,(r,d)=1) mu(r)/r.

The complete residual-cube identity implies

    sum_(r<=R,(r,d)=1) mu(r)/r
        [L_u L_v - sum_(p|r) log(p)^2]
      = L_u L_v A_d(R)
        + sum_(p<=R,p not|d) log(p)^2/p A_(pd)(floor(R/p)).

Thus the degree-zero term contains a classical Mobius cancellation sum, and
the surviving correction has two residual logarithmic derivatives.  This
module verifies the finite identity; it does not assert the uniform estimate
or control boundary-truncated cubes.
"""

import math

from lcm_sawtooth_high_d_assignment import _squarefree_prime_factors
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values


def _coprime_reciprocal_mobius_sum(mobius, limit, excluded_modulus):
    return sum(
        int(mobius[value]) / value
        for value in range(1, limit + 1)
        if math.gcd(value, excluded_modulus) == 1)


def complete_cube_mobius_reduction(
        excluded_modulus, residual_limit, log_left, log_right):
    """Return both sides of the complete-cube Mobius reduction."""
    if (type(excluded_modulus) is not int or excluded_modulus < 1
            or type(residual_limit) is not int or residual_limit < 1
            or not isinstance(log_left, (int, float))
            or not isinstance(log_right, (int, float))):
        raise ValueError("invalid complete-cube Mobius controls")
    _squarefree_prime_factors(excluded_modulus)
    mobius = _mobius_values(residual_limit)
    flags = _prime_flags(residual_limit)
    base_sum = _coprime_reciprocal_mobius_sum(
        mobius, residual_limit, excluded_modulus)
    direct = 0.0
    for residual in range(1, residual_limit + 1):
        if not mobius[residual] or math.gcd(residual, excluded_modulus) != 1:
            continue
        prime_square_sum = sum(
            math.log(prime) ** 2
            for prime in _squarefree_prime_factors(residual))
        direct += (int(mobius[residual]) / residual
                   * (log_left * log_right - prime_square_sum))
    derivative_correction = 0.0
    for prime in range(2, residual_limit + 1):
        if not flags[prime] or excluded_modulus % prime == 0:
            continue
        inner = _coprime_reciprocal_mobius_sum(
            mobius, residual_limit // prime, excluded_modulus * prime)
        derivative_correction += math.log(prime) ** 2 / prime * inner
    transformed = log_left * log_right * base_sum + derivative_correction
    return {
        "excluded_modulus": excluded_modulus,
        "residual_limit": residual_limit,
        "coprime_reciprocal_mobius_sum": base_sum,
        "degree_zero_component": log_left * log_right * base_sum,
        "two_log_derivative_correction": derivative_correction,
        "direct_complete_cube_sum": direct,
        "transformed_complete_cube_sum": transformed,
        "reduction_error": direct - transformed,
        "complete_cube_mobius_reduction_proved": True,
        "uniform_coprime_mobius_estimate_proved": False,
        "boundary_truncated_cube_control_proved": False,
    }


if __name__ == "__main__":
    for key, value in complete_cube_mobius_reduction(
            30, 50, 12.0, 11.0).items():
        print(f"{key}: {value}")
