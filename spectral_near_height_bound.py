"""Delete a growing near-height strip of the actual spectral pair sum.

Owner: Kevin's Goldbach research. Purpose: determine whether interactions
between nearby zero ordinates can carry the remaining main-scale obstacle.
They cannot, in the precise asymptotic strip proved here. Widely separated
heights retain the OPEN signed correlation. No RH, simple-zero assumption,
prime-pair coverage, numerical zero certificate or novelty claim is made.

1. STATEMENT AND THE UNBALANCED KERNEL COST.
Use the finite-period J_N(rho,sigma) in smooth_endpoint_cancellation.py,
with all positive-height zeros rho=beta+i*gamma, sigma=beta'+i*eta.
All sums below count copies of zeros, so a pair of locations has product
multiplicity m(rho)m(sigma), including m(rho)^2 at an identical location.
Fix K>0 and let L=logN. For the classical zero-free constant c>0 already
retained in spectral_diagonal_bound.py set alpha=min(1,sqrt c). Define
 W_N=exp[(alpha/30)*sqrtL].
We prove for every fixed A>0,
 sum_(0<gamma,eta<=KN; |gamma-eta|<=W_N) |J_N(rho,sigma)|
                                    <<_(A,K) N/L^A.                  (1)
The same holds for ANY weights of modulus<=1 on this region. In particular,
every fixed width log^B N is eventually covered, for each fixed B>0.
The constant and onset are not supplied numerically. W_N grows more slowly
than every fixed positive power of N; no width N^epsilon is asserted.

The rescaled partial-integral proof in spectral_diagonal_bound.py depends
only on h=gamma+eta and b=beta+beta' in(0,2), not on equality of the two
zeros. For h>=8 it gives, uniformly for EVERY terminal U>=0,
 |int_0^U (1+u^2)^(-b/2) exp[-h arctan(1/u)]
       *exp{i[u-(h/2)log(1+u^2)-b arctan u]}du| << h^(1/2-b).
Thus the exact N^(b-1) rescaling and uniform Stirling give
 |J_N(rho,sigma)|
 << N^(beta+beta'-1)/sqrt h
       *(gamma/h)^(beta-1/2)*(eta/h)^(beta'-1/2).                       (2)
For 0<r<1 and 0<beta<1, r^(beta-1/2)<=r^-1/2. Hence the factor after
N^(beta+beta'-1) is at most sqrt(h/(gamma*eta)), which is at most
sqrt(2/min(gamma,eta)). Actual positive ordinates have a fixed positive
lower bound: zeros are discrete, there are finitely many in a compact
height interval and no real zero in the nontrivial strip. No numerical
first-zero assertion is needed. The finitely many pairs with h<8 are
handled by the same bounded-initial-interval/nonstationary-tail argument
as in the diagonal proof. Consequently a uniform actual-zero estimate is
 |J_N(rho,sigma)|
       << N^(beta+beta'-1)/sqrt(1+min(gamma,eta)).                      (3)
This explicitly pays very unequal heights. The stronger comparable-height
bound cannot be silently used when one height is small.

2. PAY LOCAL COUNTS AND SYMMETRIZE THE REAL-PART WEIGHTS.
For 0<=W<=KN, Riemann-von Mangoldt gives the multiplicity-counted bound
 M(gamma,W)=#{sigma:0<eta<=KN, |eta-gamma|<=W}
                                         <<_K (W+1)L.                 (4)
Use the cumulative count difference on an interval enlarged by1 at each
endpoint to include zeros exactly on the boundary. The main-term difference
costs O((W+1)log(N+3)); the two count remainders cost O(log(N+3)). The
compact interval near height0 is absorbed. This does not assume simple
zeros or a pair-correlation law.

Put a_rho=N^(2beta-1), and define a SINGLE multiplicity-counted moment
 F_K(N)=sum_(0<gamma<=KN) a_rho/sqrt(1+gamma).
AM-GM gives N^(beta+beta'-1)<= (a_rho+a_sigma)/2. In the width-W strip,
 (1+gamma)/(1+min(gamma,eta)) <=1+W,
and the same inequality holds with eta. Since the full strip is symmetric,
summing (3), then the two AM-GM terms, yields
 S_K(N,W) << sqrt(1+W) sum_rho a_rho/sqrt(1+gamma)*M(gamma,W)
           <<_K (W+1)^(3/2) L F_K(N).                                  (5)
Each sum is over copies. Equal locations and different real parts at the
same ordinate are both included; no multiplicity square has been dropped.
Bounded weights and the retained height-SUM restriction are applied only
AFTER bounding this enclosing symmetric strip absolutely.

3. SPEND THE ALREADY CHECKED DENSITY SAVING, IN THE RIGHT DIRECTION.
Sections3-4 of spectral_diagonal_bound.py bound F_K DIRECTLY by their
zero-free split and layer-cake density calculation, omitting the additional
multiplicity logarithm needed there for m(rho)^2. We do NOT infer an upper
bound for F_K from an upper bound for the diagonal kernel sum: that would
reverse a one-sided inequality. The displayed calculation gives, safely,
 F_K(N) <<_K N L^8 exp[-(alpha/10)*sqrtL]                               (6)
for sufficiently large N. Indeed the low-height exponent is alpha/2 and
the slowest high-height exponential is5alpha/22; the remaining fixed powers
of N decay faster. Alpha/10 is a conservative common choice.

The inputs are the retained classical zero-free region and the UNIFORM
Ingham density estimate N_z(sigma,T)<<T^[3(1-sigma)/(2-sigma)]log^5T.
arXiv2507.15184v2 Corollary1/Table1 support this weaker bound with finite
constants on intervals covering[1/2,1]. No replacement of beta by1/2.

For W=W_N, eventually W<=KN and W+1<=2W. Substitution in (5)-(6) gives
 S_K(N,W_N) <<_K N L^9 exp[-(alpha/20)*sqrtL],                            (7)
since alpha/10-(3/2)*(alpha/30)=alpha/20. This proves (1), because a
fixed polynomial in L is dominated by exp(epsilon sqrtL). Also
B logL<=(alpha/30)sqrtL eventually for each fixed B, proving the stated
logarithmic-width consequence. A width N^epsilon is NOT licensed by (5):
its positive cost exp[(3epsilon/2)L] exceeds this saved decay.

4. WHAT THE POINTWISE GOLDBACH EXPRESSION NOW RETAINS.
For the fixed delta and smooth Psi of nonstationary_spectral_reduction.py,
take K=pi+2delta. Delete from the retained weighted sum every pair with
|gamma-eta|<=W_N. The remainder C_sep is FINITE, with positive heights,
 gamma+eta<=(pi+2delta)N, |gamma-eta|>W_N,
the original factor1-Psi((gamma+eta)/N), and product multiplicities.
The already proved pointwise formula becomes
 R(N)=2psi(N-1)-N+C_sep+O_(A,delta)(N/log^A N).                          (8)
The inherited opposite-sign error is still present. This is NOT a
square-root error for R. A sufficient signed lower margin for C_sep is
still OPEN. Neither (1) nor (8) proves new prime-pair coverage. The earlier
polynomial identities and bounds remain available for other combinations.

Sources: the exact phase proof and source checks in spectral_diagonal_bound.py,
https://arxiv.org/pdf/2507.15184v2 (Corollary1/Table1),
https://arxiv.org/abs/2107.06506 (Riemann-von Mangoldt remainder), and
https://arxiv.org/pdf/2212.06867v1 (Theorem1.3 plus retained compact extension).
No new numerical zero/prime experiment; helpers below guard the symmetric
counting and width budget on artificial finite algebraic data only.
"""
from fractions import Fraction as F


