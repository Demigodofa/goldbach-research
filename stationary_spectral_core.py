"""An actual interior absolute-mass obstruction and a paid cosine reduction.

Owner: Kevin's Goldbach research. Purpose: identify a surviving region that
requires signed cancellation, and preserve its phase with a controlled total
error. The cosine sum below remains OPEN. This is no Goldbach obstruction,
prime-pair coverage theorem, RH assumption, numerical zero list or novelty
claim. All polynomial components and earlier source corrections persist.

1. THE ACTUAL STATIONARY BAND.
Keep the finite-period positive-zero kernel
 J_N(rho,sigma)=(e/pi)Gamma(rho)Gamma(sigma)
                   *int_0^pi exp(iNt)(1/N+it)^(-rho-sigma)dt.
Zeros rho=beta+i*gamma, sigma=beta'+i*eta have0<beta,beta'<1 and positive
heights. Let T=N^(2/3), and restrict gamma,eta to(T,2T], counting all
ordered copies and therefore every product multiplicity. Write h=gamma+eta
and b=beta+beta'. For large N, U=piN>=4h throughout this band.

We prove that the ACTUAL surviving part of this band has
 sum |J_N(rho,sigma)| >> N log^2N,                                    (1)
even after the previously paid near-height strip is removed. Thus termwise
absolute deletion of this interior region cannot give o(N) or an all-log
error. This asserts nothing about the SIGNED real sum: its terms may cancel
with each other or with other retained regions.

In addition, define the positive amplitude and real phase
 A_N(rho,sigma)=2sqrt(2pi)/sqrt h
             *(N*gamma/h)^(beta-1/2)*(N*eta/h)^(beta'-1/2),
 Theta_N(gamma,eta)=gamma log(N*gamma/h)+eta log(N*eta/h)-pi/4.
For the full band or any subset of it, in particular the retained separated
band, we prove the ACTUAL signed reduction
 Re sum J_N = sum A_N*cos(Theta_N)+O(N^(31/45)log^12N).                 (2)
The leading phase is independent of beta,beta'; those real parts remain
in the positive amplitude. The cosine sum itself is not bounded by (2).

2. A UNIFORM FINITE-INTERVAL STATIONARY MAIN.
After u=Nt, use the exact normalized functions in spectral_diagonal_bound.py:
 A(u)=(1+u^2)^(-b/2)exp[-h arctan(1/u)],
 phi(u)=u-(h/2)log(1+u^2)-b arctan u,
 I(h,b,U)=int_0^U A(u)exp(i phi(u))du.
The limit at u=0 is understood. We establish, uniformly0<b<2, U>=4h,
 I=sqrt(2pi)e^-1 h^(1/2-b)
       *exp{i[h-hlogh-b*pi/2+pi/4]}+O(h^-b), h tending to infinity.    (3)

Choose fixed smooth chi supported in(1/2,2), equal1 on a neighborhood of1.
Outside chi(u/h), the integral is O(h^-b). Indeed [0,1] is exponentially
small, and [1,h/4] has the already paid monotone first-derivative bound.
On the remaining compact u/h range outside a fixed neighborhood of1,
phi' is bounded away from0, phi'' has fixed sign for u>=1, and amplitude
supremum plus total variation is O(h^-b). Smooth cutoff derivatives have
the same paid scale. The tail u>=4h has increasing phi'>2/3 and the same
amplitude variation bound, valid up to EVERY finite U>=4h. This also pays
the possible tiny stationary point in[0,1]; it was not ignored.

In the central integral put u=hv. Uniformly on the fixed compact support,
 A(hv)=h^-b v^-b exp(-1/v)[1+O(h^-2)],
 phi(hv)=h(v-logv-logh)-b*pi/2+O(h^-1).
Replacing these gives absolute error O(h^-b), after the du=h dv factor.
It remains to evaluate the smooth compact integral with phase
f(v)=v-logv. Its unique stationary point is1, with f(1)=1 and f''(1)=1.

For completeness, use the smooth coordinate
 w=sign(v-1)*sqrt[2(f(v)-1)].
It is a diffeomorphism on the support interval and has derivative1 at1.
The transformed amplitude B_b(w) is smooth, compactly supported, with
uniform C^2 bounds in0<=b<=2, and B_b(0)=e^-1. For a fixed smooth chi0
equal1 near0, write B_b=B_b(0)chi0+w*q_b. The quotient q_b is smooth
and compactly supported, with ||q_b'||_1 uniformly bounded. Integration
by parts gives int w*q_b exp(ihw^2/2)dw=O(h^-1). The cutoff Fresnel
integral is exp(i*pi/4)sqrt(2pi/h)+O(h^-1): the full Fresnel value follows
by Gaussian regularization, and its tails outside chi0 cost O(h^-1) by
one integration by parts. Therefore the central integral is
e^(ih)*e^-1*exp(i*pi/4)sqrt(2pi/h)+O(h^-1).
Restoring h^(1-b) and the extracted phase proves (3). In particular the
main has a nonzero uniform magnitude; the error is relatively O(h^-1/2).

3. RESTORE THE GAMMA PHASES AND THE EXACT N POWER.
The exact rescaling before (3) is
 J_N=(e/pi)Gamma(rho)Gamma(sigma)N^(rho+sigma-1)exp(pi h/2) I.
Uniform complex Stirling on this band is
 Gamma(beta+i*gamma)=sqrt(2pi)gamma^(beta-1/2)exp(-pi gamma/2)
   *exp{i[gamma loggamma-gamma+(beta-1/2)pi/2]}[1+O(1/T)].
Multiplying it out with (3) yields
 J_N=A_N exp(i Theta_N)[1+O(T^-1/2)].                                 (4)
The constant is (e/pi)*(2pi)*sqrt(2pi)/e=2sqrt(2pi).
The real-part phase contributions cancel as
 (b-1)pi/2-b*pi/2+pi/4=-pi/4.
The Gamma linear height terms cancel the +h in (3), leaving exactly
Theta_N above. Neither Gamma phases nor N^(i h) have been discarded.

4. FUNCTIONAL REFLECTION FORCES ACTUAL ABSOLUTE MASS.
For sufficiently large T, (4) gives |J_N|>=A_N/2, uniformly over the band.
Fix an ordinate pair gamma,eta, hence h and the positive bases N*gamma/h,
N*eta/h. Reflection rho->1-conj(rho) preserves ordinate and multiplicity.
On a two-location beta orbit its weights are x and1/x, so their sum is
at least2; at a critical-line location the weight is1. Thus at these fixed
ordinates the separate weighted real-part sums are at least their copy
counts. This reasoning must be done for each ordinate pair: the bases
depend on both heights and are not fixed globally across the band.
As h<=4T, summing now gives
 sum_(gamma,eta in(T,2T]) |J_N| >=c T^-1/2 M_T^2,
where M_T counts all zeros in(T,2T] with multiplicity. Riemann-von Mangoldt
gives M_T=(T/(2pi))logT+O(T), hence M_T>>TlogT. This proves
 sum |J_N| >> T^(3/2)log^2T=Nlog^2N.                                  (5)
The argument counts ordered pairs, equal locations and repeated zeros.

The band is inside the ACTUAL C_high support of spectral_height_envelope.py
except for the already paid near-height strip: eventually T>V_N,
T>N^(13/20), and gamma+eta<=4T<(pi+delta)N, so the original weight1-Psi
is exactly1 here. Its portion |gamma-eta|<=W_N has O_A(N/log^A N)
absolute mass by spectral_near_height_bound.py. Subtracting this from (5)
retains (1) on the separated band. This does not subtract signed sums or
assume that a large absolute sum has a large real part.

5. PAY THE TOTAL ERROR BEFORE USING THE COSINE FORMULA.
A pointwise relative error alone would not justify (2). The total leading
amplitude has a direct density bound. On this band A_N is at most a fixed
constant times N^(beta+beta'-1)T^-1/2, because gamma/h and eta/h stay in
[1/3,2/3]. Apply the two single-zero layer-cake estimates already proved
in spectral_low_axis_bound.py, now with G=H=T=N^(2/3). Their exponent is
 E=beta+beta'-1+(2/3)[D(beta)+D(beta')-1/2].
Writing u=1-beta, v=1-beta', the rational inequality
 D_u=3u/(1+u)<=3u/2+4/15
has positive slack (45u^2-37u+8)/(30(1+u)); the numerator is
45(u-37/90)^2+71/180. Therefore E<=46/45, giving
 sum A_N << N^(46/45)log^12N.
The uniform error from (4) totals at most
 T^-1/2 sum A_N << N^(31/45)log^12N=o(N),
also on every subset of the band. This proves (2) and pays its error
without reversing a one-sided bound on |J_N|.

Useful exact phase data, retained for a FUTURE signed-cancellation test:
 d_gamma Theta=log(N*gamma/h), d_eta Theta=log(N*eta/h),
 d_gamma^2 Theta=eta/(gamma*h), d_eta^2 Theta=gamma/(eta*h),
 d_gamma d_eta Theta=-1/h.
The Hessian has rank1, while the mixed derivative is nonzero. These are
identities, not a discrete oscillatory-sum theorem for the actual zeros.
No continuous oscillatory-integral bound has yet been transferred to this
irregular, multiplicity-counted discrete measure.

All source authority is inherited from the reviewed explicit kernel,
functional equation, Riemann-von Mangoldt and uniform Ingham bounds in the
predecessor modules. In particular arXiv2507.15184v2 remains the checked
density source; the 2016 explicit-formula error correction still controls.
No new source claim, numerical zero experiment, coverage or novelty.
The tests below are exact phase, reflection and density-budget guards.
"""
from fractions import Fraction as F

