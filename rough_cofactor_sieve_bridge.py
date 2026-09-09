"""Transfer the full smooth model to actual rare/rare affine prime pairs.

Owner: Kevin's Goldbach research. Purpose: preserve the positive cofactor
sieve, weighted density lemma and actual arithmetic transfer, with finite
guards for their exact identities. These are research components, not a
manuscript, a numerical prime experiment, or a claim of historical novelty.

THEOREM. Keep the actual-zero and large-V hypotheses, notation and B_M of
rare_affine_small_cofactor.py: chi primitive quadratic modulo D>24 with an
ACTUAL zero 1-1/(eta*log D), Y=D^V, V>=log^3 eta, t=V/eta<=1/log Y;
m is even in[Y,2Y]. Fix 0<theta<1/5. For ANY subset C of
  2<=M<=Y^(13/25), P^-(M)>Y^theta, gcd(M,D*m)=1,
one has, with rho=2^-20,
  sum_(M in C) B_M
    <<_theta S_2(m)*Y*t^2*(log eta)^9
            +Y^(1-rho/2+o(1))+S_2(m)*Y*eta^-19
     =o_theta(Y*t).                                           (1)
The limits and constants are ineffective. This does not assert a zero
exists. It extends the ACTUAL AFFINE range; the underlying model theorem
alone did not give (1). It gives neither a signed prime-correlation estimate
nor a positive lower bound for the weighted total nor Goldbach coverage.
The fixed polynomial weights can use this component and remain available.

DEPENDENCIES AND SOURCE CORRECTION.
Use full_model_box_kernel.py and its already reviewed dependencies for the
all-integer smooth model saving 1/4096. The source arithmetic is a DIRECT
adaptation of Matomaki--Merikoski (MM), arXiv:2112.11412v2, Lemmas2.4,
3.2--3.3, and the proof of Proposition2.3, especially(15),(33)--(39):
https://arxiv.org/html/2112.11412v2 . MM does not state our affine theorem.
Use Henriot's corrected NEW Theorem5, printed p377, with exact-valuation
conditions(0.1)--(0.2), as retained in multi_rare_partner.py:
https://doi.org/10.1017/S0305004114000280 ; definitions arXiv:1102.1643.
Do not retry the unchanged blocked Henriot source route or substitute the
uncorrected leading-coefficient/discriminant corollary.

MM equation(22) has a SIGN TYPO for the upper beta weights defined there.
Its exact identity must be
  sum_d lambda_d*g(d)=prod_(p<z)(1-g(p))+sum_(r odd)V_r(z),       (2)
with PLUS, not the displayed minus. Indeed its preceding pointwise
identity is 1_rough(n)=sigma(n)-sum_(r odd)S_r(n), S_r>=0.
For R=100,beta=2,z=10, support is{1,2,3,6}, coefficients(1,-1,-1,1).
At g(d)=1/d the two sides are 1/3=8/35+11/105. The relative O estimate
of Lemma3.2(ii) survives: its proof bounds the absolute remainder. We use
that estimate and the corrected sign, never the false signed equality.

I. Positive majorant with a uniform WEIGHTED harmonic density.
Choose fixed large A, then its fixed beta>=2, and U=K0*log eta. Choose K0
last, large enough in terms of A,beta,rho for all eta^-100 errors below.
Set R=Y^rho,z=Y^(1/U). Eventually rho*U>=beta, D<z<Y^theta.
All prime cutoffs mean STRICTLY below z. For d=p1*...*pr, p1>...>pr,
put lambda_d=mu(d) when every odd prefix j satisfies
  p1*...*pj*p_j^beta<R,
and zero otherwise. Then d<R and |lambda_d|<=1. Put
  sigma(n)=sum_(d|n)lambda_d >=1_((n,P(z))=1)>=0.                (3)
It can admit nonrough n: in the witness above sigma(5)=1. Never infer
that a sigma-supported M is rough. For nonnegative original summands,
ANY subset of original rough M may be enlarged and majorized by sigma.

For every fixed C>=0 write F_C(n)=prod_(p|n)(1+C/p). We prove
  sum_(B<=n<2B) sigma(n)*F_C(n)
       <<_C B/log z+R*sqrt B,                                (4)
and hence, over Y^(1/5)<=M<=Y^(13/25),
  sum sigma(M)*F_C(M)/M <<_C U.                               (5)
Here and below the fixed beta lemma constants are permitted as well.
For (4), remove the finitely many primes p<max(C,2) from F_C, at a fixed
C-dependent multiplicative cost; positivity(3) licenses this upper bound.
For remaining primes put c_p=C/p, otherwise c_p=0, and let f be squarefree
multiplicative with f(p)=c_p. Thus F(n)=sum_(d|n)f(d) and
  A_C=prod_p(1+c_p/p),
  sum_(B<=n<2B; ell|n)F(n)=B*A_C*g(ell)+O_C(sqrt B),            (6)
uniformly for EVERY positive ell, where
  g(ell)=ell^-1*prod_(p|ell)(1+c_p)/(1+c_p/p).
Expand divisors and count multiples of lcm(d,ell). Floor errors are
bounded by sum_(d<=2B)f(d)<=sqrt(2B)*sum_d f(d)/sqrt d=O_C(sqrt B).
Extending the main sum past 2B costs at most
 B*sum_(d>2B)f(d)/d=O_C(sqrt B), using gcd(d,ell)<=ell.
Both infinite products converge. Moreover g is multiplicative and
  1/p<=g(p)=(1+c_p)/(p+c_p)<=2/p.
Summing(6) against lambda_ell and applying MM Lemma3.2(ii) bounds the
main by B*prod_(p<z)(1-g(p))<<B/log z. At most R coefficients give
the stated error. A dyadic decomposition gives O(U) for the main in(5);
its errors total O(R*Y^-1/10), which is bounded. No absolute-value sum
of beta coefficients is used for the main density.

II. Actual prime majorant, uniform sieve tails, and ordering of operations.
The original M<=Y^(1/5) range is already proved; use it unchanged. For
larger M set Q=Y/M>=Y^(12/25), L=log Y. Use the fixed nonnegative smooth
majorant g(q/Q,p/Y) of the old affine proof, and lambda_chi=1*chi>=0.
Since lambda_chi(r)=2 for each prime with chi(r)=+1, our original sum is
bounded by a constant times
 L^2*sum_(M; (M,Dm)=1) sigma(M)
       *sum_(q,p=m-Mq; (qp,P(z))=1)g(q/Q,p/Y)lambda_chi(q)lambda_chi(p).
Smooth dyadic M windows can be nonnegative majorants. The source smooth
hyperbola identity supplies physical small factors a<<sqrt Q,c<<sqrt Y
and four character orientations. Keep (M,Dm)=1 EXACT while estimating
all nonnegative beta-sieve remainders, before any Mobius truncation of it.

For a common prime r|q,p on the original rough support, r|m and r>=z.
There are O(U) such primes and their reciprocal sum is O(U/z). Counting
q multiples uses Q/r+1 directly; lambda_chi(q)lambda_chi(p)<=exp(O(U)).
Since Q>=Y^.48 and log z>>log^2 eta, the cost is Q*eta^-B for any fixed
B, after the fixed logarithms. No short-interval Henriot bound at Q/r
is assumed. Average by(5), choosing B large.

The other tails collapse as in MM(15) to fixed divisor powers on n and
m-Mn with roughness cutoffs z_r=z^((beta-1)/beta)^r and factors 2^-Ar.
Apply corrected Henriot directly to these two primitive forms: x is
comparable to Q, alpha=1/2, norm exponent2/5, norm<=3Y, and a sufficiently
small FIXED function-class epsilon for the fixed divisor powers. Thus
x>=C0*(3Y)^(2/5) uniformly. The divisor-class epsilon enters the theorem
constant, NOT a spurious factor Y^epsilon in this eta-scale bound.
For p|M, (M,m)=1 means m-Mn is always a p-unit. All its positive-valuation
tuples vanish. The remaining exact local factors differ from the generic
two-root factors by 1+O_A(1/p), uniformly in v_p(M). Their product is
bounded by F_C(M) for a fixed C=C(A). At p|m use the common-root and
P_m cutoffs of MM(15); p=2 belongs here and cannot divide M. Conductor
primes introduce no new M factor because (M,D)=1. The resulting per-M
bound is
 S_2(m)*F_C(M)*Q/L^2 * U^O_A(1)
             *(exp(-c*A*rho*U)+U^6/z).                       (7)
The geometric tail of 2^-Ar absorbs the fixed changes of z_r. This is the
same fixed-parameter summation as MM(15), with the paid M factors just
described. Equations(5),(7), the finite dyadic losses, and K0 sufficiently
large make the total O(S_2(m)*Y*eta^-20).

III. Zero mode: retain sigma and obtain TWO harmonic cancellations.
Retain the exact condition (M,Dm)=1 here. Restore the q,p small-factor
roughness and recombine all four orientations and all dyadic main terms
BEFORE absolute values. For each M the result is the old affine formula
  V_(m,M,D)(z)*K_(m,M)(D)
       *integral g(y/Q,(m-My)/Y)*A_z(y)*A_z(m-My)dy.            (8)
Its exact normalization is chi(a)*chi(c)/(a*c)*K_(m,M)(D);
there is NO chi(M) factor. K_(m,M)<=4*A_D(m)/D for (M,D)=1.
At p|M, p>2 and p not dividing Dm, the sieve density changes from
1-2/p to 1-1/p. Thus
  V_(m,M,D)(z)<=F_3(M)*V_(m,1,D)(z),                          (9)
because (p-1)/(p-2)<=1+3/p. This includes small primes admitted by sigma.
When removing (M,c)=1 after c is restored to z-rough, only primes r|M
with r>=z can occur. Their reciprocal sum is O(U/z), regardless of M's
smaller prime factors. The same harmonic argument controls the other
shared-factor removals. There is no need to resum sigma to roughness.

MM Lemma2.4, subtracted at its two log endpoints, and Abel summation
give A_z(y),A_z(m-My)=O((t*U^4+eta^-30)/U). Both transition scales are
at least Y^(6/25) and lie in its permitted[Y^(1/10),Y^2] range. Restoring
conductor factors gives (A_D(m)/D)*V_(m,1,D)<<S_2(m)*U^2/L^2.
After prime logs and(5), (8) is
  O(S_2(m)*Y*t^2*U^9+S_2(m)*Y*eta^-20).                     (10)
This extra U is the explicit cost of the positive cofactor majorant.

IV. Actual nonzero modes fit the model, with every index charged.
Use PHYSICAL a and M. Insert e|a for the old small-factor sieve index
and e0|M for sigma; do not replace a by e*a' or M by e0*M'. The source
congruence is M*d1*a*n=m (mod q0), q0=d2*c. Keep gcd(D*d1,q0)=1 as
the source requires. Before expanding (M,m)=1 insert the EXACT native
mask (M,q0)=1: it is automatic on the original congruence, but need not
be automatic in individual later Mobius terms. Also retain (M,D)=1.
The (a,q0)=1 mask belongs to the model's native unit restriction.

CRT and Poisson now give the phase
  e_(q0)(-inverse(D*d1)*m*k*inverse(M*a)),                     (11)
up to the orientation sign. The conductor is D; the arithmetic modulus
is q0=d2*c, never M*q0. The normalized complete character factor is
  D^-1*sum_(gamma modD) psi1(d1*d2*c*gamma)
            *psi2(m-M*d1*d2*a*c*gamma)*e_D(-k*gamma).
This uses the negative Fourier convention in(11); reversing convention
reverses BOTH additive phases. The finite CRT guard uses the same signs.
Its absolute value is<=1, and it is periodic in both M,a modD. Bounded
small-factor characters and all q0,k dependence are allowed by the model.
Changing y=Y*s/M makes the remaining prefactor Y/(M*a*d1*q0).
For M=B*u,a=A*v the factors B/M,A/a multiply a uniformly smooth integral.
The hyperbola argument is A^2*B*u*v^2/(Y*s), with A^2*B/Y bounded.
Frequency xi=kY/(D*d1*B*A*q0) occurs as e(xi*s/(u*v)). Differentiating
u,v gives polynomial xi factors; integration by parts in compact s away
from zero offsets every such factor. Hence ALL mixed spatial derivatives
are uniformly bounded and the integral is Schwartz in xi. This proves,
rather than assumes, the smooth-coupling hypothesis of the model.

Truncate |xi| at R by Schwartz decay, paying an arbitrarily small fixed
power error; signs of k are separate. Then H_original<=D*R^2. Since
q0<=R*sqrt Y, use the model with Ystar=Y*R^2. Its prefactor is multiplied
by Y/Ystar, its frequency multiplier is Hstar<=D*R^4, and q0<=sqrt Ystar.
The physical relation A^2*B<=O(Y) places the boxes inside its hyperbola.
The slight extension bstar<1/5 is justified directly by the linear bound:
min(bstar,xstar)<1/5<31/128. For the rest the full model already applies.
Its nonzero target may be any polynomial-size integer: the proofs use m
only in divisor/gcd bounds, uniformly for 1<=|m|<=Ystar^O(1). Actual
m/Y stays in the fixed smooth support. q0=1 has no retained nonzero
frequency, since D*R^2*B*A/Y tends to zero; its Fourier tail is harmless.

Expand (M,m)=1 as sum_(l0|m,l0|M)mu(l0) in the NONZERO aggregate only.
Keep l0<=R. The joint period of e0|M,e|a,l0|M and the conductor masks is
at most D*R^3; allow the conservative bound J<=D*R^5. Five indices
e0,e,d1,d2,l0<=R cost at most R^5 by triangle. No other divisor index is
unaccounted for. Every term retains (M*a,q0)=1, even when (M,m)>1.

For the omitted l0>R terms, bound physical divisor weights by a fixed
power of tau BEFORE taking an R^3 triangle over the sieve indices. Their
untransformed total is at most
  Y^(1+epsilon)*sum_(l0|m,l0>R)1/l0<=Y^(1-rho+epsilon).
Indeed there are O(B/l0) multiples in a dyadic M interval whenever it is
nonempty, and O(Y/B) q values. For its zero-mode counterpart, absolute
harmonic sums over a,c and sum_(d1,d2<=R)1/(d1*d2) cost only Y^epsilon;
the physical e|a sum and sigma(M) are divisor bounded. The normalized
character average is<=1. Thus |nonzero|<=|whole|+|zero| gives the SAME
tail bound, with no power R loss. This restores exact gcd in(8).

Since D=Y^o(1), Hstar,J<=Ystar^(1/4096) eventually at rho=2^-20.
The full-model contribution, including five indices and the prefactor,
has exponent at most
  1-(1+2*rho)/4096+5*rho+epsilon < 1-rho.                    (12)
All fixed smooth partitions/logs and conductor costs fit epsilon. Take
epsilon sufficiently small compared with rho; the gcd tail and every
nonzero error are O(Y^(1-rho/2+o(1))).

V. Reassess the claimed gain, and retain the unresolved question.
Combine the unchanged small-M theorem with(7),(10),(12). Its earlier
Y^(1-theta+o(1)) error is absorbed into Y*eta^-20 for each FIXED theta;
we do not require theta>=rho/2. Here eta=Y^o(1),
t=Y^-o(1), S_2(m)<<log eta, and t<=1/sqrt(eta*log D). Therefore (1) is
o(Y*t), uniformly for arbitrary original rough subsets. For a fixed
polynomial kernel, |K_f(n)|<<_(f,theta)L and log q is comparable to L,
so the corresponding even-class absolute loss with M<=Y^(13/25) is also
o_(f,theta)(Y*t), in THIS actual-zero large-V regime.
The prior formal identity still reproduces the known main term only.
The signed boundary-minus-discrepancy estimate, other composite classes,
and any positive lower bound for the full total remain open. No discarded
method budget is a no-go theorem for its useful polynomial components.

Finite tests below check algebra, cutoffs, masks and exponent accounting;
they do not experimentally prove any infinite prime or zero statement.
"""
from fractions import Fraction as F
from math import gcd, isqrt, lcm, prod


