"""Remove small rare-sign factors from the conditional candidate pool.

Owner: Kevin's research. Purpose: control one composite-partner class using
the existing rare-prime sieve, without losing its small population factor.
Finite helpers verify the disjoint remainder indices and surviving factor
types. They do not detect an exceptional zero or prove a prime partner.
Sol checked the deduction and actual files. Five focused exact tests passed
normally and with Python -O; they verify algebra, not analytic estimates.

Theorem, deduction checked by Sol:
Keep ALL hypotheses of rare_prime_sieve.py, including
  24<D<=Y**(delta/4), 0<t=(1-beta)*log(Y)<=1/log(Y), m in F_D,
and the ACTUAL exceptional zero of the primitive quadratic character chi.
Take its fixed integer u sufficiently large for the upper fundamental
lemma at ratio u/2-1 as well as its original lower sieve. Put
  E=floor(Y**delta), z=ceil(Y**(delta/u)), w=floor(sqrt(E)).
Let B be the existing pool of primes p in J_m with chi(p)=+1 and partner
n=m-p coprime to D and with every prime factor>z. Let B_bad be those p
for which n has a prime divisor q satisfying z<q<=w and chi(q)=+1.
Then, uniformly in the stated regime,
  sum_{p in B_bad}log(p)=o(sum_{p in B}log(p)),
  |B_bad|=o(|B|),
  |B minus B_bad| >>_{delta,u} Y*t/log(Y)**2.             (1)
No stronger conductor or zero hypothesis is added. Constants and onset
remain ineffective, and no numerical delta,u or zero is supplied.

Relative sieve proof:
1. Use X,V(z),g and the prime-weighted divisor counts A_e=X*g(e)+r_e
   of rare_prime_sieve.py. Its progression proof covers ALL squarefree
   e<=E, not merely e with prime factors<=z. In particular, with L=log(Y),
     R=sum_{e<=E, mu(e)**2=1}|r_e|
       <<Y*A/phi(D)*(t**8*L+L**2/D)+Y**(1/2+o(1))
        =o(X*V(z)).                                    (2)
   A is the finite allowed-unit count; A/phi(D) is1 or1/2. All endpoint,
   nonreduced-residue and proper-prime-power errors are included in (2).
   The pool lower bound is sum_{p in B}log(p)>>X*V(z).
2. For a prime q with z<q<=w, chi(q)=+1 and q not dividing Dm, upper
   sieve the subsequence q|(m-p) through z. The level is floor(E/q).
   Because q>z, the supporting squarefree d have q not dividing d, and
   g(qd)=g(q)*g(d). Since q<=sqrt(E),
     log(floor(E/q))/log(z)>=u/2-o(1).
   Choose u large enough that Ford's uniform upper fundamental lemma
   gives a main factor at most2. Its coefficients have |lambda_d^(q)|<=1
   and support d<=E/q, with every prime divisor<=z. Thus
     sum_{p in B, q|(m-p)}log(p)
       <=2*X*g(q)*V(z)+sum_{d in this support}|r_(qd)|. (3)
   If q divides Dm the corresponding prime count is zero, as in the
   previous proof. Source: Ford2023, Theorem3.6(a,b), printed p38:
   https://ford126.web.illinois.edu/sieve2023.pdf
3. The map (q,d)->qd in (3) is INJECTIVE across all these q: qd is
   squarefree and has exactly ONE prime factor above z, namely q.
   Consequently summing its remainders costs at most R, with no factor
   counting q or divisors. A candidate can have several qualifying q;
   the union bound may overcount candidates, which is harmless for this
   upper bound. Let
     H=sum_{z<q<=w, q prime, chi(q)=+1}1/(q-1).
   Equations (2)-(3) imply
     sum_{p in B_bad}log(p)<=2*X*V(z)*H+R.              (4)

The small-factor rarity input:
4. Put eta=1/((1-beta)*log(D)), v=log(z)/log(D), and lambda=1*chi
   (Dirichlet convolution, NOT a sieve coefficient or Liouville function).
   Matomaki--Merikoski, Lemma2.2, states for w>z=D**v that
     sum_{z<=a<=w, (a,P(z))=1}lambda(a)/a
       <<[1/(v**2*eta**(v/2))
                    +(v/eta)*log(w)/log(z)+1/z]
                                                  *(log(w)/log(z))**2.
   Source: https://arxiv.org/html/2112.11412v2#S2
   Its definition uses P(z)=product of primes STRICTLY below z; our prime
   sub-sum q>z lies inside this support under either endpoint convention.
   The lemma allows every v>0 and eta>=10. It uses nonnegative lambda,
   not a claim about independent prime factors. For a sign+ prime q,
   lambda(q)=2 and 1/(q-1)<=2/q, so this estimate bounds H directly.
5. Here v>=4/u and log(w)/log(z)<=u/2, from the integer cutoffs and
   D<=Y**(delta/4). Also
     (v/eta)*log(w)/log(z)=log(w)/(eta*log(D))<=delta*t/2,
     eta>=4/(delta*t)>=4*log(Y)/delta.
   Thus the source estimate gives
     H <<_{delta,u} eta**(-2/u)+t+1/z=o(1).             (5)
   This controls primes below D to a fixed positive power as well as the
   larger ones. A direct Linnik prime progression estimate alone would
   have required an additional lower size condition; that condition is
   NOT inserted into (1), because Lemma2.2 supplies the needed range.
6. Combining (4)-(5) with (2) proves the weighted proportion assertion.
   Since log(Y/2)<log(p)<=log(Y) throughout J_m, the same negligible
   proportion holds for ordinary counts. The earlier lower bound then
   proves the last assertion in (1). This does not claim the loss is
   O(t) relative to the pool: eta**(-2/u) can be much larger than t.

Remaining factor configurations:
Every retained partner has sign- and no sign+ prime factor<=w. If its
total prime-factor multiplicity Omega is even, it must therefore have a
sign+ prime factor>w, with complementary factor <Y/w. If Omega is odd,
it can still consist entirely of sign- factors. Both alternatives really
allow composites: for chi modulo31, 209=11*19 has one sign+ factor19
above10, while 1331=11**3 has no sign+ factor at all. These finite examples
assert no exceptional zero. The large rare-factor correlation and the odd
composite case remain unproved; there is no P_2 or Goldbach conclusion.
"""
from math import isqrt

