"""Transfer arithmetic energy to the actual comparable linear-height kernel.

Owner: Kevin's Goldbach research. Purpose: test the missing passage from
linear arithmetic moments to an actual coupled spectral contribution.
This gives a bound for one fixed smooth band, not an all-log deletion or
the sufficient Goldbach lower margin. No RH or target averaging is used.

1. RESULT AND NORMALIZATION.
Let N be a sufficiently large positive integer, c=1/100, and let chi be
fixed real C_c^infinity((c,2c)). Keep the ACTUAL finite-period kernel
 J_N(rho,sigma)=(e/pi)Gamma(rho)Gamma(sigma)
                  *int_0^pi exp(iNt)(alpha+it)^(-rho-sigma)dt,
 alpha=1/N, rho=beta+i*gamma, sigma=beta'+i*eta.
All zeros have their actual real parts and multiplicities. We prove
 |sum_(rho,sigma) chi(gamma/N)chi(eta/N) J_N(rho,sigma)|
                                                    <<_chi NlogN. (1)
Both height supports are positive and compact, so these sums are finite;
pairs are ordered and include the diagonal. This is a COMPLEX bound.
The count-compatible model's order Nlog^2N reinforcement cannot persist
in this actual smooth band. Bound(1) still exceeds the order N scale
needed for the full signed lower margin, and does not delete this band
with an all-log error. Other height regions remain outside this theorem.

2. AN EXACT BETA QUOTIENT, NOT A SUBSTITUTED FINITE-PERIOD FORMULA.
Define
 B_N(rho,sigma)=2 N^(rho+sigma-1)
                    *Gamma(rho)Gamma(sigma)/Gamma(rho+sigma).
Euler's beta integral gives the EXACT identity
 sum chi(gamma/N)chi(eta/N) B_N(rho,sigma)
  =2 int_0^1 S_N(aN)S_N((1-a)N)/sqrt(a(1-a)) da,                  (2)
with S_N as in arithmetic_zero_moment.py. The factor2 and the measure
da are essential. There is no conjugation in (2). For each summand the
integrand is N^(rho+sigma-1)*a^(rho-1)*(1-a)^(sigma-1).
Its absolute integrability follows from beta,beta'>0; the finite sums
can therefore be exchanged with the integral without a convergence limit.

Fresh primary check2026-09-09: NIST DLMF5.12.1,
https://dlmf.nist.gov/5.12.E1 . The section explicitly requires positive
real parts for the two complex parameters, exactly as used here. We do
not identify B_N with J_N. Their difference is paid in Sections5-7.

3. LOCALIZE THE BETA INTEGRAL WITH ALL REAL-PART COSTS INCLUDED.
Choose fixed smooth zeta, equal1 on[3/10,7/10], supported in(1/4,3/4).
For s=gamma/N,t=eta/N in[c,2c], the phase of the beta integral is
 N*theta(a), theta(a)=s loga+t log(1-a).
Its stationary point s/(s+t) is in[1/3,2/3]. On the left support of
1-zeta, a<=3/10, the numerator of its derivative satisfies
 s(1-a)-ta>=c(1-3a)>=c/10.
Thus 1/theta'(a)=a(1-a)/[s(1-a)-ta] is a times a uniformly smooth
function through a=0. On the right it is (1-a) times such a function.

The left amplitude is a^(beta-1)*(1-a)^(beta'-1)*(1-zeta(a)). Applying
the integration-by-parts adjoint -d/da[A/(iN theta')] three times
gives N^-3 a^(beta-1) times uniformly bounded smooth coefficients,
for beta,beta' in(0,1). Boundary jets vanish at0 since they contain
a^beta, and at the other end by the smooth cutoff. The right endpoint
is identical with beta' in place of beta. Consequently the omitted
beta integral, before its factor N^(rho+sigma-1), costs
 O_chi(N^-3*(1/beta+1/beta')).                                    (3)
We do not assert uniform integrability as beta approaches0 for free.

The retained classical zero-free region and reflection rho->1-conj(rho)
give beta,beta'>=c_0/logN for heights in this fixed linear band, with
some fixed c_0>0. This is the already reviewed source consequence in
spectral_diagonal_bound.py, with no numerical onset asserted. Equation(3)
therefore costs O(N^-3 logN). The density first-moment proof from
arithmetic_zero_energy.py applies also at x=N itself and gives
 W=sum_(cN<=gamma<=2cN) N^(beta-1/2)<<Nlog^6N.
Indeed its same exponent is 1/2-u+D(u)<=1; changing a fixed comparison
constant for x~N does not change it. Summing the absolute endpoint
errors with product multiplicities costs
 N^-3 logN * W^2 <<N^-1 log^13N.                                  (4)

4. EXTEND THE ENERGY TO THE FIXED CENTRAL INTERVAL, THEN USE CAUCHY.
The proof of arithmetic_zero_energy.py extends to a in[1/4,3/4].
Here are the actual changed constants, rather than a free new mask:
the prime window is supported on n in[N/8,2N], and the mean value
bounds on its support are
 (2/3)|n-aN|<=|Nlog(n/(aN))|<=8|n-aN|.
The row Schur constant remains fixed and the integrated column constant
is still O(1/N). Also sum Lambda(n)^2/n<=8/N sum_(n<=2N)Lambda(n)^2
is O(logN) by the same Chebyshev argument. The density replacement,
pole estimate and Gamma integration remain uniform for this fixed
x~N range. Thus
 int_(1/4)^(3/4)|S_N(aN)|^2 da<<_chi NlogN.                         (5)
The interval is preserved by a->1-a. Since zeta(a)/sqrt(a(1-a)) is
bounded, Cauchy applied to (2)'s central integral gives O_chi(NlogN).
Together with (4), this bounds the B_N sum by O_chi(NlogN).

5. FULL-LINE INVERSION IS VALID EVEN WHEN beta+beta'<=1.
Put w=rho+sigma=b+ih, with b>0. For each fixed N and w, the elementary
Gamma/Laplace representation of (alpha+it)^(-w) gives
 (1/(2pi))int_R exp(iNt)(alpha+it)^(-w)dt
                         =exp(-alpha*N)*N^(w-1)/Gamma(w).         (6)
One direct justification inserts exp(-epsilon*t^2). Absolute Fubini
then turns the inner Fourier integral into the Gaussian approximate
identity (4pi*epsilon)^(-1/2)exp[-(N-u)^2/(4epsilon)] applied to
u^(w-1)exp(-alpha*u)/Gamma(w), u>0. This function is integrable and
continuous at N>0, giving (6) as epsilon decreases to0.
The ordinary two improper half-line integrals have the same limit:
their tails converge by one integration against exp(iNt), since the
remaining amplitude is O_w(|t|^-b) and its derivative O_w(|t|^-b-1).
For Gaussian regularization, the extra derivative tail is bounded by
2epsilon int_T^infinity t*exp(-epsilon*t^2)*t^-b dt<=T^-b.
Thus its removal commutes with the improper limit. No absolute integral
over t or estimate uniform in w is asserted at this justification step.
Multiplying (6) by 2e Gamma(rho)Gamma(sigma) gives B_N exactly.

It follows that J_N equals B_N minus its negative half-line contribution
and its positive tail from pi to infinity, each normalized by e/pi.
The following estimates are uniform for the actual band.

6. THE NEGATIVE HALF-LINE IS EXPONENTIALLY PAID.
Here h>=2cN. Uniform Stirling gives
 |Gamma(rho)Gamma(sigma)|<=C N*exp(-pi*h/2).
Writing t=-u, the modulus of (alpha-iu)^(-w) is
 (alpha^2+u^2)^(-b/2)*exp[-h arctan(u/alpha)].
For 0<=u<=1, omit the last factor and bound the integral by N^b<=N^2.
For u>=1, integrate exp(-iNu) once. The remaining function has modulus
at most u^-b and derivative at most |w|u^-b-1, so this part costs
(1+|w|/b)/N<<logN, since |w|=O(N) and b>=2c_0/logN.
The product with the Gamma factors is exponentially small, even after
all O(N^2log^2N) copy-counted pairs are summed. No negative-zero sum
or infinite spectral interchange is introduced by this step.

7. THE UPPER TAIL HAS A PROJECTABLE ENDPOINT AND A SMALL REMAINDER.
Let z_*=alpha+i*pi, f_rho=Gamma(rho)z_*^(-rho), r(t)=|alpha+it|,
v(t)=arg(alpha+it). Factoring f_rho*f_sigma from the upper tail leaves
 int_pi^infinity D(t)exp(i Phi(t))dt,
 D(t)=[r(t)/r(pi)]^-b *exp[h(v(t)-v(pi))],
 Phi(t)=Nt-hlog[r(t)/r(pi)]-b[v(t)-v(pi)].
We have D(pi)=1, Phi(pi)=Npi, and
 Phi'(t)=N-h*t/(alpha^2+t^2)-b*alpha/(alpha^2+t^2)>=c_1 N,
because h<=4cN and t>=pi. With q(t)=1/Phi'(t),
 q=O(N^-1), q'=O(N^-1 t^-2), q''=O(N^-1 t^-3).
Also D(t)<=C(t/pi)^-b. The exact logarithmic derivative
 D'/D=(-b*t+h*alpha)/(alpha^2+t^2)
shows ||D'||_1=O(1), uniformly as b decreases to0: retain the factor b
in its b/t part, whose integral is bounded; the other part decays as
t^-2. Differentiating again gives ||D''||_1=O(1). These facts, D's
bounded supremum, and the q derivative bounds justify two integrations,
with a vanishing upper boundary since b>0. They give
 int_pi^infinity D exp(i Phi)dt
       = i*(-1)^N/[N*d]+O(N^-2), d=1-h/(pi*N).                    (7)
The sign is POSITIVE i for the upper tail; it is subtracted from B_N
to obtain J_N. At pi, Phi'=Nd+O(N^-1), so q(pi)=1/(Nd)+O(N^-3).
The second boundary and residual derivative integral both cost N^-2.

For the leading tail, the fixed smooth weight
 g(s,t)=chi(s)chi(t)/(1-(s+t)/pi)
has support in a positive rectangle with its denominator bounded away
from0. The single-zero projection proved in smooth_endpoint_cancellation.py
applies to ANY fixed smooth compact positive weight: sum f_rho*w(gamma/N)
=A_N(w)+O_w(sqrtN logN)=O_w(N). Its corrected2016 explicit-formula
source and its seminorm control remain essential. A fixed smooth tensor
expansion, as already proved there, gives sum f_rho*f_sigma*g=O_g(N^2).
No condition n+m=N appears in this endpoint main, and no prime-pair
theorem is used. Dividing by N pays O_chi(N) for the leading tail.

For the remainder in (7), Stirling at z_* and gamma~N give
 |f_rho|<=C N^(beta-1/2).
The same first moment W therefore bounds sum|chi(gamma/N)f_rho| by
O_chi(Nlog^6N). Hence the summed remainder costs
 N^-2*(Nlog^6N)^2=O_chi(log^12N).                                 (8)
Using the old crude N^(3/2)logN mass here would lose the desired log.

Equations(2)-(8) prove (1) for the ACTUAL finite-period sum. Every
finite/infinite-period correction has been estimated before promotion.
No all-log bound, hard band, growing family of cutoffs, arbitrary
coupled spectral mask, positive lower margin or new coverage follows.
The arithmetic moment and energy remain reusable, together with the
polynomial components and all prior signed deletions/source corrections.
"""
from fractions import Fraction as F
from math import factorial


