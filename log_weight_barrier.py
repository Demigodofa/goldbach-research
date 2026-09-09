"""Exact obstruction to removing balanced semiprimes with higher log weights.

Owner: Kevin's research. Purpose: decide whether raising the degree of the
cubic character weight can finish its missing pointwise composite control.
This is a limitation of a specified kernel family, not of Goldbach proofs.
The rational helpers verify polynomial identities and coefficient costs.

Sol checked the theory and actual files. Nine focused exact tests passed
normally and with Python -O; these tests verify finite algebra only.

Deduction independently checked by Sol:
For f:[0,1]->R with f(0)=0 and f(1)=1, define, for n>1,
  K_f(n)=log(n)*sum_{d|n}chi(d)*f(log(n/d)/log(n)).
On a negative-sign prime this is log(n). If n=rq is squarefree, with
chi(r)=-1, chi(q)=+1, and a=log(q)/log(n), direct expansion gives
  K_f(n)/log(n)=H_f(a):=1+f(1-a)-f(a).                  (1)
Consequently H_f(a)+H_f(1-a)=2 and H_f(1/2)=1. No single such kernel is
nonpositive on a set containing both a and 1-a. These are identities in
factor proportions, not a claim that swapping signs preserves a particular
character, zero hypothesis or prime-first target. The formal midpoint does
not itself describe two distinct actual primes.

Integrating the reflection identity gives, for 0<=b<=1/2,
  integral_b^(1-b) H_f(a) da=1-2*b,
  integral_b^(1-b) max(H_f(a),0) da>=1-2*b.            (1a)
This bound does not depend on degree or coefficient size. For the cubic
f(s)=10s-9s^3, H=2+7a-27a^2+18a^3 is positive on[0,2/3) and negative
on(2/3,1). Its positive-part integral is10/9, versus1 for the original W;
the negative-part integral is-1/9. Thus tail deletion alone does not even
reduce this uniform-share positive-part budget. This measure is FORMAL,
not a proved distribution law or lower bound for actual semiprime errors.

For a polynomial f(s)=sum_{j>=1}c_j*s^j with sum c_j=1, set
  M=sum_{j>=1}j*abs(c_j).
Then |f'|<=M on[0,1], so
  |H_f(a)-1|<=M*|1-2a|.                                (2)
For actual comparable factors q/r in[1/2,2], (2) implies K_f(n)>=log(n)/2
if log(n)>=2*M*log(2). Thus a FIXED polynomial cannot make such semiprimes
nonpositive at arbitrarily large sizes. This is a conditional statement
about any factors meeting the stated size/sign conditions, not an assertion
of their density inside the remaining prime-first correlation. If H_f(a)<=0,
then necessarily M>=1/abs(1-2a). Coefficients depending on n or the character
still satisfy these pointwise identities; no uniform fixed-M conclusion is
claimed for a growing or adaptive coefficient family.

The stronger obstruction for the safe subtraction family:
For finitely many c_j>=0, j>=2, consider
  K=(1+sum c_j)*W-sum c_j*(chi*log^j)/log(n)^(j-1).
Each chi*log^j=(1*chi)*(mu*log^j)>=0: the mixed finite-difference argument
in cubic_character_minorant.py works for every positive integer j. Hence
K<=(1+sum c_j)*W, which is why this family safely transfers old upper bounds.
However, on EVERY mixed-sign semiprime with q<=r, put
x=log(r)/log(n), y=log(q)/log(n). Then x>=y and x+y=1. For j>=2,
  x^j-y^j=(x-y)*sum_{i=0}^{j-1}x^(j-1-i)*y^i<=x-y,
because that sum is at most (x+y)^(j-1)=1. Therefore
  (chi*log^j)/log(n)^(j-1)<=W(n), and K(n)>=W(n)>0.     (3)
Increasing any of the nonnegative penalties cannot reduce these partners
at all. Degree2 gives equality; for j>=3 and 0<y<x it is strict if that
penalty is positive. For example r=43,q=5 under the character modulo31
is an actual finite mixed-sign semiprime to which (3) applies. It is an
algebra guard, not a new exceptional-zero or candidate-pool assertion.

Outcome: the proposed route of removing the entire balanced range merely by
adding higher logarithmic subtractions fails. The earlier cubic reduction
remains correct. A bound for the signed total versus the remaining composite
correlation, or a materially different arithmetic ingredient, is still needed.
No aggregate lower bound for the composite error, zero existence, numerical
onset or new prime-pair coverage follows from this obstruction.

Endpoint-main versus composite suppression, independently checked by Sol:
For any FIXED polynomial f as above, put h(x)=f(1-x)-f(x). The exact
smaller-divisor kernel is log(n)*h(log(d)/log(n)). The signed-sieve proof
of cubic_positivity_obstruction.py applies to this fixed polynomial with
the same actual-zero assumptions, fixed epsilon,delta and original pool.
Write T_low,f for its divisors d<=Y^(1/2-2epsilon). For every tolerance>0,
choose the fixed u sufficiently large depending on f and that tolerance;
then, for all sufficiently large Y and uniformly in the stated targets,
  |T_low,f/(length(J_real)*S_2(m)*t)-A_f|<tolerance,
  A_f=(f'(0)+f'(1))/2=-h'(0)/2.                       (4)
This is NOT a Y-asymptotic equal to A_f at one fixed u. The Dickman main
is h(a)*rho(a/theta)-theta*integral_0^(a/theta)h'(theta*v)*rho(v)dv,
where a=1/2-2epsilon and theta=delta/u. Divide by2theta*exp(gamma).
The factorial Dickman tail and integral rho=exp(gamma) give (4) as theta
decreases; the fixed sieve error O_f(eta_s/theta^2) tends to0 as well.
Only AFTER u is fixed does Y grow. The polynomial and its derivative are
bounded on[0,1]; rough-divisor multiplicities are bounded at fixed theta,
so the previous replacements, signed sieve and remainder injection apply.
The full weighted prime correlation still includes its unrestricted tail.
The source deduction and Dickman normalization remain those of
cubic_positivity_obstruction.py; no new distribution theorem is assumed.

For the nonnegative subtraction family, let B=sum_{j>=2}(j-2)*c_j.
Then A_f=1-B/2. For a in(1/2,1), b=1-a and v=ab, define
  D_j=(a^j-b^j)/(a-b).
We have D_1=D_2=1, 0<D_j<=1, and D_j=D_(j-1)-v*D_(j-2) for j>=3; hence
  1-D_j=v*sum_{i=1}^{j-2}D_i<=(j-2)*v.               (5)
Equality holds at j=2,3,4; it is strict for j>=5. Therefore
  H_f(a)>=b*(2-B*a*(2*a-1)).                          (6)
In particular B<=2 implies H_f(a)>=2*b^2*(2*a+1)>0. Conversely,
  H_f(a)<=0 implies B>=2/(a*(2*a-1))>2,              (7)
which forces the accessible main in (4) to be negative for sufficiently
large fixed u. Cubic c_3=B or quartic c_4=B/2 attains (6), so higher
degrees cannot improve this pointwise suppression per endpoint-main cost.
The quadratic penalty is ineffective on negative-sign units. These facts
rule out the conjunction of a positive endpoint main and sign deletion of
ANY larger-positive-factor semiprime within this specified safe family.
They do not bound the density of actual semiprimes in a prime-first sum.

The cost of leaving that family can also be stated exactly. For ANY C1
normalized f, three FORMAL negative-prime logarithmic shares x,y,z>0,
x+y+z=1, have normalized triple kernel
  J_f(x,y,z)=1-h(x)-h(y)-h(z).                        (8)
This is the eight-divisor identity for a squarefree all-negative triple.
If J_f<=0 on the ENTIRE open share simplex, substituting y=1-x-z gives
h(x)-h(x+z)+h(z)>=1. Letting z decrease to0 yields h'(x)<=h'(0).
Thus if A_f>0, h'(0)<0 and h decreases strictly to h(1)=-1, so H_f(a)>0
for EVERY 0<a<1. Contrapositively, A_f>0 and H_f(a0)<=0 somewhere force
positive triple weight at some formal shares. For polynomials, A_f is
also the actual conditional accessible-main coefficient in (4).
This does not assert an actual prime-first triple count or arbitrary
character/sign configurations at those proportions.

A concrete alternative preserves the component while exposing its cost:
  f(s)=s-100*s^2*(1-s)^2*(1-2s), A_f=1,
  h(s)=(1-2s)*(1+200*s^2*(1-s)^2), H_f(3/4)=-193/64,
  J_f(9/10,1/25,3/50)=7263/15625>0.                  (9)
Its coefficients leave the nonnegative subtraction family. All-negative
squarefree triples have W=0, so this positive formal triple kernel prevents
reuse of a pointwise K<=C*W argument based on nonpositive triple weights.
The formula is a candidate component, not a new controlled prime-pair bound.
Changing coefficients alone has not closed the correlation gap.
quintic_partner_weight.py now extends absolute rare-factor pruning to this
alternative, identifies its surviving two-through-six-factor terms, and
bounds its positive pure-triple contribution on the main scale. Positive
five-factor terms also survive; sufficient composite control remains open.

Helper inputs are exact rational polynomial coefficients in ascending degree,
not sampled logarithms of actual primes. The degree64 cap is only a finite
verifier limit and is not a restriction on the mathematical identities.
"""
from fractions import Fraction as F
from math import comb


