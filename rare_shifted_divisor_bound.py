"""A second rarity factor for coefficient-one shifted primes, conditionally.

Owner: Kevin's Goldbach research. Purpose: preserve an arithmetic component
and its exact algebraic verifiers for the still-open variable-coefficient
prime correlation. This is a deduction from existing source theorems, with
no external novelty claim and no assertion that an exceptional zero exists.

Statement (NEW RESTRICTED REGIME, not the earlier fixed-u regime):
Let chi be primitive quadratic modulo D>24 with an ACTUAL real zero
  beta=1-1/(eta*log D), eta sufficiently large.
Put X=D^V, L=log X, t=V/eta and assume
  V >= (log eta)^3, 0<t<=1/L.
For every positive even integer h<=X/2, define Q++ as the sum of
log p*log(p+h) over X<p<=2X with p,p+h prime and chi(p)=chi(p+h)=+1.
Then, uniformly in these parameters,
  Q++ << S_2(h)*X*t^2*(log eta)^8 = o(S_2(h)*X*t).        (1)
The little-o is as eta tends to infinity within the stated regime. S_2
is the usual two-prime singular series, comparable to h/phi(h) for even h.
This is an upper bound, not a pair-existence or lower-bound theorem.

Source: Matomaki--Merikoski, arXiv:2112.11412v2, Proposition2.3,
equation(15), Lemma2.4 and the smooth partition in Section7:
https://arxiv.org/html/2112.11412v2 . Source checked2026-09-09.
Here lambda_chi=1*chi, NOT Liouville's lambda. It is nonnegative, and
lambda_chi(p)=2 at a positive-character prime. We use a majorant directly;
we do not import the source's larger prime-to-divisor replacement error.

Proof, including the cancellation and uniformity budget:
1. Fix sufficiently large constants A,K with AK/3000>100, then a fixed
   beta-sieve parameter sufficiently large in terms of A. Set U=K*log eta,
   z=X^(1/U), v=V/U. Eventually U>=1000*beta_sieve and z>D. This growing
   U is justified by the EXPLICIT U-uniform source statements. It is not
   obtained by changing the parameter order of earlier fixed-u repo bounds.
   P(z) means product of primes STRICTLY LESS THAN z throughout this module.
   Let g be a fixed nonnegative smooth majorant, equal to1 on[1,2], at most1,
   supported in[9/10,21/10]. Both n,n+h on its support are comparable to X.
   Since primes in question exceed z, positivity gives
     Q++ << L^2 * sum_(n(n+h) coprime P(z)) g(n/X)
                                      lambda_chi(n)*lambda_chi(n+h). (2)

2. Take a fixed C-infinity H with H(s)+H(1/s)=1, H=1 on s<=1/2,
   H=0 on s>=2, and 0<=H<=1. Swapping divisors proves the EXACT identity
     lambda_chi(n)=sum_(dk=n) H(d/k)*(chi(d)+chi(k)).     (3)
   H(1)=1/2 handles squares, and its support gives d<=sqrt(2n).
   All factors of a rough n are units since z>D. Insert principal-character
   factors on the unweighted arguments, expand the four orientations, and
   use a nonnegative smooth dyadic partition of the two small factors d.
   There are O(L^2) boxes. Each has M_j*N_j comparable to X, M_j<<N_j,
   and fixed smooth derivative constants, as required by Proposition2.3.
   Initial boxes containing d=1 can use scales >=1 with a fixed adjustment
   to the partition; no small-factor atom is discarded.

3. In either orientation the source main's small-factor character is
   chi_i(d)*psi_i(d)=chi(d). Sum ALL four orientation main terms and ALL
   dyadic boxes BEFORE taking absolute values. The resulting main is
     V_(h,D)(z)*K_h(D)*integral g(y/X)*A_z(y)*A_z(y+h) dy, (4)
   where
     A_z(y)=sum_(d coprime P(z)) chi(d)/d * H(d^2/y),
     K_h(D)=D^-1 sum_(a mod D)(chi0+chi)(a)*(chi0+chi)(a+h),
     V_(h,D)(z)=product_(p<z,p not dividing D)(1-rho_h(p)/p),
   rho_h(p)=1 if p divides h, and2 otherwise. The recombination follows
   directly from the partition of unity inside the source integral; taking
   boxwise absolute values here would lose unnecessary logarithms. The
   source main has no remaining coprimality restriction between the two d's.

4. Write C_z=product_(p<z)(1-1/p)^-1, comparable to L/U. Lemma2.4,
   at the SAME N comparable to sqrt X, evaluated at y=X and y=X^2,
   has the same main C_z. Subtraction therefore gives
     sum_(d<=N,d coprime P(z)) chi(d)/d = O(E/U),         (5)
   with the explicit source error
     E=U^4/(v^2*eta^(v/2))+v*U^5/eta+U^4/z
                      +exp(-A*U/3000)+exp(-C*sqrt L).
   We chose the source epsilon=1/10 and fixed C>=2. Indeed the difference
   of the log weights is L, so the main cancels and the errors cost C_z*E/L.
   Abel summation now gives A_z(y)=O(E/U): H(d^2/y) varies only for
   d comparable to sqrt y. Thus all required N are within [X^(1/10),X^2].
   This argument INCLUDES the d=1 atom; it does not assume a bound at small N.
   Since V>=log^3 eta and t=V/eta, the displayed error satisfies
     E << t*U^4 + eta^-20.                              (6)
   For example v>=log^2 eta/K, log z=L/U>>log^2 eta,
   sqrt L>>log^(3/2) eta, while v*U^5/eta=t*U^4.

5. If A_D(h) counts unit pairs a,a+h modulo D, then
     0<=K_h(D)=4*#{a:chi(a)=chi(a+h)=1}/D<=4*A_D(h)/D.
   CRT supplies exactly the omitted conductor-prime local factors because
   z>D. Mertens and the convergent singular-series tail give
     (A_D(h)/D)*V_(h,D)(z) << S_2(h)/log^2 z.
   Equations(4)-(6) therefore bound the main in(2) by
     S_2(h)*X*E^2/L^2 before, and S_2(h)*X*E^2 after, its L^2 factor.
   The SECOND rarity factor comes from TWO character partial sums in(5),
   not from assuming independence of the two prime sign conditions.

6. Proposition2.3 and(15), with fixed smoothing, give after summing O(L^2)
   boxes and multiplying by the prime-log majorant L^2 the total error
     O_A(X^(7/9)*D^2*L^4
           + S_2(h)*X*L^2*(U^6/z+exp(-A*U/3000))).     (7)
   From tL<=1 we have V^2*log D<=eta and L<=eta. Together with
   V>=log^3 eta these make(7) O(S_2(h)*X*eta^-10). The exponent100 choice
   in step1 leaves room for every displayed logarithm. Also t>=log^3 eta/eta,
   so eta^-10=o(t^2). Finally t<=1/sqrt(eta*log D), whence
   t*(log eta)^8 tends to0. Equations(2)-(7) prove(1).

Scope and the failed transfer:
The motivating switched terms involve q and p=m-M*q, chi(M)=-1, with
M growing up to Y^(13/25). Proposition2.3 only supplies the coefficient-one
relation +/-d1*k1+h=d2*k2. Substituting n=M*q would destroy this majorant:
chi(M*q)=-1 implies lambda_chi(M*q)=0, whereas lambda_chi(q)=2.
Absorbing M into a divisor introduces divisibility and quotient-character
constraints outside the cited theorem. No uniform estimate for this M range
is proved here. Nor does(1) estimate the required rare/common Goldbach pair
on suppressed targets. Even its large-V hypothesis is an extra restriction.
The direct multiplicative majorant tested first retained the empty cofactor
atom1 and gave no second rarity factor; (5) supplies the missing cancellation
only in the geometry just proved. Preserve the polynomial tools for a future
combination; neither this success nor that failure settles their usefulness.

Follow-on: rare_affine_small_cofactor.py now supplies a DIRECT affine proof
for the aggregate over original-Y^theta-rough M<=Y^(1/5), in the same new
large-V regime. Its total rare/rare contribution is o(Y*t), also after
fixed polynomial kernel weights. The full M<=Y^(13/25) range remains open;
the follow-on does not obtain it by the invalid substitution described here.

The finite routines below verify identities and local factors only. Their
rational reflection weight is NOT smooth and is not used in the analytic
proof. No finite character, test, or symbolic identity proves an actual zero,
an effective onset, a signed prime estimate for M, or new Goldbach coverage.
"""
from fractions import Fraction
from math import gcd, isqrt, prod

