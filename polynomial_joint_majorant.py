"""An actual joint arithmetic bound for polynomial-cutoff Vaughan boxes.

Owner: Kevin's Goldbach research. Purpose: pair a preserved polynomial tool
with corrected Henriot, and pay the complete box count. Proof and reusable
finite guards only. Sol theory/actual-file review PASS after the exact
endpoint-enclosure correction recorded in step4.

RESULT AND ITS LIMIT.
For a fixed polynomial degree k>=9, an exact alternative Vaughan remainder
has prime/cofactor boxes bounded ABSOLUTELY by O(Y S_2(m)/log Y). This uses
the actual linked arithmetic, not independent marginal norms or a formal
prime-density model. It improves the separate-moment budget in
optimized_cofactor_cutoff.py. Summing Theta(log Y) boxes over a fixed
positive exponent width yields only O(Y S_2(m)); no full cancellation,
new prime lower bound, or additional coverage follows. Polynomial weights
are retained as part of the successful JOINT bound.

SETUP AND EXACT REMAINDER.
1. Keep the unexceptional setup, gamma in(5/12,1/2), fixed
   0<delta<=1/4800, I=(Y/2,Y], even m in[5Y/4,7Y/4], S=Y^delta,
   L=log Y, and E=1_I(Lambda-Gamma_S). Let U=V=floor(Y^(gamma/2))
   and fix an integer k>=9. Choose
    lambda(d)=mu(d)(1-log(d)/log(V))_+^k,
    S_lambda(c)=sum_(d|c)lambda(d).
   Here x_+=max(x,0). In particular lambda(1)=1, |lambda(d)|<=1,
   and lambda is supported d<=V. The EXACT identity and TI transfer of
   optimized_cofactor_cutoff.py apply. The full original correlation equals
   that of R_lambda=(mu-lambda)*Lambda_>U*1, with error O_A(Y/L^A).
   Removing internal proper prime powers has the already paid total error
    O(Y^(1-gamma/4+2delta+o(1))).
   The remaining coefficient is exactly
    R_lambda,p(n)=-sum_(pc=n,p>U prime,c>=2)log(p)S_lambda(c). (1)
   Small c are genuinely present. Changing the cutoff is licensed for the
   FULL remainder by its compensating TI terms. It is NOT an assertion that
   every separately restricted old hard-cutoff box equals its new box.
   We also do not identify this grouping with the old balanced h_r grouping.

POINTWISE POLYNOMIAL AND PRIME MAJORANTS.
2. Reuse the CORRECTED radical majorant of radical_majorant_correlation.py:
    H_R(n)=log(R)*int_R w_(10(1+|t|),R)(n)/(1+|t|)^10 dt,
    w_(a,R)(n)=prod_(ell|n)2 min(1,a log(ell)/log(R)).
   The product is over distinct prime factors, including for prime powers.
   For every c>=1, Mellin inversion gives
    S_lambda(c)=k!/(2pi)*int_R e^(1+it)/(1+it)^(k+1)
                      *prod_(ell|c)(1-ell^(-(1+it)/log(V)))dt. (2)
   Proof: invert (log(V/d))_+^k/k! on Re(s)=1/log(V), multiply by
   k!/log(V)^k, set s=(1+it)/log(V), and sum the finite divisor expansion.
   The integral is absolutely convergent for each c. The term d=V is0.
   Since Re(z)>=0 implies |1-e^-z|<=min(2,|z|), each local factor is
   bounded by its w factor. Also, for k>=9,
    |1+it|^(-(k+1))<=32(1+|t|)^(-10).
   Consequently, with a fixed degree-dependent constant,
    |S_lambda(c)| <<_k H_V(c)/log(V).                       (3)
   This retains the logarithmic divisor cutoff and uses genuine prime
   factors of c. It is not the earlier formal Dickman cancellation.
3. The saved, corrected pointwise theorem gives |Gamma_S(n)|<<_G H_S(n).
   The ACTUAL prime weight also obeys, for n<=Y,
    Lambda(n) <<_delta H_S(n).
   Only n=ell^j needs checking. Radical invariance and the portion |t|<=1
   of the integral give the explicit lower bound
    H_S(ell^j)>= (511/1152) min(log ell,log S).
   Because log ell<=log Y and log S=delta log Y, this proves the claim.
   Hence on I,
    |E(n)| <<_(delta,G) H_S(n).                            (4)
   This handles partner prime powers directly; none are silently omitted.

UNIFORM AFFINE APPLICATION OF THE CORRECTED THEOREM.
4. Fix constants c0,c1 with
    1/4<c0<=c1<1-gamma/2.
   Since gamma/2<1/4, this also puts c0>gamma/2. For a nonempty
   factor box p in(P,2P], c in(C,2C], PC comparable to Y, take
    Y^c0<=C<=Y^c1,
   and retain all physical and other support masks. First suppose p is an
   actual prime with p>U and p does not divide m. The exact c-mask
    J_p={c:pc in I, m-pc in I}
   is contained in the CLOSED enclosure [x,x+y], where
    x=max(Y/2,m-Y)/p,
    x+y=min(Y,m-Y/2)/p.
   Centrality implies x/3<=y<=x and x comparable to Y/p, hence to C.
   Endpoint inclusion in J_p depends on m; do not assert an exact half-open
   interval identity. Cover the closed enclosure by the two half-open
   intervals (x-1,x+y/2] and(x+y/2,x+y]. For large Y, each has start and
   length comparable to C, and length at most its start. Their polynomial
   values stay positive: pc>=Y/2-p>0 and m-pc>=Y/2 on this cover.
   This uses only O(1) intervals and preserves all positive upper bounds. Use
    Q1(c)=c, Q2(c)=m-pc, Q=Q1 Q2=-pc^2+mc.
   They are primitive (p does not divide m), have distinct roots over Q,
   degree g=2, coefficient norm p+m<<Y, and discriminant m^2. The NEW
   Theorem5 of Henriot's2014 erratum applies with alpha=1/2, eta=1/4,
   function-class epsilon=1/2000: each covering start X satisfies
   X>=C0||Q||^eta eventually by c0>1/4, and its length is between X^alpha
   and X. Also epsilon<alpha/[50g(g+1/eta)]=1/1200. We continue to write
   x comparable to C for either covering start; V,S<x/2 eventually,
   uniformly in this fixed exponent interval.
5. This is a direct application of the corrected theorem and its exact
   valuation convention, NOT an uncorrected leading-coefficient corollary.
   Reuse its checked statement and definitions from
   radical_majorant_correlation.py and rare_affine_small_cofactor.py.
   Primary source locators: original definitions https://arxiv.org/pdf/1102.1643
   and2014 erratum NEW Theorem5, printedp377, DOI10.1017/S0305004114000280.
   The already blocked erratum fetch is not needed or retried here.
   For t,s>=10 use the nonnegative multiplicative function
    F(v,w)=w_(t,V)(v) w_(s,S)(w).
   It lies uniformly in the saved M_2(2,B_epsilon,epsilon) class:
   F<=tau(v)tau(w), with the same coprime ratio and prime-power bounds.
   Drop only nonnegative divisor-sum restrictions, retaining primes ell<=x.
   Put a=2min(1,t log ell/log V), b=2min(1,s log ell/log S).
   The exact corrected local divisor sums and root counts are
    ell not dividing p*m: rho=2, K_ell=1+(a+b)/ell;
    ell dividing m:       rho=1, K_ell=1+a*b/ell;
    ell=p not dividing m: rho=1, K_ell=1+a/ell.              (5)
   At the last prime, the second form has no root. Zero valuations in a
   nonzero tuple impose nondivisibility, as in the corrected source. The
   all-zero tuple contributes1 without an extra condition. All K_ell are
   bounded by exp((a+b)/ell), since 0<=a,b<=2 gives ab<=a+b.
6. The sieve product is <<S_2(m)/log(x)^2. When p<=x, its single extra
   leading-prime factor relative to the usual two-root product is
    (1-1/p)/(1-2/p)=(p-1)/(p-2)<=2;
   for p>x there is no such factor. Here p is odd eventually and m is even.
   Use the native common-root factors at primes dividing m; S_2(m) stays.
   With d_V=log(V)/log(x), d_S=log(S)/log(x), the SAME Mertens split as
   in the saved proof, at V^(1/t) and S^(1/s), gives
    prod_(ell<=x) K_ell << (t/d_V)^2(s/d_S)^2.
   Henriot therefore gives the ACTUAL nonnegative sum
    sum_(c in J_p) w_(t,V)(c) w_(s,S)(m-pc)
      << x S_2(m)/log(x)^2 * (t/d_V)^2(s/d_S)^2.
   Tonelli and the finite second moments against(1+|t|)^(-10) imply
    sum_(c in J_p) H_V(c)H_S(m-pc)
      << x S_2(m)/(d_V d_S).                              (6)
   Each ratio is bounded above and away from0 in the fixed parameter range.
   Combining(3),(4),(6) proves
    sum_(c in J_p)|S_lambda(c)E(m-pc)| << C S_2(m)/L.         (7)
   This is the joint arithmetic estimate missing from separate Cauchy.

ACTUAL BOX BOUND, BAD PRIMES AND COMPLETE SUMMATION COST.
7. Chebyshev gives sum_(p in(P,2P] prime)log p<<P. Thus(7) proves,
   for every bounded physical weight F and any subset of the good tuples,
    sum_(p,c in box,p>U,p not dividing m) log p
         *|S_lambda(c)F(pc/Y,(m-pc)/Y)E(m-pc)|
      <<_(gamma,delta,k,c0,c1,G,F) Y S_2(m)/L.              (8)
   Smoothness is not required for this absolute estimate. The earlier FULL
   cutoff-change TI transfer still uses its original fixed smooth F; this
   per-box fact does not upgrade that transfer to arbitrary sharp weights.
8. Do not apply the primitive-polynomial theorem when p divides m. Instead
   use |S_lambda(c)|<=tau(c), |E|<<L+S^2 and c<=Y/p. There are
   O_gamma(1) prime divisors p>U of m, since their distinct product divides m.
   Their ENTIRE contribution, across all boxes, is at most
    Y^(1-gamma/2+2delta+o(1)),                             (9)
   a power saving. The original internal-power error from step1 is also
   paid globally. Neither error is multiplied by an artificial tuple count.
9. A factor-2 partition has only O(1) compatible c-boxes per p-box because
   pc in(Y/2,Y]. Consequently a union of N such p-boxes inside the fixed
   exponent domain has absolute contribution
    O(N Y S_2(m)/L)+the globally paid power errors.          (10)
   If N=o(L), this is o(Y S_2(m)), RELATIVE to the positive cross-term scale.
   In particular any fixed polylogarithmic band around sqrt(Y) has
   N=O(log log Y) and is negligible in this relative sense. Over a fixed
   positive exponent width there are Theta(L) boxes; (10) gives only a
   main-scale upper bound, not the required full signed estimate.
   More precisely a p-exponent band of width h in a fixed admissible domain
   costs O((h+1/L)Y S_2(m)), with constants uniform in h. This can make a
   narrow transition band a small relative loss by choosing h first.
   It does not bound the rest of the factor domain or prove Goldbach.

RETAINED COMPONENT AND NEXT DISCRIMINATOR.
The exact polynomial cutoff plus corrected AFFINE majorant is now an actual
joint estimate. The failed separate-moment route remains failed under its
old input; this success uses new joint arithmetic input, not a renamed norm.
Keep original polynomial identities, conditional coverage, balanced projection
and all source corrections intact. A useful next test must address the full
logarithmic accumulation or the complementary signed ranges. Repeating the
same box estimate at higher polynomial degree cannot supply an extra log.

The routines below check finite polynomial/Euler algebra, local valuation
factors, physical interval geometry and exact exponent/log budgets. They do
not numerically integrate Mellin inversions or infer prime cancellation.
"""
from fractions import Fraction as F
from math import factorial, gcd, prod

