"""A pointwise spectral transfer with its approximation and zero-height tails paid.

Owner: Kevin's Goldbach research. Purpose: test a different arithmetic
ingredient, preserving a precise signed zero-pair target for individual
even integers. This applies a classical explicit formula; it is not a
Goldbach proof, a worldwide novelty claim, or a numerical zero certificate.

SOURCE CORRECTION BEFORE USING THE FORMULA.
1. Languasco's2016 survey, arXiv:1606.00860v1, Theorem2.2,p3,
Lemma5.1,p11 and Section6,p14, corrects the2015 Languasco-Zaccagnini
paper (and arXiv:1206.0251v1). Its normalized Cesaro error is O_k(N),
NOT the printed O_k(sqrtN). The exponential-sum error requires a constant
term. The original shifted-line formula contains -zeta'/zeta(0); its
remaining integral is O(sqrt(a)) at y0 and does not cancel that constant.
The later author's corrigendum controls over the earlier published statement.

For comparison, putting A2(X)=sum_n R(n)(X-n)_+^2/2 in the corrected
Cesaro theorem gives error O(X^3). A backward third difference at stepH,
divided by H^3, therefore only gives error O(X^3/H^3). Its positive kernel
 K_H(t)=[t_+^2-3(t-H)_+^2+3(t-2H)_+^2-(t-3H)_+^2]/(2H^3)
is the density of the sum of three uniform[0,H] variables. It has support
[0,3H]. At integerH1 only K_1(1)=K_1(2)=1/2 survive on the integers:
 R(N)=2 Delta_1^3 A2(N+2)-R(N+1).
This identity does not differentiate a big-O term into a small error.
For X>=4H the available corrected error divided by the linear main has
size X^2/H^3; it vanishes only when H/X^(2/3) tends to infinity. This
is a limitation of that error budget, not a lower bound for the error.
We instead return to the corrected exponential-sum formula itself.

DIRECT ONE-PERIOD TRANSFER, WITHOUT RH.
2. Let N>=3 be an integer, L=logN, a=1/N, z=a+it, -pi<=t<=pi.
Use the principal logarithm on Re(z)>0, and define
 S(z)=sum_(n>=1) Lambda(n)exp(-nz),
 Z(z)=sum_rho Gamma(rho)z^(-rho), M(z)=1/z-Z(z),
 I_N[f]=exp(1)/(2pi) int_(-pi)^pi f(a+it)exp(iNt)dt.
All nontrivial zeta zeros, with BOTH signs of the imaginary part and
their multiplicities, occur in Z. Their real parts are not replaced by1/2.
The corrected Lemma5.1 says S=M+E with
 |E| << 1+sqrt(|z|)*(1+log_+^2(N|t|)).                 (1)
It follows on this compact period that ||E||_2<<L^2. Parseval gives
 ||S||_2^2=2pi sum_n Lambda(n)^2 exp(-2n/N)<<N L.       (2)
For the upper bound, sum_(n<=u)Lambda(n)^2<=logu*psi(u)<<u logu
and partial summation suffice; no prime-pair estimate or RH is involved.

Fourier coefficient extraction is EXACT: R(N)=I_N[S^2], where
R(N)=sum_(j+k=N)Lambda(j)Lambda(k). Since M=S-E,
 |I_N[S^2-M^2]| << ||S||_2||E||_2+||E||_2^2
                << sqrtN L^(5/2)+L^4=o(N).           (3)
Thus the approximation error is paid at an INDIVIDUAL target, with no
average over N and no removal of a Cesaro weight. The square is S^2,
NOT |S|^2; replacing it by a positive energy changes the Fourier coefficient.

3. Put D_N(s)=I_N[z^(-s)]. Expansion of M^2 gives
 R(N)=D_N(2)-2 sum_rho Gamma(rho)D_N(1+rho)
       +sum_(rho,sigma)Gamma(rho)Gamma(sigma)D_N(rho+sigma)
       +O(sqrtN L^(5/2)+L^4).                         (4)
The finite-period kernel D_N is essential. It cannot be replaced by
N^(s-1)/Gamma(s), the full vertical-line inverse, without a separate
tail estimate for THESE zero weights. This is not the Cesaro gamma quotient.

Convergence is legitimate for each fixed N: Stirling and 0<Re(rho)<1 give
 |Gamma(rho)z^(-rho)| << N |Im(rho)|^(1/2)
           *exp(-|Im(rho)|/(2piN))
for large |Im(rho)|, uniformly on the entire period. Indeed
pi/2-|arg(z)|>=arctan(1/(piN))>=1/(2piN).
The zero count is O(T log(2T)), so this majorant is summable uniformly.
Consequently both zero sums in (4) can be interchanged with the compact
integral. The bounds need not be uniform as N tends to infinity without
retaining their displayed N-dependence.

4. There is also a paid FINITE HEIGHT version. For T>=N, split the omitted
zeros into blocks jT<|Im(rho)|<=(j+1)T, j>=1. Cumulative zero counting,
not an unproved local-density estimate, gives
 sup_(|t|<=pi)|Z(z)-Z_T(z)|
   << N T^(3/2)log(2T) exp(-T/(2piN)).                 (5)
The remaining geometric sum is bounded uniformly because T/N>=1.
For any fixed A>0, taking T=2pi(A+5)NlogN makes (5) O_A(N^(-A)).
Also ||Z||_2<<sqrt(NL)+L^2 by (1)-(2) and ||1/z||_2<<sqrtN.
Therefore the replacement of I_N[Z^2] by I_N[Z_T^2] costs at most
O_A(N^(-A)*(sqrt(NL)+L^2)+N^(-2A)). Choose A>=3 below.
This does not certify any computed list of zeros or improve computation
cost: all zeros up to T must still be included, and their number is
O_A(N log^2N). A bare list of critical-line zeros is insufficient unless
its completeness in the whole strip has been verified.

THE SINGLE-ZERO PART CAN BE REMOVED WITH ACTUAL BOUNDS.
5. Let V(z)=1/(exp(z)-1)=sum_(j>=1)exp(-jz). On the chosen period,
V(z)-1/z is uniformly bounded (its singularity at0 is removable and
the other poles at nonzero2pi*i lie outside). Exact extraction gives
 I_N[S V]=psi(N-1),
 I_N[S/z]=psi(N-1)+O(sqrt(NL)).
The full-line inverse for z^(-2), whose omitted tails are absolutely
O(1), gives D_N(2)=N+O(1). Splitting at |t|=1/N in (1) gives
 int_(|t|<=pi)|E(z)/z|dt<<L^2.
Since Z=1/z-S+E, equation(4) becomes, for the above finite T,
 R(N)=2psi(N-1)-N+B_(N,T)
             +O(sqrtN L^(5/2)+L^4),                  (6)
 B_(N,T)=sum_(|Im(rho)|,|Im(sigma)|<=T)
                   Gamma(rho)Gamma(sigma)D_N(rho+sigma).
The sum is over ORDERED zero pairs, including the diagonal. It is real
by conjugation symmetry but need not be positive. PNT makes
2psi(N-1)-N=N+o(N), unconditionally.

6. A precise sufficient input for coverage is therefore the UNPROVED
one-sided bound B_(N,T)>=-(1-delta)N for every sufficiently large evenN,
with a fixed delta>0. It would give R(N)>=delta N+o(N). Representations
with a proper prime-power summand cost O(sqrtN log^2N): there are
O(sqrtN) such powers up to N, and each pair weight is at most log^2N.
Thus that signed margin would imply genuine prime pairs. Neither this
margin nor an effective onset is established. The transfer error in (6)
is proved; the signed pair sum is still the actual arithmetic problem.

Ordinary Montgomery pair correlation is not automatically an estimate
for D_N(rho+sigma) with its complex Gamma weights and target oscillation.
The inspected Languasco-Perelli1996 stronger Dirichlet-L hypothesis
GMC(theta),0<theta<=1/2, includes GRH. Its Corollary1 gives
E(X)<<_epsilon X^(1-2theta+epsilon), so even theta1/2 leaves X^epsilon,
not a proved empty exceptional set. That result is not a blanket
nonimplication theorem for all possible consequences of pair correlation.

Sources checked2026-09-09:
* https://arxiv.org/pdf/1606.00860v1 : CORRECTED Lemma5.1,p11,
  Theorem2.2,p3, and Section6 correction of[19],p14. This supersedes the
  O(sqrtN) error still printed in arXiv1206.0251v1 and the2015journalPDF.
* https://arxiv.org/abs/2107.06506 : only the classical consequence
  number of nontrivial zeros of height<=T is O(T logT) is needed here.
* https://www.research.unipd.it/retrieve/e14fb267-6015-3de1-e053-1705fe0ac030/%5B3%5D.pdf
  Languasco-Perelli1996 pp350-351, GMC hypothesis and Corollary1;
  formulas visually checked after garbled text extraction.
The exact helpers below guard coefficient extraction, signs, normalization
and error powers. No actual zeros, new prime range, or asymptotic numerical
test is evaluated. Polynomial and sieve results remain preserved components.
"""
from fractions import Fraction as F
from math import comb


