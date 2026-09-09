"""Actual fixed-power rough localization for a polynomial sieve coefficient.

Owner: Kevin's Goldbach research. Purpose: pair the preserved polynomial
weight with a joint arithmetic majorant, and test whether small-prime
removal can be paid at prime-count precision. This is an ALTERNATIVE
exact sieve coefficient, not an estimate for the old hard H or M_e.

SETUP AND STATEMENT.
Let N=2x, I=(x/2,x], L=logx, y=floor(exp(sqrtL)), and keep
 a_n=Lambda(N-n), b_n=c_y 1_(P^-(N-n)>y), w_n=a_n-b_n,
 c_y=product_(ell<=y)(1-1/ell)^(-1), B_P~S_2(N)x/(2L).
Fix 0<gamma<1/2, an integer k>=9, V=x^gamma, and put
 T_k(n)=sum_(d|n)mu(d)(1-logd/logV)_+^k.
There is NO smooth-prime restriction on d. For 0<kappa<=1/20, z=x^kappa,
 sum_(n in I,P^-(n)<=z) |T_k(n)w_n|
   <<_(gamma,k) (kappa+1/L) S_2(N)x/L + O_A(x/L^A).       (1)
The leading constant is independent of kappa in this interval. The
arbitrarily strong error can have an onset depending on fixed parameters.
Thus small primes cost an arbitrarily small fraction of B_P by choosing
kappa first and then x sufficiently large. The factor S_2(N) is essential
to the stated bound; this is not a uniform delta*x/L claim without it.

PROOF: NORMALIZATION AND EXCEPTIONAL SUPPORT.
1. The saved polynomial_joint_majorant.py proves pointwise
 |T_k(n)| <= C_k H_V(n)/logV,
 H_V(n)=logV int_R W_(10(1+|u|),V)(n)/(1+|u|)^10 du,
 W_(t,V)(n)=product_(ell|n) a_t(ell),
 a_t(ell)=2min(1,t logell/logV).
This product is over DISTINCT factors, including on prime powers. Also
|T_k(n)|<=tau(n). All constants below may depend on fixed gamma,k.

2. We first remove gcd(n,N)>1 at actual all-log cost. For a common prime
ell<=y, b_n=0; a_n can be nonzero only when N-n is a proper prime power.
Indeed N-n>=x>y. All proper powers in [x,3x/2) number O(sqrtx logx);
|w_n T_k(n)|<<L tau(n)<<_eta L x^eta on this support (b=0).
For common ell>y, the crude bound and tau(ell*m)<=2tau(m) give
 << xL^2 sum_(ell|N,ell>y)1/ell << xL^3/(y logy).
Both are all-log small. This argument does NOT first assume n y-rough.

3. Set theta=1/10. If p<=z divides n, write n=p^j m with p not dividing
m, retaining its EXACT exponent j>=1. Pairs with p^j>x^theta have total
count at most
 x sum_(p<=z) sum_(j:p^j>x^theta) p^(-j) <= 2x^(1-theta+kappa).
Here each geometric tail is <=2x^(-theta), and there are <=x^kappa
choices of p. With |wT_k|<<_eta Lx^eta and eta=theta/4, their absolute
cost is O(x^(39/40)L), uniformly for kappa<=theta/2. Thus only
q=p^j<=x^theta, p not dividing N, need the joint arithmetic bound.

THE JOINT ESTIMATE RETAINS A SMALL-PRIME FACTOR.
4. On n=qm, (p,m)=1, radical multiplicativity gives EXACTLY
 W_(t,V)(qm)=a_t(p) W_(t,V)(m).
Extract this factor before dropping (p,m)=1 by positivity. In particular
a_t(p)<=2t logp/logV. Dropping this factor would lose the saving in (1).
The exact m interval is (X,2X], X=x/(2q)>=x^(9/10)/2. Its reflected
argument N-qm lies in [x,3x/2). Apply the corrected NEW Theorem5 of
Henriot (2014 erratum) to the primitive forms m and N-qm. Their product
has degree2, coefficient norm N+q<=3x, discriminant N^2 and no fixed
prime divisor. Indeed p does not divide N and N is even, so p is odd.
Use alpha=1/2, norm exponent eta_source=1/4, epsilon_source=1/2000.
Then X>=C||Q||^(1/4), X^alpha<X, and
epsilon_source<alpha/[50*2*(2+1/eta_source)]=1/1200.
Also V<X/2 eventually, uniformly q<=x^theta, since gamma<1/2.

5. Write a=a_t(ell), and let b be the second multiplicative function's
positive-prime-power value at ell, with 0<=b<=2. The corrected local
divisor factors, using EXACT valuations and the nonvacuous zero slots,
are the same as in polynomial_joint_majorant.py:
 ell not dividing pN: rho=2, K=1+(a+b)/ell;
 ell dividing N:      rho=1, K=1+ab/ell;
 ell=p:               rho=1, K=1+a/ell.
The exponent j does not change these cases. All K<=exp((a+b)/ell).
The extra sieve factor at ell=p is at most (p-1)/(p-2)<=2, so the
sieve product is <<S_2(N)/log(X)^2, uniformly in p,j,N.

6. For the ACTUAL Lambda term take an auxiliary R=x^(1/4800).
The saved pointwise prime-power majorant gives Lambda(h)<<H_R(h)
for h<=3x/2; enlarging its fixed constant pays this physical range.
For b=a_s,R(ell), the saved Mertens split gives
 product K <<_(gamma) t^2 s^2,
since logV/logX and logR/logX stay bounded above and away from zero.
Both functions belong uniformly to the same M_2(2,B,epsilon) class.
The source therefore bounds their joint m-sum by
 << (x/q) S_2(N) t^2 s^2/L^2.
Multiply by the extracted a_t(p), the two majorant prefactors logV*logR,
and the polynomial factor 1/logV; then integrate. The required moments
are order3 in t and order2 in s, finite against the saved power10 kernels.
Consequently
 sum_(n in I,p^j||n,(n,N)=1) |T_k(n)|a_n
       << (x/p^j) S_2(N)/L * (logp/L),                  (2)
uniformly in p^j<=x^theta. Constants include the fixed choice of R.

7. Pay the NONNEGATIVE comparison separately, rather than treating it
as an H_R majorant. Use F_2(h)=1_(P^-(h)>y). Its positive-power values
are b=0 for ell<=y and b=1 for ell>y, uniformly in the same function class.
Now
 product_(ell<=X) K_ell <<_(gamma) t^2 * logX/logy.
This follows from the saved a_t split and Mertens for sum_(y<ell<=X)1/ell.
Multiplying the source bound by c_y<<logy cancels this denominator;
the polynomial prefactors logV and 1/logV cancel each other. Extract
a_t(p) and integrate its finite third moment as before. We obtain
 sum_(n in I,p^j||n,(n,N)=1) |T_k(n)|b_n
       << (x/p^j) S_2(N)/L * (logp/L).                  (3)
Thus both the actual prime weight and its saved comparison are paid at
the SAME normalization, with no unproved prime-pair asymptotic.

8. Sum (2)+(3) over all p<=z and all their exact exponents, using a
nonnegative union bound (overcounting different small divisors is safe).
The elementary weighted prime sum gives
 sum_(p<=z) sum_(j>=1) logp/p^j
       =sum_(p<=z)logp/(p-1) << logz+1 = kappa L+O(1).
Combine with steps2/3 to prove (1). In particular the small factor is
not hidden in a kappa-dependent implicit constant.

THE EXACT NEW REMAINDER, AND WHAT HAS NOT BEEN PROVED.
9. Its coefficients have |lambda_d|<=1 and support d<=V. The SAVED
Type I estimate implies sum_(n in I)T_k(n)w_n=O_A(x/L^A). For prime
n in I, n>V eventually, so T_k(n)=1. Therefore EXACTLY up to that error,
 sum_(n in I prime)a_n=B_P-sum_(n in I composite)T_k(n)w_n.
Use (1), step2 and the rough-squareful estimate
 L sum_(p>z)sum_(m<=x/p^2)tau(p^2m) << xL^2/z,
to obtain
 sum_(n in I prime)a_n = B_P-C_(k,kappa)(w)
       +O_(gamma,k)((kappa+1/L)S_2(N)x/L)+O_(A,kappa)(x/L^A), (4)
 C_(k,kappa)(w)=sum_(n in I composite,squarefree,(n,N)=1,P^-(n)>x^kappa)
                       T_k(n)w_n.
Each remaining n has STRICTLY fewer than 1/kappa prime factors. The
correlation is now a finite collection of prime-factor patterns, for
each fixed kappa. This is an analytic finiteness statement; no practical
small number of factors or numerical choice/onset is certified.

The signed C_(k,kappa) is OPEN. A bound on it with a fixed positive
margin below B_P would imply positivity after choosing kappa small enough.
The coefficient T_k can have either sign and is not the old H, M_e or
R_nu. For a small/large semiprime with exponent shares a<min(nu,gamma)
and 1-a>gamma, the old H is0 whereas T_k=1-(1-a/gamma)^k>0. These new
composite contributions MUST remain; the old hard-cutoff localization
has not been proved. The old fixed-sieve-parameter gap estimate alone
is insufficient, and its failure is not a lower bound on the actual error.

DISPOSITION: actual small-prime suppression for a preserved polynomial
tool paired with corrected joint arithmetic input. This is a different
exact sieve formulation with a quantified cost, not formal cancellation
of the missing prime correlation. No new Goldbach coverage or onset.

Sources: the pointwise polynomial proof and corrected Henriot application
are already checked in polynomial_joint_majorant.py and
radical_majorant_correlation.py. This proof rechecks the changed forms,
prime-power coefficient, comparison function and third-moment cost.
Henriot original definitions: https://arxiv.org/pdf/1102.1643
Authority is the NEW Theorem5 in the 2014 erratum, printedp377,
DOI10.1017/S0305004114000280; the original uncorrected statement is NOT
used. The blocked erratum route was not retried. Type I and B_P remain
those of prime_producing_comparison_gate.py, not a new distribution theorem.
Finite routines guard factor extraction, local cases and exact budgets;
they do not numerically prove (1), estimate C, or establish novelty.
"""
from fractions import Fraction as F
from math import ceil, gcd, prod

