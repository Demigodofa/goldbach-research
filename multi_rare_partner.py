"""Bound the part of the character partner weight with several rare factors.

Owner: Kevin's research. Purpose: reduce the remaining squarefree composite
error to a semiprime correlation, preserving the existing rare-prime scale.
The helpers check exact local factors, Euler tails and the factor partition.
They do not detect an exceptional zero or supply asymptotic thresholds.
Sol checked theory and actual files. Five focused exact tests passed
normally and with Python -O; these tests verify finite algebra only.

Deduction independently checked by Sol:
Keep ALL hypotheses and notation of character_partner_weight.py, including
the actual exceptional zero, 0<t<=1/log(Y), D<=Y^(delta/4), the suppressed
target m, and the pruned pool. Split its E_large_sf into E_1+E_2plus by
the number h of positive-sign prime factors. Then
  0<=E_2plus(m)<<_{delta,u} Y*S_2(m)*t^2=o(Y*t).          (1)
Thus, writing P for the positive-first actual weighted prime-pair count,
  T(m)=P(m)+E_1(m)+E_rem(m), E_rem>=0,
  E_rem<<Y*S_2(m)*t^2+Y^(1-delta/u+o(1))=o(Y*t).        (2)
E_1 is exactly twice the sum of log(p)*log(r) over the remaining partners
n=r*q, where r is a negative-sign prime>z and q a positive-sign prime>w.
Here p=m-r*q is an actual positive-sign prime in the original interval.
Neither a positive lower bound for T nor control of E_1 is proved.
All constants/onsets remain ineffective and delta,u are fixed, not numerical.

Large-prime rarity with exact cutoffs:
1. Put a=w+1, E=floor(Y^delta), w=floor(sqrt(E)). For any real x>=0,
   floor(sqrt(floor(x)))=floor(sqrt(x)); hence a>Y^(delta/2)>=D^2.
   Let H=sum_{w<q<=Y, q prime, chi(q)=+1}1/q. Apply Matomaki--Merikoski
   Lemma2.2 with cutoff a, v=log(a)/log(D)>=2, upper endpoint Y, and
   eta=1/((1-beta)*log(D)). Its P(a) contains primes strictly below a,
   so the possible endpoint q=a is included. Since lambda(q)=2, it gives
     H<<_delta eta^(-1)+t+1/a <<_delta t.                (3)
   Indeed log(Y)/log(a)<=2/delta, the source's middle term is exactly t,
   eta^(-1)=t*log(D)/log(Y)<=delta*t/4, and Siegel makes 1/a=o(t).
   Source: https://arxiv.org/html/2112.11412v2#S2
   This uses the existing LARGE cutoff w; it does not improve the earlier
   small-factor bound to O(t).

Uniform bound after fixing the positive factors:
2. Each squarefree partner counted by E_2plus has the UNIQUE form n=r*M,
   with r its only negative-sign prime and M the product of h>=2 distinct
   positive-sign primes>w. Thus M<=Y/z and r lies in (Y/(2M),Y/M]. If
   gcd(M,m)>1, an actual p=m-M*r would be divisible by a prime factor of
   M<Y/2<p, impossible. It suffices to treat gcd(M,m)=1.
3. Apply Henriot's NEW Theorem5 from the 2014 erratum DIRECTLY. Take
     Q1(v)=v, Q2(v)=m-M*v, x=y=Y/(2M),
     F(v1,v2)=1_(all prime factors of v1 and v2 exceed z).
   Both polynomials are primitive, their product has degree2 and coefficient
   norm m+M<=3Y. Also x>=z/2>=Y^(delta/u)/2. Choose alpha=1/2, norm
   exponent eta0=delta/(2u), and any fixed
     0<epsilon<alpha/(50*2*(2+1/eta0)).
   Then x>=C0*||Q1*Q2||^eta0 eventually UNIFORMLY in M. The function F
   lies in M_2(1,1,epsilon), uniformly in z. Restricting both forms to the
   original intervals only reduces this nonnegative upper bound.
   Primary source, printed p377, including corrected congruences (0.1)-(0.2):
   https://doi.org/10.1017/S0305004114000280
   Definitions: https://arxiv.org/pdf/1102.1643
   No uncorrected discriminant or leading-coefficient corollary is used.
4. For a prime ell, the root count rho(ell) for v*(m-M*v) is1 if ell|Mm
   and2 otherwise. For ell<=z, the corrected local divisor factor is1.
   For ell>z, sum all nonzero exact-valuation tuples: they partition the
   event ell|v*(m-M*v), so the factor is 1+rho(ell)/ell. This includes
   ell|M, when the second form has no root. The all-zero tuple contributes1.
   Dropping the divisor-product limit and extending valuations is allowed
   by nonnegativity. For ell>max(2,z), the combined local factor is
     (1-rho(ell)/ell)*(1+rho(ell)/ell)<=1.
   Below z, M has no prime factor, so the remaining sieve product is
     <<S_2(m)/log(min(z,x))^2 <<_{delta,u} S_2(m)/log(Y)^2.
   Here x>=z/2; omitting ell<=degree2 only changes an absolute constant.
   Thus, uniformly over the admissible M,
     #{r: r and m-M*r are the required primes}
       <<_{delta,u} (Y/M)*S_2(m)/log(Y)^2.               (4)
   No independence or rare-character distribution of these two primes is
   asserted; both character restrictions may be dropped in this upper bound.

Summing the positive factors:
5. Each contribution to E_2plus is 2^h*log(p)*log(r)<=2^h*log(Y)^2.
   Sum (4), and only THEN drop M<=Y/z from the positive upper bound:
     sum_{M squarefree, omega(M)>=2, q|M => w<q<=Y, chi(q)=+1} 2^omega(M)/M
       <=prod_{w<q<=Y, chi(q)=+1}(1+2/q)-1-2*H
       <=exp(2*H)-1-2*H <=2*H^2*exp(2*H).
   The prime product is finite; each M occurs once, without a permutation
   factor. Equations (3)-(4) prove the first bound in (1). Since
   S_2(m)<<loglog(Y) and t<=1/log(Y), it is o(Y*t) uniformly. This is not
   a saving of every logarithmic power. Combining with the earlier
   repeated-factor estimate proves (2). The unresolved semiprime term
   contains two rare-sign primes, p and q, in the equation p+r*q=m.
   Finite sign assignments do not assert that the character has a real zero,
   and no new Goldbach coverage or P_2 theorem follows from this reduction.
"""
from fractions import Fraction as F
from math import gcd, isqrt, prod

