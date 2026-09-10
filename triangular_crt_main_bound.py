"""A rigorous frame bound for the triangular CRT active main term.

For g=gcd(a,b), the sampled triangular kernel T_g(h) from
``triangular_crt_main_probe.py`` is a sum over g residue classes of squared
geometric progressions.  Hence

 T_g(h)<=g*min(ceil(m/g),m/(2|hg|_m))^2.                (1)

If g>=H, the one-divisor geometric lemma gives

 sum_(h in I)T_g(h)<=96m^2/H.                           (2)

If g<H and m/(2*pi*H)>=2, no wrap occurs on the positive active half, and
the reciprocal-square tail gives

 sum_(h in I)T_g(h)<=2*pi*m*H/g.                        (3)

When also m>=16*pi*H, the exact active-band density obeys
rho>=1/(2*pi*H).  Dividing the triangular main entry by the rho-weighted
totient frame therefore gives

 B_(a,b)<=192*pi*g/sqrt(phi(a)phi(b)),       g>=H,
 B_(a,b)<=4*pi^2*H^2/(m sqrt(phi(a)phi(b))), g<H.        (4)

The dyadic gcd row sum and phi(n)>=C_eps*n^(1-eps) prove

 max_a sum_b B_(a,b)<<_eps N^eps*(1+H^2/m).             (5)

Thus the triangular CRT main satisfies the required active/frame estimate in
the near-cutoff band.  This result does not control the exact-minus-main
endpoint/logarithmic discrepancy or the centering correction.
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


def triangular_kernel_sum_bound(modulus, shift_length, gcd_value):
    """Return the right side of (2) or (3)."""
    if any(type(value) is not int for value in (
            modulus, shift_length, gcd_value)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length < modulus
            or not 1 <= gcd_value < modulus):
        raise ValueError("require 2<=H<m and 1<=g<m")
    _require_prime(modulus)
    if modulus / (2 * math.pi * shift_length) < 2:
        raise ValueError("the active lower endpoint must be at least 2")
    if gcd_value >= shift_length:
        return 96 * modulus ** 2 / shift_length
    return 2 * math.pi * modulus * shift_length / gcd_value


def _normalized_entry_bound(modulus, shift_length, left, right):
    gcd_value = math.gcd(left, right)
    totient_scale = math.sqrt(_totient(left) * _totient(right))
    if gcd_value >= shift_length:
        return 192 * math.pi * gcd_value / totient_scale
    return (4 * math.pi ** 2 * shift_length ** 2
            / (modulus * totient_scale))


def triangular_normalized_entry_bound(modulus, shift_length, left, right):
    """Return the applicable explicit entry bound in (4)."""
    if any(type(value) is not int for value in (
            modulus, shift_length, left, right)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= left < modulus
            or not 2 <= shift_length <= right < modulus
            or modulus < 16 * math.pi * shift_length):
        raise ValueError("require 2<=H<=a,b<m and m>=16*pi*H")
    _require_prime(modulus)
    return _normalized_entry_bound(modulus, shift_length, left, right)


def row_triangular_main_bound(modulus, shift_length, divisor_left):
    """Return the rigorous Schur bound obtained from (4)."""
    if any(type(value) is not int for value in (
            modulus, shift_length, divisor_left)):
        raise ValueError("all arguments must be integers")
    if (not 2 <= shift_length <= divisor_left
            or 2 * divisor_left >= modulus):
        raise ValueError("require 2<=H<=U and 2U<m")
    _require_prime(modulus)
    mobius = _mobius_values(2 * divisor_left)
    divisors = tuple(a for a in range(divisor_left + 1, 2 * divisor_left + 1)
                     if mobius[a])
    row_sums = tuple(sum(
        _normalized_entry_bound(
            modulus, shift_length, left, right)
        for right in divisors)
        for left in divisors)
    bound = max(row_sums)
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisor_count": len(divisors),
        "proved_triangular_main_schur_bound": bound,
        "worst_divisor": divisors[row_sums.index(bound)],
        "triangular_main_N_epsilon_theorem": True,
        "discrepancy_theorem_proved": False,
    }


def near_cutoff_triangular_main_bound(N):
    """Maximize the row bound over the exact prime companion range."""
    if type(N) is not int or N < 1024:
        raise ValueError("N must be an integer at least 1024")
    H, M, V = int(N ** .1), int(N ** .59), int(N ** .15)
    flags = _prime_flags(2 * M)
    primes = tuple(m for m in range(M + 1, 2 * M + 1) if flags[m])
    receipts = tuple(row_triangular_main_bound(m, H, V) for m in primes)
    worst = max(receipts, key=lambda item:
                item["proved_triangular_main_schur_bound"])
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "prime_count": len(primes),
        "uniform_proved_triangular_main_schur_bound":
            worst["proved_triangular_main_schur_bound"],
        "worst_modulus": worst["modulus"],
        "worst_divisor": worst["worst_divisor"],
        "triangular_main_N_epsilon_theorem": True,
        "discrepancy_theorem_proved": False,
    }


if __name__ == "__main__":
    for key, value in near_cutoff_triangular_main_bound(32000).items():
        print(f"{key}: {value}")
