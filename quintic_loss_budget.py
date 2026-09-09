"""Control all positive quintic composite losses on the main scale.

Owner: Kevin's research. Purpose: close the remaining absolute-constant
error-control gaps in quintic_partner_weight.py. The required SMALL loss
and positive lower bound for the full signed total remain unproved.
The helpers verify exact ranges, residue switching and formal integrals;
finite tests cannot establish the analytic prime estimates used below.
Sol checked the theory and actual files. Five focused exact tests passed
normally and with Python -O.

Deduction (theory independently checked by Sol):
Keep the actual-zero hypotheses and notation of quintic_partner_weight.py.
In particular D>24 is an actual primitive quadratic exceptional conductor,
D<=Y^(delta/4), t=(1-beta)*log(Y) is in (0,1/log(Y)], epsilon<=1/100,
delta<=epsilon/3 is sufficiently small, u is fixed and sufficiently large,
theta=delta/u, and kappa>0 is FIXED. Write L=log(Y), L_n=log(n),
R=floor(Y^a), a=1/2-2epsilon, E=floor(Y^(1/2-epsilon)/(3D^3)).
The pool B_good is unchanged. Let E_j denote the j-factor composite class
called S_j in that module, to distinguish it from the singular series S_2(m).
Then, for an ABSOLUTE constant C independent of theta,epsilon,kappa,
  sum_{j=2}^6 E_j^+ <= C*(1+kappa)*Y*S_2(m)*t + o(Y*t).       (1)
Here E_j^+ sums positive weights, rather than taking the positive part of
the class total. The little-o onset may depend on all the fixed parameters.
Equation(1) is not a small specified fraction of the prime-pair scale.

Pure five-factor partners: adapt the auxiliary cutoff.
1. Order their distinct negative-sign primes r1<...<r5. Their first two
give M=r1*r2<=n^(2/5)<=Y^(2/5). The level E/M has exponent at least
  1/2-epsilon-3delta/4-2/5 >= 7/80 > 2/25.
Choose an absolute eta0>0 sufficiently small. Sieve the remaining integer
n/M through Z_M=min(r2,Y^eta0), omitting primes of M. Its three actual
prime factors exceed r2, so this is an upper bound. Ford Theorem3.6(a,b)
(printed p38) gives a sufficiently large fixed sieve ratio, uniformly M:
https://ford126.web.illinois.edu/sieve2023.pdf
The fixed-M prime-log mass is at most
  C*X*S_2(m)/(phi(M)*min(log(r2),eta0*L)) + sum_e |r_(M*e)|, (2)
where X is the original rare first-prime mass, O(Y*t), and e is squarefree,
coprime to M, Z_M-smooth, M*e<=E. The local product follows by the same
Mertens calculation as the original sieve. Omitting two odd M primes
costs at most4 and the possible extra3 factor is bounded. For fixed theta,
Z_M exceeds a positive power of Y eventually; the singular-series tail
therefore vanishes. The upper-bound constant itself is absolute.
2. The exact weight and AM-GM on the last three logarithms give
  K=240*kappa*product(log(ri))/L_n^4
    <=(240/27)*kappa*log(r1)*log(r2)/L_n
    <=(480/27)*kappa*log(r1)*log(r2)/L.
For r2<=Y^eta0, log(r2) cancels the adaptive denominator in (2).
Using sum_{p<=x}log(p)/(p-1)<<log(2x), the nested sum is O(eta0*L);
the outer factor1/L makes it bounded. For r2>Y^eta0, use denominator
eta0*L and the double logarithmic reciprocal sum O(L^2). This gives an
absolute O(1/eta0) constant, with NO 1/theta retained. Hence
  E_5 <= C*kappa*Y*S_2(m)*t + o(Y*t).
Remainder indices are NOT injective: each squarefree index admits at most
binom(omega(index),2)=O(L^2) cofactors, even with this variable cutoff.
Since K=O(kappa*L), the relative remainder sum Y*t/L^6 already proved in
rare_twisted_bv.py costs O(kappa*Y*t/L^3)=o(Y*t).

Even classes: switch the actual prime variable to the large rare factor.
3. Such a partner has n=M*q, with exactly one positive-sign factor q>R.
M has k=1,3 or5 distinct negative-sign prime factors. Thus chi(M)=-1,
M<=Y^(1-a)<=Y^(13/25), and X_M=Y/M>=Y^(12/25). Actual terms have
gcd(M,Dm)=1: a factor of M dividing m would divide the much larger prime p.
Use q in J/M subset [X_M/2,X_M] as the ACTUAL prime variable, and sieve
p=m-M*q. No distribution at modulus M is requested. The allowed positive
q residues modulo D are exactly M^{-1} times the allowed negative partner
residues. Their number is A/2, with A/phi(D) either1 or1/2 as before.
For squarefree e coprime to DmM, the condition e|p is the reduced class
q=m*M^{-1} mod e; CRT gives A/2 positive-sign classes modulo D*e.
For primes dividing DmM the sieve density is0. Consequently the local
density is the original one, except that primes of M are omitted.
4. Choose fixed ABSOLUTE eta1>eta0>0, sufficiently small and with their
ratio sufficiently large for Ford's upper sieve. Shrink delta if needed
so X_M/2>=(D*e)^C and c*log(X_M)/log(D*e)>=28 for all e<=E0=Y^eta1.
The bulk Linnik deduction in relative_type_i.py, based on Thorner--Zaman
Theorem2.1 and equation(4.2), applies uniformly at scale X_M:
https://arxiv.org/html/2108.10878#S2
https://arxiv.org/html/2108.10878#S4
The local rarity (1-beta)*log(X_M) is between (12/25)*t and t. Summing
the normalized progression errors over squarefree e<=E0 gives
  O((Y/M)*(t^28*L+L^2/D) + sqrt(Y/M)*Y^o(1)).           (3)
Indeed sum 1/phi(e)=O(L), whereas sum 1/(e*phi(e))=O(1).
Proper powers of q can instead be removed by counting divisors of the
nonzero m-M*v^j=O(Y); their total is the last term in (3). This also
covers nonreduced residue exceptions. The progression modulus is D*e,
NEVER D*M*e. The repaired source proof is essential here.
5. Sieve p through Y^eta0 at level E0, omitting M primes. At most five
odd omitted primes cost at most2^5. The product is at most C*S_2(m)/L
with absolute C. Thus both-prime q-log mass is at most
  C*(Y/M)*t*S_2(m)/L + the remainder (3).              (4)
We assert only ONE rarity factor t, not t^2. Also log(p)/log(q)<=3
eventually. The exact quintic formulas imply, for k=1,3,5 respectively,
  |K_f(n)| <= C*(1+kappa)*product_{r|M}log(r)/L^(k-1). (5)
For k=1 use the semiprime divided difference and ||f'||<=1+44*kappa;
for k=3 use the bounded square-share bracket; k=5 is the exact formula.
The elementary prime reciprocal logarithmic sum gives
  sum_M product_{r|M}log(r)/M = O(L^k),
even after dropping all character and original-cutoff restrictions.
Equations(4)-(5) therefore bound E_2^++E_4^++E_6 by the right side of(1).
The summed errors are
  O_kappa(Y*(t^28*L^2+L^3/D) + Y^(19/25+o(1))).       (6)
For the power term use |K|=O_kappa(L) and sum_{M<=Y^(13/25)}sqrt(Y/M).
All terms in(6) are o(Y*t): t<=1/L, Siegel gives t>=Y^-h eventually
for every fixed h>0, and t>>_b D^-b with D exceeding every fixed power
of L. All onsets remain ineffective. The previous absolute bound for
E_3^+ and previous negligible classes complete(1).

A FORMAL cancellation, not a density theorem:
On the open logarithmic-share simplex define
  dnu_k=(1/k!)*dx1...dx_(k-1)/(x1*...*xk), sum xi=1.
The pure triple weight is J3=4*kappa*x*y*z*(1-5*(xy+xz+yz));
the pure five weight is J5=240*kappa*product xi. Cancelling the products
makes both integrals finite. The beta-simplex monomial formula gives
  integral J3 dnu3 = -kappa/12,
  integral J5 dnu5 = +kappa/12.                        (7)
Taking positive parts loses this formal cancellation. The measure is
explicitly DEFINED here; it is not asserted to describe actual prime
factor proportions or their correlation with m-n prime. Thus(7) cannot
be substituted for an actual signed estimate. The small signed loss and
the full-total positivity gap both remain open. No new Goldbach coverage.
The general identity in formal_weight_conservation.py now explains(7):
the total formal odd-factor integral equals the Dickman polynomial already
present in the Type-I main, also at a nonzero cutoff. This does not turn
the formal cancellation into an independent arithmetic estimate.
"""
from fractions import Fraction as F
from math import factorial, gcd

