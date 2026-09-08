"""An exact product-coupled finite model and a quadratic-coset stability bound.

Owner: Kevin's research. Purpose: test whether multiplicative cofactor
coupling by itself fixes the signed prime-minus-semiprime pair comparison.
Sol checked the argument and actual implementation on 2026-09-08. Four
focused tests passed normally and with Python -O, including 510 exhaustive
small cyclic subsets and independent multiplication in prime residue fields.

Model and normalization:
Let m>=2 be even, H=Z/mZ, h=m/2. Pick exactly one member of every pair
{x,x+h}, forming S. Put f=2*1_S and
  g(x)=E_y f(y)*f(x-y), E_y=(1/m)*sum_{y in H}.              (1)
Both weights have mean1 and lie in[0,2]. Moreover
  f(x+h)=2-f(x), g(x+h)=2-g(x).
Define P0=E_x f(x)*f(x+h)=0 and T0=E_x g(x)*g(x+h).
For m=ell-1 with ell an odd prime, identify x with a primitive root to
the power x modulo ell. Then h is multiplication by-1, (1) is the EXACT
distribution of products of two factors with the same normalized weight f,
and P0,T0 are normalized additive pair correlations at target0 modulo ell.
This is cyclic convolution in exponent coordinates, NOT additive integer
convolution of prime flags. Product factors are ordered and include repeats.

The finite theorem:
* If4|m, T0>=1/2. The constant is sharp at m=4,S={0,1}.
* Ifm=2 mod4, put a=E_x f(x)*(-1)**x and y=a*a. Then
    T0 >= (1-y)*(1+3*y)/2 >= delta,
  where delta=(1-|a|)/2 is |S symmetric_difference Q|/m for the closer
  of the two parity cosets Q. In particular T0=0 exactly when S is one
  of those cosets. For prime ell=3 mod4 these are the quadratic-residue
  and nonresidue cosets; multiplication by-1 exchanges them.

Proof:
Use hat f(k)=E_x f(x)*exp(-2*pi*i*k*x/m). Character orthogonality
E_x exp(2*pi*i*j*x/m)=1_{m|j} gives inversion, Parseval, and
hat g(k)=hat f(k)**2 by finite sum expansion. This is the probability
counting normalization in Tao, 245C Notes2, Theorem21 and the cyclic-group
discussion (read 2026-09-08):
https://terrytao.wordpress.com/2009/04/06/the-fourier-transform/
From f(x+h)=2-f(x), every nonprincipal even Fourier mode vanishes.
Since Ef^2=2 and hat f(0)=1, sum_{k odd}|hat f(k)|^2=1. Thus
  T0=sum_k (-1)**k*|hat g(k)|^2
    =1-sum_{k odd}|hat f(k)|^4.                             (2)
Reality gives equal squared mass at k and m-k. If4|m, all odd modes
occur in DISTINCT pairs. With mass w_j in pair j, the fourth-power sum
is (1/2)*sum_j w_j^2 <=(1/2)*(sum_j w_j)^2=1/2.
Ifm=2 mod4, k=m/2 is the unique odd self-conjugate mode, with mass y.
The remaining paired mass is1-y, so the fourth-power sum is at most
y^2+(1-y)^2/2. This proves the stated bound. It is zero only when y=1;
|a|=1 forces S into one parity coset, and its half-size makes it equal
to that coset. Conversely the Fourier formula gives T0=0 for a coset.
Finally delta=(1-|a|)/2 by counting the intersection with the better
coset, and (1-y)*(1+3*y)/2 >=(1-y)/2 >=(1-|a|)/2.

Exact examples:
m=4,S={0,1}: g=(1,2,1,0), P0=0,T0=1/2.
m=6,S={0,1,2}: g=(2/3,4/3,2,4/3,2/3,0), a=1/3,
T0=16/27, attaining the quadratic stability lower bound.
For any rho>0 the signed model margin P0-rho*T0 is therefore <=-rho/2
when4|m, and strictly negative outside the parity cosets whenm=2 mod4.
In the coset case it is zero, not a positive certificate.

Scope and consequence:
This enforces a shared multiplicative factor distribution, unlike assigning
the second weight independently. Bounded density plus THIS exact product
coupling alone still cannot force the signed additive margin to be positive.
It does not model the full integer factor ranges, unique semiprime counting,
size-dependent weights, cubic survivor partition, or a truthful earlier
prime prefix. It also does not satisfy the actual prime character estimates
used in our analytic transfer. These are artificial residue weights, not
prime flags, an actual negative L, or a Goldbach counterexample. The result
does not rule out stronger arithmetic coupling or estimates for actual
primes. It isolates the exceptional role of the single odd quadratic mode;
it supplies no claim of historical novelty or new actual prime coverage.
"""
from fractions import Fraction


def skew_product_profile(flags: tuple[int, ...]) -> tuple[tuple[Fraction, ...], Fraction]:
    """Return (normalized product weights, reflected product-pair mean).

    Input is a cyclic exponent-coordinate subset choosing exactly one of
    each opposite pair. These are artificial residue flags, not prime flags.
    The exact O(m^2) verifier is intended for small finite groups.
    """
    if (type(flags) is not tuple or len(flags) < 2 or len(flags) % 2
            or any(type(v) is not int or v not in (0, 1) for v in flags)):
        raise ValueError("require an even-length tuple of exact binary integers")
    m, h = len(flags), len(flags)//2
    if any(flags[x]+flags[x+h] != 1 for x in range(h)):
        raise ValueError("choose exactly one member of each opposite pair")
    chosen = [x for x, flag in enumerate(flags) if flag]
    counts = [0]*m
    for a in chosen:
        for b in chosen:
            counts[(a+b) % m] += 1
    product = tuple(Fraction(4*count, m) for count in counts)
    pair_mean = sum((product[x]*product[(x+h) % m] for x in range(m)), Fraction(0))/m
    return product, pair_mean
