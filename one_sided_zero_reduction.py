"""Delete the damped zero interactions from the actual pointwise pair kernel.

Owner: Kevin's Goldbach research. Purpose: isolate which spectral interactions
still require a signed lower bound, without assuming RH or abandoning the
preserved polynomial/sieve components. This is an asymptotic analytic reduction,
not a numerical zero certificate, new coverage, or a novelty claim.

1. SETUP AND THE ARITHMETIC INPUT.
Use pointwise_zero_pair_gate.py with N>=3, L=logN, a=1/N, z=a+it,
principal Log, and -pi<=t<=pi. All nontrivial zeros rho=beta+i*gamma,
0<beta<1, occur with multiplicities; there are no real zeros in this strip.
Write
 Z(z)=Z_+(z)+Z_-(z), Z_+ over gamma>0, Z_- over gamma<0,
 I_N[f]=e/(2pi) int_(-pi)^pi f(a+it)e^(iNt)dt,
 B_N=I_N[Z^2].
The saved, corrected explicit formula proves
 ||Z||_2 << sqrt(NL)+L^2,
 R(N)=2psi(N-1)-N+B_N+O(sqrtN L^(5/2)+L^4).             (1)
The zero sums converge absolutely and uniformly for each fixed N on this
period. Real parts are NOT replaced by1/2.

The additional input is the classical zeta zero-free region
 beta <= 1-c/log(|gamma|+3)                             (2)
for a fixed c>0. Mossinghoff-Trudgian-Yang, arXiv:2212.06867v1,
Theorem1.3, printedp3, gives a stronger explicit classical region for
|gamma|>=2. On the compact lower-height set there are finitely many zeros
and none on Re(s)=1, so decreasing c gives (2) for every zero. We supply
no numerical c or onset. This is not an assumption of RH or a claim about
the optimal current zero-free constant.

2. PAY THE SUPPRESSED HALF-PERIOD NORM, INCLUDING SMALL t.
For t>=0 and a negative-height zero rho=beta-i*gamma, gamma>0, Stirling gives
 |Gamma(rho)z^(-rho)|
  << (1+gamma)^(1/2) exp(-pi*gamma/2) |z|^(-beta),       (3)
because the additional factor exp(-gamma*arg(z)) is <=1. The finitely many
low zeros are absorbed into a fixed constant. The corresponding factor for
a positive-height zero is exp(+gamma*arg(z)); it CANNOT be suppressed in
this fashion near arg(z)=pi/2.

The radial norms, uniformly for 0<beta<1, satisfy
 || |a+it|^(-beta) ||_(L2[0,pi]) <<
    N^(1/4)                 if beta<=3/4,
    N^(beta-1/2)            if beta>3/4.                (4)
For the first line, on |z|<=1 use |z|^(-2beta)<=|z|^(-3/2),
whose integral is O(sqrtN); the remaining interval costs O(1).
For the second, put t=a*u and use the uniform boundedness of
int_0^infinity (1+u^2)^(-beta)du for beta>=3/4.
This split avoids a false uniform constant near beta=1/2, and does not
silently put every zero on the critical line.

Let Q_N=||Z_-||_(L2[0,pi]). Minkowski, (2)-(4), and the classical count
number of zeros of height<=T = O(T log(2T)) imply, for U>=2,
 Q_N << N^(1/4)+sqrtN * {
       exp[-c L/log(U+3)] + exp[-pi U/4] }.            (5)
Indeed the Gamma coefficients in (3) are absolutely summable. For
gamma<=U and beta>3/4, extract N^(beta-1)<=exp[-c L/log(U+3)].
For gamma>U use N^(beta-1)<=1; cumulative zero counting and the exponential
in (3) give a tail O(exp[-pi U/4]), with polynomial factors absorbed.
The beta<=3/4 terms cost O(N^(1/4)) over all heights.

For sufficiently large N take U=sqrtL. Both exponentials in (5), and
N^(1/4)/sqrtN, are O(exp[-c0 sqrtL]) for a fixed c0>0. Thus
 Q_N << sqrtN exp[-c0 sqrtL] <<_A sqrtN/L^A             (6)
for every fixed A>0. Reflection gives the same suppressed norm for Z_+
on [-pi,0]. The proof uses positive absolute majorants, so (5)-(6) also
hold for ANY finite truncation of the suppressed zero sum, uniformly in
its height cutoff. No such claim is made here for the TOTAL truncated norm.

3. DELETE ONLY TERMS WHOSE COST HAS NOW BEEN PAID.
For 0<=t<=pi put P(t)=Z_+(a+it), Q(t)=Z_-(a+it). Conjugation gives
 Z_+(a-it)=conj(Q(t)), Z_-(a-it)=conj(P(t)),
so EXACTLY
 B_N=e/pi Re int_0^pi e^(iNt)(P(t)+Q(t))^2 dt.         (7)
Also ||P||_(L2[0,pi]) <= ||Z||_2+||Q||_(L2[0,pi])
<<sqrt(NL) for sufficiently large N. Cauchy therefore pays
 int_0^pi |2PQ+Q^2|dt
    << N sqrtL exp[-c0 sqrtL] <<_A N/L^A.             (8)
The opposite-height-sign pair contribution is the 2PQ term in (7).
In addition, the same-sign square Q^2 on its suppressed half is negligible.
Consequently
 B_N=C_N+O_A(N/L^A),
 C_N=e/pi Re int_0^pi e^(iNt) Z_+(a+it)^2 dt.          (9)
The survivor is a SQUARE, not a squared modulus. It is a sum over ordered
positive-height pairs, including the diagonal. Taking its real part does
not make it nonnegative; no lower bound for C_N has been proved.

4. LICENSED FINITE HEIGHT AND THE REMAINING GAP.
The saved tail proof applies separately to Z_+ as well as to Z. For fixed
K>=3 and T=2pi(K+5)NlogN, sup|Z_+-Z_(+,T)|<<_K N^(-K).
Using the proved full norm, replacement of C_N by C_(N,T) costs
O_K(N^(-K)*sqrt(NL)+N^(-2K)). It follows for every fixed A>0 that
 R(N)=2psi(N-1)-N+C_(N,T)+O_A(N/L^A).                 (10)
Here K can be fixed at3; no uniformity in growing A is asserted. The
original pointwise error in (1) is also all-log small on the N scale.
First proving (8) for the FULL sums, then using the paid tail, is essential:
we have NOT proved (8) uniformly for arbitrary total truncation heights.
The cutoff requires all strip zeros to T, with multiplicities, and does
not certify a computationally supplied list of critical-line zeros.

PNT gives 2psi(N-1)-N=N+o(N). A sufficient, still UNPROVED input is
 C_(N,T) >= -(1-delta)N
for a fixed delta>0 and every sufficiently large even N. That would yield
R(N)>=delta N+o(N), and the saved O(sqrtN log^2N) proper-power bound would
give genuine prime pairs. There is no new positive margin or effective
coverage onset. This reduction does not identify ordinary difference-height
pair correlation or a positive energy with the surviving complex kernel.

Sources checked2026-09-09:
* https://arxiv.org/pdf/2212.06867v1 : Theorem1.3, printedp3; only the
  classical c/log(|gamma|+3) consequence is used, not numerical optimization.
* https://arxiv.org/abs/2107.06506 : only the classical O(TlogT) zero count.
* pointwise_zero_pair_gate.py : pointwise transfer, norms, finite-height tail,
  and the preserved arXiv1606.00860 correction to the2015 explicit formula.
The helpers below guard the sign, real-part, and norm-budget pitfalls;
they do not numerically test an asymptotic theorem or evaluate actual zeros.
"""
from fractions import Fraction as F


