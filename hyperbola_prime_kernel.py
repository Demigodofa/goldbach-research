"""All hyperbola boxes for the smooth decorated PRIME-CORE kernel.

Owner: Kevin's Goldbach research. Purpose: decide whether the remaining
box geometry is a genuine obstruction to the preserved completion method.
This is an unconditional exponential-sum estimate in the stated model.
It does NOT estimate the original signed prime correlation. General
composite cores and the complete arithmetic/sieve transfer remain OPEN.

Concrete question:
Can changing the completed-frequency grouping, supplemented by linear
Fourier completion, cover the full box family without losing the saving?
Yes. The earlier corner estimate and polynomial tools remain valid.

Sources: Kowalski--Michel--Sawin, arXiv:1511.01636v5, Theorem1.1 (1.2),
and the normalized complete-sum bound on p2, immediately before section1.2:
https://arxiv.org/pdf/1511.01636v5 . Prime modulus is essential here.
The CRT identity and smooth coupled-weight corollary are proved in
decorated_prime_kernel.py; no composite KMS theorem is assumed.

Theorem (full MODEL box family):
Let Y tend to infinity, m an integer in[Y,2Y], and put
  B=Y^b, A=Y^x, P=Y^y, K=B*A*P/Y,
  1/5<=b<=13/25, 0<=x<=(1-b)/2, 0<=y<=1/2.
Let 1<=S,J0,H<=Y^(1/4096). Sum over s<=S and primes p in[P,2P],
with c=s*p. For each pair choose a period J<=J0 and a unit r modulo c.
Let omega_(s,p,k)(M,a) be any complex function periodic in each argument
modulo J with absolute value<=1, allowed arbitrary joint and k dependence.
For fixed smooth W1,W2 supported in[1,2], set
  E=sum_(s,p) Y/(B*A*c) sum_(1<=k<=floor(H*K))
       sum_(M,a>=1; gcd(M*a,c)=1) W1(M/B)W2(a/A)
                *omega_(s,p,k)(M,a)*e_c(r*m*k*inverse(M*a)).
Uniformly in all these parameters, for every epsilon>0,
  |E| << Y^(127/128+epsilon)*S^4*J0^4*H
           +H*B*A*log(2S)+S*H*J0*(A+B)
       << Y^(4073/4096+epsilon).                              (1)
The proof bounds the sum of the absolute per-(s,p) contributions. It also
permits uniformly smooth coupled weights exactly as in the preceding
module's corollary. Uniform spatial derivative bounds remain hypotheses.
In particular, (1) makes no claim that the actual Poisson weights satisfy
them or that all original sieve indices fit within the remaining margin.

Linear-completion lemma, including its zero convention:
For p prime and p not dividing d, define on ALL residues
  K_d(z)=p^-1 sum_(u,v units modp) e_p(u+v+d*z/(u*v)).
For z!=0 this is normalized Kl3(d*z;p), and K_d(0)=1/p. Its finite
Fourier transform, with negative sign, is EXACTLY
  sum_(z modp) K_d(z)*e_p(-h*z)
     =0                       if h=0 modp,
     =S(1,d/h;p)              otherwise.                    (2)
Indeed the z sum enforces d/(u*v)=h. The latter is the ordinary
two-variable Kloosterman sum, of magnitude<=2*sqrt(p). If one instead
extends Kl3 by zero, EVERY Fourier coefficient in (2) loses1/p.

For p not dividing T, restricting a smooth sum to l=r0 modT gives
l=r0+T*j. If its l-scale is T*N with 1<=N<=p, the j-scale is N. The
Fourier transform of K_d(r0+T*j) has the same O(sqrt(p)) bound: T permutes
the frequencies and r0 adds unit phases. For any real additive twist,
Fourier inversion and summation by parts bound the smooth incomplete
sum by O(sqrt(p)*log(2p)). A Schwartz amplitude has the same bound up to
an arbitrarily small Y power after truncation/partition, when N<=p and
all scales are polynomial in Y. This is uniform in r0,T and the twist.
The progression must have smooth coefficients, not arbitrary bounded
ones. General residue weights are paid for by the residue splits below.

Proof of (1):
1. If H*K<1 the sum is empty. Otherwise b+x<=19/25 implies
   y>=6/25-1/4096. Consequently p>s*J and H*K<p eventually, uniformly
   throughout every nonempty box. Thus the preceding CRT identity applies
   at L=c*J=p*T, T=s*J, and k is a p-unit whenever p does not divide m.
   The double-Poisson prefactor is Y/(c^3*J^2). The small transform G_T
   is bounded by T^2 and depends on h,l only through their residues modT.
   For p not dividing h, the prime transform is p*K_d(l), where
     d=r*m*k*h*inverse(s^3*J^2) modp.
   This formula includes l=0 modp with the convention in (2): the single
   prime-axis value is1. No inverse modulo J is used.

2. Write U0=T*p/B and V0=T*p/A for the natural dual scales. For any
   fixed Schwartz function F and Z>0,
     sum_(n!=0)|F(n/Z)| << Z,
   with arbitrarily stronger powers of Z when Z<1. Nonzero h multiples
   of p have argument B*n/T, hence are negligible to any prescribed
   power since B/T>=Y^(1/5-2/4096). Treat h=0 separately. Its prime
   transform is 1-p*1_(p|l). Using
     sum_l |W2_hat(l/V0)| << 1+V0,
     sum_(p|l)|W2_hat(l/V0)| << 1+T/A
   gives after all (s,p) summation
     <<H*B*A*log(2S)+S*H*J0*B.
   Thus A<T, and multiple prime-axis frequencies in the l range, cause
   no omitted modes. The integer l=0, h!=0 contribution is at most
   S*H*J0*A by the nonzero Fourier L1 estimate above. If p|m, use the
   original sum: each such prime costs O(H*B*A/s). There are O(1) of
   them because every nonempty box has y>=6/25-1/4096. This costs the
   first exceptional term in (1). Every exception is below Y^(77/100).

3. For y<=49/100 use the normalized pointwise bound |K_d(l)|<=3
   off the integer axes (also valid at l=0 modp). The two nonzero
   Fourier L1 bounds give, per (s,p),
     Y/(c^3*J^2)*p*T^2*U0*V0*(H*K) << H*s*J^2*P.
   Summing gives H*S^2*J0^2*P^2<=Y^(49/50)*H*S^2*J0^2. This is
   smaller than the first term in (1), including all decoration costs.

4. It remains to handle 49/100<=y<=1/2. Fix arbitrarily small rho>0.
   If U0<Y^-rho, all h!=0 modes are arbitrarily power-small by Schwartz
   decay (choose enough derivatives). Otherwise truncate at
     |h|<=U0*Y^(2rho), |l|<=V0*Y^(2rho).
   Now the h upper length is>=1, including the thin strip U0<1.
   All resulting Y^(O(rho)) losses are absorbed in epsilon. This is
   important for uniformity when b is close to y+log_Y(T).

5. First suppose x>=1/16. Split the signs and the T^2 residue pairs of
   h,l. In each pair, G_T/T^2 is a bounded coefficient of k. Keep l as
   the single variable, and group w=k*|h|. Its coefficient is divisor-
   bounded; the l coefficient is smooth and bounded. Thus the L2 norms
   are at most sqrt(V) and sqrt(U*H*K)*Y^epsilon. NO k residue split
   is needed. The total conservative residue/small-transform cost is T^4.

   Ignoring arbitrarily small truncation powers, write a_s=log_Y(s),
   a_J=log_Y(J), a_H=log_Y(H). The two lengths have exponents
     v=y-x+a_s+a_J,
     w=x+2*y-1+a_s+a_J+a_H,
     v+w=3*y-1+2*a_s+2*a_J+a_H.
   Uniformly v>=9/100 and w>=17/400. Both lengths are below p:
   v<y follows from x>=1/16>2/4096, and
   w<=2/5+3/4096<49/100<=y. Their product is strictly between
   p^(1/4) and p^(5/4). Put the smaller length first in KMS Theorem1.1;
   its asymmetric length condition then holds automatically.

   The first saving is at least Y^(-17/800+O(rho)). The other saving is
     (V*U*H*K)^(-3/16)*p^(11/64)
       <<Y^(-(25*y-12)/64+O(rho))
   after discarding the helpful s,J,H powers. Restoring the prefactor
   and summing gives the baseline H*S^4*J0^4*P^2. Its bulk exponent
     2*y-(25*y-12)/64=(103*y+12)/64<=127/128.
   The first-saving exponent is also smaller than127/128. This proves
   the desired contribution for these boxes.

6. Suppose instead x<1/16. Split the same T^2 residue pairs and pay
   T^2 for G_T, which is constant in l within its residue for fixed k.
   For each h,k use (2) on the smooth l progression. Its j-scale is
     V0/T=p/A<=p,
   and is>=Y^(49/100-1/16). This condition uses A>=1; it does NOT
   require V0<=p. The progression form of the lemma therefore gives
   O(sqrt(p)*Y^epsilon), even when A<T. The h absolute sum is O(U0),
   and there are at most H*K frequencies. If integer l=0 was removed
   in step2, restoring/subtracting it costs at most1/p per h,k, harmless.
   Per (s,p) the bound is
     Y/(c^3*J^2)*p*T^4*U0*(H*K)*sqrt(p)
       << H*s^2*J^3*A*P/sqrt(p).
   Its total is H*S^3*J0^3*A*P^(3/2)*Y^epsilon
     <=Y^(13/16+epsilon)*H*S^3*J0^3,
   well below (1). This completes every box and the proof. Finally
   127/128+9/4096=4073/4096. No numerical prime experiment is needed.

What changed: the smooth decorated prime-core model now includes the
entire b range through13/25 and all the stated smaller divisor boxes.
The model's ORIGINAL arithmetic identification, arbitrary composite
cores, roughness/sieve costs and signed prime-correlation estimate remain
unproved. The latest original-affine estimate remains2b8cf98. The finite
checks below guard a new Fourier identity and exact exponent coverage;
they are not evidence of an exceptional zero or new Goldbach coverage.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


def _parameters(prime, multiplier, frequency):
    if (type(prime) is not int or prime < 2
            or any(prime % d == 0 for d in range(2, isqrt(prime)+1))):
        raise ValueError("modulus must be prime")
    if any(type(v) is not int for v in (multiplier, frequency)):
        raise ValueError("multiplier and frequency must be integers")
    if multiplier % prime == 0:
        raise ValueError("multiplier must be a prime-modulus unit")


def _cyclotomic(counts):
    return tuple(value-counts[-1] for value in counts[:-1])


def kl3_fourier_exact(prime, multiplier, frequency, *, zero_extension=False):
    """Compute p times the left side of (2), exactly in Z[zeta_p]."""
    _parameters(prime, multiplier, frequency)
    if type(zero_extension) is not bool:
        raise ValueError("zero_extension must be a boolean")
    counts = [0]*prime
    for z in range(1 if zero_extension else 0, prime):
        for u in range(1, prime):
            for v in range(1, prime):
                phase = (u+v+multiplier*z*pow(u*v, -1, prime)-frequency*z) % prime
                counts[phase] += 1
    return _cyclotomic(counts)


def kl2_fourier_prediction(prime, multiplier, frequency, *, zero_extension=False):
    """Independently compute p times the right side, including its zero."""
    _parameters(prime, multiplier, frequency)
    if type(zero_extension) is not bool:
        raise ValueError("zero_extension must be a boolean")
    counts = [0]*prime
    if frequency % prime:
        quotient = multiplier*pow(frequency, -1, prime) % prime
        for u in range(1, prime):
            counts[(u+quotient*pow(u, -1, prime)) % prime] += prime
    if zero_extension:
        counts[0] -= 1
    return _cyclotomic(counts)


@dataclass(frozen=True)
class BoxBudget:
    branch: str
    frequency: F
    dual_cofactor: F
    dual_divisor: F
    grouped_frequency: F
    source_product: F
    off_axis_exponent: F | None
    exception_exponent: F
    total_exponent: F
    uniform_ceiling: F


def box_budget(b, x, y, small_exponent=0, period_exponent=0, frequency_exponent=0):
    """Exact fixed-power bookkeeping, excluding arbitrary epsilon losses.

    A strictly negative dual-cofactor power is the Schwartz branch.
    The proof's rho split, not this pointwise branch label, owns uniformity
    across a Y-dependent strip adjoining zero. Negative frequency powers
    are empty for sufficiently large Y; the zero-power case is retained.
    """
    values = (b, x, y, small_exponent, period_exponent, frequency_exponent)
    if any(type(v) not in (int, F) for v in values):
        raise ValueError("exponents must be exact rational numbers")
    b, x, y, s, j, h = map(F, values)
    if not (F(1, 5) <= b <= F(13, 25) and 0 <= x <= (1-b)/2
            and 0 <= y <= F(1, 2)):
        raise ValueError("box lies outside the proved hyperbola family")
    if any(not 0 <= v <= F(1, 4096) for v in (s, j, h)):
        raise ValueError("decoration exponents must lie in[0,1/4096]")
    k = b+x+y-1+h
    u, v = y-b+s+j, y-x+s+j
    w = u+k
    product = v+w
    exception = max(h+b+x, s+h+j+max(b, x))
    ceiling = F(127, 128)+4*s+4*j+h
    if k < 0:
        branch, off, total = "empty", None, F(0)
    elif y <= F(49, 100):
        branch, off = "pointwise", 2*y+2*s+2*j+h
        total = max(off, exception)
    elif u < 0:
        branch, off, total = "schwartz", None, exception
    elif x < F(1, 16):
        branch, off = "linear", x+F(3, 2)*y+3*s+3*j+h
        total = max(off, exception)
    else:
        saving = min(min(v, w)/2, F(3, 16)*product-F(11, 64)*y)
        branch, off = "bilinear", 2*y+4*s+4*j+h-saving
        total = max(off, exception)
    return BoxBudget(branch, k, u, v, w, product, off, exception, total, ceiling)
