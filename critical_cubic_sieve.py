"""A paid moving square-root cutoff and exact cubic factor cancellations.

Owner: Kevin's Goldbach research. Purpose: reach the critical cutoff for
a specific smooth coefficient, pay its actual error, and preserve the
precise signed prime-correlation terms which remain. No arbitrary
square-root Type I theorem or Goldbach coverage is asserted.

Use N=2x, I=(x/2,x], L=logx, y=floor(exp(sqrtL)),
 a_n=Lambda(N-n), b_n=c_y 1_(P^-(N-n)>y), w_n=a_n-b_n,
 c_y=product_(ell<=y)(1-1/ell)^(-1), B_P~S_2(N)x/(2L).
For a fixed integer k>=3 define the MOVING polynomial coefficient
 U_k(n)=sum_(d|n)mu(d)(1-2logd/logn)_+^k.                 (1)
It has cutoff sqrt(n), not sqrt(x). This distinction is essential to
the exact complement identities below.

ACTUAL TYPE I WITH A LOGARITHMIC MARGIN.
1. For every fixed A there exists a fixed B>0 such that, with
D=floor(sqrt(x)/L^B),
 sum_(d<=D) max_J |sum_(dk in I,k in J)w_(dk)| <<_A x/L^A. (2)
Here the maximum is over intervals. This refines the SAVED fixed-power
range using the same inputs; it does not reach arbitrary weights at sqrtx.
Ford2023 Theorem3.4 explicitly has q<=sqrtX/(logX)^B and maxima over
reduced residues and endpoints. Apply it at X=2x, enlarging B if needed.
Abel converts prime counts to log weights, paid by asking for a larger
fixed initial saving. Subtracting two endpoint estimates gives intervals.
For (d,N)=1, the a main is interval length in n divided by phi(d).
Proper powers, also including all nonreduced a contributions, total
O(x^(1/2+eta)L^C) over d, because every nonzero N-p^j has at most
O_eta(x^eta) divisors and there are O(sqrtx L) proper powers.

2. Recheck b at this larger range. Unless some ell<=y divides both d
and N (in which case b vanishes), its forbidden k-residue density is
g(ell)=0 for ell|d and g(ell)=1/ell otherwise. These satisfy the uniform
dimension-one upper bound. The normalized density is
 M_d=c_y product_(ell<=y)(1-g(ell))
    =product_(ell|d,ell<=y)(1-1/ell)^(-1).
Use fundamental-lemma level D0=floor(x^(1/4)), independent of d.
Its parameter logD0/logy is comparable to sqrtL, so the relative error
beats every fixed inverse power of L. Each squarefree modulus has an
O(1) interval remainder even for short intervals. Their TOTAL cost is
 O(c_y D D0)=O(x^(3/4)L^(1/2-B)).
The aggregate relative main error is all-log, since
sum_(d<=D) x/phi(d)<<xL. The ratio between M_d and d/phi(d) differs
from1 by O(L/(y logy)), from primes ell|d above y. This mismatch is
all-log after summation. Moduli with a common prime ell|N above y cost
 <<xL sum_(ell|N,ell>y)1/ell <<xL^2/(y logy),
using sum_(m<=D/ell)1/phi(ell*m)<<L/ell. Small common primes already
give b=0. Together with step1's proper powers this proves (2).

PAY THE MISSING NEAR-CUTOFF DIVISORS.
3. For d<=D, d^2<x/2 eventually. The coefficient
f_d(n)=(1-2logd/logn)^k is active throughout I, monotone increasing,
lies in[0,1], and has total variation at most1. Abel and (2) therefore
control the sum with these moving coefficients by O_A(x/L^A).
For D<d<=sqrt(n)<=sqrtx, on the OTHER hand, the weight is at most
 O_B((logL/L)^k). The floor in D only changes the fixed constant.
Since |w|<<L, the entire omitted portion is at most
 <<_B Lx*(logL/L)^k sum_(D<d<=sqrtx)1/d
 <<_(B,k) x*(logL)^(k+1)/L^(k-1).                       (3)
In particular choose a fixed A=3 and its B in (2). Then
 sum_(n in I) U_3(n)w_n
       =O_B(x*(logL)^4/L^2)=o(x/L).                    (4)
This is an ACTUAL estimate for one coefficient. The long portion is
not all-log small, and it does not upgrade arbitrary Type I weights.
For k=2 this particular crude tail budget is not o(x/L); no general
quadratic impossibility follows.

LOCALIZATION WITH THE MOVING NORMALIZATION ALSO HAS TO BE PAID.
4. Fix 0<kappa<=1/20 and z=x^kappa. Apply the direct Mellin identity
from polynomial_rough_localization.py to (1), separately at each n.
Its Euler factors depend on log n, so do NOT apply Henriot as though
those factors were a fixed multiplicative function. Instead, since
logn>=L-log2>=L/2 for large x, use the pointwise domination
 |1-ell^(-2(1+iu)/logn)|
     <=2min(1,2t logell/logn)
     <=2min(1,4t logell/L), t=1+|u|.
The last product is the FIXED multiplicative W_(2t,sqrtx)(n).
After extracting the ENTIRE p-power n=p^j m, p not dividing m, its
p-factor is 2min(1,4t logp/L). For p<=z the new beta=4logp/L<=1/5.
All other source hypotheses from the saved proof still hold: if
p^j<=x^(1/10), m has interval scale>=x^(9/10)/2 and sqrtx<X/2.
The source/Mertens constants stay uniform in t>=1; the partner a and
comparison b are handled separately with their saved moments/densities.

The saturated cubic integral and complete prime sum therefore give
 sum_(n in I,P^-(n)<=z)|U_3(n)w_n|
       << kappa*(2+log(1/(4kappa))) S_2(N)x/L+all-log
       << kappa*log(e/kappa) S_2(N)x/L+all-log.          (5)
The leading constant is independent of fixed kappa in (0,1/20].
The same proof without extraction bounds sum|U_3|(a+b)<<S_2(N)x/L.
The old common-target-factor removal, large p-power tail, and squareful
rough deletion use only |U_3|<=tau; they still cost respectively
all-log, O(x^(39/40)L), and O(xL^2/x^kappa). Thus the remaining
COMPOSITE sum may be restricted to squarefree (n,N)=1 and P^-(n)>z,
with (5)'s arbitrarily small RELATIVE loss and negligible other errors.
All-log onsets after squareful removal depend on fixed kappa.

EXACT CANCELLATION OF WHOLE FACTOR CLASSES, AFTER THE ESTIMATES.
5. On squarefree n write r=omega(n), alpha_i=logp_i/logn, so
sum alpha_i=1. Let f(s)=(1-2s)_+^k and U=sum_S(-1)^|S| f(sum_S alpha).
Complementation gives
 sum_S(-1)^|S| f(1-sum_S alpha)=(-1)^r U.
For every real s, f(s)+(-1)^k f(1-s)=(1-2s)^k. Consequently
 [1+(-1)^(k+r)]U_k(n)
     =sum_S(-1)^|S| (1-2sum_S alpha)^k.                 (6)
The right side is the r-fold finite difference of a degree-k polynomial,
so vanishes for r>k. Hence U_k(n)=0 when r>k and r,k have the SAME
parity. The opposite parity is not removed by (6).

For the cubic this implies U_3=0 for odd r>=5. When r=3, only the
degree3 mixed monomial survives on the right of (6), giving
 2U_3=48 alpha_1 alpha_2 alpha_3,
 U_3(pqr)=24 logp logq logr/(log(pqr))^3.                (7)
This is valid for unbalanced as well as balanced triprimes. For a prime,
U_3=1. The EVEN factor classes remain, with their original signed U_3:
four equal shares give1/2 and six equal shares give-2/9.
Squarefreeness matters: log(rad n)/logn need not equal1 for repeated
factors, and (6) cannot silently be applied before paying their deletion.
Likewise using sqrtx instead of sqrtn changes the sum of normalized
shares and destroys the exact zero, even though the cutoffs are close.

THE PRECISE OPEN PRIME-CORRELATION TARGET.
6. On the retained rough squarefree target-coprime support define
 E_kappa(w)=sum_(n in I,omega(n) even>=2)U_3(n)w_n,
 T_kappa(w)=sum_(p<q<r,pqr in I) [logp logq logr/(log(pqr))^3] w_(pqr).
Both sums retain P^->x^kappa and (n,N)=1. The ordering in T avoids
duplicate factorizations; no additional factorial may be inserted.
Separating the prime term in (4), then applying (5)-(7), proves
 sum_(p in I prime)a_p
   =B_P-E_kappa(w)-24T_kappa(w)
       +O(kappa log(e/kappa) S_2(N)x/L)+o_kappa(x/L).     (8)
The even classes have fewer than1/kappa factors for fixed kappa. Neither
E_kappa nor T_kappa, nor their sum, has been estimated with a sufficient
signed margin. The cubic cancellation is a coefficient identity, not
cancellation of the linked prime conditions inside the remaining sums.
The paid endpoint/localization estimates license the reduction; they do
not establish Goldbach, a numerical onset, or a globally new identity.

Source checks2026-09-09: Ford2023 notes Theorem3.4, printedp35 (BV with
logarithmic margin, residue and endpoint maxima), Theorem3.6,p38
(fundamental lemma): https://ford126.web.illinois.edu/sieve2023.pdf
The comparison proof is the log-margin extension of
composite_bilinear_bridge.py, not a new beyond-half distribution result.
Direct Mellin and joint input: polynomial_rough_localization.py and
polynomial_joint_majorant.py, using Henriot's corrected NEW Theorem5,
2014 erratum p377, DOI10.1017/S0305004114000280. No blocked source
route was retried. Exact helpers below guard coefficient algebra and
error budgets; finite toy shares do not certify prime correlations.
"""
from fractions import Fraction as F
from math import prod

