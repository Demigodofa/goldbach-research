"""Character-mean transfer for the actual cubic rough-semiprime weight.

Owner: Kevin's research. Purpose: retain the analytic input needed for a
future Fourier approximation, with an exact verifier for its factor identity.
This is not a Goldbach-count implementation or a numerical onset certificate.

Character-mean lemma (independently checked by Sol, 2026-09-08):
Let Y be sufficiently large, exp((log Y)**(4/5))<=R<=Y**(1/100), and
Y**(1/4)<=z<=Y**(2/5). Put S_z(n)=1 if n=p*q for primes p,q>z, including
prime squares, and zero otherwise. Define
  k_z(t)=log(log(t)/log(z)-1)/log(t) for t>z*z, and zero otherwise.
Use primitive Dirichlet characters chi of conductor r<=R, including the
principal character at r=1. Fix a sufficiently small positive quality kappa
for the source's exceptional-zero alternative. For intervals I=(a,b] within
[1,Y], use real length |I|=b-a. If there is no exceptional zero of level R
and quality kappa, then, for some absolute c>0,
  sum_{r<=R} sum_{chi primitive mod r} sup_I
    log(Y)/(|I|+Y/R) *
    |sum_{n in I} S_z(n)*chi(n) - 1_{r=1}*integral_I k_z(t) dt|
      << exp(-c*kappa*log(Y)/log(R)).
If there is the exceptional character chi_e with zero beta, insert the
ADDITIONAL POSITIVE term
  1_{chi=chi_e}*integral_I k_z(t)*t**(beta-1) dt
in the model being subtracted, and replace the right side by
  (1-beta)*log(Y)*exp(-c*log(Y)/log(R)).
The implied constants and onset are not supplied numerically. At R=Y**delta
this exponential saving is a small constant depending on delta, not a power
of Y. The value of this input is its uniformity through power-sized moduli.

Proof from the prime-indicator Gallagher estimate:
1. Exactly, for any character chi,
   sum_I S_z(n)*chi(n)
     = (1/2)*sum_{p,q>z primes, p*q in I} chi(p)*chi(q)
       + (1/2)*sum_{p>z prime, p*p in I} chi(p)**2.
   The square term repairs its half-weight in the ordered double sum.
2. For each outer prime p<=Y/z, put U=Y/p>=z. The prime-indicator
   Lemma 7.4 cited below applies with the SAME R: exp(sqrt(log U))<=R,
   and R<=Y**.01<=U**(1/7). Its inner interval J=(I/p) intersect (z,U]
   has |J|<=|I|/p, and |J|+U/R<=(|I|+Y/R)/p. Integer endpoint changes
   of size 1 are absorbed by U/R. Also log(Y)/log(U)<=4.
   Triangle inequalities allow summing the source's character-averaged
   errors over p. Chebyshev's prime bound and partial summation give
   sum_{z<p<=Y/z}1/p=O(1), since log(Y/z)/log(z)<=3. Consequently this
   first replacement costs the asserted normalized error (with smaller c).
3. The continuous inner model density w_chi(q) is 1/log(q) for r=1,
   -q**(beta-1)/log(q) for chi=chi_e, and zero otherwise. The two cases
   are disjoint. The source initially has a discrete model sum; replacing
   it by the integral costs O(1/log z) per interval because these model
   densities are monotone in absolute value, with total variation bounded
   by their left-end value. This affects at most two characters.
4. For those characters, swap the resulting q-integral and the remaining
   p-prime sum. Apply the same prime lemma at U=Y/q to the p interval.
   The normalized error is integrated against at most dq/(q*log q), whose
   integral over [z,Y/z] is O(1). Thus the second replacement has the
   same error size. The principal double model has positive sign; the two
   negative exceptional densities also multiply to a positive sign, with
   product weight (p*q)**(beta-1)/(log p*log q). No independent-prime
   hypothesis was used: both replacements are applications of the theorem.
5. The derivative of half the continuous ordered double integral is
   (1/2)*integral_{z}^{t/z} du/(u*log u*log(t/u)) = k_z(t).
   Substitute v=log u; the partial fractions 1/[v*(log t-v)] evaluate it
   exactly. In the exceptional case the product weight pulls out as
   t**(beta-1). This proves the claimed main integrals, including the
   empty region t<=z*z and its endpoint.
6. There are O(R**2) primitive characters and at most sqrt(Y) prime
   squares. Their total normalized error is O(R**3*log(Y)/sqrt(Y)).
   The two discrete-to-integral replacements cost at most O(R*log(Y)/z):
   bound the number of outer primes, or the absolute outer model integral,
   by O(Y/z), then multiply O(1/log z) and the normalization R*log(Y)/Y.
   These deliberately loose residual bounds are power-small in our range.
7. In the exceptional case the source's (7.2) gives
   1-beta >> R**(-1/2)/(log R)**2. Moreover log(Y)/log(R)<=log(Y)**(1/5).
   Dividing the residual powers by the desired exceptional bound still
   leaves a negative power of Y times logarithmic and subpower factors.
   They are therefore absorbed for sufficiently large Y. The unexceptional
   absorption is easier. This completes the uniform character-mean proof.

Bulk normalization corollary: for intervals I within [Y/2,Y], the weight
  Lambda_{2,z}(n)=S_z(n)/k_z(n)
has the same character estimate without log(Y) in the numerator, and with
main density 1_{r=1}+1_{chi=chi_e}*t**(beta-1). Indeed k_z(t) is comparable
to 1/log(Y) on this bulk range. The supremum plus total variation of 1/k_z
is O(log Y): writing l=log t, its derivative follows from
  d[log(l/log z-1)/l]/dl
    = (l/(l-log z)-log(l/log z-1))/l**2 = O(1/log(Y)**2).
Abel summation loses O(log Y), cancelling the original normalization.
Every prefix of I has length <=|I|, preserving the denominator bound.
The normalized weight is O(log Y). Changing the new main integral to the
corresponding discrete sum costs O(R/Y), again absorbable. This corollary
does not extend normalization to t=z*z, where the kernel is zero.

Minor-arc lemma in the same Y,z,R range:
Let the major arcs be all circle distances |alpha-a/q|<=2R/Y for reduced
a/q with 1<=q<=R. On their complement, uniformly for every T<=Y,
  |sum_{n<=T} S_z(n)*exp(2*pi*i*alpha*n)| << Y*R**(-1/3).
The same bound holds for the normalized weight Lambda_{2,z} on [Y/2,Y].
This estimate uses bounded prime-factor indicators, not a distribution
assumption about additive prime pairs.

Proof: Dirichlet approximation with Q=floor(Y/R) gives a reduced a/q with
q<=Q and |alpha-a/q|<=1/(q*Q)<=1/q**2. If q<=R, that point lies in the
major arcs since 1/(q*Q)<=2R/Y. Hence R<q<=Y/R on the complement.
Split the ordered prime factors into O(log(Y)**2) dyadic rectangles
m in [M,2M), n in [K,2K), retaining the exact product cutoff mn<=T.
For any nonempty rectangle, M,K>=z/2, M,K<=Y/z, and M*K<=Y. With
coefficients of modulus <=1, Cauchy--Schwarz over m, followed by expansion
in n1,n2, gives
  |block|**2 << M*K*(M+sum_{1<=h<=K}min(M,1/||alpha*h||)).
The m-sum has an interval endpoint min(T/n1,T/n2), so the product cutoff
does not invalidate the geometric-sum bound. Here ||.|| is distance to
the nearest integer and min(M,1/0) means M.
In each h-block of at most floor(q/2) consecutive integers, the points
alpha*h modulo 1 are at least 1/(2q) apart: for distinct points their
difference d has 0<|d|<q/2, so ||a*d/q||>=1/q and the approximation
error is at most |d|/q**2<1/(2q). Summing reciprocal distances within
such a block costs O(M+q*log(2q)). There are O(K/q+1) blocks. Therefore
  |block|**2 << M*K*(M*K/q+M+K*log(2q)+q*log(2q))
    << Y**2*(1/q+1/z+q/Y)*log(2Y)
    << Y**2*log(2Y)/R.
Summing rectangles and adding the at most sqrt(Y) squares gives
  O(Y*R**(-1/2)*log(Y)**(5/2)+sqrt(Y)).
The bound is uniform in T, so Abel summation multiplies it by O(log Y)
for Lambda_{2,z}. Since R>=exp((log Y)**(4/5)), these logarithmic factors
are absorbed by R**(1/6) for sufficiently large Y, proving both assertions.

Additive minor-contribution corollary: put
  H(N)=integral_minor (sum_{n<=Y} S_z(n)*exp(2*pi*i*alpha*n))**2
                      *exp(-2*pi*i*alpha*N) d alpha.
Parseval and S_z(n) in {0,1} give
  sum_{N in integers}|H(N)|**2 << Y**3*R**(-2/3).
Thus |H(N)|>Y/log(Y)**3 for at most
  O(Y*R**(-2/3)*log(Y)**6)=O(Y*R**(-1/2))
integer targets. For fixed R=Y**delta this is a power-saving exceptional
set for this MINOR-ARC ERROR ONLY. Major-arc terms have not been controlled
here, so it is not an exceptional-set theorem for positivity of L.

Source prerequisite: Grimmelt--Teravainen, arXiv:2508.16400v2, Lemma 7.4
and equation (7.2), https://arxiv.org/html/2508.16400v2#S7.SS2 .
The proof above establishes the rough-E2 extension; the source states the
prime-input theorem. The signed major-arc model with a pointwise error bound
has since been established in major_arc_kernel.py; read its correction to
the source's squarefree-supported majorant before applying that model.
Its ordinary pair-error bounds are proved in radical_majorant_correlation.py.
Replacement by a nonnegative rough-number model and convolution errors
relative to possibly suppressed main terms remain open. These lemmas and
finite tests do not prove a power-saving exceptional set for canonical L or
new pointwise Goldbach coverage, including powers of two.
"""
from fractions import Fraction


