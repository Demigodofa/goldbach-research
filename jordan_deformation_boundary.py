"""Exact guards for the positive Jordan deformation boundary obstruction.

See notes/positive-jordan-deformation-boundary.md. Integer evaluations and
formal log vectors guard identities, not an asymptotic or a Goldbach claim.
"""
from fractions import Fraction as F
from math import prod

from complementary_divisor_correlation import central_interval
from major_arc_kernel import _factorization, _mobius_phi
from unexceptional_vaughan_gate import _add, _clean, _divisors, _positive


def jordan_integer(n, order):
    """Evaluate J_k(n) exactly for positive integer k, including n=1."""
    _positive(n, 'n')
    _positive(order, 'integer order')
    return prod(p**((a-1)*order)*(p**order-1)
                for p, a in _factorization(n))


def jordan_linear_log_vector(n):
    """Differentiate the full Mobius divisor sum at s=0, in log primes."""
    _positive(n, 'n')
    vector = {}
    for d in _divisors(n):
        _add(vector, _factorization(n//d), _mobius_phi(d)[0])
    return _clean(vector)


def local_pair_factor(prime, target, t):
    """Exact local mean when t represents p**(-s); rational algebra only."""
    if (type(prime) is not int or prime < 2
            or _factorization(prime) != ((prime, 1),)):
        raise ValueError('prime modulus required')
    if type(target) is not int or target < 0:
        raise ValueError('nonnegative integer target required')
    if type(t) is not F or not 0 <= t <= 1:
        raise ValueError('exact Fraction t in [0,1] required')
    return 1 - 2*t/prime + (t*t/prime if target % prime == 0 else 0)


def pair_vanishing_order(target, *, omit_prime_powers=False):
    """Order at s=0 of the actual unnormalized central J_s pair sum.

    None means the masked finite sum is empty, not a Goldbach certificate.
    Omitting prime powers on either side retains only omega(n)>=2 on both.
    The positive leading coefficients prevent cancellation of minimum order.
    """
    if type(omit_prime_powers) is not bool:
        raise ValueError('omit_prime_powers must be boolean')
    orders = []
    for n in central_interval(target):
        left, right = len(_factorization(n)), len(_factorization(target-n))
        if omit_prime_powers and (left == 1 or right == 1):
            continue
        orders.append(left+right)
    return min(orders) if orders else None
