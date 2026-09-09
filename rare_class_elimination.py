"""Eliminate rare-factor composite errors and sharpen the remaining question.

Owner: Kevin's Goldbach research. Purpose: compose the reviewed full affine
bound with the ORIGINAL pruned pool and polynomial weights, checking exact
class coverage rather than assuming it. Preserve the stronger linear-weight
and Buchstab endpoint consequences. No manuscript or prime-coverage claim.
Follow-on: rare_divisor_calibration.py and prime_cutoff_bridge.py now
provide the full weighted mass in this SAME restricted actual-zero regime.
The latter proves conditional prime-pair coverage; the earlier proof and
its original boundary below remain components, not universal Goldbach.

HYPOTHESES AND PARAMETER ORDER.
Keep the actual exceptional character, central suppressed target m in F_D,
I=(Y/2,Y], J={n:n,m-n in I}, and ORIGINAL B_good of rare_factor_pruning.py.
Thus m is even in[5Y/4,7Y/4], chi is primitive quadratic modulo D>24 and
has an ACTUAL zero beta=1-1/(eta*log D). Fix 0<epsilon<=1/100, sufficiently
small delta<=epsilon/3, and sufficiently large fixed u, in that order.
Set theta=delta/u, z_old=ceil(Y^theta), R=floor(Y^a), a=1/2-2epsilon.
As in rough_cofactor_sieve_bridge.py ADD the large-V regime
  Y=D^V, V>=log^3 eta, t=(1-beta)*log Y=V/eta<=1/log Y.
The former condition D<=Y^(delta/4) follows eventually from V>=4/delta.
Theta remains fixed; the bridge's U=K0 log eta and smaller internal cutoff
do not change B_good or authorize a growing-u use of an older theorem.
All limits are as eta tends to infinity in this regime, with ineffective
onsets. No zero existence or numerical parameter onset is asserted.

THE GENERAL POLYNOMIAL CONSEQUENCE.
For ANY fixed normalized polynomial f of degree d, f(0)=0,f(1)=1, put
 K_f(n)=log(n)*sum_(e|n)chi(e)*f(log(n/e)/log(n)),
 T_f=sum_(p in B_good)log(p)*K_f(m-p).
Let P be the SAME positive-sign-first weighted prime-pair sum as in
character_partner_weight.py. Define C_(k,f) using exactly this B_good,
restricted to partners n that are products of k DISTINCT negative-sign
primes and no positive-sign prime. Then
  T_f=P+sum_(3<=k<=d, k odd) C_(k,f)+o_(f,theta)(Y*t).       (1)
More strongly, the total FULL ABSOLUTE contribution of every composite
partner containing a positive-sign prime is o_(f,theta)(Y*t), after the
already negligible repeated-factor error. Positive parts of those classes
need not be treated separately or canceled against negative parts.

Proof of coverage and the absolute comparison.
1. On original rough partners, tau(n)<=2^(1/theta), so
   |K_f(n)|<=C_(f,theta)*log Y. The repeated-factor error, partners with
   at least two positive-sign primes, and partners with one positive-sign
   prime w<q<=R are already controlled ABSOLUTELY in
   quintic_partner_weight.py steps1--2. Those arguments are expressly for
   ANY fixed polynomial, using the displayed bound, rather than a special
   quintic sign inequality. The original B_good removes q<=w exactly.
   Union bounds may overlap these negligible classes; no disjointness is
   falsely needed. Their existing o(Y*t) estimates remain valid in the
   added regime. This proof uses those deductions without rerunning scans.
2. Every remaining positive-factor partner is squarefree and has a UNIQUE
   positive-sign prime q>R, all other prime factors negative. Write n=Mq.
   Since q is an integer,
     q>=floor(Y^a)+1>Y^a, M=n/q<Y^(1-a)<=Y^(13/25).          (2)
   In particular the floor does NOT leave a small uncovered band. From
   n,p=m-n in I one gets precisely
     Y/(2M)<q<=Y/M, Y/2<p=m-Mq<=Y.
   Also P^-(M)>z_old>=Y^theta and chi(q)=chi(p)=+1.
   Since chi(n)=-1, M has an odd number of negative factors and chi(M)=-1.
   The pool gives (M,D)=1. If a prime r divides both M and m then r|p,
   whereas r<=M=n/q<=Y/2<p, a contradiction. Hence (M,Dm)=1.
   These are EXACTLY the full affine theorem's hypotheses. The particular
   factorization of M, q-dependent pruning and the target restrictions
   select terms inside its NONNEGATIVE full B_M sum. The majorization is
   valid even when the original selection is not merely a set of M's.
3. Since q>Y^a with a>=12/25,
     log(p)*|K_f(n)|<=C_(f,theta)/a *log(p)*log(q).
   Each partner has exactly one such q; M=n/q is unique. There is no
   permutation or prime-factor multiplicity loss. The reviewed theorem
   rough_cofactor_sieve_bridge.py therefore makes the full absolute
   contribution o_(f,theta)(Y*t). This works for ANY factor count of M,
   not only the three quintic possibilities.
4. What remains squarefree has only negative-sign primes. Its number k
   is odd since chi(n)=-1. The exact k-fold finite difference defining
   K_f/log n annihilates a polynomial of degree<k. The k=1 term is the
   prime weight log n. This proves(1). No formal factor-share density is
   used; only the exact factor identity and actual affine upper bound.

QUINTIC AND LINEAR CONSEQUENCES.
For f(s)=s-kappa*s^2*(1-s)^2*(1-2s), fixed kappa>0, (1) becomes
  T_f=P+C_(3,f)+C_(5,f)+o_(theta,kappa)(Y*t),                 (3)
and the full absolute S2,S4,S6 contribution in quintic_partner_weight.py
is now negligible. The remaining triple and five-factor kernels are
  K_f/log n=4*kappa*x*y*z*(1-5*(xy+xz+yz)),
  K_f/log n=240*kappa*product_(i=1..5)x_i.
The triple changes sign and the five-factor term is positive. Their
previous absolute main-scale bounds survive. Their FORMAL integrals
from formal_weight_conservation.py are still not arithmetic estimates.

For f(s)=s, the sum on the right of(1) is empty. Hence the ORIGINAL
nonnegative W=chi*log=lambda_chi*Lambda satisfies
  T_W=P+E, 0<=E=o_theta(Y*t).                              (4)
Nonnegativity is exact by character_partner_weight.py; (1) now bounds
the formerly unresolved error E. Normalized quadratics give this same
W exactly, because (chi*log^2)(n)=log(n)*W(n) on negative-character units.
Thus the remaining issue for W is solely a lower bound on its FULL sum.
The size of B_good alone does not give it, since W vanishes on all-negative
squarefree composites. The exact smaller-divisor summands are still signed.

For example take chi modulo31, n=3*11*29=957, all three signs negative.
Then W(n)=0. At R=floor(957^(12/25))=26, the smaller divisors retained
are1,3,11 and their sum is log(33/29)>0; the omitted d=29 term is
-log(33/29). This finite identity refutes a pointwise assertion that
truncating W gives a lower bound. It asserts no actual zero or asymptotic
failure for the central target family. The new error estimate does not
turn the known accessible main into a lower bound for T_W.

BUCHSTAB ENDPOINT CONSEQUENCE ON THE ORIGINAL FULL ROUGH POOL.
Use A(n),S_A,U_A and Z=length(J_real)*S_2(m)*t of
buchstab_endpoint_bridge.py, which uses the FULL rough rare-first pool
before optional B_good pruning. Its exact identity remains
  S_A(R)=S_A(z_old)-U_A(z_old,R)=P+E_R, E_R>=0.
Since 3a>1, (R+1)^3>Y eventually; a terminal composite has exactly two
prime factors. It cannot be a unit square of sign-1. Thus n=rq consists
of distinct primes r,q>R with chi(r)=-1,chi(q)=+1. These terms already
belong to B_good, since R>w and R>z_old eventually. They meet(2) with
M=r. Their weight satisfies
  log(p)*log(n)<=a^-1*log(p)*log(q).
The SAME affine theorem now proves
  0<=E_R=o_theta(Y*t),                                    (5)
improving the old C*epsilon*Z upper bound, in the added large-V regime.
No small-root or equality case is omitted: both factors strictly exceed
floor(Y^a), which is the integer condition used in(2).

The initial sieve main and its fixed fundamental-lemma error are unchanged:
  P=L*X*V(z_old)-U_A(z_old,R)
                  +O((eta_u/theta)*Z)+o(Y*t).              (6)
Here X,V are EXACTLY those of buchstab_endpoint_bridge.py and L=log Y.
For any fixed c>0 it would suffice to establish
  U_A(z_old,R)<=L*X*V(z_old)-(c+C0*eta_u/theta)*Z,            (7)
with valid C0. The previous C*epsilon charge has gone; inequality(7)
remains UNPROVED. The least-factor condition P^-(k)>=q in U_A still
couples the two variables and keeps repeated factors. Do not replace
it by a separated-coefficient model or discard those factors.

WHAT CHANGED IN THE RESEARCH QUESTION.
All polynomial rare-factor errors are now small in this regime. The
quintic leaves signed all-negative odd composites; W has no such error,
but its full weighted mass is unknown. The Buchstab endpoint has no
main-scale composite loss, but the one-sided prime-times-rough estimate
remains missing. None of these consequences supplies a positive lower
bound from the formal conservation identity or estimates its signed
boundary-minus-discrepancy. Every prior source correction and method
limitation retains its original scope. These are components for further
mathematics, not a claim of Goldbach coverage or worldwide originality.

Finite helpers below guard exact support and polynomial identities only.
Their labelled logarithmic shares are formal, not sampled prime densities.
"""
from fractions import Fraction as F
from itertools import product
from math import prod

