"""Fixed-target prime-factor moments: the exact deficit and its endpoint.

Owner: Kevin's Goldbach research. Purpose: test whether largest-prime-factor
information supplies the missing signed estimate, and preserve the exact
input a future arithmetic method must improve. No manuscript or novelty
claim. The classical parity example below is applied, not rediscovered.
Independent Sol theory/actual-file review PASS after explicitly recording
all parts of the source's local-density condition(B). Seven exact tests
pass normal0.008s/-O0.006s. A vacuous wrong-sign fixture with H(10)=0 was
replaced by the nonzero H(9)=-1 fixture; no mathematical claim changed.

ASYMMETRIC CUTOFF AND THE PRECISE ONE-SIDED TARGET.
1. Retain the saved unexceptional TI setup, gamma in(5/12,1/2), model
   delta<=1/4800, and fixed nonnegative smooth F compact in(.5,1)^2.
   Put U=floor(Y^gamma), lambda=delta_1 (so V=1), L=logY and
    B_U(n)=sum_(p|n,p>U prime)logp,
    P(n)=logn*1_(n prime), C_U(n)=1_(n composite)B_U(n).
   On the physical n>U, exactly B_U=P+C_U. The full internal layer is
    sum_(b|n,b>U)Lambda(b)=logn-sum_(b|n,b<=U)Lambda(b).     (1)
   Against E=1_I(Lambda-Gamma_S), the right side is TI-small, with one
   Abel logarithm and moduli b<=U<=Y^gamma. The saved positive tuple
   pruning bounds the L1 difference from B_U by Y U^(-1/2)L^3. Hence
    C_F(B_U,E)=O_A(Y/L^A),                                (2)
   since its power error is Y^(1-gamma/2+2delta+o(1)). This is a direct
   application of optimized_cofactor_cutoff.py with an asymmetric cutoff,
   not a new distribution input. The actual prime remainder is -C_U;
   its correlation is still the unresolved prime compensation.
2. Define three actual moments and the EXACT model moment:
    A_B=sum_n B_U(n)Lambda(m-n)F(n/Y,(m-n)/Y),
    A_C=sum_n C_U(n)Lambda(m-n)F(n/Y,(m-n)/Y),
    G_F=sum_(n,q prime,n+q=m)logn logq F(n/Y,q/Y),
    M_B=sum_n B_U(n)Gamma_S(m-n)F(n/Y,(m-n)/Y).
   The physical support is implicit throughout. By(2), A_B=M_B+O_A(Y/L^A).
   Also A_B-A_C is the first-prime/partner-Lambda mass EXACTLY. Replacing
   the partner by primes costs O_F(Y^(1/2)L^3). Therefore
    G_F=M_B-A_C+O_A(Y/L^A).                               (3)
   A sufficient new estimate would be, uniformly at the desired targets,
    A_C <= M_B-kappa Y S_2(m), kappa>0 fixed.              (4)
   The identity(3) does NOT prove(4). Bounding the COMPLETE B_U moment
   again only repeats TI; restricting to composites restores the gap.
   Even positivity of M_B-A_C at a useful quantitative margin is open.
3. Keep M_B exact for this test. Its leading scale can be computed using
   the elementary all-modulus Gamma comparison in
   factored_prime_ap_transfer.py, steps6-7, at h<=U. Let
    I_F=int F(v,m/Y-v)dv, J_F=int F(v,m/Y-v)logv dv,
    K_U(m)=sum_(h<=U,(h,m)=1)Lambda(h)/phi(h).
   The full Gamma mean in the h progression is h/phi(h) if(h,m)=1 and0
   otherwise; the truncated nonreduced errors are paid in that module.
   Using(1), with the prime-power pruning and coefficient bound Lambda(h)<=L,
    M_B=Y I_F(L-K_U(m))+Y J_F+O_A(Y/L^A).                 (5)
   The period and tail errors remain power-small since U S^4<Y.
   Ordinary PNT gives sum_(h<=U)Lambda(h)/phi(h)=logU+O(1). Omitting a
   prime p|m removes at most p logp/(p-1)^2. Summing p<=logY costs
   O(loglogY), and p>logY costs O(logm/logY). Thus uniformly for m~Y,
    M_B=(1-gamma)I_F YL+O_F(Y loglogY).                   (6)
   For I_F>0, the benchmark moment is order YL whereas(4) needs an
   additive Y S_2 margin. Formula(6) is too coarse to decide that margin;
   it cannot replace the exact model moment in(4).

WHY A FIXED POWER OF THE LARGEST PRIME FACTOR DOES NOT REACH THIS GAP.
4. For EVERY odd n in(Y/2,Y], Y>4, exactly
    n is prime  <=>  P^+(n)>Y/3.                         (7)
   A composite odd n has cofactor n/P^+(n)>=3, so its largest prime is
   at most n/3<=Y/3. A prime in this interval is larger than Y/2.
   Consequently the B_(floor(Y/3)) moment against the actual prime
   partner is EXACTLY G_F. The threshold in(7) lies outside the old TI
   range, and just renaming it a largest-prime-factor tail proves nothing.
   For any fixed theta<1, Y^theta<Y/3 eventually. Choose arbitrarily
   large odd primes p, Y=4p and n=3p. Then n is an odd composite in the
   physical interval, with P^+(n)=p>Y^theta eventually. This is a factor-
   threshold witness, not a claim about a fixed-target prime partner.
   No lower bound on the actual fixed-m family 3p+q=m is asserted.
   Balanced distinct semiprimes with both factors>U additionally have
   B_U(n)=logn exactly, so this additive factor statistic by itself does
   not distinguish them from primes. The earlier absolute obstruction
   and all polynomial tools retain their original scopes.

EVEN FULL FIXED-SCALE FACTOR STATISTICS CAN MISS ALL PRIMES.
5. There is a stronger diagnostic using the CLASSICAL sieve parity
   sequence, not the actual shifted primes. Write ell(n)=(-1)^Omega(n)
   for Liouville (not the cutoff lambda and not lambda_chi=1*chi), and
    a_n=1+ell(n), H(x)=sum_(n<=x)ell(n).
   Then 0<=a_n<=2 but a_p=0 at EVERY prime. Complete multiplicativity
   gives exact finite formulas
    N(x)=floor(x)+H(x),
    N_d(x)=floor(x/d)+ell(d)H(x/d).                       (8)
   Primary input: Tao2014 Notes2, Exercise41, gives the classical strong
   summatory-Mobius bound. From ell(n)=sum_(r^2|n)mu(n/r^2), sum first
   over r<=x^(1/4) and then over the remaining r. The first part is
   O_A(x/log(x)^A) for every fixed A; the second is O(x^(3/4)). Hence
    H(x)=O_A(x/log(x)^A).                                (9)
   For every FIXED 0<c<1, (8) implies
    sum_(d<=x^c)|N_d(x)-N(x)/d|
      <=x^c+sum_(d<=x^c)|H(x/d)|+|H(x)|sum_(d<=x^c)1/d
      <<_(A,c) x/log(x)^A.                              (10)
   Uniformity uses x/d>=x^(1-c); choose extra log saving before summing.
   Thus a has index1 and level1 in the definition of Bharadwaj--Rodgers,
   with g(d)=1/d. This g is multiplicative, lies in[0,1], satisfies their
   growth condition with C=1, and sum_(p<=x)g(p)logp=logx+O(1) by
   ordinary PNT/Mertens, paying the other parts of their condition(B).
   Their remaining congruence bound follows immediately
   from a_n<=2 and N(x)~x. Their Theorem7 therefore gives this sequence
   the same fixed-dimensional normalized large-factor limits as the
   Poisson--Dirichlet process, while its prime event has probability ZERO.
   This is an application of their theorem and the known parity example;
   it makes no claim that a equals Lambda-Gamma or reflected prime data.
   In particular its local densities are not those of the prime partner.
6. Level1 in(10) means EVERY FIXED c<1, not c=1 or a moving cutoff near1.
   The failure at the endpoint is visible without conjectures: for primes
   d in(x/2,x], N_d(x)=a_d=0. PNT gives order x/logx such d and N(x)/d>=1/2
   eventually, so the full sum through d=x is at least order x/logx.
   It cannot have arbitrary logarithmic saving. Likewise weak convergence
   of factor statistics does not permit a cutoff moving to1 on a 1/logY
   scale. This rules out that abstract inference; it does not rule out
   quantitative estimates using the defining relation n=m-q with q prime.

PRIMARY SOURCES CHECKED 2026-09-09.
- A. Bharadwaj and B. Rodgers, Large prime factors of well-distributed
  sequences, Cambridge online17April2026, section1.2(A)-(C), Theorem7:
  https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/large-prime-factors-of-welldistributed-sequences/270043D7BAB4CDA2A601A061FB482AA0
  Its Proposition2 concerns a FIXED shift of the primes; no uniform m~Y
  statement is imported. Theorem7 is used only for the verified parity a.
- Tao, 254A Notes2, Exercise41 (Mobius), Exercise3(ii) (Liouville series),
  Corollary39/Exercise40 (ordinary PNT), NOT the excluded Notes7 result:
  https://terrytao.wordpress.com/2014/12/09/254a-notes-2-complex-analytic-multiplicative-number-theory/
- R. Li, arXiv:2508.18285v1, Theorem1 and section2 equations(6)-(16):
  https://arxiv.org/html/2508.18285v1
  It reports a fixed-shift largest-factor exponent .679-epsilon via
  average Brun--Titchmarsh bounds. Neither moving-target uniformity nor
  the cofactor-one endpoint is supplied. No numerical sieve integral or
  new prime estimate from that preprint is used as a proved input here.

DISPOSITION AND NEXT CONCRETE QUESTION.
The unweighted full log-factor route is a restatement of the open estimate;
fixed-power tails and even full weak factor laws do not repair it. Keep
the exact deficit(4), the asymmetric reduction and all earlier polynomial
identities. A new input must distinguish the linked-prime sequence from
the parity example at the required scale. Next test: on cubic-rough
n=m-q, write the exact signed Liouville/prime-partner correlation, then
check whether a primary correlation theorem controls its unaveraged,
moving-target sum. Recover the old factored_linear_barrier.py identity
first; do not repeat its failed one-dimensional sieve substitution.
Any logarithmically averaged or fixed-shift statement must retain its
quantifiers. This next correlation test is not performed here. Goal open.

Finite routines below guard algebra, multiplicities and support only;
they are not experiments establishing any asymptotic prime correlation.
"""
from fractions import Fraction as F
from math import isqrt

