"""A real-zero obstruction to deleting nonstationary pairs term by term.

Owner: Kevin's Goldbach research. Purpose: test whether the surviving
one-sided spectral kernel has a high-height region removable by absolute
nonstationary-phase estimates. The answer for the specified region is NO:
the finite-period endpoint leaves actual absolute mass >>N log^2N.
This is not a lower bound for the signed sum or an obstruction to all
cancellation methods. No RH, numerical zero certificate or novelty claim.

1. EXACT PHASE AND THE REGION TESTED.
Keep one_sided_zero_reduction.py: N is an integer>=3, a=1/N,
z=a+it, principal Log, and positive-height zeros rho=beta+i*gamma,
sigma=beta'+i*eta, with multiplicities and all 0<beta,beta'<1. Set
 b=beta+beta', h=gamma+eta, r=sqrt(a^2+t^2), theta=arg(z),
 J_N(rho,sigma)=e/pi Gamma(rho)Gamma(sigma)
                   *int_0^pi e^(iNt)z^(-rho-sigma)dt.
The retained coefficient is the REAL PART of the ordered sum of J_N,
including the diagonal. It is not the sum of |J_N|.

Factor K=Gamma(rho)Gamma(sigma)exp(pi*h/2). Then
 J_N=(e/pi)K int_0^pi A(t) exp(i*phi(t))dt,
 A(t)=r^(-b) exp[-h*(pi/2-theta)],
 phi(t)=Nt-h*log(r)-b*theta,
 phi'(t)=N-(h*t+b*a)/(a^2+t^2).                         (1)
Gamma phases are independent of t and remain in K; they are not dropped
from the signed sum. For u=Nt the stationary equation is exactly
 u^2-h*u+1-b=0.                                        (2)
It involves the SUM of zero heights, not their difference.

Test the actual zero band
 H_N={rho: 8piN < gamma <= 9piN}.
For rho,sigma in H_N, 16piN<h<=18piN and 0<b<2. This region is inside
the saved cutoff T=16piNlogN for sufficiently large N. On [a,pi],
 h*t/(a^2+t^2)>=h/(2t)>=8N,
so phi'<=-7N, and in fact |phi'| is comparable to N/t uniformly.
When b<1, (2) has a tiny positive root below u=1; when b>=1 that
small root is nonpositive. The large root exceeds piN. Thus the possible
tiny stationary point is confined to [0,a], which is dealt with separately.
We do NOT call the whole closed interval stationary-point-free.

2. UNIFORM ENDPOINT ASYMPTOTIC, WITH ALL ERRORS PAID.
On 0<=t<=a, theta<=pi/4 and r>=a, so
 int_0^a A(t)dt <= N^(b-1)exp(-pi*h/4) << N exp(-cN).
This pays the tiny stationary point absolutely, without dividing by phi'.

On [a,pi] put k=h/N in (16pi,18pi]. Since
 arctan(a/t)>=a/(2t),
 A(t)<=C t^(-2)exp(-8pi/t),
 |A'(t)|<=C t^(-4)exp(-8pi/t),
 |A''(t)|<=C t^(-6)exp(-8pi/t).                        (3)
Constants absorb t>=1 and are uniform in N,b,k. For example
 (log A)'=(-b*t+k)/(a^2+t^2),
whose first derivative is O(t^-3), while it is O(t^-2) itself.
Let q=1/phi'. The exact rational expression is
 q(t)=(a^2+t^2)/[N*(t^2-k*t+(1-b)*a^2)].
The denominator inside brackets has magnitude comparable to t here;
its first and second derivatives are bounded. Differentiating gives
 |q|<=C*t/N, |q'|<=C/N, |q''|<=C/(N*t).               (4)

Integrate exp(i*phi) twice by parts, using its derivative i*phi'*exp(i*phi).
The first boundary term at pi is A(pi)exp(i*phi(pi))/(i*phi'(pi)).
The second boundary term at pi is O(N^-2). At a the boundary terms
are exponentially small even after their polynomial factors. The remaining
integrand has modulus bounded by
 C/N^2 * [t^2|A''|+t|A'|+|A|],
which has bounded integral by (3). Together with the [0,a] estimate,
 int_0^pi A(t)exp(i*phi(t))dt
   = A(pi)exp(i*phi(pi))/(i*phi'(pi)) + O(N^-2).        (5)
This is uniform in the two zero real parts and throughout the height band.
Also A(pi) is bounded ABOVE AND BELOW by positive fixed constants, since
 b in(0,2) and h*arctan(1/(piN)) stays in a fixed compact positive range.
At pi, |phi'| is comparable to N. The main term in (5) therefore has
modulus at least c/N; its error cannot cancel it for sufficiently large N.
Uniform Stirling for beta,beta' in[0,1] at heights comparable to N gives
 |J_N(rho,sigma)| >= c/N * gamma^(beta-1/2)*eta^(beta'-1/2).       (6)
No numerical constant or onset is supplied. The small constant coming
from endpoint damping is fixed; it is not an asymptotically vanishing factor.

3. PAY THE SUM OVER ACTUAL ZEROS WITHOUT RH.
Let M_N count zeros in H_N with multiplicity and
 W_N=sum_(rho in H_N) gamma^(beta-1/2).
The functional-equation symmetry rho -> 1-conj(rho) keeps the positive
height, the band and multiplicity. In each two-point orbit the weights
are x and 1/x, whose sum is at least2. A fixed critical-line zero contributes1.
Thus W_N>=M_N with NO assertion that every real part is1/2.
The Riemann-von Mangoldt formula gives
 M_N=(1/2)NlogN+O(N).
Summing (6) over the ordered pairs (diagonal included) proves
 sum_(rho,sigma in H_N) |J_N(rho,sigma)|
      >= c/N * W_N^2 >= c' Nlog^2N.                   (7)
Consequently this actual nonstationary-height region cannot be deleted
by a termwise triangle inequality at o(N), O(N), or all-log precision.

Equation(7) says NOTHING about the real part of sum J_N. The endpoint
terms can cancel between different zero pairs or with other regions.
Discarding Gamma phases would erase exactly the information still needed.
It also does not prove that the full spectral coefficient is negative.
The sufficient lower bound C_(N,T)>=-(1-delta)N remains open.
The specific automatic absolute-deletion mechanism is retired; the exact
phase, endpoint expansion, and all earlier polynomial tools are preserved.

4. PRESERVE THE VALID INTERIOR DELETION COMPONENT.
Let chi be a fixed smooth function on [0,pi], vanishing on a neighborhood
of pi; it may equal1 near0. It is independent of N. Insert chi into the
integral defining J_N and call the result J_N^chi. For every fixed j,
the same differentiation gives
 |A^(j)|<=C_j t^(-2-2j)exp(-8pi/t),
 |q^(j)|<=C_j N^-1 t^(1-j) on [a,pi].
Four integrations by parts now have no upper boundary terms. Every lower
jet is exponentially small; the fourth remainder has integrable modulus
O_chi(N^-4), since each application contributes N^-1 times a polynomial
in1/t multiplying exp(-8pi/t). The [0,a] piece is still exponentially small.
Thus its integral is O_chi(N^-4). Uniform Stirling gives |K|<<N in the
fixed band, and there are O(N^2log^2N) ordered zero pairs. Consequently
 sum_(rho,sigma in H_N) |J_N^chi(rho,sigma)|
            <<_chi N^-1 log^2N.                       (8)
Choosing chi=1 outside any fixed small neighborhood of pi therefore
localizes the SAME band's signed contribution to that endpoint neighborhood
at the paid error in (8). This does not delete the endpoint contribution.
The statement is restricted to this band and a fixed cutoff; it is not
uniform for shrinking cutoff widths and does not bound the whole zero tail.

Sources checked2026-09-09:
* https://dlmf.nist.gov/25.10 : critical-strip zero symmetry about the
  real axis and Re(s)=1/2; used with multiplicities from the functional equation.
* https://arxiv.org/abs/2107.06506 : Hasanalizade-Shen-Wong, abstract;
  the stated Riemann-von Mangoldt estimate implies the displayed band count.
* one_sided_zero_reduction.py and pointwise_zero_pair_gate.py retain the
  actual coefficient normalization, licensed cutoff, and corrected sources.

The exact guards below check phase/sign and multiplicity bookkeeping.
A separate finite toy quadrature (not actual zeros and not a proof) at
b=1,h=17piN,N=8,16,32 agreed with (5): after normalizing by
A(pi)exp(i*phi(pi)), N^2 times the endpoint residual was about0.02123,
0.02122,0.02122. Doubling Simpson panels16384->32768 changed the values
by1.5e-11,1.2e-10,9.5e-10 respectively; these are observed differences,
not certified integration-error bounds. No prime range was computed.
"""
from fractions import Fraction as F


