"""A valid comparison sequence, and the limits of a near-half sieve import.

Owner: Kevin's Goldbach research. Purpose: test an actual application of
Ford--Maynard's prime-producing framework. This preserves a proved model
regularity lemma and exact failed-import conditions; actual Type II is OPEN.

COMPARISON, GROWTH, AND FIXED DIVISOR WEIGHTS.
1. Reuse composite_bilinear_bridge.py, with N=2x, L=logx, I=(x/2,x],
   y=floor(exp(sqrtL)), c_y=product_(ell<=y prime)(1-1/ell)^(-1), and
    a_n=Lambda(N-n), b_n=c_y 1_((N-n,P(y))=1), w_n=a_n-b_n
   on I, zero outside. All assertions below are uniform in this N=2x.
   The saved fundamental lemma/Bombieri--Vinogradov proof gives, for every
   fixed gamma<1/2 and A>0, sum_(d<=x^gamma)Delta_d <<_A x/L^A, with
   Delta_d=max_J |sum_(dk in I,k in J)w_(dk)|, and
    sum_(n in I)Lambda(n)b_n=(1+o(1))S_2(N)x/2.
   Do not replace b by a in either the model main or factor statistics.
2. Here |w_n|<<L, w_n>=-c_y, and c_y<<sqrtL. Hence
    sum |w_n|tau(n)<<xL^2, w_n>=-x^(nu/10)
   for every fixed nu>0 and large x. The source growth condition holds
   with its parameter varpi=3. Also Delta_d<<Lx/d for d<=x^gamma.
   For every FIXED positive integer B, tau(d)^(2B)<=tau_(4^B)(d), so
    sum tau(d)^(2B)Delta_d << x L^(4^B+1).
   Cauchy with the saved arbitrarily strong unweighted TI therefore gives
    sum_(d<=x^gamma)tau(d)^B Delta_d <<_(A,B,gamma) x/L^A. (1)
   This is an application of the saved fixed-divisor-weight argument to
   this simpler nonnegative comparison, not a new distribution level.

THE COMPARISON DOES SATISFY THE FACTOR-PATTERN HYPOTHESES.
3. Put B_P=sum_(p in I prime)b_p. Removing proper prime powers from the
   saved model main costs O(c_y sqrtx L). Since logp=L+O(1) on I,
    B_P=(1+o(1))S_2(N)x/(2L).                            (2)
   In particular B_P>=x/L^3 for all large x: source(b.1) holds.
4. Fix nu>0, 2<=k<=1/nu, and any convex T in the ordered simplex
    u1+...+uk=1, nu<=u1<=...<=uk.
   For any real f on T with |f|<=1 and Lipschitz constant<=1, we have,
   UNIFORMLY in T and f,
    sum_(n=p1...pk in I,p1<=...<=pk,v(n) in T)b_n f(v(n))
      = B_P [integral_T f(u)du/(u1...uk)+o_(nu,k)(1)].     (3)
   Integrals use projection onto the first k-1 coordinates, as in the
   source. Thus its(b.2), with error<=1/B for any fixed B eventually,
   holds on every required subset of C(R), without assuming actual II.
5. Proof of the arithmetic transfer in(3). Each prime factor exceeds
   (x/2)^nu, hence y eventually. Fix p1,...,p_(k-1), put M=their product,
   and vary the last prime t on scale Z=x/M>=(x/2)^nu. For every ell<=y,
   M is a unit modulo ell. Among prime residues t, the forbidden residue
   N/M is reduced when ell does not divide N, giving local density
   g(ell)=1/(ell-1); when ell divides N the residue is0 and g(ell)=0.
   Thus the local sieve product V_N(y)=product_(ell<=y)(1-g(ell)) is
   independent of M, EXACTLY the same product as for B_P.
   Choose sieve level D=x^(nu/4). For all such Z it is below
   Z^(1/2)/log^K Z for every fixed K eventually. BV with maxima over
   residues and endpoints controls the summed progression errors uniformly
   in M and N. The fundamental-lemma parameter logD/logy is comparable
   to sqrtL, so its relative error beats every fixed logarithmic power.
   Multiplication by c_y and all local-product factors is absorbed by
   requesting larger fixed savings. Consequently, on ANY last-prime
   interval J inside the physical support,
    sum_(t prime in J)b_(Mt)
      = c_y V_N(y) #{t prime in J}+O_A(Z/L^A).            (4)
   This error uses Z, not the possibly short length of J.
6. The normalized vector
    v(Mt)=(logp1/(logM+logt),...,logt/(logM+logt))
   traces a straight line as 1/log(Mt) varies. Convex T therefore cuts
   out an interval of t. The ordering constraints also cut out intervals.
   A Lipschitz f has bounded variation along that line, so Abel applies
   (4) with its weight. Finally
    sum_(p1,...,p_(k-1)>= (x/2)^nu)1/M
       <= (sum_((x/2)^nu<=p<=x)1/p)^(k-1)=O_(nu,k)(1).
   Summing the errors in(4) gives O_A(x/L^A), not a factor equal to the
   number of tuples. Thus the left side of(3) equals c_y V_N(y) times
   the UNWEIGHTED prime-factor-pattern sum, plus this all-log error.
   Large prime factors of N are not removed by this comparison sieve;
   no uniformity in a residue modulo their product is being assumed.
7. Ordinary multidimensional PNT gives the unweighted sum as
    (x/(2L))[integral_T f(u)du/(u1...uk)+o_(nu,k)(1)].
   For a convex polytope this follows from source Lemma5.11 with t=0,
   eta=min(nu/2,1/4), c=1/2,d=1 and radial integration: the radial
   integral is integral_(x/2)^x dt/logt=(1+O(1/L))x/(2L).
   For arbitrary convex T, approximate its projection by a fixed mesh
   depending on nu,k and the desired error. Lemma5.9 bounds boundary
   cells uniformly by O_(nu,k)(mesh). The density is bounded because
   all coordinates>=nu; Lipschitz variation has the same mesh bound.
   Apply the polytope result to interior/boundary cells, then let the mesh
   decrease. This proves a uniform o(1), not an unstated rate for all T.
   Repeated-prime diagonals are negligible: their count is at most
   sum_(p>=(x/2)^nu,p<=sqrtx)floor(x/p^2)=O(x^(1-nu)); their b mass is
   O(c_y x^(1-nu)). Ordered distinct factors require no extra k!.
   Since c_y V_N(y)=(1+o(1))S_2(N), combining with(2) proves(3).

WHY THESE VALID INPUTS DO NOT YET GIVE A POSITIVE PRIME BOUND.
8. A Type II bound is still an ADDITIONAL arithmetic input: for arbitrary
   coefficients |alpha_d|<=tau(d)^B, |beta_j|<=tau(j)^B it asks for
    |sum_((x/2)^theta<d<=x^(theta+nu),dj in I)
                    alpha_d beta_j w_(dj)| <= x/L^B.     (5)
   The existing good-factor-modulus result does not estimate(5) for all
   factors and coefficients. Its coefficients cannot be renamed to do so.
   Also, a numerical range just below1/2 cannot be treated as reaching it.
   Here is a CORRECTED explicit comparison-class example in a relevant
   restricted geometry; it is not the actual prime-partner sequence.
9. Fix 0<gamma<1/2 and theta>=0, nu>0 with theta+nu<gamma. Choose
   gamma<a<b<1/2 and let, for x/2<t<=x,
    K_x(t)=log[b(logt-aL)/(a(logt-bL))].
   It is positive and bounded above/below for large x. Define
    w_p^*=-1 at primes p,
    w_(pr)^*=1/K_x(pr) if p,r prime and x^a<=p<=x^b,
    w_n^*=0 otherwise, b_n^*=1, a_n^*=1+w_n^*.
   The smaller factor p is unique, since b<1/2 and pr>x/2. Both factors
   exceed x^gamma eventually. Therefore every TI term with 2<=d<=x^gamma
   is exactly0. Every II term in(5) is also0: d>1 and d<=x^(theta+nu)
   cannot divide a supported index. This includes theta=0, where d=1
   must remain excluded as in the source definition.
   The d=1 interval sum is O_A(x/L^A). Strong PNT twice and Abel give
   the semiprime continuous density, at total argument t,
    integral_(x^a)^(x^b)du/[u logu log(t/u)]
       =K_x(t)/logt.
   The weight1/K_x(t) makes this exactly the prime density1/logt.
   Uniform interval PNT errors are all-log small; K_x and its derivatives
   have fixed bounds after scaling. Thus this bounded nonnegative a^*
   satisfies I, II and growth but has a_p^*=0 at EVERY prime. The flat b^*
   meets(b.1)/(b.2) by the same ordinary PNT used above. This blocks a
   generic positive lower certificate in this parameter geometry only.
10. Source correction: the author PDF, printed p17, proof of Theorem4.16,
   says w_n=1 otherwise while claiming those sums vanish. That must be0
   for this construction. In addition, the printed CONSTANT K=K_x(x)
   does not give an all-log d=1 error on the fixed x-exponent band. Put
    K(r)=log[b(r-a)/(a(r-b))], K'(1)=(a-b)/((1-a)(1-b)).
   The remaining full-I sum with constant weight1/K(1) is
    [K'(1)/K(1)]*(log2-1)/2 * x/L^2 + O(x/L^3),          (6)
   with POSITIVE nonzero coefficient. This follows by Taylor expansion
   K(1+logv/L) and integral_(1/2)^1 logv dv=(log2-1)/2.
   The t-dependent normalization in step9 repairs this secondary term.
   We use that proved restricted construction, not the literal printed
   proof or an unrestricted reading of the source's reduction parameters.

THE BOUNDED-VARIANT NORMALIZATION CANNOT BE IMPORTED EITHER.
11. Source equation(4.1) requires BOTH |w_n|<=tau(n)^rho for fixed rho
   AND B_P>=x/(rho L). For our actual sequence take x=p prime, N=2p and
   n=p. Then b_p=c_y and w_p=logp-c_y~logp, whereas tau(p)^rho=2^rho.
   Thus fixed divisor boundedness fails uniformly for this family.
   No positive common scalar t_x fixes both requirements: bounding this
   entry forces t_x=O_rho(1/L); since S_2(2p) tends to a positive constant,
   (2) then gives t_x B_P=O_rho(x/L^2)<x/(rho L). This includes the
   proposed divide-by-logx normalization. It does not rule out a different
   comparison or a new theorem using other quantitative hypotheses.

DISPOSITION AND PRIMARY SOURCES.
The model's factor-pattern regularity is now PROVED, using existing
distribution tools. This closes a previously unverified framework input.
Actual II remains open. Within the safe geometry theta+nu<gamma<1/2,
even granting II cannot give a generic positive constant; use actual extra
arithmetic structure, a different region, or a genuinely applicable stronger
hypothesis. Retain polynomial tools and the exceptional-character correction
in composite_bilinear_bridge.py; an uncorrected prime asymptotic is stronger
than positivity and cannot be silently imposed. No new Goldbach coverage.
The companion critical_factor_mass.py now supplies one such ACTUAL extra
ingredient: a uniform small-mass bound on the near-critical composite region.
Combined with the still-unproved Type II input in its specified window,
it yields a conditional positive lower bound without source equation(4.1).

Ford--Maynard, On the theory of prime-producing sieves, author PDF dated
July16,2024, read2026-09-09: I/II p2, growth p3, equations(b.1)/(b.2) p12,
equation(4.1) and Definitions4.7-4.9 p13, Thm2.5 p7, Lemmas5.9/5.11
p24-25; the two literal proof issues on p17 are corrected in steps9-10.
https://www.ford126.web.illinois.edu/wwwpapers/prime-producing-sieves.pdf
Its Theorem2.2(A1) has n>=M+1, verified in the actual PDF text; the web
extraction rendered that comparison misleadingly. No new use of A1 here.
Ford, Sieve Methods2023, Theorem3.4(BV) and3.6(fundamental lemma),
the already checked inputs in composite_bilinear_bridge.py:
https://ford126.web.illinois.edu/sieve2023.pdf

Finite helpers below guard local densities, normalized-coordinate geometry,
and the two normalization calculations. They do not test asymptotic II.
"""
from fractions import Fraction as F
from math import gcd