from log_weight_barrier import _coefficients


def affine_range_certificate(scale, first, partner, rare_factor, epsilon):
    """Certify the exact interval/exponent transfer, without asserting primes.

    Character/primality/roughness/zero premises are deliberately not inferred
    from these arithmetic inequalities. The returned cofactor is n/q.
    """
    if any(type(v) is not int or v < 1 for v in (scale, first, partner, rare_factor)):
        raise ValueError('require positive integer sizes and factors')
    if type(epsilon) is not F or not 0 < epsilon <= F(1, 100):
        raise ValueError('require exact 0<epsilon<=1/100')
    if not (scale < 2*first <= 2*scale and scale < 2*partner <= 2*scale
            and 5*scale <= 4*(first+partner) <= 7*scale):
        raise ValueError('outside the original intervals or central target band')
    if rare_factor < 2 or partner % rare_factor:
        raise ValueError('require a nontrivial factor of the partner')
    exponent = F(1, 2)-2*epsilon
    if rare_factor**exponent.denominator <= scale**exponent.numerator:
        raise ValueError('factor is not strictly above floor(Y^a)')
    cofactor = partner//rare_factor
    if cofactor < 2:
        raise ValueError('this is the composite transfer, not the prime atom')
    if cofactor**25 >= scale**13:
        raise ArithmeticError('derived strict cofactor bound failed')
    return cofactor


def factor_share_kernel(coefficients, negative_shares, positive_shares=()):
    """Exact squarefree K_f/log(n), from the full divisor definition."""
    coefficients = _coefficients(coefficients)
    if (type(negative_shares) is not tuple or type(positive_shares) is not tuple
            or not negative_shares or len(negative_shares) % 2 != 1):
        raise ValueError('require an odd positive number of negative shares')
    shares = negative_shares+positive_shares
    if len(shares) > 16 or any(type(x) is not F or x <= 0 for x in shares) or sum(shares) != 1:
        raise ValueError('require at most16 positive exact shares summing to1')
    signs = (-1,)*len(negative_shares)+(1,)*len(positive_shares)
    total = F(0)
    for bits in product((0, 1), repeat=len(shares)):
        complement = sum((x for x, bit in zip(shares, bits) if not bit), F(0))
        value = F(0)
        for c in reversed(coefficients):
            value = value*complement+c
        total += prod(sign for sign, bit in zip(signs, bits) if bit)*value
    return total
