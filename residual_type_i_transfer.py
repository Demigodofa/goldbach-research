"""Exact AP-density fixtures for the unconditional actual-residual transfer.

Owner: Goldbach research. Analytical proof and scope are in
notes/unconditional-residual-type-i-transfer.md. These formal log-prime
identities verify the grouping, not asymptotic cancellation or Goldbach.
"""

from fractions import Fraction as F
from math import gcd, lcm

from major_arc_kernel import _factorization, _mobius_phi
from unexceptional_vaughan_gate import _add, _clean, _divisors, _positive


def _validate(cutoff, modulus, residue):
    _positive(cutoff, "cutoff")
    _positive(modulus, "modulus")
    if type(residue) is not int:
        raise ValueError("residue must be an integer")


def cutoff_progression_density_log_vector(cutoff, modulus, residue):
    """Exact sum mu(d) log(R/d)/lcm(d,q) over compatible d<=R."""
    _validate(cutoff, modulus, residue)
    result = {}
    for d in range(1, cutoff + 1):
        if residue % gcd(d, modulus):
            continue
        weight = F(_mobius_phi(d)[0], lcm(d, modulus))
        _add(result, _factorization(cutoff), weight)
        _add(result, _factorization(d), -weight)
    return _clean(result)


def grouped_cutoff_progression_density_log_vector(cutoff, modulus, residue):
    """Split d=h*b, h|rad(gcd(q,r)), (b,q)=1; retain real cutoff R/h."""
    _validate(cutoff, modulus, residue)
    result = {}
    for h in _divisors(gcd(modulus, residue)):
        mu_h = _mobius_phi(h)[0]
        if not mu_h:
            continue
        for b in range(1, cutoff // h + 1):
            if gcd(b, modulus) != 1:
                continue
            weight = F(mu_h * _mobius_phi(b)[0], modulus * b)
            _add(result, _factorization(cutoff), weight)
            _add(result, _factorization(h * b), -weight)
    return _clean(result)
