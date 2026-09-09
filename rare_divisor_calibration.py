"""Calibrate an ACTUAL divisor correlation against one-variable rare primes.

Owner: Kevin's Goldbach research. Purpose: preserve the conditional arithmetic
component and exact normalization guards for the next prime-replacement test.
This is a proof module, not a manuscript, novelty claim or Goldbach theorem.
Follow-on: prime_cutoff_bridge.py now supplies the previously missing
cutoff comparison in the SAME restricted actual-zero regime and composes
the results below into a conditional prime-pair asymptotic. The original
boundary of the calibration proof itself is retained explicitly below.

PARAMETERS AND STATEMENT.
Let chi be primitive quadratic modulo D>24 with an ACTUAL zero
 beta0=1-1/(eta log D), Y=D^V, V>=log^3 eta, t=V/eta<=1/log Y.
Let L=log Y, m even in[5Y/4,7Y/4] and m in F_D. Write
 A=sum_v chi0(v)chi0(m-v)>0, B=sum_v chi(v)chi0(m-v)=0,
 C=sum_v chi(v)chi(m-v)=-A.
Then A/phi(D) is 1 or 1/2. Let g(y/Y) be nonnegative, uniformly smooth,
supported where y and m-y lie strictly between Y/2 and Y, and I_g=int g.
All statements are uniform for bounded smooth seminorms; I_g>>Y is needed
only when interpreting a positive main term. Fix sufficiently large source
constants and K, and set U=K log eta, z=Y^(1/U), so eventually z>D.
P(z) contains primes STRICTLY LESS THAN z. Rough means coprime to P(z).
Put lambda=1*chi and W=chi*log=lambda*Lambda. Both are nonnegative. Define
 Q_z=sum_(x rough, (x(m-x),D)=1) g(x/Y) log(x) lambda(x),
 S_z=1/2 sum_(x(m-x) rough, (x(m-x),D)=1)
                         g(x/Y) log(x) lambda(x) W(m-x).
The partner m-x is NOT required rough in Q_z. Let P_g be the same smooth
sum of log(p)log(m-p) over positive-sign-first actual prime pairs. Then
 Q_z=(A/phi(D))*t*I_g+o(Y*t/G_z),
 S_z=G_z*Q_z+o(Y*t)=S_2(m)*t*I_g+o(Y*t),                 (1)
where G_z below is positive. Also P_g<=S_z EXACTLY. This proves only a
prime-pair UPPER bound until S_z-P_g is controlled. Limits are ineffective
as eta tends to infinity in the stated regime. No zero existence is claimed.

SOURCE INPUTS.
Matomaki--Merikoski https://arxiv.org/html/2112.11412v2, Proposition2.3,
equation(15), Lemmas2.2,2.4,3.1,3.2, checked2026-09-09. Use the corrected
PLUS upper-beta remainder in equation(22), as proved and exactly witnessed
in rough_cofactor_sieve_bridge.py; the relative-O assertion remains valid.
Use the bulk Linnik deduction in relative_type_i.py from Thorner--Zaman,
https://arxiv.org/html/2108.10878#S2 . The acknowledged Tao Proposition23
gap remains excluded. Corrected Henriot conventions remain as recorded in
the earlier bridge. No source prime-to-divisor error of order Yt times a
logarithmic factor is imported as a relative-o estimate.

ACTUAL TWO-VARIABLE CALIBRATION.
1. Fix smooth H with H(s)+H(1/s)=1, H=1 for s<=1/2, H=0 for s>=2.
   Swapping divisors gives exact hyperbolas
    lambda(x)=sum_(ab=x)H(a/b)[chi(a)+chi(b)],
    W(n)=sum_(cd=n)H(c/d)[chi(c)log(d)+chi(d)log(c)].
   Insert principal characters on unweighted arguments, allowed on units.
   Let
    A_z(y)=sum_(a rough)chi(a)/a H(a^2/y),
    B_z(n)=sum_(c rough)chi(c)/c H(c^2/n)log(n/c^2),
    V0=prod_(p<z)(1-1/p), C_z=1/V0,
    V1=prod_(p<z,p not dividing D)(1-1/p),
    V2=prod_(p<z,p not dividing D)(1-rho_m(p)/p),
   where rho_m(p)=1 if p|m and 2 otherwise.
2. Apply Proposition2.3 to the four smooth orientations and O(L^2)
   dyadic small-factor boxes, retaining a=c=1. The coefficient-one relation
   is x+n=m; no variable-coefficient substitution occurs. Normalize the
   outside log(x) and W logs by L^2 for bounded derivative constants.
   The residue means of the principal/principal, mixed, mixed and double
   character terms are A/D, B/D, B/D, C/D. More explicitly the combined
   coefficients of log(n), log(c), for fixed unit a,c, are
     chi(a)chi(c)/(acD) * (A+B, C-A).
   On F_D this is A chi(a)chi(c)/(acD)*(1,-2). Sum all orientation
   main terms and boxes BEFORE taking absolute values. The zero mode is
    S0=(A/D)*V2*int g(y/Y)*(log y/2)*A_z(y)*B_z(m-y)dy.    (2)
   The direct source errors, as in rare_shifted_divisor_bound.py, cost
    O(Y^(7/9)D^2 L^4+S_2(m)Y L^2[U^6/z+exp(-a0 U/3000)]).
   Any removed shared rough prime costs at most Y/z*exp(O(U))*L^2,
   since its square divides x(m-x) and it divides m. This is negligible.
3. Lemma2.4 at base Y, with N comparable to sqrt(Y) and logarithmic
   parameter sqrt(n), gives by smooth Abel summation
     B_z(n)=2 C_z*(1+O(E)), E=O(t U^4+eta^-B0),            (3)
   for any desired fixed B0 after choosing constants. The source permits
   1<=y<=Y^2 independently of N. The factor TWO in(3) is essential:
   log(n/d^2)=2log(sqrt(n)/d). All partial endpoints needed by Abel
   lie where d is comparable to sqrt(n); the total Abel mass is H(1/n)=1.
   At the same N, subtract the lemma at logarithmic parameters Y,Y^2.
   Their common C_z main cancels, giving partial sums O(E/U). Another
   Abel summation yields A_z(y)=O(E/U), including the atom a=1.
   Hence replacing B_z in(2) by 2C_z costs O(S_2(m)Y E^2).
   This uses int |g log(y) A_z(y)|, NOT the absolute value of its signed
   integral. Since S_2(m)<<log eta and t<=1/sqrt(eta log D), this is o(Yt).

ONE-VARIABLE SIEVE WITH ITS RELATIVE ERROR.
4. Apply the same lambda hyperbola to Q_z; keep physical a rough and sieve
   b with upper/lower beta weights at R=Y^(1/1000). For each d in the
   sieve support, (ad,D)=1; the partner unit mask has period D. Complete
   means over b are chi(a)A/D and chi(a)B/D=0, respectively. Smooth
   progression summation has floor error O(D), for a total
   O(D R sqrt(Y) L). Thus the combined main is
    Q0=(A/D)*V1*int g(y/Y)log(y)A_z(y)dy.                 (4)
   For completeness, the signed sieve remainder can be bounded after
   triangle by a rough integer mean with multiplicity tau(N)^(a0+2).
   Lemma3.2(i) starts at r>=U/1000-beta_sieve, with coefficient 2^(-a0 r).
   Lemma3.1(i), second divisor exponent zero, bounds the dyadic mean by
    Y/L * [U*(beta_sieve/(beta_sieve-1))^r]^C_a0.
   Choosing beta_sieve sufficiently large in a0 makes the r-sum geometric;
   choosing K sufficiently large gives Y eta^-B0 after the outside log.
   Clamp intermediate cutoffs below2, where this bound only becomes weaker.
   Lemma3.2(ii), with g(p)=0 at p|D and 1/p otherwise, gives
   (1+O(exp(-c_a0 U)))V1. The absolute a-harmonic mass is O(U), so its
   replacement error is also Y eta^-B0. No pointwise cancellation of signed
   sieve weights is assumed. This proves Q_z=Q0+power-small+Y eta^-B0.
5. Set G_z=V2*C_z/V1. Since z>D,
    (A/D)*V2=prod_(p<z)(1-rho_m(p)/p), V0=V1*phi(D)/D,
    G_z=Sigma_(2,z)(m)*phi(D)/A,
    Sigma_(2,z)=prod_(p<z)(1-rho_m(p)/p)/(1-1/p)^2.
   The singular-series tail is 1+O(U/z), uniformly m comparable to Y,
   since the number of primes >=z dividing m is O(U). In particular
   G_z<<S_2(m)<<log eta. Equations(2)--(4) now give
    S_z=G_z Q_z+O(S_2 Y t^2 U^8+Y^(7/9+o(1))+S_2 Y eta^-20).
   This is o(Yt), without claiming that Q0 is positive term by term.

ONE-VARIABLE PRIME REPLACEMENT, VALID AT GROWING U.
6. Discard squareful x: their weighted mass is at most
   Y/z*exp(O(U))*L. For squarefree x, lambda(x)>0 only when ALL prime
   factors have sign+. If x is composite choose its unique largest prime
   q and put x=Mq. Then M>=z, M<=Y/z and lambda(x)=2lambda(M).
   Drop the largest-factor and partner-unit restrictions for an upper bound.
   At Q=Y/M>=z the bulk Linnik estimate modulo D gives
    #{Q/2<q<=Q: q prime, chi(q)=+1}
      << Q(1-beta0)+Q/log(Q)*[eta^(-c V/U)+L^2/D].
   A nonnegative Lambda upper bound suffices here; no subtraction of prime
   powers is required. Lemma2.2, with v=V/U, gives
    sum_(z<=M<=Y/z, M rough)lambda(M)/M << t U^2+eta^-B0.
   Consequently the composite contribution to Q_z is at most
    O(Y t^2 U^2+Y t U^3[eta^(-c V/U)+L^2/D]+Y eta^-B0).
   This is o(Yt/G_z). Indeed V/U>>log^2 eta, G_z<<log eta, and the
   retained ineffective Siegel bounds imply D>>_H L^H and t>>_a D^-a.
   In particular z dominates EVERY fixed power of eta; squareful errors
   above must be paid using this fact, not by pretending 1/U is fixed.
7. The prime part of Q_z is exactly twice the positive-prime log mass
   with (m-p,D)=1. Bulk Linnik modulo D, smoothed, gives
    (A/phi(D))*int g(y/Y)(1-y^(beta0-1))dy
      +O(Y[t^28+L^2/D]+Y^(1/2+o(1))).
   Uniformly y comparable to Y, 1-y^(beta0-1)=t[1+O(t+1/L)].
   Multiplication by G_z is harmless: G_z(t+1/L)=o(1), as are the
   displayed errors divided by Yt. This proves both assertions in(1).

SEPARATE FIXED-CUTOFF COMPONENT AND THE UNRESOLVED TRANSFER.
8. At the ORIGINAL fixed cutoff z_old=ceil(Y^theta), fixed theta>0,
   define S_theta using prime factors STRICTLY GREATER THAN z_old in both
   variables. The first-variable composite error in S_theta is o(Yt).
   Changing a prime-equality endpoint costs Y^(1-theta+o(1)), if needed.
   Remove squareful/shared factors at Y^(1-theta+o(1)); now W(n)<=C_theta L.
   Write composite x=Mq as above, so Q=Y/M>=Y^theta. Retain (M,Dm)=1.
   Sieve n=m-Mq only to Z_Q=Q^(alpha/beta_sieve)<=z_old at level Q^alpha,
   for sufficiently small FIXED alpha(theta). The progression modulus
   is Dd, NEVER MDd, and D=Q^o(1). Bulk Linnik and the upper sieve bound
   the prime-log q sum by O(Q S_2(m)t/L), with power-small and arbitrarily
   high t-power errors. Pay log(x)/log(q)<=1/theta and W(n)<=C_theta L.
   Finally sum_(M>1, M rough_old)lambda(M)/M=O_theta(t) by Lemma2.2.
   The full first-variable replacement error is O_theta(Y S_2(m)t^2)
   plus o(Yt). This lemma compares S_theta with the FULL rare-first W
   sum; it does not silently identify that pool with the pruned B_good.
   To pay that distinction, rare_factor_pruning.py bounds the removed
   prime-log mass by 2 X V(z_old) H+R_bad, with H=o(1). Multiply by
   C_theta L: L X V(z_old)<<_theta Yt and L R_bad=o(Yt) by its explicit
   t^8 L and Siegel error budget. Hence the removed W-weight is o(Yt).
   Combining rare_class_elimination.py proves S_theta=P_g+o_theta(Yt).
   Fixed smooth weights preserve the absolute error estimates used here.
9. Step8 does NOT extend to U=K log eta by substitution: the pointwise
   divisor cost can be 2^U, and t U^3 2^U need not vanish. Conversely the
   sieve error for fixed theta in steps2--4 is not relative-o(Yt).
   An elementary W-mean in short affine intervals has a sqrt(Y) endpoint
   error, larger than Q when Q is near Y^(1/U). Corrected Henriot's
   fixed coefficient-norm exponent hypothesis also need not hold there.
   Needed next: a uniform W-weighted affine estimate with only polynomial
   U losses, or arithmetic cancellation before taking divisor absolutes.
   Neither the fixed-theta prime replacement nor the dynamic calibration
   alone controls S_z-P_g. Earlier T_W=P+o(Yt) applies to its ORIGINAL
   fixed-theta pruned pool. Formal conservation6f9a77b remains an identity,
   and every polynomial component remains available for a new combination.

Finite routines below verify algebra only. Their rational H is nonsmooth;
finite characters do not certify exceptional zeros or asymptotic estimates.
"""
from fractions import Fraction as F
from math import gcd, isqrt, prod

