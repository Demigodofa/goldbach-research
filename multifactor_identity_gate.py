"""A multi-factor identity gate and a usable divisor-weighted Type I lemma.

Owner: Kevin's Goldbach research. Purpose: test whether a new decomposition
actually supplies missing free-variable length, while preserving a valid
weighted TI extension. Proof and exact guards only, not publication material.
Independent Sol theory and actual-file review: PASS, with its divisor-order
wording correction applied. Eight guards passed normal0.006s and -O0.005s.

QUESTION AND RESULT.
Does the Heath-Brown identity force every required term into existing TI
or free-variable reciprocal estimates? NO: an explicit top-order box has
all free variables bounded and all large variables Mobius-weighted. This
falsifies that TERMWISE treatment, not cancellation across the identity.
A positive result survives: the existing TI bound absorbs every FIXED
divisor weight, so genuinely long free-variable terms can be handled with
their actual grouped coefficients. The previously removed balanced
self-correlation and the remaining two correlations are unchanged.

EXACT IDENTITY AND SOURCE BOUNDARY.
1. Let u(n)=mu(n)1_(n<=z), v=mu-u, K>=1 fixed, and ell(n)=log n.
   Using Dirichlet convolution and its identity delta_1,
    HB_(K,z)=sum_(j=1..K)(-1)^(j-1)binom(K,j)
                                u^{*j}*1^{*(j-1)}*ell,
    Lambda-HB_(K,z)=v^{*K}*1^{*(K-1)}*ell.                 (1)
   Indeed u*1=delta_1-v*1, ell=Lambda*1, and the binomial
   polynomial on the first line is [delta_1-(v*1)^{*K}]*Lambda.
   With z=floor(Y^(1/K)), the residual vanishes on n<=Y.
   Primary check: Tao, A combinatorial subset sum problem associated with
   bounded prime gaps, equations(24)-(25) and following display,
   https://terrytao.wordpress.com/2013/06/10/a-combinatorial-subset-sum-problem-associated-with-bounded-prime-gaps/
   checked2026-09-09. Its parameter is Y=2x. Only the identity is used:
   its MPZ distribution estimates and Type I/II labels do not assert our
   fixed-target Goldbach correlation. This is unrelated to the previously
   excluded Notes7 Linnik argument or the inaccessible Heath-Brown1986 PDF.
2. An additional exact support observation: the residual in(1) is zero
   for n<2(z+1)^K, since each v-factor has integer argument>=z+1,
   the 1-factors have argument>=1, and ell(1)=0. This is a sufficient
   vanishing range, not a claim that its endpoint is always nonzero.
   At K=2,z=2,n=18 the residual is +log2 and HB=-log2. Thus an
   unrestricted all-n use of the truncated identity is false. Its
   logarithmic factor and all K-dependent binomial coefficients must stay.

A REAL SHORT-FREE BOX, WITH A LIMITED CONCLUSION.
3. For any fixed K>=2 and arbitrarily large odd prime p, take Y=3p^K.
   In the j=K term choose all K Mobius variables equal to p, all K-1
   plain1 variables equal to1, and the logarithmic variable equal to2.
   Then n=2p^K is in(Y/2,Y], every Mobius argument is below Y^(1/K),
   and this tuple contributes exactly -log2 after the HB sign.
   Localizing the Mobius variables to a fixed ratio interval near p and
   the free variables to their displayed bounded intervals still retains
   this term; log1 is not mistaken for a nonzero weight. At the exponent
   level, the K arithmetic variables each have size Y^(1/K), and all
   free variables have exponent0. The grouped arithmetic product index has
   size Y; the displayed ordered tuple's coefficient is -log2.
4. Selecting any genuine 1 or log factor as the free variable leaves a
   coefficient multiplier of exponent1, outside both d<=Y^gamma and
   the reviewed product cap51/100. Grouping some Mobius factors into a
   product near sqrt(Y) leaves arithmetic coefficients on BOTH products;
   neither becomes a smoothly weighted free integer. That is not the
   input of free_divisor_correlation.py or its older smooth MODEL.
   Even if one grants the same separate-coefficient Poisson setup at
   product exponents r=s=1, the complete BC budgets are E1=9/5 and
   E2=15/8. These failed upper-bound budgets are not lower bounds for
   the actual sum. The free-variable length cannot be manufactured by
   moving arithmetic factors across a multiplication sign.
5. Critically, n=2p^K is composite and the FULL HB sum is Lambda(n)=0.
   The nonzero localized term cancels with other HB terms. It is NOT a
   lower bound for the original Vaughan H or for an actual prime error.
   For example, squarefree integers whose prime factors are all<=W have
   Vaughan A(n)=0, since no divisor d>W has Lambda(d)!=0. With K>=5
   and every HB free variable bounded, those squarefree examples have
   no prime factor above W eventually. The raw expansion obstruction
   does not prove that a carefully combined, support-aware treatment fails.
   On a rough semiprime pq with p,q>W and Y^(1/K)<W, the Mobius
   variables in HB must instead equal1 and p,q enter free factors.
   Restricting those factors to such semiprime support would reintroduce
   prime/roughness conditions. One cannot impose that restriction and
   keep calling the factors unrestricted smooth weights.
   Thus only 'HB identity plus termwise existing estimates covers all
   boxes' is rejected. Cross-j cancellation and new arithmetic input remain
   available questions; no broad impossibility or coverage claim follows.

POSITIVE LEMMA: DIVISOR-WEIGHTED TYPE I IS ALREADY AVAILABLE.
6. Use the unexceptional ramanujan_type_i.py input, with fixed
   gamma=1/2-eps, 0<eps<1/12, delta<=1/4800, S=Y^delta, L=log(2Y),
   E=1_I(Lambda-Gamma_S). Set
    Delta_d=max_K |sum_(dk in J_m,k in K) E(m-dk)|,
    sum_(d<=Y^gamma)Delta_d <<_A Y/L^A for every fixed A.
   For fixed positive integer s and fixed b>=0, we now have
    sum_(d<=Y^gamma)tau_s(d)L^b Delta_d <<_(A,s,b) Y/L^A,   (2)
   where tau_s is the s-fold divisor function. These orders stay fixed
   as Y grows; (2) does not license an unbounded-depth Linnik expansion.
7. Here is a full cost for(2). Trivially the Lambda interval sum is
   O(YL/d). The Gamma_S progression mean is
    sum_(q|d)mu(q)G(log(q)/log(S))c_q(m)/phi(q),
   whose absolute value is O_G(tau(d)), since |c_q(m)|<=phi(q).
   Each component has bounded amplitude and period at most q<=S^2;
   the total incomplete-period error is O_G(S^4). Consequently
    Delta_d <<_G YL tau_2(d)/d+S^4.                        (3)
   Endpoint rounding is absorbed since d<=Y^gamma<Y.
8. For positive integers a,b, tau_a(n)tau_b(n)<=tau_(ab)(n).
   At a prime power this follows by mapping each pair of weak exponent
   compositions to a nonnegative a-by-b table with those row/column
   sums; choose one canonical table. Its marginals recover the pair, so
   the map is injective. Multiply over primes. Thus
    tau_s(d)^2 tau_2(d)<=tau_(2s^2)(d).
   Direct convolution counting also gives, for fixed h>=1,
    sum_(d<=D)tau_h(d)/d <= (1+log D)^h,
    sum_(d<=D)tau_h(d) <= D(1+log D)^(h-1).
   From(3), since gamma+4delta<1,
    sum_(d<=Y^gamma)tau_s(d)^2 Delta_d
      << Y L^(2s^2+1)+S^4 Y^gamma L^(s^2-1)
      << Y L^(2s^2+1).                                   (4)
9. Cauchy with the nonnegative Delta_d now yields
    (sum tau_s(d)Delta_d)^2
      <= (sum Delta_d)(sum tau_s(d)^2 Delta_d).
   Request input TI saving 2(A+b)+2s^2+1 and use(4); multiplication
   by L^b proves(2). This retains every divisor coefficient rather than
   incorrectly absorbing its maximum Y^epsilon into a logarithmic saving.

USEFUL HB COMPONENTS AND THE REMAINING TEST.
10. Group all but one genuinely free factor of a fixed-j HB term into
    d. The grouped coefficient is bounded by L*tau_(2j-1)(d); the L
    factor is absent from that coefficient if log is left free, with its
    variation paid separately. The divisor order stays2j-1. If the remaining
    1 or log factor has scale>=Y^(1-gamma+eta), for fixed eta>0,
    the product constraint forces d<<Y^(gamma-eta)<=Y^gamma eventually.
    Then(2), with fixed-smooth Abel for the physical and log weights,
    proves the ACTUAL correlation with E is O_A(Y/L^A). No independent
    prime-pair assertion is used. In particular, j=1 has d<=Y^(1/K)
    and is available for K>=3. Additional local smooth cutoffs with
    fixed or logarithmic derivative costs are paid by the same extra logs.
11. Another retained restricted component: for j>=2 choose one plain1
    factor and group the rest into
     alpha_j=mu_<=z^{*j}*1^{*(j-2)}*ell.
    This is an exact grouping with |alpha_j(M)|<=L*tau_(2j-1)(M).
    Truncate its complementary product scale to the reviewed range
    Y^gamma<=R<=Y^.51, and do the same independently on the other side.
    The BC proof extends to these actual separate coefficients: their
    L2 norms are <=sqrt(R)L^O_K(1) by the fixed divisor moments above.
    For direct Schwartz tails use tau_s(n)<<_(s,epsilon)n^epsilon.
    The fixed-smooth Poisson/Mellin proof and both exponent budgets then
    give the same error Y^(1983/2000+epsilon), with the actual signed gcd
    main kept. No extra cutoff on the chosen free1 factor is inserted.
    This is a norm-paid extension of the proof, not an assertion that
    its old literal |alpha|<=L hypothesis included all divisor weights.
12. The all-short-free corner prevents these two criteria from covering
    all HB terms by triangle. The next useful question is whether one can
    combine specific HB terms before estimating them so their cancellation
    removes that corner without reinstating an untreated prime or roughness
    indicator. The original C_F(Z,E-Z) and C_F(A-B,E) remain OPEN.

Finite helpers verify exact logarithmic identities, residual support,
nonzero localized tuples, divisor inequalities, and weighted-TI budgets.
They are neither a new prime scan nor experimental evidence for cancellation.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from math import comb, prod

from major_arc_kernel import _factorization, _mobius_phi
from unexceptional_vaughan_gate import _add, _clean, _divisors, _positive


def divisor_count(n, order):
    """Exact tau_order; order0 is the Dirichlet convolution identity."""
    _positive(n, 'n')
    if type(order) is not int or order < 0:
        raise ValueError('nonnegative integer divisor order required')
    if order == 0:
        return int(n == 1)
    return prod(comb(exponent+order-1, order-1) for _, exponent in _factorization(n))


@lru_cache(maxsize=None)
def _mobius_power(n, order, cutoff, high):
    if order == 0:
        return int(n == 1)
    return sum(_mobius_phi(d)[0]*_mobius_power(n//d, order-1, cutoff, high)
               for d in _divisors(n) if (d > cutoff) == high)


def _log_convolution(n, order, cutoff, high):
    vector = {}
    for a in _divisors(n):
        coefficient = _mobius_power(a, order, cutoff, high)
        if coefficient:
            for b in _divisors(n//a):
                _add(vector, _factorization(n//(a*b)), coefficient*divisor_count(b, order-1))
    return _clean(vector)


def heath_brown_log_vectors(n, order, cutoff):
    """All signed j terms plus the exact residual; valid for EVERY n."""
    for value, name in ((n, 'n'), (order, 'order'), (cutoff, 'cutoff')):
        _positive(value, name)
    terms = []
    for j in range(1, order+1):
        scalar = (-1)**(j-1)*comb(order, j)
        terms.append(tuple((p, scalar*c) for p, c in _log_convolution(n, j, cutoff, False)))
    return tuple(terms), _log_convolution(n, order, cutoff, True)


def localized_hb_term(mobius_arguments, free_arguments, log_argument, order, cutoff):
    """One actual ordered HB tuple, with all factors and the log weight retained."""
    for value, name in ((order, 'order'), (cutoff, 'cutoff'), (log_argument, 'log argument')):
        _positive(value, name)
    if type(mobius_arguments) is not tuple or type(free_arguments) is not tuple:
        raise ValueError('exact factor tuples required')
    j = len(mobius_arguments)
    if not 1 <= j <= order or len(free_arguments) != j-1:
        raise ValueError('require j Mobius and j-1 free factors with 1<=j<=order')
    for n in mobius_arguments+free_arguments:
        _positive(n, 'factor')
    if any(n > cutoff for n in mobius_arguments):
        raise ValueError('Mobius factor exceeds cutoff')
    scalar = (-1)**(j-1)*comb(order, j)*prod(_mobius_phi(n)[0] for n in mobius_arguments)
    value = tuple((p, scalar*e) for p, e in _factorization(log_argument) if scalar*e)
    return prod(mobius_arguments)*prod(free_arguments)*log_argument, value


@dataclass(frozen=True)
class WeightedTypeIBudget:
    moment_log_power: int
    required_input_log_saving: int
    resulting_log_saving: int


def weighted_type_i_budget(order, target_saving, coefficient_log_power=0):
    _positive(order, 'divisor order')
    for value in (target_saving, coefficient_log_power):
        if type(value) is not int or value < 0:
            raise ValueError('nonnegative integer logarithmic powers required')
    moment = 2*order*order+1
    return WeightedTypeIBudget(moment, 2*(target_saving+coefficient_log_power)+moment, target_saving)


def long_free_type_i(gamma, free_exponent):
    """Strict exponent margin; equality needs constants and is not certified."""
    if type(gamma) is not F or not F(5, 12) < gamma < F(1, 2):
        raise ValueError('exact gamma in(5/12,1/2) required')
    if type(free_exponent) is not F or not 0 <= free_exponent <= 1:
        raise ValueError('exact free exponent in[0,1] required')
    return 1-free_exponent < gamma
