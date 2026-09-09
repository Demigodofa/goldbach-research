"""An actual arithmetic zero moment excludes the mock lattice alignment.

Owner: Kevin's Goldbach research. Purpose: add a proved prime-side
constraint beyond the counting/density data, preserving all off-critical
real parts and every approximation cost. This single moment is not the
remaining bilinear Goldbach estimate. No RH, PNT asymptotic, averaging
over N, actual prime/zero computation, or novelty claim is used.

1. ACTUAL THEOREM, INCLUDING ITS UNIFORM FREQUENCY RANGE.
Let chi be a fixed real smooth function supported compactly in
(c,2c), c=1/100. For actual nontrivial zeta zeros rho=beta+i*gamma,
counted with multiplicity, define
 S_N(x)=sum_(gamma>0) chi(gamma/N) x^(rho-1/2).
Uniformly for N/3<=x<=2N/3, including real nonintegral x, we prove
 |S_N(x)| <<_chi sqrtN logN.                                        (1)
In particular this holds at x=N/2. The factor x^(beta-1/2) is retained;
replacing it by1 would not be licensed without a separate estimate.

For nonnegative nonzero chi, the mock spectrum from
spectral_count_resonance_model.py instead has at x=N/2
 S_N^mock(N/2)=i*(NlogN/(2pi))*int chi(s)ds+O_chi(N).                 (2)
Thus the actual arithmetic identity rules out that specific alignment.
The earlier countermodel was never asserted to satisfy that identity.
No new part of C_remaining is deleted by (1) alone: the passage from
linear Fourier moments to the coupled phase of the bilinear kernel has
not been proved. The sufficient Goldbach signed lower margin stays OPEN.

2. PRIMARY FORMULA AND CONVENTIONS, WITHOUT A HIDDEN RH ASSUMPTION.
Use angular Fourier transform hatH(y)=int H(t)exp(-iyt)dt. The
Guinand formula in these conventions is
 sum_rho H((rho-1/2)/i)=H(i/2)+H(-i/2)
  +(1/(2pi))int_R H(t)K(t)dt
  -(1/(2pi))sum_(n>=2) Lambda(n)/sqrt n
                       *[hatH(logn)+hatH(-logn)],                  (3)
 K(t)=Re[Gamma'/Gamma(1/4+it/2)]-logpi.
The zeros in (3) include both signs of the actual ordinate, and the
test argument is gamma-i(beta-1/2), NOT gamma unless beta=1/2.

Source checked2026-09-09: Paul Garrett, Guinand's explicit formula,
2021-02-12, Theorem0.1 on printedp1. It states the formula for
H(t)=int g(y)exp(iyt)dy with g in C_c^infinity(R), explicitly allowing
complex zero coordinates. Its two Gamma_R logarithmic derivatives
combine to K(t). The Fourier inversion factor converts g to hatH/(2pi).
https://www-users.cse.umn.edu/~garrett/m/complex/notes_2020-21/12g_guinand_explicit_fml.pdf

Independent source cross-check: Carneiro-Chandee-Milinovich,
arXiv1309.1526v1, Lemma5 on printedpp6-7. Although the lemma first
states an RH version with h(gamma), its proof explicitly licenses the
unconditional replacement h((rho-1/2)/i). Its Fourier convention has
2pi in the exponent, giving (3) after conversion. Its real-on-the-real-
axis test condition extends to our complex H by applying linearity to
H_R(z)=[H(z)+conj(H(conj z))]/2 and
H_I(z)=[H(z)-conj(H(conj z))]/(2i), both analytic and real on R.
This does not take a nonanalytic real part off the real axis.
https://arxiv.org/pdf/1309.1526v1
We do not invoke the paper's RH-dependent bounds for S(t) or S1(t).

3. AN ENTIRE APPROXIMATION WITH A PAID COMPLEX DISPLACEMENT.
Put L=logN, V=N^(1/8). Choose a fixed smooth nu, equal1 on[-1,1]
and0 outside[-2,2], with0<=nu<=1. Define
 chi_V(z)=(1/(2pi))int hatChi(v)nu(v/V)exp(ivz)dv,
 H(t)=exp(itlogx)chi_V(t/N).                                        (4)
Here hatChi is the angular Fourier transform of chi. The frequency
integrand is smooth and compactly supported, so chi_V and H are entire
and rapidly decreasing in each fixed horizontal strip. Thus they meet
the test-function hypotheses of (3) for each N. Formula (3) is exact;
uniform N-dependent estimates are supplied separately below.

For any fixed r,M, weighted Fourier integration by parts gives
 |chi_V(u)-chi(u)|<=C_(r,M)V^-M(1+|u|)^-r.                           (5)
Indeed every derivative of hatChi(v)[nu(v/V)-1] has arbitrarily small
L1 tails, since hatChi is Schwartz. Also, uniformly |b|<=1/2,
 |chi_V(u-i*b/N)-chi_V(u)|<=C_r N^-1(1+|u|)^-r.                     (6)
For (6), differentiate chi_V along the short vertical segment and
integrate by parts in v to obtain the weighted bound. The factor
exp(v*b/N) and its derivatives stay bounded on |v|<=2V; factors
v*hatChi(v) and all derivatives are integrable. Smooth cutoff
derivatives cost nonpositive powers of V. These estimates do not
pretend the original compactly supported chi is analytic.

At the complex zero argument,
 H((rho-1/2)/i)=x^(rho-1/2)
                  *chi_V(gamma/N-i(beta-1/2)/N).
Riemann-von Mangoldt gives, for fixed r>2,
 sum_rho (1+|gamma|/N)^-r << N L.
This counts both signs and all multiplicities. Since
|x^(rho-1/2)|<=sqrt x<<sqrtN, (5)-(6) imply
 sum_rho H((rho-1/2)/i)
   =S_N(x)+O_chi(sqrtN L+N^(3/2)L V^-M).                            (7)
Take M=16; the tail term is O(N^-1/2 L). The negative-height zeros
are included in the error because the original chi vanishes there.
All sums in this comparison converge absolutely. In particular an
unweighted point count or an unshifted complex test was not substituted.

4. A RAPIDLY WEIGHTED PRIME WINDOW, WITH NO V LOSS.
The angular Fourier transform of (4) is exactly
 hatH(y)=N hatChi(N(y-logx))nu(N(y-logx)/V).                           (8)
Its support is near the positive frequency logx, so hatH(0)=0 and
hatH(-logn)=0 for every n>=2, for large N. The prime term in (3) is
 -(N/(2pi))sum_(n>=2) Lambda(n)/sqrt n
       *hatChi(Nlog(n/x))nu(Nlog(n/x)/V).                            (9)
It is a finite sum supported on |log(n/x)|<=2V/N, hence n~x~N and
|n-x|=O(V). We do NOT bound it by counting V terms of maximal size.

On this support n/x is in[1/2,2] for large N. The mean value theorem
and x/N in[1/3,2/3] give
 (3/4)|n-x|<=|Nlog(n/x)|<=6|n-x|.
Schwartz decay of hatChi therefore implies
 sum_(n>=2) |hatChi(Nlog(n/x))nu(...)|<<_chi1,
uniformly in the real center x, including half-integers. This is simply
the uniform summability of(1+|n-x|)^-r for r>1. Since
Lambda(n)<=logn<<L and1/sqrt n<<N^-1/2, (9) is O_chi(sqrtN L).
No assertion that the window contains a prime, or any PNT asymptotic,
is used in this upper bound.

5. THE POLE AND GAMMA TERMS ARE ALSO PAID.
The uniform Fourier integral in (4) gives
 |H(i/2)|+|H(-i/2)|<<x^-1/2+x^1/2<<sqrtN.                            (10)
For the archimedean integral, use K(t)=O(log(2+|t|)). By (5), replacing
chi_V(t/N) by chi(t/N) on the REAL axis costs
 O_chi(N L V^-16)=O(N^-1 L)
absolutely. On the remaining compact support t~N, one integration by
parts against exp(itlogx) yields
 |int exp(itlogx)chi(t/N)K(t)dt|
 <=(logx)^-1 int |(chi(t/N)K(t))'|dt<<(L+1)/L<<1.                   (11)
There are no boundary terms because chi is smooth and compactly supported.
Here K'=O(1/|t|) on this band. One direct verification uses the absolutely
convergent trigamma series
 psi'(z)=sum_(k>=0)(k+z)^-2,
so at z=1/4+it/2 its absolute value is at most
sum_(k>=0)[(k+1/4)^2+(t/2)^2]^-1=O(1/|t|).
The series is source-checked in NIST DLMF5.15.1:
https://dlmf.nist.gov/5.15.E1
Thus the Gamma integral is O(1), not an unpaid O(NL) absolute term.

Combining (7), (9), (10), and (11) proves (1), uniformly over the stated
real frequency interval. All real parts and all multiplicities remain.

6. EXCLUDE THE SPECIFIC MOCK ALIGNMENT, WITHOUT CLAIMING THE PAIR ESTIMATE.
Choose chi nonnegative and nonzero. In the model, every point on its
support has gamma=2pi(k+1/4)/log(N/2) and beta=1/2. Its single carrier
at x=N/2 is therefore i, so the mock moment is i sum chi(gamma/N).
The model count is M(t)+O(1), with M as in the preceding module.
Stieltjes integration against the fixed smooth weight gives
 sum chi(gamma/N)
  =(N/(2pi))[L int chi(s)ds+int chi(s)log(s/(2pi))ds]+O_chi(1),
proving (2). Its order NL violates (1). The model satisfies the counting
constraints but cannot satisfy this ACTUAL prime-side explicit formula.

This demonstrates an arithmetic constraint that the count-compatible
model lacked. It supplies a uniform family of linear moments, not a
bound on their curved bilinear combination. The phase in J_N couples
gamma and eta, and its beta amplitude also depends on both heights.
No product of two copies of (1), no free shrinking-cutoff estimate, and
no all-log bound for that coupled sum has been deduced here. All prior
actual signed reductions remain valid and the remaining margin is OPEN.

Source/runtime corrections for continuation: the exact CCM locator is
1309.1526v1 Lemma5 and its unconditional proof remark, not the recalled
Lemma8 or the unavailable v2 URL. The SBM mirror returned Anubis access
denied; it was not retried or used. Garrett's stated theorem and the
CCM formula above are the selected authorities; no interpolation theorem
from2005.02996v3 is used. Earlier2016 kernel and density corrections,
polynomial components and runtime limitations all persist.
"""
from fractions import Fraction as F