def height_comparison_ratio_squared(gamma, eta):
    """Cost squared of using gamma's denominator for a possibly lower eta."""
    if any(type(v) is not F or v<0 for v in (gamma,eta)):
        raise ValueError('nonnegative rational heights required')
    return (1+gamma)/(1+min(gamma,eta))


def retained_decay(alpha, width_rate):
    """Decay coefficient after W=exp(width_rate*sqrt(logN)) is paid."""
    if type(alpha) is not F or type(width_rate) is not F or alpha<=0 or width_rate<0:
        raise ValueError('positive rational alpha and nonnegative width rate required')
    return alpha/10-F(3,2)*width_rate


def finite_near_height_model(locations, width):
    """Exact toy model: rows (sqrt(1+height), amplitude, multiplicity).

    Integer roots make the coarse kernel denominator rational. Separate rows
    may share a height. This is not actual zero data or a zero-density test.
    """
    if type(width) is not F or width<0:
        raise ValueError('nonnegative rational width required')
    if any(type(r) is not int or r<1 or type(x) is not F or x<0
           or type(m) is not int or m<1 for r,x,m in locations):
        raise ValueError('positive integer roots/multiplicities and nonnegative rational amplitudes required')
    first_moment=sum((m*x*x/r for r,x,m in locations),F(0))
    pair_sum=F(0)
    degrees=[]
    pair_copies=0
    for r,x,m in locations:
        degree=0
        for s,y,n in locations:
            if abs(r*r-s*s)<=width:
                degree+=n
                pair_sum+=m*n*x*y/min(r,s)
                pair_copies+=m*n
        degrees.append(degree)
    return {'pair_sum':pair_sum,'first_moment':first_moment,
            'max_degree':max(degrees,default=0),'pair_copies':pair_copies}
