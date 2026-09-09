"""Prime-power stationary phase and an all-moduli balanced MODEL saving.

Owner: Kevin's Goldbach research. Purpose: remove the squarefree restriction
from the proved balanced smooth kernel, with a costed squarefull-part split.
This is a reusable proof and exact verifier, not publication packaging.
It does not transfer the original sieve weights or prove the signed prime
correlation. All previously useful polynomial components are preserved.

I. Pointwise complete sums, including every prime-power valuation.
For q>=2 and arbitrary integers h,l,t, put
  F_q(h,l;t)=sum_(x,y units modq)e_q(t/(x*y)+h*x+l*y).
Then
  |F_(p^n)(h,l;t)| <=6*p^n*gcd(p^n,h,l,t),
  |F_q(h,l;t)| <=6^omega(q)*q*gcd(q,h,l,t)
                 <<_epsilon q^(1+epsilon)*gcd(q,h,l,t).       (1)

Proof: let v=min(v_p(h),v_p(l),v_p(t),n). If v=n, the sum is exactly
phi(p^n)^2<=p^(2n), which proves the bound. This case must be handled
separately: the usual p^(2v) unit-lift identity does NOT extend to modulus1.
If v<n, write e=n-v>=1. Lifting units gives EXACTLY
  F_(p^n)(h,l;t)=p^(2v)*F_(p^e)(h/p^v,l/p^v;t/p^v).        (2)
The reduced triple has minimum valuation0. At e=1, the prime zero-pattern
formula(4) in squarefree_correlation_kernel.py and |Kl3(z;p)|<=3 on units
give |F_p|<=3p. This prime input was checked in KMS arXiv:1511.01636v5,
printed p2: https://arxiv.org/pdf/1511.01636v5 . No prime-power Kl3
theorem is imported from that prime-only source.

For e>=2, translations by p^(e-1) force the two stationary equations
  h=t/(x^2*y), l=t/(x*y^2) (modp).                         (3)
If a primitive reduced triple is not entirely units, these are impossible,
so its sum is0. For three units, stationary classes modulo p^r correspond
bijectively to z^3=t*h*l, with x=z/h,y=z/l. There are at most3 such z for
odd p, because the unit group is cyclic; at p=2 the cube map on the unit
2-group is bijective. These statements hold for every r>=1.

If e=2r, split x=x0+p^r*a,y=y0+p^r*b, with a,b modulo p^r. The exact
linear Taylor sum is0 unless (3) holds modulo p^r, when its mass is p^e.
Hence |F_(p^e)|<=3p^e (and <=p^e for p=2).

If e=2r+1>=3, first sum the lifts by p^(r+1). This enforces (3) modulo
p^r and contributes p^(2r). For each stationary base x0,y0 modulo p^r,
the remaining a,b modulo p give a two-dimensional quadratic Gauss sum.
Writing f=t/(xy)+hx+ly, the exact expansion modulo p^(2r+1) is
  f(x0+p^r*a,y0+p^r*b)
    =f0+p^r*(a*f_x+b*f_y)+p^(2r)*Q(a,b),
  Q=t/(x0*y0)*(a^2/x0^2+a*b/(x0*y0)+b^2/y0^2).           (4)
Terms of order3 vanish since3r>=2r+1. Stationarity makes f_x,f_y divisible
by p^r, so the remaining sum is e_p(Q+A*a+B*b), where A=f_x/p^r,
B=f_y/p^r modulo p. For odd p its Hessian determinant is
  3*t^2/(x0^4*y0^4)=3*h^2*l^2/z^2 (modp).
For p!=2,3 the quadratic form is nondegenerate, and completing squares
gives magnitude p. At p=3 it has rank1, giving magnitude at most p^(3/2):
one ordinary quadratic Gauss sum times either0 or p in the null direction.
There are at most3 stationary bases, so these bounds are3p^e and
3*sqrt(3)*p^e respectively. At p=2 use the reciprocal polynomial(4),
not division by2 in a Hessian: the trivial Gauss bound4 and unique base
give2p^e. Thus6p^e works in every case, and (2) proves the first bound.
CRT multiplies the local sums with unit scalings of h,l,t, preserving
all valuations. This proves (1), including zero and unequal valuations.

II. Arbitrary joint periods and a pointwise off-axis estimate.
For any integer J>=1 and |omega|<=1 periodic jointly modulo J, let L=qJ
and define F_L as in composite_linear_kernel.py. Expand
  c_ab=J^-2*sum_(r,s modJ)omega(r,s)*e_J(-a*r-b*s), |c_ab|<=1.
The EXACT lift identity, with no coprimality assumption on q,J, is
  F_L(h,l;t)=J^2*sum_(a,b modJ; J|h+qa,J|l+qb)
        c_ab*F_q((h+qa)/J,(l+qb)/J;t).                    (5)
Each common divisor of the two new frequencies,t,q divides h,l,t,q.
There are at most J^2 terms, hence
  |F_L(h,l;t)|<=6^omega(q)*q*J^4*gcd(q,h,l,t).             (6)

Set U=qJ/B,V=qJ/A. For Schwartz Fourier transforms, the nonzero integer
frequencies satisfy
  sum_(h,l!=0)|W1hat(h/U)W2hat(l/V)|*gcd(q,h,l,t)
      <<U*V*tau(q).                                      (7)
Indeed gcd(q,h,l,t)=sum_(d|q,h,l,t)phi(d), and each nonzero sum over
multiples of d is O(U/d), or O(V/d). The bound also holds when U/d<1:
rapid decay yields O((U/d)^2)<=O(U/d). Summing phi(d)/d^2<=1/d gives(7).
Double Poisson has prefactor Y/(q^3*J^2). Thus (6)--(7), summed over
k<=H*B*A*C/Y, bound the off-axis contribution of each q near C by
  <<Y^epsilon*H*J0^4*C.                                  (8)
No cancellation between moduli, no condition on m*k, and no prime-power
correlation theorem is required for this estimate.

III. Balanced smooth kernel over ALL integer moduli.
Let B=A=Y^(1/3), C=Y^(1/2), K=Y^(1/6), m an integer in[Y,2Y], and
1<=J0,H<=Y^(1/4096). For EVERY integer q in[C,2C], choose a unit r_q
modulo q, integer period J_q<=J0, and arbitrary complex |omega_(q,k)|<=1
periodic in both spatial variables modulo J_q. With fixed smooth W1,W2
supported in[1,2], set
  E_q=Y/(B*A*q)*sum_(1<=k<=H*K) sum_(M,a>=1; gcd(M*a,q)=1)
       W1(M/B)W2(a/A)*omega_(q,k)(M,a)*e_q(r_q*m*k/(M*a)).
For Z=Y^(1/128) and every epsilon>0,
  sum_(q in[C,2C])|E_q|
    <<Y^epsilon*H*(J0^8*Y^(23/24)*Z^(13/4)
                     +J0^4*Y*Z^-1/2+J0*Y^(2/3))
    <<Y^(4085/4096+epsilon).                              (9)
All prime powers, nonunit m*k and periods sharing factors with q occur.
The uniform coupled smooth-weight corollary from decorated_prime_kernel.py
also applies subject to its stated uniform spatial derivative bounds.

Proof: define the FULL squarefull part
  u(q)=product_(p^e exactly divides q; e>=2)p^e.
Then q=u*v with v squarefree and gcd(u,v)=1. Every squarefull integer
is uniquely a^2*b^3 with b squarefree (a,b need not be coprime). Therefore
their count up to X is at most sqrt(X)*sum_b b^-3/2=O(sqrt(X)), and a
dyadic sum gives sum_(u>Z squarefull)1/u=O(Z^-1/2). Consequently
  #{q in[C,2C]: u(q)>Z}<=sum_(u>Z squarefull)floor(2C/u)
                       <<C*Z^-1/2.                       (10)
Apply (8) to these moduli. Their off-axis total is the second term in(9).

For u<=Z, put s=u*gcd(v,rad(J)), Q=q/s, T=sJ. Then Q is squarefree,
gcd(Q,T)=1, s<=uJ and Q>=C/(ZJ), which tends to infinity here. The exact
CRT decomposition at qJ=QT has a Q-transform and a T-transform bounded
by T^2. Splitting the two h,l residue classes modulo T costs another T^2.
Within each residue pair the small transform is an arbitrary bounded
coefficient of k; no third split of k is needed. Changing unit variables
in the Q-transform gives F_Q(h,l;t*inverse(s^3*J^2)), so the positive h,l
ranges are unchanged. Signs are separated, and period residue restrictions
are absorbed in their respective bounded coefficients.

Now apply the reviewed trilinear lemma(6) of squarefree_correlation_kernel.py,
keeping l separate and grouping h*k. Its proof already pays every nonunit
mode; it does not require the remaining parameter to be a unit. Truncate
the nonzero frequencies at U=(qJ/B)*Y^rho,V=(qJ/A)*Y^rho for arbitrarily
small rho>0 and absorb Schwartz tails. Before its saving the per-q volume is
  Y/(q^3*J^2)*Q*T^4*U*V*H*K <<Y^epsilon*H*s^3*J^4*C.
The three factors are bounded respectively by
  s^(1/4)*Y^-1/8, Y^-1/12, Y^-1/24.
Their sum is O(s^(1/4)*Y^-1/24). Sum O(C) moduli and use
s^(13/4)*J^4<=Z^(13/4)*J0^(29/4)<=Z^(13/4)*J0^8.
This gives the first term in(9).

For the integer axes h=0,l=0 and their overlap use the already proved
one-variable Poisson and restricted Ramanujan bounds in
composite_linear_kernel.py. Each axis costs O(Y^epsilon*H*J0*B*A) after
the modulus gcd average. The overlap must separately be included when
subtracting it from the two full axes; its complete sum is bounded by
q*J^2*gcd(q,J)*tau(q)*gcd(q,m*k), giving the same aggregate estimate.
This is valid over all moduli at once; no squarefull density is needed.
The capped exponents of the three terms in(9) are exactly
  12115/12288, 4085/4096, 2/3+2/4096.
The second dominates and is strictly below1.

Reassessment: the proposed pointwise bound and density mechanism SUCCEED
in removing the squarefree restriction at this balanced MODEL box. This
does not establish a prime-power correlation theorem, further box coverage,
the full original sieve/weight transfer, or the missing signed prime-pair
estimate. Latest original-affine result remains2b8cf98. No actual zero,
effective onset, prime coverage, or worldwide originality is claimed.
Next question: which remaining boxes resist the combined model estimates?
In particular B=A=Y^(1/4),C=Y^(1/2),K=1 has no saving from the current
squarefree bilinear bound; a change of grouping or new arithmetic input
would need a quantitative test. The present theorem must not be extrapolated.

The routines below guard exact stationary/period identities, decomposition
and exponent arithmetic. Finite tests do not prove infinite source bounds.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import gcd

from composite_linear_kernel import _reduce, _periodic_parameters
from major_arc_kernel import _factorization, _mobius_phi


def _parameters(q, h, l, t):
    if type(q) is not int or q < 2:
        raise ValueError("modulus must be an integer at least2")
    if any(type(v) is not int for v in (h, l, t)):
        raise ValueError("frequencies and parameter must be integers")


def _prime_power(p, n):
    if (type(p) is not int or p < 2 or _factorization(p) != ((p, 1),)
            or type(n) is not int or n < 1):
        raise ValueError("require a prime and a positive integer exponent")
    return p**n


def _raw_transform(q, h, l, t):
    counts = [0]*q
    units = [x for x in range(1, q) if gcd(x, q) == 1]
    for x in units:
        for y in units:
            counts[(h*x+l*y+t*pow(x*y, -1, q)) % q] += 1
    return counts


def complete_exact(q, h, l, t):
    _parameters(q, h, l, t)
    return _reduce(_raw_transform(q, h, l, t), q)


def stationary_prediction(p, n, h, l, t):
    """Independent exact even/odd stationary expansion, requiring n>=2."""
    q = _prime_power(p, n)
    _parameters(q, h, l, t)
    if n < 2:
        raise ValueError("stationary expansion requires exponent at least2")
    r = n//2
    base = p**r
    counts = [0]*q
    for x in range(1, base):
        if x % p == 0:
            continue
        ix = pow(x, -1, q)
        for y in range(1, base):
            if y % p == 0:
                continue
            iy = pow(y, -1, q)
            gx, gy = (h-t*ix*ix*iy) % q, (l-t*ix*iy*iy) % q
            if gx % base or gy % base:
                continue
            phase = (t*ix*iy+h*x+l*y) % q
            if n % 2 == 0:
                counts[phase] += q
            else:
                linear_x, linear_y = gx//base, gy//base
                aa, ab, bb = t*ix**3*iy, t*ix**2*iy**2, t*ix*iy**3
                for a in range(p):
                    for b in range(p):
                        quadratic = aa*a*a+ab*a*b+bb*b*b+linear_x*a+linear_y*b
                        counts[(phase+base**2*quadratic) % q] += base**2
    return _reduce(counts, q)


def valuation_prediction(p, n, h, l, t):
    """Unit-lift identity, including the distinct all-zero reduced case."""
    q = _prime_power(p, n)
    _parameters(q, h, l, t)
    common = gcd(q, h, l, t)
    counts = [0]*q
    if common == q:
        counts[0] = _mobius_phi(q)[1]**2
    else:
        reduced = q//common
        raw = _raw_transform(reduced, h//common, l//common, t//common)
        for index, value in enumerate(raw):
            counts[common*index] += common**2*value
    return _reduce(counts, q)


def periodic_exact(q, period, t, h, l, weight):
    _periodic_parameters(q, period, t, h, l, weight)
    length = q*period
    counts = [0]*length
    units = [x for x in range(length) if gcd(x, q) == 1]
    for x in units:
        for y in units:
            phase = period*t*pow(x*y, -1, q)+h*x+l*y
            counts[phase % length] += weight[x % period][y % period]
    return _reduce(counts, length)


def periodic_lift_prediction(q, period, t, h, l, weight):
    """Expand the double DFT in (5); J^2 cancels its J^-2 normalization."""
    _periodic_parameters(q, period, t, h, l, weight)
    length = q*period
    counts = [0]*length
    for a in range(period):
        if (h+q*a) % period:
            continue
        for b in range(period):
            if (l+q*b) % period:
                continue
            raw = _raw_transform(q, (h+q*a)//period, (l+q*b)//period, t)
            for r in range(period):
                for s in range(period):
                    for index, value in enumerate(raw):
                        counts[(period*index-q*(a*r+b*s)) % length] += weight[r][s]*value
    return _reduce(counts, length)


def squarefull_parts(q):
    """Return (u,v,a,b) with q=u*v, u=a^2*b^3, b,v squarefree."""
    u = v = a = b = 1
    for p, exponent in _factorization(q):
        if exponent == 1:
            v *= p
        else:
            u *= p**exponent
            if exponent % 2:
                b *= p
                a *= p**((exponent-3)//2)
            else:
                a *= p**(exponent//2)
    return u, v, a, b


@dataclass(frozen=True)
class AllModuliBudget:
    small_part: F
    large_part: F
    axes: F
    total: F
    saving: F


def balanced_budget(period_exponent=0, frequency_exponent=0):
    if any(type(v) not in (int, F) for v in (period_exponent, frequency_exponent)):
        raise ValueError("exponents must be exact rational numbers")
    j, h = F(period_exponent), F(frequency_exponent)
    if any(not 0 <= v <= F(1, 4096) for v in (j, h)):
        raise ValueError("decoration exponents must lie in[0,1/4096]")
    small = F(23, 24)+F(13, 512)+8*j+h
    large = 1-F(1, 256)+4*j+h
    axes = F(2, 3)+j+h
    total = max(small, large, axes)
    return AllModuliBudget(small, large, axes, total, 1-total)