from spectral_low_axis_bound import density_power


def phase_pi_coefficient(beta, beta_prime):
    if any(type(b) is not F or not 0<b<1 for b in (beta,beta_prime)):
        raise ValueError('rational real parts in(0,1) required')
    return (beta+beta_prime-1)/2-(beta+beta_prime)/2+F(1,4)


def entropy_phase_hessian(gamma, eta):
    if any(type(t) is not F or t<=0 for t in (gamma,eta)):
        raise ValueError('positive rational heights required')
    h=gamma+eta
    return {'gg':eta/(gamma*h),'ge':-1/h,'ee':gamma/(eta*h)}


def reflection_orbit_totals(two_point_orbits, critical_copies=0):
    """Artificial positive base weights, not a computed zero list."""
    if type(critical_copies) is not int or critical_copies<0:
        raise ValueError('nonnegative integer critical-line copy count required')
    if any(type(x) is not F or x<=0 or type(m) is not int or m<1
           for x,m in two_point_orbits):
        raise ValueError('positive rational orbit weights and integer multiplicities required')
    return {'weight':F(critical_copies)+sum((m*(x+1/x) for x,m in two_point_orbits),F(0)),
            'copies':critical_copies+2*sum(m for x,m in two_point_orbits)}


def amplitude_density_slack(u):
    return F(3,2)*u+F(4,15)-density_power(u)


def stationary_band_density_exponent(u, v):
    return 1-u-v+F(2,3)*(density_power(u)+density_power(v)-F(1,2))
