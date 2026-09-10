"""Factor-regime gate for the surviving long Mobius covariance blocks.

Owner: Kevin's Goldbach research.  Purpose: split the exact mu_>V*log
convolution by factor size and test the obvious factor-by-factor Parseval and
Cauchy route before seeking a stronger arithmetic theorem.  The route fails
on every surviving long n-block, but the factor regimes remain useful inputs
for a signed bilinear method.

SETUP.
Let the surviving n-block have length Y=N^y with

                     y>1499/2000=.7495.                  (1)

Dyadically restrict the Mobius divisor to a~A=N^alpha.  Since n is comparable
with N, the logarithmic cofactor has scale b~C=N^(1-alpha).  The exact tail
requires alpha>3/20=.15 apart from a harmless boundary bin.  Relative to the
prime modulus m=N^.59, the natural regimes are

 lower:     .15<alpha<=.41,  a<m and b>=m;
 balanced:  .41<alpha<.59,   a<m and b<m;
 upper:     alpha>=.59,       a>=m and b<=N^.41.          (2)

Constants and dyadic boundary bins around .41,.59 require epsilon slack; (2)
is an exponent classification, not a literal inequality for every finite N.

THE GENERIC FACTOR-BY-FACTOR BUDGET.
Choose the shorter factor as the outer Cauchy variable and write its scale as

 Z=N^s,       s=min(alpha,1-alpha)<=1/2.                 (3)

This choice is essential.  A fixed arbitrary factor A would leave
O(Y/A+1), not always O(Y/A), inner values.  But every surviving y>.7495 has
Z<Y, so for fixed outer variable the product condition cuts the other factor
to O(Y/Z+1)=O(Y/Z) values.  Parseval and residue collisions bound that inner
full h-energy by

             ((Y/Z)^2+q*Y/Z)*N^(o(1)).                  (4)

Cauchy across O(Z) outer values and summation of the inner energies gives

             (Y^2+Z*q*Y)*N^(o(1)).                      (5)

This works in either orientation: for alpha<=1/2 fix a, while for alpha>=1/2
fix b, using |mu(a)|<=1 and absorbing log b into N^(o(1)).  After the exact
outer mu(d)^2(log m)^2/q weight and d,m sums, (5) becomes

             (Y^2+Z*B*M*Y)*N^(o(1)).                    (6)

Thus the optimized orientation has exponent

 max(2y, y+s+599/1000).                                  (7)

The family term fits 1499/1000 only when

                       s<=9/10-y.                        (8)

For y just above .7495 this restricts the shorter factor to exponent about
.15; for y>=.9 no positive-length factor meets (8).  More decisively, the
collision term 2y exceeds 1499/1000 for every y in (1), independent of alpha.

DISPOSITION.
Fix-one-factor Parseval followed by Cauchy is falsified on ALL three regimes
of every surviving long block.  Splitting more finely in alpha cannot remove
the common Y^2 term.  This is not a barrier to the retained tools: it says the
Mobius signs or the m,h average must be used before that Cauchy step.

The regimes still distinguish possible new inputs.  In the balanced range
both factor scales are below m, superficially matching the support geometry
of an asymptotic-large-sieve diagonal theorem, though the local band
covariance is not covered.  In the lower range the short Mobius factor is in
the favorable orientation for a mollifier-like treatment.  In the upper
range the long Mobius factor and short logarithmic factor reverse that
orientation and remain the least matched to the checked source.  No theorem
for any of these local signed forms is claimed here.
"""

from fractions import Fraction as F


def long_block_factor_budget(block_length_exponent, mobius_factor_exponent):
    """Return the exact exponent ledger (7)--(8)."""
    y, alpha = block_length_exponent, mobius_factor_exponent
    if type(y) is not F or type(alpha) is not F:
        raise ValueError("exponents must be exact Fractions")
    if not F(1499, 2000) < y <= 1 or not F(3, 20) < alpha < 1:
        raise ValueError("require a surviving y and tail factor 3/20<alpha<1")
    beta = 1 - alpha
    family = F(599, 1000)
    target = F(1499, 1000)
    shorter = min(alpha, beta)
    if alpha <= F(41, 100):
        regime = "lower"
    elif alpha < F(59, 100):
        regime = "balanced"
    else:
        regime = "upper"
    return {
        "block_length": y,
        "mobius_factor": alpha,
        "log_factor": beta,
        "regime": regime,
        "shorter_factor": shorter,
        "shorter_factor_below_block_length": shorter < y,
        "collision_exponent": 2 * y,
        "a_oriented_family_exponent": y + alpha + family,
        "b_oriented_family_exponent": y + beta + family,
        "best_family_exponent": y + shorter + family,
        "short_factor_cap": F(9, 10) - y,
        "target": target,
        "collision_fits": 2 * y <= target,
        "best_family_fits": y + shorter + family <= target,
        "factor_by_factor_route_proves_block": (
            max(2 * y, y + shorter + family) <= target),
        "signed_bilinear_input_still_required": True,
    }
