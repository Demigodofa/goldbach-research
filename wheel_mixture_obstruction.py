"""Small-wheel mixtures retain a Type I defect, even with a huge joint period.

Owner: Kevin's research. Purpose: test whether pooling the positive periodic
comparisons repairs the incompatibility in periodic_character_comparison.py.
Sol checked the deduction and actual verifier. Four focused tests passed
normally and with Python -O; they do not establish analytic estimates.
No Goldbach counterexample, actual zero, or historical novelty is claimed.

Mixture theorem:
Let N be large and even, I=(N/4,N/2], and fix0<sigma<1, B>=0, C0>=1.
Take ANY finite number of even moduli2<=Q_i<=N**sigma and real weights
  sum_i w_i=1, V=sum_i |w_i|<=C0*(log N)**B.
Set f_i(t)=(Q_i/phi(Q_i))*1_{(t,Q_i)=1}. Either put b_i=f_i, or use
  b_i(t)=f_i(t)*(1-chi(t)*t**(beta-1))
with one SHARED primitive quadratic character of conductor D>24 dividing
every Q_i, and one shared beta in[1/2,1]. For this obstruction, beta need
not be a zero. Put b=sum_i w_i*b_i. Then for any fixed gamma>0,
  sum_{d<=N**gamma} max_J |sum_{k in J, dk in I}
      (Lambda(N-dk)-b(N-dk))|
       >>_{sigma,B,C0} N/((log N)**(B+1)*loglog N).        (1)
No bound on the number of components or their least common multiple is
used. In particular, convex mixtures and bounded-total-variation signed
mixtures fail the earlier Type I premise already at A=2. For general B,
(1) contradicts every-logarithmic-saving claims by taking A>B+1.

Exact local mechanism:
Take an odd prime ell not dividing N. In the character case exclude ell=D
if D itself is prime; this removes at most one prime. On the progression
t=N-ell*k, the complete-period mean of f_i is
  1+1_{ell|Q_i}/(ell-1).
The mean of f_i*chi is0. If ell does not divide Q_i, all units are sampled.
If ell divides Q_i, fixing the nonzero ell-residue leaves a nonprincipal
character component at another factor of D unless D=ell. Extra prime powers
in Q_i do not change this argument. Complete periods, followed by Abel
summation for t**(beta-1), whose supremum and variation are bounded, give
  sum_{ell*k in I} b(N-ell*k)
    =N/(4*ell)+N*c_ell/(4*ell*(ell-1))+O(E),
where c_ell=sum_{i:ell|Q_i}w_i and
E=sum_i |w_i|*(Q_i/phi(Q_i))*Q_i=N**(sigma+o(1)).
Thus the difference from the prime progression main term N/(4*(ell-1))
is N*delta_ell/(4*ell*(ell-1)), delta_ell=1-c_ell.
Signed mixtures may have NEGATIVE delta_ell. An unweighted sum cannot
silently treat all these defects as positive.

Weighted arithmetic test:
Write L=logN and Y=4*(1+C0)*L**(B+1). Let Eset contain the primes
Y<ell<=2Y with ell not dividing N and ell!=D in the possible prime-D case.
The prime number theorem and log(rad N)<=L give
  sum_{ell in Eset}log(ell)>=(1-o(1))*Y-L-O(logY).
On the other hand,
  sum_{ell in Eset}c_ell*log(ell)
     <=sum_i |w_i|*log(Q_i)<=sigma*C0*L**(B+1).
Consequently sum_Eset delta_ell*log(ell)>=Y/2 for sufficiently large N.
Use the NONNEGATIVE test coefficients
  h_ell=ell*(ell-1)*log(ell)/(4*Y**2*log(2Y)), 0<=h_ell<=1.
The signed weighted main discrepancy is at least N/(32*Y*log(2Y)).
The weighted BV error is bounded by the absolute summed BV error, using
any fixed saving A>B+3. The total period error is at most #Eset*O(E),
a power of N smaller than this main term. Proper prime powers contribute
only sqrt(N) times a fixed logarithmic power across the selected moduli.
Finally sum of absolute discrepancies dominates this weighted signed sum,
and every ell here is below N**gamma eventually. This proves(1).

Primary inputs, already checked for the single-period argument:
PNT and Ford's Sieve Methods Lecture Notes2023, Theorem3.4 (BV, printedp35),
including its reduced-residue and endpoint maxima and Abel log weighting:
https://ford126.web.illinois.edu/sieve2023.pdf
The dependence on the number of models disappears because the coefficients
are charged by total variation, rather than counting each model as weight1.

The positive comparison margin from periodic_character_comparison.py is
preserved under NONNEGATIVE mixtures when every component satisfies that
theorem's common actual-character/zero premises and uniform scale bounds.
Then the weighted prime-versus-model mass is >>N*mu*sum_i w_i*K_i, mu
=min(1,(1-beta)logN). No analogous positivity is claimed for signed weights.
This is still a comparison containing composites, not actual prime pairs.

Scope: this rules out repairing the old absolute Type I premise by these
polylogarithmically bounded mixtures of small normalized unit wheels. It
does not rule out specific signed Vaughan cancellation, different residue
weights, larger individual moduli, or a different decomposition. It does
not affect the earlier exact parity bootstrap or the much larger primorial
comparison. The finite helpers validate residue arithmetic only, not PNT,
BV, a zero premise, an analytic threshold, or Goldbach.
"""
from fractions import Fraction
from math import gcd

