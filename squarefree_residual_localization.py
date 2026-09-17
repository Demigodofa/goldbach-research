"""Exact fixtures for signed squarefree-pair localization.

Owner: Goldbach research. See notes/squarefree-residual-localization.md for
the analytical estimate. These helpers check identities, not asymptotics.
"""

from fractions import Fraction as F
from math import gcd, lcm

from cutoff_normalized_remainder import singular_multiplier
from major_arc_kernel import _factorization, _mobius_phi
from nonunit_residual_localization import excluded_cutoff_log_vector
from unexceptional_vaughan_gate import _add, _clean, _divisors, _positive


def square_block_parameters(target, left, right):
    """Return (period, excluded, left_support, right_support), or None.

    The block has left^2|n and right^2|(target-n), with squarefree indices.
    Support records exactly which primes of excluded divide each argument.
    """
    for value, name in ((target, "target"), (left, "left"), (right, "right")):
        _positive(value, name)
    if not _mobius_phi(left)[0] or not _mobius_phi(right)[0]:
        raise ValueError("squarefree square-divisor indices required")
    if target % gcd(left, right) ** 2:
        return None
    excluded = lcm(left, right)
    return (excluded ** 2, excluded, lcm(left, gcd(right, target)),
            lcm(right, gcd(left, target)))


def square_block_cutoff_vectors(target, n, cutoff, left, right):
    """Alternating excluded-prime expansions of both A_R values on a block."""
    _positive(n, "n")
    _positive(cutoff, "cutoff")
    parameters = square_block_parameters(target, left, right)
    if parameters is None or n >= target or n % left ** 2 or (target - n) % right ** 2:
        raise ValueError("argument does not belong to the square-divisibility block")
    _, excluded, support_left, support_right = parameters
    result = []
    for argument, support in ((n, support_left), (target - n, support_right)):
        vector = {}
        for h in _divisors(support):
            _add(vector, excluded_cutoff_log_vector(argument, cutoff, excluded, h),
                 _mobius_phi(h)[0])
        result.append(_clean(vector))
    return tuple(result)


def excluded_pair_main_blocks(target, excluded):
    """Euler main blocks normalized by 2*C_2; excluded need NOT divide target."""
    _positive(target, "target")
    _positive(excluded, "excluded")
    return {
        c: F(excluded, _mobius_phi(excluded)[1])
        * F(_mobius_phi(c)[0] ** 2, _mobius_phi(c)[1])
        * singular_multiplier(c * excluded)
        for c in _divisors(target) if gcd(c, excluded) == 1
    }


def complementary_cutoff_log_vector(n, cutoff):
    """W_R(n)=sum_(k|n,R*k<n)mu(k)log(n/(R*k)).

    Defined also for nonsquarefree n, but D_R(n)=-mu(n)*W_R(n) holds only
    for squarefree n>1. The strict cutoff has zero weight at equality.
    """
    _positive(n, "n")
    _positive(cutoff, "cutoff")
    if n == 1:
        raise ValueError("require n>1")
    result = {}
    for k in _divisors(n):
        if cutoff * k >= n:
            continue
        mu = _mobius_phi(k)[0]
        _add(result, _factorization(n), mu)
        _add(result, _factorization(cutoff * k), -mu)
    return _clean(result)
