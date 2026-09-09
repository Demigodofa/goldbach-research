"""Prime support pays the actual comparable N^(9/10) band at scale N.

Owner: Kevin's Goldbach research. Purpose: use an arithmetic interval
upper bound in a surviving spectral band, retaining the actual real parts
and finite-period kernel. This is a main-scale bound, not an all-log
deletion, a small-constant lower margin, or new Goldbach coverage.

1. THE ACTUAL STATEMENTS.
Let N tend to infinity, L=logN, T=N^(9/10), and let chi be a FIXED
real C_c^infinity((1,2)) function. Count all actual zero copies in
 S_T(x)=sum_(gamma>0) chi(gamma/T)x^(rho-1/2).
Uniformly for N/4<=x<=3N/4, we prove
 |S_T(x)|<<_chi sqrtN,
 int_(1/4)^(3/4)|S_T(aN)|^2 da<<_chi N.                           (1)
The integral is in the frequency parameter a at FIXED target N.
For the actual finite-period J_N, we also prove the COMPLEX bound
 |sum_(rho,sigma)chi(gamma/T)chi(eta/T)J_N(rho,sigma)|<<_chi N.     (2)
This comparable band lies above the current N^(17/20) square. Its
weights do not satisfy the selected strongly unequal tag condition.
Nevertheless(2) does not authorize deleting it with an all-log error:
the constant is not shown small enough for the Goldbach lower margin.

2. A CHECKED PRIME-INTERVAL INPUT, WITH PRIME POWERS PAID SEPARATELY.
Source checked2026-09-09: Tomohiro Yamada, arXiv2312.16090v1,
Theorem2, printedp3, equation(13):
https://arxiv.org/pdf/2312.16090v1 . Taking k=a=1 and weakening its
positive denominator correction gives
 pi(z+y)-pi(z)<=2y/logy, z>0,y>1.                                (3)
Only this order-of-magnitude consequence is needed. The original
Montgomery--Vaughan institutional-copy route returned403; no retry,
installation or assertion that the blocked copy was read is made.

Put H=N/T=N^(1/10). For a real center x in[N/4,3N/4] and H<=R=o(N),
(3) and logp<=log(2N) give
 sum_(p prime, |p-x|<=R) logp <<R L/logR<<R.                      (4)
Enlarging interval endpoints by a fixed amount pays an endpoint prime.
The constants use logR>=(1/10)L; no uniform claim at R of bounded
length is made. Large R comparable with N can instead use Chebyshev.

For proper powers n=p^j in[N/8,2N], j>=2, enlarge to all integer
bases. For each fixed j, the derivative j*u^(j-1), at u^j>=N/8,
is at least a constant times sqrtN. Thus an interval of length2R
contains at most O(R/sqrtN+1) such j-th powers. There are O(L)
possible exponents, and every log-prime weight is O(L). Therefore
 sum_(proper powers, |n-x|<=R) Lambda(n)
       <<(R/sqrtN+1)L^2<<R, R>=H.                               (5)
Overcounting repeated representations is harmless for this upper
bound. Combining(4)-(5) controls the FULL Lambda mass on each shell.

3. SCALE THE ENTIRE GUINAND TEST WITHOUT DROPPING THE BETA SHIFT.
Use the unconditional Guinand formula, angular Fourier convention,
and fixed smooth Fourier cutoff nu from arithmetic_zero_moment.py.
Keep V=N^(1/8), but now put
 chi_V(z)=(1/(2pi))int hatChi(v)nu(v/V)exp(ivz)dv,
 H_x(t)=exp(itlogx)chi_V(t/T).
The complex zero argument is gamma-i(beta-1/2), not gamma. All
source conditions remain satisfied because the inverse Fourier
test is smooth compactly supported for each N, and V/T tends to0.

The first-order Taylor argument of arithmetic_zero_energy.py gives
 chi_V(u-i*b/T)=chi(u)-i*b*chi'(u)/T
               +O_chi((T^-2+V^-16)(1+|u|)^-r), |b|<=1/2.        (6)
It is the ENTIRE chi_V that is Taylor-expanded; chi is not continued
analytically. Fourier derivatives along the segment have bounded
Schwartz seminorms since exp(v*b/T) is bounded on |v|<=2V.

For x~N, the weighted first moment over T<=gamma<=2T obeys
 W_T(x)=sum x^(beta-1/2)<<N L^6.                                 (7)
Indeed T<=N eventually, and the retained Ingham exponent
D_I(u)=3u/(1+u) has D_I(u)-u<=1/2. The beta<=1/2 baseline is
O(TL); layer cake bounds the remaining terms by N L^6. Fixed
factors2 in the height cutoff and fixed x/N change only constants.
This same estimate holds at x=N when used below.

The localized first correction in(6) consequently costs
 W_T(x)/T<<N^(1/10)L^6.
The global BOTH-SIGN zero count gives the remaining absolute error
 sqrtN*T*L*(T^-2+V^-16)
             =O((N^(-2/5)+N^(-3/5))L).                          (8)
At the pole tests chi(0)=chi'(0)=0, so their total is
O(sqrtN*(T^-2+V^-16)). The real-axis cutoff error in the Gamma
integral is O(T L V^-16), and the compact-support term is O(1)
by integration by parts against exp(itlogx), as before. All these
costs are absorbed by the localized first correction.

The exact positive-frequency prime term is therefore
 S_T(x)=-P_T(x)+O_chi(N^(1/10)L^6),                              (9)
 P_T(x)=T/(2pi)sum_(n>=2) Lambda(n)/sqrt n
           *hatChi(Tlog(n/x))*nu(Tlog(n/x)/V).
It includes proper powers. The negative-frequency prime term is0
for large N, since the Fourier support is near positive logx.
The pole, archimedean and zero-displacement terms have been paid
before taking any square or coupled product.

4. KEEP PRIME SUPPORT IN THE SAMPLING BOUND.
For x=aN, a in[1/4,3/4], write the kernel in(9) as K_T(a,n).
Its finite support has n in[N/8,2N] and |n-aN|=O(VH)=o(N).
On that support the mean value theorem gives fixed positive
constants c,C with
 c*|n-aN|/H<=|Tlog(n/(aN))|<=C*|n-aN|/H.
Thus |K_T(a,n)|<=C_r(1+|n-aN|/H)^-r for every fixed r.
Use(4)-(5) on dyadic shells of radii2^j H. For r>2 their sum gives
 sup_a sum_n Lambda(n)|K_T(a,n)|<<_chi H.                         (10)
The permitted Fourier width VH is not an extra loss: its outer
shells are rapidly discounted, and all relevant radii are o(N).
Directly from(9)-(10), |P_T(x)|<<T H/sqrtN=sqrtN. The error in(9)
is o(sqrtN), proving the first statement of(1).

For a reusable energy bound, also observe
 sup_n int_(1/4)^(3/4)|K_T(a,n)|da<<_chi1/T,
 sum_(N/8<=n<=2N) Lambda(n)/n<<1.                               (11)
The first follows by the change v=Tlog(n/(aN)), whose Jacobian
has absolute value a/T<=3/(4T). The second follows from the
reviewed elementary Chebyshev bound psi(2N)=O(N).
Weighted Cauchy, with the NONNEGATIVE weights Lambda(n)|K_T|,
gives
 |sum Lambda(n)K_T(a,n)/sqrt n|^2
 <=[sum Lambda(n)|K_T|]*[sum Lambda(n)|K_T|/n].
Integrating, using(10)-(11), and restoring T^2/(4pi^2) gives
 int|P_T(aN)|^2 da<<T^2*(H/T)=TH=N.                              (12)
The squared replacement error is O(N^(1/5)L^12)=o(N). This proves
the second statement of(1). Unlike an integer-count row bound,
the arithmetic row in(10) does not replace Lambda by its maximum L.
No independence or cancellation between two primes was used here.

5. THE EXACT BETA TRANSFER AND ITS ENDPOINTS.
Keep B_N=2N^(rho+sigma-1)Gamma(rho)Gamma(sigma)/Gamma(rho+sigma).
The reviewed Euler-beta identity, with the actual positive real
parts and finite lists, is
 sum chi(gamma/T)chi(eta/T)B_N
  =2 int_0^1 S_T(aN)S_T((1-a)N)/sqrt(a(1-a)) da.                  (13)
There is no conjugation. Use a fixed smooth cutoff zeta equal1 on
[3/10,7/10], supported in(1/4,3/4). For s=gamma/T,t=eta/T in[1,2],
the phase is T[s loga+t log(1-a)], with stationary ratio in[1/3,2/3].
On a<=3/10, s(1-a)-ta>=1-3a>=1/10. Its reciprocal phase derivative
is a times a uniformly smooth function at0; similarly at1.
Three integrations by parts therefore cost
 O(T^-3*(1/beta+1/beta'))
before the factor N^(rho+sigma-1). This is precisely the endpoint
calculation in arithmetic_beta_transfer.py with oscillation scale T.
The vanishing a^beta boundary jets and the beta denominators remain.
Classical zero-free/reflection gives1/beta+1/beta'=O(L). Using(7)
at x=N, the TOTAL endpoint error is
 <<T^-3 L*W_T(N)^2<<N^(-7/10)L^13.                              (14)
The central integral in(13) is O(N) by(1), Cauchy, and symmetry
under a->1-a. Thus the actual B_N sum is O_chi(N).

6. PAY THE DIFFERENCE FROM THE ACTUAL FINITE-PERIOD KERNEL.
Since T=o(N), every pair in this band satisfies piN>=4(gamma+eta)
eventually. The reviewed interior expansion gives
 J_N=A_N exp(iTheta_N)[1+O(T^-1/2)],
 B_N=A_N exp(iTheta_N)[1+O(T^-1)],
with the SAME positive amplitude and phase; the second expansion
is just the uniform Gamma quotient Stirling formula. Consequently
 |J_N-B_N|<<T^-1/2 A_N.                                        (15)
No full-line beta formula was silently substituted for J_N.

Sum(15) with the original Ingham amplitude layer cakes. For equal
height exponent h=9/10, their retained exact majorant is
 E(h,h,u,v)-h/2<=1-h/5-(1-6h/5)(u+v), 0<=u,v<=1/2.
Now1-6h/5<0, so use u+v<=1. The right side is at most h=9/10.
Thus the summed actual replacement error is
 O_chi(N^(9/10)L^12)=o(N).                                      (16)
Fixed factors in the band and bounded chi affect constants only;
there is one comparable band, not a growing dyadic-box count.
Combining(13)-(16) proves(2).

7. WHAT THIS DOES AND DOES NOT RESOLVE.
The prime-interval support reduces a logarithmic loss in the
arithmetic moment bound and controls this actual surviving coupled
band at main scale. It supplies no small constant, positive sign,
all-log deletion, target average or uniform limit as T approaches N.
Removing the already-paid near-height strip changes this weighted
bound only by an all-log error; it still gives no full-core margin.
The real signed prime correlation is OPEN. Polynomial components,
the prime-offset transform and every prior source correction persist.
"""
from fractions import Fraction as F


