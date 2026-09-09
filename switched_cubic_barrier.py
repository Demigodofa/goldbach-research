"""A coefficient boundary for the unweighted cubic switching certificate.

Owner: Kevin's research. Purpose: test switching on the actual cubic
prime/composite partition, separately from the earlier 2T-M plug-in.
Sol checked the deduction and actual verifier on 2026-09-08. Four focused
tests passed normally and with Python -O.

Exact arithmetic identity:
Let A=P+C be canonical square-start cubic survivors through H=N-3,
z=floor(cuberoot(H)). P indicates odd primes and C indicates composites;
each C entry is uniquely qr for primes z<q<=r. With ordered convolutions,
  T=[P*A]_N, U=[P*C]_N, G=[P*P]_N, so G=T-U.              (1)
Writing U=U_distinct+U_square separates q<r from q=r. The switched sequence
  b_l=# {z<q<r odd primes: qr=N-l}, 3<=l<=N-3 odd,
has b_l<=1, by unique factorization. Thus U_distinct=sum_l b_l*1_prime(l).
No factor2 is inserted: q<r counts each composite once, and U already
specifies which side is composite. G itself is an ORDERED prime-pair count.
Prime squares contribute at most sqrt(N) positions. Sieving b_l to sqrt(N)
omits prime complements l<sqrt(N); these contribute at most sqrt(N) more.
Both are o(K), K=S_2(N)*N/log(N)^2. They are retained in finite identities.

Precisely the proposed plug-in, not an assertion of its arithmetic inputs:
GRANT the original shifted-prime distribution hypotheses at a fixed
0<theta1<1, and the required uniformly summable remainder hypotheses for
each switched q-band at level theta2(alpha) in[delta,1), alpha=log(q)/log(N).
Also grant the natural switched semiprime mass and local-density matching.
These are the analogues of Assumption3.1(A1),(A4),(A5) in the source below;
no improved pointwise prime or semiprime distribution theorem is claimed.
At odd p not dividing N the removed proportion is1/(p-1); at2 and p|N
it is0. Thus the shared sieve product has normalization
  V_N(y)~exp(-gamma)*S_2(N)/log(y).
The Mertens normalization is derived in factored_linear_barrier.py.
Remove original-sequence primes dividing N at cost O(log(N)), and restore
small prime survivors at cost O(z). Switched q or r dividing N, and cutoff
equality/flooring, can instead cost O(N/z); they must not be charged merely
O(z). Together with squares and small switched prime complements, the
position budget is O(z+N/z+sqrt(N))=o(K). The distribution grants concern
the sequences actually sieved after the chosen removals; no remainder
theorem for a modified sequence is inferred from this position count alone.

Source and coefficient calculation:
Matomaki--Zuniga-Alterman, Weighted sieves with switching, Definition2.4,
Lemma2.5, (3.9)-(3.11), Assumption3.1, (4.17), (5.18)-(5.19), read2026-09-08:
https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/weighted-sieves-with-switching/986429394BA969687D48224E177E2F1C
Use trivial weight W=1, v=u=3, S=1, R=2 in its decomposition. This is
the source's general setup, not its later numerical P_3 application.
Its formal Assumption3.1 also takes theta1>1/3 with a fixed margin; lower
levels already supply zero through Lemma2.5 and cannot help this test.
The lower sieve supplies for T/K the coefficient
  B(theta1)=3*exp(-gamma)*f(3theta1)
           =0                           if theta1<=2/3,
           =(2/theta1)*log(3theta1-1)    otherwise.        (2)
In the switched upper sieve, s=2theta2 and F(s)=2exp(gamma)/s. Since
V_N(sqrt(N))~2exp(-gamma)*S_2(N)/log(N), the upper-estimate coefficient
for U/K is
  C(theta2)=2*integral_{1/3}^{1/2} d alpha/
                         (alpha*(1-alpha)*theta2(alpha)). (3)
Indeed the weighted count of q<r, qr<=N is N/log(N) times this integral
WITHOUT its leading2. The prime number theorem and partial summation give
the density1/[alpha*(1-alpha)]; the discarded r<=q contribution is
O(N/log(N)^2) before multiplication by the sieve factor1/log(N).
Uniformity of the weighted dyadic remainders remains part of the grant.

The certificate boundary:
The lower linear-sieve function is strictly increasing on2<s<=3:
the derivative of log(s-1)/s has positive numerator
s/(s-1)-log(s-1). Hence B(theta1)<2log2 for fixed theta1<1.
But integral_{1/3}^{1/2}1/[alpha*(1-alpha)] d alpha=log2, and theta2<=1
implies C(theta2)>=2log2. Therefore the LOWER certificate for G from(1)
has strictly negative leading coefficient B-C. At theta1=theta2=1 it is
exactly0 only as a LIMITING coefficient benchmark, outside the source's
level range. A zero leading coefficient does not settle lower-order terms.
If theta2(alpha)<=Theta<=1, B-2log2/Theta is an optimistic ceiling on
that certificate coefficient. It is exact when theta2 is constant Theta.

This rejects only the stated unweighted cubic lower-sieve/upper-switching
plug-in. It does not upper-bound actual G, imply a negative actual L, or
exclude other weights, other decompositions, or more coupled estimates.
Unlike the previous 2T-M test, this one does not grant an upper bound for
M=[A*A]. Its failure leaves stronger arithmetic input needed. No numerical
onset, new actual prime coverage, Goldbach failure, or historical novelty
is asserted. Exact counts from the small verifier are validation only.
"""
from fractions import Fraction
from math import isqrt

