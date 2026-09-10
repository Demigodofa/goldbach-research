"""Pay the middle and low weighted masks in the actual detector transfer.

Owner: Kevin's Goldbach research. Purpose: remove the amplification gap
for most of the previously deleted zeros before using the prime-product
representation. The remaining H-weighted HIGH exterior and the signed
prime-correlation estimate stay open. This is not a Goldbach proof.

1. SETS, NORMALIZATION AND ACTUAL CONCLUSIONS.
Keep T=N^(9/10), L=logN, fixed real chi in C_c^infinity((1,2)),
and a=16/25,b=19/25. All sums are over ACTUAL positive-height
zero copies, with w_rho=|chi(gamma/T)|^2*N^(2beta-2).
The common H_N=sum_badM D_M and A_N=sum_goodM D_M use the
exact allowed dyadic detector blocks from the retained modules. A good
M has some integer1<=k<=100 with M^k in[N41/50,N49/50].
The four open bad exponent gaps are
 (49/300,41/250), (49/250,41/200),
 (49/200,41/150), (49/150,41/100).                             (1)

Let G be middle-strip copies detected at ANY good length. Let II be ALL
middle-strip Type II copies, including overlap with G, as defined by
|I_T(rho)|>=1/3. Let D_low={beta<=a} and D_high={beta>=b}.
The original survivor set is R=full band minus(D_low union D_high
union G union II). This partition and the ACTUAL detector identity
 1+A_N(rho)+H_N(rho)=I_T(rho)+O(T^-1/2)                      (2)
are unchanged. All source Gamma corrections and dyadic endpoint errors
recorded in signed_zero_detector.py remain in force.

For some fixed C we prove the WEIGHTED coefficient energies
 E_(II,H)=sum_(rho in II)w_rho*|H_N(rho)|^2
                              <<N^(-1/125)*L^C,
 E_(G union II,H)              <<N^(-4/625)*L^C,
 E_(D_low,H)                  <<N^(-11/3750)*L^72.           (3)
Thus for U=D_low union G union II,
 E_(U,H)<<N^(-11/3750)*L^C.                                  (4)
Unlike the earlier unweighted deletions, these bounds include the FULL
H_N value on the selected zeros, not just compatible multiplier pieces.

With the opposite coordinate FULL and unweighted, the actual finite-period
kernel satisfies
 |sum_(rho in U,sigma)chi(gamma/T)chi(eta/T)H_N(rho)J_N(rho,sigma)|
 <<N^(7489/7500)*L^C+N^(3557/3750)*L^C+N^(-3193/3750)*L^C.  (5)
Every term is all-log small on the N scale. The reversed coordinate is
also bounded. We do not infer a nonindicator two-mask union identity.

2. A MOMENT AT ITS OWN LENGTH, INCLUDING THE POSITIVE COST ABOVE N.
For a bad multiplier length H=N^h and an integer s>=1, D_H^s
has support P<n<=2^s P with P=H^s and coefficients bounded by
tau_(2s). The previously proved variable-beta Sobolev/mean-square argument
gives, for a fixed real-part interval and sigma at its lower edge,
 sum_(sigma<=beta<=upper, T<=gamma<=2T)|D_H(rho)|^(2s)
                    <<(T+P)*P^(1-2sigma)*L^(4s^2+5).         (6)
The source of each log, local zero-copy occupancy and real-part variation
is retained in detector_power_length_filter.py. This coefficient proof
also works on[0,a]: n^-2sigma and its log derivatives have the same
uniform bounds on this fixed interval. No density theorem at sigma=0
is being asserted. Counts are replaced by actual polynomial moments.

For middle-strip calculations partition[a,b] into360 fixed bins of
width Delta=1/3000. In each bin sigma<=beta<sigma+Delta, put
u=1-sigma. Bound N^(2beta-2) by N^(2(sigma+Delta)-2) BEFORE
using(6); copies above the bin can overcount its polynomial moment.
The resulting bin moment has exponent
 v(sh,u)+2Delta,
 v(p,u)=max(9/10,p)-p+2u*(p-1).                              (7)
The T term governs p<=9/10; the LENGTH term governs p>=9/10.
In particular v can be positive for a polynomial longer than N. We
retain that positive cost and compensate by the rarity of the chosen set.

3. ALL MIDDLE-STRIP TYPE II COPIES, USING THEIR ACTUAL COUNT.
The retained corrected source count is
 R_II(sigma,T)<<T^(2*(1-sigma))*L^C0, sigma in[a,b],           (8)
including copies and overlapping source types. It comes from the
unconditional Maynard--Pratt Appendix C proof with the NEGATIVE Gamma
argument repaired, not Hypothesis F. The earlier source verification
and contour correction remain in zero_detector_band_reduction.py.
Consequently the Type II coefficient energy in a beta bin is bounded
by N^(-u/5+2Delta)*L^C0.

Apply Holder in the actual positive measure w_rho on that Type II bin:
 sum w_rho*|D_H|^2
 <=(sum w_rho)^(1-1/s)*(sum w_rho*|D_H|^(2s))^(1/s).          (9)
The second factor is bounded by the FULL bin moment(6), not by an
assumed arithmetic norm of the Type II subset. Choose the integer s
according to the actual h:
 gap1: s=6; gap2: s=5; gap3: s=4;
 gap4 with h<=19/50: s=3; gap4 with h>=19/50: s=2.            (10)
Either choice works at h=19/50. For s>=3 all sh>49/50>9/10;
for s=2 on the last piece, 2h<41/50<9/10. Thus the unbinned
Holder exponents are, respectively,
 2u*[h-1/10-9/(10s)],
 9/20-h+u*(2h-11/10).                                       (11)
For s>=3 the bracket is negative and increases with h, so its worst
case uses the upper h endpoint and u=6/25. The successive worst
values for s=6,5,4,3 are
 -129/3125, -9/250, -31/1250, -6/625.
For s=2 both the h and u derivatives are negative on the stated
domain, so h=19/50,u=6/25 gives the worst value -29/2500.
All five cases are therefore at most -6/625 BEFORE the bin cost.
Adding 2Delta=1/1500 gives -67/7500<-1/125.                 (12)

The Holder log exponent is at most max(C0,149); the largest pure
moment has s=6 and4s^2+5=149. Summing360 bins costs a constant,
not a growing number of bins. Cauchy over O(L) bad H and then their
sum adds only two log powers. For example C=max(C0,149)+10 is
sufficient for the first bound in(3). This covers ALL middle Type II
zeros, whether or not any good detector also detects them.

4. THE SAVED SIGNED IDENTITY NOW PAYS EVERY REMAINING GOOD-DETECTED ZERO.
Let X=G minus II. Its unweighted energy obeys
 E_X<=E_G<<N^(-eta)*L^40220, eta=4/625.                       (13)
For EACH good M, choose one licensed integer k<=100. Applying the
pre-threshold mean-square and positive layer-cake proof to D_M^k gives
 K_M=sum_(all middle copies)w_rho*|D_M(rho)|^(2k)
                         <<N^(-eta)*L^(4k^2+6).              (14)
This is a moment of all middle copies. It does not require that X be
detected at this particular M. The detector threshold is NOT inserted
in(14); it is needed only in the earlier proof of(13).

Holder on X gives, for k>1,
 sum_X w_rho*|D_M|^2<=E_X^(1-1/k)*K_M^(1/k)
                              <<N^(-eta)*L^40220.            (15)
For k=1 use(14) directly, and for empty X the assertion is immediate.
Sum the O(L) good M, using pointwise Cauchy on A_N=sum_good D_M:
 sum_X w_rho*|A_N(rho)|^2<<N^(-eta)*L^40222.                 (16)
Since X excludes II, |I_T(rho)|<1/3. Equation(2) implies
 H_N=-A_N-1+I_T+O(T^-1/2),
 |H_N|^2<=2|A_N|^2+O(1),                                   (17)
uniformly on X for sufficiently large N. The constant term in(17)
is paid by E_X, not discarded. Combining(13),(16)-(17) pays X with
the same N^-eta saving. Add the first bound of(3) on II, which has
the stronger exponent1/125. Nonnegative energies handle the overlap
with G; equivalently X and II are a disjoint partition of G union II.
This proves the second bound of(3). The identity alone would not prove
it: the full-good moments and Type II weighted estimate are essential.

5. THE ENTIRE LOW EXTERIOR, WITH THE BETA=0 BASELINE RETAINED.
For the four bad gaps choose pure powers k=4,4,3,2 respectively.
Then their actual product exponents satisfy
 49/75<=p=k*h<=41/50<9/10.                                  (18)
Use(6) on[0,a]. Positive layer cake is based on the exact identity
 N^(2beta-2)=N^-2+2L*int_0^beta N^(2sigma-2)dsigma.
It supplies the required baseline N^-2 times the total polynomial
moment, as well as the integral; no mass at beta=0 is assumed.
The normalized moment exponent is
 e(beta,p)=9/10+p*(1-2beta)+2beta-2.
Since p<1 it increases with beta. At beta=a=16/25,
 e(a,p)=9/50-(7/25)*p<=-11/3750,                            (19)
with worst case p=49/75. Thus
 sum_(D_low)w_rho*|D_H(rho)|^(2k)
                        <<N^(-11/3750)*L^(4k^2+6).
The retained Ingham low-set estimate gives E_low<<N^-9/1700 L51,
a stronger power. Holder with that measure and the last moment proves
 sum_(D_low)w_rho*|D_H|^2<<N^(-11/3750)*L70.
Finally sum bad H with Cauchy; its two extra logs prove the third
bound in(3). This uses actual real parts throughout[0,a], not their
replacement by1/2. No RH or simplicity assumption is involved.

6. UNION, WEIGHTED KERNEL COSTS AND THE PRECISE REMAINING BRIDGE.
For U=D_low union G union II, its weighted energy is bounded by the
sum in(3), proving(4). Apply the arbitrary-coefficient Gram estimate
to c_rho*H_N(rho)*1_U, c_rho=chi*N^(beta-1)*exp(i*gamma*logN).
Its normalized field norm is O(N^-11/7500 times fixed logs).
Use the arithmetic O(1) norm only for the full opposite field.
This yields the central beta exponent1-11/7500=7489/7500.

The retained NEW-weight transfer in mixed_detector_weighted_mask.py
works for any coefficient energy N^-epsilon times fixed logs:
 sum|c_rho*weight(rho)|<<N^(9/20-epsilon/2)*L^C,
 sum|c_sigma|<<N^(2/5)*L6,
 |J_N-B_N|<<N^(beta+beta'-1)/T.
Therefore the absolute finite-period replacement exponent is
 19/20-epsilon/2, and the three-IBP beta endpoint exponent is
 -17/20-epsilon/2, including the small-real-part denominator log.
Taking epsilon=11/3750 gives(5). For G union II alone the three
exponents are623/625,2367/2500,-2133/2500; for II alone they are
249/250,473/500,-427/500. No unweighted error is silently reused.

The exact normalized field decomposition now has only one unpaid
removed component. With Z_(H,A)(v)=sum_(rho in A)c_rho H_N(rho)
v^(beta-1/2+i*gamma), and the actual prime-product window P_h from
detector_prime_product_transfer.py,
 Z_(H,R)=-P_h(vN)/sqrtN-Z_(H,D_high)
                         +O_L2(N^-11/7500*L^C),              (20)
on the fixed central interval with the retained smooth cutoff theta.
Indeed R,D_high,U partition the full band, (4) pays U in that norm,
and the full-field prime-product transfer error N^-59/200 L7 is
smaller. The high term in(20) has NOT been proved negligible.
The sufficient signed prime-correlation estimate remains open even
if that next weighted bridge is established; no inversion or pair-sign
conclusion follows automatically from the common detector disk.

Retained component from the initial test: for good detecting exponents
m in[.44,.45], the same powers(10) and D_M^2 detector-bin energy
have worst unbinned exponents -1223/37500,-173/6250,-17/1000,
-1/375,-4/625. The bin cost leaves at least1/500 saving, with log
exponent at most137/3 before sums, hence whole-mask energy N^-1/500
L50. This independently reviewed narrower component is superseded here
by the stronger full-G argument(13)-(17), but remains a valid way of
trading a specific detector's rarity against longer pure moments.

Only new-to-this-task claims are made. The prior aggregate-H^2 shortcut
remains retracted; each polynomial above keeps its actual support and
the correct T-versus-length cost. No new numerical zero or Goldbach
experiment, external novelty claim, manuscript or publication is involved.
"""
from fractions import Fraction as F

