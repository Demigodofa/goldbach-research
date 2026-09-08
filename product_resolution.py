"""Finite-field product mixing and the direct integer-resolution boundary.

Owner: Kevin's research. Purpose: check applicability of the bounded-product
model before importing it into an actual Goldbach target. Sol reviewed the
two deductions and actual verifier on 2026-09-08. Five focused tests passed
normally and with Python -O.

Nonzero-target product theorem:
Let ell>=7 be prime, m=ell-1, and f1,f2:F_ell^*->[0,2] have unit-group
mean1. Let g be their normalized multiplicative convolution, extended by
g(0)=0. For every NONZERO t modulo ell set
  T_t=(1/m)*sum_{a in F_ell}g(a)*g(t-a).
Then
  |T_t-(ell-2)/(ell-1)| <= (2+sqrt(ell))/(ell-1),
  T_t >= (ell-4-sqrt(ell))/(ell-1)>0.                       (1)
No assertion of sharpness is made for this lower bound. The prime threshold
cannot simply be dropped: at ell=5, f1=f2=2 on {1,4} and0 elsewhere give
g=f1 and T_1=0. Target0 is excluded: at ell=7, twice the quadratic-residue
indicator has g=f1 and T_0=0. The previous inverse theorem treats that case.

Proof from the exact factor coupling:
Use normalized multiplicative Fourier coefficients, so
  g=sum_chi c_chi*chi, c_chi=hat f1(chi)*hat f2(chi), c_1=1.
Every character, including the principal one, is extended by0 at0.
By Parseval, E fi^2<=2 gives sum_{chi!=1}|hat fi(chi)|^2<=1. Hence
  A=sum_{chi!=1}|c_chi|<=1
by Cauchy--Schwarz. For t!=0, the additive character-pair sum is
(chi*psi)(t)*J(chi,psi). The principal-principal Jacobi sum is ell-2;
one-principal sums have modulus1; pairs of nonprincipal characters have
modulus sqrt(ell) unless their product is principal, when the modulus is1.
Thus the error from the constant term is <=2A+sqrt(ell)*A^2 before dividing
by m, proving (1). Positivity follows from ell-4>sqrt(ell) for ell>=7.
Primary source for exactly these Jacobi cases, read 2026-09-08: Keith Conrad,
Gauss and Jacobi sums on finite fields and Z/mZ, Corollary2.5 and Theorem2.6,
printed pp3-4:
https://kconrad.math.uconn.edu/blurbs/gradnumthy/Gauss-Jacobi-sums.pdf
This is a finite product-distribution theorem, not a prime-pair estimate.

Exact atomic density bound:
In a group of size m let F=m/k on a k-element support and0 off it, k>=1.
Its minimum MEAN L1 distance to any density v in[0,2] with mean1 is
  inf_v E|F-v|=2*max(0,1-2k/m).                            (2)
For k<=m/2, v puts at most mass2k/m on the support, leaving at least
1-2k/m missing there and the same excess off it. Equality is attained by
v=2 on the support and v=(m-2k)/(m-k) off it. For k>=m/2 take v=F.

Consequence for direct resolution of one integer target:
Suppose retained integers are <=H. A prime modulus ell>2H is SUFFICIENT
to make congruence identify an exact sum of two retained integers, since
all their sums are <ell. For z>=2 put B=floor(H/(z+1)). Any nonempty set
of k earlier cofactor primes<=B occupies k DISTINCT nonzero residues here.
Its uniform normalized residue density is F as above, with m=ell-1>=2H
and k<=B. Consequently F exceeds the cap2, and (2) is at least
  2z/(z+1)>=4/3.                                          (3)
Thus the direct unweighted prime-atom histogram at this sufficient
no-alias modulus cannot meet the cap2 contract, or even approximate a
mean1 cap2 density with small L1 error. This fails before any issue with
product cutoffs or unordered semiprime multiplicities is considered.

Scope:
At smaller moduli a positive residue-pair count can include several integer
sums congruent to the target; it does not automatically certify that target.
The choice ell>2H is NOT claimed necessary for every possible method. This
only excludes the straightforward single-modulus no-alias application with
uniform prime atoms. Joint moduli, smoothing with a separately proved
transfer, and certified exclusion of other congruent sums remain possible
questions. No actual prime coverage, Goldbach counterexample, general
impossibility theorem, or historical-novelty claim follows.
"""
from fractions import Fraction
from math import isqrt

from redistribution import trial_prime


def _prime_modulus(ell: int) -> None:
    if type(ell) is not int or ell < 3 or not trial_prime(ell):
        raise ValueError("require an odd prime modulus")


def field_product_pairs(first: tuple[int | Fraction, ...],
                        second: tuple[int | Fraction, ...]
                        ) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    """Return product weights and all additive pair means, indexed0..ell-1.

    Input slot i represents residue i+1, NOT a cyclic exponent. Each input
    has mean1 and values in[0,2]; ell=len(first)+1 must be an odd prime.
    The calculation certifies these finite weights, not actual prime counts.
    """
    if type(first) is not tuple or type(second) is not tuple or len(first) != len(second):
        raise ValueError("require equally sized tuples")
    ell = len(first)+1
    _prime_modulus(ell)
    m = ell-1
    for values in (first, second):
        if (any(type(v) not in (int, Fraction) or not 0 <= v <= 2 for v in values)
                or sum(values) != m):
            raise ValueError("require exact rational densities in[0,2] with mean1")
    weights = [Fraction(0)]*ell
    for a in range(1, ell):
        for b in range(1, ell):
            weights[a*b % ell] += Fraction(first[a-1]*second[b-1], m)
    pairs = tuple(sum((weights[a]*weights[(t-a) % ell] for a in range(ell)),
                      Fraction(0))/m for t in range(ell))
    return tuple(weights), pairs


def jacobi_pair_floor(ell: int, *, denominator: int = 16) -> Fraction:
    """Rational lower bound for NONZERO target means under the density premises.

    The square-root upper enclosure is exact. Small denominators may give
    a weaker nonpositive bound; that does not invalidate the real bound(1).
    No input distributions or actual Goldbach target are verified here.
    """
    _prime_modulus(ell)
    if type(denominator) is not int or denominator < 1:
        raise ValueError("require a positive integer denominator")
    # ell is prime, so ell*denominator^2 is not a square.
    sqrt_upper = Fraction(isqrt(ell*denominator*denominator)+1, denominator)
    return (ell-4-sqrt_upper)/(ell-1)


def atomic_cap_distance(group_size: int, occupied: int) -> Fraction:
    """Exact minimum mean-L1 distance from uniform atoms to a mean1 cap2 density.

    occupied counts DISTINCT occupied residues, each with the same mass.
    It is not the number of samples when several samples share a residue.
    """
    if (type(group_size) is not int or type(occupied) is not int
            or group_size < 1 or not 1 <= occupied <= group_size):
        raise ValueError("require integer1<=occupied<=group_size")
    return max(Fraction(0), 2-Fraction(4*occupied, group_size))
