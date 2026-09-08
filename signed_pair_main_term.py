"""Signed-kernel pair main terms, including small exceptional conductors.

Owner: Kevin's research. Purpose: compare the main terms after the Fourier
and pointwise error bounds have been checked. Exact rational helpers verify
the periodic algebra; they do not compute actual prime counts.

Status, 2026-09-08: root-derived candidate awaiting fresh Sol review. The
existing reviewer handle reports pending_init following the interruption;
no review completion is inferred from the queued request. Six focused
finite-algebra tests passed normally and with Python -O. The analytic
arguments below must not be promoted as independently checked yet.

Theorem: let I=(Y/2,Y], J_m={n in Z:n,m-n in I}, K_m=|J_m|, and let
exp(log(Y)**(4/5))<=R<=Y**(1/400). Use the fixed smooth cutoff G of
major_arc_kernel.py, and put g(q)=G(log(q)/log(R)). Write
  Gamma(n)=sum_q mu(q)*c_q(n)/phi(q)*g(q).
Uniformly for even m in [5Y/4,7Y/4],
  (Gamma*1_I)*(Gamma*1_I)(m)=K_m*S_2(m)+O_G(Y*R**(-1/3)).       (1)
In particular this MODEL pair count is positive for all sufficiently large
Y, since K_m>=Y/4-O(1) and S_2(m) has an absolute positive lower bound.

Let chi be primitive quadratic of conductor D, 3<=D<=R**2, and put
  Xi(n)=chi(n)*D/phi(D)*Lambda_{R,D}(n),
  M_-(n)=1_I(n)*(Gamma(n)-v(n)*Xi(n)),
  M_+(n)=1_I(n)*(Gamma(n)+v(n)*Xi(n)),  v(n)=n**(beta-1),
where 0<=beta<1. Let A,B,C and P(u,w),S(u,w) be the finite character
moments and models in exceptional_character_model.py. If D<=R**(1/4), then
  M_-*M_-(m)=S_2(m)/A * sum_{n in J_m}P(v(n),v(m-n))
                               +O_G(Y*R**(-1/3)),             (2)
and the plus version replaces P by S. The constants are uniform in D,beta,m.
No assertion here identifies M_- with the actual prime weight.

Proof of the periodic algebra and truncation:
1. Write
   U0=sum_q mu(q)**2*c_q(m)/phi(q)**2*g(q)**2,
   UD=sum_{(q,D)=1} mu(q)**2*c_q(m)/phi(q)**2*g(D*q)**2.
   Complete-period means, with the second argument m-n, are exactly
     mean(Gamma*Gamma)=U0,
     mean(Gamma*Xi)=mean(Xi*Gamma)=D*B/phi(D)**2 * UD,
     mean(Xi*Xi)=D*C/phi(D)**2 * UD.                          (3)
   Ramanujan orthogonality gives
     mean_n c_q(n)*c_s(m-n)=1_{q=s}*c_q(m).
   The finite Fourier transform of a primitive character vanishes on
   nonprimitive additive frequencies: otherwise multiplication by a unit
   trivial on the corresponding quotient, but nontrivial under chi,
   contradicts primitivity. Therefore chi(n)*c_s(n), (s,D)=1, has only
   primitive frequencies of denominator Ds, by Chinese remaindering.
   The mixed mean can survive only when q=Ds. Its coefficient is zero
   unless D is squarefree. For such D, CRT and the identity
     mean_{n mod D} c_D(n)*chi(m-n)=chi(m)
   give the mixed coefficient D*mu(D)*chi(m)/phi(D)**2 times UD.
   This is D*B/phi(D)**2: for odd D, B=mu(D)*chi(m), and for the
   possible even conductors (with 2-part4 or8) both expressions vanish.
   Two Xi terms require the same cofactor s; their conductor mean is C/D.
   These arguments establish (3), including nonunit m and nonsquarefree D.

2. Each Gamma component has period q<=R**2 and amplitude O_G(1).
   Each Xi component has period Ds<=R**2 and amplitude O_G(D/phi(D)).
   The sums of the absolute component amplitudes are O_G(R**2) for
   each kernel, since there are at most R**2/D Xi components.
   A product of two components has period at most R**4. Subtracting
   its mean therefore leaves partial sums bounded by its amplitude times
   O(R**4). The weights 1,v(n),v(m-n),v(n)*v(m-n) on J_m have bounded
   supremum and total variation, uniformly in beta in [0,1]. Partial
   summation proves, with error O_G(R**8), the exact weighted main term
     U0*K_m +/- D*B/phi(D)**2*UD*sum_J(v(n)+v(m-n))
                  +D*C/phi(D)**2*UD*sum_J v(n)*v(m-n).       (4)
   Here the displayed sums are discrete; there is no integral-endpoint error.

3. For any Q>=1, the absolute Ramanujan tail obeys
     sum_{q>Q}mu(q)**2*|c_q(m)|/phi(q)**2
       <= Q**(-1/2)*product_p(1+sqrt(p)*|c_p(m)|/(p-1)**2)
       <= Q**(-1/2)*exp(O(sqrt(log(2Y)))).                   (5)
   The product at primes not dividing m converges absolutely. The other
   local factors are at most 1+O(p**(-1/2)). To bound their product,
   split prime divisors at L=log(2Y). Below L, even the sum over all
   integers of n**(-1/2) is O(sqrt L). Above L there are at most L/log L
   prime divisors, so their reciprocal-square-root sum is also O(sqrt L).
   This is a UNIFORM tail estimate; no exceptional set is used here.
   Since g(q)=1 for q<=R, (5) gives U0=S_2(m)+O_G(R**(-1/3)).
   Put S_out=sum_{(q,D)=1}mu(q)**2*c_q(m)/phi(q)**2. If D<=R**(1/4),
   then g(Dq)=1 for q<=R/D>=R**(3/4), so
     |UD-S_out| <<_G R**(-3/8)*exp(O(sqrt(log(2Y)))).
   Also D*(|B|+|C|)/phi(D)**2<=2D/phi(D)
   <=exp(O(sqrt(log(2Y)))). Since log R>=log(Y)**(4/5), these
   subexponential factors are absorbed into R**(1/24). Thus the weighted
   coefficient errors in (4) are O_G(R**(-1/3)).
   Local Euler factors give S_2(m)=(D*A/phi(D)**2)*S_out:
   for odd p|D the factor is p*(p-2)/(p-1)**2 if p does not divide m,
   and p/(p-1) if it does; the 2-part contributes 2 when present.
   This proves (1)-(2), since R**8<<Y*R**(-1/3).

Suppressed-margin consequence:
For every D>21 in (2), 0<=rho<=49/100, and t=(1-beta)*log(Y),
  M_-*M_-(m)-rho*M_+*M_+(m)
    >= (11/120)*S_2(m)*K_m*min(1,t)-O_G(Y*R**(-1/3)).       (6)
Indeed the existing finite lemma gives P-rho*S>=11*P/60. If B=0,
P>=A*(1-u*w). If B!=0, D is odd, (m,D)=1, A>=9 and |B|=|C|=1,
so P>=A-3>=2A/3. Consequently
  P>=A*min(2/3,1-u*w).
For u=v(n),w=v(m-n), Y>=4 gives u*w<=exp(-t). The elementary inequality
1-exp(-t)>=(1-exp(-1))*min(1,t), and 1-exp(-1)>1/2, prove (6).
The loss is linear in the exceptional-zero distance, not its square.

If beta is an exceptional zero of level R**4 and fixed quality kappa,
the previously checked source bounds give
  t<=kappa/(4*d),  1-beta >> 1/(sqrt(D)*log(D)**2), d=logR/logY.
For D<=R**(1/4), the latter implies min(1,t)>>R**(-1/7) for large Y.
Thus (6) is strictly positive for sufficiently large Y. The lower bound
on conductor from the same source ensures D>21 eventually. No numerical
onset is asserted. Source: Grimmelt--Teravainen arXiv:2508.16400v2,
Definition7.1 and equations(7.2)-(7.3), already checked for our Fourier model:
https://arxiv.org/html/2508.16400v2#S7.SS1

Robustness to the previously bounded pointwise errors:
Suppose |E_+|,|E_-|<=C*e*H_R(rad(n)) on I, zero elsewhere, with
e=t*exp(-c/d) as in the exceptional case and fixed C,c>0. The correlation
theorem in radical_majorant_correlation.py bounds the change in (6) by
O_C,G(e*(1+e)*d**(-2)*Y*S_2(m)). Since e=O(1),
  e*(1+e)*d**(-2)/min(1,t) <<_c d**(-3)*exp(-c/d).
For sufficiently small fixed d>0 this is arbitrarily small. Taking Y large
after fixing d, the perturbed signed-model comparison remains positive.
With no exceptional term, M_-=M_+=Gamma and (1-rho) times (1) supplies
the positive margin; the unexceptional pointwise error is handled similarly.

Large-conductor extension, R**(1/4)<D<=R**2:
Discard only targets satisfying gcd(D,m)>D*R**(-1/16). Their number in the
central range is at most
  sum_{d|D,d>D*R**(-1/16)}(2Y/d+1)
    <=tau(D)*(2Y*R**(1/16)/D+1) << Y*R**(-1/8).             (7)
For example the elementary divisor bound tau(D)<<D**(1/128), with
D<=R**2, gives tau(D)<=R**(1/32) eventually, and the last bound follows
from R<=Y**(1/400). This is an explicit divisibility family, not an assumed
random distribution. Off that family, the exact coefficients (3) are small:
|B|<=1, and the finite local character formulas give |C|<=2*gcd(D,m).
Indeed each odd local factor has size1 or p-1 according as p does not or
does divide m; the 2-part contributes at most phi(8)=4, at most twice
its common divisor with the even m. Thus
  D*|B|/phi(D)**2 <=R**(-1/4)*exp(O(sqrt(log(2Y)))),
  D*|C|/phi(D)**2 <=2R**(-1/16)*exp(O(sqrt(log(2Y)))).
The absolute Euler sum also gives |UD|<=exp(O(sqrt(log(2Y)))). Consequently
(4), valid for every D<=R**2, yields for each sign
  M_+/-*M_+/-(m)=K_m*S_2(m)+O_G(Y*R**(-1/32)).              (8)
Hence the signed comparison has an ordinary positive margin off (7).
Its pointwise perturbations are absorbed for small fixed d as above, using
e<=O(d**(-1)*exp(-c/d)). If the exceptional conductor exceeds R**2, the
existing Fourier model omits Xi altogether; use the principal main term
while retaining this exceptional error bound.

Unclosed steps: a checked Fourier transfer for the actual PRIME weight
with the same normalization/support, its remaining Fourier pair residual
relative to suppression, and conversion of the bulk weighted comparison
to canonical L. These results do not prove positivity of L, a power-saving
exceptional set for L, or any new Goldbach coverage.
"""
from fractions import Fraction
from math import gcd, isqrt, lcm

