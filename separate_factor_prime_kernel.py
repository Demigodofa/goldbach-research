"""A power-saving smooth prime-modulus kernel from separate cofactor completion.

Owner: Kevin's Goldbach research. Purpose: preserve the first successful
quantitative component of the separate-M,a route, with its transfer gaps.
This is an EXPONENTIAL-SUM theorem, NOT a new estimate for the original
prime pairs, a Goldbach lower bound, or a novelty claim.

Concrete question and result:
Does retaining M,a separately expose cancellation discarded by grouping
r=M*a before completion? Yes for the smooth PRIME-MODULUS model below.
Pointwise complete-sum bounds alone reach Y; a bilinear estimate applied
AFTER completion saves Y^(1/128). Actual arithmetic transfer remains OPEN.

Primary source: Kowalski--Michel--Sawin, Bilinear forms with Kloosterman
sums and applications, arXiv:1511.01636v5, Theorem1.1, equation(1.2), p2:
https://arxiv.org/pdf/1511.01636v5 . Checked2026-09-09. Their normalized
Kl_3(s;p)=p^-1 sum_(xyz=s mod p)e_p(x+y+z). For PRIME p, unit multiplier c,
L<=N*p^(1/4), p^(1/4)<L*N<p^(5/4), and the stated interval supports,
  |sum alpha_l beta_n Kl_3(c*l*n;p)|
    <<_epsilon p^epsilon ||alpha||2 ||beta||2 sqrt(L*N)
           *[L^(-1/2)+(L*N)^(-3/16)*p^(11/64)].        (1)
The source's section1.5.2 does not supply a composite-modulus version.

Restricted kernel theorem (unconditional):
Let Y tend to infinity, m an integer in[Y,2Y], and
  1/5<=b<=12/25, P=Y^(1/2), B=Y^b,
  A=Y^((1-b)/2), K=Y^(b/2).
Let W1,W2 be fixed smooth functions of compact support in[1,2]. For EACH
prime p in[P,2P], let |nu_(p,k)|<=1 for 1<=k<=floor(K). Define
  E = sum_(p prime in[P,2P]) Y/(B*A*p)
        *sum_(1<=k<=K) nu_(p,k)
        *sum_(M,a>=1; gcd(M*a,p)=1) W1(M/B) W2(a/A)
                                  e_p(m*k*inverse(M*a)).
For every epsilon>0, uniformly over b,m and these coefficients,
  |E| <<_(epsilon,W1,W2) Y^(127/128+epsilon).           (2)
The proof even bounds the sum of the absolute values of the per-p terms.
The oscillatory modulus p here is a small divisor's MODEL replacement;
it is not either original prime in the affine pair p_original=m-M*q.

Proof, including the modes that cannot use(1):
1. Write e_p(x)=exp(2*pi*i*x/p). The complete double Fourier transform is
   F_p(h,l;t)=sum_(x,y units mod p)e_p(t*inverse(x*y)+h*x+l*y).
   For t!=0 mod p, EXACTLY
     F_p(h,l;t)=p*Kl_3(t*h*l;p)       if h*l!=0 mod p,
     F_p(0,l;t)=F_p(h,0;t)=1        on either single nonzero axis,
     F_p(0,0;t)=1-p.                                      (3)
   For the first identity put X=h*x,Y=l*y,Z=t/(x*y). The other two
   follow by summing a nontrivial additive character over the units.
   For t=0, instead F_p(h,l;0)=c_p(h)*c_p(l), where c_p(0)=p-1 and
   c_p(h)=-1 for h!=0. Thus using(3) at t=0 would be incorrect.

2. Use Fourier convention W_hat(s)=integral W(x)e(-s*x)dx. Twice applying
   Poisson to the residue classes of M,a gives
     sum_(M,a) W1(M/B)W2(a/A)e_p(t/(M*a))
       = B*A/p^2 sum_(h,l in Z) W1_hat(B*h/p)W2_hat(A*l/p)F_p(h,l;t).
   The full outside normalization is therefore Y/p^3. For p not dividing m,
   k<p eventually, so t=m*k is a unit. Smoothness permits truncation to
     |h|<=U=(p/B)*p^rho, |l|<=V=(p/A)*p^rho              (4)
   for arbitrarily small fixed rho>0, with any desired power-saving tail.
   Indeed F_p is bounded trivially by p^2, and both Fourier transforms
   have arbitrary polynomial decay. Constants depend on finitely many
   derivatives. Choose rho small enough for U,V and V*K to be below p.
   Both h,l in(4) then represent nonzero residues unless they are zero.

3. On the off-axis part, split the signs of h,l and group w=k*|l|.
   Coefficients separate by assumption: alpha_h=W1_hat(B*h/p), and
     gamma_w=sum_(k*|l|=w) nu_(p,k)W2_hat(A*l/p).
   Thus |alpha_h|<<1, |gamma_w|<<tau(w), and their L2 norms are at most
   U^(1/2)*O(1) and (V*K)^(1/2)*p^o(1), respectively. The four sign
   choices simply change the fixed unit multiplier in Kl_3.
   Set L0=min(U,V*K), N0=max(U,V*K). Rounded endpoints and fixed factors
   are harmless; supports may be padded by zero. Since B*A=P*K,
     U*V*K = (p^2/P)*p^(2rho) = p^(1+2rho)*O(1).
   Uniformly over the stated b range, both uninflated lengths have fixed
   positive powers of p and are below p. Hence for sufficiently small rho,
   L0<=N0*p^(1/4), p^(1/4)<L0*N0<p^(5/4), N0<p. All hypotheses of(1)
   hold. The resulting off-axis sum of NORMALIZED Kl_3 is
     << U*V*K*p^o(1)*[L0^(-1/2)+p^(-1/64+O(rho))].
   The uninflated powers of Y in L0,N0 are min(1/2-b,b), max(1/2-b,b).
   Half the smaller is >=1/100 on[1/5,12/25], greater than1/128.
   Restoring the factor Y/p^2 from(3) and summing at most O(P) primes
   proves Y^(1-1/128+epsilon), on taking rho and source epsilon small.
   This uses cancellation between h and w=k*l; applying a pointwise
   O(1) bound to normalized Kl_3 gives only Y^(1+o(1)).

4. The origin in(3) contributes in absolute value at most
     sum_(p~P) Y*K/p^2 << P*K = B*A.
   The two single axes cost at most A and B, respectively, up to constants
   or arbitrarily small truncation powers. This follows from the Fourier
   L1 bounds sum_h |W1_hat(B*h/p)|<<p/B and its A analogue.
   If p|m, do NOT apply(3): there are O(1) such primes in[P,2P], since
   m<=2Y. The original sum for each has absolute value O(B*A*K), which
   its prefactor turns into O(Y*K/p)=O(B*A). Every exceptional-mode term
   is O(Y^(37/50+epsilon)), strictly smaller than(2). This proves(2).

What this supplies, and what it does not:
The two-variable completion creates a third-order Kloosterman sum, and
keeping the original frequency k until the next bilinear step supplies
the missing length. That is a specific cancellation mechanism with an
actual analytic bound in this restricted model, not only a formal identity.
It preserves the failed generic Bettin--Chandee test's useful normalization.

The ORIGINAL modulus d2*c need not be prime. The coefficients of M,a
include roughness/sieve and character restrictions, and the real Poisson
weight couples variables. No costed smooth separation or sieve relaxation
has been proved here. No claim is made for all hyperbola boxes, b outside
the displayed range, or the missing signed prime correlation. Removing
roughness entirely can lose a logarithm in sum(1/M); it is not a free step.
The exceptional-zero hypotheses and all prior polynomial components remain
as in their owning modules. The latest original-affine estimate is still
rare_affine_small_cofactor.py, not(2).

Next concrete transfer question: can a source for composite-modulus
third-divisor/Kloosterman distribution handle these smooth triple factors,
then the actual small sieve indices and conductor, within the saving?
This must be tested against explicit moduli and coefficient hypotheses.

The finite routines below verify(3) EXACTLY in Z[zeta_p], and preserve
the exponent budget. Their tests do not prove(1), smooth Poisson, or an
infinite prime-pair assertion. The proof above and its source own those.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


def _prime(value):
    if (type(value) is not int or value < 2
            or any(value % d == 0 for d in range(2, isqrt(value)+1))):
        raise ValueError("modulus must be prime")


def _integer(value, name):
    if type(value) is not int:
        raise ValueError(f"{name} must be an integer")


def _cyclotomic(counts):
    """Canonical degree<p-1 representative modulo 1+X+...+X^(p-1)."""
    return tuple(n-counts[-1] for n in counts[:-1])


def complete_transform(modulus, parameter, first_frequency, second_frequency):
    """Exact F_p(h,l;t), as coefficients in the prime cyclotomic field."""
    _prime(modulus)
    for value, name in ((parameter, "parameter"),
                        (first_frequency, "first_frequency"),
                        (second_frequency, "second_frequency")):
        _integer(value, name)
    p = modulus
    counts = [0]*p
    for x in range(1, p):
        for y in range(1, p):
            phase = (parameter*pow(x*y, -1, p)
                     + first_frequency*x + second_frequency*y) % p
            counts[phase] += 1
    return _cyclotomic(counts)


def raw_kl3(modulus, parameter):
    """Exact UNNORMALIZED p*Kl_3(parameter;p), for a unit parameter."""
    _prime(modulus)
    _integer(parameter, "parameter")
    p = modulus
    if parameter % p == 0:
        raise ValueError("Kl3 parameter must be a modulus unit")
    counts = [0]*p
    for x in range(1, p):
        for y in range(1, p):
            z = parameter*pow(x*y, -1, p) % p
            counts[(x+y+z) % p] += 1
    return _cyclotomic(counts)


@dataclass(frozen=True)
class SeparateFactorBudget:
    dual_cofactor: F
    dual_divisor: F
    original_frequency: F
    grouped_frequency: F
    dual_product: F
    short_variable_saving: F
    source_bulk_saving: F
    saving: F
    aggregate_exponent: F
    origin_and_bad_moduli: F
    pointwise_exponent: F


def separate_factor_budget(cofactor_exponent):
    """Exact critical-box diagnostic; analytic theorem above uses[1/5,12/25]."""
    if type(cofactor_exponent) not in (int, F):
        raise ValueError("cofactor exponent must be an exact rational")
    b = F(cofactor_exponent)
    if not 0 <= b <= F(1, 2):
        raise ValueError("diagnostic range is[0,1/2]")
    u, v, k = F(1, 2)-b, b/2, b/2
    short_saving = min(u, v+k)/2
    source_saving = F(1, 128)
    saving = min(short_saving, source_saving)
    return SeparateFactorBudget(u, v, k, v+k, u+v+k,
                                short_saving, source_saving, saving,
                                1-saving, (1+b)/2, F(1))