RHO = F(1, 2**20)


def _positive(n, name):
    if type(n) is not int or n < 1:
        raise ValueError(f'{name} must be a positive integer')


def primes_below(cutoff):
    _positive(cutoff, 'cutoff')
    return tuple(n for n in range(2, cutoff)
                 if all(n % d for d in range(2, isqrt(n)+1)))


def upper_beta_data(level, cutoff, beta):
    """Finite upper weights and first failed odd prefixes; strict inequalities."""
    for n, name in ((level, 'level'), (cutoff, 'cutoff'), (beta, 'beta')):
        _positive(n, name)
    if level <= 1 or beta < 2:
        raise ValueError('require level>1 and beta>=2')
    primes = tuple(reversed(primes_below(cutoff)))
    weights, failures = {1: 1}, []

    def visit(prefix, value, start):
        for index in range(start, len(primes)):
            p = primes[index]
            next_prefix, next_value = prefix+(p,), value*p
            if len(next_prefix) % 2 and next_value*p**beta >= level:
                failures.append(next_prefix)
            else:
                weights[next_value] = (-1)**len(next_prefix)
                visit(next_prefix, next_value, index+1)

    visit((), 1, 0)
    return weights, tuple(failures)


def pointwise_sieve_identity(n, level, cutoff, beta):
    """Return sigma, exact rough indicator, nonnegative first-failure sum."""
    _positive(n, 'n')
    weights, failures = upper_beta_data(level, cutoff, beta)
    primes = primes_below(cutoff)
    sigma = sum(value for d, value in weights.items() if n % d == 0)
    rough = int(all(n % p for p in primes))
    remainder = sum(n % prod(prefix) == 0
                    and all(n % p for p in primes if p < prefix[-1])
                    for prefix in failures)
    return sigma, rough, remainder


