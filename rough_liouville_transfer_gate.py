"""Cubic-rough Liouville bias and the still-open prime-partner transfer.

Owner: Kevin's Goldbach research. Purpose: make the proposed signed-parity
input testable and prevent unmasked cancellation from being imported through
a roughness filter. This reuses the saved prime/semiprime partition and
one-dimensional semiprime integral; it is not a new distribution theorem.
Independent Sol theory and actual-file review PASS, 2026-09-09, with no
material correction. Six exact guards pass normal0.008s/-O0.007s.

EXACT PRIME-PARTNER QUESTION.
1. Let Y>8, z=Y^(1/3), and R(n)=1_(P^-(n)>z), with STRICT inequality.
   Write ell(n)=(-1)^Omega(n) for Liouville, including multiplicities.
   Fix a nonnegative smooth F compactly supported in(.5,1)^2 and an
   even target m~Y. All sums below have n+q=m and q PRIME; their weight is
    W(n,q)=logn logq F(n/Y,q/Y).
   On this physical support R permits exactly primes and semiprimes,
   including prime squares: three factors greater than z would exceed Y.
   Every physical prime n is rough. Put
    A=sum R(n)W, C=sum R(n)1_(Omega(n)=2)W,
    Q=sum R(n)ell(n)W, G=sum_(n,q prime)W.
   Then EXACTLY
    A=C+G, Q=C-G, G=(A-Q)/2.                              (1)
   Thus the new arithmetic input
    Q <= -kappa Y S_2(m), kappa>0 fixed,                  (2)
   would imply G>=kappa Y S_2(m), using C>=0. This is stronger than
   necessary: positivity only needs Q<A. Formula(1) does NOT prove(2).
   This is the old factored_linear_barrier.py survivor identity with an
   explicit prime partner and physical/log weights, not a new sieve bound.

THE FILTER CREATES A NONZERO SIGNED MAIN TERM EVEN WITHOUT A PRIME PARTNER.
2. For fixed C^1 g compactly supported in(.5,1), put L=logY and
    B_g(Y)=sum_n R(n)ell(n)logn g(n/Y).
   The saved ordinary PNT and semiprime calculation give
    B_g(Y)=(log2-1)Y integral g(v)dv+O_g(Y/L).             (3)
   Here is the normalization check with the same cutoff z throughout.
   Uniformly for x in[Y/2,Y], the number of rough semiprimes <=x is
    sum_(z<p<=sqrt(x)) [pi(x/p)-pi(p)+1].
   This includes p^2 once and p*r, p<r, once. The subtracted pi(p) terms
   total O(Y/L^2). Applying PNT to both prime variables gives
    x integral_z^sqrt(x) dt/[t logt log(x/t)]+O(Y/L^2)
      = x/logx * log(logx/logz-1)+O(Y/L^2)
      = (log2)x/L+O(Y/L^2).
   For sufficiently large Y the integration interval is nonempty. Rough
   primes contribute pi(x)-pi(z)=x/L+O(Y/L^2). The possible n=1 term is
   immaterial. Abel summation with logt g(t/Y), whose supremum and total
   variation are O_g(L), proves(3). This is an application of the integral
   in switched_cubic_barrier.py, with no prime-correlation assumption.
   If g>=0 and integral g>0, the Fourier transform of this log-weighted
   sequence has absolute value >=c_g Y at frequency0 for all large Y.
   Consequently an uncentered uniform o(Y) Fourier bound after inserting
   this rough filter is FALSE. This does not preclude a centered Fourier
   model, or an estimate away from frequency0. No prime-partner asymptotic
   follows from(3), with or without an inserted singular-series factor.

WHERE THE BIAS LIVES IN EXACT INCLUSION-EXCLUSION.
3. Let P(z)=product_(p<=z)p. Complete multiplicativity gives exactly
    R(n)ell(n)
     =sum_(d|n,d|P(z)) mu(d)ell(d)ell(n/d)
     =sum_(d|n,d|P(z)) ell(n/d).                          (4)
   All outer coefficients are +1 because d is squarefree; the inner
   Liouville signs remain. For fixed 0<gamma<1 and D=floor(Y^gamma), split
   the sum against logn g(n/Y) into T_<=D and T_>D. For every A>0,
    T_<=D=O_(A,g,gamma)(Y/L^A),
    T_>D=(log2-1)Y integral g+O_g(Y/L).                  (5)
   Indeed the saved all-log estimate H(t)=sum_(k<=t)ell(k)
   <<_B t/log^B t and Abel summation bound each short-d inner sum by
   O_(B,g,gamma)((Y/d)L^(1-B)); summing 1/d<=O(L) and taking B=A+2
   proves the first assertion. All k are on scale Y/d>=Y^(1-gamma).
   The second follows from(3)-(4), taking A>=1. Constants can depend on
   gamma. This tail is an inclusion-exclusion contribution, NOT a subset
   of rough integers: for a rough n, its only admissible d is1.
   With q prime retained, the inner sum has dk+q=m and ell(k); the saved
   Type I bound for a FREE integer cofactor does not remove that sign.
   Neither part of(5) has been established for that prime-partner sum.

SOURCE-FIT TEST, READ 2026-09-09.
4. Lichtman, Averages of the Mobius function on shifted primes, v2,
   Theorems1.1,1.3 and Remark1.7, also applies to Liouville, but averages
   multiplicative shifts. It does not select our reflected moving target.
   There is a more concrete support mismatch: its(2.4)-(2.5) good set S
   requires a prime factor in[P2,Q2], Q2=exp((logX)^(1-delta/2)). At X=Y,
   for fixed delta>0 and large Y, Q2<Y^(1/3); hence S and our rough set
   are DISJOINT. Theorem6.2 retains the complementary bad-set contribution.
   Its cancellation mechanism therefore does not itself control our set.
   https://arxiv.org/html/2009.08969v2
5. Mangerel's 2024 result gives strict improvement over the trivial bound
   for FULL unweighted Liouville convolution. Its rigidity uses reflection
   on the entire interval and multiplicative dilation. The GRH followup
   proves full sign-pattern existence for large even targets, with its
   quantitative frequency result for prime targets. Neither supplies a
   rough, prime-partner estimate. The masks are not invariant under those
   dilations; absence of prime pairs is not full-interval sign rigidity.
   https://arxiv.org/abs/2404.12117
   https://arxiv.org/html/2412.17199v1 (Theorems1.2-1.3, Proposition1.4)
6. Krishnamoorthy's August2026 preprint, Theorem2, bounds an exceptional
   set of targets for unmasked binary Liouville convolution. It supplies
   neither an individual-target bound nor these masks. No other claim
   from that preprint is used as an input.
   https://arxiv.org/html/2608.13266v1
   Ordinary PNT and the all-log H bound are the already checked inputs
   of prime_factor_endpoint_gate.py (Tao2014Notes2, not excluded Notes7):
   https://terrytao.wordpress.com/2014/12/09/254a-notes-2-complex-analytic-multiplicative-number-theory/

DISPOSITION.
The direct import of unmasked Liouville cancellation fails this test.
Preserve the negative free mean, the exact target(2), the long-divisor
identity and every polynomial tool. A method which preserves or controls
this bias against the actual prime partner would still be useful. The
new ingredient is not supplied by the cited theorems, and Goldbach remains
open in this record. Finite routines guard algebra and support only; their
rational samples do not certify smoothness or asymptotic constants.
"""
from fractions import Fraction

