"""A deterministic lower frame bound for the near-cutoff full divisor Gram.

Let x=m*l, D_U={U<a<=2U:mu(a)^2=1}, L_a=log(x/a), and let G be the exact
full-frequency collision Gram from ``divisor_active_full_gram.py``.  Put

 F_aa=m^2 L_a^2 phi(a)/a^2.                              (1)

The frozen uniform-divisibility Gram P0 satisfies P0>=F by the positive gcd
feature decomposition in ``divisor_full_frame_probe.py``.  This module gives
an explicit entrywise bound R_(a,b) for E=G-P0.  Therefore

 eta=max_a sum_b R_(a,b)/sqrt(F_aa F_bb),
 G >= (1-eta)F.                                          (2)

The proof of the entry bound is elementary.  In x<n<x+m, put
C_q=#{n:q|n}.  Then |C_q-m/q|<2.  Also

 0<log(n/a)-L_a=log(n/x)<1/l.

Consequently, with q=lcm(a,b),

 |sum_(q|n)log(n/a)log(n/b)-m L_a L_b/q|
 <=2 L_a L_b+(L_a+L_b)(m/q+2)/l+(m/q+2)/l^2.            (3)

Writing alpha_a=m L_a/a and
Delta_a=2 L_a+(m/a+2)/l gives

 |S_a-alpha_a|<=Delta_a,

and the centering error is at most

 alpha_a alpha_b/(m-1)
 +m/(m-1)(alpha_a Delta_b+alpha_b Delta_a+Delta_a Delta_b). (4)

Multiplying (3) by m and adding (4) is R_(a,b).  Equations
(1)--(4) prove (2) with no numerical assumption.

For the project's near-cutoff choice U=floor(N^.15), m asymp N^.59 and
l asymp N^.41.  The standard phi(a)>=C_eps*a^(1-eps) bound and the explicit
formula give

 eta <<_eps U^(2+eps)/m + U^(1+eps)/l
      <<_eps N^(-.29+eps)+N^(-.26+eps)=o(1).             (5)

Thus G>=F/2 for every such complete row once N is sufficiently large.  This
is only a full-frequency denominator theorem.  It does not bound the active
cross-divisor numerator or any shifted-row covariance.
"""

import math

import numpy as np

from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values


def entry_error_bound(modulus, ell, left, right):
    """Return the explicit R_(a,b) from (3)--(4)."""
    if any(type(value) is not int for value in (
            modulus, ell, left, right)):
        raise ValueError("all arguments must be integers")
    if not 2 <= left < modulus or not 2 <= right < modulus or ell < 1:
        raise ValueError("require 2<=a,b<m and ell>=1")
    x = modulus * ell
    left_log = math.log(x / left)
    right_log = math.log(x / right)
    if left_log <= 0 or right_log <= 0:
        raise ValueError("the frozen logarithms must be positive")
    common = math.lcm(left, right)
    count_upper = modulus / common + 2
    collision_error = (
        2 * left_log * right_log
        + (left_log + right_log) * count_upper / ell
        + count_upper / ell ** 2)
    left_alpha = modulus * left_log / left
    right_alpha = modulus * right_log / right
    left_delta = 2 * left_log + (modulus / left + 2) / ell
    right_delta = 2 * right_log + (modulus / right + 2) / ell
    centering_error = (
        left_alpha * right_alpha / (modulus - 1)
        + modulus / (modulus - 1) * (
            left_alpha * right_delta
            + right_alpha * left_delta
            + left_delta * right_delta))
    return modulus * collision_error + centering_error


def row_lower_frame_bound(modulus, ell, divisor_left):
    """Return the rigorous eta and lower-frame coefficient in (2)."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_left)):
        raise ValueError("all arguments must be integers")
    if ell < 1 or divisor_left < 2 or 2 * divisor_left >= modulus:
        raise ValueError("require ell>=1 and 2<=U with 2U<m")
    mobius = _mobius_values(2 * divisor_left)
    divisors = tuple(a for a in range(divisor_left + 1, 2 * divisor_left + 1)
                     if mobius[a])
    if not divisors:
        raise ValueError("the squarefree divisor band must be nonempty")
    logs = {
        a: math.log(modulus * ell / a)
        for a in divisors
    }
    frame = {
        a: modulus ** 2 * logs[a] ** 2 * _totient(a) / a ** 2
        for a in divisors
    }
    row_sums = []
    for left in divisors:
        row_sums.append(sum(
            entry_error_bound(modulus, ell, left, right)
            / math.sqrt(frame[left] * frame[right])
            for right in divisors))
    eta = max(row_sums)
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisor_count": len(divisors),
        "normalized_error_schur_bound": eta,
        "proved_frame_coefficient": 1 - eta,
        "positive_lower_frame_proved": eta < 1,
    }


def near_cutoff_lower_frame_bound(N):
    """Certify (2) uniformly over the project's exact near-cutoff rows."""
    if type(N) is not int or N < 1024:
        raise ValueError("N must be an integer at least 1024")
    H, M, V = int(N ** .1), int(N ** .59), int(N ** .15)
    cofactor_left = (N + 8 * M - 1) // (8 * M)
    flags = _prime_flags(2 * M)
    primes = tuple(m for m in range(M + 1, 2 * M + 1) if flags[m])
    worst = None
    for modulus in primes:
        for ell in range(cofactor_left, 2 * cofactor_left):
            receipt = row_lower_frame_bound(modulus, ell, V)
            if (worst is None or
                    receipt["normalized_error_schur_bound"]
                    > worst["normalized_error_schur_bound"]):
                worst = receipt
    if worst is None:
        raise ValueError("the prime companion range must be nonempty")
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "cofactor_left": cofactor_left,
        "prime_count": len(primes),
        "row_count_per_prime": cofactor_left,
        "worst_modulus": worst["modulus"],
        "worst_ell": worst["ell"],
        "uniform_normalized_error_schur_bound":
            worst["normalized_error_schur_bound"],
        "uniform_proved_frame_coefficient": worst["proved_frame_coefficient"],
        "uniform_positive_lower_frame_proved":
            worst["positive_lower_frame_proved"],
    }


if __name__ == "__main__":
    for key, value in near_cutoff_lower_frame_bound(32000).items():
        print(f"{key}: {value}")
