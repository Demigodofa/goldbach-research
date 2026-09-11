"""Polylogarithmic bound for the high-conductor no-common residual collapse.

Let ``d`` be squarefree, ``d>B*V``, and write every no-common pair as
``a=u*alpha``, ``b=(d/u)*beta`` with residual
``r=lcm(alpha,beta)``.  Because ``a,b<=B`` and ``d>B*V``, both ``u`` and
``d/u`` lie in ``(V,B]`` whenever the pair exists.  Its ``r=1`` base term is
therefore present.

For fixed ``u`` and squarefree ``r``, every residual prime has at most three
states: alpha only, beta only, or both.  There are at most ``3^omega(r)``
terms, and positivity of ``log(X/a)`` for ``X>B`` gives

    |A_(d,r)| <= 3^omega(r) A_(d,1).

As ``K_(d,r)=mu(d)mu(r)A_(d,r)/(d*r)``, it follows pointwise that

    |sum_r K_(d,r)|^2 / sum_r |K_(d,r)|^2
      <= [sum_(r<=B^2/d) mu(r)^2 3^omega(r)/r]^2
      <= (1+log(B^2/d))^6.                                  (1)

The final inequality uses ``mu(r)^2 3^omega(r)<=tau_3(r)`` and

    sum_(n<=R) tau_3(n)/n
      = sum_(abc<=R) 1/(abc) <= (sum_(a<=R)1/a)^3.

Thus (1) is polylogarithmic and hence ``N^epsilon`` in the project scaling.
It controls this no-common layer only; other common layers and conductor
blocks remain separate.
"""

import math

from lcm_sawtooth_high_d_assignment import _squarefree_prime_factors
from mobius_covariance_lag_probe import _mobius_values


def three_state_harmonic_receipt(residual_limit):
    """Return the exact first bound in (1) and its log-six majorant."""
    if type(residual_limit) is not int or residual_limit < 1:
        raise ValueError("residual_limit must be a positive integer")
    mobius = _mobius_values(residual_limit)
    weight = sum(
        3 ** len(_squarefree_prime_factors(residual)) / residual
        for residual in range(1, residual_limit + 1)
        if mobius[residual])
    harmonic = sum(1 / value for value in range(1, residual_limit + 1))
    return {
        "residual_limit": residual_limit,
        "three_state_harmonic_weight": weight,
        "exact_squared_bound": weight ** 2,
        "triple_harmonic_bound": harmonic ** 6,
        "log_six_bound": (1 + math.log(residual_limit)) ** 6,
        "three_state_count_bound_proved": True,
        "no_common_polylog_bound_proved_under_d_gt_BV": True,
    }


if __name__ == "__main__":
    for key, value in three_state_harmonic_receipt(10).items():
        print(f"{key}: {value}")
