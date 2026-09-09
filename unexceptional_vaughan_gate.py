"""Exact unexceptional Type II remainder and the failed generic transfer.

Owner: Kevin's Goldbach research. Purpose: preserve the actual arithmetic
coefficients, Type I reduction and the next covariance target. This is a
proof/verification module, not a manuscript or prime-pair estimate.
Sol independently checked the derivation, actual proof/code and nine exact
guards, including the diagonal bound: PASS. Tests passed normally and under
Python -O, 0.008s each. The actual off-diagonal estimate remains unproved.

QUESTION AND DISPOSITION.
Can full_model_box_kernel.py's all-moduli reciprocal saving directly bound
the remaining unexceptional prime/model correlation? No licensed transfer
has been found: its smooth/short-period INPUT hypotheses do not include the
actual Mobius/divisor coefficients. Generic coefficient completion fails
the quantitative budget. This limits that proposed transfer, not all uses
of the kernel, Mobius cancellation, the polynomial tools or Goldbach methods.
The conditional coverage in prime_cutoff_bridge.py remains valid unchanged.

EXACT ARITHMETIC REDUCTION.
1. Work ONLY in the UNEXCEPTIONAL alternative of ramanujan_type_i.py.
   Keep I=(Y/2,Y], central even m, J={n:n,m-n in I}, L=log Y,
   gamma=1/2-eps, 0<eps<1/12, and its fixed delta<=1/4800. Write
    S=Y^delta, M_S=1_I Gamma_S, E(n)=1_I(n)Lambda(n)-M_S(n).
   This branch means the common exceptional alternative specified by the
   earlier theorem is absent; it is not an unconditional claim of absence.
   The reviewed input is
    D_TI=sum_(d<=Y^gamma) max_K |sum_(dk in J,k in K) E(m-dk)|
        <<_A Y/L^A for every fixed A,
   and CROSS=(F*M_S)(m)>>Y S_2(m), F=1_I log(n)1_prime(n).
2. Set U0=V0=floor(Y^(gamma/2)); U0 cuts Lambda, V0 cuts Mobius.
   Vaughan's EXACT convolution identity is
    Lambda=Lambda_<=U0 + mu_<=V0*log - mu_<=V0*Lambda_<=U0*1
                                      +mu_>V0*Lambda_>U0*1.       (1)
   Proof: split mu and Lambda in mu*Lambda, then convolve with1,
   using mu*1=delta_1 and Lambda*1=log. The free convolution factor1
   is ESSENTIAL; dropping it changes the Type II coefficients.
   Primary check: Tao, 254A Notes3, Lemma18 equation(32),
   https://terrytao.wordpress.com/2015/01/10/254a-notes-3-the-large-sieve-and-the-bombieri-vinogradov-theorem/
   checked2026-09-09. Its U,V names are interchanged relative to ours.
   Only this elementary identity is used here. This does NOT revive the
   excluded Linnik Proposition23 from the DIFFERENT Notes7. Notes3 also
   corrects a missing *1 and the false bound |mu_>U*1|<=1; that grouped
   coefficient is divisor-bounded. We group1 into Lambda instead.
3. On J, the first term of(1) vanishes eventually. The second contributes
    sum_(d<=V0)mu(d) sum_(dk in J)log(k) E(m-dk).
   Abel summation bounds this by O(L D_TI), because log(k) has total
   variation O(L) on each interval. Group the third term using
    C_d=sum_(ab=d,a<=V0,b<=U0)mu(a)Lambda(b).
   Its support is d<=U0 V0<=Y^gamma and |C_d|<=sum_(b|d)Lambda(b)=log d.
   Thus its contribution is also O(L D_TI). The remaining exact term is
    T(m)=sum_(ab in J,a>V0,b>U0)mu(a) B_U0(b) E(m-ab),             (2)
    B_U0(b)=sum_(d|b,d>U0)Lambda(d), 0<=B_U0(b)<=log b.
   The condition b>U0 follows from a nonempty sum; it does not license
   replacing B_U0 by Lambda or log b. Consequently
    sum_(n in J)Lambda(n)E(m-n)=T(m)+O_A(Y/L^A).                  (3)
4. To compare this with actual prime pairs, |Gamma_S(n)|<<_G S^2 follows
   by summing its O(S^2) Ramanujan components, each bounded by O_G(1).
   Proper prime powers in the first variable therefore cost
    O(Y^(1/2+2delta+o(1)))
   on replacing Lambda by F in(3). Proper prime powers in the partner
   cost O(Y^(1/2+o(1))). Thus EXACT prime-pair mass satisfies
    (F*F)(m)=(F*M_S)(m)+T(m)
                  +O_A(Y/L^A)+O(Y^(1/2+2delta+o(1))).            (4)
   A uniform T=o(Y) would suffice for a prime-pair lower bound in this
   branch. A sufficiently small ONE-SIDED lower bound also suffices;
   absolute o(Y) is a proposed sufficient target, not a necessary condition.
   Neither (1), (3) nor the already proved CROSS supplies that estimate.

WHY THE EXISTING MODEL DOES NOT AUTOMATICALLY ESTIMATE(2).
5. A dyadic piece of(2), retaining the product/interval mask, has actual
   coefficients alpha_a=mu(a), beta_b=B_U0(b)/L, both bounded by1.
   Their factor scales lie between Y^(gamma/2+o(1)) and
   Y^(1-gamma/2+o(1)); ordinary interior boxes have these full lengths.
   The full_model_box_kernel.py INPUT theorem instead has fixed smooth
   spatial factors and bounded joint periodic weights with period
   J<=Y^(1/4096), and a saved exponent sigma=1/4096. Some INTERNAL
   completed-kernel lemmas accept arbitrary coefficients. Their location
   after smooth spatial completion matters: they do not remove its input
   hypotheses or justify Poisson with these unchanged arithmetic weights.
6. For a bounded coefficient on a cyclic interval of length N, normalized
   Fourier coefficients obey
    sum_h |c_hat(h)|^2=(1/N)sum_n |c(n)|^2<=1,
    sum_h |c_hat(h)|<=sqrt(N).
   This worst-case bound is sharp: for odd prime N=p, c(n)=e_p(n^2)
   has every |c_hat(h)|=1/sqrt(p), by completing the square or by its
   zero off-diagonal cyclic autocorrelations. Hence l1=sqrt(p).
   Even GRANTING a uniform model bound for every additively modulated
   term, which is itself NOT in the saved full-model statement, using
   triangle with this generic bound would give only
      Y^(1-sigma)*sqrt(N)=Y^(1-sigma+nu/2), N=Y^nu.
   It certifies a saving only for nu<2sigma=1/2048. Here factor spans
   reach nu>=gamma/2>5/24, so this generic budget does not close.
   For example nu=1/4 gives exponent4607/4096>1. Encoding the full
   sequence as a period-N weight also exceeds the J cap.
   These are worst-case BUDGET failures; the actual Mobius or B_U0
   Fourier l1 norms have NOT been proved large. The chirp is a sharpness
   fixture for arbitrary bounded weights, not a Goldbach counterexample.

THE PRECISE NEXT ARITHMETIC ESTIMATE.
7. For a dyadic rectangle a~A,b~B, AB comparable to Y, define
    Z_ab=1_(ab in J) E(m-ab),
    K_m(b1,b2)=sum_(a~A) Z_(a,b1) conjugate(Z_(a,b2)).
   All intersection masks must stay. Then Cauchy gives EXACTLY
    |sum_(a,b)alpha_a beta_b Z_ab|^2
      <=(sum_a |alpha_a|^2)
            *sum_(b1,b2) beta_b1 conjugate(beta_b2) K_m(b1,b2). (5)
   The last quadratic form is real and nonnegative; bounding the signed
   off-diagonal terms is a separate task. Restoring the outside L in(2)
   shows, for example, that a bound on this energy by
      o(A B^2/L^6)
   uniformly across the O(L^2) dyadic boxes is sufficient for T=o(Y).
   This is a SUFFICIENT energy target, not an assertion that every route
   must use Cauchy or this amount of logarithmic saving.
8. The diagonal part of(5) IS already harmless. Since |beta_b|<=1,
    sum_b |beta_b|^2 K_m(b,b)
      <=sum_(n in J)tau(n)|E(m-n)|^2
      <<_epsilon Y^(1+4delta+epsilon).
   This uses only |E|<<L+S^2 and tau(n)<<_epsilon n^epsilon. Uniformly
   in the dyadic boxes, A B^2 is comparable to YB and B has scale at least
   Y^(gamma/2), while 4delta<=1/1200<5/24<gamma/2. Choose epsilon below
   that fixed gap: the diagonal is o(A B^2/L^6). No unproved prime-pair
   estimate is hidden in this diagonal bound.
   What remains is a sufficiently small ONE-SIDED upper bound on the
   weighted OFF-DIAGONAL covariance in(5); bounding its full absolute
   value would be stronger than necessary.
9. Expanding E=Lambda-M_S leaves the actual signed prime/model covariance
   at p_i=m-a b_i, linked by
      b2*p1-b1*p2=(b2-b1)*m.                             (6)
   The diagonal b1=b2 is different from the off-diagonal. Off-diagonal
   proportional coefficients and nonreduced residue cases must be kept;
   they are not automatically generic Kloosterman phases. A second
   decomposition of Lambda merely inserts further arithmetic coefficients
   until a new estimate controls them. Neither the present TI input nor
   the smooth reciprocal theorem proves the covariance bound in(5).

Next question: can the signed covariance in(5), with its actual divisor
weights and arithmetic degeneracies, be estimated more sharply than the
generic coefficient completion? Test an explicit average or decomposition,
with all diagonal/main corrections, rather than asserting independence of
the two linked prime conditions. Conditional character coverage, smooth
kernels and polynomial tools remain usable components; Goldbach stays open.

Finite helpers below preserve exact logarithmic coefficient identities,
intersection masks, Gram positivity and the completion budget only. They
do not model an exceptional zero, prove T=o(Y), or count new prime pairs.
"""
from fractions import Fraction as F

