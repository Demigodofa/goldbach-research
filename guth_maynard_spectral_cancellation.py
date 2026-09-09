"""Actual sub-thirteen-fifteenths cancellation with a paid density patch.

Owner: Kevin's Goldbach research. Purpose: test a stronger arithmetic
input in the already reviewed unequal-height phase argument. This extends
an actual signed deletion; it does not solve the surviving correlation.
No RH, target average, numerical zero evidence or novelty claim is used.

1. THE ACTUAL RESULT AND THE NEW SOURCE'S LIMITATION.
For every FIXED 0<kappa<13/15 and every A>0, the original finite-period
kernel J_N satisfies the COMPLEX signed estimate
 |sum_(0<gamma,eta<=N^kappa) J_N(rho,sigma)|
                              <<_(A,kappa) N/log^A N.             (1)
The actual real parts and all product multiplicities are retained. The
constants are not uniform as kappa approaches13/15. This is not an
absolute estimate: the previously proved large absolute band mass remains.
The old theorem already handles kappa<5/6. Below we prove the new range
5/6<=kappa<13/15; in particular kappa=17/20 is a concrete new cutoff.

Primary source freshly checked2026-09-09: Guth--Maynard,
New large value estimates for Dirichlet polynomials,
arXiv2405.20552v2 (7Apr2026), Theorem1.2 and equation(1.4), printedp2:
https://arxiv.org/pdf/2405.20552v2 . The theorem gives
 N_z(sigma,T)<=T^[15(1-sigma)/(3+5sigma)+o(1)],
and its combination with Ingham gives
 N_z(sigma,T)<=T^[(30/13)(1-sigma)+o(1)].                           (2)
The source counts both height signs; our positive-height count is smaller.
An extra harmless log allowance also covers a copy-count conversion using
the retained local multiplicity bound if required. We use neither the
paper's prime-short-interval corollaries nor a theorem for other L-functions.

Crucially, (2) is NOT a log-power error estimate. Using T^epsilon all
the way to sigma=1 would lose the proof. We use it only on the fixed
range1/2<=sigma<=9/10, and keep the already reviewed Huxley log-power
bound and Vinogradov--Korobov zero-free region closer to1.

2. MAKE THE FAR-FROM-ONE SOURCE INPUT UNIFORM, WITHOUT ASSUMING IT.
Set C=30/13. For any fixed epsilon>0, (2) implies
 N_z(1-u,2Y)<<_epsilon Y^(C*u+epsilon) L^50,
                       1/10<=u<=1/2, Y<=N, L=logN.                (3)
The logarithmic allowance is deliberately harmless here. To justify
uniformity if the source's o(1) is read for each fixed sigma, choose a
finite lower grid in[1/2,9/10] of mesh at most epsilon/(4C). At each
grid point its o(1) is at most epsilon/2 above a fixed threshold. Take
the largest of finitely many thresholds. For any sigma, monotonicity of
the zero count bounds it by its lower grid point, costing at most
C times the mesh in the exponent. This is less than the remaining
epsilon/2. Replacing 2Y by Y only changes a fixed factor. The grid,
threshold and implied constant depend on epsilon, never on N or a zero.

For0<=u<=1/10 retain the source-checked LOG-POWER Huxley estimate
 N_z(1-u,2Y)<<Y^[3u/(2-3u)] L^50
                  <=Y^[(30/17)u] L^50.                           (4)
Its exact exponent slack is
 (30/17)u-3u/(2-3u)=9u(1-10u)/[17(2-3u)]>=0.
The authority is Yashiro1310.0765v2, printedp2 eq(1.2), as already
checked in discrete_spectral_cancellation.py. Its log-power statement
is not replaced by the o(1) synopsis in the new paper.

3. PATCH BOTH DIFFERENT ENERGIES BEFORE APPLYING THE PHASE BOUND.
Reuse the paid low axes and the dyadic preparation from
unequal_spectral_cancellation.py. Every nonempty remaining ordered box
has N^(9/20)<=G<=H<=N^kappa eventually, with separate coordinate masks.
Put g=logG/L,h=logH/L,X=NG/H. The reviewed actual stationary phase
mechanism supplies
 |sum_box A_N exp(iTheta_N)|<<L sqrt(E_G(X)E_H(N)),                 (5)
 E_Y(Z)=sum_(Y<gamma<=2Y, with the individual mask) Z^(2beta-1).
The uniform operator and beta Fourier expansion have already been proved;
their proof is not rerun or strengthened here. Its amplitude bases X,N
are unchanged, with G/X=H/N<=N^(kappa-1).

Let
 d=2-(30/13)kappa>0, epsilon=d/(20kappa), eta=d/20,
 d_0=2(1-kappa)>0.
For the far range u>=1/10, the column and row gap coefficients are
 d_H=2-(30/13)h,
 d_G=2(1+g-h)-(30/13)g=2-2h-(4/13)g.
Both are at least d; in fact d_G-d_H=(4/13)(h-g)>=0. The epsilon
loss in (3) contributes at most kappa*epsilon=d/20. Hence BOTH
relative energy exponents in this range are at most
 -d*u+kappa*epsilon<=-d/10+d/20=-eta.                              (6)

For u<=1/10, (4) instead gives column and row gaps
 2-(30/17)h,
 2(1+g-h)-(30/17)g=2-2h+(4/17)g,
each at least d_0. No epsilon loss occurs in this range. The retained
VK source, arXiv2212.06867v1 printedp2 Theorem1.1, supplies a common cap
 beta<=1-delta_N, delta_N>>L^(-2/3)(logL)^(-1/3),                   (7)
since the relevant heights lie between N^(9/20) and2N. Its source
constant and multiplicity conventions remain unchanged.

Layer cake keeps the total-count baseline beta<=1/2 and integrates
only to1-delta_N. Splitting at u=1/10 and applying (6)-(7) gives
 E_G(X)<<_kappa GL+X L^51[N^-eta+exp(-d_0 delta_N L)],
 E_H(N)<<_kappa HL+N L^51[N^-eta+exp(-d_0 delta_N L)].              (8)
For example the relative row integrand is
X^-2u *G^[density exponent]; its logarithm divided by L is exactly
the row exponent used above. This does not substitute N for X.
The factor logZ in layer cake is at most L. The bound covers an empty
part of the near-one range without change if delta_N is initially large.

The normalized baselines in both equations(8) are at most N^(kappa-1)L.
Using sqrt(XN)=N sqrt(G/H)<=N in (5), then summing O(L^2) disjoint
boxes, gives total stationary main at most
 C_kappa [N^kappa L^4+N^(1-eta)L^54
               +N L^54 exp(-c_kappa L^(1/3)/(logL)^(1/3))].        (9)
Every term is O_(A,kappa)(N/log^A N) for each fixed A. At the concrete
kappa=17/20, d=1/26, epsilon=1/442 and eta=1/520. This is an
asymptotic deduction, not an effective onset or a near-endpoint claim.

4. THE ACTUAL FINITE-PERIOD ERROR REMAINS SMALL PAST FIVE-SIXTHS.
Actual heights at most N^kappa give piN>=4(gamma+eta) for large N.
The retained complex stationary expansion has relative error
O(H^-1/2+G^-1). Because kappa<13/15<9/10 and G>=N^(9/20), the
G^-1 term is absorbed into H^-1/2 just as before, with a positive margin.

The old Ingham-only absolute error calculation remains valid. Write
u=1-beta,v=1-beta' after collapsing beta,beta'<1/2 to the baseline.
Its exponent E(g,h,u,v)-h/2 is enlarged by setting g=h, and the
retained exact majorant D_I(u)<=6u/5+2/5 gives
 E-h/2<=1-h/5-(1-6h/5)(u+v).                                     (10)
For9/20<=h<=5/6 this is at most1-h/5<=91/100. For5/6<=h<=kappa,
the coefficient changes sign, so use u+v<=1 instead: (10) is at most
h<=kappa<13/15<91/100. Thus the summed ACTUAL COMPLEX error still
costs O(N^(91/100)L^14). We have not reused the earlier nonnegative
coefficient assumption outside its valid range. Adding the already paid
low axes to (9)-(10) proves(1), for all the stated fixed kappa.

5. THE PRECISE NEW REMAINDER, INCLUDING THE PREVIOUS RATIO DELETION.
Choose kappa_0=17/20. Start from the original pointwise spectral formula
after the absolutely paid axes and near-height strip, before any both-low
rectangle deletion. Remove the full square in(1) with this kappa_0.
Its intersections with the axes/near strip are absolutely paid, so
this subtraction does not apply the matrix theorem through a coupled mask.
The smooth original height-sum weight is identically1 on the square
for sufficiently large N. The new high part therefore has
 gamma,eta>V_N, |gamma-eta|>W_N, max(gamma,eta)>N^(17/20),
with the unchanged original weight, cap and product multiplicities.

Preserve the previous strongly unequal deletion as follows. Use exactly
the dyadic tag union G<=H^(4/5) from linear_height_ratio_cancellation.py,
the same individual bounds V_N<gamma,eta<=N/10, and impose the NEW
individual column restriction eta>N^(17/20). As already proved for
these tags, gamma<eta and eta-gamma>W_N, so the maximum restriction is
precisely this column mask. The union and its transpose are disjoint
from one another and from the deleted square. The earlier per-box bound
N H^-1/100 L^52 now has H>N^(17/20)/2 and hence total
 O(N^(1983/2000)L^54+N^(91/100)L^14).                              (11)
The finite-period error proof at the linear ceiling is unchanged.

Define C_new by the just-stated high region minus this exact union and
its transpose. Rebuilding from the pre-rectangle formula avoids an
unproved subtraction of a coupled intersection from an older core.
The result remains
 R(N)=2psi(N-1)-N+C_new+O_(A,delta)(N/log^A N).
Its sufficient signed lower margin is OPEN. There is no result at13/15,
no extension of the linear ceiling or arbitrary coupled mask, and no
new prime-pair coverage or numerical zero certificate. All polynomial
components, arithmetic moment/offset tools and source corrections remain.
In particular the corrected2016 finite-period explicit formula and the
old log-power Huxley/VK inputs have not been overwritten by an o(1) bound.
"""
from fractions import Fraction as F

