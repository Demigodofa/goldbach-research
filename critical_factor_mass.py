"""Actual mass on a shrinking critical factor region; conditional prime test.

Owner: Kevin's Goldbach research. Purpose: replace an inapplicable pointwise
boundedness condition by a proved joint arithmetic upper bound, and identify
the exact additional signed estimate. This does NOT prove that estimate.

1. Use a,b,w,I,N=2x,L and B_P from prime_producing_comparison_gate.py.
   Fix 0<e<=1/100 and set
    gamma=1/2-e, theta=e, nu=1/3-2e, P_e=(gamma,theta,nu).
   Let R consist of finite positive vectors with sum1, all coordinates
   <1-gamma, and no proper subsum in [theta,theta+nu]. C(R) consists
   of their coagulations (partition coordinates into groups and sum).
   Define K_e as composites n in I with v(n) in C(R) and P^-(n)>=n^nu.
   All logarithmic factor coordinates v_i=logp_i/logn count multiplicity.

AN UNCONDITIONAL GEOMETRIC AND ARITHMETIC UPPER BOUND.
2. The following broad envelope contains K_e. Its semiprimes have their
   smaller factor coordinate in one of
    [1/3-4e,1/3+4e], [1/2-4e,1/2],
   and its triprimes have EVERY coordinate in [1/3-4e,1/3+4e]. There
   are no other factor counts. This is an enclosure, not an equality.
   Proof: an R-coordinate is either <e or >1/3-e. The total of tiny
   coordinates is <e: otherwise the first greedy crossing of e gives
   a forbidden proper subsum in [e,2e). There are exactly2 or3 large
   coordinates. One cannot supply total1 since each is <1/2+e, and
   four already exceed1. With two, each is in (1/2-2e,1/2+e);
   with three, each is in (1/3-e,1/3+2e). In a coagulation with every
   component>=nu, each component must contain a large coordinate since
   the tiny total<e<nu. Two large coordinates yield two final factors
   within 2e of1/2. Three yield three factors within 3e of1/3, or a
   singleton-large group within 3e of1/3 and its complement near2/3.
   A single final group would be prime, excluded from K_e.
3. There is an ABSOLUTE constant C such that, for each such fixed e,
    sum_(n in K_e) a_n <= C e S_2(N)x/L + o(x/L).         (1)
   More quantitatively the proof bounds the envelope by
    C(e+1/L)S_2(N)x/L + O(x^(2/3+4e)L + sqrtx L).
   Constants in this upper bound can be taken independent of e. Its
   sufficiently-large-x threshold can depend on e. No prime-pair
   asymptotic or cancellation is used to prove (1).
4. First remove proper prime powers N-n, of total Lambda mass
   O(sqrtx L). Repeated factors of n cost at most
    L sum_(p>=(x/2)^(1/3-4e))floor(x/p^2)
      <<x^(2/3+4e)L=o(x/L).
   For the remaining squarefree n, fix all but one prime factors and
   call their product M. The remaining prime r lies in (Z/2,Z], Z=x/M.
   For semiprimes fix the smaller factor, so Z>=sqrtx. For triprimes
   fix two factors in the thirds band, so Z>=x^(1/3-8e)>x^(1/4).
   If (M,N)>1 the prime partner q=N-Mr is impossible: a prime factor
   of M divides q, but is at most M<x whereas q>=x.
5. When (M,N)=1, apply an upper sieve to the integer variable r and
   the two forms r,N-Mr. Put D=floor(Z^(1/3)), z=floor(Z^(1/100)).
   Every prime factor of M is greater than z. The forbidden root count
   rho(ell) is1 for ell|N and2 otherwise, including rho(2)=1 since
   N is even and M odd. Thus g(ell)=rho(ell)/ell has a uniform
   dimension2 sieve bound: for odd ell, g(ell)<=2/ell; the prime2
   is a fixed harmless factor. For squarefree d the interval count is
    Z rho(d)/(2d)+O(rho(d)).
   Ford's fundamental lemma (Theorem3.6,2023 notes) supplies bounded
   upper weights at level D and a main bounded by an absolute constant
   times Z product_(ell<=z)(1-rho(ell)/ell). A fixed logD/logz suffices
   for an upper bound; no asymptotic from a fixed sieve parameter is used.
   The remainder is at most sum_(d<=D)2^omega(d)<<D logD. Euler products
   and Mertens give
    product_(ell<=z)(1-rho(ell)/ell) << S_2(N)/(logZ)^2.
   Indeed the odd-prime generic factor 1-2/ell equals
   (1-1/ell)^2*(1-1/(ell-1)^2), and each ell|N replaces it with
   1-1/ell, giving the factor (ell-1)/(ell-2). Extending these latter
   positive factors to all odd ell|N only increases the upper bound.
   Both primes r,q exceed z, so every prime pair survives this sieve.
   Consequently their number is <<S_2(N)Z/log^2 Z, uniformly in N,M.
   Multiplying by Lambda(q)<=log(2x) gives <<S_2(N)x/(ML).
6. A normalized prime-factor band [a,b] is enclosed by
   (x/2)^a<=p<=x^b. Uniform PNT/Mertens on the fixed compact exponent
   interval gives sum_band 1/p <= log(b/a)+O(1/L).
   This is O(e+1/L) for either semiprime band. For the two fixed
   triprime factors the reciprocal-product sum is O((e+1/L)^2).
   Sum the upper bound from step5; discarding ordering and other
   restrictions only increases a nonnegative sum. This proves (1).

WHAT THIS WOULD GIVE WITH THE STILL-MISSING ACTUAL TYPE II INPUT.
7. Assume, ADDITIONALLY, source Type II for P_e: for every sufficiently
   large fixed B required by its decomposition, all complex coefficients
   |alpha_d|<=tau(d)^B and |beta_j|<=tau(j)^B satisfy
    |sum_((x/2)^e<d<=x^(1/3-e),dj in I)alpha_d beta_j w_(dj)|
          <=x/L^B.                                      (II_e)
   Requiring this for every fixed B is a convenient sufficient version.
   Type I with gamma=1/2-e and the source growth bound are already
   unconditional by prime_producing_comparison_gate.py. These parameter
   triples belong to the source's Q0; gamma>theta and nu<1-gamma.
8. Take g(empty)=1 and g=0 otherwise. It belongs to G1 because gamma>
   theta, as stated before source Corollary7.5. Equations7.13-7.14 give
    H(n)=sum_(d|n,d<=n^gamma,P^+(d)<n^nu)mu(d).
   The term d=1 is included. H(p)=1 for primes p. Lemma7.18(a) gives
   H(n)=1_(P^-(n)>=n^nu) on composites with v(n) in C(R).
   The NONSTRICT >= is verified in the PDF text; web extraction had >.
   Proposition7.19 controls the complement of primes and C(R) using
   growth,I,II. Lemma7.21 controls the total H-pairing by I. Hence,
   for any fixed A, (II_e) implies
    sum_(p in I prime)w_p + sum_(n in K_e)w_n=O_(A,e)(x/L^A). (2)
   Neither cited result requires the pointwise divisor bound (4.1).
   The comparison's factor-pattern condition (b.2) is not needed for
   this identity, although it was separately proved and remains useful.
9. Since a,b>=0, (2) and (1) imply
    sum_(p in I prime)a_p
       =B_P-sum_(K_e)a_n+sum_(K_e)b_n+O_(A,e)(x/L^A)
       >=[1-C' e+o_e(1)] B_P,                            (3)
   with an absolute C', using B_P~S_2(N)x/(2L).
   Thus for some sufficiently small fixed e>0, (II_e) would imply
   positive prime-pair mass of order S_2(N)x/L for every sufficiently
   large even N=2x where the hypothesis holds. Remove partner proper
   powers again, at cost O(sqrtx L), to obtain actual two-prime
   representations. No numerical threshold or small-even coverage follows.
   The uncomputed absolute constant suffices for this existential
   conditional criterion; it does not specify a certified numerical e.

DISPOSITION.
The actual narrow-region upper bound (1) and conditional implication
(II_e)=>(3) are new-to-this-task proved components. This replaces an
inapplicable pointwise boundedness hypothesis with available arithmetic.
It does not prove (II_e), weaken its coefficients, or transfer the existing
factored-modulus theorem to it. No ordering is asserted between (II_e)
and the older balanced correlation hypotheses. The corrected artificial
counterexample in prime_producing_comparison_gate.py lacks (1), so there
is no contradiction. Exceptional-character effects still matter when
attempting an actual estimate; a uniform uncorrected asymptotic has not
been obtained. No new unconditional Goldbach coverage.

Primary sources read2026-09-09: Ford--Maynard, author PDF July16,2024,
Definitions4.3,7.2; eq6.1,7.12-7.14; remark before Cor7.5; Lemmas7.18,
7.21 and Prop7.19 (printedpp51-53). These are the decomposition inputs,
not a direct application of its divisor-bounded Theorem2.5.
https://www.ford126.web.illinois.edu/wwwpapers/prime-producing-sieves.pdf
Ford, Sieve Methods2023, Theorem3.6 (printedp38), upper sieve input:
https://ford126.web.illinois.edu/sieve2023.pdf

Finite guards below check region geometry and local roots, not (II_e).
"""
from fractions import Fraction as F
from itertools import combinations
from math import gcd

