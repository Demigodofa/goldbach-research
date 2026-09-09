"""Rapid complementary modulation evades uniformly controlled C3 probes.

Owner: Kevin's Goldbach research. Purpose: test the inverse implication
from the actual controlled-phase projection bounds to paired cancellation.
This is an ARTIFICIAL dense positive model, not primes or zeta zeros.
The earlier real-part localization and arithmetic tools remain valid.

1. ONE MODEL AND THE PRECISE PROJECTION FAMILIES.
Keep T=N^(9/10), K=N^(1/10), V=N^(1/8), and the exact window
 P_b(aN)=T/(2pi)*sum_(n>=2) b(n)/sqrt n
          *hatChi(Tlog(n/(aN)))*nu(Tlog(n/(aN))/V).
Use the same angular Fourier convention and fixed cutoff nu as in
complementary_window_chirp.py. Fix chi>=0 smooth supported in(1,2),
with chi(3/2)>0, and zeta>=0 smooth supported in(1/4,3/4), equal1
near1/2. Let lambda_N be nearest3 on the odd-pi/T lattice, and put
 f_N(a)=lambda_N*a+K^-1*sin(K*(a-1/2)),
 b_N(n)=1+(1/2)*cos(T*f_N(n/N)).                                (1)
Then1/2<=b_N<=3/2 and |lambda_N-3|<=pi/T.

For any fixed compact positive interval I and fixed C, let g_N be
REAL C3 on a fixed neighborhood of I, with derivatives1,2,3 bounded
in absolute value by C. The constant term may be arbitrary. Let psi_N
be complex C1, supported in the interior of I, with common bound
 sup|psi_N|+int|psi_N'|<=C.
All these functions may depend on N. Uniformly over this family,
 |sum_n psi_N(n/N)*(b_N(n)-1)*exp[-i*T*g_N(n/N)]|
             <<_(I,C) N*(K/T)^(1/3)+T = O_(I,C)(N^(9/10)).     (2)
There is no claim for unbounded first, second or third derivatives,
or for amplitudes with unbounded total variation.

The NORMALIZED exact model window F_b(a)=P_b(aN)/sqrtN satisfies
 |int w_N(a)*exp[-i*T*g_N(a)]*F_b(a)da| << N^(-1/10),           (3)
on fixed buffered central supports as in window_phase_projection.py,
for common C1 bounds on w_N, the same C3 bounds on g_N, and the
additional lower bound |g_N'|>=c>0. In particular(3) holds on the
smaller previously proved prime-phase class that also assumes
|g_N'+a*g_N''|>=c. Thus this model satisfies a STRONGER power saving
than the actual window's proved O(N^-1/44 L^3) for that class.

Nevertheless, its exact no-conjugation paired functional obeys
 Q_b(N)=2*int zeta(a)*P_b(aN)*P_b((1-a)N)/sqrt(a*(1-a))da
       =-c_(chi,zeta)*N+O_(chi,zeta)(N^(9/10)), c_(chi,zeta)>0.  (4)
These statements concern one N-dependent coefficient model, not a
fixed coefficient sequence or the actual von Mangoldt function.

2. COMPLEMENTARY PHASE AND EXACT WINDOW ERRORS.
With x=a-1/2, oddness of sin and evenness of cos give
 f_N(a)+f_N(1-a)=lambda_N,
 exp(i*T*lambda_N)=-1,
 f_N'(a)=lambda_N+cos(K*x)=f_N'(1-a),
 f_N''(a)=-K*sin(K*x), f_N'''(a)=-K^2*cos(K*x).                (5)
For all sufficiently large N, the first derivative is between1 and5,
but the higher derivative bounds required of g_N fail for f_N.

The sum-to-integral proof in complementary_window_chirp.py applies
unchanged to the exact P_b: the derivative of b_N as a function of
the integer-scale variable is O(T/N), since f_N' is uniformly bounded.
The Schwartz kernel has absolute integral O(N/T) and derivative
integral O(1), including nu. After the prefactor T, the unit-interval
Euler error is O(T/sqrtN)=O(N^(2/5)). No growing f_N'' enters this step.

In the integral set the continuous index to aN+(N/T)y. Taylor now gives
 T*f_N(a+y/T)=T*f_N(a)+f_N'(a)*y+O(K*y^2/T).                    (6)
The logarithmic kernel and square-root weight errors retain their
Schwartz majorants from the earlier calculation. Thus the local phase
error is O(sqrtN*K/T)=O(N^-3/10), the other local error O(sqrtN/T),
and removal of nu costs O(sqrtN*V^-16)=O(N^-3/2).
The compact Fourier support has |y|=O(V), V/T->0; the phase error
is integrated against Schwartz decay, not multiplied by a flat width V.
Fourier inversion, chi(0)=0 and f_N'>0 therefore give uniformly
 P_b(aN)=(1/4)*sqrt(aN)*chi(a*f_N'(a))*exp(i*T*f_N(a))
                                      +O(N^(2/5)),            (7)
for1/4<=a<=3/4. This uses the original discrete window, not a
continuum substitute. Inserting(7) in Q_b and using(5) gives
 Q_b=-(N/8)*int zeta(a)*chi(a*[lambda_N+cos(K*x)])
                *chi((1-a)*[lambda_N+cos(K*x)])da+O(N^9/10).   (8)
Each cross error is at most N^(1/2+2/5), and the squared error is smaller.

3. PERIODIC AVERAGING PRODUCES A FIXED POSITIVE MAIN CONSTANT.
Replace lambda_N by3 in(8), at a cost O(N/T). Define the smooth
2pi-periodic function
 q(a,theta)=zeta(a)*chi(a*[3+cos(theta)])
                      *chi((1-a)*[3+cos(theta)]),
 qbar(a)=(1/(2pi))*int_0^(2pi)q(a,theta)dtheta.
Its a support is fixed compact, and its derivatives are uniformly bounded.
There is a periodic primitive R(a,theta) of q-qbar in theta, with
R and partial_a R bounded and compactly supported in a: integrate the
zero-mean periodic function from0 to theta. The identity
 d/da R(a,K*(a-1/2))=partial_a R+K*(q(a,K*(a-1/2))-qbar(a))
and its vanishing a boundary terms give
 int q(a,K*(a-1/2))da=int qbar(a)da+O(1/K).                    (9)
This proof does not require K to be an integer or the endpoints to
contain complete periods. Therefore(4) holds with
 c_(chi,zeta)=(1/(16pi))*int_a int_0^(2pi)q(a,theta)dtheta da.   (10)
The integrand is nonnegative. At a=1/2 and theta=pi/2 both chi
arguments are3/2 and zeta=1; continuity gives a fixed positive
two-dimensional neighborhood. Hence c>0. The averaging cost N/K=N^9/10
fits the discrete-window cross error; the slope cost N/T is smaller.

4. ALL CONTROLLED C3 PROBES HAVE SMALL CENTERED CORRELATION.
Expand b_N-1 into the two exponentials with coefficient1/4. Each
continuous probe phase is Phi(a)=T*(+/-f_N(a)-g_N(a)). Partition I
at K*(a-1/2)=j*pi/4. There are O_I(K+1) cells. On each cell either
|sin(K*x)|>=1/sqrt2 throughout or |cos(K*x)|>=1/sqrt2 throughout.
For sufficiently large N depending only on C, on a sine cell
 |Phi''|>=T*(K/sqrt2-C)>=c_0*T*K;
on a cosine cell
 |Phi'''|>=T*(K^2/sqrt2-C)>=c_0*T*K^2.                          (11)
The signs +/- do not affect these lower bounds. Continuity ensures
that the corresponding nonvanishing derivative has fixed sign on its cell.

Use the elementary derivative integral estimate, proved in
analytic_complementary_phase.py section3, only at orders r=2,3:
 |int_J A exp(i*Phi)| << (sup_J|A|+int_J|A'|)*M^(-1/r)
when |Phi^(r)|>=M>=1 on J. Its proof for r=2 uses monotonicity of
Phi' after removing its short sublevel interval. For r=3, Phi'' is
monotone; remove |Phi''|<=M^(2/3), of length O(M^-1/3), and apply
the r=2 case on the at most two remaining intervals. Thus C3 phases
and C1 amplitudes suffice. No fourth derivative or monotonicity of
Phi''' is needed; the amplitude need not vanish at partition endpoints.

Summing the cell bounds keeps the repeated supremum cost O(K),
while the integrals of |psi_N'| sum to its global bounded variation.
The whole integral is consequently
 O(K*(T*K)^-1/2+K*(T*K^2)^-1/3)
       =O((K/T)^1/2+(K/T)^1/3)=O(N^-4/15).                    (12)
The amplitude and phase constants are uniform in the declared family.

For the integer sum, apply the elementary Euler inequality to
 h(t)=psi_N(t/N)*exp(i*Phi(t/N)). It gives
 |sum_n h(n)-int h(t)dt|<=int|h'(t)|dt
 <=int|psi_N'|+T*int|psi_N|*(|f_N'|+|g_N'|)=O(T).             (13)
The support remains away from0, so the n>=2 restriction agrees with
the integer sum eventually. Multiplication of(12) by N and addition
of(13) prove(2). The coarser O(T) term is intentional: it already
beats the required O(N^(43/44)L^3) controlled-prime probe bound.

5. THE EXACT MODEL WINDOW PASSES THE SAME PHASE PROJECTION TEST.
Apply the adjoint change v=Tlog(u/a), u=n/N, from
window_phase_projection.py. That calculation does not require primality:
it needs only uniformly bounded first and second derivatives of g_N,
C1 amplitude bounds, a fixed support buffer, and
 (1/N)*sum_(n~N)|b_N(n)|*sqrt(n/N)=O(1).
The last condition holds because b_N is bounded. All its summed Taylor
and Fourier-cutoff errors therefore stay O(T^-1+V^-16). Precisely,
 int w_N(a)e^(-i*T*g_N(a))*F_b(a)da
  =(1/N)*sum_n b_N(n)*psi_N(n/N)*exp[-i*T*g_N(n/N)]
                             +O(T^-1+V^-16),                 (14)
 psi_N(u)=sqrt(u)*w_N(u)*chi(u*g_N'(u)).
This psi_N has a common C1 bound and fixed support: its derivative
involves g_N'+u*g_N'', whose upper bound follows from the hypotheses.
Its lower bound is not used here.

The centered part of(14) is O(N^-1/10) by(2). For the constant
background, the additional |g_N'|>=c permits one integration by
parts, giving int psi_N*exp(-i*T*g_N)=O(1/T). The derivative of
1/g_N' is bounded by C/c^2; no monotonicity assumption is required.
Euler as in(13) adds O(T) to the unnormalized sum. Thus the background
in(14) is O(T^-1+T/N), proving(3), including every discrete error.

6. THE FAILED INVERSE STEP AND THE REMAINING ARITHMETIC QUESTION.
The bounded positive coefficients satisfy the previous interval mass,
fixed multiplicative-range mass, pointwise O(sqrtN) and O(N) energy
inequalities, by the same Schwartz and Schur bounds. Equations(3)-(4)
show that these inequalities and the listed common-C3 phase projection
bounds ALONE cannot imply o(N) for the exact paired functional.
The joint complementary phase survives while the controlled probe
family cannot follow its growing higher derivatives.

This does not contradict the actual prime-phase theorem: the new f_N
lies outside its fixed common C3 bounds. It does not evade all possible
prime tests, satisfy prime support or Type I identities, or represent
the actual zeta-zero spectrum. In particular no claim is made that it
passes the real-part localization or every existing arithmetic constraint.
Polynomial weights, varying-phase bounds and Gram localization remain
available when coupled to further information. No all-method barrier,
actual paired-band improvement, or Goldbach signed lower margin follows.
The precise inverse implication is rejected; the overall goal stays open.
"""
from fractions import Fraction as F
from math import cos, sin


