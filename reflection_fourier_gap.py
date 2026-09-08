"""A single missing sum is compatible with strong Fourier norm control.

Owner: Kevin's research. Purpose: determine what the remaining norm/energy
estimates can imply before seeking target-specific arithmetic control.
Sol reviewed the argument and actual verifier on 2026-09-08. Four tiny
exact Fourier/moment tests passed normally and with Python -O.
This adds a Fourier theorem to the
existing reflection construction; it does not repeat its frozen range run.
The sets are ARTIFICIAL, not primes or counterexamples to Goldbach or L.

Finite-H concentration lemma:
Fix an even wheel Q>=2, let H be a positive multiple of 2Q, and let U be
the units in 1..H-1. Its independent reflection orbits are {a,H-a}; H/2
is ineligible. On each orbit choose10,01,00 with probabilities p,p,1-2p,
where 0<p<=1/2. Write A for the chosen indicator and V=A-p*1_U.
With Fourier convention Vhat(alpha)=sum_n V(n)*exp(2*pi*i*n*alpha),
  Pr(||Vhat||_infinity>8*sqrt(H*log H)+1)<=4*H**(-5).       (1)
The self-convolution A*A(H) is identically zero.

Proof:
At a fixed frequency each orbit's centered complex contribution Z has
|Z|<=2, and both its real and imaginary parts have mean zero. For any
real centered W in [-2,2], convexity gives
  E exp(sW)<=cosh(2s)<=exp(2s*s).
The last inequality follows by comparing the power series, using
(2j)!>=2**j*j!. There are at most H/2 independent orbits. Optimizing
the exponential bound separately for each real/imaginary tail yields
  Pr(|Vhat(alpha)|>=t)<=4*exp(-t*t/(8H)).
On the H**3 equally spaced frequencies, a union bound at
t=8*sqrt(H*log H) is at most4*H**(-5). For every outcome,
  |Vhat'(alpha)|<=2*pi*sum_{n=1}^{H-1}n*|V(n)|<=pi*H**2.
Every frequency is within1/(2H**3) of the grid, so the interpolation
loss is <=pi/(2H)<1. This proves (1) on the ENTIRE circle, not just
the four frequencies evaluated by the finite verifier below.

Simultaneous coverage away from H, robust to a forced prefix:
Assume H>=48Q and 0<=B<=H/(32Q) is an integer. For each even
k in [H/2,3H/2], k!=H, potential unordered distinct pairs of units
summing to k number at least H/(4Q)-2. Indeed their ordered positions
form an interval of length at least H/2-1, and at least one residue
class modulo Q permits both positions to be units: choose an odd class
at2 and avoid the at most two forbidden classes at each odd prime,
then use CRT, also for prime powers if Q is not squarefree.

Discard all vertices <=B or >=H-B, at most2B vertices. For this fixed
k each vertex lies in at most one potential pair, so at most2B edges
are lost. The graph on reflection orbits has degree at most2: an orbit
contains two vertices, each incident to at most one pair. There are
no loops since k!=H and diagonal pairs were removed. A greedy matching
therefore retains at least one edge per three edges, hence at least
  floor(H/(24Q))
edges under the stated H,B bounds. Their events of being selected are
independent, each with probability p*p. Union over the at most H central
even targets bounds any missing noncentral target by
  H*exp(-p*p*floor(H/(24Q))).                              (2)

Now force ANY binary labels at positions1..B, and delete H-a for each
newly prescribed included a. Position0 stays0. At most2B flags change,
and the H-hole remains protected since 2B<H. The retained core edges
above are untouched. The Fourier perturbation is at most2B by the
triangle inequality. Thus the same sample simultaneously permits every
such prefix while obeying (1) with an extra2B and the coverage event
of (2). In particular its prefix can be the truthful primes through B;
then counts for targets<=B are exact too. Primes dividing Q may be
inserted by this operation: the wheel condition above the forced prefix
is retained, while the baseline remains the original fixed wheel.
No prime-divisor classification rule is imposed on the remaining set.

Prime-density scaling and the Fourier-only gap:
Put c=Q/phi(Q), ell=ceil(log H), p=c/ell<=1/2 for sufficiently large H,
F=ell*A_after_prefix and M=c*1_U. Choose B=floor(H**beta) with fixed
0<=beta<1. Since Hp*p tends to infinity faster than log H, (1) and
(2) hold simultaneously with probability tending to1. Such samples
therefore exist separately for each sufficiently large admissible H,
with no assertion of a nested infinite set. They satisfy
  ||Fhat-Mhat||_infinity
       =O_Q(sqrt(H)*log(H)**(3/2)+B*log H),
  F*F(H)=0,                 M*M(H)=c*H,
and every other central even target is represented. The second equality
uses |U|=H*phi(Q)/Q exactly. The model mean sum M=H is prime-density
normalized. For any fixed 0<epsilon<1/2 and beta<1-epsilon, the Fourier
error is o(H**(1-epsilon)), despite this isolated missing sum.

This also fits the generic pair-error identity and energy estimate:
  F*F-M*M=(F-M)*(F+M),  ||F+M||_2**2=O_Q(H*log(H)**2).
Parseval allows a large pair error concentrated at one target. The
pointwise Cauchy bound from only Fourier norm eta and this L2 bound is
O(eta*sqrt(H)*log H); to make it o(H) by that route requires
eta=o(sqrt(H)/log H). A saving eta=O(H**(1-epsilon)), epsilon<1/2,
does not supply that condition.

Scope: the result prevents a deduction of every-target coverage or forced
failure clustering from just nonnegativity, prime-scale density, fixed-wheel
data, a growing truthful prefix, and these Fourier/energy estimates.
It does NOT meet the full growing-sieve or prime/semiprime multiplicative
hypotheses of our actual L argument. It does not invalidate its almost-all
theorems or establish an actual failed target. The next missing ingredient
is arithmetic control of the combined actual prime/composite pair error,
not a claim that no stronger method can work.
"""
from fractions import Fraction

from reflected_wheel_model import reflection_orbits


_ROOTS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def quarter_fourier(values: tuple[int | Fraction, ...]
                    ) -> tuple[tuple[Fraction, Fraction], ...]:
    """Exact positive-exponent Fourier values at 0,1/4,1/2,3/4.

    Return (real,imaginary) pairs. These four values do not certify a
    whole-circle supremum; that bound is proved analytically above.
    """
    if any(type(value) not in (int, Fraction) for value in values):
        raise ValueError("require exact rational coefficients")
    output = []
    for k in range(4):
        real = imaginary = Fraction(0)
        for n, value in enumerate(values):
            a, b = _ROOTS[k*n % 4]
            real += value*a
            imaginary += value*b
        output.append((real, imaginary))
    return tuple(output)


def reflection_variance_quarter(center: int, wheel: int,
                                probability: int | Fraction) -> tuple[Fraction, ...]:
    """Exact E|Vhat(k/4)|**2 from independent orbit contributions.

    This uses within-orbit exclusion, not independent endpoint bits.
    The finite helper allows p=0; the coverage theorem requires p>0.
    """
    if (type(probability) not in (int, Fraction)
            or not 0 <= probability <= Fraction(1, 2)):
        raise ValueError("require an exact rational probability in [0,1/2]")
    p = Fraction(probability)
    orbits = reflection_orbits(center, wheel)
    output = []
    for k in range(4):
        variance = Fraction(0)
        for a, b in orbits:
            ar, ai = _ROOTS[k*a % 4]
            br, bi = _ROOTS[k*b % 4]
            variance += 2*p-p*p*((ar+br)**2+(ai+bi)**2)
        output.append(variance)
    return tuple(output)
