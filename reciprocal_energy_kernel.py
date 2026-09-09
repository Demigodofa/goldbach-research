"""Modulus-averaged reciprocal energy saves the symmetric boundary box.

Owner: Kevin's Goldbach research. Purpose: test an additional arithmetic
cancellation mechanism where the previous composite model budgets reached Y.
The proof uses fourth moments, integer divisors and exact rational relations.
It preserves the polynomial, completion and prime-power components already
proved. This is a mathematical component, not the signed prime-pair estimate.
No external additive-energy theorem, primality assumption, or novelty claim
is needed. Finite routines below guard identities, not asymptotic theorems.

I. The modulus-average energy bound.
Let C,A>=1 and t be a NONZERO integer. For each integer q in[C,2C], q>=2,
let E_(q,t)(A) count a1,a2,a3,a4 in[A,2A], all q-units, satisfying
  t*(1/a1+1/a2-1/a3-1/a4)=0 (modq).
For A,C,|t| bounded by a fixed power of Y, every epsilon>0 gives
  sum_q E_(q,t)(A) <<Y^epsilon*(A^4+C*A^2).                (1)
The same t is used across q; multiplication by any q-dependent unit r_q
does not change the condition. t need not be coprime to q.

Proof: clearing unit denominators gives q|t*D, where
  D=(a1+a2)*a3*a4-(a3+a4)*a1*a2, |D|<=32*A^3.            (2)
For each quadruple with D!=0, the number of eligible q is at most
tau(|t*D|)<<Y^epsilon. This gives the A^4 term, after discarding the
unit restriction for an upper bound. D=0 is treated separately and never
put into a divisor-count expression. Fix a1,a2 and reduce
  u/v=1/a1+1/a2, u,v>0, gcd(u,v)=1, v<=4*A^2.
Then the rational relation with a3,a4 is EXACTLY
  (u*a3-v)*(u*a4-v)=v^2.                                  (3)
Both factors are positive: u*a3-v=v*a3/a4. Every ordered solution
therefore comes from a positive divisor of v^2, giving O(A^epsilon)
choices. There are O(A^2) choices of a1,a2 and O(C) possible moduli.
This proves(1), uniformly in all prime powers and nonunit t.

II. Weighted bilinear reciprocal sums.
Let |alpha_q(M)|,|beta_q(a)|<=1 be arbitrary complex coefficients on
M in[B,2B],a in[A,2A], and let r_q be any q-unit. Put
  S_q=sum_(M,a; gcd(M*a,q)=1)alpha_q(M)*beta_q(a)
                                    *e_q(r_q*t/(M*a)).
The coefficients may vary with q. Holder in M gives
  |S_q|^4 <<B^3*sum_(M unitsq)|sum_a beta_q(a)e_q(r_q*t/(M*a))|^4.
There are at most O(1+B/q) representatives of any inverse residue in
[B,2B]. Enlarge to all residues x modulo q. Orthogonality, followed by
absolute values of the four coefficients, gives
  sum_(x modq)|sum_a beta_q(a)e_q(r_q*t*x/a)|^4
       <=q*E_(q,t)(A).
Thus this remains valid even for B>q:
  |S_q|^4 <<B^3*(B+C)*E_(q,t)(A).
Holder in q and (1) prove
  sum_q |S_q| <<Y^epsilon*R(B,A,C),
  R(B,A,C)=C^(3/4)*B^(3/4)*(B+C)^(1/4)
                              *(A^4+C*A^2)^(1/4).         (4)
Exchanging M,a gives the minimum of R(B,A,C),R(A,B,C).
When B<=C the first expression is at most a constant times
  C*B^(3/4)*A+C^(5/4)*B^(3/4)*A^(1/2).
No cancellation between the weighted fourth-moment terms is assumed:
the arithmetic gain is the modulus average of their positive majorant.

III. The actual smooth MODEL and paid period/frequency costs.
Use the general family in composite_linear_kernel.py:
  B=Y^b,A=Y^x,C=Y^y,K=B*A*C/Y,
  1/5<=b<=13/25, 0<=x<=(1-b)/2, 0<=y<=1/2,
  m integer in[Y,2Y], 1<=J0,H<=Y^(1/4096).
For ALL integers q in[C,2C], q>=2, choose unit r_q and period J_q<=J0.
Let |omega_(q,k)|<=1 be jointly periodic modulo J_q, with arbitrary q,k
dependence. For fixed smooth W1,W2 supported in[1,2], define
  E_q=Y/(B*A*q)*sum_(1<=k<=H*K) sum_(M,a>=1; gcd(M*a,q)=1)
       W1(M/B)W2(a/A)*omega_(q,k)(M,a)*e_q(r_q*m*k/(M*a)).
Then
  sum_q |E_q| <<Y^epsilon*H*J0^2
                           *min(R(B,A,C),R(A,B,C)).        (5)

Proof: expand omega in its double period-J Fourier series. There are J^2
terms with coefficients of magnitude<=1. Each is separated between M,a;
its coefficient is absorbed into one side. Pad the frequency labels to
J0^2 positions across q, or use the same uniform fourth-moment majorant
for every component. This costs J0^2, with no gcd(q,J) restriction.
For each fixed positive k, apply(4) with t=m*k, a common nonzero integer
across q of size at most a fixed power of Y. Multiplying the prefactor
O(Y/(B*A*C)) by the number of k, at most H*B*A*C/Y, gives H. If there
is no positive k, the sum is empty. This proves(5). It includes all axes
automatically because there was no spatial Poisson decomposition.

The same proof allows arbitrary bounded separated spatial coefficients,
including character or roughness restrictions which actually separate.
Uniformly smooth coupled spatial weights can also use the previously
proved Fourier-series corollary in decorated_prime_kernel.py, with its
uniform derivative hypotheses and all series costs retained. Arbitrary
coupled arithmetic weights are NOT licensed by this assertion.

At the formerly failing symmetric box B=A=Y^(1/4),C=Y^(1/2),K=1,
  sum_q |E_q| <<Y^(15/16+epsilon)*H*J0^2
              <<Y^(3843/4096+epsilon).                    (6)
More generally, monotonicity of R shows that b,x<=9/32 and y<=1/2 give
exponent at most127/128 before decorations, hence4067/4096 after caps.
The original family restrictions still apply. This is a proved extra
region for all integer moduli, not merely a prime or squarefree theorem.

Reassessment: this concrete reciprocal-energy mechanism SUCCEEDS at the
critical symmetric box. It extends the model toolkit and leaves all earlier
polynomial identities and bounds available. It does not prove full box
coverage, the original sieve/weight transfer, or the actual signed prime
correlation. Latest original-affine estimate remains2b8cf98. No actual
exceptional zero, effective onset, prime coverage, or originality is claimed.

Two boundaries guide the next test. First, at b=1/2,x=1/4,y=1/2, the
new energy bound has exponent9/8, while the previous linear bound has1.
These are failures of these upper budgets, not lower bounds on the true
sum. Second, t must stay common across q up to a unit multiplier. Allowing
arbitrary t_q=q makes every phase1, so the divisor-average proof collapses.
The next cancellation mechanism must address the remaining unbalanced box
or an actual arithmetic transfer with all dependence retained.
"""
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import gcd