from major_arc_kernel import _factorization
from polynomial_joint_majorant import polynomial_cofactor_samples
from unexceptional_vaughan_gate import _positive


def localization_parameters(gamma, kappa):
    """Exact analytic exponent margins, not effective onset constants."""
    if type(gamma) is not F or not 0 < gamma < F(1, 2):
        raise ValueError('fixed rational 0<gamma<1/2 required')
    if type(kappa) is not F or not 0 < kappa <= F(1, 20):
        raise ValueError('fixed rational 0<kappa<=1/20 required')
    theta, eta = F(1, 10), F(1, 40)
    return {'theta': theta, 'tail_exponent': 1-theta+kappa+eta,
            'local_length_exponent': 1-theta,
            'cutoff_margin': 1-theta-gamma,
            'max_prime_factors': ceil(1/kappa)-1}


def kernel_moment(order):
    """Integral of [10(1+|u|)]^order/(1+|u|)^10 on the real line."""
    if type(order) is not int or not 0 <= order < 9:
        raise ValueError('finite moments require integer 0<=order<9')
    return F(2*10**order, 9-order)


def exact_prime_power_part(n, p):
    """Extract the entire p-power before applying radical multiplicativity."""
    _positive(n, 'n')
    if _factorization(p) != ((p, 1),):
        raise ValueError('p must be prime')
    q, m = 1, n
    while m % p == 0:
        q *= p
        m //= p
    return q, m


