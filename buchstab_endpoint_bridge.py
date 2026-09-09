"""Isolate a small actual endpoint loss; the unbalanced correlation is OPEN.

Owner: Kevin's Goldbach research. Purpose: test whether an arithmetic bound
already proved in balanced_semiprime_budget.py can replace the demand for
bilinear cancellation at nearly equal factors. Preserve this exact reduction
and its executable support checks for the next arithmetic pursuit. This is
not a prime-correlation estimate, a new coverage theorem or a novelty claim.
Sol independently checked the theory, actual files and the final test delta.
Five focused exact tests passed normally and with Python -O.

Question and outcome:
Can we sieve the actual rare-prime partner up to just below its square root,
pay for the remaining composites using the earlier rare-factor estimate,
and leave an explicit sum with a prime least factor below that endpoint?
Yes, as a reduction. The needed upper estimate for that sum is UNPROVED.
This uses an actual arithmetic loss bound, not a formal simplex density.

Exact identity, including repeated factors:
For any finitely supported real/complex weight A(n), n>=2, define
  S_A(v)=sum_{P^-(n)>v} A(n),
  U_A(z,R)=sum_{z<q<=R, q prime}
               sum_{k>=q, P^-(k)>=q} A(q*k)
             + sum_{z<q<=R, q prime} A(q).
Equivalently the inner sum includes k=1, with P^-(1)=infinity.
Every n counted in S_A(z)-S_A(R) has exactly one least prime q in(z,R].
Therefore, EXACTLY,
  S_A(R)=S_A(z)-U_A(z,R).                              (1)
The >=q condition is essential: replacing it by >q loses q^2 and q^j.
In the analytic application below A is supported on J subset(Y/2,Y]
and R<Y/2, so A(q)=0 and every removed term has two factors >1.
No sorting of character signs or attribution of a repeated factor is used.

Actual arithmetic application (deduction from the checked earlier bounds):
Keep all actual-zero, target and parameter hypotheses of
balanced_semiprime_budget.py: 0<epsilon<=1/100, sufficiently small fixed
delta<=epsilon/3, fixed sufficiently large u, theta=delta/u, z=ceil(Y^theta),
24<D<=Y^(delta/4), t=(1-beta)*log(Y) in(0,1/log(Y)], and m in F_D.
Let J={n:n,m-n in(Y/2,Y]}, L=log(Y), R=floor(Y^(1/2-2epsilon)), and
  A(n)=log(m-n)*log(n) * 1_{n in J, m-n prime,
                           chi(m-n)=+1, gcd(n,D)=1}.
We use the full rare-first pool before the optional B_good pruning.
The sign theorem in rare_prime_sieve.py gives chi(n)=-1 on this support.
Write P for the positive-sign-first actual weighted prime-pair sum, exactly
the P of character_partner_weight.py, and Z=length(J_real)*S_2(m)*t.

Eventually (R+1)^3>Y, since 3*(1/2-2epsilon)>1. Thus an R-rough n<=Y
has at most two prime factors, WITH multiplicity. A unit square has
character +1 and cannot occur. Consequently, EXACTLY,
  S_A(R)=P+E_R, E_R>=0,                                (2)
where E_R consists of distinct semiprimes n=r*q with one positive-sign
prime q and one negative-sign prime r. Both exceed R, whence
  Y^(1/2-2epsilon)<q<Y^(1/2+2epsilon).                 (3)
This also shows R>w eventually, so these terms meet the earlier large-rare-
factor condition. No claim that the entire small-z pool is squarefree.

The actual upper bound in balanced_semiprime_budget.py, steps4-5, now gives
  E_R <= C*epsilon*Z + o(Y*t),                          (4)
with C absolute. For each actual positive-sign q in(3), Henriot's corrected
two-linear-form bound counts r prime and m-q*r prime by
  C*(Y/q)*S_2(m)/L^2.
Drop the first-prime sign condition only in this upper bound. Each weight
is <=L^2. Repaired bulk Linnik and partial summation give
  sum_{q in(3), prime, chi(q)=+1}1/q
       =2*epsilon*t+o(t/loglog(Y)).
Combine these and S_2(m)<<loglog(Y), length(J_real)>=Y/4. There is ONE
rarity factor t, not t^2. This deduction does not need the cubic minorant.
Sources are the already checked deductions in balanced_semiprime_budget.py
and relative_type_i.py, with corrected Henriot, printed p377:
https://doi.org/10.1017/S0305004114000280
and Thorner--Zaman Theorem2.1 and(4.2):
https://arxiv.org/html/2108.10878 . Tao Proposition23 is not the authority.

The available initial mass and the precise new test:
Use EXACT X and g from rare_prime_sieve.py,
  X=A_D(m)/(2*phi(D))*integral_{J_real}(1-v^(beta-1))dv,
  V(z)=product_{ell<=z}(1-g(ell)),
  g(ell)=1/(ell-1) if ell does not divide D*m, and 0 otherwise.
Here A_D is the allowed residue count, distinct from the sequence A(n).
The upper/lower fundamental lemma with its fixed error eta_u and the
already proved relative remainders give
  S_A(z)=L*X*V(z)+O(eta_u*L*X*V(z))+o(Y*t).           (5)
Multiplying the prime-log count by log(n)=L+O(1) costs only o(Y*t) at
fixed theta. On F_D, L*X*V(z)=O(Z/theta) with an absolute constant:
all D-primes>=5 divide m; the only possible extra local factor is at3
and is bounded. Ordinary Mertens and the singular-series tail suffice.
Thus (1)-(5) prove
  P=L*X*V(z)-U_A(z,R)-E_R
               +O((eta_u/theta)*Z)+o(Y*t).            (6)
Choose epsilon, then delta, then u, then Y. The fixed sieve error is NOT
an o_Y(1) error. In particular a proof, for some fixed c>0, of the
one-sided arithmetic estimate
  U_A(z,R) <= L*X*V(z)
                 -(c+C*epsilon+C0*eta_u/theta)*Z      (7)
with valid constants C,C0 would imply P>=c*Z+o(Y*t)>0. No such estimate
has been established. The left side samples the two linked prime conditions
q prime and m-q*k prime, with k q-rough and chi(q*k)=-1. Its coefficients
and ordering are specified. The condition P^-(k)>=q couples q and k;
it is not a separated-coefficient Type II sum without a further argument,
and it is not an all-coefficient Type II estimate.
Nor is replacing it by its formally expected value evidence for (7).

What changed, and what did not:
The endpoint error has a proved small arithmetic budget. Cancellation is
now requested only in the displayed prime-times-rough sum below R. This
range also includes smaller factors than the older Vaughan target, so it
is NOT simply a subset or a proved easier equivalent. At fixed theta the
small-z main is of order Z/theta; the required surplus is of order Z.
An absolute error on the larger pool scale need not certify this surplus.
Ford--Maynard Theorems2.4-2.5 motivated this question by showing why a
generic missing balanced range cannot merely be dropped:
https://www.ford126.web.illinois.edu/wwwpapers/prime-producing-sieves.pdf
Their prime-producing conclusion is NOT invoked; their comparison and
boundedness hypotheses have not been proved for our signed rare-scale model.

Polynomial tools remain available. Identity(1) also holds for the signed
weight log(m-n)*K_f(n), but its initial S(z) is the FULL kernel sum, not
the accessible-divisor T_low,f. Formula(5) is proved here only for the
nonnegative A above. Substituting the old formal or accessible main for a
different full kernel total would reopen the already identified gap.
No new actual coverage, zero, numerical onset, or correlation estimate.
"""
from dataclasses import dataclass
from fractions import Fraction as F

