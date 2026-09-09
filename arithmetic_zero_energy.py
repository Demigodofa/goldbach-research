"""A mean-square arithmetic zero moment, with the displacement error paid.

Owner: Kevin's Goldbach research. Purpose: strengthen the saved arithmetic
moment into a reusable energy bound at a fixed target N. The integral is
over the frequency parameter a, NOT over targets N. No RH, prime-pair
estimate, zero computation, numerical onset or novelty claim is used.

1. RESULT AND ITS EXACT RELATION TO THE REMAINING PROBLEM.
Keep chi, nu, V=N^(1/8), the angular Fourier transform, and S_N(x) from
arithmetic_zero_moment.py. Thus chi is fixed real C_c^infinity((c,2c)),
c=1/100, and S_N(x)=sum_(gamma>0)chi(gamma/N)*x^(rho-1/2), with ACTUAL
beta and multiplicities. Write L=logN and I=[1/3,2/3]. We prove
 int_I |S_N(aN)|^2 da <<_chi N L.                                   (1)
Equivalently the integral over x in[N/3,2N/3] is O_chi(N^2 L).
These different measures must not be confused. Squaring the previously
proved pointwise sqrtN L bound only gave O(N L^2) in the a measure.

We also prove the sharper uniform arithmetic approximation
 S_N(x)=-P_N(x)+O_chi(L^6),  N/3<=x<=2N/3,                          (2)
 P_N(x)=N/(2pi) sum_(n>=2) Lambda(n)/sqrt n
                *hatChi(Nlog(n/x))*nu(Nlog(n/x)/V).
This is the SAME finite prime window as in the preceding theorem; it
includes all prime powers. No unproved local prime asymptotic is inserted.

The energy is a nonnegative conjugated product, integrated in a. It is
not the signed nonconjugated zero-pair kernel J_N with its coupled phase
and beta amplitude. Neither (1) nor (2) deletes a new part of C_remaining
by itself. The sufficient pointwise Goldbach lower margin remains OPEN.

2. A FIRST MOMENT OF THE OFF-CRITICAL WEIGHTS COSTS ONLY N L^6.
On cN<=gamma<=2cN, uniformly for x in the stated interval, put
 W_N(x)=sum x^(beta-1/2).
For beta<=1/2, bound the weight by1, paying O(NL) with total zero count.
Layer cake for the remaining weights gives the upper bound
 W_N(x)<=M_N+logx int_(1/2)^1 x^(sigma-1/2) N_z(sigma,2cN)ds,        (3)
where M_N counts ALL zeros in the band, not only those right of1/2.
The retained uniform Ingham bound gives
 N_z(sigma,2cN)<<N^[D(u)] L^5, D(u)=3u/(1+u), u=1-sigma.
This is the previously source-checked arXiv2507.15184v2 Corollary1 /
Table1 bound, used in spectral_low_axis_bound.py. Its endpoint/compact
extension and multiplicity conventions remain those already reviewed.
The exact elementary identity is
 1/2-[D(u)-u]=(1/2-u)(1-u)/(1+u)>=0, 0<=u<=1/2.                    (4)
Since x~N and sigma is in a fixed interval,
 x^(sigma-1/2) N^D(u)<<N^[1/2-u+D(u)]<=N.
Consequently W_N(x)<<N L^6. No zero-free restriction is needed here.

3. RETAIN THE FIRST TAYLOR TERM; DO NOT PAY IT BY TOTAL COUNT.
The preceding Fourier-cutoff estimates also apply to every fixed
derivative of chi_V. For real u, |b|<=1/2 and any fixed r>2, Taylor's
formula along the short complex segment gives
 chi_V(u-i*b/N)
  =chi(u)-i*b/N*chi'(u)
     +O_chi((N^-2+V^-16)(1+|u|)^-r).                              (5)
To justify this globally, first Taylor-expand the ENTIRE chi_V. Its
second derivative is uniformly Schwartz along the segment by weighted
Fourier integration by parts; exp(v*b/N) stays bounded for |v|<=2V.
Then replace chi_V and chi_V' on the real axis using their V^-16
Schwartz tails. This argument does not analytically continue chi itself.

At a zero, take u=gamma/N and b=beta-1/2. The first correction in (5)
is supported at positive heights in[cN,2cN]. Multiplying by x^(rho-1/2)
and summing its absolute value costs at most C_chi W_N(x)/N=O_chi(L^6).
For the remaining error use the GLOBAL, both-sign bound
 sum_rho (1+|gamma|/N)^-r <<NL,
and the crude |x^(rho-1/2)|<=sqrt x<<sqrtN. This pays
 (N^-2+V^-16)*N^(3/2)L=O(N^-1/2 L).                               (6)
Negative heights and all multiplicities are included here. This is why
the localized first term and the distant remainder are treated separately.
Thus the exact Guinand zero sum equals S_N(x)+O_chi(L^6).

The pole tests are also smaller than their old crude sqrtN bound. At
u=0, chi(0)=chi'(0)=0 because its support stays away from0. Equation(5)
gives chi_V(+-i/(2N))=O(N^-2+V^-16)=O(N^-2). Hence
 |H(i/2)|+|H(-i/2)|<<sqrtN*N^-2=N^-3/2.                            (7)
The already proved Gamma-integral estimate remains O(1): its real-axis
cutoff tail is O(N^-1 L), and compact-support integration by parts pays
the main. The exact angular transform and its positive-frequency support
are unchanged. Combining these estimates with the unconditional formula
in arithmetic_zero_moment.py proves (2), with its stated minus sign.

4. THE SMOOTH PRIME WINDOW IS A BOUNDED SAMPLING OPERATOR.
For a in I, write
 K_N(a,n)=hatChi(Nlog(n/(aN)))*nu(Nlog(n/(aN))/V).
For sufficiently large N, support of nu forces n in[N/4,N] and
n/(aN) in[1/2,2]. As previously proved,
 |Nlog(n/(aN))|>=(3/4)|n-aN|.
Therefore for a fixed r>1, |K_N(a,n)|<=C_chi(1+|n-aN|)^-r, and
 sup_(a in I) sum_n |K_N(a,n)|<=C_chi,
 sup_n int_I |K_N(a,n)|da<=C_chi/N.                                (8)
The first estimate is uniform summability over integer translates.
For the second, substitute t=aN and enlarge the integral to R; its
Jacobian 1/N is essential. The kernel need not be positive or real.

For ANY finitely supported complex coefficients b_n, weighted Cauchy
followed by (8) proves
 int_I |sum_n b_n K_N(a,n)|^2 da
 <=int_I [sum_n |K_N(a,n)|]*[sum_n |b_n|^2 |K_N(a,n)|] da
 <=C_chi/N *sum_n |b_n|^2.                                        (9)
No assertion about cancellation between two primes occurs in (9).
Counting O(V) terms with flat weight would not give the first bound
in (8); the rapid decay is an actual part of the argument.

Take b_n=Lambda(n)/sqrt n for n in[N/4,N], and zero otherwise. Then
 sum_n |b_n|^2<=4/N sum_(n<=N) Lambda(n)^2
             <=4L/N *psi(N)<<L.                                   (10)
Here Lambda(n)^2<=L Lambda(n) includes prime powers. Only the elementary
Chebyshev upper bound psi(N)<<N is needed, not a PNT asymptotic. For
completeness, if m is a positive integer then each prime power in(m,2m]
contributes its log-prime weight to log binomial(2m,m): its valuation
summand floor(2m/p^k)-2floor(m/p^k) is1, while all other summands are
nonnegative. Hence psi(2m)-psi(m)<=log binomial(2m,m)<=2m log2.
Sum at powers of2 and use monotonicity to obtain psi(y)<=4y log2 for
y>=1, which suffices for (10). No prime count measurement is used.

Multiply (9) by N^2/(4pi^2), then use (10). The result is
 int_I |P_N(aN)|^2 da <<_chi N L.
Finally (2) and |z+w|^2<=2|z|^2+2|w|^2 give
 int_I |S_N(aN)|^2 da <<_chi N L+L^12 <<_chi N L                    (11)
for sufficiently large N. The approximation was sharpened BEFORE being
squared; the older O(sqrtN L) replacement would not have paid (11).

5. PRESERVED BOUNDARIES.
The fixed smooth cutoff is essential to the uniform seminorms above.
No shrinking chi, derivative family with uncharged norms, target average,
arbitrary beta-modulated moment or bilinear transfer is licensed. The
actual count-model exclusion remains valid, and the polynomial identities,
signed spectral deletions and all source/runtime corrections persist.
Guinand/CCM source conventions are those explicitly checked in the prior
module, including its complex off-critical test. No new source theorem is
imported in this extension. Exact helpers below guard the exponent budget
and a finite Schur inequality, not the continuous theorem by computation.
"""
from fractions import Fraction as F

