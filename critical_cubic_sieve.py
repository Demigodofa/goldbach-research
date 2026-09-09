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

TRIPRIME DISPERSION PREFLIGHT: A PAID DIAGONAL, THE SAME OPEN COVARIANCE.
7. Test whether three prime factors automatically supply another usable
free average. Partition the ORDERED p<q<r sum into dyadic boxes
p~P,q~Q,r~R, with PQR comparable to x and every factor>x^kappa.
Use s=pq as row index; its ordered two-prime factorization is unique.
Let F_s(r) be the full coefficient in T_kappa times w_(sr), retaining
EVERY physical, ordering, squarefree, roughness and target-coprime mask.
The denominator log(sr)^3 stays in F; it is not frozen without error.
Writing K for the number of nonempty rows, Cauchy gives EXACTLY
 |T_box|^2 <= K*(D+O),
 D=sum_(s,r)|F_s(r)|^2,
 O=sum_s sum_(r!=t) F_s(r) conjugate(F_s(t)).             (9)
O is real and signed, and D+O>=0. Ordinary prime counting gives
 K<<_kappa PQ/L^2,
 D<<_kappa L^2*(P/L)*(Q/L)*(R/L)<<_kappa x/L.
Here the logarithmic coefficient is bounded, and |w|<<L; no prime
correlation estimate is used in this diagonal upper bound. Since r is
the largest factor, R is at least a fixed multiple of x^(1/3). Hence
 sqrt(KD)<<_kappa x/(sqrt(R)*L^(3/2))
             <<_kappa x^(5/6)/L^(3/2).
Even the crude O(L^3) box count leaves O_kappa(x^(5/6)L^(3/2)),
which is all-log small. Thus a diagonal loss does not obstruct this step.

8. Its off-diagonal reflected arguments are q1=N-sr,q2=N-st, and
 t*q1-r*q2=(t-r)N.                                    (10)
This is precisely the saved prime-dilation covariance, restricted now
to semiprime s and weighted by the full triprime factors. The expansion
of w*w has all four aa-ab-ba+bb terms with identical surviving masks.
The third factor changes the row coefficient/support; it does not make
either of the reflected primality conditions a free variable. In
particular free_divisor_correlation.py requires unweighted free variables
in TWO SEPARATE additive summands. Factoring s=pq does not meet that
hypothesis. Nonnegativity of the full square does NOT license deleting
prime restrictions inside its signed row sum. Any such relaxation still
requires an explicit triangle/Cauchy positive majorant and its full cost;
selected signed off-diagonal terms cannot simply be discarded.

The finite toy row x601,N1202,s35,r in{11,13,17} obeys the retained
support for a sufficiently small fixed kappa. Giving its three entries
value-1 yields T=-3,D=3,O=6,K=1: three prime factors do not themselves
force cancellation. These toy weights are not the actual w; this is
neither an actual-prime counterexample nor a universal dispersion no-go.
DISPOSITION: the proposed automatic extra-average mechanism is retired.
The diagonal bound and exact surviving masks are preserved, but no new
source is invoked for an unchanged missing input. E_kappa+24T_kappa
remains OPEN. A future trilinear theorem with matching prime coefficients
could reopen this route; the polynomial endpoint reduction remains useful.

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
from math import gcd, prod

from major_arc_kernel import _factorization
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


def triprime_rows(x, rough_cutoff, weights):
    """Exact retained toy rows; supplied values include the full log coefficient.

    The integer cutoff stands in for x^kappa; it is not an asymptotic claim.
    All supplied full weights survive unchanged on the retained support.
    """
    if type(x) is not int or x < 2 or type(rough_cutoff) is not int or rough_cutoff < 1:
        raise ValueError('integer x>=2 and cutoff>=1 required')
    rows = {}
    for n, value in weights.items():
        if type(n) is not int or n < 1 or type(value) is not F:
            raise ValueError('positive integer inputs and rational full weights required')
        if not x < 2*n <= 2*x or gcd(n,2*x) != 1:
            continue
        factors = _factorization(n)
        if len(factors) != 3 or any(power != 1 for _,power in factors):
            continue
        p,q,r = (prime for prime,_ in factors)
        if p <= rough_cutoff:
            continue
        rows.setdefault((p,q),{})[r] = value
    return rows


def triprime_row_energy(rows):
    """Full real signed covariance and its exact finite Cauchy bound."""
    row_sums = [sum(values.values(),F(0)) for values in rows.values() if values]
    diagonal = sum((v*v for values in rows.values() for v in values.values()),F(0))
    energy = sum((v*v for v in row_sums),F(0))
    return {'sum':sum(row_sums,F(0)), 'rows':len(row_sums),
            'diagonal':diagonal, 'off_diagonal':energy-diagonal,
            'energy':energy, 'cauchy_bound_squared':len(row_sums)*energy}