def gamma_exponential_rate(height_sign, arg_over_pi):
    """Coefficient of pi*abs(gamma) in the Stirling/complex-power exponential."""
    if type(height_sign) is not int or height_sign not in (-1,1):
        raise ValueError('height sign must be -1 or 1')
    if type(arg_over_pi) is not F or not -F(1,2)<arg_over_pi<F(1,2):
        raise ValueError('rational principal argument divided by pi required')
    return -F(1,2)+height_sign*arg_over_pi


def radial_norm_power(beta):
    """Uniform upper-bound exponent in (4), not an exact norm or an RH claim."""
    if type(beta) is not F or not 0<beta<1:
        raise ValueError('rational beta strictly inside the critical strip required')
    return F(1,4) if beta<=F(3,4) else beta-F(1,2)


def reflected_square_terms(p, q, phase):
    """Toy conjugate-half algebra, with the common e/(2pi) factor omitted."""
    return {
        'full':2*(phase*(p+q)**2).real,
        'retained':2*(phase*p**2).real,
        'discarded':2*(phase*(2*p*q+q**2)).real,
    }


def cross_log_saving(suppressed_norm_saving):
    """Saving in sqrtN/L^s times sqrt(NL); constants excluded."""
    if type(suppressed_norm_saving) is not F or suppressed_norm_saving<=0:
        raise ValueError('positive rational logarithmic saving required')
    return suppressed_norm_saving-F(1,2)
