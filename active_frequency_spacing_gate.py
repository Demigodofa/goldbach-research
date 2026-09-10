"""The active h/m frequencies are distinct but too dense for spacing alone.

This tests the next proposed route after ``active_band_energy_conjecture.py``.
It does not falsify that fixed-prime inequality. It falsifies the simpler
mechanism that the large prime denominators make the active additive
frequencies sufficiently separated for a generic large sieve to supply the
needed H^(-1) energy factor.

It is enough to take d=1. Let M=N^(59/100), H=N^(1/10), let m run over
primes in (M,2M], and use the exact rational subband

             m/(6H) < h < m/(4H).                          (1)

Since 2*pi>6 and pi<4, (1) lies inside the corrected angular band
m/(2*pi*H)<h<m/(pi*H). Every h is smaller than m.

1. EXACT COLLISIONS ARE ABSENT.
If h/m=h'/m' with distinct primes m,m' and 0<h<m,0<h'<m', then m divides
h*m'. Hence m divides h, a contradiction. The fractions in (1) are all
distinct.

2. N-SCALE NEAR COLLISIONS ARE FORCED.
For each m, (1) contains m/(12H)+O(1) integers. The prime number theorem
therefore gives

  K := # frequencies  asymp M^2/(H*log M)=N^(1.08+o(1)).    (2)

All frequencies lie in an interval of length 1/(12H). Partition it into
intervals of length 1/(100N). There are O(N/H)=N^(.9+o(1)) cells, so one
cell contains at least

  K/O(N/H) >> M^2/(N*log M)=N^(.18+o(1))                  (3)

distinct frequencies. Exponentials at frequencies in such a cell are
nearly parallel on any integer interval of length N. If the cluster has R
members, rephasing at the left endpoint makes every pairwise phase drift at
most 2*pi/100. The unweighted sampling Gram therefore has top eigenvalue
at least c*R*N for an absolute c>0, rather than the single-frequency scale
N. Under the actual q^(-1)=m^(-1) weight in this d=1 dyadic block, these
become c*R*N/M and N/M respectively: the relative loss is still R. The .18
crowding loss is larger than the desired .10 energy gain. Merely citing
frequency spacing cannot prove the candidate inequality.

This does not determine the fixed positive prime-log form: its coefficients,
full-minus-low centering, target phases and possible dispersion across the
opposite prime can still cancel a dense frequency cluster. A successful next
step must use that arithmetic structure, not a coefficient-uniform spacing
bound.

The finite routine below uses exact Fraction keys. At N=120000,H=3,M=990,
the rational subband has 5414 distinct frequencies and a width-1/N cell with
10 members. This is a shape check only, not asymptotic evidence for primes.
"""
from fractions import Fraction as F
from math import isqrt


def _prime(value):
    return (type(value) is int and value >= 2
            and all(value % divisor
                    for divisor in range(2, isqrt(value) + 1)))


def safe_subband_modes(prime_modulus, shift_length):
    """Integers satisfying m/(6H)<h<m/(4H), using integer comparisons."""
    if not _prime(prime_modulus):
        raise ValueError("prime modulus required")
    if type(shift_length) is not int or shift_length < 1:
        raise ValueError("positive integer shift length required")
    m, hscale = prime_modulus, shift_length
    return tuple(h for h in range(1, m)
                 if 6 * hscale * h > m and 4 * hscale * h < m)


def critical_spacing_budget():
    """Exact power exponents for the d=1 active-frequency multiset."""
    companion = F(59, 100)
    shift = F(1, 10)
    frequency_count = 2 * companion - shift
    resolution_cells = 1 - shift
    crowding = frequency_count - resolution_cells
    return {
        "companion": companion,
        "shift": shift,
        "frequency_count": frequency_count,
        "N_resolution_cells": resolution_cells,
        "forced_cluster": crowding,
        "desired_energy_gain": shift,
        "crowding_exceeds_desired_gain": crowding > shift,
        "spacing_only_route_closes": False,
        "fixed_prime_energy_conjecture_falsified": False,
    }


def distinct_prime_denominator_fractions(m, h, other_m, other_h):
    """Compare two fractions exactly, validating their prime-denominator range."""
    for modulus, numerator in ((m, h), (other_m, other_h)):
        if not _prime(modulus) or type(numerator) is not int:
            raise ValueError("prime moduli and integer numerators required")
        if not 0 < numerator < modulus:
            raise ValueError("numerators must lie strictly between zero and modulus")
    return F(h, m) != F(other_h, other_m)


def finite_cluster_receipt(N=120000, shift_length=3, M=990,
                           cells_per_N=1):
    """Enumerate exact subband fractions and their cells of width 1/(cells_per_N*N)."""
    if not all(type(value) is int and value > 0
               for value in (N, shift_length, M, cells_per_N)):
        raise ValueError("positive integer parameters required")
    frequencies = []
    for modulus in range(M + 1, 2 * M + 1):
        if _prime(modulus):
            for numerator in safe_subband_modes(modulus, shift_length):
                frequencies.append((F(numerator, modulus), modulus, numerator))
    buckets = {}
    scale = cells_per_N * N
    for frequency, modulus, numerator in frequencies:
        cell = scale * numerator // modulus
        buckets.setdefault(cell, []).append((frequency, modulus, numerator))
    largest = max(buckets.values(), key=len) if buckets else []
    return {
        "frequency_count": len(frequencies),
        "distinct_count": len({entry[0] for entry in frequencies}),
        "occupied_cells": len(buckets),
        "largest_cluster": len(largest),
        "largest_cluster_members": tuple(largest),
        "cell_width": F(1, scale),
    }
