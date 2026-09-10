"""A joint prime-row bound for the signed CRT endpoint error.

This file turns the exact row-period identity in
``row_periodic_crt_cancellation.py`` into a uniform incomplete-average bound.
For ``q=lcm(a,b)`` the count error, as a function of the base row ``ell``,
has no constant Fourier coefficient and has the form

    E_m(ell)=sum_(1<=k<q) c_(m,k)e_q(-k*m*ell),
    |c_(m,k)| <= 1/(2*min(k,q-k)).                       (1)

For a row interval of length ``A`` put
``S_k(t)=sum_ell e_q(k*t*ell)`` and ``Q=q/gcd(k,q)``.  Over a complete
``Q``-period in ``t``, orthogonality gives exactly

    sum_(t mod Q)|S_k(t)|^2
      = Q*#{(ell,r): ell==r (mod Q)}
      <= A^2+Q*A.                                       (2)

Consequently, for any interval of ``M`` candidate moduli and any subset of
``P`` primes in it, Cauchy gives

    sum_(m prime)|S_k(m)|
      <= sqrt(P*ceil(M/Q)*(A^2+Q*A)).                   (3)

Assume ``A<=M``, as at the project scales.  Summing (3) with (1), and
grouping by ``Q|q``, first yields an additional ``M^(-1/2)`` term from the
incomplete final multiplier period.  It is dominated by ``A^(-1/2)`` under
this assumption, leaving, up to subpower factors,

    (P*A)^(-1) sum_(m prime) |sum_ell E_m(ell)|
      << N^eps{A^(-1/2)+sqrt(q/(M*A))+q^(-1/2)},        (4)

using ``P >> M/log M``.  Smooth row logarithms are handled by Abel summation;
their endpoint and total-variation costs are logarithmic.  The complete
active kernel has signed-residue L1 norm ``O(M log M)``, uniformly in ``m``.

If ``a`` and ``b`` lie in bands of scales ``U`` and ``W``, respectively, then
``max(U,W)<q<=4UW``.  Applying rectangular Schur band by band and maximizing
over ``U,W<=B`` therefore gives the aggregate signed endpoint operator

    ||D_endpoint||_F << N^eps * (H*B^2/M)
       {A^(-1/2)+B/sqrt(M*A)+B^(-1/2)}.                 (5)

The argument is uniform for a fixed shifted-row lag: changing both row
indices together still rotates the compatible CRT residue by ``-m``.
It controls a common divisor coefficient vector across the row and prime
sum, which includes the actual Mobius vector; it does not assert the stronger
inequality for independently chosen coefficients on every row.

At ``H=N^.1, M=N^.59, A=N^.41, B=N^beta``, the three exponents in (5) are

    2*beta-.695,  3*beta-.99,  1.5*beta-.49.            (6)

Thus the signed endpoint is power-small for ``beta<49/150``.  The already
proved exact-full-frame perturbation ``B^2/M+B/A`` is stricter and permits
assembly of the lower union only for ``beta<.295``.  Hence the combined
current route extends the lower-band endpoint from ``.245`` to
``.295-delta`` for every fixed ``delta>0``.  This remains a divisor-frame
component, not the missing signed prime-correlation estimate.
"""

import cmath
import math


def row_geometric_sum(period, frequency, multiplier,
                      row_first, row_count):
    """Return S_k(multiplier) directly."""
    if any(type(value) is not int for value in (
            period, frequency, multiplier, row_first, row_count)):
        raise ValueError("all arguments must be integers")
    if (period < 2 or not 1 <= frequency < period
            or row_first < 0 or row_count < 1):
        raise ValueError("invalid geometric-sum ranges")
    return sum(cmath.exp(
        2j * math.pi * frequency * multiplier * ell / period)
        for ell in range(row_first, row_first + row_count))


