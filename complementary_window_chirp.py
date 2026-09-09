"""Complementary additive phase can reinforce the exact window functional.

Owner: Kevin's Goldbach research. Purpose: test whether the newly proved
interval/energy bounds, even with strong global linear Fourier control,
force cancellation in the reflected two-window product. This is an
ARTIFICIAL coefficient model, not primes, zeta zeros or a Goldbach example.

1. THE PRECISE TEST AND ITS LIMITATION.
Use T=N^(9/10), H=N/T=N^(1/10), V=N^(1/8), and the SAME angular
Fourier window operator as short_prime_window_energy.py. Fix nonnegative
chi in C_c^infinity((1,2)) with chi(3/2)>0. Keep the fixed Fourier
cutoff nu from the actual Guinand construction. For a coefficient b(n),
 P_b(aN)=T/(2pi)sum_(n>=2) b(n)/sqrt n
             *hatChi(Tlog(n/(aN)))*nu(Tlog(n/(aN))/V).             (1)
Also fix zeta>=0 smooth, supported in(1/4,3/4), equal1 near1/2.
The central paired window functional is
 Q_b(N)=2 int_0^1 zeta(a)P_b(aN)P_b((1-a)N)/sqrt(a(1-a)) da.     (2)
It has NO complex conjugation. For actual Lambda coefficients this
is the central arithmetic expression relevant to the retained beta
transfer; here we apply exactly the same operator to an artificial b.

We construct b_N taking values in[1/2,3/2] such that
 Q_b(N)=-c_(chi,zeta) N+O_(chi,zeta)(N^(9/10)), c_(chi,zeta)>0,     (3)
while its centered global Fourier sums, with ANY fixed smooth spatial
cutoff psi compactly supported in(0,infinity), satisfy
 sup_(xi real)|sum_n psi(n/N)(b_N(n)-1)exp(-i*xi*n)|
                             <<_psi N*T^(-1/3)=N^(7/10).        (4)
The coefficient sequence is N-dependent. Its bounded positive density
also satisfies the interval-mass, fixed multiplicative-range mass and
window energy INEQUALITIES used in the preceding proof. It is dense:
it does NOT have actual prime support, the zeta explicit formula,
Type I information, or every property of Lambda. Thus(3)-(4) refute
only a deduction of o(N) paired cancellation from those listed marginal
inequalities and global linear Fourier smallness alone.

2. A PHASE WITH EXACT COMPLEMENTARY SYMMETRY.
Choose an odd integer m_N nearest to3T/pi, and put
 lambda_N=pi*m_N/T, f_N(a)=lambda_N*a+(a-1/2)^3,
 b_N(n)=1+(1/2)cos[T f_N(n/N)].                                  (5)
Nearest odd integers have spacing2, so
 |lambda_N-3|<=pi/T, exp(i*T*lambda_N)=-1.
For large N, lambda_N>2. The exact identities are
 f_N(a)+f_N(1-a)=lambda_N,
 f'_N(a)=lambda_N+3(a-1/2)^2=f'_N(1-a)>0,
 f'''_N(a)=6.                                                    (6)
The first identity is responsible for the paired reinforcement.
The last identity prevents a large global single Fourier mode.

3. THE LOCAL WINDOW SEES THE POSITIVE MODULATED PHASE.
More generally write epsilon=1/2 in b_N=1+epsilon*cos(T f_N).
Uniformly for a in[1/4,3/4], we prove
 P_b(aN)=(epsilon/2)sqrt(aN)
       *chi(a f'_N(a))*exp(i*T*f_N(a))+O_chi(N^(2/5)).           (7)
All constants stay uniform for lambda_N near3.

First replace the sum in(1) by its integral over real t. Its summand
extends to a smooth compactly supported function g(t) away from0,
since the Fourier cutoff forces t~aN and |t-aN|=O(VH)=o(N).
The elementary unit-interval estimate
 |sum_(n integer)g(n)-int_R g(t)dt|<=int_R |g'(t)|dt
applies. On this support b'_N(t)=O(T/N)=O(1/H), while the kernel
has absolute integral O(H) and absolute derivative integral O(1),
by Schwartz decay after the change Tlog(t/(aN)). Differentiating
t^-1/2 gives a still smaller term. Therefore
 int|g'|=O(N^-1/2),
and the prefactor T in(1) makes the total discretization cost
 O(T/sqrtN)=O(N^(2/5)).                                         (8)
This estimate does not count the full width VH with flat weight.

In the remaining integral put t=aN+H y. Then t/N=a+y/T, and
 T f_N(a+y/T)=T f_N(a)+f'_N(a)y+O(y^2/T),
 Tlog(t/(aN))=y/a+O(y^2/T),
 t^-1/2=(aN)^-1/2[1+O(|y|/T)].                                 (9)
The support has |y|=O(V), with V/T tending to0. On that range
the logarithmic argument and y/a are comparable; derivatives of
hatChi along the joining segments have arbitrary Schwartz decay.
The polynomial remainders in(9), multiplied by that decay, are
integrable with total O(1/T). Removing the nu cutoff and extending
y to the full real line costs O_chi(V^-16). Hence the integral equals
 sqrtN/(2pi*sqrt a)
 *int_R [1+epsilon*cos(T f_N(a)+f'_N(a)y)]hatChi(y/a)dy
       +O_chi(sqrtN/T+sqrtN*V^-16).                             (10)
These two errors are smaller than(8).

Angular Fourier inversion gives
 int hatChi(y/a)exp(i*c*y)dy=2pi*a*chi(a*c).
Here chi(0)=0 and chi(-a f'_N(a))=0, since f'_N>0. Thus the
constant background and negative-frequency half of the cosine both
vanish in(10). The positive-frequency half has coefficient epsilon/2,
giving exactly(7). No claim about an actual zero moment is made.

4. THE REFLECTED PRODUCT HAS A NEGATIVE MAIN OF ORDER N.
Substituting(7) into(2) cancels the square-root a weights. The product
of the main terms has the constant phase exp(i*T*lambda_N)=-1 by(6).
Consequently
 Q_b(N)=-(epsilon^2/2)N int zeta(a)
       *chi(a f'_N(a))*chi((1-a)f'_N(a))da+O(N^(9/10)).          (11)
Indeed each main is O(sqrtN), each error is O(N^(2/5)), and zeta
stays away from0 and1. The cross error is N^(1/2+2/5)=N^(9/10);
the product of two errors is smaller. Replacing lambda_N by3 in
the amplitude costs O(N/T), by smoothness and its paid lattice error.
Thus the constant in(3) is
 c_(chi,zeta)=(1/8)int zeta(a)
    *chi(a[3+3(a-1/2)^2])*chi((1-a)[3+3(a-1/2)^2])da>0.           (12)
Both chi arguments are3/2 at a=1/2, so positivity follows on a
fixed neighborhood. This proves an ACTUAL negative asymptotic for
the DEFINED MODEL functional, not merely a possible sign of a kernel.

5. STRONG GLOBAL LINEAR FOURIER CANCELLATION STILL HOLDS.
To prove(4), expand the centered cosine into its two exponentials
and use Poisson summation for the smooth compact spatial cutoff.
Reduce xi modulo2pi to[-pi,pi]. Each Poisson term is
 N int psi(a)exp{i[+-T*f_N(a)-N*(xi+2pi*k)*a]}da.                (13)
For k=0 the phase has third derivative +-6T, independently of xi.
Its integral is O_psi(T^-1/3). An elementary proof splits out
|a-1/2|<=T^-1/3, of that length. On either remaining side the
second derivative has fixed sign and magnitude at least6T^(2/3).
The second-derivative integral estimate costs O(T^-1/3) there too,
including bounded-variation amplitudes and the split endpoints.
For completeness that estimate follows by removing |phase'|<=sqrtM,
whose length is O(M^-1/2) when |phase''|>=M; on each remaining
piece phase' is monotone and one integration by parts costs the
same O(M^-1/2), times the amplitude's supremum and total variation.

For k nonzero the first derivative in(13) has magnitude at least
c*N*|k|, for sufficiently large N depending on psi: T=o(N) and
f'_N is bounded on its fixed support. The next two derivatives are
O_psi(T). Twice integrating by parts, with no support-boundary term,
costs O_psi((N|k|)^-2), since T<=N. Multiplication by N and summation
over k nonzero therefore costs O_psi(N^-1). Combining with the k=0
term proves(4). Poisson and the integrations apply to smooth compact
functions, so no unproved unsmoothed alias estimate has been used.
The centering b_N-1 is essential; the constant background has an
order-N Fourier coefficient at xi=0.

6. THE MODEL PASSES THE LISTED MARGINAL BOUNDS AND PRESERVES THE GAP.
Because1/2<=b_N(n)<=3/2, every interval of length R>=H has total
mass O(R), sum_(n<=CN)b_N(n)=O_C(N), and
sum_(N/8<=n<=2N)b_N(n)/n=O(1). The same Schwartz shell and weighted
Schur proof therefore gives pointwise P_b=O(sqrtN) and da-energy O(N).
Equation(7) also makes that energy at least cN on a central interval,
so its scale can be saturated. These are numerical inequalities about
coefficient masses; they do not identify b_N with a prime measure.

The older resonant_semiprime_error.py countermodel concerned primitive
Ramanujan frequencies and factored-modulus progression variance. This
model instead identifies the explicit local additive phase symmetry
f(a)+f(1-a)=constant in the CURRENT window product. No new general
barrier is claimed: it is one bounded test of which additional arithmetic
information a proposed improvement would have to exploit.
Actual prime differences/sums, sparse support, local arithmetic and
their signed correlations remain potential inputs. The polynomial
components and every source correction are preserved. The sufficient
Goldbach signed lower margin and overall research goal remain OPEN.
"""
from fractions import Fraction as F


def phase(a, slope):
    if type(a) is not F or type(slope) is not F:
        raise ValueError('exact rational phase parameters required')
    return slope*a+(a-F(1,2))**3


def local_frequency(a, slope):
    if type(a) is not F or type(slope) is not F:
        raise ValueError('exact rational phase parameters required')
    return a*(slope+3*(a-F(1,2))**2)


def model_budget():
    t=F(9,10)
    return {'sum_to_integral':t-F(1,2),
            'local_linearization':F(1,2)-t,
            'paired_cross_error':t,
            'global_fourier':1-t/3,
            'slope_replacement':1-t,
            'paired_prefactor':F(1,8)}
