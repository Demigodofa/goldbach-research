"""Pointwise prime exponential-sum bounds cannot pay the active-band energy.

This source-gates the first use of Vaughan/Heath--Brown machinery on the
opposite-prime variable after ``active_frequency_spacing_gate.py``. The full
Lambda sum may legitimately be decomposed into Type I/II sums; this does not
claim that an individual prime has acquired factors. The distinction matches
Helfgott, *The ternary Goldbach problem*, arXiv:1501.05438, equations
(3.6)--(3.9), printed pp.55--56:
https://arxiv.org/pdf/1501.05438 .

The strongest checked pointwise input is Maynard--Pandey--Radziwill,
*Exponential sums over primes*, arXiv:2608.14777v1, Theorem 1.1, printed p.2,
checked 2026-09-10:
https://arxiv.org/pdf/2608.14777v1 . If

  alpha=a/q+epsilon, (a,q)=1, q<=X^(1/2),
  |epsilon|<=1/(q*X^(1/2)), D=max(q,q*X*|epsilon|),

then

  |sum_(n<X) Lambda(n)e(alpha*n)|
       <= X^(o(1))*(X/D^(1/2)+X^(19/24)).                  (1)

The paper's D is called B; D is used here to avoid collision with the
short-divisor cutoff in this repository. The source's theorem is pointwise,
not an average over our m,h family.

Apply (1) to the reduced rational alpha=h/m in the critical d=1 block,
m=X^(59/100), 0<h<m. Dirichlet supplies a/q with q<=X^(1/2). It cannot equal
h/m because m>X^(1/2). Rational separation gives

  |h/m-a/q|>=1/(m*q), hence q*X*|epsilon|>=X/m=X^(41/100). (2)

Thus D>=X^(41/100), and (1) gives the pointwise exponent

  max(1-41/200,19/24)=159/200=.795.                       (3)

The prime-only log sum differs from Lambda by proper prime powers, of size
X^(1/2+o(1)); the d=1 low-projector correction has size X/m=X^(41/100)
up to logs. Both are below (3).

There are X^(27/25+o(1)) active (m,h) pairs, and the energy has weight
1/m=X^(-59/100), ignoring logarithms. Summing the square of (3) pointwise
therefore gives

  E_band <= X^(27/25-59/100+2*(159/200)+o(1))
          = X^(52/25+o(1))=X^(2.08+o(1)).                 (4)

The existing all-frequency variance has exponent 1+59/100=1.59; the desired
H^(-1) band fraction has exponent 1.49. Hence (4) misses by X^(59/100).
The classical 4/5 bound gives 2.09 and misses by X^(3/5). The new theorem is
a real improvement, but only by X^(.01) after squaring.

More generally, if a pointwise bound X^(s+o(1)) is summed over every active
frequency, its energy exponent is 59/100-1/10+2s. To reach
1+59/100-1/10 one needs s<=1/2 exactly. Therefore no plausible incremental
pointwise improvement closes this route; averaging must occur before taking
absolute values. A sourced Type I/II expansion remains a useful component,
but only if its factors are estimated jointly over the dense m,h family.

No such averaged estimate is proved here. The fixed prime-log active-energy
conjecture, endpoint/mask transfer and signed Goldbach correlation remain open.
"""
from fractions import Fraction as F
from math import gcd


M = F(59, 100)
H = F(1, 10)
SOURCE_TERM = F(19, 24)
CLASSICAL_TERM = F(4, 5)


def rational_separation_floor(denominator_exponent=M):
    """Exponent of X/m forced in the source's Diophantine quantity."""
    if not isinstance(denominator_exponent, F) or not F(1, 2) < denominator_exponent < 1:
        raise ValueError("exact denominator exponent must lie in (1/2,1)")
    return 1 - denominator_exponent


def source_pointwise_exponent(denominator_exponent=M,
                              source_term=SOURCE_TERM):
    separation = rational_separation_floor(denominator_exponent)
    return max(1 - separation / 2, source_term)


def classical_pointwise_exponent(denominator_exponent=M):
    separation = rational_separation_floor(denominator_exponent)
    return max(1 - separation / 2, CLASSICAL_TERM)


def pointwise_energy_budget(pointwise_exponent=None):
    """Exact d=1 exponent ledger for summing an individual bound over m,h."""
    if pointwise_exponent is None:
        pointwise_exponent = source_pointwise_exponent()
    if not isinstance(pointwise_exponent, F) or not 0 <= pointwise_exponent <= 1:
        raise ValueError("exact pointwise exponent in [0,1] required")
    frequency_count = 2 * M - H
    energy = frequency_count - M + 2 * pointwise_exponent
    all_variance = 1 + M
    required_band = all_variance - H
    return {
        "active_frequency_count": frequency_count,
        "pointwise_exponent": pointwise_exponent,
        "pointwise_energy": energy,
        "all_frequency_variance": all_variance,
        "required_band_energy": required_band,
        "gap": energy - required_band,
        "required_pointwise_exponent": F(1, 2),
        "pointwise_route_closes": energy <= required_band,
        "averaged_type_I_II_estimate_proved": False,
    }


def diophantine_separation(N, h, m, a, q):
    """Exact finite version of (2) for a distinct reduced approximation a/q."""
    if not all(type(value) is int for value in (N, h, m, a, q)):
        raise ValueError("integer inputs required")
    if N < 1 or m < 2 or q < 1 or not 0 < h < m or not 0 <= a <= q:
        raise ValueError("inputs outside the stated rational ranges")
    if gcd(h, m) != 1 or gcd(a, q) != 1:
        raise ValueError("both rational fractions must be reduced")
    exact = F(h, m)
    approximation = F(a, q)
    if exact == approximation:
        raise ValueError("the approximation must be distinct")
    distance = abs(exact - approximation)
    scaled = q * N * distance
    return {
        "distance": distance,
        "scaled_D_term": scaled,
        "separation_lower_bound": F(1, m * q),
        "scaled_lower_bound": F(N, m),
        "separation_holds": distance >= F(1, m * q),
        "scaled_floor_holds": scaled >= F(N, m),
    }
