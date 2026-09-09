"""Squarefree correlation beats the preceding balanced linear budget.

Owner: Kevin's Goldbach research. Purpose: test a second cancellation step
at the actual smooth-model box where composite linear completion gave13/12.
The mechanism is Cauchy, prime correlation, CRT and a costed partition of
nonunit modes. This is not a signed prime-pair estimate or a novelty claim.
Prime powers, further box coverage and the original arithmetic transfer
remain separate requirements. All polynomial tools are preserved.

Checked primary source: Fouvry--Kowalski--Michel, Algebraic trace functions
over the primes, arXiv:1211.6043v3, Theorem1.17, Proposition3.1, section3,
and Propositions6.1--6.2: https://arxiv.org/pdf/1211.6043v3 .
We use Proposition3.1's PRIME correlation theorem, not an unstated
composite version of Theorem1.17. Kl3 has fixed conductor and is an
irreducible non-exceptional trace weight (rank3). Its bounded value at0
can be changed without affecting a square-root correlation bound.

Write, for squarefree q, including q=1 with K_1=1,
  K_q(z)=q^-1 sum_(u,v units modq)e_q(u+v+z/(u*v)).
For prime p, K_p(0)=1/p. On units this is normalized Kl3. We use this
explicit extension everywhere, including nonunit multipliers.

I. A squarefree bilinear estimate, derived from the prime source.
For M,N>=1, arbitrary coefficients |alpha_a|,|beta_n|<=1 supported on
1<=a<=M,1<=n<=N, and ANY integer c,
  |sum_(a,n)alpha_a beta_n K_q(c*a*n)|
    <<_epsilon q^epsilon*M*N
          *(q^-1/4+M^-1/2+q^(1/4)*N^-1/2).                (1)
There are no coprimality requirements on c,a,n. A harmless extra divisor
factor is absorbed in epsilon. This bounded-coefficient statement is
what the kernel proof needs; no arbitrary-coefficient L2 norm version
is asserted by (1).

Proof of (1):
1. First let c and the support a be q-units. For a prime p, Proposition3.1
   gives fixed C0,D0 and an exceptional set E_p of at most D0 pairs such
   that the correlation
     sum_(z modp)K_p(a*z)*conjugate(K_p(b*z))*e_p(h*z)
   is O(C0*sqrt(p)), unless (a/b,h/b) belongs to E_p. In all cases it
   is O(p). No assertion that E_p consists only of(1,0) is needed.
   Finitely many small primes can be included by enlarging C0,D0.

2. CRT gives EXACTLY, with Q_p=q/p,
     K_q(z)=product_(p|q)K_p(z*inverse(Q_p^3);p).
   The complete correlation modulo q consequently factors into prime
   correlations; their twists are h*inverse(Q_p), and the two K arguments
   are scaled by inverse(Q_p^3). Therefore its absolute value is at most
     C1^omega(q)*sqrt(q)*sum_(d|q)sqrt(d)*1_(E_d).          (2)
   Here E_d means that each prime dividing d is locally exceptional.
   For a fixed b, each choice of at most D0^omega(d) local pairs determines
   BOTH a and h modulo d by CRT. This remains true after the unit c twist.

3. Cauchy's inequality in n, followed by a smooth majorant and Poisson,
   bounds the square of the bilinear sum by
     (N^2/sqrt(q))*C1^omega(q)
       *sum_(d|q)sqrt(d)*D0^omega(d)*M*(M/d+1)*(1+Z/d),
   where Z=q/N. The last factor follows from the uniform Schwartz sum
   over h in ONE residue class modulo d; it is valid even when Z<1.
   The count for a is M/d+1, with at most M possible b. Summing divisors
   bounds this by
     q^epsilon*(N^2/sqrt(q))
          *(M^2+M*sqrt(q)+(q/N)*M^2+(q/N)*M).
   Taking square roots, the last term is absorbed since M>=1, and gives
   (1). Fixed constants to the power omega(q), and all divisor factors,
   are q^epsilon losses. No location of the exceptional pairs was assumed.

4. If c is not a unit, put d=gcd(c,q), q0=q/d. The explicit extension and
   CRT give
     K_q(c*z)=d^-1*K_q0(c*inverse(d^3)*z).                 (3)
   The new multiplier is a q0-unit. If q0=1 the left side is identically
   1/q. Otherwise (1) at q0, multiplied by1/d, is no larger than its
   q version: the respective additional factors are d^-3/4,d^-1,d^-5/4.

5. Finally remove the unit restriction on a by partitioning d=gcd(a,q)
   and writing a=d*a0. On each part a0 is a q0-unit, its length is M/d,
   and (3) gives multiplier c*inverse(d^2), which need not be a unit.
   Relative to the full M*N bound, the three factors now gain respectively
   d^-7/4,d^-3/2,d^-9/4. Empty parts have d>M; q0=1 is bounded directly.
   Summing at most tau(q) parts proves (1) for all coefficients as stated.

II. Exact nonunit modes of the original completed transform.
Let F_q(h,l;t)=sum_(u,v units modq)e_q(t/(u*v)+h*u+l*v).
For p prime, I_h=1_(p|h), I_l=1_(p|l), I_t=1_(p|t), EXACTLY
  F_p(h,l;t)=p*K_p(t*h*l)
    -p*(I_h*I_l+I_h*I_t+I_l*I_t)+(p^2+p)*I_h*I_l*I_t.   (4)
If at most one parameter is0, this is p*K_p(t*h*l). If exactly two are0,
it is1-p, and if all three are0 it is(p-1)^2. Thus (4) includes modes
which cannot be replaced by a Kl3 value without a correction.

For squarefree q, expand (4) prime by prime using CRT. A term is indexed
by four pairwise coprime squarefree products d_hl,d_ht,d_lt,a=d_all. Put
  D=d_hl*d_ht*d_lt*a,
  Hdiv=d_hl*d_ht*a, Ldiv=d_hl*d_lt*a, Tdiv=d_ht*d_lt*a.
It has factor q*K_(q/D)(unit*t*h*l), coefficient with absolute value
prod_(p|a)(p+1), and constraints Hdiv|h,Ldiv|l,Tdiv|t.
The unit multiplier in the remaining K is inverse(D^3) modulo q/D.
For t=m*k, put g=gcd(Tdiv,m), Kdiv=Tdiv/g. Then k is a multiple of Kdiv,
and
  Hdiv*Ldiv*Kdiv=D^2*a/g.                                 (5)
After rescaling all three variables, the normalized mass of the term is
g/D^2, apart from prod_(p|a)(1+1/p), a divisor-size loss.

Consequently, for arbitrary separated bounded weights alpha_h,beta_l,nu_k
on positive ranges h<=U,l<=V,k<=K, and ANY integer m,
  |sum_(h,l,k)alpha_h beta_l nu_k F_q(h,l;m*k)/q|
    <<_epsilon (q*U*V*K)^epsilon*U*V*K
          *(q^-1/4+V^-1/2+q^(1/4)*(U*K)^-1/2).           (6)
To see this, use (1) on each term of (4), keeping l' separate and grouping
w=h'*k'. Its coefficient is divisor-bounded. Nonempty rescaled supports
have lengths at least1. The factors in the three estimates relative to
the unpartitioned version of (6) are
  (g/D^2)*D^(1/4),
  (g/D^2)*Ldiv^(1/2),
  (g/D^2)*(Hdiv*Kdiv)^(1/2)*D^(-1/4).
Each is<=1: g<=D, Ldiv<=D, and Hdiv*Kdiv<=D^2/g. There are at most
5^omega(q) terms, including the main choice at each prime. All those
costs and grouped divisor coefficients fit the epsilon in (6). Signs of
h,l are handled by separate sign choices and changing the integer m.

III. The critical balanced squarefree kernel (unconditional MODEL).
Let B=A=Y^(1/3), C=Y^(1/2), K=Y^(1/6), m an integer in[Y,2Y], and
1<=J0,H<=Y^(1/4096). For every SQUAREFREE integer q in[C,2C], choose a
unit r_q modulo q, a period J_q<=J0, and arbitrary complex omega_(q,k)
periodic jointly in M,a modulo J_q, with absolute value<=1. Define E_q
as in composite_linear_kernel.py, with k<=H*K and fixed smooth W1,W2.
Then
  sum_q |E_q| <<Y^(23/24+epsilon)*H*J0^8+Y^epsilon*H*J0*B*A
              <<Y^(11803/12288+epsilon).                 (7)
The general linear estimate gave Y^(13/12+epsilon) at this SAME box.
Estimate (7) covers squarefree moduli with small factors and balanced
semiprime cores; it is not restricted to primes or to rough moduli.

Proof, with the period and axes paid for:
Let J=J_q, s=gcd(q,rad(J)), Q=q/s, T=s*J. Then s<=J and gcd(Q,T)=1.
The earlier exact CRT at period L=qJ=Q*T gives a Q-transform times a
small transform G_T, |G_T|<=T^2. Split the two residue classes h,l modT;
within each, G_T/T^2 is just an arbitrary bounded coefficient of k.
This costs at most T^4. No k residue split is needed.

Truncate the nonzero h,l frequencies at U=(qJ/B)*Y^rho, V=(qJ/A)*Y^rho
for arbitrarily small rho>0. Schwartz tails are negligible. Apply (6)
to the Q-transform in each residue pair; its multiplier includes r_q and
the CRT unit inverses. The divisor partitions in (4) divide Q, hence
are coprime to T; their substitutions merely change the fixed residue
classes, without any extra splits. All k dependence stays in nu_k.

Before the saving, the prefactor and volume per q are
  Y/(q^3*J^2)*Q*T^4*(U*V*H*K)
     <<Y^epsilon*H*s^3*J^4*C.
The three factors from (6), before tiny truncation losses, are
  Q^-1/4 <<s^(1/4)*Y^-1/8,
  V^-1/2 <<Y^-1/12,
  Q^(1/4)*(U*H*K)^-1/2 <<Y^-1/24.
Thus their sum is O(s^(1/4)*Y^-1/24). Sum O(C) moduli and use
s^(13/4)*J^4<=J0^(29/4)<=J0^8. This proves the first term of (7).

For the integer axes, use the proved one-variable Poisson/Ramanujan
argument in composite_linear_kernel.py: h=0 and, symmetrically, l=0
each cost O(Y^epsilon*H*J0*B*A) after modulus averaging. Their overlap
must ALSO be bounded, since these two axis sums can cancel internally.
The same restricted Ramanujan bound gives
  |F_L(0,0;r_q*m*k)|<=q*J^2*gcd(q,J)*tau(q)*gcd(q,m*k).
Its prefactor and the checked gcd average give the same bound. Thus the
union of the axes costs at most three such bounds. No nonunit mode or
zero-parameter exception is omitted. The uniform smooth coupled-weight
corollary remains subject to all spatial derivative bounds as before.

Reassessment:
This is a successful extra cancellation mechanism for the smooth balanced
SQUAREFREE model, independent of whether q has a large prime factor.
Prime powers require a separate correlation theorem or a costed removal;
CRT over distinct primes does not prove one. Further divisor boxes, all
original sieve/weight costs and the signed prime-correlation estimate
remain OPEN. The latest original-affine bound is still2b8cf98. No actual
exceptional zero, effective onset, new prime coverage or originality is
claimed. The preceding general-modulus linear estimate remains valid.

The finite verifiers below check new exact CRT/degeneracy identities and
partition costs. They do not prove the prime source's infinite estimate.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from math import gcd

from composite_linear_kernel import _reduce
from major_arc_kernel import _factorization


def _squarefree(q):
    factors = _factorization(q)
    if any(exponent != 1 for _, exponent in factors):
        raise ValueError("this result requires a squarefree modulus")
    return tuple(p for p, _ in factors)


def _integers(*values):
    if any(type(value) is not int for value in values):
        raise ValueError("parameters must be integers")


@lru_cache(maxsize=None)
def _raw_kl3(q, parameter):
    if q == 1:
        return (F(1),)
    counts = [F(0)]*q
    units = [v for v in range(1, q) if gcd(v, q) == 1]
    for u in units:
        for v in units:
            counts[(u+v+parameter*pow(u*v, -1, q)) % q] += F(1, q)
    return tuple(counts)


def kl3_exact(q, parameter):
    _squarefree(q)
    _integers(parameter)
    return _reduce(_raw_kl3(q, parameter % q), q)


def _multiply_embedded(current, factor, factor_modulus, q):
    result = [F(0)]*q
    scale = q//factor_modulus
    for i, left in enumerate(current):
        if left:
            for j, right in enumerate(factor):
                if right:
                    result[(i+scale*j) % q] += left*right
    return result


def kl3_crt_prediction(q, parameter):
    factors = _squarefree(q)
    _integers(parameter)
    result = [F(1)]+[F(0)]*(q-1)
    for p in factors:
        local = parameter*pow((q//p)**3, -1, p) % p
        result = _multiply_embedded(result, _raw_kl3(p, local), p, q)
    return _reduce(result, q)


def nonunit_multiplier_prediction(q, multiplier, argument):
    _squarefree(q)
    _integers(multiplier, argument)
    d = gcd(multiplier, q)
    reduced = q//d
    result = [F(0)]*q
    if reduced == 1:
        result[0] = F(1, q)
    else:
        parameter = multiplier*pow(d**3, -1, reduced)*argument % reduced
        for i, value in enumerate(_raw_kl3(reduced, parameter)):
            result[d*i] += value/d
    return _reduce(result, q)


@lru_cache(maxsize=None)
def _raw_correlation(q, first, second, twist):
    counts = [F(0)]*q
    for x in range(q):
        left = _raw_kl3(q, first*x % q)
        right = _raw_kl3(q, second*x % q)
        for i, a in enumerate(left):
            if a:
                for j, b in enumerate(right):
                    if b:
                        counts[(i-j+twist*x) % q] += a*b
    return tuple(counts)


def correlation_exact(q, first, second, twist):
    _squarefree(q)
    _integers(first, second, twist)
    if gcd(first*second, q) != 1:
        raise ValueError("the correlation inputs must be modulus units")
    return _reduce(_raw_correlation(q, first % q, second % q, twist % q), q)


def correlation_crt_prediction(q, first, second, twist):
    factors = _squarefree(q)
    _integers(first, second, twist)
    if gcd(first*second, q) != 1:
        raise ValueError("the correlation inputs must be modulus units")
    result = [F(1)]+[F(0)]*(q-1)
    for p in factors:
        scale = q//p
        inverse_cube = pow(scale**3, -1, p)
        local = _raw_correlation(p, first*inverse_cube % p, second*inverse_cube % p,
                                 twist*pow(scale, -1, p) % p)
        result = _multiply_embedded(result, local, p, q)
    return _reduce(result, q)


@dataclass(frozen=True)
class PartitionBudget:
    removed: int
    h_divisor: int
    l_divisor: int
    k_divisor: int
    target_gcd: int
    normalized_mass: F
    first_fourth_power: F
    short_square: F
    long_fourth_power: F


def partition_budget(hl, ht, lt, triple, target):
    _integers(target)
    parts = (hl, ht, lt, triple)
    for part in parts:
        _squarefree(part)
    for i, part in enumerate(parts):
        if any(gcd(part, other) != 1 for other in parts[i+1:]):
            raise ValueError("partition factors must be pairwise coprime")
    removed = hl*ht*lt*triple
    h_div, l_div, t_div = hl*ht*triple, hl*lt*triple, ht*lt*triple
    common = gcd(t_div, target)
    k_div = t_div//common
    mass = F(common, removed**2)
    return PartitionBudget(removed, h_div, l_div, k_div, common, mass,
                           mass**4*removed, mass**2*l_div,
                           mass**4*(h_div*k_div)**2/removed)


def balanced_kernel_budget(period_exponent=0, frequency_exponent=0):
    if any(type(v) not in (int, F) for v in (period_exponent, frequency_exponent)):
        raise ValueError("exponents must be exact rationals")
    j, h = F(period_exponent), F(frequency_exponent)
    if any(not 0 <= v <= F(1, 4096) for v in (j, h)):
        raise ValueError("decoration exponents must lie in[0,1/4096]")
    return max(F(23, 24)+8*j+h, F(2, 3)+j+h)