from composite_linear_kernel import _reduce
from major_arc_kernel import _factorization


def _interval(lower, upper):
    if (type(lower) is not int or type(upper) is not int
            or lower < 1 or upper < lower):
        raise ValueError("require a nonempty positive integer interval")
    return tuple(range(lower, upper+1))


def _divisors(n):
    values = [1]
    for p, exponent in _factorization(n):
        values = [value*p**power for value in values for power in range(exponent+1)]
    return tuple(sorted(values))


def reciprocal_polynomial(a, b, c, d):
    if any(type(value) is not int or value < 1 for value in (a, b, c, d)):
        raise ValueError("reciprocal denominators must be positive integers")
    return (a+b)*c*d-(c+d)*a*b


def rational_pair_solutions(first, second, lower, upper):
    _interval(lower, upper)
    reciprocal_polynomial(first, second, first, second)
    common = gcd(first+second, first*second)
    u, v = (first+second)//common, first*second//common
    solutions = []
    for left in _divisors(v*v):
        right = v*v//left
        if (left+v) % u or (right+v) % u:
            continue
        a, b = (left+v)//u, (right+v)//u
        if lower <= a <= upper and lower <= b <= upper:
            solutions.append((a, b))
    return tuple(sorted(solutions))


def _energy_parameters(q, parameter, lower, upper, weights):
    values = _interval(lower, upper)
    if type(q) is not int or q < 2 or type(parameter) is not int:
        raise ValueError("require modulus at least2 and an integer parameter")
    if weights is None:
        weights = (1,)*len(values)
    if len(weights) != len(values) or any(type(w) is not int for w in weights):
        raise ValueError("require one integer weight per interval element")
    return values, tuple(weights)


