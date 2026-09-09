"""Coefficient boundaries for unweighted and weighted cubic switching.

Owner: Kevin's research. Purpose: test switching on the actual cubic
prime/composite partition, separately from the earlier 2T-M plug-in.
Sol checked both deductions and actual verifiers on 2026-09-08. Eight
combined focused tests passed normally and with Python -O.

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

Weighted cubic extension:
Keep v=3,S=1,R=2 and the same explicit distribution/mass grants. Fix a
Lipschitz w with0<=w<=1 supported in[1/3,b], b<=1/2, and set
  W(n)=1-sum_{p|n} w(log(p)/log(N)).
The divisors here are DISTINCT primes: W(q^2)=1-w_q, not1-2w_q. Suppose
theta1>b with the source's fixed margin, and delta<=theta2(alpha)<1.
Let I_theta=integral w(alpha)/[alpha*(theta-alpha)] over[1/3,b]. With
B0(theta1) from(2), the source's weighted lower coefficient is
  B_w=B0(theta1)-2*I_theta1.                               (4)
This follows from(4.17), since F(3*(theta1-alpha)) has its explicit2e^gamma/s
form throughout the weight support. Equations(5.21)-(5.23) give the switched
upper coefficient
  C_w=2*integral_{1/3}^{1/2}(1-w(alpha))/
                         [alpha*(1-alpha)*theta2(alpha)]. (5)
In the leading last-prime-factor replacement, the larger factor's exponent
is1-alpha>=1/2, so its w-value is0 (the boundary point is immaterial).
Consequently (1-w(alpha)-w(1-alpha))_+=1-w(alpha). The source charges the
last-factor replacement O(N*loglog(N)/log(N)^2) before the sieve factor
1/log(N), hence o(K). Its triangular q<r truncation and the separate
O(N/z+sqrt(N)+z) position allowances remain in force. This does not assert
a new weighted remainder theorem or uniformity over N-dependent weights.
The coefficient inequality below is uniform over the admitted profiles;
the analytic o(K) statement is for each fixed Lipschitz profile. Any
uniform analytic statement would also need a common Lipschitz norm bound
and the corresponding uniform distribution/remainder hypotheses.

Functional cancellation for EVERY such fixed weight:
Since theta1<=1, I_theta1>=I_1. Since theta2<=1 and1-w>=0,
  C_w>=2*(log2-I_1).
It follows that
  B_w-C_w<=B0(theta1)-2log2<0 for fixed theta1<1.           (6)
At theta1=theta2=1 the formal limiting coefficients agree exactly:
  B_w=C_w=2*(log2-I_1).
This is an identity of the whole weight functional, not a parameter scan.
It rules out a positive leading certificate from this particular fixed
cubic, additive small-prime-divisor weight family with the stated sieve
estimates. It does NOT rule out all weighted sieves. For a fixed smaller
theta2, a weight may improve on the unweighted coefficient while both stay
negative; (6) compares to the optimistic unweighted theta2=1 ceiling.

Finite weighted certificate and its exact losses:
Using nonnegative prime weights w_p<=1 and the truthful full cubic inputs,
  Sigma1=sum_n P(N-n)*A(n)*W(n),
  Sigma2=sum_n P(N-n)*C(n)*max(W(n),0), J_W=Sigma1-Sigma2.
Then
  G-J_W=sum_{n prime}P(N-n)*w_n
        +sum_{n in C}P(N-n)*max(-W(n),0)>=0.              (7)
Thus J_W<=G, but J_W is generally NOT the exact G=T-U identity. These
finite weights need not be samples from the asymptotic Lipschitz profile;
the finite identity and the source coefficient test have separate inputs.
The verifier retains both prime-square and negative-composite terms.

Exact profile verifier:
Continuous piecewise-linear profiles are specified by rational knots from
(1/3,0) to(1/2,0), with values in[0,1]. For an affine segment w=m*alpha+c,
  integral_l^r w/[alpha*(theta-alpha)]
    =(c/theta)*log(r/l)+(m+c/theta)*log((theta-l)/(theta-r)).
For2/3<=theta<=1 both log arguments lie in[1,2], so the existing rational
logarithm enclosure applies. The mathematical inequality(6) also treats
the lower source-admissible theta1 range; there B0=0. The numerical helper
deliberately covers only theta1>=2/3, where a positive lower-sieve term
could first appear, and does not certify distribution assumptions.
"""
from fractions import Fraction
from math import isqrt

from factored_linear_barrier import factored_bound, log_enclosure
from cubic_sieve import exact_floor_cuberoot
from redistribution import trial_prime


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


