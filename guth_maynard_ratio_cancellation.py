"""A larger actual unequal-height deletion, with a paid GM density loss.

Owner: Kevin's Goldbach research. Purpose: exploit the shape of the new
density input where height-ratio decay can absorb its fixed power loss.
This extends selected actual finite-period rectangles, not the full
signed lower margin. All beta and product multiplicities are retained.

1. THE EXACT FAMILY, INCLUDING ITS ENLARGED LINEAR CEILING.
Keep J_N, V_N, W_N and the current17/20 high core from
guth_maynard_spectral_cancellation.py. Fix
 1/2<theta<59/71, delta=6/65,
 0<epsilon<(1-theta)/(1+theta)-delta.
Write a=delta+epsilon and Delta=[1-a-(1+a)theta]/2>0.
For each pair of dyadic tags G<=H with G<=H^theta, take the complete
Cartesian product of the separately restricted zero lists
 V_N<gamma<=N/2, gamma in(G,2G];
 V_N<eta<=N/2, eta in(H,2H].                                      (1)
The union U_theta of these disjoint rectangles satisfies
 |sum_(rho,sigma in U_theta)J_N(rho,sigma)|
   <<_(theta,epsilon) N^[1-(9/20)Delta]L^54+N^(91/100)L^14.         (2)
This is all-log small on the N scale, for fixed parameters. The
TRANSPOSE has the same bound. The N/2 ceiling in(1) is licensed by
the tag asymmetry, as shown below; it does not extend the full square.

For the current core, impose the further INDIVIDUAL column mask
 eta>N^(17/20).
Then H>N^(17/20)/2, improving the first term in(2) to
 N^[1-(17/20)Delta]L^54.                                          (3)
A concrete choice is
 theta=53/64, epsilon=1/1170, a=109/1170, Delta=1/1280,
so(3) is N^(25583/25600)L^54. This strictly enlarges the old theta4/5
tag union and its N/10 ceiling. It remains an asymptotic complex bound;
the sufficient Goldbach signed lower margin is still OPEN.

2. THE SHAPE OF THE THREE SOURCE EXPONENTS.
For u=1-sigma in[0,1/2], use the following SELECTED density envelope:
 D_*(u)=3u/(2-3u),          0<=u<=1/5;
        15u/(8-5u),        1/5<=u<=3/10;
        3u/(1+u),         3/10<=u<=1/2.                            (4)
The adjacent values agree at1/5 and3/10. This is not a claim that the
envelope is best among all known estimates. The outer pieces are the
retained log-power Huxley and Ingham bounds. The middle piece is the
ACTUAL exponent in Guth--Maynard2405.20552v2 Theorem1.2, printedp2:
https://arxiv.org/pdf/2405.20552v2 . Its o(1) is charged explicitly.

On the fixed middle interval, the source can be made uniform with
any fixed epsilon>0 by the finite-grid argument from the preceding
module. Here the derivative of15u/(8-5u) is120/(8-5u)^2<3. A lower
sigma grid of mesh epsilon/12 and a source loss at most epsilon/2
therefore suffice. The outer log-power estimates are unchanged. With
the same harmless multiplicity/log allowance as before,
 N_z(1-u,2Y)<<_epsilon Y^[D_*(u)+epsilon]L^50.                     (5)
Unlike the earlier full-rectangle proof, this bound may be weakened by
epsilon even near u=0: the explicit ratio saving below will pay it.
We do NOT claim a zero-free exponential saving from (5).

3. THE AFFINE ENVELOPE, WITH EXACT FACTORIZATIONS.
For every0<=u<=1/2,
 D_*(u)<=2u+6/65.                                                  (6)
On the Huxley interval the slack numerator is
 12+47u-390u^2
 =12(1-5u)+29u+390u(1/5-u)>=0,
with denominator65(2-3u)>0. On the GM interval the slack is
 (3-10u)(65u+16)/[65(8-5u)]>=0.
On the Ingham interval it is
 (10u-3)(13u-2)/[65(1+u)]>=0.
Equality is attained at u=3/10. The fixed epsilon in(5) is not
erased by this algebra: its actual exponent majorant is2u+a.

For N^(9/20)<=Y<=Z<=N, let E_Y(Z) be the copy-counted energy with
any individual mask, as in the preceding proofs. Its total-count
beta<=1/2 baseline is O(YL). Layer cake and(5)-(6) give
 E_Y(Z)<<YL+Z L^51 max_(0<=u<=1/2)[(Y/Z)^(2u)Y^a]
        <<_epsilon Z Y^a L^51.                                   (7)
The baseline is absorbed because Y<=Z and a>0. No zero-free cap or
unproved statistical independence is required for this deliberately
weaker estimate. The power Y^epsilon stays in(7).

4. RATIO DECAY PAYS THE ENERGY GROWTH.
On a nonempty selected box put X=NG/H. Since H<N/2, one has
 G<=X<=N and H<=N, so both energies meet(7). The reviewed uniform
unequal-phase operator bound remains
 |sum_box A_N exp(iTheta_N)|<<L sqrt(E_G(X)E_H(N)).
Substitution of(7) and sqrt(XN)=N sqrt(G/H) gives
 <<N G^[(1+a)/2] H^[(a-1)/2]L^52
 <=N H^-Delta L^52.                                               (8)
The coefficient of logG is positive, so using G<=H^theta is legal.
The limiting value with epsilon decreasing to0 is
 (1-delta)/(1+delta)=59/71.
It is NOT an endpoint theorem: each theta is fixed strictly below
this value, with its own fixed positive epsilon and Delta.

The low-axis restriction implies G>V_N/2>=N^(9/20), eventually.
Sum(8) over O(L^2) disjoint tag pairs to obtain the main term in(2).
The separate column mask eta>N^(17/20) instead gives the main term
in(3). For theta53/64 and epsilon1/1170 the exact arithmetic is
 a=6/65+1/1170=109/1170,
 1-a-(1+a)*(53/64)=1/640,
 1-(17/20)*(1/1280)=25583/25600.

5. WHY THE N/2 CEILING IS ALLOWED, AND BOTH ACTUAL ERRORS ARE PAID.
The selected tags satisfy
 gamma<=2G<=2H^theta<=2(N/2)^theta=o(N), eta<=N/2.
Consequently4(gamma+eta)<=2N+o(N)<piN for all sufficiently large N.
This verifies the saved UNIFORM finite-period stationary condition,
without pretending it holds for every comparable pair below N/2.
The actual complex expansion therefore remains
 J_N=A_N exp(iTheta_N)[1+O(H^-1/2+G^-1)].                          (9)
At linear H we keep the two errors separate; no G>=sqrtH assumption.

Use the same positive amplitude majorant and the ORIGINAL Ingham
layer cakes as in linear_height_ratio_cancellation.py. The exponents
of its two errors are E(g,h,u,v)-h/2 and E(g,h,u,v)-g, where
 E=1-u-v+g[1/2-u+D_I(u)]+h[-1+u+D_I(v)],
 D_I(u)=3u/(1+u), g=logG/L,h=logH/L.
Here9/20<=g<=theta*h<=theta<59/71<5/6 and g<=h<=1.
For fixed g,u,v these exponents are affine in h. Enlarge its interval
to[g,1] while retaining g<=theta; the bounding formulas themselves
do not require the original tag inequality at the artificial endpoints.
At h=g, the retained rational majorant gives
 E-g/2<=1-g/5-(1-6g/5)(u+v)<=91/100.
The Gamma error E-g is smaller there. At h=1, the retained inequality
D_I(u)-u<=1/2 gives E<=1/2+g, so the two errors are respectively
at most g<=theta<91/100 and1/2. Affineness pays both everywhere.
Their total over all boxes is O(N^(91/100)L^14). This proves the
ACTUAL estimates(2)-(3), rather than merely their stationary main.

6. DELETE THE EXACT LARGER UNION FROM THE CURRENT CORE.
For any fixed theta<1 and sufficiently large nonempty tags,
2G<H/2. Thus gamma<eta, eta-gamma>H/2>W_N, and the transposed
union is disjoint. The current condition max>N^(17/20) is precisely
the separate column condition already used in(3). Both coordinate
ceilings in(1) are separate masks, not a curved height-ratio cutoff.
Moreover(gamma+eta)/N<=1/2+o(1)<pi, so the original smooth weight
1-Psi is exactly1 and its sum cap is automatic on this family.

After the full17/20 square and the absolute axes/near-strip deletions,
remove this union with theta53/64 and its transpose. It contains the
previous theta4/5 union with ceilingN/10, so the earlier deletion is
preserved. Equivalently rebuild from the pre-union core and subtract
the new full tag family; no matrix bound on a coupled set difference
is required. The pointwise formula still has all-log total error and
an OPEN signed lower margin on the remaining C_new. More comparable
linear heights and the full transition region remain unresolved.
No RH, target average, new coverage, practical onset, worldwide novelty
or all-method barrier is claimed. The polynomial and arithmetic-offset
tools and all source/runtime corrections persist.
"""
from fractions import Fraction as F

