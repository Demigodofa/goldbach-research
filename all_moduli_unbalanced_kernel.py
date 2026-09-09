"""Repeated factors inside divisor shifts: an all-integer unbalanced MODEL.

Owner: Kevin's Goldbach research. Purpose: preserve a prime-square
correlation component and test a cheaper route around the failed
squarefull-residue split. This is a proof/verifier, not a manuscript.
All polynomial identities remain available. The signed prime correlation
and transfer of the original sieve weights remain OPEN.

I. A retained prime-square four-factor theorem.
Write K_q(z)=q^-1 sum_(u,v unitsq)e_q(u+v+z/(uv)). The stationary formula
in all_moduli_balanced_kernel.py implies, for p>=5,
  K_(p^2)(z)=sum_(w^3=z modp^2) e_(p^2)(3w),               (1)
where w ranges over units; the sum vanishes for p|z. Indeed the two
stationary variables are equal modulo p; each stationary class contributes
one phase after division by p^2, and its unique Hensel lift has phase3w.

For q=p^2 put
 C=sum_x K_q(u(x+a))*conj(K_q(v(x+a)))*conj(K_q(ux))*K_q(vx)*e_q(hx).
If p|uv, C=0. If u,v are units and p does not divide a(u-v), then
  |C|<=108*p, uniformly in every h.                         (2)
Always |C|<=108*p*gcd(p,a(u-v)) for unit u,v. This explicitly includes
nonunit h; it does not discard the exceptional congruences.

Proof: if v/u has no cube root modulo p^2 then C=0. Otherwise choose
lambda^3=mu^3=v/u, at most nine ordered pairs. Every four-root tuple is
uniquely (Y,lambda*Y,X,mu*X), with unit X,Y and
  Y^3-X^3=b=u*a, A=1-lambda, B=1-mu, c=h/u,
  Phi=3*(A*Y-B*X)+c*X^3.
Above each solution modulo p there are p lifts. Summing the tangent
parameter cancels unless
  G=A*X^2-B*Y^2+c*X^2*Y^2=0 modp.                         (3)
A stationary base contributes exactly p*e_q(Phi at any lift).
Under the generic hypotheses A,B,b are units. Equation(3) implies
B-cX^2!=0. Eliminate Y to get
  P(X)=(B-cX^2)^3*(X^3+b)^2-A^3*X^6=0 modp.              (4)
This polynomial has degree at most12 and nonzero constant B^3*b^2.
Each root X gives at most one Y, namely
  Y=(X^3+b)*(B-cX^2)/(A*X^2).
Conversely (4) gives both Y^2=A*X^2/(B-cX^2) and Y^3=X^3+b;
its roots cannot have X=0, B-cX^2=0 or X^3+b=0. Thus there are at most
12 stationary bases per branch, proving(2). The exceptional bound follows
from |K|<=3 and |C|<=81*p^2. For p=113, u=v=1,a=1,h=0 gives p(p-2),
and a=0,u=1,v=2,h=0 gives p(p-1), both larger than108p. These witnesses
use the unique unit cube root for p=2 mod3. Neither exception is cosmetic.
This prime-square component is NOT required by the next theorem.

II. The preserved factor may contain arbitrary prime powers.
In squarefree_unbalanced_kernel.py equation(3), only the complementary
factor s needs to be squarefree. The same estimate holds for ANY r,
q=r*s, gcd(r,s)=1, 4r<=X<=s:
 |sum alpha_m beta_n Z_q(cmn)| <<q^epsilon ||alpha||2||beta||2
   *(X^(3/4)r^(1/4)+X^(3/4)s^(1/8)+X^(1/4)s^(1/4)),      (5)
where c is a unit and Z_q=1_(gcd(z,q)=1)K_q. The first coefficient is
supported in[1,X]; the second may occupy ANY interval of length<=X.
The r-factor in the proof is used only for periodicity and the bound
|Z_r|<=6^omega(r), supplied by the retained all-prime-power pointwise
theorem. All four-factor estimates and signed residue graphs occur on
the squarefree s factor. Moving the second interval changes no energy,
intersection-length, or completion estimate in that proof.

Define U(q)=product_(p^e exactly divides q,e>=2)p^e, the FULL squarefull
part. If U(q)<=q^(2/5), then for sqrt(q)<=X<=q^(1/2+1/128),
 |sum alpha_m beta_n Z_q(cmn)|
       <<q^epsilon ||alpha||2||beta||2 *X*q^(-1/256).       (6)
Here and below harmless fixed interval constants are absorbed using the
strict exponent margins. To classify q, start r=U(q). If r>=q^(1/32),
use(5). Otherwise, if a remaining simple prime lies in[q^(1/32),q^(2/5)],
include it: now q^(1/32)<=r<=q^(2/5+1/32). If no such prime exists,
multiply the primes<q^(1/32) into r until crossing the lower threshold;
the first crossing is <q^(1/16). If no crossing occurs, the small factor
t<q^(1/32) leaves one or two simple primes, each >q^(2/5).
The divisor window must therefore extend to69/160, NOT just2/5.
The three savings in(5), writing r=q^rho,X=q^x, are
 (x-rho)/4, (2*x-1+rho)/8, 3*x/4-(1-rho)/4;
all are >=1/256 for x>=1/2 and 1/32<=rho<=69/160.
Also X<=s and4r<=X hold with strict margins.

For the prime/two-prime remainder use the reviewed amplification in
squarefree_unbalanced_kernel.py III, with its SAME requirements and
parameters. Splitting the first coefficient modulo t costs sqrt(t)
by Cauchy, even when t is not squarefree: only |Z_t|<<t^epsilon is used.
Its norm factor is sqrt(t)*(sqrt(X)+R^(11/64)X^(5/8)), R=q/t,
giving at least the previous q^(-11/2048) saving relative to X.
The two-prime proof permits the second variable in an arbitrary interval:
its scalar incidence uses a*m with m in[1,X], while the other variable
enters only through interval lengths/congruences. The KMS prime input
explicitly permits an arbitrary-position interval. Reduction modulo a
core modulus requires at most two wrap pieces because X<R.
No prime-square source theorem is being imported. Primary inputs remain
FKM1405.2293v2 Corollary3.4 and KMS1511.01636v5, already checked in the
retained proof modules; no new external novelty claim is made.

III. Natural K and all prime-power degeneracies.
For U(q)<=q^(51/128), arbitrary integer c, and
sqrt(q)<=X<=q^(1/2+1/256), (6) holds for natural K_q.         (7)
At each p^e||q with e>=2, K_(p^e)(z) vanishes if p|z. Thus a nonunit
c at such a prime gives zero, and otherwise the m,n unit restrictions
are separated masks. Only primes of exponent1 need the ordered
gcd(c,v),gcd(m,v/d0),gcd(n,v/(d0*d)) partition from the squarefree proof,
where v=q/U(q). Its exact factor1/D and remaining Z_(q/D) are unchanged;
D is coprime to q/D. For D<=q^(1/256), (6) applies since
  51/128=(2/5)*(1-1/256).
The support inequality is the same as that already proved. Large D use
1/D and the trivial norm factor X. Divisor multiplicities cost q^epsilon.

Put G_e(h,l,t)=F_(p^e)(h,l;t)/p^e. For EVERY prime p and e>=2,
 G_e(h,l,t)=K_(p^e)(hlt)
             +p*1_(p|h,l,t)*G_(e-1)(h/p,l/p,t/p).         (8)
For a primitive triple this follows from the unit change of variables
or the vanishing stationary equations. For an all-p-divisible triple,
F_(p^e)=p^2 F_(p^(e-1)), while K_(p^e)(hlt)=0. Iteration ends at the
exact prime formula
 G_1=K_p(hlt)-(I_h I_l+I_h I_t+I_l I_t)+(p+1)I_h I_l I_t.
This includes the completely zero triple and primes2,3.

For t=m*k, every local term has a modulus reduction D, coefficient w,
and divisibilities Hdiv|h,Ldiv|l,Tdiv|t, hence Kdiv=Tdiv/gcd(Tdiv,m)|k.
It satisfies, up to divisor-size factors,
  w/(Hdiv*Ldiv*Kdiv)<=1/D,
  w/(Hdiv*sqrt(Ldiv*Kdiv))<=1/sqrt(D).                     (9)
At recursion depth j<e the K-term has D=w=Hdiv=Ldiv=Tdiv=p^j.
The terminal hl,ht,lt corrections have D=p^e,w=p^(e-1) and respective
divisibility triples (p^e,p^e,p^(e-1)), (p^e,p^(e-1),p^e),
(p^(e-1),p^e,p^e). The all-three term has D=p^e,
w=p^(e-1)(p+1), all three divisors p^e. Only this last term needs the
factor1+1/p in(9). Multiplication over primes preserves (9); the number
of terms product(e+3) and product(1+1/p) are q^epsilon.
Exact CRT merely introduces unit dilations in these formulas.

IV. All-integer-modulus unbalanced smooth MODEL.
Use EXACTLY E_q from composite_linear_kernel.py, with
 B=Y^(1/2), A=Y^(1/4), C=Y^(1/2), K=Y^(1/4), m in[Y,2Y] integer,
 1<=H,J0<=Y^(1/4096), and EVERY integer q in[C,2C].
All unit r_q and bounded weights omega_(q,k) of joint spatial period
J=J_q<=J0 are allowed, including gcd(q,J)>1 and arbitrary k dependence.
Then, for every epsilon>0,
  sum_q |E_q|<<Y^(1-1/4096+epsilon).                       (10)
This is the specified MODEL box, not full box coverage or sieve transfer.

For good q with U(q)<=q^(39/100), use the EXACT period lift already proved:
 F_(qJ)(h,l;t)=J^2 sum_(a,b modJ; J|h+qa,l+qb)
       c_ab(k)*F_q((h+qa)/J,(l+qb)/J;t), |c_ab(k)|<=1.     (11)
Fix a,b and h BEFORE bounding l,k bilinearly. The transformed l' lies
in an arbitrary-position interval of width about q/A; k starts at1.
The arbitrary c_ab(k) is part of the k coefficient, so separation is
actual. Charge J^2 terms and the J^2 lift, for total J^4.
Importantly, if D|q and D|h'=(h+qa)/J, then D|h=Jh'-qa;
likewise for l. Thus the ORIGINAL nonzero Schwartz frequencies retain
the divisor savings in(9), even when J and q share primes.

Their original scales are U0=qJ/B~J,V0=qJ/A~sqrt(q)J, and
W=HK~sqrt(q)H. Sum nonzero h and l only; the integer axes are below.
For each h the actual l',k supports fit X~sqrt(q)H, enlarged by a tiny
Y^rho for tails. Using the ORIGINAL U0,V0 to bound norms deliberately
overcounts transformed widths and is safe. A restricted/reindexed
coefficient retains its norm; its interval length cannot increase.
For small D<=q^(1/256) in(8), the reduced Q=q/D meets(7), because
 U(Q)<=U(q) and 39/100 < (51/128)*(1-1/256).
Removing part of a prime power cannot increase the full squarefull part.
Also 1/2+1/2048 < (1-1/256)*(1/2+1/256), so X is in its padded range.
Take k as the first [1,X] variable, and l' as the arbitrary interval.
Equation(9) absorbs the D^(1/256) change in the saving. For large D use
its volume mass1/D. Both parts give, after the h sum,
  <<q^epsilon U0*sqrt(V0*W)*X*q^(-1/256).
The nonzero Schwartz divisor sums are O(scale/divisor), without '+1';
this remains true below scale1. Unit dilations and fixed h are absorbed
into the arbitrary integer multiplier in(7).

Restore Poisson prefactor Y/(q^3 J^2), normalization q, lift charge J^4,
and O(C) moduli. The good off-axis total is
  <<Y^(1-1/512+epsilon)*J0^(7/2)*H^(3/2).                (12)
At the caps its exponent is1-3/4096.
For bad q, squarefull density gives
 #{q:U(q)>q^(39/100)} <<C*sum_(u>C^(39/100) squarefull)1/u
                         <<C^(161/200).
Use the retained all-moduli pointwise off-axis bound H*J0^4*C per q.
Their total is <<Y^(361/400+epsilon)*H*J0^4. The already proved integer
axes and overlap together cost <<Y^(3/4+epsilon)*H*J0. Both are smaller
than (10) at the caps. This proves (10).

Reassessment: the old squarefull-residue budget remains a valid FAILURE
of that particular combination. The new placement of repeated factors
inside r avoids that cost. The initial proposed divisor window [1/32,2/5]
was too narrow when attaching U(q); independent review caught this, and
the widened69/160 window is paid explicitly above. Preserve (1)--(4) as
a separate promising component. Original-affine remains2b8cf98 and the
formal conservation identity6f9a77b does not estimate the signed gap.
Finite checks below test algebra and budgets, not infinite asymptotics.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import gcd

from all_moduli_balanced_kernel import _prime_power, _raw_transform, squarefull_parts
from composite_linear_kernel import _reduce
from major_arc_kernel import _factorization
from squarefree_correlation_kernel import _raw_kl3


@lru_cache(maxsize=None)
def cube_roots_square(p):
    q = _prime_power(p, 2)
    if p < 5:
        raise ValueError('cube-root formula requires p>=5')
    roots = [[] for _ in range(q)]
    for w in range(1, q):
        if w % p:
            roots[pow(w, 3, q)].append(w)
    return tuple(tuple(row) for row in roots)


def square_kl3_prediction(p, z):
    q = p*p
    counts = [0]*q
    for w in cube_roots_square(p)[z % q]:
        counts[3*w % q] += 1
    return _reduce(counts, q)


def square_correlation_raw(p, u, v, shift, twist):
    roots = cube_roots_square(p)
    q = p*p
    counts = [0]*q
    for x in range(q):
        for y1, y2, x1, x2 in product(roots[u*(x+shift) % q],
                roots[v*(x+shift) % q], roots[u*x % q], roots[v*x % q]):
            counts[(3*(y1-y2-x1+x2)+twist*x) % q] += 1
    return counts


def square_stationary_raw(p, u, v, shift, twist):
    roots = cube_roots_square(p)
    q = p*p
    counts = [0]*q
    if u % p == 0 or v % p == 0:
        return counts
    ratio = v*pow(u, -1, q) % q
    b, c = u*shift % q, twist*pow(u, -1, q) % q
    for lam, mu in product(roots[ratio], repeat=2):
        aa, bb = 1-lam, 1-mu
        for x, y in product(range(1, p), repeat=2):
            if (y**3-x**3-b) % p or (aa*x*x-bb*y*y+c*x*x*y*y) % p:
                continue
            lift = ((b+x**3-y**3)//p)*pow(3*y*y, -1, p) % p
            yy = y+p*lift
            counts[(3*(aa*yy-bb*x)+c*x**3) % q] += p
    return counts


def recursion_prediction(p, e, h, l, t):
    q = _prime_power(p, e)
    if e < 2:
        raise ValueError('recursion requires exponent at least2')
    counts = list(_raw_kl3(q, h*l*t % q))
    if h % p == l % p == t % p == 0:
        smaller = _raw_transform(q//p, h//p, l//p, t//p)
        for i, value in enumerate(smaller):
            counts[p*i] += F(p*value, q//p)
    return _reduce(counts, q)


def local_mass_terms(p, e):
    _prime_power(p, e)
    terms = []
    for j in range(e):
        d = p**j
        terms.append((d, d, d, d, d, F(1)))
    low, top = p**(e-1), p**e
    for hd, ld, td in ((top, top, low), (top, low, top), (low, top, top)):
        terms.append((top, low, hd, ld, td, F(1)))
    terms.append((top, low*(p+1), top, top, top, F(p+1, p)))
    return tuple(terms)


def repeated_factor_route(q):
    if type(q) is not int or q < 2:
        raise ValueError('require an integer modulus at least2')
    u, _, _, _ = squarefull_parts(q)
    if u**5 > q*q:
        raise ValueError('require full squarefull part <=q^(2/5)')
    simple = [p for p, e in _factorization(q) if e == 1]
    if u**32 >= q:
        return 'divisor', u, q//u
    for p in simple:
        if p**32 >= q and p**5 <= q*q:
            return 'divisor', u*p, q//(u*p)
    r = u
    for p in simple:
        if p**32 < q:
            r *= p
            if r**32 >= q:
                return 'divisor', r, q//r
    return 'core', r, tuple(p for p in simple if p**5 > q*q)


def all_integer_unbalanced_budget(period=0, frequencies=0):
    if any(type(v) not in (int, F) or not 0 <= v <= F(1, 4096)
           for v in (period, frequencies)):
        raise ValueError('require exact exponents between0 and1/4096')
    return {'good': 1-F(1, 512)+F(7, 2)*period+F(3, 2)*frequencies,
            'bad': F(361, 400)+4*period+frequencies,
            'axes': F(3, 4)+period+frequencies,
            'claimed': 1-F(1, 4096),
            'support': F(1, 2)+2*frequencies,
            'support_ceiling': (1-F(1, 256))*(F(1, 2)+F(1, 256)),
            'fullpart': F(39, 100),
            'fullpart_ceiling': F(51, 128)*(1-F(1, 256))}
