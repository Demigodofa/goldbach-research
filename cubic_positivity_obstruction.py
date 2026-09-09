"""Test the cubic weight's positivity route through its accessible divisors.

Owner: Kevin's research. Purpose: determine the sign of the Type I portion
before asking an uncontrolled complementary sum to supply a positive bound.
The helpers certify exact algebra, sieve support and a Dickman tail bound.
They neither estimate a finite prime correlation nor detect an actual zero.

Sol checked the theory and actual files. Five focused exact tests passed
normally and with Python -O; these verify finite algebra and enclosures.

Deduction independently checked by Sol:
Keep the actual-zero regime of balanced_semiprime_budget.py. Fix
0<epsilon<=1/100, kappa=1/epsilon, and its sufficiently small delta.
Choose the fixed u sufficiently large DEPENDING on these parameters.
Put theta=delta/u, a=1/2-2epsilon, R=floor(Y^a), L=log(Y), and define
  h(x)=(1-2x)*(1+kappa*x*(1-x)).
On the SAME original B_good at these parameters let
  T_low=sum_p log(p) sum_{d|(m-p), d<=R} chi(d)*log(m-p)
                                      *h(log(d)/log(m-p)).
For sufficiently large Y, uniformly in the central suppressed targets,
  T_low <= -(kappa/32)*Y*S_2(m)*t.                    (1)
Onsets remain ineffective. This is NOT a negative bound for the full
T_kappa. Its EXACT remaining divisor sum T_boundary=T_kappa-T_low must
overcome (1) before the previously checked prime-pair lower bound is useful.
In particular a claim T_boundary=o(Y*S_2*t) would make this weight fail.

Exact hyperbola and reduction to a sieve main term:
1. Pair d with n/d in the defining convolutions. Since chi(n)=-1,
chi(n/d)=-chi(d), and n cannot be a square. This gives exactly
  K_kappa(n)=sum_{d|n,d<sqrt(n)}chi(d)*log(n)*h(log(d)/log(n)),
  h(x)=1+(kappa-2)*x-3*kappa*x^2+2*kappa*x^3.          (2)
Eventually R<sqrt(Y/2), so T_low is a genuine initial part of this sum.
Every z-rough n<=Y has Omega(n)<1/theta and tau(n)<=2^(1/theta).
Replacing log(n) by L in (2) costs O_(kappa,theta)(1) per candidate.
The upper sieve bounds their prime-log mass by O_(theta)(Y*t*S_2/L),
so this replacement is negligible. Squareful rough partners contribute
O_(kappa,theta)(Y^(1-theta)*L^2)=o(Y*t), as in the earlier proof.
The original B_bad deletion also costs o(Y*t): its reciprocal rarity is
O_(delta,u)(eta^(-2/u)+t+1/z), which remains o(1/loglog(Y)). Thus we may
evaluate on the original rough pool B, using squarefree rough divisors d.
2. Sieve the condition d|(m-p) through the original z, at level
floor(E_epsilon/d), where E_epsilon=floor(floor(Y^(.5-epsilon)/D^3)/3).
The minimum sieve ratio is at least (.75epsilon)/theta+o(1). Upper and
lower fundamental lemmas give the same main X*g(d)*V(z), with relative
error eta_s=exp(-s*log(s)+s*log_3(s)+O(s)). Constants are uniform in m.
The map (d,e)->d*e is INJECTIVE: d is squarefree with all factors>z;
e is squarefree with all factors<=z. This holds for composite d too.
Hence the existing all-squarefree remainder budget is charged once.
Multiplying by the bounded polynomial costs O_kappa(L), not a divisor
multiplicity. Choosing sieve bounds according to the sign of chi(d)
gives a two-sided estimate for the signed sum. Its main is
  L*X*V(z)*sum_{d<=R,squarefree,P^-(d)>z,(d,Dm)=1}
                         chi(d)*h(log(d)/L)/phi(d),   (3)
with sieve main error O_kappa(L*X*V(z)*eta_s/theta), since the absolute
rough reciprocal sum is O(1/theta). The remainder is o(Y*t).
Sources: the relative distribution proof in balanced_semiprime_budget.py;
Ford2023, Theorem3.6(a,b), printed p38:
https://ford126.web.illinois.edu/sieve2023.pdf

Evaluation of the ACTUAL character divisor main:
3. At fixed theta,a, the prime reciprocal rarity above z is o(1), by
Matomaki--Merikoski Lemma2.2, as used in rare_factor_pruning.py:
https://arxiv.org/html/2112.11412v2#S2
On squarefree rough d, chi(d)=mu(d) unless d has a positive-sign prime.
The sum of absolute discrepancies with weight1/d is at most the rare
reciprocal sum times2*product_{z<p<=Y^a}(1+1/p)=o_(theta)(1).
Replacing 1/phi(d) by1/d costs O_theta(1/z). Omitting primes>z dividing
Dm costs O_theta(log(Y)/(z*log(z)))=o(1), uniformly in m,D. These facts
justify replacing the actual signed divisor main by its Mobius version;
they do not replace the actual first primes in T_low by a model.
4. Expand that squarefree Mobius sum by its number of prime factors,
at most floor(a/theta). Mertens' prime reciprocal formula, with repeated
primes costing O_theta(1/z), gives the limiting cumulative function
  rho(v)=sum_{j>=0}(-1)^j/j! * integral_{t_i>=1,sum t_i<=v}prod dt_i/t_i.
Only finitely many j occur at each v. Multiplying the derivative of the
jth simplex integral by v gives the preceding integral at v-1. Thus
rho=1 on[0,1] and v*rho'(v)=-rho(v-1): this is the Dickman function.
Partial summation gives the limit of the sum in (3) as
  I=h(a)*rho(a/theta)-theta*integral_0^(a/theta)h'(theta*v)*rho(v)dv. (4)
The atom at d=1 is INCLUDED in this formula; no extra constant is added.
5. The standard Laplace transform gives moments
  integral rho=e^gamma, integral v*rho=e^gamma,
  integral v^2*rho=3*e^gamma/2.
See Gorodetsky, ViBrANT seminar notes, Section2, printed p2:
https://people.maths.ox.ac.uk/gorodetsky/vibrant.pdf
It also records v*rho(v)=integral_(v-1)^v rho, implying
0<rho(v)<=1/floor(v)!. Consequently, for fixed kappa,a as theta->0,
  I/(theta*e^gamma)=2-kappa+6*kappa*theta-9*kappa*theta^2+o(1). (5)
This is NEGATIVE for the present kappa>=100. The helper below encloses
the finite-cutoff value in (4) with exact rational bounds, without using
printed decimal values of rho or gamma.

Normalization and parameter order:
6. Let b=3 if3|D and3 does not divide m, otherwise b=1. The local product
and the original rare-prime mass satisfy, uniformly in suppressed m,
  V(z)=(1+o(1))*e^(-gamma)*phi(b)*S_2(m)/log(z),
  X=(1+o(1))*length(J_real)*t/(2*phi(b)).
Primes>z dividing m have a vanishing reciprocal sum, so the truncated
singular product has relative error o(1). Thus (3) divided by
length(J_real)*S_2(m)*t has limiting main I/(2*theta*e^gamma).
Its fixed sieve error is O_kappa(eta_s/theta^2). As u increases, theta
decreases and s grows at least proportionally to epsilon/theta, so this
error tends to0. First choose u sufficiently large; THEN let Y grow.
Equations (4)-(5) place T_low below -(kappa/4)*length(J_real)*S_2*t
eventually. Since length(J_real)>=Y/4, the weaker constant1/32 in (1)
has ample margin. No varying-u or uniform growing-kappa assertion is made.

This retires positivity from the accessible part of THIS cubic weight.
It does not refute its composite-error bound, all possible weights, or
Goldbach. No new actual coverage, zero, numerical onset or priority claim.
log_weight_barrier.py extends the endpoint-main calculation to any fixed
polynomial and proves the suppression/main-sign conflict for the entire
nonnegative logarithmic-subtraction family, with a separate formal triple
obstruction when leaving that family.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import factorial

from character_partner_weight import negative_hyperbola_terms
from cubic_character_minorant import _negative_input
from major_arc_kernel import _factorization


def paired_kernel_coefficients(kappa: F) -> tuple[F, F, F, F]:
    """Exact coefficients of h, requiring a fixed nonnegative rational kappa."""
    if type(kappa) is not F or kappa < 0:
        raise ValueError("require exact Fraction kappa>=0")
    return F(1), kappa-2, -3*kappa, 2*kappa


def paired_hyperbola_split(n: int, conductor: int, kappa: F, cutoff: int,
                          *, two_sign: int = 1) -> tuple[tuple, tuple]:
    """Exact (low, boundary) polynomials for log(n)^2*K, with d<=cutoff low.

    Monomials are sorted triples of prime logarithms, as in the earlier
    cubic verifier. This finite helper retains the existing n<=20000 cap.
    Neither returned polynomial is claimed to be a pointwise lower bound.
    """
    coefficients = paired_kernel_coefficients(kappa)
    _, n_factors = _negative_input(n, conductor, two_sign)
    if type(cutoff) is not int or not 0 <= cutoff <= 20000:
        raise ValueError("require integer cutoff in[0,20000]")
    low, boundary = defaultdict(F), defaultdict(F)
    for d, sign in negative_hyperbola_terms(n, conductor, two_sign=two_sign):
        out = low if d <= cutoff else boundary
        d_factors = tuple(_factorization(d))
        for j, coefficient in enumerate(coefficients):
            for selected in product(*([n_factors]*(3-j)+[d_factors]*j)):
                value = sign*coefficient
                for _, exponent in selected:
                    value *= exponent
                out[tuple(sorted(prime for prime, _ in selected))] += value
    return tuple(tuple(sorted((key, value) for key, value in out.items() if value))
                 for out in (low, boundary))


def rough_smooth_index_split(index: int, cutoff: int, level: int,
                            rough_limit: int) -> tuple[int, int] | None:
    """Recover unique (rough d,smooth e) for a squarefree sieve index d*e.

    Allows any number of prime factors in d, including zero; checks only
    finite support, not the relative distribution or minimum sieve ratio.
    """
    if any(type(v) is not int for v in (index, cutoff, level, rough_limit)):
        raise ValueError("require exact integer parameters")
    if index < 1 or not 2 <= cutoff < rough_limit <= level:
        raise ValueError("require index>=1 and 2<=cutoff<rough_limit<=level")
    if index > level:
        return None
    rough = 1
    for prime, exponent in _factorization(index):
        if exponent != 1:
            return None
        if prime > cutoff:
            rough *= prime
    return (rough, index//rough) if rough <= rough_limit else None


def dickman_main_enclosure(kappa: F, theta: F, endpoint: F) -> tuple[F, F]:
    """Enclose I/(theta*exp(gamma)) in (4), not the actual prime sum.

    All inputs are exact Fractions. The cap floor(endpoint/theta)<=10000
    bounds this finite verifier's factorial size, not the analytic theorem.
    rho(v)<=1/floor(v)! gives, for m>=2 and j=0,1,2,
      integral_(endpoint/theta)^infinity v^j rho(v)dv <=3*(m+1)^j/m!.
    The factorial series has successive ratio at most16/27<2/3.
    Using exp(-gamma)<1 also bounds the endpoint term without decimals.
    """
    paired_kernel_coefficients(kappa)
    if any(type(v) is not F for v in (theta, endpoint)):
        raise ValueError("require exact Fraction theta and endpoint")
    if not 0 < theta <= endpoint/2 or not endpoint <= F(1, 2):
        raise ValueError("require 0<theta<=endpoint/2 and endpoint<=1/2")
    m = endpoint//theta
    if m > 10000:
        raise ValueError("finite factorial verifier requires endpoint/theta<10001")
    center = 2-kappa+6*kappa*theta-9*kappa*theta*theta
    radius = ((1+kappa/4)/theta
              +3*(abs(kappa-2)+6*kappa*theta*(m+1)
                   +6*kappa*theta*theta*(m+1)**2))/factorial(m)
    return center-radius, center+radius