from major_arc_kernel import _factorization, _mobius_phi
from unexceptional_vaughan_gate import _divisors, _positive


def polynomial_cofactor_samples(shares, degree):
    """Finite log-share algebra; rational samples need not be actual prime logs."""
    _positive(degree, 'degree')
    shares = tuple(shares)
    if len(shares) > 12 or any(type(s) is not F or s <= 0 for s in shares):
        raise ValueError('at most12 positive exact log-share samples required')
    total = F(0)
    for mask in range(1 << len(shares)):
        share = sum((s for j, s in enumerate(shares) if mask & (1 << j)), F(0))
        total += (-1)**mask.bit_count()*max(F(0), 1-share)**degree
    return total


def mellin_euler_pair(n, prime_values):
    """Exact finite divisor expansion of the Mellin Euler product."""
    _positive(n, 'n')
    prime_values = dict(prime_values)
    factors = dict(_factorization(n))
    if set(prime_values) != set(factors) or any(type(v) not in (int, F) for v in prime_values.values()):
        raise ValueError('one exact sample per distinct prime factor required')
    direct = sum((_mobius_phi(d)[0]*prod(prime_values[p]**e for p, e in _factorization(d))
                  for d in _divisors(n)), F(0))
    return direct, prod((1-v for v in prime_values.values()), start=F(1))


