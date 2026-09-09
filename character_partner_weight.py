"""Exact character divisor weight and the remaining composite correlation.

Owner: Kevin's research. Purpose: replace the two surviving factor classes
by a precise weighted prime-pair reduction, with exact algebra controls.
This uses a standard weight, not a historical novelty claim. The source is
Matomaki--Merikoski, Section2, equations (9)-(10):
https://arxiv.org/html/2112.11412v2#S2
Writing lambda=1*chi and W=chi*log, Dirichlet convolution gives
  W=lambda*Lambda >= Lambda >=0.                         (1)
Sol checked the deduction and actual files. Five focused exact tests passed
normally and with Python -O. These algebra tests do not prove asymptotic
positivity or detect an exceptional zero.

Exact support for unit n with chi(n)=-1:
Let J be the set of negative-sign prime factors with ODD exponent in n.
Its cardinality is odd. If |J|>=3, then W(n)=0. If J={r} and the
exponent of r is 2b+1, then
  W(n)=(b+1)*prod_{q|n, chi(q)=+1}(v_q(n)+1)*log(r).     (2)
Indeed lambda(q^a)=a+1 for a positive-sign prime and equals1 or0 for a
negative-sign prime according as a is even or odd. In lambda*Lambda only
one prime power can be removed. With several odd negative exponents some
zero local factor always remains. With exactly one, only powers r^j with
j odd contribute, giving b+1 identical local products. Thus for SQUAREFREE
n, W(n) is nonzero exactly when there is one negative prime r; its value
is 2^omega_+(n)*log(r). Negative primes have weight log(n); squarefree
composites composed entirely of negative primes have weight zero.

An exact smaller-divisor representation also holds:
  W(n)=sum_{d|n, d<sqrt(n)} chi(d)*log(n/d^2).            (3)
Pair d with n/d in chi*log and use chi(n/d)=-chi(d).
There is no diagonal: a unit square cannot have character sign-1.
The summands in (3) are signed although W itself is nonnegative. Merely
truncating the divisor sum does not produce a lower bound.

Conditional reduction, with ALL hypotheses of rare_factor_pruning.py:
Retain Y,D,delta,u,beta,t,m,J_m,E,z,w and the pruned pool B_good of actual
positive-sign primes p. Their partners n=m-p are units, have all prime
factors>z, and have no positive-sign prime factor<=w. Define
  T(m)=sum_{p in B_good}log(p)*W(m-p),
  P(m)=sum_{p,n in J_m, p+n=m, both prime, chi(p)=+1}log(p)*log(n).
Equivalently use p,n in I=(Y/2,Y] in the definition of P; the reflection
condition puts both in J_m. For sufficiently large Y all pairs in P
belong to B_good. In the suppressed class, the other prime has sign-1.
We have the EXACT nonnegative decomposition
  T(m)=P(m)+E_large_sf(m)+E_sq(m).                       (4)
Here E_large_sf sums precisely over squarefree composite partners with
one negative-sign prime r and h>=1 positive-sign primes, all>w. Each
contributes 2^h*log(p)*log(r). E_sq sums log(p)*W(n) over partners
divisible by a prime square.

The repeated-factor term is negligible on the rare-prime scale:
  0<=E_sq(m)<=Y^(1-delta/u+o(1))
             =o_A(Y*t/log(Y)^A)                         (5)
for EVERY fixed A, uniformly in the stated regime, with ineffective onset.
To see this, each partner n determines at most one p=m-n. If n is
z-rough and has a prime-square divisor q^2, then q>z, so their number is
at most sum_{q>z}floor(Y/q^2)<=Y/(z-1), even when summing over all integers
q instead of primes. From (1), or its divisor formula, W(n)<=tau(n)*log(n).
Both logarithmic weights and the uniform divisor bound are Y^o(1), and
z>=Y^(delta/u). The existing Siegel bound gives t>>_h Y^(-h) for every
fixed h>0, which absorbs the fixed power saving and every fixed logarithm.
There is no multiplicity loss from different first primes for the same n.

What this does and does not reduce:
The all-negative odd-composite class disappears from (4), apart from its
negligible repeated-factor contribution. The remaining squarefree error contains
at least one large positive-sign factor. This is a change of weight, not a
claim that these zero-weight partners have left the original candidate pool.
The proved lower bound for |B_good| DOES NOT give T>0: W can vanish on
composites. Neither a positive main term for T nor a small bound for
E_large_sf is proved here. Both are needed to infer P>0 from (4)-(5).
Also P is the positive-sign-first ordered part, one half of the full
ordered weighted prime-pair count in this reflection-invariant interval.
No prime-pair coverage, P_2 conclusion, numerical onset or actual zero follows.
"""
from math import isqrt

from exceptional_character_model import character_values
from major_arc_kernel import _factorization


def _negative_character(n: int, conductor: int, two_sign: int) -> tuple[int, ...]:
    if type(n) is not int or n < 2:
        raise ValueError("n must be an integer >=2")
    chi = character_values(conductor, two_sign=two_sign)
    if chi[n % conductor] != -1:
        raise ValueError("n must be a unit of character sign-1")
    return chi


def negative_log_coefficients(n: int, conductor: int, *, two_sign: int = 1
                              ) -> tuple[tuple[int, int], ...]:
    """Return exact (prime, coefficient) pairs for W(n)=sum coefficient*log(prime).

    Requires a primitive quadratic character and chi(n)=-1. The result is
    empty or has one positive integer coefficient. Repeated prime factors
    count with multiplicity. No floating logarithm is evaluated.
    """
    chi = _negative_character(n, conductor, two_sign)
    factors = _factorization(n)
    odd_negative = [(p, a) for p, a in factors if chi[p % conductor] == -1 and a % 2]
    if len(odd_negative) != 1:
        return ()
    prime, exponent = odd_negative[0]
    coefficient = (exponent+1)//2
    for q, a in factors:
        if chi[q % conductor] == 1:
            coefficient *= a+1
    return ((prime, coefficient),)


def negative_hyperbola_terms(n: int, conductor: int, *, two_sign: int = 1
                             ) -> tuple[tuple[int, int], ...]:
    """Return (d, sign) for the exact sum sign*log(n/d^2), d|n and d<sqrt(n).

    These terms may be negative; partial sums are not certified lower bounds.
    Intended for small exact verification, with no speed or analytic claim.
    """
    chi = _negative_character(n, conductor, two_sign)
    return tuple((d, chi[d % conductor]) for d in range(1, isqrt(n)+1)
                 if n % d == 0 and d*d < n)
