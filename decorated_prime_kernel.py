"""A costed CRT transfer of the separate-factor kernel to small prime multiples.

Owner: Kevin's Goldbach research. Purpose: make the surviving kernel useful
with small modulus factors, periodic arithmetic weights and longer frequency
ranges, while preserving the remaining composite-modulus and sieve gaps.
This is an unconditional EXPONENTIAL-KERNEL theorem, not an original-affine
prime-pair estimate or a claimed solution of the signed correlation problem.

Concrete test:
Can CRT and the proved prime kernel absorb SMALL modulus/weight decorations
without consuming its entire power saving? Yes, with the explicit costs
below. It is essential to let the TOTAL modulus and frequency range grow;
fixing the total modulus at sqrt(Y) would miss the critical sieve boxes.

Analytic source: Kowalski--Michel--Sawin, arXiv:1511.01636v5, Theorem1.1,
equation(1.2), https://arxiv.org/pdf/1511.01636v5 . Its PRIME-modulus
estimate and all normalizations are recorded in separate_factor_prime_kernel.py.
We apply that theorem only to the prime factor p, not to the composite c.

Theorem:
Put P=Y^(1/2), B=Y^b, A=Y^((1-b)/2), K=Y^(b/2), where
  1/5<=b<=12/25, 1<=S,J0,H<=Y^(1/4096), m an integer in[Y,2Y].
Sum over integers 1<=s<=S and primes p in[P,2P]; set c=s*p. For each pair,
choose an integer period J=J_(s,p)<=J0 and a unit r_(s,p) modulo c.
For each 1<=k<=floor(H*K), let omega_(s,p,k)(M,a) be ANY complex function
periodic in each of M,a modulo J, bounded in absolute value by1. It may
couple the two residues and depend arbitrarily on k. Let W1,W2 be fixed
smooth functions of compact support in[1,2]. Define
  E = sum_(s<=S,p prime~P) Y/(B*A*c)
        *sum_(1<=k<=H*K) sum_(M,a>=1; gcd(M*a,c)=1)
           W1(M/B)W2(a/A) omega_(s,p,k)(M,a)
                          e_c(r_(s,p)*m*k*inverse(M*a)).
For every epsilon>0, uniformly over the stated parameters and weights,
  |E| <<_(epsilon,W1,W2) Y^(127/128+epsilon)*S^4*J0^4*H
                       + H*B*A*log(2S) + S*H*J0*(A+B)
       << Y^(4073/4096+epsilon).                         (1)
The proof bounds the sum of the per-(s,p) absolute values. This theorem
has no exceptional-zero hypothesis. It is a tool for the conditional
arithmetic problem, whose hypotheses remain in its own modules.

Proof:
1. Set T=s*J and L=c*J=p*T. Eventually p>s*J and H*K<p. Complete M,a
   with period L. This is a period even when gcd(s,J)>1. The prefactor
   Y/(B*A*c) becomes Y/(c^3*J^2). The complete Fourier transform is
     F_L(h,l;t)=sum_(x,y mod L; gcd(x*y,c)=1)
             omega(x,y)*e_c(t*inverse(x*y))*e_L(h*x+l*y),
   with t=r_(s,p)*m*k. CRT splits it EXACTLY into
     F_p(h*inverse(T), l*inverse(T); t*inverse(s))*G_T(h,l;t),          (2)
   where the prime F is the complete transform of the preceding module.
   Here
     G_T = sum_(x,y mod T; gcd(x*y,s)=1) omega(x,y)
              *e_s(t*inverse(p)*inverse(x*y))*e_T(inverse(p)*(h*x+l*y)).
   The inversions in the two factors use their respective moduli. For s=1,
   the e_s factor is1. No inverse modulo J and no unit restriction modulo
   J is needed. We have |G_T|<=T^2, and its dependence on h,l is only modulo T.

2. If p does not divide m and h*l!=0 mod p, the prime factor in(2) is
     p*Kl_3(r_(s,p)*m*k*h*l*inverse(s^3*J^2);p).          (3)
   Its multiplier is a unit, irrespective of whether t is a unit modulo s.
   Schwartz decay permits truncation to
     |h|<=U=(s*J*p/B)*Y^rho, |l|<=V=(s*J*p/A)*Y^rho,
   for an arbitrarily small fixed rho>0, with any desired negligible tail.
   For sufficiently small rho, U,V and V*H*K are all below p. Thus the only
   prime-axis frequencies inside the truncated box are the integer axes.

3. Split the signs and the T^2 residue pairs (h mod T,l mod T). In EACH
   pair, G_T/T^2 is an arbitrary bounded coefficient of k. Group w=k*|l|.
   The new coefficient at w is divisor-bounded; its L2 norm is at most
   (V*H*K)^(1/2)*Y^epsilon. The h coefficient has norm O(U^(1/2)).
   There is NO need to split k into residues, even if omega depends on k.
   The conservative residue/complete-small-factor cost is therefore T^4.

   Write W=V*H*K, L0=min(U,W), N0=max(U,W). Up to truncation powers,
     U*W=s^2*J^2*H*p^2/P,  B*A=P*K.
   Both supports are below p; in particular the largest base Y-exponent
   of W is12/25 and the added factor s*J*H is at most Y^(3/4096).
   Also p^(1/4)<U*W<p^(5/4), since s^2*J^2*H<=Y^(5/4096).
   Choosing L0 first makes L0<=N0*p^(1/4) automatic. Hence all KMS
   hypotheses hold, after sufficiently small rho/source-epsilon losses.
   Its two saving factors are L0^(-1/2) and
     (U*W)^(-3/16)*p^(11/64)
       <<Y^epsilon Y^(-1/128)*(s*J)^(-3/8)*H^(-3/16).
   The first is at least as strong as Y^(-1/100+epsilon), uniformly here.
   Discarding the helpful small-factor powers leaves Y^(-1/128+epsilon).
   Restoring the Poisson prefactor, prime-transform p, and T^4 gives
     Y/(c^3*J^2) * p * T^4 * (U*W)
       <<Y^epsilon P*s^3*J^4*H
   before that saving. There are O(P) primes per s and sum_(s<=S)s^3<<S^4.
   This proves the first term of(1). Bounding G_T separately is paid for;
   it is not an assumption that small modulus factors disappear.

4. The prime origin has value1-p and each single nonzero prime axis has
   value1, for p not dividing m. With |G_T|<=T^2, the origin costs
   O(H*K/s) per pair. The single axes and the Fourier L1 norms give
   O(H*K*J/A) and O(H*K*J/B) per pair. Summing p and s gives the last two
   terms of(1). If p|m, use the original sum instead: O(1) such primes
   exist, each costs O(H*B*A/s), yielding O(H*B*A*log(2S)). No unit
   formula is applied at a zero parameter. These terms are below Y^(3/4).
   Finally 127/128+9/4096=4073/4096. Arbitrarily small truncation losses
   are absorbed by epsilon. This proves the theorem.

Smooth coupled weights corollary:
W1(M/B)W2(a/A) may be replaced by a family F_(s,p,k)(M/B,a/A) supported
in a FIXED compact subset of(1,2)^2, with all partial derivatives bounded
uniformly in s,p,k,Y. No k derivatives are required. Extend it periodically
on a fixed larger rectangle and use its two-variable Fourier series, with
fixed smooth cutoffs in M/B,a/A. Coefficients decay faster than any fixed
power of the two Fourier indices, uniformly in k. Factor out a uniform
bound for each coefficient and absorb its normalized k dependence into
omega. The product-weight proof uses finitely many
derivatives and therefore grows only polynomially with these indices;
the series converges after choosing sufficiently many derivatives. Thus(1)
holds with constants depending on this derivative family. This handles
smooth coupling at the KERNEL level; it does not assert that the actual
Poisson weights have been proved to meet these uniform bounds.

Positive roughness relaxation: a separate preserved component.
In the actual-zero large-V regime of rare_affine_small_cofactor.py,
let U=K0*log eta, z=Y^(1/U)<Y^theta, and X<=Y^(13/25). For any
NONNEGATIVE cofactor majorant, relaxing original M to z-rough M is valid.
Its reciprocal mass satisfies
  sum_(M<=X; gcd(M,P(z))=1)1/M
    <= product_(z<=r<=X,prime)(1-1/r)^-1 << 1+log(X)/log(z) << U.     (4)
For retained gcd(M,Dm)=1, the existing four-orientation ZERO MODE still has
chi(a)chi(c)/(a*c)*K_(m,M)(D), with no chi(M) factor. The two rough
character harmonics remain applicable since sqrt(Y/M)>=Y^(6/25).
Summing that zero mode therefore costs only an additional U:
  << S2(m)*Y*U*t^2*(log eta)^8 + S2(m)*Y*U*eta^-20 = o(Y*t).
For these relaxed M, sum_(r prime, r|M)1/r<<U/z, so the corresponding harmonic
coprimality-removal terms remain negligible after fixed logarithm losses.
These statements concern the existing zero-mode expression, NOT an
unproved replacement of the entire prime sum by that expression.

A new upper beta sieve on M introduces an index e0 and M=e0*M0, giving
  e0*M0*e*a*d1*b == m (mod d2*c).
One must keep conductor/target/modulus coprimality and any fixed-divisor
cases. Completion changes the M0 dual length by e0: its apparent 1/e0
prefactor cancels against this longer dual range. A triangle over indices
costs their level/count, not the reciprocal mass in(4). Periodic weights
in(1) can represent INDIVIDUAL short divisibility/character restrictions;
the whole beta sieve is not one short-period function for free. Number of
indices, coefficient norms, periods, frequency inflation and tails must all
fit a remaining power margin. No complete costed sieve application is
promoted here. The composite core c may also have several large prime
factors, which(1) does not cover. Neither the full b range nor all hyperbola
boxes have been handled, and the original signed estimate remains OPEN.

Source-route reassessment, to avoid repeating unsupported substitutions:
Topacogullari, https://arxiv.org/pdf/1506.02608v1 , Theorem1.3 and section4,
treats d3(n)*d(N-n), but is untwisted. Drappeau--Topacogullari,
https://msp.org/ant/2019/13-10/ant-v13-n10-p05-s.pdf , Lemma4.5, p2407,
allows character weights but assumes |h|<=X^(1/4) and the second function
is the ordinary divisor function. Neither statement directly covers our
large additive target with both character-divisor factors. Their separate
features cannot be combined into an unstated theorem. Their methods remain
possible routes. The next required test is a genuinely general-composite
estimate for these factors, or a costed spectral adaptation to the character
weights. Preserve this CRT component and all polynomial tools meanwhile.

Finite verifiers below work exactly in the group algebra of roots of unity.
They test CRT including gcd(s,J)>1 and nonunits modulo J, not any infinite
analytic estimate, exceptional zero, or new Goldbach coverage.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import gcd, isqrt


def _parameters(prime, small, period, parameter, h, l, weight):
    if (type(prime) is not int or prime < 2
            or any(prime % d == 0 for d in range(2, isqrt(prime)+1))):
        raise ValueError("prime factor must be prime")
    if any(type(v) is not int or v < 1 for v in (small, period)):
        raise ValueError("small factor and period must be positive integers")
    if gcd(prime, small*period) != 1:
        raise ValueError("prime factor must be coprime to small factor times period")
    if any(type(v) is not int for v in (parameter, h, l)):
        raise ValueError("parameter and frequencies must be integers")
    if (len(weight) != period or any(len(row) != period for row in weight)
            or any(type(v) is not int for row in weight for v in row)):
        raise ValueError("weight must be a period by period integer matrix")


def periodic_transform_histogram(prime, small, period, parameter, h, l, weight):
    """Exact direct complete transform in Z[X]/(X^(cJ)-1).

    Integer matrix weights may exceed1 for this algebraic verifier; that
    does not meet the analytic theorem's bounded-weight hypothesis.
    """
    _parameters(prime, small, period, parameter, h, l, weight)
    c, length = prime*small, prime*small*period
    result = [0]*length
    for x in range(length):
        if gcd(x, c) != 1:
            continue
        for y in range(length):
            if gcd(y, c) == 1:
                phase = (period*parameter*pow(x*y, -1, c)+h*x+l*y) % length
                result[phase] += weight[x % period][y % period]
    return tuple(result)


def crt_transform_histogram(prime, small, period, parameter, h, l, weight):
    """Independently compute the prime and small-period factors in(2)."""
    _parameters(prime, small, period, parameter, h, l, weight)
    p, s, j = prime, small, period
    t = s*j
    prime_counts, small_counts = [0]*p, [0]*t
    inv_s, inv_t = pow(s, -1, p), pow(t, -1, p)
    for x in range(1, p):
        for y in range(1, p):
            phase = (parameter*inv_s*pow(x*y, -1, p)+inv_t*(h*x+l*y)) % p
            prime_counts[phase] += 1
    inv_p = pow(p, -1, t) if t > 1 else 0
    for x in range(t):
        if gcd(x, s) != 1:
            continue
        for y in range(t):
            if gcd(y, s) != 1:
                continue
            inverse_phase = (j*parameter*pow(p, -1, s)*pow(x*y, -1, s)
                             if s > 1 else 0)
            phase = (inverse_phase+inv_p*(h*x+l*y)) % t
            small_counts[phase] += weight[x % j][y % j]
    result = [0]*(p*t)
    for i, left in enumerate(prime_counts):
        for n, right in enumerate(small_counts):
            result[(t*i+p*n) % (p*t)] += left*right
    return tuple(result)


@dataclass(frozen=True)
class DecorationBudget:
    dual_cofactor: F
    dual_divisor: F
    grouped_frequency: F
    source_product: F
    short_saving: F
    bulk_saving: F
    conservative_exponent: F
    origin_and_bad_primes: F
    single_axes: F
    remaining_triangle_margin: F


def decoration_budget(b, small_exponent=0, period_exponent=0, frequency_exponent=0):
    """Exact Y-power budget for the theorem, before arbitrary epsilon losses."""
    values = (b, small_exponent, period_exponent, frequency_exponent)
    if any(type(v) not in (int, F) for v in values):
        raise ValueError("exponents must be exact rationals")
    b, s, j, h = map(F, values)
    if not F(1, 5) <= b <= F(12, 25):
        raise ValueError("cofactor exponent is outside the proved range")
    if any(not 0 <= v <= F(1, 4096) for v in (s, j, h)):
        raise ValueError("decoration exponents must be in[0,1/4096]")
    u, v, w = F(1, 2)-b+s+j, b/2+s+j, b+s+j+h
    product = u+w
    short, bulk = min(u, w)/2, F(3, 16)*product-F(11, 128)
    exponent = F(127, 128)+4*s+4*j+h
    return DecorationBudget(u, v, w, product, short, bulk, exponent,
                            h+(1+b)/2, s+h+j+max(b, (1-b)/2), 1-exponent)
