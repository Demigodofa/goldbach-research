"""Exact phase collapse and surviving Parseval cost on aligned endpoints.

Owner: Kevin's Goldbach research.  Purpose: test whether the physical
q-aligned cofactor endpoints by themselves remove the long-block collision.
They do not, although they expose a better arithmetic coordinate system.

Let q=d*m, with m prime and mbar the inverse of m modulo d.  After expanding
d|n, one physical cofactor block has a common integer index l and partner

    p=q*l+r                         (conjugated),
    p=N-q*l+r                       (reflected).             (1)

For the exact full-minus-low kernel

    K_h(p)=e_q(-h*p)+(m-1)^(-1)e_d(-h*mbar*p),              (2)

both phases lose l identically.  In the first form they depend only on r; in
the second they depend only on N+r.  Any separate target phase is common in l
and remains explicit.  Thus the dense fractions h/m should not be treated as
unrelated length-N exponentials before this alignment is used.

ALIGNMENT ALONE DOES NOT PAY THE COLLISION.
For arbitrary arithmetic values c_(l,r), put

    F_q(r)=sum_(l in L)c_(l,r),
    Fhat_q(h)=sum_(r mod q)F_q(r)e_q(-h*r).                 (3)

Full Parseval and Cauchy in the K=|L| progression indices give exactly

    sum_(h mod q)|Fhat_q(h)|^2
       =q*sum_r|F_q(r)|^2
       <=q*K*sum_(r,l)|c_(l,r)|^2.                         (4)

If the physical block has length Y=q*K and coefficient square mass
Y*N^o(1), (4) is Y^2*N^o(1), the same collision term already isolated in
``mobius_covariance_dyadic_scale_gate.py``.  The low-projector term in (2)
changes only a constant in this power count.  Hence every surviving long block
Y=N^y, y>1499/2000, still exceeds the N^(1499/1000) target under purely
algebraic Parseval/Cauchy.

Disposition: changed-under-evidence.  Endpoint alignment removes arbitrary
selector freedom and reexpresses the problem as active Fourier energy of
signed progression sums F_q(r), but it supplies no H gain.  A new arithmetic
estimate must act on those progression sums before Cauchy; formal phase
collapse is not the missing signed prime-correlation estimate.
"""

from fractions import Fraction as F


def aligned_phase_receipt(d, m, h, ell, shift, target=0, reflected=False):
    """Verify (1)-(2) at the level of exact exponent numerators."""
    values = (d, m, h, ell, shift, target)
    if any(type(value) is not int for value in values) or d < 1 or m < 2:
        raise ValueError("integer data with positive moduli required")
    from math import gcd
    if gcd(d, m) != 1:
        raise ValueError("d and m must be coprime")
    q = d * m
    mbar = 0 if d == 1 else pow(m, -1, d)
    partner = target - q * ell + shift if reflected else q * ell + shift
    reduced_argument = target + shift if reflected else shift
    return {
        "q": q,
        "partner": partner,
        "full_numerator": (-h * partner) % q,
        "collapsed_full_numerator": (-h * reduced_argument) % q,
        "low_numerator": 0 if d == 1 else (-h * mbar * partner) % d,
        "collapsed_low_numerator": (
            0 if d == 1 else (-h * mbar * reduced_argument) % d),
        "long_index_removed": (
            (-h * partner) % q == (-h * reduced_argument) % q
            and (d == 1 or (-h * mbar * partner) % d
                 == (-h * mbar * reduced_argument) % d)),
    }


def aligned_parseval_budget(block_exponent):
    """Power ledger for (4), rejecting floats and retaining the open target."""
    if type(block_exponent) is not F or not 0 < block_exponent <= 1:
        raise ValueError("exact block exponent in (0,1] required")
    target = F(1499, 1000)
    collision = 2 * block_exponent
    return {
        "block_exponent": block_exponent,
        "collision_exponent": collision,
        "target_exponent": target,
        "fits_target_by_parseval": collision <= target,
        "critical_block_exponent": F(1499, 2000),
        "alignment_removes_collision": False,
        "arithmetic_progression_estimate_needed": collision > target,
    }