from mixed_detector_weighted_mask import BAD_GAPS


def multiplier_power(h, low_exterior=False):
    if type(h) is not F:
        raise ValueError('exact bad-length exponent required')
    gap=next((j for j,(left,right) in enumerate(BAD_GAPS) if left < h < right),None)
    if gap is None:
        raise ValueError('length must be inside an open bad gap')
    if low_exterior:
        return (4,4,3,2)[gap]
    if gap < 3:
        return (6,5,4)[gap]
    return 3 if h <= F(19,50) else 2


def moment_power(u,p):
    if (type(u) is not F or type(p) is not F
            or not 0 <= u <= 1 or p <= 0):
        raise ValueError('exact complementary real part and positive length required')
    return max(F(9,10),p)-p+2*u*(p-1)


def type_ii_holder_power(u,h):
    if type(u) is not F or not F(6,25) <= u <= F(9,25):
        raise ValueError('exact middle-strip complementary real part required')
    s=multiplier_power(h)
    return -F(s-1,s)*u/5+moment_power(u,s*h)/s


def large_detector_holder_power(m,u,h):
    if (type(m) is not F or not F(11,25) <= m <= F(9,20)
            or type(u) is not F or not F(6,25) <= u <= F(9,25)):
        raise ValueError('exact retained detector and middle real part required')
    s=multiplier_power(h)
    return F(s-1,s)*moment_power(u,2*m)+moment_power(u,s*h)/s


def beta_bins():
    a,step=F(16,25),F(1,3000)
    return tuple((a+j*step,a+(j+1)*step) for j in range(360))


def weighted_kernel_powers(energy_saving):
    if type(energy_saving) is not F or energy_saving <= 0:
        raise ValueError('positive exact coefficient-energy saving required')
    return {'central':1-energy_saving/2,
            'finite_period':F(19,20)-energy_saving/2,
            'endpoint':-F(17,20)-energy_saving/2}
