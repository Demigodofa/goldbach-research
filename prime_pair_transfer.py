"""Prime transfer, dyadic composition, and a power-saving L bound.

Owner: Kevin's research. Purpose: connect the checked signed models to the
actual canonical parity bound. The finite helpers verify interval composition
and weighted-to-unweighted inequalities, not analytic constants or prime labels.
Sol checked the complete transfer on 2026-09-08: prime approximation,
common dyadic parameters, extended correlations, suppressed margins,
unweighting, composite containment, and the discarded end segments.
Four finite controls passed normally and with Python -O. They validate
the exact algebra separately from the analytic proof review.

Prime-side Fourier lemma:
On I=(Y/2,Y] put F_-(n)=log(n)*1_prime(n), zero outside. In the range
exp(log(Y)**(4/5))<=R<=Y**(1/400), the same exceptional alternative at
level R**4 as major_arc_kernel.py gives
  F_-=M_-+E_-+V_-, |E_-|<<_G e*H_R(rad(n)),
  ||V_-hat||_infinity<<_G Y*R**(-1/3).                         (1)
Here M_- is the MINUS-sign model in signed_pair_main_term.py, the functions
are supported on I. Choose a common smaller c so that e has the same
unexceptional or exceptional form for both this and the rough-semiprime
model. If D>R**2, omit its model term
while retaining the exceptional error alternative.

Proof of (1):
a. Source Grimmelt--Teravainen (7.10), proved before the disputed H bound,
   gives ||Lambda-Lambda*b_R||hat<<YR**(-1/3) on I. Its proof uses the
   elementary kernel extraction and standard prime minor-arc estimates.
   The kernel has h=Y/R**4 and
     ||b_R||_1 << R**2*log R+R**8/Y << R**2*log R.
   Indeed |c_q(t)|<=(q,t), sum_{|t|<=h}(q,t)<<h*tau(q)+q, and q<=R**2.
   If the source convolution uses global Lambda, cutting it to I changes
   only endpoint strips; the L1 cost is O(h*log Y*||b_R||_1).
   Removing prime powers costs O(sqrt(Y)*log(Y)**2*(1+||b_R||_1)).
   Both are o(Y*R**(-1/3)). This proves the same Fourier extraction for
   F_- and the convolution restricted to I. No prime-power term is silently
   treated as a prime, and no corrected-H mean bound is imported from (7.10).
b. Use the source prime-indicator Lemma7.4 at P=R**4. Abel/Stieltjes
   multiplication by log n on bulk intervals cancels that lemma's log Y
   numerator, giving local density 1 for the principal character and
   -t**(beta-1) for the exceptional character. Multiplication cancels the
   source's discrete 1/log n main terms exactly. Converting integer windows
   to continuous averages costs O(P/Y) in the normalized estimate: only
   the principal and exceptional main characters contribute. This is
   absorbed even in the exceptional case by the checked lower bound
   1-beta >>P**(-1/2)/log(P)**2, together with the stated R range.
c. Every prime in I exceeds R**2. Thus source Lemma4.10 reconstructs
   F_-*b_R exactly with primitive characters. Use the corrected radical
   majorant, not the literal squarefree-supported H in that source.
   The exceptional continuous window average differs from n**(beta-1)
   by O((1-beta)/R**4), absorbed in e. Set E_-=0 on the endpoint strips.
   Their discarded L1 contribution is O_G(Y*R**(-2)*log Y*log R), as in
   major_arc_kernel.py. This proves (1), with the exceptional minus sign.
Primary source: https://arxiv.org/html/2508.16400v2#S7.SS3 , (7.10),
Lemma7.4 and the algebraic reconstruction of Lemma4.10. The original
source majorant's support correction is proved in major_arc_kernel.py.

Canonical-L theorem:
There is delta0>0 such that, for every fixed 0<delta<=delta0, all but
O_delta(X**(1-delta/8)) even m in [X,2X] satisfy L(m)>0, for large integer X.
The exponent and onset are not supplied numerically. This strengthens the
exceptional-set SIZE for this particular lower bound; it does not strengthen
the earlier L>=M/2 statement to a power-saving exceptional set, and does not
remove all exceptions. No historical novelty or Goldbach proof is claimed.
The small-conductor suppression is further localized in
character_suppression.py: outside its explicit residue family, a fixed
positive margin holds after excluding a separate Fourier-residual set.

Proof by composing the checked models:
1. Set Y=2X, R=Y**delta, J=floor(log(R)/(2*log(2))), and T=Y/2**J.
   Choose delta0<=1/1000 and eventually J>=1. Then
     Y*R**(-1/2)<=T<2Y*R**(-1/2).
   The interval I=(T,Y] is the disjoint union of I_j=(Y_j/2,Y_j],
   Y_j=Y/2**j, j=0,...,J-1. Fix z=floor(cuberoot(X-3)) throughout.
   Each half-interval satisfies both Fourier-model parameter conditions:
   R<=Y_j**(1/400), R>=exp(log(Y_j)**(4/5)), and
   Y_j**(1/4)<=z<=Y_j**(2/5), for sufficiently large X.
   All use the SAME R, cutoff G, exceptional alternative at level R**4,
   kernels Gamma,Xi, and rough-semiprime normalization k_z(n).
   Their errors e_j are bounded by a fixed multiple of the global e,
   because log(Y_j) lies between (1-delta/2)*log Y and log Y. The supports
   are disjoint, and sum_j Y_j<2Y. Adding the already checked half-interval
   identities therefore gives on I
     F_-=log(n)*1_prime(n), F_+=S_z(n)/k_z(n),
     F_+/-=M_+/-+E_+/-+V_+/-,
     |E_+/-|<<e*H_R(rad(n)), ||V_+/-hat||inf<<YR**(-1/3).      (2)
   Internal interval boundaries contribute only their already included
   errors. There is no extra factor J in the Fourier remainder.

2. The H second-moment estimate extends to I by summing the dyadic
   estimates: sum_I H**2<<Y*log Y/delta**2. For its additive correlation
   with m in [Y/2,Y], use symmetry to restrict n<=m/2, then cover
   (T,m/2] by dyadic intervals (x,2x], extending only the final lower
   interval if necessary. Here x>=T/2, 2x<=m/2 and m-n>=m/2>0.
   The proof in radical_majorant_correlation.py applies directly through
   Henriot's New Theorem5: ||u(m-u)||=m+1=O(Y), x>>Y**(1/4),
   log x is comparable to log Y, and R<=x/2. Its corrected local factors
   are unchanged, giving on each block O(x*S_2(m)/delta**2).
   Summing x=O(Y) proves sum_{n,m-n in I}H(n)H(m-n)<<Y*S_2(m)/delta**2.
   No polynomial zero is added by extending an interval in this argument.

3. The signed pair main-term proof also applies on I. Its periodic means
   are unchanged; the bias weights have uniformly bounded total variation.
   K_m=|{n:n,m-n in I}|=m-2*floor(T)-1>=Y/3 eventually. For the small
   exceptional conductor, v(n)*v(m-n)<=exp(-t), t=(1-beta)*log Y,
   because T**2>=Y. Thus the same linear margin holds, with
   mu=min(1,t)>>R**(-1/7), and the main error is O(YR**(-1/3)).
   For large D, the explicit gcd family still has O(YR**(-1/8)) targets
   in [Y/2,Y], and off it the margin has mu=1. With an absent exceptional
   model term, use the principal margin and mu=1.
   The H correlation in (2) above controls the pointwise error pairings.
   First choose the fixed delta small enough to make
   delta**(-3)*exp(-c/delta) (or its fixed-quality analogue) smaller than
   the main margin constant; then take Y large. The resulting perturbed
   model difference has a lower bound c*Y*S_2(m)*mu for rho=49/100.

4. For each sign, Q_+/-=F_+/-*F_+/--(M_+/-+E_+/-)*(M_+/-+E_+/-)
   equals V_+/-*(F_+/-+M_+/-+E_+/-). The pointwise bounds for F_+/- and
   the H second moment give, by Parseval,
     sum_m |Q_+/-(m)|**2 <<_delta Y**3*R**(-2/3)*log(Y)**2.
   In the small-conductor case a fixed small threshold c0*Y*mu excludes
   at most O_delta(Y*R**(-2/3)*log(Y)**2/mu**2)
   =O_delta(Y*R**(-1/3)) targets. In the other cases mu=1 and at most
   O_delta(Y*R**(-1/2)) targets are excluded. Union with the gcd family.
   Outside O_delta(Y*R**(-1/8)) even targets we have the ACTUAL weighted
   comparison, with positive quantitative margin
     F_-*F_-(m)-rho*F_+*F_+(m) >=c_delta*Y*mu,
   where uniformly mu>>R**(-1/7). The positive lower bound of S_2 was used.

5. Unweight without losing the margin. Every prime-pair weight on I is
   at most a=log(Y)**2. On [T,Y], the function k_z(n) is increasing for
   large Y: writing x=log n,Z=log z, its derivative has the sign of
     x/(x-Z)-log(x/Z-1),
   which is positive uniformly for x/Z near3. Each normalized semiprime
   pair weight is at least b=1/k_z(Y)**2. Also
     k_z(Y)*log Y=log(2)+o(1),
   including the exact integer cube-root cutoff. Since log(2)**2<49/100,
   rho*b>a eventually. If G_I and C_I^0 denote the unweighted ordered
   prime-pair and S_z-pair counts on I, then
     G_I-C_I^0 >= (F_-*F_-)/a-(F_+*F_+)/b
                >= (F_-*F_--rho*F_+*F_+)/a
                >= c_delta*Y*mu/log(Y)**2.                  (3)
   The second inequality has the indicated direction because rho*b>=a.

6. For the canonical target, z_m=floor(cuberoot(m-3))>=z. Every composite
   survivor C_m below m-3 has exactly TWO prime factors, both >z_m:
   three such factors would give n>=(z_m+1)**3>m-3. Consequently C_m
   is contained in S_z. No triprime error is needed in this containment.
   In the identity L=G-C_m*C_m+C_m(m/2), ignore the nonnegative diagonal.
   Pairs with at least one argument outside I occupy at most2*floor(T)
   ordered positions, since m<=Y. Hence
     L(m)>=G_I-C_I^0-2*floor(T).
   Finally T=O(YR**(-1/2))=o(YR**(-1/7)/log(Y)**2), so (3) proves L>0
   outside the stated set. All cutoffs and losses concern actual integer
   positions; positivity was never assumed in the parity recursion.
"""
from fractions import Fraction


