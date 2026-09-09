"""Two large distinct prime factors: cancellation in the unbalanced MODEL.

Owner: Kevin's Goldbach research. Purpose: test a new correlation mechanism
at B=Y^(1/2), A=Y^(1/4), C=Y^(1/2), K=Y^(1/4), where the retained linear
budget was Y and the reciprocal-energy budget was Y^(9/8). Those are upper
budget failures, not lower bounds. All earlier polynomial tools survive.
This is a derived two-prime theorem, not a signed prime-pair estimate.

Checked primary inputs (no external novelty claim):
* Kowalski--Michel--Sawin, arXiv:1511.01636v5, Definition2.2, Lemma2.5,
  (2.11)--(2.14), Theorem4.11, Proposition4.6(8):
  https://arxiv.org/pdf/1511.01636v5 . These are PRIME correlation inputs.
* Milicevic--Qin--Wu, arXiv:2511.07550v1, section4.1, (4.1)--(4.3):
  https://arxiv.org/pdf/2511.07550v1 . We adapt its scalar shift/divisor/
  Holder algebra, retaining the KMS conjugations. Its stated Kl2 theorem
  and its prime-square local theorem are NOT being asserted for Kl3.

I. Zero extension and statement.
For squarefree q let K_q(z)=q^-1 sum_(u,v unitsq)e_q(u+v+z/(uv)).
This repo's natural extension has K_p(0)=1/p. The KMS sheaf is instead
extended BY ZERO at0. Therefore put Z_q(z)=1_(gcd(z,q)=1)*K_q(z).
For q=p1*p2 with DISTINCT primes, Q_p=q/p, exactly
  Z_q(z)=product_(p|q) Z_p(z*inverse(Q_p^3)).               (1)

Let p_min>=q^(2/5), sqrt(q)<=X<=q^(1/2+1/128), and let alpha,beta be
arbitrary complex coefficients supported on positive integers <=X.
For ANY integer c and every epsilon>0,
  |sum_(m,n)alpha_m beta_n K_q(c*m*n)|
     <<epsilon ||alpha||2 ||beta||2 q^(11/64+epsilon) X^(5/8). (2)
At X=sqrt(q), the factor is q^(31/64), saving q^(1/64) against X.
Finitely many small moduli are covered by the implied constant. This
statement is neither an all-modulus theorem nor a prime-power theorem.

II. The eight-factor correlation and CRT.
First use Z and assume c unit. A fixed unit c is absorbed by scaling the
complete s variable in the following correlation; all additive twists are
allowed, so none of the estimates or b-exceptional sets change. Define
  H_b(r,s)=Z_q(s(r+b1))*Z_q(s(r+b2))
                    *conjugate(Z_q(s(r+b3))*Z_q(s(r+b4))),
  R_q(b;s1,s2)=sum_r H_b(r,s1)*conjugate(H_b(r,s2)),
  S_q(b;h1,h2)=sum_(r,s1,s2 modq; gcd(s1-s2,q)=1)
       H_b(r,s1)*conjugate(H_b(r,s2))*e_q(h1*s1+h2*s2).
The bars are essential for odd-rank Kl3 and are retained everywhere.

At a prime p, outside the rank3 SL diagonal
  {b1,b2}={b3,b4} as MULTISETS modulo p,
Lemma2.5 gives R_p<<sqrt(p) when s1!=s2 and both are nonzero. If either
is zero, Z makes the product zero, so the same bound applies to all
distinct s1,s2. Outside an additional bounded-degree bad hypersurface,
Theorem4.11 gives, for ALL lambda1,lambda2,
  C_p(lambda1,lambda2)=sum_r R(r,lambda1)*conjugate(R(r,lambda2))
     =1_(lambda1=lambda2)*p^2+O(p^(3/2)),
where R(r,lambda)=sum_s H_b(r,s)e_p(lambda*s).
Removing s1=s2 is EXACTLY
  S_p(b;h1,h2)=C_p(h1,-h2)
                -p^-1 sum_lambda C_p(h1+lambda,-h2+lambda). (3)
The p^2 terms cancel, INCLUDING h1=-h2. Thus S_p<<p^(3/2) uniformly
in both twists. Theorem4.11, not merely the distinct-twist wording of
Theorem2.6, supplies this deduction.

CRT in (1) and the change s'_i=s_i*inverse(Q_p^3) give exactly
  S_q(b;h1,h2)=product_(p|q) S_p(b;h1*Q_p^2,h2*Q_p^2).    (4)
In particular the rank-three twist is Q_p^2, not the Kl2 twist Q_p.
The unit-difference restriction factors into s1!=s2 at BOTH primes.
Hence R_q<<sqrt(q) outside the local diagonal at both primes; S_q<<q^1.5
outside the two local bad hypersurfaces. Constants are uniform since
there are exactly two prime factors and fixed rank/conductor.

III. Small shifts synchronize the diagonal and bound the bad locus.
Use M=N=X, auxiliary shifts a in(A0,2A0], b in(B0,2B0], with
  A0 asymp q^(1/8), B0 asymp X*q^(-1/8), L=A0*X.          (5)
Choose fixed constants so A0*B0<=N and 2*A0*M<q. Since
1/2+1/128-1/8<2/5, we have 2*B0<p_min and every a is a q-unit for
large q. Thus each modular diagonal in the b box is the same literal
integer multiset equality, with O(B0^2) tuples. Each bounded-degree
bad hypersurface has O(B0^3) tuples in the box: elementary polynomial
zero counting over subsets of F_p, with B0<p. Their union has this bound.

Cauchy in beta gives an n-sum of alpha pair correlations. Pairs with
gcd(m1-m2,q)>1 contribute at most
  O(N*||alpha||2^2*(1+M/p1+M/p2)),                        (6)
by summing residue classes and Cauchy within each class. The resulting
bilinear error has norm factor O(sqrt(X)+X/sqrt(p_min)), absorbed in(2).

For unit differences, the scalar shifting/Holder argument of MQW(4.3),
with the complex bars as in KMS(2.11), bounds the remaining second moment:
  T1 <<q^epsilon ||alpha||2^2 (A0*B0)^-1 (A0*N)^(3/4) M^(1/2)
                            *(sum_b |Sigma1(b,L)|)^(1/4), (7)
where Sigma1 sums R_q over positive s1,s2 at scale L, with smooth
majorants in each s_i and gcd(s1-s2,q)=1. Here is why the scalar argument
survives this composite q: auxiliary a are units; a*(m1-m2) remains a unit;
the collision equalities a*m_i=a'*m'_i are integer equalities since
2*A0*M<q; their multiplicities are divisor-bounded; and inverse-a
congruences determine n' in an interval of length O(N)<q. The bounds on
the shifted incidence weight used by Holder are A0*N*M*||alpha||2^2 and
q^epsilon*A0*N*||alpha||2^4. Shifted interval endpoints are handled by
the source's completion/partial-summation step, with logarithmic loss.
No square-root correlation for a prime square is needed for this d=1 part.

For the O(B0^2) diagonal tuples, trivial summation gives L^2*q. For the
O(B0^3) bad non-diagonal tuples, use R_q<<sqrt(q) to get L^2*sqrt(q).
For good tuples, double Poisson and (4) give q^1.5: its prefactor(L/q)^2
is canceled by the two Schwartz dual L1 norms O((q/L)^2), since L<q.
Therefore
  sum_b |Sigma1| << B0^2*L^2*q+B0^3*L^2*q^0.5+B0^4*q^1.5
                   <<X^4*q.                              (8)
The first and third terms equal this scale; the middle term is
X^5*q^(3/8), no larger because X<=q^(5/8). Substituting into(7) gives
T1<<q^epsilon||alpha||2^2*q^(11/32)*X^(5/4). Outer Cauchy proves(2)
for Z and unit c. For nonunit c the Z sum is identically0.
Finally, on a nonunit z, |K_q(z)|<=3/p_min (or1/q if q|z). Thus replacing
Z by K costs <=3*X/p_min*||alpha||2||beta||2, absorbed in(2) for all c.

IV. The costed unbalanced smooth MODEL.
Define E_q exactly as in composite_linear_kernel.py, here with
  B=Y^1/2, A=Y^1/4, C=Y^1/2, K=Y^1/4,
  m in[Y,2Y] integer, H,J0<=Y^(1/4096),
  q in[C,2C], q=p1*p2, p1!=p2, min(p1,p2)>=q^(2/5).
The unit r_q and arbitrary bounded JOINT period-J_q weights omega_(q,k)
are retained. Then
  sum_q |E_q| <<Y^(127/128+epsilon)*J0^5*H^2
                          +Y^(3/4+epsilon)*H*J0
              <<Y^(4071/4096+epsilon).                    (9)
This covers this modulus class at the formerly failing unbalanced box.

Proof: J=J_q<p_min, hence gcd(q,J)=1. Double Poisson at qJ costs
Y/(q^3*J^2). CRT splits off the J-transform, of magnitude<=J^2. Splitting
the h,l residue classes modulo J costs another J^2; for each fixed h and
l class its bounded weight is an arbitrary coefficient of k. Thus the
conservative period cost is J^4 and the l,k coefficients remain separated.
Nonzero frequencies have scales U=qJ/B asymp J and V=qJ/A asymp Y^1/4 J.
Schwartz tails can be truncated at Y^rho for arbitrarily small positive
rho, paying Y^epsilon in the final result. Every retained nonzero h is
a q-unit. Signs of h,l are split and absorbed into the multiplier.

Let F_q(h,l;t)=sum_(u,v unitsq)e_q(t/(uv)+hu+lv). At a prime, h unit gives
  F_p(h,l;t)/p=K_p(thl)-1_(p|l and p|t).
Consequently, by CRT, F_q/q differs from Z_q(unit*t*h*l) by at most
  O(sum_(p|q)(1/p+1_(p|l and p|t))).                      (10)
For t=m*k and NONZERO l, the weighted mass over l,k is O(V*H*K/p_min),
including cases p|m. The Schwartz sum over positive multiples of p is
O(V/p), even when V<p. This correction costs at most
Y^(1+epsilon)*J0^4*H/p_min after summing q, hence is absorbed in(9),
since p_min>=Y^(1/5) up to a fixed constant.

For the main Z term use(2), or its Z version, on l and k padded to
X asymp q^1/2*D*Y^rho, D=max(J,H). This satisfies the X range for small
rho. The norm product is O(sqrt(V*H*K)), with truncation and smooth
partial-summation costs absorbed into Y^epsilon. Restrictions on l modJ
only reduce its norm. The multiplier m*r_q*h times the CRT unit may be
nonunit; that case is zero for Z. Summing h costs O(U). Thus the off-axis
bound per q is
  Y/(q^3*J^2) * q*J^4 * U * sqrt(V*H*K) *q^(31/64)*D^(5/8)
    <<Y^(63/128+epsilon)*J^(7/2)*H^(1/2)*D^(5/8).
There are O(Y^1/2) eligible q, without needing any density theorem.
Since D<=J*H, the powers are J^(33/8)*H^(9/8), bounded by J0^5*H^2.
The h=0 and l=0 axes and their overlap retain the previously proved
composite_linear_kernel.py bound Y^epsilon*H*J0*B*A. This proves(9).

V. Failed applicability check retained; reassessment.
The initial proposal was to apply a modern ordinary-Kloosterman bilinear
interval theorem after just M-Poisson. The remaining sum is
S(h,r_q*m*k/a;q). The a variable occupies an INVERSE interval; relabeling
it does not make it an additive interval. Blomer--Pascadi, 2607.24311v1,
Theorem1.1/Remark1.2, https://arxiv.org/pdf/2607.24311 , and Pascadi,
Theorems1.1/1.2/7.1, https://doi.org/10.1007/s00039-026-00746-0 , do not
supply that missing support condition. Freezing a instead leaves the h
interval too short: even with separated coefficients and a unit multiplier,
the first source's bound needs h-length>q^(7/16) to improve the trivial
Weil budget here (the factor-specific second route needs>q^(1/3)).
Their theorems remain useful for genuinely linear interval inputs.

Reassessment: the direct Kl2 source application fails; the derived Kl3
two-prime mechanism succeeds. General factorizations, prime powers in this
unbalanced box, full box coverage, and ORIGINAL arithmetic/sieve transfer
remain OPEN. Latest original-affine result remains2b8cf98; no exceptional
zero, effective onset, universal prime coverage, or novelty is claimed.
The finite guards below verify new CRT twists, bars, diagonal subtraction,
zero-extension corrections and exponents; they do not prove asymptotics.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd

from composite_linear_kernel import _reduce
from major_arc_kernel import _factorization
from squarefree_correlation_kernel import _raw_kl3, _multiply_embedded


def _gauss_mul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def _conjugate(a):
    return (a[0], -a[1])


def _h_table(values, b):
    q = len(values)
    table = []
    for r in range(q):
        row = []
        for s in range(q):
            left = _gauss_mul(values[s*(r+b[0]) % q], values[s*(r+b[1]) % q])
            right = _gauss_mul(values[s*(r+b[2]) % q], values[s*(r+b[3]) % q])
            row.append(_gauss_mul(left, _conjugate(right)))
        table.append(row)
    return table


def _raw_eight(values, b, h1, h2, unit_difference):
    """Gaussian INTEGER coefficient histogram; no floating point phases."""
    q = len(values)
    table = _h_table(values, b)
    counts = [[0, 0] for _ in range(q)]
    for s1, s2 in product(range(q), repeat=2):
        if unit_difference and gcd(s1-s2, q) != 1:
            continue
        phase = (h1*s1+h2*s2) % q
        for row in table:
            amplitude = _gauss_mul(row[s1], _conjugate(row[s2]))
            counts[phase][0] += amplitude[0]
            counts[phase][1] += amplitude[1]
    return tuple(tuple(value) for value in counts)


def _reduce_gauss(counts):
    q = len(counts)
    return (_reduce([v[0] for v in counts], q),
            _reduce([v[1] for v in counts], q))


def completed_eight_exact(values, b, h1, h2):
    return _reduce_gauss(_raw_eight(values, b, h1, h2, True))


def diagonal_subtraction_exact(values, b, h1, h2):
    """Returns q*S and q*C-sum_shift C independently, including equal twists.

    This projection removes equality modulo q. It equals unit-difference
    projection only for prime q; the caller tests this distinction too.
    """
    q = len(values)
    direct = _raw_eight(values, b, h1, h2, True)
    whole = _raw_eight(values, b, h1, h2, False)
    shifted = [_raw_eight(values, b, h1+t, h2-t, False) for t in range(q)]
    left = [(q*v[0], q*v[1]) for v in direct]
    right = [tuple(q*whole[i][j]-sum(v[i][j] for v in shifted) for j in range(2))
             for i in range(q)]
    return _reduce_gauss(left), _reduce_gauss(right)


def toy_crt_values(local):
    """Complex integer trace fixtures with the rank-three inverse-cube CRT."""
    q = 1
    for p in local:
        q *= p
    values = []
    for z in range(q):
        value = (1, 0)
        for p, table in local.items():
            value = _gauss_mul(value, table[z*pow((q//p)**3, -1, p) % p])
        values.append(value)
    return tuple(values)


def completed_eight_crt(local, b, h1, h2, twist_power=2):
    q = 1
    for p in local:
        q *= p
    counts = [(1, 0)]+[(0, 0)]*(q-1)
    for p, values in local.items():
        scale = q//p
        factor = _raw_eight(values, b, h1*scale**twist_power,
                            h2*scale**twist_power, True)
        result = [[0, 0] for _ in range(q)]
        for i, a in enumerate(counts):
            for j, v in enumerate(factor):
                value = _gauss_mul(a, v)
                result[(i+scale*j) % q][0] += value[0]
                result[(i+scale*j) % q][1] += value[1]
        counts = [tuple(value) for value in result]
    return _reduce_gauss(counts)


def transform_zero_extension_prediction(q, h, l, t):
    """Exact CRT expansion of F_q/q as products of Z_p+delta_p, h a unit."""
    factors = _factorization(q)
    if (len(factors) != 2 or any(e != 1 for _, e in factors) or gcd(h, q) != 1):
        raise ValueError("require two distinct prime factors and a unit h")
    counts = [F(1)]+[F(0)]*(q-1)
    for p, _ in factors:
        parameter = t*h*l*pow((q//p)**3, -1, p) % p
        if parameter:
            local = _raw_kl3(p, parameter)
        else:
            # Literal Z_p(0)=0; natural K_p(0)=1/p belongs in delta.
            local = [F(0)]*p
            local[0] = F(1, p)-int(l % p == 0 and t % p == 0)
        counts = _multiply_embedded(counts, local, p, q)
    return _reduce(counts, q)


def two_prime_budget(sigma=0, period_exponent=0, frequency_exponent=0):
    """Exact rational exponents; sigma is log_q(X)-1/2, decorations log_Y."""
    values = (sigma, period_exponent, frequency_exponent)
    if any(type(v) not in (int, F) for v in values):
        raise ValueError("use exact rational exponents")
    sigma, j, h = map(F, values)
    if not 0 <= sigma <= F(1, 128) or not 0 <= j <= F(1, 4096) or not 0 <= h <= F(1, 4096):
        raise ValueError("outside the proved exponent range")
    x = F(1, 2)+sigma
    a, b, ell = F(1, 8), x-F(1, 8), x+F(1, 8)
    terms = (2*b+2*ell+1, 3*b+2*ell+F(1, 2), 4*b+F(3, 2))
    second = -x+F(3, 4)*(a+x)+x/2+max(terms)/4
    core = second/2
    raw_model = F(127, 128)+F(7, 2)*j+h/2+F(5, 8)*max(j, h)
    return dict(moment_terms=terms, moment=4*x+1, core=core,
                expected_core=F(11, 64)+F(5, 8)*x,
                short_shift=b, raw_model=raw_model,
                model=F(127, 128)+5*j+2*h,
                axes=F(3, 4)+j+h, correction=F(4, 5)+4*j+h)