def radical_weight(n, local_values):
    """Finite exact stand-in for W; prime exponents are deliberately ignored."""
    _positive(n, 'n')
    return prod((F(local_values[p]) for p, _ in _factorization(n)), start=F(1))


def affine_local_case(ell, target, coefficient, a, b):
    """Corrected infinite-valuation factor for m,target-coefficient*m."""
    for value in (ell, target, coefficient):
        _positive(value, 'local input')
    if _factorization(ell) != ((ell, 1),) or gcd(target, coefficient) != 1:
        raise ValueError('require prime ell and primitive affine pair')
    if not 0 <= a <= 2 or not 0 <= b <= 2:
        raise ValueError('local weights must lie in [0,2]')
    if coefficient % ell == 0:
        return 1, 1+F(a, ell)
    if target % ell == 0:
        return 1, 1+F(a*b, ell)
    return 2, 1+F(a+b, ell)


def polynomial_factor_pattern(shares, gamma, degree):
    """Exact toy log shares; not numerical logarithms of asserted primes."""
    shares = tuple(shares)
    if not shares or sum(shares) != 1 or type(gamma) is not F or not 0 < gamma < 1:
        raise ValueError('positive shares summing to1 and rational gamma in(0,1)')
    return polynomial_cofactor_samples(tuple(s/gamma for s in shares), degree)