from factored_linear_barrier import factored_bound, log_enclosure


def switching_mass(left: int | Fraction, right: int | Fraction,
                   terms: int = 12) -> tuple[Fraction, Fraction]:
    """Enclose the factor-size integral of1/[alpha*(1-alpha)] on[left,right].

    Endpoints must be exact and lie in[1/3,1/2]. This is a coefficient
    integral, not a claim of distribution of actual primes in progressions.
    """
    if (type(left) not in (int, Fraction) or type(right) not in (int, Fraction)
            or not Fraction(1, 3) <= left <= right <= Fraction(1, 2)):
        raise ValueError("require exact rational1/3<=left<=right<=1/2")
    left, right = Fraction(left), Fraction(right)
    return log_enclosure(right*(1-left)/(left*(1-right)), terms)


def switched_cubic_coefficient(theta_original: int | Fraction,
                               theta_switched: int | Fraction,
                               terms: int = 12) -> tuple[Fraction, Fraction]:
    """Enclose a LOWER-CERTIFICATE coefficient, NOT actual G/K or L/K.

    theta_switched is a constant switched level or a uniform ceiling on
    theta2(alpha); in the latter case this is an optimistic coefficient.
    Levels equal1 are limiting benchmarks, not source theorem endpoints.
    """
    if any(type(t) not in (int, Fraction) or not 0 < t <= 1
           for t in (theta_original, theta_switched)):
        raise ValueError("require exact rational levels in(0,1]")
    theta_original, theta_switched = Fraction(theta_original), Fraction(theta_switched)
    log_low, log_high = switching_mass(Fraction(1, 3), Fraction(1, 2), terms)
    if theta_original == 1:
        # Symbolic cancellation keeps the double limiting endpoint exact.
        factor = 2*(1-1/theta_switched)
        return factor*log_high, factor*log_low
    low = high = Fraction(0)
    if theta_original > Fraction(2, 3):
        low, high = log_enclosure(3*theta_original-1, terms)
        low, high = 2*low/theta_original, 2*high/theta_original
    return low-2*log_high/theta_switched, high-2*log_low/theta_switched


def switch_partition(target: int, survivors: bytearray,
                     composites: bytearray) -> tuple[int, int, int, int]:
    """Return(T,U_distinct,U_square,G) for truthful full cubic A,C inputs.

    Odd slot i means3+2i through N-3. Binary and subset checks are inherited
    from factored_bound; they do not establish primality or cubic provenance.
    The prime-square terms are counted, not dropped as an asymptotic error.
    This small identity verifier does not generate a prime/count prefix.
    """
    _, t, _, _ = factored_bound(target, survivors, composites)
    prime_flags = bytearray(a-c for a, c in zip(survivors, composites))
    distinct = square = 0
    for i, c in enumerate(composites):
        if c and prime_flags[-1-i]:
            n = 3+2*i
            if isqrt(n)**2 == n:
                square += 1
            else:
                distinct += 1
    return t, distinct, square, t-distinct-square