from factored_linear_barrier import log_enclosure
from redistribution import trial_prime


def prime_partner_local_density(target, multiplier, prime):
    """Exact surviving prime residues and their predicted proportion."""
    if (any(type(v) is not int or v <= 0 for v in (target, multiplier, prime))
            or not trial_prime(prime) or gcd(multiplier, prime) != 1):
        raise ValueError('positive integers, prime modulus, and unit multiplier required')
    survivors = sum((target-multiplier*r) % prime != 0 for r in range(1, prime))
    predicted = F(1) if target % prime == 0 else F(prime-2, prime-1)
    return F(survivors, prime-1), predicted


def normalized_ray_interval(fixed_logs, free_interval, halfspaces):
    """Intersect normalized-factor halfspaces; return free-log interval.

    Rational log coordinates are algebra fixtures, not certified logarithms.
    Each halfspace is(coefficients,bound), meaning dot(c,v)<=bound.
    """
    rational = lambda x: type(x) in (int, F)
    if (not fixed_logs or any(not rational(a) or a <= 0 for a in fixed_logs)
            or len(free_interval) != 2 or any(not rational(t) for t in free_interval)
            or not 0 < free_interval[0] <= free_interval[1]):
        raise ValueError('positive rational fixed logs and ordered positive interval required')
    lower, upper = map(F, free_interval)
    total = sum(fixed_logs)
    for coefficients, bound in halfspaces:
        if (len(coefficients) != len(fixed_logs)+1 or not rational(bound)
                or any(not rational(c) for c in coefficients)):
            raise ValueError('rational halfspace in the full factor dimension required')
        slope = coefficients[-1]-bound
        intercept = bound*total-sum(c*a for c, a in zip(coefficients, fixed_logs))
        if slope > 0:
            upper = min(upper, F(intercept)/slope)
        elif slope < 0:
            lower = max(lower, F(intercept)/slope)
        elif intercept < 0:
            return None
        if lower > upper:
            return None
    return lower, upper