from major_arc_kernel import _factorization, _mobius_phi
from rare_prime_sieve import suppressed_residue_split


def quintic_range_exponents(epsilon: F, delta: F) -> tuple[F, F, F]:
    """Return lower level/M, lower switched scale, and upper power-error exponents.

    Exponents omit floor constants; strict exponent slack is required before
    using them as eventual integer range assertions. They do not certify
    the unknown absolute constants in bulk Linnik or a numerical onset.
    """
    if (type(epsilon) is not F or type(delta) is not F
            or not 0 < epsilon <= F(1, 100) or not 0 < delta <= epsilon/3):
        raise ValueError("require exact 0<epsilon<=1/100 and 0<delta<=epsilon/3")
    a = F(1, 2)-2*epsilon
    return F(1, 10)-epsilon-3*delta/4, a, 1-a/2


def adaptive_semiprime_indices(index: int, level: int, cofactor_limit: int,
                              absolute_cutoff: int) -> tuple[tuple[int, int], ...]:
    """Support (M,e) with M=r1*r2 and e smooth through min(r2,cutoff).

    This checks the upper-support multiplicity, not actual partner factors,
    character conditions or numerical remainder estimates.
    """
    if any(type(v) is not int for v in (index, level, cofactor_limit, absolute_cutoff)):
        raise ValueError("require exact integers")
    if index < 1 or not 2 <= absolute_cutoff <= level or not 1 <= cofactor_limit <= level:
        raise ValueError("require index>=1, 2<=cutoff<=level, 1<=cofactor_limit<=level")
    if index > level:
        return ()
    factors = _factorization(index)
    if any(a != 1 for _, a in factors):
        return ()
    primes = tuple(p for p, _ in factors)
    result = []
    for j, r2 in enumerate(primes):
        for r1 in primes[:j]:
            m = r1*r2
            if m <= cofactor_limit and all(p <= min(r2, absolute_cutoff)
                                          for p in primes if p not in (r1, r2)):
                result.append((m, index//m))
    return tuple(sorted(result))


def switched_residue_density(conductor: int, target: int, cofactor: int,
                             divisor: int, *, two_sign: int = 1
                             ) -> tuple[tuple[int, ...], F]:
    """Allowed q classes and relative e-divisibility density for m-M*q.

    M is any negative-character unit coprime to m. This is finite residue
    algebra, not an actual prime count or an exceptional-zero claim.
    """
    _, _, negative = suppressed_residue_split(conductor, target, two_sign=two_sign)
    if type(cofactor) is not int or cofactor < 1 or gcd(cofactor, conductor*target) != 1:
        raise ValueError("require positive integer M coprime to D*m")
    from exceptional_character_model import character_values
    chi = character_values(conductor, two_sign=two_sign)
    if chi[cofactor % conductor] != -1:
        raise ValueError("require chi(M)=-1")
    if type(divisor) is not int or divisor < 1 or _mobius_phi(divisor)[0] == 0:
        raise ValueError("require positive squarefree integer divisor")
    inverse = pow(cofactor, -1, conductor)
    classes = tuple(sorted(inverse*r % conductor for r in negative))
    density = (F(0) if gcd(divisor, conductor*target*cofactor) > 1
               else F(1, _mobius_phi(divisor)[1]))
    return classes, density


def simplex_polynomial_integral(terms: dict[tuple[int, ...], F]) -> F:
    """Exact unweighted integral over sum(x_i)=1, x_i>=0, dimension k-1.

    Terms are barycentric exponent tuples of one common length2..8, with
    total degree<=64 and exact Fraction coefficients. This integrates a
    defined polynomial; it does not supply a prime-factor density measure.
    """
    if type(terms) is not dict or not terms:
        raise ValueError("require a nonempty polynomial dictionary")
    dimension = None
    result = F(0)
    for powers, coefficient in terms.items():
        if (type(powers) is not tuple or not 2 <= len(powers) <= 8
                or any(type(a) is not int or a < 0 for a in powers)
                or sum(powers) > 64 or type(coefficient) is not F):
            raise ValueError("require exact coefficients and nonnegative bounded exponent tuples")
        if dimension is None:
            dimension = len(powers)
        if len(powers) != dimension:
            raise ValueError("require one simplex dimension")
        numerator = 1
        for a in powers:
            numerator *= factorial(a)
        result += coefficient*F(numerator, factorial(sum(powers)+dimension-1))
    return result


def formal_quintic_cancellation(kappa: F) -> tuple[F, F]:
    """Return the two SIGNED integrals against the explicitly formal nu_k."""
    if type(kappa) is not F or kappa < 0:
        raise ValueError("require exact Fraction kappa>=0")
    triple = {(0, 0, 0): 4*kappa/F(factorial(3)),
              (1, 1, 0): -20*kappa/F(factorial(3)),
              (1, 0, 1): -20*kappa/F(factorial(3)),
              (0, 1, 1): -20*kappa/F(factorial(3))}
    five = {(0, 0, 0, 0, 0): 240*kappa/F(factorial(5))}
    return simplex_polynomial_integral(triple), simplex_polynomial_integral(five)