def scale_budget():
    """Exact exponents for this fixed T=N^(9/10) theorem."""
    t=F(9,10)
    return {
        'window':1-t, 'localized_shift':1-t,
        'global_taylor':F(1,2)-t,
        'global_fourier_tail':F(1,2)+t-2,
        'pole_taylor':F(1,2)-2*t,
        'squared_shift':2*(1-t), 'beta_endpoint':2-3*t,
        'finite_period_remainder':t,
    }


def prime_weighted_schur(matrix, measures, masses, values):
    """Exact real finite guard for the Lambda-weighted Cauchy argument.

    The proof above applies to complex kernels and coefficients. These
    rational fixtures do not approximate actual primes or zero ordinates.
    """
    if not matrix or not values or len(matrix)!=len(measures):
        raise ValueError('nonempty compatible rows and measures required')
    if len(masses)!=len(values) or any(len(row)!=len(values) for row in matrix):
        raise ValueError('compatible column masses and values required')
    entries=[v for row in matrix for v in row]+list(measures)+list(masses)+list(values)
    if any(type(v) is not F for v in entries):
        raise ValueError('exact rational data required')
    if any(v<0 for v in list(measures)+list(masses)):
        raise ValueError('nonnegative measures and masses required')
    row_bound=max(sum((m*abs(k) for m,k in zip(masses,row)),F(0)) for row in matrix)
    column_bound=max(sum((q*abs(row[j]) for q,row in zip(measures,matrix)),F(0))
                     for j in range(len(values)))
    norm=sum((m*v*v for m,v in zip(masses,values)),F(0))
    energy=sum((q*sum((m*v*k for m,v,k in zip(masses,values,row)),F(0))**2
                for q,row in zip(measures,matrix)),F(0))
    return {'energy':energy,'bound':row_bound*column_bound*norm,
            'row_bound':row_bound,'column_bound':column_bound,'weighted_norm':norm}