from major_arc_kernel import _factorization, _mobius_phi


def _positive(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f'{name} must be a positive integer')


def _divisors(n):
    values = [1]
    for p, exponent in _factorization(n):
        values = [d*p**e for d in values for e in range(exponent+1)]
    return sorted(values)


def _add(vector, terms, scalar=1):
    for p, coefficient in terms:
        vector[p] = vector.get(p, 0)+scalar*coefficient


def _clean(vector):
    return tuple((p, coefficient) for p, coefficient in sorted(vector.items()) if coefficient)


def mangoldt_log_vector(n):
    """Exact log-prime coefficients of Lambda(n), including prime powers."""
    _positive(n, 'n')
    factors = _factorization(n)
    return ((factors[0][0], 1),) if len(factors) == 1 else ()


def large_divisor_log_vector(n, lambda_cutoff):
    """Exact B_U(n), with the free Vaughan convolution factor retained."""
    _positive(n, 'n')
    _positive(lambda_cutoff, 'Lambda cutoff')
    vector = {}
    for d in _divisors(n):
        if d > lambda_cutoff:
            _add(vector, mangoldt_log_vector(d))
    return _clean(vector)


def vaughan_log_vectors(n, lambda_cutoff, mobius_cutoff):
    """Four SIGNED terms in identity(1), as exact log-prime vectors."""
    for value, name in ((n, 'n'), (lambda_cutoff, 'Lambda cutoff'), (mobius_cutoff, 'Mobius cutoff')):
        _positive(value, name)
    low, linear, subtracted, bilinear = {}, {}, {}, {}
    if n <= lambda_cutoff:
        _add(low, mangoldt_log_vector(n))
    for a in _divisors(n):
        mu = _mobius_phi(a)[0]
        if a <= mobius_cutoff:
            _add(linear, _factorization(n//a), mu)
            for b in _divisors(n//a):
                if b <= lambda_cutoff:
                    _add(subtracted, mangoldt_log_vector(b), -mu)
        else:
            _add(bilinear, large_divisor_log_vector(n//a, lambda_cutoff), mu)
    return tuple(_clean(term) for term in (low, linear, subtracted, bilinear))


def covariance_matrix(target, a_values, b_values, errors, low, high):
    """Exact real Gram covariance with low<ab<=high and positive partners."""
    _positive(target, 'target')
    if type(low) is not int or type(high) is not int or not 0 <= low < high < target:
        raise ValueError('require exact 0<=low<high<target')
    if not a_values or not b_values or len(set(a_values)) != len(a_values) or len(set(b_values)) != len(b_values):
        raise ValueError('nonempty distinct coordinate lists required')
    for v in tuple(a_values)+tuple(b_values):
        _positive(v, 'coordinate')
    rows = []
    for a in a_values:
        row = []
        for b in b_values:
            value = errors[target-a*b] if low < a*b <= high else F(0)
            if type(value) is not F:
                raise ValueError('exact Fraction error samples required')
            row.append(value)
        rows.append(tuple(row))
    gram = tuple(tuple(sum((row[i]*row[j] for row in rows), F(0))
                       for j in range(len(b_values))) for i in range(len(b_values)))
    return tuple(rows), gram


def chirp_difference_counts(prime, shift):
    """Counts of (n+h)^2-n^2 mod p, proving the exact off-axis cancellation."""
    if type(prime) is not int or prime < 3 or _factorization(prime) != ((prime, 1),):
        raise ValueError('odd prime modulus required')
    if type(shift) is not int:
        raise ValueError('integer shift required')
    counts = [0]*prime
    for n in range(prime):
        counts[((n+shift)**2-n*n) % prime] += 1
    return tuple(counts)


def generic_completion_budget(length_exponent):
    """Worst-case l1-transfer exponent, even granting phase-uniform estimates."""
    if type(length_exponent) is not F or not 0 <= length_exponent <= 1:
        raise ValueError('exact exponent in[0,1] required')
    return 1-F(1, 4096)+length_exponent/2


def diagonal_margin(delta, epsilon):
    """Fixed power margin before the arbitrarily small divisor-bound loss."""
    if type(delta) is not F or not 0 < delta <= F(1, 4800):
        raise ValueError('exact 0<delta<=1/4800 required')
    if type(epsilon) is not F or not 0 < epsilon < F(1, 12):
        raise ValueError('exact 0<epsilon<1/12 required')
    return (F(1, 2)-epsilon)/2-4*delta
