"""Exact fixtures for the cutoff-normalized complementary reduction.

Owner: Goldbach research. The uniform analytical proof is in
notes/cutoff-normalized-complementary-remainder.md. No asymptotic claim is
inferred from these finite helpers.
"""

from fractions import Fraction as F
from math import gcd

from complementary_divisor_correlation import (
    _coefficients, central_interval, frozen_mobius_log_vector,
)
from major_arc_kernel import _factorization, _mobius_phi


def singular_multiplier(n):
    """Exact S_2(n)/(2 C_2), including zero for positive odd n."""
    if type(n) is not int or n < 1:
        raise ValueError("require a positive integer")
    if n % 2:
        return F(0)
    result = F(1)
    for p, _ in _factorization(n):
        if p > 2:
            result *= F(p - 1, p - 2)
    return result


def singular_divisor_blocks(n):
    """Finite normalized summands in sum_(g|n) mu(g)^2 S_2(g)/phi(g)."""
    singular_multiplier(n)
    return {
        g: F(_mobius_phi(g)[0] ** 2, _mobius_phi(g)[1]) * singular_multiplier(g)
        for g in range(1, n + 1) if n % g == 0
    }


def common_divisor_density_blocks(target, coefficients):
    """Regroup the squarefree bilinear CRT density by g, then coprime a,b.

    Rational coefficients permit exact tests of the grouping. For the
    analytic application they stand for mu(d)log(R/d).
    """
    central_interval(target)
    coefficients = _coefficients(coefficients)
    if any(_mobius_phi(d)[0] == 0 for d in coefficients):
        raise ValueError("nonzero coefficients must have squarefree indices")
    cutoff = max(coefficients, default=0)
    blocks = {}
    for g in range(1, cutoff + 1):
        if target % g or not _mobius_phi(g)[0]:
            continue
        total = F(0)
        for a in range(1, cutoff // g + 1):
            if gcd(a, g) != 1:
                continue
            for b in range(1, cutoff // g + 1):
                if gcd(b, g) != 1 or gcd(a, b) != 1:
                    continue
                total += (coefficients.get(g * a, F(0))
                          * coefficients.get(g * b, F(0)) / (g * a * b))
        if total:
            blocks[g] = total
    return blocks


def cutoff_log_vectors(n, cutoff):
    """Return exact log-prime vectors (A(n), D(n)) in the cutoff gauge."""
    if type(n) is not int or n < 2 or type(cutoff) is not int or cutoff < 1:
        raise ValueError("require integer n >= 2 and cutoff >= 1")
    return (
        frozen_mobius_log_vector(n, cutoff, upper=cutoff),
        frozen_mobius_log_vector(n, cutoff, lower=cutoff, upper=max(n, cutoff)),
    )
