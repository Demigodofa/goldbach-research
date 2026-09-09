"""Signed cancellation for every fixed sub-five-sixths height rectangle.

Owner: Kevin's Goldbach research. Purpose: extend the reviewed discrete
phase mechanism to unequal zero heights and pay its actual approximation
error before deleting a larger region from the pointwise correlation.
This is mathematical research, not a manuscript or a claim of novelty.
All counts include copies. No RH, numerical zero list, target average,
prime-pair hypothesis or Goldbach coverage is asserted.

1. STATEMENT AND WHAT REMAINS OPEN.
For the finite-period kernel J_N from stationary_spectral_core.py, every
FIXED 0<kappa<5/6 and A>0 satisfy the COMPLEX signed estimate
 |sum_(0<gamma,eta<=N^kappa) J_N(rho,sigma)|
                                     <<_(A,kappa) N/log^A N.         (1)
The constants are not asserted uniform as kappa approaches5/6. In
particular kappa=4/5 is a concrete retained choice. The conclusion is
signed, not absolute; the already proved large absolute mass at N^(2/3)
persists. This generalizes the specified band in feb00a9.

The lower axes and near-height strip remain absolutely paid. Therefore
in the original pointwise R formula the new finite C_high can retain
 gamma,eta>V_N; |gamma-eta|>W_N; max(gamma,eta)>N^(4/5),
with the original smooth height-sum weight1-Psi((gamma+eta)/N), its
cap gamma+eta<=(pi+2delta)N, and all product multiplicities. Here
 V_N=sqrtN exp[-(loglogN)^2], W_N=exp[(alpha/30)sqrt(logN)]
are unchanged. The formula is still
 R(N)=2psi(N-1)-N+C_high+O_(A,delta)(N/log^A N).                       (2)
Its sufficient signed lower margin remains OPEN. No statement at5/6,
all-height estimate, arbitrary coupled mask, or full square-root error
follows from this result.

2. PREPARE GENUINELY UNEQUAL SCALES WITHOUT LOSING LOW HEIGHTS.
The theorem in spectral_low_axis_bound.py pays min(gamma,eta)<=V_N
absolutely, even with both heights through KN. For kappa<=1/2 the
previous both-low absolute theorem already proves (1). We may thus fix
1/2<kappa<5/6 and restrict each remaining coordinate to(V_N,N^kappa].
Partition into dyadic bands(G,2G], with separate sharp truncations at
V_N and N^kappa. By symmetry consider tags G<=H. There are O(L^2)
ordered boxes, L=logN. Tags of nonempty bands satisfy, eventually,
 N^(9/20)<=V_N/2<G<=H<=N^kappa.                                     (3)
Using <= in place of < at a possible dyadic endpoint changes nothing.
All actual heights in this restricted region are at most N^kappa.

Put r=G/H, gamma=Gx, eta=Hy, with x,y in[1,2]. For
F(gamma,eta)=gamma loggamma+eta logeta-(gamma+eta)log(gamma+eta),
the exact residual phase after removing gamma log r is
 F(Gx,Hy)-Gx log r=G phi_r(x,y),
 phi_r=xlogx+[ylogy-(y+rx)log(y+rx)]/r
      =xlogx-int_0^x [1+log(y+rt)]dt.                               (4)
The integral expression defines a smooth limit at r=0 and shows all
fixed derivatives are uniformly bounded for0<=r<=1 on the fixed
positive ratio box(1/2,3)^2. In particular
 phi_(r,xy)=-1/(y+rx),
bounded away from0. At r=0 the phase is xlog(x/y)-x. The separable
carrier removed from Theta is (gamma+eta)logN+gamma log r, not just
the logN term. Carriers are restored in unit-modulus coefficients.

3. UNIFORM CONTINUOUS AND DISCRETE OPERATOR BOUNDS.
Let a_r(x,y) be supported in a fixed compact subset of(1/2,3)^2 and
have uniformly bounded mixed derivatives through order12, seminorm Q.
The scaled kernel is exp(iG phi_r(x,y))a_r(x,y). In its TT* kernel,
the phase-difference derivative in y is
 (1/r)log[(y+rx')/(y+rx)]=int_x^x' dt/(y+rt).                         (5)
It is comparable in magnitude to |x-x'|, with higher y derivatives
of the normalized quotient bounded uniformly even at r=0. The two
integrations by parts and Schur argument in the preceding module give
scaled norm O(Q G^-1/2). Restoring physical measures multiplies by
sqrt(GH), so the physical continuous norm is O(Q sqrtH).

Use the same fixed, real-even angular Fourier projection P as before,
equal1 on[-4,4] and0 outside[-8,8], AFTER removing both carriers.
The physical residual first derivatives are
 d_gamma=log[x/(y+rx)], d_eta=log[y/(y+rx)],
bounded in absolute value by log7 on the fixed support. Higher pure
derivatives in gamma have scale G^(1-j), those in eta at most H^(1-j).
The amplitude derivatives have the corresponding inverse coordinate
scales. Nonstationary Fourier integration thus gives x and y projection
tails O(Q G^-4) and O(Q H^-4), respectively, uniformly on the whole
physical plane after Fourier inversion. The decomposition
 K-PKP=(I-P)K+PK(I-P)
pays the second projection with the fixed L1 norm of its Schwartz kernel.

If the two sequences have at most D_G,D_H copies per unit interval,
their projected delta measures have L2 norms at most
C sqrt(D_G)||c||_2 and C sqrt(D_H)||d||_2 by the previous copy-counted
Schur proof, including coincident copies. The remainder costs at most
 C Q G^-4 sqrt(GH D_GD_H)||c||_2||d||_2,
which is absorbed into Q sqrt(H D_GD_H)||c||_2||d||_2 because G>=1.
Consequently the DISCRETE bound is
 |sum_ij c_i d_j e^(iG phi_r(x_i,y_j))a_r(x_i,y_j)|
                   << Q sqrt(H D_GD_H)||c||_2||d||_2.                (6)
Actual zeros have D_G,D_H=O(L) by local Riemann-von Mangoldt. Sharp
individual band restrictions are separate masks and are allowed here.

4. RETAIN THE REAL PARTS IN TWO DIFFERENT ENERGY BASES.
Set X=NG/H. The actual stationary amplitude and phase give
 A_N e^(iTheta)=2sqrt(2pi) H^-1/2 X^(beta-1/2)N^(beta'-1/2)
  *a_r(x,y,beta,beta')
  *exp{i[G phi_r+gamma logX+eta logN-pi/4]},
 a_r=(y+rx)^-1/2 [x/(y+rx)]^(beta-1/2)
                         *[y/(y+rx)]^(beta'-1/2).                   (7)
Insert fixed height cutoffs equal1 on[1,2]. Extend beta,beta' smoothly
to a fixed compact interval containing[0,1]. The resulting amplitude
has uniformly bounded derivatives in all parameters, including r=0.
As before, Fourier expansion only in beta,beta' has summable required
xy seminorms; four integrations by parts in each beta suffice. The
Fourier factors and the restored carriers have modulus1. Applying (6)
mode by mode and cancelling H^-1/2 leaves
 |sum_box A_N e^(iTheta)| << L sqrt(E_G(X) E_H(N)),                    (8)
 E_Y(Z)=sum_(Y<gamma<=2Y, with the individual mask) Z^(2beta-1).
This does not pretend that beta is a smooth function of its ordinate.

5. BOTH ACTUAL ENERGIES HAVE A UNIFORM POSITIVE DENSITY GAP.
Use precisely the log-power Ingham/Huxley consequence and the
Vinogradov-Korobov zero-free input source-checked in
discrete_spectral_cancellation.py:
 N_z(sigma,U)<<U^[(12/5)(1-sigma)]log^50U, 1/2<=sigma<=1;
 beta<=1-delta_N, delta_N>>L^-2/3(logL)^-1/3.                         (9)
The latter is uniform for our heights: they are eventually>=3 and
<=2N, so the denominator of the retained explicit VK region at2N
gives a common delta_N. No new compact-height extension is needed.

Write g=logG/L,h=logH/L. Then logX=(1+g-h)L, with X>=1. The
column and row coefficients of u=1-sigma in the decay exponent are
 d_H=2-(12/5)h,
 d_G=2(1+g-h)-(12/5)g=2-2h-(2/5)g,
both at least d_kappa=2-(12/5)kappa>0. The row coefficient exceeds
the column coefficient by(2/5)(h-g), so an unequal ratio does not lose
the near-one gap. Layer cake, retaining the actual beta cap, gives
 E_G(X)<<GL+X L^51 exp[-d_kappa delta_N L],
 E_H(N)<<HL+N L^51 exp[-d_kappa delta_N L].                           (10)
The collapsed beta<=1/2 baselines use total counts. Both relative
baselines are power-small: G/X=H/N<=N^(kappa-1). Thus (8), summed
over the O(L^2) boxes, is bounded by
 N^kappa L^4+N L^54 exp[-c_kappa L^(1/3)/(logL)^(1/3)].               (11)
We used sqrt(XN)=N sqrt(G/H)<=N; no ratio saving was required.
This is O_(A,kappa)(N/log^A N) for every fixed A. A fixed N^epsilon
density loss would not justify the near-one step. At kappa=5/6 the
uniform d_kappa is0, and this proof does not supply the same conclusion.

6. PAY THE ACTUAL COMPLEX STATIONARY ERROR ON ALL THESE BOXES.
Actual gamma+eta<=2N^kappa implies piN>=4(gamma+eta) for large N.
The normalized finite-period integral in stationary_spectral_core.py
therefore has its already proved uniform relative error
O((gamma+eta)^-1/2)=O(H^-1/2). Uniform complex Stirling adds O(G^-1).
By (3), G>=N^(9/20)>=sqrtH when H<=N^(5/6), eventually. Hence
 J_N=A_N e^(iTheta)[1+O(H^-1/2)]                                    (12)
uniformly over the restricted boxes, including all0<beta,beta'<1.

This relative error must be summed absolutely. Directly from (7),
 A_N << N^(b+d-1)G^(b-1/2)H^-b.
Apply the two original Ingham layer-cake bounds from
spectral_low_axis_bound.py to this positive amplitude majorant. Its
real-part bases NG/H and N are nondecreasing; beta<1/2 collapses to
the total-count baseline. No reverse bound on |J_N| is used. The box
error costs at most L^12 N^max[E(g,h,b,d)-h/2], where
 E=b+d-1+g[b-1/2+D(b)]+h[-b+D(d)], D(b)=3(1-b)/(2-b).
The coefficient of g is nonnegative. Set g=h to enlarge this exponent,
write u=1-b,v=1-d, and obtain
 E-h/2 <= 1-h+[-u+hD_u]+[-v+hD_v], D_u=3u/(1+u).
For0<=u<=1/2 the exact rational inequality
 D_u<=(6/5)u+2/5
has slack (1-2u)(2-3u)/(5(1+u))>=0. It follows that
 E-h/2 <=1-h/5-(1-6h/5)(u+v)<=1-h/5<=91/100,                        (13)
since9/20<=h<=5/6. Consequently the total COMPLEX replacement error
is O(N^(91/100)L^14), which is all-log small. This is a convenient
nonoptimal bound, not a claim about saturation of the density envelope.
Combining (11)-(13) and the earlier low-axis absolute theorem proves (1).

7. RETURN TO THE ORIGINAL SUPPORT WITHOUT AN UNLICENSED MASK.
Choose kappa=4/5. The original smooth weight1-Psi is exactly1 on the
whole removed rectangle for sufficiently large N. Its parts in the
already removed axes and near-height strip are absolutely all-log, so
their subtraction from (1) is legitimate. The old both-low13/20 box
and the old specific T=N^(2/3) band are contained in the new rectangle
eventually; the former is absolutely paid, and the latter is signed
paid, with their stated overlaps handled by the retained set identity.
Equivalently start from the pointwise reduction before any both-low
deletion, remove the axes and near strip, then remove this rectangle.
This proves exactly (2), without using (6) through any coupled mask.
All other heights and the sufficient Goldbach signed lower margin
remain open. No universal barrier is claimed at this method's endpoint.

Source authorities are inherited without alteration:
https://arxiv.org/pdf/1310.0765v2 printedp2 eqs(1.1),(1.2), actual
log-power zeta statements, not a later cusp-form theorem;
https://arxiv.org/pdf/2212.06867v1 printedp2 Theorem1.1;
https://arxiv.org/pdf/2507.15184v2 retained uniform Ingham authority.
The2016 explicit-formula correction, all earlier source corrections,
polynomial components and runtime boundaries remain in force.
"""
from fractions import Fraction as F