def stationary_numerator(u, height_sum, real_sum):
    """Exact numerator of phi'/N in the u=N*t coordinate."""
    return u*u-height_sum*u+1-real_sum


def phase_derivative(n, t, height_sum, real_sum):
    """Exact phi'(t), keeping the sum of both imaginary and real parts."""
    if type(n) is not int or n<3:
        raise ValueError('integer N>=3 required')
    if any(type(v) is not F for v in (t,height_sum,real_sum)):
        raise ValueError('rational t, height sum, and real-part sum required')
    if t<0 or height_sum<=0 or not 0<real_sum<2:
        raise ValueError('t>=0, positive height sum and 0<real sum<2 required')
    a=F(1,n)
    return n-(height_sum*t+real_sum*a)/(a*a+t*t)


def reflected_weight_mass(orbits, fixed_multiplicity=0):
    """Exact toy weights x,1/x with multiplicity; no actual zero evaluation."""
    if type(fixed_multiplicity) is not int or fixed_multiplicity<0:
        raise ValueError('nonnegative integer fixed-point multiplicity required')
    count=fixed_multiplicity
    weight=F(fixed_multiplicity)
    for x,multiplicity in orbits:
        if type(x) is not F or x<=0 or type(multiplicity) is not int or multiplicity<1:
            raise ValueError('positive rational orbit weight and integer multiplicity required')
        count+=2*multiplicity
        weight+=multiplicity*(x+1/x)
    return count,weight


def smooth_interior_mass_budget(integration_order):
    """Worst all-strip Gamma factor N times O(N^2 log^2N) ordered pairs."""
    if type(integration_order) is not int or integration_order<0:
        raise ValueError('nonnegative integer integration order required')
    power=3-integration_order
    return {'n_power':power,'logn_power':2,'all_log_small_on_n_scale':power<1}
