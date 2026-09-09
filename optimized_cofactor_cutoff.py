"""Exact cutoff freedom, classical optimal cofactor norm, and its paid budget.

Owner: Kevin's Goldbach research. Purpose: decide whether changing the actual
Vaughan cutoff makes norm-only Cauchy sufficient. Preserve the usable cutoff
freedom and the precise missing covariance, not a new manuscript or sieve claim.
Independent Sol theory and actual-file review: PASS, no correction required.

QUESTION AND RESULT.
Can a smoothed Mobius cutoff lower the actual cofactor second moment enough
to control its linked prime correlation using only separate second moments?
The tested route does not close: even the optimal finite divisor weight has
mean square of order1/log V, and the paid balanced-box bound is O(Y sqrt L).
This is a limitation of THIS upper-bound calculation, not a lower bound for
the actual correlation or an obstruction to using these weights with new
arithmetic input. Retain the cutoff identity and optimizer; reactivate the
norm route only with a stronger joint moment or signed covariance estimate,
not another cutoff shape in the same family. The classical Selberg minimum
is not new mathematics.

EXACT CUTOFF FREEDOM, INCLUDING COMPENSATION.
1. Retain the unexceptional setup and fixed smooth physical F in the prior
   modules. For any real sequence lambda supported d<=V with lambda(1)=1
   and |lambda(d)|<=1, define
    R_lambda=(mu-lambda)*Lambda_>U*1.
   Exactly, for every integer n,
    Lambda=Lambda_<=U+lambda*log-lambda*Lambda_<=U*1+R_lambda. (1)
   Indeed (mu-lambda)*Lambda_>U*1=Lambda_>U-lambda*Lambda_>U*1;
   use Lambda*1=log. No omitted boundary or smoothing compensation remains.
   For U,V<=Y^gamma and UV<=Y^gamma, the two lambda terms in(1) have
   correlations O_A(Y/L^A) with the unchanged E. Abel pays log; the grouped
   third coefficient has magnitude at most sum_(b|d)Lambda(b)=log d and
   support d<=UV. The first term vanishes on the physical support eventually.
   Thus replacing the hard cutoff by ANY such lambda changes the remainder
   correlation by O_A(Y/L^A), uniformly in lambda. This is actual TI transfer.
2. Since |mu-lambda|<=2, the positive prime-power tuple proof of
   short_free_cancellation.py still gives, for the internal prime restriction,
    sum_(n<=Y)|R_lambda-R_lambda,p|(n)<<Y U^(-1/2)L^3.
   With U=V=floor(Y^(gamma/2)), its correlation error remains
    O(Y^(1-gamma/4+2delta+o(1)))=o(Y).
   Define S_lambda(c)=sum_(d|c)lambda(d). Then EXACTLY
    R_lambda,p(n)=sum_(p|n,p>U)log p [1_(n=p)-S_lambda(n/p)]
                =-sum_(pc=n,p>U prime,c>=2)log p S_lambda(c). (2)
   The prime sum is over distinct prime divisors. General lambda does NOT
   imply S_lambda(c)=0 for 2<=c<=V: unlike the hard cutoff, it can introduce
   small cofactors. Their TOTAL compensation is covered by(1); they cannot
   be dropped termwise. Squaring S_lambda to make a positive sieve weight
   would change(2) and is not licensed by the norm optimization below.

EXACT NORM OPTIMIZATION, WITH INTERVAL ERROR.
3. For C>0 write M_lambda(C)=sum_(C<c<=2C)S_lambda(c)^2. Finite expansion gives
    M_lambda(C)=C Q(lambda)+O(||lambda||_1^2),
    Q(lambda)=sum_(d,e<=V)lambda(d)lambda(e)/[d,e].            (3)
   The error constant can be1: each count differs from C/[d,e] by less1.
   Since |lambda|<=1, the error is at most V^2. It cannot be ignored when
   C is short. Put y_r=sum_(r|d,d<=V)lambda(d)/d. Using
   gcd(d,e)=sum_(r|d,r|e)phi(r), and finite dual Mobius inversion,
    Q=sum_(r<=V)phi(r)y_r^2,
    lambda(1)=sum_(r<=V)mu(r)y_r=1.
   Cauchy gives the EXACT minimum over all real supported lambda,
    Q>=1/G(V), G(V)=sum_(r<=V)mu(r)^2/phi(r).                 (4)
   Equality is attained at y_r=mu(r)/(phi(r)G(V)), hence
    lambda_d^*=mu(d)d/phi(d)*G_d(V/d)/G(V),
    G_d(x)=sum_(r<=x,(r,d)=1)mu(r)^2/phi(r).                  (5)
   The minimizer is supported on squarefrees and obeys |lambda_d^*|<=1:
   for squarefree d, the distinct terms er, e|d, r<=V/d, (r,d)=1 give
    G(V)>=[sum_(e|d)1/phi(e)]G_d(V/d)=(d/phi(d))G_d(V/d).
   Thus it is legal in(1), and the unrestricted minimum also applies to
   any smaller bounded, smoothed, or polynomial-cutoff family.
4. This is the classical Selberg quadratic minimum. Primary check:
   Steve Lester, An Introduction to the Selberg Sieve, May1,2015,
   proof printedpp5-7 (especially the reciprocal minimum onp6),
   https://www.math.tau.ac.il/~rudnick/courses/sieves2015/SelbergSieve_first_application.pdf
   The normalization is independently derived above; no prime-correlation
   theorem or lower-bound sieve is imported from that source.
   The elementary size G(V) asymp log(2V) suffices here. For the lower bound,
   nonsquarefree n<=x are covered by multiples of d^2,d>=2, whose count is
   at most x sum_(d>=2)d^-2 <(3/4)x. For large x the remaining squarefree
   count is at least x/8. Partial summation of sum mu^2(n)/n then gives
   G(V)>>log(2V). For the upper bound use
    n/phi(n)=sum_(d|n)mu^2(d)/phi(d),
    sum_(n<=V)1/phi(n)<=(1+log V)sum_(d>=1)1/(d phi(d))<<log(2V).
   The last series converges by phi(d)>=sqrt(d/2), checked prime-powerwise.
   Consequently if C~sqrt Y and V=floor(Y^(gamma/2)), gamma<1/2 fixed,
    inf_(lambda1=1,|lambda|<=1) M_lambda(C) asymp C/log V.     (6)
   Indeed the uniform endpoint error V^2=o(C/log V), and(4)-(5) bound
   this infimum from both sides. We do NOT claim(6) for all short cofactors.
   At V=3 the optimizer is(1,-4/5,-3/5); S(2)=1/5 and S(6)=-2/5.
   It remains signed and introduces c=2. At V=2 the minimum is1/2, not2.

PAY THE PARTNER NORM AND PRIME WEIGHTS.
5. For the unchanged E=1_I(Lambda-Gamma_S), one has
    sum_n |E(n)|^2 <<_G Y L.                                (7)
   Proof: Lambda(n)^2<=L Lambda(n) and the elementary Chebyshev bound
   sum_(n<=Y)Lambda(n)<<Y. Write Gamma_S=sum_(q<=S^2)a_q c_q,
   a_q=mu(q)G(log q/log S)/phi(q). Each normalized component is O_G(1).
   Ramanujan orthogonality over a complete common period makes the mean
   square sum_q |a_q|^2 phi(q)<<sum_(q<=S^2)1/phi(q)<<log(2S).
   For every pair the period is <=S^4 and its amplitude O_G(1); summing
   incomplete-period errors over at most S^4 pairs costs O_G(S^8).
   Since 8delta<1, this proves(7) by |Lambda-Gamma|^2<=2Lambda^2+2Gamma^2.
   All shifts, physical intervals and bounded F only decrease the needed
   unrestricted positive majorants, up to ||F||_infinity constants.
6. On one balanced box p~P, c~C, P C~Y and P,C~sqrt Y, set
    T_box=sum_(c,p prime>U) S_lambda(c)log p F(pc/Y,(m-pc)/Y)E(m-pc).
   Pairwise weighted Cauchy gives
    |T_box|^2 <= [sum_(c,p)S_lambda(c)^2 log p]
                 *[sum_(c,p)log p |F E(m-pc)|^2]
               <<_F P M_lambda(C)*Y L^2.                    (8)
   The first factor uses Chebyshev sum_(p~P)log p<<P. For the second,
   sum_(p|n)log p<=log n<=L, followed by(7). All masks stay in the
   exact inequality and may be dropped only in these positive bounds.
   For the optimal weights,(6) makes(8) only
    |T_box|<<Y sqrt L.                                      (9)
   This upper-bound budget already fails to give o(Y) for one box.
   Additional dyadic summations do not repair it. The lower bound(4)
   prevents further improvement of its asymptotic coefficient norm alone
   within this family. It does NOT prove the correlation is this large,
   or exclude a sharper correlated second factor or a one-sided method.

THE ARITHMETIC ENERGY STILL NEEDED.
7. Keeping the prime sum intact before Cauchy instead gives
    |T_box|^2<=M_lambda(C) H,
    H=sum_(c~C)|sum_(p~P prime>U)log p F(pc/Y,(m-pc)/Y)E(m-pc)|^2. (10)
   On the balanced optimized range, a SUFFICIENT bound is
    H<<Y^2/(C L^5).                                        (11)
   It yields |T_box|<<Y/L^3, enough even for O(L^2) such boxes. This is
   neither necessary nor established. Its diagonal IS small: the number
   of prime divisors p>U of n<=Y is O_gamma(1), so(7) gives
    H_diag<<Y L^3=o(Y^2/(C L^5))
   for C~sqrt Y. Only a suitable one-sided upper bound on the weighted
   off-diagonal is missing for this energy route. It retains the primes
   p_1,p_2 and q_i=m-c p_i, with
    p_2 q_1-p_1 q_2=(p_2-p_1)m.
   No independence, cancellation, or sign is inferred from this relation.
   Short/unbalanced cofactors, the earlier mixed remainder, all model/TI
   scope and the actual-zero conditional coverage remain as previously
   recorded. No new prime-pair coverage follows from this pursuit.

Finite routines guard the exact identity, optimizer, interval count and
Gram diagonal. They are not experiments testing asymptotic prime cancellation.
"""
from fractions import Fraction as F
from math import gcd, lcm