def rapid_phase(a, slope, frequency):
    if frequency <= 0:
        raise ValueError('positive modulation frequency required')
    return slope*a+sin(frequency*(a-0.5))/frequency


def rapid_derivative(a, slope, frequency, order):
    if frequency <= 0 or type(order) is not int or not 1 <= order <= 3:
        raise ValueError('positive frequency and order1,2,3 required')
    x=frequency*(a-0.5)
    if order == 1:
        return slope+cos(x)
    if order == 2:
        return -frequency*sin(x)
    return -frequency**2*cos(x)


def cell_derivative_order(cell):
    if type(cell) is not int:
        raise ValueError('integer quarter-period cell required')
    return 2 if cell % 4 in (1,2) else 3


def rapid_model_budget():
    t,k=F(9,10),F(1,10)
    return {'window_discretization':t-F(1,2),
            'window_phase_taylor':F(1,2)+k-t,
            'window_fourier_tail':F(1,2)-16*F(1,8),
            'paired_cross_error':t, 'periodic_averaging_error':1-k,
            'second_derivative_integral':(k-t)/2,
            'third_derivative_integral':(k-t)/3,
            'centered_integral_sum':1+(k-t)/3,
            'centered_euler_sum':t, 'normalized_projection':t-1,
            'paired_prefactor':F(1,8)}
