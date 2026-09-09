"""Combined short HB terms and pruning the actual Vaughan prime-power slot.

Owner: Kevin's Goldbach research. Purpose: distinguish cancellation of
introduced decomposition terms from an estimate for the actual remainder.
Preserve a legal combined coefficient and an actual large-prime reduction.
Proof and finite guards only. Sol theory and actual-file review: PASS.

QUESTION AND DISPOSITION.
Does summing the short-free-variable Heath-Brown terms before triangle
remove their problematic coefficient? NO in the concrete sector below:
only the top-order term can survive, and an exact aggregate coefficient
is nonzero. Its cancellation in the full identity uses longer free factors.
A formal logarithmic-derivative factorization preserves bounded divisor
norms but does not estimate its correlation with E. The useful change of
direction is to prune the original Vaughan sum to actual LARGE PRIMES,
with a proved power-small error, and retain its exact sieve cofactor weight.

EXACT COMBINED SHORT COEFFICIENT.
1. Use the reviewed HB identity of multifactor_identity_gate.py. Let
   u=mu_<=z, w=1_<=T, ell_T(n)=w(n)log n, and fixed K>=2. Define
    S_(K,z,T)=sum_(j=1..K)(-1)^(j-1)binom(K,j)
                                  u^{*j}*w^{*(j-1)}*ell_T.      (1)
   This restricts ALL original free1 factors AND the logarithmic factor
   to arguments<=T, and combines the j terms before any estimate.
   Every j term has support n<=(zT)^j. Set z=floor(Y^(1/K)) and
   T=floor(Y^eta), with fixed 0<eta<1/[K(K-1)]. For n in(Y/2,Y]
   and sufficiently large Y, every j<K term vanishes, since
    (K-1)(1/K+eta)<1.
   Thus the WHOLE short sector on this interval is exactly
    S_(K,z,T)=(-1)^(K-1)u^{*K}*w^{*(K-1)}*ell_T.                (2)
   There is no cross-j cancellation inside this sector. When T<z, it
   is supported on z-smooth integers (all prime factors at most z).
2. This is stronger than the preceding localized-tuple witness. Take
   Y=3p^K, p an odd prime, z=floor(Y^(1/K)), and 2<=T<p. On
   n=2p^K, no free factor can contain p and each nonzero Mobius factor
   contains at most one p. Therefore j=K and all Mobius arguments are
   p (2p>z). The log argument is2 and the other free arguments are1.
   Consequently the EXACT combined coefficient is
    S_(K,z,T)(2p^K)=-log2,
   while Lambda(2p^K)=0. In the full HB identity, cancellation must
   come from outside the all-short sector. This is not a lower bound
   for an asymptotic correlation or for the original Vaughan remainder.

FORMAL FACTORIZATION WITH A PAID, FINITE INVERSE.
3. The Dirichlet inverse w^{-1} exists because w(1)=1. Define
    Lambda_T=w^{-1}*ell_T, V=delta_1-u*w.
   Pure finite coefficient algebra gives, for every n,
    S_(K,z,T)=[delta_1-V^{*K}]*Lambda_T.                        (3)
   Each term in(1) equals (u*w)^{*j}*Lambda_T; apply the binomial
   theorem. Lambda_T is the logarithmic derivative of the TRUNCATED
   divisor polynomial. It is not Lambda: for T=2, Lambda_T(4)=-log2,
   whereas Lambda(4)=+log2. Both Lambda_T and w^{-1} are supported
   on T-smooth integers, but V can carry primes up to z. In particular
   V(p)=1 for T<p<=z, which retains the witness in step2 through(3).
4. The inverse is not an uncontrolled infinite-depth object on our range.
   Write r=1_>T and b=mu*r. Then w=1*(delta_1-b), so exactly on n<=Y,
    w^{-1}=mu*sum_(k=0..J)b^{*k},
    J=max{j>=0:(T+1)^j<=Y}.                                 (4)
   Terms beyond J vanish by support. Since |b|<=tau_2,
    |w^{-1}(n)|<=(J+1)tau_(2J+1)(n),
    |Lambda_T(n)|<=(J+1)log(Y)tau_(2J+2)(n), n<=Y.             (5)
   For T=floor(Y^eta), J<1/eta, so these are FIXED divisor orders.
   This is a valid norm preservation fact. It does not turn either
   factor of(3) into an untouched free variable. Expanding(4) supplies
   factors longer than T only, not the Y^(1-gamma+epsilon) length
   needed by the reviewed TI criterion, and keeps a k=0 arithmetic term.
   Neither(3) nor(5) bounds C_F(S_(K,z,T),E). No smooth-number support
   or formal identity is substituted for that still-missing estimate.

ACTUAL SUPPORT REDUCTION: REMOVE INTERNAL PROPER PRIME POWERS.
5. Return to the unchanged unexceptional setup: gamma=1/2-eps,
   0<eps<1/12, delta<=1/4800, W=floor(Y^(gamma/2)), L=log(2Y),
   E=1_I(Lambda-Gamma_S), and fixed smooth physical weight F. The
   actual Vaughan sequence is A=mu_>W*Lambda_>W*1. Put
    P_W(d)=log(d)1_(d prime,d>W), A_p=mu_>W*P_W*1.
   Then
    sum_(n<=Y)|A(n)-A_p(n)| << Y W^(-1/2)L^3.                (6)
   Proof: triangle only over the omitted d=p^j>W,j>=2 tuples gives
    sum_(d=p^j>W,j>=2)log(p) sum_(a>W,ak<=Y/d)|mu(a)|
      <= YL sum_(p^j>W,j>=2)log(p)/p^j.
   The weighted count of proper prime powers <=X is O(sqrt(X)log^2(2X)):
   sum over 2<=j<=log_2 X and use the elementary integer bound for p.
   A dyadic summation above W therefore bounds the last reciprocal tail
   by O(W^(-1/2)log^2(2W)). This proves(6). It also bounds any subset
   of these tuples, including restricted product-coefficient boxes.
6. The existing model bound |E|<<L+S^2, S=Y^delta, implies the ACTUAL
   target-uniform estimate
    |C_F(A-A_p,E)| <<_F Y^(1-gamma/4+2delta+o(1))=o(Y).       (7)
   The fixed margin gamma/4-2delta is positive throughout the allowed
   regime. This removes proper prime powers in the INTERNAL Lambda(d)
   slot; it is distinct from the already paid outer prime-power error.
   The same positive tuple bound handles any selected final support set.
   In particular A_p(n)=0 whenever every prime factor of n is<=W, so
   the actual Vaughan correlation restricted to such final n is small
   by(7). This is an estimate for the actual sum, not for HB short terms.
7. Keep slot and final-variable support distinct. For K>=5 and the eta
   in step1, eventually T<z<W. If HB is inserted into the internal
   Lambda(d) slot, its all-short argument d is z-smooth. The FULL
   Lambda(d), d>W, can then be nonzero only on proper prime powers;
   their aggregate is already removed by(7). But the final n=adk need
   not be z-smooth, since a or k can contain large primes.
   This explains why the raw HB obstacle need not carry main A_p mass.
   It does NOT justify discarding individual HB short terms without the
   compensating terms, or discarding the short sector when HB expands
   Lambda in the PARTNER E. Imposing a prime/smoothness support mask
   on decomposed variables also changes their free-weight hypotheses.

THE EXACT LARGE-PRIME/COFACTOR CORRELATION THAT REMAINS.
8. Define S_W(c)=sum_(a|c,a<=W)mu(a). For each prime divisor p>W,
    sum_(a|n/p,a>W)mu(a)=1_(n=p)-S_W(n/p).
   Therefore exactly
    A_p(n)=sum_(p|n,p>W)log(p)[1_(n=p)-S_W(n/p)]
          =-sum_(pc=n,p>W prime,c>W)log(p)S_W(c).             (8)
   The second equality uses S_W(1)=1 and S_W(c)=0 for 1<c<=W.
   In particular primes have A_p=0, rough distinct semiprimes pq have
   A_p(pq)=-log(pq), and a prime square p^2 with p>W has -log p.
   No prime divisor is counted once per exponent; the p-sum is over
   distinct prime divisors. The coefficient S_W(c) is signed in general.
9. Combining(7)-(8), the original smoothed remainder is
    T_F=-sum_(p>W prime,c>W)log(p)S_W(c)
             *F(pc/Y,(m-pc)/Y)E(m-pc)
          +O_F(Y^(1-gamma/4+2delta+o(1))).                   (9)
   Both linked conditions remain actual: p is prime and E contains
   Lambda(m-pc). Equation(9) does not prove their signed correlation is
   small. It is a better target for a new arithmetic estimate than trying
   to remove a raw HB term that cancels outside the actual prime slot.
   The balanced projection theorem and its two remaining correlations,
   fixed divisor-weighted TI, polynomial tools and conditional coverage
   remain valid. No new prime-pair coverage follows from this pursuit.

Finite routines verify the combined coefficient, finite inverse, support
and actual prime-slot formula. They do not test asymptotic cancellation.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import comb

from major_arc_kernel import _factorization, _mobius_phi
from multifactor_identity_gate import _mobius_power
from unexceptional_vaughan_gate import _add, _clean, _divisors, _positive


@lru_cache(maxsize=None)
def _short_ones(n, order, cutoff):
    if order == 0:
        return int(n == 1)
    return sum(_short_ones(n//d, order-1, cutoff) for d in _divisors(n) if d <= cutoff)


def short_hb_vectors(n, order, mobius_cutoff, free_cutoff):
    """Exact signed j terms with every original free/log factor truncated."""
    for value in (n, order, mobius_cutoff, free_cutoff):
        _positive(value, 'argument')
    result = []
    for j in range(1, order+1):
        vector = {}
        scalar = (-1)**(j-1)*comb(order, j)
        for a in _divisors(n):
            mu = _mobius_power(a, j, mobius_cutoff, False)
            if mu:
                for ell in _divisors(n//a):
                    if ell <= free_cutoff:
                        _add(vector, _factorization(ell),
                             scalar*mu*_short_ones(n//(a*ell), j-1, free_cutoff))
        result.append(_clean(vector))
    return tuple(result)


@lru_cache(maxsize=None)
def cutoff_inverse(n, cutoff):
    """Exact Dirichlet inverse of 1_(n<=cutoff), not an inverse of Lambda."""
    _positive(n, 'n')
    _positive(cutoff, 'cutoff')
    if n == 1:
        return 1
    return -sum(cutoff_inverse(n//d, cutoff) for d in _divisors(n) if 1 < d <= cutoff)


def cutoff_log_vector(n, cutoff):
    _positive(n, 'n')
    _positive(cutoff, 'cutoff')
    vector = {}
    for d in _divisors(n):
        if d <= cutoff:
            _add(vector, _factorization(d), cutoff_inverse(n//d, cutoff))
    return _clean(vector)


@lru_cache(maxsize=None)
def _defect_power(n, order, mobius_cutoff, free_cutoff):
    if order == 0:
        return int(n == 1)
    result = 0
    for d in _divisors(n):
        defect = int(d == 1)-sum(_mobius_phi(a)[0] for a in _divisors(d)
                                 if a <= mobius_cutoff and d//a <= free_cutoff)
        if defect:
            result += defect*_defect_power(n//d, order-1, mobius_cutoff, free_cutoff)
    return result


def combined_short_vector(n, order, mobius_cutoff, free_cutoff):
    """Independent coefficient calculation via (delta-V^K)*Lambda_T."""
    for value in (n, order, mobius_cutoff, free_cutoff):
        _positive(value, 'argument')
    vector = dict(cutoff_log_vector(n, free_cutoff))
    for d in _divisors(n):
        _add(vector, cutoff_log_vector(n//d, free_cutoff),
             -_defect_power(d, order, mobius_cutoff, free_cutoff))
    return _clean(vector)


def inverse_depth(limit, cutoff):
    _positive(limit, 'limit')
    _positive(cutoff, 'cutoff')
    depth, minimum = 0, 1
    while minimum*(cutoff+1) <= limit:
        depth += 1
        minimum *= cutoff+1
    return depth


def cofactor_sieve_sum(n, cutoff):
    _positive(n, 'n')
    _positive(cutoff, 'cutoff')
    return sum(_mobius_phi(d)[0] for d in _divisors(n) if d <= cutoff)


def prime_slot_log_vector(n, cutoff):
    """Exact A_p, summing each actual prime divisor only once."""
    _positive(n, 'n')
    _positive(cutoff, 'cutoff')
    return tuple((p, int(n == p)-cofactor_sieve_sum(n//p, cutoff))
                 for p, _ in _factorization(n) if p > cutoff
                 and int(n == p)-cofactor_sieve_sum(n//p, cutoff))


def internal_power_margin(gamma, delta):
    if type(gamma) is not F or not F(5, 12) < gamma < F(1, 2):
        raise ValueError('exact gamma in(5/12,1/2) required')
    if type(delta) is not F or not 0 < delta <= F(1, 4800):
        raise ValueError('exact delta in(0,1/4800] required')
    return gamma/4-2*delta