from exceptional_character_model import character_values
from major_arc_kernel import _factorization
from rare_shifted_divisor_bound import reflection_weight


def conductor_coefficients(conductor, target, small_a, small_c, *, two_sign=1):
    """Direct residue sums and predicted (log n, log c) coefficients."""
    chi = character_values(conductor, two_sign=two_sign)
    if any(type(v) is not int or v < 1 for v in (target, small_a, small_c)):
        raise ValueError('positive integer target and small factors required')
    if gcd(small_a, small_c) != 1 or gcd(small_a*small_c, conductor) != 1:
        raise ValueError('small factors must be mutually coprime conductor units')
    a, c, D = small_a, small_c, conductor
    A = sum(bool(chi[v]) and bool(chi[(target-v) % D]) for v in range(D))
    B = sum(chi[v]*bool(chi[(target-v) % D]) for v in range(D))
    C = sum(chi[v]*chi[(target-v) % D] for v in range(D))
    direct_n = direct_c = 0
    for b in range(c*D):
        if (target-a*b) % c:
            continue
        d = (target-a*b)//c
        first = chi[a % D]*bool(chi[b % D])+chi[b % D]
        second_n = chi[c % D]*bool(chi[d % D])
        second_c = chi[d % D]-second_n
        direct_n += first*second_n
        direct_c += first*second_c
    norm = F(1, a*c*D)
    signed = chi[a % D]*chi[c % D]*norm
    return (A, B, C), (direct_n*norm, direct_c*norm), ((A+B)*signed, (C-A)*signed)