def _weight_knots(knots):
    if (type(knots) is not tuple or len(knots) < 2
            or any(type(k) is not tuple or len(k) != 2 for k in knots)
            or any(type(v) not in (int, Fraction) for k in knots for v in k)):
        raise ValueError("require a tuple of exact rational(alpha,height) knots")
    converted = tuple((Fraction(a), Fraction(h)) for a, h in knots)
    if (converted[0] != (Fraction(1, 3), 0) or converted[-1] != (Fraction(1, 2), 0)
            or any(not 0 <= h <= 1 for _, h in converted)
            or any(a >= b for (a, _), (b, _) in zip(converted, converted[1:]))):
        raise ValueError("require increasing knots from(1/3,0) to(1/2,0), heights in[0,1]")
    return converted


def _scaled_interval(coefficient, interval):
    low, high = interval
    return (coefficient*low, coefficient*high) if coefficient >= 0 else (coefficient*high, coefficient*low)


def weight_kernel_integral(knots: tuple, theta: int | Fraction,
                           terms: int = 12) -> tuple[Fraction, Fraction]:
    """Enclose I_theta for a continuous rational piecewise-linear weight.

    Requires2/3<=theta<=1 and the endpoint-zero knots described above.
    This is an exact integral enclosure, not prime-distribution evidence.
    """
    converted = _weight_knots(knots)
    if type(theta) not in (int, Fraction) or not Fraction(2, 3) <= theta <= 1:
        raise ValueError("require exact rational2/3<=theta<=1")
    theta = Fraction(theta)
    log_enclosure(1, terms)  # Validate precision even for the zero profile.
    low = high = Fraction(0)
    for (left, hleft), (right, hright) in zip(converted, converted[1:]):
        slope = (hright-hleft)/(right-left)
        intercept = hleft-slope*left
        part1 = _scaled_interval(intercept/theta, log_enclosure(right/left, terms))
        part2 = _scaled_interval(slope+intercept/theta,
                                 log_enclosure((theta-left)/(theta-right), terms))
        low += part1[0]+part2[0]
        high += part1[1]+part2[1]
    return max(Fraction(0), low), high


def weighted_cubic_coefficient(knots: tuple, theta_original: int | Fraction,
                               theta_switched: int | Fraction,
                               terms: int = 12) -> tuple[Fraction, Fraction]:
    """Enclose the weighted LOWER-CERTIFICATE coefficient, NOT actual G/K.

    Requires2/3<=theta_original<=1. theta_switched in(0,1] is a constant
    level or a uniform upper ceiling, as in switched_cubic_coefficient.
    The level1 choices are formal limiting benchmarks only.
    """
    base = switched_cubic_coefficient(theta_original, theta_switched, terms)
    original = Fraction(theta_original)
    switched = Fraction(theta_switched)
    i_original = weight_kernel_integral(knots, original, terms)
    i_one = weight_kernel_integral(knots, 1, terms)
    if original == 1:
        # The two identical weighted terms cancel algebraically at(1,1).
        log_low, log_high = log_enclosure(2, terms)
        mass = (max(Fraction(0), log_low-i_one[1]), log_high-i_one[0])
        return _scaled_interval(2*(1-1/switched), mass)
    return (base[0]+2*i_one[0]/switched-2*i_original[1],
            base[1]+2*i_one[1]/switched-2*i_original[0])


def weighted_switch_partition(target: int, survivors: bytearray,
                              composites: bytearray, prime_weights: dict
                              ) -> tuple[Fraction, Fraction, Fraction, Fraction, Fraction]:
    """Return(Sigma1,Sigma2,J_W,prime_loss,negative_composite_loss).

    A,C are truthful full cubic odd-slot inputs; shape checks do not prove
    that provenance. Prime weights are exact values in[0,1], keyed by odd
    primes z<p<=floor(sqrt(N-3)); repeated prime factors count ONCE. These
    finite weights do not establish an asymptotic Lipschitz profile or any
    distribution theorem. The last two outputs sum to exact G-J_W.
    """
    switch_partition(target, survivors, composites)  # Shared input validation.
    high = target-3
    z = exact_floor_cuberoot(high)
    if (type(prime_weights) is not dict
            or any(type(p) is not int or p % 2 == 0 or not z < p <= isqrt(high)
                   or not trial_prime(p) or type(w) not in (int, Fraction) or not 0 <= w <= 1
                   for p, w in prime_weights.items())):
        raise ValueError("require exact prime weights in[0,1] on odd primes z<p<=sqrt(H)")
    primes = bytearray(a-c for a, c in zip(survivors, composites))
    sigma1 = sigma2 = prime_loss = negative_loss = Fraction(0)
    for i, a in enumerate(survivors):
        if not primes[-1-i]:
            continue
        n = 3+2*i
        weight = 1-sum((Fraction(w) for p, w in prime_weights.items() if n % p == 0),
                       Fraction(0))
        sigma1 += a*weight
        sigma2 += composites[i]*max(weight, 0)
        prime_loss += primes[i]*(1-weight)
        negative_loss += composites[i]*max(-weight, 0)
    return sigma1, sigma2, sigma1-sigma2, prime_loss, negative_loss
