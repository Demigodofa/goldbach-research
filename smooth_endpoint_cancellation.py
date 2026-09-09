"""Prime parity pays a real signed smooth spectral contribution at fixed N.

Owner: Kevin's Goldbach research. Purpose: test whether summing zeros BEFORE
estimating the endpoint defeats the termwise absolute obstruction. It does
for the specified fixed smooth height weights. This is a bounded actual
signed estimate, not a Goldbach lower margin, numerical zero certificate,
RH consequence, or worldwide novelty claim. Polynomial tools remain useful.

RESULT AND SCOPE.
For an integer N>=3 set L=logN, a=1/N, z_*=a+i*pi. For positive-height
zeros rho=beta+i*gamma, sigma=beta'+i*eta, use the saved finite-period kernel
 J_N(rho,sigma)=(e/pi)Gamma(rho)Gamma(sigma)
                       *int_0^pi e^(iNt)(a+it)^(-rho-sigma)dt.
All zeros have their actual real parts and multiplicities; pairs are ordered
and include the diagonal. For each FIXED REAL
 G in C_c^infinity((8pi,9pi)^2),
 C_G(N)=Re sum_(rho,sigma) G(gamma/N,eta/N) J_N(rho,sigma)
             =O_G(sqrtN logN+log^2N).                  (1)
No average over N, RH, PNT asymptotic, or prime/zero-pair correlation input
is used. Constants depend on fixed smooth seminorms of G. The conclusion
does not cover the hard band, N-dependent shrinking windows, the entire
zero tail, or the full remaining coefficient C_(N,T).

1. AN ENDPOINT PROJECTION ON ONE ZERO BECOMES AN ARITHMETIC SUM.
Let f_rho=Gamma(rho)z_*^(-rho), for ALL nontrivial zeros, both height signs.
For fixed w in C_c^infinity((0,infinity)), possibly complex, put
 F_N(w)=sum_rho f_rho w(gamma/N),
 A_N(w)=sum_(n>=1)Lambda(n)e^(-n/N)w(pi*n/N).
We prove
 F_N(w)=A_N(w)+O_w(sqrtN L).                           (2)
In particular F_N(w)=O_w(N); A_N(w) is real when w is real.
Only Chebyshev psi(x)<<x, with partial summation, is needed for
 sum Lambda(n)e^(-n/(2N))<<N,
 sum n*Lambda(n)e^(-n/(2N))<<N^2.                      (3)

Stirling and zero counting at z_* give the absolute bound
 M_N=sum_rho |f_rho| << N^(3/2)L.                      (4)
Indeed |z_*|>=pi, so there is NO extra N from a small radial modulus:
the positive-height terms are bounded by C(1+gamma)^(1/2)e^(-c*gamma/N),
and the negative-height terms are exponentially summable independently of N.

Use the convention
 hatw(v)=(1/(2pi))int_R w(s)e^(i*s*v)ds,
 w(s)=int_R hatw(v)e^(-i*s*v)dv,
and truncate at V=N^(1/8). On this interval e^(|v|/N) is bounded.
Replacing w(gamma/N) by
 int_(-V)^V hatw(v)e^(-rho*v/N)dv
costs O_w(N^-1+V^-11), uniformly in every zero, since 0<beta<1,
|e^(-beta*v/N)-1|<=C|v|/N, and twelve derivatives of w give the Fourier
tail O_w(V^-11). Multiplied by (4), this is O_w(sqrtN L).
Absolute convergence for each fixed N licenses interchange, giving
 F_N(w)=int_(-V)^V hatw(v) Z(z_*e^(v/N))dv+O_w(sqrtN L),           (5)
where Z(z)=sum_rho Gamma(rho)z^(-rho).

The CORRECTED explicit formula is Z(z)=1/z-S(z)+E(z),
S(z)=sum Lambda(n)e^(-nz). At z=z_*e^(v/N), its argument is unchanged,
|z| is comparable to pi, and |Im z|/Re z=piN, so E(z)=O(L^2).
The 1/z term is O(1). The formula holds for arbitrary Re z>0; no
integrality of (Re z)^-1 is needed for this radial scaling.

For |v|<=V, expand e^(v/N)=1+v/N+O(v^2/N^2). The error in the prime
sum is O(v^2), by (3) and the exponential e^(-n/(2N)). Dropping the
additional real increment n*v/N^2 costs O(|v|), again by (3). Hence
 S(z_*e^(v/N))
 =sum Lambda(n)(-1)^n e^(-n/N)e^(-i*pi*n*v/N)+O(v^2+|v|).
The weighted integral of this error is bounded, since hatw is Schwartz.
Extending the Fourier integral back to R costs O_w(N V^-11). Therefore
 F_N(w)=-sum Lambda(n)(-1)^n e^(-n/N)w(pi*n/N)
                                      +O_w(sqrtN L+L^2).
The ONLY even n with nonzero Lambda(n) are powers of2. Thus the exact
parity correction is
 -sum Lambda(n)(-1)^n e^(-n/N)w(pi*n/N)
  = A_N(w)-2log2 sum_(j>=1)e^(-2^j/N)w(pi*2^j/N).
The compact support of w stays a positive distance from0, so the number
of powers of2 meeting it is O_w(1). This proves (2), absorbing L^2 into
sqrtN L for sufficiently large N. The error is controlled by a fixed
finite smooth seminorm (twelve derivatives suffice on a fixed support).

2. PASS FROM ONE ZERO TO TWO WITHOUT LOSING THE SAVING.
For fixed smooth g supported in a fixed positive rectangle, extend it
smoothly by zero and use a tensor Fourier series with cutoff factors equal1
on its support. Its coefficients decay faster than any power; the smooth
seminorms of the separated one-variable factors grow only polynomially in
their Fourier indices. Apply (2) to each factor, then sum the errors. This
gives, for real or complex g,
 sum_(rho,sigma) f_rho f_sigma g(gamma/N,eta/N)
  = sum_(n,m>=1) Lambda(n)Lambda(m)e^(-(n+m)/N)
                                  *g(pi*n/N,pi*m/N)
    +O_g(N^(3/2)L+N L^2).                            (6)
The displayed arithmetic main is REAL if g is real and is O_g(N^2) by (3).
There is no constraint n+m=N in this main; no prime-pair estimate has
been substituted. The error is N*sqrtN L+(sqrtN L)^2, summed against
rapidly decreasing coefficients.

Do NOT instead replace both beta factors directly in a two-zero integral:
the crude cost M_N^2/N is O(N^2L^2), which loses the saving needed below.
The single-zero estimate followed by the tensor expansion is essential.
For a beta-weighted factor we only need the crude bound
 |sum_rho beta*f_rho*w(gamma/N)|<=M_N*||w||_infinity.
Combining it with F_N(w)=O_w(N) in the same tensor expansion gives
 sum_(rho,sigma)(beta+beta') f_rho f_sigma g(gamma/N,eta/N)
                                      =O_g(N^(5/2)L).           (7)
No reality or cancellation is claimed for the beta-weighted factor.

3. THE FIRST ENDPOINT TERM IS IMAGINARY; ALL OTHER TERMS ARE PAID.
Use spectral_endpoint_obstruction.py, with b=beta+beta', h=gamma+eta,
k=h/N, r=|a+it|, theta=arg(a+it),
A=r^(-b)exp[-h*(pi/2-theta)], phi=Nt-h log(r)-b*theta,
q=1/phi'. For the supported pairs, k in(16pi,18pi) and 0<b<2.
The tiny interval [0,a] is exponentially paid. On [a,pi], |phi'| is
comparable to N/t; all required derivative envelopes were proved there.
Three integrations by parts, retaining the first TWO endpoint terms, give
 int_0^pi A e^(i*phi)dt
 =A(pi)e^(i*phi(pi))*[-i*q+(A'/A)*q^2+q*q']_(t=pi)
                                                    +O(N^-3). (8)
The third boundary term is included in the remainder. Lower boundary jets
are exponentially small. The derivative integrals are uniform because a
polynomial in1/t is multiplied by exp(-8pi/t).

Set d=1-k/pi, which is bounded away from0. At t=pi,
 q=1/(N*d)+O(N^-3),
 q'=-k/(N*pi^2*d^2)+O(N^-3),
 A'/A=-b/pi+k/pi^2+O(N^-2).
After multiplying back the Gamma factors and using e^(i*N*pi)=(-1)^N,
the two endpoint coefficients multiplying (e/pi)(-1)^N*f_rho*f_sigma are
 -i/(N*d)
 +1/N^2 * [(-b/pi+k/pi^2)/d^2-k/(pi^2*d^3)].           (9)
The total error over the supported pairs is O_G(L^2): the factored Gamma
absolute mass is O(N^3L^2), so the O(N^-3) remainder in (8) is paid.
The coefficient expansions in (9) also have total error O_G(L^2).

For the first term, g(s,t)=G(s,t)/(1-(s+t)/pi) is fixed, smooth and real.
Its arithmetic main in (6) is real. Multiplication by -i makes its real
part vanish EXACTLY. Dividing the error in (6) by N costs
O_G(sqrtN L+L^2). The b-free second terms in (9) cost O_G(1) by (6).
The terms linear in b=beta+beta' cost O_G(sqrtN L) by (7) and N^-2.
Together with the paid remainder, these prove (1).

4. WHAT HAS AND HAS NOT CHANGED.
This is an ACTUAL signed cancellation mechanism: smooth spectral projection
at the parity endpoint has a real arithmetic main, while the leading
endpoint multiplier is imaginary. No lower bound for the full Goldbach
coefficient follows. This controls a specified nonempty smooth region only.
If G is nonnegative and bounded below on a smaller product rectangle, the
previous endpoint/reflection argument still gives termwise absolute mass
>>_G Nlog^2N there, while (1) is small. Thus absolute size and the signed
contribution really differ, including for these smooth weights.
Neither a hard cutoff nor smooth weights whose derivatives grow with N
are licensed by a constant that was proved only for fixed G. The remaining
same-sign interactions and C_(N,T)>=-(1-delta)N remain OPEN. No new
prime-pair coverage, numerical onset, actual zero list, or PNT asymptotic
is asserted. All previous polynomial tools and source corrections persist.

Sources checked2026-09-09:
* https://arxiv.org/pdf/1606.00860v1 : Lemma5.1 and Section6 CORRECTION
  supplying the missing constant1 in the explicit-formula remainder.
* https://arxiv.org/pdf/1206.0251v1 : Lemma1, printedp6, equation(15),
  gives the shifted-contour identity for arbitrary a>0. Its printed error
  omits the constant and MUST be read with the above2016 correction.
* https://arxiv.org/abs/2107.06506 : only classical O(TlogT) zero counting.
* spectral_endpoint_obstruction.py: actual phase, endpoint normalization,
  uniform derivative envelopes, multiplicity conventions and absolute obstruction.
The finite guards below check algebra, parity, beta dependence and error
bookkeeping; they do not evaluate actual zeros or certify an asymptotic numerically.
"""
from fractions import Fraction as F


def prime_parity_components(coefficients, weights):
    """Toy weighted coefficients; identity requires even support only on powers2."""
    total=sum((value*weights.get(n,F(0)) for n,value in coefficients.items()),F(0))
    negative_alternating=-sum(((-1)**n*value*weights.get(n,F(0))
                               for n,value in coefficients.items()),F(0))
    correction=2*sum((value*weights.get(n,F(0))
                      for n,value in coefficients.items()
                      if n>=2 and n&(n-1)==0),F(0))
    return total,negative_alternating,correction


def endpoint_coefficients(k, b, endpoint):
    """Exact coefficients of i/N and 1/N^2; endpoint is a rational algebra proxy."""
    if any(type(v) is not F for v in (k,b,endpoint)):
        raise ValueError('rational k, b, and positive endpoint required')
    if endpoint<=0 or k<=endpoint or not 0<b<2:
        raise ValueError('positive endpoint, k>endpoint, and 0<b<2 required')
    d=1-k/endpoint
    return {
        'leading_imaginary':-1/d,
        'secondary_real':(-b/endpoint+k/endpoint**2)/d**2
                         -k/(endpoint**2*d**3),
    }
