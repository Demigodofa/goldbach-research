"""Transfer actual prime phase bounds to exact windows and a conditional band.

Owner: Kevin's Goldbach research. Purpose: connect varying_prime_phase.py
to the actual arithmetic/zero window, and quantify the still-missing
phase decomposition. No existence of that decomposition is asserted.

1. EXACT OBJECTS AND THE UNCONDITIONAL PROJECTION ESTIMATE.
Keep T=N^(9/10), V=N^(1/8), L=logN, fixed real chi smooth supported
in(1,2), and the same fixed Fourier cutoff nu as short_prime_window_energy.py.
The actual arithmetic window and its normalization are
 P_N(aN)=T/(2pi)sum_(n>=2)Lambda(n)/sqrt n
      *hatChi(Tlog(n/(aN)))*nu(Tlog(n/(aN))/V),
 F_N(a)=P_N(aN)/sqrtN.                                        (1)
Use the angular convention hatChi(v)=int chi(t)exp(-i*v*t)dt.
The cutoff nu is1 on[-1,1], vanishes outside[-2,2], and is fixed smooth.

Fix closed intervals J inside the interior of I, with I compactly
contained in(1/4,3/4). Let f_N satisfy varying_prime_phase.py's uniform
C^3 bounds on I: |f'|,|f'+u*f''|>=c>0, and derivatives1,2,3 bounded
by a fixed C. Let w_N be complex C^1 supported in J, with sup|w_N|
and sup|w_N'| bounded by fixed constants. Then
 int w_N(a)exp[-i*T*f_N(a)]F_N(a) da
 = (1/N)sum_n Lambda(n)*sqrt(u)*w_N(u)*chi(u*f_N'(u))
                    *exp[-i*T*f_N(u)] +O(T^-1+V^-16),          (2)
where u=n/N and the summand is zero off the amplitude support. Hence
 |int w_N(a)exp[-i*T*f_N(a)]F_N(a) da|
                                  <<N^(-1/44)*L^3.           (3)
All constants are uniform over the specified common phase/amplitude bounds.
These are actual weighted Lambda windows, not artificial coefficients.

2. PROOF OF THE ADJOINT IDENTITY, WITH SUPPORT AND ERRORS PAID.
The cutoffs restrict every contributing n to a fixed range comparable
to N, so the sum/integral exchange is finite. For fixed u=n/N put
 v=Tlog(u/a), a=u*exp(-v/T), da=-(u/T)exp(-v/T)dv.
In the integral in(2), the coefficient after this substitution is
 Lambda(n)*sqrt(u)/(2pi*N),
and the remaining integral is
 int hatChi(v)*nu(v/V)*exp(-v/T)*w_N(u*exp(-v/T))
                         *exp[-i*T*f_N(u*exp(-v/T))]dv.         (4)
There is a fixed compact neighborhood J_1 of J lying inside I. Since
|v|<=2V and V/T tends to0, every u contributing to(4) lies in J_1
for large N, and every segment used below stays in I. Values outside
that neighborhood contribute zero exactly. No continuation of f_N
outside its domain is presumed.

Uniform Taylor estimates on that buffered range give
 T*f_N(u*exp(-v/T))=T*f_N(u)-u*f_N'(u)*v+O(v^2/T),
 exp(-v/T)*w_N(u*exp(-v/T))=w_N(u)+O(|v|/T).
The phase remainder uses bounded f' and f''; the amplitude remainder
uses the common bound on w_N'. Schwartz moments of hatChi make the
integrated total error O(1/T). Removing nu from the resulting linear
phase integral costs O(V^-16), uniformly in the phase frequency.
Angular Fourier inversion then gives
 int hatChi(v)exp[i*u*f_N'(u)*v]dv=2pi*chi(u*f_N'(u)).
The positive sign and the sqrt(u)/N factor in(2) are essential.

The sum of the absolute coefficient weights in this fixed range is
 (1/N)sum Lambda(n)*sqrt(n/N)=O(1)
by the already retained Chebyshev bound. Thus the summed normalized
error remains O(T^-1+V^-16), proving(2). The leading prime amplitude
 psi_N(u)=sqrt(u)*w_N(u)*chi(u*f_N'(u))
has common compact support and uniformly bounded supremum and C^1 norm:
its derivative involves only w_N,w_N',f_N', and f_N'+u*f_N''.
The varying-amplitude version of varying_prime_phase.py bounds its
actual Lambda sum by O(N^(43/44)L^3). Dividing by N proves(3).
The normalized adjoint errors N^-9/10 and N^-2 are smaller.

3. ACTUAL ZERO MOMENT, WITH THE EXPLICIT-FORMULA ERROR RETAINED.
Let S_T(x)=sum_(gamma>0)chi(gamma/T)x^(rho-1/2), with actual
zero copies, real parts and multiplicities, and Z_N(a)=S_T(aN)/sqrtN.
The completed short_prime_window_energy.py transfer gives, uniformly
on[1/4,3/4],
 Z_N(a)=-F_N(a)+O(N^(-2/5)*L^6),
 ||F_N||_2+||Z_N||_2=O(1)                                    (5)
in the da measure on that interval. Consequently
 |int w_N(a)exp[-i*T*f_N(a)]Z_N(a)da|
                     <<N^(-1/44)L^3+N^(-2/5)L^6.             (6)
We reuse the proved actual Guinand/prime-power/displacement estimates;
no real part beta is replaced by1/2 and no RH assumption is introduced.

4. THE PRECISE CONDITIONAL PHASE DECOMPOSITION TARGET.
Choose the SAME fixed zeta as the completed beta transfer: smooth,
equal1 on[3/10,7/10], compactly supported in(1/4,3/4). Choose J,I
above to contain its support, with the stated fixed buffer. For H_N
equal to F_N or Z_N define
 B_(H,N)(a)=2*zeta(a)*H_N(1-a)/sqrt(a*(1-a)).
The normalized central paired functional is EXACTLY
 Q_(H,N)=int H_N(a)*B_(H,N)(a)da.                             (7)
There is NO conjugation. For each N, suppose one actually has a finite
decomposition
 B_(H,N)=sum_(j=1)^m c_(j,N)*w_(j,N)(a)*exp[-i*T*f_(j,N)(a)]
                    +r_N(a),                                (8)
where EVERY phase/amplitude has the SAME bounds and buffered intervals
used in(3)/(6). Put A_N=sum_j |c_(j,N)| and R_N=||r_N||_2.
The number of terms may depend on N; its cost is paid through A_N.

By(3),(5),(6), triangle inequality and Cauchy for the residual,
 |Q_(F,N)| << N^(-1/44)L^3*A_N+R_N,
 |Q_(Z,N)| << [N^(-1/44)L^3+N^(-2/5)L^6]*A_N+R_N.             (9)
The residual estimate is valid for a bilinear integral without a
conjugate because |int H*r|<=||H||_2*||r||_2.
Thus A_N=o(N^(1/44)/L^3) and R_N=o(1) SUFFICE for o(1) of
the respective normalized central functional. Conversely, a fixed
positive lower bound for |Q_(H,N)| together with R_N=o(1) forces
 A_N >> N^(1/44)/L^3
in any decomposition with these common bounds. No such expansion
or small residual is currently known for the actual reflected window.
An arbitrary formal phase expansion is not a certificate: its coefficient
sum, phase bounds, amplitude derivatives and residual must all be paid.

5. CONDITIONAL TRANSFER TO THE ACTUAL FINITE-PERIOD BAND.
For the actual finite-period kernel J_N, short_prime_window_energy.py
sections5-6 already proves, with the same chi,zeta and T=N^(9/10),
 sum_(rho,sigma)chi(gamma/T)chi(eta/T)J_N(rho,sigma)
       =N*Q_(Z,N)+O(N^(9/10)L^12+N^(-7/10)L^13).              (10)
The second error is the paid beta endpoint sum; the first is the
paid difference between the beta quotient and the actual finite-period
kernel. Both retain actual zero real parts and multiplicities. Equation
(10) is reused with its errors, not a substitution of a full-line formula.

Therefore an ACTUAL decomposition(8) of B_(Z,N) implies the bound
 |sum chi*chi*J_N|/N
 <<[N^(-1/44)L^3+N^(-2/5)L^6]*A_N+R_N
                      +N^(-1/10)L^12+N^(-17/10)L^13.          (11)
In particular, if A_N=O(N^kappa), fixed0<=kappa<1/44, and
R_N=O(N^-sigma), fixed sigma>0, then this ONE weighted comparable
band is conditionally O_A(N/log^A N) for every fixed A. For example,
kappa=1/100 and sigma=1/50 give main power543/550, with the
explicit logarithms and the smaller errors in(11).

This is a quantified sufficient bridge to an actual signed band estimate.
It does not construct the phase decomposition, give an unconditional
o(N) band bound, or handle the full surviving spectral core. The actual
unconditional band bound remains O(N), and the Goldbach signed lower
margin remains OPEN. Polynomial tools and all source corrections persist.
"""
from fractions import Fraction as F


def normalized_projection_budget():
    return {'prime': -F(1,44), 'adjoint': -F(9,10),
            'fourier_tail': -F(2), 'zero_transfer': -F(2,5),
            'finite_period': -F(1,10), 'beta_endpoint': -F(17,10)}


def conditional_band_budget(kappa, sigma):
    if (type(kappa) is not F or type(sigma) is not F
            or not 0 <= kappa < F(1,44) or sigma <= 0):
        raise ValueError('exact 0<=kappa<1/44 and sigma>0 required')
    return {'prime_projection': F(43,44)+kappa,
            'zero_transfer': F(3,5)+kappa,
            'residual': 1-sigma,
            'finite_period': F(9,10),
            'beta_endpoint': -F(7,10)}
