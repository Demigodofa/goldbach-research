"""Divisor shifts and prime cores save the unbalanced squarefree MODEL.

Owner: Kevin's Goldbach research. Purpose: test whether the two-prime
mechanism can cover general squarefree factorizations at the previously
failing box B=Y^1/2,A=Y^1/4,C=Y^1/2,K=Y^1/4. The mechanism changes under
the evidence: use four-factor correlations for a suitable divisor, and
retain the eight-factor prime/core theorem for the remaining moduli.
Polynomial identities, reciprocal energy and earlier bounds remain tools.
This is a MODEL estimate, not the original signed prime correlation.

Primary sources checked for this derivation:
* Fouvry--Kowalski--Michel, A study in sums of products,
  arXiv:1405.2293v2, Definition1.3 and Corollary3.4, printed pp4--5,18:
  https://arxiv.org/pdf/1405.2293v2 . Its PRIME four-factor correlation
  input is used below with an explicit normality check and additive twist.
* KMS arXiv:1511.01636v5, Theorem1.1, Lemma2.5 and Theorem4.11:
  https://arxiv.org/pdf/1511.01636v5 . Prime/core amplification and CRT
  were reviewed in two_prime_kl3_kernel.py. The wider length needed here
  is checked explicitly below; it is not assumed from the old statement.
No composite version of a prime theorem, Kl2 theorem for Kl3, prime-power
correlation theorem, or external originality assertion is being imported.

I. A four-factor input with explicit exceptional parameters.
For squarefree q retain
  K_q(z)=q^-1 sum_(u,v unitsq)e_q(u+v+z/(uv)),
  Z_q(z)=1_(gcd(z,q)=1)*K_q(z).
The zero extension is deliberate; the natural K_p(0)=1/p is restored later.
For a prime p and unit u,v, define
  C_p(u,v,a;h)=sum_x Z_p(u(x+a))*conjugate(Z_p(v(x+a)))
                       *conjugate(Z_p(ux))*Z_p(vx)*e_p(hx).
Then, uniformly in h,
  |C_p|<<sqrt(p) if a!=0 and u!=v,-v (modp), and <<p always. (1)
Indeed the four affine maps u(x+a),v(x+a),ux,vx have four distinct
orbits under the sign involution x->-x in the first case. With the bar
pattern (Id,conjugate,conjugate,Id), each orbit has signed multiplicity
1 or-1, hence is3-normal. Apply FKM Corollary3.4. Replacing its extension
at0 by Z changes at most two bounded terms. Small primes are absorbed in
the uniform constant. Keeping u=-v in the exception is conservative.

CRT, using K_q(z)=product_p K_p(z*inverse((q/p)^3)), gives for squarefree s
and units u,v
  |C_s(u,v,a;h)|<<s^epsilon*sqrt(s*gcd(s,a*(u*u-v*v))).     (2)
The local parameters are u/Q_p^3,v/Q_p^3,a,h/Q_p (modp). Here x is NOT
rescaled, so the Fourier twist is inverse(Q_p), unlike the previous
eight-factor completion in the s variable. Fourier completion of any
interval of length <=s gives the same bound with logarithmic loss.

II. Divisor shifts for arbitrary coefficients.
Let q=r*s be squarefree, (r,s)=1, 4*r<=X<=s, and c a q-unit. Let alpha,beta
be arbitrary complex coefficients supported in[1,X]. Then
  |sum_(m,n) alpha_m beta_n Z_q(cmn)|
    <<q^epsilon ||alpha||2||beta||2
       [X^(3/4)*r^(1/4)+X^(3/4)*s^(1/8)+X^(1/4)*s^(1/4)]. (3)
Restrict m to q-units, since other rows vanish. Cauchy in beta reduces to
T=sum_(n<=X)|sum_m alpha_m Z_q(cmn)|^2. For fixed m1,m2 its inner
interval correlation I factors as sum_n f_r(n)*f_s(n), with |f_r|,|f_s|
bounded by q^epsilon, and f_r periodic modulo r.

Put H=floor(X/(2*r)). Averaging translates by h*r, 1<=h<=H, then Cauchy
in the extended n interval, gives the elementary divisor-shift inequality
  |I|^2 <<q^epsilon [X^2/H+(X/H)*sum_(1<=h<H)|I_s(h*r)|], (4)
where I_s is an interval correlation of f_s(n+h*r) with f_s(n). Interval
intersections have length <=X; shifted endpoints are included. Apply(2),
then use the positive-integer divisor sum
  sum_(1<=h<H) sqrt(gcd(s,h*d)) <<H*tau(s)*sqrt(gcd(s,d)),
  d=m1*m1-m2*m2.
This remains valid for d=0; no divisor count of the integer0 is used.
It follows that
  |I|<<q^epsilon [(X*r)^1/2+X^1/2*s^1/4*gcd(s,d)^1/4].   (5)

The weighted pair average is paid, including all nonunit differences:
  sum_(m1,m2 unitsq)|alpha_m1 alpha_m2|*gcd(s,m1^2-m2^2)^1/4
     <<q^epsilon ||alpha||2^2*(X+s^1/4).                  (6)
To prove this, majorize the gcd power by sum_(d|s,d|m1^2-m2^2)d^1/4.
For each d and fixed unit m1, there are at most 2^omega(d) possible
residues m2 mod d, choosing either sign at each prime. The symmetric
incidence matrix has row sums <=2^omega(d)*(X/d+1). Its quadratic form
in |alpha| is at most this bound times ||alpha||2^2. Sum over divisors.
Substitution of(5)--(6) into T and outer Cauchy proves(3).

III. Every squarefree modulus: the zero-extension theorem.
For EVERY squarefree q>=2, c unit, and sqrt(q)<=X<=q^(1/2+1/128),
  |sum alpha_m beta_n Z_q(cmn)|
     <<q^epsilon ||alpha||2||beta||2 *X*q^(-1/256).         (7)
If q has a divisor r in[q^(1/32),q^(2/5)], use(3). Writing r=q^rho and
X=q^x, its three savings relative to X are
  (x-rho)/4, (2*x-1+rho)/8, 3*x/4-(1-rho)/4.
For x>=1/2,1/32<=rho<=2/5, each is at least1/256. The conditions
4r<=X<=s hold for sufficiently large q. Finite moduli change constants.

Otherwise every prime factor is either <q^(1/32) or >q^(2/5). The product
t of the small prime factors is <q^(1/32): a first product crossing this
threshold would be <q^(1/16), a forbidden divisor. The remainder R=q/t
has one or two distinct primes, all >q^(2/5), since three such primes
would have product>q. R=1 is impossible in this case.

CRT splits Z_q into Z_t times a unit-dilated Z_R. Fix the residue of m
mod t; its Z_t factor becomes a bounded coefficient of n. Sum coefficient
norms over these residue classes by Cauchy, paying at most t^(1/2+epsilon).
For prime R the KMS prime theorem has norm factor
  O(sqrt(X)+R^(11/64)*X^(5/8)).
For two-prime R use the SAME amplification proof as two_prime_kl3_kernel.py,
now with A0=R^(1/8), B0=X*R^(-1/8), L=A0*X. Its actual requirements hold:
  R>q^(31/32), X<=q^(65/128), B0<=q^(99/256)<min(p1,p2),
  A0*X<R, X<R^(5/8), A0<min(p1,p2).
Strict exponent margins absorb the fixed interval constants. Hence both
local diagonals synchronize and the moment remains O(X^4*R). The
nonunit-difference term sqrt(X)+X/sqrt(p_min) is absorbed in
R^(11/64)*X^(5/8): p_min>=R^(2/5), X<=R^(5/8) suffice. This proves the
required wider core estimate directly, without changing the old theorem.
After the t^(1/2) cost, the saving relative to X is at least
  q^(-1/64)*t^(21/64) <=q^(-11/2048),
which is stronger than q^(-1/256). The sqrt(X) term is also smaller.
This proves(7) for all squarefree factorizations.

IV. Natural extension and ALL integer multipliers.
For all squarefree q, ANY integer c, and
  sqrt(q)<=X<=q^(1/2+1/256),
the bound(7) holds with K_q in place of Z_q.                  (8)
Here is an exact, separated partition that prevents a small prime factor
from becoming a constant-size error. Put d0=gcd(c,q), q0=q/d0. Partition
d=gcd(m,q0), then e=gcd(n,q0/d), write m=d*a,n=e*b, and set D=d0*d*e,
Q=q/D. The coefficient masks are gcd(a,q0/d)=1 and gcd(b,Q)=1; each
depends on its own variable. Exact CRT gives on this part
  K_q(c*d*a*e*b)=D^-1*Z_Q(c*d*e*a*b*inverse(D^3)).          (9)
For Q=1 the right side is the constant1/D. The restricted/reindexed L2
norms do not increase. If D<=q^(1/256), padding both supports to X is
allowed in(7), since
  1/2+1/256 < (1-1/256)*(1/2+1/128).
Thus this part has norm factor
  D^-1*X*(q/D)^(-1/256)<=X*q^(-1/256).
For D>q^(1/256), use the pointwise q^epsilon bound on Z_Q and Cauchy
on each support; the factor <=X/D gives the same saving. Summing at
most tau(q)^2 parts costs q^epsilon. This includes c=0 and nonunit m,n.

V. The full unbalanced squarefree smooth MODEL, with periods paid.
Use the exact E_q in composite_linear_kernel.py, now with
  B=Y^1/2,A=Y^1/4,C=Y^1/2,K=Y^1/4, m in[Y,2Y] integer,
  1<=H,J0<=Y^(1/4096), q in[C,2C] SQUAREFREE.
All unit r_q and arbitrary bounded joint period-J_q weights omega_(q,k)
are retained, including arbitrary dependence on q,k and gcd(J_q,q)>1.
Then for every epsilon>0,
  sum_q |E_q| <<Y^(1-1/4096+epsilon).                     (10)
The better raw exponent obtained below is1-511/1048576 before epsilon.
This theorem does not cover prime powers or the original sieve weights.

Let J=J_q, g=gcd(q,rad(J)), Q=q/g, T=g*J. Then gcd(Q,T)=1 and qJ=Q*T.
Double Poisson has prefactor Y/(q^3*J^2); exact CRT gives an F_Q factor
and a small factor G_T of magnitude<=T^2, depending on h,l only modulo T.
FIX h before applying a bilinear bound to l,k. Only l must be split into
T residue classes, so the total small-factor charge is T^3. For each
fixed h and l class, G_T/T^2 is a bounded coefficient of k. This saves
one redundant residue split from the older conservative T^4 argument;
no coupled arithmetic coefficient is assumed separated for free.

Nonzero h,l have Schwartz scales U=qJ/B asymp J,V=qJ/A asymp Y^1/4 J;
write W=H*K asymp Y^1/4 H and choose X asymp max(V,W), padded by a tiny
Y^rho for tails. All truncation/source losses fit the final epsilon.
The h=0/l=0 integer axes and their overlap are kept for the last step.

For F_Q(h,l;t)/Q use the EXACT prime degeneracy expansion (4) in
squarefree_correlation_kernel.py, with t a unit multiple of m*k. Each
term has D=d_hl*d_ht*d_lt*a dividing Q, coefficient <=a*Q^epsilon,
and h,l,k divisible respectively by Hdiv,Ldiv,Kdiv, where
  Hdiv=d_hl*d_ht*a, Ldiv=d_hl*d_lt*a, Tdiv=d_ht*d_lt*a,
  g0=gcd(Tdiv,m), Kdiv=Tdiv/g0,
  Hdiv*Ldiv*Kdiv=D^2*a/g0.                                (11)
Its remaining factor is a unit-dilated K_(Q/D)(m*h*l*k), with rescaled
variables. All these divisors are coprime to T, so an l residue class
is just changed, never split further. Fixing h leaves separated l,k weights.

If D<=Q^(1/256), apply(8) to l,k padded to the original X. This is allowed:
at the largest decorations log_Q X is at most1025/2047, whereas
  1025/2047 < (1-1/256)*(1/2+1/256).
There is a strict margin for tails and dyadic constants. After summing
nonzero h, the relative coefficient/norm mass is
  a/[Hdiv*sqrt(Ldiv*Kdiv)]=sqrt(a*g0/Hdiv)/D<=D^(-1/2).
This absorbs the factor D^(1/256) from reducing the modulus. Thus the
contribution is at most U*sqrt(V*W)*X*Q^(-1/256+epsilon).
The Schwartz sum over nonzero multiples of a divisor is O(scale/divisor),
even below scale1; no extra '+1' loss is inserted on these nonzero modes.

If D>Q^(1/256), use the pointwise bound and full volume. The relative
mass is a/(Hdiv*Ldiv*Kdiv)=g0/D^2<=1/D, giving
  U*V*W*Q^(-1/256+epsilon)<=U*sqrt(V*W)*X*Q^(-1/256+epsilon).
There are at most5^omega(Q) terms; absorb them into epsilon. Signs of h,l
are treated separately and absorbed into the unrestricted multiplier.

Restore the prefactor, F_Q normalization Q, T^3 charge and O(C) moduli.
Writing D0=max(J,H), the total off-axis bound is
  <<Y^(1-1/512+epsilon)*g^(2+1/256)*J^(5/2)*H^(1/2)*D0.    (12)
Since g<=J and J,H<=Y^(1/4096), the decoration exponent is at most
(6+1/256)/4096. Therefore(12) has exponent1-511/1048576, below that
asserted in(10). The already proved integer axes plus overlap cost
Y^(3/4+epsilon)*H*J0, also absorbed. This proves(10).

VI. The existing squarefull-part split fails its decorated power budget.
Let u(q) be the FULL squarefull part, and split at Z=Y^z. For small u,
the same CRT proof replaces g by u*gcd(q/u,rad(J)), costing u^(2+1/256)
in(12). Summing over q with a fixed full part u costs O(C/u). The known
O(sqrt(V)) count of squarefull numbers <=V therefore gives
  sum_(u<=Z squarefull)u^(1+1/256)<<Z^(3/2+1/256).
Thus, with the current full H,J0 caps, the small-u upper exponent is
  A+(3/2+1/256)*z, A=1-511/1048576.
The retained all_moduli_balanced_kernel.py pointwise/large-u bound has
upper exponent 1+5/4096-z/2. On0<=z<=1/1024 the small-u proof's support
conditions hold: even the largest log_Q X is1025/2043<32895/65536.
The best maximum of these two affine budgets occurs at z=199/233472,
where it is467315/466944>1. Equivalently, saving in the first requires
z<73/225280, while the second requires z>5/2048. They are incompatible.
This is a verified FAILURE of this combination of upper bounds, even
after paying the small-u density rather than just its supremum. It is
not a lower bound on the true error or a limitation of all prime-power
methods. Do not repeat this exact split expecting a saving at the same
caps. A stronger prime-power/off-axis estimate or a different combination
is needed for all integer moduli in this unbalanced box.

Reassessment: a factorization mechanism succeeds for ALL squarefree q in
this unbalanced MODEL box. Neither prime powers here, full hyperbola-box
coverage, nor original arithmetic/sieve transfer has been proved. Latest
original-affine result remains2b8cf98; formal cancellation remains distinct
from the unestimated signed prime correlation. No actual exceptional zero,
effective onset, universal prime coverage, or external novelty is claimed.
The direct eight-factor extension remains a promising component: the
reviewer located, and the source check confirmed, KMS Proposition4.29,
printed p44, constructing V_bad over Z[1/ell]. Thus the bad hypersurfaces
are not unrelated choices at each prime. A simultaneous congruence-count
route was considered; its full nonunit-difference/amplification transfer
is not proved here and is not needed for(10). Preserve this locator for
a workload where it improves on the divisor-shift argument.
Finite routines below guard algebra and cost accounting, not asymptotics.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd

from composite_linear_kernel import _reduce
from major_arc_kernel import _factorization
from reciprocal_energy_kernel import _divisors
from squarefree_correlation_kernel import _raw_kl3
from two_prime_kl3_kernel import _gauss_mul, _conjugate, _reduce_gauss


def _squarefree(q):
    if type(q) is not int or q < 2:
        raise ValueError('require an integer modulus at least2')
    factors = _factorization(q)
    if any(e != 1 for _, e in factors):
        raise ValueError('require a squarefree modulus')
    return tuple(p for p, _ in factors)


def affine_normality(p, u, v, shift):
    """Signed orbit counts for the four affine maps, rank3 sign involution."""
    maps = ((u % p, u*shift % p), (v % p, v*shift % p),
            (u % p, 0), (v % p, 0))
    signs = (1, -1, -1, 1)
    balances = []
    for gamma in maps:
        negative = tuple(-x % p for x in gamma)
        balances.append(sum(sign for transform, sign in zip(maps, signs) if transform == gamma)
                        -sum(sign for transform, sign in zip(maps, signs) if transform == negative))
    return tuple(balances)


def _raw_shift(values, u, v, shift, twist):
    q = len(values)
    counts = [[0, 0] for _ in range(q)]
    for x in range(q):
        value = _gauss_mul(values[u*(x+shift) % q], _conjugate(values[v*(x+shift) % q]))
        value = _gauss_mul(value, _conjugate(values[u*x % q]))
        value = _gauss_mul(value, values[v*x % q])
        counts[twist*x % q][0] += value[0]
        counts[twist*x % q][1] += value[1]
    return tuple(tuple(v) for v in counts)


def shift_correlation_exact(values, u, v, shift, twist):
    return _reduce_gauss(_raw_shift(values, u, v, shift, twist))


def shift_correlation_crt(local, u, v, shift, twist):
    q = 1
    for p in local:
        q *= p
    counts = [(1, 0)]+[(0, 0)]*(q-1)
    for p, values in local.items():
        scale = q//p
        invcube = pow(scale**3, -1, p)
        factor = _raw_shift(values, u*invcube, v*invcube, shift, twist*pow(scale, -1, p))
        result = [[0, 0] for _ in range(q)]
        for i, a in enumerate(counts):
            for j, b in enumerate(factor):
                value = _gauss_mul(a, b)
                result[(i+scale*j) % q][0] += value[0]
                result[(i+scale*j) % q][1] += value[1]
        counts = [tuple(v) for v in result]
    return _reduce_gauss(counts)


def divisor_shift_identity(first, second, length, shifts):
    """Exact Gaussian integer averaging, correlation energy, and Cauchy bound."""
    r, s = len(first), len(second)
    def add(a, b):
        return (a[0]+b[0], a[1]+b[1])
    def norm(a):
        return a[0]**2+a[1]**2
    original = (0, 0)
    for n in range(1, length+1):
        original = add(original, _gauss_mul(first[n % r], second[n % s]))
    averaged, energy = (0, 0), 0
    indices = range(1-r*shifts, length-r+1)
    for n in indices:
        inner = (0, 0)
        for h in range(1, shifts+1):
            if 1 <= n+r*h <= length:
                inner = add(inner, second[(n+r*h) % s])
        averaged = add(averaged, _gauss_mul(first[n % r], inner))
        energy += norm(inner)
    expanded = shifts*sum(norm(second[n % s]) for n in range(1, length+1))
    for h in range(1, shifts):
        corr = sum(_gauss_mul(second[(n+r*h) % s], _conjugate(second[n % s]))[0]
                   for n in range(1, length-r*h+1))
        expanded += 2*(shifts-h)*corr
    return dict(original=original, averaged=averaged, energy=energy, expanded=expanded,
                cauchy_left=shifts**2*norm(original),
                cauchy_right=len(indices)*max(map(norm, first))*energy)


def factorization_route(q):
    primes = _squarefree(q)
    for r in _divisors(q):
        if r**32 >= q and r**5 <= q*q:
            return ('divisor', r, q//r)
    small = 1
    large = []
    for p in primes:
        if p**32 < q:
            small *= p
        else:
            large.append(p)
    return ('core', small, tuple(large))


def natural_bilinear_direct(q, c, alpha, beta):
    _squarefree(q)
    counts = [F(0)]*q
    for m, a in enumerate(alpha, 1):
        for n, b in enumerate(beta, 1):
            for i, value in enumerate(_raw_kl3(q, c*m*n % q)):
                counts[i] += a*b*value
    return _reduce(counts, q)


def natural_bilinear_partition(q, c, alpha, beta):
    _squarefree(q)
    counts = [F(0)]*q
    d0 = gcd(c, q)
    q0 = q//d0
    for d in _divisors(q0):
        q1 = q0//d
        for e in _divisors(q1):
            big_d, reduced = d0*d*e, q1//e
            for a in range(1, len(alpha)//d+1):
                if gcd(a, q1) != 1:
                    continue
                for b in range(1, len(beta)//e+1):
                    if gcd(b, reduced) != 1:
                        continue
                    weight = F(alpha[d*a-1]*beta[e*b-1], big_d)
                    if reduced == 1:
                        counts[0] += weight
                    else:
                        parameter = c*d*e*a*b*pow(big_d**3, -1, reduced) % reduced
                        for i, value in enumerate(_raw_kl3(reduced, parameter)):
                            counts[big_d*i] += weight*value
    return _reduce(counts, q)


def unbalanced_squarefree_budget(period=0, frequencies=0, shared=0):
    if any(type(v) not in (int, F) for v in (period, frequencies, shared)):
        raise ValueError('use exact rational exponents')
    j, h, g = map(F, (period, frequencies, shared))
    if not 0 <= g <= j <= F(1, 4096) or not 0 <= h <= F(1, 4096):
        raise ValueError('outside the proved decoration range')
    return dict(off_axis=1-F(1, 512)+(2+F(1, 256))*g+F(5, 2)*j+h/2+max(j, h),
                axes=F(3, 4)+j+h,
                padded_x=(F(1, 4)+max(j, h))/(F(1, 2)-g),
                small_d_ceiling=(1-F(1, 256))*(F(1, 2)+F(1, 256)),
                claimed=1-F(1, 4096))


def squarefull_split_budget():
    head = 1-F(511, 1048576)
    tail = 1+F(5, 4096)
    slope = F(3, 2)+F(1, 256)
    cutoff = (tail-head)/(slope+F(1, 2))
    return dict(cutoff=cutoff, best=head+slope*cutoff,
                head_saving_threshold=(1-head)/slope,
                tail_saving_threshold=2*(tail-1),
                support_at_upper_cutoff=F(1025, 2043),
                support_ceiling=F(32895, 65536))