def dyadic_intervals(upper: int, levels: int) -> tuple[tuple[Fraction, Fraction], ...]:
    """Exact half-open intervals, descending, partitioning (upper/2**levels,upper]."""
    if type(upper) is not int or upper < 1:
        raise ValueError("upper must be a positive integer")
    if type(levels) is not int or not 1 <= levels <= 64:
        raise ValueError("levels must be an integer in [1,64]")
    return tuple((Fraction(upper, 2**(j+1)), Fraction(upper, 2**j)) for j in range(levels))


def count_difference_floor(weighted_prime: int | Fraction,
                           weighted_semiprime: int | Fraction,
                           prime_pair_upper: int | Fraction,
                           semiprime_pair_lower: int | Fraction,
                           omitted_positions: int = 0) -> Fraction:
    """Conditional exact lower bound G-S-omitted from truthful weight bounds.

    This checks types and signs, not primality or the truth of the supplied
    total weights and per-pair bounds. No floating values or rounded roots.
    """
    values = (weighted_prime, weighted_semiprime, prime_pair_upper, semiprime_pair_lower)
    if any(type(value) not in (int, Fraction) for value in values):
        raise ValueError("weights and bounds must be exact rationals")
    if weighted_prime < 0 or weighted_semiprime < 0 or prime_pair_upper <= 0 or semiprime_pair_lower <= 0:
        raise ValueError("require nonnegative totals and positive per-pair bounds")
    if type(omitted_positions) is not int or omitted_positions < 0:
        raise ValueError("omitted_positions must be a nonnegative integer")
    return (Fraction(weighted_prime)/prime_pair_upper-
            Fraction(weighted_semiprime)/semiprime_pair_lower-omitted_positions)
