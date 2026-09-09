"""Unequal-height cancellation through the full finite-period transition.

Owner: Kevin's Goldbach research. Purpose: replace the restricted
stationary approximation by an exact convolution, preserving its useful
phase bound and paying the entire integral. This removes a larger actual
weighted family; it does not prove the remaining signed lower margin.

1. STATEMENT AND EXACT SUPPORT.
Keep J_N, the current17/20 core, and V_N,W_N from the preceding modules.
Write L=logN. Fix K>0, a fixed smooth function w on[0,2K], and
 1/2<theta<59/71, 0<epsilon<(1-theta)/(1+theta)-6/65,
 a=6/65+epsilon, Delta=[1-a-(1+a)theta]/2>0.
For dyadic tags G<=H, G<=H^theta, restrict the two lists SEPARATELY:
 V_N<gamma<=KN, gamma in(G,2G];
 V_N<eta<=KN, eta in(H,2H], eta>N^(17/20).                         (1)
For their disjoint union U, with every zero copy retained,
 |sum_U w((gamma+eta)/N)J_N(rho,sigma)|
   <<_(K,w,theta,epsilon) N^[1-(17/20)Delta]L^55+N^(91/100)L^15.    (2)
The same holds for the transpose. With theta53/64, epsilon1/1170,
Delta1/1280, the first power is25583/25600. Thus(2) is all-log small.
The whole endpoint transition is included in this SELECTED unequal
family. No stationary condition such as4(gamma+eta)<=piN is imposed.

For the actual core take K=pi+2delta and w=1-Psi. This ORIGINAL FIXED
SMOOTH weight is an amplitude, not a hard curved mask. It vanishes
above the original sum cap. The separate lists in(1) include all of
its support. No arbitrary coupled restriction is licensed by(2).

2. THE EXACT FINITE-PERIOD CONVOLUTION.
For x>0 and z=rho+sigma, Re z=b=beta+beta'>0, put
 B_x=2x^(z-1)Gamma(rho)Gamma(sigma)/Gamma(z),
 K_pi(y)=int_0^pi exp(iyt)dt=(exp(i*pi*y)-1)/(iy), K_pi(0)=pi.
Then EXACTLY
 J_N=e/(2pi) int_0^infinity exp(-x/N)K_pi(N-x)B_x dx.              (3)
Indeed the Gamma Laplace integral is
 (1/N+it)^(-z)=Gamma(z)^(-1)
                   *int_0^infinity exp[-(1/N+it)x]x^(z-1)dx.
This is NIST DLMF5.9.1 with mu1, nu=z; the checked conditions are
Re nu>0, mu>0, Re(1/N+it)>0, principal powers:
https://dlmf.nist.gov/5.9.E1 . For each pair, Fubini on t in[0,pi]
is valid because int exp(-x/N)x^(b-1)dx is finite. Substitute into
the DEFINITION J_N=(e/pi)Gamma(rho)Gamma(sigma)
*int_0^pi exp(iNt)(1/N+it)^(-z)dt. The factor2 in B_x leaves e/(2pi),
and the Fourier argument is N-x, not x-N. All zero lists are finite,
so their interchange with the integral is also valid.

The elementary bound |K_pi(y)|<=min(pi,2/|y|) gives, uniformly0<b<2,
 int_0^infinity exp(-x/N)|K_pi(N-x)|x^(b-1)dx
                      <<N^(b-1)(L+1/b),                         (4)
 int_0^infinity exp(-x/N)|K_pi(N-x)|max(H,x)dx <<_K N L           (5)
when H<=KN. To check uniformity, set x=Nu. In(4) the remaining
integrand is exp(-u)u^(b-1)min(piN,2/|1-u|). On0<u<1/2 its
integral is O(1/b), on1/2<u<3/2 it is O(L), and on u>3/2 it is
O(1), uniformly0<b<2. For(5) replace u^(b-1) by max(H/N,u),
bounded by K+u, which has no singularity at0. These are ABSOLUTE
integral costs: no extra cancellation of K_pi has been assumed.

3. THE QUOTIENT RETAINS THE SAVED PHASE, WITHOUT A TIME-ENDPOINT ERROR.
Write h=gamma+eta. Uniform complex Stirling gives, for all x>0,
 B_x=A_x exp(iTheta_x)[1+O(G^-1)],
 A_x=2sqrt(2pi)h^-1/2
          *(x*gamma/h)^(beta-1/2)*(x*eta/h)^(beta'-1/2),
 Theta_x=gamma log(x*gamma/h)+eta log(x*eta/h)-pi/4.               (6)
The numerator and denominator exponential factors cancel. The net
real-part phase is[(b-1)-(b-1/2)]pi/2=-pi/4. The uniform relative
error comes only from Gamma factors; there is NO H^-1/2 finite-time
approximation error. It remains uniform as x tends to0 or infinity,
since x^(z-1) is exact. The positive amplitude obeys
 A_x << x^(b-1)G^(beta-1/2)H^(-beta).                             (7)

Use the reviewed discrete unequal-phase operator of
unequal_spectral_cancellation.py. With ratio r=G/H, its amplitude
is multiplied by w((G*s+H*t)/N). On the fixed normalized support,
all needed derivatives are bounded in terms of K,w since G,H<=KN.
Smooth extension in beta,beta' and their Fourier expansion retain
summable seminorms. After both separable carriers are removed, the
phase and projection tails are unchanged for every x>0. Thus
 |sum_box w A_x exp(iTheta_x)|
                 <<_(K,w) L sqrt(E_G(xG/H)E_H(x)).              (8)
Sharp restrictions in(1) are individual coefficient masks. This
argument never treats beta as a smooth function of its ordinate.

4. PAY THE ENERGY FOR BOTH SIDES OF EACH HEIGHT SCALE.
The reviewed fixed-epsilon density majorant D_*(u)+epsilon<=2u+a
from guth_maynard_ratio_cancellation.py gives, for Z>=1, logZ=O(L),
 E_Y(Z)<<_epsilon max(Y,Z)Y^a L^51,                              (9)
with N^(9/20)<=Y<=KN. In fact layer cake costs
 YL+Z L^51 max_(0<=u<=1/2)[(Y/Z)^(2u)Y^a].
The maximum factor is max(1,Y/Z), which also absorbs the baseline.
This proof works for Z<Y; it does not assert that the energy is
monotone in Z. For0<Z<1 the separate elementary bound is
 E_Y(Z)<=C Y L/Z, since0<beta<1.                                (10)

For H/G<=x<=N^2, both energy bases in(8) are at least1. The identity
 max(G,xG/H)=(G/H)max(H,x)
therefore yields
 |sum_box w A_x exp(iTheta_x)|
 <<max(H,x)G^[(1+a)/2]H^[(a-1)/2]L^52
 <=max(H,x)H^-Delta L^52.                                      (11)
Integrating(11) with(5) costs N H^-Delta L^53. There are O(L^2)
tag pairs; eta>N17/20 implies H>N17/20/2. This proves the main
term of(2), including its EXTRA logarithm for the convolution.

5. SMALL x, A BASE BELOW1, AND THE FAR TAIL.
For0<x<1 use the EXACT quotient and(7), not(9). Since G<=H,
 |B_x|<=C G^-1/2 x^(b-1).
The retained classical zero-free region and functional reflection
give beta,beta'>=c_K/L for all our zeros, so1/b=O_K(L). There are
O(GH L^2) pairs. Since |K_pi(N-x)|=O(1/N), this range costs
 <<sqrtG H/N L^3 <<_K N^(theta/2)L^3 per box.                    (12)

For1<=x<H/G, use(10) for the row and(9) for the column:
 E_G(xG/H)<<H L/x, E_H(x)<<H^(1+a)L^51.
The main in(8) is at most H^(1+a/2)x^-1/2 L^27. Here
H/G<=K N^(11/20)=o(N), so the Fourier kernel is again O(1/N).
Its integrated cost is
 <<N^-1 H^[(3+a)/2]G^-1/2 L^27
 <<_K N^[11/40+a/2]L^27.                                      (13)
The parameter condition and theta>1/2 imply a<1/3, whence this
power is <53/120<1/2. The two small-x costs, including O(L^2)
boxes, are absorbed by the second term of(2). For x>N^2, (7),
0<b<2, and finite pair counts give a polynomial in x,N times
exp(-x/N); integration is O_C(N^-C) for every fixed C. The same
bound pays either the exact quotient or its main/error decomposition.

6. THE GAMMA REMAINDER IS INTEGRABLE AND POWER-SMALL.
On x>=1 sum the relative O(G^-1) error in(6) absolutely. Since
A_x=(x/N)^(b-1)A_N, (4) and1/b=O(L) bound the integrated error by
 C_(K,w) (L/G) sum_box A_N.                                    (14)
The L factor is retained; it cannot be erased by formal inversion.
Pay(14) with the OLD Ingham layer cakes, not the new density loss.
To handle K>1 explicitly, put Q=(K+2)N and use A_N asymp_K A_Q
uniformly0<b<2. Let g=logG/logQ,h=logH/logQ. Then
 g>=9/20-O_K(1/logQ), g<=theta*h<=theta<5/6, g<=h<=1.
The absolute Gamma-error exponent is E(g,h,u,v)-g, where
 E=1-u-v+g[1/2-u+D_I(u)]+h[-1+u+D_I(v)],
 D_I(u)=3u/(1+u), u,v in[0,1/2].
This is affine in h for fixed g,u,v. At h=g the retained exact
inequality D_I(u)<=(6/5)u+2/5 gives
 E-g/2<=1-g/5-(1-6g/5)(u+v)<=1-g/5,
so E-g is even smaller. At h=1, D_I(u)-u<=1/2 gives
 E-g<=1/2. Consequently the entire interval costs at most
 Q^[91/100+O_K(1/logQ)]=O_K(N^(91/100)).
Layer cakes cost L^12, (14) costs L, and the boxes cost L^2:
the TOTAL remainder is O(N^(91/100)L^15), as stated in(2).
The separate fixed-Q inflation also makes both amplitude bases
QG/H,Q at least1, so the earlier layer cakes are applicable.

7. REMOVE THE LARGER EXACT FAMILY AND PRESERVE THE GAP.
Eventually2G<H/2 for selected nonempty tags. Hence gamma<eta and
eta-gamma>H/2>W_N. The larger-column condition in(1) is exactly the
current max-height condition. The transpose is disjoint. The smooth
w accounts for the original sum cap, including its transition; its
derivative constants are fixed because delta is fixed. Rebuild the
core after the17/20 square, axes and near strip but before the old
N/2 tag deletion, then delete this larger weighted union and transpose.
It contains that earlier deletion, where w=1. We never apply the
matrix estimate to an arbitrary coupled set difference.

The pointwise formula retains its all-log total error. Comparable
large heights, and the signed lower margin of the remaining actual
correlation, stay OPEN. No new Goldbach coverage, RH, target averaging,
effective onset, worldwide novelty or all-method obstruction is claimed.
The arithmetic prime-offset transform, polynomial tools, source
corrections and runtime restrictions remain available and unchanged.
"""
from cmath import exp
from fractions import Fraction as F
from math import pi, sin

from guth_maynard_ratio_cancellation import ratio_parameters


def finite_interval_kernel(y, endpoint=pi):
    """Stable angular Fourier transform of the interval [0, endpoint]."""
    if endpoint <= 0:
        raise ValueError('positive endpoint required')
    if y == 0:
        return complex(endpoint)
    return 2*exp(1j*endpoint*y/2)*sin(endpoint*y/2)/y


def energy_power(height_power, base_power, excess):
    """Power of N in the two distinct energy bounds (9)-(10)."""
    if any(type(v) is not F for v in (height_power,base_power,excess)):
        raise ValueError('exact rational powers required')
    if height_power < 0 or excess <= 0:
        raise ValueError('nonnegative height and positive density excess required')
    if base_power < 0:
        return height_power-base_power
    return max(height_power,base_power)+excess*height_power


def convolution_budget(theta, epsilon):
    """Retain the new logarithm and both endpoint power costs."""
    params=ratio_parameters(theta,epsilon)
    return {
        'core_power':params['current_core_power'], 'core_log_power':55,
        'zero_endpoint_power':theta/2,
        'small_base_power':F(11,40)+params['density_excess']/2,
        'gamma_power':F(91,100), 'gamma_log_power':15,
    }
