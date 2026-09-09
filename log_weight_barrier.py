"""Exact obstruction to removing balanced semiprimes with higher log weights.

Owner: Kevin's research. Purpose: decide whether raising the degree of the
cubic character weight can finish its missing pointwise composite control.
This is a limitation of a specified kernel family, not of Goldbach proofs.
The rational helpers verify polynomial identities and coefficient costs.

Sol checked the theory and actual files. Five focused exact tests passed
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