from major_arc_kernel import _factorization, _mobius_phi, ramanujan
from unexceptional_vaughan_gate import _add, _clean, _divisors, _positive, mangoldt_log_vector


def _weights(weights):
    values = tuple(weights)
    if len(values) < 2 or values[0] != 0 or values[1] != 1:
        raise ValueError('weights indexed from0, with lambda0=0 and lambda1=1')
    if any(type(v) not in (int, F) or abs(v) > 1 for v in values):
        raise ValueError('exact bounded weights required')
    return tuple(F(v) for v in values)


def optimal_cutoff(cutoff):
    """Classical exact finite Selberg optimizer, including index0."""
    _positive(cutoff, 'cutoff')
    g = sum((F(_mobius_phi(r)[0]**2, _mobius_phi(r)[1]) for r in range(1, cutoff+1)), F(0))
    result = [F(0)]
    for d in range(1, cutoff+1):
        mu, phi = _mobius_phi(d)
        coprime_g = sum((F(_mobius_phi(r)[0]**2, _mobius_phi(r)[1])
                         for r in range(1, cutoff//d+1) if gcd(r, d) == 1), F(0))
        result.append(F(mu*d, phi)*coprime_g/g)
    return tuple(result), 1/g


def cofactor_weight(n, weights):
    _positive(n, 'n')
    weights = _weights(weights)
    return sum((weights[d] for d in _divisors(n) if d < len(weights)), F(0))


def cutoff_vaughan_vectors(n, lambda_cutoff, weights):
    """Four signed EXACT convolution terms for an arbitrary bounded cutoff."""
    _positive(n, 'n')
    _positive(lambda_cutoff, 'Lambda cutoff')
    weights = _weights(weights)
    low = dict(mangoldt_log_vector(n)) if n <= lambda_cutoff else {}
    linear, subtraction, remainder = {}, {}, {}
    for a in _divisors(n):
        lam = weights[a] if a < len(weights) else F(0)
        _add(linear, _factorization(n//a), lam)
        for d in _divisors(n//a):
            if d <= lambda_cutoff:
                _add(subtraction, mangoldt_log_vector(d), -lam)
            else:
                _add(remainder, mangoldt_log_vector(d), _mobius_phi(a)[0]-lam)
    return tuple(_clean(v) for v in (low, linear, subtraction, remainder))


def cutoff_prime_vector(n, lambda_cutoff, weights):
    _positive(n, 'n')
    _positive(lambda_cutoff, 'Lambda cutoff')
    weights = _weights(weights)
    return _clean({p: int(n == p)-cofactor_weight(n//p, weights)
                   for p, _ in _factorization(n) if p > lambda_cutoff})


def cutoff_quadratic(weights):
    weights = _weights(weights)
    return sum((weights[d]*weights[e]/lcm(d, e)
                for d in range(1, len(weights)) for e in range(1, len(weights))), F(0))


def cutoff_diagonal_form(weights):
    weights = _weights(weights)
    return sum((_mobius_phi(r)[1]*sum((weights[d]/d
                     for d in range(r, len(weights), r)), F(0))**2
                for r in range(1, len(weights))), F(0))


def cofactor_interval_norm(start, weights):
    _positive(start, 'start')
    weights = _weights(weights)
    direct = sum((cofactor_weight(n, weights)**2 for n in range(start+1, 2*start+1)), F(0))
    floor_form = sum((weights[d]*weights[e]*(2*start//lcm(d, e)-start//lcm(d, e))
                     for d in range(1, len(weights)) for e in range(1, len(weights))), F(0))
    error_bound = sum(abs(v) for v in weights)**2
    return direct, floor_form, start*cutoff_quadratic(weights), error_bound


def ramanujan_mean_square(coefficients):
    """Exact full-period guard for the diagonal mean used in(7)."""
    coefficients = dict(coefficients)
    if any(type(q) is not int or q < 1 or type(a) not in (int, F)
           for q, a in coefficients.items()):
        raise ValueError('positive moduli and real exact coefficients required')
    period = lcm(*coefficients) if coefficients else 1
    direct = sum((sum((a*ramanujan(q, n) for q, a in coefficients.items()), F(0))**2
                  for n in range(period)), F(0))/period
    diagonal = sum((a*a*_mobius_phi(q)[1] for q, a in coefficients.items()), F(0))
    return direct, diagonal
