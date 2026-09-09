"""Remove the balanced self-correlation from the actual smoothed remainder.

Owner: Kevin's Goldbach research. Purpose: compose the reviewed actual
divisor convolution with the existing Type I estimate, without replacing
the prime model by an unrelated formal main term. Proof and exact guards
only. Independent Sol theory and actual-file review: PASS. Eight exact
guards passed normally in0.009s and under Python -O in0.010s. Those finite
guards do not replace the analytic proof or its reviewed prerequisites.

QUESTION, MECHANISM, AND DISPOSITION.
Can the signed gcd main in free_divisor_correlation.py remove a term of
the actual prime comparison? YES in the precise sense of(10) below. Its
low-modulus projection need NOT equal Gamma_S. Instead that projection
is itself Type I, and its correlation with the unchanged E=Lambda-Gamma_S
is already small. Subtracting it leaves a balanced component with small
self-correlation. Its correlations with the rest remain OPEN.
This pursuit links the older absolute TI input with the newly reviewed
actual coefficient bound. A bare Ramanujan identity would not suffice.

SETUP AND EXACT PROJECTION.
1. Retain ONLY the unexceptional branch of ramanujan_type_i.py and
   unexceptional_vaughan_gate.py: gamma=1/2-eps, 0<eps<1/12,
   fixed 0<delta<=1/4800, S=Y^delta, W=floor(Y^(gamma/2)), L=log(2Y).
   Extend E=1_I(Lambda-Gamma_S) by zero off I=(Y/2,Y]. Fix smooth F
   compactly supported in(1/2,1)^2 and m/Y in[5/4,7/4]. Define
    C_F(U,V)=sum_n F(n/Y,(m-n)/Y) U(n)V(m-n),
    I_F(tau)=integral F(t,tau-t)dt.
   No conjugation or positivity of C_F(U,U) is assumed. F need not be
   symmetric. This is a FIXED SMOOTH comparison, not an unproved upgrade
   of a sharp-cutoff result. All uses of TI below are valid by Abel
   summation with bounded total variation of this fixed physical weight.
2. Keep the actual Vaughan sequence
    A(n)=sum_(r|n)h_r, h_r=sum_(ad=r,a>W,d>W)mu(a)Lambda(d).
   Thus |h_r|<=log r and T_F=C_F(A,E). The saved Vaughan argument also
   gives C_F(Lambda,E)=T_F+O_A(Y/log(Y)^A), with its already paid
   prime-power replacement if actual primes are used. Set
    B(n)=sum_(r|n,Y^gamma<r<=Y^(51/100))h_r,
    H(n)=A(n)-B(n).
   H keeps the floor strip AND all larger product coefficients. In
   particular it keeps k=1 when n=r is comparable to Y. No omitted
   factor region is called negligible merely by this definition.
3. For any finitely supported coefficients alpha_M define
    H_alpha(q)=sum_(q|M)alpha_M/M.
   From c_q(n)=sum_(d|(q,n))d mu(q/d) and Mobius inversion,
    sum_(q|g)c_q(m)=g*1_(g|m),
    sum_(M|n)alpha_M=sum_q H_alpha(q)c_q(n).                (1)
   The second sum is finite, including nonsquarefree q. Consequently
    sum_(gcd(M,N)|m)alpha_M beta_N gcd(M,N)/(MN)
      =sum_q c_q(m)H_alpha(q)H_beta(q).                    (2)
   These are exact identities, not prime estimates. They follow directly
   from the divisor formula already used in major_arc_kernel.py; there
   is no new external analytic prerequisite for these algebraic steps.
4. Write H_B(q)=sum_(q|r,Y^gamma<r<=Y^.51)h_r/r. Uniformly in q,
    |H_B(q)| << L^2/q.                                   (3)
   One L bounds |h_r| and one bounds the harmonic sum after r=qk.
   The sharper O(L/q) bound for one dyadic box is not used for this
   aggregate. Put Q=floor(S^2) and
    P_Q(n)=sum_(q<=Q)H_B(q)c_q(n), Z(n)=B(n)-P_Q(n).        (4)
   Expanding the Ramanujan sum in divisors gives EXACTLY
    P_Q(n)=sum_(d|n,d<=Q)p_d,
    p_d=d sum_(q<=Q,d|q)H_B(q)mu(q/d), |p_d|<<L^3.         (5)
   The bound is d sum_(k<=Q/d)L^2/(dk)<<L^3. Since Q<=Y^gamma
   eventually, the existing absolute TI estimate and Abel summation give
    C_F(P_Q,E)=O_A(Y/log(Y)^A) for every fixed A.           (6)
   A larger logarithmic saving is requested in TI to absorb L^3.
5. This does NOT identify P_Q with the prime model. The latter has
    Gamma_S(n)=sum_q gamma_S(q)c_q(n),
    gamma_S(q)=mu(q)G(log(q)/log(S))/phi(q), q<=S^2.
   Its coefficients are not the block-dependent H_B(q). For example,
   the single actual product coefficient h_77=-(log7+log11), W=3,
   has a negative H(1), while gamma_S(1)=1. This finite distinction is
   not a lower bound for any asymptotic mismatch of aggregate B. Equation
   (6), not a claim of equality with Gamma_S, is the licensed transfer.

AN ACTUAL SMALL SELF-CORRELATION, WITH ALL ERRORS PAID.
6. Prime-power evaluation of c_q shows |c_q(m)|<=gcd(q,m). Since
   gcd(q,m)=sum_(d|(q,m))phi(d), for every Q>=1,
    sum_(q>Q)gcd(q,m)/q^2 <= 2*tau(m)/Q.
   Indeed for d<=Q use sum_(k>Q/d)k^-2<=2d/Q; for d>Q use
   sum_(k>=1)k^-2<2 and phi(d)/d^2<=1/d<1/Q. Thus(3) gives
    |sum_(q>Q)c_q(m)H_B(q)^2| << L^4*tau(m)/Q.             (7)
   This tail is uniform in the target; taking gcd(q,m)=1 would be wrong.
7. Partition B into O(L) dyadic product boxes. The independently
   reviewed free_divisor_correlation.py theorem applies to every pair
   and allows the sharp coefficient support cuts. It gives
    C_F(B,B)=Y I_F sum_q c_q(m)H_B(q)^2
                          +O_(F,epsilon)(Y^(1983/2000+epsilon)).
   The dyadic sums are absorbed by choosing source epsilon smaller.
   For the other three terms use the exact complete-period identities
    mean_k c_q(m-Mk)=1_(q|M)c_q(m),
    mean_n c_q(n)c_r(m-n)=1_(q=r)c_q(m).
   The second identity follows by matching equal primitive additive
   frequencies; its factor is c_q(m), NOT phi(q)c_q(m).
8. All interval errors are paid without an assumed common short period.
   Per (M,q), the AP period is at most q and amplitude at most q.
   Smooth summation therefore costs O_F(q^2), while its main term is
   (Y/M) I_F*1_(q|M)c_q(m). Summing with(3) and
   sum_r |h_r|<<Y^.51 L gives O_F(Y^.51 L^3 Q^2).
   This handles B-P and P-B; reflection of the fixed weight preserves
   its integral and required smooth norms. For P-P the period for q,r
   is at most qr and amplitude at most qr, giving discrepancy O_F(q^2 r^2).
   Summing the coefficients gives O_F(L^4 Q^4).
   Each of BP, PB, PP has main Y I_F sum_(q<=Q)c_q(m)H_B(q)^2.
   Expanding ZZ=BB-BP-PB+PP and using(7), we obtain
    |C_F(Z,Z)| <<_(F,epsilon) Y^(1983/2000+epsilon)
           +Y L^4 tau(m)/Q+Y^(51/100)L^3Q^2+L^4 Q^4.       (8)
   Since Q=Y^(2delta+o(1)), its four exponent budgets are
    1983/2000, 1-2delta, 51/100+4delta, 8delta.
   They are all below1; tau(m)<<_epsilon Y^epsilon and logarithms
   are absorbed with epsilon below the fixed margin. In particular
    C_F(Z,Z)=O_(F,epsilon)(Y^(1-sigma+epsilon)),
    sigma=min(17/2000,2delta,49/100-4delta,1-8delta)>0.     (9)
   For the allowed delta, sigma=2delta. This is an ACTUAL bound on the
   signed self-correlation, not merely a formal reconstruction of a main.

COMPOSITION INTO THE UNCHANGED PRIME ERROR.
9. Define R(n)=E(n)-Z(n), with E unchanged. Bilinearity gives EXACTLY
    T_F=C_F(A,E)
       =C_F(Z,R)+C_F(H,E)+C_F(Z,Z)+C_F(P_Q,E).
   By(6) and(8), for every fixed A and epsilon>0,
    T_F=C_F(Z,R)+C_F(H,E)
          +O_A(Y/log(Y)^A)+O_(F,epsilon)(Y^(1-sigma+epsilon)). (10)
   This removes the balanced self-correlation from the ACTUAL smoothed
   remainder. It does not assume E is independent of a divisor weight.
   An arbitrary-logarithm TI saving is not silently called a power saving.
10. On I the remaining sequence is
     R=Lambda-Gamma_S-B+P_Q.
    It includes the mixed Vaughan pieces, H, and the P_Q-Gamma_S
    mismatch. Both C_F(Z,R) and C_F(H,E) remain UNESTIMATED. A small
    self-correlation at one additive target gives no Cauchy/positivity
    control of either cross-correlation. On n=pq with distinct primes
    p,q>W, the only nonzero h_r with r|n is h_n=-log n. When n is
    comparable to Y, this entire two-prime composite lies in H. Prime
    squares likewise have h_(p^2)=-log p. These concrete short-k cases
    have not been removed by the balanced theorem.
    No unexceptional prime-pair lower bound, new coverage or effective
    onset follows. The earlier actual-zero conditional coverage and all
    retained polynomial/model components remain unchanged.

Finite helpers below guard both exact projection representations, the gcd
main, the changed coefficient norms, and exponent margins. Small fixtures
are neither asymptotic numerical experiments nor new Goldbach scans.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import gcd

from major_arc_kernel import _mobius_phi, ramanujan
from unexceptional_vaughan_gate import _positive


def _coefficients(values):
    if type(values) is not dict or not values:
        raise ValueError('nonempty finite coefficient dictionary required')
    for n, value in values.items():
        _positive(n, 'coefficient index')
        if type(value) is not F:
            raise ValueError('exact Fraction coefficients required')


def _samples(values):
    if type(values) is not tuple or len(values) < 2 or values[0] != 0:
        raise ValueError('tuple with unused zero index and at least q=1 required')
    if any(type(value) is not F for value in values):
        raise ValueError('exact Fraction samples required')


def harmonic_projection(coefficients, cutoff):
    """H_alpha(q)=sum_(q|M)alpha_M/M; no primality model substituted."""
    _coefficients(coefficients)
    _positive(cutoff, 'cutoff')
    return (F(0),)+tuple(sum((value/n for n, value in coefficients.items() if n % q == 0), F(0))
                        for q in range(1, cutoff+1))


def projection_divisors(samples):
    """Exact Type I coefficients p_d, retaining nonsquarefree frequencies."""
    _samples(samples)
    return {d: d*sum((samples[q]*_mobius_phi(q//d)[0]
                       for q in range(d, len(samples), d)), F(0))
            for d in range(1, len(samples))}


def divisor_value(coefficients, n):
    _coefficients(coefficients)
    _positive(n, 'n')
    return sum((value for d, value in coefficients.items() if n % d == 0), F(0))


def projection_value(samples, n):
    _samples(samples)
    if type(n) is not int:
        raise ValueError('integer argument required')
    return sum((samples[q]*ramanujan(q, n) for q in range(1, len(samples))), F(0))


def gcd_main(left, right, target):
    _coefficients(left)
    _coefficients(right)
    _positive(target, 'target')
    return sum((a*b*F(gcd(m, n), m*n) for m, a in left.items() for n, b in right.items()
                if target % gcd(m, n) == 0), F(0))


def ramanujan_main(left, right, target):
    _samples(left)
    _samples(right)
    _positive(target, 'target')
    return sum((left[q]*right[q]*ramanujan(q, target)
                for q in range(1, min(len(left), len(right)))), F(0))


@dataclass(frozen=True)
class ProjectionBudget:
    convolution: F
    tail: F
    mixed_period: F
    projection_period: F
    saving: F


def projection_budget(delta):
    """Power budgets for ZZ only; TI retains its separate logarithmic saving."""
    if type(delta) is not F or not 0 < delta <= F(1, 4800):
        raise ValueError('exact 0<delta<=1/4800 required')
    exponents = (F(1983, 2000), 1-2*delta, F(51, 100)+4*delta, 8*delta)
    return ProjectionBudget(*exponents, 1-max(exponents))
