"""Pay identical-zero locations in the retained spectral sum without RH.

Owner: Kevin's Goldbach research. Purpose: separate the identical-location
diagonal from the still-open distinct-zero correlation. This uses an actual
uniform kernel bound, zero-free region, and classical zero density. It is
not a simple-zero assumption, prime-pair coverage, numerical zero certificate,
worldwide novelty claim, or square-root error for the full R formula.

1. PRECISE DIAGONAL AND KERNEL BOUND.
Let J_N be the finite-period positive-height kernel from
smooth_endpoint_cancellation.py, and let m(rho) be the multiplicity at a
DISTINCT complex zero location rho=beta+i*gamma, gamma>0. For fixed K>0,
 D_K(N)=sum_(distinct rho; 0<gamma<=KN) m(rho)^2 |J_N(rho,rho)|.
We prove, for every fixed A>0,
 D_K(N)<<_(A,K) N/log^A N.                             (1)
Every identical-location pair is counted, not just one diagonal entry per
copy of a zero. Distinct locations at the SAME height are not included.

The uniform pointwise estimate is
 |J_N(rho,rho)|<<N^(2beta-1)/sqrt(1+gamma).             (2)
It includes a stationary point reaching the finite endpoint; no infinite
vertical-line kernel has been substituted for the finite-period integral.

Put h=2gamma, b=2beta in(0,2), u=Nt, U=piN. After rescaling the integral,
its absolute size, apart from e/pi, is
 N^(b-1)|Gamma(rho)|^2 exp(pi*h/2)
                   *|int_0^U A(u)exp(i*phi(u))du|,
 A(u)=(1+u^2)^(-b/2)exp[-h*arctan(1/u)],
 phi(u)=u-(h/2)log(1+u^2)-b*arctan(u).
At u=0 the arctan(1/u) limit is pi/2. Exact derivatives are
 (log A)'=(h-bu)/(1+u^2),
 phi'=1-(hu+b)/(1+u^2),
 phi''=[h(u^2-1)+2bu]/(1+u^2)^2.                     (3)
For h>=8 we show, UNIFORMLY for every terminal U>=0,
 |int_0^U A exp(i*phi)|<<h^(1/2-b).                    (4)

On [0,1], the absolute integral is <=exp(-pi*h/4). On [1,h/4], phi'<0,
|phi'| is comparable to h/u, phi' is increasing, and A is increasing
because h-bu>=h/2. Hence A/|phi'| is increasing. One integration by
parts bounds any initial portion of this interval by O(h^-b).

On [h/4,4h], phi'' is comparable to1/h, and A has at most one turning
point. Its supremum plus total variation is O(h^-b), uniformly in b.
For completeness, an unweighted phase integral on any subinterval costs
O(sqrt h): the set |phi'|<=h^-1/2 has length O(sqrt h), while its two
complementary intervals have monotone derivative of magnitude at least
h^-1/2 and cost O(sqrt h) by one integration by parts. Partial summation
with the amplitude then gives O(h^(1/2-b)). This includes a terminal
point U within the stationary region.

On [4h,infinity), phi'>2/3 is increasing. The amplitude again has at most
one turning point and supremum plus variation O(h^-b). The first-derivative
bound and partial summation give O(h^-b) on every finite terminal interval.
These four regions prove (4). Uniform Stirling yields
|Gamma(rho)|^2exp(pi*h/2)<<gamma^(b-1), which proves (2) for h>=8.
The actual zeros with 0<h<8 form a finite set. On a fixed initial interval
their integral is bounded absolutely, and on a sufficiently large u-tail
the same first-derivative argument applies. Absorb this finite set into
the constant in (2); no numerical first-zero or simple-zero claim is needed.

2. MULTIPLICITY AND THE ACTUAL DENSITY INPUT.
Riemann-von Mangoldt in the form
 N_z(T)=T/(2pi)log(T/(2pi*e))+O(log(T+3))
counts with multiplicity. Applying it on [gamma-1,gamma+1] gives
 m(rho)<<log(gamma+3).
Thus for gamma<=KN, (2) converts D_K to at most C_K logN times the
corresponding sum over zeros counted with multiplicity ONCE. Squaring
multiplicity has not been lost; it costs one logarithm.

Use the uniform classical Ingham density estimate
 N_z(sigma,T)<<T^[3(1-sigma)/(2-sigma)] log^5T,
                         1/2<=sigma<=1, T sufficiently large, (5)
where N_z(sigma,T) counts beta>=sigma with multiplicity. This is explicitly
supported by Chourasiya-Simonic arXiv2507.15184v2, Corollary1 and Table1:
their logarithmic exponent (7-5sigma)/(2-sigma) lies in[2,3], with finite
constants on intervals covering[1/2,1]. We only use the weaker exponent5.
The cited explicit corollary starts at a fixed height; every high-height
band below is eventually above it. No computed zero list is used here.

Also retain the classical zero-free region from one_sided_zero_reduction.py:
 beta<=1-c/log(gamma+3), c>0 fixed, for every nontrivial zero.              (6)
The compact low-height extension is preserved; no numerical c or onset.

3. PAY LOW HEIGHTS BEFORE APPLYING DENSITY.
Set L=logN, alpha=min(1,sqrt c), H0=exp(alpha*sqrtL). For sufficiently
large N, log(H0+3)<=2alpha*sqrtL, and alpha^2<=c. Consequently for
gamma<=H0,
 N^(2beta-1)<=N exp[-(c/alpha)*sqrtL].
Partial summation of the cumulative zero count gives
 sum_(0<gamma<=H0), with multiplicity, (1+gamma)^-1/2
                                     <<sqrtH0 log(2H0).
After the extra multiplicity logarithm, the low-height diagonal is
 <<_K N L^2 exp[-alpha*sqrtL/2].                       (7)
Indeed alpha/2-c/alpha<=-alpha/2. This small-height step is essential;
a density bound applied at a fixed height alone would not give the desired
uniform rate as N grows.

4. PAY EVERY REMAINING HEIGHT BAND WITH DENSITY.
Split H0<gamma<=KN into dyadic bands (H,2H], with H0<=H<=KN. There
are O_K(L) bands. Zeros with beta<=1/2 cost O_K(sqrtH L^2) per band,
including the extra multiplicity logarithm. For beta>1/2 use exactly
 N^(2beta-1)=1+2L int_(1/2)^beta N^(2sigma-1)d sigma,
then bound the cumulative count inside that integral by (5) at height2H.
Writing u=1-sigma gives the per-band upper bound
 C_K sqrtH L^2
 +C_K N L^7 int_0^(1/2) N^(-2u) H^[3u/(1+u)-1/2]du.  (8)
All factors are paid: log^5H from (5), L from partial summation in beta,
and L from the multiplicity-squared conversion.

The remaining exponents have simple uniform bounds:
* 0<=u<=1/10: 3u/(1+u)<=3/11, so the integrand is <=H0^(-5/22).
* 1/10<=u<=1/5: the H exponent is <=0, and N^(-2u)<=N^-1/5.
* 1/5<=u<=1/2: the H exponent is >=0, so use H<=KN and
  3u/(1+u)<=5u/2. The resulting N exponent is at most
  u/2-1/2<=-1/4, with a bounded K factor.
Summing all height bands therefore costs
 O_K(sqrtN L^3+N L^8[H0^-5/22+N^-1/5]).               (9)
Together, (7) and (9) give for some fixed c1>0
 D_K(N)<<_K N L^8 exp(-c1 sqrtL)<<_(A,K) N/L^A.
This is an all-log saving on the N scale, not a claimed square-root or
fixed power saving for the complete diagonal across arbitrarily low heights.

5. APPLY ONLY TO THE DIAGONAL ACTUALLY PAID.
In nonstationary_spectral_reduction.py the retained multiplier
1-Psi((gamma+eta)/N) lies in[0,1]. On an identical pair it is supported
on gamma<=((pi+2delta)/2)N, so (1) deletes the entire equal-location
diagonal absolutely. The remaining finite sum is over DISTINCT complex
zero locations, with their product multiplicities and the same height-sum
and smooth-weight restrictions. Its signed lower margin is still OPEN.
In particular two different real parts at the same ordinate are still
distinct locations. No additional correlation estimate follows from (1).
The full R formula retains its previously proved O_A(N/log^A N) error.

Sources checked2026-09-09:
* https://arxiv.org/pdf/2507.15184v2 : Chourasiya-Simonic, definitions onp1,
  Corollary1 and Table1 onp2; only the weaker uniform classical density
  consequence (5) is used. v2 was checked, not mixed with v1's presentation.
* https://arxiv.org/abs/2107.06506 : Riemann-von Mangoldt remainder,
  including the cumulative and local multiplicity consequences above.
* https://arxiv.org/pdf/2212.06867v1 : Theorem1.3 and the already reviewed
  compact-height extension of the classical zero-free region.
No new prime range, numerical zero computation, effective onset or novelty
claim. All polynomial tools and earlier source corrections remain preserved.
"""
from fractions import Fraction as F


