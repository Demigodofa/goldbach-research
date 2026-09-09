"""Actual prime cancellation from multiplicative curvature, with full masks.

Owner: Kevin's Goldbach research. Purpose: test actual arithmetic structure
against analytic_complementary_phase.py, and preserve a reusable phase
criterion. These are applications of classical Vaughan/van der Corput
methods. No novelty, paired-prime estimate or Goldbach coverage is claimed.

1. ACTUAL STATEMENT AND A REUSABLE CURVATURE CRITERION.
Let T=N^(9/10), L=logN and psi be fixed smooth with compact support in
(1/2,3/4). For any real lambda_N, put
 f_N(u)=lambda_N*u+sin(u-1/2)-(u-1/2).
For ACTUAL von Mangoldt weights, uniformly in lambda_N,
 |sum_n Lambda(n)psi(n/N)exp[-i*T*f_N(n/N)]|
                <<_psi N^(39/40)*L^3 <<_psi N^(79/80).          (1)
This includes all prime powers exactly. Subtracting proper powers to
obtain a prime-only statement costs O(sqrtN*L^2), which is smaller.

The same proof applies to a family of real C^3 phases f_N on a fixed
compact interval I=[A,B] inside(0,infinity), supporting psi in its
interior, whenever there are fixed positive constants c,C with
 c<=|f_N''(u)|<=C,
 c<=|(u^2*f_N''(u))'|<=C for every u in I.                     (2)
The constant in(1) may then depend on I,psi,c,C but not on N or any
unrestricted affine part of f_N. These are two separate hypotheses.
In particular nonzero f'' alone does NOT suffice: for log u, u^2*f''
is constant, and the second condition fails. No arbitrary phase family
is included without checking both conditions.

2. SOURCE AND ARITHMETIC IDENTITY, WITHOUT BRANCH ASSUMPTIONS.
Discrete source checked2026-09-09: Olivier Robert, 'On van der Corput's
k-th derivative test for exponential sums', Section3.1, Theorem1,
printedp5, equation(6), author PDF:
 https://perso.univ-st-etienne.fr/rool6510/robert-2015-indag.pdf
If lambda2<=|F''|<=alpha*lambda2 on an interval of M consecutive
integers, the sum of e(F(m)) is O_alpha(M*sqrt(lambda2)+lambda2^-1/2),
where e(v)=exp(2pi*i*v). Translation is explained on printedp2.
We apply this to angular phase divided by2pi. Restriction to every
subinterval and partial summation add only the amplitude's supremum
and total variation. A shorter-than-unit interval costs O(1), absorbed
by the bounds below. The web tool read the actual PDF. A separate local
urllib request failed certificate verification; no local PDF hash was
obtained, and no certificate bypass or unchanged retry was used.

Reuse the EXACT identity proved and checked in unexceptional_vaughan_gate.py:
 Lambda=Lambda_<=U +mu_<=V*log -mu_<=V*Lambda_<=U*1
                                  +mu_>V*Lambda_>U*1.          (3)
Here * denotes Dirichlet convolution and1 is its constant-one function.
The elementary identity itself is unconditional; we use NONE of that
module's unexceptional-distribution assumptions or prime-model estimates.
Its primary reference remains Tao, 254A Notes3, Lemma18, equation(32):
 https://terrytao.wordpress.com/2015/01/10/254a-notes-3-the-large-sieve-and-the-bombieri-vinogradov-theorem/
This does not revive the excluded, different Notes7 Proposition23.
The essential free convolution1 is retained throughout.

Set U=V=floor(N^(1/5)). Since the supported n are comparable to N,
the low Lambda term vanishes for large N. For the third term define
 C_d=sum_(ab=d,a<=V,b<=U)mu(a)Lambda(b).
Then d<=UV and |C_d|<=sum_(b|d)Lambda(b)=log d. Grouping the last
term with the free1 gives EXACT coefficients
 sum_(a>V,b>U)mu(a)B_U(b)psi(ab/N)exp[-i*T*f_N(ab/N)],
 B_U(b)=sum_(d|b,d>U)Lambda(d), 0<=B_U(b)<=log b.                (4)
We do not replace B_U by log b or Lambda; its actual values remain
in the bilinear sum. Only their stated upper bound is used.

3. TYPE I: THE COMPLETE SMALL-DIVISOR COST.
For d<=UV, on a real interval where dk/N lies in I, the angular phase
-T*f_N(dk/N) has second derivative of size T*(d/N)^2, with the fixed
lower/upper ratio in(2). The interval has length O(N/d). The discrete
source, uniformly on every prefix, therefore gives
 sum_k psi(dk/N)exp[-i*T*f_N(dk/N)]
                                  << sqrtT+(N/d)/sqrtT.        (5)
The scaled psi has bounded total variation. A log k weight adds O(L)
to that norm, including its derivative; all k here are at least a fixed
multiple of N^(3/5). Sum(5) with |mu(d)|<=1 for d<=V and with the
actual |C_d|<=log d for d<=UV. The total Type I contribution is
 O(UV*sqrtT*L+N*T^-1/2*L^2)
                    =O(N^(17/20)*L+N^(11/20)*L^2).            (6)
The two Type I terms and their signs are retained; an absolute estimate
suffices at this step. No progression distribution hypothesis was used.

4. TYPE II: EXACT MASK, COEFFICIENTS AND PHASE-DIFFERENCE CURVATURE.
Partition(4) into O(L^2) dyadic rectangles, intersecting the lower
factor cutoffs with their intervals. In every nonempty rectangle,
the product of the tags is comparable to N because ab/N lies in I.
Interchange factor labels if needed to obtain m~M,k~K with
 M>=K, MK comparable to N, M>=c_I*sqrtN, K>=c_I*N^(1/5).
Normalize the single B_U weight by a constant times L. The normalized
actual coefficients alpha_m,beta_k have absolute value<=1. We estimate
 S=sum_(m,k)alpha_m*beta_k*psi(mk/N)*exp[-i*T*f_N(mk/N)].        (7)
There is no completion into smooth coefficients and no replacement
of the product support by an unrestricted rectangle.

Cauchy on m gives |S|^2<=O(M)sum_m|sum_k beta_k*psi(mk/N)
*exp[-i*T*f_N(mk/N)]|^2. Expand the square. For k=r, its inner
m sum is O_psi(M); over O(K) diagonal pairs the cost before the
outside M is O(MK). Keep this diagonal instead of differentiating it.

For k!=r, put h=|k-r| and retain the real interval intersection
 J_(k,r)={m in the actual m interval: mk/N in I and mr/N in I}.
It may be empty. On it, set x=mk/N, y=mr/N and
 Phi(m)=-T*[f_N(x)-f_N(y)], G_N(u)=u^2*f_N''(u).
Direct differentiation gives the EXACT identity
 Phi''(m)=-T/m^2 *[G_N(x)-G_N(y)].                             (8)
By(2), G_N' has fixed sign and magnitude between c and C on I.
The interval between x and y stays inside I. The mean value theorem
therefore gives, uniformly on the full intersection,
 |Phi''(m)| comparable to T*h/(M^2*K).                         (9)
In particular the arbitrary affine phase disappears from this curvature.

The amplitude A_(k,r)(m)=psi(mk/N)*conjugate(psi(mr/N)) has a uniform
supremum and total variation: each differentiated factor integrates
to at most ||psi||_infinity*int|psi'| after its own linear substitution.
Thus the discrete source and weighted partial summation apply on J_(k,r),
including its endpoints, and yield
 |sum_m A_(k,r)(m)exp[i*Phi(m)]|
               << sqrt(T*h/K)+M*sqrt(K/(T*h)).                (10)
The curvature in(9) is O(T/M^2)=O(N^-1/10), so the harmless O(1)
short-interval contribution is absorbed by its inverse square root.

There are O(K) ordered pairs per positive h, and h<=O(K). Summing
h^(1/2) and h^(-1/2), then including the diagonal and outside M, gives
 |S|^2 << M^2*K+M*K^2*sqrtT+M^2*K^2/sqrtT.
Taking square roots and using MK comparable to N,
 |S| << N*[K^-1/2+T^(1/4)*M^-1/2+T^-1/4].                    (11)
With M>=c*sqrtN and K>=c*N^(1/5), the three terms cost respectively
N^(9/10), N^(39/40), N^(31/40). Restore the one logarithm in B_U
and the O(L^2) dyadic rectangles: the Type II total is O(N^(39/40)L^3).
Together with(6), this proves the criterion(1)-(2). The spare exponent
1/80 absorbs L^3 for sufficiently large N. No numerical onset is claimed.

5. VERIFYING THE SINE PHASE AND THE MODEL COMPARISON.
On any compact I=[A,B] inside(1/2,3/4),
 f_N''(u)=-sin(u-1/2),
 G_N'(u)=-2u*sin(u-1/2)-u^2*cos(u-1/2).
Thus |f_N''|>=sin(A-1/2)>0 and
 |G_N'|>=A^2*cos(B-1/2)>0, with fixed upper bounds. These
conditions hold uniformly in lambda_N and prove the concrete(1).

For the model's bounded slope lambda_N->3, f_N'>1 for large N.
Its own-phase coefficient expands into (1/4)sum psi(n/N) plus the
two harmonics -T*f_N and -2T*f_N. Smooth Poisson summation and
one nonstationary integration for the central alias bound each harmonic
by O_psi(N/T); the other aliases are summably O(N^-1) as before.
Hence the model coefficient is (N/4)int psi+O_psi(N^(1/10)).
For psi nonnegative and nonzero this has order N, excluded for actual
Lambda by(1). This uses actual multiplicative coefficients, an input
the preceding polynomial-probe countermodel does not encode.

6. COROLLARY: EVERY FIXED ANALYTIC NONAFFINE COMPLEMENTARY PHASE.
Let h be FIXED real analytic on(0,1), nonaffine, with
 h(u)+h(1-u)=0. For fixed smooth psi compactly supported in(0,1)
and arbitrary real lambda_N, put f_N(u)=lambda_N*u+h(u). Then
 sum_n Lambda(n)psi(n/N)exp[-i*T*f_N(n/N)]=o_(h,psi)(N),         (12)
uniformly in lambda_N. This is a qualitative statement, not a uniform
power saving over all such h or all localized cutoffs.

Indeed h'' is analytic and not identically zero. Also
 G'(u)=(u^2*h''(u))' is analytic and not identically zero. If it
vanished identically, integration would give h(u)=-c*log u+d*u+e.
The complementary identity would then force c=0 because log[u(1-u)]
is nonconstant, contradicting nonaffinity. If either function vanished
on an open subinterval, analytic continuation would give that same
global identity. Thus both have only finitely many zeros on a fixed
compact neighborhood of support(psi).

For fixed small delta>0, remove delta-neighborhoods of those finitely
many zeros, using smooth cutoffs bounded between0 and1, with the removed
part supported in neighborhoods of radius2delta. Partition the remaining
smooth amplitude into finitely many fixed compact intervals avoiding
the zeros. On each interval both conditions(2) hold with constants
depending on h,psi,delta, giving O_(h,psi,delta)(N^(79/80)).

The removed part has absolute Lambda mass O_(h,psi)(delta*N)+o(N).
To see this without assuming cancellation, use the CHECKED interval
upper bound from short_prime_window_energy.py: Yamada2312.16090v1,
Theorem2 printedp3 equation(13), https://arxiv.org/pdf/2312.16090v1,
specialized and weakened to pi(x+y)-pi(x)<=2y/logy. Here y is a
fixed multiple of delta*N, so multiplying by logN gives O(delta*N)
for sufficiently large N depending on delta. There are only a fixed
number of intervals. All proper powers together cost O(sqrtN*L^2).
The coefficient of delta*N can be taken independent of delta once
N is sufficiently large for that delta. Taking limsup as N tends
to infinity, and ONLY THEN letting delta tend to0, proves(12).
We do not interchange those limits or assert a uniform quantitative
rate through the degeneracy points. The affine case is excluded.

7. PRESERVED GAP.
The result excludes a whole class of fixed analytic complementary
alignments from actual primes. It does not extract such an alignment
from a large paired window. N-dependent nonlinear phases, many local
packets and superpositions remain outside the corollary. The actual
O(N) comparable-band bound is not improved here, and the sufficient
signed Goldbach lower margin remains OPEN. Polynomial identities,
arithmetic decompositions and all prior source corrections are retained.
"""
from fractions import Fraction as F
from math import cos, sin


def type_i_budget():
    t, u = F(9,10), F(1,5)
    return (2*u+t/2, 1-t/2)


def type_ii_budget(short_exponent):
    if type(short_exponent) is not F or not F(1,5) <= short_exponent <= F(1,2):
        raise ValueError('an exact short-factor exponent in[1/5,1/2] is required')
    t, k = F(9,10), short_exponent
    return {'diagonal': 1-k/2,
            'curvature': 1+t/4-(1-k)/2,
            'inverse_curvature': 1-t/4}


def sine_curvatures(u):
    return (-sin(u-0.5), -2*u*sin(u-0.5)-u*u*cos(u-0.5))


def phase_difference_curvature(m, k, r, n_scale, t_scale):
    """Angular second derivative in the Cauchy factor; affine parts cancel."""
    x, y = m*k/n_scale, m*r/n_scale
    return -t_scale*((k/n_scale)**2*(-sin(x-0.5))
                     -(r/n_scale)**2*(-sin(y-0.5)))