def _rational(value):
    if type(value) is not int and type(value) is not F:
        raise ValueError("require exact integers or Fractions, not rounded values")
    return F(value)


def _coefficients(values):
    if type(values) is not tuple or not 2 <= len(values) <= 65:
        raise ValueError("require a coefficient tuple of degree1 through64")
    result = tuple(_rational(value) for value in values)
    if result[0] != 0 or sum(result) != 1:
        raise ValueError("require f(0)=0 and f(1)=1")
    return result


def semiprime_kernel(coefficients: tuple) -> tuple[F, ...]:
    """Return ascending coefficients of H(a)=1+f(1-a)-f(a), exactly."""
    values = _coefficients(coefficients)
    result = [F(0)]*len(values)
    result[0] = F(1)
    for j, coefficient in enumerate(values):
        for k in range(j+1):
            result[k] += coefficient*comb(j, k)*(-1)**k
        result[j] -= coefficient
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return tuple(result)


def balanced_kernel_enclosure(coefficients: tuple, positive_share) -> tuple[F, F]:
    """Return the derivative-norm enclosure for a RATIONAL formal factor share."""
    values = _coefficients(coefficients)
    share = _rational(positive_share)
    if not 0 <= share <= 1:
        raise ValueError("positive factor share must lie in[0,1]")
    norm = sum((j*abs(value) for j, value in enumerate(values)), F(0))
    radius = norm*abs(1-2*share)
    return 1-radius, 1+radius