def normalized_phase_data(h, b, u):
    """Exact rescaled phase and logarithmic-amplitude derivatives."""
    if any(type(v) is not F for v in (h,b,u)) or h<=0 or not 0<b<2 or u<0:
        raise ValueError('rational h>0, 0<b<2 and u>=0 required')
    denominator=1+u*u
    return {'phase_first':1-(h*u+b)/denominator,
            'phase_second':(h*(u*u-1)+2*b*u)/denominator**2,
            'log_amplitude_first':(h-b*u)/denominator}


def density_integrand_powers(u):
    """Exact N/H powers after dividing the high-band diagonal bound by N."""
    if type(u) is not F or not 0<=u<=F(1,2):
        raise ValueError('rational u=1-sigma in[0,1/2] required')
    return {'n_power':-2*u,'h_power':3*u/(1+u)-F(1,2)}


def identical_location_pair_counts(multiplicities):
    """Locations are separate keys even when two locations have equal heights."""
    if any(type(m) is not int or m<1 for m in multiplicities.values()):
        raise ValueError('positive integer multiplicities required')
    copies=sum(multiplicities.values())
    identical=sum(m*m for m in multiplicities.values())
    return {'copies':copies,'identical_pairs':identical,
            'distinct_location_pairs':copies*copies-identical}


def low_height_relative_exponent(alpha, c):
    """Coefficient of sqrt(logN); a bad height split can make it positive."""
    if type(alpha) is not F or type(c) is not F or alpha<=0 or c<=0:
        raise ValueError('positive rational alpha and zero-free constant proxy required')
    return alpha/2-c/alpha
