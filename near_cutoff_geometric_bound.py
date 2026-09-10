"""A deterministic active-frequency bound for one Mobius divisor progression.

Owner: Kevin's Goldbach research.  Purpose: extract a rigorous component from
the dominant near-cutoff divisor band in ``mobius_active_factor_probe.py``.
This lemma is elementary and exact; it does not sum the different divisors or
close the active covariance.

Let m>a>=H>=2 with (a,m)=1 and

 I={1<=h<m: m/(2*pi*H)<min(h,m-h)<m/(pi*H)}.            (1)

Write |x|_m=min(x mod m,(-x) mod m), and L=ceil(m/a).  Then

 sum_(h in I) min(L,m/(2*|h*a|_m))^2 <= 96*m^2/(a*H).   (2)

Proof.  On one positive half of I, every |h*a|_m<=T corresponds to integers
(h,k) with |a*h-k*m|<=T.  The possible k occupy at most
a/(2*pi*H)+2*T/m+2 integers, and each k permits at most 2*T/a+1 integers h.
Including the reflected half gives, for T<=m/2,

 # {h in I: |h*a|_m<=T} <= T/H+a/H+12*T/a+6.           (3)

Use L<=2m/a on |h*a|_m<=a, then sum the shells
2^(j-1)*a<|h*a|_m<=min(2^j*a,m/2).  Equation (3) gives

 8*m^2/(aH)+72*m^2/a^2
 +4*m^2/(3*aH)+14*m^2/a^2
 <=96*m^2/(aH),

because a>=H.  This proves (2).

For a row m*l<ab<m*(l+1), partial summation gives

 |sum_b log(b)e_m(-h*a*b)|
 <=2*log(N)*min(L,m/(2*|h*a|_m)).                        (4)

The centering term is at most 4log(N)/a.  Consequently the exact single-a
centered transform

 Phi_(a,m,l)(h)=mu(a) sum_(m*l<ab<m*(l+1)) log(b)
                    [e_m(-h*a*b)+1/(m-1)]               (5)

satisfies

 sum_(h in I)|Phi_(a,m,l)(h)|^2
 <=800*mu(a)^2*log(N)^2*m^2/(aH).                        (6)

The remaining near-cutoff problem is cross-divisor summation over V<a<=2V;
applying Cauchy to all a separately would lose the size of that band.
"""

import math

import numpy as np

from mobius_covariance_lag_probe import _mobius_values
from mobius_covariance_endpoint_probe import _prime_flags


def _active_modes(modulus, shift_length):
    return tuple(h for h in range(1, modulus)
                 if modulus / (2 * math.pi * shift_length)
                 < min(h, modulus - h)
                 < modulus / (math.pi * shift_length))


def geometric_majorant_energy(modulus, shift_length, divisor):
    """Return the left side and explicit right side of (2)."""
    if any(type(value) is not int for value in
           (modulus, shift_length, divisor)):
        raise ValueError("modulus, shift_length and divisor must be integers")
    if not 2 <= shift_length <= divisor < modulus:
        raise ValueError("require 2<=shift_length<=divisor<modulus")
    if math.gcd(divisor, modulus) != 1:
        raise ValueError("divisor and modulus must be coprime")
    modes = np.array(_active_modes(modulus, shift_length), dtype=np.int64)
    residues = (modes * divisor) % modulus
    centered = np.minimum(residues, modulus - residues)
    length = (modulus + divisor - 1) // divisor
    terms = np.minimum(length, modulus / (2 * centered))
    energy = float(np.sum(terms ** 2))
    bound = 96 * modulus ** 2 / (divisor * shift_length)
    return {
        "modulus": modulus,
        "shift_length": shift_length,
        "divisor": divisor,
        "active_size": len(modes),
        "progression_length_bound": length,
        "saturated_count": int(np.sum(2 * centered <= divisor)),
        "energy": energy,
        "bound": bound,
        "bound_ratio": energy / bound,
        "energy_over_active_length": (
            energy / (len(modes) * length) if len(modes) else 0.0),
    }