from redistribution import trial_prime


def critical_bands(e):
    """Closed rational envelope, with an exact permissible parameter guard."""
    if type(e) not in (int, F) or not 0 < e <= F(1, 100):
        raise ValueError('require rational 0<e<=1/100')
    return (F(1, 3)-4*e, F(1, 3)+4*e), (F(1, 2)-4*e, F(1, 2))


def in_residual_region(vector, e):
    """Exact R(P_e) membership for a finite rational vector."""
    critical_bands(e)
    if (not vector or any(type(t) not in (int, F) or t <= 0 for t in vector)
            or sum(vector) != 1):
        raise ValueError('require a positive rational vector summing to one')
    if max(vector) >= F(1, 2)+e:
        return False
    return all(not e <= sum(s) <= F(1, 3)-e
               for size in range(1, len(vector)) for s in combinations(vector, size))


def affine_pair_root_density(target, multiplier, prime):
    """Exact local roots for the two forms with coprime coefficients."""
    if (any(type(v) is not int or v <= 0 for v in (target, multiplier, prime))
            or target % 2 or gcd(target, multiplier) != 1 or not trial_prime(prime)):
        raise ValueError('require even positive target, coprime multiplier, prime modulus')
    roots = sum(r*(target-multiplier*r) % prime == 0 for r in range(prime))
    predicted = 1 if target*multiplier % prime == 0 else 2
    return F(roots, prime), F(predicted, prime)