def sum_coefficient(coefficients, target):
    """Coefficient of exp(-i*target*t) in the SQUARE of a real toy series."""
    return sum((v*coefficients.get(target-j,F(0))
                for j,v in coefficients.items()),F(0))


def difference_coefficient(coefficients, target):
    """Different object: coefficient in the squared modulus of a REAL toy series."""
    return sum((v*coefficients.get(j-target,F(0))
                for j,v in coefficients.items()),F(0))


def quadratic_window(t, step):
    """Exact positive finite-difference kernel, including both zero endpoints."""
    if type(t) not in (int,F) or type(step) is not int or step < 1:
        raise ValueError('rational t and positive integer step required')
    return sum(((-1)**j*comb(3,j)*max(F(0),F(t)-j*step)**2
                for j in range(4)),F(0))/(2*step**3)


def corrected_window_budget(power):
    """Exponent of the AVAILABLE corrected Cesaro error divided by the main."""
    if type(power) is not F or not 0 <= power <= 1:
        raise ValueError('rational H exponent in[0,1] required')
    relative = 2-3*power
    return {'relative_x_power':relative,'power_saving':relative<0}


def zero_tail_profile(c_over_two_pi):
    """N/logN powers in the proved tail for T=c*N*logN; constants excluded."""
    if type(c_over_two_pi) is not F or c_over_two_pi <= 0:
        raise ValueError('positive rational c/(2pi) required')
    return {'n_power':F(5,2)-c_over_two_pi,'logn_power':F(5,2)}
