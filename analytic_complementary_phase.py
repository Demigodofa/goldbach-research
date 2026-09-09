"""One complementary analytic phase evades every fixed-degree probe family.

Owner: Kevin's Goldbach research. Purpose: test the inverse implication
missing from cubic_prime_chirp_exclusion.py. The initially proposed quintic
test led to a single sine-based model covering every fixed degree. This
avoids repeating a new higher-degree countermodel for each probe family.
It is an ARTIFICIAL dense coefficient sequence, not Lambda or zeta data.

1. EXACT STATEMENT AND QUANTIFIERS.
Keep T=N^(9/10), V=N^(1/8), and the exact window operator P_b and central
no-conjugation paired functional Q_b from complementary_window_chirp.py.
In particular chi>=0 is fixed smooth, supported in(1,2), chi(3/2)>0;
zeta>=0 is fixed smooth, supported in(1/4,3/4), equal1 near1/2.
Choose lambda_N nearest to3 on the odd-pi/T lattice and put
 f_N(a)=lambda_N*a+sin(a-1/2)-(a-1/2),
 b_N(n)=1+(1/2)cos[T*f_N(n/N)].                                (1)
Then 1/2<=b_N(n)<=3/2 and
 Q_b(N)=-c_(chi,zeta)*N+O_(chi,zeta)(N^(9/10)), c>0.             (2)

For EVERY FIXED integer D>=1, fixed C>=0 and fixed smooth psi compactly
supported in(0,infinity), let g(a)=sum_(j=0)^D c_j*a^j have real
coefficients. Allow c_0 and c_1 to be arbitrary; require |c_j|<=C for
2<=j<=D. All the coefficients may depend on N. Uniformly in this family,
 |sum_n psi(n/N)(b_N(n)-1)exp[-i*T*g(n/N)]|
                  <<_(D,C,psi) N*T^(-1/(D+2))
                   =N^(1-9/(10*(D+2))).                       (3)
For D=1 this is the full uniform linear Fourier bound N^(7/10).
For D=3 it gives N^(41/50). The SAME b_N in(1) works for each fixed D;
it is not a different model chosen after a test degree is specified.
Constants and the sufficiently-large-N onset may depend on D,C,psi.
There is no uniform claim when D grows with N, when nonlinear c_j are
unbounded, or when psi becomes N-dependent and increasingly localized.

2. THE EXACT WINDOW RETAINS ITS NEGATIVE COMPLEMENTARY MAIN.
Oddness of sin x-x and evenness of cos x give
 f_N(a)+f_N(1-a)=lambda_N,
 f'_N(a)=lambda_N-1+cos(a-1/2)=f'_N(1-a)>0,                    (4)
since lambda_N>2 for all sufficiently large N. Also
 |lambda_N-3|<=pi/T, exp(i*T*lambda_N)=-1.
Every derivative of f_N of order>=2 has magnitude<=1, globally.

The exact operator, with the same fixed Fourier cutoff nu, is
 P_b(aN)=T/(2pi)sum_(n>=2)b_N(n)/sqrt n
     *hatChi(Tlog(n/(aN)))*nu(Tlog(n/(aN))/V).
We transfer the checked calculation of complementary_window_chirp.py,
sections3-4, keeping its error estimates. Here are the hypotheses and
costs explicitly: b'_N(t)=O(T/N), the Schwartz kernel has L1 norm
O(N/T) and derivative L1 norm O(1), so the unit-interval sum-to-integral
error after the prefactor is O(T/sqrtN)=O(N^(2/5)). On setting
t=aN+(N/T)y, the phase remainder is at most y^2/(2T). The logarithmic
kernel and square-root amplitude remainders have their previous integrable
Schwartz majorants. Thus local linearization costs O(sqrtN/T), and
removing the fixed Fourier cutoff costs O(sqrtN*V^-16). No polynomial
identity was required for those bounds; the displayed derivative estimates
supply them for(1). Angular Fourier inversion and f'_N>0 select only
the positive cosine half. Uniformly for a in[1/4,3/4],
 P_b(aN)=(1/4)sqrt(aN)*chi(a*f'_N(a))*exp[i*T*f_N(a)]
                                       +O_chi(N^(2/5)).         (5)

Substitute(5) into Q_b=2 int zeta(a)P_b(aN)P_b((1-a)N)
/sqrt(a(1-a)) da. The square-root weights cancel; the complementary
phase is exactly -1. The cross error is O(N^(1/2+2/5))=O(N^(9/10));
the product of two errors is smaller. Replacing lambda_N by3 costs
O(N/T), also smaller. The resulting fixed positive constant is
 c_(chi,zeta)=(1/8)int zeta(a)
 *chi(a*[2+cos(a-1/2)])*chi((1-a)*[2+cos(a-1/2)]) da.           (6)
At a=1/2 both chi arguments are3/2. Continuity and the stated cutoffs
give a positive integral on a fixed neighborhood, proving(2).
The positivity and boundedness of b_N also preserve all the previous
interval-mass, multiplicative-mass and O(N) window-energy inequalities.

3. ELEMENTARY OSCILLATORY-INTEGRAL LEMMA, WITH AMPLITUDES.
If a real smooth phase phi on an interval satisfies |phi^(r)|>=M>=1,
where r>=2 is fixed, then
 |int A(a)exp[i*phi(a)] da|
 <<_r (sup|A|+int|A'|)*M^(-1/r).                              (7)
The interval can be any subinterval of the fixed spatial support; A need
not vanish at the new endpoints. We include a proof to specify exactly
the estimate needed, instead of importing an unstated finite-type claim.

For r=2, phi'' has fixed sign. Thus phi' is monotone, and the set
|phi'|<=sqrtM is an interval of length<=2/sqrtM. Bound that integral
absolutely. On either remaining piece, integrate by parts using
(exp(i*phi))'=i*phi'*exp(i*phi). Boundary terms and amplitude derivatives
cost O((sup|A|+int|A'|)/sqrtM). The term differentiating 1/phi'
has the same bound because phi' is monotone and never vanishes there.

Inductively, for r>=3, phi^(r-1) is monotone. Remove its sublevel
interval |phi^(r-1)|<=mu, of length at most2mu/M. On the at most
two remaining intervals apply the order-(r-1) estimate with parameter
mu. Choose mu=M^((r-1)/r). The removed integral and remaining integrals
then all cost O_r((sup|A|+int|A'|)*M^(-1/r)). This proves(7).
The proof works for complex A. Each partition uses only a bounded number
of pieces for fixed r, so its amplitude costs are uniform.

4. THE ZERO POISSON ALIAS EVADES ALL FIXED-DEGREE POLYNOMIALS.
Expand b_N-1 into its two exponentials, each with coefficient1/4.
Write g(a)=c_0+c_1*a+h(a), where h has degrees2 through D.
The constant c_0 gives a unit factor. Reduce xi=T*c_1/N modulo2pi
to[-pi,pi], which is legitimate at every integer n. Poisson summation
for the smooth compact summand gives terms
 N int psi(a)exp{i[+-T*f_N(a)-T*h(a)-N*(xi+2pi*k)*a]} da,       (8)
where k ranges over integers. This reduction is what licenses arbitrary
c_1; we do not assume its unscaled value is bounded.

For k=0, take the two consecutive derivative orders D+1 and D+2.
Both annihilate h and every linear term, including N*xi*a. The resulting
derivatives are T times a sine and a cosine of a-1/2, up to signs.
Partition the fixed support interval at a-1/2=j*pi/4, j integer.
On each resulting piece either |sin(a-1/2)|>=1/sqrt2 throughout,
or |cos(a-1/2)|>=1/sqrt2 throughout. Choose the matching derivative
order r in{D+1,D+2}; it is at least2. Applying(7) there gives
 O_(D,psi)(T^(-1/r))=O_(D,psi)(T^(-1/(D+2))).
There are only finitely many pieces depending on psi's fixed support.
The coefficients of h and the size of xi do not enter this estimate.
The partition is necessary: a single high derivative can vanish, and
we never assume one derivative stays bounded below on the whole support.

5. EVERY NONZERO POISSON ALIAS IS PAID UNIFORMLY.
On that support, f'_N and the first three derivatives of h are bounded
by constants depending only on D,C,psi. Since T=o(N), for k!=0,
 |+-T*f'_N-T*h'-N*(xi+2pi*k)|>=c*N*|k|
for sufficiently large N depending only on D,C,psi. Indeed
|xi+2pi*k|>=pi*|k|, including both endpoints xi=+-pi.
The next two derivatives of the phase in(8) are O_(D,C,psi)(T).
Twice integrating by parts, with the original compact amplitude psi,
therefore bounds its integral by O_(D,C,psi)((N*|k|)^-2).
Multiplication by N and summation over k!=0 give O_(D,C,psi)(N^-1).
Combining with the zero alias proves(3), with every alias included.
No unsmoothed polynomial sum estimate or conjecture is used.

6. THE PRECISE INVERSE IMPLICATION FAILS; PRIME CORRELATION STAYS OPEN.
For this artificial sequence, order-N negative paired reinforcement
coexists with power-saving centered correlations for EVERY FIXED DEGREE
in the specified polynomial-probe families. Thus those marginal bounds
and tests do not by themselves imply o(N) of the exact paired functional,
nor force a large coefficient against a bounded cubic phase. The previous
actual-prime cubic exclusion remains valid, but such an inverse implication
cannot transfer it using only these model-shared hypotheses.

This is not an assertion that arbitrary prime polynomial sums are small,
that actual primes follow this analytic phase, or that every polynomial
tool fails. The model lacks prime support, Type I identities and the zeta
explicit formula. It also does not test unbounded nonlinear coefficients,
increasing degrees, increasingly local probes, or a jointly controlled
superposition. Those distinctions preserve possible arithmetic inputs.
The actual O(N) comparable-band bound and missing signed Goldbach lower
margin are unchanged. This result is new-to-this-task; no worldwide
novelty or historical-priority claim is made.
"""
from fractions import Fraction as F
from math import cos, sin


def analytic_phase(a, slope):
    return slope*a+sin(a-0.5)-(a-0.5)


def phase_derivative(a, slope, order):
    if type(order) is not int or order < 1:
        raise ValueError('a positive integer derivative order is required')
    if order == 1:
        return slope-1+cos(a-0.5)
    s, c = sin(a-0.5), cos(a-0.5)
    return (s, c, -s, -c)[order % 4]


def derivative_order_for_cell(degree, cell):
    """Select a nonvanishing high derivative on x in[j*pi/4,(j+1)*pi/4]."""
    if type(degree) is not int or degree < 1 or type(cell) is not int:
        raise ValueError('positive integer degree and integer cell required')
    # Even derivatives use sine; odd derivatives use cosine, up to signs.
    sine_cell = cell % 4 in (1, 2)
    first = degree+1
    return first if (first % 2 == 0) == sine_cell else first+1


def probe_exponent(degree):
    if type(degree) is not int or degree < 1:
        raise ValueError('a fixed positive integer degree is required')
    return 1-F(9, 10*(degree+2))
