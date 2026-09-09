"""Locate and bound the new composite terms of the alternative quintic weight.

Owner: Kevin's research. Purpose: test whether the polynomial with positive
endpoint main can inherit sufficient composite control. The required small
error is still unproved.
The exact helpers test formal factor weights and noninjective sieve indices;
they do not supply actual prime densities, zeros or numerical onsets.

Sol checked the theory and actual files. Five focused exact tests passed
normally and with Python -O; these verify factor algebra and sieve support.

Deduction independently checked by Sol:
Keep the actual-zero hypotheses, fixed epsilon<=1/100, sufficiently small
delta<=epsilon/3, fixed large u and B_good of balanced_semiprime_budget.py.
Write theta=delta/u, L=log(Y), R=floor(Y^(.5-2epsilon)), and fix kappa>0.
The alternative family is
  f(s)=s-kappa*s^2*(1-s)^2*(1-2s).
Let T_f=sum_{p in B_good}log(p)*K_f(m-p), with K_f as in log_weight_barrier.py.
Its endpoint-main coefficient is1, but its FULL signed total is not known
positive. No new prime-pair coverage is asserted below.

Absolute error reductions valid for ANY fixed polynomial:
1. On z-rough n<=Y, tau(n)<=2^(1/theta), so |K_f(n)|<=C_(f,theta)*L.
The repeated-factor count from character_partner_weight.py therefore costs
o(Y*t) absolutely. For squarefree n with at least two positive-sign prime
factors, fix the unique product M of ALL such factors. They exceed w, and
their reciprocal sum is H=O_delta(t), from Matomaki--Merikoski Lemma2.2:
https://arxiv.org/html/2112.11412v2#S2
The remaining v=n/M may be ANY z-rough integer here, not necessarily prime.
The corrected Henriot argument in multi_rare_partner.py already bounds the
two rough forms v and m-M*v by C_theta*(Y/M)*S_2(m)/L^2, uniformly M<=Y/z.
The same norm and local-factor proof applies without a primality restriction
on v. Thus the absolute weighted contribution is at most a constant times
Y*S_2(m)*(product_{q>w,chi(q)=1}(1+1/q)-1-H)=O_f,theta(Y*S_2*t^2)=o(Y*t).
The fixed multiplier C_f,theta bounds the entire weight, so no growing
factor or number of permutations is inserted. Source, corrected theorem:
https://doi.org/10.1017/S0305004114000280
2. A positive-sign factor w<q<=R is handled by the already checked upper
sieve at level E_epsilon/q with ORIGINAL cutoff z. Its prime-log mass is
O(X*V(z)*t+Y*t/L^6), with injective q*smooth-index remainder accounting.
Multiplication by C_f,theta*L makes this o(Y*t) absolutely. Union bounds
allow overlap with the preceding class. No K_f<=C*W inequality is needed.

Exact surviving factor support of the quintic:
3. Write U_j=chi*log^j and W=chi*log. Pairing complementary divisors on
chi(n)=-1 gives U_2=L_n*W and U_4=2*L_n*U_3-L_n^3*W, where L_n=log(n).
Consequently
  K_f=(1+4*kappa)*W-6*kappa*U_3/L_n^2+2*kappa*U_5/L_n^4. (1)
For squarefree n let k be its odd number of negative-sign prime factors,
h its number of positive-sign factors, x_i the negative logarithmic shares
and b_j the positive shares. Every share is positive and their total is1.
Taking a difference for each negative factor and a sum for each positive
factor gives:
  k>=7: K_f=0;
  k=5: K_f/L_n=240*kappa*2^h*product_i x_i >0;
  k=3: K_f/L_n=2*kappa*2^h*x_1*x_2*x_3
                  *(-3+5*sum_i x_i^2+15*sum_j b_j^2). (2)
Indeed the negative differences annihilate polynomials of lower degree.
For k=3 the exact moments are U_3/L_n^3=6*2^h*x_1*x_2*x_3 and
U_5/L_n^5=5*2^h*x_1*x_2*x_3*(3+sum x_i^2+3*sum b_j^2).
For k=1,h=0 the weight is1 after division by L_n; k=1,h=1 is the
semiprime kernel already derived. Repeated factors are not assigned these
squarefree formulas; they were charged separately in step1.
4. Combining steps1-3 gives the SIGNED reduction
  T_f=P+S_2+S_3+S_4+S_5+S_6+o(Y*t).                 (3)
Here S_j counts squarefree j-factor partners. The even classes have exactly
one positive-sign factor q>R; the odd classes have none. S_5 and S_6 are
positive, including balanced five-negative-factor configurations. For
kappa=100, five equal formal shares1/5 give weight192/25; distinct formal
shares(1/10,3/20,1/5,1/4,3/10) give27/5. These are factor identities,
not actual prime-first examples or prime-density statements. Negative
parts of S_2,S_3,S_4 may be dropped only in an UPPER bound for T_f.

An actual main-scale bound for the positive three-factor term:
5. At k=3,h=0, (2) becomes
  K_f/L_n=4*kappa*x*y*z*(1-5*(xy+xz+yz)).              (4)
Positivity forces x^2+y^2+z^2>3/5. If the largest share A<=1/2 then
sum squares<=A<=1/2. For A>=1/2, sum squares<=A^2+(1-A)^2. Hence a
positive triple has
  A>(5+sqrt(5))/10>18/25.
The largest prime r therefore exceeds n^(18/25); the other two distinct
primes s,t have M=s*t<n^(7/25)<=Y^(7/25). This small cofactor is within
the available distribution range. If gcd(M,Dm)>1 the actual count is zero.
6. Upper sieve the large prime r=(m-p)/M with an AUXILIARY cutoff
Z0=Y^eta0, where eta0>0 is a sufficiently small ABSOLUTE constant. It
does not change B_good. Omit primes dividing M from this auxiliary sieve.
The level E_epsilon/M has exponent eventually greater than1/5, since
1/2-epsilon-3delta/4-7/25>=83/400>1/5. Choose eta0 so Ford's upper
fundamental lemma has a sufficiently large fixed ratio. The local product
is at most C*S_2(m)/L: omitting the two primes of M changes it by at most4,
and the exceptional extra3 factor is bounded. Therefore the prime-log mass
for fixed M is at most
  C*X*S_2(m)/(phi(M)*L)+sum_e |r_(M*e)|,              (5)
with an ABSOLUTE C. The e are squarefree, Z0-smooth, coprime to M and
M*e<=E_epsilon. The earlier all-squarefree rare-prime remainders apply.
This map is NOT injective: each squarefree index has at most
binom(omega(index),2)=O(L^2) possible unordered semiprime cofactors M.
Multiplying the total remainder by the weight bound O(kappa*L) thus costs
O(kappa*L^3*Y*t/L^6)=O(kappa*Y*t/L^3).
7. From (4), K_f<=4*kappa*log(s)*log(t)/log(n)
<=8*kappa*log(s)*log(t)/L eventually. Also
sum_{s<t,st<=Y^(7/25)}log(s)*log(t)/phi(st)=O(L^2),
by the ordinary prime reciprocal logarithmic sum. Multiplying (5) by this
weight and summing the unique M proves
  S_3^+ <= C*kappa*Y*S_2(m)*t                         (6)
with an ABSOLUTE C. The ratio83/400 and the auxiliary cutoff are independent
of theta,kappa, so no hidden theta-dependent sieve constant is retained.
Ford's sieve input is Theorem3.6(a,b), printed p38:
https://ford126.web.illinois.edu/sieve2023.pdf

Equation(6) is a bound on the MAIN SCALE, not o(Y*t), a small specified
fraction, or a bound below the positive endpoint coefficient1. S_2,S_4,
S_5,S_6 also remain uncontrolled at the strength required to prove P>0.
The five-factor class shows why checking only the previously noticed triple
leak is insufficient. This pursuit preserves the alternative's component
and closes two discardable classes; it has not closed its positivity gap.
All analytic onsets remain ineffective; no zero existence or novelty claim.

Continuation: quintic_loss_budget.py now bounds ALL surviving positive
composite classes by C*(1+kappa)*Y*S_2(m)*t+o(Y*t), with C absolute.
The adaptive five-factor cutoff and large-prime variable switch remove
hidden dependence on theta from this upper-bound constant. This still does
not give the small loss or full signed-total positivity required above.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb, prod

from major_arc_kernel import _factorization


def quintic_support(negative_count: int, positive_count: int) -> str:
    """Classify squarefree factor COUNTS, without asserting signs or rarity."""
    if (type(negative_count) is not int or type(positive_count) is not int
            or negative_count < 1 or negative_count % 2 != 1 or positive_count < 0
            or negative_count+positive_count > 64):
        raise ValueError("require positive odd negative count, positive count>=0, total<=64")
    if negative_count >= 7:
        return 'vanishing'
    if positive_count >= 2:
        return 'multiple_positive'
    return {1: 'prime', 2: 'semiprime', 3: 'triple', 4: 'four_factor',
            5: 'five_factor', 6: 'six_factor'}[negative_count+positive_count]


def quintic_formal_weight(kappa: F, negative_shares: tuple,
                         positive_shares: tuple = ()) -> F:
    """Exact K_f/log(n) for FORMAL squarefree factor shares, not prime samples."""
    if type(kappa) is not F or kappa < 0:
        raise ValueError("require exact Fraction kappa>=0")
    if type(negative_shares) is not tuple or type(positive_shares) is not tuple:
        raise ValueError("require tuples of exact Fraction shares")
    k, h = len(negative_shares), len(positive_shares)
    quintic_support(k, h)
    shares = negative_shares+positive_shares
    if any(type(v) is not F or v <= 0 for v in shares) or sum(shares) != 1:
        raise ValueError("require positive exact Fraction shares summing to1")
    if k >= 7:
        return F(0)
    if k == 5:
        return 240*kappa*2**h*prod(negative_shares)
    if k == 3:
        return (2*kappa*2**h*prod(negative_shares)
                *(-3+5*sum(v*v for v in negative_shares)
                  +15*sum(v*v for v in positive_shares)))
    # For one negative factor, accumulate the first five subset moments.
    moments = [F(1)]+[F(0)]*5
    for share, sign in (*((v, -1) for v in negative_shares),
                        *((v, 1) for v in positive_shares)):
        moments = [sum(comb(j, i)*share**(j-i)*moments[i] for i in range(j+1))
                   +sign*moments[j] for j in range(6)]
    coefficients = (0, 1, -kappa, 4*kappa, -5*kappa, 2*kappa)
    return sum(c*v for c, v in zip(coefficients, moments))


def semiprime_sieve_indices(index: int, level: int, cofactor_limit: int,
                           sieve_cutoff: int) -> tuple[tuple[int, int], ...]:
    """All (M,e) for a squarefree index, M two primes and e sieve-smooth.

    These indices need NOT be unique. The original rough/character filters
    on M are deliberately omitted, giving a superset for the upper bound.
    This checks exact support only, not the analytic remainder size.
    """
    if any(type(v) is not int for v in (index, level, cofactor_limit, sieve_cutoff)):
        raise ValueError("require exact integers")
    if index < 1 or not 2 <= sieve_cutoff <= level or not 1 <= cofactor_limit <= level:
        raise ValueError("require index>=1, 2<=sieve_cutoff<=level, 1<=cofactor_limit<=level")
    if index > level:
        return ()
    factors = _factorization(index)
    if any(exponent != 1 for _, exponent in factors):
        return ()
    primes = tuple(p for p, _ in factors)
    return tuple(sorted((s*t, index//(s*t)) for s, t in combinations(primes, 2)
                        if s*t <= cofactor_limit
                        and all(p <= sieve_cutoff for p in primes if p not in (s, t))))