from polynomial_joint_majorant import polynomial_cofactor_samples
from polynomial_rough_localization import polynomial_factor_pattern


def critical_pattern(shares, degree=3):
    """Exact normalized squarefree log-share algebra, up to the saved cap12."""
    return polynomial_factor_pattern(tuple(shares), F(1,2), degree)


def complement_identity(shares, degree):
    """Return the complementary-cutoff side and independent full polynomial sum."""
    shares = tuple(shares)
    value = critical_pattern(shares, degree)
    full = F(0)
    for mask in range(1 << len(shares)):
        subtotal = sum((s for j,s in enumerate(shares) if mask & (1 << j)), F(0))
        full += (-1)**mask.bit_count()*(1-2*subtotal)**degree
    return (1+(-1)**(degree+len(shares)))*value, full


def reduced_cubic_pattern(shares):
    """Apply exactly the proved cancellations; retain every even factor class."""
    shares = tuple(shares)
    direct = critical_pattern(shares)
    if len(shares) == 1:
        return F(1)
    if len(shares) == 3:
        return 24*prod(shares)
    if len(shares) >= 5 and len(shares) % 2:
        return F(0)
    return direct


def fixed_x_pattern(shares, logn_over_logx, degree=3):
    """Toy fixed-sqrtx coefficient, deliberately distinct from moving sqrtn."""
    shares = tuple(shares)
    critical_pattern(shares, degree)  # validate normalization first
    if type(logn_over_logx) is not F or not 0 < logn_over_logx <= 1:
        raise ValueError('rational 0<logn/logx<=1 required')
    return polynomial_cofactor_samples(tuple(2*logn_over_logx*s for s in shares),degree)


def tail_log_profile(degree):
    """Powers in the crude tail divided by x/logx; fixed B constants excluded."""
    if type(degree) is not int or degree < 1:
        raise ValueError('positive integer degree required')
    return {'logx_power': 2-degree, 'loglogx_power': degree+1,
            'vanishes_at_prime_scale': degree >= 3}


def moving_prime_factor_majorant(logp_over_logx, logn_over_logx, t):
    """Return moving/fixed local upper factors used before arithmetic summation."""
    if any(type(v) is not F for v in (logp_over_logx,logn_over_logx,t)):
        raise ValueError('exact rational inputs required')
    if not logp_over_logx > 0 or not F(1,2) <= logn_over_logx <= 1 or t < 1:
        raise ValueError('require positive prime share, logn/logx in[1/2,1],t>=1')
    moving = 2*min(F(1),2*t*logp_over_logx/logn_over_logx)
    fixed = 2*min(F(1),4*t*logp_over_logx)
    return moving, fixed
