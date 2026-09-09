"""Uniform actual-prime phase cancellation using bounded factor shifts.

Owner: Kevin's Goldbach research. Purpose: handle controlled N-dependent
phases, including affine phases, beyond analytic_prime_curvature.py.
This preserves an arithmetic component for a future exact-window test;
it is not a signed paired-prime estimate or a novelty claim.

1. UNIFORM ACTUAL STATEMENT.
Fix a compact positive interval I=[A,B], 0<A<B, and fixed constants
c,C,C_psi>0. Let f_N be ANY real C^3 function on I such that, throughout I,
 |f_N'(u)|>=c, |f_N'(u)+u*f_N''(u)|>=c,
 |f_N^(j)(u)|<=C for j=1,2,3.                                 (1)
Both functions in the lower bounds have fixed sign on the connected
interval, but they need not have the same sign. No analyticity, fixed
nonlinear part, or nonzero second derivative is assumed.
Allow psi_N to be complex C^1, compactly supported in the interior of
the SAME I, with sup|psi_N|+int|psi_N'|<=C_psi uniformly in N.
With T=N^(9/10) and L=logN, for actual von Mangoldt coefficients,
 |sum_n Lambda(n)psi_N(n/N)exp[-i*T*f_N(n/N)]|
                    <<_(I,c,C,C_psi) N^(43/44)*L^3
                    <<_(I,c,C,C_psi) N^(49/50).                (2)
The phases and amplitudes may vary arbitrarily with N subject to these
uniform bounds. No derivative of f_N of order4 or higher is required.
The constant term of f_N is unrestricted; its linear term is constrained
by(1). No uniformity over unbounded derivatives or vanishing lower
bounds is claimed. A shrinking amplitude support does not improve the
right side in(2) to a bound proportional to its length.

2. A DISCRETE FIRST-DERIVATIVE LEMMA WITH VARIATION.
Suppose a real C^2 angular phase phi on a real interval J satisfies
 c_0*ell<=|phi'|<=C_0*ell<=1/2,
 int_J |phi''(x)|dx<=C_1*ell, ell>0.                           (3)
Then, for a C^1 amplitude a on J,
 |sum_(n integer in J) a(n)exp[i*phi(n)]|
 <<_(c_0,C_0,C_1) (sup_J|a|+int_J|a'|)*ell^-1.                (4)
We prove this directly; no monotonicity of phi' is assumed.
Write p,...,q for the consecutive integers in J. A set of at most
one integer has the required bound immediately. For p<=n<q put
 Delta_n=phi(n+1)-phi(n), w_n=(exp(i*Delta_n)-1)^-1.
The derivative in(3) has a fixed sign, so every Delta_n has that sign
and magnitude between c_0*ell and C_0*ell<=1/2. Thus
 sup|w_n|<<ell^-1.
Also sum|Delta_(n+1)-Delta_n|<=int_J|phi''|<=C_1*ell: write each
difference as an integral of phi'' over two neighboring unit segments
and sum their translated unit averages, whose total coverage is at most1.
The derivative of (exp(i*x)-1)^-1 has magnitude O(ell^-2) on the
same signed range. Hence sum|w_(n+1)-w_n|<<ell^-1.

The exact telescoping identity
 exp[i*phi(n)]=w_n*(exp[i*phi(n+1)]-exp[i*phi(n)])
and discrete summation by parts give(4), with the last term at q and
all endpoints included. The discrete variation of a is at most its
continuous total variation. The phase needs to be defined only between
the first and last retained integers, so no extension outside J is used.

3. THE FINITE SHIFT INEQUALITY AND ITS ORDER OF USE.
For any complex sequence z supported on Q consecutive integers, extend
z by zero and let R>=1 be an integer. Then
 |sum z_k|^2 <= (Q+R-1)/R *[sum|z_k|^2
    +2 sum_(1<=h<R)(1-h/R)Re sum_k z_(k+h)*conjugate(z_k)].     (5)
Indeed R*sum z_k=sum_j sum_(0<=r<R)z_(j+r). The outer sum has
at most Q+R-1 terms. Cauchy and expansion of its squared inner sums
give(5), including the conjugate and triangular weights.
Primary cross-check: Olivier Robert, 'On van der Corput's k-th derivative
test for exponential sums', Section3.3, Lemma1, printedp8:
 https://perso.univ-st-etienne.fr/rool6510/robert-2015-indag.pdf
The actual PDF was read with web on2026-09-09. The finite derivation
above fixes the conjugation, which is lost in plain-text PDF extraction.
The prior local certificate failure is unchanged; no local retry was made.

When applying(5) below, first sum the signed correlations over m, and
only THEN bound their absolute values. Taking absolute values separately
for each m would destroy the cancellation proved by(4).

4. EXACT VAUGHAN COEFFICIENTS AND TYPE I.
Use the same unconditional convolution identity and grouped coefficients
as analytic_prime_curvature.py, with
 U=V=floor(N^(1/22)), R=floor(U/10).
We work at sufficiently large N so R>=1. The first low-Lambda term
vanishes on n/N in I. The other Type I terms are
 sum_(d<=V)mu(d)sum_k log(k)psi_N(dk/N)exp[-i*T*f_N(dk/N)],
 -sum_(d<=UV)C_d sum_k psi_N(dk/N)exp[-i*T*f_N(dk/N)],
 C_d=sum_(ab=d,a<=V,b<=U)mu(a)Lambda(b), |C_d|<=log d.            (6)
The identity's essential free convolution1 remains in the Type II
coefficient B_U(b)=sum_(d|b,d>U)Lambda(d), with 0<=B_U(b)<=log b.
No unexceptional-branch assumption or prime-model substitution is used.

For fixed d<=UV the angular phase phi_d(k)=-T*f_N(dk/N) has
 |phi_d'| comparable to ell_d=T*d/N,
 int|phi_d''|<=C_I*ell_d
on the interval dk/N in I. The largest ell_d has exponent
 9/10+2/22-1=-1/110,
so the upper derivative condition in(3) holds uniformly for large N.
Equation(4) gives inner sums O(N/(Td)); the log k weight adds O(L)
to the amplitude supremum and variation. In detail, k is comparable
to N/d, so its logarithmic derivative integrates over the fixed scaled
support with bounded variation. Summing(6) through the FULL UV range
costs only
                         O((N/T)*L^2)=O(N^(1/10)*L^2).        (7)

5. TYPE II WITH ACTUAL WEIGHTS AND SHIFTED PRODUCT INTERSECTIONS.
The remaining exact sum is
 sum_(a>V,b>U)mu(a)B_U(b)psi_N(ab/N)exp[-i*T*f_N(ab/N)].        (8)
Partition into O(L^2) dyadic rectangles, intersecting their factor
intervals with a>V,b>U. In each nonempty piece, interchange factor
labels to get m~M,k~K with M>=K and MK comparable to N. Then
 K>=U/2, K<=C_I*sqrtN, R<=K/5
for sufficiently large N. Normalize the single B_U coefficient by a
constant times L. Both actual coefficient sequences alpha_m,beta_k
then have absolute value<=1, regardless of which factor was relabeled.
Let S=sum_m alpha_m sum_k z_(m,k), with
 z_(m,k)=beta_k*psi_N(mk/N)*exp[-i*T*f_N(mk/N)].
The k sequence is zero off its actual interval; the product support is
kept inside psi_N. Cauchy in m, followed by(5) for each m, gives an
outside factor O(MK/R). Before that factor the diagonal costs O(MK).

For 1<=h<R, beta_(k+h)*conjugate(beta_k) is independent of m and
has absolute value<=1. The oscillatory m sum is restricted to
 J_(k,h)={m in the actual m interval:
              mk/N in I AND m(k+h)/N in I}.                   (9)
It is an interval or empty. Put x=m(k+h)/N, y=mk/N and
 Phi_(k,h)(m)=-T*[f_N(x)-f_N(y)], D_N(u)=u*f_N'(u).
Direct differentiation gives
 Phi'=-T/m *[D_N(x)-D_N(y)].
Since |D_N'|=|f_N'+u*f_N''| is between fixed positive constants
on I, and the segment from y to x stays in I,
               |Phi'| comparable to ell_h=T*h/N.             (10)
It has a fixed sign. For G_N(u)=u^2*f_N''(u),
 Phi''=-T/m^2 *[G_N(x)-G_N(y)].
The first three derivative upper bounds imply |G_N'|<=C_I, so
 |Phi''|<=C_I*T*h/(m*N),
 int_(J_(k,h))|Phi''|<=C_I*ell_h.
This time G_N' need not be nonzero or have fixed sign.
The largest ell_h has exponent
 9/10+1/22-1=-3/55.
Thus the upper derivative bound in(3) is valid uniformly, and(4)
applies to the full interval(9). The amplitude
psi_N(m(k+h)/N)*conjugate(psi_N(mk/N)) has uniformly bounded
supremum and variation by the two linear changes of variable. Consequently
 |sum_m psi_N(m(k+h)/N)conjugate(psi_N(mk/N))*exp(i*Phi)|
                                      << N/(T*h).             (11)
All endpoints, shifted masks, and actual coefficients are retained.

6. COMPLETE COST AND LIMITS.
For each h there are O(K) values of k. Sum(11) with its triangular
weight, keep the diagonal, and restore the outside MK/R:
 |S|^2 << (MK/R)*[MK+(K*N/T)*log(2R)]
       << N^2/R +N^2*K*log(2R)/(T*R).                         (12)
Here K/T<=C_I*N^(-2/5), so the second term is at most the first
for sufficiently large N. Since R is comparable to N^(1/22),
 |S|<<N/sqrtR=O(N^(43/44)).
The actual coefficient normalization costs one L and the dyadic boxes
cost O(L^2). Together with(7) this proves(2). The strict spare exponent
 49/50-43/44=3/1100
absorbs L^3; no effective numerical onset is asserted. All proper prime
powers are already included in Lambda. A prime-only version subtracts
O(sqrtN*L^2), which is smaller.

For example, on I=[1/4,3/4] take
 f_N(u)=lambda_N*u+epsilon_N*[sin(u-1/2)-(u-1/2)],
 5/2<=lambda_N<=7/2, 0<=epsilon_N<=1.
These parameters can vary arbitrarily with N. Elementary sine/cosine
bounds give f_N'>=79/32 and f_N'+u*f_N''>=73/32, with all the
required derivative upper bounds fixed. The case epsilon_N=0 is affine
and was outside the two nonzero-curvature criterion. On the other hand,
f=log u violates f'+u*f''!=0, so it is not silently included here.

Equation(2) is a single-phase prime correlation bound, not the actual
reflected two-window estimate. It permits uniformly controlled varying
phases and amplitudes; it does not control an unlimited superposition,
growing derivative norms or regions where the lower bounds degenerate.
The actual O(N) comparable band and sufficient signed Goldbach margin
remain unchanged. All earlier polynomial and arithmetic tools persist.
"""
from fractions import Fraction as F