def factor_components(primes: list[int], cutoff: int, lower: int, upper: int,
                      weights: tuple[int | Fraction, ...]) -> tuple[Fraction, Fraction, Fraction]:
    """Return (unordered, ordered, square) weighted sums on (lower,upper].

    Conditional input: primes is a correct complete prime list through
    floor(upper/(cutoff+1)); additional primes are harmless. Type/order checks
    do not certify primality or completeness. No prime oracle is called.
    The periodic rational weights may be character components or any other
    periodic function: the identity uses weights[p*q], so this finite
    verifier does not itself assert character multiplicativity or primitivity.
    It is intended for small controls, not a speed or range improvement.
    """
    if (type(cutoff) is not int or cutoff < 2 or type(lower) is not int or
            type(upper) is not int or not 0 <= lower <= upper):
        raise ValueError("require integer cutoff>=2 and 0<=lower<=upper")
    if (any(type(p) is not int or p < 2 for p in primes) or
            any(a >= b for a, b in zip(primes, primes[1:]))):
        raise ValueError("prime inputs must be strictly increasing integers >=2")
    if not weights or any(type(w) not in (int, Fraction) for w in weights):
        raise ValueError("weights must be a nonempty exact rational period")
    eligible = [p for p in primes if cutoff < p <= upper // (cutoff+1)]
    period = len(weights)
    ordered = Fraction(0)
    square = Fraction(0)
    for p in eligible:
        for q in eligible:
            n = p*q
            if n > upper:
                break
            if n > lower:
                ordered += weights[n % period]
        if lower < p*p <= upper:
            square += weights[p*p % period]
    return (ordered+square)/2, ordered, square
