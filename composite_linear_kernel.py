"""General composite moduli: a costed linear estimate and its balanced gap.

Owner: Kevin's Goldbach research. Purpose: test the actual composite-modulus
obstacle, including nonunit frequencies and periods sharing modulus factors.
This preserves a successful unbalanced component and an explicit FAILURE
of its power budget in the balanced critical box. It is not a lower bound
on the true error, a no-go theorem for completion, or a prime-pair estimate.

Primary analytic input: the ordinary composite Kloosterman Weil bound
  |S(a,b;q)|<=tau(q)*sqrt(q*gcd(a,b,q)),
recorded in Topacogullari, arXiv:1506.02608v1, section2, printed p4:
https://arxiv.org/pdf/1506.02608v1 . Only this complete-sum bound is used;
the source's untwisted shifted-divisor theorems are NOT being imported.
No composite-modulus version of the KMS bilinear theorem is assumed.

Concrete question and adjudication:
Does linear completion survive arbitrary composite q, nonunit m*k, and
joint periodic weights, with sufficiently small aggregate costs? YES for
the estimate below, which saves a power in an explicit unbalanced region.
NO full-box saving follows from this estimate: the balanced critical box
b=x=1/3,y=1/2 has exponent13/12 before decorations. This is an upper-bound
budget failure, not a counterexample to cancellation or to Goldbach.

Theorem (unconditional smooth general-modulus MODEL):
Let m be an integer in[Y,2Y], Y tending to infinity, and
  B=Y^b, A=Y^x, C=Y^y, K=B*A*C/Y,
  1/5<=b<=13/25, 0<=x<=(1-b)/2, 0<=y<=1/2,
  1<=J0,H<=Y^(1/4096).
For each integer q in[C,2C], q>=2, choose a unit r_q modulo q and an
integer J_q<=J0. For every k<=floor(H*K), omega_(q,k)(M,a) is any complex
function periodic in each variable modulo J_q with absolute value<=1.
It may couple residues and depend arbitrarily on q,k. For fixed smooth
W1,W2 supported in[1,2], let
  E_q=Y/(B*A*q) sum_(1<=k<=H*K) sum_(M,a>=1; gcd(M*a,q)=1)
          W1(M/B)W2(a/A)*omega_(q,k)(M,a)*e_q(r_q*m*k/(M*a)).
Then for every epsilon>0,
  sum_(q in[C,2C]) |E_q|
    << Y^epsilon*H*(J0^2*min(A,B)*C^(3/2)+J0*B*A).          (1)
There is NO condition gcd(J_q,q)=1 or gcd(m*k,q)=1. Prime powers and
balanced composite moduli are included. Uniformly smooth coupled spatial
weights are also allowed by the Fourier-series argument already proved
in decorated_prime_kernel.py; its uniform derivative hypotheses remain.

In particular, if min(b,x)+3*y/2<=127/128, (1) implies
  sum_q |E_q| <<Y^(4067/4096+epsilon).                      (2)
At y=1/2 this condition is min(b,x)<=31/128. The h=0 term is below
Y^(77/100), since b+x<=19/25. This is actual cancellation in a MODEL
kernel, not a transfer of the original roughness/sieve coefficients.

Exact transforms:
For ANY q>=2 and integers h,l,t, write
  F_q(h,l;t)=sum_(u,v units modq)e_q(t/(u*v)+h*u+l*v).
With K(l)=F_q(h,l;t)/q its negative-sign finite Fourier transform is
  sum_(l modq)K(l)e_q(-j*l)
    =S(h,t/j;q) if gcd(j,q)=1, and0 otherwise.              (3)
The l sum enforces v=j. Consequently its magnitude is at most
tau(q)*sqrt(q*gcd(h,t,q)), including nonunit h and t. Also, exactly,
  F_q(0,l;t)=c_q(t)*c_q(l),
  F_q(h,0;t)=c_q(t)*c_q(h).
These Ramanujan identities include t=0 and all prime-power valuations.

For the actual joint periodic weight set J=J_q, L=q*J and
  F_L(h,l;t)=sum_(u,v modL; gcd(u*v,q)=1)
               omega(u,v)e_q(t/(u*v))*e_L(h*u+l*v).
Define D(j)=sum_(l modL)F_L(h,l;t)/L *e_L(-j*l). This is0 if j is not
a q-unit. Otherwise expand omega(u,j)=sum_(a modJ)c_j(a)e_J(a*u), with
  c_j(a)=J^-1 sum_(r modJ)omega(r,j)e_J(-a*r), |c_j(a)|<=1.
Writing u=u0+q*v gives the EXACT formula
  D(j)=J*sum_(a modJ; J divides h+q*a)
                 c_j(a)*S((h+q*a)/J,t/j;q).                (4)
No inverse modulo J is required. If d divides((h+q*a)/J,t,q), then
d divides h, so its gcd factor divides gcd(h,t,q). Thus
  |D(j)|<=J^2*tau(q)*sqrt(q*gcd(h,t,q)).                    (5)
This conservative J^2 cost includes every Fourier coefficient. Short
period weights have not been treated as free or as smooth coefficients.

Proof of (1), including the zero frequency:
1. If H*K<1, there are no terms. Otherwise C>=Y^(6/25-1/4096), so
   all moduli in a nonempty box grow, and every m*k is a nonzero integer
   of polynomial size in Y. Twice applying Poisson at period L gives
   prefactor Y/(q*L^2)=Y/(q^3*J^2) and Fourier weights
     W1_hat(B*h/L)*W2_hat(A*l/L).

2. For fixed h,t, complete the smooth l sum using (5). Its natural scale
   N=L/A is at most L, since A>=1. Fourier inversion and summation by
   parts yield
     |sum_l W2_hat(A*l/L)*F_L(h,l;t)|
        <<L*J^2*tau(q)*sqrt(q*gcd(h,t,q))*log(2L).
   A Schwartz weight is handled by partition into L-length intervals;
   their suprema and variations are summable. If N<1, its discrete L1
   norm and the pointwise Fourier-inversion bound give the same result.
   This step requires smooth amplitudes, not arbitrary l coefficients.

3. Treat h!=0 by the elementary divisor estimate
     sum_(h!=0)|W1_hat(B*h/L)|*sqrt(gcd(h,t,q))
       <=sum_(d|(t,q))sqrt(d)*sum_(h!=0; d|h)|W1_hat(B*h/L)|
       <<(L/B)*sum_(d|(t,q))1/sqrt(d) <=(L/B)*tau(q).        (6)
   The nonzero Schwartz L1 bound is valid at EVERY positive scale,
   including L/(B*d)<1. Thus prime-power factors and all nonzero axis
   multiples are already accounted for, without assuming h or t units.
   Restoring the prefactor, (5)--(6) give per q,k
     <<Y^epsilon*Y*J^2/(B*sqrt(q)).
   There are at most H*K frequencies and O(C) moduli, giving
     <<Y^epsilon*H*J0^2*A*C^(3/2).

4. The h=0 contribution needs its arithmetic structure; the degenerate
   Weil estimate alone would lose too much. Use just the M Poisson step.
   For a fixed a coprime to q, put g=gcd(q,J). Averaging the J lifts of
   each u modulo q gives
     sum_(u modL; gcd(u,q)=1)omega(u,a)e_q(t/(u*a))
        =J*sum_(u units modq)f_a(u modg)e_q(t/(u*a)),
   where |f_a|<=1. Inverting u gives another bounded function of the
   unit residue modulo g. For ANY |f|<=1 and t' with gcd(t',q)=gcd(t,q),
     |sum_(v units modq)f(v modg)e_q(t'*v)|
        <=g*tau(q)*gcd(q,t).                               (7)
   To prove this, group v=r modg over unit residues r, and insert
   1_(gcd(v,q)=1)=sum_(d|q,d|v)mu(d). Only gcd(d,g)=1 is possible.
   Then dg divides q, and the progression v=r modg,d|v has q/(dg)
   terms. Its additive sum vanishes unless q/(dg) divides t'; if it
   does, its magnitude is q/(dg)<=gcd(q,t). Sum at most g residue
   classes and tau(q) divisors. This proves (7), also for t=0.

   With the one-variable Poisson prefactor Y/(A*q*L), the a sum has
   O(A) total smooth mass. Therefore h=0 costs at most
     <<Y*g*tau(q)*gcd(q,m*k)/q^2.
   A unit r_q does not change this gcd. For every positive n,
     sum_(C<=q<=2C)gcd(q,n)
       =sum_(d|n)phi(d)*#{q in[C,2C]:d|q}
       <=2*C*sum_(d|n)phi(d)/d <=2*C*tau(n).                (8)
   Hence (7)--(8), g<=J0, and divisor bounds for polynomial-size m*k
   give total h=0 cost <<Y^epsilon*H*J0*B*A. No individual coprimality
   exception or prime restriction was silently dropped.

5. This proves (1) with A in the first term. Swapping M and a and
   transposing omega proves it with B instead. Both hold for the same
   sum of per-q absolute values, so take the smaller bound. The uniform
   coupled-weight corollary follows by the already-proved convergent
   Fourier separation with arbitrary normalized k-dependent coefficients.

Reassessment and next question:
The complete composite transform and its nonunit modes are no longer an
unexamined obstruction. The remaining quantitative obstacle includes the
balanced example B=A=Y^(1/3), C=Y^(1/2), K=Y^(1/6), where (1) gives
Y^(13/12+epsilon) before period/frequency costs. All three original
factors and the modulus remain arithmetic candidates; none is discarded.
A new step must save more than1/12 over THIS bound at that box, plus
period/frequency costs, by using correlation across frequencies or moduli.
Merely applying the same linear completion or rechecking its identity
will not do that. KMS supplies a prime-core tool, not a composite theorem.
One UNTESTED next route is to bound additive autocorrelations of
multiplicative dilates of Kl3, then combine prime factors by CRT to test
a composite Polya--Vinogradov bilinear estimate. Prime diagonal cases,
coefficient nonunits and prime powers must all be accounted for. A primary
locator is Fouvry--Kowalski--Michel, Algebraic trace functions over the
primes, arXiv:1211.6043, Theorem1.17, cited by KMS Remark1.2. This exact
FKM theorem has NOT yet been read here, and no composite version follows
from its citation. This is a next hypothesis, not part of proof(1).
The full original arithmetic transfer and signed prime estimate remain
OPEN; the latest original-affine result is still2b8cf98. No new prime
coverage, exceptional zero, effective onset or originality is claimed.

Finite routines below check exact composite/periodic transforms and the
restricted Ramanujan decomposition in Q[zeta_n], including prime powers.
They do not prove an infinite analytic theorem or replace its source.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from math import gcd

from major_arc_kernel import _mobius_phi


def _divide_monic(numerator, denominator):
    remainder = list(numerator)
    quotient = [0]*max(0, len(numerator)-len(denominator)+1)
    for degree in range(len(remainder)-1, len(denominator)-2, -1):
        coefficient = remainder[degree]
        offset = degree-len(denominator)+1
        quotient[offset] = coefficient
        for j, value in enumerate(denominator):
            remainder[offset+j] -= coefficient*value
    return quotient, remainder[:len(denominator)-1]


@lru_cache(maxsize=None)
def _cyclotomic_polynomial(n):
    polynomial = [-1]+[0]*(n-1)+[1]
    for d in range(1, n):
        if n % d == 0:
            polynomial, remainder = _divide_monic(polynomial, _cyclotomic_polynomial(d))
            if any(remainder):
                raise ArithmeticError("cyclotomic division was not exact")
    return tuple(polynomial)


def _reduce(counts, n):
    return tuple(_divide_monic(counts, _cyclotomic_polynomial(n))[1])


def _periodic_parameters(q, period, parameter, h, dual, weight):
    if type(q) is not int or q < 2:
        raise ValueError("modulus must be an integer at least2")
    if type(period) is not int or period < 1:
        raise ValueError("period must be a positive integer")
    if any(type(v) is not int for v in (parameter, h, dual)):
        raise ValueError("parameter and frequencies must be integers")
    if (len(weight) != period or any(len(row) != period for row in weight)
            or any(type(v) is not int for row in weight for v in row)):
        raise ValueError("weight must be a period by period integer matrix")


def periodic_linear_transform(q, period, parameter, h, dual, weight):
    """Direct normalized l-DFT of F_L, exactly in Q[zeta_(qJ)].

    Integer weights can exceed1 in the algebraic check; the analytic
    theorem separately requires absolute value<=1.
    """
    _periodic_parameters(q, period, parameter, h, dual, weight)
    length = q*period
    counts = [F(0)]*length
    for x in range(length):
        if gcd(x, q) != 1:
            continue
        for y in range(length):
            if gcd(y, q) != 1:
                continue
            amplitude = F(weight[x % period][y % period], length)
            phase = period*parameter*pow(x*y, -1, q)+h*x
            for l in range(length):
                counts[(phase+l*(y-dual)) % length] += amplitude
    return _reduce(counts, length)


def periodic_kloosterman_prediction(q, period, parameter, h, dual, weight):
    """Independent right side of (4), expanding J*c_j(a) exactly."""
    _periodic_parameters(q, period, parameter, h, dual, weight)
    length = q*period
    counts = [0]*length
    if gcd(dual, q) != 1:
        return _reduce(counts, length)
    second = parameter*pow(dual, -1, q)
    for frequency in range(period):
        if (h+q*frequency) % period:
            continue
        first = (h+q*frequency)//period
        for residue in range(period):
            amplitude = weight[residue][dual % period]
            for x in range(1, q):
                if gcd(x, q) == 1:
                    phase = (period*(first*x+second*pow(x, -1, q))
                             -q*frequency*residue) % length
                    counts[phase] += amplitude
    return _reduce(counts, length)


def _axis_parameters(q, divisor, parameter, weights):
    if type(q) is not int or q < 2:
        raise ValueError("modulus must be an integer at least2")
    if type(divisor) is not int or divisor < 1 or q % divisor:
        raise ValueError("residue modulus must be a positive divisor of q")
    if type(parameter) is not int:
        raise ValueError("parameter must be an integer")
    if len(weights) != divisor or any(type(v) is not int for v in weights):
        raise ValueError("one integer weight per residue is required")


def restricted_axis_exact(q, divisor, parameter, weights):
    _axis_parameters(q, divisor, parameter, weights)
    counts = [0]*q
    for v in range(q):
        if gcd(v, q) == 1:
            counts[parameter*v % q] += weights[v % divisor]
    return _reduce(counts, q)


def restricted_axis_prediction(q, divisor, parameter, weights):
    """Independent Mobius/progression decomposition used in (7)."""
    _axis_parameters(q, divisor, parameter, weights)
    counts = [0]*q
    for d in range(1, q+1):
        if q % d or gcd(d, divisor) != 1:
            continue
        mu = _mobius_phi(d)[0]
        length = q//(d*divisor)
        if not mu or parameter % length:
            continue
        for residue in range(divisor):
            if gcd(residue, divisor) == 1:
                first = d*((residue*pow(d, -1, divisor)) % divisor) if divisor > 1 else 0
                counts[parameter*first % q] += mu*length*weights[residue]
    return _reduce(counts, q)


def axis_triangle_budget(q, divisor, parameter):
    _axis_parameters(q, divisor, parameter, (1,)*divisor)
    phi = _mobius_phi(divisor)[1]
    return phi*sum(abs(_mobius_phi(d)[0])*(q//(d*divisor))
                   for d in range(1, q+1)
                   if q % d == 0 and gcd(d, divisor) == 1
                   and parameter % (q//(d*divisor)) == 0)


@dataclass(frozen=True)
class CompositeLinearBudget:
    active: bool
    frequency_exponent: F
    nonzero_exponent: F
    axis_exponent: F
    total_exponent: F
    saving: F
    covered_by_fixed_margin: bool


def composite_linear_budget(b, x, y, period_exponent=0, frequency_exponent=0):
    values = (b, x, y, period_exponent, frequency_exponent)
    if any(type(v) not in (int, F) for v in values):
        raise ValueError("exponents must be exact rational numbers")
    b, x, y, j, h = map(F, values)
    if not (F(1, 5) <= b <= F(13, 25) and 0 <= x <= (1-b)/2
            and 0 <= y <= F(1, 2)):
        raise ValueError("box lies outside the stated family")
    if any(not 0 <= v <= F(1, 4096) for v in (j, h)):
        raise ValueError("decoration exponents must lie in[0,1/4096]")
    frequency = b+x+y-1+h
    nonzero = min(b, x)+F(3, 2)*y+2*j+h
    axis = b+x+j+h
    total = max(nonzero, axis) if frequency >= 0 else F(0)
    covered = min(b, x)+F(3, 2)*y <= F(127, 128)
    return CompositeLinearBudget(frequency >= 0, frequency, nonzero, axis,
                                 total, 1-total, covered)