from major_arc_kernel import _factorization
from prime_factor_endpoint_gate import liouville
from unexceptional_vaughan_gate import _divisors, _positive


def rough_sign(n, y):
    """ell(n) times the strict cubic rough indicator; R(1)=1."""
    _positive(n, 'n')
    _positive(y, 'Y')
    factors = _factorization(n)
    if any(p**3 <= y for p, _ in factors):
        return 0
    return (-1)**sum(e for _, e in factors)


def rough_divisor_split(n, y, cutoff):
    """Exact short/long sums in(4), retaining inner Liouville signs."""
    _positive(n, 'n')
    _positive(y, 'Y')
    _positive(cutoff, 'cutoff')
    short = long = 0
    for d in _divisors(n):
        if any(e != 1 or p**3 > y for p, e in _factorization(d)):
            continue
        if d <= cutoff:
            short += liouville(n//d)
        else:
            long += liouville(n//d)
    return short, long


def _clean_vector(vector):
    return tuple(sorted((k, v) for k, v in vector.items() if v))


def _add_log_product(vector, n, q, coefficient):
    for p, exponent in _factorization(n):
        key = tuple(sorted((p, q)))
        vector[key] = vector.get(key, 0)+coefficient*exponent


def prime_partner_split(y, target, samples=None):
    """Exact log-polynomial (A,C,G,Q); samples replace F at integer n.

    None means weight1 throughout the physical interval. An explicit dict
    has nonnegative rational values, with missing entries interpreted as0.
    G is computed independently using primality, without a rough filter.
    """
    _positive(y, 'Y')
    _positive(target, 'target')
    if y <= 8 or target % 2:
        raise ValueError('require Y>8 and an even target')
    if samples is not None and (not isinstance(samples, dict) or any(
            type(n) is not int or not y < 2*n <= 2*y
            or type(w) not in (int, Fraction) or w < 0
            for n, w in samples.items())):
        raise ValueError('samples must have physical integer keys and nonnegative rational values')
    a, c, g, qsum = {}, {}, {}, {}
    for n in range(y//2+1, y+1):
        q = target-n
        if not y < 2*q <= 2*y or _factorization(q) != ((q, 1),):
            continue
        weight = 1 if samples is None else samples.get(n, 0)
        if _factorization(n) == ((n, 1),):
            _add_log_product(g, n, q, weight)
        sign = rough_sign(n, y)
        if sign:
            _add_log_product(a, n, q, weight)
            _add_log_product(qsum, n, q, sign*weight)
            if sign == 1:
                _add_log_product(c, n, q, weight)
    return tuple(_clean_vector(v) for v in (a, c, g, qsum))


def free_log_split(y, cutoff):
    """Exact (full,short,long) log vectors on(Y/2,Y], with weight1.

    The finite sharp interval is an algebra fixture, not the smooth g used
    in the asymptotic theorem. Each key p represents log(p).
    """
    _positive(y, 'Y')
    _positive(cutoff, 'cutoff')
    full, short, long = {}, {}, {}
    for n in range(y//2+1, y+1):
        small, large = rough_divisor_split(n, y, cutoff)
        for vector, sign in ((full, rough_sign(n, y)), (short, small), (long, large)):
            for p, exponent in _factorization(n):
                vector[p] = vector.get(p, 0)+sign*exponent
    return tuple(_clean_vector(v) for v in (full, short, long))