from spectral_low_axis_bound import density_power


def first_weight_power(u):
    """The source density envelope for sum N^(beta-1/2), with u=1-beta."""
    return F(1,2)-u+density_power(u)


def localized_taylor_powers(remainder_order=2, tail_order=16):
    if type(remainder_order) is not int or remainder_order<1:
        raise ValueError('positive integer Taylor remainder order required')
    if type(tail_order) is not int or tail_order<1:
        raise ValueError('positive integer Fourier tail order required')
    return {'localized_first_term':F(0),
            'global_remainder':F(3,2)-remainder_order,
            'global_cutoff_tail':F(3,2)-F(tail_order,8),
            'pole_remainder':F(1,2)-remainder_order}


def finite_schur_energy(matrix, row_weights, coefficients):
    """Exact real finite analogue; row weights specify the integration measure.

    This is an algebraic guard, not numerical quadrature for K_N and not
    a prime/zero calculation. The proof above allows complex coefficients.
    """
    if not matrix or not coefficients or len(matrix)!=len(row_weights):
        raise ValueError('nonempty compatible matrix, weights and coefficients required')
    if any(len(row)!=len(coefficients) for row in matrix):
        raise ValueError('incompatible matrix columns')
    entries=[v for row in matrix for v in row]+list(row_weights)+list(coefficients)
    if any(type(v) is not F for v in entries) or any(w<0 for w in row_weights):
        raise ValueError('exact rational entries and nonnegative row weights required')
    row_bound=max(sum((abs(v) for v in row),F(0)) for row in matrix)
    column_bound=max(sum((w*abs(row[j]) for w,row in zip(row_weights,matrix)),F(0))
                     for j in range(len(coefficients)))
    energy=sum((w*sum((v*b for v,b in zip(row,coefficients)),F(0))**2
                for w,row in zip(row_weights,matrix)),F(0))
    bound=row_bound*column_bound*sum((b*b for b in coefficients),F(0))
    return {'energy':energy,'bound':bound,'row_bound':row_bound,'column_bound':column_bound}
