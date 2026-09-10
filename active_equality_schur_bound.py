"""A rigorous Schur bound for active equal-integer divisor collisions.

For one complete row, the equality part of the active raw Gram is

 Eeq_(a,b)=(1-rho)|I| sum_(ml<n<m(l+1),[a,b]|n)
                         log(n/a)log(n/b).               (1)

Normalize it by the proven denominator frame

 (rho F)_aa=rho*m^2*log(ml/a)^2*phi(a)/a^2.             (2)

Put L_a=log(ml/a), q=[a,b], and C_q=#{ml<n<m(l+1):q|n}.
Since |I|=rho(m-1), C_q<=m/q+2, and
log(n/a)<=L_a+1/l, the absolute normalized entry in (1) is at most

 R_(a,b)=(1-rho)(m-1)(m/q+2)(L_a+1/l)(L_b+1/l)ab
          /(m^2 L_a L_b sqrt(phi(a)phi(b))).             (3)

Consequently eta_eq=max_a sum_b R_(a,b) proves Eeq<=eta_eq*rho*F.

For a,b in (U,2U],

 sum_b gcd(a,b)
 <=sum_(d|a)phi(d)(U/d+1)<=U*tau(a)+a.                  (4)

Together with phi(a)>=C_eps*a^(1-eps), equations (3)--(4) give

 eta_eq <<_eps N^eps*(1+U^2/m).                         (5)

At U=floor(N^.15), m asymp N^.59, the endpoint term decays like
N^(-.29+eps).  Thus the equality-collision component satisfies the required
N^eps active/frame bound.  This theorem does not estimate the unequal-
difference Dirichlet kernel or exploit its measured cancellation with (1).
"""

import math

from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from near_cutoff_geometric_bound import _active_modes


def _entry_bound_precomputed(modulus, rho, ell, left, right,
                             left_log, right_log, left_phi, right_phi):
    if left_log <= 0 or right_log <= 0:
        raise ValueError("the frozen logarithms must be positive")
    common = math.lcm(left, right)
    return (
        (1 - rho) * (modulus - 1) * (modulus / common + 2)
        * (left_log + 1 / ell) * (right_log + 1 / ell)
        * left * right
        / (modulus ** 2 * left_log * right_log
           * math.sqrt(left_phi * right_phi)))


def _entry_bound_with_rho(modulus, rho, ell, left, right):
    left_log = math.log(modulus * ell / left)
    right_log = math.log(modulus * ell / right)
    return _entry_bound_precomputed(
        modulus, rho, ell, left, right, left_log, right_log,
        _totient(left), _totient(right))


def equality_normalized_entry_bound(modulus, shift_length, ell, left, right):
    """Return R_(a,b) in (3)."""
    if any(type(value) is not int for value in (
            modulus, shift_length, ell, left, right)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= left < modulus
            or not 2 <= shift_length <= right < modulus or ell < 1):
        raise ValueError("require 2<=H<=a,b<m and ell>=1")
    modes = _active_modes(modulus, shift_length)
    if not modes:
        raise ValueError("the active frequency band must be nonempty")
    rho = len(modes) / (modulus - 1)
    return _entry_bound_with_rho(modulus, rho, ell, left, right)


def row_equality_schur_bound(modulus, shift_length, ell, divisor_left):
    """Return the rigorous equality-component Schur certificate."""
    if any(type(value) is not int for value in (
            modulus, shift_length, ell, divisor_left)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= divisor_left
            or 2 * divisor_left >= modulus or ell < 1):
        raise ValueError("require 2<=H<=U, 2U<m, and ell>=1")
    mobius = _mobius_values(2 * divisor_left)
    divisors = tuple(a for a in range(divisor_left + 1, 2 * divisor_left + 1)
                     if mobius[a])
    if not divisors:
        raise ValueError("the squarefree divisor band must be nonempty")
    modes = _active_modes(modulus, shift_length)
    if not modes:
        raise ValueError("the active frequency band must be nonempty")
    rho = len(modes) / (modulus - 1)
    logs = {a: math.log(modulus * ell / a) for a in divisors}
    totients = {a: _totient(a) for a in divisors}
    row_sums = tuple(sum(
        _entry_bound_precomputed(
            modulus, rho, ell, left, right, logs[left], logs[right],
            totients[left], totients[right])
        for right in divisors)
        for left in divisors)
    eta = max(row_sums)
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "ell": ell,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisor_count": len(divisors),
        "proved_equality_schur_bound": eta,
        "worst_divisor": divisors[row_sums.index(eta)],
        "equality_component_N_epsilon_theorem": True,
        "unequal_component_proved": False,
    }


def near_cutoff_equality_schur_bound(N):
    """Maximize the exact certificate over all project primes and rows."""
    if type(N) is not int or N < 1024:
        raise ValueError("N must be an integer at least 1024")
    H, M, V = int(N ** .1), int(N ** .59), int(N ** .15)
    cofactor_left = (N + 8 * M - 1) // (8 * M)
    flags = _prime_flags(2 * M)
    primes = tuple(m for m in range(M + 1, 2 * M + 1) if flags[m])
    mobius = _mobius_values(2 * V)
    divisors = tuple(a for a in range(V + 1, 2 * V + 1) if mobius[a])
    totients = {a: _totient(a) for a in divisors}
    worst = None
    for modulus in primes:
        modes = _active_modes(modulus, H)
        if not modes:
            continue
        rho = len(modes) / (modulus - 1)
        for ell in range(cofactor_left, 2 * cofactor_left):
            logs = {a: math.log(modulus * ell / a) for a in divisors}
            row_sums = tuple(sum(
                _entry_bound_precomputed(
                    modulus, rho, ell, left, right,
                    logs[left], logs[right],
                    totients[left], totients[right])
                for right in divisors)
                for left in divisors)
            eta = max(row_sums)
            receipt = {
                "modulus": modulus,
                "ell": ell,
                "proved_equality_schur_bound": eta,
                "worst_divisor": divisors[row_sums.index(eta)],
            }
            if (worst is None or receipt["proved_equality_schur_bound"]
                    > worst["proved_equality_schur_bound"]):
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
        "uniform_proved_equality_schur_bound":
            worst["proved_equality_schur_bound"],
        "worst_modulus": worst["modulus"],
        "worst_ell": worst["ell"],
        "worst_divisor": worst["worst_divisor"],
        "equality_component_N_epsilon_theorem": True,
        "unequal_component_proved": False,
    }


if __name__ == "__main__":
    for key, value in near_cutoff_equality_schur_bound(32000).items():
        print(f"{key}: {value}")
