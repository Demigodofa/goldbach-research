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
from major_arc_kernel import _factorization, _mobius_phi, ramanujan


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


def common_divisor_density_blocks(target, coefficients, right=None):
    """Regroup the squarefree bilinear CRT density by g, then coprime a,b.

    Rational coefficients permit exact tests of the grouping. For the
    analytic application they stand for mu(d)log(R/d).
    """
    central_interval(target)
    coefficients = _coefficients(coefficients)
    right = coefficients if right is None else _coefficients(right)
    if any(_mobius_phi(d)[0] == 0 for d in coefficients.keys() | right.keys()):
        raise ValueError("nonzero coefficients must have squarefree indices")
    cutoff = max(coefficients, default=0)
    right_cutoff = max(right, default=0)
    blocks = {}
    for g in range(1, min(cutoff, right_cutoff) + 1):
        if target % g or not _mobius_phi(g)[0]:
            continue
        total = F(0)
        for a in range(1, cutoff // g + 1):
            if gcd(a, g) != 1:
                continue
            for b in range(1, right_cutoff // g + 1):
                if gcd(b, g) != 1 or gcd(a, b) != 1:
                    continue
                total += (coefficients.get(g * a, F(0))
                          * right.get(g * b, F(0)) / (g * a * b))
        if total:
            blocks[g] = total
    return blocks


def selberg_coordinates(coefficients):
    """Exact w(q)=sum_(q|d) c(d)/d; no squarefree-support restriction."""
    coefficients = _coefficients(coefficients)
    result = {}
    for d, coefficient in coefficients.items():
        for q in range(1, d + 1):
            if d % q == 0:
                result[q] = result.get(q, F(0)) + coefficient / d
    return {q: value for q, value in result.items() if value}


def ramanujan_density_channels(target, coefficients):
    """Signed complete-period reflected density by conductor, not window mass.

    For real rational coefficients each entry is c_q(target)*w(q)^2, so
    summing absolute entries gives the conductorwise absolute envelope.
    """
    central_interval(target)
    return {q: ramanujan(q, target) * value ** 2
            for q, value in selberg_coordinates(coefficients).items()}


def cutoff_mixture_norm_parts(exponents, weights):
    """Return the leading norm floor and nonnegative excess terms.

    Exact rational fixtures for the analytic result in
    notes/finite-cutoff-mixture-obstruction.md, not a finite-N norm bound.
    Weights may be signed and need not sum to one.
    """
    exponents, weights = tuple(exponents), tuple(weights)
    if not exponents or len(exponents) != len(weights):
        raise ValueError("require equally sized nonempty exponent and weight lists")
    if any(type(x) not in (int, F) for x in exponents + weights):
        raise ValueError("require exact rational exponents and weights")
    exponents, weights = tuple(map(F, exponents)), tuple(map(F, weights))
    previous, suffix = F(0), sum(weights, F(0))
    penalties = []
    for exponent, weight in zip(exponents, weights):
        if not previous < exponent < F(1, 2):
            raise ValueError("require strictly increasing exponents in (0, 1/2)")
        penalties.append((exponent - previous) * (suffix - 1) ** 2)
        previous, suffix = exponent, suffix - weight
    return 1 - exponents[-1], tuple(penalties)


def cutoff_log_vectors(n, cutoff):
    """Return exact log-prime vectors (A(n), D(n)) in the cutoff gauge."""
    if type(n) is not int or n < 2 or type(cutoff) is not int or cutoff < 1:
        raise ValueError("require integer n >= 2 and cutoff >= 1")
    return (
        frozen_mobius_log_vector(n, cutoff, upper=cutoff),
        frozen_mobius_log_vector(n, cutoff, lower=cutoff, upper=max(n, cutoff)),
    )
