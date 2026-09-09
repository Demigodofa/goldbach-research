"""Combine relative distribution and a cubic weight to localize composite loss.

Owner: Kevin's research. Purpose: bound the surviving positive semiprime
contribution by an arbitrarily small FIXED fraction of the prime-pair scale.
The exact helpers check the factor band and the enlarged sieve-index support.
They do not estimate primes, detect zeros or give numerical asymptotic onsets.

Sol checked the theory and actual files. Four focused exact tests passed
normally and with Python -O; these verify finite algebra and support only.

Deduction independently checked by Sol:
For each fixed 0<epsilon<=1/100, take delta>0 sufficiently small DEPENDING
ON epsilon, in particular delta<=epsilon/3, and the fixed u sufficiently
large. Keep the actual-zero assumptions, suppressed target m and original
pruned pool B_good at those delta,u, with t=(1-beta)*log(Y)<=1/log(Y).
Write S_2(m) for the full Goldbach singular series and L=log(Y). Put
  kappa=1/epsilon, K_kappa=(1+kappa)W-kappa*(chi*log^3)/log(n)^2,
  T_kappa(m)=sum_{p in B_good}log(p)*K_kappa(m-p).
For some absolute constant C, uniformly in the stated central target band,
  P(m)>=T_kappa(m)-C*epsilon*Y*S_2(m)*t-o_epsilon(Y*t). (1)
Here P is the SAME positive-first prime-pair mass. No positive lower bound
for T_kappa is asserted. This is not an o(Y*t) error for one fixed epsilon,
nor a same-delta or growing-kappa theorem. Constants/onsets in the little-o
may depend on the fixed parameters and are ineffective.

Near-square-root sieve reach:
1. Repeat the three-conductor proof in rare_twisted_bv.py with
     Q_epsilon=floor(Y^(1/2-epsilon)/D^3).
   The high-conductor bound becomes
     Y*t^2/L^12+Y^(1-epsilon)*L^C0+Y^(5/6+delta/2)*L^C0.
   These are still o(Y*t/L^6). The low and middle ranges, including the
   principal resonance, are unchanged; choose delta once for their fixed
   saving. Thus the squarefree rare-prime remainder budget through
     E_epsilon=floor(Q_epsilon/3)
   remains O(Y*t/L^6). Sources and the corrected bulk Linnik deduction are
   exactly those of rare_twisted_bv.py and relative_type_i.py.
2. Set R=floor(Y^(1/2-2*epsilon)). For every positive-sign prime w<q<=R,
   upper sieve q|(m-p) with the ORIGINAL cutoff z=ceil(Y^(delta/u)) and
   level floor(E_epsilon/q). Uniformly in q, this level is eventually at
   least c*Y^epsilon/D^3>=c*Y^(3*epsilon/4), whereas z^u=O_u(Y^delta).
   Thus the upper fundamental lemma applies at a fixed sufficiently large
   ratio. No requirement q<=sqrt(E_epsilon) is needed. Each supporting
   squarefree d is z-smooth, so (q,d)->q*d remains injective across all q.
   The O(t) reciprocal rarity above w and this SINGLE remainder budget give
     E_1(q<=R)<<Y*S_2(m)*t^2+Y*t/L^5=o(Y*t).
   This is the W-weighted semiprime error. For fixed kappa, its contribution
   to an upper bound for T_kappa is at most (1+kappa) times this quantity.

Uniform control in the surviving factor band:
3. For n=rq, with r negative-sign and q positive-sign primes, put a=log(q)/log(n).
   The cubic identity gives
     K_kappa(n)/log(n)=H(a)=2(1-a)-kappa*(1-a)*a*(2a-1).
   Positivity requires a<(1+sqrt(1+16*epsilon))/4<=1/2+2*epsilon.
   If also q>R and n<=Y, then a>1/2-2*epsilon. In this band H<=3:
   for a>=1/2, H<=1; below1/2 use a(1-a)<=1/4 and 1-2a<=4*epsilon.
   Hence remaining positive semiprimes satisfy
     Y^(1/2-2*epsilon)<q<Y^(1/2+2*epsilon), K_kappa(n)<=3L. (2)
4. Fix such q. If q|m the actual prime-first count is zero. Otherwise
   apply Henriot's corrected New Theorem5 to v and m-qv with
     x=y=Y/(2q), cutoff Z0=Y^(1/10), alpha=1/2,
     norm exponent=1/5, and theorem epsilon=1/2800.
   This cutoff is used only in this auxiliary upper bound; it does not
   change B_good. The actual primes v and m-qv both exceed Z0. Uniformly
   for q in[Y^(2/5),Y^(3/5)], x>=Y^(2/5)/2, product norm<=3Y, and
   x>=C0*(3Y)^(1/5) eventually. The theorem parameters are ABSOLUTE and
   independent of our epsilon,delta,u. Since q>Z0, the corrected local
   factors from multi_rare_partner.py give
     #{r prime: m-qr prime in the required intervals}
        << (Y/q)*S_2(m)/L^2,                            (3)
   with an absolute implicit constant. This avoids retaining an old
   delta/u-dependent sieve constant that could consume the epsilon saving.
   Source, printed p377: https://doi.org/10.1017/S0305004114000280

Actual rare-prime mass in the narrow band:
5. The checked bulk progression estimate, summed over the phi(D)/2
   positive residue classes, gives on every dyadic interval at scales
   Y^(2/5)..Y^(3/5) the prime-log density
     (1-v^(beta-1))/2
   with cumulative error O(X*(t^28+L^2/D)) on intervals inside[X,2X].
   Delta is small enough for exponent28 even at the smallest such scale.
   Partial summation with 1/(v*log(v)), followed by O(L) dyadic pieces,
   costs O(t^28+L^2/D), not O(L) times that error. Consequently, uniformly
   for 2/5<=a<b<=3/5,
     sum_{Y^a<q<=Y^b, q prime, chi(q)=+1}1/q
       =(b-a)*t/2+O(t^2+t^28+L^2/D).                  (4)
   Here (1-v^(beta-1))/log(v)=(1-beta)+O((1-beta)^2*log(v)).
   Siegel bounds and t<=1/L make the error in (4) o(t/loglog(Y)). Thus the
   reciprocal mass in (2) is2*epsilon*t+o(t/loglog(Y)). No independence
   between the two actual prime conditions is asserted.
6. Each remaining log(p)*K_kappa(n) is at most3L^2. Sum (3) over the
   actual positive-sign q using (4). The result is
     E_middle,K<=C*epsilon*Y*S_2(m)*t+o(Y*t)
   with C absolute, since S_2(m)<<loglog(Y). Repeated factors, multiple
   positive factors, and q<=R are handled by the existing o(Y*t) upper
   bounds times fixed1+kappa. Partners with W=0, and all other semiprimes
   with K_kappa<=0, contribute nonpositively. Dropping these terms in an
   UPPER bound for the new signed total proves (1).

The remaining requirement is a lower bound for T_kappa that exceeds the
displayed budget. Taking epsilon to0 with Y, or assuming positivity from
the original nonnegative total T, is not justified. No new actual Goldbach
coverage, numerical onset, zero existence or historical novelty follows.
"""
from fractions import Fraction as F

