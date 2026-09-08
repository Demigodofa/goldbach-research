"""An exact signed-survivor identity and a failed linear-sieve plug-in.

Owner: Kevin's research. Purpose: test target-specific information that the
reflection countermodel lacks, without mistaking a standard sieve bound
for the stronger correlation needed. Sol reviewed the argument and actual
verifier, 2026-09-08. Four focused exact tests passed normally and with
Python -O, including logarithm intervals and prime-square diagonals.

Exact identity:
For one canonical cubic target N, let A=P+C be the square-start survivors,
partitioned into odd primes P and composites C. Every C-entry has exactly
two prime factors counted with multiplicity. Put D=P-C. Then
  D(n)=-lambda(n)*A(n),
where lambda is Liouville's function (-1)**Omega(n). In particular prime
squares have lambda=+1; replacing lambda with Mobius would be incorrect.
Writing T=[P*A]_N, M=[A*A]_N and d=C(N/2),
  L(N)=[D*A]_N+d=2*T-M+d.                                 (1)
This uses the actual partition, rather than independent model labels.

Scope of the coefficient obstruction below:
It concerns ONLY substituting the standard one-dimensional lower linear
sieve for T in (1), along with the explicitly granted leading upper bound
for M below. It does not bound actual L from above, exclude every possible
sieve refinement, or show that any Goldbach target fails. Stronger coupled
arithmetic estimates or a substantially smaller known M are not ruled out.

Generous benchmark for that particular plug-in:
Fix 2<=u<=3, z=N**(1/u), K=S_2(N)*N/log(N)**2, and t=log(u-1).
The canonical cubic case is u=3; harmless integer cutoffs use H=N-3.
GRANT, without asserting a new uniform pair theorem, that
  M<=((1+t)**2+o(1))*K.                                   (2)
Also grant the shifted-prime sequence the hypotheses needed by the linear
sieve at any fixed distribution exponent 0<theta<1. This is an assumption
for testing the method; no new prime distribution theorem is claimed.

Normalization and the standard lower term:
Sieve n=N-p with p an odd prime in3..N-3, removing p|N first. At an odd
prime r not dividing N, the local removed proportion is 1/(r-1); at r|N
and at2 it is zero. Its size is X~N/log N and its sieve product is
  V_N(z)=product_{3<=r<=z, r prime, r not dividing N}(1-1/(r-1))
        ~exp(-gamma)*S_2(N)/log z.
For the product identity, split each unrestricted odd local factor as
(1-1/r)*(1-1/(r-1)**2), apply Mertens, and then restore the factors for
r|N. Divisors r>z contribute only1+o(1) uniformly, since their number is
bounded for fixed u and each factor differs from1 by O(1/z).
Removing p|N costs at most O(log N) positions. Preserving small prime
complements <=z in the square-start sieve adds at most O(z) positions.
Both are o(K), as is d<=1, and do not change the following coefficient.
Rounding z, replacing N by H=N-3, or changing p<z to p<=z affects only
O(1) boundary prime filters. They change at most O(N/z) positions, also
o(K) throughout2<=u<=3. Thus these conventions do not change the benchmark.

The standard source gives the lower term X*V_N(z)*f(s), with s=theta*u,
  f(s)=0                     for 0<s<=2,
  f(s)=2*exp(gamma)*log(s-1)/s for 2<=s<=4.
Thus the supplied lower coefficient for T/K is u*exp(-gamma)*f(theta*u).
Primary source: Weighted sieves with switching, Definition2.4,
equations(2.4)-(2.5), Lemma2.5 (read 2026-09-08):
https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/weighted-sieves-with-switching/986429394BA969687D48224E177E2F1C
That lemma has theta<1. The value theta=1 below is ONLY a limiting
coefficient benchmark, not an application of its theorem at an endpoint.

The plug-in coefficient cannot be positive:
On2<s<=3, the derivative of log(s-1)/s has numerator
s/(s-1)-log(s-1)>=3/2-log2>0. Hence f is increasing throughout the
relevant range, including its zero part. Since theta*u<=u<=3,
  u*exp(-gamma)*f(theta*u)<=2*log(u-1)=2*t.
The resulting lower-certificate coefficient in 2*T-M is therefore at most
  4*t-(1+t)**2=-(1-t)**2
              <=-(1-log2)**2 < -121/1296.                 (3)
The last rational inequality uses the already checked log2<25/36.
At u=3 and theta tending1 this coefficient is exactly -(1-log2)**2.
At theta<=2/u the lower sieve contributes zero, making the coefficient
even less useful. A negative LOWER certificate has no implication that
L itself is negative. This rejects the proposed direct plug-in as a
universal positivity argument under these grants, while preserving (1)
for future correlation or switching work. No numerical onset, actual
failed target, historical novelty, or impossibility for all sieves follows.
The later coupled_product_model.py tests a different proposed input: exact
multiplicative convolution of a bounded residue distribution with itself.
Even that product coupling alone permits a negative signed pair margin.
Its sharp finite stability theorem singles out odd quadratic cosets; it
does not impose the actual integer factor ranges or prime distribution.

Rational verifier:
For1<=x<=2, y=(x-1)/(x+1) lies in[0,1/3]. The first m positive terms of
  log x=2*sum_{j>=0}y**(2j+1)/(2j+1)
give a lower bound. A geometric upper bound for the omitted tail is
2*y**(2m+1)/((2m+1)*(1-y*y)). All returned endpoints are exact Fractions.
"""
from fractions import Fraction