def euler_sieve_identity(level, cutoff, beta, values=None):
    """Exact finite Euler sums for supplied prime densities in[0,1]."""
    primes = primes_below(cutoff)
    densities = {p: F(1, p) for p in primes} if values is None else dict(values)
    if set(densities) != set(primes) or any(type(v) not in (int, F)
            or not 0 <= v <= 1 for v in densities.values()):
        raise ValueError('supply exact densities in[0,1] for every cutoff prime')
    weights, failures = upper_beta_data(level, cutoff, beta)
    total = sum((coefficient*prod(densities[p] for p in primes if d % p == 0)
                 for d, coefficient in weights.items()), F(0))
    euler = prod((1-densities[p] for p in primes), start=F(1))
    remainder = sum((prod(densities[p] for p in prefix)
                     *prod(1-densities[p] for p in primes if p < prefix[-1])
                     for prefix in failures), F(0))
    return total, euler, remainder


def weighted_progression_identity(start, ell, coefficients):
    """Finite Euler family: exact count, divisor count, density, floor budget.

    coefficients maps primes to nonnegative rational c_p; includes ell with
    prime powers or primes outside that family. This is a finite guard for
    the lcm identity behind (6), not a claim of its infinite error constant.
    """
    _positive(start, 'start')
    _positive(ell, 'ell')
    cp = dict(coefficients)
    if any(type(p) is not int or p < 2 or any(p % d == 0
            for d in range(2, isqrt(p)+1)) or type(c) not in (int, F) or c < 0
            for p, c in cp.items()):
        raise ValueError('require prime keys and nonnegative exact coefficients')
    cp = {p: F(c) for p, c in cp.items()}
    divisors = {1: F(1)}
    for p, c in cp.items():
        divisors.update({d*p: f*c for d, f in tuple(divisors.items())})
    direct = sum((prod((1+c for p, c in cp.items() if n % p == 0), start=F(1))
                  for n in range(start, 2*start) if n % ell == 0), F(0))
    expanded = sum((f*((2*start-1)//lcm(d, ell)-(start-1)//lcm(d, ell))
                    for d, f in divisors.items()), F(0))
    density = F(1, ell)*prod((1+c/p for p, c in cp.items()), start=F(1))
    density *= prod(((1+c)/(1+c/p) for p, c in cp.items() if ell % p == 0), start=F(1))
    return direct, expanded, density, sum(divisors.values(), F(0))


def affine_inverse_phase(conductor, d1, cofactor, small, modulus, target, frequency):
    """Integer phase numerator in(11); reject any missing native unit mask."""
    for n, name in ((conductor, 'conductor'), (d1, 'd1'), (cofactor, 'cofactor'),
                    (small, 'small'), (modulus, 'modulus')):
        _positive(n, name)
    if modulus < 2 or gcd(conductor*d1*cofactor*small, modulus) != 1:
        raise ValueError('require all inverse factors to be modulus units')
    if type(target) is not int or type(frequency) is not int:
        raise ValueError('target and frequency must be integers')
    return -target*frequency*pow(conductor*d1*cofactor*small, -1, modulus) % modulus


def transfer_budget(rho=RHO):
    """Exact cap and saving margins, reserving positive room for D=Y^o(1)."""
    if type(rho) is not F or rho <= 0:
        raise ValueError('rho must be a positive exact Fraction')
    scale = 1+2*rho
    return {'frequency_margin': scale/4096-4*rho,
            'period_margin': scale/4096-5*rho,
            'model_exponent': 1-scale/4096+5*rho,
            'gcd_tail_exponent': 1-rho,
            'claimed_exponent': 1-rho/2,
            'harmonic_error_exponent': rho-F(1, 10),
            'unit_modulus_frequency_exponent': F(19, 25)-1+2*rho}
