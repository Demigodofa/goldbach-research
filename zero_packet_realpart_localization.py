"""Actual real-part localization in the comparable T=N^(9/10) band.

Owner: Kevin's Goldbach research. Purpose: test the natural phase
expansion's coefficient cost, then use its square sum to remove actual
columns of the remaining band. The retained arithmetic energy is essential.
No RH, numerical zero experiment, or external novelty claim is made.

1. OBJECTS AND ACTUAL CONCLUSION.
Keep fixed real chi in C_c^infinity((1,2)), T=N^(9/10), L=logN,
and ACTUAL positive-height zero copies rho=beta+i*gamma. Put
 Z(a)=S_T(aN)/sqrtN
     =sum_rho c_rho*a^(beta-1/2)*exp(i*gamma*loga),
 c_rho=chi(gamma/T)*N^(beta-1)*exp(i*gamma*logN).
The completed short_prime_window_energy.py proves ||Z||_2=O(1)
on[1/4,3/4] by actual prime support, including prime powers and the
explicit-formula displacement. Its proof is not repeated here.

Let D consist of the zero copies in this band for which
 beta<=16/25 OR beta>=19/25.
For every fixed A>0, the ACTUAL finite-period kernel satisfies
 sum_(rho,sigma: rho in D OR sigma in D)
       chi(gamma/T)*chi(eta/T)*J_N(rho,sigma) = O_A(N/L^A).       (1)
This is a COMPLEX signed estimate, not a termwise absolute estimate.
Equivalently, the full smooth band equals the band with BOTH real
parts in(16/25,19/25), to an all-log small error. This concerns one
fixed smooth height band. No full-core deletion or Goldbach lower
margin follows; even the remaining band's o(N) bound is open.

2. THE EXACT NATURAL EXPANSION, AND ITS UNSUCCESSFUL L1 BUDGET.
Choose a fixed smooth zeta, equal1 on[3/10,7/10], with compact support
in(1/4,3/4), and fixed buffered intervals as in window_phase_projection.py.
The reflected field has the EXACT finite expansion
 B_Z(a)=2*zeta(a)*Z(1-a)/sqrt(a*(1-a))
       =sum_sigma c_sigma*w_beta(a)*exp[-i*T*f_sigma(a)],
 w_beta(a)=2*zeta(a)*a^(-1/2)*(1-a)^(beta-1),
 f_sigma(a)=-(eta/T)*log(1-a).                                  (2)
For eta/T in[1,2] and 0<beta<1, all these amplitudes have common
C^k bounds for every fixed k on the buffered support. In particular
 f'=t/(1-a), f''=t/(1-a)^2, f'''=2t/(1-a)^3,
 f'+a*f''=t/(1-a)^2, t=eta/T.
Thus these phases really meet the previous uniform projection theorem.
There is no residual in(2), but its coefficient mass is too large:
 N^(2/5)*L <<_chi sum_sigma |c_sigma| <<_chi N^(1/2)*L^6         (3)
when chi is not identically zero. The upper bound is the retained
Ingham estimate W_T(N)=sum_(T<eta<2T)N^(beta-1/2)<<N*L^6,
multiplied by N^-1/2 and ||chi||_infinity. For the lower bound,
choose a fixed subinterval of(1,2) on which |chi|>=c>0. Actual
Riemann-von Mangoldt counting gives >>TlogT copies there. Reflection
beta+i*eta -> 1-beta+i*eta preserves multiplicity, so at least half
of these copies have beta>=1/2, each contributing >=c*N^-1/2.
The required small l1 cost o(N^(1/44)/L^3) therefore fails for THIS
raw expansion. This is not a lower bound for the signed band and does
not rule out regrouping, other expansions, or polynomial components.

3. A GRAM ESTIMATE WHICH RETAINS COINCIDENT ZERO COPIES.
For any individual subset U define
 E_U=sum_(rho in U)|chi(gamma/T)|^2*N^(2beta-2).
Take a fixed smooth theta compactly supported in(1/4,3/4), equal1
on supp(zeta) and its reflection. The packets
 p_rho(a)=theta(a)*a^(beta-1/2)*exp(i*gamma*loga)
satisfy the uniform Gram bound
 |int p_rho(a)*conj(p_sigma(a))da|
                            <<(1+|gamma-eta|)^-2.               (4)
Indeed set v=loga. The resulting amplitude has compact fixed support
and uniformly bounded derivatives through order2, independently of
both real parts in[0,1]. Two integrations by parts prove(4) for a
nonzero large difference; the trivial bound covers differences<=1.
No beta derivative as a function of height, simplicity, or separation
between individual zeros is presumed. The same proof applies to
the reflected packets w_beta(a)*exp(i*eta*log(1-a)).

The ACTUAL multiplicity-counted number of ordinates in any unit
interval in[T,2T] is O(L), from Riemann-von Mangoldt. Sum(4) over
unit intervals about any row, including the coincident copies, to get
sup_rho sum_sigma |Gram(rho,sigma)|=O(L). Finite Schur therefore gives
 ||theta*Z_U||_2^2 << L*E_U,
 ||2*zeta*Z_U(1-a)/sqrt(a*(1-a))||_2^2 << L*E_U.                 (5)
These estimates bound restricted actual sums. They do not assume that
the O(1) arithmetic energy for Z survives arbitrary coefficient masking.

Use the arithmetic O(1) energy ONLY for the full unmasked factor.
Cauchy, valid also for a bilinear pairing without conjugation, gives
 |2 int zeta*Z(a)*Z_U(1-a)/sqrt(a*(1-a))da| << sqrt(L*E_U).       (6)
The reversed column has the same bound by reflection; zeta need not
be symmetric. With both factors restricted to U, the bound is O(L*E_U).
Inclusion-exclusion (column plus row minus intersection) thus pays
the union of the two masks by O(sqrt(L*E_U)+L*E_U).

4. DENSITY INPUTS AND THE LOW REAL-PART COLUMNS.
All density counts below include multiplicities. We reuse the checked
Ingham and Huxley log-power bounds recorded in Yashiro1310.0765v2,
printedp2 equations(1.1),(1.2), freshly rechecked2026-09-09:
 https://arxiv.org/pdf/1310.0765v2
 M(s)<=C*T^[3(1-s)/(2-s)]*L^5, 1/2<=s<=1;
 M(s)<=C*T^[3(1-s)/(3s-1)]*L^44, 3/4<=s<=1.
Here M(s) counts beta>=s in our band, and can be bounded by the
source count up to2T. Fixed factors2 cost constants only. The harmless
L^50 allowance used in the owning modules covers all copy conventions.

For U_low={beta<=16/25}, layer cake and positivity give
 E_low << N^-1*M_total
       +2L*int_(1/2)^(16/25) N^(2s-2)*M(s) ds.                 (7)
This deliberately overcounts excluded high-beta copies at the truncated
weight; it is an upper bound. The baseline is O(N^-1/10*L).
With u=1-s and t=9/10, the Ingham exponent in the integrand is
 e_I(u)=t*3u/(1+u)-2u=u*(7/10-2u)/(1+u).
For9/25<=u<=1/2, 7/10-2u<=-1/50 and u/(1+u)>=9/34, so
 e_I(u)<=-9/1700.
Consequently E_low<<N^(-9/1700)*L^51. No zero-free cap is needed
for this truncated layer. Using the exact source logs reduces51 to6.

5. HIGH REAL PARTS: PAY GM'S FIXED EPSILON AWAY FROM ONE.
For U_high={beta>=19/25}, layer cake is
 E_high << N^(-12/25)*M(19/25)
       +2L*int_(19/25)^(1-delta_N) N^(2s-2)*M(s) ds,           (8)
with empty integrals interpreted as zero for large N. The common
zero-free cap is delta_N>>L^(-2/3)*(logL)^(-1/3), supplied by the
retained Vinogradov--Korobov source2212.06867v1, Theorem1.1 p2:
 https://arxiv.org/pdf/2212.06867v1 . Its region applies uniformly
to actual heights in[T,2T]; we have not assumed RH.

On19/25<=s<=4/5 use Guth--Maynard2405.20552v2, Theorem1.2 p2:
 https://arxiv.org/pdf/2405.20552v2
 M(s)<=T^[15(1-s)/(3+5s)+o(1)].                                 (9)
The actual exponent with u=1-s is
 e_G(u)=(9/10)*15u/(8-5u)-2u
       =u*(10u-5/2)/(8-5u), 1/5<=u<=6/25.
Its derivative is108/(8-5u)^2-2>0 on this interval; hence
 e_G(u)<=e_G(6/25)=-3/850.

We do not read the source o(1) as a log-power error or as already
uniform in s. Choose a FIXED sigma grid on[19/25,4/5] of mesh
1/10000 and source epsilon1/10000 at its401 points. Above the maximum
of their finitely many thresholds, round each s down to its grid point.
Monotonicity of M and |d[15u/(8-5u)]/du|<3 cost at most3/10000
in the T exponent. The total N-exponent loss is9/25000, and
 -3/850+9/25000 < -1/400.                                       (10)
The boundary term in(8) obeys the same power bound. Constants depend
on this fixed grid, not on N. This use does not extend toward s=1.

For4/5<=s<=1-delta_N, the original LOG-POWER Huxley bound instead
gives, for delta_N<=u<=1/5,
 e_H(u)=(9/10)*3u/(2-3u)-2u <=-u/14.
Indeed2-3u>=7/5 and (27/10)/(7/5)-2=-1/14. Thus(8) yields
 E_high << L^51*[N^-1/400
        +exp(-c*L^(1/3)/(logL)^(1/3))].                         (11)
Every fixed negative log power bounds(11) eventually. No source
epsilon has been applied where it would overwhelm the zero-free saving.
Combining(7),(11), the same bound holds for E_D after changing constants.

6. TRANSFER TO THE ACTUAL BAND AND THE PRECISE REMAINDER.
The completed exact beta identity gives, for any product of individual
zero masks, the central integral used in(6), multiplied by N.
Its beta endpoint error and actual J_N-minus-beta error were already
summed ABSOLUTELY over the full chi-weighted comparable band:
 O_chi(N^-7/10*L^13+N^9/10*L^12).
These errors therefore hold for each of the present subsets and their
union; there is no new coupled-mask operator assertion. Equations(5)-(6)
and inclusion-exclusion prove the more explicit bound
 |sum_(rho in D OR sigma in D) chi*chi*J_N|
 << N*[sqrt(L*E_D)+L*E_D]+N^9/10*L^12+N^-7/10*L^13.             (12)
Equations(7),(11) make every term all-log small on the N scale, proving(1).
The remaining square itself stays O(N) by subtracting(1) from the
retained full-band O(N) theorem. No smaller bound is proved for it.

Source for the retained counting law: Brent--Platt--Trudgian2021,
Mathematics of Computation90, printedp2926 equations(5)-(7), previously
checked and recorded in spectral_count_resonance_model.py:
 https://maths-people.anu.edu.au/brent/pd/rpb276-MC-preprint.pdf
A fresh web open returned Internal Error; no new access is claimed.
The classic bounds, GM theorem and VK PDF were accessible this pursuit.

The possible remaining real-part interval is a bound on where THIS
estimate can fail, not evidence that any such zeros exist. The narrow
unbuffered sign transitions of these selected density exponents occur
at beta=13/20 and3/4; no endpoint theorem is asserted. Prior square,
unequal-height, near-strip and polynomial results remain valid. Since
4T=o(N), the original smooth endpoint weight equals1 here eventually;
this does not upgrade a single chi-weighted statement to the full core.
"""
from fractions import Fraction as F