from exceptional_character_model import character_values
from major_arc_kernel import _factorization


def _positive_integer(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def reflection_weight(d: int, k: int) -> Fraction:
    """Exact nonsmooth fixture with H(d/k)+H(k/d)=1."""
    _positive_integer(d, "d")
    _positive_integer(k, "k")
    if 2*d <= k:
        return Fraction(1)
    if d >= 2*k:
        return Fraction(0)
    return Fraction(2*k-d, d+k)


def hyperbola_orientations(n: int, conductor: int) -> tuple[Fraction, Fraction]:
    """The two exact sums in(3), retaining squares and the d=1 atom."""
    _positive_integer(n, "n")
    chi = character_values(conductor)
    left = right = Fraction(0)
    for d in range(1, isqrt(2*n)+1):
        if n % d == 0:
            k = n//d
            weight = reflection_weight(d, k)
            left += weight*chi[d % conductor]
            right += weight*chi[k % conductor]
    return left, right


def rough_log_form(limit: int, cutoff: int, conductor: int):
    """Exact coefficients of sum chi(n)*log(y/n)/n over P(cutoff)-rough n.

    Returns (coefficient of log y, sorted (prime, coefficient of log prime)).
    P(cutoff) contains primes STRICTLY BELOW cutoff. Includes n=1.
    """
    _positive_integer(limit, "limit")
    _positive_integer(cutoff, "cutoff")
    chi = character_values(conductor)
    slope = Fraction(0)
    constant = {}
    for n in range(1, limit+1):
        factors = _factorization(n)
        if any(p < cutoff for p, _ in factors):
            continue
        term = Fraction(chi[n % conductor], n)
        slope += term
        for p, exponent in factors:
            constant[p] = constant.get(p, Fraction(0))-exponent*term
    return slope, tuple((p, c) for p, c in sorted(constant.items()) if c)


def shifted_local_factors(conductor: int, shift: int, cutoff: int):
    """Return K_h, A_D(h)/D, omitted-D product, and full rough product.

    Requiring cutoff>D makes the conductor-factor restoration exact.
    This finite function accepts odd shifts too, exposing their local zero.
    """
    _positive_integer(shift, "shift")
    _positive_integer(cutoff, "cutoff")
    chi = character_values(conductor)
    if cutoff <= conductor:
        raise ValueError("cutoff must exceed conductor")
    unit_pairs = sum(gcd(a, conductor) == gcd(a+shift, conductor) == 1
                     for a in range(conductor))
    positive_pairs = sum(chi[a] == chi[(a+shift) % conductor] == 1
                         for a in range(conductor))
    primes = [p for p in range(2, cutoff) if _factorization(p) == ((p, 1),)]
    factors = {p: Fraction(p-(1 if shift % p == 0 else 2), p) for p in primes}
    omitted = prod((v for p, v in factors.items() if conductor % p), start=Fraction(1))
    full = prod(factors.values(), start=Fraction(1))
    return (Fraction(4*positive_pairs, conductor), Fraction(unit_pairs, conductor),
            omitted, full)
