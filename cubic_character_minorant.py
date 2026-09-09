"""A signed cubic weight removes very unbalanced semiprime partners.

Owner: Kevin's research. Purpose: test an algebraic way to remove the
remaining large-positive-factor tail without assuming a second rarity gain.
This changes the weighted total; it does not prove its positivity.
The finite helpers return exact polynomials in logarithms of prime factors.

Sol checked the theory and actual files. Five focused exact tests passed
normally and with Python -O; these tests verify finite algebra only.

Deduction independently checked by Sol:
Keep the actual character/zero hypotheses and the SAME pruned pool B_good
of character_partner_weight.py and rare_twisted_bv.py. Write
  W=chi*log, U=chi*log^3, K(n)=10*W(n)-9*U(n)/log(n)^2.
Here * is Dirichlet convolution, log^3 is the pointwise cube, and n>1.
On negative-sign primes, K(n)=log(n), preserving the original prime weight.

Nonnegative comparison and exact cancellation:
1. Let lambda=1*chi and Lambda_3=mu*log^3. Then U=lambda*Lambda_3>=0.
   Indeed lambda>=0. For n with k distinct prime factors and log factors
   x_i, Lambda_3 is the mixed finite difference of s^3 with steps x_i,
   based at sum_i (v_i(n)-1)*x_i>=0. For k<=3 it is nonnegative by the
   nonnegative kth derivative on [0,infinity); for k>3 it vanishes.
   Thus K<=10W pointwise, including repeated factors and nonunits.
   The standard starting identity W=lambda*Lambda is recorded in
   Matomaki--Merikoski, Section2, equations (9)-(10):
   https://arxiv.org/html/2112.11412v2#S2
   The cubic finite-difference deduction is given here, not attributed to
   a theorem that the source does not state.
2. For a squarefree negative-sign semiprime n=r*q, chi(r)=-1, chi(q)=+1,
   put x=log(r), y=log(q). Direct divisor expansion gives
     W=2*x, U=2*x^3+3*x^2*y+3*x*y^2,
     log(n)^2*K(n)=x*(2*x-y)*(x+7*y).                 (1)
   Hence K<=0 exactly when q>=r^2, equivalently q>=n^(2/3).
   Equality cannot occur for the two distinct actual primes; it remains
   the exact boundary of the polynomial identity. If a squarefree partner
   has at least three negative-sign prime factors, W=0, so K<=0 there too.
   These negative contributions may be dropped only in an UPPER bound for
   the weighted total. In particular, K is not a nonnegative replacement.
3. More generally, the prime-normalized family
     K_kappa=(1+kappa)*W-kappa*U/log(n)^2, kappa>2 fixed,
   has semiprime value 2*x-kappa*x*y*(y-x)/(x+y)^2. It is nonpositive when
     log(q)/log(n)>=(1+sqrt(1+16/kappa))/4.
   This threshold tends to1/2 from above as kappa grows; no estimate here
   is uniform in a growing kappa. The fixed choice kappa=9 gives (1).
   log_weight_barrier.py checks the broader limitation: nonnegative higher
   logarithmic penalties cannot reduce the q<=r weights.
   A formal positive-part integral also records the cubic weight's cost;
   it is not a density assertion for actual prime factors.

One-sided prime-pair reduction:
4. Define the NEW signed total
     T_K(m)=sum_{p in B_good}log(p)*K(m-p).
   The prime part is exactly the SAME positive-first prime-pair mass P.
   Let E_mid be its semiprime contribution from
     w*<q<r^2, chi(q)=+1, chi(r)=-1, r>z,
   with the original interval and prime-first restrictions. Each term in
   E_mid is positive. The remaining semiprimes q>=r^2 contribute negatively.
   The contribution from q<=w* is bounded ABOVE by10 times its previously
   negligible W contribution. The same upper bound applies to repeated
   factors and squarefree partners with at least two positive factors.
   Squarefree partners with several negative factors contribute <=0.
   Consequently, uniformly in the existing regime and with ineffective onset,
     T_K(m)<=P(m)+E_mid(m)+o(Y*t),                    (2)
   where the error on the right can be chosen nonnegative. In particular
   the remaining positive semiprimes have r>n^(1/3) and q>w*, and the
   arbitrarily large-q tail has disappeared from this ONE-SIDED inequality.
   This is not T=P+E_mid+o(Y*t), and gives no lower comparison T_K>=c*T.
   Proving T_K>E_mid+the error would imply P>0; that inequality is open.
   There is no new prime-pair coverage, actual zero or numerical onset.

Finite verifier meaning:
Each polynomial is a sorted tuple ((p1,p2,p3), coefficient), representing
coefficient*log(p1)*log(p2)*log(p3). Repeated prime entries encode powers.
The second polynomial is log(n)^2*K(n), not K(n) itself. The cap n<=20000
matches the existing finite prefix; it has no analytic significance.
"""
from collections import defaultdict
from itertools import product

from character_partner_weight import negative_log_coefficients
from exceptional_character_model import character_values
from major_arc_kernel import _factorization


def _negative_input(n: int, conductor: int, two_sign: int):
    if type(n) is not int or not 2 <= n <= 20000:
        raise ValueError("require integer 2<=n<=20000 for the finite verifier")
    chi = character_values(conductor, two_sign=two_sign)
    if chi[n % conductor] != -1:
        raise ValueError("n must have character sign-1")
    return chi, tuple(_factorization(n))


def negative_cubic_coefficients(n: int, conductor: int, *, two_sign: int = 1
                                ) -> tuple[tuple, tuple]:
    """Return the exact degree-three polynomials (U(n), log(n)^2*K(n)).

    Requires a negative-sign unit and primitive quadratic character, with
    n<=20000. Coefficients are integers; no logarithm is numerically evaluated.
    """
    chi, factors = _negative_input(n, conductor, two_sign)
    cubic = defaultdict(int)
    for powers in product(*(range(exponent+1) for _, exponent in factors)):
        divisor = 1
        linear = []
        for (prime, exponent), power in zip(factors, powers):
            divisor *= prime**power
            if exponent > power:
                linear.append((prime, exponent-power))
        sign = chi[divisor % conductor]
        for a, b, c in product(linear, repeat=3):
            cubic[tuple(sorted((a[0], b[0], c[0])))] += sign*a[1]*b[1]*c[1]
    numerator = defaultdict(int, {monomial: -9*value for monomial, value in cubic.items()})
    for prime, coefficient in negative_log_coefficients(n, conductor, two_sign=two_sign):
        for (a, a_exponent), (b, b_exponent) in product(factors, repeat=2):
            numerator[tuple(sorted((prime, a, b)))] += 10*coefficient*a_exponent*b_exponent
    return (tuple(sorted((key, value) for key, value in cubic.items() if value)),
            tuple(sorted((key, value) for key, value in numerator.items() if value)))


def negative_semiprime_sign(n: int, conductor: int, *, two_sign: int = 1
                             ) -> tuple[int, int, int]:
    """Return (negative prime r, positive prime q, sign of K(r*q)).

    Requires two distinct prime factors, a negative-sign unit, and n<=20000.
    Comparison q versus r^2 determines the exact sign without rounded logs.
    """
    chi, factors = _negative_input(n, conductor, two_sign)
    if len(factors) != 2 or any(exponent != 1 for _, exponent in factors):
        raise ValueError("require a squarefree semiprime")
    negative = next(prime for prime, _ in factors if chi[prime % conductor] == -1)
    positive = next(prime for prime, _ in factors if chi[prime % conductor] == 1)
    sign = (negative*negative > positive)-(negative*negative < positive)
    return negative, positive, sign