def normalized_density_exponent(u, source):
    if type(u) is not F:
        raise ValueError('exact rational real-part complement required')
    if source == 'ingham' and 0 <= u <= F(1,2):
        density = 3*u/(1+u)
    elif source == 'gm' and F(1,5) <= u <= F(6,25):
        density = 15*u/(8-5*u)
    elif source == 'huxley' and 0 <= u <= F(1,5):
        density = 3*u/(2-3*u)
    else:
        raise ValueError('unsupported source or real-part interval')
    return F(9,10)*density-2*u


def gm_grid_budget():
    return {'raw_max':-F(3,850), 'source_epsilon':F(1,10000),
            'grid_mesh':F(1,10000), 'derivative_bound':F(3),
            'charged_max':-F(3,850)+F(9,25000),
            'claimed_max':-F(1,400)}


def reflected_phase_derivatives(a, t):
    if (type(a) is not F or type(t) is not F
            or not F(1,4) <= a <= F(3,4) or not 1 <= t <= 2):
        raise ValueError('exact central coordinate and t in[1,2] required')
    return {'first':t/(1-a), 'second':t/(1-a)**2,
            'third':2*t/(1-a)**3, 'dilation':t/(1-a)**2}


def deleted_realpart(beta):
    if type(beta) is not F or not 0 < beta < 1:
        raise ValueError('actual open-strip rational real part required')
    return beta <= F(16,25) or beta >= F(19,25)
