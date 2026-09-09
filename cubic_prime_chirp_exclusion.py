"""Actual primes exclude the preceding model's coherent cubic coefficient.

Owner: Kevin's Goldbach research. Purpose: test a concrete arithmetic input
against complementary_window_chirp.py, preserving its model and the open
paired-correlation gap. This is an application of a KNOWN prime exponential
sum theorem, not a new prime-distribution theorem or a Goldbach proof.

1. PRECISE ACTUAL ESTIMATE.
Let T=N^(9/10), f_N(a)=lambda_N*a+(a-1/2)^3, and let psi be a fixed
smooth function compactly supported in (0,infinity). The slope lambda_N
may be ANY real number depending on N. With actual von Mangoldt weights,
 M_N=sum_(n>=2) psi(n/N)Lambda(n)exp[-i*T*f_N(n/N)]
                              =O_psi(N^(63/64)).                 (1)
In particular this applies to the nearest-odd phase choice in the model.
The implied constant in (1) is uniform in lambda_N. More generally the
same estimate permits arbitrary N-dependent quadratic, linear and constant
coefficients, with cubic coefficient fixed at -T/(2pi*N^3) in e-notation.
No prime numerical experiment, RH or averaging over N is used.

2. CHECKED SOURCE AND PRECISE NORMALIZATION.
Thai Hoang Le and Craig V. Spencer, 'Intersective polynomials and
Diophantine approximation, II', author PDF:
 https://home.olemiss.edu/~leth/papers/intersective_polynomials_II_2.pdf
Retrieved 2026-09-09; SHA256
 095a441476c6ebce81a0a597c80cbd5917c1df417f82f0316e1b21843270fcd4.
Section4, Lemma5, printedp8 gives Harman's prime Weyl bound for GENERAL
real polynomials, not just monomials. To keep coprimality explicit, use
Theorem5 printedp9 with m=1,b=0 and the weight defined on printedp6:
lambda_(1,0)(n)=log n for primes and zero otherwise. For a degree-k real
polynomial F with leading coefficient alpha, reduced a/q, and
 |alpha-a/q|<=1/q^2,
it gives, for k>1 and every fixed epsilon>0,
 |sum_(p<=X) log p * e(F(p))|
 <<_(k,epsilon) X^(1+epsilon)
                *(q^-1+X^-1/2+q*X^-k)^(4^(1-k)).              (2)
Here e(u)=exp(2pi*i*u). The Section4 setup and printedp3 notation leave
the lower coefficients unrestricted; the constant is independent of them.
A constant term can be removed as a unit complex factor. The source's
lambda_(m,b) is its prime-progression weight, not von Mangoldt Lambda.

PartI, author PDF https://www.math.ksu.edu/~cvs/le_spencer-intersective.pdf,
Lemma4 printedp8 also states this general-polynomial bound. Both attribute
the k>1 estimate to Harman, 'Trigonometric sums over primes I', Mathematika
28 (1981), 249-254, Theorem1. The original publisher PDF route returned
abstract HTML and was NOT read as a PDF. The Citeseer mirror timed out;
the actual author-hosted PartII PDF above supplies the checked statement.
Kumchev's monomial theorem alone was not used for a mixed cubic.

3. RECIPROCAL APPROXIMATION AND THE FIXED POWER SAVING.
Put F_N(x)=-T*f_N(x/N)/(2pi). Its leading coefficient is
 alpha=-T/(2pi*N^3)=-1/Q0, Q0=2pi*N^3/T=2pi*N^(21/10).
Take q a nearest positive integer to Q0 and a=-1. Then (a,q)=1 and
 |alpha+1/q|=|q-Q0|/(q*Q0)<=1/(2*q*Q0)<1/q^2                  (3)
for Q0>1, since q<=Q0+1/2<2Q0. Thus q is comparable to N^(21/10).
This verifies an ACTUAL rational approximation; we do not simply insert
the reciprocal of alpha as if it were an integer denominator.

For X in [A*N,B*N], with fixed 0<A<B, the bracket in (2), k=3, is
 O_(A,B)(N^(-21/10)+N^(-1/2)+N^(-9/10))=O_(A,B)(N^(-1/2)).
The outer exponent is 4^(1-3)=1/16. Consequently
 |sum_(p<=X)log p*exp[-i*T*f_N(p/N)]|
                              <<_(A,B,epsilon) N^(31/32+epsilon).
Choose epsilon=1/64 to obtain N^(63/64). All coefficients and q are
held fixed for that N when varying the prefix endpoint X. The estimate
is uniform over the displayed comparable range; no small-X bound with
the same N-scale denominator is asserted or needed.

4. SMOOTHING AND PROPER PRIME POWERS.
Choose A,B with support(psi) inside (A,B). Stieltjes partial summation
against psi(X/N) uses only prefixes at X in [AN,BN]. The boundary
terms vanish, and the derivative has total integral
 int_(AN)^(BN) |psi'(X/N)|/N dX=int_A^B |psi'(u)|du=O_psi(1).
The prime-only smoothed sum therefore has the same exponent. Complex
psi is allowed, either directly or by splitting real and imaginary parts.

For j>=2, p^j<=BN implies p<=sqrt(BN), and only O_B(log N) exponents
j occur. The elementary bound counting all possible integer bases gives
 sum_(j>=2,p^j<=BN) log p=O_B(sqrtN*log^2 N).
Multiplication by bounded psi and a unit phase changes only a constant.
This is o(N^(63/64)), and adding proper powers proves (1).
The estimate is asymptotic with a nonnumerical implied constant; it gives
no explicit finite verification threshold.

5. THE PREVIOUS MODEL FAILS THIS ADDITIONAL ARITHMETIC TEST.
Now choose lambda_N as in complementary_window_chirp.py, so lambda_N->3,
and b_N(n)=1+(1/2)cos[T*f_N(n/N)]. The exact cosine expansion gives
 sum_n psi(n/N)b_N(n)exp[-i*T*f_N(n/N)]
 =sum_n psi(n/N)exp[-i*T*f_N(n/N)]
   +(1/4)sum_n psi(n/N)
   +(1/4)sum_n psi(n/N)exp[-2i*T*f_N(n/N)].                     (4)
The cubic Poisson argument in the model applies to the first and third
sums, with fixed phase multipliers -1 and -2: both are O_psi(N^(7/10)).
The nonzero Poisson aliases are paid because the slope stays bounded
and T=o(N); the central integral uses the nonzero cubic derivative.
Ordinary smooth Poisson summation gives sum psi(n/N)=N int psi+O(N^-1).
Therefore the model coefficient is
                    (N/4)int psi+O_psi(N^(7/10)).              (5)
For nonnegative nonzero psi this has nonzero order-N size. Equation(1)
excludes that coherent cubic coefficient for ACTUAL Lambda. Subtracting
the constant background from both measures preserves the distinction:
the background's correlation is already O(N^(7/10)) for this slope.

6. WHAT HAS AND HAS NOT BEEN CLOSED.
The preceding model remains a valid demonstration that the listed mass,
energy and linear-Fourier inequalities alone do not force o(N) paired
cancellation. Actual primes satisfy an additional NONLINEAR test that
this particular model fails. This supplies a specific arithmetic reason
the exhibited global cubic reinforcement cannot occur with order-N
coefficient in Lambda.

There is NO theorem here extracting a large cubic coefficient from every
large reflected two-window correlation. General nonpolynomial phases,
localized coherence, superpositions and cumulative losses remain open.
Thus this does not improve the actual O(N) comparable-band bound,
delete that band, supply a small constant, or prove the sufficient
Goldbach signed lower margin. Polynomial identities and bounds remain
useful components; no general limitation on their use is inferred.
"""
from fractions import Fraction as F


def reciprocal_approximant(reciprocal):
    """Exact denominator nearest a positive rational reciprocal >1."""
    if type(reciprocal) is not F or reciprocal <= 1:
        raise ValueError('an exact rational reciprocal greater than one is required')
    shifted = reciprocal + F(1, 2)
    return shifted.numerator // shifted.denominator


def cubic_bound_budget(t=F(9, 10), epsilon=F(1, 64)):
    """Exponent bookkeeping; a saving requires the returned total <1."""
    if type(t) is not F or type(epsilon) is not F or not 0 < t < 3 or epsilon <= 0:
        raise ValueError('exact 0<t<3 and epsilon>0 required')
    q_exponent = 3-t
    bracket = max(-q_exponent, -F(1, 2), q_exponent-3)
    return {'denominator': q_exponent, 'bracket': bracket,
            'harman_power': F(1, 16), 'prime_total': 1+epsilon+bracket/16,
            'proper_power': F(1, 2), 'model_coefficient': F(1, 4)}