from unequal_spectral_cancellation import stationary_remainder_exponent


def patch_parameters(kappa):
    if type(kappa) is not F or not 0<kappa<F(13,15):
        raise ValueError('fixed rational kappa in(0,13/15) required')
    gap=2-F(30,13)*kappa
    return {'far_gap':gap,'epsilon':gap/(20*kappa),
            'far_saving':gap/20,'near_gap':2*(1-kappa)}


def patched_energy_gaps(g, h, near_one=False):
    if any(type(v) is not F for v in (g,h)) or not 0<=g<=h<=1:
        raise ValueError('rational height exponents0<=g<=h<=1 required')
    coefficient=F(30,17) if near_one else F(30,13)
    return {'row':2*(1+g-h)-coefficient*g,'column':2-coefficient*h}


def far_relative_powers(g, h, u, kappa):
    parameters=patch_parameters(kappa)
    gaps=patched_energy_gaps(g,h)
    if h>kappa or type(u) is not F or not F(1,10)<=u<=F(1,2):
        raise ValueError('h<=kappa and rational u in[1/10,1/2] required')
    epsilon=parameters['epsilon']
    return {'row':-gaps['row']*u+g*epsilon,
            'column':-gaps['column']*u+h*epsilon}


def near_density_slack(u):
    if type(u) is not F or not 0<=u<=F(1,10):
        raise ValueError('rational near-one parameter u in[0,1/10] required')
    return F(30,17)*u-3*u/(2-3*u)


def remainder_majorant(h):
    if type(h) is not F or not F(9,20)<=h<F(13,15):
        raise ValueError('rational h in[9/20,13/15) required')
    return 1-h/5 if h<=F(5,6) else h


def preserved_ratio_deletion_power(kappa):
    patch_parameters(kappa)
    return 1-kappa/100