from exceptional_character_model import character_values
from major_arc_kernel import _factorization


@dataclass(frozen=True)
class BuchstabSplit:
    initial: F
    removed_by_prime: tuple[tuple[int, F], ...]
    terminal: F

    @property
    def removed(self) -> F:
        return sum((mass for _, mass in self.removed_by_prime), F(0))


def buchstab_split(weights: list, small_cutoff: int, terminal_cutoff: int) -> BuchstabSplit:
    """Finite rational identity (1), not a prime-asymptotic calculation.

    Signed weights are allowed. The tuple retains zero-sum least-factor
    buckets if their support was nonempty. Positions0,1 must have zero weight.
    """
    if (type(weights) is not list or len(weights) < 3
            or any(type(v) not in (int, F) for v in weights)
            or weights[0] != 0 or weights[1] != 0):
        raise ValueError("require a rational list indexed from0, zero at0 and1")
    if (type(small_cutoff) is not int or type(terminal_cutoff) is not int
            or not 2 <= small_cutoff <= terminal_cutoff < len(weights)):
        raise ValueError("require integer 2<=z<=R<=supported limit")
    initial, terminal = F(0), F(0)
    removed = {}
    for n, value in enumerate(weights[2:], 2):
        if not value:
            continue
        least = _factorization(n)[0][0]
        if least > small_cutoff:
            initial += value
            if least <= terminal_cutoff:
                removed[least] = removed.get(least, F(0))+value
            else:
                terminal += value
    return BuchstabSplit(initial, tuple(sorted(removed.items())), terminal)


def endpoint_factors(n: int, limit: int, cutoff: int) -> tuple[int, ...]:
    """Return the one or two prime factors of a rough n, retaining squares.

    Requires the exact finite condition (cutoff+1)^3>limit. This is a
    structural verifier; no relation between a finite sample and a zero.
    """
    if (any(type(v) is not int for v in (n, limit, cutoff))
            or not 2 <= n <= limit or not 2 <= cutoff < limit
            or (cutoff+1)**3 <= limit):
        raise ValueError("require 2<=n<=limit, 2<=R<limit, (R+1)^3>limit")
    factors = tuple(p for p, exponent in _factorization(n) for _ in range(exponent))
    if factors[0] <= cutoff:
        raise ValueError("n must have every prime factor strictly above R")
    return factors


def negative_endpoint_factors(n: int, limit: int, cutoff: int, conductor: int,
                             *, two_sign: int = 1) -> tuple[tuple[int, int], ...]:
    """Prime/sign pairs; a negative unit cannot be a square at the endpoint."""
    factors = endpoint_factors(n, limit, cutoff)
    chi = character_values(conductor, two_sign=two_sign)
    if chi[n % conductor] != -1:
        raise ValueError("require a unit n with character sign-1")
    return tuple((p, chi[p % conductor]) for p in factors)


def endpoint_exponents(epsilon: F) -> tuple[F, F, F]:
    """Exact lower/upper rare-factor exponents and slack excluding triples.

    epsilon is a fixed theorem parameter; the returned slack is not an
    effective onset for the distribution hypotheses.
    """
    if type(epsilon) is not F or not 0 < epsilon <= F(1, 100):
        raise ValueError("require exact Fraction 0<epsilon<=1/100")
    lower = F(1, 2)-2*epsilon
    return lower, 1-lower, 3*lower-1
