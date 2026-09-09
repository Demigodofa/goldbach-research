"""Delete both-low spectral pairs and expose the current density cutoff.

Owner: Kevin's Goldbach research. Purpose: isolate a smaller actual signed
correlation while identifying where this absolute upper-bound method ceases
to give a saving. Neither its cutoff nor a passed guard is a Goldbach proof.

1. ACTUAL DELETION THEOREM AND ITS METHOD BOUNDARY.
Use the finite-period J_N and all multiplicity-counted positive-height
zeros from spectral_low_axis_bound.py. Define
 kappa_*=(52+16sqrt3)/121 =0.658783577860... .
For every fixed0<kappa<kappa_* and fixed A>0,
 sum_(0<gamma,eta<=N^kappa) |J_N(rho,sigma)|
                                     <<_(A,kappa) N/log^A N.          (1)
This includes kappa=13/20. Bounded weights or further restrictions on
this region are also paid absolutely. There is no RH, simple-zero claim,
numerical onset, actual zero computation or new prime-pair coverage.

The number kappa_* is the boundary of the CURRENT Ingham density
exponent envelope below, not a proved lower bound on actual zero mass,
not an impossibility theorem for better density inputs, and not a limit
on using cancellation or the preserved polynomial tools. At that number
this upper bound has exponent1 and no longer proves an all-log saving.

2. REUSE THE PAID BOX BOUND, INCLUDING ITS REAL-PART CAPS.
Use X=3N, L=logX, the compact first height band tagged1 and the following
dyadic bands from spectral_low_axis_bound.py. On scales G<=H with
g=logG/L, h=logH/L, the absolute box bound is C L^12 X^max E, where
 E=b+d-1+g[b-1/2+D(b)]+h[-b+D(d)],
 D(s)=3(1-s)/(2-s), b,d in[1/2,1].                                    (2)
The smaller band retains b<=1-tau_G,
tau_G=min(1/2,c/log(2G+3)). This is the classical zero-free restriction.
The first compact band, all beta<1/2 mass collapsed under monotone weights,
two layer-cake factors and every product multiplicity were already paid.
Enlarging to full Cartesian bands was legitimate because the sum is
absolute. Here g<=h<=kappa since H<=N^kappa<X^kappa.

The coefficient of g in (2) is b-1/2+D(b)>=0. Therefore E(g,h)<=E(h,h)
for the SAME admissible b,d. This change does not release b's zero-free
cap. Write u=1-b, v=1-d and D_u=3u/(1+u). Then
 E(h,h)=1-h/2+f_h(u)+f_h(v), f_h(u)=-u+h D_u.                          (3)

3. AN EXPLICIT RATIONAL PROOF AT kappa=13/20.
For every0<=u<=1/2,
 D_u<=(20/13)u+49/200.                                               (4)
Its slack is (4000u^2-3163u+637)/(2600(1+u)); the numerator is
4000(u-3163/8000)^2+187431/16000>0. Thus for h<=13/20,
 E<=1-(1-20h/13)(u+v)-h/100.                                        (5)
Let alpha=min(1,sqrt c). For h>=alpha/sqrtL, (5) gives an exponent
loss at least alpha/(100sqrtL). For smaller h, eventually
1-20h/13>=1/2, while the unchanged cap on u gives
 u>=tau_G>=min(1/2,c/log(2H+3))>=c/(2alpha sqrtL).
The final inequality holds for sufficiently large N; H<=exp(alpha sqrtL).
Since alpha^2<=c, the zero-free contribution gives at least
alpha/(4sqrtL), which is more than required. Every box is therefore
O(L^12 X exp[-(alpha/100)sqrtL]). The O(L^2) box sum proves (1)
at13/20. No density hypothesis was substituted for a pair-correlation
estimate; only positive single-zero counts were used.

4. EXACT ENVELOPE AND THE FULL RANGE OF THIS INPUT.
Dropping the cap ONLY to compute the density envelope, maximize f_h on
u in[0,1/2]. Its derivative is -1+3h/(1+u)^2. The maximizing u is
0 for h<=1/3, sqrt(3h)-1 for1/3<=h<=3/4, and1/2 for h>=3/4.
Consequently the maximum in (3) is
 M(h)=1-h/2,                             0<=h<=1/3;
      3+(11/2)h-4sqrt(3h),               1/3<=h<=3/4;
      (3/2)h,                           3/4<=h<=1.                    (6)
Its positive relevant crossing M(h)=1 in the middle interval is kappa_*.
Indeed, squaring the equation with both sides positive gives
121h^2-104h+16=0. The smaller root(52-16sqrt3)/121 is below1/3 and
does not belong to that branch. Hence M(h)<1 for0<h<kappa_*, and
M(kappa_*)=1. At the latter point the maximizing real part is
2-sqrt(3kappa_*), approximately0.59417, away from the zero-free boundary.
This is an envelope calculation, not a statement that actual zeros
attain the density bound or produce large kernels with that distribution.

For a uniform all-log argument at any FIXED0<kappa<kappa_*, set
 B_kappa=max_(0<=u<=1/2)[D_u-u/kappa].
It equals0 for kappa<=1/3 and
3+1/kappa-2sqrt(3/kappa) for1/3<kappa<kappa_*.
In this range delta_kappa=1/2-2B_kappa>0. The tangent inequality
D_u<=u/kappa+B_kappa then proves, retaining the cap again,
 E<=1-(1-h/kappa)(u+v)-delta_kappa*h, h<=kappa.                        (7)
For h>=alpha/sqrtL the last term supplies a fixed positive multiple of
1/sqrtL. For smaller h, eventually1-h/kappa>=1/2, and the same
zero-free estimate used after (5) supplies another such multiple. Thus
the total is O_kappa(N log^14N exp[-c_kappa sqrt(logN)]), c_kappa>0,
which proves (1) with no claim of uniform constants as kappa approaches
kappa_*. At the boundary, (6)-(7) cease to yield a saving; they do not
establish an actual obstruction there.

5. THE SPECIFIED REMAINING SIGNED REGION.
Keep kappa=13/20 as a definite independently checked choice. In the
fixed-delta pointwise formula from spectral_low_axis_bound.py, delete
also the both-low box. Its union with the already paid axes and near-height
strip costs at most the sum of their absolute bounds. The finite C_high
therefore retains exactly the original smooth weight and product
multiplicities on
 gamma,eta>V_N; |gamma-eta|>W_N; max(gamma,eta)>N^(13/20);
 gamma+eta<=(pi+2delta)N,
where V_N=sqrtN exp[-(loglogN)^2] and
W_N=exp[(alpha/30)sqrt(logN)]. In particular
 R(N)=2psi(N-1)-N+C_high+O_(A,delta)(N/log^A N).                       (8)
The signed lower margin for C_high remains OPEN. The inherited
opposite-sign error is unchanged; no square-root full error follows.
All prior source corrections and polynomial components remain valid.

Authority: the reviewed phase, counting, zero-free and uniform Ingham
inputs in spectral_low_axis_bound.py and spectral_diagonal_bound.py;
https://arxiv.org/pdf/2507.15184v2 is the checked density source.
No new literature or novelty claim, prime range or numerical zero evidence.
The helpers below guard rational inequalities and the branch boundary.
"""
from fractions import Fraction as F

from spectral_low_axis_bound import density_box_exponent, density_power


def rational_density_slack(u):
    return F(20,13)*u+F(49,200)-density_power(u)


def thirteen_twentieths_envelope(h, u, v):
    if type(h) is not F or not 0<=h<=F(13,20):
        raise ValueError('rational h in[0,13/20] required')
    density_power(u)
    density_power(v)
    return 1-(1-F(20,13)*h)*(u+v)-h/100


def middle_branch_crossing_polynomial(h):
    if type(h) is not F or not F(1,3)<=h<=F(3,4):
        raise ValueError('rational h in middle branch[1/3,3/4] required')
    return 121*h*h-104*h+16


def critical_line_box_exponent(h):
    """Envelope at beta=beta'=1/2; no claim of actual mass saturation."""
    return density_box_exponent(h,h,F(1,2),F(1,2))