def safe_subtraction_coefficients(penalties: tuple) -> tuple[F, ...]:
    """Return f for nonnegative penalties on degrees2,3,..., up to degree64."""
    if type(penalties) is not tuple or len(penalties) > 63:
        raise ValueError("require a tuple of at most63 penalties")
    values = tuple(_rational(value) for value in penalties)
    if any(value < 0 for value in values):
        raise ValueError("safe-subtraction penalties must be nonnegative")
    result = [F(0), 1+sum(values), *(-value for value in values)]
    while len(result) > 2 and result[-1] == 0:
        result.pop()
    return tuple(result)


def type_i_endpoint_coefficient(coefficients: tuple) -> F:
    """Return (f'(0)+f'(1))/2, with the two-parameter meaning in (4).

    This is not the actual total, a fixed-u asymptotic, or a finite onset.
    """
    values = _coefficients(coefficients)
    return (values[1]+sum(j*value for j, value in enumerate(values)))/2


def safe_subtraction_tradeoff(penalties: tuple, positive_share) -> tuple[F, F, F]:
    """Return (B, lower bound for H(a), necessary B for H(a)<=0).

    Requires 1/2<a<1 as an exact rational FORMAL factor share. The last
    value is a necessary cost, not a sufficient condition for this kernel.
    """
    coefficients = safe_subtraction_coefficients(penalties)
    a = _rational(positive_share)
    if not F(1, 2) < a < 1:
        raise ValueError("require exact positive-factor share strictly in(1/2,1)")
    budget = 2-2*type_i_endpoint_coefficient(coefficients)
    return budget, (1-a)*(2-budget*a*(2*a-1)), 2/(a*(2*a-1))


def negative_triple_kernel(coefficients: tuple, shares: tuple) -> F:
    """Return the normalized formal all-negative squarefree triple kernel.

    Three strictly positive rational shares must sum to1. These are formal
    logarithmic proportions, not sampled primes or a prime-first count.
    """
    kernel = semiprime_kernel(coefficients)
    if type(shares) is not tuple or len(shares) != 3:
        raise ValueError("require a tuple of three exact shares")
    values = tuple(_rational(value) for value in shares)
    if any(value <= 0 for value in values) or sum(values) != 1:
        raise ValueError("require positive shares summing exactly to1")
    total = F(4)
    for share in values:
        value = F(0)
        for coefficient in reversed(kernel):
            value = value*share+coefficient
        total -= value
    return total
