"""Proper CRT marginals, hidden quadratic dependence, and product-pair counts.

Owner: Kevin's research. Purpose: test whether combining the smaller residue
models in product_resolution.py can certify their joint target. These are
finite residue densities, not integer prime flags or Goldbach counts.
Sol reviewed both deductions, the coprime-target extension, and the actual
verifier on 2026-09-08. Seven focused tests passed normally and with Python -O.

Setup and projection meaning:
Let D=3Q be odd and squarefree, Q>1, 3 not dividing Q. Write U_d for the
unit group modulo d and E_d for its uniform mean. Let f1,f2:U_D->[0,2]
have mean1. Assume that for EVERY proper divisor d|D their conditional
means at every unit residue modulo d are exactly1. This is substantially
stronger than uniformity at the individual primes. It suffices to check
d=D/p for each prime p|D; subsequent conditional averaging gives the rest.
Let g=f1*f2 be normalized multiplicative convolution on U_D, extended by0
to nonunits. For Q|N and 3 not dividing N set
  T_N=(1/phi(D))*sum_{a mod D} g(a)*g(N-a).
The canonical even target N=2Q is always eligible.

Exact reduction of the joint dependence:
In CRT coordinates (a3,v) in U_3 x U_Q, uniform projection onto Q gives
  fi(a3,v)=1+chi3(a3)*ui(v),  |ui|<=1,
where chi3(1)=1, chi3(2)=-1. The other maximal proper projections imply
that averaging ui over ANY one prime coordinate of U_Q gives0. In
particular E_Q ui=0, and every nonzero multiplicative Fourier coefficient
of ui is nonprincipal in EVERY prime coordinate. Direct convolution gives
  g(a3,v)=1+chi3(a3)*w(v), w=u1*u2, E_Q w=0.
Only a3=N/2 mod3 is allowed in the pair sum; the Q-coordinate is v,-v.
The two linear terms vanish after averaging, so
  2*T_N=1+E_Q w(v)*w(-v).                                (1)

Positive inverse statement:
Let chi_Q be the product of the local Legendre characters, chi_D=chi3*chi_Q,
and ai=E_D fi*chi_D=E_Q ui*chi_Q. If chi_Q(-1)=+1, then T_N>=1/4.
If chi_Q(-1)=-1, writing x=a1^2,y=a2^2 gives
  2*T_N >= F(x,y)=1-xy-(1-x)*(1-y)/2.                     (2)
Consequently T_N<=E<1/4 forces
  ai^2>=1-2E,
  E_D |fi-(1+sign(ai)*chi_D)|=1-|ai|<=1-sqrt(1-2E).        (3)
This concerns the FULL joint character, which all proper projections erase.

Proof:
Finite character orthogonality and Parseval give Fourier masses
xi_i(gamma)=|hat ui(gamma)|^2 of total <=1, since |ui|<=1. Equation(1) is
  2*T_N=1+sum_gamma gamma(-1)*xi_1(gamma)*xi_2(gamma).
The full-coordinate Fourier support contains only one real character,
chi_Q: in each odd prime unit group the only real nonprincipal character
is its Legendre character. All other modes come in distinct conjugate
pairs with equal masses and equal sign at -1. Their negative contribution
is at most half the product of their remaining total masses. If chi_Q is
even, this is <=1/2. If odd, isolate its masses x,y to obtain(2).
For x,y in[0,1], F<1/2 forces x,y>1/2, and there F>=1-x,1-y, proving(3).
The L1 equality follows from the pointwise cap2 on the two chi_D cosets.
This uses the same finite Fourier normalization and conjugate-pair
argument as coupled_product_model.py, now after the CRT projection step.

Exact obstruction to assembly from proper marginals:
Choose chi_Q(-1)=-1 and f1=f2=1+chi_D. Multiplicative orthogonality gives
g=f1, and every proper-divisor projection of f1,f2,g is uniform. All of
their projected pair means at N=2Q are POSITIVE: 1/2 if 3|d, and1 otherwise.
Nevertheless T_N=0 by(1). Taking f1=f2=1 instead gives the SAME proper
projections and full T_N=1/2. Thus even every proper joint projection,
cap2, and exact product coupling together do not determine full positivity.
Examples: D=21,N=14 and D=273,N=182. Arbitrarily many prime coordinates
are possible by multiplying Q=7 by distinct primes1 mod4. Such primes
are infinite: a prime divisor of (2*p1*...*pk)^2+1 is new and has an
element of order4 modulo it, hence is1 mod4.
The inverse bound is sharp: f1=1+chi_D, f2=1+b*chi_D, 0<=b<=1, gives
T_N=(1-b^2)/2 and the second factor's distance1-b. The positive floor1/4
is attained at D=15 by the skew four-cycle used in the focused tests.

Boundary for the next arithmetic step:
The proper projections are computed on full residue periods with their
own unit-group normalizations. They are not exact integer-sum counts.
These examples do not satisfy the prime labels, integer factor windows,
or source distribution estimates of the canonical cubic bootstrap. In
particular, a density on an entire residue period is not a prime flag
array. No Goldbach failure or new actual coverage follows. The result
identifies full joint character dependence as information that projection
assembly can lose; the inverse result has exact uniformity and cap premises,
not a proved approximate transfer for actual primes. Historical novelty
is unassessed. The construction uses3|D and Q|N; it does not refute a
claim restricted to moduli with primes>=7 and targets coprime to D.

Complementary positive theorem for coprime targets:
Let D>1 be odd and squarefree, with least prime divisor p0>=7. For ANY
global densities f1,f2 on U_D in[0,2] with mean1, set g=f1*f2 as above.
No proper-projection uniformity is required in this theorem. If gcd(N,D)=1,
put K=prod_{p|D}(p-2) and theta=K/phi(D). Then
  |T_N-theta|<=theta*(2+sqrt(p0))/(p0-2),
  T_N>=theta*(p0-4-sqrt(p0))/(p0-2)>0.                    (4)
Proof: the nonprincipal multiplicative Fourier coefficients c of g have
sum|c|<=1 by Parseval and Cauchy, exactly as in product_resolution.py.
CRT factors the Jacobi sums. Relative to the principal-principal value K,
a principal/nonprincipal global pair has modulus <=1/(p0-2). For a pair
of nonprincipal global characters, some prime coordinate is active. Its
relative local modulus is either1/(p-2) or sqrt(p)/(p-2); the latter
decreases with p and is <=sqrt(p0)/(p0-2). Every other local factor has
modulus <=1. The two single-nonprincipal terms and the double term give(4).
The local Jacobi identities are those in Keith Conrad, Corollary2.5 and
Theorem2.6, already used in product_resolution.py:
https://kconrad.math.uconn.edu/blurbs/gradnumthy/Gauss-Jacobi-sums.pdf

Why this still does not implement exact integer resolution from prime atoms:
The cap2 in(4) is GLOBAL, not a bound on each smaller marginal. For D>2H,
congruence suffices to resolve sums of integers<=H. If H<(z+1)^3, earlier
cofactor primes<=B=floor(H/(z+1)) occupy k<=B<H^(2/3) distinct unit residues
(consider a nonempty set of such unit primes). Write m=phi(D). Since
  (p-1)^4>=p^3 for p>=7, m>=D^(3/4)>(2H)^(3/4).
The atomic mean-L1 distance from F=m/k on those k residues to any mean1
global cap2 density equals2*max(0,1-2k/m), by product_resolution.py. It is
therefore strictly greater than
  2*(1-2^(1/4)*H^(-1/12)).                                (5)
For H>=8 the cap2 premise fails, and the lower bound tends to2. Thus using
many smaller prime moduli does not repair this particular direct atomic
implementation at the sufficient no-alias scale. The positivity theorem(4)
is valid; its required global density input is missing. A smaller modulus
with proved exclusion of other congruent sums, or a different transfer that
controls joint dependence, is not excluded. No actual Goldbach coverage
or failure follows from either model theorem or the input obstruction.
"""
from fractions import Fraction
from math import gcd, isqrt, prod


