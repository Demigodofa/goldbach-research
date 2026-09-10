"""Exact complement expansion for the signed short-divisor coefficient.

For n>1, a_B(n)=-sum_{d|n,d>B}mu(d).  Partitioning every squarefree
omitted d by its unique largest prime gives a canonical boundary expansion,
but it moves the reflected modulus d*m strictly above exponent .599 and
does not remove the signs.  This gates one proposed factorability route;
it does not rule out cancellation among the boundary terms.
"""
from fractions import Fraction as F

from large_prime_switching_gate import divisors, short_divisor_weight
from major_arc_kernel import _factorization, _mobius_phi


def complement_weight(n, cutoff):
    if not isinstance(n, int) or n <= 1:
        raise ValueError("require composite-or-prime n>1")
    if not isinstance(cutoff, int) or cutoff < 1:
        raise ValueError("positive cutoff required")
    return -sum(_mobius_phi(d)[0] for d in divisors(n) if d > cutoff)


def largest_prime_boundary_terms(n, cutoff):
    """Terms (largest prime p, remaining e, mu(e)) in the complement."""
    if not isinstance(n, int) or n <= 1:
        raise ValueError("require n>1")
    if not isinstance(cutoff, int) or cutoff < 1:
        raise ValueError("positive cutoff required")
    terms = []
    for d in divisors(n):
        mu = _mobius_phi(d)[0]
        if d <= cutoff or mu == 0:
            continue
        factors = _factorization(d)
        p = factors[-1][0]
        e = d // p
        terms.append((p, e, _mobius_phi(e)[0]))  # -mu(ep)=mu(e)
    return tuple(terms)


def boundary_term_sum(n, cutoff):
    return sum(coefficient for _, _, coefficient
               in largest_prime_boundary_terms(n, cutoff))


def top_core_exponent_gate(core=F(41, 100), short=F(9, 1000)):
    """Exponent consequences for d>B and m~N^(1-core)."""
    if not all(isinstance(x, F) and 0 < x < 1 for x in (core, short)):
        raise ValueError("exact exponents in (0,1) required")
    return {
        "boundary_modulus_exponent_infimum": 1 - core + short,
        "full_boundary_modulus_supremum": F(1),
        "previous_dispersion_power_loss": F(459, 1000) - core,
        "sign_resolved": False,
    }


def verify_complement(n, cutoff):
    """Finite exact guard for both complement presentations."""
    a = short_divisor_weight(n, cutoff)
    c = complement_weight(n, cutoff)
    b = boundary_term_sum(n, cutoff)
    return {"short": a, "complement": c, "partition": b,
            "exact": a == c == b}