def log_enclosure(x: int | Fraction, terms: int = 12) -> tuple[Fraction, Fraction]:
    """Certified rational enclosure for log(x), 1<=x<=2."""
    if type(x) not in (int, Fraction) or not 1 <= x <= 2:
        raise ValueError("require an exact rational x in [1,2]")
    if type(terms) is not int or not 1 <= terms <= 128:
        raise ValueError("terms must be an integer in [1,128]")
    x = Fraction(x)
    y = (x-1)/(x+1)
    lower = 2*sum((y**(2*j+1)/Fraction(2*j+1) for j in range(terms)), Fraction(0))
    tail = 2*y**(2*terms+1)/((2*terms+1)*(1-y*y))
    return lower, lower+tail


def linear_plugin_coefficient(u: int | Fraction, theta: int | Fraction,
                               terms: int = 12) -> tuple[Fraction, Fraction]:
    """Enclose the proposed certificate's coefficient, NOT actual L/K.

    Require2<=u<=3 and0<theta<=1. theta=1 is the limiting benchmark;
    it is not a proved distribution assumption or source endpoint theorem.
    """
    if (type(u) not in (int, Fraction) or type(theta) not in (int, Fraction)
            or not 2 <= u <= 3 or not 0 < theta <= 1):
        raise ValueError("require exact rational2<=u<=3 and0<theta<=1")
    u, theta = Fraction(u), Fraction(theta)
    t_low, t_high = log_enclosure(u-1, terms)
    s = theta*u
    positive_low = positive_high = Fraction(0)
    if s > 2:
        low, high = log_enclosure(s-1, terms)
        positive_low, positive_high = 4*u*low/s, 4*u*high/s
    return positive_low-(1+t_high)**2, positive_high-(1+t_low)**2


def factored_bound(target: int, survivors: bytearray,
                    composites: bytearray) -> tuple[int, int, int, int]:
    """Return (L,T,M,d) conditionally on truthful full cubic A,C inputs.

    Slot i is odd argument3+2i through N-3. Binary/subset validation does
    not establish primality or the sieve meaning of the supplied arrays.
    """
    if type(target) is not int or target < 6 or target % 2:
        raise ValueError("require an even target N>=6")
    if (not isinstance(survivors, bytearray) or not isinstance(composites, bytearray)
            or len(survivors) != (target-4)//2 or len(composites) != len(survivors)
            or any(a not in (0, 1) or c not in (0, 1) or c > a
                   for a, c in zip(survivors, composites))):
        raise ValueError("require full binary odd-slot arrays with C a subset of A")
    m = sum(a*b for a, b in zip(survivors, reversed(survivors)))
    t = sum((a-c)*b for a, c, b in zip(survivors, composites, reversed(survivors)))
    signed = sum((a-2*c)*b for a, c, b in zip(survivors, composites, reversed(survivors)))
    middle = target//2
    diagonal = composites[(middle-3)//2] if middle % 2 else 0
    return signed+diagonal, t, m, diagonal
