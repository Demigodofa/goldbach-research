"""Exact rational DHR comparison for the raw Goldbach presieve bound.

Owner: Kevin's mathematical investigation; derivation and verifier: Rill.
Purpose: check which fixed-power cutoffs the proved comparison excludes.
Scope: asymptotic N through powers of two; no numerical onset, no Goldbach
counterexample, and no claim of external novelty. Independently reviewed
by the existing Sol mathematical reviewer on 2026-09-08.

The DHR ODEs imply t**2 F_2(t) >= 8 exp(2 gamma) globally. For beta_2 <= b
and b < u <= 6, integration gives
  f_2(u) >= 16 exp(2 gamma)/u**2 * I,
  I = log((u-1)/(b-1)) + 1/(b-1) - 1/(u-1).
Use log(x) >= 2(x-1)/(x+1), x>=1. Its difference has derivative
(x-1)**2 / (x*(x+1)**2) >= 0 and vanishes at x=1.

With z=N**(1/u), ordinary both-z-rough odd pairs are a subset of the
square-start survivors M_z. DHR at D_M=N/log**11 N gives
M_z >= (N/2)*V_2(z)*(f_2(u)-o(1)): the weighted remainder is bounded by
sum_{d<=D_M} 8**omega(d) <= sum d_8(d) <= D_M*(1+log D_M)**7.
For the leading-prime count Q_z, linear DHR and weighted BV give
Q_z <= Li(N)*V_1(z)*(F_1(u/2)+o(1)) + pi(z) + O(1).
Weighted BV follows from Cauchy: sum 4**omega(d)*E_d is at most
(sum E_d)**(1/2)*(3N*sum 16**omega(d)/phi(d))**(1/2).
The second divisor sum is O(log**16 N); ordinary BV with saving 24
therefore gives O(N/log**4 N) at its corresponding level.
Since V_2/V_1 ~ 2 exp(-gamma)/log z and F_1(u/2)=4 exp(gamma)/u,
limsup 2Q_z/M_z <= 1/(2I). The exact combinatorial R_z<=2Q_z-M_z
then gives the rational upper bound computed below. Continuity absorbs
the logarithmic reductions in the two sieve levels.

Sources (read, not inferred from decimal approximations):
* DHR ODEs: Kao, section 4, https://arxiv.org/html/1606.03505v1
* DHR upper/lower bounds with weighted remainders: Franze-Kao, section 4,
  equations (19)-(20), https://arxiv.org/pdf/1812.11280
* Certified beta interval: Booker-Browning ancillary table, final table
  and explicit truncation rule, https://arxiv.org/src/1511.00601v2/anc/dhr.html
  Rigorous interval method: https://arxiv.org/pdf/1511.00601 section 5.2.6.
* Ordinary BV: Ford, Theorem 3.4, https://ford126.web.illinois.edu/sieve2023.pdf
The decimal display in Kao alone was NOT used as a certified interval.
"""
from fractions import Fraction


BETA_LOWER = Fraction("4.26645028414864191641")
BETA_UPPER = BETA_LOWER + Fraction(1, 10**20)


def raw_limsup_upper(u: Fraction, b: Fraction = Fraction(43, 10)) -> Fraction:
    """Proved upper bound for limsup R_z/M_z, z=N**(1/u), N powers of 2.

    A nonnegative result supplies no eventual-failure conclusion. It is
    never a bound for a particular finite N.
    """
    if (not isinstance(u, Fraction) or not isinstance(b, Fraction)
            or not BETA_UPPER <= b < u <= 6):
        raise ValueError("exact fractions with certified beta_upper<=b<u<=6 required")
    x = (u-1)/(b-1)
    integral_lower = 2*(x-1)/(x+1) + 1/(b-1) - 1/(u-1)
    return 1/(2*integral_lower)-1


if __name__ == "__main__":
    for u in (Fraction(6), Fraction(119, 20)):
        print(f"z=N^({1/u}): limsup R_z/M_z <= {raw_limsup_upper(u)}")
