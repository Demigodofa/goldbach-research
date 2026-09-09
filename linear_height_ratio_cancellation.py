"""Use unequal height ratios to pay selected boxes at a linear ceiling.

Owner: Kevin's Goldbach research. Purpose: test whether the ratio retained
by the discrete phase bound can absorb energy growth, and specify exactly
which additional part of the actual signed correlation it deletes.
No RH, numerical zero evidence, target averaging, Goldbach coverage,
publication or novelty claim. Earlier polynomial tools remain available.

1. PRECISE FAMILY AND COMPLEX SIGNED CONCLUSION.
Keep J_N and the current finite C_high from unequal_spectral_cancellation.py.
Let L=logN, V_N=sqrtN exp[-(loglogN)^2], and fix
 1/2<theta<9/11.
Use the same disjoint dyadic bands(G,2G], with tags G=1,2,4,...;
the compact tag1 band is irrelevant after the height restriction below.
For every pair of tags G<=H satisfying G<=H^theta, take the COMPLETE
Cartesian product of its individually restricted zero lists
 V_N<gamma<=N/10, gamma in(G,2G];
 V_N<eta<=N/10, eta in(H,2H].                                       (1)
Let U_theta be the disjoint union of these rectangles. All zero copies
and their product multiplicities are retained. The theorem is
 |sum_(rho,sigma in U_theta) J_N(rho,sigma)|
  <<_theta N^[1-(9/20)delta_theta]L^54+N^(91/100)L^14,
 delta_theta=(9-11theta)/20>0.                                     (2)
Thus it is O_(A,theta)(N/log^A N) for every fixed A. The transposed
rectangles satisfy the same bound by the exact symmetry of J_N.

For the concrete choice theta=4/5, delta_theta=1/100. In the ACTUAL
retained C_high, restrict the larger ordinate further to eta>N^(4/5).
This remains an individual column mask and improves (2) to
 O(N^(124/125)L^54+N^(91/100)L^14).                                 (3)
This is the new deleted part, together with its transpose. Its original
smooth weight is exactly1 for sufficiently large N, and its near-height
strip restriction is automatic, as proved below.

The remaining high-zero signed lower margin is still OPEN. This is a
specified union of dyadic rectangles, not the same as the curved mask
gamma<=eta^theta. No arbitrary coupled mask, extension above the N/10
ceiling, endpoint transition estimate or theta=9/11 conclusion is asserted.

2. A SHARPER SHAPE OF THE ALREADY CHECKED CLASSICAL DENSITY BOUNDS.
For u=1-sigma in[0,1/2], the previously source-checked Ingham/Huxley
bounds, with the retained harmless log^50 allowance, give
 N_z(1-u,Y)<<Y^D_*(u)(logY)^50,
 D_*(u)=3u/(2-3u), 0<=u<=1/4;
        3u/(1+u),  1/4<=u<=1/2.                                    (4)
The two exponents agree at1/4. We need the exact majorant
 D_*(u)<=2u+1/10.                                                   (5)
In the first interval its slack is
 (1-4u)(15u+2)/(10(2-3u))>=0;
in the second interval its slack is
 (5u-1)(4u-1)/(10(1+u))>=0.
Both vanish at1/4. This is an elementary consequence of the actual
log-power source statements; no new density theorem is assumed.

3. THE INDIVIDUAL ENERGIES MAY GROW; THEIR PRODUCT IS PAID BY THE RATIO.
For Y<=Z<=N, with Y>=N^(9/20), and any individual subset of zeros in
(Y,2Y], write E_Y(Z)=sum Z^(2beta-1). The beta<=1/2 baseline costs
O(YL). Layer cake and (4)-(5) give
 E_Y(Z)<<YL+Z L^51 max_(0<=u<=1/2)[(Y/Z)^(2u)Y^(1/10)]
         << Z Y^(1/10)L^51.                                       (6)
The total-count baseline is absorbed because Y<=Z and Y>=1. Factors
from replacing Y by2Y in the counting height are uniformly bounded.
No zero-free cap is needed for this particular, deliberately weaker,
energy estimate. All prior zero-free results remain available elsewhere.

On a box in (1), set X=NG/H. Since H<=N/10 and G<=H, one has
G<=X<=N and H<=N. The phase/amplitude result in the preceding module
is uniform for these ratios and yields
 |sum_box A_N exp(iTheta_N)| << L sqrt(E_G(X)E_H(N)).
Its proof only requires large G, positive ratio boxes and the stated
separate masks; it does not require H to be sublinear. Inserting (6)
and sqrt(XN)=N sqrt(G/H) gives
 |sum_box A_N exp(iTheta_N)|
       << N G^(11/20)H^(-9/20)L^52
       <= N H^(-delta_theta)L^52.                                 (7)
Thus energy growth is allowed and is paid by the height ratio.

Every nonempty band after the low-axis restriction has
G>V_N/2>=N^(9/20), eventually; hence also H>=N^(9/20). Summing
(7) over O(L^2) disjoint tag pairs proves the first term in (2).
For (3), eta>N^(4/5) and eta<=2H imply H>N^(4/5)/2; with theta=4/5
the summed main is O(N^[1-(4/5)(1/100)]L^54)=O(N^(124/125)L^54).

4. PAY BOTH DIFFERENT ACTUAL STATIONARY ERRORS AT LINEAR HEIGHTS.
Actual gamma,eta<=N/10 imply 4(gamma+eta)<=4N/5<piN. The uniform
finite-period normalized stationary expansion therefore remains valid.
Uniform complex Stirling has error O(G^-1), whereas the normalized
integral has error O(H^-1/2). At linear H they must be retained separately:
 J_N=A_N exp(iTheta_N)[1+O(H^-1/2+G^-1)].                            (8)
We do not assume G>=sqrtH here.

Directly majorize the positive stationary amplitude by
N^(b+d-1)G^(b-1/2)H^-b and apply the two original Ingham layer cakes,
exactly as in the preceding proof. The exponent is
 E(g,h,u,v)=1-u-v+g[1/2-u+D_u]+h[-1+u+D_v],
 D_u=3u/(1+u), u,v in[0,1/2], g=logG/L, h=logH/L.
Both error exponents are E-h/2 and E-g. Here
9/20<=g<=theta*h<=theta<9/11<5/6, and g<=h<=1.
For fixed g,u,v each error exponent is affine in h, so it suffices to
check h=g and h=1; the enlargement preserves the fixed bound on g.

At h=g, the already proved rational Ingham majorant gives
 E(g,g)-g/2<=1-g/5-(1-6g/5)(u+v)<=91/100.                            (9)
The Gamma exponent E(g,g)-g is smaller by g/2, so is also paid.
At h=1, the earlier exact inequality D_u-u<=1/2 gives
 E(g,1)=D_v-v+g[1/2+D_u-u]<=1/2+g.
Consequently
 E(g,1)-1/2<=g<=theta<9/11<91/100;
 E(g,1)-g<=1/2.                                                     (10)
Affineness now bounds BOTH error exponents by91/100 throughout every
box. Each costs O(N^(91/100)L^12), and O(L^2) boxes give the second
terms in (2)-(3). This proves the ACTUAL COMPLEX bounds, without
reversing a one-sided kernel inequality or silently dropping Gamma errors.

5. DELETE EXACTLY THESE RECTANGLES FROM THE CURRENT POINTWISE CORE.
For large N, G<=H^theta and H>=V_N/2 imply 2G<H/2, since theta<1.
Thus throughout each selected rectangle gamma<=2G<H/2<eta, so eta
really is the larger height; moreover eta-gamma>H/2. This exceeds
the retained W_N=exp[(alpha/30)sqrt(logN)] eventually. The chosen
rectangles and their transposes are disjoint, and have no diagonal.

Both heights>V_N are individual masks. The current max>N^(4/5)
condition becomes precisely the individual column mask eta>N^(4/5)
on the chosen orientation. No curved or other coupled restriction enters
the matrix theorem. Finally gamma+eta<=N/5 ensures the original
1-Psi((gamma+eta)/N)=1. The original sum cap and separated-height
condition are automatic on this region.

Define D_N to be this exact union for theta=4/5 with its transpose and
the indicated separate masks. Its signed contribution is paid by (3),
so the updated finite C_remaining is exactly the previous C_high minus
D_N, retaining all original weights and every remaining copy. Then
 R(N)=2psi(N-1)-N+C_remaining+O_(A,delta)(N/log^A N).
The sufficient signed lower margin for C_remaining remains OPEN.
The main-scale, more comparable high heights and the endpoint transition
were not estimated by this result. A failed bound at theta=9/11 would
only be a limitation of the displayed density/ratio budget.

Sources are inherited from discrete_spectral_cancellation.py, unchanged:
Yashiro1310.0765v2 printedp2 eqs(1.1),(1.2), the actual zeta log-power
statements; arXiv2507.15184v2 for uniform Ingham and the existing local
counting/finite-period kernel authorities. The2016 explicit-formula error
correction remains binding. No new literature claim or numerical onset.
"""
from fractions import Fraction as F