from exceptional_character_model import character_values
from redistribution import trial_prime


def mixture_prime_defect(moduli: list[int], weights: list[int | Fraction],
                         target: int, prime: int) -> tuple[Fraction, Fraction]:
    """Return(weighted coverage, ideal-minus-model LOCAL residue density).

    The even target must be coprime to the prime. Normalized unit wheels
    are assumed; signed exact weights with sum1 are allowed. The returned
    density difference is not an actual prime count or analytic error.
    """
    if (type(moduli) is not list or not moduli
            or any(type(q) is not int or q < 2 or q % 2 for q in moduli)):
        raise ValueError("require a nonempty list of exact even moduli")
    if (type(weights) is not list or len(weights) != len(moduli)
            or any(type(w) not in (int, Fraction) for w in weights)
            or sum(weights) != 1):
        raise ValueError("require matching exact rational weights summing to1")
    if (type(target) is not int or target < 6 or target % 2
            or type(prime) is not int or not trial_prime(prime)
            or target % prime == 0):
        raise ValueError("require an even target at least6 and a coprime prime")
    coverage = sum((Fraction(w) for q, w in zip(moduli, weights) if q % prime == 0),
                   Fraction(0))
    return coverage, (1-coverage)/ (prime*(prime-1))


def wheel_progression_means(modulus: int, target: int, prime: int, *,
                             conductor: int | None = None, two_sign: int = 1
                             ) -> tuple[Fraction, Fraction]:
    """Return exact means of f_Q and f_Q*chi on the prime-step progression.

    With no conductor the second mean is0. With primitive D>24 dividing Q,
    this RETAINS the exceptional D=prime case so its nonzero mean is visible.
    Enumeration is intended for small finite verification, not zero detection.
    """
    mixture_prime_defect([modulus], [1], target, prime)
    if conductor is None:
        if type(two_sign) is not int or two_sign != 1:
            raise ValueError("no character sign is used without a conductor")
        chi = None
    else:
        if (type(conductor) is not int or conductor <= 24
                or modulus % conductor):
            raise ValueError("require an exact primitive D>24 dividing Q")
        chi = character_values(conductor, two_sign=two_sign)
    phi_q = sum(gcd(a, modulus) == 1 for a in range(modulus))
    c_q = Fraction(modulus, phi_q)
    period = modulus//gcd(prime, modulus)
    total = twisted = Fraction(0)
    for k in range(period):
        residue = (target-prime*k) % modulus
        if gcd(residue, modulus) == 1:
            total += c_q
            if chi is not None:
                twisted += c_q*chi[residue % conductor]
    return total/period, twisted/period
