"""Pay the last H-weighted exterior in the actual survivor-field bridge.

Owner: Kevin's Goldbach research. Purpose: make the retained bad-detector
prime-product representation valid after the actual zero deletions. This
closes one transfer error, not the signed prime correlation or Goldbach.

1. OBJECTS AND CONCLUSION.
Use the actual positive-height zero copies, T=N^(9/10), L=logN, fixed
real chi in C_c^infinity((1,2)), and w_rho=|chi|^2*N^(2beta-2).
Keep the SAME common H_N=sum_badM D_M, good sum A_N, and original
survivors R from signed_zero_detector.py. Bad length exponents are
 (49/300,41/250), (49/250,41/200),
 (49/200,41/150), (49/150,41/100).                            (1)
Good M have a licensed integer k<=100 with p=k*logM/logN in
[41/50,49/50]. No definition or earlier deletion is changed.

For D_high={beta>=19/25}, we prove
 E_(D_high,H)=sum_(D_high)w_rho*|H_N(rho)|^2
   << L^C*[N^(-1/400)+exp(-c*L^(1/3)/(logL)^(1/3))]           (2)
for some fixed C,c>0. All zeros and multiplicities here are actual.
Thus this energy is O_A(L^-A) for EVERY fixed A, asymptotically.
Combining with the previously paid middle and low masks proves
 theta*Z_(H,R)(v)=-theta*P_h(vN)/sqrtN+O_L2,A(L^-A),          (3)
where theta is the retained fixed central cutoff and P_h is the actual
prime-product window with coefficient h*Lambda, including the SAME
bad-length mask and exp(-n/sqrtT). No unrestricted convolution replaces
it. The error in(3) is a norm, not a pointwise statement.

2. A STRONGER KNOWN DENSITY INPUT REMOVES THE OLD CORNER.
Sources checked2026-09-10:
 https://arxiv.org/pdf/2501.16779v1
Tao--Trudgian--Yang, printedp33 Table2, records the Ivic bound
 A(sigma)<=3/(2sigma) on[4/5,7/8). Their A convention permits
T^epsilon losses; it is NOT a log-power estimate. The author-maintained
proof at
 https://teorth.github.io/expdb/blueprint/zero-density-chapter.html
Corollary11.31 and Lemma11.30 also gives this bound for
sigma>=3831/4791<4/5. We need only the compact interval above.
In ordinary notation, at each fixed such sigma and each epsilon>0,
 M(sigma,T)<<_(sigma,epsilon) T^[3(1-sigma)/(2sigma)+epsilon]. (4)
Here M counts copies in our band; counting up to2T overcounts it.
No optimality claim about(4), RH, or conditional density hypothesis is
made. Stronger entries in the table are unnecessary for this test.

At beta=5/6,h=2/5, the old Huxley density gave normalized energy
exponent-1/30; the second and third multiplier moments gave+1/30
and+1/15. Their Holder budgets were exactly ZERO. With(4) the
energy exponent is instead-19/300, so the same budgets are-3/200
and-1/50, before a fixed epsilon loss. No actual zero at this corner
is asserted. This disproves the proposed barrier for these inputs.

3. UNIFORM ACTUAL POLYNOMIAL MOMENTS ON THE EXTENDED INTERVAL.
The coefficient/Sobolev proof in detector_power_length_filter.py works
uniformly on every subinterval of[0,1]: its beta integration has length
at most1, and n^(-2alpha)<=n^(-2sigma) for alpha>=sigma. Thus for
D_M^s, p=s*logM/logN, a beta bin[sigma,sigma+Delta], and u=1-sigma,
 K_s=sum_bin w_rho*|D_M(rho)|^(2s)
       <<_s N^[v(p,u)+2Delta]*L^(4s^2+5),
 v(p,u)=max(9/10,p)-p+2u*(p-1).                              (5)
This uses the ACTUAL product support (M^s,2^s*M^s], coefficients
bounded by tau_(2s), and O(L) unit-interval copy occupancy. Constants
are uniform even when the bin approaches beta=1. The moments below
have s<=100; factors2^s are fixed constants. No artificial frequency
or masked arithmetic norm is substituted for this sampling bound.

If a set X in the bin has weighted energy N^[e+2Delta] times
fixed logs, Holder gives its D_M-weighted energy exponent
 (1-1/s)*e+v(p,u)/s+2Delta.                                 (6)
A density T^epsilon loss adds at most(9/10)*epsilon to(6).

4. LOWER HIGH STRIP: 19/25<=beta<4/5.
First extend the corrected Maynard--Pratt source Type II count only
to this fixed strip. In arXiv2206.11729v2, Lemma24 p16 and Appendix C
pp36-38, retain Gamma(1/2-beta+it), NOT the printed opposite sign.
Now delta=beta-1/2 lies in[13/50,3/10]. The recurrence
 Gamma(-delta+it)=Gamma(1-delta+it)/(-delta+it)
and the Euler integral give |Gamma(-delta+it)|<=Gamma(1-delta)/delta
uniformly; Stirling gives a uniform exponential tail. The same log^3
separated extraction loses log^4 copies, the fourth-power Holder
step costs log^10, and the same short-mollifier fourth moment is
T*log^C. Consequently the restricted Type II count up to beta=4/5
is T^[2(1-sigma)]*L^C0 uniformly on this strip. Its normalized bin
energy has e_II=-u/5, u in[1/5,6/25]. These are unconditional source
ingredients; Hypothesis F is not used. The exact signed equation
 1+A_N(rho)+H_N(rho)=I_T(rho)+O(T^-1/2)                      (7)
also extends here: the contour crosses the same poles, the canceled
Gamma pole uses the actual zero, and the saved dyadic endpoint and
smoothed a_T(1) errors are unchanged.

On Type II copies choose powers6,5,4 for the first three bad gaps.
For the fourth gap choose3 if h<=39/100 and2 if h>=39/100.
For powers>=3, p>.9 and the Holder exponent is
 2u*[h-1/10-9/(10s)].
For power2, p<.82 and the exponent is
 9/20-h+u*(2h-11/10).
Both fourth-gap pieces have maximum-1/250 at u=1/5,h=39/100;
the first three gaps have stronger savings. Partition the strip into
400 FIXED bins of width1/10000. The weight loss2Delta leaves
-1/250+1/5000<-1/400. Sum the bad polynomials by Cauchy and their
O(L) lengths; the two extra logs are paid.

For X=all NON-Type-II copies in this strip, use Guth--Maynard's
already checked density theorem at the same400 fixed lower edges,
with fixed source epsilon=1/10000. Before losses its energy exponent is
 e_G(u)=u*(10u-5/2)/(8-5u)<=-3/850.                          (8)
For EACH good M use one licensed k. Since actual allowed m<.49
eventually whereas p>=.82, necessarily k>=2. If p<=.9, then
 v(p,u)<=2/25-(9/25)*u.
The sum e_G(u)+2/25-(9/25)*u is convex: its second derivative is
1080/(8-5u)^3>0. Its half-values at u=1/5 and6/25 are
-11/3500 and-211/42500. Since1/k<=1/2, the Holder exponent is
at most max(e_G,(e_G+v)/2)<=-11/3500. If p>=.9, then
v(p,u)<=-u/25<=-1/125, and(8) suffices directly. In either case,
adding2Delta+(9/10)*epsilon=29/100000 leaves less than-1/400.
This proves a weighted bound for EVERY good polynomial on X without
requiring that X be detected by that particular polynomial. Summing
good M with Cauchy pays A_N. On X, |I_T|<1/3, so(7) gives
 |H_N|^2<=2|A_N|^2+O(1).
The constant is paid by(8); it is not dropped. Adding the Type II
part proves E_(19/25<=beta<4/5,H)<<N^-1/400*L^C.

All constants at the400 source grid points are absorbed by their finite
maximum. Counts are used at each bin's exact lower edge, so no rounding
derivative loss is missing. Neither fixed epsilon nor these bins is used
near beta=1. For logs C=max(C0,40230)+10 safely covers this strip.

5. COMPACT UPPER STRIP: 4/5<=beta<7/8.
For every bad M choose pure powers6,5,4,3 on its four gaps. All
actual product exponents exceed.9, so(5) uses its LENGTH term,
including a positive cost when p>1. Bound(4) gives, before epsilon,
 e_I(u)<=-5u/16, since A<=15/8.
Equation(6), before bin losses, is therefore at most
 u*[(1-1/s)*(-5/16)+2h-2/s] <=-(11/200)*u.                  (9)
The maximum coefficient is at gap4,h=41/100,s=3; closed endpoints
only enlarge the estimate. The other three gaps are better.
Here u>=1/8. Partition into750 fixed bins of width1/10000 and
use source epsilon1/10000. Then
 -11/1600+29/100000<-1/200.
Sum their nonnegative energies and the bad polynomials, obtaining
 E_(4/5<=beta<7/8,H)<<N^-1/200*L^153.                        (10)
The right boundary beta=7/8 is assigned to the next strip.

6. NEAR ONE: RELATIVE BINS, LOG-POWER DENSITY AND ZERO-FREE CAP.
Use the retained classical Huxley LOG-POWER count, recorded in
Yashiro1310.0765v2 p2 equation(1.2), rather than the epsilon version
of the preceding source. For0<u<=1/8 its energy exponent obeys
 e_H(u)=(9/10)*3u/(2-3u)-2u<=-(22/65)*u.
With the same powers6,5,4,3 the worst coefficient in(6) is
 (2/3)*(-22/65)+2*(41/100)-2/3=-47/650.
Let v_j=(1/8)*(99/100)^j and bin the actual complementary real parts
as (99*v_j/100,v_j]. In such a bin the LOWER beta is1-v_j,
the width is v_j/100, and the weight loss is v_j/50. Thus
the weighted Holder exponent is at most
 (-47/650+1/50)*v_j=-(17/325)*v_j<-v_j/20.                  (11)
An endpoint is assigned to one bin; extra endpoint overcounting would
also be harmless. The retained Vinogradov--Korobov region from
2212.06867v1, Theorem1.1 p2, gives for all our actual copies
 u>=delta_N>>L^(-2/3)*(logL)^(-1/3).
Only O(log(1/delta_N))=O(loglogN) bins can contain zeros, and
each used v_j>=delta_N. Summing(11), including its last possibly
truncated bin, and then summing bad lengths gives
 E_(beta>=7/8,H)<<L^153*exp(-c*L^(1/3)/(logL)^(1/3)).        (12)
The largest pure moment log exponent is149, Huxley's count has
log44 (or the retained allowance50), and the bin sum and two length
logs fit153. No fixed epsilon or fixed-width bin overwhelms this cap.

7. ACTUAL KERNEL TRANSFER AND THE OPEN MATHEMATICAL GAP.
Equations(10),(12) and the lower high strip prove(2). For W=full band
minus R, the earlier middle/low weighted bound is N^-11/3750 times
fixed logs. Hence E_(W,H) satisfies(2) as well. The arbitrary-coefficient
Gram estimate gives ||theta*Z_(H,W)||_2^2<<L*E_(W,H). Combining
it with the full-field transfer error N^-59/200*L7 proves(3).

The one-coordinate ACTUAL finite-period kernel contribution with
coefficient H_N(rho)*1_W(rho) is O_A(N/L^A). Indeed its central
beta integral is at most N*sqrt(L*E_(W,H)), using arithmetic O(1)
only for the FULL opposite field. The new weighted l1 bound is
sum|c_rho*H_N*1_W|<<N^(9/20)*sqrt(L*E_(W,H)); the retained full
opposite l1 bound is N^(2/5)*L6. The uniform J-minus-beta error
therefore costs N^(19/20)*sqrt(E_(W,H))*L^C, and the three-IBP
endpoint costs N^(-17/20)*sqrt(E_(W,H))*L^C. Both are paid.
The reversed coordinate is also paid. No nonindicator union identity
or two-weight arithmetic norm is inferred.

On R the disk |1+H_N(rho)|<=3/4 and |1/H_N(rho)|<=4 persist.
Equation(3) now transfers the MULTIPLIED survivor field to actual
prime products. Pointwise bounded reciprocal values on zero copies
do not establish a bounded inverse on these nonorthogonal packets.
Nor do they determine the sign of a reflected pairing without
conjugation. Those inverse/correlation estimates, the remaining
smooth band's o(N) estimate, and universal Goldbach coverage remain
OPEN. This is new-to-this-task only, with no claim of external novelty.
"""
from fractions import Fraction as F