def mellin_majorant_constant(degree):
    """A safe constant in |S_lambda|<=constant*H_V/logV, only k>=9."""
    _positive(degree, 'degree')
    if degree < 9:
        raise ValueError('the saved H-kernel domination requires degree>=9')
    return 32*factorial(degree)  # e/(2pi)<1


def prime_power_majorant_lower_constant():
    return F(4, 9)*(1-F(1, 2**9))


def physical_cofactor_interval(y, target, prime):
    """Closed enclosure; the actual strict endpoint membership depends on m."""
    for value, name in ((y, 'Y'), (target, 'target'), (prime, 'prime')):
        _positive(value, name)
    if target % 2 or not F(5, 4)*y <= target <= F(7, 4)*y:
        raise ValueError('central even target required')
    if _factorization(prime) != ((prime, 1),):
        raise ValueError('actual prime coefficient required')
    left = max(F(y, 2), F(target-y))/prime
    right = min(F(y), target-F(y, 2))/prime
    return left, right


def _affine_inputs(local_prime, target, coefficient, a, b):
    for value, name in ((local_prime, 'local prime'), (target, 'target'), (coefficient, 'coefficient')):
        _positive(value, name)
    if _factorization(local_prime) != ((local_prime, 1),):
        raise ValueError('local modulus must be prime')
    if gcd(target, coefficient) != 1:
        raise ValueError('primitive affine form requires coprime target and coefficient')
    if any(type(v) not in (int, F) or not 0 <= v <= 2 for v in (a, b)):
        raise ValueError('exact local weights in[0,2] required')