from exceptional_character_model import character_values
from major_arc_kernel import _factorization


def _is_prime(value: int) -> bool:
    return type(value) is int and value >= 2 and all(value % d for d in range(2, isqrt(value)+1))


def affine_local_factor(prime: int, cofactor: int, target: int, cutoff: int
                        ) -> tuple[int, F, F]:
    """Return (root count, corrected divisor factor, combined sieve factor).

    For v and target-cofactor*v; require a positive even target, a positive
    cofactor coprime to it, and all cofactor prime factors>cutoff>=2. The
    prime2 factor is returned algebraically, although New Theorem5 omits it.
    """
    if not _is_prime(prime):
        raise ValueError("prime must be prime")
    if any(type(v) is not int for v in (cofactor, target, cutoff)):
        raise ValueError("cofactor, target and cutoff must be integers")
    if cofactor < 1 or target < 2 or target % 2 or cutoff < 2:
        raise ValueError("require cofactor>=1, positive even target and cutoff>=2")
    if gcd(cofactor, target) != 1 or any(q <= cutoff for q, _ in _factorization(cofactor)):
        raise ValueError("cofactor must be coprime to target and have no small prime factors")
    roots = 1 if (cofactor*target) % prime == 0 else 2
    divisor_factor = F(1) if prime <= cutoff else 1+F(roots, prime)
    return roots, divisor_factor, (1-F(roots, prime))*divisor_factor


def rare_product_tail(primes: tuple[int, ...]) -> tuple[F, F]:
    """Return H=sum 1/q and the exact weight-2 squarefree Euler tail of degree>=2.

    The input is a distinct finite prime tuple; this helper does not assert
    character signs or rarity. The tail excludes the empty and singleton terms.
    """
    if type(primes) is not tuple or any(not _is_prime(q) for q in primes):
        raise ValueError("input must be a tuple of primes")
    if len(set(primes)) != len(primes):
        raise ValueError("primes must be distinct")
    harmonic = sum((F(1, q) for q in primes), F(0))
    tail = prod((1+F(2, q) for q in primes), start=F(1))-1-2*harmonic
    return harmonic, tail


def split_squarefree_partner(partner: int, conductor: int, cutoff: int, bound: int, *,
                             two_sign: int = 1) -> tuple[int, int, int, int] | None:
    """Return (negative prime r, positive product M, h, weight 2^h), or None.

    Requires a squarefree sign- unit with all factors>cutoff and all sign+
    factors>bound>=cutoff. None means zero W weight (several sign- primes).
    A prime partner is allowed and returns M=1,h=0,weight1.
    """
    if any(type(v) is not int for v in (partner, cutoff, bound)):
        raise ValueError("partner, cutoff and bound must be integers")
    if partner < 2 or cutoff < 2 or bound < cutoff:
        raise ValueError("require partner>=2 and 2<=cutoff<=bound")
    chi = character_values(conductor, two_sign=two_sign)
    if chi[partner % conductor] != -1:
        raise ValueError("partner must be a unit of character sign-1")
    factors = _factorization(partner)
    if any(a != 1 or q <= cutoff or (chi[q % conductor] == 1 and q <= bound)
           for q, a in factors):
        raise ValueError("partner must be squarefree and satisfy both prime-factor cutoffs")
    negative = [q for q, _ in factors if chi[q % conductor] == -1]
    if len(negative) != 1:
        return None
    h = len(factors)-1
    return negative[0], partner//negative[0], h, 2**h
