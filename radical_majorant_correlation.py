"""Corrected radical-majorant correlations and finite local-density checks.

Owner: Kevin's research. Purpose: control the error when the signed Fourier
model in major_arc_kernel.py is used in an additive pair count. The rational
helpers below test the local algebra; they do not certify asymptotic constants.
Sol checked the proof, convolution consequences, and finite verifier on
2026-09-08. Four focused tests passed normally and with Python -O.

Notation and theorem (Y sufficiently large):
Let 2<=R<=Y/2, d=log(R)/log(Y), I=(Y/2,Y], and
  a_t(p)=2*min(1,t*log(p)/log(R)),
  w_t(n)=product_{p|n} a_t(p),  w_t(1)=1,
  H(n)=log(R)*integral_R w_{10*(1+|xi|)}(n)/(1+|xi|)**10 dxi.
Thus H is exactly the corrected H_R(rad(n)), not a squarefree-supported
function. Uniformly in R and even m in [5Y/4,7Y/4],
  sum_{n in I} H(n) << Y/d,
  sum_{n in I} H(n)**2 << Y*log(Y)/d**2,
  sum_{n in I} H(n)*H(m-n) << Y*S_2(m)/d**2.                 (1)
Here S_2(m)=2*product_{p>2}(1-1/(p-1)**2)
                 *product_{p|m,p>2}(p-1)/(p-2).
Restricting the last sum to m-n in I only decreases it. Constants and the
onset are not numerical; no lower bound or Goldbach coverage follows.

Source prerequisite:
Use Kevin Henriot's NEW Theorem 5 in the 2014 erratum, pp.375-377, to
"Nair--Tenenbaum bounds uniform with respect to the discriminant" (2012).
It replaces the original rhohat by rhocheck. For selected prime powers
p**nu_i, a zero exponent is not always a vacuous condition: if any other
exponent is positive, a zero exponent requires p NOT dividing that form.
This is erratum (0.1)-(0.2). The correction D* -> a*D* in Corollaries 1-2
is not needed below: we use New Theorem 5 directly, and |a*|=1 anyway.
Primary sources:
https://arxiv.org/pdf/1102.1643 (original definitions and Theorem 5)
https://www.cambridge.org/core/services/aop-cambridge-core/content/view/
B0BD208D979495FE06B8192209E710EA/S0305004114000280a.pdf (erratum)

Proof of (1):
1. In New Theorem 5 take x=y=Y/2, Q1(u)=u, Q2(u)=m-u, and
   F(v,w)=w_t(v)*w_s(w), where t,s>=10. Both linear polynomials are
   primitive, Q=-u**2+m*u has coefficient L1 norm m+1=O(Y), and its
   discriminant is m**2. Choose the theorem's alpha=1/2, norm exponent
   eta=1/4, and epsilon=1/2000. Then its hypotheses x>=C0*||Q||**eta,
   x**alpha<y<=x, and epsilon<alpha/(50*g*(g+1/eta)), g=2, hold.
   F is multiplicative and belongs uniformly to M_2(2,B_epsilon,epsilon):
   F<=tau(v)*tau(w)<=B_epsilon*(v*w)**epsilon, while its prime-power
   bound is 2**Omega(v*w). The multiplicative ratio condition follows
   for coprime products even when F vanishes. No constant depends on t,s,R.

2. Drop the theorem's divisor-sum condition n1*n2<=x, retaining primes
   p<=x, and extend all valuations to infinity. All terms are nonnegative.
   The corrected local divisor sum is exactly
     K_p=1+(a_t(p)+a_s(p))/p,                  p not dividing m,
     K_p=1+a_t(p)*a_s(p)/p,                   p dividing m.       (2)
   For p not dividing m, the positive valuations of u and m-u cannot
   coexist and each partitions an event of density 1/p. For p dividing m,
   exactly one positive valuation is forbidden by rhocheck; the pairs of
   positive valuations partition p|u, again of density 1/p. The all-zero
   divisor tuple contributes 1, without a nondivisibility restriction.
   The finite prime product converges after extending its valuations.
   Since 0<=a,b<=2 implies ab<=a+b, every K_p<=exp((a+b)/p).

3. Uniformly for t>=10,
     exp(sum_{p<=x} a_t(p)/p) << (t/d)**2.                    (3)
   If U=R**(1/t)>=2, split at U. The lower sum is O(1), using
   sum_{p<=U} log(p)/p=O(log U); the upper sum is
   2*log(log x/log U)+O(1) by Mertens. If U<2, use the all-prime bound
   exp(2*sum_{p<=x}1/p)<<log(x)**2 and t/d>log(Y)/log(2).
   Here U<x because R<=Y/2 and t>=10. Also
     product_{2<p<=x}(1-rho_Q(p)/p) << S_2(m)/log(Y)**2,
   since rho_Q(p)=2-1_{p|m}; the truncated factors at p|m are bounded
   above by those in the full positive singular series.
   Combining New Theorem 5, (2), and (3) gives
     sum_{n in I} w_t(n)*w_s(m-n)
       << Y*S_2(m)/log(Y)**2 * d**(-4)*t**2*s**2.
   Tonelli and the finite second moments against (1+|xi|)**(-10),
   multiplied by log(R)**2, prove the pair estimate in (1).

4. For Q(u)=u the same theorem (g=1 and the same fixed parameters)
   gives sum_I w_t <<Y/log(Y)*(t/d)**2: its local divisor sum is
   1+a_t(p)/p and its sieve product is O(1/log Y). Integrating proves
   the first estimate. For w_t**2 the uniform class bound is now supplied
   by tau(n)**2 and A=4. Its local coefficient a_t(p)**2<=2*a_t(p),
   so sum_I w_t**2 <<Y/log(Y)*(t/d)**4. Cauchy--Schwarz in xi with
   measure dxi/(1+|xi|)**10, whose mass is 2/9, then proves the second
   estimate in (1). All integrals used have finite second/fourth moments.

Convolution consequence for the actual normalized rough-semiprime weight:
Take f,M,E,R,Y and error accuracy e from major_arc_kernel.py; extend the
functions by zero outside I. Then |M|<<_G H, |E|<<_G e*H, and
  |[(M+E)*(M+E)-M*M](m)|
       <<_G e*(1+e)*d**(-2)*Y*S_2(m)                         (4)
for every central even m. This is the triangle inequality and (1).
Put V=f-M-E and Q=f*f-(M+E)*(M+E)=V*(f+M+E). Parseval and the already
checked ||Vhat||_infinity<<_G Y*R**(-1/3) give
  sum_m |Q(m)|**2 <<_G Y**3*R**(-2/3)
                  *[log(Y)**2+(1+e)**2*log(Y)*d**(-2)].      (5)
Here ||f||_2**2<<Y*log(Y)**2 follows from its pointwise bound, and
the H second moment controls M+E. No pointwise bound for V is assumed.

In the existing Fourier-model range exp(log(Y)**(4/5))<=R<=Y**(1/400),
one has d>=log(Y)**(-1/5). Also e=O(1): this is immediate in the
unexceptional case; in the exceptional case, Definition 7.1 of
arXiv:2508.16400v2 at level R**4 gives
  (1-beta)*log Y<=kappa/(4*d),
and e<=(kappa/(4*d))*exp(-c/d). Consequently (5) implies that outside
O_G(Y*R**(-1/2)) integer targets,
  |Q(m)|<=Y/log(Y)**3.
Indeed the exceptional count is O_G(Y*R**(-2/3)*log(Y)**8), and the
extra logarithmic factor is absorbed by R**(1/6). Together with (4),
this bounds f*f-M*M by the right side of (4) plus Y/log(Y)**3 outside
that set. This is a signed-model comparison, not a positivity theorem.
It neither removes the possible exceptional targets nor proves that the
error is small relative to an exceptionally suppressed main term.
"""
from fractions import Fraction
from math import isqrt