def exact_weighted_progression_energy(N, modulus, shift_length, divisor, ell):
    """Evaluate (5) for one row and compare it with the bound (6)."""
    if any(type(value) is not int for value in
           (N, modulus, shift_length, divisor, ell)):
        raise ValueError("all arguments must be integers")
    if N < 3 or not 2 <= shift_length <= divisor < modulus:
        raise ValueError("require N>=3 and 2<=shift_length<=divisor<modulus")
    if math.gcd(divisor, modulus) != 1:
        raise ValueError("divisor and modulus must be coprime")
    if ell < 1 or modulus * (ell + 1) - 1 > N:
        raise ValueError("the complete row must lie in 1..N")
    first = modulus * ell // divisor + 1
    last = (modulus * (ell + 1) - 1) // divisor
    cofactors = np.arange(first, last + 1, dtype=np.int64)
    weights = np.log(cofactors)
    modes = np.array(_active_modes(modulus, shift_length), dtype=np.int64)
    mobius = int(_mobius_values(divisor)[divisor])
    phases = np.exp(-2j * math.pi / modulus
                    * modes[:, None] * divisor * cofactors[None, :])
    values = mobius * (phases @ weights + np.sum(weights) / (modulus - 1))
    energy = float(np.sum(np.abs(values) ** 2))
    bound = (800 * mobius ** 2 * math.log(N) ** 2 * modulus ** 2
             / (divisor * shift_length))
    return {
        "N": N,
        "modulus": modulus,
        "shift_length": shift_length,
        "divisor": divisor,
        "ell": ell,
        "mobius": mobius,
        "cofactor_first": first,
        "cofactor_last": last,
        "active_size": len(modes),
        "energy": energy,
        "bound": bound,
        "bound_ratio": energy / bound if bound else 0.0,
        "cross_divisor_sum_proved": False,
    }


def averaged_near_cutoff_receipt(N):
    """Average (2) over the actual prime m and squarefree V<a<=2V ranges."""
    if type(N) is not int or N < 1024:
        raise ValueError("N must be an integer at least 1024")
    H, M, V = int(N ** .1), int(N ** .59), int(N ** .15)
    flags = _prime_flags(2 * M)
    primes = tuple(m for m in range(M + 1, 2 * M + 1) if flags[m])
    mobius = _mobius_values(2 * V)
    divisors = tuple(a for a in range(V + 1, 2 * V + 1) if mobius[a])
    energy = square_root_scale = trivial_scale = 0.0
    saturated = pairs = 0
    for modulus in primes:
        weight = math.log(modulus) ** 2 / modulus
        modes = np.array(_active_modes(modulus, H), dtype=np.int64)
        for divisor in divisors:
            residues = (modes * divisor) % modulus
            centered = np.minimum(residues, modulus - residues)
            length = (modulus + divisor - 1) // divisor
            terms = np.minimum(length, modulus / (2 * centered))
            energy += weight * float(np.sum(terms ** 2))
            square_root_scale += weight * len(modes) * length
            trivial_scale += weight * len(modes) * length ** 2
            saturated += int(np.sum(2 * centered <= divisor))
            pairs += len(modes)
    return {
        "N": N,
        "H": H,
        "M": M,
        "V": V,
        "prime_count": len(primes),
        "squarefree_divisor_count": len(divisors),
        "energy": energy,
        "energy_over_square_root_scale": energy / square_root_scale,
        "energy_over_trivial_scale": energy / trivial_scale,
        "saturated_fraction": saturated / pairs,
        "cross_divisor_sum_proved": False,
    }


if __name__ == "__main__":
    for arguments in ((1009, 5, 8), (10007, 10, 31),
                      (100003, 20, 89), (1000003, 32, 181)):
        print(geometric_majorant_energy(*arguments))
    for N in (32000, 200000, 1200000):
        print(averaged_near_cutoff_receipt(N))
