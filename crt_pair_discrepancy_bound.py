"""A rigorous frame bound for the exact-minus-triangular CRT discrepancy.

Let S={ml+1,...,ml+m-1}, R=m-1, and for signed |r|<R let C_(a,b)(r)
be the weighted count of pairs n,n' in S with n-n'=r, a|n, and b|n'.
With g=gcd(a,b), q=lcm(a,b), and L_a=log(ml/a), the triangular model is

 C0_(a,b)(r)=1_(g|r)*(R-|r|)L_aL_b/q.                  (1)

If g|r, CRT gives one residue class modulo q in an interval of R-|r|
integers, so its count differs from (R-|r|)/q by less than one.  Also every
row logarithm differs from L_a by less than 1/l.  Thus

 |C_(a,b)(r)-C0_(a,b)(r)|
 <=1_(g|r){L_aL_b+(m/q+1)[(L_a+L_b)/l+1/l^2]}.         (2)

The active set is the union of two frequency intervals.  The standard
geometric bound for one interval gives

 sum_(s mod m)|K_I(s)|<=4m(1+log m).                    (3)

Every residue has at most two signed representatives |r|<R, so (2)--(3)
give an explicit entry bound for the active discrepancy D.

After normalization by the rho-weighted totient frame, Schur yields

 ||D||_(rho F)
 <<_eps N^eps{H U^2 log(m)/m+H log(m)/l}.               (4)

At H=N^.1,U=N^.15,m=N^.59,l=N^.41, the two terms are
N^(-.19+eps) and N^(-.31+eps).  Hence the discrepancy is o(1) at the project
exponents.  This theorem concerns the raw equality-plus-unequal Gram; the
centering correction is not included.
"""

import math

from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from near_cutoff_geometric_bound import _active_modes


def _require_prime(modulus):
    flags = _prime_flags(modulus)
    if not flags[modulus]:
        raise ValueError("modulus must be prime")


def dirichlet_residue_l1_bound(modulus):
    """Return the right side of (3)."""
    if type(modulus) is not int or modulus < 3:
        raise ValueError("modulus must be an integer at least 3")
    return 4 * modulus * (1 + math.log(modulus))


def _entry_bound_precomputed(modulus, rho, ell, left, right,
                             left_log, right_log, left_phi, right_phi):
    common = math.lcm(left, right)
    log_variation = ((left_log + right_log) / ell + 1 / ell ** 2)
    pair_error = (left_log * right_log
                  + (modulus / common + 1) * log_variation)
    signed_kernel_l1 = 2 * dirichlet_residue_l1_bound(modulus)
    unnormalized = (1 - rho) * signed_kernel_l1 * pair_error
    frame_scale = (rho * modulus ** 2 * left_log * right_log
                   * math.sqrt(left_phi * right_phi) / (left * right))
    return unnormalized / frame_scale


def discrepancy_normalized_entry_bound(modulus, shift_length, ell,
                                        left, right):
    """Return the exact entry majorant derived from (2)--(3)."""
    if any(type(value) is not int for value in (
            modulus, shift_length, ell, left, right)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= left < modulus
            or not 2 <= shift_length <= right < modulus or ell < 1):
        raise ValueError("require 2<=H<=a,b<m and ell>=1")
    _require_prime(modulus)
    modes = _active_modes(modulus, shift_length)
    if not modes:
        raise ValueError("the active frequency band must be nonempty")
    rho = len(modes) / (modulus - 1)
    left_log = math.log(modulus * ell / left)
    right_log = math.log(modulus * ell / right)
    return _entry_bound_precomputed(
        modulus, rho, ell, left, right, left_log, right_log,
        _totient(left), _totient(right))


def row_crt_discrepancy_bound(modulus, shift_length, ell, divisor_left):
    """Return the rigorous normalized Schur bound in one complete row."""
    if any(type(value) is not int for value in (
            modulus, shift_length, ell, divisor_left)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= divisor_left
            or 2 * divisor_left >= modulus or ell < 1):
        raise ValueError("require 2<=H<=U, 2U<m, and ell>=1")
    _require_prime(modulus)
    modes = _active_modes(modulus, shift_length)
    if not modes:
        raise ValueError("the active frequency band must be nonempty")
    rho = len(modes) / (modulus - 1)
    mobius = _mobius_values(2 * divisor_left)
    divisors = tuple(a for a in range(divisor_left + 1, 2 * divisor_left + 1)
                     if mobius[a])
    logs = {a: math.log(modulus * ell / a) for a in divisors}
    totients = {a: _totient(a) for a in divisors}
    row_sums = tuple(sum(
        _entry_bound_precomputed(
            modulus, rho, ell, left, right,
            logs[left], logs[right], totients[left], totients[right])
        for right in divisors)
        for left in divisors)
    bound = max(row_sums)
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "ell": ell,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisor_count": len(divisors),
        "proved_discrepancy_schur_bound": bound,
        "worst_divisor": divisors[row_sums.index(bound)],
        "crt_discrepancy_o_one_theorem": True,
        "centering_theorem_proved": False,
    }


def near_cutoff_crt_discrepancy_bound(N):
    """Maximize the exact certificate over all project primes and rows."""
    if type(N) is not int or N < 32000:
        raise ValueError("N must be an integer at least 32000")
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
            bound = max(row_sums)
            if worst is None or bound > worst["bound"]:
                worst = {
                    "bound": bound,
                    "modulus": modulus,
                    "ell": ell,
                    "divisor": divisors[row_sums.index(bound)],
                }
    if worst is None:
        raise ValueError("the prime companion range must be nonempty")
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "cofactor_left": cofactor_left,
        "prime_count": len(primes),
        "uniform_proved_discrepancy_schur_bound": worst["bound"],
        "worst_modulus": worst["modulus"],
        "worst_ell": worst["ell"],
        "worst_divisor": worst["divisor"],
        "crt_discrepancy_o_one_theorem": True,
        "centering_theorem_proved": False,
    }


if __name__ == "__main__":
    for key, value in near_cutoff_crt_discrepancy_bound(32000).items():
        print(f"{key}: {value}")