from discrete_spectral_cancellation import classical_density_coefficient
from spectral_low_axis_bound import density_box_exponent, density_power


def piecewise_density_power(u):
    density_power(u)
    return u*classical_density_coefficient(1-u)


def ratio_density_slack(u):
    return 2*u+F(1,10)-piecewise_density_power(u)


def ratio_decay(theta):
    if type(theta) is not F or not 0<theta<=1:
        raise ValueError('rational exponent in(0,1] required')
    return (9-11*theta)/20


def signed_box_relative_exponent(g, h):
    if any(type(t) is not F for t in (g,h)) or not 0<=g<=h<=1:
        raise ValueError('rational height powers0<=g<=h<=1 required')
    return F(11,20)*g-F(9,20)*h


def linear_remainder_exponents(g, h, u, v):
    exponent=density_box_exponent(g,h,u,v)
    return {'integral':exponent-h/2, 'gamma':exponent-g}


def tag_ratio_eligible(small_tag, large_tag, theta=F(4,5)):
    for tag in (small_tag,large_tag):
        if type(tag) is not int or tag<1 or tag&(tag-1):
            raise ValueError('positive dyadic integer tags required')
    ratio_decay(theta)
    return small_tag<=large_tag and small_tag**theta.denominator<=large_tag**theta.numerator
