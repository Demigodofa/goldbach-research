"""A quantitative prime-dilation gate for the actual localized sieve error.

Owner: Kevin's Goldbach research. Purpose: decide whether multiplicative
sign averaging supplies an arithmetic estimate after the proved rough
squarefree localization. Preserve a usable exact gate and its paid costs;
do not promote the remaining covariance assumption into a prime theorem.

Reuse specialized_sieve_coefficients.py with N=2x, L=logx,
y=floor(exp(sqrtL)), gamma=1/2-e, nu=1/3-2e, 0<e<=1/100.
There M=sum_(n=trv in (x/2,x]) mu(r) w_n, |w_n|<<L, with
 r>n^gamma, mu^2(tr)=1, every prime of tr in (y,n^nu),
 v=1 OR v prime with v>=n^nu.
Its relation to prime mass is B_P-R_nu(w)+M+all-log error. Neither
M nor R_nu is currently estimated at the required signed scale.

1. AN ADDITIONAL ACTUAL SUPPORT ESTIMATE.
One may also impose gcd(n,N)=1 with O_A(x/L^A) error for every fixed A.
There are at most tau(n) representations (t,r,v). Since n is y-rough,
 any common prime ell|gcd(n,N) exceeds y. Therefore the absolute cost is
 << L sum_(ell|N,ell>y prime) sum_(m<=x/ell) tau(ell*m)
 <= 2L sum_(ell|N,ell>y) sum_(m<=x/ell) tau(m)
 << x L^2 sum_(ell|N,ell>y) 1/ell
 << x L^3/(y logy) = O_A(x/L^A).
The last step uses at most logN/logy distinct such divisors. This is an
ACTUAL estimate using the averaged divisor bound, not an n^eta maximum.
It removes deterministic noncoprime rows and prime divisors of N before
requesting uniform decorrelation. Write M^circ for the restricted sum.

2. EXACT RECONSTRUCTION, NO HARMONIC-MASS ERROR.
Fix (t,v), put c=tv and X=x/c. Define F_tv(r)=w_(cr) times EVERY mask
above, including gcd(cr,N)=1, zero outside the permitted support. Let
P_all be all primes in (y,x^nu]. Every prime divisor of an admitted r
lies in P_all, and r>n^gamma with gamma>nu implies omega(r)>=2.
With omega the number of DISTINCT prime factors,
 S_tv=sum_r mu(r)F_tv(r)
     =-sum_s mu(s)/(1+omega(s))
                    sum_(p in P_all,p not dividing s) F_tv(ps).       (1)
Indeed each r is counted omega(r) times and 1+omega(r/p)=omega(r).
Squarefreeness makes mu(ps)=-mu(s). All nonzero s have all prime
factors in P_all, so omega(s)=omega_P_all(s). There is no unrepresented
support or approximation of omega by its mean. The full prime set is
essential; restricting it arbitrarily requires a different denominator
and control of integers missed by that restricted set.

This is the classical Ramare identity, specialized to our already paid
support. It is not a new identity. Green's source below gives the same
identity and explicitly points out the prime-dilation covariance obstacle
for shifted Mobius/prime correlation. We are checking its exact costs here.

3. A SIGNED ENERGY WITH A NEGLIGIBLE ACTUAL DIAGONAL.
Partition P_all into disjoint blocks (P,2P], P=2^j*y, truncating the
last at x^nu. For the corresponding contribution S_tv,P in (1), nonzero
s is in (X/(4P),X/P]. Cauchy, using |mu(s)/(1+omega(s))|<=1, gives
 |S_tv,P|^2 <= (X/P) [D_tv,P+O_tv,P],                    (2)
 D_tv,P=sum_s sum_p |F_tv(ps)|^2,
 O_tv,P=sum_s sum_(p!=q) F_tv(ps) conjugate(F_tv(qs)).
The prime/s coprimality is retained explicitly or by F's zero extension.
O is REAL and SIGNED: it equals twice the real part of the p<q sum.
D+O is nonnegative. Remove a coefficient weight from the ENTIRE positive
square before expanding; do not remove it only from off-diagonal terms.
The elementary prime-counting upper bound gives, uniformly in every row,
 D_tv,P << L^2 X/logP.
Indeed sum_p floor(X/p)<= (X/P)*#{p in (P,2P]}<<X/logP.
An empty block, including one with X/P<1, contributes zero. Thus
 |S_tv,P| << LX/sqrt(P logP) + sqrt((X/P) O_tv,P^+),     (3)
where O^+=max(O,0). This uses a one-sided aggregate covariance, not
the larger sum of absolute values of individual prime-pair correlations.

4. PAY THE FULL SUM OVER FACTORIZATIONS.
Coarsely sum_(t,v) X <= x (sum_(t<=x)1/t)(1+sum_(v<=x prime)1/v)
 << x L^2. There are O(L) prime blocks. The diagonal part of (3),
summed geometrically in P>=y and then over rows, is <<xL^3/sqrt(y),
hence all-log small. Define the finite, actual nonnegative quantity
 E_x=sum_(t,v,P) O_tv,P^+/P,                            (4)
over all rows and blocks. Another Cauchy inequality, with sum X<<xL^3
over this full index set, proves
 |M| <<_A x/L^A + sqrt(x L^3 E_x).                     (5)
Thus E_x<<x/L^(2A+3) is a SUFFICIENT condition for M<<x/L^A.
A stronger, easier-to-state sufficient input is the uniform row estimate
 O_tv,P^+ << XP/L^(2B),                                (6)
which yields M<<x/L^(B-3) plus all-log errors. No such input is proved.
Even proving M small would leave R_nu(w) to handle in the prime identity;
the earlier critical-factor/Type II positivity criterion remains distinct.

5. WHAT ARITHMETIC IS STILL MISSING.
The two reflected von Mangoldt arguments in an off-diagonal term are
 q1=N-cps and q2=N-cqs, with q*q1-p*q2=(q-p)N.
All moving smoothness, roughness, squarefree, physical and coprimality
masks remain in F_tv(ps)F_tv(qs). Expanding w=a-b retains the four terms
a_p a_q-a_p b_q-b_p a_q+b_p b_q with those SAME masks.
Neither separate size bounds nor the identity (1) establishes their
signed cancellation. In particular one may not discard the mixed terms.

The generic Katai mean-divisor argument replaces omega_P by
H=sum_(p in P)1/p and pays a reconstruction term O(WX/sqrtH).
For auxiliary primes between y and any fixed power of x, H<=.5logL+O(1).
With W<<L this available bound is XL/sqrt(logL), too large at X/L
precision. This is a failed bound, NOT a lower bound for the actual sum.
For our moving F_x, every fixed p<=y eventually has F_x(ps)=0. Hence
fixed-prime qualitative orthogonality cannot simply be applied to this
triangular family with a claimed uniform rate. Formula (1) bypasses this
specific reconstruction loss but supplies no off-diagonal estimate.

DISPOSITION: source-known mechanism, task-specific exact masks and paid
diagonal/common-divisor costs. Actual E_x remains OPEN. No new prime
coverage, numerical onset, global impossibility result or priority claim.
The polynomial identities, joint bounds and earlier decompositions remain
available for combination with a new arithmetic input.

Primary sources checked 2026-09-09:
* Ben Green, arXiv:1604.04481v4, section2, especially the Ramare identity
  p6 and the shifted-Mobius remark p5 after Proposition2.2:
  https://arxiv.org/pdf/1604.04481v4
  We use the elementary identity, not Proposition2.2 wholesale; its
  parameter restrictions and sieve residual are not silently waived.
* Tao, 2011-11-21, Proposition1 and section1: Katai's qualitative
  criterion and the mean-divisor reconstruction error:
  https://terrytao.wordpress.com/2011/11/21/the-bourgain-sarnak-ziegler-orthogonality-criterion/
* Bourgain--Sarnak--Ziegler, Theorem2 and section2, parameters fixed
  before the large-N limit; Note1 distinguishes qualitative Mobius
  orthogonality from the rate needed for primes:
  https://publications.ias.edu/sites/default/files/disjointness%20b-s-z%20oct.pdf
Finite helpers below verify algebra and retained support, not (4)'s
unproved analytic estimate. Their rational weights are toy inputs.
"""
from fractions import Fraction
from math import gcd