def band_normalization(a, b, radial_exponent=1):
    """Exact log argument and derivative for K(r); no floating logarithms."""
    if (any(type(v) not in (int, F) for v in (a, b, radial_exponent))
            or not 0 < a < b < F(1, 2) or radial_exponent <= b):
        raise ValueError('require rational0<a<b<1/2 and radial exponent>b')
    a, b, r = map(F, (a, b, radial_exponent))
    return b*(r-a)/(a*(r-b)), (a-b)/((r-a)*(r-b))


def constant_band_error(a, b):
    """Certified coefficient interval in(6); require its log argument<=2."""
    ratio, derivative = band_normalization(a, b)
    k_low, k_high = log_enclosure(ratio)
    l_low, l_high = log_enclosure(2)
    return derivative*(l_high-1)/(2*k_high), derivative*(l_low-1)/(2*k_low)


def common_scaling_interval(log_x, c_y, relative_prime_mass, rho):
    """Necessary scalar bounds for(4.1), with relative mass=B_P logx/x."""
    if (any(type(v) not in (int, F) for v in (log_x, c_y, relative_prime_mass))
            or not 0 < c_y < log_x or relative_prime_mass <= 0
            or type(rho) is not int or rho < 1):
        raise ValueError('positive rational inputs, logx>c_y, and positive integer rho required')
    return F(1, rho)/relative_prime_mass, F(2**rho)/(log_x-c_y)