def integer_beta_integral(p, q):
    """Exact positive-integer beta identity; not a zero evaluation."""
    if any(type(v) is not int or v<1 for v in (p,q)):
        raise ValueError('positive integer beta parameters required')
    return F(factorial(p-1)*factorial(q-1),factorial(p+q-1))


def left_phase_numerator(s, t, a):
    if any(type(v) is not F for v in (s,t,a)) or s<=0 or t<=0 or not 0<=a<=1:
        raise ValueError('positive rational heights and a in[0,1] required')
    return s*(1-a)-t*a


def upper_tail_imaginary_coefficient(height_sum, endpoint):
    """Rational algebra proxy for +1/(1-h/(N*pi)); excludes transition."""
    if any(type(v) is not F for v in (height_sum,endpoint)) or not 0<=height_sum<endpoint:
        raise ValueError('rational0<=height_sum<positive endpoint required')
    return 1/(1-height_sum/endpoint)


def transfer_error_powers(single_mass_power=F(1), beta_integrations=3):
    if type(single_mass_power) is not F or single_mass_power<0:
        raise ValueError('nonnegative rational single-mass exponent required')
    if type(beta_integrations) is not int or beta_integrations<1:
        raise ValueError('positive integer integration count required')
    return {'upper_tail_remainder':2*single_mass_power-2,
            'beta_endpoint_remainder':2*single_mass_power-beta_integrations}