from log_weight_barrier import safe_subtraction_coefficients, semiprime_kernel
from major_arc_kernel import _factorization


def band_parameters(epsilon: F) -> tuple[F, F, F, F, F]:
    """Return (kappa, lower q exponent, upper q exponent, BV exponent, delta cap).

    Exact epsilon is a FIXED theorem parameter, not a numerical onset or a
    claim that the maximum allowed delta clears every implicit requirement.
    """
    if type(epsilon) is not F or not 0 < epsilon <= F(1, 100):
        raise ValueError("require exact Fraction 0<epsilon<=1/100")
    return 1/epsilon, F(1, 2)-2*epsilon, F(1, 2)+2*epsilon, F(1, 2)-epsilon, epsilon/3


def balanced_kernel_value(epsilon: F, positive_share: F) -> F:
    """Evaluate K/log(n) at a rational FORMAL share, without sampling prime logs."""
    kappa, *_ = band_parameters(epsilon)
    if type(positive_share) is not F or not 0 <= positive_share <= 1:
        raise ValueError("require an exact Fraction share in[0,1]")
    result = F(0)
    for coefficient in reversed(semiprime_kernel(safe_subtraction_coefficients((0, kappa)))):
        result = result*positive_share+coefficient
    return result


def sieve_level_certificate(level: int, factor_limit: int, cutoff: int, ratio: int) -> int:
    """Certify floor(level/q)>=cutoff^ratio for every q<=factor_limit.

    Return floor(level/factor_limit), or reject unsafe inputs. This is the
    exact integer support inequality, not a check of analytic sieve errors.
    """
    if any(type(v) is not int for v in (level, factor_limit, cutoff, ratio)):
        raise ValueError("require exact integer parameters")
    if not 2 <= cutoff < factor_limit <= level or ratio < 1:
        raise ValueError("require 2<=cutoff<factor_limit<=level and ratio>=1")
    minimum = level//factor_limit
    if minimum < cutoff**ratio:
        raise ValueError("insufficient sieve level for the requested ratio")
    return minimum


def extended_sieve_index_split(index: int, cutoff: int, level: int,
                               factor_limit: int) -> tuple[int, int] | None:
    """Recover the unique (q,d) with q<=factor_limit, q>cutoff and smooth d.

    q may exceed sqrt(level). This is algebraic support only; invoke the
    separate level certificate when a minimum sieve ratio is required.
    """
    if any(type(v) is not int for v in (index, cutoff, level, factor_limit)):
        raise ValueError("require exact integer parameters")
    if index < 1 or not 2 <= cutoff < factor_limit <= level:
        raise ValueError("require index>=1 and 2<=cutoff<factor_limit<=level")
    if index > level:
        return None
    factors = _factorization(index)
    if any(exponent != 1 for _, exponent in factors):
        return None
    large = [prime for prime, _ in factors if prime > cutoff]
    if len(large) != 1 or large[0] > factor_limit:
        return None
    return large[0], index//large[0]