from major_arc_kernel import _factorization, _mobius_phi
from specialized_sieve_coefficients import mobius_cofactor_terms
from unexceptional_vaughan_gate import _positive


def cofactor_rows(x, y, weights, *, coprime=True):
    """Finite rational rows with the actual moving masks, for identity guards."""
    _positive(x, 'x')
    _positive(y, 'y')
    rows = {}
    for n, value in weights.items():
        _positive(n, 'n')
        if not x < 2*n <= 2*x:
            raise ValueError('weight outside (x/2,x]')
        if coprime and gcd(n, 2*x) != 1:
            continue
        for t, r, v, _ in mobius_cofactor_terms(n, y):
            rows.setdefault((t, v), {})[r] = Fraction(value)
    return rows


def dilation_blocks(values, y):
    """Return P -> s -> p -> F(ps), preserving all supplied row masks.

    Requires squarefree r>1 and every prime factor>y. Uses the FULL set
    of divisors of every supplied r; no selected-prime residual is lost.
    """
    _positive(y, 'y')
    blocks = {}
    for r, value in values.items():
        _positive(r, 'r')
        factors = _factorization(r)
        if r == 1 or any(p <= y or k != 1 for p, k in factors):
            raise ValueError('require squarefree r>1 with all primes>y')
        for p, _ in factors:
            lower = y
            while p > 2*lower:
                lower *= 2
            blocks.setdefault(lower, {}).setdefault(r//p, {})[p] = Fraction(value)
    return blocks


def block_energy(rows):
    """Exact signed energy and Ramare sum for real rational toy weights."""
    total = diagonal = energy = coefficient_norm = Fraction(0)
    for s, prime_values in rows.items():
        factors = _factorization(s)
        if any(k != 1 for _, k in factors):
            raise ValueError('require squarefree s')
        for p in prime_values:
            if _factorization(p) != ((p, 1),) or s % p == 0:
                raise ValueError('require prime p coprime to s')
        coefficient = Fraction(-_mobius_phi(s)[0], 1 + len(factors))
        row_sum = sum(map(Fraction, prime_values.values()), Fraction(0))
        total += coefficient*row_sum
        coefficient_norm += coefficient**2
        diagonal += sum((Fraction(value)**2 for value in prime_values.values()), Fraction(0))
        energy += row_sum**2
    return {'sum': total, 'diagonal': diagonal, 'off_diagonal': energy-diagonal,
            'energy': energy, 'coefficient_norm': coefficient_norm,
            'cauchy_bound_squared': coefficient_norm*energy}
