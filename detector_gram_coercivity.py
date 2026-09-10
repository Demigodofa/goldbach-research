"""Test the signed detector's operator inference and isolate actual overlap.

Owner: Kevin's Goldbach research. Purpose: determine what the newly closed
prime-product bridge actually licenses. A strengthened artificial model
refutes a disk-only coercivity inference; the actual mixed overlap is
reduced to a short shifted two-prime sum. Its sign remains unproved.

1. THE PROPOSED INFERENCE AND ITS EXACT GRAM FORM.
For the retained actual survivor copies R, write
 c_rho=chi(gamma/T)*N^(beta-1)*exp(i*gamma*logN),
 f_rho(v)=theta(v)*v^(beta-1/2+i*gamma), T=N^(9/10),
 Z_R=sum c_rho*f_rho, Z_HR=sum c_rho*H_N(rho)*f_rho.
Here theta is real, smooth, supported in(1/4,3/4); cutoffs are included
in these fields for this module. Let G_(rho,sigma)=int conj(f_rho)*f_sigma
and D=diag(H_N(rho)). Then
 ||Z_R||^2=c*G*c,
 C_R=Re int Z_HR*conj(Z_R)=Re(c*G*D*c)
    =c*[(G D + D^* G)/2]*c.                                 (1)
The star means conjugate transpose; c* is a row, not multiplication.
The survivor disk gives D=-I+E with diagonal |E_jj|<=3/4.
It does NOT establish ||sum c_j E_jj f_j||<=3/4||sum c_j f_j||.
That latter PACKET-SPACE inequality, with any constant kappa<1,
would imply C_R<=-(1-kappa)||Z_R||^2 and a bounded inverse.
The two conditions are different because G need not commute with E.

2. EXACT TWO-PACKET FAILURE, INCLUDING THE INVERSE CLAIM.
Take the ARTIFICIAL positive-definite Gram matrix
 G=[[1,r],[r,1]], 0<r<1,
 D=diag(-1+i/2,-1-i/2).
Both multiplier values obey the smaller disk |1+D_jj|=1/2. The
Hermitian part of GD has off-diagonal entry-r*(1+i/2) and eigenvalues
-1 plus or minus r*sqrt(5/4), so it has a positive direction for
r>2/sqrt5. More concretely choose r=19/20 and c=(1,-1+i/2):
 c*G*c=7/20, Re(c*G*D*c)=1/8>0.                             (2)
Thus even qualitative nonpositivity fails for the proposed inference.

Such overlap is realized by actual-SHAPED, artificial smooth packets:
fix beta=7/10, any nonzero theta on a positive compact interval, and
two distinct ordinates separated by delta tending to zero. Their
normalized correlation tends to1 by dominated convergence. Rephase
one packet to make that correlation positive real; this commutes with D.
These are not asserted to be zeta zeros or to have the true H_N values.

There is also no uniform synthesized-field inverse bound from bounded
pointwise reciprocals. With c=(D_22,-D_11), direct calculation gives
 ||sum c_j f_j||^2=5/2-3r/2,
 ||sum D_jj*c_j f_j||^2=25*(1-r)/8.                         (3)
Their ratio diverges as r tends to1, although |1/D_jj|<1.
Repeated actual zero copies have equal H_N values and may be merged;
the example uses DISTINCT nearby packets and does not exploit falsely
assigning different multipliers to identical copies.

3. A STRONGER ARTIFICIAL MODEL RETAINS COMMON POLYNOMIAL STRUCTURE.
The failure is not repaired by assuming only a common short Dirichlet
polynomial with real bounded coefficients. Here is an asymptotic model
that also retains the actual form of c_rho above. It still does NOT
retain the detector's specific truncated-Mobius coefficients.

Set beta=7/10, alpha=arctan(1/2), t=pi+alpha,
 m=2*alpha/t, delta=t/logN.
Then 49/200<m<41/150: for instance .46<alpha<.47 and
3.14<pi<3.15 imply 46/181<m<47/180, strictly inside that bad gap.
Take dyadic M=2^floor(m*logN/log2), which is an allowed bad block
eventually. Its exponent differs from m by O(1/logN), with a fixed
margin from the endpoints. Select a fixed interval I inside(1,2)
where |chi| is bounded below, and take gamma0 in T*I.

Put Omega=sum_(M<n<=2M)n^-beta and
 kappa(gamma0)=Omega^-1*sum_(M<n<=2M)n^-beta*exp(-2i*gamma0*logn).
The already proved mean-value bound, averaged over this interval of
length comparable to T, gives
 average |kappa|^2 << (T+M*logM)*M^(1-2beta)/(T*Omega^2)
                   <<1/M.
Here Omega is comparable to M^(1-beta) and M*logM=o(T).
Thus some gamma0 in a buffered subinterval has |kappa|<=1/10.
Both gamma0 and gamma0+delta lie in the chi-nonzero interval eventually.

Let h1=-1-i/2 and define
 z=(h1-kappa*conj(h1))/(1-|kappa|^2),
 b(n)=[z*exp(i*gamma0*logn)+conj(z)*exp(-i*gamma0*logn)]/Omega
for M<n<=2M, and zero otherwise. These coefficients are REAL and
|b(n)|<=2|z|/Omega<=1 eventually, since |z|<=|h1|/(1-|kappa|).
For the ONE common polynomial B(s)=sum b(n)*n^-s,
 B(beta+i*gamma0)=z+kappa*conj(z)=h1 EXACTLY.                 (4)
Since |log(n/M)|<=log2 and sum|b(n)|n^-beta<=2|z|,
 B(beta+i*(gamma0+delta))=M^(-i*delta)*h1+O(delta)
                       =-1+i/2+O(1/logN).                  (5)
We used m*t=2*alpha. Both values lie in |1+B|<=3/4 for all
sufficiently large N. Support, the bound |b|<=tau, and realness all hold.

For these two ARTIFICIAL copies use the ACTUAL-SHAPED coefficient
formula from section1, with the same beta, N,T and chi. Then
 c2/c1=exp(i*t)*(1+o(1))=-exp(i*alpha)*(1+o(1)).
Their packet Gram entries divided by
 I_beta=int theta(v)^2*v^(2beta-1)dv>0
tend to1, as delta tends to zero. After division by |c1|^2*I_beta,
 ||Z||^2 tends to 2-4/sqrt5>0,
 Re int Z_B*conj(Z) tends to sqrt5-2>0.                     (6)
Thus common polynomial structure, actual length support, real bounded
coefficients and the N-phase of c do not imply homogeneous coercivity.
The coefficients b were designed using gamma0; they are NOT a_T(n)
exp(-n/sqrtT), and the frequencies are NOT actual zeta zeros. This
does not refute a special arithmetic inequality for H_N and its zeros.
The unnormalized model is small (|c1|^2 is of order N^-3/5); it also
does not refute a proposed ACTUAL inequality with an additive all-log
error. The claim tested and falsified is the homogeneous operator step.

4. WHAT AN ACTUAL OPERATOR ARGUMENT WOULD HAVE TO CONTROL.
After merging identical copies, the finite packet Gram matrix is positive
definite: distinct exponential functions are linearly independent on an
interval. Put y=G^(1/2)c. The transformed multiplier is exactly
 G^(1/2)D G^(-1/2)=D+[G^(1/2),D]G^(-1/2).                   (7)
Since Re D<=-I/4, a sufficient operator condition is that the Hermitian
part of the second term be bounded above by delta0*I for delta0<1/4.
It would give coercivity with margin1/4-delta0. No such relative
commutator estimate has been proved for the actual spectrum.

The simpler exact commutator retains the actual common polynomial:
 [G,D]_(rho,sigma)=G_(rho,sigma)*(H_N(sigma)-H_N(rho))
 =G_(rho,sigma)*sum_n h(n)*(n^-sigma-n^-rho).                 (8)
In the middle strip the retained coefficient bound only gives
 |H_N(rho)-H_N(sigma)|
 << |rho-sigma|*Q^(1-16/25)*L^2,
 Q=2*N^(41/100).
This follows by integrating the derivative along the line segment
between rho,sigma. The N power is369/2500, positive. Even at gaps
of order1/L it supplies no smallness; the disk's alternative bound
|H_N(rho)-H_N(sigma)|<=7/2 also supplies no small relative norm.
These are failed UPPER BUDGETS, not lower bounds for an actual error.

5. THE ACTUAL MIXED OVERLAP HAS A PRIME-PRODUCT REPRESENTATION.
Return now ONLY to actual R,H_N and the fixed cutoffs. The reviewed
unweighted deletion and high_detector_weighted_bridge.py give, for
every fixed A, in the central cutoff norm,
 Z_R=-theta*P_Lambda(vN)/sqrtN+O_L2,A(L^-A),
 Z_HR=-theta*P_h(vN)/sqrtN+O_L2,A(L^-A).
The full arithmetic norms are O(1) and O(L^(5/2)), respectively.
Choose the inherited saving with the extra log margin before multiplying
errors. It follows that
 C_R=(1/N)*Re int theta(v)^2*P_h(vN)*conj(P_Lambda(vN))dv
                                     +O_A(L^-A).            (9)
This is a CONJUGATED overlap, not the Goldbach reflected bilinear form.

Let F(y)=hatChi(y)*nu(y/V), V=N^(1/8), and d(k)=(h*Lambda)(k).
Set
 K_N(k,l)=int theta(v)^2*F(Tlog(k/(vN)))
                         *conj(F(Tlog(l/(vN))))dv.
The exact main term of(9) is
 T^2/(4pi^2*N)*Re sum_(k,l) d(k)*Lambda(l)/sqrt(k*l)*K_N(k,l).(10)
All product indices lie in[N/8,2N] eventually. Uniform Schwartz
bounds, followed by the change y=Tlog(k/(vN)), show for any fixed B
 |K_N(k,l)|<<_B T^-1*(1+|k-l|/Hwin)^-B,
 Hwin=N/T=N^(1/10).                                        (11)
This retains the COMPLEX kernel and the target N; no positivity or
local prime asymptotic is inserted.

6. THE ACTUAL DIAGONAL IS POWER SMALL.
For k=p prime near N, d(p)=0 since h(1)=0. For k=p^2 near N,
the only possible term is h(p)*logp, also zero because p>Q eventually.
For k=p^e,e>=3, if p<=B0=2*T^(1/100), then
 a_T(p^j)=1+mu(p)=0 for every j>=1, hence d(p^e)=0.
If p>B0, then a_T(p^j)=1, while the DAMPED masked h(p^j) lies
in[0,1]. Therefore
 0<=d(p^e)=logp*sum_(1<=j<e)h(p^j)<=log(p^e).                (12)
As p>B0 and p^e<=2N, necessarily e<1000/9, hence e<=111.
There are O(N^(1/3)) possible integer bases for these finitely many
exponents. Consequently
 sum_(k) d(k)*Lambda(k)/k<<N^(-2/3)*L^2.
Using K_N(k,k)<<1/T, the DIAGONAL in(10) is
 O(N^(-23/30)*L^2).                                        (13)
No main-scale contribution remains on k=l; this is an actual
coefficient fact, stronger than a generic divisor majorant here.

7. THE REMAINING ACTUAL SHORT-SHIFT SUM.
The part |k-l|>Hwin*L has row and column Schur bounds
 <<_B (N/T^2)*L^(1-B)
by(11) and integer summation, since Hwin>=1. The retained coefficient
norms are
 ||d(k)/sqrtk||_ell2<<L^(5/2),
 ||Lambda(l)/sqrtl||_ell2<<L^(1/2).
The second uses Lambda(l)^2<=log(2N)*Lambda(l) and Chebyshev.
After the T^2/N factor, the tail is O_B(L^(4-B)). Choose B>A+4.
Thus, after absorbing(13), equation(9) becomes
 C_R=T^2/(4pi^2*N)*Re
   sum_(0<|r|<=Hwin*L) sum_(n,m>=1)
    h(n)*Lambda(m)*Lambda(n*m+r)/sqrt(n*m*(n*m+r))
                           *K_N(n*m,n*m+r) +O_A(L^-A).       (14)
Terms have n*m,n*m+r in[N/8,2N]; all factors with Lambda(1)
vanish, and the original bad-length and damping masks stay in h.
Changing variables l=k+r and k=n*m is finite and exact before the
proved diagonal/tail deletions. The two linked prime-power conditions
are now explicit: m and n*m+r. Proper powers remain included.

8. REMOVE PROPER POWERS: THE TARGET REALLY HAS TWO PRIME CONDITIONS.
Write Lambda_pr(m)=log(m)*1_(m prime) and Lambda_pp=Lambda-Lambda_pr.
Let d_pp=h*Lambda_pp and d_pr=h*Lambda_pr. For k comparable to N,
Cauchy over divisors and tau(n*m)<=tau(n)*tau(m) give
 |d_pp(k)|^2<=tau(k)*sum_(n*m=k,m proper power)|h(n)|^2*Lambda(m)^2
       <=sum_(n*m=k,m proper power)tau(n)^3*tau(m)*Lambda(m)^2.
For each n<=Q, the sum of tau(m)*Lambda(m)^2 over proper powers
m comparable to N/n is at most sqrt(N/n)*L^4: count O(L)
exponents, bound each number of integer bases by O(sqrt(N/n)),
and use tau(p^e)<=O(L) and Lambda(m)^2<=O(L^2).

The elementary inequality tau(n)^3<=tau_8(n) follows at p^e from
 (e+1)^3<=binom(e+7,7).
Indeed the ratio of the right side to the left is nondecreasing,
because (e+1)^2*(e+8)-(e+2)^3=4e^2+5e>=0, and starts at1.
The retained divisor sum for tau_8 and partial summation give
 sum_(n<=Q)tau(n)^3/sqrtn<<sqrtQ*L^7.
Consequently
 sum_(k comparable to N)|d_pp(k)|^2/k
                    <<N^(-1/2)*sqrtQ*L^11
                    <<N^(-59/200)*L^11.                    (15)
The normalized product-window Schur estimate maps this coefficient
energy into the same bound for ||P_(d_pp)/sqrtN||_2^2.
Its contribution paired against the FULL Lambda window, whose norm
is O(1), is therefore O(N^-59/400*L^(11/2)).

Similarly sum Lambda_pp(l)^2/l<<N^-1/2*L^3, so its normalized
window norm is O(N^-1/4*L^(3/2)). The d_pr window has norm
O(L^(5/2)) by subtracting the d_pp window from the full d window.
Thus removing proper powers from the other coordinate costs
O(N^-1/4*L^4). Both errors are all-log small. Reapply the same
tail Schur bound to the prime-only coefficients, whose norms do not
exceed the retained bounds by more than these paid errors.

It follows that BOTH Lambda factors in(14) can be replaced by
Lambda_pr, with error O_A(L^-A). The remaining actual expression
has the two genuine prime conditions m prime AND n*m+r prime.
The r=0 diagonal for those prime-only coefficients vanishes exactly
because h(1)=0. Equation(13) remains a valid independently paid
component of the original prime-power formula. No cutoff in h or
the complex kernel is dropped in either version.

This gives an arithmetic target for the overlap obstruction, not a
bound for its sign. The checked norm estimates alone give O(L^(5/2))
for C_R, with no small constant or decay. Neither this Hermitian
overlap nor a hypothetical coercivity result alone determines the
original NONCONJUGATED reflected prime correlation. That estimate and
Goldbach remain OPEN. The tests below are algebraic guards and labeled
artificial fixtures, not a numerical-zero or finite-Goldbach campaign.
"""
import cmath
import math
from fractions import Fraction as F