from exceptional_character_model import character_values
from major_arc_kernel import _factorization


def sieve_index_split(index: int, cutoff: int, level: int) -> tuple[int, int] | None:
    """Recover the unique (q,d) in the switched upper-sieve support, or None.

    q is prime with cutoff<q<=floor(sqrt(level)); d is squarefree, has only
    prime factors<=cutoff, and q*d<=level. This checks algebraic support,
    not the character sign or a prime-count estimate. Squareful indices
    and other out-of-support positive indices return None.
    """
    if any(type(v) is not int for v in (index, cutoff, level)):
        raise ValueError("index, cutoff and level must be integers")
    if index < 1 or cutoff < 2 or level < 1:
        raise ValueError("require index>=1, cutoff>=2 and level>=1")
    if index > level:
        return None
    factors = _factorization(index)
    if any(exponent != 1 for _, exponent in factors):
        return None
    large = [p for p, _ in factors if p > cutoff]
    if len(large) != 1 or large[0] > isqrt(level):
        return None
    return large[0], index//large[0]


def partner_factor_profile(partner: int, conductor: int, cutoff: int, bound: int, *,
                            two_sign: int = 1
                            ) -> tuple[int, int, tuple[int, ...], tuple[int, ...]]:
    """Return sign+/sign- multiplicities and distinct small/large sign+ primes.

    Requires a sign- partner coprime to the primitive character conductor,
    with every prime factor>cutoff and cutoff<=bound. Small means<=bound.
    Repeated factors count repeatedly in the first two entries, but only
    once in each prime list. No target or exceptional zero is asserted.
    """
    if any(type(v) is not int for v in (partner, cutoff, bound)):
        raise ValueError("partner, cutoff and bound must be integers")
    if partner < 2 or cutoff < 2 or bound < cutoff:
        raise ValueError("require partner>=2 and 2<=cutoff<=bound")
    chi = character_values(conductor, two_sign=two_sign)
    if chi[partner % conductor] != -1:
        raise ValueError("partner must be a unit of character sign-1")
    factors = _factorization(partner)
    if any(p <= cutoff for p, _ in factors):
        raise ValueError("partner has a prime factor at or below the cutoff")
    positive = sum(e for p, e in factors if chi[p % conductor] == 1)
    negative = sum(e for p, e in factors if chi[p % conductor] == -1)
    small = tuple(p for p, _ in factors if chi[p % conductor] == 1 and p <= bound)
    large = tuple(p for p, _ in factors if chi[p % conductor] == 1 and p > bound)
    return positive, negative, small, large