def scaled_complex_zero_argument(beta, gamma, n):
    if type(beta) is not F or not 0<beta<1 or type(gamma) is not F:
        raise ValueError('rational real part in(0,1) and rational ordinate required')
    if type(n) is not int or n<1:
        raise ValueError('positive integer scale required')
    return {'real':gamma/n, 'imag':(F(1,2)-beta)/n}


def cutoff_error_powers(tail_order=16, cutoff_power=F(1,8)):
    if type(tail_order) is not int or tail_order<1 or type(cutoff_power) is not F or not 0<cutoff_power<1:
        raise ValueError('positive integer tail order and rational cutoff power in(0,1) required')
    return {'complex_shift':F(1,2),
            'whole_zero_tail':F(3,2)-tail_order*cutoff_power,
            'archimedean_tail':1-tail_order*cutoff_power}


def prime_sample_slope_bounds(x_over_n):
    if type(x_over_n) is not F or not F(1,3)<=x_over_n<=F(2,3):
        raise ValueError('rational normalized center in[1/3,2/3] required')
    return {'lower':1/(2*x_over_n), 'upper':2/x_over_n}


def integer_window_weight(center, radius=100):
    """Exact toy Schwartz majorant, not a prime-window measurement."""
    if type(center) is not F or type(radius) is not int or radius<1:
        raise ValueError('rational center and positive integer radius required')
    base=center.numerator//center.denominator
    return sum((1/(1+abs(F(j)-center))**2 for j in range(base-radius,base+radius+1)),F(0))


def analytic_real_imag_recombination(h, reflected_conjugate):
    """Formal coefficient pairs for H_R+i H_I=H, over rational inputs."""
    if any(type(v) is not F for v in (h,reflected_conjugate)):
        raise ValueError('rational formal values required')
    return {'real_component':(h+reflected_conjugate)/2,
            'i_times_imag_component':(h-reflected_conjugate)/2}