def affine_local_factor(local_prime, target, coefficient, a, b):
    """Corrected infinite local divisor factor and polynomial root count."""
    _affine_inputs(local_prime, target, coefficient, a, b)
    if coefficient % local_prime == 0:
        return 1+F(a)/local_prime, 1
    if target % local_prime == 0:
        return 1+F(a)*F(b)/local_prime, 1
    return 1+(F(a)+F(b))/local_prime, 2


def affine_truncated_factor(local_prime, target, coefficient, a, b, depth):
    """Enumerate the corrected exact-valuation tuples, including zero slots."""
    _affine_inputs(local_prime, target, coefficient, a, b)
    if type(depth) is not int or depth < 0 or local_prime**(depth+1) > 100000:
        raise ValueError('nonnegative depth with at most100000 residues required')
    modulus = local_prime**(depth+1)

    def valuation(value):
        exponent = 0
        while exponent <= depth and value % local_prime == 0:
            value //= local_prime
            exponent += 1
        return exponent

    total = F(0)
    for residue in range(modulus):
        v1, v2 = valuation(residue), valuation(target-coefficient*residue)
        if max(v1, v2) <= depth and v1+v2 > 0:
            total += (F(a) if v1 else 1)*(F(b) if v2 else 1)
    return 1+total/modulus


def joint_box_budget(gamma, delta, c0, c1):
    if any(type(v) is not F for v in (gamma, delta, c0, c1)):
        raise ValueError('exact exponents required')
    if not F(5, 12) < gamma < F(1, 2) or not 0 < delta <= F(1, 4800):
        raise ValueError('saved unexceptional parameter range required')
    if not F(1, 4) < c0 <= c1 < 1-gamma/2:
        raise ValueError('fixed interior cofactor-exponent range required')
    return {
        'polynomial_norm_margin': c0-F(1, 4),
        'cofactor_cutoff_margin': c0-gamma/2,
        'outer_prime_margin': 1-c1-gamma/2,
        'class_epsilon_margin': F(1, 1200)-F(1, 2000),
        'bad_prime_saving': gamma/2-2*delta,
        'internal_power_saving': gamma/4-2*delta,
        'per_box_log_saving': F(1),
    }


def summed_box_log_power(box_count_log_power):
    """N=O(L^b) pays L^(b-1), relative to Y*S2; no hidden extra log."""
    if type(box_count_log_power) is not F or box_count_log_power < 0:
        raise ValueError('nonnegative exact logarithmic box-count exponent required')
    return box_count_log_power-1