def _density_units(values: tuple[int | Fraction, ...]) -> tuple[int, ...]:
    if type(values) is not tuple or len(values) < 3 or len(values) % 2 == 0:
        raise ValueError("require a residue-indexed tuple of odd length >=3")
    modulus = len(values)
    units = tuple(a for a in range(modulus) if gcd(a, modulus) == 1)
    if (any(type(v) not in (int, Fraction) or not 0 <= v <= 2 for v in values)
            or any(values[a] != 0 for a in range(modulus) if gcd(a, modulus) != 1)
            or sum(values) != len(units)):
        raise ValueError("require exact cap2 unit density of mean1, zero at nonunits")
    return units


def unit_projection(values: tuple[int | Fraction, ...], divisor: int
                    ) -> tuple[Fraction, ...]:
    """Conditional mean on unit fibers, indexed by residues0..divisor-1.

    Input is an exact mean1 density in[0,2], zero at nonunits, with slot a
    representing residue a. Output is zero on nonunits. Divisor1 returns
    the sole density value1. This averages weights; it does not count primes.
    """
    units = _density_units(values)
    modulus = len(values)
    if type(divisor) is not int or divisor < 1 or modulus % divisor:
        raise ValueError("require a positive integer divisor of the modulus")
    phi_divisor = sum(gcd(a, divisor) == 1 for a in range(divisor))
    fiber_size = len(units)//phi_divisor
    projected = [Fraction(0)]*divisor
    for a in units:
        projected[a % divisor] += Fraction(values[a], fiber_size)
    return tuple(projected)


