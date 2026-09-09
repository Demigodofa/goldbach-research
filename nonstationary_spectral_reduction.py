"""Uniformly remove the smooth nonstationary same-sign spectral tail.

Owner: Kevin's Goldbach research. Purpose: extend the reviewed fixed-box
signed saving to the full smooth nonstationary region, paying axes, growing
support, every smooth seminorm, and coupled tails. No RH, target average,
numerical zero certificate, new coverage or worldwide novelty claim.

1. THE RESULT AND THE SURVIVING TARGET.
Use the principal logarithm and J_N from smooth_endpoint_cancellation.py.
All sums below are over positive-height nontrivial zeta zeros, with actual
real parts, multiplicities, ordered pairs and diagonal. N>=3 is an integer,
L=logN. Fix delta>0 and a fixed real smooth profile Psi with
 0<=Psi<=1, Psi(k)=0 for k<=pi+delta,
 Psi(k)=1 for k>=pi+2delta.
Such a C^infinity profile is obtained from the standard flat step
q(u)=h(u)/(h(u)+h(1-u)), h(u)=exp(-1/u) for u>0 and0 otherwise,
by putting u=(k-pi-delta)/delta. The profile and delta stay FIXED as N grows.
We prove
 H_N=Re sum_(rho,sigma) Psi((gamma+eta)/N) J_N(rho,sigma)
                 =O_(delta,Psi)(sqrtN L^40).           (1)
The exponent40 is a deliberately unoptimized explicit budget.

Consequently, with
 C_low(N)=Re sum_(gamma,eta>0; gamma+eta<=(pi+2delta)N)
           [1-Psi((gamma+eta)/N)] J_N(rho,sigma),
the actual pointwise transfer becomes
 R(N)=2psi(N-1)-N+C_low(N)+O_(A,delta,Psi)(N/L^A)      (2)
for every FIXED A>0. The earlier opposite-sign removal has error
O(N sqrtL exp(-c0 sqrtL)); it is all-log small on the N scale, but cannot
be absorbed into O(sqrtN L^40). Before this last simplification the full
error in (2) is O_(delta,Psi)(sqrtN L^40+N sqrtL exp(-c0 sqrtL)).
The remaining sum is FINITE and only needs zeros of height at most
(pi+2delta)N, rather than the former C*NlogN cutoff. This is an analytic
reduction, not a practical verification of any list of zeros. The weights
in C_low do not make the real sum positive. Its sufficient lower margin
C_low>=-(1-epsilon)N, fixed epsilon>0 for all large even N, remains OPEN.
PNT and proper-power deletion from the saved transfer would then give
genuine prime pairs. Neither that margin nor an onset is supplied here.

2. THE ONE-ZERO PROJECTION IS UNIFORM THROUGH THE AXIS.
Let z_*=1/N+i*pi, f_rho=Gamma(rho)z_*^-rho and
 M_N=sum_allrho |f_rho|<<N^(3/2)L.
For S>=1 and w in C_c^infinity([-S,S]), set
 Q12(w)=max_(0<=j<=12)||w^(j)||_infinity,
 F_N^+(w)=sum_(gamma>0) f_rho w(gamma/N),
 A_N(w)=sum_(n>=1)Lambda(n)e^(-n/N)w(pi*n/N).
The radial Fourier proof in smooth_endpoint_cancellation.py gives
 F_N^+(w)=A_N(w)+O(S*Q12(w)*sqrtN L),
 |A_N(w)|<<N*||w||_infinity.                          (3)
Here the implicit constants are independent of S and w.

Explicit changes from the fixed positive support proof: Fourier L1 and
second moments of hatw are O(SQ12), and its tail beyond V=N^(1/8) is
O(SQ12 V^-11). The beta replacement and truncation errors multiply M_N
and still cost O(SQ12 sqrtN L). The corrected explicit formula and the
Chebyshev moments have the same uniform bounds. The powers-of-two parity
correction now costs O(||w||_infinity logN), not O_w(1):
sum_(j>=1)exp(-2^j/N)<=floor(log_2 N)+1.
For the last inequality, the terms through floor(log_2 N) are at most1;
the following terms are bounded by2^-k since2^(k-1)>=k and e>2.
Finally the NEGATIVE-height endpoint sum has uniformly bounded absolute
mass, so subtracting it costs O(||w||_infinity). This proves (3) even
when w is nonzero at0 or at negative arguments. No small zero real part
has been replaced by1/2, and no zero count at a fixed first ordinate is used.

3. PAY THE GROWING SUPPORT WITH AN EXPLICIT TENSOR BUDGET.
Let B=16piL and T=BN. Choose fixed real eta0 in C_c^infinity([-2,2]),
0<=eta0<=1, equal1 on[-1,1]. For example eta0(s)=1-q((s^2-1)/3)
with the flat step above. Define
 G_N(s,t)=Psi(s+t)eta0(s/B)eta0(t/B).
Its support lies in[-2B,2B]^2. Only positive s,t are evaluated in the zero
sum, so k=s+t is between pi+delta and4B on its nonzero support there.

The required endpoint multipliers are G_N/d, the b-free secondary
coefficient times G_N, and G_N/(pi*d^2), where d=1-(s+t)/pi. Define
them to be0 below the support of Psi. They are smooth across the possible
pole because Psi vanishes on an entire neighborhood of s+t=pi. Every
mixed derivative up to order(16,16) is bounded by a fixed constant
depending on delta, Psi and eta0, independent of B>=1. The same is true
of G_N itself. Rational factors and their derivatives are bounded on
k>=pi+delta, including as k grows.

For any such multiplier g_N, take its tensor Fourier series on the
period-8B square[-4B,4B]^2. It vanishes near that square's boundary.
Sixteen integrations in each variable give coefficients
 |c_(m,n)|<=C_delta B^32(1+|m|)^-16(1+|n|)^-16.        (4)
Constants here and below also retain the fixed profiles. Insert separated
cutoff factors equal1 on[-2B,2B], supported in[-3B,3B]. The resulting
one-variable Fourier factors w_m have sup norm O(1), support S=O(B),
and Q12(w_m)<=C(1+|m|)^12. Thus the coefficient series is summable
against both factors' Q12 seminorms: 16-12=4>1.

Applying (3) one variable at a time proves
 sum_(gamma,eta>0) f_rho f_sigma g_N(gamma/N,eta/N)
  =(A_N tensor A_N)(g_N)
    +O_delta(B^33 N^(3/2)L+B^34 N L^2).               (5)
The arithmetic main is REAL when g_N is real and bounded by
N^2||g_N||_infinity, independently of its support. The errors are the
single-factor cross terms and the product of errors, multiplied by (4).
Direct absolute replacement in both zero factors is still NOT the proof.
For a beta-weighted factor use only M_N and the sup norm in one variable:
 sum_(gamma,eta>0)(beta+beta')f_rho f_sigma g_N(gamma/N,eta/N)
    =O_delta(B^32 N^(5/2)L+B^33 N^2 L^2).             (6)
Neither beta-weighted reality nor a prime-pair estimate is assumed.

4. PAY THE ENDPOINT EXPANSION UNIFORMLY UP TO k=4B.
Use a=1/N, b=beta+beta' in(0,2), h=gamma+eta=kN,
A(t)=|a+it|^-b exp[-h*(pi/2-arg(a+it))],
phi(t)=Nt-h log|a+it|-b arg(a+it), q=1/phi'.
For sufficiently large N (depending on fixed delta), on [a,pi],
 D=t^2-k*t+(1-b)*a^2,
 D/t<=pi-k+a<=-delta/2.
Hence q=(a^2+t^2)/(N*D) has no pole there, with bounds for j<=3
 |q^(j)|<=C_delta(1+k)^j N^-1 t^(1-j),
 |A^(j)|<=C_j(1+k)^j t^(-2-2j)exp[-(pi+delta)/(2t)].   (7)
The tiny interval[0,a] and all lower endpoint jets are exponentially small.
Three integrations by parts retain the same two endpoint terms
 A(pi)e^(i*phi(pi))[-i*q+(A'/A)q^2+q*q']_(t=pi)
and give normalized remainder O_delta(B^3N^-3). Each third-iteration
term has at most three powers of(1+k), three powers of N^-1, and an
integrable polynomial in1/t times the exponential in (7).

The factored Gamma absolute pair mass for gamma,eta<=2BN is
O(N^3B^3log^2(NB))=O(N^3B^3L^2). Low fixed zeros are absorbed into
constants; the count O(TlogT) and Stirling bound (1+gamma)^(1/2) suffice.
Thus the normalized remainder costs O_delta(B^6L^2).
At pi put d=1-k/pi. The uniform coefficient expansions are
 q=(N*d)^-1+O_delta(B*N^-3),
 q'=-k/(N*pi^2*d^2)+O_delta(B^2*N^-3),
 A'/A=-b/pi+k/pi^2+O(B*N^-2).
Their errors cost at most O_delta(B^4L^2+B^5N^-1L^2) in the full sum.
The retained coefficients are still
 -i/(N*d)+N^-2[(-b/pi+k/pi^2)/d^2-k/(pi^2*d^3)].

For the leading term, the main in (5) is real and its multiplication by
-i has zero real part. Dividing its error by N costs
O_delta(sqrtN L^34+L^36), since B=16piL. The beta-linear second term
costs O_delta(sqrtN L^33+L^35) by (6) and N^-2. The b-free second main
costs O_delta(1), with smaller polynomial-log/power errors from (5).
The normalized remainder is O_delta(L^8). All these displayed costs are
bounded by O_delta(sqrtN L^40); no fixed-G constant has been treated as
uniform without its support and derivative costs.

5. PAY EVERY COUPLED PAIR OUTSIDE T.
G_N equals Psi(s+t) whenever both positive heights are <=T. Else their
difference has magnitude at most1. The saved Stirling/counting proof gives
uniformly for0<=t<=pi the ABSOLUTE majorant
 M_abs(t)=sum_(gamma>0)|Gamma(rho)(a+it)^-rho|<<N^(5/2)L.
Its absolute tail for gamma>T is bounded by
 N*T^(3/2)log(2T)exp[-T/(2piN)]
       <<N^(-11/2)L^(5/2), for T=16piNlogN.            (8)
These are sums of absolute terms, not just bounds for their signed sum:
split heights into jT<gamma<=(j+1)T, apply the cumulative O(TlogT)
count and the positive Stirling majorant, and sum the resulting geometric
tail. Do NOT weaken (8) to O(N^-3) before paying the other factor.
Every pair with at least one height>T therefore costs absolutely at most
O(N^-3 L^(7/2)), using 2*M_abs times the tail and the bounded integration
interval. This estimate permits the COUPLED bounded weight; it needs no
unproved norm for an arbitrary truncation. Combining it with Section4
proves (1). The earlier pointwise transfer and its correctly retained
opposite-sign removal error prove (2), with all-log rather than square-root
precision for the combined formula.

Fixed smooth separation delta, fixed profiles and the full seminorm budget
are essential. A hard cutoff or delta tending to0 has not been licensed.
The remaining stationary region still carries the unresolved signed margin.
All earlier source corrections, polynomial tools and runtime limits persist.
Dependencies and checked primary-source locators: smooth_endpoint_cancellation.py,
spectral_endpoint_obstruction.py, one_sided_zero_reduction.py and
pointwise_zero_pair_gate.py, especially the2016 explicit-formula correction
and the O(TlogT) zero count. No new external input or zero computation.
"""
from fractions import Fraction as F