from exceptional_character_model import pair_moments
from major_arc_kernel import _mobius_phi, ramanujan


def pair_coefficients(target: int, samples: tuple[int | Fraction, ...],
                      conductor: int | None = None, *, two_sign: int = 1
                      ) -> tuple[Fraction, Fraction, Fraction]:
    """Exact U0, mixed coefficient, quadratic coefficient in (3).

    samples[k] supplies g(k); index0 is unused. These arbitrary rational
    samples do not certify a smooth cutoff or an asymptotic estimate.
    A supplied conductor must define the primitive real character accepted
    by pair_moments; None requests the principal kernel alone.
    """
    if type(target) is not int or target % 2:
        raise ValueError("target must be an even integer")
    if len(samples) < 2 or any(type(g) not in (int, Fraction) for g in samples):
        raise ValueError("samples must include index1 and contain exact rationals")
    if type(two_sign) is not int or two_sign not in (-1, 1):
        raise ValueError("two_sign must be integer -1 or 1")
    if conductor is None and two_sign != 1:
        raise ValueError("two_sign=-1 needs a conductor with an 8-component")
    if conductor is not None:
        _, b, c = pair_moments(conductor, target, two_sign=two_sign)
        _, phi_d = _mobius_phi(conductor)
    principal = Fraction(0)
    restricted = Fraction(0)
    for q in range(1, len(samples)):
        mu, phi = _mobius_phi(q)
        coefficient = Fraction(mu*mu*ramanujan(q, target), phi*phi)
        principal += coefficient*samples[q]**2
        if conductor is not None and gcd(q, conductor) == 1 and q*conductor < len(samples):
            restricted += coefficient*samples[q*conductor]**2
    if conductor is None:
        return principal, Fraction(0), Fraction(0)
    return (principal, Fraction(conductor*b, phi_d*phi_d)*restricted,
            Fraction(conductor*c, phi_d*phi_d)*restricted)


def gcd_exception_cover(conductor: int, first: int, last: int,
                        scale: int | Fraction) -> tuple[tuple[int, ...], int]:
    """Divisor cover of even m with gcd(D,m)>D/scale in [first,last].

    Returns selected divisors of D and the SUM of their even-multiple
    counts. That sum is an upper bound; overlapping targets are counted
    repeatedly. Any positive D is accepted, without a character claim.
    The analytic application takes scale=R**(1/16); this finite verifier
    accepts only an exact rational scale and does not round that root.
    """
    if any(type(n) is not int for n in (conductor, first, last)) or conductor < 1:
        raise ValueError("require integer D>=1 and integer band endpoints")
    if first < 2 or first % 2 or last % 2 or last < first:
        raise ValueError("require a nonempty even band with first>=2")
    if type(scale) not in (int, Fraction) or scale < 1:
        raise ValueError("scale must be an exact rational >=1")
    divisors = set()
    for d in range(1, isqrt(conductor)+1):
        if conductor % d == 0:
            divisors.update((d, conductor//d))
    selected = tuple(sorted(d for d in divisors if d*scale > conductor))
    count = sum(last//lcm(2, d)-(first-1)//lcm(2, d) for d in selected)
    return selected, count
