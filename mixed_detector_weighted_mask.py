"""Pay compatible detector multipliers on actually detected zero copies.

Owner: Kevin's Goldbach research. Purpose: close part of the weighted-mask
gap in the full prime-product transfer, using actual dyadic product lengths.
The covered contribution is bounded for the actual finite-period kernel;
incompatible components and the full signed Goldbach margin remain open.

1. A MIXED MOMENT WITH THE ACTUAL LOWER AND UPPER PRODUCT SCALE.
Keep N,T=N^(9/10),L=logN,a=16/25,b=19/25 and the exact D_M
from zero_detector_band_reduction.py. All sums count ACTUAL positive-height
zero copies. Write
 w_rho=|chi(gamma/T)|^2*N^(2beta-2), delta=1/(3logT).
A good length M has N41/50<=M^k<=N49/50 for some1<=k<=100.
Let X_M be the middle-strip copies a<beta<b with |D_M(rho)|>=delta.
The retained result gives, for good M,
 E_M=sum_(rho in X_M)w_rho<<N^(-4/625)*L^40220.                (1)

Let H be a bad multiplier length. Call (M,H) COMPATIBLE if some
integers r,s>=1, r+s<=100 satisfy
 P=M^r*H^s in[N^(41/50),N^(49/50)].                           (2)
For k=r+s, the polynomial F=D_M^r*D_H^s has support
 P<n<=2^k*P, with coefficients bounded by tau_(2k)(n).         (3)
This follows by the unrestricted positive Dirichlet convolution bound;
the actual dyadic restrictions only decrease that majorant. In particular
the product scale in(3) is P, not the maximal length of an aggregate H_N.

The prior coefficient-square, unit-Sobolev and variable-beta proof in
detector_power_length_filter.py applies to(3) without change. For every
sigma in[a,b], including actual local copy occupancy, it gives
 sum_(sigma<=beta<=b, T<=gamma<=2T)|F(rho)|^2
       <<(T+P)*P^(1-2sigma)*L^(4k^2+5).                      (4)
To insert N^(2beta-2), use positive layer cake for this weighted counting
measure, including the boundary at a. The numbers |F(rho)|^2 are fixed
while sigma varies; their dependence on the actual beta is already paid
by the fundamental-theorem-of-calculus argument behind(4). Bounded chi
causes no extra power. For p=logP/logN, the two normalized exponents are
 9/10+p*(1-2beta)+2beta-2 <=-4/625,
 2*(1-beta)*(p-1)         <=-6/625,
on beta in[a,b], p in[41/50,49/50]. Hence
 K_F=sum_(middle copies)w_rho*|F(rho)|^2
                              <<N^(-4/625)*L^(4k^2+6).        (5)
No detector threshold has yet been used in(5). All constants are uniform
over the finite r+s<=100 choices. The large fixed logs give no finite onset.

2. THE DETECTOR THRESHOLD AND WEIGHTED HOLDER PAY A SECOND MOMENT.
On X_M, |D_M|>=delta, so(5) implies
 sum_(rho in X_M)w_rho*|D_H(rho)|^(2s)
                 <=delta^(-2r)*K_F
                 <<N^(-4/625)*L^(4k^2+6+2r).                 (6)
The threshold loss is2r, not2k: D_H is the multiplier, not an assumed
large detector on these copies. For s>1, Holder in the positive measure
w_rho gives
 sum_(X_M)w_rho*|D_H|^2
 <=E_M^(1-1/s)*[sum_(X_M)w_rho*|D_H|^(2s)]^(1/s).            (7)
For s=1, use(6) directly; for E_M=0 the left side is zero.
Equations(1),(6)-(7) prove
 sum_(X_M)w_rho*|D_H(rho)|^2<<N^(-4/625)*L^40220              (8)
for EVERY compatible pair. The power saving is unchanged under Holder.
Indeed4k^2+6+2r<=40204 for k<=100,r<=k-1, and the log exponent
in(7) is a convex combination of this number and40220.

3. COVER A MULTIPLIER IF ANY GOOD DETECTING LENGTH CAN PAY IT.
Let G be the middle-strip copies detected at ANY good M. For each bad H,
assign a copy rho to Y_(M,H) if M is its LEAST good detecting length
compatible with H. If none exists, it has no assignment for this H.
For fixed H, the Y_(M,H) are disjoint in M and are subsets of X_M.
Different H may share copies. Define the actual complex coefficient
 C_cov(rho)=sum_(bad H with such an assignment)D_H(rho),
with zero value outside G. This includes a component when ANY good
detector pays it, even if the least good detector overall does not.
It depends only on rho, never on the other zero sigma in the pair kernel.

There are O(L) bad H and O(L) good M. Cauchy over H, then(8), gives
 E_cov=sum_rho w_rho*|C_cov(rho)|^2
 <=O(L)*sum_H sum_M sum_(rho in Y_(M,H))w_rho*|D_H(rho)|^2
                         <<N^(-4/625)*L^40230.               (9)
Three extra logs suffice for the displayed crude counting;40230 leaves
room without optimizing them. Assignment avoids duplicate coefficients,
while overcounting positive energies in the bound is harmless.

For rho in G the exact remainder is
 H_N(rho)-C_cov(rho)
   =sum_(bad H incompatible with EVERY good detecting M of rho)D_H(rho).
No small bound for that remainder is asserted. Nor are the Type II and
exterior-real-part weighted masks paid by this result.

4. TRANSFER THE COVERED COEFFICIENT TO THE ACTUAL FINITE-PERIOD KERNEL.
Put c_rho=chi(gamma/T)*N^(beta-1)*exp(i*gamma*logN), and
 Z_cov(v)=sum_rho c_rho*C_cov(rho)*v^(beta-1/2+i*gamma).
The retained arbitrary-coefficient Gram estimate gives
 ||theta*Z_cov||_2^2<<L*E_cov,
hence ||theta*Z_cov||_2<<N^(-2/625)*L^C. The opposite full field
Z=S_T(vN)/sqrtN has arithmetic norm O(1). Therefore the central
Euler-beta bilinear integral costs O(N^(623/625)*L^C).
It has NO conjugation. No arithmetic norm is assigned to a masked field.

Unlike merely inheriting an unweighted error, pay the NEW weighted
finite-period and endpoint costs explicitly. Comparable heights give
 |J_N(rho,sigma)-B_N(rho,sigma)|
                       <<N^(beta+beta'-1)/T,                 (10)
uniformly for 0<beta,beta'<1: the retained finite-interval stationary
expansion has relative error T^-1/2, its amplitude is
O(N^(beta+beta'-1)*T^-1/2), and the beta quotient has relative
Stirling error O(T^-1). This is the actual uniform proof in
stationary_spectral_core.py and short_prime_window_energy.py.
Since T=o(N), its condition piN>=4(gamma+eta) holds eventually.

There are O(TL) copies. Cauchy with(9), and the improved Ingham
first moment in detector_prime_product_transfer.py at y=N, give
 sum_rho |c_rho*C_cov(rho)| <=sqrt(O(TL)*E_cov)
                              <<N^(9/20-2/625)*L^C,
 sum_sigma |c_sigma|=O(W_T(N)/sqrtN)<<N^(2/5)*L^6.             (11)
That first-moment proof applies at y=N since N<T^(4/3).
Multiply(10) by the actual complex coefficient and sum ABSOLUTELY.
The result is at most N/T times the product in(11), with exponent
 1/10+9/20-2/625+2/5=2367/2500<1.                            (12)
The endpoint part of the beta integral, after three integrations by parts,
is bounded by N*T^-3*L times the same product. Its exponent is
 1-27/10+9/20-2/625+2/5=-2133/2500.                           (13)
The factor L pays 1/beta+1/beta' using the retained zero-free region
and reflection; the weighted coordinate itself is in the fixed middle
strip. Complex coefficients are constant in the integration variable.

Consequently, for some fixed C, the ACTUAL one-coordinate weighted sum
 |sum_(rho,sigma)chi(gamma/T)*chi(eta/T)*C_cov(rho)*J_N(rho,sigma)|
 <<N^(623/625)*L^C+N^(2367/2500)*L^C+N^(-2133/2500)*L^C.     (14)
All three terms are O_A(N/L^A) for every fixed A. The reversed
coordinate obeys the same bound. This does not claim a two-mask union
identity for nonindicator coefficients or a saving for the full H_N weight.

5. EXACT COVERAGE GEOMETRY, INCLUDING A ROBUST UNCOVERED REGION.
For ANY positive m=logM/logN,h=logH/logN, condition(2) is exactly
 membership in union_(r,s>=1,r+s<=100)
             { (m,h):41/50<=r*m+s*h<=49/50 }.                (15)
This finite union of closed strips is an exact sufficient criterion,
with the actual allowed/good/bad domains intersected afterward. The
helper below enumerates its witnesses by exact integer rounding.

A complete useful slice is m in[11/25,9/20]=[.44,.45], all good
via k=2 and inside the actual allowed length range. For h in the four
bad gaps, r>=2 would give r*m+s*h>.88+49/300>.98. Thus r=1.
Also s>=4 gives m+s*h>.44+4*(49/300)>.98. Only s=1,2,3 remain:
 - h in(49/300,41/250): ALL covered by(r,s)=(1,3).
 - h in(49/250,41/200): ALL covered by(1,2).
 - h in(49/200,41/150): covered IFF h<=(49/50-m)/2, by(1,2).
 - h in(49/150,41/100): covered IFF h>=41/50-m, by(1,1).      (16)
Both product-window equality cases are INCLUDED. The original bad-gap
endpoints are excluded because they belong to the good-length set.
For these M, only the two open residual pieces
 ((49/50-m)/2,41/150), (49/150,41/50-m)                        (17)
are unaccounted for by THIS detecting length. A different good detector
on the same zero may cover them; definition(9) uses every such detector.

In particular the closed rectangle
 .44<=m<=.45, .34<=h<=.36                                    (18)
is wholly uncovered by(15). The base r=s=1 mixed sum m+h is at most
.81<.82, while any larger r or s gives at least .44+2*.34=1.12>.98.
This is a length-criterion limitation, not evidence that actual zeros
populate the rectangle, a lower bound for their weighted sum, or a
barrier to every moment/detector method. No fractional powers are used.

The previous aggregate-fourth-moment retraction remains in force. This
result repairs the product-scale handling only on the explicitly covered
components. All other masks, the surviving signed prime correlation and
universal Goldbach coverage remain open. New-to-this-task only; no new
numerical zero experiment or finite Goldbach range is involved.
"""
from fractions import Fraction as F
from math import ceil, floor