from major_arc_kernel import _factorization, _mobius_phi
from unexceptional_vaughan_gate import _add, _clean, _divisors, _positive, mangoldt_log_vector


def liouville(n):
    _positive(n, 'n')
    return (-1)**sum(exponent for _, exponent in _factorization(n))


def liouville_square_pair(n):
    _positive(n, 'n')
    return liouville(n), sum(_mobius_phi(n//(r*r))[0] for r in range(1, isqrt(n)+1) if n % (r*r) == 0)


def factor_moment_vectors(n, cutoff):
    """B_U, its composite part, its prime part, and independent compensation."""
    _positive(n, 'n')
    _positive(cutoff, 'cutoff')
    if n <= cutoff:
        raise ValueError('physical first variable must exceed the cutoff')
    factors = _factorization(n)
    large = tuple((p, 1) for p, _ in factors if p > cutoff)
    is_prime = factors == ((n, 1),)
    compensation = dict(factors)
    for b in _divisors(n):
        is_proper_power = len(_factorization(b)) == 1 and _factorization(b)[0][1] >= 2
        if b <= cutoff or is_proper_power:
            _add(compensation, mangoldt_log_vector(b), -1)
    return large, (() if is_prime else large), (large if is_prime else ()), _clean(compensation)


def odd_prime_endpoint(n, y):
    """Return the largest-factor test; deliberately reject even/outside inputs."""
    _positive(n, 'n')
    _positive(y, 'Y')
    if y <= 4 or n % 2 == 0 or not y < 2*n <= 2*y:
        raise ValueError('odd n in (Y/2,Y] and Y>4 required')
    return 3*_factorization(n)[-1][0] > y


def prime_partner_moments(y, target, cutoff):
    """Exact log-polynomial B, composite, Goldbach and Y/3-tail moments.

    F is replaced by1 on the physical interval for this finite fixture.
    Keys (p,q) represent log(p)log(q), sorted to preserve commutativity.
    """
    _positive(y, 'Y')
    _positive(target, 'target')
    _positive(cutoff, 'cutoff')
    if target % 2 or not 1 <= cutoff < y//2 or y <= 4:
        raise ValueError('even target, Y>4, and cutoff<floor(Y/2) required')
    total, composite, pairs, endpoint = {}, {}, {}, {}
    for n in range(y//2+1, y+1):
        q = target-n
        if not y < 2*q <= 2*y or _factorization(q) != ((q, 1),):
            continue
        large, comp, prime, _ = factor_moment_vectors(n, cutoff)
        for output, terms in ((total, large), (composite, comp), (pairs, prime)):
            for p, coefficient in terms:
                key = tuple(sorted((p, q)))
                output[key] = output.get(key, 0)+coefficient
        for p, _ in _factorization(n):
            if 3*p > y:
                key = tuple(sorted((p, q)))
                endpoint[key] = endpoint.get(key, 0)+1
    return tuple(tuple(sorted(v.items())) for v in (total, composite, pairs, endpoint))


def parity_multiples(x, divisor):
    """Direct and exact multiplicative formulas for a_n=1+Liouville(n)."""
    _positive(x, 'x')
    _positive(divisor, 'divisor')
    direct = sum(1+liouville(n) for n in range(divisor, x+1, divisor))
    h = sum(liouville(k) for k in range(1, x//divisor+1))
    return direct, x//divisor+liouville(divisor)*h


def parity_level_error(x, level):
    """Finite total error and the analytic proof's exact triangle majorant."""
    _positive(x, 'x')
    _positive(level, 'level')
    if level > x:
        raise ValueError('level must not exceed x')
    h = [0]
    for n in range(1, x+1):
        h.append(h[-1]+liouville(n))
    total = x+h[x]
    direct = sum((abs(F(parity_multiples(x, d)[0])-F(total, d)) for d in range(1, level+1)), F(0))
    majorant = level+sum(abs(h[x//d]) for d in range(1, level+1))
    majorant += abs(h[x])*sum((F(1, d) for d in range(1, level+1)), F(0))
    return direct, majorant