def _squarefree_odd_primes(modulus: int) -> tuple[int, ...]:
    if type(modulus) is not int or modulus < 3 or modulus % 2 == 0:
        raise ValueError("require an odd squarefree integer modulus >=3")
    rest, p, primes = modulus, 3, []
    while p*p <= rest:
        if rest % p == 0:
            primes.append(p)
            rest //= p
            if rest % p == 0:
                raise ValueError("require a squarefree modulus")
        p += 2
    if rest > 1:
        primes.append(rest)
    return tuple(primes)


def _product_pair(first, second, units, target):
    modulus = len(first)
    weights = [Fraction(0)]*modulus
    for a in units:
        for b in units:
            weights[a*b % modulus] += Fraction(first[a]*second[b], len(units))
    pairs = sum((weights[a]*weights[(target-a) % modulus] for a in units),
                Fraction(0))/len(units)
    return tuple(weights), pairs


def joint_product_profile(first: tuple[int | Fraction, ...],
                          second: tuple[int | Fraction, ...], target: int
                          ) -> tuple[tuple[Fraction, ...], Fraction]:
    """Return exact joint product density and its normalized target pair mean.

    Tuples use residue coordinates INCLUDING0, unlike field_product_pairs.
    Enforces cap2, mean1, all proper-divisor uniformity, D=3Q squarefree,
    and a nonnegative even target divisible by Q but not3. Only tiny finite
    models are intended: multiplication takes O(phi(D)^2) exact operations.
    The returned mean is neither G(target) nor a bound on G(target).
    """
    units = _density_units(first)
    _density_units(second)
    if len(first) != len(second):
        raise ValueError("require densities on the same modulus")
    modulus = len(first)
    primes = _squarefree_odd_primes(modulus)
    if modulus <= 3 or modulus % 3:
        raise ValueError("require D=3Q with Q>1 and 3 not dividing Q")
    q = modulus//3
    if (type(target) is not int or target < 0 or target % 2
            or target % q or target % 3 == 0):
        raise ValueError("require even target divisible by Q and not3")
    for values in (first, second):
        for p in primes:
            divisor = modulus//p
            expected = tuple(int(gcd(a, divisor) == 1) for a in range(divisor))
            if unit_projection(values, divisor) != expected:
                raise ValueError("require uniform proper-divisor unit projections")
    return _product_pair(first, second, units, target)


def coprime_product_profile(first: tuple[int | Fraction, ...],
                            second: tuple[int | Fraction, ...], target: int
                            ) -> tuple[tuple[Fraction, ...], Fraction]:
    """Exact model at a unit target for squarefree D with all prime factors>=7.

    Enforces the GLOBAL cap2, mean1 density premise, with residue slots
    including0. No proper-marginal uniformity is required. A positive model
    mean does not certify an actual integer prime pair.
    """
    units = _density_units(first)
    _density_units(second)
    if len(first) != len(second):
        raise ValueError("require densities on the same modulus")
    modulus = len(first)
    if min(_squarefree_odd_primes(modulus)) < 7:
        raise ValueError("require all prime factors >=7")
    if type(target) is not int or target < 0 or gcd(target, modulus) != 1:
        raise ValueError("require a nonnegative integer unit target")
    return _product_pair(first, second, units, target)


def crt_pair_floor(modulus: int, *, denominator: int = 16) -> Fraction:
    """Rational version of(4), conditional on global densities and a unit target.

    This checks the modulus, not the density inputs or integer-sum transfer.
    A coarse denominator may yield a weaker nonpositive floor.
    """
    primes = _squarefree_odd_primes(modulus)
    p0 = min(primes)
    if p0 < 7:
        raise ValueError("require all prime factors >=7")
    if type(denominator) is not int or denominator < 1:
        raise ValueError("require a positive integer denominator")
    sqrt_upper = Fraction(isqrt(p0*denominator*denominator)+1, denominator)
    theta = Fraction(prod(p-2 for p in primes), prod(p-1 for p in primes))
    return theta*(p0-4-sqrt_upper)/(p0-2)
