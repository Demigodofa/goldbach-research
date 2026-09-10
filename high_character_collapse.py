"""Collapse the whole high prime-character family before Cauchy.

This is an exact finite identity for the high-conductor projector occurring
in ``prime_companion_dispersion.py`` and ``joint_crt_band_form.py``.  Let
q=d*m, where (d,m)=1 and m is prime.  The high family consists of every
character chi_d modulo d paired with every NONPRINCIPAL character chi_m
modulo m.  For reduced p and a,

  1/phi(q) sum_(chi_d) sum_(chi_m != 1) chi(p) conjugate(chi(a))
    = 1_(p=a mod q) - 1/(m-1) 1_(p=a mod d).                 (1)

Thus summing the entire high family is exactly ``full minus low``.  In the
Gauss-transformed form, for c nonzero modulo m,

  sum_(chi_m != 1) chi_m(p) G_m(conjugate(chi_m),c)
    = (m-1)e_m(c*p) + 1.                                   (2)

The first term is an ordinary additive prime phase; the second reconstructs
the subtracted low projector after the d-character sum and target phase are
restored.  No Kloosterman sum or spectral saving is created by (1) or (2).
One may still seek cancellation by averaging the resulting prime additive
Fourier sums jointly over m and the active h~dm/H band.  That would be a new
arithmetic estimate, not a consequence of character orthogonality.

The routines below verify the group-algebra identities exactly.  Additive
roots are represented in the canonical basis of Q(zeta_m); no floating-point
character values are used.  This module proves no signed prime-correlation
bound and leaves endpoint/mask leakage unpaid.
"""
from fractions import Fraction as F
from math import gcd, isqrt


def _prime(value):
    if (type(value) is not int or value < 2
            or any(value % divisor == 0
                   for divisor in range(2, isqrt(value) + 1))):
        raise ValueError("m must be prime")


def _unit(value, modulus, name):
    if type(value) is not int or gcd(value, modulus) != 1:
        raise ValueError(f"{name} must be an integer unit modulo the modulus")


def _primitive_root(prime):
    """Small deterministic primitive root for a prime modulus."""
    _prime(prime)
    order = prime - 1
    factors = []
    remainder = order
    divisor = 2
    while divisor * divisor <= remainder:
        if remainder % divisor == 0:
            factors.append(divisor)
            while remainder % divisor == 0:
                remainder //= divisor
        divisor += 1
    if remainder > 1:
        factors.append(remainder)
    for candidate in range(1, prime):
        if all(pow(candidate, order // factor, prime) != 1
               for factor in factors):
            return candidate
    raise AssertionError("prime multiplicative group has no primitive root")


def _discrete_log_table(prime):
    generator = _primitive_root(prime)
    table = {}
    value = 1
    for exponent in range(prime - 1):
        table[value] = exponent
        value = value * generator % prime
    return table


def nonprincipal_orthogonality(m, p, a):
    """Exact sum over nonprincipal multiplicative characters modulo m.

    The return value is
      sum_(j=1)^(m-2) zeta_(m-1)^(j*(log_g(p)-log_g(a))),
    evaluated as an integer by complete geometric-series orthogonality.
    """
    _prime(m)
    _unit(p, m, "p")
    _unit(a, m, "a")
    logs = _discrete_log_table(m)
    difference = (logs[p % m] - logs[a % m]) % (m - 1)
    return m - 2 if difference == 0 else -1


def _cyclotomic(counts):
    """Canonical degree<m-1 representative modulo 1+X+...+X^(m-1)."""
    return tuple(value - counts[-1] for value in counts[:-1])


def gauss_collapse(m, p, c):
    """Both exact sides of (2), in the canonical zeta_m basis."""
    _prime(m)
    _unit(p, m, "p")
    _unit(c, m, "c")
    direct = [0] * m
    for a in range(1, m):
        direct[c * a % m] += nonprincipal_orthogonality(m, p, a)
    expected = [0] * m
    expected[c * p % m] += m - 1
    expected[0] += 1
    return _cyclotomic(direct), _cyclotomic(expected)


def high_projector(d, m, residue, p):
    """Normalized full-minus-low coefficient in (1), exactly."""
    if type(d) is not int or d < 1:
        raise ValueError("d must be a positive integer")
    _prime(m)
    if gcd(d, m) != 1:
        raise ValueError("d and m must be coprime")
    q = d * m
    _unit(residue, q, "residue")
    _unit(p, q, "p")
    return (F(int((p - residue) % q == 0))
            - F(int((p - residue) % d == 0), m - 1))


def source_target_after_collapse():
    """Record the inference boundary exposed by the exact collapse."""
    return {
        "high_family_equals_full_minus_low": True,
        "prime_component_gauss_collapses": True,
        "ordinary_additive_prime_phase_remains": True,
        "kloosterman_sum_created_by_orthogonality": False,
        "joint_m_h_cancellation_proved": False,
        "endpoint_and_mask_leakage_paid": False,
    }