def euler_calibration(conductor, target, cutoff, *, two_sign=1):
    """Return actual G_z and its finite singular-series normalization."""
    chi = character_values(conductor, two_sign=two_sign)
    if type(cutoff) is not int or cutoff <= conductor:
        raise ValueError('integer cutoff must exceed conductor')
    if type(target) is not int or target <= 0 or target % 2:
        raise ValueError('positive even target required')
    A = sum(bool(chi[v]) and bool(chi[(target-v) % conductor]) for v in range(conductor))
    if A == 0:
        raise ValueError('no conductor-unit pairs')
    primes = [p for p in range(2, cutoff) if _factorization(p) == ((p, 1),)]
    V0 = prod((F(p-1, p) for p in primes), start=F(1))
    V1 = prod((F(p-1, p) for p in primes if conductor % p), start=F(1))
    V2 = prod((F(p-(1 if target % p == 0 else 2), p)
               for p in primes if conductor % p), start=F(1))
    sigma = prod((F(p*(p-(1 if target % p == 0 else 2)), (p-1)**2)
                  for p in primes), start=F(1))
    return V2/(V0*V1), sigma*F(sum(bool(v) for v in chi), A)


def _add_log(vector, integer, coefficient):
    for p, exponent in _factorization(integer):
        vector[p] = vector.get(p, F(0))+coefficient*exponent