def two_packet_budgets(r):
    """Exact fixed-witness and inverse energies; artificial normalized Gram."""
    if type(r) is not F or not 0 < r < 1:
        raise ValueError('exact positive-definite overlap 0<r<1 required')
    return {'witness_norm': F(9, 4)-2*r,
            'witness_mixed': F(5, 2)*r-F(9, 4),
            'inverse_input': F(5, 2)-F(3, 2)*r,
            'inverse_output': F(25, 8)*(1-r)}


def model_parameters():
    """Floating display/fixture only; the proof gives rational enclosures."""
    alpha = math.atan(.5)
    t = math.pi+alpha
    return {'beta': .7, 'alpha': alpha, 't': t, 'm': 2*alpha/t,
            'norm_limit': 2-4/math.sqrt(5), 'mixed_limit': math.sqrt(5)-2}


def interpolate_real_block(length, beta, gamma, target):
    """Artificial real polynomial, not truncated-Mobius detector coefficients."""
    if (type(length) is not int or length < 1 or length & (length-1)
            or not 0 < beta < 1 or not math.isfinite(gamma)):
        raise ValueError('positive dyadic length and finite model parameters required')
    ns = range(length+1, 2*length+1)
    omega = sum(n**(-beta) for n in ns)
    kappa = sum(n**(-beta)*cmath.exp(-2j*gamma*math.log(n)) for n in ns)/omega
    if abs(kappa) > .1:
        raise ValueError('fixture has not met the proved interpolation condition')
    z = (target-kappa*target.conjugate())/(1-abs(kappa)**2)
    coefficients = {n: 2*(z*cmath.exp(1j*gamma*math.log(n))).real/omega for n in ns}
    return coefficients, {'omega': omega, 'kappa': kappa, 'z': z}


def evaluate_model(coefficients, beta, gamma):
    return sum(value*n**(-beta)*cmath.exp(-1j*gamma*math.log(n))
               for n, value in coefficients.items())


def overlap_exponents(kernel_decay):
    if type(kernel_decay) is not int or kernel_decay <= 4:
        raise ValueError('fixed integer Schwartz decay greater than4 required')
    return {'window': F(1, 10),
            'diagonal': F(9, 10)-1-F(2, 3),
            'tail_log': 4-kernel_decay,
            'derivative_cost': F(41, 100)*(1-F(16, 25))}


def proper_power_overlap_exponents():
    coefficient_energy = -F(1, 2)+F(41, 200)
    return {'product_energy': coefficient_energy,
            'product_norm': coefficient_energy/2,
            'opposite_norm': -F(1, 4),
            'product_log_energy': 11, 'opposite_log_overlap': 4}
