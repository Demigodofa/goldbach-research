"""Actual signed cancellation in the surviving T=N^(2/3) spectral band.

Owner: Kevin's Goldbach research. Purpose: use the retained interior phase
to control a signed contribution which has already proved large in absolute
value. This is one specified band, not the full Goldbach correlation margin.
No RH, target averaging, prime-pair conjecture, zero computation or novelty
claim is made. All polynomial tools and source corrections are preserved.

1. THE RESULT AND THE MASK THAT IS ACTUALLY LICENSED.
Use J_N, A_N and Theta_N from stationary_spectral_core.py and T=N^(2/3).
Let B_T be all positive-height zeros with T<gamma<=2T, counted with copies.
For every fixed A>0 we prove the COMPLEX signed estimate
 |sum_(rho,sigma in B_T) J_N(rho,sigma)| <<_A N/log^A N.                (1)
The same estimate holds after removing the previously paid near-height
strip |gamma-eta|<=W_N. It follows by subtraction of that absolute-small
strip, not by applying a matrix bound through an arbitrary coupled mask.
Thus (1) deletes this actual band from the retained C_high expression.
Its termwise absolute mass is still >>Nlog^2N by the preceding theorem;
(1) therefore proves real cancellation, rather than a formal rearrangement.
The rest of C_high and the sufficient Goldbach lower margin remain OPEN.

2. CONTINUOUS MIXED-PHASE OPERATOR, WITH ITS CORRECT SCALE.
Remove the separable carrier exp[i(gamma+eta)logN] into the coefficients.
The remaining phase is
 F(x,y)=xlogx+ylogy-(x+y)log(x+y).
For a smooth amplitude a supported inside the fixed ratio box(1/2,3)^2,
let K_T have kernel exp[iF(x,y)] a(x/T,y/T), extended by0 outside the
positive support. We claim
 ||K_T||_(L2->L2) << Q(a)*sqrtT,                                      (2)
where Q is a fixed finite smooth seminorm, for example the maximum of
mixed derivatives through order12 on this fixed box.

Indeed F(Tu,Tv)=T f(u,v), f=u logu+v logv-(u+v)log(u+v). The scaled
operator times its adjoint has kernel
 int exp{iT[f(u,v)-f(u',v)]}a(u,v)conj(a(u',v))dv.
The derivative of the phase difference in v is
 log[(u'+v)/(u+v)]. Its magnitude is comparable to |u-u'| on this box.
After dividing by u-u', every further v derivative is uniformly bounded.
For u!=u', two integrations by parts therefore bound this kernel by
C Q(a)^2 (1+T|u-u'|)^-2, also valid at u=u' by the trivial integral bound.
Schur's test gives a squared scaled-operator norm O(Q(a)^2/T).
Restoring dx,dy multiplies the operator norm by T, proving (2).
The rank1 full Hessian is no obstacle here: the mixed derivative is
-1/(u+v), bounded away from0 on the fixed box.

3. TRANSFER TO AN IRREGULAR DISCRETE MEASURE, INCLUDING COINCIDENCES.
Take any finite sequences x_i,y_j in[T,2T], with at most D copies in each
unit interval (D>=1). No lower bound on individual spacing is imposed.
The desired discrete estimate is
 |sum_ij c_i d_j exp[iF(x_i,y_j)]a(x_i/T,y_j/T)|
                << Q(a)*D*sqrtT*||c||_2*||d||_2.                     (3)

Choose a FIXED real even smooth physical-frequency multiplier P, equal1
on[-4,4] and0 outside[-8,8], using angular Fourier frequencies. On the
support of a, |F_x| and |F_y| are at most log7<4. The kernel p of P is
Schwartz and has finite L1 norm. For |xi|>=4, repeated integration by
parts in x gives the partial Fourier bound
 |Fourier_x K_T(xi,y)| <<_r Q_r(a) T^(1-r)(1+|xi|)^-r,
uniformly in y, and similarly for Fourier_y. All derivatives of F beyond
the first have the appropriate inverse-T scale, and the support has length
O(T). Integrating the frequency tail gives, for any fixed M,
 sup_(x,y in R) |K_T-PK_TP|(x,y) <<_M Q_(M+1)(a) T^-M.                (4)
For clarity, use K_T-PK_TP=(I-P)K_T+P K_T(I-P). The second term is
bounded by the uniform right-frequency tail times ||p||_1. Thus the
second projection does not introduce an unproved restriction on its tails.
Only M=4 is needed below; the stated Q with order12 is more than enough.

For mu=sum_j d_j delta_(y_j), self-adjointness of P gives
 ||Pmu||_2^2=sum_jk d_j conj(d_k) q(y_j-y_k), q=p*p.
Schwartz decay and the copy-counted local occupancy imply
sup_j sum_k |q(y_j-y_k)| << D by summing over unit intervals. Schur's
test therefore gives ||Pmu||_2 <<sqrtD ||d||_2. The same holds for the
other sequence, including coincident copies. Applying (2) between these
two projected measures costs D sqrtT ||c||_2||d||_2.
The pointwise remainder in (4) costs at most
Q T^-4 sqrt(M_x M_y)||c||_2||d||_2 << Q D T^-3||c||_2||d||_2,
since M_x,M_y=O(TD). This is absorbed into (3).
Taking D=O(logT) is legitimate for the actual zeros by the already checked
multiplicity-counted local Riemann-von Mangoldt bound.

4. RETAIN THE REAL-PART-DEPENDENT AMPLITUDE.
Write x=gamma/T,y=eta/T. Apart from 2sqrt(2pi)T^-1/2, the stationary
amplitude is the smooth function
 a(x,y,b,d)=(x+y)^-1/2 [x/(x+y)]^(b-1/2)[y/(x+y)]^(d-1/2)
times the separate weights N^(b-1/2)N^(d-1/2). Insert fixed smooth
height cutoffs equal1 on[1,2]. Extend b,d smoothly to a compact interval
containing[0,1], then Fourier-expand only these two parameters. The
coefficients a_mn(x,y) have summable Q(a_mn): four integrations in each
real-part variable give a bound C(1+|m|)^-4(1+|n|)^-4 for their required
xy seminorms. All intervals and derivatives are fixed, independent of N.
The factors exp(i*m*constant*beta) and exp(i*n*constant*beta') have
modulus1 and therefore do not change the coefficient l2 norms. This does
not pretend beta is a smooth function of height.

Apply (3) to each coefficient with row weights
N^(beta-1/2)exp(i gamma logN) and the corresponding column weights.
The T^-1/2 stationary factor cancels the sqrtT operator cost. Consequently
 |sum_(rho,sigma in B_T) A_N exp(iTheta_N)| << logT * E_N,
 E_N=sum_(rho in B_T) N^(2beta-1).                                    (5)
The possibly large carrier frequency logN was removed BEFORE choosing
the fixed-frequency projection. It remains in unit-modulus coefficients.
Sharp INDIVIDUAL band restrictions are separate row/column masks and are
allowed. Arbitrary coupled pair masks or shrinking smooth seminorms are
not consequences of (3)-(5).

5. SOURCE-CHECKED DENSITY AND ZERO-FREE INPUT PAY THE ENERGY.
Yashiro, arXiv1310.0765v2, printedp2 equations(1.1) and(1.2), records
the classical zeta bounds
 N_z(sigma,U)<<U^[3(1-sigma)/(2-sigma)]log^5U, 1/2<=sigma<=1,
 N_z(sigma,U)<<U^[3(1-sigma)/(3sigma-1)]log^44U, 3/4<=sigma<=1.
The first is also supported by the already checked explicit Ingham source
arXiv2507.15184v2. Use the first bound below3/4 and the second above it.
Their coefficient of1-sigma is at most12/5 on the respective intervals,
giving the WEAKER uniform consequence we need,
 N_z(sigma,U)<<U^[(12/5)(1-sigma)]log^50U, 1/2<=sigma<=1.               (6)
All counts are used with multiplicity; the harmless extra logarithmic
allowance also covers a conversion using m(rho)<<logU if needed. The
derivation uses the displayed log-power bounds themselves. Replacing them
by U^epsilon estimates would not pay the following near-one limit.

Mossinghoff-Trudgian-Yang, arXiv2212.06867v1, Theorem1.1 on printedp2,
gives the Vinogradov-Korobov zero-free region
 beta<1-1/[55.241(log gamma)^(2/3)(loglog gamma)^(1/3)], gamma>=3.
For T<gamma<=2T and sufficiently large N, this implies beta<=1-delta_N,
 delta_N=1/[55.241(log(2T))^(2/3)(loglog(2T))^(1/3)]
          >=c (logN)^-2/3 (loglogN)^-1/3.                              (7)
Only existence of a positive constant is used; no current best-constant,
computed-zero or practical onset claim is made. The band eventually has
T>=3, so there is no new low-height extension to perform here.

Put L=logN. The beta<=1/2 baseline costs O(TL) by total zero counting.
Layer cake above1/2, with the ACTUAL cap1-delta_N, gives
 E_N << TL+2L int_(1/2)^(1-delta_N) N^(2sigma-1)N_z(sigma,2T)ds.
For u=1-sigma, the relative N exponent from (6) at T=N^(2/3) is
 -2u+(2/3)*(12/5)*u=-(2/5)u.
Hence
 E_N << N^(2/3)L+N L^51 exp[-(2/5)delta_N L].                          (8)
By (7), the exponential is at most
exp[-c L^(1/3)/(logL)^(1/3)], which defeats every fixed power of L.
Combining (5) and (8) proves an all-log bound for the stationary complex
main, with explicit intermediate cost
 N^(2/3)L^2+N L^52 exp[-c L^(1/3)/(logL)^(1/3)].                       (9)
The weaker classical zero-free region alone would not give this rate.

6. RETURN TO THE ACTUAL FINITE-PERIOD SUM AND ITS PRECISE SUPPORT.
stationary_spectral_core.py already proved that replacing the actual
complex kernel sum by its stationary main costs
O(N^(31/45)log^12N); its uniform complex expansion pays this before taking
real parts. Adding that error to (9) proves (1). No formal main-term
identity is being substituted for an unproved correlation estimate.

The band's near-height strip has all-log ABSOLUTE cost by the prior
theorem. Subtracting it proves the same complex bound for the separated
part of B_T x B_T. All other prior C_high restrictions are automatically
satisfied on this band for large N, including1-Psi=1. Thus the band can be
deleted from C_high with all-log error. The remaining pointwise expression
still has the original height-sum cap, axis and near-strip exclusions, and
product multiplicities, and now excludes this specified rectangular band.
Its signed lower margin is still OPEN. No uniform family of other heights,
shrinking ratio box, arbitrary coupled mask or Goldbach coverage is claimed.

Sources checked2026-09-09:
https://arxiv.org/pdf/1310.0765v2 : printedp2 eqs(1.1),(1.2), the zeta
statements in the introduction, not the paper's later cusp-form theorem.
https://arxiv.org/pdf/2212.06867v1 : printedp2 Theorem1.1.
https://arxiv.org/pdf/2507.15184v2 : retained uniform Ingham authority.
Exponent-only database or epsilon-loss summaries were not substituted for
these log-power statements. The2016 explicit-formula correction and all
earlier source boundaries remain in force. No external action or novelty.
"""
from fractions import Fraction as F