from detector_power_length_filter import eligible_powers


BAD_GAPS=((F(49,300),F(41,250)),(F(49,250),F(41,200)),
          (F(49,200),F(41,150)),(F(49,150),F(41,100)))


def mixed_witnesses(detector_exponent, multiplier_exponent):
    """Exact strip membership; caller owns actual dyadic/detector evidence."""
    m,h=detector_exponent,multiplier_exponent
    if any(type(x) is not F or x <= 0 for x in (m,h)):
        raise ValueError('positive exact length exponents required')
    out=[]
    for r in range(1,100):
        low=max(1,ceil((F(41,50)-r*m)/h))
        high=min(100-r,floor((F(49,50)-r*m)/h))
        out.extend((r,s) for s in range(low,high+1))
    return tuple(out)


def largest_good_slice_witness(m,h):
    if type(m) is not F or not F(11,25) <= m <= F(9,20):
        raise ValueError('exact detector exponent in[11/25,9/20] required')
    if type(h) is not F:
        raise ValueError('exact bad multiplier exponent required')
    gap=next((j for j,(left,right) in enumerate(BAD_GAPS) if left < h < right),None)
    if gap is None:
        raise ValueError('multiplier must be strictly inside a bad gap')
    if gap == 0:
        return (1,3)
    if gap == 1:
        return (1,2)
    if gap == 2:
        return (1,2) if h <= (F(49,50)-m)/2 else None
    return (1,1) if h >= F(41,50)-m else None


def least_covering_detector(detected_exponents, multiplier_exponent):
    """Finite assignment guard; inputs assert detection, not actual zero data."""
    if any(type(m) is not F or m <= 0 for m in detected_exponents):
        raise ValueError('positive exact detected exponents required')
    if type(multiplier_exponent) is not F or multiplier_exponent <= 0:
        raise ValueError('positive exact multiplier exponent required')
    return next((m for m in sorted(set(detected_exponents))
                 if eligible_powers(m) and mixed_witnesses(m,multiplier_exponent)),None)


def mixed_log_budget(r,s):
    if any(type(v) is not int or v < 1 for v in (r,s)) or r+s > 100:
        raise ValueError('positive integer powers with total<=100 required')
    moment=4*(r+s)**2+6
    return {'moment':moment, 'threshold':2*r,
            'holder':F(s-1,s)*40220+F(moment+2*r,s)}


def covered_kernel_exponents():
    eta=F(4,625)
    cov_l1=F(9,20)-eta/2
    full_l1=F(2,5)
    return {'energy':-eta, 'norm':-eta/2, 'central':1-eta/2,
            'finite_period':1-F(9,10)+cov_l1+full_l1,
            'endpoint':1-F(27,10)+cov_l1+full_l1}