def _check_inputs(p: int, target: int, a: int | Fraction, b: int | Fraction):
    if type(p) is not int or p < 2 or any(p % d == 0 for d in range(2, isqrt(p)+1)):
        raise ValueError("p must be prime")
    if type(target) is not int:
        raise ValueError("target must be an integer")
    if any(type(c) not in (int, Fraction) or not 0 <= c <= 2 for c in (a, b)):
        raise ValueError("local coefficients must be exact rationals in [0,2]")


def local_divisor_factor(p: int, target: int,
                         a: int | Fraction, b: int | Fraction) -> Fraction:
    """Full corrected local divisor sum for u and target-u.

    a,b are the constant positive-prime-power values, supplied exactly.
    This finite algebra does not certify the asymptotic correlation theorem.
    """
    _check_inputs(p, target, a, b)
    return 1+Fraction(a*b if target % p == 0 else a+b, p)


def truncated_local_divisor_factor(p: int, target: int,
                                   a: int | Fraction, b: int | Fraction,
                                   depth: int) -> Fraction:
    """Enumerate corrected local tuples with exponents at most depth.

    The all-zero tuple contributes 1. For any other tuple, all valuations,
    including zeros, must match. Enumerating residues modulo p**(depth+1)
    makes the test exact, including repeated factors and coincident roots.
    This deliberately small verifier refuses more than 100000 residues.
    """
    _check_inputs(p, target, a, b)
    if type(depth) is not int or depth < 0 or depth > 16 or p**(depth+1) > 100000:
        raise ValueError("require nonnegative depth with at most 100000 residues")
    modulus = p**(depth+1)

    def capped_valuation(n):
        exponent = 0
        while exponent <= depth and n % p == 0:
            n //= p
            exponent += 1
        return exponent

    total = Fraction(0)
    for n in range(modulus):
        first = capped_valuation(n)
        second = capped_valuation((target-n) % modulus)
        if first > depth or second > depth or first == second == 0:
            continue
        total += (a if first else 1)*(b if second else 1)
    return 1+total/modulus
