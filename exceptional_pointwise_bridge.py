"""Conditional pointwise prime-pair coverage and its exact excluded classes.

Owner: Kevin's research. Purpose: connect an existing POINTWISE theorem to
our checked arithmetic suppression family, keeping actual G separate from L.
The source supplies the analytic theorem; no historical novelty is asserted.
Sol checked the deductions and actual verifier on 2026-09-08. Seven focused
exact tests passed normally and with Python -O.

Primary source, read 2026-09-08:
Matomaki--Merikoski, Siegel zeros, twin primes, Goldbach's conjecture, and
primes in short intervals, IMRN 2023, Theorem 1.4:
https://academic.oup.com/imrn/article/2023/23/20337/7111993

Source hypotheses and specialization:
Let chi be primitive quadratic of conductor D>24, D=2**r*D_odd, with a
REAL ZERO beta=1-1/(eta*log D), eta>=10. Write V=log N/log D>=10.
For even N the source gives the ordered von Mangoldt pair sum
  W(N)=S_2(N)*N*b_D(N)+O((N/phi(N))*N*e(N,eta,V)),             (1)
where, fixing its C=1 and epsilon=1/10,
  e=exp(-sqrt(V*log eta))+exp(-sqrt(log N))+V*log(eta)**6/eta,
  b_D(N)=1+chi(-1)*1_{phi(2**r)|N}*(-1)**(N/phi(2**r))
                  *product_{odd p|D, p not dividing N}(-1/(p-2)).
The sign term is used only when its divisibility condition holds.
Existence of such a zero is a HYPOTHESIS, not an output of this verifier.

Exact bridge to the earlier model:
Use A_D,B_D,C_D from exceptional_character_model.py; these are residue
moments, not the cubic survivor arrays. Chinese remaindering gives
  b_D(N)=1+C_D(N)/A_D(N).                                    (2)
For odd p|D the C/A factor is chi_p(-1) if p|N, and
-chi_p(-1)/(p-2) otherwise. The 4-part gives -(-1)**(N/2).
The 8-part gives sigma*(-1)**(N/4) when 4|N and zero otherwise,
where sigma=chi_8(-1)=+1 or chi_-8(-1)=-1. These are exactly (2).

Let q0=product_{p>=5,p|D}p>1. If q0 does not divide N, then |C_D/A_D|
is at most1/3. If q0|N, then B_D=0 and C_D/A_D is in {-1,0,1}.
Consequently b_D=0 EXACTLY on the earlier F_D={B_D=0,C_D=-A_D};
off F_D, b_D>=2/3. This source coefficient omits the finite model's
linear B terms: it is NOT (A_D-2*B_D+C_D)/A_D.

Conditional coverage consequence:
For each fixed alpha in (0,1) there are constants eta0(alpha)>=10 and
N0 such that, if the zero hypothesis holds with eta>=eta0, EVERY even N
  max(D**10,N0)<=N<=D**(eta**(1-alpha)), N not in F_D,
satisfies the ACTUAL ordered odd-prime count bound
  G(N)>=S_2(N)*N/(4*log(N)**2)>0.                            (3)
No separate Fourier-residual exception is needed in this conditional
branch. No numerical eta0 or N0, actual zero, or new finite coverage run
is supplied. In particular (3) does not imply canonical L(N)>0.

Uniform error and removal of prime powers:
In the stated V range,
  e<=exp(-sqrt(10*log eta))+exp(-sqrt(log N))
                                         +eta**(-alpha)*log(eta)**6.
All three terms tend uniformly to zero as eta,N grow independently.
Also S_2(N)/(N/phi(N))>=C_2>=1/2: here
C_2=product_{p>2}(1-1/(p-1)**2), and the elementary product lower bound
1-sum x_p applies, with sum x_p <=sum_{k>=1}1/(4*k*k)<=1/2.
Thus choose eta0,N0 so the absolute error in (1) is <=S_2(N)*N/6.
It follows that W(N)>=S_2(N)*N/2 off F_D.
There are at most (floor(log_2 N)-1)*floor(sqrt N) proper prime powers
<=N: each exponent2..floor(log_2 N) has at most floor(sqrt N) bases.
Pairs involving any such power contribute at most twice this number of
positions, each weighted by at most log(N)**2. Their total is therefore
O(sqrt(N)*log(N)**3)=o(S_2(N)*N), uniformly in D and eta. Enlarge N0 so
it is <=S_2(N)*N/4. For even N>4, a pair of primes cannot involve2.
The remaining prime-pair weight is <=G(N)*log(N)**2, proving (3).

Two useful arithmetic consequences under the SAME zero/range hypotheses:
* Every power of two in the range obeys (3), since q0>1 is odd.
* F_D is empty exactly when D is odd, 3 does not divide D, and D=1 mod4,
  equivalently D=1 or5 mod12. For such conductors (3) covers the ENTIRE
  even interval. To check this classification, write D=q0*h with
  h in {1,3,4,8,12,24}. If h=1 the correlation on q0|N has the fixed
  sign chi(-1), and is negative exactly when D=3 mod4. A 3-component
  attains both signs by changing divisibility by3. A 4-component attains
  both signs at even residues0,2; an 8-component does so at0,4. CRT lets
  these choices be made independently of q0 and the other component.

Scope: F_D is where this leading-term argument is inconclusive, NOT a
family of counterexamples. The absent/insufficient-zero case, targets
outside the range, and canonical L on Fourier exceptions remain open.
The result is a source-backed conditional branch, not unconditional
coverage, a proof of Goldbach, or a detection of a Siegel zero.

Stacking boundary (deduction and actual verifier checked by Sol):
Primary source: Philippe Michel, Analytic Number Theory and Families of
Automorphic L-functions, version May24 2006, printed p21, Landau/Page:
https://www.epfl.ch/labs/tan/wp-content/uploads/2018/10/Parkcitylectures.pdf
There is an effective c0>0 such that at most one primitive real character
of conductor<=Q has a real zero in [1-c0/log Q,1]. Fix 0<c<c0, c<=1;
no numerical value of such c is supplied here.

Let DISTINCT primitive real characters of conductors D1<=D2 have zeros
beta_i=1-1/(eta_i*log D_i). If eta2>=1/c, then
  log D2/log D1 > c*eta1.                                   (4)
Otherwise both zeros belong to [1-c/log D2,1], strictly inside the source
region with Q=D2, contradicting Landau/Page. The source proof excludes a
second character even if its zero has the same numerical value. When
D1=D2, two distinct characters BOTH satisfying eta_i>=1/c are impossible.

For the ambient interval upper endpoint U1=D1**(eta1**(1-alpha)), (4) gives
  log(D2**10)/log U1 > 10*c*eta1**alpha.                    (5)
Thus 10*c*eta1**alpha>=1 forces disjoint intervals; equality is sufficient
because (4) is strict. If the right side is at least2, D2**10>U1**2.
The lower cutoff N0 can only shorten the certified intervals.
For fixed alpha, choose a fixed strength threshold ensuring eta>=1/c,
eta**(1-alpha)>=10, and 10*c*eta**alpha>=2. Any family of DISTINCT
characters exceeding that threshold has disjoint ambient intervals in
conductor order, with square-size gaps between consecutive intervals.
A finite family has bounded union. An infinite family has unbounded
conductors, and arbitrarily large even integers in these gaps. Thus these
certificates alone cannot cover a tail, even if every F_D is empty.

More generally, an upper exponent v1=o(eta1) and next lower exponent
v2>=10 give logarithmic endpoint ratio >10*c*eta1/v1, tending to infinity.
This is a GEOMETRIC statement only. Making the displayed source error
envelope tend to zero requires v1*log(eta1)**6/eta1=o(1), together with
the other source hypotheses. That stronger condition implies the geometric one;
the converse is false. Enlarging ranges subject to that error condition
therefore does not evade this asymptotic separation.

These are gaps in this strong-zero certificate family, not Goldbach
counterexamples. Weaker zeros or different analytic regimes are not ruled
out. Reusing the same zero at another alpha is not a second character and
does not justify applying (4); its enlarged range must be checked anew.

The later notes/fixed-density-exceptional-zero-obligation.md uses the SAME
source on F_D rather than off it. Arbitrarily strong zeros in suppressible
conductors would force actual central T_N/H(N) to approach zero along
explicitly lifted targets, and the cutoff residual/H to approach -1.
This is conditional density collapse, not a zero detection or a vanishing
prime-pair claim. The helper below certifies only the exact target lift.
"""
from fractions import Fraction
from math import isqrt