from mixed_detector_weighted_mask import BAD_GAPS
from weighted_detector_mask_bridge import moment_power


def bad_power(h, lower_type_ii=False):
    if type(h) is not F:
        raise ValueError('exact bad-length exponent required')
    gap = next((j for j, (lo, hi) in enumerate(BAD_GAPS) if lo < h < hi), None)
    if gap is None:
        raise ValueError('length must lie strictly inside a bad gap')
    if lower_type_ii and gap == 3 and h >= F(39, 100):
        return 2
    return (6, 5, 4, 3)[gap]


def density_energy(u, source):
    if type(u) is not F or not 0 < u <= F(6, 25):
        raise ValueError('exact high-strip complementary real part required')
    if source == 'gm' and F(1, 5) <= u <= F(6, 25):
        return u * (10*u-F(5, 2)) / (8-5*u)
    if source == 'ivic' and F(1, 8) <= u <= F(1, 5):
        return F(27, 20)*u/(1-u)-2*u
    if source == 'huxley' and u <= F(1, 5):
        return F(27, 10)*u/(2-3*u)-2*u
    if source == 'type_ii' and F(1, 5) <= u <= F(6, 25):
        return -u/5
    raise ValueError('source outside its retained range')


def bad_holder(u, h, source):
    s = bad_power(h, lower_type_ii=(source == 'type_ii'))
    return F(s-1, s)*density_energy(u, source)+moment_power(u, s*h)/s


def good_holder(u, p, k):
    if (type(p) is not F or not F(41, 50) <= p <= F(49, 50)
            or type(k) is not int or not 2 <= k <= 100):
        raise ValueError('licensed product exponent and integer power>=2 required')
    return F(k-1, k)*density_energy(u, 'gm')+moment_power(u, p)/k


def relative_u_bins(delta):
    """Exact bin geometry only; delta is supplied, not a measured zero-free cap."""
    if type(delta) is not F or not 0 < delta <= F(1, 8):
        raise ValueError('positive exact cap<=1/8 required')
    bins = []
    upper = F(1, 8)
    while upper >= delta:
        lower = F(99, 100)*upper
        bins.append((lower, upper))
        upper = lower
    return tuple(bins)


def fixed_beta_bins(left, right):
    step = F(1, 10000)
    if (type(left) is not F or type(right) is not F or left >= right
            or ((right-left)/step).denominator != 1):
        raise ValueError('exact ordered endpoints on the fixed grid required')
    return tuple((left+j*step, left+(j+1)*step)
                 for j in range(int((right-left)/step)))
