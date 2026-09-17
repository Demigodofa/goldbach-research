"""Exact fixtures for the logarithmic-cutoff/Nyman--Beurling dictionary.

Owner: Kevin/Rill research. See notes/rh-mobius-cutoff-transfer.md.
Log-prime vectors check finite identities, not norm convergence or RH.
"""
from fractions import Fraction as F

from major_arc_kernel import _factorization, _mobius_phi
from unexceptional_vaughan_gate import _add, _clean


def _inputs(cutoff, y):
    if type(cutoff) is not int or cutoff < 2:
        raise ValueError('integer cutoff >=2 required')
    if type(y) not in (int, F) or y <= 0:
        raise ValueError('positive exact rational y required')
    return F(y)


def cutoff_log_coefficients(cutoff):
    """The actual a_d=mu(d)log(R/d), as exact log-prime vectors."""
    _inputs(cutoff, 1)
    result = {}
    for d in range(1, cutoff + 1):
        mu = _mobius_phi(d)[0]
        vector = {}
        _add(vector, _factorization(cutoff), mu)
        _add(vector, _factorization(d), -mu)
        if vector := _clean(vector):
            result[d] = vector
    return result


def harmonic_coefficient(cutoff):
    """c_R=sum a_d/d, not normalized by log R."""
    result = {}
    for d, vector in cutoff_log_coefficients(cutoff).items():
        _add(result, vector, F(1, d))
    return _clean(result)


def residual_numerator(cutoff, y):
    """Direct fractional-parts formula for log(R)*e_R(1/y)."""
    y = _inputs(cutoff, y)
    result = {}
    if y > 1:
        _add(result, _factorization(cutoff))
    for d, vector in cutoff_log_coefficients(cutoff).items():
        q = y / d
        _add(result, vector, q - q.numerator // q.denominator)
    return _clean(result)


def prefix_residual_numerator(cutoff, y):
    """Same numerator from c_R and the cutoff summatory function."""
    y = _inputs(cutoff, y)
    result = {}
    if y > 1:
        _add(result, _factorization(cutoff))
    _add(result, harmonic_coefficient(cutoff), y)
    for d, vector in cutoff_log_coefficients(cutoff).items():
        _add(result, vector, -(y // d))
    return _clean(result)


def bulk_residual_numerator(cutoff, y):
    """For 1<y<=R only: y*c_R-psi(y), including proper prime powers."""
    y = _inputs(cutoff, y)
    if not 1 < y <= cutoff:
        raise ValueError('bulk identity requires 1<y<=cutoff')
    result = {}
    _add(result, harmonic_coefficient(cutoff), y)
    for m in range(2, int(y) + 1):
        factors = _factorization(m)
        if len(factors) == 1:
            _add(result, ((factors[0][0], 1),), -1)
    return _clean(result)


def far_tail_log_squared_cap(cutoff, y):
    """Rational cap for log(R)^2 times the norm tail beyond y>=R.

    The analytic inequality is proved in the note; this computes 4R^2/y.
    """
    y = _inputs(cutoff, y)
    if y < cutoff:
        raise ValueError('tail cutoff must be at least R')
    return F(4 * cutoff**2, 1) / y
