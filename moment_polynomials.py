"""Exact polynomial lower bounds for multiplicity-zero counts.

For a histogram with multiplicities in ``0..K``, let
``S_j = sum_i binom(multiplicity_i, j)``.  Every polynomial returned here has
``Q(0)=1`` and ``Q(k)<=0`` for integral ``1<=k<=K``.  Hence
``sum_i Q(multiplicity_i)`` is a rigorous lower bound for the zero count.

Inputs are assumed feasible: they must arise from nonnegative multiplicities
supported on the integer set ``0..K``.  The routine checks only the immediate
support consequence that every binomial moment above K is zero.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from math import comb
from typing import Iterable


@dataclass(frozen=True)
class RootPolynomial:
    """A polynomial stored in Newton/binomial coefficients at zero."""
    roots: tuple[int, ...]
    coefficients: tuple[Fraction, ...]

    @property
    def degree(self) -> int:
        return len(self.roots)


def _validate_cap_degree(cap: int, degree: int) -> None:
    if type(cap) is not int or cap < 0:
        raise ValueError("cap must be a nonnegative integer")
    if type(degree) is not int or degree < 0:
        raise ValueError("degree must be a nonnegative integer")


def _adjacent_pair_roots(lo: int, hi: int, pairs: int) -> Iterable[tuple[int, ...]]:
    """Choose disjoint adjacent pairs wholly contained in ``[lo, hi]``."""
    if pairs == 0:
        yield ()
        return
    for start in range(lo, hi):
        for rest in _adjacent_pair_roots(start + 2, hi, pairs - 1):
            yield (start, start + 1) + rest


def _coefficients_from_roots(roots: tuple[int, ...]) -> tuple[Fraction, ...]:
    """Return c_j=Delta^j Q(0), where Q(k)=prod(r-k)/prod(r)."""
    denominator=1
    for root in roots:
        denominator*=root
    values=[]
    for k in range(len(roots)+1):
        numerator=1
        for root in roots:
            numerator*=root-k
        values.append(Fraction(numerator,denominator))
    coefficients=[]
    while values:
        coefficients.append(values[0])
        values=[values[i+1]-values[i] for i in range(len(values)-1)]
    return tuple(coefficients)


@lru_cache(maxsize=None)
def coefficient_families(cap: int, degree: int) -> tuple[RootPolynomial, ...]:
    """Enumerate the requested distinct-root families through ``degree``.

    Odd degrees use root 1 plus disjoint adjacent pairs.  Even degrees use
    roots 1 and K plus disjoint adjacent pairs in the strict interior.  The
    empty polynomial is intentionally omitted because callers add lower bound
    zero directly.
    """
    _validate_cap_degree(cap,degree)
    answer=[]
    for current_degree in range(1,min(cap,degree)+1):
        if current_degree % 2:
            pair_count=(current_degree-1)//2
            # Root 1 is reserved, so every adjacent pair begins at least at 2.
            for tail in _adjacent_pair_roots(2,cap,pair_count):
                roots=(1,)+tail
                if len(set(roots))==len(roots):
                    answer.append(RootPolynomial(roots,_coefficients_from_roots(roots)))
        elif cap >= 2:
            pair_count=(current_degree-2)//2
            # Roots 1 and K are reserved; pairs stay in [2, K-1].
            for tail in _adjacent_pair_roots(2,cap-1,pair_count):
                roots=(1,cap)+tail
                if len(set(roots))==len(roots):
                    answer.append(RootPolynomial(roots,_coefficients_from_roots(roots)))
    return tuple(answer)


def evaluate(polynomial: RootPolynomial, k: int) -> Fraction:
    """Evaluate a polynomial from its binomial-basis coefficients."""
    if type(k) is not int or k < 0:
        raise ValueError("evaluation point must be a nonnegative integer")
    return sum((coefficient*comb(k,j) for j,coefficient in enumerate(polynomial.coefficients)
                if j<=k),Fraction())


def ceiling(value: Fraction) -> int:
    return -((-value.numerator)//value.denominator)


def strongest_lower(moments: list[int] | tuple[int, ...], cap: int) -> dict:
    """Return the strongest requested polynomial lower bound.

    The caller supplies feasible binomial moments through the desired maximum
    degree. Selection compares exact Fractions, then rounds the selected lower
    bound upward once because the unknown zero count is integral.  For the
    requested root family plus zero, this is the optimal real moment-LP lower
    bound; the ceiling is a valid integer-count lower bound.
    """
    if type(cap) is not int or cap < 0:
        raise ValueError("cap must be a nonnegative integer")
    if not moments or any(type(value) is not int or value < 0 for value in moments):
        raise ValueError("moments must be nonempty nonnegative integers")
    if any(value for value in moments[cap+1:]):
        raise ValueError("moments above the multiplicity cap must be zero")
    if cap==0:
        exact=Fraction(moments[0])
        return {
            "lower":moments[0],"numerator":exact.numerator,"denominator":exact.denominator,
            "roots":[],"degree":0,"coefficients":[[1,1]],"family_count":0,
            "method":"exact cap-zero moment LP lower bound, rounded for integer counts",
        }
    max_degree=min(cap,len(moments)-1)
    best=Fraction(0)
    selected=None
    for polynomial in coefficient_families(cap,max_degree):
        value=sum((coefficient*moments[j]
                   for j,coefficient in enumerate(polynomial.coefficients)),Fraction())
        if value>best:
            best=value
            selected=polynomial
    return {
        "lower":ceiling(best),
        "numerator":best.numerator,
        "denominator":best.denominator,
        "roots":list(selected.roots) if selected else [],
        "degree":selected.degree if selected else 0,
        "coefficients":[[coefficient.numerator,coefficient.denominator]
                        for coefficient in selected.coefficients] if selected else [[0,1]],
        "family_count":len(coefficient_families(cap,max_degree)),
        "method":"optimal real moment LP root-polynomial lower bound, rounded for integer counts",
    }