def classical_density_coefficient(sigma):
    if type(sigma) is not F or not F(1,2)<=sigma<=1:
        raise ValueError('rational sigma in[1/2,1] required')
    return 3/(2-sigma) if sigma<=F(3,4) else 3/(3*sigma-1)


def energy_relative_exponent(u, height_power=F(2,3)):
    if type(u) is not F or not 0<=u<=F(1,2) or type(height_power) is not F or height_power<=0:
        raise ValueError('rational0<=u<=1/2 and positive height power required')
    return (F(12,5)*height_power-2)*u


def transfer_scale_powers(tail_order=4):
    if type(tail_order) is not int or tail_order<2:
        raise ValueError('integer projection-tail order>=2 required')
    return {'continuous_T':F(1,2),'stationary_T':-F(1,2),
            'combined_T':F(0),'occupancy_power':F(1),
            'discrete_tail_T':F(1-tail_order)}


def copy_occupancy_schur_probe(heights):
    """Exact toy decay kernel1/(1+t^2), not the actual Fourier projector.

    Integer-cell copy occupancy gives a universal row bound7D: same/adjacent
    cells cost3D, remaining cells cost at most2D sum_(n>=1)n^-2<=4D.
    This guards the counting mechanism, not a numerical zeta claim.
    """
    if any(type(x) is not F for x in heights):
        raise ValueError('rational toy heights required')
    cells={}
    for x in heights:
        cell=x.numerator//x.denominator
        cells[cell]=cells.get(cell,0)+1
    occupancy=max(cells.values(),default=0)
    row=max((sum((1/(1+(x-y)**2) for y in heights),F(0)) for x in heights),default=F(0))
    return {'copy_occupancy':occupancy,'max_row_sum':row}