from linear_height_ratio_cancellation import linear_remainder_exponents, tag_ratio_eligible


def selected_density_power(u):
    if type(u) is not F or not 0<=u<=F(1,2):
        raise ValueError('rational u=1-beta in[0,1/2] required')
    if u<=F(1,5):
        return 3*u/(2-3*u)
    if u<=F(3,10):
        return 15*u/(8-5*u)
    return 3*u/(1+u)


def affine_density_slack(u):
    return 2*u+F(6,65)-selected_density_power(u)


def ratio_parameters(theta, epsilon):
    if type(theta) is not F or not F(1,2)<theta<F(59,71):
        raise ValueError('fixed rational theta in(1/2,59/71) required')
    if type(epsilon) is not F or epsilon<=0:
        raise ValueError('fixed positive rational source loss required')
    excess=F(6,65)+epsilon
    decay=(1-excess-(1+excess)*theta)/2
    if decay<=0:
        raise ValueError('source loss exceeds the ratio budget')
    return {'density_excess':excess,'decay':decay,
            'current_core_power':1-F(17,20)*decay}


def box_power(g, h, theta, epsilon):
    params=ratio_parameters(theta,epsilon)
    if any(type(v) is not F for v in (g,h)) or not 0<=g<=theta*h<=h<=1:
        raise ValueError('rational selected height exponents required')
    excess=params['density_excess']
    return 1+(1+excess)*g/2+(excess-1)*h/2