def exact_rotation_second_moment(period, frequency,
                                 row_first, row_count):
    """Evaluate the left side of (2) over one minimal multiplier period."""
    if any(type(value) is not int for value in (
            period, frequency, row_first, row_count)):
        raise ValueError("all arguments must be integers")
    if (period < 2 or not 1 <= frequency < period
            or row_first < 0 or row_count < 1):
        raise ValueError("invalid second-moment ranges")
    rotation_period = period // math.gcd(period, frequency)
    value = sum(abs(row_geometric_sum(
        period, frequency, multiplier, row_first, row_count)) ** 2
        for multiplier in range(rotation_period))
    collision_count = sum(
        (left - right) % rotation_period == 0
        for left in range(row_first, row_first + row_count)
        for right in range(row_first, row_first + row_count))
    return {
        "period": period,
        "frequency": frequency,
        "rotation_period": rotation_period,
        "row_count": row_count,
        "exact_second_moment": float(value),
        "orthogonality_value": rotation_period * collision_count,
        "upper_bound": row_count ** 2 + rotation_period * row_count,
        "complete_rotation_second_moment_proved": True,
    }


def incomplete_rotation_second_moment_bound(
        period, frequency, modulus_count, row_count):
    """Return the rigorous all-integer second-moment bound used in (3)."""
    if any(type(value) is not int for value in (
            period, frequency, modulus_count, row_count)):
        raise ValueError("all arguments must be integers")
    if (period < 2 or not 1 <= frequency < period
            or modulus_count < 1 or row_count < 1):
        raise ValueError("invalid incomplete-moment ranges")
    rotation_period = period // math.gcd(period, frequency)
    period_bound = row_count ** 2 + rotation_period * row_count
    return math.ceil(modulus_count / rotation_period) * period_bound


def endpoint_fourier_coefficient_bound(period, frequency):
    """Return the interval Fourier-coefficient majorant in (1)."""
    if any(type(value) is not int for value in (period, frequency)):
        raise ValueError("period and frequency must be integers")
    if period < 2 or not 1 <= frequency < period:
        raise ValueError("require 1<=frequency<period")
    return 1 / (2 * min(frequency, period - frequency))


def joint_prime_row_phase_envelope(
        period, modulus_count, row_count, prime_count):
    """Return the explicit right side of (3), summed over (1)."""
    if any(type(value) is not int for value in (
            period, modulus_count, row_count, prime_count)):
        raise ValueError("all arguments must be integers")
    if (period < 2 or modulus_count < 1 or row_count < 1
            or not 1 <= prime_count <= modulus_count):
        raise ValueError("invalid joint-envelope ranges")
    envelope = sum(
        endpoint_fourier_coefficient_bound(period, frequency)
        * math.sqrt(prime_count * incomplete_rotation_second_moment_bound(
            period, frequency, modulus_count, row_count))
        for frequency in range(1, period))
    return {
        "period": period,
        "modulus_count": modulus_count,
        "row_count": row_count,
        "prime_count": prime_count,
        "proved_fourier_cauchy_envelope": envelope,
        "normalized_joint_average_envelope": (
            envelope / (prime_count * row_count)),
        "joint_prime_row_phase_bound_proved": True,
    }


def project_endpoint_exponent_budget(divisor_exponent):
    """Evaluate (6) and the existing frame barrier at a proposed beta."""
    if (isinstance(divisor_exponent, bool)
            or not isinstance(divisor_exponent, (int, float))
            or not 0 < divisor_exponent < .5):
        raise ValueError("divisor_exponent must lie in (0,.5)")
    beta = float(divisor_exponent)
    endpoint_terms = (
        2 * beta - .695,
        3 * beta - .99,
        1.5 * beta - .49,
    )
    frame_terms = (2 * beta - .59, beta - .41)
    return {
        "divisor_exponent": beta,
        "absolute_single_row_endpoint_exponent": 2 * beta - .49,
        "joint_endpoint_term_exponents": endpoint_terms,
        "joint_endpoint_worst_exponent": max(endpoint_terms),
        "joint_endpoint_power_saving": max(endpoint_terms) < 0,
        "exact_full_frame_perturbation_exponents": frame_terms,
        "exact_full_frame_power_saving": max(frame_terms) < 0,
        "assembled_lower_union_supported": (
            max(endpoint_terms) < 0 and max(frame_terms) < 0),
        "strict_assembled_threshold": .295,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    for beta in (.245, .27, .294, .295, .31, 49 / 150):
        print(project_endpoint_exponent_budget(beta))
    print(joint_prime_row_phase_envelope(143, 200, 80, 31))
