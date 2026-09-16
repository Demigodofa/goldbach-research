"""Exact CRT checks for the source-to-binary-correlation mapping.

Owner: Goldbach research. See notes/q286-q46189-complementary-divisor-mapping.md.
These finite helpers verify identities, not the remaining long-divisor bound.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from math import gcd, lcm

from major_arc_kernel import _factorization, _mobius_phi


def central_interval(target):
    """Integer points in the strict interval (N/3, 2N/3)."""
    if type(target) is not int or target < 6 or target % 2:
        raise ValueError("require an even integer N >= 6")
    return range(target // 3 + 1, (2 * target - 1) // 3 + 1)


def complementary_cell(target, left, right):
    """Return (period, residue) for a|n, b|N-n, or None if incompatible."""
    central_interval(target)
    if any(type(d) is not int or d < 1 for d in (left, right)):
        raise ValueError("require positive integer divisors")
    common = gcd(left, right)
    if target % common:
        return None
    quotient = right // common
    multiplier = (0 if quotient == 1 else
                  (target // common) * pow(left // common, -1, quotient)
                  % quotient)
    return lcm(left, right), left * multiplier


def central_progression_count(target, period, residue):
    interval = central_interval(target)
    if type(period) is not int or period < 1 or type(residue) is not int:
        raise ValueError("require a positive integer period and integer residue")
    return ((interval.stop - 1 - residue) // period
            - (interval.start - 1 - residue) // period)


def _coefficients(values):
    if any(type(d) is not int or d < 1 or type(c) not in (int, F)
           for d, c in values.items()):
        raise ValueError("require positive integer indices and exact rational weights")
    return {d: F(c) for d, c in values.items() if c}


def divisor_value(n, coefficients):
    if type(n) is not int or n < 1:
        raise ValueError("require a positive integer argument")
    return sum((c for d, c in _coefficients(coefficients).items() if n % d == 0), F(0))


@dataclass(frozen=True)
class CorrelationExpansion:
    cells: tuple
    density: F
    correlation: F
    discrepancy: F
    discrepancy_bound: F


def complementary_expansion(target, left, right=None):
    """Exact bilinear CRT expansion with the universal l1-product error bound."""
    central_interval(target)
    left = _coefficients(left)
    right = left if right is None else _coefficients(right)
    cells = {}
    for a, ca in left.items():
        for b, cb in right.items():
            cell = complementary_cell(target, a, b)
            if cell is not None:
                cells[cell] = cells.get(cell, F(0)) + ca * cb
    density = sum((c / q for (q, _), c in cells.items()), F(0))
    correlation = sum((c * central_progression_count(target, q, r)
                       for (q, r), c in cells.items()), F(0))
    bound = sum(map(abs, left.values()), F(0)) * sum(map(abs, right.values()), F(0))
    return CorrelationExpansion(
        tuple((q, r, c) for (q, r), c in sorted(cells.items()) if c),
        density, correlation, correlation - F(target, 3) * density, bound)


def centered_square_block(modulus, row, coefficients):
    """The original F_m(ell), exactly, for rational frozen coefficients."""
    if (type(modulus) is not int or modulus < 2
            or type(row) is not int or row < 1):
        raise ValueError("require integer m >= 2 and ell >= 1")
    coefficients = _coefficients(coefficients)
    lcm_coefficients = {}
    for a, ca in coefficients.items():
        for b, cb in coefficients.items():
            q = lcm(a, b)
            lcm_coefficients[q] = lcm_coefficients.get(q, F(0)) + ca * cb
    return sum((c * (F((modulus * row + modulus - 1) // q
                       - (modulus * row) // q) - F(modulus - 1, q))
                for q, c in lcm_coefficients.items()), F(0))


def frozen_mobius_log_vector(n, scale, lower=0, upper=None):
    """Exact log-prime coefficients of sum_(lower<a<=upper,a|n) mu(a)log(X/a)."""
    if type(n) is not int or n < 1 or type(scale) is not int or scale < 1:
        raise ValueError("require positive integer n and X")
    upper = n if upper is None else upper
    if type(lower) is not int or type(upper) is not int or not 0 <= lower <= upper:
        raise ValueError("require integer 0 <= lower <= upper")
    result = {}
    for a in range(lower + 1, min(n, upper) + 1):
        if n % a:
            continue
        mu = _mobius_phi(a)[0]
        for p, power in _factorization(scale):
            result[p] = result.get(p, 0) + mu * power
        for p, power in _factorization(a):
            result[p] = result.get(p, 0) - mu * power
    return tuple(sorted((p, c) for p, c in result.items() if c))
