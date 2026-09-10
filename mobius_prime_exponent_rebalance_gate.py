"""Prime-companion exponent rebalancing gate for the open Mobius covariance.

Owner: Kevin's Goldbach research.  Purpose: test whether lowering the prime
modulus exponent from 59/100 can move the remaining balanced convolution into
a published beyond-one-half distribution theorem without reopening already
paid cofactor ranges.  It cannot, for an exact range reason.

CURRENT PARAMETRIC BUDGET.
Let the prime companion have exponent mu, retain the small divisor exponent
b=9/1000, shift exponent h=1/10, and Mobius cutoff v=3/20.  The absolute
active-band benchmark and U=1 Type-I energy exponents become

    benchmark = 1+b+mu-h = 909/1000+mu,
    type_I    = 2*(b+mu+v) = 159/500+2*mu.              (1)

Thus the old Type-I calculation has margin

    benchmark-type_I = 591/1000-mu.                    (2)

Lowering mu below .59 does not break that component.  The remaining actual
cofactor is strictly below N^.46, however, so its prime companion exponent is
strictly above .54, with .54 as its infimum.  The already proved
large-cofactor/dispersion estimates pay the complementary companion range at
or below .54; changing the split must not relabel that completed work as a
new open box.

WRIGHT'S TWO RANGE CONDITIONS HAVE NO INTERSECTION.
Use the most favorable d=1 prime modulus Q=N^mu and product X=N.  If the
longer convolution factor has exponent nu, Wright,
arXiv:2608.27732v1, Theorem 2.2 requires, with fixed epsilon slack,

    N_factor^34 * X^(-17+epsilon) <= Q
    and Q <= N_factor * X^(-epsilon).

At exponent level these require

    34*nu-17 < mu < nu.                                 (3)

There is a possible nu only if

    mu < (17+mu)/34, equivalently mu < 17/33=.51515... . (4)

This is disjoint from the unpaid mu>.54 range.  It also explains the direct
balanced-box failure: if both factors are below the modulus, then
nu<mu, contradicting the right inequality in (3) before any coefficient,
endpoint, or Fourier-band issue is considered.  Adding d<=N^.009 only makes
the modulus longer and cannot repair this range failure.

Classical Bombieri--Vinogradov is even farther away in this parametrization:
q=d*m has exponent b+mu, so a fixed power margin below N^.5 requires
mu<.491.  That is also outside
the unpaid companion range and makes the relative-to-m balanced interval
(1-mu,mu) empty.

DISPOSITION.
Prime-exponent rebalancing inside the actual unresolved range cannot license
either Wright Theorem 2.2 or classical BV.  This is a source-range exclusion,
not evidence that the covariance is large and not a reason to discard the
factor or polynomial identities.  A useful new input must either operate at
modulus exponent at least .54, exploit the active numerator average, or use
the linked Mobius/prime coefficients more strongly than these distribution
theorems.
"""

from fractions import Fraction as F


SMALL_DIVISOR = F(9, 1000)
SHIFT = F(1, 10)
MOBIUS_CUTOFF = F(3, 20)
UNPAID_COMPANION_FLOOR = F(54, 100)
WRIGHT_MODULUS_CEILING = F(17, 33)


def prime_exponent_rebalance_budget(companion_exponent):
    """Return exact inherited and source-range gates for a proposed mu."""
    mu = companion_exponent
    if type(mu) is not F or not 0 < mu < 1:
        raise ValueError("companion exponent must be an exact Fraction in (0,1)")
    benchmark = 1 + SMALL_DIVISOR + mu - SHIFT
    type_i = 2 * (SMALL_DIVISOR + mu + MOBIUS_CUTOFF)
    return {
        "companion": mu,
        "absolute_band_benchmark": benchmark,
        "u1_type_i": type_i,
        "u1_type_i_margin": benchmark - type_i,
        "u1_type_i_fits": type_i <= benchmark,
        "in_unpaid_companion_range": mu > UNPAID_COMPANION_FLOOR,
        "wright_possible_for_some_factor_scale": mu < WRIGHT_MODULUS_CEILING,
        "wright_long_factor_upper_endpoint": (17 + mu) / 34,
        "classical_bv_with_small_divisor": mu + SMALL_DIVISOR < F(1, 2),
        "relative_balanced_interval_nonempty": mu > F(1, 2),
    }


def wright_factor_range(companion_exponent):
    """Open exponent interval nu allowed by Wright's two Q-range conditions."""
    result = prime_exponent_rebalance_budget(companion_exponent)
    if not result["wright_possible_for_some_factor_scale"]:
        return None
    return (max(companion_exponent, F(1, 2)),
            result["wright_long_factor_upper_endpoint"])


if __name__ == "__main__":
    for mu in (F(59, 100), F(54, 100), F(17, 33), F(51, 100)):
        print(mu, prime_exponent_rebalance_budget(mu), wright_factor_range(mu))