def reciprocal_energy(q, parameter, lower, upper, weights=None):
    """Weighted real fourth-moment energy, computed by pair residue counts."""
    values, weights = _energy_parameters(q, parameter, lower, upper, weights)
    units = [(pow(a, -1, q), weight) for a, weight in zip(values, weights)
             if gcd(a, q) == 1]
    pairs = Counter()
    for a, wa in units:
        for b, wb in units:
            pairs[parameter*(a+b) % q] += wa*wb
    return sum(value*value for value in pairs.values())


def _cyclic_product(left, right):
    q = len(left)
    result = [0]*q
    for i, a in enumerate(left):
        if a:
            for j, b in enumerate(right):
                if b:
                    result[(i+j) % q] += a*b
    return result


def fourth_moment_exact(q, parameter, lower, upper, weights=None):
    """Direct sum of fourth powers, exactly reduced in Q[zeta_q]."""
    values, weights = _energy_parameters(q, parameter, lower, upper, weights)
    units = [(pow(a, -1, q), weight) for a, weight in zip(values, weights)
             if gcd(a, q) == 1]
    total = [0]*q
    for frequency in range(q):
        raw, conjugate = [0]*q, [0]*q
        for inverse, weight in units:
            phase = parameter*frequency*inverse % q
            raw[phase] += weight
            conjugate[-phase % q] += weight
        squared = _cyclic_product(raw, conjugate)
        fourth = _cyclic_product(squared, squared)
        total = [a+b for a, b in zip(total, fourth)]
    return _reduce(total, q)


@dataclass(frozen=True)
class EnergyDecomposition:
    zero_relation: int
    nonzero_relation: int
    total: int
    rational_quadruples: int
    divisor_triangle: int


def modulus_energy_prediction(c, parameter, lower, upper):
    """Independent integer-polynomial/divisor decomposition of the q sum."""
    values = _interval(lower, upper)
    if (type(c) is not int or c < 2 or type(parameter) is not int or parameter == 0):
        raise ValueError("require C>=2 and a common nonzero integer parameter")
    zero = nonzero = rational = triangle = 0
    for a, b, d, e in product(values, repeat=4):
        polynomial = reciprocal_polynomial(a, b, d, e)
        denominator = a*b*d*e
        if polynomial == 0:
            rational += 1
            zero += sum(gcd(q, denominator) == 1 for q in range(c, 2*c+1))
        else:
            divisors = _divisors(abs(parameter*polynomial))
            triangle += len(divisors)
            nonzero += sum(c <= q <= 2*c and gcd(q, denominator) == 1 for q in divisors)
    return EnergyDecomposition(zero, nonzero, zero+nonzero, rational, triangle)


@dataclass(frozen=True)
class ReciprocalEnergyBudget:
    active: bool
    frequency: F
    first_orientation: F
    second_orientation: F
    total: F
    saving: F
    small_box_region: bool


def energy_budget(b, x, y, period_exponent=0, frequency_exponent=0):
    values = (b, x, y, period_exponent, frequency_exponent)
    if any(type(v) not in (int, F) for v in values):
        raise ValueError("exponents must be exact rational numbers")
    b, x, y, j, h = map(F, values)
    if not (F(1, 5) <= b <= F(13, 25) and 0 <= x <= (1-b)/2
            and 0 <= y <= F(1, 2)):
        raise ValueError("box lies outside the stated general family")
    if any(not 0 <= v <= F(1, 4096) for v in (j, h)):
        raise ValueError("decoration exponents must lie in[0,1/4096]")
    def orientation(outer, inner):
        return F(3, 4)*(y+outer)+max(outer, y)/4+max(4*inner, y+2*inner)/4
    first, second = orientation(b, x), orientation(x, b)
    frequency = b+x+y-1+h
    total = min(first, second)+2*j+h if frequency >= 0 else F(0)
    return ReciprocalEnergyBudget(frequency >= 0, frequency, first, second,
                                  total, 1-total, max(b, x) <= F(9, 32))
