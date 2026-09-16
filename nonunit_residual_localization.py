"""Exact fixtures for signed localization to arguments coprime to the target.

Owner: Goldbach research. Analytical proof: notes/nonunit-residual-localization.md.
These small helpers do not estimate an asymptotic error from finite data.
"""

from fractions import Fraction as F
from math import gcd

from complementary_divisor_correlation import central_interval
from cutoff_normalized_remainder import singular_multiplier
from major_arc_kernel import _factorization, _mobius_phi


def _positive(*values):
    if any(type(value) is not int or value < 1 for value in values):
        raise ValueError("require positive integers")


def excluded_cutoff_log_vector(n, cutoff, excluded, denominator=1):
    """F_(cutoff/denominator)^(excluded)(n) as an exact log-prime vector."""
    _positive(n, cutoff, excluded, denominator)
    result = {}
    for d in range(1, min(n, cutoff // denominator) + 1):
        if n % d or gcd(d, excluded) != 1:
            continue
        mu = _mobius_phi(d)[0]
        for p, power in _factorization(cutoff):
            result[p] = result.get(p, 0) + mu * power
        for p, power in _factorization(denominator * d):
            result[p] = result.get(p, 0) - mu * power
    return tuple(sorted((p, value) for p, value in result.items() if value))


def multiple_argument_log_vector(n, cutoff, common):
    """Alternating excluded-prime cutoff formula for A_cutoff(common*n)."""
    _positive(n, cutoff, common)
    result = {}
    for h in range(1, common + 1):
        if common % h:
            continue
        mu = _mobius_phi(h)[0]
        if not mu:
            continue
        for p, value in excluded_cutoff_log_vector(n, cutoff, common, h):
            result[p] = result.get(p, 0) + mu * value
    return tuple(sorted((p, value) for p, value in result.items() if value))


def nonunit_mobius_weight(n, target):
    """Inclusion-exclusion indicator for gcd(n,target)>1."""
    _positive(n)
    central_interval(target)
    common = gcd(n, target)
    return -sum(_mobius_phi(g)[0] for g in range(2, common + 1) if common % g == 0)


def excluded_singular_blocks(target, excluded):
    """Finite Euler main blocks, normalized by 2*C_2, for excluded|target."""
    central_interval(target)
    _positive(excluded)
    if target % excluded:
        raise ValueError("the excluded divisor must divide the target")
    reduced = target // excluded
    prefactor = F(excluded, _mobius_phi(excluded)[1])
    return {
        c: prefactor * F(_mobius_phi(c)[0] ** 2, _mobius_phi(c)[1])
        * singular_multiplier(c * excluded)
        for c in range(1, reduced + 1) if reduced % c == 0 and gcd(c, excluded) == 1
    }