from pointwise_zero_pair_gate import zero_tail_profile


def bulk_denominator_ratio(n, t, k, b):
    """Exact D(t)/t; tests use a rational proxy for the upper endpoint."""
    if type(n) is not int or n<3 or any(type(v) is not F for v in (t,k,b)):
        raise ValueError('integer N>=3 and rational t,k,b required')
    if t<=0 or k<=0 or not 0<b<2:
        raise ValueError('positive t,k and 0<b<2 required')
    a=F(1,n)
    return t-k+(1-b)*a*a/t


def tensor_log_budget(fourier_order=16, projection_order=12):
    """B~logN costs after dividing the leading tensor error by N."""
    if (type(fourier_order) is not int or type(projection_order) is not int
            or projection_order<0 or fourier_order<=projection_order+1):
        raise ValueError('Fourier decay must exceed seminorm growth by more than1')
    return {'coefficient_b_power':2*fourier_order,
            'sqrt_n_log_power':2*fourier_order+2,
            'plain_log_power':2*fourier_order+4}


def coupled_absolute_tail_profile(c_over_two_pi):
    """Preserve the sharp tail before multiplying the full absolute majorant."""
    profile=zero_tail_profile(c_over_two_pi)
    return {'n_power':profile['n_power']+F(5,2),
            'logn_power':profile['logn_power']+1}