def shift_budget():
    t, u = F(9,10), F(1,22)
    return {'type_i_derivative': t+2*u-1,
            'type_ii_derivative': t+u-1,
            'type_i_sum': 1-t,
            'type_ii_diagonal': 1-u/2,
            'type_ii_off_diagonal': 1+(F(1,2)-t-u)/2,
            'log_absorbed': F(49,50),
            'spare': F(49,50)-(1-u/2)}


def shift_energy_rhs(sequence, shifts):
    """Exact finite-shift inequality RHS for rational real fixture weights."""
    if type(shifts) is not int or shifts < 1 or not sequence:
        raise ValueError('a nonempty rational sequence and positive integer shifts required')
    if any(type(z) is not F for z in sequence):
        raise ValueError('exact rational real fixture coefficients required')
    size = len(sequence)
    bracket = sum((z*z for z in sequence),F(0))
    for h in range(1,min(shifts,size)):
        cross = sum((sequence[k+h]*sequence[k] for k in range(size-h)),F(0))
        bracket += 2*(1-F(h,shifts))*cross
    return F(size+shifts-1,shifts)*bracket


def telescoping_phase_sum(values, amplitudes):
    """Finite identity behind the variation lemma; nonsingular increments only."""
    if not values or len(values) != len(amplitudes):
        raise ValueError('matching nonempty phase values and amplitudes required')
    if len(values) == 1:
        return amplitudes[0]*values[0]
    weighted = []
    for n in range(len(values)-1):
        increment = values[n+1]/values[n]-1
        if abs(increment) == 0:
            raise ValueError('resonant increment')
        weighted.append(amplitudes[n]/increment)
    result = weighted[-1]*values[-1]-weighted[0]*values[0]
    result += sum((weighted[n-1]-weighted[n])*values[n] for n in range(1,len(weighted)))
    return result+amplitudes[-1]*values[-1]