from spectral_low_axis_bound import density_box_exponent, density_power


def residual_mixed_derivative(r, x, y):
    if type(r) is not F or not 0<=r<=1:
        raise ValueError('rational ratio in[0,1] required')
    if any(type(t) is not F or not F(1,2)<=t<=3 for t in (x,y)):
        raise ValueError('rational normalized heights in[1/2,3] required')
    return -1/(y+r*x)


def unequal_energy_gaps(g, h):
    if any(type(t) is not F for t in (g,h)) or not 0<=g<=h<=1:
        raise ValueError('rational height powers0<=g<=h<=1 required')
    return {'row':2-2*h-F(2,5)*g, 'column':2-F(12,5)*h}


def energy_base_powers(g, h):
    unequal_energy_gaps(g,h)
    return {'row_base':1+g-h, 'row_relative_baseline':h-1,
            'column_relative_baseline':h-1, 'product_root':1+(g-h)/2}


def remainder_density_slack(u):
    return F(6,5)*u+F(2,5)-density_power(u)


def stationary_remainder_exponent(g, h, u, v):
    unequal_energy_gaps(g,h)
    density_power(u)
    density_power(v)
    return density_box_exponent(g,h,u,v)-h/2


def stationary_remainder_majorant(h, u, v):
    if type(h) is not F or not F(9,20)<=h<=F(5,6):
        raise ValueError('rational height power in[9/20,5/6] required')
    density_power(u)
    density_power(v)
    return 1-h/5-(1-F(6,5)*h)*(u+v)


def unequal_scale_powers(g, h):
    unequal_energy_gaps(g,h)
    return {'continuous':h/2, 'stationary_amplitude':-h/2,
            'projection_remainder':-4*g+(g+h)/2,
            'gamma_relative_error':-g, 'integral_relative_error':-h/2}