def _clean(vector):
    return tuple((p, c) for p, c in sorted(vector.items()) if c)


def weighted_abel_identity(root, cutoff, conductor):
    """Exact log-prime coefficient vectors for direct B and twice its Abel sum."""
    if any(type(v) is not int or v < 2 for v in (root, cutoff)):
        raise ValueError('integer root and cutoff >=2 required')
    chi = character_values(conductor)
    endpoint = isqrt(2*root*root)+1
    direct, abel, partial = {}, {}, {}
    for j in range(1, endpoint+1):
        weight = reflection_weight(j*j, root*root)
        next_weight = reflection_weight((j+1)**2, root*root)
        if all(p >= cutoff for p, _ in _factorization(j)):
            coefficient = F(chi[j % conductor], j)
            _add_log(partial, root, coefficient)
            _add_log(partial, j, -coefficient)
            _add_log(direct, root, 2*weight*coefficient)
            _add_log(direct, j, -2*weight*coefficient)
        for p, coefficient in partial.items():
            abel[p] = abel.get(p, F(0))+2*(weight-next_weight)*coefficient
    return _clean(direct), _clean(abel)


def lambda_w_identity(n, conductor):
    """Return chi(n), lambda(n), and exact vectors for 2W(n), lambda(n)log(n)."""
    if type(n) is not int or n < 1:
        raise ValueError('positive integer n required')
    chi = character_values(conductor)
    lam, twice_w, lam_log = 0, {}, {}
    for d in range(1, n+1):
        if n % d == 0:
            lam += chi[d % conductor]
            _add_log(twice_w, n//d, 2*chi[d % conductor])
    _add_log(lam_log, n, lam)
    return chi[n % conductor], lam, _clean(twice_w), _clean(lam_log)


def signed_calibration(weights, harmonic, moments, density, v1, v2, cz):
    """Finite quadrature guard: the replacement error requires absolute mass."""
    if not len(weights) == len(harmonic) == len(moments) or not weights:
        raise ValueError('nonempty matching quadrature vectors required')
    if any(type(v) is not F for seq in (weights, harmonic, moments) for v in seq):
        raise ValueError('exact Fraction quadrature values required')
    if any(type(v) is not F or v <= 0 for v in (density, v1, v2, cz)):
        raise ValueError('positive exact Fraction normalizations required')
    q0 = density*v1*sum((w*a for w, a in zip(weights, harmonic)), F(0))
    s0 = density*v2/2*sum((w*a*b for w, a, b in zip(weights, harmonic, moments)), F(0))
    ratio = v2*cz/v1
    bound = density*v2/2*sum((abs(w*a) for w, a in zip(weights, harmonic)), F(0))*max(abs(b-2*cz) for b in moments)
    return q0, s0, ratio, s0-ratio*q0, bound