from character_suppression import suppression_classes
from major_arc_kernel import _factorization


def pointwise_coefficient(conductor: int, target: int, *, two_sign: int = 1
                          ) -> Fraction:
    """Return the exact source coefficient, not a prime-count certificate.

    D>24 must be a primitive quadratic conductor; N is a nonnegative even
    residue representative. No zero or analytic range hypothesis is checked.
    """
    suppression_classes(conductor, two_sign=two_sign)  # Validate conductor/sign.
    if type(target) is not int or target < 0 or target % 2:
        raise ValueError("require a nonnegative even integer target")
    factors = _factorization(conductor)
    r = next((e for p, e in factors if p == 2), 0)
    phi_two = 1 if r == 0 else 2**(r-1)
    if target % phi_two:
        return Fraction(1)
    chi_minus = -1 if r == 2 else (two_sign if r == 3 else 1)
    product = Fraction((-1)**(target//phi_two))
    for p, _ in factors:
        if p == 2:
            continue
        chi_minus *= -1 if p % 4 == 3 else 1
        if target % p:
            product *= Fraction(-1, p-2)
    return 1+chi_minus*product


def density_collapse_target(conductor: int, *, two_sign: int = 1
                            ) -> int | None:
    """First F_D target >= D**10, or None when that residue family is empty.

    A returned target is even and <2*D**10, with source coefficient zero.
    This is NOT a zero detection, prime-pair count, or numerical analytic
    certificate. The conditional implication is proved in the linked note.
    """
    _, period, residues = suppression_classes(conductor, two_sign=two_sign)
    if not residues:
        return None
    lower = conductor**10
    return min(lower + (residue-lower) % period for residue in residues)


def proper_power_position_cap(target: int) -> int:
    """Bound ordered pair positions involving a proper prime power at N.

    Multiplication by log(N)**2 bounds their von Mangoldt weight. This
    deliberately overcounts bases, duplicate powers, and the center pair.
    It neither counts actual prime pairs nor validates an analytic error.
    """
    if type(target) is not int or target < 6 or target % 2:
        raise ValueError("require an even integer target N>=6")
    return 2*(target.bit_length()-2)*isqrt(target)


def separated_zero_ranges(c: int | Fraction, eta_first: int | Fraction,
                          eta_second: int | Fraction, alpha: int | Fraction,
                          *, log_gap_factor: int | Fraction = 1) -> bool:
    """Check a sufficient separation condition using exact rational bounds.

    CONDITIONAL input meaning: 0<c<c0 for a valid Landau/Page constant;
    eta_first/second are truthful LOWER bounds on the two actual zero
    strengths, for DISTINCT characters in nondecreasing conductor order.
    No zero, conductor, or validity of c is verified. Synthetic rational
    test parameters are not claimed to be available analytic constants.

    True implies the second ambient lower endpoint exceeds the first
    actual upper endpoint raised to log_gap_factor. False is inconclusive,
    not evidence of overlap. The two intervals use the SAME fixed alpha.
    For alpha=m/n, 10*c*eta_first**alpha>=gap is tested exactly by
    (10*c)**n * eta_first**m >= gap**n, avoiding floating powers.
    """
    values = (c, eta_first, eta_second, alpha, log_gap_factor)
    if (any(type(v) not in (int, Fraction) for v in values)
            or not 0 < c <= 1 or eta_first < 10 or eta_second < 10
            or not 0 < alpha < 1 or log_gap_factor < 1):
        raise ValueError("require exact rationals: 0<c<=1, eta_i>=10, 0<alpha<1, gap>=1")
    c, eta_first, eta_second, alpha, gap = map(Fraction, values)
    if c*eta_second < 1:
        return False
    return (10*c)**alpha.denominator * eta_first**alpha.numerator >= gap**alpha.denominator
